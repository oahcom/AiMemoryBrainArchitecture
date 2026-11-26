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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-25"
      last_verification_note: "This file is the recorded input of the re-verification session, written after the session. The digest in the work item manifest pins the bytes recorded here, not a prompt that was frozen before execution; executed_prompt_provenance is NOT_VERIFIED for that reason."
    usage_status: Active
    modification_status: Active-Modified
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

# Recorded input — AID-2026-064 / Issue #955

The operative instruction set for this session, reproduced as received. It is a task
assignment written in English; the session responded in Chinese per its language
directive, which is recorded in `session-evidence-955.md` rather than here.

## Assignment text

Repo: `/d/code/AiMemoryBrainArchitecture` (Windows host, bash shell). Create your own
worktree at `/d/wt/a955` from a freshly fetched `origin/main`. Do not touch any other
worktree under `/d/wt/`. Do not edit `/d/code/AiMemoryBrainArchitecture` in place.

### What to fix

Issue **#955**. `14-ai-development/work-items/AID-2026-004/manifest.yaml` declares
`bilingual_status: COMPLETE` and registers six blob SHAs (three source + three English
translation). All six have drifted from the current blobs.

The lead re-measured on `main @ 1a17d89e` and got drift on all six. The issue's own
framing is adopted as the ruling for this task:

- **Claimed:** `bilingual_status: COMPLETE` is an *activity assertion* — it asserts the
  two sides are aligned *now*. The files were edited after registration, so the field
  can no longer be read unconditionally as "aligned", and the manifest neither
  re-verified, nor downgraded, nor recorded a pending review.
- **Not claimed:** that the three pairs are currently semantically mismatched. Six
  drifted SHAs prove only that the *registered version* is stale, not that the
  *content* diverged.

Do not conflate those two. The fix direction is re-verification, not re-translation.

### What to do

1. **Re-read all six current blobs** and record, per file, the registered SHA and the
   current SHA. Report both.
2. **Do a content-side verification per pair, not a SHA refresh.** For each pair, diff
   the registered blob (`git cat-file -p <sha>`) against the current blob and confirm
   the translation covers the paragraphs the source gained. The issue already measured
   the drift as *symmetric* — source side +3/+64/+47 lines, translation side +1/+63/+46 —
   and concluded both sides were edited together (mostly a shared metadata header).
   **Verify that symmetry claim yourself** and report your own line deltas. If any pair
   is asymmetric in a way that means the source gained content the translation lacks,
   say so loudly — that changes the verdict for that pair.
3. **Choose the status honestly, per the issue's three-way enum:** `COMPLETE`
   (re-verified aligned), `PENDING_REVERIFICATION` (not yet verified), `DIVERGED`
   (mismatch found). **Refreshing the SHAs and restoring `COMPLETE` is explicitly
   forbidden** unless you actually verified content alignment and can state what you
   compared.
4. **Retain history.** Do not delete the six originally registered SHAs. They are the
   record of "this is where alignment last held". Keep them alongside the current values
   — read the manifest's existing style first and extend it in the same shape rather than
   inventing a new schema.
5. **Read the validator before choosing a status value.** Check whether anything
   validates `bilingual_status` against an enum — grep `scripts/check_bilingual_docs.py`,
   `scripts/check_document_management.py` and any manifest schema under `scripts/` or
   `14-ai-development/`. If only `COMPLETE` is accepted, do **not** silently introduce a
   new value and break the gate: report the constraint and choose the honest option that
   remains legal, stating the ceiling you hit.

### What NOT to do

- Do not retranslate anything.
- Do not edit the six documents themselves. This is a manifest-accuracy task.
- Do not add a new automated drift check. The issue explicitly scopes that out. If you
  believe one is needed, say so in the PR body and stop there.

### Verification

- After your edit, re-run your own measurement and show it now reconciles.
- `python3 scripts/check_bilingual_docs.py` — report what it says. It may need explicit
  refs; it may refuse on a shallow clone. Report the literal message rather than claiming
  a pass.
- `python3 scripts/check_document_management.py --require-changed origin/main` — note this
  script exits **2 by design** on this repository (INCOMPLETE: unclassified documents
  exist). Report the code and the summary line; do not "fix" it.
- `python3 scripts/ci/check_line_endings.py`.
- `python3 scripts/ci/check_repository_hygiene.py --base <sha> --head <sha>`.
- Note `14-ai-development/work-items/` is in `PAIR_EXEMPT_PREFIXES`, and
  `BILINGUAL-MANIFEST: COMPLETE` is detected by a plain substring test on the PR body,
  not by position. Determine empirically whether your own PR needs that line.

### Passing the gate on your own PR

`Session Evidence`, `Session Evidence self-test (base)` and
`Session Evidence self-test (head)` are **required** status contexts on `main`. Follow
the merged precedent of PR #1013: add a non-empty session-evidence document, cite it as
`Session evidence reference(s): <path>`, alongside `Related issue(s): #955` and
`AI-assisted work: YES`.

**Known blocker, do not work around it dishonestly:** the `Session Evidence` verdict has
an ordering defect (issue #1026) blocking PRs whose linked Issues all predate
2026-12-01; #955 qualifies. Do **not** force the declaration to `NO`. If the only
remaining red is #1026, say so explicitly.

### Deliverable

Commit, push a branch, open a **ready** (not draft) PR against `main`. Report the PR
number and head SHA, the exact manifest diff, the six-row registered-vs-current table,
the per-pair line deltas, the verdict chosen per pair and what was compared to justify
it, whether any gate constrains `bilingual_status` to an enum, every gate read and its
conclusion, and anything that could not be verified.

Never claim a check is green without reading its conclusion.
