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
      last_verification_note: "§1-§4 and §6-§7 measured at main 2059c8105; §8 re-measured at main 84bbe9241; §5 re-measured at main 01a3014 on 2026-11-24 19:39:28. Every §8 row is one real invocation of scripts/check_bilingual_docs.py on a worktree reset to origin/main before the single commit under test, with the exit code recorded. Cases F and G exit 0, which is the evidence that no code reads docs/zh-CN content. Cases D, H, I exit non-zero, which refutes the inference that deleting a Chinese mirror goes unannounced. The baseline is 80 lines = 3 comments + 77 entries; none of the 7 content defects appears among those 77 entries. The pair count moved 123 -> 124 between the two measurement points because main gained files. §5 was re-measured because its original two assertions were taken at 2059c8105, ten minutes before #893 added WORK_ITEM_MANIFEST_RE; AID-2026-055 (#896, 84bbe9241) through AID-2026-058 (01a3014) have since been registered through that rule. The count in §5.2 is a snapshot at that measurement point, not a standing number: 057 and 058 landed during this revision, which is the section's own argument happening to the section."
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

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION` / §8 added 2026-11-24
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 2059c8105` (§4), `main = 84bbe9241` (§8), `main = 01a3014` (§5, re-measured 2026-11-24 19:39 after #893 opened the admission channel)
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

032 §1–§5 (the dispatch channel is closed) **is no longer unaffected**: `#893` opened the channel at 2026-11-24 14:13:58, and `AID-2026-055` through `AID-2026-058` have already used it. Section-by-section re-judgement in §5.3.

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

## 5. 032 §1–§5's premise has lapsed: #893 opened the admission channel, and two work items have used it

**The original text of this section was already out of date on the day it merged.** This is not a retrospective claim; it is the timeline:

| Event | Commit | Time (+0800) |
|---|---|---|
| The two assertions in this section were measured | `main = 2059c8105` | 2026-11-24 14:03:58 |
| `#893` adds a sixth rule to admission | `e8948654f` | 2026-11-24 14:13:58 |
| `AID-2026-055` registered through that channel and merged (`#896`) | `84bbe9241` | 2026-11-24 14:51:52 |
| This file merged (`#897`) | `3026b319b` | 2026-11-24 15:12:35 |

Ten minutes between the measurement and its lapse; one hour between the lapse and the merge. **The section was right when written** — re-run on `2059c8105`, both assertions reproduce word for word (left column of 5.1). What was wrong was presenting an absolute measurement as a current fact, while main advanced one more commit between measurement and merge. This is precisely the lesson this file writes down in §8.5 ("absolute counts expire ... re-run when reviewing, do not quote this file's line numbers"), except this time the error is in the body, not in an appendix.

### 5.1 Three assertions, re-measured one by one

`scripts/ci/check_repository_hygiene.py:79-81` now reads:

```python
WORK_ITEM_MANIFEST_RE = re.compile(
    r"14-ai-development/work-items/AID-\d{4}-\d{3}/manifest\.yaml"
)
```

The `if WORK_ITEM_MANIFEST_RE.fullmatch(path): return True` at `:197` was added by `#893`, after the `.github/actions/` rule and before the final `return False`. `#915` (`a7c5cd2`) then tightened the ID segment from `[A-Za-z0-9][A-Za-z0-9._-]*` to `\d{4}-\d{3}`, on the grounds that `AID-<anything>` would admit spellings the registry cannot allocate.

**Before and after, same command, two measurement points:**

| # | Location | Before: `main = 2059c8105` (2026-11-24 14:03:58) | After: `main = 01a3014` (2026-11-24 19:39:28) |
|---|---|---|---|
| 1 | code block line 1 of this section | `is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')` → **`False`** | → **`True`** |
| 2 | code block line 2 of this section | `is_allowed_new_path('14-ai-development/governance-register/X.md')` → **`True`** | → **`True`** (value unchanged, meaning changed: no longer "only `.md` gets through", but "`.md` and work-item manifests both get through") |
| 3 | the conclusion of this section | "no new work order can be registered" still holds; "no work order now wants registering" | **both false**: `AID-2026-055` through `AID-2026-058`, four items, are all registered |

Reproduction commands (both import the real script and call the real function; neither reads the code):

```
# before: take the script at 2059c8105 and import it in isolation
$ git show 2059c8105:scripts/ci/check_repository_hygiene.py > /tmp/hyg2059t/check_repository_hygiene.py
$ cd /tmp/hyg2059t && python3 -c "import check_repository_hygiene as h; \
    print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')); \
    print(h.is_allowed_new_path('14-ai-development/governance-register/X.md'))"
False
True

# after: import directly on a checkout of 01a3014
$ python3 -c "import sys; sys.path.insert(0,'scripts/ci'); import check_repository_hygiene as h; \
    print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')); \
    print(h.is_allowed_new_path('14-ai-development/governance-register/X.md'))"
True
True

# the regex itself
$ python3 -c "import re; R=re.compile(r'14-ai-development/work-items/AID-\d{4}-\d{3}/manifest\.yaml'); \
    print(bool(R.fullmatch('14-ai-development/work-items/AID-2026-099/manifest.yaml')))"
True
```

### 5.2 The channel is not merely open; it has been used four times

| Work item | Registration commit | Time (+0800) | Evidence |
|---|---|---|---|
| `AID-2026-055` | `#896`, merge `84bbe9241` (head `5585d95`) | 2026-11-24 14:51:52 | adds `14-ai-development/work-items/AID-2026-055/manifest.yaml` + `prompt-v1.md`, and modifies `INDEX.md` |
| `AID-2026-056` | `5d83b3c` (`#908`) | 2026-11-24 17:03:50 | adds `14-ai-development/work-items/AID-2026-056/manifest.yaml` |
| `AID-2026-057` | `b3a65e5` | 2026-11-24 18:38:00 | adds `AID-2026-057/manifest.yaml` + `prompt-v1.md` |
| `AID-2026-058` | `01a3014` | 2026-11-24 19:39:28 | adds `AID-2026-058/manifest.yaml` + `prompt-v1.md` |

**These four numbers are also just a snapshot at one measurement point.** `057` and `058` merged during this very revision — the first draft of §5 measured two at 18:32, and the re-measurement at 19:39 found four. That is the section's own argument happening to the section while it was being written; so it says "four as of `main = 01a3014`", not "four".

The first line of `AID-2026-055`'s `manifest.yaml` is `work_item_id: AID-2026-055`; `AID-2026-056`'s is `work_item_id: AID-2026-056`. Both carry a full `class` / `risk` / `risk_rationale` / `status: DISPATCHED` / `base_commit_sha`; neither is a placeholder directory:

```
$ git ls-tree --name-only origin/main 14-ai-development/work-items/ | grep -E 'AID-2026-05[5-8]'
14-ai-development/work-items/AID-2026-055
14-ai-development/work-items/AID-2026-056
14-ai-development/work-items/AID-2026-057
14-ai-development/work-items/AID-2026-058
$ git show origin/main:14-ai-development/work-items/AID-2026-055/manifest.yaml | head -1
work_item_id: AID-2026-055
$ git show origin/main:14-ai-development/work-items/AID-2026-056/manifest.yaml | head -1
work_item_id: AID-2026-056
```

**A fact that follows:** the measurement point of §8 in this file is `main = 84bbe9241` — which is exactly the merge commit that registered `AID-2026-055`. That is, §8 was measured on a tree that **already contained a work order registered through the very channel** that §5 of the same file asserted refuses work orders. Two conclusions live in one document, one measured at `2059c8105` and one at `84bbe9241`, 48 minutes and one commit apart.

### 5.3 So 032 §1–§5 is re-judged section by section

032 is about the **dispatch channel**; this file is about four corrections. The two intersect only at §5, so the re-judgement is per section rather than one blanket "unaffected":

| 032 section | What it says | Now |
|---|---|---|
| §1 | "since `cfcafc98a`, no new AID work order can be registered" | **Does not hold.** `#893` added the `WORK_ITEM_MANIFEST_RE` rule; `AID-2026-055` (#896), `AID-2026-056` (#908), `AID-2026-057` and `AID-2026-058` are registered. |
| §2 | timeline: 054 manifest `a3c6280aa` (11-23) / whitelist `cfcafc98a` (11-24) / attempt to register 055 | **The facts hold** — all three dates and commits are unchanged. But their role was to witness §1, whose conclusion is now refuted, so the table now proves only "the whitelist is a day later than 054", not "the channel is closed". |
| §3 | the whitelist admits "five classes"; "`manifest.yaml` is in none of them" | **The table is no longer complete**: there is now a sixth rule. The descriptions of the first five are still accurate one by one, and `ALLOWED_DOCUMENT_SUFFIXES` / `ALLOWED_SOURCE_SUFFIXES` / `ALLOWED_CONFIG_PATHS` were not touched by `#893` (its PR body says explicitly "No global `.yaml` suffix"). |
| §4 | why this session did not widen that line itself | **Holds as a decision record**: it did refuse to change gate source from the position of the party that needs it, and the reason (the only party that wants the door open is the only party with an incentive to open it wider than needed) is valid independently of the conclusion. Its "the change needed is one line" was in fact done by `#893` and then tightened by `#915`; the wait for "one minute after the widening lands" is over. |
| §5 | "nobody tested the intersection: when the whitelist landed, nobody also tested 'can the existing work-order shape be created again'" | **The statement holds** — `#844` did land the whitelist without testing that, and `AID-2026-055` being refused by CI in `#887` is the evidence of the untested gap. **But "this is a currently existing defect" does not hold**: `#893` fixed it. |

**So this file withdraws the sentence at the end of §1, "032 §1–§5 is unaffected"**: §1's conclusion is refuted by fact, §3's enumeration is incomplete, and §2/§4/§5 have statements that still hold but no longer support the original conclusion.

This file does not edit 032's body and does not fill its `register_closure` — neither is in this session's authority (consistent with §6). 032 needs its own erratum; this file only records that its premise has lapsed, and points at `#893`, `#896`, `#908` as the three reviewable commits.

**This is not hindsight fault-finding.** When this section was written, both assertions were true on `2059c8105`, and `#892` really had not touched the whitelist. The mistake was writing "still holds" where "true at this instant" was meant, without putting the measurement point into the sentence itself — `Measured at: main = 2059c8105` sits at the top of the page, and the reader has to align it with "still" unaided. For a document whose every conclusion carries a measurement, this is the failure it most needs to guard against: measured correctly, tensed wrongly.

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

# 5. admission now admits work orders (this step edited 2026-11-24; originally False at main = 2059c8105)
python -c "import sys; sys.path.insert(0,'scripts/ci'); import check_repository_hygiene as h; \
  print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml'))"
-> True
# the same command on 2059c8105 -> False (#893 added the sixth rule at 14:13:58)
```

---

## 8. The gate does not read content — this time it was run, not read

The "it only checks existence" judgement in §4 came from **reading the source**. This section runs it. Method: on a separate worktree of `origin/main`, each case does `git reset --hard origin/main`, makes exactly one commit, and calls `scripts/check_bilingual_docs.py` with real `BASE_SHA` / `HEAD_SHA`, recording the exit code and every `::error::` line.

### 8.1 Eight cases

| # | Mutation | Files changed | Exit | What stopped it |
|---|---|---|---|---|
| control | no change at all | 0 | **2** | `NOT_APPLICABLE` (zero changed paths) |
| A | delete `docs/zh-CN/` of a REAL pair | 1 | **1** | `changed without paired change` |
| B | overwrite `docs/zh-CN/` with the English text | 1 | **1** | `changed without paired change` |
| C | delete `docs/zh-CN/` of `023` (source CJK 0) | 1 | **2** | `New bilingual gap outside frozen baseline` |
| D | delete `docs/zh-CN/` of `PR425-001` (source CJK 1057) | 1 | **1** | `changed without paired change` |
| **F** | edit source + `docs/en/` + `docs/zh-CN/`, and make `zh-CN` a byte-identical copy of the English file | 3 | **0** | **nothing** |
| **G** | same, but replace every CJK character in `zh-CN` with `X` | 3 | **0** | **nothing** |
| H | edit the source **and** delete `docs/zh-CN/` of `PR425-001` | 2 | **1** | `requires all counterparts changed` |
| I | edit the source **and** delete `docs/zh-CN/` of `023` | 2 | **2** | `New bilingual gap outside frozen baseline` |

### 8.2 F and G are the conclusion

F and G turn a genuine Chinese mirror into text containing no Chinese at all (G leaves not one CJK character), and the gate **exits 0**. This is not "one edge case was missed": **no line of code reads the content of `docs/zh-CN/`.** What §4 called "existence is the whole criterion" now has executable evidence rather than a source-reading inference.

Note the difference between F/G and B. B is caught, not because its content changed, but because **only one side changed**. Turn B into F by touching both sides and the same content destruction stops being intercepted. The rule that catches B is the pairing rule, not a content judgement. That distinction matters: replacing a mirror with English text is completely invisible as long as the same commit also touches the source file.

### 8.3 "Deleting the Chinese mirror goes unannounced" is false

A parallel measurement after §4 produced this inference: `023` (source CJK 0) reports a gap when its `zh-CN` is deleted, while `PR425-001` (source CJK 1057) does not — "deleting the Chinese mirror produces no warning". **Measurement refutes it**: D and H both fail with a non-zero exit.

That inference evaluated only the **gap predicate**, while the gate has **two** independent mechanisms: the gap predicate, and "a changed path must have a paired change". The `PR425-001` deletion is stopped by the second. Treating one of two mechanisms as the whole produces exactly that kind of "no warning" conclusion — an error that has already occurred twice in this session (reading the wrong process's `EXIT`, and inferring `PARTIAL_SIDE_BY_SIDE_PAIRS` reachability from the predicate alone). Hence this section's method: **one real invocation per conclusion, with the exit code written into the table.**

### 8.4 Two disjoint populations

`scripts/bilingual-baseline.txt` holds 80 lines: 3 comment lines plus **77** frozen entries, matching the `77 frozen` the gate prints, and explaining the 77-versus-80 pair of numbers in §4.

The point: **not one of those 77 baseline entries is among the 7 content defects.**

| Population | Criterion | Count | Overlap |
|---|---|---|---|
| Baseline (frozen) | one side **does not exist** | 77 | — |
| Content defect | both sides **exist**, but `zh-CN` is not a translation | 7 | **0** |

The two cannot intersect by construction: the baseline records a missing side, a defect is a present-but-wrong side. So `AID-2026-054`'s effort to drive the baseline from 77 down to 11 **has no effect whatsoever on those 7 files** — it is cleaning a different population. That is not a fault in 054, whose goal was never content; but it shows that "baseline emptied" does not mean "bilingual is sound", and no current metric looks at both at once.

### 8.5 Absolute counts expire; this one is 124, not 123

§4 recorded 123 pairs. Re-measuring gives **124**, because main gained new bilingual files between the two measurements (this file is itself a pair). Of the 124: `en` side with `>=100` CJK is still **1** (`PR425-001`), `en` side with `1..99` CJK is **56**, and **both sides zero CJK** is **3** (`018`, `023`, `019`).

Those 56 are not defects: a few Chinese terms or citations inside an English document is normal. They are listed to show that "the `en` side contains Chinese" is not by itself a usable signal — only `>=100` is, which is the threshold `_carries_chinese()` already uses.

**So this file claims no absolute number is durable.** Every figure corresponds to one enumeration on `main`; the commands are in §7. Re-run them rather than quoting line numbers from this file.

### 8.6 What this section establishes

1. The gate never reads the content of `docs/zh-CN/`. Proven by F and G.
2. Deleting a mirror **is** intercepted, by the pairing rule rather than a content rule. Proven by D, H, I.
3. Content destruction is **not** intercepted when it happens alongside a source-file edit. Proven by F and G.
4. The 77 baseline entries and the 7 content defects are disjoint populations; shrinking the baseline cannot fix content.
5. Therefore check (a) proposed in GAP-24 §3, if implemented, fills exactly the hole in item 3; it neither replaces the baseline nor is replaced by it.

