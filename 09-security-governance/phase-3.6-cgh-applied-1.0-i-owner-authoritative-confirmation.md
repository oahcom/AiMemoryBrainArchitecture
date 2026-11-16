# Phase 3.6 — I Owner Authoritative Confirmation for CGH-APPLIED-1.0

- Owner: Session I — Identity, Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Date: 2026-11-16
- Exact A package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact A package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`
- Common contract: **CGH-APPLIED-1.0**
- H schema reviewed: `bmcp.applied-ack / 1.0.0`, protocol major 1/minor 0, as recorded in H artifact Blob `1ea5dccdf2d965103b1a8474b79f00810f639187`
- I controlling authorization baseline: `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md`, Blob `bae6a24fe3a374bc816993979a8fa9af52517dea`
- I controlling policy baseline: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`
- Decision class: **FORMAL I OWNER AUTHORITY / CONSUMER-CONTRACT CONFIRMATION**
- Decision: **APPROVE WITH ENUMERATED I-OWNED EXCEPTIONS**
- Scope: I authorization, issuer/principal trust, PermissionDecision/PermissionEpoch currentness, revocation ordering, and I authorization evidence consumed at C/G/H Applied boundaries.
- Non-scope: C final-request evidence semantics, G Applied predicate/commit, H wire encoding/transport implementation, D ForgetFence/lineage, B reference semantics, Storage visibility, external governance approval, and runtime conformance.

## 1. Exact-version decision

I has reviewed the exact A package Blob SHA `122b164bcc0760b83bf555072a36fc55631623e1` and the H-owned `bmcp.applied-ack / 1.0.0` schema candidate identified above.

**I APPROVES CGH-APPLIED-1.0 WITH ENUMERATED I-OWNED EXCEPTIONS** for the I authorization predicates and consumer obligations in this artifact.

This is an affirmative, exact-version I Owner decision. It is not merely a generic statement that I's pre-existing PermissionEpoch baseline is compatible. It is not approval of the complete C/G/H wire contract, and it does not transfer I's policy authority to C, G or H.

## 2. Confirmed I authority and semantics

The following are normative I-owned requirements for any Full Applied eligibility claim and any protected final-request submission/disclosure boundary:

1. **Issuer and Principal trust.** IssuerRef and PrincipalRef must resolve through I's authoritative trust/identity registry and be valid for the exact tenant/security domain, workload and operation. Payload claims, adapter-provided identity fields, display labels and unverified aliases do not establish trust.
2. **Actor attribution.** ActorRef must be verifier-resolved and bound to the authenticated PrincipalRef, IssuerRef, workload/Agent/Adapter/runtime instance and exact operation/session. ActorRef is not a credential, grant or reusable capability. B owns its domain type semantics; I owns trust and attribution policy.
3. **Policy domain.** I resolves the canonical immutable PolicyDomainRef from its registry. Consumers may not infer or synthesize a policy domain from labels, ScopeRef, EnvironmentRef, tenant strings or arbitrary concatenation.
4. **PermissionEpoch.** I alone issues and advances the monotonic PermissionEpoch for a registered PolicyDomainRef. The epoch is opaque and domain-scoped. It is not comparable with or substitutable for D ForgetFenceGeneration, G ContextVersion, H CapabilityEpoch, DeliveryAttemptId or RuntimeSessionRef.
5. **Currentness.** A cached PermissionDecision is usable only after authoritative online proof that its PermissionEpoch remains current and all bound tuple members still match. No offline authorization lease, cached-ALLOW grace or stale-epoch grace is permitted in this Phase 3.6 baseline. If currentness cannot be established, deny/pause and keep protected content suppressed.
6. **Complete authorization tuple.** The authorization decision is bound to IssuerRef, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, EnvironmentRef where applicable, DelegationChainRef, PolicyDomainRef, PermissionEpoch, authenticated workload/instance and RuntimeSessionRef. Missing, ambiguous, cross-domain or mismatched tuple members fail closed.
7. **Final boundary.** The owner that performs the protected disclosure/submission must enforce current I authorization at its actual final boundary. An upstream ALLOW, transport ACK, H receiver receipt, C evidence record or G Applied record is not a transferable blanket permission.
8. **Revocation ordering.** Revocation becomes effective at I's policy-domain sequencer's durable committed epoch-advance point. Request arrival, wall-clock timestamp, local cache invalidation or eventual event delivery is not the effective point.
9. **Race result.** The exact protected operation must be ordered against revocation at the owner-final-gate. If the operation's exact commit is sequenced first, its historical terminal outcome may be COMMIT_WON; if revocation is sequenced first, it is REVOCATION_WON and the operation is rejected; if order cannot be proven, the result is INDETERMINATE_ABORTED/UNKNOWN and no success or Full Applied promotion may be asserted.
10. **Later use.** A historically valid pre-revocation submission does not authorize later operations or continued current use. G may preserve a historical Applied fact only under its own predicate and trusted causal proof; current-use eligibility must be recomputed against current I authorization and all other owner predicates.

## 3. Required I evidence at the C final-request boundary

The A package's semantic fields `PermissionDecisionRef` and `PermissionEpoch` are necessary but are not, by themselves, proof that the exact final submission was authorized at the linearization point.

For an operation/policy classified as protected irreversible disclosure, the final owner boundary MUST obtain and consume a single-use I `CommitAuthorizationReceipt` bound to:

`(PolicyDomainRef, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation_id, operation_payload_digest, owner_boundary, decision_id)`.

The receipt MUST be consumed by the exact owner-final-gate, not by a detached preflight. The durable evidence record MUST bind:
- I decision ID and CommitAuthorizationReceipt ID;
- PolicyDomainRef and PermissionEpoch;
- exact operation ID, immutable final-request digest and owner boundary;
- authenticated PrincipalRef/ActorRef and applicable Scope/Environment binding digest;
- I sequencer position and terminal outcome COMMIT_WON, REVOCATION_WON or INDETERMINATE_ABORTED;
- C FinalRequestBoundaryId and InferenceRequestId correlation, without allowing either identifier to be invented or reassigned by H.

Same operation ID + same digest + same boundary returns the same durable disposition. Same ID with changed digest, boundary, participant or security-bound tuple is a hard conflict. Receipt replay or second consumption is rejected.

**Schema/compatibility exception I-EX-01:** the current H `bmcp.applied-ack / 1.0.0` message registry carries PermissionDecision references and PermissionEpoch but does not explicitly define a CommitAuthorizationReceipt reference plus I sequencer-position/terminal-outcome evidence field for this protected final-boundary proof. H must not synthesize or validate these I values. C and the actual final-boundary owner must durably retain the I receipt and ordering proof; H may transport opaque references/evidence digests only after H and C agree the exact versioned mapping. Until that mapping is added and owner-accepted, the wire profile is a schema candidate and no consumer may claim the wire ACK itself proves I authorization.

## 4. H 1.0.0 profile: I disposition

I confirms the following H profile properties as compatible with I authority, subject to the conditions below:

- `PermissionDecisionRef` / `PermissionEpoch` remain I-issued opaque references/values; H transports them without minting, interpreting policy, refreshing, extending or substituting them.
- Protected verifier context, authenticated issuer/principal, verifier-resolved ActorRef, authenticated workload/Adapter/runtime/session and audience binding must be established by the trusted authentication boundary. Payload mirrors cannot override them.
- TLS 1.3 exporter channel binding, message digest, nonce/replay window, canonicalization identifiers, audience and RuntimeSessionRef binding are acceptable protocol mechanisms in principle.
- H receiver sequence is transport-ingress evidence only. I orders authorization/revocation using its own authoritative sequencer; a receiver sequence or sender timestamp cannot replace the I sequencer position.
- H `DURABLY_RECORDED` means only H receiver durability. It is not I authorization, C final submission, G Applied, D Forget completion or Storage visibility.
- `APPLIED_ACK`, `FORGET_ACTION_ACK`, `FINAL_REQUEST_SUBMISSION_EVIDENCE` and transport `ACK_RECEIPT` remain distinct evidence families. H cannot convert one family into another.

**I-EX-02 — cryptographic profile.** H's use of TLS 1.3 exporter channel binding and SHA-256 canonical message digests is acceptable as a protocol design baseline. The exact signature/MAC suite, key custody, issuer key admission, signing authority, rotation/overlap, compromise response, revocation distribution and trust-domain federation are not approved by this I decision. They remain subject to named I/Security governance approval of an exact policy/profile hash before production activation.

**I-EX-03 — schema evolution.** H owns field spelling, encoding, versioning and BMCP protocol compatibility. I does not freeze H's wire schema. Any addition needed for I receipt/ordering evidence must be versioned, requiredness-profiled and explicitly reconciled by H and the consuming owner. Unknown or missing security-critical fields fail closed; no silent downgrade or fallback is allowed.

## 5. Policy-domain and temporal limits

- A single-policy-domain operation may proceed only when all authorization inputs are current and the exact owner-final-gate ordering can be durably established.
- A multi-policy-domain Applied submission or protected operation is **BLOCKED / UNKNOWN** unless I's all-or-none multi-domain coordinator protocol is separately specified, approved and proven. Independent per-domain ALLOWs or COMMIT_WON results are not an atomic aggregate.
- If an unresolved earlier prepared participant exists under the applicable I ordering protocol, a conflicting revocation cannot pass it by assuming abort. The operation remains UNKNOWN/IN_DOUBT until authoritative recovery resolves it.
- Wall-clock timestamps, C event times, H receiver times, Adapter `observed_at`, G append times and D fence times are not interchangeable causal order. The owning sequencer/approved cross-owner proof is required.
- If I currentness or revocation order is missing, stale, incomparable or unverifiable, the outcome is deny/pause/UNKNOWN; G must not promote Full Applied and protected memory remains suppressed.

## 6. Explicit I exceptions and non-approvals

| ID | Exception / retained gate | Required closure |
|---|---|---|
| I-EX-01 | Current H 1.0.0 profile does not explicitly carry the I CommitAuthorizationReceipt and I sequencer terminal-order evidence needed to prove a protected final-boundary operation | C + H define exact versioned opaque reference/evidence mapping; I reviews only I-owned semantics; consuming owner persists the authoritative receipt and outcome |
| I-EX-02 | Exact signature/MAC suite, key custody, rotation, compromise and federation profile not approved | Named I/Security governance approval for exact profile/hash |
| I-EX-03 | H wire schema and operation-requiredness registry remain H-owned candidate; I does not freeze wire encoding | H publishes/reconciles versioned schema and requiredness; consumer acceptance and conformance |
| I-EX-04 | I36-GOV-01..10 external governance approvals remain GOVERNANCE-BLOCKED | Named authorized approvers and auditable approvals; no inferred approver/signature |
| I-EX-05 | ProducerDomainInventoryEpoch / InventorySeal authority and lifecycle remain CANDIDATE / OPEN where required by effective policy | I registry/governance authority and exact inventory seal lifecycle approval |
| I-EX-06 | Multi-policy-domain atomic authorization remains BLOCKED / NOT ACCEPTED | Separate normative I coordinator protocol, owner acceptance and conformance |
| I-EX-07 | D ForgetFenceGeneration, lineage coverage, D barrier and cross-authority causal order remain D-owned and are not approved by I | D exact-version decision and executable D/Storage/consumer proof |
| I-EX-08 | Runtime I36/H36/CGH conformance and implementation remain NOT VERIFIED / NOT RUN | Reproducible executable tests, raw logs, build/runtime identity and independent owner review |

I's exact-version approval does not grant an external governance approval, activate a production policy, approve any named issuer/key, waive a required InventorySeal, or close JF-10/Global Forget.

## 7. Owner authority boundaries

- **I:** issuer trust, Principal registration/linking, Actor attribution trust, authorization policy, PolicyDomainRef, PermissionDecision, PermissionEpoch, CommitAuthorizationReceipt, revocation ordering, I registry and I governance approvals.
- **B:** semantic types and namespace/reference invariants for ActorRef, ScopeRef and EnvironmentRef. I does not redefine these types.
- **C:** final immutable request, InferenceRequestId, FinalRequestBoundaryId, actual successful submit boundary, request digest and producer evidence. C/final-boundary owner enforces I authorization there.
- **G:** sole authority for ContextVersion/Delivery target and Applied predicate, Applied commit/idempotency, historical Applied and current-use projection.
- **H:** BMCP envelope, schema, field encoding, transport integrity, ACK receipt, capability negotiation, Adapter instance and reconnect mechanics. H transports I evidence but does not decide authorization.
- **D:** ForgetFenceGeneration, ForgetOperation, lineage, registration/barrier and Forget ordering.
- **Storage:** durable owner transaction and visibility/publication boundary where applicable.
- **A:** records exact Owner decisions and evidence only; no authority is inferred from integration synthesis.

## 8. Conformance and verification status

The following remain **SPECIFIED / NOT RUN** or **NOT VERIFIED**:
- I36 epoch/currentness/revocation races and receipt single-consumption/replay tests;
- H36 channel binding, nonce/replay, key rotation, ACK ordering and reconnect tests;
- CGH-01..20 historical/current-use and cross-owner evidence tests;
- multi-domain coordinator cases (blocked pending protocol specification);
- production key lifecycle, registry/seal, failover, restore and audit evidence.

No test PASS, production security certification, deployed interoperability, implementation verification, Global Forget completion or physical erasure is claimed.

## 9. Final I disposition

- Exact A package Blob `122b164bcc0760b83bf555072a36fc55631623e1`: **I APPROVES WITH ENUMERATED I-OWNED EXCEPTIONS**.
- CGH-APPLIED-1.0 I authorization/currentness/revocation semantics: **I OWNER CONFIRMED**.
- H `bmcp.applied-ack / 1.0.0`: **I ACCEPTS I-OWNED SEMANTIC CONSUMPTION WITH EXCEPTIONS; NOT A PRODUCTION CRYPTO APPROVAL OR WIRE FREEZE**.
- Protected final-boundary I receipt and sequencer proof: **MANDATORY; exact wire mapping remains OPEN under I-EX-01**.
- D ForgetFence/lineage/order: **NOT APPROVED BY I; D OWNER DECISION REQUIRED**.
- I36-GOV-01..10: **GOVERNANCE-BLOCKED**.
- Multi-policy-domain atomicity: **BLOCKED / NOT ACCEPTED**.
- Tests: **SPECIFIED / NOT RUN**.
- Implementation: **NOT VERIFIED**.
- Applied Contract Frozen: **NO**.

This decision is binding for I-owned technical authorization semantics within CGH-APPLIED-1.0. It does not modify the exact A package, rewrite another Owner's contract, authorize a branch merge, or close Issue #3.
