# Architecture Decisions

## ADR-002: Separate Static Evidence From Agent Outcomes

- Date: 2026-06-20
- Status: Accepted

### Context

v0.2 needs reproducible evidence, but the project must not require an API key or
claim unmeasured model performance.

### Decision

Measure context size and required-fact coverage offline. Import real agent-run
success and token usage only when a user supplies measured results.

### Rationale

This keeps the benchmark reproducible and honest while leaving room for stronger
future experiments.

### Alternatives

- Require a model API and run paid benchmarks automatically.
- Publish estimated success rates from static context coverage.

### Consequences

- Static reports are available to everyone.
- Agent success remains `Not measured` until a real run is imported.

## ADR-001: Use Selective Version-Controlled Memory

- Date: 2026-06-20
- Status: Accepted

### Context

Long sessions lose important context, while large instruction files can increase
cost and introduce stale requirements.

### Decision

Keep small always-loaded documents and load detailed architecture, decisions,
and history only when relevant.

### Rationale

The approach is transparent, auditable, portable, and has no service dependency.

### Alternatives

- Store everything in one large `AGENTS.md`.
- Use a vector database or hosted memory service.

### Consequences

- Project memory requires deliberate maintenance.
- Git remains the source for exhaustive history.
