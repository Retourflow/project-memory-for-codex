import tempfile
import unittest
from pathlib import Path

from scripts.validate_skill import validate_skill


ROOT = Path(__file__).resolve().parents[1]


class SkillValidationTests(unittest.TestCase):
    def test_repository_skill_passes(self) -> None:
        errors = validate_skill(ROOT / "skill" / "codex-project-memory")
        self.assertEqual(errors, [])

    def test_extra_frontmatter_key_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: example-skill\n"
                "description: Use this example skill for tests.\n"
                "version: 1\n"
                "---\n"
                "# Example\n",
                encoding="utf-8",
            )

            errors = validate_skill(skill)

            self.assertIn(
                "SKILL.md frontmatter must contain only name and description", errors
            )

    def test_folder_and_skill_name_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "folder-name"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: different-name\n"
                "description: Use this example skill for tests.\n"
                "---\n"
                "# Example\n",
                encoding="utf-8",
            )

            errors = validate_skill(skill)

            self.assertIn("skill name must match folder name", errors)


if __name__ == "__main__":
    unittest.main()
