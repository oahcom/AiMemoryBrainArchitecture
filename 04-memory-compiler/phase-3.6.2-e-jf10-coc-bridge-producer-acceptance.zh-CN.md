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
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.2-e-jf10-coc-bridge-producer-acceptance.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-2-e-jf10-coc-bridge-producer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-2-e-jf10-coc-bridge-producer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — 精确 JF-10 ↔ COC 桥接的生产者生命周期接受

- Owner：E — Memory Compiler
- 分支：`session-e-memory-compiler-2026-11-16`
- 决策方式：依照用户指示，由中央会话执行委托的 E 边界审查；不构成独立的人类签署。
- A COC 架构：`reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`，Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- D/E/Storage 共同 JF-10 协议：Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- Storage 精确 JF-10 套件接受：`reviews/storage-consistency/forget-atomicity-storage-realization-review.md`，Blob `107d21bd2c604ee0b04feff2ee5580e1de9c7fce`
- D fence/发布门禁：Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- I JF-10 v2 处置：Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`
- E 编译器状态/准入基线：Blob `e59f517fff161ab882aa0ddc4a5bda513964ae1a`
- E Forget fence/派生注册基线：Blob `00e37ba56596e710513c8d0568acd79141d9101b`
- 日期：2026-11-17
- 决策：**在列明条件下接受 — 仅限 E 生产者生命周期**

## 1. 决策

E 接受精确的 JF-10 ↔ COC 桥接，作为编译器发起的派生发布的生产者侧生命周期契约。E 的接受范围仅限稳定生产者身份、不可变清单/摘要绑定、重试/租约行为、D 注册/依赖参与，以及 E 对 Storage 发布回执的解释。E 不裁定 I 授权、D ForgetFence、Storage XID 提交/回滚、C 提供方结果、H wire 编码或 COC 共识。

## 2. E 所有的要求

1. 持久化源接收和 AcceptedReceipt 不等于 D 生产者注册、执行许可或发布。
2. 一个不可变生产者操作绑定 WorkItemId、PublicationOperationId、DerivationRunId、冻结清单摘要、规范源修订引用、精确 Owner 边界和适用的 D 血缘/fence 身份。相同身份 + 相同摘要必须幂等；相同身份 + 不同摘要是硬冲突。
3. 重试可以创建新的 AttemptId/LeaseEpoch，但必须保留 WorkItemId、PublicationOperationId、清单摘要和预分配的 Storage participant/XID 绑定。重试不得为了逃避未解决屏障而创建新的逻辑参与者。
4. E 必须在租约、解引用、执行或派生发布之前，先向 D 持久化注册生产者工作。D 的权威回执，而不是 E 本地队列或缓存，决定屏障成员资格。
5. 在 D 确认依赖注册完整且 Storage 返回权威的同操作/同 XID PublicationReceipt 之前，E 必须让暂存制品、blob、嵌入、溯源边和候选元数据保持私有。
6. 只有权威 Storage 回读证明以下内容原子提交后，E 才能报告 PUBLISHED：VisibilityPointer + PublicationReceipt + Owner outcome + receipt-consumption evidence + outbox commit。单独的 COC 观察、I COMMIT_WON、D clearance、Storage prepared receipt 或工作器成功都不够。
7. UNKNOWN/IN_DOUBT 必须保留相同操作身份和私有字节；TTL、租约过期、队列删除、移入 DLQ 或工作器重启，都不能释放 D 屏障或使制品可见。
8. 重新编译只能在同一根/源血缘和当前 D/I 检查下创建新的 DerivationRunId。它不能重置原始 Forget 截止点、改变 participant 摘要或遗漏先前注册的依赖。

## 3. E 对桥接交互的接受

E 接受 COC 是因果排序和参与者记账服务。它可以记录 E/生产者参与者生命周期观察，但不授权编译器、不决定 D 屏障完成、不决定 I 授权，也不发布 Storage 制品。E 消费各 Owner 签发的精确引用，不得强制转换其类型化命名空间。

如果编译器发起的操作受单一 I PolicyDomain JF-10 配置约束，则必须绑定一个 PolicyDomainRef。多策略域原子性仍为 BLOCKED / NOT ACCEPTED；对于无法表示在已接受单域配置内的请求，E 必须拒绝或隔离。

## 4. 例外与保留的阻断项

- E 尚未证明存在生产级编译器账本、D 注册客户端、持久化队列/outbox、工作器租约服务、制品存储或 Storage 适配器。
- 尚未实际执行端到端 E/D/Storage/I COC 参与者。
- Storage 的 PostgreSQL 18.7 CI 证据仅限定固定引擎能力和隔离参考 fixture；它不是 E 适配器集成证明。
- H 的 1.1.0 schema 候选尚未生成/互操作测试，不构成 E wire 接受。
- I 外部治理批准、ProducerDomainInventoryEpoch/InventorySeal 和 Global Forget 完成仍为 OPEN。
- JF-10 对集成实现/一致性仍为 P0 OPEN；本 E 设计接受不会关闭它。

## 5. 必需的一致性验证

E 必须测试：重复 AcceptedReceipt；相同 WorkItemId 配不同摘要；D 注册 ACK 前/后崩溃；AttemptId 更新但 PublicationOperationId/XID 稳定的重试；过期租约不得发布；部分依赖集合必须保持私有；D fence 在注册前/后的竞态；Owner 最终门禁前/后的 I 撤销；Storage PREPARE/COMMIT/ROLLBACK ACK 丢失；存在未解决参与者时恢复；同 XID 回读；fence 之后出现迟到派生项；以及重新编译不能逃离原屏障。

PASS 要求具备可执行 E 生产者/清单账本、集成的 D/I/Storage/COC 服务、确定性故障注入、权威回读和独立审查。本文仅为架构/接口接受；不声称实现、测试通过、部署或生产启用。
