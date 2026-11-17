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

## 18. Reassessment after Owner report completion and architecture-phase COC closure (2026-11-17)

### 18.1 Superseding determination

The original `NOT REVIEWABLE` verdict was driven in part by the absence of four mandatory Owner technology reports. That evidence gate is now closed: B, I, D and E reports have been created on their respective Owner branches, read back, and pinned by exact Blob SHA. All eight Owner technology reports (B/I/D/E/F/G/H/C) now exist. The original NOT REVIEWABLE verdict remains an accurate historical description of the earlier snapshot, but is **superseded for the current review state** by this reassessment.

**Current A verdict: CONDITIONAL PASS — ARCHITECTURE DESIGN BASELINE ONLY; NOT FROZEN; PRODUCTION/RELEASE ACCEPTANCE BLOCKED.**

This is a conditional acceptance of the architecture direction and owner-boundary design for continued engineering planning. It is not a production readiness decision, implementation PASS, security certification, global Forget completion, schema freeze or permission to merge/freeze TAB-001.

### 18.2 Current Owner report and branch evidence

| Owner | Current branch HEAD | Technology report Blob SHA | Disposition |
|---|---|---|---|
| B | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | `473c9bb1b8d010e9e20c16975864be7b2daa3253` | CONDITIONAL PASS; Fact/Claim ADR-001 remains blocked. |
| I | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `3558856fcc109efc6ed1cda3a53ac7900a89fd31` | CONDITIONAL PASS; Global Forget/security governance remains open. |
| D | `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9` | `3dcb96b2e3ddb81df728a7b07398b78709e1f13d` | CONDITIONAL PASS; D semantics accepted, implementation deferred. |
| E | `0d77d0ad6e564873127c53d7dd02edca09e822e1` | `6a83d67ccabdded20d4d4ebf28b9fbfa7d8f8cc3` | CONDITIONAL PASS; producer lifecycle accepted, runtime integration unverified. |
| C | `d13aa06ba42820a27bba18ecb6eae13dc9071599` | `799aa6e533d10240ed8f6050e15f56e6646c0327` | CONDITIONAL PASS; provider-specific idempotency/runtime proof open. |
| F | `5a9816ce5732a3f437e24bbd9a82630a5f4f2c6f` | `8437b5bbf676361feb2f4e62c21d9d8495f6e619` | CONDITIONAL PASS; index/cache/Anti-Resurrection tests open. |
| G | `e8547303bc464dbfd42d8d402b538e2b32033934` | `6211845c21f40a8c4a51d450330dd1750e76e50b` | CONDITIONAL PASS; Applied validator/persistence unverified. |
| H | `9c33237ecc4801a63d62d1c56184f3d48c53f65f` | `0f158555f1870c5a41273a41d35e2b05a7b39283` | CONDITIONAL PASS; schema candidate only, interoperability/runtime validation open. |

### 18.3 Architecture and protocol decisions now closed at design level

1. B/I/D/E technology reviews are complete; the four reports distinguish candidate direction from decisions, implementation and test evidence.
2. The exact CGH-APPLIED-1.1 / JF-10 bridge owner matrix is recorded at `reviews/integration/phase-3.6-cgh-applied-1.1-owner-acceptance-matrix.md`, commit `a480a713db358b30dc4cf7c9157025b3c116e439`.
3. The COC durable log/participant/recovery protocol is pinned at Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`. All A/B/C/D/E/F/G/H/I/Storage owner perspectives have exact-Blob acceptance records. A's matrix is `reviews/integration/phase-3.6.3-coc-durable-protocol-acceptance-matrix.md`, commit `e5fad5b3e67662134c18e33090b08d874f161f41`.
4. Storage Gate B is **DESIGN-LEVEL ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS**. Its consensus implementation, distributed failure tests and Gate C runtime conformance are deferred to engineering.
5. PostgreSQL 18.7 is now a qualified prepared-XID capability candidate for the pinned CI profile; it is not a production deployment selection. The latest seven-workflow regression set is 7/7 SUCCESS: PITR `43958775001`; prepared-XID `43959079736`; synchronous promotion `43959079669`; backup/restore `43959079703`; WAL PITR `43959079745`; sync-unavailable fail-closed `43959079760`; pg_rewind/rejoin `43959079930`.
6. COC in-memory outage-recovery reference model: 11 tests passed in run `43897364938`. JF-10/COC semantic validator: 18 tests passed in run `43905568915`. Neither proves a live COC quorum, owner-service integration or production runtime.

### 18.4 Updated blocking register

| ID | Current status | Updated interpretation |
|---|---|---|
| A-TAR-P0-001 — missing B/I/D/E reports | **CLOSED** | All four reports exist on Owner branches with exact Blob and current branch HEAD evidence. |
| A-TAR-P0-002 — Fact/Claim ADR | **OPEN / P0** | ADR-001 remains ADR-BLOCKED. No canonical schema or dependent wire freeze. |
| A-TAR-P0-003 — producer admission/fence/dependency/publication linearization | **DESIGN ACCEPTED / IMPLEMENTATION P0 OPEN** | D/E/Storage/JF-10 exact contract and owner acceptance now exist; PostgreSQL capability tests pass. Real E/D/I/Storage application-path integration and Gate C race/crash/failover tests remain engineering release blockers. |
| A-TAR-P0-004 — Global Forget completion and Anti-Resurrection | **OPEN / P0** | I target inventory, complete external/backup/recipient mapping, owner receipts and end-to-end suppression/rebuild/reconnect proof remain unclosed. |
| A-TAR-P1-001 — identity/typed references | **DESIGN ACCEPTED WITH EXCEPTIONS** | B/I/H/C/E boundaries are documented; runtime authentication, issuer/delegation and stale-epoch negative tests remain. |
| A-TAR-P1-002 — Full Applied final-request proof | **OPEN / P1** | C/G/H schema and owner predicates exist; real Agent final-submit hook and independent verifier are not implemented. |
| A-TAR-P1-003 — index/cache Anti-Resurrection | **OPEN / P1** | F retrieval suppression, rebuild, cache fill/hit and stale-watermark race tests remain. |
| A-TAR-P1-004 — Storage selection/recovery | **PARTIALLY RESOLVED** | PostgreSQL 18.7 is a qualified capability candidate with 7/7 CI; production engine/deployment profile and real I/D integration remain open. |
| A-TAR-P1-005 — protocol/compatibility | **OPEN / P1** | H 1.1.0 schema candidate exists; generated IDL/SDK, canonical parser, crypto and interoperability tests remain. |
| A-TAR-P1-006 — workload/resource benchmark | **OPEN / P1** | No representative corpus, throughput, latency, storage growth or VRAM/CPU benchmark. |
| A-TAR-P1-007 — prompt-injection/threat model | **OPEN / P1** | Threat model and adversarial acceptance suite remain outstanding. |

### 18.5 Architecture-phase gate interpretation

The project is in architecture design; no production implementation repository/runtime is expected yet. Set `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. Missing production code is not a design defect. Architecture contracts and owner decisions must nevertheless be complete before TAB-001 can be frozen. Executable integration, distributed fault injection, security validation, benchmarks, named deployment operators, numeric RTO and production runbooks remain engineering/deployment gates.

### 18.6 Final disposition

- **Reviewability gate:** PASS — all eight Owner reports exist and were verified.
- **Architecture design:** CONDITIONAL PASS — owner-boundary contracts and COC Gate B design are accepted with explicit exceptions.
- **TAB-001:** CANDIDATE / NOT FROZEN.
- **Fact/Claim ADR-001:** BLOCKED.
- **Global Forget governance/completion:** OPEN / BLOCKING.
- **JF-10 implementation and Gate C:** OPEN / BLOCKING for production release.
- **Production activation / merge / technology freeze:** NOT AUTHORIZED.

This reassessment supersedes only the prior `NOT REVIEWABLE` verdict's missing-report rationale and the earlier P0-003 design-contract gap. It does not waive any P0/P1 item, owner authority, exact-version acceptance requirement or production evidence requirement.
## 19. Latest logical-model and schema validation evidence (2026-11-17)

### 19.1 New evidence

| Area | Exact evidence | Result | What it does not prove |
|---|---|---|---|
| F Anti-Resurrection | Model Blob `33fa2ca2dc29771aca241e194f13e078a4f8d774`; tests Blob `c2575327a75577923440ef770d42122218a1e091`; run `43961714501`, job `133630540252`, commit `f1ba5c478e395da6b126423e32e20d0990e61920` | **19/19 PASS** | No actual ANN/index/cache/Working Set implementation, multi-process race, real reconnect or restore proof. |
| I Global Forget inventory/CEV | Model Blob `5233da028e409ec3f41848582dad73a923e7155b`; tests Blob `091f9450adf49a2a9f9ec8a2fa4470918023f765`; run `43962873109`, job `133634616584`, commit `73a0bff13b531b5b9feaeeec1887db31d6266589` | **25/25 PASS** | No production ProducerDomainInventoryEpoch registry, real TargetInventorySeal, actual external target evidence, governance approval or physical erasure. |
| H JF-10 bridge schema | Schema Blob `a8a945cc3623c2907003b93625e3c79742150944`; tests Blob `74bc4286abe1489ce29c2446c6fc22445784609f`; run `43962364955`, job `133632849768`, commit `eab7ee9d196437daed31d5853570b7fb7acf08b6` | **11/11 PASS** | No duplicate-key canonical parser, signature/channel binding, unknown-critical-extension enforcement, generated IDL/SDK or live transport interoperability. |

These results improve logical and schema evidence only. They do not close Global Forget, Anti-Resurrection runtime or JF-10 implementation P0.

### 19.2 Current Owner report manifest

| Owner | Current branch HEAD | Current technology report Blob SHA |
|---|---|---|
| B | `310f305575d6f406e80d5d6ebf951bcd9e79e35f` | `fd3e5723b81de10bed806896e4be71ceb7a1669b` |
| I | `fad96468cc5cf295b7fd389ad2677cae5dfd0979` | `6b87bc61cf48d7377cc689a2316cdf3771b616af` |
| D | `a3ea0de75ca7b2297589293ec142f2cb07757282` | `97c049050d67dd12e0c64ef49b2b05795651608c` |
| E | `5fb76b666fac49ceeb51ddb7c320fe5975313d99` | `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8` |
| C | `018de5044810e755d4e21cb21e982526c27eb9a8` | `ee42c7192561261789a0c7b5bd16d32c0eaaf14c` |
| F | `e4c26214b8f78169c0e20f1faae23f945c3afeb9` | `124cc9300442b0e3a1e83603910e1c332b4fae48` |
| G | `b0c515399c6a336dcbf17a1ced6925413c804d5c` | `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613` |
| H | `b99e5ead283dd1dcc3e86a4da871356731e162dc` | `c003e6cc078fc58d6c150d0fb418c28f94de8e8a` |

### 19.3 Updated blocking register

- A-TAR-P0-001 missing Owner reports: **CLOSED**.
- A-TAR-P0-002 Fact/Claim ADR-001: **OPEN / P0**; no formal Architecture Governance approval exists.
- A-TAR-P0-003 JF-10 atomic registration/fence/dependency/publication: **DESIGN ACCEPTED / IMPLEMENTATION P0 OPEN**.
- A-TAR-P0-004 Global Forget: **OPEN / P0**. The 25-test logical model passes, but no real inventory seal, complete target evidence, external recipient proof, restore drill or physical-erasure proof exists.
- A-TAR-P1-003 Anti-Resurrection: **LOGICAL MODEL PASS / RUNTIME OPEN**.
- A-TAR-P1-005 BMCP JF-10 schema: **STRUCTURAL VALIDATION PASS / INTEROPERABILITY OPEN**.

### 19.4 Current verdict remains unchanged

The additional logical-model/schema CI results do not justify a stronger system verdict. The current disposition remains **CONDITIONAL PASS — ARCHITECTURE DESIGN BASELINE ONLY; NOT FROZEN; PRODUCTION/RELEASE ACCEPTANCE BLOCKED**. TAB-001 remains CANDIDATE / NOT FROZEN; Global Forget is NOT COMPLETED; production activation is NOT AUTHORIZED.

---

## 20. Superseding live revalidation — TAR-AI-001 final system decision (2026-11-17)

> This section is the controlling current assessment. It supersedes the historical branch snapshot, missing-report rationale, and earlier conditional system verdicts in §§1–19 where they conflict with the live evidence below. Earlier sections remain as audit history. The original TAB-001 blueprint is not modified by this addendum.

### 20.1 Executive decision

**Final Verdict: BLOCKED.**

**TAB-001: CANDIDATE / NOT APPROVED / NOT FROZEN.**

The mandatory eight Owner technology reports now exist and have been fetched from their respective current Owner branches. Therefore, the earlier NOT REVIEWABLE verdict's missing-report rationale is no longer applicable. However, the current evidence does not satisfy the system approval gate:

- B Fact/Claim remains ADR-BLOCKED.
- D/E/Storage producer admission, Forget fence installation, complete dependency registration and final publication visibility still lack one implemented and end-to-end verified linearization boundary.
- JF-10 application integration between I sequencer, Storage prepared participant/XID, D fence/lineage and C provider-side-effect admission remains P0 OPEN. PostgreSQL capability CI does not close the application integration gap.
- I Global Forget target inventory/seal, external recipient coverage, target evidence and restore governance remain OPEN; D-local suppression is not global completion.
- C/G/H Full Applied still requires one exact compatible proof profile and an executable final-request boundary verifier.
- H/I/C identity and Permission binding has technical design progress but remains subject to governance approval, consumer conformance and runtime tests.
- F's anti-resurrection result is a logical model pass, not an actual index/cache/ANN/rebuild/reconnect pass.
- No representative application performance or resource benchmark has been run.

This is a **BLOCKED** verdict rather than NOT REVIEWABLE: the system is reviewable, the reports are present, and the blocking evidence is identifiable. It is not a PASS or CONDITIONAL PASS because the unresolved P0s are not merely future production-hardening tasks; they affect the correctness and authority boundaries of the proposed system.

### 20.2 Live branch HEAD and exact Owner report verification

The following HEADs were refreshed from the live branch refs by comparing each ref with itself. Report Blob SHAs are from fetching the exact report path at the current branch ref.

| Owner | Current branch HEAD | Technology report path | Current report Blob SHA | Owner report verdict / current qualification |
|---|---|---|---|---|
| B | `310f305575d6f406e80d5d6ebf951bcd9e79e35f` | `reviews/technology/owner-b-domain-model-technology-review.md` | `fd3e5723b81de10bed806896e4be71ceb7a1669b` | CONDITIONAL PASS; ADR-001 remains ADR-BLOCKED |
| I | `73a0bff13b531b5b9feaeeec1887db31d6266589` | `reviews/technology/owner-i-security-governance-technology-review.md` | `592baa4653e91287678a1e0926119ca94780bc08` | CONDITIONAL PASS for direction; deployment and Global Forget BLOCKED |
| D | `a3ea0de75ca7b2297589293ec142f2cb07757282` | `reviews/technology/owner-d-canonical-brain-technology-review.md` | `97c049050d67dd12e0c64ef49b2b05795651608c` | CONDITIONAL PASS for semantics; implementation/JF-10 BLOCKED |
| E | `5fb76b666fac49ceeb51ddb7c320fe5975313d99` | `reviews/technology/owner-e-memory-compiler-technology-review.md` | `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8` | CONDITIONAL PASS for compiler topology; publication/recovery BLOCKED |
| F | `e4c26214b8f78169c0e20f1faae23f945c3afeb9` | `reviews/technology/owner-f-memory-runtime-technology-review.md` | `124cc9300442b0e3a1e83603910e1c332b4fae48` | CONDITIONAL PASS; logical model PASS, runtime OPEN |
| G | `b0c515399c6a336dcbf17a1ced6925413c804d5c` | `reviews/technology/owner-g-memory-context-technology-review.md` | `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613` | CONDITIONAL PASS; Applied/runtime and durable Context evidence OPEN |
| H | `b99e5ead283dd1dcc3e86a4da871356731e162dc` | `reviews/technology/owner-h-bmcp-technology-review.md` | `c003e6cc078fc58d6c150d0fb418c28f94de8e8a` | CONDITIONAL PASS; schema structure PASS, protocol freeze OPEN |
| C | `018de5044810e755d4e21cb21e982526c27eb9a8` | `reviews/technology/owner-c-agent-integration-technology-review.md` | `ee42c7192561261789a0c7b5bd16d32c0eaaf14c` | CONDITIONAL PASS; final-submit runtime proof OPEN |

All eight reports were fetched and their contents inspected. All eight explicitly identify their execution as a centralized/delegated static architecture review, not independent human-owner attestation. This limits the governance meaning of the reports: they are owner-scoped technical review artifacts and do not substitute for separately required approvals.

**Reviewed source snapshot versus publication tip:** the report metadata records earlier source snapshots in several cases (B `a5bf20b...`, I `4b1ef1c...`, D `06bce7f...`, E `9f53263...`, F `f1ba5c4...`, G `e854730...`, H `9c33237...`, C `d13aa06...`). These are not misreported as current branch HEADs. Live compare confirms that B's one-commit delta, D/E/G/C report-publication deltas, I's eight-commit delta, F's three-commit delta, and H's nine-commit delta are distinct from the report's reviewed source snapshot. I's later delta includes Global Forget logical-model/evidence artifacts; F's includes anti-resurrection model evidence; H's includes JF-10 schema validation evidence. The current report blobs above are the fetched versions at the live branch tips.

### 20.3 Phase 2 / Phase 3 reconciliation

The required integration reports were fetched and read:

| Artifact | Path | Blob SHA | Current interpretation |
|---|---|---|---|
| Phase 2 D/E/F/G reconciliation | `reviews/integration/phase-2-defg-cross-session-reconciliation.md` | `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7` | Historical branch-aware reconciliation; CONDITIONAL PASS for continued integration, not freeze |
| Phase 3 D/E/H/I contract review | `reviews/integration/phase-3-defghi-cross-module-contract-review.md` | `edaccb802e0425f2d47bd4b613fab4dfde107144` | Historical static contract review; CONDITIONAL PASS for integration, not freeze |
| Phase 3 remediation task pack | `reviews/integration/phase-3-cross-module-remediation-task-pack.md` | `7abe73e5209ee985c9807b95d99616069911a6b7` | Task package, not approval |
| TAB-001 review task pack | `reviews/integration/tab-001-a-i-technology-architecture-review-task-pack.md` | `cf903cd5812cfed3a64a52b169a3bd84209ba3f5` | Review task pack; not review result |

Phase 2 correctly distinguishes branch visibility errors from design quality and preserves INT-P0-01..04 as open at that snapshot. Phase 3 correctly identifies the D/E registration/publication linearization gap, stale cursor references, identity binding, Global Forget mapping, Fact/Claim ADR and Applied proof as open. Later Owner decisions and tests narrow some design questions, but do not establish application implementation closure.

### 20.4 System architecture assessment

The architecture's logical separation is sound and should be preserved:

| Layer | Authority and boundary | System assessment |
|---|---|---|
| Agent Adapter / telemetry | C captures host events and final inference-boundary evidence; Agent retains planning/tool authority | Sound boundary; no Tier 1 final-submit integration demonstrated |
| BMCP | H owns envelope, schema, transport, capability negotiation and ACK carriage | Sound separation; current schema is candidate, interoperability and authentication proof open |
| Security / Governance | I owns Principal trust, authorization, PermissionEpoch, revocation, target inventory and global completion | Correct authority placement; operational security and governance approval open |
| Ingress / Compiler | E owns durable Accepted receipt, work state, extraction proposals, provenance and staged derivatives | Sound semantic split; durable implementation and publication gate open |
| Canonical Memory Brain | D owns canonical identity/version, lifecycle, canonical commit cursor, Forget fence and producer barrier | Sound authority; Fact/Claim schema remains blocked by B ADR |
| Runtime / Retrieval | F owns candidate retrieval, ranking, completeness, watermarks, activation recommendations and disposable cache/working sets | Sound boundary; filtering and anti-resurrection runtime tests open |
| Memory Context | G owns Context membership/order/budget, ContextVersion, ChangeSet and Delivery intent | Sound boundary; durable CAS/reconciliation and Applied verifier not demonstrated |
| Persistence / COC | Storage owns database transaction, prepared participant/XID, visibility pointer and publication receipt; COC orders participant observations | Authority split is coherent; latest amended protocol and physical implementation gates remain open |
| Index / Cache | Derived, rebuildable and never authoritative | Correct principle; actual anti-resurrection runtime proof absent |
| Inference | Optional, replaceable provider; model output remains proposal | Correct isolation principle; target hardware/model workload not benchmarked |

No cyclic dependency is required if these authorities remain enforced. The initial modular Rust monolith is a reasonable local-first prototype topology, but it does not by itself solve cross-authority JF-10. The COC quorum, I sequencer, D control ledger, Storage prepared participant, C provider boundary and their durable owner-local gates are separate logical durability/authority domains. Their process and failure-domain topology must be explicitly included before deployment approval. Logical modules must not automatically become microservices.

### 20.5 Technology selection matrix — current disposition

No candidate is upgraded to APPROVED solely by appearing in TAB-001 or an Owner report.

| Concern | Preferred candidate / alternatives | Current decision | Cost, reliability and compatibility assessment | ADR / prototype |
|---|---|---|---|---|
| Core language | Rust; alternatives Go/JVM/Python | Rust is the project direction, not a complete toolchain freeze | Strong typing/ownership for state machines; compile-time and integration complexity; CPU/RAM depend on workload | Existing direction; crate/dependency review |
| Async runtime | Tokio; alternatives async-std / sync workers | RECOMMENDED, not frozen | Mature async IO; CPU-heavy work must not block executor; bounded worker pools required | Runtime supervision prototype |
| Primary transactional DB | SQLite WAL vs PostgreSQL; embedded KV/RocksDB alternative | No final DB ADR | SQLite low operations and embedded footprint but single-writer limits; PostgreSQL stronger concurrent transaction and prepared-XID capability but service/admin/HA burden; KV shifts constraints and transactions into application code | ADR-TEC-001; same-fixture app conformance and workload comparison |
| PostgreSQL prepared-XID profile | PostgreSQL 18.7 pinned CI profile | QUALIFIED ENGINE-CAPABILITY CANDIDATE only | Seven CI workflows passed; does not prove production deployment, real I/D/COC integration, production fencing or application-level atomicity | Gate A remains PARTIAL PASS / OPEN |
| Blob storage | Content-addressed local filesystem + transactional metadata; alternatives DB blobs/object store | RECOMMENDED direction | Filesystem/object store needs coordinated DB visibility, digest verification, orphan reconciliation, encryption and complete backup; DB-only snapshot may omit referenced blobs | ADR-TEC-002; crash/restore prototype |
| Structured search | SQL indexes | RECOMMENDED | Strong typed filtering and transactional locality; query plans/selectivity require corpus tests | Workload/query-plan tests |
| Full-text | SQLite FTS5 vs Tantivy | FTS5 first comparison candidate; no selection | FTS5 is colocated and simple; Tantivy offers Rust-native control and scale but adds separate index generation/recovery | ADR-TEC-003; identical corpus benchmark |
| Vector ANN | usearch/HNSW vs sqlite-vec; defer remote vector DB | OPEN | ANN memory, recall, update/delete, filtering and rebuild costs are workload-sensitive; authorization must precede candidate emission | ADR-TEC-004; only after embedding/corpus freeze |
| Cache | Moka in-process; Redis or no cache | RECOMMENDED candidate | Low operational footprint; keys/invalidation must include Authority, Scope, PermissionEpoch, ForgetFenceGeneration and Context identity/version; TTL alone is insufficient | Cache race, memory bound and anti-resurrection tests |
| Queue / scheduling | Transactional outbox + bounded DB-backed Tokio workers; NATS/Kafka alternatives | Candidate for local first release | Outbox avoids dual-write only if transaction boundaries are correct; lease fencing, DLQ, replay and backpressure still require proof; external broker adds operational recovery domains | ADR-TEC-002; crash/replay/poison tests |
| Compiler / extraction | Deterministic Rust normalization + replaceable model providers | Architecture direction accepted; backend open | Deterministic ingress independent of model availability; inference workers require bounded CPU/GPU admission and retry | E application prototype |
| Embedding / reranker | ONNX Runtime candidate; CPU fallback; Candle alternative | CANDIDATE | Compatibility, quantization, execution provider, vector dimension, model/version provenance and CPU/GPU latency unmeasured | ADR-TEC-005; target hardware benchmark |
| Local generative inference | llama.cpp-compatible GGUF worker; Candle alternative; remote provider optional | CANDIDATE | Separate process recommended; weight/KV/context/batch/concurrency determine VRAM; remote provider adds residency/retention risk | ADR-TEC-006; OOM and fallback tests |
| Serialization | Serde internal; JSON/JCS candidate; CBOR/MessagePack alternatives | OPEN / H-owned | JSON debuggable but signing requires canonical bytes, duplicate-key rejection and strict number/Unicode rules; binary encodings need equivalent canonical profiles | ADR-TEC-007; golden vectors/fuzz |
| Transport | HTTP(S), Unix socket / Windows named pipe; gRPC alternative | OPEN / H-owned | HTTP broad interoperability; local IPC low hop cost but platform peer-auth; gRPC adds generated schema/runtime complexity | ADR-TEC-007; cross-language/OS tests |
| Identity / auth | I-issued Principal and typed ActorRef/ScopeRef binding; transport auth mechanisms | Design direction only | Payload identity is a claim, not proof; issuer, audience, delegation, Scope and PermissionEpoch must be authenticated and rechecked at every protected boundary | I/B/H/C joint exact contract and negative tests |
| Crypto / key custody | OS key store, vetted crypto, envelope encryption | OPEN / I-owned | Key loss/rotation/recovery, backup encryption and cryptographic erasure need explicit custody and threat model; no algorithm is approved here | ADR-TEC-010 / I security ADR |
| Backup / restore | Coordinated DB + blobs + WAL/archive + D/I control state + index rebuild | OPEN | Restore must quarantine, reapply current Forget/revocation/retention state before serving; stale backups must not resurrect content | ADR-TEC-010; restore-after-Forget drill |
| Deployment | Local modular monolith + optional isolated inference worker + capability-tiered Adapter SDK/sidecar | CANDIDATE | Good first prototype; COC/I/D/Storage protected cross-authority path adds quorum and operator requirements not proven by a single process | ADR-TEC-009; crash/isolation/upgrade tests |
| Observability / audit | tracing + metrics facade; OpenTelemetry/Prometheus exporters | RECOMMENDED direction | Correlation IDs and typed cursor metrics required; diagnostic logs must not become sensitive memory copies; audit has separate integrity/retention needs | ADR-TEC-008; redaction and audit tests |
| Schema migration | Versioned SQL migrations + compatibility checks | RECOMMENDED | Migration interruption, forward/backward compatibility and restore must be restartable/auditable | Migration fault tests |
| COC | Single logical quorum-committed log, participant registry, recovery cutoff batch, checkpoint/restore | Current amended Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` is PROPOSED / focused exact-owner re-review required | Older Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` has design-level owner acceptance with exceptions; acceptance does not transfer to amended bytes. No production quorum/service is deployed | Exact-version owner review of 86ff; Gate C implementation deferred |

### 20.6 Cross-module dependency and interface matrix

| Dependency | Authority | Current compatibility | Required closure |
|---|---|---|---|
| Fact/Claim → Canonical schema/API/wire | B + Architecture Governance; D/E/F/G consumers | BLOCKED by ADR-001 | Formal ADR decision; exact consumer mapping; schema and migration vectors |
| Principal / ActorRef / ScopeRef / EnvironmentRef | B semantics; I trust/policy; H wire binding; C/E/F/G/D consumers | Design decisions exist, but no end-to-end frozen identity/permission profile | Exact typed mapping, issuer/delegation/audience rules, authenticated transport binding, PermissionEpoch and negative conformance |
| CanonicalCommitCursor → E/F/G | D owns one global ordered sequence per Canonical Memory Authority; F owns per-channel/partition IndexWatermark | D semantic decision is explicit; downstream consumer and Storage continuity tests incomplete | Update all stale coordination artifacts; test gaps, replay, snapshot and cursor atomicity |
| Producer admission / Forget fence / dependency / publish | D semantic authority; E producer lifecycle; Storage physical transaction and visibility | Design boundaries align; application linearization P0 OPEN | One callable transaction/gate contract; no read-then-write split; race/crash proof |
| JF-10 / COC | I sequencer and receipt consumption; Storage prepared participant/XID; D fence/lineage; C provider side effect; COC order/evidence only | Single-policy-domain design only; application integration P0 OPEN | Exact final owner-gate in I policy order; same-XID recovery; C admission and provider outcome; current COC protocol exact acceptance |
| Index / cache / Runtime | D canonical feed; F IndexWatermark and suppression | Logical reference model pass; runtime OPEN | Scope/Permission before candidate emission; authoritative fence revalidation; actual ANN/cache/rebuild tests |
| Context / Delivery / Applied | G owns ContextVersion and Delivery; H transport/ACK; C final submit; I permission; D ForgetFence | Semantic split aligned; common exact Applied profile and execution not complete | Same-version exact binding, independent verifier, final immutable request proof, reconnect and revocation tests |
| Global Forget | I owns sealed target inventory and global Completion Evidence Vector; D/E/F/G/H/C/Storage provide bounded evidence | OPEN | Map every target class and ACK state; inventory epoch/seal; unknown/offline/external/backup targets cannot silently pass |
| Backup / restore | Storage physical backup; I retention/Forget policy; D canonical state | Engine capability evidence only | Restore quarantine, D/I ledger replay, blob/index/Adapter/external recipient reconciliation |

### 20.7 Data flow and control flow assessment

| Flow | Required durable boundary / confirmation | Idempotency and recovery | Status |
|---|---|---|---|
| Event Ingress → Compiler → Canonical Memory | Event + payload reference + idempotency record + AcceptedReceipt + compile intent durable before Accepted; canonical revision and CanonicalCommitCursor atomic | Same key/same payload returns same logical receipt; same key/different payload conflicts; replay retains WorkItemId and current authorization/fence checks | Semantics defined; E/Storage application implementation not evidenced |
| Canonical Memory → Index → Runtime Retrieval | Consume committed canonical changes; typed per-channel IndexWatermark; suppression and authorization before candidate disclosure | Gap detection, deterministic rebuild, stale watermark and Forget revalidation | F logical model partly tested; runtime channels not verified |
| Retrieval → Activation → Context Planning | RetrievalResult/ActivationRecommendation are proposals; G alone commits ContextVersion/ChangeSet | G CAS/base-version, deterministic snapshot/delta reconciliation | Ownership sound; durable Context application not demonstrated |
| Context Change → Delivery → Adapter Applied | G durable Delivery intent; H authenticated transport; C exact final request submission; G records Applied only after valid proof | Retry preserves logical delivery/request identity; timeout/lost ACK is Unknown until queried/reconciled; stale version is superseded | Exact final request implementation and independent verifier OPEN |
| Forget → Fence → Producer Barrier → Derived Suppression → Index/Cache/Context/Adapter Revocation | I authorizes; D installs fence and captures work barrier; E registers complete dependencies; Storage gate controls visibility; F/G/H/C provide bounded target evidence; I seals inventory and decides global completion | Late worker/replay/index rebuild/cache fill/offline Adapter/backup restore must recheck current control state; unknown remains blocking | Multiple design and logical test results exist; integrated P0 OPEN |

### 20.8 Deployment topology assessment

The prototype topology remains a local Rust modular monolith with explicit internal ports and adapters:

1. `brain-app` supervises startup, shutdown, migrations, health and worker admission.
2. Correctness-critical domain, storage coordination, ingress, Compiler state, Context state and governance interfaces remain in a small number of explicit transaction boundaries.
3. PostgreSQL is the current leading prepared-XID capability target for JF-10 integration; SQLite remains a comparative lightweight prototype, not a selected production authority.
4. Blob storage is private/content-addressed until its metadata and publication transaction is authoritative.
5. FTS5/Tantivy and vector indexes are derived services/workers; Moka cache and Working Sets are disposable.
6. Model inference runs in an isolated optional worker with bounded GPU/CPU admission.
7. Agent integration supports embedded SDK where a real final-submit hook exists and sidecar/IPC where process/language isolation is needed. Tier 2/3 integrations cannot claim Full Applied.
8. JF-10 protected operations additionally require the COC quorum, I sequencer, D control ledger, Storage participant and C provider-side-effect boundary. Their process placement, independent failure domains, fencing, operator and recovery topology are not yet deployment-approved.

Do not add Kafka, Kubernetes, a hosted vector database or microservices solely because logical modules exist. Conversely, do not claim a single local process proves distributed COC/JF-10 recovery.

### 20.9 Resource budget assessment

All numbers below are planning envelopes or estimates from TAB-001, not measured application performance.

| Profile | Current planning assumption | Safe interpretation |
|---|---|---|
| 12 GB VRAM | 1.5–2.0 GB driver/runtime/headroom; 6.5–7.5 GB LLM weights; 1.5–2.0 GB KV/context; 0–1.0 GB embedding/reranker transient | Tight budget; sequential GPU scheduling, small context/concurrency, CPU fallback or model offload likely |
| 16 GB VRAM | 1.5–2.0 GB headroom; 8.5–10.5 GB weights; 2.0–3.0 GB KV/context; 0–1.5 GB embedding/reranker transient | More room but no basis to co-schedule large generation, embedding and reranking without measured peak/fragmentation |
| CPU-only / model offload | No approved throughput or latency budget | Durable ingress and canonical authority must remain usable; inference may degrade, queue or be disabled; embedding and LLM CPU throughput require measurement |
| Host RAM | 16 GB minimal test; 32 GB preferred initial development/acceptance; 64 GB+ larger corpus/concurrency | Indicative component estimates: core 0.5–1.5 GB; deterministic compiler 0.5–1.5 GB; retrieval/index/cache 1–4 GB; inference host memory backend-dependent; OS/Agent/filesystem cache reserve additional headroom |
| SSD / database / blob / indexes | No corpus or retention volume supplied | Must budget source payloads, revisions/provenance, WAL, outbox, index amplification, model files, audit, backup generations and restore staging; disk-full must backpressure before false Accepted |
| Concurrent sessions / growth | No fixed session count, write rate, corpus size or retention horizon | No throughput, capacity, RTO/RPO or P95/P99 can be accepted yet |

**Measurement status:** no representative application benchmark or production measurement was found in the eight reports. All ingress/compile/retrieval/context/delivery/Forget latency, throughput, index build/rebuild, SSD amplification, queue depth, RAM/RSS, VRAM peak, model latency and recovery duration remain **NOT BENCHMARKED**.

### 20.10 Failure and recovery matrix

| Failure | Detection / isolation | Required recovery and safe state | Data-loss risk / required test |
|---|---|---|---|
| Database crash | Connection failure, health/readiness loss, transaction outcome unknown | No success ACK before durable commit; resolve unknown transaction by durable ID; restart/replay outbox; retain in-doubt participants | Accepted/canonical ambiguity; kill before/after commit and ACK |
| Disk space exhausted | Low-space alarm, write failure, WAL/blob growth monitor | Backpressure ingress/workers; no partial blob visibility; preserve committed state and cleanup audit | Lost uncommitted input or orphan blob; quota/disk-full injection |
| WAL corruption | Startup/checksum/archive validation failure | Isolate DB; restore from verified backup/WAL; quarantine and replay D/I control state before serving | Loss since last valid WAL/archive; corruption/PITR drill |
| Index loss/corruption | Missing generation, checksum or watermark gap | Rebuild from canonical history plus current Forget/Permission state; publish only complete generation | Stale/forgotten content reappears; delete/rebuild/partial-channel tests |
| Compiler crash | Worker heartbeat/lease expiry | Recover durable WorkItem; new AttemptId/LeaseEpoch; stale worker cannot publish; barrier still accounts for it | Lost source or duplicate derivative; crash at every durable stage |
| Outbox replay / duplicate ingress | Duplicate key, sequence gap, replay counters | Same key/digest returns same receipt; conflict on changed digest; idempotent downstream publication | Duplicate canonical/derived effects; same-key and replay tests |
| Queue/DLQ backlog | Age/depth/lease metrics | Bounded retry, DLQ nonterminal; replay rechecks D/I fence and permission; backpressure producers | Forgotten work resurfacing; poison, retry storm and DLQ-after-Forget tests |
| Forget vs derived publication race | Fence/gate conflict or unresolved participant | One serialization winner; pre-fence work included in barrier; post-fence work rejected/private; UNKNOWN keeps gate closed | Late derivative exposure; exhaustive interleaving and process-kill race suite |
| Adapter offline/reconnect | Session/capability heartbeat expiry | Pending/Unknown; authenticate, get current PermissionEpoch and ForgetFence, clear stale state, reconcile G Context before replay | Stale Context/forgotten content applied; offline Forget/reconnect tests |
| Duplicate Context delivery | Delivery/idempotency ledger | Preserve logical Delivery identity; duplicate does not create second Context version or Applied result | Duplicate or out-of-order prompt region; duplicate/reorder/base-gap tests |
| Applied ACK lost | No ACK or ambiguous adapter outcome | Query exact request-bound proof; remain Unknown until verified; never infer from transport receipt | False Applied; lost ACK after actual submit and after no-submit tests |
| Model service unavailable/OOM | Worker health, allocation failure, timeout | Durable ingress/canonical reads continue where safe; inference retry/degrade/CPU fallback; isolate worker | Lost accepted Event if coupled incorrectly; OOM/provider outage tests |
| PermissionEpoch changes | I sequencer/current policy lookup | Reauthorize at every protected boundary; stale delivery/cache/worker cannot proceed; fail closed on unknown | Unauthorized disclosure/side effect; revoke during read/compile/delivery/submit tests |
| Upgrade/schema migration interrupted | Migration journal/version mismatch | Quiesce incompatible writers; atomic/restartable migration; verified backup/rollback; restore quarantine | Corrupt or incompatible state; kill mid-migration and mixed-version tests |

No row is marked implementation-verified solely from a written recovery rule. Existing PostgreSQL CI evidence applies only to the pinned engine capability fixtures; F/H/I logical/schema tests have the bounded scopes stated above.

### 20.11 Security, Forget and Applied assessment

**Identity and Permission**

- B's formal ActorRef/ScopeRef/EnvironmentRef semantic mapping is a real B-domain decision; it does not approve I's trust policy or H's wire fields.
- I owns Principal trust, issuer/delegation, authorization, PermissionEpoch, revocation and global target policy.
- H must bind authenticated transport identity and signer/issuer evidence; payload ActorRef/ProducerId/ScopeRef is never credential proof.
- H's current identity-binding record says technical protocol binding is joint-decided, consumer-owner acceptance remains open, governance approval is blocked and H36 is NOT RUN.
- Exact H/I/C/B consumer schemas, issuer/audience/delegation behavior and stale-epoch negative tests remain prerequisites to freezing the public protocol.

**Forget and Anti-Resurrection**

- D's local ForgetFence and ProducerRegistrationHighWater are not I's ProducerDomainInventoryEpoch or target inventory seal.
- I's Global Forget Completion Evidence Vector must include D/E/F/G/H/C/Storage, backups, replicas, logs, exports, external recipients and model/provider onward copies as applicable.
- I's 25/25 global-Forget logical model tests passed (run `43962873109`); no real inventory seal, complete provider/recipient registry, target-bound deletion receipt, governance approval or physical erasure is established.
- F's 19/19 anti-resurrection reference model passed (run `43961714501`); actual F-RT index/ANN/cache/rebuild/reconnect tests remain NOT RUN.
- H's 11/11 schema tests passed (run `43962364955`); actual Adapter clear, per-region ACK, authenticated capability, duplicate-key and signature/channel-binding tests remain NOT RUN.
- Restore must be isolated and must replay current I/D policy/fence/retention state before any canonical or derived content becomes queryable.

**Applied**

Full Applied is not Delivery, Accepted, Materialized or local insertion success. It must bind G ContextVersion/Delivery, C's exact immutable final inference request and submit evidence, H Adapter instance/capability epoch, I PermissionEpoch and D ForgetFence. No model attention/comprehension claim follows from Applied. The actual final-submit hook and independent verifier are not demonstrated; no Full Applied production claim is accepted.

**Prompt injection**

Memory, evidence, provenance, summaries and retrieved content remain untrusted data. Region formatting alone cannot guarantee that an LLM ignores malicious instructions. C/H must prove protected-region integrity and I must own threat/risk acceptance. Retrieval poisoning, provenance/summary laundering, cross-scope injection and tool-authority escalation tests remain NOT RUN.

### 20.12 Protocol and compatibility assessment — COC / JF-10

The COC architecture must preserve the separation of authority:

- COC orders and durably accounts for participant observations; it does not authorize I, establish D fence effectiveness, decide Storage visibility, prove C provider success or certify G Applied.
- I owns PolicyDomainRef, CommitAuthorizationReceipt consumption, PermissionEpoch, revocation order and terminal authorization decision.
- D owns ForgetFence, lineage, producer barrier and CanonicalSuppressionComplete.
- Storage owns the exact prepared participant/XID, VisibilityPointer and PublicationReceipt.
- C owns provider-side-effect admission and immutable CSubmitOutcome.
- H transports authenticated evidence; it cannot mint owner outcomes.
- UNKNOWN/IN_DOUBT is durable and blocking. No TTL, timeout, missing row, lost ACK or operator force-clear may infer terminality.
- The accepted JF-10 architecture profile is limited to one I PolicyDomain. Multi-PolicyDomain atomicity remains BLOCKED.

**Exact-version warning:** the older COC protocol Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` has design-level owner acceptance with enumerated exceptions, recorded in A's acceptance matrix Blob `9a39e48a394fedbab16d15589056d59ef33f390f`. The current Storage protocol Blob is `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`. The Storage branch explicitly records the amended Blob as published / focused exact-owner re-review required / not yet accepted overall. Prior acceptance of 4ac63ac does not transfer to 86ff3b.

Storage's PostgreSQL 18.7 capability dossier records 7/7 CI workflows for the pinned profile. Gate A nevertheless remains PARTIAL PASS / OPEN because production runtime/DB adapter, actual I/D control-ledger integration, infrastructure fencing/failure-domain durability, operator/runbook and RPO/RTO remain unverified. Gate B design acceptance of the older protocol is not Gate C implementation/fault-injection PASS. JF-10 P0 remains OPEN; production activation is not authorized.

The amended COC review must explicitly close:
1. Recovery Cutoff Batch completeness and manifest ordering before immutable batch commit.
2. Owner-local admission gate ordering with I revocation and D fence requests.
3. C provider-side-effect admission and recovery enumeration.
4. PreparedParticipantReceipt/GID/XID/digest/database identity and single-use I authorization binding.
5. Same-XID forward/rollback recovery and Storage-only visibility proof.
6. COC prefix/quorum/restore proof and owner receipt reconciliation.
7. Exact schema/IDL, canonical bytes, duplicate-key rejection, signature/channel binding and cross-language interoperability.

### 20.13 Blocking findings

| Finding | Severity | Accountable owner(s) | Current state | Closure evidence |
|---|---|---|---|---|
| TAR-A-P0-001 — Fact/Claim canonical identity and semantics | P0 | B + Architecture Governance; D/E/F/G consult | ADR-001 explicitly ADR-BLOCKED | Formal approved/rejected ADR with named decision authority; synchronized consumer mappings and schema vectors |
| TAR-A-P0-002 — Producer Admission / Fence / Dependency / Publish linearization | P0 | D + E + Storage; F/G consume; I governs | Design semantics advanced; implementation boundary unproven | One authoritative callable gate/transaction contract; race interleavings; crash/restart; no late publication after barrier closure |
| TAR-A-P0-003 — JF-10 same-XID cross-authority recovery | P0 | I + Storage + D + C; COC coordinates; H transports | Single-domain design only; application integration NOT RUN | I sequencer and exact owner-final-gate receipt; Storage prepared XID and same-XID recovery; D ledger/fence; C provider boundary; failover/restore tests |
| TAR-A-P0-004 — I Global Forget inventory/seal/completion | P0 | I; D/E/F/G/H/C/Storage provide target evidence | Logical model 25/25 PASS; real inventory and global completion OPEN | Real ProducerDomainInventoryEpoch and TargetInventorySeal; complete target registry; per-target receipts; restore/external-copy evidence; governance approval |
| TAR-A-P1-001 — Identity and Permission binding | P1 | B/I/H/C/E; all consumers | Semantic/technical progress; governance and consumer execution open | Exact typed binding profile; issuer/delegation; transport authentication; PermissionEpoch/revocation negative tests |
| TAR-A-P1-002 — Full Applied proof | P1 | C/G/H/I/D | Contract concepts align; common exact proof/runtime not verified | Final-submit Agent hook; exact request tuple; independent verifier; lost ACK/stale version/Forget race tests |
| TAR-A-P1-003 — F Index/Cache anti-resurrection | P1 | F + D/E/I; G/H consumers | 19/19 logical model PASS only | Actual FTS/ANN/cache/rebuild/concurrent fill/offline/reconnect and restore tests |
| TAR-A-P1-004 — COC amended exact-version acceptance | P1 | Storage + A/I/D/C/H/E/G/B | 86ff3b published; focused exact-owner re-review pending | New exact-Blob owner acceptance matrix for amended bytes; no acceptance inheritance from 4ac63ac |
| TAR-A-P1-005 — Schema/transport/cryptographic interoperability | P1 | H + I + C | 11/11 schema fixtures PASS; parser/signature/channel/SDK tests open | Normative IDL/schema; canonical parser; duplicate-key/unknown-critical rejection; signed vectors; cross-language HTTP/IPC tests |
| TAR-A-P1-006 — Prompt injection and protected-region integrity | P1 | I + C + H; F/G/E contribute | Design boundary only | Adversarial fixtures and before/after protected-region/tool-policy digest evidence |
| TAR-A-P1-007 — Resource and performance envelope | P1 | A + D/E/F/G/H/C + Engineering | NOT BENCHMARKED | Reproducible corpus/hardware/workload benchmark and approved SLO/RTO/RPO |
| TAR-A-P1-008 — Blob/DB/backup/migration integration | P1 | Storage + D/E/I | Engine capability only; app boundary open | Blob visibility/orphan/digest, backup/PITR, stale restore quarantine, migration interruption and disk-full tests |

### 20.14 ADR and formal decision register

| Decision | Owner | Current status | Required next action |
|---|---|---|---|
| ADR-001 Fact/Claim canonical model | B + Architecture Governance | ADR-BLOCKED | Obtain explicit governance decision; no dependent schema freeze |
| ADR-TEC-001 database and transaction model | D + Storage; A coordinates | OPEN | Compare SQLite and PostgreSQL with the same application transaction/race harness; decide production profile only after proof |
| ADR-TEC-002 canonical persistence, outbox and blob layout | D/E/Storage | OPEN | Prove atomic acceptance, cursor, outbox, blob visibility, recovery and backup |
| ADR-TEC-003 lexical engine | F | OPEN | FTS5/Tantivy corpus benchmark |
| ADR-TEC-004 vector index/hybrid retrieval | F | OPEN | Compare ANN candidates after corpus/embedding profile is fixed |
| ADR-TEC-005 embedding/reranker backend | E/F | OPEN | Model compatibility, quality, CPU/GPU and memory benchmark |
| ADR-TEC-006 local generative inference/GPU scheduling | E/C + A | OPEN | Target model/quant/context/concurrency benchmark and OOM/fallback tests |
| ADR-TEC-007 BMCP encoding/transport/schema compatibility | H + I/C/G | OPEN | Exact owner field map, JSON/JCS vs alternatives, authenticated interoperability vectors |
| ADR-TEC-008 observability/audit/diagnostics | I + A/Storage | OPEN | Audit integrity, minimization, retention and sensitive-data review |
| ADR-TEC-009 local deployment/process/upgrade model | A + C/H + Storage | OPEN | Modular monolith, inference worker, sidecar and COC topology/failure isolation prototype |
| ADR-TEC-010 backup/restore/encryption/key custody | I + Storage | OPEN | Key lifecycle, restore quarantine, Forget/revocation replay and recovery drill |
| I36-GOV-01..10 / global target inventory and policy exceptions | I + designated governance approvers | GOVERNANCE-BLOCKED | Name approvers, approve target inventory/seal and exception semantics |
| JF-10 single-policy-domain profile | I/D/Storage/C/COC | Design accepted with exceptions; runtime P0 OPEN | Implement and test exact I/Storage/D/C same-XID boundary; multi-domain remains blocked |
| COC current amended protocol 86ff3b | Storage + A/B/C/D/E/G/H/I | Focused exact-owner re-review pending | Review exact amended Blob and publish new owner matrix |

No database, protocol encoding, transport, model backend, key algorithm, COC consensus implementation or production topology is declared formally approved by this review.

### 20.15 Prototype and benchmark plan

Execute in dependency order; do not start by tuning latency while correctness gates are open.

**Gate 1 — Domain and identity**
- Resolve ADR-001.
- Publish typed-reference, issuer/delegation, Scope and PermissionEpoch golden vectors.
- Negative tests for forged ActorRef/ProducerId, wrong issuer/audience, stale PermissionEpoch and confused deputy.

**Gate 2 — Persistence and Forget linearization**
- Implement the D/E/Storage producer admission, fence, complete dependency registration and publication operation.
- Run exhaustive register-vs-fence and publish-vs-fence interleavings.
- Crash at every durable boundary; test lease expiry, stale worker, DLQ replay and lost registration/publication ACK.
- Prove canonical revision, CanonicalCommitCursor, lifecycle event, outbox, VisibilityPointer and PublicationReceipt atomicity.

**Gate 3 — JF-10 / COC**
- Exact-owner review amended COC Blob 86ff3b.
- Implement I sequencer receipt consumption, owner-local gates, COC durable quorum/prefix, participant registry, Storage prepared XID and same-XID recovery.
- Test Recovery Cutoff Batch completeness, owner high-water capture, PreparedParticipantReceipt/GID identity, commit/rollback/unknown, coordinator crash, quorum loss, old-primary fencing, promotion, restore and ACK loss.
- Keep UNKNOWN/IN_DOUBT private and blocking; no heuristic resolution.

**Gate 4 — Forget / Derived / Applied**
- Run end-to-end Forget against E queue/leases/DLQ, F SQL/FTS/ANN/cache/Working Sets, G snapshots/deltas/deliveries, H Adapter buffers, C final request, backup/restore and external recipient fixtures.
- Prove real target inventory seal and per-target evidence.
- Implement independent Applied verifier against final immutable Agent request and exact G/H/I/D binding.
- Run prompt-injection and protected-region integrity adversarial tests.

**Gate 5 — Performance and deployment**
- Benchmark 12 GB, 16 GB and CPU-only/offload profiles with exact model, quantization, context, batch and concurrency.
- Compare SQLite/PostgreSQL on identical D/E application fixtures; record commit contention, WAL growth/checkpoint, prepared-XID duration, backup/restore and recovery.
- Compare FTS5/Tantivy and vector ANN on identical labeled corpus; report filtered recall, p50/p95/p99, memory, update/delete and rebuild.
- Measure compiler peak RSS, queue age/depth, embedding latency, retrieval P95/P99, Context delivery/Applied lag, Forget suppression/completion time, SSD amplification and index rebuild.
- Establish explicit RTO/RPO, operator/runbook, failure-domain and migration acceptance.

Every test result must record commit SHA, Blob SHA, environment, command, fixture/corpus version, expected/actual result and CI artifact. Existing logical-model and engine-capability results must not be relabeled as application conformance.

### 20.16 Required remediation and exact execution order

1. **B + Architecture Governance:** resolve ADR-001; keep E neutral CandidateProposition/ExtractionIR until decision.
2. **I + B + H + C + E:** freeze exact authenticated Principal/ActorRef/ScopeRef/ProducerIdentity/PermissionEpoch mapping and consumer negative-test vectors.
3. **D + E + Storage:** implement and prove the single producer-admission/fence/dependency/publication serialization boundary; preserve D's per-authority global CanonicalCommitCursor semantics and synchronize E/F/G.
4. **I + Storage + D + C + COC:** exact-review current COC Blob 86ff3; close Recovery Cutoff Batch, Owner-local Gate, PreparedParticipantReceipt/GID, same-XID and final owner-gate semantics; keep JF-10 P0 open until application tests pass.
5. **I + all target owners:** complete ProducerDomainInventoryEpoch, TargetInventorySeal, target evidence mapping, backup/external recipient governance and explicit Unknown/PolicyException handling.
6. **F:** execute real index/cache anti-resurrection, Scope-before-candidate, watermark gap/rebuild and concurrent fill tests.
7. **C + G + H + I + D:** converge one exact Applied proof profile and implement final-submit hook/verifier, offline reconnect and revocation/Forget races.
8. **Storage + D/E/I:** integrate blob, DB, WAL/PITR, migration, backup/restore quarantine and current control-ledger replay.
9. **H + C:** complete canonical parser/signature/channel binding, generated IDL/SDK and cross-language HTTP/IPC interoperability.
10. **I + C + H + F/G/E:** run prompt-injection, provider residency/retention, external-copy and security adversarial suite.
11. **Engineering + all Owners:** complete representative resource/performance benchmarks and set measurable SLO/RTO/RPO.
12. **A:** refresh all branch refs and exact artifacts again; run a second system integration review; request formal governance approval only after every P0 is closed and P1s are closed or explicitly accepted with bounded exceptions.

### 20.17 Exact live Commit and Blob SHA evidence

**Live refs resolved during this review**

| Ref | Exact HEAD |
|---|---|
| main | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` |
| A | `a4081392ca4863e9745ee7c166b099d6f7b151b9` |
| B | `310f305575d6f406e80d5d6ebf951bcd9e79e35f` |
| I | `73a0bff13b531b5b9feaeeec1887db31d6266589` |
| D | `a3ea0de75ca7b2297589293ec142f2cb07757282` |
| E | `5fb76b666fac49ceeb51ddb7c320fe5975313d99` |
| F | `e4c26214b8f78169c0e20f1faae23f945c3afeb9` |
| G | `b0c515399c6a336dcbf17a1ced6925413c804d5c` |
| H | `b99e5ead283dd1dcc3e86a4da871356731e162dc` |
| C | `018de5044810e755d4e21cb21e982526c27eb9a8` |
| Storage | `337fe8bffa178e64ad8e4750f1ede1d561424edc` |

**Main baseline and integration reports**

| Artifact | Blob SHA |
|---|---|
| TAB-001 blueprint | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` |
| TAR-AI-001 review task pack | `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` |
| Architecture Roadmap | `29289361973ec4369f067706132190793cd57a6b` |
| Phase 2 reconciliation | `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7` |
| Phase 3 D/E/H/I review | `edaccb802e0425f2d47bd4b613fab4dfde107144` |
| Phase 3 remediation task pack | `7abe73e5209ee985c9807b95d99616069911a6b7` |
| Phase 3.6 A final architecture acceptance | `16f86859645447f3f4397c5c89c6013c3cce92b5` |
| A COC older-version acceptance matrix | `9a39e48a394fedbab16d15589056d59ef33f390f` |

**Owner technology report blobs**

| Owner | Blob SHA |
|---|---|
| B | `fd3e5723b81de10bed806896e4be71ceb7a1669b` |
| I | `592baa4653e91287678a1e0926119ca94780bc08` |
| D | `97c049050d67dd12e0c64ef49b2b05795651608c` |
| E | `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8` |
| F | `124cc9300442b0e3a1e83603910e1c332b4fae48` |
| G | `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613` |
| H | `c003e6cc078fc58d6c150d0fb418c28f94de8e8a` |
| C | `ee42c7192561261789a0c7b5bd16d32c0eaaf14c` |

**Controlling domain, security, Storage and test evidence**

| Artifact | Blob SHA / CI evidence |
|---|---|
| B ADR-001 Fact/Claim canonical model | `df77e4a93cb8fef689ae7c828888d960cbf381d6` |
| B Actor/Scope/Environment semantic confirmation | `3a1e77889cd9a90cd5822d9f0cb3437880868706` |
| I Global Forget inventory contract | `9100061fa986fb6676656169de3fcf9fc1c72664` |
| I Global Forget reconciliation | `b6a34bf28b9f68453c93d7548f731677e1728b19` |
| I PermissionEpoch confirmation | `bae6a24fe3a374bc816993979a8fa9af52517dea` |
| I JF-10 v2 disposition | `8069ff86988396442c8d9dc3fd58653683abe2f3` |
| D joint Forget linearization decision | `1b6a312ecffd3947bbb4df59f902242482c98a40` |
| D publication gate | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| D JF-10 cross-authority recovery protocol | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` |
| E producer publication conformance contract | `a17f065e69e809fceacb51873d6a36a8b0f5c235` |
| F anti-resurrection evidence | `15049d448ace5ad24a6c02eba3fc906fcac149f6`; run `43961714501`, 19/19 PASS |
| H JF-10 schema evidence | `318c433d5b96966ecd47e6d1b265a0b12b28e581`; run `43962364955`, 11/11 PASS |
| Storage COC current amended protocol | `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` |
| Storage PostgreSQL 18.7 capability dossier | `0aabf66848dc97deee028c571183c0d7204008c0` |
| Storage realization review | `107d21bd2c604ee0b04feff2ee5580e1de9c7fce` |

### 20.18 Final system verdict

**BLOCKED — TAB-001 IS NOT READY FOR FORMAL APPROVAL OR FREEZE.**

What is complete:
- All eight Owner technology reports are present and version/blob-verified at live branch refs.
- Phase 2 and Phase 3 integration reports have been read and reconciled.
- The modular Rust/local-first architecture direction and owner authority boundaries are sufficiently coherent to continue engineering planning.
- PostgreSQL 18.7 has bounded prepared-XID capability evidence in the pinned CI profile.
- F logical anti-resurrection, I logical Global Forget and H schema-structure test suites have their stated bounded PASS results.
- The older COC protocol revision has design-level owner acceptance with explicit exceptions.

What is not complete:
- ADR-001 and other owner/governance decisions remain open.
- D/E/Storage atomic producer/fence/dependency/publication implementation is not verified.
- JF-10 same-XID cross-authority application integration is P0 OPEN.
- Global Forget inventory/seal/target completion and physical-erasure evidence are open.
- C/G/H Applied final-request runtime proof is not verified.
- Current amended COC Blob 86ff3 has not inherited the older 4ac63ac owner acceptance.
- No application-level resource/performance benchmark or integrated failure/security conformance has passed.

**TAB-001 must remain CANDIDATE. Do not mark FROZEN, APPROVED or production-ready.** The next phase is controlled owner remediation and executable engineering validation in the exact sequence in §20.16. A will perform a fresh integration review only after the evidence package is complete.

## 21. Latest exact-owner protocol, restore and logical-model evidence (2026-11-17)

### 21.1 Amended COC protocol §14 — exact owner review now complete

The current Storage COC protocol Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` and A prepared-participant mapping Blob `a71251704851cacd15f67faa985a5bd50057e92a` have now been reviewed by all B/C/D/E/G/H/I/A/Storage owner perspectives. Exact matrix: `reviews/integration/phase-3.6.4-jf10-prepared-participant-gid-owner-acceptance-matrix.md`, Blob `dd7f00945b362b8d71b91d007e0335a8cffd96c2`.

The accepted type split is PreparedParticipantRef (stable engine-neutral identity), PreparedTransactionGID (client-chosen PostgreSQL prepared handle, bound before COC intent), and EngineNativeTransactionXIDRef (observed after PREPARE). Storage PREPARE is prohibited until the exact COC intent is committed. The H 1.1.1 candidate schema Blob is `c0bbfc7611a8d88a39cee209831db32b62601fde`.

**Gate B amended §14 status: DESIGN-LEVEL EXACT OWNER ACCEPTANCE COMPLETE WITH CONDITIONS.** This supersedes §20.18's statement that Blob `86ff3...` had not inherited owner acceptance from the older `4ac63...` revision. It does not close implementation P0 or Gate C.

### 21.2 Restore control-high-water architecture — all owner perspectives accepted

The exact Storage restore contract Blob `4f656163aeba532a441eaed1d293a48e2363cb4a` has been accepted by A/B/C/D/E/F/G/H/I/Storage. Exact matrix: `reviews/integration/phase-3.6.5-restore-highwater-owner-acceptance-matrix.md`, Blob `3b488ae3a7cf9aca9a70a659aba09ecba53ce17f`.

Accepted proof boundaries: COCCommittedPrefixProof; per-PolicyDomain IControlHighWaterProof; per-ForgetOperation DForgetControlHighWaterProof; StorageParticipantLedgerProof; and Storage RestoreReconciliationReceipt in state RECONCILED_BUT_FENCED. The receipt is not permission to serve, I authorization, D clearance, Global Forget completion or physical-erasure proof.

Storage Gate A architecture design is now **CONDITIONAL PASS** because its restore proof shapes, authority boundaries, fail-closed behavior and high-water recheck order have exact owner acceptance. Storage implementation/deployment readiness remains NOT PASSED / DEFERRED. This is a sub-gate result, not a system verdict.

### 21.3 New executable evidence

| Area | Exact CI evidence | Result | Boundary |
|---|---|---|---|
| F Anti-Resurrection | Run `43961714501`, job `133630540252`; model Blob `33fa2ca2dc29771aca241e194f13e078a4f8d774`; tests Blob `c2575327a75577923440ef770d42122218a1e091` | **19/19 PASS** | Logical model only; actual ANN/index/cache/Working Set runtime remains untested. |
| I Global Forget inventory/CEV | Run `43963450717`, job `133636592112`; model Blob `5233da028e409ec3f41848582dad73a923e7155b`; tests Blob `428e15c6263b5b2d730b93ce5412d55e782a449b` | **30/30 PASS** | Logical model only; no production inventory seal, external deletion, governance approval or physical erasure. |
| H BMCP JF-10 schemas/parser | Run `43964080044`, job `133638783610`; schema 1.1.1 Blob `c0bbfc7611a8d88a39cee209831db32b62601fde`; evidence Blob `d7652727e21c2f88d6cc2481deeeca96c2efd38f` | **34/34 PASS** | Schema/parser reference tests only; no production signatures, channel binding, replay, SDK or live transport. |
| Storage restore high-water | Run `43965501810`, job `133643756066`; model Blob `be0aef6232c8ee2ed6179df7b0a74473c3e25b3b`; tests Blob `a9e1a96b449c6bf0e2b52c5fea394a8c32961a24`; evidence Blob `bf991a8a098bfdacc24bace53d452b8ccf2078e6` | **25/25 PASS** | In-memory model only; no real backup/WAL restore, signed proof APIs, old-primary fencing or measured RTO. |

### 21.4 Updated blocking register

- A-TAR-P0-002 Fact/Claim ADR-001: **OPEN / P0**; no formal Architecture Governance approval.
- A-TAR-P0-003 JF-10 atomic registration/fence/dependency/publication: **DESIGN ACCEPTED / IMPLEMENTATION P0 OPEN**. Amended §14 exact-owner review is complete.
- A-TAR-P0-004 Global Forget: **OPEN / P0**. I's 30-test model passes; real global inventory/seal, target evidence, external deletion, production restore and physical-erasure proof are absent.
- A-TAR-P1-003 Anti-Resurrection: **LOGICAL MODEL PASS / RUNTIME OPEN**.
- A-TAR-P1-005 BMCP JF-10 schema: **1.1.0/1.1.1 schema and parser reference PASS / PRODUCTION INTEROPERABILITY OPEN**.
- Storage Gate A architecture design: **CONDITIONAL PASS**; implementation/deployment NOT PASSED.
- I36-GOV-01..10: **GOVERNANCE-BLOCKED / NOT APPROVED**. The conservative decision proposal is not an approval.

### 21.5 Current Owner branch/report manifest

| Owner | Current branch HEAD | Current report/readiness Blob SHA |
|---|---|---|
| A | `78dd8c5cb44b8f50f06504ef6fc6a7523aa074d5` | `56d238fa236c2f5089eb98e8bff8363e47e73748` |
| B | `e79ff629af3656e055a7ce10cc7b9fea468cf84f` | `fd3e5723b81de10bed806896e4be71ceb7a1669b` |
| C | `c408d2c138d1975eff1167bd5889ba45a13b126b` | `ee42c7192561261789a0c7b5bd16d32c0eaaf14c` |
| D | `f5cbe59561b73c75708a52f28b0bf12707d75c71` | `97c049050d67dd12e0c64ef49b2b05795651608c` |
| E | `fb063e15ee31569e501f5fa0a3198b3cf0b67a9c` | `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8` |
| F | `86c013814fbbfff1829729eb18fdc3a5de265969` | `124cc9300442b0e3a1e83603910e1c332b4fae48` |
| G | `466e2bf5992ea5944ef6ecebd79a39eeb21cdc97` | `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613` |
| H | `a5fe5268fe846f2ec3c94448bda5592783ef7212` | `cb9d1d97604bdb71bc2f5bf47f6392e03f30ba99` |
| I | `d66361dd88f07278340663b75bcb22e040d96965` | `c24f03aae6ce7bc76eaeb1ed33bb24fb7fcac624` |
| Storage | `ec1a8bbbba53c67766e2eb415854dbc9bf9057ca` | `555844c93da2dd255f042c8bf4cd874cb0af076c` |

### 21.6 System verdict remains BLOCKED

The new exact-owner and logical-model evidence closes specific design-review gaps only. It does not justify system-level approval or freeze. **Final verdict remains BLOCKED — TAB-001 IS NOT READY FOR FORMAL APPROVAL OR FREEZE.** TAB-001 remains CANDIDATE / NOT FROZEN; JF-10 runtime P0 remains open; Global Forget is NOT COMPLETED; production activation is NOT AUTHORIZED.
## 22. ADR-001 decision-readiness package prepared — approval remains blocked

A consolidated decision/impact package is now available at `reviews/integration/phase-3.6.6-adr001-decision-readiness-and-impact-package.md`, Blob `3ddb18580563ac12607bd384d6d2b0930c5f0ff5`.

A recommends Option A as the preferred candidate because it preserves the current governance distinction between Fact and Claim and provides an auditable independent-attestation object linked to exact immutable ClaimRevisionRefs. This is explicitly a recommendation, not an approval. Option B remains a viable alternative only if Architecture Governance explicitly amends I-04/P-04/README and terminology.

The package records the exact B/D/E/F/G/H/I/C impacts, migration requirements, 15 consumer conformance scenarios and the formal approval evidence required. No named Architecture Governance authority or approver is currently recorded. A cannot self-approve ADR-001.

**ADR-001 remains ADR-BLOCKED.** No canonical FactRef, Fact schema, API, wire field or production migration is frozen. Neutral CandidateProposition/ExtractionIR and Evidence/Provenance work may continue; canonical Fact/Claim identity remains blocked.

The system verdict remains **BLOCKED — TAB-001 IS NOT READY FOR FORMAL APPROVAL OR FREEZE**. Storage Gate A's conditional design pass and exact COC/restore owner acceptances do not override ADR-001, I36 governance, Global Forget or JF-10 runtime blockers.

## 21. Phase 3.8.2 cross-owner freeze readiness refresh / Phase 3.8.2 跨 Owner 冻结准备复核

A has completed a fresh I/H/C/Storage evidence reconciliation. The controlling report is:

- `reviews/freeze-readiness/final-cross-owner-freeze-readiness.md`
- Blob: `7f65f0db36f879a709869b27aa4c1913eaed9428`
- Decision: **BLOCKED — NOT FROZEN**.

Latest H RecoveryJoin/HRC/WIRE/SCHEMA candidate CI [44042093922](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44041359883) passed 66/66; I Global Forget logical model 30/30 and Storage restore high-water logical model 25/25 remain bounded model results. These do not close I production trust/sequencer, C provider adapter/Applied, Storage physical D/Storage topology, or integrated JF-10/COC runtime. TAB-001 remains CANDIDATE / NOT APPROVED / NOT FROZEN. No mainline merge or production activation is authorized.

中文：A 已完成 I/H/C/Storage 新一轮证据校准。最新 H 候选套件 66/66 通过，I Global Forget 逻辑模型 30/30、Storage Restore High-water 逻辑模型 25/25 通过；这些都不是生产实现验收。I 信任/Sequencer、C Provider/Applied、Storage 物理拓扑、集成 JF-10/COC Runtime 仍阻断冻结。TAB-001 维持候选、未批准、未冻结；不授权合并主线或生产激活。
