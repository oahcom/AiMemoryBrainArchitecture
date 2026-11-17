# ABR-INTEGRATION-005 — Forget 跨 Owner 有限状态模型独立复核

- 审查编号：ABR-INTEGRATION-005
- 被审查模型：reviews/architecture-breakthrough/integration/model/forget_cross_owner_model.py
- Model Blob：d45807b0b165e53aa6e92d211c221cc93b46ca60
- Test Blob：64ee823eb1d3d81e020e73ef97817208326f42b5
- README Blob：c7dc620b3486e496de1792147cbf441a51cb3af0
- 历史 CI：run 44136327645，SUCCESS，精确测试提交 89a680bbad7246952d51c61c137b0c3611f52a06。该记录不是本次后续报告提交的 CI 结果。
- D 源：session-d-memory-brain-2026-11-16 / 03-memory-brain/forget-fence-operation-and-publication-gate.md，Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5
- I 源：session-i-security-governance-2026-11-16 / 09-security-governance/global-forget-target-inventory-and-completion-evidence.md，Blob 9100061fa986fb6676656169de3fcf9fc1c72664
- Storage 源：session-storage-consistency-forget-atomicity-2026-11-16 / reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md，Blob 2ab899ee37a18ae6c8f2f64dbb82ad6499842060

## 1. 结论

跨 Owner 模型比 Session A 的单 WorkItem 抽象有明显进步，显式覆盖 D Admission/Fence High-water、E Work/Attempt/Lease/Dependency、I PermissionEpoch 与撤权排序、Storage Visibility、F Read Disclosure、Inventory Gap、Restore High-water 和 Lost-ACK Receipt Replay。已有模型及回归测试记录了有限 CI PASS：深度 14 内 27,472 个 state/depth pairs，11 个削弱约束变体产生反例。

**裁定：有条件接受为有限研究模型；不能作为全系统 Forget 证明。**

有三个实质性缺口，必须先修正模型范围或补足模型，不能让当前 global_complete 状态被误认为 I 的正式 Completed。

### M-01 — Global completion 抽象越界

complete_global 转移只检查 Fence、Barrier、inventory_complete 和没有打开的 I participant。它没有检查 I 的完整 typed evidence vector、目标清理、F/G/H 消费边界抑制、外部副本处置、Backup/Restore 安全、物理擦除证据或 PolicyException 有效性。

I 当前 Global Forget 合同要求所有强制目标/组件均 Confirmed、没有未解决 Unknown/Failed、Restore 安全且必要的物理擦除证据成立。模型 README 已诚实声明多项内容未建模，但 global_complete 这个名称容易被误读为 I 的 Completed。

**要求：** 将状态改名为 core_barrier_ready 等明确限定范围的谓词；或者补齐 I 的 typed evidence vector、CompletedWithPolicyException、Failed、Reopened 及证据失效规则。

### M-02 — 已登记但从未启动的 WorkItem 没有正常终态路径

存在合法前缀：WorkItem 已持久登记，随后 Fence 安装，但 Worker 尚未执行 run，且没有 I participant。

此时：
- terminalize 因 i_decision 为 NONE 而拒绝；
- resolve_no_publication 因没有打开的 I participant 而拒绝；
- close_barrier 因 WorkItem 不是 TERMINAL 而拒绝；
- 唯一能把 i_decision 设为 REVOCATION_WON 的路径是实际 revoke 操作，不能为了清理队列而伪造一次撤权。

**要求：** D/E/Storage 定义并授权 cancel_before_execution / no_publication_proof 的持久化终态证据、身份、幂等和旧 Worker fencing；A 只能在 Owner 合同明确后建模。另一种选择是明确承认 Barrier 必须保持打开，直到外部权威终态证明到达，并把该外部输入纳入模型。

这是活性/恢复缺口，不是已发现的安全不变量反例；不得通过放宽 fail-closed 来修复。

### M-03 — 模型只允许一个 Fence Generation

install_fence 拒绝第二次 Fence。模型没有探索两个重叠 Forget、多个 target set、最大适用 generation、独立 operation barrier、晚发现 lineage 和并行 reconciliation。

README 已声明 overlapping targets 不在范围内。因此本轮结果不能证明多 Forget 操作的组合性或单调性。

## 2. 当前模型确实支持的结论

在声明的抽象和假设下，模型为以下事项提供了有用证据：
- Admission-first / Fence-first 两种排序；
- Publication-first / Fence-first 两种排序；
- I COMMIT_WON 与 Revocation-first；
- Dependency Registration 是 Visibility 前置条件；
- UNKNOWN I participant 阻止 Barrier 关闭；
- DLQ 不是终态；
- Inventory Gap 会重新打开已关闭的 Barrier；
- 最终 Read Gate 能阻止 stale cache disclosure；
- Restore 只有重放模型内 D-local Fence High-water 后才可释放；
- Lost ACK 不回滚 durable receipt；
- 11 个故意削弱约束变体的最短反例。

stale_cache negative control 的区分是有价值的：缓存字节过期本身不等于披露，只要最终 Read Gate 仍阻断；stale_cache_disclosure 变体才证明 Fence/Revocation 后的实际读取违规。

## 3. 与 Owner 原始合同的核对

### D Terminality / Barrier

当前 D 合同要求 timeout、lost ACK、expired lease、missing receipt、registry gap、DLQ state 或不可用的最新 Fence/Permission 均保持 unresolved 并阻止 Barrier closure；所有输出必须有 durable published receipt 或无法再发布的 durable suppressed/quarantined disposition；所有 Dependency/Publication 操作已解决；不存在可继续发布的 retry、DLQ replay、delayed worker、outbox 或 staged publisher；没有 UNKNOWN ACK/participant 或 inventory gap。只有满足这些条件，D 才能提交 terminal receipt 并关闭 barrier item。

模型覆盖了其中多项条件，但没有为“已登记、从未启动”的 work 提供正常 terminal proof。M-02 是缺失转移/权威输入，不是要求弱化 fail-closed。

### I Global Completion

当前 I 合同区分 D per-operation work-item barrier、I ProducerDomainInventoryEpoch/封存的 Producer-Recipient inventory，以及 E/F/G/H、外部副本、Backup/Restore、物理擦除的逐目标证据。I 的状态机包含 CompletionEvaluated、Completed、CompletedWithPolicyException、Failed、Reopened。

I 明确禁止在 D Barrier 未关闭、Lease unresolved、Inventory 不完整、E/F/G/H 证据缺失或过期、Delivery pending、Adapter Unknown、外部接收方无 ACK/Exception、Restore 不安全或物理擦除证据缺失时进入 Completed。

因此模型的 inventory_complete Boolean 不是 I Inventory Seal，global_complete 也不是 I 的 Completed；必须明确命名范围。

### Storage / JF-10

Storage 合同要求 D、I 两个独立 participant 绑定同一个 Storage Visibility Participant 和 PublicationOperationId/digest；UNKNOWN 时两个 authority barrier 保持打开且 Artifact Private。当前模型抽象了 I/Storage outcome，但没有真实 prepared transaction ID、WAL/MVCC/2PC 恢复、D/I/Storage 独立持久账本，亦没有覆盖每个 prepare/commit 边界的 crash injection。因此不能关闭 JF-10。

## 4. 必须补充的模型任务

| ID | 任务 | 责任 Owner | 验收证据 |
|---|---|---|---|
| M-01 | 将 global_complete 改为 scoped core predicate，或补齐 I typed evidence vector、CompletedWithPolicyException、Failed、Reopened 和 evidence invalidation | A 建模；I 拥有语义 | 任一强制组件缺失/Unknown/过期均阻止 I Completed |
| M-02 | 增加 pre-execution cancel/no-publication proof，定义 authority、durable identity、幂等和 late-worker fencing | D/E/Storage；A 仅在合同明确后建模 | Registered → fenced → never started → durable no-publication terminal proof → barrier closure；旧 Worker 不得发布 |
| M-03 | 至少建模两个重叠 Forget 操作、target/lineage sets、独立 barriers 和最大适用 D generation | D/I；A 建模 | 排列测试证明一个操作不能降低/抹除另一个操作的 Fence 或完成义务 |
| M-04 | 对 Registration、Dependency Commit、D participant admission、I receipt consume、Storage prepare/visibility commit、outcome propagation、D/I closure 增加 crash cut points | Storage/D/I | Crash/restart 矩阵；UNKNOWN 持续 Private 且 Barrier 保持打开，直到精确 participant 结果确定 |
| M-05 | 将 liveness/fairness 与 safety invariants 分开；定义哪些转移依赖外部 Owner 响应，哪些可以无限期保持 blocked | D/E/I/Storage | 明确 progress assumptions 与 bounded deadlock/recovery tests；公平性假设不得把 UNKNOWN 变成成功 |

## 5. 结果解释

- 现有 bounded CI PASS：**仅对该精确模型和测试集有效**。
- Session A 的 606 state/depth-pair 模型：较小的历史抽象；被当前模型在部分跨 Owner 场景扩展，不因此失效。
- Cross-owner model：**有条件的研究证据**。
- D/E/I/Storage 合同组合：**部分建模；Owner 接受和物理实现仍开放**。
- JF-10 / 物理 crash atomicity：**NOT PROVEN**。
- Global Forget completion：**当前模型不足以表达，NOT PROVEN**。
- Architecture freeze：**NOT READY**。

保留现有模型及其 CI 历史，不删除或改写历史证据。Gate 使用模型前，必须处理 M-01、由 D/E/Storage 定义 M-02、补充 M-03；M-04 仍归 Storage/D/I 的物理验证，M-05 单独审查。

本报告是同一集成会话对模型的复核，不是 D/E/I/Storage Owner 独立批准；不修改 Owner authority contract，不授权实现、合并、部署或生产激活。
