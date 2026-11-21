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

## 第八轮复测（2026-11-22 02:25 +08:00，`main @ 6696ca8a`）

追加内容；上方正文未改动且仍然准确。本节收窄数字并确认机制。

```
$ cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py; echo "EXIT=$?"
... 5506 行  <schema>.json:<pointer>:<constraint> ...
EXIT=1
```

与上次测量一致。这期间没有任何修复；本项仍然是红的。

### 缺口现在归因到单独一个数字

```
$ ls 08-bmcp-protocol/schemas/*.json | wc -l
32

$ sed -n 3p 08-bmcp-protocol/schema-nonempty-audit.md
**Audit baseline:** `main` at `88bf4875...` (2026-11-21). Scope: every
direct-child `*.json` in `08-bmcp-protocol/schemas/`; 2 files were present.
```

审计表自己声明的范围是*该目录下每一个 direct-child `*.json`*。它审计了 2 个。目录里
有 32 个。30 个文件的差额就是那 5506 条未登记约束，而且算术可核对：2 个文件 93 条
已登记约束，30 个文件 5506 条未登记。

provenance，来自 `git log --diff-filter=A`：

| 提交 | 效果 |
|---|---|
| `9a98956f`（#500） | 合入 H 协议 schemas —— 30 个文件就是这里进来的 |
| `3aaf761f`（#505） | 审计表自身的最后一次修改 |

`#500` 加了 schema 但没有扩展审计。`#505` 之后动了这张表，却没注意到范围不匹配。两条
事实都在 log 里，都不是推断。

### 为什么重新生成 5506 行仍然是错误的修法

这张表不是一串约束字符串。每一行都带着一个判断：

```
| schema | location | constraint | may be legally empty? | disposition | rationale |
```

该表自己的 Summary 记录着 #505 里**有意改动**了 2 条条件约束 —— "zero-count
PARTIAL/NOT_ENUMERATED/UNAVAILABLE/UNKNOWN 状态可以没有可报告的 highwater，且不得
凭空合成一个"。那条裁定需要读懂 schema 语义。用默认处置自动生成 5506 行，会得到一张
能通过脚本、但一个判断都没有的表 —— 那比红闸门更糟：它是一个什么都不认证的绿闸门。

因此关闭标准 3（"目录中每个 schema 要么已审计，要么带理由明确列为范围外"）才是真正的
工作，而它是阅读任务，不是脚本任务。

### 兄弟闸门对照，未变

同一目录族里，另两个闸门是绿的且可测：

- `08-bmcp-protocol/scripts/check_protocol_index.py` → `missing=0 extra=0
  duplicate_types=0 invalid_rows=0 PASS`，exit 0。
- `08-bmcp-protocol/tests/conformance` → 装齐 `requirements.txt` 后 585 passed /
  27 skipped / 0 failed（见 GAP-08 第八轮小节）。

两个都是绿的。只有非空审计是红的。这排除了"该区域处于过渡状态"的解释：同一目录上三个
闸门，两个正常，一个红，而红的那个之所以红，是因为一次比它自己那张表最后一次修改更早
的合并。

### CI 状态，未变且现在具有决定性

`#536` 合入了一次全工作区 rustfmt。CI 也没有为它跑起来。如 GAP-11 §6 所确立，本仓库
当前每个 check run 都带着

> The job was not started because recent account payments have failed or your
> spending limit needs to be increased.

所以在今天就接入方向 (c)，等于把一个红闸门引入一个无法执行的工作流。这并不削弱该建议
—— 它把顺序讲明确了：**(a) 必须先落地，(c) 才有意义**，否则 CI 会因为一个没人能观察到
的原因变红。
