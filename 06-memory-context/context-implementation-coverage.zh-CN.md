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
| README 范围、索引和 Owner 边界 | README §1–§4 | PARTIAL — 仅索引，无独立可执行行为；以下条目为实际依据 | 无；以子项为准 |
| Brain 拥有的期望 Context 成员与 Canonical Memory 分离 | context-architecture §1–§2 | PARTIAL — 有 `ContextEntry`、`ContextSnapshot`；无 canonical-store adapter；测试 `serializes_snapshot_and_prepares_non_sendable_delivery_intent` | D 拥有 canonical 访问权 |
| Context 身份绑定 Scope、Agent、实例、Session、Task、Environment 和 Purpose | context-architecture §3 | PARTIAL — `ContextIdentity::validate`；正向间接覆盖 `build_sorts_by_tier_then_priority_then_entry_id`；缺少 Environment 缺失/歧义专门测试 | B/I 身份和授权语义 |
| 环境相关身份必须 Fail-Closed | context-architecture §3 | NOT IMPLEMENTED — Rust Environment 字段可选，未实现环境依赖判定 | G 可在操作环境要求明确后补本地校验；B/I 类型绑定仍属外部 |
| P0–P3 仅是优先级，不是信任或指令等级 | context-architecture §4、§6 | PARTIAL — 有 `ContextTier` 和候选排序；测试 `build_sorts_by_tier_then_priority_then_entry_id`；无下游指令边界执行 | I/H/Agent Runtime |
| Planner 消费授权候选，F 拥有检索与排序 | context-architecture §5、§9 | PARTIAL — `build_context` 消费调用方候选；无 F adapter 或检索实现 | F 检索合同；I 授权 |
| Editor、Versioner、Reconciler、Budget Manager、Delivery Coordinator 是逻辑模块 | context-architecture §5 | PARTIAL — 有预算/快照/Delivery 基础类型，无模块级工作流 | G 本地实现；H 负责传输边界 |
| Entry 保留结构化来源、认知限定和生命周期 | context-architecture §6 | PARTIAL — `ContextCandidate`/`ContextEntry` 保留来源/证据/限定字段；测试 `rejects_missing_lineage_and_empty_content`；无来源授权校验器 | D canonical lineage；I 分类 |
| Memory 内容不得成为指令或工具授权 | context-architecture §6 | NOT IMPLEMENTED — 数据结构不执行下游 Prompt Region 隔离 | H/Agent Integration；I 安全边界 |
| Context、Entry、Delivery 生命周期分离 | context-architecture §7 | PARTIAL — 有 Context/Delivery 基础类型，缺少三套独立状态机 | G 可补本地状态机；H 提供 Adapter 证据 |
| Forget/撤权 Tombstone 阻断活动及待处理投影 | context-architecture §8 | PARTIAL — 新增 `ContextLedger.tombstones`；测试 `test_remove_tombstones_membership_not_canonical_memory`；无持久化及 Delivery 扇出 | D ForgetFence、I 撤权、H 清除证据 |
| Adapter 按 Session 清除状态及 Reconnect | context-architecture §8 | NOT IMPLEMENTED — 无 Adapter/Session Runtime | H 拥有 Adapter 协议与证据 |
| Budget 是向量而不是单一 Top-K | context-budget-and-sufficiency §1–§2 | PARTIAL — `ContextBudget` 检查 Entry 数和渲染字节；测试 `enforces_entry_and_byte_budgets_without_truncation`；缺 Token、Fan-out、来源深度、延迟、CPU、Tier 预留 | G 可增加估算；H 提供 Tokenizer/Package 限制 |
| 任务特定 Sufficiency 覆盖十个维度 | context-budget-and-sufficiency §3 | NOT IMPLEMENTED — 无 Requirement Graph 或逐维评估器 | G 可实现本地确定性评估器；F 完整性和 D/I 有效性作为外部输入 |
| 规划保留必需锚点、证据、冲突和不确定性 | context-budget-and-sufficiency §4 | PARTIAL — 有候选准入和稳定排序；无 Requirement Graph 优化器或冲突覆盖测试 | G 本地 Planner；F 检索；D/I 来源校验 |
| 在向量约束下优化候选集边际覆盖 | context-budget-and-sufficiency §5 | NOT IMPLEMENTED — 无优化器/压缩器 | G 可做确定性原型；Tokenizer/模型配置由 H 提供 |
| Compaction 保留 Lineage、限定和冲突 | context-budget-and-sufficiency §5、§9.3 | NOT IMPLEMENTED — 无 Compaction 模型或 Fidelity Validator | G 可做本地确定性校验；发布前 D 依赖注册为外部条件 |
| Sufficiency 结果和安全溢出降级 | context-budget-and-sufficiency §6–§7 | NOT IMPLEMENTED — 无 Sufficient/Conditional/Insufficient/Unknown 评估器或溢出规划器 | G 可实现本地评估器；F 完整性为外部输入 |
| Budget/Sufficiency 可观测性 | context-budget-and-sufficiency §8–§9.4 | NOT IMPLEMENTED — 无 Metrics/Report 模型 | G 可实现报告投影；生产遥测为外部 |
| ChangeSet 公共封套、前置条件和全有或全无暂存 | context-edit-operations §1 | IMPLEMENTED — `ContextLedger.apply_changeset`；测试 `test_changeset_is_all_or_nothing_on_late_invalid_operation`、`test_stale_base_version_is_rejected` | 仅 G 内存参考模型；持久化提交依赖 Storage |
| Add 精确 Canonical Ref、Lineage 和重复防护 | context-edit-operations §2 Add | IMPLEMENTED — `ContextLedger._apply_one(ADD)`；测试 `test_add_creates_one_immutable_target_version`、`test_duplicate_membership_and_cross_scope_are_rejected` | D 负责 Canonical Ref 解析 |
| Update 仅修改 Context 元数据/渲染，不修改 Canonical Memory | context-edit-operations §2 Update | IMPLEMENTED — `ContextLedger._apply_one(UPDATE)`；测试 `test_update_changes_only_context_metadata` | G 本地参考语义 |
| Remove 仅移除成员，不执行 Canonical Forget | context-edit-operations §2 Remove | IMPLEMENTED — `ContextLedger._apply_one(REMOVE)`；测试 `test_remove_tombstones_membership_not_canonical_memory` | D 拥有 Forget |
| Replace 原子替换并保留旧成员 Tombstone | context-edit-operations §2 Replace | IMPLEMENTED — `ContextLedger._apply_one(REPLACE)`；测试 `test_replace_is_one_atomic_membership_transition` | D 校验替换 Lineage |
| Reorder 要求精确覆盖同一 Context 的成员集合 | context-edit-operations §2 Reorder | IMPLEMENTED — `ContextLedger._apply_one(REORDER)`；测试 `test_reorder_requires_exact_permutation` | G 本地参考语义 |
| Expire 移除活动成员并保留 Tombstone | context-edit-operations §2 Expire | IMPLEMENTED — `ContextLedger._apply_one(EXPIRE)`；测试 `test_expire_removes_entry_and_leaves_tombstone`；有效时间调度器缺失 | G 本地调度器/时间源 |
| Compact 操作和 Lineage 安全输出 | context-edit-operations §2 Compact | NOT IMPLEMENTED — 模型中没有 Compact 操作 | G 可补本地模型；D 依赖 Gate 属外部 |
| Reconcile 操作和补偿 ChangeSet | context-edit-operations §2 Reconcile | PARTIAL — `reconcile_entry` 可分类单条目；测试 `test_reconciliation_fails_closed_on_unknown_authority_or_incomplete_retrieval`、`test_reconciliation_maps_forget_and_supersession_without_rewriting_canonical_truth`；无批量 ChangeSet 规划器 | G 可补批量规划；D/I/F 证据为外部 |
| 操作冲突、审计和错误分类 | context-edit-operations §3–§5 | PARTIAL — 拒绝未知操作、旧 Base 和变更 Digest；测试 `test_unknown_operation_and_canonical_mutation_fields_are_rejected`、`test_same_key_changed_payload_is_conflict`；未建模 Actor/Audit/PolicyEpoch | G 本地审计模型；I 策略证据 |
| Context Manager 组件责任边界 | context-manager §1–§2 | PARTIAL — 有数据原语和参考流程；无 Coordinator/Ports/Services | G 可补编排模型；外部 Port 由 D/I/F/H 拥有 |
| Manager 主流程：身份、授权、加载、消费、校验、规划、编辑、提交、交付、协调、观测 | context-manager §3 | PARTIAL — Build 和本地 ChangeSet 部分存在；无可执行端到端流程 | D/I/F/H/C/Storage；不在此替其他 Owner 裁定 |
| T1 Context 原子提交 | context-manager §4 | NOT IMPLEMENTED — 内存 ChangeSet 不等于持久化原子事务 | Storage/Consistency 物理事务；G 拥有逻辑提交 |
| T2 Delivery Attempt 与 T1 分离 | context-manager §4 | NOT IMPLEMENTED — 仅有 Private Intent，无发送/重试状态 | H 传输 |
| T3 Adapter Application 是外部行为 | context-manager §4 | NOT IMPLEMENTED — 无 Adapter Apply | H |
| T4 Reconciliation 是可恢复 Saga | context-manager §4、§6 | PARTIAL — 只有单条目分类，无持久化 Saga Journal | G 本地 Saga 模型；D/I/F/H 外部权威 |
| F 协作：候选是提案，不完整不等于不存在 | context-manager §5 | PARTIAL — 有候选输入；无 F 接口/Watermark 向量 | F |
| 故障行为和错误分类 | context-manager §6、§8 | PARTIAL — 有部分 Fail-Closed 错误；缺少完整错误目录和隐私安全投影 | G 可补本地错误目录；I 隐私边界 |
| 状态所有权与可观测性 | context-manager §7、§9 | NOT IMPLEMENTED — 无生产 Metrics/Traces | G 遥测；C/H Delivery 证据 |
| Reconciliation 触发器和权威信号归属 | context-reconciliation §1–§2 | PARTIAL — `reconcile_entry` 接受调用方事实；无 Trigger Ledger 或 D/E/F/I/H 消费者 | G Trigger 模型；D/E/F/I/H 权威输入 |
| Stale/ReconcileRequired/Reconciled/Blocked/Closed 区分 | context-reconciliation §3 | PARTIAL — 有 Entry 分类；无 Context/Run 状态机 | G 可实现本地状态机 |
| Reconciliation 算法：触发、精确 Context、先 Tombstone、加载、授权、Canonical 校验、水位比较、分类、补偿、CAS、Delivery、审计 | context-reconciliation §4 | PARTIAL — 有条目分类和本地 ChangeSet/CAS；其余流程未执行 | G 本地编排；D/I/F/H 外部 |
| Forget/撤权失效和 Adapter Target 状态 | context-reconciliation §5 | PARTIAL — 仅内存 Tombstone；无持久化 Target Evidence 或 Adapter Clear | D/I/H |
| Offline Reconnect、缓存失效和安全替换 | context-reconciliation §5–§6 | NOT IMPLEMENTED — 无 Reconnect/Adapter Runtime | H；D/I 当前权威 |
| Reconciliation Audit 和 Typed Cursor 分离 | context-reconciliation §7–§9 | NOT IMPLEMENTED — 无持久化 Run Record/向量验证器 | G 可建模记录形状；D/I/F/H 拥有 Cursor 语义 |
| 不可变 ContextVersion 和 ChangeSet 历史 | context-versioning §1–§4 | PARTIAL — 有 `ContextSnapshot.context_version` 和本地版本递增；测试 `test_add_creates_one_immutable_target_version`、`test_stale_base_version_is_rejected`；无持久化不可变版本库 | Storage |
| Context/Entry/Delivery/Applied 对象分离 | context-versioning §5–§6 | PARTIAL — 有 Snapshot 和 DeliveryIntent；无持久化 Context/Applied 对象 | G 本地模型；H/C 证据边界 |
| Snapshot/Delta 语义及精确 Base 应用 | context-versioning §7 | PARTIAL — 有 JSON Snapshot 序列化；测试 `serializes_snapshot_and_prepares_non_sendable_delivery_intent`；无 Delta Apply/Replay 模型 | G 可补本地 Delta；H 传输 |
| CAS、幂等、原子 ChangeSet、禁止隐式合并 | context-versioning §8 | IMPLEMENTED — `ContextLedger.apply_changeset`；测试 `test_same_key_same_payload_is_idempotent`、`test_same_key_changed_payload_is_conflict`、`test_stale_base_version_is_rejected`、`test_changeset_is_all_or_nothing_on_late_invalid_operation` | 仅内存；Storage 持久化 CAS 仍为外部 |
| Delivery 生命周期、迟到 ACK 和 Supersession | context-versioning §9 | NOT IMPLEMENTED — 无 Attempt Ledger/ACK 消费者 | H 拥有 Wire ACK；G 可在精确证明 Schema 后实现本地 Ledger |
| Rollback、补偿和 Replay | context-versioning §10 | PARTIAL — 有 Tombstone 和内存历史；无持久化 Replay/Rebuild | G 本地 Replay；Storage Restore 和 D/I Fence 外部 |
| Full/Partial/Bypassed/Unknown 覆盖语义 | context-versioning §11、§14.3 | PARTIAL — Applied Ledger 要求调用方 Gate 全部为真；无完整 Region 提取或 Coverage Proof | C/H 证据；I/D 当前性 |
| Typed Cursor 分离和 Producer Admission | context-versioning §13.1–§13.2 | NOT IMPLEMENTED — 无 D 注册或 Typed Cursor Validator | D；I |
| 受保护发布顺序和原子可见性 Gate | context-versioning §13.3 | PENDING CROSS-OWNER DECISION — G 仅私有暂存；没有可调用且已证明的跨存储 Gate | D + Storage/Consistency；退出：精确 Owner 合同及已验证原子/可恢复 Gate |
| Applied 状态机和精确证据映射 | context-versioning §14.1–§14.4 | PARTIAL — `GAppliedLedger.evaluate`；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_non_accepted_c_outcomes_never_create_applied`、`test_missing_or_failed_authority_gate_blocks_commit`；Gate 由调用方提供，无当前使用重验证 | C/H/I/D/COC/Storage |
| Applied 幂等、冲突和重启读回 | phase-3.6-applied-forget-reconciliation-contract §Applied；phase-3.8.22 §4–§6 | IMPLEMENTED — `GAppliedLedger.evaluate`、`read`、`conflict_count`；测试 `test_same_identity_and_same_evidence_is_idempotent`、`test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`、`test_restart_reads_original_record_and_replay_returns_same_id` | 仅单节点 SQLite；生产持久化/恢复为外部 |
| Forget/撤权后 Historical Applied 与 Current Use 分离 | phase-3.6-applied-forget-reconciliation-contract §Current Use；phase-3.8.22 §8 | PARTIAL — 有 `current_use_allowed`；测试 `test_current_use_requires_every_currentness_gate`；无持久化失效事件或 Owner 查询 | I/D/H/C 当前证据 |
| COC JF-10 Bridge、Recovery Batch 和因果 Terminal Proof | phase-3.6.2 §1–§4；phase-3.6.3 §1–§4 | PENDING CROSS-OWNER DECISION — G 消费证明，不创建/验证 COC Quorum 或 Terminal 语义 | COC/Storage；退出：部署权威证据及精确符合性测试 |
| PreparedParticipant/GID/Native XID 和 Visibility Receipt Join | phase-3.6.4 §1–§6 | PENDING CROSS-OWNER DECISION — G 不负责 Native Transaction Resolution | Storage/Consistency；退出：精确 Same-GID Terminal 与 Visibility Proof |
| Context Serving 前的 Restore Reconciliation | phase-3.6.5 §1–§4 | NOT IMPLEMENTED — 无 G Restore/Replay 集成；Restore Receipt 不能授权 Serving | Storage + COC + I + D；退出：已验证证明清单及 G Restore 测试 |
| Local Lifecycle、Producer/Derivative、Queue、Recall、Context、Restore 状态 | phase-3.7 §1–§8 | PARTIAL — ChangeSet/Reconcile 参考部分存在；无持久化 Producer/Queue/Recall/Restore Ledger | G 可补本地状态模型；D/I/F/H/C/Storage 接口为外部 |
| 入队/租约/读取受保护源之前完成 Producer Registration | phase-3.7 §2、§10.1 | NOT IMPLEMENTED — 无 D Producer Registry Receipt 或 Queue Admission | D；退出：D 签发 Producer Class/Work Registration，G 完成精确消费 |
| 可见前完成 Derivative Dependency Registration | phase-3.7 §3、§10.1 | NOT IMPLEMENTED — 无 Dependency Receipt 或 Publication Gate | D + Storage |
| Delivery Queue Attempt 身份、重试和 ACK 分离 | phase-3.7 §4 | NOT IMPLEMENTED — 无持久化 DeliveryId/Attempt Ledger | G 可实现本地 Ledger；H 提供传输证据 |
| Recall 候选 Canonical 校验和 Sufficiency | phase-3.7 §5 | PARTIAL — Rust 候选校验和 Reconciliation 模型存在；无 F Watermark 向量或实时 D/I 重验证 | F/D/I |
| Context 与 Applied 生命周期分离 | phase-3.7 §6 | PARTIAL — 模型区分 Context Version 与 Applied Ledger；无集成状态机 | G 本地集成 |
| Restore/Reconnect 隔离及当前状态协调 | phase-3.7 §7 | NOT IMPLEMENTED — 无 Restore Fence、Ledger Replay 或 Adapter Reconnect | Storage/COC/I/D/H |
| 必需竞争/故障符合性矩阵 | phase-3.7 §8–§9 | PARTIAL — 新增 14 个本地测试和 8 个 Applied 测试；无多 Owner 确定性竞争 Harness | G 本地测试；D/I/H/C/Storage 证据 |
| C Provider Outcome × SideEffect 映射 | phase-3.8.4 §1–§6 | PARTIAL — Applied Ledger 拒绝非接受结果；测试 `test_non_accepted_c_outcomes_never_create_applied`；无 SideEffect 维度或 C Record 验证 | C |
| Storage Logical Serialization Topology 与可见对象准入 | phase-3.8.5 §1–§4 | PENDING CROSS-OWNER DECISION — G 消费 Storage Visibility Proof，不实现 DB 拓扑 | Storage + D |
| Per-authority Storage Serialization Anchor 不等于 ContextVersion/AppliedCursor | phase-3.8.6 §1–§4 | PARTIAL — 仅文档区分；无 Typed Runtime Validator | Storage 权威；稳定合同后 G 可补本地类型校验 |
| H Unified 1.2.14 × CSubmitOutcome 1.0.1 Full-path 精确 Join | phase-3.8.18 §1–§7 | PARTIAL — Applied 原型仅有粗粒度证据映射；无生产 Schema Digest/签名/Authority Callback 验证 | H/C/I/D/COC/Storage |
| Outcome/SideEffect 矛盾、UNKNOWN 和 IN_DOUBT | phase-3.8.18 §2–§4 | PARTIAL — C Outcome 粗粒度 Fail-Closed；无成对 SideEffect 状态机 | C 拥有 Outcome 真值；G 可在精确 C Schema 后扩展消费模型 |
| Applied Identity/Evidence Revision 唯一性和不可变冲突 | phase-3.8.22 EN §3–§5 | PARTIAL — 有单 Identity/单 Digest 冲突模型；无独立 Evidence Revision 序列/Source Pin | G 可扩展本地参考模型；精确 C/H/COC/I/D/Storage Join 属外部 |
| Applied 原子提交和唯一约束 | phase-3.8.22 EN §5 | PARTIAL — `GAppliedLedger` 有 SQLite 事务和主键；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_same_identity_and_same_evidence_is_idempotent`；不保证多副本 | Storage/Consistency 生产拓扑 |
| Crash/Retry/Restore Fencing 和 Current-use 失效 | phase-3.8.22 EN §6–§8 | PARTIAL — 重开读回测试 `test_restart_reads_original_record_and_replay_returns_same_id`；无进程崩溃注入、Restore Fence 或 High-water 协调 | G 本地 Restore 模型；COC/I/D/Storage Owner Proof |
| Machine-readable Applied Record 和对抗符合性 | phase-3.8.22 EN §9–§11 | NOT IMPLEMENTED — 无生成 Schema/SDK 或完整 18 项 Durable Crash Suite | G 可补 Schema/测试；H/C/COC/I/D/Storage 精确接受仍必需 |
| 既有 8 项 Applied 参考模型证据 | phase-3.8.22 EN §13；phase-3.8.22 ZH 对应章节 | IMPLEMENTED — `GAppliedLedger`；测试 `test_new_complete_success_commits_one_full_applied_record`、`test_same_identity_and_same_evidence_is_idempotent`、`test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged`、`test_non_accepted_c_outcomes_never_create_applied`、`test_missing_or_failed_authority_gate_blocks_commit`、`test_restart_reads_original_record_and_replay_returns_same_id`、`test_different_logical_identity_gets_a_distinct_record`、`test_identity_requires_exact_typed_field_set` | 仅参考原型，不是生产 G Runtime |

## 4. 本次补齐的 G-local 工作

新增：

- `reference-model/g_context_model.py`：确定性内存 ChangeSet 模型，覆盖 ADD/UPDATE/REMOVE/REPLACE/REORDER/EXPIRE、载荷幂等、BaseVersion 冲突、暂存全有或全无转换、Membership/Scope 校验、Tombstone、单条目协调分类和 Fail-Closed Current-use 投影。
- `reference-model/test_g_context_model.py`：14 个测试覆盖上述行为。

这些新增内容补齐 G 自有语义，不修改 `crates/memory-context` 公开契约。模型刻意不实现持久化，也不声称实现 T1 物理原子性、D Producer Admission、D Dependency Registration、I 授权、H Delivery 或 Adapter Application。

其余 G-local 机会，如向量 Sufficiency 评估、确定性 Compaction、批量 Reconciliation 规划、Delivery Attempt Ledger、Restore Fence 状态和 Evidence Revision Ledger，已在上表明确标出，不得误认为已经实现。

## 5. 精确测试数量与验证

| 测试集 | 原有 | 新增 | 合计 |
|---|---:|---:|---:|
| Rust `crates/memory-context` 单元测试 | 7 | 0 | 7 |
| Python `test_g_applied_ledger.py` | 8 | 0 | 8 |
| Python `test_g_context_model.py` | 0 | 14 | 14 |
| **已识别测试总数** | **15** | **14** | **29** |

现有工作流 `.github/workflows/g-applied-reference-model.yml` 会发现参考模型目录下所有 `test_*.py`，因此现有测试命令会包含新增 14 个测试：
`python -m unittest discover -s 06-memory-context/reference-model -p "test_*.py" -v`。

**报告编写时测试状态：NOT RUN。** 本会话尚未取得 CI 成功证据，不声称测试通过。原有 7 个 Rust 测试未修改，但仍须由 CI 确认通过。新增后 Python 测试为 22 个（原有 8 + 新增 14）；Rust + Python 合计 29 个。

## 6. 跨 Owner 阻塞（不由 G 裁定）

- 受保护发布/可见性原子性 → D + Storage/Consistency → `context-versioning.md` §13.3、`context-manager.md` §10.2 → 精确可调用或已证明可恢复的原子 Gate，分别由 Owner 接受并测试。
- ForgetFence、Producer Registry、Dependency Registration、Barrier Terminality → D → `context-reconciliation.md` §8、Phase 3.7 §2–§3 → D 签发精确合同/Receipt，G 消费符合性通过。
- PermissionEpoch、认证 Actor/Scope、全局 Target 完成 → I（依赖 B 类型引用）→ `context-architecture.md` §3/§9、`phase-3.6-applied-forget-reconciliation-contract.md` → I 自有决策/证据 Schema 和 G 消费校验。
- Retrieval Completeness 和分区 Watermark → F → `context-budget-and-sufficiency.md` §9.1、`context-manager.md` §5 → 精确 F Result Schema、Watermark 向量及确定性缺口 Fixture。
- Adapter 协议、物化、Capability、Clear/Reconnect ACK → H → `context-architecture.md` §8–§9、Phase 3.7 §4/§7 → 精确 H Schema、认证证据及 Adapter 符合性。
- Final Immutable Request/Provider Outcome → C → Phase 3.8.4 §1–§6、Phase 3.8.18 §2–§4 → 精确 CSubmitOutcome 1.0.1/SideEffect 证据和消费者 Fixture。
- COC Participant/Terminal/Recovery Ordering → COC/Storage → Phase 3.6.2 §1–§4、Phase 3.6.3 §1–§4 → 已部署权威 Terminal/Recovery 证据及同事务 Join。
- Prepared GID、Same-GID Resolution、Visibility Pointer、Restore Receipt → Storage/Consistency → Phase 3.6.4 §1–§6、Phase 3.6.5 §1–§4 → 精确 Durable Same-GID Resolution 和独立验证的 Restore Proof。

## 7. 审查与验收边界

- 实现状态：新增 G-local 内存参考模型为 **IMPLEMENTED**；CI 通过前为 **NOT VERIFIED**。
- Rust crate 公开契约：未修改。
- 生产持久化、传输、分布式并发、跨 Owner Gate、端到端交付：**NOT IMPLEMENTED / NOT CLAIMED**。
- 独立审查：**NOT RUN**。Owner 不批准自己的交付。
- 合并/激活：本报告不授予授权。

