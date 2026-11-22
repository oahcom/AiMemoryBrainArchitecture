# GAP-22 — The document-management gate is red on `main`

**Status:** OPEN — pre-existing, reproduces on `550bb864` without any branch
**Discovered:** 2026-11-22, while verifying AID-2026-049
**Severity:** P2 — a gate that is already red cannot detect a regression
**Owner:** NOT_ASSIGNED

## What happens

```
$ python3 scripts/check_document_management.py
FAIL: 1 error(s)
  14-ai-development/adr/OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md: DM-10
  14-ai-development/adr/OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md did not exist at
  approved_version da15eeb6cbc5; the approval cannot be bound to that version
GOV-DOC-002: 613 governed documents, 49 classified, 564 unclassified
```

Exit code `1`.

## Reproduced on `main`, not caused by any branch

Run in a clean worktree at `550bb864` (`fix(bmcp): one cumulative write budget`),
with no local modifications:

```
$ git log --oneline -1
550bb864 fix(bmcp): one cumulative write budget, and stop writing when it runs out (#664)

$ python3 scripts/check_document_management.py
FAIL: 1 error(s)
  ... OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md: DM-10 ...
GOV-DOC-002: 613 governed documents, 49 classified, 564 unclassified
```

The same command on the PR #678 branch reports `614` governed documents and
**the same single error**. The count rises by one because the branch adds one
governed document (`AID-2026-049/manifest.yaml`); the error set does not change.

## What DM-10 is checking

DM-10 binds an approval to the exact document version that was approved. The
ruling records `approved_version: da15eeb6cbc5`, but
`OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md` does not exist at that
commit. So either:

- the file was created after `da15eeb6cbc5` and the approval is bound to a
  version that never contained it, or
- the file existed under a different path at that commit, and the approval
  points at the wrong one.

Both are record-keeping errors, not code errors. Deciding which requires reading
the history of that ruling, which is an accountability question rather than a
mechanical one — a checker cannot resolve it, and neither can a contributor
guessing at intent.

## Why this matters more than one red line

A gate that is red on `main` stops being a gate. Every subsequent PR learns to
say "that failure is pre-existing", which is true and is also how a real
regression gets waved through. The 564 unclassified documents (`06-memory-context:
0/21 classified`, `13-engineering-decisions: 0/58 classified`) are the same
problem in aggregate: the register is not maintained, so the gate cannot
distinguish a new violation from the standing backlog.

## Why it was not fixed in PR #678

Fixing DM-10 means deciding what the approval was actually bound to, which is an
accountability decision with an owner. AID-2026-049 authorises
`crates/memory-context` and two coverage rows; it does not authorise rewriting a
governance ruling's approval binding.

## What closing this requires

1. Decide whether `da15eeb6cbc5` is the intended approval version.
   - If yes: the file must exist at that commit — find where it lived, or
     re-issue the approval against a commit that contains it.
   - If no: correct `approved_version` to a commit that does contain the file.
2. Record the decision, since it changes what an existing approval means.
3. Re-run the gate and require exit `0` on `main` before any new document work
   is merged, so the next red is a real one.
4. Separately: bring `06-memory-context` (0/21) and `13-engineering-decisions`
   (0/58) into the classified register, or record why they are exempt.

## Acceptance for closing this

- `python3 scripts/check_document_management.py` exits `0` on `main`.
- The approval binding for `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md` is
  either correct or explicitly withdrawn, with the choice recorded.
