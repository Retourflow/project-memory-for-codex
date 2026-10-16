#!/usr/bin/env python3
"""Create an isolated, condition-specific StudyFlow benchmark workspace.

Preparation only. Does NOT run an agent or publish benchmark metrics.
Core code uses only Python's standard library (Git CLI for optional history).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "benchmarks" / "fixture-project"
CONDITIONS = (
    "no-memory",
    "concise-agents",
    "plain-summary",
    "project-memory",
)

NEUTRAL = """# Agent Instructions

Test changes before claiming verification. Preserve existing contracts and
security boundaries. Inspect source code instead of guessing implementation.
Do not store or disclose secrets, credentials, or private information.
"""

CONCISE = NEUTRAL + """
## Concise project state

StudyFlow is a layered Python task service with SQLite persistence.
Keep the v1 API response keys: id, title, completed.
Notifications originate in the service layer, not API handlers.
Current behavior: create/list/complete tasks; email adapter exists but is not wired.
Notification failures are not retried.

Update this short section at the end of meaningful work to reflect what is
actually done, tested, blocked, and next. Do not claim untested work passed.
"""

PLAIN_INSTRUCTIONS = NEUTRAL + """
## Handoff

Read HANDOFF.md before non-trivial work, verify against source, and update
HANDOFF.md after meaningful changes. Keep the next action and incomplete
work clear. A regular summary is sufficient; no special memory framework.
"""

INITIAL_HANDOFF = """# Project handoff

StudyFlow is a Python task service with SQLite persistence. The service
owns task behavior and notification dispatch; API handlers stay thin.
Preserve the v1 id/title/completed response keys.
Implemented: task creation, listing, completion, SQLite repository,
console notification. An email adapter exists but is not wired.
Known issue: notification failures are not retried.
Next before the pilot: use the session task to decide what to implement.
"""


def prepare_workspace(
    destination: Path, condition: str, *, initialize_git: bool = True
) -> Path:
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition: {condition}")

    dest = destination.expanduser().resolve()
    fixture = FIXTURE.resolve()

    if dest.exists():
        raise FileExistsError(f"refusing to overwrite workspace: {dest}")
    if dest == fixture or fixture in dest.parents:
        raise ValueError("workspace must not be inside the source fixture")

    shutil.copytree(fixture, dest)
    docs = dest / "docs"
    agents = dest / "AGENTS.md"

    if condition != "project-memory":
        shutil.rmtree(docs)
        if condition == "no-memory":
            agents.write_text(NEUTRAL, encoding="utf-8")
        elif condition == "concise-agents":
            agents.write_text(CONCISE, encoding="utf-8")
        else:
            agents.write_text(PLAIN_INSTRUCTIONS, encoding="utf-8")
            (dest / "HANDOFF.md").write_text(INITIAL_HANDOFF, encoding="utf-8")
    else:
        # Install the actual v0.2 project-memory instructions, validator, Skill.
        agents.write_text(
            (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        scripts = dest / "scripts"
        scripts.mkdir(exist_ok=True)
        shutil.copy2(ROOT / "scripts" / "validate.py", scripts / "validate.py")
        skill_dir = dest / ".agents" / "skills" / "codex-project-memory"
        shutil.copytree(ROOT / "skill" / "codex-project-memory", skill_dir)

    if initialize_git:
        subprocess.run(["git", "init", "-q", "-b", "main", str(dest)], check=True)
        subprocess.run(["git", "-C", str(dest), "add", "-A"], check=True)
        subprocess.run(
            [
                "git", "-C", str(dest),
                "-c", "user.name=Benchmark Seed",
                "-c", "user.email=seed@example.invalid",
                "commit", "-qm", "benchmark: initial fixture",
            ],
            check=True,
        )

    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=CONDITIONS, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument(
        "--no-git", action="store_true", help="Skip initializing fixture Git history"
    )
    args = parser.parse_args()
    path = prepare_workspace(
        args.workspace, args.condition, initialize_git=not args.no_git
    )
    print(f"Prepared {args.condition} workspace: {path}")
    print("No agent task or benchmark scoring has been run.")


if __name__ == "__main__":
    main()
