"""Static quality checks for the unrun cross-session benchmark manifest."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "cross_session"
MANIFEST = BENCHMARK / "scenarios.json"
EXPECTED_CONDITIONS = {
    "no-memory",
    "concise-agents",
    "plain-summary",
    "project-memory",
}


class CrossSessionManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_unrun_protocol_version(self) -> None:
        self.assertEqual(self.manifest["schema_version"], 1)
        self.assertEqual(self.manifest["status"], "unrun")
        self.assertEqual(
            {c["id"] for c in self.manifest["conditions"]},
            EXPECTED_CONDITIONS,
        )

    def test_sessions_are_ordered_and_unique(self) -> None:
        sessions = self.manifest["sessions"]
        ids = [session["id"] for session in sessions]
        self.assertEqual(ids, ["session1", "session2", "session3"])
        for session in sessions:
            self.assertEqual(session["grader_phase"], session["id"])
            self.assertTrue(session["task"].strip())
            self.assertTrue(session["memory_review"])

    def test_declared_paths_exist_and_do_not_escape_repository(self) -> None:
        declared = [
            self.manifest["base_fixture"],
            self.manifest["grading"]["behavior_suite"],
        ]
        for value in declared:
            path = (ROOT / value).resolve()
            self.assertTrue(path.is_relative_to(ROOT.resolve()))
            self.assertTrue(path.exists(), f"missing benchmark resource: {value}")

    def test_pilot_is_not_mislabeled_as_measured(self) -> None:
        self.assertIn("actual_provider_input_tokens", self.manifest["grading"]["additional_metrics"])
        self.assertTrue(self.manifest["grading"]["unknown_is_null"])
        self.assertIn("not a completed agent evaluation", (BENCHMARK / "README.md").read_text(encoding="utf-8"))

    def test_hidden_grader_parses(self) -> None:
        import ast

        path = ROOT / self.manifest["grading"]["behavior_suite"]
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


if __name__ == "__main__":
    unittest.main()
