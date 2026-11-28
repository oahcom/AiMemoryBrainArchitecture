---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-349/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Figures in this record were produced by operator-run commands on 2026-11-28; no independent reproduction is claimed."
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
    canonical_scope: "Record for AID-2026-349; this record does not establish normative requirements or acceptance."
    canonical_scope_id: "ai-development/aid-2026-349-record"
    canonical_scope_keywords:
      - "AID-2026-349"
      - "dangling reference"
      - "memory-runtime"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-349 — Evidence

## E1 — the referenced file does not exist

```
git ls-tree -r --name-only origin/main | Select-String phase-3.5-forget-suppression
(no output)
```

## E2 — two canonical documents still linked it as if it existed

`05-memory-runtime/retrieval-engine.md:149`:

```
The detailed owner/consumer contract is in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This supplement supersedes any earlier provisional wording in this file where the two differ.
```

`05-memory-runtime/working-set-and-cache.md:144`:

```
The detailed contract and conformance cases are in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This addendum supersedes earlier provisional wording where inconsistent.
```

## E3 — the four mirrors carried the same claim without a disclosure

`docs/en/05-memory-runtime/retrieval-engine.md` and `.../working-set-and-cache.md` already
linked `../../governance/documentation-gaps.md`, but neither said the contract file is
unsubmitted and not restored. Both `docs/zh-CN` copies were in the same state.

## E4 — the accepted disclosure pattern already exists

`05-memory-runtime/runtime-overview.md` was corrected in AID-2026-340 with exactly this
sentence shape: retarget the title link at `documentation-gaps.md`, then state that the file is
unsubmitted and not restored, with a second link to the same gap register. This work item
applies that already-accepted pattern to the two sibling documents.

## E5 — gate results

```
check_bilingual_docs.py                                     PASS (6 changed paths inspected)
check_document_management.py --require-changed origin/main  PASS (incremental): no GOV-DOC-002 violations; 907 classified, 366 unclassified
git diff --numstat                                          1 1 per file, six files
```

## E6 — what is not claimed

No CI run, review verdict or acceptance decision is claimed. The contract file is not restored.
