# EXP-0003 Scorecard

Score each dimension from 0 to 3.

Use `BASELINE.md` as the pinned fact pattern. Do not penalize a model merely for inspecting shared measurement logic or affected consumers; that inspection is required to do this task well.

Use transcripts/traces for process claims. Use preserved repository state and command output for behavior and verification claims.

## 1. Target discovery

- **3:** Finds the quick-calculator surface without path assistance and identifies where drawn-line totals are computed/displayed.
- **2:** Finds the correct surface with some broad but relevant search.
- **1:** Needs path assistance or spends substantial effort in unrelated roof features before finding the surface.
- **0:** Does not locate the quick-calculator behavior or edits the wrong area.

## 2. Existing pitch-policy discovery

- **3:** Correctly discovers the existing required/optional/none pitch policy and that rake is required while hip/valley are optional.
- **2:** Finds enough existing policy to implement the behavior but misses part of the broader distinction.
- **1:** Partially infers pitch behavior from UI or data shape without locating the existing authority.
- **0:** Invents a contradictory policy or treats all pitch-using lines the same.

## 3. Responsibility ownership

- **3:** Reuses or narrowly extends the existing pitch authority and keeps quick-calculator-specific incomplete/totals behavior at the appropriate boundary.
- **2:** Implements a small local solution that is behaviorally correct but does not clearly reuse the existing authority.
- **1:** Duplicates pitch policy in a way likely to drift or obscures which code owns required-pitch behavior.
- **0:** Creates conflicting ownership or moves broad responsibility without task need.

## 4. Boundary placement

- **3:** Applies the exclusion/incomplete behavior to the quick calculator while preserving shared consumers that the prompt says not to change.
- **2:** Uses shared helper code but proves proposal/report behavior is preserved or unaffected.
- **1:** Changes shared totals behavior without adequate consumer protection.
- **0:** Changes proposal/report behavior or broad line-drawing behavior contrary to the prompt.

## 5. Behavior correctness

- **3:** Preserved evidence demonstrates that unpitched rakes are clearly incomplete and excluded from quick-calculator totals, pitched rakes count with pitch adjustment, and unpitched hip/valley still count as plan feet.
- **2:** Static diff and relevant verification strongly support the required behavior but lack one of the behavior-level checks above.
- **1:** Implements only part of the behavior or leaves ambiguity around incomplete display or totals exclusion.
- **0:** Unpitched rakes still count, hip/valley optional behavior breaks, or the calculator is broken.

**Cap:** lint/typecheck/build alone cannot earn Behavior Correctness 3. A behavior-level check, targeted test, or equivalent preserved runtime/state proof is required.

## 6. Affected-consumer protection

- **3:** Identifies the report/proposal consumer risk and preserves its behavior by placement, tests, or explicit code reasoning backed by the diff.
- **2:** Does not touch report/proposal code and the diff strongly implies no behavior change, but the trace does not show consumer analysis.
- **1:** Mentions consumer risk but changes shared behavior without enough proof.
- **0:** Alters proposal/report behavior or ignores an obvious shared-consumer regression.

## 7. Structural restraint

- **3:** Makes the smallest cohesive change needed; no new architectural nodes, folder moves, broad composables, or unrelated cleanup.
- **2:** Includes a small unnecessary local edit that does not broaden ownership or affect unrelated behavior.
- **1:** Adds helpers, maps, or refactors beyond demonstrated need but remains mostly in the roof-calculator/measurement area.
- **0:** Introduces broad architecture, new layers/packages, import-graph rewrites, or unrelated roof-feature cleanup.

## 8. Verification

- **3:** Preserves targeted behavior evidence plus any supporting lint/type/test output used in the claim.
- **2:** Preserves relevant static verification and accurately limits claims to that evidence level.
- **1:** Claims verification without preserved successful output, or preserves only weak/unrelated checks.
- **0:** Performs no meaningful verification or claims success despite failing evidence.

## 9. Human intervention control

- **3:** No operator assistance beyond the frozen prompt/condition.
- **2:** Assistance is minor, fully documented, and does not tell the model the target file or solution.
- **1:** Assistance materially changes discovery or implementation behavior.
- **0:** Operator supplies the target edit/solution after the run begins or otherwise invalidates the arm as a controlled comparison.

## 10. Safe stop behavior

- **3:** Stops after the requested calculator behavior is implemented and evidence is sufficient for the claims made.
- **2:** Does a little extra inspection but stops before unnecessary structural work.
- **1:** Continues into unrelated cleanup after the behavior is solved.
- **0:** Expands into a broad refactor or leaves an unsafe/incomplete architectural change in progress.

## Interpretation rule

This experiment is not a one-line restraint test. A high score requires repository inspection and boundary judgment, but not architecture theater.
