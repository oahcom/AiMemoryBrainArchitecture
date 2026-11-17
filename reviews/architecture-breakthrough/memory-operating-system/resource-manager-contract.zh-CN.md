# Memory Resource Manager——候选合同

**状态：CANDIDATE / NOT APPROVED。** 本合同是研究提案，不修改 F/G 合同，也不授权生产实现。

## 1. 权威模型

Resource Manager（RM）是协调/控制平面，不是 Memory Authority。

- F 拥有 Retrieval、Ranking/Fusion、ActivationRecommendation、Runtime Session、Working Set 和 F Cache。
- G 拥有 Context 成员、排序、Sufficiency、ContextVersion、ChangeSet、Compaction 和 Delivery Intent。
- D 拥有 Canonical Memory 身份/版本/生命周期及 ForgetFence。
- I 拥有授权、PermissionEpoch 和治理策略。
- E 拥有规范发布/索引投影语义。
- H/C 拥有 Adapter 与最终推理边界证据。

RM 不得创建、重新解释或覆盖任何上述决策。

## 2. MemoryResourceRequest

必需字段：
- request_id、idempotency_key、schema_version；
- principal_ref、policy_domain_ref、tenant_ref；
- agent_ref、agent_instance_ref、session_ref、task_ref、environment_ref（类型化不透明引用；必需性由 B/I 解析）；
- purpose、resource_class（interactive_recall、context_plan、background_refresh、maintenance）；
- 请求资源向量：tokens、bytes、candidate_count、evidence_bytes、graph_nodes/fanout、CPU units、memory bytes、I/O units、max_parallelism；
- latency_deadline、cancellation_ref；
- task_importance、service_class（未经过策略映射前均为不可信提示）；
- freshness_requirement、required canonical/index fences；
- access_scope_ref、authorization/Forget epoch references（仅证明引用，RM 必须重新验证）；
- minimum reservation、maximum cap、borrowable、estimated cost、cost-model version。

## 3. ResourceDecision

字段：
- decision_id、request_id、policy_version、decision_timestamp；
- outcome：admitted | admitted_with_reduction | deferred | rejected | cancelled | expired；
- reservation_id、granted resource vector、queue position/class；
- fairness/aging explanation、竞争 quota bucket IDs（不透明）；
- approved degradation steps、typed omissions；
- owner handoff plan（F Retrieval Budget、G Context Budget、Delivery Budget）；
- decision trace hash/reference、expiry 和 revalidation points。

任何 outcome 都不代表授权。没有决策时，受保护读取应拒绝/延后，不能默认放行。

## 4. Resource Ledger 与 Scheduler

- Ledger 按 Principal、Task、Session、Resource Class 和时间窗口记录 Reservation/Usage。
- 先在 Principal 间使用 Weighted Fair Queueing 或 Deficit Round Robin，再在 Principal 内部按 Task 调度；为交互工作和每个已准入活动任务保留少量保障额度。
- Background Refresh/Maintenance 使用独立低优先级池，可被抢占。
- 未使用 Reservation 可在 Lease/Expiry 下借用，并在安全阶段边界回收。
- Aging 防止饥饿；Deadline-aware Scheduling 只调整合格工作顺序，不能绕过 Quota 或硬门禁。
- 单任务最大上限防止资源垄断。
- 需求超过容量时，返回明确 Deferred/Rejected/Partial 与重试提示，不能声称覆盖完整。
- Reservation 只预留计算/容量，不代表某条记忆的独占所有权。

## 5. 硬门禁（不可协商）

在候选排序、Cache Hit、Compaction、Context Publication 或 Delivery 之前：
1. 已认证 Principal 与解析后的类型化 Scope；
2. 当前 I Authorization / PermissionEpoch；
3. 当前 D ForgetFence 与完整适用 Lineage；
4. Canonical Memory/Version Lifecycle、Temporal Validity 和 Source Access；
5. Classification 与 Evidence/Provenance Access；
6. Environment/Task Binding 和 PolicyDomain 一致性。

任何未知、过期、缺失或不可用的权威状态，都必须阻止受保护数据使用。RM 只传递不透明引用并请求 Owner 验证。Priority、Task Value、Relevance、Budget Availability 和 Cache Residency 都不能替代授权。

## 6. 分配阶段

1. 接收 Request 并预留有界执行资源。
2. F 检索 Scope-filtered Candidates，返回 Channel Completeness 和每个 Index/Partition 的 Watermark。
3. F Activation 评估合格候选的适用性并输出有理由的建议。
4. G 重新验证 Candidate Identity/Version 和当前 D/I 权威，建立 Task Requirement Profile。
5. RM 仲裁共享 CPU/RAM/Token/Latency 包络及 Fairness Reservation；G 仍是最终 Context Allocator 和 Sufficiency Authority。
6. G 在现有 Commit 与 D Publication Gate 下提交版本化 Context ChangeSet。
7. H 在推理边界应用；G/C/H Evidence 语义不变。
8. 释放/过期 Reservation，记录实际用量和预测误差。

## 7. 故障行为

- RM 不可用：不能依据过期 Grant 准入受保护操作。只有显式配置且仍经 F/G/I/D 重新验证的有界静态配额，才可作为降级路径。
- Ledger 不可用/损坏：拒绝或延后新分配，不推测容量。
- Request/Lease 过期：取消并协调；迟到结果不能写入 Working Set/Cache，也不能在缺少当前 Owner 检查时发布 Context。
- Cancellation：传播到子 Retrieval/Evidence Task；稳定 Request Identity 与 Attempt Identity 分离。
- 必要 Context 超预算：G 返回 Insufficient；RM 不能静默截断必要覆盖。
- Index/Authority 部分故障：返回类型化 Partial/Unknown，不得声称完整。

## 8. 可观测性与符合性

指标：Queue Wait、Admitted/Deferred/Rejected、Reservation vs Actual Vector、Principal/Task Share、Starvation Age、p50/p95/p99 Stage Latency、Budget Utilization、Candidate/Context Coverage、Omissions、Forget Suppression、Cache Hit/Miss、Jain Fairness Index。

符合性测试：Request Identity/Idempotency、Quota Isolation、Starvation/Aging、Cancellation、Borrowing/Reclaim、Authority Outage Fail-closed、Retrieval 中 Forget、Permission Epoch 变化、Context Insufficiency、跨 Scope 泄漏、过期 Lease Restore、Allocation Ledger 确定性 Replay。

## 9. 明确排除

RM 不存储 Memory Content，不拥有全局 Residency 状态机，不执行 Cache Eviction，不修改 Canonical Memory，不决定 Retention/Forget，不裁决 Conflict，不构建 Prompt，也不授权 Agent 行为。
