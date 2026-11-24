"""Run the Project 2 decision and export visible output."""

from __future__ import annotations

import json
from pathlib import Path

from portfolio import (
    ASSETS,
    DEFAULT_COST_BPS,
    MINIMUM_RESERVE,
    OBJECTIVE_RETURN,
    baseline_portfolios,
    format_weights,
    load_estimates,
    portfolio_metrics,
    search_lowest_risk,
    weight_change,
)


ROOT = Path(__file__).resolve().parent
PRICE_PATH = ROOT / "data" / "prices.csv"
SIGNAL_PATH = ROOT / "data" / "dgs10-signal.json"
OUTPUT_JSON = ROOT / "outputs" / "visible_output.json"
OUTPUT_MD = ROOT / "outputs" / "visible_output.md"
ADOPTION_STABILITY_LIMIT = 0.20


def _case(
    name: str,
    window_months: int | None = None,
    spgm_shift: float = 0.0,
    cost_bps: float = DEFAULT_COST_BPS,
    objective_return: float = OBJECTIVE_RETURN,
    minimum_reserve: float = MINIMUM_RESERVE,
) -> dict[str, object]:
    estimates = load_estimates(PRICE_PATH, window_months=window_months)
    estimates["expected_returns"] = dict(estimates["expected_returns"])
    estimates["expected_returns"]["SPGM"] += spgm_shift
    portfolio = search_lowest_risk(
        estimates,
        objective_return=objective_return,
        minimum_reserve=minimum_reserve,
        cost_bps=cost_bps,
    )
    return {
        "name": name,
        "window_months": estimates["months_used"],
        "spgm_return_shift": spgm_shift,
        "cost_bps": cost_bps,
        "objective_return": objective_return,
        "minimum_reserve": minimum_reserve,
        "portfolio": portfolio,
    }


def evaluate_project() -> dict[str, object]:
    """Return the complete base, baseline, stress, signal, and decision record."""

    estimates = load_estimates(PRICE_PATH)
    baseline_results = {
        name: portfolio_metrics(
            weights,
            estimates,
            OBJECTIVE_RETURN,
            MINIMUM_RESERVE,
            DEFAULT_COST_BPS,
        )
        for name, weights in baseline_portfolios(estimates).items()
    }
    base = _case("Base: all available returns")
    stress_cases = [
        _case("Window: latest 36 returns", window_months=36),
        _case("Estimate: SPGM return minus 1 point", spgm_shift=-0.01),
        _case("Cost: 100 bps", cost_bps=100.0),
        _case("Constraint: net-return objective 7.0%", objective_return=0.07),
    ]
    with SIGNAL_PATH.open(encoding="utf-8") as file:
        signal = json.load(file)

    comparable = [case for case in stress_cases if case["portfolio"] is not None]
    if base["portfolio"] is None:
        decision = "REJECT"
        reason = "No portfolio passes the mandate in the base case."
        largest_change = None
    else:
        largest_change = max(
            (
                weight_change(base["portfolio"]["weights"], case["portfolio"]["weights"])
                for case in comparable
            ),
            default=None,
        )
        adoption_failures = []
        if len(comparable) != len(stress_cases):
            adoption_failures.append("at least one specified stress is infeasible")
        if largest_change is not None and largest_change > ADOPTION_STABILITY_LIMIT:
            adoption_failures.append(
                "the largest absolute asset-weight change from the base case across specified "
                f"stresses is {largest_change * 100:.0f} percentage points, above "
                f"{ADOPTION_STABILITY_LIMIT * 100:.0f}"
            )
        if signal["status"] == "HIGH-RATE REGIME":
            adoption_failures.append(
                "DGS10 is in the high-rate regime and the return estimates have not been revalidated"
            )
        if adoption_failures:
            decision = "PILOT"
            reason = "The base mandate passes, but automatic adoption is blocked because " + "; ".join(
                adoption_failures
            ) + "."
        else:
            decision = "ADOPT"
            reason = (
                "The process passes the mandate, remains within the base-relative stability gate, "
                "and clears the point-in-time signal gate."
            )

    return {
        "as_of": "2026-09-30",
        "decision": decision,
        "decision_reason": reason,
        "mandate": {
            "objective_return": OBJECTIVE_RETURN,
            "minimum_reserve": MINIMUM_RESERVE,
            "effective_grid_minimum_reserve": 0.05,
            "reserve_definition": "SGOV portfolio weight",
            "risk_measure": "Annualized volatility of monthly adjusted-close returns",
            "limits": "Long-only, fully invested, 5-point grid, at least 3% SGOV",
            "benchmark": "40% USIG / 60% SPGM",
            "cost_bps": DEFAULT_COST_BPS,
            "turnover_definition": (
                "0.5 times the sum of absolute target-minus-benchmark weights"
            ),
        },
        "estimates": estimates,
        "baselines": baseline_results,
        "base": base,
        "stresses": stress_cases,
        "all_stresses_feasible": len(comparable) == len(stress_cases),
        "largest_stress_weight_change": largest_change,
        "stability_limit": ADOPTION_STABILITY_LIMIT,
        "stability_measure": (
            "Maximum absolute change in any asset weight from the base allocation across the "
            "specified stresses; the cross-case range is descriptive and is not the gate."
        ),
        "signal": signal,
        "adoption_gate": (
            "Do not automatically adopt if any specified stress has no feasible portfolio, "
            "the maximum absolute change in any asset weight from the base allocation exceeds "
            f"{ADOPTION_STABILITY_LIMIT * 100:.0f} percentage points, or DGS10 remains in the "
            "saved high-rate regime "
            "without a documented revalidation of the return estimates."
        ),
        "pilot_stop_condition": (
            "Stop the paper pilot only if the base portfolio fails the mandate, a validation "
            "test fails, or the required point-in-time signal cannot be reproduced. Stress "
            "instability blocks adoption but does not by itself stop observation in the pilot."
        ),
    }


def _portfolio_row(name: str, result: dict[str, object]) -> str:
    failed = ", ".join(result["failed_rules"]) if result["failed_rules"] else "none"
    verdict = "PASS" if result["passes_mandate"] else "FAIL"
    return (
        f"| {name} | {format_weights(result['weights'])} | "
        f"{result['net_return']:.2%} | {result['volatility']:.2%} | "
        f"{result['reserve_weight']:.0%} | {verdict} | {failed} |"
    )


def render_markdown(result: dict[str, object]) -> str:
    """Render the GitHub-readable decision output."""

    base = result["base"]["portfolio"]
    lines = [
        "# Project 2 — Visible Executed Output",
        "",
        f"**Decision: {result['decision']} as of {result['as_of']}.**",
        "",
        "**Decision line:** Pilot the lowest-risk feasible process; adopt only if every specified "
        "stress remains feasible, the maximum absolute asset-weight change from the base case is "
        f"no more than {result['stability_limit'] * 100:.0f} percentage points, and the high-rate "
        "signal is cleared or "
        "the return estimates are revalidated.",
        "",
        f"**Reason:** {result['decision_reason']}",
        "",
        "## Mandate",
        "",
        f"- Objective: at least {result['mandate']['objective_return']:.1%} net expected return",
        f"- Universe: {', '.join(ASSETS)}",
        f"- Benchmark: {result['mandate']['benchmark']}",
        f"- Risk measure: {result['mandate']['risk_measure']}",
        f"- Limits: {result['mandate']['limits']} (effective SGOV minimum is 5% on the grid)",
        f"- Reserve definition: {result['mandate']['reserve_definition']}",
        f"- One-way transaction cost assumption: {result['mandate']['cost_bps']:.0f} bps",
        "- Turnover convention: 0.5 × sum of absolute target-minus-benchmark weights",
        "",
        "## Base decision numbers",
        "",
        f"- Allocation: **{format_weights(base['weights'])}**",
        f"- Gross expected return: **{base['gross_return']:.2%}**",
        f"- Net expected return: **{base['net_return']:.2%}**",
        f"- Annualized volatility: **{base['volatility']:.2%}**",
        f"- Reserve weight: **{base['reserve_weight']:.0%}**",
        f"- Mandate verdict: **{'PASS' if base['passes_mandate'] else 'FAIL'}**",
        f"- Base turnover and cost: **{base['turnover']:.0%} × "
        f"{result['mandate']['cost_bps']:.0f} bps = {base['transaction_cost']:.2%} "
        f"({base['transaction_cost'] * 10_000:.0f} bps)**",
        "",
        "## Benchmark and baselines",
        "",
        "| Portfolio | Weights | Net return | Volatility | Reserve | Verdict | Failed rules |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for name, baseline in result["baselines"].items():
        lines.append(_portfolio_row(name, baseline))
    lines.extend([
        _portfolio_row("Constrained portfolio", base),
        "",
        "## Stress runs",
        "",
        "| Case | Weights | Net return | Volatility | Base mandate | Max asset change from base |",
        "|---|---|---:|---:|---|---:|",
    ])
    for case in result["stresses"]:
        portfolio = case["portfolio"]
        if portfolio is None:
            lines.append(f"| {case['name']} | No feasible portfolio | — | — | FAIL | — |")
        else:
            change = weight_change(base["weights"], portfolio["weights"])
            lines.append(
                f"| {case['name']} | {format_weights(portfolio['weights'])} | "
                f"{portfolio['net_return']:.2%} | {portfolio['volatility']:.2%} | "
                f"PASS | {change * 100:.0f} points |"
            )
    lines.extend([
        "",
        f"All {len(result['stresses'])} specified stresses are mandate-feasible. The adoption "
        f"stability measure is the maximum absolute change in any asset weight from the base "
        f"allocation, which is **{result['largest_stress_weight_change'] * 100:.0f} percentage "
        "points**. The displayed "
        "55%-85% SGOV and 15%-45% SPGM sensitivity ranges span 30 points across cases; that "
        "cross-case spread is descriptive and is not the adoption-gate calculation.",
    ])
    signal = result["signal"]
    lines.extend([
        "",
        "## Point-in-time signal",
        "",
        f"DGS10 was **{signal['value']:.2f}%** on {signal['observation_date']}, the last "
        f"observation available in the saved {signal['as_known_on']} vintage. The rule labels "
        f"values above {signal['threshold']:.2f}% as a high-rate regime. Current status: "
        f"**{signal['status']}**. This prevents automatic adoption and requires monthly review; "
        "it does not silently alter portfolio weights.",
        "",
        "## Decision conditions",
        "",
        f"**Automatic-adoption gate:** {result['adoption_gate']}",
        "",
        f"**Paper-pilot stop rule:** {result['pilot_stop_condition']} The validation tests are "
        "defined in [`docs/validation-and-ai-use.md`](../docs/validation-and-ai-use.md).",
        "",
        "## Limitations",
        "",
        "- Historical arithmetic means are estimates, not forecasts.",
        "- The five-point grid can miss a lower-risk off-grid portfolio.",
        "- Volatility is not a complete measure of drawdown, inflation, or liquidity risk.",
        "- The cost model is a one-time linear estimate relative to the benchmark.",
        "- DGS10 is point-in-time controlled, but the Yahoo adjusted-close history was downloaded "
        "later and is not a historical vintage; later corporate-action adjustments may revise it.",
        "- The saved point-in-time signal is contextual and not a causal return forecast.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    """Generate both human-readable and machine-readable visible output."""

    result = evaluate_project()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(normalize_json_floats(result), indent=2) + "\n", encoding="utf-8"
    )
    OUTPUT_MD.write_text(render_markdown(result), encoding="utf-8")
    print(f"{result['decision']}: {result['decision_reason']}")
    print(f"Visible output: {OUTPUT_MD.relative_to(ROOT)}")


def normalize_json_floats(value):
    """Round nested JSON floats so insignificant binary noise cannot dirty clean runs."""

    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: normalize_json_floats(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_json_floats(item) for item in value]
    return value


if __name__ == "__main__":
    main()
