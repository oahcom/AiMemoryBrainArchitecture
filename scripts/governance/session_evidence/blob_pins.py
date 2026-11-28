"""Fail-closed verification of Git blob identities declared in manifests.

Parser-observed scalar spans are internal metadata. Their coordinates are
half-open Python-str character offsets into the original UTF-8 source text.
They are deliberately not part of the public BlobPin contract.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


class BlobPinError(ValueError):
    """Raised when a declared blob pin cannot be verified."""


class BlobPinErrorReason(str, Enum):
    YAML_PARSE = "yaml_parse"
    MISSING_SIBLING_PATH = "missing_sibling_path"
    INVALID_PATH = "invalid_path"
    INVALID_DIGEST = "invalid_digest"
    INVALID_SOURCE_COMMIT = "invalid_source_commit"
    MISSING_SOURCE_COMMIT = "missing_source_commit"
    INVALID_SOURCE_LIST_ITEM = "invalid_source_list_item"
    DUPLICATE_OR_INVALID_STRUCTURE = "duplicate_or_invalid_structure"


@dataclass(frozen=True)
class BlobPinDiagnostic:
    location: str
    reason: BlobPinErrorReason
    message: str


class _LocatedStr(str):
    """A scalar carrying its parser-observed line and source character span."""

    def __new__(
        cls,
        value: str,
        line: Optional[int] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ):
        instance = super().__new__(cls, value)
        instance.line = line
        instance.start = start
        instance.end = end
        return instance


class _LocatedInt(int):
    """An integer scalar carrying its source span for *_bytes reanchoring."""

    def __new__(
        cls,
        value: int,
        line: Optional[int] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ):
        instance = super().__new__(cls, value)
        instance.line = line
        instance.start = start
        instance.end = end
        return instance


@dataclass(frozen=True)
class BlobPin:
    """One fully bound blob identity declaration."""

    path: str
    digest: str
    algorithm: str
    location: str
    source_commit: Optional[str] = None
    line: Optional[int] = None


@dataclass(frozen=True)
class _PinRecord:
    """Private pin metadata; never exposed through BlobPin."""

    pin: BlobPin
    start: Optional[int]
    end: Optional[int]


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
    """Remove a YAML comment while preserving quoted # characters."""
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


def _split_mapping_pair(value: str) -> tuple[str, str, int]:
    """Return key, stripped value, and value's character offset in value."""
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
            index + 1 == len(value) or value[index + 1].isspace()
        ):
            key = value[:index].strip()
            raw_value_start = index + 1
            while (
                raw_value_start < len(value)
                and value[raw_value_start].isspace()
            ):
                raw_value_start += 1
            raw_end = len(value.rstrip())
            remainder = value[raw_value_start:raw_end]

            if not key:
                raise BlobPinError("empty YAML mapping key")

            return key, remainder, raw_value_start

    raise BlobPinError(f"expected YAML mapping pair, got {value!r}")


def _flow_skip_space(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _flow_quoted_end(text: str, index: int) -> int:
    """Return the index just past a single- or double-quoted token."""
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


def _parse_flow_node(
    text: str,
    index: int,
    line: Optional[int] = None,
    base_offset: int = 0,
):
    """Parse one flow node and propagate its absolute source character base."""
    index = _flow_skip_space(text, index)

    if index >= len(text):
        raise BlobPinError(f"truncated YAML flow collection: {text!r}")

    char = text[index]

    if char == "[":
        return _parse_flow_sequence(text, index, line, base_offset)
    if char == "{":
        return _parse_flow_mapping(text, index, line, base_offset)

    if char in ("'", '"'):
        end = _flow_quoted_end(text, index)
        return (
            _scalar(
                text[index:end],
                line,
                base_offset + index,
                base_offset + end,
            ),
            end,
        )

    start = index
    while index < len(text):
        char = text[index]
        if char in ",]}":
            break
        if char in "[{":
            raise BlobPinError(f"invalid YAML flow scalar: {text!r}")
        index += 1

    raw_end = index
    while raw_end > start and text[raw_end - 1].isspace():
        raw_end -= 1
    while start < raw_end and text[start].isspace():
        start += 1

    raw = text[start:raw_end]
    if not raw:
        raise BlobPinError(f"empty YAML flow scalar: {text!r}")

    return (
        _scalar(
            raw,
            line,
            base_offset + start,
            base_offset + raw_end,
        ),
        index,
    )


def _parse_flow_sequence(
    text: str,
    index: int,
    line=None,
    base_offset: int = 0,
):
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

        item, index = _parse_flow_node(
            text, index, line, base_offset
        )
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


def _parse_flow_mapping(
    text: str,
    index: int,
    line=None,
    base_offset: int = 0,
):
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

        key, index = _parse_flow_key(
            text, index, line, base_offset
        )
        index = _flow_skip_space(text, index)
        value, index = _parse_flow_node(
            text, index, line, base_offset
        )

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


def _parse_flow_key(
    text: str,
    index: int,
    line=None,
    base_offset: int = 0,
):
    index = _flow_skip_space(text, index)
    if index >= len(text):
        raise BlobPinError(
            f"unterminated YAML flow mapping: {text!r}"
        )

    if text[index] in ("'", '"'):
        end = _flow_quoted_end(text, index)
        key = _scalar(
            text[index:end],
            line,
            base_offset + index,
            base_offset + end,
        )
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

    key_end = index
    while key_end > start and text[key_end - 1].isspace():
        key_end -= 1
    while start < key_end and text[start].isspace():
        start += 1
    key = text[start:key_end]

    if not key:
        raise BlobPinError(
            f"empty YAML flow mapping key: {text!r}"
        )
    return key, index + 1


def _parse_flow_collection(
    value: str,
    line=None,
    start: Optional[int] = None,
):
    """Parse a flow collection with recursive absolute-offset propagation."""
    if start is None:
        raise BlobPinError(
            "flow collection source offset is unavailable"
        )

    node, index = _parse_flow_node(value, 0, line, start)
    if _flow_skip_space(value, index) != len(value):
        raise BlobPinError(
            f"trailing content after YAML flow collection: {value!r}"
        )
    if not isinstance(node, (list, dict)):
        raise BlobPinError(
            f"expected YAML flow collection, got {value!r}"
        )
    return node


def _scalar(
    value: str,
    line=None,
    start: Optional[int] = None,
    end: Optional[int] = None,
):
    """Parse a scalar while retaining its exact source token span."""
    leading = len(value) - len(value.lstrip())
    stripped = value.strip()
    if start is not None:
        start += leading
    if end is None and start is not None:
        end = start + len(stripped)

    if not stripped:
        return _LocatedStr("", line, start, end)
    if stripped in ("null", "Null", "NULL", "~"):
        return None
    if stripped in ("true", "True", "TRUE"):
        return True
    if stripped in ("false", "False", "FALSE"):
        return False

    if stripped.startswith('"'):
        if len(stripped) < 2 or not stripped.endswith('"'):
            raise BlobPinError(
                f"unterminated double-quoted scalar: {stripped!r}"
            )
        inner = stripped[1:-1]
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
            if char == "\\":
                if index + 1 >= len(inner):
                    raise BlobPinError(
                        "quoted scalar ends with an incomplete escape"
                    )
                following = inner[index + 1]
                result.append(escapes.get(following, following))
                index += 2
            else:
                result.append(char)
                index += 1
        return _LocatedStr("".join(result), line, start, end)

    if stripped.startswith("'"):
        if len(stripped) < 2 or not stripped.endswith("'"):
            raise BlobPinError(
                f"unterminated single-quoted scalar: {stripped!r}"
            )
        return _LocatedStr(
            stripped[1:-1].replace("''", "'"),
            line,
            start,
            end,
        )

    if stripped.startswith(("[", "{")):
        return _parse_flow_collection(stripped, line, start)

    if re.fullmatch(r"-?[0-9]+", stripped):
        try:
            return _LocatedInt(int(stripped), line, start, end)
        except ValueError:
            pass

    return _LocatedStr(stripped, line, start, end)


def _prepare_lines(source: str):
    """Return (indent, content, line, absolute content start) records."""
    if not isinstance(source, str):
        raise BlobPinError("manifest input must be UTF-8 text")

    result = []
    cursor = 0

    for line_number, original_with_ending in enumerate(
        source.splitlines(keepends=True),
        start=1,
    ):
        original = original_with_ending.rstrip("\r\n")
        leading = len(original) - len(original.lstrip(" "))
        if "\t" in original[:leading]:
            raise BlobPinError(
                f"line {line_number}: tabs are not allowed for indentation"
            )

        stripped = original[leading:]
        content = _strip_comment(stripped)
        if content:
            result.append(
                (leading, content, line_number, cursor + leading)
            )

        cursor += len(original_with_ending)

    # splitlines() returns no record for an empty source and handles a final
    # unterminated line. This explicit fallback is unnecessary for offsets,
    # but keeps the parser's empty-document behavior deterministic.
    return result


def _is_sequence_line(content: str) -> bool:
    return content == "-" or content.startswith("- ")


def _parse_block_scalar(
    lines,
    index: int,
    parent_indent: int,
    folded: bool,
):
    collected = []
    while index < len(lines):
        indent, content, _line, _start = lines[index]
        if indent <= parent_indent:
            break
        collected.append(" " * (indent - parent_indent - 1) + content)
        index += 1
    return (" " if folded else "\n").join(collected), index


def _parse_mapping(lines, index, indent, initial=None):
    result = {} if initial is None else dict(initial)

    while index < len(lines):
        current_indent, content, line_number, content_start = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise BlobPinError(
                f"line {line_number}: unexpected mapping indentation"
            )
        if _is_sequence_line(content):
            break

        key, value_text, value_offset = _split_mapping_pair(content)
        if key in result:
            raise BlobPinError(
                f"line {line_number}: duplicate YAML key {key!r}"
            )

        value_start = content_start + value_offset
        index += 1

        if value_text in ("|", "|-", "|+", ">", ">-", ">+"):
            value, index = _parse_block_scalar(
                lines, index, indent, value_text.startswith(">")
            )
            result[key] = value
            continue

        if value_text:
            result[key] = _scalar(
                value_text,
                line_number,
                value_start,
                value_start + len(value_text),
            )
            continue

        if index < len(lines) and lines[index][0] > indent:
            result[key], index = _parse_node(
                lines, index, lines[index][0]
            )
        else:
            result[key] = {}

    return result, index


def _parse_sequence(lines, index, indent):
    result = []
    block_markers = ("|", "|-", "|+", ">", ">-", ">+")

    while index < len(lines):
        current_indent, content, line_number, content_start = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent or not _is_sequence_line(content):
            break

        remainder_offset = 1
        while (
            remainder_offset < len(content)
            and content[remainder_offset].isspace()
        ):
            remainder_offset += 1
        remainder = content[remainder_offset:]
        remainder = remainder.rstrip()
        remainder_start = content_start + remainder_offset
        index += 1

        if not remainder:
            if index < len(lines) and lines[index][0] > indent:
                item, index = _parse_node(
                    lines, index, lines[index][0]
                )
                result.append(item)
            else:
                result.append(None)
            continue

        if remainder in block_markers:
            item, index = _parse_block_scalar(
                lines, index, indent, remainder.startswith(">")
            )
            result.append(item)
            continue

        if re.match(r"^[^'\"]+:(?:\s+|$)", remainder):
            key, value_text, value_offset = _split_mapping_pair(remainder)
            initial = {}
            value_start = remainder_start + value_offset

            if value_text in block_markers:
                initial[key], index = _parse_block_scalar(
                    lines,
                    index,
                    indent + 2,
                    value_text.startswith(">"),
                )
            elif value_text:
                initial[key] = _scalar(
                    value_text,
                    line_number,
                    value_start,
                    value_start + len(value_text),
                )
            elif (
                index < len(lines)
                and lines[index][0] > indent + 1
            ):
                initial[key], index = _parse_node(
                    lines, index, lines[index][0]
                )
            else:
                initial[key] = {}

            if index < len(lines) and lines[index][0] > indent:
                child_indent = lines[index][0]
                if _is_sequence_line(lines[index][1]):
                    raise BlobPinError(
                        f"line {line_number}: unexpected nested sequence "
                        "in mapping item"
                    )
                item, index = _parse_mapping(
                    lines, index, child_indent, initial
                )
            else:
                item = initial

            result.append(item)
            continue

        result.append(
            _scalar(
                remainder,
                line_number,
                remainder_start,
                remainder_start + len(remainder),
            )
        )

    return result, index


def _parse_node(lines, index, indent):
    if index >= len(lines):
        return {}, index
    current_indent, content, _line, _start = lines[index]
    if current_indent != indent:
        raise BlobPinError("invalid YAML indentation")
    if _is_sequence_line(content):
        return _parse_sequence(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_yaml_subset(source: str):
    lines = _prepare_lines(source)
    if not lines:
        return {}
    if lines[0][0] != 0:
        raise BlobPinError("manifest root must start at indentation zero")
    document, index = _parse_node(lines, 0, 0)
    if index != len(lines):
        raise BlobPinError(
            f"line {lines[index][2]}: unconsumed YAML input"
        )
    if not isinstance(document, dict):
        raise BlobPinError("manifest root must be a mapping")
    return document


def _digest_binding(key: str):
    explicit = _EXPLICIT_BINDINGS.get(key)
    if explicit is not None:
        return explicit
    if key.endswith("_blob"):
        return key[:-5], "sha1"
    if key.endswith("_sha256"):
        return key[:-7] + "_file", "sha256"
    return None


def _valid_digest(value, algorithm):
    if not isinstance(value, str):
        return False
    if algorithm == "sha1":
        return _SHA1_RE.fullmatch(value) is not None
    if algorithm == "sha256":
        return _SHA256_RE.fullmatch(value) is not None
    return False


def _normalise_path(value, location):
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


def _location(parent, key):
    return f"$.{key}" if parent == "$" else f"{parent}.{key}"


def _source_list_digest_span(value):
    """Return the source span of only the SHA child token in path: SHA."""
    if not isinstance(value, _LocatedStr):
        return None, None
    if value.start is None or value.end is None:
        return None, None

    # The supported list scalar is deliberately restricted to a direct
    # literal representation. Escaped/decoded representations cannot be
    # mapped back to child-token offsets without a character map.
    token_start = value.start
    token_end = value.end
    raw = str(value)

    if token_end - token_start < len(raw):
        return None, None

    colon = raw.find(":")
    if colon < 0 or raw.count(":") != 1:
        return None, None

    digest_start = colon + 1
    while digest_start < len(raw) and raw[digest_start].isspace():
        digest_start += 1
    digest_end = len(raw.rstrip())

    if raw[digest_start:digest_end] != raw[digest_start:digest_end].strip():
        return None, None
    if not _SHA1_RE.fullmatch(raw[digest_start:digest_end]):
        return None, None

    # Quoted scalars include their outer quote in start/end. Require the
    # literal source representation to match the decoded value exactly.
    # This rejects escaped or doubled-quote source forms conservatively.
    return token_start + (1 if token_start < token_end else 0) + digest_start, (
        token_start + (1 if token_start < token_end else 0) + digest_end
    )


def _parse_source_list_item(value, location, source_commit):
    if not isinstance(value, str):
        raise BlobPinError(
            f"{location}: expected 'path: 40-hex-Git-blob-SHA'"
        )
    if not isinstance(source_commit, str) or not source_commit:
        raise BlobPinError(f"{location}: no sibling d_source_commit")
    if not _COMMIT_RE.fullmatch(source_commit):
        raise BlobPinError(f"{location}: invalid sibling d_source_commit")
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
    start, end = _source_list_digest_span(value)
    return _PinRecord(
        BlobPin(
            path=path,
            digest=digest_text.lower(),
            algorithm="sha1",
            location=location,
            source_commit=source_commit,
            line=getattr(value, "line", None),
        ),
        start,
        end,
    )


def _collect_pin_records(document):
    records = []
    errors = []

    def record_error(location, reason, exc):
        errors.append(
            BlobPinDiagnostic(location, reason, str(exc))
        )

    def visit(value, location="$", inherited_commit=None):
        if isinstance(value, list):
            for index, item in enumerate(value):
                item_location = f"{location}[{index}]"
                if location.endswith(".d_source_blobs"):
                    try:
                        records.append(
                            _parse_source_list_item(
                                item, item_location, inherited_commit
                            )
                        )
                    except BlobPinError as exc:
                        reason = (
                            BlobPinErrorReason.MISSING_SOURCE_COMMIT
                            if "no sibling d_source_commit" in str(exc)
                            else BlobPinErrorReason.INVALID_SOURCE_LIST_ITEM
                        )
                        record_error(item_location, reason, exc)
                else:
                    visit(item, item_location, inherited_commit)
            return

        if not isinstance(value, dict):
            return

        local_commit = value.get("d_source_commit", inherited_commit)
        for key in value:
            binding = _digest_binding(key)
            if binding is None:
                continue

            path_key, algorithm = binding
            key_location = _location(location, key)
            path_location = _location(location, path_key)
            try:
                if path_key not in value:
                    raise BlobPinError(
                        f"{key_location}: no sibling path {path_key!r}"
                    )
                path = _normalise_path(value[path_key], path_location)
                digest = value[key]
                if not _valid_digest(digest, algorithm):
                    expected = (
                        "40 hexadecimal Git blob SHA-1 characters"
                        if algorithm == "sha1"
                        else "64 hexadecimal SHA-256 characters"
                    )
                    raise BlobPinError(
                        f"{key_location}: invalid digest; expected {expected}"
                    )
                records.append(
                    _PinRecord(
                        BlobPin(
                            path=path,
                            digest=digest.lower(),
                            algorithm=algorithm,
                            location=key_location,
                            source_commit=local_commit,
                            line=getattr(digest, "line", None),
                        ),
                        getattr(digest, "start", None),
                        getattr(digest, "end", None),
                    )
                )
            except BlobPinError as exc:
                message = str(exc)
                if "no sibling path" in message:
                    reason = BlobPinErrorReason.MISSING_SIBLING_PATH
                elif "invalid digest" in message:
                    reason = BlobPinErrorReason.INVALID_DIGEST
                else:
                    reason = BlobPinErrorReason.INVALID_PATH
                record_error(key_location, reason, exc)

        for key, child in value.items():
            if key == "d_source_commit":
                continue
            child_location = _location(location, key)
            child_commit = (
                local_commit if key == "d_source_blobs" else None
            )
            visit(child, child_location, child_commit)

    visit(document)
    return records, errors


def _enumerate_pin_records(source):
    try:
        document = _parse_yaml_subset(source)
    except BlobPinError as exc:
        return [], [
            BlobPinDiagnostic(
                "$", BlobPinErrorReason.YAML_PARSE, str(exc)
            )
        ]
    return _collect_pin_records(document)


def enumerate_blob_pins(source: str) -> list[BlobPin]:
    """Legacy fail-fast pin enumeration."""
    document = _parse_yaml_subset(source)
    records, errors = _collect_pin_records(document)
    if errors:
        raise BlobPinError(errors[0].message)
    return [record.pin for record in records]


def enumerate_blob_pins_with_errors(
    source: str,
) -> tuple[list[BlobPin], list[BlobPinDiagnostic]]:
    """Return every complete pin and all independently detectable errors."""
    records, errors = _enumerate_pin_records(source)
    return [record.pin for record in records], errors


def _validate_tree_entry(path, tree_index, location):
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
        raise BlobPinError(f"{location}: path '{path}' is not a blob")
    if item.get("mode") not in ("100644", "100755"):
        raise BlobPinError(
            f"{location}: path '{path}' is not a regular file"
        )
    if not isinstance(item.get("size"), int) or item["size"] <= 0:
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
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()


def verify_blob_pins(
    source: str,
    tree_index: dict,
    read_blob: Callable[[str, str], bytes],
    source_tree_resolver: Optional[Callable[[str], dict]] = None,
) -> list[BlobPin]:
    """Verify declared pins against original committed blob bytes."""
    pins = enumerate_blob_pins(source)
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
            pin.path, selected_tree, pin.location
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
        if pin.algorithm == "sha1" and pin.digest != tree_sha:
            raise BlobPinError(
                f"{pin.location}: expected {pin.digest}, actual {tree_sha}"
            )
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
