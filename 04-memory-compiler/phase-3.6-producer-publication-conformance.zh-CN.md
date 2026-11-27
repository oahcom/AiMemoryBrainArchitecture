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
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6-producer-publication-conformance.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-producer-publication-conformance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-producer-publication-conformance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6 — 生产者发布一致性

- Owner：Session E — Memory Compiler
- 状态：**设计契约完成 / 实现尚未验证**
- 范围：E Producer Work、暂存、依赖注册、最终发布、回执和向 F 交接
- 证据类别：仅静态文档契约；未运行可执行测试或故障注入。

## 1. 必需不变量

1. 每个具备派生能力的生产者类别都必须先在 D 注册并启用，之后才能准入工作。
2. 每个 WorkItemId 在重试、DLQ、重放、重新编译和工作器恢复期间都必须持久且稳定。
3. D RegistrationReceipt 必须先于入队、租约、受保护源解引用或执行而存在。
4. Candidate 和 Staged Artifact 必须保持私有，F、G、H、其他生产者及外部消费者均不可访问。
5. 最终发布之前必须完成持久化的完整依赖注册。
6. 最终发布必须在可见性提交时验证当前 ForgetFenceGeneration、I PermissionEpoch、活动工作/尝试/租约、精确源 MemoryVersion、ScopeRef、依赖回执和制品身份。
7. Fence 安装与最终可见性提交必须在同一个共享权威中序列化，或通过明确获批、可恢复的等效协议实现。
8. 未知结果必须保持私有且屏障打开；使用稳定 ID/摘要进行对账。
9. 任何重放/重建/重新编译/恢复路径都不得使已覆盖的源或后代复活。
10. F 只能索引那些已验证其提交可见性状态和 PublicationReceipt 的记录。

## 2. Producer / Storage 一致性矩阵

| ID | 场景 | 必需结果 | 保留证据 | 状态 |
|---|---|---|---|---|
| E36-01 | ProducerClass 缺失/禁用/登记不完整 | 拒绝/隔离准入；不得入队/租约 | D 类别回执/错误 + 无工作派发 | NOT RUN |
| E36-02 | RegisterProducerWork 与 InstallForgetFence 竞态 | 只能有一种序列化顺序；已准入工作纳入捕获的高水位，或 fence 后工作被拒绝/隔离 | D 注册/fence 回执 + 事务轨迹 | NOT RUN |
| E36-03 | D 注册 ACK 丢失 | 解析相同 WorkItemId/摘要；UNKNOWN 时不得入队 | D ResolveProducerWork 响应 | NOT RUN |
| E36-04 | 注册后工作器崩溃 | 使用相同 WorkItemId 恢复；旧租约失效；生成新 AttemptId | D 注册 + 租约历史 | NOT RUN |
| E36-05 | 旧工作器恢复时租约已过期 | 旧尝试不得发布或终结 | Lease epoch 和被拒绝的最终门禁回执 | NOT RUN |
| E36-06 | Retry/DLQ/Replay/Recompile | WorkItemId 稳定；新 AttemptId；重新编译使用新 DerivationRunId；重新检查当前 fence/permission | 血缘和尝试历史 | NOT RUN |
| E36-07 | F/其他生产者枚举 Candidate/Staged 对象 | 无结果；私有 ACL/可见性谓词拒绝访问 | 权威读取器测试 | NOT RUN |
| E36-08 | 依赖边集合仅部分提交 | 制品保持私有；无 PublicationReceipt | 依赖清单快照 | NOT RUN |
| E36-09 | 暂存后、发布前 fence 前进 | 最终门禁拒绝/隔离 | fence 回执 + 最终门禁结果 | NOT RUN |
| E36-10 | 暂存后、发布前 PermissionEpoch 被撤销 | 最终门禁拒绝/隔离 | I 决策 + 门禁事务轨迹 | NOT RUN |
| E36-11 | 发布与 fence 安装竞态 | 发布胜出并进入持久化清单，或 fence 胜出且发布被拒绝；不得存在第三种状态 | 可串行化竞态轨迹 | NOT RUN |
| E36-12 | 提交后 Publication ACK 丢失 | 解析相同 PublicationOperationId；返回原 PublicationReceipt；不得产生重复可见性效果 | 协调器/DB 记录 + 回读 | NOT RUN |
| E36-13 | Prepare 与最终提交之间崩溃 | Prepared Artifact 仍隐藏；恢复时幂等提交或中止 | participant/coordinator 日志 | NOT RUN |
| E36-14 | 可见性提交后、E 本地更新前崩溃 | 对账已提交标记/回执；不得再次发布 | DB 标记 + D 回执 | NOT RUN |
| E36-15 | Outbox 重放导致发布请求重复 | 相同操作 ID/摘要返回原回执 | outbox 和 D 查询 | NOT RUN |
| E36-16 | DLQ/Replay/Lease/Publication 未解决时请求终态 | D 拒绝终态；屏障保持打开 | D 终态错误/对账回执 | NOT RUN |
| E36-17 | 恢复时存在旧暂存/已发布对象 | 先隔离；服务前应用当前 fence/permission | restore manifest + reader denial | NOT RUN |
| E36-18 | Canonical + Derived 混合提交 | 使用一个获批的序列化决策；必需的 canonical 操作中止/被 fence 时不得暴露派生项 | D canonical + Publication 回执和事务轨迹 | NOT RUN |
| E36-19 | 相同幂等键、摘要变化 | 冲突；不可变原件保持不变 | 操作结果 | NOT RUN |
| E36-20 | 先前屏障检查点之后发现迟到派生项/祖先 | D 对账重新打开；不得复用过期完成证明 | 新的不可变检查点 | NOT RUN |

## 3. F 消费者契约

F 只能消费满足以下条件的制品：权威可见性记录已提交，且 D PublicationReceipt 对精确制品/版本、血缘摘要和 WorkItemId 的解析结果为 PUBLISHED。E 的 CandidateProduced、Staged、DependencyRegistered、CanonicalCommit 或 CompilerCompletionReceipt 均不足以作为依据。

对于 rebuild/backfill/replay：

- 具备派生能力的重建工作必须先取得 D producer admission；F 使用稳定 WorkItemId 并遵循 D 屏障语义。
- 在源解引用、索引段提交和披露之前，重新验证当前 D ForgetFence 覆盖范围及 I PermissionEpoch。
- 历史 STAGED/PRIVATE/UNKNOWN 记录必须隔离，绝不索引。
- SUPPRESSED/REJECTED_FENCED 记录必须排除，并对受影响的索引分区、缓存和 Working Set 应用失效。
- 不得盲目信任 PUBLISHED 记录：重新读取当前 fence/permission 和源祖先；若被覆盖/撤销/未知，则抑制而非索引。
- 只有已提交且完整的分区批次才能推进该分区连续的 IndexWatermark；存在缺口时水位停止。
- 重建绝不能将历史存在或旧 PublicationReceipt 转换为当前暴露权限。

## 4. 联合决策请求

| Owner | 请求的明确确认 | 当前状态 |
|---|---|---|
| D | 确认 WorkItemId 在重试、DLQ 重放、重新编译和工作器恢复期间仍是根屏障身份；确认精确门禁输入和 fence 胜出竞态行为 | REQUESTED / NO RESPONSE RECORDED |
| Storage/Consistency | 确认一个共享事务/序列化权威覆盖 D fence/work ledger、完整依赖注册和最终可见性标记；或提供获批的抗崩溃等效方案及恢复协议 | REQUESTED / NO RESPONSE RECORDED |
| I | 确认当前 PermissionEpoch 决策语义可在最终可见性提交时验证，并定义撤销新鲜度绑定 | OPEN / NOT CONFIRMED |
| F | 确认 rebuild/backfill 只消费已提交的 PUBLISHED 记录，并在重建和索引提交边界执行当前 fence/permission 检查 | REQUESTED / NO RESPONSE RECORDED |

## 5. 退出标准

- 已记录 D 语义确认。
- 明确确认 Storage 事务 Owner、序列化域、线性化点和恢复协议。
- 将 I 权限新鲜度语义映射到最终提交。
- F Owner 已确认消费者契约。
- 已运行可执行实现和 E36-01..20 故障/竞态套件，并保留轨迹。
- 已验证仅修改 E 路径范围；未修改 D/Storage/F/I/A 文件。

在所有适用证据具备之前，状态保持 **设计契约完成 / 实现尚未验证**。

## Phase 3.6.2 — E Owner 对修订版 JF-10 v2 的接受

**状态：E 接受 E 所有的生产者/发布消费契约；I 接受与实现仍为 OPEN。**

E 确认：

1. Accepted Receipt 仅表示持久化入口接受/幂等性；不表示 Canonical Memory commit、派生依赖注册、发布或读取器可见性。
2. E 在入队、租约、受保护源解引用、执行、重试、DLQ 重放或重新编译之前，取得 D 持久化的 ProducerWork RegistrationReceipt。WorkItemId 和血缘在各次尝试间保持稳定；AttemptId 和 LeaseEpoch 对过期工作器进行 fencing；DerivationRunId 标识重新编译，不能重置 Forget 屏障。
3. E 冻结不可变输出清单和完整的直接/传递血缘。发布 prepare 之前，依赖注册必须完整且持久化。部分/未知依赖状态保持私有。
4. E 将精确、不可变的 PublicationOperationId/RequestDigest 和 prepared participant 绑定提交给真正的 Storage 最终门禁。它不会把 CommitAuthorizationReceipt、I COMMIT_WON、队列投递、outbox 事件或 E 本地状态当作 Published。
5. 只有在权威回读匹配的 Storage PublicationReceipt 和 VisibilityPointer 结果之后，E 才进入 Published。ACK 丢失/重放解析相同操作 ID/摘要；摘要变化属于硬冲突。
6. Fence、inventory-seal、permission、work/attempt/lease、manifest、dependency 或 participant 状态过期/未知都会阻断可见性。禁止离线 ALLOW、过期 PermissionEpoch 宽限、直接暴露对象存储或未注册子工作。
7. Forget 完成后，旧任务从 retry/DLQ/replay/backup 恢复时，必须根据当前 D fence 和 I authorization/inventory 证据重新解析原 WorkItemId 和源血缘。不得创建新的 WorkItemId 逃离 fence。

E 接受 JF-10 v2 提案中 E caller/recovery 角色，以及在 I/Storage IN_DOUBT 期间保持非终态的要求。这是技术层 Owner 侧接受，不是存在可执行 Compiler、queue、lease service、database participant 或通过 E36 测试的证据。

## 4. Phase 3.6.2 补充生产者一致性用例

| ID | 场景 | 必需结果 | 保留证据 | 状态 |
|---|---|---|---|---|
| E36-21 | 离线生产者/工作器带着 fence 前排队或租约任务重新加入 | 源解引用前解析原 WorkItemId 和最新 D fence；过期尝试不得执行、暂存、发布或终结；不得生成新 ID | D 回执查询、当前 fence、租约 epoch、被拒绝尝试和审计记录 | NOT RUN |
| E36-22 | Forget 开启期间 I ProducerDomainInventoryEpoch 变化 | 当成员资格/能力/Scope/证据义务变化时，原 InventorySealReceipt 失效；E 不得将 D 高水位视为全局完整性；直到新 I seal 验证完成，发布/完成保持阻断 | 新旧 epoch、seal 摘要、失效原因和刷新后的目标清单 | NOT RUN |
| E36-23 | D CanonicalSuppressionComplete 后旧 Compiler 任务恢复 | 当前 fence 检查在发布前抑制；保留 WorkItemId 和血缘；迟到派生项触发 D proof 重新打开/对账，且永不可见 | 原工作回执、fence generation、任务/尝试身份、抑制回执和重新打开的 proof 引用 | NOT RUN |

这些补充覆盖 E36-01..20 中未作为独立 ID 明确列出的三个场景。所有既有 E36 预期结果保持不变。
