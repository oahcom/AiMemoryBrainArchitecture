---
document_metadata:
  domain: consistency-recovery
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-098/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-098/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Candidate contract text only; no backend conformance, crash-recovery, power-loss, restore or production durability evidence is claimed."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "Storage/Consistency physical transaction, durability, visibility and recovery contract candidate"
    canonical_scope_id: "consistency-recovery/storage-physical-consistency"
    canonical_scope_keywords:
      - storage-atomicity
      - durability
      - crash-recovery
      - visibility
      - forget-fence-projection
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "10-storage-consistency/storage-physical-consistency-contract.md"
    en: null
    zh-CN: "docs/zh-CN/10-storage-consistency/storage-physical-consistency-contract.md"
---
# Storage Physical Consistency Contract — Candidate

- Work Item: AID-2026-098 (PROVISIONAL)
- Version: 0.1.0-draft
- Date: 2026-11-26
- Status: **Draft / Candidate / Informative**
- Attribution: user-authorized operator (delegated by account owner); proxy registration only — 代理登记，非自然人 Owner 签署
- Canonical source: [10-storage-consistency/storage-physical-consistency-contract.md](../../../10-storage-consistency/storage-physical-consistency-contract.md)
- Chinese mirror: [ZH-CN](../../zh-CN/10-storage-consistency/storage-physical-consistency-contract.md)


- Work Item: AID-2026-098 (PROVISIONAL)
- Version: 0.1.0-draft
- Date: 2026-11-26
- Status: **Draft / Candidate / Informative**
- Attribution: user-authorized operator (delegated by account owner); proxy registration only — 代理登记，非自然人 Owner 签署
- Canonical source: `10-storage-consistency/storage-physical-consistency-contract.md`
- Mirrors: [EN](../docs/en/10-storage-consistency/storage-physical-consistency-contract.md) · [ZH-CN](../docs/zh-CN/10-storage-consistency/storage-physical-consistency-contract.md)
- Related carriers: #1211 (Storage source restoration), #1212 (A–I + Storage composition), #1125 (single Forget Fence authority), #1180 (G delivery-state projection)
- Authority note: this document proposes a reviewable physical contract. It is not an Owner approval, a frozen backend design, a runtime specification already implemented, or production conformance evidence.

## 1. Purpose, status and vocabulary

This candidate closes the *documentation shape* of the F8 Storage Atomicity gap identified by AID-2026-095. It does not close F8. Its purpose is to make physical transaction, persistence, visibility, recovery and anti-rollback obligations falsifiable.

Terms:

- **Owner fact**: a domain fact issued by its accountable Owner (for example D CanonicalCommit/Fence, E Accepted/Compiler state, G ContextVersion/Applied, I authorization/Global Forget Completion).
- **Storage fact**: a physical fact about a transaction, participant, log position, durability level, receipt, replica application or restore activation.
- **GID**: stable global transaction identity for a coordinated multi-participant operation. A GID is not a D commit cursor, E receipt ID, F watermark, G Applied ID or I PermissionEpoch.
- **Visibility pointer**: the committed physical pointer/version through which a consumer can resolve a prepared write. It is a Storage mechanism, not a domain authority.
- **Unknown**: the caller cannot determine whether a physical commit reached its terminal point. Unknown is neither commit nor abort.

A backend profile MUST state its actual transaction scope, isolation level, log mode, synchronous durability setting, replica policy, backup model and recovery limitations. This candidate does not select SQLite, PostgreSQL, a distributed database, WAL, consensus or a COC topology.

## 2. Authority and transaction boundary

### 2.1 Single-resource atomic commit

For every logical Owner operation persisted in one transactional resource, all physical records required to make that operation visible MUST commit or abort together. The required write set is determined by the Owner contract and includes, where applicable:

- immutable object/version payload and its provenance/lineage references;
- current-version pointer update guarded by the Owner's expected-version CAS;
- the Owner-issued commit sequence/cursor reference (Storage persists it but does not mint it);
- idempotency key, normalized request digest and durable result/receipt;
- the Owner's durable outbox/change-intent row;
- participant/visibility metadata needed to prevent prepared data becoming readable early;
- the current D Fence / I authorization observations used to authorize the operation, or a transactionally validated reference to their authoritative versions.

No subset may become externally visible. A failed CAS or validation MUST leave no partial object, pointer, idempotency result, outbox event or success receipt. A duplicate with the same idempotency identity and digest resolves to the original result; a changed digest conflicts.

### 2.2 Required Owner-specific write sets

- **D canonical commit:** D owns canonical identity, version/lifecycle semantics, canonical commit cursor and canonical change identity. The physical transaction MUST atomically persist the immutable canonical version, current pointer/CAS, D sequence/cursor reference, D idempotency result, D commit receipt and D canonical-change outbox. Storage supplies physical atomicity only; it cannot invent or reassign D identifiers.
- **E compiler/admission:** E owns Accepted receipt, compiler state, producer admission and compile-intent semantics. E's accepted envelope/digest/receipt/state and E compile-intent outbox MUST be atomic within E's chosen transaction boundary. This is not the D canonical-change outbox and does not make the event canonical. E and D commits are separate Owner transactions unless an explicitly accepted cross-owner protocol says otherwise.
- **G context/delivery:** G owns ContextVersion, delivery intent and its delivery-state projection; G alone owns the Applied decision under its contract. G's own version/intent/ledger records and G receipt must have a recoverable physical boundary. A Storage receipt is not Delivered, Accepted-by-Adapter or Applied.
- **I authorization:** I owns authorization decision, PermissionEpoch, retention/global Forget policy and Global Forget Completion. Storage persists or validates references; it does not issue I decisions.

### 2.3 Cross-resource operations and linearization

A local database transaction is atomic only inside that database. Two independent databases, a queue, object store, index or replica MUST NOT be described as one atomic transaction merely because the same request identifier appears in each.

Where one logical operation spans resources, the protocol MUST specify participant identities, prepare records, durable votes, a single terminal decision authority, commit/abort recovery, idempotent participant replay and a visibility gate. Until every required participant is durably terminal and the accepted coordinator protocol says commit, prepared writes remain hidden. A future COC/GID protocol is a candidate mechanism only; its cryptographic, quorum, membership and anti-rollback freeze blockers remain open under #1211.

For a single resource, the physical linearization point is the durable database commit record/terminal commit accepted by that backend profile. For a coordinated operation, it is the accepted coordinator's durable terminal commit decision, after the required participant durability predicate. Prepare, enqueue, local write, acknowledgement send, or response construction is not a linearization point.

## 3. WAL, checkpoints and crash recovery

### 3.1 Log-before-data ordering

If the backend uses WAL or an equivalent redo log:

1. Every transaction record is framed with transaction identity, ordered log position, record type/length and integrity check.
2. All redo information needed for committed changes MUST reach the configured durable log before the commit record can be acknowledged.
3. The commit record and required log prefix MUST cross the backend's declared durability barrier (for example fsync or equivalent) before a durable success receipt is returned.
4. Data pages may be flushed later only if recovery can reconstruct the committed state from the retained durable log.
5. Log truncation/recycling MUST NOT pass the oldest required recovery, replica, backup or participant checkpoint.

A WAL label or a configured synchronous flag alone is not proof that the storage device, filesystem, virtualized volume or cloud provider honors the promised flush semantics.

### 3.2 Checkpoint and replay order

A checkpoint MUST identify the exact durable log position it represents and be crash-atomic or recoverably staged. The backend MUST:

1. validate database identity, format/version and checkpoint integrity;
2. locate the last valid checkpoint and the contiguous valid log prefix after it;
3. verify log framing, checksums, transaction boundaries and commit markers;
4. redo complete committed transactions in log order;
5. discard/undo incomplete or uncommitted transactions;
6. persist the recovered state and recovery high-water mark before exposing it;
7. retain/replay any log tail needed by replicas, backups or unresolved participants.

A checkpoint is not permission to skip a missing log segment. A gap, inconsistent sequence, invalid checksum or unknown transaction outcome MUST stop affected visibility and require repair/rebuild from an authoritative source.

### 3.3 Partial writes and crash cuts

A transaction is committed only if its complete commit record and required preceding log records satisfy the backend's durable ordering rule. A partial record, torn page, truncated log tail or absent commit marker is not a successful commit. If integrity cannot distinguish committed from uncommitted state, the result is Unknown and the affected records remain hidden pending reconciliation. Corruption MUST NOT be converted into an empty database, a successful rollback claim or an assumed commit.

Restore MUST stage the backup, validate schema and integrity, apply all mandatory authority projections and recovery records, and activate the staged image atomically. Failure before activation leaves the prior live image intact; failure or uncertainty during activation blocks serving until a deterministic recovery path establishes one valid image.

## 4. Durable receipt

### 4.1 Meaning

A **Storage Durable Commit Receipt** attests only that the named physical participant reached the terminal durability state declared by its backend profile. It does not attest semantic validity, authorization, canonical commit, compiler acceptance, index coverage, delivery, application, Forget completion or physical erasure.

The result vocabulary is:

- `COMMITTED`: terminal commit and declared durability barrier are proven;
- `ABORTED`: terminal abort is proven and no write in the transaction is visible;
- `UNKNOWN`: no terminal result can yet be proven. This is a query/reconciliation result, not a durable terminal receipt.

### 4.2 Minimum fields

A terminal receipt MUST contain, at minimum:

| Field | Meaning |
|---|---|
| `receipt_id` | Stable physical receipt identity |
| `gid` | Global transaction identity, or explicit single-resource transaction identity |
| `participant_id` | Stable participant/resource identity |
| `owner_operation_ref` | Opaque reference to the initiating Owner operation; not reissued by Storage |
| `request_digest` | Digest of the immutable participant request/write set |
| `terminal_state` | COMMITTED or ABORTED |
| `storage_commit_ref` | Backend commit identity |
| `durable_log_position` | WAL LSN or backend-equivalent durable position |
| `durability_profile` | Named, versioned flush/replication guarantee actually used |
| `visibility_pointer` | Committed physical version/pointer, if the operation publishes data |
| `authority_observations` | Exact D Fence cursor/generation and I PermissionEpoch references checked, where applicable |
| `backend_epoch` | Backend incarnation/term/configuration reference sufficient to detect stale receipts |
| `integrity_digest` | Integrity binding over the receipt fields |
| `committed_at` | Backend timestamp for audit; not an ordering authority |

The receipt MUST NOT fabricate D commit cursors, D ForgetFence generations, E AcceptedReceipt IDs, F IndexWatermarks, G ContextVersion/Applied IDs, H acknowledgements or I PermissionEpochs. Missing fields that are mandatory for a given operation make the receipt unusable for that operation.

Same GID + same participant + same request digest MUST return the same terminal receipt. Same GID/participant with a different digest MUST conflict. A retry after Unknown MUST query/reconcile the same GID; it MUST NOT invent a new GID to bypass an unresolved outcome.

## 5. Visibility, isolation and read-your-writes

1. Uncommitted and PreparedHidden data MUST NOT be visible to ordinary reads, indexes, caches, Context snapshots or delivery.
2. A write becomes eligible for visibility only after the physical linearization point, durable receipt and all required Owner predicates have been established.
3. The backend profile MUST name its isolation level. Conflicting writes to the same canonical pointer, GID participant or Fence projection MUST serialize or fail with a deterministic conflict. Snapshot isolation is insufficient where write skew or predicate races can violate the declared invariants; the profile must add explicit locking/serializable validation.
4. Read-your-writes is mandatory for the committing session after COMMITTED is returned. Any read routed to another connection, replica or cache MUST either observe at least the receipt's commit position or be explicitly marked stale/unknown and excluded from authoritative decisions.
5. A replica may serve an authoritative read only after its applied position is at or beyond the required commit position and its D Fence/I epoch observations are current. Lag, missing position or uncertain replay fails closed for affected data.
6. A read begun before commit may return the prior committed version according to its declared snapshot. A read begun after a successful commit on the authoritative path MUST NOT return an older version while claiming current/linearizable visibility.

## 6. Forget Fence projection and anti-rollback

### 6.1 Single authority

AID-2026-089 / merged PR #1232 is the governing direction for this boundary:

- D is the sole logical issuer of ForgetOperation identity/state, typed canonical targets and transitive lineage coverage, Scope coverage, monotonic ForgetFence generation/cursor, canonical suppression and D-domain proof.
- Storage-local Fence rows are derived, rebuildable projections. They MUST NOT allocate an independent sequence/generation/cursor, define target/lineage coverage, authorize reads/publication or declare Forget completion.
- I alone owns authorization, global policy and Global Forget Completion. Physical erasure remains distinct from logical suppression.

This candidate does not create a second Fence authority. A Storage projection stores the exact D-issued generation/cursor and enough typed target/Scope/lineage data to enforce it; it never advances the logical generation itself.

### 6.2 Projection freshness and serving gate

Before serving or publishing affected data, Storage MUST establish that its projection covers the latest applicable D Fence snapshot/cursor for the target and source lineage. A missing, stale, corrupt, rolled-back, incomplete or insufficiently scoped projection MUST fail closed. A projection may be rebuilt from D's authoritative source; it may not be rebuilt by guessing from local row order or namespace alone.

Namespace is a partition/scope attribute, not a substitute for typed target identity, source identity, ScopeRefs or transitive lineage. A namespace-wide row cannot silently stand in for a D target/lineage Fence.

### 6.3 Restore and anti-rollback order

A restore or failover MUST NOT expose a pre-Fence image merely because its local database backup is internally consistent. Before any affected read, index swap, Context materialization, queue replay, delivery or publication:

1. recover the physical database and validate its checkpoint/log chain;
2. obtain and validate the latest D-authoritative Fence snapshot/cursor and I-authoritative PermissionEpoch/policy state;
3. compare projection coverage against those authorities and rebuild or quarantine stale projections;
4. validate replica/backup/backend epoch and any independent anti-rollback anchor required by the accepted deployment profile;
5. expose only after every required gate is current; otherwise remain unavailable for affected data.

The exact independent anti-rollback anchor, trust root, key lifecycle and multi-node quorum mechanism are not frozen by this candidate. Their absence is a blocker, not permission to rely on a backup's own monotonic counter.

## 7. Owner boundaries and cross-domain joins

| Domain | Owns | Storage may do | Storage MUST NOT do |
|---|---|---|---|
| D — canonical commit and Forget | Canonical identity/version/lifecycle, D commit cursor/outbox identity, ForgetOperation/Fence generation and D-domain proof | Atomically persist D's supplied values; enforce validated D Fence projections; return physical receipts | Mint canonical identity/cursor/Fence generation; redefine lineage; issue canonical or Forget proof |
| E — compiler | Accepted receipt, compiler state, producer admission/work lifecycle and compile intent | Persist E's supplied state/receipt/outbox atomically in E's transaction | Treat E acceptance as D canonical commit; mint E receipt semantics; publish on E's behalf |
| F — retrieval/index | Index generation, scan watermark, coverage and retrieval result | Persist index/checkpoint data and enforce visibility gates | Advance F watermark or claim scanned coverage from a Storage commit receipt |
| G — context/delivery | ContextVersion, delivery intent/projection and Applied decision | Persist G records/receipts; hide prepared or stale versions; expose recoverable reads | Issue Delivered, Accepted-by-Adapter or Applied; infer Applied from durable storage |
| H — protocol | Wire/transport/ACK evidence | Persist supplied evidence references | Mint H ACK or protocol state |
| I — security/governance | Authorization, PermissionEpoch, retention/global Forget policy and Global Forget Completion | Persist/validate supplied decision and epoch references | Authorize, waive policy or issue global completion |
| Storage/Consistency | Physical transaction, durability, log/recovery, replica/backup/restore and physical visibility | Provide physical facts and enforcement mechanisms | Become a competing domain authority |

Cross-domain receipts MUST join by stable references and digests, not by overloading one namespace. A physical COMMITTED receipt proves only the physical participant. The relevant Owner must separately resolve its semantic state after crash. An Unknown GID remains hidden until its participant receipts and coordinator decision are reconciled.

## 8. Review checkpoints and evidence classification

**Interpretation:** PASS on a `DOCUMENTED_ONLY` row means only that this candidate states a falsifiable clause. It is not Owner acceptance or Gate A conformance. FAIL on an `EVIDENCE_REQUIRED` row means the repository currently lacks the required physical proof; a future PASS requires reproducible, exact-version evidence and affected Owner acceptance.

| ID | PASS / FAIL checkpoint | Class | Candidate result |
|---|---|---|---|
| SC-01 | PASS iff the single-resource write set includes immutable payload/version, CAS pointer, Owner cursor reference, idempotency result, Owner outbox and receipt in one transaction; FAIL if any required item can commit independently. | DOCUMENTED_ONLY | PASS — clause documented; backend not proven |
| SC-02 | PASS iff conflict/validation/abort leaves no partial visible write or success receipt; FAIL if any subset leaks. | DOCUMENTED_ONLY | PASS — clause documented; backend not proven |
| SC-03 | PASS iff the physical linearization point is the durable commit (or accepted coordinator terminal decision); FAIL if prepare, enqueue or response construction is treated as commit. | DOCUMENTED_ONLY | PASS — clause documented; backend not proven |
| SC-04 | PASS iff WAL/log framing, log-before-data ordering, commit marker and durable flush are demonstrated under the declared backend profile; FAIL if receipt precedes the required durability barrier. | EVIDENCE_REQUIRED | FAIL — no fault-injection / device-flush proof |
| SC-05 | PASS iff checkpoint position, checkpoint atomicity and replay of the contiguous valid committed log prefix are demonstrated; FAIL if truncation can discard required recovery data or skip a gap. | EVIDENCE_REQUIRED | FAIL — no checkpoint/replay proof |
| SC-06 | PASS iff torn/partial records and incomplete transactions are discarded or quarantined, corruption fails closed, and restore activation is crash-safe; FAIL if ambiguous state is exposed. | EVIDENCE_REQUIRED | FAIL — no crash-cut / torn-write / restore proof |
| SC-07 | PASS iff the receipt contains every applicable minimum field and distinguishes COMMITTED, ABORTED and UNKNOWN; FAIL if a receipt overclaims an Owner fact or omits required binding. | DOCUMENTED_ONLY | PASS — receipt shape documented; no emitted receipt evidence |
| SC-08 | PASS iff same GID/participant/digest replays the same receipt and a changed digest conflicts; FAIL if retry creates duplicate or conflicting terminal state. | DOCUMENTED_ONLY | PASS — idempotency rule documented; no multiprocess evidence |
| SC-09 | PASS iff the backend isolation profile is explicit and conflicting operations serialize or deterministically conflict; FAIL if a declared invariant admits write skew/race. | DOCUMENTED_ONLY | PASS — requirement documented; profile unselected |
| SC-10 | PASS iff read-your-writes and post-commit visibility hold on every authoritative read path, and replicas prove applied position/current Fence before serving; FAIL if stale/prepared data is reported current. | EVIDENCE_REQUIRED | FAIL — no replica/visibility proof |
| SC-11 | PASS iff D remains the only logical Fence issuer and Storage projection carries D's exact cursor/generation without a local sequence; FAIL if Storage allocates or advances Fence authority. | DOCUMENTED_ONLY | PASS — authority rule documented; current implementation discrepancy remains |
| SC-12 | PASS iff missing/stale/corrupt/underscoped projection blocks affected read/publication and rebuild uses D authority; FAIL if local namespace/sequence is treated as sufficient. | EVIDENCE_REQUIRED | FAIL — no end-to-end fail-closed proof |
| SC-13 | PASS iff restore validates latest D Fence and I PermissionEpoch plus required independent anti-rollback anchors before exposure; FAIL if a pre-Fence backup can resurrect data. | EVIDENCE_REQUIRED | FAIL — no anti-rollback / restore proof |
| SC-14 | PASS iff D owns canonical identity/cursor/outbox semantics and Storage only persists supplied values; FAIL if Storage creates D facts. | DOCUMENTED_ONLY | PASS — boundary documented; D/Storage exact-version acceptance pending |
| SC-15 | PASS iff E Accepted/compiler state/compile intent remain E-owned and physically atomic only within E's declared boundary; FAIL if E acceptance is conflated with D commit. | DOCUMENTED_ONLY | PASS — boundary documented; E acceptance pending |
| SC-16 | PASS iff G ContextVersion/delivery/Applied remain G-owned and a Storage receipt is never treated as Delivered/Accepted/Applied; FAIL if physical commit promotes G state. | DOCUMENTED_ONLY | PASS — boundary documented; G acceptance pending |
| SC-17 | PASS iff cross-resource GID participants have stable identity, durable prepare/terminal records, deterministic replay and a single accepted terminal-decision authority; FAIL if independent stores are assumed atomic. | EVIDENCE_REQUIRED | FAIL — COC/GID protocol not frozen or proven |
| SC-18 | PASS iff backup, replica rollback, failover and recovery meet a declared RPO/RTO profile with repeatable evidence; FAIL if production durability is inferred from unit tests or WAL configuration alone. | EVIDENCE_REQUIRED | FAIL — no workload/production recovery evidence |

**Count:** 18 checkpoints; 10 `DOCUMENTED_ONLY`; 8 `EVIDENCE_REQUIRED`. The eight evidence-required rows are deliberately FAIL at this candidate baseline. No row constitutes a Gate A PASS.

## 9. Explicit non-claims and closure evidence

This document does not claim: a selected backend; frozen COC or JF-10; cryptographic issuer/signature/key lifecycle; consensus membership or quorum; cross-database atomicity; power-loss durability; multiprocess linearizability; production backup/restore; RPO/RTO; or Owner acceptance.

To change an evidence-required row to PASS, the evidence package must pin the exact code/configuration/backend and test environment; provide reproducible crash cuts before/during/after prepare, commit, flush, checkpoint, replica apply and restore activation; include duplicate/concurrent requests and digest mismatch; verify read paths and replica lag; restore a pre-Fence backup and prove no resurrection; retain raw logs/results; and record D/E/F/G/I plus Storage acceptance for each affected boundary.

### Current source-level discrepancy requiring explicit disposition

The current main snapshot contains Storage-local `canonical_forget_fences` and local sequence-generation code in `crates/memory-storage-sqlite/src/lib.rs`; the separate `crates/memory-event-store-sqlite/src/forget_fence.rs` also contains a namespace-keyed `forget_fence` table and `next_seq` authority. These are implementation observations, not accepted architecture. They do not satisfy the AID-2026-089 single-authority direction as written. The physical contract requires a D-derived projection and no Storage-owned Fence sequence. The exact migration, code path ownership and runtime remediation are outside this documentation-only Work Item and require D/Storage review and separately authorized implementation.

### Review disposition

- Candidate source completeness: submitted for review.
- D / Storage / A semantic acceptance: PENDING.
- E / G consumer acceptance: PENDING where their transaction and visibility boundaries are affected.
- Normative approval: NOT CLAIMED.
- Runtime/validator changes: NONE.
- Merge, Issue closure, implementation and production activation: NOT AUTHORIZED by this document.
