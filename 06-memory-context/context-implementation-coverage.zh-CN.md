# Memory Context 实现覆盖率映射

- Work Item：GAP-02 / GAP-BASELINE-001
- Owner：G — Memory Context Architect
- 提示词：CHATGPT-OWNER-G-001 v1.0
- 源树：`b9ddd241a18a00b3b8f3b0ce2e176b6f859bc0da`
- 评估引用：`main`（只读源码核验）
- Rust 源文件 Blob：`crates/memory-context/src/lib.rs` = `8e15e7b6c279183b0adaaca0557506e305739db7`
- 实现提交：`46c4b67728db8c8b58e4d8e96b277cc75ddc1f35`；Clippy/API 后续修复：`aad4a6dff0daf5c263beaaa31b72a40347bddddf`
- 状态：实现映射；不自我批准
- 范围：指定 SHA 下 `06-memory-context/` 的 19 个 Markdown 文件（README、17 份不同的英文设计/评审文档，以及 Phase 3.8.22 合同的中文对应文件）。Phase 3.8.22 中英文文件属于同一语义合同，不重复计算独立要求。

## 1. 状态定义

- **IMPLEMENTED**：指出可执行函数/类型，并列出已有或新增测试名。仅表示所指参考模型行为可执行。
- **PARTIAL**：已有可执行行为，但文档中的某个维度、状态或证据边界尚未覆盖。
- **NOT IMPLEMENTED**：尚无可执行模型覆盖该关注点。第四列说明是 G 本线程可做，还是依赖外部权威/实现。

Rust crate 仍停留在 private/staged 阶段。Round 6 新增纯内存 `ChangeSet` 编辑器，具备 Base-Version 前置条件、全有或全无暂存、类型化错误、操作记录和成员 Tombstone。Round 7 新增任务特定 Sufficiency 结果评估器：目前只测量 Evidence Ref 和明确的 Environment Identity；不支持的维度保持 Unknown。它仍不提供持久化原子提交、传输、授权、D/I 查询、发布、Requirement Graph、候选优化器、Overflow Planner 或 Compaction。Python Applied Ledger 仍是 Gate 由调用方提供的单节点 SQLite 参考原型。两条参考路径均不构成生产级分布式并发或端到端交付。

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
| Brain 拥有的期望 Context 成员与 Canonical Memory 分离 | context-architecture.md §1–§2 | PARTIAL — 有 `ContextEntry`、`ContextSnapshot`；`delivery_intent_snapshot_json_round_trips_to_equivalent_snapshot` 验证 JSON Snapshot 往返；无 canonical-store adapter | D |
| Context 身份绑定 Scope、Agent、实例、Session、Task、Environment 和 Purpose | context-architecture.md §3 | PARTIAL — `ContextIdentity::validate`；`empty_identity_scope_purpose_and_schema_version_are_rejected` 检查必需身份字段，`candidate_scope_must_be_contained_by_identity_scope` 检查 Scope 包含关系；缺少 Environment 缺失/歧义专门测试 | I |
| 环境相关身份必须 Fail-Closed | context-architecture.md §3 | NOT IMPLEMENTED — Rust Environment 字段可选，未实现环境依赖判定 | I |
| P0–P3 仅是优先级，不是信任或指令等级 | context-architecture.md §4、§6 | PARTIAL — 有 `ContextTier`；测试 `sorting_uses_tier_then_descending_priority_then_entry_id` 验证 Tier、降序 Priority 和 Entry ID 排序；无下游指令边界执行 | I |
| Planner 消费授权候选，F 拥有检索与排序 | context-architecture.md §5、§9 | PARTIAL — `build_context` 消费调用方候选；无 F adapter 或检索实现 | I |
| Editor、Versioner、Reconciler、Budget Manager、Delivery Coordinator 是逻辑模块 | context-architecture.md §5 | PARTIAL — 有预算/快照/Delivery 基础类型，无模块级工作流 | 本线程可做 |
| Entry 保留结构化来源、认知限定和生命周期 | context-architecture.md §6 | PARTIAL — `ContextCandidate`/`ContextEntry` 保留来源/证据/限定字段；`build_context_rejects_candidates_without_lineage` 和 `build_context_rejects_whitespace_only_rendered_content` 验证输入拒绝；无来源授权校验器 | D |
| Memory 内容不得成为指令或工具授权 | context-architecture.md §6 | NOT IMPLEMENTED — 数据结构不执行下游 Prompt Region 隔离 | I |
| Context、Entry、Delivery 生命周期分离 | context-architecture.md §7 | PARTIAL — `non_active_non_consolidated_lifecycles_are_rejected` 验证候选生命周期准入；Context/Entry/Delivery 仍缺少各自独立状态机 | 本线程可做 |
| Forget/撤权 Tombstone 阻断活动及待处理投影 | context-architecture.md §8 | PARTIAL — Snapshot 内可序列化的 `ContextTombstone`；`remove_tombstone_is_visible_to_later_reconcile` 验证被移除成员不会通过 Reconcile 静默复活；仍无持久化 Tombstone-first 投影或待发送 Delivery 失效机制 | D |
| Adapter 按 Session 清除状态及 Reconnect | context-architecture.md §8 | NOT IMPLEMENTED — 无 Adapter/Session Runtime | 不在范围 |
| Budget 是向量而不是单一 Top-K | context-budget-and-sufficiency.md §1–§2 | PARTIAL — `ContextBudget` 检查 Entry 数和渲染字节；`entry_budget_error_reports_actual_candidate_count`、`byte_budget_error_reports_accumulated_rendered_bytes`、`exact_entry_and_byte_budget_boundaries_succeed` 覆盖溢出与精确边界；缺 Token、Fan-out、来源深度、延迟、CPU、Tier 预留 | 本线程可做 |
| 任务特定 Sufficiency 覆盖十个维度 | context-budget-and-sufficiency.md §3 | PARTIAL — 已有 `SufficiencyRequirement`/`SufficiencyDimension` 和 `assess_sufficiency`；当前快照字段可测量 Evidence 与 Environment，其余八个维度会正确返回 Unknown；仍无 Requirement Graph 或语义证据模型 | D |
| 规划保留必需锚点、证据、冲突和不确定性 | context-budget-and-sufficiency.md §4 | PARTIAL — 有候选准入和稳定排序；无 Requirement Graph 优化器或冲突覆盖测试 | D |
| 在向量约束下优化候选集边际覆盖 | context-budget-and-sufficiency.md §5 | NOT IMPLEMENTED — Sufficiency 评估器已落地，但尚无候选集优化器或边际覆盖选择器 | 本线程可做 |
| Compaction 保留 Lineage、限定和冲突 | context-budget-and-sufficiency.md §5、§9.3 | NOT IMPLEMENTED — Sufficiency 评估器已落地；仍无 Compaction 模型或 Fidelity Validator | D |
| Sufficiency 结果和安全溢出降级 | context-budget-and-sufficiency.md §6–§7 | PARTIAL — 四种互斥结果及 Mandatory/Advisory/Unknown 判定规则已可执行；仍无 Overflow Planner 或预算降级工作流 | 本线程可做 |
| Budget/Sufficiency 可观测性 | context-budget-and-sufficiency.md §8–§9.4 | NOT IMPLEMENTED — 无 Metrics/Report 模型 | 本线程可做 |
| ChangeSet 公共封套、前置条件和全有或全无暂存 | context-edit-operations.md §1 | IMPLEMENTED — `ChangeSet`/`apply_change_set` 绑定 `base_version`，拒绝过期 Snapshot，并在私有克隆上应用；测试 `stale_base_is_rejected_without_changing_snapshot`、`any_failing_operation_discards_the_entire_staged_set`、`change_set_rejects_duplicate_operation_ids`；仅内存，持久化 T1 单独核算 | 本线程可做 |
| Add 精确 Canonical Ref、Lineage 和重复防护 | context-edit-operations.md §2 Add | PARTIAL — 候选准入仍验证 Lineage 和重复成员；无专门 Add 操作或 Canonical Ref Adapter（Reconcile 可通过无前驱的 Replace 物化期望的新成员） | D |
| Update 仅修改 Context 元数据/渲染，不修改 Canonical Memory | context-edit-operations.md §2 Update | IMPLEMENTED — `ChangeSetOperation::Update` 只修改 Context Entry，并拒绝更改 Entry/Memory/Version 身份；测试 `update_preserves_memory_version_and_rejects_version_changes` | 本线程可做 |
| Remove 仅移除成员，不执行 Canonical Forget | context-edit-operations.md §2 Remove | IMPLEMENTED — `ChangeSetOperation::Remove` 只移除 Snapshot 成员，并追加带原因的 Tombstone；测试 `remove_tombstone_is_visible_to_later_reconcile` | D |
| Replace 原子替换并保留旧成员 Tombstone | context-edit-operations.md §2 Replace | IMPLEMENTED — `ChangeSetOperation::Replace` 在同一结果中替换暂存成员并追加旧成员 Tombstone；测试 `replace_tombstones_old_membership_in_the_same_result` | D |
| Reorder 要求精确覆盖同一 Context 的成员集合 | context-edit-operations.md §2 Reorder | IMPLEMENTED — `ChangeSetOperation::Reorder` 只接受精确排列；测试 `reorder_rejects_non_permutation` | 本线程可做 |
| Expire 移除活动成员并保留 Tombstone | context-edit-operations.md §2 Expire | IMPLEMENTED — 基于版本截止条件的 `Expire` 移除到期成员并追加 `Expired` Tombstone；测试 `expire_uses_target_version_and_preserves_expiration_tombstone` | 本线程可做 |
| Compact 操作和 Lineage 安全输出 | context-edit-operations.md §2 Compact | NOT IMPLEMENTED — Sufficiency 评估器已落地；仍无 Compact 操作或 Lineage 安全输出 | D |
| Reconcile 操作和补偿 ChangeSet | context-edit-operations.md §2 Reconcile | IMPLEMENTED — `Reconcile` 将期望状态编译为 Update/Remove/Replace/Reorder，检查 Tombstone 并原子应用；测试 `reconcile_emits_updates_replacements_and_a_valid_final_order`、`remove_tombstone_is_visible_to_later_reconcile` | D |
| 操作冲突、审计和错误分类 | context-edit-operations.md §3–§5 | PARTIAL — 已有 Stale-Base/Missing/Duplicate/Reorder/Version/Budget 类型化错误，以及带操作 ID/原因的操作记录和 Tombstone；仍无持久化审计日志或隐私安全的外部错误投影 | I |
| Context Manager 组件责任边界 | context-manager.md §1–§2 | PARTIAL — 有数据原语和参考流程；无 Coordinator/Ports/Services | D |
| Manager 主流程：身份、授权、加载、消费、校验、规划、编辑、提交、交付、协调、观测 | context-manager.md §3 | PARTIAL — Build 和本地 ChangeSet 部分存在；无可执行端到端流程 | D |
| T1 Context 原子提交 | context-manager.md §4 | PARTIAL — 内存 `apply_change_set` 已按 Base-Version 全有或全无应用；这里没有持久化事务提交，Durable Commit 属于 D 的责任边界 | D |
| T2 Delivery Attempt 与 T1 分离 | context-manager.md §4 | NOT IMPLEMENTED — 仅有 Private Intent，无发送/重试状态 | 不在范围 |
| T3 Adapter Application 是外部行为 | context-manager.md §4 | NOT IMPLEMENTED — 无 Adapter Apply | 不在范围 |
| T4 Reconciliation 是可恢复 Saga | context-manager.md §4、§6 | PARTIAL — 只有单条目分类，无持久化 Saga Journal | D |
| F 协作：候选是提案，不完整不等于不存在 | context-manager.md §5 | PARTIAL — 有候选输入；无 F 接口/Watermark 向量 | 不在范围 |
| 故障行为和错误分类 | context-manager.md §6、§8 | PARTIAL — 有部分 Fail-Closed 错误；缺少完整错误目录和隐私安全投影 | I |
| 状态所有权与可观测性 | context-manager.md §7、§9 | NOT IMPLEMENTED — 无生产 Metrics/Traces | D |
| Reconciliation 触发器和权威信号归属 | context-reconciliation.md §1–§2 | NOT IMPLEMENTED — 所引用的 `ContextLedger`/`reconcile_entry` 参考模型不在本次核验的 mainline；Rust crate 未实现 ChangeSet 编辑器。 | D |
| Stale/ReconcileRequired/Reconciled/Blocked/Closed 区分 | context-reconciliation.md §3 | PARTIAL — 有 Entry 分类；无 Context/Run 状态机 | 本线程可做 |
| Reconciliation 算法：触发、精确 Context、先 Tombstone、加载、授权、Canonical 校验、水位比较、分类、补偿、CAS、Delivery、审计 | context-reconciliation.md §4 | PARTIAL — 本地 Tombstone-aware Reconcile 和 Base-Version 暂存已实现；权威触发、重新授权、Canonical/Watermark 校验、持久化 Saga、Delivery 和审计仍缺失 | D |
| Forget/撤权失效和 Adapter Target 状态 | context-reconciliation.md §5 | PARTIAL — 仅内存 Tombstone；无持久化 Target Evidence 或 Adapter Clear | D |
| Offline Reconnect、缓存失效和安全替换 | context-reconciliation.md §5–§6 | NOT IMPLEMENTED — 无 Reconnect/Adapter Runtime | D |
| Reconciliation Audit 和 Typed Cursor 分离 | context-reconciliation.md §7–§9 | NOT IMPLEMENTED — 无持久化 Run Record/向量验证器 | D |
| 不可变 ContextVersion 和 ChangeSet 历史 | context-versioning.md §1–§4 | PARTIAL — `ContextSnapshot` 携带 `context_version`，`zero_context_version_is_rejected` 拒绝零版本，`delivery_intent_targets_snapshot_context_version` 绑定 Delivery 目标；仍无不可变版本历史或 ChangeSet 历史/编辑器 | 不在范围 |
| Context/Entry/Delivery/Applied 对象分离 | context-versioning.md §5–§6 | PARTIAL — 有 Snapshot 和 DeliveryIntent；`delivery_intent_targets_snapshot_context_version` 验证目标版本绑定；无持久化 Context/Applied 对象 | 本线程可做 |
| Snapshot/Delta 语义及精确 Base 应用 | context-versioning.md §7 | PARTIAL — `apply_change_set` 针对精确 Base-Version 应用并暂存新 Snapshot；测试 `stale_base_is_rejected_without_changing_snapshot` 和 `any_failing_operation_discards_the_entire_staged_set`；仍无持久化 Delta 历史/Replay | D |
| CAS、幂等、原子 ChangeSet、禁止隐式合并 | context-versioning.md §8 | PARTIAL — `commit_change_set` 有内存 Base-Version CAS/幂等，`apply_change_set` 拒绝过期 Base 且不隐式合并；仍无持久化 Context 原子提交或持久化幂等记录 | I |
| Delivery 生命周期、迟到 ACK 和 Supersession | context-versioning.md §9 | NOT IMPLEMENTED — 无 Attempt Ledger/ACK 消费者 | 本线程可做 |
| Rollback、补偿和 Replay | context-versioning.md §10 | PARTIAL — 有 Tombstone 和内存历史；无持久化 Replay/Rebuild | D |
| Full/Partial/Bypassed/Unknown 覆盖语义 | context-versioning.md §11、§14.3 | PARTIAL — Applied Ledger 要求调用方 Gate 全部为真；无完整 Region 提取或 Coverage Proof | D |
| Typed Cursor 分离和 Producer Admission | context-versioning.md §13.1–§13.2 | NOT IMPLEMENTED — 无 D 注册或 Typed Cursor Validator | D |
| 受保护发布顺序和原子可见性 Gate | context-versioning.md §13.3 | NOT IMPLEMENTED — 当前没有已接受且可执行的跨 Owner Gate。 | D |
| Applied 状态机和精确证据映射 | context-versioning.md §14.1–§14.4 | PARTIAL — `GAppliedLedger.evaluate`；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_non_accepted_c_outcomes_never_create_applied`、`test_missing_or_failed_authority_gate_blocks_commit`；Gate 由调用方提供，无当前使用重验证 | D |
| Applied 幂等、冲突和重启读回 | phase-3.6-applied-forget-reconciliation-contract.md §Applied；phase-3.8.22 §4–§6 | IMPLEMENTED — `GAppliedLedger.evaluate`、`read`、`conflict_count`；测试 `test_same_identity_and_same_evidence_is_idempotent`、`test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`、`test_restart_reads_original_record_and_replay_returns_same_id` | 不在范围 |
| Forget/撤权后 Historical Applied 与 Current Use 分离 | phase-3.6-applied-forget-reconciliation-contract.md §Current Use；phase-3.8.22 §8 | NOT IMPLEMENTED — 当前用守卫不存在：`current_use_allowed` 与 `test_current_use_requires_every_currentness_gate` 在全仓零命中（本行此前同时声称两者存在，那是错误的）；无持久化失效事件，无 Owner 查询 | D |
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
| 必需竞争/故障符合性矩阵 | phase-3.7 §8–§9 | PARTIAL — 61 个 Rust 单元测试、6 个跨 Crate 集成测试和 8 个 Applied 测试；仍无多 Owner 确定性竞争 Harness | D |
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

本轮新增纯内存 ChangeSet 编辑器及回归测试。评估的 mainline 基线为 `b9ddd241a18a00b3b8f3b0ce2e176b6f859bc0da`；实现提交为 `46c4b67728db8c8b58e4d8e96b277cc75ddc1f35`；更新后的 Rust 源文件 Blob 为 `d405f7927235a3cb75dbd2eb1942bf75b167643f`。§2 的 19 个设计/源文件在该基线上未变化。该 crate 现有 61 个单元测试：`build_context_order_is_deterministic_across_repeated_calls`, `sorting_uses_tier_then_descending_priority_then_entry_id`, `entry_budget_error_reports_actual_candidate_count`, `byte_budget_error_reports_accumulated_rendered_bytes`, `exact_entry_and_byte_budget_boundaries_succeed`, `duplicate_entry_ids_are_rejected`, `duplicate_memory_version_membership_is_rejected`, `non_active_non_consolidated_lifecycles_are_rejected`, `candidate_scope_must_be_contained_by_identity_scope`, `empty_identity_scope_purpose_and_schema_version_are_rejected`, `zero_context_version_is_rejected`, `zero_entry_or_byte_budget_is_rejected`, `delivery_intent_visibility_is_always_private_pending_gate`, `delivery_intent_targets_snapshot_context_version`, `delivery_intent_snapshot_json_round_trips_to_equivalent_snapshot`, `build_context_rejects_candidates_without_lineage`, `build_context_rejects_whitespace_only_rendered_content`, `snapshot_accessors_report_entry_count_and_emptiness`, `build_context_rendered_byte_total_matches_entry_sum`, `validate_snapshot_rejects_inconsistent_bytes_and_empty_entry_content`, `context_version_id_rejects_empty`, `change_set_id_rejects_empty`, `context_head_rejects_genesis_with_nonzero_sequence`, `context_head_rejects_version_with_zero_sequence`, `entry_version_rejects_zero_revision`, `entry_version_rejects_rendered_byte_mismatch`, `change_set_rejects_duplicate_operation_ids`, `change_set_rejects_empty_operations`, `change_set_rejects_precomputed_target_version_when_prepared`, `change_set_rejects_payload_hash_mismatch`, `rollback_from_genesis_is_rejected`, `rollback_rejects_empty_reason`, `rollback_rejects_empty_created_at`, `rollback_rejects_duplicate_target_entry_ids`, `rollback_rejects_noop_diff`, `rollback_sets_all_declared_change_set_fields`, `rollback_adds_missing_target_entry`, `rollback_removes_entries_absent_from_target`, `rollback_replaces_changed_entry_with_target_revision`, `rollback_operation_ids_are_deterministic`, `commit_rejects_stale_policy_epoch`, `commit_rejects_wrong_base_version`, `commit_rejects_context_mismatch`, `commit_rejects_snapshot_hash_mismatch`, `commit_rejects_budget_summary_mismatch`, `commit_returns_version_with_caller_metadata_and_computed_sequence`, `commit_is_idempotently_replayed_for_same_principal_and_key`, `supersede_version_increments_sequence_and_preserves_other_fields`, `supersede_version_rejects_sequence_overflow`, `snapshot_hash_is_independent_of_entry_order`, `change_set_rejects_duplicate_operation_ids`, `stale_base_is_rejected_without_changing_snapshot`, `any_failing_operation_discards_the_entire_staged_set`, `remove_tombstone_is_visible_to_later_reconcile`, `reorder_rejects_non_permutation`, `replace_tombstones_old_membership_in_the_same_result`, `update_preserves_memory_version_and_rejects_version_changes`, `rendered_byte_budget_is_revalidated_after_update`, `expire_uses_target_version_and_preserves_expiration_tombstone`, `reconcile_materializes_new_desired_membership_through_replace`, `reconcile_emits_updates_replacements_and_a_valid_final_order`。使用 Rust `rustc 1.100.0 (0ef1bc386 2026-11-09)`、Cargo `1.100.0 (3acc79c0c 2026-11-05)` 执行命令 `cargo test -p memory-context`：61 个单元测试通过，6 个集成测试通过，0 个 Doc Test 失败（命令成功完成）。精确汇总为 `test result: ok. 61 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s`、`test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s`、`test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s`、`test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s`。集成测试清单：`e2e_negative_paths.rs` — `foreign_scope_cannot_read_or_populate_context`、`candidate_lifecycle_is_refused_by_context_after_store_round_trip`、`stale_revision_is_rejected_and_current_version_remains_n_plus_one`、`entry_budget_overflow_reports_actual_and_limit_after_store_reads`、`file_backed_sqlite_survives_storage_handle_restart`；`e2e_store_to_context.rs` — `sqlite_store_read_current_builds_context_from_persisted_revision`。新增 11 个单元测试覆盖 ChangeSet 封套和六种操作；原有 50 个 Rust 单元测试名称（包括原有 20 个 Builder 测试）全部保持不变。7 行从 NOT IMPLEMENTED 晋升为 IMPLEMENTED（封套、Update、Remove、Replace、Reorder、Expire、Reconcile）；4 行调整为 PARTIAL（本地 Tombstone 与持久化失效的边界、类型化本地审计/错误面、T1 持久化边界、持久化 CAS/幂等）。Compact 和 Sufficiency 仍在范围之外。该基线中已提交的映射表原本有 77 行关注点（38 NOT IMPLEMENTED / 37 PARTIAL / 2 IMPLEMENTED），并非 83 行；本轮更新后仍为 77 行：27 NOT IMPLEMENTED / 41 PARTIAL / 9 IMPLEMENTED。独立 Python Applied Ledger 参考测试仍为 8 项（`test_new_complete_success_commits_one_full_applied_record`, `test_same_identity_and_same_evidence_is_idempotent`, `test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`, `test_non_accepted_c_outcomes_never_create_applied`, `test_missing_or_failed_authority_gate_blocks_commit`, `test_restart_reads_original_record_and_replay_returns_same_id`, `test_different_logical_identity_gets_a_distinct_record`, `test_identity_requires_exact_typed_field_set`）；此前记录的执行命令为 `python3 -m unittest discover -s 06-memory-context/reference-model -p 'test_g_applied_ledger.py' -v`，结果 `Ran 8 tests in 0.009s`、`OK`（Linux，Python 3.14.4）。本轮未增加持久化、Compact 或 Sufficiency 评估器。


### Round 7 — Sufficiency 结果评估器

评估基线：`0cce40aae5c642f30fabef7b844ac8397322684b`；实现提交：`ad7a05843ebdcbcaaec2a51d9a6ace307ae1054d`；文档后续提交：`d236fcc94b230c2ca57e720ebc607bf8a1f72590`；Rust 源文件 Blob：`4fad76242c6426f594904d0f0c9f8871670aecc4`；执行命令：`cargo test -p memory-context`。新增 `SufficiencyRequirement`、十个命名的 `SufficiencyDimension` 及向前兼容的未知维度、`SufficiencyAssessment` 和四种结果。当前仅能测量不同的 Evidence Ref 数量，以及快照中明确存在的 Environment Identity。其余八个维度因快照 Schema 缺少结构化证据而返回 Unknown；不尝试从文本推断。任何不可判定需求优先于已知缺口，因此 Unknown 不会被降级为 Insufficient。空需求集为 Unknown，而不是空真意义上的 Sufficient。新增七项测试：`all_mandatory_requirements_met_are_sufficient`、`one_unmet_mandatory_requirement_is_named_in_insufficient_outcome`、`unmet_advisory_requirement_is_conditional_not_insufficient`、`empty_requirement_set_is_unknown_not_vacuously_sufficient`、`unknown_dimension_returns_unknown_and_never_insufficient`、`unknown_evidence_takes_precedence_over_a_known_mandatory_gap`、`four_outcomes_are_mutually_exclusive_and_exhaustive_for_the_decision_rule`。精确结果：68 个单元测试、5 个负向路径集成测试、1 个 Store-to-Context 集成测试、0 个 Doc Test，全部通过。77 行映射现在为 25 NOT IMPLEMENTED / 43 PARTIAL / 9 IMPLEMENTED。Requirement Graph、候选优化器、Compact、Fidelity Validator 和 Overflow Planner 仍为 NOT IMPLEMENTED。

## 5. 评估边界

`IMPLEMENTED` 仅表示表中明确列出的函数/结构体与测试所覆盖的参考行为；不代表生产持久化、分布式并发、跨 Owner 授权、Adapter 交付或端到端完成。`PARTIAL` 明确列出缺失维度。`NOT IMPLEMENTED` 不代表不可实现；阻塞归属仅指出下一责任边界。
