# Phase 3.7 — H Lifecycle Handoff Envelope Semantics (Not Frozen)

- Owner: H — BMCP Protocol
- Status: Semantic handoff proposal only; wire schema NOT FROZEN
- Issue: #21
- English and Chinese are normative peers.

## 1. Protocol authority (EN)
H authenticates and transports typed messages/evidence. H does not mint, upgrade, interpret as its own or substitute D registration/fence/lineage, I authorization, Storage transaction/visibility, F retrieval completeness, G Context/Applied or C provider-submit evidence. An ACK proves only its explicitly declared receipt boundary.

Each handoff identifies, as applicable: registered message type; separately versioned payload schema/profile; authenticated sender/issuer and recipient/audience; purpose, Scope and Environment; correlation/causation; stable logical idempotency identity and canonical payload digest; exact owner-issued evidence references and their issuers; capability/security profile and replay-protection context. Exact field names, serialization, canonical bytes, signature suite, key rotation/revocation, audience syntax and compatibility are deliberately not frozen.

Protocol version, payload schema version, E DerivationRun/input digest, F IndexWatermark/Working Set generation, G ContextVersion/DeliveryAttempt/Applied, I PermissionEpoch, D ForgetFence/ProducerRegistration/ParticipantIntentRef, Storage DB incarnation/XID/visibility and C FinalRequestBoundary remain distinct nominal types. Generic version/generation/epoch/cursor fields must not erase authority identity.

Same logical idempotency identity plus same canonical digest is idempotent; same identity with different digest is conflict. Attempt/lease/delivery-attempt identities rotate separately. Unknown critical types/fields/enums, duplicate keys, invalid canonical payload, wrong audience, stale/revoked signer, unsupported security profile, replay outside policy or unknown owner evidence fail closed.

A restore manifest may reference independent Storage, COC, I, D and E/F/G proofs. H transports them unchanged; it cannot synthesize global restore high-water, compare authority-local positions or convert transport receipt into proof validity. G Delivery, H Delivered/Materialized and C FinalRequestSubmitted are distinct. G owns Applied; C owns provider submission/execution evidence; D owns ParticipantIntentRef; I owns current authorization.

A future wire freeze requires a separate exact-version artifact defining canonicalization, signatures, issuer/audience, replay/downgrade, key revocation, unknown-field policy, idempotency conflicts and positive/negative interoperability vectors. This proposal freezes no schema and claims no conformance.

## 2. 中文规范
H 负责认证并传输类型化消息与证据。H 不签发、不升级、不自行解释或替代 D Registration/Fence/Lineage、I Authorization、Storage Transaction/Visibility、F Retrieval Completeness、G Context/Applied 或 C Provider Submit 证据。ACK 仅证明其明确声明的接收边界。

每次交接必须按需标明已注册 Message Type、独立版本化 Payload Schema/Profile、经认证 Sender/Issuer 与 Recipient/Audience、Purpose/Scope/Environment、Correlation/Causation、稳定逻辑 Idempotency Identity 与规范 Payload Digest、Owner 签发的精确证据引用及其签发者、Capability/Security Profile 和 Replay Protection 上下文。字段名、序列化、规范字节、签名套件、密钥轮换/撤销、Audience 语法和兼容规则均不在本提案冻结范围。

Protocol Version、Payload Schema Version、E DerivationRun/Input Digest、F IndexWatermark/Working Set Generation、G ContextVersion/DeliveryAttempt/Applied、I PermissionEpoch、D ForgetFence/ProducerRegistration/ParticipantIntentRef、Storage DB Incarnation/XID/Visibility 和 C FinalRequestBoundary 必须保持不同名义类型。不得用通用 version/generation/epoch/cursor 抹去权威身份。

相同逻辑 Idempotency Identity 与相同规范摘要幂等；同身份不同摘要冲突。Attempt/Lease/DeliveryAttempt 身份分别轮换。未知关键类型/字段/枚举、重复键、规范 Payload 无效、Audience 错误、签名者陈旧/撤销、安全 Profile 不支持、超出策略的重放或 Owner 证据未知都必须 fail-closed。

Restore Manifest 可以引用 Storage、COC、I、D 和 E/F/G 独立证明。H 原样传输，不得合成 Global Restore High-water、比较权威域内位置或将 Transport Receipt 转成证明有效性。G Delivery、H Delivered/Materialized、C FinalRequestSubmitted 相互独立；G 管理 Applied，C 管理 Provider Submission/Execution 证据，D 管理 ParticipantIntentRef，I 管理当前授权。

未来 Wire Freeze 必须另行提交精确版本文件，定义 Canonicalization、Signature、Issuer/Audience、Replay/Downgrade、Key Revocation、Unknown-field 策略、Idempotency Conflict 和正/负互操作向量。本提案不冻结 Schema，也不声称符合性。
