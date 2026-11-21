# GOV-NC-2026-11-21-EMBEDDED-ROOT-015

**Status:** OPEN — MEASUREMENT ONLY
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
