# ARCH-CONVERGENCE-001 — Minimum Runnable Architecture
# ARCH-CONVERGENCE-001 — 最小可运行架构

- Workstream: E — Minimal Technology Architecture & Runnable Vertical Slice
- Status: **DRAFT / IMPLEMENTATION-READY PROPOSAL TARGET / NOT A TECHNOLOGY FREEZE**
- Review anchor: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Primary sources: TAB-001 Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`; PRODUCT-FIRST PRs #74–#79; Storage/D L1 ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; ARCH-A/B/C/D Draft PRs #99/#101/#103/#104.
- Authority rule: technology topology may consolidate processes, crates and databases; it may not merge or delegate Brain semantic authorities.

## 1. Executive decision / 执行结论

**Minimum topology: one deployable Rust modular monolith, one Canonical Memory transaction domain per Brain authority, one SQL-backed durable work/outbox substrate, one local content-addressed blob area, native structured + lexical retrieval, optional adapters, and no mandatory distributed infrastructure.**

A–I remain logical authority boundaries. They do not require nine services, nine databases or nine crates. Canonical Memory Truth, Evidence/Provenance, Authorization, Forget, Lifecycle and Context Applied remain explicit Brain authorities.

The Storage/D ADR has already selected L1 Option A: one logical serializable transaction domain per Canonical Memory authority. This does not select the physical database product. L4 remains open. SQLite local and PostgreSQL server are candidate profiles; neither is frozen. The first implementation must demonstrate the same semantic transaction and recovery contract on whichever profile is selected.

The first implementation should WRAP a narrow SQL-backed job runner, not adopt a general workflow engine. Start with structured and lexical retrieval. Defer vector DB, graph DB, distributed cache, external broker and workflow engine until measurable adoption triggers are met. Use one replaceable Agent/Provider adapter; MCP is optional at the tool edge and BMCP remains H-owned.

**Important:** a compiling modular-monolith skeleton is not a runnable Brain. The full vertical slice is not complete until Forget/authorization races, final-request Applied evidence, crash recovery and restore fencing are executable and pass.

**最小拓扑：一个可部署的 Rust 模块化单体、每个 Brain Authority 一个 Canonical Memory 事务域、一个 SQL Durable Work/Outbox 底座、本地内容寻址 Blob 区、原生结构化与全文检索，以及可选 Adapter；不引入强制分布式基础设施。**

A–I 仍是逻辑权威边界，不要求九个服务、九个数据库或九个 Crate。Canonical Memory Truth、Evidence/Provenance、Authorization、Forget、Lifecycle 和 Context Applied 仍由 Brain 明确掌握。

Storage/D ADR 已选择 L1 Option A：每个 Canonical Memory Authority 使用一个逻辑 Serializable Transaction Domain。这并未选择物理数据库产品，L4 仍 OPEN。SQLite 本地 Profile 与 PostgreSQL 服务端 Profile 均为候选，尚未冻结。首个实现必须在选定 Profile 上证明相同的语义事务和恢复合同。

首版应 WRAP 窄范围 SQL Job Runner，而不是采用通用 Workflow Engine。先实现结构化和全文检索；向量数据库、图数据库、分布式缓存、外部 Broker 和 Workflow Engine 均推迟到满足可测量采用触发条件后。使用一个可替换 Agent/Provider Adapter；MCP 是可选工具边缘协议，BMCP 继续由 H 管理。

**重要：** 能编译的模块化单体骨架不等于可运行 Brain。只有 Forget/授权竞争、最终请求 Applied 证据、崩溃恢复和 Restore Fencing 均可执行并通过，完整垂直切片才算完成。

## 2. Architecture topology / 架构拓扑

```text
                 Agent / Local Test Runtime
                           |
                 C / H Adapter Boundary
                           |
          +------------------------------------+
          |         Rust Modular Monolith       |
          |                                    |
          |  B Domain Types / Validation        |
          |  I Identity / PEP / Policy Adapter  |
          |  E Ingress / Compiler / Work        |
          |  D Canonical Memory / Forget        |
          |  F Retrieval / Index Projection     |
          |  G Context / Delivery / Applied     |
          |  C Provider Egress / Outcome        |
          |  H BMCP / Adapter Evidence          |
          |                                    |
          |  SQL Work Table + Transactional     |
          |  Outbox + Owner-scoped ledgers      |
          +------------------+-----------------+
                             |
               One per-authority serializable
                 Canonical Memory transaction
                             |
              +--------------+--------------+
              |                             |
        Canonical SQL records        Content-addressed
        versions / events / fences   local Blob storage
              |
        Derived projection workers
              |
        Structured + native lexical index
        (vector/graph deferred)
```

The diagram is a physical deployment proposal, not an authority merger. I's policy-domain sequencer and COC's quorum/recovery log remain distinct logical consistency authorities. Storage's per-Brain serialization anchor covers the D/Storage transitions defined by the Storage L1 ADR; it does not silently fold I or COC into an XA transaction.

## 3. Capability disposition / 能力处置矩阵

| Capability | Disposition | Minimum implementation | Why / alternatives rejected |
|---|---|---|---|
| Canonical domain semantics | BUILD | Typed B domain model and validation; keep Fact/Claim blocked until ADR | No product owns Brain semantics |
| Canonical Memory + Lifecycle | BUILD | D-owned immutable versions, CAS heads, lifecycle events and commit receipts | External memory stores cannot own canonical truth |
| Evidence / Provenance | BUILD | Typed source/evidence/provenance refs and integrity metadata | Product source IDs are evidence inputs only |
| Authorization authority | BUILD | I-owned Principal/PolicyDomain/PermissionEpoch/decision and PEP enforcement | Cedar/OPA/OpenFGA are not identity/revocation authorities |
| Policy evaluation engine | WRAP (conditional) | One in-process Cedar evaluator behind I-owned wrapper only after I approval; otherwise deterministic I test policy adapter | OPA sidecar and OpenFGA service add operational surface; Cedar skip-on-error must be deny/indeterminate |
| Forget / recovery | BUILD | D fence/barrier, I global inventory/exception, owner-specific cleanup and restore proofs | DELETE endpoint or product filter is insufficient |
| Durable execution | WRAP | SQL work table, leases, attempts, transactional outbox, idempotent handlers and reconciliation | PR #75 recommends narrow SQL runner; Temporal/Restate/DBOS deferred |
| Structured retrieval | BUILD | F query planner and D/I revalidation over canonical typed refs | Required for MVP; product-native retrieval cannot authorize |
| Lexical retrieval | ADOPT | Native SQLite FTS5 or PostgreSQL FTS per selected storage profile | No separate search cluster initially |
| Vector retrieval | DEFER / EXTEND later | Optional pgvector or embedded ANN after labeled recall/latency evaluation | Qdrant adds second consistency/Forget/restore surface |
| Graph retrieval | DEFER | Typed SQL edges and bounded recursive queries first | Neo4j not required for initial graph semantics |
| Context / Applied | BUILD | G ContextVersion/Delivery/Applied ledger; C final request; H evidence transport | No product ACK can replace exact Applied evidence |
| Agent runtime | WRAP | One replaceable runtime adapter; local deterministic harness first | Do not build general Agent framework; defer multiple runtime integrations |
| MCP tools | ADOPT selectively | MCP adapter at tool ecosystem edge; every tool re-enters I/D checks | MCP is not authorization or BMCP replacement |
| BMCP | WRAP / retain H contract | H-owned protocol adapter and versioned schema after exact Owner acceptance | Do not replace BMCP with raw MCP |
| Provider integration | WRAP | One test provider adapter plus one selected provider after C contract acceptance | Provider handoff evidence must be C-owned |
| Blob storage | BUILD / ADOPT local | Content-addressed local filesystem with metadata and retention hooks | Object store only after scale/HA need; DB snapshot must include blob manifest |
| Cache | DEFER | No shared cache in MVP; bounded in-process cache only if profiling proves need | Cache is derived; invalidation and Forget add risk |
| Observability | ADOPT | One OpenTelemetry/tracing pipeline; audit evidence separate | Avoid multiple observability stacks |
| Backup / restore | BUILD + engine-native tools | Brain control-high-water manifest, quarantine, restore reconciliation; use engine-native backup | Native backup alone does not prove Forget/anti-rollback |
| Test infrastructure | BUILD | Contract, property, concurrency, fault injection, cross-profile and independent acceptance | No vendor product substitutes for Brain safety tests |
| External message broker | DEFER | SQL Outbox polling first | Add only when measured throughput/backpressure requires it |
| Distributed workflow engine | DEFER | Durable SQL state and bounded workers first | Execution ACK never proves business completion |

## 4. Storage profile decision / 存储 Profile 决策

### 4.1 What is decided and what is not

- **L1 logical topology DECIDED in Storage ADR §8:** one serializable transaction domain per Canonical Memory authority, with D and Storage semantic ownership distinct.
- **L4 physical engine/deployment OPEN:** exact product, version, configuration, topology, operator, HA/PITR, read path and restore drills remain unresolved.
- The Storage ADR does not approve SQLite or PostgreSQL. PRODUCT-FIRST Session 03 recommends PostgreSQL as server candidate and SQLite+WAL as embedded/single-host candidate; both remain candidates.
- TAB-001 recommends SQLite+WAL for an initial local prototype, but explicitly treats it as conditional and requires PostgreSQL comparison. That recommendation does not supersede the newer Storage L1/L4 boundary.

### 4.2 Candidate profile matrix

| Profile | Candidate engine | Best-fit hypothesis | Required proof before use |
|---|---|---|---|
| Local embedded | SQLite + WAL | One local Brain authority, single-host, low operational burden | Serializable/write serialization behavior, busy/retry handling, WAL durability, concurrent readers, crash/restart, backup/restore, Forget race and blob consistency |
| Server | PostgreSQL | Multi-user/multi-process, remote deployment, concurrent writes and operational HA | Exact isolation/locking, anchor-row serialization, failover fencing, synchronous durability, PITR, prepared participant/JF-10, stale replica/cache read exclusion |
| Other | Not selected | Only if both profiles fail measured requirements | Successor Storage ADR and equivalent linearizability/recovery proof |

### 4.3 Selection rule

Do not choose by familiarity or vendor popularity. Select only after:
1. representative workload and concurrency envelope is defined;
2. canonical write/Forget/publication race harness runs on each candidate;
3. crash-before/after-commit and lost-ACK recovery are demonstrated;
4. restore from a backup older than a ForgetFence is proven RESTORE_FENCED;
5. exact L1 anchor and protected read path are verified;
6. operations, backup cost, portability and human on-call ownership are documented;
7. D, Storage and I accept the exact profile and evidence.

## 5. Component/module map / 组件与模块图

| Logical module | Core responsibilities | Persistence/port boundary |
|---|---|---|
| Domain (B) | Typed IDs, domain invariants, temporal/epistemic semantics; neutral proposition candidate while ADR blocked | No DB or wire authority |
| Authorization (I) | Authenticated principal/workload, PolicyDomain, PermissionEpoch, decision and revocation ordering | I policy sequencer port; no fallback Permit |
| Ingress/Compiler (E) | Durable acceptance, idempotency, compile intent, attempts/leases, provenance preparation, private staging | SQL durable work and blob port; D admission before work |
| Canonical Brain (D) | Memory identity/version, CAS, LifecycleEvent, CanonicalCommitCursor, ForgetOperation/Fence/barrier | One per-authority transaction with Storage |
| Storage/Consistency | SQL serialization anchor, canonical rows, visibility pointer, publication receipt/outcome, outbox, restore | One serializable transaction domain per authority |
| Runtime (F) | Scope-before-candidate, retrieval routing, canonical revalidation, indexes/caches and watermarks | Derived projections; never canonical writes |
| Context (G) | ContextVersion, ChangeSet, delivery intent, reconciliation, Applied ledger | G-owned durable state and Applied predicate |
| Agent/Provider (C) | Agent boundary, ProviderAttempt, final request evidence, CSubmitOutcome | Provider adapter and exact request-submit boundary |
| Protocol/Adapter (H) | BMCP envelope, versioning, authenticated Adapter evidence, delivery/Forget ACK | Wire adapter; exact schema and trust acceptance |
| Composition root (A/app) | Configuration, dependency wiring, lifecycle and health endpoints | No new semantic authority |

### 5.1 Proposed Rust workspace (minimum) / 建议 Rust Workspace（最小）

Do not create one crate per Owner. Start with four crates; keep Owner boundaries as modules and typed ports.

| Crate | Contents | Dependency direction |
|---|---|---|
| `brain-domain` | Typed IDs, domain types, validators, canonical digest/value types | No storage, network or product dependencies |
| `brain-core` | Logical Owner modules B–I, state transitions, use cases, ports and invariant checks | Depends on brain-domain |
| `brain-storage` | SQL migrations, per-authority serialization anchor, repositories, transaction boundary, work/outbox, blob metadata | Implements core ports; depends on domain/core contracts |
| `brain-app` | Binary, API/CLI, composition root, provider/Agent/MCP/BMCP adapters and local test harness | Wires core + storage + adapters |

If Rust dependency direction makes `brain-storage` depend on concrete `brain-core` internals, move only the required port traits into a small `brain-ports` crate; do not pre-create a crate per logical Owner. The exact workspace layout is an implementation proposal and must be checked by a compiling dependency graph before freeze.

## 6. Minimum vertical slice / 最小垂直切片

The end-to-end path is retained. Each step below has an authority and a testable output. Transaction boundaries are explicitly distinguished.

| # | Step / owner | Input → output | Authoritative state / transaction | Idempotency & failure behavior | Security / evidence / acceptance |
|---:|---|---|---|---|---|
| 1 | Receive request / E | Ingress envelope → normalized request | No durable acceptance yet | Duplicate key lookup begins; invalid envelope rejected | Authenticated transport context; ingress trace |
| 2 | Authenticate & scope / I | Credential + action/resource/purpose → Principal/Actor/Scope/Environment binding | I policy-domain state | Unknown/stale epoch denies/pauses | I decision ref; forged payload identity test |
| 3 | Identity & idempotency / E | Scoped key + semantic digest → existing or new logical submission | E accepted-receipt transaction | Same key+digest returns same receipt; changed digest conflicts | No cross-principal receipt leakage |
| 4 | Durable acceptance / E+Storage | Event/payload ref + CompileIntent → AcceptedReceipt + durable work/outbox | One durable acceptance transaction or proven recoverable equivalent | ACK only after durable receipt; lost ACK same-key lookup | Receipt, payload digest, work ID; crash-before/after acceptance |
| 5 | D producer admission / D | ProducerWorkItem + lineage/scope/fence → RegistrationReceipt | D registration/fence ordering domain | Unknown ACK resolved by same ID/digest; no worker starts while unknown | D-issued registration sequence/high-water |
| 6 | Deterministic compile / E | Accepted Event + typed schema → CandidateProposition/ExtractionIR | E attempt/work state; staged output private | Stable CompileIntent/WorkItem; new AttemptId per retry | Schema version, run/attempt/lease; no arbitrary JSON bypass |
| 7 | Fact/Claim validation / B | Candidate proposition → validated neutral proposal or blocked | B semantic rules; canonical identity blocked by ADR-001 | If unresolved semantics needed, stop before canonical write | ADR gate; candidate-neutral test |
| 8 | Evidence/Provenance bind / E+B | Source refs + evidence locators → immutable lineage bundle | Evidence authority mapping remains to be finalized | Stable digest; partial evidence fails/explicit unavailable reason | Source integrity, actor/time/scope, no fabricated provenance |
| 9 | Canonical commit / D+Storage | Validated proposal + expected head → MemoryId/MemoryVersion/CanonicalCommitReceipt | One per-authority serializable transaction: canonical writes + CAS heads + LifecycleEvent if any + commit receipt/cursor + outbox | Same key/digest returns original; CAS conflict rejects; UNKNOWN resolved by lookup | Current I auth and D fence in commit; atomic visibility tests |
| 10 | Projection schedule / Storage+F | Committed outbox event → F work item | Outbox is committed with canonical transaction; projection state is derived | At-least-once; stable event/aggregate IDs | Contiguous IndexWatermark; duplicate/out-of-order delivery tests |
| 11 | Retrieval / F | Query + trusted scope → authorized candidates | F index/read path; canonical D remains truth | Partial/degraded/unavailable is explicit | Scope filter before candidate generation; no ANN post-filter |
| 12 | Revalidate / D+I+F | Candidate refs → current exact versions/permission/fence | D canonical state + I policy state; final disclosure boundary | Unknown currentness suppresses affected candidate | PermissionEpoch and ForgetFence independently checked |
| 13 | Assemble Context / G | Authorized refs → immutable ContextVersion/ChangeSet | G Context transaction | Stable Context/ChangeSet identity; CAS/reconcile | Exact MemoryVersion refs, Scope/Environment, digest |
| 14 | Prepare delivery / G | ContextVersion → Delivery intent/attempt | G durable delivery ledger | Duplicate intent same key/digest; stale attempt superseded | Delivery binding, target Adapter/session |
| 15 | Deliver/materialize / H | BMCP delivery → authenticated receipt/materialization evidence | H Adapter-local evidence; not Applied | Retry/reconnect reconciles same DeliveryId/attempt | Capability epoch, managed-region inventory and ACK scope |
| 16 | Final request + Provider / C | Materialized Context + prompt → exact final request and CSubmitOutcome | C final submit evidence and ProviderAttempt ledger | UNKNOWN/IN_DOUBT same attempt/key; no blind retry | Actual request ID, final digest, boundary ID, current I/D checks |
| 17 | Applied decision / G | C/H/I/D/COC/Storage evidence → durable Applied or explicit non-Full result | G-only Applied transaction | Same Applied identity/digest returns original; conflicting evidence rejected | Full predicate; crash after dispatch and before Applied persistence |

**Transaction boundaries:**
- E durable acceptance is not D canonical commit.
- D canonical commit atomically writes canonical data, aggregate heads, lifecycle events where applicable, commit receipt/cursor and outbox.
- Derived projection publication is a separate gated operation; it is not canonical commit.
- G Applied is a separate G-owned durable decision after exact request evidence.
- I revocation sequencer and COC quorum log remain separate authorities; no cross-log atomicity is implied.
- Storage JF-10 prepared participant/final visibility applies where required by the accepted COC/Storage protocol. It must not be omitted merely to make the local demo pass.

## 7. Durable work and outbox minimum / Durable Work 与 Outbox 最小合同

The first work substrate is one SQL-backed table family, not a general workflow product. It must distinguish:
- logical WorkItemId / CompileIntentId / DeliveryId / PublicationOperationId;
- AttemptId and LeaseId per execution;
- owner and operation kind;
- immutable request/input digest and schema version;
- state and monotonic state revision;
- lease expiry and fencing token/epoch under the owning authority;
- retry count/backoff class and terminal disposition;
- correlation/causation and source lineage refs;
- current PermissionEpoch / ForgetFence observed (typed separately);
- result/evidence receipt refs;
- outbox event ID and consumer contiguous watermark.

Required rules:
1. Durable acceptance and its work intent commit together or via a proven recoverable equivalent.
2. A worker claims work with a durable lease and fencing identity; lease expiry does not make old workers safe to commit.
3. Handlers are idempotent; duplicate delivery returns original outcome.
4. UNKNOWN is not converted to success/failure by timeout.
5. Retries preserve logical identity and source lineage; AttemptId changes.
6. DLQ is not terminal while replay remains possible.
7. Forget and PermissionEpoch are revalidated at each protected stage and final visibility/disclosure.
8. Outbox is notification/reconciliation; it is not canonical truth, Applied, or publication visibility.
9. Consumers advance only contiguous watermarks; no skip over missing commit/schema.
10. Restore replays current control high-waters before workers, indexes or serving are enabled.

## 8. Technology dependency matrix / 技术依赖矩阵

| Technology | Initial status | Why | Trigger to reconsider |
|---|---|---|---|
| Rust + Tokio + Serde | RECOMMENDED | TAB-001 direction and core implementation fit | Revisit only for measured ecosystem/latency issue |
| SQL migrations | BUILD/ADOPT | Versioned schema and repeatable migration | Need multi-profile migration tests |
| SQLite + WAL | CANDIDATE local | Embedded local-first profile | Write contention, multi-host, HA or recovery limitations measured |
| PostgreSQL | CANDIDATE server | Multi-writer/server profile; PostgreSQL 18.7 JF-10 probes exist | Workload/HA requirement and physical conformance |
| SQL Outbox + Work Table | WRAP | Narrow durable execution with one transaction authority | Throughput/backpressure/worker scaling measurements |
| PostgreSQL FTS / SQLite FTS5 | ADOPT by profile | Native lexical retrieval | Multilingual corpus proves inadequate |
| pgvector | EXTEND later | Candidate vector search in SQL | Labeled recall/latency and scope-filter benchmark |
| Qdrant | DEFER | Separate consistency, Forget, backup and restore plane | Measured scale/sharding/ANN need after dual-store proof |
| Tantivy | DEFER | Embedded Rust full-text alternative | FTS ranking/tokenization/throughput failure measured |
| Neo4j | DEFER | Typed SQL edges sufficient initially | Recursive graph workloads exceed SQL with evidence |
| Moka | DEFER initially | In-process cache optional | Profiling shows repeat-read benefit; fence-aware invalidation tested |
| Redis | DEFER | Distributed cache adds stale visibility risk | Multi-instance cache requirement and invalidation protocol proven |
| Cedar | WRAP candidate | In-process Rust PDP evaluator | I approves wrapper, error vectors and revocation tests |
| OPA | DEFER | Sidecar/Wasm/management surface | Cross-language policy distribution requirement measured |
| OpenFGA | DEFER | Separate ReBAC service and tuple synchronization | High-fanout relationship sharing requirement measured |
| Temporal / Restate | DEFER | General workflow infrastructure unnecessary initially | Complex long-running workflows/timers/compensation and operations justify |
| DBOS Rust | DEFER | PRODUCT-FIRST #75 marks Rust 0.6 pre-production and PostgreSQL-specific | Maturity and exact support verified later |
| Kafka / NATS / external broker | DEFER | SQL outbox is enough initially | Measured throughput/backpressure/independent scaling |
| OpenTelemetry | ADOPT | One trace/metric pipeline | Exporter/backend choice remains operational |
| MCP | ADOPT selectively | Tool ecosystem interoperability | Only where concrete tool servers are required |
| BMCP | WRAP/retain | H-owned Brain protocol | Exact H/C/G/I acceptance |
| Object storage | DEFER | Local content-addressed files adequate for initial local profile | Multi-host, HA, size or durability requirement |
| Kubernetes/microservices | DEFER | No measured need; authority boundaries are logical | Independent scaling/failure isolation/operations evidence |

## 9. Development and test environment / 开发与测试环境

Minimum reproducible environment:
- Rust stable toolchain pinned by `rust-toolchain.toml`; workspace dependencies pinned by lockfile.
- SQL profile under test: SQLite local and PostgreSQL candidate test profile; no production profile inferred.
- Local content-addressed blob directory with deterministic test fixtures and explicit retention cleanup.
- Fake authenticated Principal/PolicyDomain test authority; production I sequencer must be separately integrated before security claims.
- Deterministic fake Agent/Adapter/runtime that exposes the actual final request submit hook and request ID.
- Fake Provider that can return ACCEPTED/REJECTED, delay, lose ACK, callback twice and remain IN_DOUBT.
- Deterministic clock and concurrency scheduler for race tests.
- Fault hooks around transaction commit, outbox publish, lease renewal, provider dispatch, Applied persistence and restore release.
- Ephemeral CI environment; no persistent user data.
- Audit evidence stored separately from debug logs; no forgotten plaintext in traces.

No Redis, Kafka, Qdrant, Neo4j, Temporal, Restate, DBOS or Kubernetes is required to run the first test harness.

## 10. Build / run / test acceptance commands / 构建运行测试命令

The repository currently has no Rust implementation workspace. The following are **target commands** for the proposed future workspace; they are not runnable or claimed as passing today.

```bash
# Formatting and static checks
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings

# Unit and property tests
cargo test --workspace
cargo test --workspace --features property-tests

# Storage profile conformance (after profile implementations exist)
cargo test -p brain-storage --features sqlite
cargo test -p brain-storage --features postgres

# Integration and fault injection
cargo test -p brain-integration-tests
cargo test -p brain-fault-tests -- --test-threads=1

# Full local vertical slice (after binary and fixtures exist)
cargo run -p brain-app -- demo-vertical-slice --profile sqlite
cargo run -p brain-app -- verify-restore-fence --profile sqlite
```

Acceptance output must record:
- exact commit and Rust toolchain;
- selected profile, engine version and configuration;
- test names/counts/results and skipped tests;
- injected failure schedule and observed durable states;
- evidence bundle refs/digests;
- no hidden ignored/disabled critical test.
A command exiting zero is necessary but not sufficient; independent reviewers must inspect the invariant assertions and exact logs.

## 11. Product adoption triggers / 产品采用触发条件

- **Temporal/Restate/DBOS:** only if durable workflows need multi-day timers, human approvals, complex compensation, cross-service orchestration or replay volume beyond the SQL work table; benchmark operational burden and preserve Brain-owned state.
- **External broker:** only if measured outbox throughput/backpressure or independent worker scaling requires it; canonical order remains D-issued, broker ACK is not commit.
- **Qdrant:** only if pgvector/embedded ANN cannot meet measured recall/latency under strict scope filters or sharding needs; dual-store Forget/restore proof required.
- **Tantivy:** only if native FTS fails labeled multilingual ranking/tokenization/throughput tests.
- **Neo4j:** only if typed SQL relations and bounded recursive queries fail real graph workload targets.
- **Redis:** only if multi-process shared cache has measured benefit; every hit still revalidates D/I state.
- **OpenFGA:** only if high-fanout ReBAC graph workload justifies service and tuple consistency; I remains grant/revocation authority.
- **OPA:** only if cross-language policy distribution or policy ecosystem need outweighs sidecar/management cost; I remains policy authority.
- **S3/object store:** only if multi-host/HA/storage scale requires it; blob lineage, deletion and restore high-waters remain Brain governed.
- **Multiple Agent runtimes:** only after one adapter meets C/G/H conformance and a second runtime has a real user requirement.

## 12. Exit criteria / 退出条件

This proposal becomes implementation-ready only after:
1. B Fact/Claim ADR decision or an approved typed neutral candidate boundary for the first slice.
2. D/Storage exact L1 anchor schema, row ownership, transaction operation and L4 profile acceptance.
3. I authorization/PermissionEpoch/CommitAuthorizationReceipt integration and fail-closed PEP tests.
4. D/I/E/F Forget producer inventory, barrier and target completion evidence acceptance.
5. G/C/H Applied exact binding, CSubmitOutcome and H evidence schema acceptance.
6. COC/JF-10 same-GID applicability and physical proof contract acceptance.
7. Bilingual normative parity and source-of-truth publication.
8. Executable 20-scenario fault matrix and restore anti-rollback tests.
9. Independent review against all six non-negotiable authorities.

**Disposition: modular Rust monolith + one per-authority SQL serialization domain + SQL work/outbox + native lexical retrieval is the minimum candidate. No physical database, product stack or production topology is frozen.**

**处置结论：模块化 Rust 单体 + 每 Authority 一个 SQL 序列化域 + SQL Work/Outbox + 原生全文检索，是当前最小候选方案。没有冻结物理数据库、产品栈或生产拓扑。**
