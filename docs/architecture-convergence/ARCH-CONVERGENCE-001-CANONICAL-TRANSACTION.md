# ARCH-CONVERGENCE-001 — Canonical Domain & Transaction Contract
# ARCH-CONVERGENCE-001 — 规范领域模型与事务合同

- Workstream: B — Domain Semantics & Canonical Transaction
- Status: **DRAFT / CONDITIONAL CONTRACT RESOLUTION / NON-NORMATIVE**
- Review anchor: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Sources: B `session-b-domain-model-phase3@2faf8ec38f14dba49e7263d7a60804dae1a74ee2`; D `session-d-memory-brain-2026-11-16@194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`; E `session-e-memory-compiler-2026-11-16@ee098e14747d9915de5b3efb63b3a8dd77f670ed`; Storage `session-storage-consistency-forget-atomicity-2026-11-16@830a559bd2f4ec72608f5a51e1a0b43779f2b989`.
- Authority rule: this proposal does not approve B Fact/Claim, amend D contracts, or select an L4 storage engine.

## 1. Executive disposition / 执行结论

The minimum viable domain must remain typed and evidence-linked. It cannot bypass the unresolved Fact/Claim contract by placing arbitrary JSON into a generic memory payload. The current B ADR-001 explicitly remains **ADR-BLOCKED**; until Architecture Governance decides, E must emit candidate-neutral `CandidateProposition/ExtractionIR`, D must keep a neutral proposition envelope, and F/G/H must not assume canonical FactRef or ClaimRef identities.

D remains the semantic authority for Canonical Memory identity, immutable MemoryVersion, canonical commit and lifecycle event ordering. Storage supplies the physical transaction/visibility substrate but does not acquire D semantics. The Storage/D serialization ADR selects **L1 Option A**: one logical serializable transaction domain per Canonical Memory authority. Its **L4 physical engine/deployment remains OPEN**.

The earliest honest canonical vertical slice is therefore: durable E acceptance → D producer admission → deterministic typed candidate compilation → Evidence/Provenance validation → D-owned canonical commit through the selected Storage serialization domain → durable outbox. It is not yet a verified runnable slice.

最小领域模型必须保持强类型和证据关联，不能通过把任意 JSON 塞进通用 Memory Payload 来绕过尚未解决的 Fact/Claim 合同。当前 B ADR-001 明确仍为 **ADR-BLOCKED**；在 Architecture Governance 作出决定前，E 必须输出候选中立的 `CandidateProposition/ExtractionIR`，D 必须保留中立命题封套，F/G/H 不得假定存在规范 FactRef 或 ClaimRef 身份。

D 仍拥有 Canonical Memory 身份、不可变 MemoryVersion、规范提交和生命周期事件顺序的语义权威。Storage 提供物理事务/可见性底座，但不取得 D 的语义权威。Storage/D 序列化 ADR 已选择 **L1 Option A**：每个 Canonical Memory Authority 使用一个逻辑 Serializable Transaction Domain；**L4 物理数据库和部署仍 OPEN**。

当前最早可诚实定义的规范垂直切片是：E 持久接收 → D Producer Admission → 确定性强类型候选编译 → Evidence/Provenance 校验 → 经 Storage 序列化域执行 D 规范提交 → 持久 Outbox。它尚不是经过验证的可运行切片。

## 2. Minimum domain model / 最小领域模型

| Object | Minimum meaning | Authority / constraint |
|---|---|---|
| Event | Captured occurrence/report/observation; acceptance is not truth | E owns ingress receipt; B defines meaning |
| Memory | Addressable retained knowledge asset; not a truth guarantee | D owns canonical identity |
| MemoryVersion | Immutable snapshot of one Memory revision | D; append-only, exact version references |
| Proposition candidate | Typed, pre-canonical assertion proposal | E creates; B semantics; no canonical Fact/Claim ID while ADR blocked |
| Claim / Fact | Canonical proposition and possible attestation distinction | **BLOCKED** by B ADR-001; no schema/wire freeze |
| Entity | Identity-bearing referent, not a mention string | Domain semantics; D canonical identity mapping |
| Relation | Typed, scoped association with endpoint semantics | Domain semantics; no co-occurrence inference |
| Evidence | Source material/observation supporting, refuting or qualifying a proposition | Evidence authority; exact write/record ownership must be reconciled |
| Provenance | Origin and derivation lineage | E binds candidate lineage; canonical references are committed by D |
| LifecycleEvent | Append-only canonical lifecycle transition record | D; event and enclosing canonical transaction commit atomically |
| Context / ContextEntry | Versioned task-oriented selection of immutable canonical refs | G; not a second canonical Memory |
| Projection | Search/index/cache/graph derivative | F or adapter; never truth and always revalidated |

### 2.1 Typed neutral proposition boundary / 强类型中立命题边界

While ADR-001 is blocked:
- E may persist a versioned typed `CandidateProposition/ExtractionIR` proposal with source EventRef, provenance/evidence references, typed subject/predicate/value candidates, scope and temporal/epistemic qualifiers only where the existing E/B contract defines them.
- This proposal is not a canonical Claim, Fact, MemoryVersion, attestation or verified truth.
- D may accept a neutral proposition envelope as part of a canonical MemoryVersion only after B/Governance supplies the canonical semantic decision and D accepts the exact consumer mapping. Until then, D's canonical schema must not freeze Fact/Claim identities.
- Do not replace the unresolved model with untyped JSON, a free-form key/value blob, model-generated schema, or product-native memory object.
- No downstream F/G/H wire field may make a candidate identifier appear to be a canonical FactRef/ClaimRef.

ADR-001 未决期间：
- E 可以保存带版本的强类型 `CandidateProposition/ExtractionIR`，其中仅包含现有 E/B 合同已经定义的来源 EventRef、Provenance/Evidence 引用、类型化 subject/predicate/value 候选、Scope 和时间/认知限定。
- 该候选不是规范 Claim、Fact、MemoryVersion、Attestation 或 Verified Truth。
- 在 B/Governance 给出规范语义决定且 D 接受精确消费者映射之前，D 不得冻结 Fact/Claim 身份。
- 不得用无类型 JSON、自由格式键值 Blob、模型自动生成 Schema 或产品原生 Memory 对象替代未决模型。
- F/G/H 不得将候选 ID 表现成规范 FactRef/ClaimRef。

## 3. Identity and idempotency contract / 身份与幂等合同

The following identity families are already distinguished in E/D contracts. They must not be collapsed into a single generic ID.

| Identity | Stability | Issuer/owner | Retry rule |
|---|---|---|---|
| EventRef | Immutable | E | Same accepted source event |
| AcceptedReceiptId | Immutable | E | Same logical accepted submission returns same receipt |
| CallerIdempotencyKey + SemanticRequestDigest | Stable scoped pair | E/I scope binding | Same key+digest returns original; same key+different digest conflicts |
| CompileIntentId | Stable across retries | E | One logical compile intent |
| ProducerWorkItemId | Stable across retries of one work item | D ledger / E consumer | D registration lookup resolves ACK loss |
| DerivationRunId | New for each recompile/run | E | A recompile is a new derivation lineage |
| AttemptId | New for every execution attempt | E | Never used as logical work identity |
| LeaseId | New for every lease | E | Expiry invalidates lease, not work |
| DependencyRegistrationId | Stable idempotency key | D dependency inventory | Same digest returns receipt; changed digest conflicts |
| PublicationOperationId | Stable idempotency key | D/Storage interface | Ambiguous result remains private until lookup |
| MemoryId / MemoryVersionId | Stable identity + immutable version | D | Never reuse ID; version CAS protects head |
| CanonicalCommitCursor | One successful transaction position per Brain authority | D | Assigned only on durable successful commit |

Caller idempotency namespace must be bound to authenticated issuer, Principal, ProducerIdentity, security domain and validated Scope. Receipt lookup is authorization checked. Raw payload-supplied IDs are claims, not authority.

调用方幂等命名空间必须绑定认证后的 Issuer、Principal、ProducerIdentity、安全域和已验证 Scope。Receipt 查询必须经过授权。Payload 自带 ID 只是声明，不是权威。

## 4. Canonical transaction contract / 规范事务合同

### 4.1 Semantic owner vs physical substrate

- **B:** canonical domain meaning and typed object semantics; Fact/Claim remains blocked.
- **D:** canonical Memory identity, immutable versions, aggregate-head CAS, LifecycleEvent, CanonicalCommit receipt/cursor and canonical Forget records.
- **Storage:** physical serializable transaction domain, durable visibility/outcome/outbox and restore mechanics.
- **E:** durable acceptance, compilation attempts, candidate/provenance preparation and producer work; E cannot write D store internals.
- **I:** principal, authorization, PermissionEpoch, revocation and policy decision; not delegated to the database or PDP product.
- **F/G/H/C:** consume typed references and current authority checks; no independent canonical write authority.

### 4.2 Atomic canonical commit set

One successful canonical transaction must atomically commit, or use a formally proven recoverable equivalent:
1. New canonical object/version writes and immutable payload references.
2. Expected-parent/current-head CAS and aggregate-head advancement.
3. Required typed references and Evidence/Provenance linkage or an explicit permitted-unavailable reason.
4. LifecycleEvent append if the operation changes lifecycle.
5. CanonicalCommit record and idempotency receipt.
6. One D-issued CanonicalCommitCursor in the serialized successful commit order.
7. Durable outbox intent for downstream projections.

A rejected/aborted/CAS-failed transaction produces no visible canonical version, no head update, no lifecycle event, no outbox intent and no committed cursor. Readers observe the entire transaction or none of it.

### 4.3 Storage L1 anchor

Storage ADR §8 records L1 Option A as selected: one serializable transaction domain per Canonical Memory authority. The same per-authority serialization anchor is used for protected D/Storage transitions including producer admission, complete dependency registration, PublicationParticipant admission, ForgetFence installation and final visibility outcome. D retains semantic decisions; Storage owns physical anchor metadata and visibility records.

The Storage ADR does **not** select SQLite or PostgreSQL. L4 must still name the actual engine/version/configuration, DB adapter, deployment, operator, read path, HA/PITR, restore quarantine and physical crash/failover proof. If the engine cannot satisfy the selected serialization/atomicity assumptions, it is non-conforming; do not weaken to check-then-write, process mutex, queue ordering or outbox-only coordination.

### 4.4 Cursor namespaces

| Cursor/version | Authority | Meaning |
|---|---|---|
| CanonicalCommitCursor | D | Global committed transaction order within one Brain authority |
| AggregateRevision | D | Revision within one aggregate |
| LifecycleEventCursor | D | Per-Memory lifecycle event order |
| IndexWatermark | F | Contiguous canonical prefix accounted for by one index partition |
| ForgetFenceCursor | D | Forget operation/generation/target-set suppression namespace |
| PermissionEpoch | I | Policy/revocation freshness |
| ContextVersion | G | Context aggregate version |
| AdapterCapabilityEpoch | H | Adapter capability snapshot |

These values are typed and incomparable across namespaces. An IndexWatermark is not Forget proof; a CanonicalCommitCursor is not Applied evidence; a PermissionEpoch is not a ForgetFence.

## 5. Transaction and ingestion state model / 事务与摄取状态模型

This is a conditional integration state model, not a replacement for E or D Owner state machines.

```text
IngressReceived
  -> AuthenticatedAndScoped (I)
  -> IdempotencyResolved (E)
  -> AcceptedReceiptCommitted (E + durable storage)
  -> DProducerRegistrationPending
  -> DProducerRegistered
  -> CompileQueued -> Leased -> Running
  -> CandidateStaged (private)
  -> EvidenceAndProvenanceValidated
  -> DCanonicalCommitPending
  -> CanonicalCommitted (D + Storage atomic boundary)
  -> ProjectionOutboxPending -> ProjectionPublished (F; derived only)
```

Independent outcomes:
- `Rejected`: no Accepted receipt unless a separately defined durable rejection receipt exists.
- `Retry`: same logical IDs; new AttemptId and LeaseId; fresh auth/fence check.
- `LeaseExpired`: old lease invalid; work remains open.
- `DeadLettered`: operational queue state, not terminal while replay remains possible.
- `UNKNOWN/IN_DOUBT`: do not infer success or failure; resolve by the same stable operation identity.
- `CanonicalCommitted`: D proof only; not index publication, Context Applied or Forget completion.

## 6. Failure and retry semantics / 故障与重试语义

| Failure | Required result | Forbidden result |
|---|---|---|
| Duplicate ingress, same key+digest | Return original receipt and logical IDs | Duplicate Event/CompileIntent |
| Same key, different digest | IDEMPOTENCY_CONFLICT | Overwrite original request |
| Concurrent same logical fact | Serialize/dedupe or preserve explicit conflict under approved identity rules | Silent overwrite or arbitrary merge |
| Crash before canonical commit | No visible canonical effect; retry by same stable operation | Partial MemoryVersion or consumed commit cursor |
| Crash after commit before ACK | Read back original receipt/cursor | Second semantic commit |
| CAS conflict | Reject stale parent; reread/reconcile | Last-writer-wins overwrite |
| Outbox duplicate | Idempotent consumer by event/aggregate identity | Duplicate projection side effect |
| Worker lease expiry | New attempt; registration remains barrier-open | Treat lease expiry as terminal |
| PermissionEpoch/ForgetFence advances | Stale attempt is rejected/suppressed | Refresh old result without revalidation |
| Unknown transaction outcome | Hold private; query same operation tuple | Assume success after timeout |

## 7. Minimum executable acceptance definitions / 最小可执行验收定义

These are test definitions only. No test is claimed as executed by this proposal.

| Test ID | Setup / action | Required assertion |
|---|---|---|
| B-TX-01 | Commit MemoryVersion + head CAS + lifecycle event + commit receipt + outbox | All visible atomically with one cursor, or none |
| B-TX-02 | Force CAS failure / stale expected version | No new revision, lifecycle event, outbox or cursor |
| B-TX-03 | Crash immediately before commit | Restart sees no canonical mutation; same idempotency key may retry |
| B-TX-04 | Crash immediately after durable commit before response | Retry/readback returns same immutable commit receipt and cursor |
| B-TX-05 | Duplicate ingress same key+digest, then same key+different digest | First dedupes; second conflicts; no duplicate compile intent |
| B-TX-06 | Duplicate/out-of-order outbox delivery | Effects idempotent; contiguous projection watermark cannot jump a gap |
| B-TX-07 | Worker lease expires during Forget or PermissionEpoch advance | Lease invalidated; work remains open; stale result cannot publish |
| B-TX-08 | Concurrent same-identity candidate proposals | No silent overwrite; outcome follows approved identity/conflict rule |
| B-TX-09 | Attempt to submit arbitrary JSON as canonical Claim/Fact while ADR blocked | Rejected or retained only as typed, non-canonical candidate; no canonical ClaimRef/FactRef |
| B-TX-10 | Storage restore from snapshot older than Forget/commit high-water | RESTORE_FENCED until control high-waters and owner evidence reconcile |

## 8. Required ADR / Owner decisions / 必需决议

| Decision | Current source status | Required decision authority | Gate |
|---|---|---|---|
| B ADR-001 Fact/Claim | ADR-BLOCKED; no formal approver/decision record | Architecture Governance with B; D/E/F/G/H/I consulted | Blocks canonical proposition identity/schema |
| D Canonical Store | Authority/immutability DECIDED; detailed layout/transaction implementation CANDIDATE | D + Storage | Blocks physical schema and transaction implementation |
| D CanonicalCommitCursor | D domain semantics DECIDED; engine implementation and E/F/G conformance OPEN | D; Storage realization; E/F/G acceptance | Blocks end-to-end cursor claims |
| Storage L1 topology | Option A selected in §8; L4 physical engine/deployment OPEN | Storage + D, I proof boundary | Blocks physical runnable profile |
| E Accepted Receipt / Producer Admission | E candidate; D APIs and Storage realization OPEN | E + D + I + Storage | Blocks durable ingress implementation |
| Evidence record/write authority | B/D/E semantics are distributed across current source docs | Explicit Brain Owner decision | Blocks provenance-complete canonical write |

### ADR-BLOCKED guardrail

Until B and Architecture Governance publish an exact approved Fact/Claim decision:
- no canonical Fact/Claim DDL, ID, public API, wire discriminant or migration is frozen;
- E uses candidate-neutral typed proposals;
- D keeps neutral proposition envelopes and does not create canonical Claim/Fact identities;
- F/G/H use existing immutable MemoryVersion references and candidate-neutral references only where their contracts permit;
- no module may claim the Fact/Claim blocker is bypassed by JSON or a product-native schema.

## 9. Implementation boundary / 实现边界

A first modular-monolith implementation may colocate B domain validation, E compiler, D canonical services, Storage adapter and SQL outbox in one process/crate workspace, but logical authority remains separate in APIs, types, transaction ownership and tests. This does not authorize a particular crate layout or engine. The Storage L1 anchor and D/I semantic gates must be enforced in the actual transaction boundary, not only in application code.

## 10. Open issues and exit criteria / 未决项与退出条件

Workstream B remains **BLOCKED for implementation-ready canonical schema** until:
1. B Fact/Claim ADR is approved by the named governance authority.
2. B/D/E consumer mapping and typed identity contract are accepted.
3. D/Storage publish exact row ownership, transaction anchor and operation boundaries.
4. Storage L4 engine/deployment profile is selected with workload and recovery evidence.
5. E/D producer admission, dependency registration and commit ACK recovery are accepted.
6. Evidence/Provenance record authority and retention/Forget behavior are explicit.
7. B-TX-01..10 have executable fixtures and actual run evidence.

Until then this document is a conditional architecture proposal, not a runnable implementation specification.

**No ADR is approved. No Owner contract is amended. No physical engine is selected. No tests are claimed as run.**

**B 工作流仍因以下条件未满足而阻塞规范 Schema 的实现冻结：**
1. B Fact/Claim ADR 由正式治理决策机构批准；
2. B/D/E 消费者映射和强类型身份合同得到接受；
3. D/Storage 明确行所有权、事务锚点和操作边界；
4. Storage L4 物理数据库/部署配置经工作负载和恢复证据选定；
5. E/D Producer Admission、依赖注册和提交 ACK 恢复合同得到接受；
6. Evidence/Provenance 记录权威及其保留/Forget 语义明确；
7. B-TX-01 至 B-TX-10 具有可执行测试夹具和真实运行证据。

在此之前，本文件只是条件性架构提案，不是可运行实现规范。

本文件不批准 ADR、不修改 Owner 合同、不选择物理数据库，也不声称测试已运行。
