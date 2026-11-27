---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
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
        - "14-ai-development/work-items/14-ai-development/reports/aid-2026-255-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the actual implementation input and API-visible actions; it does not claim local execution."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "AI session evidence for AID-2026-255 implementation"
    canonical_scope_id: "ai-development/aid-2026-255-session-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "implementation"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-255 session evidence

## Session role

Implementation session for the AID-2026-255 delta on PR #1454, answering Issue #1350.

- Carrier ruling: Owner A ruled that `AID-2026-268` / PR #1392 is the implementation carrier already on `main`, and that `AID-2026-255` / PR #1395 may only contribute sibling-key association tests plus ratchet-negative and independent-review evidence.
- Implementation session: S6-B (acct4). Input: the landed `scripts/ci/check_manifest_blob_pins.py` and `scripts/ci/test_check_manifest_blob_pins.py` reproduced verbatim, plus four required mutation cases.
- Output: the modified test module, returned as one `<<<FILE>>>` block and applied unedited.

## Actual AI input

1. Neighbouring digest key: two sibling pairs, pair A's digest placed under pair B's key. A resolver that reads the neighbour reports the wrong pair clean; the test requires both pairs to be reported.
2. Path-key identity: `en_mirror` names file X while `en_mirror_blob` holds file Y's blob id; the failure must name X.
3. Cross-identity isolation: one correct and one wrong pin must yield exactly one mismatch.
4. Field coverage: one minimal fixture per enumerated path/digest pair (`root`/`root_blob`, `en_mirror`/`en_mirror_blob`, `zh_cn_mirror`/`zh_cn_mirror_blob`, `path`/`blob`, `evidence_file`/`evidence_blob`, prompt and session-snapshot forms).

## AI-visible output

The session returned the full test module; the eight pre-existing test methods were preserved byte-identically and four new methods were appended, each docstring naming the wrong implementation it kills.

## Provenance

Prompt text was composed by the orchestrator from the landed source and the Owner ruling. No verbatim prompt snapshot was captured for this delta; the disposition is `NOT_RECORDED`, not a claim of frozen provenance.
