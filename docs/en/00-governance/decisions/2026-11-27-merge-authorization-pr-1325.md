---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "delegated operator (coordinating session) under explicit human-owner authorization; not a natural-person signature"
      decision_date: "2026-11-27"
      approved_version:
        scheme: content-hash
        value: "db3745d513da7b5e0d2e13eb6bd4d9e20ce54f5ff563b8bf013b5d5814f4b0a8"
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "OA-MERGE-2026-11-27-1325"
        - "14-ai-development/PR-GOVERNANCE-001.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "The conditions in this record are checked at the merge decision point; whether each held is not asserted here."
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
    # Translation of the authoritative source. It does not independently
    # claim canonical authority; see bilingual_counterpart below.
    canonical_status: Non-Canonical
    canonical_scope: "Delegated merge authorization for PR #1325"
    canonical_scope_id: "ai-development/decisions/oa-merge-2026-11-27-1325"
    canonical_scope_keywords:
      - merge-authorization
      - delegated-operator
      - pr-1325
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "00-governance/decisions/2026-11-27-merge-authorization-pr-1325.md"
    zh-CN: "docs/zh-CN/00-governance/decisions/2026-11-27-merge-authorization-pr-1325.md"
  steward: "Architecture Governance (delegated operator for this record)"
---

# Merge Authorization Record — PR #1325 (Delegated Publication)

- Decision ID: `OA-MERGE-2026-11-27-1325`
- Subject: at most one merge of pull request #1325
- Publication date: 2026-11-27
- Publication identity: GitHub account `oahcom`
- Record status: published authorization, bounded and revocable; it authorizes no action by itself

## 1. Authorization subject and proxy-publication declaration

This record is published by the coordinating layer acting as a **delegated operator**, on the
basis of the human owner's explicit authorization that the coordinating layer may converge the
human role for this decision. The GitHub account `oahcom` is the **publishing identity only**.
Its appearance on this commit does not signify, and must not be read as, a document signed by
Owner A in person. No natural-person signature exists for this record, and none is claimed.

The coordinating layer is a non-human agent. It is not a natural person, it does not hold the
owner role, and this record grants it nothing beyond section 3.

## 2. Delegation source and its boundary

- Delegation source: the human owner's explicit authorization to the coordinating layer to
  converge the human role for the merge decision on PR #1325, given in the adjudicating session
  on 2026-11-27. It is **not** recorded as a separate delegation file; this record is the first
  repository-internal artifact of that authorization, and the absence of an earlier file is
  stated rather than papered over.
- Boundary: the authorization covers the decision to permit **one** merge of PR #1325. It does
  not transfer ownership, does not authorize any other pull request, and does not authorize
  changing this repository's branch protection, required contexts, or review rules.

## 3. Authorized scope

1. PR #1325 only.
2. One merge only. A second merge, a re-merge after revert, or a merge of any other PR requires
   a new record with a new Decision ID.
3. No condition in section 4 may be waived, reordered, reinterpreted, or satisfied by argument
   in place of evidence. If a condition cannot be evidenced, the merge does not happen.

## 4. Effective conditions — all five must hold at the merge decision point

The technical state below was measured on head
`a3c236823138bd138e747f71098c4019bd67c560` by the independent forensics pass (W1). It is
recorded as **measurement, not as standing permission**: the head will change when the branch is
refreshed, and every condition must be re-established on the new head.

1. **Fresh head.** The branch is refreshed onto the then-current `main` and a new head SHA is
   obtained. The SHA in this record is historical evidence and authorizes nothing.
2. **All required contexts green on that exact head.** All 16 required status contexts report
   `SUCCESS`; no `pending`, no `failure`, no absent context. The 16 names were compared
   character-for-character against `GET /repos/{owner}/{repo}/branches/main/protection` and
   matched.
3. **`mergeable_state=clean`.** At the measured head the state was `behind` (7 commits behind
   `main`), which is not clean and therefore not mergeable under this authorization until
   refreshed.
4. **SHA stability.** The head SHA observed at verification and the head SHA at merge are
   identical. A push between the two invalidates the verification.
5. **Review evidence independent of the authoring session.** Evidence that the change was
   examined by a party other than the session that authored it must exist and be citable. Ways
   to obtain it, in order of preference: (a) a review or comment from a GitHub account that is
   not the authoring session's publishing identity; (b) a recorded second-session review with
   its session identifier and the material it read; (c) a re-derivation of the changed claims
   from the repository by a party that did not write them, with the commands and outputs kept.
   A green CI run is not a substitute for any of these.

Recorded protection state at measurement: `strict=true`, `enforce_admins=true`, no required
review. `enforce_admins=true` means the merge path cannot bypass the required contexts, and the
absence of required review means condition 5 is **not** satisfied by branch protection — it must
be satisfied by evidence produced outside it.

## 5. Invalidation

This authorization lapses, without further notice, when any of the following holds:

1. Any condition in section 4 fails or cannot be evidenced.
2. The head SHA changes after verification.
3. The scope of PR #1325 changes: additional commits that alter the substance of the change,
   a widened diff, or a retitled/repurposed PR.
4. The branch protection configuration changes such that the 16-context comparison in condition
   2 no longer holds.
5. The human owner withdraws the delegation.

## 6. Minimum post-merge readback

After the merge, record and retain:

1. `main` SHA after the merge.
2. The merge commit SHA.
3. The file listing of `AID-2026-241/` as it exists on `main`.
4. The corresponding `14-ai-development/work-items/INDEX.md` line.
5. `git log -1` output for `main`.

A readback item that cannot be produced is reported as `NOT_RECORDED`, not inferred.

## 7. Known risks

- **Self-reference.** PR #1325 modifies the rule that decides whether independent review is
  established by a session or by an account. The authoring session's own assessment of that
  change is therefore self-referential: it evaluates the rule that would validate its own work.
  This is recorded as a risk, not resolved by this record.
- **CI is not review.** A green 16-context run proves that the declared checks passed on a
  commit. It does not prove that an independent party examined the change, and it must not be
  used to satisfy condition 5. CI green must not replace independent review.
- **Stale measurement.** Every technical value in section 4 was measured before the branch
  refresh. Treating it as current after a refresh is the specific error this section exists to
  prevent.
- **Measurement channel unavailable.** At publication time the GitHub API quota for this
  workspace was exhausted (HTTP 403), so the section 4 values could not be re-measured here.
  They are reported as previously measured, not as freshly verified.

## 8. Audit fields

| Field | Value |
|---|---|
| `decision_id` | `OA-MERGE-2026-11-27-1325` |
| `authorization_channel` | human owner's explicit authorization to the coordinating layer in the adjudicating session, 2026-11-27; published to the repository by the delegated operator |
| `published_by` | GitHub account `oahcom`, acting as delegated operator (publishing identity only) |
| `delegation_source` | human-owner authorization to converge the human role for this decision; `NOT_RECORDED` as a separate delegation document |
| `authorized_scope` | PR #1325, one merge |
| `measured_head` | `a3c236823138bd138e747f71098c4019bd67c560` (historical; authorizes nothing) |
| `NOT_RECORDED` | `NO_NATURAL_PERSON_SIGNATURE; DELEGATED_OPERATOR_DECISION` |
| `review_independence` | not established by this record; see condition 5 |

Nothing in this record asserts that Owner A personally reviewed, approved, signed, or merged
anything. The only claim it makes is that a delegated operator, authorized by the human owner,
published a bounded and revocable merge authorization whose conditions are checkable.
