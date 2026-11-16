# Cross-Module Conformance and Fault-Injection Plan — Phase 3

- Status: **TO_VALIDATE / planned test design**. No test has been executed or passed by this document.
- Coordinator: Session A
- Contributors/decision owners: B/C/D/E/F/G/H/I, Storage/Consistency, Testing/QA and Engineering
- Scope: contract conformance and recoverability across Phase 3 interfaces. Not implementation approval, security certification or performance sign-off.

## 1. Evidence and status rules

Allowed result states:
- **NOT_RUN** — no execution evidence.
- **BLOCKED** — cannot execute because a dependency/package/implementation is absent.
- **FAIL** — reproducible counterexample.
- **PASS** — only with a versioned test, executable procedure/code, declared environment, fixture, expected and actual result, logs/artifact reference, and reproducible rerun.
- **TO_VALIDATE** — test design or candidate contract needs owner review.

This plan records tests as NOT_RUN or BLOCKED unless an external execution record is attached. Static document consistency is not runtime conformance.

Every evidence record must include: test ID and version; contract revision/commit; code or procedure revision; environment/runtime/database/index/adapter versions; deterministic fixture and seed; exact command; expected result; actual result; logs/traces/artifact URI; timestamp; reviewer; rerun result. Redact secrets and forgotten payloads.

## 2. Dependencies and test ownership

| Suite | Accountable owner | Required contributors | Dependency / entry condition |
|---|---|---|---|
| TC-01 Domain identity and references | B | D/E/F/G | INT-P0-01 ADR and INT-P1-02 domain semantics |
| TC-02 Scope/identity/permission | I (package absent) | B/C/D/E/F/G/H | Authenticated principal/ActorRef/ScopeRef/permission epoch candidate contract |
| TC-03 Event Accepted/idempotency | E | C/H/I/Storage | INT-P1-03/04; durable payload + receipt + outbox implementation |
| TC-04 Canonical commit/revision/lifecycle | D | B/E/Storage | D-REV-P1-001/002; Claim-dependent tests blocked on ADR |
| TC-05 Typed cursors/watermarks | D (canonical), E (ingress/publication), G (Context), A coordinates | D/E/F/G/Storage | INT-X-01 candidate reviewed by owners; typed token implementation |
| TC-06 Forget/anti-resurrection | I | D/E/F/G/H/Storage | INT-P0-03 + INT-X-02 approved policy and durable fence |
| TC-07 Retrieval freshness/cache | F | D/E/I/G | Scope-before-candidate and index watermark implementation |
| TC-08 Context CAS/reconciliation/delivery | G | D/F/H/C/I | INT-P1-01; H delivery contract |
| TC-09 Applied final-request attestation | H | C/G/I | INT-P1-05; observable final inference boundary and capability negotiation |
| TC-10 Provenance/lifecycle/temporal | B | D/E/F/I | INT-P1-06 and relevant domain semantics |
| TC-11 Adapter/security prompt boundary | C | H/I/Agent runtime | INT-P0-04 threat model and protected-region contract |
| TC-12 Workload/performance | Engineering TBD | D/E/F/G/Storage | All correctness-critical suites; representative workload and hardware declaration |

H/I-dependent suites are BLOCKED until their owners provide formal packages and testable interfaces. This is a dependency status, not a negative assessment of an absent subsystem.

## 3. Test catalogue

### TC-01 — Domain identity and immutable references
- **TC-01-01** Same Memory identity with two immutable versions: exact historical ref resolves to the pinned version; current head can advance without mutating old version.
- **TC-01-02** Cross-scope Memory/Entity/Relation/Evidence references are rejected unless explicit authorized sharing exists.
- **TC-01-03** Claim/ClaimRevision/Fact identity tests remain BLOCKED until INT-P0-01 ADR and INT-P1-02 close.
- **TC-01-04** Entity merge/split preserves old refs and records explicit mappings; no historical ref silently changes target.
- **Expected:** stable opaque IDs, immutable payload, explicit scope checks and historical determinism.
- **Evidence:** D read/write traces, fixture refs, authorization decisions, revision history.

### TC-02 — Scope, identity, permission and revocation
- **TC-02-01** Principal → Producer → Agent → AgentInstance → Session/Task/Environment binding is derived from authenticated transport; payload-supplied identity mismatch is rejected.
- **TC-02-02** Same query under two principals/scopes returns no cross-scope candidates, counts, scores or existence leaks.
- **TC-02-03** ANN, lexical, structured, temporal, graph and provenance candidate backends enforce scope before candidate IDs are emitted.
- **TC-02-04** Graph edge and target node are independently authorized.
- **TC-02-05** Permission revoked after retrieval but before serialization/delivery blocks disclosure.
- **TC-02-06** Cache hit under old permission epoch is suppressed; missing policy authority fails closed.
- **Expected:** no unauthorized object becomes observable at any boundary.
- **Evidence:** backend query plans/filters, policy decision IDs/epochs, redacted traces and negative assertions.

### TC-03 — Accepted receipt, idempotency and durable ingress
- **TC-03-01** Same authenticated producer/scope/key + same canonical payload digest, sequential and concurrent: one EventID/ReceiptID and stable receipt.
- **TC-03-02** Same idempotency identity + different digest: explicit conflict; original Event remains unchanged.
- **TC-03-03** Crash before durable transaction commit: no Accepted receipt visible.
- **TC-03-04** Crash after commit before response: retry/status lookup returns original receipt and EventID.
- **TC-03-05** Crash after response before dispatch: outbox recovery dispatches compile intent exactly-once-effect (at-least-once delivery allowed).
- **TC-03-06** Payload staged but payload integrity/durability fails: no Accepted.
- **TC-03-07** Permission/Forget changes while queued or DLQ replay: worker reauthorizes and suppresses forbidden work.
- **Expected:** Accepted means durable Event + payload reference + idempotency receipt + recoverable processing intent, not Compiled.
- **Evidence:** transaction/WAL logs, receipts, outbox offsets, crash injection script and replay trace.

### TC-04 — Canonical commit, aggregate revision and lifecycle
- **TC-04-01** Two concurrent commits against one expected aggregate head: one succeeds; the other receives stale-parent conflict/reconciliation.
- **TC-04-02** Crash before canonical commit: no visible version/cursor; crash after commit before response: retry returns original commit receipt/cursor.
- **TC-04-03** CanonicalCommitCursor and AggregateRevision cannot be interchanged by API/type system.
- **TC-04-04** LifecycleEvent append and canonical state/projection recovery are atomic or recoverably consistent; deterministic fold yields same state.
- **TC-04-05** Lifecycle transition with stale expected state/sequence is rejected; no mutable projection writes bypass LifecycleEvent.
- **TC-04-06** Claim/Fact lifecycle and ConflictSet tests remain BLOCKED pending ADR.
- **Expected:** immutable versions, one aggregate head, append-only lifecycle authority, recoverable publication intent.
- **Evidence:** transaction records, commit receipts, cursor values, event log and fold comparison.

### TC-05 — Typed cursor and watermark interop
- **TC-05-01** Type/namespace/partition mismatch is rejected; no raw integer comparison across cursor families.
- **TC-05-02** Resume token is exclusive, partition-bound and epoch-bound; at-least-once replay deduplicates by immutable source ID.
- **TC-05-03** Source producer sequence gap/reorder does not masquerade as missing Brain Event cursor.
- **TC-05-04** Index receives offset N+1 before N: contiguous publication watermark remains below N until N is applied or durably dispositioned.
- **TC-05-05** Watermark vector over two partitions cannot be collapsed to max(offset); required fence checks every partition.
- **TC-05-06** Schema rebuild uses a new index generation and explicit checkpoint; old-generation watermark is not accepted as current.
- **TC-05-07** LifecycleEvent cursor and canonical commit cursor are separately resumable and correlated by immutable refs.
- **TC-05-08** Cursor retention expiry returns explicit gap/expired status; consumer cannot report complete catch-up.
- **Expected:** monotonicity only within declared namespace/partition/epoch; gap and replay behavior is deterministic.
- **Evidence:** event fixtures, partition logs, consumer offsets, deliberate reorder/crash, token rejection traces.

### TC-06 — Forget fence and anti-resurrection
- **TC-06-01** Forget fence installed during concurrent compiler execution blocks commit/publication of any stale-fence derivative.
- **TC-06-02** Forget between Event acceptance and compile start suppresses or quarantines worker; DLQ/replay/recompile cannot recreate visible derivatives.
- **TC-06-03** Forget during index rebuild prevents forgotten object reappearing in ANN/lexical/graph/temporal results.
- **TC-06-04** Forget during cache fill/query blocks both cache write and result serialization; lost invalidation event is repaired by epoch check.
- **TC-06-05** Forget during Context mutation/delivery blocks stale ChangeSet/Delta/Snapshot and Full Applied.
- **TC-06-06** Late Applied acknowledgement for a superseded/forgotten delivery is retained only as historical evidence and cannot reactivate target.
- **TC-06-07** Offline Adapter reconnect authenticates, refreshes policy/Forget epochs, discards stale cache and applies safe clear/replacement before reuse.
- **TC-06-08** Backup restore and external-provider boundaries are tested only against I-approved policy; unknown targets remain explicit exceptions.
- **Expected:** suppression barrier precedes asynchronous cleanup; no resurrection; global completion never inferred from local clear alone.
- **Evidence:** fence epochs, producer registrations, barrier snapshot, per-target receipts, index/cache/context/adapter traces, residual exception report.
- **Status:** BLOCKED pending INT-P0-03 and H/I-owned contracts.

### TC-07 — Retrieval freshness and cache
- **TC-07-01** Scope predicate is applied before candidate materialization in each retrieval backend.
- **TC-07-02** Canonical commit newer than index watermark: bounded canonical read-through/wait or explicit partial/stale result; never false complete.
- **TC-07-03** Rebuild/replay excludes forgotten/retracted/retention-ineligible objects under current canonical authority.
- **TC-07-04** Cache key partition includes principal, normalized scopes, environment, permission epoch, Forget epoch, retrieval config and relevant watermark/fence.
- **TC-07-05** Cache hit revalidates authorization, canonical version/lifecycle and Forget fence immediately before disclosure.
- **TC-07-06** Channel timeout/cancellation/index outage cannot fabricate empty-complete or stale protected result.
- **Expected:** index/cache are projections only; freshness/completeness is explicit.
- **Evidence:** backend traces, watermark vectors, canonical reads, cache key test matrix and fault logs.

### TC-08 — Context version, ChangeSet, reconciliation and delivery
- **TC-08-01** Two ChangeSets with same BaseVersion race: one commit; other conflicts/replans.
- **TC-08-02** Duplicate ChangeSet/idempotency key returns original result; changed payload conflicts.
- **TC-08-03** Delta base mismatch rejects and requests full Snapshot; Delta application is atomic.
- **TC-08-04** Failed multi-operation ChangeSet leaves no partial target ContextVersion.
- **TC-08-05** Timeout leaves Delivery Unknown; lookup by DeliveryID resolves state; late ack cannot roll desired head backward.
- **TC-08-06** Forget/revocation before delivery/application blocks stale target; offline reconnect forces reauthorization and reconciliation.
- **Expected:** ContextVersion/Delivery/Applied separate; G remains sole Context authority.
- **Evidence:** CAS histories, ChangeSet audit, Delivery state transitions, Adapter acknowledgements and reconciliation run.

### TC-09 — Applied final-request proof
- **TC-09-01** Adapter internal buffer says applied but final inference request omits managed region: Full Applied rejected.
- **TC-09-02** Partial managed-region coverage reports Partial, never Full.
- **TC-09-03** Exact ContextVersion/DeliveryID/session/InferenceRequestID/capability epoch/boundary correlation required.
- **TC-09-04** Adapter capability/config change invalidates old epoch for new request proofs.
- **TC-09-05** No final boundary observability or missing request ID => Unknown/lower tier.
- **TC-09-06** Applied acknowledgement does not assert model attention, comprehension or behavioral use.
- **Expected:** Full Applied is protocol-level proof at actual inference submission boundary only.
- **Evidence:** request assembly trace or privacy-safe boundary attestation, normalized region digest, IDs, capability negotiation and proof verifier output.
- **Status:** BLOCKED pending H/C contract and testable adapter.

### TC-10 — Provenance, Lifecycle and temporal semantics
- **TC-10-01** Provenance traversal preserves source and derivation IDs; cycle behavior follows B-approved DAG/restricted-cycle policy.
- **TC-10-02** Unknown/unavailable source is explicit and not fabricated as provenance.
- **TC-10-03** Event time, recorded time, commit time and valid time remain separate under clock skew.
- **TC-10-04** Forget dependency traversal covers registered descendants and records late derivatives.
- **TC-10-05** Evidence authorization is independent from Memory authorization.
- **Expected:** deterministic lineage, explicit uncertainty, non-reconstructive audit under Forget.
- **Evidence:** lineage fixtures, graph traversal logs, temporal query results, authorization decisions.

### TC-11 — Adapter and prompt/security boundary
- **TC-11-01** Memory payload containing fake system/developer tags remains data and cannot alter protected instruction region.
- **TC-11-02** Agent tool authorization is unchanged by Memory content or Adapter capability.
- **TC-11-03** Adversarial multi-turn indirect prompt injection is recorded as residual risk and evaluated with declared model/agent version.
- **TC-11-04** Scope-confused and forgotten memory cannot be delivered after revocation/fence.
- **Expected:** no instruction authority or tool privilege is conferred by memory; residual model influence is not claimed eliminated.
- **Evidence:** adversarial fixtures, final request assembly, policy decision logs, red-team report.
- **Status:** BLOCKED pending I threat model and H/C adapter boundary.

### TC-12 — Performance and resource validation
- **TC-12-01** Establish representative workload and dataset size/shape.
- **TC-12-02** Record hardware, CPU, RAM, GPU/VRAM, storage, network, software/compiler/index/model versions and concurrency.
- **TC-12-03** Measure latency distributions, throughput, recall/quality, index lag, memory consumption, recovery/rebuild and cost with correctness checks enabled.
- **TC-12-04** Repeat with warm/cold caches, contention, scope partitions, forget/revocation and degraded channels.
- **Expected:** publish only measured values with methodology and uncertainty; no architecture-level multiplier promise.
- **Evidence:** raw benchmark data, scripts, machine-readable config, repetitions and review.
- **Status:** BLOCKED until stable candidates and correctness suites are available.

## 4. Cross-cutting failure-injection matrix

| Fault window | Injected condition | Required invariant / expected result |
|---|---|---|
| Ingress pre-commit | process/database crash | No Accepted receipt; producer can retry |
| Ingress post-commit/pre-response | response lost | Same receipt/EventID returned |
| Outbox post-commit/pre-dispatch | dispatcher crash | Work reconstructed from durable outbox |
| Compiler in-flight | Forget fence advances | stale worker cannot commit/publish derivative |
| Canonical commit | concurrent aggregate update | CAS admits one head; conflict explicit |
| Projection | out-of-order source events | contiguous watermark does not jump gap |
| Retrieval | permission revoke mid-flight | final serialization blocked |
| Cache fill | Forget/revocation during fill | no stale cache write or disclosure |
| Context update | concurrent ChangeSets | one base wins; no partial version |
| Delivery | timeout / late ack | Unknown until query; late ack historical only |
| Adapter offline | reconnect with stale local snapshot | authenticate, refresh fence, clear/reconcile before reuse |
| Restore | old backup reintroduced | current Forget policy/fence re-applied before visibility |

## 5. Test execution ledger (initial state)

All tests below are **NOT_RUN** at creation. No execution artifacts were supplied in the reviewed design branches.

| Test family | Initial state | Blocker |
|---|---|---|
| TC-01 domain identity | NOT_RUN | Claim-dependent cases ADR-BLOCKED |
| TC-02 scope/identity | BLOCKED | I/H contract and implementation absent |
| TC-03 Accepted/idempotency | NOT_RUN | Candidate E contract; implementation evidence absent |
| TC-04 canonical/lifecycle | NOT_RUN | D-REV-P1-002 open; implementation evidence absent |
| TC-05 typed cursor/watermark | NOT_RUN | This proposal requires D/E/F/G/Storage approval |
| TC-06 Forget/anti-resurrection | BLOCKED | I policy/H Adapter package absent; D-REV-P1-003 open |
| TC-07 retrieval/cache | NOT_RUN | implementation/backend traces absent |
| TC-08 Context/delivery | NOT_RUN | H delivery package absent |
| TC-09 Applied proof | BLOCKED | H/C final boundary contract and Adapter implementation absent |
| TC-10 provenance/time | NOT_RUN | B final semantics/implementation evidence absent |
| TC-11 security/prompt boundary | BLOCKED | I threat model and H/C proof surface absent |
| TC-12 performance | BLOCKED | no declared representative workload or reproducible measurements |

## 6. Release-gate recommendations

1. Do not freeze canonical, wire or security contracts from this test plan.
2. Close INT-P0-01 ADR and INT-P0-02/03/04 governance ownership before security-sensitive implementation sign-off.
3. Require D/E/F/G owner review of every typed cursor row; D-REV-P1-002 remains a hard dependency for canonical cursor.
4. Require H/I formal design packages before Applied, global Forget, authorization, backup or external-erasure tests can be complete.
5. Keep design review, branch delivery, main integration, implementation conformance and performance sign-off as separate gates.
6. A missing test artifact is NOT_RUN/BLOCKED, never PASS by implication.

## 7. Known limits

This is a static conformance plan over design documents and named branch baselines. It does not audit Rust code, execute databases, inspect real adapters, certify security, prove physical erasure, or measure performance. Those claims require later implementation-level evidence.
