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
        - "14-ai-development/work-items/AID-2026-280/manifest.yaml"
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Source blobs and API response bodies read from main with cache-busting query parameters; branch-protection read denied (403)."
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
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "req-04"
      - "ac8"
      - "evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-280 evidence

## Pinned repository state and source readback

The user-supplied expected main was `6f597e2dd8b6e879bf7539aa16b88a39504d9c49`. A cache-busted GitHub API read of `refs/heads/main` returned **`756e1e25d735f526254fc3241b47880fef527b24`**, whose commit message is “Merge pull request #1392 ... AID-2026-268” at 2026-11-27T04:56:39Z. All new work is based on the fetched current main, not the earlier supplied SHA.

The following current-main blobs were fetched:
- `14-ai-development/work-items/INDEX.md` — `38dd20dc6acd2bcd676e6bd029405e29c82e80ca`
- `14-ai-development/work-items/AID-2026-260/scope-confirmation.md` — `e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a`
- `14-ai-development/work-items/AID-2026-254/manifest.yaml` — `5aa538b4c91d58e3051fecaa34591a6ce43fc09c`
- `14-ai-development/work-items/AID-2026-254/evidence.md` — `02567b538a87e52361a78cb3eaea1fe00d79cee9`

AID-2026-280 absence was checked by cache-busted Contents API reads:
- `GET .../contents/14-ai-development/work-items/AID-2026-280?ref=main&_=...` → HTTP 404
- `GET .../contents/14-ai-development/work-items/AID-2026-280/manifest.yaml?ref=main&_=...` → HTTP 404

## Independently verified F1–F4

- F1: Issue #265 body returns AC8 as unchecked and ABSENT, with `carrier: NO_CARRIER_FOUND`. The body also explicitly says the two authorized exits are a work-item carrier or writing the exclusion into the Issue itself.
- F2: Issue #265 body returns AC1 as unchecked OWNER_ACTION with `NO_CARRIER_FOUND`.
- F3: comment #7193586920 fetched from the Issues Comments API. It records AC8 ABSENT and explicitly describes the two exits; no Owner choice was made in that comment.
- F4: AID-260 scope-confirmation.md line 69 contains the explicit AC8 EXCLUDED paragraph. Blob: `e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a`. The reconciliation section begins line 76 in the same blob.

## Further authority check

Issue #305 was fetched directly. Its body states that ministerial transcription cannot be promoted into an operative delegation instrument; a session may not appoint itself or another session, nor treat transcription as delegation. AID-260's own metadata says approval Draft, verification Unverified, and the document calls itself a proxy determination, not a natural-person Owner signature. This defeats any claim that the AID-260 proxy record alone is a valid constitutive AC1 scope act.

## F5 timeline source and chosen clock

The timeline values in decision.md are the supplied upstream event times, corroborated by fetched Issue #265, comment #7193586920 and comment #7209840981, and the merged commit references. The selected effective-time criterion is canonical merge/publication to main. The AID-260 authoring time 03:41:45Z precedes the AID-254 merge, but the EXIT-2 carrier did not become canonical on main until 04:08:07Z, after PR #1370 merged at 03:57:44Z. Therefore the published EXIT-2 text is post-hoc relative to the measurement carrier's mainline merge. Its authority is separately insufficient under Issue #305.

## F6 and Q4 measurement analysis

AID-2026-254 evidence lines 56 and 61 describe the metric as declared root/domain fan-out and explicitly disclaim elapsed time, cognitive load and observed human session count. The evidence lines 107 onward say a machine-readable session-switch ledger does not exist and propose recording handoffs in future session evidence. Its current thresholds (≤3 roots, 4–5 soft overrun, >5 hard stop) are a work-scope fan-out budget derived from a 2.90-root cohort mean; they are not thresholds for measured human attention or context-switching cost.

No local shell command or script was executed. All repository reads and mutations in this session used GitHub API/connector operations.

## Branch protection and merge gate

A cache-busted GET to `/branches/main/protection` returned HTTP 403 “Resource not accessible by integration”. A GET to `/rulesets` returned an empty array. This session therefore cannot independently verify `strict=true` or `enforce_admins=true`; no claim is made that those settings were verified. The current main check-runs read returned 11 check runs, not the 16 required contexts, and the legacy commit status was pending with zero statuses. This evidence is not a substitute for the PR-head required-context result.

## Issue body integrity

No Issue #265 body PATCH was made. Therefore there is no before/after body SHA-256 pair to report. The canonical body remains the fetched body with AC1 [ ] OWNER_ACTION and AC8 [ ] ABSENT. The proposed corrected lines in decision.md are not yet applied. The one Issue comment (if posted) will explicitly say it is not a body edit.

## Post-merge file verification

Not applicable unless a PR is merged. No merge is claimed in this evidence file. Post-merge blob SHAs must be appended only after a real merge and fresh API readback.
