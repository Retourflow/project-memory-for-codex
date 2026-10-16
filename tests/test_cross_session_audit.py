"""Evidence audit must surface facts without claiming automated truth."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from benchmarks.cross_session.audit_memory import (
    create_packet, defined_functions, memory_excerpts,
)
from benchmarks.cross_session.prepare import prepare_workspace


class MemoryAuditTests(unittest.TestCase):
    def test_unmodified_fixture_has_no_rename_api(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            work = Path(root) / "case"
            prepare_workspace(work, "project-memory", initialize_git=False)
            packet = create_packet(work)
            self.assertFalse(packet["source_evidence"]["api_rename_defined"]["defined"])
            self.assertFalse(packet["source_evidence"]["service_rename_defined"]["defined"])
            self.assertFalse(packet["source_evidence"]["repository_rename_defined"]["defined"])
            self.assertEqual(packet["review"]["memory_truth_status"], "not_reviewed")
            self.assertTrue(packet["review"]["human_review_required"])
            self.assertIsNone(packet["review"]["false_completion_count"])

    def test_syntactic_api_presence_produces_candidate_not_false_verdict(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            work = Path(root) / "case"
            prepare_workspace(work, "plain-summary", initialize_git=False)
            (work / "src" / "studyflow" / "api.py").write_text(
                "def rename_task(service, task_id, title):\n    pass\n", encoding="utf-8"
            )
            with (work / "HANDOFF.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\n- API title edit adapter is unfinished; implement next.\n"
                )
            packet = create_packet(work)
            self.assertTrue(packet["source_evidence"]["api_rename_defined"]["defined"])
            self.assertGreater(len(packet["potential_stale_api_claims"]), 0)
            self.assertEqual(packet["review"]["memory_truth_status"], "not_reviewed")

    def test_function_extraction_is_structural_only(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            source = Path(root) / "code.py"
            source.write_text(
                "class API:\n    def rename_task(self):\n        pass\n"
                "def another():\n    pass\n", encoding="utf-8"
            )
            parsed = defined_functions(source)
            self.assertEqual(parsed[0]["name"], "rename_task")
            self.assertEqual(parsed[0]["class"], "API")
            self.assertEqual(parsed[1]["name"], "another")

    def test_ordinary_baseline_has_no_memory_excerpts(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            work = Path(root) / "case"
            prepare_workspace(work, "no-memory", initialize_git=False)
            self.assertEqual(memory_excerpts(work), [])


if __name__ == "__main__":
    unittest.main()
