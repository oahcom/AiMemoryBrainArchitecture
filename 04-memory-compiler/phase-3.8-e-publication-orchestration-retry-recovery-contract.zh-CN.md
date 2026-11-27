---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "从 Owner 源分支恢复；Owner 接受仍待定。"
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
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.8-e-publication-orchestration-retry-recovery-contract.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-8-e-publication-orchestration-retry-recovery-contract"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-8-e-publication-orchestration-retry-recovery-contract
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.8 — E 发布编排、重试与恢复契约

- Owner 角色：E — Memory Compiler
- 状态：**E 角色提案；D/I/Storage 精确 API 和独立 Owner 批准仍为 OPEN**
- 相关：Issue #25；A Phase 3.8.1 契约面补充文件
- 英文与中文为同等规范文本。

## 1. E 权限边界

E 所有 CompileIntent、编译器入口回执、不可变编译器输入包、DerivationRun、Attempt/Lease 生命周期、私有暂存、完整输出/依赖提交和编译器侧恢复编排。

E 不签发 D ProducerClass 资格、D RegistrationReceipt、D PublicationParticipantRef、I 授权、Storage 可见性结果或 Global Forget 终态。Queue ACK、E AcceptedReceipt、本地 Published/Completed 标签和对象存储存在性都不是跨 Owner 证明。

## 2. 必需身份模型

- CompileIntentId：稳定的逻辑意图。
- ProducerWorkItemId：由 D 管理的稳定逻辑工作身份。
- request_digest：不可变的逻辑准入请求。
- DerivationRunId：一次不可变编译器输入/配置运行。
- AttemptId / LeaseId / LeaseEpoch：一次执行尝试和 fencing 代次。
- DependencyRegistrationId / complete_dependency_set_digest：一个不可变的完整血缘集合。
- PublicationOperationId / publication_tuple_digest：一次不可变发布尝试。
- D PublicationParticipantRef、I CommitAuthorizationReceiptRef、StorageVisibilityParticipantRef：三个不同的 Owner 专属身份。

相同传输操作的重试或解析 ACK 丢失时，必须保留操作身份和摘要。权威 NO_PUBLICATION 之后的新发布尝试，或制品/版本、源修订、依赖集合、Scope、编译器输入或 attempt/lease 元组发生变化时，必须分配新的 PublicationOperationId、参与者身份和 tuple digest。绝不能使用同一操作 ID 配不同摘要。

## 3. 规范 E 生命周期

1. 持久化 E 入口以及稳定的 CompileIntentId/ProducerWorkItemId。
2. 调用 D RegisterProducerWork，并通过 WorkItemId + request digest 解析持久化的 D RegistrationReceipt。
3. 只有 D 注册持久化后，E 才能入队、取得租约、解引用受保护源或执行。
4. 为一个 DerivationRunId 冻结不可变编译器输入包：精确源引用/修订、证据/溯源、Scope、策略观察、编译器/模型/schema 版本及确定性输入摘要。
5. 在每个受保护源解引用和执行边界重新验证当前 I 授权和 D fence/血缘。
6. 将不可变输出写入私有暂存。不得通过公开 locator、签名 URL、索引事件或缓存预热暴露。
7. 在依赖注册/发布前，将仅有 EventRef 的入口关联到精确 Canonical MemoryRef/MemoryVersionRef 身份和修订。
8. 将全部直接 + 传递依赖集合作为一个不可变 D 依赖注册操作提交。不得发布部分集合。
9. 解析完整的 D DependencyRegistrationReceipt。
10. 请求 Storage 持久化绑定到不可变发布元组的隐藏 StorageVisibilityParticipantRef。
11. 请求 D 准入绑定到该精确持久化 Storage participant 的 PublicationParticipantRef。
12. 请求 I 在其 PolicyDomain sequencer 中消费单次 CommitAuthorization 操作，并绑定精确 D 和 Storage participant 引用。
13. 请求 Storage 执行最终可见性事务，验证精确的 D 当前 participant/fence 和已消费的 I CommitAuthorizationReceipt / ICommitAuthorizationProof（不是提交后的 ITerminalProof）。
14. 通过相同 PublicationOperationId + tuple digest 解析 Storage 权威结果。
15. D 和 I 只有在验证相同 Storage COMMITTED_VISIBLE 或 NO_PUBLICATION 结果之后，才分别关闭自己的参与者。
16. 只有 Owner 回执均已解析后，E 才更新本地输出记账。E 本地状态不能关闭 D ProducerWork。

任何未解决步骤都会阻止流程推进。UNKNOWN 会使制品保持私有，且所有已准入屏障保持打开。

## 4. 仅 EventRef 的入口

E 可以在本地接受仅 EventRef 的输入，但在 D 签发 RegistrationReceipt 之前，不得派发具备派生能力的工作。D 准入要求经过认证的生产者、已启用的 ProducerClass/版本、精确 Scope、规范请求摘要和 D 批准的不透明血缘 token/摘要。E 的 AcceptedReceipt 仅是本地入口证据。

依赖注册/发布之前，E 必须解析精确规范源引用/修订，并将其追加到原始血缘。不完整或冲突的血缘保持私有/隔离。D 注册并不等于 I 授权读取受保护载荷。

## 5. 依赖完整性

一次依赖提交是一个不可变的完整集合操作，包括：
- 制品身份/版本/内容摘要；
- 每条直接源/父边；
- D 策略要求的每条传递祖先边；
- 精确源 MemoryRef/MemoryVersionRef 和修订；
- Scope 与溯源；
- 完整集合摘要及规范化配置。

E 可以在 D 依赖提交之前暂存字节，但暂存必须保持私有。如果依赖提交响应丢失，使用相同 DependencyRegistrationId + 摘要解析。部分集合、过期源修订、缺失 EventRef 映射或 Scope 变化都会产生 INCOMPLETE/CONFLICT，且不授予发布能力。

## 6. Attempt、Lease 与 Retry 语义

- Queue 是至少一次投递机制，不是权威。
- 逻辑重试保留 ProducerWorkItemId 和 request digest。
- 每次尝试取得新的 AttemptId/LeaseId/LeaseEpoch。
- 旧尝试不得注册依赖、发布、抑制更新的尝试或终结工作。
- 同一不可变发布操作的传输重试和崩溃恢复，复用 PublicationOperationId + tuple digest + 全部 participant refs。
- 权威 NO_PUBLICATION 之后，新尝试属于新的不可变发布操作，使用新的 PublicationOperationId、participant refs、tuple digest 和新鲜 D/I 检查。
- 编译器输入、源修订、模型/schema/compiler 配置、输出摘要、依赖集合或 Scope 变化，会创建新的 DerivationRun/输出身份，并要求新的 D 依赖和发布准入。
- DLQ 是队列状态，绝不是终态证明。Replay 必须解析相同逻辑工作和当前 D/I 策略；不得绕过 ForgetFence。

## 7. 终态与输出记账

E 必须向 D 提供持久化清单：
- 每个 DerivationRun 和 Attempt；
- 每个暂存制品/版本；
- 每次依赖注册；
- 每个发布操作及其已解析的 Storage 结果；
- 每个已抑制/隔离输出，以及证明它之后不可能发布的证据；
- 所有 retry、DLQ replay、outbox 和 delayed publisher 路径。

只有 D 能签发 D ProducerWork terminal receipt。E 的 Published/Failed/Cancelled/Completed 标签都不意味着 D 已终态。任何 UNKNOWN participant 或清单缺口都会使工作保持 open。

## 8. Restore 与恢复

恢复从隔离的非服务模式开始：

1. 恢复 Storage participant/visibility 记录和 DB incarnation proof。
2. 对账 D producer ledger、RegistrationReceipt、Fence/high-water、dependency receipts 和 PublicationParticipantRefs。
3. 对账 I 当前 PolicyDomain policy/revocation/registry 及进行中的 authorization participants。
4. 对账 E CompileIntent、DerivationRun、Attempt/Lease 和输出清单。
5. 在更广泛恢复契约要求时，对账 COC 前缀及所有其他独立 Owner 证明。
6. 仅通过稳定操作身份/摘要进行幂等重放。未知缺口保持隔离。
7. 只有独立 D/I/Storage 证明一致后才重新启用服务。

不得从队列行缺失、租约过期、进程死亡、陈旧副本、缺少回执或时间推断终态。对正在进行操作的恢复，保留相同不可变发布元组。

## 9. E 状态转换概要

- INGRESS_ACCEPTED → D_REGISTRATION_PENDING → D_REGISTERED
- D_REGISTERED → QUEUED → LEASED → RUNNING
- RUNNING → PRIVATE_STAGED → DEPENDENCY_PENDING → DEPENDENCY_COMPLETE
- DEPENDENCY_COMPLETE → STORAGE_PREPARED_HIDDEN → D_PUBLICATION_ADMITTED
- D_PUBLICATION_ADMITTED → I_COMMIT_WON（或 REVOCATION_WON / UNKNOWN）
- I_COMMIT_WON → STORAGE_COMMIT_PENDING → COMMITTED_VISIBLE（或 NO_PUBLICATION / UNKNOWN）
- UNKNOWN → RECONCILIATION_REQUIRED（绝不自动中止）
- local output disposition → D_TERMINAL_PENDING → D_TERMINAL_CONFIRMED

这些是 E 编排标签，不替代 Owner 回执或 Owner 权威状态。

## 10. E 必需测试

- 入队前 D registration ACK 丢失：同一 ID 解析前不得派发。
- 仅 EventRef 输入且血缘完整/不完整。
- 至少一次投递导致的重复队列消息。
- 过期 lease 尝试注册依赖/发布。
- 完整依赖集合注册期间崩溃。
- Storage prepare 后、D admission 前崩溃。
- D admission ACK 丢失。
- I 撤销优先与 COMMIT_WON 优先两种顺序。
- Storage visibility ACK 丢失。
- NO_PUBLICATION 后使用新操作身份创建新发布尝试。
- D/I/Storage 记录缺失/矛盾时恢复。
- 终态请求之后的 DLQ replay 和 delayed publisher。

## 11. E 未决决策

精确 D/I/Storage 可调用 API schema、H wire 编码/签名、lease epoch 权威、源血缘规范化、保留期限和一致性实现仍为 OPEN。

## 12. 中文规范

### 12.1 E 权限边界
E 管理 CompileIntent、编译器入口回执、不可变 Compiler Input Bundle、DerivationRun、Attempt/Lease 生命周期、Private Staging、完整 Output/Dependency 提交和 Compiler Recovery Orchestration。E 不签发 D ProducerClass 资格、D RegistrationReceipt、D PublicationParticipantRef、I Authorization、Storage Visibility Outcome 或 Global Forget Terminality。Queue ACK、E AcceptedReceipt、本地 Published/Completed 标签和对象存储存在性均不是跨 Owner 证明。

### 12.2 生命周期
E 先持久化入口和稳定 WorkItem 身份，再取得 D RegistrationReceipt；之后才能 Queue/Lease/Protected Source Dereference/Execute。冻结单次 DerivationRun 的精确输入包。输出先进入 Private Stage。EventRef-only 必须在 Dependency Registration/Publish 前关联精确 Canonical MemoryRef/MemoryVersionRef 与 Revision。完整 Direct/Transitive Dependency Set 作为单一不可变操作登记。之后严格按 Storage Prepare → D Publication Admission → I 单次 Sequencer Consumption → Storage Final Visibility Commit → D/I 独立 Closeout 执行。

### 12.3 重试与身份
同一操作的 Transport Retry、Lost ACK Resolution、Crash Recovery 必须复用 Operation ID、Tuple Digest 和 Participant Refs。逻辑 Work Retry 保持 ProducerWorkItemId/Request Digest，但 AttemptId/LeaseId/LeaseEpoch 更新。权威 NO_PUBLICATION 后的新发布尝试必须分配新的 PublicationOperationId、Participant Refs 和 Tuple Digest。任何 Source Revision、Dependency Set、Scope、Compiler Input/Config 或 Artifact Digest 变化都需要新的不可变 Run/Output Identity 与新 Gate。

### 12.4 终态与恢复
E 必须提交所有 Run、Attempt、Stage、Dependency、Publication、Suppressed/Quarantined Output、Retry、DLQ、Outbox 和 Delayed Publisher 的完整 Inventory。仅 D 可签发 ProducerWork Terminal Receipt。Restore 先隔离，再独立核对 Storage、D、I、E 及所需 COC Proof；未知状态保持 Quarantine。不得由队列缺行、Lease 过期、进程死亡或陈旧副本推断终态。

### 12.5 未决事项
D/I/Storage Callable API、H Wire Encoding/Signature、Lease Epoch 权威、Lineage Canonicalization、Retention 和 Conformance 实现仍 OPEN。本提案不构成 Schema Freeze 或实现通过。
