---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Implementation specification delivered; exact-head execution and independent acceptance remain pending."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Implementation evidence for Issue #1246"
    canonical_scope_id: "ai-development/issue-1246-body-digest-gate"
    canonical_scope_keywords:
      - "session-evidence"
      - "body-digest"
      - "workflow-shape-guard"
    canonical_conflict_status: None
    normative_status: Informative
---

# Evidence — Issue #1246

**Work item:** AID-2026-302

**Repository:** `oahcom/AiMemoryBrainArchitecture`

**Baseline:** `cb5b3dcd23ff86e10a354bb27b668dce19e95f62`

**Carrier:** `PLACEHOLDER_PR`

## 1. Defect

The session-evidence workflow writes:

`AI-SESSION-EVIDENCE-BODY-SHA256: $digest`

to `$GITHUB_STEP_SUMMARY`, but the existing verdict reader searches only for:

`^AI-SESSION-EVIDENCE: `

Consequently, the body digest is written but never enforced by the existing workflow shape gate.

## 2. Implementation decision

Extend the existing `scripts/check_session_evidence_workflow_shape.py`.

The new checks locate the uniquely named step:

`Bind the verdict to the body it judged`

All requirements must be present inside that step:

1. `if: always()`
2. A summary write containing `AI-SESSION-EVIDENCE-BODY-SHA256: $digest`
3. A validation expression requiring 64 lowercase hexadecimal characters.

The checks are independent and produce separate diagnostics.

## 3. Required mutation coverage

| Mutation | Expected exit | Diagnostic |
|---|---:|---|
| Delete the named digest step | 1 | `PR body digest mutation 1` |
| Change `if: always()` to `if: success()` | 1 | `PR body digest mutation 2` |
| Replace the digest write with `AI-SESSION-EVIDENCE: PRESENT` | 1 | `PR body digest mutation 3` |

Every diagnostic includes a source line or a nearby job location when the step is absent.

## 4. Scope restrictions

- No new workflow.
- No new required context.
- No modification to `.github/workflows/session-evidence.yml`.
- No modification to `scripts/governance/session_evidence/validate.py`.
- No third-party Python dependencies.
- No change to the four existing workflow-shape assertions.

## 5. Gate integration

The existing repository-hygiene workflow invokes the shape checker inside the required `Repository hygiene (hard gate)` context.

The extension therefore inherits the existing enforcement path without introducing another status context.

## 6. Verification

Required command:

`python3 scripts/test_check_session_evidence_workflow_shape.py`

Required additional verification:

- Current baseline exits 0.
- Each of the three specified mutations exits 1.
- The existing 17 regression cases retain their intended assertions.
- The 64-hex validation is tested independently.
- Manifest schema validation succeeds.

## 7. Acceptance boundary

This evidence records the intended implementation and its deterministic acceptance conditions.

It does not assert that the tests have been executed, that the carrier has merged, that required contexts have passed, or that Owner acceptance has been granted.

Those claims require exact-head readback and independent verification.

## 8. Static-gate scope limitation

This guard proves that the named digest step exists and has the required textual shape: an always-run condition, the expected summary key, and a 64-character lowercase-hex validation pattern.
It does not execute the shell or prove that `$digest` is computed from the live PR body's `body` field.
A constant 64-character value can therefore satisfy this static shape check.
Runtime digest provenance and correctness are outside this guard's acceptance claim.
