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
        - "14-ai-development/work-items/AID-2026-361/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the implementation task and user-supplied local test outputs. It does not claim that this session independently executed the tests or that GitHub CI has completed."
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
    canonical_scope: "AI session evidence for AID-2026-361 manifest blob-pin ledger squash-merge verification"
    canonical_scope_id: "ai-development/aid-2026-361-session-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "ledger"
      - "squash-merge"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# Session evidence — AID-2026-361

Attribution: user-authorized operator (delegated by account owner)  
Date: 2026-11-27  
Session role: implementation session

## Session role / use case

Correct the manifest blob-pin ledger verifier so that a ledger record remains verifiable when its original repin commit has been squash-merged into the target branch and is no longer an ancestor of that target.

The implementation scope is limited to:

- `scripts/ci/check_manifest_blob_pins.py`
- `tests/test_manifest_pin_ledger.py`

Related issues: #1350 and #1349.

## Actual AI input

The implementation task required preserving the original `repin_commit` as the source of ledger evidence while allowing a non-ancestor original repin to be represented by a unique equivalent squash transition in target first-parent history.

The required proof consists of:

- resolving the original repin commit;
- verifying its first-parent pin equals the ledger `previous_pin`;
- verifying its tree pin equals the ledger `new_pin`;
- locating a unique squash commit in target first-parent history with the same previous and new pin values;
- requiring the manifest Git blob in the squash tree to equal the manifest Git blob in the original repin commit tree;
- using the resolved squash transition as the actual transition location for unledgered-history verification.

The task also required retaining rejection of forged `new_pin` values and not changing the checker CLI or unrelated governance behavior.

This is a task summary, not a byte-for-byte export of the complete chat input. The manifest therefore records prompt provenance as NOT_VERIFIED.

## AI-visible output

The implementation artifacts supplied in this session were:

- a complete replacement for `scripts/ci/check_manifest_blob_pins.py`;
- a complete replacement for `tests/test_manifest_pin_ledger.py`;
- a corrected forged-new-pin regression test using a bytes-kind manifest pin.

The user reports that these artifacts were applied to the repository and that the test commands and ratchet command recorded in `evidence.md` completed with the supplied outputs.

No claim is made here that this session independently executed those commands, that GitHub required contexts passed, that a PR was created, or that a merge occurred.
