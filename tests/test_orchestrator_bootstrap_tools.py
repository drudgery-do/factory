import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OrchestratorBootstrapToolTests(unittest.TestCase):
    def run_json(self, *args):
        result = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return json.loads(result.stdout)

    def run_text(self, *args):
        result = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout

    def test_risk_classifier_routes_red_gates_to_human_approval(self):
        payload = self.run_json(
            "orchestrator/scripts/classify_deploy_risk.py",
            "--summary",
            "first GPL seed approval for Funeral Price Pages",
            "--stream",
            "funeral-price-pages",
        )

        self.assertEqual(payload["task_id"], "ORCH-003")
        self.assertEqual(payload["risk"], "red")
        self.assertEqual(payload["approval_required"], "human")
        self.assertFalse(payload["release_reviewer_can_approve"])
        self.assertIn("human_owner", payload["required_approver_roles"])
        self.assertIn("first_gpl", payload["matched_rules"])

    def test_risk_classifier_uses_changed_files_for_sensitive_paths(self):
        payload = self.run_json(
            "orchestrator/scripts/classify_deploy_risk.py",
            "--summary",
            "update workflow permissions",
            "--changed-file",
            ".github/workflows/deploy-production.yml",
            "--changed-file",
            ".codex/config.toml",
        )

        self.assertEqual(payload["risk"], "red")
        self.assertIn("production_deploy_workflow", payload["matched_rules"])
        self.assertIn("codex_config", payload["matched_rules"])

    def test_progress_scorer_reports_backlog_counts_and_next_items(self):
        payload = self.run_json("orchestrator/scripts/score_progress.py")

        self.assertEqual(payload["task_id"], "ORCH-004")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["portfolio"]["orchestrator"]["total"], 5)
        self.assertGreaterEqual(payload["portfolio"]["orchestrator"]["done"], 2)
        self.assertIn("ORCH-003", payload["items"]["orchestrator"])
        ephemera_next = payload["next_backlog"]["ephemera-weaver"]
        if ephemera_next is None:
            self.assertEqual(
                payload["portfolio"]["ephemera-weaver"]["done"],
                payload["portfolio"]["ephemera-weaver"]["total"],
            )
        else:
            self.assertIn(ephemera_next, payload["items"]["ephemera-weaver"])

    def test_daily_digest_generator_outputs_markdown_summary(self):
        digest = self.run_text(
            "orchestrator/scripts/summarize_status.py",
            "--date",
            "2026-06-06",
            "--format",
            "markdown",
        )

        self.assertIn("# Daily Digest", digest)
        self.assertIn("Date: 2026-06-06", digest)
        self.assertIn("ORCH-003", digest)
        self.assertIn("Ephemera Weaver", digest)
        self.assertIn("No production deploys without explicit approval.", digest)

    def test_approval_card_generator_outputs_red_gate_card(self):
        card = self.run_text(
            "orchestrator/scripts/generate_approval_card.py",
            "--task",
            "FPP-001",
            "--stream",
            "funeral-price-pages",
            "--summary",
            "first GPL seed approval",
            "--requested-by",
            "orchestrator",
        )

        self.assertIn("# Approval Card", card)
        self.assertIn("Task: FPP-001", card)
        self.assertIn("Risk classification: red", card)
        self.assertIn("Human Owner or Delegate", card)
        self.assertIn("No production secrets added.", card)


if __name__ == "__main__":
    unittest.main()
