"""Fail-closed verification of Git blob identities declared in manifests.

This module deliberately has no GitHub or HTTP dependencies. The caller
supplies an indexed commit tree, a blob-byte reader, and, when historical
source pins are present, an exact-commit tree resolver.

Binding rules
-------------

Git SHA-1 fields:
    root_blob                 -> root
    blob                      -> path
    en_mirror_blob            -> en_mirror
    zh_cn_mirror_blob         -> zh_cn_mirror
    reconstructed_root_blob   -> root
    evidence_blob             -> evidence_file

SHA-256 fields:
    prompt_sha256             -> prompt_file
    executed_prompt_sha256    -> executed_prompt_snapshot_file

Other *_blob fields bind to their same-prefix path key.
Other *_sha256 fields bind to their same-prefix *_file key.

Historical list form:
    baseline_and_source_evidence:
      d_source_commit: "<exact commit SHA>"
      d_source_blobs:
        - "path/to/file: <40-hex Git blob SHA>"

Only d_source_blobs has a historical-source exemption. Its sibling
d_source_commit is mandatory and must resolve to a complete commit tree.

A declared pin is never silently skipped. A path-only declaration, a
digest-only declaration, an unresolved path, or a mismatched digest fails.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Callable, Optional


class BlobPinError(ValueError):
    """Raised when a declared blob pin cannot be verified."""


@dataclass(frozen=True)
class BlobPin:
    """One fully bound blob identity declaration."""

    path: str
    digest: str
    algorithm: str
    location: str
    source_commit: Optional[str] = None


# Explicit bindings take precedence over suffix-derived bindings.
_EXPLICIT_BINDINGS = {
    "root_blob": ("root", "sha1"),
    "blob": ("path", "sha1"),
    "en_mirror_blob": ("en_mirror", "sha1"),
    "zh_cn_mirror_blob": ("zh_cn_mirror", "sha1"),
    "reconstructed_root_blob": ("root", "sha1"),
    "evidence_blob": ("evidence_file", "sha1"),
    "prompt_sha256": ("prompt_file", "sha256"),
    "executed_prompt_sha256": (
        "executed_prompt_snapshot_file",
        "sha256",
    ),
}

_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")
_SHA1_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _strip_comment(value: str) -> str:
    """Remove a YAML comment without treating quoted # as a comment."""
    quote = None
    escaped = False

    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue

        if quote == '"' and char == "\\":
            escaped = True
            continue

        if quote is not None:
            if char == quote:
                quote = None
            continue

        if char in ("'", '"'):
            quote = char
        elif char == "#" and (
            index == 0 or value[index - 1].isspace()
        ):
            return value[:index].rstrip()

    return value.rstrip()


def _split_mapping_pair(value: str) -> tuple[str, str]:
    """Split one YAML mapping pair at its first structural colon."""
    quote = None
    escaped = False

    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue

        if quote == '"' and char == "\\":
            escaped = True
            continue

        if quote is not None:
            if char == quote:
                quote = None
            continue

        if char in ("'", '"'):
            quote = char
            continue

        if char == ":" and (
            index + 1 == len(value)
            or value[index + 1].isspace()
        ):
            key = value[:index].strip()
            remainder = value[index + 1:].strip()

            if not key:
                raise BlobPinError("empty YAML mapping key")

            return key, remainder

    raise BlobPinError(
        f"expected YAML mapping pair, got {value!r}"
    )


def _flow_skip_space(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _flow_quoted_end(text: str, index: int) -> int:
    """Return the index just past a quoted flow scalar."""
    quote = text[index]
    cursor = index + 1

    while cursor < len(text):
        char = text[cursor]

        if quote == '"':
            if char == "\\":
                cursor += 2
                continue
            if char == '"':
                return cursor + 1
        else:
            if char == "'":
                if text[cursor + 1:cursor + 2] == "'":
                    cursor += 2
                    continue
                return cursor + 1

        cursor += 1

    raise BlobPinError(
        f"unterminated quoted scalar in flow collection: {text!r}"
    )


def _parse_flow_node(text: str, index: int):
    """Parse one flow node: a collection, a quoted or a plain scalar."""
    index = _flow_skip_space(text, index)

    if index >= len(text):
        raise BlobPinError(
            f"truncated YAML flow collection: {text!r}"
        )

    char = text[index]

    if char == "[":
        return _parse_flow_sequence(text, index)

    if char == "{":
        return _parse_flow_mapping(text, index)

    if char in ("'", '"'):
        end = _flow_quoted_end(text, index)
        return _scalar(text[index:end]), end

    start = index

    while index < len(text):
        char = text[index]

        if char in ",]}":
            break

        if char in "[{":
            raise BlobPinError(
                f"invalid YAML flow scalar: {text!r}"
            )

        index += 1

    raw = text[start:index].strip()

    if not raw:
        raise BlobPinError(f"empty YAML flow scalar: {text!r}")

    return _scalar(raw), index


def _parse_flow_sequence(text: str, index: int):
    result = []
    index += 1

    while True:
        index = _flow_skip_space(text, index)

        if index >= len(text):
            raise BlobPinError(
                f"unterminated YAML flow sequence: {text!r}"
            )

        if text[index] == "]":
            return result, index + 1

        item, index = _parse_flow_node(text, index)
        result.append(item)
        index = _flow_skip_space(text, index)

        if index >= len(text):
            raise BlobPinError(
                f"unterminated YAML flow sequence: {text!r}"
            )

        if text[index] == ",":
            index += 1
            continue

        if text[index] == "]":
            return result, index + 1

        raise BlobPinError(
            f"invalid YAML flow sequence separator: {text!r}"
        )


def _parse_flow_mapping(text: str, index: int):
    result = {}
    index += 1

    while True:
        index = _flow_skip_space(text, index)

        if index >= len(text):
            raise BlobPinError(
                f"unterminated YAML flow mapping: {text!r}"
            )

        if text[index] == "}":
            return result, index + 1

        key, index = _parse_flow_key(text, index)
        index = _flow_skip_space(text, index)
        value, index = _parse_flow_node(text, index)

        if key in result:
            raise BlobPinError(
                f"duplicate key in YAML flow mapping: {key!r}"
            )

        result[key] = value
        index = _flow_skip_space(text, index)

        if index >= len(text):
            raise BlobPinError(
                f"unterminated YAML flow mapping: {text!r}"
            )

        if text[index] == ",":
            index += 1
            continue

        if text[index] == "}":
            return result, index + 1

        raise BlobPinError(
            f"invalid YAML flow mapping separator: {text!r}"
        )


def _parse_flow_key(text: str, index: int):
    index = _flow_skip_space(text, index)

    if index >= len(text):
        raise BlobPinError(
            f"unterminated YAML flow mapping: {text!r}"
        )

    if text[index] in ("'", '"'):
        end = _flow_quoted_end(text, index)
        key = _scalar(text[index:end])
        index = _flow_skip_space(text, end)

        if index >= len(text) or text[index] != ":":
            raise BlobPinError(
                f"expected ':' in YAML flow mapping: {text!r}"
            )

        return key, index + 1

    start = index

    while index < len(text) and text[index] not in ":,{}[]":
        index += 1

    if index >= len(text) or text[index] != ":":
        raise BlobPinError(
            f"expected ':' in YAML flow mapping: {text!r}"
        )

    key = text[start:index].strip()

    if not key:
        raise BlobPinError(
            f"empty YAML flow mapping key: {text!r}"
        )

    return key, index + 1


def _parse_flow_collection(value: str):
    """Parse a YAML flow collection with a tokenizer and recursive descent.

    Standard library only: no third-party YAML runtime is imported. Nested
    collections, single- and double-quoted scalars, and plain scalars are
    supported. Malformed input, duplicate keys and illegal separators fail
    closed; a flow collection is never downgraded to an ordinary string.
    """
    node, index = _parse_flow_node(value, 0)

    if _flow_skip_space(value, index) != len(value):
        raise BlobPinError(
            f"trailing content after YAML flow collection: {value!r}"
        )

    if not isinstance(node, (list, dict)):
        raise BlobPinError(
            f"expected YAML flow collection, got {value!r}"
        )

    return node


def _scalar(value: str):
    """Parse a YAML scalar while preserving embedded colons."""
    value = value.strip()

    if not value:
        return ""

    if value in ("null", "Null", "NULL", "~"):
        return None

    if value in ("true", "True", "TRUE"):
        return True

    if value in ("false", "False", "FALSE"):
        return False

    if value.startswith('"'):
        if len(value) < 2 or not value.endswith('"'):
            raise BlobPinError(
                f"unterminated double-quoted scalar: {value!r}"
            )

        # Decode only YAML's common quoted-string escapes. In particular,
        # do not use unicode_escape: it can corrupt non-ASCII UTF-8 text.
        inner = value[1:-1]
        result = []
        index = 0

        escapes = {
            '"': '"',
            "\\": "\\",
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "0": "\0",
        }

        while index < len(inner):
            char = inner[index]

            if char == "\\" and index + 1 < len(inner):
                following = inner[index + 1]
                result.append(escapes.get(following, following))
                index += 2
            else:
                result.append(char)
                index += 1

        return "".join(result)

    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise BlobPinError(
                f"unterminated single-quoted scalar: {value!r}"
            )

        # YAML single quotes escape an apostrophe by doubling it.
        return value[1:-1].replace("''", "'")

    if value.startswith(("[", "{")):
        return _parse_flow_collection(value)

    if re.fullmatch(r"-?[0-9]+", value):
        try:
            return int(value)
        except ValueError:
            pass

    # Crucially, an unquoted "path: sha" remains one scalar here.
    return value


def _prepare_lines(source: str):
    """Tokenize indentation-based YAML while ignoring blank/comment lines."""
    if not isinstance(source, str):
        raise BlobPinError("manifest input must be UTF-8 text")

    result = []

    for line_number, original in enumerate(
        source.splitlines(),
        start=1,
    ):
        if "\t" in original[:len(original) - len(original.lstrip())]:
            raise BlobPinError(
                f"line {line_number}: tabs are not allowed for indentation"
            )

        stripped = original.lstrip(" ")
        if not stripped:
            continue

        content = _strip_comment(stripped)
        if not content:
            continue

        indent = len(original) - len(stripped)

        result.append((indent, content, line_number))

    return result


def _is_sequence_line(content: str) -> bool:
    return content == "-" or content.startswith("- ")


def _parse_block_scalar(
    lines,
    index: int,
    parent_indent: int,
    folded: bool,
):
    """Consume an indented YAML block scalar as ordinary text."""
    collected = []

    while index < len(lines):
        indent, content, _ = lines[index]

        if indent <= parent_indent:
            break

        collected.append(" " * (indent - parent_indent - 1) + content)
        index += 1

    separator = " " if folded else "\n"
    return separator.join(collected), index


def _parse_mapping(
    lines,
    index: int,
    indent: int,
    initial=None,
):
    """Parse a mapping block, optionally continuing a sequence mapping."""
    result = {} if initial is None else dict(initial)

    while index < len(lines):
        current_indent, content, line_number = lines[index]

        if current_indent < indent:
            break

        if current_indent > indent:
            raise BlobPinError(
                f"line {line_number}: unexpected mapping indentation"
            )

        if _is_sequence_line(content):
            break

        key, value_text = _split_mapping_pair(content)

        if key in result:
            raise BlobPinError(
                f"line {line_number}: duplicate YAML key {key!r}"
            )

        index += 1

        if value_text in ("|", "|-", "|+", ">", ">-", ">+"):
            value, index = _parse_block_scalar(
                lines,
                index,
                indent,
                value_text.startswith(">"),
            )
            result[key] = value
            continue

        if value_text:
            result[key] = _scalar(value_text)
            continue

        if (
            index < len(lines)
            and lines[index][0] > indent
        ):
            child_indent = lines[index][0]
            result[key], index = _parse_node(
                lines,
                index,
                child_indent,
            )
        else:
            result[key] = {}

    return result, index


def _parse_sequence(lines, index: int, indent: int):
    """Parse a sequence, preserving each scalar as exactly one item."""
    result = []

    while index < len(lines):
        current_indent, content, line_number = lines[index]

        if current_indent < indent:
            break

        if current_indent != indent or not _is_sequence_line(content):
            break

        remainder = content[1:].strip()
        index += 1

        if not remainder:
            if (
                index < len(lines)
                and lines[index][0] > indent
            ):
                item, index = _parse_node(
                    lines,
                    index,
                    lines[index][0],
                )
                result.append(item)
            else:
                result.append(None)

            continue

        # Sequence mapping items such as:
        # - root: file.md
        #   root_blob: <sha>
        if re.match(r"^[^'\"]+:\s*", remainder):
            key, value_text = _split_mapping_pair(remainder)

            initial = {}

            if value_text:
                initial[key] = _scalar(value_text)
            elif (
                index < len(lines)
                and lines[index][0] > indent + 1
            ):
                initial[key], index = _parse_node(
                    lines,
                    index,
                    lines[index][0],
                )
            else:
                initial[key] = {}

            if (
                index < len(lines)
                and lines[index][0] > indent
            ):
                child_indent = lines[index][0]

                if _is_sequence_line(lines[index][1]):
                    raise BlobPinError(
                        f"line {line_number}: unexpected nested sequence "
                        "in mapping item"
                    )

                item, index = _parse_mapping(
                    lines,
                    index,
                    child_indent,
                    initial,
                )
            else:
                item = initial

            result.append(item)
            continue

        # This is the critical fix:
        # parse the entire remainder as one scalar. Do not split on ':'.
        # _scalar removes the outer YAML quotes exactly once.
        result.append(_scalar(remainder))

    return result, index


def _parse_node(lines, index: int, indent: int):
    if index >= len(lines):
        return {}, index

    current_indent, content, _ = lines[index]

    if current_indent != indent:
        raise BlobPinError("invalid YAML indentation")

    if _is_sequence_line(content):
        return _parse_sequence(lines, index, indent)

    return _parse_mapping(lines, index, indent)


def _parse_yaml_subset(source: str):
    """Parse the indentation-based YAML subset used by Work Item manifests."""
    lines = _prepare_lines(source)

    if not lines:
        return {}

    if lines[0][0] != 0:
        raise BlobPinError("manifest root must start at indentation zero")

    document, index = _parse_node(lines, 0, 0)

    if index != len(lines):
        line_number = lines[index][2]
        raise BlobPinError(
            f"line {line_number}: unconsumed YAML input"
        )

    if not isinstance(document, dict):
        raise BlobPinError("manifest root must be a mapping")

    return document


def _digest_binding(key: str):
    """Return the exact path key and algorithm for a digest key."""
    explicit = _EXPLICIT_BINDINGS.get(key)

    if explicit is not None:
        return explicit

    if key.endswith("_blob"):
        return key[:-5], "sha1"

    if key.endswith("_sha256"):
        return key[:-7] + "_file", "sha256"

    return None


def _valid_digest(value, algorithm: str) -> bool:
    if not isinstance(value, str):
        return False

    if algorithm == "sha1":
        return _SHA1_RE.fullmatch(value) is not None

    if algorithm == "sha256":
        return _SHA256_RE.fullmatch(value) is not None

    return False


def _normalise_path(value, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise BlobPinError(
            f"{location}: declared pin path must be a non-empty string"
        )

    if value != value.strip():
        raise BlobPinError(
            f"{location}: pin path contains surrounding whitespace"
        )

    if "\\" in value:
        raise BlobPinError(
            f"{location}: pin path must use POSIX separators"
        )

    if value.startswith("/") or value.endswith("/"):
        raise BlobPinError(
            f"{location}: pin path must be repository-relative"
        )

    components = value.split("/")

    if any(component in ("", ".", "..") for component in components):
        raise BlobPinError(
            f"{location}: non-canonical pin path {value!r}"
        )

    return value


def _location(parent: str, key: str) -> str:
    if parent == "$":
        return f"$.{key}"

    return f"{parent}.{key}"


def _parse_source_list_item(
    value,
    location: str,
    source_commit,
) -> BlobPin:
    """Parse exactly one d_source_blobs scalar in path: SHA form."""
    if not isinstance(value, str):
        raise BlobPinError(
            f"{location}: expected 'path: 40-hex-Git-blob-SHA'"
        )

    if not isinstance(source_commit, str) or not source_commit:
        raise BlobPinError(
            f"{location}: no sibling d_source_commit"
        )

    if not _COMMIT_RE.fullmatch(source_commit):
        raise BlobPinError(
            f"{location}: invalid sibling d_source_commit"
        )

    # Split only once. A colon in the path is not a supported repository
    # path representation and will be rejected by canonical-path checking.
    if value.count(":") != 1:
        raise BlobPinError(
            f"{location}: expected 'path: 40-hex-Git-blob-SHA'"
        )

    path_text, digest_text = value.split(":", 1)
    path_text = path_text.strip()
    digest_text = digest_text.strip()

    if not _SHA1_RE.fullmatch(digest_text):
        raise BlobPinError(
            f"{location}: expected 'path: 40-hex-Git-blob-SHA'"
        )

    path = _normalise_path(path_text, location)

    return BlobPin(
        path=path,
        digest=digest_text.lower(),
        algorithm="sha1",
        location=location,
        source_commit=source_commit,
    )


def enumerate_blob_pins(source: str) -> list[BlobPin]:
    """Dynamically enumerate and bind all declared blob digest fields.

    A path/digest pair is required. Recognized path-only declarations are
    rejected, as are digest-only declarations.

    The d_source_blobs sequence is handled separately because each item
    contains both its path and Git SHA in one scalar.
    """
    document = _parse_yaml_subset(source)
    pins = []

    def visit(value, location="$", inherited_commit=None):
        if isinstance(value, list):
            for index, item in enumerate(value):
                item_location = f"{location}[{index}]"

                if location.endswith(".d_source_blobs"):
                    pins.append(
                        _parse_source_list_item(
                            item,
                            item_location,
                            inherited_commit,
                        )
                    )
                else:
                    visit(
                        item,
                        item_location,
                        inherited_commit,
                    )
            return

        if not isinstance(value, dict):
            return

        local_commit = value.get(
            "d_source_commit",
            inherited_commit,
        )

        # Classify the fields in this mapping before binding anything.
        # Both sets are deliberately local to this mapping: a path in a
        # parent, sibling, or nested mapping cannot satisfy a digest here.
        digest_fields = {}
        path_fields = set()

        explicit_path_keys = {
            path_key
            for path_key, _algorithm in _EXPLICIT_BINDINGS.values()
        }

        for key in value:
            binding = _digest_binding(key)

            if binding is not None:
                digest_fields[key] = binding
                path_fields.add(binding[0])

            if key in explicit_path_keys or key.endswith("_file"):
                path_fields.add(key)

        # A mapping becomes a pin declaration only through a digest field.
        # Path-only mappings are ordinary path declarations and are ignored.
        # Digest-only mappings, on the other hand, are malformed pins.
        for key, (path_key, algorithm) in digest_fields.items():
            digest = value[key]
            key_location = _location(location, key)
            path_location = _location(location, path_key)

            if path_key not in value:
                raise BlobPinError(
                    f"{key_location}: no sibling path {path_key!r}"
                )

            path = _normalise_path(
                value[path_key],
                path_location,
            )

            if not _valid_digest(digest, algorithm):
                expected = (
                    "40 hexadecimal Git blob SHA-1 characters"
                    if algorithm == "sha1"
                    else "64 hexadecimal SHA-256 characters"
                )
                raise BlobPinError(
                    f"{key_location}: invalid digest; expected {expected}"
                )

            pins.append(
                BlobPin(
                    path=path,
                    digest=digest.lower(),
                    algorithm=algorithm,
                    location=key_location,
                    source_commit=local_commit,
                )
            )

        # path_fields is intentionally collected even when no digest is
        # present. Such fields are path declarations, not incomplete pins.
        # It must not be used to search outside this mapping for a digest.

        # Recurse after binding the current mapping so nested mappings
        # inherit the correct source commit.
        for key, child in value.items():
            if key == "d_source_commit":
                continue
            child_location = _location(location, key)
            child_commit = local_commit if key == "d_source_blobs" else None
            visit(child, child_location, child_commit)

    visit(document)
    return pins


def _validate_tree_entry(
    path: str,
    tree_index: dict,
    location: str,
):
    """Require an ordinary, non-empty committed Git blob."""
    item = tree_index.get(path)

    if item is None:
        raise BlobPinError(
            f"{location}: path '{path}' is missing from the required commit tree"
        )

    if not isinstance(item, dict):
        raise BlobPinError(
            f"{location}: path '{path}' has an invalid tree entry"
        )

    if item.get("type") != "blob":
        raise BlobPinError(
            f"{location}: path '{path}' is not a blob"
        )

    if item.get("mode") not in ("100644", "100755"):
        raise BlobPinError(
            f"{location}: path '{path}' is not a regular file"
        )

    size = item.get("size")

    if not isinstance(size, int) or size <= 0:
        raise BlobPinError(
            f"{location}: path '{path}' has an invalid or empty blob size"
        )

    tree_sha = item.get("sha")

    if not isinstance(tree_sha, str) or not _SHA1_RE.fullmatch(tree_sha):
        raise BlobPinError(
            f"{location}: path '{path}' has an invalid tree blob SHA"
        )

    return item


def _git_blob_sha1(raw: bytes) -> str:
    header = (
        b"blob "
        + str(len(raw)).encode("ascii")
        + b"\0"
    )

    return hashlib.sha1(header + raw).hexdigest()


def verify_blob_pins(
    source: str,
    tree_index: dict,
    read_blob: Callable[[str, str], bytes],
    source_tree_resolver: Optional[
        Callable[[str], dict]
    ] = None,
) -> list[BlobPin]:
    """Verify all declared pins against committed original bytes.

    Args:
        source:
            UTF-8 manifest text.
        tree_index:
            Path-to-entry index for the exact candidate commit tree.
        read_blob:
            Callback accepting (tree_blob_sha, path) and returning
            the original committed bytes.
        source_tree_resolver:
            Optional callback accepting an exact historical commit SHA
            and returning its complete path-to-entry tree index.

    Returns:
        The verified BlobPin objects, in declaration order.

    Raises:
        BlobPinError:
            On any malformed, missing, unresolvable or mismatched pin.
    """
    pins = enumerate_blob_pins(source)

    # Cache both the resolved tree and original bytes. The cache is scoped
    # to this verification run, so it cannot leak across different heads.
    source_tree_cache = {}
    byte_cache = {}

    verified = []

    for pin in pins:
        selected_tree = tree_index

        if pin.source_commit is not None:
            commit = pin.source_commit.lower()

            if not _COMMIT_RE.fullmatch(commit):
                raise BlobPinError(
                    f"{pin.location}: invalid historical source commit"
                )

            if source_tree_resolver is None:
                raise BlobPinError(
                    f"{pin.location}: historical source commit "
                    f"{commit} cannot be resolved"
                )

            if commit not in source_tree_cache:
                resolved_tree = source_tree_resolver(commit)

                if not isinstance(resolved_tree, dict):
                    raise BlobPinError(
                        f"{pin.location}: historical source tree "
                        f"{commit} is invalid"
                    )

                source_tree_cache[commit] = resolved_tree

            selected_tree = source_tree_cache[commit]

        entry = _validate_tree_entry(
            pin.path,
            selected_tree,
            pin.location,
        )

        tree_sha = entry["sha"].lower()
        cache_key = (tree_sha, pin.path)

        if cache_key not in byte_cache:
            raw = read_blob(tree_sha, pin.path)

            if not isinstance(raw, bytes):
                raise BlobPinError(
                    f"{pin.location}: blob reader did not return bytes"
                )

            byte_cache[cache_key] = raw

        raw = byte_cache[cache_key]

        actual_git_sha = _git_blob_sha1(raw)

        # First identity check: the declared Git SHA must agree with
        # the selected commit tree's path-to-object binding.
        if pin.algorithm == "sha1":
            if pin.digest != tree_sha:
                raise BlobPinError(
                    f"{pin.location}: expected {pin.digest}, "
                    f"actual {tree_sha}"
                )

        # Second identity check: the returned original bytes must actually
        # hash to the Git object selected by the commit tree.
        if actual_git_sha != tree_sha:
            raise BlobPinError(
                f"{pin.location}: committed-byte Git SHA mismatch; "
                f"expected {tree_sha}, actual {actual_git_sha}"
            )

        if pin.algorithm == "sha256":
            actual_sha256 = hashlib.sha256(raw).hexdigest()

            if pin.digest != actual_sha256:
                raise BlobPinError(
                    f"{pin.location}: SHA-256 mismatch; "
                    f"expected {pin.digest}, actual {actual_sha256}"
                )

        verified.append(pin)

    return verified
