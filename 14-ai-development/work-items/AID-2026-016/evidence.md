---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-016/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Verification covers the integrated implementation, named regression tests, mutation results, and reported repository gates at HEAD d07a64faf121c61e50c189b327a20dd08e81ce9d; independent acceptance and merge remain outstanding."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Implementation and verification evidence for ContextEntryVersion content hash integrity."
    canonical_scope_id: "ai-development/aid-2026-016-evidence"
    canonical_scope_keywords:
      - "context-content-integrity"
      - "content-hash-validation"
      - "implementation-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: null
    zh-CN: null
---

# Implementation Evidence

## 1. Originating defect

Issue #1145, `[MEMORY CONTEXT] Verify ContextEntryVersion content_hash against rendered content`, records a Context content integrity defect in domain G.

The required behavior is to recalculate the canonical content digest from the exact UTF-8 bytes of `rendered_content` during validation and compare that result against the declared `content_hash`.

The Issue requires:

- Exact UTF-8 byte-based digest calculation.
- An explicit algorithm, encoding, normalization, and domain-separation contract.
- Rejection of mismatches before any ChangeSet operation takes effect.
- Snapshot-level hashing based on already-validated entry content hashes.
- Adversarial tests covering incorrect hashes, empty hashes, Unicode byte lengths, normalization differences, and content modified while retaining a stale digest.

The Issue's authority boundary explicitly states that it records the G Context content integrity defect. It does not select an encryption algorithm, authorize implementation or DDL, transfer G ContextVersion authority, or transfer C/H reasoning-boundary evidence authority.

## 2. Defect evidence

The original `ContextEntryVersion::validate()` implementation checked that the declared content hash was non-empty and that the rendered byte count was valid. It did not recalculate the digest from the actual rendered content and compare the calculated result against the declaration.

Consequently, a non-empty but incorrect or stale digest could pass this validation path.

The original `commit_change_set()` path compared the overall `snapshot_hash`. That comparison did not independently establish that each entry's declared `content_hash` matched its own rendered content.

The original production implementation generated the SHA-256-prefixed content hash inline:

`format!("sha256:{}", sha256_hex(...))`

The first implementation segment established `content_hash_for()` as the shared generation and validation source of truth.

## 3. First implementation segment

### 3.1 `crates/memory-context/src/lib.rs`

- Added `pub fn content_hash_for(rendered_content: &str) -> String`.
- The helper returns deterministic `sha256:<hex>` values.
- Replaced the original inline production-side hash expression with a call to `content_hash_for()`.
- Added `ContextError::ContentHashMismatch { entry_id: OpaqueId, declared: String, actual: String }`.
- Updated `ContextEntryVersion::validate()` to recalculate the hash from `rendered_content` and reject mismatches after rendered-byte validation.
- Updated `validate_edit_entry()` to recalculate and compare the declared hash on the ContextEntry edit path.
- Documented the validated-entry content hash precondition of `snapshot_hash()`.
- Preserved the FNV-1a 64 snapshot hash algorithm.
- Replaced placeholder hashes in inline test fixtures with real `content_hash_for()` results.

### 3.2 `crates/memory-context/tests/content_hash_integrity.rs`

The first segment added six integration tests:

1. `content_hash_is_sha256_prefixed_and_deterministic`
2. `content_hash_covers_exact_utf8_bytes`
3. `content_hash_does_not_normalize_unicode`
4. `commit_rejects_entry_with_wrong_content_hash`
5. `validate_rejects_stale_hash_after_content_edit`
6. `snapshot_hash_changes_when_entry_content_hash_changes`

## 4. Post-review correction

Independent review used mutation testing to verify that the regression tests actually detect removal of the required integrity checks.

The review identified two gaps: removal of the edit-entry comparison and removal of the empty-hash check did not produce failing tests before correction.

### 4.1 Mutation verification matrix

| Mutation | Before correction | After correction | Result |
|---|---|---|---|
| V1: Delete `ContextEntryVersion::validate()` hash comparison | 2 red | 2 red | PASS |
| V2: Delete `validate_edit_entry()` hash comparison | 0 red | 1 red | PASS |
| V3: Delete empty content hash validation | 0 red | 1 red | PASS |
| V4: Change `sha256:` to `sha256x:` | 2 red | 2 red | PASS |

After correction, all four mutation cases produced failing tests (4/4 red).

The additional regression tests were:

- `change_set_validate_rejects_edit_entry_with_wrong_content_hash`
- `validate_rejects_empty_content_hash`

The complete final eight-test inventory is:

1. `pr433_tests::update_entry_recomputes_rendered_bytes_and_content_hash`
2. `change_set_validate_rejects_edit_entry_with_wrong_content_hash`
3. `commit_rejects_entry_with_wrong_content_hash`
4. `content_hash_covers_exact_utf8_bytes`
5. `content_hash_does_not_normalize_unicode`
6. `content_hash_is_sha256_prefixed_and_deterministic`
7. `snapshot_hash_changes_when_entry_content_hash_changes`
8. `validate_rejects_empty_content_hash`

### 4.2 Cross-crate content hash contract correction

The independent probe identified a producer-side contract mismatch in `crates/brain-cli/src/main.rs`.

The original brain-cli implementation used its local `sha256_hex` helper to generate a bare 64-character hexadecimal `content_hash` without the required `sha256:` prefix.

The generated value was propagated through `build_context` and rejected by the new validation with `ContentHashMismatch`.

The correction replaced the producer's content hash generation with:

`memory_context::content_hash_for(&rendered_content)`

The local `sha256_hex` helper remains in place for its other uses and has an explanatory comment clarifying that it is not the canonical content_hash producer.

The affected production file is:

`crates/brain-cli/src/main.rs`

The second implementation segment also extended `crates/memory-context/tests/content_hash_integrity.rs` with two additional tests and three assertion extensions.

## 5. Final implementation summary

| File | Final change evidence |
|---|---|
| `crates/memory-context/src/lib.rs` | First segment +43/-7; final integrated numstat +36/-7 |
| `crates/memory-context/tests/content_hash_integrity.rs` | Initial 89 lines; final 192 lines; eight tests |
| `crates/brain-cli/src/main.rs` | +4/-4 |
| Total implementation files | 3 |

Final integration branch:

`fix/2026-11-27-aid-016-context-content-hash`

Final HEAD:

`d07a64faf121c61e50c189b327a20dd08e81ce9d`

Base commit:

`46dac1b1e198c8d88daff5a34faf759ecb075869`

## 6. Issue acceptance requirement mapping

| Issue #1145 requirement | Implementation location | Test evidence | Result |
|---|---|---|---|
| Recalculate the digest from exact UTF-8 rendered content | `content_hash_for()` and `ContextEntryVersion::validate()` | `content_hash_covers_exact_utf8_bytes` | IMPLEMENTED |
| Compare calculated digest with declared content hash | `ContextEntryVersion::validate()` | `commit_rejects_entry_with_wrong_content_hash` | IMPLEMENTED |
| Establish deterministic SHA-256-prefixed generation | `content_hash_for()` | `content_hash_is_sha256_prefixed_and_deterministic` | IMPLEMENTED |
| Preserve Unicode distinctions without implicit normalization | `content_hash_for()` | `content_hash_does_not_normalize_unicode` | IMPLEMENTED |
| Reject incorrect hashes before ChangeSet operations take effect | Validation and `ContextError::ContentHashMismatch` | `commit_rejects_entry_with_wrong_content_hash` | IMPLEMENTED |
| Verify ContextEntry edit-path hashes | `validate_edit_entry()` | `change_set_validate_rejects_edit_entry_with_wrong_content_hash` | IMPLEMENTED |
| Reject empty content hashes | Content hash validation | `validate_rejects_empty_content_hash` | IMPLEMENTED |
| Verify snapshot hash changes when entry content hashes change | `snapshot_hash()` | `snapshot_hash_changes_when_entry_content_hash_changes` | IMPLEMENTED |
| Verify rendered-byte and content-hash recomputation on update | Existing update path | `pr433_tests::update_entry_recomputes_rendered_bytes_and_content_hash` | IMPLEMENTED |
| Ensure stale content cannot retain a valid declared hash | `ContextEntryVersion::validate()` | `validate_rejects_stale_hash_after_content_edit` | IMPLEMENTED |
| Ensure the CLI producer emits the canonical hash representation | `crates/brain-cli/src/main.rs` | Brain CLI test suite and cross-crate probe | IMPLEMENTED |
| Verify empty hashes and adversarial Unicode byte behavior | Validation and exact-byte hashing | `validate_rejects_empty_content_hash`; `content_hash_covers_exact_utf8_bytes`; `content_hash_does_not_normalize_unicode` | IMPLEMENTED |

## 7. Final verification results

All commands below were reported against final integrated HEAD `d07a64faf121c61e50c189b327a20dd08e81ce9d`.

| Gate | Command | Exit code | Result |
|---|---|---:|---|
| Memory context tests | `cargo test -p memory-context --no-fail-fast` | 0 | 185 passed; 0 failed |
| Brain CLI tests | `cargo test -p brain-cli --no-fail-fast` | 0 | 24 passed; 0 failed |
| Agent integration tests | `cargo test -p agent-integration --no-fail-fast` | 0 | 63 passed; 0 failed |
| Clippy | `cargo clippy -p memory-context -p brain-cli --all-targets -- -D warnings` | 0 | Finished; no warnings |
| Cargo formatting | `cargo fmt --all -- --check` | 0 | Empty output |
| Manifest parsing | `python scripts/ci/check_manifest_parse.py` | 0 | 124 manifests; 0 failed |
| Document management | `python scripts/check_document_management.py --require-changed origin/main` | 0 | PASS (incremental); 700 classified / 370 unclassified |
| Traceability | `python scripts/check_traceability.py --index-only` | 0 | PASS; 0 errors / 115 warnings |

### 7.1 Test totals

| Suite | Passed | Failed |
|---|---:|---:|
| memory-context | 185 | 0 |
| brain-cli | 24 | 0 |
| agent-integration | 63 | 0 |
| Total | 272 | 0 |

The package-output sequences were:

- memory-context: `85/10/8/9/19/8/1/2/8/14/21/0`
- brain-cli: `1/2/3/4/1/3/1/2/4/3`
- agent-integration: `36/2/19/6/0`

## 8. Authority and scope boundaries

This implementation addresses the content integrity defect recorded in Issue #1145.

It does not:

- Select or authorize an encryption algorithm.
- Modify encryption policy.
- Change G ContextVersion authority.
- Change C/H reasoning-boundary evidence authority.
- Change the FNV-1a 64 snapshot hash algorithm.
- Change snapshot hash semantics.
- Authorize DDL changes.
- Establish natural-person owner acceptance.
- Close Issue #1145.

The snapshot hash continues to use FNV-1a 64. The implementation ensures that entry content hashes are validated before they contribute to snapshot-level integrity.

No bilingual documentation mirrors were created. The work-item directory is within the established bilingual-pairing exemption prefix.

## 9. Reproducibility

Repository:

`oahcom/AiMemoryBrainArchitecture`

Integration branch:

`fix/2026-11-27-aid-016-context-content-hash`

Base:

`46dac1b1e198c8d88daff5a34faf759ecb075869`

Final HEAD:

`d07a64faf121c61e50c189b327a20dd08e81ce9d`

The following commands reproduce the reported verification gates:

```bash
cargo test -p memory-context --no-fail-fast
cargo test -p brain-cli --no-fail-fast
cargo test -p agent-integration --no-fail-fast
cargo clippy -p memory-context -p brain-cli --all-targets -- -D warnings
cargo fmt --all -- --check
python scripts/ci/check_manifest_parse.py
python scripts/check_document_management.py --require-changed origin/main
python scripts/check_traceability.py --index-only
```

The integration tests can be run independently with:

```bash
cargo test -p memory-context --test content_hash_integrity
```

## 10. Evidence and acceptance status

| Evidence item | Status |
|---|---|
| First implementation segment | RECORDED |
| Second implementation segment | RECORDED |
| Final integrated source changes | RECORDED |
| Eight content hash integration tests | RECORDED |
| Mutation verification V1–V4 | PASS; 4/4 red |
| Cross-crate brain-cli contract probe | RECORDED |
| memory-context test suite | PASSED |
| brain-cli test suite | PASSED |
| agent-integration test suite | PASSED |
| Clippy | PASSED |
| Cargo formatting | PASSED |
| Manifest parser | PASSED |
| Document management | PASSED |
| Traceability | PASSED |
| First implementing AI session | RECORDED |
| Second implementing AI session | RECORDED |
| prompt-v1 SHA-256 and byte count | RECORDED |
| prompt-v2 SHA-256 and byte count | PENDING_MEASUREMENT |
| Independent mutation review | FAIL_THEN_FIXED |
| Natural-person owner acceptance | NOT_RECORDED |
| Merge | PENDING |
| Issue #1145 | OPEN |

This evidence record documents both implementation segments and their reported verification. It does not substitute for natural-person acceptance, merge authorization, or closure of Issue #1145.
