# PRODUCT-FIRST-001 — Session 06: Architecture Simplification & Build-vs-Buy Review
# 架构简化与自研边界首席审查

- Task: PRODUCT-FIRST-001 / Session 06
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb` (read from latest repository commit listing on 2026-11-18)
- Branch: `research/PRODUCT-FIRST-001-session-06-simplification`
- Status: **DRAFT RESEARCH / NON-NORMATIVE / NOT AN OWNER APPROVAL / NOT A TECHNOLOGY FREEZE**
- Scope: logical-to-physical complexity, build-vs-buy, deployment minimization, migration and acceptance.
- Authority: A–I Owners and approved ADRs retain all semantic and domain decision rights.

---

## Executive decision / 执行结论

**EN.** The architecture is not demonstrably over-designed at the semantic level. Its principal risk is that a large number of logical responsibilities may be mistaken for a requirement to create the same number of services, databases, queues, workers, state machines, or Rust crates. The repository already explicitly rejects that inference: the system overview says logical boxes are not mandatory process/service/crate boundaries; TAB-001 recommends a modular Rust monolith and defers Kafka, Kubernetes, microservices and distributed databases until evidence requires them. The recommended simplification is therefore primarily *physical consolidation and infrastructure reuse*, not deletion of business semantics.

**中文。** 当前证据不足以认定领域语义层面过度设计。主要风险在于：大量逻辑职责可能被错误地解释为必须创建同等数量的服务、数据库、队列、Worker、状态机或 Rust Crate。仓库已有明确约束：系统总览说明逻辑方框不等于进程/服务/Crate 边界；TAB-001 推荐模块化 Rust 单体，并将 Kafka、Kubernetes、微服务和分布式数据库推迟到有证据证明需要时再引入。因此，简化重点应是**物理部署合并和基础设施复用**，而不是删除业务语义。

**Disposition / 总体处置：** retain all domain authorities and safety invariants; start with one deployable modular monolith, one transactional authority, one durable work mechanism, one policy decision implementation, one observability pipeline, no mandatory cache/vector database/message broker, and only evidence-driven process separation.

**Non-goals / 非目标：** this report does not approve a database, freeze TAB-001, amend Owner contracts, authorize production deployment, or claim end-to-end conformance.

## 0. Baseline, evidence and limitations / 基线、证据与限制

### 0.1 Exact repository evidence / 仓库精确证据

| Evidence | Exact path / ref | Finding |
|---|---|---|
| Current main | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | Latest commit returned by repository commit listing during this review |
| Project status | `README.md` | Architecture definition; implementation “Not started by design” |
| System overview | `01-system-architecture/system-overview.md` | Logical architecture; DECIDED modular monolith direction; explicit deployment neutrality |
| Responsibility matrix | `01-system-architecture/responsibility-matrix.md` | Primary/supporting roles; consistency and observability have cross-cutting responsibilities |
| Domain model | `02-domain-model/domain-model-overview.md` | Event, Memory, Claim, Entity, Relation, Evidence, Provenance, Context are distinct |
| Bilingual guide | `docs/zh-CN/01-system-architecture/system-overview.md` and English counterpart | Confirms logical boxes are not process boundaries; records semantic state distinctions and unresolved gates |
| Blueprint | `13-engineering-decisions/technology-architecture-blueprint.md`, TAB-001 v0.1 | Candidate, not freeze; recommends modular Rust monolith, durable local storage, optional isolated inference worker |
| PR #45 | research package, historical base `b372b62...`, head `6c7c591...` | Broad technology and complexity research; not current-main approval |
| PR #56 | independent review of #45 | REVISE; architecture freeze not ready; current-source and owner/ADR evidence gaps |
| PR #73 | current-source integration/remediation | Draft; preserves D/E/I/Storage owner and physical-proof limitations |

The fetched README and architecture documents are direct main-branch readbacks. The root-level Storage ADR path requested by the research handoff was not found on this main snapshot. PR #56 records a Storage branch ADR blob `bb544ba2f346bdc130d524bd5c7310d86f367988`, which selects L1 logical serialization Option A only; it does not select the L4 physical engine/deployment. This report treats that as a branch-pinned decision reference, not a main-branch file or production proof.

已直接读取 main 上的 README、系统架构、职责矩阵、领域模型和 TAB-001。当前 main 快照未找到交接材料所指的根目录 Storage ADR 路径。PR #56 记录 Storage 分支 ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988)，其只选择 L1 逻辑序列化 Option A，并未决定 L4 物理引擎/部署。本报告将其视为分支精确引用，不将其冒充 main 文件或生产证明。

### 0.2 Sessions 01–05 dependency / 前五个会话依赖

The accessible prior-session record does **not** contain individually verifiable final reports for PRODUCT-FIRST-001 Sessions 01–05. PR #45 contains broad, combined research touching Memory products, agent runtimes, durability, storage/search, security and observability; it is not evidence that each of Sessions 01–05 completed or that their individual recommendations were approved. Session 06 therefore records **SESSION-01..05 INDIVIDUAL REPORTS: NOT LOCATED / DEPENDENCY OPEN**. No missing conclusions are invented. Before final technology selection, import each session's exact report path, branch, commit and status, then reconcile disagreements against current main and Owner contracts.

当前可访问的历史记录中，没有找到 PRODUCT-FIRST-001 Session 01–05 各自可核验的最终报告。PR #45 包含覆盖 Memory 产品、Agent Runtime、Durable Execution、Storage/Search、安全和可观测性的综合研究，但不能证明五个会话分别完成，也不能证明其建议获批。因此登记为 **SESSION-01..05 INDIVIDUAL REPORTS: NOT LOCATED / DEPENDENCY OPEN**。不编造缺失结论。最终技术选型前，必须补齐各会话的报告路径、分支、Commit 和状态，并对照当前 main 与 Owner 契约进行整合。

## 1. Current Architecture Complexity Map / 当前架构复杂度地图

| Logical responsibility | Semantic authority (retain) | Physical implementation recommendation |
|---|---|---|
| A integration | Cross-module coordination and integration decisions | One application composition root; no A microservice |
| B domain model | Canonical object meaning, IDs, temporal/epistemic semantics | Shared domain types/library; no separate process |
| C Agent integration | Adapter and inference-boundary Applied evidence | Adapter SDK/library plus optional gateway façade; deploy near Agent when needed |
| D Memory Brain | Canonical Memory, lifecycle, Forget fence authority | In-process domain module over transactional store |
| E Compiler | Durable acceptance, transformation, evidence and candidate production | In-process pipeline + durable work table/outbox; isolate inference only if needed |
| F Runtime | Retrieval, activation, bounded working sets | In-process query services; derived indexes; cache initially absent |
| G Context | Context version, ChangeSet, delivery intent | In-process module; context tables in same transaction domain where permitted |
| H BMCP | Envelope, protocol version, ACK semantics | Protocol library + transport adapter; no mandatory protocol microservice |
| I Governance | Identity trust, authorization, Forget governance and completion evidence | One authoritative policy decision implementation plus boundary enforcement hooks |
| Storage/Consistency | Durable transaction, sequencing, idempotency, recovery mechanics | One physical transactional authority initially; explicit adapter only where portability is required |
| Telemetry/Observability | Correlation, audit and operational evidence | One tracing/metrics pipeline; audit data remains distinct from diagnostic telemetry |

**Key distinction:** A–I are responsibility/authority boundaries, not a deployment chart. The responsibility matrix itself assigns primary and supporting roles and states that supporting participants must not create competing sources of truth.

**关键区分：** A–I 是职责和权威边界，不是部署拓扑。职责矩阵明确区分 Primary/Supporting，并要求协作组件不得建立竞争性事实源。

## 2. Necessary vs Accidental Complexity / 必要复杂度与偶然复杂度

### 2.1 Necessary semantic complexity — MUST RETAIN / 必须保留的业务语义

- Canonical Memory authority and immutable/versioned history.
- Provenance, Evidence identity and derivation lineage.
- Event time, record/acceptance time and Valid Time distinctions.
- Event / Memory / Claim / Entity / Relation / Evidence distinctions.
- Contradiction preservation and epistemic qualification.
- Scope isolation distinct from Permission evaluation.
- Forget authorization, fencing, producer barrier, dependency registration, final publication gate, derived-artifact suppression, restore fencing and completion evidence.
- Accepted / Compiled / Canonical Committed / Indexed / Delivered / Applied as distinct milestones.
- Context Version authority distinct from Canonical Memory and Adapter application evidence.
- Applied Persistence / idempotency / restore fencing semantics where mandated by Owner contracts.

These are not “extra state machines” to remove. They encode different authorities, clocks, failure boundaries and externally observable facts. Combining their storage or execution mechanism must not collapse their meanings.

这些不是可以删除的“多余状态机”。它们编码不同权威、时钟、故障边界和可观察事实。可以合并物理存储或执行机制，但不得合并其语义。

### 2.2 Accidental engineering complexity — REDUCE / 可削减的工程复杂度

- One process/service/Crate per logical Owner.
- Multiple schedulers, retry loops, durable queues or replay engines for the same work item.
- A custom distributed workflow engine before a measured need exists.
- A message broker in front of a single-node local-first application without external consumers or throughput evidence.
- Separate databases for canonical state, context, lifecycle, idempotency, outbox and audit when a single transactional authority can preserve ownership and access controls.
- Mandatory vector DB, graph DB, search cluster and cache before retrieval benchmarks.
- Multiple policy engines evaluating the same decision under subtly different semantics.
- Separate telemetry SDKs, exporters and event pipelines for each module.
- Generic provider interfaces with no second implementation, no test seam need, and no concrete substitution requirement.
- Replicated copies of canonical data where a typed reference or rebuildable projection suffices.

## 3. Build-vs-Buy Matrix / 自研与采用成熟产品矩阵

| Capability | Build / Buy / Defer | Recommended first choice | Why / guardrail |
|---|---|---|---|
| Domain semantics and memory lifecycle | BUILD | Project-owned domain contracts | Core product IP; tools cannot decide truth, contradiction or forgetting |
| Durable workflow execution | BUY/REUSE selectively; defer engine | SQL transactional outbox + bounded Tokio workers for first single-node slice | One durable work authority; no custom workflow platform |
| Distributed durable workflows | DEFER | Re-evaluate Temporal/Restate/DBOS only with multi-process, long-running workflow evidence | They do not replace canonical SQL transactions or Forget gates |
| Queue / broker | DEFER | Durable DB work table/outbox | Broker adds operational and duplicate-delivery semantics; add only for independent consumers/backpressure |
| Primary persistence | BUY/REUSE | One transactional SQL engine selected by Storage ADR and workload proof | SQLite may serve local prototype; PostgreSQL candidate for concurrency/operations; neither is approved here |
| Blob payload storage | BUY/REUSE | Filesystem/content-addressed blobs behind a narrow interface only when payload size requires it | Keep metadata, authority and lifecycle in SQL; blob reference integrity and deletion proof required |
| Lexical search | BUY/REUSE | SQL filters + built-in FTS or one embedded lexical index after corpus benchmark | Start with structured/lexical retrieval; avoid dedicated cluster |
| Vector search | DEFER | Add one embedded vector index only after recall/latency evaluation | Vector search is derived and rebuildable; never authority |
| Graph database | DEFER | Relational edge tables and indexed joins | Domain relations do not imply a graph database |
| Cache | DELETE from mandatory baseline / DEFER | No cache initially; bounded in-memory request-local memoization if measured | Cache adds invalidation and Forget resurrection risk |
| Policy evaluation | BUY/REUSE selectively | One I-owned decision service/library; evaluate Cedar/OPA only after policy language and deployment needs are fixed | Do not run two independent policy authorities; enforcement remains at boundaries |
| Authentication/authorization model | BUILD semantics, reuse crypto/libs | I-owned policy and trust semantics; mature identity/crypto libraries | Preserve PermissionEpoch, revocation and trust-root requirements |
| Telemetry | BUY/REUSE | Rust tracing + one metrics/OpenTelemetry exporter path | Standard instrumentation; audit evidence remains durable and access-controlled |
| Agent runtime/framework | BUY/INTEGRATE at edge | Adapter integration with LangGraph/Hermes/Letta where useful | Brain must remain framework-independent and must not become an Agent runtime |
| Protocol | BUILD semantic contract, reuse codecs/transports | BMCP contracts + Serde/JSON/CBOR and one transport initially | Protocol envelope/ACK semantics are project-owned; transport is replaceable |
| Inference | BUY/REUSE | External model endpoint or isolated local inference worker | Inference must not block durable acceptance or Forget correctness |
| Scheduling/cron | DEFER | Tokio timers for bounded local maintenance; OS scheduler only if operationally needed | Do not add a general scheduler platform for simple periodic jobs |

## 4. Deletion / Merge / Replace / Defer Candidates / 删除、合并、替换、延迟候选

Every item below is a **recommendation**, not an instruction to rewrite Owner contracts. Each includes evidence, complexity source, replacement, semantic impact, migration, rollback, risk and closure conditions.

### S06-01 — Do not map A–I to services or Crates / A–I 不映射为服务或 Crate

- **Evidence:** README architecture map; `01-system-architecture/system-overview.md` §10; bilingual system overview §3; TAB-001 §2–3.
- **Complexity source:** deployment count grows with logical boxes; network hops, config, health, retries, release coordination and distributed failure modes are introduced without demonstrated isolation need.
- **Replace with:** one Rust workspace and one deployable modular monolith; internal modules/crates only where compile-time ownership or dependency hygiene warrants.
- **Semantic impact:** none if APIs, Owner authority and typed contracts remain unchanged. Do not merge domain ownership.
- **Migration:** classify each proposed crate as domain library, adapter library or deployable; start in-process; preserve public contract tests.
- **Rollback:** split a module into a process only behind a stable interface if isolation/scaling evidence later requires it.
- **Risk / close when:** risk of hidden shared mutable state; close with dependency-direction checks, module-level tests, transaction ownership map and a documented extraction trigger.

### S06-02 — Merge physical workflow machinery, not lifecycle semantics / 合并物理工作流机制，不合并生命周期语义

- **Evidence:** system overview distinguishes Accepted, Compiled, Canonical Committed, Indexed; TAB-001 recommends durable local storage and one monolith; PR #45 reports orchestration duplication as a risk.
- **Complexity source:** separate queues/retry managers/schedulers/replay engines can each own attempts, leases, timeouts and terminal states.
- **Replace with:** one durable work-item/outbox mechanism with typed work kinds, lease/claim, attempt metadata, retry schedule, idempotency key, terminal outcome and replay cursor. Domain-specific state remains in D/E/F/G/I authorities.
- **Semantic impact:** no collapsing of milestones or Owner state machines; common execution substrate only.
- **Migration:** inventory every work producer/consumer; map work kind and owner; define a single transition envelope; migrate one low-risk job; shadow-compare before cutover.
- **Rollback:** dual-read / old worker path with idempotent keys; stop new submissions to common executor and drain/restore old queue.
- **Risk / close when:** shared queue can become a bottleneck or blur ownership; close only after duplicate delivery, lease expiry, crash recovery, retry exhaustion, replay and Forget-fence race tests pass.

### S06-03 — Defer Temporal/Restate/DBOS as mandatory runtime / 延迟强制引入 Temporal/Restate/DBOS

- **Evidence:** TAB-001 §2.1–2.2 and PR #45 research; implementation not started; no runtime workflow topology proven.
- **Complexity source:** external engine/server, SDK, deployment, operational ownership, workflow versioning and cross-system failure semantics.
- **Replace with:** DB transaction + outbox + bounded Tokio workers for first single-node implementation. Preserve an adapter seam only if a real second execution backend is required.
- **Semantic impact:** durable work remains required; this is not permission to downgrade persistence, idempotency or recovery.
- **Migration:** prove the minimal worker against fault-injection tests first; benchmark workflow duration/concurrency; compare engines only when long-running/multi-host orchestration is a real requirement.
- **Rollback:** engine adoption remains behind an execution port; revert worker implementation while retaining durable work records.
- **Risk / close when:** local workers may be insufficient for multi-host workflows; revisit when jobs must survive host replacement, span services, wait on external signals for long periods, or require operational workflow visibility.

### S06-04 — No mandatory message broker / 不强制消息总线

- **Evidence:** TAB-001 explicitly defers Kafka and distributed infrastructure; README says implementation not started.
- **Complexity source:** broker cluster, schema registry, consumer groups, offsets, redelivery, ordering, dead-letter and operational monitoring duplicate DB outbox responsibilities in a single-node product.
- **Replace with:** transactional outbox/work table in the primary SQL authority; local consumers.
- **Semantic impact:** durable acceptance and ordered publication must remain proven; outbox is not a substitute for COC quorum log or any separately mandated log.
- **Migration:** retain outbox event identity and ordering; add broker relay only when an independent remote consumer appears.
- **Rollback:** relay can be disabled and DB outbox consumers resumed without losing event identity.
- **Risk / close when:** throughput or independent consumer count outgrows SQL polling; require measured lag, write amplification and recovery data before adding broker.

### S06-05 — One primary transactional database; no premature database federation / 单一主事务数据库

- **Evidence:** TAB-001 states correctness-critical transitions should remain in one process and one transactional authority wherever practical; Storage ADR reference selects logical L1 Option A only; physical L4 remains OPEN.
- **Complexity source:** cross-database coordination, partial commits, backups, migrations, restore ordering and duplicated truth.
- **Replace with:** one primary transactional database for canonical metadata and permitted co-located state; separate logical schemas/tables/permissions. Large immutable payloads may use a blob store only when needed.
- **Semantic impact:** D/I/COC authorities may remain logically separate where contracts require; a single DB must not falsely claim cross-log atomicity or XA.
- **Migration:** create a table/row ownership matrix; keep Canonical Memory authoritative; migrate projections only after consistency/reconciliation proof.
- **Rollback:** keep source DB authoritative until shadow reads and restore tests pass; revert routing to source.
- **Risk / close when:** single DB availability/write contention; decide SQLite vs PostgreSQL only through L4 ADR, workload and recovery tests. No engine selection is made by this report.

### S06-06 — Defer vector DB, graph DB and external search cluster / 延迟向量库、图数据库和外部搜索集群

- **Evidence:** TAB-001 recommends structured/lexical baseline and makes vector infrastructure conditional; domain model says relations are conceptual and require explicit association records, not graph storage.
- **Complexity source:** independent service, index consistency, scope filtering, delete propagation, rebuild jobs, capacity and operational burden.
- **Replace with:** relational filters/joins + one embedded lexical index where benchmarks justify it; vector/graph remain derived projections.
- **Semantic impact:** Evidence, relation and temporal semantics remain canonical; index never becomes truth.
- **Migration:** define canonical-to-index projection and watermark; compare recall/latency on a representative corpus; test deletion/rebuild under Forget.
- **Rollback:** drop/rebuild derived index from canonical data; fall back to SQL/lexical search.
- **Risk / close when:** recall/latency or graph traversal exceeds SQL baseline; require benchmark and full Forget/rebuild conformance before adoption.

### S06-07 — Remove cache from the mandatory v1 topology / 从 v1 强制拓扑中移除缓存

- **Evidence:** F owns bounded working sets/cache but no evidence of cache necessity or measured hit rate; Forget requires cache suppression/invalidation.
- **Complexity source:** invalidation, stale reads, cross-scope leakage, resurrection through cache refill, memory limits and duplicate copies.
- **Replace with:** no shared cache initially; request-local bounded memoization only where safe and measurable.
- **Semantic impact:** none; cache is derived, never authority. Forget still addresses any cache that is later introduced.
- **Migration:** disable cache reads/writes behind a feature flag; compare latency and DB load; remove cache service dependency.
- **Rollback:** re-enable bounded cache with version/fence-aware keys and invalidation evidence.
- **Risk / close when:** DB load/latency regresses beyond target; reintroduce only with measured benefit and Forget race tests.

### S06-08 — One Policy Decision implementation, many enforcement points / 单一策略决策实现，多处执行点

- **Evidence:** responsibility matrix assigns I primary ownership for Scope/Permission and Forget; local checks required at every boundary; I contracts remain authoritative.
- **Complexity source:** independently implemented policy rules in gateway, compiler, runtime, storage and adapter drift in default-deny, epoch, revocation and scope handling.
- **Replace with:** one I-owned policy decision library/service with typed decision input/output; boundary enforcement hooks call the same semantics. Cedar/OPA are candidates only after policy representation and operational needs are decided.
- **Semantic impact:** preserve distributed enforcement; centralizing the decision implementation does not mean trusting a single gateway or bypassing local checks.
- **Migration:** build conformance vectors from I contract; run old/new evaluators in shadow mode; switch one boundary at a time.
- **Rollback:** feature-flag evaluator selection; fail closed and retain old evaluator until parity proven.
- **Risk / close when:** policy evaluation becomes a latency or availability dependency; require cache/epoch correctness, revocation tests, negative tests and I Owner approval.

### S06-09 — Standardize telemetry; keep audit distinct / 统一遥测，但审计仍独立

- **Evidence:** responsibility matrix maps metrics/tracing/audit correlation to consistency support; TAB-001 recommends tracing and a metrics facade.
- **Complexity source:** multiple log formats, trace IDs, exporters, metrics registries and custom dashboards per module.
- **Replace with:** tracing spans/events and one metrics/OpenTelemetry export path; stable correlation IDs across Event, WorkItem, Memory, Context, Delivery and Forget.
- **Semantic impact:** audit/Forget evidence is durable governed data, not best-effort telemetry; do not replace audit records with logs.
- **Migration:** define field/attribute conventions; instrument one end-to-end flow; consolidate exporters after parity.
- **Rollback:** retain structured logs and durable audit; revert exporter without losing business evidence.
- **Risk / close when:** sensitive payload leakage/cardinality explosion; require redaction, access control, bounded labels and audit retention tests.

### S06-10 — Narrow Provider/port abstractions / 收窄 Provider 抽象

- **Evidence:** TAB-001 recommends explicit ports/adapters but does not require universal provider frameworks; technology choices remain CANDIDATE/OPEN.
- **Complexity source:** generic traits/configuration/registries for hypothetical providers create indirection and weaken compile-time guarantees.
- **Replace with:** ports only at real substitution, trust, resource-isolation or test seams: ModelInference, BlobStore (if needed), SearchIndex (if second backend exists), Transport, Clock/ID only when determinism needs it.
- **Semantic impact:** no change to protocol/domain contracts; provider must not own domain truth.
- **Migration:** inventory actual implementations and call sites; delete unused abstractions; keep concrete implementation behind narrow trait where justified.
- **Rollback:** restore adapter behind same contract; no data migration if persisted format is stable.
- **Risk / close when:** future provider addition requires broad refactor; add abstraction only with second implementation or a documented test/isolation requirement.

### S06-11 — No independent process for Protocol Gateway / 不为协议网关强制独立进程

- **Evidence:** responsibility matrix explicitly leaves open whether Protocol Gateway is a subsystem or façade; H owns protocol envelope and ACK semantics.
- **Complexity source:** network hop and duplicate auth/serialization/retry layers between modules inside one product.
- **Replace with:** BMCP library/facade in the monolith; expose one network endpoint at the product boundary.
- **Semantic impact:** H message/version/ACK contracts unchanged; external interoperability still uses a real protocol boundary.
- **Migration:** keep contract tests; route in-process callers to façade; external clients continue through transport endpoint.
- **Rollback:** deploy gateway as a separate process later using the same BMCP contract.
- **Risk / close when:** independent scaling/security boundary or multi-tenant ingress needs separate process; require threat model and load evidence.

### S06-12 — Prevent duplicate data authority / 防止数据权威重复

- **Evidence:** Domain model defines Context Entry as reference/presentation to canonical version, not a second canonical Memory; system overview states indexes/caches are derived; Owner matrix separates authorities.
- **Complexity source:** copying canonical payloads into context, search, cache, audit and workflow tables without explicit projection semantics.
- **Replace with:** authoritative rows plus typed references, immutable version IDs, content-addressed payloads where useful, and rebuildable projections with source cursor/watermark.
- **Semantic impact:** preserve legally/operationally required snapshots, receipts and evidence; never delete a copy required by audit or proof without Owner approval.
- **Migration:** classify each stored field as authority, immutable evidence, operational metadata or projection; assign owner, retention, rebuildability and Forget action.
- **Rollback:** retain old projection until dual-read parity and reconciliation pass.
- **Risk / close when:** reference-only design breaks historical rendering or audit; preserve immutable snapshots where required and document why they are not competing truth.

## 5. Product Reuse Opportunities / 成熟产品复用机会

1. **Rust runtime and libraries:** Tokio for async scheduling/worker supervision; Serde for codecs; tracing for correlation; proptest/fuzzing for state-machine and parser verification. Reuse these primitives rather than creating custom runtime infrastructure.
2. **Durable execution:** start with SQL transactional outbox + bounded worker. Temporal, Restate or DBOS are later candidates only if multi-host, long-running workflows or operator visibility justify a separate engine. Product adoption must include current license, SDK/runtime maturity and deployment burden review; PR #56 specifically flagged Restate Server BSL 1.1 disclosure as a research correction.
3. **Storage:** select one engine through Storage L4 ADR and fault/recovery evidence. SQLite is a local prototype candidate, not distributed transaction capability; PostgreSQL is a candidate, not an automatic approval.
4. **Search:** SQL filters and lexical baseline first; embedded FTS/Tantivy-like component only if measured corpus/query behavior needs it; vector search only after recall improvement is demonstrated.
5. **Policy:** evaluate Cedar/OPA/OpenFGA in Session 04's product study, but retain I as semantic authority. OpenFGA relationship authorization does not replace policy evaluation; OPA/Cedar must not create a second source of truth.
6. **Agent frameworks:** LangGraph, Hermes and Letta may be integration targets at the Adapter boundary. They must not become the Brain's canonical memory authority or impose a framework-specific internal runtime.
7. **Memory products:** Mem0/Graphiti/Letta memory mechanisms may inform extraction/retrieval patterns, but importing their storage/lifecycle wholesale would risk duplicate Canonical Memory and Forget authority.

The individual Session 01–05 conclusions remain an explicit dependency; this section is a bounded reuse shortlist from the accessible PR #45 research and current blueprint, not a substitute for those reports.

## 6. Minimal Viable Deployment Topology / 最小可行部署拓扑

### 6.1 First local deployment / 首期本地部署

```text
Agent / External Client
        |
   BMCP Adapter / one network boundary
        |
+---------------------------------------------+
| One Rust modular-monolith process           |
|                                             |
| B Domain | D Canonical | E Compiler         |
| F Runtime | G Context | H BMCP              |
| C Adapter edge | I Policy hooks             |
|                                             |
| One bounded worker pool + durable work table|
| One tracing/metrics pipeline                |
+----------------------+----------------------+
                       |
             One transactional SQL authority
             (engine selected by L4 ADR)
                       |
        Optional blob directory (large payloads)
        Optional embedded lexical index (measured)
```

Local inference is an optional separate worker/process only if model loading, GPU resource use or failure isolation could block core acceptance/recovery. No mandatory Kafka/NATS, Redis, Qdrant, Neo4j, Kubernetes, service mesh, distributed cache or workflow server.

### 6.2 Production evolution triggers / 生产演进触发条件

- Split inference worker: model load/VRAM/latency interferes with durable ingress or recovery.
- Split protocol gateway: separate threat boundary, external ingress scale or independent release cadence is evidenced.
- Adopt broker: multiple independently deployed consumers, measured outbox lag/throughput pressure, or cross-host delivery requirement.
- Adopt Temporal/Restate/DBOS: long-lived multi-service workflows and operator recovery visibility are required and tested.
- Add vector index: measurable retrieval recall or ranking improvement on representative data justifies operational cost.
- Add cache: measured latency/load benefit exceeds invalidation, memory and Forget risks.
- Split database: independent availability/scale/retention boundaries are required and cross-store consistency is specified.

These are triggers, not roadmap commitments.

## 7. Core IP Boundary / 核心知识产权边界

**Must remain project-owned:**
- Canonical Memory identity, version and lifecycle semantics.
- Event/Memory/Claim/Evidence/Provenance and temporal/epistemic semantics.
- Contradiction handling and canonical commit policy.
- Scope/Permission/PolicyEpoch/revocation and trust semantics (I authority).
- Forget safety: fence, producer admission, dependency registration, publication gate, suppression, restore fencing and completion evidence.
- Applied semantics and proof chain across Context, Adapter and final inference boundary.
- Context ownership, versioning, ChangeSet and reconciliation.
- BMCP semantic envelope, version and ACK contracts.
- Cross-domain invariants and conformance/fault-injection suite.

**Prefer commodity/reused implementations:**
- Async runtime, thread pool, SQL engine, serialization, crypto primitives, codecs, tracing, metrics exporters, lexical/vector index engines, blob storage and transport libraries.

**Rule:** buy mechanisms, not semantics. A product may execute a step; it cannot redefine what “canonical”, “forgotten”, “authorized”, “applied” or “evidence-backed” means.

## 8. Risk and Migration Analysis / 风险与迁移分析

| Risk | Failure mode | Mitigation / closure evidence |
|---|---|---|
| Over-consolidation | One process hides ownership and creates shared mutable state | module dependency rules, owner API boundaries, transaction map, tests |
| One DB bottleneck | contention or single-node availability limit | workload benchmarks, backup/restore, L4 ADR and explicit RPO/RTO |
| Common work queue | queue becomes accidental semantic authority | typed work kinds; domain state remains Owner-owned; race/fault tests |
| Policy centralization | remote PDP outage or stale cached decisions | local boundary enforcement, PermissionEpoch, fail-closed, revocation tests |
| Index simplification | retrieval recall drops | representative corpus benchmark and fallback path |
| Cache removal | increased SQL latency/load | measure baseline; bounded cache can be reintroduced |
| Provider deletion | later migration costs | retain only proven seams; add second backend test before generalization |
| Forget regression | old jobs/index/cache/restore resurrect forgotten data | mandatory producer/fence/dependency/publication/restore race suite |
| Session research gap | recommendations conflict with Sessions 01–05 | import exact reports and reconcile before final technology selection |
| Owner authority drift | simplification silently changes contracts | Owner sign-off required for any semantic or contract impact |

### Migration sequence / 迁移顺序

1. Freeze no new infrastructure; inventory all proposed runtime components, queues, stores, state machines and providers.
2. Mark each as authority, execution mechanism, projection, adapter or optional optimization.
3. Assign exactly one semantic authority per business fact and one physical transactional authority per atomic operation boundary.
4. Prove one local vertical slice: durable accept → compile → canonical commit → index → retrieve → context version → adapter applied; separately prove Forget/fencing and recovery.
5. Remove unused caches, duplicate worker loops and unconsumed event paths only after shadow comparison.
6. Introduce optional infrastructure only after trigger thresholds and acceptance evidence are met.

## 9. Recommended Simplified Architecture / 推荐简化架构

**Recommendation:** a **single-deployable modular Rust monolith**, with A–I retained as logical ownership boundaries; one transactional database chosen through Storage L4 ADR; one durable work/outbox mechanism; one bounded worker pool; one policy decision implementation under I; one observability pipeline; no mandatory cache, broker, vector database, graph database, external search cluster or workflow engine; optional isolated inference worker; framework-specific integrations only at Adapter boundaries.

This is a physical topology recommendation only. It does not collapse D/I/COC logical authority, claim cross-log atomicity, or authorize replacing any Owner's state machine. The first implementation should prove a narrow end-to-end slice and the Forget race/failure properties before adding scale infrastructure.

**推荐方案：**采用**单部署单元的模块化 Rust 单体**，保留 A–I 逻辑权威边界；通过 Storage L4 ADR 选择一个事务数据库；一个持久化 Work/Outbox 机制；一个有界 Worker 池；I 所有的一个策略决策实现；一条可观测性管线；不强制缓存、消息总线、向量数据库、图数据库、外部搜索集群或工作流引擎；推理 Worker 可按资源隔离需要独立；Agent 框架只在 Adapter 边界集成。

这只是物理拓扑建议，不合并 D/I/COC 逻辑权威，不声称跨日志原子性，也不授权替换任何 Owner 状态机。首期实现应先证明窄端到端链路及 Forget 竞争/故障属性，再增加扩展性基础设施。

## 10. Prioritized Remediation Plan / 优先级整改计划

| Priority | Action | Owner(s) to consult | Exit condition |
|---|---|---|---|
| P0 | Publish authority-vs-mechanism inventory; prohibit A–I-to-service inference | A + all A–I | approved responsibility map; no contract changed |
| P0 | Close D/E/Storage producer admission + Forget fence + dependency + publication atomicity | D/E/I/Storage | executable race/fault tests and exact Owner approvals |
| P0 | Close Applied persistence/idempotency/restore fencing and C/G/H proof chain | C/G/H/I/Storage | crash recovery and final inference-boundary evidence |
| P1 | Select one physical transactional engine/topology | Storage + A + Operations | L4 ADR, backup/restore, concurrency and failure evidence |
| P1 | Implement one durable outbox/worker substrate | E + D + Storage | duplicate/retry/lease/replay/fencing conformance |
| P1 | Consolidate policy evaluation semantics | I + C/D/E/F/G/H | conformance vectors, epoch/revocation, fail-closed tests |
| P1 | Standardize tracing/metrics; separate audit evidence | A + I + Operations | trace correlation and audit retention/access tests |
| P2 | Benchmark SQL/lexical retrieval before vector/graph adoption | F + B + Storage | recall/latency/resource report on representative corpus |
| P2 | Remove mandatory cache from topology | F + D + I | no regression beyond agreed target; Forget proof preserved |
| P2 | Narrow Provider abstractions | A + module Owners | each retained port has concrete second backend or test/isolation rationale |
| P2 | Import Sessions 01–05 exact reports | Session leads | report paths, commit pins, statuses and reconciled matrix |
| P3 | Consider service splits/broker/workflow engine | A + Operations + relevant Owners | trigger threshold met and migration/rollback plan approved |

No priority item authorizes merge, production activation, architecture freeze or Gate release.

## 11. Acceptance Criteria / 验收标准

A Session 06 recommendation is accepted only when:

1. Evidence points to an exact main/branch file, commit, PR or Owner contract.
2. The recommendation explicitly distinguishes semantic authority from physical implementation.
3. Necessary semantics listed in §2.1 are preserved.
4. Each deletion/merge/replace/defer candidate states replacement, business impact, migration, rollback, risk and closure condition.
5. No A–I Owner contract or approved ADR is silently overridden.
6. Storage engine/topology remains OPEN until L4 ADR and implementation evidence close it.
7. Durable work remains crash-safe, idempotent and replayable; no volatile queue is treated as durable acceptance.
8. Forget tests cover concurrent producer admission, fence installation, dependency registration, final publication, late discovery, index/cache rebuild, backup restore and fencing.
9. Applied tests distinguish delivery, receipt, persistence, application and final inference-boundary proof.
10. Policy tests cover scope isolation, default deny, PermissionEpoch, revocation and fail-closed behavior.
11. Indexes/caches are explicitly derived, rebuildable and Forget-aware.
12. Observability does not replace durable audit or evidence.
13. Bilingual parity is reviewed for all normative statements.
14. Sessions 01–05 reports are either imported and reconciled or remain visibly OPEN.
15. Draft PR remains unmerged; independent review and Owner approval are still required.

**Current acceptance state: PARTIAL.** Report content is drafted against current main readbacks. Individual Sessions 01–05 reports were not located; Storage L4 physical selection, runtime implementation, conformance, benchmark and Owner approvals remain OPEN. This report does not authorize Architecture Freeze.

**当前验收状态：PARTIAL。** 报告基于当前 main 读回形成草案。Session 01–05 单独报告尚未找到；Storage L4 物理选型、运行时实现、符合性、基准测试和 Owner 批准仍 OPEN。本报告不授权 Architecture Freeze。

---

## Appendix A — Explicit non-decisions / 明确不作出的决策

- No approval of SQLite, PostgreSQL or any other physical engine.
- No approval of Temporal, Restate, DBOS, NATS, Kafka, Qdrant, Redis, Neo4j, OPA, Cedar or OpenFGA for production.
- No deletion of Canonical Truth, Evidence, Temporal Validity, Contradiction, Authorization, Forget Safety, Applied Persistence or Restore Fencing.
- No merging of D, I and COC semantic authorities.
- No assertion that a modular monolith is already implemented or production-ready.
- No assertion that Sessions 01–05 completed.
- No merge, release, Gate pass or production activation.

## Appendix B — Source and review trail / 来源与审查轨迹

- Main baseline commit: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Main source: `README.md`, `01-system-architecture/system-overview.md`, `01-system-architecture/responsibility-matrix.md`, `02-domain-model/domain-model-overview.md`, `13-engineering-decisions/technology-architecture-blueprint.md`, bilingual `docs/zh-CN/01-system-architecture/system-overview.md` and English counterpart.
- Related PRs: #45 (technology reality research), #56 (independent review), #73 (current-source remediation).
- Storage logical ADR reference (Storage branch): Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; L1 Option A only; L4 OPEN.
- Session 01–05 individual final reports: NOT LOCATED in accessible prior-session records at review time.
