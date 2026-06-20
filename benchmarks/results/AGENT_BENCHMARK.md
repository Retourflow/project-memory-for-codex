# Real Agent Benchmark Evidence

Test date: 2026-06-20  
Repository commit: `d6a47d71e84d211cde3b7a44037fde715764b0e8`

## Result

| Strategy | Passed | Required facts recalled | Estimated context tokens |
|---|---:|---:|---:|
| `no-memory` | 4/6 (66.67%) | 11/14 (78.57%) | 0 |
| `large-agents` | 5/6 (83.33%) | 13/14 (92.86%) | 5,352 |
| `project-memory` | 5/6 (83.33%) | 13/14 (92.86%) | 2,921 |

Selective project memory matched the monolithic context's strict task success
while using 45.42% fewer estimated context tokens.

## Method

- Six repository-defined tasks were run under three strategies.
- Every run used a fresh Agent and a blinded directory name.
- Agents were restricted to their assigned directory, read-only inspection, and
  no network access through explicit prompt instructions. The runner did not
  return separate enforcement telemetry.
- A task passed only when every repository-defined required fact was explicitly
  or unambiguously stated.
- Primary runs used `multi_agent_v1.spawn_agent` with `agent_type: explorer`,
  `fork_context: false`, and no explicit model, reasoning-effort, or service-tier
  override.
- The resolved inherited Agent model identifier/version was not exposed by the
  runner, so it is recorded as `null` rather than inferred.
- Provider-measured input tokens were not exposed by the Agent runner. The token
  figures are the repository's deterministic `ceil(characters / 4)` estimates.
- This is one run per task/strategy pair, so it is evidence, not a statistical
  significance claim.

## Per-run scores

| Task | No memory | Large AGENTS | Project memory |
|---|---|---|---|
| Locate API entry point | Fail: HTTP-entry role not explicit | Pass | Pass |
| Explain architecture | Pass | Pass | Pass |
| Change title validation | Fail: 2 facts missing | Fail: product-purpose fact missing | Fail: product-purpose fact missing |
| Add notification retries | Pass | Pass | Pass |
| Resume email adapter | Pass | Pass | Pass |
| Preserve notification boundary | Pass | Pass | Pass |

## Grading audit

Three independent judges scored one strategy each. The initial large-context
judge passed the local-change response, while the project-memory judge failed a
nearly equivalent response. A fourth consistency arbiter reviewed the two
answers side by side and ruled that both:

- explicitly preserved the v1 JSON response; and
- did not explicitly state that StudyFlow helps students manage study tasks.

The final report therefore marks both runs as failed under the same strict
all-required-facts rule.

## Files

- `agent-evidence.json`: evidence index, methodology, runner configuration,
  limitations, summary, grading audit, and links to three evidence parts.
- `agent-evidence-part-*.json`: all 18 sanitized raw prompts and Agent outputs,
  required facts, per-item scores, public agent aliases, and blinded cases.
- `agent-results.json`: import-compatible input for:

  ```bash
  python benchmarks/run.py \
    --agent-results benchmarks/results/agent-results.json
  ```

The benchmark agents did not modify their assigned fixture directories. Private
local paths and opaque runner identifiers were replaced with stable public
aliases before this evidence was committed.
