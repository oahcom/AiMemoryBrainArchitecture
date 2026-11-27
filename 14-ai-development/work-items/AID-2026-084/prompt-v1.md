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
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count below was measured in this session at main dc826e4e, not copied from another record."
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

# AID-2026-084 — Make INDEX membership require a registry row, not any link

## The assignment, as given

You are an author session for a governed repository. Write the fix; verify it
by mutation; push a branch and open a PR.

The defect is issue #944. `scripts/ci/check_repository_hygiene.py` builds the
set of registered work-item directories with `LOCAL_LINK_RE` over the whole of
`14-ai-development/work-items/INDEX.md`, so every repository-relative link
anywhere in the file counts: in prose, inside an `<!-- -->` comment, inside a
fenced code block. The registry is a table, and the check accepts any text.

## The gap, measured

Measured at `origin/main` `dc826e4e`:

```
directories under 14-ai-development/work-items/          68
python3 scripts/ci/check_repository_hygiene.py           directories=68 linked=68, exit 0
table rows beginning with `|` in INDEX.md                132
rows naming a work-item directory                        71
non-row lines naming a work-item directory               0
non-row lines carrying any `](` link                     0
```

The assignment said 38 lines outside the table carry a link into a work-item
directory. That figure is not reproducible: at `dc826e4e` no line outside the
table carries a `](` link of any kind, and all 68 directories are named by the
71 rows that mention one. The numbers above are what the file actually
contains.

The 68 and the 68 are equal, so the check passes. They are equal by accident of
this file, not because the rule requires it: the predicate counts a link
anywhere, and here every link happens to sit in a row. Nothing enforces that,
so a row can leave the table and the count cannot notice. The reproduction the
Owner ran: wrapping the `AID-2026-081` registry row in `<!-- ... -->` removes the
visible row, and the check still exits 0 with `directories=68 linked=68` while
`grep -c '^| \[AID-2026-081\]'` returns 0. A row can be deleted from the
registry and the gate that exists to notice that says nothing.

## What this work item changes

`index_entry_directories` reads the index line by line and counts a link only
when the line is a table row — first non-space character `|` — and the link is
not inside an HTML comment or a fenced code block. The rest of the function is
unchanged: the same `LOCAL_LINK_RE`, the same first-path-segment rule, the same
skip of absolute URLs, the same two-way comparison against the tree.

## Why not the general form

"Does this row say something true" has no computable answer here, and the
surrounding docstring already records why: at `b40463cd` a naive cell
comparison failed on 24 of 46 rows. The narrow rule this work item adds is the
one that has a falsifiable answer — is the directory named by a row — and it
leaves cell contents alone.

## Acceptance criteria

- AC1: with the only link to a directory inside an `<!-- -->` comment, the
  check exits 1 and names `14-ai-development/work-items/<dir>`.
- AC2: the same for a prose line.
- AC3: the same for a fenced code block.
- AC4: a real table row still registers, and on the landing tree the summary
  reads `directories=N linked=N` with the two counts equal and exit 0, where
  `N` is the pre-existing directory count plus this work item's own. No
  directory may lose its entry — a gate that reddens the whole registry on
  landing is not acceptable.
- AC5: reverting only the production change turns the new tests red with an
  `AssertionError` naming the expected directory, not a traceback.
