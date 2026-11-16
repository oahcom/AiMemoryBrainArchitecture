# Final System Technology Architecture Review — TAR-AI-001

- Document ID: TAR-AI-001-A-FINAL
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Reviewing role: A — Principal Integration Architect
- Review date: 2026-11-17
- Blueprint reviewed: TAB-001 v0.1
- Review branch: `session-a-integration-2026-11-16`
- Review mode: branch-aware static architecture and evidence review; no implementation, fault-injection, security, or performance tests executed by this review.
- **Final verdict: NOT REVIEWABLE**
- **TAB-001 disposition: NOT APPROVED; retain CANDIDATE / NOT A TECHNOLOGY FREEZE.**

## 1. Executive Summary

The proposed system direction is coherent enough to continue controlled engineering: a modular Rust monolith, explicit ports/adapters, a transactional local persistence authority, rebuildable indexes, optional isolated inference, and capability-tiered Agent adapters. The separation of Canonical Memory, Memory Context, and Applied Context is sound. The candidate architecture correctly treats inference as optional to durable ingestion and treats indexes/caches as derived state.

This is not a final approval. Only four of the eight required owner technology reports (C, F, G, H) were found and content-read on their owner branches. Four required reports (B, I, D, E) were absent from the corresponding branch trees. Their existing domain/owner artifacts are useful inputs but are explicitly not substitutes for TAR-AI-001 owner reviews. The A branch has no prior final technology review artifact.

There are unresolved P0/P1 governance and cross-module issues: B Fact/Claim ADR is blocked; D/E/Storage producer admission/fence/dependency/publication linearization is not proven; H/I/C identity and permission binding is not freeze-ready; C/G/H Applied proof lacks final-request runtime evidence; I global Forget mapping remains open; F anti-resurrection requires fault tests. Phase 3 itself says implementation, fault-injection and security tests were not run. All performance and resource claims remain NOT BENCHMARKED.

Accordingly, the evidence is insufficient to determine that the whole architecture is internally consistent, implementable, deployable and recoverable. NOT REVIEWABLE is selected rather than CONDITIONAL PASS because the mandatory eight-report evidence gate is unmet. This is an evidence verdict, not a finding that the architecture direction is intrinsically unsound.

## 2. Eight Owner Review Verification

### 2.1 Branch HEAD snapshot

The following branch HEADs were refreshed through GitHub branch endpoints during this review:

| Owner | Branch | Observed HEAD |
|---|---|---|
| A | session-a-integration-2026-11-16 | fb061aee907c28f7da198e68161ff57ebac160b7 |
| B | session-b-domain-model-phase3 | 861fa9b2c3e1f572336543b15c7dc392493891db |
| C | session-c-agent-integration-2026-11-16 | 2e5776029bc4271c33525f04c7d0f0708e4bbae8 |
| D | session-d-memory-brain-2026-11-16 | 9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8 |
| E | session-e-memory-compiler-2026-11-16 | 4402549c39824b89a0dc49973226187c62e056c5 |
| F | session-f-memory-runtime | 714fe628fdcfe62b5e6ea901810b779c58ddddb3 |
| G | session-g-memory-context | 72a8066b4401f9586fe10775d545384b82736f07 |
| H | session-h-bmcp-protocol | 242d8ab5da890181e762561bb3d3a662287fb63c |
| I | session-i-security-governance-2026-11-16 | 1fc3b3293ebf2077edfd6ad253647d382173d9fa |
| Storage/Consistency | session-storage-consistency-forget-atomicity-2026-11-16 | e803f7d79d4ec747272299113d8222c60c3be8e9 |

These are the observed branch heads for this audit snapshot; they are not assertions that all report contents were authored at those exact heads. Branches may advance after the snapshot.

### 2.2 Report verification

| Owner | Required report | Result | Evidence / disposition |
|---|---|---|---|
| B | Owner B technology review | MISSING | No TAR-AI-001 report found in B branch tree. Existing Fact/Claim ADR remains ADR-BLOCKED. No acceptance inferred. |
| I | Owner I technology review | MISSING | No TAR-AI-001 report found in I branch tree. Existing governance/Forget artifacts are inputs only. No acceptance inferred. |
| D | Owner D technology review | MISSING | No TAR-AI-001 report found in D branch tree. Existing Forget/fence and Phase 3.6 artifacts are not a technology review. |
| E | Owner E technology review | MISSING | No TAR-AI-001 report found in E branch tree. Existing producer-admission and derived-registration artifacts are not a technology review. |
| F | `reviews/technology/owner-f-memory-runtime-technology-review.md` | VERIFIED / CONDITIONAL PASS | Blob `8437b5bbf676361feb2f4e62c21d9d8495f6e619`; branch HEAD above. Static review; no runtime/fault/security/performance tests. |
| G | `reviews/technology/owner-g-memory-context-technology-review.md` | VERIFIED / CONDITIONAL PASS | Blob `6211845c21f40a8c4a51d450330dd1750e76e50b`; branch HEAD above. Static review; no runtime/fault/security/performance tests. |
| H | `reviews/technology/owner-h-bmcp-technology-review.md` | VERIFIED / CONDITIONAL PASS | Blob `0f158555f1870c5a41273a41d35e2b05a7b39283`; branch HEAD above. Static review; no protocol/crypto/SDK/fault/performance tests. |
| C | `reviews/technology/owner-c-agent-integration-technology-review.md` | VERIFIED / CONDITIONAL PASS | Blob `799aa6e533d10240ed8f6050e15f56e6646c0327`; branch HEAD above. Static review; no framework integration/runtime/security/performance tests. |

F/G/H/C report contents were read. B/I/D/E branch trees were inspected and their missing report status confirmed. The exact blobs of relevant non-review artifacts are listed in Section 17. This report does not claim that every file in every branch was exhaustively read.

### 2.3 Owner-level assessment

- **B — NOT REVIEWABLE:** Fact/Claim semantics remain ADR-BLOCKED. No technology review; dependent schema/index/wire fields must not be frozen.
- **I — NOT REVIEWABLE:** no technology review. PermissionEpoch baseline exists, but exact external governance profile, global Forget target inventory/completion semantics, backup and external-copy handling require owner decision and evidence.
- **D — NOT REVIEWABLE:** no technology review. D owns canonical Forget/fence semantics; the D/E/Storage atomic publication race remains open.
- **E — NOT REVIEWABLE:** no technology review. Accepted receipt/idempotency and compiler pipeline require reconciliation with D's cursor and Storage's linearization contract.
- **F — CONDITIONAL PASS:** structured + lexical prototype may proceed; index technology, cursor mapping, authorization-before-candidate, anti-resurrection and cache budgets remain open.
- **G — CONDITIONAL PASS:** Context head/ChangeSet/outbox prototype may proceed; durable CAS/recovery, Applied verifier, delivery/Forget invalidation and compaction fidelity remain open.
- **H — CONDITIONAL PASS:** JSON/JCS, HTTP and local IPC prototypes may proceed; identity binding, ACK/Applied proof, Forget-to-global-target mapping and transport/encoding selection remain open.
- **C — CONDITIONAL PASS:** capability-tiered adapter strategy is coherent; Tier 1 Full Applied requires a real final-submit hook and request-bound evidence. Framework compatibility and security tests have not run.

## 3. System Architecture Assessment

### 3.1 Logical layers and authority

| Layer | Authority / responsibility | Assessment |
|---|---|---|
| Agent Adapter / telemetry | Capture host events and deliver governed context; cannot mint canonical truth or claim Full Applied without final-submit proof | Directionally sound; C implementation hooks unverified |
| BMCP | Versioned transport, envelope, negotiation, delivery and evidence carriage | Boundary sound; exact schemas and identity binding open |
| Ingress / Event acceptance | Durable acceptance receipt and idempotency before acknowledgement | Required; E/Storage implementation proof absent |
| Memory Compiler | Normalize/extract proposals, provenance and dependencies; no autonomous canonical authority | Directionally sound; atomic publication boundary open |
| Memory Brain / Canonical Memory | Canonical lifecycle, revisions, global per-authority commit cursor and Forget authority | Clear authority; B Fact/Claim decision blocks schema freeze |
| Runtime retrieval / activation | Authorized candidate retrieval, ranking, activation recommendation and working sets | Sound separation; F pre-candidate filtering and channel completeness untested |
| Memory Context | Immutable Context versions, ChangeSets, delivery intent and attempt history | Sound separation; durable transaction and recovery unproven |
| Security & Governance | Principal, policy, permission epoch, global Forget targets, retention and audit | Correct cross-cutting placement; I report missing |
| Persistence / Index / Cache | Transactional source of truth plus rebuildable derived data | Correct conceptual split; backend selection and race guarantees not proven |
| Inference | Optional provider/local model boundary; output is proposal, not canonical truth | Correctly isolated in principle; VRAM and latency unmeasured |

No inherent circular dependency is required if the ownership rules are enforced: Brain owns canonical facts/lifecycle; Compiler proposes and publishes only through Brain/Storage gates; Runtime consumes canonical state and derived indexes; Context owns its own version history; Adapter reports evidence; H transports; I authorizes and coordinates global governance. The unresolved contracts currently prevent declaring these boundaries fully implementable.

### 3.2 Deployment topology

Recommended prototype topology, not approved production topology:

1. One local Rust host process / modular monolith for correctness-critical state transitions.
2. One transactional database authority, initially evaluating SQLite WAL against PostgreSQL.
3. Content-addressed blob storage coordinated with database metadata and backup.
4. Separate rebuildable lexical/vector index generations.
5. Bounded in-process caches and working sets, always subordinate to current authorization and Forget fences.
6. Optional isolated inference worker; inference failure must not block durable event acceptance or canonical recovery.
7. Agent-side embedded SDK or sidecar depending on host runtime capability; remote gateway only with explicit identity, transport and residency policy.
8. Explicit migration, backup, restore, observability and fault-injection tooling.

Do not equate logical modules with separate services. Distributed queues, Kafka, Kubernetes and hosted vector services are not justified for the first local-first deployment without measured need.

## 4. Technology Selection Matrix

All entries below are candidate/recommendation states, not final approvals.

| Concern | Preferred prototype / candidates | Alternatives | Trade-offs, resource and recovery implications | Status / ADR / validation |
|---|---|---|---|---|
| Core language/runtime | Rust + Tokio | Go, JVM, Python orchestration | Rust type/ownership model suits state machines; Tokio ecosystem mature. CPU/RAM depends on concurrency; async task bounds required. | Rust direction DECIDED; Tokio RECOMMENDED. Prototype async supervision and crash recovery. |
| Primary DB / transactions | SQLite WAL | PostgreSQL; embedded KV/RocksDB | SQLite lowest ops and local footprint, single-writer contention; PostgreSQL better concurrent writers and service operations but adds RAM/admin; KV requires app-built transactional semantics. DB/blob consistency and WAL recovery are critical. | SQLite first prototype only; ADR required. Benchmark concurrency, fsync, WAL growth, backup/restore and crash semantics. |
| Blob storage | Content-addressed filesystem + DB metadata | DB large-object storage; object store | Filesystem avoids bloating DB but creates cross-resource publication/backup problem; object store adds service dependency. Disk and hashing cost proportional to payload. | RECOMMENDED direction; ADR/restore prototype required. |
| Structured search | SQL indexes | Dedicated search engine | Best filter locality and authorization control; query planning/index size need workload tests. | RECOMMENDED; prototype. |
| Full-text | SQLite FTS5 | Tantivy | FTS5 colocated/simple; Tantivy gives Rust-native control/scale but adds index lifecycle and recovery. | FTS5 first comparison, not freeze; ADR-F-001; benchmark identical corpus. |
| Vector ANN | usearch/HNSW, sqlite-vec or equivalent | Tantivy vector capability, remote vector DB | ANN adds RAM, build/update/delete and filtering complexity; CPU and memory depend on corpus/dimensions. | CANDIDATE; ADR-F-002; defer until embeddings/corpus stable and filtered recall measured. |
| Cache | Moka / bounded in-process cache | Redis or no cache | In-process low ops; invalidation and epoch/fence key completeness critical. Redis adds process/network and another recovery domain. | CANDIDATE; ADR-F-004; race and budget tests. |
| Queue / scheduling | Transactional outbox + bounded Tokio workers | SQLite queue, PostgreSQL queue, NATS, Kafka | Outbox avoids dual-write but requires lease/retry/DLQ semantics. External broker adds ops and replay complexity. | Outbox-first RECOMMENDED; ADR after workload. Test replay, duplicate, poison and backlog. |
| Compiler | Rust pipeline / bounded workers | External worker service | Local workers reduce operational complexity; CPU/RAM bursts and model dependency must be isolated. | Architecture direction; E review missing; benchmark peak memory/backpressure. |
| Embeddings | ModelProvider abstraction; local embedding worker optional | Remote API, CPU embedding, no vector in first slice | Local model costs VRAM/RAM and loading time; remote adds latency/privacy/availability; CPU costs latency. | CANDIDATE; ADR required for model, dimension, versioning and retention. Benchmark quality/latency and 12/16GB profiles. |
| Local inference | Isolated worker, llama.cpp/Ollama-class backends as candidates | Remote provider; CPU offload | Isolation protects durable path; GPU memory contention, quantization, model context and concurrent sessions matter. | TO_VALIDATE; no backend/model approved. Measure VRAM/RAM and OOM recovery. |
| Protocol encoding | JSON + RFC 8785 JCS | CBOR, MessagePack, Protobuf | JSON debuggable and cross-language; canonicalization/signature strictness needed. Binary can reduce bytes but adds profile/tooling complexity. | H recommends prototype only; ADR-H-001; golden vectors/fuzz/interoperability. |
| Transport | HTTP(S) remote; Unix socket / Windows named pipe local | Loopback TCP, gRPC | HTTP broad compatibility; IPC low hop overhead but peer identity/platform parity; gRPC adds streaming/schema runtime. | Candidate; ADR-H-002; auth/reconnect/latency tests. |
| Agent adapter | Sidecar candidate; embedded SDK for trusted final-submit hook | Remote gateway; event/tool-only integration | Sidecar isolates credentials/queues but adds IPC/supervision; embedded lowers latency but shares crash domain; gateway cannot infer hidden final request. | C recommends capability tiers; no default frozen. Framework matrix and hook prototype. |
| Identity/auth | I-issued authenticated principal and policy binding | mTLS, OS peer credentials, signed tokens as mechanisms | Transport proof must bind payload claims; stale epochs fail closed. Key custody/rotation and issuer mapping unresolved. | OPEN; joint B/I/H/C contract and security ADR/tests. |
| Encryption/key management | OS key store / platform secret manager; envelope encryption candidates | KMS/HSM, encrypted volume | Local-first OS store simpler; portability and recovery/key loss risks. | OPEN; I-owned decision and key rotation/restore tests. |
| Backup/restore | Coordinated DB + blob + index rebuild + Forget policy | DB-only snapshot, filesystem snapshot | DB-only is incomplete when blobs referenced; restore can resurrect forgotten content unless fences/tombstones and external-copy policy replay. | OPEN; I/D/Storage ADR and restore/anti-resurrection test. |
| Deployment isolation | Modular monolith + optional inference worker + adapter sidecar | Microservices/Kubernetes | Minimal first-release operations; process isolation only where resource/security boundaries justify. | RECOMMENDED topology, not frozen; prototype crash containment and upgrade compatibility. |

## 5. Cross-Module Dependency Matrix

| Provider → Consumer | Contract | Current state | Required closure |
|---|---|---|---|
| B → D/E/F/H/I | Fact/Claim, ActorRef, ScopeRef, typed references | ADR-BLOCKED / OPEN | Approve B ADR; synchronize schema and golden vectors |
| I → H/C/E/F/G | Principal, issuer/delegation, Scope permission, PermissionEpoch | Directionally aligned, exact mapping open | Joint typed binding, revocation and forged-identity tests |
| D → E/Storage | Canonical cursor, Forget fence, producer barrier | Semantics advanced; atomic implementation open | Linearizable admission/fence/dependency/publish operation and race proof |
| E → D/Storage/F | Accepted receipt, idempotency, staged derivative and outbox | Owner report missing; publication gate open | Durable acceptance, same-key/different-payload conflict, replay and visibility contract |
| D/E → F | Canonical feed, typed cursor and Forget suppression | OPEN | Cursor mapping, index watermark vector, late publish and rebuild tests |
| F → G | Retrieval result, completeness and per-channel watermark | Directionally aligned | No F claim of Context sufficiency; gap and stale-index behavior |
| G → H/C | ContextVersion, ChangeSet, Delivery, Applied acceptance | Conditional | Exact request/attempt binding and durable delivery ledger |
| C ↔ H | Final immutable inference request, attestation, capability tier | Conceptually aligned | Real runtime hook, request ID and independently verifiable submission evidence |
| D/I → G/H/C/F | Local fence + global target inventory and revocation | OPEN | I global mapping; offline Adapter, cache, index, Context and backup targets |
| Storage → all | Transaction boundaries, outbox, restore, migrations | Not demonstrated | Storage conformance suite and failure evidence |

## 6. Data Flow & Control Flow Assessment

### 6.1 Event Ingress → Compiler → Canonical Memory

Expected boundary: Event Accepted only after durable receipt/idempotency and recoverable work intent. Compiler outputs are proposals with provenance, not canonical truth. Canonical commit and its per-authority CanonicalCommitCursor update must be atomic. Acknowledgement, compile completion and canonical commit are distinct.

Status: design direction is coherent; E technology review missing; storage transaction and outbox implementation evidence absent. Same idempotency key/same payload must return the same logical acceptance; same key/different payload must conflict. Crash-before/after-ACK and DLQ replay tests required.

### 6.2 Canonical Memory → Index → Runtime Retrieval

Canonical store remains authority. IndexWatermark is a per-channel/per-partition vector and cannot be substituted for CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor or ForgetFenceGeneration. Scope/Permission must be enforced before unauthorized candidates can affect ranking, summaries or context. Behind-fence or stale indexes fail closed or suppress.

Status: F architecture is conditionally acceptable; FTS5/Tantivy/ANN unselected. Pre-candidate authorization, index gap/replay, deterministic rebuild and late-publication suppression untested.

### 6.3 Retrieval → Activation → Context Planning

Retrieval returns evidence and completeness metadata; activation is a recommendation, not Context mutation. Context planner must respect authority, scope, evidence, uncertainty, freshness and budget. Model-generated summaries remain untrusted data.

Status: logical boundary sound; cross-module cursor/completeness contract and quality/resource tests open.

### 6.4 Context Change → Delivery → Adapter Applied

G owns ContextVersion and Delivery intent. H transports; C owns final request boundary; Adapter reports evidence. Delivered is not Applied. Full Applied requires exact target ContextVersion and Delivery, inference_request_id, Agent/session, Adapter identity and instance, CapabilityEpoch, PermissionEpoch, ForgetFenceGeneration, managed-region digest, protected-region integrity and final immutable request submission evidence.

Status: C/G/H are conceptually aligned but no final-request runtime evidence or independent verifier execution exists. Lost ACK remains Unknown until reconciliation; duplicate/late ACK must be attempt-scoped and cannot roll back a newer target.

### 6.5 Forget → Fence → Producer Barrier → Derived Suppression → Revocation

Expected sequence: I policy/target inventory and D canonical fence are coordinated; producer admission and in-flight work barrier account for pre-fence producers; staged derivatives cannot publish unless dependency registration and publication gate pass; F suppresses cache/index/working sets; G invalidates snapshots/deltas/deliveries; H/C clear or reconcile adapters; I tracks global target completion, retention, backups and external copies.

Status: NOT CLOSED. D local fence is not I global completion. Producer admission/fence/dependency/publication atomicity lacks implementation evidence. F anti-resurrection and G/H/C offline/reconnect behavior require fault injection. No deletion or global completion guarantee may be claimed.

## 7. Deployment Topology Assessment

| Profile | Proposed topology | Constraints and fail-safe behavior |
|---|---|---|
| Local single-user | Rust modular monolith + SQLite WAL + blob store + FTS5; optional inference worker | Simplest operational model. One transactional authority; bounded workers; inference/index failure cannot block canonical recovery. |
| Local multi-Agent | Shared Brain authority, isolated Agent sessions/Contexts, per-principal authorization, sidecar or SDK | Must isolate session caches, enforce scope before candidate emission, bind Adapter identity and permission epochs. |
| Remote Agent | Authenticated HTTP gateway + BMCP + local/remote Brain service | Requires I-approved issuer/delegation, TLS/key rotation, rate limits, replay controls, residency and outage behavior. |
| CPU-only / model offload | Durable Brain + lexical/structured retrieval; remote or CPU model optional | Core memory functions remain available without local GPU. Model unavailable yields reduced capability, not loss of durable acceptance. |
| 12–16GB VRAM | Separate inference process, explicit model quantization/context/concurrency limits | No capacity claim until measured with OS/driver/runtime overhead and concurrent sessions. |

Process separation is justified for inference and potentially adapter sidecars. Splitting every logical module into a service is not justified by current evidence.

## 8. Resource Budget Assessment

**All resource/performance values are NOT BENCHMARKED.** No production measurements or reproducible prototype results were found in the reviewed reports.

| Resource | 12GB VRAM | 16GB VRAM | CPU-only / offload | Evidence required |
|---|---|---|---|---|
| Model weights + KV cache | Must fit after driver/runtime reserve; quantization/context/concurrency determine feasibility | More headroom but still workload-dependent | RAM and latency dominate | Exact model, quant, context, batch, concurrent sessions, peak VRAM |
| Embedding/reranker | Schedule separately or share GPU with strict admission | Potentially co-resident only after measurement | CPU fallback or remote | Embedding throughput, queue wait, model load, peak memory |
| Rust host / DB / indexes | Host RAM independent of VRAM; GPU contention must not starve host | Same | Host RAM/CPU only | RSS by process, WAL/cache/index sizes, CPU saturation |
| Compiler peak | Bounded worker concurrency and payload sizes | Same | CPU bound may lengthen queue | Peak RSS, CPU-seconds/event, queue backlog and recovery |
| Runtime P95/P99 | Must measure warm/cold and GPU contention | Same | CPU-only separate profile | Retrieval QPS, corpus/selectivity/top-k, p50/p95/p99 |
| SSD / growth | Canonical + blobs + WAL + index generations + backup + temporary rebuild space | Same | Same | Bytes/event, retention, amplification, rebuild scratch |
| Concurrent Agent sessions | Per-session context/cache/queue bounded | Same | Same | Session count × working set, fanout, reconnect burst |
| Index build/recovery | CPU/RAM/SSD and optional embedding GPU | Same | Slower CPU path | Full/incremental rebuild duration, peak disk/RAM, lag |

Required sizing formulas:
- Host memory = DB page cache + index resident set + cache/working sets + compiler in-flight payloads + per-session Context + transport buffers + runtime overhead.
- Durable queue bytes = pending item count × retained payload/evidence bytes × retry/retention factor.
- Index storage = corpus vectors × dimensions × bytes/component + ANN graph overhead + lexical/structured indexes + staging generation.
- GPU peak = weights + KV cache(context, concurrency, batch) + embedding/reranker allocations + runtime/driver reserve.
- Rebuild scratch must accommodate old safe generation plus new staging generation until atomic promotion.

No numeric RAM/SSD/session limits should be invented before representative workload definitions.

## 9. Failure Recovery Matrix

| Failure | Detection / isolation | Recovery source and action | Loss / safety risk | Required test |
|---|---|---|---|---|
| Database crash | Health check, failed transaction, process restart | WAL recovery; replay durable outbox from DB | Uncommitted work may retry; corruption risk | Crash at every commit boundary |
| Disk full | ENOSPC, queue and WAL growth alerts | Stop new nonessential work; preserve canonical DB; free only safe derived/temp data | Accepted receipt without work intent must never occur | Fill DB, blob and staging volumes independently |
| WAL corruption | SQLite recovery failure/checksum/consistency check | Restore verified backup; replay durable logs if available; fail closed | Potential loss since backup; no silent truncation | Corrupt/truncate WAL and verify restore |
| Index loss | Generation/checkpoint missing | Rebuild from canonical history + current Forget state | Search degraded/unavailable; resurrection risk | Delete index and rebuild after Forget |
| Compiler crash | Worker lease expiry/heartbeat | Retry from durable accepted work and idempotency key | Duplicate compile; partial staging | Crash before/after candidate and receipt |
| Outbox replay | Duplicate dispatch/lease expiry | Idempotent consumer, stable work ID, payload digest | Duplicate derivative if gate weak | Replay same/different payload under same key |
| Queue/DLQ backlog | Age/depth/bytes/attempt alarms | Backpressure, quarantine poison item, controlled replay | Latency and disk exhaustion | Burst, poison message and recovery drain |
| Forget vs derivative publish | Fence generation and barrier mismatch | Atomic admission/fence/dependency/publish gate; reject or suppress stale publication | Critical resurrection risk | Race at every interleaving, including crash/restart |
| Adapter offline | Heartbeat/network timeout | Retain bounded pending state; reconnect auth + current fence/permission + Context reconciliation | Stale context visible on reconnect | Long offline Forget and permission revocation |
| Context delivery duplicate | Delivery ID/attempt dedupe | Idempotent attempt ledger; reconcile exact target | Duplicate apply or false ACK | Duplicate, reordered and late deliveries |
| Applied ACK lost | Timeout / Unknown | Query/reconcile request-bound evidence; never infer success | False Full Applied if receipt conflated | Submit succeeded but ACK dropped |
| Model service unavailable/OOM | Health and worker exit | Restart isolated worker; queue bounded; use fallback/disable inference | No new summaries/embeddings; canonical data safe | Kill worker, VRAM OOM, provider timeout |
| PermissionEpoch changes | Epoch mismatch at protected boundary | Reauthorize; invalidate relevant cache; fail closed | Stale authorization/data leakage | Revoke during retrieval, delivery and final submit |
| Upgrade/schema migration | Version mismatch, migration failure | Backup, forward migration, compatibility gate, rollback plan | Partial schema/data incompatibility | Crash mid-migration and restore old/new version |
| Backup restore | Restore audit and generation check | Restore DB+blobs, replay governance/Forget state, rebuild indexes, reconcile adapters | Forgotten data resurrection or missing blobs | Restore pre-Forget backup and prove suppression |
| Key loss/rotation | Key version/unwrap failure | Recover via approved escrow/rotation; never silently downgrade | Data unavailable or confidentiality failure | Rotation, expired key and lost-key drill |

None of these tests is claimed as passed by this review.

## 10. Security & Forget Assessment

1. Principal identity must come from authenticated transport/session binding, not payload ActorRef/Agent/Adapter claims.
2. B owns typed ActorRef/ScopeRef semantics; I owns issuer/delegation, policy, permission and revocation. H transports and validates but does not mint authority.
3. PermissionEpoch, ForgetFenceGeneration, ProducerDomainInventoryEpoch, D work-item barrier, ContextVersion, CapabilityEpoch, CanonicalCommitCursor and IndexWatermark are distinct typed namespaces.
4. Authorization must occur before candidate emission and be rechecked at protected boundaries, including cache hit, delivery, final inference submit and reconnect.
5. Forget requires both D's canonical local fence and I's global target inventory/completion mapping. Local suppression ACKs do not independently establish global completion.
6. Backups, offline adapters, exports, external derived copies, logs and key retention require explicit I policy. A logical tombstone is not proof of physical erasure.
7. Memory/evidence/summaries are untrusted data, not instructions. Prompt injection requires a threat model and adversarial tests across ingestion, retrieval, context compaction and inference boundaries.
8. Replay must reauthorize and recheck current fence, expiry, target Context and idempotency. No stale replay may republish forgotten derivatives.
9. F cache keys must include authority/security domain, scopes, environment/session dimensions, PermissionEpoch, ForgetFenceGeneration, version/index generation, query semantics and retrieval profile. TTL is not a safety mechanism.
10. G snapshot/delta/delivery and C/H Adapter state must be invalidated or reconciled after Forget and permission changes.

Security/Forget verdict: **OPEN / BLOCKING**. No global Forget completion, physical erasure, anti-resurrection, or prompt-injection resistance is certified.

## 11. Protocol & Compatibility Assessment

- Preserve separate typed fields for protocol version, payload schema version, ContextVersion, PermissionEpoch, ForgetFenceGeneration, CapabilityEpoch, Delivery ID/attempt, inference_request_id, source sequence, CanonicalCommitCursor and IndexWatermark.
- JSON/JCS is a reasonable interoperability prototype; duplicate keys, number/timestamp normalization, Unicode, canonical digest and signature profile need strict vectors. CBOR and gRPC remain alternatives, not approvals.
- HTTP(S) plus local IPC are viable prototype paths. Peer identity mapping, Windows/Unix parity, retry ambiguity and local socket access control require tests.
- Unknown security enums/features, stale epochs, unsupported major versions and identity mismatch must fail closed.
- ACKs are per delivery/attempt. Transport receipt is not Context application. Full Applied must be request-bound and independently verifiable.
- H's local observations (SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN, UNSUPPORTED) require I mapping to global target states.
- Non-Rust clients require shared conformance vectors; Rust FFI requires ABI/version, ownership, panic containment and runtime/thread rules.
- No schema/wire identity freeze before B/I/H/C/G exact binding acceptance.

## 12. Blocking Findings

| ID | Severity | Finding | Owner(s) | Exit evidence |
|---|---|---|---|---|
| A-TAR-P0-001 | P0 gate | Four required Owner technology reviews missing (B/I/D/E) | B, I, D, E | Each report on its owner branch, reviewed source HEAD and exact commit/blob SHA |
| A-TAR-P0-002 | P0 | Fact/Claim ADR remains blocked; dependent schema/wire freeze unsafe | B + affected consumers | Approved ADR and synchronized schema/conformance vectors |
| A-TAR-P0-003 | P0 | Atomic producer admission/fence/dependency/publication linearization not proven | D, E, Storage | Exact operation contract, implementation, race/crash tests and CI evidence |
| A-TAR-P0-004 | P0 | Global Forget completion mapping and end-to-end anti-resurrection not proven | I, D, E, F, G, H, C, Storage | Global target inventory/vector, target ACK mapping, offline/backup/rebuild race suite |
| A-TAR-P1-001 | P1 | Principal/ActorRef/ScopeRef/ProducerIdentity/PermissionEpoch binding not frozen | B, I, H, C, E | Exact typed contract, issuer/delegation rules, forged/stale identity negative tests |
| A-TAR-P1-002 | P1 | Full Applied proof lacks executed final immutable request evidence and verifier | C, G, H, I | Real Agent runtime hook, request-bound attestation and independent negative verifier tests |
| A-TAR-P1-003 | P1 | Index/cache anti-resurrection and pre-candidate authorization untested | F, D, I, Storage | Forget race, rebuild, cache fill/hit and cross-scope fault tests |
| A-TAR-P1-004 | P1 | Storage choice and DB/blob/WAL recovery semantics not selected/proven | A, Storage, D, E | SQLite/PostgreSQL comparison, coordinated backup/restore and WAL corruption tests |
| A-TAR-P1-005 | P1 | Protocol encoding/transport and compatibility profile unvalidated | H, C, I, B | Golden vectors, cross-language SDK, authenticated IPC/HTTP and fuzz tests |
| A-TAR-P1-006 | P1 | No representative workload or resource/performance measurements | A, C, E, F, G, H, Engineering | Reproducible benchmark report for target hardware and workloads |
| A-TAR-P1-007 | P1 | Prompt-injection threat model and adversarial acceptance suite remain open | I, B, C, D, E, F, G, H | Threat model, trust-boundary controls and adversarial test evidence |

P0 labels here indicate release/approval blockers, not a claim that the underlying defects have been reproduced in production. The missing reports are evidence blockers in their own right.

## 13. ADR Decision Register

| ADR / decision | Current state | Decision authority | Required action |
|---|---|---|---|
| B Fact/Claim (ADR-001) | ADR-BLOCKED | B with affected consumers | Resolve semantics and migration/compatibility before schema freeze |
| Storage DB/transaction authority | OPEN / candidate SQLite WAL | Storage owner + A integration | Compare SQLite/PostgreSQL; document atomicity, backup and recovery |
| D/E/Storage producer admission/fence/publish gate | OPEN / BLOCKING | D, E, Storage | Exact linearization and executable race contract |
| F index channels / FTS5 vs Tantivy / ANN | OPEN | F | ADR-F-001/002 with benchmark criteria |
| F typed IndexWatermark and cache policy | OPEN | F with D/E/A/I | ADR-F-003/004 |
| G durable Context store, CAS/outbox | OPEN | G + Storage | ADR-G-001 and crash/CAS/restore tests |
| G snapshot/delta serialization | OPEN | G + H | ADR-G-002 and interoperability vectors |
| G/C/H/I Applied verifier profile | OPEN | C/G/H/I | ADR-G-003 and exact final-submit evidence |
| H envelope canonicalization / signing | OPEN | H + I | ADR-H-001 golden vectors and key profile |
| H HTTP/local IPC profile | OPEN | H + I + C | ADR-H-002 authenticated transport prototype |
| H schema evolution / unknown enum behavior | OPEN | H + consumers | ADR-H-003 compatibility tests |
| H ACK / Full Applied evidence | OPEN | H + C/G/I | ADR-H-004 independent verifier |
| H queue retention / dedupe / retry budgets | OPEN | H + I + E | ADR-H-005 burst, replay and retention tests |
| I global Forget, retention, backup and erasure | OPEN / governance approval required | I + D and target owners | Explicit target inventory, completion vector and backup/external-copy policy |
| Identity / issuer / delegation / PermissionEpoch | OPEN | I + B + H + C + E | Exact binding contract and security ADR |
| Embedding/local inference model | CANDIDATE | A + relevant owners | Model/version/privacy/resource ADR after workload tests |
| Adapter deployment mode | CANDIDATE | C + H + I | Capability-tiered framework compatibility ADR |

No ADR is marked approved solely because a candidate appears in TAB-001 or a review report.

## 14. Prototype & Benchmark Plan

Run correctness before performance tuning. Each result must include commit SHA, environment, fixture/corpus version, command, test ID, expected/actual result and artifact link.

### Gate A — Contract and state-machine conformance
1. B Fact/Claim golden vectors; typed ActorRef/ScopeRef and temporal values.
2. D/E/Storage admission/fence/dependency/publication linearization state machine; exhaustive interleavings and crash points.
3. Event idempotency: same key/same payload and same key/different payload.
4. Canonical cursor versus IndexWatermark typed namespace and gap/replay vectors.
5. Permission and Forget epoch checks at cache, retrieval, delivery and final submit.

### Gate B — Persistence and recovery
1. SQLite WAL prototype with canonical record + cursor + receipt + outbox atomic commit.
2. Compare PostgreSQL under concurrent writers, lock contention, throughput, backup and restore.
3. Blob/database publication, orphan cleanup and coordinated snapshot restore.
4. WAL truncation/corruption, disk full, process kill and schema migration interruption.
5. Context CAS/ChangeSet immutable version/outbox transaction and duplicate delivery ledger.

### Gate C — Forget and security
1. Forget concurrent with ingest, compile, replay, staged derivative, publication, retrieval, cache fill/hit, index rebuild, Context update, delivery, final submit and late ACK.
2. Offline Adapter reconnect after Forget and PermissionEpoch change.
3. Restore a pre-Forget backup; prove all affected canonical/derived/adapter/external targets remain suppressed according to I policy.
4. Prompt injection and poisoned evidence across ingest, retrieval, compaction and model output.
5. Key rotation, missing key, forged identity, issuer/delegation mismatch and unknown enum tests.

### Gate D — Protocol and Agent interoperability
1. JSON/JCS cross-language golden vectors, duplicate keys, Unicode, number/timestamp edge cases and signatures.
2. Rust and one non-Rust SDK over HTTP and local IPC; authenticated peer identity.
3. Lost/duplicate/late ACK, reconnect, unknown status, capability downgrade and bounded queue.
4. At least one real Agent final-submit hook; capture immutable request ID and independently verify Full Applied. Otherwise classify that integration Tier 2/3.

### Gate E — Search and resource benchmark
1. Same corpus/fixtures across SQL structured filters, FTS5 and Tantivy.
2. ANN only after embedding model and corpus are fixed; measure filtered recall, update/delete, tombstone and rebuild.
3. Workloads: corpus size, scopes/selectivity, evidence fanout, top-k, QPS, concurrent sessions, update rate, Forget rate and reconnect bursts.
4. Hardware profiles: 12GB VRAM, 16GB VRAM and CPU-only/offload. Record exact model/quant/context/batch/concurrency.
5. Measure host RAM, GPU peak, CPU, SSD bytes/write amplification, queue depth, compiler peak RSS, embedding latency, retrieval p50/p95/p99 and index rebuild duration.
6. No SLO is approved until workload and percentile methodology are agreed.

## 15. Required Remediation

Execution order:

1. **B/I/D/E publish their missing TAR-AI-001 reports** on their own branches. Each report must cite exact current source HEAD and blobs and distinguish static review from tests.
2. **B resolves Fact/Claim ADR** and publishes consumer migration/conformance vectors. Until then no dependent schema or wire freeze.
3. **D + E + Storage define and implement one atomic/linearizable producer admission, Forget fence, dependency registration and publish gate.** Include crash/restart and adversarial interleaving tests.
4. **I + B + H + C + E finalize identity binding**: authenticated Principal, ActorRef, ScopeRef, ProducerIdentity, issuer/delegation, PermissionEpoch and revocation.
5. **I + D + E + F + G + H + C reconcile global Forget**: producer inventory epoch, D work-item barrier, global target inventory/completion vector, index/cache, Context/delivery, Adapter and backup/external copies.
6. **C + G + H + I deliver executable Applied proof** at the final immutable request boundary and an independent verifier.
7. **F completes index/cache suppression tests** and typed cursor/watermark mapping.
8. **Storage/A run DB/blob/WAL/backup/restore prototypes** and choose persistence only through an ADR.
9. **H/C run cross-language protocol/transport/Agent integration prototypes** and submit exact conformance results.
10. **All owners run integrated fault and security suite**, then resource/performance benchmark.
11. **A refreshes every branch HEAD and report SHA**, performs a second integrated review, and only then recommends a TAB-001 status change through the project decision process.

No branch merge or normative contract freeze is authorized by this report.

## 16. Final Verdict

**NOT REVIEWABLE**

Reason:
- Four of eight mandatory Owner technology reports are missing.
- Multiple P0/P1 cross-module decisions and implementation boundaries remain open.
- No integrated fault-injection, security, Applied-proof, anti-resurrection or performance evidence is available.
- Technology candidates have not passed the required comparative ADR/prototype gates.

This verdict does not reject the modular Rust monolith direction. It rejects final system approval on insufficient evidence.

**TAB-001 must remain CANDIDATE — NOT A TECHNOLOGY FREEZE.** It must not be marked FROZEN, APPROVED or production-ready. A later CONDITIONAL PASS or PASS requires the exit evidence in Sections 12–15 and a fresh branch-aware review.

## 17. Exact Commit and Blob SHA Evidence

### 17.1 Core reviewed files

| Artifact | Ref | Blob SHA |
|---|---|---|
| TAB-001 technology blueprint | main | 7b6f2d139217dbe13ab3a3af31bfbff525f20e71 |
| TAR-AI-001 review task pack | main | 5a813edeccf7190d66dfd71a96ca581c48f8a4cb |
| Architecture roadmap | main | 29289361973ec4369f067706132190793cd57a6b |
| Phase 2 D/E/F/G reconciliation | main | 3cd31abeac88703de5b9a0b29bea5d82cd5fdee7 |
| Phase 3 D/E/H/I contract review | main | edaccb802e0425f2d47bd4b613fab4dfde107144 |

### 17.2 Owner report blobs

| Owner | Report blob |
|---|---|
| C | 799aa6e533d10240ed8f6050e15f56e6646c0327 |
| F | 8437b5bbf676361feb2f4e62c21d9d8495f6e619 |
| G | 6211845c21f40a8c4a51d450330dd1750e76e50b |
| H | 0f158555f1870c5a41273a41d35e2b05a7b39283 |
| B | MISSING — no TAR-AI-001 report found |
| I | MISSING — no TAR-AI-001 report found |
| D | MISSING — no TAR-AI-001 report found |
| E | MISSING — no TAR-AI-001 report found |

### 17.3 Relevant owner decision artifacts

| Artifact | Branch | Blob SHA |
|---|---|---|
| B Fact/Claim ADR-001 | B | a1024938ff5baba069cf128c69496a44e143330c |
| I global Forget target inventory/completion | I | 9100061fa986fb6676656169de3fcf9fc1c72664 |
| I Phase 3 global Forget remediation | I | 6bc45a0aed5b5cb019149e4564d1eeb73e7c2512 |
| I Phase 3.5 global identity/Forget governance | I | a8632931396125019d1afccff39ea266f52a4d3a |
| D Forget fence and completion contract | D | 1f0391bc49d007c44ec74165bd33d37412cc7990 |
| D Forget fence operation/publication gate | D | 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5 |
| D/E joint Forget linearization decision | D | 1b6a312ecffd3947bbb4df59f902242482c98a40 |
| E compiler state and producer admission | E | e59f517fff161ab882aa0ddc4a5bda513964ae1a |
| E Forget fence and derived registration | E | 00e37ba56596e710513c8d0568acd79141d9101b |

### 17.4 Snapshot limitations

Branch HEADs in Section 2.1 are the observed review snapshot. The A/B/I/D/E owner technology reports do not exist in the inspected branch trees at those heads. Existing domain, protocol, Forget and integration artifacts were used only as contextual evidence. No missing report was inferred, and no historical commit was substituted for a current owner report.

No CI run, implementation test, fault-injection run, penetration test, benchmark or production measurement was executed as part of this final review.

---

**A — Principal Integration Architect**  
**Decision: NOT REVIEWABLE**  
**TAB-001: CANDIDATE / NOT FROZEN**
