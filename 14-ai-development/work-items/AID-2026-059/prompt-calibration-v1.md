---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Executed prompt record - AID-2026-059 calibration session

PROVENANCE: NOT_VERIFIED. This file holds the dispatch text issued to the
implementing agent for the calibration run that Issue #799 criterion 14 asks
for. The manifest pins the SHA-256 of these bytes; nothing here was verified
against a byte-exact model input, because the dispatch crossed a chat channel
rather than a captured request body.

Calibration fixture, not a work product. The files it produces exist to make
the session-evidence gate print `PRESENT` once on a non-production pull
request. They are not a delivery of AID-2026-059 and must not be merged for
their content.

## Dispatch (verbatim)

```text
Build a calibration pull request in a fresh worktree. This is the last unmet
acceptance criterion of Issue #799 and it is a *measurement*, not a feature.

SETUP
  cd /tmp/opencode/amb
  git fetch https://x-access-token:$(cat /tmp/opencode/.ghtok)@github.com/oahcom/AiMemoryBrainArchitecture.git main
  git worktree add /tmp/opencode/wcalib -b test/799-calibration-present FETCH_HEAD
Then work only in /tmp/opencode/wcalib. Do NOT push (I will). Do NOT call the
GitHub API. Use only local git and python3.

WHY THIS EXISTS
Issue #799 acceptance criterion 14: verify the full flow on a real or
purpose-built non-production PR and keep the exact-head CI result. Measured:
14 real pull requests have run the gate; the four green ones all printed
NOT_APPLICABLE; PRESENT has never been printed. NOT_APPLICABLE is correct for a
historical Issue but it does not prove the evidence path works end to end.

The exemption is decided on the linked Issue: _historical_not_applicable
returns True only when every linked Issue is historical AND its declaration is
absent. An Issue carrying a declaration therefore forces full validation
regardless of its creation date.

Issue #1034 is the purpose-built fixture: it declares AI-assisted work: YES and
Session evidence reference(s) pointing at
14-ai-development/work-items/AID-2026-059/session-evidence-calibration-001.md.

WHAT TO CREATE - exactly two files, plus the manifest edit.

1. session-evidence-calibration-001.md - the evidence record the gate will
   validate against _validate_evidence_document and _parse_evidence_region:
   a Session role heading, a # Actual AI input section carrying the real input
   (a Summary: body is rejected), an # AI-visible output section carrying what
   the model actually produced, and document_metadata front matter copied in
   shape from session-evidence-799.md with Draft/Unverified values.

2. One appended entry in manifest.yaml's existing session_evidence: list -
   role CALIBRATION, issue_refs #1034, implementing_ai_session
   session-799-calibration, snapshot file prompt-calibration-v1.md, its real
   SHA-256 and byte count, provenance NOT_VERIFIED, session status
   NOT_RECORDED, and session_evidence_ref pointing at the record. The
   session_evidence: block must stay the last top-level key.

3. prompt-calibration-v1.md - the dispatched prompt snapshot, whose bytes are
   the ones the manifest pins.

VERIFY
  parse the manifest with the merged parser and show both entries
  recompute the snapshot SHA-256 and byte count
  run _validate_evidence_document on the record
  run the session-evidence unittest suite
  run check_test_reachability, check_line_endings and check_repository_hygiene
  run gate_ratchet over the bilingual-docs baseline
  run check_document_management --require-changed against main
  report whether the new files need a bilingual pair, and confirm the
  work-items/ pair-exempt prefix rather than assuming it

Commit message: test(session-evidence): add the calibration fixture that lets
the gate print PRESENT. Non-production by construction; the pull request that
cites this must not be merged for its content.
```
