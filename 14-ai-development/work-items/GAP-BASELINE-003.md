# GAP 六项 — 第五轮独立复测

复测时间：2026-11-21
复测 commit：`main @ 2025472`
复测环境：WSL2 Ubuntu 24.04 / gcc 13.3.0 / cargo 1.95.0
复测方式：`git archive main | tar -x` 到干净目录，非工作区、非增量

## 命令与结果

```
cargo test --workspace --all-targets --offline
218 passed, 0 failed, 0 ignored
```

```
cd 08-bmcp-protocol/tests/conformance
python3 -m unittest discover -s recovery_cutoff -p 'test_recovery_join*.py'
Ran 31 tests — FAILED (failures=3)

python3 -m unittest discover -s provider_outcome -p 'test_*.py'
Ran 10 tests — OK (skipped=5)
```

## 六项状态

| GAP | 本轮前 | 本轮后 | 证据 | 生产权威接入 |
|---|---|---|---|---|
| 01 Compiler | 1832 行 / 31 tests / 无接线 | **2078 行 / 35 tests / 已接线** | `cargo test -p memory-compiler` 35 passed | **NO** |
| 02 Context | 786 行 / 20 tests / 无变更语义 | **2084 行 / 61 tests / ChangeSet + 6 操作** | `cargo test -p memory-context` 61 passed | **NO** |
| 03 Agent Integration | 160 行 / 4 tests / 无 adapter | **382 行 / 8 tests / adapter 存在** | `cargo test -p agent-integration` 8 passed | **NO** |
| 04 BMCP | 1 schema / 0 可执行测试 | 2 schema / 41 tests / **3 失败** | 见上 | **NO** |
| 05 Phase 2 | 0 类型 | **24 tests / 3 compile_fail 生效** | `cargo test -p memory-domain` 24 passed | **NO** |
| 06 E2E | 1 正向测试 | **6 测试（5 通过 + 1 不可达已报告）** | `--test e2e_negative_paths` 5 passed | **NO** |

## 本轮实质进展

**GAP-01 接上了脊梁。** `compile` 现在强制经过 `AdmissionStore`：

```rust
pub fn compile(&mut self, ..., producer_work_item_id: &OpaqueId)
    -> Result<PublishedDerivative, CompilerError>
```

- 缺 producer receipt → `MissingProducerAdmission`
- authority 拒绝 → `PublicationSuppressed`，**不写 publication receipt**
- store 失败 → `AdmissionStoreFailure`
- 只有 receipt 持久化且 visible 才返回 derivative

新增 4 个测试，其中「未注册生产者被拒」和「authority 拒绝后无 receipt」是真正的路径证明。

**GAP-02 有了编辑器。** ChangeSet 是 all-or-nothing 的：stale base 拒绝、任一操作失败则零操作落地、Remove 留 tombstone、Reorder 拒绝非排列、Update 不能改 `memory_version_id`。

**GAP-05 的类型系统真的拦住了。** 3 个 `compile_fail` doctest 通过，证明：
- `ClaimRef` 不能从 `FactRef` 构造
- `Fact` 不能由 confidence + Verified 单独构造
- I/D 占位 newtype 无法伪造

**GAP-06 的负向路径立住了。** 5 个跨 crate 负向测试：scope 隔离、candidate 生命周期、stale 版本、budget 溢出（带 actual/limit）、文件库重启。

## 未闭合

**GAP-04 有 3 个测试失败，不是通过。** 根因已定位：

1. `owner_snapshots.{C,D,I}.{admission,request}_highwaters` 的 `minProperties: 1` 强制每个参与方至少报一条 highwater — 一个从未准入任何东西的参与方无法产出合法文档，只能伪造记录。
2. index 测试用整格精确匹配，实际格含括号后缀，永不命中。
3. 重复 JSON 成员被 `except ValueError` 吞成 `invalid JSON: ValueError`，与「不是 JSON」不可区分。

**GAP-06 的 forget 路径不可达。** 实测：`memory-store` 与 `memory-storage` 中 `forget` 命中数为 0；只有 `memory-event-store-sqlite/src/forget_fence.rs` 有 `record_forget`，且它需要自己的连接，不与 `MemoryStorage` 互通。所以「忘记的记忆不得进入 Context」这条 E2E 无法通过公开 API 证明。

**六项全部 NO 生产权威接入。** 这是 #457 已记录的批准链问题，本轮无变化。

## 我本轮自己的错误

1. **`git reset --hard origin/main` 丢掉了 Owner C 已合并的 adapter。** 我用它清理重复类型定义（`ClaimRef` 定义两次导致 20 个 `E0428`），清理正确，但连带删掉了 `618862d`。Owner C 独立读 GitHub 发现 main 上无 adapter 并拒绝在不一致基线上作业 —— 它是对的，我错了。已重新合并为 `b913a64`。

2. **重复合并已在 origin 的 PR。** 我把 Owner A、B 的分支又合并了一次，而它们的 PR 已经进了 origin/main，于是 `memory-domain/src/lib.rs` 里 `ClaimRef` 出现两份。教训：merge 前先 `git fetch` 并检查分支是否已是 origin/main 的祖先。

3. **我曾报告 GAP-02 为 41/40/2（共 83 行）**，实际是 38/37/2（共 77 行）。Owner G 纠正了我，我核对了文件，它是对的。

## 判定

| 项 | 判定 |
|---|---|
| 六项代码缺口 | 四项实质推进（01/02/05/06），一项待修（04），一项待接线（03） |
| 测试真实性 | 218 全绿；BMCP 3 失败已如实计入 |
| 生产就绪 | **无一项**。六项均无生产权威接入 |
| 可否宣称 GAP 关闭 | **否**。代码缺口收敛，批准链缺口零进展 |
