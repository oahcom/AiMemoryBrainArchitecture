---
document_metadata:
  domain: ai-development
  role: review-report

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "The 81 gaps and the 77 baseline lines are both measured on a real git work tree, because check_bilingual_docs_full.py shells out to git ls-files and refuses to run without one. The set differences are comm over sorted path lists, not a count subtraction."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-28 (corrected) — Two bilingual checks, one baseline, and a full scan that covers less than the repository

**Status:** **Resolved** by `150fb45e` (#910)
**Measured at:** `main` @ `f292257a98`, on a real git work tree; resolution verified at `ac0f0dfd`
**Supersedes:** the first version of this document, whose central claim was wrong — see §1
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

> **Resolution note (2026-11-24, `ac0f0dfd`).** The two checks no longer hold divergent scope. `check_bilingual_docs_full.py` imports `NORMATIVE_ROOTS`, `EMBEDDED_BILINGUAL_SOURCES` and `PAIR_EXEMPT_PREFIXES` from the authority instead of copying them.
>
> Measured after the fix: gate A freezes 77 paths, gate B reports 77, and the two baselines are **byte-identical** — the 12-entry divergence this document measured is gone. Gate B's baseline moved 81 → 77: 8 false positives left (6 side-by-side, 2 exempt-but-unlisted) and 4 true positives entered (the unpaired `08-bmcp-protocol` records).
>
> One thing this document got right and #910 confirmed: the fix was never "lower the baseline". Lowering it alone was measured to produce `regressions=66`. The constants had to converge first.
>
> Only the Status is superseded. Do not re-fix the scope — that would undo #910.

---

## 1. What I got wrong

The first version of this document claimed that `scripts/bilingual-baseline.txt` contains four entries under `08-bmcp-protocol/` which the scan can never produce, because `NORMATIVE_ROOTS` says `08-protocols`. I concluded the baseline had four unreachable lines.

That is false. There are two bilingual checks, and the baseline belongs to the other one:

| script | reads `bilingual-baseline.txt` | scans `08-bmcp-protocol/` |
|---|---|---|
| `check_bilingual_docs.py` | **yes** — `BASELINE_PATH` at `:171` | **yes** — it does not use `NORMATIVE_ROOTS` |
| `check_bilingual_docs_full.py` | no | **no** — prefix-matches `08-protocols` |

Measured, on the same tree:

```
$ BASE_SHA=$(git rev-parse HEAD~1) HEAD_SHA=$(git rev-parse HEAD) python3 scripts/check_bilingual_docs.py
bilingual baseline: 77 frozen, 0 new gaps
```

`0 new gaps`. The 77 entries are frozen and the main gate is working exactly as designed. The four `08-bmcp-protocol` entries in the baseline are found by that gate, which is why they are in the baseline at all.

I compared a number from `check_bilingual_docs_full.py` (81 gaps) against a baseline consumed by `check_bilingual_docs.py` (77 frozen) and treated the difference as a defect in the baseline. It is a difference between two different tools.

## 2. What is actually true

**(a) The main gate is healthy.** `77 frozen, 0 new gaps`. Nothing to fix there.

**(b) The full scan covers less than the repository.** `check_bilingual_docs_full.py:14` declares fifteen `NORMATIVE_ROOTS`; seven have no directory:

```
03-memory-brain                no
05-memory-runtime              no
08-protocols                   no -- the directory is 08-bmcp-protocol
09-storage-and-index           no
10-security-and-governance     no
11-consistency-and-recovery    no
12-testing-and-acceptance      no
```

Sixteen files under `08-bmcp-protocol/` and its two mirrors are therefore outside the full scan's scope. This is `GAP-26`, unchanged and unshipped — `NORMATIVE_ROOTS` still reads `08-protocols` at `f292257a98`.

**(c) The full scan reports 81 gaps.** Of those, some are real and some are the same side-by-side shapes the main gate resolves. The two tools count different things, which is the next section.

## 3. Why the two tools disagree, and why that is not a bug

The main gate is **change-scoped**: it needs `BASE_SHA` and `HEAD_SHA`, it looks at what moved in that range, and it compares the resulting gap set against a frozen baseline. Run without those variables it refuses:

```
::error::Unable to determine changed paths: BASE_SHA and HEAD_SHA are required
```

That refusal is the `#635` fix working — before it, an unset environment produced a silent pass.

The full scan is **repository-scoped**: it walks every tracked `.md` and reports every missing counterpart, with no baseline and no diff. It is a coverage inventory, not a ratchet.

So `81` and `77` are answers to different questions:

- full scan: how many documents in the repository lack a counterpart, right now
- main gate: how many gaps exist in the files this change touched, against a frozen record

Neither number is wrong. Quoting one as if it were the other is what I did.

## 4. What should change

**Only `GAP-26`'s fix.** Correct the roots, delete the seven that do not exist, and add a check that a declared root has a directory. That widens the full scan's scope to match the repository.

**Nothing about the baseline.** Its 77 entries are frozen, they are found by the gate that owns them, and `0 new gaps` means it is doing its job.

**One documentation change, which is the real point of this document:** the two scripts should say in their own headers which of them owns the baseline. `check_bilingual_docs_full.py` currently says "path/coverage checker, not a semantic translation or Owner-approval checker" — accurate, but it does not say "this is not the ratchet, and `bilingual-baseline.txt` is not mine." A reader who runs both, as I did, gets two numbers with no indication of which is comparable to what.

## 5. The rule this produces

**Before comparing two counts, confirm they come from the same tool.** I had `81` and `77`, both plausibly "the bilingual debt," and I built a defect out of the difference. The check that would have prevented it is one grep:

```bash
grep -rn "bilingual-baseline" scripts/ .github/workflows/
```

which returns `check_bilingual_docs.py:171` and nothing in the full scan. One command, and the whole §1 of this document disappears.

This is the third variant of the same error in this session, and they are worth naming together:

| document | the error |
|---|---|
| `GAP-25` | read a degraded check as a passing one |
| `GAP-21` (corrected) | generalised a rule from three hand-found instances without counting the population |
| **this one** | **compared two counts from different tools as if they measured the same thing** |

All three are measurement errors that a single command would have caught, and all three produced a confident, wrong document before the command was run.

## 6. What survives from the first version

- **`GAP-26`'s finding** stands entirely: seven roots do not exist, sixteen files are unscanned. This document does not change it.
- **The `08-protocols` observation** is correct about the *full scan* and was wrong about the *baseline*.
- **The set-versus-count argument** for the ratchet is still worth considering on its own merits, but it is not motivated by anything measured here. I am dropping it rather than keeping a recommendation whose evidence turned out to be a mistake.

## 7. Why keep this at all

Because the wrong version was written, and the correction is more useful than silence. A reader who finds `GAP-26` and wonders why the full scan's 81 gaps do not match the baseline's 77 will now find the answer: they are different tools, and only one of them owns the baseline.
