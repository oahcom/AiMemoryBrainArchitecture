"""Read-only GitHub PR Session Evidence Gate.

The validator reads trusted workflow code from the PR base revision and
resolves every evidence file exclusively against the PR head Git tree.
It never checks out or executes PR-head code.

Scope: this gate proves structure only. It proves that the declared fields
exist, that each declared reference resolves to a non-empty regular file in
the PR head tree, and that the recorded byte count and SHA-256 match that
blob. It does not prove that the evidence is truthful, complete or
sufficient, and it does not prove which model produced it. A
``AI-SESSION-EVIDENCE: PRESENT`` verdict means "the files exist and their
bytes are unchanged", nothing more.

Evidence-state vocabulary: an evidence section may instead carry one state
word, and the three states are three distinct claims:

* ``NOT_AVAILABLE``: the platform or interface does not provide the content.
* ``NOT_RECORDED``: the content was obtainable, but was not recorded at the
  time.
* ``REDACTED``: the original content exists, but the repository copy is
  redacted because of sensitive information; the redaction scope and reason
  must be stated.

The gate enforces the enum, and that every state word is accompanied by a
non-empty explanation of what could not be obtained and why. ``REDACTED``
additionally owes its scope and reason; this document records that obligation
but, beyond the same non-emptiness, the gate does not machine-check it. The
gate does not adjudicate which state is factually correct -- only the author
can know whether the platform withheld the content or the author failed to
record it. The three are therefore distinct as claims and indistinguishable
only in that the gate cannot verify the claim. The two spellings
``NOT_AVAILABLE`` and ``NOT_RECORDED`` are kept because the Work Item manifest
already uses them for ``executed_prompt_provenance`` and
``session_reference_status``.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Any


class ValidationError(Exception):
    """A fail-closed validation error."""


# ---------------------------------------------------------------------------
# GitHub API
# ---------------------------------------------------------------------------

_API_ROOT = "https://api.github.com"
_API_VERSION = "2022-11-28"
_TREE_CACHE: dict[tuple[str, str], list[dict]] = {}
_BLOB_CACHE: dict[tuple[str, str, str], str] = {}
_BLOB_BYTES_CACHE: dict[tuple[str, str, str], bytes] = {}


def _request_json(path: str) -> Any:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValidationError("GITHUB_TOKEN is missing")

    url = path if path.startswith("https://") else _API_ROOT + path
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": _API_VERSION,
            "User-Agent": "session-evidence-gate",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ValidationError(
            f"GitHub API HTTP {exc.code}: {url}"
        ) from exc
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise ValidationError(
            f"GitHub API request failed: {url}: {exc}"
        ) from exc


def gh_api(path: str) -> dict:
    """GET a GitHub API endpoint, following Link-header pagination."""
    result = _request_json(path)

    if not isinstance(result, list):
        return result

    items = list(result)
    url = path if path.startswith("https://") else _API_ROOT + path
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValidationError("GITHUB_TOKEN is missing")

    while True:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": _API_VERSION,
                "User-Agent": "session-evidence-gate",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                links = response.headers.get("Link", "")
                next_url = None
                for part in links.split(","):
                    if 'rel="next"' in part:
                        match = re.search(r"<([^>]+)>", part)
                        if match:
                            next_url = match.group(1)
                            break
        except Exception as exc:
            raise ValidationError(
                f"GitHub pagination failed: {exc}"
            ) from exc

        if not next_url:
            break

        page = _request_json(next_url)
        if not isinstance(page, list):
            raise ValidationError(
                "Unexpected paginated GitHub API response"
            )
        items.extend(page)
        url = next_url

    return {"items": items}


def gh_compare_paths(
    repo: str,
    base_sha: str,
    head_sha: str,
) -> set[str]:
    """Return paths added or changed between the PR Base and Head trees.

    GitHub's compare endpoint exposes at most 300 changed files. A response
    at that limit is treated as potentially truncated and therefore fails
    closed. No file-content diff is requested or inspected.
    """
    if not isinstance(base_sha, str) or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}", base_sha
    ):
        raise ValidationError(
            "unable to determine changed paths: PR Base SHA is missing or invalid"
        )

    if not isinstance(head_sha, str) or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}", head_sha
    ):
        raise ValidationError(
            "unable to determine changed paths: PR Head SHA is missing or invalid"
        )

    response = gh_api(
        f"/repos/{repo}/compare/{base_sha}...{head_sha}"
    )

    if not isinstance(response, dict):
        raise ValidationError(
            "unable to determine changed paths: invalid compare response"
        )

    if response.get("truncated"):
        raise ValidationError(
            "unable to determine changed paths: GitHub compare result is truncated"
        )

    files = response.get("files")
    if not isinstance(files, list):
        raise ValidationError(
            "unable to determine changed paths: compare response has no files list"
        )

    if len(files) >= 300:
        raise ValidationError(
            "unable to determine changed paths: compare result reached "
            "the 300-file limit and may be truncated"
        )

    changed = set()
    for item in files:
        if not isinstance(item, dict):
            raise ValidationError(
                "unable to determine changed paths: invalid file entry"
            )

        path = item.get("filename")
        if not isinstance(path, str) or not path:
            raise ValidationError(
                "unable to determine changed paths: file entry has no filename"
            )

        changed.add(path)

    return changed


def gh_tree(repo: str, sha: str) -> list[dict]:
    """Read the recursive Git tree for an exact commit SHA."""
    key = (repo, sha)
    if key in _TREE_CACHE:
        return _TREE_CACHE[key]

    response = gh_api(
        f"/repos/{repo}/git/trees/{sha}?recursive=1"
    )
    tree = response.get("tree")
    if not isinstance(tree, list):
        raise ValidationError(
            f"Git tree unavailable for commit {sha}"
        )

    if response.get("truncated"):
        raise ValidationError(
            f"Git tree for {sha} is truncated; refusing partial validation"
        )

    _TREE_CACHE[key] = tree
    return tree


def gh_blob_bytes(repo: str, sha: str, path: str) -> bytes:
    """Read original bytes from a blob SHA obtained from the PR Head tree.

    The caller must resolve the exact path through gh_tree first and pass
    that tree entry's blob SHA. This function never uses the Contents API.
    """
    key = (repo, sha, path)
    if key in _BLOB_BYTES_CACHE:
        return _BLOB_BYTES_CACHE[key]

    if not isinstance(sha, str) or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}", sha
    ):
        raise ValidationError(
            f"Invalid Git blob SHA for {path}"
        )

    response = gh_api(
        f"/repos/{repo}/git/blobs/{sha}"
    )
    if response.get("encoding") != "base64":
        raise ValidationError(
            f"Unsupported blob encoding: {path}"
        )

    try:
        # The REST API wraps its base64 payload at 60 characters, so the
        # content arrives with newlines in it. Stripping them is not leniency:
        # the alphabet is still validated, and the alternative is that every
        # file larger than one line fails to decode. The fixtures encoded
        # short blobs, which is why this survived a green suite.
        raw = base64.b64decode(
            "".join(response["content"].split()),
            validate=True,
        )
    except (KeyError, ValueError, TypeError) as exc:
        raise ValidationError(
            f"Cannot decode blob bytes: {path}"
        ) from exc

    _BLOB_BYTES_CACHE[key] = raw
    return raw


def gh_blob_text(repo: str, sha: str, path: str) -> str:
    """Read UTF-8 text from a blob SHA obtained from the PR Head tree.

    The caller must resolve the exact path through gh_tree first and pass
    that tree entry's blob SHA. This function never uses the Contents API.
    """
    key = (repo, sha, path)
    if key in _BLOB_CACHE:
        return _BLOB_CACHE[key]

    try:
        result = gh_blob_bytes(repo, sha, path).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(
            f"Cannot decode text blob: {path}"
        ) from exc

    _BLOB_CACHE[key] = result
    return result


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class IssueRecord:
    number: int
    url: str
    created_at: datetime
    body: str
    is_historical: bool


@dataclass
class ValidationContext:
    repo: str
    pr_number: int
    pr: dict
    body: str
    head_sha: str
    tree: list[dict]
    tree_by_path: dict[str, dict]
    effective_at: datetime
    issues: dict[int, IssueRecord]


# ---------------------------------------------------------------------------
# Common parsing
# ---------------------------------------------------------------------------

FIELD_ALIASES = {
    "ai-assisted work": "ai-assisted work",
    "session evidence reference(s)": "session evidence reference(s)",
    "session evidence references": "session evidence reference(s)",
    "related issue(s)": "related issue(s)",
    "related issues": "related issue(s)",
    "owning issue": "related issue(s)",
    # The PR template shipped this spelling; it names the same field.
    "owning issue url": "related issue(s)",
}

# The labels the validator reads. A line carrying one of them starts a new
# field, so it ends the block of the field above it even without a heading:
# the PR template stacks its fields as consecutive "- Label: value" bullets.
FIELD_LABELS = frozenset(
    {
        "work item id",
        "related issue(s)",
        "ai-assisted work",
        "session evidence reference(s)",
        "related pr(s)",
        "session id / prompt id + version + sha-256",
        "accountable owner",
        "implementing session / author",
        "independent reviewer (github login)",
        "integration / acceptance authority",
        "pr-governance-001 status / 标准状态",
    }
)


def _normalise_label(value: str) -> str:
    # A Markdown list marker is presentation, not part of the field name.
    # The repository's own PR template writes every field as "- Label: value".
    value = re.sub(r"^[-*+]\s+", "", value.strip())
    return re.sub(r"\s+", " ", value.lower())


def _field_value_from_lines(
    lines: list[str],
    index: int,
    inline_value: str | None = None,
) -> str:
    """Resolve a field value from its inline text or its following block.

    Both heading and Label: forms use this same value-resolution path. A
    field's value is the whole block of lines after the heading, not just
    its first line: a field may list several references, and every one of
    them has to reach the consumers that validate them one by one. The
    block still stops at the next Markdown heading, at the start of a
    table, or at another labelled field, so it cannot absorb the next
    field; for the same reason a table under a heading is not a field
    value. Interior blank lines are preserved so the caller can split on
    lines; leading and trailing blank lines are dropped.
    """
    if inline_value is not None and inline_value.strip():
        return inline_value.strip()

    block: list[str] = []
    for following in lines[index + 1:]:
        stripped = following.strip()

        if re.fullmatch(r"#{1,6}\s+.*", stripped):
            break

        if stripped.startswith("|"):
            break

        labelled = re.match(r"^\s*([^:]+?)\s*:\s*(.*?)\s*$", stripped)
        if labelled:
            name = _normalise_label(labelled.group(1))
            if FIELD_ALIASES.get(name, name) in FIELD_LABELS:
                break

        block.append(stripped)

    start = 0
    while start < len(block) and not block[start]:
        start += 1

    if start == len(block):
        return ""

    end = len(block)
    while end > start and not block[end - 1]:
        end -= 1

    return "\n".join(block[start:end])


def _extract_field(body: str, label: str) -> str | None:
    """Read either a Markdown heading field or a Label: value field.

    A heading requires whitespace after '#'. Thus '#101' is never
    interpreted as a Markdown heading.
    """
    wanted = FIELD_ALIASES.get(
        _normalise_label(label),
        _normalise_label(label),
    )
    lines = body.splitlines()

    # Heading form: ## Label followed by its value.
    for index, line in enumerate(lines):
        heading = re.fullmatch(
            r"#{1,6}\s+(.+?)\s*#*\s*",
            line.strip(),
        )
        if not heading:
            continue

        heading_label = FIELD_ALIASES.get(
            _normalise_label(heading.group(1)),
            _normalise_label(heading.group(1)),
        )
        if heading_label != wanted:
            continue

        return _field_value_from_lines(
            lines,
            index,
        )

    # Inline form: Label: value
    for index, line in enumerate(lines):
        match = re.match(
            r"^\s*([^:]+?)\s*:\s*(.*?)\s*$",
            line,
        )
        if not match:
            continue

        found = FIELD_ALIASES.get(
            _normalise_label(match.group(1)),
            _normalise_label(match.group(1)),
        )
        if found == wanted:
            return _field_value_from_lines(
                lines,
                index,
                match.group(2),
            )

    return None


def _parse_status(value: str | None, location: str) -> str:
    if value is None:
        raise ValidationError(
            f"{location}: missing AI-assisted work declaration"
        )

    result = value.strip().upper()
    if result not in ("YES", "NO"):
        raise ValidationError(
            f"{location}: AI-assisted work must be YES or NO"
        )
    return result


def _parse_reference_lines(
    value: str | None,
    location: str,
) -> list[str]:
    if value is None:
        raise ValidationError(
            f"{location}: missing Session evidence reference(s)"
        )

    normalised = re.sub(
        r"<br\s*/?>",
        "\n",
        value,
        flags=re.IGNORECASE,
    )
    lines = [
        line.strip().strip("`").strip()
        for line in normalised.splitlines()
        if line.strip()
    ]

    refs = []
    for line in lines:
        line = re.sub(r"^[-*]\s+", "", line).strip()
        if line.startswith("|"):
            line = line.strip("|").strip()

        if line.upper() == "N/A":
            if len(lines) != 1:
                raise ValidationError(
                    f"{location}: N/A cannot be combined with evidence paths"
                )
            return []

        refs.append(line)

    if not refs:
        raise ValidationError(
            f"{location}: no evidence references"
        )

    if len(refs) != len(set(refs)):
        raise ValidationError(
            f"{location}: duplicate evidence references"
        )

    return refs


def _contains_joined_values(value: str) -> bool:
    """Detect forbidden attempts to encode multiple values in one field."""
    if not isinstance(value, str):
        return False
    return bool(re.search(r"[,;+]|\s", value.strip()))


def _check_single_value(value: Any, location: str) -> None:
    if isinstance(value, bool):
        raise ValidationError(
            f"{location}: required single value is missing"
        )

    if isinstance(value, int):
        if value < 0:
            raise ValidationError(
                f"{location}: integer value must be nonnegative"
            )
        return

    if not isinstance(value, str) or not value.strip():
        raise ValidationError(
            f"{location}: required single value is missing"
        )

    if _contains_joined_values(value):
        raise ValidationError(
            f"{location}: joined multi-value field is forbidden; "
            "use separate session_evidence entries"
        )


# ---------------------------------------------------------------------------
# Timestamp and path validation
# ---------------------------------------------------------------------------

def parse_utc_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
        value,
    ):
        raise ValidationError(
            "Effective timestamp must be UTC ISO-8601 ending in Z"
        )

    try:
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%SZ",
        ).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValidationError(
            "Invalid effective UTC timestamp"
        ) from exc


def _parse_api_timestamp(
    value: str,
    location: str,
) -> datetime:
    if not isinstance(value, str):
        raise ValidationError(
            f"{location}: missing created_at"
        )

    try:
        result = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValidationError(
            f"{location}: invalid created_at timestamp"
        ) from exc

    if result.tzinfo is None:
        raise ValidationError(
            f"{location}: created_at must include a timezone"
        )

    return result.astimezone(timezone.utc)


def validate_canonical_evidence_path(
    path: str,
    location: str,
) -> str:
    if not isinstance(path, str) or not path:
        raise ValidationError(
            f"{location}: empty evidence path"
        )

    if path != path.strip():
        raise ValidationError(
            f"{location}: surrounding whitespace in path"
        )

    if "\\" in path:
        raise ValidationError(
            f"{location}: backslash is forbidden"
        )

    if path.startswith("/"):
        raise ValidationError(
            f"{location}: absolute path is forbidden"
        )

    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", path):
        raise ValidationError(
            f"{location}: URL scheme is forbidden"
        )

    if "%" in path:
        raise ValidationError(
            f"{location}: percent encoding is forbidden"
        )

    parts = path.split("/")

    if any(part == "" for part in parts):
        raise ValidationError(
            f"{location}: empty path segment"
        )

    if any(part in (".", "..") for part in parts):
        raise ValidationError(
            f"{location}: dot path segment is forbidden"
        )

    if PurePosixPath(path).is_absolute():
        raise ValidationError(
            f"{location}: absolute POSIX path"
        )

    if path != "/".join(parts):
        raise ValidationError(
            f"{location}: noncanonical path"
        )

    return path


def _tree_index(tree: list[dict]) -> dict[str, dict]:
    result = {}

    for item in tree:
        path = item.get("path")
        if not isinstance(path, str):
            raise ValidationError(
                "Git tree contains an invalid path"
            )

        if path in result:
            raise ValidationError(
                f"Duplicate Git tree path: {path}"
            )

        result[path] = item

    return result


def _validate_regular_file(
    path: str,
    tree_index: dict[str, dict],
    location: str,
) -> dict:
    validate_canonical_evidence_path(path, location)
    item = tree_index.get(path)

    if item is None:
        raise ValidationError(
            f"{location}: path does not exist in PR Head Git tree: {path}"
        )

    if item.get("type") != "blob":
        raise ValidationError(
            f"{location}: target is not a Git blob: {path}"
        )

    if item.get("mode") not in ("100644", "100755"):
        raise ValidationError(
            f"{location}: target is not a regular file "
            f"(mode {item.get('mode')}): {path}"
        )

    if (
        not isinstance(item.get("size"), int)
        or item["size"] <= 0
    ):
        raise ValidationError(
            f"{location}: evidence file is empty: {path}"
        )

    if not isinstance(item.get("sha"), str) or not item["sha"]:
        raise ValidationError(
            f"{location}: missing Git blob SHA: {path}"
        )

    return item


# ---------------------------------------------------------------------------
# Issue references
# ---------------------------------------------------------------------------

def _normalise_issue_reference(
    value: str,
    repo: str,
) -> int:
    value = value.strip()

    if re.fullmatch(r"#\d+", value):
        return int(value[1:])

    expected = re.fullmatch(
        r"https://github\.com/([^/]+)/([^/]+)/issues/(\d+)/?",
        value,
    )
    if not expected:
        raise ValidationError(
            f"Invalid GitHub Issue reference: {value}"
        )

    actual_repo = (
        f"{expected.group(1)}/{expected.group(2)}"
    )
    if actual_repo.lower() != repo.lower():
        raise ValidationError(
            f"Issue reference belongs to another repository: {value}"
        )

    return int(expected.group(3))


def _canonical_issue_url(number: int, repo: str) -> str:
    return f"https://github.com/{repo}/issues/{number}"


def parse_related_issues(
    body: str,
    repo: str,
) -> list[int]:
    field = _extract_field(body, "Related issue(s)")

    if field is None:
        field = _extract_field(body, "Owning Issue")

    if field is None:
        raise ValidationError(
            "PR description: missing Related issue(s)"
        )

    values = re.findall(
        r"https://github\.com/[^/\s]+/[^/\s]+/issues/\d+/?|#\d+",
        field,
    )

    if not values:
        raise ValidationError(
            "PR description: no parseable Related Issues"
        )

    numbers = [
        _normalise_issue_reference(value, repo)
        for value in values
    ]

    if len(numbers) != len(set(numbers)):
        raise ValidationError(
            "PR description: duplicate Related Issue"
        )

    return numbers


def _parse_issue_declaration(
    body: str,
    number: int,
) -> tuple[str, list[str]] | None:
    status_value = _extract_field(
        body,
        "AI-assisted work",
    )
    refs_value = _extract_field(
        body,
        "Session evidence reference(s)",
    )

    if status_value is None and refs_value is None:
        return None

    if status_value is None or refs_value is None:
        raise ValidationError(
            f"Issue #{number}: incomplete AI-assisted work declaration"
        )

    status = _parse_status(
        status_value,
        f"Issue #{number}",
    )
    refs = _parse_reference_lines(
        refs_value,
        f"Issue #{number}",
    )

    if status == "YES" and not refs:
        raise ValidationError(
            f"Issue #{number}: YES requires evidence references"
        )

    if status == "NO" and refs:
        raise ValidationError(
            f"Issue #{number}: NO requires N/A"
        )

    return status, refs


# ---------------------------------------------------------------------------
# PR Issue mapping
# ---------------------------------------------------------------------------

def parse_pr_issue_table(
    body: str,
    repo: str,
) -> dict[int, tuple[str, list[str]]]:
    lines = body.splitlines()
    header_index = None

    for index, line in enumerate(lines):
        if (
            "Related Issue" in line
            and "Issue AI-assisted work" in line
            and "Evidence refs for this Issue" in line
        ):
            header_index = index
            break

    if header_index is None:
        raise ValidationError(
            "PR description: missing per-Issue mapping table"
        )

    result = {}
    index = header_index + 1

    while index < len(lines):
        stripped = lines[index].strip()

        if not stripped.startswith("|"):
            if result:
                break
            index += 1
            continue

        # A table row may continue over multiple physical lines when
        # a cell contains newline-separated evidence paths. Keep joining
        # until the row has its closing pipe delimiter.
        row = stripped
        while not row.rstrip().endswith("|"):
            index += 1
            if index >= len(lines):
                raise ValidationError(
                    "PR mapping table: unterminated table row"
                )

            continuation = lines[index].strip()
            if not continuation:
                continue

            row += "\n" + continuation

        raw_cells = row.split("|")
        if raw_cells and raw_cells[0].strip() == "":
            raw_cells = raw_cells[1:]
        if raw_cells and raw_cells[-1].strip() == "":
            raw_cells = raw_cells[:-1]

        cells = [cell.strip() for cell in raw_cells]

        if len(cells) != 3:
            raise ValidationError(
                "PR mapping table: each row must have exactly three columns"
            )

        if all(
            re.fullmatch(r":?-{3,}:?", cell)
            for cell in cells
        ):
            index += 1
            continue

        issue_cell, status_cell, refs_cell = cells

        try:
            number = _normalise_issue_reference(
                issue_cell,
                repo,
            )
        except ValidationError as exc:
            raise ValidationError(
                f"PR mapping table: invalid Related Issue cell: {issue_cell}"
            ) from exc

        if number in result:
            raise ValidationError(
                f"PR mapping: duplicate row for Issue #{number}"
            )

        status = status_cell.upper()
        if status not in (
            "YES",
            "NO",
            "LEGACY_UNDECLARED",
        ):
            raise ValidationError(
                f"Issue #{number}: invalid mapping status {status}"
            )

        # The third column is this Issue's own reference scope. A cell
        # may contain one path or multiple newline/<br>-separated paths.
        row_refs = _parse_reference_lines(
            refs_cell,
            f"Issue #{number} mapping",
        )

        if status == "YES" and not row_refs:
            raise ValidationError(
                f"Issue #{number}: YES requires evidence references"
            )

        if status in ("NO", "LEGACY_UNDECLARED") and row_refs:
            raise ValidationError(
                f"Issue #{number}: {status} requires N/A"
            )

        result[number] = (status, row_refs)
        index += 1

    if not result:
        raise ValidationError(
            "PR mapping table has no Issue rows"
        )

    return result


# ---------------------------------------------------------------------------
# Manifest parsing
# ---------------------------------------------------------------------------

MANIFEST_FIELDS = (
    "implementing_ai_session",
    "executed_prompt_snapshot_file",
    "executed_prompt_sha256",
    "executed_prompt_bytes",
    "executed_prompt_provenance",
    "session_reference_status",
    "session_evidence_ref",
)

ALLOWED_PROVENANCE = {
    "VERIFIED",
    "NOT_VERIFIED",
    "NOT_AVAILABLE",
}

ALLOWED_SESSION_STATUS = {
    "RECORDED",
    "NOT_AVAILABLE",
    "NOT_RECORDED",
}


def _yaml_scalar(value: str) -> Any:
    value = value.strip()

    if (
        len(value) >= 2
        and value[0] == value[-1]
        and value[0] in ("'", '"')
    ):
        return value[1:-1]

    if value in ("null", "Null", "NULL", "~"):
        return None

    if re.fullmatch(r"\d+", value):
        return int(value)

    return value


def parse_manifest_session_entries(
    manifest: str,
    manifest_path: str,
) -> list[dict]:
    lines = manifest.splitlines()

    if not any(
        re.match(r"^session_evidence\s*:", line)
        for line in lines
    ):
        # Legacy reader: all seven fields must be present together.
        legacy = {}

        for line in lines:
            match = re.match(
                r"^([a-z0-9_]+)\s*:\s*(.*?)\s*$",
                line,
            )
            if match and match.group(1) in MANIFEST_FIELDS:
                legacy[match.group(1)] = _yaml_scalar(
                    match.group(2)
                )

        if not legacy:
            raise ValidationError(
                f"{manifest_path}: no session_evidence entries or legacy fields"
            )

        missing = set(MANIFEST_FIELDS) - set(legacy)
        if missing:
            raise ValidationError(
                f"{manifest_path}: incomplete legacy manifest; missing "
                + ", ".join(sorted(missing))
            )

        entry = {
            "role": "LEGACY",
            "issue_refs": [],
            **legacy,
        }
        _validate_manifest_entry(
            entry,
            manifest_path,
            legacy=True,
        )
        return [entry]

    # New entries and top-level legacy aliases must never become two
    # independently mutable sources of truth.
    top_level_legacy = []
    for line in lines:
        if line.startswith("  ") or line.startswith("\t"):
            continue

        match = re.match(r"^([a-z0-9_]+)\s*:", line)
        if match and match.group(1) in MANIFEST_FIELDS:
            top_level_legacy.append(match.group(1))

    if top_level_legacy:
        raise ValidationError(
            f"{manifest_path}: top-level legacy fields conflict with "
            "session_evidence entries"
        )

    entries = []
    current = None
    in_issue_refs = False

    for line in lines:
        if re.match(r"^session_evidence\s*:", line):
            continue

        start = re.match(
            r"^\s{2}-\s+role\s*:\s*(.*?)\s*$",
            line,
        )
        if start:
            if current is not None:
                entries.append(current)

            current = {
                "role": _yaml_scalar(start.group(1)),
                "issue_refs": [],
            }
            in_issue_refs = False
            continue

        if current is None:
            continue

        issue_start = re.match(
            r"^\s{4}issue_refs\s*:\s*$",
            line,
        )
        if issue_start:
            in_issue_refs = True
            continue

        issue_item = re.match(
            r"^\s{6}-\s*(.*?)\s*$",
            line,
        )
        if issue_item and in_issue_refs:
            current["issue_refs"].append(
                _yaml_scalar(issue_item.group(1))
            )
            continue

        field = re.match(
            r"^\s{4}([a-z0-9_]+)\s*:\s*(.*?)\s*$",
            line,
        )
        if field:
            in_issue_refs = False
            key = field.group(1)

            if key in current:
                raise ValidationError(
                    f"{manifest_path}: duplicate field {key}"
                )

            current[key] = _yaml_scalar(field.group(2))

    if current is not None:
        entries.append(current)

    if not entries:
        raise ValidationError(
            f"{manifest_path}: session_evidence contains no entries"
        )

    for index, entry in enumerate(entries, start=1):
        _validate_manifest_entry(
            entry,
            f"{manifest_path} entry #{index}",
        )

    return entries


def _validate_manifest_entry(
    entry: dict,
    location: str,
    legacy: bool = False,
) -> None:
    required = ("role",) + MANIFEST_FIELDS

    for key in required:
        if key not in entry or entry[key] is None:
            raise ValidationError(
                f"{location}: missing required field {key}"
            )

    if (
        not isinstance(entry["role"], str)
        or not entry["role"].strip()
    ):
        raise ValidationError(
            f"{location}: invalid role"
        )

    refs = entry.get("issue_refs")
    if not isinstance(refs, list):
        raise ValidationError(
            f"{location}: issue_refs must be a list"
        )

    # OD-A3 permits an entry whose evidence is declared at PR scope
    # without attribution to any linked Issue.
    if len(refs) != len(set(refs)):
        raise ValidationError(
            f"{location}: duplicate issue_refs"
        )

    for ref in refs:
        if not isinstance(ref, str):
            raise ValidationError(
                f"{location}: invalid issue_refs value"
            )

    for field in MANIFEST_FIELDS:
        value = entry[field]

        if field == "executed_prompt_bytes":
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or value < 0
            ):
                raise ValidationError(
                    f"{location}: executed_prompt_bytes must be "
                    "a nonnegative integer"
                )
            continue

        if not isinstance(value, str) or not value.strip():
            raise ValidationError(
                f"{location}: invalid {field}"
            )

        _check_single_value(
            value,
            f"{location}.{field}",
        )

    if entry["executed_prompt_provenance"] not in ALLOWED_PROVENANCE:
        raise ValidationError(
            f"{location}: invalid executed_prompt_provenance"
        )

    if entry["session_reference_status"] not in ALLOWED_SESSION_STATUS:
        raise ValidationError(
            f"{location}: invalid session_reference_status"
        )

    digest = entry["executed_prompt_sha256"]
    if not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        raise ValidationError(
            f"{location}: executed_prompt_sha256 must be "
            "64 hexadecimal characters"
        )


# ---------------------------------------------------------------------------
# Evidence document validation
# ---------------------------------------------------------------------------

def _parse_evidence_region(
    text: str,
    heading: str,
    path: str,
) -> None:
    heading_norm = _normalise_label(heading)

    lines = text.splitlines()
    start = None

    for index, line in enumerate(lines):
        match = re.fullmatch(
            r"#{1,6}\s+(.+?)\s*#*\s*",
            line.strip(),
        )
        if not match:
            continue

        found = _normalise_label(match.group(1))
        if found == heading_norm:
            start = index + 1
            break

    if start is None:
        raise ValidationError(
            f"{path}: missing required section {heading}"
        )

    section = []
    for line in lines[start:]:
        if re.fullmatch(r"#{1,6}\s+.*", line.strip()):
            break
        section.append(line)

    content = "\n".join(section).strip()

    if not content:
        raise ValidationError(
            f"{path}: empty section {heading}"
        )

    state_match = re.search(
        r"(?m)^\s*(NOT_AVAILABLE|NOT_RECORDED|REDACTED)\s*$",
        content,
    )

    if state_match:
        state = state_match.group(1)
        explanation = content[state_match.end():].strip()
        if not explanation:
            if state == "REDACTED":
                raise ValidationError(
                    f"{path}: REDACTED requires explanation of scope and reason"
                )
            raise ValidationError(
                f"{path}: {state} requires an explanation of what could "
                "not be obtained and why"
            )
        return

    # Actual recorded content is acceptable. A retrospective summary
    # alone cannot substitute for the input or output section.
    if re.search(
        r"(?i)^\s*(summary|摘要|事后摘要)\s*[:：]",
        content,
    ):
        raise ValidationError(
            f"{path}: summary cannot replace actual {heading}"
        )


def _validate_evidence_document(
    text: str,
    path: str,
) -> None:
    if not isinstance(text, str) or not text.strip():
        raise ValidationError(
            f"{path}: evidence document is empty"
        )

    role_present = bool(
        re.search(
            r"(?im)^#{1,6}\s*(session role|session role / use case|role)\b",
            text,
        )
    )
    if not role_present:
        raise ValidationError(
            f"{path}: missing Session role / use case"
        )

    _parse_evidence_region(
        text,
        "Actual AI input",
        path,
    )
    _parse_evidence_region(
        text,
        "AI-visible output",
        path,
    )


# ---------------------------------------------------------------------------
# Individual requirement checks
# ---------------------------------------------------------------------------

def check_01_pr_fields_and_issue_references(
    ctx: ValidationContext,
) -> list[int]:
    status = _parse_status(
        _extract_field(ctx.body, "AI-assisted work"),
        "PR",
    )
    refs = _parse_reference_lines(
        _extract_field(ctx.body, "Session evidence reference(s)"),
        "PR",
    )

    if status == "YES" and not refs:
        raise ValidationError(
            "PR: YES requires evidence references"
        )

    if status == "NO" and refs:
        raise ValidationError(
            "PR: NO requires N/A"
        )

    return parse_related_issues(
        ctx.body,
        ctx.repo,
    )


def check_02_pr_declaration_and_references(
    ctx: ValidationContext,
) -> tuple[str, list[str]]:
    status = _parse_status(
        _extract_field(ctx.body, "AI-assisted work"),
        "PR",
    )
    refs = _parse_reference_lines(
        _extract_field(ctx.body, "Session evidence reference(s)"),
        "PR",
    )

    # Policy for PR-level YES/NO lives in check_01, which runs first.
    # Duplicating it here made these branches unreachable and gave the
    # same condition two different messages.
    return status, refs


def check_03_issue_policy_declarations(
    ctx: ValidationContext,
    mapping: dict[int, tuple[str, list[str]]],
) -> None:
    for number, issue in ctx.issues.items():
        declared = _parse_issue_declaration(
            issue.body,
            number,
        )
        row_status, row_refs = mapping[number]

        if declared is None:
            if not issue.is_historical:
                raise ValidationError(
                    f"Issue #{number}: policy-effective Issue "
                    "has no declaration"
                )

            if row_status != "LEGACY_UNDECLARED" or row_refs:
                raise ValidationError(
                    f"Issue #{number}: undeclared historical Issue "
                    "must use LEGACY_UNDECLARED and N/A"
                )
            continue

        actual_status, actual_refs = declared

        if row_status == "LEGACY_UNDECLARED":
            raise ValidationError(
                f"Issue #{number}: LEGACY_UNDECLARED is invalid "
                "because the Issue has an explicit declaration"
            )

        if row_status != actual_status:
            raise ValidationError(
                f"Issue #{number}: PR mapping status differs "
                "from Issue declaration"
            )


def check_04_head_tree_evidence_paths(
    ctx: ValidationContext,
    paths: list[str],
) -> None:
    for path in paths:
        _validate_regular_file(
            path,
            ctx.tree_by_path,
            "PR/Issue evidence reference",
        )



def check_06_all_references_individually(
    ctx: ValidationContext,
    paths: list[str],
) -> None:
    """Reject duplicates within one declaration scope only."""
    seen = set()

    for path in paths:
        validate_canonical_evidence_path(
            path,
            "Evidence reference",
        )

        if path in seen:
            raise ValidationError(
                f"Duplicate evidence reference: {path}"
            )

        seen.add(path)

        _validate_regular_file(
            path,
            ctx.tree_by_path,
            "Evidence reference",
        )


def check_09_manifest_and_evidence_entries(
    ctx: ValidationContext,
    manifest_path: str,
    mapping: dict[int, tuple[str, list[str]]],
    pr_paths: list[str],
    changed_paths: set[str] | None = None,
) -> list[dict]:
    manifest_item = _validate_regular_file(
        manifest_path,
        ctx.tree_by_path,
        "Work Item manifest",
    )

    # Resolve the manifest exclusively through the PR Head tree.
    # Pass the resulting blob SHA, not the commit SHA, to gh_blob_text.
    manifest_blob_sha = manifest_item["sha"]
    manifest_text = gh_blob_text(
        ctx.repo,
        manifest_blob_sha,
        manifest_path,
    )

    has_canonical_entries = any(
        re.match(r"^session_evidence\s*:", line)
        for line in manifest_text.splitlines()
    )
    is_legacy_manifest = not has_canonical_entries

    if changed_paths is None:
        changed_paths = set()

    if is_legacy_manifest and manifest_path in changed_paths:
        raise ValidationError(
            f"{manifest_path}: updated manifest must use the canonical "
            "session_evidence entries"
        )

    entries = parse_manifest_session_entries(
        manifest_text,
        manifest_path,
    )

    linked_numbers = set(ctx.issues)
    entry_paths = set()

    # Preserve each Issue row's independently parsed reference list.
    # There is deliberately no fallback to PR-level references.
    issue_paths_by_number = {
        number: list(row[1])
        for number, row in mapping.items()
    }

    entry_issue_numbers: dict[str, set[int]] = {}

    for index, entry in enumerate(entries, start=1):
        location = f"{manifest_path} entry #{index}"

        refs = entry["issue_refs"]
        numbers = set()

        for issue_ref in refs:
            number = _normalise_issue_reference(
                issue_ref,
                ctx.repo,
            )

            if number not in linked_numbers:
                raise ValidationError(
                    f"{location}: issue_refs contains "
                    f"unlinked Issue #{number}"
                )

            numbers.add(number)

        evidence_path = validate_canonical_evidence_path(
            entry["session_evidence_ref"],
            location,
        )

        if evidence_path in entry_paths:
            raise ValidationError(
                f"{location}: duplicate session_evidence_ref "
                f"{evidence_path}"
            )

        entry_paths.add(evidence_path)
        entry_issue_numbers[evidence_path] = numbers

        evidence_item = _validate_regular_file(
            evidence_path,
            ctx.tree_by_path,
            location,
        )

        # Read evidence through the blob SHA resolved from the same
        # PR Head tree, never through a Contents API ref lookup.
        evidence_text = gh_blob_text(
            ctx.repo,
            evidence_item["sha"],
            evidence_path,
        )
        _validate_evidence_document(
            evidence_text,
            evidence_path,
        )

        # OD-A3-r5: canonical session_evidence entries always require
        # strict two-way Issue attribution, whether changed or historical.
        # Only unchanged legacy manifests retain the historical exemption.
        if not is_legacy_manifest:
            for number in numbers:
                row_status, row_paths = mapping[number]

                if row_status != "YES":
                    raise ValidationError(
                        f"{location}: issue_refs Issue #{number} maps to "
                        f"{row_status}; canonical entries require YES"
                    )

                if evidence_path not in set(row_paths):
                    raise ValidationError(
                        f"Issue #{number} path '{evidence_path}': "
                        "manifest entry is not listed in the Issue mapping"
                    )

    # OD-A2 two-way consistency applies to canonical entries. An unchanged
    # legacy manifest is exempt from Issue attribution, but not from its
    # field, file, evidence, prompt-hash, or byte-count validation.
    if not is_legacy_manifest:
        for number, (status, _) in mapping.items():
            row_paths = issue_paths_by_number[number]

            for path in row_paths:
                matches = [
                    entry
                    for entry in entries
                    if entry["session_evidence_ref"] == path
                ]

                if not matches:
                    raise ValidationError(
                        f"Issue #{number} path '{path}': "
                        "mapping has no matching manifest entry issue_refs"
                    )

                if not any(
                    _normalise_issue_reference(ref, ctx.repo) == number
                    for entry in matches
                    for ref in entry["issue_refs"]
                ):
                    raise ValidationError(
                        f"Issue #{number} path '{path}': "
                        "mapping has no matching manifest entry issue_refs"
                    )

    # OD-A3: PR-level references are a separate scope. They may refer
    # to the same path as an Issue row without constituting a duplicate.
    # A PR-only entry may have empty issue_refs.
    for path in pr_paths:
        if path not in entry_paths:
            raise ValidationError(
                f"path '{path}': PR evidence reference has no matching "
                "manifest Session Evidence entry"
            )

    # Every Issue YES mapping must be represented in the manifest for
    # canonical entries. Legacy manifests retain their attribution waiver.
    if not is_legacy_manifest:
        for number, (status, _) in mapping.items():
            if status == "YES" and not issue_paths_by_number[number]:
                raise ValidationError(
                    f"Issue #{number}: YES has no Session Evidence entries"
                )

    return entries


def check_11_prompt_snapshot_hashes(
    ctx: ValidationContext,
    entries: list[dict],
) -> None:
    for index, entry in enumerate(entries, start=1):
        path = validate_canonical_evidence_path(
            entry["executed_prompt_snapshot_file"],
            f"entry #{index} prompt snapshot",
        )

        item = ctx.tree_by_path.get(path)
        if item is None:
            # Prompt snapshots that are not available are governed by
            # provenance/status; a claimed usable digest cannot be verified.
            if (
                entry["executed_prompt_provenance"] == "VERIFIED"
                or entry["session_reference_status"] == "RECORDED"
            ):
                raise ValidationError(
                    f"path '{path}': verified prompt snapshot is missing"
                )
            continue

        _validate_regular_file(
            path,
            ctx.tree_by_path,
            f"entry #{index} prompt snapshot",
        )

        # Hash the original blob bytes, not decoded/re-encoded text.
        raw = gh_blob_bytes(
            ctx.repo,
            item["sha"],
            path,
        )
        actual_hash = hashlib.sha256(raw).hexdigest()
        expected_hash = entry["executed_prompt_sha256"].lower()

        if actual_hash != expected_hash:
            raise ValidationError(
                f"path '{path}': executed_prompt_sha256 mismatch "
                f"in manifest entry #{index}"
            )

        if len(raw) != entry["executed_prompt_bytes"]:
            raise ValidationError(
                f"path '{path}': executed_prompt_bytes mismatch "
                f"in manifest entry #{index}"
            )


# ---------------------------------------------------------------------------
# Context loading and orchestration
# ---------------------------------------------------------------------------

def _manifest_path_from_pr(body: str) -> str:
    match = re.search(
        r"\bAID-\d{4}-\d{3}\b",
        body,
    )
    if not match:
        raise ValidationError(
            "PR description: Work Item ID AID-YYYY-NNN is required"
        )

    return (
        "14-ai-development/work-items/"
        + match.group(0)
        + "/manifest.yaml"
    )


def _changed_paths_for_manifest(
    ctx: ValidationContext,
    manifest_path: str,
) -> set[str] | None:
    base = ctx.pr.get("base") or {}
    base_sha = base.get("sha") if isinstance(base, dict) else None

    if not isinstance(base_sha, str) or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}", base_sha
    ):
        return None

    try:
        return gh_compare_paths(
            ctx.repo,
            base_sha,
            ctx.head_sha,
        )
    except ValidationError as exc:
        message = str(exc)
        if "unable to determine changed paths" in message.lower():
            raise
        raise ValidationError(
            f"unable to determine changed paths for {manifest_path}: {message}"
        ) from exc
    except Exception as exc:
        raise ValidationError(
            f"unable to determine changed paths for {manifest_path}: "
            f"{type(exc).__name__}: {exc}"
        ) from exc


def _check_manifest_entries(
    ctx: ValidationContext,
    manifest_path: str,
    mapping: dict,
    pr_paths: list[str],
) -> None:
    """Run checks 09 and 11, scoping the legacy exemption to unchanged files."""
    changed_paths = _changed_paths_for_manifest(ctx, manifest_path)
    # An unknown base means "everything changed", so no legacy exemption
    # is granted and the canonical structure is required.
    manifest_changed = changed_paths is None or manifest_path in changed_paths
    entries = check_09_manifest_and_evidence_entries(
        ctx,
        manifest_path,
        mapping,
        pr_paths,
        {manifest_path} if manifest_changed else set(),
    )
    check_11_prompt_snapshot_hashes(ctx, entries)


def _load_context() -> ValidationContext:
    repo = os.environ.get(
        "GITHUB_REPOSITORY",
        "",
    ).strip()
    number_text = os.environ.get(
        "PR_NUMBER",
        "",
    ).strip()
    effective_text = os.environ.get(
        "AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC",
        "",
    )

    if not repo or not re.fullmatch(r"[^/]+/[^/]+", repo):
        raise ValidationError(
            "GITHUB_REPOSITORY is missing or invalid"
        )

    if not number_text.isdigit() or int(number_text) <= 0:
        raise ValidationError(
            "PR_NUMBER is missing or invalid"
        )

    effective_at = parse_utc_timestamp(effective_text)
    pr_number = int(number_text)

    pr = gh_api(
        f"/repos/{repo}/pulls/{pr_number}"
    )
    if not isinstance(pr, dict):
        raise ValidationError(
            "GitHub returned an invalid Pull Request"
        )

    body = pr.get("body") or ""
    head = pr.get("head") or {}
    head_sha = head.get("sha")

    if not isinstance(head_sha, str) or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}",
        head_sha,
    ):
        raise ValidationError(
            "PR Head SHA is missing or invalid"
        )

    tree = gh_tree(repo, head_sha)
    tree_index = _tree_index(tree)

    numbers = parse_related_issues(
        body,
        repo,
    )
    issues = {}

    for number in numbers:
        issue = gh_api(
            f"/repos/{repo}/issues/{number}"
        )

        if not isinstance(issue, dict) or issue.get("pull_request"):
            raise ValidationError(
                f"Issue #{number}: reference does not resolve to an Issue"
            )

        created_at = _parse_api_timestamp(
            issue.get("created_at"),
            f"Issue #{number}",
        )

        issues[number] = IssueRecord(
            number=number,
            url=issue.get(
                "html_url",
                _canonical_issue_url(number, repo),
            ),
            created_at=created_at,
            body=issue.get("body") or "",
            is_historical=created_at < effective_at,
        )

    return ValidationContext(
        repo=repo,
        pr_number=pr_number,
        pr=pr,
        body=body,
        head_sha=head_sha,
        tree=tree,
        tree_by_path=tree_index,
        effective_at=effective_at,
        issues=issues,
    )


def _write_summary(verdict: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return

    try:
        with open(path, "a", encoding="utf-8") as stream:
            stream.write(verdict + "\n")
    except OSError as exc:
        print(
            f"MISSING: cannot write GITHUB_STEP_SUMMARY: {exc}"
        )


def _historical_not_applicable(
    ctx: ValidationContext,
) -> bool:
    if not ctx.issues:
        return False

    for issue in ctx.issues.values():
        if not issue.is_historical:
            return False

        if _parse_issue_declaration(
            issue.body,
            issue.number,
        ) is not None:
            return False

    return True


def _validate_reference_scopes(
    ctx: ValidationContext,
    pr_paths: list[str],
    mapping: dict[int, tuple[str, list[str]]],
) -> None:
    """Validate duplicates separately for PR scope and each Issue row.

    A path may legally occur once in the PR declaration and once in one
    or more Issue rows. Reuse across scopes is not a duplicate.
    """
    check_06_all_references_individually(
        ctx,
        pr_paths,
    )

    for _, row_paths in mapping.values():
        check_06_all_references_individually(
            ctx,
            row_paths,
        )


def _run_checks(ctx: ValidationContext) -> str:
    related = check_01_pr_fields_and_issue_references(ctx)
    pr_status, pr_paths = check_02_pr_declaration_and_references(ctx)

    mapping = parse_pr_issue_table(
        ctx.body,
        ctx.repo,
    )

    if set(mapping) != set(related):
        missing = sorted(set(related) - set(mapping))
        extra = sorted(set(mapping) - set(related))
        raise ValidationError(
            "PR mapping Issue set mismatch: "
            f"missing={missing}, extra={extra}"
        )

    check_03_issue_policy_declarations(
        ctx,
        mapping,
    )

    # Historical undeclared Issues are not evidence of NO. The PR's
    # declaration is checked independently and remains in its own scope.
    if _historical_not_applicable(ctx):
        if pr_status == "YES":
            check_04_head_tree_evidence_paths(
                ctx,
                pr_paths,
            )
            _validate_reference_scopes(
                ctx,
                pr_paths,
                mapping,
            )

            manifest_path = _manifest_path_from_pr(
                ctx.body
            )
            _check_manifest_entries(
                ctx,
                manifest_path,
                mapping,
                pr_paths,
            )

        number = min(ctx.issues)
        return (
            "AI-SESSION-EVIDENCE: NOT_APPLICABLE "
            f"(linked issue #{number} predates "
            f"{os.environ['AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC']})"
        )

    # File existence/type checks may operate over the concatenated
    # references because they do not impose cross-scope uniqueness.
    all_paths = list(pr_paths)
    for _, row_paths in mapping.values():
        all_paths.extend(row_paths)

    check_04_head_tree_evidence_paths(
        ctx,
        all_paths,
    )

    # Uniqueness is enforced independently in the PR declaration and
    # each Issue row, never across these separate declaration scopes.
    _validate_reference_scopes(
        ctx,
        pr_paths,
        mapping,
    )


    manifest_path = _manifest_path_from_pr(
        ctx.body
    )
    _check_manifest_entries(
        ctx,
        manifest_path,
        mapping,
        pr_paths,
    )

    return "AI-SESSION-EVIDENCE: PRESENT"
def main(argv: list[str] | None = None) -> int:
    del argv

    _TREE_CACHE.clear()
    _BLOB_CACHE.clear()
    _BLOB_BYTES_CACHE.clear()

    try:
        ctx = _load_context()
        verdict = _run_checks(ctx)
        print(verdict)
        _write_summary(verdict)
        return 0

    except ValidationError as exc:
        message = str(exc)
        print(f"MISSING: {message}")
        _write_summary(
            "AI-SESSION-EVIDENCE: MISSING"
        )
        return 1

    except Exception as exc:
        # Unexpected API or parsing errors fail closed.
        message = (
            f"unexpected validation error: "
            f"{type(exc).__name__}: {exc}"
        )
        print(f"MISSING: {message}")
        _write_summary(
            "AI-SESSION-EVIDENCE: MISSING"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
