# Phase 3.6 — Authenticated Identity, Protected Operation and Reconnect Binding

- Owner: Session H — BMCP Protocol & Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Status: **JOINT-DECIDED technical baseline; governance and consumer acceptance OPEN; implementation/conformance NOT VERIFIED**
- Date: 2026-11-16
- Source baseline: H Phase 3.5 Identity/Applied/ACK/Reconnect contract, envelope/versioning, capability and ACK contracts; B Typed Reference Registry and Principal/Actor mapping; I Phase 3.6 Trust Chain proposal; C Telemetry Event and Identity; D/E protected-operation requirements; A Phase 3.5 Closure Review.
- Authority: H owns BMCP envelope, serialization, Adapter authentication integration, ACK transport and reconnect. B owns domain Ref semantics. I owns trust and authorization policy. C/D/E/F/G retain their payload and enforcement semantics.

## 1. Authentication boundary and field classes

Authentication occurs outside the untrusted BMCP payload. H obtains protected transport/session/workload verifier context. I validates issuer trust, credential/key status, Principal, audience, validity, revocation, delegation and authorization. A payload mirror cannot authenticate itself.

| Field class | Candidate logical wire field | Domain type | Authority / source | Trust level | Validation owner | Missing / malformed / unknown |
|---|---|---|---|---|---|---|
| Protected auth context | protected `auth.issuer_ref` | IssuerRef | I trust registry + transport verifier | Authenticated verifier output only | H obtains; I validates | Reject if absent/invalid for protected operation |
| Protected auth context | protected `auth.principal_ref` | PrincipalRef | I Principal registry + verifier | Authenticated only when out-of-payload verifier result | H binds; I resolves | Reject; never fallback to payload |
| Protected auth context | protected `auth.authentication_context_ref` | verifier-owned AuthenticationContextRef | H/I verifier | Authenticated verifier reference; no raw credential | H/I | Reject if missing/unverifiable |
| Protected auth context | protected `auth.audience` | registered audience | I policy + endpoint configuration | Authenticated/configured | H/I | Reject audience mismatch |
| Credential metadata | protected key/credential reference and validity profile | credential metadata (not a Ref substitute) | Issuer + verifier + I trust policy | Verified metadata; secret never in payload | H/I | Reject unknown algorithm/key, invalid signature, expiry or revocation |
| Domain identity | `agent_ref`, `agent_principal_ref`, `runtime_instance_ref` | AgentRef, PrincipalRef, runtime-instance identity | B AgentRef; I Principal binding; runtime registry | Payload copy is claim; registry binding required | H/I; C consumes | Reject/quarantine unresolved or mismatched required binding |
| Adapter identity | `adapter_ref`, `adapter_instance_ref`, `adapter_principal_ref` | AdapterRef + distinct instance + PrincipalRef | H Adapter registry; I Principal registry | Protected authenticated instance binding; payload copy is claim | H/I | Reject unknown/replaced/unbound instance |
| Producer identity | `producer_ref` plus protected ProducerIdentity binding | ProducerRef | B type; I Producer registry; H workload binding | Authenticated only from protected binding; payload producer_id is claim | H/I; C/E consume; D work admission separate | Reject unknown/unregistered producer or claim mismatch |
| Attribution | `actor_ref` | ActorRef | B semantic type; I validates; H verifier resolves | Verifier-produced operation attribution only | H/I; D/E/C revalidate at own boundary | Reject caller-minted, malformed or mismatched ActorRef |
| Scope | `scope_refs[]` with explicit role | ScopeRef[] | B type; I/Governance registry | Payload claim until registry resolution and authorization | H resolves syntax; I authorizes; consumer validates | Missing required scope or unknown role/ref => deny |
| Environment | `environment_ref` | EnvironmentRef | Environment authority/registry; I trust binding | Payload claim until authoritative resolution | H/I/C; operation owner enforces | Required-but-missing or unresolved => deny; no label fallback |
| Session | protected `runtime_session_ref` | RuntimeSessionRef | H/platform session issuer; I trust/revocation | Authenticated session binding only | H/I | Expired/revoked/unknown session => reject; renewal creates new ref |
| Authorization | `authorization_decision_ref`, `permission_epoch` | I decision ref + PermissionEpoch | I policy authority | I-issued opaque evidence | I issues; every consumer revalidates | Missing/stale/gapped/unknown => deny/indeterminate |
| Forget | `forget_operation_ref`, `forget_fence_ref` | D ForgetOperation/Fence token | D canonical authority | Opaque D-issued evidence | D validates; I authorization separate | Unknown/stale => suppress/block; never substitute PermissionEpoch |
| Context | `context_ref`, `target_context_version`, `delivery_id`, `delivery_attempt_id` | G-owned typed identifiers | G | Opaque G-issued values | G validates; H transports | Unknown/stale/mismatch => reject or reconcile |
| Capability | `capability_epoch` | H AdapterCapabilityEpoch | H Adapter capability registry | H-issued opaque per-instance epoch | H | Unknown/stale epoch => renegotiate; no implicit capability |
| Operation | `action`, `resource_ref`, `purpose`, `correlation_id`, `idempotency_key` | owner-defined action/resource and correlation | protected operation owner + I policy | Action/resource claims must be authorized | H syntax; I policy; operation owner | Missing required field or unknown critical action => reject |

These are logical candidate field names, not a frozen schema. H owns exact field spelling, canonical encoding, signature profile and version negotiation. H MUST preserve typed discriminators and issuer/namespace dimensions. No raw credentials, bearer secrets or private keys are serialized in ordinary payload fields.

## 2. Payload claims versus authenticated identity

The following payload fields are claims/selectors only: principal_ref, issuer, actor_ref, agent_id/agent_ref, adapter_id/adapter_ref, producer_id/producer_ref, tenant, scope_ref/scope_refs, environment_id/environment_ref, session_id/runtime_session_ref and recipient/source labels.

Rules:
1. A payload-supplied PrincipalRef, ActorRef or ProducerRef never replaces protected authentication context.
2. AdapterRef does not prove authenticated Adapter identity; ProducerRef does not prove authenticated Producer; AgentRef does not prove a security subject.
3. H compares claims with verifier-bound identities and authoritative registries. Mismatch is rejected/quarantined and audited; never resolve in favor of payload.
4. A valid message signature/digest proves integrity under a cryptographic profile, not issuer trust, Principal registration or authorization.
5. ActorRef is a B typed per-operation attribution reference, not a credential or Permission.
6. ScopeRef identifies a domain boundary, not a grant. Cross-Scope/Environment defaults are denied by I.
7. PermissionEpoch and ForgetFenceGeneration are independent opaque tokens. H transports each unchanged and does not compare them.

## 3. Protected operation binding matrix

| Operation | Required identity / payload binding | Authenticated source | Authorization owner | Failure |
|---|---|---|---|---|
| Producer Admission | ProducerRef, producer class/family, workload/instance, ActorRef, ScopeRef roles, EnvironmentRef when applicable, action/resource, PermissionEpoch | Protected workload/session -> I-resolved Principal/Producer; payload producer fields are claims | I for producer trust/action; D for durable per-work registration; E for ingress enforcement | Reject/quarantine unknown producer, claim mismatch, stale epoch, missing Scope or absent D admission receipt |
| Compiler Publication | original ProducerRef + executing ActorRef, WorkItem/Attempt, source/dependency refs, ScopeRef(s), EnvironmentRef, PermissionEpoch, D ForgetFence | Protected compiler/workload identity and verifier-produced ActorRef; durable D registration/dependency receipts | I authorizes; D owns fence/barrier; E owns publication gate; Storage realizes atomicity | Keep artifact private; abort/quarantine on missing/stale identity, epoch, fence or dependency proof |
| Retrieval | authenticated Principal/Actor, requester ScopeRef(s), EnvironmentRef if relevant, query/action/resource, PermissionEpoch | Protected caller transport/session | I authorization; F owns retrieval enforcement | Deny before candidate/snippet/count disclosure; stale cache cannot bypass |
| Context Delivery | recipient Principal, AdapterRef + instance, AgentRef/Principal, RuntimeSessionRef, ActorRef where applicable, ScopeRef, EnvironmentRef if applicable, ContextVersion, DeliveryId/attempt, PermissionEpoch, ForgetFence | Authenticated Adapter/recipient transport; protected session | I authorizes recipient/action; G owns Context/delivery state; H transport | Cancel/quarantine; no stale send/apply; unknown state is not success |
| Applied ACK | authenticated Adapter/Agent Principal and instance/session, ActorRef, ScopeRef, ContextVersion, DeliveryId/attempt, CapabilityEpoch, PermissionEpoch, D fence, final-request evidence refs | Protected authenticated Adapter session; ACK payload identities are claims | I verifies signer/authorization; C owns Applied proof predicates; G owns delivery state; H transports | Reject mismatch/replay; retain historical only if ordering proven; never rollback newer session/context |
| Forget ACK | authenticated Adapter instance/session, ActorRef, ScopeRef, ForgetOperation/Fence, action class, region/coverage, CapabilityEpoch, PermissionEpoch, evidence ID/digest | Protected authenticated Adapter session | I owns target-state/evidence acceptance and exceptions; D owns fence; H emits bounded action evidence | Unknown/unsupported/offline remains Unknown/Pending; no global completion claim |
| Memory Event Ingress | authenticated Producer/Principal/Issuer, ProducerRef, ActorRef, Agent/instance, RuntimeSessionRef, ScopeRef roles, EnvironmentRef if required, event ID/sequence/idempotency key, PermissionEpoch | Protected workload transport; payload producer/actor/scope/environment are claims | I producer trust/action; C event semantics; E durable receipt/ingress; D canonical semantics later | Reject/quarantine mismatch, unknown issuer, missing required environment/scope, stale permission or duplicate conflict |
| Reconnect | fresh Principal/Issuer, Adapter/Agent instance, RuntimeSessionRef, capability, PermissionEpoch, ForgetFence, ContextVersion/Delivery ledger | Fresh protected transport authentication; never old payload/session alone | I trust/authorization; H reconnect protocol; D fence; G reconciliation | Keep protected state suppressed; do not resume until current auth/epoch/fence and G reconciliation pass |
| Administrative Operation | Principal/Actor, issuer, session, explicit Scope/Environment, registered action/resource, delegation chain, PermissionEpoch, approval/audit ref | Strong protected transport/step-up authentication | I policy and separately approved governance; target owner executes | Deny without explicit authority/approval; audit attempt; no self-approval |

## 4. Reconnect protocol — normative order

1. **Authenticate:** establish a fresh protected transport channel and new RuntimeSessionRef; bind concrete Adapter instance.
2. **Validate Issuer:** verify issuer/key, credential type, audience, trust domain, expiry, revocation and trust-registry version under I policy.
3. **Resolve Principal:** resolve authenticated PrincipalRef; bind Agent/Adapter/Producer identities from registries; compare payload claims and reject mismatch.
4. **Negotiate Capability:** negotiate protocol major/minor and per-instance capability profile; establish current CapabilityEpoch; no silent downgrade.
5. **Obtain current PermissionEpoch:** fetch authoritative I policy-domain epochs/decision for exact operations, scopes and resources; stale cached ALLOW is unusable.
6. **Obtain current ForgetFence:** fetch D's authoritative applicable ForgetFence and operation state; keep fence opaque and distinct from PermissionEpoch.
7. **Suppress / Clear stale state:** before reuse, suppress affected targets and perform supported buffer/cache/queue actions; persist action-specific postconditions. Offline/unsupported/ambiguous remains Unknown/Pending.
8. **Reconcile pending delivery:** reconcile G ContextVersion, DeliveryId/attempt, supersession/expiry and ACK journal; discard stale snapshots/deltas; old ACK is historical only.
9. **Resume authorized operations:** reauthorize exact operation at final apply/disclosure boundary; resume only after all required checks pass.

Any failure at steps 1–8 leaves protected state suppressed or unavailable. A new session never inherits the old session's ACK authority. A stale session cannot resume merely because it presents a previously valid token.

## 5. ACK, replay and session fencing

Every ACK MUST bind at least:
- authenticated IssuerRef, PrincipalRef, AdapterRef and concrete AdapterInstanceRef;
- Agent Principal/AgentRef, runtime instance and RuntimeSessionRef;
- verifier-resolved ActorRef and exact ScopeRef role set;
- operation-specific ContextVersion/DeliveryId/attempt or ForgetOperation/Fence;
- CapabilityEpoch and current PermissionEpoch;
- action, target/managed-region identity, coverage, result and postcondition;
- immutable ACK ID, evidence digest/profile, observed time and anti-replay sequence/nonce.

ACK idempotency: same ACK ID + same digest returns original result; same ID + different digest is conflict/security event. Old-session ACKs cannot mutate new-session state. ACKs after revocation, newer ContextVersion, newer delivery attempt, newer CapabilityEpoch or newer ForgetFence are historical only if received after the relevant authoritative linearization point. Sender wall-clock event time is never ordering authority; trusted receiver receipt sequence plus the owning authority's commit cursor determines admissibility. If ordering is indeterminate, retain as evidence only and do not mutate authoritative state. H transports evidence; G/D/I decide authoritative state in their respective namespaces.

## 6. Failure taxonomy

- `AUTHENTICATION_FAILED`: no protected transport principal; reject.
- `ISSUER_UNTRUSTED` / `ISSUER_REVOKED`: reject; no payload fallback.
- `CREDENTIAL_EXPIRED`: reject and require fresh authentication.
- `PRINCIPAL_UNRESOLVED`: reject/quarantine; no auto-registration.
- `IDENTITY_BINDING_MISMATCH`: reject/quarantine and audit.
- `ACTOR_BINDING_INVALID`: reject caller-minted/unbound ActorRef.
- `SCOPE_UNRESOLVED` / `ENVIRONMENT_UNRESOLVED`: deny protected operation.
- `DELEGATION_INVALID` / `DELEGATION_REVOKED`: deny; no represented-Principal fallback.
- `PERMISSION_EPOCH_STALE` / `PERMISSION_INDETERMINATE`: deny or pause.
- `FORGET_FENCE_STALE` / `FORGET_FENCE_UNKNOWN`: suppress/block; never reinterpret as permission epoch.
- `SESSION_STALE` / `ACK_SESSION_MISMATCH`: reject replay.
- `CAPABILITY_EPOCH_STALE`: renegotiate; no capability inference.
- Unknown security-critical field/enum, missing required field, malformed typed Ref, duplicate JSON keys, invalid canonical encoding or protocol major mismatch: fail closed; no silent downgrade.

Errors expose stable code, retryability and correlation ID, not protected payloads, secrets or cross-Scope existence.

## 7. Adversarial conformance matrix

All tests below are **Specified / NOT EXECUTED**. Test execution requires an implementation build, fixtures and retained evidence.

| ID | Test | Expected result | Status |
|---|---|---|---|
| H36-01 | Forged PrincipalRef in payload | Protected Principal remains source of truth; reject mismatch | Specified / NOT RUN |
| H36-02 | Forged ActorRef | Reject caller-minted or mismatched ActorRef | Specified / NOT RUN |
| H36-03 | Forged ProducerRef | Reject unless authenticated workload maps to registered Producer | Specified / NOT RUN |
| H36-04 | Unknown Issuer | Reject before Principal resolution | Specified / NOT RUN |
| H36-05 | Revoked Issuer/key | Reject; invalidate affected session and require reconciliation | Specified / NOT RUN |
| H36-06 | Expired Credential | Reject at reconnect and protected boundary | Specified / NOT RUN |
| H36-07 | Expired Delegation | Deny; do not act as grantor | Specified / NOT RUN |
| H36-08 | Revoked Delegation | Deny and require current PermissionEpoch | Specified / NOT RUN |
| H36-09 | Stale PermissionEpoch | Reject protected operation | Specified / NOT RUN |
| H36-10 | Cross-Scope access | Deny absent explicit I-approved grant | Specified / NOT RUN |
| H36-11 | Cross-Environment access | Deny absent exact bridge/grant | Specified / NOT RUN |
| H36-12 | Authenticated Principal / payload ActorRef mismatch | Reject/quarantine and audit | Specified / NOT RUN |
| H36-13 | Old Session ACK replay | Historical only; no new-session state mutation | Specified / NOT RUN |
| H36-14 | Reconnect races with revocation | Do not resume until fresh trust/epoch/fence/reconciliation succeeds | Specified / NOT RUN |
| H36-15 | Unauthorized Forget Operation | Deny before target/fence mutation | Specified / NOT RUN |
| H36-16 | ACK ID reused with different digest | IDEMPOTENCY_CONFLICT; no state change | Specified / NOT RUN |
| H36-17 | Missing required Scope/Environment | Deny; no wildcard/default | Specified / NOT RUN |
| H36-18 | Protocol major downgrade | VERSION_UNSUPPORTED; no weakened auth | Specified / NOT RUN |

For each executed test record build/commit, protocol version, Adapter instance/tier/capability epoch, issuer/key fixture, authenticated principal class, permission domain/epoch, fence, expected/actual result, log/evidence reference and reviewer. No runtime evidence is currently available; none is marked Passed.

## 8. Owner and approval record

- **B Owner Decision (current):** B semantic mapping is included in the delegated BIH technical baseline; downstream consumer acceptance remains OPEN.
- **I Owner Decision (current):** I technical trust/authorization mapping is included in the delegated BIH baseline; external governance approval remains GOVERNANCE-BLOCKED.
- **H Owner Decision (current):** Phase 3.6 protocol-binding technical design DECIDED under delegated joint authority; no separate H-session signature is claimed.
- **Cross-module Agreement (current):** BIH Phase 3.6 technical design DECIDED under delegated joint authority; affected consumer-owner acceptance remains OPEN.
- **Governance Approval:** GOVERNANCE-BLOCKED where I policy decisions require a named approver, durable decision ID, approval time and effective version.
- **Implementation Evidence:** NOT PROVIDED / NOT VERIFIED; all H36 tests NOT RUN.
- **Fact/Claim ADR-001:** remains independently ADR-BLOCKED; this wire proposal does not change Fact/Claim semantics.

This document does not claim a frozen BMCP schema, deployed authentication implementation, secure reconnect implementation, security certification or runtime conformance PASS.

## 9. BIH Phase 3.6 — Joint Architect Decisions (authoritative technical baseline)

- Decision authority: Joint BIH technical decision authority explicitly delegated by the project user to the Joint Decision Architect in this execution.
- Decision state: **TECHNICALLY DECIDED — JOINT BASELINE**. This settles B/I/H design choices; it does not claim separate human signatures, external governance approval, implementation, or conformance.
- Precedence: this section controls Phase 3.6 BIH design choices where earlier paragraphs label the same choices Candidate/Open. It does not override owner authority boundaries.

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

### 9.2 Owner boundaries

- B retains final semantic authority for Ref types, namespace/reference invariants, ActorRef meaning and ScopeRef role distinctions. B does not decide issuer trust, grants or PermissionEpoch policy.
- I retains final policy authority for issuer admission, Principal/Producer registration, delegation, authorization, revocation, PermissionEpoch and governance exceptions. I does not redefine B domain types or H wire encoding.
- H retains final protocol authority for BMCP envelope, field spelling/encoding, versioning, protected transport integration, Adapter instance binding, ACK transport and reconnect mechanics. H does not authenticate payload claims by itself or grant authorization.
- C/D/E/F/G and Storage retain their own semantic and final enforcement/linearization boundaries. This record does not amend their owner-owned contracts or deem their acceptance complete.

### 9.3 Governance gates — deliberately not cleared

The following remain **GOVERNANCE-BLOCKED** until a named authority approves the exact policy text/hash, approver identity/authority, approval time, scope/jurisdiction, effective version and review/expiry conditions:

- issuer admission/federation, key compromise and trust-domain profile;
- Principal taxonomy and cross-issuer linking policy;
- delegation eligibility, maximum chain depth and any sub-delegation;
- cross-Scope sharing/inheritance and break-glass;
- cross-Environment federation/bridges;
- PermissionEpoch partitioning, revocation SLA and any bounded offline lease;
- revocation effective point, in-flight operation treatment and already-disclosed data handling;
- unsupported Adapter/producer exceptions and Global Forget completion exceptions.

The technical defaults above are deny-first interim rules, not substitutes for approvals. No approver, signature or effective policy version is inferred from this commit.

### 9.4 Acceptance and non-claims

| Dimension | State |
|---|---|
| BIH technical design | **DECIDED — JOINT BASELINE** |
| B/I/H cross-document consistency | **Design decided; branch readback required** |
| External governance approvals | **GOVERNANCE-BLOCKED** |
| C/D/E/F/G/Storage consumer acceptance | **OPEN — not approved by this record** |
| BMCP schema/production policy freeze | **NOT CLAIMED** |
| Runtime implementation and adversarial tests | **NOT VERIFIED / NOT RUN** |
| Security certification | **NOT CLAIMED** |
| Fact/Claim ADR-001 | **ADR-BLOCKED — independent and unchanged** |

This joint decision supersedes only B/I/H Phase 3.6 technical Candidate/Open labels for BIH36-JD-01..17. It does not supersede governance approvals, other Owner decisions, ADR-001 or implementation evidence requirements.

## 10. Phase 3.6 Self-Review Remediation — Binding H Clarifications

This section resolves H36-SR-01..07 and is normative for the H Phase 3.6 protocol binding. It does not freeze the global BMCP schema or claim runtime conformance.

### 10.1 AuthenticationContextRef disposition (H36-SR-01)

AuthenticationContextRef is a verifier-internal opaque handle jointly owned by the H/I authentication implementation boundary, not a public B domain Ref and not a sender-supplied wire field. It is never serialized in ordinary BMCP payloads, cannot be selected by a caller, is bound to one authenticated channel/session and verifier lifecycle, and is invalidated on session/channel closure, principal or workload rebinding, credential/issuer revocation, or verifier security-context reset. H may pass the handle only between trusted verifier components over protected internal interfaces. Raw credentials, bearer tokens and private keys are never copied into payload fields.

### 10.2 Message, channel and session cryptographic binding (H36-SR-02)

The authenticated channel MUST provide a channel-binding value from the negotiated secure transport (for TLS 1.3, a dedicated exporter label and context bound to protocol family, negotiated major version, server identity and fresh RuntimeSessionRef). For each protected message, H computes the canonical message digest over the complete security-relevant envelope and payload, excluding only the integrity proof field as specified by the versioned canonicalization profile. The integrity proof binds:
`(channel_binding, RuntimeSessionRef, message_id, message_nonce, audience, protocol_major, canonicalization_profile, digest_algorithm, canonical_message_digest)`.
The nonce is cryptographically unpredictable or monotonically unique within the session and is stored in a replay window. A proof captured on one channel/session/audience cannot validate on another. The receiver rejects channel/session mismatch, nonce reuse, audience mismatch, canonicalization ambiguity, duplicate keys and digest/signature mismatch. Transport channel binding and message-level integrity are complementary; neither alone establishes I authorization. The exact cryptographic algorithm suite is versioned in H's security profile and requires security review before production enablement.

### 10.3 Operation-specific requiredness profiles (H36-SR-03)

H MUST maintain a versioned Operation Requiredness Registry keyed by `(protocol_major, message_type, operation)`. For each operation it defines required, conditionally required and prohibited fields; the authoritative rule for determining applicability; identity roles; required policy domains; and the final owner boundary. The sender cannot declare a field “not applicable”. Applicability is derived from the registered resource/operation descriptor and authenticated routing context before payload execution.

Minimum rules:
- Producer admission / event ingress: authenticated IssuerRef, PrincipalRef, ProducerRef, ActorRef, AgentRef and concrete workload instance, RuntimeSessionRef, non-empty role-tagged ScopeBindingSet, EnvironmentRef when the event schema declares environment-bound semantics, current PermissionEpoch, event ID/sequence and owner-defined idempotency tuple.
- Compiler publication: the verified producer/work identity, ActorRef, all dependency/resource Scope roles, required EnvironmentRef, current PermissionEpoch and D ForgetFence where the publication boundary requires it; E/D define final lineage and commit fields.
- Retrieval: authenticated PrincipalRef/ActorRef, resource-derived ownership and applicability ScopeBindingSet, EnvironmentRef for environment-bound resources, current PermissionEpoch; deny before any candidate/snippet/count disclosure.
- Context delivery / Applied ACK: authenticated Adapter application and concrete instance, Agent/runtime instance, RuntimeSessionRef, ActorRef, exact delivery/context identity, ScopeBindingSet, CapabilityEpoch, PermissionEpoch and G-owned ContextVersion; G owns applied-state semantics.
- Forget ACK: all preceding adapter/session bindings plus D ForgetOperation/ForgetFence identity, exact region/coverage/action, PermissionEpoch, evidence digest and trusted receiver ordering metadata; D owns forget completion.
- Reconnect: fresh authenticated transport/session, issuer/principal/workload resolution, capability negotiation, current PermissionEpoch and ForgetFence checks before stale-state suppression/reconciliation and resume.

A missing required field, unknown profile, unsupported profile version, unresolvable applicability or sender/registry mismatch is rejected before protected content is disclosed or state is changed.

### 10.4 Trusted ACK ordering after revocation (H36-SR-04)

Adapter-supplied wall-clock timestamps are evidence metadata only and never determine whether an ACK preceded revocation. H assigns a trusted receiver receipt sequence and immutable receipt time at the authenticated ingress boundary. The owning state authority (D for Forget, G for Context Applied state, I for security revocation) orders ACK acceptance against its authoritative commit cursor/epoch. An ACK received after the revocation/fence/epoch linearization point is historical only, regardless of its claimed observed_at timestamp. An ACK received before that point is not automatically accepted: the owner validates session, epoch, operation identity, evidence and causal cursor, then commits it through its own sequencer. If trusted ordering cannot be established, retain as evidence only and do not mutate authoritative state. H never decides D/G/I semantic completion.

### 10.5 ACK idempotency namespace and retention (H36-SR-05)

The canonical ACK idempotency namespace is:
`(authenticated IssuerRef, AdapterRef, AdapterInstanceRef, operation_family, operation_id, ACK_ID)`.
RuntimeSessionRef is included in the signed evidence binding but is not part of the stable idempotency namespace, so reconnect cannot make a duplicate ACK new. The digest covers the canonical ACK body, authenticated identity bindings, evidence references and relevant epoch/fence/capability values. Same namespace + same digest returns the original receipt; same namespace + different digest is a conflict/security event. Retain the deduplication record and tombstone for at least the maximum of the configured message replay horizon, maximum offline queue lifetime, operation retention horizon and revocation/fence reconciliation horizon. If any horizon is unbounded or not governed, retain the tombstone indefinitely. Key rotation does not reset the namespace because issuer and registered Adapter identities remain stable; instance replacement creates a new instance namespace and cannot inherit old-session authority.

### 10.6 H conformance test additions (H36-SR-07)

Add mandatory cases: channel-binding mismatch; same message replayed across sessions/audiences; nonce reuse; canonicalization duplicate-key ambiguity; missing/unknown Operation Requiredness Registry profile; sender suppresses an applicable EnvironmentRef; cross-Adapter ACK ID collision; same ACK ID/different digest; ACK arrival racing revocation/fence advance in both orders; reconnect replay after Adapter instance replacement; capability downgrade with an old valid session. All are **SPECIFIED / NOT RUN** until runtime evidence is attached.

### 10.7 H decision-state reconciliation (H36-SR-06)

The older Section 9 Owner Decision and Cross-module Agreement lines are superseded as process status for the BIH technical design only. Current state: **H protocol-binding technical design DECIDED under the user's delegated joint decision.** This does not claim independent H-session signature, global BMCP schema freeze, external governance approval, C/D/E/F/G/Storage acceptance or implementation conformance. Those remain OPEN/BLOCKED as applicable. ADR-001 remains ADR-BLOCKED.

## 11. Phase 3.6.3 — Issue #3 H exact-version decision and BMCP Applied Wire Profile

- Owner: H — BMCP protocol, Adapter authentication, ACK transport and reconnect.
- Exact shared package: reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md, Blob SHA 122b164bcc0760b83bf555072a36fc55631623e1.
- Common contract version: **CGH-APPLIED-1.0**.
- H decision: **APPROVE WITH ENUMERATED EXCEPTIONS** for H-owned transport, authenticated binding, wire evidence and reconnect clauses. H accepts the same lifecycle and Full Applied evidence boundaries as C/G; H does not claim G Applied authority.
- H wire profile: **bmcp.applied-ack / 1.0.0**, protocol major 1, minor 0. This is the versioned H-owned schema candidate associated with CGH-APPLIED-1.0.

### 11.1 Envelope

Required fields: protocol_family=BMCP; protocol_major/minor (uint16); profile_id/profile_version; message_type; message_id; message_nonce; audience; verifier-bound RuntimeSessionRef; correlation_id; sent_at (audit only); typed body; integrity proof. Major mismatch, unknown critical type/field, duplicate keys, malformed typed Ref, canonicalization ambiguity, nonce reuse, audience/session mismatch or downgrade rejects before state mutation.

### 11.2 Message registry

| Message | Direction | Required body |
|---|---|---|
| DELIVERY_RECEIPT | Adapter → receiver | DeliveryId, attempt, ContextId/ContextVersion, AdapterRef/instance, AgentRef, RuntimeSessionRef, ActorRef, role-tagged ScopeBindingSet, applicable EnvironmentRef, CapabilityEpoch, I PermissionDecision refs, ACK_ID and digest |
| MATERIALIZATION_RECEIPT | Adapter → receiver | delivery/context tuple, ManagedRegion ref/revision, canonicalization profile, complete region digest, Adapter/session binding, ACK_ID/digest |
| FINAL_REQUEST_SUBMISSION_EVIDENCE | C → receiver | InferenceRequestId, FinalRequestBoundaryId, ContextVersion, DeliveryId/attempt, exact final-request digest, ManagedRegion digest/profile, authenticated runtime/session, ActorRef, ScopeBindingSet, applicable EnvironmentRef, PermissionDecision/PermissionEpoch, ForgetFenceGeneration, CapabilityEpoch, immutable evidence ID/digest |
| APPLIED_ACK | Adapter → receiver | context/delivery tuple, InferenceRequestId, FinalRequestBoundaryId, C evidence ref/digest, ManagedRegion digest/profile, authenticated Adapter/instance + Agent + RuntimeSession, ActorRef, ScopeBindingSet, applicable EnvironmentRef, PermissionDecision set, ForgetFence ref/generation where applicable, CapabilityEpoch, ACK_ID/digest |
| FORGET_ACTION_ACK | Adapter → receiver | ForgetOperation/Fence, target/region/action/coverage, capability/evidence tier, authenticated Adapter/session, PermissionDecision, postcondition, ACK_ID/digest |
| CAPABILITY_NEGOTIATION | bidirectional | Adapter/instance, supported protocol/profile versions, action set, evidence tier, capability digest and nonce |
| RECONNECT_STATE | bidirectional | fresh session binding, issuer/principal/workload, capability profile, current PermissionDecision set, D fence cursor, pending Delivery cursor, ACK journal digest |
| ACK_RECEIPT | receiver → Adapter | original ACK namespace/digest, trusted receiver sequence, durable receipt disposition |

Typed refs preserve B type discriminator and namespace. ScopeBindingSet is non-empty. EnvironmentRef is required exactly when the registered operation/resource applicability profile says so; sender cannot self-declare inapplicability. PermissionEpoch and ForgetFence are distinct.

### 11.3 ACK and ordering

ACK kinds: DELIVERY_RECEIVED, MATERIALIZED, FINAL_REQUEST_SUBMITTED_EVIDENCE, APPLIED, EXECUTION_STARTED, FORGET_ACTION, CAPABILITY. Results: ACCEPTED_FOR_OWNER_REVIEW, DURABLY_RECORDED, REJECTED_INVALID, REJECTED_UNAUTHORIZED, REPLAY_DUPLICATE, IDEMPOTENCY_CONFLICT, HISTORICAL_ONLY, UNKNOWN_ORDERING, UNSUPPORTED_ACTION, PENDING_RECONCILIATION. DURABLY_RECORDED proves H receiver durability only; APPLIED is not a transition command; Forget ACK is not Applied proof.

Idempotency namespace: authenticated IssuerRef, AdapterRef, AdapterInstanceRef, operation family, operation ID, ACK_ID. Same namespace+same digest returns original receipt; changed digest is conflict/security event. Session is bound in integrity evidence but does not reset deduplication. H assigns trusted receiver sequence; sender wall clock is audit-only. D/I/G order against their own authoritative commit cursor. Unknown order is evidence-only.

### 11.4 Canonicalization and integrity

Profile 1.0.0 requires deterministic canonical encoding, unique keys, valid UTF-8, explicit typed-ref encoding, normalized set ordering and explicit digest/canonicalization identifiers. Content/idempotency digest is SHA-256. Integrity binds protected-channel binding, RuntimeSessionRef, message ID/nonce, audience, protocol major, profile version, canonicalization profile and canonical digest. TLS 1.3 exporter channel binding and message-level integrity are both required. Exact signature/MAC suite, key custody, rotation and compromise policy require I/Security review before production activation. Unknown requiredness profile, duplicate keys, malformed refs, stale session, nonce reuse, audience mismatch, downgrade or canonicalization ambiguity fails closed.

### 11.5 H decision exceptions and verification

H does not mint C submission evidence, decide G Applied, authorize through I, issue D fences, or prove Storage visibility/Forget completion. Profile status: **SCHEMA CANDIDATE 1.0.0 / OWNER-DECIDED FOR CGH-APPLIED-1.0**; not production freeze or deployed interoperability. H36-01..18 and H36-SR remain **SPECIFIED / NOT RUN**.


## 12. Phase 3.6.4 — Cross-authority causal ordering profile (successor candidate)

- Profile: **`bmcp.applied-ack / 1.1.0`**
- Protocol: major 1, minor 1
- Common contract target: **CGH-APPLIED-1.1 (PROPOSED SUCCESSOR; NOT YET CROSS-OWNER FROZEN)**
- Supersedes 1.0.0 only for flows claiming Full Applied under the three-authority causal-order requirement. 1.0.0 remains parseable for historical/transport evidence but MUST NOT be treated as sufficient proof of C-submit/I-authorization/D-ForgetFence ordering.
- Status: **H-OWNED SCHEMA CANDIDATE; NOT PRODUCTION-FROZEN / NOT DEPLOYED**.

### 12.1 New typed evidence references

All references below are opaque, typed, issuer-namespaced references. H transports and integrity-binds them; H MUST NOT mint, validate semantic truth, compare their numeric values, or infer owner decisions.

| Field | Type / authority | Required meaning |
|---|---|---|
| `causal_order_profile_ref` | CausalOrderProfileRef / joint registry | Exact immutable profile and policy version |
| `causal_order_coordinator_ref` | CausalOrderCoordinatorRef / designated coordinator registry | Identity of the common durable ordering authority |
| `causal_order_transaction_ref` | CausalOrderTransactionRef / coordinator | One protected submission transaction |
| `causal_order_position` | CausalOrderPosition / coordinator | Opaque total-order position; comparable only inside the named coordinator epoch |
| `participant_intent_ref` | ParticipantIntentRef / coordinator | Durable pre-side-effect intent; creates the participant barrier before I/D terminal checks |
| `participant_reservation_ref` | ParticipantReservationRef / coordinator | Finalized reservation after I and D terminal evidence validates; required before C provider side effect |
| `i_commit_authorization_receipt_ref` | CommitAuthorizationReceiptRef / I | Single-use I receipt bound to exact authorization tuple, request digest, transaction and C boundary |
| `i_authorization_terminal_ref` | IAuthorizationTerminalRef / I | I sequencer terminal decision and effective ordering position for this operation |
| `i_revocation_request_ref` | IRevocationRequestRef / I | Immutable revocation request and coordinator admission-cutoff position |
| `d_fence_request_ref` | DForgetFenceRequestRef / D | Immutable fence request and coordinator admission-cutoff position |
| `d_forget_fence_ref` | ForgetFenceRef / D | Exact applicable fence identity and generation |
| `d_lineage_coverage_ref` | ForgetLineageCoverageRef / D | Immutable target + complete source/ancestor lineage coverage proof |
| `d_participant_clearance_ref` | DParticipantClearanceRef / D | D's proof that the reserved participant is ordered before fence effectiveness or has been safely aborted |
| `c_submit_outcome_ref` | CSubmitOutcomeRef / C | Actual provider/runtime boundary outcome, bound to actual InferenceRequestId and FinalRequestBoundaryId |
| `causal_order_terminal_proof_ref` | CausalOrderTerminalProofRef / coordinator | Terminal proof over the participant, I and D evidence references and exact ordered outcomes |

### 12.2 New message families and mandatory bodies

| Message | Direction | Mandatory fields |
|---|---|---|
| `CAUSAL_ORDER_INTENT` | C → coordinator | coordinator/profile refs, transaction ref, exact InferenceRequestId reservation namespace (or preallocated boundary correlation bound later), FinalRequestBoundaryId, immutable request digest, ContextVersion, DeliveryId/attempt, authenticated Principal/Actor/Adapter/runtime/session, ScopeBindingSet, EnvironmentRef if required, CapabilityEpoch, unique intent nonce |
| `CAUSAL_ORDER_INTENT_RECEIPT` | coordinator → C/I/D | transaction ref, ParticipantIntentRef, durable coordinator epoch/position, exact digest, intent state |
| `CAUSAL_ORDER_RESERVATION` | C → coordinator | transaction + ParticipantIntent refs, I CommitAuthorizationReceiptRef + I terminal ref, D fence + lineage + participant-clearance refs bound to ParticipantIntentRef, exact digest and owner evidence digests; finalizes the reservation only after all owner bindings validate |
| `CAUSAL_ORDER_RESERVATION_RECEIPT` | coordinator → C | transaction ref, reservation ref, accepted coordinator epoch/position, exact evidence digest, reservation state, expiry policy (must not silently expire into success) |
| `I_REVOCATION_REQUEST` | I → coordinator | IRevocationRequestRef, PolicyDomainRef, affected action/resource/scope, coordinator cutoff position, I request digest; request immediately blocks new receipts |
| `I_AUTHORIZATION_TERMINAL` | I → coordinator/C | CommitAuthorizationReceiptRef, ParticipantIntentRef, I PolicyDomainRef/PermissionEpoch, exact operation and request digest, single-use consumption result, I sequencer terminal ref/position, applicable IRevocationRequestRef/cutoff or explicit none, COMMIT_WON or REVOCATION_WON or UNKNOWN/IN_DOUBT |
| `D_FENCE_REQUEST` | D → coordinator | DForgetFenceRequestRef, ForgetOperationRef, target/source/ancestor lineage selector, coordinator cutoff position and immutable request digest; request blocks later affected intents |
| `D_FENCE_TERMINAL` | D → coordinator/C | ForgetOperationRef, DForgetFenceRequestRef, ForgetFenceRef/generation, lineage coverage ref, ParticipantIntentRef, D fence-request cutoff position, D fence-effective position, participant disposition, D clearance ref |
| `C_SUBMIT_OUTCOME` | C → coordinator | transaction/reservation refs, actual provider/runtime result, actual InferenceRequestId, FinalRequestBoundaryId, immutable final request digest, provider receipt ref, C evidence ref/digest, outcome ACCEPTED / REJECTED / UNKNOWN |
| `CAUSAL_ORDER_TERMINAL_PROOF` | coordinator → C/G/H | coordinator/profile/transaction refs, reservation ref, I receipt + terminal refs, D fence + lineage + clearance refs, C submit outcome ref, ordered positions, terminal outcome, proof digest and coordinator signature/key ref |
| `CAUSAL_ORDER_ACK` | H receiver → sender | original transaction/proof refs, receiver sequence, durable receipt disposition; explicitly transport durability only |

### 12.3 Normative participant-barrier protocol

1. **Create intent first.** C freezes the exact request digest and obtains a durable ParticipantIntentRef from the coordinator before any provider side effect. The intent binds the exact boundary, identity/session, context/delivery and request digest; it is not yet permission to submit.
2. **I terminal authorization.** I consumes the single-use CommitAuthorizationReceipt exactly once, bound to that intent, and orders it against revocation in I's authoritative sequencer. I emits a signed terminal reference. If revocation wins, C must abort without provider side effect. If authorization wins, I holds later revocation effectiveness behind this unresolved participant.
3. **D participant clearance.** D registers the same intent against exact target/source/ancestor lineage. If an applicable fence was already effective, D returns FENCE_WON. Otherwise D holds any later fence effectiveness behind this unresolved participant and emits a signed clearance.
4. **Finalize reservation.** Coordinator validates the exact I and D owner references and finalizes ParticipantReservationRef. No provider call is permitted before this step succeeds.
5. **Submit and terminalize.** C invokes the provider/runtime under that reservation, captures the actual outcome, and appends it. Coordinator emits terminal proof only after C/I/D evidence is durable.
6. **Coordinator serialization.** The coordinator durably orders intent, I authorization/revocation terminal, D fence-effective transition, final reservation and C submit outcome. I and D remain semantic authorities; coordinator order cannot override an owner rejection.
8. **Fence/revocation race.** A D fence arriving after ParticipantIntentRef MUST remain pending until the intent is safely aborted or the exact provider outcome is terminal. An I revocation arriving before I consumes the receipt may win and force abort; after I terminalizes authorization as COMMIT_WON, I must hold effective revocation behind that participant until C's outcome is terminal. If submit succeeds first, the historical submission is ordered before the later effective fence/revocation; subsequent current use is still invalidated. If safe abort is committed first, no provider submit may occur. If provider outcome cannot be determined, participant remains IN_DOUBT and the fence/revocation barrier remains blocked until authoritative reconciliation.
9. **No favorable inference.** Missing coordinator, unavailable owner, inconsistent positions, lost receipt, unknown provider outcome, incomplete lineage, receipt replay, or digest mismatch => UNKNOWN/IN_DOUBT; suppress content; no Full Applied.
10. **No wall-clock ordering.** `sent_at`, local timestamps, receiver arrival order and H receiver sequence are audit/transport metadata only; none substitutes for coordinator ordering.

### 12.4 Terminal outcome vocabulary

- `SUBMIT_COMMIT_WON`: exact provider/runtime submission is durably proven before the effective D fence and I revocation terminal points.
- `ABORT_WON`: safe abort is durably terminal before the provider side effect; provider submission is forbidden.
- `REVOCATION_WON`: I revocation is terminal before authorization consumption; C must not submit.
- `FENCE_WON`: D fence is effective before participant reservation; C must not submit.
- `IN_DOUBT`: external provider outcome or owner/coordinator ordering cannot be proven; no success or Full Applied.
- `CONFLICT`: same transaction/receipt identity has different immutable digest or contradictory terminal claims; quarantine and security event.

A successful historical submit proof never grants later permission or current-use eligibility. G alone decides Applied and recomputes current-use against current I/D state.

### 12.5 Required validation rules

- CommitAuthorizationReceiptRef MUST be I-issued, single-use, bound to exact PolicyDomainRef, PermissionEpoch, complete identity/action/resource/purpose/audience/scope/environment/delegation tuple, request digest, CausalOrderTransactionRef and FinalRequestBoundaryId.
- IAuthorizationTerminalRef MUST prove I sequencer consumption and terminal order; a PermissionDecisionRef or PermissionEpoch alone is insufficient.
- DLineageCoverageRef MUST cover exact target plus all applicable source/ancestor dependencies; DParticipantClearanceRef MUST prove the participant is before fence effectiveness or safely aborted.
- CSubmitOutcomeRef MUST be issued only from actual successful/failed provider/runtime boundary observation; local buffer, middleware render, transport ACK or reservation receipt is insufficient.
- CausalOrderTerminalProofRef MUST cryptographically bind every above ref, the common transaction, ParticipantIntentRef, I revocation request cutoff (or explicit none), D fence request cutoff, coordinator epoch/positions and terminal result.
- H MUST preserve all refs exactly, enforce profile requiredness and integrity, reject unknown critical fields, and never downgrade a 1.1.0 Full-Applied flow to 1.0.0.

### 12.6 Operational and safety limits

The coordinator's concrete operator, durable store, HA/failover, retention, disaster recovery, key trust and availability SLO are **NOT YET DESIGNATED / NOT APPROVED**. No production use is allowed until C, I, D and the coordinator/storage operator approve the same profile and demonstrate that coordinator restore cannot roll back terminal positions or clear unresolved participants. The safe failure mode is blocked submission and blocked fence/revocation completion, not bypass.

### 12.7 Conformance additions (specified, not run)

- H36-CO-01 reservation before provider side effect; no receipt means no submit.
- H36-CO-02 I receipt replay / wrong request digest; reject.
- H36-CO-03 I revocation before receipt consumption; REVOCATION_WON.
- H36-CO-04 D fence before reservation; FENCE_WON.
- H36-CO-05 fence requested after reservation; fence remains pending until submit/abort terminal.
- H36-CO-06 provider accepted, then D fence/revocation requested; historical submit ordered first, current-use invalid.
- H36-CO-07 provider outcome unknown after crash; IN_DOUBT, D/I barriers remain open.
- H36-CO-08 coordinator failover/restore cannot regress positions or clear participants.
- H36-CO-09 contradictory C/I/D terminal evidence; CONFLICT/quarantine.
- H36-CO-10 wall-clock and H receiver sequence deliberately inverted; coordinator order remains decisive.

All cases: **SPECIFIED / NOT RUN**. This addendum is a schema candidate and architecture proposal; it does not establish owner acceptance, coordinator deployment, implementation or test pass.

## H Owner exact-version decision — CGH-APPLIED-1.1

- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA: `9808b31f840606b329f1a794935dfc9c5084d63b`
- Common contract: `CGH-APPLIED-1.1`
- H schema target: `bmcp.applied-ack/1.1.0`
- Causal profile: `CausalOrderProfile/1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within H's authority over BMCP schema/serialization, authenticated transport, ACK, integrity/replay, capability and reconnect.

H accepts the 1.1 message/evidence separation and transport mapping for ParticipantIntent, ParticipantReservation, I CommitAuthorizationReceipt/AuthorizationTerminal, D fence-request/fence-effective/lineage-clearance, C SubmitOutcome and CausalOrderTerminalProof. H accepts that all such references remain owner-issued opaque typed references; H transports and integrity-protects them but does not mint or adjudicate I/D/C/G authority. Forget Action ACK remains distinct from Applied and C submit evidence. A 1.0 downgrade cannot satisfy 1.1 Full Applied.

Exceptions and closure conditions:
1. The 1.1.0 schema remains an H-owned candidate, not production-frozen, deployed or interoperably verified. Conditional requiredness, exact field types, canonicalization, unknown-critical-field behavior, compatibility and replay rules require final schema conformance evidence.
2. Exact signature/MAC suite, key custody/rotation/compromise and federation remain subject to I/Security governance approval before production activation.
3. H receiver sequence/ACK arrival order is not cross-authority causal proof. H must preserve the coordinator/owner terminal proof and may not synthesize missing I/D/C evidence.
4. Durable ACK/evidence journal, reconnect, downgrade rejection and crash/replay behavior require H36/CO test execution; all remain NOT RUN.
5. H does not approve coordinator deployment, provider idempotency, I/D sequencer/fence implementation or G Full Applied predicate.

This decision applies only to the exact A Blob above. It does not assert schema freeze, production interoperability, test pass or transfer of any CGH-APPLIED-1.0 decision.


## 12.8 H normative field-level decision for CGH-APPLIED-1.1

- Exact A candidate Blob SHA reviewed: `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`
- Schema: `bmcp.applied-ack/1.1.0` (protocol major 1, minor 1)
- Profile: `CausalOrderProfile/1.0`

**H DECISION: ACCEPT WITH ENUMERATED EXCEPTIONS**, within H's BMCP schema, serialization, transport-integrity, ACK, replay and compatibility authority. This is a schema decision, not production freeze or deployment approval.

### 12.8.1 Field encoding and common envelope

1. Every 1.1 field name is lower_snake_case and case-sensitive. Typed references are opaque non-empty UTF-8 strings (1..512 bytes after UTF-8 encoding), issuer-namespaced by the issuing authority. H MUST preserve their byte-level value after schema decoding/re-encoding; it MUST NOT parse embedded numeric meaning, rewrite namespaces, normalize identifiers or synthesize refs.
2. Digests are exactly 32-byte SHA-256 values represented as 64 lowercase hexadecimal characters. Digest algorithm and canonicalization profile identifiers are explicit fields; no implicit algorithm negotiation is permitted.
3. Structured message bodies use UTF-8 JSON with deterministic canonicalization: unique object keys, no duplicate keys, no NaN/Infinity, stable object-key ordering, arrays retain semantic order unless the field is explicitly a set, set-valued fields are sorted by canonical encoded member, and strings are valid Unicode scalar sequences. Canonicalization profile ID is mandatory and covered by the message integrity digest. A profile mismatch is rejected.
4. Coordinator epoch and order positions are opaque strings, not JSON numbers. They are comparable only by the coordinator-defined comparison operation within the same coordinator identity and epoch; H MUST NOT sort or compare them lexically or numerically. Wall-clock timestamps and H receiver sequence remain audit/transport metadata only.
5. The authenticated envelope MUST include schema_id, schema_version, message_id, nonce, audience, RuntimeSessionRef, CausalOrderCoordinatorRef, CausalOrderProfileRef, canonicalization_profile_id, payload_digest and integrity_proof_ref. The protected channel binding and message-level integrity cover the complete canonical envelope and body.

### 12.8.2 Requiredness by message family

- Every causal-order message: `schema_id`, `schema_version=1.1.0`, `message_id`, `nonce`, `audience`, authenticated session, `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_transaction_ref`, canonicalization profile, payload digest and integrity proof are REQUIRED.
- `CAUSAL_ORDER_INTENT`: transaction/profile/coordinator refs, request digest, FinalRequestBoundaryId, ContextVersion, DeliveryId + attempt, identity/Actor/Adapter/runtime/session binding, ScopeBindingSet, CapabilityEpoch and unique intent nonce are REQUIRED. EnvironmentRef is REQUIRED when the applicable policy/environment binding says one applies; otherwise it MUST be explicitly represented as not-applicable, not silently omitted.
- `CAUSAL_ORDER_INTENT_RECEIPT`: ParticipantIntentRef, coordinator epoch/position, request digest and durable intent state are REQUIRED.
- `I_AUTHORIZATION_TERMINAL`: CommitAuthorizationReceiptRef, IAuthorizationTerminalRef, ParticipantIntentRef, PolicyDomainRef, PermissionEpoch, I sequencer identity/epoch/position, request digest and terminal outcome are REQUIRED. `i_revocation_request_state` is REQUIRED with enum `PRESENT` or `NONE_AT_TERMINALIZATION`. If PRESENT, IRevocationRequestRef and its coordinator cutoff position are REQUIRED; if NONE_AT_TERMINALIZATION, both are forbidden. The explicit state prevents absence from being interpreted as proof of no earlier request.
- `D_FENCE_TERMINAL`: DForgetFenceRequestRef, request cutoff position, ForgetOperationRef, ForgetFenceRef/generation, ForgetLineageCoverageRef, ParticipantIntentRef, DParticipantClearanceRef, fence-effective position (when effective), and participant disposition are REQUIRED. Request cutoff and effective position are separate typed fields and MUST NOT share a slot. If the fence is not yet effective, effective position is explicitly null with disposition PENDING; it is not omitted.
- `CAUSAL_ORDER_RESERVATION_RECEIPT`: ParticipantIntentRef, ParticipantReservationRef, reservation coordinator epoch/position, exact evidence digest and reservation state are REQUIRED. Any expiry field is informational only and MUST NOT authorize automatic barrier release.
- `C_SUBMIT_OUTCOME`: ParticipantReservationRef, CSubmitOutcomeRef, exact request digest, FinalRequestBoundaryId, actual InferenceRequestId, provider receipt reference when outcome is ACCEPTED, and outcome enum are REQUIRED. For REJECTED, definitive no-handoff evidence is REQUIRED. For UNKNOWN, provider receipt may be absent but state MUST be IN_DOUBT and no Full Applied proof is allowed.
- `CAUSAL_ORDER_TERMINAL_PROOF`: ParticipantIntentRef, ParticipantReservationRef (if reservation was finalized), I receipt and terminal refs, explicit I revocation state/ref-or-none, D fence request cutoff, D effective position-or-pending state, lineage and D clearance refs, CSubmitOutcomeRef, coordinator epoch and ordered positions, terminal outcome, evidence digest and coordinator signature/key reference are REQUIRED. A safe-abort path MUST explicitly encode that no provider side effect occurred and include the immutable abort evidence ref.
- `CAUSAL_ORDER_ACK`: original transaction/proof refs, receiver sequence, durable receipt disposition and receiver identity are REQUIRED. ACK is transport durability only and cannot substitute for C/I/D terminal evidence.

### 12.8.3 Validation, replay and downgrade behavior

- Unknown non-critical extension fields MAY be retained and forwarded unchanged. Unknown critical fields MUST be rejected. Missing required fields, null in place of a required field, malformed typed refs, duplicate keys, digest mismatch, invalid enum, inconsistent conditional fields or mismatched transaction/boundary/digest MUST be rejected/quarantined.
- Message ID + nonce replay is rejected unless it is an exact idempotent replay of the same transaction, same message family and same canonical payload digest; same identity with a different digest is CONFLICT and security-event material. A replayed single-use CommitAuthorizationReceipt MUST never cause a second authorization consumption.
- 1.0.0 remains parseable for historical and transport evidence. For any Full Applied claim under CGH-APPLIED-1.1, negotiation MUST require 1.1.0; downgrade, fallback or mixed-version evidence is rejected as insufficient. 1.0 ACKs may be acknowledged as transport receipts but MUST NOT be promoted to 1.1 terminal proof.
- H receiver sequence, ACK arrival time and reconnect order are not causal positions. Reconnect MUST preserve original transaction, message ID, nonce, digest and owner refs; no new terminal proof may be synthesized during replay.
- H MUST reject an untrusted coordinator identity/profile, invalid channel binding, expired/stale runtime session, audience mismatch, nonce reuse, invalid integrity proof or downgrade attempt before delivering a message to the consumer.

### 12.8.4 H acceptance exceptions

1. Exact signature/MAC suite, key custody, rotation, compromise recovery and federation remain subject to separate I/Security governance approval.
2. The schema remains a candidate: generated schema artifacts, implementation interoperability, H36-CO and replay/reconnect suites are NOT RUN.
3. Coordinator/operator deployment and C/I/D service conformance remain outside H authority and are not approved by this decision.
4. G alone decides Applied; H ACK and valid schema parsing never imply Full Applied or current-use eligibility.

This H decision applies only to A package Blob `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`. It supersedes no 1.0 decision and does not claim production freeze, deployment or test pass.

## H exact-version acceptance — CGH-APPLIED-1.1 recovery-batch amendment

- A package Blob: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC Blob: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- H schema target: `bmcp.applied-ack/1.1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within H's transport/schema/integrity/replay authority.

H accepts the recovery-batch semantics as transportable evidence: durable I/D owner-local pending-gate references, the COC recovery-cutoff batch identity/position/digest, the enumerated pre-batch ParticipantIntentRef set, I-specific reconciliation outcomes, D-specific lineage/barrier reconciliation outcomes, owner high-water attestations and the final gate-reopen eligibility result. H preserves I/D owner-issued evidence as opaque references and does not infer or synthesize either authority's decision. No local clock order is elevated to a causal position.

Exceptions: (1) A's 1.1 package does not yet freeze exact wire field names, message requiredness and canonicalization for every recovery-batch evidence item; H must publish a schema addendum before production freeze; (2) signature/MAC suite, key custody/rotation/compromise and federation remain subject to I/Security approval; (3) schema generation/interoperability/replay/reconnect and H36-CO tests remain NOT RUN; (4) COC/operator deployment is not approved by H. This decision applies only to the exact A/COC Blob pair above and is not production schema freeze.

## 12.9 H schema addendum — COC outage recovery batch (1.1.0 candidate)

- Applies to A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- Schema: `bmcp.applied-ack/1.1.0`.
- Status: **H-OWNED SCHEMA CANDIDATE ADDENDUM / NOT FROZEN / NOT GENERATED / NOT INTEROPERABILITY-TESTED**.

This addendum resolves H's enumerated exception about the recovery-batch field mapping. It defines the transport representation only. I and D remain the sole authorities for their owner-local pending gates, I authorization terminality, D fence/lineage state and gate reopening. COC is the authority for its committed batch/log position, not for I/D owner decisions.

### 12.9.1 New message families

The 1.1.0 candidate adds these message families:

1. `OWNER_LOCAL_PENDING_GATE` — I or D reports a durable local pending gate created while COC is unavailable.
2. `COC_RECOVERY_CUTOFF_BATCH` — COC reports the quorum-committed recovery batch containing all owner-known I/D outage requests.
3. `PRE_BATCH_PARTICIPANT_RECONCILIATION` — owner evidence reports reconciliation of every affected pre-batch ParticipantIntentRef.
4. `OWNER_LOCAL_GATE_RELEASE` — I or D reports its own gate disposition after reconciliation; COC cannot issue this message as an owner decision.
5. `COC_RESTORE_FENCED` — COC reports that restore/prefix/high-water proof is incomplete and protected admission remains blocked.

All five families use the authenticated 1.1.0 common envelope and existing profile/coordinator/transaction binding. Each message is independently integrity-protected and replay/idempotency checked. H does not synthesize a missing message or owner attestation.

### 12.9.2 Field definitions and requiredness

**A. OWNER_LOCAL_PENDING_GATE**

Required:
- `owner_authority`: enum `I` or `D`.
- `owner_local_pending_gate_ref`: opaque owner-issued typed reference.
- Exactly one applicable request reference: `i_revocation_request_ref` when owner_authority=I, or `d_forget_fence_request_ref` when owner_authority=D. The other field MUST be absent.
- `causal_order_domain_ref`: opaque registry-resolved domain reference.
- `owner_local_gate_state`: fixed enum `PENDING_COC_CUTOFF`.
- `owner_local_request_digest`: SHA-256 digest of the immutable owner request binding.
- `owner_local_durable_attestation_ref`: owner-issued proof that the local pending gate is durably persisted.
- `affected_lineage_digest`: REQUIRED for D; forbidden for I unless I's own policy schema explicitly defines a distinct typed field.
- `owner_local_sequence`: optional opaque audit metadata only; it MUST NOT be compared with another owner's sequence, a COC position, or a wall-clock value.

No COC position is required or implied because the request has not yet been quorum-recorded. A pending-gate message MUST NOT be interpreted as an effective PermissionEpoch advance or ForgetFenceGeneration.

**B. COC_RECOVERY_CUTOFF_BATCH**

Required:
- `recovery_batch_ref`: COC-issued opaque batch reference.
- `recovery_batch_digest`: SHA-256 digest over the complete canonical batch.
- `pre_batch_log_position` and `pre_batch_log_root_digest`: exact quorum-confirmed prefix boundary before the recovery batch.
- `recovery_cutoff_position`: quorum-committed COC position of the batch.
- `included_i_revocation_request_refs`: canonical set of every I request received during the outage; empty set is explicit when none.
- `included_d_fence_request_refs`: canonical set of every D request received during the outage; empty set is explicit when none.
- `owner_request_set_digest`: SHA-256 digest over the union of both canonical request sets.
- `i_owner_batch_attestation_ref` and `d_owner_batch_attestation_ref`: required when the corresponding owner request set is non-empty; each attests completeness of that owner's outage requests.
- `batch_commit_proof_ref`: COC quorum-commit proof for the exact batch position and digest.

The I and D request arrays are canonicalized independently by opaque reference bytes and then included in the batch digest. Their array order MUST NOT be interpreted as a temporal order between I and D. Local request sequence/time is audit metadata only. Missing owner completeness attestation, missing request, prefix mismatch or digest mismatch makes the batch invalid and leaves owner gates closed.

**C. PRE_BATCH_PARTICIPANT_RECONCILIATION**

Required:
- `recovery_batch_ref` and `recovery_batch_digest`.
- `pre_batch_participant_set_digest`: digest of the complete set of affected ParticipantIntentRefs committed before the batch cutoff.
- `participant_reconciliation_entries`: non-empty array unless the authoritative complete set is explicitly attested empty.
- `participant_set_completeness_attestation_ref`: COC proof of enumeration against the committed prefix plus owner high-water attestations.
- `owner_high_water_attestations`: non-empty array containing each applicable owner authority, its opaque high-water reference and its signed completeness proof.

Each `participant_reconciliation_entries[]` item requires:
- `participant_intent_ref`;
- `causal_order_transaction_ref`;
- `request_digest`;
- `i_reconciliation_state`: `COMMIT_WON`, `REVOCATION_WON`, `PENDING`, `UNKNOWN`, or `NOT_APPLICABLE`;
- `d_reconciliation_state`: `CLEARANCE_CONFIRMED`, `FENCE_WON`, `PENDING`, `UNKNOWN`, or `NOT_APPLICABLE`;
- `c_reconciliation_state`: `ACCEPTED`, `REJECTED`, `UNKNOWN`, or `NOT_APPLICABLE`.

Conditional owner evidence:
- If I state is COMMIT_WON or REVOCATION_WON, `i_authorization_terminal_ref` is REQUIRED and must be I-issued. If I state is PENDING/UNKNOWN, any terminal ref is forbidden unless it explicitly represents that same nonterminal state under an I-owned schema.
- If D state is CLEARANCE_CONFIRMED or FENCE_WON, `d_lineage_coverage_ref` and the corresponding D-issued terminal/clearance reference are REQUIRED. If PENDING/UNKNOWN, no favorable clearance may be inferred.
- If C state is ACCEPTED or REJECTED, `c_submit_outcome_ref` is REQUIRED and must be C-issued. If UNKNOWN, the participant remains IN_DOUBT and cannot be treated as safely terminal.
- `participant_terminal_proof_ref` is REQUIRED only when all required owner outcomes are determinate and reconciled; otherwise it MUST be absent and the entry remains pending/unknown.

The message MUST explicitly distinguish an empty affected participant set from a missing or unenumerated set. An absent array is invalid; use an empty array plus the completeness attestation only when the authoritative set is proven empty.

**D. OWNER_LOCAL_GATE_RELEASE**

Required:
- `owner_authority`: I or D.
- `owner_local_pending_gate_ref`.
- `recovery_batch_ref` and `recovery_batch_digest`.
- `participant_set_completeness_attestation_ref`.
- `owner_high_water_attestation_ref`.
- `owner_reconciliation_digest`.
- `owner_gate_disposition`: `REOPENED` or `REMAINS_CLOSED`.
- `owner_gate_release_attestation_ref`: signed by the owner identified in `owner_authority`.

Only I may emit an I gate release; only D may emit a D gate release. `REOPENED` is valid only after that owner verifies all its outage requests are in the batch, all affected pre-batch participants are reconciled for its authority, and its high-water mark is monotonic. COC cannot emit or infer owner gate release. `REMAINS_CLOSED` is a fail-closed state and cannot authorize protected admission.

**E. COC_RESTORE_FENCED**

Required:
- `coordinator_ref`, `restore_attempt_ref`, `last_quorum_checkpoint_ref` if one is available;
- `observed_log_term`, `observed_log_index` and `observed_root_digest` if available;
- `restore_fence_reason`: enum `MISSING_PREFIX`, `CHECKPOINT_STALE`, `OWNER_HIGH_WATER_MISMATCH`, `PARTICIPANT_SET_INCOMPLETE`, `DIGEST_CONFLICT`, or `OWNER_UNAVAILABLE`;
- `restore_fence_state`: fixed enum `RESTORE_FENCED`;
- `reconciliation_required`: boolean true.

Missing observed values are explicitly null, not fabricated. This message reports a COC state only; it does not clear I/D local gates.

### 12.9.3 Canonicalization, integrity and replay

- All new fields are covered by the existing 1.1.0 canonical envelope, canonicalization profile identifier, payload digest and message-level integrity proof.
- Set-valued request-reference arrays and owner high-water attestations are sorted by canonical encoded opaque reference, not by local sequence/time. Participant reconciliation entries are sorted by ParticipantIntentRef canonical encoding; their semantic order is not inferred from array position.
- Every digest covers the schema version, message family, transaction/domain binding, all required/conditional fields and explicit empty-set states.
- Same message identity + same canonical digest is an idempotent replay; same identity + different digest is CONFLICT and quarantined. Recovery-batch identity cannot be rebound to a different request set or pre-batch prefix.
- Missing owner completeness proof, missing participant-set proof, unknown critical field, invalid owner signer, inconsistent conditional field, or attempted inference from local clocks is rejected.
- H receiver sequence and message arrival order remain transport metadata only. The batch's quorum-committed COC position is the sole COC ordering position; I/D owner terminal positions remain separately authoritative.

### 12.9.4 Non-claims and conformance

This schema addendum does not make the 1.1.0 schema production-frozen, does not select a cryptographic suite or key custody policy, and does not prove generated schema interoperability. Signature/MAC suite, key lifecycle, federation and coordinator workload identity remain subject to I/Security approval.

Required new H conformance cases (SPECIFIED / NOT RUN):
- H-CO-17: reject pending-gate message that includes a fabricated COC position or lacks owner durable attestation.
- H-CO-18: reject recovery batch with missing owner request, missing owner completeness attestation or mismatched pre-batch prefix/root.
- H-CO-19: prove I/D request arrays do not establish cross-owner time order.
- H-CO-20: reject incomplete pre-batch participant enumeration or owner high-water mismatch.
- H-CO-21: reject owner gate release emitted by COC or wrong owner.
- H-CO-22: preserve RESTORE_FENCED across reconnect; no gate reopen on missing owner evidence.
- H-CO-23: enforce idempotent same-digest replay and conflict on changed request set/digest.

**H disposition:** the recovery-batch field mapping exception is resolved at the H schema-candidate documentation level for this exact A package. Production freeze remains NO; generated schema, implementation interoperability, crypto governance and H-CO-17..23 remain OPEN / NOT RUN.
