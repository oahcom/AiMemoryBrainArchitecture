---
document_metadata:
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
        - "14-ai-development/work-items/AID-2026-109/prompt-v2-scope-correction.md"
        - "AID-2026-109 scope correction on 2026-11-26"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Delegated user scope correction v2; not an Owner approval."
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
    canonical_scope: "AID-2026-109 delegated work record"
    canonical_scope_id: "ai-development/aid-2026-109-correction-record"
    canonical_scope_keywords:
      - work-item
      - scope-correction
      - security-governance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# AID-2026-109 — user scope correction v2

Date: 2026-11-26  
Attribution: user-authorized operator (delegated by account owner)  
This correction supersedes the earlier broad five-document restoration scope for the final main state.

1. Reconstruct `09-security-governance/security-governance-guide.md` from the existing main EN mirror if the source branch lacks it. Classification must be `RECONSTRUCTED_FROM_MIRROR`, not restored. Keep the existing EN/ZH-CN mirror bodies unchanged; add GOV-DOC-002 metadata as required.
2. Create `09-security-governance/README.md` and its EN/ZH-CN mirrors. It must define canonical scope, state I is the policy-semantics acceptance authority without claiming I has accepted policy, and align with AID-2026-089 and AID-2026-099 HIR-18.
3. The four detailed policy contracts are `NOT_RESTORED_BY_DECISION`: `forget-retention-backup-and-erasure-policy.md`, `global-forget-target-inventory-and-completion-evidence.md`, `principal-actor-and-authorization-contract.md`, and `scope-and-revocation-policy.md`. Do not restore them. Restoring all four would require eight EN/ZH-CN mirrors; this translation work was not authorized and these detailed policy filenames were not review-named required root content.
4. Also `NOT_RESTORED_BY_DECISION`: `audit-and-exception-governance.md`, `governance-decision-register.md`, `threat-model-and-adversarial-test-plan.md`, and `security-and-identity-overview.md`. The latter was temporarily imported by the first AID-109 merge and must be removed with its mirrors in this correction.
5. Classify all 81 source-branch phase records by filename prefix; restore none.
6. Gate A item 5 I sub-item is: root authored, guide reconstructed from mirror, four detailed policies formally dispositioned. Do not say “I policy semantics accepted”. Gate A remains open.
7. COC/GID sealed cryptographic evidence is untouched and remains required under #1211.
8. Keep #1211 and #1212 open; after correction merge, post one accurate status comment to each. No 03/04/05 changes, no Runtime or product-validator semantics changes, no Issue closure.

The first AID-109 PR #1300 had already merged before this scope correction and temporarily imported five historical documents. The follow-up must remove those interim imports. Preserve AID-2026-109 as the Work Item ID; do not allocate a duplicate ID.
