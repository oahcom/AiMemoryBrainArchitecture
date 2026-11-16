# B Owner Authority Confirmation — CGH-APPLIED-1.0 Typed References

- Owner: Session B — Domain Model
- Branch: `session-b-domain-model-phase3`
- Decision: **APPROVE — B-OWNED SEMANTIC TYPES AND ROLE MAPPING ONLY**
- Common contract: `CGH-APPLIED-1.0`
- Exact A decision package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`
- Controlling B formal confirmation: `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md`, Blob `729a706860b1259115816265e847a29683c3c233`

## 1. Decision

B approves the B-owned ActorRef, ScopeRef and EnvironmentRef semantic types and role-preserving mapping as consumed by CGH-APPLIED-1.0. No semantic type substitution is required. This is an exact-package confirmation of the B-owned semantic portion only.

## 2. Normative B confirmation

1. **ActorRef** is immutable, verifier-produced, per-operation attribution bound to authenticated PrincipalRef, IssuerRef, verifier-owned authentication context and the exact operation/session. It is not PrincipalRef, credential, ProducerRef, AgentRef, AdapterRef, permission, bearer token or reusable capability.
2. **ScopeRef** is a stable typed ownership/applicability boundary, not permission or grant. Ownership, applicability, source, target and evidence/provenance roles remain explicit and role-labelled. A generic unqualified ScopeRef cannot replace multiple semantically distinct bindings.
3. **EnvironmentRef** is a stable typed external execution/state-domain identity. It is orthogonal to ScopeRef and Environment ScopeRef, environment revision, policy domain and display labels. Where both environment identity and environment-scoped data boundary are required, both typed references must be represented.
4. Payload strings, labels, URLs, coordinates or legacy `environment_id` / `environment_scope_id` values are selectors/claims only. They require authoritative registry resolution and explicit consumer-owned schema mapping; no silent cast is allowed.
5. Cross-Scope access defaults to deny and requires I authorization. Cross-Environment access defaults to deny and requires an exact registered bridge plus I authorization. Typed identity alone is not permission.
6. ActorRef, ScopeRef and EnvironmentRef must not be coerced into PrincipalRef, ProducerRef, AgentRef, AdapterRef, PermissionEpoch, CapabilityEpoch, ForgetFenceGeneration or one another.

## 3. Enumerated authority boundary

B's approval does not freeze:
- H's BMCP wire field names, encoding, requiredness, signature/MAC or canonicalization profile;
- C/G/H consumer field paths or exact producer/Applied schema implementation;
- I issuer trust, authorization, delegation, grants, PermissionEpoch or governance activation;
- D/E/Storage internal persistence schema or migration;
- Environment Registry or Scope Registry authority designation and lifecycle;
- production conformance, test execution or Fact/Claim ADR-001.

Consumer owners remain responsible for exact field paths and runtime validation. B's semantic approval cannot be used as proof that a raw string has been resolved into a trusted typed reference.

## 4. Exact CGH-APPLIED-1.0 disposition

- ActorRef semantic meaning: **B CONFIRMED**.
- ScopeRef semantic meaning and role distinctions: **B CONFIRMED**.
- EnvironmentRef semantic meaning and orthogonality: **B CONFIRMED**.
- Consumer field-path and wire encoding freeze: **NOT APPROVED BY B**.
- Registry authority designation: **OPEN**.
- Runtime conformance and tests: **NOT VERIFIED / NOT RUN**.

This decision is pinned to the exact A package Blob above. It is not approval of another package revision unless the changed revision is reviewed explicitly.
