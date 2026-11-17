# H — Phase 3.6.9 Recovery Cutoff Wire Contract Exact Review

- Owner perspective: H — BMCP Protocol
- Review date: 2026-11-17
- H branch: `session-h-bmcp-protocol`
- H branch HEAD at review: `a6659e457fc1bb7ca473f645fcdf4e6dc860e3e6`
- H prose contract Blob: `ee1ff065e60c030c633d93fcc9d480f5e8ae44e9`
- H schema 1.0.1 Blob: `b3dd3cd3d491fefc50043b6eb5d696c73c6dda81`
- A D/I reconciliation report Blob: `1cef4000d79bb63aac960ef48055d61498dd675a`
- I 3.6.8 source Blob: `929b30ba10ac627927d3959e0777b467846b268d`
- D 3.6.8 source Blob: `0668667daeb936bf223ab04921ea2a4117c3b09`
- B typed-reference registry Blob: `e7a1ced41421230bd41a3f68a1074bd95721adc0`
- Decision: **ACCEPT THE 1.0.1 STRUCTURAL REFINEMENTS; REJECT FULL WIRE-CLOSURE CLAIM — BLOCKING AMENDMENTS REQUIRED**
- Provenance: delegated H-role technical review by the current joint developer session; not an independent human H signature.

## 1. Review scope and positive findings

The 1.0.1 candidate materially improves the 1.0.0 draft:
1. Request and admission enumerations now have separate status/count/root fields.
2. The recovery batch requires I, D and C snapshot refs and digests.
3. COC participant manifest entries are typed with owner, operation identity, participant digest and prefix coordinates.
4. Release attestations bind request/admission roots and scope generation.
5. Recovery epoch completion requires three owner-release references.

These changes address the specific 1.0.0 defects identified in H's §8 refinement. The 1.0.1 schema is a meaningful structural improvement, but it is not yet a complete wire mapping of the pinned I/D amendments.

## 2. Blocking findings

### H-RC-09 — Schema version constants contradict the 1.0.1 schema identity (P1)

The file `bmcp.recovery-cutoff-1.0.1.schema.json` declares an ID/title for 1.0.1, but all six message-family definitions still constrain `schema_version` to `1.0.0`. A producer emitting 1.0.1 is rejected; a producer emitting 1.0.0 is accepted under the 1.0.1 schema. This defeats explicit version negotiation and makes the current candidate internally inconsistent.

**Required correction:** publish a new immutable schema revision whose six message definitions all require the same version as its schema ID/title. Add a negative test proving 1.0.0 is rejected by 1.0.1 and a positive test proving 1.0.1 is accepted.

### H-RC-10 — I global inventory and request-ledger snapshots are still conflated (P0)

I 3.6.8 §2 requires an `IReconciliationTuple` binding two distinct I-owned completeness domains:
- request Gate: `IGateGeneration`, `IRequestHighWater`, request-ledger root, `PermissionEpoch`, I sequencer position;
- global inventory: `PolicyDomainRef`, exact Scope binding, `ProducerDomainInventoryEpoch`, registry snapshot/change-set digests, relevant `InventoryEntryRef + InventoryEntryGeneration` set, `TargetInventorySealRef/digest`, completeness-proof generation/status and signer/key-status generation.

The 1.0.1 `ownerSnapshot` has generic gate/request/admission fields, a generic `secondary_high_waters` map and a single `scope_binding_digest`. It has no explicit `policy_domain_ref`, `scope_refs`, `permission_epoch`, `producer_domain_inventory_epoch`, registry snapshot/change-set digest, inventory-entry generation set, target-seal ref/digest, completeness generation/status or signer/key-status generation. A generic counter map cannot substitute for the typed inventory snapshot or its digest commitments.

**Required correction:** represent the I request Gate snapshot and I global inventory snapshot as distinct typed subrecords in the I owner attestation (or as two separately signed I message families). Make the complete I fields required when `owner_kind=I`. Preserve I's authority over both records; do not infer global completeness from request-ledger completeness.

### H-RC-11 — D owner snapshot does not encode the exact D barrier/closure tuple (P0)

D 3.6.8 §3–5 requires D evidence to bind `ForgetOperationRef`, request digest, `PolicyDomainRef`, exact Scope binding, D `FenceGeneration`, fence-installation cursor, producer-registration and work/attempt high-waters, barrier-membership root/count/generation, dependency-closure digest/cursor, and the exact I inventory epoch/registry projection observed by D.

The 1.0.1 owner snapshot has generic `gate_generation`, request/admission high-waters and `scope_generation`, but no typed ForgetOperation, D fence installation cursor, barrier root/count, dependency-closure digest/cursor or I registry projection. This prevents the wire verifier from proving that the D and I subrecords refer to the same Forget operation and reconciliation attempt.

**Required correction:** add a D-discriminated subrecord with the D-owned fields and the exact I inventory projection reference/digest. Do not rename generic counters and assume they carry the D semantics.

### H-RC-12 — RestoreAttempt and cross-owner restore currentness are absent (P0)

I 3.6.8 §6 and D 3.6.8 §5 require a restore release handshake bound to exact `RestoreAttemptRef`, checkpoint generation/digest, restored sequencer/registry epochs, external anti-rollback anchor, current D fence/barrier/closure, COC recovery prefix/batch/manifest and applicable Storage participant reconciliation.

The 1.0.1 schema has no `restore_attempt_ref`, checkpoint identity/digest or typed restore reconciliation tuple. A generic `anti_rollback_anchor_ref` alone cannot distinguish two restore attempts or prove which checkpoint and owner snapshots were reconciled.

**Required correction:** add a strict restore context subrecord and require it on restore-related owner snapshots, gate releases and recovery completion. Release must be bound to the same restore attempt across I and D.

### H-RC-13 — Storage participant join is not explicit in recovery wire (P1)

I 3.6.8 §2 and §4 require, where applicable, the complete Storage join: PreparedParticipantRef/GID, DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, ParticipantTupleDigest, operation/request digests, owner boundary and COC prepare-intent position/digest. The 1.0.1 `participant_entries` only carries a generic participant digest and operation identity. The separate Storage proof schema does not automatically bind that proof to the recovery batch.

**Required correction:** add a typed Storage participant proof reference/digest and exact participant tuple fields (or an explicit typed reference to the Storage proof plus all immutable join keys) in the participant manifest/recovery batch. Validate that the I receipt-consumption tuple, COC participant entry and Storage proof resolve to the same attempt and ledger version.

## 3. Required H schema amendment

Create a new immutable schema revision (recommended 1.0.2) with:
- consistent schema ID/title/message `schema_version` constants;
- I-discriminated request-gate and global-inventory subrecords;
- D-discriminated Forget/fence/barrier/lineage subrecord;
- explicit PolicyDomainRef and exact ScopeRef set/binding;
- restore-attempt context and cross-owner restore references;
- Storage participant proof/tuple join;
- strict conditional requiredness by owner kind and operation context;
- negative fixtures for missing I inventory fields, missing D barrier fields, absent restore attempt, mismatched PolicyDomain/Scope, stale inventory epoch, stale D fence, missing Storage tuple and wrong schema version.

The schema may define structure and requiredness only. I remains sole authority for signature trust, key lifecycle, PermissionEpoch, inventory membership and I Gate. D remains sole authority for ForgetFence and D barrier semantics. Storage remains sole authority for its participant ledger and visibility. H does not approve those owner decisions.

## 4. Required consumer review sequence

1. H publishes the amended schema and a mapping table against exact I 3.6.8 and D 3.6.8 blobs.
2. I reviews the I-specific wire fields and signer/trust boundary on the exact new schema.
3. D reviews the D fence/barrier/restore fields on the exact new schema.
4. B confirms nominal reference/cursor distinctions.
5. A performs final integration review and pins the same schema digest.
6. Execute structural and semantic validator suites; record raw CI evidence. H36 and I36 remain separate tests.

## 5. Current disposition

- 1.0.1 structural refinements: **ACCEPTED AS CANDIDATE IMPROVEMENTS**.
- H recovery-cutoff wire contract overall: **NOT ACCEPTED / NOT FROZEN**.
- H-RC-09: OPEN until version constants and tests are corrected.
- H-RC-10 / H-RC-11 / H-RC-12: BLOCKING for I/D recovery and restore wire closure.
- H-RC-13: BLOCKING for exact Storage participant recovery join.
- Cryptographic profile, canonical-byte interoperability, semantic validators, H36/I36 execution and production deployment: NOT APPROVED / NOT RUN as applicable.
- No change to BIH36-JD-01..17; no A gate is closed by this review.
