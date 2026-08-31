#!/usr/bin/env python3
"""Prepare, run, and preserve Cursor Agent CLI evaluation runs."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DEFAULT_CONFIG = ROOT / "TOOLING" / "cursor-runner" / "runs" / "EXP-0002-task02-quick-calculator-clear-label.json"
RUN_ID_RE = re.compile(r"^\d{4}$")


class RunnerError(RuntimeError):
    """Raised when a run cannot proceed without weakening evidence quality."""


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

    def get_run(self, run_id: str) -> LabRun:
        for run in self.runs:
            if run.run_id == run_id:
                return run
        raise RunnerError(f"run {run_id} is not in the configured run matrix")


@dataclass(frozen=True)
class ExecutionRecord:
    command: list[str]
    exit_code: int
    stdout_path: Path
    stderr_path: Path


def slug(value: str) -> str:
    text = "".join(c.lower() if c.isalnum() else "-" for c in value)
    text = re.sub(r"-+", "-", text).strip("-")
    if not text:
        raise RunnerError("value cannot be converted to a non-empty slug")
    return text


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(field)}:\s*`?([^`\n]+)`?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def run_cmd(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RunnerError(f"command failed ({completed.returncode}): {' '.join(cmd)}\n{detail}")
    return completed


def remove_tree(path: Path, ignore_errors: bool = False) -> None:
    if not path.exists():
        return

    def retry_with_write_permission(function, target: str, exc_info: object) -> None:
        try:
            os.chmod(target, stat.S_IREAD | stat.S_IWRITE)
            function(target)
        except Exception:
            if not ignore_errors:
                raise

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, ignore_errors=ignore_errors, onexc=retry_with_write_permission)
    else:
        shutil.rmtree(path, ignore_errors=ignore_errors, onerror=retry_with_write_permission)


def load_config(path: Path = DEFAULT_CONFIG) -> LabRunConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    baseline = Baseline(
        repo_name=str(data["baseline"]["repo_name"]),
        commit=str(data["baseline"]["commit"]),
        source=str(data["baseline"]["source"]),
    )
    runs = tuple(
        LabRun(
            run_id=str(item["run_id"]),
            skill_version=str(item["skill_version"]),
            condition=str(item["condition"]),
            evidence_class=str(item["evidence_class"]),
            slash_invocation=bool(item["slash_invocation"]),
        )
        for item in data["runs"]
    )
    for run in runs:
        if not RUN_ID_RE.match(run.run_id):
            raise RunnerError(f"invalid run ID in config: {run.run_id}")
    return LabRunConfig(
        experiment=str(data["experiment"]),
        skill=str(data["skill"]),
        prompt_file=str(data["prompt_file"]),
        baseline=baseline,
        default_model_label=str(data["default_model"]["label"]),
        default_cursor_model_id=str(data["default_model"].get("cursor_model_id", "")),
        runs=runs,
    )


def resolved_model_id(config: LabRunConfig, model_id: str | None) -> str:
    value = (model_id or config.default_cursor_model_id or "").strip()
    if not value:
        raise RunnerError("Cursor model ID is required; run agent --list-models and pass --model-id")
    return value


def build_prompt(root: Path, config: LabRunConfig, run: LabRun) -> str:
    body = (root / config.prompt_file).read_text(encoding="utf-8").strip()
    if run.slash_invocation:
        return f"/{config.skill}  {body}"
    return body


def local_path_exists_or_url(source: str) -> bool:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", source):
        return True
    return Path(source).exists()


def evidence_path(root: Path, run: LabRun) -> Path:
    return root / "EVIDENCE" / run.run_id


def archive_glob(root: Path, run: LabRun) -> list[Path]:
    return sorted((root / "ARCHIVES" / "local").glob(f"run-{run.run_id}-*.zip"))


def workspace_path(root: Path, run: LabRun) -> Path:
    return root / ".worktrees" / "cursor-runs" / f"run-{run.run_id}"


def skill_source_path(root: Path, config: LabRunConfig, run: LabRun) -> Path:
    return root / "SKILLS" / config.skill / run.skill_version


def skill_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in ("SKILL.md", "conventions.md"):
        file_path = path / name
        if file_path.exists():
            hashes[name] = sha256_file(file_path)
    return hashes


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_project_cli_config(workspace: Path) -> None:
    cursor_dir = workspace / ".cursor"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        cursor_dir / "cli.json",
        {
            "permissions": {
                "allow": ["Read(*)", "Write(*)", "Edit(*)", "Shell(*)"],
                "deny": [
                    "Shell(git push*)",
                    "Shell(git reset --hard*)",
                    "Shell(git clean*)",
                    "Shell(Remove-Item -Recurse*)",
                    "Shell(del /s*)",
                ],
            }
        },
    )


def write_lab_metadata(root: Path, config: LabRunConfig, run: LabRun, workspace: Path, model_id: str) -> dict[str, object]:
    prompt_path = root / config.prompt_file
    metadata: dict[str, object] = {
        "run_id": run.run_id,
        "experiment": config.experiment,
        "skill": config.skill,
        "skill_version": run.skill_version,
        "condition": run.condition,
        "evidence_class": run.evidence_class,
        "slash_invocation": run.slash_invocation,
        "model_label": config.default_model_label,
        "cursor_model_id": model_id,
        "baseline": {
            "repo_name": config.baseline.repo_name,
            "commit": config.baseline.commit,
            "source": config.baseline.source,
        },
        "prompt_file": config.prompt_file,
        "prompt_sha256": sha256_file(prompt_path),
        "prepared_at_utc": utc_now(),
    }
    if run.skill_version != "NO-SKILL":
        source = skill_source_path(root, config, run)
        metadata["skill_artifact_path"] = str(source.relative_to(root).as_posix())
        metadata["skill_hashes"] = skill_hashes(source)
    write_json(workspace / ".lab-run" / "LAB-RUN-METADATA.json", metadata)
    return metadata


def prepare_workspace(root: Path, config: LabRunConfig, run: LabRun, model_id: str) -> Path:
    if evidence_path(root, run).exists():
        raise RunnerError(f"evidence already exists for run {run.run_id}")
    target = workspace_path(root, run)
    if target.exists():
        raise RunnerError(f"workspace already exists: {target}")
    if not local_path_exists_or_url(config.baseline.source):
        raise RunnerError(f"baseline source is missing: {config.baseline.source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    run_cmd(["git", "clone", "--quiet", config.baseline.source, str(target)])
    try:
        run_cmd(["git", "checkout", "--detach", config.baseline.commit], cwd=target)
        run_cmd(["git", "remote", "set-url", "--push", "origin", "LAB-RUN-PUSH-DISABLED"], cwd=target, check=False)
        write_project_cli_config(target)
        if run.skill_version != "NO-SKILL":
            source = skill_source_path(root, config, run)
            if not source.exists():
                raise RunnerError(f"skill artifact not found: {source}")
            destination = target / ".cursor" / "skills" / config.skill
            if destination.exists():
                remove_tree(destination)
            shutil.copytree(source, destination)
        write_lab_metadata(root, config, run, target, model_id)
    except Exception:
        if target.exists():
            remove_tree(target, ignore_errors=True)
        raise
    return target


def find_agent() -> str | None:
    return shutil.which("agent") or shutil.which("agent.cmd") or shutil.which("cursor-agent") or shutil.which("cursor-agent.cmd")


def preflight(root: Path, config: LabRunConfig, run: LabRun, model_id: str | None, require_agent: bool = True) -> list[str]:
    messages: list[str] = []
    resolved_model_id(config, model_id)
    if require_agent:
        agent = find_agent()
        if not agent:
            raise RunnerError("Cursor Agent CLI executable 'agent' is missing")
        messages.append(f"agent: {agent}")
    if not local_path_exists_or_url(config.baseline.source):
        raise RunnerError(f"baseline source is missing: {config.baseline.source}")
    if evidence_path(root, run).exists():
        raise RunnerError(f"evidence already exists for run {run.run_id}: {evidence_path(root, run)}")
    existing_archives = archive_glob(root, run)
    if existing_archives:
        raise RunnerError(f"archive already exists for run {run.run_id}: {existing_archives[0]}")

    from TOOLING.verification import verify_lab

    errors = verify_lab.verify(root, release_json_path=None)
    if errors:
        raise RunnerError("lab verification failed before run:\n" + "\n".join(errors))
    messages.append("lab verification: OK")
    messages.append(f"run {run.run_id}: preflight OK")
    return messages


def execute_agent(root: Path, config: LabRunConfig, run: LabRun, workspace: Path, model_id: str) -> ExecutionRecord:
    lab_run = workspace / ".lab-run"
    lab_run.mkdir(parents=True, exist_ok=True)
    stdout_path = lab_run / "cursor-agent-stream.raw.jsonl"
    stderr_path = lab_run / "cursor-agent-stderr.txt"
    prompt = build_prompt(root, config, run)
    command = [
        "agent",
        "-p",
        "--force",
        "--trust",
        "--workspace",
        str(workspace),
        "--model",
        model_id,
        "--output-format",
        "stream-json",
        "--stream-partial-output",
        prompt,
    ]
    started = utc_now()
    with stdout_path.open("w", encoding="utf-8", newline="\n") as stdout, stderr_path.open(
        "w", encoding="utf-8", newline="\n"
    ) as stderr:
        completed = subprocess.run(command, cwd=str(workspace), text=True, stdout=stdout, stderr=stderr)
    record = ExecutionRecord(command=command, exit_code=completed.returncode, stdout_path=stdout_path, stderr_path=stderr_path)
    write_json(
        lab_run / "execution.json",
        {
            "started_at_utc": started,
            "completed_at_utc": utc_now(),
            "exit_code": completed.returncode,
            "command": command,
        },
    )
    return record


def git_output(workspace: Path, args: list[str]) -> str:
    return run_cmd(["git", *args], cwd=workspace, check=False).stdout


def list_untracked(workspace: Path) -> str:
    lines = []
    for line in git_output(workspace, ["status", "--porcelain=v1", "-uall"]).splitlines():
        if line.startswith("?? "):
            lines.append(line[3:])
    return "\n".join(lines) + ("\n" if lines else "")


def render_stream_json(path: Path) -> str:
    lines = ["# Cursor Agent Stream", ""]
    if not path.exists():
        lines += ["Raw stream file was not found.", ""]
        return "\n".join(lines)
    for index, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            lines += [f"## {index}. raw", "", raw, ""]
            continue
        item_type = item.get("type") or item.get("role") or "record"
        lines += [f"## {index}. {item_type}", ""]
        text = extract_text(item)
        if text:
            lines += [text.strip(), ""]
        else:
            lines += ["```json", json.dumps(item, indent=2), "```", ""]
    return "\n".join(lines)


def extract_text(item: dict[str, object]) -> str:
    if isinstance(item.get("result"), str):
        return str(item["result"])
    message = item.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, list):
            parts = []
            for entry in content:
                if isinstance(entry, dict) and isinstance(entry.get("text"), str):
                    parts.append(entry["text"])
            return "\n".join(parts)
    if isinstance(item.get("text"), str):
        return str(item["text"])
    return ""


def zip_workspace(workspace: Path, archive: Path) -> tuple[int, int]:
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        raise RunnerError(f"archive already exists: {archive}")
    count = 0
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in workspace.rglob("*"):
            if path.is_file():
                zf.write(path, (Path(workspace.name) / path.relative_to(workspace)).as_posix())
                count += 1
    with zipfile.ZipFile(archive, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise RunnerError(f"archive verification failed at {bad}")
        if not zf.namelist():
            raise RunnerError("archive verification failed: empty ZIP")
    return count, archive.stat().st_size


def write_hashes(evidence: Path) -> None:
    lines = []
    for path in sorted(p for p in evidence.rglob("*") if p.is_file()):
        lines.append(f"{sha256_file(path)}  {path.relative_to(evidence).as_posix()}")
    (evidence / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def append_data_run(root: Path, config: LabRunConfig, run: LabRun, asset_name: str, asset_hash: str, experiment_run_path: Path) -> None:
    data_path = root / "DATA" / "runs.json"
    data = json.loads(data_path.read_text(encoding="utf-8")) if data_path.exists() else []
    if any(str(item.get("run_id")) == run.run_id for item in data):
        raise RunnerError(f"DATA/runs.json already contains run {run.run_id}")
    data.append(
        {
            "run_id": run.run_id,
            "model": config.default_model_label,
            "skill": config.skill,
            "skill_version": run.skill_version,
            "experiment": config.experiment,
            "evidence_class": run.evidence_class,
            "condition": run.condition,
            "baseline_commit": config.baseline.commit,
            "evidence_path": f"EVIDENCE/{run.run_id}",
            "experiment_run_path": experiment_run_path.relative_to(root).as_posix(),
            "result_asset": asset_name,
            "result_asset_sha256": asset_hash,
            "release_tag": "local-unreleased",
            "status": "preserved",
        }
    )
    data.sort(key=lambda item: str(item["run_id"]))
    write_json(data_path, data)


def update_run_index(root: Path, config: LabRunConfig, run: LabRun) -> None:
    index = root / "EXPERIMENTS" / config.experiment / "RUN-INDEX.md"
    if not index.exists():
        return
    text = index.read_text(encoding="utf-8")
    pattern = re.compile(rf"(\|\s*`?{re.escape(run.run_id)}`?\s*\|[^\n]*\|\s*)planned(\s*\|)", re.IGNORECASE)
    updated, count = pattern.subn(r"\1preserved\2", text, count=1)
    if count:
        index.write_text(updated, encoding="utf-8", newline="\n")


def update_current_state(root: Path, run: LabRun) -> None:
    path = root / "CURRENT-STATE.md"
    if not path.exists():
        return
    next_id = f"{int(run.run_id) + 1:04d}"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"Current completed global run:\s*`\d{4}`", f"Current completed global run: `{run.run_id}`", text)
    text = re.sub(r"Next global run:\s*`\d{4}`", f"Next global run: `{next_id}`", text)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_development_history(root: Path, config: LabRunConfig, run: LabRun) -> None:
    path = root / "DEVELOPMENT-HISTORY" / f"{run.run_id}.md"
    if path.exists():
        raise RunnerError(f"development history already exists for run {run.run_id}: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# {run.run_id}

## Condition

{config.default_model_label}, {run.condition}.

## What this record supports

Runner-preserved state and process evidence for `{config.experiment}`. This entry records preservation only; scoring and interpretation happen after evidence review.

## Historical rule

This entry records the interpretation retained at this point in the sequence. Later findings may supersede the conclusion without rewriting this record.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def write_run_notes(
    root: Path,
    config: LabRunConfig,
    run: LabRun,
    evidence: Path,
    archive: Path,
    archive_hash: str,
    execution: ExecutionRecord,
    experiment_run_path: Path,
) -> None:
    prompt_hash = sha256_file(root / config.prompt_file)
    skill_hash_text = "N/A"
    if run.skill_version != "NO-SKILL":
        hashes = skill_hashes(skill_source_path(root, config, run))
        skill_hash_text = ", ".join(f"{name}={digest}" for name, digest in sorted(hashes.items()))
    run_md = f"""# Run {run.run_id}

Skill: {config.skill}

Version: {run.skill_version}

Model: {config.default_model_label}

Experiment: {config.experiment}

Condition: {run.condition}

Evidence class: {run.evidence_class}

Baseline: {config.baseline.commit}

Prompt hash: {prompt_hash}

Skill hash: {skill_hash_text}

Harness: Cursor Agent CLI

Human intervention: none recorded by runner

Verification: Cursor Agent exit code {execution.exit_code}; see preserved command output and result state

Status: preserved
"""
    (evidence / "RUN.md").write_text(run_md, encoding="utf-8", newline="\n")
    result_md = f"""# Run {run.run_id} Result Asset

Asset: {archive.name}

Release tag: local-unreleased

SHA-256: {archive_hash}

Path: {archive.relative_to(root).as_posix()}
"""
    (evidence / "RESULT-ASSET.md").write_text(result_md, encoding="utf-8", newline="\n")
    raw_record = f"""# Run {run.run_id} Raw Record

Record only factual material here.

## Prompt

Prompt file: `{config.prompt_file}`

Prompt SHA-256: `{prompt_hash}`

## Harness

Model: {config.default_model_label}

Tool: Cursor Agent CLI

Visible settings: `agent -p --force --trust --output-format stream-json --stream-partial-output`

Date: {utc_now()}

Operator intervention: none recorded by runner

## Transcript

Path: `EVIDENCE/{run.run_id}/cursor-agent-stream.raw.jsonl`

Completeness: raw Cursor Agent CLI stream as captured from stdout

## Result State

Archive path: `{archive.relative_to(root).as_posix()}`

Archive SHA-256: `{archive_hash}`

Changed files: see `git-status.txt`, `git-diff-name-status.txt`, and `untracked-files.txt`

Verification actually run: Cursor Agent process exit code `{execution.exit_code}`; additional command evidence must be read from the preserved stream or stderr

## Caveats

The runner does not promote transcript-only verification claims to independent command evidence.
"""
    (evidence / "RAW-RUN-RECORD.md").write_text(raw_record, encoding="utf-8", newline="\n")
    experiment_run_path.mkdir(parents=True, exist_ok=True)
    (experiment_run_path / "RUN.md").write_text(run_md, encoding="utf-8", newline="\n")
    (experiment_run_path / "ANALYSIS.md").write_text(
        f"# Run {run.run_id} Analysis\n\nNot scored by the runner.\n",
        encoding="utf-8",
        newline="\n",
    )


def preserve_run(root: Path, config: LabRunConfig, run: LabRun, workspace: Path, execution: ExecutionRecord) -> Path:
    evidence = evidence_path(root, run)
    if evidence.exists():
        raise RunnerError(f"evidence already exists for run {run.run_id}: {evidence}")
    if not workspace.exists():
        raise RunnerError(f"workspace is missing: {workspace}")
    asset_name = f"run-{run.run_id}-{slug(run.condition)}.zip"
    archive = root / "ARCHIVES" / "local" / asset_name
    if archive.exists():
        raise RunnerError(f"archive already exists: {archive}")

    archive_count, archive_size = zip_workspace(workspace, archive)
    archive_hash = sha256_file(archive)
    experiment_run_path = root / "EXPERIMENTS" / config.experiment / "runs" / f"{run.run_id}-{slug(run.skill_version)}"

    evidence.mkdir(parents=True)
    (evidence / "head.txt").write_text(git_output(workspace, ["rev-parse", "HEAD"]), encoding="utf-8", newline="\n")
    (evidence / "git-status.txt").write_text(
        git_output(workspace, ["status", "--porcelain=v1", "-uall"]), encoding="utf-8", newline="\n"
    )
    (evidence / "git-status-ignored.txt").write_text(
        git_output(workspace, ["status", "--ignored", "--short"]), encoding="utf-8", newline="\n"
    )
    (evidence / "git-diff-stat.txt").write_text(git_output(workspace, ["diff", "--stat", "HEAD"]), encoding="utf-8", newline="\n")
    (evidence / "git-diff-name-status.txt").write_text(
        git_output(workspace, ["diff", "--name-status", "HEAD"]), encoding="utf-8", newline="\n"
    )
    (evidence / "diff.patch").write_text(git_output(workspace, ["diff", "--binary", "HEAD"]), encoding="utf-8", newline="\n")
    (evidence / "untracked-files.txt").write_text(list_untracked(workspace), encoding="utf-8", newline="\n")
    if execution.stdout_path.exists():
        shutil.copy2(execution.stdout_path, evidence / "cursor-agent-stream.raw.jsonl")
        (evidence / "cursor-agent-transcript.md").write_text(
            render_stream_json(execution.stdout_path), encoding="utf-8", newline="\n"
        )
    if execution.stderr_path.exists():
        shutil.copy2(execution.stderr_path, evidence / "cursor-agent-stderr.txt")
    metadata = workspace / ".lab-run" / "LAB-RUN-METADATA.json"
    if metadata.exists():
        shutil.copy2(metadata, evidence / "LAB-RUN-METADATA.json")
    execution_json = workspace / ".lab-run" / "execution.json"
    if execution_json.exists():
        shutil.copy2(execution_json, evidence / "execution.json")
    else:
        write_json(
            evidence / "execution.json",
            {
                "exit_code": execution.exit_code,
                "command": execution.command,
            },
        )
    write_json(
        evidence / "archive-manifest.json",
        {
            "run_id": run.run_id,
            "archive": archive.name,
            "archive_sha256": archive_hash,
            "archive_size_bytes": archive_size,
            "archive_entry_count": archive_count,
            "archive_testzip": "OK",
            "workspace": str(workspace),
            "preserved_at_utc": utc_now(),
        },
    )
    write_run_notes(root, config, run, evidence, archive, archive_hash, execution, experiment_run_path)
    write_hashes(evidence)
    append_data_run(root, config, run, archive.name, archive_hash, experiment_run_path)
    write_development_history(root, config, run)
    update_run_index(root, config, run)
    update_current_state(root, run)
    remove_tree(workspace)
    return evidence


def command_preflight(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    run = config.get_run(args.run_id)
    for message in preflight(root, config, run, args.model_id, require_agent=not args.no_agent_check):
        print(message)
    return 0


def command_prepare(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    run = config.get_run(args.run_id)
    model_id = resolved_model_id(config, args.model_id)
    preflight(root, config, run, model_id, require_agent=False)
    workspace = prepare_workspace(root, config, run, model_id)
    print(workspace)
    return 0


def command_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    run = config.get_run(args.run_id)
    model_id = resolved_model_id(config, args.model_id)
    preflight(root, config, run, model_id, require_agent=True)
    workspace = prepare_workspace(root, config, run, model_id)
    execution = execute_agent(root, config, run, workspace, model_id)
    evidence = preserve_run(root, config, run, workspace, execution)
    print(f"preserved {run.run_id}: {evidence}")
    return execution.exit_code


def command_preserve(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    run = config.get_run(args.run_id)
    workspace = Path(args.workspace).resolve()
    stdout_path = workspace / ".lab-run" / "cursor-agent-stream.raw.jsonl"
    stderr_path = workspace / ".lab-run" / "cursor-agent-stderr.txt"
    execution_json = workspace / ".lab-run" / "execution.json"
    command = ["agent"]
    exit_code = 0
    if execution_json.exists():
        data = json.loads(execution_json.read_text(encoding="utf-8"))
        command = [str(part) for part in data.get("command", command)]
        exit_code = int(data.get("exit_code", 0))
    evidence = preserve_run(root, config, run, workspace, ExecutionRecord(command, exit_code, stdout_path, stderr_path))
    print(f"preserved {run.run_id}: {evidence}")
    return 0


def command_run_block(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    model_id = resolved_model_id(config, args.model_id)
    for run in config.runs:
        if evidence_path(root, run).exists():
            continue
        preflight(root, config, run, model_id, require_agent=True)
        workspace = prepare_workspace(root, config, run, model_id)
        execution = execute_agent(root, config, run, workspace, model_id)
        evidence = preserve_run(root, config, run, workspace, execution)
        print(f"preserved {run.run_id}: {evidence}")
        if execution.exit_code != 0 and not args.continue_after_failure:
            return execution.exit_code
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run planned lab arms through Cursor Agent CLI")
    parser.add_argument("--root", default=str(ROOT), help="Skill Evaluation Lab root")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="run matrix JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--run-id", required=True)
    p.add_argument("--model-id")
    p.add_argument("--no-agent-check", action="store_true")
    p.set_defaults(func=command_preflight)

    p = sub.add_parser("prepare")
    p.add_argument("--run-id", required=True)
    p.add_argument("--model-id")
    p.set_defaults(func=command_prepare)

    p = sub.add_parser("run")
    p.add_argument("--run-id", required=True)
    p.add_argument("--model-id")
    p.set_defaults(func=command_run)

    p = sub.add_parser("preserve")
    p.add_argument("--run-id", required=True)
    p.add_argument("--workspace", required=True)
    p.set_defaults(func=command_preserve)

    p = sub.add_parser("run-block")
    p.add_argument("--model-id")
    p.add_argument("--continue-after-failure", action="store_true")
    p.set_defaults(func=command_run_block)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except RunnerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
