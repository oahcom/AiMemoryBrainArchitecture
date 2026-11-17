# 三种架构方案比较

## 决策范围

三种方案均以当前 F/G 权责为基础。“模块”指逻辑职责，不代表进程、服务或 Rust Crate。任何方案都不得削弱 Forget、Permission、Security、Authority 或精确版本 Freshness。

## A——维持 Retrieval / Activation / Context / Budget 独立

**形态：** F Retrieval → F Activation Recommendation → G Planner/Budget/Committer → Adapter。F 保留 Scheduler 和 Cache Eviction。

- 复杂度：变更风险低，但预算/成本/公平性逻辑仍可能重叠。
- 正确性：最符合现有 Owner 合同；重复核算可能漂移。
- 延迟：协调开销最低；可能反复规划/估算。
- 吞吐：独立请求良好；F/G 配额不一致时容易出现邻居干扰。
- 内存效率：局部 Cache 控制良好，全局分配感知较弱。
- 可解释性：局部决策清晰，跨阶段理由分散。
- 并发：F 已有 Fair Scheduling；G 并发 Context 容量需要桥接。
- 扩展性：各模块独立演进；新增资源类型可能重复接口。
- 故障恢复：保留现有 F/G 恢复边界，不引入新的共享状态。
- 运维成本：迁移最低，长期集成成本中等。

适用：任务少、竞争弱，没有证据证明重复核算造成实际性能问题。

## B——共享 Memory Resource Manager，保留领域权责（推荐候选）

**形态：** 薄资源控制平面接收类型化 Request、预留预算、调度工作并输出 Decision Trace。F 仍负责 Retrieval/Ranking/Recommendation；G 仍负责 Context 成员、版本、预算充分性；D/I 仍是规范和安全权威。Manager 不拥有 Canonical Memory、Context State、Cache Content 或 Forget Completion。

- 复杂度：中等；共享合同/策略，减少重复 Reservation/Fairness 机制。
- 正确性：若 Manager 仅协调、Owner 每次重新验证则较好；若把缓存决策误当授权则有风险。
- 延迟：增加少量调度开销，可能减少反复预算协商。
- 吞吐：通过 Reservation/WFQ 改善并发竞争。
- 内存效率：改善共享 Token/CPU/RAM/Fan-out 利用率，但不保证 Recall 质量。
- 可解释性：统一 Allocation Trace，加 Owner 专属原因。
- 并发：显式 Principal/Task Quota、Reservation、Borrowing 和 Starvation 控制。
- 扩展性：新增资源/策略，不必合并领域 Owner。
- 故障恢复：Manager 故障不能丢失领域状态；受保护请求应失败关闭或使用有界静态 Reservation。
- 运维成本：中等；需要维护一套策略面和指标。

适用：多个并发任务竞争 Token、CPU、Memory、Retrieval Fan-out 或 Latency。

## C——完整 Memory Operating System 内核

**形态：** 统一内核拥有 Retrieval、Activation、Residency、Context、Budget、Eviction 和 Scheduling 状态。

- 复杂度：最高；需要迁移并协调 F/G 状态机和跨 Owner 边界。
- 正确性：可能统一策略，但会扩大可信计算基并引入权威冲突。
- 延迟：流水线可能优化，但中心协调/锁/串行化也可能成为主成本。
- 吞吐：可全局优化，但中心调度器可能成为竞争点。
- 内存效率：理论全局最优；不同资源类型使用单一效用分数存在过拟合风险。
- 可解释性：决策集中，但多目标策略可能不透明。
- 并发：可集中公平调度；单个 Scheduler 故障影响所有任务。
- 扩展性：内部 API 统一，但每个 Owner 的变更都与内核耦合。
- 故障恢复：新增单点故障；持久 Scheduler State、Epoch 和 Replay 成为关键。
- 运维成本：实现、验证和 On-call 成本最高。

适用：只有在证据证明 B 无法有效协调资源，并正式批准权责重构之后。当前不具备依据。

## 定性比较（不是基准测试数据）

| 维度 | A | B | C |
|---|---|---|---|
| 复杂度 | 当前低/长期中 | 中 | 极高 |
| 正确性 | 延续性高 | Owner 硬门禁下高 | 未证明，影响面大 |
| 延迟 | 基线最佳 | 少量开销 | 不确定 |
| 竞争下吞吐 | 中 | 预期最佳 | 潜力高但可能中心瓶颈 |
| 内存效率 | 局部优化 | 共享分配 | 理论最优 |
| 可解释性 | 分散 | 统一 Trace | 可能不透明 |
| 并发公平 | 部分 | 显式 | 集中化 |
| 扩展性 | 局部 | 强 | 强耦合 |
| 恢复 | 沿用现状 | 新控制面恢复 | 大规模新内核恢复 |
| 运维成本 | 低 | 中 | 极高 |

## 建议

将 **B 作为隔离、非权威候选**推进。不要实施 C。如果真实负载未显示多任务竞争或可测量重复，则保留 A。原型必须在相同合成负载下比较 B 与 A，并报告公平性/质量权衡，而不只是总利用率。
