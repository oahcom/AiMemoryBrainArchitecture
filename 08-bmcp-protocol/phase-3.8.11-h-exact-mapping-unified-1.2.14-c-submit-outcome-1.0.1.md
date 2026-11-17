# Phase 3.8.11 — H Exact Mapping: Unified 1.2.14 × CSubmitOutcome 1.0.1
# Phase 3.8.11 — H 精确映射：Unified 1.2.14 × CSubmitOutcome 1.0.1

- Owner: H — BMCP Protocol / Schema / Interoperability
- Branch: `session-h-bmcp-protocol`
- Status: **CURRENT SUCCESSOR MAPPING CANDIDATE / C REVIEW REQUIRED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Exact H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- Exact CSubmitOutcome object schema 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- H RecoveryCutoff schema 1.0.5: Blob `75cd11e3c9a7c63a7ad9c438f20174df8f43c66a`
- C Phase 3.11.1 sequence namespace amendment: Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`
- I Phase 3.8.8 C sequence namespace review: Blob `0d78e5b2bfcf66cae6b757314cead84b9c942601`
- C profile identifier ownership decision: Blob `5067dadb9c646a054d78f03c56e635facc36311a`
- I C-profile scope clarification: Blob `1e86a1349d371a1cdb4a56d69f783e0f316c7203`
- C signature projection: Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- C key-status lifecycle contract: Blob `9339b168165a7a3dd34def5236ad61cfd3163418`
- C key-status event schema: Blob `908b293eba337e9fa75864cea3704e28a1a8d82e`
- I key-status governance review: Blob `57d1b1ca616eaec6df1dee82ddaccc66519caca2`
- D RecoveryJoin 1.0.2 D-high-water crosswalk: Blob `bf35b7f047a374268920b99199c06fc2a78dabb7`
- H validator core: Blob `910e2a8f0b22adb4a192b3dbb7483e52a881e993`
- H validator tests: Blob `9ceab387e114f9a28f9dfc12602e57f3ec5a3f43`
- H C 1.0.1 crypto tests: Blob `5559fb7a612c8dd92345ceae3a6aa62f4faae41a`
- H CI run for corrected H 1.2.14 schema: run `44067666900`, exact tested commit `9892c21b9311fa08976c4b24c34fe87a509a71ea` (pending final readback at publication time).
- English and Chinese are normative peers.

## 1. Exact version and scope / 精确版本与范围

This mapping binds:
- `schema_id = bmcp.coc-jf10-unified`;
- wire `schema_version = 1.3.0`;
- exact `schema_artifact_revision = 1.2.14`;
- `message_type = C_PROVIDER_OUTCOME_RECORDED`;
- exact C object schema/version/artifact revision 1.0.1.

H Unified 1.2.14 supersedes 1.2.13 for the current wire family. The 1.2.14 schema description and common-envelope artifact revision are aligned to 1.2.14. The 1.2.14 D owner-specific high-water addition is separately governed by D's exact RecoveryJoin crosswalk; C does not own or reinterpret that D field.

本映射绑定 H Unified 1.2.14 / Wire 1.3.0 / C Provider Outcome Message Family，并精确绑定 C 对象 Schema 1.0.1。H 1.2.14 替代 1.2.13。Schema Description 与 Common Envelope Artifact Revision 均已校正为 1.2.14。1.2.14 新增的 D Owner-Specific High-Water 由 D 的 RecoveryJoin Crosswalk 单独约束；C 不拥有也不解释该 D 字段。

## 2. Exact object/wire mapping / 对象与 Wire 映射

| H wire field | CSubmitOutcome 1.0.1 field | Rule |
|---|---|---|
| `c_submit_outcome_ref` | `record_ref` | exact typed reference equality |
| `c_submit_outcome_digest` | `payload_digest` | recompute and exact equality |
| `provider_outcome` | `Outcome` | exact enum equality |
| `provider_ref` | `ProviderRef` | exact typed reference equality |
| `provider_adapter_ref` | `AdapterRef` | exact typed reference equality |
| `provider_idempotency_key_ref` | `IdempotencyKeyRef` | exact typed reference equality |
| `provider_request_ref` | `ProviderRequestRef` | exact equality when present |
| `provider_receipt_ref` | `ProviderReceiptRef` | exact equality when present |
| `final_request_boundary_id` | `FinalRequestBoundaryRef` | exact equality |
| `request_digest` | `RequestDigest` | exact digest equality |
| `transaction_ref` | `CausalOrderTransactionRef` | exact typed reference equality |
| `provider_outcome_evidence_ref` | `OutcomeEvidenceRef` | exact equality |
| `owner_admission_ref/digest` | `CAdmissionRef/CAdmissionDigest` | exact equality |
| `owner_ledger_ref/version` | `COwnerLedgerRef/COwnerLedgerVersion` | exact equality |
| `owner_local_sequence` | `COwnerLocalSequence` | exact equality |
| `owner_high_water` | `COwnerHighWater` | exact equality |
| `owner_ledger_root` | `COwnerLedgerRoot` | exact equality |
| `coc_participant_intent_ref` | `COCParticipantIntentRef` | exact nullable equality |
| `participant_reservation_ref` | `COCParticipantReservationRef` | exact nullable equality |
| `coc_absence_reason` | `COCAbsenceReason` | exact nullable equality |

Every duplicated field is an assertion, not a hint. Mismatch is INVALID. Missing/unavailable C object, provider evidence, ledger, verifier or currentness source is UNKNOWN. H must dereference the complete C object, including C Gate/GateCommit, ProviderAttemptRef/Generation, ProviderAccountRef, AdapterBuildRef, EndpointRef, RegionRef, ApiOperation, IdempotencyNamespaceRef, ProviderCapabilityRecord/Digest, FinalRequestBoundaryType, method/content type, SideEffectStatus and evidence issuer/type/digest. No field is inferred from the H wrapper.

重复字段是严格断言，不是提示。字段不匹配为 INVALID；C 对象、Provider Evidence、Ledger、Verifier 或 Currentness 来源不可用为 UNKNOWN。H 必须解引用完整 C 对象，包括 Gate/GateCommit、ProviderAttempt、Account、AdapterBuild、Endpoint、Region、API Operation、Idempotency Namespace、Provider Capability、Final Request Boundary Type、Method/ContentType、SideEffectStatus 及 Evidence Issuer/Type/Digest。不得从 H Wrapper 推断。

## 3. C signature and key-governance profiles / C 签名与 Key Governance Profile

The exact profile identities are:
- C data signature profile: `AIMBA-C-CRYPTO-1.0`, C-owned.
- I governance signature profile for C key-status events: `AIMBA-I-KEY-GOVERNANCE-1.0`, I-owned.
- I data-plane profile `AIMBA-I-CRYPTO-1.0` is separate and is not inherited by C.
- `AIMBA-C-OUTCOME-CRYPTO-1.0` is a non-normative historical example and MUST NOT be registered or accepted as the C profile.

CSubmitOutcome 1.0.1 uses a closed schema (`additionalProperties=false`). C-P0 is every present schema-allowed C object member except `payload_digest` and `signature`. The exact profile ID, message type, owner/issuer/audience/purpose, key ID/version, sequence namespace, provider/attempt/request/outcome/evidence and owner ledger/gate fields are all signed. `sequence_namespace_ref` is required and included in C-P0.

C Data Profile 与 I Key Governance Profile 完全分离。I 的 Data-plane Profile 不得被 C 继承；历史示例 `AIMBA-C-OUTCOME-CRYPTO-1.0` 不得注册或作为 C Profile 接受。CSubmitOutcome 1.0.1 的 Schema 为封闭结构；C-P0 是所有出现且允许的 C 对象字段，唯一排除 payload_digest 和 signature。Sequence Namespace、Provider/Attempt/Request/Outcome/Evidence 与 Owner Ledger/Gate 字段均参与签名。

## 4. Outcome/side-effect semantics / Outcome 与副作用语义

| Outcome | SideEffectStatus | Required evidence / result |
|---|---|---|
| HANDOFF_ACCEPTED | PROVEN_OCCURRED | request + receipt + outcome evidence + reservation; proves accepted handoff only |
| HANDOFF_REJECTED | PROVEN_NONE | request + outcome evidence + authoritative no-handoff proof; no-side-effect terminal |
| HANDOFF_REJECTED | POSSIBLE_OR_UNKNOWN | nonterminal/blocking; no no-handoff inference or retry-as-new |
| HANDOFF_REJECTED | PROVEN_OCCURRED | preserve occurred-side-effect fact and reconcile |
| NOT_INVOKED | PROVEN_NONE | both ProviderNoHandoffProofRef and NotInvokedProofRef; provider receipt forbidden |
| UNKNOWN / IN_DOUBT | POSSIBLE_OR_UNKNOWN | unknown reason; same attempt/key/request; no retry-as-new |

A rejection label alone never proves no side effect. H derives no side-effect only from the dereferenced C `SideEffectStatus=PROVEN_NONE` and the corresponding authoritative proof.

拒绝标签本身不能证明没有副作用。H 只能通过解引用 C `SideEffectStatus=PROVEN_NONE` 及对应权威证明得出无副作用结论。

## 5. Sequence namespace and key status / Sequence Namespace 与 Key Status

- C `record_sequence` and CKeyStatusEvent `event_sequence` share one authenticated C authority `sequence_namespace_ref`.
- H must verify exact namespace equality and monotonic ordering within that namespace; wall-clock, process-local counters and arrival order are insufficient.
- C owns C data-key lifecycle event production and CSubmitOutcome signing.
- I owns the governance trust root/profile and signs/authorizes C key-status events under `AIMBA-I-KEY-GOVERNANCE-1.0`.
- H verifies I governance signatures, C data signatures, key status at the C signing sequence and anti-rollback.
- Storage pins immutable C/I key-status event/checkpoint refs but cannot issue trust decisions.

## 6. H 1.2.14 D high-water boundary / H 1.2.14 D High-Water 边界

H 1.2.14 adds `ownerSpecificHighWatersD.forget_fence_generation_high_water`. It is distinct from `owner_gate_generation` and `barrier_generation`. D Phase 3.8.6 crosswalk Blob `bf35b7f047a374268920b99199c06fc2a78dabb7` defines the no-loss join to the exact D owner entry digest, ForgetOperation digest, scope binding, snapshot attestation and D fence high-water.

C accepts this as a D-owned H schema field only. C does not sign, derive, validate or substitute the D high-water. H/Storage must use D's exact crosswalk and owner proof.

H 1.2.14 新增 D ForgetFenceGeneration High-Water。该字段与 Gate Generation、Barrier Generation 不同。D Phase 3.8.6 Crosswalk 已定义其与 D Owner Entry/ForgetOperation/Scope/Snapshot Attestation 的无损 Join。C 仅接受其为 D 自有 Schema 字段，不签署、不推导、不验证，也不替代该 D High-Water。

## 7. Exact conformance evidence / 精确符合性证据

The H Provider Outcome workflow for corrected H schema 1.2.14 and C object 1.0.1 is running on exact commit `9892c21b9311fa08976c4b24c34fe87a509a71ea` (run `44067666900`). The exact run result must be read back and pinned by the H closure addendum; this mapping does not pre-claim PASS.

The test suite covers schema artifact revision, D fence high-water distinctness, C sequence namespace, conditional HANDOFF_REJECTED/SideEffectStatus, removal of the ambiguous alias, Python/Node candidate signature agreement and field-mutation rejection. It is bounded reference-model/schema/crypto-vector evidence only.

H 1.2.14 / C 1.0.1 精确 Provider Outcome Workflow 正在 Commit `9892c21b9311fa08976c4b24c34fe87a509a71ea` 上运行（Run `44067666900`）。结果必须由 H Closure Addendum 读回并绑定；本 Mapping 不预先声明 PASS。

## 8. Review and freeze boundary / 审查与冻结边界

**H disposition:** successor mapping candidate; exact C Owner review and H CI readback required. Not frozen.

**Not claimed:** production C profile registration, I governance root registration, HSM/KMS, key custody, live C sequencer/key-status ledger, provider evidence truth, authoritative same-key lookup, provider exactly-once, live multi-replica egress serialization, COC quorum durability, Storage JF-10 integration, RecoveryJoin end-to-end completeness, production deployment or Full Applied.

**H 侧结论：** 后继 Mapping 候选，仍需 C Owner 精确审查和 H CI 读回，不冻结。未声称生产 C Profile/I Governance Root 注册、HSM/KMS、Key Custody、实时 C Sequencer/Key Status、Provider Truth、同键查询、Exactly-once、多副本 Egress、COC Quorum、Storage JF-10、端到端 RecoveryJoin、生产部署或 Full Applied。
