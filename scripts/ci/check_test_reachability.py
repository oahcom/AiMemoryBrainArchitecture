#!/usr/bin/env python3
"""Fail when a repository test_*.py file is not reachable from CI workflows.

Reachability is decided by `unittest discover` roots and by explicit
references inside `.github/workflows/*.yml`. This is a structural check, not a
YAML or shell interpreter: it never executes a workflow.

The repository has 56 `test_*.py` files and all 56 are reachable today. That
number is the point. `repository-hygiene.yml` executes twelve of them from a
hand-written list, which is an instance of the coverage; this script is the
rule, so a new test file that no workflow runs fails the required gate instead
of appearing green.
"""

import fnmatch
import glob
import os
import re
import sys
from pathlib import Path

DISCOVER_RE = re.compile(
    r"\bdiscover\b"
    r"\s+-s\s+(?P<root>'[^']*'|\"[^\"]*\"|[^\s;&|]+)"
    r"(?:\s+-p\s+(?P<pattern>'[^']*'|\"[^\"]*\"|[^\s;&|]+))?"
)


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def walk(root):
    """Return every repository directory and every test_*.py, skipping .git."""
    directories, tests = [], []
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        directories.append(Path(current).resolve())
        for filename in filenames:
            if filename.startswith("test_") and filename.endswith(".py"):
                tests.append((Path(current) / filename).resolve())
    return directories, sorted(tests)


def read_workflows(root):
    paths = sorted(glob.glob(str(root / ".github" / "workflows" / "*.yml")))
    return [Path(path) for path in paths]


def discovery_rules(workflows, root, directories):
    """Resolve every `discover -s <root>` to a directory plus a filename glob."""
    rules = []
    for workflow in workflows:
        for match in DISCOVER_RE.finditer(workflow.read_text(encoding="utf-8")):
            raw_root = unquote(match.group("root"))
            pattern = unquote(match.group("pattern") or "test*.py")

            candidate = (root / raw_root).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                raise OSError(
                    "unittest discovery root escapes repository: %r" % raw_root
                )

            if candidate.is_dir():
                matches = [candidate]
            else:
                # A discovery root can be relative to a `working-directory:` or
                # to a `cd` earlier in the same step, so it need not exist at
                # the repository root. Match its path suffix against the real
                # directories and refuse to guess if more than one fits.
                parts = Path(raw_root).parts
                matches = [
                    directory
                    for directory in directories
                    if directory != root
                    and directory.relative_to(root).parts[-len(parts):] == parts
                ]

            if len(matches) > 1:
                raise OSError(
                    "ambiguous unittest discovery root %r: %s"
                    % (
                        raw_root,
                        ", ".join(
                            path.relative_to(root).as_posix() for path in matches
                        ),
                    )
                )
            if matches:
                rules.append((matches[0], pattern))
    return rules


def is_reachable(test, root, workflow_text, rules):
    for discovery_root, pattern in rules:
        if (
            discovery_root == test.parent or discovery_root in test.parents
        ) and fnmatch.fnmatch(test.name, pattern):
            return True

    # ponytail: Rule B is substring matching, so a new test whose name is
    # contained in an existing wired name is reported as reachable when it is
    # not — scripts/ci/test_check_fmt.py is hidden by scripts/test_check_fmt.
    # That is the deliberate trade: the alternative is parsing every `run:`
    # block, and a basename-only matcher was already the wrong answer twice
    # (#834 nearly reported two wired files as residual). Upgrade path: parse
    # `run:` blocks and match whole arguments.
    relative = test.relative_to(root)
    return any(
        reference in workflow_text
        for reference in (
            relative.as_posix(),
            relative.name,
            relative.stem,
            ".".join(relative.with_suffix("").parts),
        )
    )


def main(argv):
    if len(argv) > 2:
        print("usage: %s [repository-root]" % Path(argv[0]).name, file=sys.stderr)
        return 2

    try:
        root = (
            Path(argv[1]).resolve()
            if len(argv) == 2
            else Path(__file__).resolve().parent.parent.parent
        )
        if not (root / ".github" / "workflows").is_dir():
            raise OSError("no .github/workflows under %s" % root)

        workflows = read_workflows(root)
        text = "\n".join(path.read_text(encoding="utf-8") for path in workflows)
        directories, tests = walk(root)
        rules = discovery_rules(workflows, root, directories)

        unreachable = [
            test.relative_to(root).as_posix()
            for test in tests
            if not is_reachable(test, root, text, rules)
        ]
    except (OSError, UnicodeError) as exc:
        print("::error::Test reachability could not be checked: %s" % exc, file=sys.stderr)
        return 2

    if unreachable:
        for path in unreachable:
            print(path)
        print(
            "::error::Test reachability: %d of %d test files are executed by no "
            "workflow. Wire them, or the next one arrives silently."
            % (len(unreachable), len(tests)),
            file=sys.stderr,
        )
        return 1

    print(
        "Test reachability: %d test files, %d reachable, 0 unreachable"
        % (len(tests), len(tests)),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
