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
        - "AID-2026-109 scope correction; main base 7629b9de5e5832fe486ee72d101c4bc5121015e6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Records the correction to the merged AID-2026-109 scope; does not assert I Owner acceptance or production conformance."
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
    canonical_scope: "AID-2026-109 I root scope correction and restoration evidence"
    canonical_scope_id: "ai-development/aid-2026-109-i-root-restoration"
    canonical_scope_keywords:
      - security-governance
      - source-restoration
      - not-restored-by-decision
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
---
# AID-2026-109 — I Root Scope Correction and Bounded Recovery Evidence

**Attribution:** `user-authorized operator (delegated by account owner)`  
**Proxy note:** 代理登记，非自然人 Owner 签署  
**Date:** 2026-11-26  
**Work Item:** AID-2026-109 (`id_status: PROVISIONAL`)  
**Correction base:** `7629b9de5e5832fe486ee72d101c4bc5121015e6`

## 1. Why this correction exists

PR #1300 merged AID-2026-109 as merge commit `e3a134de856bbb58581fd688462c9c0282631270`. That interim version restored five historical I documents (four detailed policy contracts plus the Security/Identity overview). A later user instruction narrowed the scope: restore the guide from the existing mirror, write the README in three locations, and formally disposition those eight historical documents rather than importing the detailed policies.

This follow-up removes the five interim Canonical documents and their ten EN/ZH-CN mirrors. It preserves the already merged I-root registration in `00-governance/document-scope-registry.yaml` and `scripts/check_bilingual_docs.py::NORMATIVE_ROOTS`; it does not change checker logic or pairing exemptions.

PR #1301 was a separate draft attempt against an earlier base; GitHub now records it CLOSED and `merged=false`. It was not merged by this operator. This correction is based on the current main after the AID-110 merge.

## 2. Review derivation — F4/F6/F7

The 2026-11-26 A–I + Storage composition review identifies the missing I root in F4, F6 and F7. Its exact missing-path inventory names `09-security-governance/README.md`; the F4/F6/F7 reason paragraphs describe I responsibilities but do not enumerate the eight historical filenames below. The review permits “restore or formally disposition”.

- **F4:** I global policy root absent; authorization, retention and residual-exception policy responsibilities remain open.
- **F6:** I normative root absent; Scope/Permission policy and cache/revocation guarantees remain unspecified.
- **F7:** D leaves global completion and physical erasure policy to I; inventory, backup/external-copy and exception policy remain unaccepted.
- **F8 is excluded:** it is Storage/Consistency physical atomicity, durability, crash and restore evidence, not an I-root omission.

## 3. Guide provenance

**Classification: `RECONSTRUCTED_FROM_MIRROR`.**

The source branch `session-i-security-governance-2026-11-16` at `8abddf814467b271344a9814613a6b7ca6a446c6` has no `09-security-governance/README.md` and no `09-security-governance/security-governance-guide.md`.

Main already had these guide mirrors:
- EN original full-file blob: `061c5847b3df879eeaf3c71e5eae0bfa162b276a`
- ZH-CN original full-file blob: `372d27c79dc79d09bcdb0f142c979efdba1c2b6e`

The new Canonical guide body is byte-identical to the EN mirror. The existing EN and ZH-CN guide bodies are byte-identical to their prior main versions; only GOV-DOC-002 frontmatter was added to both mirrors.

| Guide path | Original / source blob | Corrected PR blob |
|---|---|---|
| `09-security-governance/security-governance-guide.md` | Source branch: NOT_FOUND | `0c88125480f46b2bd264dd6fd8c1f92423edd531` |
| `docs/en/09-security-governance/security-governance-guide.md` | `061c5847b3df879eeaf3c71e5eae0bfa162b276a` | `70ba84ce1ccaf1bbd316e93728a6765de553e11a` |
| `docs/zh-CN/09-security-governance/security-governance-guide.md` | `372d27c79dc79d09bcdb0f142c979efdba1c2b6e` | `54cb0ae5cfe8278a2f22b9ebaeed2e591651cf37` |

The Canonical guide and both mirrors remain Draft / Informative, with `approved_version: null`.

## 4. NOT_RESTORED_BY_DECISION register

The following table records source-branch blob SHA and, where the interim AID-109 merge had imported a file, its pre-correction main Canonical and mirror blobs. The corrective PR deletes those interim imports so the final main state is genuinely “not restored”.

| Document | Source branch blob | Interim main Canonical blob | Interim EN mirror | Interim ZH-CN mirror | Final disposition |
|---|---|---|---|---|---|
| `forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | `ab2b28829100ca1f2a17d203396b910fe3979bff` | `e3bd438c76fb4ba7b2af8342dbbb1ef5c4dc6e86` | `8117fc33573ef743c23a5ab0e8d9f9ea65f78fd9` | `NOT_RESTORED_BY_DECISION` |
| `global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | `c0ba8b2dacc115e29233268e62d5ababfc26a025` | `c453b8703a3dd93d5b1d0c5d3dc008d1afa53ebb` | `14d6b7c377ca9ce39c3c31372c55803d4ce0f69c` | `NOT_RESTORED_BY_DECISION` |
| `principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | `b8073340cb2efba990c038e0b628ee6e9d0f24da` | `eee995574ffda289e3ad29aa1919c09806f19057` | `fc127f028bca96c3bee21d8da8e51a0b508d1fe2` | `NOT_RESTORED_BY_DECISION` |
| `scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | `b4c66e90afdb57c5b60d37ad86554ccae6292e9a` | `8eef867241bdb25c01d2f9b7332f7e485def101f` | `887949ca54745e6c30cf8e402da5229bab861032` | `NOT_RESTORED_BY_DECISION` |
| `audit-and-exception-governance.md` | `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4` | NOT_PRESENT | NOT_PRESENT | NOT_PRESENT | `NOT_RESTORED_BY_DECISION` |
| `governance-decision-register.md` | `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | NOT_PRESENT | NOT_PRESENT | NOT_PRESENT | `NOT_RESTORED_BY_DECISION` |
| `threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` | NOT_PRESENT | NOT_PRESENT | NOT_PRESENT | `NOT_RESTORED_BY_DECISION` |
| `security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | `e9c71b15e19e9289bffa4d98bdfe254cc66a0b83` | `7764d0692d432979b02849fe865404ee4eed8768` | `1ba7a813a76b9b2c62e4431fe6419aaa9988a2a7` | `NOT_RESTORED_BY_DECISION` |

### Why the four detailed policies are not restored

The first four rows are detailed policy contracts. Restoring them would require eight additional EN/ZH-CN mirror documents. That translation workload was not authorized, and F4/F6/F7 did not enumerate these detailed policy filenames as mandatory root contents. Their formal disposition does not imply that their policy content is present on final main or accepted by I.

The other four rows are also formally dispositioned. The overview is removed because the existing architecture guide is the single root orientation document; the audit register, decision register and threat-model/test-plan are historical materials outside the required root.

## 5. Phase-record prefix classification

The source branch contains 91 files under `09-security-governance/`; 81 match the phase-record filename pattern. None is restored.

| Filename prefix | Count |
|---|---:|
| `phase-3` | 1 |
| `phase-3.5` | 1 |
| `phase-3.6` | 30 |
| `phase-3.7` | 1 |
| `phase-3.8` | 47 |
| `phase-3.9` | 1 |
| **Total** | **81** |

## 6. Authority and acceptance boundaries

- I is the designated acceptance authority for I policy semantics; this correction does not claim I accepted any policy.
- **AID-2026-089:** D remains the sole logical authority for ForgetOperation identity and ForgetFence generation/cursor and D-domain completion predicate. I must not mint/advance D Fence or redefine D completion.
- **AID-2026-099 HIR-18:** replay disclosure independently rechecks current I authorization/PermissionEpoch/issuer validity and current D Fence/lineage; denial or unknown fails closed.
- README and guide are Draft / Informative with `approved_version: null`. No Owner acceptance, production conformance or HIR-18 implementation is claimed.

## 7. Gate A item 5 and #1211

Gate A item 5's I sub-item changes from **root missing** to **root authored, guide reconstructed from mirror, and four detailed policy contracts formally dispositioned**. This is the review's “restore or formally disposition” path. It is not “I policy semantics accepted”. Gate A remains PARTIAL / OPEN; Gate B remains NOT VERIFIED.

**COC/GID sealed cryptographic evidence is untouched and still required.** This correction does not restore or validate COC/GID sealed evidence, signer/key custody, quorum, anti-rollback, durable-log/recovery, backup/restore or production topology. #1211 remains OPEN.

## 8. Change boundary

This correction removes the five interim I Canonical documents and their ten mirrors, adds the Canonical guide and README language set, and updates AID-2026-109 evidence. It does not change 03/04/05, Runtime, product validator semantics, tests, workflows, schemas, APIs, DDL, deployment or production configuration. It does not close #1211 or #1212.
