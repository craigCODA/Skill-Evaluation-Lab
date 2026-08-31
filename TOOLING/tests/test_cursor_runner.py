import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from TOOLING.cursor_runner import run_cursor_eval as runner


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
    (path / "src.txt").write_text("initial\n", encoding="utf-8", newline="\n")
    run_git(["add", "."], path)
    run_git(["commit", "-m", "initial"], path)
    return run_git(["rev-parse", "HEAD"], path)


def write_temp_lab(root, source_repo, baseline_commit):
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
    (skill / "SKILL.md").write_text(
        "---\nname: layered-codebase-architecture\ndescription: test\n---\n# Skill\n",
        encoding="utf-8",
        newline="\n",
    )
    (skill / "conventions.md").write_text("# Conventions\n", encoding="utf-8", newline="\n")
    (root / "DATA").mkdir()
    (root / "DATA" / "runs.json").write_text("[]\n", encoding="utf-8", newline="\n")
    (root / "CURRENT-STATE.md").write_text(
        "Current completed global run: `0000`\n\nNext global run: `0001`\n",
        encoding="utf-8",
        newline="\n",
    )
    config_path = root / "TOOLING" / "cursor-runner" / "runs"
    config_path.mkdir(parents=True)
    config = {
        "experiment": "EXP-TEST",
        "skill": "layered-codebase-architecture",
        "prompt_file": "EXPERIMENTS/EXP-TEST/PROMPT.txt",
        "baseline": {
            "repo_name": "Source",
            "commit": baseline_commit,
            "source": source_repo.as_posix(),
        },
        "default_model": {"label": "Test Model", "cursor_model_id": ""},
        "runs": [
            {
                "run_id": "0001",
                "skill_version": "NO-SKILL",
                "condition": "no skill",
                "evidence_class": "primary",
                "slash_invocation": False,
            },
            {
                "run_id": "0002",
                "skill_version": "00-SUPPLIED",
                "condition": "supplied original, forced",
                "evidence_class": "primary",
                "slash_invocation": True,
            },
        ],
    }
    file_path = config_path / "EXP-TEST.json"
    file_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8", newline="\n")
    return file_path


class CursorRunnerTests(unittest.TestCase):
    def test_prompt_for_no_skill_does_not_include_slash_invocation(self):
        config = runner.load_config(ROOT / "TOOLING/cursor-runner/runs/EXP-0002-task02-quick-calculator-clear-label.json")
        run = config.get_run("0016")

        prompt = runner.build_prompt(ROOT, config, run)

        self.assertFalse(prompt.startswith("/layered-codebase-architecture"))
        self.assertIn("Clear manual entries", prompt)

    def test_prompt_for_skill_arm_includes_exact_slash_invocation(self):
        config = runner.load_config(ROOT / "TOOLING/cursor-runner/runs/EXP-0002-task02-quick-calculator-clear-label.json")
        run = config.get_run("0017")

        prompt = runner.build_prompt(ROOT, config, run)

        self.assertTrue(prompt.startswith("/layered-codebase-architecture  "))
        self.assertIn("Clear manual entries", prompt)

    def test_prepare_workspace_copies_skill_only_for_skill_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "lab"
            root.mkdir()
            source = Path(tmp) / "source"
            commit = init_source_repo(source)
            config = runner.load_config(write_temp_lab(root, source, commit))

            no_skill_workspace = runner.prepare_workspace(root, config, config.get_run("0001"), "test-model")
            skill_workspace = runner.prepare_workspace(root, config, config.get_run("0002"), "test-model")

            self.assertFalse((no_skill_workspace / ".cursor" / "skills" / "layered-codebase-architecture").exists())
            self.assertTrue((skill_workspace / ".cursor" / "skills" / "layered-codebase-architecture" / "SKILL.md").exists())
            self.assertTrue((skill_workspace / ".cursor" / "skills" / "layered-codebase-architecture" / "conventions.md").exists())

    def test_preserve_run_archives_untracked_files_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "lab"
            root.mkdir()
            source = Path(tmp) / "source"
            commit = init_source_repo(source)
            config = runner.load_config(write_temp_lab(root, source, commit))
            run = config.get_run("0001")
            workspace = runner.prepare_workspace(root, config, run, "test-model")
            (workspace / "untracked.txt").write_text("preserve me\n", encoding="utf-8", newline="\n")
            execution = runner.ExecutionRecord(
                command=["agent", "-p", "Rename the button."],
                exit_code=0,
                stdout_path=workspace / ".lab-run" / "cursor-agent-stream.raw.jsonl",
                stderr_path=workspace / ".lab-run" / "cursor-agent-stderr.txt",
            )
            execution.stdout_path.parent.mkdir(parents=True, exist_ok=True)
            execution.stdout_path.write_text('{"type":"result","result":"ok"}\n', encoding="utf-8", newline="\n")
            execution.stderr_path.write_text("", encoding="utf-8", newline="\n")

            evidence = runner.preserve_run(root, config, run, workspace, execution)

            self.assertTrue((evidence / "RUN.md").exists())
            self.assertTrue((evidence / "cursor-agent-stream.raw.jsonl").exists())
            self.assertTrue((root / "DEVELOPMENT-HISTORY" / "0001.md").exists())
            archive_name = runner.parse_field((evidence / "RESULT-ASSET.md").read_text(encoding="utf-8"), "Asset")
            archive = root / "ARCHIVES" / "local" / archive_name
            self.assertTrue(archive.exists())
            with zipfile.ZipFile(archive, "r") as zf:
                self.assertTrue(any(name.endswith("/untracked.txt") for name in zf.namelist()))
            self.assertFalse(workspace.exists())
            with self.assertRaises(runner.RunnerError):
                runner.preserve_run(root, config, run, root / "missing-workspace", execution)


if __name__ == "__main__":
    unittest.main()
