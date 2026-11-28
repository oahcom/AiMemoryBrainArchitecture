---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every measurement in this file was run in this session against origin/main at 073ffe3e: the table-shape enumeration, the four union-merge shapes in throwaway repos, the end-to-end gate runs, and the two mutation checks. The quoted outputs are copied from those runs."
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
    source: null
    en: null
    zh-CN: null
---

# Session role / use case

IMPLEMENTER. Issues #1064 and #1069 report two halves of one problem: `INDEX.md`
conflicts on every concurrent registration, and a duplicate work-item ID is
detected only by that conflict. This session added the union merge driver and
the check that makes it safe, and nothing else.

The two are one change because either alone is worse than neither. A union
driver without the duplicate check turns a visible conflict into two rows
claiming one `AID`; the duplicate check without the driver leaves the merge
conflict that motivated #1069. This record exists to make that pairing
reviewable, not to describe a broader change.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the assignment
this change was carried out against, pinned at
`52a28e7d78ee3e7e3620017bf7fbec676f2b73176927a84a2fe555d222ce1961`, 4141 bytes.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
session read. It was assembled after the session from the assignment actually
executed, and that is stated rather than presented as a frozen snapshot.

**Read before writing:**

| input | what it settled |
|---|---|
| `14-ai-development/work-items/INDEX.md` | the table is one row per work item, no multi-line cells and no wrapping — the precondition for `merge=union` being safe at all (section "Step 0" below) |
| `scripts/check_traceability.py` | `validate_index_and_manifests` reads only the tree; `run_check` calls `parse_registry` first inside the same `try`, which is why the four T-04 assertions were unreachable (#1071) |
| `00-governance/requirements-registry.yaml` | absent from the repository — the reason the unreachability is total, not intermittent |
| `.github/workflows/repository-hygiene.yml` | `Repository hygiene (hard gate)` is a required context; a step added there runs on every PR |
| Issue #1064 body | the alternatives it lists (reservation registry, allocator); both were skipped in favour of a check on what already exists |
| Issue #1069 body | the proposed `merge=union` mechanism, and that it is the smallest fix for the conflict |

# What was added

```
.gitattributes                                          one rule + 30 lines of caveats
.github/workflows/repository-hygiene.yml                one step, in the existing required job
scripts/check_traceability.py                           --index-only entry point, 49 lines
scripts/test_check_traceability.py                      tests for it, 72 lines
14-ai-development/work-items/AID-2026-077/              manifest, prompt, this record
14-ai-development/work-items/INDEX.md                   one row + the driver's caveat block
```

# AI-visible output

The three measured outcomes are in the PR body verbatim: the union merge keeping
both rows, the duplicate being refused with `ERROR T-04 duplicate INDEX entry
AID-2026-073`, and the default path still exiting 1 without the registry. None of
the three was asserted from reading the code; each was produced by running it.

## Why these are one change

`#1069` asks for `merge=union` on `INDEX.md`. A union driver keeps both sides'
appended rows, which removes the false conflict — and removes the last
accidental duplicate-ID detector, because today a duplicate ID produces an
add/add conflict on the work-item directory. Shipping the driver alone converts
a visible conflict into an invisible duplicate row, which is strictly worse.
So the driver ships with an assertion that refuses the duplicate.

`#1064` asks for a gate that fails a duplicate. The assertion already exists
(`check_traceability.py:730`, `T-04 duplicate INDEX entry`). It has never run:
`run_check` parses `00-governance/requirements-registry.yaml` first inside the
same `try`, and that file does not exist, so the manifest half is dead code
(`#1071`). The fix is a caller for the assertion that exists, not a second
detector. This is the route both the Owner ruling on #1064 and the disposition
on #1071 prescribe.

## Step 0 — is the table a shape union can handle?

A union merge concatenates both sides' lines. If any row spans lines, a union
of half-rows parses as neither side. Measured on the committed file:

```
$ python - <<'PY'
import re
L = open("14-ai-development/work-items/INDEX.md", encoding="utf-8").read().split("\n")
rows = [(i+1, l) for i, l in enumerate(L) if re.match(r"^\| \[(AID-\d{4}-\d{3})\]", l)]
bad = []
for n, l in rows:
    if not l.rstrip().endswith("|"): bad.append((n, "no closing pipe"))
    if l.count("|") < 10:          bad.append((n, "cells=%d" % l.count("|")))
for i in range(rows[0][0]-1, rows[-1][0]):
    if not L[i].startswith("|"): bad.append((i+1, "non-pipe line inside block"))
PY
rows 47, block lines 43..96, violations []
continuation: no row line ends with a backslash
unique ids: 47
```

Every AID row is one line, closed, with the same cell count, and nothing
non-table sits inside the block. Union is safe for this file's row shape.

The file's own history also decides whether "two appends at EOF" is the case
that matters, or an edge case:

```
commits touching INDEX.md: 136
AID rows added: 61   mid-table: 45   at-end: 16
AID rows removed (deleted): 14
```

75% of additions are mid-table insertions, and rows do get deleted. A driver
whose contract is "two appends at EOF" would not describe this file.

## The change

1. `scripts/check_traceability.py` — new `run_index_check()`, selected by
   `--index-only`. It calls `validate_index_and_manifests` directly. The
   default path is byte-identical in behaviour: it still requires the registry
   and still exits 1 when it is absent. `authority_issues` is empty by
   construction, which can add T-05 warnings but cannot hide an error, because
   `verdict()` keys on `errors`.
2. `.github/workflows/repository-hygiene.yml` — one step in the existing
   `Repository hygiene (hard gate)` job: `python3 scripts/check_traceability.py
   --index-only`. No new workflow, no new required context, no `|| true`, no
   `continue-on-error`.
3. `.gitattributes` — `14-ai-development/work-items/INDEX.md merge=union`, and
   nothing wider. The comment names the three shapes union does not resolve and
   says the line is deleted in the same change that removes the check.
4. `14-ai-development/work-items/INDEX.md` — the driver's contract next to the
   table, in the file a resolver will be looking at when the check fails.
5. `scripts/test_check_traceability.py` — five tests, in the module that
   already exists.

Not built, deliberately: an ID reservation service, an allocator, a registry of
taken-but-unmerged IDs, a `next_id` cell, or a generated table. The first three
are rejected by #1064 as needing coordination this repository does not have;
the `next_id` cell would turn an append conflict into a same-cell conflict; the
generated table needs an order-stable duplicate-aware derivation first, which
is the same prerequisite this change already pays.

## Proof 1 — `merge=union` resolves two concurrent registrations, both rows kept

Scenario run against this file's own 50-row table, in a throwaway repo, with
the attribute from this change. Two branches insert a *different* row at the
same anchor (after the `AID-2026-073` row), then merge.

```
############ PROOF 1 — two different rows at the same anchor, WITH merge=union
before: 51 rows
merge exit=0
after:  52 rows
53:| [AID-2026-901](AID-2026-901/manifest.yaml) | ALPHA row |
54:| [AID-2026-902](AID-2026-902/manifest.yaml) | BETA row |
conflict markers: 0
rows=52 unique=52 dup=none
```

(The "before: 51" is 50 base rows plus the first branch's row: the merge is run
from the side that already has one of them.)

Same shape **without** the driver, for contrast:

```
############ PROOF 3 — the same shape WITHOUT the driver
merge exit=1
conflict markers: 1
14-ai-development/work-items/INDEX.md: merge: unspecified
```

## Proof 2 — the driver's silent failure mode, and that the check refuses it

Union de-duplicates identical lines and keeps **both variants** of a
disagreeing one. So the same ID appended on both sides does not conflict; it
becomes two rows.

```
############ PROOF 2 — the same AID, different content, WITH merge=union
before: 51 rows
merge exit=0
after:  52 rows
53:| [AID-2026-903](AID-2026-903/manifest.yaml) | 903 as session A |
54:| [AID-2026-903](AID-2026-903/manifest.yaml) | 903 as session B |
conflict markers: 0
rows=52 unique=51 dup=['AID-2026-903']
```

And the third shape — a deletion undone by an edit to its neighbour. This one
is worth its own measurement because the symptom is a row that came *back*, and
a resolver will not look for it:

```
############ PROOF 4 — row deleted on one side, its NEIGHBOUR edited on the other
A tree has 063: 0  (0 = deleted)
before: 49 rows
merge exit=0
after:  51 rows
063 rows after: 1   (1 = the deletion was undone)
062 rows after: 2   (2 = union kept both variants)
conflict markers: 0
rows=51 unique=50 dup=['AID-2026-062']
```

All three silent shapes end as **one AID on two lines**, which is exactly what
`T-04 duplicate INDEX entry` keys on. That is the property that makes the
driver safe, and it is a measured property of these three shapes, not an
assumption.

## Proof 3 — the check fails on a duplicate and passes on the clean tree

End-to-end, in a scratch repo carrying the real work-item tree and the real
checker. Two concurrent registrations, merged with the driver:

```
MERGE_EXIT=0
rows=52
PASS TRACEABILITY: 0 requirements / 52 work items / 0 errors / 86 warnings
TRACE_EXIT=0
```

Two sessions claiming the **same** ID, each with its own manifest, merged with
the driver, conflict resolved the way a resolver would (keep one manifest):

```
MERGE_EXIT=1                     # the manifest is add/add: the driver is INDEX-only
913 index rows=2
FAIL TRACEABILITY: 0 requirements / 52 work items / 1 errors / 86 warnings
ERROR T-04 duplicate INDEX entry AID-2026-913
TRACE_EXIT=1
```

On the real tree, appending a second `AID-2026-062` row:

```
$ python3 scripts/check_traceability.py --index-only
ERROR T-04 duplicate INDEX entry AID-2026-062
EXIT=1
$ # row removed
$ python3 scripts/check_traceability.py --index-only >/dev/null 2>&1
CLEAN_EXIT=0
```

And the `work_item_id`/directory half, by editing one manifest:

```
$ # AID-2026-062/manifest.yaml: work_item_id: AID-2026-062 -> AID-2026-062X
001. 14-ai-development/work-items/AID-2026-062/manifest.yaml -> ERROR T-04 manifest ... work_item_id='AID-2026-062X' does not match directory
EXIT=1
```

## Proof 4 — the check is reachable without the registry, and the default path is unchanged

```
$ python3 scripts/check_traceability.py --index-only
PASS TRACEABILITY: 0 requirements / 49 work items / 0 errors / 55 warnings
EXIT=0

$ python3 scripts/check_traceability.py
ERROR required registry unavailable: cannot read registry: ...
EXIT=1
```

The second line is the point of the split: `--index-only` narrows *which half
runs*, it does not make the registry optional. A missing registry is still an
error on the default path.

## Proof 5 — the tests fail if either half is reverted

```
# mutant 1: delete the T-04 duplicate call
Ran 41 tests ... FAILED (failures=2)
# restored
Ran 41 tests ... OK

# mutant 2: make run_index_check a no-op
FAIL: test_index_only_passes_without_a_registry
FAIL: test_index_only_reports_the_same_duplicate_the_default_path_does
FAIL: test_index_only_still_fails_on_a_duplicate_aid_row
FAIL: test_index_only_still_fails_on_an_id_directory_mismatch
Ran 41 tests ... FAILED (failures=4)
```

## Gates

```
$ python scripts/check_document_management.py --require-changed origin/main ; echo "EXIT=$?"
$ python scripts/ci/check_repository_hygiene.py ; echo "EXIT=$?"
$ python scripts/ci/check_line_endings.py ; echo "EXIT=$?"
$ python -m unittest discover -s scripts -p "test_*.py"
```

Results are in the PR body. `check_line_endings.py` is unaffected by the new
attribute, and that was measured rather than assumed: it asks Git via
`git check-attr --stdin` and never parses `.gitattributes` text.

## What this does not close

A collision between two sessions that have each written their files but not
merged is still invisible to everyone. Detecting that needs the open-PR list
and a `Work Item ID` field that something reads, which is #1042's subject. This
change catches the merged case — the one that happened three times in one hour
— and the residual is stated here rather than claimed as closed.
