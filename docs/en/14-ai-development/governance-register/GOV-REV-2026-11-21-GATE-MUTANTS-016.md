---
document_metadata:
  domain: ai-development
  role: review-report
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "No formal approval record, approver identity or decision date exists in this repository; recorded as NOT_RECORDED rather than inferred."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-REV-2026-11-21-GATE-MUTANTS-016.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-21-GATE-MUTANTS-016.md"
---

# GOV-REV-2026-11-21-GATE-MUTANTS-016

**Status:** OPEN — MEASUREMENT ONLY
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 1d0ecb975c`; re-verified at `fa9c32a` and `8a2ce1b` (47 tests, same verdicts)
**Extends:** `GOV-REV-2026-11-21-PR425-001.md` (which found mutant M3 surviving in the digest path)
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0.1 Revision history

| Version | Date | Change |
|---|---|---|
| v1 | 2026-11-21 | Initial. Four mutants, M5/M6 survive, with the claim that M5 surviving means "the guard producing 75% of the baseline has no test" |
| **v2** | 2026-11-21 | **M5's interpretation corrected.** Measured: deleting that guard leaves the gap count **unchanged** (77 → 77), because Shape 3 needs a `docs/en` mirror and none of the 77 has one. M5 is an **unloaded mutant**; surviving is not evidence of a test gap. The real gap is §2.3 |

**M5 surviving is a fact; v1's explanation of it was wrong.** A mutant whose removal changes no output cannot be evidence about test quality.

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
| **M5** | `if not paired and root_name == "14-ai-development":` -> `if not paired:` | embedded-bilingual recognition applies to **all nine roots** | **47 OK** | **SURVIVED** |
| **M6** | `ROOT = Path.cwd()` -> `ROOT = REPO_ROOT` | the register-014 defect is fixed (single anchor) | **47 OK** | **SURVIVED** |
| **M7** | `_has_any_chinese` returns `any(...)` -> returns `True` | the content check becomes unconditional | **1 failure** | **KILLED** |

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

**v1 said "M5 surviving means the guard producing 75% of the baseline has no test coverage". The second half of that needs correcting.**

Measured: deleting `root_name == "14-ai-development"` leaves `current_bilingual_gaps()` **completely unchanged**:

```
BEFORE  gaps=77 baseline=77 new=0 resolved=0
AFTER   gaps=77 baseline=77 new=0 resolved=0
```

Not one gap moves. The reason is in register 015 v2 §3.1: Shape 3 requires `docs/en/X` to exist, and **none** of the 77 gaps has one.

```python
if not paired and root_name == "14-ai-development":
    paired = english.is_file() and _carries_chinese(source)   # english must exist
```

So M5 surviving is **not** "the tests missed an important guard". It is "**this guard carries zero load on all 77 baseline entries; deleting it changes nothing**". The tests did not kill it because it does not change behaviour today — not because the tests are badly written.

Shape 3's actual scope, measured, is three files, all in the 14 root:

```
14-ai-development/AI-EXEC-001.md
14-ai-development/AI-EXEC-002.md
14-ai-development/AI-EXEC-ROLLOUT-001.md
```

With the guard removed, the number of files in the other eight roots meeting all four conditions (no `docs/zh-CN`, no side-by-side partner, a `docs/en` mirror, Chinese content) is **0**.

**M5 is therefore an unloaded mutant**: its survival is real, but it proves less than v1 claimed. It proves "this branch carries no load today", not "there is a hole in the tests". The hole is elsewhere — see §2.3.

### 2.3 Corrected reading: the real test gap is that embedded bilingual has no shape

Register 015 v2 §3.2 measured that all 77 gaps fall into a single mechanism class: **no counterpart file of any kind, 77/77**.

And all three gate shapes **require a second file to exist**:

| Shape | Requires |
|---|---|
| mirror | `docs/en/X` + `docs/zh-CN/X` |
| side-by-side | a `X.zh-CN.md` or `X.en.md` sibling |
| embedded (Shape 3) | `docs/en/X` **and** `_carries_chinese(X)` |

**No shape accepts "one file carrying both languages internally".** The 13 root's 57 embedded-bilingual files are gaps because they have **no second file at all** — not because a root name blocks them.

That means `EMBEDDED_BILINGUAL_SOURCES`' 21 entries are not "exemptions" but the **only** mechanism by which embedded bilingual can pass, and it requires registering each file individually. `00-governance` registered 12, the 14 root 9, the 13 root 0 — in the root where embedded bilingual is most concentrated.

**The real test gap is therefore**: no test asserts how single-file embedded bilingual should be handled. M5 surviving is one symptom of that gap, not the gap itself.

### 2.2 M6: the `cwd` split from register 014 is untested

Replacing `ROOT = Path.cwd()` with `ROOT = REPO_ROOT` — the one-line unification described in register 014 — also breaks nothing. All 43 tests pass.

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
