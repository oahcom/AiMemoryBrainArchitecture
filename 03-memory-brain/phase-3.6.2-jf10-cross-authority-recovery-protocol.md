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
