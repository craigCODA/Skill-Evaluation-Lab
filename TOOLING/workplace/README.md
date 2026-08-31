# Workplace Lifecycle

This tooling runs the public lab with the same preserve-first shape as the original ShingleFile workplace.

Local-only state:

- `MOTHER/` stores the baseline Git truth.
- `ACTIVE/ShingleFile-main/` stores exactly one open subject run.
- `ACTIVE/.run-state/` stores operator metadata, Cursor transcripts, and execution records outside the subject workspace.
- `ARCHIVES/local/*.zip` stores local-only ZIP archives. These files are ignored by Git and are not retrievable from a fresh clone.

Canonical evidence still lands in the public lab:

- `EVIDENCE/<run-id>/`
- `EXPERIMENTS/*/runs/*`
- `DEVELOPMENT-HISTORY/<run-id>.md`
- `DATA/runs.json`

`fresh` never deletes an open `ACTIVE` run. `archive` refuses to preserve anything unless the active metadata matches the requested run and a real `execution.json` exists.

## Harness Attribution

`fresh` writes the Cursor harness before the model runs:

- `.cursor/cli.json`
- `.cursor/skills/<skill>/*` for skill arms

It also records a pre-execution snapshot in `ACTIVE/.run-state/`, then `archive` copies that snapshot into `EVIDENCE/<run-id>/`:

- `harness-manifest.json` identifies harness-created files, roles, sizes, and SHA-256 hashes.
- `pre-execution-untracked-files.txt` records untracked files that existed before model execution.
- `git-status-full.txt` preserves raw final status for audit.
- `model-created-git-status.txt` and `git-status.txt` exclude harness-created and pre-execution untracked paths.
- `model-created-untracked-files.txt` and `untracked-files.txt` exclude harness-created and pre-execution untracked paths.
- `tracked-subject-files.txt` lists tracked subject-repository files changed relative to the frozen matrix baseline.

Scoring must use the model-created and tracked-subject views. It must not count `.cursor/cli.json` or installed treatment skills as semantic edit volume or agent overreach.

## Baseline Diff

`archive` records both `baseline-head.txt` and `final-head.txt`. The canonical tracked change files are generated against the matrix baseline commit, not the final `HEAD`:

- `git-diff-stat.txt`
- `git-diff-name-status.txt`
- `diff.patch`

For EXP-0002 the frozen baseline is `cd393ddd60548823dabd6875060247693a22c1be`. This keeps change evidence meaningful even if a model commits inside `ACTIVE` before preservation.

## Result Assets

`RESULT-ASSET.md` and `archive-manifest.json` record the local archive name, SHA-256, entry count, and testzip result. Until the archive is uploaded externally, the storage class is `local-only`, publication status is `pending`, and `release_tag` remains `local-unreleased`.

The intended durable publication path is a GitHub Release asset or another external artifact store. Do not commit ZIP archives into normal Git history. After publication, update the evidence with the durable tag or artifact identity and verify the release inventory, for example with `py -3 TOOLING\verification\verify_lab.py --release-json <release-json>`.

```powershell
py -3 tools\workplace.py mother-init --source D:\Downloads\ShingleFile-original-workplace\ShingleFile-original-workplace\MOTHER\ShingleFile-main.git
py -3 tools\workplace.py run-block
py -3 TOOLING\verification\verify_lab.py
```
