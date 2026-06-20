# Document Contracts

| File | Owns | Does not own | Load policy |
|---|---|---|---|
| `AGENTS.md` | Durable agent rules, document routing, validation command | Full architecture or history | Always |
| `PROJECT_CONTEXT.md` | Purpose, users, goals, scope, constraints | Task log or implementation detail | Always |
| `CURRENT_STATE.md` | Verified status, active work, blockers, next steps | Completed history | Always |
| `ARCHITECTURE.md` | Current implemented components, boundaries, data flow, contracts | Proposed designs presented as real | Architecture tasks |
| `DECISIONS.md` | Durable decisions and trade-offs | Routine edits | When rationale matters |
| `CHANGELOG.md` | Concise release/change summaries | Session transcript | Historical lookup |

## Writing Rules

- Prefer exact file paths, module names, commands, and interface names.
- Use `Implemented`, `Planned`, `Temporary`, or `Deprecated` where status could be ambiguous.
- Describe only current architecture in `ARCHITECTURE.md`; use decision records and Git for history.
- Keep `CURRENT_STATE.md` actionable and rewrite it after each meaningful task.
- Never claim a test passed unless it was run.
- Never record secrets, credentials, tokens, personal data, or local machine details.
