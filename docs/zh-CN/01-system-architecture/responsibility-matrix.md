---
document_metadata:
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Owner-authorized classification direction for AID-2026-11-26-GOV-DOC-01; not a formal approval record. Pre-metadata content blob: 4faff448e34b01963d5b04e1356d9ba8d1a08a85. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Subsystem responsibility matrix"
    canonical_scope_id: architecture/subsystem-responsibility-matrix
    canonical_scope_keywords:
      - primary-owner
      - supporting-owner
      - responsibility
      - capability
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "01-system-architecture/responsibility-matrix.md"
    en: "docs/en/01-system-architecture/responsibility-matrix.md"
    zh-CN: null
---
# 子系统职责矩阵

- 文档 ID：SYS-RESP-001
- 版本：1.0
- 源规范：[项目规范性原文](../../../01-system-architecture/responsibility-matrix.md)
- 源版本：85548fcee05b28f8c2d54d4c0a8bf77840c8cdf3
- 对应英文：[Subsystem Responsibility Matrix](../../en/01-system-architecture/responsibility-matrix.md)
- 状态：DECIDED（职责基线）；明确列出的详细边界问题仍为 OPEN

标记说明：**P** = 主责组件；**S** = 协作组件；**—** = 不负责。矩阵列是能力/组件标签，不是 Owner A–I 身份。

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

## 能力到 Owner 的权威交叉映射

上方能力列属于组件分类，不是 Owner 身份。P/S 单元格只描述组件参与关系。权威 Owner 映射如下：

| 能力列 | 主责 Owner | 协作 Owner | 权威边界 |
|---|---|---|---|
| Domain Model | B | D、E、G | B 拥有领域语义和身份含义；持久化/生命周期执行仍由 D 负责。 |
| Canonical Store | D | B、E、F、G | D 拥有 Canonical Memory 机制；B 定义含义；E 提交候选写入；F/G 消费规范状态。 |
| Lifecycle | D | B、I | D 拥有 Canonical 生命周期转换；I 拥有全局策略约束、授权及 Retention/Legal Hold 策略。 |
| Entity/Relation | B | D、E | B 拥有身份和关系语义；D 持久化规范状态；E 可提出派生关系。 |
| Ingestion | E | D、I、H、C | E 拥有接收流程；D 拥有规范事务机制；I 负责授权；H 负责协议；C 负责 Agent 侧映射。 |
| Extraction | E | B、D | E 生产候选项；B 定义领域语义；D 控制 Canonical 接纳。 |
| Evidence | E | B、I、D | E 管理证据/来源链生产；B 定义语义引用；I 管理策略/授权；D 拥有规范生命周期。 |
| Consolidation | E | B、D、I | E 转换候选项；B 拥有语义；D 拥有规范提交/生命周期；I 提供策略约束。 |
| Retrieval | F | D、B、G | F 拥有检索；D 仍是 Canonical 权威；B 定义语义；G 拥有 Context 边界。 |
| Activation | F | G、C、D | F 拥有激活策略；G 拥有 Context Version 权威；C 负责 Agent 边界集成；D 拥有规范状态。 |
| MCM | G | F、D、C、H | G 拥有 Memory Context 语义/版本；F 提供检索/激活输入；D 拥有 Canonical 身份；C/H 执行 Adapter/协议边界。 |
| Sync | 联合：G（交付意图/状态）、H（Wire 与 ACK 语义）、C（Agent 侧应用） | D、F | 整条路径不存在单一 Owner。G 不拥有 BMCP Wire 语义；H 不拥有 Context 含义；C 不选择 Canonical Memory。 |
| Governance | I | D 及所有执行 Owner | I 拥有全局授权、Retention/Legal Hold、外部副本策略、目标清单和完成标准；各 Owner 执行本地约束；D 拥有 Canonical Forget 机制。 |
| Consistency | 联合/按契约确定；无唯一主责 Owner | 按具体契约由 A、B、C、D、E、F、G、H、I 参与 | 事务、重放和恢复权威按契约分配。Owner A 协调跨 Owner 冲突；不发生笼统的领域权威转移。 |

共享职责明确保持联合归属；本交叉映射不会在权威分离时强行指定唯一 Owner。

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

## Owner 引用命名空间与验证边界

- `P` 和 `S` 仅表示主责/协作组件参与情况，均不是 Owner 角色。
- 能力列名称属于分类标签，不是 Owner 标识；引用某项能力不等于分配责任。
- 正式责任归属必须明确引用 `Owner A` 至 `Owner I`，并使用上方 Owner 交叉映射。不得使用单独 A–I 字母或未限定的能力标签作为 Owner 引用。
- 子系统标识使用 Component Map 定义的 `SYS-*` 命名空间。
- 模糊引用的自动检测由 AID-2026-081 / Issue #1237 跟踪。在检查器合并前，本规则仅供人工遵循，不代表已有自动强制执行。
