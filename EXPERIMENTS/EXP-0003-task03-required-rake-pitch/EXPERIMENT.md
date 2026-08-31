# EXP-0003: Required Rake Pitch Quick Calculator Boundary

## Question

How does the `layered-codebase-architecture` skill change agent behavior on a bounded roof-calculator bug where the correct solution requires finding and respecting an existing responsibility boundary?

## Fixture

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Prompt: `PROMPT.txt`

The prompt intentionally does not name a target file. The model must discover the relevant quick-calculator surface, the shared roof-line pitch policy, and any downstream consumers that must not change.

Evaluator-side baseline surfaces include:

- `components/roof/RoofQuickLinearCalculator.vue`
- `shared/roofLineMeasurements.ts`
- `shared/roofProbeReport.ts`

## Holdout purpose

EXP-0002 is the restraint floor: with explicit no-restructure wording, all Grok 4.6 High arms stopped at the same one-line label correction.

EXP-0003 removes that artificial restraint and asks for a real behavior fix. The model should inspect shared line-measurement logic and its consumers when needed. Inspection is not overreach here; unnecessary ownership moves or proposal/report behavior changes are.

The experiment tests whether the skill helps the model:

- find the existing required/optional/none pitch authority;
- reuse or extend the smallest existing authority needed;
- apply the incomplete-state behavior at the quick-calculator boundary;
- preserve line drawing and proposal/report behavior;
- stop without broad restructuring.

## Independent variable

Skill condition only:

- no explicit architecture skill
- `00-SUPPLIED`
- `01-V1-CANDIDATE`
- `02-V2-GRAPH`

The skill artifacts remain frozen for the full first-model block.

## Dependent observations

- target and entry-point discovery
- existing pitch-policy discovery
- responsibility ownership
- boundary placement
- behavior correctness
- affected-consumer protection
- structural restraint
- semantic edit volume
- verification quality
- process compliance visible in the preserved trace

## Expected correct shape

The expected solution is small, but not necessarily one-line.

The strongest result discovers that rake already has required pitch semantics while hip and valley are optional, then makes unpitched rakes visibly incomplete and excludes them from quick-calculator totals until a pitch is selected. It preserves the existing line-drawing workflow and does not alter proposal/report behavior.

A hard-coded `line.type === "rake"` UI patch can be behaviorally correct but scores lower if it bypasses the existing pitch policy without justification.

Creating validators, new domain packages, broad composables, folder moves, import-graph rewrites, or proposal/report edits is not required by the task.

## Validity boundary

The experiment is not valid as a matched comparison if the baseline, task prompt, model, harness, tool access, or frozen skill artifact changes between arms without being recorded as a condition change.

Transcript/trace evidence supports process claims. Preserved command output or equivalent state proof supports verification claims at the level actually demonstrated.
