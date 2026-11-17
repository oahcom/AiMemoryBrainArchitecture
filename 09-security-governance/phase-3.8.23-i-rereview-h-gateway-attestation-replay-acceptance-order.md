# Phase 3.8.23 — I Exact Re-review: H Gateway Attestation Replay and Durable Acceptance Order
# Phase 3.8.23 — I 精确复审：H Gateway Attestation Replay 与 Durable Acceptance 顺序

- H P0 candidate updated: Phase 3.8.20, Blob `93b83ac35114d20d64579d919c0699886940f0fa`
- H Unified 1.2.15 schema: Blob `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H gateway validator candidate: Blob `d16ca2e309e99984e26a5655e1fd0091b6d3b4da`
- C exact order review: Phase 3.8.27, Blob `71047cdb51139ca4080ac67f451e38a48698859d`
- I P0/schema reviews: Phase 3.8.21 Blob `6a8717930f8822033c047bd6384df2aacf630a4b`; Phase 3.8.22 Blob `d3d680dee795c0adf8af306ac549e4c3a21438ba`
- Status: **ACCEPT CORRECTED ORDER AS REFERENCE CONTRACT; PRODUCTION REPLAY / TRUST / AUTHORIZATION REMAIN OPEN**
- Provenance: delegated I-role exact re-review; not an independent human I Owner signature.

## 1. I disposition / I 侧结论

I accepts the revised order requiring:
- original C adapter transport authentication and immutable origin receipt capture;
- C object schema/digest/signature and C semantic verification before H gateway signing;
- independent receiver verification of H gateway P0 and C object;
- replay reservation and durable ingress commit only after all required authentication and owner/currentness checks.

I 接受修订后的顺序：先认证原始 C Adapter 并捕获不可变 Origin Receipt；H Gateway 签名前先验证 C Object Schema/Digest/Signature 与 C Semantic；Receiver 独立验证 H Gateway P0 与 C Object；所有必需 Authentication/Owner/Currentness 检查通过后才进行 Replay Reservation 与 Durable Ingress Commit。

## 2. Replay disclosure and state durability / Replay 披露与状态持久性

I requires the durable ingress implementation to:
1. atomically bind message ID, nonce, H P0 digest, C object ref/digest, H key/version/sequence, audience and origin context digest;
2. persist an immutable acceptance result or a recoverable pending state before acknowledging ingress;
3. recover the same reservation and message after crash; no second processing under a new message ID;
4. return SAME_DIGEST_REPLAY only after reading the original durable result and rechecking current I authorization/PermissionEpoch, key status, audience/scope and applicable D Forget fence;
5. return INVALID for same identity/nonce with changed P0 digest, and UNKNOWN for unavailable replay state or ambiguous commit;
6. avoid disclosing prior result references to callers whose current authorization is revoked or stale.

I 要求 Durable Ingress 实现：
1. 原子绑定 Message ID/Nonce、H P0 Digest、C Object Ref/Digest、H Key/Version/Sequence、Audience 与 Origin Context Digest；
2. ACK 前持久化不可变 Acceptance Result 或可恢复 Pending State；
3. 崩溃后恢复同一 Reservation/Message，不得以新 Message ID 二次处理；
4. 只有读回原始 Durable Result，并重新检查当前 I Authorization/PermissionEpoch、Key Status、Audience/Scope 与适用 D Forget Fence 后，才返回 SAME_DIGEST_REPLAY；
5. 相同 Identity/Nonce 但 P0 Digest 不同为 INVALID；Replay State 不可用或 Commit 不明确为 UNKNOWN；
6. 不得向当前授权已撤销/过期的调用方披露 Prior Result Ref。

## 3. I registration boundary / I 注册边界

This review does not register the H profile, trust root, issuer, key or replay store. All H key-status and trust-registry callbacks remain reference seams. Production I approval requires a separate exact immutable registry record, key lifecycle/custody, historical verification, revocation precedence and external anti-rollback checkpoint.

本复审不注册 H Profile、Trust Root、Issuer、Key 或 Replay Store。所有 H Key-Status/Trust-Registry Callback 仍为 Reference Seam。生产 I 批准必须另有精确不可变 Registry Record、Key Lifecycle/Custody、Historical Verification、Revocation 优先级与 External Anti-Rollback Checkpoint。

## 4. I disposition / I 侧最终结论

**Delegated I-role decision: ACCEPT the corrected H issuance and durable-acceptance order as a reference contract. H profile registration, key custody, production transport identity, replay store, current authorization recheck and anti-rollback remain OPEN. NOT FROZEN.**

**角色模拟 I 侧决议：接受修正后的 H Issuance 与 Durable-Acceptance 顺序作为 Reference Contract。H Profile 注册、Key Custody、Production Transport Identity、Replay Store、Current Authorization Recheck 与 Anti-Rollback 仍 OPEN。不冻结。**
