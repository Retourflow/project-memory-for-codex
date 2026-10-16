# Design: Reliable Cross-Session Handoff (v0.3)

Status: **Proposed / experiment-first**  
Updated: 2026-10-17  
Scope: Project Memory for Codex, not a general agent-memory platform.

## Product problem

After an agent changes code, a later session needs the **smallest accurate state**
needed to continue. The painful failure is not forgetting chat history; it is
continuing from a misleading account of what is implemented, tested, decided,
or still blocked.

**Core promise:** transfer verified, actionable project state across coding
sessions with little maintenance and unnecessary context loading.

## Invariants

1. **Code and tests are evidence; Markdown is an index, not authority.**
   Requirements and current user intent may supersede previously accepted designs.
2. **No false completion:** separate implemented, tested, proposed, and blocked.
   Never infer "tested" merely from the existence of a test.
3. **Minimal write:** update only memory whose meaning changed; never append a
   complete session transcript.
4. **Selective read:** start with compact orientation/current state. Inspect code
   and load architecture, decisions, or history only when the task needs them.
5. **Explicit uncertainty:** when evidence is incomplete or contradictory,
   surface it rather than manufacturing a definitive status.
6. **Lightweight by default:** keep Git-reviewed text and Python standard-library
   validation; no daemon, hosted memory service, vector store, or API key.
7. **Safety boundary:** no secrets, credentials, private data, or unauthorized
   cross-project context in memory.

## Narrow core loop

1. **Start:** establish task and load the minimum project state.
2. **Inspect:** check relevant code, tests, current requirements, and Git changes.
3. **Work:** implement and test within the actual task scope.
4. **Reconcile:** identify durable changes, unresolved work, and stale assertions.
5. **Handoff:** update the few affected memory documents; distinguish verified
   facts from unknowns and record a concrete next action.
6. **Check:** validate structure and (where evidence supports it) factual links.
7. **Resume:** a fresh agent reconstructs the next safe action without being
   misled by prior-session narration.

In v0.2, steps 2 and 4–6 are mainly **instructions to the agent**, not
mechanically guaranteed. We will not market them as fully automated.

## What v0.3 will *not* become

- A complete conversation archive, RAG stack, or semantic memory database.
- A multi-agent scheduler or automatic merge/conflict resolution framework.
- An automatic proof that arbitrary architecture or business decisions are right.
- A feature-rich UI or telemetry service.

## Evaluation before features

Before changing the Skill, compare it with realistic, smaller alternatives:

- **No persistent handoff:** code/Git remain available; no extra project summary.
- **Concise AGENTS.md:** practical project state/instructions maintained simply.
- **Plain wrap-up summary:** ordinary end-of-session summary prompt and Markdown.
- **Project Memory Skill:** current selective, budgeted, verified-by-instruction
  workflow.

Run equivalent coding tasks as **independent fresh sessions**, preserve allowed
artifacts from previous sessions, and test actual repository behavior. Do not
preselect files for the Skill in the scoring harness: whether it finds relevant
context is part of the outcome.

Metrics, prioritized: (1) verified task success and invariant preservation;
(2) accurate unfinished-work recovery and false-completion frequency;
(3) drift/stale-memory handling; (4) measured total model tokens when available;
(5) overhead and human intervention. Report unknown measurements as unknown.
Estimated document-size tokens are **not** measured agent usage.

See [benchmark protocol](benchmarks/cross_session/README.md) and
[initial scenario](benchmarks/cross_session/scenarios.json).

## Candidate changes, gated by observed failures

| Hypothesized failure | Smallest candidate fix | Verification |
|---|---|---|
| Agent claims a change was tested without running tests | Explicit evidence and status fields on critical handoff claims | Hidden tests and transcript audit |
| Handoff loses unresolved work or a design constraint | Short, structured next-action/blocker record | Fresh-session recovery |
| Memory refers to deleted files after a refactor | Optional path/symbol-reference checks | Stale-reference fixture |
| Skill loads too much detail for routine tasks | Route by task type and measure actual reads | Observed file access and measured tokens |
| Documents accumulate old status | Rewrite current state, diff-based relevance check | Multi-session memory-drift audit |

A feature is accepted only when it fixes a repeatable failure without
materially degrading correctness, simplicity, or maintenance cost.

## First milestone (v0.3 planning slice)

- [x] Audit v0.2 against the narrow promise.
- [x] Define a cross-session benchmark protocol and pilot scenario.
- [x] Implement condition-isolated fixture preparation and a generic external
  CLI runner with separate fresh processes per session (harness smoke-tested).
- [x] Implement independent code-behavior grading, transcript capture, and
  an evidence packet for human memory-truth audit (not an automated verdict).
- [ ] Run real agents across all baselines, repeat trials, audit memory truth,
  and publish sanitized raw evidence with verified usage metrics.
- [ ] Decide whether the Skill needs changes based on those findings.

**Stop condition:** do not claim v0.3 superiority, real token savings, or
improved correctness until real comparable runs support those claims.
