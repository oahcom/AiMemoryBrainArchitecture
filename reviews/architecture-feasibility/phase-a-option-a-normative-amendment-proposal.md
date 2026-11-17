# ARCH-CONSOL-003A — Proposed Normative Amendments for Option A
# ARCH-CONSOL-003A — Option A 规范性修订提案

- Target ADR: Storage/D Serialization Topology ADR, Blob bb544ba2f346bdc130d524bd5c7310d86f367988
- Target baseline: Storage v3.2.3 body + §8.1–8.7 addendum
- Status: **PROPOSED TEXT FOR STORAGE/D/A OWNER REVIEW — NOT ADOPTED**
- Scope: close A-01 through A-05 from the independent topology review
- This proposal does not modify the Storage Owner branch.

## 1. Transaction executor and owner write authority / 事务执行者与 Owner 写入权威

**Proposed normative text**

For each BrainAuthorityRef, D and Storage MUST use one transaction execution context bound to the exact SerializationDomainRef and DatabaseIncarnationRef. The context is a physical transaction coordinator only; it is not a semantic authority.

- D MUST authorize every D-owned row mutation through a D-issued immutable mutation command binding the operation, expected D state, owner record type, scope/lineage, request digest and D signer/currentness.
- Storage MUST authorize every Storage-owned row mutation through a Storage-issued immutable mutation command binding the exact prepared participant, GID/attempt/incarnation, visibility or NO_PUBLICATION outcome and Storage signer/currentness.
- The transaction executor MUST reject a command from the wrong owner, stale owner generation, mismatched tuple or reused transition identity.
- Database roles MUST prevent Storage credentials from arbitrarily creating or rewriting D semantic rows, and prevent D credentials from creating or rewriting Storage VisibilityPointer/PublicationReceipt/outcome rows.
- One transaction MUST commit the authorized D mutation(s), Storage mutation(s), anchor CAS and append-only SerializationTransition record atomically. The transaction executor's commit receipt proves atomic persistence only; it does not replace D or Storage signatures or semantic decisions.
- If D and Storage run in separate processes, the exact shared transaction-context API and credential/capability handoff MUST be specified. Independent service-local transactions are not equivalent.

**中文规范**

每个 BrainAuthorityRef 的 D 与 Storage 必须使用一个绑定精确 SerializationDomainRef 和 DatabaseIncarnationRef 的事务执行上下文。该上下文仅是物理事务协调器，不是语义权威。

- 每个 D 自有行变更必须由 D 签发不可变 Mutation Command 授权，绑定 Operation、预期 D 状态、Owner Record 类型、Scope/Lineage、请求摘要及 D 签名/Currentness。
- 每个 Storage 自有行变更必须由 Storage 签发不可变 Mutation Command 授权，绑定精确 Prepared Participant、GID/Attempt/Incarnation、Visibility 或 NO_PUBLICATION 结果及 Storage 签名/Currentness。
- 事务执行器必须拒绝错误 Owner、过期 Owner Generation、不匹配 Tuple 或重复 Transition Identity。
- DB Role 必须阻止 Storage 凭证任意创建/改写 D 语义行，也必须阻止 D 凭证创建/改写 Storage VisibilityPointer/PublicationReceipt/Outcome 行。
- 同一个事务必须原子提交获授权的 D Mutation、Storage Mutation、Anchor CAS 和 Append-only SerializationTransition。事务执行器 Commit Receipt 仅证明物理原子持久化，不能替代 D/Storage 签名或语义决议。
- 若 D/Storage 位于不同进程，必须明确共享 Transaction Context API 和凭证/能力传递；两个独立服务本地事务不等价。

## 2. D effect permit and lifecycle transition coverage / D Effect Permit 与生命周期转换覆盖

**Proposed normative text**

The protected serialization set MUST cover every transition that can add, expand, authorize or terminalize work that may read protected source data or publish a derivative. At minimum it includes:
1. ProducerClass registration/status and ProducerWork admission.
2. Attempt/Lease acquisition or replacement when it changes executable work membership or publication capability.
3. Retry, recompile-child, DLQ replay, restore/rebuild/backfill activation when it adds or reactivates work or lineage.
4. Complete direct/transitive dependency registration and any late dependency expansion.
5. D PublicationParticipant admission.
6. D InstallForgetFence and barrier/high-water capture or a successor reconciliation checkpoint that changes the authoritative affected set.
7. Storage final VisibilityPointer/COMMITTED_VISIBLE and terminal NO_PUBLICATION.
8. D CompleteProducerWork/ResolveProducerWork/barrier terminalization when it can close the last unresolved participant or authorize Forget completion.

For protected source-read and execution boundaries, D MUST issue a typed, single-use or otherwise non-replayable EffectPermit bound to BrainAuthorityRef, WorkItemId, AttemptId, LeaseId, exact source/lineage/scope digest, observed ForgetFenceGeneration and serialization anchor revision. Permit issuance/consumption MUST have a defined linearization point against InstallForgetFence.

- A permit that linearizes before Fence is a pre-Fence in-flight participant and MUST be included in the D barrier; Fence cannot become effective until it is completed, cancelled or authoritatively proven unable to read/publish.
- A permit requested after Fence wins MUST be denied/quarantined.
- A stale permit, changed lineage/scope, changed attempt/lease, unknown currentness or missing anchor continuity returns UNKNOWN/DENY.
- A late dependency discovered after Fence MUST reopen/extend the barrier under a new immutable checkpoint; it cannot be omitted from a previously asserted complete snapshot.
- No terminal NO_PUBLICATION may be issued while a lease, attempt, retry, replay or delayed writer can still create visibility.

This does not require holding a database transaction open for the duration of model execution or source I/O. It requires a durable, typed effect permit and explicit ordering of the protected effect against the fence.

**中文规范**

受保护序列化集合必须覆盖所有可能增加、扩展、授权或终结受保护源读取/Derivative 发布工作的状态转换，至少包括 ProducerClass 注册/状态、ProducerWork Admission、影响执行成员或发布能力的 Attempt/Lease、Retry/Recompile Child/DLQ Replay/Restore/Rebuild/Backfill、完整 Dependency Registration/迟到依赖扩展、D PublicationParticipant、D Fence/Barrier High-Water、Storage 最终 Visibility/NO_PUBLICATION，以及可能关闭最后未决 Participant 的 D Work Terminalization。

对受保护 Source Read 和 Execution，D 必须签发带类型、单次或不可重放的 EffectPermit，绑定 BrainAuthorityRef、WorkItemId、AttemptId、LeaseId、精确 Source/Lineage/Scope Digest、观察到的 ForgetFenceGeneration 和 Serialization Anchor Revision。Permit 的签发/消费必须定义相对于 InstallForgetFence 的线性化点。

- Fence 前线性化的 Permit 是 Fence 前在途 Participant，必须进入 D Barrier；Fence 只有在它完成、取消或被权威证明不可能再读取/发布后才可生效。
- Fence 获胜后请求的 Permit 必须拒绝/隔离。
- 过期 Permit、Lineage/Scope/Attempt/Lease 改变、Currentness UNKNOWN 或 Anchor Continuity 缺失均返回 UNKNOWN/DENY。
- Fence 后发现迟到 Dependency 必须通过新的不可变 Checkpoint 重新打开/扩展 Barrier，不得遗漏在此前声称完整的 Snapshot 之外。
- 只要仍有 Lease、Attempt、Retry、Replay 或延迟 Writer 能创建 Visibility，就不得签发终态 NO_PUBLICATION。

本条不要求在模型执行或源 I/O 整个期间持有 DB 事务；它要求使用持久、带类型的 EffectPermit，并明确受保护 Effect 相对于 Fence 的顺序。

## 3. BrainAuthority scope / BrainAuthority 范围

**Proposed normative text**

In v1, one atomic PublicationOperation, ProducerWork admission/fence operation and its Storage visibility outcome MUST be scoped to exactly one BrainAuthorityRef and one SerializationDomainRef. Cross-BrainAuthority atomicity is NOT SUPPORTED in v1.

A Global Forget spanning multiple BrainAuthorityRefs MUST fan out into independently fenced per-authority operations. A global coordinator may report completion only after every authority has returned its own authoritative terminal proof and the global inventory proves complete coverage. The global coordinator cannot create a cross-authority atomic transaction or infer completion from a partial set.

**中文规范**

v1 中，一个原子 PublicationOperation、ProducerWork Admission/Fence Operation 及其 Storage Visibility Outcome 必须严格限定在一个 BrainAuthorityRef 和一个 SerializationDomainRef。v1 不支持跨 BrainAuthority 原子性。

跨多个 BrainAuthorityRef 的 Global Forget 必须拆分为各 Authority 独立 Fence Operation。只有每个 Authority 都返回自己的权威终态 Proof，且 Global Inventory 证明覆盖完整后，全局协调器才能报告完成。全局协调器不能创建跨 Authority 原子事务，也不能根据部分结果推断完成。

## 4. I COMMIT_WON receipt crash and revocation semantics / I COMMIT_WON Receipt 崩溃与撤销语义

**Proposed normative text**

I receipt consumption is a single-use decision for one immutable publication tuple, not a reusable bearer permission.

- COMMIT_WON binds exactly one PublicationOperationId, D PublicationParticipantRef, StorageVisibilityParticipantRef, tuple digest, PolicyDomainRef and PermissionEpoch.
- Once COMMIT_WON wins the I sequencer for that exact tuple, a later revocation cannot retroactively change that tuple's decision; it can block later tuples. This rule is the meaning of the I linearization result, not a blanket authorization for other operations.
- Replaying the same receipt and exact tuple after crash MUST return the same immutable COMMIT_WON result and MUST NOT consume a second sequence position or authorize a different tuple.
- REVOCATION_WON means no Storage visibility commit may occur for that tuple.
- Crash after COMMIT_WON but before Storage commit leaves the operation unresolved. Recovery must resolve the same Storage operation to COMMITTED_VISIBLE or authoritative NO_PUBLICATION; it must not mint a new publication identity or silently reauthorize.
- UNKNOWN/IN_DOUBT, unavailable I sequencer or missing currentness proof never authorizes visibility.

**中文规范**

I Receipt Consumption 是针对一个不可变 Publication Tuple 的单次决议，不是可重复使用的 Bearer Permission。

- COMMIT_WON 精确绑定一个 PublicationOperationId、D PublicationParticipantRef、StorageVisibilityParticipantRef、Tuple Digest、PolicyDomainRef 和 PermissionEpoch。
- 该精确 Tuple 在 I Sequencer 中赢得 COMMIT_WON 后，后续 Revocation 不得追溯改变该 Tuple 的决议，但可以阻止后续 Tuple。这是 I 线性化结果的语义，不是对其他 Operation 的通用授权。
- 崩溃后使用相同 Receipt 和完全相同 Tuple 重放，必须返回同一不可变 COMMIT_WON 结果，不得消耗第二个 Sequence Position，也不得授权不同 Tuple。
- REVOCATION_WON 意味着该 Tuple 不得发生 Storage Visibility Commit。
- COMMIT_WON 后、Storage Commit 前崩溃时，Operation 保持未决；恢复必须解析同一 Storage Operation 为 COMMITTED_VISIBLE 或权威 NO_PUBLICATION，不得创建新 Publication Identity 或静默重新授权。
- UNKNOWN/IN_DOUBT、I Sequencer 不可用或 Currentness Proof 缺失，均不得授权 Visibility。

## 5. Anchor checkpoint and restore continuity / Anchor Checkpoint 与恢复连续性

**Proposed normative text**

The anchor transition table MUST expose a verifiable checkpoint/root that commits to the exact contiguous transition prefix for one BrainAuthorityRef and DatabaseIncarnationRef. Restore/failover MUST prove:
- the restored anchor revision and transition root are not below the last independently durable checkpoint;
- there is one authoritative primary and the former primary is fenced;
- every D/Storage owner record referenced by the transition prefix is present and digest-consistent;
- no transition fork, duplicate identity with different digest, missing revision or rollback exists;
- D Fence/Producer/Dependency/Barrier and Storage participant/Visibility/NO_PUBLICATION ledgers reconcile to the same anchor prefix.

Any unknown/forked/rolled-back prefix leaves the authority RESTORE_FENCED. The transition checkpoint is physical continuity evidence only; it cannot issue D/I/C/COC owner decisions.

**中文规范**

Anchor Transition Table 必须提供可验证 Checkpoint/Root，承诺一个 BrainAuthorityRef 和 DatabaseIncarnationRef 下精确连续的 Transition Prefix。Restore/Failover 必须证明恢复后的 Anchor Revision/Root 不低于最后独立持久 Checkpoint；只有一个权威 Primary 且旧 Primary 已隔离；Prefix 引用的 D/Storage Owner Record 全部存在且 Digest 一致；不存在 Fork、同 ID 不同 Digest、缺失 Revision 或回滚；D Fence/Producer/Dependency/Barrier 与 Storage Participant/Visibility/NO_PUBLICATION Ledger 对齐到同一 Anchor Prefix。

任何 UNKNOWN/Fork/Rollback Prefix 都必须令该 Authority 保持 RESTORE_FENCED。Transition Checkpoint 仅是物理连续性证据，不能签发 D/I/C/COC Owner 决议。

## 6. Adoption and gate mapping / 采纳与 Gate 映射

The above clauses are proposals. Storage/D must decide whether to adopt them in a successor ADR. If adopted:
- L1 closes only after A-01/A-02/A-03 are normatively specified and D/Storage/A exact reviews agree.
- L2 closes only after the I receipt rule, transaction executor authority, and restore checkpoint composition are bound to exact contracts.
- L3 closes only after deterministic concurrency/reference-model and fault vectors execute against the exact contract.
- L4 remains DB engine/version/configuration, deployment/operator, HA/PITR, production adapters and physical crash/failover/restore drills.

上述条款仍是提案，必须由 Storage/D 在后继 ADR 中决定是否采纳。若采纳：A-01/A-02/A-03 被规范化且 D/Storage/A 精确复审一致后才可关闭 L1；I Receipt、事务执行权威和恢复 Checkpoint 组合进入精确合同后才可关闭 L2；确定性并发参考模型/故障向量实际执行后才可关闭 L3；L4 仍是 DB Engine/版本/配置、部署/Operator、HA/PITR、生产 Adapter 与物理故障/恢复演练。

