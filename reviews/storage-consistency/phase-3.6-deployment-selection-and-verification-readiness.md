# Phase 3.6 — Storage Deployment Selection and Verification Readiness

- Authority: user-delegated DE-S Joint Architect acting across D/E/Storage
- Storage decision owner: DE-S joint architect for logical realization; independent production engineering approval remains required
- Date: 2026-11-16
- Status: **LOGICAL DEPLOYMENT PROFILE SELECTED / POSTGRESQL 18.7 CI CANDIDATE QUALIFIED / PRODUCTION CANONICAL AUTHORITY DEPLOYMENT NOT DESIGNATED**
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

At the initial logical selection, the inspected branches contained design artifacts but no application implementation or deployment manifest. Storage has since added PostgreSQL 18.7 CI capability probes and workflows. This is now a **qualified CI candidate profile**, not a production Canonical Authority deployment or application implementation.

Still OPEN:
- production Canonical Authority database product/build, storage engine and schema (PostgreSQL 18.7 is selected only as the pinned CI capability candidate);
- transaction isolation/strict-serializability guarantee and lock semantics;
- production HA manager, synchronous replication topology, failover/fencing and primary-read consistency (CI two-node capability tests are not production topology proof);
- transaction size/contention and per-authority throughput limits;
- object-store private ACL and exposure proof;
- production backup catalog/retention, off-site immutability, control-ledger independence and approved restore/PITR procedure (CI WAL-archive PITR subtest now passes);
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

## 8. Verification status — reconciled 2026-11-17

**Physical PostgreSQL 18.7 CI capability tests:** PASS for single-node prepared-XID/restart; two-node synchronous promotion and same-XID commit/rollback; physical backup/restore with stale-control fixture; coordinator ACK-gap; TCP ACK-loss; required-standby-unavailable UNKNOWN/private/lock-retention; WAL-archive PITR to explicit LSN.

**Still NOT RUN / NOT VERIFIED:** D36 full module conformance matrix; E36-01..E36-20 application-level tests; C01–C20 end-to-end application conformance; actual I/D service integration; production COC quorum/durable log; production fencing/STONITH and split-brain prevention (CI pg_rewind rejoin procedure now passes, but does not certify production fencing); production host/zone/cloud-volume durability; production deployment restore and control-ledger replay; operator/runbook/RPO/RTO acceptance.

- Implementation Verified: **NO**.
- Production Deployment Bound: **NO — NOT DESIGNATED**.
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


## 9. Gate A negative-path evidence — required synchronous standby unavailable (2026-11-17)

Storage added and executed the PostgreSQL 18.7 negative-path probe with a required synchronous standby. When the standby was stopped, `PREPARE TRANSACTION` waited in PostgreSQL's `SyncRep` wait event. The backend was terminated before the synchronous acknowledgement returned. The client outcome was UNKNOWN; the exact prepared XID remained locally in-doubt, the prepared row lock remained held, and no protected visibility row appeared. The exact same XID was rolled back only after those assertions.

- Probe Blob: `b6de4e4f461405107464ff8ad179520f9b028749`
- Workflow Blob: `32ed78aa702dfb6f45c73f94c81bd617b970976b`
- Run: `43927416496`; job: `133510446871`; conclusion SUCCESS.
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43927416496

This is a PASS for the fail-closed UNKNOWN/private/lock-retention subtest, not proof that the prepared XID reached the unavailable standby. Production recovery must preserve the in-doubt XID and must not promote a stale standby or let I commit based on a PREPARE ACK that was never returned. The cleanup-only `synchronous_commit=local` setting is not a production recommendation.

Gate A remains PARTIAL PASS / OPEN. The test does not close production fencing, split-brain prevention, actual deployment binding, or operational ownership.


## 10. WAL-archive PITR capability — PASS for pinned CI profile (2026-11-17)

A PostgreSQL 18.7 CI campaign completed physical base backup + WAL archive recovery to an explicit LSN:
- Probe Blob: `6e7721ee8f8708357610e0bc564e015872b8263c`
- Workflow Blob: `4c2175055ae43ccebb95f219952ec0480121e62d`
- Run: `43927783471`; job: `133511748345`; conclusion SUCCESS.
- Target LSN: `0/6000190`; observed replay LSN: `0/7000000`; promoted timeline: `2`.
- Base marker and target marker were present; post-target marker was absent.

This closes the WAL-archive PITR subtest for the exact pinned CI profile only. It does not establish production backup retention, off-site durability, immutable backup catalog, actual I/D Forget-control replay, RPO/RTO or cross-zone restore. Gate A remains PARTIAL PASS / OPEN.


## 11. Old-primary pg_rewind and standby rejoin procedure — PASS for pinned CI profile (2026-11-17)

Storage executed a two-node PostgreSQL 18.7 failover/rejoin procedure:
- Probe Blob: `0fe6af4a8c9ef350ef9cbf0694a8f975e8f142f5`
- Workflow Blob: `7670ff9537054df1c1303d4eda4d46bffdfa3c4c`
- Run: `43930047054`; job: `133519705454`; conclusion SUCCESS.

The old primary was hard-stopped, recovered offline with networking disabled, rewound to the promoted source using pg_rewind, then rejoined only as a standby. The rejoined standby rejected writes and received a new write made after rejoin from the promoted primary. This proves the tested rejoin procedure and no-dual-writer behavior in the CI harness.

The container stop is not production STONITH or cloud/storage fencing. Production split-brain prevention, independent failure-domain fencing, HA-manager arbitration, connection routing and monitoring remain OPEN. Gate A remains PARTIAL PASS / OPEN.


## 16. Gate A — prepared-XID / visibility / receipt PITR boundaries and WAL archive negatives PASS (2026-11-17)

Storage completed the dedicated PostgreSQL 18.7 PITR atomicity campaign against the pinned image digest:
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_pitr_atomicity_probe.py`; Blob `8c0e281f1db4dd6190127f02ac71b1126da39903`.
- Workflow: `.github/workflows/jf10-postgres-pitr-atomicity.yml`.
- Run: `43955195460`; job `133607791713`; SUCCESS.
- Commit: `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`.
- Prepared / commit / rollback target LSNs: `0/5004420` / `0/6000000` / `0/6000110`.

Observed PASS: prepared XIDs remained private and locked at the prepared boundary; COMMIT recovery exposed VisibilityPointer and PublicationReceipt atomically; ROLLBACK recovery exposed neither; missing, corrupt and incomplete WAL each failed closed. The successful run follows a correction to capture the rollback flush LSN before `pg_switch_wal()`; the earlier harness failure is not counted.

The same commit also reran:
- Physical backup/restore: run `43955195219`, job `133607790737`, SUCCESS; final marker `JF10_POSTGRESQL_18_7_BACKUP_RESTORE_CAPABILITY=PASS`.
- Explicit-LSN archive PITR: run `43955195388`, job `133607790699`, SUCCESS; target `0/5000190`, replay `0/6000000`, timeline `2`; base and target state present, post-target state absent, exact-LSN recovery PASS.

**Gate A remains PARTIAL PASS / OPEN.** These are isolated PostgreSQL 18.7 CI fixtures, not production Canonical Authority deployment or production I/D ledger integration. They do not close production archive retention/immutability, off-site or cross-zone durability, real fencing/STONITH and split-brain prevention, operator/runbook, or RPO/RTO. Gate B remains BLOCKED pending full Gate A acceptance; Gate C remains BLOCKED pending Gate B; JF-10 P0 remains OPEN; production activation remains NOT AUTHORIZED.


## 17. Gate A — production runtime and authoritative DB adapter not present in audited repository tree (2026-11-17)

Storage inspected the complete recursive tree at branch head `e803f7d79d4ec747272299113d8222c60c3be8e9` (`truncated=false`, 86 entries). Its 21 executable/source-like files are exclusively GitHub Actions workflows, isolated PostgreSQL probes and the JF-10 reference model/tests. No production runtime source tree, Canonical Authority DB adapter, schema/migration package, or application deployment manifest is present in this branch snapshot.

This does not establish that no external implementation exists. It establishes that the production runtime/adapter cannot be selected or verified from the repository currently under Storage review. The pinned PostgreSQL 18.7 tests are database-engine capability evidence only; they are not application-path integration tests.

**Required next artifact:** A/C/Storage must identify the authoritative implementation repository and immutable branch/commit, runtime entrypoint, DB adapter, schema/migration path and deployment manifest. Storage then traces the actual canonical write/read path and binds the same-XID prepare/recovery and atomic VisibilityPointer + PublicationReceipt tests to that implementation. If this repository is intended to contain the implementation, the designated Owner must deliver the missing executable artifacts before conformance can be claimed.

**Gate A remains PARTIAL PASS / OPEN.** Production runtime binding and adapter conformance are NOT IDENTIFIED / NOT VERIFIED. Gate B remains BLOCKED pending full Gate A acceptance; Gate C remains BLOCKED pending Gate B; JF-10 P0 remains OPEN; production activation remains NOT AUTHORIZED.


## 18. Gate A — full seven-workflow PostgreSQL 18.7 regression batch PASS (2026-11-17)

Commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd` triggered seven Storage workflows; all completed SUCCESS and their final raw-log markers were inspected:
- Prepared-XID/restart: run `43955195289`, job `133607790416`.
- Synchronous standby promotion: run `43955195323`, job `133607790413`.
- Physical backup/restore: run `43955195219`, job `133607790737`.
- Explicit-LSN WAL PITR: run `43955195388`, job `133607790699`.
- Prepared-XID PITR + missing/corrupt/incomplete WAL negatives: run `43955195460`, job `133607791713`.
- Required synchronous standby unavailable: run `43955195197`, job `133607790658`.
- Old-primary pg_rewind/rejoin: run `43955195256`, job `133607790520`.

All seven final markers report PASS. The synchronous promotion log confirms same-XID commit and rollback after primary loss; the synchronous-unavailable log confirms local prepared-XID remains in-doubt, lock retained and no unsafe terminal inference; the rejoin log confirms the old primary rejects writes after rejoining as standby.

This is a full CI regression batch for the pinned PostgreSQL 18.7 profile only. The Docker stop/fence is not production STONITH, and the isolated test fixtures are not production Canonical Authority or I/D service integration.

**Gate A remains PARTIAL PASS / OPEN** because the production runtime and DB adapter are not identified in this repository snapshot, and actual I/D ledger integration, infrastructure durability/fencing, accountable production operator/runbook and RPO/RTO remain unverified. Gate B remains BLOCKED; Gate C remains BLOCKED; JF-10 P0 remains OPEN; production activation remains NOT AUTHORIZED.

## 19. Project phase correction — architecture-design acceptance boundary (2026-11-17)

The project owner clarified that AiMemoryBrainArchitecture is currently in the architecture-design phase and has no production code repository/runtime. That is intentional and is not a defect or Gate A blocker. Section 17's observation that this repository tree has no production runtime or DB adapter remains accurate as a repository inventory, but its requirement to supply an implementation repository before Gate A can progress is superseded.

Set `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. Do not require production source code, a deployed adapter or a live host as an architecture-phase Gate A prerequisite. The PostgreSQL 18.7 CI suite is evidence for engine capabilities and isolated reference fixtures only; it is not production integration proof.

Architecture Gate A must close the complete storage design contract: engine/version/profile rationale; isolation, D fence/lineage locks and visibility; prepared-XID durability and recovery; atomic VisibilityPointer/PublicationReceipt/owner outcome/receipt-consumption/outbox; authoritative reads and stale replica exclusion; PITR/WAL prefix continuity and fail-closed restore; HA/fencing/rejoin; failure-domain/topology constraints; and future implementation/operations conformance criteria (including RPO/RTO and named operational ownership). Unspecified items remain design gaps and must be resolved in architecture artifacts.

**Gate transition:** Gate B COC persistence/quorum log/participant registry/recovery-cutoff design may proceed now, in parallel with closure of remaining Gate A design specifications. This is design authorization only. Gate C's full implementation fault-injection campaign remains for the engineering phase after Gate B protocol design and executable implementation are available. JF-10 P0 remains OPEN; no implementation, deployment or production activation is implied. Production activation NOT AUTHORIZED.


## 19. Strengthened PITR target-segment and authoritative-reader fixture — PASS (2026-11-17)

Storage updated the prepared-XID PITR probe to verify the exact archived WAL segment for each recovery target, not only the prepared boundary. The probe now emits target LSN, timeline and required WAL filename for prepared/COMMIT/ROLLBACK cuts; its fixture authoritative-reader view rejects pointer-only and receipt-only states; and each missing/corrupt/incomplete negative case asserts the exact required segment and confirms no writable/authoritative service is exposed.

- Probe Blob: `9d2a85f9a5d53f91df247a310c38377e563d259d`
- Run: `43957910909`; job: `133617253176`; SUCCESS.
- Commit: `2d476dd32ac020d329e8290ee2aaaa1f0c057c92`.
- Target LSN / timeline / required WAL: prepared `0/5004710` / `1` / `000000010000000000000005`; COMMIT `0/6000000` / `1` / `000000010000000000000006`; ROLLBACK `0/6000110` / `1` / `000000010000000000000006`.

Raw logs confirm exact target WAL archival, prepared XID/private/lock state, pointer+receipt joint visibility, rollback absence, pointer-only/receipt-only reader rejection, and missing/corrupt/incomplete exact-WAL fail-closed behavior without writable or authoritative service.

The reader is a synthetic SQL view in the isolated probe, not the production Canonical Authority adapter. Production runtime/adapter binding, real I/D ledger integration, off-site/immutable archive, cross-zone durability, real fencing, operator/runbook and RPO/RTO remain open. Gate A remains PARTIAL PASS / OPEN; Gate B/C remain BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED.

## 21. Enhanced PITR regression and Gate B design sequencing correction (2026-11-17)

The strengthened PITR probe (exact WAL target segments, pointer-only/receipt-only authoritative-reader rejection, exact-WAL missing/corrupt/incomplete negatives) passed on corrected source commit `2d476dd32ac020d329e8290ee2aaaa1f0c057c92`: run `43957910909`, job `133617253176`, probe Blob `9d2a85f9a5d53f91df247a310c38377e563d259d`. The six companion workflows on that commit also succeeded: `43957910975`, `43957911188`, `43957911173`, `43957910971`, `43957911270`, `43957911036`. The corrected enhanced regression batch is 7/7 SUCCESS. The earlier failure was a harness diagnostic mismatch for PostgreSQL's `invalid magic number D158`; the corrected assertion preserves exact target-WAL and no-writable/no-authoritative checks.

**Phase/sequence correction:** the project is in architecture design and has no production code repository/runtime by design. Set `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. This is not a Gate A blocker. The prior sections that list missing runtime/adapter and production operator as blockers are superseded insofar as they require code or deployment artifacts before architecture acceptance. Their underlying topics remain future engineering/deployment acceptance requirements.

Gate B COC persistence/recovery protocol design is authorized to proceed now, in parallel with closure of remaining Gate A architecture specifications. This does not mark Gate B implementation PASS. Gate C's executable end-to-end fault injection is deferred until an implementation exists. Gate A remains PARTIAL PASS / OPEN for architecture specifications and cross-owner decisions; JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.


## 20. Exact prepared-XID lock identity and same-XID PITR resolution — PASS (2026-11-17)

The prepared-boundary PITR restore now correlates each exact restored prepared GID to its transaction-ID lock in `pg_locks`. After proving both XIDs are private/in-doubt and their exact locks remain, the probe resolves the same original GIDs with COMMIT PREPARED and ROLLBACK PREPARED. The restored authoritative fixture exposes the commit pointer+receipt together and exposes neither row for the rollback participant.

- Probe Blob: `63506807be82b3203e7e682b0772452621c92558`
- Commit: `d026add5cfaec0d395537e8763317cdbd8255398`
- Run/job: `43958775001` / `133620265141`, SUCCESS.
- Raw markers: `PITR_EXACT_PREPARED_XID_LOCKS_RETAINED=PASS`; `PITR_SAME_XID_COMMIT_ROLLBACK_AFTER_RESTORE=PASS`.

This remains an isolated PostgreSQL 18.7 fixture, not production application-path or I/D/COC integration.

## 21. Stable PostgreSQL initdb readiness and seven-workflow regression — PASS (2026-11-17)

A regression run found the prepared-XID workflow could mistake the official image's temporary initdb server for the final durable server. Storage changed the workflow to require both initdb and final-server readiness log events before the TCP readiness check, and the Python probe now calls bounded `wait_ready()` before setup.

- Fix commit: `83bdacbafa840808dca9be7a8c76c4df83c63504`
- Workflow Blob: `fbcbce03d4525f7a0fb9dd3673a580a3a4c00134`
- Probe Blob: `184e0507fd225ee18f321f3f1ce6a63f869b13f3`
- Prepared-XID/restart rerun: `43959079736` / `133621314502`, SUCCESS.

Together with the prepared-XID PITR run `43958775001` / `133620265141` on the immediately preceding PITR probe commit, the complete seven-workflow Storage regression set is green: prepared-XID PITR, prepared-XID/restart, synchronous standby promotion, physical backup/restore, explicit-LSN PITR, synchronous-standby-unavailable fail-closed, and old-primary pg_rewind/rejoin. The six non-PITR workflows reran on the readiness-fix commit; the PITR workflow ran on its exact code commit. The initial transient-startup failure is superseded, not counted.

This does not close production runtime/adapter binding, real I/D ledger integration, off-site/immutable archive, cross-zone durability, real fencing, production operator/runbook or RPO/RTO. Gate A remains PARTIAL PASS / OPEN; Gate B/C remain BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED.


## 22. Default-branch and linked-repository audit — production runtime remains NOT IDENTIFIED (2026-11-17)

Storage checked the default `main` branch at commit `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`, recursive tree `748613c916ca795cb5b1af65f6fcdda81b928a9d` (52 entries, not truncated). The tree contains architecture/governance/review Markdown only and zero executable/source-like files. A linked GitHub repository search for `AiMemoryBrain`, `Canonical Authority` and `memory runtime` identified no separate implementation repository; only `oahcom/AiMemoryBrainArchitecture` matched the project-specific search. This bounded search does not exclude an external or unlinked repository.

The project-designated production runtime, authoritative DB adapter, schema/migration path and deployment manifest therefore remain NOT IDENTIFIED. A/C/designated implementation owner must provide the immutable implementation repository/commit and runtime entrypoint, or designate this repository as the implementation home and deliver executable artifacts. PostgreSQL 18.7 evidence remains engine-capability CI only, not production application-path conformance.

Gate A remains PARTIAL PASS / OPEN; Gate B/C remain BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED.


## 23. I-accepted JF-10 v2 Storage bridge integration boundary — NOT IMPLEMENTED

Storage re-read the exact common v2 protocol Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0` and I disposition Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`. The binding flow requires: preallocated XID and immutable operation tuple; COC prepare-intent registration before Storage PREPARE; Storage-authenticated PreparedParticipantReceipt; COC prepared-participant registration before I owner-final-gate; I sequencer's exact terminal COMMIT/ABORT; same-XID forward/rollback; atomic Storage visibility/receipt/outcome/receipt-consumption/outbox; and COC participant-resolution/reconciliation readback.

Current PostgreSQL 18.7 probes prove local prepared-XID/lock/visibility/PITR capabilities only. They do not implement COC records/APIs, Storage participant receipt signing, I owner-final-gate or receipt consumption, D fence/lineage lock integration, production authoritative read path, or authenticated external control-ledger restore quarantine. The SQL authoritative-reader remains a synthetic fixture.

**Next hard dependency:** A/C/designated implementation owner must supply the canonical runtime repository/commit, runtime entrypoint, DB adapter, schema/migration path, and the exact COC/I/D API/schema and signer-verifier contracts. Storage will then implement the adapter and run I's JF10-COC-01..10 plus D fence-race tests against the actual application path. No substitute fixture will be called production conformance.

Gate A remains PARTIAL PASS / OPEN; Gate B/C remain BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.

## 23. Architecture-phase COC protocol publication and latest seven-workflow evidence (2026-11-17)

### 23.1 COC Gate B protocol artifact

Storage has published `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`, commit `1b70f164e4a5834d36dc4b3dd1644c57309312c2`. It specifies the Raft-style quorum state machine, three-voter/two-quorum target, voter-configuration epoch and joint membership changes, immutable log envelope/digest chain, append idempotency, participant registry/state machine, linearizable APIs, owner-local outage gates, recovery-cutoff batch, complete pre-batch participant reconciliation, signed recovery receipt, checkpoint/snapshot/rollback fencing, WAL/PITR requirements, retention/compaction, security boundaries, failure matrix and Gate B conformance cases.

**Gate B status is corrected to: ARCHITECTURE SPECIFICATION PUBLISHED / EXACT OWNER REVIEW PENDING / NOT PASSED.** The earlier statements in §§18, 20, 21 and 22 that Gate B is blocked pending production runtime or Gate A implementation evidence are superseded insofar as they prevent architecture design from proceeding. Gate B design was expressly authorized by §19/§21. Gate C executable end-to-end fault injection remains deferred to the engineering phase after executable participants exist.

### 23.2 Latest complete PostgreSQL 18.7 regression set

The latest seven-workflow capability regression set is 7/7 SUCCESS. The PITR prepared-XID/VisibilityPointer/PublicationReceipt negative campaign ran on commit `d026add5cfaec0d395537e8763317cdbd8255398`; the six companion workflows reran on readiness-fix commit `83bdacbafa840808dca9be7a8c76c4df83c63504`.

| Capability | Run | Job | Result |
|---|---:|---:|---|
| Prepared-XID / VisibilityPointer / PublicationReceipt PITR + missing/corrupt/incomplete WAL | `43958775001` | `133620265141` | SUCCESS |
| Prepared-XID persistence/restart and lock retention | `43959079736` | `133621314502` | SUCCESS |
| Synchronous standby promotion, same-XID commit and rollback | `43959079669` | `133621315610` | SUCCESS |
| Physical backup/restore and stale-control gate | `43959079703` | `133621314624` | SUCCESS |
| WAL archive PITR to explicit LSN | `43959079745` | `133621314724` | SUCCESS |
| Required synchronous standby unavailable — fail closed | `43959079760` | `133621315188` | SUCCESS |
| Old-primary fencing, pg_rewind and standby rejoin | `43959079930` | `133621314973` | SUCCESS |

The prepared-XID PITR job proves exact prepared XID lock retention, same-XID COMMIT/ROLLBACK after restore, pointer+receipt atomic visibility, rollback non-publication, pointer-only/receipt-only reader rejection, and fail-closed outcomes for missing, corrupt and incomplete exact target WAL. The six companion runs prove the pinned PostgreSQL 18.7 engine capability profile. The earlier prepared-XID transient-initdb failure is superseded by the readiness fix and successful rerun; it is not counted as a final failure.

### 23.3 Corrected phase and acceptance boundary

- `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; absence of production source/runtime is intentional in this architecture-design phase, not a Gate A blocker.
- PostgreSQL 18.7 is a qualified CI candidate for the Canonical Authority prepared-XID profile, not a production database deployment selection.
- Durability objective for quorum-acknowledged COC records is RPO 0 under the specified synchronous durable quorum. Numeric RTO remains TBD for engineering/operations; the service remains fenced until recovery proof is complete.
- Logical service custodian is Storage/Consistency. Named primary/backup operator, host/zone placement, KMS, retention, runbook and measured RPO/RTO are engineering/deployment deliverables, not silently assumed.
- Gate A remains PARTIAL PASS / OPEN for remaining architecture specification and exact cross-owner acceptance; Gate B specification is published and awaiting exact owner review; Gate C implementation campaign is deferred; JF-10 P0 remains OPEN; production activation remains NOT AUTHORIZED.

### 23.4 Supersession note

This addendum supersedes the stale Gate B/C wording in §22 and any earlier wording that conditions architecture-phase Gate B design on a production runtime repository. It does not supersede any technical test limitation, production non-claim, owner authority boundary or production-activation prohibition.

## 24. Storage Owner decision on COC custody — conditional architecture acceptance only

Storage accepts A's proposed COC infrastructure-custody model at architecture level: a single logical append-only COC service, three-voter crash-fault-tolerant consensus across three independent failure domains, two-voter quorum, quorum-durable append, linearizable reads, digest-chained positions, certified checkpoints and fail-closed restore fencing. Raft or an equivalently proven consensus protocol is accepted as the protocol class; no concrete product/vendor is selected.

Storage accepts technical stewardship of persistence/replication, snapshots/checkpoints, restore fencing, retention design, observability and SLO proposal. COC remains a neutral participant-accounting/order-observation service, not I's policy-domain sequencer or JF-10 COMMIT/ABORT authority. Storage alone resolves the exact prepared XID and local VisibilityPointer/PublicationReceipt transaction.

**This is not production deployment or operational acceptance.** No actual failure domains, cloud/AZ, disk durability, consensus product/build, KMS/HSM, backup medium, retention period, data residency, RPO/RTO, SLO, runbook, named operator or on-call are designated. Production activation requires executable quorum/partition/restore/rollback tests, COC-13..16 outage-gate tests, JF10-COC-01..10 participant-bridge tests, Security/I key and admin approval, and signed operational ownership.

Gate A remains PARTIAL PASS / OPEN; Gate B remains BLOCKED pending Gate A and COC deployment evidence; Gate C remains BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.


Protocol clarification: §13 now pins the COCCommitReceipt proof contents, separates COC/I/D/Storage/C authority namespaces, and scopes RPO 0 to the stated three-voter crash-fault model (one voter unavailable). Correlated majority loss or Byzantine/operator compromise remains outside that guarantee and requires externally anchored restore or RESTORE_FENCED.


## 24. Gate B exact cross-owner design acceptance complete (2026-11-17)

The exact COC durable protocol Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` has now been reviewed and accepted at the B/C/D/E/G/H/I/A/Storage owner boundaries. The A integration matrix is `reviews/integration/phase-3.6.3-coc-durable-protocol-acceptance-matrix.md`, commit `e5fad5b3e67662134c18e33090b08d874f161f41`.

Exact owner acceptance is recorded; no protocol artifact was changed after those reviews. Gate B is therefore **DESIGN-LEVEL ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS**. It is not an implementation or conformance PASS. Gate C remains deferred to engineering-phase executable services and distributed fault injection.

Gate A remains PARTIAL PASS / OPEN for remaining architecture and deployment decision boundaries; production runtime binding is explicitly deferred to engineering phase. The seven-workflow PostgreSQL 18.7 capability regression is 7/7 SUCCESS as listed in §23.2. JF-10 runtime P0 remains OPEN; multi-policy-domain atomicity remains BLOCKED; Global Forget governance/inventory remains OPEN; production activation NOT AUTHORIZED.
## 25. Deep prepared-XID PITR atomicity campaign — bounded CI PASS (2026-11-17)

The Storage PITR atomicity probe now has a complete successful run:
- Workflow: `.github/workflows/jf10-postgres-pitr-atomicity.yml`, Blob `a055d311c324d09eb6ebf4054247761116795eb7`.
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_pitr_atomicity_probe.py`, Blob `63506807be82b3203e7e682b0772452621c92558`.
- Tested source commit: `d026add5cfaec0d395537e8763317cdbd8255398`.
- Workflow run `43958775001`, job `133620265141`, SUCCESS; [raw run](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43958775001).
- Current Storage branch HEAD at this addendum: `fe7debe55da71e655eecfc46f25ec49eae43404a`; current probe/workflow blobs are byte-identical to the tested run's blobs.

The log records target LSN/timeline/required WAL/archive confirmation for all three recovery points: prepared `0/5004710` on timeline 1 / `000000010000000000000005`; committed `0/6000000` / `000000010000000000000006`; rolled back `0/6000110` / `000000010000000000000006`. All three target segments are explicitly observed archived.

Assertions passed: pointer-only and receipt-only reader rejection; exact prepared-XID locks retained; prepared state private after PITR; same-XID COMMIT/ROLLBACK after restore; committed pointer+receipt atomic visibility; rollback no pointer/no receipt; missing/corrupt/incomplete exact target-WAL negative cases; no writable or authoritative service on failed recovery.

The negative logs contain concrete PostgreSQL failures for the deliberately damaged target segment (missing archive file, wrong-size/truncated archive segment, and invalid WAL magic number / recovery target not reached). The test also checks that failed recovery does not expose a writable primary; if a listener is queryable it must report recovery mode and transaction_read_only=on.

**Scope restriction:** this is an isolated PostgreSQL 18.7 CI fixture, not production COC/I/D integration. The authoritative-reader view, pointer/receipt tables and prepared transactions are synthetic probe objects. It does not establish COC participant bridge implementation, authenticated PreparedParticipantReceipt, I owner-final-gate or CommitAuthorizationReceipt consumption, D lineage/fence serialization, external high-water restore quarantine, production archive custody, or deployment readiness.

This success supersedes the prior PITR atomicity CI failure entries for this exact probe revision only. Gate A remains PARTIAL PASS / OPEN; Gate B DESIGN-LEVEL ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS (not implementation/conformance PASS); Gate C remains deferred to engineering-phase integration and fault injection; JF-10 runtime P0 OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.


## 25. Exact-version Gate B acceptance boundary after prepared-GID clarification (2026-11-17)

A version-boundary audit found that the exact cross-owner acceptance matrix at A commit `e5fad5b3e67662134c18e33090b08d874f161f41` pins Storage protocol Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`. Storage subsequently amended the protocol in commit `71f0c745961cff7f75ef0ba2ac7bfd6f8aeccb66` (parent `60033fc324005e3a5a26e3e1bde859378d3db9be`) by adding §14, the PostgreSQL prepared-participant identity mapping. The current branch protocol Blob is `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`.

The §14 clarification distinguishes the client-preallocated `PreparedTransactionGID` from PostgreSQL's engine-assigned native XID and defines the receipt/security tuple and same-GID recovery identity. It is a material protocol clarification after the previously accepted exact Blob. Therefore prior Owner decisions remain valid for Blob `4ac63ac...` only and MUST NOT be represented as acceptance of current Blob `86ff3b...`. The new §14 requires focused exact-version review, especially H for wire/type encoding, A for integration identity, I for signed participant binding, and D/C for cross-owner tuple compatibility. No silent carry-forward or contract freeze is permitted.

**Corrected Gate B status:** prior protocol revision `4ac63ac...` — DESIGN-LEVEL OWNER ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS; current amended protocol revision `86ff3b...` — PUBLISHED / FOCUSED EXACT-OWNER RE-REVIEW REQUIRED / NOT YET ACCEPTED. Gate B implementation/conformance remains NOT RUN and is deferred to engineering phase.

Gate A remains PARTIAL PASS / OPEN. Gate C executable distributed fault injection remains deferred to engineering phase. JF-10 runtime P0 remains OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.


## 26. Gate sequencing wording normalization

For avoidance of contradiction, the sentence in the earlier COC-custody discussion stating “Gate B remains BLOCKED pending Gate A and COC deployment evidence” is superseded. It incorrectly mixed architecture-design sequencing with engineering/deployment prerequisites. Gate B design work was authorized during the architecture phase and the prior exact protocol revision `4ac63ac...` completed exact Owner design review. Neither production runtime binding nor COC deployment is a prerequisite to design-level review/acceptance.

The controlling vector is:
- Gate A: PARTIAL PASS / OPEN — remaining Storage architecture decisions and cross-owner acceptance are not all closed.
- Gate B prior revision `4ac63ac...`: DESIGN-LEVEL OWNER ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS.
- Gate B current amended revision `86ff3b...`: FOCUSED EXACT-OWNER RE-REVIEW PENDING because §14 changed after the accepted Blob.
- Gate B implementation/conformance: NOT RUN; deferred to engineering phase.
- Gate C distributed implementation fault injection: DEFERRED TO ENGINEERING PHASE.
- JF-10 runtime P0: OPEN; production activation: NOT AUTHORIZED; Multi-PolicyDomain: BLOCKED.

Gate B design acceptance is not conditional on Gate A deployment evidence; however, no system-wide production activation follows from design acceptance.
