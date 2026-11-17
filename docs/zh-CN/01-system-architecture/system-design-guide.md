# 系统设计指南——原则、交互与质量

- 文档 ID：DOC-SYS-DESIGN-001
- 版本：1.0
- 源规范：00-governance/design-principles.md 和 01-system-architecture/*
- 对应英文：[System Design Guide](../../en/01-system-architecture/system-design-guide.md)
- 状态：解释性指南；详细源规范仍具有权威性

## 1. 如何理解系统架构

系统架构描述逻辑职责和契约，不会自动规定进程边界、微服务或 Rust Crate。组件图中的一个方框代表“系统存在这项职责”，不代表“必须将它部署成独立服务”。

组件通过明确契约交互。一次交互可以是进程内调用、持久化消息、数据流或协议请求；具体部署拓扑是单独的工程决策。

## 2. 16 项架构设计原则

| ID | 原则 | 实际含义 |
|---|---|---|
| P-01 | Brain 对记忆拥有权威 | Brain 拥有 Canonical Memory、Lifecycle、Provenance、Relation 和自己管理的 Context |
| P-02 | 独立于 Agent 和模型 | 不依赖某个 Agent 框架、模型系列/供应商、Prompt 格式或推理 API |
| P-03 | Brain 定义契约 | Adapter 将 Agent 原生状态映射到稳定的 Brain 契约 |
| P-04 | 明确领域语义 | Event、Memory、Fact、Entity、Relation 和 Evidence 不可互换 |
| P-05 | 从设计上保留 Provenance | 派生记忆必须保留来源和派生链路 |
| P-06 | 时间语义正确 | Event Time、记录/接收时间和 Valid Time 必须区分 |
| P-07 | 意图不等于结果 | 没有结果证据时，Plan/Prediction/Pending Action 不能成为已完成结果 |
| P-08 | Canonical Memory 与 Context 分离 | Context 是有 Scope 的视图；编辑 Context 不修改权威记忆 |
| P-09 | 在推理边界同步 | Context 变更在定义明确的后续上下文组装边界生效 |
| P-10 | 明确的应用 ACK | Delivery、Receipt 和 Applied 不同；Applied 不证明模型关注 |
| P-11 | Memory 是数据，不是指令 | Memory 不能获得 System/Developer 权限或覆盖 Agent 安全策略 |
| P-12 | Scope 隔离 | User/Project/Agent/Session/Environment 边界必须明确 |
| P-13 | 受治理 Forget | Context 移除不等于删除；Forget 覆盖适用派生物和备份 |
| P-14 | 保留冲突 | 冲突 Claim 保留来源、时间、认知状态和解决历史 |
| P-15 | 性能必须实测 | 延迟、检索质量、资源消耗和 Agent 收益必须可复现测量 |
| P-16 | 先定义逻辑架构 | 职责边界不自动意味着进程/服务/Crate 边界 |

## 3. 组件交互规则

1. 主责 Owner 定义语义和权威状态。
2. 协作组件可以校验、转换、传输或缓存，但不能建立竞争性权威。
3. 每个外部边界都必须检查身份、Scope、Permission、Schema 和资源限制。
4. 异步工作必须具备持久化关联和重试语义。
5. 状态变更重试必须在声明的幂等 Key 范围内满足幂等性。
6. MCM 串行化 Context Version 变更；Synchronization 只跟踪 Delivery，不拥有 Context 语义。
7. ACK 只能表达实际观察到的内容。

## 4. 主要数据流

### 从经历到权威记忆

~~~text
Agent / Environment / User
        ↓
Gateway 和已授权 Event Ingress
        ↓
持久化 Event + Accepted Receipt + Compile Intent
        ↓
Compiler 校验、规范化、提取
        ↓
Evidence / Provenance / 候选资产
        ↓
D Canonical Lifecycle 和 Version Commit
        ↓
Index 和 Projection 发布
        ↓
Runtime 可检索
~~~

### 从记忆到推理上下文

~~~text
Agent Telemetry / Recall
        ↓
授权和 Scope 解析
        ↓
带 Evidence/Freshness 的 Retrieval Candidate
        ↓
Activation Recommendation
        ↓
G Context 规划和版本提交
        ↓
H Delivery Protocol
        ↓
C/H Adapter 在下一次推理上下文组装边界应用
        ↓
Applied Attestation（仅在证明条件满足时）
~~~

### Forget 与撤销

~~~text
已授权请求
        ↓
I 身份和策略检查
        ↓
D 持久化 Forget Fence / Target Inventory
        ↓
E/F/G/H/Storage 各目标抑制和清理
        ↓
逐目标证据和例外评估
        ↓
I 全局完成决策
~~~

## 5. 同步与异步工作

| 交互 | 默认方式 | 原因 |
|---|---|---|
| 身份/Schema/Permission 校验 | 边界同步执行 | 不允许未授权操作继续 |
| 可靠 Event 接收 | 同步直到持久化 Receipt | 调用方需要真实接收结果 |
| 语义编译 | 异步 | 模型延迟/故障不能阻塞事件接收 |
| Index/Cache 传播 | 异步 | 它们是派生且可重建的数据 |
| 显式 Runtime Recall | 有界同步请求/响应 | Agent 需要及时获得候选 |
| 后台主动 Recall | 异步候选 | 不阻塞 Agent 任务循环 |
| Context Version 提交 | MCM 原子操作 | 保持唯一权威版本序列 |
| Context Delivery | 异步 | Adapter 可能离线 |
| Applied ACK | 推理边界应用后产生，再异步报告 | 证据必须晚于实际应用 |
| Forget 传播 | 持久化分阶段流程 | 涉及多个目标清理和恢复 |

## 6. 系统级故障隔离

| 故障 | 预期隔离行为 |
|---|---|
| Gateway 不可用 | 外部操作不可用；Canonical 数据不变 |
| Ingestion/Storage 故障 | 未完成可靠持久化不得返回 Accepted Receipt |
| Compiler/模型故障 | Accepted Event 保持持久化并等待重试 |
| Canonical Store 故障 | 停止 Canonical Mutation，不得虚报成功 |
| Index/Cache 故障 | 明确降级或安全回退；Canonical 仍是权威 |
| Retrieval 故障 | 返回明确超时/部分结果，不推断 Context 已变更 |
| MCM 故障 | 不产生新 Context Version；最后已提交版本仍有效 |
| Sync/Adapter 故障 | Delivery 保持待处理，不得虚报 Applied |
| Governance 故障 | 受保护操作 Fail Closed |
| Recovery/Observability 故障 | 不得静默违反审计或一致性义务 |

## 7. 质量优先级

Brain 必须在真实 Agent 工作流中作为记忆基础设施评估，而不是只看向量搜索 Benchmark。优先级为：

1. 正确性和认知完整性。
2. Scope 隔离、授权和隐私。
3. Canonical/Context 一致性与可恢复性。
4. Provenance 完整性和受治理 Forget。
5. 可预测延迟和有界资源消耗。
6. Adapter 互操作性和演进能力。
7. 可用性和故障隔离。
8. 有用的记忆激活和可测量的 Agent 收益。
9. 可运维性、可观测性和可测试性。

这些目标可能存在权衡。例如，更严格的 Provenance 和授权可能增加延迟；缓存能降低延迟，但可能增加陈旧风险；更大的 Context 可能提升覆盖，也可能消耗更多 Token 并分散 Agent 注意力。

## 8. 测量规则

在明确代表性负载和硬件基线之前，数值预算保持 OPEN。每次 Benchmark 必须声明硬件、软件版本、模型/量化方式、语料、Scope 分布、并发、查询类型、缓存状态、到达率、持续时间、正确性标注、样本量和百分位计算方法。

应测量 Ingestion 持久化、Compilation 队列年龄/阶段延迟、Recall p50/p95/p99、Activation 误报/漏报、Context 提交冲突和 Token Budget、Delivery/Applied 延迟、授权延迟、Forget 抑制延迟、CPU/RAM/Disk/GPU/VRAM、Provenance 覆盖率、Scope 泄漏和 Agent 收益。

没有可复现对比时，任何性能倍数或质量提升都不能作为架构事实。

## 9. 验收方法

采用分层验证：
- Contract Test：Schema、职责归属、状态和兼容性。
- Invariant/Property Test：不可妥协的语义约束。
- Integration Test：跨组件顺序。
- Concurrency Test：版本和竞态安全。
- Fault Injection：崩溃/恢复和故障隔离。
- Security Test：隔离、授权和 Prompt Injection。
- Performance Test：延迟、吞吐量和资源边界。
- Agent Task Evaluation：端到端实际收益。
- Governance Test：Forget、Retention、Backup 和外部接收方。

## 10. 详细源规范

- [设计原则](../../../00-governance/design-principles.md)
- [组件交互](../../../01-system-architecture/component-interactions.md)
- [数据流](../../../01-system-architecture/data-flows.md)
- [系统边界](../../../01-system-architecture/system-boundaries.md)
- [系统质量属性](../../../01-system-architecture/system-quality-attributes.md)

本指南是面向读者的综合说明，不替代详细契约，也不声称尚未测量的指标已经达到。
