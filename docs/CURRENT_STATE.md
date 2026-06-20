# Current State

Last verified: 2026-06-20

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
- GitHub Actions workflow for tests, validation, and report reproducibility.
- Independent-project disclaimer for OpenAI and Codex brand clarity.
- Security and privacy policy covering local-only operation, sensitive data,
  safe initialization, and vulnerability reporting.
- Safety rules propagated into the reusable Skill and repository template.
- README first screen explains the project's selective loading, verification,
  context-budget, Git review, current-truth, and zero-infrastructure advantages.

## In Progress

- None.

## Planned Next

1. Publish the verified v0.2 release.
2. Run a real Codex benchmark and import measured results.
3. Package the initializer and add guided compaction in v0.3.

## Known Issues

- Real agent benchmark results remain unmeasured.
- PowerShell initialization has not been executed in this Linux environment.

## Active Entry Points

- `skill/codex-project-memory/SKILL.md`: reusable workflow.
- `templates/AGENTS.md`: repository instruction template.
- `scripts/validate.py`: project-memory validator.
- `benchmarks/run.py`: reproducible benchmark entry point.
- `benchmarks/results/REPORT.md`: current static evidence.
- `SECURITY.md`: security, privacy, and reporting guidance.
