import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import workplace


def run_git(args, cwd):
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.strip()


def init_source_repo(path):
    path.mkdir(parents=True)
    run_git(["init"], path)
    run_git(["config", "user.email", "lab-test@example.invalid"], path)
    run_git(["config", "user.name", "Lab Test"], path)
    (path / "README.md").write_text("# Source\n", encoding="utf-8", newline="\n")
    (path / "component.txt").write_text("Clear entries\n", encoding="utf-8", newline="\n")
    run_git(["add", "."], path)
    run_git(["commit", "-m", "initial"], path)
    return run_git(["rev-parse", "HEAD"], path)


def write_temp_lab(root, source_repo, baseline_commit):
    (root / "MOTHER").mkdir()
    run_git(["clone", "--mirror", str(source_repo), str(root / "MOTHER" / "ShingleFile-main.git")], root)
    (root / "ACTIVE").mkdir()
    (root / "ARCHIVES" / "local").mkdir(parents=True)
    (root / "EVIDENCE").mkdir()
    (root / "DEVELOPMENT-HISTORY").mkdir()
    (root / "DATA").mkdir()
    (root / "DATA" / "runs.json").write_text("[]\n", encoding="utf-8", newline="\n")
    (root / "CURRENT-STATE.md").write_text(
        "# Current State\n\nCurrent completed global run: `0000`\n\nNext global run: `0001`\n",
        encoding="utf-8",
        newline="\n",
    )

    exp = root / "EXPERIMENTS" / "EXP-TEST"
    exp.mkdir(parents=True)
    (exp / "PROMPT.txt").write_text("Rename the button.\n", encoding="utf-8", newline="\n")
    (exp / "RUN-INDEX.md").write_text(
        "\n".join(
            [
                "# Run Index",
                "",
                "| Run | Model | Version | Evidence class | Condition | Status |",
                "| --- | --- | --- | --- | --- | --- |",
                "| `0001` | Test Model | NO-SKILL | primary | no skill | planned |",
                "| `0002` | Test Model | 00-SUPPLIED | primary | supplied original, forced | planned |",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )

    skill = root / "SKILLS" / "layered-codebase-architecture" / "00-SUPPLIED"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Skill\n", encoding="utf-8", newline="\n")
    (skill / "conventions.md").write_text("# Conventions\n", encoding="utf-8", newline="\n")

    matrix = {
        "experiment": "EXP-TEST",
        "skill": "layered-codebase-architecture",
        "prompt_file": "EXPERIMENTS/EXP-TEST/PROMPT.txt",
        "baseline": {
            "repo_name": "ShingleFile-main",
            "commit": baseline_commit,
            "branch": "main",
        },
        "runs": [
            {
                "run_id": "0001",
                "model": "Test Model",
                "cursor_model_id": "test-model",
                "skill_version": "NO-SKILL",
                "condition": "no skill",
                "evidence_class": "primary",
                "slash_invocation": False,
            },
            {
                "run_id": "0002",
                "model": "Test Model",
                "cursor_model_id": "test-model",
                "skill_version": "00-SUPPLIED",
                "condition": "supplied original, forced",
                "evidence_class": "primary",
                "slash_invocation": True,
            },
        ],
    }
    matrix_path = root / "TOOLING" / "workplace" / "runs" / "EXP-TEST.json"
    matrix_path.parent.mkdir(parents=True)
    matrix_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8", newline="\n")
    return matrix_path


def write_execution(root, run_id="0001", exit_code=0):
    lab_run = workplace.run_state_dir(root)
    lab_run.mkdir(parents=True, exist_ok=True)
    (lab_run / "cursor-agent-stream.raw.jsonl").write_text(
        '{"type":"result","result":"done"}\n',
        encoding="utf-8",
        newline="\n",
    )
    (lab_run / "cursor-agent-stderr.txt").write_text("", encoding="utf-8", newline="\n")
    workplace.write_json(
        lab_run / "execution.json",
        {
            "run_id": run_id,
            "command": ["agent", "-p", "Rename the button."],
            "exit_code": exit_code,
            "started_at_utc": "2026-08-31T00:00:00+00:00",
            "completed_at_utc": "2026-08-31T00:00:01+00:00",
        },
    )


class WorkplaceLifecycleTests(unittest.TestCase):
    def make_lab(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "lab"
        root.mkdir()
        source = Path(tmp.name) / "source"
        commit = init_source_repo(source)
        matrix = workplace.load_matrix(write_temp_lab(root, source, commit))
        return tmp, root, matrix

    def test_fresh_refuses_run_id_that_is_not_current_next_global_run(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            with self.assertRaisesRegex(workplace.WorkplaceError, "Next global run"):
                workplace.fresh(root, matrix, matrix.get_run("0002"))
            self.assertFalse((root / "ACTIVE" / "ShingleFile-main").exists())

    def test_archive_refuses_missing_execution_record_by_default(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            run = matrix.get_run("0001")
            active = workplace.fresh(root, matrix, run)

            with self.assertRaisesRegex(workplace.WorkplaceError, "execution.json is required"):
                workplace.archive_active(root, matrix, run)

            self.assertTrue(active.exists())
            self.assertFalse((root / "EVIDENCE" / "0001").exists())
            self.assertEqual([], list((root / "ARCHIVES" / "local").glob("run-0001-*.zip")))

    def test_archive_refuses_active_metadata_that_does_not_match_run(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            run = matrix.get_run("0001")
            active = workplace.fresh(root, matrix, run)
            metadata_path = workplace.run_state_dir(root) / "RUN-METADATA.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["skill_version"] = "00-SUPPLIED"
            workplace.write_json(metadata_path, metadata)
            write_execution(root)

            with self.assertRaisesRegex(workplace.WorkplaceError, "metadata mismatch"):
                workplace.archive_active(root, matrix, run)

            self.assertTrue(active.exists())
            self.assertFalse((root / "EVIDENCE" / "0001").exists())

    def test_archive_preserves_active_then_removes_it_after_zip_verification(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            run = matrix.get_run("0001")
            active = workplace.fresh(root, matrix, run)
            (active / "component.txt").write_text("Clear manual entries\n", encoding="utf-8", newline="\n")
            (active / "untracked.txt").write_text("preserve me\n", encoding="utf-8", newline="\n")
            write_execution(root)

            evidence = workplace.archive_active(root, matrix, run)

            self.assertFalse(active.exists())
            self.assertTrue((evidence / "RUN.md").exists())
            self.assertTrue((evidence / "cursor-agent-stream.raw.jsonl").exists())
            self.assertTrue((root / "DEVELOPMENT-HISTORY" / "0001.md").exists())
            self.assertIn("Current completed global run: `0001`", (root / "CURRENT-STATE.md").read_text(encoding="utf-8"))
            self.assertIn("Next global run: `0002`", (root / "CURRENT-STATE.md").read_text(encoding="utf-8"))

            data = json.loads((root / "DATA" / "runs.json").read_text(encoding="utf-8"))
            self.assertEqual("0001", data[0]["run_id"])
            archive = root / "ARCHIVES" / "local" / data[0]["result_asset"]
            with zipfile.ZipFile(archive, "r") as zf:
                self.assertIsNone(zf.testzip())
                self.assertTrue(any(name.endswith("/.git/HEAD") for name in zf.namelist()))
                self.assertTrue(any(name.endswith("/untracked.txt") for name in zf.namelist()))


if __name__ == "__main__":
    unittest.main()
