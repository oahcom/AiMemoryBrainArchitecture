# B Owner Addendum — Phase 3.6 BIH Joint Architecture Acceptance

- Branch: `session-b-domain-model-phase3`
- Controlling artifact: `02-domain-model/phase-3.6-typed-identity-trust-closure.md` (Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`)
- Status: **B semantic baseline jointly accepted; no domain redesign; governance and consumer gates remain open**
- Joint report: `reviews/integration/phase-3.6-identity-trust-joint-architecture.md` on A branch.

B jointly accepts BIH36-JD-01..17 as the shared delegated technical baseline, preserving B's authority over typed-reference semantics. PrincipalRef is stable and issuer/trust-domain/tenant/principal-kind/issuer-subject scoped; credentials authenticate a claim and do not define Principal. IssuerRef, PrincipalRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and RuntimeSessionRef are distinct types with no implicit casts. ActorRef is verifier-produced immutable per-operation attribution, not Principal alias, credential or grant. ProducerIdentity identifies a registered workload; ActorIdentity records operation attribution. ScopeRef represents ownership/applicability; EnvironmentRef represents execution/deployment environment. DelegationRef and PermissionEpoch remain typed and I-validated; PermissionEpoch and D ForgetFence are independent authorities.

B accepts the same JD-01..17 baseline jointly with I and H. B does not approve issuer trust, grants, revocation policy, PermissionEpoch policy, BMCP encoding, external governance or downstream consumer behavior. I remains policy authority; H remains wire/protocol authority; each consumer retains its enforcement boundary.

D/E/H/Storage design acceptance artifacts are recorded; implementation/runtime acceptance is not implied. C/F/G explicit acceptance remains OPEN. I36-01..20 and H36-01..18 plus H36-SR additions are specified, NOT RUN. Fact/Claim ADR-001 remains ADR-BLOCKED. No schema freeze is claimed.

B follow-through: keep Typed Reference Registry canonical; supply exact type/field mapping; review consumer proposals only for B-owned semantics. Do not sign for I or consumer Owners.
