---
document_metadata:
  domain: ai-development
  role: work-record
  steward: user-authorized operator (delegated by account owner)
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
        - "AID-2026-301/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Provisional implementation evidence; exact-Head CI and independent review control acceptance."
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
    canonical_scope: "Evidence and field registry for Issue #1350 blob-pin discovery"
    canonical_scope_id: "ai-development/aid-2026-301-evidence"
    canonical_scope_keywords:
      - "manifest-blob-pins"
      - "field-registry"
      - "issue-1350"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-301 — Blob-pin discovery evidence

## Scope and measured starting point

This is an implementation addendum to Issue #1350 and the previously landed AID-2026-268 checker. The supplied independent-review counterexample is reproduced as a required regression: top-level `prompt_sha256` with `prompt_version: v2` resolves to `prompt-v2.md` in the manifest directory and is SHA-256 over committed bytes.

The observed repository main at implementation start was `af2660d55a93278157fa6668aba338daf81e127c`, not the earlier task-provided `b12bfe8ca1c23262418f5e76951ffb874cb7ccfb`. The exact-head workflow result, not this observation, controls final acceptance.

## Explicit field registry

| Manifest field pattern | Locator | Algorithm | Definition location in repository |
|---|---|---|---|
| `root_blob`, `en_mirror_blob`, `zh_cn_mirror_blob` | sibling `root`, `en_mirror`, `zh_cn_mirror`; candidate commit | Git blob SHA-1 | Existing index-style manifests; parser branch in `scripts/ci/check_manifest_blob_pins.py` |
| `gate_a_reconstruction[].reconstructed_root_blob` | sibling `root`; entry `source_commit` or `commit` | Git blob SHA-1 | Existing Gate-A reconstruction manifests |
| `authored_indexes[].{root_blob,en_mirror_blob,zh_cn_mirror_blob}` | sibling path key; candidate commit | Git blob SHA-1 | `baseline_and_source_evidence.authored_indexes` or top-level `authored_indexes` |
| `related_evidence[].blob`, `en_mirror_blob`, `zh_cn_mirror_blob` | sibling `path`, `en_mirror`, `zh_cn_mirror`; candidate commit | Git blob SHA-1 | Existing related-evidence manifests |
| `evidence_blob` | `evidence_file`; candidate commit | Git blob SHA-1 | Existing execution-evidence manifests |
| `d_source_blobs[]` | inline `<path>: <sha>`; `d_source_commit` | Git blob SHA-1 | Existing D-source manifests |
| `prompt.prompt_sha256`, `prompt.prompt_bytes` | `prompt.prompt_file`; candidate commit | SHA-256(bytes), byte length | Nested prompt manifests |
| `session_evidence[].executed_prompt_sha256/bytes` | `executed_prompt_snapshot_file`; candidate commit | SHA-256(bytes), byte length | Session-evidence entries |
| **top-level `prompt_sha256`** | explicit `prompt_file`, else sibling `prompt-v{prompt_version}.md); candidate commit | SHA-256(bytes) | `14-ai-development/work-items/AID-2026-001/manifest.yaml:43-45` |
| `source_translation_pairs[].source_blob_sha` | `source_path`; `source_commit_sha` | Git blob SHA-1 | `AID-2026-004/manifest.yaml:22-35` |
| `source_translation_pairs[].translation_blob_sha` | `translation_path`; `translation_commit_sha` | Git blob SHA-1 | `AID-2026-004/manifest.yaml:22-35` |
| `source_translation_pairs[].translation_sha256` | `translation_path`; `translation_commit_sha` | SHA-256(bytes) | `AID-2026-004/manifest.yaml:22-35` |
| `source_blobs[].sha` | `source_blobs[].path`; `base_commit` / `baseline_commit` | Git blob SHA-1 | `AID-2026-023/manifest.yaml:38-54` |
| `source.selected_source_files[].source_blob_sha` | `path`; `source.head_sha` | Git blob SHA-1 | `AID-2026-109/manifest.yaml:22-46` |
| `source.selected_source_files[].restored_blob_sha` | `path`; candidate commit | Git blob SHA-1 | `AID-2026-109/manifest.yaml:22-46` |
| `source.selected_source_files[].frontmatter_blob_sha` | requires `frontmatter_path` or `frontmatter_file` | Git blob SHA-1 | `AID-2026-109/manifest.yaml:22-46`; absent locator is explicitly UNRESOLVED |
| `source.files[].blob` | `source.files[].path`; `source.head` | Git blob SHA-1 | `AID-2026-150/manifest.yaml:26-32` |

The executable registry is `PIN_FIELD_REGISTRY` in `scripts/ci/check_manifest_blob_pins.py`. In addition to the named handlers, recursive discovery rejects unregistered blob/digest-shaped fields with `INCOMPLETE UNRESOLVED(unregistered digest field)`; commit identifiers are not treated as blob identities.

## Fail-closed rules

- A declared digest key with an empty, malformed, or sentinel value is counted as a pin and reported INCOMPLETE, never dropped from the denominator.
- A missing path produces PATH_MISSING; a missing, malformed, ambiguous, or unavailable source commit produces INCOMPLETE/UNRESOLVED.
- Git blob SHA-1 is recomputed using the Git object header and committed bytes. SHA-256 is recomputed over committed file bytes. Byte counts use committed byte length.
- `frontmatter_blob_sha` has no locator in the observed AID-109 records. It is deliberately reported as UNRESOLVED rather than falsely compared with the whole-file blob.
- Existing historical mismatches remain subject to exact-line ratchet entries. No wildcard, directory-wide exemption, or advisory downgrade is introduced.

## Negative controls

The test suite prints actual checker output for:
1. A changed Git blob digest (declared vs recomputed actual).
2. A deleted path (PATH_MISSING).
3. An unavailable commit (UNRESOLVED/INCOMPLETE).
4. A changed top-level prompt SHA-256.
5. An unregistered digest field and a source frontmatter digest with no locator.

The authoritative real outputs are the `Self-check manifest blob pin verification` CI step on the exact PR head. No result is claimed until that run is observed.

## Baseline disposition

The baseline is not widened speculatively. Any newly discovered failure emitted by the exact-head scan must be corrected if objectively wrong; otherwise only the complete, exact emitted line may be added with an item-specific rationale and a follow-up work item. The existing 89 mismatch + 2 missing-path baseline entries are retained unchanged at implementation start.

## Regression scope

The existing required Repository hygiene job remains the carrier. Traceability, hygiene, bilingual, line-ending, and test-reachability checks remain in their existing workflow/job topology. No branch protection or required context is changed.
