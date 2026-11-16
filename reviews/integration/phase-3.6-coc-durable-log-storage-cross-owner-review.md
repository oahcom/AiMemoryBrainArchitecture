# A Owner Review — COC Durable Log, Recovery Cutoff & JF-10 Bridge

- Reviewer: A — Principal Integration Architect
- Review target: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design.md`
- Exact target: commit 9a975f665ee60f4551effe0104ea8f867716d9dd; blob cd5566b3d99b5204401ac713a5bb2dcf89a02726
- Review scope: architecture and cross-owner contract only; no implementation or deployment acceptance.
- Decision: **NEEDS_REVISION**

## 1. Accepted architectural direction

A accepts the core separation that COC is a quorum-committed cross-owner causal-order/evidence log and participant-accounting service, not an authority that decides I authorization, D ForgetFence effectiveness, C provider success, Storage visibility, or G Applied. Typed COC/I/D/Storage positions must remain separate. UNKNOWN/IN_DOUBT must remain durable and blocking; no TTL, heuristic outcome, or operator force-clear is acceptable.

The recovery state sequence `RECOVERY_FENCED → PREFIX_VERIFIED → CUTOFF_BATCH_COMMITTED → PARTICIPANTS_RECONCILING → SERVING` is directionally correct. A new leader must start fenced, and the recovery-complete record must be quorum committed before protected admission reopens.

## 2. Blocking findings

### A-COC-01 — Recovery Cutoff Batch construction order is internally inconsistent (BLOCKING)

§3.2 says `RECOVERY_CUTOFF_BATCH_COMMITTED` contains participant enumeration high-water. §5.3 step 4 commits the batch, but step 6 only then enumerates pre-P participants and persists count/set digest/manifest. An immutable batch cannot bind a complete participant set or its high-water if enumeration has not yet been performed.

Required amendment: define a pre-commit read-only enumeration against the verified prefix P and owner high-water snapshots, compute a deterministic manifest/set digest, then atomically append a batch that binds those exact values; OR split into immutable `RECOVERY_CUTOFF_BATCH_COMMITTED` and `RECOVERY_PARTICIPANT_MANIFEST_COMMITTED` records, with serving gated on both and the latter cryptographically bound to the former. Specify how the manifest is complete, retrievable and prefix-bound. No protected intent may enter between P and batch commit.

### A-COC-02 — JF-10 owner-final-gate semantics are under-specified and risk detached COMMIT (BLOCKING)

§7 states that I supplies a terminal COMMIT/ABORT and Storage resolves the same XID. It does not fully state that I's sequenced operation is the exact Storage owner-final visibility gate participant, bound to owner_boundary, XID, digest, DB identity and single-use receipt in one I coordinator transaction. The existing I disposition rejects the earlier detached sequence and requires the actual owner-final-gate operation to participate in I policy-domain ordering.

Required amendment: normatively bind the I sequencer decision to the exact prepared Storage owner-final-gate participant; distinguish I decision durability from Storage visibility commit; Storage PublicationReceipt remains the only visibility proof. Pin the exact I disposition and do not imply that a generic I terminal token authorizes a later unrelated Storage commit.

### A-COC-03 — Owner-local gate inventory omits C's side-effect admission contract (BLOCKING)

§5.2 specifies I and D local pending gates, while §5.1 says C/I/D gates close. The protocol must explicitly state C's behavior: no new protected intent/reservation/provider call when COC quorum/prefix/cutoff status is unavailable; every already admitted C participant and ambiguous provider outcome must be included in recovery enumeration and reconciled by C's authoritative provider evidence. COC cannot infer provider success.

### A-COC-04 — Participant state names can be mistaken for COC-owned decisions (BLOCKING)

The state machine includes `COMMIT_WON` and `ABORT_WON` without naming them as observations of I's signed decision. Replace with explicit observed states or require every transition to carry I decision ref/digest and state that COC only records it. Similarly `STORAGE_RESOLVED` must require Storage's authoritative same-XID proof.

## 3. Non-blocking clarifications

1. Specify a deterministic serialization/canonicalization profile for owner request sets and participant manifests, including empty-set representation and duplicate/conflict behavior.
2. State whether the batch's owner completeness attestations are captured before append and how a request racing the high-water snapshot is guaranteed to remain gated and be included in a subsequent batch.
3. Define the exact linearizable API response for a caller whose append ACK is lost; same-key read must be scoped to the verified term/index/digest prefix.
4. Define the COC record retention/archive proof and external rollback anchor before compaction/restore; current proposal leaves retention/RPO/RTO open, which is acceptable for design proposal but blocks freeze.
5. Separate `RECOVERY_EPOCH_COMPLETED` (COC service readiness) from owner-local gate release and from any I/D terminal/effective state.

## 4. Recovery Cutoff Batch assessment

- Exact pre-recovery prefix P: **specified**.
- Complete I/D inventories at owner high-water without cross-owner ordering: **specified, but race/high-water capture needs stronger atomicity**.
- Deterministic pre-P participant enumeration: **specified, but batch construction order is inconsistent**.
- Batch before post-recovery protected intent: **specified**.
- Crash before recovery-complete leaves next leader fenced: **specified**.
- Delayed post-snapshot owner requests remain gated and enter a later batch: **specified, needs explicit gate-release test**.
- Missing participant/owner proof/digest mismatch prevents serving: **specified**.

## 5. Owner-local Gate assessment

I and D own their respective gates; COC cannot release them. I release must not mint authorization; D release must not make Forget effective or release a producer barrier. Owner-local order is authoritative and timestamps are audit-only. Require explicit C fail-closed admission/side-effect behavior and test restart/failover/stale snapshot/duplicate request.

## 6. JF-10 same-XID bridge assessment

Stable operation/XID/DB/digest binding before PREPARE, Storage-signed PreparedParticipantReceipt, same-XID recovery, and Storage-only PublicationReceipt/non-publication proof are correct. The proposal must additionally pin the I owner-final-gate participant semantics and ensure COC's observed I/Storage states cannot be mistaken for authority decisions. COC outage must not create a second XID or block Storage from following an already durable I decision, but no I decision may be admitted without the required exact COC prefix and prepared registration.

## 7. Required cross-owner decisions

- I: exact owner-final-gate participation and cryptographic/quorum/restore security acceptance.
- D: D-local cutoff completeness, lineage barrier membership and effective-fence preconditions.
- C: provider boundary, local fail-closed behavior, provider same-key recovery and side-effect inventory.
- H: exact wire mapping for recovery batch and typed evidence, schema/version/canonicalization.
- Storage: revise batch ordering and same-XID participant semantics; A does not edit Storage-owned proposal.

**Conclusion:** do not freeze or advance this exact proposal as the joint COC persistence contract. Storage should publish a new exact version addressing A-COC-01..04, then request a new exact-blob review. No implementation, test, production readiness or activation is approved by this review.
