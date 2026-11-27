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
        - "14-ai-development/work-items/AID-2026-302/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Session record; the platform does not expose a verifiable session identifier, and the prompt snapshot is a structured transcription."
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
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Session provenance for AID-2026-302"
    canonical_scope_id: "ai-development/aid-2026-302-session"
    canonical_scope_keywords:
      - "aid-2026-302"
      - "session"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Session evidence — AID-2026-302

## Role

`IMPLEMENTATION_SESSION`: data repair of 93 declared pin fields, plus the
blob-pin gate change, for Issue #1350, on a delegated task.

- Implementing session: an `opencode` 2.4 subagent session, model route
  `9router_hermes`. The platform exposes no stable session identifier, so
  `session_reference_status: RECORDED` refers to **this file**, not to a
  platform id.
- Prompt: the three dispatch turns are preserved in `prompt-v1.md` (9114
  bytes, SHA-256 `5771c25c5dbc299bd6ed7cc4ffe0a05dd810a820929d35daca39a62f9d03318a`).
  The snapshot is a structured transcription of the task text, so
  `executed_prompt_provenance: NOT_VERIFIED`.
- Environment: Windows host, PowerShell 5.1, Windows `git`, `python` 3.x.
  No WSL, no `bash -lc`, no distribution `python3`/`git`; the two workflow
  commands that are written for the Linux runner were run locally as their
  Windows equivalents (`python` for `python3`, no `sed`/`sh` pipeline).

## What the session did

1. Enumerated the declared `session_evidence` digests and byte counts across
   all 132 manifests, computing each against `git cat-file blob` at
   `cb5b3dcd23ff86e10a354bb27b668dce19e95f62`. Result: 40 entries whose
   digest **and** byte count disagreed, all by exactly 58 bytes, plus the
   `AID-2026-261` entry whose path does not exist.
2. Rewrote the 40 pairs as atomic pairs in one commit, preserving the file's
   existing quoting and line endings, and asserted the exact pre-image and a
   count of 40 before writing.
3. Repinned three `authored_indexes[0]` blobs and three
   `related_evidence[0]` blobs to the candidate tree; retired the three
   `authored_indexes[1]` blob claims under that entry's own
   `SUPERSEDED_BY_MAIN` text.
4. Retired the `AID-2026-261` all-zero sentinel pair, re-anchored the
   `AID-2026-100` `gate_a_reconstruction[0]` note to `d28ebe21`, and left
   `AID-2026-170` `owner_ruling.current_blob` unchanged and `BLOCKED`.
5. Replaced the blob-pin ratchet step with a direct checker invocation and
   deleted its baseline file.
6. Ran the checker before and after, ran a negative control on a temporary
   branch (one flipped digest nibble → exit 1; restored → exit 0), then
   rebased onto the current `origin/main` and re-ran the full tree.

## What this session does not claim

- No natural-person Owner acceptance, independent review or Issue closure.
- No merge, no required-context result, and no exact-head CI run is claimed
  from inside the session; those are recorded from the pull request.
- No check that the 93 declarations are *semantically* the right ones beyond
  the scope rules in `evidence.md` §1; where the scope could not be fixed, the
  declaration is `BLOCKED` rather than guessed.
