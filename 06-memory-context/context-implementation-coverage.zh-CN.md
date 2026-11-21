# Memory Context 实现覆盖率映射

- Work Item：GAP-02 / GAP-BASELINE-001
- Owner：G — Memory Context Architect
- 提示词：CHATGPT-OWNER-G-001 v1.0
- 源树：`1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- 交付分支：`gap-02-context-coverage-reference-model`
- 状态：实现映射；不自我批准
- 范围：指定 SHA 下 `06-memory-context/` 的 19 个 Markdown 文件（README、17 份不同的英文设计/评审文档，以及 Phase 3.8.22 合同的中文对应文件）。Phase 3.8.22 中英文文件属于同一语义合同，不重复计算独立要求。

## 1. 状态定义

- **IMPLEMENTED**：指出可执行函数/类型，并列出已有或新增测试名。仅表示所指参考模型行为可执行。
- **PARTIAL**：已有可执行行为，但文档中的某个维度、状态或证据边界尚未覆盖。
- **NOT IMPLEMENTED**：尚无可执行模型覆盖该关注点。第四列说明是 G 本线程可做，还是依赖外部权威/实现。
- **PENDING CROSS-OWNER DECISION**：必须由 G 以外的 Owner 裁定；本交付不修改其他 Owner 的合同。

Rust crate 刻意停留在 private/staged 阶段：不做持久化、传输、授权、D/I 查询或发布。Python Applied Ledger 是单节点 SQLite 符合性原型，Gate 由调用方提供。新增 Context 模型是内存模型，不是持久化事务实现。三者均不构成生产级并发或端到端交付。

## 2. 源文件清单

| # | 源文件 | 基线 Blob |
|---:|---|---|
| 1 | `README.md` | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` |
| 2 | `context-architecture.md` | `56fcc0ea112d423ef69a3f00e9d626bf4230ca0e` |
| 3 | `context-budget-and-sufficiency.md` | `a2f96a88f3123862ea263da11366dda4207d5b0a` |
| 4 | `context-edit-operations.md` | `10c94e85dfe89d20dcdb202cafc2bef767f076fc` |
| 5 | `context-manager.md` | `ecc0549137a1738c197d02d12d94a1eb971ed6b5` |
| 6 | `context-reconciliation.md` | `87063aceebed1c30b7840045ada8e3f348732688` |
| 7 | `context-versioning.md` | `1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b` |
| 8 | `phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| 9 | `phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | `25c1da1f6769165881d217bb0bb492a997e0e14c` |
| 10 | `phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` |
| 11 | `phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` |
| 12 | `phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | `0910fea807b96a896e361cd2722e4c94df55187b` |
| 13 | `phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `c1de241ec69834377d9b0e24aa4770a809796d4b` |
| 14 | `phase-3.8.4-g-c-provider-outcome-consumer-review.md` | `b29160ac66fa8e989675f57fddb216aaec874f8a` |
| 15 | `phase-3.8.5-g-storage-logical-serialization-topology-impact-review.md` | `0e93acea1ebd7f1e6e86b429ef3ad2a652052c41` |
| 16 | `phase-3.8.6-g-review-storage-serialization-anchor.md` | `edc4c7210a0706381ba3eb3efd87119c2ad8721e` |
| 17 | `phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | `1894860c76336f8739d354b72beed3992cffd17e` |
| 18 | `phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | `833815e37ac8d7505d93a0a115421dafe3eb08ad` |
| 19 | `phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | `47423d6f95e613b2f1556f5e359da85d7820617b` |

## 3. 逐关注点映射表

| 关注点 | 设计出处（文件 + 章节） | 当前实现状态 | 阻塞归属 |
|---|---|---|---|
| README 范围、索引和 Owner 边界 | README §1–§4 | PARTIAL — 仅索引，无独立可执行行为；以下条目为实际依据 | 不在范围 |
| Brain 拥有的期望 Context 成员与 Canonical Memory 分离 | context-architecture.md §1–§2 | PARTIAL — 有 `ContextEntry`、`ContextSnapshot`；无 canonical-store adapter；测试 `serializes_snapshot_and_prepares_non_sendable_delivery_intent` | D |
| Context 身份绑定 Scope、Agent、实例、Session、Task、Environment 和 Purpose | context-architecture.md §3 | PARTIAL — `ContextIdentity::validate`；正向间接覆盖 `build_sorts_by_tier_then_priority_then_entry_id`；缺少 Environment 缺失/歧义专门测试 | I |
| 环境相关身份必须 Fail-Closed | context-architecture.md §3 | NOT IMPLEMENTED — Rust Environment 字段可选，未实现环境依赖判定 | I |
| P0–P3 仅是优先级，不是信任或指令等级 | context-architecture.md §4、§6 | PARTIAL — 有 `ContextTier` 和候选排序；测试 `build_sorts_by_tier_then_priority_then_entry_id`；无下游指令边界执行 | I |
| Planner 消费授权候选，F 拥有检索与排序 | context-architecture.md §5、§9 | PARTIAL — `build_context` 消费调用方候选；无 F adapter 或检索实现 | I |
| Editor、Versioner、Reconciler、Budget Manager、Delivery Coordinator 是逻辑模块 | context-architecture.md §5 | PARTIAL — 有预算/快照/Delivery 基础类型，无模块级工作流 | 本线程可做 |
| Entry 保留结构化来源、认知限定和生命周期 | context-architecture.md §6 | PARTIAL — `ContextCandidate`/`ContextEntry` 保留来源/证据/限定字段；测试 `rejects_missing_lineage_and_empty_content`；无来源授权校验器 | D |
| Memory 内容不得成为指令或工具授权 | context-architecture.md §6 | NOT IMPLEMENTED — 数据结构不执行下游 Prompt Region 隔离 | I |
| Context、Entry、Delivery 生命周期分离 | context-architecture.md §7 | PARTIAL — 有 Context/Delivery 基础类型，缺少三套独立状态机 | 本线程可做 |
| Forget/撤权 Tombstone 阻断活动及待处理投影 | context-architecture.md §8 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| Adapter 按 Session 清除状态及 Reconnect | context-architecture.md §8 | NOT IMPLEMENTED — 无 Adapter/Session Runtime | 不在范围 |
| Budget 是向量而不是单一 Top-K | context-budget-and-sufficiency.md §1–§2 | PARTIAL — `ContextBudget` 检查 Entry 数和渲染字节；测试 `enforces_entry_and_byte_budgets_without_truncation`；缺 Token、Fan-out、来源深度、延迟、CPU、Tier 预留 | 本线程可做 |
| 任务特定 Sufficiency 覆盖十个维度 | context-budget-and-sufficiency.md §3 | NOT IMPLEMENTED — 无 Requirement Graph 或逐维评估器 | D |
| 规划保留必需锚点、证据、冲突和不确定性 | context-budget-and-sufficiency.md §4 | PARTIAL — 有候选准入和稳定排序；无 Requirement Graph 优化器或冲突覆盖测试 | D |
| 在向量约束下优化候选集边际覆盖 | context-budget-and-sufficiency.md §5 | NOT IMPLEMENTED — 无优化器/压缩器 | 本线程可做 |
| Compaction 保留 Lineage、限定和冲突 | context-budget-and-sufficiency.md §5、§9.3 | NOT IMPLEMENTED — 无 Compaction 模型或 Fidelity Validator | D |
| Sufficiency 结果和安全溢出降级 | context-budget-and-sufficiency.md §6–§7 | NOT IMPLEMENTED — 无 Sufficient/Conditional/Insufficient/Unknown 评估器或溢出规划器 | 本线程可做 |
| Budget/Sufficiency 可观测性 | context-budget-and-sufficiency.md §8–§9.4 | NOT IMPLEMENTED — 无 Metrics/Report 模型 | 本线程可做 |
| ChangeSet 公共封套、前置条件和全有或全无暂存 | context-edit-operations.md §1 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | 本线程可做 |
| Add 精确 Canonical Ref、Lineage 和重复防护 | context-edit-operations.md §2 Add | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| Update 仅修改 Context 元数据/渲染，不修改 Canonical Memory | context-edit-operations.md §2 Update | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | 本线程可做 |
| Remove 仅移除成员，不执行 Canonical Forget | context-edit-operations.md §2 Remove | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| Replace 原子替换并保留旧成员 Tombstone | context-edit-operations.md §2 Replace | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| Reorder 要求精确覆盖同一 Context 的成员集合 | context-edit-operations.md §2 Reorder | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | 本线程可做 |
| Expire 移除活动成员并保留 Tombstone | context-edit-operations.md §2 Expire | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | 本线程可做 |
| Compact 操作和 Lineage 安全输出 | context-edit-operations.md §2 Compact | NOT IMPLEMENTED — 模型中没有 Compact 操作 | D |
| Reconcile 操作和补偿 ChangeSet | context-edit-operations.md §2 Reconcile | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| 操作冲突、审计和错误分类 | context-edit-operations.md §3–§5 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | I |
| Context Manager 组件责任边界 | context-manager.md §1–§2 | PARTIAL — 有数据原语和参考流程；无 Coordinator/Ports/Services | D |
| Manager 主流程：身份、授权、加载、消费、校验、规划、编辑、提交、交付、协调、观测 | context-manager.md §3 | PARTIAL — Build 和本地 ChangeSet 部分存在；无可执行端到端流程 | D |
| T1 Context 原子提交 | context-manager.md §4 | NOT IMPLEMENTED — 内存 ChangeSet 不等于持久化原子事务 | 本线程可做 |
| T2 Delivery Attempt 与 T1 分离 | context-manager.md §4 | NOT IMPLEMENTED — 仅有 Private Intent，无发送/重试状态 | 不在范围 |
| T3 Adapter Application 是外部行为 | context-manager.md §4 | NOT IMPLEMENTED — 无 Adapter Apply | 不在范围 |
| T4 Reconciliation 是可恢复 Saga | context-manager.md §4、§6 | PARTIAL — 只有单条目分类，无持久化 Saga Journal | D |
| F 协作：候选是提案，不完整不等于不存在 | context-manager.md §5 | PARTIAL — 有候选输入；无 F 接口/Watermark 向量 | 不在范围 |
| 故障行为和错误分类 | context-manager.md §6、§8 | PARTIAL — 有部分 Fail-Closed 错误；缺少完整错误目录和隐私安全投影 | I |
| 状态所有权与可观测性 | context-manager.md §7、§9 | NOT IMPLEMENTED — 无生产 Metrics/Traces | D |
| Reconciliation 触发器和权威信号归属 | context-reconciliation.md §1–§2 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| Stale/ReconcileRequired/Reconciled/Blocked/Closed 区分 | context-reconciliation.md §3 | PARTIAL — 有 Entry 分类；无 Context/Run 状态机 | 本线程可做 |
| Reconciliation 算法：触发、精确 Context、先 Tombstone、加载、授权、Canonical 校验、水位比较、分类、补偿、CAS、Delivery、审计 | context-reconciliation.md §4 | PARTIAL — 有条目分类和本地 ChangeSet/CAS；其余流程未执行 | D |
| Forget/撤权失效和 Adapter Target 状态 | context-reconciliation.md §5 | PARTIAL — 仅内存 Tombstone；无持久化 Target Evidence 或 Adapter Clear | D |
| Offline Reconnect、缓存失效和安全替换 | context-reconciliation.md §5–§6 | NOT IMPLEMENTED — 无 Reconnect/Adapter Runtime | D |
| Reconciliation Audit 和 Typed Cursor 分离 | context-reconciliation.md §7–§9 | NOT IMPLEMENTED — 无持久化 Run Record/向量验证器 | D |
| 不可变 ContextVersion 和 ChangeSet 历史 | context-versioning.md §1–§4 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | 不在范围 |
| Context/Entry/Delivery/Applied 对象分离 | context-versioning.md §5–§6 | PARTIAL — 有 Snapshot 和 DeliveryIntent；无持久化 Context/Applied 对象 | 本线程可做 |
| Snapshot/Delta 语义及精确 Base 应用 | context-versioning.md §7 | PARTIAL — 有 JSON Snapshot 序列化；测试 `serializes_snapshot_and_prepares_non_sendable_delivery_intent`；无 Delta Apply/Replay 模型 | D |
| CAS、幂等、原子 ChangeSet、禁止隐式合并 | context-versioning.md §8 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | 不在范围 |
| Delivery 生命周期、迟到 ACK 和 Supersession | context-versioning.md §9 | NOT IMPLEMENTED — 无 Attempt Ledger/ACK 消费者 | 本线程可做 |
| Rollback、补偿和 Replay | context-versioning.md §10 | PARTIAL — 有 Tombstone 和内存历史；无持久化 Replay/Rebuild | D |
| Full/Partial/Bypassed/Unknown 覆盖语义 | context-versioning.md §11、§14.3 | PARTIAL — Applied Ledger 要求调用方 Gate 全部为真；无完整 Region 提取或 Coverage Proof | D |
| Typed Cursor 分离和 Producer Admission | context-versioning.md §13.1–§13.2 | NOT IMPLEMENTED — 无 D 注册或 Typed Cursor Validator | D |
| 受保护发布顺序和原子可见性 Gate | context-versioning.md §13.3 | NOT IMPLEMENTED — 当前没有已接受且可执行的跨 Owner Gate。 | D |
| Applied 状态机和精确证据映射 | context-versioning.md §14.1–§14.4 | PARTIAL — `GAppliedLedger.evaluate`；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_non_accepted_c_outcomes_never_create_applied`、`test_missing_or_failed_authority_gate_blocks_commit`；Gate 由调用方提供，无当前使用重验证 | D |
| Applied 幂等、冲突和重启读回 | phase-3.6-applied-forget-reconciliation-contract.md §Applied；phase-3.8.22 §4–§6 | IMPLEMENTED — `GAppliedLedger.evaluate`、`read`、`conflict_count`；测试 `test_same_identity_and_same_evidence_is_idempotent`、`test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`、`test_restart_reads_original_record_and_replay_returns_same_id` | 不在范围 |
| Forget/撤权后 Historical Applied 与 Current Use 分离 | phase-3.6-applied-forget-reconciliation-contract.md §Current Use；phase-3.8.22 §8 | PARTIAL — 有 `current_use_allowed`；测试 `test_current_use_requires_every_currentness_gate`；无持久化失效事件或 Owner 查询 | D |
| COC JF-10 Bridge、Recovery Batch 和因果 Terminal Proof | phase-3.6.2 §1–§4；phase-3.6.3 §1–§4 | NOT IMPLEMENTED — 当前没有已接受且可执行的跨 Owner Gate。 | 不在范围 |
| PreparedParticipant/GID/Native XID 和 Visibility Receipt Join | phase-3.6.4 §1–§6 | NOT IMPLEMENTED — 当前没有已接受且可执行的跨 Owner Gate。 | D |
| Context Serving 前的 Restore Reconciliation | phase-3.6.5 §1–§4 | NOT IMPLEMENTED — 无 G Restore/Replay 集成；Restore Receipt 不能授权 Serving | D |
| Local Lifecycle、Producer/Derivative、Queue、Recall、Context、Restore 状态 | phase-3.7 §1–§8 | PARTIAL — ChangeSet/Reconcile 参考部分存在；无持久化 Producer/Queue/Recall/Restore Ledger | D |
| 入队/租约/读取受保护源之前完成 Producer Registration | phase-3.7 §2、§10.1 | NOT IMPLEMENTED — 无 D Producer Registry Receipt 或 Queue Admission | D |
| 可见前完成 Derivative Dependency Registration | phase-3.7 §3、§10.1 | NOT IMPLEMENTED — 无 Dependency Receipt 或 Publication Gate | D |
| Delivery Queue Attempt 身份、重试和 ACK 分离 | phase-3.7 §4 | NOT IMPLEMENTED — 无持久化 DeliveryId/Attempt Ledger | 本线程可做 |
| Recall 候选 Canonical 校验和 Sufficiency | phase-3.7 §5 | PARTIAL — Rust 候选校验和 Reconciliation 模型存在；无 F Watermark 向量或实时 D/I 重验证 | D |
| Context 与 Applied 生命周期分离 | phase-3.7 §6 | PARTIAL — 模型区分 Context Version 与 Applied Ledger；无集成状态机 | 本线程可做 |
| Restore/Reconnect 隔离及当前状态协调 | phase-3.7 §7 | NOT IMPLEMENTED — 无 Restore Fence、Ledger Replay 或 Adapter Reconnect | D |
| 必需竞争/故障符合性矩阵 | phase-3.7 §8–§9 | PARTIAL — 新增 14 个本地测试和 8 个 Applied 测试；无多 Owner 确定性竞争 Harness | D |
| C Provider Outcome × SideEffect 映射 | phase-3.8.4 §1–§6 | PARTIAL — Applied Ledger 拒绝非接受结果；测试 `test_non_accepted_c_outcomes_never_create_applied`；无 SideEffect 维度或 C Record 验证 | 不在范围 |
| Storage Logical Serialization Topology 与可见对象准入 | phase-3.8.5 §1–§4 | NOT IMPLEMENTED — 当前没有已接受且可执行的跨 Owner Gate。 | D |
| Per-authority Storage Serialization Anchor 不等于 ContextVersion/AppliedCursor | phase-3.8.6 §1–§4 | PARTIAL — 仅文档区分；无 Typed Runtime Validator | 本线程可做 |
| H Unified 1.2.14 × CSubmitOutcome 1.0.1 Full-path 精确 Join | phase-3.8.18 §1–§7 | PARTIAL — Applied 原型仅有粗粒度证据映射；无生产 Schema Digest/签名/Authority Callback 验证 | D |
| Outcome/SideEffect 矛盾、UNKNOWN 和 IN_DOUBT | phase-3.8.18 §2–§4 | PARTIAL — C Outcome 粗粒度 Fail-Closed；无成对 SideEffect 状态机 | 本线程可做 |
| Applied Identity/Evidence Revision 唯一性和不可变冲突 | phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md §3–§5 | PARTIAL — 有单 Identity/单 Digest 冲突模型；无独立 Evidence Revision 序列/Source Pin | D |
| Applied 原子提交和唯一约束 | phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md §5 | PARTIAL — `GAppliedLedger` 有 SQLite 事务和主键；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_same_identity_and_same_evidence_is_idempotent`；不保证多副本 | 不在范围 |
| Crash/Retry/Restore Fencing 和 Current-use 失效 | phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md §6–§8 | PARTIAL — 重开读回测试 `test_restart_reads_original_record_and_replay_returns_same_id`；无进程崩溃注入、Restore Fence 或 High-water 协调 | D |
| Machine-readable Applied Record 和对抗符合性 | phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md §9–§11 | NOT IMPLEMENTED — 无生成 Schema/SDK 或完整 18 项 Durable Crash Suite | D |
| 既有 8 项 Applied 参考模型证据 | phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md §13；phase-3.8.22 ZH 对应章节 | IMPLEMENTED — `GAppliedLedger`；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_same_identity_and_same_evidence_is_idempotent`、`test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`、`test_non_accepted_c_outcomes_never_create_applied`、`test_missing_or_failed_authority_gate_blocks_commit`、`test_restart_reads_original_record_and_replay_returns_same_id`、`test_different_logical_identity_gets_a_distinct_record`、`test_identity_requires_exact_typed_field_set` | 本线程可做 |


## 4. 本次范围与测试证据

本交付仅为覆盖率映射，不新增代码或测试。评估对象为 mainline 当前可见实现；未合并分支中的 `ContextLedger`/`reconcile_entry` 模型不计入当前实现。`crates/memory-context/src/lib.rs` 有 7 个单元测试：`build_sorts_by_tier_then_priority_then_entry_id`、`rejects_cross_scope_candidates`、`rejects_forgotten_and_superseded_lifecycle`、`rejects_duplicate_membership_and_entry_ids`、`enforces_entry_and_byte_budgets_without_truncation`、`serializes_snapshot_and_prepares_non_sendable_delivery_intent`、`rejects_missing_lineage_and_empty_content`。Python Applied Ledger 参考模型有 8 个既有测试：`test_new_complete_success_commits_one_full_applied_record`、`test_same_identity_and_same_evidence_is_idempotent`、`test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`、`test_non_accepted_c_outcomes_never_create_applied`、`test_missing_or_failed_authority_gate_blocks_commit`、`test_restart_reads_original_record_and_replay_returns_same_id`、`test_different_logical_identity_gets_a_distinct_record`、`test_identity_requires_exact_typed_field_set`。测试名称来自源文件；本轮未运行测试。

## 5. 评估边界

`IMPLEMENTED` 仅表示表中明确列出的函数/结构体与测试所覆盖的参考行为；不代表生产持久化、分布式并发、跨 Owner 授权、Adapter 交付或端到端完成。`PARTIAL` 明确列出缺失维度。`NOT IMPLEMENTED` 不代表不可实现；阻塞归属仅指出下一责任边界。
