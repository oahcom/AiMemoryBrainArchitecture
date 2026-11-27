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
      evidence_reference:
        - "AID-2026-241/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every figure in this prompt was measured at main 8d90843a before the prompt was written, and the two discriminating cases were executed rather than reasoned about. The prompt is the executed input; its digest is pinned in the manifest, so an amendment belongs in a separate artifact rather than in these bytes."
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
    canonical_scope_keywords:
      - "independent-review"
      - "session-identity"
      - "governance-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-241 — the independent-review gate must test the session, not the account

## Context you are given, already measured at `9ee89b32` (main)

`scripts/governance/status_migration/check_status_gates.py:275-277` enforces the
`independent_review` gate like this:

```python
aliases = _normalized_aliases(data.get("review_identity_aliases", {}))
if _identity(evidence["reviewer"], aliases) == _identity(evidence["implementer"], aliases):
    raise ValueError("REVIEWED reviewer and implementer must be different identities")
```

`_identity()` (line 228) NFKC-normalizes, casefolds, strips `github.com/` and a leading `@`,
and removes everything outside `[a-z0-9]`. So the test compares two strings that name a GitHub
account.

`14-ai-development/PR-GOVERNANCE-001.md:136-138` (both languages) says independence is a
property of the reviewing **session**, that two separate sessions may share one GitHub
identity, and that a single session adopting two roles is not independent. That wording is the
2026-11-24 amendment recorded in
`14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md`,
which replaced the earlier text that said the opposite. The clause was amended; this executable
was not.

Measured behaviour, both cases at `subject_head = 9ee89b32`, evidence bound to real blobs:

- two sessions sharing one identity string -> `FAIL: REVIEWED reviewer and implementer must be
  different identities` (this is the case section 5 declares lawful)
- one session writing two different identity strings -> `PASS` (this is the case section 5
  forbids)

The checker is not referenced by any workflow: `grep -rn check_status_gates .github/workflows/
scripts/ci/` returns nothing. It is reachable only by hand.

## What to change

1. **Add two session fields to the `independent_review` evidence contract.** In
   `EVIDENCE_FIELDS["independent_review"]`, add `reviewer_session` and `implementer_session`.
   Both are required, both are non-empty strings, and both are subject to the existing
   `_meaningful()` check.

2. **Replace the independence test with a session comparison.** The gate fails only when
   `reviewer_session` and `implementer_session` normalize to the same value. Use the same
   normalization family that already exists, but write a *separate* helper -- do not reuse
   `_identity()`, because that function's name asserts account identity and reusing it would
   make the code read as an account test. Name the new one for what it does
   (`_session_token`), and name the comparison for what it decides.

3. **Keep the identity comparison, demoted to a diagnostic.** Do not delete `reviewer`,
   `implementer`, `_identity()` or `review_identity_aliases`. When the two identity strings
   collapse to one account, that is the expected case and must not fail. Keep it reachable so
   that an auditor can still see which account carried which session. Whether to surface it in
   the output is your call; if you do, it must not change pass/fail for a same-account pair.

4. **Say what the field cannot prove -- in the code, not only in the report.** A session string
   is chosen by whoever writes the manifest. Nothing in this repository can prove that two
   strings name two contexts. Put that limit in a comment where the comparison is made, in the
   register's own voice: the check verifies that the manifest *declares* two sessions, not that
   two sessions existed. Do not write a comment that implies verification you do not perform.

## Tests you must add

Add to `scripts/governance/status_migration/test_status_migration.py` -- the module that
already exercises this checker -- one test per case, using the existing fixture style:

- same identity, two different sessions -> PASS
- different identities, one shared session -> FAIL, and the message must name the session fields
- both same -> FAIL
- either session field missing -> FAIL, and the message must name the missing field

Run: `cd scripts/governance/status_migration && python3 -m unittest test_status_migration`

## What not to touch

- Do not change `status`, `lifecycle`, `subject_head` or any other gate's contract.
- Do not add a required status context, and do not modify branch protection.
- Do not "fix" the 55 corpus failures this checker reports. 53 of them are
  `status is not an exact canonical state` / `missing/invalid lifecycle` and belong to #1154.
  This work item changes one criterion inside one arm; it does not migrate the corpus.
- Do not wire it into a workflow. Wiring is a separate decision with a separate blast radius: a
  check that fails 55 of 57 manifests cannot be added to a required context, and adding it as
  non-required would produce a permanently red job that teaches readers to ignore it.
- Do not edit anything under `scripts/governance/session_evidence/`, or
  `14-ai-development/PR-GOVERNANCE-001.md`. The clause is correct; the executable is not.

## Done means

The four tests pass, the existing suite still passes, and this command shows the two
discriminating cases behaving as section 5 requires:

```
python3 scripts/governance/status_migration/check_status_gates.py <case-a.yaml> <case-b.yaml>
  case-a (two sessions, one identity)  -> PASS
  case-b (one session, two identities) -> FAIL
```

Report the exact command output, the test count before and after, and the commit SHA. If a case
behaves differently from this description, report the discrepancy rather than adjusting the
test to match the code.
