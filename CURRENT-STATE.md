# Current State

Current skill under evaluation: `layered-codebase-architecture`

Current frozen experimental candidate: `02-V2-GRAPH`

Promotion status: experimental, not promoted as a general improvement.

Current completed global run: `0015`

Next global run: `0016`

Current experiment: `EXP-0001-task01-roof-image-measure`

Baseline repository commit: `cd393ddd60548823dabd6875060247693a22c1be`

## Evidence status

Primary skill-effect evidence preserved through V1: Grok 4.6 High, Kimi K2.7 Code, GPT-5.1.

Diagnostic evidence preserved: Gemini 2.5 because execution was inconsistent enough to make it a poor skill-effect instrument.

V2 fourth-condition experimental runs currently preserved as primary evidence: Grok 4.6 High (`0013`), Kimi K2.7 Code (`0014`), GPT-5.1 (`0015`).

Process-evidence correction:

- `0013` preserves a Cursor transcript export. The model identity is operator-supplied rather than independently encoded in that export.
- `0014` preserves `cursor-agent-transcript.raw.jsonl`, a Markdown transcript, and terminal evidence. Treat the cell as state-strong and process-usable. The independently preserved terminal evidence includes the initial failed `npx nuxt typecheck`; later typecheck/build success exists as transcript claims, not as separately preserved successful command logs.
- `0015` preserves `cursor-agent-transcript.raw.jsonl`, a Markdown transcript, and terminal evidence. Treat the cell as state-strong and process-usable. The transcript contains lint/process evidence, but no independently preserved successful typecheck/build output was found.

Process claims require preserved transcript/trace evidence. Verification claims require preserved command output or equivalent state proof at the level claimed. A transcript-only verification statement is a process claim, not independently preserved verification success.

No V2 fourth-condition run for Gemini 2.5 is preserved as of `0015`.

## Current unscored observations

These are not promoted findings until scored against the rubric.

- V2 Task 01 observations exist for runs `0013`, `0014`, and `0015`.
- Grok V2 produced a restrained seam-based restructuring result.
- Kimi V2 still produced five structural UI nodes and moved presentation-support helpers into shared scale code despite V2 already containing a new-seam proof gate.
- GPT-5.1 V2 chose a small in-place authority cleanup rather than creating a new structural node.
- V2 has not yet been evaluated on a second task prompt.
- Task 01 has not yet been fully scored across the primary comparison cells using the current rubric.

## Method decision before run 0016

Do not edit the skill yet.

Do not mint `V1.1` or `V2.1` at this stage.

Freeze the comparison set:

- no-skill control
- `00-SUPPLIED`
- `01-V1-CANDIDATE`
- `02-V2-GRAPH`

The next evidence should test generalization and isolate behavior before another instruction change is introduced.

### Step 1 - Score Task 01

Score the existing primary Task 01 cells with `SCORECARD.md` before starting another skill revision.

Use preserved result state and command output for behavior/verification scoring. Use transcripts for process scoring. A second independent rating is preferred when practical.

### Step 2 - EXP-0002 holdout

The next experiment is a second-task holdout with all four skill conditions frozen.

Choose a task meaningfully different from Task 01. A fully correct result must be allowed to make no architectural change at all and still receive the highest structural-restraint score. Do not reuse another prompt whose main instruction is to clean up or restructure a large component.

Run Grok 4.6 High through all four arms first because the existing controlled evidence shows the clearest skill-driven behavioral movement on that model.

Planned arm order beginning at global run `0016`:

1. no skill
2. supplied original
3. V1
4. V2

Failed or incomplete runs remain evidence and consume their run ID. If a process comparison requires a rerun, use a new global run ID rather than replacing the preserved run.

### Evidence contract for the holdout

- Preserve a transcript/trace for process claims.
- If the process trace is missing, preserve the result as state-only evidence.
- Preserve command output for verification claims at the level claimed.
- Do not promote transcript-only typecheck/build statements to independently verified command evidence.
- Keep prompt, baseline, model, harness, tool access, and skill artifacts fixed across the four arms where possible.

### Skill-edit gate

Edit a skill only if the scored holdout repeats a named failure and the evidence points to one instruction group that plausibly causes or fails to prevent it.

The next skill revision should change the smallest instruction group justified by that repeated failure.

Trigger-selection studies and supplied-original ablation studies come later as separate experiments. They must not be mixed into the `0016` holdout block.

## Next Action

Score Task 01 primary cells; then run the EXP-0002 holdout on frozen no-skill / original / V1 / V2. No skill edit until a scored holdout names one instruction group.
