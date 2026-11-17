# Phase 3.8.25 — G Restore Anchor 精确匹配加固
# Phase 3.8.25 — G Restore Anchor Exactness Hardening

- 日期：2026-11-18
- 已测试 G 代码 Commit：`8afe821689b8a7b5c2069aef0f45fd0e89c72f87`
- 测试源码 Blob：`4978622b1767019fb254763d4c5c44db46521f83`
- Workflow：[G Applied Persistence Reference Model #44188581729](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44188581729)
- Job：`g-applied-reference-model` — SUCCESS
- 日志：`Ran 16 tests in 0.215s`，`OK`

## 1. 发现的缺陷

此前 SQLite 参考模型仅在 Snapshot Epoch 或 Ledger High-Water **小于**可信外部 Anchor 时保持 Restore Fence。如果 Snapshot 的 Epoch 或 High-Water 数值更大，并且 Owner Currentness Boolean 全部为 True，模型就会错误地接受该 Snapshot 为当前状态。

这是不安全的：高于可信 Anchor 的 Snapshot 可能是未锚定分叉、过期/配置错误的外部 Anchor，或被回滚操纵的镜像。数值更大本身不能证明存在已提交且经过认证的 Prefix。

## 2. 修正

参考模型现在要求 Snapshot Restore Epoch 和 Ledger High-Water 与可信外部 Anchor **精确相等**，才允许清除 Restore Fence。任一方向不匹配都必须保持 FENCED。生产协议只有在独立认证的 Contiguous-Prefix/Checkpoint Proof 推进可信 Anchor 后，才能重新执行精确 Reconciliation。

新增两个负向测试：
- `test_15_snapshot_epoch_ahead_of_trusted_anchor_keeps_restore_fenced`
- `test_16_snapshot_highwater_ahead_of_trusted_anchor_keeps_restore_fenced`

两个测试证明：没有认证的 Anchor 推进时，数值看似更新的 Snapshot 也不能重新启用 Serving。

G Phase 3.8.22 中英文合同现已同步写明该规则：EN Blob `a8efd1aa9696783035e157131fa9751666a4182d`；zh-CN Blob `dd3791aa50c5fb24e93f9ab5cee50d3b5c02706e`。

## 3. 验证

Workflow 在精确代码 Commit `8afe821689b8a7b5c2069aef0f45fd0e89c72f87` 上运行；两个新增负向测试通过，完整参考套件 **16/16 PASS**。

## 4. 范围

本次关闭了有界 SQLite 参考模型中的一个缺陷，并收紧 G 规范性 Restore 规则。但这不证明生产外部单调 Anchor、签名 Checkpoint 验证、真实 COC/Owner Ledger Prefix Continuity、PostgreSQL/Storage Restore 行为、多副本恢复或生产 G Persistence。G 仍为 REFERENCE MODEL ONLY；生产 Full Applied 尚未证明。
