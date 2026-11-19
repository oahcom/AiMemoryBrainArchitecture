# COC Owner Decision — F-43-07 Applicability of ParticipantIntent to D Publication / Storage Visibility Participants

- Decision ID: `COC-OWNER-2026-11-19-001`
- Work Item: `AID-2026-013`
- Accountable Owner: COC Owner
- Status: **COC-OWNED NORMATIVE APPLICABILITY DECISION**
- Disposition: **NOT_REQUIRED — strictly bounded operation/scope/version**
- COC profile evaluated: `CausalOrderProfile/1.0`
- D contract evaluated: `D-PUB-STORAGE-COC-REF-MAP-1.0`
- Decision carrier: `recovery/c-owner-tree-2026-11-18`
- Authorization: explicit user authorization to use this existing carrier; no new branch/PR/Issue and no main/finding-ledger mutation.

## 1. Decision and exact scope

COC decides **NOT_REQUIRED** for a COC `ParticipantIntentRef` for the following operation family, and only this family:

> The D-owned publication-admission lifecycle identified by one `PublicationOperationId`, comprising (a) Storage's `StorageVisibilityParticipantRef` creation/prepare as `PREPARED_HIDDEN`, (b) D's `PublicationParticipantRef` admission into the D publication/barrier ledger, and (c) the corresponding Storage visibility terminalization and D participant closeout, as described by D contract `D-PUB-STORAGE-COC-REF-MAP-1.0` (exact D Blob below), **provided that this operation is not itself a protected C final-request/provider side effect, does not consume or terminalize an I authorization receipt, and is not a JF-10 prepared-participant/XID bridge operation under CausalOrderProfile/1.0**.

The negative applicability is exact to this operation family and these source versions:

1. D contract: `08-bmcp-protocol/d-publication-storage-coc-participantref-mapping-boundary-1.0.md`, D decision `D-OWNER-2026-11-19-008`, commit `8fbef916785986fa1867ddf2eb3e3a5e4b366c5e`, Blob `05a24f7eab663f66a3153d79adfab699b275f1a6`.
2. Storage Stage 2 disposition: `STORAGE-OWNER-2026-11-20-002`, **ACCEPT WITH LIMITATIONS**, on that exact D Blob (Issue #43 comment `7023315618`; A R43 confirmation `7023454401`).
3. H Stage 3 disposition: `H-OWNER-2026-11-20-001`, **ACCEPT WITH LIMITATIONS**, on that exact D Blob; H requires authenticated `COC_JOIN_NOT_REQUIRED` evidence for the exact scope/version/operation (Issue #43 comment `7023562083`; H artifact Blob `19e3dce92aa6d843d3d8d63b21f843eb30770b0f`).
4. COC causal-order architecture: `CausalOrderProfile/1.0`, A architecture `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, especially §§1–5 and 12.
5. C Owner provider-boundary contract: `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, Blob `45a48249717c8cddb07ab96197730ef93d406c22`.

This decision is **not** a blanket exclusion for every object called Publication, every Storage visibility operation, every transaction containing a D or Storage reference, or every future version of these contracts. It does not apply if any exclusion condition above is false, cannot be established, or the operation's scope/version changes.

## 2. Applicability rationale

COC's `CausalOrderProfile/1.0` is a cross-owner causal-order and participant-accounting mechanism for protected final-request/provider submission, I authorization/revocation ordering, D ForgetFence ordering, and the specifically defined JF-10 prepared-participant bridge. It is not a universal transaction coordinator for every D publication or Storage visibility ledger entry.

The scoped D/Storage publication lifecycle has its own owner-local facts and linearization points:
- Storage issues and owns the `StorageVisibilityParticipantRef` and its durable `PREPARED_HIDDEN` evidence.
- D issues and owns the `PublicationParticipantRef` and its publication/barrier admission.
- Storage owns its visibility terminal outcome; D owns its barrier/participant terminalization.
- The D contract requires Storage's exact authenticated `PREPARED_HIDDEN` ref+digest evidence before D admission.

The existence of a shared `PublicationOperationId`, request digest, tuple digest, or two owner references does not by itself establish a COC-governed protected transaction. The three references remain distinct nominal identities. This decision excludes only the requirement to create a third COC participant intent for the narrowly scoped D/Storage lifecycle; it does not alias, merge, replace, or weaken either owner record.

## 3. Certified negative applicability evidence

For each concrete operation in this scope, consumers MUST obtain and validate an immutable COC-issued `COC_JOIN_NOT_REQUIRED` disposition before treating the absence of `ParticipantIntentRef` as intentional or declaring the cross-domain applicability join complete.

The disposition record MUST bind, without wildcard or inferred values:

- disposition type/version and value `NOT_REQUIRED`;
- this Decision ID and exact COC decision/profile version;
- exact D contract identity/version and D authority/ledger identity;
- exact `PublicationOperationId`, canonical request digest and publication tuple digest;
- exact `PublicationParticipantRef` + D entry digest + D authority/ledger namespace, once D has admitted;
- exact `StorageVisibilityParticipantRef` + Storage participant digest + Storage authority/namespace/incarnation;
- explicit scope classification proving the operation is the D/Storage publication lifecycle described in §1;
- explicit negative predicates: no protected C provider side effect, no I authorization-receipt consumption/terminalization, and no JF-10 prepared-participant/XID bridge;
- issuer COC authority, disposition identity/digest, key/profile reference, issue/currentness metadata and verifiable COC authentication evidence.

The concrete disposition is immutable and idempotent. Exact same operation identity and complete digest returns the original disposition identity/evidence. Same identity with changed request/tuple/ref/digest/scope/version is a conflict; it MUST NOT be overwritten or silently reclassified. A changed operation or contract version requires a new applicability evaluation.

This document defines the semantic evidence contract only. It does not invent or freeze a cryptographic algorithm, wire encoding, key-management policy, production signer, endpoint, or deployed COC service. Those remain subject to the existing COC/H security and implementation gates. Until the COC-issued evidence can be authenticated and resolved, consumers MUST classify applicability as **UNKNOWN/BLOCKED**, not NOT_REQUIRED.

No `ParticipantIntentRef`, participant member, quorum append, quorum position, or quorum certificate is created for an operation validly covered by this NOT_REQUIRED disposition. The negative disposition is not a synthetic participant intent and is not a quorum proof.

## 4. Equivalent owner-local ordering and recovery boundary

The absence of a COC participant intent does not remove either owner's independent ordering or recovery obligations. The following preserves the already-owned D and Storage boundaries; it does not amend their semantics.

### 4.1 Required order

1. Storage durably creates the exact hidden visibility participant and issues its authenticated `PREPARED_HIDDEN` receipt for the immutable operation identity.
2. D verifies the exact Storage authority, namespace/incarnation, `StorageVisibilityParticipantRef`, participant digest, `PublicationOperationId`, request/tuple digests and prepare receipt.
3. D commits its own `PublicationParticipantRef` admission and D-local barrier/fence ordering.
4. Storage alone commits and attests the visibility terminal outcome under its own accepted contract.
5. D independently verifies that exact Storage terminal outcome and commits its own terminal/closeout record.

There is no COC append between these steps for the §1 operation family. COC does not choose or compare D and Storage local sequence numbers, transaction IDs, fence generations, or commit positions. The required Storage-before-D admission edge remains the D-owned prerequisite; it is not replaced by a COC quorum position.

### 4.2 Crash and recovery states

- **Crash before Storage prepare:** no Storage success receipt exists; D MUST NOT claim admission based on a caller assertion.
- **Storage prepare committed, receipt response lost, D admission not committed:** Storage resolves the same immutable operation identity and returns the original ref/digest/receipt. The participant remains hidden; D has not admitted it until D commits its own record.
- **D admission committed, Storage visibility terminal outcome not yet proven:** the D participant remains unresolved and the D barrier remains held. Recovery queries Storage by the same exact identity; no timeout, missing row, process death or missing COC intent proves abort.
- **Storage visibility terminal outcome committed, D closeout/ACK lost:** Storage returns the original terminal evidence; D independently reconciles and closes only its own record after verification. The visibility fact is not rewritten by a lost response.
- **COC NOT_REQUIRED disposition missing, stale, unauthenticated, mismatched, or unavailable for authoritative resolution:** cross-domain applicability remains UNKNOWN/BLOCKED. Absence of `ParticipantIntentRef` MUST NOT be inferred as NOT_REQUIRED. This classification does not authorize either D or Storage to bypass its own local gates.
- **Conflicting identity/digest, stale authority incarnation, incomplete ledger continuity or unprovable owner state:** affected owner remains UNKNOWN/BLOCKED or records its own integrity conflict; no timestamp/cache selection or replacement identity is permitted.

### 4.3 Retry and idempotency

The D/Storage operation retains the same `PublicationOperationId`, complete canonical request/tuple digest, and each authority's original immutable reference/digest. Exact replay resolves the original owner record and receipt. Same identity with changed semantic content, scope, version or cross-owner binding is a conflict. A new D ref, Storage ref, COC intent or transaction MUST NOT be minted merely to escape an unresolved attempt.

## 5. Boundary where COC IS required

This NOT_REQUIRED disposition ceases to apply if the operation is joined to any of the following:

1. A protected C final-request/provider side effect governed by `CausalOrderProfile/1.0`.
2. An I authorization receipt issuance/consumption or I revocation ordering obligation that must be causally joined to the same protected operation.
3. The JF-10 prepared-participant/XID bridge, including the COC pre-prepare intent and prepared-participant registration sequence in COC architecture §12.
4. Any successor contract or explicit owner-approved scope that requires COC participant accounting for this operation.

In those cases, COC applicability is **APPLICABLE** for the protected composite transaction. The applicable COC contract must then define/validate the ParticipantIntent schema/cardinality, quorum and threshold, exact typed member bindings, append ordering, quorum proof, recovery and same-identity idempotency. This decision does not pre-approve those semantics or supply a substitute schema/quorum algorithm. A missing or unverified required intent remains UNKNOWN/BLOCKED and no protected side effect may proceed.

Where scope classification is ambiguous, mixed, or cannot prove all three negative predicates in §3, fail closed: do not use this NOT_REQUIRED disposition.

## 6. Authority and non-interference

- This is a COC-owned applicability decision only. It does not modify D publication/barrier semantics, Storage visibility/prepare/terminal semantics, H wire/consumer semantics, or I authorization semantics.
- Storage's `StorageVisibilityParticipantRef` prepare receipt remains distinct from the F-43-06A `RecoveryJoinProof` durable receipt. This decision does not alter Storage's canonical RecoveryJoinProof bytes or COC's separate quorum-binding authority for that different object.
- The D, Storage and H decisions remain bounded to their exact accepted D Blob and enumerated limitations.
- No production implementation, real COC signer, quorum append, runtime conformance, deployment, or production authorization is asserted.
- F-43-07 remains subject to A Integration's independent exact-version review. This decision alone does not close the Finding.

## 7. 中文规范裁定（与英文条款同等效力）

### 7.1 裁定与精确范围

COC 对以下操作范围裁定 **NOT_REQUIRED**：以一个 `PublicationOperationId` 标识的 D Publication Admission 生命周期，包括 Storage 创建/准备 `PREPARED_HIDDEN` 的 `StorageVisibilityParticipantRef`、D 写入 `PublicationParticipantRef` Admission，以及相应的 Storage Visibility Terminalization 和 D Participant Closeout；其依据仅限 D 契约 `D-PUB-STORAGE-COC-REF-MAP-1.0` 的精确 Blob `05a24f7eab663f66a3153d79adfab699b275f1a6`。

该裁定成立的必要条件是：此操作本身不是受保护的 C Final-Request/Provider Side Effect；不消费或终结 I Authorization Receipt；不是 `CausalOrderProfile/1.0` 下的 JF-10 Prepared-Participant/XID Bridge。

本裁定不是对所有 Publication、Storage Visibility 或未来版本的普遍排除。任何条件不成立、无法证明或版本发生变化，本裁定均不适用。

### 7.2 适用性理由

`CausalOrderProfile/1.0` 的 COC 是受保护 Final-Request/Provider Submit、I Authorization/Revocation、D ForgetFence 因果排序及明确规定的 JF-10 Bridge 的跨 Owner 排序与 Participant Accounting 服务；不是所有 D Publication 或 Storage Visibility Ledger 的通用事务协调器。

本范围内 Storage 自己签发并拥有 `StorageVisibilityParticipantRef` 与 `PREPARED_HIDDEN` 证据；D 自己签发并拥有 `PublicationParticipantRef` 与 D Publication/Barrier Admission；Storage 拥有 Visibility Terminal Outcome，D 拥有自己的 Barrier/Participant Terminalization。共享 `PublicationOperationId` 或 Tuple Digest 不会自动使其成为 COC 管辖的受保护事务。

### 7.3 认证 NOT_REQUIRED 证明

每个具体操作都必须取得并验证 COC 签发的不可变 `COC_JOIN_NOT_REQUIRED` 处置记录，才能把缺少 `ParticipantIntentRef` 解释为有意不适用。证明必须精确绑定本 Decision ID、COC Profile、D 契约版本、PublicationOperationId、Request/Tuple Digest、D ref+digest、Storage ref+digest、双方 Authority/Namespace/Incarnation，以及“不存在受保护 C Provider Side Effect、I Receipt 消费/终结、JF-10 Bridge”的明确范围判定。

相同身份和完整摘要重试必须返回原证明；同一身份但摘要、范围、版本或引用变化必须冲突，不得覆盖。证明缺失、过期、未认证或无法解析时，状态必须是 UNKNOWN/BLOCKED，不得推断 NOT_REQUIRED。

本裁定定义语义证据，不冻结密码算法、Wire Encoding、密钥管理、生产签名者或部署服务。

### 7.4 等价恢复边界

不创建 COC ParticipantIntent，不做 COC quorum append；但 Storage 仍必须先持久化并证明准确的隐藏准备，D 随后验证精确 Storage ref+digest 并提交自己的 Admission。Storage 独立提交 Visibility Terminal Outcome，D 独立验证并关闭自己的 Participant/Barrier。

Storage 准备后丢失 ACK，使用同一操作身份解析原 receipt；D Admission 后 Storage Outcome 未确定，D Barrier 保持未完成；Storage 已提交 Visibility 但 D closeout ACK 丢失，按原 Storage Terminal Evidence 恢复。COC NOT_REQUIRED 证明缺失或不可验证时，跨域适用性仍为 UNKNOWN/BLOCKED。不得用缺少 COC 行、超时、缓存或进程死亡推断未提交。

### 7.5 重新适用 COC 的边界

若同一操作进入受保护 C Provider Submit、I Authorization/Revocation 因果排序、JF-10 Prepared-Participant/XID Bridge，或后继 Owner 契约明确要求 COC Participant Accounting，则本 NOT_REQUIRED 不适用；对该受保护复合事务 COC 为 APPLICABLE，必须另按适用 COC 契约定义 Schema/Cardinality、Quorum/Threshold、精确绑定、Append 顺序、Proof、Recovery 和幂等。范围不明时一律 UNKNOWN/BLOCKED。

### 7.6 不干涉与后续门禁

本裁定不修改 D、Storage、H 或 I 的域内语义，不混淆 StorageVisibilityParticipantRef 的 PREPARED_HIDDEN Receipt 与 F-43-06A RecoveryJoinProof Receipt，不宣称生产实现或实际 Quorum 已完成。F-43-07 仍须交 A Integration 对精确版本独立复审；本决定本身不关闭 Finding。

## 8. Decision record

- Decision ID: `COC-OWNER-2026-11-19-001`
- Disposition: **NOT_REQUIRED**, bounded exactly by §§1 and 7.1.
- COC profile: `CausalOrderProfile/1.0`.
- D source Blob: `05a24f7eab663f66a3153d79adfab699b275f1a6`.
- Storage Stage 2: `STORAGE-OWNER-2026-11-20-002`, ACCEPT WITH LIMITATIONS.
- H Stage 3: `H-OWNER-2026-11-20-001`, ACCEPT WITH LIMITATIONS.
- A integration predecessor: `A-OWNER-INTEGRATION-R44-2026-11-20`; A review remains the next gate.
- No new PR/Issue/branch; no main or finding-ledger modification.
