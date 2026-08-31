# Workplace Lifecycle

This tooling runs the public lab with the same preserve-first shape as the original ShingleFile workplace.

Local-only state:

- `MOTHER/` stores the baseline Git truth.
- `ACTIVE/ShingleFile-main/` stores exactly one open subject run.
- `ACTIVE/.run-state/` stores operator metadata, Cursor transcripts, and execution records outside the subject workspace.

Canonical evidence still lands in the public lab:

- `EVIDENCE/<run-id>/`
- `ARCHIVES/local/run-<run-id>-<label>.zip`
- `EXPERIMENTS/*/runs/*`
- `DEVELOPMENT-HISTORY/<run-id>.md`
- `DATA/runs.json`

`fresh` never deletes an open `ACTIVE` run. `archive` refuses to preserve anything unless the active metadata matches the requested run and a real `execution.json` exists.

```powershell
py -3 tools\workplace.py mother-init --source D:\Downloads\ShingleFile-original-workplace\ShingleFile-original-workplace\MOTHER\ShingleFile-main.git
py -3 tools\workplace.py run-block
py -3 TOOLING\verification\verify_lab.py
```
