# Phase 3.6 — Typed Identity Trust Closure (B-owned semantic proposal)

- Owner: Session B — Domain Model
- Branch: `session-b-domain-model-phase3`
- Status: **JOINT-DECIDED technical baseline; cross-owner acceptance and implementation verification remain open**
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
| Distinct typed identities and no credential/permission substitution | JOINT-DECIDED normative B semantic rule | Delegated joint decision recorded in Section 9 |
| ActorRef is immutable per-operation attribution, not Principal | JOINT-DECIDED normative B semantic rule | Delegated joint decision recorded in Section 9 |
| Principal/Issuer registry, trust, revocation and delegation | Not B-owned | I decision; governance approvals required |
| Scope registry, grant and authorization policy | B defines type only | I/Governance policy decision |
| Environment registry authority and bridge policy | B defines type only; unresolved registry authority means cross-environment operations unavailable/denied | Project must designate registry authority; until then fail closed |
| Wire names/serialization/protected auth context | Not B-owned | H decision with B/I/C acceptance |
| Producer event fields and requiredness | Not B-owned | C decision with I/H/E acceptance |
| D/E canonical/compiler field migrations | Not B-owned | D/E decisions; no implicit cast |

**B Owner Decision (current):** Phase 3.6 domain semantics technically DECIDED under delegated joint authority; no separate B-session signature is claimed.
**I Owner Decision:** Not requested/assumed by this B document.
**H Owner Decision:** Not requested/assumed by this B document.
**Cross-module Agreement (current):** BIH Phase 3.6 technical design DECIDED under delegated joint authority; downstream consumer acceptance remains OPEN.
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

## 9. BIH Joint Decision Adoption — B semantic contract

- Joint decision authority: delegated by the project user to the Joint Decision Architect for this execution.
- B semantic status: **JOINT-DECIDED technical baseline**. This is not a claim of a separate B-session signature.

### 9.1 Binding decisions

| ID | Joint decision | Authority | Required behavior |
|---|---|---|---|
| BIH36-JD-01 | PrincipalRef, IssuerRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and RuntimeSessionRef remain distinct typed identities. No implicit casts or credential/permission substitution. | B semantics; I/H consume | Preserve type discriminator, issuer/authority namespace and security-domain dimensions. |
| BIH36-JD-02 | A Ref is a selector/reference, never proof of identity, registration, authentication or permission. Payload identity fields are claims only. | B semantics; I trust; H transport | Deserialization and message integrity cannot promote a claim to authenticated identity. |
| BIH36-JD-03 | Principal resolution is issuer-scoped by validated IssuerRef, trust/security domain, tenant namespace, principal kind and issuer subject. PrincipalRef is stable and never recycled; credential rotation does not change it. | I registry; B type semantics | No subject-only global lookup, payload-driven auto-registration or ambiguous resolution. |
| BIH36-JD-04 | Issuer trust is explicit, locally admitted and non-transitive. Trust-on-first-use is disabled. Unknown, suspended, compromised, revoked or unverifiable issuer/key fails closed. | I | No payload-driven trust bootstrap or transitive trust inference. |
| BIH36-JD-05 | ActorRef is immutable, verifier-produced, per-operation attribution binding resolved Principal, issuer, operation/session and validated delegation/acting-for context. It is not a credential, grant or reusable Principal alias. | B semantics; I validation; H binding | Caller-minted ActorRef is rejected; materially different operation/session/delegation attribution gets a distinct ActorRef. |
| BIH36-JD-06 | AgentRef, AdapterRef and ProducerRef are separate registered workload/application identities. Their binding to PrincipalRef comes only from protected verifier context and authoritative registries. | B types; I Principal/Producer trust; H Adapter registry | Unknown, revoked, replaced or mismatched workload bindings are rejected/quarantined. |
| BIH36-JD-07 | Delegation authority is the strict intersection of grantor authority, delegate eligibility and every parent grant. No amplification, cycles or represented-Principal fallback. Sub-delegation is disabled by default until an approved profile enables it. | I | Any chain requiring unapproved sub-delegation is denied; grant binds issuer, parties, actions, resources, exact boundaries, audience, purpose, validity and revocation. |
| BIH36-JD-08 | Scope ownership and applicability roles remain distinct. Hierarchy, shared Agent, project, tenant label or session similarity never grants access. Cross-Scope access requires an explicit current grant naming exact source/target scopes and action/resource/purpose/audience. | B role semantics; I authorization | Each endpoint and Evidence/Provenance dereference is independently authorized. |
| BIH36-JD-09 | Cross-Environment access is denied by default. A bridge resolves exact source/target EnvironmentRefs and binds permitted relation/action/resource, purpose, provenance, validity and explicit I authorization. | B type semantics; Environment registry owner; I | No display-label, coordinate, same-project or same-user fallback. |
| BIH36-JD-10 | Every protected operation authorizes the complete tuple: PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, applicable EnvironmentRef, DelegationChainRef, policy domain and PermissionEpoch, plus authenticated workload/session bindings and owner-local fences. | I policy; operation owner enforcement | Missing, unresolved, mismatched or indeterminate required member means DENY/PAUSE; upstream ALLOW is not a blanket capability. |
| BIH36-JD-11 | PermissionEpoch is an opaque, monotonically advancing token within an explicit I-owned policy domain. Cross-domain epochs are incomparable. I is sole logical authority; consumers validate currentness at their own protected boundary and at irreversible commit/disclosure when required. | I | Stale, gapped, unknown, incomparable or unverifiable epoch blocks the operation. |
| BIH36-JD-12 | No offline/stale authorization lease is usable in this baseline. A bounded non-transferable lease requires a separately approved I governance profile specifying audience, resource/action/scope binding, maximum staleness, expiry and revocation behavior. | I + Governance | Until approved, inability to establish authoritative currentness fails closed. |
| BIH36-JD-13 | PermissionEpoch and D ForgetFenceGeneration/ForgetFence are independent typed namespaces with independent authorities and checks. They are never compared, converted or substituted. | I for PermissionEpoch; D for ForgetFence | A boundary requiring both validates both independently. |
| BIH36-JD-14 | BMCP authentication context is protected verifier/transport context outside untrusted payload claims. Payload mirrors and selectors never override protected issuer, principal, audience, session, Actor or workload bindings. | H wire/transport; I trust; B types | Integrity/signature proves message integrity only, not issuer trust, Principal registration or authorization. |
| BIH36-JD-15 | Every ACK binds authenticated issuer/principal, Adapter application and concrete instance, Agent/runtime instance, fresh RuntimeSessionRef, verifier-resolved ActorRef, exact Scope roles, operation/delivery/forget identity, CapabilityEpoch, PermissionEpoch, applicable ForgetFence, action/region/coverage, immutable ACK ID and evidence digest. | H transport; I auth; operation owners | Same ACK ID+digest is idempotent; same ID+different digest is conflict. Old-session/stale/superseded/post-revocation ACKs are historical only and cannot roll back state. |
| BIH36-JD-16 | Reconnect order is fixed: fresh Authenticate; Validate Issuer; Resolve Principal/workload bindings; Negotiate Capability; obtain current PermissionEpoch; obtain current ForgetFence; suppress/clear stale state; reconcile delivery/ACK journal; resume only after final-boundary authorization. | H protocol; I trust; D/G state | Any failed/indeterminate step keeps protected state suppressed/unavailable. Old sessions do not inherit ACK authority. |
| BIH36-JD-17 | Unknown security-critical fields/enums, malformed refs, duplicate canonical keys, unsupported major version, identity mismatch, missing required scope/environment, stale epochs and ambiguous outcomes fail closed. No silent downgrade or payload fallback. | H wire; I policy; B types | Errors expose stable non-sensitive code/correlation metadata only. |



### 9.2 B-specific adoption

B adopts BIH36-JD-01..03, JD-05..06, JD-08..09 and the B semantic portions of JD-10/JD-14/JD-15 as the controlling Phase 3.6 domain-identity baseline. ActorRef is per-operation attribution; PrincipalRef and IssuerRef are distinct; ScopeRef roles are explicit; no Ref is authentication or permission. B does not approve I governance policy, H wire encoding or C/D/E/F/G consumer migration.

### 9.3 Governance and non-claims

I36-GOV-01..08 remain GOVERNANCE-BLOCKED as applicable. Environment registry ownership remains to be formally assigned. Implementation tests are NOT RUN. ADR-001 remains ADR-BLOCKED.

## 10. Phase 3.6 Self-Review Remediation — Binding B Clarifications

This section resolves B36-SR-01..07. It is normative for B's Phase 3.6 semantic contract.

### 10.1 AuthenticationContextRef disposition (B36-SR-02 / H36-SR-01)

AuthenticationContextRef is **not a tenth domain identity Ref** and MUST NOT appear as a caller-constructible or payload-selectable domain reference. It is a verifier-internal opaque handle owned jointly by the H/I authentication implementation boundary. Its value is not serialized in ordinary BMCP payloads, is not accepted from untrusted senders, is not dereferenceable by domain consumers, and confers no permission. It is scoped to one authenticated channel/session and verifier lifecycle; it expires or is invalidated on channel/session closure, credential/issuer revocation, principal/workload binding change, or verifier restart unless a secure verifier-owned continuation is explicitly established. H may carry a protected internal handle between trusted verifier components; B does not register it in Typed Reference Registry.

ActorRef stores only the verifier's stable operation-attribution result and its validated typed domain components. It MUST NOT expose the internal AuthenticationContextRef handle as a public field or durable domain identifier.

### 10.2 Canonical Principal namespace (B36-SR-03)

The canonical Principal resolution key is the ordered tuple:
`(IssuerRef, TrustDomainRef, TenantRef, PrincipalKind, IssuerSubject)`.
All five components are required for issuer-authenticated resolution. TenantRef and TrustDomainRef are distinct dimensions and MUST NOT be concatenated into an ambiguous string. PrincipalKind is a closed, versioned enum. IssuerSubject is opaque and compared byte-for-byte after the issuer-defined canonicalization profile has been validated by I. Display names, email addresses and mutable aliases are never primary keys. A change to any tuple component creates a new resolution identity unless I records an explicit, audited link/migration; it never silently rewrites or merges PrincipalRef.

### 10.3 Workload binding cardinality and history (B36-SR-04)

Principal-to-Agent/Adapter/Producer bindings are explicit, time-bounded registry relationships, not one-to-one identity equivalence. A Principal may bind to multiple workload identities. A workload identity may have multiple Principal bindings only where I's policy explicitly models distinct credential subjects/roles and records the exact validity intervals; overlapping active bindings that create ambiguity are denied. Every binding records issuer, tenant/security domain, workload identity, concrete instance where applicable, effective-from/to, status, registration version and revocation reason. Credential rotation does not create a new workload identity unless the workload registration itself changes. Instance replacement creates a new instance identity; old instances remain historical and cannot authenticate new work after revocation/retirement.

### 10.4 Canonical Scope role set (B36-SR-05)

Every protected operation carries a canonical, non-empty, role-tagged ScopeBindingSet whenever the operation is scoped. Each entry is `(ScopeRef, ScopeRole)`; ScopeRole is a closed enum:
- `OWNERSHIP`: administrative/data custody boundary;
- `APPLICABILITY`: boundary in which the resource/proposition is asserted to apply;
- `SOURCE` and `TARGET`: explicit endpoints of a cross-Scope operation/bridge, where the operation profile requires them.

Entries are sorted by canonical typed ScopeRef encoding then ScopeRole; exact duplicates are rejected; the same ScopeRef may appear under multiple roles only if the operation profile explicitly permits that combination. Unknown roles, missing required roles, conflicting owners, unresolvable refs, or sender omission fail closed. An empty set is allowed only for an operation profile explicitly classified as global/non-scoped by I and the resource owner; the sender cannot self-declare that classification.

### 10.5 Environment registry dependency (B36-SR-01)

B owns EnvironmentRef type semantics and canonical identity shape, not the real-world authority to create/retire environment records. Until the project designates a named Environment Registry Authority and publishes its trust/administration contract, EnvironmentRef resolution is **UNAVAILABLE** for protected cross-environment operations. Such operations are denied; consumers MUST NOT fall back to display labels, project membership or caller-supplied coordinates. The future registry contract MUST provide issuer/authority namespace, tenant/project, environment-kind, opaque stable ID, revision, lifecycle, authenticated adapter provenance, administrative ownership and revocation/history. This closes the semantic ambiguity without inventing an external owner.

### 10.6 Historical attribution versus current validity (B36-SR-06)

ActorRef is immutable historical attribution. It answers who/what was verified as acting for a particular operation at its authenticated time. It does not attest that the Principal, Issuer, credential, delegation or workload remains currently valid. New operations always resolve current status and authorization. Revocation preserves historical attribution and audit records but invalidates the ActorRef as a source of authority for any new operation. A historical ActorRef may be read only under current authorization and retention policy.

### 10.7 B decision-state reconciliation (B36-SR-07)

The older Section 6 table and status lines are historical process notes, not current status. For Phase 3.6, the controlling state is: **B domain semantics technically DECIDED under the user's delegated joint decision; no separate B-session signature is claimed.** The cross-module design baseline is jointly decided for B/I/H only. Consumer acceptance by C/D/E/F/G/Storage, Environment Registry Authority designation, governance approvals and implementation evidence remain OPEN/BLOCKED as stated in Sections 9 and 10.5. Any implementation-facing reader MUST use this current status rather than the superseded Candidate/Open process wording.
