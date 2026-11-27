from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPOSITORY_ROOT / "scripts" / "check_work_item_uniqueness.py"

SPEC = importlib.util.spec_from_file_location(
    "check_work_item_uniqueness",
    CHECKER_PATH,
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load work-item uniqueness checker")

CHECKER = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class TemporaryGitRepository:
    def __init__(self, directory: str):
        self.root = Path(directory)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Work Item Uniqueness Tests")
        self.git("config", "user.email", "work-item-tests@example.invalid")

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise AssertionError(
                f"git {' '.join(args)} failed:\n{result.stdout}\n{result.stderr}"
            )
        return result.stdout.strip()

    def write(self, relative_path: str, content: str = "test\n") -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def branch(self, name: str, start: str) -> None:
        self.git("branch", name, start)

    def checkout(self, name: str) -> None:
        self.git("checkout", name)

    def update_ref(self, name: str, sha: str) -> None:
        self.git("update-ref", f"refs/heads/{name}", sha)

    def add_work_item(self, aid: str) -> None:
        self.write(
            f"14-ai-development/work-items/{aid}/manifest.yaml",
            f"work_item_id: {aid}\n",
        )
        self.write(
            "14-ai-development/work-items/INDEX.md",
            f"| [{aid}]({aid}/manifest.yaml) | test |\n",
        )

    def initial_commit(self) -> str:
        self.write(
            "14-ai-development/work-items/INDEX.md",
            "# Work Items\n",
        )
        self.write(
            "14-ai-development/work-items/AID-2026-100/manifest.yaml",
            "work_item_id: AID-2026-100\n",
        )
        return self.commit("initial target")

    def run_checker(
        self,
        target: str,
        candidate: str,
    ) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = CHECKER.main(
                [
                    "--root", str(self.root),
                    "--target", target,
                    "--candidate", candidate,
                ]
            )
        return code, output.getvalue()


class WorkItemUniquenessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = TemporaryGitRepository(self.temporary.name)
        self.base = self.repo.initial_commit()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_positive_new_unoccupied_id_is_accepted(self) -> None:
        self.repo.checkout("main")
        self.repo.branch("pr-new", self.base)
        self.repo.checkout("pr-new")
        self.repo.add_work_item("AID-2026-261")
        candidate = self.repo.commit("introduce unused ID")

        code, output = self.repo.run_checker("main", candidate)

        self.assertEqual(code, 0, output)
        self.assertIn("PASS new work-item directory AID-2026-261", output)
        self.assertIn("TARGET_OCCUPIED_NEW_DIRECTORIES=0", output)
        self.assertIn(f"candidate={candidate}", output)

    def test_negative_id_already_on_latest_target_is_rejected(self) -> None:
        self.repo.branch("pr-a", self.base)
        self.repo.branch("pr-b", self.base)

        self.repo.checkout("pr-a")
        self.repo.add_work_item("AID-2026-261")
        self.repo.commit("PR A introduces ID")

        self.repo.checkout("pr-b")
        self.repo.add_work_item("AID-2026-261")
        candidate = self.repo.commit("PR B introduces same ID")

        self.repo.checkout("main")
        self.repo.add_work_item("AID-2026-261")
        self.repo.commit("target occupies ID")

        code, output = self.repo.run_checker("main", candidate)

        self.assertEqual(code, 1, output)
        self.assertIn(
            "ERROR WU-01 duplicate work-item directory AID-2026-261",
            output,
        )
        self.assertIn("TARGET_OCCUPIED_NEW_DIRECTORIES=1", output)
        self.assertIn("BAD=1", output)

    def test_incremental_file_in_existing_directory_is_accepted(self) -> None:
        self.repo.checkout("main")
        self.repo.branch("pr-update", self.base)
        self.repo.checkout("pr-update")
        self.repo.write(
            "14-ai-development/work-items/AID-2026-100/evidence.md",
            "# Incremental evidence\n",
        )
        candidate = self.repo.commit("add evidence to existing work item")

        code, output = self.repo.run_checker("main", candidate)

        self.assertEqual(code, 0, output)
        self.assertIn(
            "PASS existing work-item directory AID-2026-100",
            output,
        )
        self.assertIn("TARGET_OCCUPIED_NEW_DIRECTORIES=0", output)

    def test_same_candidate_ref_changes_result_with_latest_target(self) -> None:
        self.repo.branch("pr-fixed", self.base)
        self.repo.checkout("pr-fixed")
        self.repo.add_work_item("AID-2026-261")
        candidate = self.repo.commit("candidate introduces ID")

        self.repo.checkout("main")
        self.repo.branch("target-before", self.base)
        self.repo.checkout("main")

        code_before, output_before = self.repo.run_checker(
            "target-before",
            "pr-fixed",
        )
        self.assertEqual(code_before, 0, output_before)

        self.repo.add_work_item("AID-2026-261")
        self.repo.commit("target advances and occupies ID")

        code_after, output_after = self.repo.run_checker(
            "main",
            "pr-fixed",
        )
        self.assertEqual(code_after, 1, output_after)
        self.assertIn(
            "ERROR WU-01 duplicate work-item directory AID-2026-261",
            output_after,
        )

        self.assertEqual(
            self.repo.git("rev-parse", "pr-fixed"),
            candidate,
        )

    def test_two_concurrent_candidates_cannot_both_pass_serial_checks(self) -> None:
        self.repo.branch("pr-a", self.base)
        self.repo.branch("pr-b", self.base)

        self.repo.checkout("pr-a")
        self.repo.add_work_item("AID-2026-262")
        candidate_a = self.repo.commit("PR A introduces shared ID")

        self.repo.checkout("pr-b")
        self.repo.add_work_item("AID-2026-262")
        candidate_b = self.repo.commit("PR B introduces shared ID")

        self.repo.checkout("main")

        code_a, output_a = self.repo.run_checker("main", candidate_a)
        self.assertEqual(code_a, 0, output_a)

        self.repo.update_ref("main", candidate_a)

        code_b, output_b = self.repo.run_checker("main", candidate_b)
        self.assertEqual(code_b, 1, output_b)
        self.assertIn(
            "ERROR WU-01 duplicate work-item directory AID-2026-262",
            output_b,
        )
        self.assertIn("BAD=1", output_b)

    def test_missing_target_ref_is_incomplete_not_pass(self) -> None:
        code, output = self.repo.run_checker(
            "refs/heads/does-not-exist",
            self.base,
        )
        self.assertEqual(code, 2, output)
        self.assertIn("INCOMPLETE:", output)

    def test_real_repository_self_comparison_does_not_report_existing_ids(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = CHECKER.main(
                [
                    "--root", str(REPOSITORY_ROOT),
                    "--target", "HEAD",
                    "--candidate", "HEAD",
                ]
            )
        self.assertEqual(code, 0, output.getvalue())
        self.assertIn("TARGET_OCCUPIED_NEW_DIRECTORIES=0", output.getvalue())
        self.assertIn("PASS WORK ITEM UNIQUENESS", output.getvalue())


if __name__ == "__main__":
    unittest.main()
