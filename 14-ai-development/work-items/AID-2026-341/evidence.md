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
        - "14-ai-development/work-items/AID-2026-341/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Local suite passes; independent review is pending."
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
      - "shared-id"
      - "duplicate-declaration"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-341 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-28
**Issue:** #1341
**Implementation base observed:** 31c1e5d83e7dad326dbd4b69d4a8e19534718ff1

## Session role / use case

Implementation session for Issue #1341. Scope: replace the shared-ID
modification/deletion rejection in the work-item uniqueness gate with a
tree-level duplicate-declaration rule, and prove the replacement against the
pinned first-parent window of main.

## Actual AI input

The executed instruction is recorded verbatim in `prompt-v1.md`. It required:
read the old rule's real code location; replace it with the section 4 rule
(candidate-tree duplicate declarations only); separate `introduced_ids` from
`occupied_ids`; treat `base_tip` as the occupancy basis and `merge_base` as
provenance only; and produce a regression fixture over the eight most recent
first-parent commits plus three positive cases.

Two review rulings then constrained the implementation: canonical manifest
paths (not `git grep` over arbitrary YAML) as the record set, with legacy
identity shapes read from content; deletion of the unreachable `occupied`
branch; a pinned old-rule oracle instead of a weak subset assertion; a hard
failure when the pinned window is missing; a target-tree-only claim ledger; and
a merge-group-aware workflow. The exact ruling text is in the session record.

## AI-visible output

Measured state of this change.

Two earlier rules produced false verdicts. The first, in the `#1413` carrier,
treated a modified or deleted path under an id the target branch already owned
as a competing declaration: `competing_claims()`,
`elif status in ("M", "D", "T", "R", "C")`, present in the pinned oracle at
`scripts/ci/fixtures/legacy_shared_id_rule_1413.py:160`. The second is the
tree-only verdict merged by PR #1477 (commit `a0500d519`): it reported
`VIOLATION new_paths=...` for any file added under an existing work-item
directory and `DELETION` with exit 1 for a directory absent from the candidate,
without ever reading a manifest identity. Section 4.4 requires both of those
outcomes to pass, so this change replaces the tree-only verdict rather than
adding to it.

Pinned first-parent window (base = first parent, old rule = the #1413 copy):

```text
commit     base       verdict_old  verdict_new  triggering_ids
31c1e5d83  159095f3c  VIOLATION    PASS         45
159095f3c  56c3fe1b2  PASS         PASS         0
56c3fe1b2  561e9f247  PASS         PASS         0
561e9f247  981397d99  PASS         PASS         0
981397d99  460f437eb  PASS         PASS         0
460f437eb  6482901cb  PASS         PASS         0
6482901cb  da69e43f8  VIOLATION    PASS         1
da69e43f8  cd1722e75  PASS         PASS         0
```

The old rule rejected two of the eight commits, not the four asserted in the
ruling narrative. The measured set is pinned in the test; the difference is
reported rather than explained away.

Triggering ids for `31c1e5d83`: AID-2026-001, 003, 009, 054–064, 066–085,
089–099, 252 (45 ids, all `M`/`D` under shared ids). For `6482901cb`:
AID-2026-291 (1 id).

Positive cases executed by the suite:

```text
two work-item directories declaring one id          -> VIOLATION (DUPLICATE_WORK_ITEM_ID)
base record + candidate second path in merge tree   -> VIOLATION (DUPLICATE_WORK_ITEM_ID)
other pull request's CLAIMED ledger entry           -> VIOLATION (claim ledger)
record with no supported identity field             -> VIOLATION (WORK_ITEM_ID_MISSING)
record whose id disagrees with its directory        -> VIOLATION (WORK_ITEM_PATH_ID_MISMATCH)
candidate-supplied ledger, base has none            -> INCOMPLETE (not authoritative)
```

Legal shared-id operations executed by the suite: same-path modification,
deletion, and additive files under an existing record all PASS.

## Record discovery and identity

Records are enumerated by canonical path
`14-ai-development/work-items/<AID-or-FIX-id>/manifest.yaml`. The id is read
from content: top-level `work_item_id`, legacy top-level `aid`, or legacy
nested `work_item.proposed_id`. The directory name is used only to check
agreement with the declared id. An unreadable or unparseable blob is
INCOMPLETE; a parsed record with no usable identity, or one that disagrees with
its own directory, is a VIOLATION.

At the observed commit the enumeration yields 138 records (AID and FIX
families), including the legacy shapes; no duplicate declaration and no
identity conflict exists on main, so the gate passes on the target tree.

## Claim ledger trust boundary

The ledger is read from the target tree only. If the target tree has no ledger
and the candidate supplies one, the gate is INCOMPLETE: a candidate may not
define the occupancy evidence that decides its own verdict. `--pull-request`
without `--repository` is INCOMPLETE, and the own-claim exemption requires both
the pull request number and the repository to match.

## Workflow

`document-management.yml` had no `merge_group` trigger at the observed commit,
although it carries a required context. This change adds
`merge_group: types: [checks_requested]`, uses
`github.event.merge_group.head_sha` and `github.event.merge_group.base_sha`,
serializes on `github.event.merge_group.base_ref`, removes the stale
pull_request base SHA from the enforcement step, and fails closed on an
unrecognized event.

## Verification status

```text
python scripts/ci/test_work_item_uniqueness.py
[regression] rows=8 old_red=2 old_pass=6 new_red=0 new_pass=8
Ran 28 tests
OK
```

The branch carries one merge of `origin/main` at
`473f06d76f7a06ff91615a2dae0ddd75295391c0`; on the two checker files the merge
kept this branch's version and discarded #1477's tree-only implementation and
its incompatible tests, as the ruling required. No other file was resolved by
whole-side selection.

No merge of the pull request, no force push, no branch-protection change, and
no real merge-queue run is claimed by this document.
