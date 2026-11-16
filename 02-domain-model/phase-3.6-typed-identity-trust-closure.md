# Phase 3.6 — Typed Identity Trust Closure (B-owned semantic proposal)

- Owner: Session B — Domain Model
- Branch: `session-b-domain-model-phase3`
- Status: **CANDIDATE — B semantic proposal; not cross-module freeze or I policy approval**
- Date: 2026-11-16
- Source baseline: B Phase 3.5 Typed Reference Registry and Principal/Actor Binding Mapping; A Phase 3.5 Closure Review; I Phase 3.6 trust-chain proposal; H Phase 3.5 identity/ACK/reconnect contract; C Telemetry Event and Identity Contract; D Forget Fence contract; E Forget Fence and Derived Publication contract.
- Authority: B owns domain type meaning and reference invariants. I owns issuer trust, Principal registration, delegation, authorization, revocation and PermissionEpoch. H owns BMCP wire and authenticated transport binding. C/D/E own their semantic producer/consumer boundaries.

## 1. Normative distinctions

- **Reference**: a typed, namespaced pointer to a registered domain identity or object. It is not proof of presenter identity and grants no permission.
- **Identity Claim**: a caller/payload assertion about an identity. It remains untrusted until compared with verifier context and authoritative registries.
- **Authentication Credential**: protected authentication material validated by a verifier under an I-approved issuer/trust policy. Credentials and secrets MUST NOT be embedded in domain references.
- **Authenticated Principal**: the verifier/I-resolved security subject resulting from successful credential, issuer, audience, validity and registry checks.
- **Authenticated binding**: verifier-produced association between an authenticated Principal/session and relevant typed identities for one operation.
- **Permission**: I-owned policy result for a Principal, action, resource, audience, purpose and resolved Scope/Environment. No Ref is a permission.

Deserialization proves syntax/type only. It does not prove existence, authenticity, lifecycle validity, Scope compatibility or authorization.

## 2. Typed identity registry

| Type | Domain semantics | Unique identity / namespace | Authority and issuer relationship | Lifecycle / stability | Cross-Scope / Environment | Payload declaration and trust |
|---|---|---|---|---|---|---|
| PrincipalRef | Stable security subject (human, Agent workload, service, Adapter, recipient) | Opaque, never-recycled subject ID under IssuerRef + tenant/security-domain + principal-kind namespace | I Principal Registry owns registration/status; IssuerRef identifies credential/assertion issuer | Stable across credential rotation; Active/Disabled/Suspended/Revoked/Retired status is I-authoritative; historical ID never reassigned | No implicit alias or crossing; federation requires explicit I mapping | Payload may provide only an untrusted selector/claim; H authenticates protected transport, I validates issuer/credential/subject/status |
| IssuerRef | Identity of an authority that issued credential, assertion or signed grant | Stable opaque issuer ID under trust-domain/issuer-registry namespace | I owns local trust admission/registry; issuer controls its keys but cannot self-admit into local trust | Trusted/Suspended/Compromised/Revoked/Retired/Unknown; key rotation is a separate security event | No transitive trust or implicit federation across trust domains | Payload issuer string is a claim, never a trust anchor; verifier obtains protected issuer/key metadata and resolves through I |
| ActorRef | Immutable per-operation attribution binding an authenticated Principal and verified acting/delegation context | Operation/attribution ID namespaced by issuer + security domain; unique per operation/auth context | B owns type semantics; I validates Principal/Issuer/delegation; H supplies verifier-produced transport/session binding | Immutable historical attribution; distinct operation/session/delegation context yields distinct ActorRef; never a credential | No implicit crossing; each operation separately binds Scope/Environment and authorization | Payload ActorRef may correlate only; cannot mint/authenticate itself; verifier resolves from protected context and registries |
| AgentRef | Logical Agent identity, distinct from runtime instance and security subject | Opaque ID under Agent registry + tenant/security domain | Agent/deployment registry owns logical identity; I binds it to PrincipalRef; B defines reference semantics | Stable logical identity; instance/config/version are separate; retirement never recycles ID | Multiple Scopes only via explicit registered association and authorization; no implicit Environment crossing | Payload Agent ID is claim/selector; validate authenticated workload assignment and Agent registry binding |
| AdapterRef | Registered Adapter application identity; concrete Adapter instance is separately identified | Opaque ID under H Adapter registry + tenant/security domain; instance has separate namespace | H owns Adapter/application/instance/capability registration; I owns authenticated Adapter Principal trust and revocation | Application stable; instance, session and CapabilityEpoch independently versioned/revocable; replacement is a new instance | No implicit managed-region/Context sharing across Scope or Environment | Payload adapter ID is claim only; H authenticates instance/workload, I validates Principal and current authorization |
| ProducerRef | Registered producer/application/workload permitted to emit declared event/work families | Opaque ID under issuer + tenant/security-domain + producer namespace | I owns producer trust/registration/revocation; C declares telemetry claim semantics; E enforces ingress/work identity; D owns per-work admission ledger | Stable producer identity; workload instance, credential and registration epochs rotate independently; revocation preserves historical attribution | Registration is explicit per tenant/security domain, allowed Scope and event/work family; no string-equality reuse | Payload producer_id/producer_claim is assertion only; H authenticated workload + I registry resolution are required; D work receipt is separate |
| ScopeRef | Typed ownership or applicability/data boundary | Scope authority + tenant/security domain + scope-kind + opaque scope ID; optional exact version | B owns semantic type; I/Governance owns authoritative registry/grant policy | Stable while identity exists; status/descriptor changes are versioned; closed/revoked refs remain historical but not ordinarily usable | Cross-Scope links are not grants; cross-Environment denied by default absent explicit bridge and I authorization | Payload ScopeRef is a hint/claim; resolve authoritative registry and validate kind/owner/parent/status before I authorization |
| EnvironmentRef | Identity of authoritative world/save/simulation/device-fleet or external state domain, not a display label | Environment authority + tenant/project + environment-kind namespace | Environment registry/owner controls identity; I governs trusted binding and cross-environment policy; B defines reference semantics | Stable identity; environment revision is separate; retired identities are never reused | Cross-Environment reference denied by default; explicit mapping must bind exact source/target and permitted relation | Payload environment_id/name/coordinates are claims only; resolve via authenticated Environment Adapter or authoritative registry |
| RuntimeSessionRef | One bounded authenticated runtime/session instance used for operation correlation/binding | Opaque unique ID under issuer + runtime/Agent/Adapter instance + session namespace | H/platform session authority issues session; I policy validates trust/revocation; B defines reference semantics | Short-lived, non-reusable; Created/Active/Expired/Revoked/Closed; renewal creates a new ref | No implicit cross-Scope use; bound Principal/instance/Scope constraints must match | Payload session_id is a selector only; protected channel/session verifier is authoritative |

### 2.1 Serialization

The table defines domain semantics, not JSON/CBOR/Protobuf names or canonical wire encoding. A serialized reference MUST preserve:
- explicit type discriminator;
- stable opaque ID;
- issuer/authority and namespace/security-domain dimensions;
- optional exact version and lifecycle/registry resolution context where applicable.

A consumer MUST NOT weaken a typed Ref into an untyped string if that loses discriminator, issuer, namespace, version or trust provenance. Display labels are presentation-only. H owns wire field names/encoding.

## 3. ActorRef invariants and Principal/Actor mapping

ActorRef is not PrincipalRef and is not a bearer token, credential, grant, role or proof of current permission.

Minimum semantic components:
- resolved `principal_ref: PrincipalRef`;
- validated `issuer_ref: IssuerRef`;
- verifier-owned `authentication_context_ref` (reference only; never raw credential);
- operation/attribution identity and authenticated time;
- optional verified AgentRef, AdapterRef, ProducerRef;
- optional validated DelegationChainRef and `acting_for_ref: PrincipalRef`;
- optional authentication-strength/profile reference.

One Principal may have many ActorRefs. A given ActorRef is immutable and operation-specific. Different operation, session, delegation chain or attribution provenance requires a distinct ActorRef. A Principal may bind to Agent/Adapter/Producer identities only through explicit registry relationships; the types remain non-interchangeable.

Payload-supplied PrincipalRef, IssuerRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and RuntimeSessionRef are claims/selectors only. Mismatch with protected verifier context or authoritative registry MUST fail closed and be audited. A caller-constructed ActorRef MUST never authenticate itself.

## 4. Scope and Environment semantics

1. Ownership Scope identifies administrative custody; applicability Scope identifies where a proposition/resource is relevant or valid. Preserve both roles; never flatten them into an untyped scope ID.
2. Multiple ScopeRefs form an explicitly role-tagged set, not an access-control union.
3. A cross-Scope link is a domain relationship, not a grant. Each endpoint, Evidence and Provenance dereference is independently authorized.
4. Parent/child/sibling, same-user, same-Agent, same-project or shared-session similarity implies no inherited access.
5. Cross-Environment references are denied by default. A bridge requires a registered mapping of exact source/target EnvironmentRefs, purpose, allowed relation, provenance, validity and I authorization.
6. EnvironmentRef, Environment ScopeRef and Environment revision are distinct types.
7. Scope resolution answers “which boundary?”; I authorization answers “may this Principal perform this action now?”

## 5. Validation order (semantic requirement)

1. H/platform authenticates protected transport/session/workload.
2. I validates issuer, credential/key, audience, validity, revocation and resolves PrincipalRef.
3. Resolve AgentRef, AdapterRef, ProducerRef and RuntimeSessionRef from their registries and bind them to authenticated Principal.
4. Compare payload claims with verifier bindings; mismatch/unknown required binding fails closed.
5. Resolve ActorRef from verifier-produced operation context and validate its Principal/Issuer/delegation references.
6. Resolve ScopeRef and EnvironmentRef from authoritative registries; validate namespace, kind, lifecycle and compatibility.
7. I authorizes exact Principal + Actor + action + resource + purpose + audience + Scope/Environment + delegation.
8. Revalidate I PermissionEpoch and relevant D ForgetFence at the owning final commit/disclosure boundary.

This is a semantic ordering requirement. It does not prescribe I APIs, H envelope fields or D/E implementation.

## 6. Owner decisions and unresolved dependencies

| Item | B semantic disposition | Required authority / status |
|---|---|---|
| Distinct typed identities and no credential/permission substitution | Proposed normative B semantic rule | B Owner decision/readback required |
| ActorRef is immutable per-operation attribution, not Principal | Proposed normative B semantic rule | B Owner decision/readback required |
| Principal/Issuer registry, trust, revocation and delegation | Not B-owned | I decision; governance approvals required |
| Scope registry, grant and authorization policy | B defines type only | I/Governance policy decision |
| Environment registry authority and bridge policy | B defines type only; registry owner must be named | Environment owner + I governance; OPEN |
| Wire names/serialization/protected auth context | Not B-owned | H decision with B/I/C acceptance |
| Producer event fields and requiredness | Not B-owned | C decision with I/H/E acceptance |
| D/E canonical/compiler field migrations | Not B-owned | D/E decisions; no implicit cast |

**B Owner Decision:** CANDIDATE proposal only; no independent B approval evidence recorded in this joint session.
**I Owner Decision:** Not requested/assumed by this B document.
**H Owner Decision:** Not requested/assumed by this B document.
**Cross-module Agreement:** OPEN.
**Governance Approval:** Not applicable to B type meaning; I policy approvals remain GOVERNANCE-BLOCKED.
**Implementation Evidence:** NOT PROVIDED / NOT VERIFIED.

## 7. Fact/Claim ADR isolation

ADR-001 remains **ADR-BLOCKED**. This identity proposal does not select Fact/Claim semantics, canonical object identity, revision model, attestation authority, DDL, API or wire fields. Identity closure MUST NOT be used to clear ADR-001 or INT-P0-01.

## 8. Conformance expectations (not executed)

- forged PrincipalRef / ActorRef / ProducerRef claims never authenticate;
- same subject string under different IssuerRefs resolves to different principals absent explicit I federation;
- AgentRef/AdapterRef/ProducerRef cannot be cast to PrincipalRef;
- expired/revoked RuntimeSessionRef cannot be reused;
- ScopeRef does not grant permission;
- cross-Scope and cross-Environment access is denied absent explicit I-approved policy;
- historical ActorRef remains immutable after Principal/issuer/delegation revocation.

**Test status:** Specified at semantic level; no implementation tests executed. No PASS claim.
