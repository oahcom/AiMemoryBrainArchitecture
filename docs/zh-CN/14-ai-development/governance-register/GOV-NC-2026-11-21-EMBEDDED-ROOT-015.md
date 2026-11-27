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
      last_verification_note: "§9 的四组缺口数（77 / 77 / 11 / 11）在 2026-11-23 于 880e6a78 的临时 worktree 上逐个实测，每组改动后调用 current_bilingual_gaps()。§9.1 的标题并置统计通过读取全部 58 个文件得出，非抽样。"
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-EMBEDDED-ROOT-015.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-EMBEDDED-ROOT-015.md"
    zh-CN: null
---

# GOV-NC-2026-11-21-EMBEDDED-ROOT-015

**Status:** `RULED` — §6 branch 3 is true (see §9); dispatched as `AID-2026-054`. Independent review remains `NOT_ASSIGNED`.
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 67074d2ff7`; re-verified at `8a2ce1b` with the same counts
**Extends:** `GOV-NC-2026-11-21-SPLIT-DOMAIN-011.md`, `...-PAIRING-RESIDUAL-013.md`, `...-CWD-SPLIT-014.md`
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0.1 修订记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1 | 2026-11-21 | 初版。声称 58 条缺口的原因是 Shape 3 被 `root_name == "14-ai-development"` 挡住 |
| **v2** | 2026-11-21 | **更正归因**：Shape 3 需要 `docs/en` 镜像，而这 58 条一条都没有，所以 Shape 3 从来不是原因。真实机制是「门禁没有任何形态承认单文件内嵌双语，只能靠白名单」。见 §3.1、§3.2 |

**v2 的更正很重要**：v1 指向了一个错的修复方向（放宽根名守卫），而那个改动实测对 77 条缺口**零影响**。按 v1 去修会得到「改了很多、什么都没变」的结果。

---

## 0. The finding

The frozen baseline has 77 entries. **58 of them — 75% — are the entire `13-engineering-decisions` root.**

```
13-engineering-decisions  58
06-memory-context         10
14-ai-development          4
08-bmcp-protocol           4
00-governance              1
---
total                     77
```

`13-engineering-decisions` contains exactly **58** `.md` files. **All 58 are gaps. Zero pass.**

This is not a documentation backlog. Those files are bilingual — they carry both languages inside one file. **The gate has no shape that recognises this at all** (§3.2), so the only way such a file can pass is a per-file entry in `EMBEDDED_BILINGUAL_SOURCES`. That list has 21 entries; none of them is in this root.

---

## 1. The files really are bilingual

Sampled directly, without any gate involvement:

```
13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-model.md
  bytes: 16152   CJK chars: 1574   ratio: 12.7%
  first headings:
    # Canonical Domain Model
    # 规范领域模型
    ## 1. Design principles / 设计原则
```

Distribution over all 58 files in the root:

| CJK ratio | files |
|---|---|
| ≥ 5% (clearly embedded bilingual) | **52** |
| ≥ 15% | 3 |
| exactly 0% | 1 |

So **57 of 58** carry substantial Chinese text. The one at 0% is `13-engineering-decisions/technology-architecture-blueprint.md`, which is a genuine single-language file and a genuine gap.

## 2. The root's own audit says so

`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md` is the root's self-audit. Its acceptance rule:

> A file is bilingual-complete only when the full normative content is present in both languages **in the same file/change set**, with semantic parity, stable-ID parity, matching decision status, matching examples/constraints and traceable source revisions.

And its per-file table records, file after file:

```
| canonical-domain-entity-inventory.md | ... | REMEDIATED — MANUAL PARITY REVIEW PENDING |
| canonical-identity-semantics.md      | ... | REMEDIATED — MANUAL REVIEW PENDING |
| canonical-state-semantics.md         | ... | REMEDIATED — MANUAL REVIEW PENDING |
| canonical-temporal-evidence-semantics.md | ... | REMEDIATED — MANUAL PARITY REVIEW PENDING |
```

Every row is `REMEDIATED`. The remediation was performed **inside the file**, which is exactly the shape `_carries_chinese()` was written to detect.

## 3. Why the gate still reports all 58

`current_bilingual_gaps()` accepts exactly three shapes:

| Shape | Condition | Applies to `13-...`? |
|---|---|---|
| 1. mirror | `docs/en/X` **and** `docs/zh-CN/X` both exist | only 3 files have this |
| 2. side-by-side | `X.zh-CN.md` / `X.en.md` sibling | 0 files have this |
| 3. embedded | `docs/en/X` exists **and** `_carries_chinese(X)` | **0 files qualify — see §3.1** |

### 3.1 更正：Shape 3 不是这 58 条的原因

**本登记的 v1 声称「Shape 3 正是匹配这些文件的形态，只是被 `root_name == "14-ai-development"` 挡住」。这个归因是错的。**

Shape 3 的前置条件是 `docs/en/X` 必须存在。实测：

```
77 条缺口中，有 docs/en 镜像的：0 条
13 根的 58 条缺口中，有 docs/en 镜像的：0 条
```

所以即使把根名守卫整个删掉，Shape 3 也**救不了任何一条**。实测确认：

```
M5（删除 root_name == "14-ai-development" 守卫）
BEFORE  gaps=77 baseline=77 new=0 resolved=0
AFTER   gaps=77 baseline=77 new=0 resolved=0
```

缺口一个都没变。这也解释了为什么 M5 变异体能存活而无人察觉——**它守的分支在 77 条基线上从不触发**。

Shape 3 真正服务的范围，实测只有 3 个文件，全在 14 根：

```
14-ai-development/AI-EXEC-001.md
14-ai-development/AI-EXEC-002.md
14-ai-development/AI-EXEC-ROLLOUT-001.md
```

它们同时满足「无 `docs/zh-CN`」「无并排配对」「有 `docs/en`」「含中文」。把守卫删掉后，其他八根里符合这四个条件的文件数是 **0**，所以删掉它今天不改变任何结果——但这不证明它无害，只证明它今天没有载荷。

### 3.2 58 条缺口的真实机制：完全没有任何对应文件

按对应文件的存在性对 77 条缺口分类，结果只有一类：

| 机制 | 条数 |
|---|---|
| 有并排配对 | 0 |
| `docs/en` + `docs/zh-CN` 双镜像齐全 | 0 |
| 只有 `docs/en` | 0 |
| 只有 `docs/zh-CN` | 0 |
| **完全没有对应文件** | **77** |

13 根的 58 条同样如此：`docs/en` = 0，`docs/zh-CN` = 0，并排配对 = 0，其中 57 条含中文。

**因此正确的表述是**：这 58 个文件是**单文件内嵌双语**，而门禁的三种形态**全部要求存在第二个文件**（镜像或并排）。门禁没有任何形态承认「一个文件内部同时承载两种语言」。`EMBEDDED_BILINGUAL_SOURCES` 那 21 条豁免之所以存在，正是因为这个——它们是**逐文件白名单**，不是形态识别。

政策与门禁的矛盾因此比我原来写的更根本：不是「形态存在但被根名挡住」，而是「**这个形态在门禁里根本不存在**，只能靠白名单逐个登记」。00-governance 登记了 12 个，14 根登记了 9 个，13 根登记了 0 个——而 13 根恰恰是内嵌双语最集中的地方（57/58）。

## 4. The exemption list makes the asymmetry explicit

`EMBEDDED_BILINGUAL_SOURCES` has 21 entries, described in the source as "reviewed single-file bilingual sources":

| Root | exemptions |
|---|---|
| `00-governance` | **12** |
| `14-ai-development` | **9** |
| `13-engineering-decisions` | **0** |

Two roots got a per-file exemption review. The third root, whose 58 files were remediated to embedded bilingual by their own audit, got none. Whether that is an oversight or a deliberate decision is not recorded anywhere I could find — and I looked in `00-governance/bilingual-documentation-policy.md`, the parity audit, and the git history for the 13 root.

**The consequence is structural:** 75% of the frozen baseline is one root's documentation that the policy considers complete and the gate considers missing. The ratchet then freezes it forever, because removing an entry is an error (`resolved must be empty`) and adding is an error (`new_gaps must be empty`). The baseline can only shrink by editing the gate — which requires authorisation nobody has.

## 5. What this changes about the other registers

| Register | Claim | Effect of this finding |
|---|---|---|
| 011 | diff domain blocks 5 real side-by-side pairs | unchanged; those 5 are all outside the 13 root |
| 013 | 5 live pairs outside the 14 root, 0 of 5 editable | unchanged |
| 014 | `ROOT = cwd` inflates the baseline 77 → 117 | **worse than reported**: 41 of the 40 added entries would be added on top of an already-75%-wrong baseline |

And a correction to my own framing in 013: I described the baseline as "77 frozen gaps" without asking what they were. **Three quarters of them are one root's embedded-bilingual documentation.** A number that large deserved a breakdown before I used it as a denominator.

## 6. What would have to be true for this to be a non-issue

Any one of these would close it:

1. `13-engineering-decisions` was deliberately excluded from embedded-bilingual recognition, and that decision is recorded. → then the 58 entries are correct and the root should arguably leave `NORMATIVE_ROOTS`.
2. The 58 files are not actually embedded bilingual despite the audit table. → then the audit table is wrong, which is a larger problem.
3. Shape 3 is meant to be root-agnostic and the `root_name ==` guard is a leftover. → then 58 entries are a gate bug, not a documentation debt.

I cannot distinguish these three from the repository. **That is the finding.** A 75% concentration in one root, produced by a hard-coded root name, with a self-audit that says the opposite, is not a state anyone can act on without a decision from the accountable owner.

## 7. Reproduction

```
repo:   oahcom/AiMemoryBrainArchitecture
commit: 67074d2ff7
cwd:    repo root   (register 014: a foreign cwd invalidates this measurement)

python -c "import sys,os;sys.path.insert(0,os.path.join(os.getcwd(),'scripts'));sys.argv=['x'];
import check_bilingual_docs as g, collections;
gp=g.current_bilingual_gaps();
print(collections.Counter(x.split('/')[0] for x in gp))"

-> {'13-engineering-decisions': 58, '06-memory-context': 10,
    '14-ai-development': 4, '08-bmcp-protocol': 4, '00-governance': 1}

find 13-engineering-decisions -name '*.md' | wc -l    -> 58
find docs/en/13-engineering-decisions -name '*.md' | wc -l   -> 3
find docs/zh-CN/13-engineering-decisions -name '*.md' | wc -l -> 3
```

CJK ratio per file requires only reading the file; no gate involvement.

## 8. What this register does not claim

- It does not claim the 58 files should be exempted. That is a policy decision.
- It does not claim the gate is wrong to require mirrors; shape 3's root guard may be intentional.
- It does not propose adding 58 entries to `EMBEDDED_BILINGUAL_SOURCES`. That would be a 58-entry exemption list nobody reviewed.
- It does not claim the parity audit is accurate. I verified CJK presence, not semantic parity — the audit itself says every row is still `MANUAL REVIEW PENDING`.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 9. 裁定：§6 的第 3 个分支为真（2026-11-23）

本登记正文与 §6 的三问**不改动**。§6 说「我无法从仓库里区分这三个分支，**这才是发现**」。本节的职责就是替这个发现做决定，并给出它当时拿不到的那个测量。

裁定文书：`OWNER-DECISION-EMBEDDED-BILINGUAL-001`（`14-ai-development/adr/`）。工作令：`AID-2026-054`。

| §6 分支 | 判定 |
|---|---|
| 1. `13-engineering-decisions` 被有意排除，且该决定有记录 | **假**。不存在这个决定。查过 `00-governance/bilingual-documentation-policy.md`、该根自己的 parity audit、`EMBEDDED_BILINGUAL_SOURCES` 及其历史、该根的 git 历史。 |
| 2. 这 58 个文件其实不是内嵌双语，audit 表是错的 | **对 57/58 为假**。见 §9.1。 |
| 3. Shape 3 本应 root-agnostic，`source.startswith("14-ai-development/")` 是遗留 | **真**。 |

### 9.1 58 个文件确实是内嵌双语，而且比 §1 的证据更强

§1 用的是 CJK 占比（≥5% → 52 个）。占比是个弱证据：一段中文附录也能把比例拉上去。本节改用**标题是否在同一行并置两种语言**（`# Agent Integration Boundary / Agent 集成边界`），因为这才是 policy §3 要求的 parity 形态。

| 度量 | 文件数 |
|---|---|
| 在 ≥50% 的标题里并置两种语言 | **42** |
| 至少一个标题并置两种语言 | **57** |
| 零个双语标题 | **1** |

唯一例外是 `13-engineering-decisions/technology-architecture-blueprint.md`：56 个标题，**49,666 字节里 0 个 CJK 字符**。它是真的单语文件，也是本裁定下唯一应当保留为缺口的证据——留着它，才能证明新谓词不是「什么都放过」。

### 9.2 §3.2 与 §6 的关键更正：删掉守卫测得零变化，是因为守卫根本没被执行

§3.1 记录了 M5 变异：删掉根名守卫，实测 `77 → 77`，因此断言「这个守卫今天没有载荷」。

这个推断错了，而且错在一个可以直接复现的地方。Shape 3 的条件是**两个**：`source.startswith("14-ai-development/")` **且** `english.is_file()`。那 58 个文件失败的是**第二个**——它们没有 `docs/en` 镜像。所以守卫所在的分支从来没被走到，删掉它测到的零变化，与守卫是否存在无关。

本节实测了三个变体，全部在 `880e6a78` 的临时 worktree 上跑 `current_bilingual_gaps()`：

| 变体 | 改动 | 缺口 |
|---|---|---|
| — | `main` 原样 | **77** |
| A | 只删根名守卫，保留 `english.is_file()` | **77** |
| B | 删两者，谓词仍是 `_carries_chinese()` | **11** |
| C（裁定采用） | 删两者，谓词改为「同文件内 CJK ≥ 100 且拉丁字母 ≥ 1000」 | **11** |

变体 A 精确复现了 M5 的 `77 → 77`。所以 M5 的数字是对的，结论是错的：**一个从未被执行的分支，在不在都是零。** 这也解释了为什么 §3.1 那个变异体能存活而无人察觉。

**B 与 C 今天测得同一个 11，但它们不等价。** B 会把「100 个 CJK 字符、零英文」的文件判为双语——这正是 013 §3.1 那个单侧谓词缺陷，只是搬到了内嵌形态上。只有 C 在明天有人提交一份纯中文文档时还成立。两者测得相同，记录为「相同」，不记录为「一致」。

### 9.3 缺口 77 → 11，resolved 66，new 0

| | |
|---|---|
| 变更后缺口 | **11** |
| 从基线中消解 | **66** |
| 新增缺口 | **0** |
| 按根分布 | `06-memory-context` 7、`08-bmcp-protocol` 2、`00-governance` 1、`13-engineering-decisions` 1 |

13 根剩下的那一条是 `technology-architecture-blueprint.md`，符合预期。另 9 条与 13 根无关的消解项已逐条核验，每一条都确实并置了两种语言（最低 105 CJK / 2,107 拉丁字母），它们此前失败的是镜像前置条件，不是语言要求。

**记录一次预测错误，而不是悄悄替换**：本节初稿按文件数推算「77 → 20，减 57」。实测是 11，因为移除镜像前置条件还顺带消解了 13 根之外的 9 条。推算只算了根内，测量覆盖全树。以测量为准。

### 9.4 状态与残留

`OPEN` → `RULED — 分支 3；已派发 AID-2026-054；独立审查仍 NOT_ASSIGNED`。

不写 `CLOSED`：裁定改变了门禁谓词，而写谓词的会话不能为自己的谓词提供独立性；且 §9.3 的基线收缩在实际效果上不可逆——66 条离开基线后，没有任何地方还记录它们曾经被视为缺口，而重新加回任何一条都是棘轮错误。所以这个变更的验证责任比通常更重，不能由派发方自证完成。

不在本登记范围内：`technology-architecture-blueprint.md` 该翻译、该加镜像、还是该移出 `NORMATIVE_ROOTS`——三者都让它继续是缺口，选哪个是文档所有者的决定。
