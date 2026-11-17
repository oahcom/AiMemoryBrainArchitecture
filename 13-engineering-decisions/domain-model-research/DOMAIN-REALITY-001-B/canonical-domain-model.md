# Canonical Domain Model
# 规范领域模型

- ID: B-CANON-001
- Status: RECOMMENDED CANONICAL MODEL — CANDIDATE; not frozen
- Baseline: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Normative authority: B for shared semantics; D/E/F/G/H/I/Storage retain their owner-local authority.

## 1. Design principles / 设计原则

1. Stable identity is independent of mutable content.
2. A domain object, a version, a protocol message and a storage record are distinct concepts.
3. State is typed by subject and owner; no universal status enum.
4. Claim epistemic standing and Memory lifecycle are independent.
5. Source, Evidence and Provenance remain distinct.
6. Occurred/Observed/Recorded/Valid/Transaction times remain distinct.
7. Every cross-module reference is typed and namespaced; references grant no permission.
8. Derived artifacts preserve exact input/version lineage and are not promoted to canonical truth by generation alone.
9. Forget, logical deletion, global completion and physical purge are separate.
10. Domain semantics do not prescribe database, wire format, runtime topology or Rust representation.

## 2. Minimum canonical model / 最小规范模型

### Identity-bearing objects

- Event — captured occurrence/report/observation.
- Memory — stable canonical asset.
- MemoryVersion — immutable version of a Memory.
- Claim — proposition with epistemic and temporal qualification; identity/schema remain ADR-BLOCKED.
- Entity — identity-bearing referent.
- Relation — typed, scoped, temporal association between endpoints.
- Evidence — independently addressable supporting/refuting/qualifying material.
- Provenance — trace of source inputs and derivation process; exact granularity OPEN.
- Context and ContextVersion — G-owned task-scoped desired view/version.
- ForgetOperation and ForgetFence — D-owned operation/suppression boundary, not Memory lifecycle aliases.
- Principal/Identity/Policy records — I-owned security/governance domain, referenced by B typed refs.

### Value/reference objects

OpaqueId, TypedObjectRef, PrincipalRef, ActorRef, IssuerRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef, RuntimeSessionRef, TimeValue/TimeInterval, Locator, ContentRef, Digest, ConfidenceValue, qualifiers and typed relationship roles.

### Derived views / implementation details

RetrievalResult, Candidate, Ranking, Activation, WorkingSet, index segments, embeddings, graph projections, summaries, runtime caches and restore projections. Their exact owner-local persistence policy does not make them canonical Memory entities.

## 3. Conceptual relationship diagram / 概念关系图

~~~mermaid
flowchart TD
  Event -->|capture / source| Evidence
  Evidence -->|supports / refutes| Claim
  Claim -->|contained in immutable snapshot| MemoryVersion
  Memory -->|has immutable versions| MemoryVersion
  Entity -->|typed endpoints| Relation
  Relation -->|supported by| Evidence
  Event -->|source input| Provenance
  Provenance -->|explains derivation of| MemoryVersion
  MemoryVersion -->|canonical source refs| ContextEntry
  Context -->|has immutable versions| ContextVersion
  ContextVersion -->|contains| ContextEntry
  ContextEntry -->|references exact version| MemoryVersion
  ContextVersion -->|delivery target| Delivery
  Delivery -->|actual final submit evidence| CSubmitOutcome
  CSubmitOutcome -->|validated and committed by G| AppliedRecord
  ForgetOperation -->|installs| ForgetFence
  ForgetFence -->|suppresses target and descendants| Memory
  PrincipalRef -->|authenticated attribution| ActorRef
  ScopeRef -->|qualifies applicability/ownership| Memory
  EnvironmentRef -->|qualifies environment-bound claims| Claim
~~~

The diagram is semantic, not a physical ERD. Delivery, CSubmitOutcome and AppliedRecord are owner-local operation/evidence objects, not B-created Memory subtypes.

该图表示语义关系，不是物理 ERD。Delivery、CSubmitOutcome 和 AppliedRecord 是 Owner 局部操作/证据对象，不是 B 创建的 Memory 子类型。

## 4. Bounded semantic ownership / 有界语义权威

| Bounded context | Canonical owner | B shared contribution |
|---|---|---|
| Canonical Memory / Lifecycle / Forget | D | Memory identity, lifecycle vocabulary, typed refs, domain relationship semantics |
| Compiler / Derivation | E | Source, Claim, Evidence, Provenance, Derivation vocabulary |
| Runtime / Retrieval | F | Retrieval/Candidate/Activation/WorkingSet boundaries; canonical refs and state separation |
| Context / Delivery / Applied | G | Context/ContextVersion/ChangeSet semantics; Applied terminology and reference boundaries |
| BMCP / Adapter protocol | H | Protocol vs domain object distinction; typed Ref mapping vocabulary |
| Security / Identity / Governance | I | Principal/Issuer/Scope/Permission distinctions; B does not define policy |
| Storage / Consistency | Storage | Logical object vs physical record/transaction/visibility distinction |
| Integration / Contract registry | A | Cross-module semantic dependency and exact contract version registration |

## 5. Minimum vs recommended model / 最小与推荐模型

### Minimum
The objects and value/reference types listed in Section 2, with explicit owner-local operation ledgers and evidence boundaries. This is sufficient to support a modular monolith and local-first deployment; it does not require distributed services, universal Event Sourcing, graph DB or ontology.

### Recommended
Minimum model plus:
- Claim–Evidence assessment/link with per-Claim role and strength;
- selective bitemporal support for time-sensitive Claim/Relation/version history;
- explicit lineage and derivation method/input version refs;
- G Applied historical record plus separately computed current-use eligibility;
- exact typed operation/receipt references and authority-local cursors/epochs;
- graph projection only for demonstrated entity-centric/multi-hop retrieval use cases.

### Deferred
Formal RDF/OWL ontology; universal event store; full graph DB as canonical store; universal Aggregate framework; standalone Source/Summary/Hypothesis/Inference/Derivation entities absent independent identity/lifecycle proof; final Session/Conversation canonical model; exact fuzzy-time schema.

### Rejected
Universal status enum; one universal ID string; one timestamp for all time semantics; untyped graph edges as canonical Relation; protocol ACK = Applied; I COMMIT_WON = Published; Forgotten = Deleted = Purged; ContextVersion = MemoryVersion = checkpoint.

## 6. System architecture fit / 系统架构适配

The model is compatible in principle with a Local-first Modular Monolith:
- bounded contexts are semantic/code ownership boundaries, not mandatory process boundaries;
- canonical write authority remains explicit;
- owner-local projections and queues are isolated behind contracts;
- references are typed without requiring distributed identity services;
- Storage transaction boundaries are chosen by actual invariants and implementation evidence.

The model does not require microservices or globally ordered IDs/cursors. Any cross-authority causal ordering (e.g. C/I/D/Storage JF-10) remains a separately evidenced operation protocol.

本模型原则上适配 Local-first Modular Monolith：Bounded Context 是语义/代码权威边界，不是强制进程边界；规范写入权威明确；Owner 局部投影和队列通过契约隔离；类型化引用不要求分布式身份服务；Storage 事务边界由真实不变量和实现证据决定。本模型不要求微服务或全局有序 ID/Cursor。任何跨权威因果排序（如 C/I/D/Storage JF-10）仍是独立的操作协议，必须单独提供证据。

## 7. Blocking semantic issues / 阻塞语义问题

- Fact/Claim ADR and Claim identity across Memory Versions.
- Scope taxonomy and Tenant/Workspace/Project/Environment namespace mapping.
- C/G/H Applied exact proof and independent Owner acceptance.
- D/I/Storage Forget vs physical purge/global completion.
- I/Storage JF-10 causal order, same-XID recovery and Published proof.
- G ContextVersion/ChangeSet and C/F consumer acceptance.
- Record Time vs Storage Transaction Time and fuzzy-time representation.
- Provenance identity granularity/cycle/retention policy.

## 8. Gate status / 门禁状态

This is the recommended candidate model for further owner reconciliation. It is not a frozen canonical contract. B2/B3/B4/B6 remain open or pending; independent review is not complete.

这是供后续 Owner 协调使用的推荐候选模型，不是已冻结的规范契约。B2/B3/B4/B6 仍开放或待完成；独立审查尚未完成。
