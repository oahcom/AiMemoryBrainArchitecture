import unittest

from memory_compiler import (
    StageError, derive, ingest, make_provenance, normalize, sha256_text,
)


class MemoryCompilerContractTests(unittest.TestCase):
    def setUp(self):
        self.a = ingest("event-a", "scope-x", "  alpha   memory ")
        self.b = ingest("event-b", "scope-x", "beta memory")
        self.graph = {self.a.memory_id: self.a, self.b.memory_id: self.b}
        self.parameter_digest = sha256_text("{}")

    def test_ingest_is_deterministic(self):
        self.assertEqual(self.a, ingest("event-a", "scope-x", "  alpha   memory "))

    def test_ingest_fails_closed_on_missing_scope(self):
        with self.assertRaisesRegex(StageError, "MISSING_SCOPE_REF"):
            ingest("event-a", "", "content")

    def test_normalize_is_deterministic_and_retains_digest(self):
        first = normalize(self.a)
        second = normalize(self.a)
        self.assertEqual(first, second)
        self.assertEqual(first.source_digest, self.a.content_digest)
        self.assertEqual(first.normalized_content, "alpha memory")

    def test_validation_rejects_digest_mismatch(self):
        from dataclasses import replace
        with self.assertRaisesRegex(StageError, "CONTENT_DIGEST_MISMATCH"):
            normalize(replace(self.a, content="tampered"))

    def test_derive_identity_is_stable(self):
        items = (normalize(self.a), normalize(self.b))
        one = derive(items, "concat", "1", self.parameter_digest)
        two = derive(items, "concat", "1", self.parameter_digest)
        self.assertEqual(one, two)
        self.assertTrue(one[0].startswith("drv:"))

    def test_derive_rejects_empty_inputs(self):
        with self.assertRaisesRegex(StageError, "DERIVE_REQUIRES_INPUTS"):
            derive((), "concat", "1", self.parameter_digest)

    def test_provenance_resolves_root_sources_and_event_anchors(self):
        record = make_provenance(
            "derived-1", "derivation-1", "concat", "1",
            (self.a.memory_id, self.b.memory_id), self.graph, "scope-x",
            "contract-v1", self.parameter_digest,
        )
        self.assertEqual(record.root_source_memory_ids, ("src:event-a", "src:event-b"))
        self.assertEqual(record.source_event_ids, ("event-a", "event-b"))
        self.assertEqual(record.source_digests, (self.a.content_digest, self.b.content_digest))

    def test_provenance_rejects_missing_parent(self):
        with self.assertRaisesRegex(StageError, "PROVENANCE_MISSING_PARENT"):
            make_provenance(
                "derived-1", "derivation-1", "concat", "1",
                ("absent",), self.graph, "scope-x", "contract-v1",
                self.parameter_digest,
            )

    def test_provenance_rejects_cycles(self):
        from dataclasses import replace
        derived = ingest("event-derived", "scope-x", "derived text")
        derived = replace(derived, derived=True, parent_memory_ids=(derived.memory_id,))
        graph = {derived.memory_id: derived}
        with self.assertRaisesRegex(StageError, "PROVENANCE_CYCLE"):
            make_provenance(
                "derived-2", "derivation-2", "concat", "1",
                (derived.memory_id,), graph, "scope-x", "contract-v1",
                self.parameter_digest,
            )

    def test_provenance_requires_at_least_one_parent(self):
        with self.assertRaisesRegex(StageError, "PROVENANCE_REQUIRES_PARENTS"):
            make_provenance(
                "derived-3", "derivation-3", "concat", "1", (),
                self.graph, "scope-x", "contract-v1", self.parameter_digest,
            )


if __name__ == "__main__":
    unittest.main()
