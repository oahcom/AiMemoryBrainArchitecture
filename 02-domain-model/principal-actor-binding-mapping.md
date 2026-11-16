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
