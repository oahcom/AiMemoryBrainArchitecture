---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
---

# Evidence — AID-2026-293

## Scope evidence

- Work item: AID-2026-293
- Related issue: #1464
- Pull request: #1478
- Canonical schema: `00-governance/schemas/work-item-registry.schema.json`
- Canonical source rules: `00-governance/schemas/work-item-registry.source-rules.md`
- Fixture runner: `00-governance/schemas/fixtures/run_fixtures.py`

## Previously reported execution evidence

The following results were supplied from the implementation branch before
the final metadata, bilingual documentation, work-item registration and
version-bump changes.

### Schema fixtures

```text
PASS=11 FAIL=0 TOTAL=11
ALL PASS
```

### Repository hygiene self-test

```text
Ran 107 tests ... OK (skipped=1)
```

### Repository new-file admission

```text
Work-item index membership version=2026-11-27.2 directories=152 linked=152
Work-item manifest consistency version=2026-11-27.2 manifests=141 in_scope=126 excluded_by_record_type=5 unrecognized=10 violations=0
Repository new-file admission version=2026-11-27.2 base=f77b1e63f0aca6b93f14fee5bd5c04510053ee23 head=8a69d6dd05679e3d21c31aadb43a0a48188fc0fa merge_base=f77b1e63f0aca6b93f14fee5bd5c04510053ee23
Repository new-file admission passed: 25 new path(s) checked.
```

Exit code: `0`.

## Interpretation limits

These results establish only the behavior of the commands at the reported
head and version. They do not establish that the final PR head passes after
the following additions or changes:

- `document_metadata` and `bilingual_counterpart` declarations;
- English and Simplified Chinese counterpart files;
- `CHECK_VERSION = "2026-11-28.1"`;
- the new black-box admission tests;
- the AID-2026-293 manifest, prompt snapshot, session evidence and INDEX row.

The three existing version assertions must be updated with the version bump.
The new A4 tests must exercise the checker through its subprocess CLI.

## Final verification still required

Run the following against the final exact PR head:

1. `python 00-governance/schemas/fixtures/run_fixtures.py`
2. `python scripts/test_check_repository_hygiene.py`
3. `python scripts/check_document_management.py --require-changed f77b1e63f0aca6b93f14fee5bd5c04510053ee23`
4. `python scripts/check_bilingual_docs.py`
5. `python scripts/check_traceability.py --index-only`
6. The Session Evidence validation workflow/check.
7. Repository new-file admission using the exact PR base and final head.

Record the exact command, exit code, head SHA and raw output for each result.
Do not describe an unrun check as passed.

## Review and acceptance

- Independent review: `NOT_ASSIGNED`
- Owner acceptance: `NOT_RECORDED`
- Merge state: `NOT_MERGED`