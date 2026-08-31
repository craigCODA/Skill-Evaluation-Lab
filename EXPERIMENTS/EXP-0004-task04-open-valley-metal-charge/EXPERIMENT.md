# EXP-0004: Open Valley Metal Customer Charge

## Question

How does `layered-codebase-architecture` change agent behavior on a cross-surface business-policy inconsistency when the prompt describes only the observed product failure and desired business outcome?

## Fixture

Repository: ShingleFile

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

Prompt: `PROMPT.txt`

The prompt intentionally does not name files, implementation details, architecture language, expected authorities, preservation requirements, or closed-valley behavior.

Evaluator-side baseline surfaces include:

- `shared/options/valleyMetal.ts`
- `shared/options/types.ts`
- `shared/options/index.ts`
- `shared/calculator/calculateEstimate.ts`
- `components/RoofingScopeForm.vue`
- `shared/contracts/roofProposalDocument.ts`
- `shared/contracts/roofProposalPricing.ts`
- `shared/contracts/roofProposalScope.ts`
- `shared/contracts/modules/compose.ts`

## Holdout Purpose

EXP-0004 is a harder cross-surface business-policy holdout.

The model must discover where billability is actually owned, distinguish option metadata from calculation and proposal presentation, propagate the intended customer charge through the existing estimate/proposal mechanisms, and preserve the closed-valley invariant without being told about it in the subject prompt.

This is not a one-line copy restraint test. It should separate shallow presentation patches, duplicated policy conditions, good existing-authority use, and architecture theater.

## Independent Variable

Skill condition only:

- `00-SUPPLIED`
- no explicit architecture skill
- `01-V1-CANDIDATE`
- `02-V2-GRAPH`

The skill artifacts remain frozen for the full GPT-5.1 block.

## Dependent Observations

- target and entry-point discovery
- discovery of the existing customer-billing metadata and actual money path
- responsibility ownership for the open-valley billability rule
- estimate total behavior
- proposal/customer pricing behavior
- preservation of non-open/closed-valley behavior
- duplicate policy conditions or drift-prone hard-coding
- structural restraint and semantic edit volume
- verification quality
- process compliance visible in the preserved trace

## Expected Correct Shape

The expected solution is cross-surface, but should still be narrow.

The strongest result discovers the existing option metadata and the actual estimate/proposal billing path, changes the billability rule once through an existing or narrowly extended authority, and makes estimate totals and proposal pricing derive from that authority without duplicating open-valley policy across consumers.

A Vue-only or presentation-only fix is incomplete even if the displayed grand total looks right.

Duplicating `style === "open"` or equivalent policy in multiple consumers is an ownership miss.

Creating a new pricing/domain package, broad layer extraction, noun map, or unrelated refactor is a restraint miss unless the baseline demonstrates the existing architecture cannot own the rule.

Do not require a specific filename, helper name, or exact patch for a top score. Score repository reality and behavior, not patch matching.

## Validity Boundary

The experiment is not valid as a matched comparison if the baseline, subject prompt, model, harness, tool access, or frozen skill artifact changes between arms without being recorded as a condition change.

Transcript/trace evidence supports process claims. Preserved command output or equivalent state proof supports verification claims at the level actually demonstrated.

Do not feed `BASELINE.md`, `SCORECARD.md`, prior experiment conclusions, expected authority, positive-control findings, or likely solution shape into the subject model.
