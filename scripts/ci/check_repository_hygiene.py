#!/usr/bin/env python3
"""Check committed repository hygiene and PR new-file admission."""

import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath


CHECK_VERSION = "2026-11-24.6"

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

# A1: protocol schema files live directly under schemas/. One level only;
# schemas/<sub>/x.schema.json is not admitted.
#
# Version note: this rule set is 2026-11-24.5, not .4. #891 reached main first
# and took .4 for the work-item index membership check, which is a different
# policy change. Two different policies must not share a version string: the
# whole point of printing it in the log is that a reader can say which rules
# produced a given PASS, and a shared number makes that unanswerable.
PROTOCOL_SCHEMA_RE = re.compile(r"08-bmcp-protocol/schemas/[^/]+\.schema\.json")

# A2: conformance vectors are JSON anywhere below the conformance root, with
# one carve-out. package.json and package-lock.json belong to D17 only at the
# conformance root; the same names one level down stay refused. The negative
# lookahead is load-bearing -- dropping it turns this into conformance/**/*.json
# and silently admits the nested package files D17 deliberately excluded.
CONFORMANCE_VECTOR_RE = re.compile(
    r"08-bmcp-protocol/tests/conformance/(?:[^/]+/)*(?!package(?:-lock)?\.json\Z)[^/]+\.json"
)

# A4: each crate owns exactly one manifest at crates/<name>/Cargo.toml.
# Workspace members are flat, so no deeper Cargo.toml is admitted.
CRATE_MANIFEST_RE = re.compile(r"crates/[^/]+/Cargo\.toml")

# A5: governance-register evidence captures, flat under evidence/.
GOVERNANCE_EVIDENCE_RE = re.compile(
    r"14-ai-development/governance-register/evidence/[^/]+\.json"
)

# A6: each crate's VERIFICATION.txt sits beside its Cargo.toml, not deeper.
CRATE_VERIFICATION_RE = re.compile(r"crates/[^/]+/VERIFICATION\.txt")

# A8: two baselines with two shapes -- the root bilingual baseline and the
# per-check baselines directory. Both branches are exercised by tests.
BASELINE_FILE_RE = re.compile(
    r"(?:scripts/bilingual-baseline\.txt|scripts/ci/baselines/[^/]+\.txt)"
)

# B9-B12: four singleton governance files. Each is an exact path, not a
# pattern; a sibling with a different name must stay refused.
GOV_DOC_001_INHERITANCE_RE = re.compile(r"\.governance/GOV-DOC-001-inheritance\.json")
ARCHITECTURE_METADATA_SCHEMA_RE = re.compile(
    r"00-governance/architecture-document-metadata\.schema\.yaml"
)
DOCUMENT_SCOPE_REGISTRY_RE = re.compile(r"00-governance/document-scope-registry\.yaml")
REMOTE_WORKER_INVENTORY_RE = re.compile(r"14-ai-development/remote-worker-inventory\.yaml")


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

    if PROTOCOL_SCHEMA_RE.fullmatch(path):
        return True

    if CONFORMANCE_VECTOR_RE.fullmatch(path):
        return True

    if CRATE_MANIFEST_RE.fullmatch(path):
        return True

    if GOVERNANCE_EVIDENCE_RE.fullmatch(path):
        return True

    if CRATE_VERIFICATION_RE.fullmatch(path):
        return True

    if BASELINE_FILE_RE.fullmatch(path):
        return True

    if GOV_DOC_001_INHERITANCE_RE.fullmatch(path):
        return True

    if ARCHITECTURE_METADATA_SCHEMA_RE.fullmatch(path):
        return True

    if DOCUMENT_SCOPE_REGISTRY_RE.fullmatch(path):
        return True

    if REMOTE_WORKER_INVENTORY_RE.fullmatch(path):
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


WORK_ITEMS_DIR = "14-ai-development/work-items"
WORK_ITEMS_INDEX = "14-ai-development/work-items/INDEX.md"
LOCAL_LINK_RE = re.compile(r"\]\(([^)#?\s]+)")

def work_item_directories(head_paths):
    """Names of the directories directly under work-items/, from the tree."""
    names = set()
    for path in head_paths:
        if not path.startswith(WORK_ITEMS_DIR + "/"):
            continue
        name, sep, _ = path[len(WORK_ITEMS_DIR) + 1:].partition("/")
        if sep and name:
            names.add(name)
    return names

def index_entry_directories(text):
    """First path segment of every repository-relative link in the index."""
    names = set()
    for target in LOCAL_LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        name, sep, _ = target.partition("/")
        if sep and name not in {".", ".."}:
            names.add(name)
    return names

def check_index_membership(root, commit, head_paths):
    """Require one index entry per work-item directory, and the converse.

    #858 is the standing evidence that a hand-kept list drifts: the directory
    is the fact and the index is the claim about it. Both directions are
    checked, so a deleted row and a deleted directory each fail. The set of
    directories is read from the committed tree, like the denylist above, so a
    working-copy edit cannot launder a missing entry.

    What this deliberately does NOT verify: membership only. It does not check
    that a row's Status/Review/Acceptance text agrees with the item's own
    manifest. That is a different relation and it is not cheap here: measured
    on main at b40463cd, a naive `status:`-prefixes-cell comparison fails on
    24 of 46 rows. Cells carry dated activity assertions (`PR OPEN`,
    `MERGED 2026-11-19T18:11:20Z`) while manifests carry lifecycle states
    (`VERIFIED`, `REMEDIATION_IN_PROGRESS`), and ten indexed items have no
    `manifest.yaml` at all -- a fix item's `authorization-manifest.yaml` is a
    different document. A gate that red on half the registry the day it landed
    would be switched off, so this one does not pretend to cover it.

    The separate manifest-consistency check verifies only internal lifecycle
    field combinations in work-item manifests. It does not compare INDEX.md
    Status cells with manifest lifecycle fields, and does not verify external
    PR or GitHub state.
    """
    directories = work_item_directories(head_paths)
    if not directories:
        return []

    if WORK_ITEMS_INDEX not in head_paths:
        # Deliberate ceiling: membership is a relation between the tree and the
        # index, so with no index there is no relation here to falsify. Taking
        # the index away is a governance act of its own (it is a Canonical
        # document) and is not a membership defect; this check does not pretend
        # to catch it.
        return []

    try:
        text = run_git(
            ["-C", root, "show", f"{commit}:{WORK_ITEMS_INDEX}"]
        ).decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            f"'{WORK_ITEMS_INDEX}' is not valid UTF-8"
        ) from exc
    except RuntimeError as exc:
        raise RuntimeError(f"cannot read '{WORK_ITEMS_INDEX}': {exc}") from exc

    entries = index_entry_directories(text)

    violations = [
        f"index membership violation: directory present, no index entry: "
        f"{WORK_ITEMS_DIR}/{name}"
        for name in sorted(directories - entries)
    ]
    violations += [
        f"index membership violation: index entry present, no directory: "
        f"{WORK_ITEMS_DIR}/{name}"
        for name in sorted(entries - directories)
    ]

    print(
        "Work-item index membership "
        f"version={CHECK_VERSION} "
        f"directories={len(directories)} "
        f"linked={len(entries)}"
    )

    return violations

def _manifest_scalar(lines, key, *, start=0, end=None):
    """Return one simple YAML scalar from a mapping block, if present."""
    if end is None:
        end = len(lines)

    pattern = re.compile(
        rf"^(\s*){re.escape(key)}:[ \t]*(.*?)[ \t]*$"
    )

    for line in lines[start:end]:
        match = pattern.fullmatch(line)
        if not match:
            continue

        value = match.group(2)
        if " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        return value

    return None


def _unquote_manifest_scalar(value):
    """Remove one matching pair of YAML scalar quotes."""
    if (
        value is not None
        and len(value) >= 2
        and value[0] == value[-1]
        and value[0] in {"'", '"'}
    ):
        return value[1:-1]
    return value


def _implementation_status(lines):
    """Read implementation.status from the implementation mapping."""
    implementation_start = None

    for index, line in enumerate(lines):
        if re.fullmatch(r"implementation:[ \t]*(?:#.*)?", line):
            implementation_start = index + 1
            break

    if implementation_start is None:
        return None

    implementation_end = len(lines)
    for index in range(implementation_start, len(lines)):
        line = lines[index]
        if line and not line[0].isspace() and not line.startswith("#"):
            implementation_end = index
            break

    for line in lines[implementation_start:implementation_end]:
        match = re.fullmatch(r"([ \t]+)status:[ \t]*(.*?)[ \t]*", line)
        if match:
            return _unquote_manifest_scalar(match.group(2))

    return None


def check_work_item_manifest_consistency(root, commit, head_paths):
    """Check internal lifecycle consistency in committed work-item manifests.

    This is deliberately a static, repository-local check. It does not verify
    that a PR exists, that a SHA exists in Git, or that a SHA is reachable
    from a target branch.
    """
    manifest_paths = sorted(
        path for path in head_paths
        if WORK_ITEM_MANIFEST_RE.fullmatch(path)
    )

    violations = []

    for path in manifest_paths:
        try:
            raw = run_git(["-C", root, "show", f"{commit}:{path}"])
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise RuntimeError(
                f"'{path}' is not valid UTF-8"
            ) from exc
        except RuntimeError as exc:
            raise RuntimeError(
                f"cannot read '{path}': {exc}"
            ) from exc

        lines = text.splitlines()

        top_status = _unquote_manifest_scalar(
            _manifest_scalar(lines, "status")
        )
        implementation_status = _implementation_status(lines)
        pull_request = _manifest_scalar(lines, "pull_request")
        merge_commit_sha = _unquote_manifest_scalar(
            _manifest_scalar(lines, "merge_commit_sha")
        )

        # R20-01: either PR_OPEN lifecycle field requires a positive,
        # unquoted YAML integer in pull_request.
        if (
            top_status == "PR_OPEN"
            or implementation_status == "PR_OPEN"
        ):
            if (
                pull_request is None
                or not re.fullmatch(r"[1-9][0-9]*", pull_request)
            ):
                violations.append(
                    "manifest consistency violation: "
                    f"'{path}': PR_OPEN requires pull_request to be "
                    "a positive integer"
                )

        # R20-02: NOT_MERGED cannot coexist with a lifecycle state that
        # asserts implementation has already merged or been verified.
        if merge_commit_sha == "NOT_MERGED":
            if (
                top_status in {"MERGED", "VERIFIED"}
                or implementation_status == "MERGED"
            ):
                violations.append(
                    "manifest consistency violation: "
                    f"'{path}': merge_commit_sha is NOT_MERGED while "
                    "the lifecycle status asserts merged implementation"
                )

        # R20-03: NOT_STARTED cannot coexist with a syntactically real
        # implementation merge SHA. No Git-object or reachability check
        # is performed here.
        if (
            implementation_status == "NOT_STARTED"
            and merge_commit_sha is not None
            and FULL_SHA_RE.fullmatch(merge_commit_sha)
        ):
            violations.append(
                "manifest consistency violation: "
                f"'{path}': implementation.status is NOT_STARTED "
                "while merge_commit_sha contains a full SHA"
            )

    print(
        "Work-item manifest consistency "
        f"version={CHECK_VERSION} "
        f"manifests={len(manifest_paths)} "
        f"violations={len(violations)}"
    )

    return violations


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

        membership = check_index_membership(root, head_for_denylist, head_paths)
        if membership:
            for violation in membership:
                error(violation)
            return 1

        manifest_consistency = check_work_item_manifest_consistency(
            root,
            head_for_denylist,
            head_paths,
        )
        if manifest_consistency:
            for violation in manifest_consistency:
                error(violation)
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
