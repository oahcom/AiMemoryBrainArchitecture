# Phase 3.6 — Storage Deployment Selection and Verification Readiness

- Authority: user-delegated DE-S Joint Architect acting across D/E/Storage
- Storage decision owner: DE-S joint architect for logical realization; independent production engineering approval remains required
- Date: 2026-11-16
- Status: **LOGICAL DEPLOYMENT PROFILE SELECTED / CONCRETE ENGINE AND RUNTIME DEPLOYMENT BLOCKED**
- Baseline: preserve the already-decided D/E/Storage logical Forget Atomicity contract; this record selects its preferred realization and does not reopen its semantics.
- I dependency: **BLOCKED — I Owner approval requested in repository issue #4; no I policy approval is implied.**

## 1. Existing decision preservation

The following previously decided operations remain normative and unchanged:
1. ProducerClass registration and authenticated ProducerIdentity binding before admission.
2. Producer WorkItem registration and durable receipt before enqueue, lease, protected source dereference or execution.
3. ForgetFence installation and immutable barrier high-water capture in the same per-authority serialization order as producer admission.
4. Complete dependency registration and immutable output-manifest version/digest before publication.
5. Final Publish Gate revalidates latest applicable fence, complete dependency set, current work/attempt/lease, current manifest/inventory evidence, exact lineage/scope and I-authoritative authorization.
6. Durable visibility commit and PublicationReceipt are one atomic observable outcome.
7. Every read surface uses authoritative visibility; stale indexes/caches/replicas cannot bypass it.
8. Producer terminality requires all outputs, attempts, child work and unknown outcomes accounted for.
9. Retry/replay preserves WorkItemId, uses a new AttemptId and LeaseEpoch, and rechecks current fence/authorization.
10. Late derivatives invalidate/reopen prior barrier evidence and are suppressed before exposure.

No new semantic conflict was found in the reviewed baseline. The JF-01..JF-09 closure remains intact.

## 2. Option comparison

Rating is qualitative against the already-decided invariants, not a benchmark of an unspecified vendor.

| Option | Atomicity / linearization | Crash recovery / ACK loss | Idempotency | Fence/Publish and Permission Revocation races | Local deployment complexity | Testability | Migration cost | Decision |
|---|---|---|---|---|---|---|---|---|
| Single transactional DB + per-authority coordinator row/serializable transaction | Strongest direct fit when all authoritative records share one transaction | Native commit outcome lookup; durable rows/receipts; recovery can query same key | Unique idempotency key + request digest in same DB | Fence, admission, dependency, visibility and terminal writes share one commit order; I permit freshness still requires I protocol | Lowest among valid options; DB HA/backup still material | High: deterministic two-connection tests and transaction traces | Medium: ledger/visibility schema and migration | **SELECTED BASELINE** |
| CAS / conditional update | Linearizable for the CAS target only; does not atomically include unrelated writes by itself | Requires idempotent retry and read-after-CAS recovery | Good for versioned operations | Safe only when dependent ledger and visibility writes are inside the same transaction/atomic unit | Low-medium | High for single-record CAS; more complex across records | Medium | **USE INSIDE SELECTED DB TRANSACTIONS**, not standalone replacement |
| Durable Work Ledger | Not a complete serialization mechanism by itself | Strong recovery/terminal accounting if durable and queryable | Natural stable WorkItemId + receipt lookup | Makes admission/barrier state durable but does not alone serialize visibility/fence | Medium (schema, compaction, reconciliation) | High | Medium-high for existing queue systems | **REQUIRED COMPONENT** |
| Transactional Outbox | Atomic with source transaction only when same DB | Excellent ACK-loss and replay handling for notifications | Dedupe by event/operation ID | Does not itself gate publish or serialize a remote visibility store | Low-medium | High | Low-medium | **REQUIRED SUPPLEMENT**, never the visibility authority |
| Serialized Coordinator service | Can linearize if backed by durable consensus/log and controls all participants | Requires durable decisions, participant recovery and in-doubt resolution | Must implement operation log/idempotency | Can serialize races only if commit participant enforces current fence and I authorization at final visibility point | High operational burden (HA, quorum, recovery, observability) | High but operationally expensive | High | **NOT SELECTED** while single DB is feasible |
| Durable 2PC / distributed transaction | Can provide atomicity with durable prepare/commit across participants | In-doubt states and coordinator recovery are complex | Requires stable global operation IDs | Possible only with hidden prepare and final current-fence/authorization validation; no participant may expose prepared state | Very high | High complexity | High | **FALLBACK ONLY** if one DB transaction cannot span authority |
| Eventual consistency / async reconciliation | Cannot provide required safety linearization | Stale reads and partial effects remain possible | Eventual dedupe does not repair exposure | Unsafe window for fence/publish and revocation | Superficially low | Cannot prove invariant | Low initially, high remediation | **REJECTED** |

## 3. Selected logical deployment profile

Select **one transactional database per Canonical Memory Authority**, using a per-authority coordinator row/lock and serializable (or formally proven equivalent strict-serializable) transactions.

The selected database transaction domain must contain, or atomically govern:
- ProducerClass registry/version/status;
- Producer Work ledger, registration sequence and immutable request digest;
- ForgetOperation, ForgetFence generation and immutable BarrierSnapshotReceipt;
- dependency-set and frozen OutputManifest records;
- AttemptId / LeaseEpoch fencing state;
- idempotency operation/outcome records;
- final publication decision and authoritative VisibilityPointer;
- PublicationReceipt and terminal disposition receipt;
- transactional outbox event and delivery state;
- restore/reconciliation watermark and control-ledger references.

### Object/blob storage

Large artifact bytes may be stored outside the database only in a private, non-listable/non-queryable staging area. Object existence, object path, bucket listing, outbox event or index row never makes an artifact visible. The database VisibilityPointer is the sole publication authority. A consumer must resolve current visibility and current fence/authorization at response finalization; stale replica/cache use is denied for safety decisions.

### CAS and conditional writes

Use CAS/conditional updates for expected version, manifest version, fence generation, lease epoch and idempotency state transitions, but execute the safety-critical dependent writes in the same selected DB transaction. Standalone CAS on one row is not accepted as a substitute for the atomic ledger + visibility transaction.

### Transactional outbox

Write outbox entries in the same transaction as the corresponding durable source state. Delivery is at-least-once and idempotent. An outbox message is a notification, not proof of publication or completion.

## 4. Transaction boundaries and race outcomes

**Admission / fence transaction:** serialize ProducerWork registration and InstallForgetFence under the same authority/lineage coordinator. Registration-first means sequence is included in captured high-water; fence-first means ordinary admission is rejected/quarantined or cleanup-only.

**Dependency transaction:** persist the complete dependency set and exact frozen manifest version/digest as one logical completeness unit. Partial dependency state is not publishable.

**Visibility transaction:** atomically verify current D fence, barrier registration, current work/attempt/lease, exact dependency digest, frozen manifest version/digest, applicable I inventory seal reference, and commit-usable I authorization proof; then atomically change VisibilityPointer and write PublicationReceipt. If any predicate is unknown, stale or mismatched, commit is denied and artifact remains private.

**Terminal transaction:** compare-and-set exact final frozen OutputManifestVersion/digest and prove all outputs, child work, attempts and commit outcomes are terminal before writing the immutable terminal receipt.

**Read boundary:** authoritative read validates current visibility/fence/authorization at response finalization. An unavailable authoritative state means omit/deny affected content.

### Permission revocation dependency

The selected DB transaction does not magically serialize an external I policy service. The I-owned interface must provide either:
1. I policy/epoch state in the same authoritative transaction domain; or
2. an I-issued, audience/action/resource/scope/subject-bound authorization lease/fencing permit whose validity is serialized against revocation and cannot remain commit-usable after revocation becomes effective; or
3. another formally proven recoverable protocol with equivalent ordering.

The I Phase 3.6 source currently allows an online authoritative decision or an approved bounded authorization lease in principle, but its governance register I36-GOV-05/06 remains GOVERNANCE-BLOCKED. No commit permit, lease policy, revocation protocol or approval is assumed here. Until I supplies and approves the interface, final publication remains **BLOCKED / FAIL CLOSED**.

## 5. Failure and recovery strategy

| Failure | Required recovery |
|---|---|
| Before transaction commit | No durable admission/publication/fence effect; retry same key/digest only after authoritative outcome resolution |
| Commit succeeds, ACK lost | `GetOperationOutcome(key,digest)` on authoritative DB returns original receipt and commit cursor |
| Outcome indeterminate | Preserve UNKNOWN; do not infer abort, create a new key or terminalize; keep staged bytes hidden |
| Crash after staging | Staged bytes remain private; reconcile same WorkItemId/AttemptId and rerun final checks |
| Crash during dependency registration | Transaction commits complete set or no publishable set |
| Crash after visibility commit before E ACK | Read authoritative VisibilityPointer + PublicationReceipt; idempotently recover E state |
| Worker lease expires | Increment LeaseEpoch; stale worker cannot stage/publish/terminalize |
| Fence advances before publish | Visibility transaction rejects; artifact remains private |
| Publish commits before fence | Publication receipt and dependency are durable pre-fence state; fence reconciliation captures/suppresses them |
| I revocation ordering unavailable | Deny final commit; do not accept stale/cached ALLOW |
| Outbox delivery duplicate/out of order | Consumer dedupes stable event ID and preserves contiguous cursor; visibility remains DB-authoritative |
| Failover/restore from stale snapshot | Enter RecoveryQuarantined; reconcile monotonic Forget control ledger and current I references before serving or publishing |

## 6. Deployment assumptions and unresolved risks

The repository contains Markdown design artifacts only on the inspected main, D, E and Storage tips; no source code, migrations, executable test project, CI workflow, database configuration or runtime deployment manifest was present. Therefore this is a **logical deployment profile selection**, not a concrete product deployment.

Still OPEN:
- database product, version, storage engine and schema;
- transaction isolation/strict-serializability guarantee and lock semantics;
- HA/replication/failover and primary-read consistency;
- transaction size/contention and per-authority throughput limits;
- object-store private ACL and exposure proof;
- backup catalog, control-ledger independence and restore procedure;
- I authorization permit / revocation serialization contract and governance approval;
- production migration plan, backfill, dual-read/write, rollback and cutover criteria;
- named independent Storage engineering approver and operational owner.

No vendor, SQL dialect, isolation guarantee, deployment topology or migration compatibility is invented.

## 7. Formal approval boundary

- **Logical architecture decision:** selected by DE-S under the user's explicit joint delegation.
- **D semantic acceptance:** D owner semantics unchanged; D does not approve I policy or claim physical implementation.
- **E producer acceptance:** E consumes the selected DB transaction/receipt boundary; E does not claim an executable implementation.
- **Storage implementation approval:** requires named engineering owner to verify exact database/version/configuration, transaction semantics, HA/failover/restore and test evidence.
- **I governance approval:** I/security/privacy/legal/data authorities approve I-owned inventory, authorization, exception and completion policy. DE-S cannot approve it.
- **Release/production approval:** separate service/product/security/data owners after implementation and test evidence.

## 8. Verification status

- D36 matrix: **NOT RUN**.
- E36-01..E36-20: **NOT RUN**.
- C01–C20: **NOT RUN**.
- Authorization/revocation, manifest/inventory, read-response/fence, unknown-outcome and restore fault additions: **NOT RUN**.
- Implementation Verified: **NO**.
- Deployment Implemented: **NO**.
- Production Ready: **NO**.


## 9. I technical baseline refresh — CommitAuthorizationReceipt and JF-10

A later branch-aware read found I HEAD `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb` and the new I artifact `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` (Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`).

The I technical baseline now specifies:
- one logical I linearizable commit sequencer per policy domain;
- a single-use, non-transferable `CommitAuthorizationReceipt` bound to the full principal/actor/action/resource/purpose/audience/scope/environment/delegation/operation ID/payload digest/owner boundary/decision tuple;
- the final owner commit/disclosure gate participates in the same per-domain commit ordering protocol as revocation;
- terminal outcomes `COMMIT_WON`, `REVOCATION_WON`, `INDETERMINATE_ABORTED`;
- offline authorization leases, stale-epoch grace and cached ALLOW without online currentness proof are prohibited in the Phase 3.6 baseline;
- multi-policy-domain operations require an all-or-none common coordinator decision.

DE-S adopts this exact receipt and outcome vocabulary. This is a technical baseline update, not a governance approval. The I document explicitly keeps external governance approvals GOVERNANCE-BLOCKED and C/D/E/F/G/Storage consumer acceptance OPEN.

### JF-10 — cross-authority crash atomicity remains P0 OPEN

The I document establishes ordering semantics but does not fully define the durable crash-recovery coupling between the I sequencer's COMMIT_WON and Storage's owner transaction that commits VisibilityPointer + PublicationReceipt. Required joint I/Storage specification:
- durable shared operation correlation and immutable payload digest;
- exact commit handshake/participant or coordinator protocol;
- idempotent authoritative outcome lookup across I and Storage;
- recovery for I sequencer COMMIT_WON followed by owner DB abort/crash;
- recovery for owner transaction/ACK loss and duplicate receipt replay;
- one authoritative terminal outcome and no visibility from one-sided evidence;
- hidden prepared/ambiguous artifacts until both authorities reconcile.

The selected local transactional DB remains the D/E/Storage baseline, but it does not alone prove I/Storage cross-authority atomicity. Final publication remains fail-closed until JF-10 is specified, jointly accepted and tested.

### I inventory and Global Forget remain separate

The latest I trust/authorization technical closure does not resolve the I-owned ProducerDomainInventoryEpoch / InventorySeal governance decision or Global Forget Completion approval. The inventory/completion artifact remains CANDIDATE and I36-GOV-07/08 remain GOVERNANCE-BLOCKED in the trust-policy approval register. Repository issue #4 tracks the I Owner response.

 
## 10. Phase 3.6.2 — Storage deployment decision for JF-10 v2

**Status: STORAGE ACCEPTS THE LOGICAL PARTICIPANT/RECOVERY MODEL; CONCRETE ENGINE SUPPORT AND I ACCEPTANCE REMAIN OPEN.**

### 10.1 Selected topology

Retain one transactional database per Canonical Memory Authority for D and Storage records. The same serializable transaction domain contains the D authority coordinator, ProducerWork/registration ledger, ForgetFence/barrier snapshot, dependency/manifest records, Storage PublicationIntent, VisibilityPointer, PublicationReceipt, owner outcome, idempotency receipt-consumption and outbox. Large immutable artifact bytes may be held in a separate object store only as private staging.

For protected publication crossing into I's policy domain, select a durable 2PC protocol in which:
- I's policy-domain sequencer is the durable coordinator for the exact owner-final-gate operation and revocation order;
- the Canonical Authority DB is a prepared participant identified by a stable XID and immutable participant digest;
- prepared state and target/lineage serialization locks survive process restart and coordinator outage;
- I's durable COMMIT/ABORT decision drives forward commit/rollback of that exact participant;
- VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox commit atomically in the local DB;
- PUBLISHED is reported only after participant commit and authoritative receipt readback.

This supersedes the prior JF-10 split model of an independent I COMMIT_WON followed by an unrelated Storage visibility transaction. I COMMIT_WON alone is never visibility.

### 10.2 Option disposition

- Single local DB transaction: selected for D/Storage owner-local atomicity; insufficient alone for I policy-domain ordering.
- Durable Work Ledger: required; it is accounting and recovery state, not a substitute for the coordinator.
- Transactional Outbox: required in the same local commit; delivery is at-least-once and not visibility.
- CAS/conditional update: required inside serializable transactions for generation, lease, manifest and visibility-version checks; not a standalone cross-record transaction.
- Serialized coordinator: no separate best-effort coordinator service is selected. I sequencer owns policy-domain ordering; local DB coordinator owns D/Storage state order.
- Cross-authority 2PC: selected for JF-10 because I requires the actual owner final gate to participate in the revocation order. Durable coordinator decision, prepared participant recovery and in-doubt blocking are mandatory.
- Eventual consistency, process-local mutex, check-then-write, stale replica, outbox-only ordering and independent I decision followed by uncoordinated Storage commit are rejected.

### 10.3 Operational constraints and gates

The DB must support durable prepared transactions/XIDs (or a formally equivalent recoverable participant protocol), retaining required locks across crash/restart and supporting deterministic recovery from the I coordinator log. The I sequencer must persist participant identity, immutable request digest, terminal decision, sequencer position and recovery ownership. If either side cannot guarantee this, JF-10 remains P0 blocked and protected publication remains private.

Concrete DB engine/version, XA/prepared-transaction semantics, transaction timeout/lock behavior, replication/quorum, failover, backup/restore, operator runbooks and production engineering approval are NOT SELECTED / NOT VERIFIED. These require a real target environment, migration, failure injection and independent Storage engineering sign-off.

## 11. COC / CGH-APPLIED-1.1 Storage boundary decision — exact amendment review

Storage has published `reviews/storage-consistency/phase-3.6-coc-storage-boundary-acceptance.md`, Blob `a589d983ac145244962c22e5da3a55427aa35ff8`, commit `7b83e61c44dd4b67fa2059a3bff83d453aeaf757`.

Decision: **CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY** for the exact A COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` and CGH-APPLIED-1.1 package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.

The COC is accepted as a logical cross-authority causal-order ledger, but it is not the per-Canonical-Memory-authority D/Storage visibility transaction and is not I's policy-domain sequencer or JF-10 2PC coordinator. Storage's one-transaction local visibility authority remains unchanged. I's owner-gate-participating JF-10 protocol remains a separate required approval; no COC append or copied receipt substitutes for I's sequencer decision or Storage's committed VisibilityPointer/PublicationReceipt.

A combined COC + JF-10 + Storage visibility flow remains BLOCKED/UNKNOWN until I specifies and approves an exact bridge, C/D/Storage accept the participant and recovery semantics, and the bridge is implemented and fault-tested. Outbox remains notification only.

The review explicitly does NOT designate a real operator, voter topology, DB product/version, RPO/RTO, SLO, KMS/key custody or deployment. Those remain OPEN pending actual infrastructure and accountable engineering evidence. COC-01..16, JF10-01..17 and Storage C01..C23 remain SPECIFIED / NOT RUN; production implementation NOT VERIFIED.


## 12. Gate A — PostgreSQL 18.7 candidate profile and physical probe result (2026-11-17)

Storage selects PostgreSQL 18.7 as the concrete candidate engine for JF-10 capability qualification. This selection applies to the pinned test profile only; it does not assert that a production Canonical Memory Authority deployment is already on this engine.

The Storage-owned dossier is:
- Path: reviews/storage-consistency/phase-3.6.2-postgres-18.7-prepared-xid-capability-dossier.md
- Candidate image: postgres:18.7
- Observed build: 18.7 (Debian 18.7-1.pgdg13+2)
- Image digest: sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc
- Probe Blob: c15ea6e66a15be2fb96f737769f58b7b6c224b7e
- Workflow Blob: 4eef5b24f6da1d596c34e0d072dc39d5008a1a25
- Successful workflow run: 43907296027
- Run commit: 8c9ef00364d93c383aba515923565f8dc04bf1b6
- Job ID: 133439447210

Exact tested settings: max_prepared_transactions=16, fsync=on, synchronous_commit=on, full_page_writes=on, wal_level=replica; SERIALIZABLE isolation; named persistent Docker volume.

**Observed PASS:** prepared transaction stayed invisible; row lock remained held; same prepared XID survived SIGKILL + container restart on the same volume; same-XID COMMIT PREPARED exposed VisibilityPointer and PublicationReceipt together; same-XID ROLLBACK PREPARED left both absent.

**Gate A disposition: PARTIAL PASS / OPEN.** The single-node PostgreSQL 18.7 prepared-XID, lock-retention, crash/restart and local atomic-visibility capability has physical CI evidence. Synchronous replication, standby promotion, failover, backup/restore, production storage semantics, actual Canonical Authority deployment configuration and named human on-call operator remain NOT VERIFIED / OPEN. wal_level=replica is not replication proof.

Accountable technical role for the candidate qualification is Storage DB Platform Operator; the actual production on-call identity is not designated. Gate B remains blocked pending full Gate A. Gate C remains blocked pending Gate B. JF-10 P0 remains OPEN; no production activation is authorized.


## 13. Gate A — PostgreSQL 18.7 synchronous standby promotion evidence (2026-11-17)

Storage has now executed the two-node physical failover probe on the exact pinned image digest.

- Probe Blob: 23d8ea8546932e592093c5c17cd2b52f8a294720
- Workflow Blob: f3c05f90c6065458b49879def10dce672685c850
- Successful run: 43908428220
- Run commit: 7cd416a1f80364fe7de316f19716325b6503cbfa
- Job: 133443444760
- Topology: one PostgreSQL 18.7 primary + one physical streaming standby; primary configured synchronous_commit=remote_apply and synchronous_standby_names=FIRST 1 (jf10_standby); standby confirmed streaming/sync before PREPARE.

The run proved that the prepared WAL was synchronously replayed, publication remained private on the hot standby, the primary was hard-killed, the standby was promoted, the same prepared XID became available after promotion recovery, the prepared row lock remained held, and COMMIT PREPARED on the original XID atomically exposed the visibility pointer and publication receipt.

**Gate A remains PARTIAL PASS / OPEN.** PostgreSQL intentionally hides pg_prepared_xacts during hot-standby recovery; recovery of the prepared transaction is inspected and resolved only after promotion completes. The dossier records this behavior and exact evidence.

Still open: rollback-after-promotion, backup/restore and point-in-time recovery, control-ledger replay before serving restored data, real host/zone/storage failure semantics, actual Canonical Authority deployment, production failover fencing/routing, human on-call/operator designation and RPO/RTO. The CI promotion command is not a production HA manager. Gate B and C remain blocked; JF-10 P0 OPEN; production activation NOT AUTHORIZED.


## 14. Gate A — rollback-after-promotion PASS (2026-11-17)

Storage extended the two-node PostgreSQL 18.7 failover probe to prepare two independent XIDs before primary loss, then resolve one by COMMIT PREPARED and the other by ROLLBACK PREPARED after standby promotion.

- Probe Blob: cbe1f317479145dbf1467e426b0c0737a6ec054c
- Workflow Blob: f3c05f90c6065458b49879def10dce672685c850
- Successful run: 43908746695
- Run commit: b59c0842dba86b581ded4d9519c4289b6a699fde
- Job ID: 133444572245

Both prepared XIDs were synchronously replayed to the standby. After primary SIGKILL and promotion, both exact XIDs were recoverable; both locks remained held. The promoted standby committed one participant (pointer + receipt visible together) and rolled back the other (neither visible).

**This closes the rollback-after-promotion subtest for the pinned CI profile. Gate A remains PARTIAL PASS / OPEN** because backup/restore + PITR, Forget-control-ledger reconciliation before restored reads, real host/zone/storage durability, production failover fencing/routing, actual Canonical Authority deployment and named human operator/RPO/RTO remain open. Gate B/C remain blocked; JF-10 P0 OPEN; production activation NOT AUTHORIZED.


## 15. Gate A — physical backup/restore and stale-control gate PASS (2026-11-17)

Storage executed a PostgreSQL 18.7 physical pg_basebackup/restore probe while a participant XID was prepared and a previously visible artifact remained in the backup snapshot.

- Probe Blob: 81072ea2411af12f29c7a7a4d984df3f870321ca
- Workflow Blob: 38369ed197665c4ed99a9ba30602cb5e3b04ba75
- Successful run: 43909138634
- Run commit: 62033b9f90a28c4afdea07fafa0f575342b084e9
- Job ID: 133445937783

The run proved the prepared XID survived physical backup/restore and could be committed by the same XID; the prepared visibility pointer and receipt remained private. A restored snapshot with local control epoch 0 failed closed against required authoritative epoch 1; the newer Forget-control state was replayed before reads; the forgotten artifact was suppressed while an unrelated artifact remained readable.

**Gate A remains PARTIAL PASS / OPEN.** This CI test uses a fixture to represent the external I/D Forget-control ledger and does not prove production integration with those services. Remaining: actual host/zone/storage durability, production failover fencing/routing, exact Canonical Authority deployment profile, named human on-call/operator, approved runbooks and RPO/RTO. Gate B/C remain blocked; JF-10 P0 OPEN; production activation NOT AUTHORIZED.


## Gate A — coordinator crash-window / unrecorded-ACK recovery PASS (2026-11-17)

Storage executed a separate PostgreSQL 18.7 probe in which a coordinator child process dies after participant PREPARE / COMMIT PREPARED / ROLLBACK PREPARED succeeds but before the coordinator records the acknowledgement in its durable test ledger.

- Probe Blob: 51cf8c7a9fa169aff8b0a5fd8a7ec5f934ad35a2
- Workflow Blob: 7b612223f309ef0b963d262a94845a083e79ec7c
- Successful run: 43912857694
- Run commit: 5f342adb95f95208e8f1e2cc52538cf0944aa9e3
- Job: 133459107145

The recovery process reconciled the exact original XID without allocating a new one. PREPARE ambiguity retained private visibility and the prepared lock; COMMIT ambiguity reconciled to pointer + receipt visible together; ROLLBACK ambiguity reconciled to neither visible.

**Important scope:** this is a deterministic coordinator process-crash / unrecorded-checkpoint test, not a TCP packet-drop test or production I sequencer/COC test. Its SQLite ledger is a test fixture. Gate A remains PARTIAL PASS / OPEN; production deployment binding, real I/D ledger integration, production fencing, host/zone durability, human operator, runbook and RPO/RTO remain open. Gate B/C remain blocked.


## Gate A — real PostgreSQL TCP ACK-loss recovery PASS (2026-11-17)

Storage added a one-shot TCP proxy that drops the PostgreSQL CommandComplete response frame after the server executes PREPARE TRANSACTION, COMMIT PREPARED or ROLLBACK PREPARED. The client sees a broken connection / UNKNOWN; recovery reconnects and reconciles the same original XID.

- Probe Blob: db843927fb3fd2f37b15b7a56dee5ca4c9b4274c
- Workflow Blob: ae9cea590721630f3ebad6d9566de79ac188fd23
- Successful run: 43913477785
- Run commit: 9f3f9595fa5fec6003ece53bb289a5ff499f87ee
- Job: 133461308120

PASS: client-observed UNKNOWN after PREPARE, COMMIT PREPARED and ROLLBACK PREPARED; exact prepared XID recovered after PREPARE response loss; COMMIT response loss reconciled to pointer + receipt together; ROLLBACK response loss reconciled to neither visible.

This is actual PostgreSQL protocol TCP response-loss fault injection at the CommandComplete boundary, not merely an application result suppressed after receipt. Scope is single-node PostgreSQL 18.7 CI; it does not prove production I sequencer/COC integration, coordinator quorum durability, cross-zone network partition behavior, production fencing or deployment readiness.

Gate A remains PARTIAL PASS / OPEN at production binding. Gate B/C remain blocked.
