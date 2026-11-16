# Phase 3.6.5 — Restore Control-High-Water Proof and Quarantine Release Contract

- Owner: Storage/Consistency
- Date: 2026-11-17
- Status: **ARCHITECTURE CONTRACT CANDIDATE / EXACT I-D-A OWNER REVIEW REQUIRED**
- Related Gate A: `reviews/storage-consistency/phase-3.6-deployment-selection-and-verification-readiness.md` §26
- Related COC protocol: Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- Related A JF-10 identity mapping: Blob `a71251704851cacd15f67faa985a5bd50057e92a`

## 1. Purpose and hard rule

A restored Canonical Authority database is not safe to serve merely because PostgreSQL PITR completed or local tables are internally consistent. The restored snapshot may predate a COC commit, I revocation/inventory change, D ForgetFence/lineage barrier, or Storage prepared-participant terminal outcome. Restore therefore starts quarantined and remains `RESTORE_FENCED` until the restored data state is reconciled against current, authenticated owner control high-waters.

**No single owner or cursor proves global restore safety.** COC, I, D and Storage proofs remain separate typed authorities. Storage verifies and records them; it does not mint COC ordering, I authorization, D Forget clearance or G Applied.

## 2. Typed control proofs

### 2.1 COCCommittedPrefixProof — COC authority

Must bind `CausalOrderDomainRef`, cluster identity, `CoordinatorEpoch`, `CoordinatorIndex`, `VoterConfigurationEpoch`, contiguous committed-prefix digest, checkpoint/snapshot ref, external monotonic anchor ref, signer/key version, audience and verification time. It proves only that the COC log prefix/checkpoint is authentic and contiguous under the stated voter configuration. A local DB backup cannot substitute for it.

### 2.2 IControlHighWaterProof — I authority

One proof per affected `PolicyDomainRef`; must bind opaque `PermissionEpoch`, I sequencer epoch/position within that same policy domain, revocation/control-ledger high-water ref and digest, current `ProducerDomainInventoryEpoch`, producer/recipient registry digest, signer/key version, audience and verification time. For each active ForgetOperation affecting the restored dataset, it also references the current I TargetInventorySeal ref/digest and policy disposition.

I proofs from different PolicyDomainRefs are never numerically compared or collapsed into one epoch. IControlHighWaterProof proves I's current policy/registry snapshot only; it does not prove D barrier completion or Storage participant resolution.

### 2.3 DForgetControlHighWaterProof — D authority

Must bind D control-ledger checkpoint/high-water, the complete set/digest of active or recently terminal ForgetOperationRefs affecting the restored dataset, and for each relevant operation: `ForgetFenceGeneration`, effective fence position, immutable request cutoff, `ProducerRegistrationHighWater` / `WorkItemBarrier`, lineage inventory snapshot/digest, barrier terminal state and D signer/key version/audience.

A missing operation, incomplete lineage inventory, open barrier, unresolved lease/participant, late derivative or unknown target makes the proof incomplete. DForgetControlHighWaterProof proves D's Forget/lineage state only; it does not prove I permission or Storage visibility.

### 2.4 StorageParticipantLedgerProof — Storage authority

Must bind `CanonicalAuthorityDBRef`, backup/base snapshot ref, target timeline/LSN, participant-ledger high-water and a digest over every PreparedParticipantRef/PreparedTransactionGID/native-XID tuple and terminal state present in the restored snapshot. Each participant must reconcile to its same-GID StorageResolutionProof or remain explicitly PREPARED/UNKNOWN/private with locks retained. PreparedTransactionGID and EngineNativeTransactionXIDRef remain separate.

### 2.5 RestoreReconciliationReceipt — Storage reconciliation result

Storage issues this receipt only after verifying the exact backup/WAL target and all required COC/I/D/Storage proofs. It binds RestoreOperationRef, CanonicalAuthorityDBRef, backup/base snapshot, target timeline/LSN, all proof refs/digests and signer/key version/audience. Its state is `RECONCILED_BUT_FENCED` until owner-specific serving gates independently revalidate current controls.

RestoreReconciliationReceipt is not an I authorization receipt, D clearance, COC commit proof, Forget completion proof or permission to serve content. It is evidence that Storage completed its local reconciliation algorithm at the recorded high-waters.

## 3. Restore protocol

1. **Quarantine first:** restore to an isolated target with no public listener, no authoritative reads/writes, no cache/index rebuild, no Adapter reconnect and no content serving. Old primary is fenced before promotion or restore target becomes authoritative.
2. **Validate data recovery:** verify base backup, timeline history and every required WAL segment through exact target LSN; preserve prepared transactions and locks; missing/corrupt/truncated/incomplete WAL is `RESTORE_FENCED`.
3. **Reconcile COC:** obtain COCCommittedPrefixProof; verify cluster, voter configuration, checkpoint anchor and contiguous committed prefix. Replay all committed records through the current high-water. Any prefix gap, stale epoch, missing external anchor or unresolved recovery batch blocks release.
4. **Reconcile I:** obtain fresh IControlHighWaterProof for every affected PolicyDomainRef and the current ProducerDomainInventoryEpoch/registry digest. Reconcile current revocation/receipt-consumption state and active Forget TargetInventorySeal refs. A stale PermissionEpoch, inventory epoch change, missing seal, signer/key failure or I outage blocks release.
5. **Reconcile D:** obtain fresh DForgetControlHighWaterProof covering every relevant ForgetOperation and the complete target/source/ancestor lineage. Reconcile ForgetFenceGeneration, request cutoff, producer registration high-water, barrier state and late derivatives. Any open barrier, unknown participant, incomplete lineage or missing operation blocks release.
6. **Reconcile Storage participants:** enumerate every PreparedParticipantRef and PreparedTransactionGID in the restored participant ledger. Query the same GID and authoritative outcome ledger; verify native XID, DB identity, original prepare timeline/LSN and terminal proof. Never infer outcome from absence in `pg_prepared_xacts`. Unknown participants remain private and locked; a restore may not hide or drop them.
7. **Reconcile visibility:** verify VisibilityPointer + PublicationReceipt + owner outcome/receipt-consumption evidence are atomic for every published artifact. Pointer-only, receipt-only, stale replica/cache or outbox-only state is non-authoritative.
8. **Stability recheck:** immediately before Storage issues RestoreReconciliationReceipt, re-read COC/I/D high-waters. If any changed during restore, replay/reconcile again. No wall-clock lease or TTL substitutes for this recheck.
9. **Owner-specific release:** Storage may mark its DB `RECONCILED_BUT_FENCED`; A/owner deployment control may permit internal service start only after the receipt verifies. D/F/G/H/C still perform their own current I/D checks before admission, retrieval, delivery, reconnect or provider submit. RestoreReconciliationReceipt alone never releases those boundaries.

## 4. Fail-closed matrix

| Condition | Required result |
|---|---|
| COC checkpoint/prefix missing, stale, gapped or invalid external anchor | RESTORE_FENCED; no authoritative service |
| I proof missing, stale PermissionEpoch, revocation gap, registry epoch changed or seal missing | RESTORE_FENCED; no protected access |
| D proof missing, incomplete lineage, open barrier, unknown participant or late derivative | RESTORE_FENCED; affected target/lineage remains suppressed |
| Storage GID absent from pg_prepared_xacts but outcome ledger unresolved | UNKNOWN/IN_DOUBT; preserve participant barrier and locks |
| Same GID rebound to another operation/request/participant tuple | CONFLICT; quarantine |
| Prepared XID/participant proof disagrees with restored DB/native XID/timeline/LSN | UNKNOWN/IN_DOUBT; quarantine |
| Pointer without receipt or receipt without pointer | Reject visibility; quarantine affected artifact |
| Old primary not fenced or stale replica can serve authoritative reads | RESTORE_FENCED; no promotion |
| Signer/key version revoked, audience mismatch or proof integrity failure | Reject proof; RESTORE_FENCED |
| Any COC/I/D high-water advances during restore | Repeat replay/reconciliation; do not issue release receipt |

## 5. Type and ordering invariants

- `CoordinatorIndex`, I sequencer position/PermissionEpoch/ProducerDomainInventoryEpoch, D ForgetFenceGeneration/ProducerRegistrationHighWater, Storage GID/native XID/LSN, and F IndexWatermark/G ContextVersion/H CapabilityEpoch remain distinct typed namespaces.
- No numeric comparison across authorities, no local timestamp ordering, no synthesized missing high-water, and no proof derived from absence of a row or message.
- IControlHighWaterProof is per PolicyDomainRef; cross-domain aggregation is a set of independent proofs, not a max epoch.
- DForgetControlHighWaterProof is per relevant ForgetOperation/lineage; one operation's barrier does not cover another operation's targets.
- Restore is not Global Forget completion. A successful restore reconciliation only proves the restored snapshot has been brought forward to the verified current controls.

## 6. Architecture acceptance and engineering boundary

Architecture phase requires exact I/D/A/Storage acceptance of the proof shapes, ownership, fail-closed behavior and recheck order. H may define the authenticated envelope/encoding only after these semantic contracts are accepted. Implementation of proof APIs, signature verification, external checkpoint custody, WAL/archive restore automation, old-primary fencing, restore runbooks, measured RPO/RTO and production HA remains deferred to engineering/deployment.

Initial service profile: RPO 0 for quorum-acknowledged COC entries under the specified three-voter/one-unavailable crash-fault model and for acknowledged synchronous DB commits under the pinned `remote_apply` profile, subject to the respective durability boundaries. Correlated loss of a majority/primary+sync standby is outside the guarantee. Numeric RTO remains TBD pending measured restore and owner-control reconciliation. No availability SLA is claimed.

**Status:** CANDIDATE / EXACT I-D-A-STORAGE REVIEW REQUIRED. Until accepted and implemented, Storage restore remains quarantined whenever current owner control high-waters cannot be proven.