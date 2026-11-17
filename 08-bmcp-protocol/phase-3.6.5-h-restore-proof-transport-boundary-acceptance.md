# H Owner — Exact Restore Control-High-Water Proof Transport Boundary Acceptance

- Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- B typed-reference registry Blob: `63ccb4bf687b00dea2b21fc2773f3018648d76e6`
- A integration acceptance Blob: `a80d90810425e94d752daa48c1b25dd78357e5aa`
- Decision: **ACCEPT SEMANTIC TRANSPORT BOUNDARY; WIRE SCHEMA DEFERRED**

H accepts the transport/authority boundary for restore control proofs:

1. COCCommittedPrefixProof, IControlHighWaterProof, DForgetControlHighWaterProof and StorageParticipantLedgerProof are separate issuer-owned proof families. H transports them without minting, changing, flattening or upgrading their authority.
2. Each proof envelope must bind sender/issuer identity, signer key version, audience, integrity proof, channel binding and immutable proof digest. Stale/revoked key, wrong audience, missing integrity/channel binding or malformed issuer reference is rejected.
3. Opaque proof refs and their underlying owner positions remain typed. H MUST NOT compare COC CoordinatorIndex with I sequencer position/PermissionEpoch, D ForgetFenceGeneration/ProducerRegistrationHighWater or Storage GID/native XID/LSN.
4. IControlHighWaterProof remains per PolicyDomainRef; DForgetControlHighWaterProof remains per ForgetOperation/lineage. H does not aggregate their numeric positions.
5. Storage RestoreReconciliationReceipt is a Storage result only; H does not treat it as permission to serve, D clearance, I authorization or Global Forget completion.
6. Any missing, stale, gapped, unauthenticated or contradictory proof is delivered as UNKNOWN/IN_DOUBT or rejected; no fallback to cached proof or wall-clock freshness.

### Wire-schema boundary

H does not freeze a new BMCP restore-proof schema in this decision. Exact message names, required fields, canonical encoding, signature suite, replay handling and version negotiation require a separate exact-version schema proposal after the semantic owners approve the contract. The current 1.1.1 JF-10 prepared-GID schema does not itself encode all restore high-water proof families.

Exceptions: no live H transport, signature/channel binding, issuer trust, replay or restore integration is implemented/verified. This is semantic transport acceptance only.