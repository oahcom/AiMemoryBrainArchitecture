"""Offline adversarial tests for Issue #1350 blob-pin integrity."""

import hashlib
import unittest

from scripts.governance.session_evidence.blob_pins import (
    BlobPinError,
    enumerate_blob_pins,
    verify_blob_pins,
)


def git_blob_sha(raw):
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()


def make_entry(raw):
    return {
        "type": "blob",
        "mode": "100644",
        "size": len(raw),
        "sha": git_blob_sha(raw),
    }


class BlobPinContractTests(unittest.TestCase):

    def setUp(self):
        self.raw = b"committed evidence bytes\n"
        self.sha = git_blob_sha(self.raw)
        self.tree = {
            "docs/evidence.md": make_entry(self.raw),
        }
        self.calls = []

    def reader(self, sha, path):
        self.calls.append((sha, path))
        if sha != self.sha:
            raise AssertionError("reader received an unexpected blob SHA")
        return self.raw

    def verify(self, manifest, tree=None, reader=None):
        return verify_blob_pins(
            manifest,
            self.tree if tree is None else tree,
            self.reader if reader is None else reader,
        )

    def test_path_and_digest_are_accepted_without_noise(self):
        """Mutation: removing byte verification must invalidate the test."""
        manifest = (
            'evidence_file: "docs/evidence.md"\n'
            f'evidence_blob: "{self.sha}"\n'
        )
        result = self.verify(manifest)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].path, "docs/evidence.md")
        self.assertEqual(self.calls, [(self.sha, "docs/evidence.md")])

    def test_digest_only_is_rejected_with_missing_path(self):
        """Mutation: accepting a digest without its path must fail."""
        manifest = f'root_blob: "{self.sha}"\n'
        with self.assertRaisesRegex(
            BlobPinError, "no sibling path 'root'"
        ):
            self.verify(manifest)

    def test_path_only_is_not_a_pin_contract_change(self):
        """C1 contract change: path-only declarations are not pins."""
        manifest = 'evidence_file: "docs/evidence.md"\n'
        result = self.verify(manifest)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
        self.assertEqual(self.calls, [])

    def test_declared_exception_path_only_is_not_a_pin(self):
        """Path-only exception records use the same structural rule."""
        manifest = (
            "declared_exceptions:\n"
            '  - path: "docs/evidence.md"\n'
        )
        result = self.verify(manifest)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
        self.assertEqual(self.calls, [])

    def test_path_and_digest_in_different_sibling_mappings_do_not_bind(self):
        """A path in another mapping cannot satisfy a digest."""
        manifest = (
            "first:\n"
            '  evidence_file: "docs/evidence.md"\n'
            "second:\n"
            f'  evidence_blob: "{self.sha}"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            r"\$\.second\.evidence_blob: no sibling path 'evidence_file'",
        ):
            self.verify(manifest)

    def test_parent_path_does_not_bind_nested_digest(self):
        """A parent mapping's path cannot satisfy a nested digest."""
        manifest = (
            'root: "docs/evidence.md"\n'
            "child:\n"
            f'  root_blob: "{self.sha}"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            r"\$\.child\.root_blob: no sibling path 'root'",
        ):
            self.verify(manifest)

    def test_nested_path_does_not_bind_parent_digest(self):
        """A nested mapping's path cannot satisfy a parent digest."""
        manifest = (
            f'root_blob: "{self.sha}"\n'
            "child:\n"
            '  root: "docs/evidence.md"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            r"\$\.root_blob: no sibling path 'root'",
        ):
            self.verify(manifest)

    def test_invalid_digest_with_sibling_path_fails_closed(self):
        """An invalid digest remains an error, not a path-only record."""
        manifest = (
            'evidence_file: "docs/evidence.md"\n'
            'evidence_blob: "not-a-git-sha"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            r"\$\.evidence_blob: invalid digest",
        ):
            self.verify(manifest)

    def test_path_only_suffix_binding_fields_are_not_pins(self):
        """Recognized path fields without digest siblings are not pins."""
        manifest = (
            'evidence_file: "docs/evidence.md"\n'
            'prompt_file: "docs/prompt.md"\n'
            'executed_prompt_snapshot_file: "docs/executed.md"\n'
        )
        result = self.verify(manifest)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
        self.assertEqual(self.calls, [])

    def test_sha256_digest_cannot_bind_path_in_another_mapping(self):
        """A SHA-256 digest must bind its path in the same mapping."""
        expected = hashlib.sha256(self.raw).hexdigest()
        manifest = (
            "first:\n"
            '  prompt_file: "docs/evidence.md"\n'
            "second:\n"
            f'  prompt_sha256: "{expected}"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            r"\$\.second\.prompt_sha256: no sibling path 'prompt_file'",
        ):
            self.verify(manifest)

    def test_multiple_mapping_pins_preserve_order_and_locations(self):
        """Independent mappings produce pins in traversal order."""
        manifest = (
            "first:\n"
            '  evidence_file: "docs/evidence.md"\n'
            f'  evidence_blob: "{self.sha}"\n'
            "second:\n"
            '  evidence_file: "docs/evidence.md"\n'
            f'  evidence_blob: "{self.sha}"\n'
        )
        result = self.verify(manifest)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            [pin.location for pin in result],
            [
                "$.first.evidence_blob",
                "$.second.evidence_blob",
            ],
        )
        self.assertEqual(
            [pin.path for pin in result],
            ["docs/evidence.md", "docs/evidence.md"],
        )

    def test_flow_mapping_uses_structural_binding_rules(self):
        """Flow mappings obey the same local path/digest contract."""
        valid_manifest = (
            "pins: [{evidence_file: "
            '"docs/evidence.md", evidence_blob: '
            f'"{self.sha}"'
            "}]"
        )
        result = self.verify(valid_manifest)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].location,
            "$.pins[0].evidence_blob",
        )

        path_only_manifest = (
            'pins: [{evidence_file: "docs/evidence.md"}]\n'
        )
        result = self.verify(path_only_manifest)
        self.assertEqual(len(result), 0)

        digest_only_manifest = (
            f'pins: [{{evidence_blob: "{self.sha}"}}]\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            r"\$\.pins\[0\]\.evidence_blob: no sibling path 'evidence_file'",
        ):
            self.verify(digest_only_manifest)

    def test_one_character_digest_difference_is_rejected(self):
        """Mutation: deleting the digest comparison must turn this green."""
        wrong = ("0" if self.sha[0] != "0" else "1") + self.sha[1:]
        manifest = (
            'evidence_file: "docs/evidence.md"\n'
            f'evidence_blob: "{wrong}"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError,
            f"expected {wrong}, actual {self.sha}",
        ):
            self.verify(manifest)

    def test_missing_candidate_path_is_rejected(self):
        """Mutation: removing path resolution must turn this green."""
        manifest = (
            'evidence_file: "docs/not-committed.md"\n'
            f'evidence_blob: "{self.sha}"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError, "missing from the required commit tree"
        ):
            self.verify(manifest)

    def test_mutated_bytes_are_rejected_even_when_pin_matches_tree(self):
        """Mutation: removing Git SHA recomputation must turn this green."""
        manifest = (
            'evidence_file: "docs/evidence.md"\n'
            f'evidence_blob: "{self.sha}"\n'
        )

        def corrupted_reader(sha, path):
            return self.raw[:-2] + b"XX"

        with self.assertRaisesRegex(
            BlobPinError, "committed-byte Git SHA mismatch"
        ):
            self.verify(manifest, reader=corrupted_reader)

    def test_sha256_pin_is_recomputed_from_original_bytes(self):
        """Mutation: removing SHA-256 recomputation must turn this green."""
        expected = hashlib.sha256(self.raw).hexdigest()
        manifest = (
            'prompt_file: "docs/evidence.md"\n'
            f'prompt_sha256: "{expected}"\n'
        )
        result = self.verify(manifest)
        self.assertEqual(result[0].algorithm, "sha256")

        wrong = ("0" if expected[0] != "0" else "1") + expected[1:]
        manifest = (
            'prompt_file: "docs/evidence.md"\n'
            f'prompt_sha256: "{wrong}"\n'
        )
        with self.assertRaisesRegex(BlobPinError, "SHA-256 mismatch"):
            self.verify(manifest)

    def test_valid_manifest_without_any_pin_has_zero_effect(self):
        """Mutation: treating arbitrary fields as pins breaks this test."""
        manifest = (
            'title: "ordinary text"\n'
            'description: "not a blob identity"\n'
            'count: 12\n'
        )
        self.assertEqual(self.verify(manifest), [])
        self.assertEqual(self.calls, [])

    def test_unrelated_fields_are_not_checked(self):
        """Mutation: widening the digest-key predicate breaks this test."""
        manifest = (
            'documentation: "ordinary prose"\n'
            'description: "not a pin"\n'
            'status: "DRAFT"\n'
        )
        self.assertEqual(enumerate_blob_pins(manifest), [])

    def test_list_pin_requires_explicit_source_commit(self):
        """Mutation: implicit historical exemption must be rejected."""
        manifest = (
            "baseline_and_source_evidence:\n"
            "  d_source_blobs:\n"
            f'    - "docs/evidence.md: {self.sha}"\n'
        )
        with self.assertRaisesRegex(
            BlobPinError, "no sibling d_source_commit"
        ):
            enumerate_blob_pins(manifest)

    def test_declared_source_commit_uses_verified_source_tree(self):
        """Mutation: removing source-tree resolution must turn this green."""
        manifest = (
            "baseline_and_source_evidence:\n"
            '  d_source_commit: "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"\n'
            "  d_source_blobs:\n"
            f'    - "docs/evidence.md: {self.sha}"\n'
        )
        # The fixture resolver is deliberately exact and explicit.
        source_index = {"docs/evidence.md": make_entry(self.raw)}
        resolved = []

        def resolver(commit):
            resolved.append(commit)
            return source_index

        result = verify_blob_pins(
            manifest,
            {},
            self.reader,
            source_tree_resolver=resolver,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].location,
                         "$.baseline_and_source_evidence.d_source_blobs[0]")
        self.assertEqual(resolved, ["b" * 40])

    def test_duplicate_reads_are_cached(self):
        """Mutation: removing the per-run byte cache breaks this assertion."""
        manifest = (
            "first:\n"
            '  evidence_file: "docs/evidence.md"\n'
            f'  evidence_blob: "{self.sha}"\n'
            "second:\n"
            '  evidence_file: "docs/evidence.md"\n'
            f'  evidence_blob: "{self.sha}"\n'
        )
        self.verify(manifest)
        self.assertEqual(len(self.calls), 1)



    def test_sequence_block_scalar_is_kept_as_one_scalar(self):
        manifest = (
            "items:\n"
            "  - |-\n"
            "    evidence_file: docs/evidence.md\n"
            f"    evidence_blob: {self.sha}\n"
            "  - ordinary item\n"
        )

        result = self.verify(manifest)

        self.assertEqual(result, [])
        self.assertEqual(self.calls, [])

    def test_sequence_mapping_block_scalar_does_not_consume_siblings(self):
        manifest = (
            "items:\n"
            "  - description: >-\n"
            "      explanatory text\n"
            "      evidence_blob: not-a-pin\n"
            '    evidence_file: "docs/evidence.md"\n'
            f'    evidence_blob: "{self.sha}"\n'
        )

        result = self.verify(manifest)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].location,
            "$.items[0].evidence_blob",
        )
        self.assertEqual(result[0].path, "docs/evidence.md")
        self.assertEqual(self.calls, [(self.sha, "docs/evidence.md")])

    def test_sequence_mapping_block_scalar_preserves_digest_token_span(self):
        from scripts.governance.session_evidence.blob_pins import (
            _enumerate_pin_records,
        )

        manifest = (
            "items:\n"
            "  - description: |-\n"
            "      evidence_blob: not-a-pin\n"
            '    evidence_file: "docs/evidence.md"\n'
            f'    evidence_blob: "{self.sha}"\n'
        )

        records, errors = _enumerate_pin_records(manifest)

        self.assertEqual(errors, [])
        self.assertEqual(len(records), 1)

        token = f'"{self.sha}"'
        token_start = manifest.index(token)
        self.assertEqual(records[0].start, token_start)
        self.assertEqual(records[0].end, token_start + len(token))

    def test_sequence_plain_scalar_with_colon_is_not_a_mapping(self):
        manifest = (
            "items:\n"
            "  - https://example.invalid/evidence\n"
        )

        from scripts.governance.session_evidence.blob_pins import (
            _parse_yaml_subset,
        )

        document = _parse_yaml_subset(manifest)

        self.assertEqual(
            document,
            {"items": ["https://example.invalid/evidence"]},
        )

    def test_sequence_mapping_with_colon_and_space_is_still_a_mapping(self):
        manifest = (
            "items:\n"
            "  - evidence_file: docs/evidence.md\n"
        )

        from scripts.governance.session_evidence.blob_pins import (
            _parse_yaml_subset,
        )

        document = _parse_yaml_subset(manifest)

        self.assertEqual(
            document,
            {"items": [{"evidence_file": "docs/evidence.md"}]},
        )

    def test_mapping_plain_scalar_continuation_is_folded(self):
        from scripts.governance.session_evidence.blob_pins import (
            _parse_yaml_subset,
        )

        manifest = (
            "authorization:\n"
            "  platform_state_change: NONE - no branch-protection payload, required context or repository\n"
            "    setting is touched.\n"
            "  architecture_spec_change: NONE - no ADR is modified.\n"
        )

        document = _parse_yaml_subset(manifest)

        self.assertEqual(
            document["authorization"]["platform_state_change"],
            "NONE - no branch-protection payload, required context or repository setting is touched.",
        )
        self.assertEqual(
            document["authorization"]["architecture_spec_change"],
            "NONE - no ADR is modified.",
        )

    def test_sequence_plain_scalar_continuation_is_folded(self):
        from scripts.governance.session_evidence.blob_pins import (
            _parse_yaml_subset,
        )

        manifest = (
            "out_of_scope:\n"
            "  - Independent migration, outbox, corruption, PITR, ACK, or other findings except\n"
            "    where a dependency must be recorded to explain a boundary or safety assumption.\n"
            "  - Treating reference-model PASS as production proof.\n"
        )

        document = _parse_yaml_subset(manifest)

        self.assertEqual(
            document["out_of_scope"],
            [
                "Independent migration, outbox, corruption, PITR, ACK, or other findings except where a dependency must be recorded to explain a boundary or safety assumption.",
                "Treating reference-model PASS as production proof.",
            ],
        )

    def test_sequence_mapping_plain_scalar_continuation_preserves_sibling(self):
        from scripts.governance.session_evidence.blob_pins import (
            _parse_yaml_subset,
        )

        manifest = (
            "basis:\n"
            "  - target: 14-ai-development/work-items/INDEX.md\n"
            "    field: AID-2026-092 prompt cell\n"
            "    prior_value: old value\n"
            "    new_value: corrected value, with the superseded\n"
            "      pair and the fact that it matched nothing stated in the cell.\n"
            "    basis: the cell quotes the manifest; correcting one and not the other would create the same\n"
            "      disagreement in a second place.\n"
        )

        document = _parse_yaml_subset(manifest)
        item = document["basis"][0]

        self.assertEqual(item["target"], "14-ai-development/work-items/INDEX.md")
        self.assertEqual(item["new_value"], "corrected value, with the superseded pair and the fact that it matched nothing stated in the cell.")
        self.assertEqual(item["basis"], "the cell quotes the manifest; correcting one and not the other would create the same disagreement in a second place.")

    def test_plain_scalar_continuation_does_not_consume_next_sequence_item(self):
        from scripts.governance.session_evidence.blob_pins import (
            _parse_yaml_subset,
        )

        manifest = (
            "non_goals:\n"
            "  - Fixing the misplaced table, which is a\n"
            "    pre-existing layout defect and not a count or provenance claim\n"
            "  - Closing or reopening any Issue\n"
        )

        document = _parse_yaml_subset(manifest)

        self.assertEqual(
            document["non_goals"],
            [
                "Fixing the misplaced table, which is a pre-existing layout defect and not a count or provenance claim",
                "Closing or reopening any Issue",
            ],
        )


if __name__ == "__main__":
    unittest.main()
