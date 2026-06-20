#!/usr/bin/env python3
"""Validate the repository's Codex Skill without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]

    try:
        frontmatter, _body = text[4:].split("\n---\n", 1)
    except ValueError:
        return {}, ["SKILL.md frontmatter is not closed"]

    values: dict[str, str] = {}
    errors: list[str] = []
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values, errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["missing SKILL.md"]

    values, parse_errors = _parse_frontmatter(
        skill_file.read_text(encoding="utf-8")
    )
    errors.extend(parse_errors)

    if set(values) != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")

    name = values.get("name", "")
    if name != skill_dir.name:
        errors.append("skill name must match folder name")
    if not NAME_PATTERN.fullmatch(name):
        errors.append("skill name must use lowercase hyphen-case")
    if not values.get("description"):
        errors.append("skill description must not be empty")

    metadata = skill_dir / "agents" / "openai.yaml"
    if metadata.is_file():
        text = metadata.read_text(encoding="utf-8")
        for field in ("interface:", "display_name:", "short_description:", "default_prompt:"):
            if field not in text:
                errors.append(f"agents/openai.yaml is missing {field}")
        if f"${name}" not in text:
            errors.append("default_prompt must reference the skill by $name")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Codex Skill directory.")
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    errors = validate_skill(args.skill_dir.resolve())
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
