# Cross-session handoff benchmark (pilot)

**Status: protocol and pilot fixture, not a completed agent evaluation.**

The goal is to test whether a fresh coding-agent session can reconstruct the
*true, actionable project state* without misleading memory, unnecessary file
reads, or excessive human intervention.

This is a **developer workflow benchmark**, not a prompt-recall quiz. The
existing v0.2 static benchmark remains separate.

## Research question

Does a small, selective project-memory workflow improve **real task completion
and reliable handoff** over (a) no persisted handoff, (b) a concise AGENTS.md,
and (c) a plain end-of-session summary?

A useful result may be that a simpler baseline works equally well. Do not
assume the Skill will win.

## Pilot: StudyFlow title editing

`scenarios.json` declares three ordered fresh-session tasks:

1. Implement a service/repository title-edit operation, **deliberately** leave
   the API adapter unfinished, and hand off the remaining work accurately.
2. A new agent finishes the API adapter while preserving v1 response shape and
   the existing notification boundary.
3. A new agent checks edge cases, memory truth, and code/test consistency.

The **same evolving repository** is carried between sessions **within a
trial**. No conversation history, model context, or hidden grader information
is carried. Each condition starts from a **separate pristine copy** of
`benchmarks/fixture-project`.

The initial setup has an existing `AGENTS.md` and `docs/` memory. For fair
comparison, the trial preparer must construct **condition-specific initial
workspaces**, as below; never leave Project Memory documents accidentally
visible in the baseline conditions.

| Condition | Added handoff mechanism (on top of identical source/tests) |
|---|---|
| `no-memory` | No memory documents or project handoff; source and Git history remain |
| `concise-agents` | One concise agent instruction/status file; no other memory documents |
| `plain-summary` | One project handoff Markdown file maintained with a generic wrap-up prompt |
| `project-memory` | v0.2 Skill and its AGENTS/docs project-memory workflow |

Give all agents equivalent general coding/testing/safety instructions, the
same user task for each session, and the same available tool permissions.
The memory mechanism, not special hints about task outcomes, is the independent
variable. Record exactly which files and setup messages each condition receives.

## Session protocol (external CLI runner available; trials not yet run)

1. Pin repository commit, runtime, chosen agent/model version, prompt,
   allowed tools, and any limits **before** beginning.
2. Create an isolated workspace for each condition/trial from the same base
   fixture using `prepare.py`, which strips specialized memory from the
   controls and installs the Skill into the experimental workspace:

   ```bash
   python benchmarks/cross_session/prepare.py \\
     --condition project-memory --workspace /tmp/studyflow-pm-trial1
   python benchmarks/cross_session/prepare.py \\
     --condition concise-agents --workspace /tmp/studyflow-agents-trial1
   ```

   The command refuses to overwrite an existing workspace and initializes a
   new Git repository by default. Use new paths for each independent trial.
   The tool only prepares files; it does not start a model or grade results.
   When running Codex, confirm that the installed Skill is actually activated
   in the project-memory condition; its presence alone does not prove use.
3. Launch a **fresh agent process/session** for session 1 with only the
   corresponding session user task from `scenarios.json`. Use the Python runner
   below; it reads the task from the manifest, sends it via stdin to the agent
   process, records stdout/stderr, and evaluates code outside the workspace.
   Do not provide `grader/`, future-session prompts, or grading rubrics to the
   agent. The process command must be configured for **new sessions**, not
   resuming prior conversation state.
4. Preserve committed and uncommitted project files and Git history for the
   *next session in that trial*; carry **no conversational context**.
5. Outside the agent's workspace, run public fixture tests and the stage
   grader with `BENCHMARK_SESSION=session1` (and likewise for sessions 2/3).
   Copy the grader to a private evaluator location or run it with a separate
   process working directory; do not expose it during the agent session.
6. Record code diffs, changed memory files, actual test exit codes, agent
   messages/tool transcripts, model/provider token usage if available, agent
   overhead, and any human help. Keep explicit `null` for unavailable values.
7. Repeat the identical protocol for all conditions. Randomize condition
   execution order and use fresh trials to reduce carryover and stochastic bias.
8. Repeat multiple independent trials after the pilot proves viable. A single
   run demonstrates the harness, not broad superiority.

Example offline evaluator invocation **after an agent run** from the repository
containing the grader, where WORKDIR is the isolated target checkout:

```bash
PYTHONPATH="$WORKDIR/src" BENCHMARK_SESSION=session1 \
  python -m unittest discover -s benchmarks/cross_session/grader -p 'test_*.py' -v
```

### CLI runner and review packet

The benchmark uses a **generic command adapter**. The specified executable
must read the task from stdin, exit after one agent session, and run in the
provided workspace. Confirm your local tool's sandbox/permission settings and
new-session semantics before real trials. There is **no bundled Codex runtime**
and no default live-agent evaluation.

Example: first prepare four workspaces in temporary directories. Then run
each of the three stages using **the same command, model, permissions and
timeout** for each condition. For a Codex CLI installation that supports
stdin via the trailing \`-\` argument, a command can be expressed as:

\`\`\`bash
python -m benchmarks.cross_session.run_session \
  --workspace /tmp/studyflow-pm-trial1 \
  --trial-dir /tmp/studyflow-pm-results1 \
  --condition project-memory \
  --stage session1 \
  --agent-command-json '["codex","exec","-"]'
\`\`\`

Execute \`session2\` and \`session3\` with the exact same workspace and
trial directory, changing only \`--stage\`, **each from a fresh process**.
Do not enable conversation resume, bypass sandbox boundaries, or grant broader
tool permissions to one experimental condition. If your CLI does not support
standard input, use a small wrapper with the same contract.

Before evaluating model behavior, test harness wiring without any real agent:

\`\`\`bash
python -m benchmarks.cross_session.run_session \
  --workspace /tmp/studyflow-no-memory-smoke \
  --trial-dir /tmp/studyflow-smoke-records \
  --condition no-memory --stage session1 --smoke \
  --agent-command-json '["python","-c","import sys;sys.stdin.read()"]'
\`\`\`

Prepare that smoke workspace with \`prepare.py\` first. Smoke mode is always
labeled **unmeasured** and intentionally fails the feature grader against
an unchanged fixture. Do not use it as evidence of model performance.

Outputs are written **outside** the agent workspace under
\`<trial-dir>/sessionN/\`: \`record.json\`, \`agent_stdout.txt\`,
\`agent_stderr.txt\`, \`grader_stdout.txt\`, \`grader_stderr.txt\`,
\`git_before.txt\`, \`git_after.txt\`, and \`memory_evidence.json\`.
The agent receives no grader code or grader results. After each session,
\`memory_evidence.json\` lists source-level observations and candidate stale
claims; it is **not** an automated verdict. Human reviewers must compare
these against actual source, test runs, transcripts and handoff documents.

Even in the declared live mode, \`record.json\` keeps \`public_comparison_ready\`
false and real token metrics null. A successful grader is only a code-behavior
result. Verify CLI/model versions and provenance of any provider token usage
before publishing aggregated measurements. Keep raw transcripts and workspace
paths private or carefully sanitize before publishing.

`BENCHMARK_SESSION` accepts `session1`, `session2`, or `session3`.
This evaluator tests **code behavior**. It is not an agent runner and does not
grade whether memory descriptions accurately reflect the implementation.

## Scoring and disqualifiers

**Primary:** passed hidden behavior checks and preservation of existing
contracts. Do not substitute a self-reported "done" message for passing tests.

**Memory-specific review**, grounded in workspace files and execution logs:
- Was unfinished API work described as unfinished after session 1?
- At session 2, did a fresh agent avoid claiming the API had already shipped?
- After session 2, was implemented status updated without erasing risks?
- At session 3, did the agent identify and repair demonstrably stale claims?
- Are claimed passing tests traceable to actual executed commands?

**Efficiency:** measured total input/output tokens, tool calls, elapsed time,
and human interventions where providers expose them. Record the size of
project-memory documents separately; do not confuse an estimate of loaded
Markdown size with actual model usage.

**Failures:** missing regressions/contract checks, false completion, unverifiable
"tested" claims, data loss, permission/sandbox bypass, or using hidden answers.

Keep a raw run record per session including condition, trial, prompt hash,
model and tool configuration, starting/ending Git SHAs/diff, grader output,
status review, and provenance of any measured tokens. A future harness may
automate this; none of those observations have been collected here.

## What this pilot cannot prove

- This scenario is small and purposely structured: it is not a statistically
  representative sample of real software development.
- Test pass rates do not automatically establish good memory or few tokens.
- A three-session pilot is not evidence about months-long projects, branch
  conflicts, or untrusted requirements.
- v0.2's 45.42% figure describes estimated preselected context size, not
  measured total coding-session token savings.

## Acceptance / stop conditions

- First run validates the grader itself and confirms it **fails correctly**
  on a pristine fixture (red test).
- Pilot all conditions on equal starting workspaces; publish raw outcomes,
  including failures, only **after the trials actually happen**.
- Propose at most one minimal Skill change per observed recurring failure.
- Retain zero-dependency, reviewable Markdown and backward compatibility.

Do not add a RAG backend, multi-agent controller, or automatic memory
"proof engine" because of this pilot.
