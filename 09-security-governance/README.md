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
        - "AID-2026-109 bounded I root and scope correction"
        - "main correction base 7629b9de5e5832fe486ee72d101c4bc5121015e6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Informative root only; no I Owner policy acceptance or production conformance asserted."
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
    canonical_status: Canonical
    canonical_scope: "Informative I security-governance root and bounded source disposition"
    canonical_scope_id: "security-governance/root-index"
    canonical_scope_keywords:
      - security-governance
      - root-index
      - authorization
      - forget
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/09-security-governance/README.md"
    zh-CN: "docs/zh-CN/09-security-governance/README.md"
---
# Security, Identity & Governance

## Canonical scope

This directory is the canonical **informative root** for the I (Security, Identity & Governance) domain. It establishes the domain boundary and points to the architecture guide; it does not publish or approve the detailed policy contracts listed below.

**Policy-semantics acceptance authority:** I is the domain Owner responsible for accepting I policy semantics. This states the responsible authority; it does **not** mean that I has accepted any policy. No natural-person I Owner acceptance is recorded by this root.

## Controlling authority boundaries

- **AID-2026-089:** D is the sole logical authority for canonical ForgetOperation identity and ForgetFence generation/cursor and the D-domain completion predicate. I's policy responsibility does not mint/advance D Fence or redefine D completion.
- **AID-2026-099 HIR-18:** before replay disclosure, independently re-check current I authorization / PermissionEpoch / issuer validity and current D Fence / lineage. Denial or unknown fails closed. This root does not claim HIR-18 implementation or conformance.
- Storage-local Fence data, if present, is a D-derived rebuildable projection, not a second authority.

## Architecture guide

- [Security, Identity & Governance — Architecture Guide](security-governance-guide.md) — **RECONSTRUCTED_FROM_MIRROR**. The historical source branch has no Canonical guide at this path. The Canonical body is copied byte-for-byte from the existing EN mirror; the existing EN/ZH-CN mirror bodies are unchanged.

## Four detailed policy contracts — NOT_RESTORED_BY_DECISION

Each of the following is formally dispositioned as `NOT_RESTORED_BY_DECISION`:

- `forget-retention-backup-and-erasure-policy.md`
- `global-forget-target-inventory-and-completion-evidence.md`
- `principal-actor-and-authorization-contract.md`
- `scope-and-revocation-policy.md`

The F4/F6/F7 review passages identify the missing I root and its responsibilities; they do not enumerate these four detailed policy files as mandatory root contents. Restoring all four would require eight additional EN/ZH-CN mirror documents. That translation workload was not authorized by the bounded-root decision. Their disposition does not imply that their detailed policy content exists on main or has been accepted by I.

## Other historical I documents — NOT_RESTORED_BY_DECISION

- `audit-and-exception-governance.md` — not named as a required root by F4/F6/F7; outside the bounded root scope.
- `governance-decision-register.md` — historical decision register; importing it risks reviving dated decisions as current authority.
- `threat-model-and-adversarial-test-plan.md` — historical threat/test material, not the root named by the review.
- `security-and-identity-overview.md` — not restored; the existing architecture guide is used as the single root orientation document. Its interim import was removed by the scope-correction follow-up.

## Historical phase records

The source branch contains 81 phase records under `09-security-governance/`. They are classified by filename prefix in the AID-2026-109 evidence report and are not restored. No historical phase record is promoted to current normative authority.

## Gate A and remaining evidence

Gate A item 5's I sub-item moves from **root missing** to **root authored, guide reconstructed from mirror, and four detailed policy contracts formally dispositioned**. This is not “I policy semantics accepted”. Gate A remains PARTIAL / OPEN; Gate B remains NOT VERIFIED.

**COC/GID cryptographic sealed evidence is not touched and remains required** under #1211. This root does not provide sealed evidence, signer/key custody, quorum, anti-rollback, durable-log/recovery or production-topology proof.

## Evidence

Source branch: `session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6`.

See [AID-2026-109 scope-correction evidence](../14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md) for source and interim-main blob SHAs, the 81-record prefix counts, and the correction history.
