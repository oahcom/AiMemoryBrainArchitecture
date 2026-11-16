# Session I — Phase 3.6 Principal Trust Chain, Authorization & Revocation Closure

- Owner: Session I — Security, Identity & Governance Principal Architect
- Status: **CANDIDATE policy contract; GOVERNANCE-BLOCKED; implementation and conformance NOT VERIFIED**
- Date: 2026-11-16
- Branch: `session-i-security-governance-2026-11-16`
- Consumes: B Typed Reference Registry; C Telemetry Event and Identity Contract; D Forget Fence Operation and Publication Gate; E Forget Fence and Derived Registration; H Phase 3.5 Identity/Applied/ACK/Reconnect contract; A Phase 3.5 Cross-Module Closure Review.
- Authority boundary: I owns issuer trust policy, Principal registration, authorization, delegation, revocation, PermissionEpoch, retention and global Forget governance. B owns typed-reference semantics; C owns telemetry semantics; D owns canonical Forget operation/fence; E owns compiler execution; H owns transport/wire; I does not redefine their schemas or local mechanisms.

## 0. Evidence baseline and limitations

The following branch tips were queried from GitHub before this write:

| Source | Branch | HEAD |
|---|---|---|
| A closure review | `session-a-integration-2026-11-16` | `5ce61e0982ce8e22b29f1267ca67c9a085a96a06` |
| B typed reference registry | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` |
| C telemetry identity | `session-c-agent-integration-2026-11-16` | `a585307222b0169c007915c25ff8ed0da517f3e4` |
| D protected operation | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` |
| E protected operation | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` |
| H identity / applied | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` |
| I source baseline | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` |

A's review explicitly records INT-P0-02 as open: authenticated Principal/Issuer → ActorRef/ProducerIdentity/Adapter/Agent → ScopeRef → PermissionEpoch lacks jointly approved cross-owner semantics and executed negative tests. It also records no signed governance approval. The review is **BLOCKED for Contract Freeze and Implementation Planning**.

**Required Phase 3.6 artifact gap:** the queried B branch exposes `typed-reference-registry.md` and `typed-reference-and-scope-semantics.md` (both Phase 3.5-labelled); C exposes `telemetry-event-and-identity-contract.md`; D exposes `forget-fence-operation-and-publication-gate.md`; E exposes `forget-fence-and-derived-registration.md`; H exposes `phase-3-5-identity-applied-ack-reconnect-contract.md`. No separately named B Phase 3.6 Typed Reference Registry, H Phase 3.6 Identity Binding, C Phase 3.6 Telemetry Identity, or H Phase 3.6 protected-operation binding artifact was present in the inspected branch trees. The available artifacts are consumed as provisional source material, not represented as Phase 3.6 approvals. Reconcile when those owner artifacts are published.

No implementation, executable test output, signed approval, deployed issuer registry, policy service, epoch store or production atomicity proof was supplied. This document defines testable semantics only.

## 1. Principal Trust Chain

Normative path:

`Authenticated Transport → Issuer Validation → Principal Resolution → Delegation Validation → ActorRef Resolution → Scope Authorization → PermissionEpoch Validation → Protected Operation`

Each stage MUST produce verifier-owned evidence. A later stage MUST NOT reconstruct trust from payload fields or skip a failed/indeterminate earlier stage.

| Step | Owner | Inputs | Output / evidence | Failure semantics |
|---|---|---|---|---|
| 1. Authenticated Transport | H for BMCP transport/session; platform ingress for other transports | Protected channel/session, peer/workload credential proof, channel binding, nonce/replay context | Verifier-authenticated transport context bound to connection/session, audience and observed time | Missing, unprotected, replayed, channel-mismatched or unverifiable transport → reject; no payload identity promoted |
| 2. Issuer Validation | I trust policy; cryptographic verifier at H/ingress | Credential/signature, issuer key ID, credential type, audience, tenant/security domain, nbf/exp, key status | Validated IssuerRef + credential verification result + trust-registry version/key epoch | Unknown/revoked issuer or key, invalid signature, wrong audience/domain/type, expired/not-yet-valid credential, unavailable trust state → DENY/INDETERMINATE |
| 3. Principal Resolution | I Principal registry | Validated issuer subject, namespace, principal kind, tenant/security domain, registry status | Stable PrincipalRef and registered status/identity binding | Unknown, retired, suspended, ambiguous, mismatched or unregistered Principal → deny/quarantine; never auto-register from claim |
| 4. Delegation Validation | I Delegation registry/policy | Grant chain, grantor/delegate PrincipalRefs, issuer, actions, resource classes, scopes, audience, purpose, nbf/exp, parent links, revocation handles | Validated immutable DelegationChainRef and effective authority intersection | Missing/expired/revoked/invalid signature/cycle/depth overflow/audience or scope mismatch/authority amplification → deny |
| 5. ActorRef Resolution | H supplies authenticated subject binding; I validates; B owns ActorRef type | Authenticated PrincipalRef, validated delegation chain, Producer/Agent/Adapter bindings, operation correlation | Resolved B ActorRef bound to verifier evidence, operation, Principal and chain | Payload-only or caller-constructed ActorRef, mismatch, unresolved typed ref or missing binding → reject; ActorRef is not a credential |
| 6. Scope Authorization | I policy; B owns ScopeRef semantics and registry typing | Principal, ActorRef, ScopeRef(s), EnvironmentRef, Action, Resource, purpose, audience, delegation chain, ownership/applicability bindings | Decision (ALLOW/DENY/INDETERMINATE), obligations, policy version and exact scope coverage | Unknown scope/environment, missing required dimension, implicit inheritance, cross-scope/environment without explicit grant → deny |
| 7. PermissionEpoch Validation | I is authority; each consumer validates through I or a verifiable I-issued bounded lease | Current policy-domain epoch, decision epoch, revocation stream continuity, decision expiry, subject/resource binding | Current authorization proof bound to policy domain/epoch and validity interval | Stale/gapped/unknown epoch, offline authority without approved bounded policy, expired decision, revocation uncertainty → pause/deny |
| 8. Protected Operation | Owning enforcement module: D/E/F/G/H/C boundary; I supplies policy | All prior verifier evidence + action/resource + final-boundary epoch and local fence/cursor state | Operation-specific durable receipt/audit decision and outcome | Any missing proof, policy change before linearization, stale fence or ambiguous outcome → abort/quarantine; never report success |

Audit evidence at every stage MUST include correlation/operation ID, stage, verifier/owner, opaque typed refs or approved non-reversible fingerprints, issuer/key/trust-registry version, decision/reason code, policy domain/epoch where applicable, timestamp/clock quality, and evidence integrity metadata. Never log credentials, bearer tokens, private keys, raw protected content or reconstructive payload excerpts.

## 2. Issuer Trust Contract

### 2.1 Trusted Issuer Registry

I owns the logical Trusted Issuer Registry. Each issuer record MUST bind:

- stable, non-recycled IssuerRef and TrustDomainRef;
- issuer legal/operational owner and accountable security contact;
- allowed tenant/security domains and federation mappings;
- credential/attestation types, signing algorithms and key IDs;
- allowed audiences, subject/principal kinds and claim namespaces;
- validity, activation, suspension, revocation and retirement state;
- key rotation schedule, overlap policy and emergency compromise procedure;
- trust-policy version, approval evidence and review/expiry date.

Trust is explicit and non-transitive. Trusting issuer A does not trust issuer B, a parent domain, a downstream issuer or a delegated issuer unless an explicit approved federation/delegation mapping exists.

### 2.2 Issuer identity and credential rules

Issuer identity is established from validated cryptographic/protected transport metadata and the configured trust registry, not from an untrusted payload string. Payload `issuer`, `principal`, `actor_ref`, `producer_id`, `agent_id`, `adapter_id`, `tenant` and `environment` are claims/selectors only.

A credential MUST be validated for issuer, key ID, signature or protected-channel proof, credential type, audience, tenant/security domain, subject namespace, not-before, expiry, revocation status and permitted authentication strength. Subject strings are resolved only within the validated issuer namespace.

### 2.3 Rotation, revocation and expiry

- Planned key rotation uses explicit key IDs and a bounded overlap period. Old and new keys may coexist only for the approved overlap; the old key is retired at the recorded cutover.
- Emergency compromise revokes the affected key/issuer immediately in the authoritative trust registry, advances the affected PermissionEpoch domain, invalidates dependent credentials/sessions/delegations and triggers consumer reconciliation.
- Issuer revocation blocks new authentication and all new protected work under that issuer. In-flight work must reauthorize at its next protected boundary.
- Principal/credential expiry is evaluated at each protected operation, not only at initial connection. Session renewal requires fresh validation.
- Unknown issuer/key, revoked issuer/key, unsupported algorithm, unknown trust domain, invalid audience, expired credential or unavailable revocation status fails closed.
- No automatic trust-on-first-use, payload-driven trust bootstrap or implicit fallback issuer is permitted.

## 3. ActorRef and Producer Identity Binding

ActorRef is a typed attribution reference, not a credential, capability or permission. The Principal is the authenticated security subject; ActorRef identifies the actor responsible for one operation and preserves the verified authority/delegation chain.

| Identity layer | Meaning / owner | Required binding | Forbidden shortcut |
|---|---|---|---|
| Principal | I: stable human, Agent, workload, service, Adapter or recipient security subject | Trusted issuer + valid credential + I registry entry + tenant/security domain | Display name, email, model name or payload ID |
| Agent Identity | Agent registry; I binds to Principal; C defines telemetry semantics | Logical AgentRef mapped to Agent Principal and approved action/scope profile | Agent label/family or self-asserted agent_id |
| Producer Identity | I registration/trust; C telemetry claim semantics; H transport binding | ProducerRef/class/instance mapped to Principal, issuer, credential epoch, source/event family and Scope coverage | Payload producer_id, queue name, event source_id |
| Adapter Identity | H owns Adapter protocol/capability registration; I owns Principal trust/policy | Adapter Principal + registered AdapterRef/application + authenticated instance + live session + capability profile/epoch | Adapter display name, payload adapter_id or session ID alone |
| Runtime Session | H/platform session authority; I policy | Authenticated session bound to Principal, instance, audience, environment/task scope, expiry and revocation | Reusing an expired or different session |
| ActorRef | B typed reference; H binds; I validates | Resolved from authenticated Principal + validated delegation + operation binding | Caller-supplied ActorRef treated as proof |

Producer registration MUST precede admission. An unregistered, disabled, quarantined, expired or revoked producer cannot ingest, enqueue, lease, dereference source data, compile, replay, derive or publish. A payload producer claim must exactly resolve to the authenticated registered ProducerIdentity and its allowed event family/scope. Mismatch is rejected and audited. No payload can create or widen a Producer registration.

## 4. Scope Authorization Contract

### 4.1 Required authorization tuple

Every protected operation evaluates the complete logical tuple:

`(PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Action, ResourceRef, PermissionEpoch, DelegationChainRef)`

The decision also binds purpose, audience, ownership Scope, applicability Scope set, policy version, obligations, expiry and authenticated producer/adapter/session binding where relevant.

- **PrincipalRef:** resolved authenticated subject.
- **ActorRef:** verifier-resolved operation attribution and delegation provenance.
- **ScopeRef:** B-owned typed scope; resolve kind, authority, namespace, status, owner and explicit relationships.
- **EnvironmentRef:** exact registry-backed environment whenever resource, action, query, Agent or Adapter is environment-dependent.
- **Action:** registered verb/action, not caller-invented free text.
- **ResourceRef:** exact object/version or registered resource class with ownership and classification.
- **PermissionEpoch:** I-issued current epoch for the applicable policy domain(s); never a fence generation.
- **DelegationChainRef:** complete validated chain or explicit absence when direct authority applies.

### 4.2 Default-deny rules

1. Missing required tuple member or unresolved typed reference → DENY/INDETERMINATE.
2. Cross-Scope access is denied unless an explicit current grant identifies source and target ScopeRefs, action, resource, purpose, audience and expiry.
3. Cross-Environment access is denied unless an explicit grant binds both exact EnvironmentRefs and permitted operation/resource class.
4. Parent/child/sibling/tenant/Agent/project/session similarity never implies access.
5. Ownership Scope and applicability Scope are evaluated independently; applicability is not a read grant.
6. Relation traversal, evidence/provenance dereference and derived summaries require independent authorization of every endpoint/source.
7. No broad wildcard or implicit superuser grant. Break-glass is a separate short-lived, reasoned, independently auditable policy path and remains subject to governance approval.
8. A grant cannot exceed the intersection of Principal authority, delegated authority, issuer trust, action, resource, scope, environment, purpose, audience and time.

## 5. PermissionEpoch Contract

### 5.1 Authority and scope

I is the sole logical authority for PermissionEpoch. Epochs are opaque, monotonically advancing tokens within a named policy domain. A policy domain MUST be explicitly named and cover a deterministic authorization partition (for example tenant/security domain plus policy namespace); a consumer MUST NOT compare epochs from different domains.

The authoritative epoch record binds policy-domain ID, epoch token, policy version/digest, commit sequence, effective time, revocation/invalidation reason, affected subject/grant/resource/scope selectors, issuer/trust changes and integrity metadata. The epoch authority must be durable and strongly consistent for high-risk protected operations.

### 5.2 Increment conditions

Advance the affected policy-domain PermissionEpoch whenever a change can alter an authorization result, including:

- Principal/credential/issuer/key trust, status, expiry or revocation;
- grant, role, action, resource, purpose, audience or obligation changes;
- DelegationGrant creation, narrowing, expiry, revocation or parent-chain change;
- Scope/Environment membership, ownership, status, federation or cross-boundary grant change;
- Producer/Agent/Adapter/recipient registration, capability authorization or revocation;
- policy rule, policy version, classification or retention constraint changes;
- emergency security response or detected epoch-stream continuity failure requiring a new policy generation.

No-op metadata changes that cannot affect authorization need not advance the epoch, but must be auditable. A single change affecting multiple policy domains advances each affected domain independently; no shared scalar across domains is implied.

### 5.3 Propagation and validation

I publishes ordered epoch/invalidation events and exposes an authoritative current-epoch validation path. Consumers track the highest contiguous applied epoch per policy domain. Gaps, out-of-order events, unknown epoch, offline status or failed subscriber are not proof of freshness.

Before each protected operation, and again at the irreversible commit/disclosure boundary for high-risk actions, the owner MUST either:
- obtain an online authoritative current decision/epoch; or
- validate an I-issued, non-transferable, audience/resource/action/scope-bound authorization lease whose maximum staleness and expiry are explicitly approved for that operation class.

A cache TTL is only an upper bound. A cached ALLOW is usable only if its domain epoch is proven current (or an approved bounded lease remains valid) and all bound identity, resource, scope, audience, purpose and delegation inputs match exactly. Old epoch never proves current authorization.

### 5.4 Non-interchangeability

`PermissionEpoch` MUST NOT be compared, incremented, converted, substituted or interpreted as `ForgetFenceGeneration`, `CanonicalCommitCursor`, `ProducerRegistrationHighWater`, `ProducerDomainInventoryEpoch`, `IndexWatermark`, `ContextVersion` or `AdapterCapabilityEpoch`. Each has a different owner, namespace and proof meaning.

## 6. Revocation Semantics and Race Matrix

Revocation is authoritative when committed by I's policy/trust authority. At that point the affected PermissionEpoch advances. New admission under the revoked authority is denied. An in-flight operation that has not crossed its owning irreversible commit/disclosure linearization point MUST revalidate and abort if authorization is no longer valid. A completed disclosure cannot be recalled; it triggers recipient/Forget handling and honest residual disclosure records.

| Concurrent boundary | Required ordering / recheck | If revocation wins before boundary | If operation linearizes first | Evidence / owner |
|---|---|---|---|---|
| Publish / derived artifact visibility | E must validate I current PermissionEpoch and D latest ForgetFence in the same final visibility gate/transaction semantics; D owns fence, I owns permission | Keep staged artifact private; abort/quarantine; do not register visible derivative | Publication remains a pre-revocation event; later access/retrieval must enforce new epoch and cleanup obligations | E publication receipt + D fence proof + I decision/epoch; storage atomicity remains open |
| Retrieval / candidate exposure | F rechecks current permission before candidate emission and finalization; no post-filter-only approach | Do not emit candidate, count, snippet or side-channel signal; invalidate cache/Working Set | Already returned data cannot be recalled; subsequent retrieval denied and incident/Forget workflow may apply | F decision and epoch evidence, cache invalidation; I policy |
| Context delivery | G/H reauthorize exact recipient, ContextVersion, DeliveryId, session, Scope and PermissionEpoch before send/apply | Cancel/quarantine pending delivery; stale deltas/snapshots cannot apply | Delivery bytes already disclosed are not retractable; recipient target enters revocation/Forget reconciliation | G intent/reconciliation + H authenticated delivery evidence + I epoch |
| Adapter apply / reconnect | H requires fresh Principal/session/capability and I epoch plus D fence before managed-region activation | Keep region suppressed/quarantined; reconcile/clear before use | Existing managed region must be suppressed on next boundary; no stale state may be reused | H target/session/ACK evidence; G Context; I epoch |
| Applied / final inference submission | C/H/G final-request boundary must validate exact request, managed region, Context/Delivery, session, current PermissionEpoch and D fence immediately before submission | Do not submit affected Memory region/request; no Full Applied attestation | Submission is a disclosure linearization point; later revocation cannot recall request but must block subsequent submissions and start applicable cleanup | C final-request attestation + H transport/target binding + G version + I epoch + D fence |
| Canonical mutation / commit | D validates current I decision/epoch at canonical commit linearization point and separately checks D fence | Reject commit; preserve idempotency/terminal failure evidence | Mutation is ordered before revocation; future reads/derived operations still reauthorize | D commit receipt + I epoch decision |
| Export / external recipient | I authorizes exact recipient, destination, purpose, scope and retention immediately before export | Abort queued export; invalidate pending credential/recipient grant | Already transferred copy cannot be recalled; initiate recipient deletion/withdrawal process | Export receipt, recipient identity/issuer, I decision and epoch |

Uncertain ordering, lost epoch events, unknown commit result or unavailable authority is not resolved optimistically. The operation remains pending/unknown and is reconciled from durable owner evidence. Revocation MUST NOT be treated as a ForgetFence installation; conversely, ForgetFence does not revoke Principal permission.

### 6.1 Forget continuity

Revoking the initiating Principal does not cancel an already accepted canonical Forget obligation. D's fence and barrier remain authoritative. Cleanup continues only under a separately authenticated, currently authorized service/continuity Principal with least privilege. The revoked requester ActorRef, cached ALLOW or session cannot be reused as cleanup authority. If that service authority is unavailable, cleanup pauses without reopening access.

## 7. Authorization Decision Table

| Condition | Decision | Mandatory behavior |
|---|---|---|
| Valid issuer, Principal, ActorRef, delegation, scope, environment and current epoch; action/resource grant matches | ALLOW (subject to obligations) | Execute only within exact bound tuple; revalidate at final boundary |
| Unknown issuer/key or revoked issuer/key | DENY | Reject authentication; audit trust failure |
| Payload Principal/issuer/ActorRef differs from authenticated binding | DENY | Reject/quarantine; do not create trusted registration |
| Unknown/unregistered/revoked producer or Adapter | DENY | Block ingress/admission/apply; do not infer identity from payload |
| Expired or revoked delegation / parent chain | DENY | Invalidate descendants and leases |
| Missing required ScopeRef or EnvironmentRef | INDETERMINATE → block | No wildcard/default environment |
| Cross-Scope or cross-Environment without explicit grant | DENY | No candidate/dereference/delivery/disclosure |
| Scope matches but action/resource grant absent | DENY | Scope is not permission |
| Stale/gapped/unknown PermissionEpoch or unavailable authoritative revocation state | INDETERMINATE → block | Pause protected operation and reconcile |
| Cached ALLOW with TTL remaining but no current epoch proof | DENY/INDETERMINATE → block | TTL does not prove current authorization |
| D ForgetFence active or stale at final publish/read/delivery | DENY for affected target | D fence wins independently of permission |
| Permission ALLOW but D fence blocks target | DENY for affected target | No permission decision overrides Forget |
| Unsupported adapter capability for required action | INDETERMINATE / Unknown | No success; alternative control or approved exception required |
| Governance decision required but no approval evidence | GOVERNANCE-BLOCKED | Keep policy candidate; no production enablement |

## 8. Governance Decision Register — Phase 3.6

Every decision below is **GOVERNANCE-BLOCKED** until an append-only approval record contains exact approved text/hash, approver PrincipalRef and Issuer, authority basis, independent reviewer where required, evidence/test refs, scope/jurisdiction, effective policy version/time, expiry/review and revocation/supersession conditions. A code/document commit or architect recommendation is not approval.

| ID | Decision requiring approval | Required approving authority | Current state |
|---|---|---|---|
| I36-GOV-01 | Trusted Issuer Registry admission, federation, trust-domain and key/credential rotation/compromise policy | Identity/Security Governance; issuer owner; Privacy/Legal where jurisdictional | GOVERNANCE-BLOCKED |
| I36-GOV-02 | Delegation policy: eligible grantors/delegates, depth, sub-delegation, audience/purpose, expiry and parent revocation | Security Governance; Identity Governance; Legal where agency/consent applies | GOVERNANCE-BLOCKED |
| I36-GOV-03 | Cross-Scope grants and any inheritance/sharing algebra | Security/Architecture Governance; B domain owner; data/tenant owner | GOVERNANCE-BLOCKED |
| I36-GOV-04 | Cross-Environment grants and federation boundaries | Security/Architecture Governance; environment owner; data/tenant owner | GOVERNANCE-BLOCKED |
| I36-GOV-05 | Revocation effective point, in-flight linearization, offline behavior and already-disclosed data handling | Security Governance; D/E/F/G/H/C boundary owners; service owner | GOVERNANCE-BLOCKED |
| I36-GOV-06 | PermissionEpoch authority, policy-domain partitioning, increment/propagation and bounded authorization leases | Security Governance; identity/policy platform owner; all consumers | GOVERNANCE-BLOCKED |
| I36-GOV-07 | Unsupported Adapter/producer policy, alternate controls, disablement and residual-risk handling | Security Governance; H; service/product owner; Privacy/Legal if data leaves control | GOVERNANCE-BLOCKED |
| I36-GOV-08 | Global Forget Completion exceptions for external recipient, backup retention, unsupported/offline target and physical erasure | Privacy/Legal + Security Governance + data owner + storage/recipient owner | GOVERNANCE-BLOCKED |

No approval artifact was found in the reviewed I register or A closure review. These decisions remain proposals; none is effective.

## 9. Security Conformance Test Plan

The following are **test specifications only**. Status for every case is **NOT RUN**; no PASS/FAIL is claimed. An execution result requires executable fixture, environment/build, policy/issuer registry snapshot, expected and actual result, durable test artifact, timestamps, owner sign-off and non-sensitive audit evidence.

| Test ID | Adversarial scenario | Expected result | Required audit evidence | Owner(s) |
|---|---|---|---|---|
| I36-T01 | Forged PrincipalRef in payload with valid transport for another Principal | Reject claim mismatch; no impersonation | Authenticated subject fingerprint, claimed ref fingerprint, mismatch reason | H + I |
| I36-T02 | Forged ActorRef or caller-constructed ActorRef without verifier binding | Reject; ActorRef never authenticates | B type resolution, verifier binding absence, denial | B + H + I |
| I36-T03 | Unknown Issuer / unknown key ID | DENY/INDETERMINATE; no TOFU | Registry lookup/version, unknown issuer/key reason | I |
| I36-T04 | Revoked Issuer or compromised signing key | Reject new auth; invalidate dependent sessions/grants; epoch advance | Revocation event, affected domain epoch, consumer ACK/gap | I + H |
| I36-T05 | Expired delegation or expired parent grant | Deny delegate and all descendants | Chain refs, expiry/parent state, decision | I |
| I36-T06 | Delegation cycle, excessive depth or authority amplification | Deny chain | Chain digest, depth/cycle/amplification reason | I |
| I36-T07 | Stale PermissionEpoch with apparently valid cached ALLOW | Deny/pause despite unexpired cache TTL | Cached epoch, authoritative epoch, invalidation reason | I + consumer |
| I36-T08 | PermissionEpoch stream gap or authority unavailable | Pause protected operation; reconcile before resume | Last contiguous epoch, gap, blocked operation ID | I + consumer |
| I36-T09 | Cross-Scope access without explicit grant (tenant/user/project/Agent/task/session) | DENY; no candidate, count or graph side channel | Source/target Scope fingerprints, action, deny result | B + I + F/G |
| I36-T10 | Cross-Environment access with free-text or caller-supplied environment | DENY; require registry-backed EnvironmentRef and explicit grant | Authenticated environment binding, registry lookup, deny | B + I + C/H |
| I36-T11 | Producer self-asserts unregistered identity or mismatches authenticated ProducerIdentity | Reject before enqueue/lease/dereference/compile | Authenticated workload, registration status, payload mismatch | C + H + I + E |
| I36-T12 | Adapter identity spoof or session from another instance | Reject; managed region remains suppressed | Adapter Principal, instance/session binding, capability epoch | H + I |
| I36-T13 | Revocation races with E publication before final visibility linearization | Staged artifact remains private; publication denied | I epoch, D fence, E publication gate receipt/outcome | I + D + E + Storage |
| I36-T14 | Revocation races with F retrieval before candidate emission/finalization | No candidate/count/snippet disclosure; cache invalidated | Epoch at each boundary, candidate decision, cache disposition | I + F |
| I36-T15 | Revocation races with G/H delivery or Adapter apply | Cancel/quarantine pending delivery; reconnect requires fresh auth | DeliveryId, ContextVersion, session, epoch, cancel/apply result | I + G + H |
| I36-T16 | Revocation races with C final Applied / final inference submission | No submission if revocation linearizes first; no Full Applied | FinalRequestBoundaryId, exact request/session, epoch and fence | I + C + G + H |
| I36-T17 | PermissionEpoch incorrectly compared/substituted with ForgetFenceGeneration | Type/namespace validation rejects; independent checks remain | Both typed refs and rejected coercion | I + D + consumer |
| I36-T18 | Revocation after a disclosure already linearized | Do not claim recall; block future access and start recipient/Forget workflow | Disclosure receipt/time, revocation time, recipient target workflow | I + recipient owner |
| I36-T19 | Initiating Principal revoked after D Forget fence installed | Forget obligation persists; only current continuity Principal may clean up | D fence/barrier refs, revoked actor, cleanup Principal decision | I + D |
| I36-T20 | Unsupported Adapter action or offline recipient during Global Forget | Unknown/Pending; exception only with explicit approved evidence | Target/action, capability evidence, approver/expiry if exception | I + H + Privacy/Legal |

### 9.1 Conformance gate

- All identity/authorization tests MUST pass before Contract Freeze for INT-P0-02.
- Publish, retrieval, delivery and Applied race tests MUST run with deterministic pause points around each owning linearization boundary.
- Negative scope tests MUST include side-channel assertions, not only response-body checks.
- Test execution MUST be recorded separately from this test specification; editing this document never changes NOT RUN.
- Any failure affecting Principal authenticity, cross-tenant isolation, stale authorization or Forget resurrection is a release blocker unless the required independent authority explicitly approves a narrowly scoped exception. Cross-tenant disclosure and revocation bypass are not routine residual risks.

## 10. Relationship to existing I governance

This document extends, and does not silently approve, `principal-actor-and-authorization-contract.md`, `scope-and-revocation-policy.md`, `threat-model-and-adversarial-test-plan.md`, `phase-3.5-global-identity-forget-governance.md` and `governance-decision-register.md`.

Global Forget remains a separate evidence vector: D fence/barrier, E derived publication/registration, F runtime/index suppression, G Context reconciliation, H target/action-bound ACKs, external recipients, backup/restore and physical erasure. PermissionEpoch proves current authorization only; it cannot prove Forget completion. Unsupported, offline, Unknown or missing target evidence blocks completion unless a narrow exception is approved under I36-GOV-08.

## 11. Closure status

- Trust-chain semantics: **specified as CANDIDATE**.
- Issuer trust and ActorRef/Producer binding: **CANDIDATE; joint H/B alignment and governance approval open**.
- Scope authorization: **CANDIDATE; cross-scope and cross-environment grants GOVERNANCE-BLOCKED**.
- PermissionEpoch: **CANDIDATE; authority/lease policy GOVERNANCE-BLOCKED**.
- Revocation race rules: **CANDIDATE; owner implementation and deterministic tests NOT RUN**.
- Global Forget exception policy: **GOVERNANCE-BLOCKED**.
- Security conformance: **test plan specified; execution NOT RUN**.
- Phase 3.6 cross-module artifact freshness: **PARTIAL / BLOCKED** because separate B/H/C Phase 3.6 owner artifacts were not present in inspected branch trees.
- Contract Freeze / implementation certification: **NOT AUTHORIZED by this I document**.

No unapproved policy in this document is effective. No implementation behavior, test pass, global Forget completion or physical erasure is claimed.
