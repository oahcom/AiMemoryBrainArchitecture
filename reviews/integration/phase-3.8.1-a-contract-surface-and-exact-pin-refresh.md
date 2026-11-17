# Phase 3.8.1 — A Contract-Surface Reconciliation and Exact-Pin Refresh

- Owner role: A — Principal Integration Architect (integration-session role simulation)
- Status: **PROPOSED CONTRACT SURFACE; NOT OWNER-APPROVED, NOT FROZEN**
- Language: English and Chinese are normative peers.
- Supersedes: only the stale D/E/Storage source pins in the earlier Phase 3.8 A report and Issue #25. It does not silently amend the owner artifacts.

## 1. Why this addendum exists

A fresh read of the four owner branches found that D, E and Storage had advanced after the Phase 3.8 report was written. The earlier A report and Issue #25 therefore no longer identified the current exact source blobs. This addendum pins the files actually read and defines a conservative cross-owner contract surface for the next owner-exact review.

### 1.1 Current exact source pins

| Role | Branch | Path | Current Blob SHA | Readback |
|---|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` | `4c01713bc8793a8926ef18b625b72d132572173d` | fetched from branch in this review |
| E | `session-e-memory-compiler-2026-11-16` | `04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` | fetched from branch in this review |
| I | `session-i-security-governance-2026-11-16` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` | fetched from branch in this review |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md` | `2ab899ee37a18ae6c8f2f64dbb82ad6499842060` | fetched from branch in this review |

The previous D `206ead...`, E `bad04d...`, and Storage `1ad895...` pins are superseded for all future reviews. I's pin remains unchanged. The earlier A report is retained as historical evidence; this addendum is the current pin correction.

## 2. Cross-owner semantic decisions retained

1. EventRef-only ProducerWork may be registered by D before Canonical MemoryRef exists only when authenticated producer binding, enabled ProducerClass/version, exact Scope, canonical request digest and D-approved opaque lineage token/digest are complete. D registration is barrier-counted. This does not authorize protected payload dereference. E must link exact canonical refs/revisions before dependency registration/publication.
2. Register-before-work remains mandatory: D durable RegistrationReceipt precedes queue insertion, lease, protected source dereference, execution, retry/replay or publication.
3. Complete dependency registration is an immutable complete-set operation. Partial sets never produce a dependency-complete receipt and cannot publish.
4. Retry preserves ProducerWorkItemId and request digest; AttemptId/LeaseId are attempt-scoped and fenced. Changed logical input or compiler configuration requires a new DerivationRun/input identity and fresh gates.
5. The final visibility boundary is conjunctive: current D publication participant/fence, the pre-commit I sequencer consumption proof (`CommitAuthorizationReceipt` / `ICommitAuthorizationProof`), and the exact durable Storage participant. Post-commit `ITerminalProof` is not a precondition to visibility. No detached reusable token authorizes a later write.
6. Crash-safe ordering is **Storage hidden durable participant → D PublicationParticipant admission → I single-use receipt consumption → Storage final visibility commit → D/I independent closeout**.
7. UNKNOWN/IN_DOUBT remains private and barrier-open. Missing rows, timeout, lease expiry, process death, age, stale replicas, queue deletion and lost ACK never imply abort or success.
8. D PublicationParticipantRef, I CommitAuthorizationReceipt, StorageVisibilityParticipantRef, C ParticipantIntentRef and Storage PreparedParticipantRef/GID/XID are distinct nominal types and idempotency scopes.

## 3. Proposed typed contract surface (candidate, not frozen schema)

The following is the minimum logical field set needed to make the owner proposals implementable and testable. Field names are descriptive placeholders; H must later define canonical wire names, encoding, signature profile and compatibility rules. No numeric D/I positions are compared across authority domains.

### 3.1 Shared immutable publication tuple

`PublicationTuple`:
- `publication_operation_id`: globally unique opaque operation identity, never recycled.
- `publication_request_digest`: digest over the canonical immutable request.
- `producer_work_item_id` and `d_registration_receipt_ref`.
- `derivation_run_id`, `attempt_id`, `lease_id`, and `lease_epoch`.
- `artifact_ref`, `artifact_version`, and `artifact_content_digest`.
- `dependency_registration_receipt_ref` and `complete_dependency_set_digest`.
- `scope_ref` and exact source/target lineage digest.
- `producer_class_id` and `producer_class_version`.
- `private_stage_ref` (opaque; never a public serving locator).
- `canonicalization_profile_id` and `digest_algorithm_id`.

All participants must bind the same tuple digest. A participant may add authority-local fields, but may not reinterpret or weaken the tuple.

### 3.2 Storage prepare record and result

`StorageVisibilityParticipant` (Storage authority):
- `storage_visibility_participant_ref`
- `publication_operation_id`, `publication_request_digest`, `publication_tuple_digest`
- `private_stage_ref`, `artifact_ref`, `artifact_version`, `artifact_content_digest`
- `producer_work_item_id`, `attempt_id`, `lease_id`, `lease_epoch`
- `dependency_registration_receipt_ref`, `complete_dependency_set_digest`
- `state`: PREPARED_HIDDEN | COMMITTED_VISIBLE | NO_PUBLICATION | UNKNOWN
- `storage_transaction_ref`, `created_at`, `record_version`

Prepare is durable and hidden. It creates no serving pointer, public URL or authorization. Exact replay (same operation ID and tuple digest) returns the same participant; changed digest is IMMUTABLE_IDENTITY_CONFLICT. D admission is forbidden until Storage can authoritatively resolve this participant as durable PREPARED_HIDDEN.

### 3.3 D publication admission and terminal evidence

`DPublicationParticipant`:
- `publication_participant_ref`
- exact `storage_visibility_participant_ref`
- `publication_operation_id`, `publication_request_digest`, `publication_tuple_digest`
- `producer_work_item_id`, `d_registration_receipt_ref`
- `artifact_ref`, `artifact_version`, `complete_dependency_set_digest`
- `scope_ref`, `attempt_id`, `lease_id`, `lease_epoch`
- D-local `fence_generation`, `admission_position`, `state`: ACTIVE | COMMITTED_VISIBLE | NO_PUBLICATION | UNKNOWN

D admission must verify the exact Storage participant is durably PREPARED_HIDDEN, all dependency receipts are complete, the attempt/lease is current, and the D fence ordering permits admission. Fence-first rejects. Admission-first creates an unresolved D barrier participant, not visibility permission.

D terminalization accepts only authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION evidence for the same participant and tuple digest. D may not infer terminality from I COMMIT_WON or from missing Storage state.

### 3.4 I single-use authorization receipt and terminal proof

`CommitAuthorizationReceipt`:
- `authorization_receipt_ref`, `receipt_nonce`
- `policy_domain_ref`, `policy_version_ref`, `issuer_key_id`, `issuer_key_version`, `issuer_key_status_ref`
- authenticated `subject_ref`, `actor_ref`, `workload_ref` and delegation-chain digest
- `owner_boundary_ref`, `final_visibility_gate_ref`
- exact `publication_operation_id`, `publication_tuple_digest`
- exact `storage_visibility_participant_ref`, `publication_participant_ref`
- `subject_ref`, `purpose`, `audience`, `scope_ref`, `environment_ref`
- I-local `permission_epoch`, `sequencer_position`
- `consumption_result`: COMMIT_WON | REVOCATION_WON | UNKNOWN (sequencer result; not a caller-selected claim)
- `sequencer_position`, `consumed_at`, `issued_at`, `accept_before`
- `signature_profile_id`, `signature`

The logical receipt is the signed, single-use sequencer result and is the pre-commit ICommitAuthorizationProof. `ITerminalProof` is a separate post-commit closeout proof. If the implementation separates an authorization request/token from the consumption result, those MUST be distinct nominal types; do not put a caller-supplied decision into a signed bearer token. I consumes the authorization exactly once in its PolicyDomain sequencer. Revocation-first yields REVOCATION_WON. COMMIT_WON creates an unresolved I participant and holds subsequent applicable revocation until the same Storage terminal outcome. UNKNOWN holds. `accept_before` constrains first consumption only; it cannot expire or release an already-consumed COMMIT_WON participant. A consumed receipt is not a bearer token for an independent Storage write.

`ITerminalProof` binds the receipt, both participant refs, tuple digest and exact Storage outcome proof. I closes only after validating COMMITTED_VISIBLE or authoritative NO_PUBLICATION. Issuer/key status, policy version, audience, replay and anti-rollback rules remain I/H owner decisions and are not silently decided here.

### 3.5 Storage final outcome

`StorageVisibilityOutcome`:
- `publication_operation_id`, `publication_tuple_digest`
- exact `storage_visibility_participant_ref`, `publication_participant_ref`, `authorization_receipt_ref`
- `outcome`: COMMITTED_VISIBLE | NO_PUBLICATION | UNKNOWN
- `visibility_transaction_ref`, `visibility_pointer_ref` (required only for COMMITTED_VISIBLE)
- exact D current-participant/fence proof reference
- exact pre-commit ICommitAuthorizationProofRef (the consumed CommitAuthorizationReceipt; distinct from post-commit ITerminalProof)
- `outbox_event_ref`, `committed_at`, `outcome_digest`

The visibility linearization point is the durable transaction that validates the exact D participant/fence proof and ICommitAuthorizationProof, then changes the authoritative visibility pointer/outcome atomically. NO_PUBLICATION requires positive authoritative proof that no visibility pointer was installed and no delayed publisher/outbox/retry can later install it. UNKNOWN has no terminal semantics and leaves the artifact private.

### 3.6 E orchestration state

E retains local ownership of CompileIntent, immutable compiler input bundle, DerivationRun, Attempt/Lease, private staging and output accounting. Its orchestration must preserve:
- D registration before queue/lease/execute;
- Storage prepare before D publication admission;
- D admission before I receipt consumption;
- I receipt before Storage final visibility commit;
- same operation/tuple digest across retries and recovery;
- fresh attempt/lease fencing and fresh current D/I checks where a new publication attempt is created;
- no E-local receipt or queue ACK interpreted as D/I/Storage authority evidence.

## 4. Required operation surface and idempotency

| Operation | Authority | Idempotency key | Success evidence | Non-success |
|---|---|---|---|---|
| RegisterProducerWork | D | WorkItemId + request digest | D RegistrationReceipt + D registration position | REJECTED / QUARANTINED / UNKNOWN |
| InstallForgetFence | D | ForgetOperationRef + target digest | immutable fence + captured registration high-water | UNKNOWN blocks admission |
| RegisterDerivedDependencySet | D (E supplies complete set) | dependency registration ID + complete-set digest | complete D DependencyRegistrationReceipt | INCOMPLETE / CONFLICT / UNKNOWN |
| PrepareVisibility | Storage | PublicationOperationId + tuple digest | durable hidden StorageVisibilityParticipantRef | CONFLICT / UNKNOWN |
| AdmitPublication | D | PublicationOperationId + tuple digest | D PublicationParticipantRef bound to Storage ref | FENCE_WON / REJECTED / UNKNOWN |
| ConsumeCommitAuthorization | I | receipt nonce + tuple digest | COMMIT_WON / REVOCATION_WON terminal sequencer result | REPLAY / REVOKED / UNKNOWN |
| CommitVisibility | Storage | PublicationOperationId + tuple digest | COMMITTED_VISIBLE or authoritative NO_PUBLICATION | UNKNOWN remains hidden |
| CloseDParticipant | D | PublicationParticipantRef + Storage outcome digest | D terminal receipt | HOLD / UNKNOWN |
| CloseIParticipant | I | authorization receipt + Storage outcome digest | I terminal proof | HOLD / UNKNOWN |
| CompleteProducerWork | D (E supplies inventory) | WorkItemId + final inventory digest | D terminal work receipt | OPEN / UNKNOWN |

Every mutating operation must define same-key/same-digest replay, same-key/different-digest conflict, response-loss resolution and authority-local monotonicity. Idempotency records must outlive all retry/replay/restore horizons; retention policy cannot permit identity reuse.

**Retry identity rule:** a transport retry, lost-ACK resolution or recovery replay of the *same immutable publication attempt* reuses the same PublicationOperationId, tuple digest and participant identities. A new publication attempt after authoritative NO_PUBLICATION (or a changed artifact/version, dependency set, Scope, source revision or attempt/lease tuple) is a new immutable operation: allocate a new PublicationOperationId, new participant identities, new tuple digest and fresh D/I checks. Never reuse one operation ID with a changed digest, and never rewrite a historical terminal outcome.

## 5. Error and recovery vocabulary

Minimum distinct outcomes:
- `REJECTED`: authoritative policy/fence/identity denial; no side effect beyond durable rejection evidence.
- `QUARANTINED`: insufficient or unresolved evidence; no queue/lease/execute/visibility capability.
- `IMMUTABLE_IDENTITY_CONFLICT`: same idempotency identity with changed canonical digest.
- `FENCE_WON`: D fence linearized before publication admission.
- `REVOCATION_WON`: I revocation linearized before receipt consumption.
- `STALE_ATTEMPT`: attempt/lease epoch is no longer current.
- `INCOMPLETE_DEPENDENCY_SET`: dependency set not complete; no receipt and no publication.
- `UNKNOWN` / `IN_DOUBT`: cannot prove terminal outcome; preserve private state and all admitted barriers.
- `COMMITTED_VISIBLE`: authoritative visibility commit proof.
- `NO_PUBLICATION`: authoritative terminal proof that publication did not occur and cannot occur later.

Do not collapse UNKNOWN into retryable abort. A retry after proven NO_PUBLICATION uses fresh D/I checks and a new attempt as required; it must not mutate the historical outcome.

## 6. Role-simulated exact-Blob review (not independent Owner signatures)

The following dispositions are this integration session's independent analytical passes over the four current Blob pins in §1. They are not GitHub approvals by the named Owners.

| Role lens | Disposition | Findings / required amendments |
|---|---|---|
| D | ACCEPT WITH ENUMERATED AMENDMENTS (semantic composition only) | Current D Blob explicitly requires durable Storage participant before D admission and binds the exact Storage ref. Keep D fence/admission ordering in one D authority domain. Before freeze, D must publish exact request/receipt/terminal schemas, stable operation names, and exact behavior for rejection, replay, stale attempt and UNKNOWN. |
| E | ACCEPT WITH ENUMERATED AMENDMENTS (orchestration only) | Current E Blob adopts D registration and complete dependencies; §11 corrects the earlier §10 order. Treat §11 as controlling and remove the stale D-before-Storage wording from §10 in the next E cleanup to prevent implementer ambiguity. Distinguish same-operation recovery replay from a new publication attempt after NO_PUBLICATION. |
| I | ACCEPT WITH ENUMERATED AMENDMENTS (authorization semantics only) | Current I Blob correctly requires exact Storage participant before single-use sequencer consumption and holds revocation after COMMIT_WON. It still leaves token serialization, key-status/rotation/revocation, nonce retention, audience, anti-replay/anti-rollback and proof validity at Storage commit as open I/H decisions. The candidate receipt fields above must remain a proposed mapping until I signs them. |
| Storage | ACCEPT WITH ENUMERATED AMENDMENTS (logical transaction model only) | Current Storage Blob has illustrative records and clear atomicity/race obligations but does not choose or prove the physical serialization domain. Storage must specify how its final commit atomically validates the exact D participant/current fence and I proof, and how NO_PUBLICATION proves no delayed publisher can later install a pointer. |

Cross-cutting: all four current Blobs are semantically compatible with the Storage-first sequence. No exact callable API or wire schema is yet frozen. The D/E/Storage physical authority boundary, I sequencer-to-Storage proof semantics, H canonicalization/signatures and deterministic test evidence remain blockers.

## 7. Deterministic conformance matrix (required, not yet run)

| Test | Forced ordering/fault | Required result |
|---|---|---|
| Registration vs fence | register commits first | work included in immutable fence high-water |
| Registration vs fence | fence commits first | later work rejected/quarantined; no execution |
| EventRef ingress | complete approved identity/Scope/lineage | D registered and barrier-counted; no protected dereference grant |
| EventRef ingress | missing lineage/auth/Scope | no execution capability |
| Dependency completeness | crash between edge writes | no complete receipt; cannot publish |
| Storage prepare crash | crash before D admission | orphan private Storage participant; no visibility |
| D admission | missing/non-durable Storage participant | D admission rejected |
| D admission ACK loss | response lost after commit | same operation resolves same D participant |
| I revocation race | revocation first | REVOCATION_WON; no visibility |
| I receipt race | COMMIT_WON first | revocation held until Storage terminal |
| Visibility ACK loss | commit may have happened | UNKNOWN/private until same operation resolves |
| Stale worker | old lease publishes | STALE_ATTEMPT; no visibility |
| Storage ledger gap | D admission confirmed, Storage row absent | UNKNOWN/ledger inconsistency; both gates held |
| Restore | D/I/Storage proofs disagree | quarantine; no serving |
| NO_PUBLICATION | terminal proof exists | D and I independently close exact participant |
| Outbox/replay | duplicate delivery or delayed worker | no second visibility transition |

Each test must assert durable records, visibility pointer state, D barrier state, I revocation state and retry identity—not merely HTTP status.

## 8. Physical topology decision remains OPEN

A recommends a single serializable transaction domain per Canonical Memory authority only as a candidate. D and Storage must identify the actual deployment boundary and prove that RegisterProducerWork, InstallForgetFence/high-water, complete dependency registration and final visibility transition share the required ordering. If physically split, a D/Storage-approved durable prepare/commit or linearizable coordinator protocol must demonstrate equivalent crash/failover/restore behavior. No database product is selected by this addendum.

I's PolicyDomain sequencer remains independent. No cross-domain scalar epoch comparison is permitted. The Storage visibility commit must validate the exact consumed CommitAuthorizationReceipt / ICommitAuthorizationProof whose COMMIT_WON semantics remain valid through the commit linearization point. ITerminalProof is post-Storage-outcome closeout evidence and MUST NOT be a precondition to that same commit; a detached stale ALLOW snapshot is insufficient.

## 9. Owner-exact review checklist

- **D:** accept/reject exact PublicationParticipant fields, fence admission linearization, Storage participant precondition, terminalization proof, operation/error/idempotency semantics.
- **E:** accept/reject orchestration order, stable work/run/attempt/lease identities, complete dependency set, retry and recovery mappings.
- **I:** accept/reject receipt schema, sequencer semantics, issuer/key status, audience/scope, nonce/replay, anti-rollback and COMMIT_WON/revocation hold.
- **Storage:** accept/reject durable prepare record, final transaction proof, NO_PUBLICATION proof, physical topology and restore behavior.
- **H:** define canonical wire encoding, signature suite, key discovery/rotation/revocation, canonicalization, version negotiation, replay/downgrade and interoperability vectors.
- **A:** reconcile only after each owner disposition is explicit and pinned to the exact reviewed Blob.

A role simulation by one integration session is not an independent Owner signature. Every owner must record ACCEPT, ACCEPT WITH ENUMERATED AMENDMENTS, REJECT or CANDIDATE / NO APPROVAL against the exact current Blob. Until then this artifact is a candidate contract surface only.

## 10. Explicit non-claims

No schema/wire freeze, API existence, database selection/deployment, independent Owner approval, implementation, conformance PASS, branch merge, provider execution, production activation, Global Forget completion or physical-erasure claim is made.

## 11. 中文规范

### 11.1 精确基线

本补充文件重新读取 D/E/I/Storage 四个 Owner 分支。D 当前 Blob 为 `4c01713bc8793a8926ef18b625b72d132572173d`，E 为 `4fb9e58511941f59b4d777336f8f85ad88ecccf1`，I 为 `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`，Storage 为 `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`。此前 D `206ead...`、E `bad04d...`、Storage `1ad895...` 均被替代；I 未变化。旧 A 报告保留为历史证据，本文件负责当前 Pin 修正。

### 11.2 保留的语义裁决

仅含 EventRef 的 ProducerWork 在认证 Producer、启用 ProducerClass/Version、精确 Scope、规范请求摘要及 D 批准的 opaque Lineage Token/Digest 完整时，允许 D 提前注册并纳入 ForgetFence High-water；但不授予受保护 Payload 读取权限。E 必须在 Dependency Registration/Publish 前补齐 Canonical MemoryRef/MemoryVersionRef 及 Revision。D RegistrationReceipt 必须早于 Queue/Lease/Protected Dereference/Execution/Retry/Replay/Publication。Dependency Set 必须完整集合原子登记。UNKNOWN 永远保持 Private 和 Barrier-open。

### 11.3 发布顺序

强制顺序：Storage 先持久化隐藏 StorageVisibilityParticipantRef；D 再准入绑定该 Participant 的 PublicationParticipantRef；I 在自己的 PolicyDomain Sequencer 单次消费绑定两个精确 Participant 和不可变 Tuple 的 CommitAuthorizationReceipt；Storage 最终提交同时验证 D 当前 Participant/Fence 与 I CommitAuthorizationReceipt/COMMIT_WON Sequencer Proof（不是 Storage Outcome 后才签发的 ITerminalProof）；D/I 分别验证同一权威 Storage Outcome 后才关闭 Participant。COMMITTED_VISIBLE 或有权威证据的 NO_PUBLICATION 才能终态化。UNKNOWN/IN_DOUBT 不得释放 Gate。

### 11.4 类型与摘要隔离

PublicationOperationId、ProducerWorkItemId、DerivationRunId、AttemptId、LeaseId、D PublicationParticipantRef、I CommitAuthorizationReceipt、StorageVisibilityParticipantRef、C ParticipantIntentRef、Storage PreparedParticipantRef/GID/XID 均为不同名义类型。D RegistrationSequence/FenceGeneration/CanonicalCommitCursor、I PermissionEpoch、Storage Transaction/XID/Visibility Pointer 不得合并或跨域比较。所有参与者绑定相同不可变 Publication Tuple Digest；同身份同摘要幂等，同身份不同摘要冲突。

### 11.5 精确合同仍待 Owner 决定

本文件的字段集合和操作表只是候选逻辑合同，不是冻结 Schema。D 必须决定 Fence/Admission/Terminal 语义；E 决定 Orchestration/Retry/Recovery；I 决定 Receipt、Sequencer、Key Status、Audience、Replay 和 Anti-rollback；Storage 决定 Prepare/Commit/NO_PUBLICATION 与实际事务拓扑；H 决定 Wire Canonicalization/Signature/Interop。单一集成会话模拟角色不等于独立 Owner 签署。

### 11.6 符合性验证

必须执行注册与 Fence 竞态、EventRef Admission、Dependency Completeness、Storage Prepare Crash、D Admission ACK Loss、I Revocation Race、Visibility ACK Loss、Stale Lease、Ledger Gap、Restore Disagreement、NO_PUBLICATION 与 Outbox Replay 测试。每项必须检查持久化记录、Visibility Pointer、D Barrier、I Revocation State 和 Retry Identity，不能只检查 HTTP 状态。

### 11.7 未授权事项

不宣称 Schema/Wire Freeze、API 已存在、数据库已选型或部署、独立 Owner 批准、实现完成、Conformance PASS、分支合并、Provider Execution、Production Activation、Global Forget Completion 或物理擦除完成。


## 12. Owner-role contract artifacts created in their respective branches

These are role-authored candidate contract artifacts created during this integration session. They are not independent signatures by the named repository Owners.

| Role | Branch | Path | Exact Blob SHA | Disposition |
|---|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` | Candidate D participant/admission/terminal contract |
| E | `session-e-memory-compiler-2026-11-16` | `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md` | `475fee41e5eea527af4edefbfe88c58c86967d0a` | Candidate orchestration/retry/recovery contract |
| I | `session-i-security-governance-2026-11-16` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | `54bab0484bd232a5a258e65e34cc7425288b39a6` | Candidate authorization receipt/sequencer contract |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `175ee7b1349cfdb79a19898b311a88391ed88010` | Candidate durable prepare/visibility outcome contract |

### 12.1 Integration cross-check

- D requires durable Storage PREPARED_HIDDEN before admitting its PublicationParticipantRef.
- E orchestrates the full Storage → D → I → Storage sequence and distinguishes same-operation recovery replay from a new publication after NO_PUBLICATION.
- I separates caller request, single-use sequencer consumption receipt and terminal proof; COMMIT_WON holds revocation but never grants standalone visibility.
- Storage owns the durable participant, final visibility linearization, immutable outcome and positive NO_PUBLICATION proof; physical topology remains open.

The four artifacts are mutually consistent at the logical contract level. Their exact APIs, canonical wire schemas, cryptographic profiles, physical serialization topology and conformance evidence remain open. A final owner-exact review must be performed by each actual Owner against these exact Blob SHAs.

## 13. Circular-proof dependency correction

The final pre-commit proof set is:
- D current PublicationParticipantRef + current D fence proof;
- Storage durable PREPARED_HIDDEN StorageVisibilityParticipantRef;
- I consumed CommitAuthorizationReceipt, which is the pre-commit `ICommitAuthorizationProof` and proves COMMIT_WON in the I PolicyDomain sequencer.

Storage validates this ICommitAuthorizationProof at the visibility linearization point. Only after Storage emits COMMITTED_VISIBLE or authoritative NO_PUBLICATION may I issue `ITerminalProof` to close its in-flight authorization participant and release held revocation as appropriate.

`ITerminalProof` MUST NOT be required by the Storage commit that creates the outcome it attests. That would be a circular dependency. The consumed CommitAuthorizationReceipt and post-commit ITerminalProof are distinct proof stages and MUST remain distinct in every API and wire schema.

### 中文规范

最终提交前证明集合为：D 当前 PublicationParticipantRef 与当前 D Fence Proof；Storage 已持久化的 PREPARED_HIDDEN StorageVisibilityParticipantRef；以及 I 已消费的 CommitAuthorizationReceipt（即提交前 ICommitAuthorizationProof），证明该精确发布在 I PolicyDomain Sequencer 中取得 COMMIT_WON。

Storage 在 Visibility Linearization Point 验证 ICommitAuthorizationProof。只有 Storage 产生 COMMITTED_VISIBLE 或权威 NO_PUBLICATION 后，I 才能签发 ITerminalProof，用于关闭自己的进行中 Authorization Participant，并按规则释放等待中的 Revocation。

Storage 不得要求 ITerminalProof 来执行产生该证明所依赖 Storage Outcome 的提交，否则形成循环依赖。已消费 CommitAuthorizationReceipt 与提交后 ITerminalProof 是两个不同证明阶段，所有 API/Wire Schema 必须保持类型隔离。


## 14. Current Phase 3.8 Owner-source refresh and bounded publication-model evidence (2026-11-18)

### 14.1 Exact current Owner branch pins

The following branch tips and Phase 3.8 contract artifacts were fetched again after PR #151/#153 integration. The branch tips are the observed source snapshot for this refresh; the Blob SHAs identify the exact files read.

| Owner | Branch | Observed branch HEAD | Phase 3.8 contract Blob |
|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `0ddfbb0b7582c4600c9c92007414dd933d5d2bac` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | `475fee41e5eea527af4edefbfe88c58c86967d0a` |
| I | `session-i-security-governance-2026-11-16` | `8758fc8caf6412ce8a7c6d5178fb70d43569ac76` | `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `f6887cc9ea5bfa5293c1bc47e9f10e582830cba3` | `175ee7b1349cfdb79a19898b311a88391ed88010` |
| A | `session-a-integration-2026-11-16` | `6e05831d264040e0e3b3359245b1e01ea613b46c` | this addendum, prior to §14 refresh |

All four Owner contracts still explicitly leave independent Owner approval, exact wire/canonicalization, cryptographic/key lifecycle, physical serialization topology and conformance open. The observed branch heads are not Owner approvals. The role-authored artifacts were read from their named branches and must not be treated as independently signed decisions.

### 14.2 Mainline reference-model changes since the prior integration review

Two bounded reference-model PRs are now merged:

1. PR #151, exact Head `31a48f53b85929482ec1ef39a9ad2b254c64af00`, merge `d38c8379392e56fa095ad7577e96c46b8ff202f3`. Exact-head publication workflow #44189403281 completed SUCCESS with 18 tests.
2. PR #153, exact Head `faf90302fb519c6f3e86946fe854b12639cc1423`, merge `be90d5c5d04dab65123f53a153cadd562242daa1`. Exact-head publication workflow #44189766480 completed SUCCESS with 20 tests.

The model now exercises these bounded rules:

- Fence-first: after D installs ForgetFence, a previously registered ProducerWork and hidden Storage participant cannot obtain a new PublicationParticipant.
- Publication-first: a PublicationParticipant admitted before the fence remains in the modeled fence barrier until D closes it against the exact modeled Storage outcome.
- Later fence: a publication already D-closed before a later fence is not reintroduced into the pending barrier.
- Idempotent replay: an existing operation ID returns its receipt only for the same immutable tuple of auth ID, publication participant, Storage participant, D admission proof and I COMMIT_WON proof. A changed tuple conflicts.

These are deterministic, in-memory reference-model tests. They do not establish database serializability, real multi-process concurrency, distributed transaction atomicity, proof authenticity, actual D/I/Storage adapters, crash/failover/restore behavior or production conformance. The test double's methods represent durable transitions; they are not themselves durable transactions.

### 14.3 Updated integration disposition

The Phase 3.8 composition remains **COHERENT PROPOSED CONTRACT / NOT FROZEN**.

The two PRs reduce ambiguity in the reference model but do not close any Owner authority gate. The following remain OPEN:

- independent exact-version D/E/I/Storage Owner decisions on the Phase 3.8 source Blobs above;
- H wire schema, canonical encoding, signature and cross-language interoperability;
- I trust-root/key lifecycle, revocation propagation, nonce consumption and authoritative PolicyDomain sequencer proof;
- Storage's selected physical serialization/transaction topology and actual final visibility linearization proof;
- D/Storage crash, lost-ACK, concurrent race, failover, restore and anti-rollback conformance;
- end-to-end COC/participant registry and real owner-ledger integration;
- explicit production engineering entry, which remains deferred by project authority to the engineering phase.

No architecture freeze, Owner approval, production implementation, Forget completion, deployment or production activation is claimed.

### 14.4 中文规范

#### 14.4.1 当前 Phase 3.8 Owner 分支精确版本

本次在 PR #151/#153 集成后重新读取了以下 Owner 分支及 Phase 3.8 契约文件。分支 Head 是本次观察到的源快照；Blob SHA 标识实际读取的文件。

| Owner | 分支 | 观察到的分支 HEAD | Phase 3.8 契约 Blob |
|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `0ddfbb0b7582c4600c9c92007414dd933d5d2bac` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | `475fee41e5eea527af4edefbfe88c58c86967d0a` |
| I | `session-i-security-governance-2026-11-16` | `8758fc8caf6412ce8a7c6d5178fb70d43569ac76` | `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `f6887cc9ea5bfa5293c1bc47e9f10e582830cba3` | `175ee7b1349cfdb79a19898b311a88391ed88010` |
| A | `session-a-integration-2026-11-16` | `6e05831d264040e0e3b3359245b1e01ea613b46c` | 本文件 §14 更新前版本 |

四个 Owner 契约仍明确保留独立 Owner 批准、精确 Wire/规范化、密码学/密钥生命周期、物理序列化拓扑及符合性验证等 OPEN 项。观察到的分支 Head 不等于 Owner 批准。角色会话撰写的文件不能冒充独立签署的决策。

#### 14.4.2 自上次集成审查以来的主线参考模型变化

两个有界参考模型 PR 已合并：

1. PR #151，精确 Head `31a48f53b85929482ec1ef39a9ad2b254c64af00`，合并提交 `d38c8379392e56fa095ad7577e96c46b8ff202f3`。精确 Head 的 Publication 工作流 #44189403281 SUCCESS，共 18 项测试。
2. PR #153，精确 Head `faf90302fb519c6f3e86946fe854b12639cc1423`，合并提交 `be90d5c5d04dab65123f53a153cadd562242daa1`。精确 Head 的 Publication 工作流 #44189766480 SUCCESS，共 20 项测试。

当前模型覆盖：

- Fence-first：D 安装 ForgetFence 后，即使 ProducerWork 和隐藏 Storage participant 之前已注册，也不能再取得新的 PublicationParticipant。
- Publication-first：Fence 前已准入的 PublicationParticipant 必须持续保留在模型中的 Forget barrier，直到 D 根据精确的模型 Storage 终态完成关闭。
- 后续 Fence：在后续 Fence 安装前已由 D 关闭的 publication，不会重新进入待处理 barrier。
- 幂等重放：已有 operation ID 只有在 auth ID、publication participant、Storage participant、D 准入证明和 I COMMIT_WON 证明组成的不可变元组完全一致时才返回原 receipt。任何元组变化都冲突。

以上仅为确定性的内存参考模型测试，不能证明数据库可串行化、真实多进程并发、分布式事务原子性、证明真实性、真实 D/I/Storage 适配器、崩溃/故障切换/恢复行为或生产符合性。模型方法只是模拟持久化转换，并不是真正的持久事务。

#### 14.4.3 更新后的集成裁决

Phase 3.8 组合仍为 **契约层面一致的提案 / 未冻结**。

两个 PR 降低了参考模型中的语义歧义，但没有关闭任何 Owner 权威门禁。以下事项仍 OPEN：

- D/E/I/Storage 对上述 Phase 3.8 精确 Blob 的独立 Owner 决策；
- H Wire Schema、规范编码、签名及跨语言互操作；
- I 信任根/密钥生命周期、撤权传播、Nonce 消费及权威 PolicyDomain Sequencer 证明；
- Storage 已选定的物理序列化/事务拓扑及真实最终可见性线性化证明；
- D/Storage 崩溃、ACK 丢失、并发竞态、故障切换、恢复及防回滚符合性；
- 端到端 COC/Participant Registry 与真实 Owner Ledger 集成；
- 生产工程实施入口；项目负责人仍明确将其延期至工程阶段。

本次不宣称架构冻结、Owner 批准、生产实现、Forget 完成、部署或生产激活。


## 15. UNKNOWN outcome replay hardening — PR #159 (2026-11-18)

PR #159 was merged to main at `05fe0f9551ef3149d1c54b6f3a5e2f0ba6672551`.

- Exact PR Head: `3c75b246cbaa2053460408b949a7b83a032a5fd8`.
- Exact-head publication reference-model workflow [#44191060992](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44191060992): SUCCESS; job log reports 21 tests / OK.
- Exact-head GOV-DOC-001 structural check #44191060993: SUCCESS.
- Main readback: reference-model source Blob `321fc511aa3f1b5cc8bfcac47664c432bee89c50`, 21 test methods.

### 15.1 Bounded behavior

The model now rejects a commit attempt when the same `operation_id` is already in `private_unknown`. The regression test asserts that a retry cannot create visibility, outcome, receipt or outbox state, and cannot consume authorization while the authoritative Storage outcome remains unknown.

This closes the modeled fail-open path where an UNKNOWN operation could otherwise be recommitted as though it were a fresh attempt and clear its private-unknown marker without reconciliation.

### 15.2 Remaining evidence limit

This is still an in-memory model. It does not implement or prove the authoritative Storage reconciliation protocol, durable operation-intent binding across process restart, database uniqueness, multi-process races, cryptographic proof authenticity, cross-owner participant ledgers or production crash/failover/restore. The model still has no executable positive `NO_PUBLICATION` proof path; D/I closeout is exercised only for the modeled COMMITTED outcome, while UNKNOWN is proven non-terminal. That missing positive no-publication path remains an explicit coverage gap, not an inferred PASS.

### 15.3 Updated disposition

The publication reference-model sequence now has bounded tests for fence-first rejection, publication-first barrier retention, exclusion of D-closed participants from later fences, exact immutable operation replay binding and UNKNOWN non-recommit. The Phase 3.8 architecture remains **COHERENT PROPOSED CONTRACT / NOT FROZEN**. Independent D/E/I/Storage decisions, H wire/crypto, physical topology, positive NO_PUBLICATION proof, real Storage reconciliation, crash/failover/restore and production conformance remain OPEN.

### 中文规范

PR #159 已合并至 main，合并提交为 `05fe0f9551ef3149d1c54b6f3a5e2f0ba6672551`。

- 精确 PR Head：`3c75b246cbaa2053460408b949a7b83a032a5fd8`。
- 精确 Head 的 Publication 参考模型工作流 #44191060992 SUCCESS；Job 日志报告 21 项测试通过。
- 精确 Head 的 GOV-DOC-001 检查 #44191060993 SUCCESS。
- 主线回读的参考模型源码 Blob：`321fc511aa3f1b5cc8bfcac47664c432bee89c50`，共 21 个测试方法。

#### 15.1 有界行为

当同一 `operation_id` 已处于 `private_unknown` 时，模型现在拒绝再次提交。回归测试确认：在 Storage 权威终态仍未知时，重试不能创建可见性、终态、Receipt 或 Outbox，也不能消费授权。

这关闭了模型中 UNKNOWN 操作被当作新尝试重新提交、并在未完成权威对账前清除 private-unknown 标记的失效开放路径。

#### 15.2 仍然存在的证据边界

这仍是内存模型，并未实现或证明权威 Storage 对账协议、跨进程重启的持久操作意图绑定、数据库唯一性、多进程竞态、密码学证明真实性、跨 Owner Participant Ledger 或生产崩溃/故障切换/恢复。模型仍没有可执行的正向 `NO_PUBLICATION` 证明路径；D/I 关闭目前只对模型 COMMITTED 终态进行测试，UNKNOWN 则被证明不能终态化。该正向 NO_PUBLICATION 路径缺失是明确的测试覆盖缺口，不能推断为 PASS。

#### 15.3 更新后的裁决

当前发布参考模型已覆盖 Fence-first 拒绝、Publication-first Barrier 保留、后续 Fence 排除已由 D 关闭的 Participant、精确不可变操作元组重放，以及 UNKNOWN 禁止重新提交。Phase 3.8 架构仍为 **契约层面一致的提案 / 未冻结**。独立 D/E/I/Storage 决策、H Wire/密码学、物理拓扑、正向 NO_PUBLICATION 证明、真实 Storage 对账、崩溃/故障切换/恢复及生产符合性仍 OPEN。


## 16. I sequencer / Storage terminal separation — PR #168 (2026-11-18)

PR #168 merged to main at `2fabe07640e2f3cee69b213275c9f5a7b17edd5d`.

- Exact PR Head: `206909f5af9834b993cfc198b2f171c54bc7cd3f`.
- Exact-head Publication Protocol workflow [#44194106522](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44194106522): SUCCESS, 28 tests / OK.
- Exact-head GOV-DOC-001 structural check #44194106534: SUCCESS.
- Main readback source Blob: `3417e0d5a6ec21ff36fa1bba7c9994352bc70849`; 28 test methods.

### 16.1 Corrected authority boundary

The earlier PR #163/#164 NO_PUBLICATION path was too compressed: it treated I authorization consumption as part of Storage commit and rejected a consumed authorization as inconsistent with NO_PUBLICATION. That contradicted the Phase 3.8 Owner sequence.

PR #168 now models two separate authority transitions:

1. I sequencer `COMMIT_WON`: consumes the single-use authorization, persists the exact immutable operation tuple and creates a pending I participant.
2. Storage final transaction: validates the exact I proof and D participant, then writes visibility, Storage outcome, receipt and outbox. It does not consume I authorization.

Consequences now exercised:

- Revocation before I COMMIT_WON rejects.
- Revocation after COMMIT_WON remains pending and cannot cancel the winner; the exact I proof is replayable, and I closeout releases the pending revocation only after the exact Storage outcome.
- A known crash before Storage commit leaves I authorization consumed and I participant pending, but creates no Storage visibility, outcome, receipt or outbox. The same immutable operation can retry.
- UNKNOWN blocks recommit until authoritative Storage reconciliation.
- Positive NO_PUBLICATION preserves consumed I authorization and the pending I participant; it creates no visibility/receipt/outbox. D and I close only against the same exact Storage terminal outcome, with D's active ForgetFence participant barrier retained until D closeout.

### 16.2 Historical correction and evidence ceiling

Section 15's statement that the model lacked a positive NO_PUBLICATION path is superseded by PR #163/#164; this section further corrects the I/Storage sequencing mismatch found during review of those merged changes. The typed `StorageNoPublicationProof` remains only an in-memory test seam. Its booleans are not authenticated Storage evidence, a wire schema, a signature or Owner acceptance.

The current model still does not prove real I sequencer durability, Storage transaction durability, DB serializability, multi-process concurrency, cross-service atomicity, proof authenticity, process restart, failover, restore or anti-rollback. No production implementation or conformance is claimed.

The Phase 3.8 disposition remains **COHERENT PROPOSED CONTRACT / NOT FROZEN**. Independent D/E/I/Storage Owner decisions, H wire/crypto, physical topology and production conformance remain OPEN.

### 中文规范

PR #168 已合并至 main，合并提交为 `2fabe07640e2f3cee69b213275c9f5a7b17edd5d`。

- 精确 PR Head：`206909f5af9834b993cfc198b2f171c54bc7cd3f`。
- 精确 Head 的 Publication Protocol 工作流 #44194106522 SUCCESS，共 28 项测试。
- 精确 Head 的 GOV-DOC-001 检查 #44194106534 SUCCESS。
- 主线回读源码 Blob：`3417e0d5a6ec21ff36fa1bba7c9994352bc70849`，共 28 个测试方法。

#### 16.1 修正后的权威边界

此前 PR #163/#164 的 NO_PUBLICATION 路径过度压缩了状态机：它把 I 授权消费视为 Storage 提交的一部分，并将已消费授权视为与 NO_PUBLICATION 冲突。这与 Phase 3.8 Owner 规定的先后顺序矛盾。

PR #168 现在分别建模两个权威转换：

1. I Sequencer `COMMIT_WON`：消费单次授权，持久化精确不可变操作元组，并创建待关闭的 I Participant。
2. Storage 最终事务：验证精确 I 证明和 D Participant，然后写入可见性、Storage 终态、Receipt 和 Outbox；它不负责消费 I 授权。

现在测试覆盖：

- I COMMIT_WON 之前发生撤权，准入失败。
- COMMIT_WON 之后发生撤权，撤权保持待处理，不能取消已经胜出的决策；精确 I 证明可以重放，只有 I 在精确 Storage 终态后关闭时才释放待处理撤权。
- Storage 提交前已知崩溃会保留已消费的 I 授权和待关闭的 I Participant，但不会创建 Storage 可见性、终态、Receipt 或 Outbox；相同不可变操作可以重试。
- UNKNOWN 在权威 Storage 对账前禁止重新提交。
- 正向 NO_PUBLICATION 保留已消费的 I 授权和待关闭 I Participant，不创建可见性/Receipt/Outbox。D/I 只能针对同一个精确 Storage 终态关闭；D 的 ForgetFence Participant Barrier 必须一直保留到 D 关闭。

#### 16.2 历史纠正与证据边界

§15 关于模型缺少正向 NO_PUBLICATION 路径的陈述已被 PR #163/#164 的合并所 supersede；本节进一步纠正了审查这些合并变更时发现的 I/Storage 先后顺序问题。类型化 `StorageNoPublicationProof` 仍然只是内存测试夹具，其布尔值不是经过认证的 Storage 证据、Wire Schema、签名或 Owner 批准。

当前模型仍不能证明真实 I Sequencer 持久性、Storage 事务持久性、数据库可串行化、多进程并发、跨服务原子性、证明真实性、进程重启、故障切换、恢复或防回滚。不宣称生产实现或生产符合性。

Phase 3.8 裁决仍为 **契约层面一致的提案 / 未冻结**。独立 D/E/I/Storage Owner 决策、H Wire/密码学、物理拓扑及生产符合性仍 OPEN。
