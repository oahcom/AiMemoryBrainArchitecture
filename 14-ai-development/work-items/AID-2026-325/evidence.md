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
        - "14-ai-development/work-items/AID-2026-325/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Measurements below are transcribed from the supplied verification record; this authoring session has not independently rerun the commands or API requests."
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
    canonical_scope: "Measurement log supporting the AID-2026-325 decision on session-level independent review."
    canonical_scope_id: "ai-development/aid-2026-325-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-325"
      - "measurements"
      - "verification"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-325

## 1. Evidence boundary

This file records the supplied measurements for the decision in
`decision.md`.

The measurements belong to different repository states and must not be
combined as if they came from one corpus snapshot.

- Independent verification of the original issue: commit `9c3ecf2`,
  56 manifests.
- Current implementation and corpus measurements: base commit
  `5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0`, 130 manifests.
- Merged implementation: PR #1325, merge commit
  `3daebd2cad699b5ecccd7ffa7df86029dfbecec6`.

The current authoring session has not independently executed these
commands or API requests. The values below are attributed to the
supplied measurement record, not represented as fresh observations.

## 2. Original issue reproduction

The original defect was reproduced at `9c3ecf2`.

Case A: same GitHub identity, different sessions.

Expected under amended §5: independent.

Original gate result:

```text
{"result": "FAIL", "error": "REVIEWED reviewer and implementer must be different identities"}
```

Case B: different GitHub identities, same session.

Expected under amended §5: not independent.

Original gate result:

```text
{"result": "PASS", "phase": "VALIDATION", "content_integrity": "PASS", "source_authenticity": "NOT_VERIFIED"}
```

The two cases demonstrate that the old identity predicate was both
over-restrictive and under-restrictive relative to the governing
session-level rule.

## 3. Independent verification corrections

The independent verification comment dated
`2026-11-26T07:20:31Z` corrected two measurements in the original issue.

### 3.1 Original manifest count and gate records

The original issue stated 57 manifests and zero independent-review
records.

The corrected measurement was:

```text
56 manifests total

4 manifests carried lifecycle.gates.independent_review:

AID-2026-005  NOT_RECORDED
AID-2026-006  NOT_RECORDED
AID-2026-008  PENDING
AID-2026-009  NOT_RECORDED

0 of 56 carried independent_review status PASS.
```

### 3.2 Original checker distribution

The independently verified distribution at `9c3ecf2` was:

```text
2 pass / 54 fail of 56

37  status is not an exact canonical state
15  missing/invalid lifecycle
 1  unknown gate records: registration
 1  invalid gate disposition: merge
```

These failures explain why most manifests did not reach the
independent-review comparison.

### 3.3 Reproduction environment limitation

A shallow clone is insufficient for reproducing the original
measurement.

The checker reports:

```text
sidecar commit message lacks a sha256 anchor
```

A full clone is required.

### 3.4 Explicit verification limitation

The independent verification did not determine whether session-level
independence is representable as proof in a manifest.

That is a design limitation, not a result established by the tree.

## 4. Current repository write identities

Measured at base commit
`5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0`.

Request:

```text
GET /repos/oahcom/AiMemoryBrainArchitecture/collaborators?affiliation=direct&per_page=100
```

Result:

```text
1 entry:
login=oahcom

permissions:
  admin: true
  maintain: true
  push: true
  triage: true
  pull: true
```

Repository owner:

```text
GET /repos/oahcom/AiMemoryBrainArchitecture

owner.login = oahcom

permissions:
  admin: true
  maintain: true
  push: true
  triage: true
  pull: true
```

Measured conclusion: exactly one direct account has push permission.

## 5. Commit authorship distribution

Command:

```bash
git log --format='%an <%ae>'
```

Measured over 3239 commits reachable from HEAD:

```text
3239  total commits reachable from HEAD
2337  oahcom <81014746+oahcom@users.noreply.github.com>
 172  t <t@example.invalid>
  87  oahcom <1491856051@qq.com>
  60  Ubuntu <ubuntu@localhost.localdomain>
  55  oahcom <oahcom@users.noreply.github.com>
  35  unknown <1491856051>
```

The three `oahcom` author/email forms account for:

```text
2479 of 3239 commits
76.6 %
```

The other author strings are local build identities in the supplied
measurement. They are not evidence of additional GitHub accounts.

## 6. Pull request author and merger identities

The list endpoint returned `merged_by: null` for the supplied token.
The measurements therefore used individual pull-request fetches:

```text
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/{number}
```

Fields inspected:

- `user.login`
- `merged_by.login`

Ten most recently merged PRs in the supplied sample:

```text
#1446 author=oahcom merged_by=oahcom 2026-11-27T07:20:45Z merge=f64a3f8bd004135e9873aeafc40e50ef10e10a9c
#1421 author=oahcom merged_by=oahcom 2026-11-27T07:16:58Z merge=b4c1b11d1263b0750d5701208d6fe5be317350d7
#1442 author=oahcom merged_by=oahcom 2026-11-27T07:09:35Z merge=5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0
#1440 author=oahcom merged_by=oahcom 2026-11-27T07:01:40Z merge=f20fff10307f512d3c299b6371f172c85f941e30
#1416 author=oahcom merged_by=oahcom 2026-11-27T06:49:59Z merge=7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19
#1408 author=oahcom merged_by=oahcom 2026-11-27T06:14:16Z merge=7ecf2a8e7d1e40a13f6af6d4335a6766a222194f
#1429 author=oahcom merged_by=oahcom 2026-11-27T06:42:36Z merge=cbdaf78313404fc24a6c250dc06faa72d4d0b97c
#1435 author=oahcom merged_by=oahcom 2026-11-27T06:35:59Z merge=056209b71c2e559efa3526a31870187a8e6e47f2
#1423 author=oahcom merged_by=oahcom 2026-11-27T06:32:41Z merge=5670357db7a836d4f26838dbaf99494af41e2b65
#1409 author=oahcom merged_by=oahcom 2026-11-27T06:19:12Z merge=229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c
```

Result:

```text
same-account: 10 of 10
```

Wider sample:

```text
132 merged pull requests
132 of 132 authored by oahcom
```

PR #1325:

```text
author=oahcom
merged_by=oahcom
merged=2026-11-27T04:38:43Z
merge_commit=3daebd2cad699b5ecccd7ffa7df86029dfbecec6
```

These are observed repository workflow measurements. They do not
establish that a read-only external reviewer is technically impossible.

## 7. Accountable-owner distribution

Measured across 130 work-item manifests:

```text
102  USER-PRINCIPAL-DELEGATED
  9  NOT_ASSIGNED
  3  Integration Owner
  2  A
  2  USER-PRINCIPAL-DELEGATED (session-eligible per D-2026-1120-02)
  1  Project Owner adoption authority; not inferred from this session
  1  Project Owner (adoption authority)
  1  USER-PRINCIPAL-DELEGATED (Owner instrument, Issue #305 comment 7042461592)
  1  USER-PRINCIPAL-DELEGATED (session-eligible under the user's continuous instruction in this session)
  1  Owner G
  1  Owner C / Owner G joint
  1  Owner A coordination
  1  Owner H; cross-owner acceptance by C/G/D/I/Storage as applicable
  1  Owner A / Governance coordination; D/E/F/I content Owners retain domain acceptance
  1  user-authorized operator (delegated by account owner)
```

No manifest in the supplied measurement names a second GitHub
account as owner.

The delegate is the single principal in this accounting. The literal
`NOT_ASSIGNED` is already present in the tree.

## 8. Current gate state

Command:

```bash
python scripts/governance/status_migration/check_status_gates.py
```

Measured result over 130 manifests:

```text
exit 1
130 total
2 PASS / 128 FAIL
```

Failure distribution:

```text
 88  status is not an exact canonical state
 38  missing/invalid lifecycle
  1  unknown gate records: registration
  1  invalid gate disposition: merge
```

Zero failures are the old identity-comparison error.

The string:

```text
REVIEWED reviewer and implementer must be different identities
```

does not occur in the measured corpus output.

Independent-review records:

```text
5 of 130 manifests

AID-2026-005  NOT_RECORDED
AID-2026-006  NOT_RECORDED
AID-2026-008  PENDING
AID-2026-009  NOT_RECORDED
AID-2026-026  NOT_STARTED

0 of 130 carry status PASS.
```

The corpus result is not a claim that the checker passes overall.
It exits 1 because the other validation failures remain.

## 9. Behavioral tests

Command:

```bash
cd scripts/governance/status_migration && python -m unittest test_status_migration
```

Measured result:

```text
Ran 31 tests in 94.606s

OK
```

The discriminating tests are:

```text
test_one_account_with_two_sessions_is_independent
test_two_accounts_sharing_one_session_is_not_independent
```

Together they test the two cases that the retired identity predicate
misclassified.

## 10. CI wiring

Command:

```bash
git grep -l check_status_gates -- .github/workflows
```

Measured result:

```text
(no output)
```

The supplied measurement also identifies references in:

```text
14-ai-development/governance-register/evidence/main-paths.json
AID-2026-085 records
```

Those references do not constitute GitHub Actions workflow wiring.

## 11. Current implementation excerpt

At base commit `5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0`,
the independent-review arm contains:

```python
if name == "independent_review":
    aliases = _normalized_aliases(data.get("review_identity_aliases", {}))
    # Diagnostic only, never the verdict: independence is decided by the
    # reviewing session, so two sessions on one GitHub account are the
    # expected case and must pass.  Kept because the alias table is part of
    # the manifest contract and must still be validated when present.
    _same_account = (_identity(evidence["reviewer"], aliases)
                     == _identity(evidence["implementer"], aliases))
    # The check verifies that the manifest DECLARES two sessions.  It does
    # not and cannot verify that two sessions existed: a session value is a
    # string the writer chooses, and no artifact in this repository can
    # corroborate it.
    if _session_token(evidence["reviewer_session"]) == _session_token(
            evidence["implementer_session"]):
        raise ValueError(
            "REVIEWED reviewer_session and implementer_session must be different sessions")
```

The required evidence tuple is:

```python
"independent_review": ("reviewer", "implementer", "reviewer_session", "implementer_session",
                       "reviewed_head", "report", "findings_disposition"),
```

The `_session_token` function performs NFKC normalization, casefolding,
and stripping to `[a-z0-9]`. An empty normalized token is rejected.

The `_same_account` assignment appears exactly once in the file and
is never read.

This establishes the implementation's current declaration comparison
and its dead diagnostic limitation.

## 12. Merged implementation record

PR #1325:

```text
title:
fix(241): decide independent review by session, not by GitHub account

author:
oahcom

merged_by:
oahcom

merged_at:
2026-11-27T04:38:43Z

merge_commit:
3daebd2cad699b5ecccd7ffa7df86029dfbecec6

final_head:
fe16a378930e3f06a71a55e6b9036fb9397522f1
```

Delivery verification:

```text
16/16 required contexts SUCCESS
behind=0
```

The delivery comment reports a per-file check of all six files of
AID-2026-241 and equality between the merge commit blobs and
`origin/main` blobs.

The corresponding main commit is:

```text
0f7dfbc9
fix(082): decide independent review by session, not by GitHub account
```

The subject identifier difference between `082` and the PR title's
`241` is recorded as an observation only.

The implementation manifest is:

```text
14-ai-development/work-items/AID-2026-241/manifest.yaml
```

Recorded status: `MERGED`.

## 13. Reproduction commands and limitations

The following commands are the principal local verification surfaces:

```bash
python scripts/governance/status_migration/check_status_gates.py
```

```bash
cd scripts/governance/status_migration && python -m unittest test_status_migration
```

```bash
git grep -l check_status_gates -- .github/workflows
```

The GitHub account and pull-request measurements require API access.
The individual PR endpoint must be used to retrieve `merged_by` for
the supplied measurement because the list endpoint returned null for
that field.

The original 56-manifest verification requires a full clone because
the checker needs the sidecar commit-message SHA-256 anchor.

The current 130-manifest figures are tied to base commit
`5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0`. They must not be
represented as a fresh measurement of a later HEAD without rerunning
the commands.

## 14. Evidence limitations

This evidence record does not establish:

- That writer-declared session strings correspond to distinct real
  execution contexts.
- That session provenance is independently corroborated.
- That the checker has CI enforcement.
- That the `_same_account` assignment produces an observable
  diagnostic.
- That the 130-manifest checker exits successfully.
- That AID-2026-325 has been reviewed, accepted, or merged.

Those limitations remain explicit in the decision and manifest.
