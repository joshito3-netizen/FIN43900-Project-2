"""Interactive committee interface for the Project 2 portfolio process."""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from analysis import PRICE_PATH, SIGNAL_PATH, evaluate_project
from portfolio import (
    ASSETS,
    ASSET_NAMES,
    DEFAULT_COST_BPS,
    MINIMUM_RESERVE,
    OBJECTIVE_RETURN,
    baseline_portfolios,
    format_weights,
    load_estimates,
    portfolio_metrics,
    search_lowest_risk,
)


st.set_page_config(page_title="Project 2 Portfolio Pilot", layout="wide")
st.title("Project 2 — Portfolio Process Pilot")
st.caption("Built with OpenAI Codex assistance; the student owns the final analysis and decision.")
st.caption("Educational use only — not investment advice.")

with st.sidebar:
    st.header("Move one control")
    window_label = st.selectbox(
        "Estimation window",
        ("All 59 monthly returns", "Latest 36 monthly returns"),
    )
    spgm_shift_points = st.slider(
        "SPGM expected-return shift (percentage points)", -3.0, 3.0, 0.0, 0.25
    )
    objective_percent = st.slider(
        "Net expected-return objective (%)", 4.0, 9.0, OBJECTIVE_RETURN * 100, 0.25
    )
    reserve_percent = st.slider(
        "Minimum SGOV reserve (%)", 0.0, 50.0, MINIMUM_RESERVE * 100, 1.0
    )
    cost_bps = st.slider(
        "One-way transaction cost (bps)", 0, 150, int(DEFAULT_COST_BPS), 5
    )
    st.caption("Weights are long-only, fully invested, and searched in five-point steps.")

window_months = 36 if window_label.startswith("Latest") else None
estimates = load_estimates(PRICE_PATH, window_months=window_months)
estimates["expected_returns"] = dict(estimates["expected_returns"])
estimates["expected_returns"]["SPGM"] += spgm_shift_points / 100.0

candidate = search_lowest_risk(
    estimates,
    objective_return=objective_percent / 100.0,
    minimum_reserve=reserve_percent / 100.0,
    cost_bps=cost_bps,
)

if candidate is None:
    st.error("MANDATE VERDICT: FAIL — no portfolio on the five-point grid passes every rule.")
else:
    st.success("MANDATE VERDICT: PASS — the displayed constrained portfolio passes every rule.")
    st.subheader("Constrained portfolio")
    weight_columns = st.columns(len(ASSETS))
    for column, asset in zip(weight_columns, ASSETS):
        column.metric(asset, f"{candidate['weights'][asset]:.0%}")
        column.caption(ASSET_NAMES[asset])
    metric_columns = st.columns(4)
    metric_columns[0].metric("Net expected return", f"{candidate['net_return']:.2%}")
    metric_columns[1].metric("Annualized volatility", f"{candidate['volatility']:.2%}")
    metric_columns[2].metric("SGOV reserve", f"{candidate['reserve_weight']:.0%}")
    metric_columns[3].metric("Turnover vs benchmark", f"{candidate['turnover']:.0%}")

st.subheader("Benchmark and transparent baselines")
rows = []
for name, weights in baseline_portfolios(estimates).items():
    result = portfolio_metrics(
        weights,
        estimates,
        objective_return=objective_percent / 100.0,
        minimum_reserve=reserve_percent / 100.0,
        cost_bps=cost_bps,
    )
    rows.append(
        {
            "Portfolio": name,
            "Weights": format_weights(result["weights"]),
            "Net return": f"{result['net_return']:.2%}",
            "Volatility": f"{result['volatility']:.2%}",
            "Reserve": f"{result['reserve_weight']:.0%}",
            "Mandate": "PASS" if result["passes_mandate"] else "FAIL",
            "Failed rules": ", ".join(result["failed_rules"]) or "none",
        }
    )
if candidate is not None:
    rows.append(
        {
            "Portfolio": "Constrained portfolio",
            "Weights": format_weights(candidate["weights"]),
            "Net return": f"{candidate['net_return']:.2%}",
            "Volatility": f"{candidate['volatility']:.2%}",
            "Reserve": f"{candidate['reserve_weight']:.0%}",
            "Mandate": "PASS",
            "Failed rules": "none",
        }
    )
st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

with st.expander("Inputs and estimates", expanded=False):
    estimate_rows = [
        {
            "Ticker": asset,
            "Annualized arithmetic return": f"{estimates['expected_returns'][asset]:.2%}",
            "Annualized volatility": f"{estimates['volatilities'][asset]:.2%}",
        }
        for asset in ASSETS
    ]
    st.write(
        f"The selected window uses {estimates['months_used']} monthly returns from "
        f"{estimates['start_date']} through {estimates['end_date']}."
    )
    st.dataframe(pd.DataFrame(estimate_rows), hide_index=True, use_container_width=True)

frozen = evaluate_project()
st.subheader("Frozen stress conclusion")
st.write(f"**Project recommendation: {frozen['decision']}.** {frozen['decision_reason']}")
stress_rows = []
for case in frozen["stresses"]:
    result = case["portfolio"]
    stress_rows.append(
        {
            "Case": case["name"],
            "Weights": "No feasible portfolio" if result is None else format_weights(result["weights"]),
            "Mandate": "FAIL" if result is None else "PASS",
        }
    )
st.dataframe(pd.DataFrame(stress_rows), hide_index=True, use_container_width=True)
st.caption(
    "Stop rather than adopt if a specified stress becomes infeasible, if any asset moves more "
    "than 20 points from base, or if the point-in-time signal cannot be reproduced."
)

with SIGNAL_PATH.open(encoding="utf-8") as file:
    signal = json.load(file)
st.subheader("Point-in-time signal and data card")
st.info(
    f"{signal['series_id']} = {signal['value']:.2f}% on {signal['observation_date']}, "
    f"as known on {signal['as_known_on']}: {signal['status']}."
)
st.markdown(
    f"""
- **Meaning:** {signal['name']}
- **Source:** [{signal['source']}]({signal['source_url']})
- **Units/frequency:** {signal['units']}; {signal['frequency']}
- **Publication lag:** {signal['publication_lag']}
- **As-of rule:** {signal['revision_rule']}
- **Decision rule:** Above {signal['threshold']:.2f}% prevents automatic adoption and triggers monthly review; it does not silently change weights.
"""
)
