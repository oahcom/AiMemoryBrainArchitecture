---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "04-memory-compiler/compiler-state-and-producer-admission.md @ bc36ad36895496f0f7707fcecb12d156c6be97c3"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Canonical source and bilingual mirror path verified; design status remains as stated in the document."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "Memory Compiler design specification: compiler-state-producer-admission"
    canonical_scope_id: "memory-compiler/compiler-state-producer-admission"
    canonical_scope_keywords:
      - state-machine
      - producer-admission
      - lease
      - barrier
      - terminal-disposition
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/compiler-state-and-producer-admission.md"
    en: "docs/en/04-memory-compiler/compiler-state-and-producer-admission.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/compiler-state-and-producer-admission.md"
---

# Compiler 状态机与 D Producer Admission 接口

- 规范源：[compiler-state-and-producer-admission.md](../../../04-memory-compiler/compiler-state-and-producer-admission.md)
- 规范源 Blob：bc36ad36895496f0f7707fcecb12d156c6be97c3

- 文档 ID：E-PRODUCER-ADMISSION-001
- 版本：1.0
- 源分支：session-e-memory-compiler-2026-11-16
- 对应英文：[Compiler State Machine and D Producer Admission Interface](../../en/04-memory-compiler/compiler-state-and-producer-admission.md)
- 状态：E Lifecycle 语义为 CANDIDATE；D 语义操作为 DECIDED；可调用 API/Transport 和 Storage 原子性为 OPEN

## 1. 身份层级

| Identity | 稳定性 | 含义 |
|---|---|---|
| EventRef | 不可变 | 一个已接收来源 Event |
| AcceptedReceiptId | 不可变 | E 对可靠 Ingress 的证据 |
| CompileIntentId | Retry 期间稳定 | 逻辑 Compilation Intent |
| ProducerWorkItemId | 同一逻辑 Work 的 Retry 期间稳定 | D 可见的 Producer Registration/Barrier 身份 |
| DerivationRunId | 每个 Run 一个；Recompile 时新建 | 特定 Compiler/Model/Schema 执行血缘 |
| AttemptId | 每次 Attempt 新建 | Retry/Worker 执行尝试 |
| LeaseId | 每次 Lease 新建 | 有时限的 Worker 所有权 |
| DerivedArtifactRef/version | 每个输出版本不可变 | 私有 Staged Derivative 身份 |
| DependencyRegistrationId | 稳定幂等 Key | D Dependency Registration 协调身份 |
| PublicationOperationId | 稳定幂等 Key | Final Gate/Visibility 协调身份 |

ID 必须不透明并持久分配。不得信任 Payload 提供的 ID 作为权威。Recompile 创建新的 DerivationRunId，并重新检查授权/Fence；D 是否要求新的 ProducerWorkItemId，还是在原 Work 下登记 Child，仍为 OPEN 的 D Interface Decision。无论哪种方式，都不得绕过原始 Source Lineage 或 Barrier。

## 2. 状态转换

```text
Received
  -> Validating
  -> Accepted
  -> D_Registration_Pending
  -> Registered
  -> Queued
  -> Leased
  -> Running
  -> Staged
  -> Dependency_Registration_Pending
  -> DependencyRegistered
  -> Publication_Gate_Pending
  -> Published
  -> Terminal
```

其他出口：
- Validating → Rejected（没有 Accepted Receipt；除非另行定义持久化且符合策略安全要求的拒绝 Receipt）。
- Accepted / Queued / Leased / Running / Staged → Cancelled 或 Suppressed；只有在持久化“不会发布”的证据后才 Terminal。
- Running / Staged / Dependency Pending → Retry，再使用相同 ProducerWorkItemId 和新 AttemptId 返回 Queued；必须重新授权/检查 Fence。
- Retry Budget 耗尽 → DeadLettered；只要仍可能 Replay，就**不是终态**。
- D Canonical Write → CanonicalCommitted 是独立结果/证据轴，不是 Published 的别名。
- LeaseExpired 是运维状态，只使该 Lease 失效，不终结 Work Item，也不将其从 D Barrier 移除。

## 3. Admission 与 Barrier 映射

| E 事件/状态 | D Ledger 必须表达的含义 |
|---|---|
| Accepted | 不意味着 D Admission |
| D_Registration_Pending | 请求可能已提交；E 必须按稳定 ProducerWorkItemId/Digest 查询 |
| Registered | D Registration Receipt 已存在；Barrier High-water/Registration Identity 已持久化 |
| Queued / Retry / DeadLettered | 同一个 D Registration 仍然开放；Retry/DLQ 不会从 Barrier 消失 |
| Leased / LeaseExpired | D 可以关联活动/过期 LeaseId + AttemptId；过期不是终态 |
| Running / Staged | D Registration 仍然开放；E 进度只是遥测，不代表 Barrier 完成 |
| DependencyRegistered | D Dependency Inventory 已有所有必需的直接/传递 Edge Receipt |
| Published / CanonicalCommitted | Durable Gate 和/或 Canonical Commit 证据独立记录 |
| Cancelled / Rejected / Terminal | E 提交持久化 Terminal Disposition；D 只有在验证证据且确认不可能再发布后才关闭 Barrier Item |

D 的 Forget 契约要求：Fence 的 Producer Registration High-water 之前接纳的每个 Work Item 都必须达到持久化 Terminal Disposition。E 绝不能删除 Registration、隐藏 DLQ Item，或把丢失的 Worker 当成已完成。

## 4. D 所需语义操作（不是 API 名称）

### 4.1 Producer Registration

E 需要一个 D 操作，在 Enqueue/Execution 前持久化登记逻辑 Producer Work。最低请求字段：
- ProducerWorkItemId、Producer Class 和已认证 ProducerIdentity Binding；
- Source EventRef，以及可用时的 Canonical Source Ref/准确 Version；
- Source/Transitive Lineage Digest 或获批的不透明 Dependency Token；
- ScopeRefs 和 Security Domain Binding；
- Operation、Correlation 和 Causation ID；
- Admission CanonicalCommitCursor（D 签发的当前 Authority Position；若尚无 Canonical Commit，则使用 D 明确定义的 Genesis/Empty 值）；
- 已观察 ForgetFenceCursor 和 I PermissionEpoch；
- Request Digest、适用时的初始 AttemptId/LeaseId、Producer Schema/Version。

最低结果：持久化 ProducerRegistrationReceipt、Registration Ledger Sequence/High-water Token，以及 Accepted/Rejected Disposition。按 ProducerWorkItemId + Digest 查询 Receipt 必须幂等。

**OPEN：** D 必须定义在尚无 Canonical MemoryRef 的 EventRef-only Ingress 场景下如何登记，以及一个逻辑 Work Item 是否对应一条 Ledger Entry，或每个 Attempt/Recompile 都单独登记。

### 4.2 Dependency Registration

E 需要 D 操作，在可见之前持久化登记每个 DerivedArtifactRef/Version 及完整来源祖先。最低请求：Artifact Ref/Version、ProducerWorkItemId、DerivationRunId、直接/传递 Source Ref 或 I 批准的不透明 Token、准确 Source Version、ProvenanceRef、ScopeRefs、Lineage Digest、已观察 Fence 和幂等身份。结果为持久化 DerivedRegistrationReceipt 和 Inventory Position。

相同 Key/Digest 的重复 Registration 返回原 Receipt；相同 Key/不同 Digest 冲突。部分 Registration 保持不可见。D 必须定义 Source Reference Class，以及由 D 本身还是 D 指定的 Inventory Service 拥有权威。

### 4.3 最终 Publication Gate

E 需要一个 D 权威 Final Gate，检查最新 ForgetFenceCursor 和 Registration Inventory，并将结果与并发 Fence Installation 串行化。最低请求：PublicationOperationId、Artifact/Version、ProducerWorkItemId、DerivationRunId、AttemptId/LeaseId、全部 Dependency Receipt ID、当前 PermissionEpoch/Authorization Decision Ref、已观察 ForgetFenceCursor、ScopeRefs 和 Request Digest。

结果必须是持久化 PublicationReceipt，并绑定准确 Artifact/Version、Dependency Receipt、Fence Generation、Permission Epoch 和 Visibility Outcome。Storage 在 Gate 成功 Commit 被证明之前不得暴露 Artifact。

**OPEN：** D 必须定义 Gate 自己执行 Visibility Transition，还是签发一次性 Fence Token，由 Storage 在共享 Transaction/CAS 下消费。Token 后跟一个未协调的 Write 不足以保证安全。

## 5. 故障语义

- Admission ACK 丢失：查询相同 Work ID；未知时绝不 Enqueue。
- Worker 崩溃/Lease 过期：D Registration 继续开放；新 Attempt 必须刷新 Permission/Fence。
- Dependency ACK 丢失：查询稳定 Dependency Key；Artifact 保持 Private。
- Dependency 部分写入：幂等恢复；不得部分 Publication。
- Publication ACK 丢失：查明 Commit 前 Artifact 保持 Private。
- Fence 或 PermissionEpoch 推进：陈旧 Lease/Attempt 被拒绝；不能通过刷新 Generation 让同一个陈旧结果合法。
- DLQ：在明确 Terminal ACK 或授权 Replay 前保持 Barrier-open。
- 迟到结果：丢弃/隔离；不得覆盖更新或终态。
- Restore：任何 Staging/Derived Object 可查询之前先应用当前 Fence。

## 6. 可观测性

必须跟踪：EventRef、AcceptedReceiptId、CompileIntentId、ProducerWorkItemId、DerivationRunId、AttemptId、LeaseId、D Registration Receipt/High-water、DependencyRegistrationIds、PublicationOperationId/Receipt、已观察 CanonicalCommitCursor、AggregateRevision Ref、LifecycleEventCursor、ForgetFenceCursor、PermissionEpoch、状态转换、Retry Count、Terminal Disposition、Correlation/Causation ID 和结构化故障类别。绝不记录已遗忘内容或敏感 Locator。

## 7. 一致性用例（NOT RUN）

- D Registration 先于 Queue/Lease；Admission Timeout 阻止执行。
- Fence Install 与 Registration 竞争时，只有一个串行化结果获胜。
- D Barrier 包含 Queue Pending、Leased、Expired、Retry、DLQ 和 Replay。
- Lease Expiry 不得被计为 Terminal。
- Final Gate 前必须完成 Dependency Registration。
- Staging 到 Gate 期间 Fence/Permission 变化必须拒绝 Publication。
- 每个边界的 ACK 丢失都能解析为相同 Receipt。
- Recompile 创建新的 Provenance/Run Identity，不能绕过 Source Fence。
- Terminal/Cancel 后的迟到结果不能发布。
- 崩溃/Restore 后 D/E 状态能够协调。

**本文不声称存在任何运行时接口或实现。**

## Phase 3.5 — Producer Work Lifecycle 与 Admission 细化

**状态：** E 拥有的 Lifecycle 语义为 CANDIDATE；D Operation Schema 和 D/E/Storage 线性化仍为 OPEN。本文不声称已有运行时实现。

### A. Producer Class Registration 与 Work Item Registration

两者是不同概念：
- **ProducerClass：** 标识可产生派生物的 Producer 边界，包括 Compiler Ingress、Extraction/Consolidation、Retry Scheduler、DLQ Replay Worker、Operator Replay/Recompile Worker，以及任何可能触发派生 Work 的 E-owned Outbox Dispatcher。
- **ProducerClassRegistration：** D 拥有的封闭世界 Inventory 声明，绑定稳定 Class ID/Version、Owner Module、认证 ProducerIdentity Class、Source/Derivative Capability、Scope Coverage、Enabled/Disabled State 和 Registration Schema。D 未确认 Class 已登记并 Active 前，E 不得执行可产生派生物的路径。
- **ProducerWorkItem：** 在已登记 Class 下接纳的一个逻辑、持久化 Work 单元。其稳定 ProducerWorkItemId 必须在 Queue Insert、Lease Acquire 或 Execution 之前持久化。
- D 契约将 RegisterProducerWork 用于单个 Work 登记。Class Registration 是否有独立 D Operation，以及准确 Request/Response/Version Transition 仍为 **OPEN-D-CLASS-01**。E 不得自行发明该 API。

### B. E 必须遵循的 Lifecycle/Identity 规则

| Lifecycle 场景 | E 规则 | 对 D Barrier 的影响 |
|---|---|---|
| 初始 Admission | 持久化 CompileIntent + 稳定 ProducerWorkItemId，再获得 D Durable Registration Receipt 后才 Enqueue | D Ledger 在执行前包含该 Work |
| Lease Acquire | 新 LeaseId + AttemptId；绑定 Worker Identity、Expiry、Observed PermissionEpoch 和 ForgetFenceCursor | 原 Work 继续开放；Lease 是证据，不是新 Admission |
| Lease Renew | 保留 LeaseId/AttemptId；重新验证当前授权/Fence 后才续租，并持久化结果 | 续租不能让 Admission 越过 Fence，也不能抹去 Barrier Membership |
| Lease Expiry | 标记 Lease 过期；保留 Work Item 和 Attempt History；接管前协调 Owner/Heartbeat | 过期绝不是 Terminal，不能关闭 Barrier |
| Retry | 相同 ProducerWorkItemId/CompileIntentId；新 AttemptId/LeaseId；重新授权/检查 Fence | 同一 Barrier Member 继续开放 |
| DLQ | 持久化 Parked Record，包含 Reason、Source Lineage 和 Replay Policy；D Registration 仍开放 | 只要可 Replay，DLQ 就不是 Terminal |
| DLQ Replay | 新 AttemptId/LeaseId，相同 ProducerWorkItemId；Dispatch 前按同 ID/Digest 解析 D Registration | Replay 不能逃离原 Barrier |
| Operator Replay | 已认证/授权操作；保留 Source Lineage 和 Work ID；审计 Operator/Reason | 不得有未登记旁路 |
| Recompile | 新 DerivationRunId 和不可变 Output Identity；检查当前 Policy/Fence；链接原 Intent/Run。是否为 Child Attempt 或单独登记的 Child Work 仍为 OPEN-D-RECOMPILE-01 | 永远不得绕过 Source Ancestry 或先前 Fence |
| Terminal Disposition | 持久化“不再发布”声明，并协调所有 Output/Dependency/Publication Outcome | 只有 D 接受 Terminal Evidence 后才关闭 Barrier Item |

Attempt Identity 不可变且只追加。Retry/Recovery 不复用 AttemptId；Lease Renewal 不创建新逻辑 Work Item。WorkItem Identity 不从 Payload 文本重新计算，也不能删除来隐藏卡住的 Item。

### C. Terminal Disposition 词汇

E 可以向 D 提交以下明确 Terminal Disposition 和 Evidence：
- PUBLISHED_ALL_OUTPUTS：每个 Output 都有 Durable Dependency Receipt 和 PublicationReceipt；没有未核算 Staged Output。
- CANONICAL_COMMITTED：D CanonicalCommitReceipt 已为指定 Canonical Operation 持久解析；不意味着派生 Projection 已发布。
- CANCELLED_NO_OUTPUT：取消已持久化，且没有 Output 已产生或仍可能产生。
- SUPPRESSED_NO_PUBLICATION：Fence/Authorization Denial 已持久化；Staged Output 已隔离/不可见，所有 Publication Attempt 均被禁用。
- REJECTED_PERMANENT：Policy/Schema/Source 拒绝已终结，不再存在启用的 Replay 路径。
- FAILED_PARKED：只要仍可能 Replay/Recovery 就不是 Terminal；仅作为非终态 DLQ 状态。

Terminal Assertion 必须包含 ProducerWorkItemId、Registration Receipt、Terminal Disposition、所有 DerivationRunId/AttemptId、Output Inventory Digest、Dependency/Publication/Canonical Receipt 引用、最新观察 Fence/Permission Decision Ref、Timestamp、Reason 和 Evidence Digest。D 拥有 Terminal Evidence 的接受权。E 不能只凭本地状态关闭 D Barrier Item。

### D. 崩溃/恢复不变量

1. Dispatch 前恢复 Accepted/CompileIntent/Outbox；不得从本地 Queue Row 推断 D Registration 已成功。
2. RegisterProducerWork ACK 丢失时，按 ProducerWorkItemId + Request Digest 查询；结果未知期间不得 Lease/Execute。
3. Dependency Registration ACK 丢失时，按相同 DependencyRegistrationId + Digest 查询；Staged Artifact 保持 Private。
4. Publication ACK 丢失时，按相同 PublicationOperationId 查询；证明 Commit 成功前不得暴露。
5. D Registration 后进程崩溃时，从 Durable Intent + D Receipt 重建 Work；保留相同 Work Identity。
6. Worker 崩溃时，过期/撤销 Lease；只有当前 Auth/Fence 检查通过后才创建新 AttemptId。
7. Restore 时，在任何 Staged Artifact/Replay 可查询之前协调当前 D Fence 和 I PermissionEpoch。
8. Outbox/DLQ Replay 是 At-least-once；依靠稳定 Identity/Idempotency，而不是假设 Queue Exactly-once。

### E. E 之外 Owner 的 OPEN 项

- OPEN-D-CLASS-01：D ProducerClass Registration、Class Disable/Revocation 和 Class Registry Version 的 Operation/Schema/顺序。
- OPEN-D-REG-02：RegisterProducerWork 准确 Request/Response、High-water Token、Duplicate/Conflict Error，以及与 InstallForgetFence 的串行化。
- OPEN-D-RECOMPILE-01：Recompile 是 Child Work Registration，还是链接原 Lineage 的新 ProducerWorkItemId。
- OPEN-D-TERMINAL-01：D 接受的 Terminal Disposition Schema 和 Evidence Validation Rule。
- OPEN-I-AUTH-01：已认证 ProducerIdentity/ActorRef/ScopeRef Binding 仍需 B/I/H 协议；B Fact/Claim 仍 ADR-BLOCKED。
- OPEN-STORAGE-01：Durable Lease、Staging、Outbox、Dependency 和 Visibility Transaction 实现尚未选型/测试。

## Phase 3.5 补充 — D Registry 与 Barrier Snapshot 消费

E 的 ProducerClass Registration 不只是本地配置。在接纳可产生派生物的 Work 之前，E 必须持有 D ProducerClassRegistrationReceipt，证明该 Class 在已提交 ProducerRegistryVersion 下为 ENABLED。本地 Allow-list 不能替代 D 的封闭世界 Registry。禁用 Class 会阻止新 Work，但不会删除或终结既有 Work。

D 的 ProducerWork RegistrationReceipt 包含 ProducerRegistrationSequence 和 ProducerRegistryVersion。Sequence/High-water 属于 Producer Ledger Namespace，不是 CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor 或 ForgetFenceGeneration。E 必须原样保存，并仅按 D 的语义使用。

D InstallForgetFence 在 Fence 生效的同一个持久化线性化点捕获 ProducerRegistryVersion 和 ProducerRegistrationHighWater。CaptureProducerRegistrationHighWater 返回与该 Installation 绑定的不可变 BarrierSnapshotReceipt；它是验证/读取操作，不是第二个或可移动的 Cutoff。

E Recovery 使用原始 ProducerWorkItemId 和 Registration Digest 调用 D ResolveProducerWork。D ReconcileForgetBarrier 是 D 对不可变 Barrier/Dependency/Target Checkpoint 的权威本地汇总。E 提供 Receipt 和 Terminal Evidence，但不能自行断言 DRAINED 或 Global Completion。

D 的规范 Operation 集还包括 RegisterProducerClass、CaptureProducerRegistrationHighWater、ResolveProducerWork 和 ReconcileForgetBarrier，以及 RegisterProducerWork、InstallForgetFence、RegisterDerivedDependency、PublishDerivedIfFenceCurrent 和 CompleteProducerWork。精确 D 语义操作由 D 的 Operation-level Specification 定义；API Transport Schema 仍为 OPEN。

## Phase 3.5 补充 — Producer Admission OPEN 项修正

D 当前 Operation-level Specification 已定义 ProducerClass/ProducerWork Registration 的输入、输出、幂等、语义错误和线性化，也定义 InstallForgetFence 捕获 ProducerRegistryVersion + ProducerRegistrationHighWater、CaptureProducerRegistrationHighWater 不可变 Snapshot Receipt、ResolveProducerWork 和 ReconcileForgetBarrier。因此，任何暗示 D 尚未定义这些语义元素的旧 OPEN 表述都已被 SUPERSEDED。

剩余 OPEN 工作仅包括：
- 可调用 API/Transport Schema 和已认证 B/I/H Identity Serialization；
- D 本地 ProducerClass Registry 与 I/A Producer/Recipient Inventory 的全局完整性协调；
- E 明确 Recompile Child/Re-admission Identity Rule；
- Storage/Consistency 实现 Owner 的指定，以及共享 Serialization/Visibility Boundary；
- 可执行 Crash/Race/Fault 测试和证据留存。

E 必须原样消费 D 的语义字段。特别是 ProducerRegistrationSequence 是 Barrier Inclusion 的排序位置；ProducerRegistryVersion 标识 Class Registry Snapshot。两者都不是 CanonicalCommitCursor 或 ForgetFenceGeneration。

## Phase 3.5 重新验证 — Producer Lifecycle 与 D 语义消费

本节取代可能暗示 D 尚未定义语义 Operation 输入/输出、幂等、错误或线性化的旧措辞。D 的权威语义来源是 `03-memory-brain/forget-fence-operation-and-publication-gate.md`；Cursor 权威来源是 `commit-cursor-semantics.md`。E 消费这些语义，不得自行发明可调用 API 或 Wire Schema。

| Lifecycle 元素 | Identity/State | E 必需行为与 D Barrier 影响 |
|---|---|---|
| ProducerClass Registration | 稳定 ProducerClassId + Contract Version；D Registry Status | 与 WorkItem Registration 分离。只有 D 确认 ENABLED Class 才可接纳 Work。Unknown/Disabled/Registry 不完整时 Fail-closed。 |
| WorkItem Registration | 稳定 ProducerWorkItemId + Request Digest + D RegistrationReceipt | Enqueue/Lease/Protected Dereference/Execution 前持久化登记。相同 ID/Digest 返回相同 Receipt；不同 Digest 冲突。 |
| Lease Acquire/Renew | LeaseId + 单调 Lease Epoch/Expiry | 条件式当前 Owner Lease；重新验证 Identity、PermissionEpoch 和 ForgetFence。Lease 不是新的 Admission Authority。 |
| Lease Expiry | Attempt/Lease 已过期；WorkItem 仍开放 | 只使该 Attempt 失效；绝不 Terminal，也不关闭 Barrier。 |
| Attempt Identity | 每次 Execution Attempt 使用新的 AttemptId | 追加式审计身份；不能替代 WorkItemId。 |
| Retry | 相同 WorkItemId；新的 AttemptId | 复用 D Registration；重新检查当前 Authorization/Fence。Retry 不创建第二条逻辑 Registration。 |
| DLQ | 相同 WorkItemId/Lineage，持久化失败原因 | 只要仍可能 Replay/Publication，就保持 Barrier-open。Park/Delete Queue Entry 不构成 Terminal。 |
| Replay | 相同 WorkItemId、新 AttemptId、原始 Source/Receipt Ref | 重新认证/授权；在 Dereference、Staging、Dependency Registration 和 Publication 前重新检查 Fence。 |
| Recompile | 新 DerivationRunId，链接原始 Source/Intent | D 要求明确的 Linked Child/Re-admission 决策。是否需要独立 Child ProducerWorkItemId 仍为 OPEN-RECOMPILE-01。 |
| Terminal Disposition | D ProducerWorkTerminalReceipt + 全部 Output/Attempt Evidence | 只有每个 Output 都有 Publication Receipt，或已 Suppressed/Quarantined 且不存在后续发布可能时，才可 CompleteProducerWork。 |

正常路径：`REGISTERED → QUEUED → LEASED → RUNNING → STAGED → DEPENDENCY_REGISTERED → PUBLISH_PENDING → PUBLISHED`。Retry 在相同 WorkItemId 下以新 AttemptId 返回 QUEUED。DLQ/Lease Expiry 都不是终态。Suppression/Quarantine Terminal Path 必须具有持久化证据，证明未来不可能再发布。

**D 已 DECIDED：** ProducerClass/WorkItem 区分；RegisterProducerWork/InstallForgetFence 共享排序；不可变 ProducerRegistryVersion + ProducerRegistrationHighWater；Dependency 在 Visibility 前持久化；最终 Publish Linearization；Terminal/Reconciliation Receipt。**OPEN：** 可调用 Transport/API 和 Wire Error；H/B/I Identity Serialization；I PermissionEpoch 当前决策绑定；I 全局 Inventory Reconciliation；准确 Recompile Child Identity；指定 Storage Owner 和已验证原子实现；可执行一致性测试。本文不声称任何 Endpoint/Implementation 已存在或通过。

## Phase 3.6 — 由 Fence 强制执行的 Producer Work 协议

**状态：** E Producer Execution 契约已定义；消费 D 语义操作；Storage 串行化/可见性实现和 D/Storage Owner 确认仍为 OPEN。**实现 NOT VERIFIED。**

### 1. 稳定 Work Identity 与 Attempt 模型

逻辑 Producer Work Identity 在整个恢复/重新处理生命周期中不可变：

- **ProducerClass：** 由 D 登记、带版本且启用的 Producer Capability Class。E 的 Compiler Ingress、Extraction/Normalization、Consolidation、Retry Scheduler、DLQ Replay、Worker Recovery、Outbox Dispatcher、Rebuild/Recompile Initiator，按 D/I Inventory Policy 声明为独立能力。本地 E Allow-list 不是 Admission Authority。
- **WorkItemId / ProducerWorkItemId：** 一个逻辑 Source-to-Derived Work 义务的稳定身份。在 Dispatch 前创建并持久化。Retry、DLQ、Replay、Recompile、Outbox Replay、Lease Expiry、Worker Recovery 和进程重启期间保持不变。同一 ID 搭配不同语义请求必须 Conflict；新的 AttemptId/DerivationRunId 绝不创建新的 WorkItemId。
- **AttemptId：** 单次执行尝试的不可变身份；每次 Retry/Replay/Recovery 都创建新的 AttemptId。
- **DerivationRunId：** 一次 Extraction/Normalization/Consolidation Run 的不可变身份。Recompile 创建新的 Run，并链接原 WorkItemId、已接收来源和 Lineage；它不创建替代 WorkItemId。D 要求的任何 Child/Re-admission Operation 都必须保留 Root WorkItemId 作为 Barrier Identity，并在 Dispatch 前由 D 明确确认。
- **RegistrationReceipt：** E 分别保存 D 签发的 ProducerClassRegistrationReceipt 和 ProducerRegistrationReceipt。后者绑定 WorkItemId、Canonical Request Digest、ProducerClass/Registry Version、Source Lineage、ScopeRefs、Admission Disposition 和 ProducerRegistrationSequence。它不是 AcceptedReceipt、Lease 或 Publish Permit。
- **Lease：** 有时限的 Worker Claim，绑定 WorkItemId、AttemptId、Worker Identity、LeaseId、Lease Epoch/Expiry、Observed ForgetFenceCursor 和 PermissionEpoch。Lease Acquire/Renew 必须是条件式且持久化。Lease 永远不是 Admission Authority；Expiry 只使该 Attempt 失效。
- **Source MemoryVersion：** 若存在 Canonical Memory，使用准确不可变 Source MemoryRef + MemoryVersionRef/Revision；Event-only Ingress 则保留 EventRef + 不可变 Payload Digest。每次 Recompile/Derivative-of-Derivative 都保留完整 Source Ancestry 和 Lineage Digest。
- **ScopeRef：** 类型化、已验证的 Scope Binding 和 Security Domain Ref。ScopeRef 不等于 Permission，Payload 声明不等于 Credential。
- **FenceGeneration / ForgetFenceCursor：** D 签发的类型化 Fence Generation/Cursor Tuple。E 原样保存，绝不与 PermissionEpoch 或其他 Cursor 做数值比较。
- **PermissionEpoch：** I 签发的不透明授权新鲜度值，带 Authorization Decision Ref。E 必须通过 I 重新验证；它本身不是 Grant。
- **Dependency Registration：** 稳定 DependencyRegistrationId + Canonical Digest，以及 D 签发的 DependencyRegistrationReceipt；该 Receipt 覆盖完整 Artifact/Version 和全部直接/传递 Source/Parent Edge。相同 ID/Digest 解析为原 Receipt；Digest 变化产生 Conflict。
- **Terminal Disposition：** 持久化、追加式的最终 Work 结果，通过 D CompleteProducerWork 提交，并且只有 D 返回 ProducerWorkTerminalReceipt 才被接受。E 本地完成不等于 D Barrier 关闭。

### 2. Admission 与 Execution 顺序

必需顺序如下：

1. 在 E 的 Durable Acceptance/Outbox 边界持久化不可变 Ingress/CompileIntent 和稳定 WorkItemId。
2. 解析已启用的 D ProducerClass Registration，以及当前已认证 Producer/Scope Binding。
3. 使用 WorkItemId + Canonical Request Digest 和准确 Source Lineage 调用 D RegisterProducerWork；任何 Timeout 都使用相同 Key 解析。
4. 只有确认收到持久化 ACCEPTED RegistrationReceipt 后才能 Dispatch/Queue。REJECTED、QUARANTINED、CLEANUP_ONLY、UNKNOWN、缺少 Receipt 或 Registry Gap 都不能进入普通 Compile Execution。
5. 在当前 I Authorization 和 D Fence 状态下获取新的 LeaseId/AttemptId。只有此后才允许解引用受保护 Source/Evidence/Provenance。
6. 在 Private Staging 中执行 Extraction、Normalization 和 Consolidation。记录 Source MemoryVersion、ScopeRef、FenceGeneration Observation、PermissionEpoch Observation 和 Provenance Digest。
7. 向 D 登记完整 Derived Dependency Set。部分/未知 Dependency Registration 必须保持 Private。
8. 调用最终 PublishDerivedIfFenceCurrent Operation；决定 Publication 的是最终 Visibility Commit，而不是之前的预检查。
9. 解析权威 PublicationReceipt，再向 D 提交 Terminal Evidence。只有所有 Output/Attempt/Replay Path 都协调完成后，Work 才算 Terminal。

任何 E Queue Insert、Lease、Source Dereference、Execution、Retry、DLQ Replay、Recompile、Rebuild 触发的 Compiler Work 或 Publication 都不得绕过 D Registration 和当前 Authorization/Fence 检查。

### 3. Lease、Retry 与 Terminal 规则

- Lease Renewal 保留 WorkItemId、AttemptId 和 LeaseId；只有在当前 Authorization/Fence 检查通过后才推进 Lease Epoch/Expiry。
- Lease Expiry 撤销旧 Lease/Attempt 的 Publication 能力。Recovery 保留 WorkItemId 和 Lineage，创建新的 AttemptId/LeaseId，并在访问 Source 前重新解析 D Work State、当前 I PermissionEpoch 和 D ForgetFence。
- Retry 和 DLQ Parking 不关闭 D Barrier Membership。只要仍可能 Replay/Publication，DLQ 就不是 Terminal。
- DLQ Replay/Outbox Replay 使用相同 WorkItemId、CompileIntentId、Source EventRef/MemoryVersion 和 Request Digest；创建新的 AttemptId/Lease，再重新检查全部当前控制。
- Recompile 使用相同 WorkItemId 和原始 Source Lineage、新 DerivationRunId，以及不可变的新 Output Artifact/Version ID。不得创建新的 AcceptedReceipt，也不得使用新的 WorkItemId 逃避旧 Fence。D 必须明确确认任何 Child Registration 表示法，并保留 Root Barrier Identity。
- 只有在所有 Attempt 均已撤销/过期、所有 Output 均已带 Receipt 发布或被抑制/隔离、没有 Dependency/Publication UNKNOWN、没有 Outbox/DLQ/Replay Dispatch 路径，且 D 接受 CompleteProducerWork 后，才允许 Terminal Disposition。FAILED_PARKED 不是 Terminal。
- 旧 Worker 不得在新 Attempt/Lease 接管后发布或终结 Work。D Final Gate 必须校验活动 Attempt/Lease；Storage 必须将该校验与 Visibility 串行化。

### 4. 类型化状态转换

`RECEIVED -> DURABLE_INGESTION -> ACCEPTED -> D_REGISTRATION_PENDING -> REGISTERED -> QUEUED -> LEASED -> RUNNING -> CANDIDATE_PRIVATE -> STAGED_PRIVATE -> DEPENDENCY_REGISTRATION_PENDING -> DEPENDENCY_REGISTERED -> PUBLISH_PENDING -> PUBLISHED -> TERMINAL`

替代转换：
- 任一 D Operation 结果不明确：`*_PENDING -> UNKNOWN_RECONCILIATION`；在相同 Operation Identity 解析前，不得推进、Dispatch 或暴露。
- Retry/Worker Recovery：`RUNNING/STAGED/UNKNOWN -> RETRY_QUEUED`；同一 WorkItemId、新 AttemptId/LeaseId，并重新授权/检查 Fence。
- DLQ：`RETRY_QUEUED -> DLQ_PARKED`；仍已登记且 Barrier-open。
- Recompile：在相同 WorkItemId 下使用新 DerivationRunId；旧 Run/Output Evidence 保持不可变并关联。
- Fence/Permission Denial：`*_PRIVATE -> SUPPRESSED_QUARANTINED`；禁用 Publication；只有持久化“不可能再发布”证明且 D 接受后才可 Terminal。
- 任一部分 Dependency Registration 或不明确 Publication：保持 Private 和未解决状态。

### 5. E/D 证据分离

E 的本地状态（Queued、Leased、Running、Candidate、Staged、Retry、DLQ）是 Execution Telemetry。D 的 RegistrationReceipt、DependencyRegistrationReceipt、PublicationReceipt 和 ProducerWorkTerminalReceipt 才是权威 Ledger Evidence。本地 Row、Queue ACK、Object Store 存在、Lease Heartbeat 或 Worker Success Log 都不能替代 D Receipt。

D Producer Registration Sequence/High-water、D ForgetFenceGeneration、D CanonicalCommitCursor 和 I PermissionEpoch 属于不同类型化 Namespace。E 必须分别存入各自类型字段，并将 Currentness/Coverage 评估交给签发方。
