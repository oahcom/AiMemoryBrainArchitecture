# Phase 3.8.13 — C Exact Review of H Unified 1.2.13 × CSubmitOutcome 1.0.1 Mapping
# Phase 3.8.13 — C 对 H Unified 1.2.13 × CSubmitOutcome 1.0.1 Mapping 的精确复审

- Owner: C — Provider Outcome Semantic Authority
- Branch: `session-c-agent-integration-2026-11-16`
- Exact H Unified schema 1.2.13: Blob `8e7f6a6c9663388863db88548f9c37d0fdb1bd97`
- Exact CSubmitOutcome schema 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- Exact H mapping Phase 3.8.9: Blob `37e8c41a580a51df8aa0188d90dd6b1d798d69f0`
- H validator core: Blob `0449090a0367576b8b4ac20b1b46897facf9233d`
- H validator unit tests: Blob `78d3c58ec0d56a95ef78c41ffbad9b21eb797556`
- H independent C 1.0.1 crypto tests: Blob `5559fb7a612c8dd92345ceae3a6aa62f4faae41a`
- C sequence namespace amendment: Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`
- I sequence namespace review: Blob `0d78e5b2bfcf66cae6b757314cead84b9c942601`
- C key-status event schema: Blob `908b293eba337e9fa75864cea3704e28a1a8d82e`
- I key-status governance review: Blob `57d1b1ca616eaec6df1dee82ddaccc66519caca2`
- C key-status lifecycle contract: Blob `9339b168165a7a3dd34def5236ad61cfd3163418`
- H CI run: `44064634701`; job `133975007711`; tested commit `01a53d6caa3caed0151a7e7d60bf069a233784fb`; **21 tests, 21 passed**.
- Status: **ACCEPT AS L1/L2 PROTOCOL MAPPING CANDIDATE; NOT FROZEN / NOT PRODUCTION-AUTHORIZED**
- Provenance: delegated C-role review at user's direction; not an independent human C Owner signature.
- English and Chinese are normative peers.

## 1. Exact mapping decision / 精确映射决议

C has re-reviewed the exact H Phase 3.8.9 mapping Blob `37e8c41a580a51df8aa0188d90dd6b1d798d69f0` against the exact H 1.2.13 schema and immutable CSubmitOutcome 1.0.1 object schema.

**C accepts the H 1.2.13 → CSubmitOutcome 1.0.1 mapping as the current L1/L2 protocol candidate.**

The mapping correctly:
- binds H artifact revision 1.2.13 / wire family 1.3.0 to C object schema ID/version/artifact revision 1.0.1;
- binds H duplicated fields to exact C immutable fields and requires C object dereference;
- maps `c_submit_outcome_digest` to C `payload_digest` for exact recomputation/equality;
- removes the ambiguous legacy `participant_intent_ref` alias;
- uses one nullable `coc_participant_intent_ref` paired with reservation/absence semantics;
- requires signed `sequence_namespace_ref`;
- preserves C, H, I, D, Storage and COC proof authority separation.

C 已将 H Phase 3.8.9 Mapping 精确 Blob 与 H 1.2.13 Schema、CSubmitOutcome 1.0.1 不可变对象 Schema 进行复审。

**C 接受 H 1.2.13 → CSubmitOutcome 1.0.1 作为当前 L1/L2 协议候选。**

该映射正确绑定 H 1.2.13 / Wire 1.3.0 与 C 对象 1.0.1，要求 C 对象解引用及重复字段精确比较，令 H `c_submit_outcome_digest` 等于 C `payload_digest` 并重新计算，删除旧的歧义 Alias，使用单一 nullable COC Intent，强制签名 Sequence Namespace，并保留各 Owner 独立证明权威。

## 2. Outcome and side-effect semantics / Outcome 与副作用语义

C confirms the exact H mapping is consistent with C's two-dimensional result model:

| Outcome | SideEffectStatus | C disposition |
|---|---|---|
| HANDOFF_ACCEPTED | PROVEN_OCCURRED | Provider request + receipt + outcome evidence + reservation; accepted handoff fact only |
| HANDOFF_REJECTED | PROVEN_NONE | Provider request + outcome evidence + authoritative no-handoff proof; no-side-effect terminal |
| HANDOFF_REJECTED | POSSIBLE_OR_UNKNOWN | Nonterminal/blocking; never infer no handoff or safe retry |
| HANDOFF_REJECTED | PROVEN_OCCURRED | Preserve occurred-side-effect evidence and reconcile as occurred |
| NOT_INVOKED | PROVEN_NONE | Requires both ProviderNoHandoffProofRef and NotInvokedProofRef; provider receipt forbidden |
| UNKNOWN / IN_DOUBT | POSSIBLE_OR_UNKNOWN | Unknown reason required; same attempt/key/request; no retry-as-new |

A rejection label does not imply no side effect. The H validator correctly keeps `provider_no_handoff_proof_ref` conditional on C `SideEffectStatus=PROVEN_NONE`, rather than requiring it for every `HANDOFF_REJECTED`.

拒绝标签不代表没有副作用。H Validator 正确地将 `provider_no_handoff_proof_ref` 设为 C `SideEffectStatus=PROVEN_NONE` 时的条件要求，而不是对所有 `HANDOFF_REJECTED` 无条件要求。

## 3. Exact C object and signature projection / C 对象与签名投影

CSubmitOutcome 1.0.1 requires:
- immutable record identity, record sequence and signed sequence namespace;
- issuer authority/subject, audience, purpose, message ID/nonce;
- C admission/ledger/high-water/root and C Gate/GateCommit identity;
- one-use ProviderAttempt identity/generation;
- Provider, Account, Adapter, AdapterBuild, Endpoint, Region, API operation;
- IdempotencyNamespace/Key and ProviderCapability record/digest;
- immutable final request boundary/type/digest/content type/method;
- causal-order transaction;
- Outcome and SideEffectStatus;
- provider evidence issuer/type/ref/digest and conditional request/receipt/lookup/no-handoff/not-invoked/unknown refs;
- COC participant intent/reservation/absence semantics;
- prior/superseding/reconciliation observation links;
- owner signature reference, key ID/version and signature.

The schema has `additionalProperties=false`. C-P0 is every present schema-allowed member except `payload_digest` and `signature`. The signed `sequence_namespace_ref` is part of C-P0. H recomputes the C digest and compares every duplicated wire field. Unknown or unbound fields are rejected.

CSubmitOutcome 1.0.1 的 Schema `additionalProperties=false`。C-P0 是所有已出现且被 Schema 允许的字段，唯一排除 `payload_digest` 与 `signature`。签名 `sequence_namespace_ref` 必须进入 C-P0。H 必须重算 C Digest 并比较每个重复 Wire 字段；未知或未绑定字段必须拒绝。

## 4. Sequence namespace and key governance / Sequence Namespace 与 Key Governance

C accepts I's exact requirement:
- C `record_sequence` and CKeyStatusEvent `event_sequence` MUST be allocated in the same authenticated C authority sequence namespace;
- `sequence_namespace_ref` in CSubmitOutcome must equal the namespace in the authoritative CKeyStatusEvent ledger;
- wall-clock order, process-local counters or arrival order cannot substitute;
- unavailable/forked/stale C sequencer or anti-rollback checkpoint returns UNKNOWN and blocks provider egress.

Authority separation:
- C owns C data-key creation, C key-status event production and CSubmitOutcome signing use.
- I owns the governance trust root, governance signature profile approval, lifecycle policy, revocation/compromise rules and registration.
- H verifies I governance signatures, C data signatures, key status at the C signing sequence and anti-rollback.
- Storage pins exact immutable key-status ledger/checkpoint evidence but cannot issue C/I trust decisions.

Current candidate profile IDs:
- C data profile: `AIMBA-C-CRYPTO-1.0`.
- I governance profile for C key-status events: `AIMBA-I-KEY-GOVERNANCE-1.0`.
- I's own protected evidence profile `AIMBA-I-CRYPTO-1.0` remains a separate I data-plane profile.

Both C and I profile registrations remain NOT REGISTERED. This is a governance/trust activation gate, not a structural contradiction in the current protocol mapping.

## 5. Exact CI evidence / 精确 CI 证据

H run `44064634701` completed SUCCESS on exact tested commit `01a53d6caa3caed0151a7e7d60bf069a233784fb`. Job `133975007711` executed the H Provider Outcome conformance workflow:
- 15 H validator/semantic/schema tests;
- 3 independent Python/Node C 1.0.1 crypto interoperability tests;
- 3 additional Python/Node C crypto compatibility tests;
- **21 total tests, 21 passed, 0 failed**.

The logs explicitly show:
- strict duplicate JSON key rejection;
- invalid UTF-8 and non-finite number rejection;
- C profile/message-type domain-separated digest/preimage;
- C owner high-water validation;
- missing authority callbacks do not silently succeed;
- CKeyStatusEvent schema closure and governance-profile separation;
- CSubmitOutcome 1.0.1 sequence namespace requiredness;
- H Unified 1.2.13 exact loaded-schema pin and legacy 1.2.11 rejection;
- removal of ambiguous participant-intent alias;
- conditional HANDOFF_REJECTED / SideEffectStatus semantics;
- independent Node/Python Ed25519/JCS vector agreement and field-mutation rejection.

This is bounded reference-model/schema/crypto-vector evidence. It does not prove production I trust root, C key registry, C sequencer, anti-rollback service, provider evidence truth, live adapter race serialization, COC quorum, Storage durability or end-to-end owner joins.

H Run `44064634701` 在精确 Commit `01a53d6caa3caed0151a7e7d60bf069a233784fb` 上 SUCCESS，Job `133975007711` 共执行 **21 项测试，全部通过**。覆盖严格 JSON、UTF-8、NaN/Infinity、Profile/Message Domain Separation、Owner High-water、缺失 Authority Callback Fail-closed、CKeyStatusEvent、CSubmitOutcome 1.0.1 Namespace、H 1.2.13 精确 Schema、旧 Alias 拒绝、条件化 Rejected 语义以及 Python/Node Ed25519/JCS 向量一致性。

该结果仅为有限参考模型/Schema/密码学候选向量证据，不证明生产 I Trust Root、C Key Registry/Sequencer、Anti-rollback、Provider 证据真实性、Live Adapter 竞态、COC Quorum、Storage 持久性或端到端 Owner Join。

## 6. Remaining architecture and governance obligations / 剩余架构与治理义务

1. C provider evidence taxonomy and authoritative same-key lookup semantics remain provider-capability-specific. A provider without authoritative lookup cannot promise deterministic absence or exactly-once side effects.
2. C owner ledger inclusion/currentness and C AdmissionSnapshotMembershipProof must be joined to RecoveryJoin 1.0.2 for every represented C admission/attempt/outcome row.
3. I governance root/profile and C data profile remain unregistered. Their trust chain, key status, lifecycle and anti-rollback architecture are defined as candidates, but governance activation is not approved.
4. H authority callbacks are test seams. Missing production verifier remains UNKNOWN; no silent success.
5. C multi-replica egress gate and provider handoff linearization still require an abstract concurrency/failure reference model beyond schema vectors.
6. COC Batch/Manifest/RecoveryJoin, Storage JF-10 and D/I owner currentness must bind the exact same operation/participant tuple. No owner can infer another owner's terminal truth.
7. Full Applied remains G-owned and requires more than HANDOFF_ACCEPTED.

## 7. Final C disposition / C 最终结论

**ACCEPT H PHASE 3.8.9 MAPPING + H UNIFIED 1.2.13 + CSubmitOutcome 1.0.1 AS THE CURRENT L1/L2 PROTOCOL CANDIDATE. NOT FROZEN / NOT PRODUCTION-AUTHORIZED.**

The exact mapping and 21/21 H candidate CI close the identified 1.2.12→1.2.13 structural/semantic compatibility defects for this C outcome family. Profile registration, provider capability/truth, live adapter egress, RecoveryJoin owner-membership proof, COC/Storage/I/D cross-owner joins and production authorization remain open.

**接受 H Phase 3.8.9 Mapping + H Unified 1.2.13 + CSubmitOutcome 1.0.1 作为当前 L1/L2 协议候选；不冻结、不授权生产。** 精确映射和 H 21/21 候选 CI 已关闭本 C Outcome 分支的 1.2.12→1.2.13 结构/语义兼容缺陷。Profile 注册、Provider Capability/Truth、Live Adapter Egress、RecoveryJoin Owner Membership Proof、COC/Storage/I/D 跨 Owner Join 和生产授权仍 OPEN。

This is a delegated C-role technical review, not an independent human C Owner signature.
