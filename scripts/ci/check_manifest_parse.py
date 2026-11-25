#!/usr/bin/env python3
"""Parse every committed work-item manifest, rejecting duplicate keys.

`aid-2026-001-manifest-validation.yml` is the only strict-parse job in CI, and
it names one file in both its `paths:` filter and its body. Every manifest
under `14-ai-development/work-items/*/manifest.yaml` parses today, and none is
required to. That is how a manifest sat unparseable while every gate reported
`violations=0` (b34c8e37 repaired four).

This check closes that gap: it globs every manifest, parses it with a loader
that rejects a duplicate key instead of silently keeping the last one, and
names every failing path with its reason.

Deliberate ceiling: this is parseability and duplicate keys. It is not schema
validation and it is not a consistency check between fields. The passing run
says so, so green is not read as more than it is.

Exit codes:
    0: every manifest parsed, no duplicate keys.
    1: one or more manifests failed to parse or carry a duplicate key.
    2: no manifest was found to check, so nothing was verified.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
from yaml.constructor import ConstructorError

MANIFEST_GLOB = "14-ai-development/work-items/*/manifest.yaml"

NOT_CHECKED = (
    "This checks YAML parseability and duplicate keys only. It does not "
    "validate field values, field semantics, status validity, or cross-field "
    "consistency."
)


class UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that rejects a duplicate mapping key rather than keeping one."""


def _construct_unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            hash(key)
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def load_strict(text):
    """Parse YAML text, raising on a duplicate key at any depth."""
    return yaml.load(text, Loader=UniqueKeyLoader)


def find_manifests(root):
    """Every manifest in the tree, sorted. Counted by file, not by directory."""
    return sorted(root.glob(MANIFEST_GLOB))


def failures_in(paths):
    """Return [(path, reason)] for every manifest that does not parse cleanly."""
    failures = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            failures.append((path, f"cannot read: {exc}"))
            continue
        try:
            load_strict(text)
        except yaml.YAMLError as exc:
            failures.append((path, " ".join(str(exc).split())))
    return failures


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) > 2:
        print(f"usage: {Path(argv[0]).name} [repository-root]", file=sys.stderr)
        return 2

    root = (
        Path(argv[1]).resolve()
        if len(argv) == 2
        else Path(__file__).resolve().parents[2]
    )

    paths = find_manifests(root)
    if not paths:
        print(
            f"::error::No work-item manifest found under {root} ({MANIFEST_GLOB}); "
            "nothing was verified.",
            file=sys.stderr,
        )
        return 2

    failures = failures_in(paths)
    for path, reason in failures:
        print(f"::error::Manifest parse failure {path}: {reason}", file=sys.stderr)

    print(NOT_CHECKED)
    print(
        f"Manifest parse: {len(paths)} manifests found, "
        f"{len(paths) - len(failures)} parsed, {len(failures)} failed."
    )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
