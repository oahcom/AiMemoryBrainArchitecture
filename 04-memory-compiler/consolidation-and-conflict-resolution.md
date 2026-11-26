---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-e-memory-compiler-2026-11-16"
        - "source commit: ee098e14747d9915de5b3efb63b3a8dd77f670ed"
        - "original source blob: d16f8e2e41a6cca81ad285e5f79f075d87e64edb"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact E source Blob pinned; Owner exact-version and dependency review pending."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Candidate
    canonical_scope: "Memory Compiler consolidation and conflict resolution"
    canonical_scope_id: memory-compiler/consolidation-and-conflict-resolution
    canonical_scope_keywords:
      - consolidation
      - conflict-resolution
      - canonical-authority
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/consolidation-and-conflict-resolution.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/consolidation-and-conflict-resolution.md"
---

# Consolidation and Conflict Resolution

**Status:** DECIDED for no-silent-overwrite, evidence preservation and canonical authority boundaries; CANDIDATE for matching and scoring policies; OPEN for Claim identity/revision and Conflict Set schema.  
**Owner:** Memory Compiler / MC-04.  
**Integration:** INT-P0-01/02/03; INT-P1-02/04/06; AR-004.

## 1. Purpose

Evaluate candidate propositions and memories against authorized canonical assets to identify duplicates, related claims, temporal coexistence, revisions and genuine conflicts. Produce auditable proposals for D's Canonical Memory/Lifecycle authority. Consolidation is not blind deduplication and conflict detection is not truth adjudication.

## 2. Scope

Includes candidate grouping, duplicate detection, entity-resolution collaboration, Claim revision proposals, conflict-set proposals, Evidence comparison, policy-based consolidation recommendations, human/Agent review routing, canonical write request preparation, and post-commit projection notification.

Excludes final Claim identity, Conflict Set canonical schema and lifecycle authority (D), entity merge/split authority (D's Entity Manager), runtime relevance ranking (F), Context editing (G), and governance/retention authorization (I).

## 3. Responsibilities

Build candidate comparison sets only after Scope and permission filtering; distinguish exact duplicate, paraphrase, related proposition, temporal update, revision and contradiction; compare subject/predicate/object/polarity, modality, Scope, Environment, valid-time overlap, epistemic status and Evidence; preserve supporting/refuting/qualifying Evidence and common ancestry; ask Entity Manager to resolve identity; create explicit ConflictSet and ClaimRevision proposals; defer uncertain/high-impact decisions to authorized review; submit version-checked canonical writes.

## 4. Non-Responsibilities

Compiler does not decide canonical truth, promote claims to Verified based on confidence, silently overwrite prior claims, independently merge entities, erase superseded history, set final lifecycle state, or let an LLM make authorization/lifecycle decisions.

## 5. Inputs / Outputs

**Inputs:** CandidateEnvelope and ExtractionIR; Evidence/Provenance; authorized canonical candidate set; Entity/Relation responses; D's current version/lifecycle state; Scope/Permission context; policy and vocabulary versions.

**Outputs:** ConsolidationProposal; DuplicateAssessment; ClaimRevisionProposal; ConflictSetProposal; EvidenceComparison; EntityResolutionRequest; CanonicalWriteRequest; ReviewTask; Commit/Deferred/Rejected result; IndexPublicationRequested event.

## 6. Data Model

### 6.1 ConsolidationProposal

~~~text
ConsolidationProposal {
  proposal_id: OpaqueId
  scope_refs: ScopeRef[]
  candidate_refs: TypedObjectRef[]
  target_memory_ref: TypedObjectRef?
  proposed_operation: create | append_claim | revise_claim |
                     supersede | relate | split_candidate | defer
  duplicate_assessments: DuplicateAssessment[]
  revision_proposals: ClaimRevisionProposal[]
  conflict_set_proposals: ConflictSetProposal[]
  evidence_comparisons: EvidenceComparison[]
  entity_resolution_refs: TypedObjectRef[]
  expected_canonical_version: VersionRef?
  policy_version: Version
  method_refs: MethodRef[]
  decision_rationale_refs: TypedObjectRef[]
  created_at: Instant
}
~~~

### 6.2 ConflictSetProposal (CANDIDATE, D-owned final schema)

~~~text
ConflictSetProposal {
  proposal_id: OpaqueId
  scope_refs: ScopeRef[]
  participant_proposition_refs: TypedObjectRef[]
  conflict_dimensions: subject | predicate | object | polarity |
                       temporal_overlap | source_disagreement |
                       modality | scope_incompatibility
  temporal_intersection: TimeInterval?
  supporting_evidence_refs: TypedObjectRef[]
  refuting_evidence_refs: TypedObjectRef[]
  common_ancestry_refs: TypedObjectRef[]
  state: unresolved | review_required | resolved_proposal
  proposed_resolution: retain_both | select_successor | retract |
                       narrow_validity | mark_disputed | no_conflict
  rationale: String
  method_refs: MethodRef[]
}
~~~

Final Conflict/Conflict Set identity, revision and lifecycle are blocked on INT-P1-02/D. This proposal does not freeze D's schema.

### 6.3 ClaimRevisionProposal (CANDIDATE)

~~~text
ClaimRevisionProposal {
  prior_claim_ref: TypedObjectRef
  proposed_claim_ref: TypedObjectRef
  relation: correct | refine | supersede | retract | reinstate
  reason: String
  evidence_refs: TypedObjectRef[]
  expected_claim_or_memory_version: VersionRef
  scope_refs: ScopeRef[]
  temporal_effect: TimeInterval?
  provenance_ref: TypedObjectRef
}
~~~

This supports either stable Claim identity plus immutable revisions or successor Claim identity. It must be mapped after D resolves the policy.

## 7. Pipeline / State Machine

~~~mermaid
flowchart TD
 A[Candidate + Evidence] --> B[Resolve and authorize Scope]
 B --> C[Generate comparable canonical set]
 C --> D[Entity identity resolution]
 D --> E[Exact / semantic duplicate assessment]
 E --> F[Temporal + epistemic comparison]
 F --> G[Conflict / revision proposal]
 G --> H{Policy confidence and impact}
 H -->|routine safe| I[Prepare Canonical Write]
 H -->|ambiguous/high impact| J[Human or Agent review]
 H -->|insufficient evidence| K[Defer / retain candidate]
 I --> L[D lifecycle + version-checked commit]
 J --> L
 L -->|committed| M[Canonical change outbox]
 L -->|stale/conflict| N[Reload and reconcile]
 M --> O[Index publication request]
~~~

States: PROPOSED → SCOPE_FILTERED → MATCHED → ASSESSED → REVIEW_PENDING or WRITE_PENDING → COMMITTED / DEFERRED / REJECTED / STALE_RECONCILE. Every state is persisted with attempt and policy version.

## 8. Invariants

Scope filters precede comparison-set generation, graph expansion, similarity search and aggregation. Different users or incompatible Environment Scopes are never consolidated absent explicit sharing. Same label or embedding proximity does not prove Entity identity. Intent/plan/prediction/attempted action are not outcomes. A contradiction is not inferred when valid-time intervals do not overlap or scopes/modalities differ. Conflicting Claims are never silently overwritten. Evidence ancestry is considered. Confidence and semantic similarity do not equal truth or verification. Canonical write uses D's expected version/lifecycle contract. Canonical commit and index visibility are separate milestones.

## 9. Idempotency

Proposal identity derives from sorted candidate refs + source digests + canonical target/version + Scope + policy/method versions. Same inputs return same logical proposal. Changed canonical version or policy creates a new proposal revision. Commit request has stable operation key; same key/same payload returns prior commit; same key/different payload conflicts. Retry after unknown commit outcome queries D before retrying.

## 10. Consistency

Consolidation reads a scoped canonical snapshot/generation. Candidate set records its generation and policy version. Canonical write includes expected target version and source lineage. D commits immutable Memory Version/current pointer atomically with required Claim/Evidence/Provenance references and outbox. If index publication fails, canonical remains authoritative and index watermark remains behind. No transaction spans D, model provider and index; recoverable outbox/replay is required.

## 11. Failure Recovery

Ambiguous entity resolution retains hypotheses and defers; changed canonical generation rebuilds comparison set; stale version triggers reload/re-assessment; conflict detector outage retains candidate; review outage keeps review-pending; unavailable Evidence lowers eligibility or defers; model outage allows deterministic checks; Forget fence cancels comparison and suppresses proposal/replay; unknown commit outcome queries D; index outage preserves outbox and retries.

## 12. Security / Scope

Authorize reads of all candidate and canonical participants before they enter comparison sets. No cross-scope embedding or graph matching. Scope must be compatible under D/I policy; Environment Scope is a hard partition for environment-dependent propositions. Evidence refs require separate permission. Async review/write workers re-check grants, revocation epoch and Forget fence. Review tasks disclose only authorized excerpts. Content remains untrusted; instruction-like text cannot trigger review action, tool call or privilege escalation.

## 13. Performance / Backpressure

Use cheap deterministic blocking keys first (Scope, entity refs, predicate/type, time bucket, source identity), then bounded lexical/semantic candidate expansion. Cap candidate count, graph depth, fan-out, model comparisons, review queue and per-scope concurrency. Semantic similarity is candidate generation only. Under overload, defer low-priority consolidation while preserving candidate/provenance; never weaken Scope filters. Measure false-duplicate, false-conflict, missed-conflict, review rate, canonical conflict rate, fan-out, time-to-commit and resource use. Thresholds are TO_VALIDATE.

## 14. Observability

Record proposal ID, candidate/target refs (protected in traces), Scope class, canonical generation, policy/method version, duplicate/conflict classifications, Evidence ancestry summary, review status, expected/actual version, commit result, index generation, retries and latency. Metrics avoid high-cardinality IDs and sensitive proposition text. Audit revision/retraction/merge proposals and final D decisions with actor/reason.

## 15. Interfaces

### 15.1 D — Canonical Write Contract

Candidate request fields: request_id, schema_version, actor_ref, scope_refs, environment_scope_ref, operation/idempotency key, expected_memory_version or expected_claim_revision, candidate object mapping after ADR, entity/relation refs, evidence_refs, provenance_refs, conflict_set_refs/proposals, temporal/epistemic qualifiers, source event refs, policy/method refs, correlation/causation IDs.

D response: committed/deferred/rejected/stale; canonical memory/version refs; claim revision refs; lifecycle decision and reason; commit generation; outbox event ref. Errors: SCOPE_MISMATCH, PERMISSION_DENIED, STALE_VERSION, INVALID_TRANSITION, MISSING_EVIDENCE, PROVENANCE_INCOMPLETE, CONFLICT_REQUIRES_REVIEW, IDEMPOTENCY_CONFLICT, FORGET_FENCE_ACTIVE.

D alone decides canonical IDs, Claim identity/revision, Conflict Set canonical shape and lifecycle state. Compiler retries with same operation key and re-reads after unknown outcome.

### 15.2 F — Index Publication

On canonical commit publish CanonicalCommitCommitted with commit_id, canonical_generation, changed memory/version/claim/entity/relation refs, Scope refs, change kind, Provenance refs and event schema version. F acknowledges applied generation/watermark separately. Index projections include Memory, Entity and Relation, plus Claim/Evidence metadata only where authorized. Stale index generation is detectable; index is rebuildable.

### 15.3 G — Context impact events

Publish MemoryVersionChanged, ClaimRetracted, MemorySuperseded, MemoryArchived, MemoryForgotten, EvidenceRestricted with canonical refs, prior/new version, Scope, event generation, reason code and correlation. G decides whether affected context entries are removed, replaced, qualified or replanned. Compiler does not mutate Context.

### 15.4 H and I

H receives Event Accepted/processing state distinction. I supplies authorization recheck, Forget fence, retention class and deletion obligations. All messages have versioned schema, idempotency, typed errors and replay semantics.

## 16. Test Scenarios

Same entity label across scopes; same Agent in two worlds; paraphrase duplicate vs different temporal claim; overlapping contradictory claims create Conflict Set; non-overlapping claims coexist; copied Evidence not independent; model suggests false merge rejected by Entity Manager; two concurrent canonical writes; stale commit retry; explicit retraction preserves history; Forget during review; index outage after commit; permission revoked before commit.

## 17. Dependencies

D Canonical Memory/Lifecycle/Entity Manager; B Claim/epistemic/time/provenance semantics; I Scope/permission/Forget/retention; F index projection and watermark; G context impact; H Actor/Scope identity; Evidence/Provenance store; Storage/Consistency outbox and generation model.

## 18. Open Questions

- **OPEN:** INT-P0-01 Fact/Claim ADR and output mapping.
- **OPEN:** INT-P1-02 stable Claim ID versus successor revision and canonical Conflict Set model.
- **OPEN:** INT-P1-06 lifecycle authority record and Provenance DAG.
- **CANDIDATE:** deterministic blocking keys + semantic candidate generation + explicit review.
- **TO_VALIDATE:** duplicate/conflict precision and recall, candidate fan-out, human review volume and latency.
- **OPEN:** authorized human/Agent adjudicator and authoritative attestation (D/I).


## 19. Cross-module interface contract details (CANDIDATE until owner approval)

The following is the minimum semantic contract, not a replacement for D/F/G/H/I's owned specifications. All messages are versioned, typed, scope-bound, correlated, and replayable.

| Consumer / producer | Required fields | Version and idempotency | Authorization | Errors | Recovery |
|---|---|---|---|---|---|
| D Canonical Write | request_id, schema_version, actor_ref, scope_refs, environment_scope_ref, source_event_refs, candidate refs, entity/relation refs, evidence_refs, provenance_refs, conflict/revision proposals, expected canonical version, operation key, policy/method refs, correlation/causation | schema_version + domain schema version; same operation key and same canonical payload returns same commit; same key/different payload conflicts | D/I authorize actor, action, all source/evidence refs, target scopes and Forget fence immediately before commit | SCOPE_MISMATCH, PERMISSION_DENIED, STALE_VERSION, INVALID_TRANSITION, MISSING_EVIDENCE, PROVENANCE_INCOMPLETE, CONFLICT_REQUIRES_REVIEW, IDEMPOTENCY_CONFLICT, FORGET_FENCE_ACTIVE | Query operation result after timeout; reload canonical version and re-propose on stale; never blind retry |
| F Index Publication | event_id, schema_version, commit_id, canonical_generation, changed object refs/types, prior/new version refs, scope_refs, change_kind, provenance_refs, recorded_at, correlation/causation | event schema version; unique commit_id + generation; consumer checkpoint/watermark is monotonic | F filters every projection by Scope and per-object permissions; Evidence projections require separate authorization | INVALID_EVENT, SCOPE_DENIED, STALE_GENERATION, GAP_DETECTED, PROJECTION_UNAVAILABLE | At-least-once consume; deduplicate by event_id/commit_id; replay from durable canonical outbox; rebuild projection and publish watermark only after complete application |
| G Context impact | event_id, schema_version, canonical_ref, prior/new version, lifecycle/change kind, scope_refs, generation, reason_code, occurred_at, correlation/causation | unique event_id + canonical generation; duplicate delivery is no-op | G/I re-check current access and Forget/revocation epoch before Context read/write or Adapter delivery | UNKNOWN_CONTEXT, SCOPE_DENIED, STALE_CONTEXT, RECONCILIATION_REQUIRED, FORGET_SUPPRESSED | G owns Context version and reconciliation; E replays event; no Context mutation by E; late/duplicate events cannot regress versions |
| H Accepted / status | schema_version, authenticated producer identity, actor_ref, scope_refs, event/source identity, payload_ref/digest, idempotency_key, source times, retention/sensitivity, correlation/causation; receipt_id/event_id/accepted_at/status | protocol + envelope version; same key/same digest returns same receipt; same key/different digest returns conflict | H authenticates producer; I authorizes event.ingest; E rechecks worker permission | INVALID_ENVELOPE, UNAUTHENTICATED_PRODUCER, SCOPE_INVALID, PERMISSION_DENIED, IDEMPOTENCY_KEY_REUSE_CONFLICT, INGRESS_CAPACITY_EXCEEDED, RETRYABLE_UNAVAILABLE | receipt lookup; durable outbox reconstructs work; processing status is separate from Accepted; replay preserves event identity |
| I authorization / Forget | principal/actor, action, resource refs, scope_refs, policy/revocation epoch, retention_class, forget_operation_ref, fence_epoch, dependency refs, audit correlation | governance policy version and fence epoch; repeated Forget operation is idempotent; monotonic stage progress | I is policy authority; E enforces returned decision at ingress, every worker stage, replay and canonical commit | PERMISSION_DENIED, POLICY_UNAVAILABLE, SCOPE_REVOKED, RETENTION_BLOCKED, FORGET_FENCE_ACTIVE, FORGET_IN_PROGRESS | Fail closed for protected operations; pause/retry workers after policy recovery; durable fence prevents resurrection; completion only from I's target evidence |

### 19.1 Shared error and replay rules

- Errors distinguish permanent rejection, retryable unavailability, stale-version conflict, policy denial, missing dependency and partial projection.
- Error bodies do not disclose protected object existence, content, identifiers or candidate counts.
- Every asynchronous message has stable event/operation identity, attempt metadata and correlation/causation.
- At-least-once delivery is assumed; consumers must deduplicate and commit their checkpoint with their local effect or use an equivalent inbox/outbox protocol.
- A replay is an execution attempt over an existing immutable source/operation identity, not permission to recreate deleted content.
- A Forget fence or authorization revocation invalidates queued work and cached decisions before any further protected dereference or mutation.
- No component may infer success from timeout. Query by stable operation/event ID and reconcile against the authoritative owner.

### 19.2 Ownership and compatibility

D owns canonical object semantics and write decisions; F owns index projection and watermark; G owns Context state; H owns protocol and producer authentication; I owns policy, revocation and retention. E is a producer/consumer at these boundaries, not a second authority. Breaking semantic changes require the owning module's version migration and cross-module conformance update; optional unknown extension fields may be ignored only when they do not alter required semantics.


## 20. Durable receipt, cursor and Forget addendum

- Consolidation consumes only durably Accepted Event identities and versioned compiled candidates. Replaying an existing receipt is not a new Event; replay/recompile creates a new attempt under the same immutable source identity and current authorization.
- Every comparison-set read, entity resolution, review-task creation, canonical write submission and delayed retry checks the current D Forget fence and I authorization epoch. A stale lease/fence epoch suppresses the proposal.
- Canonical write operation identity is stable across retries. If D's response is unknown, query D using the same operation key; never generate a new key to force another canonical effect.
- D alone returns CanonicalCommitted and its canonical cursor. E records the reference but does not allocate or interpret it. F alone confirms Indexed and advances its per-index/per-partition watermark.
- No candidate, conflict proposal, review payload or canonical-write envelope derived from a forgotten source may be newly published after fence activation. Derived dependency registration precedes visibility.
- CandidateProposition/ExtractionIR to canonical Claim mapping remains **ADR-BLOCKED** pending B/Governance approval.
- See `accepted-receipt-and-idempotency-contract.md` and `forget-fence-and-derived-registration.md` for normative E boundary proposals; these remain CANDIDATE until D/H/I/Storage/F owners approve their interfaces.
