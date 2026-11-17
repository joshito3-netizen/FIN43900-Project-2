"""Deterministic portfolio engine for FIN 43900 Project 2."""

from __future__ import annotations

from itertools import combinations
from math import isclose, sqrt
from pathlib import Path
from typing import Mapping, Sequence

import pandas as pd


ASSETS = ("SGOV", "SCHR", "USIG", "SPGM")
ASSET_NAMES = {
    "SGOV": "iShares 0–3 Month Treasury Bond ETF",
    "SCHR": "Schwab Intermediate-Term U.S. Treasury ETF",
    "USIG": "iShares Broad USD Investment Grade Corporate Bond ETF",
    "SPGM": "SPDR Portfolio MSCI Global Stock Market ETF",
}
BENCHMARK_WEIGHTS = {"SGOV": 0.0, "SCHR": 0.0, "USIG": 0.40, "SPGM": 0.60}
OBJECTIVE_RETURN = 0.065
MINIMUM_RESERVE = 0.03
RESERVE_ASSETS = ("SGOV",)
GRID_STEP = 0.05
DEFAULT_COST_BPS = 20.0


def load_estimates(
    csv_path: str | Path, window_months: int | None = None
) -> dict[str, object]:
    """Estimate annualized arithmetic returns, volatility, and correlation."""

    prices = pd.read_csv(csv_path)
    if list(prices.columns) != ["Date", *ASSETS]:
        raise ValueError(f"Price columns must be Date, {', '.join(ASSETS)} in that order.")
    prices["Date"] = pd.to_datetime(prices["Date"], errors="raise")
    if prices["Date"].duplicated().any() or not prices["Date"].is_monotonic_increasing:
        raise ValueError("Price dates must be unique and ordered oldest first.")
    values = prices[list(ASSETS)].apply(pd.to_numeric, errors="raise")
    if values.isna().any().any() or (values <= 0.0).any().any():
        raise ValueError("Every adjusted-close price must be present and positive.")

    monthly_returns = values.pct_change(fill_method=None).dropna()
    if window_months is not None:
        if window_months < 2:
            raise ValueError("The estimation window must contain at least two returns.")
        monthly_returns = monthly_returns.tail(window_months)
    if len(monthly_returns) < 2:
        raise ValueError("At least three monthly prices are required.")

    expected_returns = monthly_returns.mean() * 12.0
    volatilities = monthly_returns.std(ddof=1) * sqrt(12.0)
    correlations = monthly_returns.corr()
    if (volatilities <= 0.0).any():
        raise ValueError("Volatility must be positive for every asset.")
    return {
        "assets": ASSETS,
        "expected_returns": {asset: float(expected_returns[asset]) for asset in ASSETS},
        "volatilities": {asset: float(volatilities[asset]) for asset in ASSETS},
        "correlations": {
            asset: {other: float(correlations.loc[asset, other]) for other in ASSETS}
            for asset in ASSETS
        },
        "months_used": len(monthly_returns),
        "start_date": prices.loc[monthly_returns.index[0], "Date"].date().isoformat(),
        "end_date": prices.loc[monthly_returns.index[-1], "Date"].date().isoformat(),
    }


def validate_weights(weights: Mapping[str, float]) -> None:
    """Require one long-only weight per asset and a 100% total."""

    if set(weights) != set(ASSETS):
        raise ValueError("Weights must include every asset exactly once.")
    if any(weight < 0.0 for weight in weights.values()):
        raise ValueError("Weights must be long-only.")
    if not isclose(sum(weights.values()), 1.0, abs_tol=1e-10):
        raise ValueError("Weights must sum to 100%.")


def covariance_matrix(estimates: Mapping[str, object]) -> dict[str, dict[str, float]]:
    """Convert volatilities and correlations into a covariance matrix."""

    volatilities = estimates["volatilities"]
    correlations = estimates["correlations"]
    return {
        asset: {
            other: (
                correlations[asset][other]
                * volatilities[asset]
                * volatilities[other]
            )
            for other in ASSETS
        }
        for asset in ASSETS
    }


def inverse_volatility_weights(volatilities: Mapping[str, float]) -> dict[str, float]:
    """Return transparent inverse-volatility baseline weights."""

    if any(volatilities[asset] <= 0.0 for asset in ASSETS):
        raise ValueError("Inverse-volatility weights require positive volatility.")
    inverse = {asset: 1.0 / volatilities[asset] for asset in ASSETS}
    total = sum(inverse.values())
    return {asset: inverse[asset] / total for asset in ASSETS}


def portfolio_metrics(
    weights: Mapping[str, float],
    estimates: Mapping[str, object],
    objective_return: float = OBJECTIVE_RETURN,
    minimum_reserve: float = MINIMUM_RESERVE,
    cost_bps: float = DEFAULT_COST_BPS,
) -> dict[str, object]:
    """Calculate measures and a rule-by-rule mandate verdict."""

    validate_weights(weights)
    if not 0.0 <= minimum_reserve <= 1.0:
        raise ValueError("Minimum reserve must be between 0% and 100%.")
    if cost_bps < 0.0:
        raise ValueError("Transaction cost cannot be negative.")

    expected_returns = estimates["expected_returns"]
    covariance = covariance_matrix(estimates)
    gross_return = sum(weights[asset] * expected_returns[asset] for asset in ASSETS)
    variance = sum(
        weights[asset] * weights[other] * covariance[asset][other]
        for asset in ASSETS
        for other in ASSETS
    )
    reserve_weight = sum(weights[asset] for asset in RESERVE_ASSETS)
    turnover = 0.5 * sum(
        abs(weights[asset] - BENCHMARK_WEIGHTS[asset]) for asset in ASSETS
    )
    transaction_cost = turnover * cost_bps / 10_000.0
    net_return = gross_return - transaction_cost
    rules = {
        "net_return": net_return + 1e-12 >= objective_return,
        "reserve": reserve_weight + 1e-12 >= minimum_reserve,
        "long_only": all(weight >= 0.0 for weight in weights.values()),
        "fully_invested": isclose(sum(weights.values()), 1.0, abs_tol=1e-10),
    }
    failed_rules = [name for name, passed in rules.items() if not passed]
    return {
        "weights": dict(weights),
        "gross_return": gross_return,
        "net_return": net_return,
        "volatility": sqrt(max(variance, 0.0)),
        "reserve_weight": reserve_weight,
        "turnover": turnover,
        "transaction_cost": transaction_cost,
        "rules": rules,
        "passes_mandate": not failed_rules,
        "failed_rules": failed_rules,
    }


def baseline_portfolios(estimates: Mapping[str, object]) -> dict[str, dict[str, float]]:
    """Return the mandate benchmark and two transparent baselines."""

    return {
        "Mandate benchmark": dict(BENCHMARK_WEIGHTS),
        "Equal weight": {asset: 1.0 / len(ASSETS) for asset in ASSETS},
        "Inverse volatility": inverse_volatility_weights(estimates["volatilities"]),
    }


def grid_weights(step: float = GRID_STEP):
    """Yield every long-only portfolio on an exact fixed-weight grid."""

    units = round(1.0 / step)
    if step <= 0.0 or not isclose(units * step, 1.0, abs_tol=1e-12):
        raise ValueError("Grid step must divide 100% into equal whole units.")
    for dividers in combinations(range(units + len(ASSETS) - 1), len(ASSETS) - 1):
        boundaries = (-1, *dividers, units + len(ASSETS) - 1)
        counts = [
            boundaries[index + 1] - boundaries[index] - 1
            for index in range(len(ASSETS))
        ]
        yield {asset: count / units for asset, count in zip(ASSETS, counts)}


def search_lowest_risk(
    estimates: Mapping[str, object],
    objective_return: float = OBJECTIVE_RETURN,
    minimum_reserve: float = MINIMUM_RESERVE,
    cost_bps: float = DEFAULT_COST_BPS,
    step: float = GRID_STEP,
) -> dict[str, object] | None:
    """Find the lowest-volatility grid portfolio that passes every rule."""

    best = None
    for weights in grid_weights(step):
        metrics = portfolio_metrics(
            weights, estimates, objective_return, minimum_reserve, cost_bps
        )
        if not metrics["passes_mandate"]:
            continue
        if best is None or metrics["volatility"] < best["volatility"] - 1e-15:
            best = metrics
    return best


def weight_change(first: Mapping[str, float], second: Mapping[str, float]) -> float:
    """Return the largest absolute asset-weight change."""

    return max(abs(first[asset] - second[asset]) for asset in ASSETS)


def format_weights(weights: Mapping[str, float]) -> str:
    """Format weights in the fixed universe order."""

    return " / ".join(f"{asset} {weights[asset]:.0%}" for asset in ASSETS)
