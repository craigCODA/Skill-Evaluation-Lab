import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from TOOLING.verification import verify_lab


class VerifyLabTests(unittest.TestCase):
    def test_verify_lab_accepts_multi_experiment_run_indexes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "lab"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".worktrees"))
            exp2 = root / "EXPERIMENTS" / "EXP-0002-task02-quick-calculator-clear-label" / "RUN-INDEX.md"
            text = exp2.read_text(encoding="utf-8")
            self.assertIn("| `0016` |", text)

            errors = verify_lab.verify(root, release_json_path=None)

            self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
