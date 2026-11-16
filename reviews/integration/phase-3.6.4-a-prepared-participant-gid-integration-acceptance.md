# A Owner — Exact JF-10 PreparedParticipantRef / PreparedTransactionGID Integration Acceptance

- Storage COC protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A identity mapping addendum Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH ENUMERATED OWNER / ENGINEERING CONDITIONS**
- Mode: delegated A integration review under user instruction; not independent human sign-off.

A accepts the §14 identity mapping and the companion integration order as the current JF-10 architecture candidate:

1. Storage-owned PreparedParticipantRef is the stable engine-neutral participant identity; Storage-owned PreparedTransactionGID is the client-chosen PostgreSQL prepared handle; EngineNativeTransactionXIDRef is observed after PREPARE and never substitutes for either.
2. Storage preallocation of the pair and immutable operation tuple precedes COC prepare-intent registration. COC must quorum-commit the exact pair before Storage PREPARE is allowed.
3. COC records the same pair at prepare-intent, prepared receipt, I terminal decision observation, Storage resolution and reconciliation. Any mismatch is CONFLICT/UNKNOWN.
4. I terminal decision binds the stable pair and tuple; D barrier keys the same PreparedParticipantRef; C provider idempotency key remains a separate namespace; E publication identity and G Full Applied proof bind the same pair.
5. H schema 1.1.1 is the candidate wire mapping. Legacy 1.1.0 aliases are deprecated and must byte-match canonical fields if present.
6. Native XID/system identifier/database OID/timeline/LSN are Storage evidence. They do not grant authority or replace the stable participant/GID.
7. If D/I cutoff wins before COC intent, no PREPARE is allowed; a preallocated-but-not-prepared reservation requires Storage's durable cancellation proof. If intent wins first, the exact participant is included in D/I recovery and barrier reconciliation.

### Non-waived conditions

- Storage must own and durably enforce GID uniqueness, immutable tuple binding, preallocation state, same-GID retry/terminal resolution and ledger/readback reconciliation.
- H schema 1.1.1 remains candidate; semantic verifier must enforce alias equality and same-GID/same-participant consistency across messages.
- B/I/D/C/E/G/H exact owner acceptance records must all reference the same protocol and A mapping blobs.
- No production COC quorum, DB adapter, I/D service integration, cryptographic transport, generated SDK or Gate C fault injection is claimed.
- I36 governance approvals, Fact/Claim ADR-001, multi-PolicyDomain atomicity, Global Forget target inventory and physical erasure remain open.

**Disposition:** A accepts this exact architecture mapping for continued design/integration. Gate B's amended specification is not overall accepted until every affected Owner's exact review is recorded. JF-10 runtime P0 remains OPEN; TAB-001 remains candidate/not frozen; production activation is not authorized.