"""Tests the external CLI session runner without claiming a real-agent result."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from benchmarks.cross_session.prepare import prepare_workspace
from benchmarks.cross_session.run_session import (
    checked_command, run_session, sha256, git_snapshot, memory_artifact_warnings,
)


class CrossSessionRunnerTests(unittest.TestCase):
    def test_smoke_red_fixture_and_no_hidden_grader_leak(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            work = folder / "agent_workspace"
            records = folder / "records"
            prepare_workspace(work, "no-memory")
            # Reads task from stdin but does not edit the fixture.
            cmd = [sys.executable, "-c", "import sys; print(len(sys.stdin.read()))"]
            output = run_session(
                work, records, "no-memory", "session1", cmd,
                timeout=20, smoke=True,
            )
            self.assertEqual(output["runner_mode"], "smoke")
            self.assertEqual(output["agent_returncode"], 0)
            self.assertFalse(output["grader_pass"])
            self.assertIsNone(output["actual_provider_input_tokens"])
            self.assertEqual(output["memory_review_status"], "not_reviewed")
            self.assertFalse(output["public_comparison_ready"])
            self.assertFalse(
                (work / "benchmarks" / "cross_session" / "grader").exists()
            )
            self.assertTrue((records / "session1" / "grader_stderr.txt").exists())
            stored = json.loads(
                (records / "session1" / "record.json").read_text(encoding="utf-8")
            )
            self.assertEqual(stored["prompt_sha256"], output["prompt_sha256"])

    def test_second_stage_requires_previous_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            work = root / "agent_workspace"
            prepare_workspace(work, "plain-summary")
            with self.assertRaises(FileNotFoundError):
                run_session(
                    work, root / "records", "plain-summary", "session2",
                    [sys.executable, "-c", "print('unused')"], smoke=True,
                )

    def test_all_three_stages_keep_the_workspace_and_fresh_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "agent_workspace"
            records = root / "records"
            prepare_workspace(workspace, "plain-summary")
            cmd = [sys.executable, "-c", "import sys;sys.stdin.read()"]
            for stage in ("session1", "session2", "session3"):
                result = run_session(
                    workspace, records, "plain-summary", stage, cmd, smoke=True,
                    timeout=20,
                )
                self.assertIsNone(result["agent_error"])
                self.assertFalse(result["grader_pass"])
            self.assertEqual(
                len(list(records.glob("session*/record.json"))), 3
            )
            with self.assertRaises(FileExistsError):
                run_session(
                    workspace, records, "plain-summary", "session3", cmd,
                    smoke=True, timeout=20,
                )

    def test_invalid_command_and_invalid_output_dir(self) -> None:
        self.assertEqual(checked_command('["python", "-c", "print(1)"]'),
                         ["python", "-c", "print(1)"])
        for bad in ("[]", '"python"', '["python", 2]', "not_json"):
            with self.subTest(bad=bad):
                with self.assertRaises((ValueError, json.JSONDecodeError)):
                    checked_command(bad)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "agent_workspace"
            prepare_workspace(workspace, "no-memory", initialize_git=False)
            with self.assertRaises(ValueError):
                run_session(
                    workspace, workspace / "records", "no-memory", "session1",
                    [sys.executable, "-c", "print('unused')"], smoke=True,
                )

    def test_baseline_contamination_review_flags_extra_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "agent_workspace"
            prepare_workspace(workspace, "no-memory", initialize_git=False)
            self.assertEqual(memory_artifact_warnings(workspace, "no-memory"), [])
            (workspace / "HANDOFF.md").write_text(
                "Created by an agent", encoding="utf-8"
            )
            self.assertEqual(
                memory_artifact_warnings(workspace, "no-memory"), ["HANDOFF.md"]
            )
            self.assertEqual(
                memory_artifact_warnings(workspace, "plain-summary"), []
            )

    def test_git_snapshot_and_sha_are_deterministic(self) -> None:
        self.assertEqual(sha256("a"), sha256("a"))
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "workspace"
            prepare_workspace(work, "no-memory")
            snapshot = git_snapshot(work)
            self.assertIsNotNone(snapshot["head_sha"])
            self.assertEqual(snapshot["status"], "")


if __name__ == "__main__":
    unittest.main()
