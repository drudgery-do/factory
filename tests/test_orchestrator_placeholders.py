import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OrchestratorPlaceholderTests(unittest.TestCase):
    def run_script(self, *args):
        result = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return json.loads(result.stdout)

    def test_deploy_risk_classifier_marks_docs_as_green(self):
        payload = self.run_script(
            "orchestrator/scripts/classify_deploy_risk.py",
            "--summary",
            "docs and copy update only",
        )

        self.assertEqual(payload["risk"], "green")
        self.assertIn("docs", payload["matched_rules"])

    def test_deploy_risk_classifier_marks_disclaimer_change_as_red(self):
        payload = self.run_script(
            "orchestrator/scripts/classify_deploy_risk.py",
            "--summary",
            "change public disclaimer language",
        )

        self.assertEqual(payload["risk"], "red")
        self.assertIn("disclaimer", payload["matched_rules"])
        self.assertTrue(payload["requires_human_approval"])

    def test_quality_gate_runner_reports_placeholder_checks(self):
        payload = self.run_script("orchestrator/scripts/run_quality_gate.py")

        self.assertEqual(payload["status"], "pass")
        self.assertGreaterEqual(payload["checks_total"], 10)
        self.assertIn("portfolio.yaml", payload["checks"])
        self.assertIn("deploy_review_policy", payload["checks"])


if __name__ == "__main__":
    unittest.main()
