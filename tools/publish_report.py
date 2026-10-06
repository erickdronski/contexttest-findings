"""Copy a contexttest report into results/, with this machine's paths removed.

A report is written for the person who ran it, so it carries absolute paths:
the repository root, each trial's worktree, the home directory, and the
mangled project key Claude Code derives from the repository path. None of that
is evidence, and all of it identifies the machine. This rewrites those paths
to stable placeholders, keeps every number and every line of agent output
otherwise intact, and regenerates the HTML from the scrubbed JSON so the two
files cannot disagree.

    python3 tools/publish_report.py .contexttest/reports/<run>/report.json \\
        results/<experiment>/<date>/run-1

The HTML is rendered by contexttest. Set CONTEXTTEST_CLI to use a local
checkout instead of the published package, e.g.
CONTEXTTEST_CLI="node ../contexttest/src/cli.mjs".
"""

import json
import os
import re
import shlex
import subprocess
import sys

DEFAULT_CLI = "npx --yes github:erickdronski/contexttest"


def repository_root():
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def scrubber(root):
    home = os.path.expanduser("~")
    worktree = re.compile(re.escape(root) + r"/\.contexttest/worktrees/[^/\s\"']+/[^/\s\"']+")
    mangled = re.sub(r"[^A-Za-z0-9]", "-", root)

    def scrub(text):
        text = worktree.sub("<worktree>", text)
        text = text.replace(root, "<repo>")
        text = text.replace(mangled, "<repo-key>")
        return text.replace(home, "~")

    return scrub


def walk(value, scrub):
    if isinstance(value, str):
        return scrub(value)
    if isinstance(value, list):
        return [walk(item, scrub) for item in value]
    if isinstance(value, dict):
        return {key: walk(item, scrub) for key, item in value.items()}
    return value


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    source, destination = argv[1], argv[2]
    root = repository_root()
    with open(source, encoding="utf-8") as handle:
        report = json.load(handle)

    report = walk(report, scrubber(root))
    report["artifacts"] = {"json": "report.json", "html": "report.html"}

    os.makedirs(destination, exist_ok=True)
    target = os.path.join(destination, "report.json")
    with open(target, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    cli = shlex.split(os.environ.get("CONTEXTTEST_CLI", DEFAULT_CLI))
    subprocess.run([*cli, "report", target], check=True)

    home = os.path.expanduser("~")
    for name in ("report.json", "report.html"):
        with open(os.path.join(destination, name), encoding="utf-8") as handle:
            if home in handle.read():
                sys.exit(f"publish_report: {name} still contains {home}; refusing to publish")
    print(f"publish_report: wrote {destination}/report.json and report.html")


if __name__ == "__main__":
    main(sys.argv)
