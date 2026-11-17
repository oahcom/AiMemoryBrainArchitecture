# Memory Versioning 与历史语义

- 文档 ID：D-VERSIONING-001
- 版本：1.0
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：af747f339d03bdd4684b6ed60fca05957dc8e1fb
- 审查时源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- 源规范：[D Owner 规范](../../../03-memory-brain/memory-versioning.md)
- 对应英文：[Memory Versioning and Historical Semantics](../../en/03-memory-brain/memory-versioning.md)
- 状态：不可变版本原则为 DECIDED；Claim Revision 和精确事务/时间语义为 CANDIDATE/OPEN
- 相关问题：INT-P0-01/03、INT-P1-01/02/06；DM-002/003/006/008/009/013

## 1. 目的

定义 Canonical Memory、Claim、Entity 和 Relation 的变更如何表示，以避免破坏性覆盖；提供确定性的历史查询、并发控制、幂等性、协调和感知 Forget 的历史语义。

## 2. 范围与所有权

覆盖 MemoryVersion、候选 ClaimRevision、EntityVersion、RelationRevision、LifecycleEvent Sequence、Canonical Commit Receipt、时间语义、历史引用解析和迁移记录。ContextVersion 和 ChangeSet 明确由 G 拥有。

D 定义不可变修订语义和 Parent 关系；Canonical Store 持久化 Revision/Commit Record；Lifecycle Manager 拥有 Lifecycle Event；B 拥有领域/认知/时间语义；I 拥有授权和 Forget Policy。

## 3. 职责与非职责

职责：定义不可变 Revision Identity/Parent；定义 CAS 和 Stale-write 行为；分别保留 Valid Time 与 Record/Transaction Time 历史；提供精确历史/As-of 读取；使 Retry 幂等并显式暴露 Conflict；保留 Entity Merge/Split 和 Relation Migration 历史；协调 Version/Dependency 枚举与 Forget。

不负责 ContextVersion 状态机、Delivery/Applied、Event Ingestion Sequence、BMCP Version 协商、全局 Permission Policy、Storage Engine 选型或物理擦除策略。

## 4. 领域对象

- **MemoryVersion：** 单个 Memory 的不可变 Snapshot；Per-Memory 单调 Sequence、Parent Version、Canonical Commit Sequence、Digest、Actor、Reason、Schema Version、Recorded Time、引用和内容快照。
- **ClaimRevision（CANDIDATE；INT-P0-01 ADR 阻塞）：** 稳定 Claim Identity 的不可变修订；包含 Revision ID、Claim ID、Sequence、Parent Revision、命题、Epistemic Status、Valid Time、来源/Evidence 引用、Provenance 引用、ScopeRefs、Actor、Recorded Time、Method 和 Digest。
- **EntityVersion：** 稳定 Entity ID 的不可变属性/别名档案修订。
- **RelationRevision：** 稳定 Relation ID 的不可变 Predicate/Endpoint/Validity/Evidence/Lifecycle 修订。
- **LifecycleEvent：** 权威的追加式状态转换记录，具有 Per-Aggregate Sequence；当前状态通过 Fold/Projection 得出。
- **CanonicalCommitReceipt：** Idempotency Key、Request Digest、Expected Base、Committed Version、Commit Sequence、Outcome 和 Timestamp。
- **MigrationRecord：** 明确的旧/新类型化引用、操作类型、映射/分区、Actor、Evidence、Scope、Sequence 和 Reason。

## 5. 数据模型与时间语义

所有 Revision 都不可变、使用不透明 ID 寻址、带 Schema Version 且绑定 Scope。除 Genesis 外，每个 Revision 都有一个 Parent。分支/Fork 不得静默合并：Canonical Aggregate Head 通过 CAS 推进；竞争 Revision 成为被拒提案或明确的协调候选。

时间轴：
- Event Time：被描述事件实际发生的时间。
- Recorded At：Brain 接受/记录信息的时间。
- Valid Time：命题/关系声称成立的区间。
- Commit/Transaction Time：Canonical Version 成为权威的时间。

候选 TimeValue 字段：lower_bound、upper_bound、precision、timezone、certainty、original_phrase、source_ref。TimeInterval 包含 start/end TimeValue、左闭右开边界约定，以及显式 Unknown/Unbounded 标记。Unknown 不等于 Infinity；缺失不代表永远有效。

历史查询契约：“在 T 时有效”按 Valid Time 过滤；“在 T2 时已知”按 Canonical Transaction/Record Time 过滤。结果标识准确 Revision/Version，以及它是 Current、Superseded、Retracted、Archived 还是因 Forget 不可用。

## 6. Claim Identity 备选方案（INT-P1-02）

| 维度 | Option A：稳定 Claim ID + 不可变 ClaimRevision | Option B：每次修正/后继都创建新 Claim ID |
|---|---|---|
| 身份 | 命题线程跨 Revision 持续；Revision 标识准确声明 | 每次声明/修正都是新身份，通过 Successor 关联 |
| Evidence | 链接到准确 Revision；共享 Evidence 显式关联 | 自然绑定 Claim，但重复链接会增多 |
| Lifecycle | 追加 Epistemic Status Revision；Retraction 是 Revision/Event | 旧 Claim Retract，再创建 Successor/新 Claim |
| Versioning | MemoryVersion 固定 ClaimRevision ID | MemoryVersion 固定 Claim ID；修正会导致身份变化 |
| Conflict | ConflictSet 引用准确 Revision | ConflictSet 引用不同 Claim Identity |
| Query | “当时已知的 Claim”需要选择 Revision | 不可变声明查询更简单；演进命题的聚合更困难 |
| Permissions | Scope 作用于 Claim Identity 和每个 Revision | 每个新 Claim 分别评估 Scope；Successor Link 另行授权 |
| Storage | Revision Table + Identity Index | 更多 Identity 和 Successor Graph |

**CANDIDATE 推荐：** Option A，即稳定 Claim ID 加不可变 ClaimRevision。它在保持每条历史声明不可变的同时，提供持久引用身份。Correction 创建新 Revision 和明确的 Correction/Supersession Relation；Retraction 创建新的 Epistemic Revision/Event，不删除先前声明。如果 ADR 批准独立 Fact 对象，FactRecord 具有自己的不可变 Revision Stream，并链接到其 Attest 的准确 ClaimRevision。ADR 批准前不冻结 Claim/Fact Schema。

## 7. 状态机

Revision：Draft → Validated → Committed。Committed Revision 不可变；后继 Revision 指向之前已提交 Revision。Retraction 是新的 Revision/Status Event，不是修改旧 Revision。Lifecycle 独立，由 Lifecycle Manager 管理。

Entity/Relation Version 使用相同的追加式 Parent/CAS 模式。Merge/Split 创建 Migration Record，不改写旧引用。ContextVersion/ChangeSet 是 G 拥有的独立对象，并固定 MemoryVersion ID。

## 8. 操作与并发

操作：ReadHead；ReadRevision；ReadAsOf(valid_at, known_by)；CommitRevision(expected_parent)；RetractClaim(expected_revision)；SupersedeRelation；MergeEntity；SplitEntity；ReconcileConflict；ResolveHistoricalRef；EnumerateVersionDependenciesForForget。

并发更新：
1. 客户端读取 Head Revision/Version。
2. 使用 Expected Parent 和 Idempotency Key 提交修改。
3. Brain 校验 Schema、Scope、Permission 结果、引用和 Evidence。
4. CAS 只推进一次 Head。
5. 失败方收到 STALE_VERSION；若授权允许，附带当前可见 Head 引用。
6. 调用方重新读取并提交协调后的新操作；不得自动 Last-write-wins。

Idempotency Key 的范围由 ActorRef + Operation + Resource + 相关 ScopeRef 确定；Request Digest 绑定 Canonical Payload。相同 Key/相同 Digest 返回原 Receipt；相同 Key/不同 Digest 产生 Conflict。Receipt 保留必须与 Forget/Retention 协调，不能保留已遗忘内容。

## 9. 不变量

- 已提交 Revision 不得原地更新。
- 每个 Revision 都有稳定身份和 Parent Lineage。
- 每个 Aggregate 同时只有一个权威 Head；并发 Fork 必须显式协调。
- 历史查询返回准确 Revision Identity 和时间依据。
- Event、Valid、Recorded 和 Transaction Time 不得混淆。
- Correction 不得静默改写过去有效性或 Epistemic Status。
- Merge/Split 和 Relation Migration 保留历史引用。
- Context 引用固定准确 MemoryVersion，而不是会变化的 Current Pointer。
- Forget 可以使内容不可用，但不得伪造历史 Sequence 元数据。

## 10. 接口

E 提交带 Expected Base、Source Event/Evidence Ref、Provenance、Actor/Scope/Time 和 Idempotency 的 Candidate Revision。Brain 返回已接受的 Canonical Revision/MemoryVersion 引用，或结构化 Conflict/Defer。F 读取准确 Revision/As-of State，并暴露陈旧/部分 Projection。G 在 Context Entry 中保存 Memory ID + MemoryVersion ID，并独立管理 Context/ChangeSet Version（INT-P1-01）。H 序列化不透明 Version 引用。I 授权 Revision/Forget，并定义哪些历史元数据可保留。跨模块操作按需携带 Schema Version、ActorRef、ScopeRefs、Correlation/Causation 和 Idempotency。

## 11. 错误处理

STALE_VERSION；REVISION_PARENT_MISMATCH；IDEMPOTENCY_CONFLICT；INVALID_TIME_INTERVAL；TIME_PRECISION_LOSS；SCOPE_MISMATCH；PERMISSION_DENIED；REVISION_NOT_FOUND_OR_NOT_VISIBLE；HISTORY_UNAVAILABLE_DUE_TO_FORGET；MIGRATION_MAPPING_INCOMPLETE；SCHEMA_VERSION_UNSUPPORTED。

## 12. 一致性

Aggregate Head 更新和不可变 Revision 追加，必须与 Receipt/Outbox 原子提交。历史读取使用已提交 Transaction Sequence，而不是 Projection 到达顺序。LifecycleEvent Sequence 在每个 Memory Aggregate 内唯一，并确定性折叠。Projection Rebuild 记录 Watermark 和 Schema 兼容性。Entity/Relation Migration 和 Successor Ref 与 Canonical Version/Outbox Intent 一起提交。

## 13. 安全 / Scope

每个 Revision 都携带或继承明确解析的 Ownership/Applicability ScopeRef，并遵循文档化继承规则；不得扩大 Scope。授权必须同时检查 Identity 和准确 Revision。Evidence Ref 独立授权。历史查询不能绕过当前 Policy 或 Forget Suppression。不得从 Revision Snapshot、Log、可逆辅助数据、Cache 或 Provenance 摘录中重建已遗忘 Payload。

## 14. 性能

候选优化：不可变 Snapshot + 紧凑 Current Projection + 周期性派生 Snapshot。限制历史扫描、Parent Chain 深度、Relation Migration 扇出和 Conflict 查询窗口。基准测试 Snapshot 频率、写放大、Temporal Index 选择性、CAS 竞争和历史读取延迟。压缩必须保留所需 Lineage/Retention 义务。

## 15. 可观测性

记录 Aggregate ID、Version/Revision ID、Parent ID、Commit Sequence、Actor/Scope ID、Request Digest、Idempotency Outcome、CAS Conflict、Schema Version、Transaction/Recorded/Valid Time 和 Projection Watermark。指标包括历史深度、Conflict Rate、Stale-write Rate、Reconciliation Latency 和历史查询 Partial Rate。

## 16. 故障场景

- 并发更新：一个 CAS 获胜；失败方协调。
- 响应丢失后的重复 Retry：返回原 Receipt。
- 相同 Idempotency Key 搭配修改后的 Payload：拒绝。
- Projection 滞后：准确 Canonical Read 仍可用，或明确返回降级结果。
- 未知 Schema：安全失败；绝不静默重新解释字段。
- Merge/Split Projection 失败：重放 Migration Record。
- Forget 删除 Payload：只保留 I 批准的不可反向重建审计状态；历史内容读取返回 Unavailable。
- Clock Skew：保留来源时间/精度并独立记录 Commit Time；不得仅按客户端时间戳排序。

## 17. 依赖与开放问题

依赖：Domain Model 时间/认知语义；Canonical Store；Lifecycle Manager；E Proposal/Replay；F Historical Retrieval；G ContextVersion 引用；H ActorRef/Wire 兼容性；I Retention/Forget Policy；Consistency/Recovery。

- OPEN：INT-P0-01 Fact/Claim ADR 及最终 Revision Model。
- OPEN：如果 ADR 选择不同语义，Claim 修正采用稳定 ID Revision 还是 Successor Identity。
- OPEN：ContextVersion/ChangeSet Schema 由 G 拥有；Brain 只提供固定引用。
- OPEN：不确定 TimeValue 规范化和时区策略（DM-006）。
- OPEN：Sequence 范围（Per-Aggregate 还是 Global Commit Stream）。
- OPEN：Schema/Vocabulary Registry 和 Migration 兼容性（DM-013）。
- TO_VALIDATE：不可变 Snapshot 与 Delta Storage、历史查询和迁移性能。

## Phase 3 整改 — 规范 Cursor 边界

以下是不同类型，**MUST NOT** 将它们比较、相加、替代或序列化为一个通用整数：

| 类型 | 权威/范围 | 含义 |
|---|---|---|
| CanonicalCommitCursor | D；单个 Brain Authority | 全局有序的已提交事务位置，仅在成功原子提交时分配 |
| AggregateRevision | D；单个 Aggregate | Aggregate 内单调 Revision，不可全局比较；已提交 Revision 同时携带 CanonicalCommitCursor |
| LifecycleEventCursor | D；单个 Memory Lifecycle Stream | (memory_id, lifecycle_event_sequence, event_id)；按 Memory 连续，同时记录所属 CanonicalCommitCursor |
| IndexWatermark | F；单个 Index/Channel/Partition | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata)；仅表示覆盖进度，绝不是 Forget Proof |
| ForgetFenceCursor | D；Operation + Target Set | (forget_operation_id, fence_generation, target_set_digest)；单调抑制 Epoch，不是 Commit Position 或 Index Watermark |

ContextVersion 仍由 G 拥有；BMCP Delivery/Request ID 仍由 H 拥有；I Permission/Revocation Epoch 仍由 I 拥有。D 不定义其 Wire Encoding。

### Canonical Transaction 可见性与 Replay

成功的 Canonical Transaction 原子暴露对象/Revision 写入、Aggregate Head CAS 更新、LifecycleEvent 追加、CanonicalCommit Record 和可恢复 Outbox Intent。它在 Commit Serialization 时获得一个全局有序 CanonicalCommitCursor。中止/拒绝事务不获得 Cursor；回滚分配不会在已提交 Stream 中造成空洞。As-of Reader 看到整个事务或完全看不到。Cursor 只有在持久化提交后才可见。

Consumer 从最后一个持久化应用 Cursor 之后恢复。允许重新投递，但必须幂等。任何 Consumer 都不得越过缺失 Commit、应用失败或未知 Schema 推进。乱序工作可以暂存，但 Watermark 必须停留在最后连续前缀。历史过期时，使用带 Base Cursor 的一致 Snapshot Bootstrap，再继续；不得跳到 Latest。Outbox 延迟/重试不能改变 Canonical 顺序。Projection Watermark 只报告覆盖进度。

### Lifecycle Event Cursor

LifecycleEvent Sequence 属于单个 Memory Stream，只有 Event 和所属 Transaction 提交时才分配。Consumer 观察到 Gap 时必须 Replay/Reconciliation。Commit Cursor 排序跨 Aggregate 事务；Lifecycle Cursor 排序单个 Memory 的事件。二者不能互相替代。

## Phase 3 整改 — Version 与 Cursor 语义

**DECIDED：** MemoryVersion Sequence 是 Per-Memory AggregateRevision，不是全局 CanonicalCommitCursor。每个已提交 MemoryVersion 都记录两者。EntityVersion 和 RelationRevision 同样携带各自 Revision 和 Commit Cursor。只有成功提交才推进 Aggregate Revision；被拒提案/CAS 失败不消耗 Revision。

**DECIDED：** LifecycleEventCursor 属于单个 Memory Lifecycle Stream，独立于 MemoryVersion AggregateRevision 和 CanonicalCommitCursor。Lifecycle Event 可以与 MemoryVersion 在同一事务提交，但三种值必须保留独立名称和含义。Lifecycle Event 记录所属 Canonical Commit Cursor。

**DECIDED：** IndexWatermark 由 F 拥有，并限定于 Index/Channel Partition。它描述已应用的连续前缀以及 Coverage/Schema 元数据。Rebuild 从一致 Canonical Snapshot Cursor 开始并 Replay；候选可见前检查最新 ForgetFence。Rebuild 进度不得使用 MemoryVersion Sequence 或 LifecycleEventCursor 表示。

### 历史读取与 Replay

历史读取使用已提交 CanonicalCommitCursor/As-of Snapshot 和准确 Aggregate Revision 引用，绝不依赖 Projection 到达顺序。Replay Cursor 是 Exclusive：从最后一个已提交且已应用 Cursor 之后恢复。重复 Replay 必须幂等；缺失 Cursor 阻止连续推进。Replay Window 过期时，使用带 Base Cursor 的一致 Snapshot。由于其他 Aggregate 可能在两个 Revision 之间提交，一个 Aggregate 的历史在全局 Commit Stream 中可以是稀疏的；这不代表该 Aggregate 自己的 Revision Sequence 有缺口。

### Claim / ConflictSet 冻结门禁

Claim Identity、ClaimRevision Schema、ConflictSet Schema 和字段级引用，在 Architecture Governance + B 批准 INT-P0-01 之前都保持 **ADR-BLOCKED**。本文现有 ClaimRevision 表只是备选草图，不是 D 决议。D 会在批准后将 ADR 映射到不可变 Revision 机制；此前不得冻结 Schema、DDL、公共 API 或 Wire Contract。
