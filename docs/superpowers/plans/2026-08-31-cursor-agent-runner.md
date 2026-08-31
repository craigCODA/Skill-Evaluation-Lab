# Cursor Agent Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build fail-closed tooling that can run planned Skill Evaluation Lab arms through the official Cursor Agent CLI and preserve evidence automatically.

**Architecture:** A Python runner owns the lab-side workflow: load planned run metadata, prepare an isolated ShingleFile workspace, install the correct project skill for skill arms, launch `agent`, and preserve all evidence before cleanup. The existing verifier is generalized so the lab can grow past `0015` and across multiple experiments without breaking its current public snapshot checks.

**Tech Stack:** Python standard library, PowerShell entry commands, Git CLI, Cursor Agent CLI (`agent`), existing Markdown/JSON lab metadata.

**Spec:** `docs/superpowers/specs/2026-08-31-cursor-agent-runner-design.md`

## Global Constraints

- Current public preserved record is `0001` through `0015`; next public run is `0016`.
- `02-V2-GRAPH` remains experimental and must not be promoted by this tooling.
- No skill artifact edits are part of this work.
- The runner must fail closed when `agent` is missing, the Cursor model ID is unresolved, or a run ID is already preserved.
- The runner must preserve evidence before cleanup and must not overwrite existing evidence or archive assets.
- Transcript/trace output supports process claims; command output supports verification claims only at the level actually captured.
- Planned EXP-0002 arm order is `0016` no skill, `0017` supplied original, `0018` V1, `0019` V2.

---

### Task 1: Runner Plan And Configuration

**Files:**
- Create: `docs/superpowers/specs/2026-08-31-cursor-agent-runner-design.md`
- Create: `docs/superpowers/plans/2026-08-31-cursor-agent-runner.md`
- Create: `TOOLING/cursor-runner/runs/EXP-0002-task02-quick-calculator-clear-label.json`
- Create: `TOOLING/cursor-runner/README.md`

**Interfaces:**
- Consumes: Existing experiment docs under `EXPERIMENTS/EXP-0002-task02-quick-calculator-clear-label/`
- Produces: JSON run matrix consumed by `TOOLING/cursor_runner/run_cursor_eval.py`

- [ ] **Step 1: Add the EXP-0002 run matrix**

Create `TOOLING/cursor-runner/runs/EXP-0002-task02-quick-calculator-clear-label.json`:

```json
{
  "experiment": "EXP-0002-task02-quick-calculator-clear-label",
  "skill": "layered-codebase-architecture",
  "prompt_file": "EXPERIMENTS/EXP-0002-task02-quick-calculator-clear-label/PROMPT.txt",
  "baseline": {
    "repo_name": "ShingleFile-main",
    "commit": "cd393ddd60548823dabd6875060247693a22c1be",
    "source": "D:/Downloads/ShingleFile-original-workplace/ShingleFile-original-workplace/MOTHER/ShingleFile-main.git"
  },
  "default_model": {
    "label": "Grok 4.6 High",
    "cursor_model_id": ""
  },
  "runs": [
    {
      "run_id": "0016",
      "skill_version": "NO-SKILL",
      "condition": "no explicit architecture skill",
      "evidence_class": "primary",
      "slash_invocation": false
    },
    {
      "run_id": "0017",
      "skill_version": "00-SUPPLIED",
      "condition": "supplied original, forced",
      "evidence_class": "primary",
      "slash_invocation": true
    },
    {
      "run_id": "0018",
      "skill_version": "01-V1-CANDIDATE",
      "condition": "V1, forced",
      "evidence_class": "primary",
      "slash_invocation": true
    },
    {
      "run_id": "0019",
      "skill_version": "02-V2-GRAPH",
      "condition": "V2, forced",
      "evidence_class": "primary",
      "slash_invocation": true
    }
  ]
}
```

- [ ] **Step 2: Add operator docs**

Document these commands in `TOOLING/cursor-runner/README.md`:

```powershell
py -3 TOOLING/cursor_runner/run_cursor_eval.py preflight --run-id 0016 --model-id <cursor-model-id>
py -3 TOOLING/cursor_runner/run_cursor_eval.py run --run-id 0016 --model-id <cursor-model-id>
py -3 TOOLING/cursor_runner/run_cursor_eval.py run-block --model-id <cursor-model-id>
```

- [ ] **Step 3: Verify no code behavior changed**

Run:

```powershell
git diff -- docs/superpowers TOOLING/cursor-runner
```

Expected: only documentation and JSON run-matrix additions.

- [ ] **Step 4: Commit Task 1**

Run:

```powershell
git add docs/superpowers/specs/2026-08-31-cursor-agent-runner-design.md docs/superpowers/plans/2026-08-31-cursor-agent-runner.md TOOLING/cursor-runner
git commit -m "docs: plan cursor agent runner"
```

### Task 2: Runner Unit Tests

**Files:**
- Create: `TOOLING/tests/test_cursor_runner.py`
- Create: `TOOLING/tests/test_verify_lab.py`

**Interfaces:**
- Consumes: Future `TOOLING/cursor_runner/run_cursor_eval.py`
- Produces: Regression coverage for prompt construction, workspace preparation, preservation, and verifier behavior.

- [ ] **Step 1: Write tests before production code**

Create tests that assert:

```python
def test_prompt_for_no_skill_does_not_include_slash_invocation(): ...
def test_prompt_for_skill_arm_includes_exact_slash_invocation(): ...
def test_prepare_workspace_copies_skill_only_for_skill_arm(): ...
def test_preserve_run_archives_untracked_files_and_refuses_overwrite(): ...
def test_verify_lab_accepts_multi_experiment_run_indexes(): ...
```

- [ ] **Step 2: Run tests and watch them fail**

Run:

```powershell
py -3 -m unittest discover -s TOOLING/tests -v
```

Expected: import errors because `TOOLING.cursor_runner.run_cursor_eval` does not exist yet.

- [ ] **Step 3: Commit Task 2**

Run only after the failing test output is captured in the terminal:

```powershell
git add TOOLING/tests
git commit -m "test: specify cursor runner behavior"
```

### Task 3: Cursor Runner Implementation

**Files:**
- Create: `TOOLING/cursor_runner/__init__.py`
- Create: `TOOLING/cursor_runner/run_cursor_eval.py`

**Interfaces:**
- Consumes:
  - `load_config(config_path: Path) -> LabRunConfig`
  - `build_prompt(config: LabRunConfig, run: LabRun) -> str`
  - `prepare_workspace(root: Path, config: LabRunConfig, run: LabRun, model_id: str) -> Path`
  - `preserve_run(root: Path, config: LabRunConfig, run: LabRun, workspace: Path, execution: ExecutionRecord) -> Path`
- Produces:
  - CLI commands `preflight`, `prepare`, `run`, `preserve`, and `run-block`

- [ ] **Step 1: Implement dataclasses and config loading**

Add dataclasses for:

```python
@dataclass(frozen=True)
class Baseline:
    repo_name: str
    commit: str
    source: str

@dataclass(frozen=True)
class LabRun:
    run_id: str
    skill_version: str
    condition: str
    evidence_class: str
    slash_invocation: bool

@dataclass(frozen=True)
class LabRunConfig:
    experiment: str
    skill: str
    prompt_file: str
    baseline: Baseline
    default_model_label: str
    default_cursor_model_id: str
    runs: tuple[LabRun, ...]
```

- [ ] **Step 2: Implement preflight**

`preflight` must check:

```text
agent exists on PATH
model ID is non-empty
baseline source exists when it is a local path
EVIDENCE/<run_id> does not exist
ARCHIVES/local/run-<run_id>-*.zip does not exist
py -3 TOOLING/verification/verify_lab.py exits 0
```

- [ ] **Step 3: Implement workspace preparation**

`prepare_workspace` must:

```text
create .worktrees/cursor-runs/run-XXXX
clone baseline source into that directory
checkout the pinned baseline commit
disable push URL
write LAB-RUN-METADATA.json
copy SKILL.md and conventions.md into .cursor/skills/layered-codebase-architecture for skill arms
skip project-skill install for NO-SKILL
write .cursor/cli.json with deny rules for destructive cleanup and push commands
```

- [ ] **Step 4: Implement execution**

`run` must invoke:

```powershell
agent -p --force --trust --workspace <workspace> --model <model-id> --output-format stream-json --stream-partial-output <prompt>
```

It must capture stdout to `.lab-run/cursor-agent-stream.raw.jsonl`, stderr to `.lab-run/cursor-agent-stderr.txt`, and exit metadata to `.lab-run/execution.json`.

- [ ] **Step 5: Implement preservation**

`preserve_run` must:

```text
create EVIDENCE/<run_id>
copy raw stream JSONL, stderr, execution metadata, and LAB-RUN-METADATA.json
write head/status/ignored/diff/stat/name-status/untracked evidence files
render a readable transcript Markdown file from JSONL best-effort
create ARCHIVES/local/run-<run_id>-<slug>.zip from the workspace
verify zip.testzip() returns None and the archive is non-empty
write RUN.md, RAW-RUN-RECORD.md, RESULT-ASSET.md, HASHES.txt
append DATA/runs.json
update the matching EXP-0002 RUN-INDEX row from planned to preserved
update CURRENT-STATE.md completed/next run values
remove the workspace only after archive verification succeeds
```

- [ ] **Step 6: Run tests**

Run:

```powershell
py -3 -m unittest discover -s TOOLING/tests -v
```

Expected: all runner tests pass.

- [ ] **Step 7: Commit Task 3**

Run:

```powershell
git add TOOLING/cursor_runner TOOLING/tests TOOLING/cursor-runner DATA/runs.json CURRENT-STATE.md EXPERIMENTS
git commit -m "feat: add cursor agent evaluation runner"
```

### Task 4: Verification Generalization

**Files:**
- Modify: `TOOLING/verification/verify_lab.py`
- Modify: `TOOLING/verification/README.md`

**Interfaces:**
- Consumes: Existing `DATA/runs.json`, all `EVIDENCE/<run>`, and every `EXPERIMENTS/*/RUN-INDEX.md`
- Produces: A verifier that validates current preserved runs and recognizes planned future experiment rows without hard-coding final run `0015`.

- [ ] **Step 1: Refactor run-index validation**

Replace the single EXP-0001 run-index check with a function that reads every `EXPERIMENTS/*/RUN-INDEX.md`, extracts rows whose status is not `planned`, and compares preserved IDs to `DATA/runs.json`.

- [ ] **Step 2: Replace hard-coded final run**

Read `Current completed global run:` from `CURRENT-STATE.md` and validate that it matches the highest preserved `EVIDENCE/<run>` directory.

- [ ] **Step 3: Keep release JSON snapshot behavior**

When `--release-json` is supplied for `evidence-0001-0015`, compare release assets only for rows whose `release_tag` is `evidence-0001-0015`.

- [ ] **Step 4: Run verifier tests**

Run:

```powershell
py -3 -m unittest discover -s TOOLING/tests -v
```

Expected: all tests pass.

- [ ] **Step 5: Run current lab verification**

Run:

```powershell
py -3 TOOLING/verification/verify_lab.py
```

Expected: `OK: verified 15 canonical runs through 0015`.

- [ ] **Step 6: Commit Task 4**

Run:

```powershell
git add TOOLING/verification TOOLING/tests
git commit -m "test: generalize lab verification"
```

### Task 5: CLI Bootstrap Check And Final Verification

**Files:**
- Modify: `TOOLING/cursor-runner/README.md`

**Interfaces:**
- Consumes: Local machine state for `agent`
- Produces: Clear run-readiness state without hiding missing auth/model prerequisites.

- [ ] **Step 1: Check local Cursor Agent CLI**

Run:

```powershell
Get-Command agent -ErrorAction SilentlyContinue
agent --version
agent status
agent --list-models
```

Expected: either concrete CLI/model output or a documented setup blocker.

- [ ] **Step 2: Update README with observed setup status**

If `agent` is missing, record the official install command:

```powershell
irm 'https://cursor.com/install?win32=true' | iex
```

If `agent` exists but auth or model selection is missing, record the exact next command to run after login.

- [ ] **Step 3: Run all verification**

Run:

```powershell
py -3 -m unittest discover -s TOOLING/tests -v
py -3 TOOLING/verification/verify_lab.py
```

Expected: tests pass and current lab verification passes.

- [ ] **Step 4: Commit Task 5**

Run:

```powershell
git add TOOLING/cursor-runner/README.md
git commit -m "docs: document cursor agent runner setup"
```
