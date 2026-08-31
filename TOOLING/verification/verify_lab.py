#!/usr/bin/env python3
"""Verify the Skill Evaluation Lab current record."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = ROOT
RUN_ID_RE = re.compile(r"^\d{4}$")
FORBIDDEN = (
    "qw" + "en",
    "qw" + "en2.5",
    "qw" + "en25",
    "0010-" + "qw" + "en",
    "0011-" + "qw" + "en",
    "0012-" + "qw" + "en",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_lf_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def parse_field(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(field)}:\s*`?([^`\n]+)`?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def load_runs(errors: list[str]) -> list[dict[str, str]]:
    path = ROOT / "DATA" / "runs.json"
    if not path.exists():
        fail(errors, "missing DATA/runs.json")
        return []
    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid DATA/runs.json: {exc}")
        return []
    if not isinstance(data, list):
        fail(errors, "DATA/runs.json must contain a list")
        return []
    return data


def current_state_ids(errors: list[str]) -> tuple[str | None, str | None]:
    path = ROOT / "CURRENT-STATE.md"
    if not path.exists():
        fail(errors, "missing CURRENT-STATE.md")
        return None, None
    text = read(path)
    completed = parse_field(text, "Current completed global run")
    next_run = parse_field(text, "Next global run")
    for field, value in (("Current completed global run", completed), ("Next global run", next_run)):
        if value is None:
            fail(errors, f"missing CURRENT-STATE.md field: {field}")
        elif not RUN_ID_RE.match(value):
            fail(errors, f"invalid CURRENT-STATE.md {field}: {value}")
    return completed, next_run


def check_forbidden(errors: list[str]) -> None:
    skip_parts = {".git", ".worktrees", ".superpowers"}
    checked_suffixes = {".md", ".txt", ".json", ".py", ".ps1", ".sh"}
    for path in ROOT.rglob("*"):
        if any(part in skip_parts for part in path.parts):
            continue
        lower_path = rel(path).lower()
        for token in FORBIDDEN:
            if token in lower_path:
                fail(errors, f"forbidden token in path: {rel(path)}")
        if not path.is_file() or path.suffix.lower() not in checked_suffixes:
            continue
        lower_text = read(path).lower()
        for token in FORBIDDEN:
            if token in lower_text:
                fail(errors, f"forbidden token in file: {rel(path)}")


def expected_ids(ids: list[str]) -> list[str]:
    if not ids:
        return []
    first = int(ids[0])
    last = int(ids[-1])
    return [f"{i:04d}" for i in range(first, last + 1)]


def check_contiguous_dirs(errors: list[str], name: str, path: Path) -> list[str]:
    if not path.exists():
        fail(errors, f"missing {rel(path)}")
        return []
    ids = sorted(p.name for p in path.iterdir() if p.is_dir() and RUN_ID_RE.match(p.name))
    expected = expected_ids(ids)
    if ids != expected:
        fail(errors, f"{name} IDs are not contiguous: got {ids}, expected {expected}")
    return ids


def check_development_history(errors: list[str], expected: list[str]) -> None:
    actual = sorted(p.stem for p in (ROOT / "DEVELOPMENT-HISTORY").glob("*.md") if RUN_ID_RE.match(p.stem))
    if actual != expected:
        fail(errors, f"development history IDs mismatch: got {actual}, expected {expected}")
    for run_id in expected:
        path = ROOT / "DEVELOPMENT-HISTORY" / f"{run_id}.md"
        if not path.exists():
            fail(errors, f"missing development history {run_id}")
            continue
        first = read(path).splitlines()[0].strip()
        if first != f"# {run_id}":
            fail(errors, f"{rel(path)} heading is {first!r}, expected '# {run_id}'")


def check_run_index(errors: list[str], expected: list[str]) -> None:
    paths = sorted((ROOT / "EXPERIMENTS").glob("*/RUN-INDEX.md"))
    if not paths:
        fail(errors, "missing experiment RUN-INDEX.md files")
        return
    ids = []
    for path in paths:
        text = read(path)
        for line in text.splitlines():
            if not line.startswith("|"):
                continue
            cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
            if not cells or not RUN_ID_RE.match(cells[0]):
                continue
            status = cells[5].strip().lower() if len(cells) >= 6 else "preserved"
            if status == "planned":
                continue
            ids.append(cells[0])
    if ids != expected:
        fail(errors, f"RUN-INDEX IDs mismatch: got {ids}, expected {expected}")


def check_data(errors: list[str], runs: list[dict[str, str]], expected: list[str]) -> None:
    data_ids = [str(item.get("run_id", "")) for item in runs]
    if data_ids != expected:
        fail(errors, f"DATA run IDs mismatch: got {data_ids}, expected {expected}")
    required = {
        "run_id",
        "model",
        "skill",
        "skill_version",
        "experiment",
        "evidence_class",
        "condition",
        "baseline_commit",
        "evidence_path",
        "experiment_run_path",
        "result_asset",
        "result_asset_sha256",
        "release_tag",
        "status",
    }
    for item in runs:
        run_id = str(item.get("run_id", ""))
        missing = sorted(k for k in required if not item.get(k))
        if missing:
            fail(errors, f"DATA run {run_id} missing fields: {missing}")
        for key in ("evidence_path", "experiment_run_path"):
            value = item.get(key)
            if value and not (ROOT / value).exists():
                fail(errors, f"DATA run {run_id} points to missing {key}: {value}")


def check_evidence(errors: list[str], runs: list[dict[str, str]], expected: list[str]) -> None:
    by_id = {item["run_id"]: item for item in runs if "run_id" in item}
    for run_id in expected:
        evidence = ROOT / "EVIDENCE" / run_id
        for filename in ("RUN.md", "RESULT-ASSET.md", "HASHES.txt", "RAW-RUN-RECORD.md"):
            if not (evidence / filename).exists():
                fail(errors, f"missing {rel(evidence / filename)}")
        if not (evidence / "RUN.md").exists() or not (evidence / "RESULT-ASSET.md").exists():
            continue
        run_text = read(evidence / "RUN.md")
        asset_text = read(evidence / "RESULT-ASSET.md")
        if not run_text.startswith(f"# Run {run_id}"):
            fail(errors, f"{rel(evidence / 'RUN.md')} heading mismatch")
        asset = parse_field(asset_text, "Asset")
        release_tag = parse_field(asset_text, "Release tag")
        digest = parse_field(asset_text, "SHA-256")
        if asset and not asset.startswith(f"run-{run_id}-"):
            fail(errors, f"{rel(evidence / 'RESULT-ASSET.md')} asset does not start with run ID")
        data = by_id.get(run_id)
        if data:
            if asset != data.get("result_asset"):
                fail(errors, f"asset mismatch for {run_id}: evidence {asset}, DATA {data.get('result_asset')}")
            if release_tag != data.get("release_tag"):
                fail(errors, f"release tag mismatch for {run_id}")
            if digest != data.get("result_asset_sha256"):
                fail(errors, f"asset hash mismatch for {run_id}")


def check_canonical_hashes(errors: list[str]) -> None:
    manifest = ROOT / "CANONICAL" / "layered-codebase-architecture" / "MANIFEST.txt"
    text = read(manifest)
    expected = {
        "SKILL.md": parse_field(text, "SKILL.md SHA-256"),
        "conventions.md": parse_field(text, "conventions.md SHA-256"),
    }
    for filename, digest in expected.items():
        if not digest:
            fail(errors, f"missing canonical hash for {filename}")
            continue
        actual = sha256_lf_text(ROOT / "CANONICAL" / "layered-codebase-architecture" / filename)
        if actual != digest:
            fail(errors, f"canonical hash mismatch for {filename}: {actual} != {digest}")


def check_release_json(errors: list[str], runs: list[dict[str, str]], path: Path | None) -> None:
    if path is None:
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid release JSON: {exc}")
        return
    assets = data.get("assets", [])
    names = sorted(asset.get("name", "") for asset in assets)
    tag = data.get("tagName") or data.get("tag_name")
    release_runs = runs
    if tag:
        release_runs = [item for item in runs if item.get("release_tag") == tag]
    expected = sorted([item["result_asset"] for item in release_runs] + ["SHA256SUMS.txt"])
    if names != expected:
        fail(errors, f"release assets mismatch: got {names}, expected {expected}")
    body = str(data.get("body", "")).lower()
    for token in FORBIDDEN:
        if token in body:
            fail(errors, "release body contains forbidden token")
    for name in names:
        for token in FORBIDDEN:
            if token in name.lower():
                fail(errors, f"release asset contains forbidden token: {name}")


def verify(root: Path = DEFAULT_ROOT, release_json_path: Path | None = None) -> list[str]:
    global ROOT
    previous_root = ROOT
    ROOT = Path(root).resolve()
    errors: list[str] = []
    try:
        check_forbidden(errors)
        runs = load_runs(errors)
        completed, next_run = current_state_ids(errors)
        evidence_ids = check_contiguous_dirs(errors, "evidence", ROOT / "EVIDENCE")
        expected = expected_ids(evidence_ids)
        if expected and expected[0] != "0001":
            fail(errors, f"current first run should be 0001, got {expected[0]}")
        if expected and completed and completed != expected[-1]:
            fail(errors, f"CURRENT-STATE completed run mismatch: got {completed}, expected {expected[-1]}")
        if expected and next_run and next_run != f"{int(expected[-1]) + 1:04d}":
            fail(errors, f"CURRENT-STATE next run mismatch: got {next_run}, expected {int(expected[-1]) + 1:04d}")
        if not expected and completed not in (None, "0000"):
            fail(errors, f"CURRENT-STATE completed run mismatch: got {completed}, expected 0000")
        check_development_history(errors, expected)
        check_run_index(errors, expected)
        check_data(errors, runs, expected)
        check_evidence(errors, runs, expected)
        check_canonical_hashes(errors)
        check_release_json(errors, runs, release_json_path)
        return errors
    finally:
        ROOT = previous_root


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-json", type=Path)
    args = parser.parse_args(argv)

    errors = verify(ROOT, args.release_json)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    evidence_ids = sorted(p.name for p in (ROOT / "EVIDENCE").iterdir() if p.is_dir() and RUN_ID_RE.match(p.name))
    through = evidence_ids[-1] if evidence_ids else "none"
    print(f"OK: verified {len(evidence_ids)} canonical runs through {through}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
