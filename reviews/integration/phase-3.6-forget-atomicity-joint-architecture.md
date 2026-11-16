# Phase 3.6 — D/E/Storage Joint Forget Atomicity Architecture

- Date: 2026-11-16
- Joint architecture authority: user-delegated DE-S team (D / E / Storage)
- Repository: oahcom/AiMemoryBrainArchitecture
- Status: **DE-S OWNER ARCHITECTURE ALIGNED / JF-10 V2 PROPOSED TO I / I GOVERNANCE AND JF-10 ACCEPTANCE OPEN / IMPLEMENTATION NOT VERIFIED / TESTS NOT RUN**
- Write scope: D, E and Storage Owner branches only. This report is published on the Storage Owner branch. No I or A file is modified; no branch is merged.
- This document is the common DE-S architecture version. It preserves the decided JF-01..JF-09 baseline and supersedes the split JF-10 v1 interpretation with a revised owner-gate-participating 2PC proposal. The revised JF-10 is not represented as I-approved.

## 1. Branch-aware source baseline and readback

### 1.1 Live branch snapshot before this report publication

| Owner | Branch | HEAD SHA |
|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 6a22f86e4fa04a2f00a67b45c3389b65d721d127 |
| E | session-e-memory-compiler-2026-11-16 | ba769bed2956c2550c37fcc5ba7bd4c21332d576 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 52c492091bcc88a8c17e1099fe8ac61296174456 |
| I (read-only dependency) | session-i-security-governance-2026-11-16 | 678a97ef6b43aed9f51f8ecdadf0955ea53915fa |
| A (integration context) | session-a-integration-2026-11-16 | 801406ab8c190da781ba019a154c1fa0cd3ff075 |
| main (comparison only) | main | 8a6414158c9c056c1638222534e1993d1bbc99d2 |

These are live branch refs re-read after DE-S owner-file updates. Historical HEADs in older reports are not substituted for this snapshot. The report publication itself advances the Storage branch; its post-publication HEAD is recorded in the delivery evidence outside this pre-write snapshot.

### 1.2 Updated owner artifact manifest

| Owner | Authoritative artifact | Blob SHA | Owner-side disposition |
|---|---|---|---|
| D | 03-memory-brain/forget-fence-operation-and-publication-gate.md | 9dd71428e512b6d22c5ed6abb2f6e2c54260bce8 | D owner acceptance of D fence/serialization predicates; D36 rows 11–13 added |
| D | 03-memory-brain/phase-3.6.2-jf10-cross-authority-recovery-protocol.md | d544cc38a922b314e6dc45dd4db76aae6b47f5fc | Exact shared JF-10 v2 bytes |
| E | 04-memory-compiler/phase-3.6-producer-publication-conformance.md | a17f065e69e809fceacb51873d6a36a8b0f5c235 | E owner acceptance; E36-21..23 added |
| E | 04-memory-compiler/phase-3.6.2-jf10-cross-authority-recovery-protocol.md | d544cc38a922b314e6dc45dd4db76aae6b47f5fc | Exact shared JF-10 v2 bytes |
| Storage | reviews/storage-consistency/phase-3.6-deployment-selection-and-verification-readiness.md | 89f8fb36f22a2c1eb7920e0d2941cfcc85652a5c | Storage accepts logical participant/recovery model; concrete engine remains open |
| Storage | reviews/storage-consistency/forget-atomicity-storage-realization-review.md | 2830bb6ea0da45f67e06dd909c8fb80e74e68058 | C21–C23 added |
| Storage | reviews/storage-consistency/phase-3.6.2-jf10-cross-authority-recovery-protocol.md | d544cc38a922b314e6dc45dd4db76aae6b47f5fc | Exact shared JF-10 v2 bytes |
| I (read only) | 09-security-governance/phase-3.6.2-jf10-owner-gate-ordering-correction.md | 57474cfb0c5da07a2cbcbeff1fc792ced36c5dd6 | Normative I36-SR-02 correction; v1 split protocol not accepted |
| I (read only) | 09-security-governance/phase-3.6.2-jf10-commit-authorization-recovery-acceptance.md | 77ffa8f019ea7734e22d785953e54f65c05208ac | I-owned receipt/replay/terminal semantics accepted with boundary clarifications |
| I (read only) | 09-security-governance/global-forget-target-inventory-and-completion-evidence.md | 9100061fa986fb6676656169de3fcf9fc1c72664 | Candidate I inventory/completion contract; not governance-approved |

The common JF-10 v2 file has the same exact Blob SHA on D, E and Storage. This proves byte-identical architecture text, not independent human signatures or I approval. The three owner-specific artifacts above record D, E and Storage's respective technical acceptance boundaries.

### 1.3 Discovery result

The D, E and Storage branches contain the authoritative Forget/Compiler/Storage documents even when the same files are absent from main. Main is comparison-only. The reviewed DE-S source tree contains architecture Markdown but no implementation source, executable test project, database migration, DB configuration, runtime deployment manifest or CI test harness. This is repository evidence only; it does not assert that no external implementation exists elsewhere.

## 2. Preserved architecture decisions

No redesign is made to the already-decided JF-01..JF-09 semantics:

1. Stable ProducerWorkItemId is the root barrier identity across retry, DLQ, replay, worker restart and lease replacement. AttemptId, LeaseId and LeaseEpoch identify executions only.
2. ProducerClass must be registered/enabled and every ProducerWorkItem must be durably registered before enqueue, lease, protected source dereference, execution, retry, DLQ replay or publication.
3. RegisterProducerWork and InstallForgetFence share one linearizable ordering domain per Canonical Memory Authority and affected lineage.
4. Fence installation captures an immutable ProducerRegistrationHighWater, ProducerRegistryVersion and target-set digest in the same transaction that commits ForgetFenceGeneration and the barrier snapshot.
5. Complete direct/transitive dependency registration and a frozen output manifest precede visibility.
6. Every staged artifact remains private until the final visibility transaction commits.
7. Final publication revalidates current D fence, work/attempt/lease, dependency set, manifest, inventory seal and I-authoritative authorization at the actual owner gate.
8. Unknown outcomes remain UNKNOWN/IN_DOUBT; timeout, missing ACK, lease expiry, queue deletion, DLQ parking and stale replica are never proof of abort or terminality.
9. Retry/replay preserves stable IDs/digests and rechecks current fences and authorization; stale work cannot mint a new identity to escape Forget.
10. Reader visibility is determined by the authoritative Storage VisibilityPointer and PublicationReceipt, never by staged bytes, object listing, queue, outbox, index, cache or E-local state.
11. Late derivative or newly discovered lineage invalidates/reopens prior barrier/completion evidence.
12. I Global Producer Inventory and D per-operation work high-water remain separate typed authorities.

The two prior DE-S six-dimension review rounds remain valid for the baselines they reviewed and recorded zero new findings. They do not constitute review of the newly revised JF-10 v2 by I or proof of implementation.

## 3. Final architecture and authority matrix

| Concern / authoritative object | Authority | D/E/Storage boundary |
|---|---|---|
| Canonical ForgetOperation ID/state, request/target digest, affected canonical refs | D | D defines semantics and lifecycle; I supplies authorization |
| ForgetFence and FenceGeneration | D | Monotonic per D authority; no caller-supplied generation grants publish rights |
| ProducerClass registry and D ProducerWork registration ledger | D | D owns canonical admission receipts and registration sequence; module owners authenticate their producers |
| ProducerDomainInventoryEpoch and InventorySealReceipt | I | I alone proves global producer/recipient domain completeness |
| ProducerRegistrationHighWater / BarrierSnapshotReceipt | D | Per Canonical Memory Authority, captured atomically with fence installation |
| CanonicalCommitCursor | D | Per Brain authority; canonical commit/audit ordering, not ProducerRegistrationSequence, FenceGeneration or PermissionEpoch |
| Derived Dependency / complete lineage set | D inventory; E supplies lineage | D owns durable dependency receipt and completeness predicate; E owns extraction/manifest correctness |
| Compiler WorkItem/Attempt/Lease/DerivationRun and staged output | E | E owns execution and retry lifecycle; stage remains private |
| OutputManifestVersion/digest | E | Immutable for a publication operation; mutation requires explicit reopen/new version and re-registration |
| CommitAuthorizationReceipt, PermissionEpoch, revocation order and I sequencer decision | I | I owns credential and policy-domain order; DE-S cannot mint, reinterpret or approve it |
| Per-authority coordinator and local transaction | Storage with D owner semantics | One DB transaction domain for D/Storage authoritative rows |
| VisibilityPointer, PublicationReceipt, owner commit cursor/outcome | Storage | Sole durable reader-visible publication authority |
| Transactional Outbox | Storage | Same-transaction notification only; never visibility or barrier proof |
| CanonicalSuppressionComplete | D | D-local canonical barrier/target proof only; not Global Forget Completion |
| Global Forget Completion / exceptions / physical erasure | I | Requires I-approved policy and complete evidence vector; never inferred by D/E/Storage |

### 3.1 Typed cursor and epoch scopes

- ProducerRegistrationSequence and ProducerRegistrationHighWater: one D producer-work ledger per Canonical Memory Authority; H is the immutable captured upper bound for that fence.
- CanonicalCommitCursor: one ordered cursor per Brain authority for canonical commit/audit events.
- ForgetFenceGeneration: D suppression namespace, monotonic per D authority.
- ProducerDomainInventoryEpoch: I global producer/recipient catalogue epoch.
- PermissionEpoch: I policy-domain authorization/revocation namespace.
- LeaseEpoch: E attempt fencing namespace.
- InventorySealReceipt, BarrierSnapshotReceipt, IndexWatermark and ContextVersion retain their own authorities and scopes.

No cross-namespace numeric comparison, conversion or substitution is allowed. A multi-authority Forget uses per-authority cursors/barriers plus I's global inventory seal; there is no invented global D cursor.

## 4. Canonical Forget protocol and state machine

### 4.1 Fence linearization point

The D linearization point is the durable commit of the InstallForgetFence transaction in the Canonical Authority DB. That one transaction:
- resolves ForgetOperation idempotency key + normalized request digest;
- allocates a strictly increasing FenceGeneration;
- persists exact target/version-family/lineage digest and ForgetFenceCursor;
- snapshots the committed ProducerRegistryVersion and ProducerRegistrationHighWater;
- persists immutable BarrierSnapshotReceipt;
- records the fence installation CanonicalCommitCursor and outbox intent.

A retry of the same ForgetOperationId/digest returns the same generation and H. Same idempotency key with changed digest conflicts. Fence generation is never reused or decreased.

### 4.2 Producer admission before and after fence

- Registration transaction wins first: accepted work receives durable RegistrationReceipt and sequence s; if fence later installs, s <= H and work is included in the barrier.
- Fence transaction wins first: ordinary work referencing covered target/lineage is rejected or quarantined; only explicitly cleanup/suppression-only work may be admitted, with no ordinary publish capability.
- Concurrent operations serialize in the same per-authority DB order. There is no admitted-but-unaccounted work state.
- Queue insertion, worker lease, producer-local mutex or process memory is not registration.

### 4.3 Barrier and work resolution

Every pre-fence work item at/below H must reach a durable terminal disposition:
- published before fence with complete dependency registration and inventory evidence;
- cancelled/expired with stale attempt fenced and no future publication;
- suppressed/quarantined by the fence;
- failed and durably parked with publication disabled, which remains unresolved unless D's explicit terminal criteria are satisfied.

An expired lease is not terminal. An unresolved attempt, retry, DLQ/replay, child work, unknown publication outcome, missing dependency receipt, registry gap or late derivative keeps the barrier open. Multi-output WorkItem terminality requires every output and child path to be accounted for.

### 4.4 ForgetOperation lifecycle and completion

D phases: Requested -> FenceEstablished -> InventoryOpen -> BarrierDraining -> TargetReconciliation -> CanonicalSuppressionComplete, with Blocked/Failed branches. Memory lifecycle (Candidate/Consolidated/Active/Superseded/Archived/Forgotten) is separate.

D may declare CanonicalSuppressionComplete only when:
- the exact fence and immutable barrier snapshot are known;
- all captured ProducerWorkItems and descendants have durable terminal dispositions;
- all derivative dependencies are complete and reconciled;
- no unknown producer class, registration gap, unresolved lease/retry/DLQ/replay/publication or late derivative remains;
- every D-domain target is suppression-confirmed or carries an exact I-approved residual exception;
- canonical target suppression proof and final reconciliation cursor are durable.

D does not declare Global Forget Completion. I additionally decides the mandatory global target set, current inventory seal, offline/unsupported policy, backup/restore and external-recipient evidence, physical-erasure requirements and exceptions.

## 5. E Producer and Publish Gate

### 5.1 Accepted Receipt

Accepted Receipt means ingress accepted and idempotently recorded. It does **not** mean canonical Memory committed, a derivative was registered, publication succeeded or the artifact is visible.

### 5.2 Producer lifecycle

1. Authenticate/bind ProducerIdentity and ProducerClass.
2. Resolve/obtain D ProducerClass registration and durable WorkItem RegistrationReceipt.
3. Only then enqueue, lease, dereference protected source or execute.
4. Extract/normalize/consolidate and build immutable output manifest with exact source revisions and direct/transitive lineage.
5. Register the complete dependency set durably with D before publication prepare.
6. Write candidate bytes only to private staging.
7. Submit one stable PublicationOperationId/RequestDigest to the actual Storage final gate.
8. Remain non-terminal until matching Storage PublicationReceipt and VisibilityPointer are authoritatively read back.
9. On retry/replay/recompile, preserve root WorkItemId and lineage, allocate fresh AttemptId/LeaseEpoch and explicit DerivationRunId as appropriate, and recheck current D/I state.

### 5.3 Final Publish Gate

All conditions are conjunctive:
- exact ProducerWorkItem registration exists and remains eligible;
- AttemptId/LeaseEpoch is current and not terminal/stale;
- exact source revisions, target scopes and complete dependency digest are durable;
- output manifest version/digest is frozen and unchanged;
- current D ForgetFence permits the exact artifact and all ancestors;
- current I inventory seal/epoch required for this target is authentic and current;
- I CommitAuthorizationReceipt is valid for the exact operation, digest, policy domain and owner boundary;
- the owner final-gate operation is joined to I's sequencer/2PC order as specified in JF-10 v2;
- Storage local transaction commits VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption + outbox atomically.

Any missing, stale, revoked, incomplete, unavailable or indeterminate predicate leaves bytes private. E may not declare Published based on I COMMIT_WON alone.

## 6. Storage persistence and transaction model

### 6.1 Selected local deployment profile

Select one transactional database per Canonical Memory Authority. D and Storage authoritative rows share a serializable per-authority transaction domain/coordinator. Durable records include:
- ProducerClass registry/version and ProducerWork ledger;
- RegistrationReceipt and ProducerRegistrationSequence;
- ForgetFence, BarrierSnapshotReceipt and ForgetOperation state;
- complete DependencyRegistration and frozen output manifest digest/version;
- WorkAttempt/Lease fencing state;
- PublicationIntent and stable idempotency key/request digest;
- prepared participant/XID and coordinator correlation;
- VisibilityPointer and PublicationReceipt;
- owner outcome and receipt-consumption ledger;
- transactional Outbox and restore/reconciliation checkpoint.

Object/blob storage may hold large immutable bytes only in a private staging namespace. DB VisibilityPointer is the sole publication authority.

### 6.2 Option decision

| Option | Decision | Reason |
|---|---|---|
| Single transactional DB per Canonical Memory Authority | SELECTED for D/Storage local atomicity | One serializable order covers admission, fence, dependencies, visibility and terminal records |
| Durable Work Ledger | REQUIRED | Stable WorkItem accounting and crash/replay recovery; not a serialization mechanism by itself |
| Transactional Outbox | REQUIRED supplement | Atomic same-DB event intent and at-least-once replay; not visibility or completion authority |
| Conditional Update / CAS | REQUIRED inside transaction | Guards generation/version/lease/manifest; standalone CAS cannot atomically cover related rows |
| Serialized Coordinator service | Not selected as a separate best-effort service | Local DB coordinator handles D/Storage order; I sequencer coordinates policy-domain order |
| Durable cross-authority 2PC | SELECTED for JF-10 proposal | I requires actual owner final gate to join revocation order and participant recovery |
| Eventual consistency / process-local lock / check-then-write | REJECTED | Cannot prove no stale publish or uncovered work |
| Independent I COMMIT_WON then unrelated Storage write | REJECTED | Explicitly insufficient under I36-SR-02 |

### 6.3 JF-10 v2 cross-authority topology

The actual Storage final gate prepares the exact owner visibility transaction in the Canonical Authority DB. The durable prepared participant/XID retains the D target/lineage serialization locks, WorkItem/Lease, dependency, manifest and visibility-version predicates. It remains private and non-visible.

Storage then submits that exact prepared participant, stable PublicationOperationId/RequestDigest, owner_boundary and CommitAuthorizationReceipt to the I policy-domain sequencer's owner-final-gate operation. I orders the owner operation against revocation and durably records COMMIT/ABORT with participant identity. The sequencer decision controls forward commit or rollback of the prepared Storage participant.

On COMMIT, the participant commits VisibilityPointer, PublicationReceipt, owner outcome, idempotency/receipt-consumption and outbox in one local transaction. Only after authoritative receipt readback may Storage/E say PUBLISHED. On ABORT, the participant rolls back and remains private. Unknown/in-doubt state retains locks and blocks visibility; revocation cannot pass an unresolved earlier operation by assuming abort.

D fence installation shares the same Canonical Authority DB target/lineage locks. Fence-first rejects prepare. Prepared-participant-first blocks conflicting fence installation until I commit/abort and participant resolution. If publication commits first, the subsequent fence sees it as pre-fence work and suppresses/reconciles it. This is the D ordering boundary, not an I override.

The I sequencer must accept the prepared participant as part of the exact owner-final-gate operation, not merely return a detached authorization token. If I cannot provide durable participant registration/decision/recovery, or the DB cannot durably retain prepared state/locks, JF-10 remains blocked; no weaker protocol is substituted.

### 6.4 Concrete deployment not selected

No production DB engine/version, XA/prepared transaction support, isolation setting, lock timeout behavior, replication/quorum, HA/failover, backup/restore topology or operational runbook has been supplied. Storage engineering must validate durable prepared-XID semantics and coordinator recovery on a real target platform before Deployment Implemented or Implementation Verified.

## 7. Recovery model

| Event | Authoritative recovery |
|---|---|
| Crash before work registration commit | No accepted receipt; no queue/lease/execute; retry same WorkItemId/digest |
| Registration commit, ACK lost | Resolve same receipt; no second sequence or work row |
| Fence commit, ACK lost | Resolve same ForgetOperationId/digest; same FenceGeneration/H |
| Dependency partial write/crash | No complete DependencyRegistrationReceipt; artifact remains private |
| Crash after owner prepare, before I order | Recover prepared XID and locks; submit/replay same I owner-gate operation |
| I COMMIT durable, Storage not committed | Forward-commit exact prepared XID; keep readers closed until Storage commit |
| I ABORT durable, Storage not rolled back | Roll back exact XID; keep bytes private until abort confirmed |
| Storage visibility commit, ACK lost | Read authoritative PublicationReceipt/VisibilityPointer; return same result |
| Outbox replay | At-least-once delivery with event ID and operation dedupe; no second visibility effect |
| Stale lease/old worker | LeaseEpoch rejects dependency, publish and terminal writes |
| I or Storage coordinator unavailable | UNKNOWN/IN_DOUBT; retain prepared locks; fail closed; recover durable decision |
| Backup/restore | Quarantine before serving; restore coordinator log, prepared participant, D fence and inventory evidence; reconcile before reader admission |
| Old Compiler task after Forget | Resolve original WorkItemId/lineage; current fence suppresses; no new ID or publication; late derivative reopens proof |

No absence, timeout, ACK loss, stale replica or process death is proof of NOT_COMMITTED. A negative terminal result requires authoritative durable ABORT plus participant rollback proof. A positive publication result requires both I decision evidence and committed Storage PublicationReceipt/VisibilityPointer.

## 8. I external dependency contract and request

### 8.1 Producer inventory split

I maintains the complete Producer Domain Inventory and issues ProducerDomainInventoryEpoch + immutable signed InventorySealReceipt. It must enumerate every domain/instance capable of creating, transforming, retaining, copying, serving, restoring, exporting or receiving target/derivative data, including D/E/F/G/H, queues/retries/DLQ, indexes/caches, Context, adapters/regions, replicas, backups, external recipients, onward recipients and relevant audit/observability stores.

D maintains its canonical producer-class/work registration ledger and per-operation ProducerRegistrationHighWater. D proves which concrete pre-fence work items were admitted in its authority. D's H cannot prove that all global producer/recipient domains were enumerated; I's epoch/seal cannot replace D's H. Both are required and remain separate.

### 8.2 Inventory change during Forget

I increments ProducerDomainInventoryEpoch when producer/recipient membership, instance, owner/issuer, Scope, capability, backup/restore path or evidence obligation changes. Any relevant epoch change or late target discovery invalidates the current seal and reopens global reconciliation. I issues a replacement seal/digest; all newly applicable targets/evidence are reconciled.

D's already committed fence generation and H remain immutable; they are not silently recaptured. Newly discovered work/targets are handled by D's current-fence checks, suppression/reconciliation and a new proof checkpoint. New producer classes/instances cannot process protected data until authenticated registration/admission. A global completion claim is prohibited while the seal is stale or a registry gap remains.

### 8.3 Unknown, offline and unsupported producers

Unknown/unregistered producer: DENY/QUARANTINE; no auto-registration and no implicit NotApplicable.
Offline/unsupported/missing target or missing acknowledgement: UNKNOWN/PENDING by default. It remains an open global evidence obligation unless I issues an exact policy-approved exception with target, scope, rationale, approver, expiry/review and residual risk.
Rejoining workers must authenticate and reconcile current D fence and I inventory/authorization before source dereference or execution.

### 8.4 Authorization and Global Completion

I's technical interface record retains stable operation ID/digest, CommitAuthorizationReceipt binding, authoritative lookup/replay, hard conflict on changed digest, durable terminal outcomes and sequencer recovery. However I's later owner-gate correction explicitly rejects JF-10 v1's detached COMMIT_WON followed by an independent Storage transaction. The exact v2 participant protocol in this report is submitted for I review; it is not accepted yet.

I alone approves PermissionEpoch policy, ProducerDomainInventoryEpoch/InventorySeal governance, unknown/offline exception policy, Global Completion Evidence Vector, mandatory target states, backup/retention/restore and physical-erasure rules. The inventory contract remains CANDIDATE; I36-GOV-01..10 remain GOVERNANCE-BLOCKED in the inspected I record. No I authority is assumed.

### 8.5 Exact I Owner decision requested

I is asked to accept or amend the exact common JF-10 v2 Blob SHA d544cc38a922b314e6dc45dd4db76aae6b47f5fc, specifically:
1. Storage prepared participant/XID is part of the actual owner-final-gate operation submitted to the I sequencer.
2. I's durable COMMIT/ABORT decision is tied to that participant and is recoverable; revocation cannot pass an unresolved earlier final gate.
3. I defines coordinator log retention, participant registration, authoritative decision lookup, recovery ownership, failover/restore and multi-policy-domain all-or-none semantics.
4. COMMIT_WON is not reader-visible publication; Storage participant commit and PublicationReceipt readback are required.
5. I confirms that its global inventory/seal and governance decisions remain I-owned and are not inferred from D's local barrier.

DE-S does not modify I-owned files or close I governance blockers.

## 9. Twelve mandatory architecture scenarios

Each scenario defines the authoritative order, legal outcomes, forbidden transitions and safety invariant. These are architecture outcomes, not executed tests.

| # | Scenario and ordering | Legal outcome / transitions | Forbidden transition | Invariant |
|---|---|---|---|---|
| 1 | ProducerClass/ProducerWork registration races Fence installation | Same DB serializes. Registration first gets durable receipt/sequence and is included at/below H; fence first rejects/quarantines ordinary work | Accepted work outside H; queue/lease before receipt | No admitted-but-unaccounted work |
| 2 | Work registration races High-Water capture | Registration sequence allocation and H capture occur in the same per-authority transaction order | Read sequence in one store and capture H later from queue scan | Every pre-fence accepted work is at/below immutable H |
| 3 | Dependency registration races Fence | Complete dependency set first is durable and included in reconciliation; fence first rejects covered lineage and artifact remains private | Partial dependency receipt treated complete; post-fence source derivative registered as ordinary | No visible derivative without complete lineage and fence accounting |
| 4 | Derived Publish races Forget | Storage prepared participant and fence use same target locks. Fence first rejects; participant first holds ordering until I commit/abort, then fence proceeds and captures/suppresses a pre-fence publish | Fence slips between final D check and visibility commit | No third state and no post-fence publication |
| 5 | Publish commits but external ACK is lost | Read same PublicationOperationId/digest; return original PublicationReceipt | Mint new operation or duplicate visibility | Commit outcome is resolved by authoritative readback |
| 6 | Commit crashes at each boundary | Before prepare: no participant; after prepare: XID recoverable; after I decision: participant forward commit/rollback; after DB commit: receipt readback | Infer abort from missing row/ACK; expose prepared bytes | Durable coordinator decision and participant recovery converge |
| 7 | Durable Work Ledger recovery | Recover stable WorkItemId, immutable digest, registration sequence, attempts/LeaseEpoch and terminal receipts | Delete queue entry or expired lease closes barrier | Work accounting survives worker/process/queue loss |
| 8 | Outbox replay duplicates event | Outbox replays at least once; consumer dedupes by stable event/operation ID and reads authoritative receipt | Outbox delivery creates second publication or proves visibility | Outbox is propagation only |
| 9 | Permission revocation races Publish | I sequencer orders actual owner final gate vs revocation; COMMIT decision triggers participant commit; REVOCATION/ABORT blocks; unknown remains private/in-doubt | Detached earlier ALLOW followed by independent owner write | Revocation cannot be bypassed between authorization and owner gate |
| 10 | Producer offline then rejoins | Original WorkItemId/lineage resolves; latest fence and current I identity/inventory state are checked before source access; stale attempt suppressed | Resume from local queue/cache or mint new work identity | Offline is not success; no stale producer resurrection |
| 11 | Global Inventory changes during Forget | I epoch change invalidates old seal; new seal and newly applicable target evidence required; D H remains immutable | Treat D H as global inventory proof or reuse stale I seal | Global closed-world proof binds one current I epoch/seal |
| 12 | Old Compiler task resumes after Forget completion | Current D fence suppresses before publish; late derivative reopens D proof and is audited | Trust old receipt/generation, re-use completion proof, publish under new ID | No late derivative or replay resurrection |

## 10. Validation and test specification assessment

### 10.1 Required status vocabulary

| Status | Meaning |
|---|---|
| Architecture Scenario Defined | The race/failure has an explicit order, legal outcomes, forbidden transitions and invariant |
| Architecture Review Passed | The exact architecture baseline completed the stated review; does not imply implementation |
| Test Specification Complete | Test IDs, setup/actors, fault injection point, expected/forbidden outcome and required evidence are defined |
| Software Test Executed | An implementation and environment ran the test and raw results were retained |

### 10.2 Existing test inventory

- D36: original D §9 rows 1–10 preserved; rows 11–13 added for offline rejoin, inventory epoch change and stale task after canonical suppression.
- E36: E36-01..20 preserved; E36-21..23 added for the same missing cross-cutting cases.
- Storage: C01–C20 preserved; C21–C23 added.
- JF-10: JF10-01..08 and JF10-I-09..13 added for owner-gate participation, 2PC participant crash/recovery, D fence ordering, multi-domain operation, backup/restore, replay, digest conflict, I replica lag, revocation and sequencer failover.

### 10.3 Twelve-scenario coverage mapping

| Scenario | D36 | E36 | C-series | Additional |
|---|---|---|---|---|
| 1 Registration vs Fence | §9 row 1 | E36-02 | C01–C03 | JF10-06 |
| 2 Registration vs High-Water | §9 row 1 | E36-02 | C01–C03 | D immutable H assertion |
| 3 Dependency vs Fence | §9 dependency variant | E36-08 | C04 | JF10-06 |
| 4 Publish vs Forget | §9 row 8 / publish matrix | E36-09, E36-11 | C05, C15 | JF10-06 |
| 5 Publish ACK lost | §9 row 4 | E36-12 | C09, C17 | JF10-04 |
| 6 Commit crash | §9 row 3/4 | E36-13/14 | C06–C09, C14, C19 | JF10-02/03/05 |
| 7 Work Ledger recovery | §9 row 5/6 | E36-04/05/16 | C10–C12, C18 | JF10-05 |
| 8 Outbox replay | §9 replay variant | E36-15 | C13 | JF10-04 |
| 9 Permission revocation vs Publish | §9 row 9 | E36-10/11 | authorization extension | JF10-01/12 |
| 10 Offline producer rejoin | §9 row 11 | E36-21 | C21 | I inventory/identity evidence |
| 11 Inventory change during Forget | §9 row 12 | E36-22 | C22 | replacement InventorySeal |
| 12 Old task after Forget | §9 row 13 | E36-23 | C23 | late derivative proof reopen |

### 10.4 Test completeness and execution state

- Architecture Scenario Defined: **YES** for all twelve requested scenarios.
- Architecture Review Passed: **YES** for the previously reviewed JF-01..JF-09 DE-S baseline (two consecutive zero-finding rounds). The new JF-10 v2 has D/E/Storage owner-side alignment but is **NOT I-ACCEPTED** and has not completed an independent I cross-authority review.
- Test Specification Complete: **ARCHITECTURE-LEVEL SCENARIO SPECIFICATIONS COMPLETE** after D36/E36/C21–23/JF10 additions. Execution-ready harness detail remains incomplete: no runnable build, deterministic fixture package, database instance/configuration, fault-injection runner or CI command exists in the inspected repository.
- Software Test Executed: **NO — D36, E36-01..23, C01..C23 and JF10-01..13 are NOT RUN.** Not run is not pass and not fail.
- Implementation Verified: **NO**.
- Concrete Deployment Implemented: **NO**.
- Global Forget Completion: **NOT CLAIMED**.

Before execution, the test owner must bind each test to an implementation commit, DB engine/version/isolation and HA configuration, deterministic seed, actor/connection schedule, exact pause/crash point, operation IDs/digests, expected/actual receipts, transaction/XID/lock/sequencer trace, authoritative reader snapshot, recovery log and invariant checker output.

## 11. Joint owner confirmation and residual gates

| Owner | Confirmed in its Owner artifact | Still not claimed |
|---|---|---|
| D | D fence/high-water/dependency/lineage predicates and serialization against prepared Storage participant; CanonicalSuppressionComplete boundary | I governance, global inventory completeness, DB implementation or tests |
| E | Accepted Receipt vs canonical commit distinction; stable WorkItem/Attempt/Lease lifecycle; frozen manifest/dependency and private staging; Published only after Storage receipt readback | Compiler runtime, executable E36, I policy approval |
| Storage | One DB per Canonical Memory Authority for D/Storage rows; durable 2PC participant model for I final-gate order; pointer/receipt/outbox atomicity | Concrete DB/XA support, HA/restore deployment, independent engineering sign-off and test results |

The same JF-10 v2 Blob SHA is recorded in all three Owner branches. This is a common technical text baseline and delegated architecture confirmation, not human signatures or final I acceptance.

### 11.1 Open gates

| Gate | Owner | Closure evidence |
|---|---|---|
| JF-10 v2 exact protocol acceptance | I + D/E/Storage | I reviews Blob d544cc38a922b314e6dc45dd4db76aae6b47f5fc and accepts/amends; D/E/Storage resolve any comments |
| I durable sequencer participant/2PC implementation | I | Durable decision log, participant registry/XID, lookup, retention, failover/restore and multi-domain evidence |
| Global Producer Inventory and InventorySeal | I | Approved authoritative registry, signed current seal, epoch invalidation and complete membership proof |
| PermissionEpoch/governance activation | I and authorized governance approvers | Exact approved policy/hash, approver authority, scope/jurisdiction, effective version/time, expiry/review and audit |
| Unsupported/offline/exception policy | I and relevant governance authorities | Explicit exception authority and criteria; otherwise Unknown/Pending |
| Concrete DB deployment | Storage engineering | Engine/version, prepared-XID semantics, serializable isolation, HA/failover/replication, backup/restore, runbooks |
| Runtime implementation | D/E/Storage engineering | Executable APIs, ledger schemas, prepared participant, pointer/receipt/outbox and restore gates |
| D36/E36/C/JF10 execution | D/E/Storage test owners | Reproducible build, fixtures, deterministic faults, raw evidence and independent test review |
| Consumer conformance | F/G/H/C and I | Read/index/cache/Context/Adapter and final-request evidence |
| Global Forget Completion | I and target owners | Current seal, all required target acknowledgements, backup/external/physical-erasure evidence and approved exceptions |

## 12. Final disposition

**DE-S architecture:** Owner-side architecture is aligned on the preserved JF-01..JF-09 contract, the selected local transactional DB profile and the revised JF-10 v2 2PC proposal. D/E/Storage authoritative files have been updated on their respective Owner branches; no branch was merged.

**JF-10:** P0 remains OPEN pending I review and acceptance of the exact owner-gate-participating protocol. The earlier detached I COMMIT_WON + independent Storage commit is explicitly rejected. Until I accepts a conformant protocol and implementation is verified, protected publication fails closed on unresolved cross-authority state.

**I governance and Global Forget:** BLOCKED / CANDIDATE. No policy approval, global inventory seal, offline exception approval or Global Forget Completion is claimed.

**Implementation and tests:** NOT VERIFIED / NOT RUN. Architecture decisions and test specifications are not software execution evidence.

No I-owned file was modified. No other Owner branch was merged. No physical-erasure, production-readiness or Phase 3.6 overall final-acceptance claim is made.


## 13. Post-publication branch refresh

A further live branch read after the report publication found the I Owner branch advanced from the §1.1 snapshot HEAD 678a97ef6b43aed9f51f8ecdadf0955ea53915fa to **36171dff26ff1251d5ad6a8e54a41bfa49b5e2c2**. The relevant I JF-10 correction Blob remains **57474cfb0c5da07a2cbcbeff1fc792ced36c5dd6**, the I JF-10 interface acceptance Blob remains **77ffa8f019ea7734e22d785953e54f65c05208ac**, and the I Global Inventory contract Blob remains **9100061fa986fb6676656169de3fcf9fc1c72664**. The I governance/consumer acceptance register advanced to Blob **11c4bfde5de02a684cc6e5df46d1f9676f5a40a5**; its latest readback recognizes H design acceptance but continues to record JF-10 P0 OPEN and I36-GOV-01..10 GOVERNANCE-BLOCKED. No I response accepting or amending the newly submitted DE-S JF-10 v2 was present in issue #4 at this refresh.

D, E and Storage Owner branch HEADs remained respectively **6a22f86e4fa04a2f00a67b45c3389b65d721d127**, **ba769bed2956c2550c37fcc5ba7bd4c21332d576** and **68d06a9b8297a4545dea67efad56b72b6da8d765** before this report append. This refresh changes no I-owned artifact and does not infer I acceptance from the unrelated I register update.
