# Current State

Current skill under evaluation: `layered-codebase-architecture`

Current frozen experimental candidate: `02-V2-GRAPH`

Promotion status: experimental, not promoted as a general improvement.

Current completed global run: `0021`

Next global run: `0022`

Current experiment: `EXP-0003-task03-required-rake-pitch`

Baseline repository commit: `cd393ddd60548823dabd6875060247693a22c1be`

## Evidence Status

Primary skill-effect evidence preserved through V1 for EXP-0001: Grok 4.6 High, Kimi K2.7 Code, GPT-5.1.

Diagnostic evidence preserved for EXP-0001: Gemini 2.5 because execution was inconsistent enough to make it a poor skill-effect instrument.

V2 fourth-condition experimental runs preserved as primary EXP-0001 evidence: Grok 4.6 High (`0013`), Kimi K2.7 Code (`0014`), GPT-5.1 (`0015`).

EXP-0002 Task 02 holdout evidence preserved:

- Grok 4.6 High supplied original forced run (`0016`).
- Grok 4.6 High no-skill control run (`0017`).
- Grok 4.6 High V1 forced run (`0018`).
- Grok 4.6 High V2 forced run (`0019`).

EXP-0002 is retained as the restraint floor. All four Grok 4.6 High arms made the same one-line label-only change; no skill revision is justified by EXP-0002 alone.

EXP-0003 Task 03 first-model evidence preserved:

- Grok 4.6 High supplied original forced run (`0020`).
- Grok 4.6 High no-skill control run (`0021`).

Process claims require preserved transcript/trace evidence. Verification claims require preserved command output or equivalent state proof at the level claimed. A transcript-only verification statement is a process claim, not independently preserved verification success.

## Current Unscored Observations

These are not promoted findings until scored against the rubric.

- EXP-0002 `0016`, `0017`, `0018`, and `0019` each made a one-line label-only change in `components/roof/RoofQuickLinearCalculator.vue`.
- The exported Cursor prompt for `0016` omitted the leading word `In` from `PROMPT.txt`; the preserved evidence records the exported prompt exactly.
- The `0016`, `0017`, `0018`, and `0019` archives are local-only in `ARCHIVES/local/` and are not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0003 `0020` changed two tracked files, created `.cursor/noun-map.md`, and added `shared/roofLineMeasurements.test.ts`; this is preserved but not scored.
- The `0020` archive is local-only in `ARCHIVES/local/` and is not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0003 `0021` changed two tracked files and had no untracked subject-repository files; this is preserved but not scored.
- No independent test, typecheck, build, or browser/runtime verification was preserved for `0021`.
- The `0021` archive is local-only in `ARCHIVES/local/` and is not fresh-clone retrievable until published to durable release/artifact storage.

## EXP-0002 Holdout Block

Do not edit the skill or rerun these specimens when using them as the restraint floor.

Run Grok 4.6 High through the four frozen arms in this order:

1. `0016` supplied original (`00-SUPPLIED`) - preserved
2. `0017` no-skill control - preserved
3. `0018` V1 (`01-V1-CANDIDATE`) - preserved
4. `0019` V2 (`02-V2-GRAPH`) - preserved

Each run starts from a fresh clone of Mother at baseline `cd393ddd60548823dabd6875060247693a22c1be` and a fresh Cursor conversation.

Failed or incomplete runs remain evidence and consume their run ID. If a process comparison requires a rerun, use a new global run ID rather than replacing the preserved run.

## EXP-0003 First-Model Block

Do not edit the skill during this block.

Run Grok 4.6 High through the four frozen arms in this order:

1. `0020` supplied original (`00-SUPPLIED`) - preserved
2. `0021` no-skill control - preserved
3. `0022` V1 (`01-V1-CANDIDATE`) - next
4. `0023` V2 (`02-V2-GRAPH`) - planned

Each run starts from a fresh clone of Mother at baseline `cd393ddd60548823dabd6875060247693a22c1be` and a fresh Cursor conversation.

Use the Shingle workplace lifecycle: clone Mother to Active, open Cursor in Active, control the skill through Cursor global `skills-cursor`, preserve transcript and evidence outside Active, archive Active as the numbered run, then clear Active before the next arm.

## Evidence Contract For The Holdout

- Preserve a transcript/trace for process claims.
- If the process trace is missing, preserve the result as state-only evidence.
- Preserve command output for verification claims at the level claimed.
- Do not promote transcript-only typecheck/build statements to independently verified command evidence.
- Keep prompt, baseline, model, harness, tool access, and skill artifacts fixed across the four arms where possible.
- For no-skill control runs, remove `layered-codebase-architecture` from Cursor global `skills-cursor` directory before the run.
- For skill-arm runs, install the condition artifact into Cursor global `skills-cursor` directory; do not inject skill files into the subject repository.

## Next Action

Prepare run `0022` from a fresh Active clone, install `01-V1-CANDIDATE` into Cursor global `skills-cursor`, use a forced `/layered-codebase-architecture` invocation, and run the EXP-0003 prompt with Grok 4.6 High.
