# Phase 3.8.3 — Storage Review of H Storage-Resolution Verifier Seam
# Phase 3.8.3 — Storage 对 H Storage-Resolution Verifier Seam 的复审

- Owner: Storage — COC Durable Log / Prepared Participant / Recovery
- H Unified schema 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H mapping Blob: `c196fdc7a9d88e344d37ba2810a9bce1803f8b96`
- H validator core Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H test source Blob: `70a3796446553464e71999f916b76bc22e47da11`
- H current-head CI run `44068869146`, exact commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`: **SUCCESS**
- H closure addendum Blob: `9083ad54581352c83be21ac981aea845cd307382`
- Storage per-authority serialization anchor ADR Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`
- Decision: **ACCEPT AS FAIL-CLOSED STORAGE PROOF CONSUMER INTERFACE ONLY; SAME-GID RUNTIME PROOF OPEN**
- Provenance: delegated Storage-role review; not an independent human Storage Owner signature.

## 1. Storage authority boundary / Storage 权威边界

Storage owns physical persistence, PreparedParticipant identity, Storage PrepareAttemptRef/generation, PreparedTransactionGID, database incarnation, participant ledger, COC durable records, RecoveryCutoff Batch/Manifest and StorageResolutionProof. H's `verify_storage_resolution_proof` is only a consumer-side verification seam. It cannot mint a Storage resolution or convert an unresolved participant into terminal.

Storage 独占物理持久化、PreparedParticipant、Storage PrepareAttempt、PreparedTransactionGID、Database Incarnation、Participant Ledger、COC Durable Record、RecoveryCutoff Batch/Manifest 和 StorageResolutionProof。H 的 `verify_storage_resolution_proof` 仅是消费侧验证接口，不签发 Storage Resolution，也不能把未决 Participant 转为终态。

## 2. Required callback contract / Callback 必需合同

The Storage callback MUST verify:
- exact Storage authority and database-incarnation identity;
- exact PreparedParticipantRef, Storage PrepareAttemptRef/generation and participant ledger entry/version/digest;
- exact PreparedTransactionGID, engine-native transaction identity and recovery observation under the same database incarnation;
- immutable operation/participant tuple, C object/outcome digest, D/I owner proof references and COC intent/reservation joins as applicable;
- exact StorageResolutionProof issuer, payload digest, state transition and authoritative readback;
- RecoveryBatch/Manifest positions, distinct digest domains, quorum commit proof and Batch-before-Manifest backlink when the resolution depends on a recovery cutoff;
- exact per-authority SerializationTransitionRef/revision where required, without treating it as an owner counter or substitute for PreparedTransactionGID.

Storage Callback 必须验证 Storage Authority/Database Incarnation、PreparedParticipant、Storage PrepareAttempt、Participant Ledger、PreparedTransactionGID、Engine-Native Transaction Identity、同一 DB Incarnation 的 Recovery Observation、不可变 Operation/Participant Tuple、C/D/I Proof、COC Join、Resolution Issuer/Digest/State/权威 Readback，以及 Recovery Cutoff 相关的 Batch/Manifest/Quorum/Backlink。必要时校验 SerializationTransition，但不得将其当作 Owner Counter 或 PreparedTransactionGID。

## 3. Nominal types and fail-closed behavior / 名义类型与失败关闭

- Storage `SerializationRevision`, `PreparedTransactionGID`, `EngineNativeXIDRef`, Storage PrepareAttempt generation, C ProviderAttempt generation, D FenceGeneration, I PermissionEpoch and COC positions are distinct nominal types.
- Missing database incarnation, uncertain failover/restore history, absent prepared-transaction lookup, incomplete participant ledger, missing quorum/readback or ambiguous same-GID recovery returns UNKNOWN / RESTORE_FENCED.
- A mismatched GID, DB incarnation, participant tuple, digest or contradictory terminal record returns INVALID / integrity incident.
- H cannot interpret an unavailable Storage callback as success and cannot release C/D/I gates.
- The serialization anchor is a physical order primitive; it is not COC quorum authority, D Forget authority or I authorization.

Storage SerializationRevision、PreparedTransactionGID、EngineNativeXID、Storage PrepareAttempt、C ProviderAttempt、D FenceGeneration、I PermissionEpoch 和 COC Position 均为不同名义类型。DB Incarnation、Failover/Restore History、Prepared Transaction Lookup、Participant Ledger、Quorum/Readback 任一不可用，必须 UNKNOWN/RESTORE_FENCED。GID/Incarnation/Tuple/Digest/Terminal Record 矛盾为 INVALID/Integrity Incident。H 不得把 Callback 不可用当作成功，也不得释放 C/D/I Gate。

## 4. Storage disposition / Storage 侧结论

**Delegated Storage-role decision: ACCEPT `verify_storage_resolution_proof` as a fail-closed consumer interface only. Production same-GID lookup, durable participant ledger, COC quorum, Batch/Manifest linearizable readback, database-incarnation continuity, restore/failover drills and L3 fault injection remain OPEN; NOT FROZEN.**

This review does not claim Storage v3.2.3 implementation conformance, Gate B persistence deployment, Gate C end-to-end fault injection, JF-10 completion, physical Forget or production activation.

**角色模拟 Storage 侧结论：** 仅接受 H `verify_storage_resolution_proof` 为 Fail-Closed 消费接口。生产 Same-GID Lookup、持久 Participant Ledger、COC Quorum、Batch/Manifest Linearizable Readback、DB Incarnation 连续性、Restore/Failover 演练与 L3 故障注入仍 OPEN，不冻结。

本复审不声称 Storage v3.2.3 实现符合、Gate B 持久化部署、Gate C 端到端故障注入、JF-10 完成、物理 Forget 或生产激活。
