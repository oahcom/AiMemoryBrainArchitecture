---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-330/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Implementation instructions for AID-2026-330 blob declaration inventory."
    canonical_scope_id: "ai-development/aid-2026-330-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-330"
      - "prompt"
      - "blob-pin-inventory"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# MISSING STRUCTURES SUPPLIED. Write Deliverable B now.

You flagged that the manifest schema and the INDEX row shape were not in evidence. Both are below, verbatim from `main=f77b1e63f0aca6b93f14fee5bd5c04510053ee23`. Two corrections to my earlier message first.

## Correction 1 - the grep returned seven paths, not six

I wrote "exactly six paths" and pasted seven. The seven are correct. Record it as seven in the evidence file and drop my miscount.

## Correction 2 - a manifest schema checker exists, and it confirms the finding

`scripts/ci/check_work_item_manifest_schema.py` (258 lines) is the manifest schema of record. Its required top-level keys:

```python
REQUIRED = (
    "work_item_id", "title", "class", "risk", "risk_rationale", "status",
    "id_status", "sponsor", "accountable_owner", "acceptance_authority",
    "attribution", "date", "repository", "base_branch", "base_commit_sha",
    "scope", "evidence", "documentation", "session_evidence", "implementation",
)
DOC_RELATIONSHIPS = {"normative", "design", "implementation", "evidence", "reference", "code", "schema"}
IMPL_STATUSES = {"NOT_STARTED", "IN_PROGRESS", "IMPLEMENTED", "BLOCKED", "NOT_APPLICABLE"}
```

Structural rules it enforces:

- `documentation` must be a non-empty sequence of `{path, relationship}`; `path` must exist in the git tree; `relationship` must be in the set above.
- `session_evidence` must be a non-empty sequence; each entry must carry `role`, `issue_refs`, `implementing_ai_session`, `session_evidence_ref`; the ref's basename must match `session-evidence*.md`.
- `implementation` must carry `status`, `summary`, `files_changed`, `tests`; `status` must be in the set above; `files_changed` and `tests` must be sequences.
- Duplicate YAML keys are rejected.

**No blob-declaration field appears anywhere in that schema.** `root_blob`, `en_mirror_blob`, `related_evidence`, `authored_indexes`, `evidence_blob`, `d_source_blobs` are outside the manifest schema entirely. That is the discovery gap stated as a fact rather than a suspicion.

## The template's Section 1, verbatim

```yaml
work_item_id: "AID-YYYY-NNN"
title: ""
class: "ARCH | IMPL | TEST | SEC | MIG | PERF | DOC | OPS"
risk: "R0 | R1 | R2 | R3"
status: "PROPOSED"
sponsor: ""
accountable_owner: "A | B | C | D | E | F | G | H | I | CROSS-CUTTING"
implementing_ai_session: ""
independent_reviewer: ""
integration_reviewer: ""
acceptance_authority: ""
repository: "oahcom/AiMemoryBrainArchitecture"
base_branch: ""
base_commit_sha: ""
dependency_refs: []
# Non-normative and human-readable only; CI does not read this field. The
# normative prompt digest is executed_prompt_sha256 in the session_evidence entry.
prompt_id: ""
prompt_version: "v1"
# Non-normative and human-readable only; CI does not read this field or verify it
# against the snapshot. Same value as executed_prompt_sha256 when both are set.
prompt_sha256: ""
# Exact payload sent to this session after composing baseline + task-specific instructions.
executed_prompt_snapshot_file: ""
executed_prompt_sha256: ""
executed_prompt_bytes: null
executed_prompt_provenance: "VERIFIED | NOT_VERIFIED | NOT_AVAILABLE"
session_reference_status: "RECORDED | NOT_AVAILABLE | NOT_RECORDED"
session_evidence_ref: ""
created_at: ""
updated_at: ""
implementation_branch: ""
implementation_commits: []
changed_paths: []
documentation:
  architecture_significant: true
  policy_id: "GOV-DOC-001"
  chinese_paths: []
  english_paths: []
  source_revision: ""
  parity_review: "NOT_STARTED"
  coverage_register_updated: false
verification:
  status: "NOT_RUN"
  commit_sha: ""
  commands: []
  evidence_refs: []
evidence_tiering:
  repository: ""
  change_class: "ARCHITECTURE | SECURITY | PERFORMANCE_CRITICAL | PUBLIC_API | DATA_MIGRATION | DOC_NORMATIVE | FEATURE | BUGFIX | DOC_EDITORIAL | OPS | UNKNOWN"
  review_level: "R0 | R1 | R2 | R3"
  evidence_level: "1 | 2 | 3"
  assessed_by: ""
  assessed_at: ""
  rationale: ""
  base_head: ""
  classification_basis: ""
  classification_confirmed_by: ""
  classification_record: ""
  downgrade_justification: ""
  downgrade_confirmed_by: ""
  downgrade_confirmation_record: ""
  escalation_target: ""
  checker_result: "NOT_RUN"
  declaration_path: "evidence-declaration.yaml"
review:
  status: "NOT_STARTED"
  report_ref: ""
  findings: []
acceptance:
  status: "PENDING"
  record_ref: ""
merge:
  target_branch: ""
  merge_commit_sha: ""
  status: "NOT_MERGED"
```
```

## The INDEX table header and one live row, verbatim

```
| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
| [AID-2026-287](AID-2026-287/manifest.yaml) | Record the Capacity Alignment Ruling on the Allocation of Governance Capacity Between Records and Product Implementation | USER-PRINCIPAL-DELEGATED | DOC/GOVERNANCE / R1 | DISPATCHED — PROPOSED decision record; four rulings A1–A4 with falsifiers; no code, gate, workflow or branch-protection change; nothing merged | `AID-2026-287-PROMPT` v1 → `prompt-v1.md`; SHA-256 `9044c0fb487e91babdf100678b9ed859aee3111c63692c8317cefd73763df19c`, `11534` bytes; structured snapshot, provenance `NOT_VERIFIED` | Two ruling files (zh source + en counterpart) and the four work-item records; INDEX row; no upstream normative text edited | NOT_ASSIGNED — no independent exact-Head review recorded | PENDING — no Owner acceptance asserted; #1341 and #1349 remain OPEN |
```

The header is nine columns: `Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance`. Cells use ` — ` as a separator and carry no trailing pipes beyond the ninth.

## The operative manifest shape, verbatim (`AID-2026-326/manifest.yaml`, 176 lines)

```yaml
work_item_id: AID-2026-326
title: "Verify actual execution of required PR check contexts on exact Head"
class: CODE/CI
risk: R2
risk_rationale: >-
  Adds a read-only GitHub check-run audit and a manually dispatched workflow.
  Does not modify branch protection or the existing required-context set.
  The implementation distinguishes absent execution, stale heads, failed
  runs, pending runs and incomplete API evidence.
status: DISPATCHED
id_status: PROVISIONAL
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED
acceptance_authority: NOT_ASSIGNED
attribution: "user-authorized operator (delegated by account owner)"
date: "2026-11-27"
repository: oahcom/AiMemoryBrainArchitecture
base_branch: main
base_commit_sha: "31c1e5d83e7dad326dbd4b69d4a8e19534718ff1"
tracking_issue: "#1469"

scope:
  summary: >-
    Implement an independent execution-evidence audit for the sixteen
    declared required PR check contexts. The audit must establish actual
    check-run execution on the exact current PR head rather than relying
    on static workflow job declarations.
  in_scope:
    - "Add scripts/ci/check_required_context_execution.py."
    - "Parse declared contexts from PR-GOVERNANCE-001.md using the existing fenced declaration."
    - "Read PR head SHA, mergeable_state and draft through the GitHub REST API."
    - "Retry mergeable_state=unknown and return INCOMPLETE if unresolved."
    - "Read check-runs for the exact head SHA."
    - "Select the latest run per context by maximum started_at."
    - "Distinguish EXECUTED, ABSENT, STALE, FAILED and INCOMPLETE."
    - "Support GITHUB_TOKEN and GH_TOKEN."
    - "Add offline unittest coverage."
    - "Add a manually dispatched reachability workflow."
    - "Insert one registration row into the work-item INDEX."
  files_out_of_scope:
    - "14-ai-development/PR-GOVERNANCE-001.md"
    - "scripts/check_declared_check_contexts.py"
    - "scripts/test_check_document_management.py"
    - "Branch protection and required_status_checks configuration"
  change_boundary: >-
    This work item adds an execution-evidence observer only.
    It does not change the sixteen required contexts, branch protection,
    canonical governance text, existing declaration checker or
    document-management tests. The new workflow is manually dispatched
    and is not itself a required context.

evidence:
  - "Issue #1469"
  - "Supplied bidirectional scheduling probes"
  - "14-ai-development/PR-GOVERNANCE-001.md: declared-check-contexts"
  - "scripts/check_declared_check_contexts.py"
  - "Base commit 31c1e5d83e7dad326dbd4b69d4a8e19534718ff1"

documentation:
  - path: "14-ai-development/work-items/AID-2026-326/prompt-v1.md"
    relationship: reference
  - path: "14-ai-development/work-items/AID-2026-326/evidence.md"
    relationship: evidence
  - path: "14-ai-development/work-items/AID-2026-326/session-evidence.md"
    relationship: evidence

acceptance_criteria:
  - id: AC1
    description: >-
      All sixteen required contexts are parsed from the canonical
      fenced declaration without hardcoding the list.
    measurement: >-
      Execute the checker against a temporary document containing the
      declaration and inspect the resulting checks list.
    expected_result: "Exactly sixteen declared contexts in canonical order."

  - id: AC2
    description: >-
      Unknown mergeability is never interpreted as execution evidence.
    measurement: >-
      Offline unittest for persistent mergeable_state=unknown.
    expected_result: >-
      Five retries after the initial request, six PR reads,
      INCOMPLETE and exit 2.

  - id: AC3
    description: >-
      The latest run is selected by started_at rather than API list order.
    measurement: >-
      Offline unittest with an older failure and newer success for
      the same context, placing the older run last.
    expected_result: "EXECUTED; selected run is the newer success."

  - id: AC4
    description: "Missing execution and completed failure remain distinguishable."
    measurement: "Offline unittest for ABSENT and FAILED."
    expected_result: >-
      ABSENT contains the missing context; FAILED contains the failed
      context; neither is classified as INCOMPLETE.

  - id: AC5
    description: "Pending and unreadable evidence cannot produce EXECUTED."
    measurement: "Offline unittest for in_progress and API exceptions."
    expected_result: "Both return INCOMPLETE and exit 2."

  - id: AC6
    description: "A dirty head is classified as STALE."
    measurement: "Offline unittest with all-green fixture runs and dirty state."
    expected_result: "STALE and exit 1."

  - id: AC7
    description: "All-green exact-head evidence produces EXECUTED."
    measurement: "Offline unittest with sixteen completed/success runs."
    expected_result: "EXECUTED and exit 0."

  - id: AC8
    description: "The audit workflow is reachable without changing required contexts."
    measurement: >-
      Inspect .github/workflows/required-context-execution.yml and
      the branch-protection required context configuration.
    expected_result: >-
      workflow_dispatch only; no addition to required_status_checks.

review:
  status: NOT_ASSIGNED
  note: >-
    Independent review has not been recorded. The implementing session
    does not review or approve its own work.

acceptance:
  status: NOT_ASSIGNED
  record_ref: ""
  acceptance_authority: NOT_ASSIGNED

implementation:
  status: IMPLEMENTED
  summary: >-
    Proposed implementation consists of the execution checker, offline
    unittest suite, manually dispatched workflow, evidence record,
    session evidence, prompt reference and INDEX registration.
    No command execution, test pass, repository write, PR creation,
    independent review, Owner acceptance or merge is claimed.
  pull_request: PENDING
  merge_commit: ""
  implementation_commit: ""
  ci_status: NOT_CLAIMED
  files_changed:
    - scripts/ci/check_required_context_execution.py
    - scripts/ci/test_check_required_context_execution.py
    - .github/workflows/required-context-execution.yml
    - 14-ai-development/work-items/AID-2026-326/manifest.yaml
    - 14-ai-development/work-items/AID-2026-326/prompt-v1.md
    - 14-ai-development/work-items/AID-2026-326/evidence.md
    - 14-ai-development/work-items/AID-2026-326/session-evidence.md
    - 14-ai-development/work-items/INDEX.md
  tests:
    - "python -m unittest discover -s scripts/ci -p 'test_check_required_context_execution.py' -v"
    - "python scripts/ci/check_required_context_execution.py --pr 1469"
    - "python scripts/ci/check_required_context_execution.py --pr 1469 --json"
    - "python scripts/check_declared_check_contexts.py"
    - "python scripts/ci/check_work_item_manifest_schema.py"
    - "python scripts/ci/check_manifest_parse.py"
    - "python scripts/ci/check_test_reachability.py"
    - "python scripts/ci/check_repository_hygiene.py --base <base> --head <head>"

session_evidence:
  - role: IMPLEMENTER
    issue_refs:
      - "#1469"
    implementing_ai_session: GPT6_SESSION_20261127_AID2026326
    executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-326/prompt-v1.md
    executed_prompt_sha256: afc8e732df2de2eb29e22b21b05558c395c1b2ee1ee2c4ddeca5e3744ba39e91
    executed_prompt_bytes: 4894
    executed_prompt_provenance: NOT_VERIFIED
    session_reference_status: "RECORDED"
    session_evidence_ref: 14-ai-development/work-items/AID-2026-326/session-evidence.md
```

Note how that file satisfies both the schema checker and the template while remaining honest: `id_status: PROVISIONAL`, `implementation.pull_request: PENDING`, `ci_status: NOT_CLAIMED`, `review.status: NOT_ASSIGNED`, `acceptance.status: NOT_ASSIGNED`, and a `session_evidence` entry with `executed_prompt_provenance: NOT_VERIFIED`.

# Deliverable B, final

Produce the complete file set for the AID-2026-330 documentation-only PR, in this order, each as a fenced block labelled with its exact path:

1. `14-ai-development/work-items/AID-2026-330/manifest.yaml` — must pass `check_work_item_manifest_schema.py` (all 20 required keys) and must not claim any merge, CI result, review or acceptance. `base_commit_sha: f77b1e63f0aca6b93f14fee5bd5c04510053ee23`. `class` and `risk` values must come from the enumerations the schema checker and template actually accept.
2. `14-ai-development/work-items/AID-2026-330/prompt-v1.md` — the prompt snapshot, with one clearly marked placeholder line where the literal payload goes.
3. `14-ai-development/work-items/AID-2026-330/session-evidence.md`.
4. `14-ai-development/work-items/AID-2026-330/blob-declaration-inventory.md` — Deliverable A from your previous reply, cleaned up: the table with the corrected path count, the enumeration commands with their real outputs, the `DISCOVERY_LIMITS` section, and the coverage-collision findings (template non-normative top-level `prompt_sha256`; nested `prompt:` mapping undefined; `session_evidence/validate.py` check 11 already enforcing SHA-256 and byte count from the PR-head tree; two bases can disagree).
5. The exact `INDEX.md` row, nine cells, matching the live row's style.
6. The PR body with `AI-assisted work: YES`, the per-Issue table and the Session evidence reference.
7. A list of every path the PR touches, so I can confirm documentation-only.

Also answer the two decisions from my previous message explicitly:

- Does the fail-closed rule live in AID-2026-330 (recorded) or AID-2026-336 (implemented)?
- Does AID-2026-333 survive as scoped, or does it collapse into "remove the duplicate byte-count branches, `session_evidence/validate.py` remains the enforcing gate"? Restate its scope and evidence if it collapses.

Hard constraints: documentation only, nothing executable changes, no acceptance or merge language, every claim traceable to a command output or a quoted line above. If something still blocks you, name the exact file and the exact field you need, not a general request.
