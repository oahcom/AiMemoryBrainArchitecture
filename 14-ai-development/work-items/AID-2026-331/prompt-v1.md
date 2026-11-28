---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-331/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Prompt payload is a replacement placeholder; exact executed payload and digest are not yet recorded."
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
    canonical_scope: "Prompt snapshot for AID-2026-331"
    canonical_scope_id: "ai-development/aid-2026-331-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-331"
      - "prompt"
      - "reference-semantics"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Second Owner ruling arrived. Fold it into the AID-2026-331 set and merge the two records.

The Owner has now ruled on the prompt-snapshot family that the Option C ruling excluded. Verbatim:

```
decision_id: PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001
base: main=b333ad1c
scope:
  - AID-2026-101/session_evidence[0].executed_prompt_snapshot_file
  - AID-2026-102/session_evidence[0].executed_prompt_snapshot_file

1. CHOSEN OPTION: OPTION 1 — POINT-IN-TIME RECORD.

   The declared executed_prompt_sha256 and executed_prompt_bytes identify the exact prompt snapshot bytes executed for that session; they are historical evidence, not standing assertions about the current candidate-tree contents.

2. ACCEPTED CONSEQUENCE:

   A later edit to a prompt snapshot file does not invalidate an earlier session record, provided the declared snapshot can be verified against the commit recorded in that session-evidence entry, or against its unambiguous entry history.

3. DISPOSITION OF THE FOUR CURRENT FAILURES:

   Reclassify all four failures as false positives from applying candidate-tree equality to a point-in-time evidence family. Do not rewrite either session's digest or byte-count declarations merely to match the current files, and do not restore the current prompt-v1.md files solely to satisfy this check.

   Verification must resolve the snapshot bytes at the session's recorded commit. If the entry does not identify a commit sufficiently to resolve those bytes unambiguously, that is a missing historical-provenance defect to report separately; it is not permission to substitute candidate-tree bytes or silently rewrite the declarations.

4. BLOB-PIN CHECKER / AID-2026-333 SCOPE:

   Remove session_evidence[].executed_prompt_snapshot_file digest and byte-count assertions from the blob-pin checker's candidate-tree comparison. The Session Evidence validator remains the authoritative enforcement point for both fields against the PR-head tree blob under check 11.

   Historical verification of what was executed remains a Session Evidence provenance responsibility. The blob-pin checker must not duplicate that validator's current-tree assertion under a different base or report the resulting disagreement as a blob-pin mismatch.

5. IMPLEMENTATION UNBLOCKING:

   This ruling together with the prior Option C ruling is sufficient to define the reference semantics needed by AID-2026-331 and AID-2026-336. No third semantic decision is outstanding for the two ruled families.

   AID-2026-331 must document and migrate both decisions:
   - authored_indexes[]: historical reference;
   - related_evidence[]: explicit per-entry historical/current reference_mode;
   - executed_prompt_snapshot_file: point-in-time session evidence, not a candidate-tree blob-pin assertion.

   AID-2026-336 must implement the corresponding checker behavior and diagnostics, including removal of the duplicate candidate-tree assertion for executed_prompt_snapshot_file. It must not weaken or remove Session Evidence validator check 11.

   Any unresolved question about how an existing session-evidence entry records or identifies its execution commit is a provenance-data assessment within implementation and migration; it does not reopen the chosen point-in-time semantics.

6. NON-ACCEPTANCE / ISSUE STATUS:

   This ruling is not acceptance of AID-2026-255, does not establish that any implementation or migration is complete, and does not close #1350. **#1350 remains open** pending its own acceptance review against the landed implementation, evidence, and applicable gates.
```

## What changes in your Deliverable 2

1. `reference-semantics.md` must cover **three** families, not two: `authored_indexes[]` (historical authorship reference), `related_evidence[]` (explicit per-entry `reference_mode`), and `session_evidence[].executed_prompt_snapshot_file` (point-in-time session evidence, not a candidate-tree blob-pin assertion). For the third family state plainly that the blob-pin checker must stop asserting it and that Session Evidence check 11 remains the enforcing gate.
2. `migration-table.md` must add the two prompt-snapshot records: field, path, declared digest, declared bytes, current digest, current bytes, the disposition `reclassify as point-in-time session evidence; preserve declared digest and byte count; no rewrite`, and the note that the four current failures are false positives from a candidate-tree rule applied to a point-in-time family.
3. The manifest's `scope`, `evidence`, and `implementation.summary` must name both rulings by their decision identity (`Option C` for the two reference families; `PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001` for the snapshot family).
4. AID-2026-336's scope statement must add: remove the duplicate `session_evidence[].executed_prompt_snapshot_file` digest and byte-count assertion from the blob-pin checker, do not weaken check 11, and report the resulting three diagnostics plus the removed-assertion evidence.

## What changes in your Deliverable 1

Produce one combined `#1350` ruling record that carries both rulings, quoting each one's operative sentences, and stating:

- both decisions are recorded and are not acceptance of AID-2026-255;
- #1350 remains open;
- the two `main`-red contexts are outside this lane;
- AID-2026-331 documents and migrates the semantics; AID-2026-336 implements them.

## Also still required

Re-emit, in full and final form, the complete file set for the AID-2026-331 documentation-only PR, since I have not landed any of it yet:

1. `manifest.yaml` (no duplicate keys; `__PROMPT_SHA256__` / `__PROMPT_BYTES__` placeholders)
2. `reference-semantics.md` (now three families)
3. `migration-table.md` (now eleven rows: nine reference declarations plus two prompt-snapshot records)
4. `session-evidence.md`
5. `prompt-v1.md` (single `__PROMPT_PAYLOAD__` line)
6. the exact `INDEX.md` row
7. the PR body, with `## Related issue(s)` then `#1350`, `## AI-assisted work` then a bare `YES`, and a three-column per-Issue table whose header contains `Related Issue`, `Issue AI-assisted work`, `Evidence refs for this Issue`, with row `| #1350 | YES | <session-evidence path> |`

Constraints unchanged: documentation only, no digest rewritten, no checker or validator change, no acceptance language.
