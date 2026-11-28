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
      last_verification_note: "Contains user-supplied original command outputs. Repository CI and PR required-context results have not been asserted."
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
    canonical_scope: "Implementation and local test evidence for AID-2026-361"
    canonical_scope_id: "ai-development/aid-2026-361-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "ledger"
      - "squash-merge"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-361 evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Baseline main:** `f0843a8f38a420883921cfda96b515204967f885`

## Scope

Fix manifest blob-pin ledger verification for squash-merged repin commits.

The defect occurred after PR #1512 was squash-merged. The ledger retained the original repin commit SHA `6045af65fcc2e89d1895e09ed666af4d737203bf`, but that commit was not an ancestor of the target main tip. The checker treated this valid squash-merge history as incomplete, causing the required `Repository hygiene (hard gate)` context to fail.

Only the following implementation files are in scope:

- `scripts/ci/check_manifest_blob_pins.py`
- `tests/test_manifest_pin_ledger.py`

No workflow, branch-protection, baseline, or unrelated manifest change is included in this work item.

## Implementation

The ledger continues to identify the original repin commit. The verifier now distinguishes the original evidence commit from the commit that represents the transition in target history.

For a non-ancestor original repin commit, acceptance requires all of the following:

1. The original repin commit can be resolved.
2. Its first-parent pin equals the ledger `previous_pin`.
3. Its tree pin equals the ledger `new_pin`.
4. Exactly one equivalent squash transition exists in target first-parent history.
5. The squash transition's first-parent pin equals `previous_pin`.
6. The squash transition's tree pin equals `new_pin`.
7. The manifest Git blob in the squash tree exactly equals the manifest Git blob in the original repin commit tree.

The resolved squash commit is used as the actual transition location by `verify_unledgered_history`.

The implementation adds `resolve_ledger_transition()` and `Git.blob_oid()`. The ledger history verification uses the resolved transition location rather than assuming the original repin SHA must be a target ancestor.

The regression tests cover successful unique squash equivalence, rejection when the squash manifest blob differs, and rejection when a forged ledger `new_pin` is not present in the original repin commit tree.

## User-reported local verification

The following command outputs were supplied by the user after applying the two implementation files.

### Manifest blob-pin checker tests

Command:

