"""Known-answer and failure tests for the Project 2 engine."""

from __future__ import annotations

import json
import unittest

from analysis import PRICE_PATH, SIGNAL_PATH, evaluate_project
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
        self.assertEqual(result["largest_stress_weight_change"], 0.25)


if __name__ == "__main__":
    unittest.main()
