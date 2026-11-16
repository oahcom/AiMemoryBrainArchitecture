# Typed Cursor and Watermark Contract — Phase 3 Coordination Proposal

- Status: **CANDIDATE** (A coordination proposal; not a schema freeze or implementation guarantee)
- Coordinator: Session A
- Canonical cursor semantic authority: Session D
- Required consumers/validators: E, F, G, Storage/Consistency; H transports opaque typed references; I governs policy epochs separately.
- Current refs: A `session-a-integration-2026-11-16 @ f76cc558273fbc1a27bb930a2f1e8d940b717c80`; D `session-d-memory-brain-2026-11-16 @ 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6`; E `session-e-memory-compiler-2026-11-16 @ 3dea6096eefa6779eb12e4e788bcf9429d2a3f83`; H `session-h-bmcp-protocol @ fcc5103399b4c322e52d642cae5a2414969399a7`; I `session-i-security-governance-2026-11-16 @ 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb`.

## 1. Hard rule

A cursor, revision, watermark, generation, version, delivery sequence or permission epoch is a typed token in one explicitly owned namespace. Raw numeric values from different namespaces are never compared. Cross-stream causality is expressed by typed references or a vector, not scalar coercion.

D's domain-level semantic decision is authoritative for CanonicalCommitCursor. This document records that decision; A does not select or alter D's cursor scope.

## 2. Normative typed inventory

| Type | Authority / scope | Semantics | Does not mean |
|---|---|---|---|
| **CanonicalCommitCursor** | D; one globally ordered sequence per Canonical Memory Authority | Identifies successful canonical transactions in that authority's single total commit order. Domain reference includes authority identity and commit sequence. | No index application, Context update, Forget completion or physical erasure proof |
| **AggregateRevision** | D; each aggregate independently | Monotonically increasing immutable revision sequence for one aggregate. | No global order across aggregates |
| **LifecycleEventCursor** | D; each Memory independently | Monotonically increasing append-only lifecycle event sequence for one Memory; each event also references its enclosing CanonicalCommitCursor. | Not an aggregate revision or global cursor |
| **IndexWatermark** | F; each index/channel partition | Contiguous prefix of canonical commits fully accounted for by that index partition, including explicit irrelevant/no-op coverage. | Not canonical authority, global cursor, or proof of deletion/Forget completion |
| **ForgetFence Generation** | D canonical fence namespace, scoped to Forget operation/target set | Independent monotonically advancing fencing generation. Fence installation itself has a CanonicalCommitCursor for audit/replay, but the generation is not derived from or interchangeable with that cursor. | Not a cursor, commit offset, permission epoch or IndexWatermark |
| **SourceEventCursor** | E; durable Brain ingress stream/partition | E-assigned source-ingress position; producer-supplied sequence remains separate source metadata. | Not CanonicalCommitCursor |
| **ContextVersion / ChangeSet** | G; Context authority | Immutable desired Context version and its change record. | Not canonical Memory revision or delivery acknowledgement |
| **Delivery ID/sequence; Adapter capability epoch; InferenceRequestID** | G/H/C by each owned field | Correlates delivery, adapter capability/configuration and exact inference request boundary. | Not canonical commit ordering |
| **PermissionEpoch** | I; policy domain | Authorization-policy generation, with exact partitioning governed by I. | Not ForgetFence generation; no numeric comparison |

## 3. D-owned CanonicalCommitCursor decision (recorded, not re-decided by A)

D has decided:

1. One globally ordered `CanonicalCommitCursor` sequence per Canonical Memory Authority.
2. Each aggregate has its own independently increasing `AggregateRevision`.
3. Each Memory has its own independently increasing `LifecycleEventCursor`.
4. F owns `IndexWatermark`, scoped by index/channel partition and advanced over a contiguous accounted-for canonical prefix.
5. ForgetFence generation is a separate fencing namespace, not a cursor.

There is no per-aggregate or per-partition CanonicalCommitCursor in D's chosen semantic model. A MUST NOT replace D's global per-authority sequence with the superseded partitioned candidate. Multiple Brain authorities have separate sequences; this does not create a distributed global total order across authorities.

## 4. Causality and consumer rules

- E stores and propagates D's CanonicalCommitCursor unchanged when referring to a committed canonical transaction. E's SourceEventCursor remains a different namespace.
- F consumes canonical commit references and advances its own IndexWatermark independently for each index/channel partition. A partition watermark represents a contiguous accounted prefix; a gap blocks advancement.
- G consumes immutable MemoryVersion references from D and retrieval/activation outputs from F. G's ContextVersion remains G-owned and is not derived by comparing cursor integers.
- H transports owner-defined typed values opaquely; it does not reinterpret, serialize by assumption, or compare D/I generations.
- I's PermissionEpoch and D's ForgetFence generation remain separate typed namespaces. I's global Forget proof is a typed vector of per-domain evidence, not one scalar.
- Consumers must define duplicate handling, out-of-order staging, gap detection, replay/resume, snapshot bootstrap and stale/unknown behavior before declaring conformance.

## 5. Explicitly OPEN — Storage/Consistency realization

D's semantic decision does **not** prove a storage implementation. The following remain OPEN and must not be inferred from the domain contract:

1. How Storage/Consistency allocates and serializes the single per-authority global sequence under concurrent writers.
2. How transaction commit, cursor assignment, canonical visibility and outbox intent share one atomic or proven recoverable boundary.
3. How crash recovery, WAL/replication failover, replay, snapshot bootstrap and restore preserve uniqueness, monotonicity and contiguous committed ordering.
4. Whether aborted/rejected transactions consume no visible committed cursor and how gaps are represented after recovery.
5. How multi-authority cursor identity is named, routed, authorized and retained without pretending there is a global order between authorities.
6. How E, F and G consumers persist their own offsets/watermarks and handle gaps, duplicates, out-of-order delivery, replay and authority changes.
7. How F maps one authority-wide canonical sequence into independent index/channel partition watermarks without advancing over missing relevant work.

No implementation or fault-injection evidence was supplied in the D semantic document. Storage validation remains **OPEN / NOT VERIFIED**.

## 6. Conformance requirements (not yet passed)

| Test | Required result | Status |
|---|---|---|
| Concurrent commits in one authority | Unique, strictly ordered canonical commit cursors; transaction visibility matches that order | NOT RUN |
| Multi-aggregate transaction | One canonical cursor shared by transaction effects; each aggregate revision advances independently | NOT RUN |
| Rejected/aborted transaction | No partially visible commit; cursor behavior matches the committed-sequence contract | NOT RUN |
| Crash at cursor allocation/commit/outbox boundaries | Recovery yields no duplicate/reused visible cursor and no partially visible transaction | NOT RUN |
| Failover/restore | Monotonic per-authority sequence and contiguous replay resume are preserved | NOT RUN |
| Consumer gap/reordering | E/F/G stage or replay missing work; no contiguous watermark jumps the gap | NOT RUN |
| Multiple authorities | Tokens route to the correct authority; no cross-authority numeric ordering assumption | NOT RUN |
| Index partition lag | F partition watermark stops at first unaccounted canonical commit | NOT RUN |
| Fence vs cursor vs permission epoch | Type checks reject cross-namespace substitution/comparison | NOT RUN |

## 7. Ownership and change control

D alone changes CanonicalCommitCursor semantic authority. F alone defines IndexWatermark operational semantics. G owns ContextVersion and ChangeSet. H owns wire representation/transport. I owns permission and global Forget policy. Storage/Consistency owns concrete persistence/transaction/recovery realization. A maintains this cross-module coordination proposal and records owner decisions without superseding them.

This update resolves only the A-vs-D semantic description mismatch. It does not close CR-P1-01, INT-P0-03, INT-X-01, D-REV-P1-003, or any Storage/consumer conformance item.
