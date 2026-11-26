---
document_metadata:
  domain: security-governance
  role: review-report
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
        - "AID-2026-109 — bounded I source-root restoration audit"
        - "Source branch session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Audit report and source blob readback; does not assert I Owner acceptance or production conformance."
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
    canonical_scope: "AID-2026-109 I security-governance source-root restoration audit"
    canonical_scope_id: "ai-development/aid-2026-109-i-root-restoration"
    canonical_scope_keywords:
      - security-governance
      - source-restoration
      - phase-freeze
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
---
# I Security & Governance Normative-Root Recovery — AID-2026-109

**Attribution:** `user-authorized operator (delegated by account owner)`  
**Date:** 2026-11-26  
**ID status:** `PROVISIONAL`  
**Latest main fetched immediately before commit:** `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`  
**INDEX allocation readback:** maximum `AID-2026-108`; `AID-2026-109` absent; assigned next.  
**Historical source:** `session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6`

## 1. Derivation from F1–F8

The current-main composition review identifies three I-root blockers:

- **F4, lines 180–181:** “I global policy root absent”; I is required for authorization, retention and residual-exception policy.
- **F6, lines 218–219:** “I normative root absent”; the Scope/Permission model leaves policy and cache/revocation guarantees open; I must supply issuer, signed decision/attestor, PermissionEpoch, revocation/cache freshness and verifier.
- **F7, lines 237–238:** “I root absent”; D explicitly leaves global completion and physical erasure to I; inventory, backup/external-copy and exception policy are not accepted.

F1–F3 and F5 do not identify the missing I root as their primary blocker. F8 is a Storage/Consistency physical atomicity, durability, crash and restore gap, not an I-root gap.

**Filename evidence boundary:** the review itself names `09-security-governance/README.md` as `NOT_FOUND_ON_MAIN`; the F4/F6/F7 reason paragraphs say “I root” but do not enumerate the five policy filenames. The five source documents below are the narrowly selected candidates supplied by the assignment and mapped to those responsibilities. They are not represented as literal filenames quoted by F4/F6/F7.

## 2. Restricted selection

The source branch contains 91 files under `09-security-governance/`. This recovery restores only the five selected source documents plus a newly authored README navigation root. It does not copy audit registers, phase-3.x decision records, self-reviews, tests, reference models, or the remaining historical branch files.

## 3. Source / restored blob comparison

The canonical files preserve the complete source document body byte-for-byte. The only prefix added is GOV-DOC-002 frontmatter; no source prose was rewritten. The third SHA is the Git blob SHA of the newly added frontmatter block itself.

| Restored canonical path | Source blob SHA | New full-file blob SHA | Frontmatter-only blob SHA | Disposition |
|---|---|---|---|---|
| `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | `0d6f49a54522ad0ccd541bf4f1abf486e6b4b2cc` | `5691d1c392f796325de4b378341c9b67455ee608` | CURRENT — Candidate / Informative |
| `09-security-governance/forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | `92312ab9f4f31d775ea5cab5ccb44679c7a6b140` | `7ff3fe4d17677a0b4f173544a77d640ab182eb05` | CURRENT — Candidate / Informative |
| `09-security-governance/principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | `505588d330778bf2c228d621a3db4cfbedaeb7be` | `ffafb5d3e777dac25164cefe8675bcec7d307307` | CURRENT — Candidate / Informative |
| `09-security-governance/scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | `6398d21cb3c8ed77c2080412d20cd9cc23a253b0` | `b78f4f675e4f4f00e85cd24abb167f3190e9d845` | CURRENT — Candidate / Informative |
| `09-security-governance/security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | `bbabc755216b113a1580d3a6dab8a932700eb7d1` | `0488c9bac114dfd311e5076765faf5a2f0cb39f3` | CURRENT — Candidate / Informative |

README is newly authored (there is no README blob on the source branch); it is an informative index, not a recovered historical policy.

## 4. Replacement / authority determination

All five restored documents are **CURRENT as informative candidate source material**, not current normative authority:

| Document | Mapping | Determination |
|---|---|---|
| global-forget-target-inventory-and-completion-evidence.md | F4 / F7 | CURRENT — Informative; I global inventory, target evidence and completion policy |
| forget-retention-backup-and-erasure-policy.md | F4 / F7 | CURRENT — Informative; I retention, backup, external-copy and physical-erasure policy |
| principal-actor-and-authorization-contract.md | F6 | CURRENT — Informative; I authorization semantics, with B retaining ActorRef/ScopeRef type semantics |
| scope-and-revocation-policy.md | F6 | CURRENT — Informative; I policy, PermissionEpoch, revocation and cache freshness |
| security-and-identity-overview.md | F4 / F6 / F7 | CURRENT — Informative overview; its embedded historical baseline references remain provenance, not a new current-main pin |

No selected document was marked `SUPERSEDED_BY`: inspection found no authority claim that must be displaced by AID-2026-089 or AID-2026-099. This is a non-supersession finding, not a claim that the source documents are approved. All remain `decision_status: Draft`, `approved_version: null`, `normative_status: Informative`. No Owner acceptance is created by this restoration.

## 5. Alignment with AID-2026-089 and AID-2026-099 HIR-18

- **AID-2026-089:** D alone issues ForgetOperation identity and ForgetFence generation/cursor. The restored I documents retain I's authorization/global-completion/retention role and do not transfer Fence issuance, lineage authority or canonical suppression to I or Storage.
- **AID-2026-099 HIR-18:** replay disclosure must independently recheck current I authorization/PermissionEpoch/issuer status and current D Fence/lineage; either denial or unknown blocks disclosure. The I documents provide candidate policy semantics only. This restoration does not claim HIR-18 implementation, cross-owner acceptance, cryptographic verifier readiness or runtime conformance.
- Storage-local Fence records remain D-derived, rebuildable projections only; no competing authority is introduced.

## 6. Gate A and Issue impact

The I source-presence sub-item previously recorded OPEN because `09-security-governance/README.md` and the I policy roots were absent. After this restoration it becomes:

**RESTORED_CANDIDATE_SOURCE_PRESENT / INFORMATIVE — exact-version I Owner validation and acceptance still OPEN.**

This does not close Gate A. Gate A remains PARTIAL / OPEN; Gate B remains NOT VERIFIED. No natural-person Owner signature, policy ratification, implementation acceptance or production conformance is claimed.

## 7. #1211 COC / GID cryptographic evidence boundary

**Not touched; still required.** This work restores I governance source material only. It does not restore or validate the Storage/Consistency COC/GID source set, sealed cryptographic evidence, signer/key custody, quorum, anti-rollback, durable-log/recovery, backup/restore or production topology. #1211 remains OPEN.

## 8. Change boundary

No changes to 03/04/05 domains; no runtime/product code, validator code or validator semantics, tests, scripts, workflows, schemas, APIs, DDL, deployment or production configuration. No Issue is closed.
