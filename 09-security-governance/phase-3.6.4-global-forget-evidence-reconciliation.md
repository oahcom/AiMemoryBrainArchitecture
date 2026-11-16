# Phase 3.6.4 — Global Forget Target Evidence Reconciliation

- Owner: I — Security & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Date: 2026-11-17
- Status: **TECHNICAL EVIDENCE RECONCILIATION; GOVERNANCE APPROVAL AND GLOBAL COMPLETION NOT CLAIMED**
- Base inventory contract Blob: `9100061fa986fb6676656169de3fcf9fc1c72664`
- Phase 3.5 identity/Forget governance Blob: `a8632931396125019d1afccff39ea266f52a4d3a`
- Retention/backup/erasure policy Blob: `f14cb2149ca3f817229533005ab89dbdc7f0b3a8`
- COC durable protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- COC exact owner acceptance matrix commit: `e5fad5b3e67662134c18e33090b08d874f161f41`

## 1. Purpose and authority boundary

This document reconciles current design and test evidence against I's existing Global Forget target classes and Completion Evidence Vector (CEV). It does not approve I36-GOV-01..10, seal a ProducerDomainInventoryEpoch, create a TargetInventorySeal for a real Forget operation, grant a PolicyException, declare Global Forget complete, or claim physical erasure. Formal governance approval remains subject to the I governance register's exact approver/evidence requirements.

## 2. Current target-class evidence matrix

| I inventory class | Accountable owner(s) | Current evidence | Current state | Missing evidence / hard stop |
|---|---|---|---|---|
| D canonical Memory, ForgetFence, lineage and producer barrier | D | D fence/publication gate and JF-10/COC exact acceptance; COC Gate B protocol accepted at design level | DESIGN ACCEPTED / RUNTIME OPEN | Durable D ledger, real producer registration/high-water, lineage enumeration and barrier drain not executed. |
| E ingress, compiler workers, queues, leases, retries, DLQ, staged outputs and derivatives | E | E producer lifecycle and JF-10/COC exact acceptance; immutable WorkItem/PublicationOperation/manifest rules | DESIGN ACCEPTED / RUNTIME OPEN | Production ingress/outbox/worker ledger, exact D registration, queue replay and artifact visibility integration absent. |
| F indexes per partition, retrieval materializations, caches, Working Sets and rebuild workers | F | In-memory anti-resurrection model 19/19 tests PASS; CI run `43961714501`, job `133630540252` | LOGICAL MODEL PASS / RUNTIME OPEN | Actual ANN pre-filter, partition watermark, cache-shard invalidation, rebuild/reconnect, concurrent fill, offline adapter and stale snapshot tests F-RT-01..13 remain NOT RUN. |
| G Context membership/materializations, snapshots, deltas, ChangeSets, delivery intents and delivery ledger | G | G Applied/Forget contract and exact JF-10/COC evidence acceptance | DESIGN ACCEPTED / RUNTIME OPEN | Durable Context reconciliation, real delivery/ACK ledger, adapter/session replay and Full Applied validator/persistence not executed. |
| H Adapter instances, regions, local buffers, queues and caches | H | BMCP JF-10 schema candidate; 11/11 Draft 2020-12/fixture tests PASS, run `43962364955`, job `133632849768` | SCHEMA STRUCTURE PASS / RUNTIME OPEN | No live adapter capability inventory, authenticated per-region ACK, reconnect replay, buffer purge or duplicate-key/signature/channel-binding test. |
| Storage backups, replicas, snapshots, WAL/archive and restore destinations | Storage | PostgreSQL 18.7 capability profile 7/7 CI SUCCESS: `43958775001`, `43959079736`, `43959079669`, `43959079703`, `43959079745`, `43959079760`, `43959079930` | ENGINE CAPABILITY PASS / DEPLOYMENT OPEN | No production backup catalog, real Forget restore drill, full control-ledger replay, external anchor or production replica/region inventory. |
| External recipients, exports, sync services, analytics, model/inference providers and onward recipients | I + C/H + recipient owners + Privacy/Legal | Candidate target classes and evidence contract only | UNKNOWN / GOVERNANCE OPEN | No complete provider/recipient registry, onward-recipient enumeration, deletion contracts, target-bound receipts or legal/privacy exception approvals. |
| Other derived/copied artifacts: summaries, embeddings, projections, reports, human/admin exports, support bundles | E/F/G/H + product/data owners | Candidate class taxonomy only | UNKNOWN / INVENTORY OPEN | No authoritative complete enumeration, lineage inventory, owner evidence or deletion/retention action per target class. |
| Audit/observability logs, traces, metrics, incident attachments and tombstones | I + Storage + audit owner | Candidate retention/minimization policy only | UNKNOWN / GOVERNANCE OPEN | No data map, retention schedule, non-reconstructive tombstone verification, legal basis or independent reconstruction test. |

## 3. CEV reconciliation

| CEV component | Current design/evidence | Current status |
|---|---|---|
| ImmediateAccessSuppression | D fence contract and F logical suppression model; no live D/F serving boundary | DESIGN / RUNTIME UNKNOWN |
| ProducerBarrierCompletion | D/E/Storage/JF-10/COC design contract and owner acceptance; no integrated ledger | DESIGN ACCEPTED / RUNTIME OPEN |
| DerivedArtifactCleanup | E/F/G target contracts; F reference model only | PARTIAL LOGICAL EVIDENCE / RUNTIME OPEN |
| RuntimeContextAdapterSuppression | G/H contracts; H schema shape tests only | DESIGN / RUNTIME UNKNOWN |
| ExternalCopyHandling | Inventory taxonomy only | UNKNOWN / GOVERNANCE OPEN |
| BackupRetentionRestore | PostgreSQL 18.7 isolated prepared-XID/PITR/restore tests | ENGINE CAPABILITY EVIDENCE ONLY |
| PhysicalErasure | Policy definition only | NOT PROVEN / NO CLAIM |

Global completion requires every mandatory target and CEV component Confirmed or a narrowly approved, valid, unexpired PolicyException; NotApplicable requires positive evidence of absence and independent review. No component rollup can hide missing target members.

## 4. Epoch, seal and barrier non-substitution

1. I ProducerDomainInventoryEpoch covers the global producer/recipient/backup/export catalogue. It is not D's per-operation ProducerRegistrationHighWater or WorkItemBarrier.
2. D ForgetFenceGeneration and effective fence position are not I PermissionEpoch or COC CoordinatorEpoch/Index.
3. F IndexWatermark and partition generation prove only F's local index coverage; they cannot confirm external recipients, H adapters or backup erasure.
4. H Adapter ACK proves only the exact target/action/scope/capability/session it authenticates. Request receipt is not delete completion; UNSUPPORTED/offline/timeout remains Unknown.
5. PostgreSQL prepared-XID/PITR capability tests do not prove the production backup universe or restore completion for a real ForgetOperation.
6. COC recovery batch and terminal proof establish order/participant accounting only; they do not mint I/D/Storage owner outcomes.

## 5. Current executable evidence and limits

- F anti-resurrection logical reference model: 19/19 tests pass. This is not an actual index/cache/Working Set implementation.
- H JF-10 bridge JSON Schema: 11/11 structural/conditional fixture tests pass. This is not transport, cryptographic, duplicate-key or adapter runtime conformance.
- Storage PostgreSQL 18.7 prepared-XID/PITR/HA capability profile: 7/7 workflows pass. This is not a production DB deployment, complete backup inventory or real Global Forget restore drill.
- A COC outage recovery logical model: 11 tests pass; JF-10/COC semantic validator: 18 tests pass. Neither is a live Raft quorum or cross-owner service integration.
- I Global Forget logical reference model and workflow files have been added under `09-security-governance/tests/`; **CI execution has not yet been observed** and is not counted as passing evidence.

## 6. Formal governance status — unchanged

The following remain GOVERNANCE-BLOCKED in `governance-decision-register.md` and the Phase 3.6 Governance Approval & Consumer Acceptance Register:

- I36-GOV-01: trusted issuer registry/federation/key lifecycle.
- I36-GOV-02: delegation eligibility, depth, audience, expiry and parent revocation.
- I36-GOV-03/04: cross-Scope and cross-Environment grant algebra.
- I36-GOV-05/06: revocation effective point, in-flight ordering, PermissionEpoch partitioning/freshness and offline behavior.
- I36-GOV-07: unsupported Adapter/producer controls and residual-risk policy.
- I36-GOV-08: external recipient/backup retention exceptions and physical-erasure policy.
- I36-GOV-09/10: Principal resolution and ActorRef/Principal binding policy.

No formal approval record with approver PrincipalRef/Issuer, authority basis, exact policy hash, scope/jurisdiction, independent reviewer, effective version/time and expiry was created. Technical owner acceptance and user delegation to execute engineering work are not substitutes for those governance approvals. I must not self-approve legal/privacy/security risk or mark a PolicyException.

## 7. Current disposition

- ProducerDomainInventoryEpoch: no production authoritative registry/seal asserted.
- TargetInventorySeal: no real-operation seal asserted.
- Global Forget Completion: **OPEN / NOT COMPLETED**.
- ExternalCopyHandling: **UNKNOWN / GOVERNANCE OPEN**.
- BackupRetentionRestore: **ENGINE CAPABILITY TESTED; REAL INVENTORY/RESTORE OPEN**.
- PhysicalErasure: **NOT PROVEN; NO CLAIM**.
- PolicyException: **NO NEW EXCEPTION APPROVED**.
- INT-P0-03: design contract accepted; runtime conformance and complete target evidence remain P0 OPEN.

## 8. Required next execution order

1. Populate the authoritative I producer/recipient/backup/export inventory with authenticated owner, instance, ScopeRef, capability, retention and onward-recipient metadata; record registry gaps rather than guessing.
2. Reconcile each D/E/F/G/H/Storage target instance/partition against that global inventory and exact per-owner evidence contract.
3. Implement and execute actual F runtime suppression/rebuild/reconnect and G/H adapter ACK paths; reference-model passes are not substitutes.
4. Execute real Storage backup/restore after Forget with quarantine and current I/D control-ledger replay, then prove no stale visibility.
5. Obtain external recipient deletion/withdrawal evidence or retain Unknown; any exception goes through authorized Privacy/Legal/Security/data-owner approval.
6. Only an authorized I/governance approver may approve I36-GOV items and any PolicyException; record exact text/hash and approver proof.
7. Re-seal inventory after every relevant epoch/target change and evaluate the full CEV. Never mark Completed while any mandatory target is Unknown, Failed, Pending or unapproved PolicyException.

**Final:** this reconciliation narrows the technical unknowns and records new model/CI evidence, but Global Forget remains open. No real target inventory seal, global completion, external deletion or physical erasure is claimed.
## 9. Reference-model CI result — superseding the pre-run note (2026-11-17)

The Global Forget inventory/completion logical reference model now has a successful CI run. Evidence: `phase-3.6.4-global-forget-reference-model-evidence.md`, commit `674b9496bcb866fdaf725108104ce55f6d127528`; model Blob `5233da028e409ec3f41848582dad73a923e7155b`; test Blob `091f9450adf49a2a9f9ec8a2fa4470918023f765`; run `43962873109`, job `133634616584`, commit `73a0bff13b531b5b9feaeeec1887db31d6266589`; **25/25 tests PASS**.

This supersedes §5's statement that CI execution had not yet been observed. It does not change the limits in §§1–8: the model is in-memory, and no real inventory seal, production target evidence, external deletion, formal governance approval, PolicyException or physical erasure is claimed.