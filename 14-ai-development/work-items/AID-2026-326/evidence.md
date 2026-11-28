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
        - "14-ai-development/work-items/AID-2026-326/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "The initial probe results and baseline are supplied by the requester. No independent command execution or live API measurement is claimed."
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
    canonical_scope: "Evidence boundary and acceptance measurements for AID-2026-326."
    canonical_scope_id: "ai-development/aid-2026-326-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-326"
      - "execution"
      - "evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-326

## 1. Evidence boundary

This document records the facts supplied with Issue #1469 and the
implementation's intended verification criteria.

The following are supplied measurements, not measurements independently
reproduced by the authoring session.

Baseline:

`31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`

Canonical declaration source:

`14-ai-development/PR-GOVERNANCE-001.md`

Existing static declaration checker:

`scripts/check_declared_check_contexts.py`

The canonical document and existing checker are not modified by this
work item.

## 2. Existing declaration contract

The existing checker validates:

`required ⊆ declared ⊆ produced`

The produced set is derived from workflow job IDs and job display
names in `.github/workflows/*.yml` and `.yaml`.

This proves static workflow declaration, not actual execution on a
particular PR head.

The supplied measurements also report:

```text
git grep -l "check-runs\|check_runs" origin/main -- scripts .github
(no output)

git grep -l "mergeable_state" origin/main -- scripts .github
(no output)
```

Accordingly, the stated gap is execution evidence rather than another
static workflow declaration check.

## 3. Supplied scheduling probes

The requester supplied the following observations:

### Dirty mergeability

On the same branch and same head:

```text
mergeable_state=dirty
t+20s:  runs=0
t+140s: runs=0
```

The supplied interpretation is that GitHub did not schedule the
workflows for this dirty head.

### Clean head

After:

```text
git reset --hard origin/main
git commit --allow-empty
```

The supplied observation was:

```text
25 seconds:
8 workflow runs
all completed
```

### Draft behavior

The supplied observation was:

```text
clean + draft
60 seconds:
8 workflow runs
```

This falsifies the proposition that draft status alone prevents
workflow scheduling in the tested case.

### Lazy mergeability computation

Immediately after push/rebase, GitHub may return:

```text
mergeable_state=unknown
```

A subsequent read approximately one minute later may return:

```text
mergeable_state=dirty
```

The implementation must not classify the intermediate unknown
observation as proof of execution or as a definitive stale result.

These measurements are attributed to the supplied probe record.
They are not represented as fresh measurements by this session.

## 4. Required context declaration

The following sixteen exact strings are read at runtime from the
canonical fenced block.

```text
GOV-DOC-001 structural checks
Branch freshness vs base
audit
GOV-DOC-002 metadata checks
BMCP protocol index (hard gate)
BMCP conformance suite (hard gate)
Schema non-empty audit (hard gate)
Bilingual docs coverage (ratchet)
Rust clippy (hard gate)
Repository hygiene (hard gate)
Rust format (hard gate)
Rust doctests (hard gate)
Session Evidence
Session Evidence self-test (base)
Session Evidence self-test (head)
rust-workspace-test
```

This list is reproduced here for evidence readability only.
It is not an independent runtime source or an implementation constant.

## 5. Execution-verdict contract

| Verdict | Condition | Exit |
|---|---|---:|
| EXECUTED | All sixteen latest runs are completed/success | 0 |
| ABSENT | At least one context has no run on the exact head | 1 |
| STALE | mergeable_state is dirty | 1 |
| FAILED | A latest completed run has non-success conclusion | 1 |
| INCOMPLETE | Unknown persists, API fails, evidence is unreadable or a run is pending | 2 |

The classification is based on the current PR head SHA, not on
branch-level success or an earlier head's check runs.

When a context has multiple runs, the selected run is the one with
the maximum `started_at` string. API array position is not evidence
of recency.

## 6. Failure and uncertainty boundaries

The following distinctions are mandatory:

- No check run is ABSENT, not FAILED.
- A completed failure is FAILED, not ABSENT.
- A non-completed run is INCOMPLETE.
- An API exception is INCOMPLETE, not ABSENT.
- Missing authentication is INCOMPLETE, not ABSENT.
- Persistent mergeability unknown is INCOMPLETE.
- Dirty mergeability is STALE.
- A newer successful run supersedes an older failed run for the
  same context under the specified latest-run rule.

The implementation does not infer execution from workflow existence.

## 7. Workflow boundary

The new workflow is manually dispatched.

It is a reachability mechanism, not a new required context.

The following are explicitly outside this work item's authority:

- Modifying PR-GOVERNANCE-001.md.
- Modifying check_declared_check_contexts.py.
- Modifying scripts/test_check_document_management.py.
- Modifying required_status_checks.
- Weakening or removing any existing branch-protection requirement.

## 8. Verification status

No commands or tests are claimed as executed by this authoring session.

The delivery operator must independently establish:

1. The eight required offline test cases pass.
2. Additional authentication and parser failure tests pass.
3. The canonical declaration parses into exactly sixteen entries.
4. The latest-run ordering test selects the newer successful run.
5. The checker returns the specified exit codes.
6. The workflow remains outside branch-protection required contexts.
7. Repository governance and document-management gates pass.

Until those observations are recorded, implementation verification
remains NOT_VERIFIED.
