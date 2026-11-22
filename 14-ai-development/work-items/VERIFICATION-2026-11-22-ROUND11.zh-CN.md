# 验证轮次 —— 2026-11-22 12:20–12:40 +08:00

本文只记录验证者的实测。文中没有任何代码由验证者编写。

## 0. 先看这个：数字每隔几分钟就变

本轮测量期间 main 前进了三次：

| 时间 | head | passed | ignored |
|---|---|---|---|
| 12:20 | `1904c1af` | 487 | 3 |
| 12:35 | `b093b59f` | **503** | **1** |

所以下文没有一个数字是"关于这个仓库"的事实，每个都是"关于某个 commit、某一分钟"的
事实。后续结论在本文提交前已于 `b093b59f` 复核；之所以把趋势也记下来，是因为变化
速度本身就是本轮最重要的测量。

## 1. 测试基线已变，我此前的数字作废

```
$ cargo test --workspace --all-targets      # at b093b59f
PASSED=503  FAILED=0  IGNORED=1
```

计数链条现在完全对得上，而 GAP-10 §6.2 留下的那个缺口也不再是问题：

| 测点 | passed | ignored | 变化 |
|---|---|---|---|
| `b29278a8`（§6 的测量） | 385 | 10 | — |
| `444deef1`（本验证者） | 411 | 10 | +26 |
| `1904c1af`（本验证者） | 487 | 3 | +76 / ignore 减 7 |
| `b093b59f`（本验证者） | **503** | **1** | +16 / ignore 减 2 |

这一窗口内共有 9 个测试不再被 ignore，这才是实质变化：它们不是被跳过，而是被实现了。
§6.2 里"371 与 385 对不上"的悬案至此失效——因为该注要求的正是"重新推导而不是继承"，
而这一次确实重新推导了。

仍被 ignore 的只剩一个：`dm2_06_missing_authorization_ref_blocks_fact_publication`。
它有名字，所以是一个已知的洞，而不是无声的洞。

## 2. D6.2 已落地，且落得正确

`#576`（`6500d9d4`）做的正是 GAP-12 第 1 步所规定的，且由一个并非我派出的会话完成
（我派出的 Owner 在动手之前就被 429 限流）。

按 GAP-12 自己的关闭标准逐条核对：

| 标准 | 结果 | 证据 |
|---|---|---|
| C1 无任何一行把游标称作"确认" | **通过** | `lib.rs:643-647` 注释明写 "NOT evidence that a canonical commit was confirmed" |
| C2 `StagingInput` 字段改名 | **通过** | `lib.rs:431` `canonical_commit_cursor_recorded`；`:287` 的 `PublicationProof` 有意保持不变 |
| C3 有测试：仅凭游标不得得出 `true` | **通过** | `caller_supplied_cursor_does_not_confirm_canonical_commit`，另有 `staging_accepts_a_recorded_cursor_...`、`staging_rejects_a_run_with_no_recorded_cursor` |
| C4 `pending_d()` 不在 gate 路径上 | **通过** | `grep pending_d crates/memory-compiler/` → 0 |
| C5 disposition 不变 | **通过** | 503/0/1，`Ok(Blocked)` 保持 |
| C6 第 2/4/5 步连同归属记录在案 | **通过** | GAP-12 §5、GAP-13 §6 |

值得注意的是改名的边界守得很准：`StagingInput` 改了名，`PublicationProof` 没有改。
若改错一个，gate 就会被意外打开。

## 3. GAP-11 已实质性关闭

我此前记为"通过本身就是缺陷"的那个只有四行注释的空函数，现在是一个真实测试，
位于 `crates/memory-context/tests/e2e_negative_paths.rs:195`：

```
running 1 test
test forgotten_memory_is_excluded_from_context ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 7 filtered out
```

它断言五件事，其中包含一个"遗忘前可见"的前置检查，使后续断言真正有意义：

- 遗忘前可见（`assert_eq!(before.memory_version_id, ...)`）
- 遗忘后 `read_current` → `Ok(None)`
- 遗忘后 `read_revision` → `Ok(None)`
- 被 fence 的写入返回 `MemoryStoreError::Storage(StorageError::Forgotten)`
- `forget_memory` 是 `MemoryStore` 的公开方法（`lib.rs:125`）

GAP-11 的核心发现——"测试没有任何断言，所以 `ok` 什么也没证明"——已不再成立。
取代它的是一个"遗忘功能一旦失效就会失败"的测试。

## 4. 仍未关闭的，均为实测而非推测

**GAP-09 —— schema 非空审计仍是红的。**

```
$ cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py
EXIT=1
5506 行
目录下 32 个 *.json
```

与上一轮完全一致，并在 `b093b59f` 复核过，逐字节相同。归因不变：审计表声明覆盖
"每个直接子级 `*.json`"，实际覆盖 32 个中的 2 个。这需要对 30 个 schema 族逐行做人的
判断，不能靠脚本——重新生成行是错误的修法，因为 #505 是在读懂 schema 语义之后，才刻意
修改了 2 条条件约束。

**GAP-11 —— 两处 fence 仍未合并。**

`memory-storage-sqlite` 的 `canonical_forget_fences` 被 5 处查询
（`lib.rs:128,176,214,250,1062`）。`memory-event-store-sqlite` 的 `forget_fence.rs`
自带一套 fence。两个 crate 互不引用。遗忘**路径**现在经由 `MemoryStore` 端到端可用，
所以用户可见的缺陷已关闭；但我记录的"分裂权威"依然存在：两处 fence、两套键、没有 join。

这比 GAP-11 原本的严重度低得多，应当重新定级，而不是继续当作 Tier 1 背着走。

**GAP-13 —— 参与者准入，外部依赖，未变。** Rust 中 `JF10` 仍为 0；回执 schema 仍自称
候选并放弃密钥策略。本轮没有任何推进。

## 5. 本轮没有做什么

- 没有重审那 30 个 schema（需要对每个族做归属方判断）。
- 没有尝试 `Published`：它仍需要 GAP-12 §5 与 GAP-13 §6 点名的那三个外部签发者。
- 没有处理两个工作树里都存在的未跟踪 `Cargo.lock`；它该不该入库是归属方的判断，
  不是验证者的。
