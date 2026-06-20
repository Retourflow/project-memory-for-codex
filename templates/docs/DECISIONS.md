# Architecture Decisions

Add new records at the top. Keep old records and mark replaced decisions as
`Superseded`.

## ADR-000: Use Explicit Project Memory

- Date: YYYY-MM-DD
- Status: Accepted

### Context

Long-running agent sessions can lose project goals, constraints, and rationale.

### Decision

Keep concise, verified project memory in version-controlled Markdown files and
load detailed documents only when relevant to the task.

### Rationale

This keeps context transparent, reviewable, portable, and inexpensive.

### Alternatives

- Store all context in one large agent instruction file.
- Use an external database or vector memory service.

### Consequences

- Project memory must be updated with meaningful changes.
- Git remains the source for exhaustive historical detail.
