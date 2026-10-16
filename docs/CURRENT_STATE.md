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

- The v0.3 experimental branch now contains a scoped `design.md`, four
  isolated condition-specific workspace setups, a three-session StudyFlow
  coding scenario, a generic fresh-process external agent CLI runner,
  stage-aware independent behavioral grading, and a source-evidence packet
  for human memory review. Tests cover manifest structure, isolated workspace
  setup, smoke runner behavior, source inspection, and the expected-red grader.
- The runner never reports a model success rate from its own smoke tests;
  records mark provider token usage unknown and memory truth not reviewed.

## Planned Next

1. Pin agent CLI/model version and sandbox permissions and run a small pilot
   with all four conditions in genuinely fresh coding-agent sessions.
2. Independently review memory claims against code, behavior tests, and
   transcripts; verify which provider usage metrics are exposed.
3. Repeat trials, preserve and sanitize raw evidence, and publish uncertainty.
4. Fix the smallest repeatable handoff failure, if the evidence warrants it.
5. Release v0.3 only after demonstrated improvements or clear negative results.

## Known Issues

- Provider-measured token usage and resolved Agent model versions were not
  exposed by the benchmark runner.
- The real Agent benchmark currently has one run per task/strategy pair.
- v0.3 has an unrun live-agent scenario with a CLI harness, smoke tests,
  and an evidence packet; no comparable live-agent trial results, token
  savings, or memory-accuracy scores exist yet.

## Active Entry Points

- `design.md`: experimental v0.3 design and scope guardrails.
- `benchmarks/cross_session/README.md`: evaluation protocol and limitations.
- `benchmarks/cross_session/scenarios.json`: three-session pilot manifest.
- `benchmarks/cross_session/grader/test_title_edit.py`: independent behavior checks.
- `benchmarks/cross_session/prepare.py`: fair per-condition workspaces.
- `benchmarks/cross_session/run_session.py`: fresh-session CLI and offline tests.
- `benchmarks/cross_session/audit_memory.py`: human-review evidence packets.

- `skill/codex-project-memory/SKILL.md`: reusable workflow.
- `templates/AGENTS.md`: repository instruction template.
- `scripts/validate.py`: project-memory validator.
- `benchmarks/run.py`: reproducible benchmark entry point.
- `benchmarks/results/REPORT.md`: current static evidence.
- `benchmarks/results/AGENT_BENCHMARK.md`: real Agent benchmark summary.
- `benchmarks/results/agent-evidence.json`: sanitized evidence index and audit.
- `SECURITY.md`: security, privacy, and reporting guidance.
