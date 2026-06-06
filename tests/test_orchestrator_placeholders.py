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

    def test_quality_gate_runner_validates_orch_002_policy_checks(self):
        payload = self.run_script("orchestrator/scripts/run_quality_gate.py")

        self.assertEqual(payload["task_id"], "ORCH-002")
        self.assertNotIn("placeholder", payload["note"].lower())
        for check_name in [
            "scaffold_files",
            "stream_files",
            "backlog_ids",
            "deploy_review_policy",
            "pr_evidence_pack",
            "codex_agent_boundaries",
            "workflow_deploy_safety",
            "stream_red_gates",
            "no_production_secrets",
        ]:
            self.assertEqual(payload["checks"][check_name]["status"], "pass")

    def test_quality_gate_runner_reports_first_backlog_entries(self):
        payload = self.run_script("orchestrator/scripts/run_quality_gate.py")

        self.assertEqual(
            payload["first_backlog_entries"]["orchestrator"],
            ["ORCH-001", "ORCH-002", "ORCH-003", "ORCH-004", "ORCH-005"],
        )
        self.assertEqual(payload["first_backlog_entries"]["ephemera-weaver"][0], "EPH-001")
        self.assertEqual(payload["first_backlog_entries"]["bid-spec-atlas"][0], "BSA-001")
        self.assertEqual(payload["first_backlog_entries"]["funeral-price-pages"][0], "FPP-001")


if __name__ == "__main__":
    unittest.main()
