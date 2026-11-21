---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "PR #429 English mirror and historical source blob 35a766fae29c0b8ddf692a6ec062762f0fca29d2
        - "OWNER-DECISION-FACT-CLAIM-001, merged PR #446"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Source restored from the current bilingual E design artifact; Fact/Claim semantics reconciled to the merged Owner decision. Runtime/schema approval is not implied."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Memory Compiler design-specification: compiler-overview"
    canonical_scope_id: "memory-compiler/compiler-overview"
    canonical_scope_keywords:
      - candidate-ir
      - canonical-schema
      - fact
      - claim
      - identity
      - lifecycle
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/compiler-overview.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/compiler-overview.md"
---

# Memory Compiler Overview

- Document ID: E-COMPILER-001
- Version: 1.2
- Restored source lineage: updated E owner design mirror in PR #429; historical source blob 35a766fae29c0b8ddf692a6ec062762f0fca29d2.
- Owner semantic decision: OWNER-DECISION-FACT-CLAIM-001, merged in PR #446.
- Status: Ownership/safety invariants DECIDED; stage topology/orchestration CANDIDATE; model routing/throughput/resource budgets TO_VALIDATE
- Owner: Session E — Memory Compiler
- Baseline: A/B/C architecture and domain semantics as of 2026-11-16
- Integration dependencies: INT-P0-01/02/03/04; INT-P1-02/04/06; AR-004

## 1. Purpose

The Memory Compiler transforms durably accepted source Events and registered source material into traceable candidate Memory/Claim/Entity/Relation assets and, after canonical authority decisions, coordinates canonical commit and downstream projection publication. It is a recoverable semantic transformation system, not an LLM-to-vector-database shortcut.

The Compiler guarantees that source identity, Scope, evidence links, derivation method, temporal qualification, epistemic status and idempotency survive each stage. It does not claim accepted input is true or that compilation necessarily produces a Memory.

## 2. Scope

Included: Event-to-work orchestration, deterministic normalization, model-assisted extraction, classification, entity-resolution collaboration, Evidence/Provenance creation, consolidation, conflict proposal, canonical-write coordination, retries, replay, and index/context invalidation notifications.

Excluded: Canonical Memory schema authority and lifecycle policy (D); retrieval scheduling/ranking/Runtime Cache (F); Context version ownership (G); Agent Adapter/BMCP wire authority (H); global identity/permission/retention policy (I); physical index implementation.

## 3. Responsibilities

- Consume durable Event refs and recoverable compile intents.
- Produce candidate objects with immutable source refs and stage lineage.
- Enforce Scope filters before source dereference, extraction, entity matching, merge or write.
- Keep deterministic stages independent of LLM availability.
- Use model inference only as optional, bounded, versioned transformation.
- Coordinate, but never usurp, Entity/Relation Manager and Canonical/Lifecycle authority.
- Preserve conflicts and revisions; never silently overwrite.
- Emit canonical-commit and projection-publication events with monotonic generations.

## 4. Non-responsibilities

Compiler does not authenticate an untrusted Agent claim by itself; choose external action permissions; define whether Fact is an independent object; define canonical Claim identity/revision; decide final lifecycle state; own Runtime ranking or Context; guarantee model truthfulness; or promise physical erasure beyond I's governed policy.

## 5. Inputs / Outputs

**Inputs:** Accepted EventRef, SourceRef/ContentRef, authenticated ActorRef, resolved ScopeRef set, Permission decision context, schema version, source timestamps, idempotency identity, retention class, source trust metadata, correlation/causation IDs, and optional extraction policy/model profile.

**Outputs:** stage receipts; CandidateEnvelope; Evidence/Provenance refs; Entity/Relation proposals; ConflictSet proposal; CanonicalWriteRequest; CanonicalCommitResult; IndexPublicationRequested; MemoryVersionChanged / ClaimRevisionChanged / ClaimRetracted / MemoryForgotten notifications; structured retryable/permanent errors.

Compilation may yield NO_CANDIDATE, PENDING_EVIDENCE, REVIEW_REQUIRED, DEFERRED or REJECTED without violating Accepted durability.

## 6. Data model

### 6.1 CompilerWorkItem (logical candidate)

~~~text
CompilerWorkItem {
  work_id: OpaqueId
  event_ref: TypedObjectRef
  scope_refs: ScopeRef[]
  actor_ref: ActorRef
  ingress_receipt_ref: TypedObjectRef
  idempotency_scope: IdempotencyScope
  source_digest: Digest
  schema_version: Version
  pipeline_version: Version
  stage: CompilerStage
  state: WorkState
  attempt: u32
  lease_epoch: u64
  authorization_epoch: VersionRef?
  forget_fence_epoch: VersionRef?
  correlation_id: OpaqueId
  causation_id: OpaqueId?
  created_at: Instant
  updated_at: Instant
}
~~~

### 6.2 CandidateEnvelope (CANDIDATE; not canonical schema)

~~~text
CandidateEnvelope {
  candidate_id: OpaqueId
  source_event_refs: TypedObjectRef[]
  scope_refs: ScopeRef[]
  environment_scope_ref: ScopeRef?
  modality: SourceModality
  propositions: CandidateProposition[]
  entity_mentions: EntityMention[]
  relation_proposals: RelationProposal[]
  evidence_drafts: EvidenceDraft[]
  provenance_draft: ProvenanceDraft
  temporal_qualifications: TimeQualification[]
  source_epistemic_basis: EpistemicBasis
  extraction_method: MethodRef
  uncertainty: UncertaintyRecord[]
  unresolved_questions: String[]
  schema_status: "candidate-unfrozen"
}
~~~

CandidateProposition intentionally avoids deciding Fact-versus-Claim object identity. It records proposition structure, modality, polarity, subject/object hypotheses, evidence pointers, source epistemic basis and qualifications. Mapping to D's approved Claim/Fact ADR is a separate adapter layer. No canonical output schema is frozen before INT-P0-01.

### 6.3 Stage receipt

Each stage records input/output digest or reference, stage version, deterministic/model-assisted mode, actor/method, start/completion time, attempt, authorization/fence epoch, and terminal/retryable result. Raw source payload is not copied into ordinary logs.

## 7. Pipeline / state machine

~~~mermaid
flowchart TD
 A[Source Event / Document / Telemetry] --> B[Durable Ingress + Receipt]
 B --> C[Scope & Permission Recheck]
 C --> D[Deterministic Normalize / Classify]
 D --> E[Extract Candidates]
 E --> F[Entity Resolution Collaboration]
 F --> G[Evidence Creation]
 G --> H[Provenance Construction]
 H --> I[Candidate Memory]
 I --> J[Consolidation / Duplicate Detection]
 J --> K[Conflict Detection / Revision Proposal]
 K --> L[Canonical Write Contract]
 L --> M{D / Lifecycle decision}
 M -->|commit| N[Canonical Commit + Outbox]
 M -->|defer/review| O[Persist Candidate / Review State]
 M -->|reject| P[Reasoned Rejection]
 N --> Q[Index Publication Event]
~~~

| Stage | Default execution | Model use |
|---|---|---|
| Envelope validation, digest, idempotency, scope binding | Deterministic | Never required |
| Text decoding, structural parsing, timestamp preservation | Deterministic | Optional assisted parsing only |
| Modality/event classification | Rules first; uncertain items queued | Optional classifier |
| Entity/Relation mention extraction | Hybrid | Optional model |
| Candidate proposition extraction | Hybrid | Optional model |
| Evidence locator validation/digest | Deterministic | Model may suggest spans; validator verifies |
| Provenance construction | Deterministic from stage receipts | Model cannot invent lineage |
| Scope compatibility/authorization | Deterministic policy enforcement | Never delegated |
| Dedup/conflict candidate generation | Deterministic filters + optional semantic similarity | Model may propose, not adjudicate |
| Canonical commit | D/Lifecycle-owned transaction | Never delegated |

Work state: RECEIVED → READY → LEASED → STAGE_RUNNING → STAGE_COMMITTED → READY(next stage) → PROPOSAL_READY → CANONICAL_PENDING → COMMITTED / DEFERRED / REJECTED / DEAD_LETTER. Lease is not a canonical transaction lock. Each stage commits an idempotent result before advancing its durable cursor.

## 8. Invariants

1. Accepted Event remains durable independent of Compiler/LLM availability.
2. Event, Evidence, candidate proposition, Memory and Claim are not aliases.
3. No stage reads or correlates outside authorized Scope.
4. Every derived proposition links to source Evidence/Provenance or explicit unavailable reason.
5. Plan/intent/prediction/pending/attempted cannot become completed outcome without outcome Evidence.
6. Source content is untrusted data; it cannot alter tool authority, system policy or compiler configuration.
7. Model output is an untrusted proposal, never permission or canonical decision.
8. Canonical writes use expected version and D-approved semantics.
9. Conflicts remain explicit; no last-write-wins semantic overwrite.
10. Indexes are derived; canonical commit and index visibility are distinct.

## 9. Idempotency

Each stage key derives from stable work identity + stage name/version + input digest + scope identity. Same key/same input returns prior stage receipt. Same key/different input is an integrity conflict. Model stages persist exact model/provider/profile/prompt-template version and normalized output digest; nondeterministic re-execution creates a new attempt/revision, not overwrite. Canonical commit uses D idempotency and expected-version contract.

## 10. Consistency

Event log and compile-intent/outbox are atomically committed at ingress. Stage outputs and next-stage scheduling use atomic stage-result/outbox boundary or equivalent recoverable journal. Candidate records are not canonical. D owns canonical version/current-pointer atomicity. Canonical commit notification is transactionally outboxed; index workers publish watermarks only after applying matching canonical generation.

## 11. Failure recovery

- Restart resumes from last committed stage receipt.
- Model outage leaves work pending; deterministic stages continue where possible.
- Invalid/unsupported input is quarantined with reason; raw accepted Event remains governed by retention.
- Repeated permanent failure enters DLQ; operator replay creates new attempt while retaining old receipts.
- Canonical conflict triggers reload/reconcile, never blind overwrite.
- Missing source during replay is marked unavailable; no excerpt is fabricated.
- Forget fence invalidates queued/leased work before further protected read/write.

## 12. Security / Scope

Resolve and authorize Scope at ingress, every worker lease, each source dereference, entity candidate search, consolidation-set construction, canonical write and replay. Filters precede candidate generation, ranking, aggregation and graph expansion. Evidence has independent read authorization. Async workers re-check current principal, permission version, revocation/Forget fence and target scope. Cache keys bind scope, environment, actor class, policy/revocation epoch and source version. No model-generated Scope is trusted.

## 13. Performance / backpressure

**CANDIDATE:** separate logical queues/lanes for critical outcomes, ordinary interactive events, bulk imports and low-priority telemetry. Queue classes may share physical store in modular monolith. Bound payload size, queue bytes, concurrent model jobs, entity fan-out, graph depth, retry count and per-scope quotas.

Under pressure: reject before Accepted if durable capacity cannot be guaranteed; after Accepted preserve durable work and delay lower-priority compilation; coalesce only explicitly replaceable telemetry, never fabricate complete history. Numeric budgets are TO_VALIDATE on declared hardware/workloads.

## 14. Observability

Track acceptance latency, backlog bytes/age, per-stage latency, deterministic/model-assisted ratio, model queue wait, retry/DLQ rates, canonical-commit lag, index-watermark lag, scope denials, Forget-fence cancellations, candidate-to-commit conversion, unsupported-claim rate and provenance coverage. Trace correlation/causation from ingress through canonical/index events. Never put raw prompts, source payloads, credentials or sensitive excerpts in metric labels.

## 15. Interfaces

- **H / BMCP → E:** validated ingress envelope and Accepted receipt; E consumes authenticated ActorRef/resolved Scope but does not define wire names.
- **D ← E:** Candidate Memory / Canonical Write / conflict and revision proposals; D owns canonical schema and decision.
- **F ← E/D:** canonical commit and index-publication events with generation, typed refs, changed object classes and scope.
- **G ← D/E:** MemoryVersion changed, Claim retracted/superseded, lifecycle changed, Forget suppression events.
- **I ↔ E:** authorization recheck, Forget fence, retention class, deletion dependency registration, audit-safe tombstones.
- **Consistency/Storage:** outbox, replay cursor, canonical generation, index watermark, backup and recovery contracts.

All cross-module messages carry schema version, actor/scope context, correlation/causation, idempotency for state-changing actions and explicit error/retry semantics.

## 16. Test scenarios

LLM outage before/after Accepted; crash after Event+Outbox commit; duplicate stage dispatch; same key/different digest; plan-only input; cross-scope entity match; permission revoked between queue and execution; Forget while leased; canonical commit with index outage; replay after source expiry; malicious document with tool/policy instructions.

## 17. Dependencies

A/B/C baseline; D Canonical Memory/lifecycle contracts; H producer identity/ingress envelope; I permission, retention, Forget and revocation epochs; F projection requirements; G context invalidation semantics; Storage/Consistency outbox/recovery; bounded model inference scheduler.

## 18. Open questions

- RESOLVED: Fact/Claim semantics and I1 identity/revision choice are adopted by OWNER-DECISION-FACT-CLAIM-001 (PR #446 merged).
- OPEN: D canonical ClaimRevision/ConflictSet field schema, lifecycle contract and consumer pins; semantic identity/revision is decided, but concrete schema remains unfrozen.
- OPEN: INT-P1-06 Provenance cycle policy and lifecycle authority event.
- CANDIDATE: queue lanes, model routing, deterministic-first thresholds, stage journal.
- TO_VALIDATE: local model-assisted extraction quality/cost on 12–16 GB VRAM; throughput and backlog recovery.
- OPEN: ingress idempotency receipt and replay metadata retention horizon, jointly with I.

## 19. Phase 3 durable ingress and Forget integration addendum

- Pipeline consumes E durable Accepted receipt and compile-intent record. Accepted is custody/durability only; it is not Processed, Compiled, CanonicalCommitted or Indexed. Receipt/idempotency survive model outages and transport response loss.
- Stage results and next-stage intents require atomic stage-result/outbox boundary or equivalent recoverable journal. Every replay/recompile is a new attempt over immutable Event identity, reauthorized against current I Permission Epoch and D Forget Fence.
- CompilerWorkItem lease authorization_epoch and forget_fence_epoch are opaque owner-issued tokens. E must not mint, numerically compare or substitute them for source Event cursor, D canonical commit cursor, F index watermark or ContextVersion.
- E registers each in-flight producer/run and every derived dependency before output visibility. D/I authoritative barrier/publication gate must serialize registration against Forget; local prechecks alone do not close check-then-publish race.
- H BMCP envelope and I Principal/ActorRef contracts are candidate dependencies. H transports owner-defined idempotency namespace/key/digest; I defines authenticated producer binding, security-domain identity, PermissionEpoch and policy.
- Owner has approved Fact/Claim semantics as Option A + I1. Exact E-to-D/I canonical mapping remains Candidate; CandidateEnvelope/CandidateProposition remain pre-canonical IR.
- See accepted-receipt-and-idempotency-contract.md and forget-fence-and-derived-registration-part1.md for detailed CANDIDATE contracts.

## 20. Architecture follow-up — Candidate IR and Canonical Schema boundary

**Status:** E-owned architecture contract extension / PROPOSED. This section incorporates OWNER-DECISION-FACT-CLAIM-001 for semantics and identity choice; it does not freeze a cross-owner schema or authorize Runtime implementation.

### 20.1 Candidate IR is not Canonical Record

Candidate IR is the versioned, compiler-owned representation of what was extracted from an accepted source and how that extraction was derived. It is private, provisional, provenance-bearing and non-authoritative. CandidateEnvelope, ExtractionIR and CandidateProposition are related stages/views of this pre-canonical representation; they are not aliases for Canonical Memory, Claim, Fact, Entity or Relation records.

The input boundary is a durably accepted source bundle: immutable EventRef/SourceRef/ContentRef, exact source digest, accepted-receipt and compile-intent references, trusted ActorRef/ScopeRefs supplied by the owning ingress/security contracts, source metadata, and pinned extraction/pipeline policy versions. An arbitrary string without source identity, digest and trusted scope context is not sufficient for an authoritative compile operation.

Candidate IR MUST preserve, directly or by immutable reference:

- Original source identity, exact digest, source schema/content type, locale and source-time metadata; source bytes remain at their governed source location rather than being copied into ordinary logs.
- Source spans/locators bound to the exact immutable source representation, including encoding and normalization version where offsets depend on them.
- Original surface text/value and any normalized hypothesis as separate values; normalization MUST NOT overwrite the source representation.
- Modality, polarity, source epistemic basis, temporal qualifications, Scope and environment qualification.
- Entity mentions and relation hypotheses without assigning canonical identities; proposition subject/predicate/object hypotheses and qualifiers.
- Evidence and provenance references/drafts, extraction method/profile/version, stage receipts, uncertainty, ambiguity, unresolved fields and explicit unsupported/unavailable reasons.
- Non-semantic source metadata and unknown extension material when it can be retained safely. If an input field cannot be represented or safely retained, compilation MUST report it as unsupported/unresolved or quarantine the candidate; it MUST NOT silently discard it.

Candidate-local IDs identify only candidate/stage artifacts. They MUST NOT be presented as D-issued canonical IDs or reused as Canonical Identity.

### 20.2 Candidate validation invariants

Validation is more than a non-empty check. A candidate is structurally valid only when:

1. Required source, digest, schema/pipeline version and trusted scope references are present and well-typed.
2. Every referenced source, evidence, provenance and stage receipt resolves to the exact expected immutable version, or carries an explicit unavailable reason.
3. Every source span is within the exact source byte/segment bounds and is bound to the source digest, encoding and normalization profile.
4. Candidate-local identifiers are unique within their declared namespace; typed references and relation endpoints have compatible kinds.
5. Modality, polarity, epistemic basis, time precision/zone, confidence/uncertainty and optional values use declared types and valid ranges; unknown is explicit, never fabricated as a default.
6. Scope/environment metadata comes from trusted ingress/security context, not source text or model output.
7. Provenance links every derived proposition to source evidence or an explicit missing-evidence reason; model output cannot invent lineage.
8. Original values, normalized values, qualifiers, metadata, uncertainty and unresolved content remain recoverable.
9. No candidate state implies CanonicalCommitted, Published, Indexed, Verified, authorized, or Forget-complete.

A validation report identifies each failure by stable error code and field/path/reference, and distinguishes invalid, incomplete, unsupported, stale-authority and transient-unavailability outcomes. Partial extraction may produce a PARTIAL/REVIEW_REQUIRED candidate only when all emitted fields independently satisfy the invariants; invalid fields are not silently omitted.

### 20.3 Candidate lifecycle and errors

Candidate artifacts and stage receipts are append-only by logical attempt. A retry of the same work and same input digest is idempotent; changed source bytes, policy, parser/model profile or schema version creates a new attempt/revision with explicit lineage. Recompile MUST NOT mutate an earlier candidate or reset the root producer-work identity.

The compiler may return a reasoned outcome such as NO_CANDIDATE, PARTIAL, REVIEW_REQUIRED, DEFERRED, REJECTED or QUARANTINED. These are compiler outcomes, not D lifecycle states. Candidate retention, protected-content access and deletion are subject to I policy and the applicable D/I Forget Fence; an expired lease, timeout, missing receipt or unknown authority state is never success or terminal proof.

Error classes include: EMPTY_INPUT; MALFORMED_SOURCE; UNSUPPORTED_CONTENT_TYPE/SCHEMA_VERSION; MISSING_REQUIRED_FIELD; DIGEST_OR_SPAN_MISMATCH; INVALID_TYPED_REFERENCE; SCOPE_MISMATCH; AMBIGUOUS_OR_UNRESOLVED; MISSING_EVIDENCE_OR_PROVENANCE; IDEMPOTENCY_CONFLICT; STALE_PERMISSION_EPOCH; FORGET_FENCE_BLOCKED; CANONICAL_VERSION_CONFLICT; ADR_MAPPING_BLOCKED; SERIALIZATION_PROFILE_UNSUPPORTED; and RETRYABLE_DEPENDENCY_UNAVAILABLE. Error details must not disclose protected content or object existence beyond the caller's authority.

## 21. Canonical Schema boundary and authority

Canonical Schema is defined by the approved domain model and the accountable domain Owner contracts, not by Candidate IR field names, an E proposal, a storage adapter, or a serializer. The relevant source contracts include the D Canonical Memory Store and Memory Versioning contracts, B's Fact/Claim decision record, I's authorization/retention/Forget policy, and H's separately owned wire serialization rules.

The authority split is:

| Concern | Authority | Compiler constraint |
|---|---|---|
| Canonical Memory/Claim/Fact/Entity/Relation identity allocation and canonical version/lifecycle | D, subject to approved domain semantics | E emits proposals and consumes D-issued references/results; it never mints, rewrites or substitutes canonical IDs |
| Canonical commit, expected-version checks, lifecycle transition and canonical cursor | D | E submits a request through the D-owned contract; no direct canonical-store write |
| Forget Fence semantics, producer barrier, lineage inventory and final canonical publication ordering | D, coordinated with I and Storage | E supplies complete source/derivative lineage and obeys the authoritative gate; local prechecks do not authorize publication |
| Authentication, authorization, PermissionEpoch, revocation, retention and global Forget policy/completion | I | E consumes current owner-issued authorization context/receipts; it does not mint, compare as a substitute, or override PermissionEpoch |
| H wire envelope and external protocol serialization | H | E's internal Candidate serialization is not a wire contract |
| Durable physical transaction/visibility realization | Storage/Consistency under its accountable owner contract | E cannot claim atomicity or visibility from a local receipt or queue ACK |

Compiler permission: E may persist its own accepted-work bookkeeping, candidate artifacts, stage receipts and private staging outputs within its approved scope. E may submit a CanonicalWriteRequest and record D's authoritative response. E MUST NOT directly write or overwrite Canonical Schema, allocate canonical identity, choose final lifecycle, fabricate CanonicalCommitCursor, manufacture PermissionEpoch/ForgetFence tokens, or expose derived artifacts before the D/I/Storage publication gate is satisfied.

OWNER-DECISION-FACT-CLAIM-001 selects Option A + I1: Claim is a stable proposition thread with immutable ClaimRevision; Fact is a separate governed attestation with immutable FactRevision bound to exact ClaimRevisionRef values. This resolves the semantic and identity choice. It does NOT freeze field-level schema, DDL, public API, H wire fields, D ConflictSet shape or Storage layout. CandidateProposition and CandidateEnvelope remain neutral pre-canonical IR. Canonical mapping remains blocked until D's schema/lifecycle contract, I's authorization and attestor policy, H's wire contract, and consumer acceptance are version-pinned; no heuristic mapping is permitted.

## 22. Fact/Claim mapping — Owner semantic decision adopted; schema boundary remains open

Fact and Claim MUST remain semantically distinct in the candidate model:

- **Claim candidate:** a proposition asserted, reported, inferred, disputed or retracted by a source. It is not a guarantee of truth. Subject/predicate/object hypotheses, polarity, modality, qualifiers, Scope, time, epistemic basis and evidence lineage remain explicit.
- **Fact/attestation candidate:** a possible adjudication/attestation about an exact proposition/revision, with candidate references to attestor, method/version, evidence, Scope, validity and decision history. This is a conceptual candidate only; E does not define or instantiate a canonical Fact identity or lifecycle.
- **CandidateProposition:** neutral extraction IR. The Owner decision selects a separate identity-bearing Fact attestation and Claim proposition; E still cannot mint either canonical identity or instantiate a canonical Fact.

The current status must be read with precise granularity. OWNER-DECISION-FACT-CLAIM-001 was approved and merged in PR #446 (merge commit ad5ca81a32b413aef3f9b5bccd06030aabde8275). It selects Option A + I1 for Fact/Claim semantics and immutable identity/revision behavior. The earlier B-ADR-FACT-CLAIM-001 ADR-BLOCKED conclusion on the semantic question is superseded by this Owner decision. D's independent schema-freeze gate remains in force: no field-level ClaimRevision/FactRevision schema, DDL, public API, ConflictSet schema, storage layout or H wire payload is approved. E MUST preserve neutral CandidateProposition and MUST NOT perform canonical mapping until D/I/H consumer contracts, migration/compatibility and conformance evidence are version-pinned.

The candidate alternatives are:

| Option | Meaning | D impact | I impact | Disposition |
|---|---|---|---|---|
| A — separate Fact attestation object | Fact has its own canonical identity/revision and binds exact ClaimRevisionRef(s), authorized attestor, method, evidence, Scope and validity | Requires D-owned identity, lifecycle, versioning, reference integrity and Forget dependency rules for Fact and Claim revisions | Requires I-approved attestor authorization, PermissionEpoch recheck, evidence access/retention and global Forget policy | **Owner-approved semantic direction (PR #446); exact mapping remains Candidate** |
| B — Fact as a qualified view of an exact ClaimRevision | No separate Fact identity; a view/qualification is derived from a precise Claim revision and declared predicate | Lower identity/storage complexity, but D must define exact revision and lifecycle semantics for the view | I still governs authorization, policy and evidence retention; view must not imply permission or truth | Not selected; requires a superseding Owner decision |
| N — neutral pre-canonical mapping | Preserve CandidateProposition and any attestation evidence as candidate-only references; do not map to canonical Fact/Claim | No new D identity or lifecycle is created before approval | No attestation authority is inferred; current I controls still apply to source access | **Required compiler behavior until D/I/H consumer and schema gates close** |

E does not select domain semantics. The Owner has approved Option A + I1 as the semantic direction. Therefore E MUST continue to emit neutral CandidateProposition and MUST NOT perform canonical Fact/Claim mapping until the responsible D/I/Storage/H consumer contracts, migration/compatibility and conformance evidence are version-pinned and reviewed. Text similarity, extraction confidence or a model label such as “fact” never grants canonical identity or attestation authority.

### 22.1 Formal Owner decision request

- **DECISION_REQUEST_ID:** MC-ADR-FACT-CLAIM-001
- **MODULE:** Memory Compiler
- **ISSUE_OR_ADR:** OWNER-DECISION-FACT-CLAIM-001; B-ADR-FACT-CLAIM-001 historical record; INT-P0-01; source: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md
- **DECISION_REQUIRED:** Record the Owner decision as authoritative for semantics and I1 identity/revision choice; complete D/E/F/G/H/I consumer mapping and acceptance; define exact schema and candidate-to-canonical boundary conditions. Exact schema approval remains a separate later gate.
- **CURRENT_FACTS:** CandidateProposition remains neutral pre-canonical IR. Owner semantic decision `OWNER-DECISION-FACT-CLAIM-001` is approved and merged (main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`; PR #446 merge commit `ad5ca81a32b413aef3f9b5bccd06030aabde8275`). The B ADR is superseded as the live semantic decision request and remains historical evidence. No full Fact/Claim schema, DDL, public API or wire contract is approved; exact consumer mappings remain Candidate pending version-pinned review.
- **CONFLICTING_CONTRACTS:** Historical B-ADR-FACT-CLAIM-001 recommendation/status; D Memory Versioning's consumer-contract/schema-freeze gate; Domain Model's approved DECIDED semantics; E Extraction and Normalization mapping; historical PR #194 OPEN correction, later superseded by AID-2026-014 convergence commits.
- **OPTIONS:** A + I1 is the adopted semantic model; N remains mandatory for E's pre-canonical Candidate IR boundary until D/I/H consumer and schema gates close. Any change requires a superseding Owner decision.
- **RECOMMENDED_OPTION:** Preserve neutral CandidateProposition and defer canonical mapping; do not treat the selected semantic direction as an approved schema.
- **IMPACT_ON_D:** D must own any approved canonical IDs, immutable revisions, lifecycle transitions, expected-version commit, reference integrity and Forget dependency closure. No E-generated identity is admissible.
- **IMPACT_ON_I:** I must define/accept attestor authorization, current PermissionEpoch/revocation checks, source/evidence access, sensitivity/retention and global policy implications. E cannot create or waive authorization.
- **FORGET_FENCE_IMPACT:** Any selected Fact/Claim object and all evidence/provenance derivatives must be included in D's authoritative producer/dependency inventory and D/I fence/publication ordering. Unknown or stale fence state blocks publication; no post-fence derivative visibility or resurrection.
- **RUNTIME_IMPLEMENTATION_IMPACT:** Mapping code, canonical Fact/Claim serialization, schema/DDL, cross-module wire fields and mapping conformance tests remain blocked. Runtime may implement only neutral Candidate IR behavior after the separate engineering-phase entry authorization and approved owner contracts.
- **REQUIRED_AUTHORITY:** Owner semantic selection is approved in merged PR #446; B/D/E/F/G/H/I consumer artifacts must still be version-pinned and reviewed before implementation mapping/schema freeze; A refreshes integration registry and consumer pins; Storage and H own persistence and wire contracts.
- **OWNER_DECISION:** DECIDED_OPTION_A_I1; CROSS_OWNER_SCHEMA_ACCEPTANCE_PENDING
- **EVIDENCE:** Owner decision `OWNER-DECISION-FACT-CLAIM-001` main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`; PR #446 merge `ad5ca81a32b413aef3f9b5bccd06030aabde8275`; current main `c138654c942dc93b5a36eccb2ff0e41452156429`; historical B-ADR-FACT-CLAIM-001; docs/en/03-memory-brain/memory-versioning.md §§17/Claim-freeze gate; 02-domain-model/domain-model-overview.md §§10–13; merged PR #194 and its superseding AID-2026-014 commits; docs/en/04-memory-compiler/extraction-and-normalization.md; Issue #7 deferral record.
- **FOLLOW_UP_ACTIONS:** B reconciles ADR status/source pins; D publishes exact canonical identity/lifecycle mapping; I records attestor authorization/retention/Forget acceptance; F/G/H record exact consumer mapping and compatibility; Storage publishes persistence acceptance; A refreshes integration registry and pins; E keeps neutral Candidate IR until all required evidence exists; blocked tests remain blocked until exact decisions are pinned.

## 23. End-to-end compiler lifecycle and data flow

| Stage | Input → output | Owner | Preconditions and authority | Failure/retry and data status |
|---|---|---|---|---|
| Raw source / durable ingress | Source bytes or reference + metadata → immutable EventRef, Accepted receipt, compile intent | H/I for authenticated envelope and policy; E for E-owned ingress semantics; durable store for custody | Authenticated producer, resolved Scope, idempotency and durable acceptance | Before Accepted: reject without claiming custody. After Accepted: preserve durable source/work; retry by stable identity |
| Candidate IR | Accepted source bundle → ExtractionIR/CandidateEnvelope and stage receipts | E | Source digest/version, current access context, pinned parser/policy; no canonical identity | Partial/unresolved is explicit; retry same digest idempotently; changed input/method creates new attempt |
| Validation | Candidate + trusted validation context → field-addressed ValidationReport | E, consuming D/I/H references | Structural/provenance/scope checks; authoritative current I permission and D fence must be checked at protected boundaries | Invalid is permanent until corrected; stale authority/fence fails closed; transient dependency outage may retry |
| Mapping decision | Valid neutral candidate → approved mapping instruction or ADR_MAPPING_BLOCKED | B decides semantics; D accepts canonical mapping; I constrains authorization; E adapts | Exact approved ADR and pinned D/I consumer contracts | Semantic decision is resolved; concrete schema mapping remains blocked until D/I/H contracts are pinned; no heuristic mapping |
| Canonical Schema boundary | CanonicalWriteRequest → D-issued canonical IDs/revisions/commit result or reasoned defer/reject | D; I/Storage participate at their boundaries | D expected-version/lifecycle rules; current I PermissionEpoch; D/I Forget Fence; complete dependency and Storage visibility protocol | Conflict/defer/reject returned explicitly; unknown outcome queried by stable operation key; E never fabricates success |
| Candidate serialization | Valid Candidate IR + pinned profile → deterministic candidate bytes + digest | E for internal candidate format; H for wire; D/Storage for canonical persistence format | Versioned profile and lossless representability; canonical schema remains separately governed | Unsupported profile/field fails explicitly; same input/profile produces same bytes; round-trip preserves semantic content |

Pipeline summary: Raw Memory/Source → durable Accepted boundary → Candidate IR → structural and provenance validation → Mapping Decision → D-owned Canonical Schema boundary → separately governed serialization/persistence. A blocked mapping may terminate as a valid private Candidate result; it must not be promoted by fallback.

## 24. Language-neutral interface contract for future Runtime

These are semantic contracts, not Rust signatures, frozen API schemas or implementation authorization.

### Existing Workspace Rust reference pipeline — main readback

The current Workspace does contain `crates/memory-compiler/src/lib.rs` (main `f23906dc75256a6ffb90051a6c0888d0dd247e62`, Blob `7476835ca770c1522b4b405f7c74e517eab894e5`, 614 lines). It is explicitly described in its module header as a pure Rust reference pipeline with no database, network, model-provider or authorization implementation; production authority integrations are traits and remain unimplemented.

- `MemoryCompiler<A>::compile()` exists and composes Ingestion, Extraction, Normalization, Staging and PublicationGate.
- No public `MemoryCompiler::validate()` or `MemoryCompiler::serialize()` method exists in this source snapshot. The language-neutral `validate` and `serialize` contracts below are target semantics, not current callable APIs.
- `PublicationAuthority` is an injected trait; the crate contains no production D/Storage/I authority implementation.
- Eleven inline Rust unit tests exist in `lib.rs`. `cargo test -p memory-compiler` passed 11/11 on local checkout `7a926e57091a1b11277fa936cb75a6f215712164`; `crates/memory-compiler` was byte-identical to the cited main commit. These tests cover the reference pipeline only and do not satisfy the full MC-AT matrix.
- The originally requested legacy paths `src/memory/compiler.rs` and `tests/compiler_test.rs` are absent; the actual Workspace path is the crate above.

This is real reference code and test evidence, not production integration or authorization to extend Runtime behavior.

### compile

- **Input:** an AcceptedSourceBundle containing immutable source/event/content references, digest, accepted-receipt and compile-intent references, trusted ActorRef/ScopeRefs, source metadata and pinned compile policy/profile versions.
- **Output:** CompileResult containing candidate references, stage receipts, explicit completeness/outcome and field-addressed diagnostics; no Canonical Record is implied.
- **Errors:** malformed/empty/unsupported input, missing source, scope denial, stale PermissionEpoch, Forget Fence block, idempotency conflict, unresolved ambiguity, missing evidence, ADR mapping block and retryable dependency failure.
- **Invariants:** same stable work identity + same digest/profile is idempotent; changed digest/profile creates a new attempt/revision; no valid source information is silently dropped; Accepted is not Compiled or CanonicalCommitted.
- **Side effects:** may create E-owned work/stage/candidate records and private staging artifacts; may not directly write canonical records or expose derivatives.
- **Permission/idempotency:** uses owner-issued current authorization and fence evidence; stable producer-work identity survives retry/replay; D/I/Storage gates govern publication.
- **Dependencies:** H ingress identity/envelope; I authorization and PermissionEpoch; D producer registration, canonical identity/lifecycle and Forget Fence; Storage durability/visibility; B Fact/Claim ADR.

### validate

- **Input:** CandidateEnvelope/ExtractionIR plus the exact source/evidence references and a validation context carrying opaque, current owner-issued authorization/fence evidence where protected reads or boundary checks are required.
- **Output:** ValidationReport with VALID, PARTIAL, INVALID, UNSUPPORTED, STALE_AUTHORITY or BLOCKED_BY_ARCHITECTURE_DECISION disposition and stable error code + field/path/reference for each finding.
- **Errors:** required field/type/range violations, digest/span mismatch, unresolved required reference, scope mismatch, missing provenance, invalid modality/time/metadata, stale permission/fence, identity/lifecycle conflict and ADR block.
- **Invariants:** validation never upgrades epistemic status, canonical lifecycle, identity, permission or truth; it validates candidate semantics and reports external authority outcomes without minting them.
- **Side effects:** no canonical mutation, no permission grant, no fence update and no candidate-field deletion; any diagnostic/audit write is separately identified and idempotent.
- **Permission/idempotency:** repeated validation over the same candidate and same authority snapshot is stable; changed authority snapshot is a distinct validation result.
- **Dependencies:** E candidate rules; B epistemic/domain semantics; D canonical/lifecycle/fence predicates; I current authorization/PermissionEpoch; H typed envelope references.

### serialize

- **Input:** a validated Candidate IR object and an explicitly pinned CandidateSerializationProfile/version.
- **Output:** deterministic bytes, profile/version identifier and content digest; the output is a candidate artifact, not a Canonical Schema record or H wire message.
- **Errors:** unsupported profile/version, unrepresentable required field, duplicate/invalid key, invalid numeric/time value, encoding failure and unknown required extension.
- **Invariants:** same semantic candidate + same profile produces byte-identical output; decode(encode(candidate)) preserves all required fields, metadata, references, uncertainty and extensions; unknown required semantics fail rather than disappear.
- **Side effects:** pure transformation; no identity allocation, canonical write, authorization decision, publication or external side effect.
- **Permission/idempotency:** serialization is deterministic and safe to repeat; protected content may only be serialized for an authorized recipient/scope and in accordance with I retention/handling policy.
- **Dependencies:** E candidate schema/profile; B domain semantics; I data handling/retention; H only if an external wire mapping is separately requested; D/Storage only for canonical persistence encoding.

**Serialization profile status:** the internal candidate format and canonicalization profile are CANDIDATE, not frozen. The selected profile must specify UTF-8 handling, deterministic object-key ordering, stable enum tokens, numeric/time encoding, optional-field representation, collection ordering, extension handling and schema-version compatibility. Unicode code points and original surface forms are preserved; normalization must be explicit and versioned, never an implicit lossy rewrite. No serializer may silently omit unknown or unsupported source metadata. H wire encoding and D/Storage canonical persistence remain separate contracts.

## 25. Runtime acceptance plan — architecture test matrix

All rows below remain planned acceptance-matrix scenarios, not executed matrix results. Separately, the existing Workspace Rust reference crate has 11/11 unit tests passing as recorded above; that result does not satisfy or relabel any MC-AT row. Production Runtime integrations remain unauthorized in this phase.

| ID | Scenario | Required assertion | Status |
|---|---|---|---|
| MC-AT-01 | Valid accepted source → Candidate | Candidate IR and stage lineage are produced; no canonical status is implied | PLANNED_NOT_RUN |
| MC-AT-02 | Empty input | Explicit EMPTY_INPUT; no empty successful candidate | PLANNED_NOT_RUN |
| MC-AT-03 | Malformed source/encoding | Stable field-addressed error; no panic or silent truncation | PLANNED_NOT_RUN |
| MC-AT-04 | Missing required source/digest/Scope metadata | Reject or quarantine with exact missing path; no guessed defaults | PLANNED_NOT_RUN |
| MC-AT-05 | Unicode, CJK, combining marks and emoji | Preserve source code points and round-trip bytes under the pinned profile | PLANNED_NOT_RUN |
| MC-AT-06 | Metadata and optional fields | Preserve source time, locale, trust, retention, qualifiers, uncertainty and optional values | PLANNED_NOT_RUN |
| MC-AT-07 | Unknown extension/source field | Preserve losslessly or return explicit unsupported/quarantine result | PLANNED_NOT_RUN |
| MC-AT-08 | Invalid digest/source span | Reject span outside exact source bytes or mismatched digest | PLANNED_NOT_RUN |
| MC-AT-09 | Fact/Claim semantic and identity model | Verify Option A + I1 decision consumption; canonical field mapping remains blocked pending D/I/H contracts | BLOCKED_BY_SCHEMA_CONTRACT |
| MC-AT-10 | Claim identity/revision schema mapping | Verify only after D canonical schema, lifecycle and consumer pins | BLOCKED_BY_SCHEMA_CONTRACT |
| MC-AT-11 | Canonical identity conflict | E does not mint/overwrite identity; D conflict is surfaced unchanged | PLANNED_NOT_RUN — D fixture required |
| MC-AT-12 | Lifecycle conflict | E does not choose lifecycle; D conflict/defer is preserved | PLANNED_NOT_RUN — D fixture required |
| MC-AT-13 | PermissionEpoch mismatch/revocation | Fail closed; stale authorization cannot dereference, publish or disclose | PLANNED_NOT_RUN — I fixture required |
| MC-AT-14 | Forget Fence race/conflict | Fence-first blocks; ambiguous/unknown remains private; no post-fence publication | PLANNED_NOT_RUN — D/I/Storage fixture required |
| MC-AT-15 | Stable serialization | Same candidate/profile yields byte-identical bytes and digest | PLANNED_NOT_RUN |
| MC-AT-16 | Serialization round trip | Decode/encode preserves semantic fields, metadata, refs, Unicode and extensions | PLANNED_NOT_RUN |
| MC-AT-17 | No silent information loss | Field inventory before/after is equal or each loss is an explicit error/unresolved reason | PLANNED_NOT_RUN |
| MC-AT-18 | Idempotency replay | Same key/digest returns prior receipt; same key/different digest is conflict | PLANNED_NOT_RUN |
| MC-AT-19 | Recompile after policy/model change | New attempt/revision; old candidate and receipts remain immutable | PLANNED_NOT_RUN |
| MC-AT-20 | Model output with fabricated span/instruction | Reject fabricated locator; embedded instructions remain inert source data | PLANNED_NOT_RUN |

A future Runtime evidence package must include exact source/head SHA, reproducible commands, test output/CI run, fixtures, failure-path coverage and independent read-back. The two consumer-mapping-blocked rows cannot be relabelled PASS by mock data, candidate-only tests or owner silence.

## 26. Runtime implementation entry prerequisites

A pure Rust reference pipeline exists at `crates/memory-compiler`; it is not a production Runtime integration. Issue #7 is CLOSED / not_planned in its latest GitHub state; its controlling implementation binding remains DEFERRED_TO_ENGINEERING_PHASE. This architecture work does not reopen Issue #7, change its state or authorize additional Runtime implementation.

Before production Runtime/conformance work begins, project authority and accountable engineering leadership must record: (1) canonical Runtime repository and active branch or authorized creation decision; (2) named accountable engineering owners/maintainers for D/E/F/G/H/I/Storage and coordinating components; (3) reproducible build/CI/test commands and authoritative artifact SHA; (4) deployed topology, environments, databases, queues, indexes, replicas and backup/restore; (5) contract-to-code traceability ownership; (6) exact B/D/I/H/Storage decisions and interface pins required by each implementation; and (7) executable fault hooks and acceptance fixtures for retry, concurrency, permission revocation, Forget races, visibility uncertainty and restore.

Until those prerequisites are authorized, this contract is architecture preparation only. No Runtime code, placeholder implementation, production data access/write, test PASS, production conformance or production activation is claimed.

## 27. Architecture completion boundary and remaining decisions

The E-owned Candidate IR, validation, compile/validate/serialize semantics, lifecycle flow and test plan are documented here as a reviewable proposal. The Owner semantic direction Option A + I1 is approved and merged in PR #446. The B ADR is superseded as the live semantic decision request; exact D/I/Storage/H consumer contracts still require version-pinned reconciliation and review before canonical mapping or schema freeze. Architecture completion for the full cross-owner mapping remains PARTIAL. The standalone acceptance-plan document is not created because the current compiler overview can carry the matrix without inventing a new normative document location.
