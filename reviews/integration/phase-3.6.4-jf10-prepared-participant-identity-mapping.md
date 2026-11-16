# A Integration Addendum — JF-10 PreparedParticipantRef / PreparedTransactionGID / Native XID Identity Mapping

- Owner: A — Principal Integration Architect
- Exact Storage protocol revision: Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`, §14
- Base A COC/JF-10 architecture: Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, §12
- H schema candidate: `bmcp.applied-ack/1.1.1`, file `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json`
- Status: **A INTEGRATION MAPPING PROPOSED / OWNER EXACT-VERSION REVIEW REQUIRED**
- Date: 2026-11-17

## 1. Three distinct identifiers — no aliasing

| Type | Authority / lifecycle | Meaning | Forbidden substitution |
|---|---|---|---|
| `PreparedParticipantRef` | Storage-owned, stable, engine-neutral | Cross-service identity for one prepared participant and its immutable operation tuple. | Not a PostgreSQL GID or native XID. |
| `PreparedTransactionGID` | Storage-owned, client-chosen, PostgreSQL-specific handle | Stable GID passed to PREPARE TRANSACTION and reused for every lookup/retry/COMMIT PREPARED/ROLLBACK PREPARED. | Not the numeric `pg_prepared_xacts.transaction` value. |
| `EngineNativeTransactionXIDRef` | Engine-assigned observation, returned after PREPARE | Native transaction XID/handle as observed from the selected DB engine. | Not preallocatable; never the sole participant identity. |

`PreparedParticipantRef` and `PreparedTransactionGID` are bound to one `PublicationOperationId`, `RequestDigest`, participant digest, exact owner boundary, `CausalOrderDomainRef`, one `PolicyDomainRef` and `CanonicalAuthorityDBRef`. `EngineNativeTransactionXIDRef` is observed evidence attached after PREPARE. These are distinct types even if their serialized strings happen to look similar.

## 2. Required allocation and execution order

1. Before any COC prepare-intent append, Storage's authenticated preallocation operation returns or durably adopts one `PreparedParticipantRef` and one unique `PreparedTransactionGID`, and persists the immutable operation/request/participant/database tuple in Storage's participant ledger as `ALLOCATED_NOT_PREPARED`.
2. The caller MUST NOT choose a new participant/GID after an uncertain response. It queries the same `PublicationOperationId` + `RequestDigest` and receives the original pair. Same identity/digest is idempotent; same identity with changed tuple or same GID rebound to another tuple is CONFLICT.
3. COC then quorum-commits `JF10_PREPARE_INTENT_REGISTERED` with `PreparedParticipantRef`, `PreparedTransactionGID`, operation/request/participant digests, owner boundary, `CanonicalAuthorityDBRef`, `CausalOrderDomainRef`, `PolicyDomainRef` and COC prepare-intent position/digest.
4. Storage may issue PostgreSQL PREPARE only after authoritative readback proves that exact COC prepare-intent record committed. PREPARE uses the same `PreparedTransactionGID`; it does not use or predict the native XID.
5. After PREPARE, Storage reads the engine-assigned native XID and original prepare timeline/LSN, then returns a Storage-signed `PreparedParticipantReceipt` binding both stable identifiers, native XID, cluster `system_identifier`, database OID, participant digest, operation/request tuple, COC intent position/digest, prepared state, signer/key version and audience.
6. COC records `JF10_PREPARED_PARTICIPANT_REGISTERED` using the same pair and receipt digest before I may decide the owner-final gate.
7. I's terminal receipt/decision binds the same `PreparedParticipantRef` + `PreparedTransactionGID` and complete immutable tuple. I does not authorize by native XID alone.
8. Storage resolves the exact same GID after I's durable COMMIT/ABORT. `StorageResolutionProof` binds the same participant ref, GID, observed native XID, DB identity, original prepare timeline/LSN, operation/request/participant digest and final state. Commit includes exact VisibilityPointer/PublicationReceipt transaction identity and digest; rollback includes authoritative non-publication proof.

## 3. COC record and API mapping

- `JF10_PREPARE_INTENT_REGISTERED`: canonical fields `prepared_participant_ref` and `prepared_transaction_gid`; native XID is absent because PREPARE has not yet run.
- `JF10_PREPARED_PARTICIPANT_REGISTERED`: same canonical pair plus `engine_native_transaction_xid_ref`, PostgreSQL cluster/database identity, original prepare timeline/LSN, Storage signer/key version and receipt proof.
- `I_JF10_TERMINAL_DECISION_OBSERVED`: same canonical pair plus I terminal receipt/consumption proof and I sequencer position; COC does not infer I terminality.
- `STORAGE_JF10_PARTICIPANT_RESOLVED`: same canonical pair + same native XID observation + Storage resolution proof + pointer/receipt or non-publication evidence.
- `JF10_BRIDGE_RECONCILIATION_RECORDED`: same canonical pair and owner lookup states; if Storage state is PREPARED/COMMITTED/ROLLED_BACK, include native XID and original prepare metadata.

Canonical H 1.1.1 fields are `prepared_participant_ref`, `prepared_transaction_gid`, `engine_native_transaction_xid_ref`, `postgres_system_identifier`, `target_database_oid`, `prepare_timeline`, `prepare_lsn` and `storage_signer_key_version`. Legacy 1.1.0 fields (`storage_participant_ref`, `storage_xid_ref`, `preallocated_storage_xid_ref`, `storage_prepare_transaction_ref`) are deprecated aliases only and, if present, MUST byte-match their 1.1.1 canonical counterpart. Consumers MUST NOT infer types from field spelling or compare values across namespaces.

## 4. Crash, retry and cutoff rules

- Crash after preallocation but before COC intent: remain `ALLOCATED_NOT_PREPARED`; no PREPARE is allowed. A D/I cutoff that wins before the COC intent rejects the operation. Cancellation is allowed only after the Storage ledger and authoritative engine lookup prove PREPARE never occurred; absence from `pg_prepared_xacts` alone is insufficient.
- COC append ACK lost: lookup same operation/request digest; never allocate a second participant/GID.
- COC intent committed, Storage PREPARE ACK lost: query the same GID and Storage ledger; append the prepared receipt only after authoritative same-GID state is established.
- Storage PREPARE succeeded, COC receipt append unavailable: preserve private bytes and locks; no I terminal decision or D barrier completion. Recover the same GID and append the original receipt observation.
- I COMMIT_WON: forward-commit same GID. I ABORT/REVOCATION_WON: rollback same GID. UNKNOWN remains IN_DOUBT; no heuristic action, new GID or TTL.
- D cutoff before COC prepare-intent: reject prepare. Prepare-intent before D cutoff: D includes the `PreparedParticipantRef` in the target/source/ancestor barrier, even before Storage PREPARE receipt.
- `PreparedTransactionGID` is unique within the bound PostgreSQL cluster/database and is never reused after resolution. A same-GID/different-tuple request is CONFLICT.

## 5. Exact owner review boundary

This addendum is A's proposed integration mapping for Storage protocol §14. It does not claim that H has approved the 1.1.1 schema, I has accepted the exact GID binding, D has accepted the exact barrier key, C/E/G/B have accepted the updated typed tuple, or Storage has approved A's allocation ordering. Each affected Owner must review the exact Blob SHA of this addendum and the exact Storage protocol Blob `86ff3b...` before the revised bridge can be called design-accepted.

Production implementation, generated SDK, signatures, DB adapter, COC quorum and cross-owner fault injection remain deferred to engineering. JF-10 P0 remains OPEN; no production activation is implied.