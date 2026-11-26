---
document_metadata:
  domain: memory-context
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
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a mirror that carried no front-matter: records domain, role, status and the canonical source path only (basis, the document's own statement: Status: G semantic decisions recorded; FREEZE BLOCKED; implementation/execution NOT VERIFIED). Claims no canonical authority and does not verify semantic parity with the source. Pre-metadata content blob: 1c0782271a01c01648d0917bed59da12e94fd9d7."
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md"
    en: null
    zh-CN: "docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md"
---
<!-- Source: session-g-memory-context / 06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md / Blob aa3afa73d8a76cc6f025839c52bfbff6a983046a -->
<!-- Chinese companion: ../../zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md -->

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


## Phase 3.6 CFG joint architecture closure addendum — G Owner decision

- Decision package: A-owned `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA reviewed: `61d961c32138fd875069e8cbac4696bb031447c0`
- G decision: **APPROVE WITH ENUMERATED EXCEPTIONS** for G-owned ContextVersion, Delivery and Applied semantics. This is not a global freeze and is not H approval.

### G accepted clauses

1. G owns desired Context state, immutable ContextVersion, ChangeSet commit, Delivery intent/target, reconciliation and the authoritative per-request Applied record. G does not own canonical Memory mutation/Forget, BMCP wire, Agent reasoning or tool execution.
2. The lifecycle is `Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`, with independent evidence and authority at each transition. G does not infer a later state from an earlier receipt.
3. Full Applied is per exact ContextId/ContextVersion + DeliveryId/attempt + InferenceRequestId + FinalRequestBoundaryId + authenticated Agent/Adapter/Runtime/Session + Scope/Environment + ManagedRegion revision/inventory + complete digest/profile + current I PermissionEpoch/decision + current D ForgetFence/lineage + H CapabilityEpoch + valid H delivery/identity proof + immutable C submission proof. Every predicate must be verified; missing, stale, mismatched, ambiguous or unverifiable evidence rejects Full.
4. G commits Applied idempotently by the exact request/attempt/evidence identity. Exact duplicate digest returns the original disposition; same identity with changed digest is conflict/quarantine. Late evidence may add historical fact only and cannot roll back a newer ContextVersion or Delivery attempt.
5. Historical truth and current-use eligibility are separate. A submit proven before a later Forget/revocation may be retained as historical Applied, but current-use is invalidated. If Forget/revocation precedes submit, reject Full. If order is ambiguous, Unknown and suppress.
6. Execution Started is a separate runtime/provider fact bound to the same InferenceRequestId; G does not infer it from Applied.
7. Remove is Context membership removal only. It does not create a canonical ForgetOperation, advance D's fence, or prove deletion. A D Forget independently tombstones every matching G entry by canonical lineage and exact Scope.
8. G deny tombstones suppress affected entries, non-serving ContextVersions, ChangeSets, Snapshots, Deltas, pending Delivery attempts, reconnect state and current-use projections before physical cleanup. Historical audit facts remain immutable subject to I retention policy.
9. Reconnect is a new trust boundary: H authenticates and negotiates the new session/capability; I and D provide current independent epochs/fence; G reconciles tombstones, delivery ledger and current head; old Snapshot is rejected when stale/superseded/tombstoned/unauthorized; Delta requires exact known base and current target; unknown continuity requires a new full Snapshot only after current checks. Revalidate again immediately before apply and final submit.

### Enumerated exceptions and external authority reservations

- **H wire exception:** G accepts the semantic separation of delivery receipt, materialization evidence, final-submit evidence, Applied record and Execution Started receipt. G does not freeze H message schema, ACK enums, signature profile, wire field encoding, replay journal or capability negotiation. H must explicitly accept the same package Blob SHA or issue a new common version.
- **C producer exception:** G cannot manufacture final-request proof; C remains the sole producer of exact submit evidence. The C decision must remain pinned to this package and the evidence profile.
- **I authorization exception:** I alone defines PermissionEpoch, Principal/Issuer/delegation, revocation and policy freshness. G requires a current decision but does not define its policy.
- **D Forget exception:** D alone defines ForgetOperation/Fence/lineage authority and ordering. G consumes D's current fence and durable target evidence.
- **B type exception:** B owns ActorRef/ScopeRef/EnvironmentRef typed semantics; G does not redefine them.
- **D/E/Storage publication exception:** a G ChangeSet may be staged privately but cannot become public Context head, sendable Snapshot/Delta or Prepared Delivery until dependency registration, current D fence, current I PermissionEpoch, D final publication gate and G BaseVersion CAS are all proven. Callable API/physical transaction realization remains open to D/E/Storage.

### Context operation and version rules reaffirmed

- Add/Update/Remove/Replace/Reorder/Expire/Compact/Reconcile are ChangeSet operations against one Context and exact BaseVersion; deterministic operation order and idempotency identity are required.
- Validate against a staged working copy; no partial target version becomes visible. A successful non-no-op ChangeSet creates one immutable ContextVersion; a stale base conflicts/reconciles rather than silently rebasing. Duplicate operation identity with identical payload is idempotent; altered payload is conflict.
- Remove writes a G membership tombstone only. Replace is atomic at ContextVersion publication; Reorder changes membership ordering only; Expire is evaluated against authoritative time/policy and must not resurrect on replay; Compact preserves provenance/trust/conflict labels and lineage; Reconcile revalidates canonical refs, permission, temporal validity, retrieval freshness and Adapter state.
- Context entries reference only legal canonical MemoryVersionRefs. A stale canonical ref is reconciled to an eligible successor only under D lifecycle semantics and current I authorization; no implicit float-to-latest.

### G decision consequence

G considers its semantic portion of the A package accepted with the exceptions above. The C/G/H Applied Contract remains **NOT FROZEN** until H explicitly accepts the same version and I/D/B provide their own authority confirmations. G conformance remains **SPECIFIED / NOT RUN**; implementation remains **NOT VERIFIED**.

## Phase 3.6.3 — Issue #3 exact-version G Owner decision

- Owner: G — ContextVersion, Delivery, reconciliation and Applied state authority.
- Exact shared package: reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md, Blob SHA 122b164bcc0760b83bf555072a36fc55631623e1.
- Decision: **APPROVE WITH ENUMERATED EXCEPTIONS** for G-owned Context/Delivery/Applied clauses. This is G's explicit Issue #3 decision, not a global freeze.
- Common contract version: **CGH-APPLIED-1.0**, anchored to the exact package Blob above.
- G owns the authoritative per-request Applied record. Full Applied requires exact ContextId/ContextVersion, DeliveryId/attempt, InferenceRequestId, FinalRequestBoundaryId, authenticated Agent/Adapter/RuntimeSession, verifier-resolved ActorRef, role-tagged ScopeBindingSet, applicable EnvironmentRef, complete ManagedRegion revision/inventory/digest/profile, current I PermissionDecision/PermissionEpoch, current D ForgetFence/lineage, H CapabilityEpoch and authenticated H ACK plus immutable C final-submit proof.
- Commit/idempotency: exact request/attempt/evidence identity; same identity+same digest returns original disposition; same identity+different digest is conflict/quarantine. Late evidence cannot roll back newer ContextVersion or Delivery attempt.
- Temporal rule: proven submit before later Forget/revocation may remain historical Applied while current-use is invalid; Forget/revocation before submit rejects Full; unknown order remains Unknown and suppressed. Sender wall clock is not ordering authority; owning authority commit cursor and trusted receiver receipt sequence are required.
- Exceptions: G does not own C final-request evidence, H wire encoding/cryptography, I authorization/PermissionEpoch policy, D ForgetFence/lineage, B typed references or Storage publication atomicity. This does not prove execution, attention, comprehension, recall, global Forget or physical erasure.
- Negative cases (missing C proof, invalid H binding, stale epoch/fence, scope/environment mismatch, unsupported tier, stale delivery, changed duplicate digest, ambiguous order) reject Full or remain historical/Unknown.
- CGH-01..20 remain **SPECIFIED / NOT RUN**.

## Phase 3.6.3 — Issue #6 G BIH consumer acceptance

- Exact BIH package: reviews/integration/phase-3.6-identity-trust-joint-architecture.md, Blob SHA a45ae90b318a79bf009d14f4d917611881e9e214.
- Disposition: **ACCEPT WITH ENUMERATED EXCEPTIONS** as a downstream consumer of BIH36-JD-01..17.
- Mapping: G binds authenticated Principal/Issuer and Adapter/Agent workload instance to RuntimeSession; ActorRef must be verifier-resolved and operation-bound. G preserves exact ScopeRef role set and applicable EnvironmentRef in Context, Delivery, Applied and reconciliation records. PermissionEpoch is opaque and I-issued; ForgetFence is a distinct D-issued token; CapabilityEpoch is H-owned.
- Enforcement: before Delivery authorization, on authenticated receipt/materialization, and at Applied commit, G verifies current I decision/epoch, exact ContextVersion/Delivery attempt, H authenticated Adapter/session/capability evidence, D fence/lineage and C immutable final-submit evidence. Reconnect reconciles G's durable delivery/ACK journal after fresh authentication and current authority checks.
- Fail closed: payload-only identity, unknown/revoked issuer or Adapter, forged ActorRef, missing Scope/Environment, absent explicit cross-Scope/Environment grant, stale/incomparable epoch, stale/unknown fence, capability mismatch, old-session ACK, changed duplicate digest, or unknown causal order cannot mutate Applied state; reject/quarantine, historical-only or Unknown as applicable.
- Exceptions: G does not define B identity types, I trust/authorization policy, H wire cryptography/serialization, D fence issuance, C submit evidence or Storage atomicity. External governance and runtime conformance remain separate.
- G Applied/reconciliation matrix remains **SPECIFIED / NOT RUN**.

## G Owner exact-version decision — CGH-APPLIED-1.1

- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA: `9808b31f840606b329f1a794935dfc9c5084d63b`
- Common contract: `CGH-APPLIED-1.1`
- Causal profile: `CausalOrderProfile/1.0`
- H schema target: `bmcp.applied-ack/1.1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within G's sole authority over the Full Applied predicate, durable Applied fact/idempotency and historical-versus-current-use projection.

G accepts the 1.1 evidence set as the required causal-order input to its Applied decision: exact G target/context/delivery attempt; C actual provider receipt and immutable CSubmitOutcome; I receipt and terminal proof including revocation cutoff; D intent-bound clearance and lineage/fence cutoff/effective evidence; H integrity-protected transport/schema evidence; B typed references; and a determinate CausalOrderTerminalProof binding the same transaction, digest, reservation and terminal outcome. G will not infer Full Applied from I COMMIT_WON, D clearance, reservation, intent or transport ACK alone.

G's Applied rule for 1.1 is: commit historical Full Applied only after validating the complete predicate and a determinate successful C provider handoff; keep historical fact distinct from current-use eligibility, which is recomputed against current Context head, I authorization/PermissionEpoch, D fence/lineage, scope/environment, session and capability. Later revocation/fence/supersession cannot rewrite a valid historical fact but immediately makes it non-current for protected use. Any unknown order, incomplete lineage, missing/contradictory owner evidence, unknown provider outcome or digest conflict yields no Full promotion and remains suppressed/UNKNOWN.

Exceptions and closure conditions:
1. The coordinator and durable participant/order service are not designated/deployed/verified. G acceptance is conditional on durable, monotonic terminal proof and recovery that cannot clear IN_DOUBT participants.
2. G's validator and Applied persistence implementation have not been shown to consume the complete 1.1 evidence set. This is contract acceptance, not implementation verification.
3. Same transaction/idempotency key plus same digest is idempotent; same identity with changed digest is conflict/quarantine, never last-write-wins. G's durable commit and recovery behavior requires tests.
4. Historical Applied does not authorize current use; current-use projection must fail closed on stale/missing I/D/current-context evidence.
5. G-CO/Applied race and recovery conformance remains SPECIFIED / NOT RUN; no runtime pass is claimed.

This decision applies only to the exact A Blob above and does not transfer the prior 1.0 decision, certify global Forget, or imply implementation/deployment.


## G Owner exact-version reaffirmation — current CGH-APPLIED-1.1 candidate

- A candidate Blob SHA: `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`
- Profile: `CausalOrderProfile/1.0`; H schema: `bmcp.applied-ack/1.1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within G's sole authority over Full Applied, durable Applied idempotency and historical/current-use projection.

G accepts the candidate's complete 1.1 predicate: exact G ContextVersion/Delivery attempt; actual C provider receipt and CSubmitOutcome; I single-use receipt and I sequencer terminal evidence with revocation request cutoff or explicit none; D intent-bound participant clearance, complete lineage, request cutoff and distinct effective position; H integrity-protected 1.1 transport; B typed-reference semantics; and a determinate CausalOrderTerminalProof binding the same transaction, digest, reservation and terminal result. G will not promote Full Applied from I COMMIT_WON, D clearance, intent, reservation or H ACK alone.

G accepts the COC-outage admission safety rule as a mandatory fail-closed precondition: if coordinator ordering or owner cutoff reconciliation is unavailable/unknown, G must not commit a new Full Applied record and must suppress protected current use. G does not infer that no revocation/fence exists from missing coordinator evidence. Historical Applied, once validly committed, remains an immutable historical fact; current-use is separately recomputed against current Context head, I authorization/PermissionEpoch, D fence/lineage, scope/environment, session and capability.

Exceptions: (1) coordinator/operator and durable participant/order service are not designated/deployed/verified; (2) G validator and Applied persistence implementation have not been shown consuming the full 1.1 evidence set; (3) idempotent same-identity/same-digest replay and changed-digest conflict behavior require executable recovery tests; (4) G-CO/Applied race suites remain SPECIFIED / NOT RUN. No implementation or production pass is claimed. This decision applies only to the exact A Blob above and does not transfer the 1.0 decision.

## G exact-version Applied acceptance — CGH-APPLIED-1.1 recovery-batch amendment

- A package Blob: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC Blob: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Profile: `CausalOrderProfile/1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within G's Full Applied predicate, durable Applied fact/idempotency and current-use projection authority.

G accepts the recovery-cutoff batch and pre-batch participant reconciliation as mandatory evidence prerequisites for any new Full Applied promotion. If COC order, owner-local pending gate reconciliation, participant enumeration, I terminal outcome, D complete-lineage barrier or owner high-water proof is missing/unknown, G MUST NOT commit a new Full Applied record and MUST suppress protected current use. G will not infer that no revocation/fence exists from COC outage or missing owner messages. A recovery batch does not itself establish C provider success; exact CSubmitOutcome and determinate CausalOrderTerminalProof remain required.

Historical Applied remains immutable only if it was validly committed under the evidence predicate at that time; current-use is independently recomputed against current I/D/Context/session/capability state.

Exceptions: (1) G validator/Applied persistence implementation has not been shown consuming all recovery-batch evidence; (2) same-identity/digest replay, conflict quarantine and restore behavior require executable tests; (3) G-CO/Applied race suites remain SPECIFIED / NOT RUN; (4) no implementation or production pass is claimed. This decision applies only to the exact A/COC Blob pair above.
