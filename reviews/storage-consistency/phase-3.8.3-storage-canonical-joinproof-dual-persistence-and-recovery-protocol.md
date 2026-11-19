# Phase 3.8.3 — Storage Canonical JoinProof Dual-Persistence and Recovery Protocol

- Decision ID: `STORAGE-OWNER-2026-11-20-001`
- Work Item: `AID-2026-011`
- Owner: Storage Owner
- Finding: F-43-06A (P1)
- Status: **STORAGE NORMATIVE DECISION — ACCEPTED AS STORAGE-OWNED ARCHITECTURE CONTRACT**
- Scope: canonical Storage persistence of one immutable RecoveryJoinProof, subsequent COC quorum binding, bidirectional authoritative readback, retry/replay and crash recovery.
- Explicit non-scope: production implementation/conformance, COC quorum algorithm or threshold, COC-owned ParticipantIntent semantics, H wire/schema freeze, D/I/C owner release decisions, physical deployment selection.
- Predecessor: `reviews/storage-consistency/phase-3.6.11-storage-bidirectional-coc-owner-admission-join-proof.md`, Blob `eac350ed5cb53094bdd5626f49e6f82ebea1f78c`.
- Related topology boundary: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`, Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`.

## 1. Normative terms and authority split

The object governed here is the immutable **RecoveryJoinProof**. It is distinct from `StorageVisibilityParticipantRef`, `D PublicationParticipantRef`, and COC `ParticipantIntentRef`. A participant reference is not a JoinProof identity, and none of these nominal types may be aliased.

The immutable JoinProof identity is:

`JoinProofIdentity = (StorageAuthorityRef, JoinProofNamespace, RecoveryEpochRef, RecoveryRound, RecoveryJoinProofRef, RecoveryJoinProofDigest, CanonicalizationProfileRef, SchemaProfileRef)`.

The request/idempotency key is the stable `RecoveryJoinProofRef` within the Storage authority/namespace and recovery epoch/round. The complete immutable request digest covers every semantic field, membership edge, source snapshot ref+digest, prefix, scope, generation, schema/profile version and canonical payload byte. Transport metadata, retry count, wall-clock time and response destination are excluded. A changed semantic field or canonical byte changes the digest and is not an exact replay.

**Storage owns content authority.** Storage's durable record at the exact Storage reference is the one and only canonical byte/content copy of the JoinProof. Storage owns the ref namespace, immutable content digest, durable version/commit identity, signed durable receipt, retention, restore and authoritative content readback.

**COC owns commit/visibility authority.** COC owns its ParticipantIntent/append record, quorum rule, quorum configuration/epoch, append position, quorum certificate and authoritative proof that the binding was quorum committed. COC stores a binding envelope, not a second canonical JoinProof content copy. The binding envelope contains the exact Storage identity/ref/digest and the exact Storage receipt (or its collision-resistant digest plus retrievable signed envelope), along with COC's own transaction/intent identity. COC may retain an opaque immutable evidence attachment only if COC's own contract requires it; that attachment is never a competing canonical JoinProof copy and must byte-match Storage's canonical content if it purports to reproduce it.

Neither authority substitutes for the other:
- Storage durable write/receipt does not prove COC quorum append.
- COC quorum binding does not make COC the content authority and cannot repair, rewrite or replace Storage content.
- A D/H/A cache, replica, index, export or local copy is a projection, not canonical.
- COC alone defines whether a JoinProof is in its scope and what constitutes its quorum certificate. If COC applicability is required but not authoritatively established, state is UNKNOWN/BLOCKED.

## 2. Canonical encoding and immutable content

Before the first write, the producer constructs the complete JoinProof payload under the exact H-approved schema/canonicalization profile and computes its content digest over the canonical bytes using the digest algorithm/profile named in the payload. The profile/version and schema revision are part of the immutable identity. Storage MUST reject ambiguous, non-canonical or profile-mismatched bytes; it MUST NOT silently normalize or reserialize a previously accepted identity.

The canonical bytes MUST include all JoinProof content and binding evidence required by the predecessor contract, including:
- exact RecoveryEpochRef, round, JoinProofRef and reconciliation attempt generation;
- exact COC domain/prefix and RecoveryBatchRef+digest;
- ParticipantManifestRef, content digest and record digest;
- exact I/D/C snapshot refs, digests, authorities, completeness states, roots/high-waters and relevant generation/scope anchors;
- both directional join-edge sets and explicit completeness/difference results;
- JF-10 sub-join evidence where applicable;
- schema/canonicalization/digest profile identifiers and issuer/key reference metadata.

No field may be appended, removed, reinterpreted or mutated under an existing JoinProofRef. A semantic change requires a separately authorized new RecoveryEpoch/round and a new identity after the prior identity has a proven terminal disposition. A new identity MUST NOT be used to escape an unresolved/UNKNOWN prior attempt.

## 3. Required write and commit sequence

The only valid success sequence is:

**Storage durable write → Storage signed durable receipt → COC quorum append binding exact Storage ref/digest/receipt → dual authoritative readback → owner release eligibility.**

### 3.1 Storage durable write (first)

Storage executes an atomic immutable `PutIfAbsent` (or equivalent linearizable create) for the exact JoinProof identity and canonical bytes. Before success, Storage MUST:
1. authenticate the caller and validate authority/namespace, epoch/round, schema and canonicalization profile;
2. compute/verify the canonical content digest itself;
3. enforce uniqueness of `RecoveryJoinProofRef` within its namespace;
4. durably commit the complete canonical bytes, immutable identity, digest and commit/version metadata to Storage's authoritative durability domain;
5. ensure the acknowledged write survives the durability/failover guarantee claimed by that Storage authority.

Only after the durable commit may Storage issue a success receipt. A write to volatile memory, local cache, asynchronous queue, uncommitted transaction, non-authoritative replica or object store without the required durability acknowledgement is not a durable write and MUST NOT produce a success receipt.

### 3.2 Signed Storage durable receipt

The receipt is signed by the Storage authority and binds at minimum:
- receipt type/version and Storage authority/key identity;
- exact Storage namespace and database/authority incarnation;
- exact `RecoveryJoinProofRef` and complete `JoinProofIdentity`;
- exact canonical `RecoveryJoinProofDigest`, byte length and canonicalization/schema profile;
- immutable Storage record reference and durable record/version/commit identity;
- durable-write outcome and the authority's declared durability class;
- the exact immutable request/idempotency digest.

The receipt signature covers the complete canonical receipt payload. The receipt is issued only after §3.1 commit. A receipt is not a COC quorum proof and does not authorize owner release. Lost receipt delivery is resolved by querying Storage with the same identity and request digest; Storage returns the original signed receipt byte-for-byte (or its same signed immutable envelope), never a newly minted receipt for a new record.

### 3.3 COC quorum append (second)

After verifying the Storage receipt and independently resolving the exact Storage record, the caller submits one immutable COC append request. COC's append binding MUST include:
- COC authority, COC namespace and COC transaction/ParticipantIntent identity;
- exact Storage authority/namespace/incarnation;
- exact `RecoveryJoinProofRef`, immutable Storage reference and `RecoveryJoinProofDigest`;
- exact Storage receipt bytes or receipt digest plus an authenticated retrievable receipt reference;
- the immutable request/idempotency digest and schema/canonicalization profile;
- the exact COC-defined scope/applicability and transaction correlation fields.

The COC append is successful only at COC's own quorum-defined durable linearization point. COC MUST return a signed/authenticated quorum append proof identifying its exact intent/binding digest, quorum configuration/epoch, append position or opaque cursor, and the quorum certificate/evidence needed for authoritative verification. The quorum proof MUST cryptographically or structurally bind the complete binding envelope, including the exact Storage ref, content digest and receipt. A bare ref, transaction ID, count, unbound root, local append acknowledgement or non-quorum replica write is insufficient.

This protocol does not select a quorum size, consensus algorithm, COC log format or physical topology. Those remain COC-owned. It requires COC to expose verifiable proof that its own specified quorum committed this exact binding.

### 3.4 Dual authoritative readback (third)

Before any owner release, perform both reads against the owning authorities, not caches:

**Storage read:** resolve the exact Storage ref and return canonical bytes, identity, digest, schema/profile, immutable version/commit identity and the original signed Storage receipt. Verify the digest by recomputing it over the returned canonical bytes; verify receipt signature, key/authority status and every receipt binding.

**COC read:** resolve the exact COC append/intent and return the quorum-committed binding envelope, exact Storage ref/digest/identity, exact Storage receipt binding and verifiable quorum proof. Verify COC authority, configuration/epoch, append position/cursor, committed status and the proof's binding to the complete envelope.

Compare, field-for-field:
- Storage authority, namespace and incarnation;
- RecoveryEpochRef, RecoveryRound, RecoveryJoinProofRef and immutable request/idempotency digest;
- exact Storage reference and RecoveryJoinProofDigest;
- schema/canonicalization profile and byte length;
- Storage receipt identity, payload digest and signature binding;
- COC intent identity, binding digest, quorum configuration/epoch and append proof.

All comparisons MUST be exact. Any missing field, failed signature/currentness check, unavailable authority, unavailable quorum proof, digest mismatch, ref substitution, stale incarnation, non-linearizable read or inability to prove quorum commit yields **UNKNOWN/BLOCKED**. Do not downgrade to a best-effort comparison.

### 3.5 Owner release (fourth)

Storage may report `JOIN_PROOF_DURABLE_AND_COC_BOUND` only after §§3.1–3.4 all succeed. This status means the cross-domain evidence is complete; it is not an OwnerGateRelease and does not itself release any D/I/C gate.

Each owner independently evaluates its own release predicate and currentness at its own authority. Storage MUST NOT issue D, I or C owner release, sign their semantic terminal receipts, or treat the JoinProof as sufficient if their own predicates remain unresolved. No release, completion event or barrier clearing may occur after only Storage write, only receipt, only COC append, or only one side's readback.

## 4. Canonical-copy conflict and repair policy

Storage's canonical bytes are authoritative for JoinProof content. COC's quorum-committed binding is authoritative for whether COC committed the exact Storage record. Neither is a general-purpose tie-breaker for the other.

| Observed condition | Decisive authority / classification | Required action |
|---|---|---|
| Storage bytes match their signed receipt; COC exact binding and quorum proof match | Both authorities agree | Eligible for owner-local release evaluation |
| Storage unavailable; COC binding exists | No content readback; COC proof cannot replace canonical bytes | UNKNOWN/BLOCKED; retain gates; restore/read same Storage identity |
| COC unavailable; Storage record and receipt exist | No proof of COC quorum commit | UNKNOWN/BLOCKED; retain gates; query/recover same COC identity |
| COC binds different ref, digest, identity or receipt | COC binding is decisive for what COC committed; it does not alter Storage content | INTEGRITY_CONFLICT; quarantine; no release |
| Storage returns bytes whose digest differs from immutable receipt/identity | Storage canonical record integrity failure | INTEGRITY_CONFLICT; quarantine; no overwrite |
| COC claims commit but quorum proof cannot be verified | COC commit not established | UNKNOWN/BLOCKED; no release |
| A cache/replica/newer timestamp disagrees with either authority | Cache/time has no authority | Ignore as decision evidence; investigate; no overwrite |

No automatic repair may select the newer timestamp, largest version, freshest replica, local cache, or last successful response. No system may copy COC's binding-only record over Storage canonical content, or copy Storage content into COC and claim that this creates a quorum commit.

If the canonical Storage copy is temporarily unavailable, the system remains UNKNOWN/BLOCKED. Recovery may restore the exact same canonical bytes under the same immutable Storage reference only from authenticated, integrity-verified backup/replica evidence, preserving the original identity, digest, receipt and durable commit lineage. If that cannot be proven, remain quarantined; do not synthesize a replacement receipt or identity. If COC's quorum history is unavailable or forked, only COC may restore/resolve its own quorum history; Storage cannot infer it.

## 5. Idempotency, replay and changed requests

Every attempt, retry, timeout recovery and response-loss query MUST reuse the same `RecoveryJoinProofRef`, immutable identity and request/idempotency digest. The COC side MUST likewise reuse the same COC intent/append idempotency identity. A cross-domain retry may not replace either side's identity.

- **Exact replay:** same identity + same canonical digest + same complete immutable request returns/resolves the original Storage record and original signed receipt. If COC already committed, it returns/resolves the original COC intent and original quorum proof. No duplicate logical append or new receipt identity is minted.
- **Changed digest:** same identity with different content/request digest returns `IMMUTABLE_IDENTITY_CONFLICT`; it is not an update, overwrite, new version or retry. Quarantine the identity and preserve both request evidence and the original record.
- **Changed parameters:** any change to epoch/round, prefix, owner snapshots, participant set, edge membership, scope, generation, schema/profile or canonical bytes is a changed immutable request even if the caller reuses the same ID. Reject as conflict; do not silently ignore the changed field.
- **Timeout/lost ACK:** outcome is UNKNOWN until queried from the owning authority. A timeout is neither commit nor abort.
- **Query order:** query Storage by exact Storage identity; query COC by exact COC idempotency/intent identity; verify exact binding; then repeat dual readback. Never infer COC abort from a missing Storage response or infer Storage abort from a COC response.
- **No new identity escape:** if the original identity is UNKNOWN/BLOCKED, do not mint a successor identity, new epoch, new round, replacement ref or alternate digest to bypass it. A successor may be considered only after the original authority proves a terminal disposition and the applicable owner/governance contract authorizes a new epoch/round.

## 6. Crash and recovery matrix

| # | Crash / failure point | Recovery query and classification | Required disposition |
|---|---|---|---|
| 1 | Before Storage durable write commits | Query Storage with same identity; if authoritative linearizable proof establishes no write and no delayed write/retry can commit, state `NOT_COMMITTED`; otherwise UNKNOWN | No success receipt; do not call COC append; retry same identity only |
| 2 | Storage durable write committed, signed receipt response lost | Query Storage exact identity + request digest; verify canonical bytes and durable record; return original signed receipt | Treat as Storage-durable only after authoritative verification; continue same COC identity |
| 3 | Receipt exists, COC append not yet committed | Query Storage for original record/receipt; query COC exact append identity | If COC proves not appended, retry same append identity; if cannot prove, UNKNOWN; Storage copy remains canonical |
| 4 | COC quorum append committed, response lost | Query COC exact intent/idempotency identity and verify quorum proof + binding digest | Return original quorum proof; never append a second logical intent |
| 5 | COC append failed to reach quorum | COC must report non-commit only with authoritative proof covering in-flight append/replay; otherwise UNKNOWN | No release; retry same COC identity; do not infer abort from timeout/negative ACK |
| 6 | COC committed, Storage readback temporarily fails | Query COC proof and retry Storage exact ref read | UNKNOWN/BLOCKED until Storage canonical readback and receipt verify; no release |
| 7 | Storage and COC readbacks disagree | Preserve both evidence sets; compare exact identity/ref/digest/receipt binding | INTEGRITY_CONFLICT; quarantine; no overwrite, no release; Owner/A escalation |
| 8 | Crash after dual readback but before owner release | Re-run both authoritative readbacks and each owner's currentness/release predicate | Release only after fresh successful checks; otherwise UNKNOWN/BLOCKED |
| 9 | Recovery finds identity exists but digest differs | Verify original Storage receipt and COC binding; classify changed digest as immutable identity conflict | INTEGRITY_CONFLICT; do not mutate, replace or create new identity |
| 10 | Retry reuses identity but changes any request parameter | Recompute complete immutable request digest and compare to registered identity | IMMUTABLE_IDENTITY_CONFLICT; reject changed request; preserve original attempt |

A `NOT_COMMITTED` classification is permitted only when the owning authority supplies a linearizable no-commit/no-effect proof that covers delayed writes, retries, queues, outbox handlers, failover and replay. A missing row, timeout, RPC error, expired lease, process death or stale replica is not such proof.

## 7. State vocabulary and fail-closed rules

Storage-local state vocabulary:
- `STORAGE_NOT_WRITTEN`: authoritative proof no durable write occurred and no delayed write can occur.
- `STORAGE_DURABLE_RECEIPTED`: exact canonical record durably committed and signed receipt verifiable.
- `COC_APPEND_PENDING`: Storage durable record exists; COC commit not yet proven.
- `COC_COMMIT_PROVEN`: COC quorum proof verifies exact Storage binding.
- `DUAL_READBACK_VERIFIED`: both authorities returned exact matching evidence.
- `JOIN_PROOF_DURABLE_AND_COC_BOUND`: §§3.1–3.4 completed; owner-local release evaluation may begin.
- `UNKNOWN_BLOCKED`: commit/readback/currentness cannot be established.
- `IMMUTABLE_IDENTITY_CONFLICT`: same identity presented with changed digest or immutable parameters.
- `INTEGRITY_CONFLICT`: authoritative records/proofs contradict or canonical bytes fail integrity verification.

The following MUST remain UNKNOWN/BLOCKED (or INTEGRITY_CONFLICT where contradiction is proven): either authority unavailable; missing identity/ref/digest/receipt fields; receipt or quorum proof unverifiable; quorum not established; stale/forked log or database incarnation; incomplete/non-linearizable readback; cross-side mismatch; canonical copy unavailable; unresolved timeout; uncertain commit; identity exists with changed digest; retry parameters changed; or recovery cannot prove no delayed commit. These states MUST NOT release any owner gate, mark the epoch complete, or be converted to abort by elapsed time.

## 8. Topology boundary

This protocol defines logical authority and ordering, not a physical cross-system atomic transaction. It does not claim XA/2PC, a shared transaction, or atomic commit spanning Storage and COC.

The Storage/D serialization ADR remains bounded: its L1 logical Option A concerns the D/Storage serialization domain; COC remains a separate quorum log and is not silently folded into that database transaction or treated as XA. If actual deployment cannot satisfy Storage durable acknowledgement, authoritative read-after-commit, failover fencing and continuity, the Storage side is non-conforming. If COC cannot prove its own quorum append and exact binding, the COC side is non-conforming. Any proposed topology change requires the responsible Owners' successor decision and evidence; this document does not select an L4 engine or deployment.

## 9. Explicit non-claims

This is a normative Storage architecture decision only. It does not assert that any production implementation exists, that a signed receipt has been generated in production, that a real COC quorum append/readback has occurred, that a dual-readback has been executed, that D/I/C gates were released, or that tests/CI/physical topology are verified. No production activation is authorized.

---

## 中文规范（与英文条款同等效力）

### 10. 权威与规范副本

RecoveryJoinProof 是本协议对象，必须与 `StorageVisibilityParticipantRef`、D `PublicationParticipantRef`、COC `ParticipantIntentRef` 保持不同名义类型。

**Storage 是 JoinProof 内容权威和唯一规范副本持有者**：完整规范字节、内容摘要、不可变 ref、持久化版本/提交身份、签名持久化回执、保留/恢复及权威内容回读均归 Storage。**COC 是提交/可见性权威**：COC 自己决定适用性、ParticipantIntent、quorum 规则、配置/epoch、append 位置及 quorum proof。COC 保存绑定 envelope，不保存第二份可竞争的 JoinProof 内容规范副本。

Storage receipt 不证明 COC quorum；COC quorum binding 不替代 Storage 内容，不得改写或修复 Storage 内容。缓存、索引、导出和 A/D/H 投影均不是规范副本。

### 11. 强制写序

1. **Storage durable write**：按稳定 `RecoveryJoinProofRef` 执行线性化 PutIfAbsent，完整持久化 canonical bytes、identity、digest、schema/profile 和 commit/version 元数据。未达到 Storage 权威持久化确认，不得返回成功。
2. **Storage signed receipt**：仅在 durable commit 后签发。必须绑定 Storage authority/namespace/incarnation、精确 JoinProof ref、完整 immutable identity、canonical digest、字节长度、schema/canonicalization profile、record/version/commit identity、请求幂等摘要。receipt 签名覆盖完整 canonical receipt payload。
3. **COC quorum append**：COC append 必须绑定精确 Storage authority/namespace/incarnation、JoinProof ref、digest、receipt（原始签名 envelope 或其摘要及可认证取回引用）、请求幂等摘要、schema/profile 和 COC 自己的 intent/transaction identity。只有达到 COC 自己定义的 quorum durable linearization point 才算成功；quorum proof 必须绑定完整 binding envelope。裸 ref、transaction ID、count、未绑定 root 或单副本 ACK 不算提交。
4. **双向权威回读**：Storage 读 canonical bytes、identity、digest、profile、version/commit identity 和原始 signed receipt；COC 读 quorum-committed binding envelope、精确 Storage ref/digest/identity/receipt binding 及 quorum proof。逐字段精确比较并重新计算内容摘要、验证签名和 quorum。
5. **owner release eligibility**：仅当以上四步全部成功，Storage 才可报告 `JOIN_PROOF_DURABLE_AND_COC_BOUND`。这只是允许各 Owner 独立执行自己的 release predicate，不是 Storage 代替 D/I/C 释放 Gate。

### 12. 冲突与 canonical-copy 规则

Storage canonical bytes 决定 JoinProof 内容；COC quorum binding 决定 COC 是否提交了该精确 Storage 记录。两者不能互相替代。Storage 不可用而 COC binding 存在、或 COC 不可用而 Storage receipt 存在，均为 UNKNOWN/BLOCKED。COC 绑定不同 ref/digest/receipt，或 Storage bytes 与 receipt/identity digest 不符，均隔离为 INTEGRITY_CONFLICT。禁止按时间戳、较新副本、缓存或最后响应自动覆盖。恢复 Storage canonical copy 只能使用认证且摘要匹配的备份，在同一 ref/identity/digest 下恢复原字节和提交 lineage；无法证明则持续隔离。COC quorum 历史只能由 COC 自行恢复。

### 13. 重试与十类崩溃

所有 retry/replay/timeout recovery 必须复用同一 `RecoveryJoinProofRef`、immutable identity、request digest；COC 同样复用原 intent/append idempotency identity。exact replay 返回原记录、原签名 receipt 和原 quorum proof。相同 identity 的 changed digest 或任何 immutable 参数变化均为 `IMMUTABLE_IDENTITY_CONFLICT`，不得覆盖或另建 identity。超时既不表示 commit，也不表示 abort；只能向各自权威查询原提交。旧 identity UNKNOWN/BLOCKED 时禁止创建新 identity 掩盖。

十个 crash window 的逐项判定以英文 §6 矩阵为规范：写前崩溃无成功 receipt；写后 receipt 丢失按同 ID 查询原 receipt；receipt 后 COC 未提交则同 COC identity 恢复；COC 成功但响应丢失则查询原 quorum proof；未达 quorum 不能由 timeout 推断 abort；COC 已提交但 Storage 回读失败保持 UNKNOWN；两侧不一致隔离；release 前崩溃必须重做双回读及 Owner currentness；identity 已存在但 digest 不同为 integrity conflict；同 identity 请求参数变化为 immutable identity conflict。

### 14. UNKNOWN/BLOCKED fail-closed

任一权威不可访问、字段缺失、签名/receipt/quorum 无法验证、quorum 未证明、日志 fork/DB incarnation 不确定、回读不线性、两侧不一致、canonical copy 不可用、timeout 未决、identity digest 冲突或参数变化，均不得 release、不得标记 epoch complete、不得按时间推断 abort。只有权威系统提供覆盖延迟写入、重试、队列、outbox、failover 和 replay 的线性化 no-commit/no-effect 证明，才可认定 NOT_COMMITTED。

### 15. 拓扑和实现边界

本规范定义跨域逻辑协议，不声称 Storage 与 COC 具有 XA/2PC 或共享原子事务。Storage/D ADR 的 L1 Option A 仅覆盖 D/Storage 序列化域；COC 仍是独立 quorum log，不得静默并入该数据库事务。本文不选择 L4 数据库/部署拓扑，不证明生产实现，不授权生产启用，也不替任何 Owner 释放 Gate。
