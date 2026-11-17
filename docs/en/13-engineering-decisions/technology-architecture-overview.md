# AI Memory Brain — Technology Architecture Overview

- Document ID: DOC-TEC-001
- Version: 1.0
- Chinese counterpart: [技术架构总览](../../zh-CN/13-engineering-decisions/technology-architecture-overview.md)
- Basis: TAB-001 v0.1 and the TAR-AI-001 final system technology architecture review
- Status: Technology guide; candidate options are not a technology freeze

## 1. What the technology architecture must answer

The logical architecture explains what the system contains and who owns each responsibility. The technology architecture additionally answers: which technologies implement those responsibilities, how components communicate, which state transitions share a transaction, how the system is deployed and recovered, and how it operates within local CPU, RAM, SSD, and 12–16 GB VRAM constraints.

Technology choices must serve correctness, recoverability, and maintainability—not technology fashion.

## 2. Current recommended first-release shape

**A modular Rust monolith with explicit internal interfaces, local persistence, and an optional isolated inference process.**

- Keep logical modules clear without prematurely splitting them into microservices.
- Keep correctness-critical state changes within explicit transaction boundaries wherever practical.
- Run model inference in an optional separate process so model loading, GPU OOM, or inference stalls cannot block durable event acceptance and recovery.
- Integrate Agent Adapters inside an Agent or through a Sidecar/local Gateway.
- Treat indexes and caches as derived data, never as authoritative memory.

This is a first-release engineering candidate, not production deployment approval.

## 3. Technology layers

| Technology layer | Responsibility | Main constraints |
|---|---|---|
| Agent Adapter / BMCP | Telemetry ingress, context delivery, ACK, capability negotiation | Authentication, version compatibility, final inference-boundary evidence |
| Ingress / Compiler | Durable acceptance, extraction, normalization, evidence, derivative production | Idempotency, retries, work recovery, Forget publication gate |
| Canonical Memory | Authoritative memories, versions, lifecycle | Transaction consistency, history, forgetting barrier |
| Runtime / Retrieval | Retrieval, ranking, activation, working sets | Scope-first filtering, index watermarks, anti-resurrection |
| Memory Context | Context planning, editing, versioning, delivery | CAS, Delivery state, Applied proof |
| Governance | Identity, permission, retention, Forget, audit | Cross-module enforcement and verifiable evidence |
| Storage / Index / Cache | Persistence, search indexes, cache | Authority/derived-data separation, recoverable rebuild |
| Inference Provider | Embedding, extraction, reranking, optional generation | Resource isolation, replaceable models, budget controls |

## 4. Candidate technologies and current status

| Area | Candidates | Current status | What must be validated |
|---|---|---|---|
| Core language | Rust | Project direction decided | Crate boundaries, dependency governance, compile/integration cost |
| Async runtime | Tokio | Recommended candidate | Bounded tasks, backpressure, CPU-heavy task isolation |
| Transactional database | SQLite WAL / PostgreSQL | No final decision | Transactions, concurrency, crash recovery, Forget atomicity under the same workload |
| Blob storage | Content-addressed filesystem | Recommended direction | DB/blob consistency, orphan cleanup, encryption, backup and restore |
| Full-text search | FTS5 / Tantivy | Comparison required | Index cost, query latency, updates, and rebuild on the same corpus |
| Vector retrieval | usearch / sqlite-vec, etc. | OPEN | Recall, filtering, memory, updates/deletes, and rebuild |
| Cache | Moka / no cache / Redis | Candidate | Invalidation, permission isolation, Forget anti-resurrection, memory limits |
| Task execution | Transactional Outbox + bounded Tokio workers | First-release candidate | Leases, retries, DLQ, replay, idempotency, crash recovery |
| Model inference | ONNX Runtime, GGUF/llama.cpp, etc. | Candidate | Target-hardware latency, VRAM, quantization, model version, fallback |
| Protocol encoding | Serde, JSON/JCS, CBOR, etc. | OPEN | Canonical bytes, signatures, cross-language compatibility, strict parsing |
| Transport | HTTP, Unix Socket, Named Pipe, gRPC | OPEN | Authentication, reconnect, portability, latency, observability |
| Key management | OS Key Store, envelope encryption, etc. | OPEN | Rotation, recovery, backup, cryptographic erasure |

A technology does not become an approved selection merely because it appears in TAB-001.

## 5. Why the database cannot be selected by preference alone

The database may carry Canonical Memory, versions, Events, Accepted Receipts, Idempotency records, Producer Registrations, Forget Fences, Dependency Registrations, Outbox, recovery checkpoints, Context, Delivery, and governance records—not merely memory text.

SQLite WAL offers simple local deployment and low operational overhead; its constraints include its single-writer model and write contention. PostgreSQL offers stronger concurrent transaction and operational capabilities but requires a separate service and additional deployment and backup management.

Compare both using the same representative workloads and consistency tests—not preference.

## 6. Correctness-first data flow

~~~text
Event + Idempotency + Accepted Receipt
                ↓
        Durable Compiler Work
                ↓
       Candidate / Derivative
                ↓
  D Authority + Storage Publish Gate
                ↓
       Canonical Commit + Cursor
                ↓
       Index / Runtime Visibility
~~~

The Forget workflow must remain safe when it races with producer work:

~~~text
Producer Admission ─────┐
                        ├─ Shared linearization boundary
Forget Fence Install ───┘
                        ↓
Dependency Registration
                        ↓
Final Publication Gate
                        ↓
Visible or Suppressed
~~~

**A two-step “read the Fence, then separately write the derivative” check is not atomic.** A concrete transaction or equivalent linearization mechanism is required, followed by concurrency-race and crash-injection tests.

## 7. Deployment and resource-budget principles

The current planning envelope is 12–16 GB VRAM. This is not a completed capacity test.

- Persistence, governance, and core state machines must operate without GPU inference.
- Embedding, reranking, and generation models must be independently startable, stoppable, rate-limited, and degradable.
- Measure model weights, KV cache, context length, batch size, concurrency, and VRAM fragmentation separately.
- CPU, RAM, SSD IOPS, index build time, and recovery time are also part of the budget.
- Declare hardware, model version, quantization, corpus size, concurrency, and measurement method.

Without reproducible measurements, results must be labelled estimates or validation items—not measured performance.

## 8. Current technology review conclusion

The TAR-AI-001 final system verdict is **BLOCKED**. TAB-001 remains CANDIDATE, not approved and not frozen.

Key blockers:
1. Fact/Claim ADR is not approved; dependent schemas and interfaces cannot be frozen.
2. D/E/Storage producer admission, Forget Fence, dependency registration, and publication atomicity lack application-level implementation evidence.
3. JF-10 / COC same-XID recovery and real participant integration remain open.
4. Global Forget target mapping, acknowledgement, and completion evidence require end-to-end closure.
5. C/G/H final inference-request Applied proof requires a real Adapter integration.
6. F index, cache, and rebuild anti-resurrection require runtime fault tests.
7. Representative workload, resource, and P95/P99 benchmarks are not complete.

## 9. Recommended validation order

1. Resolve the Fact/Claim ADR.
2. Build D/E/Storage/COC/I atomic publication and recovery integration tests.
3. Close the Global Forget target inventory and evidence vector.
4. Implement and validate C/G/H final-request Applied proof.
5. Validate F's real index, cache, and anti-resurrection behavior.
6. Once correctness contracts stabilize, compare database, full-text index, vector index, and inference backends.
7. Run representative workloads and resource tests on the 12–16 GB VRAM target.

---
**Chinese counterpart:** [AI Memory Brain 技术架构总览](../../zh-CN/13-engineering-decisions/technology-architecture-overview.md)
