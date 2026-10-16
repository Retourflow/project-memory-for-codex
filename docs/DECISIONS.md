# Architecture Decisions

## ADR-003: Validate Cross-session Handoffs Before Expanding Features

- Date: 2026-10-17
- Status: Accepted for v0.3 experimental branch

### Context

Selective context and budget validation exist in v0.2, but the six-task
benchmark does not establish reliable multi-session code handoff. A simpler
AGENTS.md or wrap-up summary might perform just as well.

### Decision

Focus the next experimental milestone on accurate unfinished-work handoff,
independent correctness checks, and realistic simple baselines. Keep the core
zero-dependency and postpone new retrieval, storage, multi-agent orchestration,
and elaborate memory validation until a repeated failure demands them.

### Rationale

This protects the project's small, auditable character and tests the actual
developer friction rather than the complexity of the proposed solution.

### Alternatives

- Expand directly into a general memory framework.
- Add automatic Git-diff validation before proving the handoff problem.
- Optimize estimated document tokens without testing end-to-end code outcomes.

### Consequences

- v0.3 first ships an **unrun** pilot protocol and offline checks.
- No superiority claim is permitted without comparable agent trials.
- A limited or negative result will be reported and may mean no new core
  feature is needed.

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
