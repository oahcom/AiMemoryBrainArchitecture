# Phase 3.6.18 — Storage v3.2.8 Successor: Outer Envelope Authentication Exact Bundle
# Phase 3.6.18 — Storage v3.2.8 后继：外层 Envelope Authentication 精确 Bundle

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **C/H/I OUTER-ENVELOPE ARCHITECTURE CANDIDATE BOUND; AUTHENTICATION IMPLEMENTATION / STORAGE INGRESS NOT VERIFIED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor exact bundle: Storage v3.2.7, Blob `f7a3acc1845f4322b2b38264eb0d4bae92623bac`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; not an independent human Storage Owner signature.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

Storage v3.2.8 succeeds v3.2.7 only for exact architecture-bundle binding. It adds the outer BMCP envelope authentication boundary for `C_PROVIDER_OUTCOME_RECORDED`, binds the corrected C origin-signer/P0 candidate, H exact JSON-Pointer mapping, I trust-governance review, and records the C/H/I/A delegated reviews. It does not modify the normative Storage technical body, COC protocol or any production implementation.

Storage v3.2.8 仅作为精确架构 Bundle Binding 的 v3.2.7 后继。它新增 `C_PROVIDER_OUTCOME_RECORDED` 外层 BMCP Envelope Authentication 边界，绑定修正后的 C Origin-Signer/P0 Candidate、H 精确 JSON-Pointer Mapping、I Trust-Governance Review，并记录 C/H/I/A 委托角色复审。它不修改 Storage Normative Technical Body、COC Protocol 或任何生产实现。

## 2. Exact current candidate bundle / 当前精确候选 Bundle

| Authority | Artifact | Exact Blob / CI | Evidence ceiling |
|---|---|---|---|
| Storage | Normative Storage v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | architecture body only |
| Storage | COC companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | protocol design only |
| Storage | R1/R2 ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | design/fault matrix, not executed |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | immutable object wire schema |
| C | C sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C owner namespace contract |
| C | C object P0/profile candidate | `44641b4b01d721c47e08ae9380ffe645bb3ccda0` | candidate, not registered |
| C | C object exact projection | `06d9264124d85896ccd44ef7789d9af245d8255b` | candidate projection |
| C | Outer-envelope signer/P0 decision candidate, Phase 3.8.22 | `310e7e0073d3c32f594bc151f10c249c828ce30f` | C origin signer and separate outer P0; candidate only |
| C | Outer-envelope gap review, Phase 3.8.21 | `d9da97c25cab7d22041dd6e25acab164cde1f9c4` | C-role acceptance of separate gap; delegated |
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | exact current structural schema |
| H | Outer-envelope gap/owner contract, Phase 3.8.18 | `fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1` | gap and ownership analysis |
| H | Corrected exact P0 JSON-Pointer mapping, Phase 3.8.20 | `4ba7e1699215d02224f805a15484b1da2e40c03f` | maps exact common + C branch fields; architecture candidate |
| H | Provider Outcome validator | `eab961a08d41e871f38543b18ee60cf024977414` | local C object validation; does not authenticate outer envelope |
| H | Provider Outcome tests | `da1454ed985c84160c4cb6a0462df9d1225fab7f` | 42 tests at exact run below; envelope auth not tested |
| H | Full-path fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | test-only synthetic signatures and authority callbacks |
| H | Exact Provider Outcome CI | Run `44072037563`, commit `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`, job `134000402978` | SUCCESS; 42 tests, 0 failures; local C object path only |
| I | Trust-boundary review, Phase 3.8.18 | `b6d1ea45825a1c2090abfba42474814f02f073a3` | accepts separation candidate; no profile registration |
| I | Corrected C P0 exact review, Phase 3.8.19 | `63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00` | binds corrected C proof-ref allowlist and H mapping; no crypto approval |
| A | Prior outer-envelope boundary review, Phase 3.8.19 | `e12cd7b5c79e2234178014243fd51f2e7d51272e` | reviews gap and authority separation; predates corrected C P0 and H mapping; NOT final review of v3.2.8 |

## 3. Outer-envelope candidate semantics / 外层 Envelope 候选语义

The current candidate architecture has two independently signed objects:
1. C immutable CSubmitOutcome object, signed under its separate C object P0/profile.
2. C-originated BMCP `C_PROVIDER_OUTCOME_RECORDED` envelope, signed by the C provider adapter under a separate outer-envelope P0/profile.

The H gateway cannot substitute its signature for C origin authentication. It may issue a separate H-originated ingress receipt after verifying C's message and protected transport. I owns trust registration, algorithm governance, key status/history, revocation, anti-rollback and authenticated principal policy. H owns exact wire mapping and verifier integration. Storage accepts durable ingress only after the complete authenticated-ingress predicate succeeds.

当前候选架构包含两个独立 Signed Object：
1. C 不可变 CSubmitOutcome Object，使用独立 C Object P0/Profile 签名。
2. C-originated BMCP `C_PROVIDER_OUTCOME_RECORDED` Envelope，由 C Provider Adapter 使用独立 Outer-Envelope P0/Profile 签名。

H Gateway 不得用自身 Signature 替代 C Origin Authentication。H 可在验证 C Message 与 Protected Transport 后签发独立 H-originated Ingress Receipt。I 拥有 Trust Registration、Algorithm Governance、Key Status/History、Revocation、Anti-rollback 与 Authenticated Principal Policy。H 拥有精确 Wire Mapping 与 Verifier Integration。Storage 仅在完整 Authenticated-Ingress Predicate 成功后持久接受。

## 4. Critical correction / 关键修正

The C Phase 3.8.22 candidate was corrected after H identified an omission: `integrity_proof_ref` and `channel_binding_proof_ref` are now explicitly in the outer-envelope P0 allowlist. H Phase 3.8.20 maps them to exact JSON Pointers. Both locators are signed and their referenced evidence remains independently verified. The corrected C Blob and H mapping Blob above supersede the earlier C Blob `6347c9...` and H preliminary review `2a3a995...`.

H 在发现 C Phase 3.8.22 漏项后完成修正：`integrity_proof_ref` 与 `channel_binding_proof_ref` 已明确纳入 Outer-Envelope P0 Allowlist。H Phase 3.8.20 将其映射为精确 JSON Pointer。两个 Locator 均被签名，其引用 Evidence 仍需独立验证。上方修正后的 C Blob 与 H Mapping Blob 取代早期 C Blob `6347c9...` 与 H 初步 Review `2a3a995...`。

## 5. Storage durable-ingress contract / Storage Durable-Ingress 合同

Storage's acceptance boundary must be downstream of all of the following:
- strict raw JSON parse and exact H schema pin;
- C outer-envelope digest/signature validation under I-authorized profile and key status;
- protected transport principal and channel-binding verification;
- authoritative nonce/replay/idempotency check;
- independent C object digest/signature verification and H/C duplicate-field equality;
- I terminal proof, D clearance, Storage same-GID proof and COC proof verification where required;
- currentness checks and fail-closed tri-state result.

No message is durably marked accepted merely because its JSON Schema validates, a signature-shaped field is present, the C object signature is valid, or a gateway receipt exists. Missing/unavailable required authority returns UNKNOWN and prevents positive durable acceptance. Invalid signature/identity/replay/evidence mismatch returns INVALID.

Storage Acceptance Boundary 必须位于以下全部步骤之后：
- Strict Raw JSON Parse 与精确 H Schema Pin；
- 在 I-authorized Profile/Key Status 下验证 C Outer-Envelope Digest/Signature；
- Protected Transport Principal 与 Channel-Binding 验证；
- 权威 Nonce/Replay/Idempotency 检查；
- 独立 C Object Digest/Signature 验证与 H/C Duplicate-Field Equality；
- 在需要时验证 I Terminal Proof、D Clearance、Storage Same-GID Proof 与 COC Proof；
- Currentness Check 与 Fail-Closed Tri-State Result。

不得仅因 JSON Schema 验证通过、存在形态化 Signature Field、C Object Signature 有效或存在 Gateway Receipt，就将消息持久标记为 Accepted。必需 Authority 缺失/不可用返回 UNKNOWN 并阻止 Positive Durable Acceptance。Signature/Identity/Replay/Evidence Mismatch 已确认无效则返回 INVALID。

## 6. Evidence ceiling / 证据上限

- H CI run 44072037563: 42 local tests passed. It does not execute outer envelope signature verification, transport principal authentication, channel-binding validation, nonce replay ledger, production I trust registry or Storage durable ingress.
- C/I profile IDs and crypto primitives are candidate design values only; no profile registry or production key registration is evidenced.
- H Phase 3.8.20 is a schema-derived architecture mapping, not executable validator proof.
- No production adapter, Gateway, HSM/KMS, key custody, revocation service, anti-rollback anchor, replay store, COC quorum persistence or Storage same-GID deployment is proven.
- No distributed crash/failover/fault-injection test for authenticated ingress has run.

- H CI Run 44072037563：42 项本地测试通过；没有执行 Outer Envelope Signature Verification、Transport Principal Authentication、Channel-Binding Validation、Nonce Replay Ledger、Production I Trust Registry 或 Storage Durable Ingress。
- C/I Profile ID 与 Crypto Primitive 仅是候选设计值；没有 Profile Registry 或 Production Key Registration 证据。
- H Phase 3.8.20 是 Schema-derived Architecture Mapping，不是 Executable Validator Proof。
- 未证明 Production Adapter、Gateway、HSM/KMS、Key Custody、Revocation Service、Anti-rollback Anchor、Replay Store、COC Quorum Persistence 或 Storage Same-GID Deployment。
- 未运行 Authenticated Ingress 的 Distributed Crash/Failover/Fault-Injection Test。

## 7. Gate status / Gate 状态

- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local Gate linearization/release: **OPEN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C outer-envelope authentication: **ARCHITECTURE CANDIDATE / NOT IMPLEMENTED / NOT VERIFIED**.
- I C profile trust registration: **OPEN / NOT APPROVED**.
- Storage authenticated durable-ingress integration: **OPEN / NOT IMPLEMENTED**.
- Production activation/provider egress: **NOT AUTHORIZED**.

## 8. Required next steps / 后续步骤

1. C independent Owner must approve the corrected outer signer/P0 candidate and maintain C object vs envelope P0 separation.
2. I must issue a formal exact-version crypto governance decision and profile/key registration, including trust/key history/revocation/anti-rollback.
3. H must implement strict parser, exact P0 extraction, digest/signature, channel-binding, protected principal, replay and full VALID/INVALID/UNKNOWN tests.
4. Storage must implement durable authenticated-ingress and replay/idempotency acceptance boundary, including crash/retry behavior.
5. A must issue a fresh exact-version integration review against this v3.2.8 bundle after C/H/I/Storage decisions and implementation evidence.
6. Gate A/B/C and JF-10/R1/R2 must remain at their current states until their separate closure predicates are met.

1. C Independent Owner 必须批准修正后的 Outer Signer/P0 Candidate，并保持 C Object 与 Envelope P0 分离。
2. I 必须发布正式精确版本 Crypto Governance Decision 与 Profile/Key Registration，包括 Trust/Key History/Revocation/Anti-rollback。
3. H 必须实现 Strict Parser、Exact P0 Extraction、Digest/Signature、Channel-Binding、Protected Principal、Replay 与完整 VALID/INVALID/UNKNOWN Test。
4. Storage 必须实现 Durable Authenticated-Ingress 与 Replay/Idempotency Acceptance Boundary，包括 Crash/Retry 行为。
5. 在 C/H/I/Storage 决策与实现证据完成后，A 必须针对本 v3.2.8 Bundle 发布全新精确版本 Integration Review。
6. 在各自 Closure Predicate 满足前，Gate A/B/C 与 JF-10/R1/R2 保持当前状态。

---
**Disposition:** exact architecture bundle candidate bound; not jointly accepted, not protocol frozen, not production authorized.
