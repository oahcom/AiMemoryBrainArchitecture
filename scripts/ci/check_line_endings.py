#!/usr/bin/env python3
"""Reject CRLF line endings in committed blobs Git identifies as text.

The verdict is based exclusively on the committed HEAD tree, never on
working-tree files. Paths are enumerated with ``git ls-tree -r -z HEAD``,
their attributes are obtained from Git, and blob contents are read through
one ``git cat-file --batch`` process.

All committed blobs are considered, regardless of filename or extension.
The effective Git ``text`` attribute determines eligibility: paths whose
value is ``unset`` are skipped; all other values are inspected.
The only exemption mechanism is ``-text`` in ``.gitattributes``.
No path or extension exemption list is maintained by this checker.

Exit codes:
    0: HEAD contains no violations.
    1: One or more CRLF violations were found.
    2: The committed tree or its required Git metadata could not be inspected.
"""

from __future__ import annotations

import subprocess
import sys


class InspectionError(Exception):
    """Raised when the committed tree cannot be inspected completely."""


def error(message: str) -> None:
    """Print a GitHub Actions error annotation."""
    print(f"::error::{message}", file=sys.stderr)


def run_git(args: list[str], *, input_data: bytes | None = None) -> bytes:
    """Run Git and return stdout, failing closed on inspection errors."""
    try:
        result = subprocess.run(
            ["git", *args],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise InspectionError(f"cannot execute git: {exc}") from exc

    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise InspectionError(
            f"git {' '.join(args)} failed"
            + (f": {detail}" if detail else "")
        )

    return result.stdout


def committed_blobs() -> list[tuple[bytes, bytes]]:
    """Return (object ID, path) pairs for blobs in the committed HEAD tree."""
    output = run_git(["ls-tree", "-r", "-z", "HEAD"])
    entries = []

    for record in output.split(b"\0"):
        if not record:
            continue

        try:
            metadata, path = record.split(b"\t", 1)
            mode, object_type, object_id = metadata.split(b" ", 2)
        except ValueError as exc:
            raise InspectionError(
                "git ls-tree returned an invalid tree entry"
            ) from exc

        if object_type != b"blob":
            continue

        entries.append((object_id, path))

    return entries


def attribute_values(
    paths: list[bytes],
    attribute: bytes,
) -> dict[bytes, bytes]:
    """Read one Git attribute for all paths in a single Git invocation."""
    if not paths:
        return {}

    output = run_git(
        ["check-attr", "--stdin", "-z", attribute.decode("ascii")],
        input_data=b"".join(path + b"\0" for path in paths),
    )

    fields = output.split(b"\0")
    if fields and fields[-1] == b"":
        fields.pop()

    if len(fields) % 3:
        raise InspectionError(
            f"git check-attr returned malformed {attribute.decode()} output"
        )

    values: dict[bytes, bytes] = {}

    for index in range(0, len(fields), 3):
        path, name, value = fields[index:index + 3]

        if name != attribute or path not in paths:
            raise InspectionError(
                f"git check-attr returned an unexpected "
                f"{attribute.decode()} attribute record"
            )

        values[path] = value

    if len(values) != len(paths):
        raise InspectionError(
            f"git check-attr omitted {attribute.decode()} attribute results"
        )

    return values


def blob_contents(object_ids: list[bytes]) -> dict[bytes, bytes]:
    """Read all requested blobs through one git cat-file --batch process."""
    if not object_ids:
        return {}

    request = b"".join(object_id + b"\n" for object_id in object_ids)
    output = run_git(["cat-file", "--batch"], input_data=request)

    result: dict[bytes, bytes] = {}
    position = 0

    for expected_id in object_ids:
        header_end = output.find(b"\n", position)
        if header_end < 0:
            raise InspectionError(
                "git cat-file --batch returned an incomplete object header"
            )

        header = output[position:header_end]
        position = header_end + 1

        fields = header.split(b" ")
        if (
            len(fields) != 3
            or fields[0] != expected_id
            or fields[1] != b"blob"
        ):
            raise InspectionError(
                f"git cat-file --batch returned an unexpected object: "
                f"{header!r}"
            )

        try:
            size = int(fields[2])
        except ValueError as exc:
            raise InspectionError(
                "git cat-file --batch returned an invalid object size"
            ) from exc

        if size < 0 or position + size >= len(output):
            raise InspectionError(
                "git cat-file --batch returned incomplete blob contents"
            )

        contents = output[position:position + size]
        position += size

        if output[position:position + 1] != b"\n":
            raise InspectionError(
                "git cat-file --batch returned an invalid blob separator"
            )

        position += 1
        result[expected_id] = contents

    if position != len(output):
        raise InspectionError(
            "git cat-file --batch returned unexpected trailing output"
        )

    return result


def line_count(contents: bytes) -> int:
    """Count logical lines, including a final unterminated line."""
    if not contents:
        return 0

    return contents.count(b"\n") + (
        0 if contents.endswith(b"\n") else 1
    )


def main() -> int:
    try:
        entries = committed_blobs()

        paths = [path for _, path in entries]

        text_attributes = attribute_values(paths, b"text")

        eligible = [
            (object_id, path)
            for object_id, path in entries
            if text_attributes[path] != b"unset"
        ]

        contents_by_id = blob_contents(
            list(dict.fromkeys(object_id for object_id, _ in eligible))
        )

    except InspectionError as exc:
        error(f"line-ending inspection incomplete: {exc}")
        return 2

    violations = 0
    inspected = 0

    for object_id, path in eligible:
        contents = contents_by_id[object_id]
        crlf_count = contents.count(b"\r\n")

        inspected += 1

        if crlf_count == 0:
            continue

        violations += 1
        path_display = path.decode("utf-8", errors="backslashreplace")

        error(
            f"CRLF line endings in committed file '{path_display}': "
            f"{crlf_count} CRLF sequences, "
            f"{line_count(contents)} total lines"
        )

    print(
        f"Line-ending check: {inspected} files inspected, "
        f"{violations} violations."
    )

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
