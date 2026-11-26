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
        - "AID-2026-109 bounded I governance root; main base a7e7c64bfd6c6d709a0a7b55358f94b8535815c1"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Informative root only; no I Owner acceptance or production conformance asserted."
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
    canonical_scope: "Language mirror of the informative I security-governance root"
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
    source: "09-security-governance/README.md"
    en: null
    zh-CN: "docs/zh-CN/09-security-governance/README.md"
---
# Security, Identity & Governance

## Canonical scope

This is the canonical **informative root** for the I (Security, Identity & Governance) domain. It orients readers to identity, authorization policy, revocation, retention, audit governance, cross-system Forget policy and evidence acceptance. It is not a detailed policy contract or production security certification.

**Acceptance authority:** I is the domain Owner responsible for accepting policy semantics. This states who must accept them; it does **not** assert that I has accepted any policy. No natural-person I Owner acceptance is recorded here.

- **AID-2026-089:** D remains the sole logical authority for canonical ForgetOperation identity and ForgetFence generation/cursor and D-domain completion predicate. I policy must not mint/advance D Fence or redefine D completion.
- **AID-2026-099 HIR-18:** before replay disclosure, independently re-check current I authorization/PermissionEpoch/issuer validity and current D Fence/lineage; denial or unknown fails closed. This root does not claim HIR-18 implementation or conformance.

## Architecture guide

- [Security, Identity & Governance — Architecture Guide](security-governance-guide.md) — `RECONSTRUCTED_FROM_MIRROR`; source branch has no guide blob at this path; canonical body is copied byte-for-byte from the existing EN mirror.

## Four detailed policy contracts not restored

Each is formally dispositioned as `NOT_RESTORED_BY_DECISION`. F4/F6/F7 identify the missing I root and its responsibilities; they do not enumerate these four detailed policy files as mandatory root files. Restoring all four would require eight additional EN/ZH-CN mirror documents. That translation workload was not authorized and would imply detailed policy text is present/accepted when it is not.

- `forget-retention-backup-and-erasure-policy.md` — `NOT_RESTORED_BY_DECISION`; source blob `f14cb2149ca3f817229533005ab89dbdc7f0b3a8`. Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.
- `global-forget-target-inventory-and-completion-evidence.md` — `NOT_RESTORED_BY_DECISION`; source blob `9100061fa986fb6676656169de3fcf9fc1c72664`. Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.
- `principal-actor-and-authorization-contract.md` — `NOT_RESTORED_BY_DECISION`; source blob `03765efac4bb1153f303ce0030f9e277d602e81d`. Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.
- `scope-and-revocation-policy.md` — `NOT_RESTORED_BY_DECISION`; source blob `71df6aaf21bb1767cd9fe5c947581b871325e023`. Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.

## Other historical I documents not restored

- `audit-and-exception-governance.md` — `NOT_RESTORED_BY_DECISION`; source blob `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4`. Not enumerated as required root content; outside bounded scope.
- `governance-decision-register.md` — `NOT_RESTORED_BY_DECISION`; source blob `f5fd2558c657f4ef49396a7a00cdbcd0f226f853`. Historical decision register could revive dated decisions as current authority; outside bounded scope.
- `threat-model-and-adversarial-test-plan.md` — `NOT_RESTORED_BY_DECISION`; source blob `4227ac0e26228ca3504589efdee022b5d0802e12`. Not named as the missing normative root; outside bounded scope.
- `security-and-identity-overview.md` — `NOT_RESTORED_BY_DECISION`; source blob `26a990e44709d8604ae515a2a63b510400fd8471`. Guide reconstructed from existing mirror; restoring this additional historical overview would duplicate content and require more mirror work.

## Historical phase records

The source branch has 81 phase records under this directory. They are classified by filename prefix in the AID-2026-109 report and are not restored. No historical phase record is promoted to current normative authority.

## Gate A status

Gate A item 5's I sub-item changes from **root missing** to **root authored, guide reconstructed from mirror, and four detailed policy contracts formally dispositioned**. This is not “I policy semantics accepted”. Gate A remains PARTIAL / OPEN; Gate B remains NOT VERIFIED.
