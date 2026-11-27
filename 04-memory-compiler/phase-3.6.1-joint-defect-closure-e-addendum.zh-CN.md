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
    canonical_status: Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.1-joint-defect-closure-e-addendum.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-1-joint-defect-closure-e-addendum"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-1-joint-defect-closure-e-addendum
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6.1 — E 联合缺陷关闭补充文件

- 权限：用户委托的 DE-S 联合架构师；仅涉及 E 生产者语义
- 状态：**已记录联合语义决策 / 实现尚未验证**
- 本文件与 `phase-3.6-joint-producer-publication-decision.md` 一并适用，并对其作进一步细化。
- 除用户联合委托范围外，不声称 I/D/Storage 已实现或批准。

## 1. JF-01 — 生产者清单与准入证据

E 必须在任何生产者类别和实例摄取、入队、取得租约、执行、重试、重放、重新编译或发布之前完成注册。E 的类别/实例清单必须有版本，并与 I 的 `ProducerDomainInventoryEpoch` 对账；D 的 `ProducerRegistryVersion` 和 `ProducerRegistrationHighWater` 仍是不同的量。E 不得把 D 工作高水位当作 E 已发现全部生产者路径的证明。

每个 WorkItem 注册请求都必须绑定生产者类别/实例、稳定的 WorkItemId、带类型的源 EventRef/MemoryRef 血缘、Scope、请求摘要、根项/父项，以及观察到的清单 epoch。只有在 D 返回持久化回执且适用的 inventory seal 有效之后，E 才能执行。未知或新发现的生产者路径必须停止准入，并使受影响的完成证明失效。

## 2. JF-02 — 授权门禁绑定

E 向最终门禁提供精确的 action、principal/actor、artifact、源血缘、ScopeRef、WorkItemId、AttemptId、LeaseEpoch、DependencySetDigest 和 fence generation。门禁必须使用 I 权威签发的 CommitAuthorizationReceipt，并将其绑定到这些精确值、PermissionEpoch、撤销水位、策略版本、audience、expiry 和 nonce。

缓存策略结果、过期 epoch、过期许可、不匹配的 Scope，或无法证明撤销排序的情况，都必须拒绝。E 不得签发或延长授权。许可必须在实际可见性线性化点之前持续满足提交/撤销序列化协议；仅在进入 PublishGatePending 时验证是不够的。如果 I 无法提供此保证，E 必须让制品保持私有并报告 blocked/unknown，绝不能标记为 Published。

## 3. JF-03 — 冻结输出清单

任何输出提交依赖注册或发布之前，E 都必须为根 WorkItem 持久化冻结一个 `OutputManifestVersion` 及其摘要。清单必须枚举每个输出槽/ArtifactId、预期基数或封闭发现标记、子 WorkItem、DerivationRunId 和血缘关系。输出按制品分别发布；这不意味着所有输出具有原子可见性。

任何新增输出、子项、摘要变化或依赖变更都必须创建新的清单版本，并使先前的依赖完整性证据和根终态证据失效。E 必须重新打开、重建并重新冻结清单；不允许原地修改。根终态要求最终冻结清单中的所有输出均有终态处置，所有子项和执行尝试均已记账，且不存在未知提交结果或仍然有效的过期工作器路径。

## 4. JF-04 — 未知结果与幂等恢复

对于每个 D/Storage 操作，E 必须在推进本地状态之前持久化精确的幂等键、请求摘要和返回回执。ACK 丢失/超时会使状态转为 `OutcomeUnknown`；E 使用相同键和摘要向权威方查询。不得为了绕过不确定性而创建新的 WorkItemId、独立于 AttemptId 的操作键、依赖键或发布键。

只有已确认的回执或已确认的拒绝才能解决该状态。如果权威方不可用或无法证明结果，E 必须保持非终态、让字节保持私有，且不得发出 Published。重复响应投递必须幂等；相同键/不同摘要属于冲突。

## 5. JF-05 — 所有消费者路径遵循权威可见性

E 的生产者成功状态、编译器索引、事件流、outbox 通知和派生制品查找都不是可见性权威。只有在权威 PublicationReceipt 已提交之后，E 才能发出下游通知。每个 E 所有的读取器/消费者都必须在使用/响应时重新检查权威可见性和适用 fence；过期索引或事件重放不得使已抑制制品复活。E 必须传播 ArtifactId、摘要、血缘和发布回执，使消费者能验证同一对象。消费者专属强制执行仍归其 Owner 负责；E 不声称 F/G/H 已符合要求。

## 6. JF-06 — Restore 与重放安全

在工作器、队列、数据库或对象存储恢复后，E 必须先对账 D 当前 Forget 控制水位、当前清单 epoch、工作/尝试/租约账本、冻结输出清单、依赖回执、可见性回执以及 I 授权/撤销水位，然后才能恢复工作。恢复出来的队列项不是执行授权。过期租约 epoch、过期 fence 观察值或未知发布结果都必须隔离。

对象字节必须保持私有，直至当前门禁成功。恢复出来的 Published 标记不可信，除非其回执和摘要能与当前控制账本对账一致。如果无法证明控制状态连续性，E 必须停止发布并保持 recovery-blocked。

## 7. E 生命周期细化

增加 `OutputManifestOpen`、`OutputManifestFrozen`、`OutcomeUnknown` 和 `RecoveryBlocked` 作为明确的持久化状态（或等效的类型化子状态）。它们都不是终态。只有最终不可变输出清单加上每个输出的持久化终态回执，才能关闭根义务。DLQ、超时、队列删除、工作器死亡、租约过期和对象存储中存在对象，都仍然是非终态。

E36 竞态/故障/重放/恢复测试仍为 **NOT RUN**。本文记录的是语义，不是可执行实现。

## 8. 第一轮自审关闭 — JF-07 / JF-08

### JF-07 — 清单转换是持久化屏障事件

E 必须针对根 WorkItemId 持久化每次输出声明、关闭发现、冻结、重新打开和终态请求，并使用单调递增的 OutputManifestVersion 和不可变摘要。E 在依赖某次转换之前，必须取得 D 对每个与屏障相关转换的持久化回执。冻结与终态请求通过 D 的共享权威进行竞争：终态化必须指明精确的最终冻结版本/摘要；先发生的清单变更会迫使终态化重新评估，而已提交的终态处置会拒绝后续变更。若终态化之后发现新的独立输出，必须先将其作为新的关联子 WorkItem 准入，再进行任何处理；绝不能悄悄挂到已终态根项上。E 本地清单状态不是权威。

### JF-08 — Unknown 不等于否定

除非权威协调器返回带有已完成决策屏障游标的 NOT_COMMITTED 结果，否则 E 必须将缺少回执、空查询结果、超时、副本延迟和协调器不可用视为 OutcomeUnknown。E 必须将该游标与结果一并持久化。结果未知时不得生成新的幂等键；只允许使用相同键/摘要重放或进行权威查询。未解决的结果会阻止 Published 和根终态。

### JF-09 — 将每次发布尝试绑定到当前清单和输出清单

对于每个依赖注册和最终发布请求，E 都必须包含 Forget 域所要求的精确 InventorySealReceipt / ProducerDomainInventoryEpoch，以及当前冻结的 OutputManifestVersion/摘要。如果 inventory epoch 变化、清单重新打开，或在可见性提交前出现更新的清单版本，E 必须刷新清单和输出清单，按需重建依赖完整性，并使用绑定到新不可变请求的新操作键重新提交；此前暂存的字节仍必须保持私有。先前成功的 PublishGatePending 检查或依赖回执，不能授权针对已被替代清单或 inventory seal 的可见性。

## 9. Phase 3.6 部署配置文件消费决策

E 接受 Storage 选定的 **每个 Canonical Memory Authority 使用单一事务数据库，并配备每权威协调器/可串行化事务** 作为首选逻辑部署配置。E 保留现有顺序：Producer Registration → 私有暂存 → 完整依赖/清单注册 → 最终 Publish Gate → 原子可见性/PublicationReceipt → 终态处置。

E 的队列、租约、重试、DLQ、重放、重新编译和 outbox 都不是准入、可见性或终态的权威。D 的持久化 WorkItem 回执必须先于入队/租约/源解引用/执行；最终可见性提交必须使用所选权威事务，以及精确的当前 fence/清单/inventory 和 I 授权证明。CAS 仅是事务内保护条件；必须存在 Work Ledger；outbox 是同一事务内的通知机制。

本接受是逻辑消费者映射，不是可执行 E API、数据库部署或独立 Storage 工程批准。仓库中没有 E runtime、构建/测试框架、迁移或数据库配置。E36-01..20 仍为 NOT RUN。

**I 外部依赖仍为 BLOCKED：**尚未提供获批的 I ProducerDomainInventoryEpoch/InventorySeal 或可用于提交的 PermissionEpoch/撤销接口。缺失、过期或未知证明出现时，E 必须保持私有/非终态。I Owner 请求记录在仓库 Issue #4。

## 10. I Phase 3.6 技术契约刷新 — CommitAuthorizationReceipt

E 采用当前 I 所有的 `CommitAuthorizationReceipt`，其来源为 `phase-3.6-identity-trust-policy-joint-closure.md`（观察到的 I HEAD：`8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb`，Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`）。这是受委托的技术基线；I 治理批准仍受阻，且不意味着 C/D/E/F/G/Storage 消费者已接受。

该回执是单次使用、不可转让的，并绑定 policy_domain_id、PermissionEpoch、PrincipalRef、ActorRef、action、ResourceRef、purpose、audience、ScopeBindingSet 摘要、EnvironmentRef、DelegationChainRef、operation_id、operation_payload_digest、owner_boundary 和 decision_id。E 提供精确操作身份/摘要，并将回执提交到最终发布门禁。门禁必须参与同一个 I 每域线性化排序器，该排序器负责对授权决策和撤销排序。E 记录回执 ID、I 决策 ID、排序器位置、epoch、操作摘要、Owner 事务/提交游标，以及终态结果 `COMMIT_WON`、`REVOCATION_WON` 或 `INDETERMINATE_ABORTED`。

本基线不允许离线授权租约、过期 epoch 宽限或缓存 ALLOW。如果无法访问当前 I 排序器、回执过期/不匹配/被重放，或排序结果不确定，E 必须让字节保持私有，并使 WorkItem 保持非终态。

**JF-10 — I 排序器 / Storage 提交恢复协议仍是集成阻断项。** I 技术契约规定了排序要求，但被检查的工件尚未完整定义以下恢复情形：I 排序器已记录 COMMIT_WON，而 Storage 事务/可见性提交发生崩溃或 ACK 丢失。E 不会自行发明跨 Owner 事务协议。I + Storage 必须定义持久化关联、幂等查询、Owner 提交证明，以及排序器和 Owner 事务双方的对账机制。在该机制被定义并测试之前，E 不能确认 Published。
