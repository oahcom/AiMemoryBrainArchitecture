# Session I — Phase 3.5 Global Identity, Target and Forget Governance Addendum

- Owner: Session I — Security, Identity & Governance Principal Architect
- Status: **CANDIDATE governance addendum; cross-owner approval and implementation evidence OPEN**
- Policy version: `I-GOV-3.5-candidate.1`
- Baseline reviewed: D/E/H/I Phase 3 cross-module review dated 2026-11-16; B typed-reference baseline and C Agent telemetry/attestation semantics are consumed without redefining their ownership.
- Related: CR-P0-02, CR-P1-05, INT-P0-02, INT-P0-03, INT-X-02, INT-X-03, INT-X-04, INT-X-06.

## 1. Authority and non-goals

I owns global identity trust and authorization policy, delegation/revocation, Producer/Recipient Domain Inventory, PermissionEpoch, target evidence policy, Global Forget Completion, retention, external-copy/backup policy, audit and physical-erasure requirements.

I does not define B's ActorRef/ScopeRef domain types, C's telemetry event schema or inference semantics, D's ForgetOperation/Fence/WorkItem Barrier, E's compiler work lifecycle, H's BMCP wire schema or Adapter implementation, nor F/G local execution semantics. The logical mappings below are I policy requirements, not wire/API schemas.

The following are distinct and non-interchangeable:
- I `ProducerDomainInventoryEpoch`: global closed-world catalogue generation for Producer/Recipient Domain classes and instances.
- D `ProducerRegistrationHighWater` / per-Forget `WorkItemBarrier`: concrete work admitted for one Forget operation.
- I `PermissionEpoch`: authorization-policy generation in a declared policy domain.
- D `ForgetFenceGeneration`: canonical suppression generation.
- F `IndexWatermark`, G `ContextVersion`, H `AdapterCapabilityEpoch`: module-owned typed positions/epochs.

No numeric comparison, coercion, shared counter, cursor substitution or inferred equality is allowed across these namespaces.

## 2. Principal / Permission Mapping

### 2.1 Principal and Issuer

A Principal is an opaque security subject established by a trusted authentication mechanism and namespaced by Issuer plus tenant/security domain. Principal classes include human, logical Agent, Agent instance/workload, service, Adapter instance and external recipient. Principal identifiers are stable and never recycled.

An Issuer is a trust authority that vouches for credentials or attestations. I's trust registry binds issuer, key ID, credential type, audience, tenant/security domain, validity interval, rotation and revocation status. Unknown issuer/key, invalid signature, wrong audience, expired/not-yet-valid credential, revoked key or unresolved trust state is DENY/INDETERMINATE.

### 2.2 ActorRef and ScopeRef

- `ActorRef` identifies the actor and authority/delegation chain for an operation. It is a B-owned typed domain reference and is never a credential or bearer capability.
- `ScopeRef` is a B-owned typed domain reference. I resolves and authorizes its ownership/applicability semantics; scope match is not permission.
- Payload ActorRef, ScopeRef, producer_id, agent_id, adapter_id or recipient_id is a claim/selector only. H must bind the authenticated transport identity; I validates the policy binding. A mismatch is rejected or quarantined and audited.
- No display name, label, Agent family, parent-child inference, free-text environment or payload-supplied tenant can widen identity or scope.

### 2.3 Producer / Agent / Adapter identity mapping

| Identity | Authenticated binding required | I policy responsibility | Not sufficient |
|---|---|---|---|
| Agent Principal | Issuer + credential/workload identity + tenant/security domain | Register Agent class, permitted actions/scopes, status and revocation | Model name, Agent label, telemetry producer_id |
| Agent instance | Agent Principal + unique instance/workload credential + lifecycle | Bind instance to Agent, environment/session/task scope and validity | Caller-supplied instance ID |
| ProducerIdentity | Principal + issuer + producer/application registration + instance + credential epoch + source/event families + Scope coverage | Admit producer class/instance and revoke/limit source authority | Queue name, Event source_id, payload producer_id |
| AdapterIdentity | Adapter Principal + authenticated instance/transport identity + registered capability profile | Bind instance to target managed regions, scopes, recipient and capability obligations | Adapter display name, session ID alone |
| ExternalRecipientIdentity | Issuer-authenticated recipient/service identity + audience + contract/endpoint identity + onward-recipient declaration | Register copy domain, scope, purpose, retention, deletion and evidence obligations | Webhook URL or export destination string |
| Service Principal | Workload identity + issuer + deployment/environment binding | Least-privilege service policy and epoch/revocation | Static service label |

C telemetry fields remain telemetry claims and are correlated to authenticated ProducerIdentity; they do not create or authenticate a Principal. H owns transport extraction and authenticated Adapter binding; I owns trust registration and authorization policy.

### 2.4 Permission decision and reauthorization

A usable decision is bound to subject/ActorRef, action, resource class and identity, ownership ScopeRef, applicability ScopeRefs, purpose, audience, delegation chain, policy version, PermissionEpoch, obligations, decision time and expiry. Only ALLOW is usable. DENY and INDETERMINATE both stop protected work.

Every protected operation MUST obtain or validate a current decision at its own trust boundary. This applies to ingress/registration, queue dispatch and lease acquisition, each protected source/evidence dereference, each sensitive stage commit, dependency registration where protected, canonical write, final derivative publication, retrieval candidate generation and finalization, cache/Working Set access, Context mutation/reconciliation, delivery, Adapter apply/reconnect, final inference submission, export, backup and restore.

A prior Context, signed decision, lease, accepted receipt, cached ALLOW or previously authenticated session is not perpetual authorization. At each boundary:
1. authenticate or validate the still-live authenticated binding;
2. resolve current Principal, ProducerIdentity, ActorRef and ScopeRef bindings;
3. obtain the authoritative current PermissionEpoch for the relevant policy domain;
4. evaluate current grant, delegation, revocation, purpose, retention and obligations;
5. compare the decision's typed policy epoch using I's policy-domain rules;
6. re-evaluate immediately at the irreversible commit/disclosure boundary.

If the policy service is unavailable, epoch continuity has a gap, revocation state is uncertain, the decision is expired, or a required binding is missing, fail closed for protected data. TTL is an upper bound, never proof that a cached decision remains current.

### 2.5 Delegation and revocation

Delegation is signed, audience/purpose/action/resource/Scope/time bounded and non-amplifying. Effective authority is the intersection of grantor authority, delegate authority, delegated actions, resource class, Scope, audience, purpose and time. Delegation depth is bounded; cycles and implicit sub-delegation are rejected. Revocation/expiry of a grantor or parent invalidates dependent grants.

Revocation is an I policy event that advances the relevant PermissionEpoch. Admission stops immediately once authoritative revocation is visible. In-flight work not yet past its defined commit/disclosure linearization point must reauthorize and abort if no longer allowed. Consumers with a gap/offline/unknown epoch pause protected operations, invalidate old decisions/caches/leases and synchronously reconcile before resuming.

A Forget operation already canonically suppressed remains an obligation if the initiating actor is later revoked. Cleanup may continue only under a separately authenticated and currently authorized service/continuity Principal; stale requester Context is not reused as authority.

## 3. Two-layer Producer / Recipient Inventory

### 3.1 Layer A — Global Producer/Recipient Domain Inventory (I-owned)

This is the closed-world governance catalogue of classes and instances capable of creating, transforming, retaining, serving, applying, copying, restoring, exporting or receiving a target or derivative.

Each entry MUST identify:
- stable non-recycled DomainId/TargetId and domain class;
- producer, consumer, recipient, storage, backup or Adapter role;
- accountable owner Principal/team and trusted Issuer;
- authenticated instance identity or explicitly justified singleton identity;
- exact ScopeRef coverage and binding fingerprint;
- capability set/version/epoch and supported actions;
- lineage/source/recipient relationships and onward-copy obligations;
- online/offline/disabled/revoked/unknown state;
- retention class, jurisdiction, backup/restore relationship;
- evidence profile, acknowledgement requirements, verifier and contract version.

I advances `ProducerDomainInventoryEpoch` whenever membership, class, instance, owner, issuer, scope coverage, capability, recipient, backup/restore route or evidence obligation changes in a way that can affect completeness. For a Forget operation I enumerates the applicable records, records the epoch and canonical inventory digest, identifies unresolved gaps and seals the exact target set. A relevant epoch change or late target discovery invalidates the seal and forces Reopened + re-enumeration + new evidence evaluation.

Minimum classes include D canonical authority/dependency registry; E ingress/compiler/queue/lease/retry/DLQ/replay/staging; F index partitions/caches/Working Sets/rebuilds; G Context/snapshots/deltas/delivery; each H Adapter instance and managed region; external recipients and onward recipients; primary/replica/backup/WAL/archive/DR; human/admin exports; audit/observability/support systems.

### 3.2 Layer B — Per-Work-Item Producer Registration Barrier (D-owned)

For one ForgetOperation, D captures its own registration high-water/barrier over concrete derivative-capable work items durably registered before fence installation. Each pre-fence work item must reach a durable terminal disposition; unresolved leases, retries, DLQ/replay possibility, registration gaps and late derivatives keep the barrier open.

I consumes D's typed barrier proof as one component of global evidence. I does not allocate, advance, reinterpret or replace D's high-water. D's per-operation barrier does not prove that I's global producer/recipient catalogue is complete.

### 3.3 Reconciliation rule

I must establish both:
- global domain completeness at a sealed `ProducerDomainInventoryEpoch`; and
- D's operation-specific work-item barrier closure under the canonical ForgetFence.

The two proofs answer different questions and are jointly required. A new global domain/recipient discovered after sealing invalidates I's seal even if D's old work-item barrier is closed. A D barrier gap remains open even if I's domain catalogue is stable. Neither can compensate for the other.

## 4. ACK-to-Target Matrix (H → I)

An H acknowledgement is evidence for one authenticated Adapter target, managed region and action only. It is not a global verdict and is not automatically evidence of physical erasure.

| H ACK class | I target state | Permitted conclusion | Explicit non-conclusion |
|---|---|---|---|
| `SUPPRESSED` | Confirmed for access-suppression action only | Named managed region is ineligible for future protected inference assembly | No purge, buffer clear, queue cancellation or provider erasure |
| `LOCAL_BUFFER_CLEARED` | Confirmed for named volatile buffer action only | Enumerated local buffer was cleared under declared capability | No persistent cache/media/other region deletion |
| `LOCAL_CACHE_PURGED` | Confirmed for named Adapter-controlled cache action only | Enumerated cache namespace was purged under declared capability | No secure media erasure, hidden provider cache or other target coverage |
| `QUEUED_DELIVERY_CANCELLED` | Confirmed for enumerated delivery IDs only | Named not-yet-submitted delivery intents were cancelled | No recall of already submitted bytes or unrelated queues |
| `FAILED` | Failed | Attempted target action definitively failed | Cannot be rolled up as pending success |
| `UNKNOWN` | Unknown | Outcome/evidence cannot be verified | Never Confirmed by timeout, retry exhaustion or offline status |
| `UNSUPPORTED` | Unknown by default; PolicyException only after independent approval | Capability is absent for the named action | Never a technical success or implicit NotApplicable |

### 4.1 Mandatory ACK evidence binding

Every ACK used by I MUST bind:
- ForgetOperationId and exact target TargetId;
- authenticated AdapterIdentity, Principal, Issuer and instance identity;
- CapabilityEpoch/profile/version and the declared capability for this action;
- authenticated Session identity/reference and session validity at ACK time;
- exact managed-region, buffer/cache/queue identity and ScopeRef coverage;
- D ForgetFence reference (opaque; validate only through D authority);
- PermissionEpoch/policy decision where the action is permission-sensitive;
- G ContextVersion/delivery IDs when clearing or cancelling Context delivery;
- ACK class, action, attempt/operation ID, observed time, evidence-contract version;
- integrity/signature proof, verifier identity, reason/status and audit correlation.

Missing or ambiguous target, identity, scope, capability, session or operation binding yields Unknown/Failed according to evidence integrity; it never yields Confirmed. A stale/revoked capability epoch cannot establish that a newly required action is supported. Session expiry after a validly signed historical ACK does not erase the historical fact, but the ACK cannot authorize a later operation or reconnect. Evidence validity is action-specific and policy-defined; there is no universal TTL. Expired evidence may remain historical audit evidence but cannot satisfy a current completion evaluation unless the policy explicitly defines it as durable proof of that completed action.

## 5. Global Forget Completion Evidence Vector

For a sealed target inventory, I evaluates a typed vector. Every component is evaluated against its mandatory target set; aggregate counts cannot hide missing partitions or recipients.

| Component | Owner/source evidence | Required target closure |
|---|---|---|
| Canonical suppression | D ForgetFence + canonical target status | Fence is durable and every mandatory canonical target is suppressed |
| Producer barrier | D WorkItemBarrier + E/F/G/H producer disposition | All pre-fence work terminal; no unresolved lease, registry gap or late publication |
| Derived artifacts | E lineage/dependency registration + target-specific cleanup evidence | All registered derivatives and transitive descendants handled under policy |
| Runtime/index/cache | F per-index/per-partition watermarks and cache/Working Set evidence | Every mandatory runtime target has crossed the required fence and cannot emit stale candidates |
| Context/delivery | G reconciliation/ContextVersion + delivery cancellation/reconciliation | No stale snapshot/delta/ChangeSet/delivery can apply or reactivate forgotten content |
| Adapter managed regions | H per-Adapter/per-region ACK + capability/session/Scope binding | Every mandatory Adapter target has required action-specific evidence |
| External copies | Recipient request/receipt/withdrawal/deletion attestation + onward-copy evidence | Each mandatory recipient Confirmed or has a valid, narrow PolicyException |
| Backup/restore | Backup catalog, retention/expiry, quarantine, restore ledger replay | All restore paths remain quarantined until current Forget/revocation ledger is applied; required backup retention/expiry action met |
| Physical erasure | Storage/media/key-scope proof and external assurance where applicable | Applicable erasure standard is independently evidenced; logical suppression is not substituted |

Component state is `Pending | Confirmed | Failed | Unknown | PolicyException | NotApplicable`. NotApplicable requires proof from the sealed inventory that no applicable target exists, plus independent reviewer approval. Optional targets are only those explicitly classified optional by an approved policy rule and recorded in the seal; absence of evidence does not make a target optional.

### 5.1 Global result rules

- Unknown, Failed, missing, stale or contradictory evidence on a mandatory target blocks Completed.
- Unsupported maps to Unknown unless an authorized independent approver grants a narrow PolicyException with expiry and compensating controls.
- PolicyException is a disclosed residual risk, never technical success. Expiry/revocation reopens the operation.
- A newly discovered derivative, recipient, backup route, target instance or capability surface reopens inventory and supersedes the prior completion proof.
- Any relevant ProducerDomainInventoryEpoch change invalidates the seal unless an independent reviewer proves the change is non-semantic to membership, scope, capability and evidence coverage.
- Backup restore must apply the current durable Forget/revocation control ledger before any restored object is queryable, indexed, delivered or used for inference. Restored stale state is quarantined; resurrection reopens the operation.
- External recipient receipt proves request delivery only. Deletion/withdrawal evidence must bind recipient, target class, Scope, onward recipients, action, time and assurance. Provider-internal copies beyond verifiable control remain Unknown or a narrow exception.
- Physical erasure is a separate vector component. No tombstone, main-row delete, local cache clear or provider ACK alone proves media erasure.
- Completion is evaluated against a specific inventory seal, D fence/barrier references, policy version and evidence set. It is not a permanent assertion against future target discovery or restore resurrection.

## 6. OPEN Policy Decisions

| ID | Decision required | I owner | Required approver(s) | Evidence needed | Status |
|---|---|---|---|---|---|
| I35-PD-01 | Final typed Principal/Issuer/ProducerIdentity ↔ B ActorRef/ScopeRef mapping | I | B + H + Architecture Governance | B typed-reference approval, H authenticated transport binding, negative identity/scope tests | OPEN |
| I35-PD-02 | PermissionEpoch policy-domain partitioning, monotonicity and freshness/online-check guarantees | I | Security Governance + D/E/F/G/H consumers | policy-domain registry, epoch continuity semantics, stale-cache/revocation race tests | OPEN |
| I35-PD-03 | Agent/Adapter instance enrollment, credential rotation and revocation authority | I | H + C + Identity/Platform Security | issuer trust config, instance attestation, key rotation/revocation test evidence | OPEN |
| I35-PD-04 | Producer/Recipient Domain Inventory required/optional class taxonomy and seal invalidation rules | I | D/E/F/G/H + Storage + Privacy | domain catalogue, owner attestations, inventory diff and late-discovery tests | OPEN |
| I35-PD-05 | H ACK evidence assurance profiles and per-action evidence validity periods | I | H + Security Governance | ACK schema/attestation, capability binding, session/region coverage, replay/expiry tests | OPEN |
| I35-PD-06 | External recipient deletion assurance and onward-recipient obligations | I | Privacy/Legal + Data Owner + Security | contractual terms, API semantics, deletion receipt and recipient audit evidence | OPEN |
| I35-PD-07 | Backup retention, restore quarantine and physical-erasure standards by storage class/jurisdiction | I | Storage + Privacy/Legal + Security | backup catalog, retention schedule, crypto-erasure proof, restore drill | OPEN |
| I35-PD-08 | PolicyException classes, approvers, expiry and user disclosure | I | Privacy/Legal + Security + relevant data/service owner | approval matrix, signed exception record, expiry/reopen tests | OPEN |
| I35-PD-09 | Audit evidence retention schedule and non-reconstructive tombstone limits | I | Privacy/Legal + Audit Owner | data map, jurisdictional basis, minimization and reconstruction tests | OPEN |
| I35-PD-10 | Global Forget completion thresholds and when physical erasure is mandatory vs retention-expiry/exception | I | Privacy/Legal + Security + Storage + Product/Data Owner | policy by data class, retention/hold basis, signed risk decision | OPEN |
| I35-PD-11 | Cross-environment and onward-copy inventory coverage, including provider/model telemetry | I | C + H + Privacy/Legal + external providers | environment/scope inventory, provider capability declarations, external-copy evidence | OPEN |
| I35-PD-12 | Policy decision continuity during I authority outage and approved bounded offline behavior | I | Security Governance + SRE + Privacy | threat analysis, bounded-staleness profile, outage/partition fault tests | OPEN |

No OPEN decision may be treated as approved by the existence of this document. Any approval must be entered in the Governance Decision Register with approver identity, evidence, effective policy version and date.

## 7. Required conformance evidence (NOT RUN)

At minimum, test:
1. payload ActorRef/ProducerIdentity spoofing and issuer/key revocation;
2. ScopeRef mismatch, missing environment and cross-scope lineage;
3. PermissionEpoch advancement between admission, source dereference, commit and publication;
4. old Context/session/lease replay after revocation;
5. ProducerDomainInventoryEpoch change while Forget is in progress;
6. D registration racing D fence installation, with both serialized outcomes;
7. each H ACK class with wrong Adapter, target, capability epoch, session, Scope or managed region;
8. H offline reconnect, stale snapshot and late ACK;
9. Unknown/Unsupported/Failed mandatory targets blocking completion;
10. late derivative/recipient discovery invalidating a seal;
11. backup restore with stale data and current control-ledger replay;
12. external recipient non-response and onward-copy uncertainty;
13. expiry/revocation of PolicyException;
14. physical-erasure proof scope mismatch and audit reconstruction attempt.

A PASS requires fixture, test version/environment, expected and actual result, reproducible artifact, owner sign-off and non-sensitive evidence. No such execution is claimed here.

## 8. Non-claims

This addendum is a candidate governance specification. It does not prove implementation, runtime enforcement, D/E/Storage atomicity, F/G/H conformance, recipient compliance, backup expiry, restore safety, physical erasure or production readiness. B retains typed reference authority; C retains Agent telemetry/inference semantics; H retains wire encoding; D/E/F/G retain local execution mechanisms.
