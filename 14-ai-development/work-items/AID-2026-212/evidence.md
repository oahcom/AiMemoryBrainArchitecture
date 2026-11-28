---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Implementation evidence is pending local execution and final readback; no acceptance or independent review is asserted."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Implementation evidence for AID-2026-212"
    canonical_scope_id: "ai-development/aid-2026-212-implementation-evidence"
    canonical_scope_keywords:
      - "blob-pin-integrity"
      - "implementation-evidence"
      - "work-item"
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-212 — Implementation evidence

## 1. Objective

Implement Issue #1350 and close the missing integrity-verification gate
identified by Issue #1349.

The required security property is:

Every declared blob identity must resolve to committed bytes in the
appropriate exact commit tree, and the declared digest must match those
bytes.

## 2. Implementation inventory

| Artifact | Change |
|---|---|
| scripts/governance/session_evidence/blob_pins.py | New pure validation module |
| scripts/governance/session_evidence/validate.py | Check 12 integration |
| tests/session_evidence/test_blob_pins.py | Offline adversarial tests |
| manifest.yaml | Work Item registration |
| prompt-v1.md | Executed task snapshot |
| session-evidence.md | Session evidence |

The validator integration is intentionally limited to:
- one import addition;
- one check-number documentation addition;
- one new check function;
- one invocation after check 11.

Existing checks are not redesigned.

## 3. Binding contract

Digest recognition is dynamic and restricted to these classes:

| Digest key | Sibling path key | Algorithm |
|---|---|---|
| root_blob | root | Git SHA-1 |
| blob | path | Git SHA-1 |
| en_mirror_blob | en_mirror | Git SHA-1 |
| zh_cn_mirror_blob | zh_cn_mirror | Git SHA-1 |
| reconstructed_root_blob | root | Git SHA-1 |
| evidence_blob | evidence_file | Git SHA-1 |
| prompt_sha256 | prompt_file | SHA-256 |
| executed_prompt_sha256 | executed_prompt_snapshot_file | SHA-256 |
| any other *_blob | same-prefix path key | Git SHA-1 |
| any other *_sha256 | same-prefix *_file key | SHA-256 |

The explicit mappings take precedence over suffix derivation.

List representation:
- baseline_and_source_evidence.d_source_blobs
- Each element must be a quoted or unquoted `path: sha` scalar.
- The SHA must be exactly 40 hexadecimal characters.
- Each element requires the same parent mapping to declare d_source_commit.

No arbitrary prose, status, count, URL, or other non-digest field is
interpreted as a blob pin.

## 4. Three-state contract

| Declaration | Result |
|---|---|
| Path and digest both present | Resolve path and verify digest |
| Digest without path | Reject with missing-path error |
| Path without digest | Reject with missing-digest error |

A valid pin produces no warning or notice.

A missing path is not converted into an unavailable state. An unresolved
pin is a validation failure.

## 5. Historical-source exemption register

The only historical-source exemption is the explicitly structured
d_source_blobs list.

The exemption is bound to the same parent mapping's d_source_commit.
It is not inferred from a branch name, file location, or digest value.

The following historical declarations in the observed AID-2026-100
manifest are the enumerated members of this exemption class:

| Key | Historical path | Reason |
|---|---|---|
| baseline_and_source_evidence.d_source_blobs[1] | memory-brain-overview.md | Source blob belongs to the separately declared D source commit |
| baseline_and_source_evidence.d_source_blobs[2] | canonical-memory-store.md | Source blob belongs to the separately declared D source commit |
| baseline_and_source_evidence.d_source_blobs[3] | memory-lifecycle-manager.md | Source blob belongs to the separately declared D source commit |
| baseline_and_source_evidence.d_source_blobs[4] | forget-fence-operation-and-publication-gate.md | Source blob belongs to the separately declared D source commit |

The parent mapping declares:
- d_source_branch: session-d-memory-brain-2026-11-16
- d_source_commit: b525e1f8fee2471a131e4a38efda99804045e424

The branch is provenance information, not an authorization to skip
verification. The exact commit is the verification authority.

The verifier must:
1. retrieve that exact commit through the GitHub commit API;
2. confirm that the returned commit SHA is identical;
3. retrieve its complete recursive tree;
4. reject truncated trees;
5. resolve every listed path in that tree;
6. compare the tree blob SHA with the declared SHA;
7. retrieve and recompute the original Git blob identity.

No other observed pin key receives a historical exemption.

In particular, root_blob, en_mirror_blob, zh_cn_mirror_blob,
reconstructed_root_blob, evidence_blob and prompt_sha256 are not
automatically exempt.

If the exact source commit or tree cannot be resolved, validation fails.

## 6. Why both Git identity checks are required

The first comparison is:

manifest Git SHA == selected tree entry SHA

This proves that the declared identity agrees with the path-to-object
binding in the selected commit tree.

The second comparison is:

SHA1("blob " + decimal_byte_length + NUL + original_bytes)
    == selected tree entry SHA

This independently proves that the retrieved bytes really are the
Git object selected by that tree entry.

These checks are not redundant: the first validates tree metadata;
the second validates the actual returned content.

For SHA-256 pins, SHA-256 is separately recomputed over original bytes.

## 7. Performance

- The existing Git tree path index provides O(1) lookup.
- Source commit trees are cached per exact commit within one validation.
- Byte reads are cached per (tree blob SHA, path) within one validation.
- No repeated recursive scan of the candidate tree is required.
- Existing gh_blob_bytes caching remains in use.

## 8. Test inventory and mutation assertions

| Test | Security property | Mutation that must turn it red |
|---|---|---|
| test_path_and_digest_are_accepted_without_noise | Valid pins pass silently | Remove byte verification |
| test_digest_only_is_rejected_with_missing_path | Digest cannot float without a path | Remove missing-path rejection |
| test_path_only_is_rejected_with_missing_digest | Path cannot be declared without identity | Remove missing-digest rejection |
| test_one_character_digest_difference_is_rejected | Digest comparison is mandatory | Remove digest comparison |
| test_missing_candidate_path_is_rejected | Candidate-tree resolution is mandatory | Remove path lookup |
| test_mutated_bytes_are_rejected_even_when_pin_matches_tree | Retrieved bytes must match tree identity | Remove Git SHA recomputation |
| test_sha256_pin_is_recomputed_from_original_bytes | SHA-256 is derived from bytes | Remove SHA-256 recomputation |
| test_valid_manifest_without_any_pin_has_zero_effect | No-pin manifests remain compatible | Treat arbitrary fields as pins |
| test_unrelated_fields_are_not_checked | Scope is restricted to digest fields | Widen the digest-key predicate |
| test_list_pin_requires_explicit_source_commit | No implicit historical exemption | Allow missing source commit |
| test_declared_source_commit_uses_verified_source_tree | Historical resolution is explicit | Remove source-tree resolution |
| test_duplicate_reads_are_cached | Repeated reads are avoided | Remove the per-run byte cache |

The mutation assertions are executable assertions, not merely a list of
recommended future mutations.

## 9. Exact candidate binding

The production integration supplies:
- ctx.head_sha as the PR Head commit;
- ctx.tree_by_path as the index constructed from gh_tree(repo, head_sha);
- gh_blob_bytes as the original-byte reader.

The verifier does not use the base branch tree as the candidate tree.

Historical pins use only the separately verified source commit described
in section 5.

## 10. Regression evidence required

The following must be run against the final candidate:

1. `python3 -m unittest tests.session_evidence.test_blob_pins`
2. `python3 -m unittest tests.session_evidence.test_validate`
3. The repository Session Evidence workflow command:
   `python3 -m scripts.governance.session_evidence.validate`
4. The repository traceability checker.
5. The repository hygiene checker.
6. The bilingual documentation gate.

No regression PASS is claimed by this document until the coordinator
records actual command output, candidate SHA, exit status and timestamp.

## 11. Evidence limitations

This document records the implementation contract and intended test
assertions. It does not claim that remote CI, the complete repository
test suite, independent review, or merge acceptance has already occurred.

The final evidence update must append:
- exact candidate commit SHA;
- executed test names and counts;
- exit statuses;
- workflow run URL;
- regression command outputs;
- prompt SHA-256 and byte count;
- actual mutation execution results.
