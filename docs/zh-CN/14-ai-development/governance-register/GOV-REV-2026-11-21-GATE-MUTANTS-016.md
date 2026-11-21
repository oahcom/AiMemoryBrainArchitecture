# GOV-REV-2026-11-21-GATE-MUTANTS-016

**Status:** OPEN — MEASUREMENT ONLY
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 1d0ecb975c`; re-verified at `fa9c32a` and `8a2ce1b` (47 tests, same verdicts)
**Extends:** `GOV-REV-2026-11-21-PR425-001.md` (which found mutant M3 surviving in the digest path)
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0.1 修订记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1 | 2026-11-21 | 初版。四个变异体，M5/M6 存活，并声称 M5 存活意味着「产生 75% 基线的守卫没有测试」 |
| **v2** | 2026-11-21 | **更正 M5 的解释**。实测删掉该守卫后缺口数**完全不变**（77→77），因为 Shape 3 需要 `docs/en` 镜像而这 77 条一条都没有。M5 是**空载变异体**，存活不等于测试有洞。真正的空洞在 §2.3 |

**M5 的「存活」是事实，v1 对它的解释是错的。** 一个删掉后不改变任何输出的变异体，其存活不能作为测试质量的证据。

---

## 0. Method

Four single-line mutations of `scripts/check_bilingual_docs.py`, each applied alone, each followed by:

```
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 47 tests
```

The file was restored after each run and `git status` confirmed clean.

A mutant is **killed** if at least one test fails. A mutant **survives** if all 47 pass — which means the line it removed is not protected by any test.

---

## 1. Results

| # | Mutation | Effect of the mutation | Tests | Verdict |
|---|---|---|---|---|
| **M4** | delete `and not partial_side_by_side` | a pair registered as partially translated counts as paired again | **1 failure** | **KILLED** |
| **M5** | `if not paired and root_name == "14-ai-development":` → `if not paired:` | embedded-bilingual recognition applies to **all nine roots** | **47 OK** | **SURVIVED** |
| **M6** | `ROOT = Path.cwd()` → `ROOT = REPO_ROOT` | the register-014 defect is fixed (single anchor) | **47 OK** | **SURVIVED** |
| **M7** | `_has_any_chinese` returns `any(...)` → returns `True` | the content check becomes unconditional | **1 failure** | **KILLED** |

Verbatim failure for M4:

```
AssertionError: '02-domain-model/zz-partial-probe.md' not found in set()
FAILED (failures=1)
```

Verbatim failure count for M7: `FAILED (failures=1)`.

Verbatim result for M5 and M6: `Ran 47 tests in ... OK`.

---

## 2. What the two survivors mean

### 2.1 M5: the guard survives because the branch it guards never fires

**本登记的 v1 说「M5 存活意味着产生 75% 基线的那个守卫没有测试覆盖」。这句话的后半句要改。**

实测：把 `root_name == "14-ai-development"` 删掉后，`current_bilingual_gaps()` 的返回值**完全不变**：

```
BEFORE  gaps=77 baseline=77 new=0 resolved=0
AFTER   gaps=77 baseline=77 new=0 resolved=0
```

一个缺口都没动。原因在登记 015 v2 §3.1：Shape 3 的前置条件是 `docs/en/X` 必须存在，而 77 条缺口里**没有一条**有这个镜像。

```python
if not paired and root_name == "14-ai-development":
    paired = english.is_file() and _carries_chinese(source)   # english must exist
```

所以 M5 存活**不是**「测试漏了一个重要守卫」，而是「**这个守卫对全部 77 条基线零载荷，删不删都一样**」。测试没杀它，是因为它今天不改变任何行为——不是因为测试写得差。

Shape 3 的实际作用域实测只有 3 个文件，全在 14 根：

```
14-ai-development/AI-EXEC-001.md
14-ai-development/AI-EXEC-002.md
14-ai-development/AI-EXEC-ROLLOUT-001.md
```

把守卫删掉后，其他八根里同时满足「无 `docs/zh-CN`、无并排配对、有 `docs/en`、含中文」的文件数是 **0**。

**所以 M5 是一个「空载变异体」**：它存活是真的，但它证明的东西比 v1 声称的弱。它证明的是「这个分支今天无载荷」，不是「测试有洞」。真正的洞在别处——见 §2.3。

### 2.3 更正后的判断：真正的测试空洞是「内嵌双语没有形态」

登记 015 v2 §3.2 实测：77 条缺口的机制分类只有一类——**完全没有对应文件，77/77**。

而门禁的三种形态**全部要求存在第二个文件**：

| 形态 | 需要 |
|---|---|
| mirror | `docs/en/X` + `docs/zh-CN/X` |
| side-by-side | `X.zh-CN.md` 或 `X.en.md` 兄弟文件 |
| embedded (Shape 3) | `docs/en/X` **且** `_carries_chinese(X)` |

**没有任何形态承认「一个文件内部同时承载两种语言」。** 13 根的 57 个内嵌双语文件之所以是缺口，是因为它们**连第二个文件都没有**——不是被根名挡住。

这意味着：`EMBEDDED_BILINGUAL_SOURCES` 那 21 条不是「豁免」，而是**唯一能让内嵌双语通过的机制**，且必须逐个文件登记。00-governance 登记了 12 个，14 根 9 个，13 根 0 个——而 13 根是内嵌双语最集中的地方。

**真正的测试空洞因此是**：没有任何测试断言「单文件内嵌双语应当如何被处理」。M5 存活只是这个空洞的一个症状。

### 2.2 M6: the `cwd` split from register 014 is untested

Replacing `ROOT = Path.cwd()` with `ROOT = REPO_ROOT` — the one-line unification described in register 014 — also breaks nothing. All 47 tests pass.

That means every test in `test_gate_normative_roots.py` runs with `cwd == REPO_ROOT`, so the two anchors are indistinguishable to the suite. The defect is invisible precisely because the tests never leave the repository root — the same reason it is invisible in CI.

Combined with register 014: a change that would fix a defect corrupts no test, and the defect itself corrupts no test. Both states are equally green.

### 2.3 M4 and M7 are the exception, and the difference is instructive

`PARTIAL_SIDE_BY_SIDE_PAIRS` **is** covered: `test_gate_normative_roots.py` lines 549/562 add entries and line 577 asserts the register is empty at rest. The content predicate is also covered.

**Caveat added after further measurement — see `GOV-REV-2026-11-21-PARTIAL-SCOPE-019.md`.** The coverage is real, but the control it protects is narrower than I implied here. `PARTIAL_SIDE_BY_SIDE_PAIRS` is referenced only at line 44 (declaration) and line 305 (inside `current_bilingual_gaps()`); `check_normative_pairing()` contains **zero** references to it. So M4 being killed proves the *scan* honours the register, not that PR enforcement does. It does not.

So the suite protects the **newest** controls and leaves the **oldest** ones unconstrained. That is the ordinary shape of test decay: tests are written with the feature and never backfilled.

---

## 3. Relationship to PR425-001's M3

`GOV-REV-2026-11-21-PR425-001.md` established mutant **M3** surviving in the digest-verification path, and proposed `TEST-DRAFT-2026-11-21-PR425-M3.md` to kill it. That finding is unchanged.

This register adds four more mutants to the same picture:

| Mutant | Location | Status |
|---|---|---|
| M3 | digest verification | **SURVIVED** (PR425-001) |
| M4 | `PARTIAL_SIDE_BY_SIDE_PAIRS` guard | killed |
| M5 | Shape 3 root guard | **SURVIVED** |
| M6 | `ROOT` anchor | **SURVIVED** |
| M7 | `_has_any_chinese` | killed |

Three of five survive. The pattern is not "tests are bad"; it is "tests cover what was recently added and not what the design depends on".

---

## 4. What this register does not claim

- It does not claim M5 should be killed by removing the guard. Killing M5 means **adding a test that asserts the current policy**, whichever policy the owner picks.
- It does not claim M6's mutation is the correct fix. Register 014 §6 notes that unifying the anchor is still a gate change requiring authorisation.
- It does not claim a surviving mutant is a live bug. A surviving mutant means *no test would notice*; whether the current behaviour is wrong is separate.
- It does not re-run the full Rust workspace suite; these are gate-script mutations only.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

---

## 5. Reproduction

```
repo:   oahcom/AiMemoryBrainArchitecture
commit: 1d0ecb975c
cwd:    repo root   (register 014: a foreign cwd invalidates this measurement)

# baseline
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 47 tests ... OK

# M5
sed -i 's/if not paired and root_name == "14-ai-development":/if not paired:/' scripts/check_bilingual_docs.py
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 47 tests ... OK          # survived
git checkout -- scripts/check_bilingual_docs.py

# M6
sed -i 's/^ROOT = Path.cwd()/ROOT = REPO_ROOT/' scripts/check_bilingual_docs.py
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 47 tests ... OK          # survived
git checkout -- scripts/check_bilingual_docs.py

# M4  -> FAILED (failures=1)     killed
# M7  -> FAILED (failures=1)     killed
```

No network access, no CI, no API quota required.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.
