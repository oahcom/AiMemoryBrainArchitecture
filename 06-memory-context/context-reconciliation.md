# Context Reconciliation

**Status:** DECIDED safety ordering; CANDIDATE workflow implementation  
**Owner:** Session G  
**Related:** INT-P0-02, INT-P0-03, INT-P1-06

Requirement ID `CR-01` is a stable reference for the 1 MUST occurrence in
this document. It is a label only; the normative text is unchanged. Other
documents SHOULD cite `CR-nn` rather than a section number, because section
numbers drift.

## 1. Purpose and sources

Reconciliation compares desired Context with current canonical, permission, temporal, retrieval-freshness and Adapter-delivery reality. It detects drift and creates a new valid Context version or blocks use. It does not change Canonical Memory or decide claim truth.

| Signal | Authority | G behavior |
|---|---|---|
| Memory identity/version/lifecycle | D canonical authority | Re-resolve exact ref and eligible successor |
| Revision/retract/Forget | E event stream plus D/I status | Tombstone immediately; do not wait for index |
| Entity/Relation changes | D | Revalidate affected references/paths |
| Permission/policy revocation | I | Reauthorize each entry and delivery |
| Retrieval completeness/index watermark | F | Mark incomplete/stale; omission is not proof of absence |
| Applied/delivery evidence | H Adapter attestation recorded by G | Compare per-delivery target to per-session applied state |

A stale index is a projection problem, not canonical authority. If F's watermark trails relevant canonical events, mark Stale/ReconcileRequired; validate directly with D or conservatively block affected entries.

## 2. Trigger classes

Canonical revision/supersession; retraction/Forget; Entity merge/split; Relation revision/retraction; evidence/provenance revision or source unavailability; Scope/policy change; permission revocation; entry expiry; Context TTL or environment/session closure; index lag or retrieval truncation; delivery gap/rejection; Adapter restart/capability change; timeout/late Applied ack; periodic audit.

## 3. State distinctions

- **Stale:** known source, index, policy or delivery watermark differs from last reconciled baseline.
- **ReconcileRequired:** a concrete event/ref/permission/delivery gap requires a run; unsafe affected entries are blocked pending outcome.
- **Reconciled:** a run completed for a declared watermark/scope, with affected refs valid, replaced, removed or explicitly unresolved/blocked. This is a run result, not a permanent Context Lifecycle state.
- **Blocked:** authorization, Forget, Scope, integrity or canonical eligibility cannot be established.
- **Closed:** Context lifecycle terminal; reconcile may only perform governed cleanup/audit, not reactivate.

Context Lifecycle may be Active after a successful run. Preserve the Reconciled run record separately; do not add Reconciled to Delivery or Entry lifecycle.

## 4. Reconciliation algorithm

1. Persist trigger ID, source watermark, affected refs, Scope hint, timestamps and correlation.
2. Resolve exact Contexts by canonical IDs and environment/task/Agent Scope; never broad-match names.
3. Install immediate deny/tombstone for Forget, retraction, revocation or invalid environment identity before expensive work.
4. Load Context head, immutable snapshot, pending Change Sets/deliveries and Adapter/session attestations.
5. Reauthorize principal, Context, every Memory/evidence/rendering ref and target Adapter under current policy epoch.
6. Resolve canonical Memory ID/version, lifecycle, successor/superseded/retracted status, Claim/Entity/Relation and provenance through D.
7. Compare E event and F index watermarks; detect delay/truncation. Missing index result is not deletion.
8. Classify each entry: Valid, StaleRevision, Retracted, Forgotten, PermissionRevoked, Expired, ScopeMismatch, SourceUnavailable, Superseded, ConflictChanged or Unknown.
9. Plan compensation: Update to validated successor, Replace, Remove/Expire, compact, defer or Block. Never silently replace a disputed claim with a preferred one.
10. Commit atomic Change Set against current Base Version; on CAS failure reload and recompute.
11. Cancel/supersede pending deliveries, send latest Snapshot/Delta, request adapter clear where required, collect per-target outcomes.
12. Record watermarks, auth epoch, refs examined, operations, unresolved gaps and delivery evidence. Mark run Reconciled only for declared scope/watermark.

## 5. Forget and revocation protocol

### Immediate logical invalidation

On Forget, G:
- persists deny tombstone keyed by canonical memory identity/version family and affected Scope;
- makes matching entries ineligible immediately in reads/planning/delivery, even if historical immutable snapshots still contain refs;
- cancels/supersedes pending Change Sets and deliveries containing target;
- invalidates Snapshot/Delta materializations and caches by Scope + memory ref + policy/Forget epoch;
- blocks new Applied confirmation for deliveries containing target;
- creates clear/quarantine requests for every Adapter/session that may have received target.

Tombstone check is mandatory immediately before delivery and at Adapter application boundary. Historical snapshots are audit-only and never served as current state.

### Adapter states and offline behavior

Track per target Adapter/session: **pending**, **confirmed**, **failed**, **unknown**.
- pending: clear requested/required but not attested.
- confirmed: Adapter attests target removed/quarantined from managed region and local managed cache under declared capability.
- failed: Adapter cannot clear or validation fails; remain blocked and retry/escalate.
- unknown: offline, timeout, lost ack or insufficient visibility.

Offline Adapter remains unknown/pending. On reconnect it authenticates, re-resolves Scope, fetches current Forget/revocation epochs, discards stale cached Snapshot/Delta, applies safe replacement Snapshot/clear set, then attests. It cannot reuse cached Context before reconciliation.

### Completion boundary

G reports Context-side propagation complete only if no active/pending Brain Context/Delivery can expose the target and every known Adapter/session is confirmed cleared/inaccessible. Unknown or failed targets remain explicit exceptions; global result is not confirmed complete. Historical retention is I-governed. G cannot claim external model/provider physical erasure or erase tokens already processed by prior inference. I owns canonical Forget completion and external boundary claims.

## 6. Partial failure and index incompleteness

Reconciliation is a resumable saga; results are per Context and Adapter session. Retries use trigger ID + Scope + target watermark + payload hash. Failed stages retain tombstones; no retry resurrects a blocked entry.

F supplies watermark, completeness, truncation and uncertainty. If incomplete/unknown, preserve coverage gap, do not infer absence, validate existing entries directly with D, schedule re-retrieval after watermark catch-up and mark sufficiency incomplete where required coverage may be missing.

## 7. Audit and decisions

Audit trigger/source/watermark, Context IDs, canonical refs as permitted, policy epoch, affected Adapter sessions, tombstone epoch, classifications, operations, Change Set/version IDs, Delivery IDs, acknowledgements and unresolved failures. Do not log memory plaintext merely to prove cleanup.

- **DECIDED:** D remains canonical authority; indexes are projections; Forget/revocation tombstone wins immediately; reauthorize during reconcile and before delivery/application.
- **CANDIDATE:** event-driven invalidation plus periodic watermark sweep.
- **TO_VALIDATE:** fan-out, propagation lag and reconnect convergence.
- **OPEN:** canonical Forget proof (I); event/watermark schema (E); completeness (F); Adapter clear attestation (H).


## 8. Phase 3.5 ForgetFence, typed inventory and target-evidence alignment

### 8.1 Authority and cursor separation

G consumes but does not create or redefine the following:
- D ForgetOperationId, ForgetFenceCursor/Generation, CanonicalCommitCursor, ProducerRegistryVersion, ProducerRegistrationSequence/HighWater, dependency inventory and D barrier receipts;
- I PermissionEpoch, ProducerDomainInventoryEpoch, TargetInventorySeal, TargetId, required action, target state, PolicyException and Global Forget Completion;
- F per-index/per-partition IndexWatermark and completeness/truncation evidence;
- H CapabilityEpoch and action-specific Adapter ACK evidence;
- G ContextVersion, ChangeSet, DeliveryId and attempt identities.

These are typed opaque references from independent authorities. No max, numeric comparison, arithmetic or conversion across them is valid. D's ProducerRegistrationHighWater is a per-Forget work barrier, not I's global ProducerDomainInventoryEpoch. A sealed I target inventory does not prove D's producer work drained. An F IndexWatermark does not prove Forget suppression or cleanup. G ContextVersion does not prove Adapter application.

### 8.2 G producer registration and barrier participation

G is a registered derivative producer for Context membership/materializations, ChangeSets, snapshots, deltas and delivery intents. Before derivative-capable work is queued, leased, executed or allowed to dereference protected canonical content, G registers the producer class and stable ProducerWorkItemId with D. The work record binds canonical request digest, exact source refs/revisions and transitive lineage, ScopeRefs, Context/artifact identity, admission CanonicalCommitCursor, observed ForgetFenceCursor, I PermissionEpoch/decision and correlation refs. Retries preserve WorkItemId/digest; attempt/lease identities are separate.

Every derived Context artifact registers complete dependencies with D before visibility. G consumes D's RegisterDerivedDependency and PublishDerivedIfFenceCurrent semantics; these names are semantic contracts, not a claim of an available callable API. The final fence/permission check must serialize with the artifact visibility transition. If D/Storage cannot provide the atomic/recoverable gate, G keeps the artifact private and no sendable delivery is created. G completes producer work only with durable terminal evidence; expired lease, deleted queue message or lost ACK is not terminal.

### 8.3 Forget immediate suppression and Context invalidation

When D installs a ForgetFence covering a Memory identity or ancestor lineage, G immediately installs a deny tombstone before expensive reconciliation. It:
1. blocks affected entries in active Context reads/planning and blocks new inclusion;
2. invalidates affected staged ChangeSets and private/pending materializations;
3. cancels or supersedes Prepared/Delivered deliveries where possible and blocks any late Applied promotion;
4. invalidates affected snapshots, deltas, compaction artifacts and G caches by Scope + lineage + D fence reference + I PermissionEpoch;
5. commits a safe replacement ContextVersion only through complete D dependency registration and final publication gate;
6. emits G-owned target evidence for I's sealed inventory, while requesting H's separate Adapter suppression/clear actions;
7. keeps old immutable versions only as non-serving audit history under I retention rules.

The tombstone is checked on read, plan, edit, replay, snapshot construction, immediately before delivery and in the H apply/reconnect gate. A stale cached fence or missing current fence is fail-closed. A new Memory ID, rendering hash or compaction ID cannot escape source-lineage coverage.

### 8.4 I target evidence from G

I owns TargetId and TargetInventorySeal. G never invents target identity or decides global state. For each I-registered G target slice, G emits evidence binding:
- ForgetOperationId, TargetId and inventory seal reference;
- exact ScopeRef coverage and G producer identity/instance;
- D ForgetFenceCursor and relevant I PermissionEpoch/authorization decision;
- target class and action/postcondition (Context access suppression, snapshot/delta invalidation, ChangeSet/delivery cancellation, G cache/queue invalidation, or other explicitly registered G surface);
- Context IDs, ContextVersion(s), ChangeSet IDs, Delivery IDs/attempts and ProducerWorkItemId/terminal receipts as applicable;
- attempt, timestamp, integrity/evidence reference, correlation/causation and unresolved coverage gaps.

G may report only the action it controls. It cannot claim H Adapter cache purge from a G delivery cancellation, F index cleanup from a G snapshot invalidation, backup erasure, external recipient deletion or global Forget completion. I evaluates target state as Pending, Confirmed, Failed, Unknown or PolicyException. G's local result remains evidence, not I's state.

### 8.5 Adapter ACK and offline reconnect

H ACK classes are distinct: SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED. Each is bound to an authenticated Adapter instance/runtime session, ScopeRef, Managed Region, capability epoch, action and exact target. G stores the evidence and correlates it to its Context/Delivery; I decides whether it satisfies the target requirement. A generic "cleared" or "deleted" response is not accepted.

Offline Adapter remains Pending/Unknown. On reconnect, H authenticates identity, refreshes current I PermissionEpoch and D ForgetFence for affected lineage, suppresses/clears stale local state, reports action-specific evidence, queries G's current Context/delivery ledger, rejects stale Snapshot/Delta and only then restores a current authorized managed region. No old cache or queued payload is replayed before this sequence. A missing ACK remains Unknown; UNSUPPORTED is not success and only I may approve a PolicyException.

### 8.6 Reconciliation completion boundaries

G may report its Context-side propagation complete only when no active or pending G-owned Context artifact/delivery can expose the target and every known G-owned target slice is reconciled with accepted evidence. G does not declare global Forget complete. I's global completion requires its sealed ProducerDomainInventoryEpoch/TargetInventorySeal, D's producer work barrier and canonical suppression proof, E/F/G/H target evidence, external-copy and backup/restore obligations, and required physical-erasure evidence or valid PolicyException. Unknown, missing target, invalidated seal, late derivative, unresolved D work item or pending H Adapter target prevents I completion.

### 8.7 Typed reconciliation inputs

A reconciliation run records the exact typed vector it observed: D CanonicalCommitCursor, D ForgetFenceCursor, D ProducerRegistryVersion and ProducerRegistrationHighWater/barrier receipt; I PermissionEpoch and ProducerDomainInventoryEpoch/TargetInventorySeal; F IndexWatermark per index/partition with gap/coverage status; G Base/Target ContextVersion; H CapabilityEpoch and per-session ACK evidence. A run cannot collapse these into one freshness integer. If any required authority is unknown, stale or gapped, the run remains Blocked/Unknown for affected references.


## 9. Phase 3.5 — Reconnect contract, concurrency and conformance

### 9.1 Normative reconnect contract (H executes wire/Adapter order; G supplies current Context state)

**CR-01** — Reconnect MUST be treated as a fresh authorization and reconciliation boundary, not a continuation of the last local session.

1. H authenticates transport and binds Adapter Principal/Instance, Agent Principal/Instance, Runtime Instance/Session, issuer, audience and typed ScopeRef. Payload IDs remain claims only.
2. H negotiates protocol/schema and capability set; establishes current CapabilityEpoch. A changed Adapter instance or capability epoch invalidates old proof coverage for new actions.
3. H obtains authoritative current I PermissionEpoch and action-specific authorization for the exact recipient/Scope/Context.
4. H obtains authoritative current D ForgetFence for every relevant target and source lineage. G never supplies a cached fence as authoritative.
5. H persists suppression markers and clears/suppresses affected managed-region state, buffers, caches and local queued deliveries to the declared capability extent. G independently tombstones affected Context entries and cancels/supersedes G-owned pending deliveries.
6. H submits action-specific ACK evidence (SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN or UNSUPPORTED). G stores/correlates the evidence; I alone decides whether it satisfies an inventory target. No ACK class is silently promoted to another.
7. H queries G for the current Context head, exact desired target, delivery ledger and unresolved attempts. G responds from authoritative state, not a stale cache or an Adapter-provided version.
8. G/H reject any Snapshot older than the current desired ContextVersion, any Snapshot containing a currently tombstoned/fenced/unauthorized lineage, and any Delta whose BaseVersion is not the exact current Adapter version or whose TargetVersion is superseded.
9. If Adapter continuity, version chain, fence or permission epoch is unknown/gapped, H requests a full current Snapshot only after the suppression/authorization gates; it does not replay old queued payloads.
10. Immediately before applying the new Snapshot/Delta and again at final inference submission, H rechecks current PermissionEpoch, D ForgetFence, G ContextVersion/delivery status, expiry/supersession and CapabilityEpoch.
11. H applies only the current authorized managed region and emits separate Delivered, materialized and final-request Applied evidence. G marks Full Applied only after validating the C/H evidence mapping in context-versioning §14.3.
12. If any authoritative state is unavailable, incomparable, stale or gapped, protected memory remains blocked and outcome is Unknown/Pending. Offline is never inferred clear or Applied.

Reconnect completion means only that this Adapter session has reconciled to a current authorized Context target. It does not mean global Forget completion or physical erasure.

### 9.2 Old Snapshot/Delta anti-resurrection

- A Snapshot is acceptable only when ContextRef, exact TargetVersion, digest, Scope binding, current PermissionEpoch and current D fence all validate.
- A Delta is acceptable only when its BaseVersion exactly equals the Adapter's known applied base, its ordered operations are complete, and the target remains current and authorized.
- A duplicate DeliveryId + AttemptId + digest returns the recorded result without replaying side effects.
- A duplicate identity with a different digest is rejected as a conflict.
- Any attempt invalidated by Forget, revocation, scope change, supersession or expiry is non-replayable even if a new message ID is assigned.
- If version continuity is unknown, require a fresh Snapshot; if authorization/fence continuity is unknown, block rather than snapshot-replay.
- Tombstones and replay-deny markers must survive Adapter restart for the required replay/retention horizon. G's tombstones survive Context reconstruction and are keyed by source lineage/Scope, not display text or rendering hash.

### 9.3 Concurrency and fault matrix

| ID | Race/fault | Linearization / winner rule | Required outcome | Evidence |
|---|---|---|---|---|
| G-CON-01 | Duplicate ChangeSet | Principal+Context+family+idempotency key; payload hash decides | Same hash returns original version/result; different hash rejects | Key, principal, Context, normalized hash, original result |
| G-CON-02 | Duplicate ACK | Adapter+Delivery+Attempt+ACK identity; digest decides | Same digest idempotent; different digest conflict; no second promotion | ACK identity/digest, prior outcome, Adapter/session |
| G-CON-03 | Out-of-order ACKs | Per-attempt state + trusted event sequence and invalidation order | Older ACK may be historical only; never overwrite newer attempt/current head | Attempt IDs, sequence, observed times, target versions |
| G-CON-04 | Context update vs Delivery | Delivery captures immutable TargetVersion; commit/head CAS serializes | If update wins first, old delivery superseded; if delivery prepared first, final send/apply gate rechecks current head and aborts stale target | Base/target versions, CAS result, delivery state, gate receipt |
| G-CON-05 | Forget vs Delivery | D fence + final D publication gate is authoritative; tombstone is immediate deny | If fence wins before visibility/apply, staged artifact remains private and delivery is cancelled/superseded; if already submitted, retain historical request evidence but invalidate current use and reconcile Adapter | ForgetFence, producer work/dependency receipts, visibility decision, delivery/attempt, final boundary |
| G-CON-06 | Permission Revocation vs Applied | I PermissionEpoch/authorization at final submission boundary decides | If revocation wins before final boundary, no Full Applied; if valid submission precedes revocation, preserve historical Applied then mark current-use invalidated | Old/new PermissionEpoch, decision refs, boundary ID/time, attestation |
| G-CON-07 | Reconnect vs old Delivery replay | H fresh auth/fence/capability + G current head queried before replay | Suppression and cancellation first; stale attempt rejected; only new current target may apply | Session/CapabilityEpoch, PermissionEpoch, ForgetFence, current ContextVersion, rejected attempt |
| G-CON-08 | Crash after local apply before ACK | No ACK is not proof either way | Unknown until exact request/session evidence reconciled; no duplicate side effect or automatic Applied | durable local attempt record, request ID, anti-replay identity, recovery query |
| G-CON-09 | Crash after tombstone before Context rebuild | Deny tombstone durable before expensive work | Affected entry stays blocked; retry rebuilds from current safe canonical refs into a new version | tombstone receipt, old/new versions, trigger and work IDs |
| G-CON-10 | D fence/permission authority unavailable | No cached authority is accepted as current | Fail closed; no new publish, delivery or apply for affected lineage | authority query failure, last-known token marked stale, blocked action |
| G-CON-11 | F watermark lag/truncation | F completeness is a separate input; omission is not deletion | Mark Stale/ReconcileRequired; direct D/I validation or block; do not compact away unknown coverage | per-index/partition watermark, completeness/truncation flags |
| G-CON-12 | CapabilityEpoch changes during delivery | H capability/session binding at action boundary | Old attempt cannot inherit new capability; supersede/re-negotiate and create a new attempt | old/new capability epochs, attempt IDs, negotiated set |
| G-CON-13 | Scope change races delivery | I current authorization and exact B ScopeRef binding at final gate | Old scope-bound delivery blocked; new scope requires re-resolution and new version/delivery | old/new ScopeRef, PermissionEpoch, scope fingerprint, gate result |
| G-CON-14 | Late derivative after fence | D registration barrier/dependency ledger and final publication gate | No visibility after closed barrier; unknown registration/atomicity remains OPEN and blocks publication | ProducerWorkItemId, registration sequence, fence, dependency receipt, terminal disposition |

Important implementation limitation: G can specify the winner rule but cannot claim it is executable until D and Storage/Consistency define and prove the atomic registration/fence/visibility boundary. A G-local check followed by an independent head write is not sufficient.

### 9.4 Conformance matrix (specification cases; NOT RUN)

| ID | Initial state | Input | State transition | Expected result | Forbidden result | Required evidence |
|---|---|---|---|---|---|---|
| G-CF-01 | v7 active; entry M@r1 valid; delivery Prepared | D fence covers M lineage | Entry→Forgotten/blocked; v7 non-serving; attempt→Superseded | New safe version excludes M after gated rebuild | v7 or old delta remains sendable | Fence, lineage match, tombstone, version and delivery IDs |
| G-CF-02 | v7 applied to session S1 | I revokes permission epoch P1→P2 | Entry blocked; applied ref→AuthorizationStale | No later request uses P1; reauthorize before rebuild | Treat P1 as current because TTL remains | Epochs, decision, session, invalidation record |
| G-CF-03 | v7 includes M@r1 | D reports canonical successor M@r2 | Entry→StaleRevision/Superseded; reconcile creates v8 only after validation | Exact r2 is added by new ChangeSet if eligible | Implicitly float r1 to latest | D resolution, old/new refs, ChangeSet and version |
| G-CF-04 | v7 scope fingerprint A; delivery Prepared | Scope binding changes to B | Entry/delivery blocked pending I/B resolution | New version/delivery only after new scope auth | Reuse A-bound delivery in B | Scope refs, fingerprints, PermissionEpoch, gate |
| G-CF-05 | v7; F index watermark behind required canonical point | Retrieval returns incomplete/truncated | Context→Stale/ReconcileRequired | Existing refs validated directly; coverage gap recorded | Infer missing candidate means delete/absent | Per-partition watermark and completeness flags |
| G-CF-06 | Delivery D1 Delivered; no final-request evidence | Transport receipt only | Delivered remains Delivered/Unknown | No Applied pointer | Delivered→Applied | H transport ACK and absence of C final-boundary evidence |
| G-CF-07 | D1 superseded by D2; D1 ACK arrives late | Valid old Applied ACK | D1 historical evidence only; current pointer remains D2/none | No rollback; D2 status unchanged | D1 becomes current Applied | ACK identity, target versions, invalidation order |
| G-CF-08 | Adapter offline with old Snapshot S7 | Reconnect after fence and permission epoch advanced | Offline→Unknown; reconnect gates→clear/suppress→query current head→fresh Snapshot | Only current authorized snapshot may apply | Replay S7 before fresh authority checks | Session, epochs, fence, current G head, stale rejection |
| G-CF-09 | Same ChangeSet key/hash already committed | Duplicate same payload | Return original committed result/version | Exactly one head advance | Second version or repeated side effect | Idempotency key/hash, original result |
| G-CF-10 | Same ChangeSet key, changed payload | Duplicate key with different normalized hash | Reject IDEMPOTENCY_KEY_REUSE | Head unchanged | Accept changed payload as retry | Principal, Context, key, old/new hash |
| G-CF-11 | ACK identity already recorded | Duplicate same ACK digest | Return prior result | No duplicate Applied record | Double-count evidence | ACK ID/digest, prior result |
| G-CF-12 | ACK identity already recorded | Same identity, different digest | Conflict/quarantine | No state promotion | Last-write-wins overwrite | ACK ID, both digests, security event |
| G-CF-13 | Delivery Prepared; Context head advances before send | Concurrent Context ChangeSet commits | Old delivery→Superseded; new target prepared | No stale send; new target gets new delivery | Send old snapshot based only on prior prepare | CAS, head versions, delivery state |
| G-CF-14 | Delivery Prepared; D fence installs before visibility gate | Forget races publish | Staged artifact remains private; no head advance/send | Abort/quarantine and reconcile | Publish based on pre-fence local check | D fence, registration/dependency receipts, final gate result |
| G-CF-15 | Final inference not yet submitted; I revokes permission | Permission revocation races Applied | No Full Applied; attempt blocked/Unknown/Rejected | Reauthorize or omit managed region | Apply stale ALLOW or promote later ACK | PermissionEpoch, decision, boundary evidence |
| G-CF-16 | Final request submitted with valid P1; P2 revocation occurs later | Historical Applied ACK arrives | Historical Applied preserved; current-use ref invalidated | No future reuse under P1 | Erase history or claim current authorization | Submission time, P1/P2, final boundary, invalidation |
| G-CF-17 | Adapter has current session but CapabilityEpoch changes | Old attempt ACK arrives | Old attempt remains historical/Unknown; new capability requires new attempt | No inherited Full coverage | Upgrade old attempt using new capability | Old/new epoch, session, attempt IDs |
| G-CF-18 | D/I authority unavailable during reconnect | Adapter requests current state | Reconnect remains blocked/Unknown | No Snapshot/Delta apply | Trust last cached fence/permission | Authority outage, stale token marker, blocked action |
| G-CF-19 | Remove operation committed in G | Old Snapshot/Delta replay contains removed entry | Replay rejected/superseded; tombstone remains | New version remains authoritative | Interpret Remove as Canonical Forget or resurrect membership | ChangeSet op=Remove, version, replay ID and rejection |
| G-CF-20 | G emits target evidence for I sealed inventory | I evaluates global Forget | G evidence covers only declared G target slice | I independently evaluates all target classes | G claims H/F/external/backup completion | TargetId/seal supplied by I, action, Context/delivery evidence, gaps |

These are normative design fixtures, not executed test results. A PASS requires executable test ID, fixture, environment, expected/actual result, reproducible artifact and owner sign-off.

### 9.5 OPEN items and ownership

| ID | OPEN item | Owner / dependency | G safe behavior until closed |
|---|---|---|---|
| G35-O-01 | D producer-class/work-item registration and fence-install linearization; durable receipts and crash/retry semantics | D + E + Storage/Consistency | Keep derivative work private; no public head advance or delivery if gate cannot be proven |
| G35-O-02 | Atomic/recoverable boundary coupling D dependency registration + PublishDerivedIfFenceCurrent to G Context visibility | D + Storage/Consistency + G | No independent G-local check-then-publish |
| G35-O-03 | B ActorRef/ScopeRef exact types and I Principal/issuer mapping | B + I + H | Fail closed on unresolved identity/scope; keep exact typed refs opaque |
| G35-O-04 | C final-request attestation schema/profile and executable proof tier | C + H | Full Applied only when every C/H predicate is verifiable; otherwise Partial/Bypassed/Unknown |
| G35-O-05 | H ACK wire schema, capability coverage and integrity profile | H + I + G | Store action-specific evidence; no generic “cleared” promotion |
| G35-O-06 | F canonical suppression, per-index watermark and completeness/truncation contract at current head | F + D + G | Do not infer absence from index omission; direct validate or block |
| G35-O-07 | I PermissionEpoch domain/continuity and revocation propagation guarantee | I + all consumers | Unknown/gapped/offline epoch blocks protected operation |
| G35-O-08 | Storage implementation, recovery, fault injection and cross-module visibility gate proof | Storage/Consistency + D/G | Specification only; no implementation conformance claim |
| G35-O-09 | Snapshot/delta digest canonicalization and retention/non-reconstructive audit policy | G + H + I | Treat digest as integrity only; retain no forgotten plaintext for proof |
| G35-O-10 | Per-entry delivery and partial-coverage semantics for mixed-safe/blocked target | G + H + C | Default atomic full-region apply or reject; Partial is never Full Applied |

### 9.6 Conformance disposition

Status: **CONTRACT SPECIFIED / IMPLEMENTATION AND EXECUTION NOT VERIFIED**. This update defines G-side state and evidence expectations. It does not prove Adapter behavior, D/Storage atomicity, C final-boundary observability, F suppression, I policy closure, physical erasure or global Forget completion.
