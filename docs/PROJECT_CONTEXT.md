# Project Context

## Purpose

Project Memory for Codex is an open-source, token-aware project context system
for Codex. It preserves the smallest verified project state needed across
sessions without requiring a database, hosted service, or API key.

## Primary Users

- Individual developers maintaining long-running projects with coding agents.
- Open-source maintainers who want explicit, reviewable agent context.

## Goals

- `Implemented`: Provide selective project-memory templates and initialization.
- `Implemented`: Enforce context budgets with a standard-library validator.
- `Implemented`: Provide reproducible evidence comparing context strategies.

## Non-Goals

- Capture every conversation or tool call automatically.
- Replace Git history, source inspection, or tests.
- Provide semantic search, embeddings, or a hosted memory service.

## Constraints

- Core workflows must remain zero-dependency.
- Reports must distinguish measured, estimated, and unmeasured values.
- Documentation must reflect verified implementation rather than aspiration.
- The project must not imply affiliation with or endorsement by OpenAI.
- Project memory must not contain secrets, credentials, personal data, or
  private machine-specific information.

## Success Criteria

- A new Codex session can recover goals, current state, and architecture quickly.
- Selective context can be compared reproducibly with no-memory and monolithic
  baselines.
- Installation, validation, tests, and benchmarks run on standard Python.
