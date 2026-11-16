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
