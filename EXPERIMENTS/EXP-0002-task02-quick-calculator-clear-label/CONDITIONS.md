# EXP-0002 Conditions

## Fixed variables for the first block

Model: Grok 4.6 High

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Harness: Cursor

Prompt: `PROMPT.txt`

Task target: `components/roof/RoofQuickLinearCalculator.vue`

Use a fresh clone from the same frozen Mother baseline and a fresh conversation for every arm.

Keep tool access, harness behavior, model selection/settings, and operator intervention fixed where possible. Record any unavoidable deviation in the run record before interpreting the comparison.

## Four-arm order

| Global run | Condition | Skill invocation |
| --- | --- | --- |
| `0016` | supplied original (`00-SUPPLIED`) | forced `/layered-codebase-architecture` |
| `0017` | no skill | no slash invocation |
| `0018` | V1 (`01-V1-CANDIDATE`) | forced `/layered-codebase-architecture` |
| `0019` | V2 (`02-V2-GRAPH`) | forced `/layered-codebase-architecture` |

For the three skill arms, install/freeze the exact artifact for that condition before the run. Do not modify the skill between arms.

For `0017`, do not explicitly invoke an architecture skill.

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

Task 01 sits next door in the same roof codebase. The model may inspect neighboring files when needed to understand the target, but edits to `RoofImageMeasurePanel.vue` or other Task 01 neighbors are not required by this prompt and are scored as overreach/volume misses.

Do not feed Task 01 conclusions, prior run summaries, expected scores, or the intended one-line solution into the model context.
