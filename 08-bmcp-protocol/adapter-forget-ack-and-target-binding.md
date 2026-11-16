# Adapter Forget ACK, Target Identity and Reconnect Contract

- Owner: H; status: CANDIDATE, subject to I/D/G/B approvals
- Remediation: CR-P1-05 / CR-P0-02 (H-owned boundary)
- H baseline: session-h-bmcp-protocol @ fcc5103399b4c322e52d642cae5a2414969399a7
- Inputs: I @ 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb; D @ 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6; G @ 3d2c065be863bc1d349faaeece6f6eaa0047abae; B @ ab19afbf92f67fe0a7679e9aa3a35b015fed89f4.

## 1. Authority and evidence boundary

H owns BMCP wire representation, Adapter execution boundary, local evidence, retries and reconnect gates. I owns target inventory, required actions, Target State, PolicyException authorization and Global Forget Completion. D owns ForgetOperation identity and ForgetFence generation/ordering. G owns Context membership/version, invalidation, delivery intent and Context-side reconciliation. B owns ActorRef/ScopeRef domain semantics and stable reference rules. H references these authorities and does not redefine them.

An ACK is one bounded observation by one authenticated Adapter Instance, for one Agent/runtime session, ScopeRef, Managed Region, ForgetOperation/fence and declared capability set. It says nothing about other Adapter instances, provider logs, external recipients, backups, model internals or global completion.

Evidence stages MUST remain distinct:
1. Command received: authenticated endpoint received a request; transport receipt only.
2. Local action attempted: Adapter began the operation.
3. Local action completed: Adapter observed and persisted the defined postcondition.
4. ACK transmitted/received: evidence transport only; it does not expand evidence scope.

Delivered is not Applied, SUPPRESSED, LOCAL_BUFFER_CLEARED or LOCAL_CACHE_PURGED. A successful HTTP/gRPC response is not a clear ACK unless it contains a valid action-completion attestation.

## 2. ACK vocabulary and I Target State mapping

| ACK | Required Adapter-local postcondition | Candidate I Target State evidence | Retry | Can satisfy I target? |
|---|---|---|---|---|
| SUPPRESSED | Durable local gate prevents target selection/assembly in future inference requests through this Adapter + Managed Region. No byte-removal claim. | Confirmed only for a target whose required action is logical suppression/inaccessibility. | Idempotent query/retry; retain gate until authoritative release. | Yes, suppression target only. |
| LOCAL_BUFFER_CLEARED | All Adapter-controlled volatile buffers in the declared region/session holding affected content cleared or rendered inaccessible; postcondition checked. No claim for undeclared buffers or persistent/provider copies. | Confirmed only for a buffer target if complete buffer inventory is declared and matches I target. | Same operation key; safely re-check. | Conditional, exact buffer scope only. |
| LOCAL_CACHE_PURGED | All matching entries in declared Adapter-controlled cache namespaces/partitions purged; coverage and watermark recorded. | Confirmed only for enumerated complete cache scope with verifiable purge result/watermark. | Safe repeat with same operation identity. | Conditional, declared cache scope only. |
| QUEUED_DELIVERY_CANCELLED | All matching locally queued/retry/persisted Pending deliveries in declared queue namespace cancelled or durably non-replayable; scan/drain watermark recorded. No claim for remote/Brain queues. | Confirmed only for this Adapter queue target with complete queue inventory. | Safe repeat/reconcile. | Conditional, Adapter-local queue only. |
| FAILED | Attempt definitively failed; stage and reason recorded; no postcondition asserted. | Failed or Unknown as I evaluates evidence. | Only transient retry after fresh auth/fence check. | No. |
| UNKNOWN | Outcome cannot be established (offline, crash window, timeout, missing evidence, ambiguous coverage). | Unknown/Pending; unresolved. | Query/reconcile/retry after fresh checks. | No. |
| UNSUPPORTED | Capability absent for requested action or management boundary. | Unknown; I may separately authorize PolicyException. | Not until capability changes; new capability epoch. | No; exception only by I. |

FAILED, UNKNOWN and UNSUPPORTED are distinct. Unknown/offline is never success. H cannot grant a PolicyException. SUPPRESSED proves only future inaccessibility at the stated boundary; it does not prove buffers or caches were purged. LOCAL_BUFFER_CLEARED does not include persistent caches. LOCAL_CACHE_PURGED and QUEUED_DELIVERY_CANCELLED cover only declared Adapter-managed namespaces.

## 3. Required ACK evidence envelope

Every ACK binds:
- ack_id, ack_status, reason_code;
- D-issued ForgetOperation ID and opaque ForgetFence Generation;
- I-issued Permission Epoch used for this action;
- registered Adapter Principal/Instance identity;
- authenticated Agent Principal, Runtime Instance and Session ID;
- Authenticated Principal, Issuer, B-typed ActorRef and transport-authentication context reference;
- B-typed ScopeRef resolved/authorized by I;
- Managed Region ID, region revision and declared coverage inventory version;
- capability set and Capability Epoch;
- G ContextRef and opaque ContextVersion where relevant;
- logical Delivery ID and attempt ID where relevant;
- evidence time, monotonic local sequence/clock domain;
- action-specific postcondition, affected range/count and queue/cache watermark where relevant;
- privacy-safe evidence reference/digest, canonicalization profile and integrity binding;
- correlation and causation IDs.

If a field is inapplicable, use an explicit typed null/reason as schema defines; do not omit identity/generation dimensions. Missing or mismatched Adapter instance, Agent/runtime session, ScopeRef, Managed Region, Capability Epoch, Permission Epoch or ForgetFence makes the ACK untrusted for target satisfaction.

Capability declaration MUST enumerate managed buffer classes, cache namespaces/partitions, pending-delivery stores, session scope and whether completeness is provable. “All local data” is prohibited unless backed by a versioned, enumerated management inventory. Region/capability changes invalidate coverage assumptions for future operations; historical evidence remains historical.

## 4. I target accounting

| H ACK | H can prove | I must independently evaluate |
|---|---|---|
| SUPPRESSED | Durable deny marker, selector/fence, region/session and anti-replay gate | Whether the registered target requires suppression only; not buffer/cache deletion |
| LOCAL_BUFFER_CLEARED | Declared buffer classes, region, post-clear check and time | Whether inventory is complete and matches the target |
| LOCAL_CACHE_PURGED | Cache namespace/partition inventory, purge result and watermark | Whether every required partition is covered; gaps mean Unknown |
| QUEUED_DELIVERY_CANCELLED | Local queue scan, cancelled/non-replayable IDs and watermark | Whether the target is this Adapter queue; G/Brain queues need separate evidence |
| FAILED | Failure stage and reason | Failed or Unknown, never success |
| UNKNOWN | Ambiguity reason and last verified state | Unknown; retry/reconcile |
| UNSUPPORTED | Missing capability and capability epoch | Unknown unless I separately approves a scoped PolicyException |

One ACK can satisfy at most the matching Adapter Instance + Agent/runtime Session + ScopeRef + Managed Region + capability slice. It cannot close the global inventory. I defines target classes, required action, evidence acceptance, aggregation and exceptions.

## 5. Target identity and B/I bindings

Logical target tuple:
AdapterPrincipalRef + AdapterInstanceRef + AgentPrincipalRef + RuntimeInstanceRef + SessionRef + ScopeRef + ManagedRegionRef + CapabilityEpoch.

Resolve it from authenticated transport/session context, I's identity registry and B's typed references. Payload adapter_id, agent_id, runtime_id, actor_ref, producer_id, issuer, session_id and scope_ref are claims only. Compare each to the authenticated/registered binding; mismatch => reject/quarantine and fail closed.

- Adapter Identity: I-registered Adapter Principal and concrete instance/workload identity. Replacement is a new target unless I explicitly maps continuity.
- Agent/Runtime Identity: authenticated Agent Principal plus concrete runtime instance, bound to an expiring session.
- Principal/Issuer: I-approved issuer, audience, credential/key validity and revocation status.
- ActorRef: B typed domain reference; I security assertions; not a bearer credential.
- ScopeRef: B typed domain identity; I resolves and authorizes it; never a grant.
- Managed Region: H/Adapter registered region and revision, disjoint from protected instruction, user, Agent-policy and tool regions.
- Capability Set/Epoch: negotiated features; ACK valid only for the epoch used.
- Transport Authentication Context: authenticated peer, issuer, audience, credential/key ID, session and validity reference; never raw credentials.

H uses B's authoritative ActorRef/ScopeRef types. B owns semantic identity/namespace rules; I owns trust and authorization; H owns only encoding and transport binding.

## 6. Permission Epoch and ForgetFence are different namespaces

PermissionEpoch is issued by I and represents authorization policy state. ForgetFenceGeneration is issued by D and represents a canonical Forget barrier. They have different issuers, type IDs, scopes, ordering rules and consumers. H MUST NOT numerically compare, reuse, convert, increment, order across or copy one token into the other's field. Neither is ContextVersion or CapabilityEpoch. H stores each opaque token and invokes only its owning authority's validation/currentness operation. If either required value is unavailable, stale, untrusted or incomparable, fail closed: hold/suppress managed memory, do not apply Context and report UNKNOWN/FAILED as evidence warrants. A message may be current in one namespace and stale in the other; both checks are mandatory.

## 7. Clear, Apply and reconnect order

### Clear
1. Authenticate transport; resolve Adapter, Agent/runtime, Principal/Issuer, Session and Scope.
2. Validate integrity, protocol/schema, audience, expiry and operation authorization.
3. Fetch/check current I PermissionEpoch and current D ForgetFence.
4. Bind target to G Context/Delivery IDs and exact Managed Region.
5. Persist local suppression gate before asynchronous purge/cancel.
6. Clear declared volatile buffers, purge declared caches and cancel local queued deliveries as separate actions.
7. Verify each postcondition against declared coverage inventory.
8. Persist ACK evidence durably, then transmit. If transmission fails, retry same ACK identity/evidence.

### Delivery Apply gate
Immediately before Context application and again at final inference submission: authenticate current session; verify current I authorization/PermissionEpoch; verify applicable D ForgetFence; verify G ContextVersion, delivery ID, expiry and supersession; verify capability epoch and region; verify no suppression marker blocks included content. Any failed/indeterminate check blocks affected managed memory. Prior ALLOW/ACK is not a perpetual lease.

### Reconnect (normative H sequence)
1. Establish trusted Transport Authentication (issuer, audience, credential/key validity).
2. Authenticate/bind Adapter Instance, Agent/Runtime, Principal/ActorRef, Session and ScopeRef; compare payload claims.
3. Negotiate protocol/schema versions and capability set; establish current CapabilityEpoch.
4. Obtain current I PermissionEpoch and authorization for exact operation.
5. Obtain current D ForgetFence for every relevant target/scope.
6. Clear/suppress stale Managed Regions, buffers, caches and Pending Deliveries invalidated by permission/fence; persist suppression first.
7. Submit local action evidence/ACKs; preserve UNKNOWN for offline/unverifiable targets.
8. Query G current Context target and delivery ledger; reconcile unresolved/late IDs.
9. Validate candidate Snapshot/Delta against exact G ContextVersion/base/target, expiry and supersession; reject stale Snapshot or mismatched Delta.
10. Reauthorize and recheck PermissionEpoch + ForgetFence immediately before apply and final submission.
11. Apply only current authorized Context into the declared managed region; never replay historical queued payload before reconciliation.
12. Emit Applied Attestation only at its declared observability tier and final-request boundary, separate from Forget ACK.

If trusted state cannot be established, remain blocked for protected memory and fail closed. Offline Adapter is Pending/Unknown, never automatically cleared or confirmed.

## 8. Applied Attestation is not Forget ACK

Applied Attestation proves only that a particular Adapter at a particular capability epoch materialized a specified G ContextVersion in a declared managed region at the defined inference submission boundary, bound to delivery/session/request and current authorization/fence. It does not prove model attention, comprehension or use.

Forget ACK proves only a particular local suppression, buffer-clear, cache-purge or queue-cancel action for one target and region/session. It does not prove Context Applied, canonical suppression, all-target cleanup, provider deletion or global Forget completion. Separate message types, status enums, predicates and audit evidence are required.

## 9. Conformance scenarios

| ID | Scenario | Allowed result | Forbidden result | Evidence |
|---|---|---|---|---|
| H-FRG-01 | Normal online Clear | Suppress, perform supported local actions, emit separate ACKs | Generic “deleted” ACK | Target tuple, epochs, region coverage, per-action postcondition/time |
| H-FRG-02 | Forget while Adapter offline | Target remains Pending/Unknown | Offline inferred cleared/confirmed | Last session, unreachable state, no positive ACK |
| H-FRG-03 | Reconnect with expired PermissionEpoch | Refresh/re-authorize; deny protected apply | Cached ALLOW or old Context replay | Old/current epoch, decision result, suppression |
| H-FRG-04 | Reconnect after Fence advanced | Suppress/clear before Context use; reconcile current G target | Apply pre-fence Snapshot/Delta | Old/current fence, clear evidence, stale rejection |
| H-FRG-05 | Old Delivery resent after Clear | Reject stale/superseded; keep suppression | Reinsert content | Delivery ID, G version, fence, digest, rejection |
| H-FRG-06 | Capability lacks complete Clear | UNSUPPORTED or narrower ACK with exact coverage | Claim full purge or self-authorize exception | Capability/epoch, uncovered classes, reason |
| H-FRG-07 | ACK lost, command repeated | Replay same ACK/evidence idempotently or reconcile | Assume action failed/succeeded; conflicting ACK | Stable operation/ACK IDs, digest, attempt IDs, durable journal |
| H-FRG-08 | Adapter Instance replaced | New instance separately authenticates/inventories | Transfer old ACK to new identity | Old/new instance refs, issuer/session, registration |
| H-FRG-09 | Managed Region changes | New region revision/capability epoch | Reuse old coverage as new clear | Region revisions, epoch transition, inventory |
| H-FRG-10 | Permission revocation races Apply | Final-boundary recheck; block if revocation wins; preserve historical event if submit already crossed boundary | Use stale lease or claim retroactive recall | Epochs, decision, linearization and request evidence |

## 10. Retry, idempotency and open ownership

ACK identity is stable for one completed action/evidence digest. Retransmission reuses ACK ID and digest; transport attempt ID may change. Same operation key + same target digest returns stored result/resumes idempotently. Same key + different digest is a conflict. Missing ACK after local success remains UNKNOWN remotely until queried/replayed. Retry reauthenticates and refreshes both epochs; it cannot extend expiry or bypass revocation. Late ACK is historical only if identity and ordering are verifiable; it cannot reverse newer fence, revocation or G supersession. Unprovable ordering remains UNKNOWN.

Open decisions:
- I: target classes, required actions, evidence predicates, PolicyException authority/expiry/controls, completion aggregation, PermissionEpoch partition/currentness API and trust profile.
- D: canonical ForgetFence token/reference, validation/comparison API and target selector.
- B: final ActorRef/ScopeRef schema and issuer/namespace mapping.
- G: ContextVersion wire reference, delivery status vocabulary and per-session Adapter inventory.
- C/runtime: final inference submission hook and request identity.
- Engineering: durable Adapter journal, cache/queue inventory completeness and crash-consistency tests.

H acceptance means only the H wire/SDK evidence contract is specified and internally aligned. It does not mean cross-owner approval, implementation conformance, physical erasure or Global Forget Completion have passed.
