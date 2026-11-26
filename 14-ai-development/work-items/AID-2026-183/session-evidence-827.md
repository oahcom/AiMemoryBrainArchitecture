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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count, verdict and exit code below was produced by a command run in this session against this branch, based on origin/main 31385bc1, on 2026-11-26."
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

# Session evidence — AID-2026-183 (issue #827)

## Session role / use case

IMPLEMENTER. This session re-measured issue #827's audit at the current head,
bound every reachable error message the gate can emit that no test covered, and
verified each binding by mutation. It did not change
`scripts/check_document_management.py`, did not delete the one unreachable
emission, and did not weaken any existing test.

## Actual AI input

The assignment that produced this change, abridged only where it repeated
repository context:

> Your job is a **measurement plus a binding test**, verified by mutation,
> pushed as one PR.
>
> The defect (issue #827): for each error message
> `scripts/check_document_management.py` can emit, does any test turn red if that
> emission is deleted? Ten could not be, on `main = a9f7c9b849`, with baseline
> `239/239 passed`. ... **The suite is no longer 239.** ... re-measure; do not
> quote 239 as current.
>
> Step 1 — re-run the audit at the current head, mechanically. Do not hand-pick
> messages. ... Write the driver as a throwaway script under `/c/tmp/opencode/`
> — **do not commit it**.
>
> Step 2 — for each UNBOUND prefix that is actually reachable ... add one test.
> ... For each UNBOUND prefix you **cannot** reach, do not invent a test. ...
> do **not** delete it in this PR.
>
> Step 3 — mutation verification, mandatory. ... confirm **your** test fails with
> an `AssertionError` naming the message — not a traceback and not a different
> test. Record verbatim output per case.

## AI-visible output

The output visible to the user is: the diff to
`scripts/test_check_document_management.py`, the three files in this directory,
one row appended to `14-ai-development/work-items/INDEX.md`, and the pull request
that carries them.

## 1. Baseline

```
$ python3 scripts/test_check_document_management.py
...
318/318 passed
1 skipped, 1 registered of 1 allowed: T68c a real 0o000 directory is reported by path (integration)
```

`origin/main` at measurement time: `31385bc1aabc1599be2c8320be408c0d170057a8`.
The issue's `239/239` is from an older tree and is not reproduced here.

## 2. The audit

The driver parsed the gate with `ast`, collected every
`errors.append` / `problems.append` / `errors.extend` site whose first argument
is a string or f-string literal containing `DM-`, rendered each as a template
(`{}` per interpolation, `{!r}` per `!r` conversion), and deduped. For each
template it copied the tree, replaced exactly the statements emitting it with
`None`, and ran the suite.

```
emission_sites=99 distinct_templates=99
BASELINE rc=0 ::   318/318 passed
TOTAL=99 BOUND=61 UNBOUND=38
```

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

## 3. Reachability of the 38 UNBOUND templates

37 are reachable and are bound by T94–T128. Each was first demonstrated: the
fixture was built, the gate was run, and the message was observed in its output
before any assertion was written. The fixtures are the ones in the new
`run_unbound_emissions()` section; each is the minimum document or registry
that makes that one message speak while its neighbours stay quiet.

1 is **not reachable**: `DM-01 outside the repository root: {}`, emitted at
`scripts/check_document_management.py:2281` when `path.relative_to(root)` raises
`ValueError`. Every target reaching that loop comes from
`collect_governed(root)`, which yields `root / rel`; `main()` resolves
`--root` before scanning, and `scan_root()` reports a symlink rather than
following it. No document, registry entry or directory layout can produce a
target outside the resolved root.

The branch is not dead in the sense of "cannot be written": a probe that
monkeypatched `collect_governed()` to append an out-of-tree path did emit the
message. It is dead in the sense that no input the gate can be handed reaches
it. It is left in place — issue #827 asks for tests, not a deletion — and no
test fabricates an input for it.

## 4. The tests added

One function, `run_unbound_emissions()`, called from `main()` after
`run_fault_injection()`. It adds 37 cases (T94–T128; T98 carries three, one per
omitted resolution field). Each case:

- builds the fixture that makes one message speak,
- matches the emitted text against the emission's own literal with each `{}`
  turned into `.+`,
- records a failure carrying an `AssertionError` that names the pattern it
  expected and the messages it actually saw.

Final suite:

```
355/355 passed
1 skipped, 1 registered of 1 allowed: T68c a real 0o000 directory is reported by path (integration)
```

## 5. Mutation verification

For each of the 37 bindings, the emission statement was replaced with `None` in
an isolated copy of the tree and the whole suite was run. In every case the run
exited non-zero and the only new failure was the case that binds that message,
with an `AssertionError`. Verbatim, one per template:

**`DM-01 {} must be a string path, got {}`** — T100 DM-01 a non-string counterpart path is named

```
[FAIL] T100 DM-01 a non-string counterpart path is named  AssertionError: no emitted message matched 'DM\\-01 .+ bilingual_counterpart\\.en must be a string path, got list'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 1 error(s)', '  00-governance/a.md: DM-01 bilingual_counterpart.en must be nullable-string, got list']
```

**`DM-04 Revoked requires revocation.revocation_decision_id`** — T94 DM-04 Revoked without revocation_decision_id is named

```
[FAIL] T94 DM-04 Revoked without revocation_decision_id is named  AssertionError: no emitted message matched 'DM\\-04 Revoked requires revocation\\.revocation_decision_id'; emitted []
```

**`DM-04 Revoked requires revocation.revocation_reason`** — T96 DM-04 Revoked without revocation_reason is named

```
[FAIL] T96 DM-04 Revoked without revocation_reason is named  AssertionError: no emitted message matched 'DM\\-04 Revoked requires revocation\\.revocation_reason'; emitted []
```

**`DM-04 Revoked requires revocation.revoked_date`** — T95 DM-04 Revoked without revoked_date is named

```
[FAIL] T95 DM-04 Revoked without revoked_date is named  AssertionError: no emitted message matched 'DM\\-04 Revoked requires revocation\\.revoked_date'; emitted []
```

**`DM-04 revocation_decision_id {!r} reused by {} and {}`** — T101 DM-04 a reused revocation_decision_id is reported

```
[FAIL] T101 DM-04 a reused revocation_decision_id is reported  AssertionError: no emitted message matched 'DM\\-04 revocation_decision_id .+ reused by .+ and .+'; emitted ['GOV-DOC-002: 4 governed documents, 4 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 2/2 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'PASS (whole tree): no GOV-DOC-002 violations; 4 classified, 0 unclassified']
```

**`DM-06 canonical_scope_keywords entries must be non-empty strings`** — T97 DM-06 a blank keyword entry is named

```
[FAIL] T97 DM-06 a blank keyword entry is named  AssertionError: no emitted message matched 'DM\\-06 canonical_scope_keywords entries must be non\\-empty strings'; emitted []
```

**`DM-10 {} did not exist at approved_version {}; the approval cannot be bound to that version`** — T102 DM-10 an approval pinned before the file existed is named

```
[FAIL] T102 DM-10 an approval pinned before the file existed is named  AssertionError: no emitted message matched 'DM\\-10 .+ did not exist at approved_version .+; the approval cannot be bound to that version'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", 'PASS (whole tree): no GOV-DOC-002 violations; 3 classified, 0 unclassified']
```

**`DM-11 resolution requires resolution_decision_id`** — T98 DM-11 a resolution without resolution_decision_id is named

```
[FAIL] T98 DM-11 a resolution without resolution_decision_id is named  AssertionError: no emitted message matched 'DM\\-11 resolution requires resolution_decision_id'; emitted []
```

**`DM-11 resolution requires resolved_date`** — T98 DM-11 a resolution without resolved_date is named

```
[FAIL] T98 DM-11 a resolution without resolved_date is named  AssertionError: no emitted message matched 'DM\\-11 resolution requires resolved_date'; emitted []
```

**`DM-11 resolution requires selected_document`** — T98 DM-11 a resolution without selected_document is named

```
[FAIL] T98 DM-11 a resolution without selected_document is named  AssertionError: no emitted message matched 'DM\\-11 resolution requires selected_document'; emitted []
```

**`DM-11 scope {!r} resolution selects {!r}, which does not declare this scope`** — T103 DM-11 a resolution selecting a non-member of the scope is named

```
[FAIL] T103 DM-11 a resolution selecting a non-member of the scope is named  AssertionError: no emitted message matched 'DM\\-11 scope .+ resolution selects .+, which does not declare this scope'; emitted ["  conflict: scope 'architecture/dup' has no authoritative source", 'GOV-DOC-002: 4 governed documents, 4 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 2/2 classified', '  docs: 2/2 classified', '  authority: architecture/dup -> NO_AUTHORITATIVE_SOURCE', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'PASS (whole tree): no GOV-DOC-002 violations; 4 classified, 0 unclassified']
```

**`DM-11 scope {!r} resolution selects {!r}, which is not the unique Canonical document ({})`** — T104 DM-11 a resolution selecting a non-Canonical document is named

```
[FAIL] T104 DM-11 a resolution selecting a non-Canonical document is named  AssertionError: no emitted message matched 'DM\\-11 scope .+ resolution selects .+, which is not the unique Canonical document \\(.+\\)'; emitted ["  conflict: scope 'architecture/dup' has no authoritative source", 'GOV-DOC-002: 4 governed documents, 4 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 2/2 classified', '  docs: 2/2 classified', '  authority: architecture/dup -> NO_AUTHORITATIVE_SOURCE', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 1 error(s)', "  DM-11 scope 'architecture/dup' has 2 resolution records: 00-governance/a.md, 00-governance/b.md"]
```

**`DM-12 {} -> {}: neither its source ({}) nor a sibling mirror of it ({!r})`** — T111 DM-12 a link to a third party's mirror is named

```
[FAIL] T111 DM-12 a link to a third party's mirror is named  AssertionError: no emitted message matched 'DM\\-12 .+ -> .+: neither its source \\(.+\\) nor a sibling mirror of it \\(.+\\)'; emitted ['GOV-DOC-002: 6 governed documents, 6 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 2/2 classified', '  docs: 4/4 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', '  00-governance/b.md: DM-02 lifecycle.bilingual_counterpart: unknown key (allowed: approval, archival, evidence_verification, modification_status, supersession, usage_status)', '  DM-12 docs/en/a.md: bilingual_counterpart.zh-CN must point under docs/zh-CN/, got docs/en/b.md', '  DM-12 docs/en/a.md: names 00-governance/a.md as its source, but 00-governance/a.md does not list this mirror', '  DM-12 docs/en/b.md: names 00-governance/b.md as its source, but 00-governance/b.md does not list this mirror']
```

**`DM-12 {}: bilingual_counterpart.{} does not exist: {}`** — T105 DM-12 a counterpart that does not exist is named

```
[FAIL] T105 DM-12 a counterpart that does not exist is named  AssertionError: no emitted message matched 'DM\\-12 .+: bilingual_counterpart\\.en does not exist: .+'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'PASS (whole tree): no GOV-DOC-002 violations; 3 classified, 0 unclassified']
```

**`DM-12 {}: bilingual_counterpart.{} must point under {}, got {}`** — T106 DM-12 a counterpart outside the mirror root is named

```
[FAIL] T106 DM-12 a counterpart outside the mirror root is named  AssertionError: no emitted message matched 'DM\\-12 .+: bilingual_counterpart\\.en must point under docs/en/, got .+'; emitted ['GOV-DOC-002: 4 governed documents, 4 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 2/2 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 1 error(s)', '  DM-12 00-governance/b.md <-> 00-governance/a.md: the counterpart does not name 00-governance/b.md as its source']
```

**`DM-12 {}: bilingual_counterpart.{} points to itself`** — T107 DM-12 a counterpart pointing at itself is named

```
[FAIL] T107 DM-12 a counterpart pointing at itself is named  AssertionError: no emitted message matched 'DM\\-12 .+: bilingual_counterpart\\.en points to itself'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'PASS (whole tree): no GOV-DOC-002 violations; 3 classified, 0 unclassified']
```

**`DM-12 {}: both a document and its mirror claim Canonical ({})`** — T108 DM-12 two Canonical claims in one group are named

```
[FAIL] T108 DM-12 two Canonical claims in one group are named  AssertionError: no emitted message matched 'DM\\-12 .+: both a document and its mirror claim Canonical \\(.+\\)'; emitted ['GOV-DOC-002: 4 governed documents, 4 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 3/3 classified', '  authority: architecture/data-model-design -> NO_AUTHORITATIVE_SOURCE', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 1 error(s)', "  DM-07 scope 'architecture/data-model-design' has 2 Canonical documents: 00-governance/a.md, docs/en/a.md"]
```

**`DM-12 {}: source must be the authoritative file, not a mirror ({})`** — T109 DM-12 a mirror naming a mirror as its source is named

```
[FAIL] T109 DM-12 a mirror naming a mirror as its source is named  AssertionError: no emitted message matched 'DM\\-12 .+: source must be the authoritative file, not a mirror \\(.+\\)'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 3/3 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 2 error(s)', '  DM-12 docs/en/a.md: bilingual_counterpart.source does not exist: docs/en/b.md', '  DM-12 docs/en/a.md: names docs/en/b.md as its source, but that file is not a classified governed document']
```

**`DM-12 {}: {} {!r} disagrees with {} ({!r})`** — T110 DM-12 a field disagreeing across a group is named

```
[FAIL] T110 DM-12 a field disagreeing across a group is named  AssertionError: no emitted message matched 'DM\\-12 .+: role .+ disagrees with .+ \\(.+\\)'; emitted ['GOV-DOC-002: 4 governed documents, 4 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 3/3 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'PASS (whole tree): no GOV-DOC-002 violations; 4 classified, 0 unclassified']
```

**`DM-13 {}: a document cannot supersede itself`** — T112 DM-13 a document superseding itself is named

```
[FAIL] T112 DM-13 a document superseding itself is named  AssertionError: no emitted message matched 'DM\\-13 .+: a document cannot supersede itself'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'PASS (whole tree): no GOV-DOC-002 violations; 3 classified, 0 unclassified']
```

**`DM-13 {}: supersedes must be a list`** — T113 DM-13 a non-list supersedes is named

```
[FAIL] T113 DM-13 a non-list supersedes is named  AssertionError: no emitted message matched 'DM\\-13 .+: supersedes must be a list'; emitted ['GOV-DOC-002: 3 governed documents, 3 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  00-governance: 1/1 classified', '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 1 error(s)', '  00-governance/a.md: DM-01 lifecycle.supersession.supersedes must be sequence, got str']
```

**`DM-14 backlog {!r} has no reason`** — T115 DM-14 a backlog entry with no reason is named

```
[FAIL] T115 DM-14 a backlog entry with no reason is named  AssertionError: no emitted message matched "DM\\-14 backlog 'docs' has no reason"; emitted ['GOV-DOC-002: 2 governed documents, 2 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 3 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']"]
```

**`DM-14 backlog {!r} has no reason_zh (GOV-DOC-001)`** — T116 DM-14 a backlog entry with no reason_zh is named

```
[FAIL] T116 DM-14 a backlog entry with no reason_zh is named  AssertionError: no emitted message matched "DM\\-14 backlog 'docs' has no reason_zh \\(GOV\\-DOC\\-001\\)"; emitted ['GOV-DOC-002: 2 governed documents, 2 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 3 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']"]
```

**`DM-14 backlog {!r} must be a mapping with a count`** — T114 DM-14 a backlog entry that is not a mapping is named

```
[FAIL] T114 DM-14 a backlog entry that is not a mapping is named  AssertionError: no emitted message matched "DM\\-14 backlog 'docs' must be a mapping with a count"; emitted ['GOV-DOC-002: 2 governed documents, 2 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 3 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']"]
```

**`DM-14 bilingual mirror directory {} is a symbolic link; a mirror must be real content of this repository`** — T128 DM-14 a symlinked mirror directory is named

```
[FAIL] T128 DM-14 a symlinked mirror directory is named  AssertionError: no emitted message matched 'DM\\-14 bilingual mirror directory docs/en is a symbolic link; a mirror must be real content of this repository'; emitted ['GOV-DOC-002: 2 governed documents, 2 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 3 error(s)', '  DM-14 docs/en is a symbolic link; a governed or backlog root must be a real directory inside the repository, not a pointer to one', '  DM-14 docs/en is a symbolic link; the gate does not follow links, and a linked directory would make the scanned set depend on a target outside the repository', '  DM-14 docs/en is a symbolic link; the gate does not follow links, and a linked directory would make the scanned set depend on a target outside the repository']
```

**`DM-14 excluded {!r} has no reason_zh (GOV-DOC-001)`** — T118 DM-14 an excluded entry with no reason_zh is named

```
[FAIL] T118 DM-14 an excluded entry with no reason_zh is named  AssertionError: no emitted message matched "DM\\-14 excluded 'tools' has no reason_zh \\(GOV\\-DOC\\-001\\)"; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 excluded {!r} must be a mapping with a reason`** — T117 DM-14 an excluded entry that is not a mapping is named

```
[FAIL] T117 DM-14 an excluded entry that is not a mapping is named  AssertionError: no emitted message matched "DM\\-14 excluded 'tools' must be a mapping with a reason"; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 excluded {!r} must declare kind one of {}, got {!r}`** — T119 DM-14 an excluded entry with an unknown kind is named

```
[FAIL] T119 DM-14 an excluded entry with an unknown kind is named  AssertionError: no emitted message matched "DM\\-14 excluded 'tools' must declare kind one of .+, got 'whatever'"; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 governed file {} sits in {}, which is neither governed, backlog nor excluded: declare the directory's status first`** — T127 DM-14 a governed file in an unaccounted directory is named

```
[FAIL] T127 DM-14 a governed file in an unaccounted directory is named  AssertionError: no emitted message matched "DM\\-14 governed file 15\\-orphan/x\\.md sits in 15\\-orphan, which is neither governed, backlog nor excluded: declare the directory's status first"; emitted ["DM-14 top-level directories not accounted for: ['15-orphan']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "DM-14 governed_files disagrees with the gate; registry-only ['docs/governance/documentation-gaps.md'], gate-only ['15-orphan/x.md']", "DM-14 backlog 'docs' declares 1 documents but 2 are on disk; update the registry"]
```

**`DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only {}, enforced-only {}`** — T126 DM-14 a registry disagreeing with NORMATIVE_ROOTS is named

```
[FAIL] T126 DM-14 a registry disagreeing with NORMATIVE_ROOTS is named  AssertionError: no emitted message matched 'DM\\-14 scope registry and NORMATIVE_ROOTS disagree; declared\\-only .+, enforced\\-only .+'; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 3 error(s)', "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 {} are both governed and backlog; pick one`** — T124 DM-14 a governed root also declared backlog is named

```
[FAIL] T124 DM-14 a governed root also declared backlog is named  AssertionError: no emitted message matched "DM\\-14 \\['00\\-governance'\\] are both governed and backlog; pick one"; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 5 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 backlog '00-governance' declares 1 documents but 0 are on disk; update the registry", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 {} are both governed-or-backlog and excluded`** — T125 DM-14 a governed root also excluded is named

```
[FAIL] T125 DM-14 a governed root also excluded is named  AssertionError: no emitted message matched "DM\\-14 \\['00\\-governance'\\] are both governed\\-or\\-backlog and excluded"; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 {} backlog must be a mapping`** — T120 DM-14 a backlog that is not a mapping is named

```
[FAIL] T120 DM-14 a backlog that is not a mapping is named  AssertionError: no emitted message matched 'DM\\-14 .+ backlog must be a mapping'; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 {} excluded must be a mapping`** — T121 DM-14 an excluded that is not a mapping is named

```
[FAIL] T121 DM-14 an excluded that is not a mapping is named  AssertionError: no emitted message matched 'DM\\-14 .+ excluded must be a mapping'; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 {} governed_files must be a sequence`** — T122 DM-14 a governed_files that is not a sequence is named

```
[FAIL] T122 DM-14 a governed_files that is not a sequence is named  AssertionError: no emitted message matched 'DM\\-14 .+ governed_files must be a sequence'; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-14 {} must declare a non-empty governed list`** — T123 DM-14 an empty governed list is named

```
[FAIL] T123 DM-14 an empty governed list is named  AssertionError: no emitted message matched 'DM\\-14 .+ must declare a non\\-empty governed list'; emitted ['GOV-DOC-002: 1 governed documents, 1 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 1/1 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 4 error(s)', "  DM-14 scope registry and NORMATIVE_ROOTS disagree; declared-only [], enforced-only ['00-governance', '01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development']", "  DM-14 top-level directories not accounted for: ['00-governance', '01-system-architecture', '02-domain-model', '04-memory-compiler', '06-memory-context', '07-agent-integration', '08-bmcp-protocol', '13-engineering-decisions', '14-ai-development', 'docs', 'tools']. Add each to 00-governance/document-scope-registry.yaml as governed or excluded-with-reason", "  DM-14 governed_files disagrees with the gate; registry-only [], gate-only ['docs/governance/documentation-gaps.md']", "  DM-14 governed file docs/governance/documentation-gaps.md sits in docs, which is neither governed, backlog nor excluded: declare the directory's status first"]
```

**`DM-01 not valid UTF-8: {}`** — T99 DM-01 a non-UTF-8 governed file is reported by path

```
[FAIL] T99 DM-01 a non-UTF-8 governed file is reported by path  AssertionError: no emitted message matched 'DM\\-01 not valid UTF\\-8: .+'; emitted ['GOV-DOC-002: 3 governed documents, 2 classified, 0 unclassified', 'DM-10 out-of-scope stale bindings: 0', "::notice::advisory (non-blocking): 0 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)", '  docs: 2/2 classified', "  manual controls (not machine-verified, policy 9.2): M-01 Whether two `Canonical` scopes genuinely overlap; M-02 Whether an `Approved` decision is real; M-03 Whether `evidence_verification` evidence supports the decision; M-04 Whether a whole-document approval is the scope the approver intended; M-05 Semantic parity of a bilingual mirror; M-06 Whether an exclusion reason is honest; M-07 Whether a declared backlog is acceptable to ship; M-08 Whether external consumers obey `resolve_canonical()`; M-09 Whether the normalisation equivalence is appropriate for a document's semantics; M-10 Whether the `_unclassified` citation ban is respected", '  note: no git work tree here, approval binding NOT VERIFIED', 'FAIL: 1 error(s)', '  DM-01 accounting: 2 classified + 0 unclassified != 3 governed files']
```


## 6. Gates

```
python3 scripts/test_check_document_management.py        0
python3 scripts/ci/check_repository_hygiene.py           0
python3 scripts/check_traceability.py --index-only       0
python3 scripts/ci/check_manifest_parse.py               0
```

## 7. What this record does not claim

- It does not claim the issue's figure of ten is wrong. It claims the figure is
  from an older tree and gives the current one: 38 of 99 at `31385bc1`.
- It does not claim every BOUND message has a *good* test, only that deleting
  its emission turns something red.
- It does not claim the unreachable branch is correct. It claims it is
  unreachable and leaves it alone.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt was written from
  the same measurements as this record but was not re-read line by line against
  the final diff.
