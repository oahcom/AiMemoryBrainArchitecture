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

 
## 9. Phase 3.6 Registry Closure Addendum (B-owned semantics; dependent decisions remain Candidate)

- **Status:** CANDIDATE — domain typing and separation rules proposed by B; not a cross-module freeze and not I policy approval.
- **Baseline:** B branch HEAD `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`; prior registry blob `50252bce6a531c4087678c1e85b0cb8fe8348dd3`.
- **Decision boundary:** B defines type meaning and constraints. I alone approves issuer trust, principal registration, delegation, authorization, revocation and PermissionEpoch policy. H owns wire encoding and transport binding. C/D/E own their respective producer/consumer field semantics.

### 9.1 Complete typed-reference registry

| Type | Domain meaning | Namespace | Authority / issuer | Stability | Lifecycle | Cross-Scope reference | Payload self-declaration | Trusted validation boundary |
|---|---|---|---|---|---|---|---|---|
| `PrincipalRef` | Stable security subject (human, Agent workload, service, Adapter or recipient) | Issuer + tenant/security-domain + principal-kind namespace | I Principal registry; credential/assertion issuer is identified by IssuerRef | Stable opaque subject ID; never reassigned; credential rotation does not change subject identity | Active/disabled/revoked/retired status is I-authoritative; historical attribution remains addressable | No implicit cross-tenant alias; federation mapping must be explicit | May appear only as an untrusted claim/selector; cannot prove identity | H authenticates transport/session; I validates issuer, credential, audience, status and subject binding |
| `IssuerRef` | Typed identity of the authority that issued a credential, assertion or signed grant | Issuer registry namespace + trust domain | I owns trusted-issuer registry and trust policy; external issuer controls its own keys, not local trust admission | Stable issuer identity; key/credential rotation is a separate versioned security event | Trusted, suspended, compromised, retired or unknown states are I-authoritative; never reuse issuer ID | No transitive cross-Issuer trust; federation requires explicit I trust mapping | Payload issuer value is an untrusted claim, never a trust anchor | Verifier obtains issuer/key identity from protected credential metadata and resolves it against I trust registry |
| `ActorRef` | Immutable per-operation attribution binding an authenticated Principal and any verified acting/delegation context | Issuer + security domain + operation/attribution namespace | B owns semantic type; I validates Principal/issuer/delegation assertions; H supplies authenticated binding | Immutable per operation; distinct ActorRef for distinct operation/auth context; never credential | Historical attribution immutable; present usability depends on current I trust, revocation and authorization | No implicit crossing; operation-specific Scope and grant checks required | A payload may carry a claimed ActorRef for correlation, but cannot mint or authenticate it | Only verifier-issued binding assembled from protected auth context and resolved registries; D/E revalidate at protected boundary |
| `AgentRef` | Stable logical Agent identity, not runtime instance or security subject | Agent registry + tenant/security domain | Agent/deployment registry; I binds Agent to Principal; B defines ref semantics | Stable logical identity; config/version and instance are separate | Registered, active, suspended, retired; no ID reuse | Multiple scopes only through explicit registered association and authorization | Payload Agent ID is a selector/claim only | H/I validate authenticated workload assignment and Agent registry binding |
| `AdapterRef` | Registered protocol Adapter application identity; concrete instance is separately identified | Adapter registry + issuer/security domain | H owns Adapter/capability registry; I owns Adapter Principal trust and revocation | Application identity stable; instance/session/capability epoch are distinct | Registered, active, disabled, revoked, retired; instance replacement does not silently inherit identity | No implicit managed-region/Context sharing across scopes | Payload adapter ID is an untrusted claim | H authenticates Adapter transport/workload and resolves instance; I validates bound Principal and current authorization |
| `ProducerRef` | Registered producer/application/workload allowed to emit declared event/work families | Producer registry + issuer + tenant/security domain | I owns producer trust/registration/revocation; C declares telemetry claim; E enforces ingress; D owns per-work admission | Stable producer identity; workload instance and registration epoch rotate independently | Registered, active, suspended, revoked, retired; historical attribution retained | Explicit per-domain and allowed-Scope/event-family registration; no string-equality sharing | Payload producer_id/producer_claim is assertion only | H authenticates workload; I resolves ProducerIdentity; C/E compare claim; D separately checks work barrier |
| `ScopeRef` | Registered ownership or applicability/data boundary | Scope authority + tenant/security domain + Scope kind + opaque ID | B owns semantic type; authoritative registry and grant policy are I/Governance-owned | Stable opaque identity; descriptor/parent changes are versioned, not ID reuse | Active, suspended, closed or retired; historical reference may resolve subject to retention | Cross-Scope relation may be represented only with explicit compatible relation; dereference/action separately authorized | Payload ScopeRef may be an untrusted hint; never authoritative by itself | Resolve against authoritative Scope registry; validate kind, authority, owner, parent, status and binding; I authorizes action |
| `EnvironmentRef` | Registered external state domain (world/save/simulation/device fleet), not a label | Environment authority + tenant/project + environment-kind namespace | Environment registry/owner; I governs trust binding and cross-environment policy; B defines semantics | Stable environment identity; environment revision is separate | Active, suspended, closed or retired; historical identity not reused | Cross-environment references denied by default; bridge requires explicit mapping and authorization | Payload environment_id is an untrusted selector/claim | Authenticated Environment Adapter or authoritative registry resolves exact ref; I authorizes bridge/action |
| `RuntimeSessionRef` | One authenticated, bounded runtime/session instance used for correlation and operation binding | Issuer + runtime/Agent/Adapter instance + session namespace | H/I session authority; verifier/session service issues it; B defines reference semantics | Short-lived, unique, non-reusable; renewal creates a new ref | Created, active, expired, revoked, closed; no resurrection after expiry/revocation | No implicit cross-Scope use; session's bound Principal/Agent/Adapter and scope constraints must match | Payload session_id is correlation/claim only; never authentication | H verifies protected channel/session; I validates issuer, Principal binding, audience, expiry and revocation |

### 9.2 Identity, claim, credential and authentication result

These are four different layers and MUST NOT be collapsed:

1. **Reference:** typed address to an identity/resource. A reference does not authenticate its presenter and grants no access.
2. **Identity Claim:** untrusted statement such as payload `principal_ref`, `actor_ref`, `producer_id`, `agent_id`, `adapter_id`, `scope_ref`, `environment_id` or `session_id`. It is a selector/assertion to compare with trusted context.
3. **Authentication Credential:** verifier-consumed material (for example, credential/key-backed proof). It belongs to the authentication boundary and MUST NOT be embedded in a Ref or logged as a domain field.
4. **Authenticated Principal:** verifier result after credential, issuer, audience, validity, key and revocation checks. It is represented by a resolved PrincipalRef plus protected authentication-context evidence; the Ref alone is not that evidence.

ActorRef, AgentRef, AdapterRef and ProducerRef are never authentication credentials. A signed payload/digest may prove integrity under a key but does not establish that the key is trusted or authorized to assert the payload identity.

### 9.3 Serialization and declaration rules

- Every serialized reference preserves discriminator, issuer/authority, namespace/security-domain and opaque object identity. Exact wire field names and canonical encoding remain H-owned and OPEN.
- Unknown or incompatible discriminator, issuer/namespace mismatch, unresolved authority, retired identity or malformed version binding fails closed.
- Payload-supplied references remain claims until independently resolved. A payload cannot declare its own trusted issuer, Principal, Actor, Producer, Adapter, Scope, Environment or Runtime Session.
- A trusted boundary may accept payload references as selectors only after comparison with protected authenticated context and authoritative registries.
- No reference is a bearer token, capability, credential, permission, authorization receipt or PermissionEpoch.
- PermissionEpoch, ForgetFenceGeneration, ContextVersion, AdapterCapabilityEpoch, ProducerRegistrationEpoch and RuntimeSessionRef are distinct namespaces and MUST NOT be compared, cast or substituted.

### 9.4 Registry-wide unresolved items

- **OPEN / I:** issuer admission/federation, Principal registration, delegation eligibility, revocation effective point and PermissionEpoch policy.
- **OPEN / H:** exact wire type IDs, field names, canonical encoding, authentication-context and RuntimeSessionRef transport binding.
- **OPEN / C:** exact telemetry field profile and mandatory/optional identity fields.
- **OPEN / D/E:** exact domain field mapping, durable producer admission interface and ActorRef/ScopeRef validation receipts.
- **CANDIDATE / B:** the nine semantic definitions and fail-closed type separation in §9.1; this is not cross-module approval.


## 10. Phase 3.6.2 — B decision on the pinned C/G/H Applied Contract package

- Reviewed A package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA: `61d961c32138fd875069e8cbac4696bb031447c0`
- B disposition: **APPROVE WITH ENUMERATED EXCEPTIONS — B-owned reference semantics only**.

B confirms the package's use of distinct typed references and authority boundaries for PrincipalRef, IssuerRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef and EnvironmentRef; immutable ContextVersion/Delivery references remain G-owned values, while RuntimeSessionRef and CapabilityEpoch retain their H-owned identity/lifecycle. References are opaque typed selectors, not credentials, grants, permission decisions or proof of current authorization. Payload self-declaration never authenticates a Principal, Actor, Producer, Adapter, Scope or Environment. Cross-Scope and cross-Environment use requires explicit compatible relationships and current authorization; default is deny.

Enumerated exceptions:

1. B approves semantic meaning, namespace separation and validation order only. Exact wire discriminators, field names, canonical encoding and version negotiation remain H-owned and are not frozen by this decision.
2. I alone approves issuer trust, Principal/Producer/Environment registration, delegation, authorization, revocation and PermissionEpoch policy. B's decision is not I approval and does not lift I's GOVERNANCE-BLOCKED state.
3. The cross-Scope algebra, Environment bridge governance and formal registry authority/federation remain OPEN pending I/Governance decisions and authoritative registry evidence.
4. Consumer-specific C/D/E field production, D durable admission receipts and executable negative tests remain under their respective owners; no conformance execution is claimed.

**Decision consequence:** B's semantic portion of the exact A package is accepted with the exceptions above. B does not claim cross-owner schema freeze, I policy approval, runtime implementation or conformance. The prior Phase 3.6 Candidate dependent-authority items remain Candidate/Open; this decision only resolves B's semantic review of the pinned package.

## 11. Phase 3.6.4 — Prepared participant / prepared GID / native XID type separation

Exact inputs reviewed: Storage COC protocol §14 Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`; A integration mapping Blob `a71251704851cacd15f67faa985a5bd50057e92a`; H BMCP schema 1.1.1 candidate Blob `c0bbfc7611a8d88a39cee209831db32b62601fde`.

Add these distinct candidate domain types:

| Type | Issuer/owner | Semantic contract |
|---|---|---|
| `PreparedParticipantRef` | Storage | Stable opaque engine-neutral identity for one prepared participant; bound to immutable PublicationOperationId/RequestDigest/participant tuple and CanonicalAuthorityDBRef. |
| `PreparedTransactionGID` | Storage, PostgreSQL 18.7 profile | Client-chosen, preallocated, cluster/database-scoped GID used for PREPARE/lookup/retry/COMMIT PREPARED/ROLLBACK PREPARED. Never reused or rebound to another tuple. |
| `EngineNativeTransactionXIDRef` | Database engine, observed by Storage | Engine-assigned native transaction XID/handle observed after PREPARE. Evidence only; not preallocatable and never the participant identity. |
| `CanonicalAuthorityDBRef` | Storage registry | Opaque identity for the authoritative cluster/database boundary; distinct from PostgreSQL system_identifier, database OID, timeline and LSN. |

Type invariants:

1. `PreparedParticipantRef`, `PreparedTransactionGID`, `EngineNativeTransactionXIDRef`, `CanonicalAuthorityDBRef`, `PostgresSystemIdentifier`, `DatabaseOID`, `Timeline` and `LSN` are separate typed namespaces. No cast, arithmetic, lexical ordering or inferred equality across namespaces.
2. The participant ref and GID are immutable for the operation. Same tuple/digest retry is idempotent; same GID or participant ref rebound to a different tuple is CONFLICT.
3. The native XID is observed only after PREPARE and is bound as evidence to the stable participant/GID and original DB/timeline/LSN. It cannot authorize a COMMIT/ROLLBACK or replace the GID.
4. `PreparedParticipantRef` is engine-neutral; `PreparedTransactionGID` is PostgreSQL-profile-specific. Other engines require a separately named engine-specific prepared handle and native transaction identity.
5. COC, I, D, H and G position/epoch/proof types remain separate from all Storage transaction identifiers.
6. H 1.1.1 fields are wire encodings of these B semantic types, not new authority. Legacy 1.1.0 aliases are deprecated and do not change the type system.

Disposition: **CANDIDATE / B TYPE SEMANTICS ACCEPTED FOR THIS EXACT MAPPING**. This does not close ADR-001, approve I identity governance, freeze a canonical schema, select a production database or certify runtime conformance.
## 12. Phase 3.6.5 — Restore control-high-water proof types

Exact Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`; I proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`; D proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`; A integration acceptance Blob: `a80d90810425e94d752daa48c1b25dd78357e5aa`.

Add these candidate proof/reference types:

| Type | Authority | Meaning |
|---|---|---|
| `COCCommittedPrefixProofRef` | COC | Authenticated cluster/config/checkpoint/contiguous committed-prefix proof. |
| `IControlHighWaterProofRef` | I | One PolicyDomainRef's current PermissionEpoch/sequencer/revocation state plus global ProducerDomainInventoryEpoch/registry digest and relevant target seals. |
| `DForgetControlHighWaterProofRef` | D | Relevant ForgetOperation set, fence generation/request cutoff, producer registration high-water, lineage inventory and barrier terminal state. |
| `StorageParticipantLedgerProofRef` | Storage | Restored DB's complete prepared participant/GID/native-XID and terminal outcome ledger proof. |
| `RestoreReconciliationReceiptRef` | Storage | Storage's evidence that its restored snapshot reconciled against the exact owner proofs; state may be RECONCILED_BUT_FENCED. |
| `RestoreOperationRef` | Storage | One immutable restore attempt, backup, target timeline/LSN and reconciliation run. |

Non-substitution invariants:

1. `CoordinatorIndex`, I sequencer epoch/position, PermissionEpoch, ProducerDomainInventoryEpoch, D ForgetFenceGeneration, ProducerRegistrationHighWater, Storage GID/native XID/LSN and F IndexWatermark remain distinct namespaces.
2. IControlHighWaterProof is per PolicyDomainRef. Multiple proofs form a set; no cross-domain numeric max or comparison.
3. DForgetControlHighWaterProof is per relevant ForgetOperation/lineage. One operation's barrier cannot cover another operation.
4. Storage's RestoreReconciliationReceipt is not I authorization, D clearance, COC commit proof, Global Forget completion, physical-erasure evidence or permission to serve.
5. A proof reference is opaque; its content and signature are verified by the owning authority. A caller cannot mint or upgrade another owner's proof.
6. Missing, stale, gapped, audience-mismatched or unverifiable proof remains UNKNOWN and keeps restore fenced.

Disposition: **B ACCEPTS THE TYPE/REFERENCE SEPARATION AS CANDIDATE SEMANTICS ONLY.** This does not approve I governance, create a real inventory seal, close Global Forget, or authorize production restore.