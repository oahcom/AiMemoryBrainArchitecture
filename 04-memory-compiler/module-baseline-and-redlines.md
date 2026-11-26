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
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Restored byte-for-byte from Owner source branch; Owner acceptance remains pending."
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
    canonical_scope: "E-domain Memory Compiler record module-baseline-and-redlines.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-module-baseline-and-redlines"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - module-baseline-and-redlines
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# E Module Baseline & Redlines — Memory Compiler

**Proposal ID:** DEF-G0-E-001  
**Owner:** E — Memory Compiler Architect  
**Status:** PROPOSED — Owner Review Required  
**Version:** 0.1.0  
**Branch:** `session-e-memory-compiler-2026-11-16`  
**Authority:** E owns compiler lifecycle and enforcement. D, I and Storage retain their respective authorities.

## 1. Module Mission

E transforms durably accepted source Events and registered source material into traceable candidate Memory/Claim/Entity/Relation assets and coordinates their controlled handoff to canonical authority and downstream projection publication. E is a recoverable semantic transformation pipeline, not a canonical database writer, permission authority or index/runtime owner. Accepted input remains durable independently of model availability; compilation may yield no candidate, review, defer, reject or dead-letter outcomes.

## 2. Ownership Baseline

E owns:
- CompilerWorkItem, CompileIntent, DerivationRun, Attempt, Lease and stage lifecycle.
- Durable stage receipts, deterministic normalization and model-assisted extraction orchestration.
- CandidateEnvelope / pre-canonical intermediate representation, Evidence/Provenance drafts and conflict/revision proposals.
- Retry scheduler, DLQ, replay/recompile policy and compiler-local recovery.
- Private staging of immutable derived artifacts and frozen output manifests.
- Enforcement that D registration, dependency registration, current I authorization/PermissionEpoch, current D ForgetFence and Storage final visibility gate are prerequisites to publication.
- Compiler-side reconciliation of durable receipts and terminal outcomes.

E does not own Canonical Memory schemas/revisions/commit, D ProducerRegistration ledger/barrier, D ForgetOperation/Fence, I PermissionEpoch/authorization, Storage physical atomic visibility, F indexes/IndexWatermark/cache/retrieval, G ContextVersion, or H wire schemas.

## 3. Capability Baseline

1. Durable accepted ingress receipt and stable CompileIntent independent of compiler/model availability.
2. Idempotent, versioned deterministic normalization and optional bounded model-assisted extraction.
3. Candidate and evidence/provenance lineage traceable to immutable source identities.
4. Durable stage-result/next-stage scheduling through transactional outbox or equivalent recoverable journal.
5. Stable logical work identity across retries; new AttemptId/LeaseId for each attempt/lease; new DerivationRunId for recompile.
6. D ProducerWorkItem registration before enqueue, lease, protected source dereference or execution.
7. Immutable private staging; no query, listing-based exposure or consumer access before final gate.
8. Complete direct/transitive dependency registration before publication.
9. Revalidation of I PermissionEpoch/authorization and D ForgetFence at each protected read and final gate.
10. Storage PublicationReceipt readback before E records Published/terminal success.
11. Replay, DLQ and restore preserve original lineage and cannot bypass D's barrier or current fence.

Pipeline topology, model routing, queue budgets and callable transport bindings remain candidate/TO_VALIDATE where not yet pinned by owner decisions.

## 4. Domain Ownership

| Entity | Owner | E rule |
|---|---|---|
| CompilerWorkItem / CompileIntent | E | Stable logical work identity |
| DerivationRunId | E | New for recompile; links prior run and original source |
| AttemptId / LeaseId | E | New per attempt/lease; no authority beyond execution fencing |
| StageReceipt | E | Immutable input/output digest, stage/version and result |
| CandidateEnvelope | E | Pre-canonical IR; not a D schema or canonical object |
| Evidence/Provenance draft | E produces; canonical acceptance per D/B contracts | Never invent lineage or evidence |
| ProducerClass registration / ProducerWork registration | D authority; E requests/consumes | No execution until D receipt |
| Dependency registration | D authority; E requests/consumes | All required edges durable before gate |
| ForgetFenceCursor | D | E stores/consumes opaque current token |
| PermissionEpoch / authorization | I | E revalidates; never mints or compares epochs |
| PublicationOperationId / PublicationReceipt | Storage-owned operation/receipt under cross-owner protocol; E maintains request/reconciliation state | Published only after matching durable Storage receipt |
| CanonicalCommitCursor / AggregateRevision | D | E consumes exact D result |
| IndexWatermark | F | E emits publication request/event only |
| ContextVersion | G | E cannot mutate |

## 5. Interface Baseline

### 5.1 Ingress and identity

Accepted means durable custody/ingress only. It is not Processed, Compiled, CanonicalCommitted, Published or Indexed. EventRef is immutable. AcceptedReceiptId and CompileIntentId are stable. ProducerWorkItemId is stable across retries of one logical work item; AttemptId/LeaseId change per execution. Recompile creates a new DerivationRunId and fresh authorization/fence checks. The exact D policy for a new ProducerWorkItemId versus child registration on recompile remains OPEN and E must not invent it.

### 5.2 Producer admission and barrier

E must obtain a durable D Producer Registration Receipt before queue insertion, lease acquisition, source dereference or execution. If the request ACK is lost, E resolves the same ProducerWorkItemId + digest; UNKNOWN blocks execution. Queue state, lease, retry count, DLQ, worker replacement or operator replay never removes the D registration. Lease expiry invalidates the lease only; it does not terminate work or release the barrier. D remains authority for class/work ledger, registration high-water, fence cutoff and barrier closure.

Producer-class declaration and per-work admission are separate. D's exact class-registration operation/version semantics remain OPEN (OPEN-D-CLASS-01). E cannot invent a D API or run an unregistered producer path.

### 5.3 Stages, extraction and provenance

Deterministic validation, decoding, structural normalization, timestamp preservation, scope checks, evidence locator validation and provenance construction must not depend on an LLM. Model-assisted classification/extraction is optional, bounded, versioned and treated as untrusted proposal output. Model output cannot grant permission, change Scope, invent lineage, decide canonical identity or adjudicate conflicts. CandidateProposition remains pre-canonical until B/D decisions settle Fact/Claim mapping and canonical schemas.

Every stage receipt binds input/output digests, stage and pipeline versions, deterministic/model-assisted mode, method/model profile where applicable, attempt, permission/fence observations and result. Raw protected payload is excluded from ordinary logs.

### 5.4 Private staging and dependency registration

StagedPrivate is immutable and non-queryable. Object-store path, listing, signed staging URL, queue membership, outbox event, local compiler status or possession of an artifact reference cannot expose bytes. E freezes a complete output manifest and lineage, requests D dependency registration for all direct/transitive sources and artifacts, and waits for durable receipts. Partial or unknown dependency registration leaves all affected artifacts private.

### 5.5 Final publication gate

Before final gate, E revalidates current I authorization/PermissionEpoch, current D ForgetFence for every source ancestor and target, current work/attempt/lease fencing, complete dependency set and frozen manifest, scope and any I-required inventory seal. The actual visibility transition must be serialized with D fence/producer/dependency operations and the I owner-final-gate ordering protocol. A local check followed by an independent write is forbidden.

The JF-10 v2 owner-side design specifies a prepared Storage participant/XID, D/Storage shared per-authority serialization, I sequencer decision, and Storage same-XID commit/rollback. I COMMIT is not publication. Only the atomic Storage VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox commit, followed by authoritative receipt readback, permits E to record Published. Storage must prove real database support before this is treated as implementable.

### 5.6 Cursor semantics

E consumes D CanonicalCommitCursor and LifecycleEventCursor as separate typed values, preserves exact refs and never mints them. F owns IndexWatermark and advances only after contiguous canonical prefix accounting. ForgetFenceCursor is D-owned and independent of CanonicalCommitCursor, LifecycleEventCursor, IndexWatermark and I PermissionEpoch. E must not compare opaque cursor values or use one as another.

## 6. Security Baseline

- Resolve scope and permission before protected source dereference, extraction, entity search, consolidation, replay, canonical write request and publication.
- Revalidate current authorization and PermissionEpoch at worker admission, lease, protected reads, retry/replay and final gate.
- Revalidate D ForgetFence and complete source/ancestor lineage at admission, after expensive work and immediately before visibility.
- Treat source payload and model output as untrusted data; they cannot modify policy, tools, Scope or compiler configuration.
- Cache/stage keys bind scope, environment, actor class, policy/revocation epoch and source version; private staging is not a read surface.
- Fail closed on missing, stale, ambiguous or unavailable I/D/Storage evidence.
- Do not log forgotten plaintext, raw sensitive excerpts, prompts or credentials in ordinary telemetry.

## 7. Module Redlines

1. StagedPrivate is never queryable or consumer-visible.
2. Accepted, Registered, Queued, Leased, Running, Staged, DependencyRegistered, I COMMIT_WON and local E Published-intent are not interchangeable.
3. Retry, lease expiry, DLQ, replay, recompile or worker replacement cannot bypass the original D producer barrier or create an unregistered side channel.
4. Every retry/replay/recompile rechecks current I PermissionEpoch and D ForgetFence; stale attempts cannot be legitimized by copying a newer token onto stale output.
5. Dependency registration must complete before visibility; partial registration is non-publishable.
6. Final gate rechecks exact lineage and latest fence in a serialization protocol, not a check-then-write sequence.
7. E cannot mint CanonicalCommitCursor, canonical revisions, ForgetFenceCursor, ProducerRegistrationReceipt or IndexWatermark.
8. E cannot decide canonical commit, permission, global Forget completion, index freshness or Context mutation.
9. I COMMIT_WON alone never means Published; Storage participant commit and receipt readback are mandatory.
10. Unknown/in-doubt participant, missing receipt, stale replica, timeout or lost ACK is not success or safe abort.
11. No concrete DB/XA/prepared-XID capability may be claimed until Storage identifies and verifies the actual engine/configuration and crash/recovery behavior.

## 8. Forbidden Cross-module Actions

- D: E may submit candidates and canonical write requests, but cannot choose D canonical schema, revision, commit cursor, lifecycle or Forget state.
- F: E may emit canonical-commit/projection notifications, but cannot write index projections, rank retrieval, mutate cache/Working Set or advance IndexWatermark.
- G: E may emit lifecycle/change notifications, but cannot mutate Context or ContextVersion.
- I: E consumes authorization/PermissionEpoch and policy decisions; cannot mint, reinterpret or override them.
- Storage: E stages and requests publication; cannot declare physical visibility atomic or recover prepared XID on Storage's behalf.
- H: E consumes authenticated ingress identity/envelope; cannot redefine BMCP wire or Adapter behavior.

## 9. Dependency Contracts

| Dependency | Provider | Required contract | Current status |
|---|---|---|---|
| Canonical schema/commit/cursor/fence/producer ledger | D | Typed canonical write, durable producer/dependency receipts, final fence gate | D semantics DECIDED; callable API/atomic realization OPEN |
| Permission/PermissionEpoch/revocation | I | Current decision and exact protected-operation binding | I policy owns; implementation NOT VERIFIED |
| Durable visibility / prepared participant | Storage | Same-XID prepare/recovery, atomic pointer+receipt+outbox, restore proof | DB engine NOT SELECTED / NOT VERIFIED |
| Ingress identity/wire | H | Authenticated ProducerIdentity, stable idempotency and scope binding | H-owned; exact schema acceptance separate |
| Typed domain refs / Fact-Claim mapping | B | Candidate-to-canonical mapping and reference types | Fact/Claim ADR OPEN |
| Runtime/index consumption | F | Canonical events and fence-aware publication, separate IndexWatermark | Consumer contract required |
| Context invalidation | G | Typed lifecycle/forget events; G owns Context | Consumer contract required |
| I inventory seal | I | Current epoch/seal where policy requires it | Governance/implementation OPEN |

## 10. Conformance Requirements

All cases below are SPECIFIED / NOT RUN unless separate executable evidence is linked:
- Accepted receipt survives compiler/model outage and restart.
- Duplicate ingress/stage dispatch is idempotent; same key/different digest conflicts.
- Scope/permission denied before source dereference and candidate generation.
- D producer registration occurs before queue/lease/run; unknown registration blocks execution.
- Fence-versus-registration race has exactly one serialized outcome.
- Queue pending, leased, expired, retry, DLQ and replay remain in D barrier.
- Retry/replay after PermissionEpoch or ForgetFence change is denied/restarted from safe point.
- StagedPrivate cannot be read/listed/query-indexed by any consumer.
- Dependency registration ACK loss resolves by stable key; partial registration remains private.
- Fence or permission advances between staging and final gate; publication is rejected.
- Storage prepare/fence race has exactly two valid orders; unknown remains private/in-doubt.
- Same-XID commit/rollback survives process restart/failover and lost ACK.
- I COMMIT_WON without Storage participant commit does not expose bytes.
- Atomic VisibilityPointer/PublicationReceipt/outcome/receipt-consumption/outbox transaction is all-or-none.
- Restore/rebuild/replay cannot resurrect fenced source derivatives.
- Candidate-to-canonical mapping respects B/D approved schemas and does not assume Fact/Claim decision.

## 11. Acceptance Criteria

E G0 proposal is acceptable only when:
1. All 14 required sections are present and owner boundaries are explicit.
2. Work/attempt/run/lease identity and D admission semantics are consistent with D's current branch contracts.
3. Private staging, dependency registration and final gate prevent pre-publication visibility.
4. Retry/replay cannot bypass D Producer Barrier or current I/D checks.
5. JF-10 v2 is described as architecture protocol only, with exact exceptions and NOT VERIFIED/NOT RUN statuses preserved.
6. Cursor domains remain distinct.
7. E Owner reviews and explicitly accepts an exact version; this proposal itself remains PROPOSED.

## 12. Change Authority

E alone changes compiler-internal work lifecycle, extraction, normalization, stage journal, attempt/lease/retry/DLQ/replay and candidate IR. D alone changes canonical domain, Producer Registration ledger/barrier, ForgetFence and canonical publication authority. I alone changes permission/revocation/global Forget policy. Storage alone certifies database/prepared-XID/visibility implementation. B owns domain typing and Fact/Claim decisions; F/G/H own their consumer/runtime/wire domains. Cross-owner changes require exact-version decisions by affected Owners.

## 13. Open Decisions

- OPEN-D-CLASS-01: D ProducerClass registration operation and version-transition semantics.
- OPEN-D-WORK-02: EventRef-only ingress admission before canonical MemoryRef exists.
- OPEN-D-RECOMPILE-03: same ProducerWorkItemId versus child registration for recompile; original lineage/barrier always retained.
- OPEN-D-GATE-04: exact D API/linearization binding for final publication gate and Storage visibility transition.
- Storage concrete DB engine/version, isolation, prepared-XID/lock retention, same-XID recovery, failover and backup/restore.
- I InventorySeal authority/signer/verifier/epoch lifecycle and governance.
- B Fact/Claim ADR, Claim identity/revision, Provenance cycle policy.
- F/G consumer contracts and event replay/retention semantics.
- Model routing, throughput, VRAM/resource budgets and queue quotas remain TO_VALIDATE.

## 14. Explicit Non-Claims

This proposal does not claim compiler production implementation, D API availability, D/E/Storage atomic registration, private staging isolation certification, final publication gate implementation, selected database, prepared-XID durability, same-XID crash recovery, I sequencer implementation, InventorySeal governance, passing tests, Global Forget completion or production activation. JF-10 P0 remains OPEN; multi-policy-domain atomicity remains BLOCKED / NOT ACCEPTED. The JF-10 v2 document is an architecture protocol with enumerated owner dependencies, not implementation evidence.

## Evidence

- E branch starting HEAD: `530645a08b55716257cf4cde20b0900b628abb52`
- `04-memory-compiler/compiler-overview.md` Blob: `35a766fae29c0b8ddf692a6ec062762f0fca29d2`
- `04-memory-compiler/compiler-state-and-producer-admission.md` Blob: `e59f517fff161ab882aa0ddc4a5bda513964ae1a`
- `04-memory-compiler/forget-fence-and-derived-registration.md` Blob: `00e37ba56596e710513c8d0568acd79141d9101b`
- `04-memory-compiler/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` Blob: `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- D's exact JF-10 v2 decision: D branch HEAD `1460fbd17ee38ea4044dc6c75cfe49039c7fc585`; D accepted single-I-PolicyDomain D-owned semantics with enumerated exceptions only.
