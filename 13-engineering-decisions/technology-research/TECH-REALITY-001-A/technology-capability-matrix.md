# Technology Capability Matrix / 技术能力映射矩阵

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Source baseline: `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Status: **TECHNICAL ASSESSMENT — NOT AN ADR / 技术评估，不是 ADR**

## 1. Classification / 分类

- **M1 — Mature direct support:** a mature component provides the core primitive, subject to configuration.
- **M2 — Mature composition:** mature components exist, but Brain-specific orchestration/adaptation is required.
- **M3 — Project-owned logic:** no mature off-the-shelf component can own the Brain-specific semantic invariant.
- **M4 — Feasible, unproven:** technically plausible but requires prototype/fault evidence.
- **M5 — Fundamental risk:** candidate topology may be unable to provide the claimed guarantee without changing assumptions.

## 2. Capability map / 能力映射

| Capability | Current design / contract | Candidate mature mechanism | What it really provides | Gap / Brain-owned work | Class / risk |
|---|---|---|---|---|---|
| Canonical Memory persistence | Canonical assets, revisions, lifecycle, provenance and typed cursors | SQLite transactions; PostgreSQL MVCC/locks; SQL migrations | Atomic SQL rows within one database transaction; constraints, indexes, recovery tooling | Schema, authority API, immutable revision semantics, cursor CAS/ordering, blob coordination, backup and migration | M2/M4; high |
| Durable Event acceptance | Event + processing intent durable before Accepted | SQL transaction + outbox + DB worker; NATS/Temporal if justified | Atomic SQL write to event and outbox; broker delivery/worker retry when adopted | Exact idempotency namespace/retention, payload/blob staging, receipt semantics, replay and admission | M2/M4; high |
| Durable Workflow | Compiler and Forget work with leases, retries, recovery | SQL lease/outbox; Temporal; Restate | Retry, timers, durable history/steps, worker task delivery depending on engine | Integrate with canonical DB and owner-specific fence semantics; prove no workflow side effect bypass | M2/M4; high |
| Forget / anti-resurrection | Fence, inventory, barrier, derived suppression, restore replay | SQL locking/CAS, transaction isolation, append-only audit, index delete/rebuild | SQL serializes committed operations inside its transaction scope | Cross-owner producer admission, fence install, dependency registration and publication linearization; external recipients/backups; physical erasure policy | M3/M4; critical |
| Evidence & provenance | Source Evidence and lineage for each derived asset | Relational foreign keys, append-only revisions, blob hashes, graph edges | Referential integrity and immutable content identity within defined storage boundaries | Provenance semantics, Evidence authorization, retention and derivative lineage | M2/M3; high |
| Retrieval | Structured + lexical + vector + temporal/relational channels | SQL indexes, FTS5, Tantivy, pgvector/Qdrant/LanceDB | Query filtering, BM25, ANN and hybrid candidate generation | Ranking/activation, freshness, provenance, authorization and Forget suppression before context | M2/M4; medium-high |
| Entity resolution | Entity identity, merge/split, relations and conflict history | Graphiti patterns; relational unique/alias tables; LLM proposal | Entity extraction/dedup proposals and graph traversal | Canonical identity authority, reversible merge/split, evidence and deterministic validation | M2/M3; high |
| Context versioning | One authoritative ContextVersion sequence, snapshots/deltas, Applied evidence | SQL optimistic concurrency/CAS; Agent Adapter hooks | Atomic version increments and base-version conflict checks in one DB | Exact inference-boundary integration, Applied proof and reconnect/Forget semantics | M2/M4; critical |
| Protocol | BMCP versioned schema, capabilities, ACK taxonomy | Serde JSON/CBOR; HTTP/local IPC/gRPC | Serialization, transport, generated clients/validation | H-owned wire schema; authenticated identity binding; C final-request evidence; cross-language conformance | M2/M4; high |
| Authorization | Scope distinct from Permission; revocation and epochs | Cedar embedded Rust engine; OpenFGA/SpiceDB service; OPA/Rego | Policy evaluation or relationship graph checks | I-owned identity issuance, current policy, revocation propagation, in-flight operation control, audit | M2/M4; critical |
| Cache | Bounded, disposable working-set cache | Moka in-process; optional distributed cache later | Local cache concurrency/eviction | Typed cache keys, epoch/fence invalidation and mandatory authoritative re-check | M1/M2; medium |
| Observability | Cross-module correlation, no protected data leakage | Rust tracing; OpenTelemetry; Prometheus/Grafana | Spans, metrics, structured telemetry and exporters | Semantic trace IDs, redaction, audit separation, operational SLOs | M1/M2; medium |
| Backup & recovery | DB + blob + indexes + Forget/revocation replay | SQLite backup API / pgBackRest-like DB-native backup + blob manifests | Database-consistent snapshot and restore primitives | Coordinated DB/blob snapshot, version manifests, restore isolation and anti-resurrection gate | M2/M4; critical |
| Deployment | Local modular monolith first; optional workers | Rust binary, systemd/OCI, optional inference worker | Packaging, process isolation, restart and resource limits | Migration/upgrade, health, backup, secrets, OS matrix and operator workflow | M2/M4; medium-high |

## 3. Capability details / 能力说明

### 3.1 Storage is the transaction authority, not a collection of repository interfaces

A repository abstraction does not prove a transaction. For every correctness-critical transition, the design must identify the exact database transaction, lock/CAS operation, isolation level, uniqueness constraint, commit point and recovery read. Cross-database or filesystem operations need a staged protocol with explicit intermediate states and compensation/reconciliation; they are not magically included in an SQL transaction.

存储接口并不等于事务证明。每个关键状态迁移都必须指出具体数据库事务、锁/CAS 操作、隔离级别、唯一约束、提交点和恢复读取方式。跨数据库或文件系统操作需要显式阶段状态、补偿与对账协议，不会自动进入 SQL 事务。

### 3.2 Forget is not a product feature supplied by a database

A database can serialize a set of row updates, but it cannot discover every producer, worker, external provider, index, cache, Agent Adapter, replica, backup and restore target. The Brain must own the inventory and cross-owner protocol. Physical erasure, cryptographic erasure, logical suppression and downstream acknowledgement are separate guarantees.

数据库可以串行化一组行更新，但不能自动发现所有 Producer、Worker、外部 Provider、索引、缓存、Agent Adapter、副本、备份和恢复目标。Brain 必须拥有目标清单与跨 Owner 协议。物理擦除、密码学擦除、逻辑抑制和下游确认是不同保证。

### 3.3 Retrieval indexes are projections

FTS5/Tantivy/Qdrant/LanceDB can find candidates. They do not decide whether a candidate is canonical, authorized, current, non-forgotten or epistemically qualified. The Brain must apply authoritative filters before a result can affect ranking, summary, activation or context.

FTS5/Tantivy/Qdrant/LanceDB 能够生成候选结果，但不能决定候选是否为 Canonical、是否获授权、是否最新、是否已被 Forget 或是否具有合适的认知状态。Brain 必须在候选影响排序、摘要、激活或 Context 之前执行权威过滤。

### 3.4 Durable workflow is orthogonal to domain transactions

Temporal/Restate can durably execute steps and recover orchestration. They do not automatically join a workflow history transaction to a canonical SQL transaction. Workflow completion must never be used as a substitute for CanonicalCommitCursor, Applied attestation or Forget completion evidence.

Temporal/Restate 能够持久执行步骤并恢复编排，但不会自动把 Workflow History 事务加入 Canonical SQL 事务。Workflow 完成不能替代 CanonicalCommitCursor、Applied 证明或 Forget 完成证据。

## 4. Current critical gaps / 当前关键缺口

1. D/E/Storage admission/fence/dependency/publication operation semantics and physical topology remain OPEN/ADR-BLOCKED.
2. B Fact/Claim and typed identity semantics affect storage schema, index keys, protocol serialization and migrations.
3. C/G/H Applied evidence remains not frozen; exact final-request observation and adapter attestation must be mapped.
4. I identity, policy, revocation, global Forget target inventory and cryptographic erasure decisions remain I-owned.
5. Workload inputs and retrieval evaluation dataset are not supplied; no quantitative selection can be made.
6. No Brain implementation or prototype has demonstrated the composed guarantees.

## 5. Decision rule / 决策规则

No row becomes DECIDED by this matrix. Each choice must be moved into the owning ADR only after: (a) exact owner contract pin, (b) competing candidate comparison, (c) minimal prototype, (d) crash/race/fault tests, (e) migration and recovery plan, and (f) independent review.


## 6. Updated Storage evidence / Storage 最新证据补充

The current Storage branch's serialization ADR addendum (Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`) selects **one logical serializable transaction domain per Canonical Memory authority** as the normative v1 serialization architecture. It covers D admission/fence/dependency/publication-participant records and Storage hidden participant/final VisibilityPointer/PublicationReceipt/outcome/outbox records while keeping D and Storage semantic authorities separate. I's PolicyDomain sequencer and COC quorum log remain independent.

This is an architecture-level logical profile, not a physical database selection. The PostgreSQL 18.7 capability dossier (Blob `0aabf66848dc97deee028c571183c0d7204008c0`) records bounded CI engine capability PASS for prepared-XID persistence and same-XID recovery, synchronous failover, backup/restore, ACK-loss and PITR subtests. It does not prove the Brain's D/I/COC adapters, integrated publication races, production deployment or JF-10 end-to-end behavior. Gate A PARTIAL PASS / OPEN; JF-10 runtime P0 OPEN.

Storage 当前分支的序列化 ADR 补充条款（Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`）选择**每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain**作为 v1 规范性序列化架构，覆盖 D Admission/Fence/Dependency/PublicationParticipant 与 Storage Hidden Participant/最终 VisibilityPointer/PublicationReceipt/Outcome/Outbox，同时保持 D 和 Storage 的语义权威分离。I 的 PolicyDomain Sequencer 与 COC Quorum Log 仍独立。

这是逻辑架构档案，不是物理数据库选型。PostgreSQL 18.7 能力档案（Blob `0aabf66848dc97deee028c571183c0d7204008c0`）记录了 Prepared-XID 持久化与同 XID 恢复、同步故障切换、备份恢复、ACK 丢失和 PITR 的有限 CI 引擎能力 PASS。它不能证明 Brain 的 D/I/COC Adapter、集成 Publication 竞争、生产部署或 JF-10 端到端行为。Gate A PARTIAL PASS / OPEN；JF-10 runtime P0 OPEN。
