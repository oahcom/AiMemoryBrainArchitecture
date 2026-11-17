# Memory Operating System 架构研究（独立工作流）

**状态：** 启动基线已固定；方案与实验尚未完成。  
**基线：** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`（2026-11-18）  
**跟踪：** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## 核心问题

Retrieval、Activation、Context Assembly、Budget、Eviction、Working Set 与 Scheduling 是否重复承担“在任务约束和资源限制下选择/保留哪些记忆”的决策？能否形成统一 Memory Resource Manager，同时保留领域边界与安全硬约束？

本研究不是把 Linux 概念改名搬入 Memory Brain，而是比较不同架构的复杂度、可证明性和真实运行代价。

## 当前约束

- Memory Runtime 仍处于架构定义/可行性研究阶段；本研究不授权 Runtime 实现。
- Forget、Permission、Authority、Provenance、Freshness 等硬约束不能降级为排序分数。
- Issue #43 中的架构决策与 Owner authority 不因本研究而改变。
- 本分支不修改 F/G 或其他 Owner 的权威契约。

## 基线检查

精确读取当前 F Retrieval、G Runtime、B Domain Model、C Agent Integration，以及 Context、Activation、Budget、Eviction、Storage/Index/Cache 相关文档和测试。为每个关键来源记录 branch HEAD、path、Blob SHA、状态和读取时间。

## 方案对比

- A：保留现有 Retrieval / Activation / Context / Budget 的独立职责。
- B：统一资源决策模型，保留各领域职责与模块接口。
- C：更彻底的 Memory OS 内核，统一请求调度、驻留、预算与淘汰。

每个方案比较复杂度、正确性、延迟、吞吐、资源利用率、可解释性、并发公平性、饥饿、恢复、运维成本和迁移成本。

## 必须研究的机制

Working Set、Page Cache、Page Fault、Memory Pressure、LRU/LFU/ARC、CPU Scheduling、Cgroups、NUMA、Kubernetes Resource Requests/Limits。每种映射必须给出适用条件、失效边界和是否真的对应 Memory 语义。

## 原型实验

用固定种子合成数据比较：
1. Top-K Retrieval；
2. Retrieval + Reranking + Budget；
3. Unified Resource Manager。

至少报告 Recall、Precision、Token Efficiency、Context Redundancy、Latency、Task Coverage、Budget Utilization、Starvation、Fairness。公开数据生成、参数、运行命令和原始结果。合成数据只证明该实验设置下的机制表现。

## 安全不变量

资源管理器只能在授权候选集合中优化。Forget suppression、Permission、Authority、Scope 和 Provenance 是硬过滤条件；不能以效用分数抵消。资源管理器不得自行创造 Canonical Memory，也不得改变生命周期权威。

## 验收与交付

交付当前复杂度地图、OS 机制映射、三方案矩阵、候选请求/决策契约、可运行原型、基准结果、迁移/风险分析和双语报告。结论必须标记 DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED，并明确是否值得提出正式架构变更。
