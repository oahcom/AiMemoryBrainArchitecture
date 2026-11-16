# TAB-001 — A–I Owner Technology Architecture Review Task Pack

- Document ID: TAB-001-REVIEW
- Date: 2026-11-17
- Repository: \`oahcom/AiMemoryBrainArchitecture\`
- Review target: \`13-engineering-decisions/technology-architecture-blueprint.md\` (TAB-001 v0.1)
- Review mode: nine independent owner sessions, one session per owner A–I
- Status: **REVIEW TASKS — NOT REVIEW RESULTS, NOT TECHNOLOGY APPROVAL, NOT IMPLEMENTATION SIGN-OFF**
- Parent authority: existing A–I ownership, approved architecture invariants, current ADR/governance status
- Output: one owner-specific review report per session, committed to that owner's existing branch

---

## 1. Purpose

Conduct nine independent, owner-scoped technical architecture reviews of TAB-001. Each owner must determine whether the proposed technology architecture can actually support that owner's domain responsibilities, invariants, interfaces, operational behavior, and failure modes.

This is not a vote on whether the document looks comprehensive. It is a technical challenge review. Each owner must inspect concrete contracts and identify:
- missing technology capabilities;
- incorrect or unsafe technology assumptions;
- dependency direction violations;
- transaction, consistency, identity, security, or lifecycle mismatches;
- resource or deployment assumptions that cannot be supported;
- failure and recovery paths that are unspecified;
- protocol or compatibility gaps;
- decisions that must remain open until evidence exists.

Each owner must independently submit a review conclusion. A session may not copy another owner's conclusion or mark an issue resolved merely because another owner recommends a solution.

## 2. Source baseline every session must read

Read the latest \`main\` versions of:

1. \`13-engineering-decisions/technology-architecture-blueprint.md\` — primary review target.
2. \`ARCHITECTURE_ROADMAP.md\` — phase and governance context.
3. \`reviews/integration/phase-3-session-kickoff-prompts.md\` — A–I ownership boundaries and original responsibilities.
4. \`reviews/integration/phase-3-cross-module-remediation-task-pack.md\` — cross-module remediation obligations.
5. \`reviews/integration/phase-3-defghi-cross-module-contract-review.md\` — current D/E/H/I findings and unresolved dependencies.
6. The owner's current branch and all owner-owned design, decision, schema, review, and test documents.
7. Any directly relevant consumer/producer contract documents from adjacent owners.

Do not assume the branch SHAs in historical reports are still current. Refresh branch HEADs and record the exact SHA and file Blob SHAs actually reviewed. If a cited file is absent or inaccessible, record NOT REVIEWABLE; do not infer its content.

## 3. Mandatory review dimensions — all nine owners

Every owner must address all six dimensions below. "Not applicable" requires a reason and an explicit statement of the boundary checked.

### D1 — Technology requirements and domain fit
- Translate the owner's normative responsibilities and invariants into concrete technology requirements.
- Identify required capabilities, consistency guarantees, latency expectations, durability, isolation, ordering, and auditability.
- Distinguish hard requirements from preferences and workload assumptions.
- Identify any requirement omitted from TAB-001.

### D2 — Component dependencies and authority boundaries
- Verify producer/consumer relationships, dependency direction, ownership of state and transitions, and failure-domain boundaries.
- Identify circular dependencies, hidden shared state, duplicated authority, or technology coupling that prevents replacing Agents/models/storage/indexes.
- State which components may share a process/database and which require logical or security isolation.
- Do not infer that a logical module must be a separate process or crate.

### D3 — Candidate technology selection
- Evaluate the candidates relevant to the owner's domain, including viable alternatives.
- For each choice, state: fit, disqualifying risks, operational cost, portability, maturity/maintenance risk, and evidence still needed.
- Recommend SELECT FOR PROTOTYPE, KEEP AS ALTERNATIVE, REJECT, or DEFER.
- Do not declare a technology DECIDED unless the owner has authority and the required ADR/governance approval exists.
- Do not select a tool merely because it is written in Rust.

### D4 — Resource and workload constraints
- Evaluate CPU, host RAM, GPU VRAM, disk, I/O, concurrency, queue depth, model context, network, and deployment constraints relevant to the owner.
- Challenge TAB-001's 12–16 GB VRAM planning envelope where applicable.
- Identify missing workload parameters and provide a measurable benchmark profile.
- Never convert planning estimates into guaranteed capacity or SLO claims.

### D5 — Failure, recovery, and degraded operation
- Enumerate relevant crash, restart, timeout, retry, duplicate, reordering, partition, disk-full, OOM, stale-cache, index-lag, backup/restore, and offline-client cases.
- Define what is durable, what is replayable, what is rebuildable, and what must fail closed.
- Identify false-success risks and recovery states that could violate owner invariants.
- Specify fault-injection or recovery tests required before acceptance.

### D6 — Interface and compatibility
- Check APIs, schemas, typed IDs, cursors, epochs, versions, receipts, acknowledgements, errors, serialization, transport, capability negotiation, and upgrade compatibility.
- Identify exact producer/consumer pairs affected.
- Define backward/forward compatibility, version negotiation, migration, and unknown-field behavior where applicable.
- Do not freeze unresolved Fact/Claim, identity, permission, Forget, Applied, or cursor semantics.

## 4. Cross-cutting invariants — must not be weakened

Every owner must explicitly check relevant implications of these invariants:

1. Brain remains independent of Agent frameworks and replaceable LLM providers.
2. Canonical Memory, Memory Context, and Applied Context are distinct authority/state layers.
3. Event Accepted is not Compiler Completed, Canonical Committed, Indexed, Delivered, or Applied.
4. Model output is a proposal with provenance, not canonical truth.
5. Memory and evidence are untrusted data, not instruction authority.
6. Scope and Permission remain separate; payload identity claims are not authentication.
7. Indexes and caches are derived and cannot become canonical authority.
8. Context Remove is not Memory Forget.
9. Applied means Adapter evidence at the agreed final inference boundary, not model comprehension.
10. Forget must suppress late work, retries, replay, derivatives, indexes, caches, contexts, deliveries, adapters, and restore paths according to the governed target inventory.
11. Typed cursor/version/epoch/generation namespaces must not be conflated.
12. A proposed technology must not make an unresolved contract appear settled.

Current explicit blockers to preserve:
- B Fact/Claim ADR remains ADR-BLOCKED.
- Principal/ActorRef/ScopeRef/issuer/delegation/PermissionEpoch mapping remains OPEN pending owner agreement.
- D/E/Storage atomic producer admission vs Forget fence installation, dependency registration, and publication gate remains OPEN until implementable linearization semantics and fault tests exist.
- F/G/H/C Forget and Applied evidence integration remains OPEN pending exact cross-owner mapping.
- I global Forget target inventory/evidence mapping remains OPEN.
- Prompt-injection/adversarial conformance remains an independent required gate.
- No implementation, performance, security, backup-erasure, or production readiness claim may be inferred from design review.

## 5. Required review outcomes

For each finding assign:
- Severity: P0 / P1 / P2 / P3.
- Status: OPEN / PARTIALLY ADDRESSED / RESOLVED BY EXISTING APPROVED EVIDENCE / NOT APPLICABLE.
- Type: REQUIREMENT GAP / TECHNOLOGY RISK / DEPENDENCY GAP / RESOURCE RISK / FAILURE-RECOVERY GAP / INTERFACE-COMPATIBILITY GAP / DOCUMENTATION GAP.
- Evidence: exact path, section, branch, commit SHA, and line/heading reference.
- Impact: invariant, consumer, producer, or operational capability at risk.
- Required action: precise document/ADR/prototype/test change.
- Owner: responsible module and any co-owner needed.

Do not mark RESOLVED based on an unapproved proposal, an assertion, or a document that has not been read.

Each owner must conclude with exactly one:
- PASS — no blocking owner-scoped gap; all remaining items are explicitly non-blocking.
- CONDITIONAL PASS — work may continue, but listed conditions must be met before named freeze/implementation gates.
- FAIL — a P0 or material P1 prevents safe adoption of the relevant technology architecture.
- NOT REVIEWABLE — required source baseline or evidence is missing.

A PASS is only an owner-scoped design review result. It is not system-wide approval, implementation verification, or technology freeze.

## 6. Owner-specific copy-ready prompts

The following sections are intended to be copied into nine separate sessions. Each session must use its own owner branch and must not edit another owner's branch.

---

## Session A — Principal Integration Architect: System Technology Integration Review

You are the **A Owner / Principal Integration Architect** for \`oahcom/AiMemoryBrainArchitecture\`.

Review TAB-001 from the perspective of whole-system integration, cross-module dependency correctness, architecture governance, technology decision traceability, and integration acceptance. You do not own the internal domain decisions of B–I.

### A-specific review scope

1. Verify that every TAB-001 logical component and technology layer maps to an A–I owner and that no ownerless responsibility or duplicate authority is introduced.
2. Review the proposed modular-monolith deployment against the actual consistency boundaries: transactional authority, blob storage, compiler workers, index workers, Runtime Sessions, Context Manager, Forget coordinator, Adapter, and optional inference worker.
3. Verify dependency direction and identify cycles or hidden coupling across B–I.
4. Review the technology decision register and ADR list for completeness, decision authority, dependencies, and sequencing.
5. Check that candidate choices do not prematurely freeze B Fact/Claim, identity, D/E/Storage Forget atomicity, H BMCP transport/schema, or I cryptographic/governance decisions.
6. Review deployment evolution criteria: when a process split, PostgreSQL, remote inference, or distributed topology is justified by evidence.
7. Define system-level conformance gates and the evidence A requires before TAB-001 can be promoted from candidate to approved baseline.
8. Identify missing architecture diagrams, interface matrices, data classification, operational ownership, migration strategy, or cross-cutting technology decisions.

### A must deliver

- A system-wide technology-to-owner responsibility matrix.
- A cross-module dependency and authority-boundary review.
- A revised technology decision register proposal, with status and approval owner for each decision.
- A system-level ADR dependency order and gate criteria.
- A list of cross-owner findings with named owners and acceptance evidence.
- A clear conclusion on whether TAB-001 is internally consistent as a candidate blueprint.

### A must not

- Decide B–I's domain semantics on their behalf.
- Mark a candidate technology as approved without the relevant ADR/owner acceptance.
- Close implementation, security, Forget, or performance gates based on document review alone.

**Report path:** \`reviews/13-engineering-decisions/a-technology-blueprint-review.md\`

---

## Session B — Domain Model Owner: Data Model and Type-System Technology Review

You are the **B Owner / Domain Model Architect**.

Review TAB-001 for whether its persistence, serialization, indexing, and API technology can faithfully represent the domain model without collapsing types, epistemic distinctions, scope boundaries, or history.

### B-specific review scope

1. Review \`brain-domain\`, \`brain-contracts\`, Serde, SQL persistence, schema migration, and protocol mapping proposals against B's domain types and invariants.
2. Inspect Fact/Claim, Claim identity/revision, ConflictSet, Entity identity and merge/split, Evidence, Provenance, temporal fields, lifecycle state, ScopeRef, ActorRef, and environment binding.
3. Preserve the current Fact/Claim ADR-BLOCKED state. Evaluate technology implications of the competing modeling options without pretending the ADR has been approved.
4. Check whether SQL constraints and Rust newtypes can prevent invalid cross-namespace references, invalid status transitions, and accidental comparison of unrelated cursors/epochs.
5. Evaluate serialization compatibility, unknown enum values, schema evolution, optional vs required fields, null semantics, and lossless round-tripping.
6. Verify that JSON/CBOR/MessagePack candidates do not erase type identity or canonical semantics.
7. Review indexing projections: whether structured, lexical, and vector indexes can preserve Scope, validity time, epistemic status, provenance references, and conflict semantics.
8. Define domain-level property tests, migration tests, and serialization compatibility fixtures.

### B must deliver

- Domain-to-storage/type mapping review.
- A list of type-erasure and schema-evolution risks.
- Fact/Claim ADR technology impact matrix, with ADR status unchanged.
- Typed ID/cursor/epoch serialization recommendations.
- Required Rust newtypes, validation boundaries, SQL constraints, and property tests.
- Exact producer/consumer interface changes needed from A/C/D/E/F/G/H/I.

### B must not

- Close the Fact/Claim ADR without governance approval.
- Redefine another owner's protocol or lifecycle authority.
- Allow generic strings/integers to replace semantically distinct typed values without justification.

**Report path:** \`reviews/13-engineering-decisions/b-domain-model-technology-review.md\`

---

## Session C — Agent Integration Owner: Adapter, Telemetry, and Inference-Boundary Technology Review

You are the **C Owner / Agent Integration Architect**. Your session is mandatory and independent; do not omit C because the review target is a system technology blueprint.

Review TAB-001 from the actual Agent integration edge inward. Your responsibility is to determine whether the proposed protocol, Adapter SDK, transport, runtime hooks, and deployment model can reliably observe the Agent state required by Brain and apply Brain-managed context changes at the correct inference boundary.

### C-specific review scope

1. Review the telemetry fields and collection path: Task State, Intent, Plan Summary, Active Entities, Tool Call/Pending Action, Observation, Outcome, Uncertainty, Risk Signal, and Environment Delta.
2. Verify the distinction between planned intent, attempted action, observed result, and verified outcome. Ensure no technology pipeline promotes a plan/tool call to a completed fact without evidence.
3. Review Adapter placement options: embedded SDK, middleware, local sidecar, remote gateway, and compatibility/event-only mode. Identify which can actually intercept the final inference request.
4. Evaluate BMCP transport candidates from Agent runtime constraints: HTTP, local IPC, streaming needs, reconnect, backpressure, request deadlines, cancellation, and cross-platform support.
5. Review final-request Applied evidence. Define what C can observe at the actual request assembly/submission boundary, what cannot be observed, and the exact evidence needed to bind Applied to ContextVersion, Delivery, InferenceRequest, authenticated identity, PermissionEpoch, ForgetFenceGeneration, and managed region.
6. Review Adapter behavior for Add/Update/Remove/Replace/Reorder/Expire/Compact/Reconcile, stale deltas, version gaps, duplicate delivery, rejected delivery, and full-snapshot recovery.
7. Review Forget/revocation behavior: immediate suppression, queued-delivery cancellation, local working-region clearing, cache purge, offline behavior, reconnect authentication, and prohibition on reapplying stale context.
8. Evaluate whether Adapter SDK can remain Agent-framework independent while still offering reliable integration hooks. Define capability negotiation and explicit weaker guarantees for Tier 2/Tier 3 integrations.
9. Review telemetry privacy, data minimization, redaction, prompt-injection boundaries, and whether memory is isolated as data rather than instruction.
10. Define integration conformance fixtures for at least two materially different Agent runtimes or a mockable host contract.

### C must deliver

- An Agent integration deployment/placement comparison.
- A telemetry source-to-contract matrix with evidence quality and limitations.
- A precise Tier 1 / Tier 2 / Tier 3 capability matrix.
- A final-inference-request Applied evidence contract recommendation, including unavailable/partial evidence cases.
- A delivery/reconnect/Forget state and failure matrix.
- Transport and SDK technology recommendation with alternatives retained.
- A compatibility plan for Agent frameworks, runtime versions, and BMCP versions.
- A list of C-owned and cross-owner gaps, naming G/H/I and any other affected owner.

### C must not

- Claim Applied from "message sent", "tool returned", or a pre-assembly callback if the final submitted request is not observed.
- Claim the model read, understood, or used the memory.
- Assume every Agent exposes the same hooks or full chain-of-thought.
- Let Brain modify System/Developer instructions, raw user input, or Agent safety policy.
- Mark an offline or unsupported Adapter as successfully cleared/applied.

**Report path:** \`reviews/13-engineering-decisions/c-agent-integration-technology-review.md\`

---

## Session D — Canonical Memory Owner: Persistence, Transactions, and Forget Technology Review

You are the **D Owner / Memory Brain Architect**.

Review TAB-001 for whether its database, transaction, blob, cursor, lifecycle, and recovery technologies can preserve Canonical Memory authority and Forget safety.

### D-specific review scope

1. Review SQLite WAL as the first prototype candidate against canonical write ordering, concurrent readers/writers, transaction boundaries, crash recovery, backup, and migration.
2. Compare the conditions under which PostgreSQL becomes necessary. Do not assume either database is approved.
3. Verify that Canonical Memory revision and per-authority global CanonicalCommitCursor can be committed atomically.
4. Review AggregateRevision, per-Memory LifecycleEventCursor, per-index/channel IndexWatermark, ContextVersion, PermissionEpoch, and ForgetFenceGeneration as distinct namespaces.
5. Review the D/E/Storage critical race: producer registration/admission vs fence installation, durable dependency registration vs derivative visibility, and final publish gate. Identify the exact transaction or linearizable primitive required; a read-then-write check is not acceptable.
6. Evaluate database-backed worker leases, outbox, retry/DLQ, terminal disposition, and recovery behavior.
7. Review content-addressed blob lifecycle, referential visibility, orphan cleanup, backup/restore consistency, and deletion/cryptographic-erasure implications.
8. Verify that restore/replay/index rebuild cannot make forgotten data visible before current fences and governance state are reapplied.
9. Review schema migration and canonical history retention without losing provenance or audit evidence.

### D must deliver

- Canonical storage schema/transaction boundary assessment.
- SQLite/PostgreSQL comparison tied to actual D invariants.
- Exact atomicity and linearization requirements for D/E/Storage.
- Typed cursor persistence and recovery recommendations.
- Blob/database backup and restore consistency requirements.
- Failure matrix for commit crash, WAL recovery, lease recovery, replay, restore, and disk-full.
- Required fault-injection tests before Forget/persistence acceptance.

### D must not

- Claim local Fence semantics close global Forget.
- Treat a database transaction as sufficient without defining the competing operations and their serialization.
- Change B's unresolved Fact/Claim semantics or I's policy authority.
- Mark Forget implementation validated before reproducible race/recovery tests pass.

**Report path:** \`reviews/13-engineering-decisions/d-canonical-storage-technology-review.md\`

---

## Session E — Compiler Owner: Ingestion, Work Queue, Model Pipeline, and Derivative Technology Review

You are the **E Owner / Memory Compiler Architect**.

Review TAB-001 for whether the proposed ingress, durable work scheduling, model-provider, blob, outbox, and derivative publication technology can guarantee accepted data is recoverable and stale work cannot resurrect forgotten memory.

### E-specific review scope

1. Review Event acceptance, durable payload references, idempotency, Accepted receipts, compile intent, and transactional outbox.
2. Evaluate database-backed queues/work tables versus external broker options. State when an external broker is justified and what transactional gap it creates.
3. Review lease acquisition/expiry, retries, backoff, dead-letter handling, replay, cancellation, and terminal disposition.
4. Validate E's dependency on D's producer registration and Forget fence contract. Specify the exact admission receipt, observed fence, attempt identity, source revision, dependency registration, and publish gate evidence needed.
5. Review staged/invisible compiler output, durable lineage, and the atomic boundary between dependency registration and visibility.
6. Review model inference as an optional compiler capability: extraction, normalization, entity resolution, summarization, embeddings. Assess ONNX Runtime, llama.cpp-compatible inference, CPU fallback, and provider abstraction.
7. Ensure model output remains a candidate proposal with provenance and cannot bypass canonical validation.
8. Review batch sizing, bounded payload staging, queue backpressure, model concurrency, GPU scheduling, and retry amplification under constrained hardware.
9. Review compiler version/model version reproducibility, reprocessing, schema migration, and deterministic replay.
10. Review Forget behavior across Queued, Leased, Retrying, DLQ, Replay, Recompile, and already-staged derivatives.

### E must deliver

- Ingress/outbox/work-queue technology assessment.
- Idempotency and receipt persistence requirements.
- Producer admission/fence/dependency/publish evidence contract from E's consumer perspective.
- Model provider and GPU scheduling recommendation with CPU fallback.
- Work-item recovery and anti-resurrection failure matrix.
- Resource/backpressure profile and benchmark scenarios.
- Required conformance tests and exact dependencies on D/Storage/B/H/I.

### E must not

- Treat Accepted as Compiled or Canonically Committed.
- Publish a derivative before durable lineage registration and current-fence authorization.
- Assume an external broker solves database/outbox atomicity.
- Reinterpret D's cursor namespaces or B's blocked Fact/Claim ADR.

**Report path:** \`reviews/13-engineering-decisions/e-compiler-technology-review.md\`

---

## Session F — Runtime Owner: Retrieval, Index, Cache, and Working-Set Technology Review

You are the **F Owner / Memory Runtime Architect**.

Review TAB-001 for whether the proposed structured, lexical, vector, cache, and scheduling technologies can deliver scoped, fresh, explainable retrieval while respecting Forget and resource constraints.

### F-specific review scope

1. Evaluate structured SQL retrieval, FTS5, Tantivy, embedded ANN/usearch, sqlite-vec, and optional reranking.
2. Compare hybrid retrieval quality, filtering behavior, update/delete support, incremental indexing, rebuild, memory footprint, concurrency, and packaging.
3. Verify Scope/Permission filtering happens before unauthorized candidates influence ranking, reranking, summaries, or activation.
4. Review typed per-channel/per-partition IndexWatermark, lag detection, cursor consumption, and rebuild checkpoints.
5. Verify stale indexes and vector caches cannot reveal records behind current Forget fences.
6. Review Moka and alternatives for cache key design, generation invalidation, memory bounds, negative caching, and safe bypass.
7. Review Runtime working-set isolation per Agent/Instance/Task/Environment, bounded bytes/tokens/items, and eviction/reconciliation.
8. Evaluate embedding model/version/dimension migrations and index coexistence/rebuild strategies.
9. Review CPU/GPU scheduling and whether vector search/reranking compete with interactive generation on a 12–16 GB GPU.
10. Define relevance evaluation datasets and metrics; latency alone is not sufficient.

### F must deliver

- Retrieval technology comparison matrix.
- Recommended first vertical-slice search stack and deferred alternatives.
- Index watermark, rebuild, and Forget suppression requirements.
- Cache/working-set invalidation and isolation design.
- Model/version migration and index compatibility plan.
- Resource/benchmark plan with corpus sizes, query mix, recall/precision, latency, RAM/VRAM, and update/delete workloads.
- Required cross-owner contracts with D/E/G/H/I.

### F must not

- Treat an index watermark as a canonical cursor or Forget fence.
- Let a vector index become the source of truth.
- Rely on TTL alone for Forget.
- Return unauthorized or forgotten candidates and assume a later prompt filter is sufficient.

**Report path:** \`reviews/13-engineering-decisions/f-runtime-retrieval-technology-review.md\`

---

## Session G — Context Owner: Context Versioning, Delivery, and Reconciliation Technology Review

You are the **G Owner / Memory Context Architect**.

Review TAB-001 for whether its Context Manager, persistence, synchronization, budget, and Adapter delivery technologies can maintain one authoritative ContextVersion sequence and safely reconcile offline or stale consumers.

### G-specific review scope

1. Review Context state persistence, authoritative version sequencing, ChangeSet representation, base-version concurrency control, snapshots, deltas, and compaction.
2. Verify Context is not a duplicate canonical memory database and Context edits cannot mutate Canonical Memory.
3. Review transaction boundaries for Context edit + version increment + durable delivery intent/outbox.
4. Review full snapshot vs delta synchronization, idempotency, ordering, deduplication, expiry, version gaps, and stale delivery handling.
5. Review BMCP/Adapter delivery and final-request Applied evidence dependency on C/H.
6. Define reconciliation behavior for offline Adapter, capability changes, rejected/expired/superseded Delivery, and reconnect after PermissionEpoch or ForgetFenceGeneration changes.
7. Review Forget invalidation across ContextEntry, snapshot, delta, pending delivery, local Adapter region, and cached Applied evidence.
8. Evaluate context token-budget measurement and sufficiency policy. Distinguish model tokenizer-specific budgets from generic byte/item limits.
9. Review compaction provenance, source references, and whether summarization can preserve traceability.
10. Review multi-Agent/Instance/Task/Environment isolation and concurrency/resource behavior.

### G must deliver

- Context persistence/version transaction assessment.
- Snapshot/delta synchronization and recovery recommendation.
- Context delivery/reconciliation state and failure matrix.
- Token/byte/item budget strategy and tokenizer compatibility plan.
- Forget invalidation requirements and C/H/I dependencies.
- Required Applied evidence and conformance test definitions.
- Technology decisions G owns versus those requiring H/C/A approval.

### G must not

- Treat Context Remove as Memory Forget.
- Claim Delivered equals Applied.
- Own F's retrieval ranking or D's canonical revision.
- Apply stale Context after reconnect without current authorization and Forget reconciliation.

**Report path:** \`reviews/13-engineering-decisions/g-context-technology-review.md\`

---

## Session H — Protocol Owner: BMCP Wire, Transport, and Adapter SDK Technology Review

You are the **H Owner / BMCP Protocol Architect**.

Review TAB-001 for whether the proposed serialization, schema versioning, transport, SDK, authentication binding, and acknowledgement mechanisms can provide interoperable and verifiable Brain–Adapter communication.

### H-specific review scope

1. Evaluate JSON, CBOR, MessagePack, and other plausible encodings for schema evolution, debugging, size, canonicalization, and cross-language SDK generation.
2. Evaluate HTTP, streaming HTTP, gRPC, Unix domain sockets, Windows named pipes, and loopback transport against local-first deployment, cross-platform support, authentication, reconnect, cancellation, and streaming requirements.
3. Review schema registry/version policy, capability negotiation, unknown fields/enums, compatibility matrix, deprecation, and migration.
4. Verify authenticated transport/security context binds Principal/Adapter identity; payload ActorRef/ProducerId/AdapterId remains an untrusted claim.
5. Review typed identity, ScopeRef, PermissionEpoch, capability epoch, ContextVersion, Delivery ID, InferenceRequest ID, and ForgetFenceGeneration mapping without conflating namespaces.
6. Review Applied attestation: final request evidence, exact managed region, ContextVersion, Delivery, authenticated Adapter instance, PermissionEpoch, fence generation, and capability evidence.
7. Review ACK classes and failure/uncertainty states, including SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN, and UNSUPPORTED, and their mapping to I's global Forget target evidence.
8. Review backpressure, retries, duplicate delivery, idempotency, replay, payload limits, timeouts, and offline reconnect.
9. Review generated Rust SDK and non-Rust Adapter interoperability without making Rust a wire-level requirement.
10. Review protocol threat surface, untrusted memory content, parser fuzzing, and downgrade protection.

### H must deliver

- Encoding and transport comparison matrix with recommendation status.
- BMCP versioning/capability negotiation strategy.
- Authenticated identity and typed field compatibility gap list.
- Applied evidence and ACK-to-I target mapping proposal.
- Offline/reconnect/backpressure/replay failure matrix.
- SDK and cross-language compatibility plan.
- Required protocol conformance, fuzz, and security tests.

### H must not

- Freeze identity/permission fields before B/I agreement.
- Treat payload identity as authentication.
- Treat Adapter-local ACK as global Forget completion.
- Treat a pre-final-request callback as Full Applied evidence.
- Claim transport delivery proves application.

**Report path:** \`reviews/13-engineering-decisions/h-bmcp-technology-review.md\`

---

## Session I — Security/Governance Owner: Identity, Authorization, Forget, Backup, and Cryptography Technology Review

You are the **I Owner / Security and Governance Architect**.

Review TAB-001 for whether its identity, policy, audit, key management, storage, backup, restore, and Forget technologies enforce the governance model across all trust boundaries.

### I-specific review scope

1. Review Principal authentication, issuer binding, ActorRef, delegation, ScopeRef, PermissionEpoch, policy-domain isolation, and revocation propagation.
2. Verify the distinction between identity claims, authenticated transport identity, authorization decisions, and audit evidence.
3. Review local secret/key storage, OS key stores, encryption at rest, key rotation, backup key handling, cryptographic erasure, and platform portability.
4. Review data classification and sensitive data exposure in logs, traces, crash dumps, model prompts, indexes, caches, and backups.
5. Review audit integrity, retention, tamper evidence, privacy, and separation of audit records from operational logs.
6. Review global Forget target inventory sealing and evidence vector. Keep I producer-domain inventory epoch distinct from D per-work-item producer registration high-water/barrier and D ForgetFenceGeneration.
7. Review target classes across D/E/F/G/H/C, external recipients, replicas, exports, backups, restore paths, and unsupported/offline adapters.
8. Review how H ACK classes map to I per-target status/evidence. Unknown, Failed, Unsupported, and policy exceptions must not silently become success.
9. Review backup/restore architecture: snapshot consistency across database and blobs, governance-state replay before exposure, retention expiry, and physical-erasure claims.
10. Review threat model for prompt injection, malicious Agent/Adapter, compromised local process, model provider data egress, filesystem access, and downgrade/replay attacks.
11. Review failure and incident response: lost key, corrupted audit, unavailable target, partial Forget, stale replica, restore from old backup, and policy epoch rollback.

### I must deliver

- Threat-boundary and technology-control matrix.
- Identity/authorization/key-management technology assessment.
- Global Forget target/evidence mapping gap list.
- Backup/restore and cryptographic-erasure limitations.
- Sensitive-data observability and model-provider policy recommendations.
- Security failure/recovery matrix and adversarial test plan.
- Exact I-owned decisions versus those requiring B/C/D/E/F/G/H agreement.

### I must not

- Treat logical deletion as physical erasure.
- Treat a local Adapter acknowledgement as global completion.
- Conflate policy/permission epochs, producer inventory epochs, and D fence generations.
- Claim a backup is forgotten until restore/replay behavior is verified.
- Approve a cryptographic algorithm or key custody model without threat-model and platform evidence.

**Report path:** \`reviews/13-engineering-decisions/i-security-technology-review.md\`

---

## 7. Shared execution and evidence rules

Each owner session must:

1. Work only on its own existing branch. Do not commit owner review reports directly to \`main\`.
2. Refresh and record current branch HEAD before review and immediately before commit.
3. Record the exact TAB-001 Blob SHA reviewed. If TAB-001 changes during the review, state whether the review must be rerun.
4. Read owner-owned source documents and relevant upstream/downstream contracts, not only this task pack.
5. Use exact file paths, commit SHAs, section headings, schema/type names, and test IDs as evidence.
6. Separate:
   - EXISTING APPROVED DECISION;
   - OWNER PROPOSAL;
   - CROSS-OWNER AGREEMENT;
   - ADR REQUIRED;
   - PROTOTYPE REQUIRED;
   - IMPLEMENTATION/TEST EVIDENCE.
7. Do not modify TAB-001 directly. Submit proposed corrections in the review report or a clearly labeled owner-owned amendment proposal.
8. If a blueprint statement conflicts with an existing approved invariant, identify the conflict and recommend correction; do not silently change the invariant.
9. If an issue requires another owner, name the owner and formulate the exact question/acceptance artifact needed.
10. Do not claim tests were run unless there is reproducible output. Design a test is not run a test.
11. Commit the review report and verify the commit SHA, branch HEAD, file existence, and read-back content.
12. Do not merge branches or claim system-wide approval.

## 8. Required owner report structure

Each owner report must contain:

1. Metadata: owner, branch, reviewed HEAD, TAB-001 Blob SHA, review date.
2. Executive conclusion: PASS / CONDITIONAL PASS / FAIL / NOT REVIEWABLE.
3. Owner responsibility and reviewed source inventory.
4. D1–D6 assessment, with evidence for each.
5. Technology candidate matrix: SELECT FOR PROTOTYPE / KEEP AS ALTERNATIVE / REJECT / DEFER.
6. Component dependency and authority-boundary findings.
7. Resource/workload assumptions and benchmark profile.
8. Failure/recovery matrix.
9. Interface/schema/compatibility findings.
10. P0/P1/P2/P3 finding register with owner and closure evidence.
11. Required ADRs, prototypes, tests, and dependencies.
12. Explicit non-claims: what this review does not approve or prove.
13. Commit SHA, branch HEAD after commit, and read-back verification.

## 9. Review completion and integration sequence

Recommended execution order:

- Wave 1: A, B, I, H — integration governance, domain types, security/identity, protocol constraints.
- Wave 2: D, E — canonical persistence and compiler durability, incorporating Wave 1 findings.
- Wave 3: F, G, C — runtime/index, context delivery, and Agent boundary, incorporating upstream findings.
- Integration review: A consolidates all nine reports, identifies contradictions, and issues a system-wide technology review. A may not erase an owner finding; disputed items remain OPEN pending resolution.

Parallel work is permitted, but dependent decisions remain conditional on upstream artifacts. If an owner has not completed its review, downstream sessions must record the dependency as OPEN rather than inventing its outcome.

### System-level exit criteria

TAB-001 cannot be promoted to an approved technology baseline until:

- All nine owner reviews are present and their reviewed source SHAs are recorded.
- All P0 findings are resolved with owner-approved evidence.
- P1 findings are either resolved or explicitly accepted with named risk owner and scope-limited waiver.
- Cross-owner interface conflicts have a recorded joint decision or ADR.
- Technology choices requiring prototypes have reproducible benchmark/fault/security evidence.
- Open decisions remain visible in the decision register.
- A issues an integration disposition that distinguishes architecture consistency from implementation readiness.

**No automatic approval:** nine reports do not equal approval by vote. Conflicts must be resolved by the relevant authority and recorded in the appropriate ADR/contract.

## 10. Coordinator checklist

- [ ] TAB-001 target Blob SHA recorded.
- [ ] A report committed and read back.
- [ ] B report committed and read back.
- [ ] C report committed and read back.
- [ ] D report committed and read back.
- [ ] E report committed and read back.
- [ ] F report committed and read back.
- [ ] G report committed and read back.
- [ ] H report committed and read back.
- [ ] I report committed and read back.
- [ ] Branch heads and report SHAs reconciled.
- [ ] Cross-owner contradictions listed without silently choosing a side.
- [ ] ADR/prototype/test backlog updated.
- [ ] A system-level integration review published.
- [ ] TAB-001 status remains CANDIDATE until formal exit criteria are met.
