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
      last_verified_date: "2026-11-23"
      last_verification_note: "§8.1 的四个数字（86 个配对、最短一侧 1364 字符、0 个零字节伙伴、0 个逐字节相同配对）均在 2026-11-23 于 880e6a78 全树枚举得出，非抽样。§8.4 的 CI 前提更正依据首次真实执行的 run id，见 GOV-NC-2026-11-23-EXECUTION-RESTORED-029。"
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
    source: null
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-PAIRING-RESIDUAL-013.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-PAIRING-RESIDUAL-013.md"
---

# GOV-NC-2026-11-21-PAIRING-RESIDUAL-013

**Status:** `DISPATCHED` — §3.1–§3.3 authorised as `AID-2026-054` (see §8); §1 and §2 out of scope. Independent review remains `NOT_ASSIGNED`.
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = f687346cd0` (also reproduced at `e236193824`)
**Supersedes:** nothing. **Extends:** `GOV-NC-2026-11-21-SPLIT-DOMAIN-011.md`.
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. Purpose and boundary

Register 011 established that the bilingual gate has two judgement domains that disagree. Between 011 and this measurement, four PRs landed (#487, #486, #485, #491). This register re-measures the residual state and answers one question:

> After the recent merges, which parts of 011 still hold, which were fixed, and which new weaknesses appeared?

**This register proposes no fix and changes no code.** It records what `f687346` actually does.

---

## 0.1 Corrections to my own earlier statements

Two claims from my previous rounds are **withdrawn or corrected here**. Both were measurement-harness defects, not repository defects.

| # | Earlier claim | Status | Cause |
|---|---|---|---|
| C-1 | "PR #470 wrote a GitHub API JSON body into `scripts/bilingual-baseline.txt`" | **WITHDRAWN** (already in 011 §0.1) | `GET /git/blobs/{sha}` returns `{"content":"<base64>"}`; my `fetch_blob()` stored the wrapper verbatim |
| C-2 | "7 three-file (ambiguous) side-by-side groups exist" | **WITHDRAWN (this round)** | my inventory grouped by stem only, not by `(directory, stem)`; seven unrelated `README.md` files in different directories were merged into one false group. Correct count is **0** |
| C-3 | "`14-ai-development/AI-EXEC-001.md` edit returns `rc=0`, so the 14 root passes" | **CORRECTED** | that single-file edit correctly returns `rc=1`; the passing case requires **both** sides (`AI-EXEC-001.md` + `docs/en/.../AI-EXEC-001.md`) and does return `rc=0` |

C-2 and C-3 matter because both, taken at face value, would have inflated the defect count. A register that overstates its findings is as unusable as one that understates them.

---

## 1. What #487 fixed, and what it did not

`#487` (`fix(bilingual): accept short Chinese side-by-side translations`, merge commit `18b1c574`, `+13 −4` in `scripts/check_bilingual_docs.py`) added a second content predicate:

```python
def _has_any_chinese(source: str) -> bool:
    """Return True when a source contains at least one CJK Unified Ideograph."""
    ...
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)

def _side_by_side_bilingual(source: str) -> bool:
    """True when `source` has a side-by-side partner and the pair carries Chinese."""
    partner = side_by_side_partner(source)
    if partner is None:
        return False
    return _has_any_chinese(source) or _has_any_chinese(partner)
```

### 1.1 Fixed: the half-mirror regression from 011 §3 is gone

| Case | `0ca4d93` | `cb04524` (011) | **`f687346` (now)** |
|---|---|---|---|
| `02-domain-model/hm.md` (Chinese) + `docs/en/hm.md`, **no `docs/zh-CN`** | GAP | **accepted** | **GAP again** |

Measured: adding only `docs/en/` now produces `New bilingual gap: 02-domain-model/hm.md`. The `english.is_file() and _carries_chinese(source)` branch is once again gated on `root_name == "14-ai-development"`.

### 1.2 Fixed: short genuine translations are accepted

| Case | Result |
|---|---|
| `short.md` (≈5 Chinese characters) + `short.zh-CN.md` | **accepted** |

### 1.3 Not fixed: the split between the two domains

`check_normative_pairing()` is byte-identical to 011's quote:

```python
en = f"docs/en/{source}"
zh = f"docs/zh-CN/{source}"
errors.extend(check_counterpart_requirement(source, [en, zh], changed, statuses, exception))
```

The `if source.startswith("14-ai-development/")` branch at line 738 is the only path that consults `counterpart_14()`. Every other root still demands **both** `docs/` mirrors.

---

## 2. The residual defect, measured on `f687346`

`BASE_SHA` = real parent commit, `HEAD_SHA` = the commit under test, `PR_BODY` = `BILINGUAL-MANIFEST: COMPLETE`.

### 2.1 Every live side-by-side pair outside the 14 root is blocked

Inventory, grouping by `(directory, stem)`:

| Root | side-by-side groups | live (non-exempt) | three-file |
|---|---|---|---|
| `00-governance` | 0 | 0 | 0 |
| `01-system-architecture` | 0 | 0 | 0 |
| `02-domain-model` | 1 | 1 | 0 |
| `04-memory-compiler` | 0 | 0 | 0 |
| `06-memory-context` | 2 | 2 | 0 |
| `07-agent-integration` | 1 | 1 | 0 |
| `08-bmcp-protocol` | 1 | 1 | 0 |
| `13-engineering-decisions` | 0 | 0 | 0 |
| `14-ai-development` | 18 | 15 | 0 |
| **total** | **23** | **20** | **0** |

**5 live pairs sit outside the 14 root. All 5 return `EXIT=1` when both sides are edited:**

| Pair (both sides touched) | Result | Errors |
|---|---|---|
| `02-domain-model/phase-2-domain-extension` | `EXIT=1` | 2 × `requires all counterparts changed` |
| `06-memory-context/context-implementation-coverage` | `EXIT=1` | 2 |
| `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract` | `EXIT=1` | 2 |
| `07-agent-integration/adapter-capability-tiers` | `EXIT=1` | 2 |
| `08-bmcp-protocol/protocol-index` | `EXIT=1` | 2 |
| **passes** | **0 of 5** | |

### 2.2 The control that isolates the cause

| Case | `EXIT` |
|---|---|
| new `02-domain-model/pn.md` + `pn.zh-CN.md` (side-by-side) | **1** |
| new `02-domain-model/pm.md` + `docs/en/pm.md` + `docs/zh-CN/pm.md` (mirror triple) | **0** |
| new `08-bmcp-protocol/pq.md` + `pq.zh-CN.md` (side-by-side) | **1** |
| new `14-ai-development/pr.md` + `pr.zh-CN.md` (side-by-side) | **0** |
| existing `14-ai-development/AI-EXEC-001.md` + `docs/en/.../AI-EXEC-001.md` | **0** |
| existing `14-ai-development/AI-EXEC-001.md` **alone** | **1** |
| new `02-domain-model/ps.md` alone | **2** |

The same file shape passes in one root and fails in another. The discriminator is `source.startswith("14-ai-development/")`, not the bilingual policy.

### 2.3 The only pass path is to register a correct pair as a defect

A seven-field `BILINGUAL-EXCEPTION: APPROVED` in the PR body returns `EXIT=0` while the gate still prints *"human governance approval remains mandatory"*. For the 5 pairs above, the sole way to edit them on main is to declare them defective.

---

## 3. Three content-predicate weaknesses (new, measured this round)

`#487` widened acceptance to *any* CJK character. That was the intended fix for short translations, but it also sets the floor at one character.

### 3.1 One CJK character anywhere is enough

```
02-domain-model/c1.md          = "# Title\n\nThis is English.\n\n一\n"
02-domain-model/c1.zh-CN.md    = "# Title\n\nThis is English.\n\n一\n"
-> new gaps: []      (ACCEPTED as a bilingual pair)
```

Two files, both essentially English, each containing the single character `一`, satisfy the gate.

### 3.2 A zero-byte partner is enough

```
02-domain-model/c3.md          = 30 lines of Chinese
02-domain-model/c3.zh-CN.md    = "" (0 bytes)
-> new gaps: []      (ACCEPTED)
```

`_has_any_chinese(source) or _has_any_chinese(partner)` is satisfied by the source alone. The partner never has to contain anything.

### 3.3 Asymmetry and non-idempotence in `side_by_side_partner`

The function returns the first candidate that exists, in a fixed suffix order, with no uniqueness check and no symmetry check. With three files present:

```
02-domain-model/t1.md         -> 02-domain-model/t1.en.md
02-domain-model/t1.en.md      -> 02-domain-model/t1.zh-CN.md
02-domain-model/t1.zh-CN.md   -> 02-domain-model/t1.en.md

partner(partner(t1.md)) = t1.zh-CN.md  ≠  t1.md     (not symmetric)
```

All three files are nonetheless reported as paired. This is the exact condition spec §4.5.2 R-2 was written to reject.

---

## 4. What is *not* a defect

| Case | Result | Correct? |
|---|---|---|
| both sides identical English, zero CJK (`c2.md` + `c2.zh-CN.md`) | both are GAPs | yes |
| `c6.en.md` (EN) + `c6.md` (EN), no CJK anywhere | both are GAPs | yes |
| cross-directory same stem: `02/x.md` + `08/x.zh-CN.md` | both are GAPs | yes |
| P3 coexistence: `c5.md` + `c5.zh-CN.md` + full mirror | accepted | yes |
| full mirror triple in a non-14 root | `EXIT=0` | yes |
| `14` single-file edit without its mirror | `EXIT=1` | yes |

The gate is not uniformly permissive. Its content check is weak at the floor and its scope check is wrong outside the 14 root. Those are separate problems and should be fixed separately.

---

## 5. Test execution on `f687346`

```
CC=<zig cc wrapper> AR=<zig ar wrapper> CARGO_TARGET_DIR=<external> cargo test --workspace
-> 26 binaries, 218 passed, 0 failed, 0 ignored
```

Up from 182 passed / 25 binaries at `cb04524` (register 012). `e2e_negative_paths` (5) and the strengthened `memory-context` suite account for part of the increase.

**This does not upgrade any acceptance claim.** `GOV-REV-2026-11-21-PR425-001.md` proved mutant M3 survives; passing tests are not effective tests. Coverage and mutation score remain unmeasured.

---

## 6. Reproduction

```
repo:   oahcom/AiMemoryBrainArchitecture
commit: f687346cd0   (also reproduced at e236193824)
gate:   scripts/check_bilingual_docs.py
run:    BASE_SHA=<parent> HEAD_SHA=<commit> PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
        python scripts/check_bilingual_docs.py
```

Every table above is produced by that invocation plus file creation; no step requires network access or CI.

---

## 7. What this register does not claim

- It does not claim the 5 blocked pairs *should* be editable — that is a policy decision for the accountable owner.
- It does not claim `#487` was wrong; it fixed a real problem and introduced a lower floor.
- It does not claim the 14 root is exempt by policy; it observes that the 14 root is exempt *in code*.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.
- It does not assert CI ran. CI still returns `steps=0` for every job (register 005).

**Status of the blocking chain is unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 8. 实施派发：§3 的三个缺陷已授权修复（2026-11-23）

本登记正文与 §3 的三条实测**不改动**。§3.1、§3.2、§3.3 在 `f687346c` 上为真，记录保留。

| 项目 | 内容 |
|---|---|
| 工作令 | `AID-2026-054`（`14-ai-development/work-items/AID-2026-054/`） |
| 派发依据 | 本登记 §3.1、§3.2、§3.3；裁定 `OWNER-DECISION-EMBEDDED-BILINGUAL-001` §4 |
| 实施范围 | `scripts/check_bilingual_docs.py` 的 `_side_by_side_bilingual()` 与 `side_by_side_partner()`，以及由改动决定的 `scripts/bilingual-baseline.txt` |
| 明确不授权 | §1 的 5 个被阻断配对（属登记 011）、§2 的 diff 域策略、本登记关闭 |

### 8.1 §3.1 与 §3.2 的修复阈值是标定出来的，不是选出来的

本登记 §3.1 测到「任意一个 CJK 字符即通过」，§3.2 测到「0 字节伙伴即通过」。两处都需修，但**修多严**不是偏好问题：

| 度量 | 值 |
|---|---|
| 树中已被接受的并排配对 | **86** |
| 最小配对中较短一侧的字符数 | **1,364** |
| 伙伴为 0 字节的配对 | **0** |
| 两侧逐字节相同的配对 | **0** |

全部 86 个真实配对的较短一侧都在 1,364 字符以上，最短的十个落在 1,364–2,214。所以 **1 到 400 之间任何阈值都不会误伤这 86 个**。裁定取 100，理由只有一个：`_carries_chinese()` 已经在用 100 做同一件事。

同时要求两种文字都有实质内容（`cjk >= 100` 且 `latin >= 1000`）。只数 CJK 会放过一份纯中文文件，那是本登记 §3.1 的同一个单侧缺陷，只是换了位置。

### 8.2 §3.3 是不成立的潜伏缺陷，仍然要修

§3.3 的三文件不对称（`partner(partner(x)) != x`）当前**不可触发**：实测全树 0 个源文件同时存在 `.en.md` 与 `.zh-CN.md`。它仍然被纳入授权，因为不可触发只在今天成立——有人在一个已有 `.zh-CN.md` 的文件旁边加一个 `.en.md`，它立刻可触发。修一条永远走不到的路径成本低于在它被走到之后再去查为什么三个文件都说自己配对了。

### 8.3 为什么状态不是 CLOSED

§3 是三个**内容谓词**缺陷，修完它们不改变 §1 与 §2：

- §1 的 5 个被阻断配对属于登记 011 的 diff 域策略，与谓词无关，本次不动。
- §2 的 143 行结论（基线可被外来锚点膨胀）已由登记 014 §7 实测为已修复且无护栏，与本登记不同。
- 本登记 §7 明确不指派独立审查席位，该席位仍为 `NOT_ASSIGNED`；写谓词的会话不能为自己的谓词提供独立性。

`OPEN` → `DISPATCHED — §3 已授权（AID-2026-054）；§1、§2 不在范围内；独立审查仍 NOT_ASSIGNED`。

### 8.4 一处必须更正：§7 依赖了一个已失效的前提

§7 末条写着「CI 仍对每个 Job 返回 `steps=0`（登记 005）」。**这句话已经过期。** 实测首次真实执行为 2026-11-22，详见 `GOV-NC-2026-11-23-EXECUTION-RESTORED-029`。

这不改变本登记的任何数字——§3 的每条都是本地 `python scripts/check_bilingual_docs.py` 测出来的，不依赖 CI。但它改变**这条限制的含义**：当时的意思是「CI 不执行，所以本地测量是唯一证据」；现在的意思是「CI 会执行，但执行了不等于可信」。后者的限制更弱，不应再被引用为前者的依据。
