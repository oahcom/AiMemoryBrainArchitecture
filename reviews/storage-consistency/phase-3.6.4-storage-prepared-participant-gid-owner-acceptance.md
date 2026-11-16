# Storage Owner — Exact JF-10 PreparedParticipantRef / PreparedTransactionGID Acceptance

- Exact Storage COC protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- H schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- PostgreSQL 18.7 probe Blob: `6350e6c2a0e6b28d1ad23e0a1a6cb1d4b6c0b3a4`
- Decision: **ACCEPT WITH STORAGE-OWNED PARTICIPANT / GID INVARIANTS — ARCHITECTURE ONLY**
- Mode: Storage Owner technical acceptance; not independent validation or production approval.

Storage accepts the exact identity split:

1. PreparedParticipantRef is the stable engine-neutral cross-service participant identity.
2. PreparedTransactionGID is the client-chosen PostgreSQL GID; Storage allocates and durably binds it to the immutable PublicationOperationId/RequestDigest/participant tuple and CanonicalAuthorityDBRef before COC prepare-intent registration.
3. EngineNativeTransactionXIDRef is the PostgreSQL-native XID observed after PREPARE; it is never preallocated and never replaces the GID or participant ref.
4. PostgreSQL system_identifier, target database OID, original prepare timeline/LSN and Storage signer/key version/audience are bound into PreparedParticipantReceipt and StorageResolutionProof.
5. GID uniqueness is enforced within the bound cluster/database. Same GID/same tuple is lookup/replay; same GID/different tuple is CONFLICT. GID is never reassigned after terminal resolution.
6. Storage PREPARE is prohibited until authoritative readback proves the exact COC prepare-intent record committed. Preallocation without COC intent remains ALLOCATED_NOT_PREPARED and has no prepared side effect.
7. A D/I cutoff that wins before COC intent prevents PREPARE. Any cancellation of an allocated reservation requires durable Storage ledger proof and authoritative engine lookup proving PREPARE never occurred; absence from pg_prepared_xacts alone is insufficient.
8. After I terminal decision, Storage resolves the same GID. COMMITTED proof binds exact VisibilityPointer/PublicationReceipt transaction and digest; ROLLED_BACK proof binds authoritative non-publication evidence. Any missing/disagreeing ledger/readback remains UNKNOWN/IN_DOUBT.

### Evidence and limits

The PostgreSQL 18.7 capability probe already exercises client-chosen GIDs across PREPARE, restart/PITR, same-GID COMMIT/ROLLBACK and missing/corrupt/incomplete WAL cases. The latest seven-workflow regression set is 7/7 SUCCESS. These tests do not yet implement the COC prepare-intent gate, signed PreparedParticipantReceipt, I terminal decision, real D barrier or production Storage ledger.

Storage accepts the H 1.1.1 candidate wire mapping for exact owner review; alias equality and cross-message identity consistency must be enforced by semantic validation and Storage's durable ledger, not JSON Schema alone.

**Disposition:** Storage §14 and the A integration mapping are accepted at architecture level. No production PostgreSQL deployment, COC service, Storage adapter, named human operator, KMS, end-to-end integration or Gate C fault injection is claimed. JF-10 runtime P0 remains OPEN; production activation NOT AUTHORIZED.
## 1.1 Storage issuance of PreparedParticipantRef

Storage clarifies and accepts the A mapping's allocation boundary: the authenticated Storage preallocation operation returns a Storage-issued PreparedParticipantRef and PreparedTransactionGID, or durably adopts a caller-supplied candidate PreparedParticipantRef only after collision/tuple/authority verification. The canonical ref is immutable once persisted; callers cannot mint an authoritative ref by assertion. The ledger records the pair in ALLOCATED_NOT_PREPARED before the COC prepare-intent commit.