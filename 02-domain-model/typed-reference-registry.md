# Typed Reference Registry — Phase 3.5

- **Owner:** Session B — Domain Model
- **Status:** DECIDED semantic distinctions; exact wire encodings and several registry authorities remain OPEN
- **Branch:** `session-b-domain-model-phase3`
- **Purpose:** Common typed-reference semantics for C/D/E/H/I. This is a domain contract, not a credential format, wire schema, or authorization policy.

## 1. Normative vocabulary

These terms MUST NOT be collapsed:

- **Identity** is the durable subject or resource identity maintained by its authority.
- **Reference** is a typed, scoped pointer to an identity (optionally to an exact version). A reference is not proof that its presenter is that identity, nor permission to dereference it.
- **Credential** is evidence presented to an authentication boundary and validated under an issuer/trust policy. Credentials, secrets, bearer tokens, signatures and private key material MUST NOT be embedded in domain references.
- **Authenticated binding** is a verifier-produced association between a validated credential/session and one or more typed identities for a specific operation.
- **Permission** is a policy decision for a Principal, action, resource, audience, purpose and resolved Scope binding. It is not encoded by possession of a ScopeRef or any other Ref.

All IDs are opaque, non-semantic and non-reusable. Display names, labels, email addresses, model names, hostnames and caller-selected strings are never identity keys.

## 2. Common logical shape and serialization constraints

A logical reference has a discriminated type and typed components, not a bare universal string:

```text
TypedRef<T> {
  ref_type: registered type discriminator
  issuer_ref: IssuerRef
  namespace: NamespaceRef
  object_id: OpaqueId
  tenant_or_security_domain_ref: optional typed boundary
  version_ref: optional exact immutable version
}
```

This is illustrative logical shape only; it does not freeze JSON/CBOR/Protobuf field names or wire encoding.

1. A consumer MUST preserve the discriminator and namespace/issuer dimensions end-to-end.
2. A consumer MUST reject unknown or incompatible ref types; it MUST NOT reinterpret one Ref type as another.
3. A reference to a mutable head and a reference to an immutable version are distinct semantics. Use an exact version ref where historical identity/content matters.
4. Serialization MUST be canonical and versioned at the owning protocol boundary; string concatenation, delimiter parsing, lossy coercion and display-label serialization are forbidden.
5. References MUST NOT contain credentials, authorization decisions, permission epochs masquerading as identity, or secret-bearing locator data.
6. Deserialization establishes syntax/type only. Trust, existence, lifecycle, scope compatibility and authorization are separate validations.
7. Redaction-safe logs use type + non-reversible fingerprint or approved opaque ID; never log credential material or protected payloads.

## 3. Typed Reference Registry

| Type | Domain meaning | Identity / authority | Namespace | Stability / lifecycle | Cross-tenant / cross-Scope | Trust source and validation boundary |
|---|---|---|---|---|---|---|
| `ActorRef` | Attribution of the actor responsible for one operation, preserving authenticated principal and authority/delegation provenance | B owns semantic type; I establishes security assertions; H binds transport-authenticated subject | Issuer + tenant/security domain + Principal namespace; operation attribution may include ProducerRef/DelegationRef | Immutable per operation; points to stable PrincipalRef and immutable authentication/delegation context refs; never a credential | No implicit crossing; cross-scope action requires current authorization and explicit delegation/sharing | Trusted H authentication/session binding + I issuer/Principal/Delegation registry; D/E validate verifier-issued binding at their protected boundary. Payload ActorRef alone is untrusted |
| `ScopeRef` | Typed reference to an ownership or applicability/resource-data boundary | B owns domain meaning; I/Governance owns authoritative registry, grant/policy enforcement | Scope authority + tenant/security domain + Scope kind + opaque Scope ID | Stable while scope exists; status changes are authoritative and versioned; closed/revoked refs remain historically addressable but not ordinarily usable | Cross-Scope references require explicit compatible relationship and authorization; never infer from parent/child | Authoritative Scope registry and authenticated binding; validate kind, owner, parent, status, environment binding, compatibility, then separately authorize |
| `PrincipalRef` | Stable security subject (human, Agent, Agent instance, service, Adapter, external recipient) | I owns Principal registration and retirement; trusted Issuer establishes subject | Issuer + tenant/security domain + principal kind | Stable, opaque, never reassigned; retirement/revocation changes status, not identity | No implicit cross-tenant aliasing; explicit federation/trust mapping required | Valid credential/session, trusted issuer, audience, key and validity; I resolves; H authenticates. Ref itself is not proof |
| `AgentRef` | Logical Agent identity, distinct from a particular runtime instance or Adapter | Agent registry / deployment authority; I binds it to PrincipalRef; B defines reference semantics | Agent registry namespace + tenant/security domain | Stable logical identity; version/config revisions separate; retirement does not recycle ID | Same Agent may participate in multiple Scopes only through explicit bindings; no automatic cross-tenant or environment access | Registered Agent registry plus authenticated workload/Principal binding; H/I validate claims at ingress |
| `AdapterRef` | Registered Adapter application/instance identity that applies protocol/context operations | H owns Adapter registration and protocol capability identity; I owns authenticated Adapter Principal and trust/revocation | Adapter registry + issuer + tenant/security domain; instance identity distinct from application identity | Application identity stable; instance/session/capability epochs are separate, versioned and revocable | No implicit sharing of managed regions or Context across tenants/Scopes; explicit recipient/region authorization | Authenticated Adapter credential/session and H capability registry, bound to I Principal; payload adapter ID is only a claim |
| `ProducerRef` | Registered producer/application/workload identity permitted to emit a declared family of events or derived work | I owns trust/registration/revocation semantics; C declares telemetry producer assertion; E enforces ingress/work identity; D owns canonical producer-class/work admission ledger | Issuer + tenant/security domain + producer application/workload namespace | Stable producer identity; credential/workload instances and registration epochs rotate independently; revocation does not erase historical attribution | Producer must be explicitly registered per tenant/security domain and allowed Scope/event family; no cross-tenant reuse by string equality | Authenticated workload/session + I producer registry + H transport binding; compare C payload producer ID, never trust it alone |
| `EnvironmentRef` | Identity of a world/save/simulation/device-fleet or other authoritative external state domain; not merely a label | Environment authority/registry; I controls trusted binding; B defines semantic reference | Environment authority + tenant/project namespace + environment kind | Stable identity; environment version/revision is separate; closed/retired environments remain historical | Cross-environment references are disallowed by default; explicit bridge/mapping and authorization required; no cross-tenant reuse | Authoritative Environment registry or authenticated environment Adapter; free-text environment label is not trusted |

## 4. ActorRef semantics and principal binding

ActorRef is an attribution reference, not an authentication artifact. Its minimum semantic components are:

- `principal_ref: PrincipalRef` — authenticated security subject;
- `issuer_ref: IssuerRef` — issuer whose trust was validated;
- `authentication_context_ref: AuthenticationContextRef` — verifier-owned reference to the validated session/assertion, never raw credential;
- optional `agent_ref: AgentRef`, `adapter_ref: AdapterRef`, `producer_ref: ProducerRef`;
- optional `delegation_chain_ref: DelegationChainRef` and `acting_for_ref: PrincipalRef`;
- `authenticated_at` and an authentication-strength/profile reference where policy requires it.

The exact serialization is H-owned and OPEN. The above fields are semantic components, not a frozen envelope.

**Hard rule:** Payload-supplied ActorRef, PrincipalRef, AgentRef, AdapterRef, ProducerRef, issuer string, tenant, ScopeRef or EnvironmentRef is an untrusted claim. A receiving boundary MUST compare it with authenticated transport/session/workload identity and authoritative registries. A match does not replace credential verification. A mismatch fails closed and is audited. Caller-constructed ActorRef MUST NOT authenticate itself.

Delegation is not a Ref conversion. It is a separately verifiable, signed, bounded grant chain. Effective authority is the intersection of grantor authority, delegated action/resource, Scope, audience, purpose and time constraints. Cycles, missing parents, expired/revoked grants and unknown validity fail closed.

## 5. Scope semantics

### 5.1 ScopeRef is not Permission

- **ScopeRef** identifies an ownership namespace or applicability/data boundary.
- **Permission** is an I/Governance policy result for a Principal + action + resource + purpose + audience + resolved Scope binding + policy version/epoch.
- Scope resolution answers “which domain does this object/request belong to?”.
- Authorization answers “may this authenticated Principal perform this action on this resource now?”.
- An in-scope resource can still be denied. A Principal with permission in one Scope has no implied permission in another.

### 5.2 Ownership and applicability

Ownership Scope identifies custody/administrative boundary. Applicability Scope qualifies where a fact or asset is relevant/valid. Multiple ScopeRefs are a typed set with explicit roles; they are not a free-form union and do not broaden visibility.

A ScopeRef SHOULD carry or resolve: `scope_id`, `scope_kind`, `authority_ref`, `tenant/security_domain_ref`, `owner_ref`, optional `parent_scope_ref`, namespace, lifecycle status and optional exact Scope version. Display names are descriptive only.

### 5.3 Cross-Scope and cross-Environment references

1. Default deny. No implicit parent-to-child, child-to-parent, sibling, same-Agent, same-user or same-label access.
2. A cross-Scope relationship may be stored only when the domain relationship is valid; dereferencing it still requires authorization for each endpoint and any Evidence/Provenance independently.
3. Sharing is an explicit I-authorized grant with recipient, operations, purpose, audience, expiry/revocation and audit. It does not rewrite ownership Scope or union namespaces.
4. Environment-bound Event/Claim/Memory/Relation MUST carry a resolved EnvironmentRef/Environment Scope. Same Agent in two worlds does not make the worlds equivalent.
5. Cross-Environment references are rejected unless a registered bridge/mapping explicitly declares source and target EnvironmentRefs, permitted relation, provenance and authorization. No free-text label or inferred coordinate mapping is sufficient.
6. A reference may remain historically visible as metadata after Scope closure/revocation, but ordinary reads/writes/delivery are denied according to current policy.

### 5.4 Validation order

Authenticate and bind Principal/Actor/Producer/Adapter → resolve typed Scope/Environment refs → validate existence, kind, namespace, status and domain compatibility → validate delegation → evaluate current permission → recheck policy epoch/fence at final commit/disclosure boundary. Syntax validity alone never passes these steps.

## 6. Type conversion restrictions

- `PrincipalRef` MUST NOT be converted to `ActorRef` without a verifier-issued operation binding.
- `AgentRef` MUST NOT be treated as `PrincipalRef` unless I has an explicit registered Principal binding; logical Agent and security subject remain distinct.
- `AdapterRef` MUST NOT be treated as `AgentRef`; an Adapter can act for an Agent only through authenticated binding and authorized delegation/assignment.
- `ProducerRef` MUST NOT be inferred from `source_id`, `source_type`, `agent_id` or caller key; resolve via authenticated producer registry.
- `EnvironmentRef` MUST NOT be converted from a display label, URL, world name or coordinates without authoritative registry resolution.
- `ScopeRef` MUST NOT be converted into a grant, role, PermissionDecision or wildcard tenant.
- `ActorRef` MUST NOT be used as a credential, bearer token, proof of current authorization or replayable capability.
- A typed Ref cannot be weakened to a generic string at an API, storage, event, log or wire boundary if that loses type, issuer, namespace, version or trust provenance. A display string may be emitted only as non-authoritative presentation data.

## 7. Validation errors (logical vocabulary; wire mapping owned by H)

`REF_TYPE_UNKNOWN`, `REF_NAMESPACE_MISMATCH`, `REF_ISSUER_UNTRUSTED`, `REF_NOT_FOUND_OR_NOT_VISIBLE`, `REF_RETIRED`, `REF_SCOPE_INCOMPATIBLE`, `REF_ENVIRONMENT_MISMATCH`, `ACTOR_BINDING_MISMATCH`, `PRODUCER_NOT_REGISTERED`, `DELEGATION_INVALID`, `SCOPE_REQUIRED`, `CROSS_SCOPE_NOT_AUTHORIZED`.

Do not reveal protected object existence through error distinctions where I policy requires a disclosure-safe response.

## 8. Versioning and open issues

- Reference type discriminators and namespaces are registry-versioned. Unknown required type fails closed.
- Object identity and object version are distinct. A stable Ref does not imply a current version or current permission.
- Credential rotation, Adapter capability epoch, Producer registration epoch, PermissionEpoch, D ForgetFenceGeneration, CanonicalCommitCursor and Environment version are separate typed namespaces; never compare or substitute them.
- **OPEN:** exact common IssuerRef/NamespaceRef schema and federation model.
- **OPEN:** exact C telemetry field names and Agent/Adapter/Environment binding source; see Consumer Compatibility Matrix.
- **OPEN:** H wire representation, version negotiation and error encoding.
- **OPEN:** I formal registration/trust approval for Principal, Producer and Environment authorities.
- **OPEN:** D/E callable producer admission/registration operations and exact ref serialization.
- **OPEN:** cross-Scope algebra and Environment bridge governance.
- No implementation, cryptographic, runtime or conformance test is claimed by this document.
