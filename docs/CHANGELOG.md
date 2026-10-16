# Changelog

## Unreleased — v0.3 experiment preparation

### Added

- Root `design.md` defining minimal, reliable cross-session project handoff
  as the narrow product promise and restricting unrelated feature growth.
- Cross-session benchmark protocol, four comparison conditions, and three
  ordered StudyFlow coding-session tasks.
- Offline stage-aware behavior checks for task-title changes and API contract
  preservation, plus manifest integrity and expected-red grader unit tests.
- Deterministic condition-specific workspace preparation, including baseline
  memory isolation and v0.2 Skill installation for the experimental condition.
- ADR-003 documenting why evaluation precedes new features.

### Verification status

- Experimental planning artifacts only; live-agent comparison **not run**.
- No v0.3 success-rate or real token-reduction claims.

## v0.2

Released: 2026-06-20

### Added

- Repository-local project memory for dogfooding the Skill.
- Reproducible benchmark fixture with six tasks and three context strategies.
- Static context metrics, optional real-result imports, and generated reports.
- GitHub Actions CI for tests, validation, fixture checks, and report freshness.
- Standard-library Skill metadata validation.
- Security and privacy policy with vulnerability-reporting guidance.
- Sanitized evidence for 18 blinded Agent runs across six tasks and three
  context strategies.
- Import-compatible real Agent outcomes and a dedicated benchmark report.

### Changed

- README now documents benchmark methodology, results, workflow, and limitations.
- README now identifies the project as independent and not affiliated with,
  endorsed by, or sponsored by OpenAI.
- Skill guidance now separates static evidence from real agent outcomes.
- Skill and templates now prohibit sensitive-data storage and security-boundary
  bypasses.
- README now surfaces the project's primary differentiators near the top:
  selective loading, verified memory, explicit budgets, Git reviewability,
  current-state maintenance, and zero required infrastructure.
- README now reports real Agent task success separately from estimated
  project-context token usage and documents the benchmark limitations.

### Fixed

- None.

## v0.1

### Added

- Codex Skill, templates, initialization scripts, validator, tests, and example.
