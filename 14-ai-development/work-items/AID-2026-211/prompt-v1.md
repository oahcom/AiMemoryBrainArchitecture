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
      last_verification_note: "Delegated scope snapshot for the RC-1/RC-2 task; not represented as a verbatim raw prompt transcript."
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
    canonical_scope: "Scope snapshot of the delegated AID-2026-211 task input"
    canonical_scope_id: "ai-development/aid-2026-211-prompt-snapshot"
    canonical_scope_keywords:
      - "simpler-gate"
      - "rc-1"
      - "rc-2"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-211 — Prompt v1 scope snapshot

**Provenance:** structured scope snapshot derived from the user-authorized delegated task received in this conversation. It is not claimed to be a byte-for-byte export of the raw chat message. `executed_prompt_provenance` is therefore `NOT_VERIFIED`.

## Repository and operating constraints

- Repository: `oahcom/AiMemoryBrainArchitecture`; base branch `main`; observed base commit `788fbc011877a14976fc0a974ffe2e013dd9991b`.
- Allocate a Work Item number only after reading `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all&per_page=100`; do not reuse any number in PR titles or head branches.
- Metadata uses block-style YAML, never inline mappings beginning with `{`.
- PR body must include `Related issue(s): #1212`, `AI-assisted work: YES`, and `Session evidence reference(s): 14-ai-development/work-items/AID-2026-211/session-evidence.md`; the referenced file must exist in the head tree and contain `Session role / use case`, `Actual AI input`, and `AI-visible output`.
- If the Actions run listing truly reports zero for the PR head within the dispatch window, use the specified no-force rebuild/reopen fallback and comment/close the superseded PR. Do not claim checks passed without exact-head evidence.
- Merge only with all 16 required contexts successful, strict protection and enforce_admins enabled, branch freshness at zero behind, and the required merge method. Do not squash, rebase-merge, force-push, change branch protection or close Issue #1212. Verify every changed path's blob after merge.
- Attribution: `user-authorized operator (delegated by account owner)`; date `2026-11-27`. A delegated adjudication record must say `代理裁决，非自然人 Owner 签署`.

## Already-issued ruling to implement (do not re-argue)

**Principle:** add no validation. Make the gate's declaration agree with what it already does. Frontmatter is the sole authority for `canonical_status`. Do not change decision logic, exit codes, enumerations, thresholds or other gate behavior.

### RC-1 — M-02 wording

In `scripts/check_document_management.py` M-02, replace the false statement that the gate proves a decision record exists, names an approver and binds to a commit. State only that the gate validates the `decision_status` enumeration; for `Approved`, requires `approved_version` and `approval_scope` (and the actual `approval_applicability` requirement); and DM-10 binds the body hash to `approved_version`. Explicitly state that `approver` and `decision_date` are not required and the gate does not verify that any approval exists.

Search `00-governance/` and `14-ai-development/` for claims that the gate machine-enforces approval; qualify policy requirements as `policy requirement, not machine-enforced` without deleting policy intent.

### RC-2 — security-governance README

Correct `09-security-governance/README.md`, including its bilingual mirror group, so it no longer says the five linked documents remain Candidate / Informative when each of their own frontmatters says `canonical_status: Canonical`. Explicitly say each document's own `canonical_status` is the sole authority and the README is a guide, not a normative source. Preserve the disclaimer that this does not ratify Phase 3.x decisions, approve production policy, or establish implementation/conformance evidence.

### Required characterization tests

1. DM test: construct a legal document with `approver` and `decision_date`, remove both, and assert `check_document()` returns zero errors; the test docstring quotes the new M-02 wording.
2. README test: assert the README no longer describes the five documents as Candidate / Informative and that the five frontmatters agree with the README declaration.

## Deliverables and report

Create a new Work Item and INDEX row, with evidence and session evidence. Report the Work Item number, PR, every changed location with file/line and before/after context, the two test names/results, all 16 required contexts, merge SHA and post-merge per-file blob verification. Evidence must state that this implements the simpler-gate ruling, include the delegated attribution/date, and self-prove no new validation by showing the checker diff contains no decision-logic change.
