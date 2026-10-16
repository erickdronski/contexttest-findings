"""Copy a contexttest report into results/, with this machine's paths removed.

A report is written for the person who ran it, so it carries absolute paths:
the repository root, each trial's worktree, the home directory, and the
mangled project key Claude Code derives from the repository path. None of that
is evidence, and all of it identifies the machine. This rewrites those paths
to stable placeholders, keeps every number and every line of agent output
otherwise intact, and regenerates the HTML from the scrubbed JSON so the two
files cannot disagree. A new destination is required: rendering and path checks
finish in a temporary directory before either artifact is published.

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
import tempfile
from pathlib import Path

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
    worktree = re.compile(
        re.escape(root) + r"/\.contexttest/worktrees/[^/\s\"']+/[^/\s\"']+"
    )
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
        result = {}
        for key, item in value.items():
            clean_key = scrub(key)
            if clean_key in result:
                raise ValueError("path scrubbing would merge distinct report keys")
            result[clean_key] = walk(item, scrub)
        return result
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

    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError(
            "destination already exists; choose a new directory to preserve published evidence"
        )
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    assert_no_machine_paths(serialized, "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    cli = shlex.split(os.environ.get("CONTEXTTEST_CLI", DEFAULT_CLI))
    if not cli:
        raise ValueError("CONTEXTTEST_CLI must name a renderer")
    with tempfile.TemporaryDirectory(
        prefix=".report-draft-", dir=destination.parent
    ) as staging:
        target = Path(staging) / "report.json"
        target.write_text(serialized, encoding="utf-8")
        subprocess.run([*cli, "report", str(target)], check=True)
        for name in ("report.json", "report.html"):
            assert_no_machine_paths(
                (Path(staging) / name).read_text(encoding="utf-8"), name
            )
        # Publish the complete pair together; failures above leave no destination.
        Path(staging).rename(destination)
    print(f"publish_report: wrote {destination}/report.json and report.html")


def assert_no_machine_paths(text, name):
    # Refuse foreign-machine homes instead of silently exporting a report that
    # was only scrubbed for the machine running this tool. This is a path check,
    # not a general secret scanner; review the report before sharing it.
    homes = re.compile(
        r"/(?:Users|home)/[^/\s\"<>]+(?:/|$)|[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s\"<>]+",
        re.MULTILINE,
    )
    if homes.search(text) or os.path.expanduser("~") in text:
        raise ValueError(
            f"{name} still contains a machine home path; refusing to publish"
        )


if __name__ == "__main__":
    try:
        main(sys.argv)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"publish_report: {exc}")
