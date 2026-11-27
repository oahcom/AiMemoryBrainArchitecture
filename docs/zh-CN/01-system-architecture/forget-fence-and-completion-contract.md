---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Delegated direction decision, 2026-11-26"
        - "Work Item AID-2026-089"
        - "Issues #1125 and #1211"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Candidate source restored in Draft PR; exact-version D/Storage/A acceptance and normative approval pending."
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
    canonical_scope: "D canonical ForgetFence authority and Storage projection boundary"
    canonical_scope_id: "memory-brain/forget-fence-authority"
    canonical_scope_keywords:
      - forget-fence
      - canonical-suppression
      - storage-projection
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "01-system-architecture/forget-fence-and-completion-contract.md"
---
# Canonical Forget Fence 与完成契约

- 文档 ID：D-FORGET-CONTRACT-001
- 版本：1.0
- 源分支：main
- 源文件版本：AID-2026-089 已恢复规范根路径；精确 Blob 记录于 Draft PR Head。
- 历史源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3（仅作来源证据）
- 规范源：[01-system-architecture/forget-fence-and-completion-contract.md](../../../01-system-architecture/forget-fence-and-completion-contract.md)；本文件和英文文件均为镜像。
- 对应英文：[Canonical Forget Fence and Completion Contract](../../en/01-system-architecture/forget-fence-and-completion-contract.md)
- Owner：Session D — Memory Brain Principal Architect
- 状态：D Canonical Domain 语义为 DECIDED；跨模块执行和全局完成策略为 OPEN / 由 I 拥有
- 相关问题：D-REV-P1-001、D-REV-P1-003、INT-P0-02、INT-P0-03、INT-P1-03、INT-P1-06

## 1. 目的与权威

本契约定义 Forget 的 Canonical Authority 边界：持久化操作身份、单调抑制 Fence、依赖清单、Producer Admission/Registration、Barrier 语义、目标确认以及 Canonical Domain 证明。这是领域契约，不是 Wire/API Schema。

- **D 拥有：** Canonical ForgetOperation ID/状态；受影响的 Canonical Target 引用；持久化 ForgetFenceCursor/Generation；依赖清单权威；Producer Registration/Barrier Ledger；Canonical Target 进度；Canonical Domain 抑制证明；在 I 提供治理标准后，将 Lifecycle 转换为 Forgotten。
- **I 拥有：** Principal/授权与撤销策略、Permission Epoch、Retention、Backup/外部副本规则、残余例外批准、全局完成策略和物理擦除要求。D 不得自行授权，也不得宣布全局/物理完成。
- **E 拥有：** Compiler Work Queue/Lease/Retry/DLQ/Replay，以及派生物发布执行。
- **F 拥有：** 在途 Retrieval 取消/最终处理、候选抑制、Cache/Working Set、Index 重建和每个 Index 的 Watermark。
- **G 拥有：** Context Snapshot/Delta/ChangeSet/Delivery Intent 和 Context 协调。
- **H 拥有：** BMCP Wire、Adapter 本地状态、离线重连，以及可信的应用/清除确认。

D 对其他模块动作的引用是强制边界要求，不是在定义这些模块的内部状态机、Wire 字段或实现。

## 2. 术语：三种不同结果

1. **Logical Suppression（逻辑抑制）：** 被覆盖的 Canonical Target 不再可供普通读取、候选生成、引用解析和新发布。它由持久化 Fence 强制执行，并在 Canonical Authority 边界立即生效。抑制不等于删除。
2. **Asynchronous Cleanup（异步清理）：** 每个派生物 Owner 使自己的物化结果失效、移除、重建或隔离，并记录针对具体目标的确认。清理可以重试，也可能保持部分完成。
3. **Physical Erasure（物理擦除）：** 根据 I 的策略和证据规则，从存储、备份、外部接收方或供应商控制系统中不可逆地移除。D 不执行，也不证明物理擦除。

D 的 CanonicalSuppressionComplete 仅表示：D 定义的封闭世界 Producer Barrier 已排空，所有必需的 Canonical Domain Target 均已抑制，或带有 I 明确批准的残余例外。它不表示每个模块都已物理删除字节，也不代表全局 Forget 完成。

## 3. 持久化身份与 Fence

每个被接受的 Forget Request 都获得唯一、不透明、持久化的 ForgetOperationId。客户端重试使用有 Scope 的 Idempotency Key 和规范化 Request Digest：相同 Key/相同 Digest 返回同一 Operation；相同 Key/不同 Digest 属于幂等冲突。Operation 记录准确的 Target TypedObjectRefs、Target Set Digest、ScopeRefs、请求方 ActorRef、I 的授权决策引用/Policy Version、Reason、时间戳、Dependency Inventory ID、Producer Barrier 元数据、逐目标状态和证明引用。不得存储已遗忘的明文内容。

Fence 安装是 Canonical Transaction。D 从 Canonical Forget Authority 分配严格递增的 fence_generation，并持久化：
- ForgetFenceCursor = (forget_operation_id, fence_generation, target_set_digest)；
- 准确覆盖的 Target Identity 和 Version Family，包括之后发现的 Canonical Descendant；
- 生效抑制时间戳和 Fence 安装时的 Canonical Commit Cursor；
- Idempotency Receipt 和可恢复 Outbox Intent。

Generation 永不递减、永不复用，并且在重启/恢复后保留。重叠的 Forget Operation 产生更晚的 Generation；某个 Target 的有效 Fence 是所有适用 Generation 中最大的一个。Fence 作用于 Target Identity/Version Family 及已登记后代，而不只是请求时观察到的精确 Payload Revision。不得通过新建 Memory ID 重新导入相同的已遗忘来源或派生血缘。

每个读取/写入/发布边界都必须根据 Target 和来源血缘检查最新适用 Fence。陈旧缓存 Fence 不够：如果无法确定最新 Fence，受影响 Target 必须 Fail-closed。Worker 的 Admission Generation 只能证明它观察到了什么，不能永久授权其发布。

## 4. 依赖清单与 Producer Registration

### 4.1 封闭世界 Producer Registry

D 为所有获准创建、转换、重放或发布 Canonical Target 派生物的组件维护规范 Producer Class/Registration Ledger。每个模块 Owner 必须在某个 Producer Class 开始处理数据前，注册该类别及其 Work Admission 边界。每个 Work Item 在执行前必须持久化登记，并包含：
- 稳定 Producer/Work ID 和 Producer Class；
- 来源 Canonical 引用及准确 Revision/Lineage；
- Target ScopeRefs 和 Operation/Correlation ID；
- Admission CanonicalCommitCursor 和已观察的 ForgetFenceCursor/Generation；
- Lease/Attempt 身份和 Registration 状态。

当前架构要求登记的 Producer Class 包括：E Compilation/Replay；F Retrieval/Materialization/Index Rebuild；G Context Reconciliation/Snapshot/Delta/Delivery；H Adapter Delivery/Reconnect。这是 Producer 边界清单，不代表 D 实现了这些 Worker。

在 Registration 持久化之前，Producer 不得启动 Work、获取 Lease、排入 Retry/DLQ Replay 或发布派生物。仅插入 Queue 不足以构成 Registration。Work Registration 必须幂等。Ledger 有缺口或 Producer Class 未知时，Barrier 不得关闭。

### 4.2 Fence Snapshot 与 Barrier

Fence 安装必须原子捕获当前 Producer Registration High-water Mark（producer_registration_barrier），并同时捕获 Target Inventory Snapshot/Watermark。该 Barrier 包含 Fence Transaction 之前所有已持久化接纳的 Work Item。Canonical Suppression Proof 形成之前，每项工作都必须获得持久化的终态处置：
- 在 Fence 之前提交/发布，并且所有派生物均已登记且纳入 Dependency Inventory；
- 取消/过期且未发布；
- 被 Fence 抑制/隔离；
- 失败并持久化停放，禁止发布，等待明确恢复。

Lease Timeout 不是 ACK。过期 Lease 必须由 Owner 恢复/协调；在记录终态证据前，Work Item 仍未解决。Producer 不得通过删除 Queue Message 或丢弃 Lease 让自己从 Barrier 中消失。

Fence 安装后，引用已被 Fence 覆盖的 Target/Lineage 的新 Work Registration 必须被拒绝、隔离，或仅作为抑制/清理任务接纳。新任务不能仅因为携带当前 Generation，就发布来自已遗忘来源的派生物。其 Source Lineage 必须重新检查活动和终态 Fence。Producer Class 不得存在未登记的旁路；如果无法证明 Registry 完整，Barrier 必须保持打开。

### 4.3 Register-before-visible 规则

每个派生物在对任何消费者可见之前，都必须登记到 D 的 Dependency Inventory。派生物记录和 Dependency Edge 必须原子提交，或采用等价的持久化 Prepare/Commit 协议，确保失败时派生物不可见。最终 Publish/Commit Gate 必须在昂贵处理完成后、可见性发生前立即重新检查最新适用 Fence。如果 Fence 已推进或覆盖任一祖先，输出必须被抑制/隔离，不能进入 Canonical Read、Index、Cache、Context、Delivery 或 Inference Input。

该规则关闭“扫描已经完成，但迟到输出又出现”的竞争窗口：Fence 前接纳的 Producer Work 会被纳入 Barrier；其输出若没有最终 Fence 检查和预先完成的 Dependency Registration，就不能变为可见。Fence 后接纳的工作不能绕过活动 Fence。Fence 后发现未登记派生物属于 Barrier Integrity Violation：立即抑制它，重新打开/使先前证明失效，记录 Producer Class 缺陷并通知 I/A；绝不能静默把它计为已经覆盖。

## 5. Target ACK 与完成证明

每个 Target ACK 的键为 (forget_operation_id, target_ref, target_owner, target_attempt)，并记录：
- state：discovered | suppression_requested | suppression_confirmed | cleanup_confirmed | failed | unknown | excepted；
- Target Owner 的稳定 ACK ID 和 Contract/Capability Version；
- 已观察的 ForgetFenceCursor/Generation 及准确 Target/Ref Digest；
- 时间戳、Retry/Attempt、Correlation/Causation ID 和结构化错误；
- 该 ACK 覆盖的是 Active Read、Queued Work、In-flight Work、Cache、Index、Snapshot/Delta、Delivery，还是 Adapter 本地受管区域。

ACK 语义不可互换。suppression_confirmed 证明该 Owner 会在其声明边界内阻止暴露或新发布该 Target。cleanup_confirmed 证明该 Owner 声明的清理动作已经完成。两者都不能证明该 Owner 控制域之外的物理擦除。Unknown 和 Timeout 不是成功。对同一 Attempt，ACK 必须单调；重试不得降低已确认的抑制状态。但如果后来发现新的派生物，必须创建新的 Target Entry，并使之前的封闭世界证明失效，直到重新协调。

D 的 Canonical Domain Proof 必须绑定：
1. ForgetOperationId、规范化 Request Digest、Target Set Digest 和最终 Fence Generation；
2. Fence 安装的 CanonicalCommitCursor 和准确受影响 Canonical Ref；
3. Producer Registry Version 和 Producer Registration Barrier High-water Mark；
4. 证明每个 Fence 前已登记 Work Item 均已终结，且每个派生物在可见前均已登记的证据；
5. Dependency Inventory Snapshot 和最终 Reconciliation Watermark/Cursor；
6. 逐目标抑制 ACK，或精确的 I 批准残余例外引用；
7. 不存在未解决的 Producer Registry 缺口、Lease、Retry、DLQ/Replay Item、发布缺口或未知必需 Target；
8. 如果/当 Memory 转为 Forgotten 时，对应的 Canonical Lifecycle Event/Ref；
9. Proof Schema Version、创建时间和审计关联信息。

Proof 不可变且不能反向重建内容：只包含标识符、Digest、状态和引用，不包含已遗忘内容。它只能证明 D 的 Canonical Domain 抑制边界，以及其中列举的已登记 Target ACK。

I 的策略决定全局完成是否要求 Cleanup ACK、离线 Adapter ACK、Backup、外部接收方或物理擦除。例外只有在 I 提供持久化、策略批准的引用时才有效，其中必须包含 Target、Scope、理由、过期/复核条件和残余风险。D 不得自行发明或批准例外。

## 6. 必需竞争矩阵与边界要求

| 竞争场景/子系统 | D Canonical 要求 | Owner 模块执行义务 | 失败结果 |
|---|---|---|---|
| E 排队中的 Compiler Work | Queue Admission 和 Work Registration 必须先于执行；Fence Inventory 包含排队任务 | E 在 Dequeue/Lease 前，以及 Canonical Proposal/Commit 前检查 Fence | 取消/隔离；直到终态前 Barrier 保持打开 |
| E 已租用/在途 Work | Lease/Work ID 必须在 Fence 前 Barrier 中；最终 Publish Gate 重新检查 Fence | E 在 Extraction/Consolidation 后、派生物登记/提交前立即检查 | 抑制输出；将发现的 Target 登记为 Blocked；不得 Canonical 可见 |
| E Retry/Scheduler/DLQ/Replay | 每次 Retry/Replay 都是链接原始来源血缘的已登记 Work Item | E 携带原 Source Ref/Fence Context；每次 Retry/Replay 都重新授权并检查 Fence | 拒绝/隔离陈旧 Replay；Retry 不能续期发布权 |
| F 在途 Retrieval | Request/Source Ref 和活动执行都由 Producer Registration 覆盖 | F 在最终候选/结果输出前重新检查 Fence，而不是只在 Query 开始时检查 | 丢弃受影响候选；按 F 定义将响应标记为 Incomplete/Blocked |
| F Cache / Working Set | Cache/Materialization Target 纳入 Dependency Inventory | F 在 Cache Read/Write 检查 Fence；Key/Invalidation 包含 Fence Generation 和 Scope/Policy Context | Cache Miss/Deny；不得返回陈旧条目 |
| F Index Rebuild | Rebuild Job/Output Generation 已登记；IndexWatermark 不是 Forget Proof | F 在 Segment Publish/Swap 和 Candidate Generation 前检查 Fence；从 Canonical Snapshot + Replay 重建 | 不发布陈旧 Segment；隔离/重建；Watermark 不得越过未解决 Commit 缺口 |
| G Context Snapshot/Delta/ChangeSet | Context Ref 和待处理变更必须可发现 | G 对受影响引用写 Tombstone、使 Snapshot/Delta 失效并提交新的安全 ContextVersion | 旧不可变 Snapshot 仅供审计；绝不作为当前版本提供 |
| G Prepared/Delivered Work | Pending Delivery 已登记并绑定准确 ContextVersion | G 尽可能取消/Supersede，并在 Delivery 前立即检查 Tombstone/Fence | Delivery 保持 Pending/Unknown/Superseded；不得迟到提升 Applied |
| H Adapter 在线 Delivery | Adapter/Session 是已登记派生目标；D 不定义 Wire 字段 | H 消费 Fence/Revocation 并返回其拥有的 ACK | 抑制受管区域；缺失 ACK 保持 Unknown |
| H Adapter 离线重连 | 离线 Adapter 仍是未解决目标；Offline 不等于成功 | H 认证并协调最新 Fence，丢弃陈旧 Snapshot/Delta，应用安全状态并在复用前证明 | 不得复用缓存 Context；在 H 的标准满足前保持 Unknown/Blocked |
| 迟到 Applied ACK | 迟到 ACK 不得覆盖更新的 Fence 或恢复陈旧 Target | G/H 拒绝对当前状态应用陈旧 Target Version；只保留为历史证据 | 记录迟到证据；不得复活或回滚 Head |
| Backup / 外部副本 | 清单/ACK 要求由 I 定义；D 记录发现的 Target/Ref | I 和指定 Owner 执行 Retention、Backup 和外部接收方策略 | D 不得声称物理删除；全局完成仍由 I 拥有 |
| 并发 Canonical Write | Fence 与写入 Gate 必须针对相同 Target Lineage 串行化 | D 在 Canonical Transaction Commit 时检查最新 Fence | 拒绝/隔离写入；不得出现 Fence 后可见派生物 |

## 7. Operation 状态与 Lifecycle 分离

ForgetOperation 状态不是 Memory Lifecycle。D 的 Operation 阶段包括 Requested、FenceEstablished、InventoryOpen、BarrierDraining、TargetReconciliation、CanonicalSuppressionComplete、Blocked 和 Failed。Memory Lifecycle 仍然是 Candidate、Consolidated、Active、Superseded、Archived 或 Forgotten。“Forgetting”不是 Memory 状态。只有当 I 的适用策略标准满足时，才追加独立的 Canonical Lifecycle Event，将 Memory 转为 Forgotten；该事件本身不是物理擦除证据。

## 8. 接口、故障、幂等与可观测性

- **Producer Registration Contract：** D 拥有领域契约；E/F/G/H 是 Producer；D Dependency/Barrier Ledger 和 I Completion Evaluator 消费该契约。必须提供稳定 Work ID、Source Ref/Revision、ScopeRefs 和已观察 Fence。Retry 保留 Work Identity/Lineage，或创建关联 Attempt；不得无登记 Replay。
- **Target ACK Contract：** D 定义领域含义；E/F/G/H 产生 Owner 专属证据；I 决定必需 Target Class 和例外策略。相同 ACK ID/Digest 必须幂等；冲突证据应拒绝并审计。
- **故障行为：** 无法获取最新 Fence 时，对受影响 Target Fail-closed；未知 Target/Producer/Lease/Gap 阻止 Barrier 关闭。部分工作可恢复。绝不把 Timeout 转成成功。
- **可观测性：** Operation ID、Fence Generation、Target Set Digest、Producer Registration High-water、开放 Work 数量、Dependency Inventory Cursor、Target 状态数量、迟到派生物数量、Barrier 年龄、阻塞原因和 Correlation/Causation。不得记录已遗忘 Payload。

## 9. 一致性测试（设计验收；尚未执行）

1. Forget 与 Canonical Write 竞争：只有一个串行化顺序获胜；Fence 获胜则拒绝写入；Write 获胜则派生物已登记并纳入 Barrier。
2. 排队、已租用、Retry、DLQ 和 Replay 的 Compiler Work 在 Fence 后都不能发布；全部能在 Registration Ledger 中找到。
3. Fence 后才完成 Extraction 的迟到 Compiler Output，必须在登记/可见前隔离，不能创建可读取 Canonical Asset。
4. 在 Query 开始后、Response 最终确定前安装 Fence，必须抑制 Runtime 在途结果和 Cache Hit。
5. Index Rebuild 在 Fence 后不能交换陈旧 Segment；Watermark 不代表抑制或清理。
6. G Snapshot/Delta 和 Prepared/Delivered Context 在 Fence 后不得重新应用；迟到 Applied Evidence 不得重新激活。
7. 离线 Adapter 重连后，必须先协调最新 Fence 再使用缓存 Context；无 ACK 意味着 Unknown。
8. Producer Registration 缺口、过期且未恢复的 Lease、未知 Target 或缺失 ACK 都会阻止 Barrier 关闭。
9. Fence 后尝试从已遗忘祖先登记派生物，即使提交最新 Generation 也必须拒绝/隔离。
10. 重复 Forget Request 返回相同 Operation；相同 Idempotency Key 配不同 Target Digest 时冲突。
11. 迟到的未登记派生物使既有 Proof 失效并重新打开协调；不得静默成功。
12. Proof 不包含已遗忘明文，也不声称 Backup/Provider 已物理擦除。

**验收状态：** 语义已定义；实现一致性、I 策略批准和 E/F/G/H 执行证据仍为 OPEN。本文不代表 INT-P0-03 已在全局关闭。

## 10. Phase 3.5 操作级原子性契约

[forget-fence-operation-and-publication-gate.md](forget-fence-operation-and-publication-gate.md) 对 CR-P1-01 / D-REV-P1-003 的 D 语义具有规范效力。它细化但不削弱上文 §§3–9。

规范操作包括 RegisterProducerClass、RegisterProducerWork、InstallForgetFence、CaptureProducerRegistrationHighWater、RegisterDerivedDependency、PublishDerivedIfFenceCurrent、CompleteProducerWork、ResolveProducerWork 和 ReconcileForgetBarrier。其输入、输出、幂等键、错误结果和线性化点均在 Operation Contract 中定义。

### 10.1 强制串行化规则

RegisterProducerWork 和 InstallForgetFence 必须共享一个可线性化排序域。如果 Registration 先提交，其 ProducerRegistrationSequence 必须小于或等于 Fence 捕获的不可变 High-water，并纳入 Barrier。如果 Fence 安装先提交，则针对被覆盖来源的普通派生物 Admission 必须被拒绝/隔离，或明确限制为 Cleanup-only。禁止存在“已 Accepted 但未被 Barrier 捕获，却仍可能发布”的 Work Item。

### 10.2 强制可见性规则

Dependency Registration 必须先于可见性持久化。PublishDerivedIfFenceCurrent 必须在同一个外部可观察的原子/线性化边界上，校验完整 Dependency Set、Work/Attempt Identity、最新适用 ForgetFence，以及 I 当前的 PermissionEpoch；该边界同时将 Artifact 从 Private 改为 Visible。独立的 Check-then-write 或未协调的 Gate Token 不够。结果不明确时，Artifact 必须保持 Private，直到 ResolveProducerWork 确认已提交结果。

### 10.3 证据与类型分离

Publication Evidence 必须绑定 WorkItemId/AttemptId、ProducerClass、来源 MemoryVersion/Revision、ScopeRefs、RegistrationReceipt、已观察及权威 ForgetFenceCursor、PermissionEpoch 和 I Decision Reference、DerivedArtifact 身份，以及每个 DependencyRegistrationReceipt。ForgetFenceGeneration 和 PermissionEpoch 是不同的类型化命名空间，绝不能进行数值比较或混用。

### 10.4 状态

D 的 Operation 语义和必需竞争结果已作为领域契约 DECIDED。E 映射、I 授权决策语义、全局 Producer Inventory 完整性，以及 Storage/Consistency 实现仍为 OPEN。已审查的任务包中没有建立 Storage/Consistency Owner，这是明确的 OPEN 所有权缺口。设计一致性测试用例已定义，但 NOT RUN。本节不关闭 INT-P0-03，也不声称端到端 Forget 已完成。

## Phase 3.6 规范性补充 — 原子性边界

D 拥有的 Phase 3.6 操作级线性化、Producer Work 状态机、Fence/Permission 双重校验规则、与实现无关的 Storage 语义要求、12 项 Fault/Race Proof Matrix 和 D/E/Storage OPEN Decision Register，均在 [forget-fence-operation-and-publication-gate.md](forget-fence-operation-and-publication-gate.md) 的 “Phase 3.6 — Forget Fence Linearization & Atomicity Semantics” 中规范性定义。

唯一安全不变量是：只有在逻辑 Producer Work 已持久化登记并被每个适用 Forget Barrier 核算、完整依赖血缘已持久化，并且最终可见性提交校验了最新适用 D ForgetFence 以及针对已认证 Principal 和准确 Scope 的 I 当前授权/PermissionEpoch 后，派生物才可以被检索、投递、索引、推理或以其他方式暴露。Unknown 或陈旧证据意味着不可见。

Work Registration、Barrier Capture、Dependency Registration、Staging、Publish Authorization、Durable Commit、Artifact Visibility 和 Terminal Disposition 是分别带证据的阶段。Barrier Capture 负责核算 Fence 前工作，不等于发布许可。Lease 过期、Queue 删除、Retry 延迟和 DLQ 停放都不构成 Work 终结。

D 只定义领域语义和可观察顺序。Storage 可以选择任何能够证明相同线性化和崩溃恢复行为的实现；本补充不批准任何数据库，也不声称已经实现。**CR-P1-01 仍为 OPEN，等待 E + Storage 联合确认和可执行证据。**

## 10. 单一权威裁决——委托方向决策，2026-11-26

授权人：user-authorized operator (delegated by account owner)  
决策日期：2026-11-26  
状态：方向已记录；D、Storage/Consistency 与 A 的精确版本验收待完成。本裁决不构成实现授权。

D — Memory Brain — 是 ForgetOperation 身份/状态、Canonical Target 与传递派生血缘覆盖范围、单调 ForgetFence Generation/Cursor、Canonical Suppression 和 D 域证明的唯一逻辑权威。即使 Storage 物理持久化这些字节，Forget 也只有一个决策空间。

Namespace 是已解析 Scope/分区属性，可以约束匹配，但不是独立 Fence 身份，不能替代 Typed Canonical Target Identity、精确 Memory/Version 引用、来源身份或派生血缘。Target Set 必须明确精确 Scope 覆盖范围及来源到派生物的血缘。

任何 Storage 本地 Memory/Version Fence 行都只是 D 所有权威 Snapshot 的派生、可重建投影。它 MUST NOT 创建独立 Generation/Cursor、决定覆盖范围，或在没有当前 D 权威状态时授权读取/发布。Storage 仍拥有物理存储的事务持久性、原子可见性、备份/恢复、复制和防回滚机制权威；物理保管不转移逻辑权威。投影不一致时必须 Fail-closed，并从 D 协调重建。

每个读取/写入/发布、Compiler、Retrieval/Index、Context、Delivery/Reconnect 和最终请求 Gate，都必须针对精确 Target/Lineage 建立当前 D Snapshot/Cursor。D 状态缺失、陈旧、损坏、回滚或 Scope 覆盖不足时必须 Fail-closed。本地 Target Suppression 不等于 Global Forget Completion；I 保留全局策略、Retention、Legal Hold、外部副本和物理擦除权威。

Reviewer 判据：
- FF-A1 PASS 当且仅当 D 是 ForgetFence Generation/Cursor 的唯一逻辑签发者/权威；否则 FAIL。
- FF-A2 PASS 当且仅当 Storage 本地 Fence 是可重建的 D 派生投影且没有独立 Sequence/Cursor；否则 FAIL。
- FF-A3 PASS 当且仅当 Namespace 未替代 Typed Target、Scope 和传递血缘覆盖；否则 FAIL。
- FF-A4 PASS 当且仅当 D 状态缺失/陈旧/损坏会阻止受影响读取/发布；否则 FAIL。
- FF-A5 PASS 当且仅当本地抑制与 I 治理的 Global Forget Completion 明确区分；否则 FAIL。

仍未闭合：D 公共 Snapshot/Read API、精确 Target/Lineage Schema 验收、跨 Owner 执行顺序、Storage 物理防回滚证明及实现/一致性验证。
