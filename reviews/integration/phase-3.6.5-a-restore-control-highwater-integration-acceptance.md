# A Owner — Exact Restore Control-High-Water and Quarantine Integration Acceptance

- Exact Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- Exact I restore proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- Exact D restore proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- Related COC protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- Decision: **ACCEPT AS SYSTEM RESTORE ARCHITECTURE WITH OWNER-LOCAL RELEASE GATES**
- Mode: delegated A integration review under user instruction; not independent human sign-off.

A accepts the four-proof reconciliation architecture:

1. COCCommittedPrefixProof establishes only the durable COC prefix/checkpoint and voter configuration.
2. IControlHighWaterProof is per PolicyDomainRef and establishes only current I sequencer/revocation/registry state.
3. DForgetControlHighWaterProof is per relevant ForgetOperation/lineage and establishes only D fence, producer barrier and lineage state.
4. StorageParticipantLedgerProof establishes only the restored Storage participant/GID/native-XID and visibility/receipt outcome state.
5. Storage's RestoreReconciliationReceipt records that the restored local DB was reconciled against those proofs; it is `RECONCILED_BUT_FENCED`, not a grant to serve, publish, disclose, complete Forget or claim physical erasure.
6. Before the receipt is issued, Storage re-reads COC/I/D high-waters; any advance repeats reconciliation. Every owner service continues to check its own current authority at its protected boundary.
7. Missing/invalid/stale proof, WAL gap, unknown GID, open D barrier, I registry/revocation gap, COC prefix gap or signer/audience failure keeps restore quarantined.

### A integration conditions

- A will not treat RestoreReconciliationReceipt as a cross-owner authorization or use one authority's high-water as a substitute for another.
- The restored data plane remains fenced until Storage's internal state is reconciled and A's deployment gate has verified the exact receipt; F/G/H/C still require their own I/D current-use checks.
- No partial release is permitted unless target/partition isolation is explicitly proven; otherwise one unresolved relevant target blocks the restored authoritative service.
- Numeric RTO remains TBD; RPO 0 is bounded to the specified synchronous durability fault models, not correlated total-cluster/site loss.

Exceptions: no production proof API, signature/key verification, restore orchestration or cross-owner release gate is implemented. The contract is accepted at architecture level only. Gate C implementation/fault injection remains deferred to engineering.