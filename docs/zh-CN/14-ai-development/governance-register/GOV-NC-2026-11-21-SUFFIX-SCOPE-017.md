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
      last_verification_note: "§8 的结论在 2026-11-23 于 main f39dfb7b 实测：384 个 normative_changes 候选中非 .md 为 0；把 717dfbf0 那一行改回去可在干净 worktree 上复现 §0 记录的错误；套件在 9944d07e 为 52 个全过、在 8ab40fb4 为 24 个问题。全部为本会话实跑，非引用。"
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-SUFFIX-SCOPE-017.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-SUFFIX-SCOPE-017.md"
    zh-CN: null
---

# GOV-NC-2026-11-21-SUFFIX-SCOPE-017

**Status:** `FIXED-CLOSED-BY-OTHER` — fixed in `717dfbf0` (#527) by a different route than §5 branch 3, behaviourally verified (see §8). Its three shipped tests are broken and no workflow runs them. Independent review remains `NOT_ASSIGNED`.
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = d647e7d5ef`
**Extends:** `...-SPLIT-DOMAIN-011.md`, `...-PAIRING-RESIDUAL-013.md`, `...-CWD-SPLIT-014.md`, `...-EMBEDDED-ROOT-015.md`
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. The finding

`PAIR_ENFORCED_SUFFIXES = {".md"}` exists to limit the pairing requirement to Markdown. It is applied **inside the `14-ai-development` branch only**:

```python
for source in normative_changes:
    if source in EMBEDDED_BILINGUAL_SOURCES:      continue
    if source.startswith(PAIR_EXEMPT_PREFIXES):    continue
    if source.startswith("14-ai-development/"):
        if Path(source).suffix.lower() not in PAIR_ENFORCED_SUFFIXES:
            continue                               # <-- suffix filter lives HERE
        partner = counterpart_14(source)
        ...
        continue
    en = f"docs/en/{source}"                       # <-- no suffix filter
    zh = f"docs/zh-CN/{source}"
    errors.extend(check_counterpart_requirement(source, [en, zh], changed, statuses, exception))
```

Every source outside `14-ai-development` reaches the mirror branch with **no suffix check at all**. Any file type in a normative root therefore demands `docs/en/` **and** `docs/zh-CN/` counterparts.

Measured consequence on PR #500 (`6a7cafdb`, 77 files):

```
EXIT=1   errors=41   all 41 classified PAIR
08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json requires all counterparts changed
08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json requires all counterparts changed
08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.0.schema.json requires all counterparts changed
...
```

All 41 errors are `.json`:

```
by extension: {'json': 41}
```

A JSON schema cannot carry a Chinese translation of itself as Markdown, and translating a machine-readable schema into `docs/zh-CN/` would break its own consumers. The requirement is not strict — it is unsatisfiable as written.

---

## 1. This is a distinct defect from 011

Register 011 said: the diff domain demands mirrors where the gap scan accepts side-by-side. That was about **which shape** counts.

This is about **which file types** are subject to the rule at all. `PAIR_ENFORCED_SUFFIXES` already encodes the correct policy; it is simply unreachable for eight of the nine roots.

| Register | Question | Answer |
|---|---|---|
| 011 | does a side-by-side pair satisfy the diff domain? | no — mirrors required |
| 017 | does a `.json` file require a bilingual counterpart? | yes, outside the 14 root — and it cannot have one |

## 2. The PR matrix that exposed it

All nine open PRs, each overlaid on `main = d647e7d5ef` at its exact head, `PR_BODY` = the PR's real body:

| PR | head | gate | errors | class | touches `scripts/`/`crates/` |
|---|---|---|---|---|---|
| #509 | `78d61766` | **PASS** | 0 | — | yes |
| #507 | `c8f496ae` | FAIL | 1 -> **1** after manifest | manifest, then **011** | yes |
| #505 | `75e3b9e2` | FAIL | 1 -> **2** after manifest | manifest, then **017 x2** | no |
| #504 | `a608df27` | **PASS** | 0 | — | yes |
| #500 | `6a7cafdb` | **FAIL** | **41** | **PAIR ×41, all `.json`** | no |
| #496 | `4495b314` | **PASS** | 0 | — | no |
| #494 | `c572c946` | **PASS** | 0 | — | no |
| #471 | `d33ee2bb` | FAIL | 1 -> **0** after manifest | manifest only | yes |
| #433 | `81558c89` | **PASS** | 0 | — | yes |

5 pass, 4 fail. After supplying the missing manifest: **6 pass, 3 fail** — of which **2 are gate defects** (`#500`, `#505`, both 017) and **1 is a legitimate author omission** (`#507`, mirrors not updated).

### 2.1 The manifest error is only the first error, not the only error

`#507`, `#505`, `#471` all fail first with:

```
Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE'
or a fully documented 'BILINGUAL-EXCEPTION: APPROVED' block
```

**I initially recorded this as the whole story and that was wrong.** Re-running each PR twice — once with its real body, once with `BILINGUAL-MANIFEST: COMPLETE` appended — separates manifest failures from structural ones:

| PR | real body | body + `BILINGUAL-MANIFEST: COMPLETE` |
|---|---|---|
| `#471` | `EXIT=1` (manifest) | **`EXIT=0`** — manifest was the only problem |
| `#507` | `EXIT=1` (manifest) | **`EXIT=1`** — `02-domain-model/domain-model-overview.md requires all counterparts changed` |
| `#505` | `EXIT=1` (manifest) | **`EXIT=1`** — `08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json requires all counterparts changed` (x2) |

So of the three, **only `#471` is a pure manifest failure.** The other two have a structural error underneath, and the manifest error was masking it because the gate returns early.

### 2.2 Three PRs are structurally blocked, and all three are the same two defects

| PR | blocking file | defect |
|---|---|---|
| `#500` | 41 × `08-bmcp-protocol/schemas/*.schema.json` | **017** — `.json` subject to pairing |
| `#505` | 2 × `08-bmcp-protocol/schemas/*.schema.json` | **017** — same |
| `#507` | `02-domain-model/domain-model-overview.md` | **NOT a defect** — see §2.2a |

### 2.2a #507's error is legitimate, and I got it wrong first

`#507` fails after the manifest with:

```
02-domain-model/domain-model-overview.md requires all counterparts changed in this PR
```

I first attributed this to register 011. **That was wrong.** On main, `domain-model-overview.md` **already has both mirrors**:

```
02-domain-model/domain-model-overview.md          27542 bytes
docs/en/02-domain-model/domain-model-overview.md  29109 bytes
docs/zh-CN/02-domain-model/domain-model-overview.md 26231 bytes
```

So the file is a full mirror triple, the diff domain's requirement is satisfiable, and `#507` simply edited the source without updating the two mirrors. **That is a real pairing omission by the author, and the gate is right to reject it.**

The distinction matters: register 011's claim is that a correct side-by-side pair is rejected. `#507` is the opposite case — a file that has mirrors, edited without them. Conflating the two would have inflated 011's evidence with a case that does not support it.

`#507`'s other file, `phase-2-domain-extension.md`, genuinely has no mirrors and is a genuine 011 case. But the PR fails on `domain-model-overview.md` regardless, so `#507` cannot serve as 011's witness. Register 011's witness remains the five pairs measured directly in 013 §2.1.

`#507`'s file list is instructive:

```
modified 02-domain-model/domain-model-overview.md        <- no partner, blocked by 011
modified 02-domain-model/phase-2-domain-extension.md     <- has .zh-CN.md partner, ALSO blocked by 011
modified 02-domain-model/phase-2-domain-extension.zh-CN.md
modified crates/memory-domain/src/lib.rs
```

It **did** pair `phase-2-domain-extension` correctly — both sides in the same PR — and is still rejected, because the diff domain wants `docs/en` + `docs/zh-CN`, not the side-by-side pair. That is register 011's exact claim, now with a live PR as its witness.

`#505`'s file list shows the author doing the right thing twice over:

```
added    08-bmcp-protocol/schema-nonempty-audit.md        <- correct .md + .zh-CN.md pair
added    08-bmcp-protocol/schema-nonempty-audit.zh-CN.md
modified 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
modified 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json
added    08-bmcp-protocol/schemas/test_nonempty_audit.py
```

The `.md` pair is satisfied. The two `.json` edits are not, and cannot be.

### 2.3 #494 passes

`#494` — the register branch carrying 011/012/013/014/015/016 — passes at its own exact head with 35 changed paths inspected, baseline 77 frozen. The governance documents it adds are all `.md` and all mirrored, so they do not hit the suffix problem.

---

## 3. Why `PAIR_ENFORCED_SUFFIXES` is unreachable, not wrong

The constant is correct and was presumably added when someone hit exactly this problem inside `14-ai-development`. The 14 root contains `.png`, `.drawio`, `.yaml`, `.json` and the filter skips them.

The other eight roots never got the filter, because they were never given a `counterpart_14()`-style resolution path at all — they got the blanket two-mirror rule. So the suffix policy was written once, for one root, and the blanket branch was written without it.

This is the same structural pattern as register 015: a rule that exists, is correct, and is scoped to one root by a hard-coded prefix.

---

## 4. Relationship to the other four registers

| # | Defect | Root scope | File-type scope | CI impact |
|---|---|---|---|---|
| 011 | side-by-side rejected in diff domain | 8 of 9 roots | `.md` only (in practice) | blocks 5 real pairs |
| 013 | 1-CJK / 0-byte partner accepted | 9 of 9 | `.md` only | accepts empty translations |
| 014 | `ROOT = cwd` vs `REPO_ROOT` | global | all | local only |
| 015 | embedded bilingual only in 14 root | 8 of 9 roots | `.md` only | 58 of 77 baseline entries |
| **017** | **suffix filter only in 14 root** | **8 of 9 roots** | **all types** | **blocks #500, 41 errors** |

Five defects, all produced by the same design decision: one root (`14-ai-development`) got a bespoke resolution path, and the other eight got a blanket rule that ignores every refinement the bespoke path accumulated — suffix filtering (017), embedded-bilingual recognition (015), and side-by-side acceptance (011).

**That is the single sentence this whole series reduces to.** It is not five unrelated bugs. It is one root being special-cased, and every special case being withheld from the other eight.

---

## 5. What would have to be true for this to be a non-issue

1. JSON schemas are meant to have `docs/zh-CN/` Markdown translations of their field descriptions. → then `docs/zh-CN/08-bmcp-protocol/schemas/` should exist for the current 40+ schemas and does not; check whether any exist today.
2. `08-bmcp-protocol/schemas/` is meant to be outside the normative scan entirely. → then `NORMATIVE_ROOTS` or a new exempt prefix should say so.
3. The suffix filter is meant to be root-agnostic. → then 41 errors on #500 are a gate bug.

I checked (1) partially: `docs/zh-CN/08-bmcp-protocol/` exists but I did not find a `schemas/` subtree in it. Whether that is because nobody tried or because the policy forbids it, I cannot tell from the repository.

---

## 6. Reproduction

```
repo:    oahcom/AiMemoryBrainArchitecture
base:    main = d647e7d5ef
PR:      #500 head 6a7cafdb (77 files)

# overlay #500's files on main, commit, then:
BASE_SHA=<main> HEAD_SHA=<overlay> PR_BODY='<#500 body>' \
  python scripts/check_bilingual_docs.py
-> EXIT=1, 41 errors, every one of the form
   "08-bmcp-protocol/schemas/*.json requires all counterparts changed in this PR:
    08-bmcp-protocol/schemas/*.json, docs/en/08-bmcp-protocol/schemas/*.json,
    docs/zh-CN/08-bmcp-protocol/schemas/*.json"

# the constant
grep -n 'PAIR_ENFORCED_SUFFIXES' scripts/check_bilingual_docs.py
-> 40:PAIR_ENFORCED_SUFFIXES = {".md"}
-> 892:            if Path(source).suffix.lower() not in PAIR_ENFORCED_SUFFIXES:   # inside the 14 branch
```

No CI, no API quota beyond reading the PR.

---

## 7. What this register does not claim

- It does not claim #500 should be merged. Its 41 errors are structural, not its only problem.
- It does not claim JSON schemas need no bilingual treatment. It claims they cannot get the treatment the gate demands.
- It does not propose moving the suffix check. That is a gate change requiring authorisation.
- It does not verify whether `docs/zh-CN/08-bmcp-protocol/schemas/` has ever existed in git history.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 8. 实测：本登记的缺陷已被修复，修法与本登记 §5 第 3 分支不同（2026-11-23）

本登记正文与 §2 的 PR 矩阵**不改动**。那些数字测于 `d647e7d5`，记录保留。以下是当前 `main` 上的实测。

### 8.1 修复已落地，比本登记被登记早 80 分钟

| 项 | 值 |
|---|---|
| 修复 commit | `717dfbf0`，2026-11-21 22:09:16 +0800，`fix(bilingual): stop treating data files as documents requiring counterparts`（PR #527） |
| 本登记测量点 | `d647e7d5`，2026-11-21 20:48:30 +0800 |
| 本登记入库 | `d9c29a1c`，2026-11-21 23:21:05 +0800（PR #494） |
| 变更 | 一行：`suffix in {".md",".yaml",".yml",".json",".toml",".proto"}` → `suffix == ".md"`，`+1 −1` |
| 同 commit 附带 | `scripts/governance/evidence/test_gate_normative_roots.py` `+71`，3 个测试 |

修复早于本登记入库 72 分钟、早于本登记测量点 80 分钟。**该 commit 的提交信息没有提到 017**，全仓 `grep SUFFIX-SCOPE-017` 除本登记自身外零命中——与本登记 §2.2a 记录 #507 时的情形同构：证据都在，只是没有连起来。

### 8.2 修法不是 §5 的第 3 分支，而差别是实质的

§5 第 3 分支是「后缀过滤器本应 root-agnostic」。**该分支的诊断为真**（§3 的推理成立），但实际的修法不是移走过滤器，而是把**上游**收窄成只收 `.md`：

```python
normative_changes = []
for path in sorted(changed):
    parts = Path(path).parts
    if len(parts) >= 2 and parts[0] in NORMATIVE_ROOTS:
        if Path(path).suffix.lower() in EXEMPT_SUFFIXES:
            continue
        if Path(path).suffix.lower() == ".md":      # <-- 这里，不是第 1031 行
            normative_changes.append(path)
```

后果：`check_normative_pairing()` 永远收不到非 `.md` 文件，第 1031 行的 `PAIR_ENFORCED_SUFFIXES` 守卫再也不可能触发。按 `main` 的构造逻辑重放全树 552 个 normative 路径：**384 个候选，其中非 `.md` 为 0**。

`PAIR_ENFORCED_SUFFIXES = {".md"}` 仍在第 41 行声明、仍被第 1031 行读取，但已是恒真判断。代码读起来是「只对 Markdown 要求配对」，实际执行的是「只有 Markdown 会到这里」。

### 8.3 行为验证：缺陷态可复现，不是只读代码

在 `origin/main` 的干净 worktree 上，只改一个 `.json` schema 一个字符：

| 树状态 | 结果 |
|---|---|
| `main` 原样 | `PASS (1 changed paths inspected)` |
| 把 `717dfbf0` 那一行改回去 | `FAIL` — `::error::08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json requires all counterparts changed in this PR: ..., docs/en/..., docs/zh-CN/...` |

这正是本登记 §0 记录的错误形态。所以缺陷是真的，修复也是真的。

### 8.4 代价：167 个文件退出配对检查，其中 0 个曾有过镜像

`.json` 59、`.py` 54、`.yaml` 47、`.mjs` 4、其他 4。`docs/en/` 与 `docs/zh-CN/` 下的非 `.md` 文件数：**0**。

§5 的判断——要求 JSON schema 提供 Markdown 译文是**不满足的**——在修复后依然成立；修复只是把「不满足」改成「不检查」。结果上这是对的。本节不主张回退。

但 `.py`（54 个）与 `.json`（59 个）共享同一豁免这件事没有记录：一个 schema 与一个校验器在「是否需要中文说明」上不是同一类问题。

### 8.5 修复自带的 3 个测试在 `main` 上全部失效

`717dfbf0` 加的 3 个测试（`test_schema_json_change_does_not_require_counterpart`、`test_markdown_still_requires_counterpart`、`test_governance_markdown_still_requires_counterpart`）都走 `_run_real_git_gate_for_change()`。它们在 `9944d07e`（`#534`，补 `sys.argv`）时全绿，在 `8ab40fb4`（登记 014 的修复，把 `changed_status()` 的 `cwd=ROOT` 改成 `cwd=REPO_ROOT`）之后全部失效——因为 `load_gate()` 只改了 `mod.ROOT`，没改 `mod.REPO_ROOT`。

而且这个套件**没有任何 workflow 运行**：`grep -rn 'test_gate_normative_roots' .github/` 零命中。所以这 3 个测试既不再通过，也不会在 CI 变红。

完整测量与时间线见 `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030`。

### 8.6 状态

`OPEN` → `FIXED-CLOSED-BY-OTHER` — 缺陷已由 `717dfbf0` 修复并经行为验证；修法与 §5 第 3 分支不同（§8.2）；其自带的 3 个测试已失效且无 workflow 运行（§8.5）。独立审查仍 `NOT_ASSIGNED`。

不写 `CLOSED`：§6 的阻断链包含独立审查，而写这段文字的会话不能为自己的测量提供独立性；且 §8.2、§8.5 各自留下一个未决项，都由 030 承接。
