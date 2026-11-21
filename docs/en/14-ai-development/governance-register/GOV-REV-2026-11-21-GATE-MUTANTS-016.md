# GOV-REV-2026-11-21-GATE-MUTANTS-016

**Status:** OPEN — MEASUREMENT ONLY
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 1d0ecb975c`
**Extends:** `GOV-REV-2026-11-21-PR425-001.md` (which found mutant M3 surviving in the digest path)
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. Method

Four single-line mutations of `scripts/check_bilingual_docs.py`, each applied alone, each followed by:

```
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 43 tests
```

The file was restored after each run and `git status` confirmed clean.

A mutant is **killed** if at least one test fails. A mutant **survives** if all 43 pass — which means the line it removed is not protected by any test.

---

## 1. Results

| # | Mutation | Effect of the mutation | Tests | Verdict |
|---|---|---|---|---|
| **M4** | delete `and not partial_side_by_side` | a pair registered as partially translated counts as paired again | **1 failure** | **KILLED** |
| **M5** | `if not paired and root_name == "14-ai-development":` -> `if not paired:` | embedded-bilingual recognition applies to **all nine roots** | **43 OK** | **SURVIVED** |
| **M6** | `ROOT = Path.cwd()` -> `ROOT = REPO_ROOT` | the register-014 defect is fixed (single anchor) | **43 OK** | **SURVIVED** |
| **M7** | `_has_any_chinese` returns `any(...)` -> returns `True` | the content check becomes unconditional | **1 failure** | **KILLED** |

Verbatim failure for M4:

```
AssertionError: '02-domain-model/zz-partial-probe.md' not found in set()
FAILED (failures=1)
```

Verbatim failure count for M7: `FAILED (failures=1)`.

Verbatim result for M5 and M6: `Ran 43 tests in ... OK`.

---

## 2. What the two survivors mean

### 2.1 M5: the root guard that produces 75% of the baseline is untested

Register 015 measured that **58 of 77 frozen baseline entries are the entire `13-engineering-decisions` root**, and that the mechanism excluding them is:

```python
if not paired and root_name == "14-ai-development":
    paired = english.is_file() and _carries_chinese(source)
```

Deleting `root_name == "14-ai-development"` — making embedded-bilingual recognition root-agnostic — breaks **nothing** in the test suite. All 43 tests still pass.

So the test suite cannot tell the difference between:

- the current policy: embedded bilingual counts **only** in `14-ai-development`
- the alternative policy: embedded bilingual counts **everywhere**

A 58-entry policy consequence rests on a line no test constrains. Whether the guard is correct is a policy question (register 015 §6 lists three readings I cannot distinguish). That it is **unprotected** is not a policy question.

### 2.2 M6: the `cwd` split from register 014 is untested

Replacing `ROOT = Path.cwd()` with `ROOT = REPO_ROOT` — the one-line unification described in register 014 — also breaks nothing. All 43 tests pass.

That means every test in `test_gate_normative_roots.py` runs with `cwd == REPO_ROOT`, so the two anchors are indistinguishable to the suite. The defect is invisible precisely because the tests never leave the repository root — the same reason it is invisible in CI.

Combined with register 014: a change that would fix a defect corrupts no test, and the defect itself corrupts no test. Both states are equally green.

### 2.3 M4 and M7 are the exception, and the difference is instructive

`PARTIAL_SIDE_BY_SIDE_PAIRS` **is** covered: `test_gate_normative_roots.py` lines 549/562 add entries and line 577 asserts the register is empty at rest. The content predicate is also covered.

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
-> Ran 43 tests ... OK

# M5
sed -i 's/if not paired and root_name == "14-ai-development":/if not paired:/' scripts/check_bilingual_docs.py
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 43 tests ... OK          # survived
git checkout -- scripts/check_bilingual_docs.py

# M6
sed -i 's/^ROOT = Path.cwd()/ROOT = REPO_ROOT/' scripts/check_bilingual_docs.py
python -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"
-> Ran 43 tests ... OK          # survived
git checkout -- scripts/check_bilingual_docs.py

# M4  -> FAILED (failures=1)     killed
# M7  -> FAILED (failures=1)     killed
```

No network access, no CI, no API quota required.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.
