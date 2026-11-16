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

ACK idempotency: same ACK ID + same digest returns original result; same ID + different digest is conflict/security event. Old-session ACKs cannot mutate new-session state. ACKs after revocation, newer ContextVersion, newer delivery attempt, newer CapabilityEpoch or newer ForgetFence are historical only unless the owning authority independently validates their event-time ordering; they never roll back current state. H transports evidence; G/D/I decide authoritative state in their respective namespaces.

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

- **B Owner Decision:** typed-reference meanings consumed as B proposal; B acceptance of exact H mapping remains OPEN.
- **I Owner Decision:** trust/authorization/revocation/PermissionEpoch policy consumed as I candidate; formal policy and governance approval remain OPEN.
- **H Owner Decision:** H wire proposal authored; no independent H approval/readback is inferred by this document.
- **Cross-module Agreement:** OPEN until explicit B/I/H and affected consumer-owner decisions are recorded.
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