# EXP-0002 Grok Restraint Floor

Runs covered: `0016` through `0019`

Model: Grok 4.6 High

Baseline commit: `cd393ddd60548823dabd6875060247693a22c1be`

## Summary

EXP-0002 is retained as the restraint floor for `layered-codebase-architecture`.

All four preserved Grok 4.6 High arms made the same semantic repository change: the visible quick-calculator bottom-button label changed from `Clear entries` to `Clear manual entries` in `components/roof/RoofQuickLinearCalculator.vue`.

No arm created a new helper, composable, module, folder, import-graph change, or neighboring roof-feature edit.

## Interpretation

The result is useful, but narrow. EXP-0002 shows that under an explicit bounded-copy prompt with no-restructure wording, the supplied skill, no-skill control, V1, and V2 all reached the same restrained outcome.

That is a floor, not a promotion signal by itself. It does not test whether a model can find an existing responsibility boundary, preserve an affected consumer, and stop when the implementation requires more than a one-line presentation change.

No skill revision is justified by EXP-0002 alone.

## Evidence Boundary

The preserved evidence bytes for `0016` through `0019` remain unchanged.

The archives for `0016` through `0019` are local-only in `ARCHIVES/local/` and are not fresh-clone retrievable until they are published to durable release or artifact storage.
