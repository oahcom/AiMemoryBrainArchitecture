# D Module Baseline & Redlines — Memory Brain

**Proposal ID:** DEF-G0-D-001  
**Owner:** D — Memory Brain Architect  
**Status:** PROPOSED — Owner Review Required  
**Version:** 0.1.0  
**Branch:** `session-d-memory-brain-2026-11-16`  
**Authority:** D owns Canonical Memory and canonical Forget authority only. This proposal does not approve implementation or transfer authority.

## 1. Module Mission

D is the authoritative domain boundary for Canonical Memory state and canonical Forget semantics. D defines immutable canonical revisions, canonical commit ordering, lifecycle history, durable ForgetOperation identity, ForgetFence, producer registration/inventory and the canonical publication gate. D provides typed, auditable contracts to downstream modules; it does not own their workers, storage engine internals, permission policy or materialized views.

## 2. Ownership Baseline

D exclusively owns:
- Canonical Memory aggregate identity, canonical revisions and canonical commit records/cursor.
- LifecycleEvent records and per-Memory LifecycleEventCursor.
- ForgetOperation identity/state, ForgetFence generation/cursor, target and lineage coverage.
- Producer class registration authority, per-work registration ledger, registration high-water and barrier snapshot.
- Dependency inventory authority and canonical-domain suppression proof.
- Canonical publication eligibility and the D-owned final canonical visibility decision.

D consumes but does not own:
- I authorization decisions, PermissionEpoch, revocation and global/physical Forget policy.
- E compiler work/attempt/lease/retry/DLQ/staging implementation.
- F indexes, caches, Working Sets, retrieval and IndexWatermark.
- Storage's transaction manager, database selection, XA/prepared transaction implementation and physical durability certification.
- COC/coordinator deployment and operation; C provider outcomes; H wire schema.

## 3. Capability Baseline

D domain capabilities:
1. Create and revise canonical Memory under scope, identity and lineage invariants.
2. Commit multi-object canonical changes with one authority-local CanonicalCommitCursor.
3. Append lifecycle events with per-Memory LifecycleEventCursor.
4. Install monotonic ForgetFence generations over exact target/version-family and lineage coverage.
5. Register producer classes and individual work before execution/admission side effects.
6. Snapshot the producer-registration high-water and dependency inventory at the Forget cutoff.
7. Keep the barrier open until every pre-cutoff participant has authoritative terminal disposition.
8. Reject/quarantine post-fence publication and invalidate proof on late/unregistered derivatives.
9. Emit D-owned canonical suppression evidence without claiming global or physical erasure.

These are domain/contract capabilities. Unless separately evidenced by executable tests and production deployment, implementation status remains NOT VERIFIED.

## 4. Domain Ownership

| Domain object | Authority | Required invariant |
|---|---|---|
| Canonical Memory / MemoryVersion | D | Immutable revisions; exact scope and lineage |
| CanonicalCommitCursor | D | One authority-local successful commit order |
| LifecycleEventCursor | D | Per-Memory append-only lifecycle order |
| ForgetOperation | D | Durable identity, idempotency and immutable audit references |
| ForgetFenceCursor | D | Monotonic generation scoped to operation and target digest |
| ProducerRegistrationHighWater | D | Durable closed-world admission evidence |
| Dependency Inventory | D | Derivative registered before visibility |
| BarrierSnapshotReceipt | D | Exact cutoff and participant set/high-water evidence |
| CanonicalSuppressionComplete | D | D-domain proof only; not Global Forget |

## 5. Interface Baseline

### 5.1 Cursor types — never interchangeable

- `CanonicalCommitCursor`: orders successful canonical transactions within one Brain authority.
- `LifecycleEventCursor`: orders lifecycle events for one Memory; each event also references its enclosing CanonicalCommitCursor.
- `IndexWatermark`: F-owned, partition/index-scoped contiguous applied-through CanonicalCommitCursor plus coverage/schema identity. It is not a canonical cursor or Forget proof.
- `ForgetFenceCursor`: D-owned tuple of ForgetOperation, monotonic fence generation and target-set digest. It is not a commit cursor, lifecycle cursor or index watermark.

A consumer may advance an IndexWatermark only over a contiguous, fully accounted canonical prefix. G ContextVersion and I PermissionEpoch are separate typed domains.

### 5.2 Canonical commit

A successful canonical transaction atomically (or via a proven recoverable equivalent) commits canonical writes, aggregate revisions/heads, applicable lifecycle events, the canonical commit record and outbox intent. Cursor assignment and durable visibility are one boundary. Rejected/aborted transactions do not consume a committed cursor. A read at cursor N sees all effects through N and none after N.

### 5.3 Producer registration and publication

Producer classes and individual work items must be durably registered before work starts, a lease is acquired, retry/DLQ replay is enqueued, or a derivative can become visible. Registration binds stable work/producer identity, source refs and exact revisions/lineage, scope, admission cursor, observed fence, attempt/lease identity and status.

A derivative's dependency edge must be registered before visibility, atomically with the derivative or through a durable prepare/commit protocol that leaves it invisible on failure. The final gate rechecks the latest applicable fence and lineage immediately before canonical visibility. Queue presence, worker-local state or a successful compiler attempt is not publication authority.

### 5.4 Forget fence and barrier

Fence installation durably records exact targets, target-set digest, monotonic generation, canonical installation cursor, dependency inventory snapshot and producer-registration high-water. Every pre-cutoff registered work item remains in the barrier until durable terminal disposition: committed before fence with derivatives inventoried, safely cancelled, suppressed/quarantined, or failed and durably parked with publication disabled. Timeout, lease expiry, queue deletion, worker loss, missing ACK or UNKNOWN/IN_DOUBT is not terminal evidence.

A post-fence work item referencing a fenced target/ancestor is rejected or admitted only for suppression/cleanup. Late-discovered unregistered derivatives invalidate prior closed-world proof and require immediate suppression and reconciliation.

## 6. Security Baseline

- Every operation is scope-bound and uses typed object/actor references.
- I supplies authorization evidence and PermissionEpoch; D verifies required evidence but cannot mint or reinterpret it.
- Missing, stale, incomparable or unverifiable fence/lineage evidence fails closed.
- No forgotten plaintext is stored in the Forget proof; proofs contain identifiers, digests, statuses and evidence references.
- Producer identity and registration are authenticated and durable; unknown producer classes or registry gaps prevent barrier closure.
- D exposes no API that lets a consumer substitute IndexWatermark, LifecycleEventCursor, ContextVersion or PermissionEpoch for ForgetFenceCursor.
- Global completion and physical-erasure policy remain I-owned.

## 7. Module Redlines

1. No module other than D may mint CanonicalCommitCursor, canonical revisions, ForgetOperation, ForgetFenceCursor or D barrier receipts.
2. No compiler or runtime local state may declare canonical publication or canonical suppression complete.
3. No derivative becomes visible before D dependency registration and final fence/lineage validation.
4. No queue, lease timeout, retry count, DLQ movement or worker restart may remove a pre-cutoff participant from the barrier.
5. No cursor type coercion, numeric comparison across cursor domains, wall-clock ordering or opaque-token ordering.
6. No stale admission fence is treated as a permanent publication authorization.
7. No late-discovered dependency may be silently folded into an already-finalized proof.
8. No D decision may certify I authorization, Storage XA/database support, C provider idempotency, COC durability, H schema production readiness or physical erasure.
9. Multi-PolicyDomain atomicity is not accepted by the present JF-10 v2 decision.

## 8. Forbidden Cross-module Actions

- E must not write Canonical Memory or mint canonical commits; it registers producer work and requests D publication.
- F must not write canonical state or infer Forget completion from local suppression/index progress.
- G must not mutate canonical Memory or use ContextVersion as a canonical cursor.
- I must not mint D fence generations or rewrite D lineage facts; D must not decide I authorization.
- Storage must not redefine D domain semantics through a database-specific token; D must not claim unverified Storage internals.
- COC/H/C may provide authenticated ordering or transport evidence but cannot mint D-owned fence, lineage or canonical completion state.

## 9. Dependency Contracts

| Dependency | Provider | D requirement | Current disposition |
|---|---|---|---|
| Permission decision / PermissionEpoch | I | Exact authorization evidence; separate epoch domain | OPEN / I-owned |
| Compiler producer registration and publication | E | Register-before-work/visibility; final D gate | Contract required; implementation NOT VERIFIED |
| Index/cache/retrieval suppression | F | Consume current fence and canonical cursor; owner acknowledgements | Contract required |
| Durable transactions / prepared XID | Storage | Atomic commit/visibility and same-XID recovery evidence | BLOCKED pending DB capability proof |
| Causal ordering / participant evidence | COC/C | Authenticated participant ordering; no D authority transfer | Architecture accepted with exceptions |
| Wire mapping | H | Preserve typed identities without semantic coercion | H-owned, not certified here |

## 10. Conformance Requirements

Required D conformance suites include:
- Atomic multi-aggregate canonical commit and cursor assignment.
- CAS/abort consumes no committed cursor or aggregate revision.
- Lifecycle event sequence continuity and deterministic replay.
- Cursor-domain type confusion rejection.
- Producer registration-before-lease/execute/retry/replay.
- Atomic registration versus fence cutoff race in both orderings.
- Barrier remains open on UNKNOWN, timeout, missing row, stale prefix, lost ACK and owner outage.
- Derivative dependency registration precedes visibility.
- Final publication gate rejects advanced fence and forgotten ancestors.
- Late-discovered dependency invalidates prior proof.
- Same-XID prepared participant recovery across restart/failover.
- Snapshot bootstrap plus exclusive replay preserves contiguous consumer progress.

## 11. Acceptance Criteria

D G0 proposal is acceptable only when:
1. All ownership and non-ownership boundaries above are explicit.
2. The four cursor types are distinct in contracts and tests.
3. Producer registration, fence cutoff and barrier closure are specified without an admission race.
4. Register-before-visible and final publication gate are mandatory.
5. JF-10 exact-version decision and exceptions are pinned to evidence.
6. Tests and implementation claims are status-labelled accurately.
7. D Owner reviews and explicitly accepts a version; this proposal alone remains PROPOSED.

## 12. Change Authority

D alone may change D-owned canonical domain semantics, cursor authority, ForgetOperation/Fence, lineage and producer barrier rules. Cross-module interface changes require the affected Owner's explicit versioned decision. I alone changes permission/global Forget policy; Storage alone certifies database/transaction capabilities; E/F/G/H/C retain their respective internal implementation and contract authority. A coordinates integration acceptance but does not silently replace Owner decisions.

## 13. Open Decisions

- Storage engine selection and evidence for prepared-XID retention, same-XID restart/failover recovery, lock retention and atomic visibility.
- Executable durable producer registry and atomic fence/registration serialization.
- COC operator, durable store, quorum/failover/restore evidence.
- I sequencer implementation, PermissionEpoch/revocation and policy-domain coverage.
- Multi-PolicyDomain atomicity profile.
- C provider idempotency/outcome proof and H schema/parser/SDK interoperability.
- D36, JF10-01..13, Storage crash/fault and cross-owner conformance execution.

## 14. Explicit Non-Claims

This proposal does not claim that D APIs, canonical transaction engine, durable ledger, producer registry, fence locks, COC, Storage prepared transactions or recovery are implemented or production verified. It does not claim D36/JF10 tests passed, global Forget completion, physical erasure, multi-PolicyDomain atomicity, or production activation. D's exact JF-10 v2 architecture acceptance is limited to the single-I-PolicyDomain D-owned semantics and enumerated exceptions recorded in the D Owner decision artifact.

## Evidence

- D branch commit: `1460fbd17ee38ea4044dc6c75cfe49039c7fc585`
- `03-memory-brain/commit-cursor-semantics.md` Blob: `4688a0ca487bf4d853c7f0220408abe8d743d159`
- `03-memory-brain/forget-fence-and-completion-contract.md` Blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- `03-memory-brain/forget-fence-operation-and-publication-gate.md` Blob: `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` Blob: `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2`
- Exact JF-10 v2 decision is pinned in the D branch HEAD commit diff above.
