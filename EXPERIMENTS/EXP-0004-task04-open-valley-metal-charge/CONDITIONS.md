# EXP-0004 Conditions

## Fixed Variables For The First Block

Model: GPT-5.1

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Harness: Cursor

Prompt: `PROMPT.txt`

Use a fresh clone from the same frozen Mother baseline and a fresh conversation for every arm.

Keep tool access, harness behavior, model selection/settings, and operator intervention fixed where possible. Record any unavoidable deviation in the run record before interpreting the comparison.

## Four-Arm Order

| Global run | Condition | Skill invocation |
| --- | --- | --- |
| `0024` | supplied original (`00-SUPPLIED`) | forced `/layered-codebase-architecture` |
| `0025` | no skill | no slash invocation |
| `0026` | V1 (`01-V1-CANDIDATE`) | forced `/layered-codebase-architecture` |
| `0027` | V2 (`02-V2-GRAPH`) | forced `/layered-codebase-architecture` |

## Second-Model Block

Model: Opus

| Global run | Condition | Skill invocation |
| --- | --- | --- |
| `0028` | supplied original (`00-SUPPLIED`) | forced `/layered-codebase-architecture` |
| `0029` | no skill | no slash invocation |
| `0030` | V1 (`01-V1-CANDIDATE`) | forced `/layered-codebase-architecture` |
| `0031` | V2 (`02-V2-GRAPH`) | forced `/layered-codebase-architecture` |

For the three skill arms, install/freeze the exact artifact for that condition before the run. Do not modify the skill between arms.

For `0025`, remove `layered-codebase-architecture` from Cursor global `skills-cursor` before opening Cursor. Do not explicitly invoke an architecture skill.

## Workplace Lifecycle

Use the Shingle workplace architecture execution pattern:

- fresh clone `ACTIVE/ShingleFile-main` from `MOTHER/ShingleFile-main.git` before each run;
- open Cursor in `ACTIVE/ShingleFile-main`;
- control the skill only through `%USERPROFILE%/.cursor/skills-cursor/layered-codebase-architecture`;
- do not inject `.cursor` files, harness files, or skill files into the subject repository;
- preserve transcript/evidence outside `ACTIVE/ShingleFile-main`;
- archive the complete Active checkout as the numbered run before clearing Active;
- then clear Active and fresh-clone the next arm.

## Run Validity Contract

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

## Contamination Control

Do not feed `BASELINE.md`, `SCORECARD.md`, EXP-0003 conclusions, expected solution notes, file targets, positive-control findings, or scorecard criteria into the model context.

The subject prompt is exactly `PROMPT.txt`. Do not append architecture instructions, implementation hints, preservation instructions, closed-valley instructions, or expected solution details.
