# Evidence Standard

Evidence is the preserved factual record of a run.

Preserve the exact prompt, exact skill hashes, model and visible harness settings, baseline repository identity, human intervention, transcript or raw run record, exact result state, SHA-256 checksums, and verification actually performed whenever those artifacts exist.

Static inspection is not runtime verification. Transcript claims are not independently verified unless the resulting state or command output is also preserved.

Never reset, clean, or repair a failed run before preservation.

Evidence files should avoid interpretation except where a factual caveat is needed to describe what was actually preserved.

Analysis belongs in `EXPERIMENTS/*/runs/*/ANALYSIS.md`, `DEVELOPMENT-HISTORY/`, `REPORTS/`, or `RESEARCH/`.

If a run has no release asset, `RESULT-ASSET.md` must state the reason.
