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

Calibration fixture, not a work product. Nothing here records work on
AID-2026-059; the record exists so the session-evidence gate can be observed
printing `PRESENT` once on a non-production pull request. The pull request that
cites it must not be merged for its content.

# Session role / use case

CALIBRATION. A purpose-built non-production session, not a delivery of
AID-2026-059. Issue #799 acceptance criterion 14 asks for the whole gate to be
observed on a real or purpose-built non-production pull request with the
exact-head result kept. Fourteen real pull requests have run it and every
green verdict was `NOT_APPLICABLE`, because each linked only a pre-policy Issue
carrying no declaration. That verdict is correct and also blind: the evidence
path -- manifest entry, evidence record, prompt digest, Issue attribution --
has never been exercised on a live run. This session forces it by attributing
a manifest entry to Issue #1034, which declares AI-assisted work and so defeats
the historical exemption in `_historical_not_applicable`.

# Actual AI input

The input was one dispatch message handed to the implementing agent in the
calibration worktree, plus the merged validator the message told it to read
before writing anything. The dispatch is reproduced in full, because the gate
reads this file and a pointer to another file would let the record claim an
input it does not carry. The same text is pinned as
`prompt-calibration-v1.md` and hashed into the manifest entry
(`sha256:dc79a1d7fd2eaf8e1b00eca724d3e6e3e0b5ba73367202cb38877cca8cea7dd7`,
`bytes:4996`).

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

The files the agent read before writing, because the dispatch forbade guessing
at their contract: `scripts/governance/session_evidence/validate.py` --
`_validate_evidence_document` (role heading regex, two mandatory regions),
`_parse_evidence_region` (a region ends at the next Markdown heading, and a
`Summary:` first line is rejected as a substitute for the input or output),
`parse_manifest_session_entries` (fields scanned as
`^\s{4}([a-z0-9_]+)\s*:` over the whole file, hence the requirement that
`session_evidence:` be the last top-level key), `_validate_manifest_entry`
(enum membership for provenance and session status, 64-hex digest),
`check_09_manifest_and_evidence_entries` (Issue attribution plus the OD-A2
two-way mapping), `check_11_prompt_snapshot_hashes` (digest and byte count
compared against the blob the PR head tree resolves), and
`_historical_not_applicable` (the exemption this fixture defeats). Also
`14-ai-development/work-items/AID-2026-059/session-evidence-799.md` for the
front-matter shape and `prompt-v1.md` for the snapshot convention.

# AI-visible output

Two files are new and one was edited in place, all in
`14-ai-development/work-items/AID-2026-059/`.

`prompt-calibration-v1.md` is new: the dispatch text above behind the same
`document_metadata` block the sibling prompt record carries, written as UTF-8
with LF endings. Its raw bytes hash to
`dc79a1d7fd2eaf8e1b00eca724d3e6e3e0b5ba73367202cb38877cca8cea7dd7` and measure
4996 bytes.

`manifest.yaml` gained a second entry under the existing `session_evidence:`
list, appended after the IMPLEMENTER entry; it stays the last top-level key:

```
  - role: CALIBRATION
    issue_refs:
      - "https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1034"
    implementing_ai_session: session-799-calibration
    executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-059/prompt-calibration-v1.md
    executed_prompt_sha256: dc79a1d7fd2eaf8e1b00eca724d3e6e3e0b5ba73367202cb38877cca8cea7dd7
    executed_prompt_bytes: 4996
    executed_prompt_provenance: NOT_VERIFIED
    session_reference_status: NOT_RECORDED
    session_evidence_ref: 14-ai-development/work-items/AID-2026-059/session-evidence-calibration-001.md
```

This file, `session-evidence-calibration-001.md`, is the third. Its only
consumer is the gate; it is not listed in the manifest's `scope:` section
because it is not part of the delivery AID-2026-059 describes.

The measurements the dispatch asked for, run on this branch after the commit,
are recorded in the pull request body rather than restated here, because a
passed gate printed into the file that the gate reads would make the file
assert a result instead of recording one.
