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
      last_verified_date: "2026-11-26"
      last_verification_note: "This is the assignment text as recorded by the orchestrating session, not a captured platform payload. The session transport was not recorded, so the digest pinned in the manifest proves the committed file has not changed since it was pinned, not that this is the byte-exact string any model received."
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

# Executed prompt — AID-2026-059 / Issue #1223

## Assignment

Repair the duplicate-line blindness in `scripts/check_declared_check_contexts.py`.

The checker reads a fenced block of declared CI check-context names from
`14-ai-development/PR-GOVERNANCE-001.md` and compares it to the platform's
required contexts. Both sides were collapsed to `set()`, so a name listed
**twice** in the document was invisible: the sets still matched and the run
printed PASS. Measured on unmodified `main` with one duplicate line added:

```
17 declared check contexts, all produced by a job in .github/workflows and all required on main
DECLARED CHECK CONTEXTS: PASS
main() rc with 17 lines / 16 protected = 0
```

Seventeen declared lines passed against a sixteen-element protected set. Both
printed statements were individually true — the notice counted the list (17),
the comparison used the set (16) — which is why the disagreement was invisible.
The shape is the one #1061 and #1076 share: a check reporting success over a
fact it never read.

## Constraints

1. **Minimum diff.** One guard block plus one test. No refactor, no interface
   with one implementation, no new configuration.
2. **Exit code `1`, not `2`.** A duplicated line is a readable-but-wrong
   document. `2` stays reserved for `INCOMPLETE`, where the condition could not
   be read at all. Do not collapse the two.
3. **Keep the existing messages.** The unproduced-context errors, the
   set-difference errors and their wording stay byte-identical. The new failure
   is an additional branch, not a replacement.
4. **Do not touch `fetch_protected_contexts` or the endpoint it calls.** #1224
   requirement 1 owns the credential question; the `/branches/{branch}` payload
   stays as it is.
5. **No new dependency.** Standard library only, as the file already is.
6. **No behaviour change outside the named defect.** Existing suite counts may
   not decrease; no existing test is weakened or deleted.

## Acceptance

A named test that goes red when the guard is deleted. Deleting the new block
must fail exactly `test_violation_when_a_context_is_declared_twice` with an
`AssertionError`; restoring it must return the suite to green. The suite is
`scripts/test_check_declared_check_contexts.py`, and it must go 12 → 13 tests.
`tests/session_evidence` must stay at 98 tests passing, because nothing there
is touched.

Do not amend the existing fix commit; this document records the assignment that
produced it.
