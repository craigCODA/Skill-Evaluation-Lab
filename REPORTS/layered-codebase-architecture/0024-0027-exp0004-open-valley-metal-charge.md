# EXP-0004 Open Valley Metal Charge Scoring, Runs 0024-0027

Date scored: 2026-08-31

Model block: GPT-5.1

Runs scored:
- `0024`: supplied original skill, `/layered-codebase-architecture`
- `0025`: no skill installed
- `0026`: V1 skill, `/layered-codebase-architecture`
- `0027`: V2 skill, `/layered-codebase-architecture`

## Summary

EXP-0004 separates the conditions more sharply than EXP-0002 and differently than EXP-0003. The supplied original and V2 arms both reached the executable estimate plus proposal-pricing surfaces. No-skill fixed the estimate total and UI copy but missed proposal pricing. V1 made the cleanest-looking patch but failed the actual money path by treating `billed: true` metadata as if it were an automatic executable aggregator.

No arm earned Behavior Correctness 3 or Verification 3. None preserved a targeted behavior check demonstrating open valley customer charge, final estimate total inclusion, proposal/customer pricing inclusion, closed-valley non-charge, and no double-counting. The best behavior score available in this block is therefore 2, based on static diff plus limited preserved verification.

The highest score is a tie between `0024` and `0027` at 22/30:

- `0024` covered more presentation/documentation surfaces, including UI copy and pricebook comment text, but had more edit volume.
- `0027` made the cleaner executable cross-surface patch, but left the visible `RoofingScopeForm.vue` valley-metal copy saying the charge is not added to the customer total.

The strongest skill signal is not "V2 beats everything." It is that V2 avoided the V1 metadata-only failure while staying narrower than the supplied original. This supports keeping V2 as the better candidate direction, but it does not yet justify editing V2 from this experiment alone.

## Scores

| Dimension | 0024 supplied original | 0025 no skill | 0026 V1 | 0027 V2 |
| --- | ---: | ---: | ---: | ---: |
| Target discovery | 2 | 1 | 2 | 2 |
| Existing billing authority discovery | 3 | 2 | 2 | 3 |
| Responsibility ownership | 3 | 2 | 1 | 3 |
| Boundary placement | 3 | 1 | 1 | 2 |
| Behavior correctness | 2 | 1 | 0 | 2 |
| Closed-valley invariant and no double counting | 2 | 2 | 1 | 2 |
| Proposal/contract protection | 2 | 1 | 1 | 2 |
| Structural restraint | 2 | 3 | 3 | 3 |
| Verification | 1 | 1 | 1 | 1 |
| Human intervention and safe stop | 2 | 2 | 2 | 2 |
| **Total** | **22/30** | **16/30** | **14/30** | **22/30** |

## Scoring Notes

The baseline establishes that `billed` is real customer-billing metadata, but not an automatic executable money-flow mechanism. `calculateRoofingEstimate()` manually builds `grandTotal`, and `buildRoofPricingLines()` manually emits customer proposal pricing lines. A high-scoring run therefore had to reconcile the metadata with those executable consumers.

The proposal path matters independently from the contract amount. `roofProposalDocument.ts` uses `roofingTotals.grandTotal` for the contract amount and also uses `buildRoofPricingLines(...)` for the Contract Price / Scope Summary pricing section. A run that only changes `grandTotal` still leaves the customer pricing line absent.

Closed-valley preservation is statically supported when the run leaves `valleyMetalCost(...)` computing `billableLf` only for `style === "open"` and adds only `valleyMetal.cost`. It cannot earn 3 without a preserved behavior check.

## Per-Run Notes

### 0024 - Supplied Original Skill

Score: 22/30

Strengths:
- Found option metadata, estimate totals, proposal pricing, and UI presentation.
- Changed `valleyMetalOption.billed` to true and updated option wording.
- Added `valleyMetal.cost` to `calculateRoofingEstimate()` grandTotal.
- Added a `Valley metal` line to `buildRoofPricingLines(...)`.
- Updated visible UI copy that previously said valley metal was not billed.

Limits:
- Initial discovery involved tool/path wandering, so Target discovery is 2 rather than 3.
- Edited five files, including `shared/pricebook/types.ts`; that extra documentation edit is small but not required for the executable fix.
- Preserved `npm run typecheck` failed because `nuxt` was not recognized.
- Preserved no targeted open/closed valley behavior check and no no-double-counting check.

### 0025 - No Skill

Score: 16/30

Strengths:
- Found the valley-metal option and customer grand-total calculation.
- Kept the patch small and did not create extra artifacts.
- Preserved the closed-valley calculation shape by leaving `valleyMetalCost(...)` intact.

Limits:
- Did not change `shared/contracts/roofProposalPricing.ts`, so proposal customer pricing remains missing the valley-metal line.
- Claimed the roofing proposal would reflect the charge through `grandTotal`, but the pricing section still lacks the line required by the experiment.
- Preserved no typecheck, test, build, browser/runtime check, or targeted behavior check.

### 0026 - V1 Skill

Score: 14/30

Strengths:
- Found the option metadata and looked at relevant estimate/proposal concepts.
- Made the smallest patch and left no untracked subject files.

Limits:
- Changed only `shared/options/valleyMetal.ts`.
- Treated `billed: true` as sufficient for customer total and proposal pricing even though the baseline proves executable money flow is manually wired.
- Left `calculateRoofingEstimate()` excluding `valleyMetal.cost`.
- Left `buildRoofPricingLines(...)` without a valley-metal pricing line.
- Preserved no targeted behavior check or successful typecheck.

### 0027 - V2 Skill

Score: 22/30

Strengths:
- Found option metadata, estimate total, and proposal pricing.
- Changed `valleyMetalOption.billed` to true and updated option wording.
- Added `valleyMetal.cost` to `calculateRoofingEstimate()` grandTotal.
- Added a `Valley metal` line to `buildRoofPricingLines(...)`.
- Kept the patch to three tracked files with no untracked subject-repository files.

Limits:
- Initial discovery involved tool/path wandering, so Target discovery is 2 rather than 3.
- Did not update `components/RoofingScopeForm.vue`, leaving the visible valley-metal copy that says the amount is not added to the customer total.
- Preserved `npm run typecheck` failed because `nuxt` was not recognized.
- Preserved no targeted open/closed valley behavior check and no no-double-counting check.

## Interpretation

EXP-0004 shows a real cross-surface skill effect:

- No-skill handled the obvious estimate-total surface but missed the proposal pricing consumer.
- V1 over-compressed responsibility into option metadata and missed the executable money path.
- V2 recovered the necessary executable estimate plus proposal-pricing path without the supplied original's extra documentation edit.
- Supplied original and V2 tie overall because supplied original handled stale UI copy while V2 stayed cleaner but left that presentation mismatch.

The repeated weakness in this block is verification, not broad restructuring. Every arm failed to preserve a targeted behavior proof. The next useful step is replication before skill editing: run EXP-0004 on a second model or inspect whether the missing behavior-check pattern repeats across more than this GPT-5.1 block.

Do not promote, rewrite, or edit the skill solely from this score. Do not rerun or rewrite `0024` through `0027`; they are valid preserved evidence for this GPT-5.1 block.
