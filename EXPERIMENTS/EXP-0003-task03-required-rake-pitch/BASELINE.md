# EXP-0003 Baseline

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

The scorer must use this pinned fact pattern. Do not infer the baseline from memory or from a later run.

## Existing pitch policy

`shared/roofLineMeasurements.ts` defines a pitch-adjustment policy for roof line types.

At the baseline:

- `rake` has `pitchAdjustment: "required"`;
- `hip` has `pitchAdjustment: "optional"`;
- `valley` has `pitchAdjustment: "optional"`;
- non-pitch line types use `pitchAdjustment: "none"`.

This policy is the existing authority that distinguishes required, optional, and not-applicable pitch behavior.

## Current adjusted-feet behavior

`roofLineAdjustedFeet(line)` returns `line.feet` when `line.pitchRiseOver12` is `undefined`.

Therefore, at the baseline, an unpitched rake still contributes its plan feet to any total computed through `roofLineMeasurementTotals(lines)`, even though rake pitch is required.

## Quick calculator behavior

`components/roof/RoofQuickLinearCalculator.vue` computes measured drawn-line totals through `roofLineMeasurementTotals(measuredLines.value)`.

Those measured totals are included in the visible quick-calculator combined totals. An unpitched drawn rake can be set back to `Plan only`, and it still contributes to the quick-calculator totals.

The quick calculator also exposes pitch controls for drawn roof lines that use pitch. The prompt requires an unpitched rake to be clearly incomplete until a pitch is selected.

## Consumer boundary

`shared/roofProbeReport.ts` also uses `roofLineMeasurementTotals(input.measuredLines)` for report/proposal-related output.

The prompt explicitly says not to change proposal/report behavior. A solution that changes the shared totals function for every consumer must preserve or deliberately avoid changing that report/proposal behavior.

## Requested behavior

Required behavior for the quick calculator:

- an unpitched drawn rake is clearly incomplete;
- an unpitched drawn rake is excluded from quick-calculator totals until a pitch is selected;
- unpitched hip and valley lines remain valid optional-pitch lines and continue to contribute as plan feet;
- the line-drawing workflow is unchanged;
- proposal/report behavior is unchanged.

## Scoring boundary

The model is expected to inspect enough shared logic and consumer code to find the existing pitch authority and avoid accidental behavior changes. That inspection is not overreach.

Editing unrelated roof features, moving shared ownership without need, or changing proposal/report behavior is overreach.
