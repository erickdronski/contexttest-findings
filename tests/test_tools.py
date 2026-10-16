"""Export and deletion-safety regressions; no agent or network calls."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "publish_report", ROOT / "tools/publish_report.py"
)
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class TestPublishReport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "input.json"
        self.destination = self.root / "published"
        self.source.write_text(json.dumps({"output": "safe sample", "score": 0.5}))

    def render(self, command, **kwargs):
        source = Path(command[-1])
        source.with_name("report.html").write_text(source.read_text())

    def publish(self, renderer=None):
        with (
            patch.object(publisher, "repository_root", return_value=str(self.root)),
            patch.object(
                publisher.subprocess, "run", side_effect=renderer or self.render
            ),
            patch.dict(os.environ, {"CONTEXTTEST_CLI": "test-renderer"}),
        ):
            publisher.main(
                ["publish_report.py", str(self.source), str(self.destination)]
            )

    def test_complete_pair_published_after_rendering(self):
        self.publish()
        data = json.loads((self.destination / "report.json").read_text())
        self.assertEqual(data["score"], 0.5)
        self.assertEqual(
            data["artifacts"], {"json": "report.json", "html": "report.html"}
        )
        self.assertTrue((self.destination / "report.html").is_file())
        self.assertFalse(list(self.root.glob(".report-draft-*")))

    def test_renderer_failure_leaves_no_partial_publication(self):
        def fail(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "test-renderer")

        with self.assertRaises(subprocess.CalledProcessError):
            self.publish(fail)
        self.assertFalse(self.destination.exists())
        self.assertFalse(list(self.root.glob(".report-draft-*")))

    def test_existing_results_are_never_overwritten(self):
        self.destination.mkdir()
        target = self.destination / "report.json"
        target.write_text("original evidence")
        with self.assertRaisesRegex(ValueError, "destination already exists"):
            self.publish()
        self.assertEqual(target.read_text(), "original evidence")

    def test_foreign_home_paths_are_rejected_before_publication(self):
        for path in (
            "/Users/anotherperson/work/repo",
            "/home/anotherperson/work/repo",
            r"C:\Users\anotherperson\repo",
        ):
            with self.subTest(path=path):
                self.source.write_text(json.dumps({"output": path}))
                with self.assertRaisesRegex(ValueError, "machine home path"):
                    self.publish()
                self.assertFalse(self.destination.exists())

    def test_renderer_cannot_introduce_a_machine_home_path(self):
        def leak(command, **kwargs):
            Path(command[-1]).with_name("report.html").write_text(
                "/home/anotherperson/repo"
            )

        with self.assertRaisesRegex(ValueError, "machine home path"):
            self.publish(leak)
        self.assertFalse(self.destination.exists())

    def test_paths_in_dictionary_keys_are_scrubbed_without_losing_values(self):
        data = {str(self.root / "file"): {"score": 0.5}}
        self.assertEqual(
            publisher.walk(data, publisher.scrubber(str(self.root))),
            {"<repo>/file": {"score": 0.5}},
        )
        with self.assertRaisesRegex(ValueError, "merge distinct"):
            publisher.walk(
                {str(self.root): 1, "<repo>": 2}, publisher.scrubber(str(self.root))
            )


class TestSanitizeWorktree(unittest.TestCase):
    def test_refuses_primary_checkout_and_removes_only_worktree_answer_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            fixture = root / "experiments/sample/fixture"
            fixture.mkdir(parents=True)
            (fixture / "task.py").write_text("# fixture\n")
            (root / "README.md").write_text("answer\n")
            (root / "experiments/sample/CLAUDE.candidate.md").write_text("answer\n")
            (root / "CLAUDE.md").write_text("treatment\n")

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True, text=True
                )

            git("init")
            git("add", ".")
            git(
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@localhost",
                "-c",
                "core.hooksPath=/dev/null",
                "commit",
                "-m",
                "test fixture",
            )
            command = [sys.executable, str(ROOT / "tools/sanitize_worktree.py")]
            refused = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("refusing to delete", refused.stderr)
            self.assertTrue((root / "README.md").is_file())
            worktree = Path(temporary) / "trial"
            git("worktree", "add", "--detach", str(worktree), "HEAD")
            outside = Path(temporary) / "outside"
            outside.mkdir()
            external_answer = outside / "contexttest.json"
            external_answer.write_text("external evidence")
            linked_experiment = worktree / "experiments/external"
            linked_experiment.symlink_to(outside, target_is_directory=True)
            escaped = subprocess.run(
                command, cwd=worktree, capture_output=True, text=True
            )
            self.assertNotEqual(escaped.returncode, 0)
            self.assertIn("escapes the worktree", escaped.stderr)
            self.assertEqual(external_answer.read_text(), "external evidence")
            self.assertTrue(
                (worktree / "README.md").is_file(),
                "preflight must finish before deleting any file",
            )
            linked_experiment.unlink()
            # A leaf symlink can be unlinked without touching its target.
            leaf = worktree / "experiments/sample/contexttest.json"
            leaf.symlink_to(external_answer)
            accepted = subprocess.run(
                command, cwd=worktree, capture_output=True, text=True
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertFalse((worktree / "README.md").exists())
            self.assertFalse(leaf.exists())
            self.assertEqual(external_answer.read_text(), "external evidence")
            self.assertFalse(
                (worktree / "experiments/sample/CLAUDE.candidate.md").exists()
            )
            self.assertTrue((worktree / "experiments/sample/fixture/task.py").is_file())
            self.assertEqual((worktree / "CLAUDE.md").read_text(), "treatment\n")
            self.assertTrue((root / "README.md").is_file())
            # This documents the real limit: the Git object remains accessible.
            recovered = subprocess.run(
                ["git", "show", "HEAD:README.md"],
                cwd=worktree,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(recovered.stdout, "answer\n")
            git("worktree", "remove", "--force", str(worktree))


if __name__ == "__main__":
    unittest.main()
