---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
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
    canonical_scope: "E-domain Memory Compiler record phase-3.6-producer-publication-conformance.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-6-producer-publication-conformance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-producer-publication-conformance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6 — Producer Publication Conformance

- Owner: Session E — Memory Compiler
- Status: **DESIGN CONTRACT COMPLETE / IMPLEMENTATION NOT VERIFIED**
- Scope: E Producer Work, staging, dependency registration, final publish, receipts and F handoff
- Evidence class: static document contract only; no executable tests or fault injection were run.

## 1. Required invariants

1. Every derivative-capable producer class is D-registered and enabled before work admission.
2. Every WorkItemId is durable and stable across retry, DLQ, replay, recompile and worker recovery.
3. D RegistrationReceipt exists before enqueue, lease, protected source dereference or execution.
4. Candidate and Staged Artifact are private and unavailable to F, G, H, other producers and external consumers.
5. Complete dependency registration is durable before final publish.
6. Final publication validates current ForgetFenceGeneration, I PermissionEpoch, active work/attempt/lease, exact source MemoryVersion, ScopeRef, dependency receipts and artifact identity at the visibility commit.
7. Fence installation and final visibility commit serialize in one shared authority or an explicitly approved equivalent recoverable protocol.
8. Unknown outcomes remain private and barrier-open; stable IDs/digests reconcile them.
9. No replay/rebuild/recompile/restore path can resurrect a covered source or descendant.
10. F indexes only records whose committed visibility state and PublicationReceipt are verified.

## 2. Producer / storage conformance matrix

| ID | Scenario | Required result | Evidence to retain | Status |
|---|---|---|---|---|
| E36-01 | ProducerClass absent/disabled/registry incomplete | Admission rejected/quarantined; no queue/lease | D class receipt/error + no work dispatch | NOT RUN |
| E36-02 | RegisterProducerWork races InstallForgetFence | Exactly one serialization order; admitted work is included in captured high-water, or post-fence work is rejected/quarantined | D registration/fence receipts + transaction trace | NOT RUN |
| E36-03 | D registration ACK lost | Resolve same WorkItemId/digest; no enqueue while UNKNOWN | D ResolveProducerWork response | NOT RUN |
| E36-04 | Worker crash after registration | Same WorkItemId recovered; old lease invalidated; new AttemptId | D registration + lease history | NOT RUN |
| E36-05 | Lease expiry while old worker resumes | Old attempt cannot publish or terminalize | Lease epoch and rejected final gate receipt | NOT RUN |
| E36-06 | Retry/DLQ/replay/recompile | Stable WorkItemId; new AttemptId; recompile new DerivationRunId; current fence/permission rechecked | lineage and attempt history | NOT RUN |
| E36-07 | Candidate/staged object enumerated by F/other producer | No result; private ACL/visibility predicate denies access | authoritative reader tests | NOT RUN |
| E36-08 | Dependency edge set partially committed | Artifact remains private; no PublicationReceipt | dependency inventory snapshot | NOT RUN |
| E36-09 | Fence advances after staging, before publish | Final gate rejects/quarantines | fence receipt + final gate result | NOT RUN |
| E36-10 | PermissionEpoch revoked after staging, before publish | Final gate rejects/quarantines | I decision + gate transaction trace | NOT RUN |
| E36-11 | Publish races fence installation | Publish wins and is in durable inventory, or fence wins and publish rejects; no third state | serializable race trace | NOT RUN |
| E36-12 | Publication ACK lost after commit | Resolve same PublicationOperationId; original PublicationReceipt; no duplicate visibility effect | coordinator/DB record + readback | NOT RUN |
| E36-13 | Crash between prepare and final commit | Prepared artifact remains hidden; recovery commits or aborts idempotently | participant/coordinator logs | NOT RUN |
| E36-14 | Crash after visibility commit before E local update | Reconcile committed marker/receipt; no second publish | DB marker + D receipt | NOT RUN |
| E36-15 | Outbox replay duplicates publish request | Same operation ID/digest returns original receipt | outbox and D lookup | NOT RUN |
| E36-16 | Terminal request while DLQ/replay/lease/publication unresolved | D refuses terminal; barrier remains open | D terminal error/reconcile receipt | NOT RUN |
| E36-17 | Restore with old staged/published objects | Quarantine first; current fence/permission applied before serve | restore manifest + reader denial | NOT RUN |
| E36-18 | Mixed canonical + derived commit | One approved serialization decision; no visible derivative if required canonical operation is aborted/fenced | D canonical + Publication receipts and transaction trace | NOT RUN |
| E36-19 | Same idempotency key, changed digest | Conflict; immutable original unchanged | operation result | NOT RUN |
| E36-20 | Late derivative/ancestor discovered after prior barrier checkpoint | D reconciliation reopens; stale completion not reused | new immutable checkpoint | NOT RUN |

## 3. F consumer contract

F may consume only artifacts whose authoritative visibility record is committed and whose D PublicationReceipt resolves to PUBLISHED for the exact artifact/version, lineage digest and WorkItemId. An E CandidateProduced, Staged, DependencyRegistered, CanonicalCommit or CompilerCompletionReceipt is not sufficient.

For rebuild/backfill/replay:

- D producer admission is required before derivative-capable rebuild work; F uses a stable WorkItemId and follows D barrier semantics.
- Revalidate current D ForgetFence coverage and I PermissionEpoch before source dereference, before index segment commit and before disclosure.
- Historical STAGED/PRIVATE/UNKNOWN records are quarantined and never indexed.
- SUPPRESSED/REJECTED_FENCED records are excluded and invalidation is applied to affected index partitions, caches and Working Sets.
- PUBLISHED records are not blindly trusted: re-read current fence/permission and source ancestry; if covered/revoked/unknown, suppress rather than index.
- Only a committed, complete partition batch advances that partition's contiguous IndexWatermark; gaps stop the watermark.
- A rebuild never converts historical existence or an old PublicationReceipt into current permission to expose.

## 4. Joint decision requests

| Owner | Explicit confirmation requested | Current status |
|---|---|---|
| D | Confirm WorkItemId remains the root barrier identity across retry, DLQ replay, recompile and worker recovery; confirm exact gate inputs and fence-winning race behavior | REQUESTED / NO RESPONSE RECORDED |
| Storage/Consistency | Confirm one shared transaction/serialization authority covers D fence/work ledger, complete dependency registration and final visibility marker; or provide approved crash-safe equivalent and recovery protocol | REQUESTED / NO RESPONSE RECORDED |
| I | Confirm current PermissionEpoch decision semantics can be validated at final visibility commit and define revocation freshness binding | OPEN / NOT CONFIRMED |
| F | Confirm rebuild/backfill consumes only committed PUBLISHED records and performs current fence/permission checks at rebuild and index-commit boundaries | REQUESTED / NO RESPONSE RECORDED |

## 5. Exit criteria

- D semantic confirmation recorded.
- Storage transaction owner, serialization domain, linearization point and recovery protocol explicitly confirmed.
- I permission freshness semantics mapped to the final commit.
- F consumer contract acknowledged by F owner.
- Executable implementation and E36-01..20 fault/race suite run with retained traces.
- E-only path scope verified; no D/Storage/F/I/A files changed.

Until all applicable evidence exists, status remains **DESIGN CONTRACT COMPLETE / IMPLEMENTATION NOT VERIFIED**.

 
## Phase 3.6.2 — E owner acceptance of revised JF-10 v2

**Status: E ACCEPTS THE E-OWNED PRODUCER/PUBLISH CONSUMPTION CONTRACT; I ACCEPTANCE AND IMPLEMENTATION REMAIN OPEN.**

E confirms:

1. Accepted Receipt means durable ingress acceptance/idempotency only. It does not mean Canonical Memory commit, derived dependency registration, publication or reader visibility.
2. E obtains D's durable ProducerWork RegistrationReceipt before enqueue, lease, protected source dereference, execution, retry, DLQ replay or recompile. WorkItemId and lineage remain stable across attempts; AttemptId and LeaseEpoch fence stale workers; DerivationRunId identifies a recompile and cannot reset the Forget barrier.
3. E freezes an immutable output manifest and complete direct/transitive lineage. Dependency registration must be complete and durable before publication prepare. Partial/unknown dependency state remains private.
4. E submits the exact immutable PublicationOperationId/RequestDigest and prepared participant binding to the actual final Storage gate. It does not treat CommitAuthorizationReceipt, I COMMIT_WON, queue delivery, outbox event or E-local state as Published.
5. E becomes Published only after authoritative readback of the matching Storage PublicationReceipt and VisibilityPointer outcome. Lost ACK/replay resolves the same operation ID/digest; changed digest is a hard conflict.
6. Fence, inventory-seal, permission, work/attempt/lease, manifest, dependency or participant state that is stale/unknown blocks visibility. No offline ALLOW, stale PermissionEpoch grace, direct object-store exposure or unregistered child work is permitted.
7. After Forget completion, an old task resumed from retry/DLQ/replay/backup must re-resolve the original WorkItemId and source lineage against the current D fence and I authorization/inventory evidence. It cannot create a new WorkItemId to escape the fence.

E accepts the JF-10 v2 proposal's E caller/recovery role and the requirement to remain non-terminal through I/Storage IN_DOUBT. This is a technical owner-side acceptance, not evidence of an executable Compiler, queue, lease service, database participant or passing E36 test.


## 4. Phase 3.6.2 additional producer conformance cases

| ID | Scenario | Required result | Evidence to retain | Status |
|---|---|---|---|---|
| E36-21 | Offline producer/worker rejoins with queued or leased pre-fence task | Resolve original WorkItemId and latest D fence before source dereference; stale attempt cannot execute, stage, publish or terminalize; no new ID is minted | D receipt lookup, current fence, lease epoch, rejected attempt and audit record | NOT RUN |
| E36-22 | I ProducerDomainInventoryEpoch changes while Forget is open | Existing InventorySealReceipt is invalidated when membership/capability/scope/evidence obligations change; E does not treat D high-water as global completeness; publication/completion remains blocked until replacement I seal is verified | old/new epoch, seal digest, invalidation reason and refreshed target manifest | NOT RUN |
| E36-23 | Old Compiler task resumes after D CanonicalSuppressionComplete | Current fence check suppresses before publish; preserve WorkItemId and lineage; late derivative triggers D proof reopen/reconciliation and is never visible | original work receipt, fence generation, task/attempt identity, suppression receipt and reopened proof reference | NOT RUN |

These additions cover three cases not explicit as standalone IDs in E36-01..20. All existing E36 expected outcomes remain unchanged.
