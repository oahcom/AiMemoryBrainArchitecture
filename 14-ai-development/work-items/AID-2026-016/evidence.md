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
      last_verification_note: "Verification covers the recorded implementation changes, named tests, and reported repository gates at HEAD 731d9d08; independent review, natural-person acceptance, merge, and Issue closure remain unverified."
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
    canonical_scope: "Implementation and test evidence for AID-2026-016 ContextEntryVersion content hash integrity."
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

The production implementation at the previously observed line 272 generated the SHA-256-prefixed content hash inline:

`format!("sha256:{}", sha256_hex(...))`

This established the production prefix convention but did not provide a shared public single-source helper for generation and validation.

The available line-level evidence identifies the original inline production expression at line 272. Exact original line numbers for the validation and ChangeSet implementations were not supplied as verified facts and are therefore not asserted here.

## 3. Implementation changes

### 3.1 `crates/memory-context/src/lib.rs`

Changes: +43 / -7.

- Added `pub fn content_hash_for(rendered_content: &str) -> String`.
- The helper returns a deterministic `sha256:<hex>` value.
- The helper is the single source of truth for generating the content hash.
- Replaced the original inline production-side `format!("sha256:{}", sha256_hex(...))` expression with a call to `content_hash_for()`.
- Added `ContextError::ContentHashMismatch { entry_id: OpaqueId, declared: String, actual: String }`.
- Updated `ContextEntryVersion::validate()` to recalculate the content hash from `rendered_content` and reject a mismatch after the rendered-byte validation.
- Updated `validate_edit_entry()` on the `ContextEntry` path to recalculate and compare the content hash.
- Added documentation to `snapshot_hash()` explaining that its entry set is based on validated `content_hash` values.
- Kept the existing FNV-1a 64 snapshot hash algorithm unchanged.
- Updated four inline-test fixture locations that previously used placeholder or fabricated hashes to use real values from `content_hash_for()`.

### 3.2 `crates/memory-context/tests/content_hash_integrity.rs`

Changes: new file, 89 lines.

Added six integration tests:

1. `content_hash_is_sha256_prefixed_and_deterministic`
2. `content_hash_covers_exact_utf8_bytes`
3. `content_hash_does_not_normalize_unicode`
4. `commit_rejects_entry_with_wrong_content_hash`
5. `validate_rejects_stale_hash_after_content_edit`
6. `snapshot_hash_changes_when_entry_content_hash_changes`

### 3.3 Change summary

| Item | Result |
|---|---|
| Existing files modified | 1 |
| New files added | 1 |
| Total files changed | 2 |
| Insertions | +125 |
| Deletions | -7 |
| New integration tests | 6 |
| Implementation HEAD | `731d9d08` |

## 4. Issue acceptance requirement mapping

| Issue #1145 requirement | Implementation location | Test evidence | Result |
|---|---|---|---|
| Recalculate the canonical digest from exact UTF-8 rendered content | `content_hash_for()` and `ContextEntryVersion::validate()` in `crates/memory-context/src/lib.rs` | `content_hash_covers_exact_utf8_bytes` | IMPLEMENTED |
| Compare the calculated digest against the declared content hash | `ContextEntryVersion::validate()` | `commit_rejects_entry_with_wrong_content_hash`; `validate_rejects_stale_hash_after_content_edit` | IMPLEMENTED |
| Establish the SHA-256 prefix and deterministic generation contract | `content_hash_for()` | `content_hash_is_sha256_prefixed_and_deterministic` | IMPLEMENTED |
| Preserve Unicode distinctions without implicit normalization | Exact string-to-UTF-8-byte hashing through `content_hash_for()` | `content_hash_does_not_normalize_unicode` | IMPLEMENTED |
| Reject incorrect content hashes before ChangeSet operations take effect | Validation and `ContextError::ContentHashMismatch` | `commit_rejects_entry_with_wrong_content_hash` | IMPLEMENTED |
| Apply the same content-hash verification to the ContextEntry edit path | `validate_edit_entry()` | Validation coverage in `crates/memory-context/src/lib.rs` | IMPLEMENTED |
| Base snapshot-level hashing on validated entry content hashes | `snapshot_hash()` documentation and existing validated-entry data path | `snapshot_hash_changes_when_entry_content_hash_changes` | IMPLEMENTED |
| Cover stale hashes after content modification | `ContextEntryVersion::validate()` | `validate_rejects_stale_hash_after_content_edit` | IMPLEMENTED |
| Cover empty declared hashes and adversarial byte-length cases | Existing validation plus the new hashing and validation test coverage | Exact individual empty-hash and byte-length test mapping: NOT_MEASURED | PARTIALLY_MEASURED |

The final row distinguishes the Issue's requested adversarial categories from the specifically named six new integration tests. The supplied evidence does not identify a separate new test name for every empty-hash or rendered-byte-length case. No additional test coverage is claimed beyond the verified test inventory.

## 5. Verification and gate results

All commands below were executed against implementation HEAD `731d9d08`.

| Gate | Command | Exit code | Observed result |
|---|---|---:|---|
| Memory context tests | `cargo test -p memory-context --no-fail-fast` | 0 | 85 / 10 / 6 / 9 / 19 / 8 / 1 / 2 / 8 / 14 / 21 / 0; 0 failed |
| Agent integration tests | `cargo test -p agent-integration --no-fail-fast` | 0 | 36 / 2 / 19 / 6 / 0; 0 failed |
| Brain CLI tests | `cargo test -p brain-cli --no-fail-fast` | 0 | All OK; 0 failed |
| Clippy | `cargo clippy -p memory-context --all-targets -- -D warnings` | 0 | Finished dev profile |
| Cargo formatting | `cargo fmt --all -- --check` | 0 | Empty output |
| Repository formatting and integrity check | `python scripts/check_fmt.py` | 0 | `FMT_RESULT=PASS`; `CHECK_RESULT=PASS`; `WORKTREE_RESULT=CLEAN`; `CHECKED_COMMIT_SHA=731d9d08` |

The reported test counts are preserved as observed package-output sequences. They are not converted into inferred aggregate counts.

### Formatting correction record

The first `cargo fmt --all -- --check` execution exited with code 1 because of import-use line wrapping in the new integration test file.

The issue was returned to the implementing ChatGPT session. A formatting correction was supplied as an EDIT block and mechanically applied by the execution party.

The correction introduced no semantic changes.

The subsequent formatting check exited with code 0. The repository formatting and integrity check also passed.

## 6. Authority and scope boundaries

This implementation addresses the content integrity defect recorded by Issue #1145.

It does not:

- Select or authorize an encryption algorithm.
- Modify encryption policy.
- Change the authority of G ContextVersion.
- Change the authority of C/H reasoning-boundary evidence.
- Change the FNV-1a 64 snapshot hash algorithm.
- Change the snapshot hash calculation semantics.
- Authorize DDL changes.
- Establish independent review or natural-person acceptance.
- Close Issue #1145.

The snapshot hash algorithm remains FNV-1a 64. The change documents and relies on validated entry content hashes; it does not replace the snapshot algorithm with SHA-256.

No bilingual documentation mirrors were created. The work-item directory is within the established bilingual-pairing exemption prefix.

## 7. Reproducibility

Repository:

`oahcom/AiMemoryBrainArchitecture`

Implementation branch:

`fix/2026-11-27-aid-241-context-content-hash`

Implementation HEAD:

`731d9d08`

Observed base:

`origin/main = a588cd99`

The base SHA is recorded as the supplied short SHA. Its full 40-character form was not supplied and is not fabricated.

The following commands reproduce the reported verification gates when executed against the implementation commit in the corresponding repository environment:

```bash
cargo test -p memory-context --no-fail-fast
cargo test -p agent-integration --no-fail-fast
cargo test -p brain-cli --no-fail-fast
cargo clippy -p memory-context --all-targets -- -D warnings
cargo fmt --all -- --check
python scripts/check_fmt.py
```

The new integration test file can be run independently with:

```bash
cargo test -p memory-context --test content_hash_integrity
```

The implementation-session reference is:

`ChatGPT 6b08f8b6-4298-83ec-945c-91fafb7bf422 (acct1)`

The executed prompt snapshot source is:

`D:\code\chatgpt-session-ops\prompts\27-aid241-context-entry-content-hash.md`

The final `prompt-v1.md` consists of its GOV-DOC-002 frontmatter followed by the source prompt as a byte-for-byte body copy. The final file's measured SHA-256 digest and byte count, including the frontmatter, are recorded in the manifest's `executed_prompt_sha256` and `executed_prompt_bytes` fields.

## 8. Evidence status

| Evidence item | Status |
|---|---|
| Implementation source changes | RECORDED |
| Six new integration tests | RECORDED |
| Three package test commands | PASSED |
| Clippy | PASSED |
| Cargo formatting check | PASSED |
| Repository formatting and integrity check | PASSED |
| Implementing AI session reference | RECORDED |
| Five successful API deliveries | RECORDED |
| Prompt snapshot SHA-256 | NOT_MEASURED |
| Prompt snapshot byte count | NOT_MEASURED |
| Independent reviewer | NOT_ASSIGNED |
| Natural-person owner acceptance | NOT_RECORDED |
| Merge | PENDING |
| Issue #1145 closure | OPEN |

This evidence record documents the implementation and its reported technical verification. It does not substitute for independent review, acceptance authority, or repository merge authorization.
