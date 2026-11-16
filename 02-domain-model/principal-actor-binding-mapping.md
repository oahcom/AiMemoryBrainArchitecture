# Principal / Actor Binding and Consumer Compatibility Matrix

- **Owner:** Session B — Domain Model
- **Status:** CANDIDATE cross-module mapping; identity freeze remains OPEN (INT-P0-02 / INT-X-03)
- **Branch:** `session-b-domain-model-phase3`
- **Authority:** B defines reference semantics only. I owns Principal/authentication policy and trust registry; H owns transport binding/wire format; C owns telemetry field semantics; D/E own their internal canonical/compiler operations.

## 1. Principal-to-actor binding chain

`Issuer → validated credential/session → authenticated PrincipalRef → verifier-issued ActorRef → optional DelegationChainRef → operation-specific AgentRef / AdapterRef / ProducerRef + ScopeRef / EnvironmentRef → I PolicyDecision`

Each arrow is a verified binding, not a string cast.

| Concept | Meaning | Owner / authority | Required distinction |
|---|---|---|---|
| Issuer | Authority that issued a credential/assertion or signed delegation | I trust registry | Unknown/untrusted issuer fails closed; trust is not transitive |
| Authenticated Principal | Security subject established by credential/session verification | I, verified at H boundary | PrincipalRef is not a payload identity claim |
| ActorRef | Per-operation attribution preserving Principal and auth/delegation provenance | B semantics; I assertions; H binding | Not a credential, not a permission, not a long-lived bearer token |
| Delegation | Bounded signed authority chain from grantor to delegate | I policy; B typed references | Not identity conversion; effective authority is intersection of all constraints |
| AgentRef | Logical Agent identity | Agent registry; I binding | Not an Agent instance, Principal or Adapter |
| AdapterRef | Registered protocol Adapter/application or instance | H registry; I Principal binding | Not the logical Agent; capability/session epoch is separate |
| ProducerRef | Registered source producer/workload | I registry; C assertion; E ingress; D work admission | Payload producer_id is a claim, not authentication |
| ScopeRef | Ownership/applicability domain | B semantics; I/Governance registry/policy | Not permission or tenant wildcard |
| EnvironmentRef | Authoritative world/save/simulation/external-state identity | Environment registry; I trust binding | Not a display label; environment version is separate |
| PermissionDecision | Action/resource/scope/purpose/audience-bound authorization result | I | Not a Ref and not transferable across resource/scope/audience |

## 2. Binding invariants

1. Authentication MUST complete before payload identity claims are resolved.
2. H MUST bind transport/session/workload identity to I's authenticated Principal and registered Adapter/Producer identity; exact wire fields remain H-owned.
3. C's telemetry `producer_id`, `agent_id`, `adapter_id`, `environment_id` (if present) are claims to compare against trusted bindings, never credentials.
4. E MUST preserve the verifier-issued ActorRef and typed Scope/Environment refs through receipt, compile attempt, retry and proposal; it MUST NOT mint identity from model output or source text.
5. D MUST validate ActorRef binding and Scope compatibility at canonical mutation/commit boundaries; canonical authority does not imply authentication authority.
6. I MUST re-evaluate current policy, delegation, revocation and PermissionEpoch at protected boundaries. Historical ActorRef does not prove current permission.
7. Adapter and Producer identities are independently registered and revocable even when they are bound to the same Principal.
8. An Agent may be delegated to act for a Principal only through explicit bounded delegation/assignment; a matching Agent label is not evidence.
9. EnvironmentRef and ScopeRef are resolved from authoritative registries or authenticated adapters, never inferred from free text.
10. If any required binding is absent, ambiguous, stale or inconsistent, fail closed. Do not silently downgrade to a generic string or anonymous actor.

## 3. Consumer compatibility matrix

| Consumer | Field / logical input | Type | Issuer / authority | Trust source | Validation boundary | Status / OPEN |
|---|---|---|---|---|---|---|
| C Telemetry | `producer_id` | ProducerRef assertion | I Producer registry; C defines field | Authenticated H session/workload + I registry | C ingress adapter/H binding; E rechecks on acceptance | Exact C field schema/path not independently retrieved; confirm requiredness and whether producer_id maps 1:1 to ProducerRef |
| C Telemetry | `agent_id` | AgentRef assertion | Agent registry + I Principal binding | Authenticated workload/session and registered Agent assignment | H/I before telemetry accepted; C validates semantic consistency | OPEN: distinguish logical Agent from agent instance |
| C Telemetry | `adapter_id` | AdapterRef assertion | H Adapter registry + I Principal binding | Authenticated Adapter session/capability registry | H transport boundary | OPEN: C field may be absent; never treat as AgentRef |
| C Telemetry | `environment_id` / environment context | EnvironmentRef assertion + Environment ScopeRef | Environment registry / I trust binding | Authenticated Environment Adapter or authoritative registry | H/I resolution; E validates Event/Evidence scope | OPEN: exact C field name and trusted source |
| D Canonical Memory | `author_ref`, `ActorRef` | ActorRef | B semantics; I Principal/issuer; H authenticated binding | Verifier-issued auth context + delegation chain | D canonical write/commit boundary | D core model uses author_kind + author_ref; ensure author_kind does not replace typed ActorRef |
| D Canonical Memory | `scope_refs[]`, `environment_scope_id` | ScopeRef[], EnvironmentRef/Environment ScopeRef | B semantics; I/Governance registry | Resolved registry refs, not caller strings | D canonical validation and read/write boundary | D must retain type and namespace; environment-bound assets require explicit binding |
| D Canonical Memory | `requester_actor_ref`, `target_scope_refs` | ActorRef, ScopeRef[] | D operation schema + I policy | Authenticated request binding and I authorization receipt | D Forget request admission; I controls permission and global completion | Do not infer global permission from ActorRef |
| E Compiler | `collector_ref`, `source_id`, `source_type` | ActorRef or ProducerRef according to field meaning; source_id is typed source identity, not auth | B semantics; I Producer registry; H binding | Authenticated ProducerIdentity/ActorRef; source registry | E durable ingress/receipt and every retry/replay | OPEN: preserve source origin vs executing collector; never collapse them |
| E Compiler | `scope_refs[]`, `environment_scope_id` | ScopeRef[], EnvironmentRef | B semantics; I/Governance registry | Trusted ingress metadata and authoritative environment binding | E acceptance, compile, dereference, publication | Must survive ExtractionIR and candidate proposals without model-generated substitution |
| E Compiler | `producer_ref`, `work_id`, `producer_class` | ProducerRef + stable work identity | I producer registration; D canonical producer-class/work barrier | Authenticated ProducerRef plus durable D registration receipt | E work admission/lease/retry and final publication gate | D work registration is not I producer-domain inventory; both epochs distinct |
| H BMCP | `source`, `recipient` | ProducerRef / AdapterRef / PrincipalRef assertions, role-discriminated | I trust registry; H wire registry | Authenticated transport/session plus H adapter registry | H envelope decode/authenticate/bind | Existing H calls source a logical producer assertion, not authentication |
| H BMCP | `scope_ref` | ScopeRef | B semantic type; I/Governance authoritative registry | Authenticated request binding and resolved Scope registry | H decode/bind then I authorize; consumer revalidates | Opaque owner-defined ref; wire encoding OPEN |
| H BMCP | `permission_epoch` | PermissionEpoch (not a Ref) | I | I signed/current policy decision | H transports unchanged; each consumer checks currentness | Never cast to ScopeRef, ActorRef or generic cursor |
| H BMCP | `forget_fence` | D ForgetFenceCursor/Generation (not a Ref) | D | D canonical fence receipt; I policy binding | H transports unchanged; D/I/consumers enforce own semantics | Never compare numerically to PermissionEpoch or capability epoch |
| I Governance | `authenticated_principal_ref` | PrincipalRef | I Principal registry, trusted Issuer | Credential/session verification | H authentication boundary; I resolves and authorizes | Candidate until joint B/H/Governance approval |
| I Governance | `actor_ref` | ActorRef | B semantic type; I auth assertion | H verifier-issued binding; issuer and auth context refs | I authorization decision and final operation boundary | Payload ActorRef alone rejected |
| I Governance | `producer_identity_ref` | ProducerRef / ProducerIdentityRef | I producer registry | Authenticated workload/session and registered producer | I ingress/authorization; E acceptance | Separate from D producer work registration |
| I Governance | `delegation_chain_ref`, `acting_for_ref` | DelegationChainRef, PrincipalRef | I delegation registry | Signed grant chain + issuer trust + revocation state | I before authorization and final commit/disclosure | Delegation never transfers ownership |
| I Governance | `ownership_scope_ref`, `applicability_scope_refs[]`, `environment_scope_ref` | ScopeRef[], EnvironmentRef | B semantics; I/Governance registry | Authenticated binding + authoritative registry | I scope resolution then policy evaluation | Scope resolution is not authorization |
| I Governance | `PolicyDecision.subject_ref`, `actor_ref` | PrincipalRef, ActorRef | I | Current policy engine and authenticated binding | I policy decision; consumers recheck epoch | Decision is bound to action/resource/scope/audience/purpose |

## 4. Producer and Agent identity distinctions

- **AgentRef** answers which logical Agent is involved.
- **PrincipalRef** answers which security subject was authenticated.
- **ActorRef** answers which authenticated subject is attributed with this operation.
- **AdapterRef** answers which registered Adapter instance/application transports or applies the operation.
- **ProducerRef** answers which registered source/workload is allowed to produce the declared event/work family.
- **EnvironmentRef** answers which authoritative external state domain the observation/action belongs to.
- **ScopeRef** answers which ownership/applicability boundary contains or qualifies the resource.

One operation may bind all of these, but they remain separate typed fields. A common Principal may be bound to an Agent, Adapter and Producer through explicit registry relationships; that does not make the references interchangeable.

## 5. ADR and approval gates

- INT-P0-02 / INT-X-03 remain **OPEN** until B typed reference semantics, I security assertions, H authenticated transport binding and C telemetry mapping are reconciled.
- H wire field names and encodings remain H-owned candidates; this document does not freeze them.
- I owns authentication, authorization, delegation, revocation and policy epochs.
- C owns telemetry schema and producer/event semantics.
- D owns canonical object identity and commit; E owns ingress/compile/producer-side enforcement.
- Architecture Governance must record the joint approval and evidence before any public identity schema is frozen.

 
## 6. Phase 3.6 Principal / Actor Binding Closure (CANDIDATE)

- **Status:** CANDIDATE cross-module mapping; INT-P0-02 / INT-X-03 remain OPEN. This section does not approve I policy or freeze H wire fields.
- **Baseline:** B HEAD `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`; prior blob `f20dc0cbd99b5eaf6451b5b8daf1af7c297102c6`.
- **Authority:** B defines typed semantics. I owns authentication, trust, delegation, authorization, revocation and PermissionEpoch. H owns transport/session binding and wire format. C owns telemetry event fields. D/E own canonical and compiler boundary validation.

### 6.1 Principal-to-Actor cardinality and lifecycle

- One Principal may be represented by many ActorRefs. ActorRef is per-operation attribution, not a second durable security subject; different operation, authenticated session, delegation context or attribution provenance produces a distinct immutable ActorRef.
- A Principal may be bound to multiple logical Agents, Adapters or Producers only through independently registered, authenticated bindings. These references remain different types and may have independent lifecycle/revocation.
- A single ActorRef identifies one operation's attributed actor context. It MUST bind the resolved PrincipalRef and IssuerRef plus verifier-owned AuthenticationContextRef; optional AgentRef, AdapterRef, ProducerRef and delegation refs are included only when verified and relevant.
- ActorRef has an immutable historical lifecycle: it is not rewritten or reassigned. The validity of using it for a new operation is not durable: I must re-check Principal, issuer, credential/session, delegation, revocation and current authorization.
- Revoking a Principal, issuer, credential, Agent, Adapter, Producer or delegation prevents new protected use according to I policy. It does not rewrite historical attribution. Whether an in-flight operation aborts depends on I's approved revocation/linearization policy and the owning D/E/H/C boundary; this remains **CANDIDATE / I GOVERNANCE-BLOCKED**, not decided by B.

### 6.2 Delegation and acting-for semantics

- Delegation is not PrincipalRef-to-ActorRef conversion, not ownership transfer and not a type cast.
- Candidate semantic shape: a verifier-resolved ActorRef may record the authenticated delegate PrincipalRef and an `acting_for_ref` grantor/represented PrincipalRef, together with a typed DelegationChainRef and AuthenticationContextRef.
- The delegated actor remains the authenticated delegate; the represented Principal remains separately identified. The ActorRef records both roles rather than pretending the delegate authenticated as the grantor.
- Effective authority, eligible grantors/delegates, maximum chain depth, sub-delegation, audience, purpose, resource/action, Scope, expiry and parent revocation are I policy decisions. They remain **GOVERNANCE-BLOCKED** in I36-GOV-02; B does not authorize them.
- Without a currently valid I-approved delegation/assignment, an Agent acting for a Principal is denied/indeterminate. Matching labels or possession of AgentRef do not establish delegation.

### 6.3 Issuer and cross-Issuer handling

- IssuerRef is a typed identity of an issuing authority; it is not a trust decision.
- Principal identity is namespaced by IssuerRef and the declared tenant/security domain. Equal subject strings under different issuers are different identities unless I approves an explicit federation mapping.
- No trust is transitive. A credential/assertion from an unknown, suspended, compromised or untrusted issuer cannot establish an Authenticated Principal.
- Cross-Issuer identity linking, federation, key rotation/compromise and trust-domain admission remain **OPEN / I36-GOV-01 GOVERNANCE-BLOCKED**. B only requires explicit issuer-qualified references and rejects string-based aliasing.

### 6.4 Revocation effects (domain semantics vs policy)

| Event | B domain invariant | I policy dependency / status |
|---|---|---|
| Credential/key rotation | PrincipalRef may remain stable; credential/authentication context is new | I decides trust transition; OPEN |
| Principal or Issuer revoked | Historical ActorRefs remain immutable; no new trusted binding is inferred | I defines effective point and in-flight semantics; GOVERNANCE-BLOCKED |
| Agent/Adapter/Producer registration revoked | Their refs remain historical identifiers, but new operation binding must not be inferred | I/H define registration and revocation; OPEN |
| Delegation revoked/expired | ActorRef's historical delegation provenance remains; it cannot prove current delegated authority | I defines chain invalidation and PermissionEpoch; GOVERNANCE-BLOCKED |
| Runtime session expired/revoked | RuntimeSessionRef remains historical; cannot be renewed or replayed as current session | H/I define session authority and revocation; OPEN |
| Scope closed/revoked | ScopeRef remains an identity; new access/association is policy-controlled | I/Governance decides action and retention behavior; OPEN |

### 6.5 Required validation order (logical; policy remains I-owned)

1. Authenticate protected transport/session/workload using an approved verifier; obtain protected issuer and credential/session result.
2. Resolve IssuerRef and Authenticated PrincipalRef through I trust/Principal registry.
3. Resolve AgentRef, AdapterRef, ProducerRef and RuntimeSessionRef from their authoritative registries and bind to authenticated Principal; do not trust payload selectors.
4. Compare payload identity claims with protected bindings. Any mismatch, unknown issuer, missing required binding or stale/revoked session is rejected or quarantined; never prefer payload.
5. Resolve ActorRef only from verifier-produced operation context; validate its Principal, Issuer, authentication-context and any delegation chain.
6. Resolve ScopeRef and EnvironmentRef from authoritative registries; validate namespace, kind, lifecycle and operation compatibility.
7. Ask I for current authorization of exact Principal + Actor + action + resource + audience + purpose + resolved Scope/Environment; revalidate at the owning final commit/disclosure boundary.

The order is a candidate cross-module protocol sequence. Exact APIs and wire representation remain OPEN.

### 6.6 Consumer Field Mapping — producer, wire and domain bindings

All names in the Wire Field column are existing logical names or candidate mappings only. H owns wire naming/serialization; C owns telemetry field definitions; this table does not freeze either.

| Consumer | Producer Field | Wire Field (candidate / logical) | Domain Type | Issuer / Authority | Authentication Source | Validation Owner | Authorization Owner | OPEN Decision |
|---|---|---|---|---|---|---|---|---|
| C Telemetry | producer's declared producer identity | `producer_claim`, `producer_id` | ProducerRef assertion | I Producer registry | H protected workload/session binding resolved by I | H/I at ingress; C checks claim; E rechecks acceptance | I | Exact required field, alias and ProducerRef-to-ProducerIdentity cardinality |
| C Telemetry | logical Agent and running instance | `agent_id`, `agent_instance_id` | AgentRef + distinct instance identity | Agent/deployment registry; I Principal binding | H authenticated workload/session + assignment | H/I binding; C semantic validation | I | Exact instance Ref type and whether both fields mandatory by signal kind |
| C Telemetry | Adapter application/instance | `adapter_id`, optional `adapter_instance_ref` | AdapterRef + distinct instance ref | H Adapter registry; I Adapter Principal | H authenticated Adapter channel/session | H; I verifies Principal/revocation | I | C field presence and canonical Adapter instance ref |
| C Telemetry | environment context | `environment_id` | EnvironmentRef assertion | Environment registry; I trust binding | Authenticated Environment Adapter or trusted registry resolution | H/I resolve; C validates signal requirement; E checks scope | I | Exact trusted environment source and requiredness for environment-dependent signals |
| C Telemetry | operation attribution | `actor_ref` / ActorRef claim | ActorRef | B semantic type; I auth assertions | H verifier-issued AuthenticationContextRef | H produces; C/E/D reject unverified payload ActorRef | I | Exact protected binding evidence and ActorRef profile |
| C Telemetry | ownership/applicability boundary | `scope_ref` / `scope_refs[]` | ScopeRef[] with explicit roles | B semantics; I/Governance registry | Protected request binding + authoritative registry | H/I resolve; C checks event semantics; E validates ingress | I | Single vs multiple scopes, roles, and exact C field name |
| C Telemetry | runtime session | `session_id` | RuntimeSessionRef selector, not auth | H/I session authority | Protected authenticated channel/session | H/I | I | Whether C serializes opaque RuntimeSessionRef or only a non-authoritative correlation selector |
| D Canonical Memory | author/attributor | `author_ref`, `created_by_actor_ref`, `author_actor_ref` | ActorRef | B semantics; I Principal/Issuer; H verifier | Protected auth context + verified operation binding | D at canonical mutation/commit; I supplies trust/policy result | I | D field alias consolidation and typed schema; `author_kind` cannot replace ActorRef |
| D Canonical Memory | owner/applicability | `owner_scope_ref`, `scope_refs[]`, `applicability_scope_refs`, legacy `environment_scope_id` | ScopeRef[] with role; EnvironmentRef distinct | B semantics; I/Governance Scope registry; Environment authority | Trusted request context + registry resolution | D canonical validation/read/write; I validates grant | I | Retire untyped `environment_scope_id` only through D-owned migration; no implicit cast |
| D Forget admission | requester and target | `requester_actor_ref`, `target_scope_refs` | ActorRef + ScopeRef[] | B type; I Principal/authorization | Protected request authentication | D admission checks typed refs; I decision | I | Exact request envelope and policy receipt fields |
| E Compiler ingress | event origin vs executing collector | `producer_ref`, `producer_actor_ref`, `collector_ref`, `source_id`, `source_type` | ProducerRef; ActorRef; typed Source identity (not auth) | I Producer registry; source registry; B type semantics | H authenticated ProducerIdentity/session; verifier ActorRef | E durable ingress and every retry/replay; I resolves trust | I | Preserve origin ProducerRef separately from collector ActorRef; no overload of source_id |
| E Compiler ingress | scope/environment context | `scope_refs[]`, `environment_scope_id` (legacy candidate) | ScopeRef[] + EnvironmentRef | B semantics; I/Governance + Environment registry | Trusted ingress metadata, not model output | E acceptance, compile, dereference and publication; D rechecks canonical commit | I | E field migration to typed EnvironmentRef; role/requiredness |
| E Compiler work | producer and work admission | `producer_ref`, `work_id`, `producer_class` | ProducerRef + separate WorkItem identity/class | I producer registration; D per-work barrier | Authenticated ProducerRef plus D durable work-registration receipt | E admission/lease/retry/publication; D validates its barrier | I for producer trust; D for work admission | Keep I ProducerDomain inventory distinct from D WorkItem registration/cursor |
| H BMCP envelope | source endpoint/producer | `source` | role-discriminated ProducerRef / PrincipalRef assertion | I trust registry; H endpoint registry | Protected authenticated transport | H decode/authenticate/bind; I resolves | I | Candidate wire role discriminator and exact encoding |
| H BMCP envelope | recipient endpoint | `recipient` | role-discriminated AdapterRef / PrincipalRef assertion | H Adapter registry; I Principal registry | Authenticated channel + registered recipient binding | H and I | I | Distinguish stable Adapter app, Adapter instance and Principal |
| H BMCP envelope | request scope | `scope_ref` | ScopeRef | B semantic type; I/Governance registry | Protected authenticated request + registry resolution | H bind; each consumer revalidates | I | Exact wire representation and multi-scope extension |
| H BMCP protected context | authenticated caller/session | protected `auth.issuer_ref`, `auth.principal_ref`, `auth.authentication_context_ref`, `runtime_session_ref` | IssuerRef + PrincipalRef + verifier context + RuntimeSessionRef | I trust/Principal; H/I session authority | Transport verifier output only; payload mirror remains claim | H obtains protected context; I validates trust/session | I | Protected context API, RuntimeSessionRef issuer/expiry and exact field names |
| H BMCP | policy token | `permission_epoch` | I PermissionEpoch (not a Ref) | I | I-issued policy authority | H transports unchanged; consumer rechecks | I | Policy-domain/lease contract remains I36-GOV-06 GOVERNANCE-BLOCKED |
| H BMCP | Forget token | `forget_fence` | D ForgetFenceRef/Generation (not a Ref) | D | D canonical fence receipt | H transports unchanged; D validates | I owns authorization; D owns fence | Exact wire mapping; never compare with PermissionEpoch |
| I Governance | authenticated subject | `authenticated_principal_ref` | PrincipalRef | I Principal registry + IssuerRef | Validated credential/session at H verifier | I resolves issuer/Principal and trust chain | I | I36-GOV-01 issuer and Principal policy GOVERNANCE-BLOCKED |
| I Governance | operation attribution | `actor_ref` | ActorRef | B semantic type; I assertion policy | H verifier-issued auth context; optional delegation proof | I validates binding and chain | I | I36-GOV-02 delegation policy GOVERNANCE-BLOCKED |
| I Governance | producer registration | `producer_identity_ref` | ProducerRef / I ProducerIdentity binding | I producer registry | Authenticated workload/session | I ingress; E acceptance; D separately registers work | I | ProducerRef registry and inventory contract approval |
| I Governance | delegation relationship | `delegation_chain_ref`, `acting_for_ref` | DelegationChainRef + PrincipalRef | I delegation authority | Signed issuer-verified grant chain | I validates before authorization and final boundary | I | Eligibility, depth, sub-delegation and revocation remain GOV-BLOCKED |
| I Governance | resource boundaries | `ownership_scope_ref`, `applicability_scope_refs[]`, `environment_scope_ref` | ScopeRef[] + EnvironmentRef | B type semantics; I/Governance and Environment registry | Authenticated binding + registry | I resolves Scope/Environment | I | Cross-Scope I36-GOV-03 and cross-Environment I36-GOV-04 GOV-BLOCKED |

### 6.7 Authorization boundary and non-substitution

- Authentication answers who presented a valid credential/session under a trusted issuer.
- Reference resolution answers which registered domain identity a typed reference denotes.
- Authorization answers whether the authenticated Principal may perform the exact action on the exact resource, audience, purpose and resolved Scope/Environment now.
- D/E canonical or durable custody does not confer authentication or permission.
- H transport integrity does not establish authorization or semantic truth.
- C telemetry authenticity does not promote a report into a verified Fact/Claim.
- A PermissionDecision is I-owned, action/resource/audience/purpose/scope-bound and non-transferable. PermissionEpoch is an I-owned currentness token, not a reference and not interchangeable with any other epoch.

### 6.8 OPEN decisions and evidence requirements

| ID | Decision | Owner | Status |
|---|---|---|---|
| B36-OPEN-01 | Approve common IssuerRef/NamespaceRef and federation binding | I + B; Governance approval | OPEN / I36-GOV-01 GOVERNANCE-BLOCKED |
| B36-OPEN-02 | Approve delegation grant model, actor acting-for semantics and revocation | I; B supplies type semantics | OPEN / I36-GOV-02 GOVERNANCE-BLOCKED |
| B36-OPEN-03 | Approve cross-Scope grant/inheritance/sharing algebra | I + Governance; B supplies Scope semantics | OPEN / I36-GOV-03 GOVERNANCE-BLOCKED |
| B36-OPEN-04 | Approve cross-Environment bridge/federation policy | I + Environment owner | OPEN / I36-GOV-04 GOVERNANCE-BLOCKED |
| B36-OPEN-05 | Approve revocation effective point and in-flight operation behavior | I + owning boundary owners | OPEN / I36-GOV-05 GOVERNANCE-BLOCKED |
| B36-OPEN-06 | Approve PermissionEpoch policy-domain, propagation and bounded lease semantics | I | OPEN / I36-GOV-06 GOVERNANCE-BLOCKED |
| B36-OPEN-07 | Freeze H wire names/encoding and protected authentication-context exposure | H with B/C/I acceptance | OPEN / CANDIDATE |
| B36-OPEN-08 | Confirm C telemetry field presence/requiredness and typed mapping | C with B/H/I | OPEN / CANDIDATE |
| B36-OPEN-09 | Confirm D/E canonical/compiler field aliases and typed EnvironmentRef migration | D/E with B; I validates policy | OPEN / CANDIDATE |
| B36-OPEN-10 | Confirm runtime-session issuer, lifetime and cross-instance binding | H/I | OPEN / CANDIDATE |

### 6.9 ADR-001 remains independent and blocked

This identity mapping does not decide Fact/Claim semantics, canonical object identity or attestation authority.

- ADR-001 status remains **ADR-BLOCKED**.
- No Fact/Claim schema, canonical ID, revision model, DDL, API or wire field is approved by this update.
- E continues to emit neutral CandidateProposition/ExtractionIR; D does not create canonical Fact/Claim objects.
- Any ClaimRef/ClaimRevisionRef use remains conditional on formal ADR approval.
- Identity/Scope completion cannot be used as evidence to close INT-P0-01.
