# B Owner — Exact Restore Control-High-Water Proof Type Review

- Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- IControlHighWaterProof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- DForgetControlHighWaterProof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- Updated B typed-reference registry commit: `848a74593e20bef8842a2c492e3bd592ec5fd714`
- Decision: **ACCEPT WITH B TYPE / AUTHORITY SEPARATION CONDITIONS**

B accepts the five proof/reference types and their issuer boundaries: COCCommittedPrefixProofRef, IControlHighWaterProofRef, DForgetControlHighWaterProofRef, StorageParticipantLedgerProofRef and RestoreReconciliationReceiptRef.

B confirms that CoordinatorIndex, I sequencer position, PermissionEpoch, ProducerDomainInventoryEpoch, D ForgetFenceGeneration, ProducerRegistrationHighWater, Storage GID/native XID/LSN and F IndexWatermark are non-interchangeable. I proof is per PolicyDomainRef; D proof is per ForgetOperation/lineage.

B explicitly rejects treating Storage RestoreReconciliationReceipt as authorization, D clearance, I decision, Global Forget completion or permission to serve. All proof refs are opaque typed selectors whose content/signature must be verified by the issuing owner.

Non-waived: Fact/Claim ADR-001 remains ADR-BLOCKED; I36 governance remains GOVERNANCE-BLOCKED; no production restore, inventory seal or physical-erasure claim.