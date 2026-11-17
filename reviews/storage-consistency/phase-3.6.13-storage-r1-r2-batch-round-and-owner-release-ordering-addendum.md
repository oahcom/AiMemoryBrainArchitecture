# Phase 3.6.13 — Storage R1/R2 Batch-Round and Owner-Release Ordering Addendum
# Phase 3.6.13 — Storage R1/R2 Batch 轮次与 Owner Release 顺序补充

- Owner perspective: Storage / COC Durable Log and Recovery
- Status: **PROPOSED ADDENDUM / FRESH OWNER REVIEW REQUIRED**
- Normative base: Storage v3.1, Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- A blocking review: Blob `fdf63550696948f77dc37c0a3788276ac4d525f5`, Issue #14 R1/R2
- I candidate: Blob `57ef6c4352d79577ae53a77895f73bce434c5fca`
- D candidate: Blob `a7cba2c72720bb7873d77f1a9d151df974605a9e`
- C candidate: Blob `5c37ebea98436fc985a94f17063b50b4df7ad7a6`
- H wire crosswalk candidate: Blob to be pinned after readback.

## 1. One recovery round is immutable / 单轮恢复不可变

A RecoveryRound is identified by `(RecoveryEpochRef, RecoveryRound, CutoffRequestIdentityDigest)`. The round's frozen owner snapshots, exact committed prefix P, manifest payload, manifest_id/digest, Batch record and Manifest record are immutable. Retrying after timeout/lost ACK MUST use the same stable identities and authoritative lookup; it MUST NOT allocate a new batch/manifest merely because the client did not receive the ACK.

Any owner-local request/admission/scope/gate-generation advance after a snapshot cannot be appended retroactively to that round. It remains blocked and is assigned to a successor RecoveryRound with fresh owner snapshots and a fresh Batch/Manifest pair. The prior round remains immutable and auditable.

## 2. Batch-before-Manifest is a durable two-record protocol / Batch 先于 Manifest

For each round, Storage/COC enforces:
1. freeze complete owner snapshots and participant enumeration against exact committed prefix P;
2. prepare canonical manifest payload and content/member-set digests without claiming it is committed;
3. quorum commit `COC_RECOVERY_CUTOFF_BATCH` binding P, owner snapshot roots, high-waters, counts and manifest identity/digests;
4. quorum commit `PARTICIPANT_SET_RECONCILIATION` binding the exact Batch record ref, position and entry digest and repeating the exact manifest identity/digests/counts/roots;
5. linearizable readback of both records and verify strict same-prefix order `BatchPosition < ManifestPosition`, exact reference/digest equality and quorum evidence;
6. only then transition to PARTICIPANTS_RECONCILING.

A crash after step 3 leaves the system fenced. The new leader performs same-identity lookup and completes/verifies step 4; it may not create a replacement batch. A missing, conflicting or out-of-order Manifest leaves RESTORE_FENCED.

## 3. Complete-set proof is not just a count / 完整集合证明不只是 Count

The Storage verifier MUST compare:
- COC participant enumeration at P, with explicit query/projection identity and pagination-complete evidence;
- each I/D/C owner request and admission snapshot, including independent request/admission ledger roots and high-waters;
- union manifest member set, duplicate-free canonical ordering, per-owner counts and membership proof references;
- every COC participant's owner-specific joins and every owner-local admission's disposition.

A count equality without exact member identity and root equality is insufficient. Empty is a first-class explicit empty set, not missing data. Partial reads, stale indexes, unknown owner verifier, missing ledger pages or anti-rollback uncertainty return INCOMPLETE/UNKNOWN and keep recovery fenced.

## 4. Owner release is a separate owner transaction / Owner Release 是独立事务

After reconciliation, each owner independently performs a fresh owner-local currentness read and CAS at its own authoritative serialization boundary. Storage requires a signed release record binding:
`OwnerKind + GateRef + GateGeneration + ScopeBinding + RecoveryEpoch + BatchRef/Position/EntryDigest + ManifestRef/Position/EntryDigest/ContentDigest + RequestHighWater/Root + AdmissionHighWater/Root + ReconciliationRoot + AntiRollbackAnchor`.

The owner's CAS MUST verify that current GateGeneration, scope/lineage version, request high-water, admission high-water, roots, key status and anti-rollback anchor still equal the release's frozen values. A changed value rejects release and requires a successor round. The release record is append-only and owner-signed. Storage can verify and persist it but cannot issue it or substitute its own decision.

I release does not grant permission or decide revocation victory. D release does not clear effective ForgetFence or producer barrier. C release does not authorize an individual provider invocation. COC epoch completion does not replace any owner release.

## 5. Race outcomes / 竞争结果

| Race | If request/admission wins serialization first | If close/fence wins first |
|---|---|---|
| I request vs I authorization/receipt issue/consume | admission is durably recorded and included in frozen in-flight set | authorization/receipt effect rejected behind closed gate |
| D Producer/Work/Queue/Lease/Retry/Replay vs ForgetFence | admission/attempt recorded and reconciled | protected progress rejected/quarantined |
| C provider send admission vs egress close | durable attempt included and same-key provider evidence reconciled | send rejected with authoritative NOT_INVOKED proof; no transport write |
| Any new request after frozen snapshot | remains blocked and belongs to successor round | remains blocked and belongs to successor round |

The first column never means that a provider has accepted work or that a Forget/permission effect is terminal. It means only that a durable admission won the owner-local ordering and must be reconciled.

## 6. COC state transitions and release barrier / COC 状态转换与 Release Barrier

The only path to `RECOVERY_EPOCH_COMPLETED` is:
`RECOVERY_FENCED → PREFIX_VERIFIED → CUTOFF_BATCH_COMMITTED → PARTICIPANT_MANIFEST_COMMITTED → PARTICIPANTS_RECONCILING → ALL_REQUIRED_OWNER_RELEASES_VERIFIED → RECOVERY_EPOCH_COMPLETED`.

The final record binds exact P, Batch, Manifest, reconciliation root and the complete required owner-release reference set. Any absent/duplicate/wrong-owner/stale release, changed high-water, unresolved participant or unknown proof prevents completion. Completion permits only the COC recovery service transition; it is not an application-level success signal.

## 7. Required Storage verification / Storage 必需验证

Specified, not executed:
- crash at every boundary before/after Batch commit and Manifest commit;
- lost ACK and idempotent same-key retry;
- Batch/Manifest inversion and cross-prefix mismatch;
- omission/duplicate/partial page/stale replica/empty-vs-null;
- request/admission high-water advancing during reconciliation;
- owner gate generation/scope version advancing between seal and release CAS;
- owner release missing, duplicated, stale, forged, wrong owner or wrong Batch;
- restore from stale snapshot cannot reduce cursor/generation or reopen gate;
- COC completion without every required owner release is rejected.

## 8. Decision boundary / 决议边界

This addendum is a Storage-role candidate authored in the coordinating session. It is not an independent Storage Owner acceptance, deployed sequencer, quorum implementation, linearizable readback proof or fault-injection result. It requires exact H/I/D/C review and a new A integration review. Gate A remains PARTIAL PASS/OPEN; Gate B/C BLOCKED; R1/R2 OPEN; JF-10 P0 OPEN; production activation NOT AUTHORIZED.
