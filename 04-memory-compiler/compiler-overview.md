---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Owner authorized this root source/mirror topology in PR #429 comment 7061562608; content acceptance, bilingual semantic parity, independent review and CI remain pending."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Canonical
    canonical_scope: "Memory Compiler design specification: compiler-overview"
    canonical_scope_id: memory-compiler/compiler-overview
    canonical_scope_keywords:
      - candidate-ir
      - canonical-schema
      - fact
      - claim
      - identity
      - lifecycle
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/compiler-overview.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/compiler-overview.md"
---

# Memory Compiler Overview

- Document ID: E-COMPILER-001
- Version: 1.2
- Canonical root source restored from verified historical E source Blob `35a766fae29c0b8ddf692a6ec062762f0fca29d2`, then reconciled with accepted #429 English mirror revisions, the current five-stage contract and #459 lifecycle overlay.
- Batch-base English mirror Blob: `c89a256afda105ceac3db75d743ab58d177ef586`; ZH-CN mirror Blob: `82d5def36f41bf068420d47a450a00ef32979c47`.
- Stage A frozen-snapshot validation base: `c58878fce24528a0842b4f8887c93ddbf465b566`.
- Canonical language mirrors: [English](../docs/en/04-memory-compiler/compiler-overview.md) and [简体中文](../docs/zh-CN/04-memory-compiler/compiler-overview.md); both are Non-Canonical mirrors of this root source.
- Current-snapshot five-stage contract: EN Blob `6d733294232a93aa59123009d2a2801d9b83f459`; ZH-CN Blob `ad386cac5636b4ba3eaf8b93ad93afcb444e8b46`.
- Current-main Rust reference at Stage B base `d647e7d5eff0049fd6b223908f27d674b6c9f5f1`: `lib.rs` Blob `dc6b756a1c54059c1fd64ee71763289c1f2f260f`; `admission.rs` Blob `7143caf157a37b6d6643ab5d91c2a736a317f127`.
- #459 execution-lifecycle overlay merge: `59c15db9c0ea13f86b05b1f30ab0b4973a49e4dd`.
- Status: Ownership/safety invariants and the five-stage topology DECIDED; detailed orchestration CANDIDATE; model routing/throughput/resource budgets TO_VALIDATE
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

CandidateProposition remains neutral pre-canonical extraction IR. It records proposition structure, modality, polarity, subject/object hypotheses, evidence pointers, source epistemic basis and qualifications. The Owner-approved semantic direction is Option A + I1 (separate Fact attestation; stable ClaimRef with immutable ClaimRevisionRef), but E does not instantiate canonical identities or implement the mapping. Exact B/D/I/Storage/H consumer contracts and schema/compatibility gates remain open; no canonical output schema is frozen.

### 6.3 Stage receipt

Each stage records input/output digest or reference, stage version, deterministic/model-assisted mode, actor/method, start/completion time, attempt, authorization/fence epoch, and terminal/retryable result. Raw source payload is not copied into ordinary logs.

## 7. Pipeline / state machine

~~~mermaid
flowchart TD
 A[Durably Accepted Event + Receipt + Intent] --> B[Ingestion]
 B --> C[Extraction]
 C --> D[Normalization]
 D --> E[Staging / PREPARED_HIDDEN]
 E --> F{PublicationGate}
 F -->|owner evidence permits| G[Publication disposition]
 F -->|defer / reject / unknown| H[Keep private; reasoned outcome]
 P[(Provenance — cross-cutting)] -. records immutable lineage .-> B
 P -. records immutable lineage .-> C
 P -. records immutable lineage .-> D
 P -. records immutable lineage .-> E
 P -. records immutable lineage .-> F
~~~

The five named stages are Ingestion → Extraction → Normalization → Staging → PublicationGate. Evidence creation, entity/relation hypotheses, consolidation and conflict proposals are responsibilities within those stages, not additional pipeline stages. Provenance is cross-cutting and accompanies every stage output; it is not a sixth stage.

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

- DECIDED: Owner/B/D/I semantic direction Option A + I1. The B ADR is historical evidence, not the live semantic decision request.
- OPEN: B schema-freeze/consumer gate; D immutable-revision transaction, currentness and migration/compatibility; I exact attestor authorization, retention and Forget mapping; and version-pinned B/D/E/F/G/H/I/Storage consumer acceptance.
- OPEN: D ConflictSet lifecycle and canonical schema/consumer contract; no field-level schema is frozen.
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

**Status:** E-owned architecture contract extension / PROPOSED. This section records the Owner-approved Option A + I1 semantic direction but does not approve a cross-owner schema, freeze consumer mappings, or authorize Runtime implementation.

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

The merged Owner decision `OWNER-DECISION-FACT-CLAIM-001` and the B/D/I owner acceptances (PR #446; comments 7060251435, 7060243632 and 7060259541) approve Option A + I1 as the semantic direction. The B ADR is retained as historical evidence, not the live semantic decision request. This does not freeze JSON Schema, DDL, storage layout, public APIs, H wire fields or Runtime behavior. B schema-freeze/consumer acceptance remains OPEN; D immutable-revision transaction/currentness and migration/compatibility remain OPEN; I exact attestor authorization, retention and Forget mapping remain OPEN. CandidateProposition and CandidateEnvelope therefore remain neutral pre-canonical IR, and E MUST NOT perform canonical mapping until the exact owner contracts are version-pinned and reviewed.

## 22. Fact/Claim semantics — approved direction; consumer mapping remains open

Fact and Claim MUST remain semantically distinct in the candidate model:

- **Claim candidate:** a proposition asserted, reported, inferred, disputed or retracted by a source. It is not a guarantee of truth. Subject/predicate/object hypotheses, polarity, modality, qualifiers, Scope, time, epistemic basis and evidence lineage remain explicit.
- **Fact/attestation candidate:** a possible adjudication/attestation about an exact proposition/revision, with candidate references to attestor, method/version, evidence, Scope, validity and decision history. This is a conceptual candidate only; E does not define or instantiate a canonical Fact identity or lifecycle.
- **CandidateProposition:** neutral extraction IR. Option A + I1 is the approved semantic direction (separate Fact attestation; stable ClaimRef and immutable ClaimRevisionRef), but this candidate artifact does not instantiate canonical identities or decide field-level schema.

The merged Owner decision record `OWNER-DECISION-FACT-CLAIM-001` (main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`; PR #446 merge commit `ad5ca81a32b413aef3f9b5bccd06030aabde8275`) selects Option A — separate Fact attestation and Claim proposition — with I1 — stable ClaimRef plus immutable ClaimRevisionRef. B, D and I accepted this semantic direction in Owner comments 7060251435, 7060243632 and 7060259541. The B ADR is historical evidence, not the live semantic decision request. The non-decisions remain material: B schema-freeze and consumer acceptance; D immutable-revision transaction/currentness, migration and compatibility; I exact attestor authorization, retention and Forget mapping; and all B/D/E/F/G/H/Storage consumer contracts remain OPEN pending version pins and review. D owns canonical ID allocation, revision commit/currentness, lifecycle, ConflictSet lifecycle and D ForgetFence authority. I owns authorization, PermissionEpoch, attestor authorization, revocation, retention and global Forget policy/completion. H transports opaque owner-issued references; F/G consume exact revision-pinned references; Storage owns its physical transaction/visibility contract. No JSON Schema, DDL, storage layout, public API, wire field or Runtime mapping is approved.

The candidate alternatives are:

| Option | Meaning | D impact | I impact | Disposition |
|---|---|---|---|---|
| A — separate Fact attestation object | Fact has its own canonical identity/revision and binds exact ClaimRevisionRef(s), authorized attestor, method, evidence, Scope and validity | Requires D-owned identity, lifecycle, versioning, reference integrity and Forget dependency rules for Fact and Claim revisions | Requires I-approved attestor authorization, PermissionEpoch recheck, evidence access/retention and global Forget policy | **Owner-approved semantic direction (PR #446); exact mapping remains Candidate** |
| B — Fact as a qualified view of an exact ClaimRevision | No separate Fact identity; a view/qualification is derived from a precise Claim revision and declared predicate | Lower identity/storage complexity, but D must define exact revision and lifecycle semantics for the view | I still governs authorization, policy and evidence retention; view must not imply permission or truth | Not selected; requires a superseding Owner decision |
| N — neutral pre-canonical output | Preserve CandidateProposition and attestation evidence as candidate-only references; do not mint canonical Fact/Claim IDs or map fields | D allocates IDs and owns revisions/lifecycle only under its accepted contracts | I authorization, attestor, retention and Forget controls remain authoritative | **Required E behavior until exact B/D/I/Storage/H consumer contracts and schema gates are accepted** |

E does not select domain semantics. The Owner has approved Option A + I1 as the semantic direction. Therefore E MUST continue to emit neutral CandidateProposition and MUST NOT perform canonical Fact/Claim mapping until the responsible D/I/Storage/H consumer contracts, migration/compatibility and conformance evidence are version-pinned and reviewed. Text similarity, extraction confidence or a model label such as “fact” never grants canonical identity or attestation authority.

### 22.1 Outstanding owner-contract mapping and acceptance

- **SEMANTIC_DIRECTION:** DECIDED — Option A + I1, accepted by the Project Owner and B/D/I Owner sessions (PR #446; comments 7060251435, 7060243632 and 7060259541).
- **B:** semantic baseline accepted; schema-freeze conditions and exact consumer acceptance remain OPEN. The B ADR is historical evidence, not the live semantic decision request.
- **D:** owns canonical IDs, immutable revisions, currentness, lifecycle, ConflictSet lifecycle and D ForgetFence authority; immutable-revision transaction/currentness, migration and compatibility contracts remain OPEN.
- **I:** owns authorization, PermissionEpoch, attestor authorization, revocation, retention and global Forget policy/completion; exact attestor/retention/Forget consumer mapping remains OPEN.
- **H:** transports opaque owner-issued references; no wire fields or protocol schema are frozen here.
- **F/G:** consume exact revision-pinned references; no mutable latest-head substitution. Exact consumer acceptance remains OPEN.
- **Storage/Consistency:** owns physical transaction and visibility realization under its accountable contract; no E-local receipt proves cross-service atomicity.
- **E boundary:** continue emitting neutral CandidateProposition/ExtractionIR. No canonical ClaimRef/ClaimRevisionRef/FactRef/FactRevisionRef minting, no mapping by confidence, and no publication without the D/I/Storage owner gates.
- **Required evidence:** version-pinned B/D/I/H/Storage consumer artifacts, migration/compatibility disposition and independent semantic review before mapping or schema freeze. Until then, mapping acceptance tests remain PLANNED_NOT_RUN / NOT AUTHORIZED.
## 23. End-to-end compiler lifecycle and data flow

| Stage | Input → output | Owner | Preconditions and authority | Failure/retry and data status |
|---|---|---|---|---|
| Raw source / durable ingress | Source bytes or reference + metadata → immutable EventRef, Accepted receipt, compile intent | H/I for authenticated envelope and policy; E for E-owned ingress semantics; durable store for custody | Authenticated producer, resolved Scope, idempotency and durable acceptance | Before Accepted: reject without claiming custody. After Accepted: preserve durable source/work; retry by stable identity |
| Candidate IR | Accepted source bundle → ExtractionIR/CandidateEnvelope and stage receipts | E | Source digest/version, current access context, pinned parser/policy; no canonical identity | Partial/unresolved is explicit; retry same digest idempotently; changed input/method creates new attempt |
| Validation | Candidate + trusted validation context → field-addressed ValidationReport | E, consuming D/I/H references | Structural/provenance/scope checks; authoritative current I permission and D fence must be checked at protected boundaries | Invalid is permanent until corrected; stale authority/fence fails closed; transient dependency outage may retry |
| Mapping gate | Valid neutral candidate → owner-contract-approved mapping path or private deferred candidate | B semantic direction is decided; D owns canonical mapping; I constrains authorization; E adapts | Exact version-pinned B/D/I/H/Storage consumer contracts and compatibility evidence | Until those pins are reviewed, remain private and report a contract-gate outcome; no heuristic mapping |
| Canonical Schema boundary | CanonicalWriteRequest → D-issued canonical IDs/revisions/commit result or reasoned defer/reject | D; I/Storage participate at their boundaries | D expected-version/lifecycle rules; current I PermissionEpoch; D/I Forget Fence; complete dependency and Storage visibility protocol | Conflict/defer/reject returned explicitly; unknown outcome queried by stable operation key; E never fabricates success |
| Candidate serialization | Valid Candidate IR + pinned profile → deterministic candidate bytes + digest | E for internal candidate format; H for wire; D/Storage for canonical persistence format | Versioned profile and lossless representability; canonical schema remains separately governed | Unsupported profile/field fails explicitly; same input/profile produces same bytes; round-trip preserves semantic content |

Pipeline summary: Raw Memory/Source → durable Accepted boundary → Ingestion → Extraction → Normalization → Staging → PublicationGate, with Provenance cross-cutting. Candidate-to-canonical mapping occurs only through separately approved B/D/I/Storage/H contracts; until then a valid private Candidate result may terminate as deferred and must never be promoted by fallback.

## 24. Language-neutral interface contract for future Runtime

These are semantic contracts, not Rust signatures, frozen API schemas or implementation authorization.

### Existing Workspace Rust reference pipeline — main readback

The current Workspace contains `crates/memory-compiler/src/lib.rs` (main Rust pipeline Blob `dc6b756a1c54059c1fd64ee71763289c1f2f260f`). The Rust pipeline is the single reference implementation. The `admission` reference implementation is pinned separately at Blob `7143caf157a37b6d6643ab5d91c2a736a317f127`. `AdmissionStore::open()` opens a WAL-backed file database with `synchronous=FULL`; `in_memory()` is for isolated tests. The current `compile()` path reads caller-pre-registered local producer-work and dependency receipts, then writes a local publication receipt after the injected `PublicationAuthority` admits the derivative. These are local reference-ledger operations, not D's authoritative producer registry/Forget Fence, I's permission authority or Storage's visibility/commit authority, and do not establish cross-service atomicity. Production D/Storage/I authority integrations remain unimplemented.

- `MemoryCompiler<A>::compile()` composes all five stages, but now also requires caller-pre-registered producer-work and complete dependency receipts in the local `AdmissionStore`; it derives staging admission fields from that ledger and writes a local publication receipt after the injected `PublicationAuthority` returns `Published`.
- No public `MemoryCompiler::validate()` or `MemoryCompiler::serialize()` method exists in this source snapshot. The language-neutral `validate` and `serialize` contracts below are target semantics, not current callable APIs.
- `PublicationAuthority` is an injected trait; the crate contains no production D/Storage/I authority implementation.
- Historical reference-crate evidence: 31 unit tests were reported on snapshot `713774c381effbbe9e70693f88a7fa99a33a040d`; that result is not transferred to this validation batch. The exact command must be re-run on the new head. These crate tests do not satisfy the full MC-AT matrix or prove production authority integration.
- The originally requested legacy paths `src/memory/compiler.rs` and `tests/compiler_test.rs` are absent; the actual Workspace path is the crate above.

This is real reference code and test evidence, not production integration or authorization to extend Runtime behavior.

### compile

- **Input:** an AcceptedSourceBundle containing immutable source/event/content references, digest, accepted-receipt and compile-intent references, trusted ActorRef/ScopeRefs, source metadata and pinned compile policy/profile versions.
- **Output:** CompileResult containing candidate references, stage receipts, explicit completeness/outcome and field-addressed diagnostics; no Canonical Record is implied.
- **Errors:** malformed/empty/unsupported input, missing source, scope denial, stale PermissionEpoch, Forget Fence block, idempotency conflict, unresolved ambiguity, missing evidence, ADR mapping block and retryable dependency failure.
- **Invariants:** same stable work identity + same digest/profile is idempotent; changed digest/profile creates a new attempt/revision; no valid source information is silently dropped; Accepted is not Compiled or CanonicalCommitted.
- **Side effects:** may create E-owned work/stage/candidate records and private staging artifacts; may not directly write canonical records or expose derivatives.
- **Permission/idempotency:** uses owner-issued current authorization and fence evidence; stable producer-work identity survives retry/replay; D/I/Storage gates govern publication.
- **Dependencies:** H ingress identity/envelope; I authorization, PermissionEpoch and attestor policy; D producer registration, canonical identity/revision/currentness/lifecycle and Forget Fence; Storage durability/visibility; B semantic baseline and schema/consumer acceptance.

### validate

- **Input:** CandidateEnvelope/ExtractionIR plus the exact source/evidence references and a validation context carrying opaque, current owner-issued authorization/fence evidence where protected reads or boundary checks are required.
- **Output:** ValidationReport with VALID, PARTIAL, INVALID, UNSUPPORTED, STALE_AUTHORITY or BLOCKED_BY_OWNER_CONTRACTS disposition and stable error code + field/path/reference for each finding.
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

All rows below remain planned acceptance-matrix scenarios, not executed matrix results. The 31 Rust reference-crate unit tests are separate evidence and do not satisfy or relabel any MC-AT row. Production Runtime integrations remain NOT AUTHORIZED in this phase.

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
| MC-AT-09 | Fact/Claim mapping boundary | Option A + I1 semantics are preserved; no canonical IDs or field mapping until exact B/D/I/Storage/H consumer contracts and schema gate are reviewed | PLANNED_NOT_RUN / NOT AUTHORIZED — owner-contract gate open |
| MC-AT-10 | ClaimRef / ClaimRevisionRef / FactRef / FactRevisionRef mapping | Exact D transaction/currentness and compatibility plus I attestor/retention/Forget contracts are pinned and accepted before conformance | PLANNED_NOT_RUN / NOT AUTHORIZED — owner-contract gate open |
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

A Rust reference pipeline with a local SQLite admission ledger exists at `crates/memory-compiler`; it is not a production Runtime integration. Issue #7 is CLOSED (`not_planned`) in its latest GitHub state; its controlling implementation binding remains `DEFERRED_TO_ENGINEERING_PHASE`. This architecture work does not reopen Issue #7, change its state or authorize additional Runtime implementation.

Before production Runtime/conformance work begins, project authority and accountable engineering leadership must record: (1) canonical Runtime repository and active branch or authorized creation decision; (2) named accountable engineering owners/maintainers for D/E/F/G/H/I/Storage and coordinating components; (3) reproducible build/CI/test commands and authoritative artifact SHA; (4) deployed topology, environments, databases, queues, indexes, replicas and backup/restore; (5) contract-to-code traceability ownership; (6) exact B/D/I/H/Storage decisions and interface pins required by each implementation; and (7) executable fault hooks and acceptance fixtures for retry, concurrency, permission revocation, Forget races, visibility uncertainty and restore.

Until those prerequisites are authorized, this contract is architecture preparation only. No Runtime code, placeholder implementation, production data access/write, test PASS, production conformance or production activation is claimed.

## 27. Architecture completion boundary and remaining decisions

The E-owned Candidate IR, validation, compile/validate/serialize target semantics, five-stage lifecycle flow and test plan are documented here. Option A + I1 is DECIDED by the Project Owner and accepted by B/D/I; the B ADR remains historical evidence. Exact B schema-freeze/consumer acceptance, D transaction/currentness and compatibility, I attestor/retention/Forget mapping, and all cross-owner consumer contracts remain OPEN. E continues to emit neutral CandidateProposition/ExtractionIR only. Architecture completion for cross-owner mapping remains PARTIAL; no Runtime, schema, DDL, public API or wire freeze is authorized.

## 28. Execution-state, retry, lease and recovery overlay — #459 boundary

The compiler topology remains exactly five stages: **Ingestion → Extraction → Normalization → Staging → PublicationGate**. Provenance remains cross-cutting and accompanies stage outputs; it is not a sixth stage. The stage names, typed stage outputs and ownership boundaries in the pinned [Compiler Stage Contract](../docs/en/04-memory-compiler/compiler-stage-contract.md) are unchanged.

PR #459 adds an execution-lifecycle overlay across those stages: operation identity, current stage, execution state, attempt generation, lease generation, retry transition and recovery metadata. These are lifecycle/control-plane concerns, not additional compiler transformations or stage outputs.

### 28.1 What the merged Rust reference implements

At #459 merge `59c15db9c0ea13f86b05b1f30ab0b4973a49e4dd`, the Rust reference represents execution metadata in `StageExecution` (`operation_id`, `stage`, `state`, `attempt_generation`, `last_durable_stage` and optional `lease`). State advancement checks the local transition graph. `retry()` is limited to `Failed`/`Blocked`, increments the attempt generation, returns to `Pending` and clears the lease. Lease-currentness is checked against the supplied generation. These are in-memory reference values and transitions, not a production lease service or durable execution ledger.

The current `MemoryCompiler::compile()` path is now wired to the local SQLite `AdmissionStore`: the caller must pre-register producer work and dependency edges; `compile()` reads and validates those local receipts, derives staging-admission flags and dependency IDs from the ledger (not caller-supplied booleans), executes the five stages and injected `PublicationAuthority`, then records a local publication receipt through `final_publication_gate()`. `AdmissionStore::open()` is WAL-backed with `synchronous=FULL`; `in_memory()` is used for isolated tests. This ledger is not D-authoritative producer registration, D-owned ForgetFence, I PermissionEpoch authorization or Storage commit/visibility authority.

The implemented `MemoryCompiler::resume` is deliberately narrower than arbitrary-stage recovery:

- Its `StagingInput` must already contain an available `NormalizedIR`; the API does not reconstruct that value from a durable store.
- It rejects terminal execution state and validates operation/lease/generation consistency.
- It validates `last_durable_stage` only as a known enum value. Neither `last_durable_stage` nor `StageExecution.stage` selects a stage-specific resume branch.
- It always runs `StagingStage` followed by `PublicationGate` from the supplied normalized result.
- This `resume` path is separate from `compile()`; it does not reconstruct `NormalizedIR` from `AdmissionStore` or persist a local publication receipt.
- `StageExecution::record_durable()` only assigns the in-memory `last_durable_stage` marker; it does not persist a durable stage result or next-stage intent.

Therefore the current `resume` code demonstrates only a bounded in-process continuation from a supplied normalized result. It does **not** demonstrate recovery from arbitrary last-durable stages, complete crash recovery, durable execution retry/replay, durable lease ownership, commit-outcome resolution or cross-service publication atomicity. The local SQLite admission ledger persists producer/dependency/publication receipts only; it does not persist `StageExecution`, stage results or next-stage intents. The reference crate has no production durable execution store, production lease provider, authorization service or D/I/Storage publication authority integration.

### 28.2 Normative recovery requirements remain stronger

The pinned Compiler Stage Contract §6.3 remains the normative target: a completed stage must have a durable result and recoverable next-stage intent; recovery must identify the last durable stage result and resume from that result without repeating an externally visible effect. The #459 in-memory marker and bounded `resume` implementation do not satisfy or prove those durability requirements. Production conformance requires separately authorized persistent execution records, durable stage results/intents, lease-provider semantics, authoritative permission/Forget checks, publication-outcome resolution and D/Storage cross-service integration. None is authorized or claimed by this architecture-only PR.

PR #459's merged verification reported 31 compiler tests and 141 workspace tests passing. That is evidence attached to #459's merge, not a new #429 exact-head result and not proof of durable recovery or production integration. This PR separately reports its own exact-head test commands and outputs.
