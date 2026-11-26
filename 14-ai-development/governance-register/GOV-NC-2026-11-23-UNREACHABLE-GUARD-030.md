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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure was measured on 2026-11-23 at main f39dfb7b: §2 by replaying main's normative_changes construction over all 552 tracked normative paths; §3 by enumerating extensions over the same set; §4 and §5 by running the suite at 9944d07e and at 8ab40fb4 in a detached worktree; §6 by grepping .github/ for the suite name. No figure is carried over from another register."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-23-UNREACHABLE-GUARD-030.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-23-UNREACHABLE-GUARD-030.md"
---

# GOV-NC-2026-11-23-UNREACHABLE-GUARD-030

**Status:** `OPEN` — `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = f39dfb7b`
**Extends:** `...-SUFFIX-SCOPE-017.md`, `...-CWD-SPLIT-014.md`
**Register author:** owner-proxy session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. 两件事：一件已被修掉，一件是修出来的

本登记回答 `SUFFIX-SCOPE-017` 的现状，并记录在核对该现状时发现的、由修复本身造成的缺陷。

| | 结论 |
|---|---|
| 017 的缺陷（`.json` 被要求双语镜像） | **已修复** — `717dfbf0`，2026-11-21 22:09:16 +0800，PR #527 |
| 修法是否等于 017 §5 提出的方案 | **否**。017 提的是「把后缀过滤器变成 root-agnostic」；实际做的是「把上游的 `normative_changes` 收窄为只有 `.md`」 |
| 修复的代价 | `PAIR_ENFORCED_SUFFIXES` 变成**死代码**；normative roots 下 167 个非 `.md` 文件全部退出配对检查 |
| 修复自带的 3 个测试 | **全部失效**，失效原因来自 `8ab40fb4`（登记 014 的修复） |
| 登记 014 §7.3 对此的解释 | **错误**，见 §5 |

---

## 1. 017 在它自己的测量点上为真，80 分钟后被修掉

017 测于 `d647e7d5`（2026-11-21 20:48:30 +0800）。当时 `main` 的判定链是：

```python
if Path(path).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}:
    normative_changes.append(path)
```

`717dfbf0`（22:09:16 +0800，80 分钟后）把它改成：

```python
if Path(path).suffix.lower() == ".md":
```

一行，`+1 −1`，同一 commit 加了 3 个测试（`+71`）。**该 commit 的提交信息没有提到 017**；全仓 `grep SUFFIX-SCOPE-017` 除本登记自身外零命中。这与 014 §7.4 记录的是同一种失效模式：修了，但没有回指。

## 2. 修法与 017 §5 的第三个分支不同，而差别是实质的

017 §5 列出三种「这就不是问题」的状态，第 3 种是「后缀过滤器本应 root-agnostic」。若按此修，`PAIR_ENFORCED_SUFFIXES` 会被移到两个分支都读得到的位置：`.md` 继续受配对约束，`.json` 不受。

实际修法把整个 `normative_changes` 收窄成只有 `.md`。后果是 `check_normative_pairing()` 现在永远收不到非 `.md` 文件，因此第 1031 行那个后缀守卫再也不可能触发。实测（按 main 的构造逻辑重放全树 552 个 normative 路径）：

```
normative_changes 候选   384
其中非 .md                 0
=> 后缀守卫可触发次数       0
```

`PAIR_ENFORCED_SUFFIXES = {".md"}` 仍在第 41 行声明，仍被第 1031 行读取，但**它已经是一个恒真判断**。代码读起来像「只对 Markdown 要求配对」，实际执行的是「只有 Markdown 会到达这里」——这两句话不同，而第二句没有被任何注释写下来。

## 3. 代价：167 个文件退出配对检查，其中 0 个曾有过镜像

| 类型 | 数量 | 例 |
|---|---|---|
| `.json` | 59 | `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` |
| `.py` | 54 | `08-bmcp-protocol/runtime_reference/*.py` |
| `.yaml` | 47 | `00-governance/architecture-document-metadata.schema.yaml` |
| `.mjs` | 4 | — |
| `.txt` / `.log` / 无扩展名 | 4 | — |

`docs/en/` 与 `docs/zh-CN/` 下的非 `.md` 文件数：**0**。

所以 017 的判断——「JSON schema 无法为自己提供 Markdown 译文，要求它是不满足的」——在修复后**依然成立**；修复只是把这条要求从「不满足」变成「不检查」。结果上这是对的：一个无法满足的要求，撤销它比留着它更诚实。**本登记不主张回退。**

但它留下两件事没有答案：

1. **`.yaml` 与 `.json` 是数据，`.py` 不是。** 一个 schema 与一个校验器在「是否需要中文说明」上不是同一类问题，而它们现在共享同一个豁免。017 §7 已声明「不主张 JSON schema 无需双语处理」，本次收窄把这句话的适用范围扩大了，而没有记录扩大到了哪里。
2. **`00-governance/architecture-document-metadata.schema.yaml` 是治理元数据 schema 本身**，它在 `EMBEDDED_BILINGUAL_SOURCES` 里（21 条之一），本就有豁免理由；另外 46 个 `.yaml` 没有。

## 4. 修复自带的 3 个测试全部失效，而失效由登记 014 的修复造成

`717dfbf0` 加的 3 个测试都走 `_run_real_git_gate_for_change()`：在临时目录里 `git init`、提交，再断言闸门判定。它们依赖这个 helper：

```python
def load_gate(root: Path):
    mod.ROOT = root          # 指向临时仓库
    return mod               # REPO_ROOT 未改动
```

`8ab40fb4`（2026-11-22 10:37:32 +0800，登记 014 的修复）把 `changed_status()` 的 `cwd=ROOT` 改成 `cwd=REPO_ROOT`。于是 helper 建的临时仓库再也不会被读取：

```
load_gate(root=tmp) 之后
  ROOT      = ...\Temp\tmpjv6rdbdy
  REPO_ROOT = <真实仓库>            <- changed_status() 读这个
```

`git diff A...B` 于是在**真实仓库**里跑两个只存在于临时仓库的 SHA，退出 128：

```
fatal: Invalid symmetric difference expression edf87e7b...3d443bfb
```

时间线是硬的：

| commit | 时间 | 该套件 |
|---|---|---|
| `9944d07e`（#534，补 `sys.argv`） | 2026-11-21 23:36 | `Ran 52 tests` / **OK** |
| `8ab40fb4`（登记 014 的修复） | 2026-11-22 10:37 | `Ran 52 tests` / **FAILED (failures=3, errors=21)** |

两者之间只有 `8ab40fb4` 一个 commit 触碰过 `scripts/check_bilingual_docs.py` 或该测试文件。**52 个测试从全绿变成 24 个问题，是 014 的修复造成的。**

## 5. 登记 014 §7.3 的因果解释是错的

014 §7.3 写：

> 那 24 个失败是既有的 Windows 临时路径问题（`run([...], cwd=WindowsPath('C:/Users/ADMINI~1/...'))` 断言匹配不上），与本缺陷无关，且在两种状态下完全一致。

**「完全一致」是对的；「既有」和「与本缺陷无关」是错的。**

- 不是既有的：`8ab40fb4` 之前该套件 52 个全过。
- 与本缺陷直接相关：正是「把 `cwd=ROOT` 改成 `cwd=REPO_ROOT`」这一步——014 的修复本体——让 helper 失效。
- 归因不完整：24 个里只有 1 个是 `WindowsPath` 断言；10 个是 `current_bilingual_gaps()` 的 `git ls-files` 退出 128；11 个是其他；2 个是文件创建身份不可识别。

014 §7.3 的**主结论仍然成立**——缺陷可以在两套测试都不响的情况下回来，因为 `scripts/test_check_bilingual_docs.py`（3 个测试）在修复态与缺陷态都是 `OK`。但支撑它的那段解释需要更正，否则读者会以为那 24 个是历史遗留噪音，从而认为「测试本来就不太绿」。

## 6. 这个套件已由 `GOV-DOC-001 structural checks` 运行（2026-11-25 更正）

本节原文写于 2026-11-23（main `f39dfb7b`）：当时 `grep -rn 'test_gate_normative_roots' .github/` 确实零命中，`.github/workflows/bilingual-docs.yml` 只跑 `scripts/test_check_bilingual_docs.py`。该观察次日被推翻：

- `aaf6da96`（#892，2026-11-24）在同一 workflow 新增一步 `python3 -m unittest scripts.governance.evidence.test_gate_normative_roots`，放在真实闸门之前；job 名为 `GOV-DOC-001 structural checks`，即必需 contexts 之一。
- 同一提交修掉了 §4 的 helper 双根（`ROOT` / `REPO_ROOT`）。2026-11-25 复测：`8ab40fb4` 仍为 `Ran 52 tests` / `FAILED (failures=3, errors=21)`；main `a3a62021` 为 `Ran 52 tests` / **OK**。

所以 §4 的 24 个失败会在该必需 context 变红。它们现已不存在：该套件每个 PR 都跑且为绿。

## 7. 本登记不主张什么

- 不主张回退 `717dfbf0`。017 指出的要求确实不可满足，撤销是对的。
- 不主张 `.py` 需要双语镜像。只指出它与 `.json` 共享豁免这件事没有被记录。
- 不主张回退 014 的修复。`cwd=REPO_ROOT` 是正确的；错的是测试 helper 没跟着改，以及 §7.3 的归因。
- 不指派独立审查席位。该席位为 `NOT_ASSIGNED`。

**阻断链：** 独立审查 `NOT_ASSIGNED`，实施授权 `NOT_AUTHORISED`，sponsor / accountable owner `NOT_ASSIGNED`。

## 8. 复现

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  f39dfb7b

# 1. 后缀守卫不可触发 —— 按 main 的 normative_changes 构造逻辑重放全树
#    输出: 384 candidates, 0 non-.md

# 2. 改一个 .json 现在通过
git checkout -B probe origin/main
# 修改 08-bmcp-protocol/schemas/*.schema.json 一个字符，commit
BASE_SHA=HEAD~1 HEAD_SHA=HEAD PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
  python scripts/check_bilingual_docs.py
-> PASS (1 changed paths inspected)

# 3. 把 717dfbf0 那一行改回去，同一个 probe
-> FAIL
   ::error::08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
     requires all counterparts changed in this PR: ..., docs/en/..., docs/zh-CN/...

# 4. 套件在 8ab40fb4 前后
git checkout 9944d07e && python -m unittest discover -s scripts/governance/evidence \
  -p test_gate_normative_roots.py -q
-> Ran 52 tests / OK
git checkout 8ab40fb4 && (同上)
-> Ran 52 tests / FAILED (failures=3, errors=21)

# 5. 没有 workflow 跑它
grep -rn 'test_gate_normative_roots' .github/
-> (空)
```
