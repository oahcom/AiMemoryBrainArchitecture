# Phase 3.8.21 — H Exact Schema Mapping: Unified 1.2.15 Gateway-Attested C Provider Outcome
# Phase 3.8.21 — H 精确 Schema 映射：Unified 1.2.15 Gateway-Attested C Provider Outcome

- Owner perspective: H — BMCP Protocol / Schema and Envelope Authentication
- H Unified schema 1.2.15 candidate Blob: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H Phase 3.8.20 P0 candidate Blob: `a08bff1145dfeccac3e583e065055ca7dfdcb189`
- C exact P0 review: Phase 3.8.25, Blob `6a5c5c63a12bdfd8ef23f76dcee9ae30ab40db6c`
- I exact P0 review: Phase 3.8.21, Blob `6a8717930f8822033c047bd6384df2aacf630a4b`
- H Unified predecessor 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- Status: **SCHEMA 1.2.15 CANDIDATE CREATED; EXACT C/I SCHEMA REVIEW REQUIRED; NO VALIDATOR/CI CLAIM YET; NOT FROZEN**
- Provenance: delegated H-role schema drafting; not an independent human H Owner signature or I registration.
- English and Chinese are normative peers.

## 1. Versioning / 版本纪律

H 1.2.15 is a new immutable schema artifact revision; H 1.2.14 remains unchanged and historical for messages already authored under that revision. Wire family remains `1.3.0`. The new `schema_artifact_revision` const and schema `$id` are both 1.2.15.

A receiver MUST select the exact schema from trusted receiver configuration, validate the artifact revision, and reject an envelope that claims 1.2.15 while being validated against 1.2.14 or vice versa. No silent schema upgrade/downgrade is allowed.

H 1.2.15 是新的不可变 Schema Artifact Revision；H 1.2.14 保持不变，作为按该 Revision 编写的历史消息 Schema。Wire Family 仍为 `1.3.0`。新的 `schema_artifact_revision` const 与 Schema `$id` 均为 1.2.15。

Receiver 必须从可信 Receiver Configuration 选择精确 Schema、验证 Artifact Revision，并拒绝将声称 1.2.15 的 Envelope 用 1.2.14 验证，或反之。禁止静默升级/降级。

## 2. New conditional fields / 新增条件字段

For `C_PROVIDER_OUTCOME_RECORDED`, schema 1.2.15 adds these common-envelope properties and conditionally requires all of them:
- `signature_profile_id`;
- `origin_transport_context_ref`;
- `origin_transport_context_digest`;
- `origin_received_bytes_digest`;
- `origin_issuer_ref`;
- `origin_sender_authority_ref`;
- `origin_sender_subject_ref`;
- `origin_authentication_context_ref`;
- `origin_channel_binding_proof_ref`;
- `origin_received_at`;
- `signing_sequence_namespace_ref`;
- `signing_record_sequence`.

The Provider Outcome branch also constrains `owner_authority` to `C`. The fields remain optional at the shared common-envelope level so unrelated message families do not inherit C-specific requirements. The conditional rule is applied only to the C Provider Outcome branch.

对 `C_PROVIDER_OUTCOME_RECORDED`，Schema 1.2.15 新增并条件性要求上述 12 个 Common-Envelope Property。Provider Outcome Branch 同时将 `owner_authority` 限定为 `C`。这些字段在共享 Common Envelope 层仍为 Optional，避免无关 Message Family 被强加 C 专属要求；Conditional Rule 仅应用于 C Provider Outcome Branch。

## 3. Type and digest rules / 类型与 Digest 规则

- `origin_transport_context_digest` and `origin_received_bytes_digest` reference the existing `sha256` definition: exactly 64 lowercase hexadecimal characters.
- `signing_record_sequence` is a decimal string matching `^(0|[1-9][0-9]*)$`; it is scoped only to `signing_sequence_namespace_ref`.
- `origin_received_at` is date-time syntax only; it is not a sequence or ordering authority.
- `signature_profile_id` is a separate signature-profile identifier and MUST NOT be inferred from `canonicalization_profile_id`.
- `channel_binding_proof_ref` remains the H gateway's downstream channel; `origin_channel_binding_proof_ref` is the original C-to-H ingress channel. They are distinct fields and distinct proofs.
- The C object `payload_digest` and H envelope `payload_digest` remain separate digest domains, even if both use SHA-256 lowercase hex.

`origin_transport_context_digest` 与 `origin_received_bytes_digest` 引用现有 `sha256` 定义，严格为 64 字符小写十六进制；`signing_record_sequence` 为十进制字符串，仅在自身 Namespace 内有序；`origin_received_at` 仅是 Date-Time，不是顺序权威；`signature_profile_id` 独立于 `canonicalization_profile_id`；H 下游 Channel 与原始 C→H Ingress Channel 分别使用两个独立 Proof Ref；C Object Payload Digest 与 H Envelope Payload Digest 是独立 Digest Domain，即使两者都使用 SHA-256 小写十六进制。

## 4. Required semantic validator behavior / Semantic Validator 必需行为

The JSON Schema is structural only. H validator 1.2.15 must additionally:
1. resolve the exact H gateway signer/profile from an I-approved registry;
2. verify `owner_authority=C` and the authorized H gateway-to-C owner delegation;
3. verify `origin_transport_context_ref/digest` against the verifier-produced ingress receipt and compare origin C adapter identity with C object `AdapterRef`;
4. verify `origin_received_bytes_digest` against retained raw ingress bytes;
5. verify H signing sequence namespace/record sequence against the H key-status registry and anti-rollback checkpoint;
6. recompute H P0 digest using lowercase-hex SHA-256 and verify the H signature;
7. verify C object digest/signature independently;
8. compare every duplicated H wire field to the immutable C object;
9. enforce replay/durable-ingress state machine and current authorization before prior-result disclosure;
10. return INVALID for proven contradictions and UNKNOWN for missing/unavailable registry, transport, key-status, replay or owner evidence.

JSON Schema 仅负责结构。H Validator 1.2.15 还必须执行 I Registry/Profile 解析、Owner Authority/Delegation、Origin Receipt/Digest 与 C AdapterRef 对账、Raw Bytes Digest、H Signing Sequence/Anti-Rollback、H P0 Digest/Signature、独立 C Object Digest/Signature、逐字段 Wire/Object Equality、Replay/Durable-Ingress 与 Prior-Result Authorization，并保持 INVALID/UNKNOWN 区分。

## 5. Schema review checklist / Schema 复审清单

C must confirm:
- the new origin fields do not transfer provider truth or C semantic authority to H;
- every C Provider Outcome duplicate remains exact and C object signature remains independently required;
- origin transport identity is compared to C AdapterRef under an explicit registry relation.

I must confirm:
- H profile/key/issuer registry ownership and sequence linkage;
- trust-root, key status/history, revocation and anti-rollback semantics;
- signer delegation and audience/subject/owner-authority relation.

H must then add schema/validator tests for:
- all new fields present and valid;
- each required field missing;
- invalid digest pattern, invalid sequence, invalid date-time;
- owner_authority not C;
- 1.2.14/1.2.15 revision mismatch;
- exact null/absent behavior;
- positive and negative P0 signature vectors.

C 必须确认新增 Origin 字段不转移 Provider Truth/C Semantic Authority，C 重复字段仍精确且 C Object Signature 独立必需，并通过显式 Registry Relation 对账 Origin Identity 与 C AdapterRef。I 必须确认 H Profile/Key/Issuer Registry、Sequence、Trust Root、Key Status/History、Revocation、Anti-Rollback 与 Signer Delegation。H 随后补齐 Schema/Validator 正负测试。

## 6. Disposition / 结论

**Delegated H-role disposition: publish schema 1.2.15 as an immutable candidate successor for cross-review only. Do not claim validator support, CI conformance, H profile registration, production signer trust or production ingress. NOT FROZEN.**

**角色模拟 H 侧结论：发布 Schema 1.2.15 作为不可变后继候选，仅供交叉复审。不声称 Validator 已支持、CI 符合性已通过、H Profile 已注册、生产 Signer 已可信或生产 Ingress 已启用。不冻结。**

---
**Provenance:** delegated H-role schema drafting in the coordinating session; not an independent human H Owner signature or I security registration.
