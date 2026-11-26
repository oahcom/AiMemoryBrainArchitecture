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
      last_verification_note: "Every count and verdict below was produced by the audit driver described in section 2, run in this session against origin/main 31385bc1."
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

# AID-2026-183 — Bind the gate's reachable unbound error emissions with tests

## 1. The brief this session executed

Issue #827 asks one question per error message `scripts/check_document_management.py`
can emit: **if this statement were deleted, would any test turn red?** An audit on
an older tree reported ten that could not be. This session re-measured at the
current head, mechanically, and bound every reachable one.

The brief, abridged only where it repeated repository context:

> Step 1 — re-run the audit at the current head, mechanically. Do not hand-pick
> messages. Extract every message literal passed to `errors.append(...)` /
> `errors +=` in `scripts/check_document_management.py`, truncated at the first
> `{` so it acts as a stable prefix; dedupe. For each distinct prefix, in an
> isolated copy of the tree, replace **only** the statements emitting that
> message with `pass`, run `python3 scripts/test_check_document_management.py`,
> and record BOUND (suite red) / UNBOUND (suite green at baseline). Write the
> driver as a throwaway script; **do not commit it**.
>
> Step 2 — for each UNBOUND prefix that is actually reachable, add one test that
> asserts on that message. Reachability must be demonstrated, not assumed. For
> each UNBOUND prefix you cannot reach, do not invent a test: state the concrete
> reason, or say it is dead code and leave it.
>
> Step 3 — mutation verification, mandatory. For each test added, delete the
> emission the test binds and confirm **your** test fails with an
> `AssertionError` naming the message — not a traceback and not a different test.

## 2. What was measured, and how

`origin/main` at measurement time: `31385bc1aabc1599be2c8320be408c0d170057a8`.
Baseline suite: **318/318 passed**, one registered skip (`T68c`).

The driver parsed the gate with `ast`, collected every `errors.append(x)` /
`problems.append(x)` / `errors.extend(...)` site whose first argument is a
string or f-string literal containing `DM-`, and rendered each as a template
(`{}` for every interpolation, `{!r}` for a `!r` conversion). Interpolated
prefixes collapse to one template because two emissions that differ only in
their arguments are one message shape. **99 emission sites, 99 distinct
templates.**

For each template the driver copied the tree to an isolated directory, replaced
exactly the statements emitting it with `None`, and ran the suite:

- **BOUND** — the suite went red. Something already tests that message.
- **UNBOUND** — the suite stayed green at 318/318. Nothing tests it.

Result: **99 distinct prefixes, 61 BOUND, 38 UNBOUND, baseline 318/318.**

The issue's table is from an older tree (`main = a9f7c9b849`, baseline 239).
Its numbers are not comparable to these and are not reproduced. The issue said
"ten could not be bound"; at this head the number is 38 of 99, because the gate
grew and the audit is now mechanical rather than hand-picked.

## 3. The full audit table

| # | Message template | Verdict |
| --- | --- | --- |
| 1 | `DM-01 accounting: {} classified + {} unclassified != {} governed files` | BOUND |
| 2 | `DM-01 cannot resolve {}: {}` | BOUND |
| 3 | `DM-01 missing required field: {}{}` | BOUND |
| 4 | `DM-01 missing {} block: {}` | BOUND |
| 5 | `DM-01 not a file: {}` | BOUND |
| 6 | `DM-01 not valid UTF-8: {}` | UNBOUND |
| 7 | `DM-01 outside the repository root: {}` | UNBOUND |
| 8 | `DM-01 schema field {} declares unknown items kind {}` | BOUND |
| 9 | `DM-01 schema field {}{} declares unknown kind {}` | BOUND |
| 10 | `DM-01 schema field {}{} is not a mapping` | BOUND |
| 11 | `DM-01 {} contains a NUL byte` | BOUND |
| 12 | `DM-01 {} has a repeated ./ prefix: {}` | BOUND |
| 13 | `DM-01 {} is not a normalised relative path: {}` | BOUND |
| 14 | `DM-01 {} must be a mapping, got {}` | BOUND |
| 15 | `DM-01 {} must be a scalar, got {}` | BOUND |
| 16 | `DM-01 {} must be a string path, got {}` | UNBOUND |
| 17 | `DM-01 {} must be repository-relative, got absolute {}` | BOUND |
| 18 | `DM-01 {} must be {}, got {}` | BOUND |
| 19 | `DM-01 {} uses a backslash separator: {}` | BOUND |
| 20 | `DM-01 {}[{}] must be {}, got {}` | BOUND |
| 21 | `DM-03 Approved requires approval.approval_applicability` | BOUND |
| 22 | `DM-03 Approved requires approval.approval_scope.type` | BOUND |
| 23 | `DM-03 Approved requires approval.approved_version.value` | BOUND |
| 24 | `DM-03 approval_scope.type {} is not implemented: DM-10 compares the whole body, so this approval would be silently narrower than the gate checks. Only 'Full-document' is honoured` | BOUND |
| 25 | `DM-03 approval_scope.{} is not honoured: only 'Full-document' is checked, so a non-empty list would claim a boundary the gate never verifies. Remove it` | BOUND |
| 26 | `DM-04 Revoked requires a revocation block` | BOUND |
| 27 | `DM-04 Revoked requires revocation.revocation_decision_id` | UNBOUND |
| 28 | `DM-04 Revoked requires revocation.revocation_reason` | UNBOUND |
| 29 | `DM-04 Revoked requires revocation.revoked_date` | UNBOUND |
| 30 | `DM-04 revocation_decision_id {} reused by {} and {}` | UNBOUND |
| 31 | `DM-05 Archived requires archival.archival_reason` | BOUND |
| 32 | `DM-05 Archived requires archival.archived_date` | BOUND |
| 33 | `DM-06 Canonical requires authority.canonical_scope` | BOUND |
| 34 | `DM-06 Canonical requires authority.canonical_scope_id` | BOUND |
| 35 | `DM-06 Canonical requires non-empty canonical_scope_keywords` | BOUND |
| 36 | `DM-06 canonical_scope_id not normalized (expect '<domain>/<kebab-case>'): {}` | BOUND |
| 37 | `DM-06 canonical_scope_id prefix {} must equal the declared domain {}` | BOUND |
| 38 | `DM-06 canonical_scope_keywords entries must be non-empty strings` | UNBOUND |
| 39 | `DM-08 {} is {}: CI-derived, MUST NOT be hand-written` | BOUND |
| 40 | `DM-09 a generated artifact MUST NOT be Normative or Canonical; the Markdown source is the authority (policy 7)` | BOUND |
| 41 | `DM-10 approved_version {} is not a commit in this repository` | BOUND |
| 42 | `DM-10 approved_version {} must be a full 40-hex commit id, not a branch, tag or abbreviated reference` | BOUND |
| 43 | `DM-10 content changed after approved_version: approval_applicability MUST be Not-Applicable-To-Current-Version (a stale approval MUST NOT be presented as current)` | BOUND |
| 44 | `DM-10 content changed after approved_version: modification_status MUST be Pending-Reapproval` | BOUND |
| 45 | `DM-10 {} did not exist at approved_version {}; the approval cannot be bound to that version` | UNBOUND |
| 46 | `DM-11 a document under canonical conflict MUST NOT be Canonical; set canonical_status: Candidate until the conflict is resolved` | BOUND |
| 47 | `DM-11 canonical_conflict_status: Resolved requires a resolution block` | BOUND |
| 48 | `DM-11 resolution requires resolution_decision_id` | UNBOUND |
| 49 | `DM-11 resolution requires resolved_date` | UNBOUND |
| 50 | `DM-11 resolution requires selected_document` | UNBOUND |
| 51 | `DM-11 scope {} resolution selects {}, which does not declare this scope` | UNBOUND |
| 52 | `DM-11 scope {} resolution selects {}, which is not the unique Canonical document ({})` | UNBOUND |
| 53 | `DM-12 {} -> {}: neither its source ({}) nor a sibling mirror of it ({})` | UNBOUND |
| 54 | `DM-12 {} <-> {}: the counterpart does not name {} as its source` | BOUND |
| 55 | `DM-12 {}: bilingual_counterpart.{} does not exist: {}` | UNBOUND |
| 56 | `DM-12 {}: bilingual_counterpart.{} must point under {}, got {}` | UNBOUND |
| 57 | `DM-12 {}: bilingual_counterpart.{} points to itself` | UNBOUND |
| 58 | `DM-12 {}: both a document and its mirror claim Canonical ({})` | UNBOUND |
| 59 | `DM-12 {}: counterpart {} exists but carries no document_metadata, so parity cannot be verified` | BOUND |
| 60 | `DM-12 {}: lives under a language mirror root but declares no bilingual_counterpart.source, so it belongs to no group` | BOUND |
| 61 | `DM-12 {}: names {} as its source, but that file is not a classified governed document` | BOUND |
| 62 | `DM-12 {}: names {} as its source, but {} does not list this mirror` | BOUND |
| 63 | `DM-12 {}: source must be the authoritative file, not a mirror ({})` | UNBOUND |
| 64 | `DM-12 {}: {} {} disagrees with {} ({})` | UNBOUND |
| 65 | `DM-13 {}: a document cannot supersede itself` | UNBOUND |
| 66 | `DM-13 {}: supersedes must be a list` | UNBOUND |
| 67 | `DM-13 {}: supersedes target does not exist: {}` | BOUND |
| 68 | `DM-14 backlog {} declares {} documents but {} are on disk; update the registry` | BOUND |
| 69 | `DM-14 backlog {} has no reason` | UNBOUND |
| 70 | `DM-14 backlog {} has no reason_zh (GOV-DOC-001)` | UNBOUND |
| 71 | `DM-14 backlog {} must be a mapping with a count` | UNBOUND |
| 72 | `DM-14 backlog {} must declare `documents` as a non-negative integer, got {}` | BOUND |
| 73 | `DM-14 backlog {} {} restates a document count {}; `documents:` is the only place a count may be stated, so the prose cannot drift from it` | BOUND |
| 74 | `DM-14 bilingual mirror directory {} is a symbolic link; a mirror must be real content of this repository` | UNBOUND |
| 75 | `DM-14 bilingual mirror directory {} is missing` | BOUND |
| 76 | `DM-14 cannot read {}: {}` | BOUND |
| 77 | `DM-14 collect_governed: governed file {} is not a regular file inside the repository (missing, a symlink, or reached through one)` | BOUND |
| 78 | `DM-14 excluded {} has no reason` | BOUND |
| 79 | `DM-14 excluded {} has no reason_zh (GOV-DOC-001)` | UNBOUND |
| 80 | `DM-14 excluded {} must be a mapping with a reason` | UNBOUND |
| 81 | `DM-14 excluded {} must declare kind one of {}, got {}` | UNBOUND |
| 82 | `DM-14 governed file {} is already covered by root {}; drop the individual entry` | BOUND |
| 83 | `DM-14 governed file {} is not a regular file inside the repository (missing, a symlink, or reached through one)` | BOUND |
| 84 | `DM-14 governed file {} sits in {}, which is neither governed, backlog nor excluded: declare the directory's status first` | UNBOUND |
| 85 | `DM-14 governed_files disagrees with the gate; registry-only {}, gate-only {}` | BOUND |
| 86 | `DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only {}, enforced-only {}` | UNBOUND |
| 87 | `DM-14 symbolic links at the repository root are not governed roots: {}. A symlink makes the governed set depend on a target outside the repository` | BOUND |
| 88 | `DM-14 top-level directories not accounted for: {}. Add each to {} as governed or excluded-with-reason` | BOUND |
| 89 | `DM-14 {} are both governed and backlog; pick one` | UNBOUND |
| 90 | `DM-14 {} are both governed-or-backlog and excluded` | UNBOUND |
| 91 | `DM-14 {} backlog must be a mapping` | UNBOUND |
| 92 | `DM-14 {} declares registry_version {} but this gate implements {}` | BOUND |
| 93 | `DM-14 {} excluded must be a mapping` | UNBOUND |
| 94 | `DM-14 {} governed_files must be a sequence` | UNBOUND |
| 95 | `DM-14 {} is a symbolic link; a governed document must be a regular file inside the repository` | BOUND |
| 96 | `DM-14 {} is a symbolic link; a governed or backlog root must be a real directory inside the repository, not a pointer to one` | BOUND |
| 97 | `DM-14 {} is a symbolic link; the gate does not follow links, and a linked directory would make the scanned set depend on a target outside the repository` | BOUND |
| 98 | `DM-14 {} must declare a non-empty governed list` | UNBOUND |
| 99 | `DM-14 {} names directories that do not exist: {}` | BOUND |

## 4. The one UNBOUND prefix that is not bound

`DM-01 outside the repository root: {}` is emitted when
`path.relative_to(root)` raises `ValueError`. Every target reaching that loop
comes from `collect_governed(root)`, which yields paths built as `root / rel`;
`main()` resolves `--root` before scanning, and `scan_root()` reports symlinks
rather than following them. No document, registry entry or directory layout can
produce a target outside the resolved root. The branch is defensive and
unreachable on the current tree. It is **not** deleted — issue #827 says not to
delete dead code in this change — and no test fabricates an input for it.

## 5. Acceptance criteria

- AC1: the audit is reproducible from the gate's own source, with no hand-picked
  message list, and reports its total, BOUND, UNBOUND and baseline count.
- AC2: every reachable UNBOUND prefix has a test that asserts on that message
  and fails when the emission is deleted.
- AC3: the one unreachable prefix is named with its reason, not tested, and not
  deleted.
- AC4: the suite is green at the end, with no existing case weakened.
- AC5: no production file changes. This is a test-only change.
