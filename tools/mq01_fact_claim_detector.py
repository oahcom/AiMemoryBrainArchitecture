#!/usr/bin/env python3
"""Executable source-level detector for REQ-07 finding MQ-01.

This is a bounded static check, not a semantic proof or a production acceptance
test. It verifies whether the canonical Rust domain module exposes distinct
public Fact and Claim type declarations.
"""
from __future__ import annotations

import argparse
import re
import sys
import unittest
from pathlib import Path


TYPE_DECL = re.compile(r"\bpub\s+(?:struct|enum|type|trait)\s+(Fact|Claim)\b")


def strip_rust_comments(source: str) -> str:
    """Remove // and nested /* */ comments while preserving line structure."""
    out: list[str] = []
    i = 0
    depth = 0
    line_comment = False
    while i < len(source):
        if line_comment:
            if source[i] == "\n":
                line_comment = False
                out.append("\n")
            else:
                out.append(" ")
            i += 1
            continue
        if depth:
            if source.startswith("/*", i):
                depth += 1
                out.extend("  ")
                i += 2
            elif source.startswith("*/", i):
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if source[i] == "\n" else " ")
                i += 1
            continue
        if source.startswith("//", i):
            line_comment = True
            out.extend("  ")
            i += 2
        elif source.startswith("/*", i):
            depth = 1
            out.extend("  ")
            i += 2
        else:
            out.append(source[i])
            i += 1
    return "".join(out)


def inspect_source(source: str) -> dict[str, object]:
    code = strip_rust_comments(source)
    declared = {match.group(1) for match in TYPE_DECL.finditer(code)}
    return {
        "fact_declared": "Fact" in declared,
        "claim_declared": "Claim" in declared,
        "mq01_detected": "Claim" in declared and "Fact" not in declared,
    }


class DetectorTests(unittest.TestCase):
    def test_claim_without_fact_reproduces_mq01(self) -> None:
        result = inspect_source("pub struct Claim { id: String }")
        self.assertTrue(result["claim_declared"])
        self.assertFalse(result["fact_declared"])
        self.assertTrue(result["mq01_detected"])

    def test_distinct_fact_and_claim_types_clear_detection(self) -> None:
        result = inspect_source(
            "pub struct Fact { id: String }\npub struct Claim { id: String }"
        )
        self.assertTrue(result["fact_declared"])
        self.assertTrue(result["claim_declared"])
        self.assertFalse(result["mq01_detected"])

    def test_fact_mentioned_only_in_comment_does_not_count(self) -> None:
        result = inspect_source(
            "// pub struct Fact { fake: bool }\npub struct Claim { id: String }"
        )
        self.assertFalse(result["fact_declared"])
        self.assertTrue(result["mq01_detected"])

    def test_nested_block_comment_does_not_count(self) -> None:
        result = inspect_source(
            "/* outer /* pub struct Fact {} */ still comment */\n"
            "pub struct Claim { id: String }"
        )
        self.assertFalse(result["fact_declared"])
        self.assertTrue(result["mq01_detected"])

    def test_neither_type_is_not_misreported_as_mq01(self) -> None:
        result = inspect_source("pub struct Memory { id: String }")
        self.assertFalse(result["claim_declared"])
        self.assertFalse(result["mq01_detected"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default="crates/memory-domain/src/lib.rs",
        help="Rust domain source to inspect (default: %(default)s)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the detector's standard-library unit tests",
    )
    args = parser.parse_args()

    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(DetectorTests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            return 1

    path = Path(args.source)
    if not path.is_file():
        print(f"ERROR: source file not found: {path}", file=sys.stderr)
        return 2

    result = inspect_source(path.read_text(encoding="utf-8"))
    print(f"source={path}")
    print(f"fact_type_declared={str(result['fact_declared']).lower()}")
    print(f"claim_type_declared={str(result['claim_declared']).lower()}")
    if not result["claim_declared"]:
        print("MQ-01: INDETERMINATE (no public Claim declaration found)")
        return 2
    if result["mq01_detected"]:
        print("MQ-01: DETECTED — public Claim exists; distinct public Fact type is absent")
    else:
        print("MQ-01: NOT_DETECTED — distinct public Fact and Claim declarations exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
