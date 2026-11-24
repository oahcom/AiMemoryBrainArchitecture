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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure came from a run in this session at main 2059c8105. The suite figures are the unittest summary lines before and after, run in a throwaway worktree C:/tmp/w900. The two mutation results are the same suite after patching scripts/check_bilingual_docs.py in that worktree, restored and re-run afterwards to confirm OK. The mirror audit enumerated every docs/en path against docs/zh-CN with git ls-tree and compared git show blobs byte for byte. The admission result is is_allowed_new_path() called directly on that tree."
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
    en: "docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
---

# GOV-REV-2026-11-24-FOUR-CORRECTIONS-033

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 2059c8105`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. 四条更正，三条打在我自己身上

本文件写在 `REGISTER-INDEX-031` 与 `DISPATCH-CHANNEL-CLOSED-032` 合并后一小时内。合并期间主干前进了三支，其中一支直接拆掉了我在 030 上引用的事实。

| # | 我此前写的 | 现在的实测 | 判定 |
|---|---|---|---|
| 1 | 030 §4/§6：52 个测试、24 个问题、无 workflow 运行 | `Ran 52 tests / OK`；`bilingual-docs.yml:27` 已运行 | **已被 `aaf6da966`（#892）修掉** |
| 2 | 「24 个问题」的存在意味着套件不能被杀 | 两个变异测试都杀掉了它 | **我的推断错**：它是能失败的 |
| 3 | 032 §6：把该工单保留待放行 | 工作已完成，工单内容作废 | **我保留的东西已无对象** |
| 4 | GAP-24：zh-CN 镜像是英文文件 | 123 对里 2 对逐字节相同，**方向相反** | **GAP-24 少算且只描述了一个方向** |

032 §1–§5（发派通道关闭）不受影响，§3 重新验证仍在。

---

## 2. 030 §4 与 §6 已被修掉，且修得对

`aaf6da966`（#892，2026-11-24 13:49:49 +0800）在我测量之后合入。同一台机器、同一条命令：

| 时点 | 输出 |
|---|---|
| `main` `ef7266db`（我测量时） | `Ran 52 tests in 72.708s` / **`FAILED (failures=3, errors=21)`** |
| `main` `2059c8105`（现在） | `Ran 52 tests in 35.976s` / **`OK`** |

它的提交信息把根因写对了，而且写得比我准：`REPO_ROOT` 在第 24 行定义，`ROOT = REPO_ROOT` 在第 170 行是一次**普通赋值而不是代理**，所以重绑一个名字另一个仍指向真实检出。两个名字已经漂成两种用途——文件存在性与配对逻辑读 `ROOT`，而**每一处** `subprocess.run(..., cwd=...)`、`BASELINE_PATH`、两个 import-time 检查读 `REPO_ROOT`。

§6 也一并修掉：`bilingual-docs.yml:27` 现在运行该套件，且放在真实闸门之前，理由写在提交信息里——「a fixture-only failure cannot be mistaken for a document problem」。这比我原本要派工单写的「加进 hygiene 的显式列表」更好：它挂在 `GOV-DOC-001 structural checks` 这个 required context 上，而不是挂在另一个 job 的时长里。

**所以 `AID-2026-055` 不需要登记了。** 032 §6 保留的那份内容（对象、依据、七条验收）现在指向一件已完成的工作。我不删除 032 的 §6——它记录了当时的判断，而判断当时是对的——但本文件声明它作废。

---

## 3. 我对「24 个问题」的推断是错的：套件能被杀

030 §4 说 24 个失败「不会在任何地方变红」。我据此推断这套测试对被它守护的控制是钝的，并在 032 §6 写了两个变异测试要求。**推断错了**：24 个问题来自 helper 读错仓库，而不是来自断言恒真。

在 `main 2059c8105` 上，对 `scripts/check_bilingual_docs.py` 做两次变异，各跑一次 52 个测试，再还原：

| 变异 | 结果 | 判定 |
|---|---|---|
| 基线（未变异） | `Ran 52 tests in 25.117s` / **`OK`** | — |
| 甲：删掉 `and not partial_side_by_side` | `Ran 52 tests in 21.868s` / **`FAILED (failures=1)`** | **KILLED** |
| 乙：把每处 `cwd=ROOT` 换回真实检出（重造半覆盖 bug） | `Ran 52 tests in 97.701s` / **`FAILED (failures=8, errors=11)`** | **KILLED** |
| 还原后 | `Ran 52 tests in 16.828s` / **`OK`** | — |

两条都有明确的数字，不是「跑了一下没问题」。

**这对 `AID-2026-054` 有直接后果。** `ERRATUM-01` 的判据 11 要求「删掉 `and not partial_side_by_side` 后至少一个测试失败，并贴出失败输出」。该判据在写的时候是**不可满足**的——`PARTIAL_SIDE_BY_SIDE_PAIRS` 当时没有能生效的测试。现在可满足，且安全边际是 1 个失败：`ERRATUM-01` 的 C 项（加判据 11）由此从「提出要求」变成「要求可被执行」，但 1 个失败也是**薄**的——任何进一步削弱该断言的改动仍可能把它抹掉。判据 11 应改为要求「至少 1 个失败且该失败断言的是 `PARTIAL_SIDE_BY_SIDE_PAIRS` 语义」，而不只是「有测试变红」。

---

## 4. GAP-24 少算了一对，而且只描述了一个方向

以 `git ls-tree` 枚举主干上所有 `docs/en/<P>` 与 `docs/zh-CN/<P>` 同时存在的 `<P>`，逐对比对 blob：

| 类别 | 判据 | 数量 |
|---|---|---|
| **IDENTICAL** | `en` 与 `zh-CN` 逐字节相同 | **2** |
| **ZH_EMPTY** | 不同，且 `zh-CN` 零个 CJK 字符 | **2** |
| **ZH_THIN** | 不同，`zh-CN` 有 1–99 个 CJK | **3** |
| **REAL** | 不同，`zh-CN` ≥100 个 CJK | **116** |
| 合计 | — | **123** |

只有 2 对逐字节相同，也就是 123 分之 2。这个比例说明问题不是普遍的，GAP-24 的框架应该按「个别文件」而不是「一类文件」来读。

**但这两对的方向相反，而 GAP-24 只写了其中一个方向：**

| 文件 | 字节 | CJK | 根文件是 | 镜像问题 |
|---|---|---|---|---|
| `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023.md` | 12181 | **0** | 英文 | `docs/zh-CN/` 是英文副本 —— **GAP-24 描述的就是这一种** |
| `GOV-REV-2026-11-21-PR425-001.md` | 7390 | **1057** | **中文** | `docs/en/` 是**中文**副本 —— **反方向，GAP-24 没有这一种** |

`GOV-REV-...-PR425-001.md` 的三个位置（根、`docs/en`、`docs/zh-CN`）md5 完全相同，内容是一份中文技术审查记录。它的 `docs/zh-CN/` 是**真中文**；错的是 `docs/en/`——一个打开 `docs/en/` 期待英文的读者会拿到 1057 个 CJK 字符的中文。

后果是 GAP-24 §3 提的检查 (a)（`md5(zh-CN) == md5(source)` 即报错）**当检测器仍然对**——它会抓到 2 个文件——**但它的描述会把 425 这一对归错**：那一对的 `zh-CN` 没有问题，问题在 `docs/en/`。检查必须写成方向无关（「任一侧是另一侧的逐字节副本」），并且两对的补救不同：

- `023`：补一份真的中文，或把它从 `docs/zh-CN/` 撤下并登记豁免。
- `PR425-001`：根文件是中文，`docs/zh-CN/` 合法，`docs/en/` 才是缺英文的那一侧。

**GAP-24 的计数因此要更正为 2，不是 1；而「zh-CN 镜像是英文文件」这句话只对其中 1 对成立。**

---

## 5. 032 §1–§5 不受影响，已重新验证

#892 没有碰准入白名单：`scripts/ci/check_repository_hygiene.py` 最近两次改动仍是 `cfcafc98a`（#844）与 `e798b1a72`。在当前主干上直接调用该函数：

```
is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')  -> False
is_allowed_new_path('14-ai-development/governance-register/X.md')                -> True
```

所以「新的工作单无法登记」仍然成立，只是**现在没有工作单想被登记**。这两件事同时为真并不矛盾——通道关着，而最后一件想走通道的活儿刚被别人用另一条路做完了。

---

## 6. 本文件不主张什么

- 不主张 #892 需要回退。它修得比我要求的更好。
- 不主张 030 应当关闭。它的 §4/§6 已被修掉，§1–§3、§5、§7 的状态我不重测，`register_closure` 也不在本次授权内。
- 不主张 GAP-24 的白名单不需要管。我只更正它的计数与方向；它的 `docs/zh-CN/` 方向对 `023` 完全成立。
- 不主张 2 个逐字节相同就是全部。我只测了 `docs/en` 与 `docs/zh-CN` 同时存在的 123 对；并排配对（`X.en.md` / `X.zh-CN.md`）与只有单侧镜像的文件不在本次枚举内。
- 不指派独立审查。席位 `NOT_ASSIGNED`，本文件不能填。

**阻断链：** 独立审查 `NOT_ASSIGNED`，实施授权 `NOT_AUTHORISED`，sponsor / accountable owner `NOT_ASSIGNED`。

---

## 7. 复现

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  2059c8105

# 1. 套件现在全绿
git worktree add --detach <tmp> origin/main
cd <tmp> && python -m unittest scripts.governance.evidence.test_gate_normative_roots
-> Ran 52 tests / OK

# 2. 它能被打红
#    把 `and not partial_side_by_side` 从 current_bilingual_gaps() 删掉，重跑
-> FAILED (failures=1)
#    把每处 `cwd=ROOT` 换成 pathlib.Path(__file__).resolve().parents[1]，重跑
-> FAILED (failures=8, errors=11)

# 3. 它现在被 CI 运行
grep -n 'test_gate_normative_roots' .github/workflows/bilingual-docs.yml
-> 27:        run: python3 -m unittest scripts.governance.evidence.test_gate_normative_roots

# 4. 镜像审计
#    枚举 docs/en/P 且 docs/zh-CN/P 同时存在的 P，比对 git show 的 blob
-> 123 pairs; IDENTICAL 2, ZH_EMPTY 2, ZH_THIN 3, REAL 116
#    两对逐字节相同的 CJK 计数分别是 0 与 1057

# 5. 准入仍拒绝工作单
python -c "import check_repository_hygiene as h; print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml'))"
-> False
```
