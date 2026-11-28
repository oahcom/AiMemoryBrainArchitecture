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
        - "14-ai-development/work-items/AID-2026-327/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Repository observations recorded at the base SHA and branch head; independent review and current-head CI are pending."
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
    canonical_scope: "Evidence for recording the final Owner D-10 cursor authority decision."
    canonical_scope_id: "ai-development/aid-2026-327-evidence"
    canonical_scope_keywords: ["AID-2026-327", "d10-cursor-authority"]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Evidence — AID-2026-327

## Decision authority

- Repository: oahcom/AiMemoryBrainArchitecture
- Base branch: main
- Base commit: 4a6cdd0e7c5dc0db53be37a2f945e02c59d5abf9
- Final Owner decision: [Issue #1210, comment 7174534633](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1210#issuecomment-7174534633), dated 2026-11-27.
- This Work Item records the final decision; it does not reopen it.

## Decision recorded

The canonical System Boundaries section 15 records:
1. One deployment has one logical Brain authority; tenant and shard are partition boundaries within that authority.
2. CanonicalCommitCursor is partitioned per tenant/shard; there is no total order across tenants or shards.
3. Authority identity and epoch/incarnation are explicit cursor identity; cursors from different authorities or epochs are incomparable.
4. A cross-shard transaction produces one cursor entry per participating shard and commits all or none; this does not create a cross-shard total order.
5. Aggregate revisions and lifecycle cursors remain separate domains.
6. ForgetFence and ProducerRegistrationHighWater are per-authority and carry authority identity plus applicable target/partition scope.
7. Required rejection cases are cursor_comparison_across_authority_rejected and cross_shard_commit_exposes_no_total_order.

## Branch result

- Branch: docs/aid-2026-327-d10-cursor-authority
- Canonical source blob after section 15: fd05a4d559a852fd24370297c7cd290384d9414a
- English and Chinese mirrors are pinned to that canonical blob.
- The canonical source remains Draft / Unverified. No formal approval is claimed.
- No code, runtime, API, schema, DDL, tests, workflows, branch-protection, or Issue-body changes are included.
- Detailed D/F/G consumer specifications, multi-shard transaction representation, and F/G consistent-snapshot/cut protocol remain follow-up work.

## Provenance and validation limits

- The prompt snapshot is operator-authored and not a verbatim platform prompt; executed prompt provenance is NOT_VERIFIED.
- Prompt digest/byte-count metadata has not been independently computed for this Work Item and is intentionally not asserted.
- The external implementing-session identifier is not recorded; no identity is inferred.
- No independent review or current-head CI result is claimed.
