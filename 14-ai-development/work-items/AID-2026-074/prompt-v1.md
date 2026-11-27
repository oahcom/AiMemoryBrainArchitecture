---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The 16 was measured against GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main at 2026-11-25T09:50Z on main = afb0c6ce; PR-GOVERNANCE-001 section 7 was read at the same ref. The reverse-check behaviour was observed by running the extended checker, not inferred."
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

# WO — make the declared required-context set answerable against the platform

Scope: close the second half of Issue #1029 — the one that survived #1033. #1033
made §7's count correct; nothing made it stay correct. `scripts/check_declared_check_contexts.py`
asserted `declared ⊆ produced`, which is a subset test, so deleting a line from
the document could only make it more true.

## What this instruction is carried out against

1. Issue #1029 and its eleven comments. The title says 12-vs-15; that state was
   removed by #1033 (`2570ba0c`) before this work started. The measured count on
   `main` at `afb0c6ce` is **16**, and §7 already declares 16 — so the count
   premise of the title is stale and is not re-litigated here.
2. The reverse direction, which no gate held. Issue #1029 comment `7151648238`
   measured it by mutating the declared block four ways and observing `rc=0` on
   three of them. That is the defect this work item fixes.
3. The endpoint correction in comment `7151816460`: `GET /branches/{branch}`
   returns `protection.required_status_checks.contexts` under **Contents (read)**,
   so the comparison runs in CI without a new secret. `/protection` needs
   Administration (read), which `GITHUB_TOKEN`'s permission vocabulary cannot
   express, and is not used.
4. The ratification ruling in comment `7153866597`, which authorises the three
   session-evidence contexts from the enforcement window it identifies. §7 and
   `AID-2026-059`'s `required_context_change` field are amended to record it.

## Acceptance asked for

1. One command measures the count, and the measurement is what the document says.
2. The checker compares the declared set to the platform in **both** directions
   and names which direction drifted.
3. Unreadable platform exits 2 (INCOMPLETE). Absent token does not skip the
   comparison; absent token on a public repository is still a successful read.
4. Every carrier that said "twelve" as a standing assertion is either dated or
   pointed at §7. Anything that is a verbatim quote or a dated measurement stays.
5. No branch-protection write. This work changes what the repository *says*
   about a payload; it does not change the payload.

## Out of scope

`strict`, `enforce_admins`, `allow_force_pushes` and `allow_deletions` remain a
dated measurement in §7 prose. `/branches/{branch}` does not carry them, so a
live comparison of those four would need the Administration endpoint the token
cannot reach. Issue #134 keeps the wider question.
