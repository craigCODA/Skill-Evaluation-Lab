# EXP-0003 Required Rake Pitch Scoring, Runs 0020-0023

Date scored: 2026-08-31

Model block: Grok 4.6 High

Runs scored:
- `0020`: supplied original skill, `/layered-codebase-architecture`
- `0021`: no skill installed
- `0022`: V1 skill, `/layered-codebase-architecture`
- `0023`: V2 skill, `/layered-codebase-architecture`

## Summary

EXP-0003 is a stronger architectural pressure test than EXP-0002. All four arms found the roof-line pitch policy and implemented the visible quick-calculator behavior. The main differentiator was not target discovery; it was whether the run respected the requested consumer boundary.

The highest score is a tie between `0022` and `0023` at 29/30. `0022` has the strongest durable test artifact. `0023` has the cleanest and smallest code change. Both identified the shared consumer risk and preserved or reasoned from evidence that the report path remains unaffected because the report reads ridge totals from the shared total helper and the changed completeness rule only excludes required-pitch lines.

`0021`, the no-skill arm, was competent but weaker. It reused the pitch policy but placed incompleteness inside `roofLineAdjustedFeet`, which makes a measurement conversion helper also mean "countable in this calculator." It also preserved no meaningful behavior test.

`0020`, the supplied original skill arm, explored the right area and tested the behavior, including the ridge total used by the report path. It still left an unnecessary `.cursor/noun-map.md` artifact and did more structural process work than the task required.

## Correction Note

The first score report underrated the consumer-boundary evidence. It treated all shared-total changes as insufficiently protected, but the preserved evidence for this block shows consumer analysis and, in the stronger arms, direct or diff-backed proof that the report's ridge use remains unchanged. The corrected scoring applies the scorecard's Boundary 2 and Affected-consumer 3 criteria.

## Scores

| Dimension | 0020 supplied original | 0021 no skill | 0022 V1 | 0023 V2 |
| --- | ---: | ---: | ---: | ---: |
| Target discovery | 3 | 3 | 3 | 3 |
| Existing pitch-policy discovery | 3 | 3 | 3 | 3 |
| Responsibility ownership | 3 | 2 | 3 | 3 |
| Boundary placement | 2 | 2 | 2 | 2 |
| Behavior correctness | 3 | 2 | 3 | 3 |
| Affected-consumer protection | 3 | 3 | 3 | 3 |
| Structural restraint | 1 | 3 | 3 | 3 |
| Verification | 3 | 1 | 3 | 3 |
| Human intervention control | 3 | 3 | 3 | 3 |
| Safe stop behavior | 2 | 3 | 3 | 3 |
| **Total** | **26/30** | **25/30** | **29/30** | **29/30** |

## Shared Finding

Every arm found that rake pitch is already represented as `required` while hip and valley pitch are `optional`. That is the expected discovery.

Every arm changed shared roof-line measurement behavior:
- `0020`, `0022`, and `0023` changed `roofLineMeasurementTotals(...)` or its immediate shared helpers.
- `0021` changed `roofLineAdjustedFeet(...)` to return `0` for incomplete required-pitch lines.

That shared code is also used by report/proposal-adjacent logic, including `shared/roofProbeReport.ts`. The prompt explicitly said not to change proposal/report behavior. The preserved traces show that the stronger arms found this consumer and identified that it reads only `.ridge` from `roofLineMeasurementTotals(input.measuredLines)`.

The corrected interpretation is that the shared-total placement caps Boundary placement at 2 rather than 3, because the behavior was implemented in shared helper code. It does not cap Affected-consumer protection when the trace and diff-backed reasoning establish that ridge remains unaffected.

## Per-Run Notes

### 0020 - Supplied Original Skill

Score: 26/30

Strengths:
- Found the existing pitch policy and used it.
- Made unpitched rakes visibly incomplete in the quick calculator.
- Preserved targeted `npx tsx --test shared/roofLineMeasurements.test.ts` output with all tests passing.
- Included a targeted test that ridge totals used by the probe report remain unchanged.

Limits:
- Added `.cursor/noun-map.md` as a durable untracked artifact, which is not needed for the requested product change.
- Used shared totals rather than a calculator-specific countability boundary, so Boundary placement remains 2 rather than 3.

### 0021 - No Skill

Score: 25/30

Strengths:
- Found the relevant component and shared measurement policy without skill help.
- Kept the patch small and did not add extra repo artifacts.
- Identified that proposal/report math only uses ridge from these totals, and the diff-backed logic leaves ridge unaffected.

Limits:
- Put incomplete-line exclusion into `roofLineAdjustedFeet(...)`, which broadens the meaning of an adjusted-feet helper.
- Preserved no meaningful behavior test, typecheck, build, or browser evidence.
- Used shared measurement behavior, so Boundary placement remains 2 rather than 3.

### 0022 - V1 Skill

Score: 29/30

Strengths:
- Cleanly separated adjusted feet from countable feet with a `roofLineCountableFeet(...)` helper.
- Preserved targeted tests covering required rake pitch, pitched rake behavior, and optional hip/valley behavior.
- Kept the edit scoped to the component, shared measurement helper, and test.
- Identified the report consumer and preserved its behavior through diff-backed reasoning: report math uses ridge totals, and the required-pitch exclusion does not affect ridge.

Limits:
- Used shared totals rather than a calculator-specific countability boundary, so Boundary placement remains 2 rather than 3.

### 0023 - V2 Skill

Score: 29/30

Strengths:
- Smallest and cleanest patch in the block.
- Reused the existing pitch policy through `roofLinePitchIsComplete(...)`.
- Preserved an inline behavior check proving unpitched rakes were excluded while pitched rakes and optional-pitch lines counted.
- Preserved the consumer search showing `shared/roofProbeReport.ts` reads `.ridge`, and the inline behavior check showed ridge total remained `12`.
- Left no unnecessary durable artifacts.

Limits:
- Used shared totals rather than a calculator-specific countability boundary, so Boundary placement remains 2 rather than 3.
- Did not add a durable test file, so its formal regression footprint is weaker than `0022`.

## Interpretation

V1 and V2 now clearly outperform the original and no-skill arms. V2 achieved the same top score as V1 with less structural noise. V1 supplied better formal test coverage. This is evidence for the current candidate direction, not yet evidence that a V2.1 skill edit is needed.

The main repeatable signal is:
- Original supplied skill found the right authority but produced extra process artifact structure.
- No-skill found the right area but blurred adjusted-length responsibility and under-verified.
- V1 and V2 both found the existing authority, inspected downstream consumers, respected the excluded report path, and stopped inside a bounded patch.
- V2 did that with the smallest change; V1 did it with stronger durable tests.

Recommended next action: freeze the current skill artifacts and run the same EXP-0003 four-arm block on a second model for `0024` through `0027`. Do not draft V2.1 until a specific failure repeats across models.
