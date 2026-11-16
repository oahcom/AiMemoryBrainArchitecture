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
