# Phase 3.5 — Forget Atomicity Storage Realization Review

**Owner:** Session Storage/Consistency — Storage & Consistency Architect  
**Review date:** 2026-11-16  
**Status:** DESIGN REVIEW / PROPOSED REALIZATION  
**Implementation status:** NOT IMPLEMENTED / NOT VERIFIED

## 0. Scope, source baseline and authority

Repository inspection at the start of this workflow found no pre-existing Storage/Consistency owner package, Storage-owned module directory, storage implementation or fault-injection suite. This branch now contains the first Storage/Consistency proposed realization report (this document); it is a review artifact, not an established module authority or implementation. The package is not present on main and has not been owner-approved or merged.

Reviewed source artifacts:

| Artifact | Branch | Branch HEAD | Path |
|---|---|---|---|
| Cross-module contract review | main | 8a6414158c9c056c1638222534e1993d1bbc99d2 (reviewed source commit) | reviews/integration/phase-3-defghi-cross-module-contract-review.md |
| D Forget operation + fence contract | session-d-memory-brain-2026-11-16 | da8e5882d0b238d765d00b2225b79eea45a483b1 | 03-memory-brain/forget-fence-operation-and-publication-gate.md; 03-memory-brain/forget-fence-and-completion-contract.md |
| D cursor semantics | session-d-memory-brain-2026-11-16 | da8e5882d0b238d765d00b2225b79eea45a483b1 | 03-memory-brain/commit-cursor-semantics.md |
| E producer admission | session-e-memory-compiler-2026-11-16 | 13a720724fcfae84f4c4abe36fbc44dd2820445d | 04-memory-compiler/compiler-state-and-producer-admission.md |
| E derived registration | session-e-memory-compiler-2026-11-16 | 13a720724fcfae84f4c4abe36fbc44dd2820445d | 04-memory-compiler/forget-fence-and-derived-registration.md |
| I Global Forget inventory | session-i-security-governance-2026-11-16 | 5591ad3620ec3f5d74194bd79556dcf3e25bea07 | 09-security-governance/global-forget-target-inventory-and-completion-evidence.md |
| Storage proposed realization | session-storage-consistency-forget-atomicity-2026-11-16 | ec0e29d9b6e6e32728116514376214503aeb2434 (pre-update HEAD) | reviews/storage-consistency/forget-atomicity-storage-realization-review.md |

Fetched source blob SHAs:
- D Forget operation + publication gate: 2c5b1358ff58f99af838b741a75966ccd07ad088
- D Forget completion contract: cce2108899525c9ce6808716224641baa11faf4f
- D cursor semantics: 4688a0ca487bf4d853c7f0220408abe8d743d159
- E producer admission: 07b3d47dcb12fa94c2d449160905ba9731ee2ccd
- E derived registration: 81841c5f29f0d21c5acdb5fe8a392ff560808919
- I Global Forget inventory: 9100061fa986fb6676656169de3fcf9fc1c72664

Authority is unchanged:
- D owns ForgetOperation, ForgetFence, canonical producer-registration/barrier semantics, dependency inventory authority and CanonicalCommitCursor.
- E owns compiler work/attempt/stage lifecycle, retries, derived lineage and producer enforcement.
- I owns authorization/PermissionEpoch, global producer-domain inventory, retention, backup/external-copy policy and global completion.
- Storage owns only persistence, transaction, locking/CAS, visibility and recovery realization.
- This report does not change domain meanings, invent a D API or authorize I policy.

The cross-module review marks CR-P1-01 / INT-P0-03 / Forget barrier enforcement OPEN. D semantics are specified; D/E/Storage atomic registration/publication and implementation evidence remain open. E explicitly describes its operation names as requirements, not existing callable APIs.

## 1. Executive decision

### 1.1 Recommended realization

Use a **single transactional coordination authority per Canonical Memory authority**, with:
1. A coordinator record serializing Producer Work Registration, Fence Installation, Dependency Registration and Publication Gate decisions.
2. A durable Producer Work Ledger with stable work identity, monotonic registration sequence, source lineage, admission receipt, attempts/leases and terminal disposition.
3. A durable Forget Fence record with D-owned generation, target-set digest and captured producer-registration high-water.
4. A durable Derived Artifact / Dependency Ledger with complete lineage and idempotent registration keys.
5. A Publication Ledger and authoritative visibility pointer/state.
6. A transactional Outbox for asynchronous propagation and replay.

Preferred deployment: one transactional database for the coordinator, ledgers, publication state, visibility pointer and outbox. Large artifact bytes may live in blob/object storage, but must remain private until the database commits the authoritative visibility pointer. No consumer may bypass that pointer.

**Core invariant:** every derivative-capable Work W covered by fence F is either (a) durably registered with registration_sequence <= F.barrier_high_water and remains barrier-open until terminal disposition, or (b) durably rejected/quarantined by the admission transaction with no execution/publication capability. There is no third state in which W is outside the barrier but can publish.

Barrier capture makes pre-fence work accountable; it does not grant publication permission. Every final publication must recheck the current fence.

### 1.2 Rejected shortcuts

- A local E fence read followed by an independent write is unsafe.
- Queue insertion is not D registration.
- An outbox alone does not serialize admission against fence installation.
- Lease expiry, worker disappearance or DLQ parking is not terminal disposition.
- A D gate message followed by an unrelated Storage visibility write is unsafe unless a single-use token is atomically consumed against the current fence at the visibility commit and uncertainty keeps the artifact hidden.

## 2. Logical persistence model

These are Storage concepts, not frozen D/E schemas or APIs.

| Record | Minimum durable fields | Purpose |
|---|---|---|
| AuthorityCoordinator | brain_authority_id, coordination_version, next_registration_sequence, current_fence_generation/ref | One serialization point |
| ProducerWork | work_id, producer_class, authenticated producer binding ref, source refs/revisions, lineage digest, ScopeRefs, admission cursor, observed fence, registration_sequence, request digest, state | Admission and barrier membership |
| WorkAttempt | work_id, attempt_id, lease_id, monotonic lease_epoch, owner, expiry, observed fence/permission refs, state | Recoverable worker ownership |
| ForgetFence | operation_id, generation, target_set_digest, target/lineage inventory ref, barrier_high_water, install commit cursor, state | Fence and immutable barrier snapshot |
| DerivedArtifact | artifact_ref/version, work_id, run_id, private stage locator, payload digest, visibility_state, lineage_digest | Staged derivative |
| DependencyEdge | registration_id, artifact_ref/version, source_ref/version, lineage digest, scope binding, request digest, registration position | Complete dependency inventory |
| Publication | publication_operation_id, artifact/version, work/attempt IDs, dependency receipt digest, checked fence generation, permission decision ref/epoch, state, receipt | Idempotent visibility decision |
| WorkTerminal | work_id, terminal disposition, evidence digest, outputs accounted, final attempt, D receipt | Barrier completion |
| Outbox | event_id, aggregate key, event type, payload ref/digest, source cursor, delivery state | At-least-once propagation |

Stable IDs are opaque and non-recycled. Same idempotency key + same request digest returns the original receipt; same key + different digest conflicts. Registration sequence is not a timestamp, CanonicalCommitCursor, ForgetFenceGeneration or PermissionEpoch. D's CanonicalCommitCursor remains one globally ordered sequence per Brain authority. Fence generation remains a separate D-owned namespace.

Staged artifacts are private by default. Visibility is a durable DB state/pointer, not an in-memory cache flag or object-store naming convention.

## 3. S1 — Atomicity plan

### 3.1 Producer Work Registration

**Transaction:** AuthorityCoordinator + ProducerWork + registration receipt/outbox in one transaction.

1. Lock or conditionally update the authority coordinator.
2. Resolve idempotency by stable work_id and request digest.
3. Validate producer class and source lineage/scope against D/I-owned authority.
4. Evaluate the latest applicable fence while holding the same serialization boundary as Fence Installation.
5. If allowed, allocate the next registration sequence and insert ProducerWork + durable receipt.
6. If blocked, persist a rejected/quarantined disposition with no executable lease/queue capability.
7. Commit. E may enqueue/lease/execute only after the accepted receipt is established.

**Linearization point:** commit of the transaction that checks the current fence and inserts the accepted registration under the shared coordinator.

**Recovery:** query/retry the same work_id + digest. If ACK outcome is unknown, no queue/lease/run is allowed until resolved. No second logical registration is created.

### 3.2 Fence Installation

**Transaction:** the same AuthorityCoordinator serialization namespace, plus ForgetFence, operation state, barrier snapshot and outbox.

1. Lock/conditionally update coordinator.
2. Resolve ForgetOperation idempotency and target-set digest.
3. Allocate the next D-owned fence generation.
4. Capture barrier_high_water = last committed registration sequence in this same transaction.
5. Persist generation, target digest/lineage scope, high-water, installation CanonicalCommitCursor reference, operation state and outbox intent.
6. Commit. Later admission checks see the installed fence.

**Linearization point:** commit of Fence Installation while holding the same serialization point as Producer Work Registration.

**Recovery:** ForgetOperationId + normalized request digest returns the same generation and same high-water after ACK loss. A retry must not recapture a later high-water.

### 3.3 Barrier High-Water Capture

This is not a later queue scan. It is part of the Fence Installation transaction.

Persist barrier_high_water, producer registry version/reference, target inventory snapshot/digest reference and fence installation cursor/reference. Every accepted ProducerWork with registration_sequence <= barrier_high_water is included. Unknown producer classes or registry gaps remain independent hard stops; the sequence does not prove global producer inventory completeness.

**Linearization point:** same commit as Fence Installation.

### 3.4 Dependency Registration

**Transaction:** AuthorityCoordinator + DerivedArtifact/DependencyEdge ledger + receipt/outbox. Insert the complete required dependency set atomically, or persist an explicitly incomplete group that is never publishable.

1. Resolve DependencyRegistrationId and digest.
2. Confirm ProducerWork exists and is not terminal; verify exact source revisions.
3. Under the shared fence coordinator, evaluate every source ancestor and artifact target against the latest applicable fence.
4. Insert immutable artifact identity and complete direct/transitive dependency set.
5. Commit a complete receipt only when the required set is durable.

**Linearization point:** commit of complete dependency registration under the shared fence serialization boundary.

If a fence installs while pre-fence work is still running, later dependency registration for a covered lineage must be rejected/quarantined. Work remains barrier-open until terminal disposition. Late discovery after a prior proof reopens reconciliation as D/I require.

### 3.5 Derived Publication

**Transaction:** one atomic transaction must:
- resolve PublicationOperationId idempotency/digest;
- verify work/attempt/lease is current and not terminal;
- verify all dependency receipts are complete and bound to this artifact/work;
- verify current fence and source lineage under the same coordinator as Fence Installation;
- validate current authorization evidence under the agreed I contract;
- persist Publication success receipt;
- flip authoritative visibility from PRIVATE_STAGED to VISIBLE;
- append outbox event.

**Linearization point:** commit of this transaction. Before commit, every reader sees PRIVATE_STAGED/absent. After commit, readers may see VISIBLE only through the authoritative visibility gate and current fence enforcement.

Upload bytes to private/quarantine object storage first. No public bucket, direct object enumeration, shared signed URL or alternate consumer path may expose staged bytes. If D and Storage are separate physical services, their shared linearization mechanism remains OPEN until proven. A gate-accepted message followed by an independent write is not sufficient.

### 3.6 Work Terminal Disposition

**Transaction:** ProducerWork + WorkAttempt + WorkTerminal + barrier state + outbox.

Verify final lease epoch; all outputs are either published with durable receipts or suppressed/quarantined and incapable of later publication; all dependency/publication operations are resolved; no ambiguous gate remains. Persist immutable terminal disposition and D-visible receipt, then close the barrier item exactly once.

**Linearization point:** commit of terminal receipt and work-state transition.

Lease expiry only invalidates an attempt. It does not close the logical work item. A resumed worker with an old lease epoch must fail dependency, publication and terminal updates.

## 4. S2 — Registration/Fence concurrency proof

Both admission and fence installation must serialize on the same per-authority coordinator. The critical section includes reading the current fence, allocating the registration sequence or fence generation, writing the corresponding ledger rows and committing. Process-local mutexes, queue ordering, eventual replicas and independent check-then-write calls do not qualify.

Let W be a work item whose lineage is covered by F; r(W) is its committed registration sequence and H(F) is the captured high-water.

**Order A — registration first**
1. W acquires coordinator serialization while no applicable fence exists.
2. W is accepted with sequence n and the registration transaction commits.
3. F obtains coordinator serialization and captures H >= n.
4. Thus r(W) <= H(F): W is captured and remains barrier-open.
5. Any later dependency registration/publication rechecks the now-current fence. Covered output is rejected/quarantined; W cannot publish after F.

**Order B — fence first**
1. F acquires coordinator serialization, persists its generation/target scope and captures H, then commits.
2. W obtains coordinator serialization afterward.
3. W evaluates the latest fence and is rejected/quarantined; no accepted registration, lease or execution capability is granted.

These are the only serialized orders. There is no path where F captures H before W allocates a sequence but W still commits admission based on an earlier fence, because both operations require the same serialization point.

**Publication race:** publication and fence installation use that same coordinator. If publication commits first, the derivative and dependency record are durable before F and must be included in the inventory/reconciliation. If F commits first, publication sees F and rejects. Barrier capture alone is not a publication authorization.

## 5. S3 — Crash recovery

| Failure | Durable state | Recovery | Safety result |
|---|---|---|---|
| Before registration commit | No accepted receipt | Retry/query same work_id + digest | No execution until resolved |
| Registration commit, ACK lost | Work + receipt durable | Query same ID; replay outbox | One registration; barrier-visible |
| Registration ACK, before queue | D work open; E queue absent | Reconciler enqueues same work idempotently | No lost work |
| Fence transaction before commit | Transaction absent/rolled back | Retry same ForgetOperationId | No partial fence/H |
| Fence commit, ACK lost | Fence + H + outbox durable | Query same operation | Same generation/H; no recapture |
| Lease expiry | Work remains open | Invalidate lease epoch; new attempt after fresh checks | Expiry is not terminal |
| Worker restart | Work and attempt history durable | Recover same work ID, new attempt, recheck auth/fence | Stale output cannot publish |
| Dual Worker retry | Competing attempts | Conditional lease claim + monotonic lease_epoch | Duplicate compute possible; one valid gate |
| Outbox replay | Duplicate/out-of-order events | Deduplicate by event_id/operation ID; contiguous cursors only | At-least-once, no duplicate effect |
| Dependency ACK lost | Edges may already exist | Lookup stable DependencyRegistrationId + digest | Same receipt; artifact private |
| Crash after dependency, before Publish | Dependencies durable; artifact private | Recheck current fence/auth; resume same PUB key or suppress | No implicit visibility |
| Publish commit, ACK lost | Receipt + VISIBLE pointer durable | Query same PublicationOperationId | One logical publication |
| Crash before Publish commit | No receipt/visibility flip | Retry same key after fresh checks | Artifact hidden |
| Fence advances concurrent with Publish | Both serialize | Whichever commits first determines order | No stale-fence publish |
| Visibility commit, outbox not delivered | Visibility + outbox durable | Replay outbox | Source visibility authoritative |
| Terminal transaction interrupted | All-or-nothing | Query terminal receipt; retry same digest | Work open or terminal, never half-closed |
| Restore stale snapshot | Old data/fence may be restored | Quarantine; replay independent current Forget ledger before serving | No stale derivative served |

A lease must have a monotonic fencing epoch or equivalent conditional update. A worker resuming after lease replacement cannot commit using an old epoch.

## 6. S4 — Persistence and consistency choices

| Option | Preconditions | Benefits | Costs/failure modes | Decision |
|---|---|---|---|---|
| Single DB transaction + coordinator row lock | One DB transacts over coordinator, work, fence, dependency, visibility and outbox | Simplest proof; one commit point; recoverable idempotency | Per-authority contention; DB availability/latency; isolation/locking must be verified | **Recommended baseline** |
| CAS/conditional update | Durable linearizable CAS; dependent writes atomic or rigorously guarded | Explicit versions; can reduce lock contention | CAS alone does not atomically commit ledgers/visibility; retry and ABA risks | Accept only with atomic dependent writes |
| Transactional Outbox | Outbox shares transaction with source state | Reliable replay and notification | Does not serialize admission/fence or make remote visibility atomic | Required supplement, not gate |
| Durable Work Ledger | Durable sequence and terminal receipts | Work cannot disappear with queue/lease; supports barrier reconciliation | Growth, retention, compaction and indexing | Required |
| Distributed transaction / 2PC | Participants support durable prepare, coordinator recovery and atomic commit | Can span storage systems | In-doubt/blocking states and operational complexity | Possible, not preferred |
| D gate + Storage token | Single-use token bound to artifact, digest, work and fence; Storage atomically checks current fence at visibility commit | Could separate services | Stale token/revocation race unless same current fence is enforced at Storage commit | OPEN; not accepted without proof |
| Eventual consistency / async reconciliation | No shared linearizable boundary | Loose coupling/availability | Allows stale admission/publication window; cannot undo exposure | Rejected for safety gate |

### 6.1 Database capabilities to verify (not assumed present)

The selected engine/configuration must demonstrate:
1. Atomic durable transactions across coordinator, ledgers, visibility state and outbox.
2. A serialization mechanism ordering registration, fence installation, dependency registration and publication.
3. Unique/idempotency constraints on operation IDs and request digests.
4. Query by idempotency key after timeout/unknown commit.
5. Read-after-commit consistency for fence and publication state.
6. Conditional updates/lease epochs preventing stale owners from committing.
7. Atomic visibility pointer transition; no partial multi-row state visible.
8. Transactional outbox or equivalent.
9. Restore procedures that cannot roll back the independent current Forget control ledger.
10. Documented isolation, failover, replication and acknowledged-write durability.

**Verification:** inspect exact engine/version docs and deployed configuration; run two-client concurrent tests; force primary failover around commit/ACK; verify reads after failover; test duplicate keys and rollback; inspect lock/predicate behavior; inject crashes at every transition. A vendor feature name or local unit test alone is insufficient.

### 6.2 Performance

The coordinator serializes critical operations. Scope it per Brain authority, keep transactions short, and never hold locks during extraction, blob upload or network calls. Do expensive work in private staging before the final gate. Partition telemetry/outbox delivery, not the safety-critical ordering without a proof-preserving design. Measure lock wait, retry rate, admission latency, fence latency, publication latency, barrier age and unresolved work. If sharding is needed, define independent fence domains explicitly; do not silently partition D's global per-authority CanonicalCommitCursor.

## 7. S5 — Executable conformance plan (NOT RUN)

### 7.1 Common fixture

One Brain authority A; source Memory M and lineage L; registered/authenticated producer P; stable work W with source revision, ScopeRef and digest; fence F targeting M/L; private artifact X; dependency registration DREG(X); publication operation PUB(X); two independent clients/workers; deterministic latches/crash hooks; authoritative read API that returns only VISIBLE artifacts and rechecks the fence; audit query exposing IDs, registration sequence, H, generation, dependency/publication receipts, lease epoch and terminal disposition without forgotten plaintext.

### 7.2 Test matrix

| ID / class | Fixture and operation order | Expected result | Observable evidence |
|---|---|---|---|
| C01 Thread race: registration first | Commit W registration; then install F | W sequence <= F.H; W remains barrier-open | Registration receipt, sequence, H, barrier query |
| C02 Thread race: fence first | Commit F; then register W | W rejected/quarantined; no lease/execution | Fence generation/H, rejection receipt, no accepted work |
| C03 Stress race | N workers repeatedly race work admissions against F | Every W captured or rejected; zero uncovered publish | Race seed, ledger export, invariant checker, DB traces |
| C04 Dependency vs fence | Stage X; race DREG(X) with F | If DREG first, inventory + barrier capture; if F first, DREG rejected; X private | Dependency receipt/order, H, visibility state |
| C05 Publish vs fence | Complete DREG; race PUB(X) with F | Publish-first is inventoried; fence-first rejects; no stale publish | Publication receipt, generation, commit order, reader result |
| C06 Crash before registration commit | Kill process before commit | No accepted receipt; retry resolves one outcome | DB state, request digest, retry result |
| C07 Crash after registration commit | Commit then kill caller before ACK | Same receipt returned; one work row | Unique work row, receipt ID, recovery log |
| C08 Crash after fence commit | Commit then drop ACK | Same generation and H returned | Fence row, idempotency record |
| C09 ACK loss | Drop ACK after registration, DREG and Publish commits | Lookup returns original receipts; no duplicate effect | Receipt IDs/digests, unique row counts |
| C10 Lease expiry | Pause worker past expiry; replacement claims; old worker resumes | Old lease cannot publish/terminalize; barrier remains open until valid terminal | Lease epochs, rejected stale write |
| C11 Worker restart | Kill at each compiler stage; restart | Same work ID, new attempt, fresh checks, no duplicate visibility | Attempt chain, state transitions |
| C12 Dual Worker retry | Two workers race lease claim and same PUB key | At most one current lease and one logical publication | Conditional update, unique PUB row, visibility pointer |
| C13 Outbox replay | Replay duplicate/out-of-order event deliveries | Consumer effects idempotent; no cursor gap skipped | Event IDs, dedup rows, contiguous cursor |
| C14 DREG/Publish crash gap | Commit DREG; crash before PUB; restart | X remains private until same PUB key commits after fresh checks | DREG receipt, no visibility before replay |
| C15 Stale fence | Cache old generation; install newer F; attempt admission/DREG/PUB with stale observation | Authoritative transaction rejects | Old/new generation, rejection, no visibility |
| C16 Late derivative | After proof, inject unregistered derivative from forgotten lineage | Suppress/quarantine; proof reopened/invalidated; audit defect | Lineage, proof supersession, read denial |
| C17 Duplicate operation | Repeat Forget/work/DREG/PUB IDs with same then altered digest | Same digest returns original receipt; changed digest conflicts | Idempotency rows, receipt IDs, conflict audit |
| C18 Barrier terminality | Expire lease, delete queue, park DLQ, attempt barrier close | Barrier stays open until explicit terminal receipt | Open work query, DLQ/lease history, no terminal receipt |
| C19 Atomic visibility | Crash around visibility/outbox commit | Reader sees private/absent or fully visible with receipts; never partial | Reader snapshots, transaction logs, receipt rows |
| C20 Restore stale snapshot | Restore old work/artifact snapshot while current Forget ledger is newer | Quarantine until current control ledger replay and reconciliation | Restore state, replay cursor, denial evidence |

**Acceptance criteria:** no covered work is neither captured nor rejected; no artifact is visible without complete dependencies and committed publication receipt; stale fence/lease cannot pass; ACK loss resolves to original result; expiry/DLQ/queue deletion cannot close a barrier; late derivative reopens proof; actual engine failover/crash tests verify durability and serialization. These are acceptance criteria, not results.

## 8. OPEN decisions for D/E/I

| ID | Question | Proposed default | Owners |
|---|---|---|---|
| O-01 | Exact shared serialization authority for registration and fence installation? | D-owned per-Brain coordinator realized by one transaction/linearizable register | D + Storage |
| O-02 | Scope of producer registration sequence? | Per-authority sequence for barrier only; distinct from CanonicalCommitCursor | D |
| O-03 | EventRef-only ingress before canonical MemoryRef exists? | Register immutable EventRef + lineage token/digest; bind canonical refs later without losing original barrier identity | D + E + B |
| O-04 | Logical work registration across retry/recompile? | Stable parent work identity; child work only if linked and independently barrier-accounted before execution | D + E |
| O-05 | Complete dependency set atomic or prepare/finalize group? | Prefer atomic complete set; incomplete group never publishable | D + E + Storage |
| O-06 | Does D gate own visibility transaction or issue a token? | Prefer one transaction owner; token only with same-current-fence CAS at visibility commit | D + E + Storage |
| O-07 | How is current I PermissionEpoch/authorization validated at publication? | I-authoritative verifiable decision with explicit freshness/revocation semantics; fail closed if stale/unknown | I + D + E |
| O-08 | Terminal disposition with multiple outputs/publication attempts? | Close only when all outputs accounted and no attempt can publish later | D + E |
| O-09 | Link I ProducerDomainInventoryEpoch to D work barrier? | Preserve two distinct epochs; reconcile inventory completeness before global proof | I + D |
| O-10 | Transitive lineage and scope for EventRef-only/derivative-of-derivative? | Immutable lineage digest + typed refs; payload IDs never confer authority | B + D + E + I |
| O-11 | Restore protocol preventing Forget control-ledger rollback? | Independent monotonic control ledger or authoritative replay before serving | D + I + Storage |
| O-12 | Which DB isolation/replication/failover guarantees does selected engine support? | Verify exact engine/config; no vendor assumption | Storage |

These questions do not authorize Storage to rewrite D/E/I contracts. Any semantic deviation must return to the owning module for explicit decision.

## 9. Risks and non-claims

- A single coordinator may bottleneck; measure before considering sharding.
- Cross-service authorization freshness is not solved by a local DB transaction unless I supplies a verifiable decision/epoch contract.
- Object-store bytes are safe only if every access path honors private staging and the authoritative visibility gate.
- A DB transaction cannot enumerate unknown producers, external recipients, backups or restore paths. I's ProducerDomainInventoryEpoch and Target Inventory Seal remain separate global controls.
- This report does not prove physical erasure, backup expiry, external deletion, F/G/H enforcement or global Forget completion.
- No code, migration, runtime service, database engine, load test, crash injection or conformance test was executed.

## 10. Disposition

**Recommended:** accept the single-transaction coordination model as the Storage/Consistency design direction, subject to D/E/I resolution of O-01 through O-12 and verification of actual database capabilities.

**Current gate:** DESIGN REVIEW / PROPOSED REALIZATION ONLY. CR-P1-01 and INT-P0-03 remain OPEN. Do not label Implementation Verified, Conformance Passed, Contract Frozen or Production Ready.

**Next step:** D, E and Storage jointly select the shared linearization authority and operation/receipt contracts; I confirms authorization freshness and inventory linkage. Only then implement the coordinator, ledgers, visibility gate and crash-injection suite.


---

## Phase 3.5 Reassessment Addendum — Current D/E/I Owner Baseline

**Reassessment date:** 2026-11-16  
**Status:** DESIGN REVIEW / PROPOSED REALIZATION; no implementation or test execution is claimed.

This addendum supersedes stale source-baseline and OPEN-item wording above where the latest owner branches have since made semantic decisions. It does not supersede D/E/I authority.

### A. Current owner decisions consumed

D's current operation-level contract specifies nine semantic operations: RegisterProducerClass, RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. It specifies stable operation identities/digests, durable receipts, typed outcomes, idempotency and semantic linearization points.

E's current producer-admission and derived-registration addenda explicitly consume that operation set and correct earlier OPEN statements. Therefore this Storage review MUST NOT continue to describe D's semantic registration/fence fields, high-water type, operation receipt vocabulary or two-outcome race as undefined.

I's current inventory contract explicitly distinguishes:
- I ProducerDomainInventoryEpoch: global closed-world producer/recipient class and instance inventory;
- D ProducerRegistryVersion: D-local producer-class registry snapshot;
- D ProducerRegistrationHighWater: concrete admitted-work cutoff for one ForgetOperation.

These are distinct evidence dimensions. Storage can persist and reconcile them but cannot collapse them or claim that a complete D ledger proves global producer-domain completeness.

### B. Corrected Storage decision boundary

The recommended physical realization remains one shared per-Canonical-Memory-authority serialization domain. The logical coordinator must serialize at least:
1. RegisterProducerWork;
2. InstallForgetFence and its captured ProducerRegistryVersion + ProducerRegistrationHighWater;
3. RegisterDerivedDependency for the complete artifact/dependency set;
4. PublishDerivedIfFenceCurrent and the authoritative visibility transition;
5. CompleteProducerWork and barrier-visible terminal disposition.

RegisterProducerClass must commit a versioned enabled/disabled registry state which RegisterProducerWork reads in that same authority's admission order. CaptureProducerRegistrationHighWater is a consistent immutable read tied to the fence installation commit; it MUST NOT allocate a later cutoff or repair a missing ledger sequence.

**Important deployment qualification:** the single-database recommendation is valid only if D's authoritative fence/producer ledger and the visibility authority can participate in the same atomic transaction/serialization domain. If they are physically separate, a plain D-issued token followed by an independent E/object-store write is rejected. The only acceptable alternative is a D-approved durable prepare/commit or equivalent linearizable coordinator protocol in which the final visibility commit validates the current fence at its own commit point, survives coordinator/participant crash, and exposes no prepared artifact. This deployment choice remains unverified.

### C. Linearization and visibility invariants

- Work admission linearizes when the durable ProducerWork row and its ProducerRegistrationSequence commit in the same serialization domain used by fence installation.
- Fence installation linearizes when the effective fence and immutable registry-version/work-high-water snapshot commit together.
- Dependency registration linearizes only when the artifact identity and the complete required dependency edge set are durably committed as one complete registration; partial sets remain non-publishable.
- Publication linearizes only at the authoritative visibility commit. The latest fence, current dependency receipts, active work/attempt/lease and I-authoritative authorization decision must be validated within that commit's serialization boundary.
- Terminal disposition linearizes when the durable terminal receipt and barrier-visible terminal state commit after every output/attempt/replay path is resolved.
- The reader's visibility predicate must not trust a stale cache, staging path, object-store listing, index replay or outbox event. Only committed publication state may make an artifact queryable, and the applicable current fence remains enforceable on every read/rebuild path.

### D. Corrected OPEN item disposition

| Prior report item | Current disposition | Remaining work |
|---|---|---|
| O-01 shared serialization authority | **Storage realization OPEN; D semantic order DECIDED** | D + Storage name one authority/transaction or approved equivalent and prove it |
| O-02 producer sequence scope | **D DECIDED** | Persist typed ProducerRegistrationSequence/HighWater separately from CanonicalCommitCursor |
| O-03 EventRef-only ingress | **D/E semantics specified; detailed typed lineage/identity dependencies remain OPEN** | B/D/E confirm typed refs and immutable lineage binding; no untracked admission |
| O-04 retry/recompile identity | **OPEN** | D/E decide linked child/re-admission identity and barrier accounting before execution |
| O-05 dependency atomicity | **D semantic complete-set rule DECIDED** | Storage prove atomic complete-set commit or D-approved durable prepare/finalize with invisible incomplete state |
| O-06 visibility ownership/token | **D semantic visibility linearization DECIDED** | D/E/Storage select physical transaction/coordinator; no check-then-write |
| O-07 current I authorization | **I-owned OPEN** | I define authoritative decision freshness, revocation and lookup semantics at gate commit |
| O-08 terminal disposition | **D semantics specified** | E map multi-output/replay lifecycle; Storage prove stale lease/attempt cannot terminalize |
| O-09 global inventory linkage | **I semantics distinguish the epochs** | I/A/module owners prove closed-world ProducerDomainInventoryEpoch and map D-local registry/work evidence |
| O-10 transitive lineage/scope | **D/E typed evidence requirements specified; exact B/I identity integration remains OPEN** | Verify complete lineage digest and typed ScopeRef/source references, including EventRef-only and derivative-of-derivative |
| O-11 restore safety | **Storage + D/I realization OPEN** | Prove current Forget control ledger is replayed/authoritative before any restored artifact is served |
| O-12 database guarantees | **Storage OPEN** | Select engine/version/configuration and execute the verification plan in §6.1 |

The earlier OPEN-01..05 language in the body is to be read through this corrected owner-status table. Storage must not convert a semantic D decision into a claim that its physical realization is already implemented.

### E. Registration/fence proof — explicit exhaustive outcomes

Let the coordinator serialize RegisterProducerWork and InstallForgetFence. For any work W applicable to fence F:

**Admission commits first:** W receives sequence n; InstallForgetFence subsequently commits captured high-water H with n ≤ H. W is barrier-captured. It may continue only as tracked work; any dependency/publication gate subsequently observes F and cannot make a covered derivative visible.

**Fence commits first:** F and H become durable; RegisterProducerWork subsequently evaluates the current fence and commits REJECTED/QUARANTINED/CLEANUP_ONLY (as D's semantic contract directs). No lease or execution permission is granted.

No third state is legal. In particular, sequence allocation outside the same serialization transaction, local E admission based on cached fence, or queue insertion before authoritative receipt would violate the proof.

Fence/publication has the same two-order property: publication visibility commits first and is then part of the durable pre-fence inventory/reconciliation, or fence installation commits first and publication is rejected. A captured barrier is not itself a publication permit.

### F. Conformance plan status and required execution evidence

The existing C01–C20 matrix remains the executable plan, not a result. Add/retain the following hard assertions in its harness:
- For every generated WorkItemId, exactly one of (accepted with sequence ≤ the applicable fence H) or (durably rejected/quarantined/cleanup-only) is observable.
- No accepted work can be absent from the captured ledger snapshot.
- No VISIBLE artifact can lack a complete dependency receipt and committed PublicationReceipt.
- No stale lease epoch, stale fence observation or revoked PermissionEpoch can commit visibility.
- A late derivative or inventory epoch change invalidates/reopens any prior barrier/global completion proof.
- After failover/restore, stale control data cannot be served before the current Forget control ledger is reconciled.

Required evidence per run: engine/version/configuration, isolation and replication mode, two-client race trace, deterministic seed, crash point, request IDs/digests, registration/fence/dependency/publication/terminal receipts, authoritative reader snapshots, database transaction/lock/CAS traces, failover/restore logs, invariant-checker output and owner sign-off. None of this evidence is currently present; no C01–C20 test has been executed by this review.

### G. Updated disposition

**Recommended realization:** one durable transaction/linearizable coordinator per Canonical Memory authority, with Durable Work Ledger, immutable barrier snapshot, complete dependency registration, authoritative visibility commit and transactional outbox. Use a distributed prepare/commit or equivalent only if a single transaction domain cannot cover D's fence ledger and the authoritative visibility store.

**Gate:** DESIGN REVIEW / PROPOSED REALIZATION ONLY. D's semantic contract is substantially specified; Storage's physical serialization, replica/read behavior, restore safety and crash/fault conformance remain OPEN. INT-P0-03 and D-REV-P1-003 remain OPEN. No implementation, runtime or fault-injection verification is claimed.


## 8. Phase 3.6.2 additional C-series verification cases

| ID | Scenario | Required result | Evidence | Status |
|---|---|---|---|---|
| C21 | Offline producer/worker rejoin after fence | Original WorkItemId is resolved; latest fence is checked before dereference/lease/execute; no stale attempt publishes; unknown producer status blocks global proof | D registration/fence receipts, lease history, inventory state, reader snapshot | NOT RUN |
| C22 | ProducerDomainInventoryEpoch changes during Forget | I seal invalidates/reopens; D local high-water remains a separate unchanged cursor; no Global Forget completion until a replacement seal and target reconciliation | old/new I epoch and seal, D barrier snapshot, completion evaluator output | NOT RUN |
| C23 | Old Compiler task resumes after CanonicalSuppressionComplete | Current fence rejects/suppresses the task; late derivative reopens D proof; no post-fence visibility or stale completion reuse | WorkItemId/lineage, fence generation, participant/visibility trace, proof revision | NOT RUN |

C01–C20 are preserved unchanged. C21–C23 are additive coverage, not replacements.

## Phase 3.6.2 — Storage exact-version acceptance of JF-10 prepared participant ↔ COC bridge

**Reviewed exact A artifact:** `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, A branch `session-a-integration-2026-11-16`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, §12.1–12.8.

**Storage DECISION: ACCEPT THE STORAGE PARTICIPANT CONTRACT FOR THIS EXACT A BLOB, SUBJECT TO CONCRETE DATABASE CAPABILITY AND DEPLOYMENT PROOF.**

Storage accepts the following Storage-owned requirements as the target architecture:

1. Storage MUST receive a stable preallocated XID and participant identity before PREPARE; the operation ID, canonical RequestDigest, owner boundary, participant digest and canonical authority DB identity remain immutable across retries.
2. Storage MUST durably prepare that exact XID and retain private bytes and required target/lineage serialization locks until authoritative I COMMIT/ABORT recovery and participant resolution.
3. Storage MUST return an authenticated, Storage-signed `PreparedParticipantReceipt` binding the same XID, participant digest, operation ID/digest, DB identity and prepared state. A lost response is resolved through authoritative lookup of the same XID; no replacement XID is permitted.
4. Storage MUST execute forward-commit or rollback only for the same prepared XID in the direction of I's durable terminal decision. No heuristic commit/abort, timeout inference, alternate-XID recovery or reversal is permitted.
5. On commit, Storage atomically publishes VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox in the same Canonical Authority DB transaction. On abort, Storage proves non-publication. COC observation/reconciliation is not the visibility authority.
6. Storage's authoritative read API returns the same-XID prepared/committed/rolled-back state and exact PublicationReceipt from the authoritative database; stale replicas and caches are not decision sources.
7. Storage accepts COC as participant-accounting/observation only. COC does not decide the I transaction or authorize visibility.

**Implementation qualification:** this is architecture-level Storage acceptance, not proof that the selected database can provide durable prepared-XID/lock retention, crash-safe recovery, serializable D/Storage fence ordering or the required atomic visibility transaction. No concrete engine/version, XA profile, replication/failover topology, operator or deployment has been selected/verified by this decision. If the selected database cannot durably retain and recover the exact prepared XID and locks across crash/restart, implementation is blocked; no weaker check-then-write substitute is accepted.

Storage does not accept or decide I authorization/PermissionEpoch/receipt semantics, D fence meaning, H wire schema or multi-policy-domain atomicity. JF10-COC-01..10 and storage crash/fault suites remain NOT RUN. JF-10 remains P0 OPEN; implementation and production deployment remain NOT VERIFIED.


## Phase 3.6.2 — Storage exact acceptance of complete JF-10 ↔ COC decision bundle

**Decision:** **ACCEPT WITH ENUMERATED EXCEPTIONS — ARCHITECTURE / PARTICIPANT INTERFACE ONLY.** This confirms Storage's target participant and recovery contract for the single-I-PolicyDomain JF-10 v2 profile. It is not a selected-database capability statement, deployment acceptance, or production conformance result.

### Exact bundle reviewed
- A COC architecture: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- I JF-10 v2 Owner disposition: `8069ff86988396442c8d9dc3fd58653683abe2f3`
- D/E/Storage common JF-10 v2 recovery protocol: `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- C bridge Owner contract: `45a48249717c8cddb07ab96197730ef93d406c22`
- D fence/barrier Owner contract: `5a56c406578fdf257509315eb3f6f3f75456116c`
- Storage realization / participant contract: `55c01f4512f2e3d8aac767dd004e768ae073178e`
- H bridge wire mapping Owner contract (current branch readback): `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- H JSON Schema candidate: `a8a945cc3623c2907003b93625e3c79742150944`

### Storage-owned accepted semantics
1. Storage receives the immutable operation ID/digest, owner boundary, participant identity/digest, canonical DB identity and preallocated XID before PREPARE. Retries and recovery use the same XID; replacement XID or changed tuple is a hard conflict.
2. Storage durably prepares that exact XID and retains private bytes plus required target/lineage serialization locks until the authoritative I terminal decision and same-XID resolution are recovered.
3. Storage returns a Storage-signed PreparedParticipantReceipt binding the exact XID, participant digest, operation ID/digest, owner boundary and DB identity. Lost ACK is resolved by authoritative lookup of the same XID.
4. I COMMIT drives forward-commit of that same prepared XID; I ABORT / REVOCATION_WON / INDETERMINATE_ABORTED drives rollback/non-publication. UNKNOWN/IN_DOUBT remains prepared, private and unresolved. No heuristic commit/abort, timeout inference or alternate-XID recovery is permitted.
5. On commit, Storage atomically writes VisibilityPointer, immutable PublicationReceipt, owner outcome, receipt-consumption evidence and outbox in the same Canonical Authority DB transaction. Outbox is notification only. Authoritative reads must exclude stale replicas/caches as decision sources.
6. D retains fence/lineage authority; I retains authorization/sequencer authority; C retains provider outcome authority; COC is ordering/participant-accounting evidence only. No COC append or I COMMIT alone makes Storage content visible.
7. Acceptance is limited to one I PolicyDomain. Multi-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.

### Enumerated exceptions / closure conditions
- The common protocol and bridge are accepted as architecture/interface only. The actual DB product/version/build, extensions/configuration, isolation/replication/failover profile, prepared-XID capability, lock durability, operator and deployment boundary are NOT SELECTED / NOT VERIFIED.
- Storage has not executed a capability probe or crash/restart/failover/restore test. C01–C23 and JF10-01..13 remain NOT RUN.
- The required one-transaction visibility boundary and same-XID recovery must be proven on the selected engine. If unsupported, stop and publish a blocking incompatibility plus a D/I-approved alternative; do not substitute check-then-write or a weaker independent transaction.
- COC quorum/log durability, snapshot rollback protection, RPO/RTO, SLO, retention, KMS/key custody and operational ownership remain OPEN.
- This decision does not approve I external governance, cryptographic suite/key lifecycle, H production schema freeze, C provider implementation, or production activation. JF-10 P0 remains OPEN.
