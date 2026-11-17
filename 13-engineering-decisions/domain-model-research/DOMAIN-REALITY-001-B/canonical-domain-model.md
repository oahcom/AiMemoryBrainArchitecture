# Canonical Domain Model
# 规范领域模型

- ID: B-CANON-001
- Status: RECOMMENDED CANONICAL MODEL — CANDIDATE; not frozen
- Baseline: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Normative authority: B for shared semantics; D/E/F/G/H/I/Storage retain their owner-local authority.

## 1. Design principles / 设计原则

1. Stable identity is independent of mutable content.
   稳定身份独立于可变内容。
2. A domain object, a version, a protocol message and a storage record are distinct concepts.
   领域对象、版本、协议消息和存储记录是不同概念。
3. State is typed by subject and owner; no universal status enum.
   状态必须按主体和 Owner 进行类型化；不得建立通用状态枚举。
4. Claim epistemic standing and Memory lifecycle are independent.
   Claim 的认知地位与 Memory 生命周期相互独立。
5. Source, Evidence and Provenance remain distinct.
   Source、Evidence 与 Provenance 必须保持为不同概念。
6. Occurred/Observed/Recorded/Valid/Transaction times remain distinct.
   Occurred Time、Observed At、Recorded At、Valid Time 和 Transaction Time 必须保持区分。
7. Every cross-module reference is typed and namespaced; references grant no permission.
   每个跨模块引用都必须类型化并带命名空间；引用本身不授予任何权限。
8. Derived artifacts preserve exact input/version lineage and are not promoted to canonical truth by generation alone.
   派生产物必须保留精确输入/版本谱系；不得仅因生成行为就提升为规范事实。
9. Forget, logical deletion, global completion and physical purge are separate.
   Forget、逻辑删除、全局完成和物理清除是不同事项。
10. Domain semantics do not prescribe database, wire format, runtime topology or Rust representation.
    领域语义不规定数据库、Wire 格式、运行时拓扑或 Rust 表示方式。

## 2. Minimum canonical model / 最小规范模型

### Identity-bearing objects / 具有身份的对象

- Event — captured occurrence/report/observation.
  Event（事件）——被捕获的发生事项、报告或观察。
- Memory — stable canonical asset.
  Memory（记忆）——稳定的规范资产。
- MemoryVersion — immutable version of a Memory.
  MemoryVersion（记忆版本）——Memory 的不可变版本。
- Claim — proposition with epistemic and temporal qualification; identity/schema remain ADR-BLOCKED.
  Claim（主张）——带有认知与时间限定的命题；其身份/Schema 仍受 ADR 阻塞。
- Entity — identity-bearing referent.
  Entity（实体）——具有独立身份的指称对象。
- Relation — typed, scoped, temporal association between endpoints.
  Relation（关系）——端点之间类型化、受 Scope 限定且具有时间语义的关联。
- Evidence — independently addressable supporting/refuting/qualifying material.
  Evidence（证据）——可独立寻址、用于支持/反驳/限定主张的材料。
- Provenance — trace of source inputs and derivation process; exact granularity OPEN.
  Provenance（溯源）——来源输入与派生过程的追踪记录；其精确粒度仍为 OPEN。
- Context and ContextVersion — G-owned task-scoped desired view/version.
  Context 与 ContextVersion——由 G 负责、按任务 Scope 限定的期望视图及其版本。
- ForgetOperation and ForgetFence — D-owned operation/suppression boundary, not Memory lifecycle aliases.
  ForgetOperation 与 ForgetFence——由 D 负责的操作/抑制边界，不是 Memory 生命周期状态的别名。
- Principal/Identity/Policy records — I-owned security/governance domain, referenced by B typed refs.
  Principal/Identity/Policy 记录——由 I 负责的安全/治理领域对象，通过 B 定义的类型化引用进行引用。

### Value/reference objects / 值对象与引用对象

OpaqueId, TypedObjectRef, PrincipalRef, ActorRef, IssuerRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef, RuntimeSessionRef, TimeValue/TimeInterval, Locator, ContentRef, Digest, ConfidenceValue, qualifiers and typed relationship roles.

包括 OpaqueId（不透明标识）、TypedObjectRef（类型化对象引用）、PrincipalRef（主体引用）、ActorRef（行为者引用）、IssuerRef（签发方引用）、AgentRef（Agent 引用）、AdapterRef（适配器引用）、ProducerRef（生产者引用）、ScopeRef（范围引用）、EnvironmentRef（环境引用）、RuntimeSessionRef（运行时会话引用）、TimeValue/TimeInterval（时间值/时间区间）、Locator（定位符）、ContentRef（内容引用）、Digest（摘要）、ConfidenceValue（置信度值）、限定符以及类型化关系角色。

### Derived views / implementation details / 派生视图与实现细节

RetrievalResult, Candidate, Ranking, Activation, WorkingSet, index segments, embeddings, graph projections, summaries, runtime caches and restore projections. Their exact owner-local persistence policy does not make them canonical Memory entities.

RetrievalResult（检索结果）、Candidate（候选项）、Ranking（排序结果）、Activation（激活项）、WorkingSet（工作集）、索引分段、Embedding（嵌入向量）、图投影、摘要、运行时缓存和恢复投影均属于派生视图或实现细节。它们各自的 Owner 局部持久化策略，不会使其自动成为规范 Memory 实体。

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

该图表达语义关系，不是物理 ERD。Delivery、CSubmitOutcome 和 AppliedRecord 是 Owner 局部的操作/证据对象，并非由 B 创建的 Memory 子类型。

## 4. Bounded semantic ownership / 有界语义权威

| Bounded context / 有界上下文 | Canonical owner / 规范 Owner | B shared contribution / B 的共享语义贡献 |
|---|---|---|
| Canonical Memory / Lifecycle / Forget | D | Memory identity, lifecycle vocabulary, typed refs, domain relationship semantics / Memory 身份、生命周期词汇、类型化引用及领域关系语义 |
| Compiler / Derivation | E | Source, Claim, Evidence, Provenance, Derivation vocabulary / Source、Claim、Evidence、Provenance、Derivation 词汇 |
| Runtime / Retrieval | F | Retrieval/Candidate/Activation/WorkingSet boundaries; canonical refs and state separation / Retrieval、Candidate、Activation、WorkingSet 边界；规范引用与状态分离 |
| Context / Delivery / Applied | G | Context/ContextVersion/ChangeSet semantics; Applied terminology and reference boundaries / Context、ContextVersion、ChangeSet 语义；Applied 术语与引用边界 |
| BMCP / Adapter protocol | H | Protocol vs domain object distinction; typed Ref mapping vocabulary / Protocol 与领域对象的区分；类型化 Ref 映射词汇 |
| Security / Identity / Governance | I | Principal/Issuer/Scope/Permission distinctions; B does not define policy / Principal、Issuer、Scope、Permission 的区分；B 不定义策略 |
| Storage / Consistency | Storage | Logical object vs physical record/transaction/visibility distinction / 逻辑对象与物理记录/事务/可见性的区分 |
| Integration / Contract registry | A | Cross-module semantic dependency and exact contract version registration / 跨模块语义依赖与精确契约版本登记 |

## 5. Minimum vs recommended model / 最小模型与推荐模型

### Minimum / 最小模型

The objects and value/reference types listed in Section 2, with explicit owner-local operation ledgers and evidence boundaries. This is sufficient to support a modular monolith and local-first deployment; it does not require distributed services, universal Event Sourcing, graph DB or ontology.

第 2 节列出的对象和值/引用类型，加上明确的 Owner 局部操作台账与证据边界，即构成最小模型。该模型足以支持模块化单体和 Local-first 部署；它不要求分布式服务、通用 Event Sourcing、图数据库或本体。

### Recommended / 推荐模型

Minimum model plus:
最小模型之外，建议增加：

- Claim–Evidence assessment/link with per-Claim role and strength;
  Claim–Evidence 评估/关联，并为每个 Claim 单独记录角色与强度；
- selective bitemporal support for time-sensitive Claim/Relation/version history;
  对具有时间敏感性的 Claim、Relation 和版本历史选择性支持双时态；
- explicit lineage and derivation method/input version refs;
  明确记录谱系、派生方法和输入版本引用；
- G Applied historical record plus separately computed current-use eligibility;
  G 所拥有的 Applied 历史记录，以及单独计算的当前使用资格；
- exact typed operation/receipt references and authority-local cursors/epochs;
  精确的类型化操作/回执引用，以及各权威域局部的 Cursor/Epoch；
- graph projection only for demonstrated entity-centric/multi-hop retrieval use cases.
  仅在已有证据证明实体中心或多跳检索用例确有需要时，才采用图投影。

### Deferred / 延后事项

Formal RDF/OWL ontology; universal event store; full graph DB as canonical store; universal Aggregate framework; standalone Source/Summary/Hypothesis/Inference/Derivation entities absent independent identity/lifecycle proof; final Session/Conversation canonical model; exact fuzzy-time schema.

延后事项包括：正式 RDF/OWL 本体；通用事件存储；将完整图数据库作为规范存储；通用 Aggregate 框架；在缺少独立身份/生命周期证据时，将 Source、Summary、Hypothesis、Inference、Derivation 单独建模为实体；最终 Session/Conversation 规范模型；精确的模糊时间 Schema。

### Rejected / 已拒绝的建模方式

Universal status enum; one universal ID string; one timestamp for all time semantics; untyped graph edges as canonical Relation; protocol ACK = Applied; I COMMIT_WON = Published; Forgotten = Deleted = Purged; ContextVersion = MemoryVersion = checkpoint.

已拒绝的方式包括：通用状态枚举；单一通用 ID 字符串；用一个时间戳代表所有时间语义；将无类型图边作为规范 Relation；Protocol ACK 等于 Applied；I COMMIT_WON 等于 Published；Forgotten 等于 Deleted 等于 Purged；ContextVersion 等于 MemoryVersion 等于 checkpoint。

## 6. System architecture fit / 系统架构适配

The model is compatible in principle with a Local-first Modular Monolith:
本模型原则上与 Local-first Modular Monolith（本地优先的模块化单体）兼容：

- bounded contexts are semantic/code ownership boundaries, not mandatory process boundaries;
  Bounded Context 是语义/代码权威边界，不是强制的进程边界；
- canonical write authority remains explicit;
  规范写入权威必须保持明确；
- owner-local projections and queues are isolated behind contracts;
  Owner 局部投影和队列必须通过契约隔离；
- references are typed without requiring distributed identity services;
  引用必须类型化，但不因此要求分布式身份服务；
- Storage transaction boundaries are chosen by actual invariants and implementation evidence.
  Storage 事务边界应根据真实不变量和实现证据选择。

The model does not require microservices or globally ordered IDs/cursors. Any cross-authority causal ordering (e.g. C/I/D/Storage JF-10) remains a separately evidenced operation protocol.

本模型不要求微服务，也不要求全局有序 ID/Cursor。任何跨权威因果排序（例如 C/I/D/Storage JF-10）仍属于独立的操作协议，必须单独提供证据。

## 7. Authenticated ingress and physical ordering boundaries / 认证入口与物理排序边界

The domain model preserves three separate layers:
本领域模型保留三个相互独立的层次：

1. Domain identity and ActorRef/PrincipalRef/ScopeRef/EnvironmentRef typed attribution (B types; I trust/authorization; H protected transport binding).
   领域身份及 ActorRef/PrincipalRef/ScopeRef/EnvironmentRef 类型化归因（B 定义类型；I 负责 Trust/Authorization；H 负责受保护传输绑定）。
2. C origin-signed message semantics and exact C object P0, distinct from H outer-envelope P0 and protected transport authentication.
   C 的 Origin 签名消息语义及精确 C Object P0，必须与 H Outer Envelope P0 及受保护传输认证相区分。
3. Storage per-authority physical serialization anchor, a physical implementation primitive whose SerializationRevision is not comparable with D fences, I PermissionEpoch, C sequence, COC position or XID.
   Storage 的 per-authority 物理序列化锚点是一种物理实现原语；其 SerializationRevision 不得与 D Fence、I PermissionEpoch、C Sequence、COC Position 或 XID 比较。

C owns origin P0, H owns wire extraction/verification, I owns cryptographic trust/profile/key governance, and Storage owns durable authenticated ingress/replay. Current reviews accept portions only as bounded candidates; A marks outer authentication as a blocking gap and no production ingress is authorized.

C 负责 Origin P0；H 负责 Wire 提取/验证；I 负责密码学 Trust/Profile/Key 治理；Storage 负责认证后的持久 Ingress/Replay。当前审查仅将部分内容作为有边界的候选项接受；A 将外层认证列为阻塞缺口，尚未授权生产 Ingress。

## 8. Blocking semantic issues / 阻塞语义问题

- Fact/Claim ADR and Claim identity across Memory Versions.
  Fact/Claim ADR，以及 Claim 在不同 Memory Version 之间的身份问题。
- Scope taxonomy and Tenant/Workspace/Project/Environment namespace mapping.
  Scope 分类体系，以及 Tenant/Workspace/Project/Environment 命名空间映射。
- C/G/H Applied exact proof and independent Owner acceptance.
  C/G/H 的 Applied 精确证明及各 Owner 独立验收。
- D/I/Storage Forget vs physical purge/global completion.
  D/I/Storage 的 Forget 与物理清除/全局完成之间的关系。
- I/Storage JF-10 causal order, same-XID recovery and Published proof.
  I/Storage JF-10 因果顺序、同一 XID 恢复及 Published 证明。
- G ContextVersion/ChangeSet and C/F consumer acceptance.
  G 的 ContextVersion/ChangeSet，以及 C/F 消费方验收。
- Record Time vs Storage Transaction Time and fuzzy-time representation.
  Record Time 与 Storage Transaction Time 的区分，以及模糊时间表示。
- Provenance identity granularity/cycle/retention policy.
  Provenance 身份粒度、循环策略及保留策略。

## 9. Gate status / 门禁状态

This is the recommended candidate model for further owner reconciliation. It is not a frozen canonical contract. B2/B3/B4/B6 remain open or pending; independent review is not complete.

本文件是供后续 Owner 协调使用的推荐候选模型，不是已冻结的规范契约。B2/B3/B4/B6 仍处于开放或待完成状态；独立审查尚未完成。
