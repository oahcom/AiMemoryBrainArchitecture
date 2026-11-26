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
        - "Canonical source blob 71df6aaf21bb1767cd9fe5c947581b871325e023 on session-i-security-governance-2026-11-16"
        - "AID-2026-109 bilingual source mirror; translation parity not implied"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "English mirror body is copied from the canonical source; semantic translation is not applicable to this English counterpart."
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
    canonical_scope: "security-governance/scope-revocation bilingual mirror"
    canonical_scope_id: "security-governance/scope-revocation"
    canonical_scope_keywords:
      - security-governance
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/scope-and-revocation-policy.md"
---
# Scope and Revocation Policy

- Owner: Session I
- Status: **CANDIDATE policy; end-to-end enforcement proof OPEN**
- Related: INT-P0-02, INT-P1-03, INT-X-03, INT-X-04.

## 1. Scope is a domain boundary, not a grant

B defines ScopeRef as a typed domain reference. I defines how Scope participates in authorization. Four independent dimensions must be evaluated:

1. authenticated Principal / ActorRef;
2. resource ownership Scope;
3. resource applicability Scope;
4. action-specific Permission and obligations.

A match in any one dimension does not substitute for the others. No broadening by display name, Agent family, project label, environment name or inferred parent-child relationship is permitted.

## 2. Scope resolution

A ScopeRef resolves to an authoritative, versioned registry entry with:
- opaque scope ID and registered kind;
- owner/tenant boundary;
- optional parent reference and explicit relationship type;
- status (active, suspended, retired);
- issuer/source of binding;
- effective interval and registry version;
- classification and applicable policy profile.

The security binding tuple is tenant/user/project/Agent/Agent-instance/task/session/environment. Each operation class declares its required subset. The tuple is carried as authenticated, resolved context, not trusted from request text.

### 2.1 Ownership and applicability

Ownership Scope is singular for ordinary protected assets unless B explicitly defines a composite owner. Applicability Scope may be zero or more typed contexts. Applicability narrows semantic use; it does not make content readable. A share grant can authorize a recipient to access a resource without changing its owner.

Cross-scope relation traversal requires independent authorization of:
- the edge/relation;
- each endpoint object;
- every expanded evidence/provenance reference;
- any derived aggregate or summary returned.

A caller cannot infer an inaccessible endpoint from a graph count, ranking effect, error detail or timing side channel. F must filter before candidate emission; post-filtering is insufficient.

## 3. Reauthorization matrix

| Stage | Reauthorization required | Revocation effect |
|---|---|---|
| Ingress | Producer, `event.ingest`, source scope, retention class | Reject new ingress; queued work rechecked |
| Compile start / each dereference | Actor, source/content, purpose, current scope | Cancel or quarantine work; no new derivation |
| Derivative creation/publication | Current permission + Forget fence at commit/publication | Reject stale job output; register dependencies before visibility |
| Canonical commit / lifecycle | Actor, action, owner scope, expected version, current epoch/fence | Commit rejected if stale at linearization point |
| Retrieval candidate generation | Scope + action before candidate/count/fusion | Candidate never emitted to caller |
| Retrieval finalization | Recheck every candidate and evidence reference | Drop or fail-closed if revocation raced |
| Cache read/write | Principal, scopes, environment, permission epoch, Forget epoch and version | Cache invalidated/bypassed; no stale protected hit |
| Evidence/Provenance dereference | Independent resource-level authorization | Deny even if parent Memory is visible |
| Context plan/edit/reconcile | Entry's exact MemoryVersion, scope, permission, lifecycle, Forget | Tombstone/block invalid entries |
| Context snapshot/delta delivery | Recipient, session/environment, target version, current epochs | Cancel/quarantine pending delivery |
| Adapter apply / reconnect | Fresh policy/fence, capability epoch and snapshot version | Must clear/quarantine stale managed region before use |
| Final inference request | Reauthorize exact managed region immediately before submission | Block request or omit/quarantine Memory region; never silently submit stale content |
| Export / backup / restore | Destination and retention/Forget policy | Deny copy or restore under suppression fence |

## 4. Revocation semantics

Revocation is an authoritative policy event with a monotonically increasing PermissionEpoch. It can revoke:
- Principal credentials and ProducerIdentity;
- delegation grants and descendants;
- resource/action grants;
- external recipient permissions;
- Adapter capability registration;
- session/task/environment bindings.

Revocation has two effects:

- **Admission stop:** new operations under the revoked authority are denied.
- **In-flight invalidation:** work not yet past its defined commit/disclosure linearization point must revalidate and abort if the new epoch denies it.

No system can retract bytes already disclosed to a recipient. For already-disclosed copies, I starts the applicable external recipient/Forget workflow and records what can and cannot be confirmed.

### 4.1 Epoch propagation

Each policy domain publishes an ordered epoch/invalidation stream. Consumers store the highest contiguous applied epoch. A gap, missing event, unknown epoch, offline state or failed subscriber is not equivalent to current state. The consumer must:
1. stop protected reads/writes/delivery;
2. synchronously obtain authoritative current policy/epoch and affected fence state;
3. invalidate local decision/cache/lease state;
4. resume only after successful reconciliation.

A stale cache entry cannot be used just because its TTL has not expired. TTL is a maximum lifetime, not revocation proof.

### 4.2 Leases

A decision lease is bound to principal, actor, action, resource class/ID, ownership/applicability scopes, audience, purpose, policy version, PermissionEpoch and expiry. Leases are short-lived and non-transferable. High-risk operations require online check at commit/disclosure. Offline mode may serve only explicitly classified non-sensitive data under an approved bounded-staleness policy; it cannot claim current authorization for protected Memory or confirm Forget completion.

## 5. Boundary-specific rules

### E — Ingress and compile
Payload `producer_id`, `actor_ref`, tenant, project and environment fields are claims only. E compares them with authenticated transport context. Source dereference, extraction, entity matching, consolidation, replay, DLQ and retry all reauthorize. A durable Accepted receipt is not a standing permission.

### D — Canonical store and lifecycle
D checks the current policy decision and Forget fence in the transaction's final commit path. A check performed before a long-running validation phase is insufficient. If policy or fence advances between check and commit, the commit aborts or restarts against current state.

### F — Retrieval and caches
F must scope-filter before lexical, ANN, structured, temporal, graph, evidence or provenance candidates can influence output. Canonical status and Forget fences override stale projections. Cache namespaces include principal, scope, environment, permission epoch, canonical version/watermark and Forget fence. Query-result counts and ranking features are also disclosure.

### G/H/C — Context, delivery and inference
G reauthorizes at Context mutation and reconciliation; H revalidates before Adapter application; C defines the protected final-request boundary. A stale/offline Adapter remains Pending/Unknown and must not reapply an old snapshot. Full Applied is not asserted unless H can observe the exact final request and current epochs. Applied does not prove model attention or behavioral compliance.

## 6. Failure and degraded mode

Fail closed for:
- identity/issuer/credential ambiguity;
- missing required Scope binding;
- policy service unavailable for protected access;
- unknown/stale PermissionEpoch or unresolved stream gap;
- missing or stale ForgetFence;
- unverified delegation or external recipient;
- Evidence/Provenance target not independently authorized;
- Adapter offline when protected Memory would be applied;
- backup restore unable to consult Forget ledger.

A degraded mode must name the data class, permitted action, maximum staleness, expiry, owner and approval. “Best effort” is not a policy.

## 7. Adversarial cases

- Forged tenant/user/Agent/environment field in payload.
- Principal A reuses Principal B's idempotency key or cached response.
- Revocation races with commit, evidence dereference, cache hit or final inference submission.
- Parent Memory readable but attached Evidence restricted.
- Graph edge visible but endpoint outside caller's Scope.
- Stale adapter reconnects with older ContextVersion and permission epoch.
- ANN global top-k leaks cross-scope candidate counts before filtering.
- Permission event stream has a missing epoch or consumer is partitioned.

## 8. Open dependencies

- B must approve typed ScopeRef/ActorRef and explicit scope hierarchy semantics.
- H must bind authenticated transport principal, audience, producer and capability epoch; no I wire fields are prescribed here.
- C must expose the final inference boundary and distinguish managed-region inclusion from model behavior.
- D/E/F/G must map local reauthorization to their transaction, worker, query, cache and delivery linearization points.
- A must register common typed epochs/cursors without conflating PermissionEpoch, ForgetFence, canonical commit sequence, index watermark, ContextVersion or Adapter capability epoch.

---

## Phase 3 targeted remediation — permission epoch, revocation and boundary obligations

**Status: CANDIDATE policy semantics; implementation conformance OPEN.**

### 7. PermissionEpoch contract

PermissionEpoch is an opaque typed generation issued by I's policy authority for a named policy domain. Its domain identifier, issuer, generation, policy version, effective time and revocation-stream position are part of its verification context. The generation is monotonic only within that exact domain and issuer. No cross-domain arithmetic or ordering is valid.

A policy-domain change affecting a Principal, delegation, grant, ProducerIdentity, AdapterIdentity, scope membership or protected resource increments the affected epoch(s) according to the authority's published fan-out map. A consumer may rely on an epoch only when it has a contiguous, authenticated view through the required point or has synchronously revalidated with the authority. Unknown partition mapping, gap, issuer mismatch, stale cache or offline revocation state fails closed.

PermissionEpoch expiry is not a permission grant. A decision expires at the earliest of decision expiry, credential expiry, delegation expiry, session expiry, policy validity end or resource/Scope binding expiry. At expiry the consumer must reauthorize; it cannot extend the prior ALLOW locally.

### 8. Forget concurrency

Permission revocation and Forget are distinct concurrent workflows:
- revocation denies future actions under the revoked authority and invalidates in-flight operations not past their declared commit/disclosure point;
- Forget suppression remains governed by D's ForgetFence and I's global completion policy;
- revoking the requester does not roll back a committed fence or convert pending targets to complete;
- if the requester loses authority before the Forget authorization/fence commit, the operation must stop or be reauthorized by a currently authorized Principal;
- cleanup after requester revocation may continue only under a registered service Principal with a scoped, auditable delegation/policy grant;
- evidence binds both the applicable PermissionEpoch and D ForgetFence reference separately.

### 9. Boundary reauthorization requirements

| Boundary | Required identity/policy evidence | Fail-closed behavior |
|---|---|---|
| Ingress / producer registration | authenticated Principal, Issuer, ProducerIdentity, ActorRef claim match, ScopeRef and current PermissionEpoch | reject acceptance/registration |
| Compiler execution / replay | producer + actor binding, source ScopeRef, purpose, delegation, current PermissionEpoch and D fence | cancel/quarantine work; no dereference/publication |
| Canonical commit | actor/principal, action/resource, ownership ScopeRef, current permission decision and D fence at commit | abort/retry against current policy |
| Runtime candidate/finalization | caller identity, requested ScopeRef, current epoch and target authorization | filter before emission; fail closed if final recheck unavailable |
| Cache / Working Set | principal, scope, environment, PermissionEpoch, ForgetFence and version namespace | bypass/invalidate; never serve stale protected hit |
| Context reconciliation/delivery | recipient Principal/AdapterIdentity, Context target, ScopeRef, PermissionEpoch and D fence | pending/unknown; no stale apply |
| Adapter reconnect/final inference | authenticated AdapterIdentity, capability epoch, current PermissionEpoch, D fence and G target | quarantine managed region until reconciled |
| External recipient/export | authenticated recipient identity, audience, purpose, ScopeRef, current epoch and retention policy | stop new export; revoke credentials and issue withdrawal |
| Backup/restore | storage workload Principal, restore target scope, current permission and persistent Forget ledger | restore to quarantine; no serving before reconciliation |

### 10. Revocation state and recovery

Revocation states are `Active | RevocationPending | Revoked | Expired | Unknown`. Only Active with a current, verified epoch may authorize. RevocationPending/Unknown blocks protected actions. Recovery requires authenticated resynchronization, current policy decision, invalidation of old decision/cache/lease state and audit record. A late invalidation cannot be ignored because a local cache is still within TTL.


