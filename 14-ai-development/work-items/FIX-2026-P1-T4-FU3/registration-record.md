# FIX-2026-P1-T4-FU3 — INDEX registration record

This file records the execution of `authorization-manifest.yaml` §8, which deferred the
INDEX row for this work item and attached terms to the deferral. The terms required the
row to be written after the merge, from binding facts, with no pending assertion at the
moment of writing.

## Authorization

    authority: FIX-2026-P1-T4-FU3/authorization-manifest.yaml §8 ("scope: its own
               authorization, one path")
    decision:  DEC-FIX-2026-P1-T4-FU3-GO-001 (self-issued coordinator decision)
    note:      self-issued; not an Owner approval and not an independent authorization.

§8 stated the terms as: responsible party, trigger, condition, scope, and that the deferral
expires with the registration. This record is that registration, executed on the trigger.

## Binding facts written into the row

| Fact | Value | How obtained |
|---|---|---|
| merge commit | `691210f9ebe69dc7491cedd377c5932315e51825` | `GET /pulls/295` after merge |
| merge time | `2026-11-19T19:00:50Z` | same |
| merge parents | `4c52f42a` (pre-merge main tip) + `1109e4df` (exact Head) | `git show -s --format=%P` |
| merged file blobs | `88fab752` (test module), `8b7ed8b5` (manifest) | `git ls-tree` on the merge commit |
| untouched upstream blobs | `93f3f0d5` checker, `c515636e` template, `bbc1d546` policy, `ef3b951d` INDEX | same read-back |
| review chain | R1 `a4edd31` NEEDS-REVISION (1xP1/2xP2/1xP3) → `1109e4d` → R2 PASS | comment `7019054347` |
| exception | RULING-06, Actions billing interruption, `UNATTRIBUTED` | comment `7019087033` |
| acceptance | §2.1 four-line record | comment `7019087688` |
| post-merge verification | parity 2/2, four untouched files unchanged | comment `7019106398` |

Every value above was read after the merge. Nothing in the row asserts a pending state, so
the row cannot be stale by construction — that was the whole reason for deferring it.

## What the row deliberately still says is unresolved

The row records that the verbatim case is insensitive to the path base **by construction**,
and that this is documented rather than eliminated. Writing "tests added, gap closed" would
have been the more comfortable sentence and the less true one: the gap is covered by two
other cases, not removed from the case in question.

It also records that the checker is still unwired, so the policy has no automated
enforcement. A row that omitted that would let a later reader conclude from the presence of
tests that enforcement exists.

## Verification

- `INDEX.md`: one line added, 14 rows (was 13). `git diff` is a single insertion, so the
  other 13 rows are byte-identical.
- No other file changed.
