# B Owner Formal Confirmation — ActorRef, ScopeRef and EnvironmentRef Type Mapping

- Owner: Session B — Domain Model
- Branch: session-b-domain-model-phase3
- Date: 2026-11-16
- Decision: APPROVE THE B-OWNED SEMANTIC TYPE MAPPING; EXACT CONSUMER FIELD PATHS AND WIRE ENCODINGS REMAIN OWNER-BOUND / CANDIDATE WHERE NOT FROZEN
- Exact A decision package reviewed: reviews/integration/phase-3.6-identity-trust-joint-architecture.md, Blob a45ae90b318a79bf009d14f4d917611881e9e214
- B canonical registry: 02-domain-model/typed-reference-registry.md, Blob af23ca9e019ab067a5f8ff62da902d4a419db3f3
- B principal/actor mapping: 02-domain-model/principal-actor-binding-mapping.md, Blob bbbef919e1e2ffe158cda8d9b2c5e718efaae969
- B scope/environment semantics: 02-domain-model/typed-reference-and-scope-semantics.md, Blob e9a6bd21e06bc02a5208619f5a949217860b1c00
- Prior B joint decision: 02-domain-model/phase-3.6-bih-joint-architecture-acceptance-addendum.md, Blob 2abf2784051a4ef1430d4acfacbdfd234d7553fc

## 1. Formal decision

B has reviewed A's exact Phase 3.6 BIH joint architecture decision package and the current B-owned typed-reference, Principal/Actor and Scope/Environment artifacts.

**B APPROVES the domain-semantic mapping of ActorRef, ScopeRef and EnvironmentRef set out below and in the cited A package.** No semantic type substitution is required. This is a B Owner decision within B's authority over domain types and reference semantics.

This approval does not freeze H's wire field names/serialization, approve I trust or authorization policy, designate an external registry authority, approve C telemetry schema, or sign for D/E/H/I or other consumers. Where an exact consumer field path is not yet owner-confirmed, it remains a candidate mapping rather than an approved implementation schema.

## 2. Normative type mapping

### 2.1 ActorRef

**B-confirmed meaning:** immutable, verifier-produced, per-operation attribution identifying the actor context responsible for one operation. It is not a stable Principal alias, credential, permission, bearer token or reusable capability.

Required semantic binding:
- authenticated PrincipalRef;
- validated IssuerRef;
- verifier-owned AuthenticationContextRef (opaque reference, never raw credential);
- exact operation/attribution identity and applicable RuntimeSessionRef;
- optional AgentRef, AdapterRef, ProducerRef, DelegationChainRef and acting_for_ref: PrincipalRef, only when independently resolved and relevant.

Rules:
1. The trusted verifier constructs ActorRef from protected authentication/session/workload context and authoritative registries. A payload ActorRef is an untrusted claim only.
2. One Principal may have many ActorRefs. Different operation, session, delegation or attribution provenance produces a distinct immutable ActorRef.
3. Historical attribution is immutable and never reassigned. Its use for a new operation does not prove current authentication, delegation, revocation status or permission; I must revalidate those.
4. Delegation does not convert the delegate Principal into the represented Principal. ActorRef records the authenticated actor and separately records any verified acting-for relationship.
5. ProducerIdentity/ProducerRef identifies the emitting workload; ActorRef identifies the attributed actor. They are not interchangeable.
6. H owns transport authentication/binding and wire representation; I owns issuer trust, Principal resolution, delegation and authorization assertions; B owns this domain meaning.

**Approved semantic mapping:** any logical field whose meaning is “who/what authenticated actor performed this operation” maps to ActorRef (e.g. D author_ref/requester_actor_ref, H's authenticated Actor binding, I actor_ref). Such fields MUST NOT be mapped to PrincipalRef, ProducerRef, AgentRef or AdapterRef merely because a legacy field is named author, source or actor_id.

### 2.2 ScopeRef

**B-confirmed meaning:** stable, typed identity of an ownership or applicability/data boundary. ScopeRef identifies the domain in which an object/request is owned, interpreted or applicable. It is not permission, role, grant, tenant wildcard, policy decision or physical storage partition.

Required semantic distinctions:
- exactly one primary ownership ScopeRef for a canonical object under the current model;
- zero or more role-labelled applicability ScopeRefs;
- where relevant, explicit source, target, evidence/provenance or other role-labelled ScopeRef bindings;
- authoritative Scope registry namespace, opaque never-reused Scope ID and registry-validated Scope kind/status;
- optional versioned Scope descriptor/containment history when the operation depends on historical hierarchy or attributes.

Rules:
1. Ownership and applicability MUST remain separately typed and role-labelled; they MUST NOT be flattened into an unordered union.
2. Containment is domain organization/lifecycle metadata only. Parent/child, sibling, same tenant, same Principal, same Agent or same label grants no access and implies no permission inheritance.
3. A stored cross-Scope reference is not permission to dereference either endpoint. Each endpoint and Evidence/Provenance access is separately authorized by I.
4. Cross-Scope access defaults to deny; any sharing/grant and its recipient/action/resource/purpose/audience/expiry/revocation are I-owned policy.
5. Scope mismatch (invalid domain relationship) and Permission Denied (policy rejection) are distinct outcomes.
6. A ScopeRef remains historically addressable after closure/revocation under retention rules, but its existence does not authorize new operations.

**Approved semantic mapping:** owner_scope_ref/ownership_scope_ref map to one owner ScopeRef; applicability_scope_refs[] map to a role-labelled set of ScopeRefs; target_scope_refs[], source and evidence Scope fields retain their explicit roles. A generic scope_ref is insufficient where the operation requires multiple roles unless the role is separately encoded and validated.

### 2.3 EnvironmentRef

**B-confirmed meaning:** stable typed identity of an authoritative external execution/state domain (for example, a world, save, simulation, device fleet or other external state domain). It is not a display label, ScopeRef, tenant label, URL, coordinate, environment version or policy domain.

Required semantic binding:
- authoritative Environment Registry namespace/authority;
- opaque, stable Environment identity;
- registry-resolved tenant/project/security-domain relationship and environment kind where required;
- explicit lifecycle/status;
- separate environment revision/version where state version matters;
- when a domain model requires an Environment Scope association, a distinct role-labelled ScopeRef in addition to EnvironmentRef.

Rules:
1. EnvironmentRef and ScopeRef are orthogonal and MUST NOT be cast to each other. An Environment ScopeRef may scope data associated with an environment; it does not replace the EnvironmentRef identity.
2. Environment-bound Event/Observation/Memory/Relation data must carry a resolved EnvironmentRef when environment identity is material. Required Environment Scope association is carried separately.
3. Free-text names, labels, URLs, world names or coordinates are selectors/claims only; resolve them through the authoritative registry or authenticated Environment Adapter.
4. Cross-Environment references/access default to deny. A bridge requires exact registered source and target EnvironmentRefs, explicit bridge/mapping relation, provenance, validity and I authorization.
5. Same Agent, Principal, project label or Scope kind in two environments does not establish environment equivalence.
6. Environment identity and environment revision are distinct; a bridge between identities does not prove revision/state equivalence.

**Approved semantic mapping:** logical environment_ref/applicable_environment_ref/environment_scope_ref fields must resolve to the correct typed EnvironmentRef or explicit Environment ScopeRef according to their actual meaning. A legacy environment_id or environment_scope_id string MUST NOT be silently treated as either type without an authoritative registry resolution and explicit schema mapping. If both environment identity and environment-scoped data boundary are needed, both typed references are present.

## 3. Cross-module mapping matrix — B semantic approval

| Consumer / boundary | Logical field or concept | B-confirmed type and semantics | Boundary / remaining authority |
|---|---|---|---|
| C telemetry | agent_id | AgentRef claim, not ActorRef or PrincipalRef | C owns exact telemetry field/schema; H/I verify trusted binding |
| C telemetry | producer_id | ProducerRef claim, not ActorRef | C owns event semantics; I owns Producer registry; H authenticates workload |
| C telemetry | adapter_id | AdapterRef claim, not AgentRef | H owns Adapter registry/protocol binding; C owns field presence |
| C telemetry | environment_id / environment context | Candidate EnvironmentRef selector; registry-resolve before use; any Environment ScopeRef is separate | C owns exact path; Environment Registry Authority/I owns trusted resolution |
| D canonical memory | author_ref, requester_actor_ref | ActorRef when meaning is operation attribution | D owns exact model/path and canonical validation; I/H supply trusted binding |
| D canonical memory | scope_refs[], target_scope_refs[] | Role-labelled ScopeRef set (owner/applicability/target roles preserved) | D owns exact storage shape; I authorizes access |
| D canonical memory | environment_scope_id | Legacy/ambiguous selector only; resolve to EnvironmentRef and, if required, a separate Environment ScopeRef | D owns migration/schema; registry/I owns resolution |
| E compiler | executing collector / attributed operation | ActorRef | E preserves verifier-issued attribution; H/I provide trust context |
| E compiler | source_id, source_type, producer_ref | Typed source identity / ProducerRef according to source-vs-producer meaning; never infer ActorRef from source string | E owns exact field semantics; I owns producer registration |
| E compiler | scope_refs[] | Role-labelled ScopeRef set, not flattened | E owns ExtractionIR/proposal paths; D owns canonical model |
| E compiler | environment_scope_id | Resolve as environment identity and/or environment scope through explicit mapping; never cast from raw string | E owns migration/requiredness; registry/I owns trusted resolution |
| H BMCP | authenticated actor binding | ActorRef bound to protected verifier context and exact operation/session | H owns wire encoding/authentication binding; I owns trust assertions |
| H BMCP | scope_ref / Scope bindings | ScopeRef with explicit role(s); multiple roles remain distinguishable | H owns wire schema/requiredness; I authorizes; consumer revalidates |
| H BMCP | applicable Environment | EnvironmentRef; separate Environment ScopeRef if required | H owns wire schema; I/Environment Registry Authority own trust/bridge policy |
| I authorization | actor_ref | ActorRef, separate from authenticated PrincipalRef | I owns validation/policy; H supplies verifier binding |
| I authorization | ownership/applicability Scope fields | Role-labelled ScopeRef(s) | I owns policy and registry authority; B owns type meaning |
| I authorization | environment_ref / environment scope | EnvironmentRef plus separate Environment ScopeRef where applicable | I owns authorization/bridge policy; registry authority resolves identity |
| Storage / E final boundary | actor + Scope + Environment | Preserve exact typed refs and role/digest binding; no string coercion | Storage/E own enforcement and durable mapping; I owns current authorization |

This matrix approves semantic types and non-substitution rules only. It does not approve unverified field names, field presence, cardinality in a concrete schema, serialization, database columns, or consumer implementation.

## 4. Namespace and conversion invariants

- Every reference retains a registered type discriminator and authority/issuer/namespace dimensions through API, event, storage, log and wire boundaries.
- IDs are opaque, non-semantic and never reused. Display labels and caller-selected strings are not identity keys.
- Unknown/incompatible type, namespace mismatch, ambiguous resolution or loss of role information fails closed.
- No implicit conversion is permitted among ActorRef, PrincipalRef, ProducerRef, AgentRef, AdapterRef, ScopeRef, EnvironmentRef, PermissionEpoch, CapabilityEpoch or D ForgetFenceGeneration.
- Deserialization establishes syntax/type only. Existence, lifecycle, trust, domain compatibility and authorization remain separate checks.
- Exact JSON/CBOR/Protobuf fields and canonical serialization are not frozen by B; H owns BMCP wire form and each consumer owns its internal schema.

## 5. Explicit open decisions and authority boundaries

The following remain open and are not silently approved by this B decision:
1. I/Governance: trusted Issuer/Principal/Producer/Adapter/Environment authority, delegation, grants, revocation, PermissionEpoch, cross-Scope grants, cross-Environment bridge and governance activation.
2. H: exact BMCP field spelling, envelope schema, canonicalization, requiredness registry, protocol versioning and cryptographic profile.
3. C: exact telemetry field paths, producer/agent/adapter/environment field presence and migration.
4. D/E: exact internal schema/field paths, environment_scope_id migration, owner/applicability role names and persistence.
5. Environment Registry Authority designation and authoritative Scope Registry ownership/lifecycle remain OPEN until formally assigned.
6. Runtime implementation and conformance remain unverified. No I36/H36/B consumer test PASS is claimed.

Fact/Claim ADR-001 remains ADR-BLOCKED. This mapping approval does not authorize a Fact/Claim canonical identity or revision model.

## 6. Disposition for A

A may record:
- B ActorRef semantic mapping: OWNER-CONFIRMED.
- B ScopeRef semantic mapping: OWNER-CONFIRMED.
- B EnvironmentRef semantic mapping: OWNER-CONFIRMED.
- Cross-module semantic type/non-substitution matrix: B-APPROVED.
- Exact consumer field paths and wire schema: PARTIAL / OWNER-BOUND / NOT FROZEN.
- External registry/governance authority: OPEN / GOVERNANCE-BLOCKED.
- Implementation/runtime conformance: NOT VERIFIED.

A must not infer H wire-schema freeze, I governance approval, C/D/E consumer schema acceptance, production readiness or runtime conformance from this B decision.

## B Owner exact-version typed-reference confirmation — CGH-APPLIED-1.1

- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA: `9808b31f840606b329f1a794935dfc9c5084d63b`
- Common contract: `CGH-APPLIED-1.1`
- Causal profile: `CausalOrderProfile/1.0`

**Decision: APPROVE — B-owned typed-reference semantics and role-preserving bindings for this exact 1.1 package**, with the bounded reservations below.

B confirms ActorRef remains verifier-produced per-operation attribution bound to authenticated PrincipalRef/IssuerRef and exact operation/session; ScopeRef remains a stable ownership/applicability boundary with role-labelled source/target/evidence bindings kept distinct; EnvironmentRef remains a stable authoritative external state-domain identity, distinct from ScopeRef and environment-scoped data boundaries. The 1.1 package's Actor/Principal/Issuer, role-labelled ScopeBindingSet and EnvironmentRef bindings do not require a B semantic type change.

Reservations:
1. Typed references are identifiers/attribution types, not credentials, permission grants, authorization receipts, coordinator positions, fence clearances or reusable capabilities.
2. B does not authorize cross-Scope or cross-Environment access; those remain deny-by-default absent exact registry resolution and I authorization.
3. B confirms semantic types and role preservation only. C/G/H own their consumer field paths, schema field encoding, canonicalization and wire requiredness; this decision does not freeze those representations.
4. Legacy untyped strings must not be silently cast to typed refs; registry-backed authoritative resolution remains required.
5. B does not approve I governance, coordinator deployment, D lineage completeness, G Applied implementation, runtime conformance or any 1.0-to-1.1 approval transfer.

This is an exact-version B semantic confirmation against the A Blob above, not a wire-schema approval or implementation claim.
