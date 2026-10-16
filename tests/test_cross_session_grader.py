"""Check the offline grader detects the missing feature in the pristine v0.2 fixture."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SRC = ROOT / "benchmarks" / "fixture-project" / "src"
GRADER = ROOT / "benchmarks" / "cross_session" / "grader"


class CrossSessionGraderTests(unittest.TestCase):
    def test_pristine_fixture_correctly_fails_session1(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(FIXTURE_SRC)
        env["BENCHMARK_SESSION"] = "session1"
        process = subprocess.run(
            [
                sys.executable, "-m", "unittest", "discover",
                "-s", str(GRADER), "-p", "test_*.py", "-v",
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        combined = process.stdout + process.stderr
        self.assertIn("AttributeError", combined)
        self.assertIn("rename_task", combined)
        # Old completion behavior should still be verified independently.
        self.assertIn("test_existing_completion_api_contract_is_unchanged", combined)


if __name__ == "__main__":
    unittest.main()
