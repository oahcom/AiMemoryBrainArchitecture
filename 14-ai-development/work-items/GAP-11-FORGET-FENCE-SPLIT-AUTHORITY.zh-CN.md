# GAP-11 — #541 的合并制造了第二套 forget fence，且没有关闭任何缺口

**状态：** 开放 —— 由一个已合并改动引入的新分歧
**测量位置：** `main @ b29278a8`，2026-11-22 02:05 +08:00，WSL2 Ubuntu 24.04
**不取代任何项。** 与 GAP-06 并列，GAP-06 保持开放。

## 本文为什么存在

PR #541 于 2026-11-21T18:00:32Z 合并为 `b29278a8`。它给
`crates/memory-storage-sqlite` 加了一套真实且有测试的 forget 授权。它**没有**
关闭 GAP-06，并且引入了 GAP-06 从未规定的第二套 fence。

两句话都在下文被测量。二者都不是对该 PR 质量的评价：代码做到了它 commit
message 说的事。问题在于本仓库里 "forget" 现在不再指同一件事。

## 1. #541 实际建了什么

一张新表，与既有的 `forget_fence` 完全独立：

```sql
CREATE TABLE IF NOT EXISTS canonical_forget_fences (
  target_kind TEXT NOT NULL CHECK (target_kind IN ('Memory', 'Version')),
  target_id   TEXT NOT NULL,
  fence_sequence INTEGER NOT NULL UNIQUE CHECK (fence_sequence > 0),
  reason_digest TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  PRIMARY KEY (target_kind, target_id)
);
```

`crates/memory-storage-sqlite/src/lib.rs:117`。

既有的 event-store fence 的主键不是这个：

```sql
CREATE TABLE IF NOT EXISTS forget_fence(
  namespace_key TEXT PRIMARY KEY,
  fence_seq INTEGER NOT NULL UNIQUE CHECK(fence_seq > 0),
  reason_digest TEXT NOT NULL,
  recorded_at TEXT NOT NULL
);
```

`crates/memory-event-store-sqlite/src/forget_fence.rs:56`。

GAP-06 的契约是后者："被 fence 的 **namespace** 不能产出 Memory revision"
（GAP-06 推荐方案）。#541 实现的是前者："被 fence 的 **memory 或 version** 不能
产出 Memory revision"。粒度不同、表不同、API 不同，且没有对账路径。

## 2. 两套 fence 互相不知道对方

```
$ grep -rn "forget_fence" crates/memory-storage-sqlite/src/lib.rs crates/memory-store/src/lib.rs
（零匹配 —— 存储层从不查询 namespace fence）

$ grep -rn "canonical_forget" crates/memory-event-store-sqlite/src/forget_fence.rs
（零匹配 —— 事件存储从不记录 target fence）
```

可独立复核的后果：

- 通过 `ForgetFence::record_forget(namespace_key, digest)` 记录的 forget，仍然
  拦不住 `MemoryStore::read_current`。主线上有一条测试仍在通过，见下。
- 通过 `MemoryStorage::forget_memory(memory_id, digest)` 记录的 forget，不会让
  `ForgetFence::restore_backup` 清除该 memory 的事件行。恢复路径只按 namespace
  过滤 `accepted_events.scope_json`（`forget_fence.rs:176`）。
- 两套机制的 reason_digest 各成一套命名空间，审计方无法 join 出"这条 memory 是否
  被遗忘过"。

## 3. GAP-06 仍未关闭的证据

GAP-06 关闭条件第 4 条原文：

> 反向测试 `forget_api_absence_is_detectable` 改为断言已强制执行的行为，或由明确的
> 替代回归测试取代；目标 E2E `forgotten_memory_is_excluded_from_context` 取消
> ignore 并通过。

在 `main @ b29278a8` 上实测：

```
$ cargo test -p memory-context --test e2e_negative_paths -- --include-ignored
test forgotten_memory_is_excluded_from_context ... ok
test forget_api_absence_is_detectable ... ok
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`forget_api_absence_is_detectable` **通过本身才是缺陷**，不是好消息。该测试先记录
一个 namespace fence，然后断言 revision **仍可读**。它自己就写明
（`e2e_negative_paths.rs:209-211`）：

> This test is expected to FAIL the moment forget is wired into the read gate.

它没有失败。namespace fence 仍然没有接入任何读取门禁。

## 4. `forgotten_memory_is_excluded_from_context` 是一条没有断言的"绿"

这是更严重的发现，且与 #541 无关。

```rust
#[test]
#[ignore = "unreachable: no public forget API; see GAP-06-FORGET-PATH-UNREACHABLE"]
fn forgotten_memory_is_excluded_from_context() {
    // Intended public flow once the boundary exists:
    // create + write -> MemoryStore::forget_memory(memory_id, scope)
    // -> read_current returns no eligible revision -> build_context is empty.
    // Do not emulate this by editing ContextCandidate.lifecycle.
}
```

`crates/memory-context/tests/e2e_negative_paths.rs:199-207`。函数体是四行注释，
没有 `assert`、没有调用、没有 fixture。

因此 `--include-ignored` 会报 `ok`，而任何"跑 ignored 测试来度量进度"的未来
工具都会把它计为一条通过的 forget 测试。它不是测试，是一个会报成功的 TODO。

对照 phase-2 验收测试，同样的"暂时做不到"被诚实地处理：

```
$ cargo test -p memory-domain --test phase2_acceptance -- --include-ignored
dm2_01_claim_revision_ref_uniqueness_enforced ... FAILED
dm2_02_accepted_revision_is_append_only ... FAILED
dm2_03_ci_classification_vectors ... FAILED
dm2_04_resolution_rejects_claim_head_substitution ... FAILED
dm2_06_missing_authorization_ref_blocks_fact_publication ... FAILED
dm2_08_unregistered_relation_type_rejected ... FAILED
dm2_09_relation_time_scope_lifecycle_independent ... FAILED
dm2_11_provenance_lineage_or_unavailable_reason_mandatory ... FAILED
dm2_12_shared_ancestry_not_independent_evidence ... FAILED
```

九条失败，每条都是指名行上的 `unimplemented!()`，每条 `#[ignore]` 理由都点名了
缺失的 API。那叫"被阻塞的测试"。forget 那条 E2E 是个空函数。区别就是全部要害：
一个被强制运行时大声失败，另一个不可能失败。

## 5. 新的 forget 路径在生产中依然不可达

与 GAP-07 同一形状。新 API 的全部调用点都在 `#[cfg(test)]` 内：

```
$ grep -rn "\.forget_memory(\|\.forget_version(" crates/ --include=*.rs
crates/memory-store/src/lib.rs:832,876                    (mod tests，cfg(test) 在 120)
crates/memory-storage-sqlite/src/lib.rs:2948..3205        (mod tests，cfg(test) 在 1182)
```

- `MemoryStore` 共 8 个 pub 方法，没有一个叫 forget（`lib.rs:33-98`）。
- `brain-cli` 中 `forget` 出现 0 次。
- 唯一可承载调用方的是 `MemoryStorage` trait，而它的适配器消费方尚不存在。

于是：树里现在有三套 forget 机制 —— event-store namespace fence、storage target
fence、以及 `MemoryLifecycle::Forgotten` —— 而没有一条可执行路径能到达任何一套。

## 6. CI 没有评估其中任何一条

#541 head commit 与 `main` 上的四个 check run 给出同一个非结论。注解原文：

> The job was not started because recent account payments have failed or your
> spending limit needs to be increased.

`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` 返回
`403 — Upgrade to GitHub Pro or make this repository public to enable this
feature.`

所以 #541 是在"mergeable 为真、零个已执行检查、无分支保护"的条件下合并的。本文
全部发现都是本地跑出来的；在当前 CI 状态下，其中没有一条可能被捕获。

## 关闭条件

以下全部满足才能关闭 GAP-11：

1. 在规范文件中点名指定一套 forget 授权为权威；另一套要么删除，要么明确定义为
   它的派生索引。
2. namespace fence 与 target fence 完成对账：要么 namespace forget 同时阻断其下
   memory 的读取，要么删除 namespace fence 并把 GAP-06 显式重定为 target 粒度。
3. `forgotten_memory_is_excluded_from_context` 要么含有"今天失败、修复后通过"的
   断言，要么删除。空的 ignored 函数不得继续作为进度信号存在。
4. `forget_api_absence_is_detectable` 失败，随后由断言已强制行为的回归测试取代。
5. 存在非测试调用方：`MemoryStore::forget_*` 或一个 CLI 动词，并有穿过它的测试。
6. 合并结果上 `cargo test --workspace --all-targets` 报 0 failed，且关键地，
   ignore 计数是重新推导的，而不是继承来的。

## 本文不主张的事

- 不主张 #541 是错的。它的 fence 在 7 条写/读路径上强制执行（已核验：
  `create_memory`、`commit_version`、`prepare_version`、`publish_prepared`、
  `read_version_row`、`list_changes`、`resolve_idempotency`），新增 19 条测试，
  未删除任何一条。
- 不主张 forget 功能完成度是 0%。在 target 粒度上它是真实且有测试的。
- 不主张 namespace fence 就是正确设计。它很可能就是错的那个。而这恰恰是关闭条件
  1–2 要求有人做出并记录的决定，而不是让两套机制偶然共存。
