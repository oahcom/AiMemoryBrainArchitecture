# Memory Compiler Overview

- Document ID: E-COMPILER-001
- Version: 1.0
- Source branch: session-e-memory-compiler-2026-11-16
- Source revision: DEREFERENCED — historical source blob `35a766fae29c0b8ddf692a6ec062762f0fca29d2` retained; no current normative source path exists.
- Source branch head audited: a1b8ba129ef7d5f4463bd4229667f0b2bf6d9886
- Source: DEREFERENCED — original normative path `04-memory-compiler/compiler-overview.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/04-memory-compiler/compiler-overview.md) (blob `7aced742e4b1130a857399ccb96c836273c9694e`; translation only, not an authoritative substitute).
- Chinese counterpart: [Memory Compiler 总览](../../zh-CN/04-memory-compiler/compiler-overview.md)
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

- OPEN: INT-P0-01 Fact/Claim ADR; Candidate proposition mapping remains unfrozen.
- OPEN: INT-P1-02 Claim identity/revision and ConflictSet canonical shape.
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
- B Fact/Claim mapping remains ADR-BLOCKED. CandidateEnvelope/CandidateProposition remain pre-canonical IR.
- See accepted-receipt-and-idempotency-contract.md and forget-fence-and-derived-registration.md for detailed CANDIDATE contracts.
