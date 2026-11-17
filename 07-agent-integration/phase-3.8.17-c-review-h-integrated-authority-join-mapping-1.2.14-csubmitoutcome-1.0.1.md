# Phase 3.8.17 — C Review of H Integrated Authority-Join Mapping
# Phase 3.8.17 — C 对 H 集成 Authority-Join Mapping 的复审

- Owner perspective: C — Agent Integration / Provider Outcome Semantic Authority
- Exact H integrated mapping: Blob 1cbe74eba69325510d6b1019d971661f965eabf8
- Exact H Unified 1.2.14 schema: Blob 09fcd1fa29fe24255fbd87cae79dafb406594a59
- Exact CSubmitOutcome 1.0.1 schema: Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- Exact C sequence namespace amendment: Blob 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb
- Exact C RecoveryJoin P0 crosswalk: Blob df12af95e6859a389ba71eb1b7dba512b9feb8f6
- Exact D RecoveryJoin P0 crosswalk: Blob c4adf827dd62d44c43b8e871dec4835581508adf
- Exact I P0 allowlist: Blob 35e6843da8becbf3b152512a561b05cf5486819b
- Exact I compatibility review: commit 947553e77375a94671523931518e0d9673c4a766
- Exact H validator core/test: eab961a08d41e871f38543b18ee60cf024977414 / 53774aca0224fd9a727dfa625ba142825f1754b0
- H callback-seam CI: run 44068247661, tested commit 0701b12c3f43e1e6d5706c8eb2747e1c583d60b7, 25 tests passed
- Storage v3.2.7 candidate manifest: Blob 4435fc0340a4fce10751679a95f3b4c821bdae4d
- Decision: **ACCEPT C-OWNED SEMANTIC BOUNDARY AND EXACT C OBJECT MAPPING AS L1/L2 CANDIDATE; ENUMERATED CONDITIONS REMAIN; NOT FROZEN**
- Provenance: delegated C-role technical review; **not an independent human C Owner signature**
- English and Chinese are normative peers

## 1. Decision / 决议

C accepts H's integrated authority-join mapping as an L1/L2 candidate for carrying C Provider Outcome evidence alongside independent I terminal, D Forget clearance and Storage resolution proof seams.

This acceptance is limited to the C-owned semantic boundary and the exact CSubmitOutcome 1.0.1 object/wire mapping. It does not transfer C authority to H, I, D, Storage or COC. It does not approve provider invocation, production egress, provider exactly-once, or production trust.

C 接受 H 集成 Authority-Join Mapping 作为 L1/L2 候选，用于承载 C Provider Outcome 证据，并与独立 I Terminal、D Forget Clearance、Storage Resolution Proof 接口并存。本接受仅限 C 自有语义边界及 CSubmitOutcome 1.0.1 对象/Wire 精确映射，不将 C 权威转移给 H、I、D、Storage 或 COC；不批准 Provider Invocation、生产 Egress、Provider Exactly-Once 或生产信任。

## 2. C-owned invariant set / C 自有不变量

1. CSubmitOutcome 1.0.1 remains the sole immutable semantic source for C provider submission facts: provider/adapter identity, attempt, outcome, side-effect status, evidence, final request boundary, request digest, idempotency namespace/key, C admission and C owner-ledger sequence.
2. `sequence_namespace_ref` is required and signed. C alone owns the namespace and durable sequencer that orders `record_sequence` and authenticated CKeyStatusEvent `event_sequence`. H may compare authenticated values; it cannot create or advance C sequence state.
3. C ProviderAttempt, ProviderOutcome and CSubmitOutcome are distinct from H BMCP envelope identity, COC participant intent/reservation, D ForgetFence generation, I PolicyDomain position and Storage SerializationRevision/GID/XID.
4. C Provider Egress Gate and immutable CSubmitOutcome are independent evidence. Storage may require and validate them before visibility but cannot mint C provider truth or infer that an unknown provider outcome means no side effect.
5. `HANDOFF_REJECTED` is not proof of no side effect. `PROVEN_NONE` requires the applicable authoritative no-handoff proof; `POSSIBLE_OR_UNKNOWN` remains nonterminal/UNKNOWN.
6. Provider-specific idempotency, same-key lookup, adapter race/fault behavior and issuer truth remain C-owned proof obligations.

## 3. Integrated authority seams / 集成权威接口

C accepts the separation expressed by H mapping Blob 1cbe...:

| Seam | C review condition |
|---|---|
| C Provider Outcome | H dereferences exact CSubmitOutcome 1.0.1, validates schema identity/version/revision, recomputes C-P0 digest, checks exact duplicated fields and verifies C-owned signature/key status/provider evidence/owner ledger. |
| I terminal decision | Must be verified by I's authority. For provider invocation authorization, only the applicable I `COMMIT_WON` proof is sufficient; a different terminal decision cannot be substituted. |
| D Forget clearance | Must be verified by D's authority against exact ForgetFenceGeneration, affected lineage/barrier and final effect boundary. |
| Storage resolution | Must be verified by Storage against exact DB incarnation, GID/transaction identity, prepare attempt, participant ledger and same-GID terminal resolution/visibility. |
| COC join | Remains separate quorum/participant evidence; it cannot substitute for C Provider Outcome, I, D or Storage proof. |

No callback may be supplied by H itself as a self-asserted Owner decision. A True result requires the corresponding authority to authenticate the exact proof and currentness. Proven contradiction is INVALID; unavailable/missing proof, verifier, key status or currentness is UNKNOWN. C requires this fail-closed distinction to remain normative.

C 接受 H Mapping 对各权威接口的分离：H 解引用并验证 CSubmitOutcome 1.0.1；I、D、Storage 分别验证自身的 Terminal、Forget Clearance、Storage Resolution。Provider Invocation 授权必须有适用的 I `COMMIT_WON`；其他 I 终态不能替代。COC 仅提供独立 Quorum/Participant 证据，不能替代 C Provider Outcome、I、D 或 Storage 证明。任何 Callback 都不得由 H 自己伪造 Owner 决议。确定矛盾为 INVALID；Proof、Verifier、Key Status 或 Currentness 不可用则为 UNKNOWN。

## 4. H test evidence ceiling / H 测试证据上限

H callback-seam CI run 44068247661 passed 25 tests on the exact validator/test source pinned above. It exercises the actual `validate_provider_outcome` orchestration function and demonstrates separate I/D/Storage callback slots and UNKNOWN when callbacks are absent.

However, Storage v3.2.7 §3.1 explicitly records that the orchestration cases mock schema validation, semantic validation and candidate digest/preimage calculation. The run is not a full unmocked H envelope + CSubmitOutcome object validation, does not authenticate real I/D/Storage proof payloads, and does not connect production authority stores.

C therefore accepts the architecture of the separate seams, not an end-to-end proof result. A full unmocked positive fixture and negative mutation matrix remain required before L3 closure.

H Callback-Seam CI 44068247661 对精确 Validator/Test 源运行 25 项测试并全部通过。测试调用真实 `validate_provider_outcome` 编排函数，证明 I/D/Storage Callback 分离以及 Callback 缺失时返回 UNKNOWN。但 Storage v3.2.7 §3.1 明确记录：编排测试对 Schema 校验、语义校验和候选 Digest/Preimage 计算使用 Mock。它不是完整无 Mock 的 H Envelope + CSubmitOutcome 正向验证，不认证真实 I/D/Storage Proof Payload，也未连接生产权威存储。因此 C 接受的是分离接口的架构设计，而不是端到端证明已经通过。

## 5. Required negative vectors / 必需负向向量

1. C object schema identity/version/revision differs from 1.0.1 → INVALID.
2. `sequence_namespace_ref` differs from authenticated CKeyStatusEvent namespace → INVALID; key-status source unavailable → UNKNOWN.
3. `record_sequence` and `event_sequence` are not proven to share the same durable C sequencer → UNKNOWN/INVALID according to authoritative evidence.
4. Any duplicated H/C field differs, including C object digest, provider/adapter, request boundary, idempotency key, outcome, evidence, admission or C owner sequence → INVALID.
5. `HANDOFF_REJECTED` plus `PROVEN_NONE` without authoritative no-handoff proof → INVALID; `POSSIBLE_OR_UNKNOWN` cannot be coerced to `PROVEN_NONE`.
6. I terminal decision is missing or not the required `COMMIT_WON` for provider invocation → UNKNOWN or DENY; never infer authorization from C/COC proof.
7. D ForgetFenceGeneration is stale, incomplete or blocks the effect → DENY/UNKNOWN; H cannot issue D clearance.
8. Storage GID, DB incarnation, prepare attempt or same-GID terminal proof mismatch → INVALID; unavailable recovery evidence → UNKNOWN.
9. COC quorum proof is absent or stale → UNKNOWN; COC proof cannot replace any owner-specific callback.
10. Mutation of one authority proof must not change another authority's digest or acceptance state.

## 6. C disposition / C 侧结论

**C ACCEPTS H Integrated Authority-Join Mapping Blob 1cbe... as an L1/L2 candidate, subject to the exact pins and evidence ceilings above. NOT FROZEN.**

Still OPEN: same-manifest C/H/D/I/Storage adoption; unmocked end-to-end fixtures; production C profile registration/trust roots/key custody/anti-rollback; production C sequencer/key-status service; provider issuer truth; provider-specific idempotency and same-key lookup; live adapter race/fault tests; physical Storage and COC joins; independent human C Owner approval.

**C 接受 H Integrated Authority-Join Mapping Blob 1cbe... 作为 L1/L2 候选，受上述精确 Pin 与证据上限约束；不冻结。** 仍 OPEN：同一 Manifest 的 C/H/D/I/Storage 联合采纳；无 Mock 端到端 Fixture；生产 C Profile 注册/Trust Root/Key Custody/Anti-rollback；生产 C Sequencer/Key Status 服务；Provider Issuer Truth；Provider 专属幂等与 Same-Key Lookup；真实 Adapter Race/Fault；物理 Storage/COC Join；独立人类 C Owner 批准。
