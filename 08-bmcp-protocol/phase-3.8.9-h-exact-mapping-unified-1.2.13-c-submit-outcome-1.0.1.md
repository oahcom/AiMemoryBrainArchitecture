# Phase 3.8.9 — H Exact Mapping: Unified 1.2.13 × CSubmitOutcome 1.0.1
# Phase 3.8.9 — H Unified 1.2.13 × CSubmitOutcome 1.0.1 精确映射

- Owner perspective: H — BMCP Protocol / Schema and Interoperability
- Status: **CURRENT SUCCESSOR MAPPING CANDIDATE / VALIDATOR SOURCE UPDATED / EXACT CI RE-RUN REQUIRED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H Unified schema 1.2.13 / wire 1.3.0: Blob `8e7f6a6c9663388863db88548f9c37d0fdb1bd97`
- CSubmitOutcome schema 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C Phase 3.11.1 sequence namespace amendment: Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`
- I Phase 3.8.8 sequence namespace review: Blob `0d78e5b2bfcf66cae6b757314cead84b9c942601`
- C key-status event schema 1.0.0: Blob `908b293eba337e9fa75864cea3704e28a1a8d82e`
- H validator core: Blob `241657140375c93acd90d107724b54c612d99597`
- H validator tests: Blob `418f0a78ea363286f143ae414af4b92e9a3e89bf`
- C review of H 1.2.13 × C 1.0.1: Blob `761f204ac0ad3a433c336d71217e7c3147ebc09e`
- H predecessor mapping 1.2.12 × C 1.0.1: Blob `fad28f1b62f6a686669e209ebe30d69df6330d75`
- H predecessor mapping 1.2.13 × C 1.0.0: Blob `6b86fa62c248f2092815fe552e39eb5896f48630`
- Provenance: delegated H-role update in the coordinating session; **not an independent human H Owner signature**.

## 1. Exact currentness and supersession / 精确当前性与替代关系

For new C Provider Outcome records, the current candidate pair is:
- H Unified schema artifact revision `1.2.13`, wire family `1.3.0`;
- CSubmitOutcome schema/artifact revision `1.0.1`.

The H 1.2.12 / C 1.0.1 mapping and H 1.2.13 / C 1.0.0 mapping are predecessor candidates only. No silent schema upgrade is permitted. The validator MUST reject a wrong H artifact revision or wrong C object schema ID/version/revision.

新 C Provider Outcome 记录的当前候选版本对为 H Unified 1.2.13（Wire 1.3.0）与 CSubmitOutcome 1.0.1。H 1.2.12 × C 1.0.1 及 H 1.2.13 × C 1.0.0 均为前序候选，不得静默升级。Validator 必须拒绝错误的 H Artifact Revision 或 C Object Schema ID/Version/Revision。

## 2. Exact duplicated field mapping / 重复字段精确映射

| H 1.2.13 field | CSubmitOutcome 1.0.1 field | Rule |
|---|---|---|
| `c_submit_outcome_ref` | `record_ref` | Exact immutable object identity |
| `c_submit_outcome_digest` | `payload_digest` | Exact C-P0 digest equality and recomputation under registered C profile |
| `provider_outcome` | `Outcome` | Exact enum equality |
| `provider_ref` | `ProviderRef` | Exact typed identity |
| `provider_adapter_ref` | `AdapterRef` | Exact typed identity |
| `provider_idempotency_key_ref` | `IdempotencyKeyRef` | Exact key; namespace remains C-object-only |
| `provider_request_ref` | `ProviderRequestRef` | Exact when applicable |
| `provider_receipt_ref` | `ProviderReceiptRef` | Exact when applicable |
| `provider_lookup_proof_ref` | `ProviderLookupProofRef` | Exact when applicable |
| `provider_no_handoff_proof_ref` | `ProviderNoHandoffProofRef` | Exact when present/required by C SideEffectStatus |
| `not_invoked_proof_ref` | `NotInvokedProofRef` | Exact when applicable |
| `unknown_reason_ref` | `UnknownReasonRef` | Exact for UNKNOWN / IN_DOUBT |
| `actual_inference_request_id` | `ActualInferenceRequestId` | Exact when present in C object |
| `final_request_boundary_id` | `FinalRequestBoundaryRef` | Exact boundary identity |
| `request_digest` | `RequestDigest` | Exact digest |
| `transaction_ref` | `CausalOrderTransactionRef` | Exact typed transaction |
| `provider_outcome_evidence_ref` | `OutcomeEvidenceRef` | Exact evidence ref; separately verify C OutcomeEvidenceDigest |
| `owner_signature_ref` | `OwnerSignatureRef` | Exact C signature evidence ref |
| `owner_admission_ref/digest` | `CAdmissionRef/CAdmissionDigest` | Exact C owner admission identity/digest |
| `owner_ledger_ref/version` | `COwnerLedgerRef/COwnerLedgerVersion` | C owner ledger, not Storage participant ledger |
| `owner_local_sequence` | `COwnerLocalSequence` | Exact C-local sequence |
| `owner_high_water` | `COwnerHighWater` | Exact C high-water |
| `owner_ledger_root` | `COwnerLedgerRoot` | Exact C ledger root |
| `coc_participant_intent_ref` | `COCParticipantIntentRef` | Exact nullable COC intent |
| `participant_reservation_ref` | `COCParticipantReservationRef` | Exact reservation when applicable |
| `coc_absence_reason` | `COCAbsenceReason` | Exact when COC intent/reservation are null |

The H 1.2.13 C branch does not contain `participant_intent_ref`. H MUST NOT accept the old 1.2.12 alias as an alternate source for `coc_participant_intent_ref`. Null and absent are not interchangeable.

H 1.2.13 C 分支不再包含 `participant_intent_ref`。H 不得把 1.2.12 的旧别名当作 `coc_participant_intent_ref` 的替代来源。Null 与 Absent 不可互换。

## 3. C-object-only fields and mandatory dereference / 仅存在于 C 对象的字段与强制解引用

The following values are not inline in the H C outcome branch and MUST be obtained from the immutable C object:
- `CGateRef`, `CGateGeneration`, `CGateCommitRef`, `CGateCommitDigest`;
- `ProviderAttemptRef`, `ProviderAttemptGeneration`;
- `ProviderAccountRef`, `AdapterBuildRef`, `EndpointRef`, `RegionRef`, `ApiOperation`;
- `IdempotencyNamespaceRef`, `ProviderCapabilityRecordRef`, `ProviderCapabilityDigest`;
- `FinalRequestBoundaryType`, `RequestContentType`, `RequestMethod`;
- `SideEffectStatus`, `OutcomeObservedAt`, `OutcomeEvidenceDigest`, `ProviderEvidenceIssuerRef`, `ProviderEvidenceType`;
- `sequence_namespace_ref`;
- `PriorObservationRef`, `SupersedesObservationRef`, `ReconciliationParentRef`.

The 1.0.1 `sequence_namespace_ref` MUST equal the authenticated CKeyStatusEvent sequence namespace and the namespace of the authoritative C signing sequencer. H must prove that C `record_sequence` and CKeyStatusEvent `event_sequence` are allocated in the same durable monotonic namespace. Missing/mismatched namespace is INVALID; unavailable sequencer, key-status ledger or anti-rollback checkpoint is UNKNOWN.

H `prepare_attempt_ref/generation` belongs to Storage's prepared-participant attempt, not C's ProviderAttempt. H `participant_ledger_ref/version` belongs to Storage, not C's `COwnerLedgerRef/Version`. H's `provider_idempotency_key_ref` maps only the key; C namespace remains in the object.

以下字段不在 H C Outcome 分支内联，必须从不可变 C 对象解引用：Gate/Generation/Commit、ProviderAttempt/Generation、ProviderAccount、AdapterBuild、Endpoint、Region、API、Idempotency Namespace、Capability、Final Request 类型/方法/内容类型、SideEffectStatus、Outcome 时间/摘要/Issuer/Type、Sequence Namespace 和追加观察链字段。

1.0.1 的 `sequence_namespace_ref` 必须等于认证后的 CKeyStatusEvent Namespace 以及 C 权威签名 Sequencer Namespace。H 必须证明 C `record_sequence` 与 CKeyStatusEvent `event_sequence` 由同一个持久化单调 Namespace 分配。缺失/不匹配为 INVALID；Sequencer、Key Status Ledger 或 Anti-Rollback Checkpoint 不可用为 UNKNOWN。

H Storage PrepareAttempt 不等于 C ProviderAttempt；Storage ParticipantLedger 不等于 C OwnerLedger；Provider Idempotency Key 不包含 C Namespace。

## 4. Outcome semantic predicates / Outcome 语义谓词

H structural validation is followed by C-object dereference and these semantic rules:

| C Outcome | C SideEffectStatus | H wire requirements | Semantic disposition |
|---|---|---|---|
| HANDOFF_ACCEPTED | PROVEN_OCCURRED | provider request + receipt + outcome evidence + reservation | VALID only after provider evidence and all owner joins verify |
| HANDOFF_REJECTED | PROVEN_NONE | provider request + outcome evidence; no-handoff proof must be present/equal | No-side-effect only after authoritative proof verifies |
| HANDOFF_REJECTED | POSSIBLE_OR_UNKNOWN | provider request + outcome evidence; no-handoff proof not required | Nonterminal / blocking; never safe retry-as-new |
| HANDOFF_REJECTED | PROVEN_OCCURRED | provider request + outcome evidence | Preserve occurred side effect; reconcile as occurred |
| NOT_INVOKED | PROVEN_NONE | not-invoked proof; provider receipt forbidden | Requires same durable gate serialization authority proof |
| UNKNOWN / IN_DOUBT | POSSIBLE_OR_UNKNOWN | unknown reason | Preserve original attempt/key/request tuple; no retry-as-new |

A provider rejection label does not prove no handoff. H must not infer C SideEffectStatus from the H enum. It must read and validate the C object and evidence. Missing C object member is INVALID; unavailable object/currentness/key-status/provider verifier is UNKNOWN.

Provider 拒绝标签不证明没有交接。H 不得从 H Outcome 枚举推断 C SideEffectStatus，必须读取并验证 C 对象及证据。C 对象必需字段缺失为 INVALID；对象/当前性/Key Status/Provider Verifier 不可用为 UNKNOWN。

## 5. Separate owner evidence / 独立 Owner 证据

These H fields are separate authority facts and are not C-P0:
- COC commit/record/position/entry digest;
- Storage PreparedParticipantRef, Storage PrepareAttempt, participant ledger, tuple digest and StorageResolutionProof;
- I terminal decision proof;
- D clearance proof.

C provider truth is C-owned. H cannot mint it. C cannot mint I COMMIT_WON, D clearance, Storage resolution, COC quorum commitment or G Applied. Each proof must be authenticated by its owner and bound to the exact operation/participant tuple.

## 6. Validator and CI currentness / Validator 与 CI 当前性

The H validator core now pins:
- `SCHEMA_ARTIFACT_REVISION=1.2.13`;
- `WIRE_SCHEMA_VERSION=1.3.0`;
- `C_OBJECT_SCHEMA_ID=urn:aimba:schema:c-submit-outcome:1.0.1`;
- C profile candidate `AIMBA-C-CRYPTO-1.0`.

Exact validator core Blob: `241657140375c93acd90d107724b54c612d99597`.
Exact test source Blob: `418f0a78ea363286f143ae414af4b92e9a3e89bf`.

The test source now includes 1.2.13 schema pinning, 1.0.1 C object namespace checks, removal of the legacy intent alias and the HANDOFF_REJECTED/SideEffectStatus conditional cases. **These latest tests have not yet been tied to a completed exact-head GitHub Actions run in this review.** The earlier H run 44060704553 (17 tests) tested H 1.2.12/C 1.0.1 and is not evidence for H 1.2.13.

Validator authority callbacks remain integration seams. Missing profile registration, key-status, C signature, provider evidence or owner-ledger callbacks return UNKNOWN. The C profile remains unregistered.

H Validator Core 已固定 1.2.13 / Wire 1.3.0 / C Object 1.0.1。最新测试源码覆盖 1.2.13 Schema、1.0.1 Namespace、旧 Intent Alias 删除及 HANDOFF_REJECTED/SideEffectStatus 条件；但本审查尚未将最新测试绑定到已完成的精确 HEAD GitHub Actions 运行。旧 H Run 44060704553 测试的是 H 1.2.12/C 1.0.1，不能作为 H 1.2.13 证据。

## 7. H disposition / H 侧决议

**Delegated H-role disposition: ACCEPT AS THE CURRENT 1.2.13 / C 1.0.1 MAPPING CANDIDATE WITH ENUMERATED VALIDATION BLOCKERS. NOT FROZEN.**

Required next steps:
1. Run the updated H tests on the exact current H branch HEAD and record the workflow run, tested commit and test-file Blob.
2. Add a full H 1.2.13 envelope + CSubmitOutcome 1.0.1 object positive test and one negative mutation for every duplicated field.
3. Add explicit CKeyStatusEvent namespace mismatch, stale key-status head and anti-rollback checkpoint vectors.
4. Keep all missing production callbacks fail-closed as UNKNOWN.
5. Obtain C's exact review of this updated H mapping/validator pair; then update Storage's successor bundle manifest and obtain a fresh A integration review.
6. I profile registration, production trust root/key lifecycle, provider-specific adapter proof, C sequencer, COC quorum and Storage deployment gates remain OPEN.

**角色模拟 H 侧决议：接受为当前 1.2.13 / C 1.0.1 映射候选，保留明确验证阻断项，不冻结。** 下一步必须执行精确 HEAD H 测试、补齐完整 Envelope/Object 及逐字段负向测试、验证 Key Status Namespace/Anti-Rollback，并取得 C 对更新后 H Mapping/Validator 的精确复审。随后更新 Storage 后继清单并由 A 重新集成审查。I Profile 注册、生产 Trust/Key Lifecycle、Provider Adapter、C Sequencer、COC Quorum 和 Storage 部署门禁仍 OPEN。
