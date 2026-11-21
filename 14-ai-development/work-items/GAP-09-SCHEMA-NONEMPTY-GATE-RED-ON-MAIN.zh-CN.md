# GAP-09 · schema 非空闸门在 main 上是红的

**状态**：未关闭 — `main` 无法通过自己的既定闸门
**领域**：08-bmcp-protocol / schema audit
**归属线**：Owner H（协议）

## 缺口陈述

`08-bmcp-protocol/schemas/test_nonempty_audit.py` 在 `main` 上退出码为 **1**。
它报告 5506 条约束存在于 schema 中却未登记进 `schema-nonempty-audit.md`。

审计表是按 **2** 个 schema 的基线写的。`#500` 合入了另外 **30** 个，却没有
改动该表。

这是闸门在正常工作，而不是闸门坏了。GAP-04 建它正是为了抓这类情况，它抓到
了。真正的缺陷是：这次合并在闸门为红的状态下落了地，而且没人发现，因为它
没接进 CI。

## 证据（在 `main @ dc32fce3` 上核验）

**1. 闸门今天退出 1。**

```sh
cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py; echo "EXIT=$?"
```

```
EXIT=1
```

5506 行输出，每行形如 `<schema>.json:<json-pointer>:<constraint>`，正是脚本
第 103 行 `item not in registered` 分支的输出。没有出现 `AUDIT_STALE:` 行，
说明全部是未登记约束——schema 增多了，表没跟上。

**2. #500 之前它是通过的。**

导出 `main @ b961ba31`（#500 之前的提交）运行同一脚本：

```
OK: 2 schemas; 93 registered constraints; no unregistered or stale entries.
EXIT=0
```

因此这是 #500 引入的回归，不是既有状态。

**3. #500 没有改动审计表。**

```sh
git show 9a98956f --stat | grep -i audit
```

零匹配。该表最后一次变更是 `3aaf761f`（#505）。

**4. 表内仍声明旧的基线。**

`schema-nonempty-audit.md` 开头写着：

```
**Audit baseline:** `main` at `88bf4875...`. Scope: every direct-child `*.json`
in `08-bmcp-protocol/schemas/`; 2 files were present.
```

而 schema 目录现在有 32 个 `*.json` 文件。

**5. 同一区域的姊妹闸门是绿的。**

`#535` 新增了 `08-bmcp-protocol/scripts/check_protocol_index.py` 与
`tests/test_protocol_index_consistency.py`。两者在同一提交上都通过：

```
indexed_unique=22
missing=0
extra=0
duplicate_types=0
invalid_rows=0
PASS
```

```
8 passed in 0.14s
```

这一点很重要，因为它排除了"仓库正处于过渡状态、闸门本来就不可能通过"这一
借口。有人正在往这同一个目录里加守卫并让它们变绿。非空审计是被跳过了，不是
被阻断了。

这也意味着红色审计并不是唯一未自动化的闸门：`check_protocol_index.py` 和
`test_protocol_index_consistency.py` 同样不出现在任何工作流里。PR 上真正跑
测试的只有 `rust-phase1.yml`。

## 为什么最显然的修法是错的

诱人的修法是用脚本重新生成那 5506 行，让闸门变绿。那会摧毁这个产物的意义。

表里每一行都承载着生成器无法代做的判断：

| 列 | 它断言什么 |
|---|---|
| may be legally empty? | 该字段的 `""`/`[]` 是否是合法协议状态 |
| disposition | 保留、收窄、或修改 |
| rationale | 用领域语言说明为什么 |

表自身的摘要证明这些是真实区分而非套话：93 条约束中有 2 条条件约束被**修改**，
因为此前的 catch-all 在计数为零时也要求 highwaters——"零计数的不完整/不可用
状态可以保持为空"，且不得凭空合成 highwater。

自动登记 5506 行未经阅读的行，等于把审计降级成清单，并使闸门无论新 schema
做什么都永久为绿。

## 候选方向

### (a) 按约束族正经审计这 30 个新 schema

5506 条原始行不等于 5506 个决策。新 schema 来自少数几个协议族
（`coc-jf10-unified` 1.2.0–1.2.17、`applied-ack`、`recovery-cutoff`、
`recovery-join`、`storage-prepared-participant-proof`、
`i-owner-snapshot-attestation`）。约束跨版本以相同含义重复，因此工作量是
若干族级裁定加上由这些裁定机械投影出的行。

这是唯一保住该产物意义的方向。它是 Owner H 的决定，因为它编码协议语义。

### (b) 把审计范围限定在已声明的 schema 集合

修改脚本，只审计表中基线所列的 schema，这样新增 schema 不会静默打破闸门。
这通过缩小覆盖面让闸门变绿。只有当表中明确说明哪些 schema 未审计时才诚实，
且会产生一个不断增长的未审集合。

### (c) 在 CI 中失败关闭

与 (a)(b) 独立：把脚本接进 CI，让红色闸门阻断合并，而不是等到某次测量才被
发现。没有这一条，下一次大批 schema 合并会重演同样的事。

## 建议

**先 (c)，再 (a)。** CI 接线很小，它把问题从"测量时偶然发现"变成"无法合并"。
然后按族级裁定做 (a)，而非逐行做。

方向 (b) 应被否决，除非项目确实打算支持未审计的 schema——因为它用一个可见
的红闸门换了一个不可见的覆盖漏洞。

## 关闭标准

1. `python3 test_nonempty_audit.py` 在 `main` 上退出 0。
2. 表中声明的基线与已检 schema 数量与现实一致。
3. 目录中每个 schema 要么已审计，要么带理由明确列为范围外。
4. 脚本在 CI 中运行并阻断合并，使红色闸门不会数周后才被发现。
