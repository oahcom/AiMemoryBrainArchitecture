# Phase 3.8.27 — H Applied Delivery Evidence 1.0.0 精确 Head 同步与 30 项测试验证
# Phase 3.8.27 — H Applied Delivery Evidence 1.0.0 Exact-Head Sync and 30-Test Verification

- 日期：2026-11-18
- Owner 分支：`session-h-bmcp-protocol`
- 精确分支 Head：`4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`
- 关联 Issue：#3
- 上游阶段：H Phase 3.8.24 / 3.8.25 / 3.8.26

## 1. 精确源码 Pin

H Owner 分支已同步 main 中最新的 Resolver Reference 精确相等修复及对应负向测试。该分支继续保留独立的 Applied Delivery Evidence 1.0.0 消息族；Unified 1.2.15 保持不变。

| Artifact | 精确 Blob |
|---|---|
| Applied Delivery Evidence 1.0.0 Schema | `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` |
| Reference Validator | `43f402e4a09034da197ac24856cddbd496c9c75f` |
| 符合性测试 | `98242cc193a77b27d58b39353ccc031201992614` |
| H Workflow | `c029a0b1beb6f24916163169873b856fb16d5214` |
| CSubmitOutcome Join 补充文件 | `9ff4ac5b64b354f63add21a5d16d37da46835c07` |

## 2. 精确 Head CI

GitHub Actions Run [#44187702465](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187702465) 由 Push 触发，并检出了精确 Head `4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`。

- Workflow：H Applied Delivery Evidence Conformance
- Job：`applied-delivery-evidence` — SUCCESS
- 测试步骤：`Run Applied Delivery Evidence schema and semantic conformance tests` — SUCCESS
- 解码后的 Job 日志：`Ran 30 tests ... OK`
- 负向测试 `test_27_resolver_record_ref_must_equal_h_c_submit_outcome_ref` 已成功执行。

这证明 H Owner 分支精确 Head 上的 Python 参考/符合性候选套件 30/30 通过。

## 3. 正确性影响

同步前，H 的 Resolver Callback 可以返回一条不同于 H Envelope 中不透明 `c_submit_outcome_ref` 的、但本身有效的 CSubmitOutcome 记录。现在 Validator 强制要求 Resolver 返回的 C `record_ref` 与请求引用完全相等；不匹配时在 H 接受 Observation 前返回 INVALID。

该修复防止 Resolver 替换将 H 证据静默绑定到另一条有效 C 记录。原有的 Record Sequence、Payload Digest、Final Request Boundary 以及可选 ActualInferenceRequestId 精确相等检查仍然保留。

## 4. 严格范围与剩余阻塞

30/30 结果只证明有界 Python 参考/符合性套件通过，不证明：
- 真实、经认证的 C Owner Ledger Resolver 或 C Signature/Trust Root 验证；
- 生产 JCS/Canonicalization、Ed25519/HSM/KMS Key Lifecycle 或外部 Anti-Rollback；
- H Durable Replay/Observation Storage、崩溃恢复或已部署 Adapter/Runtime 集成；
- 真实 I PermissionEpoch 与 D ForgetFence Ledger Adapter；
- G Durable Applied Persistence/Restore、多副本幂等或端到端 Full Applied；
- 独立人类 C/H/G Owner 验收。

**处置：** H 候选参考套件 — **PASS（精确 Head 上 30/30）**。H 生产服务 — **未验证**。跨 Owner Wire Freeze — **NO**。生产激活 — **NOT AUTHORIZED**。
