#!/usr/bin/env python3
"""Small stdlib-only delivery precheck for Rust source files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TOOL_MARKERS = ("executed on", "sandbox", "container id", "session id:")
PAIRS = ("{}", "()", "[]")


def trailing_pollution(path: Path, source: str) -> list[tuple[int, str]]:
    """Find suspicious lines among the last three non-empty source lines."""
    nonempty = [
        (number, line)
        for number, line in enumerate(source.splitlines(), start=1)
        if line.strip()
    ][-3:]
    findings = []
    for number, line in nonempty:
        stripped = line.lstrip()
        lowered = line.casefold()
        marker_match = any(marker in lowered for marker in TOOL_MARKERS)
        malformed_bracket_line = (
            stripped.startswith("[")
            and not stripped.endswith("]")
            and not stripped.startswith("#[")
            and not stripped.startswith("#![")
        )
        if marker_match or malformed_bracket_line:
            findings.append((number, line))
    return findings


def _raw_string_end(source: str, start: int) -> int | None:
    """Return the index after a Rust raw string, or None if no raw opener."""
    match = re.match(r"(?:b)?r(#{0,})\"", source[start:])
    if not match:
        return None
    hashes = match.group(1)
    terminator = '"' + hashes
    end = source.find(terminator, start + len(match.group(0)))
    return len(source) if end < 0 else end + len(terminator)


def _char_literal_end(source: str, start: int) -> int | None:
    """Recognize Rust char literals; do not consume lifetime apostrophes."""
    if start + 2 < len(source) and source[start + 2] == "'":
        return start + 3
    if start + 1 >= len(source) or source[start + 1] != "\\":
        return None
    index = start + 2
    while index < len(source) and source[index] != "\n" and index - start <= 12:
        if source[index] == "'":
            return index + 1
        index += 1
    return None


def delimiter_deltas(source: str) -> dict[str, int]:
    """Count opening-minus-closing delimiters outside strings and comments."""
    counts = {pair[0]: 0 for pair in PAIRS}
    closing = {pair[1]: pair[0] for pair in PAIRS}
    index = 0
    state = "code"
    block_depth = 0

    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""

        if state == "line_comment":
            if char == "\n":
                state = "code"
            index += 1
            continue
        if state == "block_comment":
            if char == "/" and following == "*":
                block_depth += 1
                index += 2
            elif char == "*" and following == "/":
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
            else:
                index += 1
            continue
        if state == "string":
            if char == "\\":
                index += 2
            elif char == '"':
                state = "code"
                index += 1
            else:
                index += 1
            continue

        if char == "/" and following == "/":
            state = "line_comment"
            index += 2
            continue
        if char == "/" and following == "*":
            state = "block_comment"
            block_depth = 1
            index += 2
            continue

        raw_end = _raw_string_end(source, index)
        if raw_end is not None:
            index = raw_end
            continue
        if char == '"':
            state = "string"
            index += 1
            continue
        if char == "'":
            char_end = _char_literal_end(source, index)
            if char_end is not None:
                index = char_end
                continue

        if char in counts:
            counts[char] += 1
        elif char in closing:
            counts[closing[char]] -= 1
        index += 1

    return {
        pair: counts[pair[0]]
        for pair in ("{", "(", "[")
    }


def inspect_tree(root: Path) -> int:
    failed = False
    rust_files = sorted((root / "crates").rglob("*.rs"))
    for path in rust_files:
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(f"{path}: cannot read Rust source: {error}", file=sys.stderr)
            failed = True
            continue

        for line_number, line in trailing_pollution(path, source):
            print(f"{path}:{line_number}:{line}")
            failed = True

        deltas = delimiter_deltas(source)
        nonzero = {key: value for key, value in deltas.items() if value}
        if nonzero:
            names = {"{": "braces", "(": "parentheses", "[": "brackets"}
            detail = ", ".join(f"{names[key]}: {value:+d}" for key, value in nonzero.items())
            print(f"{path}: delimiter imbalance ({detail})")
            failed = True

    if not failed:
        print(f"precheck_delivery: OK ({len(rust_files)} Rust files scanned)")
        return 0
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args()
    return inspect_tree(args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
