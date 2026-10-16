"""Workspace isolation checks; no agents or model APIs are used."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from benchmarks.cross_session.prepare import CONDITIONS, FIXTURE, prepare_workspace


class PrepareCrossSessionTests(unittest.TestCase):
    def test_each_condition_preserves_identical_application_code(self) -> None:
        original = (FIXTURE / "src" / "studyflow" / "service.py").read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            for condition in CONDITIONS:
                with self.subTest(condition=condition):
                    dest = Path(tmp) / condition
                    prepare_workspace(dest, condition, initialize_git=False)
                    self.assertEqual(
                        (dest / "src" / "studyflow" / "service.py").read_bytes(),
                        original,
                    )
                    self.assertTrue((dest / "tests" / "test_service.py").exists())
                    self.assertFalse(
                        (dest / "benchmarks" / "cross_session" / "grader").exists()
                    )

    def test_baselines_do_not_receive_specialized_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for condition in ("no-memory", "concise-agents", "plain-summary"):
                with self.subTest(condition=condition):
                    dest = Path(tmp) / condition
                    prepare_workspace(dest, condition, initialize_git=False)
                    self.assertFalse((dest / "docs").exists())
                    self.assertFalse((dest / ".agents" / "skills").exists())

            no_memory = Path(tmp) / "no-memory"
            self.assertNotIn("Current behavior:", (no_memory / "AGENTS.md").read_text())
            plain = Path(tmp) / "plain-summary"
            self.assertTrue((plain / "HANDOFF.md").exists())
            concise = Path(tmp) / "concise-agents"
            self.assertFalse((concise / "HANDOFF.md").exists())

    def test_project_memory_has_real_skill_and_validator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project-memory"
            prepare_workspace(dest, "project-memory", initialize_git=False)
            self.assertTrue((dest / "docs" / "CURRENT_STATE.md").exists())
            self.assertTrue((dest / "scripts" / "validate.py").exists())
            self.assertTrue(
                (dest / ".agents" / "skills" / "codex-project-memory" / "SKILL.md").exists()
            )

    def test_refuses_to_overwrite_existing_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):
                prepare_workspace(Path(tmp), "no-memory", initialize_git=False)

    def test_rejects_unknown_condition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                prepare_workspace(Path(tmp) / "new", "wrong", initialize_git=False)


if __name__ == "__main__":
    unittest.main()
