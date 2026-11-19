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

## 13. Phase 3.6.6 — Storage v3 prepared-participant identity reconciliation

Exact source reviewed:
- Storage v3: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.md`, commit `db226387b0f2dede30a32a19a1478136b368cc1e`, Blob `4a60420d457f359780c568dce42b8bef000026ca`, §§15.1–15.7.
- Storage companion protocol: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`, §14.
- H schema 1.1.1 candidate: `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json`, Blob `c0bbfc7611a8d88a39cee209831db32b62601fde`.
- A Phase 3.6 final closure plan: `reviews/integration/phase-3.6-final-closure-plan.md`, Blob `0adca0f54ff6ee1e344949cb48334ff475fad247`.

**Disposition: ACCEPT WITH ENUMERATED AMENDMENTS — B DOMAIN-TYPE SEMANTICS ONLY; CANDIDATE MAPPING, NOT A CROSS-OWNER FREEZE.**

### 13.1 Canonical nominal type additions

The following types are now registered as candidate domain semantics. Their wire spelling remains H-owned; issuer, registry and authorization policy remain owned by the named authority.

| Nominal type | Authority | B semantic rule |
|---|---|---|
| `DatabaseIncarnationRef` | Storage authority registry | Non-reusable identity for one governed logical database incarnation under a `CanonicalAuthorityDBRef`; survives restart/failover of that same incarnation; clone, independent restore, copy, re-provision or authority migration creates a new value unless a separately authorized migration record preserves identity. |
| `PrepareAttemptRef` | Storage | Opaque identity for one attempt to prepare one participant; never reused for a later attempt. |
| `PrepareAttemptGeneration` | Storage | Strictly monotonic positive generation scoped to one `PreparedParticipantRef`; not comparable to any COC/I/D/H/G position or generation. |
| `ParticipantLedgerRef` | Storage | Opaque identity for the durable Storage participant ledger that records the immutable tuple and append-only attempt history. |
| `ParticipantLedgerVersion` | Storage | Strictly monotonic positive version within one `ParticipantLedgerRef`; not a global sequence and not an owner-authority cursor. |
| `ParticipantTupleDigest` | Storage | Algorithm/profile-tagged digest of the complete immutable participant tuple, including the DB incarnation, attempt and ledger binding. It is not a substitute for the tuple or its signed proof. |
| `PostgreSQLNativeXID` | PostgreSQL engine, observed by Storage | PostgreSQL-specific engine-assigned unsigned native XID observed after PREPARE. It is distinct from the client-chosen GID and from the engine-neutral `EngineNativeTransactionXIDRef`; neither is cast to the other. |
| `PostgreSQLSystemIdentifier` | PostgreSQL engine, observed by Storage | Cluster identity evidence; not a canonical authority or database-incarnation identity. |
| `PostgreSQLDatabaseOID` | PostgreSQL engine, observed by Storage | Database-local OID; never globally stable or sufficient to identify a database incarnation. |
| `PostgreSQLTimeline` | PostgreSQL engine, observed by Storage | Engine timeline metadata; not a causal-order cursor. |
| `PostgreSQLLSN` | PostgreSQL engine, observed by Storage | Canonical PostgreSQL WAL location; not an integer sequence comparable with COC/I/D positions. |

The existing registry names `PostgresSystemIdentifier`, `DatabaseOID`, `Timeline` and `LSN` are compatibility vocabulary for the corresponding PostgreSQL-specific nominal types above. The full PostgreSQL-prefixed names are canonical for the v3 adapter contract. This is a naming clarification, not permission to coerce these types or treat the underlying values as interchangeable.

### 13.2 Immutable participant tuple and lookup semantics

The Storage v3 tuple is accepted as a candidate semantic contract when it binds, at minimum:
- `PublicationOperationId` and `RequestDigest`;
- `PreparedParticipantRef`, `PrepareAttemptRef`, `PrepareAttemptGeneration`;
- `PreparedTransactionGID` and `PostgreSQLNativeXID` as separate values, with the latter observed only after PREPARE;
- `CanonicalAuthorityDBRef` and `DatabaseIncarnationRef`;
- `PostgreSQLSystemIdentifier`, `PostgreSQLDatabaseOID`, original `PostgreSQLTimeline` and `PostgreSQLLSN`;
- owner boundary, `CausalOrderDomainRef`, `PolicyDomainRef`, COC prepare-intent identity/digest;
- `ParticipantLedgerRef`, `ParticipantLedgerVersion` and `ParticipantTupleDigest`.

Authoritative participant lookup MUST use the complete key:
`(CanonicalAuthorityDBRef, DatabaseIncarnationRef, PreparedParticipantRef, PreparedTransactionGID)`.
GID-only, participant-only, system-identifier-only, OID-only or database-name-only lookup is insufficient. A matching GID found in another incarnation MUST NOT resolve the original participant.

A new prepare attempt is permitted only after the previous attempt has an authoritative append-only terminal attempt record and a new COC prepare-intent binding. A previous receipt cannot authorize a new attempt. Same complete tuple + same attempt is idempotent; any changed tuple field, attempt generation, ledger version, DB incarnation or digest under the same immutable identity is CONFLICT.

Original prepare timeline/LSN are immutable historical facts. Recovery timeline/LSN belong to append-only recovery observations and MUST NOT overwrite the original prepare coordinates.

### 13.3 Cross-owner naming and proof constraints

1. `PostgreSQLNativeXID` is the PostgreSQL-specific refinement; `EngineNativeTransactionXIDRef` remains an engine-neutral opaque reference for other adapters. A wire decoder MUST retain the engine discriminator and MUST NOT infer type from a matching string or number.
2. `PreparedTransactionGID` is the PostgreSQL client-chosen locator. It is not the PostgreSQL native XID and is not a universal database-engine handle.
3. `DatabaseIncarnationRef` is distinct from `CanonicalAuthorityDBRef`: the former identifies a governed incarnation; the latter identifies the canonical authority boundary.
4. `ParticipantLedgerRef` is distinct from `StorageParticipantLedgerProofRef`; the latter is evidence about a ledger, not the ledger identity.
5. The I terminal proof must bind the exact participant, GID, DB incarnation, attempt/generation, participant-ledger version, operation/request/tuple digests and owner-final-gate participant. B does not define or mint that I proof.
6. The H schema must encode the nominal types and requiredness without converting authority positions to integers or a synthetic global sequence.
7. Storage registry authority, signer trust, cryptographic profile, H canonicalization, I receipt consumption and production deployment remain outside B's approval.

### 13.4 Preservation and non-claims

- BIH36-JD-01..17 are unchanged.
- Fact/Claim ADR-001 remains **ADR-BLOCKED**; this type addition does not decide Fact/Claim semantics.
- No Storage registry authority is designated by B.
- No I36 governance approval, inventory seal, authorization permit, H wire freeze, production DB selection, runtime implementation or conformance PASS is claimed.
- The A G0–G10 plan remains the overall acceptance authority. This B type decision can support G4 technical reconciliation but does not close G5, G6, G7 or G10.


### 13.5 Companion protocol §14 reconciliation requirement

The exact Storage companion protocol §14, Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`, is older/narrower than Storage v3 §§15.1–15.7, Blob `4a60420d457f359780c568dce42b8bef000026ca`. §14 currently binds PreparedParticipantRef, PreparedTransactionGID, engine-native XID, CanonicalAuthorityDBRef, system identifier, target database/OID, original prepare timeline/LSN, participant digest, operation/request digest, owner boundary, CausalOrderDomainRef, PolicyDomainRef and COC prepare-intent position/digest. It does **not** enumerate DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version or ParticipantTupleDigest as separate required tuple fields.

B requires Storage to either:
1. amend §14 so its receipt, lookup and same-GID resolution rules use the complete v3 tuple and the exact lookup key in §13.2; or
2. explicitly mark §14 as superseded for PostgreSQL v3 and publish one unambiguous normative mapping.

Until then, the repository contains two non-identical prepared-participant field contracts. H's new schema candidate implements the v3 fields; it does not silently amend Storage's §14. No approval of the older incomplete §14 mapping is inferred.


## 14. Phase 3.6.7 — current Storage v3.2.3 / companion §14 exact-source reconciliation — 2026-11-18

This append-only addendum supersedes the active remediation wording in §13.5 for the current Storage Owner source readback. It does not rewrite the historical v3 review baseline.

### Exact current sources read

- Storage Owner branch HEAD at discovery: `268af57b099209b33835b663596e87d21bb9c22b`.
- Storage v3.2.3 normative design: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.3.md`, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- Current PostgreSQL companion protocol §14: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `dbc1dfd4c488c5d5e5a328388487d190984e8adc`.
- Storage v3.3.2 exact-version bundle manifest: Blob `5c614375e10698e4931d83deb57d20321445e068`; it pins the v3.2.3 body but remains **NOT JOINTLY ACCEPTED / NOT FROZEN**.

### B semantic re-evaluation

1. Current companion §14.1–14.4 explicitly binds `DatabaseIncarnationRef`, `PrepareAttemptRef` / `PrepareAttemptGeneration`, `ParticipantLedgerRef` / `ParticipantLedgerVersion`, and `ParticipantTupleDigest` as required typed values. It also defines the exact pre-PREPARE allocation sequence, signed PreparedParticipantReceipt binding, attempt replay/conflict rules, and append-only recovery observations.
2. Current Storage v3.2.3 §15.7 explicitly includes the DB incarnation, attempt/generation, participant-ledger ref/version, exact PreparedParticipantReceipt ref/digest, full tuple digest and owner-final-gate participant in the I proof binding. This closes the omission described by historical B-V3-04 at the current design-text level.
3. Current companion §14.2–14.3 uses the complete tuple and prohibits a generic `xid` field. This closes the historical §14 mismatch described by B-V3-06 at the current design-text level. The older companion Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` is a historical predecessor and is no longer the current Storage branch source.
4. Storage v3.2.3 also keeps `PreparedTransactionGID` distinct from `PostgreSQLNativeXID`, and its I outcome vocabulary rejects `ABORT_WON`; this is consistent with B's nominal type separation and I's owner-defined outcomes.

### Disposition and remaining boundary

- Historical B-V3-04 and B-V3-06: **RESOLVED AT CURRENT DOCUMENT-ALIGNMENT LEVEL** by the exact current Storage v3.2.3 and companion §14 sources above.
- B type semantics in §§11–13 remain unchanged; BIH36-JD-01..17 remain unchanged.
- The Storage v3.3.2 manifest does not list the current companion §14 Blob `dbc1dfd4c488c5d5e5a328388487d190984e8adc` in its exact artifact table. Storage/A must pin this exact companion Blob (or a successor) in the final version bundle and obtain affected-Owner exact-version review. A current source read is not a contract freeze.
- B does **not** accept the entire Storage v3.3.2 bundle, COC deployment, production implementation, crypto profile or runtime behavior.
- B runtime type tests remain **NOT RUN**; no B executable domain-model harness was found. Fact/Claim ADR-001 remains **ADR-BLOCKED**.

A must decide whether this evidence closes the corresponding G4 subfinding. It does not close G2/G3/G5/G7/G8/G9/G10.


---

## 15. BIH §9 currentness and status-scope reconciliation — B Owner addendum (2026-11-19)

**Decision ID:** `B-OWNER-BIH-REGISTRY-2026-11-19-001`  
**Disposition:** DECIDED — this addendum decides the B Registry's currentness vocabulary, authority boundaries and status-scope interpretation only. It does not decide another Owner's fields, policy, schema, deployment or runtime behavior.

### 15.1 Exact source pin and version evolution

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Owner branch: `session-b-domain-model-phase3`
- Source commit before this addendum: `4ba22c899469ab0f5df9e6f965a1ba1253625733`
- Registry path: `02-domain-model/typed-reference-registry.md`
- Registry Blob before this addendum: `d13e7acf5348bccf58c28882a9400aaaa7a17766`

Historical pins are retained, not rewritten:

1. §9's original baseline pin is B HEAD `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` / prior Registry Blob `50252bce6a531c4087678c1e85b0cb8fe8348dd3`.
2. A's earlier joint BIH package pinned Registry Blob `af23ca9e019ab067a5f8ff62da902d4a419db3f3` (the 181-line historical snapshot).
3. The later B Registry readback is Blob `d13e7acf5348bccf58c28882a9400aaaa7a17766` (355 lines at the source commit above), containing the expanded §9 and subsequent §§10–14. The historical `af23...` object remains valid as historical evidence, not current source.
4. This addendum is append-only. It does not delete, rewrite or silently supersede any prior source pin or decision.

### 15.2 Currentness is not lifecycle status, permission or freshness-by-clock

The Registry uses the following **currentness result vocabulary** for an attempted authoritative resolution of one exact typed identity:

| Result | Definition | Required handling |
|---|---|---|
| `CURRENT` | The exact typed reference resolves in its responsible authority's current registry/state, with authenticated source evidence and demonstrable continuity/no unresolved gap for the relevant namespace or epoch. | May proceed to the separate lifecycle, trust, Scope and authorization checks. `CURRENT` alone is never ALLOW. |
| `STALE` | The evidence is known to be superseded, invalidated, behind a known authoritative version/epoch, or inconsistent with a later authoritative event. | Reject for protected use; refresh from the authority. |
| `UNKNOWN` | The authority is unavailable, evidence is missing/ambiguous, a gap or rollback cannot be excluded, or continuity cannot be established. | Fail closed for protected operations; do not infer ACTIVE, ALLOW or success. |
| `NOT VERIFIED` | No exact-source verification record, reproducible validation or attributable evidence has been supplied for the claim being made. | Keep the claim unverified; do not convert it to CURRENT or PASS. |

These are **evidence/currentness results**, not identity lifecycle states. An identity whose authoritative lifecycle status is `REVOKED`, `DISABLED` or `RETIRED` may still have a `CURRENT` read result: the read is current precisely because it authoritatively reports that status. Currentness does not mean usable.

Currentness MUST be established from the authority named below, using its authenticated registry read, signed/current state or owner-defined monotonic version/epoch and continuity evidence. A wall-clock timestamp, `updated_at`, local cache age, local receipt time, H transport sequence or consumer's last-seen value is not authoritative currentness evidence. Cache TTL never extends identity validity. In the Phase 3.6 I baseline, cached ALLOW and offline/stale authorization continuation without current I proof are prohibited.

### 15.3 Identity lifecycle vocabulary and authoritative sources

There is no single universal lifecycle enum. The following status sets are type-scoped; a status from one row MUST NOT be copied to another type.

| Identity type | Lifecycle/status vocabulary in scope | Authority for status/currentness | Boundary and non-substitution |
|---|---|---|---|
| `IssuerRef` | `TRUSTED`, `SUSPENDED`, `COMPROMISED`, `RETIRED`, `UNKNOWN` | I Trusted Issuer Registry and its trust/key decision record; external key events are inputs, not local trust admission. | I owns local trust admission, rotation/compromise/revocation policy. A valid signature or timestamp does not establish trusted issuer status. |
| `PrincipalRef` | `ACTIVE`, `DISABLED`, `REVOKED`, `RETIRED`, `UNKNOWN` | I Principal Registry, resolved inside the authenticated IssuerRef and namespace. | H authenticates the protected transport/session; H does not replace I's Principal status or authorization decision. |
| `ActorRef` | Immutable per-operation attribution; no independently mutable lifecycle enum. | Verifier-produced operation binding from protected H context plus I-resolved Principal/Issuer/delegation evidence. | Historical attribution is not erased by later revocation. Present use must revalidate linked trust, delegation and permission; ActorRef is not a credential or authorization. |
| `AgentRef` | Registry-defined `REGISTERED` / `ACTIVE` / `SUSPENDED` / `RETIRED` outcomes; unresolved is `UNKNOWN`. | Authoritative Agent/deployment registry plus I's binding of the workload Principal where applicable. | B defines reference semantics; it does not designate or operate the Agent deployment registry. AgentRef is not PrincipalRef or a runtime instance. |
| `AdapterRef` | `REGISTERED`, `ACTIVE`, `DISABLED`, `REVOKED`, `RETIRED`, `UNKNOWN`. | H Adapter/application/instance and capability registry, combined with I's authenticated Adapter Principal/trust status. | H owns Adapter protocol/capability identity; I owns Principal trust and authorization. CapabilityEpoch is separate from identity. |
| `ProducerRef` | `REGISTERED`, `ACTIVE`, `SUSPENDED`, `REVOKED`, `RETIRED`, `UNKNOWN`. | I Producer registration/trust registry plus authenticated H workload binding; D's work-admission ledger is an additional D-local gate. | C payload producer fields are claims. D ProducerRegistrationHighWater/WorkItemBarrier does not replace I's Producer registry or ProducerDomainInventoryEpoch. |
| `ScopeRef` | `ACTIVE`, `SUSPENDED`, `CLOSED`, `RETIRED`, `UNKNOWN`. | Authoritative Scope registry for identity/lifecycle; I owns grants, authorization and PermissionEpoch. | B defines Scope meaning. Formal Scope Registry authority/designation and governance activation remain open; absent authoritative registry evidence, currentness is UNKNOWN. ScopeRef is not permission. |
| `EnvironmentRef` | `ACTIVE`, `SUSPENDED`, `CLOSED`, `RETIRED`, `UNKNOWN`. | A formally designated Environment Registry Authority; I governs trust binding and cross-environment authorization. | No formal Environment Registry Authority designation is evidenced in the current I register. Until designation and authoritative evidence exist, EnvironmentRef currentness is UNKNOWN/NOT VERIFIED; labels, URLs and coordinates are not substitutes. |
| `RuntimeSessionRef` | `CREATED`, `ACTIVE`, `EXPIRED`, `REVOKED`, `CLOSED`, `UNKNOWN`. | H/I verifier or session authority, protected channel/session state and I revocation state. | Payload session ID and local clock are not proof. Reconnect requires a newly authenticated/current binding; old-session ACK is historical only. |

### 15.4 Events that invalidate or require revalidation

A currentness result MUST be re-established after any applicable authoritative event, including:

- issuer admission, key/credential rotation, suspension, compromise, retirement or trust-policy change;
- Principal registration/binding change, disablement, revocation or retirement;
- delegation grant, amendment, expiry, parent-chain change or revocation;
- Agent registration/deployment/Principal-binding change;
- Adapter registration, instance replacement, capability change, disablement or revocation;
- Producer registration, workload/epoch change, suspension, revocation or retirement;
- Scope creation, closure, retirement, owner/parent/descriptor change or cross-Scope grant change;
- Environment registration/revision, closure/retirement, bridge/trust change or registry-authority change;
- RuntimeSession expiry, revocation, reconnect, channel-binding change or verifier invalidation;
- I policy change or revocation event advancing the affected PolicyDomain's PermissionEpoch.

A consumer MUST NOT infer that an event is irrelevant merely because the reference string did not change. Identity, version, credential, session, capability, Scope, Environment and PermissionEpoch are separate namespaces.

### 15.5 Evidence loss, unavailable authority and continuity failure

If the responsible source cannot be reached, the exact reference cannot be resolved, a required signature/attestation is absent, a registry version or epoch has a gap, a rollback/fork cannot be excluded, or the evidence chain cannot prove continuity, the result is `UNKNOWN` (and the claim remains `NOT VERIFIED` until evidence is supplied). Protected reads, writes, publication, delivery and other sensitive operations MUST pause, deny or quarantine according to the owning boundary. No fallback to timestamp, local cache, payload self-declaration, prior successful lookup or another Owner's cursor is permitted.

I's PermissionEpoch currentness is a separate authorization check: I is the sole logical authority; values are comparable only within their PolicyDomain; consumers must obtain authoritative currentness at each protected boundary. It is not an identity status and cannot be substituted for D ForgetFenceGeneration, ProducerRegistrationHighWater, H CapabilityEpoch or any other owner-local sequence.

### 15.6 Status-scope reconciliation — authoritative layers

| Status layer | Vocabulary / result | What it applies to | Authority and effect |
|---|---|---|---|
| Identity lifecycle | Type-specific values in §15.3 | One identity record in its own namespace | The named identity/registry authority only. Does not grant access. |
| Identity currentness | `CURRENT` / `STALE` / `UNKNOWN` / `NOT VERIFIED` | One exact typed-reference resolution and its evidence chain | The relevant authority; a current `REVOKED` result is still unusable. |
| Design maturity | `CANDIDATE` / `DECIDED` | A proposal or exact semantic decision within a named Owner/delegated authority scope | Candidate is not accepted. Decided is limited to the exact semantic subject and authority that made the decision. |
| Consumer acceptance | `OPEN` / `ACCEPTED` / `ACCEPTED WITH CONDITIONS` / `REJECTED` | One exact artifact/version at one named consumer's own boundary | Only that consumer Owner can accept its field path/enforcement boundary. Acceptance does not propagate to other consumers. |
| Wire/schema | `CANDIDATE` / `FROZEN` (or explicitly `NOT FROZEN`) | Exact protocol schema, field names, encoding, requiredness and version negotiation | H alone decides H-owned wire/schema freeze. Design acceptance is not freeze. |
| Governance | `GOVERNANCE-BLOCKED` / `APPROVED` (with exact effective version and scope) | I-owned trust, registration, delegation, grants, revocation, PermissionEpoch and cross-boundary policy | Only the authorized external governance body can approve; an Owner proposal or delegated technical decision is not approval. |
| Runtime/conformance | `NOT VERIFIED` / `NOT RUN` / evidence-backed `PASS` or `FAIL` | A named implementation/build, operation boundary and reproducible test or operational proof | Each implementation/consumer Owner supplies evidence. Document agreement is not runtime conformance. |
| Finding tracking | `OPEN` / `BLOCKED` / `REMEDIATION ACCEPTED` / `CLOSED` | The Finding record in the authoritative ledger | A Integration controls ledger disposition; these are not identity, consumer, schema or governance statuses. |

No status is inherited across layers. In particular: `DECIDED ≠ ACCEPTED`; `ACCEPTED ≠ FROZEN`; `FROZEN ≠ GOVERNANCE APPROVED`; `GOVERNANCE APPROVED ≠ RUNTIME CONFORMANT`; `CURRENT ≠ ACTIVE`; and `NOT VERIFIED` is not a pass.

### 15.7 Candidate / decided / accepted / frozen / governance / runtime boundary

1. **Delegated BIH technical baseline:** BIH36-JD-01..17 are recorded as a delegated joint technical baseline, technically DECIDED within that bounded B/I/H design scope. This is not a claim of separate human signatures, external governance approval, blanket consumer sign-off, production schema freeze or runtime conformance.
2. **Registry §9 Candidate addendum:** the detailed nine-type §9 closure addendum remains labelled CANDIDATE as a composite dependent-authority package. Its presence in this Registry and the later BIH baseline do not automatically promote every row, consumer field path or authority dependency.
3. **B-owned semantic decisions:** B's exact formal confirmation (Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`) approves the B semantic mapping of ActorRef, ScopeRef and EnvironmentRef, including role-preserving distinctions. It expressly does not freeze wire fields, approve I policy, designate an external registry authority, approve C telemetry schema or sign for other consumers. Other detailed §9 type clauses remain bounded by their own exact B decision evidence; no blanket promotion is made here.
4. **Consumer-specific acceptance:** D and E have design-level acceptance records for their own canonical-mutation and compiler-publication boundaries; H has design-level acceptance for its BMCP authentication/protected-message/ACK/reconnect boundary; Storage has design-level acceptance for its durable publication/visibility boundary. These records are exact-owner, design-level evidence only. C's telemetry semantic boundaries are DECIDED, but its event profile remains CANDIDATE and H/I-dependent identity binding remains OPEN; no C BIH consumer acceptance is inferred. F and G remain OPEN in A's BIH consumer matrix absent their own exact acceptance records. No consumer's acceptance is shared automatically with another consumer.
5. **H wire/schema freeze:** NOT FROZEN. H owns wire names, canonicalization, requiredness, protocol versioning and schema freeze. H's BIH design acceptance and candidate schema artifacts do not establish production freeze or interoperability.
6. **I governance approval:** GOVERNANCE-BLOCKED. I36-GOV-01..10 remain blocked/not approved absent the required authorized approver, exact policy hash, authority basis, scope/jurisdiction, effective version and durable approval record.
7. **Runtime conformance:** NOT VERIFIED. I36/H36 cases are specified but NOT RUN in the cited baseline; D/E/H/Storage records explicitly limit themselves to design acceptance and do not claim runtime implementation/conformance.

### 15.8 Unresolved items, accountable Owners and return evidence

| Unresolved item | Accountable Owner(s) | Independent acceptance required | Return carrier | Required evidence |
|---|---|---|---|---|
| Formal I issuer/Principal/Producer trust, delegation, revocation and PermissionEpoch policy; I36-GOV-01..10 | I + authorized Security/Identity/Architecture Governance | Authorized governance body; each protected-boundary consumer validates I output | I governance decision register → A Integration → existing Issue #43 | Named authorized approver, decision ID, exact policy text/hash, authority/delegation basis, scope/jurisdiction, effective version/time, expiry/revocation and durable signed record |
| Formal Scope Registry authority, namespace and lifecycle/continuity source | I + B (semantics); designated Scope authority | I governance and each consumer using Scope | I registry/governance record → B Registry → A / #43 | Named authority, exact registry ref/version, lifecycle vocabulary, authenticated current read and gap/rollback evidence |
| Environment Registry Authority designation and EnvironmentRef currentness | I + Environment owner; B only for type semantics | I and each environment-dependent consumer | I governance register + Environment authority record → B Registry → A / #43 | Named registry authority, namespace, status/version source, trust binding, bridge policy and continuity proof |
| C telemetry identity/producer/Agent/Adapter/Environment field paths and requiredness | C; H/I/B for dependent bindings | C Owner; H for wire; I for trust policy | C telemetry contract + H schema/requiredness record → A / #43 | Exact field path, type, requiredness, authenticated source, negative cases and exact version pins |
| D canonical-memory field paths, role mapping and admission/receipt enforcement | D | D Owner; I independently for policy/receipt; H if wire consumed | D consumer contract → A / #43 | Exact schema/path, owner decision, receipt binding and negative/race evidence; runtime claim only with reproducible implementation tests |
| E ExtractionIR/ingress/publication field paths and final gate | E | E Owner; I policy and Storage visibility remain independent | E consumer contract → A / #43 | Exact field paths/requiredness, producer binding, lineage, final PermissionEpoch/fence checks and reproducible evidence |
| F retrieval/index/cache identity and pre-disclosure acceptance | F | F Owner; I authorization; B semantics | F consumer contract → A / #43 | Exact field mapping, cache/rebuild/currentness behavior, negative tests and final-boundary proof |
| G Context/Delivery/Applied identity and recipient acceptance | G | G Owner; H wire and I policy independently | G consumer contract → A / #43 | Exact ContextVersion/Delivery/session/Scope/epoch mapping, replay/reconnect behavior and Applied evidence |
| H production wire/schema freeze and interoperable implementation | H | H Owner; affected consumers accept exact same version | H schema/validator/CI record → A / #43 | Exact schema/IDL and commit/Blob, canonicalization, requiredness, version negotiation, generated bindings, interoperability and authorized freeze record |
| Runtime conformance across consumers | Each implementation/consumer Owner; I for policy service evidence | Each affected consumer Owner and A integration review | Owner implementation/test evidence → A / #43 ledger | Exact build/commit, test commands/environment, raw logs, CI run/job where applicable, protected-boundary negative/race/recovery evidence; no document-only substitution |
| Fact/Claim canonical identity ADR-001 | B proposes; authorized Architecture Governance decides; affected consumers adopt separately | Governance plus each affected consumer | ADR-001 decision record → A / existing governance tracking | Formal decision authority, approved option/text/hash and exact consumer migrations; BIH identity decisions do not resolve this ADR |

### 15.9 Non-claims and A Integration handoff

This addendum is an authoritative B Registry reconciliation, not a rewrite of the BIH baseline. It does not approve another Owner's fields, designate an external registry authority, change I36 governance status, freeze H schema, close a consumer acceptance, prove runtime conformance or close F-43-06B. The A Integration Owner must independently re-read the exact resulting commit and Blob, reconcile its ledger/source pins and decide the Finding disposition. Until then F-43-06B remains OPEN.

---

## 16. BIH §9 当前性与状态范围权威对账 — B Owner 增补（2026-11-19）

**Decision ID：** `B-OWNER-BIH-REGISTRY-2026-11-19-001`  
**裁定范围：** 仅决定 B Registry 的 currentness 词汇、权威边界和状态适用范围；不代替其他 Owner 决定字段、策略、Schema、部署或 Runtime 行为。

### 16.1 精确来源 Pin 与版本演进

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- Owner 分支：`session-b-domain-model-phase3`
- 本次增补前 commit：`4ba22c899469ab0f5df9e6f965a1ba1253625733`
- Registry 路径：`02-domain-model/typed-reference-registry.md`
- 本次增补前 Blob：`d13e7acf5348bccf58c28882a9400aaaa7a17766`

历史 Pin 保留，不覆盖：

1. §9 原始基线：B HEAD `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` / Registry 旧 Blob `50252bce6a531c4087678c1e85b0cb8fe8348dd3`。
2. A 早期联合 BIH 包引用的 Registry Blob：`af23ca9e019ab067a5f8ff62da902d4a419db3f3`，属于 181 行历史快照。
3. 后续 B Registry 精确读回：Blob `d13e7acf5348bccf58c28882a9400aaaa7a17766`，在上述 commit 下为 355 行，包含扩展 §9 及后续 §§10–14。旧 `af23...` 仍是有效历史对象，但不是当前文件。
4. 本增补采用追加方式，不删除、改写或静默取代任何历史 source pin 或决定。

### 16.2 Currentness 不等于生命周期状态、Permission 或时钟新鲜度

对一个精确 typed identity 的权威解析，采用以下 **currentness 结果词汇**：

| 结果 | 定义 | 必须处理方式 |
|---|---|---|
| `CURRENT` | 精确 typed reference 在责任权威的当前 Registry/状态中解析成功，且有认证来源证据，并能证明相关 namespace/epoch 的连续性、无未解决缺口。 | 之后仍须单独检查生命周期、信任、Scope 和授权；`CURRENT` 本身绝不是 ALLOW。 |
| `STALE` | 证据已被取代、失效、落后于已知权威版本/epoch，或与后续权威事件冲突。 | 保护性使用必须拒绝；从权威来源刷新。 |
| `UNKNOWN` | 权威源不可用、证据缺失/歧义、存在无法排除的 gap/rollback，或无法证明连续性。 | 保护性操作 fail closed；不得推断 ACTIVE、ALLOW 或成功。 |
| `NOT VERIFIED` | 没有针对该主张的精确来源核验记录、可复现验证或可归属证据。 | 保持未验证；不得转换为 CURRENT 或 PASS。 |

这些是**证据/当前性结果**，不是 identity lifecycle 状态。权威记录为 `REVOKED`、`DISABLED` 或 `RETIRED` 的 identity，其读取结果仍可能是 `CURRENT`：因为权威当前状态恰好报告了该状态。Currentness 不等于可用。

Currentness 必须来自下文指定权威的认证 Registry read、签名/当前状态，或 Owner 定义的单调版本/epoch 与连续性证据。墙上时钟时间戳、`updated_at`、本地缓存年龄、本地 receipt 时间、H transport sequence、消费者 last-seen 值均不是权威 currentness 证据。Cache TTL 不延长 identity 有效性。Phase 3.6 I 基线禁止在缺少 I 当前性证明时使用 cached ALLOW 或离线/过期授权继续执行。

### 16.3 Identity 生命周期词汇与权威来源

不存在可通用于所有类型的生命周期 enum。以下状态集按类型限定，不得跨行复制：

| Identity 类型 | 适用生命周期/状态词汇 | 状态/currentness 权威 | 边界与禁止替代 |
|---|---|---|---|
| `IssuerRef` | `TRUSTED`、`SUSPENDED`、`COMPROMISED`、`RETIRED`、`UNKNOWN` | I Trusted Issuer Registry 及其 trust/key 决议记录；外部 key 事件只是输入，不是本地信任准入。 | I 拥有本地信任准入、轮换/失陷/撤销策略。签名有效或时间戳新不代表 Issuer 可信。 |
| `PrincipalRef` | `ACTIVE`、`DISABLED`、`REVOKED`、`RETIRED`、`UNKNOWN` | I Principal Registry，在已认证 IssuerRef 与 namespace 内解析。 | H 认证受保护 transport/session；H 不替代 I 的 Principal 状态或授权决策。 |
| `ActorRef` | 每操作不可变 attribution；没有独立可变生命周期 enum。 | 由受保护 H context 与 I 解析的 Principal/Issuer/delegation 证据组成的 verifier-produced operation binding。 | 后续撤销不抹除历史 attribution。当前使用必须重验关联 trust、delegation 和 permission；ActorRef 不是 credential 或授权。 |
| `AgentRef` | Registry 定义的 `REGISTERED` / `ACTIVE` / `SUSPENDED` / `RETIRED`；无法解析为 `UNKNOWN`。 | 权威 Agent/deployment Registry，以及适用时 I 对 workload Principal 的绑定。 | B 定义引用语义，不指定或运营 Agent deployment Registry。AgentRef 不等于 PrincipalRef 或 runtime instance。 |
| `AdapterRef` | `REGISTERED`、`ACTIVE`、`DISABLED`、`REVOKED`、`RETIRED`、`UNKNOWN`。 | H Adapter/application/instance 与 capability Registry，结合 I 对已认证 Adapter Principal 的 trust 状态。 | H 拥有 Adapter protocol/capability identity；I 拥有 Principal trust 与 authorization。CapabilityEpoch 与 identity 分离。 |
| `ProducerRef` | `REGISTERED`、`ACTIVE`、`SUSPENDED`、`REVOKED`、`RETIRED`、`UNKNOWN`。 | I Producer registration/trust Registry，加上 H authenticated workload binding；D work-admission ledger 是额外的 D-local gate。 | C payload producer 字段只是 claim。D ProducerRegistrationHighWater/WorkItemBarrier 不替代 I Producer Registry 或 ProducerDomainInventoryEpoch。 |
| `ScopeRef` | `ACTIVE`、`SUSPENDED`、`CLOSED`、`RETIRED`、`UNKNOWN`。 | identity/lifecycle 由权威 Scope Registry；I 拥有 grants、authorization 与 PermissionEpoch。 | B 定义 Scope 含义。正式 Scope Registry authority/designation 与治理启用仍 OPEN；缺少权威 Registry 证据时 currentness 为 UNKNOWN。ScopeRef 不是 permission。 |
| `EnvironmentRef` | `ACTIVE`、`SUSPENDED`、`CLOSED`、`RETIRED`、`UNKNOWN`。 | 正式指定的 Environment Registry Authority；I 管理 trust binding 与跨环境授权。 | 当前 I register 未证明已正式指定 Environment Registry Authority。在指定并提供权威证据前，EnvironmentRef currentness 为 UNKNOWN/NOT VERIFIED；label、URL、坐标不能替代。 |
| `RuntimeSessionRef` | `CREATED`、`ACTIVE`、`EXPIRED`、`REVOKED`、`CLOSED`、`UNKNOWN`。 | H/I verifier 或 session authority、受保护 channel/session 状态与 I revocation 状态。 | payload session ID 和本地时钟不是证明。Reconnect 必须重新认证/绑定；旧 session ACK 仅为历史证据。 |

### 16.4 导致 currentness 失效或必须重验的事件

发生任何适用权威事件后，必须重新建立 currentness，包括：

- Issuer 准入、key/credential 轮换、suspend、compromise、retire 或 trust-policy 变化；
- Principal 注册/绑定变化、disable、revoke 或 retire；
- delegation grant、修改、到期、父链变化或撤销；
- Agent 注册、deployment 或 Principal binding 变化；
- Adapter 注册、实例替换、capability 变化、disable 或 revoke；
- Producer 注册、workload/epoch 变化、suspend、revoke 或 retire；
- Scope 创建、关闭、retire、owner/parent/descriptor 变化或跨 Scope grant 变化；
- Environment 注册/版本、关闭/retire、bridge/trust 变化或 Registry authority 变化；
- RuntimeSession 到期、撤销、reconnect、channel-binding 变化或 verifier invalidation；
- I policy 变化或 revocation event 推进受影响 PolicyDomain 的 PermissionEpoch。

消费者不得仅因 reference 字符串未变化就推断事件无关。Identity、version、credential、session、capability、Scope、Environment 与 PermissionEpoch 是不同 namespace。

### 16.5 证据缺失、权威源不可用与连续性无法证明

责任来源不可达、精确 reference 无法解析、必需签名/attestation 缺失、Registry version/epoch 存在 gap、无法排除 rollback/fork，或证据链无法证明连续性时，结果为 `UNKNOWN`（在证据补齐前，该主张同时保持 `NOT VERIFIED`）。受保护读取、写入、发布、交付及其他敏感操作必须按所属边界 pause、deny 或 quarantine。不得回退到时间戳、本地缓存、payload 自我声明、历史成功查询或其他 Owner 的 cursor。

I PermissionEpoch currentness 是独立授权检查：I 是唯一逻辑权威；值只在自己的 PolicyDomain 内可比较；消费者必须在每个受保护边界取得权威当前性。它不是 identity status，也不能替代 D ForgetFenceGeneration、ProducerRegistrationHighWater、H CapabilityEpoch 或任何其他 Owner-local sequence。

### 16.6 Status-scope 对账 — 权威层次

| 状态层 | 词汇/结果 | 适用对象 | 权威与效力 |
|---|---|---|---|
| Identity lifecycle | §16.3 的按类型状态 | 自身 namespace 内的一条 identity 记录 | 仅对应 identity/Registry authority；不授予访问权。 |
| Identity currentness | `CURRENT` / `STALE` / `UNKNOWN` / `NOT VERIFIED` | 一个精确 typed-reference 解析及其证据链 | 对应权威；当前读到 `REVOKED` 仍不可用。 |
| Design maturity | `CANDIDATE` / `DECIDED` | 提案或具名 Owner/委托权威范围内的精确语义决定 | Candidate 不等于 accepted；Decided 仅限作出决定的精确语义对象与权限范围。 |
| Consumer acceptance | `OPEN` / `ACCEPTED` / `ACCEPTED WITH CONDITIONS` / `REJECTED` | 某个具名 consumer 对一个精确 artifact/version 的自有边界 | 仅该 consumer Owner 能接受其 field path/enforcement boundary；不自动传递给其他 consumer。 |
| Wire/schema | `CANDIDATE` / `FROZEN`（或明确 `NOT FROZEN`） | 精确 protocol schema、field names、encoding、requiredness、version negotiation | 仅 H 决定 H-owned wire/schema freeze；设计接受不是 freeze。 |
| Governance | `GOVERNANCE-BLOCKED` / `APPROVED`（须附精确 effective version 与 scope） | I-owned trust、registration、delegation、grant、revocation、PermissionEpoch 与跨边界 policy | 只有获授权的外部治理机构可批准；Owner proposal 或 delegated technical decision 不是批准。 |
| Runtime/conformance | `NOT VERIFIED` / `NOT RUN` / 有证据的 `PASS` 或 `FAIL` | 指定 implementation/build、operation boundary 与可复现测试或运行证明 | 每个 implementation/consumer Owner 提供证据；文档一致不等于 runtime conformance。 |
| Finding tracking | `OPEN` / `BLOCKED` / `REMEDIATION ACCEPTED` / `CLOSED` | 权威 ledger 中的一条 Finding | A Integration 管理 ledger disposition；这些不是 identity、consumer、schema 或 governance 状态。 |

各层状态不得继承。尤其：`DECIDED ≠ ACCEPTED`；`ACCEPTED ≠ FROZEN`；`FROZEN ≠ GOVERNANCE APPROVED`；`GOVERNANCE APPROVED ≠ RUNTIME CONFORMANT`；`CURRENT ≠ ACTIVE`；`NOT VERIFIED` 不等于 PASS。

### 16.7 Candidate / decided / accepted / frozen / governance / runtime 边界

1. **委托 BIH 技术基线：** BIH36-JD-01..17 被记录为委托联合技术基线，在该有限 B/I/H 设计范围内为 TECHNICALLY DECIDED。这不声称存在分别的人类签名、外部治理批准、所有消费者签收、生产 Schema freeze 或 runtime conformance。
2. **Registry §9 Candidate addendum：** 详细的九类型 §9 closure addendum 作为一个依赖其他权威的整体仍为 CANDIDATE。它存在于 Registry 中、以及后续 BIH baseline 的形成，都不会自动提升每一行、consumer field path 或 authority dependency。
3. **B-owned semantic decisions：** B 的精确正式确认（Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`）批准 ActorRef、ScopeRef、EnvironmentRef 的 B-owned semantic mapping，包括保留角色的区分。该决定明确不冻结 wire fields、不批准 I policy、不指定外部 Registry authority、不批准 C telemetry schema，也不代表其他 consumer 签收。§9 其他详细 type clauses 仍受各自精确 B 决策证据约束；本增补不作整体提升。
4. **Consumer-specific acceptance：** D、E 已对各自 canonical-mutation 与 compiler-publication 边界记录 design-level acceptance；H 已对自身 BMCP authentication/protected-message/ACK/reconnect 边界记录 design-level acceptance；Storage 已对自身 durable publication/visibility 边界记录 design-level acceptance。这些只是在精确 Owner 范围内的设计证据。C telemetry semantic boundaries 为 DECIDED，但 event profile 仍 CANDIDATE、H/I-dependent identity binding 仍 OPEN；不推断 C 已完成 BIH consumer acceptance。A 的 BIH consumer matrix 中 F、G 在缺少各自精确 acceptance 记录时仍 OPEN。任一 consumer 的 acceptance 不自动共享给其他 consumer。
5. **H wire/schema freeze：** NOT FROZEN。H 拥有 wire names、canonicalization、requiredness、protocol versioning 与 schema freeze。H 的 BIH design acceptance 和 candidate schema 工件不构成生产 freeze 或 interoperability 证明。
6. **I governance approval：** GOVERNANCE-BLOCKED。I36-GOV-01..10 在缺少获授权 approver、精确 policy hash、authority basis、scope/jurisdiction、effective version 与持久化批准记录前均保持 blocked/not approved。
7. **Runtime conformance：** NOT VERIFIED。所引用基线中的 I36/H36 cases 已定义但 NOT RUN；D/E/H/Storage 记录均将自身限制为 design acceptance，不声称 runtime implementation/conformance。

### 16.8 未决项、责任 Owner 与回流证据

| 未决事项 | 责任 Owner | 必须独立接受的主体 | 回流载体 | 必需证据 |
|---|---|---|---|---|
| I issuer/Principal/Producer trust、delegation、revocation、PermissionEpoch policy 正式批准；I36-GOV-01..10 | I + 获授权 Security/Identity/Architecture Governance | 获授权治理机构；各受保护边界 consumer 验证 I 输出 | I governance decision register → A Integration → 既有 Issue #43 | 具名授权 approver、Decision ID、精确 policy 文本/hash、authority/delegation basis、scope/jurisdiction、effective version/time、expiry/revocation、持久化签名记录 |
| Scope Registry authority、namespace、lifecycle/continuity 来源正式指定 | I + B（语义）；指定的 Scope authority | I governance 与每个使用 Scope 的 consumer | I registry/governance record → B Registry → A / #43 | 具名 authority、精确 Registry ref/version、lifecycle vocabulary、认证 current read、gap/rollback 证据 |
| Environment Registry Authority 指定与 EnvironmentRef currentness | I + Environment owner；B 仅负责类型语义 | I 与每个依赖 Environment 的 consumer | I governance register + Environment authority record → B Registry → A / #43 | 具名 Registry authority、namespace、status/version 来源、trust binding、bridge policy、连续性证明 |
| C telemetry identity/producer/Agent/Adapter/Environment field paths 与 requiredness | C；依赖绑定由 H/I/B 各自负责 | C Owner；wire 由 H；trust policy 由 I | C telemetry contract + H schema/requiredness record → A / #43 | 精确 field path、type、requiredness、authenticated source、negative cases、精确版本 Pin |
| D canonical-memory field paths、role mapping 与 admission/receipt enforcement | D | D Owner；I 对 policy/receipt 独立决定；消费 wire 时 H 独立决定 | D consumer contract → A / #43 | 精确 schema/path、Owner decision、receipt binding、negative/race evidence；只有可复现 implementation tests 才能声称 runtime |
| E ExtractionIR/ingress/publication field paths 与 final gate | E | E Owner；I policy 和 Storage visibility 仍独立 | E consumer contract → A / #43 | 精确 field paths/requiredness、producer binding、lineage、final PermissionEpoch/fence checks、可复现证据 |
| F retrieval/index/cache identity 与 pre-disclosure acceptance | F | F Owner；I authorization；B semantics | F consumer contract → A / #43 | 精确 field mapping、cache/rebuild/currentness behavior、negative tests、final-boundary proof |
| G Context/Delivery/Applied identity 与 recipient acceptance | G | G Owner；H wire、I policy 独立 | G consumer contract → A / #43 | 精确 ContextVersion/Delivery/session/Scope/epoch mapping、replay/reconnect behavior、Applied evidence |
| H production wire/schema freeze 与 interoperable implementation | H | H Owner；受影响 consumers 接受同一精确版本 | H schema/validator/CI record → A / #43 | 精确 schema/IDL 与 commit/Blob、canonicalization、requiredness、version negotiation、generated bindings、interoperability、获授权 freeze record |
| 各 consumer Runtime conformance | 各 implementation/consumer Owner；I 对 policy service evidence 负责 | 每个受影响 consumer Owner 与 A 集成复审 | Owner implementation/test evidence → A / #43 ledger | 精确 build/commit、测试命令/环境、原始日志、适用时 CI run/job、受保护边界 negative/race/recovery 证据；不得用文档替代 |
| Fact/Claim canonical identity ADR-001 | B 提案；获授权 Architecture Governance 决定；受影响 consumers 分别采纳 | Governance 与每个受影响 consumer | ADR-001 decision record → A / 既有治理跟踪 | 正式决策权威、批准选项/文本/hash、精确 consumer migration；BIH identity 决定不解决该 ADR |

### 16.9 非主张与 A Integration 回流

本增补是 B Registry 权威对账，不是重写 BIH baseline。它不批准其他 Owner 的字段、不指定外部 Registry authority、不改变 I36 governance 状态、不冻结 H schema、不关闭 consumer acceptance、不证明 runtime conformance，也不关闭 F-43-06B。A Integration Owner 必须独立回读最终 commit/Blob、对账自己的 ledger/source pins 并决定 Finding disposition。在此之前 F-43-06B 保持 OPEN。
