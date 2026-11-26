#!/usr/bin/env python3
"""Fail when a repository test_*.py file is not reachable from CI workflows.

Reachability is decided by `unittest discover` roots and by explicit
references inside `.github/workflows/*.yml`. This is a structural check, not a
YAML or shell interpreter: it never executes a workflow.

The repository has 63 `test_*.py` files and all 63 are reachable today. That
number is the point. `repository-hygiene.yml` executes some of them from a
hand-written list, which is an instance of the coverage; this script is the
rule, so a new test file that no workflow runs fails the required gate instead
of appearing green.

The same rule is applied to gate-shaped scripts (#925): a
`scripts/**/{check,audit,validate,verify}_*.py` file counts as wired only when
its path or basename is an argument of a command in a `run:` block. A name in a
comment does not count, and neither does wiring the gate's own *test* -- that
confusion is what let `tests/test_policy_inheritance.py` run while
`scripts/check_policy_inheritance.py` ran nowhere.

The unwired set is baselined in `scripts/ci/baselines/gate-wiring.txt` with the
same doctrine as `scripts/ci/gate_ratchet.py`: a new unwired gate fails, and a
baselined gate that becomes wired fails until the line is removed.
"""

import fnmatch
import glob
import os
import re
import sys
from pathlib import Path

GATE_NAME_RE = re.compile(r"^(?:check|audit|validate|verify)_.*\.py$")
RUN_KEY_RE = re.compile(r"^(?P<indent>[ ]*)(?:-\s+)?run:[ \t]*(?P<rest>.*)$")
RUN_BLOCK_RE = re.compile(r"^[|>][+-]?\d*$")
SHELL_SPLIT_RE = re.compile(r"[ \t\r\n;&|()<>]+")
BASELINE = Path("scripts") / "ci" / "baselines" / "gate-wiring.txt"

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
    """Return every repository directory, every test_*.py, and every gate script."""
    directories, tests, gates = [], [], []
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        directories.append(Path(current).resolve())
        for filename in filenames:
            path = (Path(current) / filename).resolve()
            if filename.startswith("test_") and filename.endswith(".py"):
                tests.append(path)
            elif GATE_NAME_RE.match(filename) and path.relative_to(root).parts[0] == "scripts":
                gates.append(path)
    return directories, sorted(tests), sorted(gates)


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


def stem_collisions(tests, root):
    """Return {stem: [paths]} for every stem shared by two or more test files.

    Rule B below is substring matching, so it is sound only while no two test
    files share a stem. This turns that precondition into a check: a collision
    makes the gate fail closed instead of reporting the shadowed file reachable.
    """
    by_stem = {}
    for test in tests:
        by_stem.setdefault(test.stem, []).append(test.relative_to(root).as_posix())
    return {stem: paths for stem, paths in by_stem.items() if len(paths) > 1}


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
    # (#834 nearly reported two wired files as residual). The trade is bounded
    # by stem_collisions() above, which fails closed before this runs. Upgrade
    # path: parse `run:` blocks and match whole arguments.
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


def strip_comment(line):
    """Drop a trailing shell comment, ignoring `#` inside quotes."""
    quote = None
    for index, char in enumerate(line):
        if quote:
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "#" and (index == 0 or line[index - 1] in " \t;&|("):
            return line[:index]
    return line


def run_blocks(text):
    """Return the shell text of every `run:` block in a workflow file.

    A `run:` value is either inline (`run: cmd`) or a `|`/`>` block whose body
    is the more-indented lines that follow. Comments are stripped so a gate
    named only in a comment is not an executed argument. This is a structural
    reading of the YAML that workflows actually use here, not a parser.
    """
    lines = text.splitlines()
    blocks = []
    index = 0
    while index < len(lines):
        match = RUN_KEY_RE.match(lines[index])
        if not match:
            index += 1
            continue
        rest, indent = match.group("rest").strip(), len(match.group("indent"))
        index += 1
        if RUN_BLOCK_RE.match(rest):
            body = []
            while index < len(lines):
                line = lines[index]
                if line.strip() and len(line) - len(line.lstrip()) <= indent:
                    break
                body.append(line)
                index += 1
            rest = "\n".join(body)
        blocks.append("\n".join(strip_comment(line) for line in rest.splitlines()))
    return blocks


def gate_wiring(gates, workflows, root):
    """Return {gate path: True/False} for wiring by an executed `run:` command.

    An argument matches when it is the gate's repository-relative path or its
    basename. Both are compared as whole tokens, so `check_policy_inheritance`
    in a comment, `tests/test_policy_inheritance.py`, and
    `scripts/check_policy_inheritance.py.bak` are all non-matches.
    """
    tokens = set()
    for workflow in workflows:
        for block in run_blocks(workflow.read_text(encoding="utf-8")):
            # Quotes are stripped per token because a gate is sometimes handed
            # to a wrapper as one quoted argument, e.g. gate_ratchet.py
            # --command "python3 scripts/check_bilingual_docs_full.py".
            tokens.update(
                token.strip("'\"")
                for token in SHELL_SPLIT_RE.split(block)
                if token.strip("'\"")
            )

    wired = {}
    for gate in gates:
        relative = gate.relative_to(root).as_posix()
        wired[relative] = relative in tokens or gate.name in tokens
    return wired


def read_baseline(root):
    path = root / BASELINE
    if not path.is_file():
        raise OSError("gate-wiring baseline not found: %s" % BASELINE.as_posix())
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            entries.append(stripped)
    return set(entries)


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
        directories, tests, gates = walk(root)

        collisions = stem_collisions(tests, root)
        if collisions:
            for stem, paths in sorted(collisions.items()):
                print(
                    "::error::Test file stem %r is shared by %s. Rule B matches "
                    "by substring, so it cannot tell them apart and would report "
                    "the unreferenced one reachable." % (stem, " and ".join(paths)),
                    file=sys.stderr,
                )
            return 1

        rules = discovery_rules(workflows, root, directories)

        unreachable = [
            test.relative_to(root).as_posix()
            for test in tests
            if not is_reachable(test, root, text, rules)
        ]

        wired = gate_wiring(gates, workflows, root)
        baseline = read_baseline(root)
        unwired = sorted(path for path, ok in wired.items() if not ok)
        new_unwired = [path for path in unwired if path not in baseline]
        stale = sorted(baseline - set(unwired))
    except (OSError, UnicodeError) as exc:
        print("::error::Test reachability could not be checked: %s" % exc, file=sys.stderr)
        return 2

    failed = False
    if unreachable:
        failed = True
        for path in unreachable:
            print(path)
        print(
            "::error::Test reachability: %d of %d test files are executed by no "
            "workflow. Wire them, or the next one arrives silently."
            % (len(unreachable), len(tests)),
            file=sys.stderr,
        )

    for path in new_unwired:
        print(path)
    if new_unwired:
        failed = True
        print(
            "::error::Gate wiring: %d gate-shaped script(s) are executed by no "
            "workflow and are not in %s. Wire them, or the next one arrives "
            "silently (#925)." % (len(new_unwired), BASELINE.as_posix()),
            file=sys.stderr,
        )

    for path in stale:
        print(
            "::error::Gate wiring baseline is stale (now wired or gone): %s" % path,
            file=sys.stderr,
        )
        failed = True

    if failed:
        return 1

    print(
        "Test reachability: %d test files, %d reachable, 0 unreachable"
        % (len(tests), len(tests)),
        file=sys.stderr,
    )
    print(
        "Gate wiring: %d gate scripts, %d unwired, %d baselined"
        % (len(gates), len(unwired), len(baseline)),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
