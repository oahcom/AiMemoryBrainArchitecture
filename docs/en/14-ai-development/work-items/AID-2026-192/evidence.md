---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-192/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every before/after number below was produced in this working tree by running the quoted command, with the pre-fix files taken from origin/main at 2f4f4118bd2c2d8e43a23975f667deeb06553f3c; no CI result, merge SHA or platform context is claimed."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: "AID-2026-192 making three gate helpers fail closed on an absent or comment-only input"
    canonical_scope_id: "ai-development/aid-2026-192-gates-fail-closed-on-unreadable-inputs"
    canonical_scope_keywords:
      - "fail-closed"
      - "index-membership"
      - "declared-check-contexts"
      - "test-reachability"
      - "comment-stripping"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-192/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-192/evidence.md"
---

# AID-2026-192 — Three gates answered a question they could not read

**Status: DRAFT — helper and test change only.** No required context, job id, job display name,
index row or baseline entry is added, renamed or removed. Every judgement each checker already
made is kept; the change is what happens when its input is missing, `.yaml`-suffixed, or present
only in a comment.

## 1. Why this record exists

Three checks in this repository are relations, not single-file inspections:

| Check | Relation | Its two sides |
|---|---|---|
| `check_index_membership` | directory ↔ index row | `14-ai-development/work-items/*/` and `INDEX.md` |
| `check_declared_check_contexts` | declared ↔ produced | the fenced block in `PR-GOVERNANCE-001.md` and the jobs in `.github/workflows/` |
| `check_test_reachability` | test file ↔ workflow | `test_*.py` under the tree and what a workflow executes |

Each one could return green while one side of the relation was empty. An empty side is not a
satisfied relation: it is an unbound one. The three cases below were measured, not inferred — the
pre-fix files are the versions at `origin/main` = `2f4f4118bd2c2d8e43a23975f667deeb06553f3c`.

## 2. Defect 1 — index membership passed on an empty set

`check_index_membership` had two early returns:

```python
directories = work_item_directories(head_paths)
if not directories:
    return []                      # no directory side -> no violations
if WORK_ITEMS_INDEX not in head_paths:
    return []                      # no index side -> no violations
```

`main()` reads `[]` as "nothing to report" and prints the pass line. Measured with the pre-fix
file, on a tree whose only path is `README.md`:

| Input | Before | After |
|---|---|---|
| No work-item directory at all (the shape a renamed `work-items/` produces) | `check_index_membership` returns `[]`; the checker prints `Repository hygiene check passed` and exits 0 | `RuntimeError` → `::error::repository hygiene cannot be determined: no work-item directories under '14-ai-development/work-items' ...` → exit 2 |
| Directories present, `INDEX.md` absent from the head tree | returns `[]`; exit 0 | `RuntimeError` → `::error::... the work-item index '14-ai-development/work-items/INDEX.md' is absent from the tree ...` → exit 2 |

`RuntimeError` is this file's existing "cannot be determined" channel, which `main()` already
turns into exit 2 — the same answer the other checks in the file give a missing input. No new
exit code and no new message channel were introduced. `CHECK_VERSION` moves from
`2026-11-24.8` to `2026-11-27.1`, because a reader who cites a version string is citing a rule
set, and this rule set changed.

## 3. Defect 2 — a comment ate a workflow

Two independent blind spots in the two workflow readers.

### 3.1 `jobs:  # comment`

`produced_contexts` looked for a line whose `rstrip()` equals `jobs:` and, failing that, for a
column-0 key that would end the mapping. `jobs:  # comment` is neither, so the reader never
entered the jobs mapping and the file produced no contexts. The declared-versus-produced test is
a subset test, so an empty produced set cannot fail it — every declared name was satisfied by the
other files.

Measured on a three-job fixture (`fmt`, its display name, `audit`) with the comment on the header:

| | Before | After |
|---|---|---|
| `produced_contexts(...)` result | 0 contexts | 3 contexts: `fmt`, `Rust format (hard gate)`, `audit` |

The converse is pinned too: a job that exists only as `  # audit:` produces nothing, so a
declaration that leans on a commented job fails with
`declares required check context 'audit', but no job in .github/workflows produces it`.

### 3.2 `.yml` only

Both readers globbed `*.yml`. GitHub reads `.yaml` as a workflow too. Measured with a single
`gates.yaml` carrying the declared job:

| | Before | After |
|---|---|---|
| `check_declared_check_contexts.main` on a `.yaml`-only workflow tree | exit 2 — `INCOMPLETE: no workflows under .github/workflows` | exit 0, the context is produced |
| `check_test_reachability` on a `.yaml` workflow with a `discover` root and a gate `run:` | the file was not read at all | 0 unreachable, gate wired |

## 4. Defect 3 — a comment made a test reachable

Rule B matches a test's path, name, stem or dotted module against the concatenated workflow text.
That text was the raw file, so a name in a comment counted as executed while the *gate* branch in
the same module already stripped comments — two answers to one question, and the permissive one
won. Measured on a tree with one test file and a workflow whose only mention of it is a `# TODO`
comment:

| | Before | After |
|---|---|---|
| `check_test_reachability` | exit 0, "0 unreachable" — the test is reported executed | exit 1, `pkg/test_x.py` printed as unreachable |

The same reading was applied one step earlier: a commented-out
`# - run: python3 -m unittest discover -s pkg` was a discovery root and reached every test under
`pkg`. Both branches now read one comment-stripped view of each file, produced by the
`strip_comment` helper the gate branch already used.

## 5. What changed

| File | Change |
|---|---|
| `scripts/ci/check_repository_hygiene.py` | Two `return []` branches become `RuntimeError`; `CHECK_VERSION` → `2026-11-27.1`; docstring states the fail-closed rule and why an empty side is not a satisfied relation |
| `scripts/check_declared_check_contexts.py` | `strip_yaml_comment` / `strip_yaml_comments`, applied inside `produced_contexts`; `WORKFLOW_GLOBS = ("*.yml", "*.yaml")` with a `workflow_files()` helper |
| `scripts/ci/check_test_reachability.py` | `WORKFLOW_GLOBS` in `read_workflows`; new `workflow_text()` (comment-stripped) used by both `discovery_rules` and the Rule B text |
| `scripts/test_check_repository_hygiene.py` | `with_index` fixture switch, two fail-closed cases, and a `commit()` helper that gives every fixture both sides of the membership relation |
| `scripts/test_check_declared_check_contexts.py` | Three cases: commented header, commented job, `.yaml` workflow |
| `scripts/ci/test_check_test_reachability.py` | Three cases: commented test name, commented `discover`, `.yaml` workflow for both branches |

## 6. Measured before and after

All numbers were produced in this working tree. The "before" side ran the same command against a
detached worktree at `origin/main` = `2f4f4118`.

| Quantity | Before | After |
|---|---|---|
| `check_repository_hygiene.py` version | `2026-11-24.8` | `2026-11-27.1` |
| `Work-item index membership ... directories= / linked=` | 106 / 106, exit 0 | 106 / 106, exit 0 |
| `check_declared_check_contexts.py` | 16 declared, 16 produced, exit 0 | 16 declared, 16 produced, exit 0 |
| `check_test_reachability.py` | 65 test files, 65 reachable; 18 gate scripts, 3 unwired, 3 baselined | identical |
| `scripts/test_check_repository_hygiene.py` | Ran 97, OK (skipped=1) | Ran 99, OK (skipped=1) |
| `scripts/ci/test_check_test_reachability.py` | Ran 24, OK | Ran 27, OK |
| `scripts/test_check_declared_check_contexts.py` | Ran 13, OK | Ran 16, OK |

The declared-versus-produced half of `check_declared_check_contexts` is deliberately run with the
protected side injected from the declaration: the live branch-protection payload needs a token
and a network round trip, and this record claims no platform result. `check_repository_hygiene`
and `check_test_reachability` are run as CI runs them, against this tree.

## 7. The new tests are falsifiable

Each fix was reverted alone, and the suite re-run. The failures are exactly the new cases:

| Reverted | New cases that fail | Everything else |
|---|---|---|
| `strip_yaml_comments` in `produced_contexts` | `test_jobs_header_with_a_trailing_comment_still_produces_contexts`, `test_yaml_workflow_suffix_is_read` | green |
| `*.yaml` half of the glob, in both readers | `test_yaml_workflow_suffix_is_read_for_both_branches`, `test_yaml_workflow_suffix_is_read` | green |
| Comment stripping of the Rule B text | `test_test_named_only_in_a_comment_is_unreachable` | green |

The two fail-closed cases assert exit 2 and the message, so the pre-fix `[]` cannot satisfy them:
`[]` exits 0 by construction.

## 8. The fixture change is not a weakened case

`scripts/test_check_repository_hygiene.py` shared a `commit()` helper that wrote every fixture's
files plus an empty schema registry. Those fixtures had no work-item directory and no
`INDEX.md`, so the membership check now fails closed on them — correctly, and for a reason that
has nothing to do with what those cases test. The helper therefore writes one work-item directory
and an `INDEX.md` row for every directory the fixture carries, unless the case passes its own or
sets `with_index=False`.

This was checked both ways: 65 of 97 cases failed when the helper was not updated, and the two
cases that are *about* the absent sides use `with_index=False` and assert exit 2.

## 9. What this record does not claim

- No CI context result, on any SHA.
- No merge SHA, and no branch-protection state.
- No change to the sixteen declared contexts, the sixteen produced contexts, or any job name.
- No new gate-wiring baseline entry: the three baselined unwired gates stay baselined.
- Nothing about a checker this unit did not name.
