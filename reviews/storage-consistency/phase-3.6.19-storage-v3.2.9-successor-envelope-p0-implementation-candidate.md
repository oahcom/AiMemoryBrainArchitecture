# Phase 3.6.19 — Storage v3.2.9 Successor: Outer Envelope P0 Reference Implementation Candidate
# Phase 3.6.19 — Storage v3.2.9 后继：外层 Envelope P0 Reference Implementation Candidate

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **C/H/I ENVELOPE ARCHITECTURE + H P0/DIGEST SOURCE CANDIDATE BOUND; UPDATED CI NOT OBSERVED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor: Storage v3.2.8, Blob `3c9d84e54c745c77d9e3895b631d4e164828ea9b`
- Normative Storage technical body unchanged: v3.2.3 Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; not an independent human Storage Owner signature.
- English and Chinese are normative peers.

## 1. Scope / 范围

v3.2.9 supersedes v3.2.8 only as the exact candidate bundle manifest. It binds H's new reference P0/digest construction and C-origin principal enforcement, plus the exact 28-method outer-envelope test source. It does not claim CI success for those updated files. No Storage technical normative body or production behavior is changed.

v3.2.9 仅作为精确候选 Bundle Manifest 替代 v3.2.8。它绑定 H 新增的 Reference P0/Digest Construction 与 C-origin Principal Enforcement，以及精确 28-method Outer-Envelope Test Source。它不声称这些更新文件的 CI 已成功。未修改 Storage Technical Normative Body 或生产行为。

## 2. Exact bundle / 精确 Bundle

| Authority | Artifact | Exact Blob / evidence | Status / ceiling |
|---|---|---|---|
| Storage | Normative Storage v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | unchanged architecture body |
| Storage | COC companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | protocol design only |
| Storage | R1/R2 ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | design/fault matrix, not executed |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | immutable C object schema |
| C | C sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C-owned sequence namespace contract |
| C | C object P0/profile candidate | `44641b4b01d721c47e08ae9380ffe645bb3ccda0` | candidate, not registered |
| C | C object exact projection | `06d9264124d85896ccd44ef7789d9af245d8255b` | candidate projection |
| C | Outer-envelope signer/P0 candidate | `310e7e0073d3c32f594bc151f10c249c828ce30f` | C adapter origin signer; separate outer P0; candidate only |
| C | C outer-auth boundary review | `d9da97c25cab7d22041dd6e25acab164cde1f9c4` | delegated C-role review |
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | exact structural schema |
| H | Corrected C outer P0 JSON-Pointer mapping | `4ba7e1699215d02224f805a15484b1da2e40c03f` | exact schema-derived candidate mapping |
| H | Outer envelope auth reference validator | `571f69d326be51fd80acfe0c5a3f5f2dddce61f4` | computes P0 digest/preimage; signature/trust callbacks remain injected |
| H | Outer envelope auth test source | `e4639b8c7389aea59e09fce897afa3ea56e6e388` | 28 test methods; execution not yet observed |
| H | H P0 implementation closure note | `cbca0d3496285c672d0b27b388da850db5a9f8c3` | records exact source and CI pending |
| H | C object Provider Outcome validator | `b8cd692d261df7a31a0f65c3e003693e305f73a2` | local C object validation, separate from envelope |
| H | Previous 60-test CI | Run `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380` | valid for older exact source only; NOT evidence for current P0 code |
| I | C trust-boundary review | `b6d1ea45825a1c2090abfba42474814f02f073a3` | candidate separation accepted; no crypto approval |
| I | Corrected C P0 exact review | `63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00` | exact corrected C/H refs; no profile registration |
| A | v3.2.8 exact integration review | `621ca5e08f33dcd82f2f9a2e7ba0fd5ab023cec5` | predecessor review; stale for new H implementation source; fresh A review required |

## 3. H P0 implementation delta / H P0 实现增量

H now contains a local deterministic outer-envelope P0 extractor and digest/preimage constructor:
- exact C envelope profile ID `AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0`;
- exact JCS candidate `RFC8785-JCS-1.0`;
- domain-separated SHA-256 payload digest and Ed25519 preimage;
- signed inclusion of both integrity_proof_ref and channel_binding_proof_ref;
- exact allowlist with unknown/unclassified field rejection;
- explicit exclusion of coordinator-appended COC fields;
- recomputed digest must match before signature callback;
- preferred callback receives the exact signature preimage;
- protected transport authority_kind must be C for this C-originated message family.

H 当前包含本地确定性 Outer-Envelope P0 Extractor 与 Digest/Preimage Constructor：
- 精确 C Envelope Profile ID `AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0`；
- 精确 JCS Candidate `RFC8785-JCS-1.0`；
- Domain-separated SHA-256 Payload Digest 与 Ed25519 Preimage；
- Integrity/Channel-Binding 两个 Ref 均纳入签名；
- Exact Allowlist 与 Unknown/Unclassified Field 拒绝；
- 明确排除 Coordinator 后续追加 COC Field；
- Signature Callback 前必须匹配重算 Digest；
- Preferred Callback 接收精确 Signature Preimage；
- 此 C-originated Message Family 的 Protected Transport authority_kind 必须为 C。

## 4. Evidence ceiling / 证据上限

**Source-level candidate only.** The updated H test file contains 28 methods, but no CI run for the exact current H source was observed when this manifest was written. Combined commit status was empty and commit-workflow lookup returned no runs. Therefore the 28 methods are not counted as passed.

Even after CI passes, the implementation remains a reference integration gate:
- Ed25519 signature verification is injected, not implemented here;
- I profile registry, C signer/key registration, trust roots, key lifecycle, revocation/history and anti-rollback are not implemented;
- protected transport/channel-binding verifiers are callbacks;
- replay/idempotency authority is a callback, not durable storage;
- no Storage authenticated durable-ingress integration or crash/failover test;
- no production Gateway, HSM/KMS, COC quorum persistence or same-GID proof.

**仅源码候选。** 更新后的 H Test File 包含 28 个方法，但写入本 Manifest 时没有观察到精确当前 H Source 的 CI Run。Combined Commit Status 为空，Commit Workflow Lookup 没有返回 Run。因此这 28 个方法不计为通过。

即使 CI 通过，该实现仍是 Reference Integration Gate：
- Ed25519 Signature Verification 仍是注入 Callback，未在此实现；
- I Profile Registry、C Signer/Key Registration、Trust Root、Key Lifecycle、Revocation/History 与 Anti-rollback 未实现；
- Protected Transport/Channel-Binding Verifier 仍为 Callback；
- Replay/Idempotency Authority 是 Callback，不是 Durable Storage；
- 没有 Storage Authenticated Durable-Ingress Integration 或 Crash/Failover Test；
- 没有 Production Gateway、HSM/KMS、COC Quorum Persistence 或 Same-GID Proof。

## 5. Required next sequence / 后续顺序

1. Obtain exact-head H CI for the current validator/test blobs and inspect raw logs; if failure, fix before binding a pass.
2. C independent Owner must accept the corrected C outer signer/P0 and separate object/envelope signatures.
3. I must formally approve or reject the crypto suite/profile and register C signer/key trust policy.
4. H must implement actual signature verifier adapter, protected transport/channel binding and replay authority integration.
5. Storage must implement durable authenticated ingress/replay/idempotency and crash/retry/failover semantics.
6. A must re-review exact current source/CI and this successor bundle after Owner decisions.
7. No Gate changes until independent closure evidence satisfies each Gate predicate.

1. 获取当前 Validator/Test Blob 的精确 HEAD H CI 并检查 Raw Log；若失败先修复，不得绑定为通过。
2. C Independent Owner 必须接受修正后的 C Outer Signer/P0 与 Object/Envelope 双签名分离。
3. I 必须正式批准或拒绝 Crypto Suite/Profile，并注册 C Signer/Key Trust Policy。
4. H 必须实现真实 Signature Verifier Adapter、Protected Transport/Channel Binding 与 Replay Authority Integration。
5. Storage 必须实现 Durable Authenticated Ingress/Replay/Idempotency 与 Crash/Retry/Failover 语义。
6. 在 Owner 决策后，A 必须针对精确当前 Source/CI 与本 Successor Bundle 重新审查。
7. 各 Gate 的独立 Closure Evidence 满足前不得变更 Gate 状态。

## 6. Gate status / Gate 状态

- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local Gate linearization/release: **OPEN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- H outer-envelope P0/digest reference implementation: **SOURCE CANDIDATE / CI NOT OBSERVED**.
- C outer-envelope profile registration / I trust approval: **OPEN**.
- Storage durable authenticated ingress: **OPEN / NOT IMPLEMENTED**.
- Production activation/provider egress: **NOT AUTHORIZED**.

---
**Disposition:** exact source bundle bound with explicit CI-pending state; not jointly accepted, not frozen, not production authorized.
