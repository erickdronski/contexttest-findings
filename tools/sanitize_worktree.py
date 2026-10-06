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
match it.
"""

import glob
import os
import shutil

ANSWER_KEY = [
    "README.md",
    "results",
    ".github",
    "experiments/*/contexttest.json",
    "experiments/*/*.candidate.md",
    "experiments/*/HYPOTHESIS.md",
]


def main():
    removed = 0
    for pattern in ANSWER_KEY:
        for path in glob.glob(pattern):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            removed += 1
    print(f"sanitize_worktree: removed {removed} answer-key path(s)")


if __name__ == "__main__":
    main()
