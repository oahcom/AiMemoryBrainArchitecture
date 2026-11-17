# Memory Operating System — 架构突破研究

**结论：推荐将 B 作为候选方案；尚未批准任何正式架构变更。**

## 核心判断

项目不需要完整的 Memory OS 内核。真正可能有价值的是建立一个共享资源控制平面，在并发任务之间分配有限的计算、缓存、检索和上下文容量。这个控制平面不能成为记忆身份、访问权限、Forget、Context 成员关系或模型应用状态的权威。

## 主要发现

1. Retrieval 与 Activation 应继续区分。Retrieval 回答“发现了哪些符合条件的候选记忆，证据与完整性如何”；Activation 回答“哪些候选应立即推荐、延后、排除或要求显式 Recall”。最终 Context 成员资格仍由 G 决定。
2. Context Budget 与 Cache Eviction 可以共享资源核算概念，但不能共享语义。G 的 Budget 是任务相关的语义覆盖约束；F 的 Eviction 是回收可丢弃的缓存/Working Set 投影。可以共享 ResourceVector，不能合并为一个 Eviction 状态机。
3. Working Memory 应继续作为 Runtime View，而不是新的规范存储。F Working Set 是会话级、可丢弃的；G Context 是独立版本化的受管理推理区域；Agent 规划状态又是另一回事。
4. Residency 仅适合作为临时投影元数据。不应引入持久化的全局 Residency 状态机。Canonical Lifecycle、Index Generation、Cache Presence、Working Set Membership、Context Membership、Adapter Application 必须保持为不同维度。
5. 并发任务需要按 Principal/Task 进行 Reservation、加权公平调度、最低保障额度、受限借用、等待老化、Deadline 和 Cancellation。任何任务都不能耗尽所有共享容量。
6. 通过最低保障额度和单任务上限，避免单一任务饿死其他任务。借用的容量必须能在安全阶段边界回收。
7. Forget、Permission、Security、Scope 和 Authority 必须先于排序执行硬门禁。权威状态未知或过期时，阻止受保护内容使用。资源优先级永远不等于权限。
8. 重要性变化应更新软效用和后续资源预留，并采用迟滞机制；不能改变 Canonical Lifecycle，也不能追溯修改已提交的不可变 Context Version。
9. 不同资源类别需要不同策略：交互式 Recall、显式 Recall、Context Planning、后台刷新、缓存回收、压缩和维护。
10. 只有共享分配器真正替代重复的 Reservation/Fairness 逻辑时，模块数量才会减少。完整内核反而可能增加可信计算复杂度和跨模块状态耦合。

## 三种架构方案

- A：保留 F/G 独立模块。迁移风险最低，但局部预算可能出现漂移。
- B：建立共享 Memory Resource Manager，保留 F/G 领域权责。在存在资源竞争时最平衡。
- C：完整 Memory OS 内核。复杂度最高、影响面最大，并引入新的单点故障。

## 候选资源合同

MemoryResourceRequest 声明类型化身份/Scope、任务类别、Deadline、Freshness、预算向量、最低预留、最大上限、取消引用，以及由 Owner 验证的 Permission/Forget 引用。ResourceDecision 记录批准、缩减、延后或拒绝，并给出 Reservation、资源向量和可解释的公平调度轨迹。它不是授权令牌。

## 安全与故障模型

资源管理器不是权威。F/G 必须在每次受保护读取、Context Commit 和 Delivery 边界重新验证 D/I。若资源管理器不可用，新受保护任务应延后或拒绝，除非存在明确批准的有界静态策略。任何旧 Reservation 都不能跨越 Permission 或 Forget 变化继续生效。Canonical Memory 和 Context 状态必须能独立恢复。

## 定量原型

固定随机种子的合成实验：30 个任务、720 个候选记忆、共享预算 9,000 tokens：

- Direct Top-K：Recall 0.5333，Precision 0.4741，Jain 公平度 0.8325，1 个任务饥饿。
- Rerank+Budget：Recall 0.5417，Precision 0.2863，Jain 公平度 0.8141，无任务饥饿。
- Unified RM：Recall 0.5083，Precision 0.2699，Jain 公平度 0.8554，无任务饥饿。

RM 提高了公平性，但降低了 Recall/Precision，并增加本地选择延迟（中位数 0.324ms，对比 Top-K 的 0.099ms）。这只是合成算法实验，不是真实用户行为或生产容量证据。

## 最终建议

当前继续保留 A。先建立基线监控，再将 B 作为 Shadow Mode 候选进行 Owner 审查。不要实施 C。严格保留 F/G/D/E/I/H/C 的权责边界和所有 Forget/Permission 约束。
