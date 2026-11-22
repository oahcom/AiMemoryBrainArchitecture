# GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022

**登记编号**：GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022
**性质**：MEASUREMENT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
**测量点**：`main = b093b59f`（2026-11-22 12:29 +08:00）
**登记时间**：2026-11-22
**作者**：协调会话（非独立审查者）
**取代**：本文件取代被驳回的 PR #589（原拟编号 021，因编号已被 `GOV-NC-2026-11-22-ENUM-BOUNDARY-021` 占用而改号）

---

## 0. 为什么重写而不是修订

PR #589 被 Owner 驳回，两条理由都成立：

1. **分母过时**。它用 `dba34a35` 的测量（9 条 ignore）描述 `main` 的现状，而 `main`
   上实际只剩 2 条。表中 5 条 API 已经存在。
2. **复现命令跑不起来**。头部写 `AR=zigar`，该二进制不存在。

第 2 条尤其致命：一份登记的全部价值是「这是我跑过的命令」，命令报错比没有命令更糟。

本文件因此把**当前表放在最前**，历史表标注 `superseded` 放后面。这是 #589 评论里的
要求，也是正确的读法。

---

## 1. 当前状态（`main = b093b59f`，2026-11-22 12:29 +08:00）

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets
binaries: 30
passed=503  failed=0  ignored=1
```

平台：Windows 10，Git Bash，`cargo 1.100.0`。`zigcc` / `zigar` 是本机的
`.bat` 包装（`%LOCALAPPDATA%\Temp\opencode\zigcc.bat`），因为本机 gcc 缺 `cc1`：

```
gcc.exe: fatal error: cannot execute 'cc1': CreateProcess: No such file or directory
```

在 WSL2 上等价写法是 `CC=zigcc AR="zig ar"`（`zig` 在 PATH 中，无 `.bat` 包装）。
**两种写法互不通用**，这是 #589 被打回的第二条原因。

`crates/memory-domain/tests/phase2_acceptance.rs` 中仅剩 **1** 条 ignore：

| 行 | 测试 | 阻塞者 |
|---:|---|---|
| 605 | `dm2_06_missing_authorization_ref_blocks_fact_publication` | 权威 I |

Phase 2 验收共 20 个测试：**19 通过 / 1 ignored**。

### 1.1 唯一剩余缺口：`dm2_06`

原文理由：

> `FactRevision::initial` 强制要求 `AuthorizationDecisionRef`，但当前唯一公开构造是
> `AuthorizationDecisionRef::pending_i()`；类型没有 absent/validated-I-issued 状态，
> 无法证明缺失授权被拒绝。Round 4 的 `fact_with_placeholder_attestor_validates_today`
> 固定了当前占位符可通过的事实。

实测确认这条理由**仍然成立**：

```rust
// memory-domain/src/lib.rs — pending_i() 的文档注释
/// NOT DEFINED: awaiting I. Placeholder only; security identity semantics are not inferred.
/// `pending_i()` is public and any caller can create this placeholder. It is not proof of
/// an attestor identity. This known temporary construction window closes only when I
/// defines the contract and the placeholder is replaced by a validated, non-forgeable ref.
```

这是 Phase 2 里**唯一**一条被外部决定硬阻塞的条目。它需要的不是代码，是 I 签发
`AuthorizationDecisionRef` 契约（至少三态：`Absent` / `Pending` / `Validated`，且
`FactRevision::validate` 在前两态返回 `Err`）。

**已知冲突必须一并处理**：`fact_with_placeholder_attestor_validates_today` 固定了
「当前占位符可通过」这一事实。新判据与它互斥，两者必须同时改，否则无论先改哪边
都会让测试变红。

---

## 2. 历史表（`dba34a35`，**superseded**，仅供追溯）

以下是被 #589 用作「现状」的表。它准确描述了 `dba34a35`，**不准确描述任何更晚的
提交**。保留它是因为它记录了 9 条 ignore 各自的理由原文，而其中 8 条现在已不存在
于代码中，理由只能从这里查到。

| 测试 | `dba34a35` 理由 | 关闭者 |
|---|---|---|
| `dm2_01` | 无 `ClaimRevisionRegistry` / `register_revision` | #570 `5c50b910` |
| `dm2_02` | 无 `AcceptedRevisionState` | #570 `5c50b910` |
| `dm2_03` | 无 `classify_claim_change` | #545 `444deef1` 加 `classify()`；测试体由 #567 `caa37a7e` 改写 |
| `dm2_04` | 无 `ClaimRevisionResolver` / `resolve_claim_head` | #570 `5c50b910` |
| `dm2_06` | 见 §1.1 | **未关闭** |
| `dm2_08` | 无 `RelationTypeRegistry` | #574 `241e385c`（+ #581 `a0d4f7d7` 区分失败模式） |
| `dm2_09` | `RelationExtension` 无 `scope_refs` | #574 `241e385c` |
| `dm2_11` | `Provenance` 无 `validate` / `parent_provenance_refs` / `unavailable_reason` | #583（`Provenance` 现有 `source_version_refs`、`parent_provenance_refs`、`unavailable_reason`、`method_version` 四字段 + `validate`） |
| `dm2_12` | 无 `ProvenanceGraph` / `DerivationEdge` / `validate_independent` | #582 `fe9e25a5` |

### 2.1 `dm2_03` 是本系列唯一的方法论证据

`dm2_03` 的 ignore 理由在 `dba34a35` 时就已经是假的——`classify()` 由 #545 落地，
19 个测试覆盖 CI-01..CI-13 中可达的 10 条。发现方式不是读文档，是跑：

```sh
grep -rc "classify" --include=*.rs crates/memory-domain/src/
cargo test -p memory-domain --lib claim_identity   # 19 passed
```

这正是 Owner 保留这段的理由：「你检查的是代码，不是上一份文档」。但它随后也被
#567 改写并合入，所以现在这段同样是历史。

---

## 3. 对「Phase 2/3 领域模型 100% 未启动」的最终更正

这句话在三个测量点上都是错的，且错得越来越彻底：

| 测量点 | 通过的验收维度 | 剩余 ignore |
|---|---:|---:|
| `dba34a35` | 11 | 9 |
| `fe9e25a5` | 18 | 2 |
| `b093b59f` | **19** | **1** |

Phase 2 的真实状态是：**19 个验收维度通过，1 个等 I 权威**。不是「未启动」，是
「只剩一条被外部决定卡住的收尾项」。

这个更正的价值不在于数字，而在于**处置方式完全不同**：

- 若相信「未启动」，会派工去写 20 个维度的规格与实现——其中 19 个已存在，产生
  重复劳动（#573 就是这样被关闭的：它重写了 #570 已落地的四个 API）。
- 若看到「19 通过 1 阻塞」，唯一正确的动作是**等 I 的决定**，不派工。

---

## 4. 我从这两次驳回里学到的方法论

两次驳回指向同一个缺陷：**用旧测量描述新状态**。

第一次（登记 021 v1 → v2）我加了「是否有并行 PR 在做」这一维。第二次（#589 被驳回）
说明这还不够——我加了「查开放 PR」，但**没查已合并的 PR**，也没在写文档前重跑一次。

修正后的发布前检查清单：

1. `git fetch && git reset --hard origin/main`，记录实际 HEAD；
2. 在该 HEAD 上跑一次复现命令，把输出贴进文档，不引用上一轮的输出；
3. 复现命令必须**在本机实际执行通过**再写进文档（#589 的 `AR=zigar` 就没通过）；
4. 查开放 PR 与**近期已合并** PR，两者都要看；
5. 表格第一行必须是当前测量点，历史放后面并标注 `superseded`。

第 3 条是这次新加的。前两条我在 021 v2 已经做了，但复现命令没验证。

---

## 5. 本登记不做的事

- 不修改 `phase2_acceptance.rs`；
- 不新增生产代码；
- 不声称 `dm2_06` 可做——它等 I；
- 不声称本登记是独立审查（作者是协调会话）；
- 不触碰 `INDEX.md`（这是登记条目，不是新工作项）；
- 不复用编号 021（已被 `GOV-NC-2026-11-22-ENUM-BOUNDARY-021` 占用）。

## 6. 复核清单

```sh
# 平台：Windows Git Bash，本机 gcc 缺 cc1，故用 .bat 包装
export CC="$LOCALAPPDATA/Temp/opencode/zigcc.bat"
export AR="$LOCALAPPDATA/Temp/opencode/zigar.bat"

git fetch && git reset --hard origin/main && git clean -fd
git log -1 --format='%h %ci %s'

cargo test --workspace --all-targets
grep -n "#\[ignore" crates/memory-domain/tests/phase2_acceptance.rs
```

预期（`b093b59f`）：`passed=503 failed=0 ignored=1`，ignore 仅 605 行。
若 ignore 数量变化，§1 与 §3 的表需要重测，不得沿用。
