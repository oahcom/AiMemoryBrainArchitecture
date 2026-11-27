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
        - "14-ai-development/work-items/AID-2026-268/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation evidence only; exact scan counts and CI results are not asserted until observed."
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
    canonical_scope: "Implementation evidence for AID-2026-268 manifest blob-pin verification"
    canonical_scope_id: "ai-development/aid-2026-268-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "integrity"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-268 evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Baseline fetched:** 2026-11-27T03:57:43Z  
**Baseline main:** 40195e8bf96b9cc6aa254066b9b72968f29ac361

## Scope

Implement blob-pin integrity checking in the existing required Repository hygiene job. No branch-protection, new-job, or new-workflow changes are in scope.

## Measurements

The baseline full scan and the #1220 negative scan are pending execution by GitHub Actions on an exact checkout. No scan counts, test results, required-context result, or merge SHA are claimed in this evidence file until the corresponding raw outputs are observed.

## Field enumeration

The checker implementation contains explicit branches for:
- top-level `root/root_blob`, `en_mirror/en_mirror_blob`, and `zh_cn_mirror/zh_cn_mirror_blob`;
- `gate_a_reconstruction[].root/reconstructed_root_blob`, resolved against the entry's explicit source commit or a commit SHA explicitly named in its note;
- `related_evidence[].path/blob` and its EN/ZH-CN mirror pairs;
- top-level `evidence_file/evidence_blob`;
- `d_source_blobs[]` entries, resolved against `d_source_commit`;
- `prompt.prompt_file` with `prompt_sha256/prompt_bytes`;
- `session_evidence[].executed_prompt_snapshot_file` with `executed_prompt_sha256/executed_prompt_bytes`.

Non-blob metadata such as timestamps, counts, and status values is deliberately ignored.
