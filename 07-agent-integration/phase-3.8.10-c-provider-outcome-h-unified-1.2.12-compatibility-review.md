# Phase 3.8.10 — C Exact Compatibility Review: Provider Outcome × H Unified 1.2.12
# Phase 3.8.10 — C Provider Outcome 与 H Unified 1.2.12 精确兼容性复审

- Owner perspective: C — Provider Outcome semantic authority
- Status: **NEEDS REVISION for H 1.2.12 C-branch compatibility; C object semantics remain PROPOSED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- CSubmitOutcome 1.0.0 schema: `07-agent-integration/schemas/c-submit-outcome-1.0.0.schema.json`, Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- C Phase 3.8.9 schema/conformance contract: Blob `2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac`
- C Phase 3.8.6 gate/attempt/idempotency amendment: Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- C Phase 3.8.8 signature projection: Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- H Unified schema 1.2.12 (wire 1.3.0): Blob `9aa366d857d0229687df7e44e8e70d2097a99237`
- H Phase 3.8.7 mapping review: Blob `c9a56ed1eaca6624daad68ff150744bd3be98092`
- H RecoveryCutoff schema 1.0.5: Blob `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`
- H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- I C-crypto candidate addendum: Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
- Provenance: delegated C-role simulation in the coordinating session; **not an independent human C Owner signature**.

## 1. Exact-version correction / 精确版本纠正

C's Phase 3.8.9 and 3.8.8 documents still name H artifact 1.2.11. That pin is historical and is superseded for current compatibility review by H Unified schema artifact revision **1.2.12**, wire family **1.3.0**, exact Blob `9aa366d857d0229687df7e44e8e70d2097a99237`.

C's immutable object schema 1.0.0 remains the same exact source. The H wire envelope does not replace, rewrite or become the source of C-owned provider truth. H must dereference the immutable C object and compare every duplicated wire field.

C 的 Phase 3.8.9 与 3.8.8 文档仍引用 H 1.2.11。该引用仅为历史版本；当前兼容性复审应绑定 H Unified Schema 工件修订 **1.2.12**、Wire 协议族版本 **1.3.0**、Blob `9aa366d857d0229687df7e44e8e70d2097a99237`。

C 的不可变对象 Schema 1.0.0 仍是相同精确源。H Wire 信封不能替代、改写或成为 C Provider 事实的权威来源。H 必须解引用不可变 C 对象，并逐字段比较重复 Wire 值。

## 2. C-owned field mapping / C 自有字段映射

C accepts the following H 1.2.12 mapping as a candidate, subject to the blocking schema conflict in §3:

| C object field | H wire field | C disposition |
|---|---|---|
| `record_ref` | `c_submit_outcome_ref` | Exact immutable object reference |
| `payload_digest` | `c_submit_outcome_digest` | Exact equality; recompute only under I-registered C profile |
| `Outcome` | `provider_outcome` | Exact enum equality |
| `ProviderRef` | `provider_ref` | Exact typed identity |
| `AdapterRef` | `provider_adapter_ref` | Exact typed identity |
| `IdempotencyKeyRef` | `provider_idempotency_key_ref` | Exact key; namespace remains C-object-only |
| `FinalRequestBoundaryRef` | `final_request_boundary_id` | Exact boundary identity |
| `RequestDigest` | `request_digest` | Exact digest |
| `CausalOrderTransactionRef` | `transaction_ref` | Exact typed transaction identity |
| `ProviderRequestRef` | `provider_request_ref` | Exact when applicable |
| `ProviderReceiptRef` | `provider_receipt_ref` | Exact when applicable |
| `ProviderLookupProofRef` | `provider_lookup_proof_ref` | Exact when applicable |
| `ProviderNoHandoffProofRef` | `provider_no_handoff_proof_ref` | Exact when applicable |
| `NotInvokedProofRef` | `not_invoked_proof_ref` | Exact when applicable |
| `UnknownReasonRef` | `unknown_reason_ref` | Exact for UNKNOWN / IN_DOUBT |
| `OutcomeEvidenceRef` | `provider_outcome_evidence_ref` | Exact evidence reference |
| `CAdmissionRef / CAdmissionDigest` | `owner_admission_ref / owner_admission_digest` | Exact C primary admission identity/digest |
| `COwnerLedgerRef / Version` | `owner_ledger_ref / owner_ledger_version` | C ledger, never Storage ledger |
| `COwnerLocalSequence / HighWater / Root` | `owner_local_sequence / owner_high_water / owner_ledger_root` | Exact C ledger currentness tuple |
| `OwnerSignatureRef` | `owner_signature_ref` | Exact C signature evidence reference |
| `ActualInferenceRequestId` | `actual_inference_request_id` | Exact if present in C object |
| `COCParticipantIntentRef` | `coc_participant_intent_ref` | Exact nullable COC intent |
| `COCParticipantReservationRef` | `participant_reservation_ref` | Exact reservation identity |

The H optional `participant_intent_ref` has no separately defined C semantic field. Until H defines a distinct authority/type, C requires it to be absent or exactly equal to `coc_participant_intent_ref`; a mismatch is INVALID. It cannot override a null COC intent.

以上映射作为候选接受，但受第 3 节阻断项约束。H 可选字段 `participant_intent_ref` 当前没有独立的 C 语义字段；H 明确独立类型/权威前，C 要求其缺省或与 `coc_participant_intent_ref` 完全相等，不相等即 INVALID，且不能覆盖 COC intent 的 null 状态。

## 3. Blocking incompatibility — HANDOFF_REJECTED / 阻断性不兼容：HANDOFF_REJECTED

The exact C object schema permits:

- `Outcome=HANDOFF_REJECTED`;
- `SideEffectStatus=PROVEN_NONE`, `POSSIBLE_OR_UNKNOWN`, or `PROVEN_OCCURRED`;
- `ProviderRequestRef` is required;
- a provider rejection label alone does not prove that no side effect occurred.

H Unified 1.2.12 instead unconditionally requires `provider_no_handoff_proof_ref` for `provider_outcome=HANDOFF_REJECTED`. This is not compatible with C's explicit ambiguous-side-effect and occurred-side-effect states. A no-handoff proof cannot be mandatory when C records `POSSIBLE_OR_UNKNOWN` or `PROVEN_OCCURRED`.

**C decision: NEEDS REVISION.** H must publish a successor schema artifact with this conditional contract:

1. `HANDOFF_REJECTED` structurally requires `provider_request_ref` and `provider_outcome_evidence_ref`.
2. `provider_no_handoff_proof_ref` is required only when the dereferenced C object says `SideEffectStatus=PROVEN_NONE`.
3. If C says `POSSIBLE_OR_UNKNOWN`, the outcome remains nonterminal/blocking for any action requiring proof of no side effect. H must not synthesize `PROVEN_NONE`.
4. If C says `PROVEN_OCCURRED`, the side effect must be reconciled as occurred; H must not relabel it as no handoff.
5. A provider rejection response, timeout, transport error or missing receipt is not a substitute for authoritative side-effect evidence.

精确 C 对象 Schema 允许 HANDOFF_REJECTED 同时携带 PROVEN_NONE、POSSIBLE_OR_UNKNOWN 或 PROVEN_OCCURRED；并要求 ProviderRequestRef。Provider 拒绝标签本身不证明没有副作用。

H Unified 1.2.12 却对 HANDOFF_REJECTED 无条件要求 `provider_no_handoff_proof_ref`。这与 C 明确允许的模糊副作用/已发生副作用状态不兼容。若 C 记录 POSSIBLE_OR_UNKNOWN 或 PROVEN_OCCURRED，就不能强制要求“未发生交接”证明。

**C 决议：NEEDS REVISION。** H 必须发布后继 Schema：
1. HANDOFF_REJECTED 结构上要求 `provider_request_ref` 和 `provider_outcome_evidence_ref`；
2. 只有 C 对象的 SideEffectStatus=PROVEN_NONE 时，才要求 `provider_no_handoff_proof_ref`；
3. POSSIBLE_OR_UNKNOWN 必须保持非终态/阻塞，不能被合成为 PROVEN_NONE；
4. PROVEN_OCCURRED 必须按已发生副作用进行协调，不能重标为未交接；
5. Provider 拒绝响应、超时、传输错误或缺失 Receipt 均不能替代权威副作用证据。

## 4. Mandatory dereference and nominal type separation / 强制解引用与名义类型隔离

The H 1.2.12 C branch does not inline the complete C tuple. The following MUST be read from the immutable C object and checked against the C owner ledger/provider evidence:

- `CGateRef`, `CGateGeneration`, `CGateCommitRef`, `CGateCommitDigest`;
- `ProviderAttemptRef`, `ProviderAttemptGeneration`;
- `ProviderAccountRef`, `AdapterBuildRef`, `EndpointRef`, `RegionRef`, `ApiOperation`;
- `IdempotencyNamespaceRef`, `ProviderCapabilityRecordRef`, `ProviderCapabilityDigest`;
- `FinalRequestBoundaryType`, `RequestContentType`, `RequestMethod`;
- `SideEffectStatus`, `OutcomeObservedAt`, `OutcomeEvidenceDigest`, `ProviderEvidenceIssuerRef`, `ProviderEvidenceType`;
- prior/supersession/reconciliation linkage fields.

Strict type separation:
- C `ProviderAttemptRef/Generation` is not H `prepare_attempt_ref/generation`; the latter is Storage's prepared-participant attempt.
- C `COwnerLedgerRef/Version` is not H `participant_ledger_ref/version`; the latter is Storage's participant ledger.
- H `provider_idempotency_key_ref` maps only the key; it does not carry C's namespace.
- BMCP envelope `payload_digest` is not C object `payload_digest` / `c_submit_outcome_digest`.
- C's `OutcomeEvidenceDigest` is not the BMCP envelope digest or C object digest.

H 1.2.12 C 分支未内联完整 C 元组。以下字段必须从不可变 C 对象读取，并与 C Owner Ledger/Provider Evidence 核验：CGate、ProviderAttempt、ProviderAccount、AdapterBuild、Endpoint、Region、API Operation、Idempotency Namespace、Provider Capability、Final Request Boundary Type、Request Content Type/Method、SideEffectStatus、OutcomeObservedAt、OutcomeEvidenceDigest、ProviderEvidenceIssuer/Type 及追加观察链字段。

严格类型隔离：
- C ProviderAttempt 不是 H prepare_attempt；后者属于 Storage；
- C OwnerLedger 不是 H participant_ledger；后者属于 Storage；
- H provider_idempotency_key_ref 只映射 Key，不含 C Namespace；
- BMCP Envelope payload_digest 不等于 C 对象 payload_digest / c_submit_outcome_digest；
- OutcomeEvidenceDigest 也不等于上述任一摘要。

## 5. Independent evidence joins / 独立证据 Join

H-only fields remain independently authoritative and must not be inferred from the C object:

- COC commit proof, COC record ref/position/entry digest;
- Storage PreparedParticipantRef, Storage PrepareAttempt, Storage ParticipantLedger, ParticipantTupleDigest and StorageResolutionProof;
- I terminal decision proof;
- D clearance proof.

C's object does not mint I COMMIT_WON, D clearance, Storage resolution, COC quorum commitment or G Applied. Every such proof must bind the same operation/participant tuple and be verified by its own authority. C's immutable provider outcome remains C-owned and cannot be synthesized from a Storage commit or COC recovery state.

H 独立字段继续由各自权威负责，不能从 C 对象推断：COC Commit/Record 证明、Storage PreparedParticipant/Attempt/Ledger/Resolution、I Terminal Decision、D Clearance。C 对象不能签发 I COMMIT_WON、D Clearance、Storage Resolution、COC Quorum 或 G Applied。所有证明都必须绑定同一操作/参与者元组并由各自权威验证。

## 6. Outcome cross-checks / Outcome 交叉核验

- HANDOFF_ACCEPTED: C requires ProviderRequestRef + ProviderReceiptRef and `SideEffectStatus=PROVEN_OCCURRED`; H requires provider request/receipt/evidence and COC reservation.
- HANDOFF_REJECTED: apply §3; never infer no side effect from the rejection enum.
- NOT_INVOKED: C requires ProviderNoHandoffProofRef + NotInvokedProofRef and `SideEffectStatus=PROVEN_NONE`; H's not-invoked proof must equal the C object.
- UNKNOWN / IN_DOUBT: C requires UnknownReasonRef and `SideEffectStatus=POSSIBLE_OR_UNKNOWN`; preserve original attempt, namespace/key, request boundary and digest; no retry-as-new.
- COC intent/reservation is an atomic pair: both present or both null with explicit COCAbsenceReason. H's nullable `coc_participant_intent_ref` and `coc_absence_reason` must match the C object exactly. H handoff outcomes require a reservation; a no-COC absence cannot authorize provider invocation.

## 7. Correction to C Phase 3.8.9 evidence wording / 对 C Phase 3.8.9 测试表述的纠正

C Phase 3.8.9 §7 says “No tests have been executed by this artifact,” while §§8–10 record completed CI runs. This addendum clarifies the correct evidence ledger:

| Evidence | Run | Result | Scope |
|---|---:|---|---|
| C schema/selected semantic suite | `44055965702` | 3 passed | C schema + 10 synthetic vectors / selected semantic predicates |
| C candidate JCS/Ed25519 suite | `44057463855` | 7 passed | Candidate-only Python/Node construction; public test seed; profile unregistered |
| H independent candidate JCS/Ed25519 suite | `44057944517` | 10 passed | Independent candidate verification against byte-identical C schema/vectors |

The §7 sentence is superseded as a stale editorial statement. These results are bounded CI evidence only. They do not register `AIMBA-C-CRYPTO-1.0`, approve C trust roots/key custody/anti-rollback, prove provider truth, execute live C gate races, verify owner-ledger/COC inclusion or certify production adapters.

C Phase 3.8.9 §7 写有“No tests have been executed by this artifact”，但 §§8–10 又列出了成功 CI。此处明确：§7 句子属于过时编辑表述，按本附录纠正。现有证据仅为受限 CI，不代表配置注册、信任根/密钥治理批准、真实 Provider 事实、Gate Race、Owner Ledger/COC 纳入或生产 Adapter 认证。

## 8. C disposition / C 侧决议

**Delegated C-role disposition: NEEDS REVISION for H Unified 1.2.12 compatibility.** C accepts its own immutable object schema and the field-mapping proposal as candidates, but rejects the current H 1.2.12 HANDOFF_REJECTED conditional as incompatible with C's signed semantic contract.

Required next steps:
1. H publishes a successor schema revision correcting the outcome conditional and resolving the intent-field ambiguity.
2. C rebinds this mapping to the exact successor H schema Blob and publishes updated vectors.
3. H updates its semantic validator contract and runs the exact successor-schema tests.
4. I decides whether to register or reject the C crypto profile and publishes the key-status/trust/anti-rollback policy.
5. C/H execute independent cross-language canonical-byte and signature vectors under the registered profile.
6. A performs exact-version integration review only after I/D/C/H bind the same bundle.

**JF-10 P0 remains OPEN.** No cryptographic freeze, wire freeze, provider exactly-once, implementation/conformance PASS, production activation, Multi-PolicyDomain, Global Forget completion or physical Forget is claimed.

**角色模拟的 C 侧结论：H 1.2.12 兼容性 NEEDS REVISION。** C 自有不可变对象 Schema 与字段映射建议可作为候选；但当前 H 1.2.12 的 HANDOFF_REJECTED 条件与 C 语义合同不兼容。JF-10 P0 仍 OPEN，不声称密码学冻结、Wire 冻结、Provider exactly-once、实现/一致性通过、生产激活、多 PolicyDomain、Global Forget 或物理 Forget。
