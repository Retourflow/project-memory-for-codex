#!/usr/bin/env python3
"""Validate a Codex Project Memory installation using only the standard library."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BUDGETS = {
    "AGENTS.md": ("lines", 150),
    "docs/PROJECT_CONTEXT.md": ("words", 800),
    "docs/CURRENT_STATE.md": ("words", 500),
    "docs/ARCHITECTURE.md": ("words", 2000),
    "docs/DECISIONS.md": ("words", 4000),
    "docs/CHANGELOG.md": ("words", 4000),
}

REQUIRED_HEADINGS = {
    "docs/PROJECT_CONTEXT.md": ["Purpose", "Goals", "Constraints", "Success Criteria"],
    "docs/CURRENT_STATE.md": ["Implemented", "In Progress", "Planned Next", "Known Issues"],
    "docs/ARCHITECTURE.md": ["System Overview", "Components", "Data Flow"],
}

PLACEHOLDER_PATTERN = re.compile(r"\b(TBD|FIXME)\b", re.IGNORECASE)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative_path, (unit, limit) in BUDGETS.items():
        path = root / relative_path
        if not path.is_file():
            errors.append(f"missing: {relative_path}")
            continue

        text = path.read_text(encoding="utf-8")
        size = len(text.splitlines()) if unit == "lines" else word_count(text)
        if size > limit:
            errors.append(f"budget exceeded: {relative_path} has {size} {unit}, limit is {limit}")

        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"unresolved placeholder: {relative_path} contains TBD or FIXME")

        headings = re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
        duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
        if duplicates:
            errors.append(
                f"duplicate headings: {relative_path} repeats {', '.join(duplicates)}"
            )

        for heading in REQUIRED_HEADINGS.get(relative_path, []):
            if heading not in headings:
                errors.append(f"missing heading: {relative_path} requires '## {heading}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check project memory files, required sections, and context budgets."
    )
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    errors = validate(root)

    if errors:
        print("Project memory validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Project memory validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
