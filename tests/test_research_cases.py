"""Fixture schema checks only; no Gemini calls or behavioral pass claims."""

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class ResearchCaseTests(unittest.TestCase):
    def test_twelve_unique_cases_explicitly_start_unexecuted(self):
        path = ROOT / "evals/admin-research/cases.yml"
        self.assertTrue(path.is_file(), "Research case fixtures are missing")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["evaluation_kind"], "authored_fixtures_not_model_results")
        cases = data["cases"]
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({case["id"] for case in cases}), 12)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["execution_status"], "not_run")
                for key in ("prompt", "lane", "material_claims", "required", "forbidden",
                            "source_policy", "pass_rule"):
                    self.assertTrue(case[key], key)
                self.assertIn(case["lane"], ("Fast non-research", "Quick evidence",
                                            "Standard evidence", "Deep evidence"))


if __name__ == "__main__":
    unittest.main()
