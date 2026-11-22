---
document_metadata:
  domain: ai-development
  role: research

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "The two results are from the same commit measured two ways: tarball 1a7e3cddae (566 total, 13 DM-10 notes) and a git clone at 1a7e3cddae (567 total, 1 DM-10). The single real violation was confirmed with git cat-file -e against da15eeb and git log --follow for the file."
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

# GAP-25 — A degraded check and a passing check produce the same output shape

**Status:** Open · **Area:** measurement method, not code
**Measured at:** `main` @ `1a7e3cddae` (tarball) vs the same tree (git clone)
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. Two runs, one tree, different answers

The same commit, measured two ways:

| method | result |
|---|---|
| tarball unpacked, no `.git` | `FAIL: 566` — `564 DM-01`, `13 DM-10`, `1 DM-02`, `1 DM-13` |
| git clone, real work tree | `FAIL: 567` — `566 DM-01`, `1 DM-10` |

Neither number is wrong for its method. But I reported the first as if it were the second, twice, and the difference is not noise — it is one real defect that the tarball run could not see and 12 false ones it invented.

## 2. What the gate does without a work tree

```
note: DM-10 docs/en/00-governance/design-principles.md: approval binding NOT VERIFIED
      (no git work tree); run the gate inside the repository
...
note: no git work tree here, approval binding NOT VERIFIED
```

Thirteen notes. Twelve of them are documents whose binding was never checked. One — `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md` — was a real violation, and in a tarball run it is **indistinguishable from the other twelve**.

The real violation:

```
DM-10 ... did not exist at approved_version da15eeb6cbc5;
the approval cannot be bound to that version
```

`da15eeb6cbc5` is `feat(context): implement delivery lifecycle and ACK consumer`. The ruling first appears in `c9036544`. I had bound the approval to a commit that never contained the document — an approval of text that did not exist there. Fixed in `#676`.

## 3. The error is not "I used a tarball"

A tarball is a reasonable way to read a tree when `git fetch` times out against `github.com:443`, which it does here routinely. The error is that I read **the absence of a failure** as **evidence of correctness** in a run whose own output said the check did not execute.

The gate printed `NOT VERIFIED` thirteen times and I summarised it as "13 DM-10, all tarball artifacts." The word `VERIFIED` appears in the output, negated, and I counted the lines instead of reading them. That is the same mistake `GAP-20` §6 names one level up:

> A gate that is silent about a state is not the same as a gate that approves of it.

Here it is: **a gate that is *degraded* about a state is not a gate that approved it.** Silence and degradation both produce output that does not contain the word `FAIL` for that item, and I treated both as pass.

## 4. How to tell the two apart, concretely

Three rules, each earned by a specific miss in this session:

**(a) A `note:` is not a pass.** The gate uses `note:` for "did not check" and the absence of a line for "checked and passed." Counting error lines undercounts; counting `note:` lines and subtracting is the only arithmetic that works. For `check_document_management.py`, the reliable read is:

```bash
grep -c 'NOT VERIFIED' out.txt   # how many checks did not run
grep -c '^FAIL' out.txt          # whether the run is authoritative at all
```

If the first number is non-zero, the run cannot be cited as a baseline without saying so.

**(b) Reproduce the measurement in the environment the claim requires.** A claim about `approved_version` is a claim about git history. It cannot be tested without history, and no amount of re-reading the tarball will produce it. `GAP-23`'s numbers came from CI and were citable precisely because CI has the work tree; the same numbers from a tarball would have been unverifiable.

**(c) When a measurement contradicts a previous one, find the method difference before finding the defect.** I had two numbers, 563 and 566, and I explained the difference as "three docs commits landed in between." That was true and irrelevant — the difference that mattered was `13 DM-10` vs `1 DM-10`, which I did not look at because I had already explained the delta.

## 5. The tarball is still the right tool for most of this

To be precise about what should change: most of this session's measurements are unaffected. File counts, line counts, `todo!()` locations, schema inventories, the 22 message types, the md5 identity in `GAP-24` — none of them need git history, and all of them were correct from a tarball.

What needs a work tree is exactly one thing: **`approved_version` binding**, because it is a question about a different commit than the one being measured. That is a narrow requirement and it should be stated narrowly rather than as "always clone", which is advice I cannot follow reliably here — the clone took 5m27s and the subsequent `git fetch` timed out after 5m.

So the rule is: **for `DM-10`, either clone or report the number as unverified.** Not "clone always."

## 6. The count that should be quoted

At `1a7e3cddae`, on a work tree, before the fix:

```
FAIL: 567   ->  566 DM-01, 1 DM-10
```

After `#676`, the `1 DM-10` is gone; the 566 remains and is the real backlog. Every earlier statement in this session that said "563, all DM-01" or "566, all DM-01" was quoting a number whose `DM-10` component had not actually been checked.

That is worth writing down rather than quietly correcting, because the same sentence — "all DM-01" — will be written again by whoever measures next, and the way to make it true is to know which check was skipped to produce it.

## 7. Why this is a document and not a commit message

Because the defect it describes is in a method, not a file, and the method is what the next measurement will reuse. `GAP-20` §6 made the point about silence; this is the case where the gate was not silent — it said `NOT VERIFIED` thirteen times — and the reader (me) discarded the qualifier. A gate cannot defend against that. Only a written rule about what counts as a baseline can.
