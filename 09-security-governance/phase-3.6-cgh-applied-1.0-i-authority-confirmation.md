# I Owner Authority Confirmation — CGH-APPLIED-1.0

- Owner: Session I — Identity, Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Decision: **APPROVE WITH ENUMERATED EXCEPTIONS — I-OWNED AUTHORIZATION SEMANTICS ONLY**
- Common contract: `CGH-APPLIED-1.0`
- Exact A decision package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`
- Controlling I confirmation: `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md`, Blob `bae6a24fe3a374bc816993979a8fa9af52517dea`
- Related I policy baseline: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`

## 1. Decision

I confirms the I-owned authorization and revocation predicates consumed by CGH-APPLIED-1.0. The confirmation is limited to I authority and does not approve C's producer evidence, G's Applied predicate or commit implementation, H's wire encoding, D's ForgetFence semantics, or B's type definitions.

I approves the package's requirement that a Full Applied decision cannot rely on a payload-supplied identity or stale/cached authorization result. At the exact protected submission boundary, the consumer must bind and validate the complete I authorization tuple and authoritative current PermissionEpoch in the applicable I-registered PolicyDomain.

## 2. Normative I confirmation

1. **Issuer and authority:** I is the sole logical authority for PermissionEpoch, policy-domain registration, issuer/principal/delegation trust, authorization decisions and revocation ordering.
2. **Typed authorization tuple:** the protected decision binds IssuerRef, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, applicable EnvironmentRef, DelegationChainRef, PolicyDomainRef, PermissionEpoch, authenticated workload/instance and RuntimeSessionRef.
3. **Currentness:** PermissionEpoch is opaque, monotonically advancing only within its registered PolicyDomain. The owner obtains authoritative online currentness at the protected boundary. Stale, gapped, unknown, incomparable, unverifiable or indeterminate state means DENY/PAUSE, never ALLOW.
4. **No offline grace:** cached ALLOW, event delivery, local high-water marks or offline leases do not establish currentness in this Phase 3.6 profile.
5. **Revocation ordering:** revocation is effective at the durable committed epoch-advance point in the I policy-domain sequencer. The exact owner-final-gate receipt must enter the same sequencer. COMMIT_WON, REVOCATION_WON and UNKNOWN/IN_DOUBT are distinct terminal/indeterminate outcomes; uncertainty never promotes Full Applied.
6. **Receipt binding:** an irreversible protected operation uses a single-use CommitAuthorizationReceipt bound to the policy domain/epoch, complete identity and authorization tuple, operation ID, immutable request/payload digest and exact owner boundary. A detached preflight ALLOW is insufficient.
7. **Independent D authority:** PermissionEpoch and D ForgetFenceGeneration are independent namespaces and independent final-boundary checks. Neither can replace or order the other absent an explicit shared causal/serialization proof.
8. **Historical versus current-use:** I authorization at submission determines whether the historical submission boundary was authorized. A later epoch advance cannot rewrite a terminal I decision already durably sequenced first, but it invalidates authorization for later operations. G remains sole authority for recording Applied history and computing its current-use projection.

## 3. Enumerated exceptions and limits

1. This is an I technical authority confirmation, **not** external governance approval or policy activation. I36-GOV-01..10 and the named approver evidence remain GOVERNANCE-BLOCKED.
2. I does not approve H's concrete signature/MAC suite, key custody/rotation/compromise profile or production cryptographic activation. Those require the designated Security/Governance review.
3. This confirmation does not establish that C's final-submit evidence is complete, immutable, cryptographically valid or observable at every adapter tier. C owns that evidence.
4. This confirmation does not supply a cross-authority causal proof between C's actual submit event and D's ForgetFence order. If the required common sequencer/receipt evidence cannot establish order, the result is UNKNOWN and Full Applied must not be promoted.
5. This confirmation does not approve H wire field paths or serialization. H owns those; its `bmcp.applied-ack/1.0.0` remains an owner-decided schema candidate, not deployed interoperability.
6. I service deployment, durable sequencer HA, consumer integration and I36/H36/CGH conformance remain NOT VERIFIED / NOT RUN.

## 4. Exact CGH-APPLIED-1.0 disposition

- I PermissionEpoch authority/currentness predicates: **CONFIRMED**.
- I complete authorization tuple and default-deny semantics: **CONFIRMED**.
- I revocation effective point and commit-versus-revocation ordering semantics: **CONFIRMED**.
- I/D independent authority namespaces: **CONFIRMED**.
- External governance approval: **BLOCKED**.
- Cross-authority C-submit/D-fence causal proof: **NOT ESTABLISHED BY THIS ARTIFACT**.
- Production implementation and conformance: **NOT VERIFIED / NOT RUN**.

This decision is pinned to the exact A package Blob above. It is not approval of another package revision unless the changed revision is reviewed explicitly.
