"""Known-answer and failure tests for the Project 2 engine."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from analysis import PRICE_PATH, SIGNAL_PATH, evaluate_project, normalize_json_floats
from portfolio import (
    baseline_portfolios,
    grid_weights,
    load_estimates,
    portfolio_metrics,
    search_lowest_risk,
    validate_weights,
    weight_change,
)


class ProjectTwoKnownAnswers(unittest.TestCase):
    def setUp(self):
        self.estimates = load_estimates(PRICE_PATH)

    def test_base_known_answer(self):
        result = search_lowest_risk(self.estimates)
        self.assertIsNotNone(result)
        self.assertEqual(result["weights"], {"SGOV": 0.60, "SCHR": 0.0, "USIG": 0.0, "SPGM": 0.40})
        self.assertEqual(f"{result['net_return']:.2%}", "6.74%")
        self.assertEqual(f"{result['volatility']:.2%}", "6.02%")
        self.assertTrue(result["passes_mandate"])

    def test_json_float_normalization_rounds_nested_values(self):
        value = {"outer": [0.2310728220411379, {"inner": 1.23456789012345}], "count": 2}
        self.assertEqual(
            normalize_json_floats(value),
            {"outer": [0.231072822041, {"inner": 1.234567890123}], "count": 2},
        )

    def test_baseline_verdicts_name_failed_rules(self):
        results = {
            name: portfolio_metrics(weights, self.estimates)
            for name, weights in baseline_portfolios(self.estimates).items()
        }
        self.assertEqual(results["Mandate benchmark"]["failed_rules"], ["reserve"])
        self.assertIn("net_return", results["Equal weight"]["failed_rules"])
        self.assertIn("net_return", results["Inverse volatility"]["failed_rules"])

    def test_latest_36_month_window_changes_25_points(self):
        base = search_lowest_risk(self.estimates)
        recent = search_lowest_risk(load_estimates(PRICE_PATH, window_months=36))
        self.assertIsNotNone(base)
        self.assertIsNotNone(recent)
        self.assertEqual(recent["weights"], {"SGOV": 0.85, "SCHR": 0.0, "USIG": 0.0, "SPGM": 0.15})
        self.assertEqual(weight_change(base["weights"], recent["weights"]), 0.25)

    def test_one_point_spgm_return_stress_propagates(self):
        stressed = load_estimates(PRICE_PATH)
        stressed["expected_returns"] = dict(stressed["expected_returns"])
        stressed["expected_returns"]["SPGM"] -= 0.01
        result = search_lowest_risk(stressed)
        self.assertEqual(result["weights"], {"SGOV": 0.55, "SCHR": 0.0, "USIG": 0.0, "SPGM": 0.45})

    def test_constraint_stress_propagates(self):
        result = search_lowest_risk(self.estimates, objective_return=0.07)
        self.assertIsNotNone(result)
        self.assertEqual(result["weights"], {"SGOV": 0.55, "SCHR": 0.0, "USIG": 0.0, "SPGM": 0.45})
        self.assertGreaterEqual(result["net_return"], 0.07)

    def test_transaction_cost_bridge(self):
        result = search_lowest_risk(self.estimates)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result["turnover"], 0.60)
        self.assertAlmostEqual(result["transaction_cost"], 0.0012)
        self.assertAlmostEqual(
            result["gross_return"] - result["transaction_cost"],
            result["net_return"],
        )

    def test_price_lineage_boundary(self):
        prices = pd.read_csv(PRICE_PATH)
        self.assertEqual(len(prices), 60)
        self.assertEqual(prices.iloc[0]["Date"], "2021-10-01")
        self.assertEqual(prices.iloc[-1]["Date"], "2026-09-01")
        self.assertFalse(prices.isna().any().any())

    def test_bad_price_data_fail_loudly(self):
        prices = pd.read_csv(PRICE_PATH)
        prices.loc[4, "SGOV"] = -1.0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad-prices.csv"
            prices.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "present and positive"):
                load_estimates(path)

    def test_grid_contains_each_allocation_once(self):
        portfolios = list(grid_weights())
        keys = {tuple(weights.values()) for weights in portfolios}
        self.assertEqual(len(portfolios), 1771)
        self.assertEqual(len(keys), len(portfolios))

    def test_invalid_weights_fail_loudly(self):
        with self.assertRaisesRegex(ValueError, "sum to 100%"):
            validate_weights({"SGOV": 0.5, "SCHR": 0.0, "USIG": 0.0, "SPGM": 0.4})

    def test_point_in_time_signal_respects_as_of_date(self):
        signal = json.loads(SIGNAL_PATH.read_text(encoding="utf-8"))
        self.assertLessEqual(signal["observation_date"], signal["as_known_on"])
        self.assertEqual(signal["status"], "HIGH-RATE REGIME")

    def test_project_decision_is_pilot(self):
        result = evaluate_project()
        self.assertEqual(result["decision"], "PILOT")
        self.assertTrue(result["all_stresses_feasible"])
        self.assertEqual(result["largest_stress_weight_change"], 0.25)
        self.assertEqual(result["stability_limit"], 0.20)
        self.assertIn("from the base allocation", result["stability_measure"])
        self.assertIn("automatically adopt", result["adoption_gate"])
        self.assertIn("Stop the paper pilot only", result["pilot_stop_condition"])
        self.assertIn("25 percentage points", result["decision_reason"])
        self.assertIn("high-rate regime", result["decision_reason"])
        self.assertEqual(len(result["stresses"]), 4)
        self.assertEqual(result["stresses"][-1]["objective_return"], 0.07)

    def test_cross_case_range_is_distinct_from_stability_gate(self):
        result = evaluate_project()
        feasible = [case["portfolio"] for case in result["stresses"] if case["portfolio"]]
        sgov_weights = [portfolio["weights"]["SGOV"] for portfolio in feasible]
        self.assertAlmostEqual(max(sgov_weights) - min(sgov_weights), 0.30)
        self.assertAlmostEqual(result["largest_stress_weight_change"], 0.25)


if __name__ == "__main__":
    unittest.main()
