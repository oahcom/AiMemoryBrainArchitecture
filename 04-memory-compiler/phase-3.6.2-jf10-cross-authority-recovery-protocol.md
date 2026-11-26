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
    canonical_scope: "E-domain Memory Compiler record phase-3.6.2-jf10-cross-authority-recovery-protocol.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-6-2-jf10-cross-authority-recovery-protocol"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-2-jf10-cross-authority-recovery-protocol
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6.2 — JF-10 Cross-Authority Commit Recovery Protocol

- Status: **DE-S ENGINEERING PROPOSAL / CANDIDATE**
- Decision authority: D, E and Storage may define their owner-side consumption and recovery behavior; I alone owns the policy-domain sequencer and `CommitAuthorizationReceipt` semantics.
- Approval: **I acceptance required; no I approval is implied by this proposal.**
- Implementation: **NOT IMPLEMENTED**
- Conformance: **NOT RUN**
- Finding: **JF-10 P0 remains OPEN until I accepts the interface and the protocol passes crash/recovery tests.**

## 1. Problem and safety objective

JF-10 covers two indistinguishable-to-a-caller failure windows:
1. I durably orders an authorization decision as `COMMIT_WON`, then Storage crashes before `VisibilityPointer` and `PublicationReceipt` are durably committed.
2. Storage has committed visibility, but the I response/acknowledgement or the caller's acknowledgement is lost.

A timeout, missing response, absent replica row or process restart is never evidence of either commit or non-commit. The protocol must preserve I's revocation ordering and D's fence ordering while ensuring that bytes remain private until the Storage visibility transaction commits.

## 2. Normative authority boundaries

- **I** is authoritative for issuer/principal/actor authorization, PermissionEpoch, revocation ordering, and the durable terminal sequencer outcome.
- **D** is authoritative for ForgetFence, captured work/barrier state, dependency completeness, and the D-side publication predicate.
- **E** is authoritative for producer execution state and frozen output/lineage manifest inputs; it cannot declare an artifact Published.
- **Storage** is authoritative for the durable `VisibilityPointer`, `PublicationReceipt`, owner commit cursor, and reader-visible publication state.
- `VisibilityPointer` remains the sole publication authority. Staged object existence, outbox delivery, I authorization alone, and E local state never make bytes visible.

## 3. Stable operation identity and immutable binding

Before contacting I, Storage MUST durably persist an owner-side publication intent in the same Canonical Memory Authority database that owns the visibility pointer. The intent has:
- stable `PublicationOperationId` / idempotency key across retries and recovery;
- canonical `RequestDigest` covering the full immutable request;
- `CommitAuthorizationReceipt` reference or the exact I request binding;
- policy domain, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef and DelegationChainRef;
- ForgetOperationId, fence generation/high-water, WorkItemId, AttemptId, LeaseEpoch, ProducerRef;
- DependencySetDigest, OutputManifestVersion/digest, ProducerDomainInventoryEpoch and InventorySealReceipt digest where required;
- owner authority, intended visibility operation and creation/decision metadata.

Same operation ID + same digest is an idempotent replay. Same operation ID + different digest is a hard conflict and MUST be rejected/audited. A new operation ID MUST NOT be minted to escape an unresolved outcome.

## 4. Commit protocol

### Phase A — owner prepare (not visible)

1. E submits the complete frozen manifest and dependency evidence; D validates the current fence/barrier predicate.
2. Storage validates all owner-local predicates and durably inserts `PublicationIntent(PREPARED_FOR_I)` with a unique constraint on operation ID and immutable request digest.
3. No `VisibilityPointer` is written. Artifact bytes remain in private staging.
4. If the prepare acknowledgement is lost, Storage resolves the same operation ID and digest through its authoritative decision barrier. Until resolved, the result is `UNKNOWN`, not `NOT_COMMITTED`.

### Phase B — I sequencer decision (durable and revocation-ordered)

5. Storage requests the I decision using the same operation ID and digest and the single-use, non-transferable `CommitAuthorizationReceipt` bound to the exact protected-operation tuple.
6. I MUST atomically serialize this decision against revocation in the policy domain and durably record one terminal result: `COMMIT_WON`, `REVOCATION_WON`, or `INDETERMINATE_ABORTED`.
7. I MUST expose an authoritative, authenticated lookup by operation ID + digest. Repeating the same request returns the same durable terminal result; a different digest conflicts. A lost I ACK is resolved by lookup/replay, never by creating a new operation.
8. `COMMIT_WON` is an authorization-order result only; it is not, by itself, publication or reader visibility. `REVOCATION_WON` and `INDETERMINATE_ABORTED` prohibit visibility. Unknown/unavailable I state keeps the operation pending and private.

### Phase C — owner visibility commit (one local atomic transaction)

9. After verifying the durable I `COMMIT_WON` result and receipt binding, Storage rechecks the D fence/barrier, WorkItem/Attempt/Lease fencing, dependency digest, frozen manifest version/digest, inventory seal freshness where required, and all owner-local invariants at the actual owner commit boundary.
10. In one transaction in the Canonical Memory Authority database, Storage MUST atomically:
   - compare-and-set the exact expected visibility generation and owner commit cursor;
   - write/update the `VisibilityPointer`;
   - write the immutable `PublicationReceipt` containing the I decision/receipt reference, I sequencer position, exact request digest, D fence generation, manifest/dependency digests and owner commit cursor;
   - record the operation as `OWNER_COMMITTED` with the terminal owner outcome;
   - record idempotent receipt consumption for this operation; and
   - append the same-transaction outbox event.
11. The pointer, receipt, outcome and outbox either all commit or all roll back. Outbox delivery is notification/reconciliation only and is never the visibility authority.
12. Only after this transaction commits may Storage return `PUBLISHED`; E may then record its terminal Published state using the durable Storage receipt. If the D fence or any owner predicate wins, Storage records a non-visible terminal rejection/abort and no pointer is published.

## 5. Recovery and acknowledgement-loss rules

| Durable I outcome | Durable Storage outcome | Recovery action |
|---|---|---|
| `COMMIT_WON` | `OWNER_COMMITTED` with matching digest and receipt | Return the same publication receipt; do not republish or mint new IDs |
| `COMMIT_WON` | Prepared intent, no owner commit | Re-run Phase C with the same operation ID/digest after rechecking D fence and all owner predicates |
| `REVOCATION_WON` | No owner commit | Mark denied/aborted; keep bytes private; no retry under a new key |
| `INDETERMINATE_ABORTED` | No owner commit | Mark aborted/non-visible according to I terminal evidence; preserve audit |
| I outcome unknown/unavailable | No owner commit | Remain `OUTCOME_UNKNOWN`; keep bytes private; query/replay same key only |
| Any I outcome | Storage outcome unknown | Use Storage's authoritative decision barrier; do not infer from missing row or stale replica |
| Storage says committed but I receipt/binding cannot be verified | Any | Quarantine/fail closed; never expose based on Storage row alone |

Recovery workers MUST be idempotent and fenced. They may not bypass the current D predicate, reuse an expired lease, mutate a frozen manifest, accept a changed digest, or turn an unknown state into success. Restores MUST reconcile the control ledger, I terminal decision and owner commit cursor before serving readers.

## 6. Required I interface acceptance

I must explicitly accept or replace the following semantics in an I-owned artifact:
1. durable terminal decision keyed by stable operation ID + request digest;
2. authenticated authoritative lookup/replay returning the same terminal outcome for the same binding;
3. hard conflict for same ID with a different digest;
4. irrevocable retention of `COMMIT_WON` as a sequencer ordering fact, with a documented retention/recovery guarantee sufficient for owner crash recovery;
5. exact relationship between single-use `CommitAuthorizationReceipt`, its consumption record and the terminal sequencer decision;
6. defined behavior for I crash before/after decision persistence, response loss, replica lag, restore and sequencer failover;
7. confirmation that `COMMIT_WON` means authorization won against revocation, not that Storage visibility has already committed.

If I cannot guarantee durable terminal lookup and forward recovery, this protocol is insufficient; a formally specified durable distributed transaction/2PC protocol with participant recovery is required. DE-S MUST NOT silently substitute a cache, lease, stale epoch or local ALLOW.

## 7. DE-S acceptance and implementation evidence

- **D:** confirm the exact point at which fence/barrier state is rechecked and serialized with owner visibility commit; define the owner-side terminal disposition when I says `COMMIT_WON` but D's fence wins before pointer commit.
- **E:** persist the stable operation ID/digest and remain non-terminal until the matching Storage `PublicationReceipt` is durably confirmed; never report Published from I `COMMIT_WON` alone.
- **Storage:** implement the durable intent, unique idempotency constraint, authoritative outcome lookup/barrier, atomic pointer+receipt+outbox transaction, recovery worker and restore reconciliation.
- **All:** retain separate I authorization order, D Forget fence order and Storage visibility commit cursor; do not collapse their authority or watermarks.

## 8. Proposed JF-10 conformance cases (new proposal; NOT EXECUTED)

| Case | Injected failure/race | Required result |
|---|---|---|
| JF10-01 | I records `COMMIT_WON`; Storage crashes before visibility transaction | Same-key recovery completes only after rechecking D/owner predicates; no duplicate pointer/receipt |
| JF10-02 | I decision response lost after durable `COMMIT_WON` | Lookup returns the same decision; no new operation ID |
| JF10-03 | Storage transaction commits pointer+receipt; caller ACK lost | Same-key lookup returns the identical receipt; exactly one visible publication |
| JF10-04 | I revocation races with sequencer decision | Exactly one durable I terminal order; non-winning authorization cannot publish |
| JF10-05 | D ForgetFence installs after I `COMMIT_WON` but before owner visibility commit | D fence predicate wins at owner commit; no pointer; terminal non-visible disposition |
| JF10-06 | Same operation ID replayed with a different digest | Hard conflict; no visibility |
| JF10-07 | I or Storage replica is stale/unavailable during recovery | UNKNOWN/PENDING; no visibility or false NOT_COMMITTED |
| JF10-08 | Restore after I decision but before Storage visibility commit | Reconcile I decision + owner ledger/cursor; complete or remain blocked without unsafe visibility |

Each executed case must retain build SHA, database/runtime version, deterministic fixture/seed, fault-injection point, I decision evidence, Storage transaction/lock/CAS trace, D fence cursor, PublicationReceipt ID/digest, actual outcome and independent reviewer sign-off. This table specifies tests; it is not evidence that they ran.

## 9. Decision and non-claims

This document is a DE-S candidate protocol for I review. It does not close JF-10, approve I governance, establish consumer acceptance, select a concrete database vendor, prove implementation, or pass any test. Until I accepts the required sequencer semantics and executable crash/recovery evidence exists, JF-10 remains **P0 OPEN**, final publication remains fail-closed on unknown outcomes, and Phase 3.6 cannot pass the final gate.


---

# Addendum — Reconciliation against I36-SR-02 owner-gate ordering (JF-10 P0)

- Added: 2026-11-16
- Status: **MATERIAL PROTOCOL GAP IDENTIFIED — I DECISION REQUIRED**
- Applies to the candidate protocol above; it does not silently replace or reinterpret the earlier phases.

## A. Newly confirmed I requirement

The current I-owned joint trust policy (Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`), §10.2, requires:

1. a single logical I authority and linearizable sequencer per policy domain;
2. a single-use `CommitAuthorizationReceipt` bound to the full authorization tuple, operation ID/digest and owner boundary;
3. the operation owner's final commit/disclosure gate to participate in the **same per-domain commit ordering protocol**;
4. atomic ordering of the owner operation commit against revocation, yielding `COMMIT_WON`, `REVOCATION_WON` or `INDETERMINATE_ABORTED`.

The receipt is not a transferable permission or offline lease. I's §10.2 also states that the implementation evidence is NOT VERIFIED.

## B. Gap in the current JF-10 candidate

The existing candidate's Phase B durably records I `COMMIT_WON` as an authorization-order result, after which Phase C independently commits Storage's VisibilityPointer + PublicationReceipt transaction.

That split-phase sequence is useful for idempotency and forward recovery, but **the candidate has not demonstrated that Storage's final owner commit participates in the same I policy-domain ordering protocol**. A prior I decision followed later by an independent Storage transaction cannot be assumed to meet I36-SR-02 merely because Storage stores the receipt ID and sequencer position in its local transaction.

Likewise, a local single-use receipt-consumption row does not by itself prove that receipt consumption and the owner commit are atomically ordered against a concurrent revocation in I's sequencer.

Therefore:
- JF-10 candidate v1 is **NOT YET SHOWN CONFORMANT** to I36-SR-02;
- no claim is made that the existing Phase B/Phase C split is accepted by I;
- JF-10 remains P0 OPEN and publication remains fail-closed for unknown/indeterminate outcomes.

## C. I Owner decision required before protocol freeze

I must publish an I-owned normative protocol decision that defines, at minimum:

1. **Ordering participant:** how the Storage owner gate joins the same per-policy-domain sequencer order as revocation. Identify the protocol participants and the exact linearization point.
2. **Receipt semantics:** whether `CommitAuthorizationReceipt` is a prepare/authorization token, a commit-order reservation, or another primitive; define exactly when and by whom it is consumed, and how consumption is bound to the terminal owner outcome.
3. **Atomic outcome:** how the protocol guarantees that revocation and the Storage visibility commit cannot both win, including the precise meaning of each terminal result.
4. **Crash matrix:** behavior if I crashes before/after recording an order, Storage crashes before/after local durable commit, either response is lost, a participant restarts, replicas lag, or failover/restore occurs.
5. **Recovery authority:** which authority answers an authenticated lookup for the global operation outcome, what durable records are required, and how recovery resumes without minting a new operation ID.
6. **Liveness vs safety:** whether the protocol uses a sequencer-mediated participant protocol, durable prepare/commit with recovery, 2PC or another formally specified mechanism. If no progress is possible during a partition, explicitly preserve safety and specify the blocked state; do not imply availability.
7. **Evidence:** required I sequencer log, Storage transaction proof, participant recovery log, receipt-consumption proof and fault-injection cases.

DE-S does not choose this I-owned cross-authority ordering mechanism or declare 2PC mandatory. I must ACCEPT a concrete protocol, REVISE with an I-owned normative design, or BLOCK with accountable owner and missing proof.

## D. Interim DE-S safety rule

Until I publishes and accepts the owner-gate participation protocol:
- a standalone prior `COMMIT_WON` response is not sufficient evidence to make Storage data visible;
- the final Storage gate must fail closed unless it can prove the I-approved ordering protocol has completed for the exact operation ID/digest and owner boundary;
- missing, stale, replayed, mismatched or indeterminate receipt/outcome leaves staged data private;
- D ForgetFence remains an independent owner-local ordering check;
- no new operation ID may be minted to escape an unknown prior outcome.

## E. Status

This addendum is a DE-S gap report and formal request for I's decision, not an I policy amendment or acceptance. The original candidate remains preserved for traceability. **JF-10 P0 OPEN; I36-SR-02 runtime NOT VERIFIED; no cross-authority atomicity proof; no Phase 3.6 final gate.**


# Addendum v2 — Owner-Gate-Participating Durable 2PC Protocol (JF-10)

- Status: **DE-S REVISED ARCHITECTURE PROPOSAL / READY FOR EXACT I OWNER REVIEW; NOT I-ACCEPTED; NOT IMPLEMENTED; NOT TESTED**
- Supersedes: the split Phase-B/Phase-C interpretation in JF-10 candidate v1. Earlier I receipt binding, immutable operation identity, authoritative lookup, replay/conflict and terminal-outcome requirements remain in force.
- This is the D/E/Storage owner-side proposal. It does not amend I policy or claim I approval.

## A. Decision

Adopt a **durable two-phase commit (2PC) participant protocol integrated with the I policy-domain sequencer** for protected publication. A standalone I authorization decision followed by an unrelated Storage transaction is rejected. The actual Storage final visibility gate submits the exact owner operation, with a durable prepared Storage participant, into the same I ordering protocol as revocation.

The deployment profile is two-tier:

1. Within one Canonical Memory Authority, D Forget/producer/dependency ledgers and Storage publication/visibility records share one transactional database and one serializable per-authority coordinator.
2. Across the I policy domain and that owner database, the I sequencer is the durable ordering/2PC coordinator for the protected final owner-gate operation. The Storage database is a recoverable prepared participant. No best-effort coordinator or asynchronous authorization token is permitted.

This is the minimum protocol proposed to satisfy I36-SR-02 while preserving D's independent fence authority and Storage's sole visibility authority. It is a protocol selection, not a concrete vendor/version/deployment approval.

## B. Participants and authority

| Participant | Authority and durable records | Required role |
|---|---|---|
| I policy-domain sequencer/coordinator | CommitAuthorizationReceipt, PermissionEpoch, revocation order, durable transaction decision and participant/XID registry | Orders the exact owner final-gate operation against revocation; records COMMIT/ABORT decision; drives participant recovery |
| Canonical Authority DB (D + Storage) | D ForgetFence, ProducerClass/WorkItem/Dependency ledgers, Storage PublicationIntent, prepared XID, VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption record and outbox | Validates/locks D and owner predicates; prepares exact visibility transaction; commits/rolls back only from I's durable coordinator decision |
| E Compiler | WorkItem/Attempt/Lease lifecycle, frozen output manifest, staged bytes, lineage and publication request | Calls final gate; remains non-terminal until authoritative Storage receipt confirms commit |
| D Forget authority | Canonical ForgetOperation, fence generation, per-authority registration high-water, dependency/barrier proof | Serializes fence installation against prepared publication; never treats I authorization as a fence override |
| I inventory registry | ProducerDomainInventoryEpoch, InventorySealReceipt and global target catalogue | Supplies closed-world producer/recipient coverage; remains separate from D work high-water |

## C. JF-10 v2 protocol

### C1. Immutable operation identity

Before any I sequencer call, Storage durably assigns one stable PublicationOperationId and canonical RequestDigest. The digest binds the complete immutable operation: exact artifact/version and payload digest; WorkItemId, AttemptId and LeaseEpoch; ProducerClass/ProducerIdentity binding; source and transitive lineage; ScopeRefs; DependencySetDigest; frozen OutputManifestVersion/digest; D ForgetOperationId, applicable fence generation and target digest; current I inventory epoch/seal reference; policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef; exact owner_boundary; and CommitAuthorizationReceipt/decision binding.

Same ID + same digest is a lookup/replay of the same operation. Same ID + different digest or changed security-bound tuple is a hard conflict. No retry may mint a new ID to escape an unknown outcome.

### C2. Phase 0 — prepare eligibility

E must have a durable D RegistrationReceipt before enqueue, lease, source dereference or execution. E freezes its complete output manifest and lineage. D confirms complete dependency registration. Storage confirms the applicable I InventorySealReceipt is authentic, current and bound to the exact inventory epoch/digest required by I policy. These are preconditions, not publication permission.

Candidate bytes remain in private staging. Object-store listing, path knowledge, signed staging URL, queue state, outbox delivery and E local state cannot make an artifact visible.

### C3. Phase 1 — Storage participant prepare and D fence serialization

The actual Storage final gate opens a serializable transaction in the Canonical Authority DB and prepares the exact visibility transaction. It must:

1. Resolve PublicationOperationId + RequestDigest idempotently.
2. Lock the per-authority coordinator and all affected target/lineage fence rows, ProducerWork/Attempt/Lease rows, dependency-set and frozen-manifest versions, inventory-seal reference, and expected VisibilityPointer generation.
3. Verify the latest D fence for every source ancestor and target; verify WorkItem/Attempt/Lease fencing; verify complete immutable dependencies/manifest; verify current I seal reference and all owner-local predicates.
4. Validate the exact CommitAuthorizationReceipt binding, without interpreting the receipt itself as a sequencer decision.
5. Persist a durable prepared participant/XID and participant digest. The DB prepared state retains serialization locks across process restart and coordinator unavailability. No VisibilityPointer or PublicationReceipt is exposed; bytes remain private.

D InstallForgetFence, RegisterProducerWork and RegisterDerivedDependency use the same per-authority serialization rows/keys. If a fence/registration/dependency transaction wins first, prepare sees that committed state and either rejects or binds the exact eligible state. If the publication participant prepares first, the conflicting D operation cannot pass the held serialization locks until I resolves commit or abort. Thus D fence and publication have exactly one order; lock timeout or participant uncertainty is UNKNOWN, never permission.

If the selected DB cannot durably retain prepared state and locks across crash/restart, this protocol is not implementable on that DB profile and deployment is blocked; a formally equivalent durable participant protocol is required.

### C4. Phase 2 — I sequencer orders the actual owner final gate

Storage submits the prepared participant token, PublicationOperationId, RequestDigest, exact owner_boundary, receipt and participant identity to the I sequencer's **owner-final-gate operation**. This is not a separate preflight authorization call.

I atomically orders this exact operation against revocation in the policy domain and durably records one coordinator decision:

- COMMIT: the exact owner final-gate operation is ordered before conflicting revocation. The I terminal result is COMMIT_WON and includes sequencer position, receipt/decision binding, immutable digest and durable Storage participant/XID identity.
- ABORT: revocation is ordered first or the operation is denied. The terminal result is REVOCATION_WON or INDETERMINATE_ABORTED as defined by I. No visibility is permitted.
- UNKNOWN/IN_DOUBT: no terminal decision is yet recoverably established. Neither participant may infer commit or abort; the artifact remains private and affected ordering remains blocked pending coordinator recovery.

I must not record COMMIT_WON for a free-standing authorization check detached from the prepared owner participant. The coordinator decision and participant identity are durable and recoverable. Revocation cannot pass an unresolved earlier final-gate operation by assuming abort; it must obtain the coordinator's durable decision or remain pending. This is the safety-over-availability rule for an in-doubt transaction.

### C5. Phase 3 — participant completion and visibility

On durable I COMMIT, the Storage participant recovery worker commits the exact prepared DB transaction. In that one local transaction, it atomically writes the VisibilityPointer, immutable PublicationReceipt, owner terminal outcome, idempotent receipt-consumption evidence and same-transaction outbox event. It records the I coordinator decision ID/position, receipt ID, RequestDigest, participant/XID, D fence generation, dependency and manifest digests, inventory epoch/seal, owner commit cursor and visibility generation.

Only after this participant commit is authoritatively read back may Storage return PUBLISHED and E terminalize the work as Published. I COMMIT_WON alone is not publication success.

On durable I ABORT, the participant rolls back; the artifact remains private and the operation becomes non-published only after participant abort is durably confirmed. D locks/reservations are released only after participant resolution. Outbox delivery is at-least-once notification/reconciliation and never the visibility authority.

### C6. D fence interaction

D fence installation and the Storage prepared participant share the same Canonical Authority DB serialization domain and target/lineage locks:

- Fence commit wins before participant prepare: prepare observes the fence and rejects/quarantines the derivative.
- Participant prepare wins: D fence installation is blocked behind the prepared participant. If I commits, Storage commits visibility first and the subsequent fence captures/suppresses that publication as pre-fence work. If I aborts, Storage rolls back and the fence may then install.
- Unknown participant/coordinator state: neither visibility nor fence completion is inferred; the operation remains unresolved and the fence cannot claim a closed barrier while a conflicting prepared publication exists.

This is not an I override of D. It is the shared local ordering mechanism that prevents a fence from slipping between the D check and the owner visibility commit.

## D. Durable state machine

| State | Authority | Legal next state | Forbidden shortcut |
|---|---|---|---|
| PRIVATE_STAGED | E/Storage | DEPENDENCIES_COMPLETE | Reader visibility or Published |
| DEPENDENCIES_COMPLETE | D/E | OWNER_PREPARED or REJECTED | Publish without full lineage |
| OWNER_PREPARED | Storage DB participant | I_ORDER_PENDING | Release locks or expose bytes |
| I_ORDER_PENDING | I coordinator | I_COMMIT_DECIDED, I_ABORT_DECIDED or IN_DOUBT | Treat timeout as abort/success |
| I_COMMIT_DECIDED | I coordinator | OWNER_COMMITTED after participant commit | Mint another ID; report Published before DB commit |
| I_ABORT_DECIDED | I coordinator | OWNER_ABORTED after participant rollback | Publish or retry under changed digest |
| IN_DOUBT | I + Storage recovery | I_COMMIT_DECIDED or I_ABORT_DECIDED after authoritative recovery | Release locks, advance revocation past unknown order, or expose bytes |
| OWNER_COMMITTED | Storage | PUBLISHED receipt readback; E may terminalize | Duplicate visibility effect |
| OWNER_ABORTED | Storage | REJECTED/SUPPRESSED after all outputs resolved | Reopen same intent with changed digest |

COMMIT_WON is the I ordering/commit decision; PUBLISHED is the Storage participant commit plus exact PublicationReceipt readback. These are distinct states. The complete cross-authority operation is successful only when both are evidenced.

## E. Recovery and crash matrix

| Failure point | Required durable state | Recovery |
|---|---|---|
| Before owner prepare commit | No prepared participant; no visibility | Retry same ID/digest; no receipt means no admission |
| After owner prepare, before I order | Prepared XID and locks; private bytes | I coordinator resolves/replays same request; no new ID |
| I order request/ACK lost | I coordinator lookup by ID+digest and XID | Return exact decision/position or UNKNOWN |
| I COMMIT durable, Storage participant not committed | Durable coordinator COMMIT + recoverable prepared XID | Forward-commit exact XID; readers stay closed until participant commit |
| I ABORT durable, participant not rolled back | Durable ABORT + prepared XID | Roll back exact XID; readers stay closed until abort confirmed |
| Storage participant committed, ACK lost | VisibilityPointer + PublicationReceipt + outcome + outbox committed atomically | Read back same receipt; no second publication |
| I/Storage restart or replica lag | Coordinator log and participant XID recovered from authoritative durable state | No stale replica decisions; no serving until reconciliation |
| Backup/restore | Restore manifest plus coordinator/participant decision log and D fence ledger | Quarantine partitions; replay decisions and current fences before serving |
| Coordinator unavailable / partition | Prepared participant remains in doubt and locked | Fail closed; conflicting revocation/fence cannot pass unknown order; recover coordinator or remain blocked |
| Duplicate same key | Original digest/decision | Return same result and sequencer position |
| Changed digest/boundary | Original immutable row | Hard conflict and audit; no overwrite |

No NOT_COMMITTED conclusion is allowed from row absence, timeout, stale replica, missing ACK or process death. A negative result requires an authoritative durable ABORT decision and participant rollback proof.

## F. Storage and deployment decision

- Selected local profile: one transactional DB per Canonical Memory Authority; D and Storage authoritative rows share serializable transactions and a per-authority coordinator.
- Required records: Durable Work Ledger; ProducerClass registry/version; ProducerRegistrationHighWater; ForgetFence and BarrierSnapshotReceipt; dependency set/manifest; prepared participant/XID; PublicationIntent; VisibilityPointer; PublicationReceipt; owner outcome; idempotency/receipt-consumption ledger; transactional outbox; restore/reconciliation checkpoint.
- CAS: required inside selected transactions for generation/version/lease checks; not a standalone cross-record atomicity mechanism.
- Outbox: required in the same Storage commit transaction for downstream notifications; never visibility or completion proof.
- Object storage: allowed only for private staged immutable bytes; DB VisibilityPointer is sole publication authority.
- Serialized coordinator: no independent best-effort coordinator service is selected. The I sequencer is the durable coordinator for the I/Storage protected commit protocol; the local DB coordinator serializes D/Storage owner state.
- 2PC: selected as the cross-authority JF-10 recovery mechanism. If I cannot provide durable coordinator decisions and participant recovery, or the DB cannot retain prepared XIDs/locks, JF-10 remains blocked; no weaker check-then-write substitute is permitted.
- Concrete engine/version, XA/prepared-transaction support, isolation configuration, replication/quorum, failover and backup/restore topology: NOT SELECTED / NOT VERIFIED. Storage engineering approval and executable evidence are required.

## G. Required I Owner decision (not presumed)

I is requested to review this exact v2 artifact and either accept or amend:
1. The owner-final-gate operation is the sequenced I operation and carries the prepared Storage participant/XID, immutable PublicationOperationId/RequestDigest and exact owner_boundary.
2. I's durable coordinator decision is recoverable and controls participant COMMIT/ABORT; revocation cannot pass an in-doubt earlier gate.
3. I defines coordinator log retention, participant registration, decision lookup, recovery ownership, failover/restore and multi-policy-domain all-or-none behavior.
4. COMMIT_WON is not reader-visible publication; Storage must commit and return its PublicationReceipt.
5. I retains sole authority for inventory epoch/seal, PermissionEpoch, authorization policy, exceptions and Global Forget Completion. DE-S does not activate or approve these policies.

Until I accepts the exact revised protocol, JF-10 is **P0 OPEN / I REVIEW REQUIRED** and final protected publication remains fail-closed on unresolved cross-authority state.

## H. Added conformance cases (all NOT RUN)

| ID | Required scenario | Expected invariant |
|---|---|---|
| JF10-01 | Storage prepare enters I owner-gate sequencer while revocation races | Exactly one order; no standalone preflight decision |
| JF10-02 | I COMMIT decision durable, Storage participant crashes before commit | Prepared XID recovered and forward-committed; no visibility before commit |
| JF10-03 | I ABORT decision durable, Storage participant crashes before rollback | Prepared XID recovered and rolled back; no visibility |
| JF10-04 | Storage participant commits, response/ACK is lost | Same receipt returned by readback; no duplicate visibility |
| JF10-05 | Coordinator crashes before/after durable decision | Recover exact decision; unknown remains locked/private |
| JF10-06 | D fence races prepared participant | Fence-first rejects; participant-first blocks fence until commit/abort; no third order |
| JF10-07 | Multi-policy-domain operation | All-or-none decision; no partial visibility |
| JF10-08 | Backup/restore loses local recent snapshot but coordinator decision survives | Quarantine and replay decision/fence before serving |
| JF10-I-09 | Same ID/digest retry after receipt consumption | Identical outcome/position; no second consumption |
| JF10-I-10 | Same ID with changed digest or owner_boundary | Hard conflict |
| JF10-I-11 | I replica lag / unavailable lookup | UNKNOWN; no local ALLOW or NOT_COMMITTED inference |
| JF10-I-12 | Revocation arrives during unresolved participant prepare | Revocation cannot pass unresolved ordering; recovery resolves commit/abort first |
| JF10-I-13 | I sequencer failover/restore | Terminal decisions and participant XIDs remain monotonic and recoverable |

## I. Non-claims and status

This is an architecture proposal for exact I Owner review. It is not I approval, governance activation, concrete DB deployment, implementation, test result, production readiness decision, or Global Forget Completion. D36, E36-01..20, C01..C20 and JF10-01..13 remain NOT RUN until executable implementation and fault-injection environment exist.


## Phase 3.6.2 — I Owner disposition consumed by D/E/Storage

**Disposition source:** I Owner, `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`, Blob `b7b0287cde3922434a560fca90051cc5b418d987`.

**Status correction:** I ACCEPTS the JF-10 v2 architecture for a **single I policy domain with binding clarifications**. This supersedes the earlier §6 statement that I acceptance was still pending. It does not close JF-10 P0, approve implementation, or approve governance. Multi-policy-domain atomicity remains **BLOCKED / NOT ACCEPTED**.

### A. Binding single-domain contract

The owner-final-gate operation MUST bind, as one immutable authorization/participant tuple:

- stable PublicationOperationId and canonical RequestDigest;
- exact owner_boundary for the Storage VisibilityPointer commit gate;
- durable Storage participant identity, XID and participant digest;
- CommitAuthorizationReceipt ID and decision binding;
- policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef and DelegationChainRef;
- applicable D ForgetOperationId/fence reference and exact D owner-predicate evidence;
- when required by effective I policy, authoritative ProducerDomainInventoryEpoch and InventorySealReceipt identity/digest.

I coordinator COMMIT is the authorization/revocation ordering record for this exact participant. It is not publication. Storage MUST forward-commit that same XID after durable COMMIT and MUST NOT publish until the local visibility transaction and matching PublicationReceipt are durably read back.

### B. Receipt consumption and replay

I receipt consumption MUST be atomically bound to the coordinator transaction record, participant XID/digest, operation ID/digest, owner boundary, decision ID, policy domain, PermissionEpoch and sequencer position. A same-ID/same-digest/same-boundary replay returns the same durable state. Any changed digest, XID, boundary or security tuple is a hard conflict. A receipt cannot authorize a second owner operation.

### C. Terminal outcome and in-doubt behavior

- `COMMIT_WON`: durable coordinator decision; Storage forward-commits the exact participant. Not a visibility claim.
- `REVOCATION_WON`: durable revocation-first result; Storage rolls back and proves non-publication.
- `INDETERMINATE_ABORTED`: durable non-success terminal result; Storage rolls back.
- `UNKNOWN/IN_DOUBT`: not terminal. Keep bytes private, retain prepared participant and required locks, and block conflicting revocation progress until authoritative recovery.

No heuristic commit/abort, timeout-based inference, stale-replica decision, or operator override is permitted. I's authoritative lookup must be authenticated and linearizable. Coordinator log, participant identity, receipt consumption and terminal decision must survive failover/restore without loss, duplication, reordering or reversal.

### D. Explicit D/E/Storage owner consumption

- **D:** D's existing Phase 3.6.2 owner acceptance in `forget-fence-operation-and-publication-gate.md` is the D disposition for fence/registration/barrier ordering. D must keep an in-doubt participant inside the open barrier; fence-first rejects prepare; participant-first retains target/lineage serialization until resolution. I COMMIT never overrides D fence semantics.
- **E:** E remains non-terminal until it reads the matching durable Storage PublicationReceipt. Stable PublicationOperationId/RequestDigest survive retry/recovery; AttemptId/LeaseEpoch only fence execution attempts and cannot mint a new logical publication.
- **Storage:** Storage owns prepared-XID durability/recovery and atomic VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox commit. It must prove same-XID forward commit/rollback, retained locks, no heuristic outcome, and restore/failover behavior on the selected DB.

These are architecture-consumption requirements, not implementation evidence. Each owner must supply runtime evidence for its own boundary.

### E. Inventory and multi-domain restrictions

When policy requires InventorySeal, I must validate the current authoritative epoch, seal ID and digest inside the sequenced owner-final-gate operation. A Storage-local copy/lock does not establish currentness. Until I's inventory authority, signer/verifier, epoch/seal lifecycle and conformance are approved, missing/stale/unverifiable seal evidence remains BLOCKED/UNKNOWN.

Any operation spanning more than one I policy domain MUST be rejected or paused as BLOCKED/UNKNOWN. Independent per-domain COMMIT_WON decisions and best-effort aggregation are forbidden until I publishes and the owners consume a normative global all-or-none coordinator protocol.

### F. Conformance and closure status

JF10-01..13 plus I's added coordinator/participant/receipt/inventory/fence cases remain **SPECIFIED / NOT RUN**. Required evidence includes coordinator PREPARE and terminal log positions, participant XID traces, receipt-consumption proof, D fence/barrier trace, Storage atomic transaction proof, inventory seal version, database/runtime identity, deterministic fault injection, and independent owner review.

**Overall disposition:** single-domain architecture accepted with binding clarifications; multi-domain blocked; JF-10 P0 OPEN; implementation NOT VERIFIED; software tests NOT RUN; InventorySeal and Global Forget governance OPEN; Global Forget Completion NOT CLAIMED.
