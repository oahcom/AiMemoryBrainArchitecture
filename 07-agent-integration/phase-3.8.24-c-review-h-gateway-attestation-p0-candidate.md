# Phase 3.8.24 — C Exact Review: H Gateway Attestation P0 Candidate
# Phase 3.8.24 — C 精确复审：H Gateway Attestation P0 候选

- Owner perspective: C — Provider Outcome Semantic Authority
- H Phase 3.8.20 P0 candidate: Blob `05313c60c757cd736cb3ab127b330a5dce674dd1`
- CSubmitOutcome 1.0.1 schema: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C P0 signature projection: Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- C Phase 3.8.23 signer/attestation disposition: Blob `65aa82bac678e317325b1673121b92c04121b4f4`
- I Phase 3.8.19 trust model review: Blob `a698fb8d58181c9fc760be5a0a3901cc9817dcad`
- Status: **ACCEPT WITH C-OWNED SEMANTIC CONDITIONS; H P0 AND SCHEMA 1.2.15 NOT FROZEN**
- Provenance: delegated C-role exact review; not an independent human C Owner signature.
- English and Chinese are normative peers.

## 1. C disposition / C 侧结论

C accepts H Phase 3.8.20's proposed separation and P0 field groups as the correct candidate direction:
- CSubmitOutcome 1.0.1 remains independently signed under C-P0 by the C owner/adapter authority.
- H gateway signs a distinct envelope P0 after authenticating the original C adapter at ingress.
- The H signature asserts gateway receipt/binding only; it never asserts provider outcome truth.
- C P0 and H P0 use separate domain separators, profile IDs, key namespaces and evidence references.

C 接受 H Phase 3.8.20 提出的分离方式与 P0 字段分组作为正确候选方向：
- CSubmitOutcome 1.0.1 仍由 C Owner/Adapter Authority 使用 C-P0 独立签名；
- H Gateway 在 Ingress 认证原始 C Adapter 后签署独立 Envelope P0；
- H Signature 仅证明 Gateway Receipt/Binding，永远不证明 Provider Outcome Truth；
- C P0 与 H P0 使用独立 Domain Separator、Profile ID、Key Namespace 与 Evidence Ref。

## 2. C-owned field and evidence conditions / C 自有字段与证据条件

1. H P0 MUST include the exact C object ref and digest and every duplicated Provider Outcome wire field. The receiver must dereference the immutable C object and compare every duplicated field exactly before any C semantic conclusion.
2. H P0 MUST include the C object signature evidence reference (`owner_signature_ref`) and bind it to the exact C record ref/digest. H gateway receipt cannot replace C object signature verification.
3. `origin_received_bytes_digest` must be the digest of the exact raw bytes received from the authenticated C adapter before parsing, normalization, decompression or field rewriting. The H gateway must retain or durably reference those bytes for forensic/replay verification under retention policy.
4. `origin_transport_context_ref/digest` must bind the authenticated C adapter identity and session/channel evidence. The C adapter identity in that receipt must match the C object `AdapterRef` under an explicit C/I registry mapping; do not infer this from a matching string.
5. The H P0 must not copy mutable provider response data into new fields and reinterpret it. All provider-side-effect facts remain in the immutable C object and C evidence references.
6. H attestation issuance must be downstream of successful C object schema, digest and signature verification. A gateway must not sign a malformed, digest-mismatched or unauthenticated C object merely because the transport connection was authenticated.
7. A C object that is UNKNOWN/IN_DOUBT remains UNKNOWN after H attestation; H receipt cannot terminalize C attempt or grant retry permission.

1. H P0 必须包含精确 C Object Ref/Digest 与每个重复 Provider Outcome Wire Field。接收方必须解引用不可变 C Object，并在作出 C Semantic 结论前逐字段精确比较。
2. H P0 必须包含 C Object Signature Evidence Ref（`owner_signature_ref`），并绑定精确 C Record Ref/Digest。H Gateway Receipt 不能替代 C Object Signature 验证。
3. `origin_received_bytes_digest` 必须针对认证 C Adapter 发送的原始字节，在 Parse/Normalize/Decompress/Field Rewrite 前计算。H Gateway 必须按保留策略保存或持久引用这些字节，以供取证/Replay 验证。
4. `origin_transport_context_ref/digest` 必须绑定认证 C Adapter Identity 与 Session/Channel Evidence。Receipt 中 C Adapter Identity 必须通过显式 C/I Registry Mapping 与 C Object `AdapterRef` 匹配，不得仅凭字符串相等推断。
5. H P0 不得复制可变 Provider Response Data 并赋予新语义。所有 Provider Side-Effect 事实仍属于不可变 C Object 与 C Evidence Ref。
6. H Attestation 必须在 C Object Schema、Digest、Signature 验证成功后签发。不能仅因 Transport Connection 已认证，就为格式错误、Digest 不匹配或未认证的 C Object 签名。
7. C Object 为 UNKNOWN/IN_DOUBT 时，H Attestation 后仍是 UNKNOWN；H Receipt 不能终结 C Attempt 或授予 Retry Permission。

## 3. Clarifications required in H successor / H 后继版本必须澄清

- The proposed P0 says `integrity_proof_ref` is excluded to avoid a cycle. H must define the referenced integrity evidence record schema and bind its digest/ref to the same P0 digest, signature, profile, key version and signing sequence. The reference cannot be an unverified mutable pointer.
- The proposed P0 includes `created_at` and `signing_record_sequence`; sequence is authoritative for ordering/key status. Timestamp is informational and must never replace sequence ordering.
- The H schema must make `signature_profile_id` conditionally REQUIRED for gateway-attested C Provider Outcome messages, not merely optional.
- The 1.2.15 schema must explicitly distinguish the original C→H ingress channel proof from the H gateway's downstream channel binding. One reference cannot ambiguously represent both.
- H must define whether `origin_transport_context_ref` is a single immutable receipt or a composite of issuer authentication, channel binding, session identity and raw-byte digest. Partial or paginated evidence returns UNKNOWN.
- H gateway signing must occur only after C object signature verification and before durable acceptance. The exact crash/recovery state machine must prevent signing the same ingress under multiple message IDs or publishing multiple receipts.

- 拟议 P0 将 `integrity_proof_ref` 排除以避免循环。H 必须定义其引用的 Integrity Evidence Record Schema，并将其 Digest/Ref 绑定到同一 P0 Digest、Signature、Profile、Key Version 与 Signing Sequence。该 Ref 不能是未经验证的可变指针。
- P0 包含 `created_at` 与 `signing_record_sequence`；Sequence 才是权威排序/Key Status 依据。Timestamp 仅供参考，不能替代 Sequence。
- H Schema 必须对 Gateway-Attested C Provider Outcome Message 将 `signature_profile_id` 条件性设为 REQUIRED，不能仅保持 Optional。
- 1.2.15 Schema 必须明确区分原始 C→H Ingress Channel Proof 与 H Gateway 下游 Channel Binding；一个 Ref 不得模糊代表两者。
- H 必须定义 `origin_transport_context_ref` 是单一不可变 Receipt，还是由 Issuer Auth、Channel Binding、Session Identity、Raw-Byte Digest 组成的 Composite。部分/分页不完整的证据为 UNKNOWN。
- H Gateway 只能在 C Object Signature 验证后、Durable Acceptance 前签名。精确 Crash/Recovery State Machine 必须防止同一 Ingress 被多个 Message ID 签署或发布多个 Receipt。

## 4. C final disposition / C 最终结论

**Delegated C-role decision: ACCEPT the H Phase 3.8.20 P0 field architecture as a candidate with the above C-owned semantic conditions. H schema 1.2.15 and P0 remain unfrozen; I registration, H key custody, exact integrity-proof record and executable cross-language vectors remain required. C provider truth and C-P0 authority remain separate.**

**角色模拟 C 侧决议：接受 H Phase 3.8.20 P0 字段架构作为候选，但必须满足上述 C 自有语义条件。H Schema 1.2.15 与 P0 仍不冻结；仍需 I 注册、H Key Custody、精确 Integrity-Proof Record 与可执行跨语言向量。C Provider Truth 与 C-P0 权威继续独立。**

---
**Provenance:** delegated C-role exact review authored in the coordinating session; not an independent human C Owner signature or provider certification.
