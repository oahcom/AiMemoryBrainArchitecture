# I — Exact Authority Review of H Recovery Cutoff Wire Contract 1.0.1

- Owner perspective: I — Security & Governance
- Review date: 2026-11-17
- I branch: `session-i-security-governance-2026-11-16`
- I branch HEAD at review: `8a90c91c442c91543b82f085efb0886b745be4da`
- I source contract: `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md`
- I source Blob: `929b30ba10ac627927d3959e0777b467846b268d`
- H prose contract Blob: `ee1ff065e60c030c633d93fcc9d480f5e8ae44e9`
- H schema target: `08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.1.schema.json`
- H schema Blob: `b3dd3cd3d491fefc50043b6eb5d696c73c6dda81`
- A D/I semantic review Blob: `1cef4000d79bb63aac960ef48055d61498dd675a`
- Decision: **CANDIDATE / NO I WIRE APPROVAL — REQUIRED I AUTHORITY FIELDS ARE NOT REPRESENTED**
- Provenance: delegated I-role security/authority review by the current joint developer session; not an independent human I signature or external governance approval.

## 1. I authority decision boundary

I confirms that the 1.0.1 schema's separation of request and admission enumerations, explicit I/D/C snapshot references, typed participant entries and owner-only release references is directionally compatible with I's recovery-gate model.

I does **not** approve this schema as a wire representation of I Phase 3.6.8. The I-specific authority tuple is materially underrepresented. A generic `secondary_high_waters` map and a single `scope_binding_digest` are not sufficient to represent, verify or authorize the I inventory and receipt boundaries.

## 2. Blocking I findings

### I-WIRE-01 — Missing PolicyDomain and exact Scope binding

I 3.6.8 requires `PolicyDomainRef` and the exact normalized Scope binding for every inventory, authorization and release proof. H 1.0.1 has only `scope_binding_digest`; it has no `policy_domain_ref` or typed `scope_refs` collection. A digest without an explicit authority namespace and retrievable scope membership is insufficient for I's cross-PolicyDomain isolation and registry lookup.

**Required:** add PolicyDomainRef, exact ScopeRefs (or a separately authenticated, version-pinned Scope manifest ref plus digest), and the scope-binding fingerprint. Missing or ambiguous scope remains UNKNOWN/deny.

### I-WIRE-02 — Request Gate snapshot is not the global inventory snapshot

I 3.6.8 expressly separates:
- I Gate/request ledger: IGateGeneration, IRequestHighWater, request set root/count, PermissionEpoch, I sequencer position;
- I global inventory: ProducerDomainInventoryEpoch, registry snapshot/change-set digest, relevant InventoryEntryRef/Generation set, TargetInventorySealRef/digest, completeness proof generation/status and signer/key-status generation.

H 1.0.1 encodes the former only in generic owner snapshot fields. It does not encode the latter as a typed record. `secondary_high_waters` cannot prove registry membership, entry-generation currentness or a sealed target universe.

**Required:** add a separately identifiable I global-inventory snapshot subrecord or separate I-signed message family. It must be joined to the I request snapshot by one immutable IReconciliationTuple; the two high-waters must remain distinct.

### I-WIRE-03 — Inventory currentness cannot be validated from the schema

The I 3.6.8 release/issuance predicate rechecks ProducerDomainInventoryEpoch, registry snapshot digest, each relevant entry generation, completeness/seal generations, signer/key status, PermissionEpoch, sequencer and anti-rollback generation at the final I sequencer/CAS transaction. H 1.0.1 carries none of the typed inventory or key-status generations.

**Required:** encode the candidate snapshot values and the exact currentness proof references. The semantic validator and I's final CAS remain authoritative; schema validity alone never authorizes issue, consume or release.

### I-WIRE-04 — Restore attempt identity and cross-owner currentness are absent

I 3.6.8 §6 requires RestoreAttemptRef, checkpoint generation/digest, restored sequencer/registry epochs, external anti-rollback anchor, current D fence/barrier/closure, COC recovery prefix/batch/manifest and applicable Storage participant reconciliation. H 1.0.1 has no RestoreAttemptRef or checkpoint identity.

**Required:** add a strict restore-context record. I Gate release after restore must bind the same RestoreAttemptRef and current D evidence; I release cannot clear D's Forget Fence or authorize Storage visibility.

### I-WIRE-05 — Storage participant receipt consumption tuple is not joined

I 3.6.8 §4 requires exact participant, GID, DB authority/incarnation, native XID where known, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, ParticipantTupleDigest, operation/request digests, owner boundary and COC intent position/digest. H 1.0.1 participant entries carry a generic participant digest and operation identity but no explicit Storage proof reference or complete immutable tuple.

**Required:** bind the Storage proof reference/digest and exact tuple join keys to the recovery manifest and I terminal/receipt-consumption evidence. Same participant, attempt and ledger version must be verified across I, COC and Storage.

### I-WIRE-06 — 1.0.1 schema version mismatch

The schema ID/title is 1.0.1, while each of its six message-family `schema_version` constants remains 1.0.0. This makes producer/consumer negotiation ambiguous and must be corrected in a new immutable schema revision.

## 3. Security constraints for the amended wire contract

1. I signs only I-owned request Gate, inventory, permission/revocation and release subrecords. H/COC cannot mint or infer them.
2. Each I subrecord binds issuer, subject, owner authority, audience, purpose, key/version, algorithm/canonicalization/digest profile refs, payload digest and signature evidence under an I-approved trust policy.
3. I key status and PermissionEpoch are checked at the final I issue/consume/release linearization point, not accepted from stale payload claims.
4. An inventory epoch advance invalidates affected inventory proof until revalidation; no stale seal may be reused.
5. A restore attempt with stale/forked sequencer, registry or anti-rollback evidence remains UNKNOWN and I Gate CLOSED.
6. Missing owner snapshot, missing member page, empty-without-proof, unregistered recipient, unknown scope, stale key or incomplete Storage join never means empty or safe.
7. I Gate release is I-local only. It does not release D Gate, clear ForgetFence, resolve Storage XID, prove physical erasure or imply Global Forget completion.

## 4. Required H amendment and I re-review

H must publish a new immutable schema revision with:
- one consistent schema version in all message definitions;
- explicit PolicyDomainRef and exact Scope binding;
- separate I request-ledger and global-inventory records;
- ProducerDomainInventoryEpoch, registry snapshot/change-set digests and entry generations;
- TargetInventorySeal/completeness status and generations;
- PermissionEpoch, I sequencer and signer/key-status generation;
- RestoreAttempt/checkpoint/anti-rollback tuple;
- Storage participant receipt/attempt/ledger tuple join;
- strict conditional requiredness and negative fixtures.

I will review the exact new schema Blob and the matching H mapping table. No approval carries forward from this review.

## 5. Status

- I 3.6.8 semantic proposal: **PROPOSED / EXACT I RE-REVIEW STILL REQUIRED**.
- H recovery-cutoff 1.0.1: **CANDIDATE / NO I WIRE APPROVAL**.
- I inventory proof / TargetInventorySeal: **NOT ISSUED / NOT EVIDENCED**.
- I36-GOV-01..10: **GOVERNANCE-BLOCKED**.
- I36 tests: **NOT RUN**.
- Cryptographic profile and key custody: **NOT APPROVED**.
- Global Forget completion / physical erasure / production activation: **NOT CLAIMED / NOT AUTHORIZED**.

This review does not alter BIH36-JD-01..17 and does not authorize any other Owner's contract or implementation.
