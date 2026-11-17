# Phase 3.8.22 — I Exact Review: H Unified 1.2.15 Gateway-Attestation Schema
# Phase 3.8.22 — I 精确复审：H Unified 1.2.15 Gateway-Attestation Schema

- H schema 1.2.15 Blob: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H exact mapping Blob: `2dc30f193d9c4f4bdc05ca4c137103687db28924`
- H P0 candidate Blob: `a08bff1145dfeccac3e583e065055ca7dfdcb189`
- C signer/attestation decision Blob: `65aa82bac678e317325b1673121b92c04121b4f4`
- C schema review Blob: `78fd99c0ea4c90dc989eef19f079c8d18e2e1468`
- I P0 exact re-review Blob: `6a8717930f8822033c047bd6384df2aacf630a4b`
- Status: **ACCEPT SCHEMA SHAPE AS TRUST-CARRIER CANDIDATE; I REGISTRATION / H KEY STATUS / TRUST ROOT REMAIN OPEN**
- Provenance: delegated I-role exact review; not an independent human I Owner signature or formal registration.

## 1. I schema disposition / I Schema 结论

I accepts the H Unified 1.2.15 structural carrier changes as a candidate:
- immutable artifact revision 1.2.15, wire family 1.3.0;
- conditional H signature profile ID and H signing sequence namespace/record sequence;
- distinct origin C-to-H transport context, raw bytes digest, issuer/sender identity, authentication context and channel-binding proof;
- distinct H downstream channel binding;
- lowercase-hex SHA-256 digest fields;
- C owner authority preserved as C while H gateway issuer/sender is separately identified.

I 接受 H Unified 1.2.15 结构 Carrier 变更作为候选：
- 不可变 Artifact Revision 1.2.15，Wire Family 1.3.0；
- 条件性 H Signature Profile ID 与 H Signing Sequence Namespace/Record Sequence；
- 独立 Origin C-to-H Transport Context、Raw Bytes Digest、Issuer/Sender Identity、Authentication Context 与 Channel-Binding Proof；
- 独立 H 下游 Channel Binding；
- Lowercase-Hex SHA-256 Digest；
- C Owner Authority 保持为 C，H Gateway Issuer/Sender 独立标识。

## 2. I-owned security conditions / I 自有安全条件

1. The schema only carries profile/key/origin references. It does not authenticate them. The production verifier must resolve the exact profile and signer through an I-approved immutable registry.
2. `signing_sequence_namespace_ref` and `signing_record_sequence` must bind to a durable H signing sequencer and an authenticated H key-status event/history stream. The namespace cannot reuse C or I sequence namespaces.
3. I must approve the H issuer, authority kind, signer subject, allowed message family, audience, owner-authority delegation, key purpose, validity interval and revocation state.
4. Key status must be checked at signing sequence and current time, with compromise/revocation precedence, historical verification, anti-rollback checkpoint and restore/failover continuity.
5. `origin_transport_context_ref/digest` must refer to a verifier-produced immutable receipt. A payload-supplied ref/digest alone is not authentication.
6. The H integrity evidence record must be immutable and bind P0 digest, signature, profile, key version, issuer and sequence. The schema's `integrity_proof_ref` alone is not sufficient.
7. Unknown registry/key status/checkpoint/transport context returns UNKNOWN; authenticated mismatch returns INVALID. No fallback/downgrade.

1. Schema 仅承载 Profile/Key/Origin Ref，不认证它们。生产 Verifier 必须通过 I 批准的不可变 Registry 解析精确 Profile 与 Signer。
2. `signing_sequence_namespace_ref` 与 `signing_record_sequence` 必须绑定 Durable H Signing Sequencer 与认证 H Key-Status Event/History Stream。不得复用 C/I Sequence Namespace。
3. I 必须批准 H Issuer、Authority Kind、Signer Subject、Allowed Message Family、Audience、Owner-Authority Delegation、Key Purpose、Validity Interval 与 Revocation State。
4. Key Status 必须按 Signing Sequence 与当前时间检查，并执行 Compromise/Revocation 优先级、Historical Verification、Anti-Rollback Checkpoint 与 Restore/Failover Continuity。
5. `origin_transport_context_ref/digest` 必须引用 Verifier 生成的不可变 Receipt。Payload 自带 Ref/Digest 不构成认证。
6. H Integrity Evidence Record 必须不可变，并绑定 P0 Digest、Signature、Profile、Key Version、Issuer 与 Sequence。Schema 的 `integrity_proof_ref` 单独不足。
7. Registry/Key Status/Checkpoint/Transport Context 未知返回 UNKNOWN；认证后不匹配返回 INVALID。禁止回退/降级。

## 3. Registration boundary / 注册边界

This review does not register `AIMBA-H-GATEWAY-ATTEST-1.0`, approve JCS/SHA-256/Ed25519 for production H signing, approve a gateway trust root/key/custody, or authorize production ingress. The exact P0, schema and executable verifier must return for a separate I registration decision after C/H close the listed semantic and test conditions.

本复审不注册 `AIMBA-H-GATEWAY-ATTEST-1.0`，不批准生产 H Signing 使用 JCS/SHA-256/Ed25519，不批准 Gateway Trust Root/Key/Custody，也不授权生产 Ingress。C/H 关闭所列语义与测试条件后，精确 P0、Schema 与可执行 Verifier 必须另行返回 I 作注册决议。

## 4. I disposition / I 侧最终结论

**Delegated I-role decision: ACCEPT H Unified 1.2.15 as a structural trust-carrier candidate. All H profile registration, gateway issuer/key approval, key-status lifecycle, custody, anti-rollback and production verification remain OPEN. NOT FROZEN.**

**角色模拟 I 侧决议：接受 H Unified 1.2.15 作为结构 Trust-Carrier 候选。所有 H Profile 注册、Gateway Issuer/Key 批准、Key Status Lifecycle、Custody、Anti-Rollback 与生产验证仍 OPEN。不冻结。**
