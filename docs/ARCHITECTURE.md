# Architecture

Last verified: 2026-06-20

## System Overview

The project is a zero-dependency toolkit composed of a Codex Skill, repository
templates, initialization scripts, validation logic, examples, tests, and a
reproducible benchmark package.

## Components

| Component | Responsibility | Primary Files | Status |
|---|---|---|---|
| Skill | Route and maintain project memory | `skill/codex-project-memory/` | Implemented |
| Templates | Seed repository-local memory | `templates/` | Implemented |
| Initializers | Copy templates without overwriting by default | `scripts/init.sh`, `scripts/init.ps1` | Implemented |
| Validator | Enforce files, headings, placeholders, and budgets | `scripts/validate.py` | Implemented |
| Skill Validator | Check Skill metadata without third-party packages | `scripts/validate_skill.py` | Implemented |
| Benchmark | Compare context strategies and evidence | `benchmarks/` | Implemented |
| CI | Reproduce tests and reports | `.github/workflows/ci.yml` | Implemented |
| Security guidance | Define privacy boundaries, safe use, and reporting | `SECURITY.md` | Implemented |

## Data Flow

1. A developer initializes project-memory files in a repository.
2. Codex loads `AGENTS.md`, project context, and current state.
3. Codex loads architecture, decisions, or history only when relevant.
4. Codex verifies documentation against code and tests.
5. After changes, Codex updates only affected memory and runs validation.

Benchmark flow:

1. `benchmarks/run.py` loads `benchmarks/tasks.json`.
2. `benchmarks/benchmark.py` selects context for each strategy and task.
3. Static metrics measure size and required-fact presence.
4. Optional imported results add measured agent outcomes.
5. Reports are written deterministically to `benchmarks/results/`.

## Interfaces And Contracts

- `bash scripts/init.sh <project> [--force]`
- `scripts/init.ps1 -ProjectPath <project> [-Force]`
- `python scripts/validate.py <project>`
- `python scripts/validate_skill.py <skill-directory>`
- `python -m unittest discover -s tests -v`
- `python benchmarks/run.py [--agent-results <file>]`

## Data And Storage

All durable state is plain UTF-8 Markdown or JSON committed to Git. No runtime
database or external storage is required.

## External Dependencies

Core functionality uses only Bash, PowerShell, Git, and Python's standard
library. Codex and Figma are optional consumers, not runtime dependencies.

## Cross-Cutting Constraints

- Never report estimated tokens as provider-measured usage.
- Preserve existing project files unless replacement is explicitly requested.
- Keep active context smaller than exhaustive history.
- Do not record secrets, credentials, personal data, or private machine details.
- Do not bypass Codex sandboxing, approvals, or repository permissions.
- Do not imply that the project is affiliated with or endorsed by OpenAI.
