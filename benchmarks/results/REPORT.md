# Project Memory for Codex Context Benchmark

This report separates deterministic static context measurements from real
agent outcomes. Null agent values are shown as `Not measured`.

## Methodology

- Estimated tokens: `ceil(characters / 4)`; this is not provider usage.
- Required-fact coverage: literal case-insensitive fact presence in loaded context.
- Task success: imported from real agent runs only.

## Strategy Summary

| Strategy | Tasks | Total words | Estimated tokens | Average fact coverage | Agent runs measured | Task success rate |
|---|---:|---:|---:|---:|---:|---|
| `no-memory` | 6 | 0 | 0 | 0.00% | 0 | Not measured |
| `large-agents` | 6 | 2814 | 5352 | 100.00% | 0 | Not measured |
| `project-memory` | 6 | 1473 | 2921 | 100.00% | 0 | Not measured |

Selective project memory used **45.42% fewer estimated tokens**
than the monolithic context across this static fixture.

## Results

| Task | Strategy | Files | Words | Estimated tokens | Required-fact coverage | Task success | Measured input tokens |
|---|---|---:|---:|---:|---:|---|---|
| Locate the API entry point | `no-memory` | 0 | 0 | 0 | 0.00% | Not measured | Not measured |
| Locate the API entry point | `large-agents` | 1 | 469 | 892 | 100.00% | Not measured | Not measured |
| Locate the API entry point | `project-memory` | 4 | 266 | 527 | 100.00% | Not measured | Not measured |
| Explain the service architecture | `no-memory` | 0 | 0 | 0 | 0.00% | Not measured | Not measured |
| Explain the service architecture | `large-agents` | 1 | 469 | 892 | 100.00% | Not measured | Not measured |
| Explain the service architecture | `project-memory` | 5 | 323 | 643 | 100.00% | Not measured | Not measured |
| Change local title validation | `no-memory` | 0 | 0 | 0 | 0.00% | Not measured | Not measured |
| Change local title validation | `large-agents` | 1 | 469 | 892 | 100.00% | Not measured | Not measured |
| Change local title validation | `project-memory` | 3 | 168 | 331 | 100.00% | Not measured | Not measured |
| Add notification retry behavior | `no-memory` | 0 | 0 | 0 | 0.00% | Not measured | Not measured |
| Add notification retry behavior | `large-agents` | 1 | 469 | 892 | 100.00% | Not measured | Not measured |
| Add notification retry behavior | `project-memory` | 5 | 323 | 643 | 100.00% | Not measured | Not measured |
| Resume unfinished email adapter work | `no-memory` | 0 | 0 | 0 | 0.00% | Not measured | Not measured |
| Resume unfinished email adapter work | `large-agents` | 1 | 469 | 892 | 100.00% | Not measured | Not measured |
| Resume unfinished email adapter work | `project-memory` | 3 | 168 | 331 | 100.00% | Not measured | Not measured |
| Preserve the notification boundary | `no-memory` | 0 | 0 | 0 | 0.00% | Not measured | Not measured |
| Preserve the notification boundary | `large-agents` | 1 | 469 | 892 | 100.00% | Not measured | Not measured |
| Preserve the notification boundary | `project-memory` | 4 | 225 | 446 | 100.00% | Not measured | Not measured |

## Interpretation

Static coverage shows whether declared facts are present in the selected
context. It does not prove that an agent understood them or completed a task.
Use imported real runs before making task-success claims.
