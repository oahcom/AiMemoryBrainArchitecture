# Phase 3.8.26 — G Restore-Fenced Write Admission 加固
# Phase 3.8.26 — G Restore-Fenced Write Admission Hardening

- 日期：2026-11-18
- 精确代码 Commit：`470d4c1934999263bfb8a4822b13c2ff854c3dfd`
- 测试 Blob：`e77d2375506e423bf53d8341fe9aecf2719d0609`
- Workflow：[G Applied Persistence Reference Model #44188852578](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44188852578)
- Job：`g-applied-reference-model` — SUCCESS
- 日志：`Ran 17 tests ... OK`

## 1. 发现的缺陷

参考模型在 Stale/Mismatched Restore 后能够正确禁止受保护的 Current Use，但 `commit_full_applied` 没有检查全局 Restore Fence 状态 `serving_enabled`。因此，在 Restore Reconciliation 仍处于 FENCED 时，调用方仍可创建新的 Full Applied Ledger/Outbox Record。

这违反了 G 合同中“权威 Reconciliation 完成前，必须阻止新的 Full Applied 和受保护 Current Use”的要求。

## 2. 修复

现在 `commit_full_applied` 会在同一个 SQLite 写事务中读取 `g_meta.serving_enabled`。在 Restore Fence 激活时，分配新 Ledger Sequence 或插入新 Applied Row 之前，必须拒绝新的 Full Applied Commit。

对已经提交且 Identity/Revision/Digest 完全相同的幂等查询，仍返回原 Receipt；不会创建新 Row。全局 Restore Fence 激活期间，Current Use 仍被禁止。

新增负向测试：
- `test_17_restore_fence_blocks_new_full_applied_commit`

该测试先提交一条既有 Applied Row，再引入 Stale Restore 使状态变为 FENCED，随后尝试不同的新 Applied Identity。新提交被拒绝，Ledger/Outbox 数量保持不变。

## 3. 验证

精确 Commit `470d4c1934999263bfb8a4822b13c2ff854c3dfd` 在 Run #44188852578 中 **17/17 PASS**。前一阶段新增的 Restore Anchor 测试 15、16 也在本次完整套件中再次通过。

## 4. 限制

这仍是有界 SQLite 参考模型，不证明生产 G 数据库事务、认证外部 Anchor、实时 Owner Ledger Proof 解析、多进程/多副本恢复、PostgreSQL/Storage 集成或生产 Full Applied。生产 G 仍为 NOT IMPLEMENTED / NOT VERIFIED。
