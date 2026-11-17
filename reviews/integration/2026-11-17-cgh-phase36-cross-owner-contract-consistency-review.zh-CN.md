# C/G/H 跨 Owner 契约一致性复审 — 当前基线修正版

- 日期：2026-11-17
- 复审：在读取独立精确版本 Owner 补充决议、H 当前 Full-Path 闭环和 C/G 当前复审后，对跨 Owner 审计作出修正。
- PR #28 仍为 Draft/Open。
- 本版本取代同路径此前报告。早期审计只读取 C/G/H 基础合同，遗漏独立精确版本 C 补充决议、H Schema/Mapping 决议及后续 Full-Path 工件，因此产生了错误的缺口判断。

## 1. 当前精确证据基线

| 权威方 | 工件 | 精确 Blob / 证据 |
|---|---|---|
| C 精确 CGH-APPLIED-1.1 recovery-batch 接受 | C Phase 3.6 C-submit / I / D 因果顺序补充合同 | 45a48249717c8cddb07ab96197730ef93d406c22 |
| C 规范 Provider Outcome 语义 | C Phase 3.8.4 Provider Submit Outcome 规范合同 | 819705037da89834e10b6dd2ec6e66c1b8c70886 |
| C 不可变对象 Schema | CSubmitOutcome 1.0.1 JSON Schema | a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda |
| C 当前 Full-Path 复审 | C Phase 3.8.19 对 H 38-test 闭环的复审 | 24337b79cfea6264a8a6f11fa414578fc559716c |
| H Wire Schema | Unified 1.2.14 / wire 1.3.0 | 09fcd1fa29fe24255fbd87cae79dafb406594a59 |
| H Authority-Join Mapping | H Phase 3.8.10 / integrated mapping | 579dd2a91edf47b86e744e897ba6668b839944bd / 1cbe74eba69325510d6b1019d971661f965eabf8 |
| H Full-Path Validator/Test/Fixture | Validator / Test / Fixture | eab961a08d41e871f38543b18ee60cf024977414 / 540056d7c4f290c31290b17c264c69cfd76b1cb2 / c80247a6ecfbb4a29ff0993e8e2aea4829d00626 |
| H Full-Path 闭环 | H Phase 3.8.14 | cda025fb157815570b3280fa5ff168d5e62453b1 |
| H 精确 CI | Run / commit / job | 44070924346 / 77a9d5e2e716ba33387f0beb1195f864ed8ac54f / 133996627914 SUCCESS |
| G 当前消费者复审 | G Phase 3.8.18 委托角色复审 | 1894860c76336f8739d354b72beed3992cffd17e |
| G Applied 源文件 | G Phase 3.6 Applied / Forget 合同 | aa3afa73d8a76cc6f025839c52bfbff6a983046a |

辅助候选 Schema 包括 H RecoveryCutoff 1.0.5（Blob 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7）和 RecoveryJoin 1.0.2（Blob 4b664e3bce465499bcdfd93796349a4ba7074002）。它们属于独立 Schema 家族，不替代 H Unified 1.2.14 或 CSubmitOutcome 1.0.1。

## 2. 修正后的总体结论

**C/G/H 设计级消费者映射：在委托 L1/L2 层面已 ACCEPT WITH ENUMERATED CONDITIONS；NOT FROZEN。**

此前关于 C 没有精确 1.1 recovery-batch 决议、没有 CSubmitOutcome 对象合同的 P1 判断是错误的。C 已在独立 Owner 补充工件中，对精确 A/COC recovery-batch pair 作出 ACCEPT WITH ENUMERATED EXCEPTIONS；C 的规范 Provider Outcome 合同和 1.0.1 Schema 已定义 C 自有不可变 Provider Outcome。C 明确保留 Provider 专属 same-key 幂等和 crash recovery 作为未验证条件。

此前关于 H 没有具体 Schema 的判断也过于宽泛。H 已有 Unified 1.2.14 / wire 1.3.0、精确 C Object Mapping、完整本地 H Envelope + C Object Validator 路径，以及文档派生的 JSON Schema 候选。H 当前 Full-Path Run 报告 38 个方法：32 个 H Validator Unit/Fixture 方法，以及 6 个 C Crypto Interop 方法；精确 Provider Outcome Job 在固定 Commit 上通过。

G 也已针对精确 CSubmitOutcome 1.0.1 × H Unified 1.2.14 映射发布委托 G 角色消费者复审，保留 G 对 Applied 的独占权威，并明确 Outcome × SideEffectStatus 映射。但这不是独立人类 G Owner 签字。

## 3. 跨 Owner 语义检查

| 主题 | 当前结果 | 边界 |
|---|---|---|
| C Provider Outcome 与 SideEffect 语义 | 合同/Schema 层 PASS | C 拥有不可变 Outcome；Outcome 与 SideEffectStatus 分离 |
| H Wire Mapping 与本地 Full-Path Validator | L1/L2 候选层 PASS | 精确 Schema/Object Join/Digest/负向篡改已本地测试 |
| G Applied 消费 | 委托复审 ACCEPT WITH G 自有条件 | 只有 G 决定 Full Applied 和 current-use projection |
| I/D/Storage/COC 权威分离 | 接口架构 PASS | 测试 Callback 不是生产权威验证 |
| 历史 Applied 与 current-use | 合同层 PASS | 后续撤销/Fence 使当前使用失效，不改写有效历史 |
| Forget/late work/unknown ordering | 合同要求 fail closed | 未知或缺失 Proof 不得提升 Applied 或释放 Barrier |
| Execution Started/model use/completion | 独立证据族 | Provider 接受不证明执行或模型注意 |

重要 Digest 区分：C RequestDigest 绑定完整不可变 Final Request；G Managed Region Digest/Inventory 绑定完整 Managed Memory Region；C Object Digest 和 H Envelope Payload Digest 又是独立范围。它们必须 Join 到同一个 Request，但不得混淆或假定相等。

## 4. 发现项 — 更新后的状态

### XCH-36-001 — C Producer 证据合同
**在 L1/L2 合同定义层面 CLOSED。** C 精确 recovery-batch 决议、规范 CSubmitOutcome 合同和 1.0.1 Schema 已固定。**Provider 专属 same-key lookup/幂等、crash/restart/failover 恢复及真实 Provider Issuer Truth 仍 OPEN。**

### XCH-36-002 — H Wire/Schema/Full-Path Mapping
**在 L1/L2 Schema/Validator 候选层面 CLOSED。** H Unified 1.2.14、CSubmitOutcome 1.0.1 Mapping 和 38-method Full-Path CI 已固定。**生产 Schema/IDL 生成、生产 Trust/Key Governance、实时 Authority Callback 和互操作/部署仍 OPEN。**

### XCH-36-003 — 精确版本 C/G/H 消费者接受
**在委托技术复审层面 CLOSED，但有明确限制。** C 和 H 的精确 Mapping 复审已存在；G Phase 3.8.18 在 G 权威范围内接受同一精确 C/H Mapping。**独立人类 Owner 签字和全局冻结尚未成立。**

### XCH-36-004 — 跨权威顺序与 Digest 命名空间
**在本次复审的设计层面 CLOSED。** COC、I、D、Storage、C Request、Managed Region 和 H Envelope Digest/Position 域保持独立；任何本地时钟、Receiver Sequence 或其他权威 Cursor 均不得替代所需 Owner Proof。保留精确版本绑定；不得跨权威比较或合并 opaque position。

### XCH-36-005 — Runtime 与生产证据
**OPEN。** L1/L2 本地 Full-Path 测试已通过，但正向 Fixture 的十个 Authority Callback 全部是确定性 Test Double。尚未证明生产 Trust Root、实时 C Sequencer/Key Status Ledger、Provider Truth/Same-Key Lookup、实时 I/D/Storage Proof Verification、COC Quorum Durability、Storage Same-GID 物理恢复、G Applied Persistence、多副本 Egress Serialization 或生产部署。G adversarial race/reconnect/replay/restore Suite 仍为 SPECIFIED / NOT RUN。

## 5. 剩余生产 Gate

1. I Governance Trust Root/Profile 注册、C Key Lifecycle、HSM/KMS 托管、Key Rotation/Revocation 和 Anti-Rollback。
2. Provider 专属权威 Idempotency 和 Same-Key Lookup，包括 Crash/Restart/Failover，以及不确定 Handoff 后禁止 Retry-as-New。
3. 实时 I/D/Storage Authority Verifier 与 Proof-Currentness Join；不得用 Test Double 替代。
4. 指定 COC Operator、Durable Quorum/Participant Registry、Outage Recovery、Restore 和 High-Water Proof。
5. 选定 Storage 拓扑及物理 Same-GID Prepared/Commit/Rollback、Visibility/Non-publication 和 Restore 保证。
6. G Applied Durable Persistence/Validator 实现和 L3/L4 Adversarial Conformance。
7. 独立人类 Owner/Governance 批准、共享 Release Manifest 和生产授权。
8. Multi-PolicyDomain Atomicity 仍 BLOCKED / NOT ACCEPTED。

## 6. 最终 Gate

- C/H L1/L2 本地 Full-Path Validation：**PASS**。
- G L1/L2 Consumer Review：**ACCEPT WITH ENUMERATED CONDITIONS（委托角色复审）**。
- C/G/H 全局 Applied Contract Frozen：**NO**。
- 生产 Authority Integration：**OPEN / NOT VERIFIED**。
- G Applied Runtime/Persistence：**NOT VERIFIED**。
- L3/L4 端到端 Conformance：**NOT RUN / OPEN**。
- 生产激活 / Provider Egress 授权：**NOT AUTHORIZED**。
- PR #28：**Draft/Open；未授权合并**。

本修正版不声称全局 Forget 完成、物理擦除、Provider Exactly-once、模型注意或生产就绪。
