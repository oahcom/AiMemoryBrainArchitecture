# Phase 3.6 — Context Applied State, Forget and Reconciliation Contract

- Owner: Session G — ContextVersion, Delivery, Applied State and Reconciliation
- Status: **G semantic decisions recorded; C/G/H Applied contract FREEZE BLOCKED; implementation/execution NOT VERIFIED**
- Branch: session-g-memory-context
- Authorities: G owns desired Context and Applied record; C produces final-request evidence; H owns wire/ACK/capability; I owns authorization; D owns ForgetFence.

## 1. Context evidence stages

G maintains independent Context, Delivery and Entry lifecycles. The following request-bound stages are strictly distinct:

Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started

- **Prepared:** G has committed/identified an immutable ContextVersion and Delivery intent.
- **Delivered:** H has authenticated transport receipt for a specific DeliveryId/attempt.
- **Materialized:** Adapter reports exact content in its declared Managed Region.
- **Final Request Submitted:** C provides trustworthy evidence that the exact immutable request, including the exact region digest, crossed the actual submit boundary.
- **Applied:** G validates all predicates and commits a per-request Applied record.
- **Execution Started:** correlated runtime/provider execution-start evidence.

G's Applied record means only that the specified ContextVersion was included in the exact submitted request under valid authorization/fence/capability bindings. It does not prove model attention, understanding, recall, behavioral use or correctness.

## 2. Applied state machine

Delivery and Applied evidence are per Adapter instance, Runtime Session, Context, Delivery and InferenceRequestId; a single scalar applied_version is insufficient.

| State | Entry condition | Allowed next states | Notes |
|---|---|---|---|
| Prepared | G commits immutable target and delivery intent | Delivered, Rejected, Expired, Superseded | Not sent |
| Delivered | H authenticated transport receipt matches DeliveryId/attempt | Materialized, Rejected, Expired, Superseded | Not Applied |
| Materialized | Adapter evidence confirms exact managed region and digest | FinalRequestSubmitted, Rejected, Expired, Superseded | Not final request proof |
| FinalRequestSubmitted | C evidence proves actual immutable final request submission | Applied, Rejected, Unknown | G validates predicate; submission fact can be retained historically |
| Applied | G accepts complete predicate and writes immutable Applied record | ExecutionStarted, InvalidatedForCurrentUse | Historical fact retained |
| ExecutionStarted | Correlated runtime/provider start evidence | Completed/Failed if separately observed | Does not imply successful completion |
| InvalidatedForCurrentUse | Later Forget/revocation/scope/session/capability/supersession invalidates future reuse | ReconcileRequired | Historical Applied record retained |

Partial/Unknown/Bypassed/Unsupported are evidence dispositions, not synonyms for Full Applied. Tier 2 and Tier 3 cannot transition to Full Applied. An Adapter without final boundary observability remains Limited/Unsupported.

## 3. Applied Acceptance Predicate

G accepts Full Applied only if **all** conditions hold at the final request submission boundary and are verified against authoritative owner evidence:

1. ContextId and exact immutable ContextVersion match the active G target.
2. DeliveryId and DeliveryAttemptId match the exact non-superseded attempt.
3. InferenceRequestId and FinalRequestBoundaryId are actual, unique and bound to the same request.
4. Agent principal/reference/instance, Adapter principal/reference/instance, Runtime instance and Runtime Session are authenticated, registered, current and mutually bound.
5. Exact ScopeRef and required EnvironmentRef match the Context and authorization decision.
6. Managed Region identity/inventory and complete region content digest match the target actually delivered/materialized.
7. PermissionEpoch and I authorization decision are valid/current at the final submission boundary.
8. D ForgetFenceGeneration/Cursor is current for all canonical source and transitive lineage represented in the region.
9. H AdapterCapabilityEpoch is current, bound to this Adapter instance/session and supports final immutable request observation.
10. C Final Request Submitted evidence is complete, immutable, integrity-valid, non-replayed and causally ordered after matching delivery/materialization.
11. H transport/ACK evidence required to bind authenticated delivery and Adapter instance is valid.
12. No supersession, revocation, fence, Scope/Environment change, session replacement or capability downgrade linearized before submission.
13. All required source references remain eligible and no unknown coverage gap exists.

Missing, stale, ambiguous, unverifiable or mismatched evidence rejects Full Applied. No local G inference can replace C's final-request evidence, H's protocol proof or I/D authority checks.

## 4. Historical truth versus current validity

- An Applied record is append-only historical evidence.
- Forget or revocation does not rewrite an actually valid historical Applied fact.
- Current-use validity is a separate projection, recomputed against current D fence, I PermissionEpoch/decision, Scope, Environment, Context head, Adapter capability and session.
- If valid submission linearized before later Forget/revocation, retain Applied history and mark it InvalidatedForCurrentUse.
- If Forget/revocation linearized before submission, do not accept Full Applied.
- If ordering cannot be proven, mark Unknown and suppress the region for future use.
- A late ACK can add historical evidence only; it cannot roll back a newer ContextVersion or newer Delivery attempt.
- Duplicate same identity/digest is idempotent. Same identity with changed digest is a conflict and must not promote state.
- Old Session/Adapter ACK is never rebound to a new session or capability epoch.

## 5. Forget and revocation handling

On D ForgetFence advancement or I revocation/PermissionEpoch change, G immediately installs a durable deny tombstone keyed by canonical source identity, transitive lineage and exact Scope coverage. Before physical cleanup, G:

1. Suppresses affected ContextEntry materialization and canonical dereference.
2. Marks affected ContextVersions non-serving for new requests; historical immutable versions remain audit-only.
3. Invalidates affected ChangeSets and prevents stale staged edits from committing.
4. Invalidates Snapshots and Deltas containing affected entries; stale targets become non-sendable.
5. Cancels/supersedes Pending Delivery and every active attempt whose final gate has not passed.
6. Marks historical Applied references InvalidatedForCurrentUse; does not erase the historical fact.
7. Invalidates G caches/queues and any reconnect restoration state.
8. Emits G-owned action-specific target evidence; it cannot claim F index/cache purge or H Adapter local purge.
9. Reconciles current Context head to a new safe version only after canonical lineage, D fence and I permission are revalidated.

Context Remove is only membership removal. It is not Canonical Forget and cannot satisfy a Forget target.

## 6. Object disposition matrix

| Object | Forget/revocation action | Audit/history rule |
|---|---|---|
| ContextEntry | Suppress; mark invalidated; remove from current desired membership | Retain non-reconstructive identity/provenance metadata as policy permits |
| ContextVersion | Invalidate for serving; create successor version without forgotten/unauthorized content | Immutable historical version retained, never replayed |
| ContextChangeSet | Cancel/reject if pending; revalidate if committed but not delivered | Retain digest and disposition, not forgotten plaintext |
| Snapshot | Invalidate and mark non-sendable if contains affected lineage or stale auth | Historical digest/target metadata only |
| Delta | Invalidate if base/target chain contains affected lineage or stale authorization | Never replay across tombstone/supersession |
| Pending Delivery | Cancel/supersede; reject send/apply at final gate | Retain attempt and cancellation evidence |
| Applied Context | Preserve historical Applied fact; invalidate current-use eligibility | No reuse until fresh authorization/reconciliation |
| Cached Context | Suppress and invalidate immediately; clear supported local bytes | Do not claim physical erasure without proof |
| Reconnect State | Invalidate old session snapshot/delta/ACK; force fresh auth and reconciliation | Retain minimal replay-deny marker and audit evidence |

PermissionEpoch changes require reauthorization even when ContextVersion is unchanged. A same-version Context is not proof of current permission.

## 7. Reconciliation and reconnect protocol

Reconnect is a new trust boundary, not continuation of old local state.

1. H authenticates current Adapter/Agent/runtime identities and establishes a new session.
2. H negotiates current protocol/capability profile and CapabilityEpoch.
3. I supplies current PermissionEpoch and exact action/Scope authorization.
4. D supplies current ForgetFence state for each source/lineage.
5. G persists/validates deny tombstones and cancels stale deliveries/attempts.
6. Adapter suppresses/clears local state to its declared capability; H emits action-specific evidence (SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN, UNSUPPORTED).
7. G reads authoritative current Context head, delivery ledger, desired target and unresolved attempts.
8. Old Snapshot is rejected if superseded, tombstoned, stale, cross-scope or unauthorized. Old Delta is rejected unless exact base equals current known adapter base and target remains current and authorized.
9. Unknown continuity requires a new full Snapshot only after current identity/permission/fence checks; unknown authority blocks rather than snapshot replay.
10. Immediately before apply and again before final request submission, revalidate PermissionEpoch, D fence, ContextVersion/delivery status, expiry/supersession and CapabilityEpoch.
11. G accepts Applied only through the predicate in §3.
12. Reconnect completion means this session is reconciled to a current authorized Context target only. It is not global Forget completion or physical erasure.

No old queued payload or old Session ACK is replayed before this sequence. Offline remains Pending/Unknown, never implicitly clear.

## 8. Conformance matrix

All cases are **SPECIFIED / NOT RUN** in this design pass. Test Passed requires executable fixture, deterministic concurrency ordering, environment, expected/actual output, durable evidence and owner sign-off.

| ID | Fixture / operation order | Expected | Forbidden | Evidence |
|---|---|---|---|---|
| G-36-01 | Materialized but no final submit evidence | Materialized only; no Applied | Materialized→Applied | Region receipt; absent C submit evidence |
| G-36-02 | Final submit evidence valid, G acceptance pending | FinalRequestSubmitted only | Claim Applied before predicate commit | C evidence and G validation record |
| G-36-03 | Full predicate passes | G commits per-request Applied | Infer model comprehension | All predicate refs and immutable Applied record |
| G-36-04 | PermissionEpoch changes before Applied decision | Reject/Unknown; reauthorize | Accept stale permission | Old/new epoch and decision |
| G-36-05 | Fence advances during delivery | Tombstone, cancel/supersede, no new Applied | Send/apply stale snapshot | Fence, delivery attempt, cancellation |
| G-36-06 | Valid Applied then later Forget | Preserve history; mark current-use invalid | Rewrite history or reuse | Applied record, fence and invalidation |
| G-36-07 | Late ACK for superseded ContextVersion | Historical only; current pointer unchanged | Rollback current version | Old/new versions and ACK ordering |
| G-36-08 | Duplicate ACK same digest | Idempotent | Double promotion | ACK identity/digest and prior result |
| G-36-09 | Duplicate ACK changed digest | Conflict/quarantine | Last-write-wins | Both digests and audit event |
| G-36-10 | Old Session ACK after reconnect | Reject or historical only | Rebind to new session | Old/new session and capability epoch |
| G-36-11 | Cross-Scope delivery attempt | Reject before materialization | Cross-scope content | Typed scopes and I decision |
| G-36-12 | ContextVersion unchanged but PermissionEpoch changed | Reauthorize before reuse | Treat version as permission proof | ContextVersion plus old/new epoch |
| G-36-13 | Reconnect offers old Snapshot/Delta | Suppress/clear then reconcile; reject stale artifact | Restore then clean later | Current authority vector and stale rejection |
| G-36-14 | Remove operation without canonical Forget | Remove membership only | Claim canonical deletion/global Forget | ChangeSet and D operation absence |
| G-36-15 | Forget races final request submission | D/I boundary order determines; ambiguity blocks | Submit under stale fence or invent order | D fence, I decision, C boundary proof |

## 9. Prompt injection / trust boundary

Context is a data region, not an instruction region. Entries carry source refs, provenance, trust/epistemic and lifecycle status, Scope, classification and validity. Summary/compaction is a derived untrusted artifact and must preserve provenance/lineage and trust labels. No content may enter system/developer instructions, tool definitions, tool authorization or Agent policy. Cross-Scope entries are rejected. Tool-call declarations in memory are not execution evidence.

## 10. Open findings and decision record

- **G-36-01 BLOCKED:** C evidence schema/integrity and final-boundary proof requires C/H agreement.
- **G-36-02 BLOCKED:** H ACK/capability/reconnect wire contract remains H-owned and not frozen here.
- **G-36-03 BLOCKED:** I PermissionEpoch freshness/revocation and B typed identity/Scope semantics require owner approval.
- **G-36-04 BLOCKED:** D/E/Storage physical Forget publication atomicity and durable gate are not implementation-verified.
- **G-36-05 NOT RUN:** no executable Applied, race, reconnect, stale replay or injection test output supplied.

**G decisions:** G is authoritative for Applied state; Applied requires complete request-bound evidence; historical Applied and current-use validity are separate; Forget/revocation invalidates all current delivery/reconnect surfaces but does not rewrite history; Context Remove is not Canonical Forget; reconnect always reauthenticates and reconciles current authority before restoring context.

**Cross-module status:** Applied Contract Frozen = NO. Runtime Forget End-to-End Closed = NO. No global Forget completion or physical erasure claim is made.
