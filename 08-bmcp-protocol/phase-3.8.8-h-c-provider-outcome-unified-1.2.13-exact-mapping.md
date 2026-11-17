# Phase 3.8.8 — H Exact C Provider Outcome Mapping for Unified Schema 1.2.13
# Phase 3.8.8 — H Unified Schema 1.2.13 的 C Provider Outcome 精确映射

- Owner perspective: H — BMCP Protocol / Schema and Interoperability
- Status: **SUCCESSOR MAPPING CANDIDATE / DELEGATED H-ROLE REVIEW / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H unified schema 1.2.13: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.13.schema.json`, Blob `88a33e26f3dbfa9b2f7286e72a5d98caae90dc67`
- H predecessor schema 1.2.12: Blob `9aa366d857d0229687df7e44e8e70d2097a99237` (historical; C outcome branch requires revision)
- CSubmitOutcome schema 1.0.0: Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- C Phase 3.8.9 contract: Blob `2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac`
- C Phase 3.8.10 exact compatibility review: Blob `3a01f4e605d0d6def574cffd8fedd77eae5d24bd`
- C Phase 3.8.6 semantic amendment: Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- C Phase 3.8.8 signature projection: Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- I C-crypto candidate addendum: Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
- Provenance: delegated H-role review in the coordinating session; **not an independent human H Owner signature**.

## 1. Exact version and supersession / 精确版本与替代关系

This successor mapping binds:
- `schema_id = bmcp.coc-jf10-unified`;
- wire `schema_version = 1.3.0`;
- exact artifact `schema_artifact_revision = 1.2.13`;
- `message_type = C_PROVIDER_OUTCOME_RECORDED`.

H 1.2.13 supersedes the H 1.2.12 C Provider Outcome branch only for this successor candidate. It does not silently rebind RecoveryCutoff 1.0.5 or RecoveryJoin 1.0.2, and it does not claim those companion schemas are changed.

本后继映射绑定：
- `schema_id = bmcp.coc-jf10-unified`；
- Wire `schema_version = 1.3.0`；
- 精确工件 `schema_artifact_revision = 1.2.13`；
- `message_type = C_PROVIDER_OUTCOME_RECORDED`。

H 1.2.13 仅在本后继候选范围内替代 H 1.2.12 的 C Provider Outcome 分支；不隐式改绑 RecoveryCutoff 1.0.5 或 RecoveryJoin 1.0.2，也不声称这两个伴随 Schema 已变更。

## 2. Schema 1.2.13 corrections / Schema 1.2.13 修正

Two corrections are normative for this candidate:

1. For `HANDOFF_REJECTED`, the structural schema requires `provider_request_ref` and `provider_outcome_evidence_ref`; it does **not** unconditionally require `provider_no_handoff_proof_ref`.
2. The ambiguous optional `participant_intent_ref` property is removed from the C outcome branch. `coc_participant_intent_ref` is the single authoritative nullable COC intent field; it is paired with `participant_reservation_ref` and `coc_absence_reason`.

The H schema retains `provider_no_handoff_proof_ref` as a field. The semantic validator requires it when C's dereferenced `SideEffectStatus=PROVEN_NONE` is used to establish no handoff; it does not require it for `POSSIBLE_OR_UNKNOWN` or `PROVEN_OCCURRED`.

本候选的两个规范修正：
1. HANDOFF_REJECTED 结构上要求 `provider_request_ref` 和 `provider_outcome_evidence_ref`，不再无条件要求 `provider_no_handoff_proof_ref`；
2. 从 C Outcome 分支删除语义重复且未定义的可选 `participant_intent_ref`，只保留权威 nullable 字段 `coc_participant_intent_ref`，并与 Reservation/AbsenceReason 成对校验。

Schema 保留 `provider_no_handoff_proof_ref` 字段。只有当 C 解引用对象的 SideEffectStatus=PROVEN_NONE 并据此证明无交接时，语义验证器才要求该证明；POSSIBLE_OR_UNKNOWN 或 PROVEN_OCCURRED 不得被强制转为无交接。

## 3. Exact object/wire mapping / 对象与 Wire 精确映射

The equality mapping from H Phase 3.8.7 remains applicable, with the following canonical fields:
- `c_submit_outcome_ref` ↔ C `record_ref`;
- `c_submit_outcome_digest` ↔ C `payload_digest`;
- `provider_outcome` ↔ C `Outcome`;
- `provider_ref` ↔ C `ProviderRef`;
- `provider_adapter_ref` ↔ C `AdapterRef`;
- `provider_idempotency_key_ref` ↔ C `IdempotencyKeyRef`;
- `final_request_boundary_id` ↔ C `FinalRequestBoundaryRef`;
- `request_digest` ↔ C `RequestDigest`;
- `transaction_ref` ↔ C `CausalOrderTransactionRef`;
- `provider_outcome_evidence_ref` ↔ C `OutcomeEvidenceRef`;
- `owner_admission_ref/digest` ↔ C `CAdmissionRef/CAdmissionDigest`;
- `owner_ledger_ref/version`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root` ↔ C `COwnerLedgerRef/Version/LocalSequence/HighWater/LedgerRoot`;
- `coc_participant_intent_ref` ↔ C `COCParticipantIntentRef`;
- `participant_reservation_ref` ↔ C `COCParticipantReservationRef`.

All duplicated values are exact equality assertions. A mismatch is INVALID; an unavailable object, ledger, verifier or currentness source is UNKNOWN. The C object's remaining tuple members (CGateRef/Generation/Commit, ProviderAttemptRef/Generation, ProviderAccountRef, AdapterBuildRef, EndpointRef, RegionRef, ApiOperation, IdempotencyNamespaceRef, ProviderCapabilityRecord/Digest, FinalRequestBoundaryType, request method/content type, SideEffectStatus and evidence digest/issuer/type) remain mandatory C-object dereference fields.

H Phase 3.8.7 的字段映射继续适用，规范字段如上。所有重复字段均为严格相等断言；不匹配为 INVALID；对象、Ledger、Verifier 或当前性来源不可用为 UNKNOWN。C 对象中的剩余 Gate/ProviderAttempt/Account/Endpoint/Region/API/Idempotency Namespace/Capability/Request Type/SideEffectStatus/Evidence Digest 等字段仍必须解引用，不能因 H 未内联而视为可选。

## 4. Digest and signature domains / 摘要与签名域

- H `c_submit_outcome_digest` equals C object `payload_digest` and is recomputed under the exact I-registered C profile.
- H common-envelope `payload_digest` protects the BMCP envelope and is a separate digest domain.
- C `OutcomeEvidenceDigest` binds the provider evidence and is a third separate digest domain.
- C object's signature and the BMCP envelope signature are separately validated protected objects; neither signature is inferred from the other.
- `AIMBA-C-CRYPTO-1.0` remains candidate/unregistered until I issues a formal profile registration and trust/key lifecycle decision.

H `c_submit_outcome_digest` 等于 C 对象 `payload_digest`，并须在 I 注册 C 配置后按该配置重新计算。H 信封 `payload_digest` 与 C `OutcomeEvidenceDigest` 是另外两个独立摘要域。C 对象签名与 BMCP 信封签名必须分别验证，不得相互推断。AIMBA-C-CRYPTO-1.0 仍是未注册候选配置。

## 5. Outcome semantic rules / Outcome 语义规则

| C Outcome | Required C semantic state | H structural fields | H semantic result |
|---|---|---|---|
| HANDOFF_ACCEPTED | `SideEffectStatus=PROVEN_OCCURRED`; request + receipt + outcome evidence; COC reservation/intent | provider request, receipt, outcome evidence, participant reservation | VALID only after C object/provider evidence and all authority joins verify |
| HANDOFF_REJECTED + PROVEN_NONE | provider request + outcome evidence + authoritative no-handoff proof | provider request, outcome evidence, provider no-handoff proof | May prove no side effect after proof verification |
| HANDOFF_REJECTED + POSSIBLE_OR_UNKNOWN | provider request + outcome evidence; no fabricated no-handoff proof | provider request, outcome evidence; no-handoff proof not required | Nonterminal / blocking; never safe retry-as-new |
| HANDOFF_REJECTED + PROVEN_OCCURRED | provider request + outcome evidence | provider request, outcome evidence | Reconcile observed side effect; never classify as no handoff |
| NOT_INVOKED | `SideEffectStatus=PROVEN_NONE`; no-handoff + not-invoked proofs | not-invoked proof; no provider receipt | VALID only after same-serialization-authority no-invocation proof |
| UNKNOWN / IN_DOUBT | `SideEffectStatus=POSSIBLE_OR_UNKNOWN`; unknown reason | unknown reason | UNKNOWN / IN_DOUBT; preserve original attempt/key/request tuple |

H semantic validation must not infer C side-effect status from the H enum. It must dereference the C object and verify the evidence. A provider rejection is not automatically a no-handoff result.

H 语义验证器不得从 H Outcome 枚举推断 C SideEffectStatus，必须解引用 C 对象并验证证据。Provider 拒绝不自动等于没有交接。

## 6. Nominal type and authority separation / 名义类型与权威隔离

- C `ProviderAttemptRef/Generation` is distinct from Storage `prepare_attempt_ref/generation`.
- C `COwnerLedgerRef/Version` is distinct from Storage `participant_ledger_ref/version`.
- C Provider Idempotency Namespace and Key are separate; H inline key reference does not replace the namespace.
- H `i_terminal_decision_ref`, `d_clearance_ref`, `storage_resolution_proof_ref`, and COC commit/record proofs are independent owner evidence, not C-owned outcome facts.
- C owns provider truth; I owns authorization/revocation and C profile governance; D owns ForgetFence/lineage clearance; Storage owns prepared participant and same-GID resolution; H owns wire and semantic mapping.

## 7. Required semantic vectors / 必需语义向量

The H12-C01..C18 vectors from Phase 3.8.7 remain required, with these additions:
- H13-C19: HANDOFF_REJECTED + PROVEN_NONE without no-handoff proof → INVALID.
- H13-C20: HANDOFF_REJECTED + POSSIBLE_OR_UNKNOWN without no-handoff proof → accepted as a nonterminal outcome, never treated as no-handoff.
- H13-C21: HANDOFF_REJECTED + PROVEN_OCCURRED → preserve occurred-side-effect evidence; no no-handoff classification.
- H13-C22: legacy `participant_intent_ref` present in the 1.2.13 C branch → INVALID as unknown/forbidden field.
- H13-C23: c_submit_outcome_digest equals BMCP envelope payload_digest but differs from C object payload_digest → INVALID.

These are specified vectors only; no 1.2.13 validator run is claimed.

## 8. Review disposition / 审查结论

**Delegated H-role disposition: ACCEPT AS A SUCCESSOR MAPPING CANDIDATE WITH ENUMERATED BLOCKERS; NOT FROZEN.**

Remaining blockers:
1. C must review and accept/revise this exact 1.2.13 mapping.
2. H semantic validator implementation and H13-C01..C23 execution are NOT RUN.
3. I crypto profile registration, trust roots, key lifecycle, historical verification and anti-rollback remain OPEN.
4. Independent Python/JavaScript canonical-byte and signature interoperability against the registered profile remains OPEN.
5. Provider-specific same-key lookup/idempotency and actual adapter fault/race tests remain OPEN.
6. Storage must bind the exact C outcome object and H envelope into the bidirectional RecoveryJoin proof.
7. A must perform exact-version integration review after fresh I/D/C/H decisions.

**JF-10 P0 remains OPEN.** No wire/crypto freeze, implementation/conformance PASS, provider exactly-once, production activation, Multi-PolicyDomain, Global Forget completion or physical Forget is claimed.

**角色模拟 H 侧结论：有条件接受为后继映射候选，尚有明确阻断项，不冻结。** H13 语义向量尚未执行；I 配置注册/密钥治理、跨语言互操作、Provider Adapter 实测、Storage RecoveryJoin 与 A 集成复审均未完成。JF-10 P0 仍 OPEN。
