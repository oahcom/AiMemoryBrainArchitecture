# GOV-NC-2026-11-21-PAIRING-RESIDUAL-013

**Status:** OPEN — MEASUREMENT ONLY
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
