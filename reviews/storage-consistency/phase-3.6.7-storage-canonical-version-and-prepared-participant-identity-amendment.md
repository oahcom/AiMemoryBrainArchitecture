# Phase 3.6.7 — Storage Canonical Version Binding & PreparedParticipant Identity Amendment

- Owner perspective: Storage / Consistency
- Status: **OWNER-BRANCH PROPOSAL — EXACT REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT DEPLOYED
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`

## 1. Exact source pins and version decision

This amendment reconciles the following immutable artifacts:

| Role | Exact artifact | Blob |
|---|---|---|
| Storage Design v2 | `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v2.md` | `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` |
| Current COC persistence protocol | `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md` | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| Superseded companion clarification | same COC protocol path, earlier immutable version | `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` |

**Canonical version relationship (corrected after exact cross-reference inspection):**

1. Storage Design v2 Blob `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` is a preserved historical predecessor, not the current companion target for COC protocol `8ac178...`.
2. Storage Design v3.1 Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca` is the current Storage design candidate on this branch and contains the §§15.1–15.7 explicitly required by COC protocol §14.
3. COC protocol Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d` is the current companion candidate. Its §14.1–14.5 provides the corresponding COC-side identity and recovery contract.
4. The current exact review bundle is therefore `StorageDesignBlob=d5bdc72...` + `COCProtocolBlob=8ac178...`. The v3.1 header's older `86ff3...` companion note is historical provenance; this amendment explicitly binds the later `8ac178...` companion for this bundle.
5. The v2 pair `4ed423...` + `8ac178...` is NOT a coherent normative pair because v2 lacks the referenced §§15.1–15.7. Any change to either member of the current bundle creates a new immutable bundle revision and requires affected-owner exact-blob re-review. No floating “latest” reference is allowed.

This is a version-binding amendment, not a claim that either artifact has been accepted by A/I/D/C/H or frozen.

## 2. Complete PreparedParticipant identity tuple

For the PostgreSQL 18.x profile, the immutable identity is the following tuple. Fields are typed; similarly named values from different namespaces MUST NOT be substituted.

### 2.1 Stable participant and attempt identity

- `PreparedParticipantRef`: globally unique, opaque, never reused cross-service participant identity.
- `PreparedTransactionGID`: client-chosen PostgreSQL prepared-transaction locator; allocated once and preserved byte-for-byte, including case.
- `PrepareAttemptRef` and monotonic `PrepareAttemptGeneration`: one immutable prepare attempt. A later attempt requires a terminal prior attempt and a new COC prepare-intent binding.
- `ParticipantLedgerRef` and `ParticipantLedgerVersion`: exact append-only Storage ledger row/version; every state transition appends a new version.
- `ParticipantTupleDigest`: domain-separated digest over the complete canonical immutable tuple.
- `PublicationOperationId`, `RequestDigest`, and exact `owner_boundary`.

### 2.2 Domain and database identity

- `CausalOrderDomainRef` and exactly one `PolicyDomainRef`.
- `CanonicalAuthorityDBRef`: governed logical canonical authority.
- `DatabaseIncarnationRef`: governed, non-reusable database-incarnation identity; distinct from cluster system identifier, database OID, hostname, endpoint, or database name.
- PostgreSQL evidence fields: `PostgreSQLSystemIdentifier`, `PostgreSQLDatabaseOID`, observed `PostgreSQLNativeXID`, original prepare timeline and LSN.
- COC prepare-intent identity: `COCClusterRef`, `COCRecordRef` / typed term-index position, `COCEntryDigest`, `OperationId`, and canonical request digest.

### 2.3 Signed PreparedParticipantReceipt envelope

The Storage-signed receipt binds the complete tuple above plus:
- state = `PREPARED_PRIVATE` and authoritative observation source (`pg_prepared_xacts` on the writable primary);
- original prepare observation time (audit only), timeline and LSN;
- schema/message type and version, issuer, subject, owner authority, audience, purpose;
- signer/key ID and version, algorithm and canonicalization profile IDs, digest profile, payload digest and signature.

`PreparedParticipantRef`, GID, native XID, DB incarnation, prepare attempt, ledger version and COC position are separate fields. A generic `xid` field is prohibited.

### 2.4 Resolution identity

`StorageResolutionProof` MUST repeat and bind the same participant, GID, native XID, DB incarnation, attempt generation, ledger ref/version, operation/request/tuple digests, owner boundary and COC prepare-intent reference.

- COMMITTED: exact VisibilityPointer and PublicationReceipt identities, transaction identity and digests.
- ROLLED_BACK: authoritative non-publication evidence.
- UNKNOWN / IN_DOUBT: same participant retained; no new GID, XID or attempt substitution; locks/private bytes remain protected.

Absence from `pg_prepared_xacts` alone is never terminal evidence. Resolution requires the durable participant outcome ledger plus authoritative DB readback. Failover/PITR timeline/LSN are appended as RecoveryObservation entries and never overwrite original prepare evidence.

## 3. Lifecycle and ordering

1. Allocate and durably persist the immutable tuple and GID mapping as `ALLOCATED_NOT_PREPARED`.
2. Quorum-commit the COC `JF10_PREPARE_INTENT_REGISTERED` binding that exact tuple/digest.
3. Linearizably read back the same COC intent and verify no earlier applicable I/D cutoff.
4. Only then issue PREPARE using the same GID.
5. Read authoritative primary `pg_prepared_xacts`; bind observed native XID, DB incarnation, original timeline/LSN.
6. Persist signed PreparedParticipantReceipt and its digest to the same durable participant ledger before returning or registering the receipt.
7. After the exact I terminal decision, resolve the same participant/GID/native XID. Append resolution proof; never infer from COC state or absence from prepared_xacts.

Any changed tuple field under the same participant/attempt/GID is immutable CONFLICT. Same tuple/digest is lookup/replay and returns original evidence.

## 4. Storage's owner-local Gate and Admission inventory

Storage does not own I's policy gate or D's Forget gate. Storage's own persistence/visibility gate MUST nevertheless enforce the exact admission boundary:

- The Storage final visibility transaction atomically checks current I terminal proof, current D fence/barrier proof, exact PreparedParticipant tuple, DB incarnation and operation digest before committing VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox.
- If the storage engine cannot make that final predicate and visibility mutation one atomic transaction, the operation remains private and blocked; a prior check followed by a later unconstrained publish is forbidden.
- The durable participant ledger inventories every allocation, PREPARE attempt, prepared XID, resolution attempt, visibility attempt and uncertain ACK, including work not yet registered as a COC participant.
- Recovery enumeration is from the Storage ledger plus authoritative engine state, not only the COC projection. Any ledger/engine/COC mismatch is UNKNOWN and blocks release.

Minimum admission states: `ALLOCATED_NOT_PREPARED`, `COC_INTENT_COMMITTED`, `PREPARE_IN_PROGRESS`, `PREPARED_PRIVATE`, `RESOLUTION_IN_PROGRESS`, `COMMITTED_VISIBLE`, `ROLLED_BACK_NONPUBLISHED`, `UNKNOWN_IN_DOUBT`, `CONFLICT_QUARANTINED`.

## 5. Recovery and Release boundary

Storage may release only its own visibility/read gate, and only after:
1. exact COC prefix/batch/manifest is verified;
2. Storage ledger high-water and engine inventory are reconciled with every pre-cutoff allocation, prepare attempt and prepared participant;
3. every prepared participant is resolved by same-identity authoritative evidence or remains explicitly private and excluded from serving;
4. current I terminal proof and D effective-fence/barrier proof are independently validated at the final visibility linearization point;
5. DB incarnation, timeline/LSN and anti-rollback anchors are current;
6. no unknown participant, ledger gap, stale proof, conflicting digest or unaccounted in-flight operation can become visible.

Storage release does not release I Gate, D Gate, D Forget barrier, C provider side-effect Gate, or COC recovery Gate. COC recovery completion is not Storage visibility permission.

## 6. Required cross-owner exact review

- I: approve the I proof fields and final-gate binding; Storage does not mint I evidence.
- D: approve D fence/barrier proof and publication ordering; Storage does not mint D clearance.
- H: define exact wire names, types, nullability, canonicalization and compatibility.
- A: accept the exact version pair and integration boundary.
- Storage: this document is a proposed Storage amendment, not an independent human Owner signature.

## 7. Status

The canonical pair proposed here is `4ed4234...` + `8ac1781...`. The earlier `86ff3...` companion is superseded for current prepared-participant semantics. Architecture only; no protocol freeze, implementation, production conformance or production activation is claimed.


## 8. Critical exact-version correction — v2 is not the current companion target

A further exact-file check found that the COC protocol Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d` §14 explicitly requires the Storage design's §§15.1–15.7. Storage Design v2 Blob `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` does not contain §§15.1–15.7; it contains only the earlier abbreviated PostgreSQL mapping in §7.5 and ends at §14. Therefore, **the pair `4ed423...` + `8ac178...` is not a coherent normative pair**.

The Storage branch contains the successor artifact:

- Path: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.md`
- Displayed version: **Storage Design v3.1**
- Exact current blob returned by branch readback: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- It contains §§15.1–15.7 and those sections provide the nominal identity types, DatabaseIncarnationRef registry, immutable prepare-attempt/ledger, receipt preconditions and fields, resolution proof, and exact I terminal proof join required by COC protocol §14.

Accordingly, the corrected version lineage is:

`Storage Design v2 (4ed423...)` → `Storage Design v3.1 (d5bdc72...)`

and the proposed current companion bundle is:

`Storage Design v3.1 (d5bdc72...)` + `COC persistence protocol (8ac178...)`.

The v3.1 header still cites `86ff3...` as its companion clarification source. That reference is historical and is superseded for this exact review bundle by the later COC protocol Blob `8ac178...`, whose §14.1–14.5 both preserves and extends the same-participant identity contract and explicitly points to Storage §§15.1–15.7. This amendment is the explicit cross-file binding; the v3.1 source itself remains immutable.

### 8.1 Cross-file identity completeness check

The v3.1 §§15.1–15.7 and COC protocol §14.1–14.5 MUST be interpreted as one typed semantic contract. The combined tuple includes:
- PreparedParticipantRef; PreparedTransactionGID; PostgreSQLNativeXID;
- CanonicalAuthorityDBRef; DatabaseIncarnationRef; PostgreSQLSystemIdentifier; PostgreSQLDatabaseOID;
- PrepareAttemptRef; PrepareAttemptGeneration; ParticipantLedgerRef; ParticipantLedgerVersion;
- PublicationOperationId; RequestDigest; ParticipantTupleDigest; owner boundary;
- CausalOrderDomainRef; PolicyDomainRef;
- COC prepare-intent identity, position and digest;
- original prepare timeline and LSN; authoritative writable-primary PREPARED observation;
- protected envelope identity: message/schema version, issuer, subject, owner authority, audience, purpose, key ID/version, algorithm/canonicalization/digest profile, payload digest and signature;
- StorageResolutionProof with same-tuple binding, exact VisibilityPointer + PublicationReceipt for COMMITTED, authoritative non-publication proof for ROLLED_BACK, and append-only RecoveryObservation[].

The following are not interchangeable: GID/native XID; authority DB ref/incarnation/system identifier/database OID; original prepare timeline/LSN versus recovery observations; I sequencer position versus COC position versus D FenceGeneration; participant identity versus attempt identity versus ledger identity.

### 8.2 Disposition

- `4ed423...`: preserved historical v2 proposal; not the current companion target for `8ac178...`.
- `d5bdc72...`: current Storage Design v3.1 candidate; exact owner review still required.
- `8ac178...`: current COC persistence protocol candidate; exact owner review still required.
- `86ff3...`: superseded companion clarification for the current pair; retain only as immutable history.
- No acceptance is inherited from the v2 artifact. A/I/D/C/H must review the exact v3.1 + 8ac178 bundle where their authority is affected.
