#!/usr/bin/env python3
"""Generate a source-based evidence packet for HUMAN handoff-truth review.

This tool is NOT a semantic truth oracle. Presence of a method in the AST
doesn't prove that its implementation works; use the independent behavior
grader for that. It does not make a pass/fail claim about project memory.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

MODULES = {
    "api_rename_defined": "src/studyflow/api.py",
    "service_rename_defined": "src/studyflow/service.py",
    "repository_rename_defined": "src/studyflow/repository.py",
}
MEMORY_NAMES = ("AGENTS.md", "HANDOFF.md", "docs/CURRENT_STATE.md",
                "docs/ARCHITECTURE.md", "docs/DECISIONS.md",
                "docs/PROJECT_CONTEXT.md", "docs/CHANGELOG.md")
TOPIC = re.compile(r"rename|title.edit|edit.*title|title.*edit", re.I)
PROVISIONAL = re.compile(
    r"pending|unfinished|in.progress|planned|not.implemented|todo|remain", re.I
)


def defined_functions(source: Path) -> list[dict[str, object]]:
    """Return direct function/method definitions, not inferred behavior."""
    if not source.is_file():
        return []
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    results: list[dict[str, object]] = []
    for child in tree.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results.append({"name": child.name, "line": child.lineno})
        elif isinstance(child, ast.ClassDef):
            for member in child.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    results.append({
                        "name": member.name, "line": member.lineno,
                        "class": child.name,
                    })
    return results


def source_evidence(workspace: Path) -> dict[str, object]:
    evidence: dict[str, object] = {}
    for key, relative in MODULES.items():
        source = workspace / relative
        definitions = defined_functions(source)
        name = "rename_task" if key != "repository_rename_defined" else "rename"
        evidence[key] = {
            "defined": any(f["name"] == name for f in definitions),
            "source": relative,
            "definitions": [f for f in definitions if f["name"] == name],
            "status": "syntactic_presence_only",
        }
    return evidence


def memory_excerpts(workspace: Path) -> list[dict[str, object]]:
    excerpts: list[dict[str, object]] = []
    for relative in MEMORY_NAMES:
        path = workspace / relative
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if not TOPIC.search(line):
                continue
            context = "\n".join(lines[max(0, i - 1):min(len(lines), i + 2)])
            excerpts.append({
                "file": relative,
                "line": i + 1,
                "context": context,
                "possible_unfinished_claim": bool(PROVISIONAL.search(context)),
            })
    return excerpts


def create_packet(workspace: Path) -> dict[str, object]:
    if not (workspace / "src" / "studyflow" / "service.py").is_file():
        raise ValueError("not a prepared StudyFlow workspace")
    code = source_evidence(workspace)
    mentions = memory_excerpts(workspace)
    api_present = bool(code["api_rename_defined"]["defined"])
    candidate = [
        x for x in mentions if x["possible_unfinished_claim"]
        and re.search(r"\bapi\b|adapter|handler", x["context"], re.I)
    ]
    return {
        "schema_version": 1,
        "workspace": str(workspace),
        "source_evidence": code,
        "memory_excerpts": mentions,
        "potential_stale_api_claims": candidate if api_present else [],
        "review": {
            "memory_truth_status": "not_reviewed",
            "false_completion_count": None,
            "handoff_correctness": None,
            "human_review_required": True,
        },
        "limitations": [
            "A function definition does not prove correct runtime behavior.",
            "Regex excerpts are candidates for human review, not a verdict.",
            "Absent project-memory files are not automatically a baseline failure.",
            "Test-execution claims require actual agent command logs, not AST checks.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve(strict=True)
    target = args.output.resolve()
    if workspace == target or workspace in target.parents:
        parser.error("evidence packets must stay outside the agent workspace")
    packet = create_packet(workspace)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote human-review evidence packet: {target}")
    print("Memory truth remains NOT REVIEWED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
