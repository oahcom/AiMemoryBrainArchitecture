# Phase 3.8.33 — H Unified 1.2.17 Owner Gate Release 语义参考验证
# Phase 3.8.33 — H Unified 1.2.17 Owner Gate Release Semantic Reference

- 日期：2026-11-18
- 精确测试 H 代码 Head：`f08dadd27b743b2a31fce859d6ed2c438438d1e1`
- H Owner 分支：`session-h-bmcp-protocol`
- Unified Schema 1.2.17 Blob：`1b8f44675f30919764481d33755c566ef5cf1ea8`
- Unified Schema 1.2.16 Blob：`91c4fd70cb1e1cff76d733baa180325bd2da84c1`
- 1.2.17 语义参考 Validator Blob：`60cd1b686eaa9ac364c69a708353fa0e5f635197`
- 1.2.17 语义测试 Blob：`24d3cf0730a138f25719cb1e29de28f833a00cdf`
- 1.2.16 实例测试 Blob：`e1667b0f9526884c56c311bf1bcf8af6af0b9477`
- 精确 H Recovery Cutoff Run [#44193331446](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44193331446)：SUCCESS；日志报告 **390 tests**，OK，22 项 skipped。
- 1.2.16 Schema 修正精确 Run [#44192602325](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44192602325)：SUCCESS；日志报告 356 tests，OK，22 项 skipped。

## 1. 修复 1.2.16 Owner Snapshot 实例缺陷

原 1.2.16 中 Owner=I 的条件要求旧字段 `inventory_epoch_ref`，而 I 专属封闭字段定义的是 `producer_domain_inventory_epoch_ref`。由于 `additionalProperties: false`，I Snapshot 实际无法满足 Schema。现已将条件修正为 `producer_domain_inventory_epoch_ref`。

专项测试现在验证真实 I、D、C Owner Snapshot 实例，并拒绝：
- 缺少 I ProducerDomainInventoryEpoch；
- 使用禁止的 I 旧字段别名；
- 缺少 D Dependency-closure Root；
- 缺少 C Provider Idempotency Namespace。

1.2.16 专项测试现为 16 项。完整 356 项 Run #44192602325 是该版本精确 Head 的历史验证。

## 2. 1.2.17 精确 Owner Gate Release 语义 Join

测试 Profile 语义 Validator 不再只比较 Release 与单条记录字段，还检查：

1. Release 的完整 Owner Snapshot 字段与输入 Owner Snapshot 完全一致。
2. Batch 的 `owner_snapshots` 中对应 Owner 项必须是同一份精确 Snapshot。
3. Manifest 的 `owner_snapshot_roots[owner]` 必须与该 Snapshot 的 Root Projection 完全一致，包含 Scope Generation、Owner Gate Generation、Request/Admission High-water、Ledger Root、Anti-rollback Anchor 和 Owner-specific High-water Digest。
4. Manifest 必须通过 `batch_record_ref`、`batch_position`、`batch_entry_digest` 回链到精确 Batch。
5. Batch 与 Manifest 必须共享 RecoveryEpoch、精确 Prefix、ManifestId、ManifestContentDigest、Enumeration High-water、Participant Counts 和 Member-set Root。
6. Batch 的 COC Position 必须早于 Manifest 的 COC Position。
7. Owner Signature、COC Commit Proof 和 Owner Currentness 仍是独立 Callback。Callback 异常/证据缺失返回 UNKNOWN；明确的签名/证明/当前性拒绝返回 INVALID。

1.2.17 语义测试共 34 项，覆盖 Pair Substitution、Owner Snapshot Substitution、顺序约束和 Callback Exception。精确完整 H 套件 Run #44193331446 通过 390 项（22 项 skipped）。

## 3. 证据边界 / 不作出的声明

这仍是 TEST Profile 参考 Validator：
- Signature Verification、COC Quorum Proof 和 Currentness CAS 均为注入 Callback；
- 尚未连接真实 I/D/C Owner Ledger Adapter 或签名 Snapshot Attestation Verifier；
- Test-profile Digest Helper 不是获批的生产 Canonicalization/Signature Profile；
- 不证明生产 COC Quorum、Owner Gate Release、PostgreSQL/Storage Prepared Participant、Crash/Failover 或物理 JF-10；
- H Schema 测试不等于 I/D/C Owner 已接受 1.2.16 新增的 Owner-specific High-water 字段。

**结论：** 1.2.16 Schema 实例结构 — PASS；1.2.17 有界语义参考 Join — 已包含于 390 项测试套件并通过；生产 Owner Gate Release / COC / JF-10 — OPEN / NOT VERIFIED / NOT AUTHORIZED。
