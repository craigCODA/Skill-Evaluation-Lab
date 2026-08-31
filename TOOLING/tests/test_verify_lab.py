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
    def test_verify_accepts_current_state_with_planned_future_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "lab"
            shutil.copytree(
                ROOT,
                root,
                ignore=shutil.ignore_patterns(".git", ".worktrees", ".superpowers", "ACTIVE", "MOTHER", "ARCHIVE"),
            )

            run_index = root / "EXPERIMENTS" / "EXP-0002-task02-quick-calculator-clear-label" / "RUN-INDEX.md"
            self.assertIn("| `0016` |", run_index.read_text(encoding="utf-8"))

            self.assertEqual([], verify_lab.verify(root, release_json_path=None))


if __name__ == "__main__":
    unittest.main()
