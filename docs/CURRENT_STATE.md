# Current State

Last reviewed: 2026-10-17 (v0.3 experiment branch; live-agent evaluation not run)

## Implemented

- English Codex Skill with document-routing and compaction guidance.
- Project-memory templates for goals, state, architecture, decisions, and history.
- Bash and PowerShell initialization scripts.
- Standard-library context-budget validator with three unit tests.
- Standard-library Codex Skill metadata validator.
- Editable FigJam workflow diagram.
- v0.2 static benchmark with three strategies and six tasks.
- Optional import format for real agent-run metrics.
- Deterministic JSON and Markdown benchmark reports.
- Sanitized evidence from 18 blinded Agent runs across all task/strategy pairs.
- Real Agent outcomes imported alongside the deterministic static measurements.
- GitHub Actions workflow for tests, validation, and report reproducibility.
- Independent-project disclaimer for OpenAI and Codex brand clarity.
- Security and privacy policy covering local-only operation, sensitive data,
  safe initialization, and vulnerability reporting.
- Safety rules propagated into the reusable Skill and repository template.
- README first screen explains the project's selective loading, verification,
  context-budget, Git review, current-truth, and zero-infrastructure advantages.

## In Progress

- Experimental v0.3 branch defines a narrowly scoped reliable-handoff design
  (`design.md`), a cross-session evaluation protocol and pilot scenario
  (`benchmarks/cross_session/`), offline stage-aware behavior grader, and
  manifest structure tests. Agent outcome measurements are **not yet run**.

## Planned Next

1. Validate benchmark resources with local unit tests and confirm the hidden
   grader fails as expected on an unmodified fixture.
2. Build reproducible per-condition isolated workspaces and a fresh-session
   orchestration harness; do not leak evaluator tests to agents.
3. Run repeated live-agent cross-session trials for all four conditions;
   preserve raw evidence, measured usage if exposed, and failures.
4. Choose the smallest Skill improvement justified by repeated failures.
5. Release v0.3 only after verifying the new workflow; handle packaging and
   guided compaction later if needed.

## Known Issues

- Provider-measured token usage and resolved Agent model versions were not
  exposed by the benchmark runner.
- The real Agent benchmark currently has one run per task/strategy pair.
- v0.3's pilot benchmark is a protocol and offline behavior grader only;
  no live-agent results, token savings, or comparison outcomes exist yet.

## Active Entry Points

- `design.md`: experimental v0.3 design and scope guardrails.
- `benchmarks/cross_session/README.md`: evaluation protocol and limitations.
- `benchmarks/cross_session/scenarios.json`: three-session pilot manifest.
- `benchmarks/cross_session/grader/test_title_edit.py`: independent behavior checks.

- `skill/codex-project-memory/SKILL.md`: reusable workflow.
- `templates/AGENTS.md`: repository instruction template.
- `scripts/validate.py`: project-memory validator.
- `benchmarks/run.py`: reproducible benchmark entry point.
- `benchmarks/results/REPORT.md`: current static evidence.
- `benchmarks/results/AGENT_BENCHMARK.md`: real Agent benchmark summary.
- `benchmarks/results/agent-evidence.json`: sanitized evidence index and audit.
- `SECURITY.md`: security, privacy, and reporting guidance.
