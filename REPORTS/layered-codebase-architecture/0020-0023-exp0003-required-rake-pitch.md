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

The highest score is a tie between `0022` and `0023` at 26/30. `0022` has the strongest durable test artifact. `0023` has the cleanest and smallest code change. Both are capped by the same boundary issue: each changes shared total-calculation behavior used outside the quick calculator without preserved proof that proposal/report behavior stayed unchanged.

`0021`, the no-skill arm, was competent but weaker. It reused the pitch policy but placed incompleteness inside `roofLineAdjustedFeet`, which makes a measurement conversion helper also mean "countable in this calculator." It also preserved no meaningful behavior test.

`0020`, the supplied original skill arm, explored the right area and tested the behavior, but left an unnecessary `.cursor/noun-map.md` artifact and still changed shared totals without protecting excluded consumers.

## Scores

| Dimension | 0020 supplied original | 0021 no skill | 0022 V1 | 0023 V2 |
| --- | ---: | ---: | ---: | ---: |
| Target discovery | 3 | 3 | 3 | 3 |
| Existing pitch-policy discovery | 3 | 3 | 3 | 3 |
| Responsibility ownership | 3 | 2 | 3 | 3 |
| Boundary placement | 1 | 1 | 1 | 1 |
| Behavior correctness | 3 | 2 | 3 | 3 |
| Affected-consumer protection | 1 | 1 | 1 | 1 |
| Structural restraint | 1 | 3 | 3 | 3 |
| Verification | 3 | 1 | 3 | 3 |
| Human intervention control | 3 | 3 | 3 | 3 |
| Safe stop behavior | 2 | 3 | 3 | 3 |
| **Total** | **23/30** | **22/30** | **26/30** | **26/30** |

## Shared Finding

Every arm found that rake pitch is already represented as `required` while hip and valley pitch are `optional`. That is the expected discovery.

Every arm also changed shared roof-line measurement behavior:
- `0020`, `0022`, and `0023` changed `roofLineMeasurementTotals(...)` or its immediate shared helpers.
- `0021` changed `roofLineAdjustedFeet(...)` to return `0` for incomplete required-pitch lines.

That shared code is also used by report/proposal-adjacent logic, including `shared/roofProbeReport.ts`. The prompt explicitly said not to change proposal/report behavior. Searching or reading those consumers was appropriate; the gap is that none of the runs preserved evidence proving those excluded consumers were unaffected. That caps both Boundary placement and Affected-consumer protection.

This does not invalidate the EXP-0003 runs. It means the experiment found the next real skill problem: distinguishing "reuse the existing domain authority" from "change a shared consumer contract without proof."

## Per-Run Notes

### 0020 - Supplied Original Skill

Score: 23/30

Strengths:
- Found the existing pitch policy and used it.
- Made unpitched rakes visibly incomplete in the quick calculator.
- Preserved targeted `npx tsx --test shared/roofLineMeasurements.test.ts` output with all tests passing.

Limits:
- Added `.cursor/noun-map.md` as a durable untracked artifact, which is not needed for the requested product change.
- Changed shared totals rather than a calculator-specific countability boundary.
- Did not preserve report/proposal protection evidence.

### 0021 - No Skill

Score: 22/30

Strengths:
- Found the relevant component and shared measurement policy without skill help.
- Kept the patch small and did not add extra repo artifacts.

Limits:
- Put incomplete-line exclusion into `roofLineAdjustedFeet(...)`, which broadens the meaning of an adjusted-feet helper.
- Preserved no meaningful behavior test, typecheck, build, or browser evidence.
- Did not protect report/proposal consumers.

### 0022 - V1 Skill

Score: 26/30

Strengths:
- Cleanly separated adjusted feet from countable feet with a `roofLineCountableFeet(...)` helper.
- Preserved targeted tests covering required rake pitch, pitched rake behavior, and optional hip/valley behavior.
- Kept the edit scoped to the component, shared measurement helper, and test.

Limits:
- Still changed shared totals used by other consumers.
- Did not preserve proof that proposal/report behavior stayed unchanged.

### 0023 - V2 Skill

Score: 26/30

Strengths:
- Smallest and cleanest patch in the block.
- Reused the existing pitch policy through `roofLinePitchIsComplete(...)`.
- Preserved an inline behavior check proving unpitched rakes were excluded while pitched rakes and optional-pitch lines counted.
- Left no unnecessary durable artifacts.

Limits:
- Still changed shared totals used by other consumers.
- Did not preserve proof that proposal/report behavior stayed unchanged.
- Did not add a durable test file, so its formal regression footprint is weaker than `0022`.

## Interpretation

V2 is still the best candidate direction because it achieved the same top score as V1 with less structural noise. V1 supplied better formal test coverage. The next skill revision should not focus on more target discovery; all arms already did that well.

The next revision should focus on affected-consumer proof:
- If a prompt limits behavior to one consumer, changing a shared helper is allowed only when the run preserves evidence that excluded consumers are unchanged.
- If that proof is unavailable or expensive, place the new behavior at the requesting consumer boundary or introduce a clearly named consumer-specific helper.
- "Inspected the other consumer" is not enough; the evidence packet needs a preserved check, test, or explicit static argument tied to the excluded behavior.

Recommended next action: draft V2.1 around that boundary rule before spending another run on `0024`.
