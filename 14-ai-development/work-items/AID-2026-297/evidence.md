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
        - "14-ai-development/work-items/AID-2026-297/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This record transcribes execution results supplied for PR #1513; the commands and resulting repository state have not been independently re-executed for this record."
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
    canonical_scope: "Execution results and bounded evidence for AID-2026-297."
    canonical_scope_id: "ai-development/aid-2026-297-implementation-evidence"
    canonical_scope_keywords:
      - "AID-2026-297"
      - "registry migration"
      - "dry run"
      - "validation"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-297

## Evidence scope

This document records the implementation and validation results supplied for PR #1513 and the explicit boundaries of what those results establish. It does not assert that the PR has been merged, that registry migration has been performed, or that independent review or Owner acceptance has occurred.

## Implementation artifacts

The PR delivery set comprises:

1. `00-governance/registry-migration/policy.md`
2. `00-governance/registry-migration/policy.zh-CN.md`
3. `00-governance/registry-migration/inventory.rules.md`
4. `00-governance/registry-migration/inventory.rules.zh-CN.md`
5. `00-governance/registry-migration/inventory.yaml`
6. `00-governance/registry-adjudications/schema.json`
7. `tools/migrate_work_item_registry.py`
8. `14-ai-development/work-items/AID-2026-297/manifest.yaml`
9. `14-ai-development/work-items/AID-2026-297/prompt-v1.md`
10. `14-ai-development/work-items/AID-2026-297/evidence.md`
11. `14-ai-development/work-items/AID-2026-297/session-evidence.md`
12. `14-ai-development/work-items/INDEX.md`

## Validation results

The following command results were supplied as completed local executions.

### Migration dry run

Command:

```text
python tools/migrate_work_item_registry.py --source-tree efbdebfa --inventory 00-governance/registry-migration/inventory.yaml --output 00-governance/registry --dry-run --report json
```

Recorded result:

- Exit code: `0`
- Items: `140`
- Field cells: `1680`
- `prompt_sha256`: 8 passes and 69 failures
- Schema: `NOT_PRESENT/DEFERRED`

The dry run did not write to `00-governance/registry/`. No existing manifest was rewritten.

The prompt digest result is recorded as reported. The 69 failures are not represented as successful prompt-pin verification.

### Repository tests

Command:

```text
python -m pytest tests -q
```

Recorded result:

- `144 passed`
- `34 subtests passed`

### Bilingual document validation

Command:

```text
python scripts/check_bilingual_docs.py
```

Recorded result: `PASS`.

### Document-management validation

Command:

```text
python scripts/check_document_management.py --require-changed origin/main
```

Recorded result: `PASS`.

### Work-item manifest schema validation

Command:

```text
python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json
```

The command is recorded as executed. No exit code or output was supplied here, so this evidence record does not assign it a PASS result.

## Explicit non-claims and boundaries

- The dry run did not write `00-governance/registry/`.
- No existing work-item manifest was rewritten.
- The migration inventory was used as input; this record does not claim that registry records were created.
- PR #1513 has not been merged.
- Independent review has not been performed.
- Owner acceptance has not been recorded.
- The session does not claim that the executed prompt snapshot is an authenticated byte-for-byte copy of the original prompt transmission.
- The prompt SHA-256 and byte count remain placeholders until the delivery operator calculates them from the finalized `prompt-v1.md` bytes.
