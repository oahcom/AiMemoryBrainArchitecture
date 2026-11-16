# E Owner — Exact Restore Reconciliation / Compiler Publication Consumer Acceptance

- Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A restore integration acceptance Blob: `fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- Decision: **ACCEPT WITH E PRODUCER / PUBLICATION RESTORE GATES**

E accepts that restored staged artifacts, queues, outboxes and manifests remain private until the COC committed prefix, current I policy/revocation/registry proofs, D Forget/lineage proofs and Storage participant/visibility ledger are reconciled. RestoreReconciliationReceipt is not a PublicationReceipt, VisibilityPointer commit, owner-final-gate or Full Applied proof.

E must preserve the same PublicationOperationId/RequestDigest/PreparedParticipantRef/PreparedTransactionGID across restore and retries. AttemptId/LeaseEpoch may change, but the immutable tuple cannot. If Storage pointer and PublicationReceipt transaction identities disagree, or D/I/COC high-waters are stale, E cannot publish or expose artifacts. Any late derivative or post-fence producer remains blocked.

Limit: no production E queue/outbox/manifest restore or publication-gate integration is implemented/verified.