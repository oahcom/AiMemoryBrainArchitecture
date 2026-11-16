# Phase 3.6 — Identity Trust, Authorization and Revocation Closure

- Owner: Session I — Security, Identity & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Status: **JOINT-DECIDED technical baseline; GOVERNANCE-BLOCKED; implementation/conformance NOT VERIFIED**
- Date: 2026-11-16
- Source baseline: I Phase 3.6 Principal Trust Chain contract; I Principal/Actor/Authorization contract and Governance Decision Register; B Phase 3.5 Typed Reference Registry and Phase 3.6 candidate; H Phase 3.5 Identity/ACK/Reconnect; C Telemetry Event and Identity; D/E protected-operation contracts; A Phase 3.5 Closure Review.
- Authority: I owns issuer trust, Principal/Producer registration, delegation, authorization, revocation and PermissionEpoch. B owns Ref semantics; H owns transport/wire; operation owners enforce their protected boundaries.

## 1. Principal trust chain

Normative candidate path:

`Authenticated Transport → Issuer Trust Validation → Principal Resolution → Delegation Validation → ActorRef Resolution → Scope Authorization → PermissionEpoch Validation → Protected Operation`

Every stage produces verifier/authority-owned evidence. A later stage MUST NOT reconstruct trust from payload fields or skip an earlier failed/indeterminate stage.

| Stage | Authority | Input | Output / audit evidence | Failure and revocation semantics |
|---|---|---|---|---|
| Authenticated Transport | H for BMCP; platform ingress for other transports | Protected channel/session, peer/workload credential proof, channel binding, nonce/replay context | Verifier-authenticated transport context bound to connection/session, audience and time | Missing, replayed, unprotected, mismatched or unverifiable transport: reject; no payload identity promotion |
| Issuer Trust | I policy + cryptographic verifier | Credential/signature, issuer/key ID, type, audience, tenant/security domain, nbf/exp, key and revocation status | Validated IssuerRef, key/trust-registry version, verification result | Unknown/revoked/compromised issuer or key, invalid signature, wrong audience/domain/type, expired/not-yet-valid credential, unavailable trust state: DENY/INDETERMINATE |
| Principal Resolution | I Principal Registry | Validated issuer subject, namespace, principal kind and registry status | Stable PrincipalRef and registered status/binding | Unknown, retired, suspended, ambiguous, mismatched or unregistered subject: deny/quarantine; never auto-register from payload |
| Delegation Validation | I Delegation Registry/policy | Grant chain, grantor/delegate, issuer, actions, resource, Scope, audience, purpose, nbf/exp, parent links and revocation | Immutable validated DelegationChainRef and authority intersection | Missing/expired/revoked/invalid signature/cycle/depth overflow/audience or Scope mismatch/amplification: deny |
| ActorRef Resolution | B defines type; H supplies authenticated binding; I validates assertions | Authenticated Principal, validated delegation, Agent/Adapter/Producer binding, operation correlation | Verifier-resolved ActorRef bound to Principal, operation and chain | Payload-only/caller-constructed ActorRef, mismatch or missing binding: reject and audit |
| Scope Authorization | I policy; B owns ScopeRef semantics | Principal, ActorRef, ScopeRef roles, EnvironmentRef, Action, Resource, purpose, audience, delegation | ALLOW/DENY/INDETERMINATE, obligations, policy version and exact scope coverage | Unknown/missing required Scope/Environment, implicit inheritance or unapproved cross-boundary request: deny |
| PermissionEpoch Validation | I sole logical authority; each consumer validates with I or approved bounded lease | Current policy-domain epoch, linearizable revocation position, single-use CommitAuthorizationReceipt and subject/resource binding | Current authorization proof plus single-use receipt atomically ordered with owner commit and revocation | Stale/gapped/unknown epoch, expired decision, revocation uncertainty or unapproved offline lease: pause/deny |
| Protected Operation | Owning boundary: C/D/E/F/G/H; I supplies policy | All verifier evidence + exact action/resource + final-boundary epoch and owner-local fence/version | Operation receipt and audit decision | Missing proof, epoch change before linearization, stale fence or ambiguous outcome: abort/quarantine; never report success |

Audit record: correlation/operation ID, stage, verifier/owner, opaque typed refs or approved non-reversible fingerprints, issuer/key/trust-registry version, decision/reason, policy domain/epoch, timestamp/clock quality and integrity metadata. Never log credentials, bearer tokens, private keys or protected plaintext.

## 2. Issuer Trust

I owns the logical Trusted Issuer Registry. Each issuer record binds:
- stable, non-recycled IssuerRef and TrustDomainRef;
- accountable issuer owner/security contact;
- allowed tenant/security domains and explicit federation mappings;
- credential/attestation types, algorithms and key IDs;
- allowed audiences, subject/principal kinds and claim namespaces;
- activation, suspension, compromise, revocation and retirement state;
- key rotation schedule, bounded overlap and emergency compromise procedure;
- policy version, approval evidence and review/expiry date.

Trust is explicit and non-transitive. Trusting issuer A does not trust issuer B or a delegated issuer without explicit I-approved mapping.

Credential validation MUST cover issuer, key ID, signature/protected-channel proof, credential type, audience, tenant/security domain, subject namespace, nbf, exp, revocation, authentication strength and key status. Subject strings resolve only inside the validated issuer namespace.

- Planned rotation: explicit key IDs and bounded overlap; retire old key at recorded cutover.
- Emergency compromise: revoke key/issuer, advance affected PermissionEpoch domains, invalidate dependent credentials/sessions/delegations and trigger consumer reconciliation.
- Issuer revocation blocks new authentication/work; in-flight work reauthorizes at next protected boundary.
- Credential expiry is checked at every protected operation; session renewal requires fresh validation.
- Unknown issuer/key, unsupported algorithm, unavailable revocation state, invalid audience/domain, expired credential and trust-on-first-use all fail closed. No payload-driven trust bootstrap.

## 3. Delegation and revocation

A DelegationGrant MUST bind:
- unique grant and issuer identity;
- grantor PrincipalRef and delegate PrincipalRef;
- permitted actions and resource classes/identifiers;
- exact ScopeRef roles and EnvironmentRef constraints;
- audience, purpose and tenant/security domain;
- not-before, expiry and revocation handle;
- parent DelegationGrant/chain and sub-delegation constraints;
- integrity/signature and policy version.

Validation requires trusted issuer, active grantor authority, active delegate, complete parent chain, non-amplification, cycle/depth limits, exact audience/purpose/action/resource/Scope match, time validity and current revocation. Effective authority is the intersection of grantor authority and every chain link. Missing/expired/revoked/indeterminate grant fails closed. ActorRef records delegate and acting-for Principal separately; delegation does not change identity or ownership.

Revocation is authoritative when committed by I. It advances affected PermissionEpoch domains. New admission is denied. In-flight work not yet across its owner-defined irreversible commit/disclosure point MUST revalidate and abort if revocation wins. Completed disclosure cannot be recalled; it creates an honest residual-disclosure/recipient-reconciliation record.

## 4. Authorization policy

Every protected operation binds the complete logical tuple:

`(PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Action, ResourceRef, PermissionEpoch, DelegationChainRef)`

Also bind purpose, audience, ownership Scope, applicability Scope set, policy version, obligations, expiry and authenticated Producer/Adapter/RuntimeSession binding when relevant.

Default deny:
1. Missing required tuple member or unresolved typed ref => DENY/INDETERMINATE.
2. Cross-Scope access requires an explicit current grant naming source/target ScopeRefs, action, resource, purpose, audience and expiry.
3. Cross-Environment access requires an explicit grant naming exact source/target EnvironmentRefs and permitted operation/resource class.
4. Parent/child/sibling/tenant/Agent/project/session similarity does not imply access.
5. Ownership Scope and applicability Scope are evaluated independently; applicability is not a read grant.
6. Relation traversal, Evidence/Provenance dereference and derived summaries independently authorize every endpoint/source.
7. No wildcard or implicit superuser. Break-glass is a separately governed, short-lived, reasoned and audited path.
8. A grant cannot exceed the intersection of Principal, delegation, issuer trust, action, resource, Scope, Environment, purpose, audience and time constraints.

Transport integrity, signature validity, typed-ref resolution, durable custody and capability negotiation are not authorization.

## 5. PermissionEpoch contract

### 5.1 Authority and namespace

I is the sole logical authority for PermissionEpoch. It is an opaque, monotonically advancing token within a named policy domain. A policy domain MUST be explicit and deterministic (for example tenant/security domain + policy namespace). Epochs from different domains are incomparable.

The authoritative record binds policy-domain ID, epoch token, policy version/digest, commit sequence, effective time, invalidation reason, affected subject/grant/resource/Scope selectors, issuer/trust changes and integrity metadata. High-risk operations require durable, strongly consistent currentness.

### 5.2 Increment conditions

Advance each affected policy domain whenever a change can alter authorization:
- Principal, credential, issuer, key trust/status/expiry/revocation;
- grant, role, action, resource, purpose, audience or obligation;
- delegation creation, narrowing, expiry, revocation or parent-chain change;
- Scope/Environment membership, ownership, status, federation or boundary grant;
- Producer/Agent/Adapter/recipient registration, authorization or revocation;
- policy rule/version, classification or retention constraint;
- emergency response or detected epoch-stream continuity failure.

No-op metadata changes need not advance the epoch if they cannot change authorization, but remain auditable. A multi-domain change advances each affected domain independently.

### 5.3 Propagation, cache invalidation and old-epoch behavior

I publishes ordered epoch/invalidation events and exposes authoritative current-epoch validation. Consumers track highest contiguous applied epoch per domain. Gaps, out-of-order events, offline state or failed subscribers do not prove freshness.

Before each protected operation, and again at irreversible commit/disclosure for high-risk actions, the owner MUST:
- obtain online authoritative current decision/epoch; or
- validate an I-issued, non-transferable lease bound to audience/resource/action/Scope with explicitly approved maximum staleness and expiry.

Cache TTL is never authorization validity. Cached ALLOW is usable only after online proof that the policy-domain PermissionEpoch remains current and all identity/resource/Scope/audience/purpose/delegation inputs match. Offline authorization leases, stale-epoch grace and cached ALLOW without currentness proof are prohibited in this Phase 3.6 baseline. Old, stale, unknown or incomparable epoch MUST be rejected; consumers fail closed on currentness uncertainty. Invalidation must evict/mark unusable decisions, sessions, derived grants and local authorization caches bound to the affected domain.

### 5.4 Distinction from ForgetFenceGeneration

PermissionEpoch and D ForgetFenceGeneration are distinct typed namespaces with different owners and meanings:
- PermissionEpoch: I policy authorization freshness.
- ForgetFenceGeneration: D canonical suppression/fence applicability.
Never compare, increment, convert, substitute or use one as evidence for the other. A protected publication/disclosure may require both independently at its final boundary.

## 6. Governance approval register

The following decisions require a named formal governance authority, durable decision record, approval timestamp and effective policy version. No such approval evidence is present in the inspected baseline; therefore each remains GOVERNANCE-BLOCKED.

| Decision | Policy owner | Required approving body / evidence | Status |
|---|---|---|---|
| Trusted issuer admission, federation and trust-domain rules | I | Named Security Governance approver; signed decision ID, issuer/trust-domain scope, effective version | GOVERNANCE-BLOCKED |
| Principal taxonomy/registration and cross-issuer identity linking | I (B types) | Named Identity Governance approver and registry policy version | GOVERNANCE-BLOCKED |
| Delegation eligibility, maximum chain depth, sub-delegation and acting-for rules | I | Named Security Governance approver and approved grant profile | GOVERNANCE-BLOCKED |
| Cross-Scope grants/sharing/inheritance and break-glass | I + B semantics | Named Data/Scope Governance approver; exact grant policy version | GOVERNANCE-BLOCKED |
| Cross-Environment bridge/federation | I + Environment owner | Named Environment Governance approver; mapping and policy version | GOVERNANCE-BLOCKED |
| PermissionEpoch domains, bounded offline lease/staleness and revocation SLA | I | Named Security Governance approver; epoch service/profile version | GOVERNANCE-BLOCKED |
| Revocation effective point and in-flight operation semantics | I + each boundary owner | Named Security Governance approver plus D/E/F/G/H boundary acknowledgements | GOVERNANCE-BLOCKED |
| Administrative/break-glass operations | I | Named independent approver, reason, expiry, audit and emergency policy | GOVERNANCE-BLOCKED |

**No approver is invented.** The existing Governance Decision Register remains the authority for recording approvals. Until it contains a named approving principal/body, decision ID, approval time and effective version, policy remains GOVERNANCE-BLOCKED. Owner-authored proposal is not governance approval.

## 7. Protected-operation enforcement requirements

- Memory Event Ingress: H authenticates workload; I resolves ProducerRef/Principal/Actor and authorizes exact ingress; C validates semantic claims; E validates durable receipt and producer admission.
- Compiler Publication: E checks producer/work admission, complete dependency lineage, current I PermissionEpoch and D ForgetFence at the same final visibility linearization boundary.
- Retrieval: F rechecks authorization and current epoch before candidate disclosure; stale caches cannot emit data.
- Context Delivery: G/H bind recipient, ContextVersion, DeliveryId/attempt, session, Scope and current epoch before disclosure/application.
- Applied ACK: H transports evidence; C/G validate Applied predicates and I validates signer, target, Scope and current policy; old ACK is historical only.
- Forget ACK: H supplies action/region/instance-bounded evidence; I alone evaluates target state and exceptions; ACK cannot grant access or close global completion.
- Reconnect: reauthenticate and revalidate trust/permission before stale local state is reconciled or protected operation resumes.
- Administrative Operation: separately registered action/resource, strong authentication, explicit Scope, short-lived approval, dual control where required and immutable audit.

Every consumer enforces at its own boundary; an upstream ALLOW is not a transferable blanket capability.

## 8. Test plan and evidence status

All cases below are **Specified / NOT EXECUTED**. No test is Passed without reproducible implementation evidence.

| ID | Scenario | Expected result | Test status |
|---|---|---|---|
| I36-01 | Forged PrincipalRef | Ignore as auth; reject mismatch with protected Principal | Specified / NOT RUN |
| I36-02 | Forged ActorRef | Reject caller-minted/unbound ActorRef | Specified / NOT RUN |
| I36-03 | Forged ProducerRef | Reject unless authenticated workload resolves to registered producer | Specified / NOT RUN |
| I36-04 | Unknown Issuer | Deny; no TOFU/bootstrap | Specified / NOT RUN |
| I36-05 | Revoked Issuer/key | Deny new work; invalidate affected sessions/decisions | Specified / NOT RUN |
| I36-06 | Expired Credential | Deny at protected boundary | Specified / NOT RUN |
| I36-07 | Expired Delegation | Deny; do not fall back to represented Principal | Specified / NOT RUN |
| I36-08 | Revoked Delegation | Deny and advance affected PermissionEpoch | Specified / NOT RUN |
| I36-09 | Stale PermissionEpoch | Deny/reauthorize; no protected operation | Specified / NOT RUN |
| I36-10 | Cross-Scope access | Deny without explicit current grant | Specified / NOT RUN |
| I36-11 | Cross-Environment access | Deny without explicit bridge and grant | Specified / NOT RUN |
| I36-12 | Authenticated Principal vs payload ActorRef mismatch | Reject/quarantine and audit | Specified / NOT RUN |
| I36-13 | Old Session ACK replay | Historical only; no state rollback | Specified / NOT RUN |
| I36-14 | Reconnect during revocation | Block stale state; current auth/epoch required before resume | Specified / NOT RUN |
| I36-15 | Unauthorized Forget operation | Deny before fence/target mutation; audit attempt | Specified / NOT RUN |

Evidence required per executed test: build/commit, test harness/version, issuer/key fixture, policy domain and epoch, protected transport context, operation/resource/Scope, expected/actual result, logs/evidence digest and reviewer. No credentials or protected plaintext in logs.

## 9. Joint decision and non-claims

- **B Owner Decision:** B semantic proposal consumed; no B approval inferred.
- **I Owner Decision (current):** Phase 3.6 technical policy design DECIDED under delegated joint authority; external governance approval remains GOVERNANCE-BLOCKED.
- **H Owner Decision:** H wire/authentication mapping approval remains OPEN.
- **Cross-module Agreement (current):** BIH Phase 3.6 technical design DECIDED under delegated joint authority; C/D/E/F/G/Storage consumer acceptance remains OPEN.
- **Governance Approval:** GOVERNANCE-BLOCKED; no named approver, decision record and effective version evidenced.
- **Implementation Evidence:** NOT PROVIDED / NOT VERIFIED; tests NOT RUN.
- **Fact/Claim ADR-001:** remains independently ADR-BLOCKED. This policy proposal does not resolve it.

No contract freeze, production security certification, implemented issuer registry, implemented epoch service, complete revocation propagation or runtime security PASS is claimed.

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

## 10. Phase 3.6 Self-Review Remediation — Binding I Clarifications

This section resolves I36-SR-01..07 and is normative for the I Phase 3.6 technical baseline. It does not activate governance-blocked policy profiles.

### 10.1 Principal collision, alias and migration (I36-SR-01)

The canonical resolution key is `(IssuerRef, TrustDomainRef, TenantRef, PrincipalKind, IssuerSubject)`. Subject equality across issuers, trust domains, tenants or kinds MUST NOT merge Principals. Key rotation under the same IssuerRef does not by itself create a new Principal. Issuer subject-format migration requires an explicit signed issuer migration assertion plus I registry approval, preserving the old key as a historical alias with effective interval, provenance and audit trail. Alias linking is one-way and non-authoritative for authentication: both old and new identifiers resolve only through I's registry, and revocation of either alias follows the recorded migration policy. Principal merge is prohibited by default; any future merge requires a separately governed migration procedure, dual-control approval, collision analysis and immutable audit lineage. No automatic email/name/subject similarity linking is permitted.

### 10.2 PermissionEpoch consistency and revocation linearization (I36-SR-02 / I36-SR-05)

Each policy domain has a single logical I authority backed by a linearizable commit sequencer. Authorization decisions and revocation commits for that domain are totally ordered by that sequencer. Revocation becomes effective at the sequencer's committed epoch-advance point; no replica-local clock or eventually consistent cache can declare it effective earlier or later.

A protected irreversible operation must obtain a single-use I CommitAuthorizationReceipt bound to:
`(policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation_id, operation_payload_digest, owner_boundary, decision_id)`.
The receipt is not a transferable permission and is not an offline lease. The operation owner MUST submit the receipt to its final commit/disclosure gate, which participates in the same per-domain commit ordering protocol. The gate atomically orders the operation commit against revocation:
- if operation commit is sequenced first, it may complete and the audit record states COMMIT_WON;
- if revocation epoch advance is sequenced first, the receipt is rejected and the operation states REVOCATION_WON;
- if ordering cannot be established, the operation is paused/aborted and no success is reported.

Receipt replay, changed operation digest, changed boundary, stale epoch, duplicate commit, or expired/unknown receipt is rejected. A receipt is single-use. The owner records receipt ID, decision ID, sequencer position, epoch, operation digest and terminal outcome. This is a required protocol contract; implementation evidence is still NOT VERIFIED.

### 10.3 Canonical policy-domain identity and multi-domain operations (I36-SR-03)

A policy domain is a registered I-owned policy partition with immutable `PolicyDomainRef`. Its canonical identity is assigned by I registry and is not computed ad hoc by consumers. Registry metadata binds tenant/security domain, policy authority, resource classes, issuer trust set, epoch stream ID, status and policy version. Consumers may not derive a domain from labels or concatenate arbitrary fields.

An operation touching resources in multiple policy domains MUST obtain a current epoch and commit authorization for every domain. It is permitted only if the I coordinator can atomically reserve/sequence the full domain set as one all-or-none decision. Partial ALLOW is never sufficient. If a common coordinator is unavailable, domain membership is ambiguous, epochs cannot be proven current, or atomic ordering cannot be achieved, the operation is DENIED/PAUSED. Domain migration is an explicit I registry event with old/new domain mapping, migration epoch, cutover position and audit record; old epochs are never reinterpreted in the new domain.

### 10.4 Offline lease rule — no lease is active (I36-SR-04)

For this Phase 3.6 baseline, **offline authorization leases, cached ALLOW based on a lease, and stale-epoch grace are prohibited**. Remove any implication that an I-issued bounded lease is currently usable. Cache TTL is only a performance hint: a cached decision is usable only after online proof that its PermissionEpoch is current and all bound inputs still match. If currentness cannot be checked, deny/pause. A future bounded lease requires a new explicit governance approval and a new versioned policy profile; this addendum does not enable one.

### 10.5 Required revocation evidence and race audit (I36-SR-05)

Every operation owner must retain a verifiable terminal ordering record containing I decision ID, CommitAuthorizationReceipt ID, policy-domain sequencer position(s), PermissionEpoch(s), operation digest, owner commit cursor/transaction ID, revocation event ID/epoch where relevant, and terminal outcome `COMMIT_WON`, `REVOCATION_WON` or `INDETERMINATE_ABORTED`. INDETERMINATE_ABORTED is never reported as success. If the operation cannot expose this evidence, it is not eligible for protected production operation.

### 10.6 Test additions (I36-SR-07)

Add mandatory adversarial cases: (a) epoch read races revocation commit; (b) operation receipt commit races revocation and both sequencer orderings are checked; (c) cross-domain partial authorization failure; (d) multi-domain coordinator outage; (e) issuer subject collision across issuers/tenants/kinds; (f) key rotation overlap, rollback and revoked old key; (g) alias migration replay and attempted Principal merge. All are **SPECIFIED / NOT RUN** until runtime evidence is attached.

### 10.7 I decision-state reconciliation (I36-SR-06)

The older Section 9 Owner Decision and Cross-module Agreement lines are superseded as process status for the BIH technical design only. Current state: **I technical policy design DECIDED under the user's delegated joint decision.** External governance approval remains **GOVERNANCE-BLOCKED** for the enumerated profiles; no external approver, signature, jurisdictional approval or policy activation is inferred. C/D/E/F/G/Storage acceptance remains OPEN. Runtime verification remains NOT RUN. ADR-001 remains ADR-BLOCKED.
