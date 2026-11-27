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
        - "14-ai-development/work-items/AID-2026-279/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Schema and state machine are enforced by scripts/ci/check_work_item_registry.py and its 15 local tests; the live pull-request check was not exercised against the GitHub API in this session."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "work-item-uniqueness"
      - "claim-registry"
      - "registry-schema"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-279 — Claim registry design

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-27
**Issue:** #1341

## Why a registry at all

The tree comparison in `check_work_item_uniqueness.py` answers one question: does
this candidate introduce a directory that the target branch already has? It
cannot answer "is another open pull request about to introduce it too", because
an open pull request has no tree on the target branch. Two branches that both
add `AID-2026-NNN/` are both "new" until one of them merges.

The registry is that missing fact: an authoritative, reviewed record of which
pull request holds which id. It is a ledger, not a lock — it is read by the gate
and written by the pull request that claims an id.

## Location and shape

```
14-ai-development/work-items/registry/work-item-claims.yaml
```

One exact path. `scripts/ci/check_repository_hygiene.py` admits it by an
anchored regex (`WORK_ITEM_CLAIMS_REGISTRY_RE`); a sibling `.yaml` in the same
directory is still refused, so the directory cannot grow into a fragment store.

```yaml
schema_version: 1
claims:
  - work_item_id: AID-2026-279
    status: MERGED                     # CLAIMED | MERGED | ABANDONED
    pull_request: 1372                 # integer, the claiming pull request
    repository: oahcom/AiMemoryBrainArchitecture
    head_sha: 82daefb8...              # candidate head at claim time
    merge_commit_sha: 386d8f57...      # required iff status is MERGED
    claimed_at: "2026-11-27T03:41:00Z"
    updated_at: "2026-11-27T04:17:27Z"
    owner_work_item: AID-2026-279
    evidence:                          # paths that justify the row
      - "14-ai-development/work-items/AID-2026-279/manifest.yaml"
```

One row per `(work_item_id, pull_request, repository)`. A transition mutates the
existing row; it does not append a second row for the same pull request.

## State machine

| From | To | Allowed | Note |
|---|---|---|---|
| CLAIMED | MERGED | yes | requires `merge_commit_sha` |
| CLAIMED | ABANDONED | yes | the id is **not** released automatically |
| MERGED | anything | no | MERGED is terminal and permanent |
| ABANDONED | anything | no | a human edits the ledger; no automatic reclaim |

Enforced by `scripts/ci/check_work_item_registry.py`:

* schema — required fields, status enum, `pull_request` positive integer,
  `repository` as `owner/name`, 40-character lowercase `head_sha`,
  `merge_commit_sha` present iff MERGED, `updated_at >= claimed_at`,
  non-empty `evidence` for CLAIMED/MERGED;
* state — at most one CLAIMED row per id, no CLAIMED row for an id that already
  has a MERGED row, no claim that starts after the merge;
* history — with `--previous <file>`, every row must move along an allowed edge,
  MERGED rows must stay MERGED, and rows may never be deleted;
* live — with `--check-live-prs`, every CLAIMED row's `head_sha` must match the
  pull request's current head and the pull request must be open. A missing
  token, an HTTP error, or an unparsable body is exit 2 (INCOMPLETE). The check
  never guesses a verdict.

## How the uniqueness gate consumes it

`check_work_item_uniqueness.py --registry <path>` reads the ledger **from the
target tree** (`--base`). The target branch is authoritative: a claim that only
exists on the candidate side cannot authorise the candidate.

Two deliberate rules:

1. **Bootstrap.** When the ledger is absent from the base tree but present on
   the candidate tree, the candidate copy is read and the summary says
   `registry=head ... (bootstrap)`. This is what lets the change that introduces
   the ledger pass its own gate.
2. **Absence is empty, not INCOMPLETE.** When neither tree has the ledger, the
   claim list is empty and the summary says `registry=absent`. The Owner ruling
   is explicit that the gate must not depend on registry completeness, because
   ids that already exist on the target tree are rejected by the tree
   comparison alone. An *unreadable or malformed* ledger is still exit 2: that
   is a broken input, not a missing one.

A new id is rejected when a row for it is CLAIMED or MERGED by a different
pull request. Pass `--pull-request N --repository owner/name` so a candidate is
not blocked by its own row. ABANDONED rows do not block: per the ruling the id
is not released automatically, so a reclaim is a human edit of the ledger, and
the validator rejects a MERGED id being claimed again.

## Initial contents

`AID-2026-279` is recorded as MERGED by pull request 1372 at
`386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`. Earlier merged ids are intentionally
left out: backfilling 118 rows would be an unverifiable guess, and the tree
comparison already rejects them.
