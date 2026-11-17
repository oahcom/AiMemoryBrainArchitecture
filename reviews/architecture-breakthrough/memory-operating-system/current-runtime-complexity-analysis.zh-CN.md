# 当前 Memory Runtime 复杂度分析

- 状态：仅供研究/候选，不构成 Owner 决策或实现授权。
- 基线：main `b3c666e67982cb3d3374e759cfb6552c7765aacb`；F 分支 HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`；G 分支 HEAD `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`。
- 控制事项：Issue #43。F/G 源规范来自 Owner 分支实时读取，本报告不替代它们。

## 执行结论

当前设计的职责分离具有实际意义，并非简单的意外重复。F 负责 Recall 执行、Retrieval、排序/融合、Activation Recommendation、请求调度以及可丢弃 Working Set/Cache。G 负责目标 Context 的成员关系、排序、多维 Budget/Sufficiency、不可变 Context Version 和 Delivery Intent。D/E/I/H/C 仍分别掌握规范记忆、发布、授权、Adapter 和推理边界权威。

重复风险主要集中在资源决策及其信号：F 候选/延迟/CPU/RAM 预算、F Working Set/Cache 容量与淘汰、F Activation 成本/紧迫性、G Token/Byte/Count/Latency Budget、G Tier Reservation、G Compaction/Deferred Entry，以及 C/H 边界遥测。它们使用相似的 Cost、Urgency、Freshness、Deadline、Capacity 概念，但管理的是不同资源和不同状态所有者。

## 已观察到的源规范事实

1. F RetrievalResult 表示发现与证据结果；ActivationRecommendation 是立即纳入/延后/排除建议。两者都不会创建 G Context 成员。
2. F Scheduler 已定义有界 Admission、按 Principal/Scope 并发限制、交互/后台资源池、Quota、Cancellation、Backpressure 和 Fairness 候选机制。
3. F Working Set 是可丢弃、会话隔离的视图/缓存，不是 Canonical Memory、G Context 或 Agent 规划状态。Cache Hit 必须重新验证当前授权与 Forget。
4. G Budget Manager 已采用向量：Token、Byte、Entry/Ref 数、Relation/Provenance 上限、Latency、Refresh、CPU 和 Compaction 成本。Sufficiency 是任务相关的多维判断，不是 Top-K。
5. G 将 F 候选作为不可变提案消费，再重新解析 Canonical Version/Lifecycle 和 I/D 授权/Fence。G 拥有 Context 成员关系与版本。
6. G Context Budget 与 F Runtime Memory Budget 不是同一种资源：前者限制受管理推理区域，后者限制临时执行和缓存内存。
7. 现有 F anti-resurrection 测试是逻辑参考模型测试，不是物理 Adapter、生产拓扑或性能证明。F 技术审查明确要求先对索引后端与数值限制做基准测试。

## 复杂度分布

| 关注点 | F 权责 | G 权责 | 重复风险 | 建议 |
|---|---|---|---|---|
| 候选发现 | Retrieval/路由/融合 | 消费候选 | 低 | 保留 F |
| 候选适用性 | Activation Recommendation | 最终决定 Context 成员 | 中 | F 解释候选效用；G 决定 Context |
| Token/Byte Budget | 仅成本估算 | 受管理区域硬预算 | 中 | 共享类型化成本模型；G 保留最终分配权 |
| CPU/RAM/Fan-out/Deadline | Runtime Scheduler | Planning/Commit/Delivery 延迟约束 | 中 | 共享资源包络；阶段预算独立 |
| Working Set/Cache | F 所有 | G 所有 Context Snapshot/Cache 影响 | 中 | 保留 F 临时视图，不新增 Context Store |
| Eviction | F 可丢弃 Cache/WS | G 延后/移除 Entry/压缩 Context | 高，容易混淆语义 | 分别命名：Cache Reclaim 与 Context Membership Change |
| Freshness | F Index/Channel Watermark | G Sufficiency/Source Freshness | 中 | 传递类型化向量，禁止合并 Watermark |
| Forget/Permission | 执行 D/I 当前决策 | Context/Delivery 执行 | 若错误集中化则高危 | D/I 硬门禁不能交给 RM |
| Residency | F 本地缓存状态 | G Context Lifecycle 与 H Applied 状态 | 全局化后风险高 | 不建立全局持久 Residency 状态 |

## 主要设计问题

- F 排序后 G 拒绝，再由 F 重新检索和排序，可能缺少统一的决策轨迹。保留独立权威，但增加共同 Decision Trace ID 和明确反馈。
- Token 估算可能在 F、G 重复计费。明确成本归属：F 估算仅供参考；G 按目标 Tokenizer/Rendering Profile 对已提交 Context 实际计费。
- “Eviction” 可能混淆 Cache 删除、Working Set 移除、Context 延后、Context Entry 移除和 Canonical Forget。它们不能共享命令或终态。
- F 已有请求级 Fair Scheduling，但 G 的 Context 容量如何在并发任务间共享仍需要桥接。任务级 Reservation Ledger 可以解决分配问题，而不接管 F/G 的领域状态。
- 源文档没有证明代表性负载下存在实际重复、延迟或利用率问题。没有基准测试前，不应声称当前架构低效。

## 基线判断

当前 F/G 分工在概念上成立。最合适的目标不是合并职责，而是共享资源分配合同和调度策略：协调 Request、Reservation 与 Fairness，同时让 Retrieval、Activation 语义、Context 状态和安全权威继续由原 Owner 掌握。

## 精确源版本

- F Retrieval：`05-memory-runtime/retrieval-engine.md`，Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`。
- F Activation：`05-memory-runtime/activation-policy-engine.md`，Blob `b7f5d85468f5262e472769a1991b812ac4a64f5b`。
- F Scheduling：`05-memory-runtime/runtime-scheduling.md`，Blob `ca35d8cddd012c1ff067328ee22177f57c40ae36`。
- F Working Set：`05-memory-runtime/working-set-and-cache.md`，Blob `a934491950c876701e8ac592a0e6aaea983b44e3`。
- G Context Architecture：`06-memory-context/context-architecture.md`，Blob `56fcc0ea112d423ef69a3f00e9d626bf4230ca0e`。
- G Budget：`06-memory-context/context-budget-and-sufficiency.md`，Blob `a2f96a88f3123862ea263da11366dda4207d5b0a`。
- G Manager：`06-memory-context/context-manager.md`，Blob `ecc0549137a1738c197d02d12d94a1eb971ed6b5`。
- B Domain Model：`02-domain-model/domain-model-overview.md`，Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`。
- F 逻辑测试：`tests/anti_resurrection/test_f_runtime_model.py`，Blob `c2575327a75577923440ef770d42122218a1e091`。
