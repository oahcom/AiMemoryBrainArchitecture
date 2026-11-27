---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Delegated direction decision, 2026-11-26"
        - "Work Item AID-2026-089"
        - "Issues #1125 and #1211"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Candidate source restored in Draft PR; exact-version D/Storage/A acceptance and normative approval pending."
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
    canonical_status: Canonical
    canonical_scope: "D canonical ForgetFence authority and Storage projection boundary"
    canonical_scope_id: "memory-brain/forget-fence-authority"
    canonical_scope_keywords:
      - forget-fence
      - canonical-suppression
      - storage-projection
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/01-system-architecture/forget-fence-and-completion-contract.md"
    zh-CN: "docs/zh-CN/01-system-architecture/forget-fence-and-completion-contract.md"
---
# Canonical Forget Fence and Completion Contract

- Document ID: D-FORGET-CONTRACT-001
- Version: 1.0
- Source branch: main
- Source revision: canonical root restored by AID-2026-089; exact Blob is recorded on the Draft PR Head.
- Historical source branch head: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3 (provenance only)
- Canonical source: this file (`01-system-architecture/forget-fence-and-completion-contract.md`); EN/ZH-CN counterparts are mirrors under `docs/`.
- Chinese counterpart: [Canonical Forget Fence 与完成契约](../docs/zh-CN/01-system-architecture/forget-fence-and-completion-contract.md)
- Owner: Session D — Memory Brain Principal Architect
- Status: D canonical-domain semantics DECIDED; cross-module execution and global completion policy OPEN / I-owned
- Related: D-REV-P1-001, D-REV-P1-003, INT-P0-02, INT-P0-03, INT-P1-03, INT-P1-06

## 1. Purpose and authority

This contract defines the canonical authority boundary for Forget: durable operation identity, monotonic suppression fence, dependency inventory, producer admission/registration, barrier semantics, target acknowledgements and canonical-domain proof. It is a domain contract, not a wire/API schema.

- **D owns:** canonical ForgetOperation ID/state; affected canonical target refs; durable ForgetFenceCursor/generation; dependency inventory authority; producer registration/barrier ledger; canonical target progress; canonical-domain suppression proof; lifecycle transition to Forgotten once I supplies the governing criterion.
- **I owns:** principal/authorization and revocation policy, permission epochs, retention, backup/external-copy rules, residual-exception approval, global completion policy and physical-erasure requirements. D cannot authorize itself or declare global/physical completion.
- **E owns:** compiler work queues/leases/retries/DLQ/replay and derivative publication enforcement.
- **F owns:** retrieval in-flight cancellation/finalization, candidate suppression, caches/Working Sets, index rebuild and per-index watermarks.
- **G owns:** Context snapshots/deltas/ChangeSets/delivery intents and Context reconciliation.
- **H owns:** BMCP wire, Adapter local state, offline reconnect and trustworthy application/clear acknowledgement.

D's references to module actions are mandatory boundary requirements, not an attempt to define their internal state machines, wire fields or implementation.

## 2. Vocabulary: three different outcomes

1. **Logical suppression:** covered canonical targets become unavailable to ordinary reads, candidate generation, reference resolution and new publication. It is enforced by the durable fence and is immediate at the canonical authority boundary. Suppression is not deletion.
2. **Asynchronous cleanup:** each derivative owner invalidates/removes/rebuilds/quarantines its own materializations and records a target-specific acknowledgement. Cleanup may be retried and may remain partial.
3. **Physical erasure:** irreversible removal from storage, backups, external recipients or provider-controlled systems under I's policy and evidence rules. D does not perform or prove it.

D's CanonicalSuppressionComplete means only that the D-defined closed-world producer barrier has drained and all required canonical-domain targets are suppressed or carry an explicit I-approved residual exception. It does not mean every module has physically deleted bytes, and it is not global Forget completion.

## 3. Durable identity and fence

Every accepted Forget request receives one opaque, durable ForgetOperationId. Client retries use a scoped idempotency key plus normalized request digest: same key/same digest returns the same operation; same key/different digest is an idempotency conflict. The operation records exact target TypedObjectRefs, target-set digest, ScopeRefs, requester ActorRef, I authorization-decision reference/policy version, reason, timestamps, dependency inventory ID, producer barrier metadata, per-target status and proof references. It stores no forgotten plaintext.

Fence installation is a canonical transaction. D allocates a strictly increasing fence_generation from the canonical Forget authority and persists:
- ForgetFenceCursor = (forget_operation_id, fence_generation, target_set_digest);
- exact covered target identities and version families, including canonical descendants discovered later;
- effective suppression timestamp and canonical commit cursor of fence installation;
- idempotency receipt and recoverable outbox intent.

Generation never decreases or reuses and survives restart/restore. Overlapping Forget operations create later generations; the effective fence for a target is the greatest applicable generation. A fence applies to target identity/version family and registered descendants, not merely the exact payload revision observed at request time. A new Memory ID is not a way to re-import the same forgotten source or derivative lineage.

Every read/write/publication boundary evaluates the latest applicable fence against target and source lineage. A stale cached fence is insufficient: if the latest fence cannot be established, fail closed for affected targets. A worker's admission generation is evidence of what it observed, not permanent authorization to publish.

## 4. Dependency inventory and producer registration

### 4.1 Closed-world producer registry

D maintains the canonical producer-class/registration ledger for all components permitted to create, transform, replay or publish derivatives of canonical targets. Each module owner registers producer classes and work-admission boundary before that class can process data. Each individual work item registers durably before execution with:
- stable producer/work ID and producer class;
- source canonical refs and exact revisions/lineage;
- target ScopeRefs and operation/correlation IDs;
- admission CanonicalCommitCursor and observed ForgetFenceCursor/generation;
- lease/attempt identity and registration status.

Producer classes required by current architecture include E compilation/replay, F retrieval/materialization/index rebuild, G Context reconciliation/snapshot/delta/delivery, and H Adapter delivery/reconnect. This inventories producer boundaries; it does not claim D implements their workers.

No producer may start work, acquire a lease, enqueue retry/DLQ replay or publish a derivative before registration is durable. Queue insertion alone is not sufficient. Registration is idempotent. A ledger gap or unknown producer class prevents barrier closure.

### 4.2 Fence snapshot and barrier

Fence installation atomically captures current producer-registration high-water mark, producer_registration_barrier, together with target inventory snapshot/watermark. It includes every work item durably admitted before the fence transaction. Every such item must reach durable terminal disposition before canonical suppression proof:
- committed/published before fence, with all resulting derivatives already registered and included in dependency inventory;
- cancelled/expired without publication;
- suppressed/quarantined by the fence;
- failed and durably parked with publication disabled pending explicit recovery.

Lease timeout is not acknowledgement. Expired leases require owner recovery/reconciliation; work remains unresolved until terminal evidence is recorded. A producer cannot remove itself from the barrier by deleting a queue message or dropping a lease.

After fence installation, new work registration referencing a fenced target or lineage is rejected, quarantined, or admitted only as suppression/cleanup work. A new task cannot publish a derivative of forgotten source merely because it carries the current generation. Its lineage is re-evaluated against active and terminal fences. Producer classes must not have an unregistered side channel; if registry completeness cannot be established, the barrier remains open.

### 4.3 Register-before-visible rule

Every derivative must be registered with D's dependency inventory before becoming visible to any consumer. Derivative record and dependency edge commit atomically, or an equivalent durable prepare/commit protocol ensures failure leaves derivative invisible. The final publish/commit gate rechecks latest applicable fence after expensive processing and immediately before visibility. If a fence advanced or covers any ancestor, output is suppressed/quarantined and cannot enter canonical reads, indexes, caches, Context, delivery or inference input.

This closes the “scan completed, late output appears” race: pre-fence producer work is represented in the barrier; output cannot become visible without final fence check and prior dependency registration. Post-fence work cannot bypass active fence. A post-fence discovery of an unregistered derivative is a barrier-integrity violation: immediately suppress it, reopen/invalidate prior proof, record producer-class defect and notify I/A; never silently count it as covered.

## 5. Target acknowledgement and completion proof

Each target acknowledgement is keyed by (forget_operation_id, target_ref, target_owner, target_attempt) and records:
- state: discovered | suppression_requested | suppression_confirmed | cleanup_confirmed | failed | unknown | excepted;
- target owner's stable acknowledgement ID and contract/capability version;
- observed ForgetFenceCursor/generation and exact target/ref digest;
- timestamp, retry/attempt, correlation/causation IDs and structured error;
- whether it covers active reads, queued work, in-flight work, caches, indexes, snapshots/deltas, delivery or local Adapter managed region.

Acknowledgement semantics are not interchangeable. suppression_confirmed proves the owner will not expose or newly publish the target under its stated boundary. cleanup_confirmed proves that owner's declared cleanup action completed. Neither proves physical erasure outside that owner's controlled domain. Unknown and timeout are not success. Acknowledgements are monotonic for a given attempt; retries cannot downgrade confirmed suppression, but a later-discovered derivative creates a new target entry and invalidates prior closed-world proof until reconciled.

D's canonical-domain proof MUST bind:
1. ForgetOperationId, normalized request digest, target-set digest and final fence generation;
2. fence installation CanonicalCommitCursor and exact affected canonical refs;
3. producer registry version and producer-registration barrier high-water mark;
4. evidence every registered pre-fence work item is terminal and every derivative was registered before visibility;
5. dependency inventory snapshot and final reconciliation watermark/cursor;
6. per-target suppression acknowledgements or exact I-approved residual-exception references;
7. no unresolved producer registry gap, lease, retry, DLQ/replay item, publication gap or unknown required target;
8. canonical lifecycle event/ref if and when Memory transitions to Forgotten;
9. proof schema version, creation time and audit correlation.

Proof is immutable and non-reconstructive: identifiers, digests, statuses and references, not forgotten content. It proves only D's canonical-domain suppression boundary and enumerated registered target acknowledgements.

I's policy decides whether cleanup acknowledgements, offline Adapter acknowledgement, backups, external recipients or physical erasure are required for global completion. An exception is valid only with a durable I-approved reference containing target, scope, rationale, expiry/review condition and residual risk. D never invents or approves an exception.

## 6. Required race matrix and boundary requirements

| Race / subsystem | D canonical requirement | Owning module execution obligation | Failure outcome |
|---|---|---|---|
| E queued compiler work | Queue admission/work registration precede execution; fence inventory includes queued work | E checks fence before dequeue/lease and before canonical proposal/commit | Cancel/quarantine; barrier remains open until terminal |
| E leased/in-flight work | Lease/work ID is in pre-fence barrier; final publish gate rechecks fence | E checks after extraction/consolidation and immediately before derived registration/commit | Suppress output; register discovered target as blocked; no canonical visibility |
| E retry, scheduler, DLQ and replay | Every retry/replay is a registered work item linked to original source lineage | E carries original source refs/fence context; reauthorizes and checks fence on every retry/replay | Reject/quarantine stale replay; retry cannot renew publication rights |
| F in-flight retrieval | Request/source refs and active execution are covered by producer registration | F rechecks fence before final candidate/result emission, not only at query start | Drop affected candidates; response marked incomplete/blocked |
| F cache / Working Set | Cache/materialization target is in dependency inventory | F checks fence on cache read/write; key/invalidation includes fence generation and scope/policy context | Cache miss/deny; stale entries cannot be returned |
| F index rebuild | Rebuild job/output generation registered; IndexWatermark is not Forget proof | F checks fence before segment publish/swap and candidate generation; rebuilds from canonical snapshot plus replay | Do not publish stale segment; quarantine/rebuild; watermark cannot cross unresolved commit gap |
| G Context snapshot/delta/ChangeSet | Context refs and pending changes are discoverable targets | G tombstones affected refs, invalidates snapshots/deltas and commits a new safe ContextVersion | Old immutable snapshot is audit-only; never served as current |
| G Prepared/Delivered work | Pending deliveries registered and bound to exact ContextVersion | G cancels/supersedes when possible and checks tombstone/fence immediately before delivery | Delivery remains pending/unknown/superseded; no late Applied promotion |
| H Adapter online delivery | Adapter/session is registered derivative target; D does not define wire fields | H consumes fence/revocation and returns its owned acknowledgement | Suppress managed region; missing ACK remains unknown |
| H Adapter offline reconnect | Offline Adapter remains outstanding target; offline is not implicit success | H authenticates/reconciles latest fence, discards stale snapshots/deltas, applies safe state and attests before reuse | No cached Context reuse; unknown/blocked until H criterion met |
| Late Applied acknowledgement | Late ACK cannot override newer fence or restore stale target | G/H reject stale target-version application for current state; preserve as historical evidence only | Record late evidence; no resurrection/head rollback |
| Backup / external copy | Inventory/ack requirement is I-defined; D records discovered targets/references | I/designated owners enforce retention, backup and external-recipient policy | D cannot claim physical deletion; global completion remains I-owned |
| Concurrent canonical write | Fence and write gate serialize against same target lineage | D checks latest fence in canonical transaction at commit | Reject/quarantine write; no post-fence visible derivative |

## 7. Operation state and lifecycle separation

ForgetOperation state is not Memory lifecycle. D operation phases are Requested, FenceEstablished, InventoryOpen, BarrierDraining, TargetReconciliation, CanonicalSuppressionComplete, Blocked and Failed. Memory lifecycle remains Candidate, Consolidated, Active, Superseded, Archived or Forgotten. “Forgetting” is not a Memory state. Transition to Forgotten is appended only as a separate canonical lifecycle event when I's applicable policy criterion is met; the event itself is not physical-erasure evidence.

## 8. Interfaces, failure, idempotency and observability

- **Producer registration contract:** D owns domain contract; producers E/F/G/H; D dependency/barrier ledger and I completion evaluator consume it. Stable work ID, source refs/revisions, ScopeRefs and observed fence are required. Retry preserves work identity/lineage or creates a linked attempt; no untracked replay.
- **Target acknowledgement contract:** D defines domain meaning; E/F/G/H produce owner-specific evidence; I determines required target classes and exception policy. Same acknowledgement ID/digest is idempotent; conflicting evidence is rejected and audited.
- **Failure behavior:** fail closed for affected target if latest fence unavailable; unknown target/producer/lease/gap blocks barrier closure. Partial work is resumable. Timeout never becomes success.
- **Observability:** operation ID, fence generation, target-set digest, producer registration high-water, open work count, dependency inventory cursor, target state counts, late derivative count, barrier age, blocked reason and correlation/causation. Do not log forgotten payloads.

## 9. Conformance tests (design acceptance; not yet executed)

1. Forget races with canonical write: one serialization order wins; if fence wins, write is rejected; if write wins, derivative is registered and included in barrier.
2. Queued, leased, retry, DLQ and replayed compiler work cannot publish after fence; all appear in registration ledger.
3. Delayed compiler output completing extraction after fence is quarantined before registration/visibility and cannot create readable canonical asset.
4. Runtime in-flight result/cache hit is suppressed by a fence installed after query start but before response finalization.
5. Index rebuild cannot swap stale segment after fence; watermark does not imply suppression or cleanup.
6. G snapshot/delta and Prepared/Delivered Context cannot be re-applied after fence; late Applied evidence cannot reactivate it.
7. Offline Adapter reconnect reconciles latest fence before cached Context use; no acknowledgement means unknown.
8. Producer registration gap, expired unrecovered lease, unknown target or missing acknowledgement prevents barrier closure.
9. Post-fence derivative registration from forgotten ancestor is rejected/quarantined even if latest generation is presented.
10. Duplicate Forget request returns same operation; same idempotency key with different target digest conflicts.
11. Late unregistered derivative invalidates prior proof and reopens reconciliation; no silent success.
12. Proof contains no forgotten plaintext and does not claim backup/provider physical erasure.

**Acceptance status:** semantics specified; implementation conformance, I policy approval and E/F/G/H enforcement evidence remain OPEN. This document does not close INT-P0-03 globally.

## 10. Phase 3.5 operation-level atomicity contract

[forget-fence-operation-and-publication-gate.md](forget-fence-operation-and-publication-gate.md) is normative for D semantics of CR-P1-01 / D-REV-P1-003. It refines, and does not weaken, §§3–9 above.

Normative operations: RegisterProducerClass, RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. Inputs, outputs, idempotency keys, errors and linearization points are in the operation contract.

### 10.1 Mandatory serialization rule

RegisterProducerWork and InstallForgetFence share one linearizable ordering domain. If registration commits first, its ProducerRegistrationSequence is at or below the immutable high-water captured by the fence and is included in the barrier. If fence installation commits first, ordinary derivative admission for covered source is rejected/quarantined or cleanup-only. Accepted-but-uncaptured work that can publish is forbidden.

### 10.2 Mandatory visibility rule

Dependency registration is durable before visibility. PublishDerivedIfFenceCurrent validates the complete dependency set, work/attempt identity, latest applicable ForgetFence, and I's current PermissionEpoch at the same externally observable atomic/linearizable boundary that changes artifact from private to visible. Independent check-then-write or uncoordinated gate token is insufficient. Ambiguous outcomes remain private until ResolveProducerWork establishes committed result.

### 10.3 Evidence and type separation

Publication evidence binds WorkItemId/AttemptId, ProducerClass, source MemoryVersion/Revision, ScopeRefs, RegistrationReceipt, observed and authoritative ForgetFenceCursor, PermissionEpoch and I decision reference, DerivedArtifact identity, and every DependencyRegistrationReceipt. ForgetFenceGeneration and PermissionEpoch are distinct typed namespaces and must never be numerically compared or mixed.

### 10.4 Status

D operation semantics and required race outcomes are DECIDED as a domain contract. E mapping, I authorization decision semantics, global producer inventory completeness and Storage/Consistency realization remain OPEN. No Storage/Consistency Owner was established in the reviewed package; this is an explicit OPEN ownership gap. Design conformance cases are specified but NOT RUN. This section does not close INT-P0-03 or assert end-to-end Forget completion.

## Phase 3.6 normative addendum — atomicity boundary

D-owned operation-level Phase 3.6 linearization, Producer Work state machine, Fence/Permission dual-validation rules, implementation-neutral Storage semantic requirements, 12-case Fault/Race Proof Matrix and D/E/Storage OPEN Decision Register are specified in [forget-fence-operation-and-publication-gate.md](forget-fence-operation-and-publication-gate.md), Phase 3.6 — Forget Fence Linearization & Atomicity Semantics.

The unique safety invariant is: no derivative may become retrievable, deliverable, indexable, inferable or otherwise visible unless its logical Producer Work is durably registered and accounted for by every applicable Forget barrier, its complete dependency lineage is durable, and the final visibility commit validates the latest applicable D ForgetFence and current I authorization/PermissionEpoch for the authenticated Principal and exact Scope. Unknown or stale evidence is non-visible.

Work Registration, Barrier Capture, Dependency Registration, Staging, Publish Authorization, Durable Commit, Artifact Visibility and Terminal Disposition are separate evidence-bearing stages. Barrier capture accounts for pre-fence work; it is not publication permission. Lease expiry, queue deletion, retry delay and DLQ parking do not terminalize work.

D defines domain semantics and observable ordering only. Storage may choose any realization that proves the same linearization and crash-recovery behavior; this addendum does not approve a database or claim implementation. **CR-P1-01 remains OPEN pending E + Storage joint confirmation and executable evidence.**

## 10. Single-authority resolution — delegated direction, 2026-11-26

Authority: user-authorized operator (delegated by account owner)  
Decision date: 2026-11-26  
Status: direction recorded; D, Storage/Consistency and A exact-version acceptance pending. No implementation authorization.

D — Memory Brain — is the sole logical authority for ForgetOperation identity/state, canonical target and transitive lineage coverage, the monotonic ForgetFence generation/cursor, canonical suppression and the D-domain proof. There is one Forget decision space even if Storage physically persists the bytes.

Namespace is a resolved Scope/partition attribute. It may constrain matching but is not an independent fence identity and cannot replace typed canonical target identity, exact Memory/Version refs, source identity or derived lineage. The target set must state exact Scope coverage and source-to-derived lineage.

Any Storage-local Memory/Version fence row is a derived, rebuildable projection of the D-owned authoritative snapshot. It MUST NOT issue its own generation/cursor, decide coverage or authorize reads/publication without current D authority. Storage retains physical transaction durability, atomic visibility, backup/restore, recovery, replication and anti-rollback authority for the physical store; physical custody does not transfer logical authority. Projection mismatch fails closed and is reconciled from D.

Every read/write/publication, Compiler, Retrieval/Index, Context, Delivery/reconnect and final-request gate must establish a current D snapshot/cursor for the exact target/lineage. Missing, stale, corrupt, rolled-back or insufficiently scoped D state fails closed. Local target suppression is not Global Forget Completion; I retains global policy, retention, legal-hold, external-copy and physical-erasure authority.

Reviewer criteria:
- FF-A1 PASS iff D is the only logical issuer/authority of ForgetFence generation/cursor; otherwise FAIL.
- FF-A2 PASS iff Storage-local fences are rebuildable D-derived projections with no independent sequence/cursor; otherwise FAIL.
- FF-A3 PASS iff namespace does not replace typed target, Scope and transitive lineage coverage; otherwise FAIL.
- FF-A4 PASS iff missing/stale/corrupt D state blocks affected reads/publication; otherwise FAIL.
- FF-A5 PASS iff local suppression is distinct from I-governed Global Forget Completion; otherwise FAIL.

Open: D public snapshot/read API, exact target/lineage schema acceptance, cross-owner execution order, Storage physical anti-rollback proof and implementation/conformance.
