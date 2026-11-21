# G Owner — Exact JF-10 Prepared Participant Identity / GID Applied-Evidence Acceptance

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Decision: **ACCEPT WITH G-OWNED FULL APPLIED / CURRENT-USE CONDITIONS**
- Mode: delegated G-boundary review under user instruction; not independent human sign-off.

G accepts the exact participant identity tuple as Storage evidence consumed by the Full Applied proof:

1. Full Applied binds `PreparedParticipantRef` + `PreparedTransactionGID` + `EngineNativeTransactionXIDRef` + CanonicalAuthorityDBRef + PostgreSQL system/database identity + original prepare timeline/LSN + participant digest + PublicationOperationId/RequestDigest + owner boundary + COC intent position/digest + Storage signer/key version/audience.
2. PreparedParticipantRef/GID are stable identity/handle; native XID is observed evidence only. None alone proves publication or Applied.
3. Full Applied still requires CSubmitOutcome, valid H envelope/ACK, I terminal authorization/receipt consumption, D complete-lineage barrier/clearance, Storage same-GID terminal resolution and the atomic VisibilityPointer/PublicationReceipt proof, all bound to the same immutable tuple.
4. COMMITTED Storage proof must identify the exact VisibilityPointer and PublicationReceipt transaction/digest. ROLLED_BACK proof must establish non-publication. Prepared-but-unresolved, GID absent without durable outcome, missing WAL, conflicting native XID or stale database identity remains UNKNOWN/IN_DOUBT.
5. COC commit position and the PreparedTransactionGID/native XID are not interchangeable with I sequencer position, D fence generation, G ContextVersion or delivery cursor.
6. Historical Applied is immutable only if the original complete proof was valid. Current-use remains separately gated by current Context head, I PermissionEpoch, D ForgetFence, Scope/Environment, session and capability.

Exceptions: G Applied validator/persistence and integrated COC/Storage proof lookup are not implemented/verified; G-CO race suites remain NOT RUN. This is design acceptance only and does not claim Global Forget completion.