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
    canonical_scope: "E-domain Memory Compiler record phase-3.6-joint-producer-publication-decision.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3.6-joint-producer-publication-decision"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3.6-joint-producer-publication-decision
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# Phase 3.6 — E Joint Architecture Decision: Producer Work and Publication Enforcement

- Decision authority: user-delegated DE-S Joint Architect (ChatGPT acting across D, E and Storage)
- Date: 2026-11-16
- Status: **JOINT ARCHITECTURE DECISION RECORDED / IMPLEMENTATION NOT VERIFIED**
- Branch: `session-e-memory-compiler-2026-11-16`
- Scope: E-owned producer lifecycle, attempts, leases, derivations, dependency registration and publication enforcement.

## 1. Identity model

| Identity | Meaning | Retry / replay / recovery rule |
|---|---|---|
| `WorkItemId` | Stable root producer obligation registered with D | Reused across retry, DLQ replay, redelivery and worker recovery |
| `AttemptId` | One execution attempt | New for each retry/replay execution |
| `LeaseEpoch` | Fencing generation for worker ownership | Advances on reassignment; stale epochs cannot stage, publish or terminalize |
| `DerivationRunId` | One compiler derivation/recompile run | New for every recompile |
| `ArtifactId` | Immutable output identity | New for a materially new output; content digest is immutable |
| `DependencySetDigest` | Complete immutable lineage/dependency set | Changes require a new dependency registration receipt |

Recompile of the same obligation retains the root `WorkItemId` and creates a new `DerivationRunId`. If it is independently scheduled, E must register a child WorkItem with D before enqueue/lease/execute. The child is linked to the root and participates in the same root barrier accounting. E may not create a fresh unlinked root to evade a fence.

## 2. Required lifecycle

`Accepted → Registered → Queued → Leased → Running → StagedPrivate → DependenciesRegistered → PublishGatePending → Published`

Terminal dispositions are separate from queue state. `DLQ`, `LeaseExpired`, `WorkerLost`, `RetryPending` and `StagedPrivate` are non-terminal. A root with multiple outputs/children becomes terminal only after every declared output and descendant has a durable terminal disposition and no attempt can publish.

E MUST obtain D's durable ProducerRegistrationReceipt before queue insertion, leasing, execution, source dereference or staging. A lost response is resolved by retrying the same idempotency key and request digest; it must return the original receipt or a deterministic conflict.

## 3. Dependency and publish protocol

1. Build the complete immutable dependency set, including transitive source lineage and typed scope references.
2. Stage bytes only in a private, non-queryable location.
3. Register the complete dependency set with D/Storage as one durable completeness unit. Partial registration is never publishable.
4. Submit the final gate with root WorkItemId, AttemptId, LeaseEpoch, DerivationRunId, ArtifactId, digest, dependency receipt(s), lineage and scope.
5. The coordinator performs the final fence, authorization, work/lease and dependency checks and commits the authoritative visibility transition plus PublicationReceipt atomically.
6. Only after commit may E acknowledge Published or downstream consumers be notified. Outbox delivery is at-least-once and idempotent; an outbox message alone never establishes visibility.

No E-local cache, earlier gate token, successful staging event or object-store listing can establish publication.

## 4. Retry, replay and recovery

- Retry/replay keeps WorkItemId, creates a new AttemptId and obtains a current LeaseEpoch.
- Recompile keeps the root WorkItemId, creates a new DerivationRunId, and registers any independently scheduled child before execution.
- Duplicate requests with the same idempotency key and digest return the original durable receipt.
- Same key with a different digest is a conflict and fails closed.
- Worker recovery must query durable work/lease state; process memory and queue presence are not authority.
- A stale worker may finish computation but cannot register dependencies, publish or terminalize after its LeaseEpoch is superseded.
- DLQ is an operational routing state, not proof that publication is impossible.

## 5. Terminality

E may request root terminal disposition only after all outputs, retries, replays, child derivations and publication attempts are durably accounted for. D records the barrier-visible terminal receipt. An unresolved or unknown commit result remains pending and is reconciled from durable receipts; it is never optimistically marked terminal.

## 6. Verification boundary

This decision resolves E's architecture mapping under the user's explicit delegation of D/E/Storage responsibilities to one joint architect. It does not claim an executable producer API, atomic dependency store, deployed visibility gate, lease-fencing implementation or passing E36 tests. All runtime/fault tests remain **NOT RUN**.
