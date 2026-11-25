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
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The five gaps and the fifth-item wording were read on 2026-11-25 from Issue #262 comment 7153428650 and from section 5 of PR-GOVERNANCE-001.md at main edbc3632. The counts below were produced by reading every manifest under 14-ai-development/work-items with a script, not estimated."
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

# WO — An observation-only attachment point for the assessment signature requirement (#262 AC2)

Scope: build the missing reader for the four normative requirements in section 5 of
`PR-GOVERNANCE-001.md`, and run it in observation mode. This work item does not make
the check blocking, does not change branch protection, and does not add a required
context.

## Why this is the last open item

Issue #262 AC2 asks for a REQ-level risk assessment that is signed by a session
independent of what it assesses. The standard now says so in both languages, in
four parts: role, isolation, signature, accountability. The text is merged —
`PR-GOVERNANCE-001.md` section 5, via PR #1073, merge commit `edbc3632`.

What is absent is the attachment point. Measured on `main` at `edbc3632`:

| measured | how | result |
|---|---|---|
| readers of `assessor` / `assessed_version` / `evidence_baseline` | search over `*.py`, `*.yml`, `*.yaml`, `*.sh`, `*.rs` | 0 |
| manifests carrying all three of `sponsor`, `accountable_owner`, `implementing_ai_session` | read every `work-items/*/manifest.yaml` | 41 of 48 |
| manifests carrying `implementing_ai_session` only inside a nested block | same | 14 |
| manifests distinguishing `accountable_owner` from `implementing_ai_session` by principal | same | 41 of 41 once `sponsor == accountable_owner` is permitted |
| assessments in `#262` that carry `assessor`, `assessed_version` or `evidence_baseline` | read the assessment comments | 0 of 4 |

The clause AID-2026-071 delivered says in its own evidence record that no check
enforces it. A requirement with no reader cannot be breached in any way that is
observable, so AC2 stays PARTIAL while the clause alone is in place.

## The staging, and why it is not caution

Three stages, and this work item carries only the first:

1. **Observe.** Report findings. Do not fail the pull request. Do not become a
   required context.
2. **Remediate.** Bring the applicable records into compliance, with the observer's
   output as the list.
3. **Block.** Make the result a required context. Separate authorization.

Running the stages out of order produces the state `rust-workspace-test` was in
before PR #1027: a required context that fails on the commit that introduces it,
where the only available action is a revert of the gate that was just added. The
measured numbers above are the reason: turning this on as blocking today would
report violations against most of the registry and would mark every existing
assessment unsigned in the same run.

## What stage one must and must not do

Must: read the top-level fields, judge principal identity rather than string
inequality, report each missing field separately, validate the `assessed_version`
length, produce the same findings for the same inputs, and leave previously
accepted assessments distinguishable from ones governed by the corrected clause's
applicability boundary.

Must not: fail a pull request on its findings, register itself as a required
context, modify branch protection, or change any validator that already gates
merges. `gate_behaviour_change` is `NOT_GRANTED` in the manifest, and C10 restates
it as an acceptance criterion so a reviewer can check the shape of the workflow
rather than take the manifest's word for it.

## Out of scope

The ten canonical requirements in the manifest are the scope. Not in it: rewriting
the assessment records, re-signing historical assessments, editing the standard
again, and any change under `crates/`.
