# Phase 3.8.27 — C Exact Re-review: H Gateway P0 Issuance and Durable Acceptance Order
# Phase 3.8.27 — C 精确复审：H Gateway P0 签发与 Durable Acceptance 顺序

- H P0 candidate updated: Phase 3.8.20, Blob `93b83ac35114d20d64579d919c0699886940f0fa`
- H schema 1.2.15: Blob `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H schema mapping: Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924`
- CSubmitOutcome 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C signer model: Phase 3.8.23, Blob `65aa82bac678e317325b1673121b92c04121b4f4`
- C schema review: Phase 3.8.26, Blob `78fd99c0ea4c90dc989eef19f079c8d18e2e1468`
- Status: **ACCEPT CORRECTED ORDER; C VERIFICATION MUST PRECEDE H SIGNING AND DURABLE INGRESS**
- Provenance: delegated C-role exact re-review; not an independent human C Owner signature.

## 1. C disposition / C 侧结论

C accepts the updated sequence:
1. H gateway authenticates the original C adapter and captures the exact raw ingress bytes/context.
2. H gateway validates the immutable CSubmitOutcome schema, C-P0 digest/signature, C sequence namespace, provider evidence and C semantics.
3. Only then may H create/sign the distinct H gateway-attestation P0.
4. The receiver independently validates the H attestation and C object.
5. Replay reservation and durable ingress acceptance occur only after both authentication domains and all required owner/currentness checks pass.

C 接受更新后的顺序：
1. H Gateway 认证原始 C Adapter，并捕获精确 Raw Ingress Bytes/Context；
2. H Gateway 验证不可变 CSubmitOutcome Schema、C-P0 Digest/Signature、C Sequence Namespace、Provider Evidence 与 C Semantics；
3. 只有完成 C 验证后，H 才能创建/签署独立 H Gateway-Attestation P0；
4. Receiver 独立验证 H Attestation 与 C Object；
5. 只有两个认证域与所有必需 Owner/Currentness 检查均通过后，才执行 Replay Reservation 与 Durable Ingress Acceptance。

## 2. Required fail-closed behavior / 必需 Fail-Closed 行为

- C object schema/digest/signature contradiction → INVALID; unavailable C verifier/key status → UNKNOWN; H must not sign.
- C provider outcome UNKNOWN/IN_DOUBT or unresolved side-effect status → H may retain an ingress receipt for audit, but cannot mark Provider Outcome VALID or terminal.
- H signature valid but C signature invalid/unavailable → no durable semantically-valid Provider Outcome acceptance.
- C signature valid but H gateway attestation invalid/unavailable → no authenticated H ingress acceptance.
- Replay reservation or durable ingress commit ambiguous → UNKNOWN; recover the same immutable message/reservation, never mint a new message ID to bypass it.

- C Object Schema/Digest/Signature 矛盾为 INVALID；C Verifier/Key Status 不可用为 UNKNOWN；H 不得签名；
- C Provider Outcome 为 UNKNOWN/IN_DOUBT 或 Side-Effect Status 未解决时，H 可为审计保留 Ingress Receipt，但不能标记 Provider Outcome VALID 或终态；
- H Signature 有效但 C Signature 无效/不可用，不得 Durable Accept 为语义有效 Provider Outcome；
- C Signature 有效但 H Gateway Attestation 无效/不可用，不得 Authenticated H Ingress Accept；
- Replay Reservation/Durable Ingress Commit 不明确为 UNKNOWN；必须恢复同一不可变 Message/Reservation，不得创建新 Message ID 绕过。

## 3. C disposition / C 侧最终结论

**Delegated C-role decision: ACCEPT the corrected issuance/receiver-validation/durable-acceptance order. The H P0 and schema remain candidates only; C production key/trust/provider adapter evidence remains OPEN. NOT FROZEN.**

**角色模拟 C 侧决议：接受修正后的 Issuance/Receiver Validation/Durable Acceptance 顺序。H P0 与 Schema 仍仅为候选；C 生产 Key/Trust/Provider Adapter 证据仍 OPEN。不冻结。**
