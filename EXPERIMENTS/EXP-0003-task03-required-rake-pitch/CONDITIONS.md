# EXP-0003 Conditions

## Fixed variables for the first block

Model: Grok 4.6 High

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Harness: Cursor

Prompt: `PROMPT.txt`

Use a fresh clone from the same frozen Mother baseline and a fresh conversation for every arm.

Keep tool access, harness behavior, model selection/settings, and operator intervention fixed where possible. Record any unavoidable deviation in the run record before interpreting the comparison.

## Four-arm order

| Global run | Condition | Skill invocation |
| --- | --- | --- |
| `0020` | supplied original (`00-SUPPLIED`) | forced `/layered-codebase-architecture` |
| `0021` | no skill | no slash invocation |
| `0022` | V1 (`01-V1-CANDIDATE`) | forced `/layered-codebase-architecture` |
| `0023` | V2 (`02-V2-GRAPH`) | forced `/layered-codebase-architecture` |

For the three skill arms, install/freeze the exact artifact for that condition before the run. Do not modify the skill between arms.

For `0021`, remove `layered-codebase-architecture` from Cursor global `skills-cursor` before opening Cursor. Do not explicitly invoke an architecture skill.

## Workplace lifecycle

Use the Shingle workplace architecture execution pattern:

- fresh clone `ACTIVE/ShingleFile-main` from `MOTHER/ShingleFile-main.git` before each run;
- open Cursor in `ACTIVE/ShingleFile-main`;
- control the skill only through `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture`;
- do not inject `.cursor` files or skill files into the subject repository;
- preserve transcript/evidence outside `ACTIVE/ShingleFile-main`;
- archive the complete Active checkout as the numbered run before clearing Active;
- then clear Active and fresh-clone the next arm.

## Run validity contract

Every arm must preserve:

- the final repository state before cleanup;
- `git status` / changed-file evidence;
- a transcript or agent trace sufficient for process claims;
- terminal/command logs used to support verification claims;
- the exact prompt as delivered to the model;
- the exact skill artifact identity for skill arms;
- operator interventions, path assistance, retries, or environment deviations.

A missing transcript does not erase the run. Preserve it as state-only evidence and consume the global run ID.

A transcript statement that typecheck/build/test passed is process evidence unless the successful command output is independently preserved.

If a matched process comparison requires a rerun, assign a new global run ID. Never replace the preserved specimen.

## Contamination control

Do not feed EXP-0002 results, prior run summaries, expected solution notes, file targets, baseline analysis, or scorecard criteria into the model context.

The model may inspect shared roof-line measurement logic and report/proposal consumers when needed. Editing the proposal/report path is not required by the prompt and is scored as an affected-consumer miss unless the preserved evidence proves behavior is unchanged.
