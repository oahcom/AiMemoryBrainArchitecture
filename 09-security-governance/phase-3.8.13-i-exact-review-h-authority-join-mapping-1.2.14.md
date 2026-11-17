# Phase 3.8.13 — I Exact Review: H Authority-Join Mapping 1.2.14 / RecoveryJoin 1.0.2
# Phase 3.8.13 — I 精确复审：H Authority-Join Mapping 1.2.14 / RecoveryJoin 1.0.2

- Owner: I — Security, Identity and Governance
- Status: **ACCEPT I TERMINAL-PROOF CARRIER / P0 COMPATIBILITY AS L1/L2 CANDIDATE; TRUST/L3/PRODUCTION OPEN**
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H authority-join mapping Blob: `1cbe74eba69325510d6b1019d971661f965eabf8`
- H RecoveryJoin 1.0.2 Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`
- I P0 allowlist successor Blob: `44986f5f864bcdc1a79d34978273644d381a68c0`
- I owner snapshot membership proof contract Blob: `88209bbea0ab600880c5c630cfe83af31ee16dd7`
- H validator Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H test Blob: `53774aca0224fd9a727dfa625ba142825f1754b0`
- H callback-seam CI: run `44068247661`, tested commit `0701b12c3f43e1e6d5706c8eb2747e1c583d60b7`, SUCCESS, 25 tests.
- Provenance: delegated I-role review; **not an independent human I Owner or governance approval**.
- English and Chinese are normative peers.

## 1. Exact I carrier and P0 / I Carrier 与 P0 精确绑定

I accepts H Unified 1.2.14 / RecoveryJoin 1.0.2 as structural carriers for I-owned protected evidence. The exact I P0 includes `schema_artifact_revision=1.2.14` as a signed field distinct from wire `schema_version=1.3.0`. I's owner-specific high-water vector and I proof families remain I-owned; the D-only ForgetFenceGeneration high-water is not an I field and must not be compared with I PermissionEpoch, InventoryEpoch, receipt issue/consume positions or PolicyDomain sequence values.

I 接受 H Unified 1.2.14 / RecoveryJoin 1.0.2 作为 I 自有保护证据的结构载体。I P0 将 `schema_artifact_revision=1.2.14` 纳入签名，并与 Wire `schema_version=1.3.0` 区分。I 专属 High-Water 与 Proof Family 仍由 I 拥有；D-only ForgetFenceGeneration 不属于 I，不得与 I PermissionEpoch、InventoryEpoch、Receipt Issue/Consume 或 PolicyDomain Sequence 比较。

## 2. I terminal callback boundary / I Terminal 回调边界

H's separate `verify_i_terminal_decision` callback is an appropriate orchestration seam, but it must resolve and authenticate the exact I-signed terminal proof/authorization receipt and bind it to the exact operation, participant, policy domain, admission, scope generation, I ledger entry and final I GateGeneration. It must verify whether the terminal result is the required `COMMIT_WON` for the operation; a generic I terminal outcome is not automatically authorization to cross C provider egress.

H 的独立 `verify_i_terminal_decision` 回调是合理的编排接口，但必须解引用并认证精确 I 签名 Terminal Proof/Authorization Receipt，并绑定 Operation、Participant、PolicyDomain、Admission、Scope Generation、I Ledger Entry 与最终 I GateGeneration。必须判断该操作是否取得所需的 `COMMIT_WON`；任意 I Terminal Outcome 都不能自动授权 C Provider Egress。

I remains the sole authority for I ledger completeness, authorization, PermissionEpoch, key status, revocation/compromise ordering, historical verification, anti-rollback and I gate release. H/COC/Storage cannot mint I terminality or release I gates.

I 仍是 I Ledger Completeness、Authorization、PermissionEpoch、Key Status、Revocation/Compromise Ordering、Historical Verification、Anti-Rollback 与 I Gate Release 的唯一权威。H/COC/Storage 不能签发 I Terminality 或释放 I Gate。

## 3. Test ceiling / 测试证据上限

H run `44068247661` passed 25 tests on exact commit `0701b12c3f43e1e6d5706c8eb2747e1c583d60b7`. It demonstrates independent I/D/Storage callback slots and fail-closed UNKNOWN when missing. The orchestration tests mock schema validation, semantic validation and candidate digest/preimage calculation. They do not authenticate real I proofs, prove I ledger completeness, exercise production key status or demonstrate final I currentness CAS.

H Run `44068247661` 精确 Commit 上 25 项通过，证明 I/D/Storage 回调槽独立以及缺失回调时 fail-closed UNKNOWN。编排测试 Mock 了 Schema、语义及 Digest/Preimage 计算；未认证真实 I Proof、未证明 I Ledger 完整性、未执行生产 Key Status 或最终 I Currentness CAS。

## 4. Conditions retained / 保留条件

1. AIMBA-I-CRYPTO-1.0 remains an architecture candidate; production trust-root registration, HSM/KMS custody, key ceremonies and key lifecycle operations remain OPEN.
2. Per-family L3 P0/JCS/digest/signature-preimage vectors across two independent implementations remain OPEN.
3. External anti-rollback and historical verification remain OPEN.
4. H's I callback remains an interface/test seam until connected to I-authoritative stores and currentness sources; missing/unavailable evidence must return UNKNOWN.
5. I36-GOV-01..10 remain GOVERNANCE-BLOCKED; no Multi-PolicyDomain, Global Forget completeness, physical erasure or production activation is authorized.
6. The C profile is C-owned; I controls trust registration/status within I's authority, not C's semantic profile definition.

## 5. I disposition / I 侧结论

**Delegated I-role decision: ACCEPT H mapping Blob `1cbe74...`, H Unified 1.2.14 and RecoveryJoin 1.0.2 as an L1/L2 structural candidate for I proof transport, provided the exact I terminal proof callback enforces the predicates above. TRUST/L3/PRODUCTION remain OPEN.**

This is not an independent human I Owner signature or formal governance approval.

**角色模拟 I 侧决议：接受 H Mapping Blob `1cbe74...`、H 1.2.14 与 RecoveryJoin 1.0.2 作为 I Proof 传输的 L1/L2 结构候选，但 I Terminal 回调必须执行上述谓词。Trust/L3/Production 继续 OPEN。** 本结论不是独立人类 I Owner 签名或正式治理批准。
