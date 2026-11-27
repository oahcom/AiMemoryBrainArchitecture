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
        - "14-ai-development/work-items/AID-2026-211/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation record for the already-issued simpler-gate RC-1/RC-2 ruling; verification is limited to the named tests and exact PR head recorded in evidence."
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
    canonical_scope: "Execution evidence for the RC-1/RC-2 simpler-gate ruling"
    canonical_scope_id: "ai-development/aid-2026-211-simpler-gate-evidence"
    canonical_scope_keywords:
      - "document-management"
      - "approval-boundary"
      - "canonical-status"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-211 — Implement the simpler-gate RC-1 / RC-2 ruling

## Attribution and authority

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base: `main` at `788fbc011877a14976fc0a974ffe2e013dd9991b`
- Implementation branch (first attempt): `fix/2026-11-27-simple-gate-rc-1-2`
- Final PR branch: `fix/2026-11-27-simple-gate-rc-1-2-r3`
- Final PR: #1360; superseded attempts #1358 and #1359 were commented and closed.
- Work Item: `AID-2026-211` (`id_status: PROVISIONAL`; allocated after checking the 100-entry all-state PR listing and current remote branch names)
- Attribution: `user-authorized operator (delegated by account owner)`
- Date: `2026-11-27`
- This is execution of the already-issued “更简单的门禁” ruling (RC-1 + RC-2), not a new adjudication. The delegated record is not a natural-person Owner signature (`代理裁决，非自然人 Owner 签署`).

## Ruling implemented

**Principle:** add no validation; make the gate's declaration match what it actually does; frontmatter remains the sole authority for `canonical_status`. No decision logic, exit code, enumeration, threshold or required context is to change.

### RC-1 — M-02 description

The M-02 manual-control text now states only what the implementation checks: `decision_status` enumeration; for `Approved`, required `approved_version`, `approval_scope` and `approval_applicability`; and DM-10 body-hash binding to `approved_version`. It explicitly states that `approver` and `decision_date` are not required and that the gate does not verify that any approval exists. The generated M-02 row in the policy is synchronized with `MANUAL_CONTROLS`.

A scoped grep of `00-governance/` and `14-ai-development/` found no additional sentence asserting that GOV-DOC-002 mechanically enforces the existence of an approval. Statements describing policy obligations or GitHub's separate platform-level review protection were not weakened.

### RC-2 — security-governance README

The root README and its EN/ZH-CN mirrors now state that each of the five linked documents has `canonical_status: Canonical` in its own frontmatter; that frontmatter is the only authority for the field; and the README is a guide, not a normative source. The existing disclaimer remains: this does not ratify Phase 3.x decisions, approve a production policy, or establish implementation/conformance evidence. The five documents remain `normative_status: Informative`, `decision_status: Draft`, with no `approved_version`.

## Changed paths

- `scripts/check_document_management.py` — M-02 string in `MANUAL_CONTROLS` only.
- `00-governance/architecture-document-management-policy.md` — generated M-02 row only.
- `09-security-governance/README.md` — stale Candidate/Informative description and verification note corrected.
- `docs/en/09-security-governance/README.md` — matching English mirror corrected.
- `docs/zh-CN/09-security-governance/README.md` — Chinese summary and mirrored English section corrected.
- `scripts/test_check_document_management.py` — two feature tests added: `M-02 does not require approver or decision_date`; `09-security-governance README matches five Canonical frontmatters`.
- `14-ai-development/work-items/AID-2026-211/prompt-v1.md` — structured scope snapshot of the received task, explicitly not claimed as a verbatim raw transcript; manifest hash and byte count are bound to this exact file.

## Tests and gate evidence

Baseline self-check on the unchanged base: `367/367 passed`. After adding the two feature tests, the committed head self-check is `369/369 passed`; both named feature tests passed:

- `M-02 does not require approver or decision_date` — PASS.
- `09-security-governance README matches five Canonical frontmatters` — PASS.

Additional exact-head local results: GOV-DOC-002 incremental `--require-changed` — PASS (641 classified, 371 unclassified; 0 rule violations in the changed set); bilingual structural gate with `PR_BODY=BILINGUAL-MANIFEST: COMPLETE` — PASS (10 changed Markdown paths inspected, baseline 77 frozen / 0 new gaps); repository hygiene — PASS (119 work-item directories / 119 index links, 3 new paths admitted, 0 violations); line endings — 1715 files inspected, 0 violations. The bilingual gate explicitly reports that it is structural only; semantic parity is not claimed. The final PR sequence is recorded without treating the connector's incomplete Actions listing as authoritative: #1358's authenticated Actions listing contained eight workflows (seven success, one Session Evidence failure); its log said `MISSING: PR description: missing per-Issue mapping table`. The Session Evidence validator also requires an Issue-specific mapping row. Issue #1212 is historical and has no AI declaration, so the corrected row in #1360 is `| #1212 | LEGACY_UNDECLARED | N/A |`; the PR-level AI declaration and session evidence reference remain YES and fully populated. #1358 and #1359 were commented and closed as superseded; #1360 is the final active PR. The final branch head is a real two-parent merge commit, pushed through Git without force. The 16 required contexts must be read from the final head after this evidence update and are not inferred from earlier attempts.

The DM-side test constructs a document containing both optional fields and then removes `approver` and `decision_date`; `check_document()` returns zero errors. Its docstring quotes the revised M-02 description. The README-side test rejects the old Candidate/Informative wording in all three README group members and compares all five source frontmatters against the README declaration, while checking that the non-approval/non-conformance disclaimer remains.

**No new validation:** the `git diff` for `scripts/check_document_management.py` changes only the M-02 string literal inside `MANUAL_CONTROLS`; no condition, branch, parser, rule function, return value, exit code, enum, threshold or workflow is changed. The two added tests characterize existing behavior and README consistency; they do not add gate checks.

## Non-goals

- No new checker, validator, schema field, required key, or approval-presence test in production gate logic.
- No changes to policy obligations beyond clarifying that they are policy requirements, not machine-enforced by GOV-DOC-002.
- No changes to branch protection, required contexts, CI workflows, merge mode or Issue state.
- No Phase 3.x decision approval, production policy approval, implementation acceptance or conformance claim.
