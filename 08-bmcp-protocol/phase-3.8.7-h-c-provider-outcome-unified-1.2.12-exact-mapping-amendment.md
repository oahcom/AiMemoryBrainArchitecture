# Phase 3.8.7 — H Exact C Provider Outcome Mapping for Unified Schema 1.2.12
# Phase 3.8.7 — H Unified Schema 1.2.12 的 C Provider Outcome 精确映射

- Owner perspective: H — BMCP Protocol / Schema and Interoperability
- Status: **CANDIDATE MAPPING / DELEGATED H-ROLE REVIEW / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H unified schema: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.12.schema.json`, Blob `9aa366d857d0229687df7e44e8e70d2097a99237`
- H RecoveryCutoff schema 1.0.5: Blob `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`
- H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- CSubmitOutcome object schema 1.0.0: Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- C schema/conformance contract Phase 3.8.9: Blob `2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac`
- C semantic amendment Phase 3.8.6: Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- C signature projection Phase 3.8.8: Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- I C-crypto candidate addendum: Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
- Provenance: coordinator-authored delegated H-role review; **not an independent human H Owner signature**.

## 1. Purpose and version boundary / 目的与版本边界

This addendum replaces the historical H 1.2.11 C Provider Outcome mapping as the current mapping candidate. It does not alter the C-owned immutable object schema or authorize a wire/crypto freeze.

The exact H wire binding is:
- `schema_id = bmcp.coc-jf10-unified`;
- `schema_version = 1.3.0` (wire-family version);
- `schema_artifact_revision = 1.2.12` (exact schema artifact revision);
- `message_type = C_PROVIDER_OUTCOME_RECORDED`.

The H schema's common-envelope description was corrected to say artifact revision 1.2.12; its structural `schema_artifact_revision` constant is also 1.2.12. The schema's JSON was parsed successfully after the correction.

旧 H 1.2.11 的 C Provider Outcome 映射仅作为历史版本保留。本附录将 H 1.2.12 作为当前映射候选，不修改 C 自有不可变对象 Schema，也不授权 Wire 或密码学冻结。

精确绑定为：
- `schema_id = bmcp.coc-jf10-unified`；
- `schema_version = 1.3.0`（Wire 协议族版本）；
- `schema_artifact_revision = 1.2.12`（精确 Schema 工件修订）；
- `message_type = C_PROVIDER_OUTCOME_RECORDED`。

H Schema 公共信封中残留的 1.2.11 描述已更正为 1.2.12；结构约束本身也固定为 1.2.12，修订后 JSON 已成功解析。

## 2. Three digest domains — never conflate / 三种摘要域不得混用

1. **C object `payload_digest`** is the C-P0 digest defined by C's candidate profile construction. H field `c_submit_outcome_digest` MUST equal this exact C object field. H must recompute it from the dereferenced C object under the exact C profile once I registers that profile.
2. **BMCP envelope `payload_digest`** protects the H wire message's own canonical payload. It is not the C object digest and MUST NOT be compared as if it were `c_submit_outcome_digest`.
3. **Provider outcome evidence digest** is C object's `OutcomeEvidenceDigest`; it binds the provider evidence object and is distinct from both prior digests.

The C candidate profile `AIMBA-C-CRYPTO-1.0` remains **NOT REGISTERED**. Until I registers the profile and H has an approved canonical-byte/signature contract, successful JSON Schema validation or equality of digest strings does not establish an authenticated C outcome. The semantic result is UNKNOWN for trust-dependent decisions.

三种摘要必须严格区分：
1. C 对象的 `payload_digest` 是 C-P0 摘要；H 字段 `c_submit_outcome_digest` 必须与该字段完全相等。I 注册配置后，H 必须按精确 C 配置从解引用对象重新计算。
2. BMCP 信封的 `payload_digest` 保护 H Wire 消息自身的规范化载荷，不是 C 对象摘要，不得与 `c_submit_outcome_digest` 混为一谈。
3. Provider Outcome Evidence Digest 是 C 对象的 `OutcomeEvidenceDigest`，只绑定 Provider 证据对象。

C 候选配置 `AIMBA-C-CRYPTO-1.0` 仍未注册。在 I 注册且 H 完成批准的规范字节/签名契约前，Schema 校验或摘要字符串相等均不能证明 C Outcome 已认证；依赖信任的语义判定必须为 UNKNOWN。

## 3. Exact inline field mapping / 精确内联字段映射

The following mappings are equality assertions. If both the H field and the C object field exist, they MUST be byte-for-byte equal after their respective typed decoding. No normalization, case folding, fallback, or best-effort matching is permitted.

| H 1.2.12 field | C object field | Rule |
|---|---|---|
| `c_submit_outcome_ref` | `record_ref` | Exact immutable object reference |
| `c_submit_outcome_digest` | `payload_digest` | Exact equality; recompute only under registered profile |
| `provider_outcome` | `Outcome` | Exact enum equality |
| `provider_ref` | `ProviderRef` | Exact typed reference equality |
| `provider_adapter_ref` | `AdapterRef` | Exact typed reference equality |
| `provider_idempotency_key_ref` | `IdempotencyKeyRef` | Exact key reference; namespace remains object-only |
| `final_request_boundary_id` | `FinalRequestBoundaryRef` | Exact boundary identity |
| `request_digest` | `RequestDigest` | Exact digest equality |
| `transaction_ref` | `CausalOrderTransactionRef` | Exact typed transaction identity |
| `provider_request_ref` | `ProviderRequestRef` | Exact equality when applicable |
| `provider_receipt_ref` | `ProviderReceiptRef` | Exact equality when applicable |
| `provider_lookup_proof_ref` | `ProviderLookupProofRef` | Exact equality when applicable |
| `provider_no_handoff_proof_ref` | `ProviderNoHandoffProofRef` | Exact equality when applicable |
| `not_invoked_proof_ref` | `NotInvokedProofRef` | Exact equality when applicable |
| `unknown_reason_ref` | `UnknownReasonRef` | Exact equality for UNKNOWN / IN_DOUBT |
| `provider_outcome_evidence_ref` | `OutcomeEvidenceRef` | Exact reference; H also dereferences and verifies the C-bound evidence digest |
| `owner_admission_ref` | `CAdmissionRef` | Exact primary C owner-admission identity |
| `owner_admission_digest` | `CAdmissionDigest` | Exact digest equality |
| `owner_ledger_ref` | `COwnerLedgerRef` | C owner ledger; not Storage participant ledger |
| `owner_ledger_version` | `COwnerLedgerVersion` | Exact version equality |
| `owner_local_sequence` | `COwnerLocalSequence` | Exact owner-local sequence |
| `owner_high_water` | `COwnerHighWater` | Exact C owner high-water |
| `owner_ledger_root` | `COwnerLedgerRoot` | Exact C owner ledger root |
| `owner_signature_ref` | `OwnerSignatureRef` | Exact reference to C owner-signature evidence |
| `actual_inference_request_id` | `ActualInferenceRequestId` | Exact equality when present in C object |
| `coc_participant_intent_ref` | `COCParticipantIntentRef` | Exact nullable identity; null requires matching absence reason |
| `participant_reservation_ref` | `COCParticipantReservationRef` | Exact identity when required by outcome |

For the optional `participant_intent_ref` field in the H branch, the current schema does not define a distinct semantic owner or type from `coc_participant_intent_ref`. Until H publishes that distinction, if both are present they MUST be exactly equal; a mismatch is INVALID. A present `participant_intent_ref` MUST NOT be used to override a null `coc_participant_intent_ref`.

以上映射均为严格相等断言。两个位置均存在时，按各自类型解码后必须完全相等；不得规范化、忽略大小写、回退或模糊匹配。

H 分支中的可选字段 `participant_intent_ref` 当前没有定义与 `coc_participant_intent_ref` 不同的语义 Owner 或类型。在 H 明确其区别前，两者同时出现时必须完全相等；不相等即 INVALID。不得用前者覆盖后者的 null 状态。

## 4. C-object-only fields — mandatory dereference / 仅存在于 C 对象中的字段必须解引用

The following C-owned fields are not represented as equivalent inline fields in the H 1.2.12 C branch. H MUST obtain them from the immutable C object at `c_submit_outcome_ref`, verify the object digest, and preserve their nominal types:

- `CAdmissionRef` details beyond the primary `owner_admission_ref` join; `CAdmissionDigest` and C ledger entry identity.
- `CGateRef`, `CGateGeneration`, `CGateCommitRef`, `CGateCommitDigest`.
- `ProviderAttemptRef`, `ProviderAttemptGeneration`.
- `ProviderAccountRef`, `AdapterBuildRef`, `EndpointRef`, `RegionRef`, `ApiOperation`.
- `IdempotencyNamespaceRef` (H's `provider_idempotency_key_ref` is only the key identity).
- `ProviderCapabilityRecordRef`, `ProviderCapabilityDigest`.
- `FinalRequestBoundaryType`, `RequestContentType`, `RequestMethod`.
- `SideEffectStatus`, `OutcomeObservedAt`, `OutcomeEvidenceDigest`, `ProviderEvidenceIssuerRef`, `ProviderEvidenceType`.
- `PriorObservationRef`, `SupersedesObservationRef`, `ReconciliationParentRef`.

The H field `prepare_attempt_ref` / `prepare_attempt_generation` belongs to the Storage prepared-participant attempt. It MUST NOT be treated as C's `ProviderAttemptRef` / `ProviderAttemptGeneration`. Likewise, H `participant_ledger_ref` / `participant_ledger_version` is the Storage participant ledger, while H `owner_ledger_ref` / `owner_ledger_version` is the C owner ledger. These are distinct nominal identities even if their textual values happen to match.

The H schema does not inline C's complete provider account/endpoint/region/API/capability and egress-gate tuple. This is an explicit dereference obligation, not evidence that the tuple is absent or optional.

以下 C 自有字段在 H 1.2.12 C 分支中没有等价内联字段。H 必须通过 `c_submit_outcome_ref` 解引用不可变 C 对象、验证对象摘要并保留其名义类型：
- `CGateRef`、`CGateGeneration`、`CGateCommitRef`、`CGateCommitDigest`；
- `ProviderAttemptRef`、`ProviderAttemptGeneration`；
- Provider Account、Adapter Build、Endpoint、Region、API Operation；
- Idempotency Namespace、Provider Capability Record/Digest；
- Final Request Boundary Type、Request Content Type/Method；
- SideEffectStatus、OutcomeObservedAt、OutcomeEvidenceDigest、ProviderEvidenceIssuer/Type；
- Prior/Supersedes/Reconciliation Parent 等追加观察链字段。

H 的 `prepare_attempt_ref` / `prepare_attempt_generation` 属于 Storage prepared participant attempt，绝不能当成 C 的 ProviderAttemptRef/Generation。H 的 `participant_ledger_ref` / version 属于 Storage participant ledger；`owner_ledger_ref` / version 才对应 C owner ledger。即使文本值相同，它们也属于不同名义类型。

## 5. H-only evidence fields — separate authority joins / H 独有证据字段必须独立 Join

These H fields are not C-owned facts and MUST NOT be copied into or inferred from the C object:

- `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`;
- `prepared_participant_ref`, `prepare_attempt_ref`, `prepare_attempt_generation`, `participant_ledger_ref`, `participant_ledger_version`, `participant_tuple_digest`, `storage_resolution_proof_ref`;
- `i_terminal_decision_ref`, `d_clearance_ref`;
- COC/Storage quorum, record-position and commit evidence.

H validates these as separate authority proofs against exact I, D, Storage and COC references and the common immutable operation/participant tuple. A valid C object signature cannot synthesize I COMMIT_WON, D clearance, Storage resolution, COC quorum commitment or G Applied.

以下 H 字段不是 C 自有事实，不得复制进 C 对象或从 C 对象推断：
- COC Commit Proof、Record Ref、Position、Entry Digest；
- Storage PreparedParticipantRef、PrepareAttempt、ParticipantLedger、TupleDigest、StorageResolutionProof；
- I Terminal Decision 与 D Clearance；
- COC/Storage Quorum、Record Position 与 Commit 证据。

H 必须通过各自权威来源验证这些证据，并绑定到同一不可变操作/参与者元组。有效的 C 对象签名不能代替 I COMMIT_WON、D Clearance、Storage Resolution、COC Quorum 或 G Applied。

## 6. Outcome and cross-field predicates / Outcome 与跨字段谓词

H semantic validation MUST enforce all of the following in addition to JSON Schema:

1. The C object and H envelope have the same outcome enum and exact operation/request/owner-admission identity.
2. `HANDOFF_ACCEPTED` requires the exact provider request, provider receipt, outcome evidence, COC participant intent/reservation, and C `SideEffectStatus=PROVEN_OCCURRED`.
3. `HANDOFF_REJECTED` in C schema 1.0.0 requires `ProviderRequestRef` and permits `SideEffectStatus` values `PROVEN_NONE`, `POSSIBLE_OR_UNKNOWN` or `PROVEN_OCCURRED`. H schema 1.2.12 instead unconditionally requires `provider_no_handoff_proof_ref`. This is a BLOCKING semantic incompatibility: a no-handoff proof cannot be required when C explicitly records a possible or occurred side effect. Proposed H correction for the next schema artifact: require `provider_request_ref` and `provider_outcome_evidence_ref` for `HANDOFF_REJECTED`; require `provider_no_handoff_proof_ref` only when the dereferenced C object says `SideEffectStatus=PROVEN_NONE`. `POSSIBLE_OR_UNKNOWN` remains nonterminal/blocking and must not be treated as safe no-handoff; `PROVEN_OCCURRED` must be reconciled as an observed side effect. The current 1.2.12 schema does not satisfy this rule.
4. `NOT_INVOKED` requires both C `NotInvokedProofRef` and H `not_invoked_proof_ref`, C `SideEffectStatus=PROVEN_NONE`, and no provider receipt.
5. `UNKNOWN` / `IN_DOUBT` requires an immutable unknown reason, preserves the original provider attempt/key/request tuple and MUST NOT be upgraded by timeout, COC status or Storage resolution.
6. If `coc_participant_intent_ref` is null, `coc_absence_reason` is mandatory and must equal the C object's `COCAbsenceReason`; a handoff outcome with no COC participant/reservation is INVALID.
7. Any required C object member missing after authoritative dereference is INVALID. Unavailable object store, stale object, unavailable currentness, missing key-status proof or unavailable owner verifier is UNKNOWN.
8. H's `provider_outcome_evidence_ref` is compared with C `OutcomeEvidenceRef`; the C `OutcomeEvidenceDigest` is verified separately and must not be substituted with the BMCP envelope digest.
9. H's `participant_reservation_ref` and `participant_intent_ref` must obey the exact COC linkage pair; if both intent fields are present they must agree.
10. C ProviderAttempt identity/generation is validated from the C object and C owner ledger; Storage PrepareAttempt identity/generation is validated independently from the Storage receipt. No cross-type equality is inferred.

除 JSON Schema 外，H 语义验证器必须检查：
1. C 对象与 H 信封的 Outcome、操作/请求及 Owner Admission 身份一致；
2. HANDOFF_ACCEPTED 必须有精确 Provider Request/Receipt、Outcome Evidence、COC Intent/Reservation，以及 C 的 PROVEN_OCCURRED；
3. HANDOFF_REJECTED 必须有 Provider No-Handoff Proof 和 Outcome Evidence；仅有拒绝标签不能证明没有副作用；
4. NOT_INVOKED 必须有 NotInvokedProof、PROVEN_NONE 且不得带 Provider Receipt；
5. UNKNOWN/IN_DOUBT 必须保留原 Provider Attempt/Key/Request 元组，不能由超时、COC 状态或 Storage Resolution 升级；
6. COC Intent 为 null 时必须提供与 C 对象一致的 AbsenceReason；无 COC Participant/Reservation 的 HANDOFF 结果无效；
7. 缺失权威 C 对象成员为 INVALID；对象不可用、当前性未知、Key Status 或 Owner Verifier 不可用均为 UNKNOWN；
8. Provider Outcome Evidence Ref 与 C 对象精确一致，OutcomeEvidenceDigest 独立验证，不得替换成 BMCP Envelope Digest；
9. Reservation 与 Intent 必须满足 COC 成对关系；两个 Intent 字段同时存在时必须一致；
10. C ProviderAttempt 与 Storage PrepareAttempt 分别验证，不得跨类型比较。

## 7. Security and authority boundary / 安全与权威边界

- H owns structural parsing, exact field mapping, canonical wire bytes, schema versioning and tri-state semantic orchestration.
- C owns CSubmitOutcome semantics, provider attempt, gate generation, provider identity, idempotency namespace/key, final request boundary and actual provider outcome.
- I owns signature profile registration, trust roots, key custody/status/rotation/revocation/compromise, historical verification and anti-rollback.
- D owns ForgetFence, affected lineage and D clearance.
- Storage owns prepared participant identity, DB incarnation, Storage attempt/ledger, same-GID resolution and visibility proof.
- A owns integration composition and freeze recommendation, not the other Owners' decisions.

The C profile remains candidate / unregistered. The H helper/owner-verifier callback remains TEST-ONLY. No production owner-verifier, COC quorum, provider adapter, signature trust or runtime conformance is claimed.

## 8. Required vectors / 必需向量（均为待执行要求）

Add at least:
- H12-C01: schema artifact revision 1.2.11 downgrade;
- H12-C02: C object ref/digest mismatch;
- H12-C03: C object payload_digest differs from c_submit_outcome_digest;
- H12-C04: C GateGeneration absent or stale in dereferenced object;
- H12-C05: C ProviderAttempt differs from provider lookup evidence;
- H12-C06: Storage PrepareAttempt substituted for C ProviderAttempt;
- H12-C07: Storage participant ledger substituted for C owner ledger;
- H12-C08: provider account/endpoint/region/API operation missing from C object;
- H12-C09: provider idempotency key equal but namespace mismatch;
- H12-C10: participant_intent_ref differs from coc_participant_intent_ref;
- H12-C11: null COC intent without matching absence reason;
- H12-C12: HANDOFF_ACCEPTED without receipt or COC reservation;
- H12-C13: HANDOFF_REJECTED without authoritative no-handoff proof;
- H12-C14: NOT_INVOKED with provider receipt or POSSIBLE_OR_UNKNOWN side effect;
- H12-C15: UNKNOWN/IN_DOUBT changed attempt/key/request tuple;
- H12-C16: missing/revoked/unknown C key status;
- H12-C17: BMCP envelope payload_digest confused with C object payload_digest;
- H12-C18: C provider outcome evidence digest substituted by another digest domain.

These vectors are specified only. No new test run is claimed.

## 9. Review disposition / 审查结论

**Delegated H-role disposition: NEEDS REVISION for exact compatibility with CSubmitOutcome 1.0.0. The mapping table is a candidate; H schema 1.2.12 is NOT ACCEPTED as a compatible C outcome branch. NOT FROZEN.**

Blocking before joint wire/crypto freeze:
1. H must publish a successor schema artifact correcting the HANDOFF_REJECTED conditional so it does not equate provider rejection with proof of no side effect.
2. H must resolve the semantic distinction, if any, between `participant_intent_ref` and `coc_participant_intent_ref`.
3. C must publish an exact compatibility addendum pinning the successor H schema and confirm all object-to-wire mappings.
4. H must implement the semantic dereference/join validator and run the exact-version vectors.
5. I must register or reject the C signature profile and approve key-status/trust/anti-rollback policy.
6. C/H must bind independent Python/JavaScript canonical-byte vectors to the exact current schema and registered profile.
7. A must re-review the same exact bundle after I/D/C/H decisions.

**JF-10 P0 remains OPEN.** This review does not approve Gate B/C implementation, production activation, Multi-PolicyDomain, Global Forget completion, provider exactly-once, or physical Forget.

**角色模拟的 H 侧结论：有条件接受为版本化映射候选，存在阻断项，不冻结。** 上述审查由协调会话扮演 H 角色完成，不是独立人类 H Owner 签署。JF-10 P0 仍 OPEN，不批准 Gate B/C 实现、生产激活、多 PolicyDomain、Global Forget、Provider exactly-once 或物理 Forget。
