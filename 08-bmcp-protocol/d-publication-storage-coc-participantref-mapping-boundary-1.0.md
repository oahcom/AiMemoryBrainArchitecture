# D Publication / Storage Visibility / COC Participant Reference Mapping Boundary — 1.0

- Contract ID: `D-PUB-STORAGE-COC-REF-MAP-1.0`
- Finding: AID-2026-010 / Issue #43 / F-43-07 (P1)
- Owner: D Domain Owner
- D Owner Decision ID: `D-OWNER-2026-11-19-008`
- Status: **D-OWNED NORMATIVE DRAFT — D clauses accepted as a D proposal; Storage/COC/H clauses are proposed boundaries only; independent Owner decisions OPEN**
- Existing authorized branch: `remediation/aid-2026-001-forget-contract-closure-2026-11-18`
- D source proposal reviewed: `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md`, Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` (D branch `session-d-memory-brain-2026-11-16`)
- D producer/intent boundary reviewed: `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md`, Blob `4c01713bc8793a8926ef18b625b72d132572173d` (D branch `session-d-memory-brain-2026-11-16`)
- Storage proposal reviewed: `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md`, Blob `175ee7b1349cfdb79a19898b311a88391ed88010` (Storage branch `session-storage-consistency-forget-atomicity-2026-11-16`)
- COC/H schema material is treated as interface evidence only; it does not transfer COC or H authority to D.
- This artifact is a normative boundary draft, not a three-owner common baseline, schema freeze, topology selection, implementation proof, or production authorization.

## 1. Decision summary and non-alias rule

The three references are **distinct nominal identities** owned by different authorities:

1. `PublicationParticipantRef` is a D-owned identity for one durable, unresolved publication admission in the D publication/barrier ledger.
2. `StorageVisibilityParticipantRef` is a Storage-owned identity for one durable hidden visibility participant in the Storage visibility ledger.
3. `ParticipantIntentRef` is a COC-owned identity for one participant intent in the COC participant/quorum ledger.

They MUST NOT be the same identifier, alias, interchangeable locator, or common primary key. Similar field names, matching operation IDs, matching tuple digests, a common database, or a shared transport representation do not establish identity equality.

The proposed relation is **partial cross-domain binding, not identity mapping**:

- D binds the exact Storage ref+digest as an immutable prerequisite/evidence edge. D does not mint or rewrite the Storage identity.
- Where COC participation is required by the applicable COC contract, the COC intent may bind both the exact D publication participant ref+digest and the exact Storage visibility participant ref+digest as separate typed members/owner-admission bindings.
- A COC intent is not created by D admission, and D admission is not created by a COC quorum append. Each authority records its own fact.
- No universal one-to-one cardinality is asserted by D. The relevant Owners must define whether a COC intent can bind one or several owner admissions and whether an owner admission can participate in more than one COC transaction. Until then, ambiguous cardinality is UNKNOWN/BLOCKED.

D does not decide whether a transaction is within COC scope, who owns COC's canonical participant copy, how COC quorum is physically persisted, or which physical transaction topology is used. Those are COC/Storage-owned decisions.

## 2. Nominal identity, authority and namespace

### 2.1 D PublicationParticipantRef

Nominal type: `DPublicationParticipantRef`.

Authority: D Memory Brain / Publication Admission and ForgetFence authority.

Namespace: a stable D `PublicationParticipantLedgerId`, scoped by `BrainAuthorityId` and the D publication/barrier lineage. The namespace identity MUST be assigned and attested by D authority; it MUST NOT be inferred from a path, service name, tenant label, Storage ref, COC ref, or caller-provided string.

The immutable D identity record MUST include at least:

- D authority and PublicationParticipantLedger identity;
- `PublicationParticipantRef` and D entry digest;
- `PublicationOperationId`;
- canonical publication request digest and publication tuple digest;
- exact `StorageVisibilityParticipantRef` and Storage participant digest;
- ProducerWorkItemId and exact D RegistrationReceipt ref+digest;
- producer class/version, artifact/version/content digest;
- complete dependency receipt ref+digest and dependency-set digest;
- exact Scope and source/target lineage digests;
- DerivationRunId, AttemptId, LeaseId and LeaseEpoch;
- D-local fence generation, D admission position, state and record version.

The D ref identifies the D ledger entry; the digest identifies its immutable content. Neither one alone is a complete binding.

### 2.2 StorageVisibilityParticipantRef

Nominal type: `StorageVisibilityParticipantRef`.

Authority: Storage's visibility persistence authority.

Namespace: Storage-assigned `StorageVisibilityParticipantLedgerId`, scoped by the exact Storage authority/database incarnation/visibility domain that Storage chooses and attests. D MUST treat the ref as opaque and MUST NOT allocate its namespace, infer its physical store, or claim a Storage write occurred.

The Storage immutable identity record is expected to bind:

- Storage authority and participant-ledger identity;
- exact StorageVisibilityParticipantRef and participant digest;
- PublicationOperationId and immutable publication tuple digest;
- artifact/version/content digest and private-stage identity/digest;
- exact Storage owner-boundary and final-visibility-gate identities, if required by the Storage contract;
- durable write/prepare receipt ref+digest;
- Storage-local transaction/commit identity and database-incarnation identity;
- state, state version, and the exact transition evidence.

D's use of the ref is limited to storing and verifying the exact Storage-issued ref+digest and the evidence required by D's own admission/terminalization rules. A D receipt is not a Storage receipt.

### 2.3 COC ParticipantIntentRef

Nominal type: `COCParticipantIntentRef`.

Authority: Causal Order Coordinator (COC) participant-intent and quorum authority.

Namespace: COC-assigned `COCParticipantLedgerId` / quorum-log identity, scoped to the COC authority and transaction lineage.

The COC immutable identity record is expected to bind:

- COC authority and participant-ledger/quorum-log identity;
- exact ParticipantIntentRef and intent digest;
- COC transaction identity and request digest;
- participant tuple digest and participant owner/type;
- exact D owner-admission binding, when applicable;
- exact Storage prepared/visibility participant binding, when applicable;
- COC append position/term or equivalent opaque quorum cursor;
- quorum receipt ref+digest and the quorum configuration/epoch needed to verify it.

The COC reference and append position are COC-local. They MUST NOT be compared numerically with D admission positions, D fence generations, Storage transaction IDs, or Storage commit positions.

### 2.4 Shared correlation identity is not shared authority

`PublicationOperationId` and the canonical publication tuple digest are proposed cross-domain correlation anchors. Each domain MUST still issue its own local entry/ref/digest and maintain its own idempotency record.

A shared PublicationOperationId does not make the three refs equal, does not make one ledger authoritative for another, and does not establish that the corresponding write/append committed.

## 3. Exact immutable cross-domain binding

### 3.1 D-to-Storage binding

Before D admits a PublicationParticipantRef, D MUST resolve Storage's authoritative evidence that the exact StorageVisibilityParticipantRef is durably `PREPARED_HIDDEN`, and verify:

1. exact Storage authority and namespace identity;
2. exact Storage ref and participant digest;
3. exact PublicationOperationId;
4. exact canonical publication request digest and tuple digest;
5. exact artifact/version/content digest and private-stage binding;
6. Storage durable prepare/write receipt ref+digest;
7. Storage state/version and database-incarnation identity;
8. the Storage evidence is authenticated by the Storage authority and is not merely a caller claim or transport ACK.

D stores the ref+digest pair unchanged in its immutable participant entry. If any binding member is missing, unresolved, or contradictory, D admission is rejected or UNKNOWN/BLOCKED according to whether the contradiction is proven. D MUST NOT synthesize a Storage receipt.

### 3.2 D/Storage-to-COC binding (conditional proposal)

If the COC authority determines that this publication belongs to a COC-governed transaction, the COC intent is expected to contain distinct binding records for:

- D `PublicationParticipantRef` + D entry digest + D authority/ledger identity;
- Storage `StorageVisibilityParticipantRef` + Storage participant digest + Storage authority/ledger identity;
- common PublicationOperationId + canonical request digest + publication tuple digest;
- the COC transaction identity and COC's own participant intent digest.

The COC append receipt MUST bind the exact COC intent ref+digest and the exact included D/Storage ref+digest values. A quorum receipt that binds only a transaction ID, count, or root without resolvable member-level inclusion/consistency evidence is insufficient for an exact join.

D may verify that a COC-issued proof names its exact D ref+digest and exact operation/tuple identity. D MUST NOT claim that its own ledger proves COC append, quorum, membership, or canonical-copy correctness.

### 3.3 No silent COC alias or inferred absence

A missing COC ParticipantIntentRef MUST NOT be interpreted by D as:
- proof that no COC participant was required;
- proof that the COC transaction was never appended;
- proof of abort/no-effect;
- proof that a participant was safely removed.

If COC is outside scope, the COC authority must provide an explicit, authenticated applicability disposition (see §8). If the applicability disposition is absent or unknown, the cross-domain result is UNKNOWN/BLOCKED.

## 4. Operation identity and idempotency

The proposed immutable publication operation tuple is:

`PublicationOperationIdentity = (PublicationOperationId, CanonicalRequestDigest, PublicationTupleDigest, ArtifactVersion, ArtifactContentDigest, DependencySetDigest, ScopeDigest, SourceLineageDigest, TargetLineageDigest)`.

The exact tuple schema/version is subject to D, Storage and H review; this list is a D proposal and does not supersede their owner-owned fields.

Rules:

1. Same PublicationOperationId + same complete tuple digest within one authority namespace is an exact retry and returns/resolves the original local ref+digest and original outcome.
2. Same PublicationOperationId + changed request, tuple, artifact, dependency, scope, lineage, or participant binding is an immutable identity conflict. It MUST NOT mutate or replace the original entry.
3. Each authority maintains its own idempotency record keyed by its local namespace plus the shared operation identity. A shared key is not a shared idempotency database.
4. A repeated request that changes only a downstream ref/digest is not automatically a retry. It is a binding conflict unless the owning authority proves the prior attempt never committed and its contract explicitly authorizes a new attempt identity.
5. AttemptId/LeaseId/LeaseEpoch may change only under the relevant owner contract. They do not authorize changing the immutable publication operation tuple.
6. Replaying a terminal operation returns the exact original terminal receipt. A conflicting terminal result is an integrity conflict and must be quarantined.

## 5. Ordering and linearization boundaries

This section defines D-owned ordering and proposes cross-domain prerequisites; it does not select a physical topology or impose a COC quorum ordering that COC has not accepted.

### 5.1 D-owned linearization

D's `AdmitPublication` linearization point is the durable D ledger commit that atomically:

- validates the exact Storage PREPARED_HIDDEN ref+digest and immutable operation tuple;
- validates D RegistrationReceipt and complete dependency/lineage/Scope bindings;
- orders the admission against D InstallForgetFence in the D-authoritative ordering domain;
- records the unresolved PublicationParticipantRef in the D barrier.

Fence-first means D rejects/quarantines the admission. Admission-first means the D participant remains unresolved and holds the applicable D fence until D accepts an authoritative Storage terminal outcome. D's admission commit does not linearize Storage visibility or COC quorum append.

### 5.2 Storage-owned linearization

Storage alone defines the durable write/prepare and final visibility linearization points, their transaction boundaries, and their recovery guarantees.

D's prerequisite is that Storage's PREPARED_HIDDEN state and signed receipt are durable and independently verifiable before D admission. Storage alone decides whether that evidence is sufficient under its own authority. The final visibility commit must be bound to the exact D participant and the required pre-commit authorization evidence defined by the applicable owner contracts. D does not decide Storage's atomicity mechanism or physical topology.

### 5.3 COC-owned quorum append

COC alone defines the ParticipantIntentRef creation/append linearization point, quorum rule, canonical participant record, and append receipt.

Where COC participation is required, the COC append must bind exact immutable ref+digest pairs, not mutable aliases. The relative ordering of COC append and D admission beyond the Storage-before-D prerequisite is intentionally **UNDECIDED BY D** pending COC/Storage acceptance. No owner may infer the order from field names or an in-memory model.

## 6. Receipt, quorum append and canonical-copy binding

1. Storage's durable prepare receipt is issued only after the Storage-owned durable write/prepare has committed. It binds Storage authority, namespace, ref, participant digest, operation identity, tuple digest, state/version and database incarnation.
2. D's admission receipt is issued only after the D-owned admission/barrier commit. It binds the exact D ref+digest and the Storage ref+digest that D verified.
3. If COC participation is required, COC's quorum append receipt is issued only after the COC authority has committed the exact ParticipantIntent record to its quorum-defined durable log. It binds COC ref+digest, transaction identity, quorum checkpoint/cursor and the exact included D/Storage ref+digest pairs.
4. No receipt may be issued before its own authority's durable linearization point. A receipt from one domain is not evidence of another domain's commit.
5. The canonical copy for each record is owned by the authority that minted its ref: D owns the D entry; Storage owns the Storage participant; COC owns the COC intent and quorum append. A's integration view, H's wire copy, or another domain's cache is a projection, not a competing canonical copy.
6. Any COC canonical-copy or replica/quorum readback rule must be specified and accepted by COC. D only requires that evidence consumed by D be authenticated, exact, and resolvable.
7. For a required cross-domain join, each side must be able to read back the same exact ref+digest and immutable operation identity from the authority that owns it. Ref-only, digest-only, count-only, or transaction-ID-only matches are insufficient.
8. Storage/COC must define their own bidirectional readback and quorum-consistency requirements. D's verification of a returned proof does not substitute for Storage or COC's independent readback.

## 7. Retry, replay, changed digest and idempotency conflict

- **Exact retry before known commit:** reuse the same local idempotency identity and immutable operation tuple; query/reconcile the original operation. Do not mint a replacement participant identity merely because the response was lost.
- **Exact retry after durable commit:** return the original ref+digest and original receipt/quorum proof.
- **Same identity, changed digest:** return the owning domain's immutable-identity/idempotency conflict. Never overwrite, rebind, or silently fork the original record.
- **Duplicate COC append:** COC's own idempotency/unique constraint decides whether the exact intent is the original append or a conflict. D cannot decide the COC uniqueness rule.
- **Ref exists, proof unavailable:** UNKNOWN/BLOCKED. Do not treat a locator as proof of durability or membership.
- **Ref absent from one read:** absence is not proof of non-commit unless the owning authority supplies a linearizable absence/no-effect proof covering all delayed writes, retries, outbox work and replay paths.
- **Conflicting digest or operation identity:** quarantine the conflicting evidence and preserve both immutable observations for investigation; do not repair by changing the old digest.
- **Cross-domain retry:** each authority resolves its own original identity. No retry may replace the Storage ref, D ref or COC ref while retaining the same immutable tuple unless the owning authority's accepted contract explicitly proves a non-committed attempt and authorizes a new attempt identity.

## 8. Crash/recovery and authoritative state vocabulary

### 8.1 D-owned recovery enumeration

D proposes the following D-local state enum for its PublicationParticipantRef. It is a D ledger state, not a Storage or COC state:

- `D_ADMISSION_NOT_COMMITTED`
- `D_ADMITTED_UNRESOLVED`
- `D_TERMINAL_COMMITTED_VISIBLE`
- `D_TERMINAL_NO_PUBLICATION`
- `D_RECOVERY_UNKNOWN`
- `D_RECOVERY_BLOCKED`
- `D_INTEGRITY_CONFLICT`

Only D may issue a D-local state transition/receipt. D may enter either terminal state only after verifying the exact authoritative Storage outcome under the D contract. UNKNOWN/BLOCKED never terminalizes the D participant or releases the D barrier.

### 8.2 COC applicability and recovery enumeration (proposed for COC decision)

If the COC join is not applicable, D proposes that COC—not D—own an authenticated applicability disposition:

- `COC_JOIN_REQUIRED`
- `COC_JOIN_NOT_REQUIRED`
- `COC_JOIN_APPLICABILITY_UNKNOWN`

If required, COC additionally owns the intent lifecycle:

- `COC_INTENT_NOT_APPENDED`
- `COC_INTENT_APPENDED`
- `COC_INTENT_APPEND_UNKNOWN`
- `COC_INTENT_APPEND_CONFLICT`
- `COC_INTENT_RECOVERY_BLOCKED`

These are proposed enum labels, not a D declaration of COC's current schema. COC must define which authority issues the applicability proof, what exact scope/version it covers, and how the proof is bound to the operation and transaction. If COC does not accept this enum, it must provide its own explicit authoritative equivalent. Absence of a ParticipantIntentRef without a valid NOT_REQUIRED disposition remains UNKNOWN/BLOCKED.

### 8.3 Crash windows

- Crash before Storage durable prepare: no Storage success receipt; D MUST NOT admit.
- Crash after Storage prepare but before receipt delivery: Storage resolves the same operation identity and returns the original ref+digest/receipt; D remains not admitted or UNKNOWN until it verifies it.
- Crash after Storage prepare but before D admission: the hidden participant remains private; exact retry may continue using the same identity. It is not visible and is not a D participant until D commits admission.
- Crash after D admission but before COC append (where required): D participant remains unresolved; COC join state is UNKNOWN/NOT_APPENDED only if COC can prove it. D fence remains held.
- Crash after COC append but before quorum receipt delivery: COC must resolve the exact append by the same operation/intent identity and return the original quorum proof; no second append may create a distinct logical participant.
- Crash after Storage visibility commit but before D/COC closeout: the visible outcome is not undone by missing ACK. Storage returns the original terminal receipt; D and COC independently reconcile their own entries. Until reconciled, their relevant states remain UNKNOWN/BLOCKED and cannot be falsely marked terminal.
- Crash/restore with missing ledger continuity, stale database incarnation, forked quorum history, rollback, or unresolved digest conflict: affected authority reports UNKNOWN/BLOCKED or integrity conflict. No cached VALID, local wall clock, timeout, missing row or process death establishes abort.

### 8.4 Release condition

D releases its barrier participant only after D verifies an authoritative Storage terminal outcome and records its own immutable terminal receipt. If the applicable COC contract requires COC closeout for a separate COC barrier, COC releases that barrier only under its own accepted terminal proof. D cannot release a COC barrier, and COC cannot release D's ForgetFence barrier.

## 9. Mapping decision: partial binding, not ref identity conversion

D's proposed mapping answer is:

| Ref | Same identity as COC ParticipantIntentRef? | Proposed relation |
|---|---|---|
| D PublicationParticipantRef | **No** | Separate D-owned identity; when COC applies, a COC-owned owner-admission binding points to the exact D ref+digest and D ledger identity |
| StorageVisibilityParticipantRef | **No** | Separate Storage-owned identity; when COC applies, the COC intent separately binds the exact Storage ref+digest and Storage authority/namespace |
| COC ParticipantIntentRef | **Itself** | COC-owned intent identity and quorum-log entry; not an alias for either owner ref |

This is not a blanket exclusion of D or Storage from COC. It is an exclusion of **identity aliasing**. The exact binding cardinality, whether every D/Storage pair must be joined in one COC intent, and the applicability predicate remain subject to COC/Storage/H acceptance.

If a transaction is outside COC scope, COC must provide its authoritative `COC_JOIN_NOT_REQUIRED` disposition. If it is in scope, COC must append and prove the exact intent. If applicability or append state cannot be established, the result is UNKNOWN/BLOCKED.

## 10. D authority boundary and independent review requirements

D accepts only the D-owned propositions in this draft:

- D PublicationParticipantRef is a D-local nominal identity in a D-owned namespace.
- D admission requires exact, authenticated Storage PREPARED_HIDDEN ref+digest evidence.
- D admission and InstallForgetFence linearize in D's own ordering domain.
- D's participant remains unresolved until D verifies an authoritative Storage terminal outcome.
- D retries/replays preserve the immutable operation identity; changed digest is conflict.
- D UNKNOWN/BLOCKED never closes the D participant or releases the D barrier.
- D does not mint, rename, rewrite, or own StorageVisibilityParticipantRef or COC ParticipantIntentRef.

The following are **proposals requiring independent owner disposition**, not D decisions:

- Storage's identity schema, authority/namespace, durable-write receipt, transaction boundary, canonical copy, bidirectional readback, retry/crash recovery and visibility release conditions;
- COC's identity schema, authority/namespace, participant cardinality, quorum append, canonical participant record, applicability/recovery enum and quorum readback;
- H's consumer mapping, wire encoding, currentness/status scope, stale/invalid/unknown treatment and fail-closed behavior;
- any physical topology, XA/2PC arrangement, database engine, distributed lock, quorum implementation or cross-domain transaction guarantee.

### Required Storage Owner review on this exact Blob

Storage must issue ACCEPT / ACCEPT WITH LIMITATIONS / REJECT for the Storage-owned clauses in §§2.2, 3.1–3.2, 5.2, 5.3, 6, 7 and 8, identifying exact clauses, authority/namespace, durable write-to-receipt binding, COC quorum ref/digest binding, canonical-copy and bidirectional readback rules, retry/idempotency/crash recovery, and visibility release conditions. A rejection/limitation must include replacement wording or a precise unresolved dependency.

### Required H Owner review on this exact Blob

H must issue ACCEPT / ACCEPT WITH LIMITATIONS / REJECT for consumer mapping and interpretation in §§3.1–3.3, 4, 6–9, including publication/visibility identity binding, currentness/status scope, receipt/quorum evidence requirements, stale/invalid/unknown classification, retry/replay/recovery, and fail-closed handling of incomplete evidence. H does not decide D or Storage write authority.

### A Integration gate

A may conduct cross-domain integration review only after D, Storage and H have each recorded an explicit decision against this **same exact Blob SHA**, with separate Decision IDs, exact branch/commit/Blob pins, limitations and rejection reasons. A's integration decision does not substitute for any Owner's decision.

F-43-07 remains OPEN/BLOCKED until the complete closure criteria in the governing dispatch are independently satisfied. This draft alone does not close the Finding.

## 11. Decision and evidence boundary

**D Owner Decision ID:** `D-OWNER-2026-11-19-008`

**Disposition:** D Owner ACCEPTS the D-owned identity/authority boundary and D-owned admission/recovery semantics as a normative D proposal, and submits §§2.1, 3.1, 5.1, 7 (D-owned idempotency effects), 8.1, 8.3 (D effects only), 8.4 and 9 for independent cross-owner review. This is not an acceptance on behalf of Storage, COC or H.

No production implementation, signed Storage receipt, COC quorum append, COC canonical-copy proof, physical topology, H consumer acceptance, cross-domain test, or runtime conformance is asserted by this document.

F-43-07 remains OPEN/BLOCKED pending Storage and H independent dispositions on the exact Blob, any required owner amendments, and A Integration's subsequent exact-version review.

## 12. 中文规范摘要（与英文条款同等效力）

### 12.1 三种身份不得别名

- D `PublicationParticipantRef`：D Publication/ForgetFence Ledger 中一个持久化未完成发布准入项的 D-owned 身份。
- Storage `StorageVisibilityParticipantRef`：Storage Visibility Ledger 中一个持久化隐藏可见性参与项的 Storage-owned 身份。
- COC `ParticipantIntentRef`：COC Participant/Quorum Ledger 中一个参与意图的 COC-owned 身份。

三者是不同 nominal type、不同 authority、不同 namespace。不得因为字段名称、操作 ID、Tuple Digest、同库或传输格式相同而视为同一身份。

### 12.2 采用部分绑定，不采用身份合并

D 仅保存并验证 Storage 权威签发的精确 ref+digest；D 不创建 Storage ref，不签发 Storage receipt。若交易属于 COC 适用范围，COC 可以在其自有 ParticipantIntent 中分别绑定精确 D ref+digest 与 Storage ref+digest。COC Intent 不等于 D Admission，也不等于 Storage Participant。是否适用 COC、绑定基数和 COC 规范副本由 COC/Storage/H 按各自权限裁决，D 不单方决定。

### 12.3 身份与摘要绑定

所有跨域关联必须绑定 PublicationOperationId、规范 Request Digest、Publication Tuple Digest，以及各领域自己的 ref、entry digest、authority、namespace 和 receipt/proof。共享操作 ID 仅是关联锚点，不是共享主键、共享幂等库或跨域提交证明。Ref-only、Digest-only、Count-only 或 Transaction-ID-only 均不足以建立精确 Join。

### 12.4 顺序与线性化

Storage 自己决定 Durable Prepare/Write 和最终 Visibility Commit 的线性化点；D 自己决定 Publication Admission 与 InstallForgetFence 的 D-local 线性化点；COC 自己决定 ParticipantIntent Append 和 Quorum 的线性化点。D 只规定 Storage 的 PREPARED_HIDDEN 证据必须先于 D Admission。D 不决定 COC append 与 D admission 的相对顺序，也不决定物理事务拓扑。

### 12.5 重试、崩溃与恢复

同一身份和同一完整摘要重试必须解析原记录并返回原 ref+digest/receipt；同一身份但摘要变化必须冲突，不得覆盖或重绑。丢失 ACK 不等于 abort。D Admission 后崩溃、COC append 后丢失 quorum ACK、Storage 可见性提交后尚未 closeout，都必须由各自权威按同一身份恢复原结果。无法证明提交、未提交、日志连续性或无延迟重放时一律 UNKNOWN/BLOCKED。

D 提议 D-local 恢复枚举：`D_ADMISSION_NOT_COMMITTED`、`D_ADMITTED_UNRESOLVED`、`D_TERMINAL_COMMITTED_VISIBLE`、`D_TERMINAL_NO_PUBLICATION`、`D_RECOVERY_UNKNOWN`、`D_RECOVERY_BLOCKED`、`D_INTEGRITY_CONFLICT`。COC 适用性与 COC append 恢复枚举必须由 COC 自己接受或提供等效枚举；没有经认证的 `COC_JOIN_NOT_REQUIRED` 证明时，不得把缺少 ParticipantIntentRef 解释为无需 COC。

### 12.6 决策边界

本文件是 D Owner 的规范性草案。D 只接受 D 自有身份、准入、D Fence 顺序、D 幂等和 D 恢复语义。Storage 必须独立决定其持久化/receipt/quorum binding/canonical-copy/readback/retry/crash/visibility release 语义；H 必须独立决定消费侧映射、status/currentness、证据消费和 fail-closed 语义。三方必须对同一精确 Blob 独立接受后，A 才可集成复审。F-43-07 仍 OPEN/BLOCKED。
