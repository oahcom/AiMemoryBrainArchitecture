# AID-2026-001 — Joined Forget / Memory Lifecycle Contract Proposal v2.2 (EN)

**PROPOSED — NOT NORMATIVE.** Additive Storage/Backup persistence-boundary completion layer over frozen v2.1. It does not replace, edit, supersede or weaken v2.1. Per the governance record, exact v2.1 blobs remain the approved upstream layer; that approval does not transfer to v2.2. D/I/Storage approval for this v2.2 exact SHA: NOT CLAIMED.

Read with [ZH v2.2](forget-lifecycle-joined-contract-proposal-v2.2.zh-CN.md), [frozen v2.1 EN](forget-lifecycle-joined-contract-proposal-v2.1.en.md), and [frozen v2.1 ZH](forget-lifecycle-joined-contract-proposal-v2.1.zh-CN.md). v2.1 remains immutable.

- Work item: AID-2026-001 / STOR-R3-001 remediation
- Layer: v2.2 additive durable-persistence-boundary completion over v2.1
- Baseline Head: cc571886c7f5afb8f581740486f6f32ed5f2e61d
- Source Blobs: v1 96882570d44f6a3c6d60a30b1edb0e405bde5efc; v2 28ce1f735be6781b8de32a310d50e24cb457f01e; v2.1 EN 7acd3e5095995c6b8c52b637d7d9978e96619c3a; v2.1 ZH 5c778a6e095d3087937da5edd0273cbfc744ec80; U-010 e12bc3beaf7327f7646fa090cb1fe2cda023cacf; Owner Execution Boundary Contracts v1 008b625bdb29ee65fe136f21c0e9be6396228e4b; R3 Contract Test Matrix 0dac44f65a47541bf5dca90563c90ade6a5d4331.
- Status: PROPOSED — NOT NORMATIVE; implementation/evidence NOT VERIFIED; tests NOT RUN.

## 1. Purpose and authority

This layer addresses STOR-R3-001 / P1 / Issue #41 by explicitly carrying U-010 D-R3-D-002 and Owner Execution Boundary Contracts v1 §8 Storage/Backup obligations. It is additive; v2.1 remains the approved upstream semantic layer. Where silent, v2.1 and its sources continue to apply. This proposal is not proof of implementation, atomicity, backup completeness, restore safety or test execution.

Owner D owns canonical lifecycle/Fence semantics and supplies the domain event/proof. Owner I owns authorization, policy, retention/legal-hold and governance evidence acceptance and supplies its typed decision/reference. Storage/Backup owns and must demonstrate durable serialization, atomicity, replication/failover, backup lifecycle, restore quarantine and recovery visibility. No authority is transferred.

## 2. STOR-01 — Atomic durable semantic commit tuple

For each Forget operation reaching SuppressionCommitted, Storage MUST bind all six elements within one Storage-approved durable atomic ordering and visibility boundary, or an explicitly reviewed equivalent transaction protocol with equivalent observable guarantees:

1. Canonical Memory identity and expected current Lifecycle/Version, including the concurrency/version predicate preventing stale writes.
2. Terminal MemoryLifecycle=Forgotten and its corresponding immutable canonical LifecycleEvent.
3. Applicable monotonically increasing ForgetFence generation and tombstone, bound to the canonical identity and protected against rollback/lowering.
4. Stable ForgetOperation identity, idempotency identity/request binding, and operation phase SuppressionCommitted.
5. Durable Outbox/Publication record sufficient to make committed suppression observable to downstream enforcement/reconciliation; a best-effort notification written after the boundary is insufficient.
6. Immutable typed references and/or cryptographic digests for the I authorization decision and D suppression proof, bound to the same operation, Memory identity, fence generation and commit.

These six elements form one semantic tuple, not six independently successful writes. The authoritative outcome MUST be all-or-nothing. Partial visibility of Forgotten without its fence, operation state, proof references or durable publication intent is prohibited. A fence/outbox record without canonical terminalization is not a completed suppression commit.

Storage MUST document the selected transaction/consensus/WAL protocol, atomicity/durability guarantees, serialization point, isolation/visibility, crash recovery and idempotent retry behavior. If no single physical database transaction is used, the equivalent protocol MUST be explicitly reviewed and demonstrate: (a) one authoritative commit decision for the complete tuple; (b) durable recovery after process/node/availability-zone failure within the declared failure model; (c) no externally visible partial tuple; (d) deterministic reconciliation of unknown client outcome without repeating a non-idempotent action; and (e) durable publication intent coupled to commit with replay-safe dispatch.

The transaction/WAL receipt MUST identify transaction/commit, operation, canonical Memory reference, fence generation, tuple/proof references and authoritative outcome. Generic success, queue ACK, transport ACK or an independently written event is not atomicity proof.

Storage MUST NOT claim SuppressionCommitted without verifiable evidence that the complete six-element tuple crossed the approved atomic durable boundary. Unknown outcome is UNKNOWN: fail closed for reads/publication and reconcile authoritative durable state. Do not infer success from timeout, process completion, partial rows or notification. The semantic trigger remains successful durable SuppressionCommitted, where canonical MemoryLifecycle becomes terminal Forgotten. I authorization is a precondition, not a substitute for Storage commit. D/I governance completion and physical erasure remain separate facts.

## 3. STOR-02 — Monotonic fence durability across replication/failover

Storage MUST preserve a durable, monotonically increasing high-water mark for applicable ForgetFence generations across replication, failover, leader election, replica promotion, restore and disaster recovery.

1. Every authoritative write/promotion path MUST compare against the committed high-water mark before becoming authoritative or serving protected reads.
2. A stale/lagging replica below the latest committed fence high-water mark MUST NOT become an authority. It remains non-authoritative, fenced or quarantined until caught up and reconciled.
3. Replication lag MUST NOT lower, erase, roll back or make the committed fence optional. Promotion preserves the maximum committed generation, not merely the promoted replica's local observation.
4. Generation allocation/commit MUST be monotonic and resist stale-writer/split-brain commits. Conflict resolution MUST never select a lower generation.
5. Storage MUST expose a verifiable replica high-water observation identifying replica, observed generation, authoritative generation, observation time and verification method. Missing/unavailable observation is UNKNOWN, not proof of parity.

No procedure may restore ordinary read authority by promoting a replica below the committed fence high-water mark.

## 4. STOR-03 — Suppression-first visibility and fail-closed reads

Suppression MUST take effect at the canonical commit boundary and precede asynchronous physical erase/de-identification. Pending physical cleanup does not weaken suppression.

1. Every read, retrieval, derivation, activation, delivery, index/cache serving and restore-visibility path MUST consult the authoritative current ForgetFence, or an explicitly approved equivalent that cannot be stale below the committed high-water mark, before making protected content observable.
2. If a serving path cannot query/validate the authoritative fence, establish freshness/high-water mark, or receives UNKNOWN/timeout/inconsistent state, it MUST fail closed for the affected identity/scope or be isolated from serving. It MUST NOT fall back to a stale local replica/cache or assume no fence exists.
3. Suppression remains effective while physical cleanup, replica convergence, backup expiry or external-recipient work is pending.
4. Cache, index, derived projection and publication consumers MUST discard/quarantine stale content when the fence advances. Durable publication intent does not authorize stale dispatch/replay; current fence must be rechecked.
5. SuppressionCommitted does not prove physical erasure. Storage and each responsible executor report physical erase/de-identification separately with per-copy evidence.

## 5. STOR-04 — Backup-set inventory, retention and uncertainty

For every in-scope backup set, Storage/Backup MUST maintain a durable manifest identifying: immutable backup-set ID and snapshot/time identity; coverage (systems, stores, regions, shards, replicas, object classes and time/version ranges included or explicitly excluded); creation time; expiry time; applicable retention policy/version; applicable encryption/key, access and restore constraints; restore ordering/dependencies and required fence/reconciliation procedure; manifest integrity/provenance, verifier and observation time.

A backup not yet at verified expiry is NOT erased. Expiry alone is not a per-copy erase receipt unless policy and evidence establish that the media/object is no longer recoverable. Any retention exception remains a separately attributable I decision with bounded scope, controls and expiry; this layer grants none.

A missing, inaccessible, incomplete or unauthenticated backup manifest MUST be recorded as UNKNOWN. Missing inventory MUST NOT mean no backup, no copy, expired or erased. Unknown backup coverage blocks any completion/compliance claim dependent on proving that coverage.

## 6. STOR-05 — Restore preflight, quarantine and reconciliation

Restore is a potential resurrection event. Before any restored copy, snapshot, replica or derived state becomes queryable, deliverable, activatable or otherwise visible, Storage/Backup MUST:

1. Place the restored target/snapshot in quarantined, non-serving state. Quarantine remains if any required manifest, fence state or reconciliation evidence is unavailable.
2. Obtain and durably apply the latest authoritative ForgetFence generation/high-water mark, including all tombstones applicable to restored coverage. A snapshot's embedded fence is not presumed current.
3. Enumerate every Forget operation committed after the backup snapshot cut/time and reconcile each against restored coverage: operation identity, canonical Memory identity, fence generation, commit outcome and affected copy/target.
4. Reapply suppression/tombstones and invalidate stale index, cache, projection, publication intent or delivery state that could expose a forgotten identity.
5. Verify post-restore state with negative query/delivery checks and record the restore preflight/reconciliation trace.
6. Release quarantine only after fence application and reconciliation complete, evidence is durable and the accountable Storage/Backup release condition is met. UNKNOWN, missing manifest, incomplete reconciliation or unavailable fence service means remain quarantined.

Restore MUST invalidate prior D completion/I governance completion evaluation that depended on restored coverage until reconciliation completes and relevant owners re-evaluate. Restore must never lower the fence or resurrect ordinary access, even where the backup snapshot predates the Forget operation.

## 7. STOR-06 — Evidence obligations and status

Storage/Backup evidence MUST be append-only, integrity-protected, content-minimal and attributable to exact operation, fence generation, target/copy and execution version. At minimum, as applicable, evidence MUST include:
- transaction/WAL commit receipt proving atomic durable commit of the six-element tuple;
- ForgetOperation identity, idempotency identity, commit outcome and fence generation;
- replica high-water observations across relevant replicas and promotion/failover boundaries;
- per-copy erase/de-identification receipt with copy identity, action, result, verifier and trusted observation time;
- backup-set manifest, coverage and verified expiry/retention proof;
- restore preflight and per-operation reconciliation trace, including quarantine entry/release decision;
- post-restore negative query and delivery test evidence.

Each item MUST have immutable reference/digest, evidence kind, provenance, authenticated producer/verifier, trusted observed_at, integrity protection and binding to the relevant operation/target/fence. Evidence MUST NOT contain forgotten payload or become an unauthorized retained copy.

**Evidence status: OPEN / NOT RUN / NOT PROVIDED.** This specification creates no receipts and claims no transaction proof, replica observation, erase receipt, backup manifest, restore trace or negative-test result. Missing evidence is UNKNOWN/NOT PROVIDED, not proof that the corresponding copy or risk does not exist.

## 8. STOR-07 — Mandatory failure rules

Preserving Owner Execution Boundary Contracts v1 §8:
- No atomicity proof: do not claim SuppressionCommitted; keep UNKNOWN/blocked and fail closed until authoritative reconciliation.
- Replication lag: never lower/roll back the fence; a replica below committed high-water mark cannot become serving authority.
- Restore: keep backup restore quarantined until latest fence/high-water mark is applied and all post-snapshot Forget operations are reconciled.
- Missing backup manifest: classify coverage/state as UNKNOWN, never erased.
- Fence lookup unavailable or stale: affected read/serving paths fail closed or are isolated; no stale fallback.
- Partial tuple or publication failure: do not expose partial success; reconcile authoritative transaction and durable outbox intent.
- Unknown post-commit outcome: do not blindly replay destructive actions; reconcile first. A proven commit remains Forgotten and its fence remains monotonic.

These are mandatory failure constraints, not discretionary recommendations.

## 9. Test cross-references and verification gate

Existing source IDs are cross-references only; this layer does not copy, rename, rewrite or replace their scenarios/assertions:
- DFI-021 — atomic suppression commit/failover: this layer §§2–3 and §8; original source ID/assertion remain in the R3 matrix.
- DFI-022 — backup restore before latest fence application: this layer §§5–8; original source ID/assertion remain in the R3 matrix.
- DFI-012 — backup restore after Forget: this layer §6; original source ID/assertion remain in the v2.1 crosswalk.

These references are not execution evidence. Storage/Backup evidence and reproducible fault-injection tests remain OPEN / NOT RUN. No test ID is redefined here.

## 10. Finding, approvals and non-claims

- STOR-R3-001 — P1 — Issue #41 — SPECIFICATION_REMEDIATION_PROPOSED / PENDING_INDEPENDENT_REVIEW_AND_STORAGE_REASSESSMENT. §§2–8 explicitly state the six-element atomic tuple, executable Storage/Backup failover/read/backup/restore obligations, failure rules and evidence requirements.
- v2.1 is treated as the frozen upstream approved layer per the governance record; this commit does not modify its files or exact content SHAs.
- D/I/Storage approval of this v2.2 exact content SHA: NOT CLAIMED. Any later approval must identify this exact SHA and be attributable to the relevant authority.
- Independent review, Storage reassessment, D/I supplemental same-SHA approval, integration review, R3 reproducible tests and fault-injection evidence remain pending.
- No runtime implementation, production conformance, atomicity proof, backup completeness, physical erasure, restore safety, test PASS, Finding closure, merge or production activation is claimed.

**Overall AID-2026-001 status remains BLOCKED_PENDING_R3_EVIDENCE.** Specification repair is not approval, implementation evidence or test evidence.
