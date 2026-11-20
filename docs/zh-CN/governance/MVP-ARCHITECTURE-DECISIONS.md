# MVP 架构决策 — Store / Query / Inject

- 文档 ID：MVP-ARCH-DECISIONS-001
- 版本：1.0
- 日期：2026-11-20
- 状态：**MVP 试点基线——已选定实现配置；跨 Owner 契约仍为条件性状态**
- 英文对应版本：[MVP Architecture Decisions](../../../governance/MVP-ARCHITECTURE-DECISIONS.md)
- 源基线：main@e52594f181d2edb77448adcfed64a0fbdffaf3aa

## 1. 决策摘要

本文定义试点可直接实现的三个公共操作：

1. **Store**：接收强类型、带证据链的记忆写入，并提交一个不可变的规范 MemoryVersion。
2. **Query**：以候选形式返回经过授权的规范 MemoryVersion 引用；索引命中不等于规范事实，也不等于 Context 已应用。
3. **Inject**：创建版本化 Context Delivery，并仅报告实际证据能够证明的最强运行时阶段。只有 G 可以持久化 Applied 决议。

这些是面向 MVP 实现的决策，不代表底层 Owner 契约已全局批准。D 的详细记录布局和事务实现仍为候选；B ADR-001 的 Fact/Claim 语义仍为 ADR-BLOCKED；Storage L1 Option A 已选定，但 L4 物理引擎/部署仍 OPEN；C/G/H/I 的跨 Owner Applied 证据映射尚未冻结。本文保留这些限制。

## 2. 三个核心接口

以下为完整 TypeScript 契约代码，每个代码块均可独立复制。TypeScript 用于表达公共 API；核心实现语言为 Rust。

### 2.1 Store

~~~typescript
/* Store contract — standalone TypeScript */
export type StoreId = string;
export type StoreDigest = string;
export interface StoreActor { principalRef: StoreId; producerRef: StoreId; permissionEpoch: number; }
export interface StoreScope { scopeRef: StoreId; environmentRef: StoreId; }
export interface StoreEvidenceRef { evidenceRef: StoreId; digest: StoreDigest; mediaType: string; }
export interface StoreProvenance {
  sourceEventRef: StoreId; sourceRecordedAt: string; derivationRunRef?: StoreId;
  evidence: readonly StoreEvidenceRef[];
}
export type StoreCandidateValue =
  | { kind: "text"; value: string }
  | { kind: "number"; value: number; unit?: string }
  | { kind: "boolean"; value: boolean }
  | { kind: "entity-reference-candidate"; mention: string; typeHint?: string }
  | { kind: "structured-candidate"; schemaId: string; fields: Readonly<Record<string, string | number | boolean | null>> };
export interface StoreCandidateProposition {
  schemaVersion: "candidate-proposition/1"; candidateRef: StoreId;
  subject: { label: string; typeHint: string }; predicate: { name: string; typeHint: string };
  value: StoreCandidateValue; scope: StoreScope; observedAt?: string; validFrom?: string;
  validUntil?: string; epistemicQualifier?: "reported" | "observed" | "inferred" | "uncertain";
  provenance: StoreProvenance;
}
/** 中立记忆封套，不是规范 Fact 或 Claim。 */
export interface StoreMemoryContent {
  schemaVersion: "memory-content/1"; title: string; bodyText: string;
  tags: readonly string[]; candidatePropositions: readonly StoreCandidateProposition[];
  provenance: StoreProvenance;
}
export interface StoreCommitRequest {
  actor: StoreActor; scope: StoreScope; idempotencyKey: string;
  semanticRequestDigest: StoreDigest; memoryRef?: StoreId;
  expectedParentVersionRef?: StoreId; content: StoreMemoryContent;
}
export interface StoreCommitReceipt {
  memoryRef: StoreId; memoryVersionRef: StoreId; aggregateRevision: number;
  canonicalCommitCursor: string; lifecycleEventRef: StoreId; committedAt: string;
  contentDigest: StoreDigest; replayed: boolean;
}
export type StoreErrorCode =
  | "INVALID_INPUT" | "AUTHORIZATION_DENIED" | "PERMISSION_EPOCH_STALE"
  | "FORGET_FENCE_ACTIVE" | "PROVENANCE_INCOMPLETE" | "VERSION_CONFLICT"
  | "IDEMPOTENCY_CONFLICT" | "STORAGE_UNAVAILABLE" | "OUTCOME_UNKNOWN" | "OUTCOME_IN_DOUBT";
export interface StoreError {
  code: StoreErrorCode; message: string; operationRef: StoreId;
  retry: "NEVER" | "READ_BACK_SAME_OPERATION" | "RECONCILE_SAME_OPERATION";
}
export type StoreResult<T> = { ok: true; value: T } | { ok: false; error: StoreError };
export interface Store {
  /** 原子提交 Version、Head CAS、Provenance/Evidence、LifecycleEvent、Receipt/Cursor 和 Outbox。 */
  commit(request: StoreCommitRequest): Promise<StoreResult<StoreCommitReceipt>>;
}
~~~

### 2.2 Query

~~~typescript
/* Query contract — standalone TypeScript */
export type QueryId = string;
export interface QueryActor { principalRef: string; agentInstanceRef: string; permissionEpoch: number; }
export interface QueryScope { scopeRef: string; environmentRef: string; }
export interface QueryRequest {
  queryId: QueryId; actor: QueryActor; scope: QueryScope; text: string; limit: number;
  filters?: { tagsAny?: readonly string[]; sourceEventRefs?: readonly string[]; recordedAfter?: string; recordedBefore?: string; };
}
export interface QueryCandidate {
  memoryRef: string; memoryVersionRef: string; title: string; excerpt: string; score: number;
  recordedAt: string; provenanceRefs: readonly string[]; contentDigest: string;
}
export interface QueryResult {
  queryId: QueryId; candidates: readonly QueryCandidate[];
  completeness: "COMPLETE" | "PARTIAL" | "UNAVAILABLE";
  indexWatermark?: string; evaluatedPermissionEpoch: number; evaluatedAt: string;
}
export type QueryErrorCode =
  | "INVALID_QUERY" | "AUTHORIZATION_DENIED" | "PERMISSION_EPOCH_STALE"
  | "FORGET_FENCE_ACTIVE" | "INDEX_UNAVAILABLE" | "CANONICAL_READ_UNAVAILABLE";
export interface QueryError { code: QueryErrorCode; message: string; retryable: boolean; }
export type QueryResponse = { ok: true; value: QueryResult } | { ok: false; error: QueryError };
export interface Query {
  /** 返回前重新验证规范版本、Scope、当前授权和 Forget 可见性；索引行与分数不是权威。 */
  search(request: QueryRequest): Promise<QueryResponse>;
}
~~~

### 2.3 Inject

~~~typescript
/* Inject contract — standalone TypeScript */
export interface InjectActor {
  principalRef: string; agentInstanceRef: string; sessionRef: string; permissionEpoch: number;
}
export interface InjectScope { scopeRef: string; environmentRef: string; }
export interface InjectRequest {
  actor: InjectActor; scope: InjectScope; contextRef: string;
  expectedContextVersionRef?: string; deliveryIdempotencyKey: string; queryId: string;
  memoryVersions: readonly { memoryRef: string; memoryVersionRef: string; contentDigest: string; }[];
  managedRegion: { regionRef: string; inventoryDigest: string; contentDigest: string; };
}
export type InjectStage =
  | "CONTEXT_VERSION_COMMITTED" | "DELIVERY_INTENT_COMMITTED" | "DELIVERY_ACCEPTED"
  | "MANAGED_REGION_MATERIALIZED" | "FINAL_REQUEST_SUBMITTED" | "REJECTED" | "UNKNOWN" | "IN_DOUBT";
export type InjectAppliedStatus = "NOT_APPLIED" | "FULL_APPLIED";
export interface InjectEvidence {
  inferenceRequestRef?: string; deliveryRef: string; contextVersionRef: string;
  adapterInstanceRef?: string; boundaryRef?: string; adapterCapabilityEpoch?: number;
  permissionEpoch: number; forgetFenceRef: string; managedRegionInventoryDigest: string;
  managedRegionContentDigest: string; coverage: "COMPLETE" | "PARTIAL" | "BYPASSED" | "UNKNOWN";
  evidenceTier: 1 | 2 | 3;
  providerHandoff: "HANDOFF_ACCEPTED" | "HANDOFF_REJECTED" | "NOT_INVOKED" | "UNKNOWN" | "IN_DOUBT";
}
export interface InjectResult {
  deliveryRef: string; contextVersionRef: string; stage: InjectStage;
  applied: InjectAppliedStatus; evidence?: InjectEvidence; appliedRecordRef?: string; reasonCode?: string;
}
export type InjectErrorCode =
  | "AUTHORIZATION_DENIED" | "PERMISSION_EPOCH_STALE" | "FORGET_FENCE_ACTIVE"
  | "CONTEXT_VERSION_CONFLICT" | "DELIVERY_REJECTED" | "EVIDENCE_INCOMPLETE"
  | "PROVIDER_OUTCOME_UNKNOWN" | "PROVIDER_OUTCOME_IN_DOUBT" | "APPLIED_COMMIT_UNAVAILABLE";
export interface InjectError {
  code: InjectErrorCode; message: string;
  retry: "NEVER" | "RECONCILE_SAME_DELIVERY" | "RECONCILE_SAME_PROVIDER_ATTEMPT";
}
export type InjectResponse = { ok: true; value: InjectResult } | { ok: false; error: InjectError };
export interface Inject {
  /** 只有 G 对精确最终请求的完整 Tier-1 证据完成持久化 Applied Commit 后，才允许 FULL_APPLIED。 */
  deliver(request: InjectRequest): Promise<InjectResponse>;
}
~~~

## 3. 技术选型

| 项目 | MVP 选型 | 状态与边界 |
|---|---|---|
| 核心实现语言 | **Rust stable，Edition 2024** | 遵循 TAB-001 的 Rust 主语言方向。 |
| 异步运行时 | **Tokio** | 用于 IO 和后台 Worker；首版正确性关键状态迁移先留在单进程。 |
| 序列化 | **Serde** | 使用带版本的强类型封套；不得把任意 Payload 反序列化为规范 Fact/Claim。 |
| 错误处理 | **thiserror**（领域/存储库）、端口强类型 Result、**anyhow**（仅进程/CLI 边界） | 保留稳定错误码和重试策略。 |
| 试点持久化 | **SQLite WAL**，置于 Storage Adapter 后 | TAB-001 对首个原型的条件性推荐，不构成 L4 冻结。 |
| 事务拓扑 | **每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain** | Storage/D L1 Option A；SQLite 锁与事务行为必须通过竞态/崩溃测试。 |
| 标识符 | UUIDv7 字符串；Rust 中使用不同 Newtype | 不同 Cursor 命名空间不得互相替代。 |
| 规范数据 | 不可变 MemoryVersion、Aggregate Head CAS、追加式 LifecycleEvent、CanonicalCommit Receipt/Cursor、幂等 Receipt、持久 Outbox | 原子提交，或采用经证明的可恢复等价方案。 |
| 检索索引 | SQLite FTS5 词法索引，作为可重建投影 | IndexWatermark 不等于 CanonicalCommitCursor 或 ForgetFenceCursor。 |
| 向量/图 | 延后 | 首个垂直切片不依赖向量/图；不得从共现推断关系。 |

### 数据结构规则

- Canonical Memory 身份和不可变 MemoryVersion 由 D 持有。
- 写入必须携带类型化 Source Event/Evidence/Provenance 引用；来源不可用时必须记录明确允许的 unavailable 原因，不能静默省略。
- B ADR-001 处于 ADR-BLOCKED 期间，命题数据只能作为带版本的中立 CandidateProposition/ExtractionIR 封套。不得引入规范 FactRef、ClaimRef、Fact/Claim DDL 或 Wire discriminant。
- CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor、IndexWatermark、ForgetFenceCursor、PermissionEpoch、ContextVersion 和 AdapterCapabilityEpoch 是不同强类型命名空间，不是可互换整数。
- 搜索索引、缓存、摘要片段和 Embedding 都只是投影。使用前必须根据规范版本、授权和 Forget 状态重新验证。
- Context 是 G 所有的、由不可变规范引用组成的版本化选择；修改 Context 不得修改 Canonical Memory。

### 错误与重试规则

1. 领域/契约失败返回强类型错误；不得吞异常，也不得把所有失败转换成 false 或空结果。
2. 相同幂等键 + 相同语义摘要返回原 Receipt/结果；相同键 + 不同摘要返回 IDEMPOTENCY_CONFLICT。
3. Version/CAS 冲突必须显式返回；禁止 last-writer-wins 覆盖或隐式合并。
4. 超时、ACK 丢失、进程崩溃或缺少数据库行不能证明操作失败。必须用相同稳定操作身份处理 UNKNOWN/IN_DOUBT；可能已有副作用时不得换新的 Provider Key。
5. 重试使用新的执行 AttemptId/LeaseId，但保留逻辑 Work/Operation 身份。恢复前重新检查 PermissionEpoch 和 ForgetFence。
6. 规范提交不得部分可见。Version/Head、LifecycleEvent、Receipt/Cursor 和 Outbox 意图属于同一原子集合。
7. Query 索引滞后必须报告 PARTIAL/UNAVAILABLE；不得伪造完整性或把陈旧结果冒充当前结果。
8. Inject 阶段不得折叠成通用成功布尔值。只有 G 的持久化判定可以产生 FULL_APPLIED。

## 4. 实现边界

### MVP 要做

- 将 Store 实现为唯一规范写入端口，由 D 负责身份、版本、Head 和事务语义。
- 实现持久幂等、Expected-Version CAS、Provenance/Evidence 关联、追加式 LifecycleEvent 和事务 Outbox。
- 使用 FTS5 实现 Query，提供有界 Top-K、显式过滤、Provenance 引用、完整性状态和 IndexWatermark。
- Query 结果暴露或注入前，重新验证规范版本、Scope、I 当前授权/PermissionEpoch 和 D ForgetFence。
- 使用 G ContextVersion 与 Delivery Intent 实现 Inject；首版采用受控进程内 H Adapter/Runtime Harness，并在可用平台设置可观测的 C 最终请求提交 Hook。
- 将 G Applied 单独持久化；只有精确最终不可变请求具备 Tier-1 完整证据且所有必要 Owner 证明均有效时才提交。
- 增加幂等重放/冲突、CAS 竞态、提交前后崩溃、Outbox 重复、权限撤销、Forget 竞态、陈旧 Context Delivery、不完整证据、Provider UNKNOWN/IN_DOUBT 和 Applied 重放测试。

### MVP 不做

- B ADR-001 未决时不得冻结或发明规范 Fact/Claim 身份。
- 不允许 Agent、Adapter、Provider 或外部 Memory 产品直接写规范存储。
- 不得将 Event Accepted、Compiler Completed、Canonical Committed、Index Published、Delivery ACK、Materialized、Provider Response 和 Workflow Completed 混为一谈。
- 没有精确最终请求观测、真实请求身份、完整 Managed Region Digest 和 G 持久 Applied Commit 时，不得声称 Full Applied。
- 不得从 Applied 推断模型注意、理解、记住、行为遵从或回答正确。
- Store/Query/Inject 不声明全局 Forget 完成或物理擦除；只执行 D 本地抑制，全局完成归 I/D 治理。
- 不引入微服务、Kafka、Kubernetes、托管向量数据库、强制云端推理、图数据库、自主 Agent 规划器或第二规范存储。
- 首个垂直切片不要求 Vector Search、Embedding、Graph Traversal、Summarization 或 LLM Extraction。
- 在 Storage 验证证据形成前，不得声称 SQLite WAL 已证明满足 L1 串行化、崩溃恢复、HA、PITR 或 Restore Quarantine。

## 5. 验收门槛

接口层面的试点基线已具备实现条件；但在以下项目均有可执行证据前，**不得称为生产认证**：

- Store：Version/Head/Event/Receipt/Cursor/Outbox 原子提交；CAS 失败无可见副作用；同键重放幂等；摘要变化冲突。
- Query：授权与 Forget 重新验证；陈旧投影不能绕过规范读取；Index Watermark 只能跨连续前缀推进。
- Inject：Delivery 与 Materialization 分离；Tier-2/Tier-3 不能产生 Full Applied；校验精确最终请求 Digest；UNKNOWN/IN_DOUBT 禁止盲重试；G Applied 在崩溃/重放下幂等。
- Storage：实际 SQLite WAL 事务配置通过并发写入、进程崩溃和恢复测试，满足所选 L1 拓扑。
- 文档：同一变更集完成中英文语义一致性和链接检查。

## 6. 权威与变更控制

本 MVP 配置不批准 B ADR-001，不替代 D/E/F/G/H/I/Storage Owner 契约，不冻结 Storage L4，也不认证 C/G/H/I 生产证据。若本文实现便利性与 Owner 契约冲突，以 Owner 契约和已批准 ADR 为准。任何涉及规范身份、事务原子性、授权、Forget、Applied 语义或 Wire 身份的变更，都必须取得相关 Owner/ADR 决策。

**裁定：** Store / Query / Inject 契约已为受限试点定义。Rust + Tokio + Serde + SQLite WAL 是具体首个原型技术栈；SQLite 仍为条件性选择，等待 Storage 验证。本文不声称生产符合性或端到端执行已完成。
