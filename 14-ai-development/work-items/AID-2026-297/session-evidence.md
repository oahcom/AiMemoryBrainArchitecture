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
        - "14-ai-development/work-items/AID-2026-297/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This record describes the supplied task constraints and authored evidence artifacts. Session identity and prompt provenance are not independently corroborated."
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
    canonical_scope: "Session role, actual input and AI-visible output for AID-2026-297."
    canonical_scope_id: "ai-development/aid-2026-297-session-provenance"
    canonical_scope_keywords:
      - "AID-2026-297"
      - "MIGRATION-POLICY"
      - "session evidence"
      - "provenance"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session evidence — AID-2026-297

## Session identity

```yaml
role: IMPLEMENTER
issue_refs:
  - "#1464"
implementing_ai_session: MIGRATION-POLICY
executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-297/prompt-v1.md
executed_prompt_sha256: __EXECUTED_PROMPT_SHA256__
executed_prompt_bytes: __EXECUTED_PROMPT_BYTES__
executed_prompt_provenance: NOT_VERIFIED
session_reference_status: RECORDED
session_evidence_ref: session-evidence.md
```

`implementing_ai_session` is recorded as the single value `MIGRATION-POLICY`. It is not a concatenation of multiple session identifiers.

The session token is a recording identifier. Its relationship to an independently attested execution environment has not been established.

The prompt snapshot is to be supplied by the delivery operator. Its digest and byte count must be calculated from the finalized file bytes. This record does not assert that the snapshot is an authenticated byte-for-byte copy of the original prompt transmission.

## Session role / use case

This session acted as the implementation-artifact authoring session for AID-2026-297.

Its assigned task was to prepare the work-item manifest and evidence records for the migration-policy work delivered in PR #1513, while preserving the supplied implementation facts and validation results.

The work-item scope covers:

1. The registry migration policy and its Chinese counterpart.
2. The inventory rules and their Chinese counterpart.
3. The migration inventory input.
4. The adjudication schema.
5. The read-only migration tool.
6. The migration dry-run evidence.
7. The work-item manifest, prompt reference and session evidence.
8. The proposed INDEX registration.

The session does not claim independent review of its own output.

## Actual AI input

The user supplied these task facts and constraints:

- Work item ID: `AID-2026-297`.
- Work-item title: 修复工作项 registry 迁移政策、adjudication schema 与库存规则，并做只读 dry-run.
- Tracking issue: `#1464`.
- Base branch: `main`.
- Base commit: `cc5d22b9126e00e3f93ffe71282554309908bc89`.
- PR: `#1513`.
- The PR body declares `Work Item ID: AID-2026-297`; the Session Evidence check failed because the manifest path was absent from the PR head Git tree.
- The manifest must conform to `work-item-manifest.schema.yaml` and the session-evidence structure.
- `session_evidence[].implementing_ai_session` must be the single value `MIGRATION-POLICY`.
- `session_evidence[].issue_refs` must reference Issue `#1464`, not a PR number.
- `session_evidence[].session_evidence_ref` must be the filename `session-evidence.md`.
- The session evidence document must contain non-empty sections titled `Session role / use case`, `Actual AI input` and `AI-visible output`.
- Every `documentation[].path` must exist in the submitted Git tree.
- The executed prompt digest and byte count must remain `__EXECUTED_PROMPT_SHA256__` and `__EXECUTED_PROMPT_BYTES__` until the delivery operator replaces them using the finalized prompt file bytes.
- `prompt-v1.md` is to be authored and placed by the delivery operator; this session does not output that file.

The user supplied the following validation results:

1. Migration dry run:

   ```text
   python tools/migrate_work_item_registry.py --source-tree efbdebfa --inventory 00-governance/registry-migration/inventory.yaml --output 00-governance/registry --dry-run --report json
   ```

   Exit code `0`; `items=140`; `field_cells=1680`; `prompt_sha256 pass=8 / fail=69`; `schema=NOT_PRESENT/DEFERRED`.

2. Repository tests:

   ```text
   python -m pytest tests -q
   ```

   Result: `144 passed, 34 subtests passed`.

3. Bilingual document check:

   ```text
   python scripts/check_bilingual_docs.py
   ```

   Result: `PASS`.

4. Document-management check:

   ```text
   python scripts/check_document_management.py --require-changed origin/main
   ```

   Result: `PASS`.

5. Work-item manifest schema check:

   ```text
   python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json
   ```

   The command was supplied as executed, but no output or exit code was provided in the task facts.

## AI-visible output

This session authored the following work-item records for AID-2026-297:

1. `14-ai-development/work-items/AID-2026-297/manifest.yaml`
2. `14-ai-development/work-items/AID-2026-297/evidence.md`
3. `14-ai-development/work-items/AID-2026-297/session-evidence.md`
4. A proposed registration row for `14-ai-development/work-items/INDEX.md`

The session records the implementation artifacts already identified in PR #1513:

- `00-governance/registry-migration/policy.md`
- `00-governance/registry-migration/policy.zh-CN.md`
- `00-governance/registry-migration/inventory.rules.md`
- `00-governance/registry-migration/inventory.rules.zh-CN.md`
- `00-governance/registry-migration/inventory.yaml`
- `00-governance/registry-adjudications/schema.json`
- `tools/migrate_work_item_registry.py`

The evidence record preserves the reported test and dry-run outcomes without upgrading unreported results to PASS.

The session explicitly records that:

- The dry run did not write `00-governance/registry/`.
- No existing manifest was rewritten.
- No PR was merged.
- Independent review was not performed.
- Owner acceptance was not recorded.
- Prompt provenance remains unverified pending the delivery operator's byte-level calculation.
