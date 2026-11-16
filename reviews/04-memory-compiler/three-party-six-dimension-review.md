# Memory Compiler — Three-Party, Six-Dimension Review

- **Date:** 2026-11-16
- **Review scope:** Five Session E architecture documents in 04-memory-compiler/
- **Review type:** Static architecture review; no implementation, runtime, penetration or performance testing performed.
- **Review status:** Conditional Pass — architecture direction accepted for continued cross-session design; not a frozen implementation contract.
- **Branch:** session-e-memory-compiler-2026-11-16
- **Review method:** Three independent professional lenses simulated as architecture, engineering/reliability, and security/governance reviews. This is not a claim that three independent external reviewers signed off.

## 1. Materials and baseline

Reviewed repository baseline:
- README.md and ARCHITECTURE_ROADMAP.md
- 00-governance/architecture-invariants.md, design-principles.md, terminology.md
- 01-system-architecture/component-interactions.md, component-map.md, data-flows.md, responsibility-matrix.md, system-boundaries.md, system-overview.md, system-quality-attributes.md
- 02-domain-model/core-entities.md, domain-model-overview.md, epistemic-and-temporal-semantics.md, lifecycle-model.md, relationships-and-provenance.md, scope-and-permission-model.md
- reviews/integration/phase-1-abc-cross-document-integration-review.md
- reviews/architecture/2026-11-16-memory-domain-model-three-party-six-dimension-review.md
- reviews/07-agent-integration/three-party-six-dimension-review.md

The A/B/C integration report explicitly allows controlled D/E/F/G design but prohibits freezing Fact/Claim semantics, final identity/permission wire contracts, Forget completion guarantees and Accepted/Applied contracts before their respective decisions. E therefore marks those interfaces as candidates or open.

## 2. Executive conclusion

The Compiler architecture is compatible with the repository's primary authority boundaries:
- Ingestion owns durable acceptance and receipts.
- Compiler owns transformation and candidate proposals.
- Evidence/Provenance owns source and derivation traceability.
- Consolidation proposes duplicates, revisions and conflicts.
- D owns canonical identity, lifecycle and canonical commit.
- F owns retrieval/index projections and watermark semantics.
- G owns Context; E only emits impact events.
- H owns BMCP wire/Adapter contract; I owns global authorization, retention and Forget policy.

The design correctly separates Accepted, Processing, Compiled, Canonical Commit and Indexed. Model inference is optional and asynchronous. Deterministic validation and durable acceptance do not depend on an LLM.

**Conditional Pass** is appropriate because core semantic and governance contracts remain open in the upstream architecture. The documents intentionally avoid freezing those decisions. This report does not certify that Scope isolation, deletion, prompt-injection resistance, throughput or recovery have been implemented.

## 3. Three professional reviews

### 3.1 System Architect

**Conclusion: Pass with conditions.**

**Strengths**
- Clean split between ingress durability, semantic compilation, canonical authority and index publication.
- Compiler is a logical boundary, not a mandatory service or crate; modular monolith remains valid.
- Pipeline is explicit and preserves Event/Memory/Claim/Evidence/Provenance distinctions.
- Candidate IR avoids locking Fact/Claim semantics before INT-P0-01 ADR.
- Canonical writes are version-checked and lifecycle-owned; index updates are downstream projections.

**Conditions / concerns**
1. Candidate proposition mapping must be revisited immediately after Fact/Claim ADR; no implementation should treat the interim IR as canonical.
2. Claim identity/revision and Conflict Set remain D-owned and must be jointly tested with E.
3. Canonical commit event schema, generation and Index Watermark must be agreed with D/F/Storage.
4. Context impact event semantics must be agreed with G; E must not mutate Context or imply synchronous context invalidation.
5. Provenance DAG rule needs an ADR/decision with D/I before Forget dependency traversal is treated as complete.

### 3.2 Engineering and Reliability Lead

**Conclusion: Pass with conditions; implementation is not yet ready.**

**Strengths**
- Atomic Event + idempotency + receipt + outbox acceptance boundary is explicit.
- Crash windows before commit, after commit/before response and after response/before dispatch are testable.
- At-least-once dispatch plus stage idempotency is realistic for a modular monolith.
- Unknown canonical commit outcome is reconciled by operation identity instead of blind retry.
- Model outage does not block Accepted; deterministic extraction can continue.
- DLQ/replay preserve original Event identity and attempt history.

**Conditions / concerns**
1. Actual storage transaction/outbox implementation and payload/blob staging order remain CANDIDATE until Storage/Consistency design.
2. Receipt and idempotency retention horizons are I-owned and must be reconciled with Forget; tombstones must not retain forbidden content.
3. Lease fencing/epoch semantics need property tests under worker pause, duplicate lease and process restart.
4. Per-source ordering and out-of-order stream handling are not frozen; coordinate C/H.
5. Canonical commit/outbox and provenance atomic visibility need an implementation-level contract from D/Storage.
6. Queue priority and backpressure policies need load tests; no queue capacity or latency number is claimed.

### 3.3 Security and Reliability Auditor

**Conclusion: Pass on threat boundaries; residual risk remains and must be tested.**

**Strengths**
- Scope filtering is required before entity search, comparison set construction, graph expansion and aggregation.
- Permission is rechecked at worker execution; Evidence authorization is independent of Memory access.
- Forget fences suppress queued/replayed work and prevent resurrection.
- Raw content and model outputs are treated as untrusted data; extraction worker has no tool authority.
- Prompt-injection detection is explicitly described as incomplete, not a guarantee.
- Provenance supports audit and deletion dependency discovery without preserving forbidden source text by default.

**Conditions / concerns**
1. I must define authorization epochs, revocation SLA, Forget fence authority, retention and tombstone policy.
2. Cross-scope tests must include embedding candidate generation, entity resolution, graph expansion, caches, review queues and error/count side channels.
3. Evidence locators and lineage can reveal sensitive source existence; error and audit redaction need governance rules.
4. Prompt injection remains a model behavior residual risk; Agent action authorization stays outside Brain.
5. External model/provider copies cannot be declared physically erased by E; report only policy-defined suppression/erasure status.

## 4. Six-dimension assessment

### Dimension 1 — Architecture and responsibility boundaries

**Result: Pass with conditions.**

The five documents respect the A/C responsibility matrix. Ingestion does not compile; Compiler does not own canonical truth; Evidence does not adjudicate; Consolidation does not own lifecycle; F owns index projection; G owns Context; H owns wire contracts; I owns governance.

**Required follow-up**
- D must publish Canonical Write, Candidate Memory and lifecycle contracts.
- F must define generation and watermark consumption.
- G must define lifecycle/Forget context-impact event handling.
- No new E file or change to other sessions' paths is needed.

### Dimension 2 — Data model and semantics

**Result: Conditional Pass.**

Positive:
- CandidateProposition is deliberately neutral and preserves modality and source basis.
- Event, Evidence, Provenance, Memory and canonical Claim are not conflated.
- Time, scope, environment, confidence, trust and evidence strength remain distinct.
- Conflict and revision are proposals, not premature canonical objects.

Open:
- INT-P0-01 Fact/Claim ADR.
- INT-P1-02 Claim identity/revision and Conflict Set.
- INT-P1-06 typed references, lifecycle authority and Provenance DAG.
- D's final TimeValue/TimeInterval/ContentRef/ActorRef/ScopeRef types.

**Gate:** do not freeze extraction output or database schema until D ADR and reference contract are available.

### Dimension 3 — Data flow and transaction consistency

**Result: Pass with conditions.**

Positive:
- Accepted is committed with Event, idempotency record, receipt and compile intent.
- Outbox dispatch is at-least-once and processing is idempotent.
- Stage result and next-stage intent have a recoverable boundary.
- Canonical commit and Index publication are separate.
- Unknown outcomes are reconciled rather than assumed failed.

Open:
- Exact outbox/WAL mechanism and storage transaction boundary.
- Idempotency key composition and retention with H/I.
- Stage lease fencing and ordering semantics.
- Canonical commit event and watermark with D/F.
- Index rebuild and stale projection behavior in Storage/Consistency.

**Gate:** implement crash-injection matrix before claiming Accepted durability.

### Dimension 4 — Security, Scope and Forget

**Result: Conditional Pass; highest priority.**

Positive:
- Scope filter before candidate generation, entity matching and consolidation.
- Current authorization and Forget fence rechecked in async worker.
- Evidence is independently authorized.
- Forget blocks retries and replay from resurrecting content.
- Prompt injection is a documented residual risk.

Open:
- INT-P0-02 final identity/permission contract and revocation epochs.
- INT-P0-03 dependency completeness, deletion proof, backup/replica and idempotency tombstones.
- INT-P0-04 shared threat model and Agent-side action controls.
- Provenance DAG constraint needed to prove dependency traversal coverage.

**Gate:** I/D must define fence and deletion contracts; E cannot claim physical deletion completion.

### Dimension 5 — Performance, backpressure and resource use

**Result: Pass as a design proposal; validation pending.**

Positive:
- No synchronous large-model requirement on remember()/Accepted.
- Deterministic-first extraction and deferred model enrichment.
- Queue lanes, payload bounds, concurrency, candidate fan-out and lineage depth are explicit budget dimensions.
- Under overload, delay optional compile rather than weaken Scope checks or discard accepted Events.

Open:
- Workload arrival rates, event sizes, queue capacity, batch size, model routing and hardware envelope.
- Model-assisted extraction on target local VRAM.
- Conflict and entity candidate expansion cost.
- Backlog drain/recovery time and DLQ volume.

**Gate:** publish reproducible benchmark declarations; all numerical budgets remain TO_VALIDATE.

### Dimension 6 — Evolvability and observability

**Result: Pass with conditions.**

Positive:
- Schema, pipeline, method and model versions are recorded.
- Candidate proposals and immutable stage receipts support reprocessing.
- Correlation/causation chain spans Event through canonical/index publication.
- Metrics avoid raw payload and sensitive excerpt leakage.

Open:
- Shared schema registry and enum evolution rules with D/H.
- Canonical event compatibility and consumer replay contract.
- High-cardinality trace retention and audit redaction.
- Provenance compaction and source-retention policy.

**Gate:** cross-module conformance suite and event compatibility policy required before protocol freeze.

## 5. INT issue disposition

| ID | E treatment | Status after Session E design | Owner / next action |
|---|---|---|---|
| INT-P0-01 Fact / Claim | Neutral CandidateProposition IR; mapping adapter explicitly blocked | **OPEN / correctly contained** | Governance + D/B approve ADR; E remaps afterward |
| INT-P0-02 Scope Isolation | Scope at ingress, source dereference, entity search, consolidation, write, replay; async reauthorization | **DESIGN ADDRESSED; POLICY OPEN** | I defines identity, grants, epochs; D/F/G/H implement boundary checks |
| INT-P0-03 Forget | Dependency registration, immediate fence checks, suppression of queue/replay, derivative invalidation hooks | **DESIGN ADDRESSED; COMPLETION OPEN** | I/D define target coverage, tombstones, backups, proof; E supplies dependency inventory |
| INT-P0-04 Prompt Injection | Source/trust metadata, inert content, no tools in extraction worker, validation, residual risk disclosure | **MITIGATIONS SPECIFIED; RESIDUAL RISK OPEN** | I/H and Agent policy define threat model and conformance tests |
| INT-P1-02 Claim Revision / Conflict Set | Proposal IR includes participants, dimensions, evidence and resolution proposal | **CANDIDATE; D DECISION REQUIRED** | D owns identity/revision/Conflict Set canonical model |
| INT-P1-04 Accepted / Idempotency / Durable Ingestion | Atomic acceptance bundle, same/same and same/different semantics, crash matrix, outbox recovery | **DESIGN ADDRESSED; H/I/STORAGE CONTRACT OPEN** | H fields, I retention, Consistency implementation |
| INT-P1-06 Provenance / Lifecycle / Reference Types | Typed candidate refs, stage lineage, proposed DAG, lifecycle delegation | **PARTIALLY ADDRESSED; D/I OPEN** | D decides reference types/lifecycle authority; I/D decide DAG and Forget semantics |
| AR-004 Canonical / Index consistency | Canonical commit outbox + generation + index watermark; index rebuildable and lag visible | **DESIGN ADDRESSED; F/STORAGE CONTRACT OPEN** | D emits canonical generation; F specifies projection/watermark; Storage proves replay |

No issue is declared closed merely because an E proposal exists. Closure requires the named authority's decision and cross-document integration review.

## 6. Cross-module contracts delivered

### 6.1 D — Memory Brain

E supplies:
- CandidateEnvelope and CandidateProposition as non-canonical IR.
- CanonicalWriteRequest with source Event, Scope, actor, expected version, Evidence, Provenance, Entity/Relation and conflict/revision proposals.
- Commit response states committed/deferred/rejected/stale, canonical refs/version, lifecycle reason, generation and outbox ref.
- Typed error families for scope, permission, stale version, missing Evidence, incomplete Provenance, conflict review, idempotency and Forget fence.

D must decide canonical schema, Fact/Claim ADR mapping, Claim revision, Conflict Set, lifecycle authority and typed references. Requests are versioned and idempotent; retries after unknown outcome query the original operation.

### 6.2 F — Memory Runtime / Index

Canonical commit event fields: event_id, schema_version, commit_id, canonical_generation, changed object refs and types, prior/new version refs, scope refs, change kind, provenance refs, recorded_at, correlation/causation.

F's projection contract must publish per-index applied generation/watermark, lag, rebuild state and stale-read behavior. Memory, Entity and Relation projections are required; Claim/Evidence detail is exposed only under separate authorization. Index publication is asynchronous and cannot roll back canonical commit.

### 6.3 G — Memory Context

E/D publish version/lifecycle impact events: MemoryVersionChanged, ClaimRetracted, MemorySuperseded, MemoryArchived, MemoryForgotten and EvidenceRestricted. Each includes canonical ref, prior/new version, scope, event generation, reason code and correlation/causation. G alone decides Context Entry removal/replacement/qualification and Context version. Forget/revocation events require prompt reconciliation; E does not mutate Context.

### 6.4 H — Agent Integration / BMCP

E consumes a validated Event Envelope and returns AcceptedReceipt only after durable acceptance. Receipt and processing status are separate. Required logical attributes include authenticated producer, ActorRef, ScopeRefs, source identity, event classification, payload digest/ref, idempotency key, source times, retention/sensitivity and correlation IDs. H owns wire names, auth and negotiation.

### 6.5 I — Security and Governance

E requires:
- authorize ingress and every worker execution;
- current permission/revocation epoch and Forget fence;
- retention class, source sensitivity and legal processing obligations;
- dependency registration and target enumeration;
- tombstone/idempotency receipt retention policy;
- audit-safe deletion proof and external/backup residual semantics.

### 6.6 Contract common rules

All contracts carry schema version, stable typed references, Scope, Actor, correlation/causation, operation identity and explicit result/error. Same operation key/same canonical payload returns same result; same key/different payload conflicts. Async workers re-check authorization. Replay is at-least-once and idempotent. Unknown outcome is queried/reconciled, never guessed.

## 7. Required acceptance and fault-injection matrix

| Scenario | Expected result |
|---|---|
| Crash before ingress commit | No Accepted receipt |
| Commit succeeds, response lost | Retry returns original receipt |
| Response succeeds, worker dispatch fails | Outbox reconstructs work |
| Duplicate worker stage | Same stage result/receipt |
| Same key, different payload | Explicit conflict; original preserved |
| LLM offline | Accepted remains durable; deterministic stages continue |
| Permission revoked before worker execution | Fail closed; no source read/write |
| Forget fence during active stage | Cancel/suppress; no replay resurrection |
| Plan without outcome | No completed-outcome candidate |
| Same name across scopes | No cross-scope entity resolution |
| Conflicting overlapping claims | Conflict proposal; no silent overwrite |
| Non-overlapping validity | Coexistence, not false conflict |
| Evidence inaccessible | Do not disclose excerpt; defer or mark unavailable |
| Provenance cycle attempted | Reject pending DAG decision |
| Canonical commit, index outage | Canonical valid; index watermark lags and rebuilds |
| Canonical response lost | Query idempotent commit result |
| Malicious source requests tool use | Remains inert data; no tool call |
| Source unavailable during replay | Explicit unavailable lineage; no fabricated payload |

## 8. Decision summary

### DECIDED
- Accepted durability is independent of LLM inference.
- Event, candidate proposition, Evidence, Provenance, Memory and Claim remain distinct.
- Scope filtering precedes candidate generation and all comparison/merge operations.
- Plan/intent/prediction/attempt are not outcomes.
- Model output is untrusted proposal data; no model authority over permission, lifecycle or canonical commit.
- Canonical authority belongs to D; index is a derived projection.
- Conflicts are never silently overwritten.

### CANDIDATE
- CandidateEnvelope and ExtractionIR shapes.
- Atomic local transaction with outbox or equivalent WAL.
- Deterministic-first extraction, optional model enrichment.
- Strict DAG for derivation lineage.
- Logical queue priorities and deterministic blocking keys.
- Canonical generation and index watermark event shape pending F/Storage.

### TO_VALIDATE
- Model-assisted extraction quality and VRAM cost.
- Ingestion throughput, backlog recovery, queue sizing and stage latency.
- Entity/conflict candidate fan-out and false-positive/negative rates.
- Provenance traversal and Forget dependency discovery performance.

### OPEN
- Fact/Claim ADR (INT-P0-01).
- Final principal/producer identity and authorization epochs (INT-P0-02).
- Forget completion, tombstone, backup and external-copy semantics (INT-P0-03).
- Prompt-injection residual risk acceptance and cross-system threat model (INT-P0-04).
- Claim identity/revision and Conflict Set (INT-P1-02).
- H/I idempotency fields and retention (INT-P1-04).
- Provenance DAG, lifecycle authority and typed reference schemas (INT-P1-06).
- F Index Watermark and G context-impact handling details.

## 9. Final recommendation

**Conditional Pass.** The five E documents are suitable as a controlled architecture proposal and as input to D/F/G/H/I interface integration. They are not a frozen schema or implementation specification. Before Rust implementation, require:
1. approved Fact/Claim ADR and D's Claim/Conflict contracts;
2. I's identity, authorization, Forget and retention contracts;
3. H's ingress envelope/idempotency wire contract;
4. D/F canonical generation and index watermark agreement;
5. D's Provenance/reference/lifecycle authority decisions;
6. executable crash, replay, Scope isolation, Forget and conflict-preservation conformance tests.

No performance, security or deletion guarantee is claimed as implemented.
