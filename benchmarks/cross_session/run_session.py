#!/usr/bin/env python3
"""Run ONE fresh coding-agent session and independently grade its code changes.

This is a generic external-CLI adapter, not an embedded agent runtime.
The selected command must read the session task from standard input and exit.
The command must start a *new* session every time; never use resume flags.
Raw transcripts stay outside the agent workspace for later human review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from benchmarks.cross_session.audit_memory import create_packet
from benchmarks.cross_session.prepare import CONDITIONS

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = ROOT / "benchmarks" / "cross_session" / "scenarios.json"
GRADER_DIR = ROOT / "benchmarks" / "cross_session" / "grader"
STAGES = ("session1", "session2", "session3")


def run_command(argv: list[str], *, cwd: Path, env: dict[str, str],
                input_text: str | None = None, timeout: int = 1800
                ) -> dict[str, object]:
    try:
        completed = subprocess.run(
            argv, cwd=cwd, env=env, input=input_text, text=True,
            capture_output=True, check=False, timeout=timeout,
        )
        return {
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
            "error": None,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "returncode": None,
            "stdout": str(exc.stdout or ""),
            "stderr": str(exc.stderr or ""),
            "timed_out": True,
            "error": f"timed out after {timeout} seconds",
        }
    except OSError as exc:
        return {
            "returncode": None, "stdout": "", "stderr": "",
            "timed_out": False, "error": str(exc),
        }


def git_snapshot(path: Path) -> dict[str, str | None]:
    def git(*args: str) -> str | None:
        p = subprocess.run(
            ["git", "-C", str(path), *args], text=True, capture_output=True,
            check=False,
        )
        return p.stdout if p.returncode == 0 else None

    return {
        "head_sha": (git("rev-parse", "HEAD") or "").strip() or None,
        "status": git("status", "--porcelain=v1", "--untracked-files=all"),
        "diff": git("diff", "--binary", "HEAD"),
    }


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str | None) -> None:
    path.write_text(value if value is not None else "", encoding="utf-8")


def checked_command(value: str) -> list[str]:
    command = json.loads(value)
    if not isinstance(command, list) or not command or not all(
        isinstance(item, str) and item for item in command
    ):
        raise ValueError("--agent-command-json must be a nonempty JSON array of strings")
    return command


def run_session(workspace: Path, trial_dir: Path, condition: str,
                stage: str, agent_command: list[str], *,
                timeout: int = 1800, smoke: bool = False
                ) -> dict[str, object]:
    workspace = workspace.resolve(strict=True)
    trial_dir = trial_dir.resolve()
    if condition not in CONDITIONS or stage not in STAGES:
        raise ValueError("unknown condition or stage")
    if trial_dir == workspace or workspace in trial_dir.parents:
        raise ValueError("trial record directory must be outside the agent workspace")
    if ROOT == workspace or ROOT in workspace.parents:
        raise ValueError("agent workspace must not be inside the benchmark source")
    if not (workspace / "src" / "studyflow" / "service.py").is_file():
        raise ValueError("not a prepared StudyFlow workspace")
    if (workspace / "benchmarks" / "cross_session").exists():
        raise ValueError("hidden benchmark resources leaked into workspace")

    manifest = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    user_task = next(s["task"] for s in manifest["sessions"] if s["id"] == stage)
    if stage == "session1":
        if trial_dir.exists() and any(trial_dir.iterdir()):
            raise FileExistsError("trial directory must be new or empty for session1")
        trial_dir.mkdir(parents=True, exist_ok=True)
        trial_info = {
            "schema_version": 1,
            "condition": condition,
            "workspace": str(workspace),
            "benchmark": manifest["benchmark_id"],
            "manifest_sha256": sha256(SCENARIOS.read_text(encoding="utf-8")),
            "smoke": smoke,
        }
        (trial_dir / "trial.json").write_text(
            json.dumps(trial_info, indent=2) + "\n", encoding="utf-8"
        )
    else:
        metadata = json.loads((trial_dir / "trial.json").read_text(encoding="utf-8"))
        if metadata["condition"] != condition or metadata["workspace"] != str(workspace):
            raise ValueError("condition/workspace mismatch with recorded trial")
        if metadata["manifest_sha256"] != sha256(SCENARIOS.read_text(encoding="utf-8")):
            raise ValueError("scenario manifest changed during trial")
        if metadata["smoke"] != smoke:
            raise ValueError("cannot mix smoke and live-declared sessions")
        previous = STAGES[STAGES.index(stage) - 1]
        if not (trial_dir / previous / "record.json").is_file():
            raise ValueError("previous session has not been recorded")

    run_dir = trial_dir / stage
    run_dir.mkdir(exist_ok=False)
    before = git_snapshot(workspace)
    write_text(run_dir / "git_before.txt", json.dumps(before, indent=2))
    write_text(run_dir / "task_sha256.txt", sha256(user_task) + "\n")

    # Do not pass grader configuration or PYTHONPATH into the agent process.
    agent_env = os.environ.copy()
    agent_env.pop("BENCHMARK_SESSION", None)
    agent_env.pop("PYTHONPATH", None)
    agent = run_command(agent_command, cwd=workspace, env=agent_env,
                        input_text=user_task, timeout=timeout)
    write_text(run_dir / "agent_stdout.txt", str(agent["stdout"]))
    write_text(run_dir / "agent_stderr.txt", str(agent["stderr"]))

    after = git_snapshot(workspace)
    write_text(run_dir / "git_after.txt", json.dumps(after, indent=2))

    grader_env = os.environ.copy()
    grader_env["PYTHONPATH"] = str(workspace / "src")
    grader_env["BENCHMARK_SESSION"] = stage
    grader = run_command(
        [sys.executable, "-m", "unittest", "discover",
         "-s", str(GRADER_DIR), "-p", "test_*.py", "-v"],
        cwd=ROOT, env=grader_env, timeout=120,
    )
    write_text(run_dir / "grader_stdout.txt", str(grader["stdout"]))
    write_text(run_dir / "grader_stderr.txt", str(grader["stderr"]))

    # Inspect project memory without making a claim about its factual accuracy.
    audit_packet = create_packet(workspace)
    (run_dir / "memory_evidence.json").write_text(
        json.dumps(audit_packet, indent=2) + "\n", encoding="utf-8"
    )

    # Grader success means all required behavior checks passed, not that
    # memory statements are truthful or token usage has been measured.
    record = {
        "schema_version": 1,
        "benchmark": manifest["benchmark_id"],
        "condition": condition,
        "stage": stage,
        "runner_mode": "smoke" if smoke else "declared_external_agent_cli",
        "agent_implementation_verified": False,
        "prompt_sha256": sha256(user_task),
        "workspace": str(workspace),
        "agent_command": agent_command,
        "agent_returncode": agent["returncode"],
        "agent_timed_out": agent["timed_out"],
        "agent_error": agent["error"],
        "head_before": before["head_sha"],
        "head_after": after["head_sha"],
        "grader_pass": grader["returncode"] == 0,
        "grader_returncode": grader["returncode"],
        "grader_error": grader["error"],
        "memory_review_status": "not_reviewed",
        "memory_evidence_file": "memory_evidence.json",
        "potential_stale_api_claims": len(audit_packet["potential_stale_api_claims"]),
        "actual_provider_input_tokens": None,
        "actual_provider_output_tokens": None,
        "tool_calls": None,
        "human_interventions": None,
        "public_comparison_ready": False,
    }
    (run_dir / "record.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--trial-dir", required=True, type=Path)
    parser.add_argument("--condition", choices=CONDITIONS, required=True)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--agent-command-json", required=True,
                        help="JSON argv e.g. '[\"codex\", \"exec\", \"-\"]'; reads task from stdin")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--smoke", action="store_true",
                        help="Non-agent dry-run; never publish as a measured trial")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be >= 1 second")
    record = run_session(
        args.workspace, args.trial_dir, args.condition, args.stage,
        checked_command(args.agent_command_json), timeout=args.timeout,
        smoke=args.smoke,
    )
    print(json.dumps({
        "stage": record["stage"], "condition": record["condition"],
        "runner_mode": record["runner_mode"],
        "agent_returncode": record["agent_returncode"],
        "grader_pass": record["grader_pass"],
        "review": record["memory_review_status"],
        "provider_tokens": "unmeasured",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
