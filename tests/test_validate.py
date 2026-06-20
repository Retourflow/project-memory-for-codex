import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate.py"


class ValidateTests(unittest.TestCase):
    def initialize(self, target: Path) -> None:
        subprocess.run(
            ["bash", str(ROOT / "scripts" / "init.sh"), str(target)],
            check=True,
            capture_output=True,
            text=True,
        )

    def run_validator(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(target)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_generated_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.initialize(target)
            result = self.run_validator(target)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.initialize(target)
            (target / "docs" / "CURRENT_STATE.md").unlink()
            result = self.run_validator(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing: docs/CURRENT_STATE.md", result.stdout)

    def test_context_budget_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.initialize(target)
            context = target / "docs" / "PROJECT_CONTEXT.md"
            context.write_text(context.read_text() + "\nword " * 900, encoding="utf-8")
            result = self.run_validator(target)
            self.assertEqual(result.returncode, 1)
            self.assertIn("budget exceeded: docs/PROJECT_CONTEXT.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
