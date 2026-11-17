# 迁移影响与分阶段采用

## 建议

不要把 F/G 迁移成统一内核。只有在架构研究评审之后，才引入薄型共享分配合同。第一阶段可以是现有 Modular Monolith 内的 Library/Module，不需要新增 Service。

## 阶段 0——不改变架构

- 保留 F Retrieval、Activation、Scheduling 和 Working Set。
- 保留 G Context Planner、Budget Manager、Versioning/Committer 和 Reconciler。
- 记录 Decision ID、预计/实际资源用量、Queue Wait、Task Allocation 和 Sufficiency Outcome。
- 建立基线负载与竞争指标。

退出条件：证明资源核算重复发生在哪里，以及任务是否实际饥饿或超出共享预算。

## 阶段 1——共享术语和 Trace

增加候选公共值对象：ResourceVector、ResourceRequest、ResourceReservation、ResourceDecision、ResourceUsage。不引入共享可变状态。F/G 仍分别决定自己的资源。

退出条件：双语 Schema Review、精确 Owner 接受、Identity/Accounting/无跨 Scope 复用属性测试。

## 阶段 2——咨询式分配器原型

使用 Weighted Fair Queueing/Deficit Round Robin 分配 CPU、RAM、Candidate/Fan-out 和 Latency。G 仍分配 Token/Byte Context Budget。RM 只提出 Task Token Reservation，G 验证并提交。Shadow Mode 对比现有决策。

退出条件：公平性/饥饿改善有实测证据，同时 Recall、Task Coverage、p95 Latency、Forget Suppression 和 Authorization 不退化。

## 阶段 3——有限采用

RM 只负责 Admission 和 Reservation。F 保留 Retrieval/Activation/Cache；G 保留 Context Sufficiency/Commit。PermissionEpoch/ForgetFence 过期或不可用时失败关闭。静态 Principal Quota 只能作为明确批准的降级方案。

退出条件：Concurrency、Cancellation、Restore、Lease Expiry、Policy Change、Forget Race 和 Authority Outage 符合性测试通过。

## 阶段 4——仅凭证据重新评估

只有当共享分配器被证明无法协调所需资源时，才通过独立 ADR 重新考虑更广泛的 Memory OS Kernel。必须证明总复杂度更低，且不引入新的关键单点故障。

## 破坏性变更风险

- Resource Request Schema 可能变成事实上的跨 Owner 权威接口。
- Token Cost Estimate 可能与 H 最终 Tokenizer/Rendering 不同；G 必须按实际物化 Context 成本核算。
- F/G 独立重试可能重复 Reservation，必须区分 Idempotency 与 Attempt Identity。
- 中央 Scheduler 可能成为瓶颈或故障放大器。
- 跨任务公平性可能与紧急用户任务冲突；Service Class 必须由策略定义且受边界限制。
- 新增 Residency Flag 可能被误认为 Lifecycle/Permission，必须避免全局持久 Residency。
- 资源压力不能静默丢弃必需 Evidence、Uncertainty、Provenance 或 P0 Context Anchor。

## 回滚

关闭 RM Admission 集成，回到 F/G 本地 Scheduler，并使用保守的 Principal 静态配额。不得回滚或重写 ContextVersion、Canonical Memory、Forget Evidence、PermissionEpoch 或现有 F/G 状态机。
