# EXP-0002: Quick Calculator Clear Label Holdout

## Question

How does the `layered-codebase-architecture` skill change agent behavior on a bounded copy correction where the correct architectural decision is to make no architectural change?

## Fixture

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Target: `components/roof/RoofQuickLinearCalculator.vue`

This experiment deliberately sits near the Task 01 roof-measurement code. Neighboring Task 01 files are available to the model, but they are not part of this task. That adjacency is both useful pressure and a contamination risk.

## Holdout purpose

Task 01 explicitly invited cleanup and restructuring. EXP-0002 does not.

The requested change is a label correction whose fully correct implementation may be a one-line in-place edit. A model must be able to inspect enough repository reality to understand the behavior without turning that inspection into unnecessary architecture work.

A result that changes nothing architectural can receive the highest score.

## Independent variable

Skill condition only:

- no explicit architecture skill
- `00-SUPPLIED`
- `01-V1-CANDIDATE`
- `02-V2-GRAPH`

The skill artifacts remain frozen for the full four-arm Grok block.

## Dependent observations

- target discovery
- repository-reality reading
- responsibility and boundary judgment
- behavior preservation
- structural restraint
- semantic edit volume
- verification quality
- process compliance visible in the preserved trace

## Expected correct shape

The expected architectural decision is no architectural restructuring.

The strongest result changes the visible bottom-button label from `Clear entries` to `Clear manual entries` in `RoofQuickLinearCalculator.vue`, with only the minimum matching accessible/visible copy change if one is actually required by the existing markup.

No new node, folder, helper, composable, shared module, noun map, import-graph change, or neighboring-file cleanup is required by the task.

## Validity boundary

The experiment is not valid as a matched comparison if the baseline, task prompt, model, harness, tool access, or frozen skill artifact changes between arms without being recorded as a condition change.

Transcript/trace evidence supports process claims. Preserved command output or equivalent state proof supports verification claims at the level actually demonstrated.
