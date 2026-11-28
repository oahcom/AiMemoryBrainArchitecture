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

# AID-2026-347 — Evidence

Base commit for every measurement below: `origin/main` `f0843a8f38a420883921cfda96b515204967f885`.

## E1 — check_traceability.py counted a commented-out INDEX row

Pre-fix (`scripts/check_traceability.py` at `f0843a8f`), with the `AID-2026-340` row of
`14-ai-development/work-items/INDEX.md` wrapped in `<!-- ... -->`:

```
PASS TRACEABILITY: 0 requirements / 166 work items / 0 errors / 131 warnings
```

Post-fix, same fixture:

```
FAIL TRACEABILITY: 0 requirements / 166 work items / 1 errors / 131 warnings
001. 14-ai-development/work-items/AID-2026-340/manifest.yaml -> ERROR T-04 manifest ... exists on disk but is not indexed
```

Unmodified `INDEX.md` gives `PASS ... 0 errors` in both states, so the fixture is the only
difference.

## E2 — check_bilingual_docs.py accepted a newly added normative-looking file in an excluded root

A file `reviews/fixture-new-normative.md` declaring "This document declares normative
requirements for all owners" was committed on top of `f0843a8f`, with
`BASE_SHA=origin/main HEAD_SHA=HEAD PR_BODY="BILINGUAL-MANIFEST: COMPLETE"`.

Pre-fix:

```
NOTE: 1 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
Bilingual documentation and prompt-library gate: PASS (1 changed paths inspected).
```

Post-fix:

```
::error::reviews/fixture-new-normative.md: new Markdown file is outside NORMATIVE_ROOTS; move it into a governed root, or register it as governed/excluded with a justification.
Bilingual documentation gate: FAIL
```

## E3 — the modified-file path still degrades to a NOTE

Same command, but the changed path is a modification of an already committed `reviews/`
Markdown file:

```
NOTE: 1 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
Bilingual documentation and prompt-library gate: PASS (1 changed paths inspected).
```

exit 0.

## E4 — test results

```
python scripts/test_check_traceability_sanitize.py       Ran 6 tests  OK
python scripts/test_check_bilingual_docs_outside_root.py Ran 7 tests  OK
python scripts/test_check_traceability.py                Ran 41 tests OK
python scripts/test_check_bilingual_docs.py              Ran 27 tests OK
```

## E5 — what is not claimed

- No CI run, review verdict, or acceptance decision is claimed.
- The fixture commits used for E1–E3 were discarded with `git reset --hard` and are not part
  of the pull request.
- The behaviour of `scripts/ci/check_repository_hygiene.py` was read, not modified.
