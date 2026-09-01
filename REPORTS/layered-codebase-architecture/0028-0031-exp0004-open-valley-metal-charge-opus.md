# EXP-0004 Open Valley Metal Charge Scoring, Runs 0028-0031

Date scored: 2026-09-01

Model block: Opus

Runs scored:
- `0028`: supplied original skill, `/layered-codebase-architecture`
- `0029`: no skill installed
- `0030`: V1 skill, `/layered-codebase-architecture`
- `0031`: V2 skill, `/layered-codebase-architecture`

## Summary

EXP-0004's Opus block is flatter than the GPT-5.1 block. All four arms found the executable estimate total and proposal pricing surfaces, all four flipped the valley metal option metadata to `billed: true`, all four added `valleyMetal.cost` to `grandTotal`, and all four added a proposal pricing line gated on the computed valley metal cost.

The highest score is a tie between no-skill and V2 at 23/30:

- `0029` no-skill found the same functional cross-surface fix as the skill arms and kept the patch to four tracked files.
- `0031` V2 also produced the four-file functional patch and explicitly reasoned about duplicate authority, saved-contract persistence, and not widening into a generic billed-option refactor.
- `0028` supplied original and `0030` V1 both score 22/30 because they made the same functional fix but also edited `shared/pricebook/types.ts`, a small extra documentation/type-comment surface that was not required for the executable estimate/proposal behavior.

No arm earned Behavior Correctness 3 or Verification 3. The preserved evidence does not include a targeted behavior check proving open-valley customer-charge propagation, final estimate total inclusion, proposal pricing inclusion, closed-valley non-charge, and no double-counting. Typecheck and lint claims in Cursor transcripts are treated as process evidence unless matching successful command output is preserved in the run packet.

## Scores

| Dimension | 0028 supplied original | 0029 no skill | 0030 V1 | 0031 V2 |
| --- | ---: | ---: | ---: | ---: |
| Target discovery | 2 | 2 | 2 | 2 |
| Existing billing authority discovery | 3 | 3 | 3 | 3 |
| Responsibility ownership | 3 | 3 | 3 | 3 |
| Boundary placement | 3 | 3 | 3 | 3 |
| Behavior correctness | 2 | 2 | 2 | 2 |
| Closed-valley invariant and no double counting | 2 | 2 | 2 | 2 |
| Proposal/contract protection | 2 | 2 | 2 | 2 |
| Structural restraint | 2 | 3 | 2 | 3 |
| Verification | 1 | 1 | 1 | 1 |
| Human intervention and safe stop | 2 | 2 | 2 | 2 |
| **Total** | **22/30** | **23/30** | **22/30** | **23/30** |

## Scoring Notes

The baseline fact pattern still controls the scoring: `billed` is real customer-billing metadata, but the executable money flow is not derived automatically from that field. `calculateRoofingEstimate()` manually builds `grandTotal`, and `buildRoofPricingLines()` manually emits proposal/customer pricing lines. A complete implementation therefore needs metadata, estimate total, and proposal pricing to agree.

The Opus no-skill arm is materially stronger than the GPT-5.1 no-skill arm because it did not stop at the estimate total. It found and updated proposal pricing too. That reduces the apparent skill-effect signal for EXP-0004 on this model.

All four diffs preserve the closed-valley invariant statically because `valleyMetalCost(...)` still computes `billableLf` from `valleys.style === "open" ? valleys.openLf : 0`, and the new estimate/proposal charges derive from `totals.valleyMetal.cost` rather than duplicating an open-valley style check in multiple consumers. This supports a score of 2, not 3, because no preserved behavior-level check proves the invariant or no-double-counting.

## Per-Run Notes

### 0028 - Supplied Original Skill

Score: 22/30

Strengths:
- Found option metadata, estimate totals, proposal pricing, UI copy, pricebook type comments, contract document usage, and server contract routes.
- Changed `valleyMetalOption.billed` to true and updated option wording.
- Added `valleyMetal.cost` to `calculateRoofingEstimate()` grand total.
- Added a `Valley metal` line to `buildRoofPricingLines(...)`.
- Updated the visible estimator copy that previously said valley metal was not billed.

Limits:
- Discovery used broad skill-driven route/UI/contract/adapter/domain tracing and had some failed or odd search output, so Target discovery is 2 rather than 3.
- Edited five tracked files, including `shared/pricebook/types.ts`; that extra type-comment edit is small but not required for the executable fix.
- The option metadata still says valley metal informs materials counts in one updated text field, even though the transcript noticed `materialsCounts` does not read job-level open-valley footage.
- No successful typecheck, test, build, runtime check, proposal-pricing behavior check, explicit open/closed-valley behavior check, or no-double-counting check was independently preserved.

### 0029 - No Skill

Score: 23/30

Strengths:
- Found the option metadata, estimate grand total, proposal pricing, material-count distinction, and contract paths.
- Correctly treated `billed: false` as metadata that had to align with executable money paths, not as an automatic total/proposal mechanism.
- Added `valleyMetal.cost` to the grand total and added an `Open valley metal` proposal pricing line.
- Kept the patch to four tracked files with no untracked subject-repository files.

Limits:
- Discovery started with a very broad subagent pass and then required direct cross-checking because initial search output disagreed with the subagent, so Target discovery is 2 rather than 3.
- The preserved terminal packet contains repository searches and package/test discovery only; no successful typecheck, test, build, runtime check, proposal-pricing behavior check, explicit open/closed-valley behavior check, or no-double-counting check was independently preserved.
- The UI copy says closed valley footage is billed through ice and water. That is directionally consistent with the per-plane ice/water path but still not a behavior proof for the job-level closed-valley invariant.

### 0030 - V1 Skill

Score: 22/30

Strengths:
- Found the valley metal option, estimate total, proposal pricing, UI, material-count, documentation, and contract paths through a subagent plus direct inspection.
- Avoided the GPT-5.1 V1 failure mode: it did not treat `billed: true` alone as sufficient.
- Added the estimate total term and proposal pricing line required for the customer-facing behavior.

Limits:
- The preserved main transcript is weaker than the subagent trace for implementation reasoning, and terminal evidence is mostly listing/search output.
- Edited five tracked files, including `shared/pricebook/types.ts`; the extra comment edit is a small restraint miss.
- The preserved terminal evidence includes one PowerShell `dir ... /b` error despite exported success metadata.
- No successful typecheck, test, build, runtime check, proposal-pricing behavior check, explicit open/closed-valley behavior check, or no-double-counting check was independently preserved.

### 0031 - V2 Skill

Score: 23/30

Strengths:
- Found valley metal option metadata, estimate totals, proposal pricing, UI presentation, material counts, contract store, docs, and persistence paths.
- Explicitly identified the duplicate-authority risk between option metadata, the hand-written grand-total sum, and proposal pricing omission.
- Declined the broader generic billed-option refactor because the repository lacks a uniform amount accessor across option breakdowns.
- Produced the cleaner four-file functional patch, without editing `shared/pricebook/types.ts`.
- Preserved no untracked subject-repository files.

Limits:
- Discovery used two subagents and broad repository exploration, so Target discovery is 2 rather than 3.
- The transcript records `npm install`, `npm run typecheck`, ReadLints, and typecheck/lint success claims, but the preserved terminal files do not include successful npm install or typecheck output. Those claims remain process evidence, not independently preserved verification success.
- The local archive includes ignored dependency/build directories `node_modules/` and `.nuxt/` created during verification. They are not semantic edit volume, but they are a preservation artifact.
- No targeted open/closed-valley behavior check, proposal-pricing behavior check, or no-double-counting check was independently preserved.

## Cross-Model Interpretation

Across EXP-0004 so far, V2 is the most reliable skill candidate, but this Opus block does not show V2 outperforming no-skill on functional output. Instead, the model itself found the full cross-surface fix in the no-skill arm.

The combined GPT-5.1 and Opus evidence says:

- V2 avoided the V1 metadata-only failure seen in GPT-5.1 `0026`.
- V2 matched the best functional patch shape in both model blocks.
- No-skill behavior is model-sensitive: GPT-5.1 no-skill missed proposal pricing, while Opus no-skill found it.
- The repeated weakness across both models is not architecture theater; it is missing behavior-level verification. No EXP-0004 arm preserved the targeted open/closed/no-double-counting proof required for Behavior 3 and Verification 3.

Do not edit, promote, or rewrite the skill solely from this score. The next useful action is to compare EXP-0003 and EXP-0004 together and decide whether a V2.1 draft is justified by a repeated failure pattern rather than a single-model result.
