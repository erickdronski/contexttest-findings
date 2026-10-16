"""Remove the answer key from a trial worktree before the agent starts.

Every experiment runs inside a checkout of this repository. Without this step
the agent could open the candidate instruction file, the assertion commands in
an experiment config, a hypothesis note, or the README's discussion of what was
expected — and the arm that is supposed to run without instructions would
quietly receive the treatment anyway.

contexttest runs this as a setup command: after the variant's instruction file
is placed at the repository root, and before the baseline snapshot, so nothing
removed here counts as a change the agent made. The instruction file under test
is never touched, because it lives at the root and none of the paths below
match it. This removes ordinary file access, not Git-history access: an agent
with Git or network access can still recover committed material. It is not a
security boundary or proof of blinded treatment.
"""

import glob
import shutil
import subprocess
import sys
from pathlib import Path

ANSWER_KEY = [
    "README.md",
    "results",
    ".github",
    "experiments/*/contexttest.json",
    "experiments/*/*.candidate.md",
    "experiments/*/HYPOTHESIS.md",
]


def require_linked_worktree():
    root = Path.cwd().resolve()
    if not (root / ".git").is_file():
        raise ValueError(
            "run only at the root of a disposable linked git worktree; refusing to delete files here"
        )
    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--show-toplevel",
            "--absolute-git-dir",
            "--git-common-dir",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    top, git_dir, common_dir = result.stdout.strip().splitlines()
    if (
        Path(top).resolve() != root
        or Path(git_dir).resolve() == Path(common_dir).resolve()
    ):
        raise ValueError(
            "run only in a disposable linked git worktree; primary checkouts and submodules are not supported"
        )

    return root


def main():
    root = require_linked_worktree()
    paths = [Path(path) for pattern in ANSWER_KEY for path in glob.glob(pattern)]
    # Check every parent before deleting anything. glob follows intermediate
    # directory symlinks, while a leaf symlink itself can safely be unlinked.
    for path in paths:
        parent = path.parent.resolve()
        if parent != root and root not in parent.parents:
            raise ValueError(
                f"answer-key path escapes the worktree through its parent: {path}; refusing to delete files"
            )
    for path in paths:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
    print(f"sanitize_worktree: removed {len(paths)} answer-key path(s)")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"sanitize_worktree: {exc}")
