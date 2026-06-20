"""Benchmark context strategies without requiring a model or external service."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STRATEGIES = ("no-memory", "large-agents", "project-memory")


@dataclass(frozen=True)
class ContextBundle:
    files: list[str]
    text: str


def _join_files(root: Path, files: list[str]) -> str:
    sections = []
    for relative_path in files:
        content = (root / relative_path).read_text(encoding="utf-8")
        sections.append(f"# Source: {relative_path}\n\n{content.strip()}")
    return "\n\n---\n\n".join(sections)


def build_context(
    root: Path, manifest: dict[str, Any], task: dict[str, Any], strategy: str
) -> ContextBundle:
    if strategy not in STRATEGIES:
        raise ValueError(f"unknown strategy: {strategy}")

    if strategy == "no-memory":
        files: list[str] = []
    elif strategy == "large-agents":
        files = [manifest["large_context_file"]] if manifest.get(
            "large_context_file"
        ) else list(manifest["memory_files"])
    else:
        files = list(task["selective_files"])

    return ContextBundle(files=files, text=_join_files(root, files))


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def _normalize_fact_text(text: str) -> str:
    return " ".join(text.replace("`", "").casefold().split())


def measure_context(
    text: str, files: list[str], required_facts: list[str]
) -> dict[str, Any]:
    normalized = _normalize_fact_text(text)
    matched = [
        fact for fact in required_facts if _normalize_fact_text(fact) in normalized
    ]
    required_count = len(required_facts)
    coverage = 100.0 if required_count == 0 else len(matched) / required_count * 100

    return {
        "loaded_files": files,
        "loaded_file_count": len(files),
        "characters": len(text),
        "words": _word_count(text),
        "estimated_tokens": math.ceil(len(text) / 4) if text else 0,
        "matched_facts": matched,
        "matched_fact_count": len(matched),
        "required_fact_count": required_count,
        "fact_coverage_percent": round(coverage, 2),
    }


def read_agent_results(path: Path | None) -> dict[tuple[str, str], dict[str, Any]]:
    if path is None:
        return {}

    payload = json.loads(path.read_text(encoding="utf-8"))
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for run in payload.get("runs", []):
        key = (run["task_id"], run["strategy"])
        indexed[key] = {
            "task_success": run.get("task_success"),
            "measured_input_tokens": run.get("measured_input_tokens"),
            "constraint_violations": run.get("constraint_violations"),
            "notes": run.get("notes"),
        }
    return indexed


def run_benchmark(
    root: Path,
    manifest: dict[str, Any],
    agent_results: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    imported = agent_results or {}
    results = []

    for task in manifest["tasks"]:
        for strategy in STRATEGIES:
            bundle = build_context(root, manifest, task, strategy)
            static_metrics = measure_context(
                bundle.text, bundle.files, task.get("required_facts", [])
            )
            measured = imported.get((task["id"], strategy), {})
            results.append(
                {
                    "task_id": task["id"],
                    "task_title": task["title"],
                    "task_type": task["type"],
                    "strategy": strategy,
                    "static_metrics": static_metrics,
                    "agent_metrics": {
                        "task_success": measured.get("task_success"),
                        "measured_input_tokens": measured.get("measured_input_tokens"),
                        "constraint_violations": measured.get("constraint_violations"),
                        "notes": measured.get("notes"),
                    },
                }
            )

    summary: dict[str, dict[str, Any]] = {}
    for strategy in STRATEGIES:
        rows = [row for row in results if row["strategy"] == strategy]
        measured_runs = [
            row for row in rows if row["agent_metrics"]["task_success"] is not None
        ]
        successes = sum(
            1 for row in measured_runs if row["agent_metrics"]["task_success"]
        )
        summary[strategy] = {
            "task_count": len(rows),
            "loaded_files_total": sum(
                row["static_metrics"]["loaded_file_count"] for row in rows
            ),
            "words_total": sum(row["static_metrics"]["words"] for row in rows),
            "estimated_tokens_total": sum(
                row["static_metrics"]["estimated_tokens"] for row in rows
            ),
            "average_fact_coverage_percent": round(
                sum(row["static_metrics"]["fact_coverage_percent"] for row in rows)
                / len(rows),
                2,
            ),
            "agent_runs_measured": len(measured_runs),
            "task_success_rate_percent": (
                round(successes / len(measured_runs) * 100, 2)
                if measured_runs
                else None
            ),
        }

    large_tokens = summary["large-agents"]["estimated_tokens_total"]
    selective_tokens = summary["project-memory"]["estimated_tokens_total"]
    reduction = (
        round((large_tokens - selective_tokens) / large_tokens * 100, 2)
        if large_tokens
        else 0.0
    )

    return {
        "schema_version": 1,
        "benchmark_name": manifest.get(
            "benchmark_name", "Project Memory for Codex Context Benchmark"
        ),
        "methodology": {
            "token_metric": "estimated",
            "token_estimation": "ceil(UTF-8 text characters / 4)",
            "agent_outcomes": "Imported measured values only; null means Not measured.",
        },
        "strategies": list(STRATEGIES),
        "summary": summary,
        "comparisons": {
            "project_memory_estimated_token_reduction_vs_large_percent": reduction
        },
        "results": results,
    }


def _display(value: Any) -> str:
    if value is None:
        return "Not measured"
    if isinstance(value, bool):
        return "Pass" if value else "Fail"
    return str(value)


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['benchmark_name']}",
        "",
        "This report separates deterministic static context measurements from real",
        "agent outcomes. Null agent values are shown as `Not measured`.",
        "",
        "## Methodology",
        "",
        "- Estimated tokens: `ceil(characters / 4)`; this is not provider usage.",
        "- Required-fact coverage: literal case-insensitive fact presence in loaded context.",
        "- Task success: imported from real agent runs only.",
        "",
        "## Strategy Summary",
        "",
        "| Strategy | Tasks | Total words | Estimated tokens | Average fact coverage | Agent runs measured | Task success rate |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for strategy in report["strategies"]:
        summary = report["summary"][strategy]
        lines.append(
            "| `{strategy}` | {tasks} | {words} | {tokens} | {coverage:.2f}% | {runs} | {success} |".format(
                strategy=strategy,
                tasks=summary["task_count"],
                words=summary["words_total"],
                tokens=summary["estimated_tokens_total"],
                coverage=summary["average_fact_coverage_percent"],
                runs=summary["agent_runs_measured"],
                success=_display(summary["task_success_rate_percent"]),
            )
        )

    reduction = report["comparisons"][
        "project_memory_estimated_token_reduction_vs_large_percent"
    ]
    lines.extend(
        [
            "",
            f"Selective project memory used **{reduction:.2f}% fewer estimated tokens**",
            "than the monolithic context across this static fixture.",
            "",
            "## Results",
            "",
            "| Task | Strategy | Files | Words | Estimated tokens | Required-fact coverage | Task success | Measured input tokens |",
            "|---|---|---:|---:|---:|---:|---|---|",
        ]
    )

    for result in report["results"]:
        static = result["static_metrics"]
        agent = result["agent_metrics"]
        lines.append(
            "| {task} | `{strategy}` | {files} | {words} | {tokens} | {coverage:.2f}% | {success} | {measured} |".format(
                task=result["task_title"],
                strategy=result["strategy"],
                files=static["loaded_file_count"],
                words=static["words"],
                tokens=static["estimated_tokens"],
                coverage=static["fact_coverage_percent"],
                success=_display(agent["task_success"]),
                measured=_display(agent["measured_input_tokens"]),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Static coverage shows whether declared facts are present in the selected",
            "context. It does not prove that an agent understood them or completed a task.",
            "Use imported real runs before making task-success claims.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(report: dict[str, Any], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "latest.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "REPORT.md").write_text(
        render_markdown_report(report), encoding="utf-8"
    )
