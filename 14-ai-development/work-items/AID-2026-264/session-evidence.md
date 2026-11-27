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
        - "14-ai-development/work-items/AID-2026-264/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "The three required sections are present with recorded content. Whether the recorded input is the complete dispatch is not machine-verifiable; the platform payload was not captured."
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
    canonical_scope_keywords:
      - "session-evidence"
      - "merge-authorization"
      - "pr-1325"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session evidence — AID-2026-264

## Session role / use case

Delegated-operator session `GOVREC-2026-11-27`, a non-human agent. The role was to publish a
repository-internal, attributable record of the human owner's bounded authorization to merge
PR #1325 at most once, and then to close out the two failing contexts on the PR that carries
that record (#1393) without rewriting history and without touching PR #1325's branch. The
session holds no owner role, signed nothing as a natural person, and merged nothing.

## Actual AI input

The verbatim dispatches are recorded in `prompt-v1.md`; this section states what they contained
and which part was operative, not a paraphrase of the whole task.

Block 1 (record authoring) named the decision to record — `OA-MERGE-2026-11-27-1325` — the
authorization source (the human owner's explicit authorization that the coordinating layer may
converge the human role), the prohibition on presenting delegated publication as a signature by
Owner A in person, the five effective conditions, the invalidation list, the post-merge readback
list, the self-reference risk, and the required audit fields. It also stated that the GitHub API
quota was exhausted and that PR creation should be recorded as `PR_NOT_CREATED_RATE_LIMIT` if
refused.

Block 2 (this close-out) stated the measured PR state (15/17 contexts success, `Branch freshness
vs base` and `Session Evidence` red), explained that the Session Evidence gate resolves each
declared reference against a Work Item manifest `session_evidence` entry in the PR head tree,
forbade rebase plus force push in favour of a plain `git merge origin/main`, required the new
work item `AID-2026-264` after a three-ref occupancy check, and listed the machine checks that
must be run and reported.

Both blocks were received as chat text in this session. The platform payload (transport bytes,
session identifier) was not captured, which is why the manifest records
`executed_prompt_provenance: NOT_VERIFIED` while the digest and byte count are real.

## AI-visible output

- `00-governance/decisions/2026-11-27-merge-authorization-pr-1325.md`, with `docs/en/` and
  `docs/zh-CN/` mirrors, all three carrying GOV-DOC-002 metadata and a body-bound
  `approved_version` content hash.
- This work item: `manifest.yaml`, `prompt-v1.md`, `session-evidence.md`, `evidence.md`, plus one
  row in `14-ai-development/work-items/INDEX.md`.
- Commit `9fbaa09ac6d38f3148302ad40474528c2202f3c6` (record) and
  `25b1ec6ebf88af22887f9631ee1e7e7078ea901c` (correction of an API-quota claim the record had
  made and that the session then falsified by succeeding), followed by a plain merge of
  `origin/main` into the branch.
- Local gate results: GOV-DOC-002 incremental PASS, bilingual gate PASS (3 changed paths),
  line-endings PASS (0 violations), repository hygiene new-file admission passed, `check_fmt`
  PASS, traceability index PASS. Raw output is kept in `D:\code\_aimb\round\govrec-gates.log`
  and summarised in `evidence.md`.

What this output does not contain: any claim that Owner A personally reviewed, approved, signed
or merged anything; any independent review of the record; and any evidence about PR #1325's
head, which was not re-measured.
