---
document_metadata:
  domain: memory-brain
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
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Issue #1177"
        - "source commit: b525e1f8fee2471a131e4a38efda99804045e424"
        - "original source blob: b4ed712ac0626ab127cccfd205c50a9013df01fb"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Existing translated companion body preserved; source pin refreshed; semantic parity review pending."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/memory-brain-overview.md"
    en: null
    zh-CN: "docs/zh-CN/03-memory-brain/memory-brain-overview.md"
---

# Memory Brain — Subsystem Architecture

- Document ID: D-MEMORY-BRAIN-001
- Version: 1.0
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: 3965c1e6c0810ac1850b75a6c08fb966610828e0
- Source branch head audited: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- Source: [canonical D source](../../../03-memory-brain/memory-brain-overview.md) (source commit `b525e1f8fee2471a131e4a38efda99804045e424`; original source blob `b4ed712ac0626ab127cccfd205c50a9013df01fb`).
- Chinese counterpart: [Memory Brain 子系统架构](../../zh-CN/03-memory-brain/memory-brain-overview.md)
- Status: DECIDED for authority boundaries and invariants; CANDIDATE for detailed object/operation contracts; OPEN items remain non-normative
- Owner: Session D — Memory Brain Principal Architecture

## 1. Purpose

Memory Brain is the logical authority for durable, addressable canonical memory assets: Memory identities and immutable versions, Claim/Fact semantics subject to ADR, Entity identities, typed Relations, Evidence references, Provenance lineage, lifecycle history, and domain support for governed Forget/Retention.

It preserves memory assets independently of any Agent, LLM, inference vendor, or Agent framework. It is a Rust Modular Monolith design target; logical components are responsibility boundaries, not mandatory processes, services, or crates.

## 2. Scope

In scope: Canonical Memory Store; identity/versioning; Claim and proposed Fact model; Entity and Relationship management; Lifecycle Manager; historical queries; Scope-bearing resource references; provenance and evidence links; Forget dependency discovery and operation records; stable internal contracts for E/F/G/H/I.

Out of scope: Event ingress and complete compilation pipeline (E); retrieval scheduling, ranking, and Runtime Cache (F); Context planning/editing/delivery and Context state machine (G); Agent Adapter and BMCP wire protocol (H); global principal authentication, policy evaluation, physical erasure execution, backup policy, and security governance (I).

## 3. Responsibilities

- Own canonical identities, immutable canonical revisions, current-version pointers, and historical interpretation.
- Validate domain invariants before commit; preserve evidence, provenance, temporal and epistemic qualifications.
- Provide lifecycle transition decisions and append-only transition history.
- Resolve Entity identity only within explicit, compatible scopes; preserve merge/split history.
- Store typed, temporal, evidence-qualified Relations.
- Expose scope-aware reads and typed references; never infer identity from display strings.
- Maintain a durable Forget Operation model and dependency inventory contract without claiming control over third-party copies.
- Publish canonical change records through a recoverable outbox/change-feed boundary.

## 4. Non-Responsibilities

Brain does not plan, reason, choose actions, invoke tools, execute skills, control an Environment, determine LLM prompts, or grant tool authority. It does not own raw Event ingestion, extraction algorithms, embedding/index implementation, runtime ranking, Context budgets, BMCP serialization, global authorization policy, or physical deletion in external systems.

## 5. Domain Objects

| Object | Meaning and identity |
|---|---|
| Memory | Durable knowledge asset identity; stable across immutable Memory Versions. |
| MemoryVersion | Immutable committed snapshot of a Memory's canonical content and references. |
| Claim | A proposition asserted about an Entity, Event, or state, with epistemic and temporal qualification. |
| FactRecord (CANDIDATE; ADR-blocked) | A separately addressable attestation/qualification that a proposition met a declared verification standard; not an assertion of metaphysical certainty. |
| Evidence | Source material/observation or protected locator supporting, refuting, or qualifying a proposition. |
| ProvenanceRecord | Immutable derivation record linking a target to typed sources and method identity. |
| Entity | Stable identity for a referent; display names and aliases are not identity. |
| EntityVersion | Immutable descriptive/profile revision for an Entity identity. |
| Relation | Typed, directed or explicitly symmetric association with validity, evidence, scope, and revisions. |
| ConflictSet | Explicit group of incompatible Claims and their evidence/resolution history. |
| LifecycleEvent | Append-only authoritative record of a lifecycle transition. |
| ForgetOperation | Durable governed workflow record for access suppression, dependency discovery, derivative handling, and completion exceptions. |
| ScopeRef / ActorRef / TypedObjectRef | Stable typed references used in all cross-object contracts. |

## 6. Data Model

All IDs are opaque and non-semantic. UUIDv7 is only a candidate implementation choice. Timestamps preserve source precision and timezone where relevant; normalized instants use UTC. Valid-time intervals default to half-open [start,end). Unknown is explicit.

Every protected asset carries one ownership ScopeRef and zero or more applicability ScopeRefs. Sharing is represented by a separately governed grant, not by rewriting ownership or unioning scopes. Every asset also carries created/recorded metadata and schema version.

A MemoryVersion snapshot contains content digest, parent version, commit sequence, author ActorRef, reason, immutable Claim references/snapshots, Entity/Relation references, Evidence/Provenance references, temporal metadata, and schema version. It is not a mutable row representing current truth.

## 7. State Machine

Memory lifecycle: Candidate → Consolidated → Active → Superseded or Archived. Active/Superseded may be Archived. Archived → Active requires explicit restore authorization and a new auditable transition/version. Forget is not a Memory lifecycle state or transition. A governed ForgetOperation installs a durable suppression fence; after the applicable I-governed completion criterion is met, the Memory may transition directly from its existing non-Forgotten lifecycle state to terminal Forgotten. The operation's in-progress state is never stored in the Memory lifecycle field. No resurrection after Forget; newly supplied information gets a new identity and provenance.

Claim epistemic status is independent: Observed, Reported, Inferred, Verified, Disputed, Retracted. Entity identity status and Relation lifecycle are separate state machines. FactRecord status, if approved, is separately defined by its ADR. Context and Delivery states belong to G and Sync, not Brain.

## 8. Operations

Core commands: CreateCandidate; CommitMemoryVersion(expected_version); ReadMemory(at_version/as_of); TransitionLifecycle(expected_state/version); ReviseClaim; RetractClaim; Create/UpdateEntityVersion; ResolveEntity; MergeEntities; SplitEntity; Create/Revise/Retract/SupersedeRelation; CreateConflictSet; TraverseProvenance; StartForget; EnumerateForgetDependencies; RecordForgetTargetProgress; CompleteForget.

Every mutation includes authenticated ActorRef, resolved ScopeRefs, operation/resource identity, schema version, idempotency key, correlation/causation IDs, reason, and expected version/state. Authorization is evaluated by I; Brain independently validates semantic scope compatibility and rejects unresolved scope.

## 9. Invariants

- Canonical Memory identity and version history are Brain-owned (I-01).
- Event, Memory, Claim, Fact (until ADR), Entity, Relation, Evidence and Context remain distinct.
- Immutable versions are never overwritten; stale writes never silently win.
- Every derived asset has typed provenance or an explicit unavailable reason.
- Scope is not Permission; no implicit cross-scope merge/read/reference.
- Evidence access is independently authorized from Memory access.
- Memory content is untrusted data and cannot become system/developer instruction or tool authorization.
- Context edits never mutate canonical assets.
- Lifecycle state has one authoritative representation (LifecycleEvent stream plus a deterministically derived current state; see versioning contract).
- Forget is not complete while required targets remain unresolved.

## 10. Interfaces

**E — Compiler to Brain:** candidate envelope, Claim proposals, Entity/Relation proposals, Evidence and Provenance references, ActorRef, ScopeRefs, source epistemic status, TimeValues, idempotency key, schema version. Output: accepted canonical IDs/version IDs and lifecycle result, or deferred/rejected typed error. Compiler proposes; Brain owns canonical acceptance/version. Fact/Claim schema is ADR-blocked (INT-P0-01). Same key/same canonical payload returns same result; same key/different payload is conflict.

**F — Runtime to Brain:** scope-filtered canonical query/read with explicit version or current-as-of semantics, requested fields, evidence/provenance expansion budget. Output: canonical references, version IDs, lifecycle/epistemic/time qualifiers and authorization-safe partial-result markers. Brain owns truth and versions; F owns scheduling/ranking/cache. Filter before candidate materialization and recheck every graph edge/target (INT-P0-02).

**G — Context Manager to Brain:** Memory ID + exact MemoryVersion ID (or explicitly requested current pointer), source refs, change reason and authorization context. Output: immutable canonical references and content handles; G owns ContextVersion/ChangeSet and its state machine (INT-P1-01). A context entry must not silently follow a moving current pointer.

**H — BMCP/Adapter:** typed opaque Memory/Version/Entity/Relation references and protocol-safe summaries; H owns wire encoding, actor authentication envelope and delivery/ack protocol. Brain does not define BMCP wire fields. No display name is an identity.

**I — Governance:** ActorRef, ScopeRef, TypedObjectRef, action, purpose, policy/grant version, Forget request and retention obligations. I owns authorization decisions, audit policy and physical-erasure policy; Brain supplies canonical dependency and state records. Async workers reauthorize before protected/irreversible stages (INT-P0-02/03).

Every interface returns structured errors: code, object type/ID when disclosable, field path, invariant ID, retryability, correlation ID, and safe remediation. Unauthorized errors must not reveal object existence.

## 11. Error Handling

Stable categories: NOT_FOUND_OR_NOT_VISIBLE; SCOPE_UNRESOLVED; SCOPE_MISMATCH; PERMISSION_DENIED; INVALID_TRANSITION; STALE_VERSION; IDEMPOTENCY_CONFLICT; DUPLICATE_ID; INVALID_REFERENCE; EVIDENCE_UNAVAILABLE; PROVENANCE_INCOMPLETE; CONFLICT_REQUIRES_RECONCILIATION; FORGET_IN_PROGRESS; FORGET_PARTIAL; SCHEMA_UNSUPPORTED; INVARIANT_VIOLATION. Error detail is minimized to prevent existence and side-channel leaks.

## 12. Consistency

Canonical commit, immutable version visibility, lifecycle transition record and outbox/change-feed entry must be atomic or recoverably equivalent. Indexes, graph projections, caches and search documents are derived and rebuildable. Current pointers advance with compare-and-swap. Change-feed consumers track a monotonic canonical sequence/watermark and reject stale projections.

## 13. Security / Scope

Resolve identity from authenticated ActorRef and typed ScopeRef, never model output, display name, alias, or Agent-supplied labels alone. Validate owner scope and every applicability scope. Cross-scope references require explicit grants and independent source/evidence checks. Apply scope filtering before reads can influence F ranking, Context assembly, counts, or caches. Cache keys must include principal, scope set, environment, policy/grant revision and canonical version/watermark. Memory and Evidence payloads are untrusted data, with source identity, epistemic status, trust metadata, Evidence refs and Provenance lineage retained (INT-P0-04).

## 14. Performance Considerations

No latency or throughput guarantee is frozen. Bound graph traversal by depth, node count, fan-out and deadline; return explicit truncation/incomplete markers. Batch authorization and typed-reference validation without weakening per-resource semantics. Measure version snapshot size, commit amplification, provenance traversal, temporal queries, conflict detection, merge/split migration and Forget dependency discovery. Indexes remain projections.

## 15. Observability

Carry correlation_id, causation_id, actor_ref, scope_ref IDs, operation_id, idempotency identity, object/version IDs, schema version, canonical sequence, stage, attempt and timestamps. Metrics: commit latency, stale-write rate, outbox lag, projection watermark lag, lifecycle transitions, conflict backlog, provenance incompleteness, scope denials, Forget suppression latency and unresolved targets. Logs must not copy sensitive payloads.

## 16. Failure Scenarios

- Store commit succeeds but publication fails: outbox replay publishes once logically; consumers deduplicate by event ID.
- Concurrent version writers: one CAS wins; others receive STALE_VERSION and reconcile.
- Index stale or unavailable: canonical reads remain authoritative; degraded status is explicit.
- Permission service unavailable: protected operation fails closed.
- Provenance source unavailable: preserve permitted typed reference and unavailable reason; never fabricate source text.
- Merge/split partially projected: canonical migration record remains authoritative; projections rebuild.
- Forget worker crash: resume from durable per-target progress; never mark complete prematurely.
- Third-party model already received data: record boundary/exception; do not claim remote deletion.

## 17. Dependencies

Depends on B Domain Model for canonical semantics; E for source/Event and proposal contracts; F for scope-first query and projection consumption; G for exact version references; H for authenticated actor and wire boundary; I for authorization, retention and physical-erasure policy; storage/recovery architecture for atomic commit/outbox and backups.

## 18. Open Questions

- OPEN: INT-P0-01 ADR approval and resulting Fact/Claim identity/schema.
- OPEN: generic Scope algebra, multiple owners and shared ownership (DM-005).
- OPEN: final Principal/ActorRef authentication semantics with H/I (INT-P1-03).
- OPEN: TimeValue uncertain-time schema and precision rules (DM-006).
- OPEN: whether Consolidated is durable state or evaluation checkpoint.
- OPEN: retention/backup cryptographic-erasure guarantees and external source deletion (INT-P0-03, DM-011).
- TO_VALIDATE: storage layout, snapshot strategy, graph fan-out/depth budgets, and local Rust performance.

## Phase 3 remediation — authority clarifications

### Memory lifecycle versus Forget operation

The only Memory lifecycle states are Candidate, Consolidated, Active, Superseded, Archived and Forgotten. “Forgetting” is not a lifecycle state, status alias or transient lifecycle transition. A ForgetOperation is a separate durable workflow with its own operation state and monotonic fence. Immediate read suppression is an effective availability rule derived from the active fence; it is not a mutation of Memory lifecycle. The canonical transition to Forgotten is a distinct LifecycleEvent after the applicable governance criterion is supplied by I. Forgotten is terminal for that content identity; genuinely new information requires a new identity and provenance.

### Typed ordering

The normative cursor definitions, transaction visibility and replay rules are in [commit-cursor-semantics.md](commit-cursor-semantics.md). Every MemoryVersion carries both its per-Memory AggregateRevision and its CanonicalCommitCursor. LifecycleEventCursor, IndexWatermark and ForgetFenceCursor are separate types. ContextVersion is G-owned; protocol/delivery identifiers are H-owned; authorization epochs and completion policy are I-owned.

### Forget authority boundary

D is authoritative for the durable ForgetOperation identity, target references, suppression fence/generation, canonical dependency inventory, producer registration barrier, target-progress evidence and canonical-domain suppression proof. D does not authorize the operation, decide retention/backup/external-recipient policy, attest remote physical erasure, or declare global system Forget complete. I supplies the governing authorization and completion policy. E/F/G/H own their local execution and acknowledgement mechanics. The detailed contract is [forget-fence-and-completion-contract.md](forget-fence-and-completion-contract.md).

### Fact/Claim

INT-P0-01 remains ADR-BLOCKED: the inspected main branch contains no approved 02-domain-model/adr/ADR-001-fact-claim-canonical-model.md. Claim, ClaimRevision and ConflictSet fields in D documents remain illustrative CANDIDATE descriptions only. No schema, DDL, API or wire shape is frozen by this remediation.
