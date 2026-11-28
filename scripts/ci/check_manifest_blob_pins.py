# scripts/ci/check_manifest_blob_pins.py
#!/usr/bin/env python3
"""Verify in-scope manifest blob pins against a commit tree or reachable history.

Exit status:
  0 PASS
  1 VIOLATION (a declared reference does not resolve as required)
  2 INCOMPLETE (malformed or ambiguous declaration, or unreadable Git data)
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
RAW_DIFF = re.compile(
    rb"^:[0-7]{6} [0-7]{6} ([0-9a-f]{40}) ([0-9a-f]{40}) "
    rb"([A-Z][0-9]*)\t(.*)$"
)
ZERO40 = "0" * 40
HEX64 = re.compile(r"^[0-9a-f]{64}$")

# AID-2026-296: SHA-256 claims over committed file bytes.
# Qualifier suffixes such as model_blob_sha256_lf remain in scope.
BLOB_SHA256_KEY = re.compile(r"^(?P<base>(?:.*_)?)blob_sha256(?:_[a-z0-9]+)*$")

# Exact, documented exclusions. These are not general-purpose suffix rules.
PROMPT_METADATA_KEYS = {
    "prompt_sha256",
    "prompt_bytes",
    "prompt_original_payload_sha256",
    "prompt_original_payload_bytes",
}
UNDEFINED_BLOB_KEYS = {
    "latest_invariant_source_blob",
    "prior_invariant_source_blob",
    "latest_forget_fence_contract_blob",
    "latest_system_boundaries_blob",
    "latest_context_version_blob",
    "latest_applied_evidence_blob",
}
OUT_OF_SCOPE_FAMILIES = {"gate_a_reconstruction", "d_source_blobs"}

INDEX_PAIRS = (
    ("root", "root_blob"),
    ("en_mirror", "en_mirror_blob"),
    ("zh_cn_mirror", "zh_cn_mirror_blob"),
)
RELATED_PAIRS = (
    ("path", "blob"),
    ("en_mirror", "en_mirror_blob"),
    ("zh_cn_mirror", "zh_cn_mirror_blob"),
)


class Incomplete(Exception):
    """The checker cannot establish a trustworthy result."""


class Violation(Exception):
    """A required candidate-tree path is absent."""


class Git:
    def __init__(self, root: Path):
        self.root = root
        self._history_cache: dict[tuple[str, str], set[str]] = {}
        self._tree_cache: dict[tuple[str, str], str | None] = {}

    def run(self, *args: str) -> bytes:
        try:
            process = subprocess.run(
                ["git", *args],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot execute git: {exc}") from exc

        if process.returncode:
            detail = process.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(
                detail or f"git {' '.join(args)} failed ({process.returncode})"
            )
        return process.stdout

    def resolve_commit(self, revision: str) -> str:
        """Resolve any commit-ish revision to a full, lowercase 40-hex SHA."""
        if not isinstance(revision, str) or not revision.strip():
            raise Incomplete(f"invalid or absent source commit: {revision!r}")

        try:
            resolved = self.run(
                "rev-parse", "--verify", f"{revision}^{{commit}}"
            ).decode("ascii").strip().lower()
        except (Incomplete, UnicodeError) as exc:
            raise Incomplete(
                f"invalid or absent source commit: {revision!r}"
            ) from exc

        if not HEX40.fullmatch(resolved):
            raise Incomplete(
                f"source revision did not resolve to a full commit SHA: "
                f"{revision!r}"
            )
        return resolved

    def tree_blob(self, commit: str, path: str) -> str | None:
        key = (commit, path)
        if key in self._tree_cache:
            return self._tree_cache[key]

        try:
            output = self.run("rev-parse", "--verify", f"{commit}:{path}")
        except Incomplete:
            self._tree_cache[key] = None
            return None

        oid = output.decode("ascii", "replace").strip().lower()
        if not HEX40.fullmatch(oid):
            self._tree_cache[key] = None
            return None

        try:
            kind = self.run("cat-file", "-t", oid).decode().strip()
        except Incomplete:
            raise

        if kind != "blob":
            self._tree_cache[key] = None
            return None

        self._tree_cache[key] = oid
        return oid

    def object_bytes(self, commit: str, path: str) -> bytes:
        resolved = self.resolve_commit(commit)
        spec = f"{resolved}:{path}"
        try:
            process = subprocess.run(
                ["git", "cat-file", "blob", spec],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot execute git cat-file: {exc}") from exc

        if process.returncode:
            raise Violation(f"path is absent from source commit: {path}")
        return process.stdout

    def historical_blobs(self, commit: str, path: str) -> set[str]:
        """Collect blob IDs recorded at this exact path in reachable history."""
        resolved = self.resolve_commit(commit)
        cache_key = (resolved, path)
        if cache_key in self._history_cache:
            return self._history_cache[cache_key]

        raw = self.run(
            "log",
            "--full-history",
            "--format=",
            "--raw",
            "--no-abbrev",
            "-m",
            "--no-renames",
            resolved,
            "--",
            path,
        )

        blobs: set[str] = set()
        for line in raw.splitlines():
            match = RAW_DIFF.match(line)
            if not match:
                continue
            old_oid = match.group(1).decode("ascii").lower()
            new_oid = match.group(2).decode("ascii").lower()
            if old_oid != ZERO40:
                blobs.add(old_oid)
            if new_oid != ZERO40:
                blobs.add(new_oid)

        self._history_cache[cache_key] = blobs
        return blobs


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def as_mapping(value):
    return value if isinstance(value, dict) else {}


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def pointer_token(key):
    return str(key).replace("~", "~0").replace("/", "~1")


def walk_declarations(node, pointer=""):
    """Yield (JSON pointer, field, value, containing mapping)."""
    stack = [(pointer, node)]
    while stack:
        ptr, current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                child = f"{ptr}/{pointer_token(key)}"
                if isinstance(key, str) and BLOB_SHA256_KEY.match(key):
                    yield child, key, value, current
                stack.append((child, value))
        elif isinstance(current, list):
            for index, value in enumerate(current):
                stack.append((f"{ptr}/{index}", value))


def bind_path(container, field):
    """Bind a blob_sha256 declaration to a path in its own mapping."""
    match = BLOB_SHA256_KEY.match(field)
    if not match:
        return None, None

    base = match.group("base").rstrip("_")
    names = [f"{base}_path", f"{base}_file"] if base else []

    for name in names + ["path", "file"]:
        value = container.get(name)
        if nonempty(value):
            return name, value.strip()

    value = container.get(base) if base else None
    if nonempty(value) and (
        "/" in value or re.search(r"\.[A-Za-z0-9]{1,8}$", value)
    ):
        return base, value.strip()

    return None, None


def is_pin_like_key(key) -> bool:
    if not isinstance(key, str):
        return False
    lowered = key.lower()
    return (
        lowered.endswith("_blob")
        or lowered.endswith("_sha256")
        or lowered.endswith("_bytes")
        or lowered in {"blob", "root_blob"}
    )


def discover_manifests(git: Git, commit: str) -> list[str]:
    names = git.run("ls-tree", "-r", "--name-only", commit)
    paths = names.decode("utf-8").splitlines()
    return sorted(
        path for path in paths
        if path.startswith(MANIFEST_ROOT + "/")
        and path.endswith("/manifest.yaml")
    )


class Checker:
    def __init__(self, git: Git, commit: str, verbose: bool = True):
        self.git = git
        self.commit = git.resolve_commit(commit)
        self.verbose = verbose
        self.manifests = 0
        self.pins = 0
        self.ok = 0
        self.mismatch = 0
        self.missing = 0
        self.incomplete = 0
        self.excluded = 0
        self.unbound = 0
        self.problems: list[str] = []

    def incomplete_finding(self, context: str, reason: str):
        self.incomplete += 1
        self.problems.append(f"INCOMPLETE {context}: {reason}")

    def semantic_finding(
        self,
        code: str,
        *,
        manifest: str,
        field: str,
        scope: str,
        locator: str,
        declared,
        actual: str = "",
        reason: str,
        classification: str,
        basis: str,
    ):
        if code == "HISTORICAL_REFERENCE_NOT_FOUND":
            self.mismatch += 1
        elif code == "CURRENT_REFERENCE_MISMATCH":
            if "absent" in reason:
                self.missing += 1
            else:
                self.mismatch += 1

        self.problems.append(
            f'{code} manifest={manifest} pin_id={field} field={field} '
            f'scope={scope} locator={locator} declared="{declared}" '
            f'actual="{actual}" reason="{reason}" '
            f'classification="{classification}" basis="{basis}"'
        )

    def resolve_family(self, doc: dict, family: str, manifest_path: str):
        """Resolve a family from root/nested locations, rejecting conflicts.

        Returns (present, value, source_mapping). Equal duplicate declarations
        are evaluated once. Different duplicate declarations fail closed.
        """
        nested = as_mapping(doc.get("baseline_and_source_evidence"))
        locations = []
        if family in doc:
            locations.append(("top-level", doc[family], doc))
        if family in nested:
            locations.append(("baseline_and_source_evidence", nested[family], nested))

        if not locations:
            return False, None, None

        if len(locations) == 2 and locations[0][1] != locations[1][1]:
            self.incomplete_finding(
                f"manifest={manifest_path}",
                f"conflicting {family} declarations at top level and "
                "baseline_and_source_evidence",
            )
            return True, None, None

        return True, locations[0][1], locations[0][2]

    def resolve_pair(
        self, doc: dict, family: str, path_key: str, digest_key: str,
        manifest_path: str,
    ):
        """Resolve a path/digest pair from either supported mapping."""
        nested = as_mapping(doc.get("baseline_and_source_evidence"))
        top_present = path_key in doc or digest_key in doc
        nested_present = path_key in nested or digest_key in nested

        if not top_present and not nested_present:
            return False, None, None

        top_pair = (doc.get(path_key), doc.get(digest_key))
        nested_pair = (nested.get(path_key), nested.get(digest_key))

        if top_present and nested_present and top_pair != nested_pair:
            self.incomplete_finding(
                f"manifest={manifest_path}",
                f"conflicting {family} declaration for {path_key} "
                "at top level and baseline_and_source_evidence",
            )
            return True, None, None

        source = doc if top_present else nested
        return True, source.get(path_key), source.get(digest_key)

    def check_pin(
        self,
        *,
        manifest: str,
        field: str,
        path,
        declared,
        reference_mode: str = "current",
        algorithm: str = "git",
        source_commit: str | None = None,
        count_pin: bool = True,
    ):
        if declared is None or (isinstance(declared, str) and not declared.strip()):
            return

        if count_pin:
            self.pins += 1

        if not nonempty(path):
            self.incomplete_finding(
                f"{field}",
                f"corresponding exact path is absent for digest {declared!r}",
            )
            return

        if algorithm == "bytes":
            if isinstance(declared, bool) or not isinstance(declared, (int, str)):
                self.incomplete_finding(
                    field, f"invalid byte-count declaration {declared!r}"
                )
                return
        elif not isinstance(declared, str) or not declared.strip():
            self.incomplete_finding(
                field, f"invalid digest declaration {declared!r}"
            )
            return

        if reference_mode == "historical":
            try:
                history = self.git.historical_blobs(self.commit, path)
            except Incomplete as exc:
                self.incomplete_finding(f"{field} path={path}", str(exc))
                return

            if declared.lower() not in history:
                self.semantic_finding(
                    "HISTORICAL_REFERENCE_NOT_FOUND",
                    manifest=manifest,
                    field=field,
                    scope="reachable-history",
                    locator=path,
                    declared=declared,
                    reason=(
                        "path has no reachable blob history"
                        if not history
                        else "declared blob is not recorded at this exact path "
                             "in reachable history"
                    ),
                    classification="historical",
                    basis=self.commit,
                )
                return

            self.ok += 1
            return

        if reference_mode not in {"current", None}:
            self.incomplete_finding(
                field, f"unsupported reference mode {reference_mode!r}"
            )
            return

        try:
            selected_commit = (
                self.git.resolve_commit(source_commit)
                if source_commit is not None
                else self.commit
            )
            if algorithm == "bytes" or algorithm == "sha256":
                data = self.git.object_bytes(selected_commit, path)
                if algorithm == "bytes":
                    actual = str(len(data))
                    expected = str(int(declared))
                else:
                    actual = hashlib.sha256(data).hexdigest()
                    expected = declared.lower()
            elif source_commit is not None:
                data = self.git.object_bytes(selected_commit, path)
                actual = git_blob_sha(data)
                expected = declared.lower()
            else:
                actual_oid = self.git.tree_blob(selected_commit, path)
                if actual_oid is None:
                    self.semantic_finding(
                        "CURRENT_REFERENCE_MISMATCH",
                        manifest=manifest,
                        field=field,
                        scope="candidate-tree",
                        locator=path,
                        declared=declared,
                        reason="path is absent from candidate commit tree",
                        classification="current",
                        basis=selected_commit,
                    )
                    return
                actual = actual_oid
                expected = declared.lower()
        except Violation as exc:
            self.semantic_finding(
                "CURRENT_REFERENCE_MISMATCH",
                manifest=manifest,
                field=field,
                scope="source-commit",
                locator=path,
                declared=declared,
                reason=str(exc),
                classification="current",
                basis=source_commit or self.commit,
            )
            return
        except (Incomplete, ValueError) as exc:
            self.incomplete_finding(f"{field} path={path}", str(exc))
            return

        if actual != expected:
            self.semantic_finding(
                "CURRENT_REFERENCE_MISMATCH",
                manifest=manifest,
                field=field,
                scope="candidate-tree" if source_commit is None else "source-commit",
                locator=path,
                declared=declared,
                actual=actual,
                reason="declared digest or byte count differs from actual content",
                classification="current",
                basis=selected_commit,
            )
        else:
            self.ok += 1

    def check_index_pairs(self, doc: dict, manifest_path: str):
        nested = as_mapping(doc.get("baseline_and_source_evidence"))
        for path_key, digest_key in INDEX_PAIRS:
            present, path, digest = self.resolve_pair(
                doc, "top-level index", path_key, digest_key, manifest_path
            )
            if present and digest is not None:
                self.check_pin(
                    manifest=manifest_path,
                    field=f"index.{path_key}",
                    path=path,
                    declared=digest,
                )

    def check_authored_indexes(self, doc: dict, manifest_path: str):
        present, entries, _ = self.resolve_family(
            doc, "authored_indexes", manifest_path
        )
        if not present or entries is None:
            return
        if not isinstance(entries, list):
            self.incomplete_finding(
                f"manifest={manifest_path}", "authored_indexes is not a list"
            )
            return

        allowed = {key for pair in INDEX_PAIRS for key in pair}
        for index, entry in enumerate(entries):
            context = f"authored_indexes[{index}]"
            if not isinstance(entry, dict):
                self.incomplete_finding(
                    context, "declaration record is not a mapping"
                )
                continue

            found = False
            for path_key, digest_key in INDEX_PAIRS:
                if digest_key in entry:
                    found = True
                    self.check_pin(
                        manifest=manifest_path,
                        field=f"{context}.{path_key}",
                        path=entry.get(path_key),
                        declared=entry.get(digest_key),
                        reference_mode="historical",
                    )
                elif path_key in entry:
                    # A path without its paired digest is not itself a pin.
                    continue

            for key in entry:
                if is_pin_like_key(key) and key not in allowed:
                    self.incomplete_finding(
                        context,
                        f"unrecognized declaration-bearing key {key!r}",
                    )

            if not found and any(is_pin_like_key(key) for key in entry):
                # The key-specific diagnostic above is the authoritative one.
                pass

    def check_related_evidence(self, doc: dict, manifest_path: str):
        present, entries, _ = self.resolve_family(
            doc, "related_evidence", manifest_path
        )
        if not present or entries is None:
            return
        if not isinstance(entries, list):
            self.incomplete_finding(
                f"manifest={manifest_path}", "related_evidence is not a list"
            )
            return

        allowed = {key for pair in RELATED_PAIRS for key in pair}
        allowed.add("reference_mode")

        for index, entry in enumerate(entries):
            context = f"related_evidence[{index}]"
            if not isinstance(entry, dict):
                self.incomplete_finding(
                    context, "declaration record is not a mapping"
                )
                continue

            declared_pairs = [
                (path_key, digest_key)
                for path_key, digest_key in RELATED_PAIRS
                if digest_key in entry
            ]

            mode = entry.get("reference_mode")
            if mode not in {"historical", "current"}:
                # Count the declared pins even though they cannot be evaluated.
                self.pins += sum(
                    1 for _, digest_key in declared_pairs
                    if entry.get(digest_key) is not None
                    and not (
                        isinstance(entry.get(digest_key), str)
                        and not entry[digest_key].strip()
                    )
                )
                self.mismatch += 1
                self.problems.append(
                    f"REFERENCE_MODE_MISSING_OR_INVALID manifest={manifest_path} "
                    f"pin_id={context} field={context} scope=related_evidence "
                    f"locator=reference_mode declared={mode!r} actual=\"\" "
                    "reason=\"reference_mode must be historical or current\" "
                    "classification=\"policy\" basis=\"manifest\""
                )
                continue

            for path_key, digest_key in declared_pairs:
                self.check_pin(
                    manifest=manifest_path,
                    field=f"{context}.{path_key}",
                    path=entry.get(path_key),
                    declared=entry.get(digest_key),
                    reference_mode=mode,
                )

            for key in entry:
                if is_pin_like_key(key) and key not in allowed:
                    self.incomplete_finding(
                        context,
                        f"unrecognized declaration-bearing key {key!r}",
                    )

    def check_evidence_blob(self, doc: dict, manifest_path: str):
        nested = as_mapping(doc.get("baseline_and_source_evidence"))
        top_present = "evidence_blob" in doc or "evidence_file" in doc
        nested_present = "evidence_blob" in nested or "evidence_file" in nested
        if not top_present and not nested_present:
            return

        top_pair = (doc.get("evidence_file"), doc.get("evidence_blob"))
        nested_pair = (nested.get("evidence_file"), nested.get("evidence_blob"))
        if top_present and nested_present and top_pair != nested_pair:
            self.incomplete_finding(
                f"manifest={manifest_path}",
                "conflicting evidence_file/evidence_blob declarations",
            )
            return

        source = doc if top_present else nested
        if "evidence_blob" not in source:
            self.incomplete_finding(
                f"manifest={manifest_path}",
                "evidence_file is present without evidence_blob",
            )
            return

        self.check_pin(
            manifest=manifest_path,
            field="evidence_file",
            path=source.get("evidence_file"),
            declared=source.get("evidence_blob"),
        )

    def check_known_exclusions(self, doc: dict, manifest_path: str):
        nested = as_mapping(doc.get("baseline_and_source_evidence"))

        # Exact legacy prompt metadata keys are deliberately outside this gate.
        # Session Evidence check 11 remains authoritative for prompt snapshots.
        for container in (doc, nested):
            self.excluded += sum(1 for key in container if key in PROMPT_METADATA_KEYS)
            self.excluded += sum(1 for key in container if key in UNDEFINED_BLOB_KEYS)

        # These two families are known, explicitly out of scope, and are not
        # interpreted or resolved by AID-336.
        for family in OUT_OF_SCOPE_FAMILIES:
            present, value, _ = self.resolve_family(doc, family, manifest_path)
            if present and value is not None:
                if isinstance(value, list):
                    self.excluded += len(value)
                else:
                    self.excluded += 1

        # Reject unknown declaration-bearing keys at the manifest mapping
        # levels. Exact exclusions above are the only silent exceptions.
        known = (
            PROMPT_METADATA_KEYS
            | UNDEFINED_BLOB_KEYS
            | OUT_OF_SCOPE_FAMILIES
            | {
                "root_blob", "en_mirror_blob", "zh_cn_mirror_blob",
                "evidence_blob", "authored_indexes", "related_evidence",
                "baseline_and_source_evidence", "d_source_blobs",
                "gate_a_reconstruction", "executed_prompt_sha256",
                "executed_prompt_bytes",
            }
        )
        for container_name, container in (
            ("manifest", doc),
            ("baseline_and_source_evidence", nested),
        ):
            for key in container:
                if (
                    is_pin_like_key(key)
                    and key not in known
                    and not (
                        isinstance(key, str)
                        and BLOB_SHA256_KEY.match(key)
                    )
                ):
                    self.incomplete_finding(
                        f"manifest={manifest_path}",
                        f"unrecognized declaration-bearing key "
                        f"{container_name}.{key}",
                    )

    def check_blob_sha256(self, doc: dict, manifest_path: str):
        """Check every in-scope blob_sha256 declaration in the manifest."""
        for pointer, field, declared, container in walk_declarations(doc):
            if declared is None or (
                isinstance(declared, str) and not declared.strip()
            ):
                continue

            self.pins += 1

            if not isinstance(declared, str):
                self.incomplete_finding(
                    f"blob_sha256 manifest={manifest_path} pointer={pointer}",
                    f"invalid digest declaration {declared!r}",
                )
                continue

            declared = declared.strip()
            if not HEX64.fullmatch(declared.lower()):
                self.incomplete_finding(
                    f"blob_sha256 manifest={manifest_path} pointer={pointer}",
                    f"invalid SHA-256 digest declaration {declared!r}",
                )
                continue

            _, path = bind_path(container, field)
            if not path:
                self.unbound += 1
                self.problems.append(
                    f"UNBOUND_BLOB_SHA256 manifest={manifest_path} "
                    f"pointer={pointer} field={field} declared={declared}"
                )
                continue

            try:
                data = self.git.object_bytes(self.commit, path)
            except Violation:
                self.missing += 1
                self.problems.append(
                    f"PATH_MISSING blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} path={path} declared={declared}"
                )
                continue
            except Incomplete as exc:
                self.incomplete_finding(
                    f"blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} path={path}",
                    str(exc),
                )
                continue

            actual = hashlib.sha256(data).hexdigest()
            if actual != declared.lower():
                self.mismatch += 1
                self.problems.append(
                    f"MISMATCH blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} path={path} declared={declared} "
                    f"actual={actual}"
                )
            else:
                self.ok += 1

    def run(self):
        paths = discover_manifests(self.git, self.commit)
        if not paths:
            raise Incomplete(f"no manifests found in commit {self.commit}")

        self.manifests = len(paths)
        for manifest_path in paths:
            try:
                raw = self.git.object_bytes(self.commit, manifest_path)
                document = yaml.safe_load(raw.decode("utf-8"))
            except (UnicodeError, yaml.YAMLError, Incomplete, Violation) as exc:
                self.incomplete_finding(f"manifest={manifest_path}", str(exc))
                continue

            if not isinstance(document, dict):
                self.incomplete_finding(
                    f"manifest={manifest_path}",
                    "top-level YAML is not a mapping",
                )
                continue

            self.check_known_exclusions(document, manifest_path)
            self.check_index_pairs(document, manifest_path)
            self.check_authored_indexes(document, manifest_path)
            self.check_related_evidence(document, manifest_path)
            self.check_evidence_blob(document, manifest_path)
            self.check_blob_sha256(document, manifest_path)

        if self.verbose:
            print(
                f"main={self.commit} manifests={self.manifests} "
                f"pins={self.pins} ok={self.ok} mismatch={self.mismatch} "
                f"path_missing={self.missing} incomplete={self.incomplete} "
                f"excluded={self.excluded} unbound={self.unbound}"
            )
            for problem in self.problems:
                print(problem)

        if self.incomplete:
            return 2
        if self.mismatch or self.missing or self.unbound:
            return 1
        return 0


def verify(root: Path, commit: str, verbose: bool = True):
    git = Git(root)
    checker = Checker(git, commit, verbose=verbose)
    return checker.run()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args(argv)

    try:
        git = Git(args.root)
        commit = git.resolve_commit(args.commit)
        return verify(args.root, commit)
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
