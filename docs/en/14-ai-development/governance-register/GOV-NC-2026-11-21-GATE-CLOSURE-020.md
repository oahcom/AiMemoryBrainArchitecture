# GOV-NC-2026-11-21-GATE-CLOSURE-020

**Register**: GOV-NC-2026-11-21-GATE-CLOSURE-020
**Nature**: MEASUREMENT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
**Measured at**: `main = 1a5342421a` (`grep -vc '^#' scripts/bilingual-baseline.txt` = 77)
**Date**: 2026-11-21
**Author**: coordination session (not an independent reviewer)

---

## 0. What this register is for

Registers 011 to 019 recorded eight gate defects between `0cce40a` and `d647e7d`. Main has since advanced to `1a53424`, and several gate-repair PRs landed in that window. This register checks each of the eight: **which are closed, by what mechanism, and which are still open.**

This is not a declaration that the defects are fixed. Closure is decided by measurement, and the recorder is not an independent reviewer.

---

## 0.1 One of my own conclusions, overturned here

Register 017 said `.json` schemas are required to have bilingual mirrors, and attributed the mechanism to `PAIR_ENFORCED_SUFFIXES` applying only inside the 14 branch. **The defect was real, but I had the root cause half wrong.**

The actual fix came from #527 (`717dfbf`), and it did not touch `PAIR_ENFORCED_SUFFIXES`. It changed the filter that builds `normative_changes` inside `main()`:

```python
# before (line 996 in d647e7d)
if Path(path).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}:
    normative_changes.append(path)

# after (line 1064 in 1a53424)
if Path(path).suffix.lower() == ".md":
    normative_changes.append(path)
```

So `.json` no longer **enters** the pairing check at all, rather than "entering and being let through by the suffix filter". Line 937's `PAIR_ENFORCED_SUFFIXES` is still inside the 14 branch, but it is no longer where `.json` escapes.

The difference has a real consequence: my proposal (hoist the suffix filter out of the branch) would let `.json` enter the pairing check and then be exempted, keeping **two** definitions of "which suffixes count as documents". The fix actually adopted has one definition, which is harder to get wrong. **The adopted fix is better than my proposal.**

---

## 1. Item-by-item status

| Register | Defect | State at `1a53424` | How closed |
|---|---|---|---|
| 011 | non-14 side-by-side pair rejected in the diff domain | **CLOSED** | #485 `5f10930` added a `side_by_side_partner(source)` branch to `check_normative_pairing()` |
| 013 | same (residual measurement) | **CLOSED** | same as 011 |
| 014 | `ROOT = Path.cwd()` split from `REPO_ROOT` | **OPEN** | unfixed, see §2.1 |
| 015 | 58 frozen gaps in `13-engineering-decisions` | **OPEN** | unfixed, baseline still 77, all 58 still there |
| 016 | mutants M5/M6 survive | **OPEN** | see §3 |
| 017 | `.json` required to have bilingual mirrors | **CLOSED** | #527 `717dfbf` narrowed `normative_changes` to `.md` only |
| 019 | `PARTIAL_SIDE_BY_SIDE_PAIRS` never reaches the diff domain | **OPEN** | unfixed, see §2.2 |
| 020 | zero-byte / three-file / single-CJK holes | **OPEN** | see §2.3 |

**2 closed, 6 open.** Both closed items are gate-shape problems. Of the six still open, three are policy problems (014/015/019) and three are predicate-strength problems (020).

---

## 2. Precise state of the open items

### 2.1 014 — the `ROOT` / `REPO_ROOT` split still exists

```python
REPO_ROOT = Path(__file__).resolve().parents[1]   # line 23
ROOT      = Path.cwd()                            # line 157
```

Measured at `1a53424`: `str(REPO_ROOT) == str(ROOT)` is `True` when run from the repo root, `False` from any other directory. `--write-baseline` from a foreign directory still writes 117 entries instead of 77.

CI is unaffected (the workflow's cwd is the checkout root). This is a local-measurement and baseline-regeneration hazard, not a CI runtime defect.

### 2.2 019 — `PARTIAL_SIDE_BY_SIDE_PAIRS` is still empty and still absent from the diff domain

```python
# line 44
PARTIAL_SIDE_BY_SIDE_PAIRS: set[frozenset[str]] = set()

# line 350 — inside current_bilingual_gaps()
and frozenset((source, side_by_side)) in PARTIAL_SIDE_BY_SIDE_PAIRS
```

References inside `check_normative_pairing()` (lines 919-963): **0**.

And **0 of 77** baseline entries pair with another baseline entry, so the register cannot affect existing gaps either. Its real scope is "the gap scan for new pairs", far narrower than its name suggests.

### 2.3 020 — three predicate-strength holes, all reachable through the real CLI

All three verified through the real CI entry point: write files → `git add` → `git commit` → `BASE_SHA=HEAD~1 HEAD_SHA=HEAD PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python scripts/check_bilingual_docs.py`. The precondition `REPO_ROOT == ROOT` was asserted `True`.

| Hole | Construction | CLI result | Should be |
|---|---|---|---|
| **H1 zero-byte** | `zb.md` (Chinese) + `zb.zh-CN.md` (**0 bytes**) | **`EXIT=0`** | reject |
| **H2 three-file** | `am.md` (zh) + `am.en.md` (en) + `am.zh-CN.md` (zh) | **`EXIT=0`** | reject (ambiguous) |
| **H3 single CJK** | both sides English, each with one `一` | **`EXIT=0`** | reject |

**H1 detail**: `_has_any_chinese` is `False` for `zb.zh-CN.md`, yet `_side_by_side_bilingual` returns `True` — because the predicate is "the source **or** the partner carries CJK", and the source carries Chinese. The 0-byte partner is never read.

**H2 detail**: the pairing chain is **asymmetric**, which is a more serious fact than "three files are accepted":

```
am.md        -> am.en.md      -> am.zh-CN.md     ASYMMETRIC
am.en.md     -> am.zh-CN.md   -> am.en.md        SYMMETRIC
am.zh-CN.md  -> am.en.md      -> am.en.md        SYMMETRIC
```

`am.md` points at `am.en.md`, but `am.en.md` points back at `am.zh-CN.md`. `partner(partner(am.md)) != am.md`. So `am.md`'s Chinese body is **never required to be synchronised by anyone** — it looks paired and is in fact excluded from pairing. That is a direct consequence of first-match-returns.

**H3 detail**: `_has_any_chinese` requires one CJK character. One `一` is enough. Two English files, each with a single `一`, constitute a "bilingual pair".

### 2.4 Existing exploitation: exploitable, unexploited

```
0-byte .zh-CN.md files : 0
total .zh-CN.md files  : 72
```

**All 72 `.zh-CN.md` files are non-empty.** All three holes are **potential**, not **realised**. That distinction must be preserved: "the gate has holes" and "the repo contains fake translations" are different claims, and the second one is false.

---

## 3. Mutant status: M5 and M6 still survive

Re-ran four mutants at `1a53424` (the test file currently holds 47 tests):

| Mutant | Result |
|---|---|
| **M4** remove `and not partial_side_by_side` | **KILLED** (1 failure) |
| **M5** remove Shape 3's `root_name == "14-ai-development"` guard | **SURVIVED** (47 pass) |
| **M6** `ROOT = Path.cwd()` → `ROOT = REPO_ROOT` | **SURVIVED** (47 pass) |
| **M7** `_has_any_chinese` → `return True` | **KILLED** (1 failure) |

**M5 surviving means**: the root-name guard that produces 58 of the 77 baseline entries (register 015) has no test coverage. Anyone can delete it and the suite stays green.

**M6 surviving means**: both the defect from register 014 and its fix are **invisible** to the suite, because every test runs at the repo root. That is also why 014 has been able to persist.

---

## 4. Current PR matrix

`main = 1a5342421a`, 10 open PRs, each overlaid at its exact head onto main and then gated:

| PR | head | files | raw body | + manifest | verdict |
|---|---|---|---|---|---|
| #530 | `f1fd4219` | 1 | `EXIT=0` | `EXIT=0` | PASS |
| #529 | `85257d5d` | 3 | `EXIT=0` | `EXIT=0` | PASS |
| #523 | `6bb94365` | 3 | `EXIT=0` | `EXIT=0` | PASS |
| #518 | `2651e226` | 1 | `EXIT=0` | `EXIT=0` | PASS |
| #513 | `d7992210` | 2 | `EXIT=0` | `EXIT=0` | PASS |
| #512 | `e265f7d5` | 2 | `EXIT=0` | `EXIT=0` | PASS |
| #496 | `4d1ce5ab` | 9 | `EXIT=0` | `EXIT=0` | PASS |
| #494 | `c1beeb1d` | 30 | `EXIT=0` | `EXIT=0` | PASS |
| #471 | `d33ee2bb` | 8 | `EXIT=1` (1) | **`EXIT=0`** | MANIFEST-ONLY |
| #433 | `81558c89` | 3 | `EXIT=0` | `EXIT=0` | PASS |

**9 pass, 1 needs only its manifest.** Against register 017's "5 pass / 4 fail", the gate-shape problems are essentially cleared. None of the remaining failures belongs to the 011 or 017 class.

---

## 5. What this register does not claim

- **It does not claim the gate is trustworthy.** M5 and M6 survive; 47 tests do not cover the rule that produces 75% of the baseline.
- **It does not claim the three holes must be fixed now.** Fixing requires a judgement: would a non-empty-partner predicate disturb the 77 baseline entries? Would a higher CJK threshold turn genuine short documents into new gaps? I did not measure either, so I propose no fix.
- **It does not claim 011/017 were closed under independent review.** I did not audit the review trail of #485 or #527. Closure is a measured fact, not a review verdict.
- **It does not claim CI executed.** All 348 checks still show `steps=[]` (register 005); every verification this round is local compensating evidence.
- **It does not claim passing tests mean adequate coverage.** 47 green tests and M5/M6 surviving are simultaneously true — a live instance of "passing is not effective".

---

## 6. Reproduction

```bash
git clone https://github.com/oahcom/AiMemoryBrainArchitecture.git && cd AiMemoryBrainArchitecture
git rev-parse --short HEAD                      # 1a53424
grep -vc '^#' scripts/bilingual-baseline.txt    # 77

# H1 zero-byte
printf '# 标题\n\n%s\n' "$(python3 -c "print('中文内容测试。'*30)")" > 02-domain-model/zb.md
: > 02-domain-model/zb.zh-CN.md
git add -A && git -c user.email=t@t -c user.name=t commit -qm p
BASE_SHA=$(git rev-parse HEAD~1) HEAD_SHA=$(git rev-parse HEAD) \
  PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py; echo "EXIT=$?"
# -> EXIT=0

# H2 asymmetry
python3 -c "
import sys,os; sys.path.insert(0,'scripts'); sys.argv=['x']
import check_bilingual_docs as g
for f in ('02-domain-model/am.md','02-domain-model/am.en.md','02-domain-model/am.zh-CN.md'):
    p=g.side_by_side_partner(f); q=g.side_by_side_partner(p) if p else None
    print(f,'->',p,'->',q,'SYMMETRIC' if q==f else 'ASYMMETRIC')"

# M5 / M6 survival
python3 -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"   # 47 OK
# then edit the guard, rerun -> still 47 OK
```

---

## 7. Three questions for an independent reviewer

1. **Why does M5 have no test?** Is the `root_name == "14-ai-development"` guard that produces 58/77 baseline entries a policy decision or historical residue? If policy, a test should pin it; if residue, it should be removed and the baseline regenerated.
2. **Would the minimal H1 fix disturb the baseline?** Would "a partner file must be non-empty" produce new `resolved` entries among the 77 frozen gaps (the other ratchet direction errors out)? I did not measure this.
3. **Should H2 ambiguity be rejected or should precedence be defined?** Rejecting makes the three-file shape unusable; defining precedence requires saying why `.md` outranks `.en.md`. This is a policy question, not an implementation question.

---

**This file is a measurement record, not a review verdict, and authorises no implementation.**
