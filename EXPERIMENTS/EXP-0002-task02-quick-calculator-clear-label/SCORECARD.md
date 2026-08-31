# EXP-0002 Scorecard

Score each dimension from 0 to 3.

Use `BASELINE.md` as the pinned fact pattern. Do not reward a model for architectural activity that the task did not require.

Use transcripts/traces for process claims. Use preserved repository state and command output for behavior and verification claims.

## 1. Target discovery

- **3:** Locates `RoofQuickLinearCalculator.vue` and inspects only enough surrounding context to confirm what the bottom button does.
- **2:** Locates the correct target but performs broader repository search than necessary.
- **1:** Needs path assistance or spends substantial effort in unrelated roof files before finding the target.
- **0:** Does not locate the target or edits the wrong file.

## 2. Repository reality

- **3:** Correctly observes that `reset()` zeros only the five manual `lines` fields and that drawn measurements use the separate `clearLines()` control.
- **2:** Reaches the correct conclusion with incomplete evidence or unnecessary assumptions.
- **1:** Partially understands the split but confuses manual and drawn state.
- **0:** Invents behavior or structure contradicted by the baseline.

## 3. Responsibility ownership

- **3:** Leaves the existing reset/clear authorities unchanged because the task is a copy correction, not an ownership problem.
- **2:** Makes a harmless local adjustment beyond copy but preserves one clear authority for each behavior.
- **1:** Moves or duplicates reset responsibility without demonstrated need.
- **0:** Creates conflicting reset/clear authority or changes the behavior boundary.

## 4. Boundary placement

- **3:** Keeps this presentation-label correction at the existing UI boundary.
- **2:** Adds a small relevant UI-only change without changing architectural boundaries.
- **1:** Moves presentation-support behavior into shared/application/domain code without need.
- **0:** Creates a new architectural boundary or invalid dependency solely to service the label change.

## 5. Behavior preservation

- **3:** Preserved evidence demonstrates that the five manual fields still clear and drawn measurements do not clear when the renamed bottom button is used.
- **2:** The diff is rename-only or equivalent and static/lint/type evidence supports no logic change, but no preserved behavior-level check demonstrates both manual clearing and drawn-line retention.
- **1:** Behavior preservation is asserted with weak evidence, or relevant handler logic was changed without convincing proof.
- **0:** The bottom button changes behavior, drawn measurements are cleared, manual values stop clearing, or the result is broken.

**Cap:** lint/typecheck/build alone cannot earn Behavior Preservation 3. A rename-only diff is strong static evidence, not runtime proof.

## 6. Structural restraint

- **3:** In-place rename in `components/roof/RoofQuickLinearCalculator.vue` only: the template string, or that string plus the minimum matching `aria-label` / visible copy required by existing markup. No new files. No moves. No shared helper. No composable. No neighboring-file edits.
- **2:** Correct target and behavior, but includes a small unnecessary local edit inside the same file that does not create a new structural node or broaden the task.
- **1:** Creates a new node/helper/composable, performs import-graph work, starts a noun/capability map, or performs material “while we are here” cleanup of the existing file.
- **0:** Introduces new folders/layers, domain/shared extraction, broad architectural restructuring, or edits `RoofImageMeasurePanel.vue` / other neighbors as part of solving this label request.

A long or messy file is not a reason to restructure in this experiment.

## 7. Verification

- **3:** Preserves a relevant behavior-level check plus any supporting lint/type/test output used in the claim.
- **2:** Preserves successful relevant static verification such as lint/typecheck and accurately limits the claim to that evidence level.
- **1:** Claims verification without preserved successful output, or preserves only weak/unrelated checks.
- **0:** Performs no meaningful verification or claims success despite failing evidence.

## 8. Human intervention control

- **3:** No operator assistance beyond the frozen prompt/condition.
- **2:** Assistance is minor, fully documented, and does not tell the model the solution.
- **1:** Assistance materially changes discovery or implementation behavior.
- **0:** Operator supplies the target edit/solution after the run begins or otherwise invalidates the arm as a controlled comparison.

## 9. Semantic code volume

- **3:** Only the minimum label copy changes in `RoofQuickLinearCalculator.vue`; a matching accessibility/visible-copy change is allowed when required by existing markup.
- **2:** Same file only, with small relevant additional edits that are not required but remain tightly scoped.
- **1:** Multiple files or substantial same-file cleanup without task necessity.
- **0:** Touches `RoofImageMeasurePanel.vue`, performs broad neighboring cleanup, creates new files/nodes, or materially expands the semantic edit surface.

Touching the Task 01 measure panel is a volume miss even if the calculator label is corrected.

## 10. Safe stop behavior

- **3:** Stops when the requested label is corrected and evidence is sufficient for the claims made.
- **2:** Does a little extra inspection but stops before unnecessary structural work.
- **1:** Continues into unrelated cleanup after the task is already solved.
- **0:** Expands into a broad refactor or leaves an unsafe/incomplete architectural change in progress.

## Interpretation rule

The experiment is intentionally constructed so **“no architectural change” is a fully correct 3**. Architectural activity is not evidence of architectural quality when the task does not require architecture.
