# Entity 与 Relationship Manager（实体与关系管理器）

- 文档 ID：D-ENTITY-RELATION-001
- 版本：1.0
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：DEREFERENCED — 保留历史源 Blob `14697658d4d873381ca8d4e3bed7c1170368ec29`；当前仓库不存在可解析的规范性源文件。
- 审查时源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- 源规范：DEREFERENCED — 原规范源路径 `03-memory-brain/entity-and-relationship-manager.md` 在当前 main tree 中不存在；替代物：[英文对照版](../../en/03-memory-brain/entity-and-relationship-manager.md)（Blob `c5a545e985c7a46b09c68205ea1b0bde3b985327`；仅为对照文本，不是规范性替代源）。
- 对应英文：[Entity and Relationship Manager](../../en/03-memory-brain/entity-and-relationship-manager.md)
- 状态：身份和类型化时间关系原则为 DECIDED；Merge/Split 和词汇细节为 CANDIDATE/OPEN
- 相关问题：INT-P0-02/03、INT-P1-02/03/06；DM-005/006/007/009/010/013

## 1. 目的与范围

管理具有身份的 Entity 和由 Evidence 支持的类型化 Relation，避免将身份与名称、文本提及、共同出现或 Graph Projection 混淆。保留历史身份决策，以及 Merge/Split 操作中的引用迁移。

拥有 Entity Identity/Version、Alias/Mention 链接、解析决策、Merge/Split Record、Relation Identity/Revision、类型化 Predicate/Value、方向、有效性、Evidence、Scope 约束和 Canonical Graph Reference 一致性。不拥有 Retrieval Ranking、全局 Policy、Event Ingestion 或物理删除。

## 2. 职责与非职责

- 分配稳定不透明 Entity ID，身份不依赖展示标签。
- 根据 Evidence 和 Scope 约束解析引用；有歧义时返回 Ambiguous，不猜测。
- 维护带版本的属性/别名及其 Provenance/Validity。
- 强制执行类型化 Relation 端点、方向、时间有效性、Evidence 和 Scope。
- 将 Entity Merge/Split 和 Relation Migration 记录为不可变操作。
- 提供有界、经过授权的 Graph Traversal 和历史查询。
- 确保 Forget Dependency Discovery 能找到 Entity/Relation 引用及派生投影。

禁止仅凭名称推断身份、无限制跨 Scope 解析、真伪裁定、Relation 排序、向量相似度策略、Agent 规划或授予 Permission。Display Name 是标签，不是身份 Key。

## 3. 领域对象

- **EntityIdentity：** entity_id、owner_scope_ref、applicability_scope_refs、entity_kind、created_at、created_by_actor_ref、identity_status。稳定且永不复用。
- **EntityVersion：** entity_version_id、entity_id、sequence、parent_version_id、canonical_attributes、attribute_validity、content_digest、alias_refs、provenance_refs、actor_ref、recorded_at、schema_version。不可变描述修订。
- **Alias：** alias_id、entity_id、normalized_label、language/locale、alias_kind、valid_time、source/evidence refs、scope refs、confidence/method metadata。它是带 Scope/时间限定的标签，永远不是身份。
- **MentionRef：** 来源对象/版本、Locator、Surface Form、候选 Entity Ref 和解析状态。Mention 不自动成为 Entity。
- **EntityResolutionDecision：** decision_id、mention_ref、candidate_entity_refs、selected_entity_ref 或 unresolved、evidence_refs、method_ref、actor_ref、scope_refs、recorded_at、status。歧义必须明确保留。
- **EntityMergeRecord：** merge_id、source_entity_ids、survivor_entity_id、source versions、evidence refs、relation migration refs、scope refs、actor、reason、commit sequence、timestamp、correction/supersession ref。显式 Redirect Map 保留历史查询。
- **EntitySplitRecord：** split_id、source_entity_id、new_entity_ids、partition criteria、受影响 mention/claim/relation refs、evidence refs、scope refs、actor、reason、commit sequence、timestamp、correction ref。记录引用如何分区，不改写历史。
- **RelationIdentity：** relation_id、canonical subject TypedObjectRef、typed predicate、canonical object TypedValue/TypedObjectRef、direction、owner/applicability scopes、created metadata。
- **RelationRevision：** relation_revision_id、relation_id、sequence、parent_revision_id、validity interval、epistemic status、lifecycle state、evidence/provenance refs、confidence assessment ref、author ActorRef、reason、recorded_at、schema version、digest。不可变。
- **RelationMigrationRecord：** migration_id、operation kind、old/new relation refs、affected Entity refs、evidence、scope、actor、reason、sequence 和 timestamp。

## 4. 类型化数据模型

TypedPredicate 包含 Vocabulary Namespace、Predicate Code/Version、Arity、Endpoint Type Constraint、Symmetry/Inverse 声明、时间行为和弃用元数据。TypedValue 包含 Value Kind、Canonical Encoding、可选 Unit/Locale、Schema/Vocabulary Version，以及显式 Unknown/Null 语义。自由格式 Predicate 不得静默视为 Canonical Vocabulary。

TypedObjectRef = object_type + 不透明 object_id + 可选不可变 version/revision ID + 可选 scope_ref + reference purpose。ScopeRef = scope_id + 已注册 scope_kind + owner_ref + 可选 parent_scope_id + status/version。ActorRef = actor_kind + 稳定 Subject ID + issuer/authentication ref + 可选 delegation chain；display_name 仅用于描述。TimeValue = 规范化边界、精度、时区、确定性、来源原话和 source_ref。TimeInterval = start/end TimeValue、边界约定和显式 Unbounded/Unknown 标记。ContentRef = content_id、media/content kind、不可变 Version/Digest、Locator/Access Class、Availability State 和来源身份。这些是最低候选结构；H/I 最终确定身份/认证字段。

Relation 方向必须明确。对有向 Predicate，Subject/Object 位置具有规范意义。对称 Relation 在词汇表中声明对称性；逆向遍历可以派生。**CANDIDATE 默认方案：** 只持久化一条 Canonical 有向边，并派生逆向遍历；除非审计/领域语义要求，否则不复制逆向记录。

## 5. 状态机

Entity Identity：Provisional → Resolved → Merged 或 Split；Resolved 在明确策略下可以变为 Retired。Merged/Split Identity 仍作为带 Redirect/Partition 元数据的历史身份可寻址；ID 永不复用。

Relation Lifecycle：Proposed → Active → Superseded 或 Retracted。新 Revision 取代旧 Revision，但不修改旧 Revision。Retraction 保留历史和原因。Valid Time 独立于记录 Lifecycle；Active Relation 也可以有有限有效区间。

## 6. 操作

CreateEntity；AddAlias；ResolveMention；UpdateEntityVersion(expected_version)；MergeEntities；SplitEntity；CreateRelation；ReviseRelation(expected_revision)；RetractRelation；SupersedeRelation；TraverseRelations(scope, depth, fanout, as_of)；ResolveHistoricalReference；RebuildGraphProjection。

**Merge 工作流：** 授权来源/Survivor Scope；验证属于同一允许的所有权域或存在明确共享；评估身份 Evidence；创建不可变 Merge Record 和 Survivor Version；创建 Redirect；通过显式映射迁移当前引用；历史引用保持不变；为 F/G 发出变更事件并重建投影。仅名称相似不得授权跨 User/Project/Environment 合并。

**Split 工作流：** 授权；定义由 Evidence 支持的分区；创建新 Entity Identity；显式分配受影响的当前引用；记录未解决/有歧义引用；保留旧历史 Version 和源 Entity Identity；发出 Migration Record 和下游协调事件。不得自动拆分所有历史引用。

## 7. 不变量

- Entity ID 不透明、稳定且永不复用。
- Alias/Display Name/Mention 本身永远不能确立身份。
- 解析受 Scope 限制；不允许隐式跨 User/Project/Agent/Environment 合并。
- 每个 Entity/Relation 都具有明确的 Ownership/Applicability ScopeRefs。
- 每个 Relation 都有类型化 Predicate、Direction、Endpoint Type、Lifecycle 和 Validity 语义。
- Evidence/Provenance 独立引用、独立授权。
- Merge/Split 采用追加式、可审计、经 Scope 检查的操作；历史修正只能通过新 Correction Record 实现，不做破坏性回滚。
- Graph Projection 可重建；Canonical Relation Revision 是权威。
- Forget Dependency Discovery 能枚举引用和派生物。

## 8. 接口

E 提交 Entity/Relation 提案、Mention、Alias Evidence、类型化 Predicate/Value、Time 和 Scope；Manager 返回 Provisional/Resolved ID、Ambiguity 或 Validation Error。E 不得仅根据 Display Name 相似度合并身份。

F 请求带 Scope 的 Relation Traversal，并明确 Depth/Fanout/Deadline 和精确 Version/As-of 语义。每条 Edge 和 Target Node 在影响 Ranking、Aggregation 或 Result Count 前都必须进行 Scope Filter 和授权（INT-P0-02）。截断必须明确标记。

G 可以把 Entity/Relation Ref 作为解释性引用保存，但 ContextVersion/ChangeSet 仍由 G 拥有（INT-P1-01）。H 传输类型化不透明 Ref，并拥有 Protocol Schema。I 授权 Merge/Split、Relation 修改、跨 Scope 共享、Forget 和 Retention。E/F/G/H/I 不得把 Alias 当作稳定身份。

## 9. 错误处理

ENTITY_NOT_FOUND_OR_NOT_VISIBLE；AMBIGUOUS_ENTITY；ALIAS_SCOPE_MISMATCH；ENTITY_MERGE_CONFLICT；ENTITY_SPLIT_PARTITION_INCOMPLETE；STALE_ENTITY_VERSION；INVALID_PREDICATE；ENDPOINT_TYPE_MISMATCH；RELATION_SCOPE_MISMATCH；INVALID_VALID_TIME；RELATION_RETRACTED；GRAPH_TRAVERSAL_LIMIT；PERMISSION_DENIED；IDEMPOTENCY_CONFLICT。错误只能披露已授权元数据。

## 10. 一致性

Entity/Relation Canonical Record 和 Migration Event 与 Outbox/Change-feed Intent 一起提交。Projection Rebuild 使用不可变 Revision 和 Migration Record。历史 Ref 解析到原始 Identity/Revision；只有调用方获得授权且明确请求 Current Mapping 时，“当前 Canonical Identity”查询才可跟随 Redirect。Relation Endpoint Ref 必须在所引用 Version 上解析到兼容的 Entity/Memory/Event 类型。Merge/Split Migration 不得隐式修改历史。

## 11. 安全 / Scope

身份解析和 Graph Traversal 必须从已解析 ScopeRefs 和授权开始。跨 Scope 身份等价需要明确 Grant 和来源 Owner 批准。Evidence 访问独立检查。Scope Filter 必须先于 Candidate Generation/Graph Expansion；每条 Edge 和 Destination 都要重新检查。不得通过 Alias 匹配数量、Ambiguity Message、Graph Degree、Ranking 或错误详情泄露受保护 Entity 是否存在。依赖环境的 Entity/Relation 必须具有 Environment Identity。

## 12. 性能与可观测性

限制 Relation Fanout、Depth、Page Size 和时间预算。提供 Cursor 和明确的 Partial/Truncated 状态。可以批量 Endpoint Validation/Authorization，但必须保留逐 Edge 检查。测量 Alias Collision、Resolution Ambiguity、Merge/Split Migration 大小、Relation Traversal、Temporal Filter 和 Projection Rebuild。

跟踪 Resolution Decision/Ambiguity、Merge/Split 数量、Redirected Reference 数量、未解决历史引用、Relation Revision Conflict、Graph Projection 滞后、Traversal Truncation 和 Scope Denial。携带 Actor、Scope、Correlation/Causation、Operation、Object/Revision ID 和时间戳；必要时对 Alias/Source Payload 脱敏。

## 13. 故障场景

- Alias Collision：返回 Ambiguous，不合并。
- 跨 Scope 候选匹配：除非明确共享 Grant 授权，否则排除。
- Merge Commit 成功但 Projection Migration 失败：Canonical Merge Record 是权威；Replay Migration。
- Split 存在未解决历史 Mention：保留未解决映射，不猜测。
- Forget 后 Relation Endpoint 不可用：只保留策略允许的 Tombstone/Reference State，并标记 Graph Edge 不可用。
- 达到 Traversal Limit：返回带 Truncation Marker 的 Partial Result，不得虚报完整。
- Vocabulary Version 未知：拒绝不安全解释，或仅在兼容策略明确允许时保留不透明扩展。

## 14. 依赖与开放问题

依赖：B 的 Type/Temporal 语义；Canonical Store 的不可变 Revision/Outbox；E 的 Mention/Proposal/Evidence；F 的 Graph Retrieval；G 的 Pinned Ref；H 的 ActorRef/Wire Ref；I 的 Scope Grant/Permission/Forget/Retention；Predicate 兼容性所需的 Vocabulary Registry。

- OPEN：通用 Scope Parent/Child 和 Multi-owner Algebra（DM-005）。
- OPEN：ActorRef Issuer/Delegation 和 Workload Identity（INT-P1-03）。
- OPEN：Vocabulary Registry、扩展和弃用规则（DM-013）。
- OPEN：Claim ADR 后历史 Claim 引用的 Merge/Split Policy（DM-009）。
- OPEN：除派生遍历外是否还需要显式逆向 Relation Record。
- OPEN：跨 Relation/Entity 派生的 Provenance 链接是否要求 DAG/环约束（DM-007）。
- TO_VALIDATE：Relation Fanout/Depth 和 Merge/Split Migration 基准。

## Phase 3 整改 — 历史安全的 Merge/Split 与 Relation Migration

**D 领域契约层面的 DECIDED：** Entity ID、EntityVersion ID、Relation ID 和 RelationRevision ID 都不可变且永不复用。Merge/Split 不得改写历史对象 Payload、旧 MemoryVersion、Claim/Evidence/Provenance Ref 或既有 RelationRevision。它只能追加不可变 Migration Record 并发出 Canonical Change/Outbox Event。

### Entity Merge

EntityMergeRecord **MUST** 包含 Operation ID、有序 Source Entity ID 和准确 Source EntityVersion Ref、Survivor Entity ID 及其前后准确 Version、Evidence/Provenance Ref、Scope Ref、Actor Ref、Reason、Canonical Commit Cursor、Redirect Mapping、受影响当前引用清单 Digest、RelationMigrationRecord Ref 和 Correction/Supersession Pointer。来源身份仍可作为历史身份解析。历史查询返回原 ID/Version；只有明确授权的“Resolve Current Identity”查询才可跟随 Redirect。Redirect Traversal 必须检查环并限制深度。

Merge 不是破坏性 Alias 改写。当前引用只能通过与 Merge 一起提交的逐引用显式映射迁移。有歧义的引用保持未解决。Relation Edge 不得仅因为端点 Redirect 到同一 Survivor 就自动去重；必须评估并记录语义等价性、Scope、Validity 和 Evidence。

### Entity Split

EntitySplitRecord **MUST** 包含 Source Entity ID/准确 Version、新分配的 Entity ID/Genesis Version、由 Evidence 支持的分区标准、准确受影响当前引用集合、逐引用目标映射或明确未解决结果、受影响 Relation Migration Ref、Actor/Scope/Reason、Canonical Commit Cursor 和 Correction Pointer。源 Entity 和所有历史 Version 始终可寻址。只有 Evidence 充分时才拆分当前引用；有歧义的引用根据明确映射决策保留在历史来源或标记未解决。不得自动改写历史引用。

### Relation Migration

RelationMigrationRecord 将准确旧 RelationRevision（包括 Endpoint Ref）映射到零个、一个或多个后继 Relation ID/Revision，或明确的 Retired/Unresolved 结果。每个后继都是新的不可变 Revision（若 Predicate/Endpoint 语义发生实质变化，则创建新的 Relation Identity），并具有新的 Subject/Object Ref、Evidence/Provenance、Validity、Scope 和 Reason。旧 Revision 仍可查询历史。Migration 必须与 Canonical Migration Record/Outbox Intent 原子提交；Projection 失败通过 Replay 修复，不能修改历史。

对于 Merge，只有重新验证 Scope/Predicate 约束后，端点 Redirect 的 Edge 才可以创建使用 Survivor Endpoint 的后继 Revision。对于 Split，只有 Endpoint Partition Evidence 确定正确的新 Entity 时，Edge 才能分配到后继；否则当前遍历标记为 Unresolved/Retired，同时保留旧 Revision 供授权历史查询。Symmetric/Inverse Traversal 仍由 Vocabulary 派生；默认不创建重复逆向记录。

### 查询语义与审计

- 历史查询：返回原始存储的准确 Entity/Relation Identity 和 Revision；不得静默跟随 Redirect。
- 当前身份查询：可以跟随已授权 Redirect/Partition Map，并返回 Migration Chain 和 Mapping Confidence/Status。
- Graph Traversal：只使用当前 Successor Revision；陈旧 Projection 从 Canonical Migration Record 失效/重建，不得复活已 Retire 的 Edge。
- Forget Dependency Discovery：按 I 的 Retention Policy 纳入原始/后继 Identity、Migration Record 和所有当前/历史引用；Redirect 不等于删除。

### 验收用例

1. Merge 后执行历史查询，返回原 Source ID/Revision；当前查询按记录的 Redirect 跟随，并提供审计链。
2. Merge 后 Split，创建新 ID 和明确 Correction Chain；不改写先前 Merge 或旧引用。
3. 有歧义的 Split 引用保持 Unresolved；不猜测分配。
4. Relation Endpoint Migration 创建新 Revision/Record；旧 Edge 历史保持完整。
5. Merge/Split 后 Projection Rebuild 得到相同当前 Graph，并保留历史查询语义。
6. 缺少 I 授权 Grant Evidence 时，跨 Scope Merge/Split 必须 Fail-closed。
