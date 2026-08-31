#!/usr/bin/env python3
"""Preserve-first workplace lifecycle for Skill Evaluation Lab runs."""

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


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "TOOLING" / "workplace" / "runs" / "EXP-0002-task02-quick-calculator-clear-label.json"
RUN_ID_RE = re.compile(r"^\d{4}$")
LOCAL_RELEASE_TAG = "local-unreleased"


class WorkplaceError(RuntimeError):
    """Raised when the lifecycle would weaken evidence integrity."""


@dataclass(frozen=True)
class Baseline:
    repo_name: str
    commit: str
    branch: str


@dataclass(frozen=True)
class LabRun:
    run_id: str
    model: str
    cursor_model_id: str
    skill_version: str
    condition: str
    evidence_class: str
    slash_invocation: bool


@dataclass(frozen=True)
class RunMatrix:
    experiment: str
    skill: str
    prompt_file: str
    baseline: Baseline
    runs: tuple[LabRun, ...]

    def get_run(self, run_id: str) -> LabRun:
        for run in self.runs:
            if run.run_id == run_id:
                return run
        raise WorkplaceError(f"run {run_id} is not in the run matrix")

    def remaining_from(self, run_id: str) -> list[LabRun]:
        return [run for run in self.runs if int(run.run_id) >= int(run_id)]


def run_cmd(cmd: list[object], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [str(part) for part in cmd],
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise WorkplaceError(f"command failed ({completed.returncode}): {' '.join(map(str, cmd))}\n{detail}")
    return completed


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def slug(value: str) -> str:
    text = "".join(c.lower() if c.isalnum() else "-" for c in value)
    text = re.sub(r"-+", "-", text).strip("-")
    if not text:
        raise WorkplaceError("label becomes empty after sanitizing")
    return text


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_path(path: str) -> str:
    return path.replace("\\", "/").rstrip("/")


def is_harness_path(path: str) -> bool:
    normalized = repo_path(path)
    return normalized == ".cursor" or normalized.startswith(".cursor/")


def status_line_paths(line: str) -> list[str]:
    if len(line) < 4:
        return []
    payload = repo_path(line[3:].strip())
    if " -> " in payload:
        return [repo_path(part.strip()) for part in payload.split(" -> ", 1)]
    return [payload]


def path_matches(path: str, excluded: set[str], include_harness: bool = True) -> bool:
    normalized = repo_path(path)
    if include_harness and is_harness_path(normalized):
        return True
    for excluded_path in excluded:
        if normalized == excluded_path or normalized.startswith(excluded_path + "/"):
            return True
    return False


def filter_status(status: str, excluded: set[str]) -> str:
    lines = []
    for line in status.splitlines():
        paths = status_line_paths(line)
        if paths and any(path_matches(path, excluded) for path in paths):
            continue
        lines.append(line)
    return "\n".join(lines) + ("\n" if lines else "")


def read_path_list(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {repo_path(line.strip()) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def harness_role(path: str) -> str:
    normalized = repo_path(path)
    if normalized == ".cursor/cli.json":
        return "cursor-cli-config"
    if normalized.startswith(".cursor/skills/"):
        return "treatment-skill"
    return "harness"


def collect_harness_manifest(root: Path, matrix: RunMatrix, run: LabRun) -> dict[str, object]:
    active = active_path(root, matrix)
    cursor_dir = active / ".cursor"
    files = []
    if cursor_dir.exists():
        for path in sorted(p for p in cursor_dir.rglob("*") if p.is_file()):
            relative = repo_path(path.relative_to(active).as_posix())
            files.append(
                {
                    "path": relative,
                    "role": harness_role(relative),
                    "sha256": sha256_file(path),
                    "size_bytes": path.stat().st_size,
                }
            )
    return {
        "schema_version": 1,
        "classification": "harness-created-state",
        "generated_at_utc": utc_now(),
        "run_id": run.run_id,
        "experiment": matrix.experiment,
        "skill": matrix.skill,
        "skill_version": run.skill_version,
        "files": files,
    }


def load_harness_paths(state: Path) -> set[str]:
    path = state / "harness-manifest.json"
    if not path.exists():
        return set()
    manifest = read_json(path)
    if not isinstance(manifest, dict):
        raise WorkplaceError("harness manifest must contain an object")
    files = manifest.get("files", [])
    if not isinstance(files, list):
        raise WorkplaceError("harness manifest files must contain a list")
    paths: set[str] = set()
    for item in files:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.add(repo_path(item["path"]))
    return paths


def parse_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(field)}:\s*`?([^`\n]+)`?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


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


def load_workplace(root: Path) -> dict[str, object]:
    path = root / "workplace.json"
    if not path.exists():
        raise WorkplaceError(f"missing workplace config: {path}")
    data = read_json(path)
    if not isinstance(data, dict):
        raise WorkplaceError("workplace.json must contain an object")
    return data


def configured_path(root: Path, key: str, default: str) -> Path:
    data = load_workplace(root)
    return root / str(data.get(key, default))


def mother_path(root: Path, matrix: RunMatrix | None = None) -> Path:
    repo_name = matrix.baseline.repo_name if matrix else str(load_workplace(root).get("repo_name", "ShingleFile-main"))
    return configured_path(root, "mother_path", f"MOTHER/{repo_name}.git")


def active_path(root: Path, matrix: RunMatrix | None = None) -> Path:
    repo_name = matrix.baseline.repo_name if matrix else str(load_workplace(root).get("repo_name", "ShingleFile-main"))
    return configured_path(root, "active_path", f"ACTIVE/{repo_name}")


def run_state_dir(root: Path) -> Path:
    return configured_path(root, "active_state_path", "ACTIVE/.run-state")


def evidence_path(root: Path, run: LabRun) -> Path:
    return root / "EVIDENCE" / run.run_id


def archive_path(root: Path, run: LabRun) -> Path:
    return root / "ARCHIVES" / "local" / f"run-{run.run_id}-{slug(run.condition)}.zip"


def skill_source_path(root: Path, matrix: RunMatrix, run: LabRun) -> Path:
    return root / "SKILLS" / matrix.skill / run.skill_version


def load_matrix(path: Path = DEFAULT_MATRIX) -> RunMatrix:
    data = read_json(path)
    if not isinstance(data, dict):
        raise WorkplaceError("run matrix must contain an object")
    baseline_data = data["baseline"]
    baseline = Baseline(
        repo_name=str(baseline_data["repo_name"]),
        commit=str(baseline_data["commit"]),
        branch=str(baseline_data.get("branch", "main")),
    )
    runs = tuple(
        LabRun(
            run_id=str(item["run_id"]),
            model=str(item["model"]),
            cursor_model_id=str(item["cursor_model_id"]),
            skill_version=str(item["skill_version"]),
            condition=str(item["condition"]),
            evidence_class=str(item["evidence_class"]),
            slash_invocation=bool(item["slash_invocation"]),
        )
        for item in data["runs"]
    )
    for run in runs:
        if not RUN_ID_RE.match(run.run_id):
            raise WorkplaceError(f"invalid run ID in matrix: {run.run_id}")
    return RunMatrix(
        experiment=str(data["experiment"]),
        skill=str(data["skill"]),
        prompt_file=str(data["prompt_file"]),
        baseline=baseline,
        runs=runs,
    )


def current_state_ids(root: Path) -> tuple[str | None, str]:
    path = root / "CURRENT-STATE.md"
    if not path.exists():
        raise WorkplaceError("missing CURRENT-STATE.md")
    text = path.read_text(encoding="utf-8")
    completed = parse_field(text, "Current completed global run")
    next_run = parse_field(text, "Next global run")
    if not next_run or not RUN_ID_RE.match(next_run):
        raise WorkplaceError("CURRENT-STATE.md has no valid Next global run")
    if completed and not RUN_ID_RE.match(completed):
        raise WorkplaceError("CURRENT-STATE.md has invalid Current completed global run")
    return completed, next_run


def ensure_next_global_run(root: Path, run: LabRun) -> None:
    _, next_run = current_state_ids(root)
    if run.run_id != next_run:
        raise WorkplaceError(f"Next global run is {next_run}; refusing requested run {run.run_id}")


def ensure_no_existing_canonical(root: Path, run: LabRun) -> None:
    evidence = evidence_path(root, run)
    archive = archive_path(root, run)
    if evidence.exists():
        raise WorkplaceError(f"evidence already exists for run {run.run_id}: {evidence}")
    if archive.exists():
        raise WorkplaceError(f"archive already exists for run {run.run_id}: {archive}")


def init_mother(root: Path, matrix: RunMatrix, source: str) -> Path:
    mother = mother_path(root, matrix)
    if mother.exists():
        raise WorkplaceError(f"Mother already exists; refusing overwrite: {mother}")
    mother.parent.mkdir(parents=True, exist_ok=True)
    run_cmd(["git", "clone", "--mirror", source, mother])
    actual = run_cmd(["git", "rev-parse", matrix.baseline.commit], cwd=mother).stdout.strip()
    if actual != matrix.baseline.commit:
        raise WorkplaceError(f"Mother missing baseline commit {matrix.baseline.commit}")
    return mother


def configure_active(active: Path, matrix: RunMatrix) -> None:
    branch = matrix.baseline.branch
    commit = matrix.baseline.commit
    checked = run_cmd(["git", "checkout", branch], cwd=active, check=False)
    if checked.returncode != 0:
        run_cmd(["git", "checkout", "-b", branch, commit], cwd=active)
    run_cmd(["git", "reset", "--hard", commit], cwd=active)
    run_cmd(["git", "remote", "set-url", "origin", f"../../MOTHER/{matrix.baseline.repo_name}.git"], cwd=active)
    run_cmd(["git", "remote", "set-url", "--push", "origin", "WORKPLACE-MOTHER-PUSH-DISABLED"], cwd=active, check=False)


def write_project_cli_config(active: Path) -> None:
    write_json(
        active / ".cursor" / "cli.json",
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


def skill_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for filename in ("SKILL.md", "conventions.md"):
        file_path = path / filename
        if file_path.exists():
            hashes[filename] = sha256_file(file_path)
    return hashes


def build_prompt(root: Path, matrix: RunMatrix, run: LabRun) -> str:
    body = (root / matrix.prompt_file).read_text(encoding="utf-8").strip()
    if run.slash_invocation:
        return f"/{matrix.skill}  {body}"
    return body


def run_metadata(root: Path, matrix: RunMatrix, run: LabRun) -> dict[str, object]:
    prompt_path = root / matrix.prompt_file
    metadata: dict[str, object] = {
        "run_id": run.run_id,
        "experiment": matrix.experiment,
        "skill": matrix.skill,
        "skill_version": run.skill_version,
        "condition": run.condition,
        "evidence_class": run.evidence_class,
        "model": run.model,
        "cursor_model_id": run.cursor_model_id,
        "slash_invocation": run.slash_invocation,
        "baseline": {
            "repo_name": matrix.baseline.repo_name,
            "commit": matrix.baseline.commit,
            "branch": matrix.baseline.branch,
        },
        "prompt_file": matrix.prompt_file,
        "prompt_sha256": sha256_file(prompt_path),
        "prepared_at_utc": utc_now(),
        "active_path": str(active_path(root, matrix)),
        "run_state_path": str(run_state_dir(root)),
    }
    if run.skill_version != "NO-SKILL":
        source = skill_source_path(root, matrix, run)
        metadata["skill_artifact_path"] = source.relative_to(root).as_posix()
        metadata["skill_hashes"] = skill_hashes(source)
    return metadata


def fresh(root: Path, matrix: RunMatrix, run: LabRun) -> Path:
    ensure_next_global_run(root, run)
    ensure_no_existing_canonical(root, run)
    mother = mother_path(root, matrix)
    active = active_path(root, matrix)
    state = run_state_dir(root)
    if not mother.exists():
        raise WorkplaceError(f"Mother not found: {mother}")
    if active.exists():
        raise WorkplaceError(f"Active still exists: {active}\nArchive it first. Fresh never deletes an open run.")
    if state.exists():
        raise WorkplaceError(f"run state still exists: {state}\nArchive the active run before starting another.")

    active.parent.mkdir(parents=True, exist_ok=True)
    run_cmd(["git", "clone", mother, active])
    try:
        configure_active(active, matrix)
        write_project_cli_config(active)
        if run.skill_version != "NO-SKILL":
            source = skill_source_path(root, matrix, run)
            if not source.exists():
                raise WorkplaceError(f"skill artifact not found: {source}")
            shutil.copytree(source, active / ".cursor" / "skills" / matrix.skill)
        state.mkdir(parents=True)
        write_json(state / "RUN-METADATA.json", run_metadata(root, matrix, run))
        capture_pre_execution_snapshot(root, matrix, run)
    except Exception:
        remove_tree(active, ignore_errors=True)
        remove_tree(state, ignore_errors=True)
        raise
    return active


def find_agent() -> str | None:
    for name in ("agent", "agent.cmd", "cursor-agent", "cursor-agent.cmd"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    bases = [os.environ.get("LOCALAPPDATA"), str(Path.home() / "AppData" / "Local")]
    for base in bases:
        if not base:
            continue
        install = Path(base) / "cursor-agent"
        for name in ("agent.cmd", "agent.exe", "cursor-agent.cmd", "cursor-agent.exe"):
            candidate = install / name
            if candidate.exists():
                return str(candidate)
    return None


def agent_probe(agent: str, args: list[str], timeout_seconds: int = 60) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [agent, *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorkplaceError(f"Cursor Agent CLI probe timed out: {agent} {' '.join(args)}") from exc


def validate_agent_model(agent: str, model_id: str) -> None:
    completed = agent_probe(agent, ["--list-models"])
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise WorkplaceError(
            "Cursor Agent CLI is not ready: model listing failed. "
            "Run agent login or set CURSOR_API_KEY/CURSOR_AUTH_TOKEN.\n"
            + detail
        )
    if model_id.lower() not in completed.stdout.lower():
        raise WorkplaceError(f"Cursor model ID {model_id!r} was not reported by agent --list-models")


def verify_canonical_state(root: Path) -> None:
    verifier = root / "TOOLING" / "verification" / "verify_lab.py"
    if not verifier.exists():
        return
    completed = run_cmd([sys.executable, verifier], cwd=root, check=False)
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise WorkplaceError(f"lab verifier failed before run\n{detail}")


def preflight(root: Path, matrix: RunMatrix, run: LabRun, require_agent: bool = True) -> list[str]:
    ensure_next_global_run(root, run)
    ensure_no_existing_canonical(root, run)
    verify_canonical_state(root)
    if not run.cursor_model_id:
        raise WorkplaceError(f"run {run.run_id} has no Cursor model ID")
    messages = []
    if not mother_path(root, matrix).exists():
        raise WorkplaceError(f"Mother not found: {mother_path(root, matrix)}")
    if active_path(root, matrix).exists() or run_state_dir(root).exists():
        raise WorkplaceError("Active run is already open; archive it before starting another")
    if require_agent:
        agent = find_agent()
        if not agent:
            raise WorkplaceError("Cursor Agent CLI executable 'agent' is missing")
        validate_agent_model(agent, run.cursor_model_id)
        messages.append(f"agent: {agent}")
    return messages + [f"run {run.run_id}: preflight OK"]


def execute_active(root: Path, matrix: RunMatrix, run: LabRun) -> dict[str, object]:
    active = active_path(root, matrix)
    if not active.exists():
        raise WorkplaceError(f"Active repo not found: {active}")
    validate_active_metadata(root, matrix, run)
    agent = find_agent()
    if not agent:
        raise WorkplaceError("Cursor Agent CLI executable 'agent' is missing")
    validate_agent_model(agent, run.cursor_model_id)

    state = run_state_dir(root)
    stdout_path = state / "cursor-agent-stream.raw.jsonl"
    stderr_path = state / "cursor-agent-stderr.txt"
    command = [
        agent,
        "-p",
        "--force",
        "--trust",
        "--workspace",
        str(active),
        "--model",
        run.cursor_model_id,
        "--output-format",
        "stream-json",
        "--stream-partial-output",
        build_prompt(root, matrix, run),
    ]
    started = utc_now()
    with stdout_path.open("w", encoding="utf-8", newline="\n") as stdout, stderr_path.open(
        "w", encoding="utf-8", newline="\n"
    ) as stderr:
        completed = subprocess.run(command, cwd=str(active), text=True, stdout=stdout, stderr=stderr)
    execution = {
        "run_id": run.run_id,
        "started_at_utc": started,
        "completed_at_utc": utc_now(),
        "exit_code": completed.returncode,
        "command": command,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
    }
    write_json(state / "execution.json", execution)
    return execution


def validate_active_metadata(root: Path, matrix: RunMatrix, run: LabRun) -> dict[str, object]:
    state = run_state_dir(root)
    metadata_path = state / "RUN-METADATA.json"
    if not metadata_path.exists():
        raise WorkplaceError(f"missing active run metadata: {metadata_path}")
    metadata = read_json(metadata_path)
    if not isinstance(metadata, dict):
        raise WorkplaceError("active run metadata must contain an object")
    expected = {
        "run_id": run.run_id,
        "experiment": matrix.experiment,
        "skill": matrix.skill,
        "skill_version": run.skill_version,
        "condition": run.condition,
        "evidence_class": run.evidence_class,
        "model": run.model,
        "cursor_model_id": run.cursor_model_id,
    }
    mismatches = []
    for key, value in expected.items():
        if metadata.get(key) != value:
            mismatches.append(f"{key}: {metadata.get(key)!r} != {value!r}")
    baseline = metadata.get("baseline")
    if not isinstance(baseline, dict) or baseline.get("commit") != matrix.baseline.commit:
        mismatches.append("baseline.commit")
    if mismatches:
        raise WorkplaceError("metadata mismatch: " + "; ".join(mismatches))
    return metadata


def load_execution(root: Path, run: LabRun, state_only: bool = False, reason: str | None = None) -> dict[str, object]:
    path = run_state_dir(root) / "execution.json"
    if not path.exists():
        if not state_only:
            raise WorkplaceError("execution.json is required before canonical archive; use --state-only with a reason for incomplete runs")
        if not reason:
            raise WorkplaceError("--state-only requires --reason")
        return {
            "run_id": run.run_id,
            "command": [],
            "exit_code": None,
            "state_only": True,
            "state_only_reason": reason,
            "completed_at_utc": utc_now(),
        }
    execution = read_json(path)
    if not isinstance(execution, dict):
        raise WorkplaceError("execution.json must contain an object")
    if execution.get("run_id") != run.run_id:
        raise WorkplaceError(f"execution metadata mismatch: {execution.get('run_id')!r} != {run.run_id!r}")
    return execution


def git_output(active: Path, args: list[str]) -> str:
    return run_cmd(["git", *args], cwd=active, check=False).stdout


def list_untracked(active: Path, excluded: set[str] | None = None, exclude_harness: bool = False) -> str:
    excluded = excluded or set()
    lines = []
    for line in git_output(active, ["status", "--porcelain=v1", "-uall"]).splitlines():
        if line.startswith("?? "):
            path = repo_path(line[3:])
            if not path_matches(path, excluded, include_harness=exclude_harness):
                lines.append(path)
    return "\n".join(lines) + ("\n" if lines else "")


def git_diff_from_baseline(active: Path, matrix: RunMatrix, args: list[str]) -> str:
    return git_output(active, ["diff", *args, matrix.baseline.commit, "--", ".", ":(exclude).cursor/**"])


def tracked_subject_files(active: Path, matrix: RunMatrix) -> str:
    paths = [repo_path(line) for line in git_diff_from_baseline(active, matrix, ["--name-only"]).splitlines() if line]
    return "\n".join(paths) + ("\n" if paths else "")


def capture_pre_execution_snapshot(root: Path, matrix: RunMatrix, run: LabRun) -> None:
    active = active_path(root, matrix)
    state = run_state_dir(root)
    write_json(state / "harness-manifest.json", collect_harness_manifest(root, matrix, run))
    (state / "pre-execution-head.txt").write_text(
        git_output(active, ["rev-parse", "HEAD"]), encoding="utf-8", newline="\n"
    )
    (state / "pre-execution-git-status.txt").write_text(
        git_output(active, ["status", "--porcelain=v1", "-uall"]), encoding="utf-8", newline="\n"
    )
    (state / "pre-execution-git-status-ignored.txt").write_text(
        git_output(active, ["status", "--ignored", "--short"]), encoding="utf-8", newline="\n"
    )
    (state / "pre-execution-untracked-files.txt").write_text(
        list_untracked(active), encoding="utf-8", newline="\n"
    )


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


def render_stream_json(path: Path) -> str:
    lines = ["# Cursor Agent Stream", ""]
    if not path.exists():
        return "\n".join(lines + ["Raw stream file was not found.", ""])
    for index, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            lines += [f"## {index}. raw", "", raw, ""]
            continue
        if not isinstance(item, dict):
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


def zip_active(active: Path, archive: Path) -> tuple[int, int]:
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        raise WorkplaceError(f"archive already exists: {archive}")
    count = 0
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in active.rglob("*"):
            if path.is_file():
                zf.write(path, (Path(active.name) / path.relative_to(active)).as_posix())
                count += 1
    with zipfile.ZipFile(archive, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise WorkplaceError(f"archive verification failed at {bad}")
        names = zf.namelist()
        if not names:
            raise WorkplaceError("archive verification failed: empty ZIP")
        if not any("/.git/" in f"/{name}" or name.endswith("/.git/HEAD") for name in names):
            raise WorkplaceError("archive verification failed: .git metadata missing")
    return count, archive.stat().st_size


def write_hashes(evidence: Path) -> None:
    lines = []
    for path in sorted(p for p in evidence.rglob("*") if p.is_file()):
        if path.name == "HASHES.txt":
            continue
        lines.append(f"{sha256_file(path)}  {path.relative_to(evidence).as_posix()}")
    (evidence / "HASHES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def experiment_run_path(root: Path, matrix: RunMatrix, run: LabRun) -> Path:
    return root / "EXPERIMENTS" / matrix.experiment / "runs" / f"{run.run_id}-{slug(run.skill_version)}"


def execution_exit_code(execution: dict[str, object]) -> str:
    value = execution.get("exit_code")
    return "state-only" if value is None else str(value)


def write_run_notes(
    root: Path,
    matrix: RunMatrix,
    run: LabRun,
    evidence: Path,
    archive: Path,
    archive_hash: str,
    execution: dict[str, object],
) -> None:
    prompt_hash = sha256_file(root / matrix.prompt_file)
    skill_hash_text = "N/A"
    if run.skill_version != "NO-SKILL":
        hashes = skill_hashes(skill_source_path(root, matrix, run))
        skill_hash_text = ", ".join(f"{name}={digest}" for name, digest in sorted(hashes.items()))
    run_md = f"""# Run {run.run_id}

Skill: {matrix.skill}

Version: {run.skill_version}

Model: {run.model}

Experiment: {matrix.experiment}

Condition: {run.condition}

Evidence class: {run.evidence_class}

Baseline: {matrix.baseline.commit}

Prompt hash: {prompt_hash}

Skill hash: {skill_hash_text}

Harness: Cursor Agent CLI via workplace lifecycle

Human intervention: none recorded by runner

Verification: Cursor Agent exit code {execution_exit_code(execution)}; see preserved command output and result state

Status: preserved
"""
    (evidence / "RUN.md").write_text(run_md, encoding="utf-8", newline="\n")
    result_md = f"""# Run {run.run_id} Result Asset

Asset: {archive.name}

Storage class: local-only archive

Publication status: pending

Fresh-clone retrievable: no

Durable publication path: GitHub Release asset (pending)

Release tag: {LOCAL_RELEASE_TAG}

SHA-256: {archive_hash}

Path: {archive.relative_to(root).as_posix()}

Manifest: EVIDENCE/{run.run_id}/archive-manifest.json
"""
    (evidence / "RESULT-ASSET.md").write_text(result_md, encoding="utf-8", newline="\n")
    raw_record = f"""# Run {run.run_id} Raw Record

Record only factual material here.

## Prompt

Prompt file: `{matrix.prompt_file}`

Prompt SHA-256: `{prompt_hash}`

## Harness

Model: {run.model}

Tool: Cursor Agent CLI

Visible settings: `agent -p --force --trust --output-format stream-json --stream-partial-output`

Date: {utc_now()}

Operator intervention: none recorded by runner

## Transcript

Path: `EVIDENCE/{run.run_id}/cursor-agent-stream.raw.jsonl`

Completeness: raw Cursor Agent CLI stream as captured outside the active subject repository

## Result State

Archive path: `{archive.relative_to(root).as_posix()}`

Archive SHA-256: `{archive_hash}`

Archive storage: local-only; not retrievable from a fresh clone until published as a durable external asset

Baseline commit for tracked change evidence: `{matrix.baseline.commit}`

Final HEAD: see `final-head.txt`

Harness attribution: see `harness-manifest.json`, `pre-execution-untracked-files.txt`, and `git-status-full.txt`

Model-created files: see `model-created-git-status.txt`, `tracked-subject-files.txt`, and `model-created-untracked-files.txt`

Tracked subject-repository changes: see `git-diff-name-status.txt` and `diff.patch`; generated against the frozen matrix baseline, not final HEAD

Verification actually run: Cursor Agent process exit code `{execution_exit_code(execution)}`; additional command evidence must be read from the preserved stream or stderr

## Caveats

The lifecycle does not promote transcript-only verification claims to independent command evidence.
"""
    (evidence / "RAW-RUN-RECORD.md").write_text(raw_record, encoding="utf-8", newline="\n")
    run_path = experiment_run_path(root, matrix, run)
    run_path.mkdir(parents=True, exist_ok=True)
    (run_path / "RUN.md").write_text(run_md, encoding="utf-8", newline="\n")
    (run_path / "ANALYSIS.md").write_text(
        f"# Run {run.run_id} Analysis\n\nNot scored by the runner.\n",
        encoding="utf-8",
        newline="\n",
    )


def append_data_run(root: Path, matrix: RunMatrix, run: LabRun, archive: Path, archive_hash: str) -> None:
    data_path = root / "DATA" / "runs.json"
    data = read_json(data_path) if data_path.exists() else []
    if not isinstance(data, list):
        raise WorkplaceError("DATA/runs.json must contain a list")
    if any(str(item.get("run_id")) == run.run_id for item in data if isinstance(item, dict)):
        raise WorkplaceError(f"DATA/runs.json already contains run {run.run_id}")
    data.append(
        {
            "run_id": run.run_id,
            "model": run.model,
            "skill": matrix.skill,
            "skill_version": run.skill_version,
            "experiment": matrix.experiment,
            "evidence_class": run.evidence_class,
            "condition": run.condition,
            "baseline_commit": matrix.baseline.commit,
            "evidence_path": f"EVIDENCE/{run.run_id}",
            "experiment_run_path": experiment_run_path(root, matrix, run).relative_to(root).as_posix(),
            "result_asset": archive.name,
            "result_asset_sha256": archive_hash,
            "result_asset_storage": "local-only",
            "result_asset_publication_status": "pending",
            "result_asset_fresh_clone_retrievable": False,
            "durable_publication_path": "GitHub Release asset",
            "release_tag": LOCAL_RELEASE_TAG,
            "status": "preserved",
        }
    )
    data.sort(key=lambda item: str(item["run_id"]))
    write_json(data_path, data)


def update_run_index(root: Path, matrix: RunMatrix, run: LabRun) -> None:
    path = root / "EXPERIMENTS" / matrix.experiment / "RUN-INDEX.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(\|\s*`?{re.escape(run.run_id)}`?\s*\|[^\n]*\|\s*)planned(\s*\|)", re.IGNORECASE)
    updated, count = pattern.subn(r"\1preserved\2", text, count=1)
    if count != 1:
        raise WorkplaceError(f"RUN-INDEX row for {run.run_id} was not planned")
    path.write_text(updated, encoding="utf-8", newline="\n")


def update_current_state(root: Path, matrix: RunMatrix, run: LabRun) -> None:
    path = root / "CURRENT-STATE.md"
    text = path.read_text(encoding="utf-8")
    next_id = f"{int(run.run_id) + 1:04d}"
    text = re.sub(r"Current completed global run:\s*`\d{4}`", f"Current completed global run: `{run.run_id}`", text)
    text = re.sub(r"Next global run:\s*`\d{4}`", f"Next global run: `{next_id}`", text)
    text = re.sub(r"Current experiment:\s*`[^`]+`", f"Current experiment: `{matrix.experiment}`", text)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_development_history(root: Path, matrix: RunMatrix, run: LabRun) -> None:
    path = root / "DEVELOPMENT-HISTORY" / f"{run.run_id}.md"
    if path.exists():
        raise WorkplaceError(f"development history already exists for run {run.run_id}: {path}")
    text = f"""# {run.run_id}

## Condition

{run.model}, {run.condition}.

## What this record supports

Workplace-lifecycle-preserved state and process evidence for `{matrix.experiment}`. This entry records preservation only; scoring and interpretation happen after evidence review.

## Historical rule

This entry records the interpretation retained at this point in the sequence. Later findings may supersede the conclusion without rewriting this record.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def archive_active(root: Path, matrix: RunMatrix, run: LabRun, state_only: bool = False, reason: str | None = None) -> Path:
    ensure_next_global_run(root, run)
    ensure_no_existing_canonical(root, run)
    active = active_path(root, matrix)
    state = run_state_dir(root)
    if not active.exists():
        raise WorkplaceError(f"No Active repo found: {active}")
    if not state.exists():
        raise WorkplaceError(f"No active run state found: {state}")
    metadata = validate_active_metadata(root, matrix, run)
    execution = load_execution(root, run, state_only=state_only, reason=reason)
    pre_execution_files = (
        "harness-manifest.json",
        "pre-execution-head.txt",
        "pre-execution-git-status.txt",
        "pre-execution-git-status-ignored.txt",
        "pre-execution-untracked-files.txt",
    )
    missing_pre_execution = [name for name in pre_execution_files if not (state / name).exists()]
    if missing_pre_execution:
        raise WorkplaceError(f"missing pre-execution snapshot files: {', '.join(missing_pre_execution)}")

    archive = archive_path(root, run)
    entry_count, archive_size = zip_active(active, archive)
    archive_hash = sha256_file(archive)
    evidence = evidence_path(root, run)
    evidence.mkdir(parents=True)

    for filename in pre_execution_files:
        shutil.copy2(state / filename, evidence / filename)

    full_status = git_output(active, ["status", "--porcelain=v1", "-uall"])
    harness_paths = load_harness_paths(state)
    pre_execution_untracked = read_path_list(state / "pre-execution-untracked-files.txt")
    excluded_model_paths = harness_paths | pre_execution_untracked
    model_status = filter_status(full_status, excluded_model_paths)
    final_head = git_output(active, ["rev-parse", "HEAD"])

    (evidence / "head.txt").write_text(final_head, encoding="utf-8", newline="\n")
    (evidence / "final-head.txt").write_text(final_head, encoding="utf-8", newline="\n")
    (evidence / "baseline-head.txt").write_text(matrix.baseline.commit + "\n", encoding="utf-8", newline="\n")
    (evidence / "git-status-full.txt").write_text(full_status, encoding="utf-8", newline="\n")
    (evidence / "git-status.txt").write_text(model_status, encoding="utf-8", newline="\n")
    (evidence / "model-created-git-status.txt").write_text(model_status, encoding="utf-8", newline="\n")
    (evidence / "git-status-ignored.txt").write_text(git_output(active, ["status", "--ignored", "--short"]), encoding="utf-8", newline="\n")
    (evidence / "git-diff-stat.txt").write_text(git_diff_from_baseline(active, matrix, ["--stat"]), encoding="utf-8", newline="\n")
    (evidence / "git-diff-name-status.txt").write_text(
        git_diff_from_baseline(active, matrix, ["--name-status"]), encoding="utf-8", newline="\n"
    )
    (evidence / "diff.patch").write_text(git_diff_from_baseline(active, matrix, ["--binary"]), encoding="utf-8", newline="\n")
    (evidence / "tracked-subject-files.txt").write_text(tracked_subject_files(active, matrix), encoding="utf-8", newline="\n")
    (evidence / "untracked-files-full.txt").write_text(list_untracked(active), encoding="utf-8", newline="\n")
    (evidence / "untracked-files.txt").write_text(
        list_untracked(active, excluded_model_paths, exclude_harness=True), encoding="utf-8", newline="\n"
    )
    (evidence / "model-created-untracked-files.txt").write_text(
        list_untracked(active, excluded_model_paths, exclude_harness=True), encoding="utf-8", newline="\n"
    )
    write_json(evidence / "RUN-METADATA.json", metadata)
    write_json(evidence / "execution.json", execution)

    stream = state / "cursor-agent-stream.raw.jsonl"
    if stream.exists():
        shutil.copy2(stream, evidence / "cursor-agent-stream.raw.jsonl")
        (evidence / "cursor-agent-transcript.md").write_text(render_stream_json(stream), encoding="utf-8", newline="\n")
    stderr = state / "cursor-agent-stderr.txt"
    if stderr.exists():
        shutil.copy2(stderr, evidence / "cursor-agent-stderr.txt")
    write_json(
        evidence / "archive-manifest.json",
        {
            "run_id": run.run_id,
            "archive": archive.name,
            "archive_sha256": archive_hash,
            "archive_size_bytes": archive_size,
            "archive_entry_count": entry_count,
            "archive_testzip": "OK",
            "active": str(active),
            "run_state": str(state),
            "storage_class": "local-only",
            "publication_status": "pending",
            "fresh_clone_retrievable": False,
            "durable_publication_path": "GitHub Release asset",
            "preserved_at_utc": utc_now(),
        },
    )
    write_run_notes(root, matrix, run, evidence, archive, archive_hash, execution)
    write_hashes(evidence)
    append_data_run(root, matrix, run, archive, archive_hash)
    write_development_history(root, matrix, run)
    update_run_index(root, matrix, run)
    update_current_state(root, matrix, run)
    remove_tree(active)
    remove_tree(state)
    return evidence


def command_mother_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    mother = init_mother(root, matrix, args.source)
    print(f"Mother initialized: {mother}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    completed, next_run = current_state_ids(root)
    print(f"Workplace: {root}")
    print(f"Current completed global run: {completed}")
    print(f"Next global run: {next_run}")
    print(f"Mother exists: {mother_path(root, matrix).exists()}")
    active = active_path(root, matrix)
    print(f"Active exists: {active.exists()}")
    if active.exists():
        print(f"Active HEAD: {run_cmd(['git', 'rev-parse', 'HEAD'], cwd=active).stdout.strip()}")
        print(run_cmd(["git", "status", "--short", "--branch"], cwd=active).stdout.rstrip())
    return 0


def command_preflight(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    run = matrix.get_run(args.run_id)
    for message in preflight(root, matrix, run, require_agent=not args.no_agent_check):
        print(message)
    return 0


def command_fresh(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    run = matrix.get_run(args.run_id)
    active = fresh(root, matrix, run)
    print(f"Fresh Active clone created: {active}")
    print(f"HEAD: {run_cmd(['git', 'rev-parse', 'HEAD'], cwd=active).stdout.strip()}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    run = matrix.get_run(args.run_id)
    preflight(root, matrix, run, require_agent=True)
    fresh(root, matrix, run)
    execution = execute_active(root, matrix, run)
    evidence = archive_active(root, matrix, run)
    print(f"preserved {run.run_id}: {evidence}")
    return int(execution.get("exit_code") or 0)


def command_archive(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    run = matrix.get_run(args.run_id)
    evidence = archive_active(root, matrix, run, state_only=args.state_only, reason=args.reason)
    print(f"preserved {run.run_id}: {evidence}")
    return 0


def command_run_block(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    matrix = load_matrix(Path(args.matrix).resolve())
    _, next_run = current_state_ids(root)
    exit_code = 0
    for run in matrix.remaining_from(next_run):
        if evidence_path(root, run).exists():
            continue
        preflight(root, matrix, run, require_agent=True)
        fresh(root, matrix, run)
        execution = execute_active(root, matrix, run)
        evidence = archive_active(root, matrix, run)
        print(f"preserved {run.run_id}: {evidence}")
        exit_code = int(execution.get("exit_code") or 0)
        if exit_code != 0 and not args.continue_after_failure:
            return exit_code
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skill Evaluation Lab workplace lifecycle")
    parser.add_argument("--root", default=str(ROOT), help="lab root")
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX), help="run matrix JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("mother-init")
    p.add_argument("--source", required=True)
    p.set_defaults(func=command_mother_init)

    p = sub.add_parser("status")
    p.set_defaults(func=command_status)

    p = sub.add_parser("preflight")
    p.add_argument("--run-id", required=True)
    p.add_argument("--no-agent-check", action="store_true")
    p.set_defaults(func=command_preflight)

    p = sub.add_parser("fresh")
    p.add_argument("--run-id", required=True)
    p.set_defaults(func=command_fresh)

    p = sub.add_parser("run")
    p.add_argument("--run-id", required=True)
    p.set_defaults(func=command_run)

    p = sub.add_parser("archive")
    p.add_argument("--run-id", required=True)
    p.add_argument("--state-only", action="store_true")
    p.add_argument("--reason")
    p.set_defaults(func=command_archive)

    p = sub.add_parser("run-block")
    p.add_argument("--continue-after-failure", action="store_true")
    p.set_defaults(func=command_run_block)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except WorkplaceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
