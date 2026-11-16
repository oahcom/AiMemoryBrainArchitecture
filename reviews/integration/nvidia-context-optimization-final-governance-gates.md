# NVIDIA Context Optimization — Final Governance Gates

- Owner: A — Principal Integration Architect
- Date: 2026-11-17
- Evidence state: architecture design plus bounded CI/model evidence; no end-to-end runtime certification

## 1. Gate summary

| Gate | Status | Rationale | Required exit evidence |
|---|---|---|---|
| Domain Contract | CONDITIONAL | B accepts typed domain/reference boundary with conditions; domain vocabulary/TSS mapping and exact wire semantics remain open | B semantic addendum; exact typed reference and temporal/epistemic mappings accepted |
| Archive Contract | CONDITIONAL | F accepts Archive/Recall ownership with conditions; schema, retention, D/I enforcement and restore proof open | F/G/B/H/I/D exact Recall contract; producer classification; archive read/cache/restore conformance |
| Context Contract | CONDITIONAL | G accepts Context/TSS/compaction direction with conditions; TSS fields, fidelity vetoes, lineage and transitive Forget proof open | G exact Context/TSS/lineage contract; B/C/D/F/I/H review; CAS and stale-source tests |
| Agent Applied Contract | CONDITIONAL | CGH-APPLIED-1.1 exact owner matrix records design-level acceptance with enumerated exceptions; H schema remains candidate, C provider-specific idempotency and G Applied persistence unverified; Issue #3 open | Close Issue #3 with exact residual decisions; versioned schema/IDL and provider evidence; final-request, supersession and reconnect tests |
| Compiler Publication Contract | CONDITIONAL | E accepts authority separation; D/E/Storage atomic gate and JF-10 runtime remain open | D/E/Storage exact gate contract; I sequencer acceptance; complete dependency and receipt recovery tests |
| BMCP Protocol Contract | CONDITIONAL | H accepts message-family semantics and a schema candidate; generated wire/IDL, parser, crypto/channel binding and interoperability not complete | H versioned schemas/IDL; B type mapping; C/G/I/D/F review; parser, idempotency, timeout and reconnect tests |
| Security & Permission Contract | BLOCKED | I security boundary conditionally accepted, but global inventory/seal and external governance approvals remain blocked; Issue #4 and JF-10 consumer integration open | I effective governance decisions and authenticated inventory/seal; D/I currentness proof; owner gate sequencer and restore tests |
| Forget Atomicity | BLOCKED | No joined F/G/D/E/H/C/I/Storage proof; negative suites not run end-to-end | Fault-injection suite with zero post-fence disclosure, stale replay and false completion |
| PITR / Restore Safety | BLOCKED | Restore/PITR design and bounded PostgreSQL capability tests exist; no project deployment binding or integrated D/I/Archive/Context restore proof | Production-equivalent backup/PITR/restore tests; WAL gap negatives; independent D/I high-water and quarantine/release receipts |
| Negative Conformance Tests | BLOCKED | Owner negative suites and A conformance plan remain NOT RUN as integrated tests; bounded CI/model suites do not satisfy end-to-end gates | Executed owner-owned suites with pinned build/config, traces, readbacks and independent review |
| Interface Freeze | BLOCKED | NVIDIA package Owners all conditional; CGH-APPLIED and COC matrices are design-level only with exceptions; Issue #3/#4, JF-10 P0 and domain schema ADR remain open | All required Owners accept exact same immutable contract revision; no P0; schemas/errors/idempotency/concurrency/recovery and negative tests accepted |
| Rust Implementation Authorization | BLOCKED | No interface freeze, JF-10 production proof, end-to-end Forget/Restore evidence or completed governance | Separate A authorization after all prior gates pass and accountable engineering/deployment owners are assigned |

## 2. Forget end-to-end gate

| Stage | Owner | Preconditions / authoritative state | Allowed | Prohibited | Recovery behavior | Required evidence | Test status |
|---|---|---|---|---|---|---|---|
| Capture | F; D/I dependencies | Authenticated Producer/Principal; trusted Scope; I PermissionEpoch; D producer registration and fence | Admit classified work with stable work ID into private staging | Unknown producer, stale auth, post-fence publication, implicit canonical registration | Reconcile same work ID; quarantine uncertain manifest/blob | producer identity, scope, epoch, D fence/high-water, work ID, manifest/hash, gate trace | NOT RUN |
| Archive | F | Immutable F revision/manifest; I retention/permission; D fence for D-covered lineage | Immutable blob/revision, locator and catalog/index under policy | Mutable revision, locator-as-grant, unclassified derivative/replica | Orphan bytes remain non-queryable; quarantine until manifest/lineage reconciled | manifest/blob hash, source revision, registration, retention class, storage receipt | NOT RUN |
| Recall | F; G intent; I/D checks | Bounded G RecallIntent; authenticated Principal/Scope; current I epoch and D fence | Exact bounded page reads; F receipt and completeness | Cross-session cursor, stale revision, false COMPLETE, receipt-as-authorization | Cancel, invalidate cursor, discard staged bytes on fence/revoke | per-page permission/fence checkpoint, selector/range, hash, receipt, completeness, cursor binding | NOT RUN |
| Cache Fill / Hit | F; I/D | Source lineage and current I/D state at admission and atomic publish/hit | Publish only after final currentness gate | Late pre-fence fill, stale cache hit, cached ALLOW without approved guarantee | Reject late fill; invalidate hits/session/cursors; fail closed | fill work ID, source digest, fence/epoch, publication CAS and hit-denial traces | NOT RUN |
| Context Selection | G; B/F/I/D | F RecallResult; exact source revision/receipt; B semantics; I/D currentness | Stage typed ContextObservationReference and candidate membership | Treat receipt as truth; silently rebind source; promote to canonical | Mark stale/suppressed; new ContextVersion only after revalidation | ContextId/version, source refs/revisions, selector decision, permission/fence checkpoint | NOT RUN |
| Compaction | G; B/C/F/D/I | Current source set, TSS schema, fidelity vetoes, transitive lineage, cost telemetry | Stage candidate; CAS commit after revalidation | Reintroduce forgotten ancestor; epistemic upgrade; discard critical constraints; retain forgotten plaintext | Abort candidate; prior Context remains authoritative; rehydrate only authorized retained source | decision/economic inputs, fidelity report, lineage/loss ledger, CAS and dependency checks | NOT RUN |
| Delivery | G/H/C; I/D | Exact ContextVersion, DeliveryIntent, current I/D, Adapter capability | Deliver immutable target; record stage-specific ACK | ACK-as-Applied; stale target; partial materialization as Full | Stable DeliveryId, new AttemptId, reconcile UNKNOWN; supersede stale version | payload digest, delivery/attempt IDs, H ACK stage, C materialization and final request proof | NOT RUN |
| Offline Reconnect | H/C/G; I/D | Fresh authenticated session, current I PermissionEpoch and D fence, target/version reconciliation | Suppress local data first; fetch authorized Snapshot or contiguous Delta | Replay old queue/cache before checks; offline lease or stale epoch grace | Keep content suppressed and state UNKNOWN until authorities resolve | session, epoch/fence readback, queue suppression, stale cursor rejection, snapshot/delta proof | NOT RUN |
| Archive Restore / PITR | Storage; D/I/F/G | Integrity and WAL continuity; independent D fence/lineage high-water; I epoch/revocation and inventory seal | Quarantine until every owner receipt and coverage proof exists | Queryability before fence/permission/inventory replay; partial WAL restore | Missing/corrupt/incomplete prefix => RESTORE_FENCED; no heuristic recovery | restore ID, snapshot/WAL manifest, cutoff, high-water, inventory seal, quarantine/release receipts | NOT RUN |
| Snapshot / Delta Replay | D/G/H/I/F | Current fence/epoch, matching base version, contiguous authorized event range | Replay only after suppression and current authority; new ContextVersion as needed | Stale snapshot, gap, cursor substitution, old derived payload reactivation | Stop at first gap/mismatch; reconcile fresh snapshot; remain suppressed if unknown | base/target versions, sequence/cursor types, event digest, fence/epoch, replay receipt | NOT RUN |

## 3. JF-10 / COC / PITR sub-gates

### 3.1 Design status

- CGH-APPLIED-1.1 / JF-10 bridge: exact owner design decisions recorded with enumerated exceptions; single-I-PolicyDomain only.
- COC durable protocol Gate B: exact Owner review complete with enumerated exceptions; specification accepted at design level, not implemented.
- JF-10 P0: OPEN. COC quorum implementation, I sequencer, D fence ledger, E producer ledger, Storage prepared participant integration and Gate C remain unverified.
- Multi-I-PolicyDomain atomicity: BLOCKED / NOT ACCEPTED.
- Project production Canonical Authority deployment: NOT DESIGNATED.

### 3.2 Bounded CI evidence

The following seven PostgreSQL 18.7 capability workflows were independently read back as completed/success:
- `43958775001` — PITR prepared-XID atomicity and Archive negatives.
- `43959079736` — Prepared-XID capability.
- `43959079669` — Synchronous failover capability.
- `43959079703` — Backup/restore capability.
- `43959079745` — WAL archive PITR.
- `43959079760` — Synchronous standby unavailable fail-closed.
- `43959079930` — Fenced old-primary rewind/rejoin.

Also completed successfully:
- `43897364938` — COC in-memory outage-recovery reference model.
- `43905568915` — JF-10/COC semantic conformance validator.

These establish only the pinned CI capability/model results. They do not establish a live COC quorum, real I sequencer, D ledger, E producer service, Storage participant integration, production deployment, end-to-end Archive Restore or full JF10-01..17 conformance.

### 3.3 Required fail-closed recovery

- Recovery Cutoff Batch must bind authoritative COC/log high-water and owner-local evidence; no owner infers terminal order from wall clock alone.
- Owner-local Gate validates exact operation identity/digest, participant/XID, D fence/lineage, I authorization/inventory seal and Storage visibility state before exposure.
- Same-XID recovery is mandatory for a prepared participant. New-XID retry cannot replace unresolved operation identity.
- I sequencer decision and Storage VisibilityPointer/PublicationReceipt must be causally reconciled. I COMMIT alone is not reader visibility.
- WAL missing/corrupt/incomplete, control ledger unavailable, prepared XID unresolved or authority disagreement means quarantine/private bytes and blocked readers.
- No heuristic commit/abort, TTL expiry, stale replica read, missing row or ACK loss may be interpreted as success.

## 4. Evidence classification

| Evidence | Establishes | Does not establish |
|---|---|---|
| Owner ACCEPT WITH CONDITIONS | Bounded decision on exact artifacts | Unconditional acceptance, tests, implementation or freeze |
| Architecture protocol | Specified safety model | Implementation or runtime behavior |
| In-memory reference-model CI | Modeled state-machine assertions | Real DB durability, I sequencer, XID recovery, HA/PITR or Archive Restore |
| PostgreSQL 18.7 capability CI | Tested database capability in pinned CI profile | Designated project deployment or full JF-10 |
| Restore design / conformance plan | Required restore procedure/tests | Passed integrated restore/PITR |
| ReadReceipt / ACK | F returned bytes / transport stage accepted | Semantic truth, Context Applied or canonical publication |

## 5. Exit rule

No gate is upgraded by narrative, branch existence, a green bounded CI job or another Owner's approval. Each Owner produces its own exact-version acceptance and evidence. A records global disposition without changing underlying authority.
