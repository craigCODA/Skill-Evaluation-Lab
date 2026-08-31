# Cursor Agent Runner

This directory contains operator-facing configuration for running planned lab arms through the official Cursor Agent CLI.

The executable boundary is `agent`, not the GUI `cursor` command. On this machine, `cursor agent -p` behaved like the editor wrapper instead of the documented headless CLI, so runner preflight requires a real `agent` executable.

## Current Run Matrix

The EXP-0002 Grok holdout block is defined in:

```text
TOOLING/cursor-runner/runs/EXP-0002-task02-quick-calculator-clear-label.json
```

The planned order is:

```text
0016  NO-SKILL
0017  00-SUPPLIED
0018  01-V1-CANDIDATE
0019  02-V2-GRAPH
```

## Commands

Run preflight before starting a paid or write-capable Cursor Agent run:

```powershell
py -3 TOOLING/cursor_runner/run_cursor_eval.py preflight --run-id 0016 --model-id <cursor-model-id>
```

Run one planned arm:

```powershell
py -3 TOOLING/cursor_runner/run_cursor_eval.py run --run-id 0016 --model-id <cursor-model-id>
```

Run the remaining planned block in order:

```powershell
py -3 TOOLING/cursor_runner/run_cursor_eval.py run-block --model-id <cursor-model-id>
```

Prepare a workspace without launching Cursor:

```powershell
py -3 TOOLING/cursor_runner/run_cursor_eval.py prepare --run-id 0016 --model-id <cursor-model-id>
```

Preserve an already prepared workspace:

```powershell
py -3 TOOLING/cursor_runner/run_cursor_eval.py preserve --run-id 0016 --workspace .worktrees/cursor-runs/run-0016
```

## CLI Setup

Official Cursor Agent CLI install command for Windows PowerShell:

```powershell
irm 'https://cursor.com/install?win32=true' | iex
```

After install, verify:

```powershell
agent --version
agent status
agent --list-models
```

If a fresh shell still cannot resolve `agent`, the runner also checks the standard `%LOCALAPPDATA%\cursor-agent` install directory directly.

The run matrix intentionally leaves `default_model.cursor_model_id` blank until `agent --list-models` confirms the exact Cursor model ID for `Grok 4.6 High`.

## Evidence Rules

The runner must fail closed when:

- `agent` is missing;
- model ID is blank;
- `agent --list-models` fails because Cursor is not authenticated;
- the requested model ID is not reported by `agent --list-models`;
- `EVIDENCE/<run-id>` already exists;
- a matching archive already exists;
- the planned run ID is missing from the matrix;
- current lab verification fails before launch.

The runner preserves state before cleanup. It does not treat transcript-only verification claims as independent successful command evidence.
