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
    workplace.write_json(
        root / "workplace.json",
        {
            "format_version": 1,
            "repo_name": "ShingleFile-main",
            "baseline_sha": baseline_commit,
            "baseline_branch": "main",
            "baseline_tag": "workplace-baseline",
            "mode": "skill-research",
            "mother_path": "MOTHER/ShingleFile-main.git",
            "active_path": "ACTIVE/ShingleFile-main",
            "active_state_path": "ACTIVE/.run-state",
        },
    )
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


def set_current_state(root, completed, next_run):
    (root / "CURRENT-STATE.md").write_text(
        f"# Current State\n\nCurrent completed global run: `{completed}`\n\nNext global run: `{next_run}`\n",
        encoding="utf-8",
        newline="\n",
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

    def test_execute_refuses_prompt_hash_drift_before_agent_lookup(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            run = matrix.get_run("0001")
            workplace.fresh(root, matrix, run)
            (root / matrix.prompt_file).write_text("Different prompt.\n", encoding="utf-8", newline="\n")

            with self.assertRaisesRegex(workplace.WorkplaceError, "prompt_sha256 mismatch"):
                workplace.execute_active(root, matrix, run)

    def test_archive_refuses_source_skill_hash_drift_after_fresh(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            set_current_state(root, "0001", "0002")
            run = matrix.get_run("0002")
            active = workplace.fresh(root, matrix, run)
            (root / "SKILLS" / matrix.skill / "00-SUPPLIED" / "SKILL.md").write_text(
                "# Changed Skill\n", encoding="utf-8", newline="\n"
            )
            write_execution(root, run_id="0002")

            with self.assertRaisesRegex(workplace.WorkplaceError, "skill_hashes mismatch"):
                workplace.archive_active(root, matrix, run)

            self.assertTrue(active.exists())
            self.assertFalse((root / "EVIDENCE" / "0002").exists())

    def test_archive_refuses_injected_harness_skill_drift_after_fresh(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            set_current_state(root, "0001", "0002")
            run = matrix.get_run("0002")
            active = workplace.fresh(root, matrix, run)
            (active / ".cursor" / "skills" / matrix.skill / "SKILL.md").write_text(
                "# Changed Injected Skill\n", encoding="utf-8", newline="\n"
            )
            write_execution(root, run_id="0002")

            with self.assertRaisesRegex(workplace.WorkplaceError, "harness manifest mismatch"):
                workplace.archive_active(root, matrix, run)

            self.assertTrue(active.exists())
            self.assertFalse((root / "EVIDENCE" / "0002").exists())

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

    def test_archive_separates_harness_state_from_model_created_changes(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            set_current_state(root, "0001", "0002")
            run = matrix.get_run("0002")
            active = workplace.fresh(root, matrix, run)
            (active / "component.txt").write_text("Clear manual entries\n", encoding="utf-8", newline="\n")
            (active / "model-note.txt").write_text("model-created\n", encoding="utf-8", newline="\n")
            write_execution(root, run_id="0002")

            evidence = workplace.archive_active(root, matrix, run)

            harness = json.loads((evidence / "harness-manifest.json").read_text(encoding="utf-8"))
            harness_paths = {item["path"] for item in harness["files"]}
            self.assertIn(".cursor/cli.json", harness_paths)
            self.assertIn(".cursor/skills/layered-codebase-architecture/SKILL.md", harness_paths)

            pre_untracked = (evidence / "pre-execution-untracked-files.txt").read_text(encoding="utf-8")
            self.assertIn(".cursor/cli.json", pre_untracked)
            self.assertIn(".cursor/skills/layered-codebase-architecture/SKILL.md", pre_untracked)

            model_untracked = (evidence / "model-created-untracked-files.txt").read_text(encoding="utf-8")
            self.assertIn("model-note.txt", model_untracked)
            self.assertNotIn(".cursor/cli.json", model_untracked)
            self.assertNotIn(".cursor/skills/layered-codebase-architecture/SKILL.md", model_untracked)

            tracked_subject = (evidence / "tracked-subject-files.txt").read_text(encoding="utf-8")
            self.assertEqual("component.txt", tracked_subject.strip())
            subject_status = (evidence / "model-created-git-status.txt").read_text(encoding="utf-8")
            self.assertIn(" M component.txt", subject_status)
            self.assertIn("?? model-note.txt", subject_status)
            self.assertNotIn(".cursor/", subject_status)

    def test_archive_diffs_against_baseline_even_if_agent_commits_change(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            run = matrix.get_run("0001")
            active = workplace.fresh(root, matrix, run)
            baseline = matrix.baseline.commit
            (active / "component.txt").write_text("Clear manual entries\n", encoding="utf-8", newline="\n")
            run_git(["config", "user.email", "agent@example.invalid"], active)
            run_git(["config", "user.name", "Agent"], active)
            run_git(["add", "component.txt"], active)
            run_git(["commit", "-m", "agent change"], active)
            final_head = run_git(["rev-parse", "HEAD"], active)
            write_execution(root)

            evidence = workplace.archive_active(root, matrix, run)

            self.assertNotEqual(baseline, final_head)
            self.assertEqual(final_head, (evidence / "final-head.txt").read_text(encoding="utf-8").strip())
            self.assertEqual(baseline, (evidence / "baseline-head.txt").read_text(encoding="utf-8").strip())
            self.assertIn("M\tcomponent.txt", (evidence / "git-diff-name-status.txt").read_text(encoding="utf-8"))
            diff = (evidence / "diff.patch").read_text(encoding="utf-8")
            self.assertIn("-Clear entries", diff)
            self.assertIn("+Clear manual entries", diff)

    def test_result_asset_record_marks_local_archive_pending_publication(self):
        tmp, root, matrix = self.make_lab()
        with tmp:
            run = matrix.get_run("0001")
            active = workplace.fresh(root, matrix, run)
            (active / "component.txt").write_text("Clear manual entries\n", encoding="utf-8", newline="\n")
            write_execution(root)

            evidence = workplace.archive_active(root, matrix, run)

            result = (evidence / "RESULT-ASSET.md").read_text(encoding="utf-8")
            self.assertIn("Storage class: local-only archive", result)
            self.assertIn("Publication status: pending", result)
            self.assertIn("Fresh-clone retrievable: no", result)
            self.assertIn("Durable publication path: GitHub Release asset", result)


if __name__ == "__main__":
    unittest.main()
