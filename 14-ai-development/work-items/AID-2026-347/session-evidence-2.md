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
        - "14-ai-development/work-items/AID-2026-347/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Figures in this record were produced by operator-run commands on 2026-11-28 against origin/main f0843a8f; no independent reproduction is claimed."
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
    canonical_scope: "Measurement record for AID-2026-347; this record does not establish normative requirements or acceptance."
    canonical_scope_id: "ai-development/aid-2026-347-evidence"
    canonical_scope_keywords:
      - "AID-2026-347"
      - "traceability"
      - "bilingual gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-347 — Session evidence (segment 2: outside-root additions)

## Session role / use case

**Session role:** IMPLEMENTER.

**Use case:** Stop `scripts/check_bilingual_docs.py` from downgrading newly added Markdown
outside `NORMATIVE_ROOTS` to a non-blocking NOTE.

## Session identification

- Work item: `AID-2026-347`.
- Tracking issue: `#1540`.
- Repository: `oahcom/AiMemoryBrainArchitecture`.
- Branch: `fix/2026-11-28-aid347-gate-comment-and-outside-root`.
- Implementing AI session identifier: `6b0a5e8d-06f8-83ec-a73e-de6917ca18fd`.
- Session role: `IMPLEMENTER`.

## Executed prompt snapshot

- Recorded snapshot destination: `14-ai-development/work-items/AID-2026-347/prompt-v2.md`.
- Recorded byte count and SHA-256 are pinned in `manifest.yaml`.
- Executed prompt provenance: `NOT_VERIFIED`.
- Session reference status: `RECORDED`.

An initial brief preceded this snapshot; its first answer nested the helper functions inside
`main()` and called `sys.exit(1)` directly. That answer was not applied. The recorded
snapshot is the corrective follow-up.

## Execution scope

1. `scripts/check_bilingual_docs.py`: two new module-level functions and one changed block in `main()`.
2. `scripts/test_check_bilingual_docs_outside_root.py`: new file, seven tests.

## Execution constraints

- Helpers must be module-level, placed after `NORMATIVE_ROOTS` and before `main()`.
- Errors must be appended to the existing `errors` list so the existing exit-code path decides the verdict.
- Error text must be English, name the path, and give both ways out.
- `NORMATIVE_ROOTS` contents and `check_document_management.py` must not change.
- No new environment-variable switch.

## Actual AI input

The requester supplied:

- The measured fixture matrix showing that `reviews/` is the only placement that gets both
  gates green for a newly added normative-looking Markdown file.
- The existing `skipped = [...]` block verbatim, and the fact that `changed_status()` already
  returns per-path status.
- The instruction to distinguish added from modified/deleted rather than to block all
  outside-root Markdown.

## AI-visible output

The authoring session returned:

1. One `INSERT_AFTER` block adding `outside_root_markdown_paths()` and `outside_root_additions()` after the `NORMATIVE_ROOTS` literal.
2. One `REPLACE` block turning the skipped computation into an error loop for additions plus the unchanged NOTE for the rest.
3. One `CREATE` block with the full seven-test file.

The operator applied the three blocks. `apply_blocks.py` was extended to accept
`|INSERT_AFTER` as a `REPLACE` alias because the emitted block already carried the full anchor
text.

## Verification and status

Operator-run results, not independently reproduced:

- `scripts/test_check_bilingual_docs_outside_root.py`: 7 tests, OK.
- `scripts/test_check_bilingual_docs.py`: 27 tests, OK.
- Fixture measurements E2 and E3 in `evidence.md`.

Recorded status: pull request PENDING, CI NOT_CLAIMED, review NOT_ASSIGNED, acceptance
NOT_ASSIGNED, prompt provenance NOT_VERIFIED.
