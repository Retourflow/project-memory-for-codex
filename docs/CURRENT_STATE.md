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

- None.

## Planned Next

1. Publish the verified v0.2 release.
2. Repeat the Agent benchmark across additional runs and exposed model versions.
3. Package the initializer and add guided compaction in v0.3.

## Known Issues

- Provider-measured token usage and resolved Agent model versions were not
  exposed by the benchmark runner.
- The real Agent benchmark currently has one run per task/strategy pair.

## Active Entry Points

- `skill/codex-project-memory/SKILL.md`: reusable workflow.
- `templates/AGENTS.md`: repository instruction template.
- `scripts/validate.py`: project-memory validator.
- `benchmarks/run.py`: reproducible benchmark entry point.
- `benchmarks/results/REPORT.md`: current static evidence.
- `benchmarks/results/AGENT_BENCHMARK.md`: real Agent benchmark summary.
- `benchmarks/results/agent-evidence.json`: sanitized evidence index and audit.
- `SECURITY.md`: security, privacy, and reporting guidance.
