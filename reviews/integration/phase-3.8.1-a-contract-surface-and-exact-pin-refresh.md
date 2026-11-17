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
5. The final visibility boundary is conjunctive: current D publication participant/fence AND I terminal authorization proof AND exact Storage participant/outcome. No detached reusable token authorizes a later write.
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

The logical receipt is the signed, single-use sequencer result. If the implementation separates an authorization request/token from the consumption result, those MUST be distinct nominal types; do not put a caller-supplied decision into a signed bearer token. I consumes the authorization exactly once in its PolicyDomain sequencer. Revocation-first yields REVOCATION_WON. COMMIT_WON creates an unresolved I participant and holds subsequent applicable revocation until the same Storage terminal outcome. UNKNOWN holds. `accept_before` constrains first consumption only; it cannot expire or release an already-consumed COMMIT_WON participant. A consumed receipt is not a bearer token for an independent Storage write.

`ITerminalProof` binds the receipt, both participant refs, tuple digest and exact Storage outcome proof. I closes only after validating COMMITTED_VISIBLE or authoritative NO_PUBLICATION. Issuer/key status, policy version, audience, replay and anti-rollback rules remain I/H owner decisions and are not silently decided here.

### 3.5 Storage final outcome

`StorageVisibilityOutcome`:
- `publication_operation_id`, `publication_tuple_digest`
- exact `storage_visibility_participant_ref`, `publication_participant_ref`, `authorization_receipt_ref`
- `outcome`: COMMITTED_VISIBLE | NO_PUBLICATION | UNKNOWN
- `visibility_transaction_ref`, `visibility_pointer_ref` (required only for COMMITTED_VISIBLE)
- exact D current-participant/fence proof reference
- exact I terminal authorization proof reference
- `outbox_event_ref`, `committed_at`, `outcome_digest`

The visibility linearization point is the durable transaction that validates the exact D and I proofs and changes the authoritative visibility pointer/outcome atomically. NO_PUBLICATION requires positive authoritative proof that no visibility pointer was installed and no delayed publisher/outbox/retry can later install it. UNKNOWN has no terminal semantics and leaves the artifact private.

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

I's PolicyDomain sequencer remains independent. No cross-domain scalar epoch comparison is permitted. The Storage visibility commit must validate an exact I proof whose semantics remain valid through the commit linearization point; a detached stale ALLOW snapshot is insufficient.

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

强制顺序：Storage 先持久化隐藏 StorageVisibilityParticipantRef；D 再准入绑定该 Participant 的 PublicationParticipantRef；I 在自己的 PolicyDomain Sequencer 单次消费绑定两个精确 Participant 和不可变 Tuple 的 CommitAuthorizationReceipt；Storage 最终提交同时验证 D 当前 Participant/Fence 与 I Terminal Proof；D/I 分别验证同一权威 Storage Outcome 后才关闭 Participant。COMMITTED_VISIBLE 或有权威证据的 NO_PUBLICATION 才能终态化。UNKNOWN/IN_DOUBT 不得释放 Gate。

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
| E | `session-e-memory-compiler-2026-11-16` | `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md` | `cee88de8614b1739aa6a575ac88cb907463a0312` | Candidate orchestration/retry/recovery contract |
| I | `session-i-security-governance-2026-11-16` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | `b0b6997bf518e03e924faee8cdba367807dfeda6` | Candidate authorization receipt/sequencer contract |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `73c6d3d86a51a7163a727994aef247ba97fde083` | Candidate durable prepare/visibility outcome contract |

### 12.1 Integration cross-check

- D requires durable Storage PREPARED_HIDDEN before admitting its PublicationParticipantRef.
- E orchestrates the full Storage → D → I → Storage sequence and distinguishes same-operation recovery replay from a new publication after NO_PUBLICATION.
- I separates caller request, single-use sequencer consumption receipt and terminal proof; COMMIT_WON holds revocation but never grants standalone visibility.
- Storage owns the durable participant, final visibility linearization, immutable outcome and positive NO_PUBLICATION proof; physical topology remains open.

The four artifacts are mutually consistent at the logical contract level. Their exact APIs, canonical wire schemas, cryptographic profiles, physical serialization topology and conformance evidence remain open. A final owner-exact review must be performed by each actual Owner against these exact Blob SHAs.