---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-e-memory-compiler-2026-11-16"
        - "source commit: ee098e14747d9915de5b3efb63b3a8dd77f670ed"
        - "original source blob: 5ca77a5b48e69afb3bc81429baf538be7dce4d46"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact source Blob pinned; translated body retained; semantic parity review pending."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/accepted-receipt-and-idempotency-contract.md"
    en: "docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md"
    zh-CN: null
---

# Accepted Receipt、Compiler 完成与幂等契约

- 文档 ID：E-RECEIPT-001
- 版本：1.0
- 源分支：session-e-memory-compiler-2026-11-16
- 源文件版本：精确源 Blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46`，源提交 `ee098e14747d9915de5b3efb63b3a8dd77f670ed`。
- 源规范：[已恢复的规范源](../../../04-memory-compiler/accepted-receipt-and-idempotency-contract.md)（`5ca77a5b48e69afb3bc81429baf538be7dce4d46`）。
- 对应英文：[Accepted Receipt, Compiler Completion and Idempotency Contract](../../en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md)
- 状态：E 的 CANDIDATE 契约；Storage 实现、D Producer API、H Envelope 和 I Policy 批准仍为 OPEN

## 1. 证据必须分离

以下证据对象证明不同事实，**MUST NOT** 合并成一个 Accepted/Success Boolean。

| 证据 | 签发方/Owner | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| AcceptedReceipt | E | 不可变来源 Event、Payload Ref/Digest、Idempotency Record 和 Compile Intent 可持久恢复 | D Admission、Compiler 完成、Canonical Commit、Dependency Registration、Publication 或 Indexing |
| ProducerRegistrationReceipt | D | 稳定 ProducerWorkItem 已持久登记到 D Producer Ledger/Barrier Inventory | Work 已执行、输出存在、Dependency Edge 已登记或发布成功 |
| CompilerCompletionReceipt | E | 指定 Compile Run 已达到持久化的 Compiler 终态，并具有 Stage/Provenance 引用 | Canonical Memory 已提交或派生输出已可见 |
| CanonicalCommitReceipt | D | D 接受并提交 Canonical Transaction；包含 D CanonicalCommitCursor 和准确 Aggregate Revision Ref | 派生 Projection/Index 已应用、Context 已更新或物理擦除 |
| DerivedRegistrationReceipt | D 或 D 指定的权威 Ledger | 指定派生 Artifact/Source Dependency 已持久登记在 D Dependency Inventory | Artifact 已可见或最终 Publication 已获准 |
| PublicationReceipt | 最终 Gate 权威；D/Storage 对 Receipt Schema 的所有权仍 OPEN | 准确 Artifact/Version 通过最终 Gate，且原子 Visibility Transition 已提交 | F IndexWatermark 已推进或 G ContextVersion 已改变 |
| IndexAppliedAcknowledgement | F | 指定 Index/Channel Partition 已持久核算某个 Canonical 前缀，并返回类型化 IndexWatermark | Forget 完成或物理删除 |

Transport ACK、HTTP 2xx、Queue Enqueue、AcceptedReceipt、CompilerCompletionReceipt、D RegistrationReceipt 或本地数据库 Commit，都不能替代表中其他证据。

## 2. Accepted 语义与 Ingress 线性化点

`Received` 表示字节到达某个进程，数据可能仍处于易失状态。只有在不可变 EventRef、已验证的不可变 Payload Ref/Digest、Idempotency Record、AcceptedReceipt 和持久化 CompileIntent/Outbox 已原子提交，或通过已证明可恢复的 WAL 提交后，才算 `Accepted`。

推荐事务顺序：
1. 认证传输上下文，并通过 H/I 解析可信 ProducerIdentity；校验 Payload 声明与之匹配。
2. 根据 I 当前 Policy/PermissionEpoch 授权 Ingress；解析 B 类型化 ScopeRef 和 Security Domain。
3. 持久化不可变 Payload Bytes/Ref，并在 Metadata Commit 前验证 Digest。
4. 在一个事务中持久化 Event、Payload Ref/Digest、Idempotency Unique Row、AcceptedReceipt 和 CompileIntent/Outbox。
5. Commit。该 Commit 就是 Accepted Linearization Point。只有此后才返回 Receipt。
6. 至少一次 Dispatch；Queue Delivery 不是第二次 Acceptance。

如果 Payload Storage 和 Metadata DB 分离，必须先持久化暂存不可变 Payload 并验证，再由 Metadata Transaction 引用它。崩溃可以留下孤儿暂存 Blob，但不能暴露指向缺失/可变字节的 Accepted Event。WAL 方案必须有 Durable Commit Marker，将全部接收记录绑定起来。具体 Storage 产品、Replication 和 fsync 要求仍为 OPEN。

## 3. 幂等与认证命名空间

候选命名空间：

`(issuer_ref, authenticated_principal_ref, producer_identity_ref, security_domain_ref, validated_scope_binding, operation_family, caller_idempotency_key)`

- Principal 和 ProducerIdentity 必须来自认证传输/安全上下文，不能来自 Payload 自我声明。
- ScopeRef 是 B 的类型化领域引用；Scope 本身不授予 Permission。I 决定授权的 Scope Binding，以及规范化 ScopeRef 集合是否/如何参与 Namespace。
- Security Domain 是 I 管理的隔离边界，不能从任意 Payload 文本推断。
- Event/Operation Family 用于区分不同语义。
- 同一个逻辑提交在重连/重试期间保持 Caller Key 不变。

Semantic Request Digest 包含不可变 Payload Bytes/Digest、Event Family/Schema、可信 Producer Binding、已验证 Scope/Security Domain Binding、来源/环境身份，以及语义相关的来源时间/内容类型。它排除 Transport Attempt、Retry Time 和仅用于 Trace 的元数据。算法和 Canonicalization Profile 必须带版本；H 的 Wire Canonicalization 仍为 CANDIDATE。

| 已存在的 Key | Digest | 结果 |
|---|---|---|
| 不存在 | 有效 | 创建一个 Event、Receipt 和 Compile Intent |
| 已存在 | 规范化语义 Digest 相同 | 返回原 Receipt/Event/Intent/Work Identity 和当前状态；不产生重复副作用 |
| 已存在 | Digest 不同 | Idempotency Conflict；保留原记录 |
| 已有 Forget/Retention Tombstone | 任意 Replay | 按策略安全抑制/拒绝；绝不重建 Payload 或 Work |

Receipt Replay 读取原记录，不重新运行 Compilation、不延长 Retention，也不绕过当前 Authorization/Forget。受控 Recompile 使用新的 DerivationRunId，并且必须通过当前 I/D 检查。

## 4. Compiler Completion 是独立状态机

Compiler Work Lifecycle 和 D Barrier 映射由 E 的 `compiler-state-and-producer-admission.md` 规范定义。关键规则：在 E 将派生能力 Work 入 Queue、Lease 或执行前，D Registration 必须持久化。E 跟踪 Accepted、Queued、Leased、Running、Staged、DependencyRegistered、Retry、DeadLettered 和 Terminal；D 跟踪 Admission、Barrier Membership、Dependency Receipt 和 Terminal Disposition。DLQ/Lease Expiry 不是终态。

CompilerCompletionReceipt 必须绑定：
- CompileIntentId、ProducerWorkItemId、DerivationRunId 和最终 AttemptId；
- EventRef 和来源血缘 Digest/引用；
- Compiler/Extractor/Normalizer/Consolidator/Model/Prompt Template/Schema Version；
- Stage Outcome、Provenance Ref 和 Terminal Disposition；
- 已存在的 DerivedRegistrationReceipt ID、PublicationReceipt ID 和 CanonicalCommitReceipt 引用，分别作为独立可选证据；
- 已观察到的 PermissionEpoch 和 ForgetFenceCursor，仅作为历史观察，不是当前授权；
- 完成时间、结构化结果/错误和 Idempotency Digest。

Candidate-only Compilation 可以没有 CanonicalCommitReceipt 或 PublicationReceipt。它仍然只是 Compiler Output，不会自动成为 Canonical Claim/Fact。

## 5. 类型化 Cursor 与 Epoch 使用

| 字段 | 正确类型/Owner | E 的规则 |
|---|---|---|
| Source Ingress Position | SourceEventCursor / E | 每个声明的 Source/Ingress Partition；仅用于 Acceptance Replay |
| Canonical Transaction Position | CanonicalCommitCursor / D | 每个 Canonical Memory Authority 一个全局有序序列；只能存储 D 返回值 |
| Object Revision | AggregateRevision / D | 每个 Aggregate 独立单调递增；不可全局比较 |
| Lifecycle Transition Position | LifecycleEventCursor / D | 每个 Memory Lifecycle Stream；与 Commit Cursor 分开存储 |
| Projection Progress | IndexWatermark / F | 每个 Index/Channel/Partition；applied-through 为 CanonicalCommitCursor；E 不分配 |
| Forget Suppression Generation | ForgetFenceCursor / D | Operation + Target Set Digest + Generation；不是 Stream Cursor |
| Authorization Freshness | PermissionEpoch / I | 独立 Policy/Principal/Security Namespace；在受保护边界重新检查 |
| Context State | ContextVersion / G | 不透明下游依赖；E 不创建或递增 |

SourceEventCursor、Outbox Dispatch Offset、AttemptId、AggregateRevision、LifecycleEventCursor、IndexWatermark、ForgetFenceCursor、PermissionEpoch 或 ContextVersion **MUST NOT** 复制到 CanonicalCommitCursor。CanonicalCommitCursor 只能在 D 成功 Canonical Transaction Commit 时分配。D 契约规定单个 Brain Authority 内的已提交位置连续；被拒绝/中止的事务不获得 Cursor。

## 6. Retry、Replay 与未知结果

- 假定 Queue Delivery 为 At-least-once。稳定 EventRef/CompileIntentId/ProducerWorkItemId 用于去重逻辑 Work；每次 Retry 使用新的 AttemptId。
- Retry、DLQ Requeue、Operator Replay 和 Recompile 都必须重新认证，并重新检查当前 PermissionEpoch、Scope、Retention 和最新适用 ForgetFence。
- Replay 保留原 Source EventRef 和 Acceptance Receipt；不能用新 Queue Message/Attempt 逃避先前 Fence。
- 如果 D Admission/Registration/Commit/Publication 响应丢失，使用相同稳定 Operation Identity/Digest 查询。不得创建新 Key，也不得从 Timeout 推断成功。
- 如果 D Canonical Commit 成功但 E 丢失 ACK，按稳定 Canonical Operation Key 查询 D，并记录准确原始 CanonicalCommitReceipt。
- 如果 Publication Outcome 未知，Artifact 保持 Private，直到 PublicationOperationId 查询证明 Commit 成功。
- 只要仍可能 Replay/Publication，DLQ 就必须保持已登记且 Barrier-open。只有持久化 Terminal Disposition 才能关闭。
- Dedup Retention 必须覆盖支持的 Retry、Lease、DLQ、Operator Recovery 和 Audit 时间范围；具体时长及 Tombstone 过期仍是 I 拥有的 OPEN 决策。

## 7. 跨模块身份与 Permission

H 要求认证传输 Principal Binding。Payload 中的 `producer_id`、`ActorRef`、`agent_id` 和 `scope_ref` 都只是声明/选择器，不是凭据。I 的候选 ProducerIdentity 绑定已认证 Principal/Issuer、注册 Producer/Application、Workload/Instance、Credential Validity/Epoch、允许的 Event Family、Security Domain 和 Revocation State。E 必须拒绝/隔离不匹配，并且绝不能把 Payload ProducerId 当成认证。

ActorRef 和 ScopeRef 遵循 B/I 类型语义。PermissionEpoch 由 I 拥有；授权检查发生在 Ingress、受保护 Source/Evidence/Provenance 解引用前、敏感 Stage Commit 前、D Write Submission 前以及最终 Publication 时。如果 Principal、Permission、Scope、Security Domain 或 Forget State 未知，必须 Fail-closed。

H/I/B 套件仍为 CANDIDATE；本文消费其语义，但不冻结 Wire Field 或 Security Policy。

## 8. 一致性计划（NOT RUN）

1. 同一认证 Namespace 下，同 Key/同 Digest 返回唯一 AcceptedReceipt/EventRef/CompileIntentId。
2. 同 Key/不同 Digest 冲突且不修改原记录。
3. Acceptance ACK 丢失后返回原 Receipt，不产生重复 Work。
4. Accepted 不代表 D Producer Registration 或 Compiler Completion。
5. 没有 Canonical Commit 的 Compiler Completion 不得具有 CanonicalCommitCursor。
6. D Canonical Commit Receipt 必须包含 D 签发的、每个 Authority 全局有序的 CanonicalCommitCursor，以及独立 AggregateRevision/LifecycleEventCursor。
7. 只有 F ACK 后才记录 F IndexWatermark。
8. D Registration/Canonical Commit/Dependency Registration/Publication ACK 丢失时，通过稳定 Operation Lookup 恢复。
9. Permission 被撤销或 ForgetFence 推进后，Retry/Replay/Recompile 和迟到结果都必须被阻止。
10. DLQ 和过期 Lease 在 Terminal Disposition 前保持 Barrier-open。
11. 在 D Registration Receipt 和最终 PublicationReceipt 之前，Staged Artifact 永远不可被消费者看到。
12. B ADR 仍为 ADR-BLOCKED；任何 Candidate IR 都不能自动提升为 Canonical Claim/Fact。

**验收：** 本文仅是设计契约。Storage 原子性、D 可调用 API、运行时行为和一致性测试结果尚未验证。

## Phase 3.5 — Receipt 状态矩阵与恢复细化

### 1. 独立证据状态

| 状态/证据 | 已建立的持久事实 | 不证明什么 | 恢复 Owner |
|---|---|---|---|
| Accepted / AcceptedReceipt | 不可变 Event/Payload Ref+Digest、Idempotency Record 和 CompileIntent/Outbox 已持久化 | D ProducerWork Registration、Compile Start、Candidate Output、Canonical Commit、Dependency Registration 或 Publication | E |
| DurableIngestion | Source Bytes/Ref 和 Ingress Metadata 在声明的 Storage Profile 下可持久恢复 | Compilation 已开始或完成 | E/Storage |
| CompileStarted | 指定 DerivationRunId/AttemptId 在 D Admission 和当前 Auth/Fence 检查后开始 | Candidate 已存在或 Canonical Effect 已发生 | E |
| CandidateProduced | 指定 Candidate/Staged Artifact 和 Provenance Checkpoint 在 Private 状态存在 | Runtime Visibility、Canonical Commit、Dependency Completeness 或 Publication | E |
| CanonicalCommit | D CanonicalCommitReceipt 确认 Canonical Transaction Commit，包含 D CanonicalCommitCursor | Derived Artifact Publication、Index Application 或 Forget Completion | D |
| DerivedDependencyRegistered | D Dependency Inventory 已持久化准确 Artifact/Source Edge | Artifact 可见或 Publication Gate 通过 | D / 指定 Inventory Owner |
| DerivedArtifactPublished | Final Gate 和 Atomic Visibility Transition 具有持久化 PublicationReceipt | Canonical Commit、F Index Watermark、G ContextVersion 或 Global Forget Completion | D/Storage 所有权仍 OPEN；E 负责协调 |

Accepted 只是 Custody/Receipt 声明。绝不能描述为已编译、已保存到记忆、已提交或已发布。

### 2. Receipt 与 Idempotency Identity

- AcceptedReceiptId 对一个被接受的逻辑提交保持不可变。
- CallerIdempotencyKey 的 Scope 由已认证 Issuer + Principal + ProducerIdentity + Security Domain + 已验证 Scope Binding + Operation Family 确定。准确 Canonical ScopeRef Encoding 仍由 B/I/H 决定。
- SemanticRequestDigest 绑定不可变 Payload Bytes/Digest、Event/Schema Family、已认证 Producer Binding、已验证 Scope/Security Domain 和语义来源身份。排除 Retry Count、Transport Attempt、Retry Timestamp 和仅用于 Trace 的元数据。
- CompileIntentId 和 ProducerWorkItemId 必须持久化，并与原 Receipt 一起返回/恢复。Retry 不创建新的逻辑 Work ID。
- 每次执行 Attempt 都使用新的 AttemptId；每条不同 Recompile/Run Lineage 使用新的 DerivationRunId。
- Receipt Lookup 必须授权；一个 Principal/Scope 不得获知另一个提交者的 Receipt 是否存在或其 Payload Metadata。

### 3. 重复提交与 Replay 矩阵

| 条件 | 必需结果 | 副作用 |
|---|---|---|
| 首次有效 Key + Digest | Commit 一个 AcceptedReceipt/Event/CompileIntent | 一个逻辑提交 |
| 重复 Key + 相同语义 Digest | 返回原 AcceptedReceiptId、EventRef、CompileIntentId、ProducerWorkItemId 和当前状态 | 不创建重复 Event/Intent/D Registration |
| 重复 Key + 不同语义 Digest | Idempotency Conflict；原记录不变 | 不产生新 Compile/Canonical Effect |
| Receipt Commit 结果未知时收到重复提交 | 使用相同 Key/Digest 解析；不创建第二个 Key | 解析完成前暂停 Dispatch |
| Compilation 已开始/完成后收到重复提交 | 返回原 Receipt 和当前 Evidence Ref/Status | 不隐式重跑 Compile |
| 显式 Recompile | 新 DerivationRunId；当前 Auth/Fence 检查；链接原 Source/Intent；D Work Registration 形式仍 OPEN | 仅新 Run；不创建新 AcceptedReceipt |
| Forget 后 Replay | 按策略安全抑制/拒绝；不重建 Payload/Derivative；保留不可反向重建审计元数据 | 不可见、不复活 |
| Payload 过期/Forget 后保留 Receipt Tombstone | 在授权情况下仅返回策略安全、无内容的状态 | 绝不重建 Event Bytes 或 Compile Intent |

### 4. ACK 丢失与崩溃恢复

| 丢失/不明确的边界 | 恢复 Key | 强制行为 |
|---|---|---|
| Accepted Transaction ACK | 已认证 Idempotency Namespace + Semantic Digest | 查询已有 Receipt；不得重复 Acceptance |
| D RegisterProducerWork ACK | ProducerWorkItemId + Request Digest | D Lookup 返回持久化接受 Receipt 或明确拒绝前，不得 Enqueue/Lease/Run |
| Compile Start/Outbox ACK | CompileIntentId + Outbox Event ID | At-least-once Replay；保留相同逻辑 Work Identity |
| Dependency Registration ACK | DependencyRegistrationId + Request Digest | Artifact 保持 Private；查询/恢复相同 Registration |
| Publication ACK | PublicationOperationId + Request Digest | 找到已提交 PublicationReceipt 前保持 Private |
| D CanonicalCommit ACK | 稳定 Canonical Operation/Idempotency Key + Digest | 查询 D 并记录原 CanonicalCommitReceipt/Cursor；绝不发起第二次语义 Commit |
| CompleteProducerWork ACK | ProducerWorkItemId + Terminal Request Digest | D 确认 Terminal ACK 前 Barrier 保持未解决 |

任何边界发生进程崩溃，都必须从 Durable Intent + Stable Operation Key 恢复。Timeout/Lost ACK 是 UNKNOWN，绝不是成功。任何恢复路径都不得改变 Source Lineage、Idempotency Namespace 或 Fence Applicability。

### 5. Cursor Namespace 再确认

E 原样保存 D 签发的 CanonicalCommitCursor：每个 Canonical Memory Authority 一个全局有序序列。AggregateRevision 仍独立限定于每个 Aggregate；LifecycleEventCursor 仍是每个 Memory 的 Lifecycle Stream；IndexWatermark 仍由 F 按 Index/Channel Partition 拥有；ForgetFenceGeneration 仍是 D 的 Fence Namespace；PermissionEpoch 仍是 I 的授权新鲜度。禁止跨 Namespace 数值比较、转换或替代。

### 6. OPEN Receipt 决策

- OPEN-REC-01：AcceptedReceipt + Payload Ref + Idempotency Row + CompileIntent/Outbox 的 Storage Transaction/WAL 持久性、Replication 和崩溃恢复配置。
- OPEN-REC-02：Canonical Semantic Digest 算法/规范化版本，以及 B/H Typed Identity/Scope Serialization。
- OPEN-REC-03：Idempotency/Tombstone 保留期限和 Forget 后安全披露策略（I 拥有）。
- OPEN-REC-04：D 对 Producer Registration、Dependency Registration、Publication 和 Terminal Completion 的准确 Lookup Operation/Error Code。
- OPEN-REC-05：Recompile Registration 形式（子 Work Item 还是新登记 Work Item）由 D 决定。

## Phase 3.5 补充 — Producer Ledger Receipt 类型

D 的 ProducerRegistrationReceipt 携带 ProducerRegistryVersion 和 ProducerRegistrationSequence。后者是 D Producer Ledger 内用于证明被 Forget Barrier 纳入的排序 Token。它不是 CanonicalCommitCursor，绝不能存入该字段或解释为 Canonical Commit Position。

InstallForgetFence 在 Fence Installation Linearization Point 捕获 ProducerRegistryVersion + ProducerRegistrationHighWater。CaptureProducerRegistrationHighWater 返回不可变 BarrierSnapshotReceipt，证明使用了同一个 Cutoff；重复 Capture 不得移动该 Cutoff。E 记录两个 Receipt 身份和用于 Terminal Reconciliation 的 D Snapshot Version。

ResolveProducerWork 是 Registration/Dependency/Publication/Terminal ACK 丢失后的只读恢复路径。它使用原始稳定 WorkItemId 和 Registration Digest，可选 AttemptId/LeaseId/Operation ID。缺失/歧义结果为 UNKNOWN，不是创建新 Work/Publication Key 的理由。

ReconcileForgetBarrier 返回 D 在明确不可变检查点处的本地 Barrier 处置和未解决数量。E 提供完整证据，但不能自行宣布 Barrier 已排空。后来发现派生物或 Ledger Gap 时，必须追加新的 Reconciliation Checkpoint，并使此前的当前 Proof 失效。

Receipt Evidence Matrix 扩展为：
- ProducerClassRegistrationReceipt + ProducerRegistryVersion；
- ProducerRegistrationReceipt + ProducerRegistrationSequence；
- ForgetFenceCursor + Installation CanonicalCommitCursor；
- BarrierSnapshotReceipt + ProducerRegistrationHighWater；
- DependencyRegistrationReceipt + Dependency Inventory Position；
- PublicationReceipt + Visibility Commit Identity；
- ProducerWorkTerminalReceipt + D Barrier Reconciliation Cursor。

以上均为独立类型化证据对象，不能与 AggregateRevision、LifecycleEventCursor、IndexWatermark、ForgetFenceGeneration、PermissionEpoch 或 ContextVersion 互换。

## Phase 3.5 补充 — Receipt OPEN 项修正

D 的规范 Operation 文档已经定义 RegisterProducerClass、RegisterProducerWork、InstallForgetFence、CaptureProducerRegistrationHighWater、RegisterDerivedDependency、PublishDerivedIfFenceCurrent、CompleteProducerWork、ResolveProducerWork 和 ReconcileForgetBarrier 的语义 Lookup/Receipt 行为。因此 OPEN-REC-04 已收窄：D 语义 Lookup Identity、Receipt Class 和 Error Outcome 已定义；可调用 API/Transport Schema、认证序列化和 Wire Error Mapping 仍在 OPEN-API-01 下 OPEN。Storage/Consistency 原子可见性与恢复仍在 OPEN-STORAGE-01 下 OPEN。

AcceptedReceipt 自身的持久化 Commit Profile 仍由 OPEN-REC-01 单独跟踪。D Producer Ledger Receipt 持久性不能替代 E Ingress Transaction；AcceptedReceipt 也不意味着存在 D ProducerRegistrationReceipt。

## Phase 3.5 重新验证 — Receipt State Matrix 与 Replay

| 状态/证据 | 已建立的持久事实 | 不证明什么 | 恢复规则 |
|---|---|---|---|
| DurableIngestion | 不可变 EventRef 和 Payload Bytes/Ref/Digest 已持久化并完成完整性校验 | 除非另行提交，否则不证明 AcceptedReceipt、Compile Intent/Start 或 Canonical Effect | 通过 EventRef+Payload Digest 恢复；孤儿 Private Payload 不算 Accepted Work |
| Accepted / AcceptedReceipt | Event + 不可变 Payload Ref/Digest + 已认证 Idempotency Row + AcceptedReceipt + CompileIntent/Outbox 已原子提交或通过已证明可恢复 WAL 提交 | D ProducerWork Registration、CompileStarted、CandidateProduced、CanonicalCommit、Dependency Registration 或 Published | 相同认证 Namespace/Key/Digest 返回原 Receipt/ID；Digest 改变则冲突 |
| CompileStarted | 指定 DerivationRunId/AttemptId 在 D Admission 和最新 Auth/Fence 检查后开始 | Candidate、Canonical Commit 或 Publication | 恢复相同 WorkItem/CompileIntent；只有新执行才使用新 AttemptId |
| CandidateProduced | Candidate/Staged Artifact 和 Provenance Checkpoint 对指定 Run 私有存在 | Staging 可见性、Dependency 完整性、Canonical Commit 或 Publication | 解析相同 Artifact/Version 和 Dependency Operation ID；绝不暴露 Staging |
| CanonicalCommit | D CanonicalCommitReceipt 确认 Canonical Transaction 并返回 D 签发 CanonicalCommitCursor | Derived Publication、F Indexing、G Context 或 Forget Completion | ACK 丢失后按相同 Canonical Operation Identity 查询 |
| DerivedDependencyRegistered | D Inventory 已持久记录完整 Artifact/Source/Parent Edge 集合和位置 | 可见性或 Publish Gate 成功 | 使用相同 DependencyRegistrationId+Digest 查询；Partial/Unknown 保持 Private |
| DerivedArtifactPublished | D Final Gate + Atomic Visibility Boundary 具有持久化 PublicationReceipt 和 Visibility Commit Identity | F IndexWatermark、G ContextVersion、Global Forget Completion 或 Physical Erasure | 使用相同 PublicationOperationId+Digest 查询；结果不明确时保持 Private |
| CompilerTerminal | D ProducerWorkTerminalReceipt 核算每个输出并证明以后没有 Attempt 能发布 | 除非 D ReconcileForgetBarrier 确认，否则不证明 Forget Barrier 已排空 | 使用相同 WorkItemId+Terminal Digest 查询；Conflict 不可变 |

### 重复提交与 Replay

- Candidate Idempotency Namespace 仍等待 B/H/I 协议：已认证 Issuer + Principal + ProducerIdentity + Security Domain + Validated Scope Binding + Operation Family + Caller Key。Payload ActorRef/ProducerId/ScopeRef 都是声明，不是认证。
- 相同 Namespace/Key + 相同 Semantic Digest 返回原 AcceptedReceiptId、EventRef、CompileIntentId、ProducerWorkItemId 和当前已授权状态；不产生第二个 Event、Registration、Compile 或 Canonical 副作用。
- 相同 Namespace/Key + 不同 Digest 返回 IDEMPOTENCY_CONFLICT，原记录保持不可变。
- Receipt Commit 未知时使用相同 Namespace/Key/Digest 解析；不得创建新 Key、乐观返回成功或 Dispatch 重复 Work。
- Receipt Lookup 必须授权；其他 Principal 不能枚举 Receipt 是否存在。
- Outbox/DLQ Replay 保留 EventRef、CompileIntentId 和 ProducerWorkItemId；只有新执行才改变 AttemptId。Forget 后 Replay 必须重新授权/检查 Fence，不能重建已遗忘 Payload。
- Recompile 不等于重复 Accepted Submission：使用新的关联 DerivationRunId，不产生新 AcceptedReceipt；OPEN-RECOMPILE-01 管理子 WorkItem 重新 Admission。
- D Registration/Dependency/Publication/Terminal ACK 丢失时，使用原 Operation ID/Digest。UNKNOWN 意味着 Artifact 保持 Private 且 Barrier 保持打开。

Canonical Digest Profile、Typed Identity Serialization、Retention Horizon 和 Forget 后 Receipt 安全披露仍由 B/H/I/Storage 决定，当前 OPEN。没有任何 Wire Schema 或保留期限被冻结。

### Typed Cursor 与 Fence Generation Namespace — E 的明确契约

| Token | Owner/范围 | E 的处理方式 |
|---|---|---|
| CanonicalCommitCursor | D；每个 Canonical Memory Authority 一个全局有序序列 | 仅在成功 Canonical Commit 后原样保存 D 签发值。 |
| AggregateRevision | D；每个 Aggregate 独立序列 | 与 Aggregate Identity 分开保存；绝不能用作全局 Commit 顺序。 |
| LifecycleEventCursor | D；每个 Memory 独立追加流 | 只有存在 Lifecycle Event 时才保存；保留 Memory Scope。 |
| IndexWatermark | F；每个 Index/Channel Partition，applied-through CanonicalCommitCursor | E 提供来源/Outbox Event，但不分配或推进它。 |
| ForgetFenceGeneration | D；ForgetFence Namespace 中的单调 Generation，通过 ForgetFenceCursor 绑定 ForgetOperationId/Target Set Digest | 将其视为 Fence Token，不是 Commit Cursor 或 Work Registration Sequence。只通过 D 语义验证新鲜度。 |
| ProducerRegistrationSequence / ProducerRegistrationHighWater | D；Producer Work Ledger 和单个 Forget Barrier Cutoff | 独立保存；不得替代 CanonicalCommitCursor 或 ForgetFenceGeneration。 |
| PermissionEpoch | I；Policy/Security Domain | 通过 I 重新验证；绝不与 D Fence Generation 做数值比较。 |
| ContextVersion | G；受管 Context | 不透明下游引用；E 不分配。 |

禁止跨 Namespace 算术、数值比较、强制转换或 Token 替代。特别是，Fence Installation 可以带有用于审计的 Installation CanonicalCommitCursor，但该 Cursor 不定义也不替代 ForgetFenceGeneration。

## Phase 3.6 — Receipt 语义与持久恢复

### 1. Receipt 阶段是独立证据

| 阶段 | Receipt/证据 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| Accepted | AcceptedReceipt | E 在声明 Ingress 契约下可靠接收了已认证逻辑提交 | 除非 Receipt 契约明确包含 Payload Durability Profile，否则不证明 Payload Bytes 持久；也不证明 D Producer Admission、Compile Start、Candidate、Canonical Commit、Dependency Registration 或 Publication |
| Durable Ingestion | DurableIngestionReceipt / 不可变 EventRef + Payload Digest 和 Storage Durability Evidence | Source Bytes/Ref 和 Ingress Metadata 在声明 Storage Profile 下可持久恢复 | 不证明 Accepted、Queued、Compile Started 或任何 Canonical/Derived Effect |
| Compile Started | 绑定 WorkItemId、DerivationRunId、AttemptId、LeaseId 的 CompileStarted Evidence | 指定 Admission Attempt 在当前 Authorization/Fence 检查后开始 | 不证明 Candidate、Dependency Registration、Canonical Commit 或 Publication |
| Candidate Produced | CandidateProduced Evidence | 指定 Run 的 Candidate/IR/Provenance Checkpoint 在 Private 状态存在 | 不证明 Staging Visibility、Dependency Completeness、Canonical Commit 或 Publication |
| Dependency Registered | D DependencyRegistrationReceipt | 完整 Artifact/Version 和必需 Lineage Edge 已持久记录在 D Inventory | 不证明 Final Gate 已通过或 Artifact 可见 |
| Canonical Commit | D CanonicalCommitReceipt + CanonicalCommitCursor | D 提交了指定 Canonical Mutation | 不证明派生 Artifact Publication、Index Application、Context Activation 或 Global Forget Completion |
| Derived Artifact Published | D/Storage PublicationReceipt + Visibility Commit Identity | 准确 Artifact/Version 通过 Final Gate，并在原子 Visibility Commit 时变为可见 | 除非另行引用，否则不证明 Canonical Commit；也不证明 F IndexWatermark、G ContextVersion、Global Forget Completion 或 Physical Erasure |

**CompilerCompletionReceipt** 是 E 对实际存在的 Stage Receipt 的汇总引用。它不能把 CandidateProduced 升级成 DependencyRegistered、CanonicalCommit 或 Published。每个 Stage 都是追加式且可独立解析的证据。

### 2. ACK 语义

- Transport ACK / HTTP 2xx / Queue ACK 只能证明对应 Transport/Queue 声明的接收事实。
- 只有 E Acceptance Linearization Point（Event + 不可变 Payload Ref/Digest + Idempotency Row + AcceptedReceipt + CompileIntent/Outbox）在声明的 Transaction/WAL Profile 下持久化后，才返回 Accepted。
- 如果 Payload Durability 早于 Metadata Acceptance，或使用独立 Storage，则 Durable Ingestion 是单独证据。
- RegistrationReceipt 只证明 D Admission。
- DependencyRegistrationReceipt 只证明完整 Dependency Registration。
- PublicationReceipt 只证明原子 Visibility Transition。
- F IndexAppliedAcknowledgement 只证明指定 F Partition 的连续应用前缀。

### 3. 未知结果与 Retry Identity

对每个操作，Timeout/Lost ACK 都是 UNKNOWN，不是失败或成功。恢复必须使用原 Operation ID 和 Canonical Request Digest：

- Accepted：认证 Idempotency Namespace + Caller Key + Semantic Digest。
- Producer Registration：WorkItemId + Registration Digest。
- Lease：WorkItemId + AttemptId + LeaseId/Lease Epoch。
- Dependency Registration：DependencyRegistrationId + Dependency Digest。
- Canonical Commit：D Canonical Operation ID + Request Digest。
- Publication：PublicationOperationId + Publication Digest。
- Terminal Completion：WorkItemId + Terminal Digest。

相同 Identity + 相同 Digest 返回原不可变 Receipt/Outcome。相同 Identity + 不同 Digest 是 Conflict。任何 Timeout Recovery 都不得创建替代 WorkItemId 或 PublicationOperationId。

### 4. 崩溃 / Replay 矩阵

| 故障 | 恢复行为 | 可见性/Barrier 规则 |
|---|---|---|
| Accepted ACK 丢失 | 解析相同 Idempotency Namespace/Key/Digest；若已 Commit，返回原 AcceptedReceipt | 不重复 Event/Receipt/CompileIntent |
| Durable Ingestion ACK 丢失 | 解析 EventRef/Payload Digest 和 Storage Durability Record | 孤儿 Staged Payload 不算 Accepted Work |
| Worker 崩溃 | Lease 过期/撤销；保留 WorkItemId；重新检查当前 Auth/Fence 后创建新 AttemptId/LeaseId | 旧 Attempt 不得发布；Work 仍保持 Barrier-open |
| Lease 过期 | 视为旧 Lease 无效，不是 Work 终态；接管前解析 D 状态 | 不得关闭 Barrier |
| 重复 Attempt | 强制 Attempt/Lease Epoch 和唯一活动 Publication Identity；最终 Gate 拒绝过期 Attempt | 不得重复发布 |
| DLQ Replay | 同 WorkItemId、新 AttemptId/LeaseId；重新 Auth/Fence 检查并使用同一 D Registration | Terminal Receipt 前 DLQ 保持 Barrier-open |
| Outbox Replay | 使用稳定 Outbox Event/Operation Identity At-least-once Dispatch；动作前解析 D Receipt | 不产生重复逻辑 Work |
| Recompile | 相同 WorkItemId 和原 Source Lineage；新 DerivationRunId/不可变 Artifact Version；当前 Auth/Fence 检查 | 不得重置 Fence Applicability 或 Receipt Stage |
| Dependency 部分提交 | 解析相同 DependencyRegistrationId/Digest；完成完整集合或隔离 | 不得部分可见 |
| Canonical Commit ACK 丢失 | 解析相同 D Canonical Operation ID/Digest | 绝不发起第二次 Canonical Mutation |
| Publication ACK 丢失 | 解析相同 PublicationOperationId/Digest；区分 Committed/Aborted/Unknown | Unknown 保持 Private；Committed 返回原 PublicationReceipt |
| Final Transaction Commit 后、Local State 更新前崩溃 | 按稳定 Operation ID 读取权威 Visibility Marker + PublicationReceipt | 若已 Commit 则协调本地状态；绝不重新发布 |
| Separate-store Prepare/Commit 期间崩溃 | 幂等恢复 Coordinator 和全部 Participant Record；Prepared 在 Commit 前保持隐藏 | Prepare Record/陈旧 Token 不得导致可见 |
| Restore/Rebuild | 隔离 Projection/Staging；服务前 Replay 当前 Fence/Permission 控制状态 | 不得复活 |

### 5. Terminal 与 Reconciliation

Worker 返回、Queue Entry 消失、Lease 过期、Retry Budget 耗尽或本地写入 Completion Event，都不代表 Work Item 已终结。只有在每个 Run、Attempt、Staged Artifact、Dependency Registration、Canonical Operation、Publication Operation、Outbox 和 DLQ Replay 路径都已解决后，E 才能提交 CompleteProducerWork。D ProducerWorkTerminalReceipt 是 E 将 D Barrier Disposition 标记为 Terminal 的必要证据。

### 6. 一致性状态

Phase 3.6 在 `phase-3.6-producer-publication-conformance.md` 中列出的用例 **NOT RUN**。文档和 Repository Readback 不能证明事务正确性、防复活行为或运行时故障安全。
