# PRODUCT-FIRST-001 — Session 02: Durable Execution & Workflow Product Adoption
# PRODUCT-FIRST-001 — Session 02：持久化执行与工作流产品采用研究

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Research baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Research branch: `research/PRODUCT-FIRST-001-session-02-durable-execution`
- Status: **DRAFT RESEARCH / NOT AN ADR / NO TECHNOLOGY FREEZE**
- Evidence labels: VERIFIED / PARTIALLY VERIFIED / UNVERIFIED
- Date: 2026-11-18

> This report is an adoption study. It does not change, approve, freeze, or supersede any Owner contract. Product execution authority is deliberately separated from Brain domain, transaction, Applied, evidence, Forget, provider-side-effect, and authorization authorities.
>
> 本报告是产品采用性研究，不修改、不批准、不冻结或取代任何 Owner 契约。产品执行权威必须与 Brain 领域、事务、Applied、Evidence、Forget、Provider Side-effect 和 Authorization 权威严格分离。

## Executive decision / 执行摘要

**Recommendation: WRAP a small database-backed job runner first; DEFER adopting Temporal or Restate as a production dependency; evaluate DBOS only in a PostgreSQL-backed, isolated spike after its Rust maturity and exact integration constraints are accepted. Do not adopt DBOS Rust 0.6 as production-ready.**

**建议：第一阶段 WRAP 一个小型、数据库驱动的 Job Runner；DEFER 将 Temporal 或 Restate 引入生产依赖；仅在接受 DBOS Rust 的成熟度及集成约束后，开展 PostgreSQL 隔离验证。不得将 DBOS Rust 0.6 视为生产就绪。**

The current architecture is a logical architecture, not an implementation. The baseline explicitly says subsystem boundaries do not mandate separate services, recommends a modular monolith as a candidate, and describes durable ingress separately from semantic compilation. Existing Phase 3.8 cross-owner proposals add a much stricter publication protocol: durable ingress, D producer registration and Forget fencing, private staging, Storage hidden participant, I single-use authorization, and a final Storage serializable transaction. A workflow engine can schedule and recover these steps; it cannot own their truth.

当前架构仍是逻辑架构，不是生产实现。基线明确规定子系统边界不等于独立服务，模块化单体只是候选方向，并将 Durable Ingress 与语义编译分离。Phase 3.8 跨 Owner 提案进一步定义了严格发布协议：持久化入口、D Producer Registration 与 Forget Fence、私有暂存、Storage Hidden Participant、I 单次授权，以及 Storage 最终 Serializable Transaction。Workflow Engine 可以调度和恢复这些步骤，但不能成为这些事实的权威。

**Product adoption is not an architecture shortcut.** The lowest-complexity near-term path is one SQL-backed execution ledger/outbox/lease scheduler inside the modular monolith, with explicit state transitions and fencing. Keep it intentionally narrow: do not implement general-purpose workflow replay, arbitrary timers, distributed queues, or a second event-sourced domain unless measured requirements force that step.

**产品采用不是架构捷径。** 当前复杂度最低的路径是在模块化单体内采用一个 SQL 驱动的执行账本/Outbox/Lease Scheduler，并保留明确状态转换和 Fencing。应有意限制范围：不要自行实现通用 Workflow Replay、任意 Timer、分布式 Queue 或第二套 Event-sourced Domain，除非实测需求证明必须升级。

## 1. Current Architecture Baseline / 当前架构基线

### 1.1 Exact main and source evidence

| Item | Observed | Status |
|---|---|---|
| Repository default branch | main | VERIFIED |
| Exact main HEAD | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | VERIFIED |
| System overview | `01-system-architecture/system-overview.md` | VERIFIED |
| Component map | `01-system-architecture/component-map.md` | VERIFIED |
| Responsibility matrix | `01-system-architecture/responsibility-matrix.md` | VERIFIED |
| System boundaries | `01-system-architecture/system-boundaries.md` | VERIFIED |
| Normative invariants | `00-governance/architecture-invariants.md` | VERIFIED |
| TAB-001 | `13-engineering-decisions/technology-architecture-blueprint.md`, CANDIDATE not freeze | VERIFIED |
| Current Phase 3 review/task pack | `reviews/integration/phase-3-defghi-cross-module-contract-review.md`, `phase-3-cross-module-remediation-task-pack.md` | VERIFIED |

The main tree at the pinned commit contains the system architecture, governance, domain model, Agent integration, technology blueprint, and review artifacts. It does not contain an implementation workspace for the Brain or a shipped durable-workflow subsystem. The report therefore evaluates architecture and proposals, not observed runtime behavior.

固定提交的 main tree 包含系统架构、治理、领域模型、Agent 集成、技术蓝图和审查工件；没有 Brain 实现 Workspace 或已交付 Durable Workflow 子系统。因此本报告评估的是架构与提案，不是已观察到的运行时行为。

### 1.2 Normative ownership found in main

- System overview: Brain owns canonical memory identity/lifecycle, canonical persistence, provenance/evidence references, retention and forgetting governance. Compiler owns durable event ingress and transformation pipeline. Runtime owns retrieval/context planning. Adapter applies context at inference assembly boundary.
- Component map: XF-04 Consistency, Recovery & Observability supports idempotency, replay, reconciliation, health, tracing, metrics and audit correlation; this is a logical responsibility, not a mandate for a separate service.
- Responsibility matrix: consistency/replay/recovery is cross-cutting primary responsibility; durable event acceptance is Ingestion primary; canonical storage mechanics are Store primary; forgetting/retention enforcement is Governance primary.
- Invariants I-10/I-11/I-18: Applied requires explicit Adapter acknowledgement at a defined inference boundary and proves protocol-level application, not model comprehension.
- Invariants I-16/I-17/I-20: state-changing protocol retries are idempotent; context version sequence has one authority; Forget covers derived records and secondary representations.
- I-21: subsystem boundaries do not imply process/service/crate boundaries.

### 1.3 Current Phase 3.8 proposal delta (PR #73)

PR #73 is a Draft remediation branch based on the current main HEAD. Its owner-remediation artifact records role-simulated source pins and explicitly says these are proposals, not real Owner approvals or executable conformance. Relevant current proposed responsibilities:

| Authority | Owner / current proposal | What a workflow product must not take over |
|---|---|---|
| Producer admission / ForgetFence / dependency lineage / publication participant | D | Whether work is admissible under current fence; complete lineage; publication terminality |
| Durable ingress / CompileIntent / immutable input / Attempt-Lease / private staging | E | Whether ingress is accepted; whether dependencies are complete; semantic compile outcome |
| Principal/workload trust / PolicyDomain / PermissionEpoch / revocation / authorization proof | I | Whether actor is authorized now; revocation ordering and terminal proof |
| Hidden participant / visibility / final serializable transaction / outcome / receipt / outbox | Storage | Canonical visibility and atomic durable commit |
| Provider side-effect intent/outcome/evidence | C | Whether external provider action happened, is unknown, or has durable evidence |
| Applied context / final inference request evidence | C/G/H | Whether a particular payload was applied at a particular inference boundary |
| Workflow scheduling/retry/recovery | Candidate infrastructure | Only execution progress, attempts, timers, task delivery and replay state |

The proposed publication order is: E durable ingress and D registration; immutable input/private staging; D complete dependency registration; Storage hidden participant; D publication admission bound to that participant; I single-use authorization; Storage final serializable transaction atomically commits visibility pointer/outcome/PublicationReceipt/outbox; D and I close only after the same authoritative Storage outcome. UNKNOWN remains private and barrier-held. This sequence is still a proposal, not a frozen API or implemented protocol.

PR #73 是以当前 main 为基线的 Draft 整改分支。其 Owner Remediation 文档记录的是角色模拟源 Pin，明确不是 Owner 真实批准或可执行符合性。其发布顺序仍为提案：E 持久化入口和 D 注册；不可变输入/私有暂存；D 完整依赖注册；Storage 隐藏 Participant；D 绑定该 Participant 的发布准入；I 单次授权；Storage 最终 Serializable Transaction 原子提交 Visibility Pointer/Outcome/Receipt/Outbox；D/I 仅在同一 Storage 权威结果后关闭。UNKNOWN 保持私有并持有 Barrier。

### 1.4 Related research PRs

- PR #45: historical TECH-REALITY-001-A package; Draft/Open; based on old main `b372b62...`, head `6c7c591...`.
- PR #56: independent review of #45; Draft/Open; verdict REVISE / NOT YET PROVEN / ARCHITECTURE FREEZE NOT READY. It records staleness, missing current Phase 3.8 integration, Restate license disclosure, and bilingual parity issues.
- PR #73: current-main remediation; Draft/Open; base `b3c666e...`, head `7b4771b...`. It updates source pins and Restate Server license disclosure but explicitly does not claim Owner approval, CI execution, production conformance, or architecture freeze.

These are context and evidence, not approvals for this Session 02 recommendation.

## 2. Product Comparison / 产品比较

### 2.1 Architectural shape

| Dimension | Temporal | Restate | DBOS |
|---|---|---|---|
| Core shape | External orchestration service + SDK Workers | External durable execution server + service SDKs | In-process library using SQL system DB |
| Execution model | Deterministic Workflow code replays ordered Event History; Activities execute side effects | Durable handlers/services, Virtual Objects and Workflows; journaled steps and durable RPC | Workflow/step checkpoints in DB; application code resumes from completed steps |
| State authority | Temporal Service owns workflow execution history/state | Restate Server owns invocation journal and durable state | DBOS system DB owns execution/step/queue state |
| Task dispatch | Server Task Queues polled by Workers | Server schedules durable invocations and retries; handler endpoints are registered | Database-backed queues and scheduler in library/runtime |
| Timers / schedules | Native durable timers, schedules and cron-like workflows | Durable timers/sleep and scheduled invocation patterns | Durable sleep and scheduled workflows; feature set depends on SDK |
| Replay | Full deterministic workflow replay from event history | Journal replay of recorded operations; re-executes handler around recorded results | Step checkpoint recovery; not Temporal-style deterministic whole-workflow event replay |
| RPC | Client/server workflow APIs; Nexus for service interaction | Durable RPC is a central design point | Library APIs and workflow/queue interactions |
| Operational footprint | Highest of these three when self-hosted; service cluster + persistence DB + workers + visibility stack | Server/cluster + persistent log/state + service endpoints; less split than Temporal but still an external system | Lowest infra footprint if PostgreSQL already exists; library and DB, optional control plane |
| Fit for current Rust project | Rust SDK exists; separate server needed | Rust SDK exists; Server BSL applies independently | Rust SDK is pre-production (0.6) and requires PostgreSQL per current Rust quickstart |

### 2.2 Temporal

Temporal is the most established general-purpose workflow orchestration model in this comparison. The architecture separates Client, Temporal Service and Worker. The service persists workflow state, append-only event history, task queues and timers; workers poll queues, execute workflow/activity code, and replay workflow code against history after failure. The persistence documentation lists supported persistence stores; the current evaluation guide lists Cassandra, MySQL, PostgreSQL or SQLite, with Elasticsearch as an optional advanced visibility store. Self-hosting means operating Temporal services and database; Temporal Cloud removes much of that service/database operations burden.

Temporal 的优势是通用 Durable Workflow 能力成熟、边界清晰、生态和运维工具丰富。代价是必须引入独立 Temporal Service 和 Worker 部署模型。工作流代码必须遵守确定性约束；外部 I/O 应放在 Activity，Activity 的副作用必须幂等或明确处理重试。Workflow Replay 不能把外部副作用变成 exactly-once。

**Strengths:** durable long-running workflows; native task queues, retries/backoff, timers, schedules, signals, cancellation, workflow replay, operational visibility and multi-worker recovery.

**Costs/risks:** another stateful service and persistence system; workflow determinism/versioning learning curve; worker topology and server operations; workflow history growth/retention; application interactions must cross SDK/service boundaries. A Rust SDK is available, but project-specific compatibility and feature maturity still require a spike.

**Fit:** best future candidate if Brain truly needs many long-lived workflows, complex orchestration, cross-service coordination, durable timers, operational visibility, and the team accepts the server dependency. Not justified merely to retry compiler jobs.

### 2.3 Restate

Restate is a durable execution server built around journaled invocations, durable services/handlers, Virtual Objects and Workflows. Its SDKs make durable RPC and stateful service patterns central; recorded journal results allow recovery without repeating already-recorded steps. Restate can connect event sources such as Kafka and retry handler invocations. Its Rust SDK is MIT-licensed, but the Server has a separate BSL 1.1 license with an Additional Use Grant.

Restate 的突出价值是 Durable RPC、服务调用、Virtual Object 状态协调和基于 Journal 的恢复。相比 Temporal 的显式 Workflow/Activity 编程模型，它更偏向让服务调用本身具备持久化执行语义。对大量 RPC、状态化对象和事件处理流程有吸引力。

**Strengths:** durable RPC; journaled steps; retry and recovery; Virtual Objects for keyed state/coordination; event-source integrations; Rust SDK.

**Costs/risks:** another server-managed execution/state authority; service registration and deployment model; server storage/cluster operations; semantics of handler retries and side effects need careful integration. Restate Server licensing is materially different from its SDK license.

**Fit:** potentially attractive if the Brain evolves into a network of independently deployed services and durable RPC is a first-class need. It is not a shortcut for the D/Storage/I publication protocol, and it would add a second durable state authority before the project has proved it needs one.

### 2.4 DBOS

DBOS is a database-native durable execution library. It stores workflow and step execution history in a system database, uses database-backed queues and scheduling, and recovers from checkpoints. It does not require a separate orchestration server in the basic architecture. This is conceptually closest to the project's SQL-first modular-monolith candidate.

DBOS 的关键特点是将 Workflow 执行状态、Step Checkpoint、Queue 和协调机制放在数据库中，采用库集成而不是独立 Orchestrator Server。它减少基础设施，但使 DBOS system schema、事务语义和数据库兼容性成为关键约束。

**Important Rust maturity constraint:** the official DBOS Rust quickstart and integration guide identify DBOS Transact for Rust 0.6 as pre-production and not supported for production use; the Rust quickstart requires PostgreSQL. This is a blocker to production adoption in a Rust-first Brain today.

**SQLite compatibility must not be generalized across language SDKs:** current Python docs describe PostgreSQL or SQLite as system database choices; Go docs also expose SQLiteSystemDB with an explicit driver-registration requirement and note SQLite is useful for local development/testing/single-node use, while sharded system DB requires PostgreSQL compatibility and excludes SQLite. The current Rust docs instead say Rust DBOS requires PostgreSQL. Thus “DBOS supports SQLite” is SDK/version/feature-specific, not a guarantee for DBOS Rust or all DBOS capabilities.

**Fit:** strongest conceptual fit for a PostgreSQL-backed Rust modular monolith after Rust SDK reaches production maturity and the exact supported features are verified. For current development, evaluate only in a disposable spike; do not make it the project's production execution authority.

### 2.5 Other mature products

- **NATS JetStream:** strong durable stream, consumer, acknowledgement, redelivery and replay primitives. It is a message broker, not a full general-purpose workflow engine. “Exactly once” claims are bounded to broker deduplication/acknowledgement semantics; they do not guarantee canonical transaction or provider side-effect exactly-once.
- **River / Faktory / Sidekiq-style job systems:** useful job queue patterns, but language/runtime/database fit must be checked; introducing a separate broker or service is not automatically simpler.
- **Argo Workflows / Airflow / Dagster:** strong batch/data pipeline orchestration; likely excessive for low-latency memory ingestion and local-first runtime.
- **LangGraph persistence/checkpointing:** useful Agent graph/thread checkpoint model; it does not replace Brain canonical persistence, Forget fences, authorization or Applied proof.

## 3. Workflow Capability Mapping / 工作流能力映射

| Capability | Temporal | Restate | DBOS | Brain boundary |
|---|---|---|---|---|
| Durable Workflow | Native | Native | Native | Workflow engine owns execution state only |
| Durable RPC | Client APIs/Nexus | Core strength | Not primary differentiator | RPC completion is not canonical commit |
| Background Jobs | Activities/Workers | Durable handlers | Durable workflows/queues | E owns compile intent and semantics |
| Task Queue | Native queues | Durable invocation scheduling | DB queues | Queue delivery is not acceptance or publication |
| Retry / Backoff | Native retry policies | Built-in retry/replay | Step/workflow retries | Retry must preserve immutable operation identity |
| Timer / Scheduler | Native timers/schedules | Durable sleep/scheduling | Durable sleep/schedules | Timer firing does not override Forget/revocation |
| Crash Recovery | History replay | Journal replay | Step checkpoint recovery | Recovery must revalidate current fences and authorization |
| Workflow Replay | Deterministic full replay | Journal replay | Checkpoint-based resume | Replay must not replay unsafe side effects |
| Idempotency | Workflow IDs/activity idempotency patterns | Invocation keys/journal semantics | Workflow/step IDs and DB transaction semantics | Brain-specific key scope, digest conflict and retention remain owned |
| Outbox / Inbox | Application DB integration needed | Ingress/event integrations, app DB transaction still separate | DB-native queue/transaction patterns | Canonical Outbox/Receipt atomics remain Storage-owned |
| Distributed Coordination | Signals, child workflows, task queues | Virtual Objects and keyed state | DB-backed coordination/queues | Does not own D fence, I sequencer, COC quorum |
| Compensation / Saga | Saga pattern composed from Activities | Durable workflows/handlers can compose compensations | Workflow steps can compose compensation | Compensation is not evidence that external effect was undone |
| Long-running Tasks | Strong | Strong | Strong | Only adopt when real long-lived work appears |
| Provider Side Effects | Activities + idempotency/reconciliation by app | Durable steps + idempotency/reconciliation by app | Steps/checkpoints + app idempotency | C/provider ledger and side-effect evidence remain authoritative |
| Operational Observability | Mature UI/CLI/visibility | Admin API/UI/metrics depending deployment | SQL introspection + optional Conductor | Brain audit/evidence identity remains separate |

### 3.1 What each product does not solve

1. None can prove that an external payment/model/provider call happened exactly once if the provider lacks an idempotency key or queryable operation ledger.
2. None can atomically commit a Brain canonical visibility pointer together with D's registration state, I's revocation sequencer, an external provider, and another independent log without an explicit distributed protocol.
3. None can infer complete derivative lineage or decide that a Forget operation is safe to complete.
4. None can prove an Adapter applied a specific context version to a specific final inference request.
5. None can decide whether an authenticated principal is currently authorized under the Brain's PolicyDomain and revocation epoch.
6. None can turn a task queue ACK into a canonical durable acceptance receipt.

## 4. Existing Design Duplication / 现有设计重复建设

### 4.1 Duplications that should be removed or delegated

The architecture risks reimplementing generic infrastructure if it separately defines all of the following without product adoption:

- Durable job state machine, attempts, leases, retry/backoff, dead-letter handling and timer persistence.
- Generic queue dispatch, worker polling, concurrency limits and backpressure.
- Workflow checkpoint/replay engine and deterministic execution versioning.
- Generic scheduled task service and delayed execution index.
- Generic workflow administration/query API and operational UI.

**Recommendation:** do not build a generic workflow engine. Start with a small DB-backed job runner or adopt a mature product only when requirements justify it. Keep Brain-owned state machines limited to domain lifecycle and cross-owner protocol states.

### 4.2 Semantics that must not be collapsed as “workflow duplication”

These are distinct facts, not redundant workflow states:

- Accepted Event vs CompileIntent vs DerivationRun vs Attempt/Lease.
- Canonical Commit vs Index Publication Watermark.
- D Producer Registration vs Storage Visibility Participant.
- I CommitAuthorizationProof vs I TerminalProof.
- Applied Context vs Delivery Acknowledgement.
- Provider Intent vs Provider Outcome vs Provider-side evidence.
- ForgetFence generation vs Authorization PermissionEpoch.
- Workflow execution history vs canonical evidence/provenance history.

A workflow engine may store references to these facts and move between them; it must not mint or reinterpret them.

## 5. Transaction / Applied / Forget Boundary / 事务、Applied 与 Forget 边界

### 5.1 Authority matrix

| Authority | Owns | Workflow product role |
|---|---|---|
| Workflow execution authority | Workflow ID, run/attempt, replay history, timers, task dispatch, worker recovery | May own this entire column |
| Canonical transaction authority | Atomic canonical writes, visibility pointer, canonical cursor, transaction commit result | May invoke Storage API; must not replace Storage |
| Applied persistence authority | Durable Applied record bound to final inference request and context version | May schedule/retry delivery; must not assert Applied |
| Evidence identity | Stable evidence IDs, digest, source/lineage binding and conflict semantics | May carry IDs; must not invent or overwrite them |
| External provider side-effect evidence | Provider operation ID, idempotency key, response/query evidence, UNKNOWN resolution | May execute calls as an activity/handler; C/provider ledger owns evidence |
| Forget fencing | Producer admission, generation, dependency inventory, barrier and completion conditions | Must check/recheck fences; never own or bypass them |
| Authorization revocation | Principal trust, PolicyDomain, PermissionEpoch, revocation ordering and proof | Must call authorization boundary; never cache authority beyond defined validity |

### 5.2 Critical rule: workflow completion is not business completion

A Temporal Activity success, Restate handler completion, or DBOS step checkpoint only proves that the workflow runtime recorded that operation's result according to its own protocol. It does not prove:

- the canonical transaction committed;
- the Storage visibility pointer became authoritative;
- a provider performed an external side effect;
- the effect is reversible;
- a Forget barrier may be released;
- authorization remained valid at the actual commit point;
- an Adapter installed context into the final inference request.

A workflow may complete only after it has observed the authoritative result from the owning subsystem. If the result is UNKNOWN, the workflow must remain pending/reconciling and must not manufacture success or compensate blindly.

### 5.3 Required call pattern

1. Workflow persists its own execution progress and immutable operation references.
2. Before any protected action, call the owning D/I/Storage/C boundary with the current generation/epoch and stable identity.
3. Perform work in private staging where required.
4. Call the authoritative commit/provider/Applied boundary.
5. Read back the authoritative receipt/outcome using the stable operation ID.
6. Only then advance the workflow to a terminal state.
7. On restart/replay, revalidate current fence and authorization; do not trust a previously cached “allowed” decision after revocation or Forget generation changes.

## 6. Failure and Recovery Analysis / 故障与恢复分析

| Failure window | Required safe behavior | Product contribution | Brain-owned requirement |
|---|---|---|---|
| Worker crashes before work | Retry same immutable operation | Queue/retry | Preserve operation identity |
| Worker crashes after provider call, before recording result | Query provider by idempotency key/operation ID; UNKNOWN until resolved | Replay/retry scheduling | C provider evidence and reconciliation |
| Duplicate task delivery | Same business operation, no duplicate canonical effect | At-least-once dispatch | Brain idempotency key/digest contract |
| Lease expires while old worker continues | Old worker must be fenced from commit | Lease/fencing primitives | D/Storage commit fence |
| Forget fence advances during compile | Suppress late output; retain barrier until dependencies close | Cancel/retry orchestration | D complete lineage and publication fencing |
| Authorization revoked mid-flight | Commit must fail if authorization proof no longer valid | Workflow can retry/stop | I PermissionEpoch and commit authorization |
| Storage commit succeeds but response lost | Read authoritative outcome by stable participant/operation identity | Replay can re-query | Storage receipt/outcome identity |
| Applied ACK lost | Query/reconcile exact final inference request evidence; never infer Applied from delivery | Durable retry | C/G/H Applied persistence |
| Workflow code changes | Version/replay compatibility or explicit migration | Temporal versioning; product-specific mechanisms | Brain semantic schema versioning separate |
| Restore from backup | Restore workflow and domain state without resurrecting forgotten/revoked data | Product recovery tooling | Forget/Permission high-water fencing before serving |

**UNKNOWN is a first-class state.** Do not convert network timeout, missing ACK, process crash or provider timeout into failure or success without reconciliation. Do not release Forget barriers because a workflow reached a local terminal label.

**UNKNOWN 是一等状态。** 网络超时、ACK 丢失、进程崩溃或 Provider 超时都不能在未对账时直接变成成功或失败。不能因为 Workflow 本地进入终态就释放 Forget Barrier。

## 7. License and Deployment Analysis / 许可证与部署分析

| Product | License evidence | Deployment / storage | Complexity and migration |
|---|---|---|---|
| Temporal Server | MIT at temporalio/temporal repository LICENSE | Self-hosted service cluster + supported persistence DB; optional Temporal Cloud | High operations if self-hosted; migrate job state/handlers and externalize workflows |
| Temporal Rust SDK | MIT; verify SDK repo and exact release independently | Rust Worker talks to Temporal Server | Rust SDK available; determinism and history compatibility require engineering |
| Restate Server | BSL 1.1 + Additional Use Grant; canonical root LICENSE | Self-hosted Restate Server/cluster or Restate Cloud; durable server-side journal/state | Medium-high operations; separate state system and service registration |
| Restate Rust SDK | MIT; distinct from Server license | Rust service endpoint connects to Restate Server | SDK currently active development; version compatibility must be pinned |
| DBOS Rust | Repository license should be checked at exact release; this report does not provide a legal opinion | Rust docs currently require PostgreSQL; 0.6 pre-production | Low infra but high integration/maturity risk now; PostgreSQL commitment |
| DBOS Python/Go | SDK-specific license and feature checks required | Some current SDK docs support SQLite for local/single-node, PostgreSQL recommended for production; Go sharding excludes SQLite | Do not transfer language-specific support to Rust |

### 7.1 Restate license — precise finding

The current canonical Server LICENSE is **Business Source License 1.1 (BSL 1.1)** with an Additional Use Grant. The grant permits production deployment for workflows/services written by the licensee or its organization, employees or contractors, and internal deployments where only those parties access Restate APIs. It restricts a **Public Restate Platform Service** that lets unrelated third-party developers register their own Restate service deployments and invoke them through the managed platform. The change license is Apache 2.0 on the stated change date (four years after release). This is not an unrestricted OSI open-source license.

The Restate Rust SDK has a separate MIT license. The SDK license does not change the Server license. Do not write “Restate is MIT” based only on the Rust SDK. If Brain becomes a public managed platform that exposes Restate APIs to third-party developers, obtain legal review against the exact distribution and service model. Do not generalize the grant into a ban on every third-party-facing service; the restriction is specifically framed around public Restate platform use and the license text includes permitted abstraction-layer scenarios.

### 7.2 DBOS and SQLite — precise finding

“DBOS supports SQLite” is not a portable statement. Python documentation supports SQLite or PostgreSQL as the system database. Go exposes SQLite system DB support when the SQLite driver is registered, and its documentation limits sharded system databases to PostgreSQL-compatible systems (SQLite excluded). The Rust integration/quickstart pages currently state that DBOS Rust requires PostgreSQL and identify version 0.6 as pre-production. Therefore:
- DBOS Rust + SQLite: **UNVERIFIED / not documented as supported by the current Rust guide**.
- DBOS Rust + PostgreSQL: documented path, but SDK is pre-production.
- DBOS Python/Go + SQLite: documented with language-specific limitations; not evidence for Rust.
- DBOS sharded system DB + SQLite: explicitly unsupported in the cited DBOS docs.

### 7.3 Deployment recommendation

For the initial local-first profile:
- Keep one Brain application and one canonical database authority.
- Keep execution records in the same database only if the Storage Owner approves schema/transaction isolation; otherwise isolate DBOS/job tables in a separate schema/database while preserving explicit cross-transaction semantics.
- Start with one worker process and bounded concurrency; add workers only after fencing and load tests.
- Do not add NATS, Temporal, Restate, Redis, or a separate scheduler simultaneously.
- Treat a managed Temporal/Restate cloud option as a later topology decision, not a shortcut around data residency, privacy, or authority boundaries.

## 8. ADOPT / EXTEND / WRAP / BUILD / DEFER Matrix / 采用矩阵

| Capability / layer | Decision | Rationale / boundary |
|---|---|---|
| Basic background job execution | WRAP | Narrow SQL job runner abstraction in modular monolith |
| Retry/backoff/lease | WRAP | Reuse standard library/runtime patterns; persist attempt and lease state; add fencing |
| Durable task queue | WRAP | SQL outbox/queue first; no separate broker until measured |
| Timer/scheduler | EXTEND | Basic next_run_at polling first; durable arbitrary timers deferred |
| Workflow orchestration | DEFER | No demonstrated need for general workflow engine yet |
| Temporal | DEFER | Best mature full workflow candidate if long-running/multi-service needs materialize |
| Restate | DEFER | Revisit if durable RPC/Virtual Objects become central; Server BSL and extra state authority |
| DBOS Rust | DEFER / SPIKE ONLY | Conceptual fit, but Rust 0.6 pre-production and PostgreSQL required |
| NATS JetStream | DEFER | Add only if independent stream fanout, broker durability or multi-consumer scale is measured |
| Workflow replay engine | ADOPT via product later | Do not build a custom replay engine |
| Canonical transaction / visibility | BUILD (Brain-owned) | Storage owns exact serializable atomic commit |
| Forget fence / dependency lineage | BUILD (Brain-owned) | D/I/Storage semantics are non-delegable |
| Applied proof persistence | BUILD (Brain-owned) | C/G/H final inference-boundary evidence |
| Provider idempotency/reconciliation | BUILD / WRAP provider APIs | C/provider ledger owns evidence; product activity is only execution wrapper |
| Authorization/revocation | BUILD / ADOPT policy primitives separately | I owns trust, PolicyDomain and revocation sequence |
| Operational telemetry | ADOPT | OpenTelemetry/tracing/metrics plus product UI if adopted; audit evidence remains Brain-owned |
| Saga compensation | WRAP | Explicit business compensation steps with evidence; never claim rollback of irreversible provider effects |

## 9. Recommended Architecture / 推荐架构

### 9.1 Phase 0 — minimal execution substrate

Implement only a narrow interface and SQL-backed execution table(s) inside the modular monolith. This is a product-wrapper recommendation, not a new authoritative domain model.

Minimum fields (illustrative; exact schema belongs to Storage/Engineering review):
- job_id, job_kind, operation_id, idempotency_key, input_digest
- state: READY / RUNNING / WAITING / RETRYABLE / UNKNOWN / SUCCEEDED / FAILED / CANCELLED
- attempt_no, available_at, lease_owner, lease_until, lease_generation
- created_at, updated_at, last_error_class, trace_id
- authoritative_result_ref (nullable; reference only, not copied authority)

Minimum behavior:
1. Durable enqueue in the same transaction as the event/intent it represents, where the Storage contract permits.
2. Claim with lease generation and compare-and-swap.
3. Bounded retry with exponential backoff and jitter.
4. Recheck D ForgetFence and I PermissionEpoch before protected work and before commit.
5. Never store provider secrets or treat job result JSON as evidence authority.
6. UNKNOWN goes to reconciliation, not automatic retry of an unsafe side effect.
7. Terminal status is derived from authoritative subsystem receipt, not worker return code.
8. Every state-changing command is idempotent and observable.

### 9.2 Phase 1 — vertical slice and fault proof

Build one compiler workflow:
- accepted event -> CompileIntent -> private staging -> dependency registration -> publication participant -> authorization -> Storage commit -> terminal reconciliation.
- Inject crash before/after every durable boundary, duplicate delivery, lease expiry, lost ACK, Forget fence race, authorization revocation race, Storage commit response loss and restore.
- Confirm no late derivative resurrection and no false terminal success.
- Test local SQLite only if the Storage Owner accepts its single-writer/same-host profile; do not infer distributed safety.
- If the selected physical topology is PostgreSQL, test the actual DB schema and isolation behavior, not only engine capability subtests.

### 9.3 Phase 2 — adoption trigger

Run a product spike only when at least one measured trigger is met:
- Workflows routinely outlive process/host restart and last hours/days;
- Multiple independently deployed worker pools need durable task routing;
- Timer/signal/cancellation/replay semantics become complex enough that the custom wrapper is demonstrably expensive;
- Queue throughput, concurrency isolation or operational recovery exceeds the simple DB worker profile;
- Cross-service orchestration has enough durable steps to justify an external authority.

Decision sequence:
1. DBOS Rust after production support and SQLite/PostgreSQL constraints are confirmed, if SQL-native modular-monolith integration remains preferred.
2. Temporal if broad orchestration, complex long-running workflows, multi-worker fleet and mature operational tooling dominate.
3. Restate if durable RPC, keyed stateful Virtual Objects and service-level event processing dominate, after BSL use-case review.

Do not run three production platforms in parallel. A short isolated benchmark may compare candidates, but the production architecture should select at most one execution authority.

## 10. Verification and Acceptance Criteria / 验证与验收标准

### 10.1 Evidence labels

- **VERIFIED:** directly read from pinned repository source or official current documentation.
- **PARTIALLY VERIFIED:** mechanism is documented, but project-specific behavior, exact SDK version, license interpretation or deployment fit remains unproven.
- **UNVERIFIED:** no direct source/test evidence or the capability is not documented for the required target.

### 10.2 Acceptance gates

| ID | Acceptance criterion | Evidence required | Current status |
|---|---|---|---|
| WF-01 | Main baseline and architecture boundaries are exact | Main SHA + source file readback | VERIFIED |
| WF-02 | PR #45/#56/#73 current state is checked | PR metadata and source pins | VERIFIED |
| WF-03 | Workflow engine authority is separated from canonical transaction | Authority matrix + Storage contract review | PARTIALLY VERIFIED |
| WF-04 | Applied persistence and Evidence identity remain Brain-owned | C/G/H exact Owner contract and conformance | PARTIALLY VERIFIED |
| WF-05 | Forget and revocation fencing survive retry/replay/restore | D/I/Storage approved contracts + race/fault tests | UNVERIFIED |
| WF-06 | Provider side-effect UNKNOWN recovery is safe | Provider idempotency/query evidence + fault tests | UNVERIFIED |
| WF-07 | DBOS Rust production maturity is confirmed | Stable supported release and compatibility tests | UNVERIFIED (0.6 pre-production) |
| WF-08 | DBOS SQLite claim is language-specific | Rust vs Python/Go official docs | VERIFIED |
| WF-09 | Restate Server BSL + Additional Use Grant is accurately described | Canonical Server LICENSE readback | VERIFIED |
| WF-10 | Product adoption reduces rather than increases infrastructure | Measured prototype/ops comparison | UNVERIFIED |
| WF-11 | Bilingual semantic parity | Paired-section independent audit | PARTIALLY VERIFIED; not yet independently audited |
| WF-12 | No Owner contract changed | PR diff limited to this research file | VERIFIED after diff review |

### 10.3 Required closure evidence before production adoption

- Real Owner approvals for D/E/I/Storage/C/G/H contracts; role simulation does not count.
- Exact API/schema pins and current branch HEADs.
- Storage physical topology ADR (L4) and JF-10 application-level evidence.
- Durable ingress/outbox/idempotency and lease-fencing integration tests.
- ForgetFence vs producer registration and publication races in both serial orders.
- PermissionEpoch revocation race tests.
- Provider idempotency, timeout, lost-response, query/reconciliation and UNKNOWN tests.
- C/G/H final inference request Applied evidence with lost ACK, stale delivery, reconnect and Forget/revocation races.
- Backup/restore with Forget and revocation high-water marks before serving.
- Representative workload benchmark and operator runbook.
- License review for selected product, exact version, distribution model and transitive dependencies.

## 11. Source Register / 来源登记

### Project source pins

- Main HEAD: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/b3c666e67982cb3d3374e759cfb6552c7765aacb
- Main system overview: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/b3c666e67982cb3d3374e759cfb6552c7765aacb/01-system-architecture/system-overview.md
- Main component map: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/b3c666e67982cb3d3374e759cfb6552c7765aacb/01-system-architecture/component-map.md
- Main responsibility matrix: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/b3c666e67982cb3d3374e759cfb6552c7765aacb/01-system-architecture/responsibility-matrix.md
- Main invariants: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/b3c666e67982cb3d3374e759cfb6552c7765aacb/00-governance/architecture-invariants.md
- Current-main remediation PR #73: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/73
- Historical research PR #45: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/45
- Independent review PR #56: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/56

### Official product sources

**Temporal**
- Understanding Temporal: https://docs.temporal.io/evaluate/understanding-temporal
- Persistence: https://docs.temporal.io/temporal-service/persistence
- Tasks and replay: https://docs.temporal.io/tasks
- Server architecture: https://docs.temporal.io/temporal-service/temporal-server
- Server LICENSE: https://github.com/temporalio/temporal/blob/main/LICENSE
- Rust SDK: https://github.com/temporalio/sdk-rust

**Restate**
- Documentation index: https://docs.restate.dev/llms.txt
- Durable multi-agent journal example: https://docs.restate.dev/ai/patterns/multi-agent
- Kafka/event ingress and retry: https://docs.restate.dev/guides/kafka-quickstart
- Server canonical LICENSE (BSL 1.1 + Additional Use Grant): https://github.com/restatedev/restate/blob/main/LICENSE
- Rust SDK README: https://github.com/restatedev/sdk-rust
- Rust SDK LICENSE (MIT): https://github.com/restatedev/sdk-rust/blob/main/LICENSE
- Rust SDK Cargo manifest: https://github.com/restatedev/sdk-rust/blob/main/Cargo.toml

**DBOS**
- Architecture: https://docs.dbos.dev/architecture
- System database: https://docs.dbos.dev/explanations/system-tables
- Rust quickstart (0.6 pre-production; PostgreSQL requirement): https://docs.dbos.dev/quickstart?language=rust
- Rust integration: https://docs.dbos.dev/rust/integrating-dbos
- Python configuration (PostgreSQL/SQLite): https://docs.dbos.dev/python/reference/configuration
- Go configuration (SQLite driver and system DB): https://docs.dbos.dev/golang/reference/configuration
- Sharding limitations (SQLite excluded): https://docs.dbos.dev/python/tutorials/sharding
- Rust repository: https://github.com/dbos-inc/dbos-transact-rust

**Other**
- NATS JetStream concepts: https://docs.nats.io/concepts/jetstream
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence

## 12. Final disposition / 最终结论

**Adoption decision:** WRAP first; DEFER full workflow product adoption. Do not build a custom general-purpose workflow engine. Preserve Brain-owned transaction, Applied, evidence, provider-side-effect, Forget and authorization authorities. DBOS is a future candidate, not a current Rust production recommendation. Temporal and Restate remain conditional future candidates.

**采用结论：** 先 WRAP，暂缓完整 Workflow 产品采用。不要自研通用 Workflow Engine。必须保留 Brain 自有的 Transaction、Applied、Evidence、Provider Side-effect、Forget 和 Authorization 权威。DBOS 是未来候选，不是当前 Rust 生产推荐。Temporal 与 Restate 作为满足明确触发条件后的候选。

This report is a draft research artifact only. It does not approve a technology, change an Owner contract, authorize implementation against unapproved interfaces, close any Gate, or freeze the architecture. Independent review and owner-specific acceptance remain required.

本报告仅为研究 Draft，不批准技术、不修改 Owner 契约、不授权基于未批准接口的实现、不关闭任何 Gate，也不冻结架构。仍需独立审查和对应 Owner 验收。
