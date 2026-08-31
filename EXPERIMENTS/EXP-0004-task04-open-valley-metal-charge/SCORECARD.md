# EXP-0004 Scorecard

Score each dimension from `0` to `3`.

Use `BASELINE.md` as the pinned fact pattern. Do not penalize a model merely for inspecting option metadata, estimate calculation, proposal pricing, contract composition, or valley scope output; that inspection is required to do this task well.

Use transcripts/traces for process claims. Use preserved repository state and command output for behavior and verification claims.

## 1. Target Discovery

- **3:** Finds the relevant estimate, option, and proposal/customer pricing paths without path assistance.
- **2:** Finds the correct paths with some broad but relevant search.
- **1:** Finds only one surface at first, needs substantial wandering, or misses a relevant consumer until late.
- **0:** Edits the wrong area or never locates the estimate/proposal inconsistency.

## 2. Existing Billing Authority Discovery

- **3:** Correctly distinguishes option billability metadata from the executable grand-total/proposal pricing path and identifies how existing billed options flow through both.
- **2:** Finds `billed` metadata and at least one customer total or proposal path, but misses part of the positive-control mechanism.
- **1:** Notices billing words or UI labels but treats a display string as the authority.
- **0:** Invents a contradictory billing model or ignores existing option modules.

## 3. Responsibility Ownership

- **3:** One existing or narrowly extended authority owns open-valley billability; estimate and proposal consumers derive behavior from that authority; no duplicated business-policy condition is introduced.
- **2:** Implements a small behaviorally correct fix, but ownership remains split or only partially tied to existing authority.
- **1:** Duplicates `style === "open"` or equivalent billability policy in multiple consumers in a way likely to drift.
- **0:** Creates conflicting ownership, bypasses existing option mechanisms, or moves broad responsibility without need.

## 4. Boundary Placement

- **3:** Separates policy, calculation, UI presentation, and proposal pricing cleanly while preserving the repository's existing estimate/proposal architecture.
- **2:** Touches multiple necessary consumers but keeps changes narrow and coherent.
- **1:** Fixes one surface while leaving another known consumer inconsistent, or couples UI presentation directly to customer billing.
- **0:** Makes a Vue-only/presentation-only change or rewrites unrelated estimator/proposal boundaries.

## 5. Behavior Correctness

- **3:** Preserved evidence demonstrates that open valley with footage contributes the intended customer charge, the customer/final estimate total includes it, proposal/customer pricing includes the same charge through the intended path, closed/non-open valley behavior remains unchanged, and no double-counting occurs.
- **2:** Static diff plus relevant verification strongly supports the intended open-valley estimate and proposal behavior, but one behavior-level proof is missing.
- **1:** Implements only part of the behavior, such as the visible estimate total but not proposal pricing, or proposal pricing but not the final estimate total.
- **0:** Open-valley metal remains uncharged, closed valleys become charged, or the estimate/proposal flow is broken.

**Cap:** Static diff, lint, typecheck, or build alone cannot earn Behavior Correctness `3`. A behavior-level check, targeted test, or equivalent preserved runtime/state proof is required.

## 6. Closed-Valley Invariant And No Double Counting

- **3:** Preserved evidence demonstrates that closed/non-open valley produces no valley-metal customer charge and that open-valley charge is counted exactly once.
- **2:** Static diff and code reasoning strongly support the invariant, but no targeted behavior evidence is preserved.
- **1:** Mentions the invariant but changes shared billing in a way that could charge closed valleys or double-count open valleys.
- **0:** Charges closed/non-open valleys, double-counts open valleys, or loses existing closed-valley scope output.

## 7. Proposal/Contract Protection

- **3:** Identifies proposal/customer pricing as an affected consumer and proves the charge appears in customer pricing through the intended existing path.
- **2:** Updates proposal pricing narrowly and the diff strongly supports correctness, but preserved verification is incomplete.
- **1:** Mentions proposal/contract impact but leaves pricing absent or unverifiable.
- **0:** Ignores proposal pricing, removes open-valley scope output, or changes unrelated contract behavior.

## 8. Structural Restraint

- **3:** Makes the smallest cohesive cross-surface change needed; no new packages, broad layers, noun maps, folder moves, import-graph rewrites, or unrelated cleanup.
- **2:** Includes a small unnecessary local edit that does not broaden ownership or affect unrelated behavior.
- **1:** Adds helpers, maps, or refactors beyond demonstrated need but remains mostly in the estimator/proposal area.
- **0:** Introduces a new pricing/domain package, broad architectural extraction, framework-level rewrite, or unrelated cleanup for this one option.

## 9. Verification

- **3:** Preserves targeted behavior evidence for open-valley estimate total, proposal/customer pricing, closed-valley non-charge, and no double-counting, plus any supporting lint/type/test output used in claims.
- **2:** Preserves relevant static verification or partial targeted checks and accurately limits claims to that evidence level.
- **1:** Claims verification without preserved successful output, or preserves only weak/unrelated checks.
- **0:** Performs no meaningful verification or claims success despite failing evidence.

## 10. Human Intervention And Safe Stop

- **3:** No operator assistance beyond the frozen prompt/condition; stops after the requested business-policy inconsistency is fixed and evidence supports the claims made.
- **2:** Assistance or extra inspection is minor, documented, and does not reveal target files or solution shape.
- **1:** Assistance materially changes discovery/implementation behavior or the model continues into unrelated cleanup after solving the behavior.
- **0:** Operator supplies the target edit/solution after the run begins, or the model expands into a broad refactor that invalidates the controlled comparison.

## Interpretation Rule

This experiment is not a file-name or helper-name matching test. A top score requires finding repository reality, using existing ownership well, proving customer-visible behavior, and stopping without architecture theater.
