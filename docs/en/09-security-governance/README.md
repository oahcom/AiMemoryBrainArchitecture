---
document_metadata:
  domain: security-governance
  role: index
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
        - "AID-2026-109 bounded I source-root recovery"
        - "Source branch session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Navigation index only; linked contracts remain Candidate/Informative and unaccepted."
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
    canonical_scope: "Bounded I security-governance source-root navigation"
    canonical_scope_id: "security-governance/root-index"
    canonical_scope_keywords:
      - security-governance
      - source-root
      - navigation
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/README.md"
---

# Security, Identity & Governance

This is the bounded canonical entry point for the restored I-domain source set.

## Scope of this recovery

AID-2026-109 restores only five policy/contract documents selected against the I-root blockers in F4, F6 and F7 of the 2026-11-26 A–I + Storage composition review. It does **not** import the historical `session-i-security-governance-2026-11-16` tree wholesale. That branch contains 91 files under this domain; the other files are not restored by this work item.

The five documents have `canonical_status: Canonical` in their respective frontmatter. Each document's own frontmatter is the sole authority for its `canonical_status`; this README is an informational guide, not a normative source for document status. Their presence does not ratify Phase 3.x decisions, approve a production policy, or establish implementation/conformance evidence.

## Canonical I documents

- [Global Forget Target Inventory and Completion Evidence Contract](global-forget-target-inventory-and-completion-evidence.md)
- [Forget, Retention, Backup and Physical Erasure Policy](forget-retention-backup-and-erasure-policy.md)
- [Principal, ActorRef and Authorization Contract](principal-actor-and-authorization-contract.md)
- [Scope and Revocation Policy](scope-and-revocation-policy.md)
- [Security, Identity & Governance Overview](security-and-identity-overview.md)

## Authority boundaries that remain controlling

- **D is the sole logical authority** for ForgetOperation identity and ForgetFence generation/cursor. I owns authorization, retention, global inventory/completion policy and physical-erasure requirements; it does not issue or advance D's Fence. See AID-2026-089.
- **H replay disclosure independently rechecks current I authorization and current D Fence/lineage**, fail-closed. A historical receipt/signature is not current authorization. See AID-2026-099 HIR-18.
- Storage-local Fence data, if present, is a D-derived rebuildable projection, not a second authority.
- All five restored documents are `normative_status: Informative`, `decision_status: Draft`, and have no `approved_version`. Exact Owner acceptance and implementation evidence remain outstanding.

## Evidence

Original source branch: `session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6`.

Restoration and source/new blob comparisons are recorded in [AID-2026-109](../14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md).
