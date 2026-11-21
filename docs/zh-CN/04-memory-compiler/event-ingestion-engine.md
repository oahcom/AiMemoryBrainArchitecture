---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "04-memory-compiler/event-ingestion-engine.md @ b463e01a9d831e5678041c370065472b3924c0b3"
        - "OWNER-DECISION-FACT-CLAIM-001 (semantic identity dependency)"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Canonical source and bilingual mirror path verified; candidate/open implementation contracts remain unfrozen."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Memory Compiler design specification: event-ingestion"
    canonical_scope_id: "memory-compiler/event-ingestion"
    canonical_scope_keywords:
      - event
      - ingestion
      - outbox
      - queue
      - accepted
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/event-ingestion-engine.md"
    en: "docs/en/04-memory-compiler/event-ingestion-engine.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/event-ingestion-engine.md"
---

# 事件接收引擎

- 规范源：[event-ingestion-engine.md](../../../04-memory-compiler/event-ingestion-engine.md)
- 规范源 Blob：b463e01a9d831e5678041c370065472b3924c0b3

- 文档 ID：E-INGEST-001
- 版本：1.0
- 对应英文：[Event Ingestion Engine](../../en/04-memory-compiler/event-ingestion-engine.md)
- 状态：Accepted 语义和安全不变量已 DECIDED；Outbox/Queue 拓扑为 CANDIDATE；容量和排序目标为 TO_VALIDATE
- Owner：Memory Compiler / MC-01
- 集成关系：INT-P0-02/03；INT-P1-03/04；C Telemetry Identity 和 Source Semantics

## 1. 目的

将经过认证的来源事件接收到 Brain 的持久化托管边界内，并提供真实的 Receipt 语义、幂等重试、可恢复的 Compile Intent 和明确的 Backpressure。Ingestion 是持久化边界，不是语义验证，也不代表 Memory 已编译。

## 2. 范围

包括 Envelope 校验、Source Identity 绑定、Scope 解析、Permission 检查、Payload 完整性、Idempotency、Event 持久化、Processing Intent/Outbox、Receipt、Admission Control、Queue Priority、Retry、DLQ、Replay 和 Crash Recovery。

不包括 H 的 Agent Telemetry Mapping/BMCP Wire Format；D 的 Canonical Memory 语义/Lifecycle；I 的 Global Policy/Retention 定义；Runtime Recall；以及 Dispatch 之后的 Compilation Stage。

## 3. 职责

校验带版本的 Event Envelope；将已认证 Producer 绑定到 Source Identity；解析明确的 Scope（包括 Environment Scope）；授权 event.ingest 并落实 Retention 义务；将不可变 Source Event、Payload Ref/Digest、Idempotency Record、Receipt 和 Processing Intent 作为一个可恢复单元持久化；只有 Durable Commit 后才返回 Accepted；将 event_time 与 Brain recorded_at 分开保存；重建待处理 Work；处理前重新检查 Authorization 和 Forget/Retention Fence。

## 4. 非职责

Ingestion 不判断陈述是否真实、不提取 Claim、不推断 Outcome、不解析语义 Entity、不创建 Canonical Memory、不授权未来 Action，也不保证 Index 可见性。Accepted 不等于 Compiled、Verified、Indexed 或 Activated。

## 5. 输入 / 输出

输入：已认证 Principal/Producer Context、Schema Version、Source Type/ID、Source Payload 或持久化 ContentRef、ScopeRefs、可选 EnvironmentScope、Event Kind/Classification、带来源精度/时区的 event_time、Idempotency Key、Payload Digest、Retention Class、Sensitivity、Correlation/Causation ID 和 Source Trust Metadata。

输出：AcceptedReceipt，或类型化 Rejection/Retryable-Unavailable。Receipt 包含稳定 event_id、receipt_id、accepted_at/recorded_at、Idempotency Identity Fingerprint、Payload Digest、Schema Version 和 processing_state=Pending。它不得声称已经完成 Compilation。

## 6. 数据模型

### 6.1 EventEnvelope（逻辑模型；Wire 字段名由 H 拥有）

~~~text
EventEnvelope {
  schema_version: Version
  event_kind: EventKind
  source_type: SourceType
  source_id: OpaqueIdOrNamespacedString
  producer_actor_ref: ActorRef
  producer_instance_ref: ActorRef?
  scope_refs: ScopeRef[]
  environment_scope_ref: ScopeRef?
  classification: observed | reported | planned | predicted |
                  attempted | outcome | administrative | unknown
  payload_ref: ContentRef
  payload_digest: Digest
  content_type: MediaType
  event_time: TimeValue?
  source_recorded_at: TimeValue?
  idempotency_key: OpaqueString
  retention_class: RetentionClass
  sensitivity: Sensitivity
  trust_metadata: SourceTrustMetadata
  correlation_id: OpaqueId
  causation_id: OpaqueId?
  stream_ref: TypedObjectRef?
  stream_sequence: u64?
}
~~~

recorded_at 由 Brain 在持久化接收时分配，并且不可变。Source 提供的时间戳必须单独标注来源。依赖 Environment 的 Event 必须携带 Environment Scope；展示标签绝不能充当稳定 Scope Identifier。

### 6.2 接收事务

~~~text
IngressCommit {
  event_record: ImmutableEvent
  payload_record_or_durable_ref: ContentRef
  idempotency_record: IdempotencyRecord
  accepted_receipt: AcceptedReceipt
  compile_outbox_record: OutboxRecord
  transaction_generation: u64
}
~~~

所有记录必须在一个本地 Transaction 或等价 WAL Protocol 中原子提交。如果 Payload 存储在外部，则必须先持久化暂存并验证完整性，再由事务发布 Accepted；对象存储中一个悬空的上传对象不构成 Accepted Event。

### 6.3 Idempotency Identity（等待 H/I 确认，当前为 CANDIDATE）

~~~text
IdempotencyScope = (
  authenticated_producer_id,
  owner_scope_id,
  operation_family,
  idempotency_key
)
IdempotencyRecord {
  scope: IdempotencyScope
  canonical_payload_digest: Digest
  event_id: OpaqueId
  receipt_id: OpaqueId
  accepted_at: Instant
  expires_at: Instant?
  state: accepted | forgotten_tombstone | expired
}
~~~

准确字段名和 Retention Window 由 H/I 联合拥有。Digest 基于带版本的 Canonical Envelope 表示和 Payload Integrity 计算，不依赖任意 JSON Key 顺序。

## 7. Pipeline 与状态机

~~~mermaid
sequenceDiagram
 participant P as Producer / Adapter
 participant G as Gateway
 participant I as Ingestion
 participant DB as Durable Event Store + Outbox
 participant W as Compiler Worker
 P->>G: EventEnvelope + idempotency key
 G->>G: Authenticate / resolve Scope / authorize
 G->>I: Validated envelope
 I->>DB: Atomic Event + payload ref + idempotency + receipt + outbox
 DB-->>P: AcceptedReceipt(event_id, receipt_id)
 DB-->>W: Durable pending work
 W->>W: Recheck permission, scope and Forget fence
 W->>W: Claim work lease / process idempotently
~~~

~~~mermaid
stateDiagram-v2
 [*] --> Validating
 Validating --> Rejected: schema / scope / permission invalid
 Validating --> CapacityBlocked: durable capacity unavailable
 CapacityBlocked --> Validating: retry after capacity
 Validating --> Committing: all checks pass
 Committing --> AcceptedPending: atomic durable commit
 Committing --> RetryableUnavailable: commit outcome unknown/unavailable
 AcceptedPending --> Processing
 Processing --> CompiledProposal
 Processing --> RetryScheduled
 RetryScheduled --> Processing
 Processing --> DeadLetter: retry budget / permanent error
 DeadLetter --> Processing: authorized replay
 AcceptedPending --> Suppressed: Forget fence / retention restriction
~~~

### 7.1 四个不同里程碑

| 里程碑 | 含义 | 证据 |
|---|---|---|
| Accepted | Event、Payload Ref、Scope、Idempotency、Receipt 和可恢复 Processing Intent 均已持久化 | Commit Generation + Receipt |
| Processing | Worker 已取得 Lease 或暂存 Work | Durable Lease/Stage Receipt |
| Compiled | Compiler 已完成 Candidate Proposal，但不一定成为 Canonical | Terminal Compiler Stage Receipt |
| Canonical Commit | D/Lifecycle Authority 接受并持久化 Canonical Memory/Claim Version | Canonical Version + Commit Event |

Indexed 是之后由 F/Storage 完成的 Projection 里程碑，不能从 Canonical Commit 推断。

## 8. 不变量

未 Durable Commit 前绝不返回 Accepted；Accepted Event 在 Compiler/Model 故障或重启后仍然存在；相同 Idempotency Identity 和 Digest 返回相同 Event/Receipt；相同 Identity 配不同 Digest 必须冲突；Event/Source/Brain Time 保持独立；Acceptance 不验证真伪；异步 Work 期间重新检查 Scope/Permission；依赖 Environment 的数据不得退化为仅 Agent Scope；Forget Fence 阻止 Replay 复活；响应丢失通过 Retry/Status Query 恢复。

## 9. 幂等性

- 相同 Key + 相同 Payload：返回原 event_id、Receipt Identity 和 accepted_at；不创建第二个逻辑 Work Item。
- 相同 Key + 不同 Payload Digest：以 IDEMPOTENCY_KEY_REUSE_CONFLICT 拒绝，并保留原记录。
- 相同 Payload + 不同 Key：视为不同提交，除非明确的 Source-level Dedup Policy 另有规定。
- 并发相同提交：由 Unique Constraint/Serialized Transaction 选出一个胜者；其他请求返回其 Receipt。
- Replay 复用原 Event Identity 和 recorded_at；只增加 Attempt/Replay Metadata。
- Forgotten/Expired Key：受治理的 Tombstone 在要求的 Retention Window 内防止复活；准确期限由 I 拥有，仍为 OPEN。
- 保存 Digest Algorithm/Canonicalization Version；绝不静默改变历史 Identity 的解释方式。

## 10. 一致性与事务边界

**DECIDED 要求：** Event、Idempotency Record、Receipt 和 Compile Intent 必须原子提交，或采用等价可恢复协议，确保四者未全部持久化时绝不会暴露 Accepted。

**CANDIDATE 实现：** 一个 Database Transaction 写入 Event Metadata、持久化 Payload Ref、Idempotency Row、Receipt 和 Outbox Row。Dispatcher 读取 Outbox，并以 At-least-once 发布 Work。Worker Stage Operation 必须幂等。如果使用独立 Blob Storage，必须先写入并验证不可变 Payload，再提交其 Metadata Ref；孤立暂存 Blob 只有在 Reconciliation 后才可垃圾回收。

不假设 Model Provider、Canonical Store 和 Index 之间存在分布式事务。

## 11. 故障恢复

| 故障点 | 必需行为 |
|---|---|
| Transaction 前 | 不生成 Receipt；Producer 重试 |
| Commit 前 Transaction 期间 | Rollback；不得 Accepted |
| Commit 成功但响应丢失 | Retry 返回原 Receipt |
| 已返回响应但 Worker 未 Dispatch | Outbox Scan 重建 Pending Work |
| Worker 在 Stage Commit 前崩溃 | Lease 过期；Stage 幂等重试 |
| Worker 已 Commit Stage 但 ACK 前崩溃 | 重复 Worker 读取已提交 Stage Receipt |
| Model 不可用 | Accepted Work 保持 Pending |
| Canonical Write 结果未知 | 查询 Commit/Idempotency Ref；不得重复创建 Version |
| Acceptance 后、Processing 前发生 Forget | Fence 抑制 Work 并安排派生物处理 |
| Retention 过期后 Replay | 按 I Policy 拒绝或标记 Source Unavailable；绝不重建已擦除 Payload |

## 12. 安全 / Scope

Ingress 阶段：认证 Producer；将 Principal 绑定到 Producer/Agent/Instance/Session/Task/Environment Identity；解析 ScopeRefs；授权 event.ingest；校验 Retention/Sensitivity；应用 Per-Scope Quota。

Processing 阶段：重新评估当前 Permission 和 Scope Status；验证每个被引用 Payload；检查 Forget Fence。Filter 必须先于 Event Lookup、Source Dereference、Stream Join 和 Replay Selection。

Agent 提供的 Scope 在认证/解析前只是 Hint。User Permission 不自动授予 Evidence Access。原始 Payload 是不可信数据；类似指令的内容仍然只是数据。错误信息不得泄露不可访问的 Event 是否存在。

## 13. 性能 / Backpressure

候选优先级：
- P0 运维/治理 Event（Forget、Revocation、安全事件）；
- P1 Task Transition、Action Outcome、高价值 Observation；
- P2 普通 User/Agent Message 和 Document；
- P3 高频、可替换的 Telemetry/Snapshot 及批量 Backfill。

Acceptance 前，如果不能保证 Durable Capacity，应以可重试的 INGRESS_CAPACITY_EXCEEDED 拒绝；绝不能先放入 Volatile Buffer 再声称 Accepted。Acceptance 后不得丢弃必需 Event；可以延迟低优先级 Compilation、批处理 Worker，或仅合并 Source Contract 明确允许替换的 Event。Sampling 必须携带 Gap/Coverage Metadata。限制 Payload Size、Producer Rate、Queue Bytes、Oldest Age、Active Lease 和 Retry Budget。具体数值限制为 TO_VALIDATE。

## 14. 可观测性

记录 Event/Receipt ID、Producer Class、Scope Class、Payload Digest（不记录 Payload）、Schema Version、accepted_at、Commit Generation、Queue Age、Priority、Attempt、Lease Epoch、Error Class、Replay Origin 和 Forget Suppression。

指标包括 Acceptance p50/p95/p99、Rejection/Backpressure、Outbox Lag、Queue Bytes/Age、各 Priority 等待时间、Duplicate Rate、Idempotency Conflict、Worker Lease Expiry、Replay Count、DLQ Count，以及 Accepted 到 Compiled/Canonical 的延迟。避免在 Metric Label 中使用原始来源或高基数 Identifier。

## 15. 接口

### 15.1 H / BMCP Accepted Contract（逻辑候选）

必需字段：Protocol/Schema Version；Authenticated Producer Identity；ActorRef；Resolved ScopeRefs；Event Kind/Source Type/Source ID；Content Type；Payload Ref 或 Bytes；Payload Digest；Idempotency Key；Source Event Time；Retention/Sensitivity；Correlation/Causation。Wire Serialization 和 Authentication Envelope 由 H 拥有。

Receipt：receipt_id、event_id、accepted_at、payload_digest、idempotency identity fingerprint、state=accepted_pending、schema version。accepted_pending 不表示 Compilation 已完成。

错误：INVALID_ENVELOPE、UNAUTHENTICATED_PRODUCER、SCOPE_INVALID、PERMISSION_DENIED、IDEMPOTENCY_KEY_REUSE_CONFLICT、INGRESS_CAPACITY_EXCEEDED、PAYLOAD_UNAVAILABLE、RETRYABLE_UNAVAILABLE。

### 15.2 Retry 与 Recovery

Retry 复用相同 Idempotency Identity。Receipt Lookup 分别返回原始 Acceptance State 和之后的 Processing State。Replay 必须授权，并保留 Source Identity 和 recorded_at。

### 15.3 D / F / G / I

D 接收 Accepted Event Ref 并拥有 Canonical Output；F 只接收已提交 Canonical Generation Event；G 接收 Lifecycle/Forget Notification；I 定义 Retention、Deletion、Tombstone Horizon 和 Worker Revocation 语义。

## 16. 测试场景

Commit 前/期间崩溃、Commit 后/响应前崩溃、响应后/Dispatch 前崩溃；相同 Key/相同 Digest 的顺序及并发提交；相同 Key/不同 Digest；Payload 已暂存但 Metadata Commit 失败；Outbox 故障/重启；Compiler 故障；排队期间 Scope/Permission 被撤销；Retry/DLQ/Replay Pending 时安装 Forget Fence；缺失 Environment Scope；过载/Coalescing；Source 过期后 Replay。

## 17. 依赖

H 提供 Producer Identity 和 BMCP Envelope；I 提供 Authorization、Retention、Forget、Audit 和 Tombstone；D 提供 Event Semantics 和 Typed Ref；Consistency/Storage 提供 Durable Transaction/Outbox；C 提供 Telemetry Classification 和 Identity Binding；F 消费 Canonical/Index Event。

## 18. 开放问题

- OPEN：与 H/I 最终确定 INT-P1-04 Idempotency Key Composition 和 Receipt Schema。
- OPEN：Forget/Retention 下 Idempotency Tombstone 和 Receipt Retention Horizon。
- CANDIDATE：Local Transactional Outbox 与 WAL-backed Journal 的选择，留待 Rust/Storage 设计。
- CANDIDATE：四个 Priority Class 和 Logical Lane Scheduling。
- TO_VALIDATE：Payload Size Limit、Throughput、Queue Budget、Recovery Time 和 Model Offline Backlog Drain。
- OPEN：Per-source Ordering Guarantee 及迟到/乱序 Event Policy（与 C/H 协调）。

## 19. Phase 3 H/I 对齐与 Durable Receipt 补充

- H 的 `message-envelope-and-versioning.md` 要求由 Owner 定义 Idempotency Namespace/Key/Payload Digest、带版本的 Canonicalization 和 Integrity Metadata。H 当前将 JCS 作为 Canonicalization 候选；E 拥有 Ingress Key 语义，H 拥有 Wire 表示。Protocol Version、Payload Schema Version、Permission Epoch 和 Forget Fence 必须保持独立。
- I 的 `principal-actor-and-authorization-contract.md` 提议 Idempotency Identity 由 Authenticated Producer + Tenant/Security Domain + Operation Family + Caller Key 共同限定。Payload ActorRef/Producer Claim 绝不是 Authentication。Receipt Lookup/Replay 不得跨 Principal 或 Scope 泄露 Receipt。
- I 要求在 Ingress 时授权，并在每次 Retry/Replay 时再次授权；持久化 Accepted Receipt 不是未来 Compilation 的永久许可。E 必须在 Worker Execution 和最终 Commit/Publication Linearization Point 重新校验当前 Permission Epoch 与 Forget Fence。
- Retention Duration 尚未冻结：I 要求覆盖声明的 Retry/Replay Horizon，同时尽量减少内容，并让 Idempotency Metadata/Tombstone 受 Forget Policy 约束。准确数值期限和 Legal Hold 处理仍由 I/Privacy/Legal 决定，状态 OPEN。
- I 的 Scope/Revocation Matrix 明确覆盖 Compile Start、每次 Dereference、Derivative Creation/Publication、Canonical Commit、DLQ/Replay 和 Retry。Permission Epoch 或 Forget Fence 缺失/陈旧时必须 Fail-closed。
- E 的 Accepted Linearization Point 仍是 Event、不可变 Payload Ref/Digest、Idempotency Record、Receipt 和 Compile Intent 的原子/可恢复提交。H 的 Receipt Wire Format 和 I 的 Identity/Retention Policy 不改变该持久化边界。
- 事务/WAL 崩溃矩阵和 Cursor 分离详见 [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md)。
