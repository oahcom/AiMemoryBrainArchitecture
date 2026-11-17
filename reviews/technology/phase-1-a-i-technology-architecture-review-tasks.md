# Phase 1 — A–I Technology Architecture Blueprint Review Tasks

- Document ID: TAR-AI-001
- Version: 1.0
- Date: 2026-11-17
- Repository: oahcom/AiMemoryBrainArchitecture
- Blueprint: 13-engineering-decisions/technology-architecture-blueprint.md
- Blueprint: TAB-001 v0.1; task-creation blob SHA 7b6f2d139217dbe13ab3a3af31bfbff525f20e71
- Status: REVIEW TASKS — NOT OWNER ACCEPTANCE, NOT ADR APPROVAL, NOT IMPLEMENTATION EVIDENCE

## 1. Objective

Run nine independent, owner-scoped technical architecture reviews of TAB-001. A, B, C, D, E, F, G, H, and I must each examine the system-wide blueprint from their own authority boundary and submit a separately versioned review conclusion on their own existing owner branch.

The goal is to establish whether the proposed technology architecture is technically viable, complete, internally consistent, resource-feasible, recoverable, and compatible with the owner’s logical contracts. The goal is not to force all owners to accept the same stack, nor to convert recommendations into decisions without evidence.

**C is explicitly included as a full review owner.** C must review Agent integration, telemetry, Adapter deployment, inference-boundary integration, Context application and Applied attestation. C is not merely a consulted stakeholder.

## 2. Mandatory source refresh

Every owner session must begin by refreshing:

1. main:13-engineering-decisions/technology-architecture-blueprint.md
2. main:ARCHITECTURE_ROADMAP.md
3. main:reviews/integration/phase-3-session-kickoff-prompts.md
4. main:reviews/integration/phase-2-defg-cross-session-reconciliation.md
5. main:reviews/integration/phase-3-defghi-cross-module-contract-review.md
6. The owner’s current branch HEAD and all owner-owned design, decision, review, and change-log artifacts.
7. Relevant upstream/downstream owner artifacts identified by the task.

The blueprint SHA above is the task-creation baseline only. If main has advanced, review the current main version, record both the task baseline and the actual reviewed blob SHA, and identify material changes. Do not review a stale local copy.

Refresh the owner branch HEAD immediately before writing. Do not overwrite or revert newer work. If the branch contains later decisions, consume them and cite exact paths and commit/blob SHAs in the report.

### Known owner branches

| Owner | Branch |
|---|---|
| A | session-a-integration-2026-11-16 |
| B | session-b-domain-model-phase3 |
| C | session-c-agent-integration-2026-11-16 |
| D | session-d-memory-brain-2026-11-16 |
| E | session-e-memory-compiler-2026-11-16 |
| F | session-f-memory-runtime |
| G | session-g-memory-context |
| H | session-h-bmcp-protocol |
| I | session-i-security-governance-2026-11-16 |

If a named branch is absent or renamed, stop and report the exact observed state. Do not create a replacement branch or write to main as a workaround.

## 3. Common review requirements — all owners

Each owner must independently assess all six dimensions below. A dimension may be marked NOT APPLICABLE only with a reason tied to the owner’s actual boundary.

### R1 — Technical requirements and workload fit
- Identify functional, non-functional, consistency, security, latency, throughput, availability, durability, and operability requirements.
- Map each requirement to a component, interface, technology capability, and verification method.
- Identify omitted requirements, assumptions, and unquantified requirements.
- Distinguish hard invariants from performance preferences.

### R2 — Component dependencies and boundaries
- Check upstream/downstream dependencies, ownership, authority, and data flow.
- Identify cyclic dependencies, duplicate authority, hidden shared state, implicit synchronous coupling, and missing interfaces.
- Verify that logical components are not incorrectly equated with crates, processes, services, or databases.
- Identify dependencies that could make optional inference, indexing, or Adapter availability block correctness-critical paths.

### R3 — Candidate technology selection
For every relevant candidate named in TAB-001:
- Assess fitness for the actual workload and contract semantics.
- Identify alternatives and comparison criteria.
- Assess ecosystem maturity, Rust integration, platform support, licensing/operations, persistence semantics, migration path, and lock-in.
- Mark each technology as recommendation, candidate, unresolved decision, or already-decided project constraint.
- State what evidence is needed before selection.

Do not approve a technology merely because it is named in the blueprint. Do not introduce a new dependency without explaining why existing candidates are insufficient.

### R4 — Resource constraints
- Review CPU, host RAM, GPU VRAM, disk, I/O, concurrency, queue, cache, index, and model assumptions relevant to the owner.
- Explicitly account for the 12–16 GB VRAM planning envelope.
- Identify peak-memory, burst, contention, backpressure, and resource-exhaustion risks.
- Give measurable sizing formulas or workload dimensions where exact numbers are unavailable.
- Separate estimates from measured data. No invented benchmarks or SLOs.

### R5 — Failure recovery and operational safety
Review process crash, host restart, partial writes, database unavailable, disk full, worker lease expiry, retries, duplicate delivery, stale replay, index rebuild, cache invalidation, model OOM/unavailable, Adapter offline/reconnect, backup restore, and upgrade/migration as relevant.

For each critical transition, state durable authority, linearization/commit point, idempotency and retry behavior, recovery source of truth, fail-open/fail-closed behavior, observability/operator evidence, and required fault-injection tests.

### R6 — Interface and compatibility
- Verify compatibility with current owner contracts and adjacent owner interfaces.
- Identify wire/schema/version/cursor/epoch/identifier mismatches.
- Distinguish transport identity from payload claims.
- Identify forward/backward compatibility and rolling-upgrade concerns.
- Do not reinterpret CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark, ContextVersion, PermissionEpoch, ProducerDomainInventoryEpoch, and ForgetFenceGeneration as interchangeable.

## 4. Project-wide constraints to preserve

Every owner must explicitly assess the impact of these constraints:

1. Brain remains Agent- and model-independent; it does not become an Agent planner or tool executor.
2. Canonical Memory, Memory Context, and Applied Context are separate authorities/states.
3. Accepted Event, compiled Candidate, Canonical Commit, indexed representation, delivered Context, and Adapter Applied are distinct states.
4. Model output is a proposal, not Canonical Truth.
5. Scope and Permission are separate; untrusted memory/evidence/summaries are data, not instructions.
6. Durable ingress and canonical recovery cannot depend on an LLM being available.
7. Indexes and caches are derived, rebuildable, and cannot override canonical authority or Forget suppression.
8. Forget must prevent replay, recompile, late derivative publication, index rebuild, Context delivery, Adapter reconnect, and backup restore from resurrecting forgotten content.
9. D’s selected semantic decision is one globally ordered CanonicalCommitCursor per Canonical Memory Authority. Other revisions, cursors, epochs, and generations remain separate typed namespaces. Storage realization and crash recovery still require evidence.
10. D/E/Storage producer admission versus Forget fence installation, dependency registration, and publication gate remain open until a concrete atomic/linearizable operation contract and race/fault tests exist.
11. B’s Fact/Claim ADR remains ADR-BLOCKED unless a current formal governance decision is found. Do not infer approval from an owner preference.
12. H owns BMCP normative wire/protocol decisions; I owns security/governance policy; C owns Agent integration requirements and Adapter-side conformance; G owns Context version/change/delivery authority; F owns retrieval/runtime activation; D owns Canonical Memory authority; E owns compilation and staged derivative workflow.
13. TAB-001 is a candidate blueprint, not a technology freeze. Owners may accept, conditionally accept, reject, or request changes to individual recommendations without changing unrelated decision statuses.

## 5. Owner-specific assignments

Each owner completes R1–R6 and the additional scope below.

### A — System Architecture and Integration Owner
- Branch: session-a-integration-2026-11-16
- Report: reviews/technology/owner-a-system-technology-architecture-review.md

Review TAB-001 as the system integration authority.
- Validate that technology layers, component boundaries, data flows, process topology, crate map, and decision register cover the system without gaps or duplicate ownership.
- Check that technology choices support cross-module invariants and do not prematurely freeze open contracts.
- Review dependency direction across A–I and missing cross-cutting interfaces: identity context, authorization, idempotency, transaction/outbox, typed cursors, Forget evidence, audit, and observability.
- Reconcile TAB-001 with roadmap, Phase 2 reconciliation, Phase 3 task pack, and latest D/E/H/I review.
- Review ADR ordering/dependencies.
- Assess modular-monolith, embedded-database, isolated-inference-worker, and future multi-process evolution risks.
- Produce a system-level dependency map and owner-by-owner technology decision matrix.
- Explicitly verify that C’s Agent Integration responsibilities are first-class architecture concerns.

Required conclusion: Is TAB-001 complete enough as a candidate system technology baseline? Which choices can remain recommendations, which require ADRs, and which are blocked by domain contracts? What cross-owner reviews and prototypes must precede baseline approval?

### B — Domain Model Owner
- Branch: session-b-domain-model-phase3
- Report: reviews/technology/owner-b-domain-model-technology-review.md

Review whether the stack can represent and preserve the domain model without semantic loss.
- Typed IDs, Entity, Relation, Event, Memory, Fact, Claim, Evidence, Provenance, ConflictSet, ScopeRef, ActorRef/Principal references, environment namespace, temporal fields, epistemic status, lifecycle state, confidence, and relevance.
- SQL relational representation versus JSON/document payloads, normalized tables, immutable revisions, schema evolution, constraints, and referential integrity.
- Serde, JSON, CBOR/MessagePack candidates, protocol mapping, and migration implications.
- Whether indexes preserve identity, scope, temporal, epistemic, and lifecycle distinctions.
- Provenance graph storage, cycle policy, entity merge/split history, and immutable source references.
- Explicitly preserve the unresolved Fact/Claim ADR. Assess technology implications of plausible alternatives without choosing the ADR by implication.
- Identify property tests, schema round-trip tests, migration tests, and malformed/untrusted input tests.

Required conclusion: Can persistence and serialization faithfully encode the domain model? Which types or constraints are underspecified? Which technology decisions depend on Fact/Claim or typed-reference semantics?

### C — Agent Integration Owner — mandatory independent review
- Branch: session-c-agent-integration-2026-11-16
- Report: reviews/technology/owner-c-agent-integration-technology-review.md

Review from the Agent/Adapter and inference-boundary perspective. C is a full owner deliverable, not a secondary consultation.
- Adapter deployment options: embedded SDK/library, sidecar/local process, remote gateway client, and compatibility across Agent frameworks/languages.
- BMCP client integration, transport, authentication binding, reconnect, capability/version negotiation, timeout, retry, backpressure, and offline behavior.
- Telemetry: Task State, Intent, Plan Summary, Active Entities, Tool Call/Pending Action, Observation, Outcome, Uncertainty, Risk Signal, Environment Delta. Plans/intents must not become completed outcomes; telemetry gaps must remain uncertainty.
- Tier 1 inference-boundary integration: obtain Brain-managed region, stage Add/Update/Remove, apply exact Context version to final inference request, and prove Applied at the agreed boundary.
- Tier 2 middleware and Tier 3 event/tool compatibility modes: document capability limits; they must not falsely claim Tier 1 semantics.
- Context isolation: Brain-managed memory must not overwrite System/Developer/User source text or bypass Agent safety policy.
- Prompt-injection containment, provenance traceability, token budgeting, context-window variation, tokenizer differences, and compaction.
- Bind Applied evidence to InferenceRequest, ContextVersion, Delivery, Adapter identity/capability epoch, PermissionEpoch, and ForgetFenceGeneration. Applied is not proof of model comprehension.
- Adapter SDK language support and Rust FFI/HTTP/IPC options; do not assume every Agent runtime is Rust.
- Define conformance fixtures for final-request observation, stale delivery rejection, offline reconnect, Forget suppression/clear, permission revocation, and model/provider change.

Required conclusion: Is the topology implementable across heterogeneous Agents? What integration boundary and evidence can C support? Which transport, SDK, and conformance choices remain open pending H/I/G? How will tests distinguish Applied from Delivered and model usage?

### D — Canonical Memory Brain Owner
- Branch: session-d-memory-brain-2026-11-16
- Report: reviews/technology/owner-d-canonical-brain-technology-review.md

Review persistence and technology choices for Canonical Memory authority.
- Canonical record/revision layout, immutable history, AggregateRevision, lifecycle events, per-authority CanonicalCommitCursor, and per-memory LifecycleEventCursor.
- SQLite WAL transaction/locking semantics against atomic canonical commit and cursor advancement.
- Compare PostgreSQL and embedded KV alternatives for transaction scope, concurrent writers, recovery, audit, migration, and local deployment.
- Producer registration, work-item admission, ForgetFence generation, dependency registration, staged visibility, publication gate, and barrier closure.
- Determine whether database abstraction can express a real linearization point rather than a read-then-write race.
- Outbox, replay, lease, recovery, transaction boundaries, and idempotency.
- Content-addressed blob references and integrity for immutable evidence/source artifacts.
- Backup/restore and canonical cursor continuity.
- Identify invariants requiring SQL constraints, unique indexes, transactions, locks, compare-and-swap, or another primitive.

Required conclusion: Can SQLite WAL plausibly implement D’s authority semantics and under what transaction/locking assumptions? Which operations need prototypes before database selection? Does TAB-001 distinguish semantic decisions from Storage implementation proof?

### E — Memory Compiler Owner
- Branch: session-e-memory-compiler-2026-11-16
- Report: reviews/technology/owner-e-memory-compiler-technology-review.md

Review ingestion, compilation, extraction, provenance, consolidation, and derivative pipeline.
- Durable Event acceptance, payload/blob registration, Accepted Receipt, idempotency scope, compile intent, transactional outbox, queue, work lease, retry, timeout, dead-letter, replay, and recompile.
- Database-backed worker queues versus external brokers. Do not introduce Kafka-class infrastructure without measured need.
- Deterministic normalization versus model-assisted extraction; provider abstraction for embedding, extraction, resolution, and summarization.
- CPU/GPU scheduling, batching, concurrency, model unavailability, rate limits, memory pressure, and retry policy.
- Staged invisible derivatives, durable provenance/dependency registration, D fence admission, final publication gate, and stale worker suppression.
- Model/version/tokenizer metadata and reproducibility.
- Blob staging, content-addressing, duplicate detection, partial-write recovery, and orphan cleanup.
- Conflict resolution and Canonical Memory handoff; Compiler must not declare Canonical Truth.
- Fault tests for crash between durable stages, duplicate ingress, lease expiry, retry after fence advancement, DLQ replay, and late derivative publication.

Required conclusion: Is durable outbox/DB-worker approach adequate for local deployment? Which transaction/queue semantics are underspecified? Which inference tasks should be async, optional, CPU-fallback capable, or isolated?

### F — Memory Runtime Owner
- Branch: session-f-memory-runtime
- Report: reviews/technology/owner-f-memory-runtime-technology-review.md

Review low-latency retrieval, ranking, activation, working sets, cache, and scheduling.
- Compare structured SQL, FTS5, Tantivy, embedded ANN/usearch, sqlite-vec, and optional reranking.
- Define workload-sensitive criteria: corpus size, scope selectivity, update/delete rate, top-k, recall quality, p50/p95/p99 latency, memory, disk, rebuild time, and complexity.
- Review hybrid retrieval/ranking order; authorization and Forget suppression precede ranking, reranking, summaries, and activation.
- Per-channel/per-partition IndexWatermark and relation to D CanonicalCommitCursor.
- Stale-index handling, rebuild, compaction, tombstones, partial channel failure, and safe fallback.
- Moka cache keys/invalidation across Scope, PermissionEpoch, ForgetFenceGeneration, canonical revision, and query semantics.
- Bounded working-set memory, token budget, eviction, and per-Agent/Session isolation.
- CPU/GPU contention if embedding/reranking shares a 12–16 GB GPU with local LLM.
- Determine whether vector search is needed in first vertical slice or should follow lexical baseline.

Required conclusion: Which channels enter first prototype and why? What evidence selects FTS5/Tantivy and vector index? Can watermark/cache/fence design prevent stale or forgotten candidate leakage?

### G — Memory Context Owner
- Branch: session-g-memory-context
- Report: reviews/technology/owner-g-memory-context-technology-review.md

Review Context planning, edits, versioning, reconciliation, delivery, and budget.
- Persistence for ContextVersion, ChangeSet, ContextEntry, snapshots, deltas, delivery attempts, ACKs, and reconciliation state.
- G remains sole Context version/change authority; F retrieval recommendations and H transport cannot become Context authority.
- Optimistic concurrency/base_version, idempotent edits, ordering, compaction, expiry, replacement, remove, and full-snapshot fallback.
- Delivery queue durability, stale/superseded deliveries, Adapter offline/reconnect, capability downgrade, and exact Applied evidence.
- Token budgeting across model context windows, tokenizers, managed-region limits, and safety headroom.
- Context rendering/encoding, untrusted-data isolation, source references through compaction, deterministic reconstruction.
- Forget invalidation of entries, snapshots, deltas, pending deliveries, and reconnect state.
- Concurrent Agent sessions and independent Contexts sharing canonical memory.
- Tests for version gaps, concurrent edits, duplicate delivery, lost/stale ACK, offline Adapter, budget overflow, and Forget during delivery.

Required conclusion: Does the design preserve one authoritative Context version sequence? What is durable versus recomputable? What exact Adapter evidence permits G to mark Applied?

### H — BMCP Protocol Owner
- Branch: session-h-bmcp-protocol
- Report: reviews/technology/owner-h-bmcp-technology-review.md

Review schema, encoding, transport, SDK compatibility, capabilities, and ACK evidence.
- Compare JSON, CBOR, MessagePack for evolvability, canonicalization, size, streaming, debugging, validation, and cross-language SDKs.
- Compare HTTP, local IPC (Unix sockets/Windows named pipes/loopback), and gRPC only against explicit interoperability/streaming needs.
- Version negotiation, unknown fields, required/optional fields, capability epoch, correlation, idempotency, replay, timeout, and retry.
- Principal/ActorRef/ProducerIdentity and PermissionEpoch must bind to authenticated transport/security context; payload identity is not proof.
- Typed cursor/epoch/generation serialization; avoid ambiguous generic integer fields.
- Delivery/ACK taxonomy: Applied, rejected, expired, superseded, suppressed, local buffer cleared, cache purged, queued delivery cancelled, failed, unknown, unsupported.
- C final-request Applied evidence and G Context authority.
- I per-target Forget evidence and capability mapping.
- Heterogeneous Agent languages and rolling protocol upgrades.
- Conformance vectors, malformed-message, downgrade, replay, and authenticated identity mismatch tests.

Required conclusion: Which encoding/transport should be prototyped first and what decides? Are BMCP contracts sufficient for C/G/I? Which fields or ACK claims must remain open?

### I — Security and Governance Owner
- Branch: session-i-security-governance-2026-11-16
- Report: reviews/technology/owner-i-security-governance-technology-review.md

Review security, authorization, revocation, retention, backup, erasure, and global Forget.
- Threat model across Adapter, Brain, IPC/network, database, blob store, model worker/provider, indexes, caches, logs, backups, replicas, external recipients.
- Principal authentication, issuer binding, delegation, ActorRef/ScopeRef, PermissionEpoch, policy caching, revocation, and reauthorization at protected boundaries.
- OS key store, encryption at rest, transport authentication, key rotation, backup encryption/recovery, and cryptographic erasure.
- Secrets, local file permissions, process isolation, least privilege, audit tamper evidence, and sensitive-data redaction.
- Data residency/provider policy for optional remote inference.
- Forget target inventory, producer-domain registration epoch, D work-item fence/barrier, E derivative registration, F index/cache suppression, G Context invalidation, H/C Adapter attestations, backups, restore, external recipients.
- Keep I producer-domain inventory epoch distinct from D work-item registration high-water mark and ForgetFenceGeneration; no numeric reinterpretation or cross-domain ordering.
- Global completion as typed evidence vector; unknown/unsupported/offline targets cannot silently count as success.
- Backup retention, restore suppression, deletion proof, legal hold/retention exception, physical erasure claims.
- Security tests: unauthorized scope probes, confused deputy, forged payload identity, stale permission epoch, replay after revocation, prompt injection, restore after Forget, log leakage.

Required conclusion: Is this defensible without overstating guarantees? Which primitives/key choices remain open? What target evidence and exception semantics are required before Global Forget can complete?

## 6. Required independent report format

Each owner creates exactly one primary report at the assigned path on their own branch. Include:

1. Metadata: owner, branch, reviewed branch HEAD, blueprint version/blob SHA, date, report version.
2. Executive verdict: PASS, CONDITIONAL PASS, REQUEST CHANGES, BLOCKED, or NOT REVIEWABLE.
3. Scope/evidence: exact files, paths, commits/blob SHAs reviewed; unavailable inputs.
4. Six-dimension matrix R1–R6, each with verdict, evidence, gaps, and impact.
5. Findings with stable IDs TAR-A-P0-001, TAR-B-P1-001, etc.; severity P0/P1/P2/P3; location, evidence, consequence, recommendation, owner, dependencies, closure test.
6. Technology disposition table: ACCEPT AS CANDIDATE, RECOMMEND, REJECT, DEFER, or NEEDS ADR. Never use APPROVED unless actual decision authority and governance record exist.
7. Resource assessment: known constraints, estimates, unknowns, sizing method, required measurements.
8. Failure/recovery matrix: failure, durable authority, recovery, expected behavior, test ID/proposed test.
9. Compatibility assessment: upstream/downstream owner, contract, compatibility status, unresolved mapping.
10. Required ADRs/prototypes/tests ordered by dependency and criticality.
11. Final recommendation: owner acceptance conditions and what must not be frozen.
12. No-claim statement listing implementation, security, performance, and physical-erasure validations not run.

Verdict rubric:
- PASS: no material owner-level gap; recommendations may proceed as candidates.
- CONDITIONAL PASS: direction usable, but named issues must close before affected decisions freeze.
- REQUEST CHANGES: material architecture changes required before owner acceptance.
- BLOCKED: unresolved upstream decision or missing evidence prevents meaningful conclusion.
- NOT REVIEWABLE: required sources unavailable or baseline cannot be established.

## 7. Evidence and writing rules

- Review independently; do not copy another owner’s verdict.
- Do not claim benchmark, test, deployment, or acceptance without evidence.
- Cite exact source path and commit/blob SHA for every material finding.
- Mark assumptions and inferred risks explicitly.
- Preserve dissent; do not force consensus by weakening findings.
- Do not silently modify TAB-001 or another owner’s artifacts.
- Describe exact proposed blueprint corrections; A coordinates any later revision.
- If another owner decision is required, create a dependency finding; do not decide for them.
- No branch merge, PR merge, or main write is authorized.
- Commit the report to the assigned owner branch. Fetch it back and verify path, content, blob SHA, and branch HEAD.
- A successful commit proves only report publication, not the verdict or implementation behavior.

## 8. Completion report to coordinator

Return owner and branch; reviewed branch HEAD and blueprint blob SHA; report path/blob SHA/commit SHA/URL; verdict; P0/P1/P2/P3 counts; top three findings and dependencies; recommended/rejected/deferred technologies; required ADRs/prototypes/tests; confirmation no other owner files or main were modified; and explicit statement of what was not tested.

## 9. Suggested execution order

1. B and I: domain/identity/security constraints.
2. D and E: persistence, transaction boundaries, compiler and Forget races.
3. F and G: retrieval/index/cache and Context/delivery.
4. H and C: wire/transport and heterogeneous Agent integration.
5. A: system synthesis after the other eight reports are available.

Reviews may run in parallel. If a dependency report is unfinished, record it OPEN and continue reviewable portions.

## 10. Overall acceptance rule

TAB-001 cannot become an approved technology baseline merely because nine reports exist. A must synthesize findings, resolve cross-owner conflicts, obtain required ADR decisions through project governance, and record exact approved versions.

At minimum, keep explicit blockers until evidenced:
- D/E/Storage atomic producer admission, Forget fence installation, dependency registration, and final publication gate.
- B Fact/Claim ADR and typed domain reference semantics.
- C/G/H final-request Applied proof and Adapter conformance.
- H/I/C authenticated identity and permission binding.
- I global Forget target inventory/evidence mapping and backup/restore suppression.
- F index watermark, cache invalidation, and anti-resurrection conformance.
- Measured database, index, model, VRAM/RAM, latency, throughput, and recovery characteristics.

**Final instruction to every owner:** Review the current TAB-001 blueprint against your own authoritative contracts, submit your own evidence-backed report on your own branch, and state plainly where the technology architecture is not yet decidable. Do not manufacture consensus or implementation evidence.


## Mandatory architecture delivery rule / 架构交付强制规则

This task is governed by GOV-DOC-BILINGUAL-001. The Owner MUST produce or update Chinese and English counterparts in the same change set for the review report and every architecture-significant proposal or specification changed during this task. Both versions must preserve the same findings, severity, verdict, evidence, open issues, and non-claims. Update docs/translation-status.md. A report with a missing or stale language counterpart is not a complete deliverable.

本任务受 GOV-DOC-BILINGUAL-001 约束。Owner 必须在同一变更集中为审查报告及本任务修改的所有重要架构提案/规范提供或更新中英文版本。两种语言必须保持相同的发现、严重级别、结论、证据、未决事项和非声明，并更新 docs/translation-status.md。缺少或过期语言版本的报告不构成完整交付。
