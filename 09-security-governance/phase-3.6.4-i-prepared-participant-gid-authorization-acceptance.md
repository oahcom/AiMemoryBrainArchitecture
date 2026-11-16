# I Owner — Exact JF-10 Prepared Participant Identity / GID Authorization-Boundary Acceptance

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH I-OWNED AUTHORIZATION / RECEIPT-CONSUMPTION CONDITIONS**
- Mode: delegated I technical-boundary review under user instruction; not external governance approval or independent human signature.

I accepts the exact prepared participant identity mapping at the I authorization boundary:

1. I terminal decision and receipt consumption bind the exact `PreparedParticipantRef` + `PreparedTransactionGID` and immutable PublicationOperationId/RequestDigest/participant/owner/domain tuple.
2. `EngineNativeTransactionXIDRef`, PostgreSQL system_identifier, database OID, timeline and LSN are Storage evidence only. They do not identify the authorization subject, prove I's decision or replace I sequencer position/PermissionEpoch.
3. I alone issues and consumes CommitAuthorizationReceipt and decides COMMIT_WON / ABORT_WON / REVOCATION_WON / UNKNOWN. COC intent commit, Storage preallocation, PreparedParticipantReceipt and native XID are not I terminality.
4. Storage preallocation before COC prepare-intent is `ALLOCATED_NOT_PREPARED`; it does not authorize PREPARE or publication. I revocation/cutoff that wins before COC intent prevents the prepare-intent admission; if intent committed first, the exact pair is included in I's and D's participant reconciliation.
5. I receipt consumption must be idempotently bound to the same participant ref/GID and request digest. Same tuple replay is idempotent; changed GID, participant, authority, digest, PolicyDomainRef or CausalOrderDomainRef is CONFLICT.
6. A missing/ambiguous Storage outcome, absent GID without authoritative outcome ledger/readback, mismatched native XID, stale key/receipt or unavailable I sequencer remains UNKNOWN/IN_DOUBT; no inferred COMMIT/ABORT.
7. I sequencer positions and PermissionEpoch remain incomparable with COC CoordinatorIndex, D ForgetFenceGeneration, Storage native XID/GID, G ContextVersion and H ACK sequence.

Exceptions: I sequencer/receipt-consumption implementation and real Storage/COC integration remain NOT VERIFIED. I36-GOV-01..10 remain GOVERNANCE-BLOCKED / NOT APPROVED; this technical acceptance does not approve issuer federation, delegation, cross-Scope/Environment grants, offline authorization leases, Global Forget exceptions or physical erasure.