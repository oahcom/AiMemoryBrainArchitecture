# E Forget Fence 与 Derived Registration — 第 1 部分：核心契约

- 文档 ID：E-FORGET-DERIVED-001-P1
- 源文件版本：DEREFERENCED — 保留历史源 Blob `00e37ba56596e710513c8d0568acd79141d9101b`；当前仓库不存在可解析的规范性源文件。
- 源分支：session-e-memory-compiler-2026-11-16
- 对应英文：[Part 1 — Core Contract](../../en/04-memory-compiler/forget-fence-and-derived-registration-part1.md)
- 源规范：DEREFERENCED — 原规范源路径 `04-memory-compiler/forget-fence-and-derived-registration-part1.md` 在当前 main tree 中不存在；替代物：[英文对照版](../../en/04-memory-compiler/forget-fence-and-derived-registration-part1.md)（Blob `6bb639cb242665cf3f6d3f4816e3d24deac51fb0`；仅为对照文本，不是规范性替代源）。

## 1. 安全不变量

在以下条件全部满足前，Compiler 产生的 Artifact、Provenance Edge、Proposal、Embedding、Excerpt、Cache Item、Outbox Payload 或其他派生物，都不得被 Runtime、Canonical Reader、Retrieval、Context、Adapter 或任何其他 Consumer 使用：

(a) 其 Source Lineage 已持久登记到 D Dependency Inventory；  
(b) 当前 Authorization/PermissionEpoch 和 D ForgetFence 检查通过；  
(c) 权威 Final Publication Gate 已持久 Commit。

Staged Artifact 必须 Private 且不可查询。Queue Membership、Accepted Receipt、Compiler Completion、本地 Provenance 持久化、D Registration Receipt 或本地 Precheck，都不构成暴露许可。

任何检查、Registration、Gate Result 或必需 Authority 不可用/有歧义时，都必须保持 Non-visible 并 Fail-closed。Logical Suppression、Asynchronous Cleanup 和 Physical Erasure 仍是不同概念；E 无权宣布 Global Forget Completion 或 Physical Deletion。

## 2. 消费的 D 契约（当前分支版本）

来源读取：session-d-memory-brain-2026-11-16@30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6。

| D-owned 契约 | D 当前语义决议 | E 的消费/边界 |
|---|---|---|
| ForgetOperation Identity | 持久化 Operation ID；幂等 Request Key + 规范化 Digest；准确 Typed Target 和 Target Set Digest | E 保存/传播 D 签发的 Operation/Fence Ref；不得自行发明 Forget ID 或目标匹配 |
| ForgetFenceCursor | (forget_operation_id, fence_generation, target_set_digest)；单调 D Generation，独立于 Commit Cursor/Permission Epoch | 每个 Worker/Attempt 记录观察到的 Typed Fence；受保护读取和最终 Visibility Boundary 刷新最新适用 Fence |
| Producer Registry | 封闭世界 Producer Class/Registration Ledger；每个 Work Item 执行前都必须登记稳定 Producer/Work ID、Class、Source Ref/Revision、Scope、Operation/Correlation ID、Admission CanonicalCommitCursor、Observed Fence 和 Lease/Attempt Identity | E 在 Queue/Lease/Run 前登记；Queue Insert 不等于 Admission；Registration Outcome 未知时按稳定 Work ID 查询，不能假定成功 |
| Producer Barrier | Fence Installation 原子捕获 Producer Registration High-water；所有 Fence 前登记的 Work 必须达到持久化 Terminal Disposition | E 在 Retry、DLQ、Replay 和迟到结果处理中保持 Registration 开放；Lease 过期或 Queue 删除都不能使 Item 消失 |
| Fence 后 Admission | 引用已 Fence Target/Lineage 的新 Work 被拒绝、隔离，或仅作为 Suppression/Cleanup Work 接纳 | Requeue/Recompile 不能通过新 Attempt 或当前 Generation 获得合法性；D 重新评估 Source Ancestry |
| Register-before-visible | Derivative Record + Dependency Edge 原子提交，或使用等价 Durable Prepare/Commit；最终 Gate 在 Visibility 前重新检查最新 Fence | E 先持久化 Private Staged Output，登记所有 Dependency，再请求 Final Gate；禁止本地 Check-then-publish |
| Target ACK | 针对具体 Target 的 Suppression/Cleanup/Unknown/Exception Evidence；Unknown 不等于成功 | E 只报告 E Producer/Job/Derivative 范围；D/I 拥有汇总和 Global Completion |
| Canonical Commit Cursor | 每个 Canonical Memory Authority 一个全局 Sequence；AggregateRevision 和 Per-Memory LifecycleEventCursor 独立 | E 原样保存 D 返回的 CanonicalCommitCursor，并分别保存 Aggregate/Lifecycle 引用 |
| Transaction Visibility | Canonical Write、Aggregate Head CAS、LifecycleEvent Append、CanonicalCommit Record 和 Outbox Intent 在同一个原子/可恢复 D Transaction 中；Cursor 只在持久化 Commit 后可见 | E 不伪造 Commit Evidence/Cursor；结果未知时按稳定 Operation Key 查询 |

**重要精确性：** D 定义的是语义义务，不是已存在的可调用 API 名称、Request/Response Schema 或已证明的 Storage 实现。以下 E 侧名称只表示必需 Operation 语义，不表示 D API 已经存在。

## 3. Compiler Work Item 身份与生命周期

### 3.1 稳定身份

- EventRef：不可变 Accepted Source Event Identity；Payload 修正必须是新 Event/Correction Link，不能原地修改。
- AcceptedReceiptId：E 的可靠接收证据。
- CompileIntentId：与 Acceptance 一起创建的稳定逻辑处理意图。
- ProducerWorkItemId：D 登记的一个逻辑派生 Work Item 的稳定身份。它不是 Attempt ID，Retry 不重新创建。
- DerivationRunId：一次执行/派生血缘；Recompile 创建新 Run，并链接原 Event/Intent 和前序 Run，同时受当前 Policy 约束。
- AttemptId 和 LeaseId：每次执行 Attempt/Lease 唯一。Retry 保留 ProducerWorkItemId，并创建新的 AttemptId/LeaseId。
- DerivedArtifactRef：一个 Staged Derivative 的稳定身份；派生输出变化时创建新的不可变 Artifact/Version，不能覆盖。
- DependencyRegistrationId 和 PublicationOperationId：Registration/Publication 协调的稳定幂等身份。

建议在 Acceptance/CompileIntent 创建时分配并持久化不透明 Work Identity，而不是从 Payload 文本重新计算 Hash。每次 Retry/Recovery 都必须向 D 提交相同 ProducerWorkItemId。

### 3.2 状态机

| 状态 | Owner / 含义 | D Barrier 可见性 |
|---|---|---|
| Accepted | E：Event + Payload Ref + Idempotency Receipt + CompileIntent 已持久提交 | 尚未 Admission；不允许执行 |
| Registered | D 已持久接受 ProducerWorkItem Registration，并返回/可查询 Registration Receipt | **是**；纳入 D Registration Ledger/High-water |
| Queued | E：已登记 Intent 等待 Dispatch | D Registration 仍开放 |
| Leased | E：取得 Attempt/Lease；包含 Observed PermissionEpoch 和 ForgetFenceCursor | D 必须能把 Lease/Attempt Identity 关联到已登记 Work |
| Running | E：正在执行受保护读取/Extraction/Consolidation | D Registration 仍开放 |
| Staged | E/Storage：不可变输出保存在 Private Staging；不可查询、不可发布 | D Registration 仍开放 |
| DependencyRegistered | 每个必需 Source/Transitive Dependency 都有持久 D Registration Receipt；部分集合不可 Publish | D Dependency Inventory 已反映所有 Dependency |
| Published | Final Publication Gate 成功；Publication Receipt 持久化，Artifact Visibility 原子切换 | 只有 Gate Evidence 后，D 才看到成功 Terminal Disposition |
| CanonicalCommitted | 独立 D Evidence 确认 Canonical Write；包含 CanonicalCommitCursor + 准确 Aggregate Revision Ref | D Canonical Transaction 是权威；不由 Published 推断 |
| Retry | E：针对相同 Work/Lineage 安排 Retry，使用新 AttemptId；重新检查当前 Auth/Fence | Registration 仍开放；Retry 不是新 Admission 绕过 |
| DeadLettered | E：达到 Retry Budget/永久错误后停放；仍可能 Replay | **不是 Terminal**；Replay/Publication 仍可能时 Barrier 保持开放 |
| Cancelled / Rejected | 持久化 Terminal Disposition；不可能 Publication；记录取消/抑制原因 | D 收到 Terminal Evidence |
| Terminal | E 声明 Work 不可能再次 Publish；所有 Output 已 Publish/Canonical-committed，或 Suppressed/Rejected 并完成协调 | 只有 D 收到持久化 Terminal ACK 后，才可计入 Barrier |

Published 与 CanonicalCommitted 是独立 Evidence 维度：派生物可以 Published，但不是 Canonical Memory；Canonical Commit 也不代表派生 Projection/Index 已 Published。适用时一个 Work Item 可以同时具有两种结果。DeadLettered 是停放状态，不会自动完成 Barrier。Lease Expiry 不是 Terminal。

### 3.3 D 可观察状态与 E 内部状态

D 必须观察：Producer Class；稳定 ProducerWorkItemId；Source Ref 和适用时的准确 Version/Revision；ScopeRefs；Operation/Correlation/Causation Ref；Admission CanonicalCommitCursor；Observed ForgetFenceCursor；Attempt/Lease Identity；持久 Registration Receipt/High-water Position；Dependency Registration Evidence；Terminal Disposition 和 Evidence。

E 内部管理：Accepted、Queued、Running、Staged、Retry Schedule、DLQ Residence、Worker Health 和 Stage Checkpoint。E 可以把这些作为进度遥测暴露，但它们不能替代 D Barrier Ledger。如果 D Ledger 能可靠地将已 Admission Work 保持为 Open，直到收到显式 Terminal ACK，则 D 不必镜像每个 E 内部子状态。

即使 Queue Row、Worker Process 或 Lease 消失，Fence 前 Registration 仍留在 Barrier 中。只有每个 Pre-barrier Registration 都 Terminal，且它产生的每个 Derivative 在可见前均已登记，D Barrier 才能关闭。

## 4. Register-before-visible 协议

以下是必需语义顺序。等宽字体中的名称是 E 侧 Operation Intent，不是现存 D API 声明。

1. **Durable Ingress：** 原子持久化不可变 EventRef/Payload Ref/Digest、AcceptedReceipt、Idempotency Row 和 CompileIntent/Outbox，或使用已证明可恢复的 WAL。只有 Durable Commit 后才能返回 Accepted。
2. **Stable Work Identity：** 分配 ProducerWorkItemId，并与 CompileIntent、Source EventRef、Source Lineage 和 Idempotency Context 一起持久化。
3. **D Producer Admission：** 在 Enqueue、Lease、受保护 Payload Dereference 或 Execution 之前向 D 登记 Work。必需字段见 §7。等待持久 Registration Receipt。响应丢失时用相同 Work ID/Digest 查询/重试。无 Receipt 不执行。
4. **Queue and Execute：** 只有 Registered Item 可以 Queued/Leased/Running。每个 Attempt 在 Payload/Source Access 前及每个受保护边界重新验证已认证 ProducerIdentity、当前 Authorization/PermissionEpoch、Scope Binding 和最新适用 ForgetFence。
5. **Private Staging：** 在 Private Staging Namespace 写入不可变 DerivedArtifactRef 和 Provenance。Runtime、Search、Canonical Reader 和下游 Consumer 不得枚举/读取 Staged Row。Object Store ACL/Metadata 默认必须拒绝 Consumer。
6. **Dependency Registration：** 持久化完整直接/传递 Lineage；向 D Dependency Inventory 登记每个 Dependency。等待 D 持久化 Registration Receipt。部分 Registration、Timeout 或 Receipt Unknown 都使 Artifact 保持不可见。
7. **Final Authorization/Fence Check：** 针对所有 Source Ancestor、Target Ref 和 ScopeRef，刷新当前 I PermissionEpoch 和最新 D ForgetFenceCursor。Admission 时缓存值不足以授权。
8. **Final Publication Gate：** 提交准确 Artifact/Version、Work/Run/Attempt/Lease ID、全部 Dependency Receipt ID、Request Digest、当前 PermissionEpoch、Observed ForgetFenceCursor 和 Publication Operation Key。D 必须将 Gate Acceptance 与 Fence Installation 原子/线性化排序，并证明 Registration 已持久化。
9. **Atomic Visibility：** 只有持久化成功 Publication Receipt 后，Storage 才能将 Artifact 从 Private Staged 切换为 Visible。Gate 和 Storage Visibility Transition 必须共享一个 Transaction/Linearizable Commit Protocol；否则必须使用可恢复 Prepare/Commit Protocol，保证崩溃和结果不确定时 Artifact 仍隐藏，直到协调完成。
10. **Terminal Acknowledgement：** E 记录 Published/CanonicalCommitted Outcome，并且只有当该 Work Item 不可能再产生任何 Publication 时，才向 D 提交 Durable Terminal Disposition。

本地读取 Fence 后再执行独立 Storage Write 明确不安全。如果 Final Gate 不能绑定 Visibility Transition，E 不得 Publish。

## 5. 故障、幂等与崩溃恢复

| 故障/竞争 | E 必需行为 |
|---|---|
| D Admission 不可用/Unknown | 不得 Enqueue/Execute。使用 ProducerWorkItemId + Request Digest Resolve；绝不假定已 Admission |
| D Commit 后 Admission ACK 丢失 | 查询相同 Work ID；接受相同 D Registration Receipt；不创建第二条逻辑 Registration |
| Registration 后、Queue 前 Crash | D Ledger 保持 Open；Recovery 扫描已登记的非 Terminal Work，并用相同 Work ID 重新 Enqueue |
| 重复 Event/Message | 相同认证 Idempotency Namespace + 相同 Digest 返回原 Event/Receipt/CompileIntent/WorkItem；不产生第二次效果 |
| 相同 Idempotency Key、不同 Digest | Conflict；保留原 Receipt；不创建 Work |
| Worker Crash / Lease Expiry | Lease 过期但 Work 仍在 D 中登记/Open；用新 AttemptId Recovery，并在任何受保护读取前重新检查当前 Auth/Fence |
| Staging 后 Crash | Staged Output 保持 Private；继续操作前协调 Dependency Receipt 和当前 Fence |
| Dependency Registration 部分完成 | 保持不可见；幂等重试缺失 Registration；不得发布部分 Dependency Set |
| Registration ACK 丢失 | 用稳定 DependencyRegistrationId/Derived Ref + Digest 查询；不得重复 Edge 或假定成功 |
| Gate 因 Fence/Permission Epoch 推进而拒绝 | Suppress/Quarantine Staged Output；不得刷新 Generation 后把同一旧 Work 当作新授权重试 |
| Gate ACK 丢失 | 保持 Output 隐藏；查询 PublicationOperationId。只有权威证明 Commit 成功后才可暴露 |
| Gate Commit 后、E 记录 Receipt 前 Crash | 查询相同 PublicationOperationId；记录原 Publication Receipt；绝不发起不同 Publication Key |
| DLQ/Replay | DLQ 保留 EventRef、CompileIntentId、ProducerWorkItemId、Lineage 和最后安全 Checkpoint。Replay 创建新 Attempt，而不是新 Authority；重新授权/检查 Fence |
| Recompile | 新 DerivationRunId 和 Provenance Version，链接原 Source Lineage；按 D 要求执行新的 Admission/Registration；若任何 Ancestor 已 Fence 或 Retention 不允许则禁止 |
| Lease Loss/Cancel/Fence 后的迟到结果 | 丢弃，或仅保留 Policy 允许的 Private Diagnostic Metadata；绝不 Publish；D Terminal State 仍为权威 |
| Permission 撤销 | 停止受保护读取/写入；使 Lease 失效；除非 I 授权准确 Operation，否则不得新的 Stage Commit、Dependency Registration 或 Publication |
| ForgetFence 推进 | 任意旧 Lease/Attempt 均陈旧；抑制 Output 并 Terminal ACK；不得把旧 Work Rebase 到最新 Fence |
| Restore/Rebuild | 让恢复的 Staging/Derivative 可查询前，先重新应用当前 ForgetFence 和 Authorization；旧 Queue Snapshot 不具备 Authority |

每次 Retry、Replay、DLQ Requeue 和 Recompile 都复用或链接原 Source Identity，并且必须通过新鲜授权/Fence 检查。Queue Transition 不产生 Permission。较新的 Fence Generation 不能替代 Source Eligibility。

## 6. Cursor 与 Receipt 分离

| 类型 | Owner / Namespace | E 的用法 | 绝不能替代 |
|---|---|---|---|
| SourceEventCursor | E；一个声明的 Ingress Partition | Durable Source Acceptance Position；Replay/Resume | CanonicalCommitCursor、AggregateRevision、IndexWatermark |
| CanonicalCommitCursor | D；每个 Brain Authority 一个全局有序序列 | 保存 D 返回的准确 Cursor，用于 Canonical Commit/As-of Ref | Source Offset、AggregateRevision、LifecycleEventCursor、IndexWatermark |
| AggregateRevision | D；每个 Aggregate | 保存准确不可变 Memory/Entity/Relation Revision Identity/Sequence | Global Canonical Cursor |
| LifecycleEventCursor | D；每个 Memory Lifecycle Stream | 保存准确 Lifecycle Event Position，并单独保存所属 Canonical Cursor | CanonicalCommitCursor 或 AggregateRevision |
| IndexWatermark | F；Index/Channel/Partition，applied-through CanonicalCommitCursor | 只消费 F 的类型化 ACK | D Cursor 本身或 Forget Proof |
| ForgetFenceCursor | D；ForgetOperation + Target-set Digest + Generation | 作为 Fence 观察；仅在 D 定义的 Fence Namespace 内比较 | 任何 Cursor、PermissionEpoch |
| PermissionEpoch | I；定义的 Principal/Security Policy Namespace | 在受保护边界重新验证当前授权 | ForgetFenceCursor 或 Commit Cursor |
| ContextVersion | G；单个 Context | 仅作为下游 Context Version | 任何 E/D Cursor |
| Delivery/Adapter ID | G/H | 在关联时不透明传递 | Canonical 或 Source Cursor |

只有对应 Event 确实发生时，E Receipt/Provenance 才能携带该类型字段。CandidateProposition/ExtractionIR 不得携带伪造的 CanonicalCommitCursor。只有 D 确认 Commit 后才记录 Canonical Commit Receipt。E 不定义或推进 F IndexWatermark。

## 7. D/E/Storage 原子边界 — 明确 OPEN 的接口

D 当前契约定义语义要求，但**没有**发布以下内容的可调用 API 名称、完整 Request/Response Schema、Transaction Ownership 或故障/恢复语义。这里的 E 侧名称只是要求，不代表实现已存在。

| 必需 Operation 语义 | 必需输入/输出 Evidence | 原子/线性化要求 | 当前状态 |
|---|---|---|---|
| Producer Work Registration | 输入：ProducerWorkItemId、Producer Class/Identity Binding、Source EventRef + 存在时的 Canonical Ref/Revision、ScopeRefs、Operation/Correlation ID、Admission CanonicalCommitCursor、Observed ForgetFenceCursor、Permission/Policy Epoch、Request Digest、Attempt/Lease Identity。输出：Durable Registration Receipt + D Registration High-water/Epoch + Accepted/Rejected Disposition | Registration Ledger Commit 必须先于 E Queue/Lease/Execution，并与 Fence Installation 排序 | **OPEN — D Schema/API + Storage Transaction** |
| Dependency Registration | 输入：DerivedArtifactRef/Version、ProducerWorkItemId/DerivationRunId、完整 Source/Transitive Source Ref 或获批不透明 Token、准确 Source Version、ProvenanceRef、ScopeRefs、Lineage Digest、Observed Fence。输出：Durable Derived Registration Receipt、Registration ID 和 Inventory Position | Dependency Edge 和 Derivative Registration 必须在任何 Visibility 前持久化；重复 Registration 幂等 | **OPEN — D Ledger API + E/Storage Atomicity** |
| Final Publication Gate | 输入：PublicationOperationId、Artifact/Version、Work/Run/Attempt/Lease ID、全部 Dependency Receipt ID、当前 PermissionEpoch、当前 ForgetFenceCursor、Request Digest。输出：Commit/Reject 结果、Durable Publication Receipt 和权威 Fence/Registration Evidence | Gate Decision 必须与 Fence Installation 串行化，并原子控制 Storage Visibility；或使用已证明可恢复的 Prepare/Commit Protocol，在不确定时保持隐藏 | **OPEN / BLOCKING — D/E/Storage** |
| Producer Terminal ACK | 输入：ProducerWorkItemId、最终 Attempt/Lease、Terminal Disposition、全部 Output/Registration/Publication Ref、Reason 和 Digest。输出：Durable Terminal Receipt / Barrier Ledger Update | D 只有在 Durable ACK 后才把 Item 计为 Terminal；Lease Expiry/Queue Deletion 不代表 Terminal | **OPEN — D Response Schema + Reconciliation Semantics** |
| Current Fence/Permission Lookup | 输入：准确 Target/Source Ancestry 和 Scope；输出：最新适用 ForgetFenceCursor 和当前 I PermissionEpoch/Decision | Freshness/Consistency 保证必须覆盖 Final Gate；陈旧缓存值不能授权 Publication | **OPEN — D/I API Consistency 和 Epoch Lookup 语义** |

### 7.1 向 D 确认的最低接口问题

1. 哪个准确 API/Command 持久登记一个 ProducerWorkItem？在 Canonical Object 尚不存在的 EventRef-only Ingress 中，需要哪些字段/Typed Ref？
2. D Registration 覆盖逻辑 Work Item，还是分别覆盖每个 Attempt？Retry、DLQ、Lease 替换和 Recompile 如何关联，避免 Barrier Gap？
3. Receipt Identity、Registration High-water 字段/类型、Producer Registry Version 和按 Idempotency 查询的准确 Operation 是什么？
4. 哪个准确 API 持久化登记 DerivedArtifactRef 和每个 Source Dependency？E 写入最终 Artifact Row 前，D 是否要求 Prepare Token？
5. 哪个 Operation 将 ForgetFence 与 ProducerWork Registration 原子安装/推进？Admission 与 Fence Installation 竞争时的 Linearization Order 是什么？
6. 哪个准确 Final Gate Operation 接受 Dependency Receipt 和 PermissionEpoch/ForgetFenceCursor？它自己拥有 Visibility Flip，还是返回由 Storage 消费的 Token？
7. 如果 Storage 拥有 Visibility Flip，什么 Shared Transaction、Lock/CAS、Fencing Token 或 Transactional Outbox Protocol 能让 Gate Acceptance 与 Visibility 成为同一 Linearizable Event？
8. ACK 丢失、Commit 后 Timeout、重复 Receipt、部分 Dependency Registration、Digest Conflict、Lease Expiry 和迟到结果如何查询/协调？
9. Durable Terminal Disposition Enum 是什么？哪些 DLQ 状态保持 Barrier-open？
10. D Inventory 接受哪些 Source Reference（EventRef、MemoryRef、MemoryVersionRef、EvidenceRef、不透明 Token）？如何校验传递 Ancestry 和 Scope Matching？

### 7.2 E 必须 Fail-closed 停止的条件

出现以下任一情况时，E **MUST** 在执行受影响动作前停止：
- 无法确认持久化 D Producer Registration Receipt；
- D 无法确定最新适用 ForgetFenceCursor；
- I 无法确定已认证 Principal/ProducerIdentity 和当前 PermissionEpoch；
- 操作的 ScopeRef 语义或 Security Domain Binding 未解决；
- 任一必需 Dependency Registration 缺失/部分/Unknown；
- 无法证明 Final Gate 和 Storage Visibility 共享 Atomic/Linearizable Boundary；
- Lease/Attempt 陈旧、撤销、过期或被 Fence；
- Source/Ancestor 已 Forgotten、Retention 不允许或未授权；
- D Barrier Ledger 报告 Gap、Unknown Producer Class 或未解决的先前 Attempt。

不得使用 Availability Fallback、手工 Queue Replay 或 Operator Override 绕过这些条件。只有 I-owned Policy Exception 可以改变 I Policy；它不能发明 D API，也不能免除可审计 D Barrier 的要求。

## 8. 安全与类型化身份对齐

- ProducerIdentity 必须绑定已认证传输上下文：已认证 Principal/Issuer、注册 Producer/Application Identity、Instance/Workload Identity、Credential/Key Validity、允许的 Event Family、Tenant/Security Domain 和 Revocation/Credential Epoch。
- Payload 中的 producer_id、ProducerId、ActorRef、agent_id 或 scope_ref 都只是声明/选择器，不是认证。H 绑定 Transport Principal；I 校验 Trust/Policy。Mismatch 必须 Reject/Quarantine。
- ActorRef 是 B/I 指向 Principal 和 Authority Chain 的类型化引用，不是 Bearer Credential。E 不能接受调用方构造的 ActorRef 作为证明。
- ScopeRef 遵循 B 的类型化领域引用语义。Scope Membership/Applicability 不等于 Grant；I 单独授权每个 Source 和 Operation。
- 当前 PermissionEpoch 必须在 Ingress、受保护 Dereference 前、每个敏感 Stage Commit 前、必要的 D Registration 前、Canonical Write Submission 前和 Final Publication 时重新检查。Admission 时 Epoch 只是观察值，不是永久能力。
- Idempotency Namespace 绑定已认证 Principal + ProducerIdentity + 已验证 Scope Binding + Tenant/Security Domain + Operation/Event Family + Caller Key。准确字段编码，以及多个 ScopeRef 是否组成规范集合，仍为 **CANDIDATE / 需 H-I-B 批准**。ScopeRef 不能被视为 Authorization。
- Authentication、Principal Binding、Scope Resolution、Policy Epoch、Retention 或 Revocation Status 任一未知，都必须 Fail-closed。

H Message Envelope 文档和 I Principal/ActorRef Contract 仍是 CANDIDATE 输入，不是冻结 Wire/Policy Schema。

## 9. Conformance 场景（NOT RUN）

1. D Registration Receipt 持久化前，Work Item 不得 Lease。
2. Forget 与 Admission 竞争必须串行化：Registration 要么纳入捕获 Barrier，要么被拒绝/隔离。
3. 每个 Fence 前 Work Item 在 Worker Crash、Lease Expiry、Retry 和 DLQ 期间都必须继续被 D 看见。
4. 只要仍可能 Replay，DLQ Item 就不能计为 Terminal。
5. 所有 Dependency Receipt 和 Publication Receipt 存在前，Runtime/Consumer 不得读取 Derived Artifact。
6. Dependency Registration 后、Final Gate 前发生 Forget，必须拒绝陈旧 Publication。
7. Lease 和 Gate 之间 PermissionEpoch 推进，旧 Attempt 不能 Publish。
8. 重复 Event 和 Accepted ACK 丢失，返回相同 Receipt/Work Identity。
9. D Registration ACK 丢失，返回相同 Receipt，不产生重复 Registration。
10. Publication ACK 丢失时 Artifact 保持隐藏，直到 Lookup 证明 Gate 已 Commit。
11. Cancel/Fence 后的迟到 Worker Result 不得可见。
12. Transitive Ancestor Forget 必须抑制 Derivative-of-derivative。
13. 跨 Scope Lineage 不得扩大授权。
14. Restore/Replay 在可查询前重新应用当前 Fence。
15. Canonical Cursor 在每个 Brain Authority 内全局有序；Aggregate Revision/Lifecycle Cursor 独立；F IndexWatermark 不得由 E 改写。

**验收：** 仅记录设计要求。不声称存在 Runtime 实现、Storage Atomicity、Conformance Test 或 Production Safety 结果。
