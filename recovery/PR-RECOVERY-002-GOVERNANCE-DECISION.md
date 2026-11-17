# PR-RECOVERY-002 Governance Decision / 集成治理决议

**Status:** INTERIM RECOVERY CONTROL / PROPOSED FOR GOVERNANCE APPROVAL. This document does not claim an approved permanent policy.

## Roles
- **Accountable Owner:** domain authority responsible for scope and acceptance.
- **Implementation author:** person/automation that changes the branch; cannot independently approve its own work.
- **Independent reviewer:** reviewer who did not author the implementation and has the relevant domain/security competence.
- **Integration Owner:** coordinates base freshness, CI, merge method, exact-SHA merge and post-merge verification; cannot override domain acceptance.
- **Repository administrator:** supplies branch protection/ruleset evidence and controls required checks.

## Ready-for-review criteria
A PR is Ready only when scope, acceptance criteria, changed-file list, dependency/base, exact head SHA, test evidence, security impact, bilingual parity where normative, and requested reviewers are recorded. Draft is not a Ready signal.

## Review and integration SLAs (proposed)
- P0 security/integrity: acknowledge within 4 working hours; triage/containment plan within 1 business day.
- P1: reviewer assigned within 1 business day; first review within 2 business days.
- P2: reviewer assigned within 2 business days; first review within 5 business days.
- P3: reviewer assigned within 5 business days; review within 10 business days.
- Once all gates pass: integration within 1 business day, or record a specific blocker and accountable Owner.

These are proposed operational targets, not yet approved repository policy.

## Escalation
- Missing domain Owner/reviewer: mark OWNERSHIP_MISSING and escalate to project governance.
- Missing CI/branch rule evidence: mark CI_BLOCKED / UNKNOWN; do not infer success.
- Architecture conflict: stop the affected PR and request exact Owner/governance decision.
- Security uncertainty: SECURITY_REVIEW_REQUIRED; do not weaken controls.
- Stale PR: compare exact base/head, inspect diff and determine rebase, supersession or closure with evidence.

## Merge and closeout
- No self-approval where independent review is required.
- No bypass of required checks or branch protection.
- Record exact head SHA, all applicable gate results and merge method before merge.
- After merge, verify merge commit on main, PR merged state, linked Issue/Work Item and downstream PR diffs.
- GitHub Issues/PRs remain the authoritative engineering state; no external database or custom runtime is introduced.

## Current governance observation
At the frozen baseline all 68 PRs were authored by `oahcom`, with zero requested reviewers in the REST collection. This does not prove there are no submitted reviews, but it demonstrates reviewer assignment is not being used. Formal reviews were confirmed empty for #23, #27, #94, #95, #102 and #103. Independent review coverage across the remaining inventory is still UNKNOWN and must be read per PR.


## Latest live reviewer-assignment observation — 2026-11-18
- Current Open PR count is 76 (72 Draft / 4 Ready), all authored by `oahcom`.
- The live Open PR collection reports **zero requested individual or team reviewers** across all 76 PRs.
- The four Ready PRs #108–#111 have zero formal submitted reviews, zero review threads and zero check-runs at their exact heads. They are Ready for review, not merge-eligible.
- This is an operational assignment failure, not evidence that all 76 PRs have defective code. The PR Integration Owner must assign a distinct qualified reviewer before M7 can pass.
- This governance document remains INTERIM / PROPOSED FOR GOVERNANCE APPROVAL; the proposed SLAs are not yet normative.
