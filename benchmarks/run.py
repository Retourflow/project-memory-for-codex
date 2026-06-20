#!/usr/bin/env python3
"""Run the reproducible Project Memory for Codex context benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmarks.benchmark import read_agent_results, run_benchmark, write_reports


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare no-memory, monolithic, and selective context strategies."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "benchmarks" / "results",
        help="Directory for latest.json and REPORT.md.",
    )
    parser.add_argument(
        "--agent-results",
        type=Path,
        help="Optional JSON file containing measured real agent-run results.",
    )
    args = parser.parse_args()

    benchmark_dir = ROOT / "benchmarks"
    fixture_root = benchmark_dir / "fixture-project"
    manifest = json.loads((benchmark_dir / "tasks.json").read_text(encoding="utf-8"))
    imported = read_agent_results(args.agent_results)
    report = run_benchmark(fixture_root, manifest, imported)
    write_reports(report, args.output)
    print(f"Wrote benchmark reports to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
