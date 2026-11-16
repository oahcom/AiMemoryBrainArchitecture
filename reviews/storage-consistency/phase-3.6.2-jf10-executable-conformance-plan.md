# Phase 3.6.2 — JF-10 Executable Conformance Plan

- Owner: Storage test-plan lead with D/E/I boundary owners
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- Status: **TEST DESIGN / READY FOR IMPLEMENTATION MAPPING / NOT EXECUTED**
- Common protocol Blob: `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- I disposition Blob: `b7b0287cde3922434a560fca90051cc5b418d987`
- Scope: one I policy domain. Multi-domain requests must reject as BLOCKED/UNKNOWN.
- Non-claim: no implementation, runner, selected DB or test result is asserted.

## 1. Objective and release gate

Prove that the exact Storage prepared participant/XID is sequenced by I against revocation, retains D fence/lineage serialization, and alone can create the Storage visibility transaction.

JF-10 P0 cannot close until all cases pass on the production-equivalent coordinator and selected DB deployment, recovery/restore evidence is retained, and D/E/I/Storage independently accept their boundary evidence.

Every pass requires positive evidence (durable decision, participant transition, receipt and authoritative reader result) and negative evidence (no pointer/receipt before commit, no alternate XID, no duplicate receipt consumption, no heuristic outcome, and no staging/object-store/outbox/cache/index bypass).

## 2. Required harness

The executable harness must provide:
1. I sequencer/coordinator with authoritative authenticated lookup and durable log inspection.
2. Storage participant manager exposing XID lifecycle and prepared-lock state.
3. Canonical Authority DB configured as the candidate deployment: engine/version, isolation, HA, replication, durability and restore settings.
4. D fence, ProducerWork and Dependency ledgers with barrier-state probes.
5. E frozen manifest, stable WorkItemId and PublicationOperationId fixtures.
6. Revocation and I inventory-seal mutation actors.
7. Deterministic crash hooks, process kill/restart, ACK drop, replica lag, coordinator failover and DB failover/restore.
8. Authoritative reader probe plus independent staging/object-store/outbox/index/cache probes.
9. Correlated trace IDs: PublicationOperationId, RequestDigest, XID/digest, receipt ID, decision ID, policy domain, sequencer position, ForgetOperationId/FenceGeneration and manifest/dependency digests.
10. Integrity-protected machine-readable event log and evidence manifest.

Mocks that return expected values without exercising durable coordinator, participant and DB behavior are not conformance evidence.

## 3. Crash hooks

| Hook | Injection boundary | Required state |
|---|---|---|
| H01 | Before owner intent durable | No I request, no visibility |
| H02 | After owner intent, before participant PREPARE | Stable intent resolves, private |
| H03 | After durable XID PREPARE, before I registration | XID/locks survive, private |
| H04 | After I participant registration, before terminal decision | IN_DOUBT; conflicting revocation blocked |
| H05 | After durable I COMMIT, before ACK | Lookup returns same COMMIT; exact XID forward-commits |
| H06 | After durable I ABORT, before ACK | Lookup returns same ABORT; exact XID rolls back |
| H07 | During Storage local commit, before transaction commit | Atomic rollback/retry; no partial pointer/receipt/outbox |
| H08 | After local visibility commit, before Storage ACK | Same receipt read back; no duplicate publication |
| H09 | Coordinator failover/restore with unresolved XID | Decision/order retained; no heuristic resolution |
| H10 | DB failover/restore with prepared XID | XID/locks survive or remain safely blocked/private |
| H11 | Storage process restart with prepared XID | Same XID recovered |
| H12 | Revocation races unresolved participant | Revocation cannot pass earlier unresolved owner gate |
| H13 | D fence races participant prepare | Fence-first rejects; participant-first blocks fence until resolution |

## 4. Required conformance cases

| Case | Deterministic schedule | Required result |
|---|---|---|
| JF10-01 | I COMMIT durable; crash before Storage commit | Same XID forward-commits; one receipt/visibility transition |
| JF10-02 | I ABORT durable; crash before rollback ACK | Same XID rolls back; no pointer/receipt |
| JF10-03 | Storage commit succeeds; ACK lost; retry same key | Original receipt returned; no second commit |
| JF10-04 | I COMMIT durable; I ACK lost | Authoritative lookup returns same decision and position |
| JF10-05 | I unavailable before terminal decision | IN_DOUBT, private bytes, retained locks, revocation blocked |
| JF10-06 | I ABORT; coordinator failover/restore | ABORT retained; no heuristic COMMIT |
| JF10-07 | I COMMIT; coordinator failover/restore | COMMIT retained; exact XID forward-recovers |
| JF10-08 | DB failover/restore while XID prepared | XID/locks survive or remain unavailable/private; never silently disappear |
| JF10-I-09 | Conflicting revocation during IN_DOUBT | Revocation waits; ordering follows recovered terminal decision |
| JF10-I-10 | Replay same ID/digest/boundary/XID | Same state/position; receipt consumption exactly once |
| JF10-I-11 | Same ID with changed digest/XID/boundary/security tuple | Hard conflict; no second participant or receipt consumption |
| JF10-I-12 | Inventory epoch/seal changes before owner gate | Old seal rejected; BLOCKED/UNKNOWN; no visibility |
| JF10-I-13 | Inventory change ordered after owner gate | Exact prior seal snapshot remains bound; later global reconciliation stays open |
| JF10-D-14 | Fence commits before participant prepare | Prepare rejects; no publication |
| JF10-D-15 | Participant prepare wins before fence | Fence waits for participant resolution; barrier accounts for pre-fence publication if committed |
| JF10-E-16 | E retry/lease replacement during unresolved publication | Stable WorkItemId/PublicationOperationId; stale AttemptId/LeaseEpoch cannot publish |
| JF10-X-17 | Request spans two I policy domains | Reject/pause BLOCKED/UNKNOWN; zero per-domain partial commits |

## 5. Cross-case invariants

Every case asserts:
- I COMMIT is not reader visibility; only Storage's committed VisibilityPointer plus matching PublicationReceipt is.
- Only the exact XID bound to the immutable operation tuple may commit.
- Durable COMMIT/ABORT cannot be reversed heuristically.
- IN_DOUBT retains private bytes and required locks; timeout, missing row, lost ACK or stale replica is not terminal evidence.
- Conflicting revocation cannot pass an unresolved earlier owner gate.
- D fence and participant have one proven serialization order; I authorization never overrides D fence.
- VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox commit atomically.
- Staging, object store, outbox, index/cache and E-local state cannot bypass reader visibility.
- Same binding is idempotent; changed digest/boundary/XID/security tuple conflicts.
- Multi-domain requests never partially commit.
- Restore/rebuild remains quarantined until current I and D control state is reconciled.

## 6. Evidence bundle

Each run must record:
- case/run/schedule/fault IDs;
- exact D/E/I/Storage source commits and common protocol Blob;
- implementation build SHA, DB engine/version/config digest, coordinator version/config digest;
- policy domain and authenticated actor identities;
- PublicationOperationId, RequestDigest, XID/digest, CommitAuthorizationReceipt ID, decision ID and sequencer position;
- D ForgetOperationId, FenceGeneration, ProducerRegistrationHighWater, BarrierSnapshotReceipt and lineage digest;
- ProducerDomainInventoryEpoch and InventorySealReceipt ID/digest where applicable;
- ordered coordinator/participant/DB/fence/revocation traces and crash/failover events;
- Storage transaction/receipt readbacks and independent reader + bypass-path probes;
- assertion results, log hashes, evidence bundle digest and independent reviewer disposition.

Missing evidence is UNKNOWN, not PASS. A run without authoritative reader and coordinator/participant evidence is INVALID.

## 7. Implementation mapping before execution

The repository currently contains architecture specifications, not executable implementation or a test harness. Before any case is marked RUN:
1. identify the coordinator service/API, durable log and participant registry;
2. select DB engine/version and prove prepared-XID durability, lock retention, HA failover and restore;
3. map H01–H13 to code locations or deterministic fault injectors;
4. implement authoritative lookup and same-XID recovery workers;
5. implement shared D fence/Storage participant ordering on the selected DB;
6. provide D/E/I/Storage fixtures and authoritative reader/bypass probes;
7. add CI suite and reproducible run commands;
8. obtain each Owner's review of its own evidence and A's integration verification.

Until then: **TEST DESIGN COMPLETE / EXECUTABLE HARNESS NOT PRESENT / ALL CASES NOT RUN**.

## 8. Closure checklist

- [ ] I single-domain coordinator semantics implemented and durable
- [ ] Prepared XID survives process restart, coordinator outage, DB failover and restore
- [ ] D fence/lineage serialization and barrier ordering proven
- [ ] E stable identity and Storage receipt-readback behavior proven
- [ ] I validates required InventorySeal at the sequenced owner gate
- [ ] JF10-01..08 pass
- [ ] JF10-I-09..13 pass
- [ ] JF10-D-14..15 pass
- [ ] JF10-E-16 pass
- [ ] JF10-X-17 rejects multi-domain operations
- [ ] Independent D/E/I/Storage evidence review complete
- [ ] A accepts exact evidence bundle
- [ ] No unresolved UNKNOWN/IN_DOUBT participant or missing evidence


## 9. Executable reference-model implementation tranche — scope boundary

### Repository and implementation-location finding

The three Owner copies of the JF-10 common protocol currently read back to the same Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`. The Storage executable conformance plan is Blob `634b856a878234bac186c55b2937344392f5d5ff` and explicitly says **EXECUTABLE HARNESS NOT PRESENT / ALL CASES NOT RUN**. The repository README on main says this is an architecture-definition repository and implementation is not started by design. Organization repository discovery found only `AiMemoryBrainArchitecture`; no separate runtime implementation repository was identified.

### Work that can proceed without fabricating production claims

Create an executable, deterministic **JF-10 reference state-machine model** under the Storage-owned branch. It may validate logical ordering, stable identity, single-domain rejection, same-XID recovery rules, fail-closed IN_DOUBT behavior and the atomic publication invariant in a test model. It is explicitly not a production implementation and cannot prove database prepared-transaction durability, HA/failover, storage isolation, or real I sequencer integration.

### Production implementation still requires

- authoritative runtime repository and engineering owner;
- selected canonical database/coordinator deployment and verified prepared-XID support;
- I-owned sequencer API and durable receipt implementation;
- D/E/Storage runtime module mapping;
- production-equivalent crash/recovery, failover and restore tests.

The reference model is a development aid only. It must not change JF-10 P0, G3, or test-execution status.

## 10. Reference model published — implementation boundary retained

An executable logical reference model and deterministic unittest suite have been added on this Storage Owner branch:

- `reviews/storage-consistency/reference_model/jf10_linearization_model.py` — Blob is recorded by the subsequent Owner readback.
- `reviews/storage-consistency/reference_model/test_jf10_linearization_model.py`
- `reviews/storage-consistency/reference_model/README.md`

The model encodes one-policy-domain rejection; immutable coordinator terminal decision; stable operation/XID/manifest binding; PREPARED and UNKNOWN/IN_DOUBT behavior; same-XID recovery; modeled atomic publication facts; one-time receipt consumption; D fence-first and participant-first ordering; E retry identity semantics; and injected crashes immediately before and after the local publication commit point with projection reconstruction on recovery. A branch-scoped GitHub Actions workflow now runs the unittest suite on changes and pull requests, but no successful run has yet been verified.

D and E Owner branches now each contain an explicit consumption/mapping note:
- D: `03-memory-brain/phase-3.6.2-jf10-reference-model-consumption.md`
- E: `04-memory-compiler/phase-3.6.2-jf10-reference-model-consumption.md`

15 deterministic unittest methods are authored. No execution result has been verified in a local Python runtime or GitHub Actions; test status remains NOT RUN. **The committed unittest suite has not yet been run by a repository CI runner.** The reference model is in-memory and does not implement a durable coordinator, real database prepared transactions, shared serializable D/Storage state, I service, receipt cryptography, HA, failover, restore, or real reader/object-store integration.

### Status correction

- Logical reference model: **IMPLEMENTED**.
- Deterministic unittest source: **AUTHORED / NOT RUN IN REPOSITORY CI**.
- Production JF-10 implementation: **NOT IMPLEMENTED / NOT VERIFIED**.
- Production conformance JF10-01..17: **NOT RUN**.
- JF-10 P0: **OPEN**.
- G3: **BLOCKED** pending authoritative runtime repository, accountable engineering owner, database/coordinator selection and production-equivalent evidence.

The model is not a substitute for the production harness specified above.

## 11. JF-10 logical reference-model CI result — 2026-11-16

A branch-scoped GitHub Actions run executed the committed deterministic unittest suite:

- Workflow: `JF-10 Logical Reference Model`
- Run: `43895971452`
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43895971452
- Head commit: `684ac873bec331649c18a45a992007d04f211832`
- Test source Blob: `a38d73b4a5e7c65210fb414a62fb91b30649b788`
- Result: **SUCCESS**
- Job: `Deterministic JF-10 reference-model tests`
- Step `Run unittest suite`: **SUCCESS**
- Authored unittest methods: **15**

The 15 logical tests cover prepared-not-visible, I decision before Storage commit/IN_DOUBT, same-XID recovery, unknown decision fail-closed, crash before/after the modeled local commit, exact receipt binding, idempotent readback, abort, D fence-first and participant-first races, multi-domain rejection, stable operation/digest binding, E retry identity and immutable terminal decision.

**Strict evidence boundary:** this is a successful CI run of the in-memory Python reference state machine only. It is not a real database, prepared-XID, I sequencer, COC consensus, D/Storage shared transaction, process-kill, HA/failover, backup/restore, object-store or reader integration test. It does not pass JF10-01..17 production conformance, COC-01..16, Storage C01..C23, I-CO or G-CO. JF-10 P0 remains OPEN; production implementation remains NOT IMPLEMENTED / NOT VERIFIED; G3 remains BLOCKED.
