# Technology Architecture Blueprint

- Document ID: TAB-001
- Version: 0.1
- Date: 2026-11-17
- Repository: oahcom/AiMemoryBrainArchitecture
- Baseline commit: 8a6414158c9c056c1638222534e1993d1bbc99d2
- Status: **CANDIDATE SYSTEM-WIDE BLUEPRINT — NOT A TECHNOLOGY FREEZE**
- Scope: technology layers, component topology, deployment, persistence, indexing, model inference, data flows, resource budgets, engineering boundaries, and validation gates.
- Coordination owner: A. Domain owners B–I retain authority over their own contracts and decisions.

## 1. Purpose and decision status

This document translates the existing logical architecture into a technology architecture for engineering planning. It supplements, and does not replace, the A–I ownership model or existing system invariants.

The Brain remains an Agent- and model-independent memory authority. Canonical Memory, Memory Context, and Applied Context remain separate. Durable ingestion, provenance, Scope/Permission enforcement, inference-boundary application, and governed Forget remain mandatory.

Technology statements use these statuses:

| Status | Meaning |
|---|---|
| DECIDED | Existing architecture constraint or formally accepted project decision. |
| RECOMMENDED | Preferred engineering direction, pending owner review and any required ADR. |
| CANDIDATE | Viable option requiring comparative evaluation. |
| TO_VALIDATE | Requires prototype, fault injection, benchmark, or security evidence. |
| OPEN | Unresolved decision or dependency. |

A recommendation here is not an approved ADR. No library, database, model, transport, or deployment choice becomes normative merely by appearing in this document.

## 2. Architecture drivers and constraints

### 2.1 Drivers

1. Local-first, reusable Memory Brain independent of Agent frameworks and LLM vendors.
2. Rust as the primary language for core control, persistence coordination, domain logic, retrieval orchestration, and runtime services.
3. Durable memory continuity across Agents, models, sessions, and environments.
4. Correctness, provenance, authorization, recoverability, and Forget safety take precedence over raw retrieval throughput.
5. Support multiple Agent instances with isolated Runtime Sessions and Contexts while sharing authorized canonical memory infrastructure.
6. First implementation should be operable on a local workstation; unnecessary distributed infrastructure is deferred.
7. Optional local model inference must fit a constrained GPU profile, with 12–16 GB VRAM as the current planning envelope.
8. Logical subsystem boundaries do not automatically imply process, service, database, or crate boundaries.

### 2.2 Non-goals

- Building an Agent planner, tool executor, browser, terminal, or multi-agent orchestration framework.
- Owning model internals or requiring a specific LLM family.
- Requiring a cloud control plane or hosted vector database for the first local deployment.
- Introducing Kafka, Kubernetes, microservices, or a distributed database before measured requirements justify them.
- Claiming physical erasure from a logical tombstone, cache invalidation, or primary-row deletion alone.

### 2.3 Carried-forward constraints

- Canonical Memory is authoritative; indexes and caches are rebuildable derived representations.
- Memory Context has its own authoritative version sequence; Context edits do not mutate Canonical Memory.
- Event Accepted, Compiler Completed, Canonical Committed, Indexed, Delivered, and Applied are distinct states.
- Intent and plans are not completed outcomes.
- Memory, Evidence, Provenance, and summaries are untrusted data, not instruction authority.
- Scope and Permission are separate.
- Forget must prevent late producer work and derived artifacts from resurrecting suppressed memory.
- D's selected CanonicalCommitCursor semantics are one global ordered sequence per Canonical Memory Authority. AggregateRevision, LifecycleEventCursor, IndexWatermark, ContextVersion, PermissionEpoch, and ForgetFenceGeneration remain distinct typed values.
- The D/E/Storage atomic producer-admission, fence-installation, dependency-registration, and publication contract remains OPEN pending implementable operation semantics and tests.
- B's Fact/Claim ADR remains ADR-BLOCKED; no schema or wire field depending on its unresolved choice may be frozen.

## 3. Technology architecture at a glance

The recommended first implementation shape is a **modular Rust monolith with explicit ports/adapters and durable local storage**, plus an optional isolated model-inference worker and Agent Adapters embedded in or adjacent to Agent runtimes.

Logical architecture:
1. Agent Integration and BMCP boundary.
2. Ingress and Telemetry normalization.
3. Memory Compiler pipeline.
4. Canonical Memory domain and lifecycle authority.
5. Memory Runtime: retrieval, activation, working sets.
6. Memory Context Manager and synchronization.
7. Cross-cutting identity, authorization, Forget, consistency, audit, and observability.

Technology architecture:
1. Rust application host and async runtime.
2. Transactional metadata/event store.
3. Content-addressed blob store for large source payloads.
4. Rebuildable lexical and vector indexes.
5. Cache and bounded working-set layer.
6. Model provider abstraction with optional local inference backends.
7. Versioned protocol/transport adapters.
8. Diagnostics, backup, migration, and recovery tooling.

Correctness-critical state transitions should initially remain in one process and one transactional authority wherever practical. Model inference is an optional resource-heavy boundary and may run in a separate process so GPU failure, model loading, or inference stalls cannot block durable Event acceptance or canonical recovery.

## 4. Technology layers and recommended choices

### 4.1 Language, build, and runtime

| Concern | Recommendation | Status | Rationale / constraints |
|---|---|---|---|
| Primary language | Rust | DECIDED direction | Explicit types and ownership for state machines, concurrency, and storage coordination. |
| Async runtime | Tokio | RECOMMENDED | Mature ecosystem for network IO, background workers, timers, and task supervision. |
| Serialization | Serde | RECOMMENDED | Shared typed serialization for internal contracts and persisted envelopes. |
| Error model | thiserror in libraries; anyhow at application boundaries | CANDIDATE | Preserve machine-readable error classes and retryability. |
| Tracing | tracing + tracing-subscriber | RECOMMENDED | Correlate Event, WorkItem, Memory, Context, Delivery, and ForgetOperation. |
| Metrics | metrics facade or OpenTelemetry metrics | CANDIDATE | Keep instrumentation independent from exporters. |
| Property testing | proptest | RECOMMENDED | State-machine, cursor, idempotency, and race invariants. |
| Fuzzing | cargo-fuzz/libFuzzer | CANDIDATE | Protocol parsers, schema migration, identifiers, and untrusted payload boundaries. |

Rust crate boundaries are implementation boundaries, not separate services. The initial crate map is in Section 10.

### 4.2 Persistence and transaction authority

**Recommended first prototype: SQLite in WAL mode**, behind a Storage interface. This is a conditional recommendation for a single-node, local-first first release, not a final decision.

| Option | Strengths | Risks / limits | Evaluation |
|---|---|---|---|
| SQLite + WAL | Embedded, low operational burden, transactional, local deployment friendly | Single-writer behavior, write contention, migration discipline, backup coordination | First prototype and single-node benchmark |
| PostgreSQL | Strong concurrent transaction model, mature operations, multi-process and multi-user scaling | Separate service and operational footprint | Required comparison if concurrency or remote deployment requires it |
| RocksDB or other embedded KV | High write throughput and flexible key-value layout | Transaction and relational semantics require more application design; compaction/backup complexity | Only if measured workloads outgrow SQL options |

Storage principles:

- Canonical records, revisions, events, receipts, idempotency records, producer registrations, Forget fences, dependency registrations, outbox records, and recovery checkpoints need explicit transactional semantics.
- CanonicalCommitCursor update must be atomic with the canonical change it orders. Storage/Consistency realization remains TO_VALIDATE.
- Accepted Event plus durable processing intent must be atomic or recoverably equivalent; acknowledgement must not precede durable acceptance.
- Producer admission versus Forget fence installation requires a proven linearization point. A read-then-write check is insufficient.
- Dependency registration and publication visibility require a defined atomic or linearizable gate. Staged derivatives remain invisible until the gate succeeds.
- SQLite WAL does not by itself prove that the D/E Forget race contract is satisfied. Transaction/locking design and crash/race tests are mandatory.
- An index must never be the sole authority for canonical truth.

**Storage layout recommendation:**

- SQLite database for metadata, canonical records, revisions, events, receipts, state machines, cursors, outbox, and governance records.
- Content-addressed filesystem blob store for large raw payloads, attachments, source documents, and immutable source artifacts.
- Blob metadata includes digest, byte length, media type, encryption/key reference, retention class, provenance, and lifecycle state.
- A blob becomes referentially visible only after durable write and metadata registration; orphan cleanup is recoverable and auditable.
- Database and blob-store backup/restore coordination is explicit. A database snapshot without its referenced blobs is not a complete backup.

### 4.3 Search and index architecture

Use multiple retrieval channels rather than treating vector similarity as the complete memory search system.

| Channel | Candidate | Status / decision rule |
|---|---|---|
| Structured filters | SQL indexes | RECOMMENDED for Scope, Principal, Environment, validity, lifecycle, epistemic status, entity and typed references |
| Full-text | SQLite FTS5 | RECOMMENDED first comparison for simplest colocated deployment |
| Full-text | Tantivy | CANDIDATE when indexing throughput, ranking control, tokenization, or corpus scale justify a separate Rust index |
| Vector ANN | usearch/HNSW or equivalent embedded ANN | CANDIDATE; benchmark corpus size, update/delete rate, memory, recall, and rebuild |
| Vector in SQLite | sqlite-vec or equivalent extension | CANDIDATE; evaluate maturity, filtering, persistence, and operations |
| Reranking | Cross-encoder or compact reranker behind ModelProvider | TO_VALIDATE; adopt only if quality gain justifies latency and model resources |

Index rules:

1. Indexes are derived from committed canonical changes and carry typed per-channel/per-partition watermarks.
2. IndexWatermark is not CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, or ForgetFenceGeneration.
3. Scope and Permission filtering must occur before unauthorized candidates can affect ranking, summaries, or context.
4. A stale or behind-fence index must not expose forgotten content. Query paths apply authoritative suppression/fence checks or fail closed.
5. Index rebuild consumes canonical history and current Forget state; it must not reintroduce forgotten data.
6. Update/delete behavior, tombstone compaction, per-scope filtering, backup, and deterministic rebuild are selection criteria.
7. The first release may begin with structured + lexical retrieval and add vector retrieval after embedding and evaluation data are stable.

### 4.4 Cache and working-set technology

- In-process cache candidate: Moka.
- Cache keys include relevant Authority, Scope, PermissionEpoch, ForgetFenceGeneration, Context identity/version, and query semantics.
- Cache entries are disposable; they are never authority for authorization, Forget, canonical truth, or Applied state.
- Cache invalidation is generation-aware; TTL alone is not a Forget guarantee.
- Runtime working sets are bounded by item count, bytes, token budget, and age.
- Cache misses and eviction must be safe; cache hits still satisfy current authorization and suppression requirements.
- Prefer a small number of explicit cache classes over one untyped global cache.

Status: Moka is RECOMMENDED as a first in-process cache candidate, subject to invalidation and memory-bound tests. A distributed cache is not required initially.

### 4.5 Model and inference architecture

Model independence is a DECIDED architecture constraint. Model implementations are replaceable providers.

Define separate capability interfaces:

- EmbeddingProvider: content to vector plus model/version/dimension metadata.
- RerankerProvider: query plus authorized candidates to reranked scores.
- ExtractionProvider: source content to candidate structured extraction.
- ResolutionProvider: entity/claim resolution proposals.
- SummarizationProvider: context compaction with source references preserved.
- GeneralLLMProvider: optional model-assisted operation, never a dependency for durable ingress or core authority.

Candidate local backends:

| Workload | Candidate backend | Status / notes |
|---|---|---|
| Embedding / reranking | ONNX Runtime when compatible ONNX artifacts exist | CANDIDATE; validate operators, execution provider, quantization, CPU/GPU, packaging |
| Local generative LLM | llama.cpp-compatible backend for GGUF models | CANDIDATE; process isolation recommended; weights/context/KV cache determine VRAM |
| Rust-native experimentation | candle or another Rust inference runtime | CANDIDATE; evaluate model/operator coverage and operational maturity |
| Remote inference | Provider adapter behind explicit policy and credentials | OPTIONAL; disabled unless configured and authorized; govern residency and retention |

Inference rules:

1. Durable Event acceptance cannot wait for model loading or inference.
2. Deterministic validation, authorization, idempotency, and suppression checks remain in the Rust core.
3. Model output is a proposal with provenance and confidence metadata, not Canonical Truth.
4. Model failure creates retryable/degraded Compiler state; it must not lose accepted source data.
5. No model receives data outside its authorized Scope and declared provider policy.
6. Model and tokenizer versions are recorded with derived artifacts for reproducibility and reprocessing.
7. Do not run embedding, reranking, and large LLM workloads concurrently on a constrained GPU by default. Use GPU admission scheduling and sequential/bounded execution.
8. Keep CPU fallback for small embedding or deterministic tasks where practical; define degraded behavior when GPU is unavailable.
9. Model context window and GPU VRAM are separate budgets. Enforce context and concurrency limits.
10. Model-assisted summarization preserves source Memory/Evidence references.

### 4.6 Protocol and transport

BMCP remains the logical Brain–Agent/Adapter protocol. H owns normative wire schema, versioning, capability negotiation, and acknowledgement semantics.

Technology direction:

- Define transport-independent typed message contracts first.
- Keep protocol/schema version, capability epoch, identity binding, correlation ID, and idempotency metadata explicit.
- JSON is a practical human-debuggable initial encoding candidate; CBOR/MessagePack are alternatives if payload size or binary efficiency becomes material.
- HTTP is a practical interoperability transport candidate. Local IPC (Unix domain sockets, Windows named pipes, or loopback) may be added behind a transport adapter.
- gRPC is a candidate only if streaming, generated SDKs, and cross-language interoperability justify its complexity.
- Do not freeze JSON, CBOR, HTTP, gRPC, or field layout in this system blueprint. H decides after compatibility, security, and Adapter conformance review.
- Authentication binds to transport/security context; payload-supplied ActorRef, ProducerId, or AdapterId is a claim, not proof.
- Delivered, Accepted, Applied, Cleared, and Global Forget Completed are different evidence classes.

### 4.7 Security, identity, and cryptography

Security technology must be selected against I's policy contract and threat model.

Required capabilities:

- OS-backed secret/key storage where available; otherwise documented local key storage with restrictive permissions and rotation procedure.
- Authenticated local IPC or mutually authenticated remote transport where remote access is enabled.
- Encryption at rest for sensitive payloads when the threat model requires it; define key ownership, rotation, backup, and cryptographic-erasure implications.
- Authenticated Adapter attestations where the trust boundary requires proof beyond an in-process callback.
- Append-only or tamper-evident audit strategy for governance actions, subject to retention and privacy constraints.
- Vetted cryptographic libraries; no custom cryptography.
- Redaction of sensitive payloads from logs, traces, crash dumps, and benchmark artifacts.

Exact algorithms, key custody, Principal/ActorRef/ScopeRef mapping, and PermissionEpoch fields remain OPEN until I/B/H decisions and threat-model review. Do not freeze them here.

### 4.8 Observability and operations

Recommended instrumentation:

- tracing spans across InferenceRequest, Event, Receipt, CompilerWorkItem, Memory, CanonicalCommitCursor, ForgetOperation, ContextVersion, Delivery, and Adapter acknowledgement.
- Metrics for queue depth/age, retries, lease age, producer barrier progress, fence rejections, canonical commit latency, index lag, cache hit rate, retrieval latency, context reconciliation, Applied lag, GPU/VRAM, model latency, and backup/restore status.
- Structured logs with stable IDs and typed errors; raw memory content is excluded by default.
- Health/CLI diagnostics distinguish liveness, readiness, degraded model availability, index lag, and governance/Forget blockers.
- Audit records are separate from diagnostic logs and follow I's retention policy.

Candidate stack: tracing, tracing-subscriber, a metrics facade, OpenTelemetry exporters, and Prometheus-compatible scraping. Final exporter and dashboard remain deployment choices.

## 5. Component relationship and technology ownership

A–I remain the domain ownership model. This mapping does not force one crate or process per letter.

| Module | Technology-facing responsibility | Main implementation dependencies |
|---|---|---|
| A — Architecture/Integration | ADR registry, contract matrix, compatibility and conformance governance | Documentation, schema registry process, CI, test harness |
| B — Domain Model | Typed identifiers, domain types, Fact/Claim semantics, Scope references | Rust domain crate, Serde schemas, property tests |
| C — Agent Integration | Telemetry contract, inference boundary requirements, Agent-side conformance | Adapter SDK interfaces, test fixtures, capability model |
| D — Memory Brain | Canonical authority, lifecycle, versions, Forget fence, cursor semantics | Transaction API, storage ports, audit and recovery |
| E — Memory Compiler | Durable ingress, work state machine, extraction, provenance, staged derivatives | Outbox/worker runtime, model providers, blob store |
| F — Memory Runtime | Retrieval routing, ranking, activation, cache and working sets | SQL/FTS/vector indexes, Moka, optional reranker |
| G — Memory Context | Context planner/editor/version/reconciliation and delivery intent | Canonical refs, Runtime proposals, protocol delivery adapter |
| H — BMCP | Wire schema, transport, capability negotiation, Adapter ACK | Serde/schema validation, transport adapters, SDK |
| I — Security/Governance | Principal/Permission policy, revocation, target inventory, retention and global Forget evaluation | Policy interfaces, audit, key management, target evidence |

Cross-cutting shared interfaces include identity context, authorization decision, time abstraction, typed cursor, idempotency, transactional outbox, audit, tracing, and storage transactions. Shared interfaces must not create duplicate authority.

## 6. Rust implementation architecture

### 6.1 Initial crate map

| Crate | Responsibility |
|---|---|
| brain-domain | Domain types, identifiers, enums, invariants, validation |
| brain-contracts | Internal command/event/query contracts and typed errors |
| brain-storage | SQL migrations, transaction interfaces, canonical persistence, blob metadata |
| brain-ingress | Authenticated ingress, schema validation, idempotent acceptance, outbox |
| brain-compiler | Work orchestration, extraction stages, evidence/provenance, consolidation proposals |
| brain-index | Lexical/vector index adapters, index watermarks, rebuild workers |
| brain-retrieval | Structured/lexical/vector candidate retrieval, filtering and ranking |
| brain-runtime | Activation, scheduling, bounded working sets and cache orchestration |
| brain-context | Context planning, edit operations, versioning and reconciliation |
| brain-protocol | BMCP message types, validation and version negotiation |
| brain-adapter-sdk | Agent-facing integration interfaces and conformance helpers |
| brain-governance | Authorization interfaces, Forget orchestration, retention and audit policy |
| brain-observability | Tracing, metrics, diagnostics adapters |
| brain-app | Application composition, configuration, lifecycle, CLI/service entry points |

This is a candidate crate map. It may be consolidated during implementation; it is not a mandate to create every crate immediately.

### 6.2 Dependency rules

- Domain crates do not depend on concrete database, index, model, or transport implementations.
- Storage adapters implement explicit transaction and repository ports.
- Compiler creates proposals but cannot bypass Canonical Memory authority.
- Index workers consume committed changes and never become authoritative.
- Retrieval applies authorization and Forget suppression before results influence context.
- Context authority is isolated from retrieval and Adapter delivery.
- Protocol types do not redefine B's domain types; use versioned mapping layers.
- Model providers are injected through capability interfaces.
- Governance checks are enforced at every protected boundary, not only at the API gateway.
- Avoid cyclic crate dependencies. Shared contracts belong in small lower-level crates.

### 6.3 Application composition

The brain-app process owns startup/shutdown, configuration, worker supervision, connection pools, transaction coordinators, and health reporting. It wires modules through interfaces. Failure in optional model inference must not prevent storage recovery, read-only diagnostics, or durable ingress where safe.

## 7. Deployment topology

### 7.1 First deployment: local modular monolith

Recommended topology:

- One Brain application process containing Rust domain/application modules.
- One local transactional database authority.
- One content-addressed blob directory managed by Brain.
- One or more rebuildable index files/directories.
- In-process bounded caches and Runtime Session state.
- Optional isolated inference worker process for local LLM/embedding workloads.
- Agent Adapter embedded in the Agent runtime or deployed as a separate local integration process.
- CLI/admin interface for diagnostics, migrations, backup, restore, and governance operations.

Logical boundaries remain independent even when they share a process.

### 7.2 Process topology

Conceptual topology:

    Agent Runtime
      Agent / LLM
        Agent Adapter: BMCP client, telemetry mapper, inference boundary
              |
              | authenticated local or remote transport
              v
    Brain Application Process
      Protocol Gateway | Identity/Policy | Ingress/Observer
      Compiler Workers | Canonical Brain | Runtime/Retrieval
      Context Manager | Forget Coordinator | Audit/Recovery
      Transaction/Outbox Coordinator | Tracing/Metrics
              |                         |
              v                         v
        SQLite + WAL             Content-addressed blob store
              |
          +---+----------------------+
          |                          |
          v                          v
      Lexical index              Vector index
      FTS5/Tantivy               ANN candidate

    Optional Inference Worker
      Model Provider API | Embedding | Reranking | Local LLM
      GPU admission / queue / model lifecycle / resource limits

This is conceptual. It does not prescribe a specific transport or require all boxes to be separate processes.

### 7.3 When to split processes or services

Split only when measurable reasons exist:

- GPU inference must be isolated from core availability and memory pressure.
- A worker needs independent restart/scaling or crash containment.
- Index rebuilds materially interfere with interactive retrieval.
- Multiple Brain processes need concurrent transactional writes beyond the embedded store's tested envelope.
- Remote Agents require a network-facing gateway with a distinct security boundary.
- Operational deployment requires independent upgrades or fault domains.

Do not split merely because A–I or crate boundaries exist.

### 7.4 Future deployment evolution

Potential later topology, only after evidence:

1. Single-node modular monolith.
2. Single-node Brain core plus isolated compiler/index/inference workers.
3. Multi-process local deployment with explicit storage coordination.
4. Optional PostgreSQL-backed multi-user/multi-host deployment.
5. Remote inference providers or external Adapters under explicit data governance.

Each step requires migration planning for identity, canonical cursors, transaction boundaries, outbox delivery, index watermarks, Forget fences, backups, and protocol compatibility.

## 8. End-to-end data flows

### 8.1 Experience-to-memory flow

1. Agent/Environment Adapter emits a typed event or telemetry observation.
2. Protocol boundary authenticates transport, validates schema, resolves Principal/Scope, and authorizes ingress.
3. Ingress validates idempotency and durable payload reference.
4. Event plus durable processing intent is committed atomically or through an equivalent recoverable protocol.
5. Ingress returns Accepted receipt; this does not imply compilation or canonical commitment.
6. Compiler worker obtains durable work-item admission tied to the current Forget fence.
7. Deterministic normalization and optional model-assisted extraction create staged candidate artifacts.
8. Evidence and provenance links are durably registered.
9. Canonical Brain validates domain semantics, lifecycle, conflicts, Scope, and policy.
10. Canonical commit writes the new revision and typed CanonicalCommitCursor.
11. Outbox/change feed drives index and Runtime consumers.
12. Each index channel advances its own watermark only after durable publication.
13. Runtime retrieves only authorized, current, non-suppressed records.

### 8.2 Runtime recall and activation flow

1. Adapter sends a scoped query and current telemetry.
2. Brain authenticates and authorizes the request.
3. Retrieval applies Scope, Permission, environment, time, lifecycle, and Forget suppression constraints.
4. Structured and lexical channels retrieve candidates; vector retrieval and reranking are optional.
5. Candidate results include canonical references, revisions, provenance, freshness, and epistemic status.
6. Activation policy determines relevance and proposes context changes.
7. Context Manager checks budget, sufficiency, version, and concurrent-edit rules.
8. Context Manager commits one authoritative ContextVersion and ChangeSet.
9. Synchronization sends a delta or full snapshot through BMCP.
10. Adapter validates and stages delivery.
11. At the next inference assembly boundary, Adapter applies the exact Brain-managed region.
12. Adapter returns Applied attestation bound to final request, ContextVersion, Delivery, identity, PermissionEpoch, ForgetFenceGeneration, and capability.
13. Context synchronization validates acknowledgement; it does not infer model comprehension.

### 8.3 Forget and anti-resurrection flow

1. I-governed request authenticates and authorizes Forget.
2. Target inventory is sealed; unknown producer/recipient domains block completion or require an explicit approved exception.
3. D installs a durable Forget fence with a linearizable relation to producer admission.
4. Pre-fence work is included in the barrier and must reach durable terminal disposition.
5. E prevents stale work, retries, DLQ replay, recompile, and late derivatives from becoming visible.
6. D/E/Storage enforce dependency registration and final publication gate against the current fence and PermissionEpoch.
7. F suppresses affected retrieval/index/cache/working-set representations and advances typed channel watermarks.
8. G invalidates or reconciles Context entries, snapshots, deltas, and pending deliveries.
9. H/C coordinate Adapter-local suppression, clear, queued-delivery cancellation, reconnect, and attestation.
10. I evaluates external recipients, backups, replicas, restore suppression, retention expiry, and physical-erasure requirements.
11. Global completion is a typed evidence vector; missing, unknown, failed, or unsupported required targets do not silently become success.
12. Restore/rebuild/replay paths reapply Forget state before data becomes queryable.

This is an architecture requirement, not evidence that all steps are implemented. D/E/Storage atomicity, F/G/H evidence, and I target mapping remain open until owner decisions and conformance tests close them.

### 8.4 Recovery and replay flow

- Durable accepted events and outbox records are replayable by stable IDs and idempotency scope.
- Compiler work leases have durable expiry and terminal disposition.
- Canonical commits are ordered by D's per-authority CanonicalCommitCursor.
- Index consumers resume from their own typed watermarks and reject stale generations.
- Context synchronization reconciles against the Context Manager's authoritative version; a gap requires a full snapshot or explicit repair.
- Adapter reconnect reauthenticates and obtains current PermissionEpoch and Forget fence before applying queued context.
- Backup restore starts isolated and replays governance/Forget suppression before exposing restored data.
- Unknown work or missing evidence blocks barrier closure; recovery must not manufacture success.

## 9. Consistency and transaction boundaries

| Operation | Required guarantee | Status |
|---|---|---|
| Event acceptance | Event and processing intent durable before Accepted | DECIDED invariant; transaction implementation TO_VALIDATE |
| Idempotent ingress | Same key/same payload returns same logical receipt; same key/different payload conflicts | Required; exact namespace/retention OPEN pending identity |
| Canonical commit | Canonical revision and CanonicalCommitCursor become visible atomically | Required; Storage implementation TO_VALIDATE |
| Producer admission vs Forget fence | Concurrent operations linearize to included in barrier or rejected/quarantined | OPEN / critical blocker |
| Derived dependency registration vs visibility | No derivative visible before durable lineage registration and final current-fence gate | OPEN / critical blocker |
| Index publication | Derived index state advances with typed per-channel watermark | Required; implementation TO_VALIDATE |
| Context edit | One authoritative ContextVersion sequence with base-version concurrency control | DECIDED invariant; implementation TO_VALIDATE |
| Applied acknowledgement | Applied only for exact ContextVersion at agreed final inference boundary | Required; C/G/H evidence mapping OPEN |
| Global Forget completion | Typed evidence vector over sealed target inventory | I-owned candidate; cross-owner mapping OPEN |

Never use one integer or timestamp as a substitute for unrelated typed cursors, revisions, epochs, and generations.

## 10. Rust implementation architecture

### 10.1 Initial crate map

| Crate | Responsibility |
|---|---|
| brain-domain | Domain types, identifiers, enums, invariants, validation |
| brain-contracts | Internal command/event/query contracts and typed errors |
| brain-storage | SQL migrations, transaction interfaces, canonical persistence, blob metadata |
| brain-ingress | Authenticated ingress, schema validation, idempotent acceptance, outbox |
| brain-compiler | Work orchestration, extraction stages, evidence/provenance, consolidation proposals |
| brain-index | Lexical/vector index adapters, index watermarks, rebuild workers |
| brain-retrieval | Structured/lexical/vector candidate retrieval, filtering and ranking |
| brain-runtime | Activation, scheduling, bounded working sets and cache orchestration |
| brain-context | Context planning, edit operations, versioning and reconciliation |
| brain-protocol | BMCP message types, validation and version negotiation |
| brain-adapter-sdk | Agent-facing integration interfaces and conformance helpers |
| brain-governance | Authorization interfaces, Forget orchestration, retention and audit policy |
| brain-observability | Tracing, metrics, diagnostics adapters |
| brain-app | Application composition, configuration, lifecycle, CLI/service entry points |

This is a candidate crate map. It may be consolidated during implementation; it is not a mandate to create every crate immediately.

### 10.2 Dependency rules

- Domain crates do not depend on concrete database, index, model, or transport implementations.
- Storage adapters implement explicit transaction and repository ports.
- Compiler creates proposals but cannot bypass Canonical Memory authority.
- Index workers consume committed changes and never become authoritative.
- Retrieval applies authorization and Forget suppression before results influence context.
- Context authority is isolated from retrieval and Adapter delivery.
- Protocol types do not redefine B's domain types; use versioned mapping layers.
- Model providers are injected through capability interfaces.
- Governance checks are enforced at every protected boundary, not only at the API gateway.
- Avoid cyclic crate dependencies. Shared contracts belong in small lower-level crates.

### 10.3 Application composition

The brain-app process owns startup/shutdown, configuration, worker supervision, connection pools, transaction coordinators, and health reporting. It wires modules through interfaces. Failure in optional model inference must not prevent storage recovery, read-only diagnostics, or durable ingress where safe.

## 11. Resource budget and capacity model

### 11.1 Planning envelope

Current planning constraint: 12–16 GB GPU VRAM. Host RAM, CPU model/core count, GPU model, storage type, corpus size, Agent concurrency, and model selection are not confirmed. The following are initial allocation envelopes, not guaranteed operating limits or performance claims.

### 11.2 GPU VRAM policy

| Workload | 12 GB VRAM planning envelope | 16 GB VRAM planning envelope | Policy |
|---|---:|---:|---|
| Driver/runtime/display and safety headroom | 1.5–2.0 GB | 1.5–2.0 GB | Reserve; do not allocate to model weights |
| Generative LLM weights | 6.5–7.5 GB | 8.5–10.5 GB | Depends on architecture and quantization |
| KV cache / active context | 1.5–2.0 GB | 2.0–3.0 GB | Enforce context and concurrency caps |
| Embedding/reranker transient allocation | 0–1.0 GB | 0–1.5 GB | Prefer CPU or sequential GPU scheduling initially |
| Remaining fragmentation margin | Remaining capacity | Remaining capacity | Do not plan for 100% utilization |

These ranges are planning assumptions only. Actual use must be measured with the selected model, context length, batch size, quantization, GPU backend, and driver.

GPU scheduling requirements:

- One primary large generative model at a time by default.
- Bounded inference queue and explicit admission control.
- Separate priority classes for interactive requests and background compilation.
- Background summarization/embedding yields to interactive inference where policy allows.
- Model unload/reload and OOM recovery must not corrupt accepted Events or canonical state.
- Record peak/steady VRAM, load time, token throughput, and tail latency.

### 11.3 Host RAM

GPU VRAM is not host RAM. Provisional host-RAM profiles to benchmark:

| Host RAM tier | Intended profile |
|---|---|
| 16 GB | Minimal functional test; small corpus, low concurrency, model inference constrained or external |
| 32 GB | Preferred initial local development/acceptance target with one local inference workload and moderate indexes |
| 64 GB or more | Larger corpus, larger indexes, more concurrent sessions, or more aggressive local model workloads |

Indicative process budgets, not hard allocations:

- Brain core, protocol, governance and storage connections: 0.5–1.5 GB resident target.
- Compiler deterministic workers and queues: 0.5–1.5 GB with bounded payload staging.
- Retrieval, lexical/vector indexes and cache: 1–4 GB depending on corpus and index design.
- Inference worker host-side memory: model/backend dependent; may be several GB or more.
- OS, filesystem cache, Agent runtime and safety headroom: reserve explicitly.

Expose memory pressure and apply backpressure before uncontrolled swapping or OOM termination.

### 11.4 CPU and concurrency

- Keep interactive Recall, durable ingress, background compilation, index rebuild, and model inference in distinct scheduling classes.
- Bound worker counts and queue sizes by workload class.
- Avoid CPU oversubscription between Tokio tasks, ANN/search threads, tokenization, and inference backends.
- CPU-heavy inference must not block Tokio executor threads; use dedicated blocking pools or external worker processes.
- Benchmark on actual target CPU; no fixed core count or throughput claim is approved.

### 11.5 Disk and I/O

Disk budget derives from raw source retention, canonical revisions and provenance, event/outbox retention, index duplication, WAL growth, backup generations, restore staging, model files, and audit retention.

Required controls: disk quota, low-space alarms, WAL checkpoint policy, orphan-blob scanner, index rebuild space reservation, backup integrity checks, and safe behavior when disk is full. Disk-full must not result in an Accepted receipt without durable commit.

### 11.6 Initial workload classes

The first benchmark suite must define small/medium/large corpora and concurrency profiles.

Dimensions include Event count and payload sizes; Memory/Claim/Entity/Relation/Evidence counts; blob distribution; scopes/environments/Agents/sessions; lexical/vector index size; read/write ratio and bursts; compiler model-on/model-off mix; Forget fan-out; and online/offline Adapter distribution.

## 12. Performance objectives and benchmark plan

Quantitative SLOs remain OPEN until representative workload and hardware are declared.

Required measurements:

- Ingress durable acceptance p50/p95/p99 and write-contention rate.
- Compiler queue age, stage latency, retry count, and time-to-canonical.
- Recall end-to-end and per-channel p50/p95/p99.
- Retrieval precision/recall and provenance correctness.
- Activation precision, false activation, and missed relevant memory.
- Context plan/edit/commit latency and version-conflict rate.
- Delivery latency, Applied lag, retries, and snapshot fallback rate.
- Forget time-to-suppression, barrier completion, per-target cleanup, and global completion duration.
- CPU, RSS, peak/steady VRAM, disk IO, database/WAL size, index size, and queue depth.
- Agent-task success and error rates against no-memory and simple-retrieval baselines.

Every benchmark report includes hardware, OS, software commit, configuration, model/quantization, corpus, query mix, scope distribution, concurrency, cache state, warmup, sample count, percentiles, and correctness dataset.

Do not publish performance multipliers or SLOs without reproducible evidence.

## 13. Failure isolation and operational behavior

| Failure | Required behavior |
|---|---|
| Model unavailable/OOM | Durable ingress and canonical reads continue where safe; Compiler work remains retryable |
| Database unavailable | No Accepted/canonical success acknowledgement; expose degraded health |
| Blob write interrupted | No visible reference to incomplete blob; recovery detects incomplete/orphan artifacts |
| Index unavailable/behind | Safe fallback or explicit degraded result; no stale/forgotten content leakage |
| Cache inconsistency | Bypass/invalidate cache and re-check authoritative policy/fence |
| Compiler worker crash | Durable lease/work state recovers; no work disappears from Forget barrier |
| Adapter offline | Delivery remains pending/unknown; do not mark Applied or Clear |
| Forget fence advanced | Old work/replay/publication rejected or quarantined |
| Disk full | Apply backpressure; preserve durable correctness; no false acceptance |
| Backup restore | Restore isolated; apply current Forget/revocation state before serving |
| Telemetry gap/out-of-order | Mark uncertainty/gap; do not promote inferred outcomes to verified facts |

Operational tooling required before implementation acceptance:
- database migration and schema inspection;
- health and diagnostics CLI;
- backup and restore verification;
- index rebuild and watermark inspection;
- replay and dead-letter inspection;
- Forget target and evidence inspection;
- redacted trace export;
- configuration validation and resource limits.

## 14. Technology decision register

| ID | Decision | Initial recommendation | Status | Required closure evidence |
|---|---|---|---|---|
| TEC-001 | Core language | Rust | DECIDED direction | Existing architecture baseline |
| TEC-002 | Async runtime | Tokio | RECOMMENDED | Runtime prototype and dependency review |
| TEC-003 | Primary transactional store | SQLite + WAL for single-node prototype | CANDIDATE / TO_VALIDATE | D/E Forget race tests, transaction/recovery tests, concurrency benchmark |
| TEC-004 | Multi-writer/remote database | PostgreSQL evolution path | CANDIDATE | Workload threshold and migration comparison |
| TEC-005 | Blob storage | Content-addressed local filesystem plus metadata | RECOMMENDED | Crash consistency, integrity, backup/restore tests |
| TEC-006 | Full-text index | FTS5 first; Tantivy comparison | CANDIDATE | Recall quality, indexing throughput, update/delete and rebuild benchmarks |
| TEC-007 | Vector index | Embedded ANN (e.g. usearch) versus sqlite-vec | OPEN | Recall/latency/memory/update/delete/rebuild evaluation |
| TEC-008 | Cache | Moka in-process | RECOMMENDED | Generation invalidation, concurrency and memory-bound tests |
| TEC-009 | Embedding inference | ONNX Runtime where compatible artifacts exist | CANDIDATE | Model compatibility and CPU/GPU benchmark |
| TEC-010 | Local generative inference | llama.cpp-compatible backend | CANDIDATE | Target GPU model/context/VRAM and latency benchmark |
| TEC-011 | Model abstraction | Capability-based provider interfaces | RECOMMENDED architecture | Contract and provider conformance tests |
| TEC-012 | Protocol encoding | JSON initial candidate; binary alternative retained | OPEN / H-owned | H schema, compatibility and payload benchmark |
| TEC-013 | Transport | HTTP/local IPC adapter abstraction | OPEN / H-owned | Security, streaming, reconnect and cross-platform tests |
| TEC-014 | Observability | tracing + metrics facade; OpenTelemetry/Prometheus exporters | RECOMMENDED | Correlation and sensitive-data review |
| TEC-015 | Secrets/crypto | OS key store where available; vetted crypto libraries | OPEN / I-owned | Threat model, key lifecycle, platform matrix |
| TEC-016 | Deployment | Local modular monolith + optional inference worker | CANDIDATE | Fault isolation and resource benchmark |
| TEC-017 | Schema migration | Versioned SQL migrations and compatibility checks | RECOMMENDED | Upgrade/downgrade/restore tests |
| TEC-018 | Queue/outbox | Transactional outbox + durable DB-backed workers initially | CANDIDATE | Admission/fence linearization and replay/fault tests |

## 15. Required ADRs and prototypes

Create the following ADRs under 13-engineering-decisions after owner review:

1. ADR-TEC-001 — Primary transactional database and transaction model.
2. ADR-TEC-002 — Canonical persistence, event/outbox, and blob storage layout.
3. ADR-TEC-003 — Lexical search engine selection.
4. ADR-TEC-004 — Vector index and hybrid retrieval architecture.
5. ADR-TEC-005 — Embedding and reranker inference backend.
6. ADR-TEC-006 — Local generative inference backend and GPU scheduling.
7. ADR-TEC-007 — BMCP encoding, transport, and schema compatibility.
8. ADR-TEC-008 — Observability, audit, and diagnostics stack.
9. ADR-TEC-009 — Local deployment, process boundaries, and upgrade model.
10. ADR-TEC-010 — Backup, restore, encryption, and key management.

Mandatory prototypes before relevant ADR approval:

- SQLite/PostgreSQL transaction and contention comparison.
- D/E producer admission versus Forget fence race prototype.
- Durable outbox, lease expiry, crash recovery, replay, and DLQ prototype.
- Canonical cursor atomicity and crash recovery test.
- FTS5/Tantivy lexical benchmark.
- Vector ANN recall/latency/memory/update/delete/rebuild benchmark.
- Embedding and LLM VRAM/context benchmark on target GPU.
- Adapter final-request Applied and reconnect conformance prototype.
- Backup restore with Forget/revocation replay test.

## 16. Implementation sequence and gates

### Gate T0 — Architecture reconciliation

- A registers this blueprint and links it to system architecture.
- B/C/D/E/F/G/H/I review technology constraints affecting their ownership.
- No domain contract is changed by this document.
- Open cross-module blockers remain visible.

### Gate T1 — Storage and consistency spike

- Implement a narrow transaction prototype.
- Prove durable Event + outbox acceptance.
- Prove canonical commit cursor atomicity.
- Resolve producer admission/fence installation/publication linearization with D/E/Storage.
- Exercise crash, retry, lease, and replay cases.

No Forget implementation sign-off before required race tests pass.

### Gate T2 — Retrieval and model spike

- Compare FTS5 and Tantivy.
- Compare at least two vector index candidates.
- Measure embedding and optional reranking on CPU/GPU.
- Define corpus and labeled retrieval evaluation set.

### Gate T3 — Agent/Context/Protocol spike

- Validate BMCP capability negotiation.
- Prove final-request Applied evidence at Tier 1.
- Test version gaps, offline reconnect, stale Delivery, and Forget invalidation.
- Test untrusted-memory prompt injection boundaries.

### Gate T4 — Local deployment and recovery

- Verify clean install, migration, backup, restore, index rebuild, and upgrade.
- Verify GPU worker failure does not corrupt or block durable core state.
- Verify disk-full and process-crash behavior.
- Establish measured resource budgets and initial SLOs.

### Gate T5 — Technology baseline approval

Only after ADRs and prototype evidence are reviewed may A record the selected stack as DECIDED. Unselected options remain documented as alternatives. Implementation proceeds in vertical slices against approved contracts.

## 17. Open questions

1. Exact host RAM, CPU, GPU model, storage type, OS, and target corpus are not specified in the current baseline.
2. Expected number of concurrent Agent instances and write-producing sessions is not fixed.
3. Single-user local versus multi-user local deployment scope needs explicit confirmation.
4. B Fact/Claim ADR and typed ActorRef/ScopeRef semantics remain unresolved.
5. D/E/Storage atomic producer admission, Forget fence, and publication gate remain open.
6. H/C/G final-request Applied attestation and Adapter capability mapping remain open.
7. I global Forget target evidence mapping with D/E/F/G/H remains open.
8. Exact encryption/key custody and backup threat model remain I-owned decisions.
9. Quantitative latency, throughput, recall quality, RTO/RPO, and capacity targets remain TO_VALIDATE.
10. Whether vector search is needed in the first vertical slice must be decided from retrieval evaluation, not assumption.

## 18. Acceptance checklist

- [ ] Technology layers are mapped to A–I without changing ownership.
- [ ] Deployment topology distinguishes logical components from processes.
- [ ] Durable data, derived indexes, cache, and blobs have explicit authority boundaries.
- [ ] Ingestion, Recall, Context, Forget, and Recovery data flows are described.
- [ ] Model inference is optional, replaceable, isolated, and resource-bounded.
- [ ] 12–16 GB VRAM planning ranges and unknown host-resource assumptions are explicit.
- [ ] Database, lexical, vector, model, protocol, and deployment options have status and closure evidence.
- [ ] D/E/Storage atomicity and other open contracts remain OPEN.
- [ ] No performance or security claim is presented without evidence.
- [ ] Required ADRs, prototypes, and implementation gates are listed.

**Current conclusion:** The project has a coherent candidate technology architecture for a local-first Rust implementation. The first recommended implementation shape is a modular monolith, transactional local store, content-addressed blob storage, rebuildable lexical/vector indexes, bounded in-process caches, and an optional isolated model worker. The concrete database, index, inference backend, wire encoding, cryptography, and quantitative resource limits are not frozen until owner review and reproducible validation.
