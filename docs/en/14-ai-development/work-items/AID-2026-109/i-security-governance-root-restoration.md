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
        - "AID-2026-109 bounded I root recovery evidence"
        - "main base a7e7c64bfd6c6d709a0a7b55358f94b8535815c1"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source branch, mirrors and dispositions recorded; no I policy acceptance inferred."
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
    canonical_scope: "Language mirror of AID-2026-109 bounded I security-governance root recovery evidence"
    canonical_scope_id: "ai-development/aid-2026-109-i-root-recovery"
    canonical_scope_keywords:
      - security-governance
      - source-restoration
      - not-restored-by-decision
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
---
# AID-2026-109 — Bounded I Security & Governance Root Recovery

**Attribution:** `user-authorized operator (delegated by account owner)`  
**Date:** 2026-11-26 · **ID:** `PROVISIONAL` · **Main:** `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`

## 1. Review derivation

F4 (review lines 176–193), F6 (214–231) and F7 (233–250) identify the missing I root and its responsibilities. The exact missing-path inventory (lines 96–100) names `09-security-governance/README.md`; the three reason paragraphs do not enumerate individual policy filenames. The review allows IMPL2/I to “restore or formally disposition” the root.

The source branch contains 91 files under `09-security-governance/`, including 81 phase records. This change does not import the tree.

## 2. Guide source determination

**`RECONSTRUCTED_FROM_MIRROR`, not restored.** The source branch tree was checked and contains no `09-security-governance/security-governance-guide.md`. Main already has EN mirror blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a` and ZH-CN mirror blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e`. The new Canonical body is byte-identical to the EN mirror; only GOV-DOC-002 frontmatter is added. Existing mirror body text is unchanged; GOV-DOC-002 frontmatter was added to both mirrors in this PR.

## 3. NOT_RESTORED_BY_DECISION

| Document | Source branch blob | Disposition | Reason |
|---|---|---|---|
| `forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `audit-and-exception-governance.md` | `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4` | `NOT_RESTORED_BY_DECISION` | Not enumerated as required root content; outside bounded scope. |
| `governance-decision-register.md` | `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | `NOT_RESTORED_BY_DECISION` | Historical decision register could revive dated decisions as current authority; outside bounded scope. |
| `threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` | `NOT_RESTORED_BY_DECISION` | Not named as the missing normative root; outside bounded scope. |
| `security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | `NOT_RESTORED_BY_DECISION` | Guide reconstructed from existing mirror; restoring this additional historical overview would duplicate content and require more mirror work. |

The four detailed policy contracts (first four rows) would require eight additional EN/ZH-CN mirror documents. This translation workload was not authorized; the review did not enumerate those detailed policies as required root files. Their formal disposition does not mean their contents exist on main or are accepted by I.

## 4. Phase-record prefix classification

All 81 phase records are excluded. Prefix counts: **phase-3: 1; phase-3.5: 1; phase-3.6: 30; phase-3.7: 1; phase-3.8: 47; phase-3.9: 1 (total 81)**. No phase record is promoted to current normative authority.

## 5. Authority and acceptance

- I is the policy-semantics acceptance authority; no I Owner acceptance is recorded.
- AID-2026-089: D alone owns canonical ForgetOperation identity, ForgetFence generation/cursor and D-domain completion predicate. I must not mint/advance D Fence or redefine D completion.
- AID-2026-099 HIR-18: before replay disclosure, independently re-check current I authorization/PermissionEpoch/issuer validity and current D Fence/lineage; denial/unknown fails closed.
- README and guide remain Draft / Informative; `approved_version: null`. No normative acceptance or production conformance asserted.

## 6. Gate A and boundary

Gate A item 5's I sub-item moves from **root missing** to **root authored, guide reconstructed from mirror, four detailed policy contracts formally dispositioned**. This is not “I policy semantics accepted”. Gate A remains PARTIAL / OPEN; Gate B NOT VERIFIED.

No changes to 03/04/05, runtime, validator semantics, tests, scripts, workflows, schemas, APIs, DDL, deployment or production configuration. No Issue closed.


## 7. Existing guide mirror metadata

The existing mirror bodies remain byte-for-byte unchanged. GOV-DOC-002 frontmatter was added so the three guide counterparts are all present in this PR:

| Mirror | Original full-file blob | New full-file blob |
|---|---|---|
| `docs/en/09-security-governance/security-governance-guide.md` | `061c5847b3df879eeaf3c71e5eae0bfa162b276a` | `688dd950b844e977cef23bc28ab69255927bb181` |
| `docs/zh-CN/09-security-governance/security-governance-guide.md` | `372d27c79dc79d09bcdb0f142c979efdba1c2b6e` | `f5aa06bbde32e1b67f81ce43796fd461a6b1e0af` |
