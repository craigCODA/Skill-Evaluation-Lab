# Current State

Current skill under evaluation: `layered-codebase-architecture`

Current frozen experimental candidate: `02-V2-GRAPH`

Promotion status: experimental, not promoted as a general improvement.

Current completed global run: `0023`

Next global run: `0024`

Current experiment: `EXP-0004-task04-open-valley-metal-charge`

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

Historical closed-PR #2 EXP-0002 scoring from source commit `4bdf610` is preserved in `REPORTS/layered-codebase-architecture/closed-pr2-4bdf610-exp0002-0016-0027-score.md`. That report scores closed-PR evidence only; it does not import PR #2 run IDs into current-branch canonical evidence.

EXP-0003 Task 03 first-model evidence preserved:

- Grok 4.6 High supplied original forced run (`0020`).
- Grok 4.6 High no-skill control run (`0021`).
- Grok 4.6 High V1 forced run (`0022`).
- Grok 4.6 High V2 forced run (`0023`).

EXP-0003 Task 03 first-model scoring is preserved in `REPORTS/layered-codebase-architecture/0020-0023-exp0003-required-rake-pitch.md`. Corrected scores are: supplied original (`0020`) 26/30, no-skill control (`0021`) 25/30, V1 (`0022`) 29/30, and V2 (`0023`) 29/30. V2 has the cleanest patch, V1 has the stronger durable test artifact, and both substantially outperform original/no-skill on responsibility-boundary judgment.

The earlier EXP-0003 second-model block was a proposed next action only and was not cut. No `0024` through `0027` EXP-0003 rows exist in `RUN-INDEX.md`, `DATA/runs.json`, `EVIDENCE/`, `DEVELOPMENT-HISTORY/`, archive ZIPs, or prep files. EXP-0003 evidence remains preserved exactly through `0023`.

EXP-0004 Task 04 setup is preserved in `EXPERIMENTS/EXP-0004-task04-open-valley-metal-charge/`. Its frozen first model is GPT-5.1, with planned four-arm runs `0024` through `0027`.

Process claims require preserved transcript/trace evidence. Verification claims require preserved command output or equivalent state proof at the level claimed. A transcript-only verification statement is a process claim, not independently preserved verification success.

## Current Run Observations

These are raw run observations. EXP-0003 scoring for `0020` through `0023` is promoted in `REPORTS/layered-codebase-architecture/0020-0023-exp0003-required-rake-pitch.md`.

- EXP-0002 `0016`, `0017`, `0018`, and `0019` each made a one-line label-only change in `components/roof/RoofQuickLinearCalculator.vue`.
- The exported Cursor prompt for `0016` omitted the leading word `In` from `PROMPT.txt`; the preserved evidence records the exported prompt exactly.
- The `0016`, `0017`, `0018`, and `0019` archives are local-only in `ARCHIVES/local/` and are not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0003 `0020` changed two tracked files, created `.cursor/noun-map.md`, and added `shared/roofLineMeasurements.test.ts`; it scored 26/30.
- The `0020` archive is local-only in `ARCHIVES/local/` and is not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0003 `0021` changed two tracked files and had no untracked subject-repository files; it scored 25/30.
- No independent test, typecheck, build, or browser/runtime verification was preserved for `0021`.
- The `0021` archive is local-only in `ARCHIVES/local/` and is not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0003 `0022` changed two tracked files and added `shared/roofLineMeasurements.test.ts`; it scored 29/30.
- The exported Cursor prompt for `0022` omitted the leading word `In` after the forced slash invocation; the preserved evidence records the exported prompt exactly.
- Preserved terminal evidence for `0022` records `npx tsx --test shared/roofLineMeasurements.test.ts` passing four tests twice.
- No successful Nuxt typecheck or browser/runtime verification was independently preserved for `0022`; terminal evidence records `node_modules` and `nuxt` absent.
- The `0022` archive is local-only in `ARCHIVES/local/` and is not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0003 `0023` changed two tracked files and had no untracked subject-repository files; it scored 29/30.
- Preserved terminal evidence for `0023` records an inline `npx tsx` domain check exiting 0 and confirming the intended rake/hip totals behavior.
- No successful Nuxt typecheck or browser/runtime verification was independently preserved for `0023`; terminal evidence records `node_modules` and `nuxt` absent.
- The `0023` archive is local-only in `ARCHIVES/local/` and is not fresh-clone retrievable until published to durable release/artifact storage.
- EXP-0004 baseline premise was verified directly against ShingleFile baseline `cd393ddd60548823dabd6875060247693a22c1be`.
- No EXP-0004 model run has been cut or preserved yet.

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
3. `0022` V1 (`01-V1-CANDIDATE`) - preserved
4. `0023` V2 (`02-V2-GRAPH`) - preserved

Each run starts from a fresh clone of Mother at baseline `cd393ddd60548823dabd6875060247693a22c1be` and a fresh Cursor conversation.

Use the Shingle workplace lifecycle: clone Mother to Active, open Cursor in Active, control the skill through Cursor global `skills-cursor`, preserve transcript and evidence outside Active, archive Active as the numbered run, then clear Active before the next arm.

## EXP-0004 First-Model Block

Do not edit the skill during this block.

Run GPT-5.1 through the four frozen arms in this order:

1. `0024` supplied original (`00-SUPPLIED`)
2. `0025` no-skill control
3. `0026` V1 (`01-V1-CANDIDATE`)
4. `0027` V2 (`02-V2-GRAPH`)

Each run starts from a fresh clone of Mother at baseline `cd393ddd60548823dabd6875060247693a22c1be` and a fresh Cursor conversation.

Use the same Shingle workplace lifecycle as the first EXP-0003 model block.

The subject prompt is exactly:

```text
When I choose an open valley and enter the footage, the estimate shows a valley metal amount but the customer total and roofing proposal ignore it. Open valley metal is a customer charge.
```

Do not expose `BASELINE.md`, `SCORECARD.md`, expected authority, positive-control findings, closed-valley expectations, prior experiment conclusions, implementation hints, or likely solution shape to the subject model.

## Evidence Contract For The Holdout

- Preserve a transcript/trace for process claims.
- If the process trace is missing, preserve the result as state-only evidence.
- Preserve command output for verification claims at the level claimed.
- Do not promote transcript-only typecheck/build statements to independently verified command evidence.
- Keep prompt, baseline, model, harness, tool access, and skill artifacts fixed across the four arms where possible.
- For no-skill control runs, remove `layered-codebase-architecture` from Cursor global `skills-cursor` directory before the run.
- For skill-arm runs, install the condition artifact into Cursor global `skills-cursor` directory; do not inject skill files into the subject repository.

## Next Action

Cut EXP-0004 run `0024` first: GPT-5.1 with supplied original `00-SUPPLIED`, forced `/layered-codebase-architecture`, fresh Mother-to-Active clone, fresh Cursor conversation, and no subject-repository skill files.
