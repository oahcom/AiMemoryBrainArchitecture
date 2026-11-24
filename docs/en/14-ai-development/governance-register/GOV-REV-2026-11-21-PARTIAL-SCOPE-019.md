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
      last_verification_note: "Section 7 added on 2026-11-24 at main 5c64e560: the floor from AID-2026-054 Change 3 was patched into a throwaway worktree and the predicate was evaluated on two constructed pairs (a 1-line English fixture, and a full-English + partial-Chinese pair); the four register/branch configurations were evaluated in both trees; and the 43-pair / 86-file calibration was enumerated at 880e6a78 and again at 5c64e560. Every figure came from a run."
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
    source: "14-ai-development/governance-register/GOV-REV-2026-11-21-PARTIAL-SCOPE-019.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-21-PARTIAL-SCOPE-019.md"
---

# GOV-REV-2026-11-21-PARTIAL-SCOPE-019

**Status:** OPEN — MEASUREMENT ONLY, §7 added 2026-11-24
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = fa9c32a7f7`
**Corrects:** my own reading of PR #485 recorded in `GOV-REV-2026-11-21-GATE-MUTANTS-016.md` §2.3
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. What I got wrong

In register 016 §2.3 I wrote:

> `PARTIAL_SIDE_BY_SIDE_PAIRS` **is** covered: `test_gate_normative_roots.py` lines 549/562 add entries and line 577 asserts the register is empty at rest.

That statement about test coverage is true. What I implied — that the control meaningfully closes the "1-CJK character counts as a translation" hole from register 013 §3.1 — is **false**. Two measurements show why.

---

## 1. The register cannot reach the diff domain

`PARTIAL_SIDE_BY_SIDE_PAIRS` has exactly two references in `scripts/check_bilingual_docs.py`:

```
44:PARTIAL_SIDE_BY_SIDE_PAIRS: set[frozenset[str]] = set()
305:                and frozenset((source, side_by_side)) in PARTIAL_SIDE_BY_SIDE_PAIRS
```

Line 305 sits inside `current_bilingual_gaps()` — the **gap scan**. Counting references inside `check_normative_pairing()` (the **diff domain**, the one CI actually enforces on a PR):

```
count of references inside check_normative_pairing: 0
```

So a pair registered as partially translated still satisfies `check_normative_pairing()`. The register suppresses the *inventory* view of a bad pair and leaves the *enforcement* view untouched.

**Practical consequence:** for a PR that edits both sides of a registered partial pair, the gate still passes, because the diff domain never asks whether the pair is partial.

## 2. The register cannot reach the frozen baseline either

The gap scan enumerates only Markdown:

```
292:        for path in sorted(root.rglob("*.md")):
```

and then subtracts the baseline. So the register's effect is confined to **newly added pairs that are not already in the baseline**.

Measured: of the 77 baseline entries, how many form a side-by-side pair with both sides in the baseline?

```
baseline entries: 77
baseline pairs (both sides in baseline): 0
```

**Zero.** Not one baseline entry pairs with another baseline entry. So `PARTIAL_SIDE_BY_SIDE_PAIRS` has no effect on any of the 77 frozen gaps — it cannot retro-fix them, and it cannot make them worse.

That is consistent with register 015 §3: the frozen entries are either embedded-bilingual files with no sibling, or mirror-form files with no sibling. There is no side-by-side pair among them to register.

## 3. What the control actually covers

| Scenario | Register helps? |
|---|---|
| new `X.md` + `X.zh-CN.md` pair with 1 CJK char, registered as partial | **only until `AID-2026-054` lands** — see §7.2 |
| new realistic partial pair (full English, partial Chinese), registered | **yes** — neither side is a gap in the scan |
| new pair, not registered | no — accepted (register 013 §3.1) |
| existing baseline pair, registered | **n/a — no such pair exists** |
| a PR editing both sides of a registered partial pair | **no** — diff domain never consults the register |

So the control is a **declaration mechanism for new pairs**, and it works only in the direction of the gap scan. It is a real control with a real test, and it is narrower than the commit message on `#485` implies:

> "A pair registered as partially translated does not count as paired even though it carries CJK. That closes the '10% translated, passes `_has_any_chinese`, counted as done' case, which is the next hole after the one that was just closed."

That sentence is true **for the inventory**. It is not true for PR enforcement. A pair registered as partial can still be merged with both sides edited, and the gate will not object.

## 4. Why this matters less than it sounds, and more

**Less:** register 013 §3.1's finding stands unchanged. A 1-CJK pair is still accepted unless someone registers it. The register is an available remedy, not an automatic one. Nothing in 013 needs retraction.

**More:** the pattern is the same as registers 011/015/017. A mechanism is added to the gap scan and not to the diff domain, so the two views diverge again. This is now the **fourth** instance of the same divergence:

| # | Mechanism added to the gap scan | Also in the diff domain? |
|---|---|---|
| 011 | side-by-side acceptance | **no** |
| 015 | embedded-bilingual recognition | no (and 14-only in the scan) |
| 017 | suffix filtering | no (14-only in the diff domain) |
| **019** | **`PARTIAL_SIDE_BY_SIDE_PAIRS`** | **no** |

Every fix to the inventory has widened the distance between the two views. The gate now has two policies, and each one has been patched independently of the other.

## 5. What this register does not claim

- It does not claim `#485` is broken. It adds a real control with a real test.
- It does not claim the register should be consulted by the diff domain. That is a design decision requiring authorisation.
- It does not retract register 013 §3.1 or §3.2. Those findings are unchanged.
- It does not retract the M4 result in register 016 — M4 is still killed, and that test is still real coverage.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

---

## 6. Reproduction

```
repo:    oahcom/AiMemoryBrainArchitecture
commit:  fa9c32a7f7
cwd:     repo root

# 1. the register never appears in the diff domain
grep -n 'PARTIAL_SIDE_BY_SIDE_PAIRS' scripts/check_bilingual_docs.py
-> 44:  declaration
-> 305: inside current_bilingual_gaps()

awk '/^def check_normative_pairing/,/^def [a-z_]+\(/' scripts/check_bilingual_docs.py \
  | grep -c PARTIAL_SIDE_BY_SIDE_PAIRS
-> 0

# 2. no baseline entry pairs with another baseline entry
python -c "
import sys,os;sys.path.insert(0,os.path.join(os.getcwd(),'scripts'));sys.argv=['x']
import check_bilingual_docs as g
bs=set(g.read_baseline())
print(len(bs), sum(1 for b in bs if g.side_by_side_partner(b) in bs))"
-> 77 0
```

No CI, no API quota required.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 7. Correction, 2026-11-24: the register survives the floor, but its test does not

**Measured at:** `main = 5c64e560`. **Supersedes an inference I recorded earlier in this session and never published as a finding.**

I had reasoned: `AID-2026-054` makes the side-by-side predicate require `cjk >= 100 and latin >= 1000`; the register only ever subtracts from a `True` predicate; therefore the floor makes the register unreachable. **Only the first two premises are true.** The conclusion is false, and the measurement that settles it is cheap.

### 7.1 A real partial pair still clears the floor

The floor is applied to the **pair**, not to one side — `AID-2026-054` §1 Change 3 says explicitly "a 50/50 split and a 0/100 split are both legitimate". So a pair must be measured as a pair:

| pair | cjk | latin | clears the floor | `_side_by_side_bilingual` | register decisive? |
|---|---|---|---|---|---|
| the fixture in `test_partial_side_by_side_pair_rejects_both_sides` | 200 | **28** | **no** | `False` | **no** |
| a realistic partial pair (full English + partial Chinese) | 270 | 4560 | **yes** | `True` | **yes** |

The second row is the case the register exists for. It clears the floor because the untranslated half is English, and English letters count toward `latin`. **The register is not dead code under the floor.** My inference was wrong.

### 7.2 What the floor actually breaks: the test, not the control

The repo's only regression test for the register builds a pair whose English side is one sentence — 28 Latin letters, far under the floor's 1,000. Under the floor that pair is rejected by the **predicate**, before `partial_side_by_side` is consulted. The assertion is "both sides are gaps", which is then satisfied for a reason that has nothing to do with the register:

```
asserts: EN in gaps AND ZH in gaps

configuration                        EN gap  ZH gap  result
register present, branch present     True    True    PASS
register present, branch REMOVED     True    True    PASS   <- mutant not killed
register absent,  branch present     True    True    PASS
register absent,  branch REMOVED     True    True    PASS
```

The same four configurations on today's tree (no floor), same fixture:

```
configuration                        EN gap  ZH gap  result
register present, branch present     True    True    PASS
register present, branch REMOVED     False   False   FAIL   <- mutant killed
register absent,  branch present     False   False   FAIL
register absent,  branch REMOVED     False   False   FAIL
```

So the discriminating power of the test is **2 outcome vectors before the floor, 1 after**. The floor does not make the register unreachable; it makes the register's only test unable to fail. That is a different defect, it lands inside `AID-2026-054`'s acceptance set, and no criterion in that work order covers it: criterion 8 says "the existing 86 accepted pairs still pass" and criterion 9 only forbids the pre-existing failure count from growing. A test that still passes still counts as a pass.

### 7.3 The sibling test was already tautological

`test_partial_side_by_side_registration_does_not_block_mirrors` asserts that a registered partial pair with full `docs/en` + `docs/zh-CN` mirrors is **not** a gap. It writes both mirrors before asserting, so `mirrored` is `True` and `paired = mirrored or (...)` short-circuits. Measured: **all four configurations give `gap=False`, with and without the floor.** That test has never been able to fail, and the floor is not implicated. It is recorded here because it sits in the same block and a reviewer reading §7.2 would otherwise assume this one still works.

### 7.4 Correction to `AID-2026-054`'s calibration claim

The work order states: "All 86 accepted pairs in the tree have a shorter side of at least 1,364 characters; the 10 shortest run 1,364–2,214." Measured at the work order's own `base_commit_sha` (`880e6a78`) and again at `5c64e560`:

| quantity | claimed | measured at `880e6a78` | measured at `5c64e560` |
|---|---|---|---|
| accepted side-by-side units | "86 pairs" | **43 pairs / 86 files** | 43 pairs / 86 files |
| shortest side, minimum | 1,364 | **1,364** | 1,364 |
| 10 shortest, upper end | 2,214 | **4,412** | 4,412 |

The minimum is right and it is what the floor depends on, so **the floor's safety argument stands**: a floor of 100 rejects none of the 43 pairs. The two defects are (a) "86" counts files while the word is "pairs", and (b) the 10-shortest upper bound is off by a factor of two — 2,214 is the **second** entry, not the tenth. Neither changes the ruling; both would mislead an implementer who checks criterion 8 by asserting `86` against a pair count and gets `43`.

### 7.5 Status

`OPEN` — unchanged. §1's two measurements were re-run today and both still hold (`0` references inside `check_normative_pairing()`; `0` baseline entries whose partner is also in the baseline). What changed is §3's first row: "new pair with 1 CJK char, registered as partial → yes, both become gaps" becomes **"no — the floor already rejects it"**, while the row for a real partial pair is still served by the register. The control is narrower than §3 says and stronger than my inference said.
