# Agent Instructions

## Project Memory

The files under `docs/` are durable project memory. Keep them concise, verified,
and synchronized with the implementation.

Before any non-trivial task:

1. Read `docs/PROJECT_CONTEXT.md`.
2. Read `docs/CURRENT_STATE.md`.
3. Inspect relevant code before trusting documentation.

Load additional documents only when needed:

- Read `docs/ARCHITECTURE.md` for structure, interfaces, data flow, dependencies,
  or cross-module changes.
- Read relevant entries in `docs/DECISIONS.md` when prior rationale matters.
- Search `docs/CHANGELOG.md` or Git only for historical investigation.

After verified changes, update only affected memory documents. Do not describe
planned work as implemented. Mark future work as `Planned` and shortcuts as
`Temporary`.

Never record secrets, credentials, tokens, personal data, private machine
details, or proprietary source excerpts that should not be committed. Do not
bypass sandboxing, approval requirements, repository permissions, or other
user-controlled security boundaries.

## Context Budgets

- `AGENTS.md`: at most 150 lines
- `docs/PROJECT_CONTEXT.md`: at most 800 words
- `docs/CURRENT_STATE.md`: at most 500 words
- `docs/ARCHITECTURE.md`: at most 2,000 words
- `docs/DECISIONS.md`: at most 4,000 words
- `docs/CHANGELOG.md`: at most 4,000 words

Run `python scripts/validate.py .` after updating project memory.
