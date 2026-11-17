# Phase 3.8.6 — H Exact Wire Crosswalk for R1/R2 Owner Gate Linearization
# Phase 3.8.6 — H R1/R2 Owner Gate 线性化精确 Wire 映射

- Owner perspective: H — BMCP Protocol / Schema and Interoperability
- Status: **CANDIDATE CONTRACT / NOT FROZEN / NOT EXECUTED**
- Exact current unified schema: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.12.schema.json`, Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`
- Exact RecoveryJoin schema: `08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json`, Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- Exact RecoveryCutoff companion schema: `08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.5.schema.json`, Blob `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`
- Exact Storage source: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.md`, Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- Exact coordinator candidate sources: I Blob `57ef6c4352d79577ae53a77895f73bce434c5fca`; D Blob `a7cba2c72720bb7873d77f1a9d151df974605a9e`; C Blob `5c37ebea98436fc985a94f17063b50b4df7ad7a6`.

## 1. Version correction / 版本纠正

The currently published H unified schema on the H branch is artifact revision **1.2.12**, not 1.2.11. The current RecoveryCutoff companion is 1.0.5 and RecoveryJoin is 1.0.2. Earlier 1.2.11 references in historical review notes are historical inputs only and MUST NOT be presented as the current schema binding. The wire schema version remains whatever the exact schema envelope declares; artifact revision and wire version are distinct.

H 分支当前统一 Schema 是 1.2.12，而不是历史文档中出现的 1.2.11。当前 RecoveryCutoff 为 1.0.5、RecoveryJoin 为 1.0.2。历史 1.2.11 引用不得继续作为当前绑定。Artifact revision 与 wire schema version 必须区分。

## 2. R1/R2 record-family crosswalk / 记录族映射

| Required semantic record | Unified 1.2.12 message type | Structural binding |
|---|---|---|
| Owner pending gate + frozen snapshot | `OWNER_LOCAL_PENDING_GATE` | owner kind, gate ref/generation, request/admission counts/digests/high-waters, request/admission roots, anti-rollback anchor, owner signature |
| Immutable recovery batch | `COC_RECOVERY_CUTOFF_BATCH` | exact P, RecoveryEpoch, owner snapshots, manifest ID, enumeration high-water, manifest content digest, counts/member-set root, quorum proof and COC position |
| Immutable participant manifest | `PARTICIPANT_SET_RECONCILIATION` | exact Batch ref/position/entry digest, P, manifest identity/digest, owner snapshot roots, sorted union members, retrieval locator and quorum proof |
| Owner-local pre-COC admission | manifest member `OWNER_LOCAL_ADMISSION` | owner admission/entry identity, ledger/version/sequence/high-water/root, snapshot/attestation, operation/request/scope digests, effect boundary/state, proof ref/digest |
| COC participant | manifest member `COC_PARTICIPANT` | exact participant intent and typed C/D/I/Storage evidence refs |
| Owner gate release | `OWNER_LOCAL_GATE_RELEASE` | exact owner, gate generation, RecoveryEpoch, Batch+Manifest refs/digests/positions, request/admission high-waters/digests/roots, reconciliation root, owner signature |
| Recovery completion | `RECOVERY_EPOCH_COMPLETED` | exact P, Batch+Manifest, reconciliation root, all owner release refs and quorum proof |

The companion RecoveryCutoff 1.0.5 is a structural companion family. It is not a replacement for Unified 1.2.12's complete cross-family envelope. RecoveryJoin 1.0.2 carries owner snapshot membership proof payloads; it does not itself close or release an owner gate.

## 3. R1 completeness semantics / R1 完整性语义

Schema validity alone MUST NOT produce COMPLETE. The semantic validator MUST prove:
1. one exact immutable snapshot per required owner and the same RecoveryEpoch/scope;
2. request and admission ledgers are independently enumerable, pagination-complete and rooted at the attested snapshot;
3. counts equal the actual unique canonical member sets; empty is explicit empty array plus zero count and canonical empty-set digest/root, never null or omitted;
4. every admission through admission_high_water is either a COC participant or an owner-local admission with exact membership proof and disposition; no duplicate, omission or cross-owner counter comparison;
5. all manifest content digest, member-set root, Batch binding and Manifest record binding recompute and match;
6. the committed Batch precedes the Manifest record in the same exact COC prefix; both records are linearly read back;
7. any request/admission/scope/gate-generation advance after snapshot makes the old release stale and requires a successor cutoff round.

A partial page, unavailable owner ledger, unknown key status, stale replica, missing membership verifier or incomplete anti-rollback proof yields UNKNOWN/INCOMPLETE, never empty/complete.

## 4. R2 owner-local release semantics / R2 Owner-local Release 语义

The release validator MUST route to the owner authority and validate the exact signed release projection. Immediately before owner CAS, the owner independently re-reads current GateGeneration, ScopeVersion/scope binding, request high-water, admission high-water, roots and key/anti-rollback status. All must still match the frozen snapshot and complete reconciliation. A mismatch fails closed and starts a successor batch; it cannot be repaired by rewriting an old immutable Batch or Manifest.

COC may persist/verify a signed release but cannot issue it, synthesize it, or release another owner's gate. `RECOVERY_EPOCH_COMPLETED` is not a substitute for any owner release. Gate release only clears the outage-admission gate; it does not grant I permission, clear D ForgetFence/barrier, authorize C provider send, or imply Storage visibility.

## 5. Membership proof verifier integration / Membership Proof 验证集成

RecoveryJoin 1.0.2's `ownerSnapshotMembershipProof` is the per-row cryptographic membership envelope. The H adapter contract in Phase 3.8.5 remains the interface boundary:
- H checks structural shape, exact row/snapshot joins, refs/digests and canonical ordering.
- I/D/C verify their own authority, signature profile, key status, scope, ledger inclusion, snapshot attestation and anti-rollback.
- H maps owner result tri-state: VALID / INVALID / UNKNOWN. Missing verifier, timeout, unavailable registry/ledger or unknown profile is UNKNOWN.

The present Python helper and callback remain TEST-ONLY. No production owner verifier is claimed.

## 6. Explicit semantic gaps / 必须补齐的语义缺口

The schema structurally carries gate generation, request/admission high-waters, roots, owner-specific high-waters, scope-binding digest and signed release references. It does NOT by itself prove:
- that the sequencer actually serialized close against all admission/effect transactions;
- that a high-water/root was captured atomically with gate closure;
- that the owner ledger query is complete and linearizable;
- that owner release performs a fresh currentness CAS at the final serialization point;
- that post-snapshot work is blocked and causes a successor Recovery Cutoff Batch;
- that C's transport handoff is serialized with its egress gate;
- that all signature, key registry, anti-rollback and quorum proofs are authoritative.

Do not add a redundant generic `scope_version` wire field until I/D/C define the owner-specific typed meaning and exact signed preimage. Current `scope_binding_digest` and proof-level `scope_generation` are not interchangeable without an owner-approved mapping.

## 7. Required test matrix (specified, NOT RUN) / 测试矩阵（已定义，未执行）

- R1: omitted admission, duplicate member, wrong owner proof, empty-vs-null, partial pagination, stale snapshot, member root mismatch, Batch-before-Manifest inversion, crash after Batch before Manifest, lost ACK same-key recovery.
- R2: gate generation advance after seal, request high-water advance, admission high-water advance, scope expansion, revoked/unknown key, stale anti-rollback anchor, wrong owner release, COC-synthesized release, RECOVERY_EPOCH_COMPLETED without one release.
- Races: request-vs-close, receipt issue/consume-vs-close, producer/work/lease/retry/replay-vs-Fence, provider send-vs-egress-close in both linearization orders.
- Every trust/evidence outage maps to UNKNOWN/INCOMPLETE; never VALID or empty.

## 8. Decision boundary / 决议边界

This is a coordinator-authored H-role crosswalk candidate. It is not independent H Owner approval, schema freeze, runtime implementation or interoperability PASS. H must independently review the exact schema/source blobs and either adopt, amend or reject this contract. Storage must map the exact same record identities/order; I/D/C must independently attest their owner semantics. A must then perform a fresh exact-version integration review. R1/R2 remain OPEN; Gate A PARTIAL PASS/OPEN; Gate B/C BLOCKED; JF-10 P0 OPEN; Multi-PolicyDomain atomicity BLOCKED; production activation NOT AUTHORIZED.
