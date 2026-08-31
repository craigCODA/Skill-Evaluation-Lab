# Cursor Agent Runner Design

## Goal

Add lab tooling that can prepare, run, and preserve Cursor Agent CLI evaluation runs without relying on ad hoc manual Cursor sessions.

## Scope

The runner targets planned Skill Evaluation Lab runs such as `EXP-0002-task02-quick-calculator-clear-label` runs `0016` through `0019`.

It must not silently rewrite preserved evidence. A failed or incomplete Cursor run is still evidence and consumes the run ID when preservation is requested.

## External Boundary

The execution boundary is the official Cursor Agent CLI executable, `agent`.

The local Cursor editor wrapper `cursor` is not treated as equivalent because this machine currently exposes editor-style options through `cursor agent`, not the documented headless `agent -p` behavior.

The runner may launch `agent` only after preflight confirms:

- the executable exists;
- a concrete Cursor model ID was provided;
- the baseline repository source exists or is cloneable;
- the target run ID is planned and not already preserved;
- local lab metadata passes verification before starting.

## Data Flow

1. Load a run matrix from `TOOLING/cursor-runner/runs/EXP-0002-task02-quick-calculator-clear-label.json`.
2. Prepare a fresh run workspace under `.worktrees/cursor-runs/run-XXXX`.
3. Clone the baseline repository and check out the pinned baseline commit.
4. For skill arms, copy the frozen skill artifact into `.cursor/skills/layered-codebase-architecture`.
5. Build the exact prompt. Skill arms prepend `/layered-codebase-architecture  `. No-skill arms use only the frozen prompt text.
6. Launch `agent -p --force --trust --workspace <workspace> --model <model-id> --output-format stream-json --stream-partial-output <prompt>`.
7. Capture stdout JSONL, stderr, exit code, command metadata, and post-run Git state.
8. Preserve evidence under `EVIDENCE/XXXX` and the full result ZIP under `ARCHIVES/local/`.
9. Update `DATA/runs.json`, the experiment run index, and `CURRENT-STATE.md`.
10. Remove the prepared workspace only after the ZIP validates.

## Fail-Closed Rules

- Do not run when `agent` is missing.
- Do not run when the model ID is missing or still a placeholder.
- Do not overwrite `EVIDENCE/XXXX`.
- Do not overwrite an archive ZIP.
- Do not preserve transcript-only verification as command-level verification.
- Do not edit skill artifacts while running a frozen comparison block.
- Do not delete a run workspace until the archive ZIP test passes.

## Verification

Unit tests must cover prompt construction, run config loading, workspace preparation, archive preservation, and multi-experiment verification. The existing lab verifier must continue to pass on the current `0001` through `0015` record and must not block planned future runs only because `0015` is currently the latest preserved run.
