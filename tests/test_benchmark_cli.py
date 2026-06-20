import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "benchmarks" / "run.py"


class BenchmarkCliTests(unittest.TestCase):
    def test_cli_writes_reports_without_agent_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            result = subprocess.run(
                [sys.executable, str(RUNNER), "--output", str(output)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((output / "latest.json").read_text())
            self.assertEqual(len(report["results"]), 18)
            self.assertIn("Wrote benchmark reports", result.stdout)

    def test_cli_imports_example_agent_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            agent_results = ROOT / "benchmarks" / "results" / "example-agent-results.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--output",
                    str(output),
                    "--agent-results",
                    str(agent_results),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((output / "latest.json").read_text())
            measured = [
                row
                for row in report["results"]
                if row["agent_metrics"]["task_success"] is not None
            ]
            self.assertEqual(len(measured), 1)


if __name__ == "__main__":
    unittest.main()
