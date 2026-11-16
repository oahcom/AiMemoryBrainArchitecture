# D Owner — Exact JF-10 Prepared Participant Identity / GID Fence-Boundary Acceptance

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH D-OWNED FENCE / PARTICIPANT-ADMISSION CONDITIONS**
- Mode: delegated D-boundary review under user instruction; not independent human sign-off.

D accepts the new identifier separation and admission ordering:

1. `PreparedParticipantRef` is the stable barrier participant identity. `PreparedTransactionGID` is the exact Storage-preallocated PostgreSQL handle bound to the immutable operation tuple. `EngineNativeTransactionXIDRef` is observed engine evidence only and is not a D barrier key.
2. COC `JF10_PREPARE_INTENT_REGISTERED` is the participant-admission linearization point. D must include the exact PreparedParticipantRef/GID tuple in the relevant target/source/ancestor barrier once that COC intent is committed, even if Storage PREPARE receipt is not yet visible.
3. Storage must not execute PREPARE before authoritative readback of the exact COC intent. A D cutoff that wins before that intent causes COC admission rejection and no PREPARE.
4. A Storage preallocation that exists before COC intent is `ALLOCATED_NOT_PREPARED`, not a prepared side effect. If a D cutoff wins in this window, D may not infer cancellation from missing COC intent alone; Storage must provide durable same-GID proof that PREPARE never occurred and the reservation is terminally cancelled before D completes.
5. Same PreparedParticipantRef/GID and immutable tuple survive retry/recovery. Rebinding either to another operation, digest, owner boundary, Scope/Environment or CanonicalAuthorityDBRef is CONFLICT.
6. Native XID, PostgreSQL system_identifier, database OID, timeline and LSN are supporting Storage evidence. They do not replace D's fence generation, request cutoff, lineage high-water or canonical suppression proof.
7. Missing/contradictory GID reservation, COC intent, Storage receipt or terminal proof leaves the D barrier UNKNOWN/IN_DOUBT. No timeout, worker death, missing pg_prepared_xacts row or cache eviction releases it.

Exceptions: D durable ledger/API, participant admission, preallocation cancellation proof and real barrier races remain NOT IMPLEMENTED / NOT RUN. This is D semantic acceptance only; JF-10 runtime P0 and Global Forget completion remain OPEN.