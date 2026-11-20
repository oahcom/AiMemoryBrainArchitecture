#!/usr/bin/env python3
"""Regression tests for the candidate-only Memory IR prototype.

Synthetic-only. These tests do not establish schema migration, E integration,
B-domain acceptance, canonical commit authority, or production conformance.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "memory_ir_prototype.py"
FIXTURE = HERE / "shadow_corpus_24.json"

spec = importlib.util.spec_from_file_location("memory_ir_prototype", SOURCE)
prototype = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(prototype)


def load_rows():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def compile_rows(rows):
    parsed, parse_diagnostics = prototype.parse_to_ir(rows)
    valid, semantic_diagnostics = prototype.semantic_validate(parsed)
    lowered = prototype.normalize_and_lower(valid)
    return parsed, valid, lowered, parse_diagnostics, semantic_diagnostics


class ShadowCorpusRegressionTests(unittest.TestCase):
    def test_fixture_has_24_synthetic_cases_and_expected_rejections(self):
        rows = load_rows()
        parsed, valid, lowered, parse_diag, semantic_diag = compile_rows(rows)
        self.assertEqual(len(rows), 24)
        self.assertEqual(len(parsed), 22)
        self.assertEqual(len(valid), 21)
        self.assertEqual(len(lowered), 21)
        self.assertEqual(len(parse_diag), 2)
        self.assertEqual(len(semantic_diag), 1)

    def test_same_input_same_version_replays_byte_identically(self):
        rows = load_rows()
        first = compile_rows(rows)
        second = compile_rows(rows)
        self.assertEqual(prototype.digest(first[2]), prototype.digest(second[2]))
        self.assertEqual(first[3:], second[3:])

    def test_every_accepted_node_has_closed_evidence_and_lineage(self):
        _, _, lowered, _, _ = compile_rows(load_rows())
        self.assertTrue(lowered)
        for node in lowered:
            self.assertTrue(node["evidence"])
            evidence = node["evidence"][0]
            self.assertTrue(evidence["source_id"])
            self.assertTrue(evidence["event_id"])
            self.assertTrue(evidence["source_digest"])
            self.assertEqual(len(node["provenance"]["input_digest"]), 64)
            self.assertTrue(node["provenance"]["ruleset_version"])
            self.assertTrue(node["provenance"]["extractor_version"])

    def test_single_source_mutation_invalidates_only_its_node_identity(self):
        rows = load_rows()
        old_ir, _ = prototype.parse_to_ir(rows)
        changed = copy.deepcopy(rows)
        changed_row = next(row for row in changed if row.get("source_id") == "src-003")
        changed_row["confidence"] = 0.99
        new_ir, _ = prototype.parse_to_ir(changed)
        old_ids = {node["evidence"][0]["source_id"]: node["node_id"] for node in old_ir}
        new_ids = {node["evidence"][0]["source_id"]: node["node_id"] for node in new_ir}
        self.assertNotEqual(old_ids["src-003"], new_ids["src-003"])
        for source_id in old_ids.keys() - {"src-003"}:
            self.assertEqual(old_ids[source_id], new_ids[source_id])

    def test_conflicts_are_preserved_for_review_without_winner_selection(self):
        _, _, lowered, _, _ = compile_rows(load_rows())
        pair = [node for node in lowered if node["node_id"] in {
            next(n["node_id"] for n in lowered if n["evidence"][0]["source_id"] == "src-001"),
            next(n["node_id"] for n in lowered if n["evidence"][0]["source_id"] == "src-002"),
        }]
        self.assertEqual(len(pair), 2)
        conflicts = prototype.detect_conflicts(lowered)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["disposition"], "preserve_both_review")
        self.assertEqual({conflicts[0]["left"], conflicts[0]["right"]},
                         {node["node_id"] for node in pair})

    def test_candidate_output_never_claims_canonical_identity(self):
        _, _, lowered, _, _ = compile_rows(load_rows())
        for node in lowered:
            self.assertEqual(node["node_id"].startswith("node-"), True)
            self.assertNotIn("canonical_memory_ref", node)
            self.assertNotIn("fact_id", node)
            self.assertNotIn("claim_id", node)


if __name__ == "__main__":
    unittest.main()
