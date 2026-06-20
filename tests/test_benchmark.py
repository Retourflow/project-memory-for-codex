import json
import tempfile
import unittest
from pathlib import Path

from benchmarks.benchmark import (
    build_context,
    measure_context,
    read_agent_results,
    render_markdown_report,
    run_benchmark,
    write_reports,
)

ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> dict:
        (root / "docs").mkdir()
        (root / "AGENTS.md").write_text("Always preserve API compatibility.", encoding="utf-8")
        (root / "docs" / "PROJECT_CONTEXT.md").write_text(
            "The service manages study tasks.", encoding="utf-8"
        )
        (root / "docs" / "CURRENT_STATE.md").write_text(
            "Email notifications are planned.", encoding="utf-8"
        )
        (root / "docs" / "ARCHITECTURE.md").write_text(
            "TaskService calls TaskRepository.", encoding="utf-8"
        )
        return {
            "memory_files": [
                "AGENTS.md",
                "docs/PROJECT_CONTEXT.md",
                "docs/CURRENT_STATE.md",
                "docs/ARCHITECTURE.md",
            ],
            "tasks": [
                {
                    "id": "explain-architecture",
                    "title": "Explain architecture",
                    "type": "architecture",
                    "selective_files": [
                        "AGENTS.md",
                        "docs/PROJECT_CONTEXT.md",
                        "docs/CURRENT_STATE.md",
                        "docs/ARCHITECTURE.md",
                    ],
                    "required_facts": [
                        "TaskService calls TaskRepository",
                        "preserve API compatibility",
                    ],
                },
                {
                    "id": "resume-work",
                    "title": "Resume work",
                    "type": "resume",
                    "selective_files": [
                        "AGENTS.md",
                        "docs/PROJECT_CONTEXT.md",
                        "docs/CURRENT_STATE.md",
                    ],
                    "required_facts": ["Email notifications are planned"],
                },
            ],
        }

    def test_build_context_selects_files_by_strategy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.make_fixture(root)
            task = manifest["tasks"][1]
            no_memory = build_context(root, manifest, task, "no-memory")
            monolithic = build_context(root, manifest, task, "large-agents")
            selective = build_context(root, manifest, task, "project-memory")
            self.assertEqual(no_memory.files, [])
            self.assertEqual(len(monolithic.files), 4)
            self.assertEqual(len(selective.files), 3)
            self.assertNotIn("TaskService calls TaskRepository", selective.text)

    def test_measure_context_reports_size_and_fact_coverage(self) -> None:
        measurement = measure_context(
            text="TaskService calls TaskRepository. Preserve API compatibility.",
            files=["docs/ARCHITECTURE.md", "AGENTS.md"],
            required_facts=[
                "TaskService calls TaskRepository",
                "preserve API compatibility",
                "email notifications",
            ],
        )
        self.assertEqual(measurement["loaded_file_count"], 2)
        self.assertEqual(measurement["matched_fact_count"], 2)
        self.assertEqual(measurement["required_fact_count"], 3)
        self.assertAlmostEqual(measurement["fact_coverage_percent"], 66.67)
        self.assertGreater(measurement["estimated_tokens"], 0)

    def test_run_benchmark_keeps_agent_metrics_unmeasured(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.make_fixture(root)
            report = run_benchmark(root, manifest)
            first = report["results"][0]
            self.assertIsNone(first["agent_metrics"]["task_success"])
            self.assertIsNone(first["agent_metrics"]["measured_input_tokens"])
            self.assertEqual(report["methodology"]["token_metric"], "estimated")

    def test_run_benchmark_summarizes_strategy_totals_and_reduction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.make_fixture(root)
            report = run_benchmark(root, manifest)
            summary = report["summary"]
            self.assertEqual(summary["no-memory"]["task_count"], 2)
            self.assertEqual(summary["large-agents"]["average_fact_coverage_percent"], 100.0)
            self.assertLess(
                summary["project-memory"]["estimated_tokens_total"],
                summary["large-agents"]["estimated_tokens_total"],
            )
            self.assertGreater(
                report["comparisons"]["project_memory_estimated_token_reduction_vs_large_percent"], 0
            )

    def test_agent_results_are_imported_by_task_and_strategy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "agent-results.json"
            path.write_text(json.dumps({"runs": [{"task_id": "resume-work", "strategy": "project-memory", "task_success": True, "measured_input_tokens": 321, "constraint_violations": 0}]}), encoding="utf-8")
            results = read_agent_results(path)
            self.assertTrue(results[("resume-work", "project-memory")]["task_success"])
            self.assertEqual(results[("resume-work", "project-memory")]["measured_input_tokens"], 321)

    def test_markdown_report_labels_unmeasured_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.make_fixture(root)
            markdown = render_markdown_report(run_benchmark(root, manifest))
            self.assertIn("Not measured", markdown)
            self.assertIn("Estimated tokens", markdown)
            self.assertIn("Required-fact coverage", markdown)

    def test_write_reports_creates_deterministic_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.make_fixture(root)
            report = run_benchmark(root, manifest)
            output = root / "results"
            write_reports(report, output)
            json_path = output / "latest.json"
            markdown_path = output / "REPORT.md"
            self.assertTrue(json_path.is_file())
            self.assertTrue(markdown_path.is_file())
            self.assertEqual(json.loads(json_path.read_text()), report)
            self.assertEqual(markdown_path.read_text(encoding="utf-8"), render_markdown_report(report))

    def test_repository_fixture_has_full_selective_coverage_with_less_context(self) -> None:
        root = ROOT / "benchmarks" / "fixture-project"
        manifest = json.loads((ROOT / "benchmarks" / "tasks.json").read_text())
        report = run_benchmark(root, manifest)
        by_task = {}
        for result in report["results"]:
            by_task.setdefault(result["task_id"], {})[result["strategy"]] = result
        self.assertEqual(len(by_task), 6)
        for strategies in by_task.values():
            selective = strategies["project-memory"]["static_metrics"]
            monolithic = strategies["large-agents"]["static_metrics"]
            self.assertEqual(selective["fact_coverage_percent"], 100.0)
            self.assertLessEqual(selective["words"], monolithic["words"])


if __name__ == "__main__":
    unittest.main()
