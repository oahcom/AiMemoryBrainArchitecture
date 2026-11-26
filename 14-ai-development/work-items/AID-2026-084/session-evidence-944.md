---
document_metadata:
  domain: ai-development
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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count, exit code and failure line below was produced by a command run against this branch, on 2026-11-26. The defect measurements were taken at origin/main dc826e4e; the branch was rebuilt on baca092b when main moved, and section 5 states both bases."
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

# Session evidence — AID-2026-084

## Session role

IMPLEMENTER. This session narrowed the index-membership predicate reported in
issue #944, added the three tests that make the narrowing falsifiable, ran the
mutation that removes the guard, and did not touch any other rule in the
checker.

## Actual AI input

The assignment that produced this change, abridged where it repeated
repository context:

> The defect (issue #944) — already measured, do not re-derive the premise.
> `scripts/ci/check_repository_hygiene.py` builds the set of "registered"
> work-item directories with `LOCAL_LINK_RE` over the whole index, so every
> repository-relative link anywhere in `INDEX.md` counts — in prose, in HTML
> comments, in fenced code blocks.
>
> Change membership so that only a markdown table row can register a work-item
> directory. ... Links in prose, inside `<!-- -->`, or inside fenced code
> fences must not count. ... Keep the check passing on the current tree ...
> A gate that reddens the whole registry on landing is not acceptable.
>
> Mutation verification — mandatory. After the suite is green, revert only your
> production change and confirm the new tests fail with an `AssertionError`
> naming the expectation — not a traceback ... A passing test that does not turn
> red when the guard is removed is not evidence.

## AI-visible output

The diff to `scripts/ci/check_repository_hygiene.py` and
`scripts/test_check_repository_hygiene.py`, the three files in this directory,
one row inserted into `14-ai-development/work-items/INDEX.md`, and the pull
request that carries them.

## 1. What the check counted, and what the registry contains

At `origin/main` `dc826e4e`, before the change:

```
$ python3 scripts/ci/check_repository_hygiene.py
Work-item index membership version=2026-11-24.8 directories=68 linked=68
Work-item manifest consistency version=2026-11-24.8 manifests=57 in_scope=55 excluded_by_record_type=2 unrecognized=0 violations=0
Repository hygiene check passed (version=2026-11-24.8).      # exit 0
```

The file that produced `linked=68`:

```
lines in INDEX.md beginning with `|`                      132
those rows naming a work-item directory                    71
lines not beginning with `|` that name one                  0
repository-relative links in the whole file that land in a
  work-item directory                                      81
unique work-item directories named by those links          68
directories under 14-ai-development/work-items/            68
```

Two facts follow. The sets coincided on this tree, so narrowing the rule
changes no verdict here — that is the constraint the assignment set. And they
coincided because all 81 links happen to sit in a table row today, not because
the predicate required it. A row moved out of the table keeps counting.

The assignment stated that 38 lines outside the table carry such a link. That
figure is not reproducible here: the count of non-row lines carrying any `](`
link at all is 0, so the 81 links are entirely inside rows. The 71/81/68
figures above are from a re-run, not from the issue text.

The reproduction, re-run on this branch's tree against the real file in memory
rather than asserted from the issue:

```
row hidden: visible rows matching AID-2026-081 = 0
old rule missing dirs: []
new rule missing dirs: ['AID-2026-081']
```

With the `AID-2026-081` row wrapped in `<!-- ... -->`, the old predicate loses
nothing — its link is still in the file, so the directory still counts. The new
predicate loses the directory, which is the point.

## 2. The change

`index_entry_directories` now reads the index line by line:

- an `<!-- ... -->` region is skipped, including a comment that opens and
  closes on one line and a link that follows a closing `-->` on the same line;
- a fenced block (```` ``` ```` or `~~~`, up to three leading spaces) is skipped
  until its closing fence;
- a line registers only if its first non-space character is `|`.

Everything else is unchanged: the same `LOCAL_LINK_RE`, the same
first-path-segment rule, the same skip of `http://`, `https://` and `mailto:`,
the same two-way comparison against the committed tree.

The docstring states the new rule and its deliberate ceiling — a row in the
file's *other* table counts the same, and no cell content is read.

## 3. The tests

Three cases, each of which makes the link the directory's only reference, so
the directory must be reported missing:

```
test_index_membership_ignores_a_link_inside_an_html_comment
test_index_membership_ignores_a_link_in_prose
test_index_membership_ignores_a_link_inside_a_fenced_code_block
```

Plus one control, because a rule that rejected every line would pass all three:

```
test_index_membership_counts_a_row_among_prose_and_a_comment
```

That control asserts `directories=2 linked=2` and exit 0 with prose, a comment
and two real rows present.

The helper asserts the named violation **before** the exit code. The first
version asserted the exit code first, and the mutation then failed on
`AssertionError: 0 != 1` — a count, not the directory. Reordering was required
to make the failure say what went wrong.

## 4. Mutation output

Production change reverted to the previous whole-file body
(`for target in LOCAL_LINK_RE.findall(text)`), test file untouched:

```
$ python3 scripts/test_check_repository_hygiene.py
FAIL: test_index_membership_counts_a_row_among_prose_and_a_comment (__main__.RepositoryHygieneTests.test_index_membership_counts_a_row_among_prose_and_a_comment)
FAIL: test_index_membership_ignores_a_link_in_prose (__main__.RepositoryHygieneTests.test_index_membership_ignores_a_link_in_prose)
FAIL: test_index_membership_ignores_a_link_inside_a_fenced_code_block (__main__.RepositoryHygieneTests.test_index_membership_ignores_a_link_inside_a_fenced_code_block)
FAIL: test_index_membership_ignores_a_link_inside_an_html_comment (__main__.RepositoryHygieneTests.test_index_membership_ignores_a_link_inside_an_html_comment)
Ran 97 tests in 64.114s
FAILED (failures=4, skipped=1)
```

Each of the three named tests failed on the same assertion:

```
AssertionError: '::error::index membership violation: directory present, no index entry: 14-ai-development/work-items/AID-2026-002' not found in 'Work-item manifest consistency unrecognized shape: 14-ai-development/work-items/AID-2026-001/manifest.yaml\nWork-item manifest consistency unrecognized shape: 14-ai-development/work-items/AID-2026-002/manifest.yaml\n' : stdout:
Work-item index membership version=2026-11-24.8 directories=2 linked=2
Work-item manifest consistency version=2026-11-24.8 manifests=2 in_scope=0 excluded_by_record_type=0 unrecognized=2 violations=0
Repository hygiene check passed (version=2026-11-24.8).
```

The control failed separately, on the opposite expectation, which is what it is
for:

```
AssertionError: 1 != 0 : stdout:
Work-item index membership version=2026-11-24.8 directories=2 linked=3

stderr:
::error::index membership violation: index entry present, no directory: 14-ai-development/work-items/AID-2026-009
```

Restored, the module is green again:

```
$ python3 scripts/test_check_repository_hygiene.py
Ran 97 tests in 65.433s

OK (skipped=1)
```

No other test in the module changed verdict under the mutation, so the four
above are the whole effect of removing the guard.

## 5. Counts

```
tests before        93 (1 skipped)
tests after         97 (1 skipped)
files changed       2 production/test + 3 work-item record + INDEX.md
```

On the branch as first cut from `dc826e4e`:

```
python3 scripts/ci/check_repository_hygiene.py
directories=69 linked=69, exit 0        # 68 pre-existing + this work item's own
```

`origin/main` moved while this branch was open. The branch was rebuilt on the
current base rather than merged into it: the index is declared `merge=union` in
`.gitattributes`, and both a union merge and a `git rebase` of this change onto
the moved base produced `T-04 duplicate INDEX entry AID-2026-080` (and later
`AID-2026-101`), which is the failure mode that file's own comment describes.
Rebuilding the single commit on the new base keeps one row per work item. On
`baca092be10eaa531be4fe19b54d644fbd56e92c`:

```
python3 scripts/ci/check_repository_hygiene.py
directories=78 linked=78, exit 0
python3 scripts/test_check_repository_hygiene.py
Ran 97 tests, OK (skipped=1)
```

The `dc826e4e` figures above stay as measured; they are the state the defect
was reported against, not a claim about the current tree.
