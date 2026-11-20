# 子系统职责矩阵

- 文档 ID：SYS-RESP-001
- 版本：1.0
- 源规范：[项目规范性原文](../../../01-system-architecture/responsibility-matrix.md)
- 源版本：85548fcee05b28f8c2d54d4c0a8bf77840c8cdf3
- 对应英文：[Subsystem Responsibility Matrix](../../en/01-system-architecture/responsibility-matrix.md)
- 状态：DECIDED（职责基线）；明确列出的详细边界问题仍为 OPEN

标记说明：**P** = 主责 Owner；**S** = 协作参与者；**—** = 不负责。

| 能力 / 关注点 | Domain Model | Canonical Store | Lifecycle | Entity/Relation | Ingestion | Extraction | Evidence | Consolidation | Retrieval | Activation | MCM | Sync | Governance | Consistency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 权威对象语义 | P | S | S | S | — | S | S | S | S | — | S | — | S | — |
| 可靠事件接收 | S | S | — | — | P | — | — | — | — | — | — | — | S | S |
| 候选内容提取 | S | — | S | S | S | P | S | S | — | — | — | — | — | — |
| Provenance/Evidence 关联 | S | S | — | S | S | S | P | S | S | — | S | — | S | — |
| Entity 身份和类型化关系 | S | S | — | P | — | S | S | S | S | S | S | — | S | — |
| Consolidation/冲突处理 | S | S | S | S | — | S | S | P | — | — | S | — | S | S |
| Canonical 生命周期转换 | S | S | P | S | — | S | S | S | S | — | S | — | S | S |
| 候选记忆检索 | S | S | — | S | — | — | S | — | P | S | S | — | S | S |
| 激活决策 | S | — | S | S | — | — | S | S | S | P | S | — | S | — |
| Context 规划/编辑/版本管理 | S | S | — | S | — | — | S | S | S | S | P | S | S | S |
| Context 投递/确认 | — | — | — | — | — | — | — | — | — | S | S | P | S | S |
| Scope/Permission 执行 | S | S | S | S | S | S | S | S | S | S | S | S | P | S |
| Forget/Retention 治理 | S | S | S | S | S | S | S | S | S | — | S | S | P | S |
| 入站幂等与 Receipt 重放 | — | S | — | — | P | S | — | — | — | — | — | — | S | S |
| 跨组件重放、协调与恢复 | — | S | S | S | S | S | S | S | S | S | S | S | S | P |
| Metrics/Tracing/审计关联 | — | S | S | S | S | S | S | S | S | S | S | S | S | P |

## 职责归属规则

1. 主责 Owner 定义其能力的契约和状态转换。
2. 协作组件可以提供数据或执行子步骤，但不得建立相互竞争的事实来源。
3. Governance 是横切执行责任；每个子系统仍必须在自己的边界执行本地检查。
4. Context Manager 拥有 Context Version 权威；Synchronization Engine 负责 Delivery 跟踪，不拥有 Context 语义。
5. Canonical Store 拥有持久化机制；Domain Model 拥有语义和有效性规则。
6. Compiler 负责提出和转换记忆；Canonical Lifecycle Policy 决定候选内容是否以及如何成为权威记忆资产。
7. Retrieval 返回候选及证据；Activation Policy 决定候选是否进入 Context。
8. Agent Adapter 在推理边界应用 Context，但不成为记忆选择或 Canonical Memory 的权威。
9. 幂等性职责分层：Event Ingestion 负责入站去重和原始 Receipt 语义；Event Store 负责 Event 与编译意图的原子持久化；Consistency/Recovery 负责跨组件重放、协调和恢复。精确幂等身份字段仍由专门的幂等契约规定，本文不重新定义。

## 需要在详细设计中解决的边界问题

- Lifecycle Policy 是独立模块，还是 Canonical Domain Services 的一部分。
- Entity Resolution 按事件类型采用同步、异步还是混合方式。
- 哪些 Consistency 操作属于共享协调器，哪些属于子系统本地 Transactional Outbox。
- Protocol Gateway 是独立逻辑子系统，还是 BMCP 服务的 Facade。

这些问题仍是待解决的设计问题，本矩阵不擅自替它们作出决议。
