#!/usr/bin/env python3
"""Check committed repository hygiene and PR new-file admission."""

import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath


# Version note: 2026-11-27.1 is not a rule change -- the allowlist below is
# unchanged -- but it is a contract change and it has to be distinguishable in
# a log. A run that omits --base/--head used to print the same "passed" line as
# a run that performed new-file admission; a reader cannot tell the two
# 2026-11-24.8 PASSes apart. From this version the unqualified run exits 2 with
# SKIPPED and the head-tree half must be requested with --head-tree-only, so a
# 2026-11-27.1 PASS with no "SKIPPED" in it means admission actually ran.
#
# 2026-11-27.2 is a rule change on the head-tree half: index membership fails
# closed when either side of the relation is absent, where it used to return no
# violations over an empty set (AID-2026-199, #1212). The two versions are
# separate numbers on purpose -- one changed the contract, the other the rules.
CHECK_VERSION = "2026-11-27.3"

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

# The AC4 legacy ratchet is data, but only this exact report path is admitted.
ALLOWED_DATA_PATHS = frozenset({
    "14-ai-development/reports/work-item-manifest-ac4-baseline.json",
    "14-ai-development/reports/steward-adoption-baseline.json",
    "14-ai-development/reports/work-item-legacy-cohort.json",
    "14-ai-development/reports/work-item-legacy-disposition.json",
    "14-ai-development/work-items/AID-2026-291/baseline.json",
    "scripts/ci/baselines/protection-fingerprint.json",
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

# The schema registry is the one file directly under work-items/ that is not a
# work-item directory. The path is exact: the exclusion list has to stay a
# single file a reviewer can read in one diff, not a directory of fragments
# that accumulate without anyone seeing the whole policy.
MANIFEST_SCHEMA_REGISTRY_RE = re.compile(
    r"14-ai-development/work-items/manifest-schema-registry\.yaml"
)

# AID-2026-251: the one normative Work Item manifest schema file.
WORK_ITEM_MANIFEST_SCHEMA_RE = re.compile(
    r"14-ai-development/work-items/work-item-manifest\.schema\.yaml"
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

    if path in ALLOWED_DATA_PATHS:
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

    if MANIFEST_SCHEMA_REGISTRY_RE.fullmatch(path):
        return True

    if WORK_ITEM_MANIFEST_SCHEMA_RE.fullmatch(path):
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


# A root-level underscore or dot file is a working-copy artifact, not
# repository content: `_pr_body.md` and `_tmp_pr_create.py` reached main's
# review queue that way. The rule is root-scoped on purpose -- a leading
# underscore in a subdirectory is ordinary (a private module, an internal
# fixture), and widening this to the whole tree would refuse both.
ROOT_SCRATCH_PREFIXES = ("_", ".")


def is_root_scratch_path(path):
    """True for a new path directly at the repository root, _ or . prefixed."""
    pure = PurePosixPath(path)
    return (
        pure.parent == PurePosixPath(".")
        and pure.name.startswith(ROOT_SCRATCH_PREFIXES)
    )


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

    rejected = []
    for path in new_paths:
        if is_root_scratch_path(path):
            rejected.append((
                path,
                f"'{path}' is a root-level underscore/dot file; "
                "scratch files do not belong at the repository root",
            ))
        elif not is_allowed_new_path(path):
            rejected.append((path, f"no allowlist rule for '{path}'"))

    print(
        "Repository new-file admission "
        f"version={CHECK_VERSION} "
        f"base={base} "
        f"head={head} "
        f"merge_base={merge_base}"
    )

    if rejected:
        for _, reason in rejected:
            error(f"new-file admission violation: {reason}")
        return 1

    print(
        "Repository new-file admission passed: "
        f"{len(new_paths)} new path(s) checked."
    )
    return 0


WORK_ITEMS_DIR = "14-ai-development/work-items"
WORK_ITEMS_INDEX = "14-ai-development/work-items/INDEX.md"
MANIFEST_SCHEMA_REGISTRY = (
    "14-ai-development/work-items/manifest-schema-registry.yaml"
)
SCHEMA_REGISTRY_VERSION = "1"
SCHEMA_REGISTRY_DISPOSITION = "EXCLUDED_FROM_MANIFEST_CONSISTENCY_GATE"
SCHEMA_REGISTRY_FIELDS = frozenset(
    {"path", "record_type", "disposition", "rationale"}
)
LOCAL_LINK_RE = re.compile(r"\]\(([^)#?\s]+)")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

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
    """First path segment of every repository-relative link in a table row.

    Only a table row registers: a line whose first non-space character is `|`,
    after HTML comment spans are removed and outside a fenced code block. A
    link in prose, in an `<!-- -->` comment or in a fence is not a registry
    entry and registers nothing. Before this rule any link anywhere in the
    file counted, so a row commented out kept the check green while the row
    was gone from the table (#944).

    What this deliberately does NOT verify: that the row is in the work-item
    registry table, or that any cell in it says something true. A row in the
    file's other, unrelated table counts the same, and cell contents are not
    read at all. Two ceilings are accepted rather than handled: an `<!--` with
    no `-->` removes nothing, so the text after it is still read, and an
    unbalanced fence inverts the in-fence test for the rest of the file.
    """
    names = set()
    in_fence = False
    # A comment span is removed before lines are read, so a commented-out row
    # is not a row. Newlines inside the span are kept, so removing a comment
    # cannot splice the lines on either side into one.
    uncommented = COMMENT_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"), text
    )
    for line in uncommented.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not line.lstrip().startswith("|"):
            continue
        for target in LOCAL_LINK_RE.findall(line):
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

    Both sides fail closed when absent (#1212). An empty side is not a satisfied
    relation, it is an unbound one: with no directories the summary printed
    `directories=0 linked=N` and reported every entry missing, and with no index
    it printed nothing at all and returned no violations. Either way, renaming
    `work-items/` or deleting a Canonical index silenced the check, and a
    silent pass is indistinguishable from a real one in the log. `RuntimeError`
    is this file's "cannot be determined" channel, so `main()` turns it into
    exit 2, the same answer the other checks give for a missing input.
    """
    directories = work_item_directories(head_paths)
    if not directories:
        raise RuntimeError(
            f"no work-item directories under '{WORK_ITEMS_DIR}'; the membership "
            "relation has no directory side to verify, so a renamed or deleted "
            "directory must not read as a pass"
        )

    if WORK_ITEMS_INDEX not in head_paths:
        raise RuntimeError(
            f"the work-item index '{WORK_ITEMS_INDEX}' is absent from the tree; "
            "the index side of the membership relation cannot be read, and its "
            "absence is not a pass"
        )

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

def _mapping_scalar(lines, key, indent):
    """Return a scalar only when key is a direct child at the exact indent."""
    pattern = re.compile(
        rf"^{{0}}{re.escape(key)}\s*:\s*(.*?)\s*$".format(" " * indent)
    )

    for line in lines:
        match = pattern.match(line)
        if match:
            return _strip_yaml_scalar(match.group(1))

    return None


def _strip_yaml_scalar(value):
    """Strip a simple YAML comment and matching scalar quotes."""
    value = value.strip()

    if not value:
        return None

    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]

    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]

    # Comments are only recognized when preceded by whitespace.
    value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
    return value or None


def _implementation_mapping(lines):
    """Return direct scalar children of the top-level implementation mapping."""
    implementation_indent = 0
    implementation_line = None

    for index, line in enumerate(lines):
        if re.match(r"^implementation\s*:\s*(?:#.*)?$", line):
            implementation_line = index
            break

    if implementation_line is None:
        return None

    block = []
    for line in lines[implementation_line + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        if indent <= implementation_indent:
            break

        block.append((indent, line))

    if not block:
        return {}

    # Direct children use the minimum indentation in this mapping.
    child_indent = min(indent for indent, _ in block)

    direct_lines = [
        line[child_indent:]
        for indent, line in block
        if indent == child_indent
    ]

    return {
        "status": _mapping_scalar(direct_lines, "status", 0),
        "pull_request": _mapping_scalar(direct_lines, "pull_request", 0),
        "merge_commit_sha": _mapping_scalar(
            direct_lines, "merge_commit_sha", 0
        ),
    }


def _top_level_manifest_scalar(lines, key):
    """Read a scalar from a top-level YAML mapping key only."""
    return _mapping_scalar(lines, key, 0)


def load_manifest_schema_registry(root, commit):
    """Return {path: record_type} of records explicitly excluded from the gate.

    Exact pairs only. A record_type on its own excludes nothing: otherwise a
    future manifest could opt out of the gate simply by declaring a type, and
    the registry would become a naming convention rather than a decision.
    Wildcards, directory-level exemptions and filename prefixes are not
    implemented, for the same reason.

    The registry is read from the same committed tree as the manifests, so a
    working-copy edit cannot widen the exclusion set.

    A missing or malformed registry is an error, not an empty registry. "No
    policy declared" and "policy unreadable" must not produce the same output:
    only one of them means the gate legitimately has nothing to exclude.
    """
    try:
        raw = run_git(
            ["-C", root, "show", f"{commit}:{MANIFEST_SCHEMA_REGISTRY}"]
        )
    except RuntimeError as exc:
        raise RuntimeError(
            f"cannot read '{MANIFEST_SCHEMA_REGISTRY}': {exc}"
        ) from exc

    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            f"'{MANIFEST_SCHEMA_REGISTRY}' is not valid UTF-8"
        ) from exc

    version = None
    entries = []
    current = None
    in_records = False
    dash_indent = None

    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        where = f"'{MANIFEST_SCHEMA_REGISTRY}' line {lineno}"

        if not line[0].isspace():
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current = None
            if key == "schema_registry_version":
                version = _strip_yaml_scalar(value)
                in_records = False
                continue
            if key == "excluded_records":
                if value:
                    raise RuntimeError(
                        f"{where}: 'excluded_records' must be a block "
                        "sequence, not an inline value"
                    )
                in_records = True
                continue
            raise RuntimeError(
                f"{where}: unexpected top-level key '{key}'"
            )

        if not in_records:
            raise RuntimeError(
                f"{where}: indented content outside 'excluded_records'"
            )

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if stripped.startswith("- "):
            dash_indent = indent
            current = {}
            entries.append(current)
            stripped = stripped[2:].strip()
            if not stripped:
                continue
        elif current is None or dash_indent is None or indent <= dash_indent:
            raise RuntimeError(
                f"{where}: entry field is not indented under a list item"
            )

        key, _, value = stripped.partition(":")
        key = key.strip()
        if key not in SCHEMA_REGISTRY_FIELDS:
            raise RuntimeError(f"{where}: unexpected entry field '{key}'")
        if key in current:
            raise RuntimeError(f"{where}: duplicate entry field '{key}'")
        current[key] = _strip_yaml_scalar(value)

    if version != SCHEMA_REGISTRY_VERSION:
        raise RuntimeError(
            f"'{MANIFEST_SCHEMA_REGISTRY}': schema_registry_version must be "
            f"'{SCHEMA_REGISTRY_VERSION}', found {version!r}"
        )

    if not in_records:
        raise RuntimeError(
            f"'{MANIFEST_SCHEMA_REGISTRY}': 'excluded_records' is missing"
        )

    exclusions = {}
    for entry in entries:
        path = entry.get("path")
        record_type = entry.get("record_type")
        disposition = entry.get("disposition")

        if not path or not record_type or not disposition:
            raise RuntimeError(
                f"'{MANIFEST_SCHEMA_REGISTRY}': every entry needs path, "
                "record_type and disposition"
            )

        if disposition != SCHEMA_REGISTRY_DISPOSITION:
            raise RuntimeError(
                f"'{MANIFEST_SCHEMA_REGISTRY}': '{path}' has disposition "
                f"'{disposition}', which this gate does not implement"
            )

        if not WORK_ITEM_MANIFEST_RE.fullmatch(path):
            raise RuntimeError(
                f"'{MANIFEST_SCHEMA_REGISTRY}': '{path}' is not a path this "
                "gate inspects, so excluding it would have no effect"
            )

        if path in exclusions:
            if exclusions[path] == record_type:
                raise RuntimeError(
                    f"'{MANIFEST_SCHEMA_REGISTRY}': '{path}' is registered "
                    "twice with the same record_type"
                )
            raise RuntimeError(
                f"'{MANIFEST_SCHEMA_REGISTRY}': '{path}' is registered with "
                f"two different record_type values ('{exclusions[path]}' and "
                f"'{record_type}'); a record has one type"
            )

        exclusions[path] = record_type

    return exclusions


def check_work_item_manifest_consistency(root, commit, head_paths):
    """Check internal lifecycle consistency in committed work-item manifests.

    This is deliberately a static, repository-local check. It does not verify
    that a PR exists, that a SHA exists in Git, or that a SHA is reachable
    from a target branch.

    Reading is scoped, not global: the top-level `status` is taken only from
    an unindented key, and `status` / `pull_request` / `merge_commit_sha` are
    taken only from direct children of the top-level `implementation` mapping.
    A first-match-wins scan over the whole file would let a nested cell such
    as `status: "FROZEN"` impersonate the lifecycle status; two manifests in
    this repository have exactly that shape.

    Each manifest lands in exactly one of three buckets. `in_scope` items are
    checked. `excluded_by_record_type` items match a registered path and
    record_type pair exactly, and are a different record type living at a
    manifest path, not a manifest with missing fields. `unrecognized` items
    are neither, and are reported by path: not a pass, just not read.

    What this deliberately does NOT check, and why: a full SHA in
    `implementation.merge_commit_sha` is not by itself evidence that
    `implementation.status` must be MERGED. From the manifest alone the same
    pair of fields cannot distinguish an implementation merge from a merged
    registration or measurement package, and at least one work item records
    the latter under `implementation.merge_commit_sha` with an Owner-
    authorised revision entry behind it. Rejecting NOT_STARTED solely because
    a SHA is present would therefore reject a recorded fact, so that rule is
    withdrawn rather than narrowed. A replacement needs an independently
    established field contract, not a stronger guess.
    """
    manifest_paths = sorted(
        path for path in head_paths
        if WORK_ITEM_MANIFEST_RE.fullmatch(path)
    )

    exclusions = load_manifest_schema_registry(root, commit)

    stale = sorted(set(exclusions) - set(manifest_paths))
    if stale:
        raise RuntimeError(
            f"'{MANIFEST_SCHEMA_REGISTRY}' excludes "
            f"{len(stale)} path(s) absent from this commit: "
            + ", ".join(stale)
        )

    violations = []
    in_scope = 0
    excluded = 0
    unrecognized = []

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

        record_type = _top_level_manifest_scalar(lines, "record_type")
        registered = exclusions.get(path)
        if registered is not None and registered == record_type:
            excluded += 1
            continue

        top_status = _top_level_manifest_scalar(lines, "status")
        implementation = _implementation_mapping(lines) or {}
        implementation_status = implementation.get("status")
        implementation_pull_request = implementation.get("pull_request")
        implementation_merge_commit_sha = implementation.get(
            "merge_commit_sha"
        )

        if top_status is None and implementation_status is None:
            unrecognized.append(path)
            continue

        in_scope += 1

        # R20-01: either PR_OPEN lifecycle field requires a positive,
        # unquoted YAML integer in implementation.pull_request.
        if (
            top_status == "PR_OPEN"
            or implementation_status == "PR_OPEN"
        ):
            if (
                implementation_pull_request is None
                or not re.fullmatch(
                    r"[1-9][0-9]*", implementation_pull_request
                )
            ):
                violations.append(
                    "manifest consistency violation: "
                    f"'{path}': PR_OPEN requires pull_request to be "
                    "a positive integer"
                )

        # R20-02: NOT_MERGED cannot coexist with a lifecycle state that
        # asserts implementation has already merged or been verified.
        if implementation_merge_commit_sha == "NOT_MERGED":
            if (
                top_status in {"MERGED", "VERIFIED"}
                or implementation_status == "MERGED"
            ):
                violations.append(
                    "manifest consistency violation: "
                    f"'{path}': merge_commit_sha is NOT_MERGED while "
                    "the lifecycle status asserts merged implementation"
                )

        # R20-03 is withdrawn, not narrowed. See the docstring: a full SHA
        # in implementation.merge_commit_sha does not prove that
        # implementation.status must be MERGED, and this check must not
        # reject NOT_STARTED on the strength of that field alone.

    if len(manifest_paths) != in_scope + excluded + len(unrecognized):
        raise RuntimeError(
            "manifest consistency accounting is broken: "
            f"{len(manifest_paths)} manifests but "
            f"in_scope={in_scope} excluded={excluded} "
            f"unrecognized={len(unrecognized)}"
        )

    print(
        "Work-item manifest consistency "
        f"version={CHECK_VERSION} "
        f"manifests={len(manifest_paths)} "
        f"in_scope={in_scope} "
        f"excluded_by_record_type={excluded} "
        f"unrecognized={len(unrecognized)} "
        f"violations={len(violations)}"
    )

    for path in unrecognized:
        print(
            "Work-item manifest consistency unrecognized shape: "
            f"{path}",
            file=sys.stderr,
        )

    return violations


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="full base commit SHA")
    parser.add_argument("--head", help="full final head commit SHA")
    # The head-tree half -- prohibited paths, INDEX membership, manifest
    # consistency -- is real work that needs no range. New-file admission is
    # the half that cannot run without one. Before this option existed the two
    # were indistinguishable from the outside: a caller that omitted
    # --base/--head received the same "passed" line as a run that had performed
    # admission, so a CI step that had degraded to the head-tree half stayed
    # green (repository-hygiene.yml ran this script twice, once without a
    # range). The weaker half is no longer the default: it has to be named,
    # and an unqualified run is refused rather than downgraded.
    parser.add_argument(
        "--head-tree-only",
        action="store_true",
        help=(
            "run only the checks that need no --base/--head; new-file "
            "admission is reported SKIPPED, never reported as passed"
        ),
    )
    args = parser.parse_args()

    if bool(args.base) != bool(args.head):
        parser.error("--base and --head must be supplied together")

    if args.head_tree_only and (args.base or args.head):
        parser.error(
            "--head-tree-only cannot be combined with --base and --head"
        )

    return args


def main():
    args = parse_args()

    # Refuse an unqualified run before touching the repository. The most this
    # script can say without a range is "admission did not run", and a check
    # that did not run must not report success. Exit 2 is the INCOMPLETE code
    # this script already uses when a condition cannot be determined, so a
    # caller that forgot the range fails closed instead of reading green.
    if not (args.base and args.head) and not args.head_tree_only:
        print(
            "Repository new-file admission SKIPPED "
            "(new-file admission requires --base and --head)."
        )
        error(
            "repository hygiene cannot be determined: "
            "new-file admission requires --base and --head"
        )
        return 2

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
        "Repository hygiene head-tree checks complete "
        f"(version={CHECK_VERSION}). "
        "New-file admission SKIPPED "
        "(new-file admission requires --base and --head)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
