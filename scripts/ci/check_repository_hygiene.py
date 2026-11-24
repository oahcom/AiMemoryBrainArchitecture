#!/usr/bin/env python3
"""Check committed repository hygiene and PR new-file admission."""

import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath


CHECK_VERSION = "2026-11-24.3"

# Repository-root-relative paths, written with a leading slash.
PROHIBITED_PATHS = (
    "/_dm.txt",
)

# Fixed source-code allowlist. Do not infer this set from the base tree.
ALLOWED_SOURCE_SUFFIXES = frozenset({
    ".py",
    ".sh",
    ".bash",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".kts",
    ".rb",
    ".pl",
    ".sql",
    ".html",
    ".css",
    ".scss",
})

ALLOWED_DOCUMENT_SUFFIXES = frozenset({
    ".md",
    ".rst",
    ".adoc",
})

# Exact configuration filenames. JSON is intentionally limited to named
# configuration files; arbitrary JSON data and snapshots are not admitted.
ALLOWED_CONFIG_PATHS = frozenset({
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "Cargo.toml",
    "Dockerfile",
    "Makefile",
    "package.json",
    "pyproject.toml",
    "pytest.ini",
    "setup.cfg",
    "tox.ini",
    "tsconfig.json",
})

REQUIREMENTS_FILE_RE = re.compile(r"requirements(?:-[A-Za-z0-9_.-]+)?\.txt\Z")
FULL_SHA_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
# Work-item manifests are YAML, so no suffix rule can admit them without
# widening .yaml globally. This anchored path shape admits exactly the
# registry's own file and nothing else: one AID-YYYY-NNN directory level
# under work-items/, the literal name manifest.yaml, no nesting, no case
# variants.
#
# The ID segment is a four-digit year, a hyphen, and a three-digit sequence.
# It is not an arbitrary alnum run: AID-<anything> would admit spellings the
# registry cannot allocate, so a typo in a directory name would create a work
# item the index step then cannot resolve. The year is a shape, not a
# constant -- pinning it to one value would reject next year's first item,
# which is a rule nobody would remember to edit.
WORK_ITEM_MANIFEST_RE = re.compile(
    r"14-ai-development/work-items/AID-\d{4}-\d{3}/manifest\.yaml"
)

# D7: one explicitly approved nested conformance dependency pin.
# Do not merge this into REQUIREMENTS_FILE_RE: that rule remains root-only.
CONFORMANCE_PROVIDER_REQUIREMENTS_RE = re.compile(
    r"08-bmcp-protocol/tests/conformance/provider_outcome/requirements\.txt"
)

# D17: the conformance harness has its own package manifest and lockfile.
# Keep both exact paths under the conformance directory; this is not a
# general nested package.json or package-lock.json admission rule.
CONFORMANCE_PACKAGE_FILES_RE = re.compile(
    r"08-bmcp-protocol/tests/conformance/package(?:-lock)?\.json"
)

# D19: source snapshots are admitted only directly inside an AID work-item
# directory. The filename must end in .source.txt; nested directories and
# other work-item ID families are not admitted.
AID_SOURCE_SNAPSHOT_RE = re.compile(
    r"14-ai-development/work-items/AID-[0-9]{4}-[0-9]{3}/[^/]+\.source\.txt"
)

# D20: only the reference-model .gitignore directly under an AID work item
# is admitted. No other nested .gitignore path is covered.
AID_REFERENCE_MODEL_GITIGNORE_RE = re.compile(
    r"14-ai-development/work-items/AID-[0-9]{4}-[0-9]{3}/reference-model/\.gitignore"
)


def error(message):
    print(f"::error::{message}", file=sys.stderr)


def run_git(args, *, cwd=None):
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"cannot execute git: {exc}") from exc

    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(
            f"git {' '.join(args)} failed"
            + (f": {detail}" if detail else "")
        )

    return result.stdout


def repository_root():
    output = run_git(["rev-parse", "--show-toplevel"])
    root = output.decode("utf-8", errors="strict").strip()
    if not root:
        raise RuntimeError("git returned an empty repository root")
    return root


def resolve_commit(root, sha, label):
    if not FULL_SHA_RE.fullmatch(sha):
        raise RuntimeError(
            f"{label} must be a full 40-character commit SHA"
        )

    resolved = run_git(
        ["-C", root, "rev-parse", "--verify", f"{sha}^{{commit}}"]
    ).decode("ascii").strip()

    if resolved.lower() != sha.lower():
        raise RuntimeError(
            f"{label} did not resolve to the supplied commit SHA"
        )

    return resolved


def tree_paths(root, commit):
    """Return UTF-8 repository-relative paths from a committed Git tree."""
    raw = run_git([
        "-C",
        root,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        "--name-only",
        commit,
    ])

    paths = set()
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        try:
            paths.add(entry.decode("utf-8", errors="strict"))
        except UnicodeDecodeError as exc:
            raise RuntimeError(
                "tree contains a path that is not valid UTF-8; "
                "cannot apply the admission policy safely"
            ) from exc

    return paths


def is_allowed_new_path(path):
    """Apply the fixed, positive admission policy to one new tree path."""
    pure = PurePosixPath(path)
    name = pure.name
    suffix = pure.suffix.lower()

    if suffix in ALLOWED_DOCUMENT_SUFFIXES:
        return True

    if suffix in ALLOWED_SOURCE_SUFFIXES:
        return True

    if path in ALLOWED_CONFIG_PATHS:
        return True

    if (
        pure.parent == PurePosixPath(".")
        and REQUIREMENTS_FILE_RE.fullmatch(name)
    ):
        return True

    if (
        path.startswith(".github/workflows/")
        and suffix in {".yml", ".yaml"}
    ):
        return True

    if (
        path.startswith(".github/actions/")
        and name in {"action.yml", "action.yaml"}
    ):
        return True

    if WORK_ITEM_MANIFEST_RE.fullmatch(path):
        return True

    if CONFORMANCE_PROVIDER_REQUIREMENTS_RE.fullmatch(path):
        return True

    if CONFORMANCE_PACKAGE_FILES_RE.fullmatch(path):
        return True

    if AID_SOURCE_SNAPSHOT_RE.fullmatch(path):
        return True

    if AID_REFERENCE_MODEL_GITIGNORE_RE.fullmatch(path):
        return True

    return False


def check_prohibited_head_paths(head_paths):
    violations = []
    for prohibited_path in PROHIBITED_PATHS:
        tree_path = prohibited_path.lstrip("/")
        if tree_path in head_paths:
            violations.append(prohibited_path)
    return violations


def check_new_paths(root, base_sha, head_sha):
    """Check new paths in head tree relative to the merge-base tree."""
    base = resolve_commit(root, base_sha, "base SHA")
    head = resolve_commit(root, head_sha, "head SHA")

    merge_base = run_git([
        "-C",
        root,
        "merge-base",
        base,
        head,
    ]).decode("ascii").strip()

    if not FULL_SHA_RE.fullmatch(merge_base):
        raise RuntimeError("git merge-base returned an invalid commit SHA")

    baseline_paths = tree_paths(root, merge_base)
    head_paths = tree_paths(root, head)
    new_paths = sorted(head_paths - baseline_paths)

    rejected = [
        path for path in new_paths
        if not is_allowed_new_path(path)
    ]

    print(
        "Repository new-file admission "
        f"version={CHECK_VERSION} "
        f"base={base} "
        f"head={head} "
        f"merge_base={merge_base}"
    )

    if rejected:
        for path in rejected:
            error(
                "new-file admission violation: "
                f"no allowlist rule for '{path}'"
            )
        return 1

    print(
        "Repository new-file admission passed: "
        f"{len(new_paths)} new path(s) checked."
    )
    return 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="full base commit SHA")
    parser.add_argument("--head", help="full final head commit SHA")
    args = parser.parse_args()

    if bool(args.base) != bool(args.head):
        parser.error("--base and --head must be supplied together")

    return args


def main():
    args = parse_args()

    try:
        root = repository_root()

        # The original committed-HEAD denylist remains active on PR and push.
        head_for_denylist = (
            resolve_commit(root, args.head, "head SHA")
            if args.head
            else "HEAD"
        )
        head_paths = tree_paths(root, head_for_denylist)
        prohibited = check_prohibited_head_paths(head_paths)

        if prohibited:
            for path in prohibited:
                error(
                    "repository hygiene violation: "
                    f"prohibited committed file '{path}'"
                )
            return 1

        if args.base and args.head:
            return check_new_paths(root, args.base, args.head)

    except RuntimeError as exc:
        error(f"repository hygiene cannot be determined: {exc}")
        return 2

    print(
        "Repository hygiene check passed "
        f"(version={CHECK_VERSION})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
