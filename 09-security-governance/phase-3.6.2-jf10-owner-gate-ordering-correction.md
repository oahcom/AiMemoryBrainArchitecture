# Phase 3.6.2 — I Correction: JF-10 Must Join the I Policy-Domain Commit Order

- Owner: Session I — Security, Identity & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Status: **P0 PROTOCOL ACCEPTANCE BLOCKED — REQUIRED I SEMANTICS CLARIFIED**
- Supersedes: any interpretation of `phase-3.6.2-jf10-commit-authorization-recovery-acceptance.md` as acceptance of JF-10 candidate v1's split Phase-B/Phase-C protocol.
- Source evidence:
  - I policy baseline `phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`, §10.2 / I36-SR-02.
  - Current D/E/Storage JF-10 candidate, identical Blob `ff83abbad8172d4efec5a7f088064f31f21844b9`, including its I36-SR-02 gap addendum.
- This is an I-owned technical interpretation and correction. It is not external governance approval, production policy activation, implementation evidence, or D/E/Storage acceptance.

## 1. Correction and disposition

I confirms that I36-SR-02 requires the **operation owner's final commit/disclosure gate itself to participate in the same per-policy-domain commit-ordering protocol as revocation**.

The current JF-10 candidate v1 sequence:
1. I independently records a terminal `COMMIT_WON`;
2. Storage later performs an independent local VisibilityPointer transaction;

does **not**, by itself, prove that the owner final gate participated in the I sequencer order. Persisting the I decision ID/position in a later Storage transaction, or recording local receipt consumption, does not close that gap.

Therefore:
- JF-10 candidate v1 is **NOT ACCEPTED as conformant to I36-SR-02**.
- The earlier I interface addendum remains valid only for its durable identity, immutable binding, replay/conflict, authoritative lookup and evidence requirements. Its description of a prior terminal `COMMIT_WON` as sufficient input for a later independent owner commit is superseded.
- No final JF-10 cross-authority protocol is accepted by I at this time.
- JF-10 remains **P0 OPEN**; final publication remains fail-closed until a conformant protocol is jointly specified, implemented and tested.

## 2. Normative I requirement — owner final gate is the ordered operation

For every protected irreversible commit/disclosure operation, I requires:
1. The operation owner obtains a single-use, non-transferable `CommitAuthorizationReceipt` bound to the exact tuple:
   `(policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation_id, operation_payload_digest, owner_boundary, decision_id)`.
2. The owner submits that receipt to its **actual final commit/disclosure gate**, not merely to an earlier admission, prepare, or preflight check.
3. That final gate participates in the same per-policy-domain ordering protocol as I revocation.
4. The sequenced operation is the exact owner operation identified by operation ID, immutable digest and owner boundary. The sequencer outcome is not a free-standing authorization token that can be detached from the owner gate.
5. The ordering yields exactly one terminal outcome:
   - `COMMIT_WON`: the owner final commit gate was ordered before the conflicting revocation event;
   - `REVOCATION_WON`: revocation was ordered first and the owner operation cannot commit;
   - `INDETERMINATE_ABORTED`: ordering cannot safely be established; no success or visibility is permitted.
6. Receipt consumption, operation identity/digest, sequencer position and terminal ordering evidence are durably correlated and recoverable. Replay, changed digest/boundary, stale epoch, duplicate commit, unknown receipt or unresolved order is rejected/blocked.

A separate earlier I authorization decision followed by an independent owner commit is not equivalent to this requirement.

## 3. Required protocol properties — solution is for joint owner design

I does not unilaterally choose the DE-S transaction coordinator, database product, distributed transaction technology or D fence implementation. D/E/Storage must return a concrete owner-side protocol design that proves all of the following:

### 3.1 Same-order participation

- Identify the exact participants and messages by which the Storage final visibility gate joins the I per-domain sequencer order.
- Identify the single linearization point at which the owner operation is ordered against revocation.
- Prove that no Storage visibility commit can occur from a prior standalone authorization response, cached ALLOW, local receipt row, stale epoch or one-sided evidence.
- Prove that a concurrent revocation cannot be ordered between a supposedly winning I authorization result and an unprotected later owner commit.

### 3.2 Crash and recovery

The protocol must define durable states and recovery for:
- crash before the final gate joins/enters the ordering protocol;
- crash after ordering begins but before a terminal order is durable;
- crash after the terminal order is durable but before the owner visibility transaction;
- owner transaction abort/failure after a purported winning order;
- owner transaction commit with lost acknowledgement;
- I or Storage process restart, replica lag, failover and restore;
- duplicate same-key retry and changed-digest/boundary conflict;
- unavailable coordinator/participant or partition.

An irrevocable `COMMIT_WON` must not coexist with a permanently impossible owner commit. If the protocol can produce an in-doubt state, it must define durable participant state, recovery authority, retry rules and the conditions under which revocation may proceed. Safety takes precedence over availability during unresolved ordering.

### 3.3 D fence remains independent and mandatory

I's authorization order does not override D's ForgetFence. The revised protocol must specify how the D owner predicate is checked/serialized at the actual owner visibility boundary, including the race where a fence installs while the I/Storage participant protocol is in progress.

No I decision alone can prove the D predicate. A stale fence, missing barrier, incomplete dependency, expired lease or unknown D state blocks visibility. D must define whether its fence participant/order is coordinated with the same final operation protocol or how the owner transaction proves the fence cannot be bypassed.

### 3.4 Storage visibility remains sole publication authority

Only the authoritative Storage visibility transaction may make staged bytes reader-visible. It must atomically persist its local pointer, immutable PublicationReceipt, owner outcome, idempotency/receipt-consumption evidence and outbox as required by the Storage contract. I sequencer evidence and outbox delivery are not visibility.

The joint protocol must reconcile I's terminal order with Storage's durable transaction outcome without treating either side's unilateral record as sufficient proof of overall publication.

### 3.5 Multi-domain operations

If one operation spans multiple I policy domains, the I coordinator must provide an all-or-none ordering decision for the complete domain set. Partial domain success cannot authorize owner visibility. If common coordination is unavailable or membership is ambiguous, pause/deny.

## 4. Required D/E/Storage response

D/E/Storage should revise the current JF-10 candidate and provide an owner-approved response containing:

| Required item | Minimum evidence |
|---|---|
| Protocol topology | Named I sequencer role, Storage final-gate participant, D fence participant/serialization, E caller/recovery role |
| State machine | Every durable state, legal transition, terminal outcome and forbidden transition |
| Linearization | Exact point where owner commit and revocation are ordered; exact D fence check/order |
| Receipt semantics | Issue, bind, submit, consume, replay, expiry and terminal correlation |
| Atomicity | Which records share one transaction; which are coordinated across authorities; why no split-brain terminal outcome is possible |
| Crash matrix | Before/after each durable write, lost ACK, failover, replica lag, restore and partition |
| Recovery | Authoritative lookup, participant recovery, idempotency, in-doubt blocking and retention |
| Tests | Deterministic JF10-01..08 plus I36-SR-02 race tests with build/runtime/database identity and raw traces |
| Owner decisions | Explicit D, E and Storage acceptance of their own predicates and recovery responsibilities |

D/E/Storage must not mark the candidate accepted by I or JF-10 closed until I reviews the exact revised artifact Blob and explicitly records acceptance or a further blocker.

## 5. I-owned interface details retained

The following requirements from the earlier I interface addendum remain valid:
- stable `PublicationOperationId` and canonical immutable `RequestDigest`;
- same ID + same digest resolves to the same durable operation and terminal evidence;
- same ID + different digest or changed security-bound tuple is a hard conflict;
- authenticated authoritative lookup/recovery; never infer commit or non-commit from timeout, missing response or stale replica;
- receipt and terminal evidence bind policy domain, PermissionEpoch, PrincipalRef, ActorRef, action/resource, purpose/audience, Scope/Environment, delegation, operation ID/digest and exact owner boundary;
- durable audit evidence includes receipt ID, decision ID, sequencer position(s), epoch, digest, owner transaction/commit cursor and terminal outcome;
- no offline lease, stale-epoch grace or cached ALLOW is enabled by this decision.

The earlier five supplementary I tests JF10-I-09..13 remain required, and must be extended to test the final owner-gate participation protocol, not only an independent I decision endpoint.

## 6. Gate and authority status

- I36-SR-02: **NORMATIVE REQUIREMENT CONFIRMED; IMPLEMENTATION NOT VERIFIED**.
- JF-10 candidate v1: **NOT ACCEPTED / NOT CONFORMANT AS EVIDENCED**.
- Revised JF-10: **REQUESTED FROM D/E/Storage; NOT YET RECEIVED**.
- I36-GOV-01..10: **GOVERNANCE-BLOCKED**; this technical correction is not external approval.
- I36/H36/JF10 execution: **NOT RUN**.
- Global Producer Inventory Seal / Global Forget completion: **NOT EVIDENCED**.
- Fact/Claim ADR-001: **ADR-BLOCKED**, independent and unchanged.
- No deployment selection, production readiness or Phase 3.6 final acceptance is claimed.

## 7. Final disposition

I corrects its earlier JF-10 response: the required I semantics are not satisfied by a prior standalone `COMMIT_WON` followed by an independent Storage commit. The owner final gate must participate in the same per-policy-domain ordering protocol as revocation. D/E/Storage must supply a revised, recoverable protocol with D fence serialization and Storage visibility atomicity. Until I accepts that exact design and executable conformance evidence passes, JF-10 remains P0 OPEN and all publication paths remain fail-closed on ambiguity.
