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


def _case(
    name: str,
    window_months: int | None = None,
    spgm_shift: float = 0.0,
    cost_bps: float = DEFAULT_COST_BPS,
) -> dict[str, object]:
    estimates = load_estimates(PRICE_PATH, window_months=window_months)
    estimates["expected_returns"] = dict(estimates["expected_returns"])
    estimates["expected_returns"]["SPGM"] += spgm_shift
    portfolio = search_lowest_risk(
        estimates,
        objective_return=OBJECTIVE_RETURN,
        minimum_reserve=MINIMUM_RESERVE,
        cost_bps=cost_bps,
    )
    return {
        "name": name,
        "window_months": estimates["months_used"],
        "spgm_return_shift": spgm_shift,
        "cost_bps": cost_bps,
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
    ]
    with SIGNAL_PATH.open(encoding="utf-8") as file:
        signal = json.load(file)

    if base["portfolio"] is None:
        decision = "REJECT"
        reason = "No portfolio passes the mandate in the base case."
        largest_change = None
    else:
        comparable = [case for case in stress_cases if case["portfolio"] is not None]
        largest_change = max(
            weight_change(base["portfolio"]["weights"], case["portfolio"]["weights"])
            for case in comparable
        )
        if len(comparable) != len(stress_cases) or largest_change > 0.20:
            decision = "PILOT"
            reason = (
                "The process passes the base mandate but changes by more than 20 percentage "
                "points under a specified stress or loses feasibility."
            )
        else:
            decision = "ADOPT"
            reason = "The process passes the mandate and remains within the stability limit."

    return {
        "as_of": "2026-09-30",
        "decision": decision,
        "decision_reason": reason,
        "mandate": {
            "objective_return": OBJECTIVE_RETURN,
            "minimum_reserve": MINIMUM_RESERVE,
            "risk_measure": "Annualized volatility of monthly adjusted-close returns",
            "limits": "Long-only, fully invested, 5-point grid, at least 3% SGOV",
            "benchmark": "40% USIG / 60% SPGM",
            "cost_bps": DEFAULT_COST_BPS,
        },
        "estimates": estimates,
        "baselines": baseline_results,
        "base": base,
        "stresses": stress_cases,
        "largest_stress_weight_change": largest_change,
        "signal": signal,
        "stop_condition": (
            "Stop rather than adopt if any specified stress has no feasible portfolio, "
            "the largest asset-weight change exceeds 20 points, or the saved signal cannot "
            "be reproduced with an as-of vintage."
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
        "**Decision line:** Pilot the lowest-risk feasible process; adopt only if the largest "
        "allocation change is no more than 20 percentage points across the specified stresses "
        "and every case remains mandate-feasible.",
        "",
        f"**Reason:** {result['decision_reason']}",
        "",
        "## Mandate",
        "",
        f"- Objective: at least {result['mandate']['objective_return']:.1%} net expected return",
        f"- Universe: {', '.join(ASSETS)}",
        f"- Benchmark: {result['mandate']['benchmark']}",
        f"- Risk measure: {result['mandate']['risk_measure']}",
        f"- Limits: {result['mandate']['limits']}",
        f"- One-way transaction cost assumption: {result['mandate']['cost_bps']:.0f} bps",
        "",
        "## Base decision numbers",
        "",
        f"- Allocation: **{format_weights(base['weights'])}**",
        f"- Gross expected return: **{base['gross_return']:.2%}**",
        f"- Net expected return: **{base['net_return']:.2%}**",
        f"- Annualized volatility: **{base['volatility']:.2%}**",
        f"- Reserve weight: **{base['reserve_weight']:.0%}**",
        f"- Mandate verdict: **{'PASS' if base['passes_mandate'] else 'FAIL'}**",
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
        "| Case | Weights | Net return | Volatility | Mandate | Change from base |",
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
                f"PASS | {change:.0%} |"
            )
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
        "## Stop condition",
        "",
        result["stop_condition"],
        "",
        "## Limitations",
        "",
        "- Historical arithmetic means are estimates, not forecasts.",
        "- The five-point grid can miss a lower-risk off-grid portfolio.",
        "- Volatility is not a complete measure of drawdown, inflation, or liquidity risk.",
        "- The cost model is a one-time linear estimate relative to the benchmark.",
        "- The saved point-in-time signal is contextual and not a causal return forecast.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    """Generate both human-readable and machine-readable visible output."""

    result = evaluate_project()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(result), encoding="utf-8")
    print(f"{result['decision']}: {result['decision_reason']}")
    print(f"Visible output: {OUTPUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
