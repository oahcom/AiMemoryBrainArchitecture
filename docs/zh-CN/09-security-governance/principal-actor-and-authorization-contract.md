---
document_metadata:
  domain: security-governance
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Canonical source blob 03765efac4bb1153f303ce0030f9e277d602e81d on session-i-security-governance-2026-11-16"
        - "AID-2026-109 bilingual source mirror; translation parity not implied"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "English body is preserved; Chinese mirror has a translated summary and retained source text. Full semantic translation parity is NOT_VERIFIED."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "security-governance/principal-actor-authorization bilingual mirror"
    canonical_scope_id: "security-governance/principal-actor-authorization"
    canonical_scope_keywords:
      - security-governance
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/principal-actor-and-authorization-contract.md"
---
# Principal、ActorRef 与授权契约

## 中文镜像状态

本文件描述主体与执行者身份、issuer、授权决策及 PermissionEpoch。类型语义与 I 的政策/授权职责应分层理解。

**翻译状态：** 本镜像目前提供中文标题与摘要；为防止未经审定的政策译文被误认为权威，下方保留英文 canonical 正文。完整中文逐段译文及语义一致性尚未完成独立审核。本文件为 Informative，不得单独作为中文规范性依据。

---

## 英文源正文（逐字保留）

# Principal, ActorRef and Authorization Contract

- Owner: Session I
- Status: **CANDIDATE semantic contract; joint approval required from B/H and Architecture Governance**
- Related: INT-P0-02, INT-P1-03, INT-P1-04, INT-X-03, INT-X-06.

## 1. Identity model

### 1.1 Principal

A Principal is a stable, opaque security subject established by an authenticated issuer. Candidate principal kinds:

- `human`: user or administrator;
- `agent`: logical Agent identity;
- `agent_instance`: a running or provisioned Agent instance;
- `service`: Brain subsystem or service workload;
- `adapter`: registered Adapter instance;
- `external_recipient`: an explicitly registered downstream processor/copy recipient.

A Principal identifier is namespaced by issuer and tenant/security domain. Display names, email strings, model names, user-supplied IDs and payload claims are descriptive only. Principal IDs are not reused after retirement.

### 1.2 ActorRef

ActorRef identifies the Principal that performed a particular operation and preserves the authority chain. It is a typed domain reference, not a bearer credential.

Logical shape (illustrative, not wire encoding):

```text
ActorRef {
  principal_ref: PrincipalRef
  issuer_ref: IssuerRef
  authentication_context_ref: AuthenticationContextRef
  producer_identity_ref?: ProducerIdentityRef
  delegation_chain_ref?: DelegationChainRef
  acting_for_ref?: PrincipalRef
  authenticated_at: Instant
  authn_strength: AuthenticationStrength
}
```

B owns the cross-domain typed-reference meaning and stable reference rules. I defines the security assertions that a valid ActorRef must represent. H binds the authenticated transport principal to the operation; E/D/F/G must not accept a caller-constructed ActorRef as proof of authentication.

### 1.3 ProducerIdentity

ProducerIdentity binds a source producer to:
- authenticated Principal and issuer;
- registered producer/application identity;
- instance or workload identity where applicable;
- credential/key identifier and validity;
- declared source kind and permitted event families;
- tenant/security domain;
- revocation status and credential epoch.

C's telemetry `producer_id` is a payload-level reference that must match or resolve to the authenticated ProducerIdentity. A mismatch is rejected and security-audited without trusting the payload's claimed identity. H owns transport extraction/binding mechanics; I owns policy and trust registry semantics.

### 1.4 Issuer and trust

An Issuer is accepted only if its trust configuration is active for the relevant tenant, audience, credential type and time. Issuer trust is not transitive by default. Key rotation supports overlap windows, explicit key IDs, revocation and audit. Unknown issuer, unknown key, invalid signature, wrong audience, expired/not-yet-valid credential or revoked credential fails closed.

## 2. Scope binding

A request carries a resolved scope tuple, not an arbitrary list of strings:

`ScopeBinding = (tenant, user, project, agent, agent_instance, task, session, environment)`

Not every operation requires every dimension. Each action/resource class declares required dimensions. Missing required dimension is DENY/INDETERMINATE, never a wildcard.

| Dimension | Meaning | Binding source |
|---|---|---|
| tenant | security and administrative boundary | authenticated tenant membership |
| user | data subject / user-owned partition | authenticated subject or explicit grant |
| project | project namespace | registered project membership |
| agent | logical Agent namespace | registered Agent Principal |
| agent_instance | concrete Agent runtime identity | authenticated workload/instance credential |
| task | task isolation | Brain-issued or authenticated Agent task binding |
| session | session isolation | authenticated session binding, expiring |
| environment | world/save/simulation/tenant environment | authoritative Environment registry / authenticated environment adapter |

The tuple is a set of typed bindings with provenance and validity, not a positional wire schema. Environment must be bound whenever a Memory, Event, action or query is environment-dependent. An environment label supplied only in free text is insufficient.

### 2.1 Ownership Scope and applicability Scope

- **Ownership Scope** identifies the security/domain namespace that owns the object and controls administrative custody.
- **Applicability Scope** describes contexts in which an object may be relevant or valid (for example, a project or environment).
- Neither grants access.
- Sharing is a separately authorized grant; it does not rewrite ownership or union scopes.
- A child scope is not automatically visible to a parent, sibling or descendant. Inheritance requires an explicit policy rule and a tested direction.
- Applicability does not imply the object can be dereferenced by a Principal in that scope.

This preserves B's `ScopeRef` domain semantics and the governance invariant that Scope and Permission are distinct.

## 3. Delegation

A DelegationGrant is a signed, auditable, bounded grant from a grantor Principal to a delegate Principal. It includes:
- grant ID and issuer;
- grantor and delegate PrincipalRefs;
- allowed actions and resource classes;
- exact ownership Scope and permitted applicability scopes;
- audience/recipient;
- purpose constraints;
- not-before, expiry and maximum lifetime;
- parent delegation reference (if chained);
- grant version/epoch and revocation handle;
- obligations and approval evidence.

Rules:

1. Delegation is deny-by-default and explicitly opt-in.
2. A delegate may not exceed the intersection of grantor authority, delegated actions, scopes, audience, purpose and time.
3. Delegation depth is bounded; cycles are rejected.
4. A delegate cannot further delegate unless `delegate` is explicitly granted.
5. Revoking a grantor's underlying authority invalidates dependent delegations.
6. Expiry or uncertainty about chain validity blocks the operation.
7. Delegation never transfers ownership or data subject rights.
8. Human/admin break-glass is a separate, short-lived, reasoned and audited path; it is not implicit superuser access.

## 4. Authorization decision contract

A decision request contains:

```text
AuthorizationRequest {
  authenticated_principal_ref
  actor_ref
  producer_identity_ref?
  action
  resource_ref / resource_class
  ownership_scope_ref
  applicability_scope_refs[]
  requested_purpose
  audience
  environment_scope_ref?
  delegation_chain_ref?
  expected_permission_epoch?
  forget_fence_ref?
  request_id / correlation_id
}
```

The response is:

```text
PolicyDecision {
  decision_id
  effect: ALLOW | DENY | INDETERMINATE
  policy_version
  permission_epoch
  subject_ref
  actor_ref
  action
  resource_ref
  scope_binding_fingerprint
  audience
  obligations[]
  issued_at
  expires_at
  reason_code
}
```

The response is bound to the exact action, resource, scope tuple, audience and epoch. It is not transferable to another resource, purpose, scope or recipient. Decision cache entries must use all bound dimensions and expire no later than the decision, credential, delegation or policy validity.

### 4.1 Decision evaluation order

1. Verify transport/session authentication and issuer trust.
2. Resolve authenticated Principal and registered ProducerIdentity.
3. Compare payload actor/producer claims to authenticated binding.
4. Resolve ownership and applicability ScopeRefs from authoritative registries.
5. Validate required tenant/user/project/Agent/task/session/environment dimensions.
6. Validate delegation chain, purpose, audience, time and revocation.
7. Check resource lifecycle, retention, legal hold and Forget fence.
8. Evaluate action/resource policy and obligations.
9. Return ALLOW only when all mandatory facts are established.
10. Recheck epoch/fence at the operation's commit or disclosure linearization point.

### 4.2 Fail-closed rules

- Missing or conflicting identity, unknown issuer, revoked/expired credential: deny.
- Policy service unavailable or response indeterminate: deny protected read/write/export/delivery.
- Permission epoch cannot be checked or is stale: do not use cached ALLOW; refresh or deny.
- Scope dimension required but absent/ambiguous: deny.
- Delegation chain unavailable, expired, revoked or over-depth: deny.
- Resource's owner or current lifecycle cannot be established: deny or return disclosure-safe unavailable.
- Evidence/Provenance target authorization cannot be independently established: do not dereference.
- A previous ALLOW is not a perpetual capability; leases must be short and revocable.
- Non-sensitive public metadata may use a separately declared availability policy; this does not weaken protected content checks.

## 5. Permission epochs and linearization

PermissionEpoch is a monotonic generation scoped to a policy domain (at minimum tenant + subject/grant domain; exact partitioning is an implementation decision). A decision records the epoch it evaluated. On grant/revoke/policy change, the authority advances the affected epoch and publishes an invalidation event.

Every consumer maintains a high-water mark. A request may proceed only if its decision epoch is current under the declared consistency profile. A delayed invalidation, missing sequence, partition gap or disconnected subscriber means the consumer cannot prove currency: it must synchronously revalidate or fail closed.

For sensitive disclosure and irreversible mutation, reauthorization must occur at the final linearization point, not only at request admission. In-flight operations carry a cancellation/revocation token and must be checked immediately before commit or disclosure. If an operation has already crossed the defined disclosure/commit point, the system cannot retroactively undo the disclosed bytes; it must stop subsequent work and record the race.

## 6. Ingress, Accepted and idempotency

E's Accepted receipt means durable custody, not authorization forever or permission to compile later. At ingress E validates current `event.ingest`, producer binding, source Scope, payload classification and retention obligation before durable acceptance. Each retry/replay revalidates current authorization and Forget fence.

The idempotency identity is scoped by authenticated producer + tenant/security domain + operation family + caller idempotency key. Same key/same canonical payload digest returns the original receipt; same key/different digest returns conflict. Do not expose a receipt across principals or scopes. Retention of idempotency metadata must be long enough for the declared retry/replay horizon, but its content is minimized and subject to Forget policy.

## 7. Error and observability contract

Suggested logical errors: `UNAUTHENTICATED`, `IDENTITY_MISMATCH`, `ISSUER_UNTRUSTED`, `DELEGATION_INVALID`, `SCOPE_REQUIRED`, `SCOPE_MISMATCH`, `PERMISSION_DENIED`, `POLICY_UNAVAILABLE`, `PERMISSION_EPOCH_STALE`, `FORGET_FENCE_ACTIVE`, `RETENTION_BLOCKED`, `AUDIENCE_MISMATCH`, `AUTHORIZATION_INDETERMINATE`.

Audit the decision ID, policy version, epoch, actor/issuer references, action/resource class, scope fingerprint, result and reason code. Never log credentials, bearer tokens, raw sensitive payloads or hidden prompts. H owns wire error encoding.

## 8. Open decisions / dependencies

- **OPEN INT-P0-02:** B/I/H must jointly approve typed ScopeRef and authenticated principal binding; B owns domain reference semantics, I policy, H transport binding.
- **OPEN INT-P1-03:** C's producer/event identity and environment semantics require H/I binding and E ingestion conformance.
- **OPEN INT-P1-04:** E/H/I/storage must finalize durable Accepted receipt and retention horizon.
- **OPEN:** exact issuer federation, credential format, key management, epoch partitioning and consistency SLA require security engineering and deployment threat assessment.
- **OPEN:** B's typed ActorRef/ScopeRef details are candidate and must be reconciled before public schema freeze.

---

## Phase 3 targeted remediation — authenticated identity and permission binding

**Status: CANDIDATE security semantics; INT-P0-02 remains OPEN pending B typed-reference and H transport alignment.**

### 9. Cross-module identity binding

The authorization subject is resolved from a trusted authentication context, never from a payload field. The trust chain is:

`Issuer → authenticated credential/session → Principal → ActorRef → (optional) Delegation chain → ProducerIdentity / AdapterIdentity → action + resource + ScopeRef → PolicyDecision`.

- **Principal:** stable security subject, namespaced by trusted Issuer and tenant/security domain. Retired IDs are never reassigned.
- **Issuer:** trusted credential/delegation authority with active audience, key, tenant and validity configuration. Trust is explicit, non-transitive by default.
- **ActorRef:** B-owned typed domain reference identifying the actor for one operation. I requires it to resolve to the authenticated Principal and preserve issuer/authentication provenance. It is not a credential or bearer token.
- **ProducerIdentity:** registered producer/application/workload instance bound to authenticated Principal, issuer, credential, allowed event families, scope and revocation state.
- **AdapterIdentity:** registered Adapter Principal plus stable instance identity, issuer, capability registration/version and managed-region/scope coverage. A payload Adapter ID is only a claim to compare.
- **ScopeRef:** B-owned typed domain reference. I defines its security use: ownership scope and applicability scope are independent of permission and neither grants access by itself.
- **Delegation:** signed, bounded grant chain from grantor to delegate. Every link is checked for signature/trust, audience, action/resource, scope, purpose, time, depth, parent authority and revocation. Effective authority is the intersection of all links and the grantor's current authority.
- **PermissionEpoch:** I-owned monotonic authorization generation scoped to a declared policy domain (at minimum the affected tenant + subject/grant domain; finer partitioning is allowed only if the authority publishes an unambiguous mapping). It invalidates decisions, leases and caches. It is not a Forget fence.
- **RevocationState:** authoritative active/revoked/expired/unknown state for credentials, delegations, principals, producers, adapters and grants. Unknown is not active.

### 10. Payload claims versus authentication

Payload `ActorRef`, `producer_id`, `adapter_id`, tenant, project, environment or issuer strings are untrusted claims. The receiving boundary MUST compare each claim with the authenticated transport/session/workload identity and authoritative registries. A match does not replace signature/session verification. A mismatch is rejected and security-audited. Caller-constructed ActorRef is never accepted as proof of identity.

### 11. Delegation and revocation

Delegation validation is online or backed by a verifiably current revocation snapshot. If any parent grantor loses the underlying authority, all dependent grants become invalid. Cycles, excessive depth, missing parent, unknown issuer, invalid signature, audience mismatch, expired/not-yet-valid grant or unresolved revocation state fail closed.

Revocation is a PermissionEpoch-changing policy event. Consumers track the highest contiguous epoch in their declared policy domain. On a gap, offline state or uncertain ordering they stop protected operations, synchronously revalidate, invalidate decisions/caches/leases and resume only after authoritative reconciliation. An old cached ALLOW is never valid merely because its TTL has not elapsed.

### 12. Epoch separation and final authorization

`PermissionEpoch`, `ForgetFenceGeneration`, D producer-registration barrier, I ProducerDomainInventoryEpoch, F IndexWatermark, G ContextVersion and H capability epoch are separate typed namespaces with separate owners and ordering semantics. They MUST NOT be combined into a scalar, numerically compared, or used as substitutes.

PermissionEpoch advances for authorization-policy changes. ForgetFenceGeneration advances under D's canonical Forget authority for suppression. A Forget request must be separately authorized under the current PermissionEpoch; revocation can deny the actor's ability to initiate or continue administrative work, but it does not erase the already committed suppression obligation. A valid service/continuity principal may continue cleanup only under explicitly delegated, auditable authority.

Every protected boundary reauthorizes: ingress, compile and every source dereference, derivative publication, canonical commit, retrieval candidate and finalization, cache/Working Set read/write, evidence/provenance dereference, Context mutation/reconciliation, delivery, Adapter apply/reconnect, final inference submission, export, backup and restore. Sensitive disclosure and irreversible mutation recheck at their final linearization point. Unknown identity, untrusted issuer, expired credential/delegation, stale PermissionEpoch, unresolved revocation, missing ScopeRef or unavailable policy service fails closed.

### 13. B compatibility guard

I does not define or freeze ActorRef/ScopeRef wire or domain types. B owns their stable typed-reference semantics. The logical fields above are semantic assertions only. The Fact/Claim ADR remains **ADR-BLOCKED**; this remediation does not approve Fact, Claim, ClaimRevision, ConflictSet or any canonical schema. H owns transport/wire binding and must consume B/I decisions without treating payload claims as credentials.



## Phase 3.5 explicit boundary requirements

The Principal/Permission Mapping and Producer/Recipient inventory reconciliation are expanded in `phase-3.5-global-identity-forget-governance.md` §§2–3.

Normative clarification: each protected operation is independently authorized at its own boundary using the current I policy decision and current PermissionEpoch. A previously authenticated Context, old cached ALLOW, queued-work admission decision, lease, session or accepted receipt is not a reusable grant. Revalidate before protected dereference, sensitive stage commit, dependency registration where protected, canonical commit, final publication, retrieval finalization, Context delivery, Adapter apply/reconnect, final inference submission, export, backup and restore. If current policy/epoch/revocation cannot be established, stop the protected action. B remains the authority for ActorRef/ScopeRef type semantics; H remains the transport binding authority.


## Phase 3.6 trust-chain and revocation closure addendum

The end-to-end trust-chain sequence, Issuer Trust Registry requirements, Producer/Agent/Adapter/Runtime Session binding rules, complete authorization tuple, PermissionEpoch contract, revocation race matrix, Governance Decision Register and I36-T01..T20 test specifications are maintained in `phase-3.6-principal-trust-chain-authorization-revocation.md`.

This addendum does not redefine B's ActorRef/ScopeRef types or H's transport/wire schema. It consumes the currently available B/C/D/E/H branch artifacts as provisional evidence. A's Phase 3.5 closure review still records INT-P0-02 OPEN and no formal cross-owner approval. Separate Phase 3.6 B/H/C owner artifacts were not present in the inspected branch trees; therefore the Phase 3.6 mapping remains **CANDIDATE / GOVERNANCE-BLOCKED**, and no Contract Freeze or implementation conformance is claimed.
