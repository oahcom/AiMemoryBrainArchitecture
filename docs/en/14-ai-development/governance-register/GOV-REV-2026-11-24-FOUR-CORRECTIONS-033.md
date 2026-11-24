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
    source: "14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
---

# GOV-REV-2026-11-24-FOUR-CORRECTIONS-033

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 2059c8105`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. Four corrections, three of them against my own work

This file is written within an hour of `REGISTER-INDEX-031` and `DISPATCH-CHANNEL-CLOSED-032` merging. While they merged, main advanced three commits, and one of them removed a fact I had relied on in 030.

| # | What I wrote before | What is measured now | Verdict |
|---|---|---|---|
| 1 | 030 §4/§6: 52 tests, 24 problems, no workflow runs it | `Ran 52 tests / OK`; `bilingual-docs.yml:27` runs it | **fixed by `aaf6da966` (#892)** |
| 2 | The 24 problems meant the suite cannot be killed | two mutation tests both killed it | **my inference was wrong**: it can fail |
| 3 | 032 §6: preserve that work order for when the widening lands | the work is already done; the order has no object | **what I preserved is void** |
| 4 | GAP-24: the zh-CN mirror is the English file | 2 of 123 pairs are byte-identical, **in opposite directions** | **GAP-24 undercounts and describes one direction only** |

032 §1–§5 (the dispatch channel is closed) is unaffected and re-verified in §5.

---

## 2. 030 §4 and §6 are fixed, and fixed well

`aaf6da966` (#892, 2026-11-24 13:49:49 +0800) merged after my measurement. Same machine, same command:

| Point | Output |
|---|---|
| `main` `ef7266db` (when I measured) | `Ran 52 tests in 72.708s` / **`FAILED (failures=3, errors=21)`** |
| `main` `2059c8105` (now) | `Ran 52 tests in 35.976s` / **`OK`** |

Its commit message names the root cause correctly, and more precisely than I did: `REPO_ROOT` is defined at line 24 and `ROOT = REPO_ROOT` at line 170 is a **plain assignment, not a proxy**, so rebinding one name leaves the other pointing at the real checkout. The two names had drifted into different jobs — file-existence and pairing logic read `ROOT`, while *every* `subprocess.run(..., cwd=...)`, `BASELINE_PATH`, and both import-time checks read `REPO_ROOT`.

§6 is fixed too: `bilingual-docs.yml:27` now runs the suite, placed before the real gate, with the reason in the commit message — "a fixture-only failure cannot be mistaken for a document problem." That is better than the work order I was going to write, which would have added it to the hygiene workflow's explicit list: it now hangs off the required `GOV-DOC-001 structural checks` context instead of off another job's duration.

**So `AID-2026-055` does not need registering.** The content preserved in 032 §6 — object, basis, seven criteria — now points at finished work. I do not delete 032's §6: it records the judgement of the moment, and the judgement was right then. This file declares it void.

---

## 3. My inference about the 24 problems was wrong: the suite can be killed

030 §4 said the 24 failures "will not go red anywhere". From that I inferred the suite was blunt against the control it guards, and wrote two mutation tests into 032 §6 as requirements. **The inference was wrong**: the 24 came from the helper reading the wrong repository, not from tautological assertions.

At `main 2059c8105`, two mutations against `scripts/check_bilingual_docs.py`, one 52-test run each, then restored:

| Mutation | Result | Verdict |
|---|---|---|
| baseline (unmutated) | `Ran 52 tests in 25.117s` / **`OK`** | — |
| A: delete `and not partial_side_by_side` | `Ran 52 tests in 21.868s` / **`FAILED (failures=1)`** | **KILLED** |
| B: replace every `cwd=ROOT` with the real checkout (recreate the half-override bug) | `Ran 52 tests in 97.701s` / **`FAILED (failures=8, errors=11)`** | **KILLED** |
| after restoring | `Ran 52 tests in 16.828s` / **`OK`** | — |

Both carry numbers, not "it ran fine".

**This has a direct consequence for `AID-2026-054`.** `ERRATUM-01` criterion 11 requires that deleting `and not partial_side_by_side` fails at least one test, with the output pasted. When written, that criterion was **unsatisfiable** — `PARTIAL_SIDE_BY_SIDE_PAIRS` had no effective test. It is now satisfiable, and the margin is exactly 1 failure. So `ERRATUM-01`'s item C moves from "raising a requirement" to "a requirement that can be executed" — but 1 failure is **thin**: any further weakening of that assertion could still erase it. Criterion 11 should require "at least one failure, and that failure asserts `PARTIAL_SIDE_BY_SIDE_PAIRS` semantics", not merely "something goes red".

---

## 4. GAP-24 undercounts by one pair, and describes only one direction

Enumerating every `<P>` on main where both `docs/en/<P>` and `docs/zh-CN/<P>` exist, and comparing blobs:

| Class | Criterion | Count |
|---|---|---|
| **IDENTICAL** | `en` and `zh-CN` byte-identical | **2** |
| **ZH_EMPTY** | differ, `zh-CN` has zero CJK | **2** |
| **ZH_THIN** | differ, `zh-CN` has 1–99 CJK | **3** |
| **REAL** | differ, `zh-CN` has ≥100 CJK | **116** |
| Total | — | **123** |

Only 2 of 123 are byte-identical. That ratio says the problem is not systemic, and GAP-24 should be read as "individual files", not "a class of files".

**But those two run in opposite directions, and GAP-24 describes only one:**

| File | Bytes | CJK | Root file is | Mirror defect |
|---|---|---|---|---|
| `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023.md` | 12181 | **0** | English | `docs/zh-CN/` is an English copy — **GAP-24's case** |
| `GOV-REV-2026-11-21-PR425-001.md` | 7390 | **1057** | **Chinese** | `docs/en/` is a **Chinese** copy — **the inverse, which GAP-24 does not have** |

`GOV-REV-...-PR425-001.md` has the same md5 in all three locations (root, `docs/en`, `docs/zh-CN`); the content is a Chinese technical review record. Its `docs/zh-CN/` is **genuinely Chinese**; the wrong file is `docs/en/` — a reader opening `docs/en/` for English gets 1057 CJK characters of Chinese.

The consequence: GAP-24 §3's check (a) (`md5(zh-CN) == md5(source)` is an error) **is still correct as a detector** — it catches 2 files — **but its wording misclassifies the 425 pair**: that pair's `zh-CN` is fine and the defect is in `docs/en/`. The check must be written direction-agnostically ("either side is a byte-for-byte copy of the other"), and the two pairs need different remedies:

- `023`: supply a real Chinese version, or withdraw it from `docs/zh-CN/` and register an exemption.
- `PR425-001`: the root is Chinese, `docs/zh-CN/` is legitimate, and `docs/en/` is the side missing English.

**GAP-24's count is therefore 2, not 1; and "the zh-CN mirror is the English file" is true of only one of them.**

---

## 5. 032 §1–§5 is unaffected, and re-verified

#892 did not touch the admission whitelist: the two most recent changes to `scripts/ci/check_repository_hygiene.py` are still `cfcafc98a` (#844) and `e798b1a72`. Calling the function directly on the current tree:

```
is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')  -> False
is_allowed_new_path('14-ai-development/governance-register/X.md')                -> True
```

So "no new work order can be registered" still holds — it is simply that **no work order now wants registering**. Both facts are true at once: the channel is shut, and the last thing that wanted it was finished by someone else down a different road.

---

## 6. What this file does not claim

- That #892 should be reverted. It fixed this better than I asked for.
- That 030 should be closed. Its §4/§6 are fixed; I do not re-measure §1–§3, §5, §7, and `register_closure` is not in this session's authority.
- That GAP-24's allowance needs no attention. I correct only its count and direction; its `docs/zh-CN/` direction is entirely right for `023`.
- That 2 byte-identical pairs is the whole of it. I enumerated only the 123 pairs where both `docs/en` and `docs/zh-CN` exist; side-by-side pairs (`X.en.md` / `X.zh-CN.md`) and single-sided mirrors are outside this count.
- An independent reviewer. That seat is `NOT_ASSIGNED`, and this file cannot fill it.

**Blocking chain:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 7. Reproduction

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  2059c8105

# 1. the suite is green now
git worktree add --detach <tmp> origin/main
cd <tmp> && python -m unittest scripts.governance.evidence.test_gate_normative_roots
-> Ran 52 tests / OK

# 2. it can be made red
#    delete `and not partial_side_by_side` from current_bilingual_gaps(), re-run
-> FAILED (failures=1)
#    replace every `cwd=ROOT` with pathlib.Path(__file__).resolve().parents[1], re-run
-> FAILED (failures=8, errors=11)

# 3. CI runs it now
grep -n 'test_gate_normative_roots' .github/workflows/bilingual-docs.yml
-> 27:        run: python3 -m unittest scripts.governance.evidence.test_gate_normative_roots

# 4. the mirror audit
#    enumerate P where docs/en/P and docs/zh-CN/P both exist; compare git show blobs
-> 123 pairs; IDENTICAL 2, ZH_EMPTY 2, ZH_THIN 3, REAL 116
#    the two byte-identical pairs have CJK counts of 0 and 1057

# 5. admission still refuses work orders
python -c "import check_repository_hygiene as h; print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml'))"
-> False
```
