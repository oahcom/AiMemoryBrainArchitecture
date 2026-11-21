# GOV-REV-2026-11-21-PARTIAL-SCOPE-019

**Status:** OPEN — MEASUREMENT ONLY
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
| new `X.md` + `X.zh-CN.md` pair with 1 CJK char, registered as partial | **yes** — both become gaps in the scan |
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
