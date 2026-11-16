# I Owner Contract Addendum — CommitAuthorizationReceipt and Cross-Authority Causal Ordering

- Owner: Session I — Identity, Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Target profile: `CausalOrderProfile/1.0`
- Target H schema: `bmcp.applied-ack/1.1.0`
- Target common package: `CGH-APPLIED-1.1` (proposed successor; not cross-owner frozen)
- Status: **I-SIDE RECEIPT/ORDERING CONTRACT SPECIFIED; service deployment, external governance and cross-owner acceptance OPEN**.

## 1. I remains the authorization authority

I alone resolves issuer/principal/delegation trust, PolicyDomainRef, authorization decision, PermissionEpoch and revocation effective point. The coordinator is an ordering mechanism only: it MUST NOT mint, advance, interpret or override I authorization or PermissionEpoch.

## 2. CommitAuthorizationReceipt contract

I issues an opaque, signed, single-use CommitAuthorizationReceipt only after online validation of the complete tuple:
IssuerRef, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, applicable EnvironmentRef, DelegationChainRef, PolicyDomainRef, PermissionEpoch, authenticated workload/instance, RuntimeSessionRef,  CausalOrderTransactionRef, pre-submit ParticipantIntentRef, FinalRequestBoundaryId and immutable request digest.

Receipt MUST bind:
- unique ReceiptRef and I issuer/key epoch;
- exact operation/action/resource/purpose/audience;
- complete typed identity and scope/environment/delegation tuple;
- PolicyDomainRef and PermissionEpoch;
- CausalOrderTransactionRef and ParticipantIntentRef (the coordinator's durable pre-side-effect intent);
- FinalRequestBoundaryId and exact request digest;
- expiry/consumption rules that never turn timeout into successful authorization;
- replay-protected single-use state.

A generic PermissionDecisionRef, cached ALLOW, epoch value or unconsumed receipt is not a commit authorization.

## 3. I sequencer terminal evidence

I consumes the receipt exactly once in its authoritative PolicyDomain sequencer and emits IAuthorizationTerminalRef, binding:
- ReceiptRef, transaction/reservation refs, exact request digest and authorization tuple digest;
- PermissionEpoch and PolicyDomainRef;
- I sequencer identity/epoch and durable terminal position;
- terminal outcome COMMIT_WON, REVOCATION_WON or UNKNOWN/IN_DOUBT;
- signed immutable evidence digest.

Revocation remains effective at I's durable committed epoch-advance point. A revocation request that arrives while a pre-existing reserved participant is unresolved is recorded as pending; I MUST NOT claim its effective epoch-advance point has passed that participant until the participant is committed or safely aborted under the common coordinator protocol. This preserves I's own sequencer semantics while making the cross-authority ordering explicit.

If I cannot establish currentness or the terminal order, deny/pause and return UNKNOWN/IN_DOUBT. Never issue a favorable terminal proof from wall-clock or receiver sequence.

## 3.1 Revocation request ordering and admission cutoff

Every revocation request that can affect this protected operation MUST first be durably recorded with the common coordinator and carry an immutable IRevocationRequestRef plus coordinator request position. I remains the only authority that commits the effective PermissionEpoch advance in its own policy-domain sequencer; the coordinator position establishes only the cross-authority causal cutoff.

- Revocation request position before ParticipantIntentRef: no new intent/receipt may be admitted for the affected policy domain and operation; the request is REVOCATION_WON for that candidate.
- ParticipantIntentRef before revocation request but before receipt consumption: I may order revocation first in its own sequencer; receipt consumption returns REVOCATION_WON and C safely aborts.
- Receipt consumption terminalized COMMIT_WON before revocation request: I immediately blocks new receipts/authorizations in the affected domain, records the revocation as pending, and does not commit its effective epoch advance past the unresolved participant until C's exact submit outcome or safe abort is terminal.
- Unknown provider outcome keeps the revocation pending and the participant unresolved. No timeout or coordinator outage may silently clear it.

IAuthorizationTerminalRef binds the applicable IRevocationRequestRef/cutoff position (or explicitly states that no earlier revocation request existed at the terminalization point), the I sequencer terminal position and ParticipantIntentRef. The coordinator cannot choose the I effective point.

## 4. Cross-authority protocol obligations

- I validates the coordinator's registered identity/profile and verifies ParticipantIntentRef is durable and bound to the exact transaction/digest.
- I signs its own authorization terminal evidence and sends the immutable ref to the coordinator/C. Coordinator positions are correlation/order evidence, not I authority.
- I does not accept D's fence generation as a substitute for PermissionEpoch and does not accept C/H claims as proof of authorization.
- I revocation requested before receipt consumption may win and force safe abort. Once I terminalizes receipt consumption as COMMIT_WON, later revocation effectiveness MUST wait behind that unresolved ParticipantIntentRef until C's provider outcome is terminal. Unknown provider outcomes keep the participant unresolved until authoritative reconciliation.
- A terminal submit ordered before revocation remains historical only; it does not authorize later operations or current use.

## 5. Failure and security rules

Receipt replay, changed digest, wrong transaction, wrong boundary, wrong principal/actor/session, stale epoch, untrusted coordinator, missing lineage participant binding, contradictory terminal evidence or coordinator rollback => reject/quarantine and emit security event. Coordinator outage => no new protected submit and no false revocation-complete claim. No offline grace or cached ALLOW.

## 6. I conformance

Add I-CO-01..10: single-use exact binding; replay; stale epoch; revocation before receipt consumption; pending revocation behind registered participant; submit success then later revocation; unknown provider outcome; coordinator failover/rollback; contradictory terminal evidence; coordinator identity/key compromise.

Status: **SPECIFIED / NOT RUN**. I36-GOV-01..10 remain external GOVERNANCE-BLOCKED; this document does not approve cryptographic suite/key custody or production activation.

## 7. Acceptance boundary

This artifact specifies I's required receipt and sequencer behavior. It does not establish deployment of the common coordinator, D fence implementation, C provider integration, H serialization acceptance or G Applied state. Exact cross-owner acceptance of `CausalOrderProfile/1.0` and `bmcp.applied-ack/1.1.0` remains required before `CGH-APPLIED-1.1` can be frozen.

## I Owner exact-version decision — CGH-APPLIED-1.1

- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA: `9808b31f840606b329f1a794935dfc9c5084d63b`
- Common contract: `CGH-APPLIED-1.1`
- Causal profile: `CausalOrderProfile/1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within I's authority over issuer/principal trust, authorization, single-use CommitAuthorizationReceipt, PermissionEpoch and revocation sequencing.

I accepts the exact package's ParticipantIntent-bound, single-use CommitAuthorizationReceipt and authoritative consumption/terminalization. I accepts IAuthorizationTerminalRef binding the applicable IRevocationRequestRef and its request/cutoff position, or an explicit assertion that no earlier revocation request existed. A revocation request before intent blocks admission; after intent but before receipt consumption may win (REVOCATION_WON); after COMMIT_WON it remains pending behind that unresolved participant until safe terminal outcome. COMMIT_WON proves only the I owner gate ordering, never provider success.

Exceptions and closure conditions:
1. I receipt issuance/consumption service and sequencer deployment, durable reservation correlation and recovery are not verified. Acceptance is conditional on durable single-use consumption and monotonic revocation state across crash/failover/restore.
2. The same durable participant transaction must be reconciled with D's fence barrier and C's provider outcome. No local timestamp, cached ALLOW, H receiver sequence or coordinator-only position substitutes for I's authoritative terminal evidence.
3. Unknown provider outcome retains the participant and pending revocation; no automatic expiry, heuristic abort or retry-as-new-operation is permitted.
4. Exact H signature/MAC suite, key custody/rotation/compromise and federation require separate I/Security governance approval before production activation. External I36-GOV approvals remain separately BLOCKED unless independently evidenced.
5. Multi-PolicyDomain/all-or-none authorization remains BLOCKED unless I approves a complete domain-set protocol. I-CO and I36 conformance remain NOT RUN; production implementation NOT VERIFIED.

This decision applies only to the exact A Blob above. It does not approve D authority, H deployment, G Applied, external governance, or transfer any 1.0 approval.
