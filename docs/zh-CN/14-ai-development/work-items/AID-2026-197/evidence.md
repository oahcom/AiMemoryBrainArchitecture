---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-197/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "下文每个数字都来自在本工作树（base 4326669c，merge base 0c752ee6）实际运行已提交的文件：两个门禁在修复前后的运行、两份自检在修复后脚本与修复前脚本上的运行、以及 ratchet 对随仓库发布的 77 条基线运行。不声称任何 CI 结果、check-run 状态或合并结果。"
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "gate"
      - "ratchet"
      - "source-revision-pointer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-197/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-197/evidence.md"
    zh-CN: null
---

# AID-2026-197 —— 两个"看起来在查、其实没查"的门禁不再名副其实

**状态：DRAFT —— 已派发、已实现、已本地验证。** 本记录覆盖 `gates` lane 的两处缺陷。两处都是静默的：
两者都产出了报告，而报告里缺的恰恰是门禁本身要报的东西。

## 1. DEF-gates-08 —— `scripts/check_source_revision_pointers.py`

模块 docstring 写的是"仅当每个 live 指针都解析成功并与源 blob 一致时才 exit 0"。有两处机制与之矛盾。

**（a）可移动引用能通过。** 当 `Source revision:` 的值不是 40 位 blob（`main`、`HEAD`、tag、一句散文）时，
脚本打印 `NON_BLOB_REFERENCE`、计数、然后把它排除在 `BAD` 之外——而退出码只读 `BAD`。于是一个
什么都解析不到的指针就成了通过的指针。

**（b）所有指针都拿 `links[0]` 比对。** 一个文档里有两对 `Source revision:` / `Source:` 时，两条记录都被拿去
和**第一个** `Source:` 链接比对。第二个指针因此与错误的文件比较：正确指针可以被判成 `STALE`，错误指针
也可以被一个它从未指过的 blob 确认为正确。缺陷文件里的合成复现显示，第二个指针声明的 blob 被记在了
`00-governance/a.md` 名下。

### 改了什么

- 非 blob 值保留原有计数器，并同时计入 `BAD`。
- live 版本记录与 live `Source:` 行按文档顺序配对：第 n 条记录对第 n 行。没有自己那一行的记录判为
  `UNRESOLVED`（`NO_SOURCE_LINK`），不再继承上一条记录的文件。
- 新增 `scan(root)` 与可选 `--root`，使行为可以在夹具仓库上被测试。默认根不变；不带参数的命令行
  行为与之前一致。

### 在本树上实测（base 4326669c）

| 运行 | exit | POINTERS | ACCURATE | STALE | NON_BLOB | BAD |
|---|---|---|---|---|---|---|
| 修复前 | 1 | 50 | 16 | 8 | 6 | 8 |
| 修复后 | 1 | 50 | 16 | 8 | 6 | 14 |

退出码没有变化，因为 8 条 STALE 指针本来就让扫描失败（这也是该脚本在
`scripts/ci/baselines/gate-wiring.txt` 里被基线化为"未接线"的原因）。变化的是判定：6 条被报出又被忽略的
可移动引用现在计入失败。它们全部是散文或分支名，而不是 blob：

```
docs/en/01-system-architecture/forget-fence-and-completion-contract.md:52
docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md:53
docs/en/03-memory-brain/memory-brain-guide.md:6
docs/zh-CN/01-system-architecture/forget-fence-and-completion-contract.md:52
docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md:53
docs/zh-CN/03-memory-brain/memory-brain-guide.md:6
```

它们只被报出，没有被修复：修复意味着改文档，那不是本工作项的范围。

### 夹具证明（同一批字节，两个脚本各跑一次）

| 夹具 | 修复前 | 修复后 |
|---|---|---|
| 一个指针，`Source revision: main`，一行 source | exit 0，`BAD=0`，`NON_BLOB_REFERENCE=1` | exit 1，`BAD=1` |
| 两个指针都正确，各有一行 source | exit 1，`ACCURATE=1` `STALE=1`，第二个指针被记在 `00-governance/a.md` 名下 | exit 0，`ACCURATE=2` `STALE=0` |

第二行同时是假红和假绿：旧脚本既给一个正确指针编造了失败，也会在错误 blob 恰好匹配时用错误的理由
确认一个坏指针。

## 2. DEF-gates-07 —— `scripts/ci/gate_ratchet.py`

ratchet 的全部价值是"失败集合与基线精确相等"。有两处归一化在比较发生之前就把信息删掉了。

**（a）`--format paths` 在箭头处截断。** 每条条目都被 `\s+->\s+.*$` 剥掉尾部，于是
`a.md -> missing docs/en/a.md` 与 `a.md -> missing docs/zh-CN/a.md` 变成同一条 `a.md`。同一路径上的两种
不同失败成了一条，第二种永远不会被当作 regression。

**（b）带判定词前缀的行被整条丢弃。** 任何以 `PASS`、`FAIL`、`OK`、`Ran `、`FAILED`、`NO TESTS` 开头的行
都被当作摘要跳过——包括 `OK 00-governance/a.md has no counterpart`，那是一条约莫真实的违规条目。

### 改了什么

- 条目保留被包裹门禁为其打印的全部内容，只去掉 `NNN. ` 前缀。
- 只有"像判定词开头且不指名任何仓库对象"的行才算摘要。`OK <path> …` 是条目；`OK`、`PASS`、
  `FAILED (failures=2)`、`Ran 12 tests in 0.031s`、`GOV-DOC-001 full scan: … violations.` 仍是摘要。
- 前缀判断加了词边界，因此 `OK_STATUS` 是条目而不是摘要。
- 由于基线条目按设计就是裸路径（`gates.yml` 与 `14-ai-development/ci-gates-and-ratchets.en.md` 都记录了
  `sed -E 's/ -> .*$//'` 这条再生成命令），一条裸条目现在只覆盖**一条**以 `"<path> -> "` 开头的条目，
  而不是该路径上的所有条目。同一路径两种细节现在需要两条基线条目，第二条就是 regression；某路径的
  条目全部消失仍然算 `fixed`。

### 在本树上实测

随仓库发布的基线依然精确匹配，所以必检上下文 `bilingual` 的颜色不变：

```
ratchet: baseline=77 current=77 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.    (exit 0)
```

同一条命令跑在修复前的脚本上也是 exit 0、四个数字相同：该缺陷在今天的输出里不可见，这正是它需要
夹具来钉住的原因。

### 夹具证明（`scripts/ci/test_gate_ratchet.py`）

| 夹具 | 修复前 | 修复后 |
|---|---|---|
| 基线 `a.md`；门禁打印 `a.md -> m1` 与 `a.md -> m2` | `current=1`，PASS（两种失败并成一条） | `current=2`，exit 1，恰好一条 regression 指出 `a.md -> m2` |
| 基线 `a.md -> x`；门禁打印 `a.md -> y` | `current=1` 的裸 `a.md`，一条 regression 加两条 stale | 一条 regression，指出新的细节 |
| 空基线；门禁打印 `OK 00-governance/a.md has no counterpart` | `current=0` → "exited 1 without printing any item" | `current=1` → regression 指出该行 |
| 门禁只打印 `PASS`、`OK`、`FAILED (failures=2)`、`Ran 12 tests …`、full-scan 计数行 | 无条目 → 崩溃守卫 | 无条目 → 崩溃守卫（不变） |

## 3. 测试

`scripts/ci/test_gate_ratchet.py`：7 个测试 → 14 个。在修复后的脚本上全部通过，且新增的 7 个是可证伪的：
其中 6 个在修复前的 `gate_ratchet.py` 上失败（第 7 个钉住必须保留的行为，它只在条目保真断言上不同，
其前提本身不是缺陷）。

`scripts/test_check_source_revision_pointers.py`（新增）：5 个测试。在修复后的脚本上全部通过；在修复前的
脚本上 5 个全部失败。由于修复前的脚本既没有 `--root` 也没有 `scan()`，两处指针缺陷另外做了端到端证伪：
把修复前脚本放进夹具仓库的 `<root>/scripts/check_source_revision_pointers.py` 位置，在同一批字节上跑出
了上面夹具表的那两行，随后修复后脚本在同样字节上通过。

新测试文件是可达的：它被加进 `.github/workflows/repository-hygiene.yml` 里已有的
"Run unreachable self-checks from the repository root" 列表，`scripts/ci/check_test_reachability.py`
报 `66 test files, 66 reachable`。

## 4. 本记录不声称什么

- 没有任何必检上下文变色。`bilingual` 仍是同一个 ratchet，仍是同样 77 条条目。
- `scripts/check_source_revision_pointers.py` 没有被接进任何 workflow，它在 `gate-wiring.txt` 里的基线
  条目也没有被删。
- 两份双语基线都没有被编辑、下调或再生成。
- 脚本报出的 8 条 STALE 指针与 6 条可移动引用保持原样。让门禁变红是本次修复；让仓库变干净是另一个
  工作项。
- `gate_ratchet.py` 的 `--format schema` 分支仍然无人调用。它自己的 ponytail 注记要求在下次改动该文件时
  一并删除；但那会改变 `gates.yml` 传入的命令行，更适合作为独立改动。
- `scripts/ci/baselines/gate-wiring.txt` 里的注释仍写着该脚本在 main 上因"8 STALE pointers"而失败。现在它
  带着 14 条失败记录失败。基线文件未被编辑，因此该注释低估了运行结果；本段就是记录在案的更正。
