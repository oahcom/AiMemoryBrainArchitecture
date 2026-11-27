---
document_metadata:
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Metadata added on 2026-11-24 so that this file can be edited without tripping DM-01. No content claim in this file is verified by this block."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "14-ai-development/PR-GOVERNANCE-001.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md"
---

# PR-GOVERNANCE-001 — Enforcement & Evidence Addendum
# PR 治理强制执行与证据补充规范

- Document ID: PR-GOVERNANCE-001-ENFORCEMENT
- Version: 1.2
- Status: PROPOSED — becomes normative only after authorized review and merge
- Parent: [PR-GOVERNANCE-001](../../../14-ai-development/PR-GOVERNANCE-001.md)
- Tracking: [Issue #130](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130), [Issue #134](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/134)
- Bilingual counterpart: [简体中文](../../zh-CN/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md)

## 0. PR creation and branch-merge boundary

A pull request is mandatory **only when the target branch is `main`**. This applies to every source branch, including Owner primary branches and child/work branches: if the merge target is `main`, use a PR and satisfy the applicable exact-Head checks and independent-review gate in this addendum.

Merges whose target is any non-`main` branch do **not** require a PR. This includes child/work branch → its Owner primary branch, ordinary branch → Owner primary branch, and Owner primary branch → another non-`main` branch. These are Owner-internal integration operations; the responsible Owner still performs the required scope, test, evidence and safety checks and records material decisions in the existing owning work item. Do not create a PR solely to represent such an internal merge.

Do not interpret this exception as permission to bypass the `main` PR gate by merging into `main` through another route. Before creating a PR, search for an existing PR covering the same change and target; update/reuse it rather than creating a duplicate. Before creating an Issue, search for an existing owning Issue and update/link it. A session, subtask, or closeout is not by itself grounds for a new PR or Issue. Close only demonstrably duplicate, superseded, or completed carriers after preserving links and rationale.

## 1. Exact-Head merge gate

A PR may be classified MERGE only when all checks applicable to its changed paths and risk class have completed successfully on the exact current PR Head SHA. The closeout must record the check's displayed GitHub context/name, workflow run ID, URL, conclusion, and tested Head SHA. Re-read the PR Head immediately before merge; any new commit invalidates prior exact-Head evidence and requires re-running affected checks.

Mandatory documentation gate:
- `GOV-DOC-001 structural checks` from the Bilingual documentation gate for every PR that changes governed documentation or its PR manifest.
- The bilingual manifest must be `BILINGUAL-MANIFEST: COMPLETE`, or a formally approved, time-bounded `BILINGUAL-EXCEPTION: APPROVED` with accountable Owner, missing counterpart path, exact source revision, due date and tracking Issue.
- A green documentation workflow does not itself prove semantic bilingual parity; the PR must also list paired paths and disclose any semantic differences.

Rust gate:
- For changes to `Cargo.toml`, `Cargo.lock`, `crates/**`, or the Rust workflow, require the exact-Head Rust Workspace test result for `cargo test --workspace --all-targets`.
- Measured 2026-11-25: the Rust workflow has carried no `pull_request.paths` filter since #1027, and `rust-workspace-test` is one of the sixteen required contexts on `main` (protection read back 2026-11-25, `strict: true`, `enforce_admins` enabled), so it already runs on every pull request and needs no aggregate gate. Conditional rule: if a future change re-introduces a `paths` filter on a workflow whose context is required, that check will be skipped on non-matching pull requests, and an always-running aggregate gate must be added before the context is made required.

No merge on missing, pending, skipped-when-applicable, failed, stale-Head, or unverifiable checks. A run on another PR or a later main commit is not a substitute for exact-Head PR evidence.

Platform check unavailability:
- A check may be applicable yet unable to start because of a documented platform failure, for example an Actions billing suspension, a runner that is permanently offline, or a repository-level API refusal. In that situation the PR may still be classified MERGE only when the acceptance comment records all of the following: (a) the exact run ID and URL where a run object exists, plus the platform message verbatim; (b) an equivalent local execution, at the exact PR Head, of the same in-repo check script with identical inputs (same base SHA, head SHA and PR body), whose stdout, stderr, exit code and SHA-256 are archived in the PR or a linked evidence file, together with a statement of why that script is deterministic for those inputs; (c) a named exception under the RULING-06 five fields; and (d) an explicit statement that this is compensating evidence, not evidence that the check passed.
- Such an exception is scoped to that PR only. It expires when the platform can run checks again or at its recorded expiry date, whichever is earlier, and MUST NOT be reused for later PRs, cited as precedent for skipping checks, or treated as equivalent to a passing check.

## 2. Review and approval gate

- Require at least one approving review from a session independent of the PR author for normal changes; require affected domain Owner approval for changes to that Owner's normative contract. Independence is a property of the reviewing session, not of the GitHub account: separate sessions may share one identity.
- Dismiss stale approvals when new commits are pushed.
- Require all review conversations to be resolved before merge.
- A COMMENT is not an APPROVE. A separate session reviewing the artifacts of a change it did not author and did not implement **is** an independent reviewer, and may report through the same connected GitHub identity. AI role simulation inside the authoring session is not independent review: the reviewer and the author would share one context and one incentive.
- Record reviewer login, review state, reviewed Head SHA, timestamp/link, same-identity/delegation disclosure and unresolved findings.
- Where independent approval cannot be obtained, disposition is HOLD unless an authorized, explicit, scoped and time-bounded exception is recorded. Do not self-approve or represent role-play as Owner approval.

## 2.1 Acceptance comment minimum checklist

An acceptance or merge-authorization comment posted in an Issue — as distinct from the PR body, which the pull request template governs — MUST contain the following four rows. This clause exists because a PR template constrains the PR body only; it cannot constrain free-form Issue comments. An acceptance comment that omits check conclusions can grant ACCEPT while an exact-Head check is failing.

Required rows:

1. **Exact Head SHA** — the commit actually evaluated, written in full or truncated with the length stated. A branch name is not a substitute.
2. **Applicable check conclusions** — for that exact Head, each applicable check name with its conclusion and run URL. If no check is applicable, state "none applicable" and give the reason. That reason MUST be objectively verifiable from the change itself, for example that no changed path matches any workflow path filter. Proving that no path-filtered workflow matches is not sufficient by itself; the accepting party must also exclude applicable checks that run unconditionally regardless of path. A bare assertion by the accepting party, without such a basis, does not satisfy this row.
3. **Review state and reviewer identity** — review state (APPROVED / COMMENTED / REQUESTED_CHANGES / NOT_REVIEWED), reviewer login, reviewed Head SHA, and a same-identity or delegation disclosure. A COMMENT is not an APPROVE. An APPROVED state is valid only when the approval comes from a reviewer who satisfies the independence requirements of section 2; an approval recorded under the same GitHub identity as the PR author is valid only when the session that produced it is independent under section 2 and the comment discloses that independence is session-level; an approval produced by AI role simulation inside the authoring session is not a valid approval and MUST NOT be recorded as APPROVED. Where section 2 requires an approving review for the change, a state of NOT_REVIEWED, COMMENTED or REQUESTED_CHANGES MUST be paired with an exception record under row 4; absent that pairing the comment MUST NOT carry ACCEPT.
4. **Exception record** — if any applicable check is failing, missing, pending, skipped-when-applicable, stale-Head or unverifiable, the exception MUST be named: basis, authorizing party, scope, expiry condition and tracking Issue. If there is no exception, state "no exception".

Scope of the row-4 exception record: it is a disclosure and audit mechanism and does not exempt the section 1 check gate. A section 2 exception is an authorized exception to the review and approval gate only; a failing, missing, pending, skipped-when-applicable, stale-Head or unverifiable check cannot be exempted merely by registering an exception in this checklist. While any such check state persists, the PR MUST NOT be merged and the comment MUST NOT carry ACCEPT or merge-authorization YES, regardless of any exception recorded in row 4.

Invalidity rule:

A comment missing any of the four rows MUST NOT be treated as a valid acceptance and MUST NOT carry an ACCEPT or merge-authorization YES. Such a comment is void and must be withdrawn and re-issued. The withdrawal MUST be recorded as an appended VOID declaration in the same thread that cites the replacement comment; deleting or editing the void comment is prohibited, because it destroys the audit trail by which a later reader could detect the breach.
 A later valid acceptance does not retroactively validate a merge already performed; that merge MUST be recorded as a gate-breach finding.

Recorded instance:

PR #273, exact Head `5e0a919a9253b8747c59062b87d0a580cd204e54`, had `GOV-DOC-001 structural checks` = failure (run `44491572672`, completed 2026-11-19T08:54:26Z). Acceptance comment `7005241529` (2026-11-19T09:33:25Z) recorded ACCEPT and merge authorization YES with a six-row reconciliation table that contained no check-conclusion row. The PR merged at 2026-11-19T09:33:37Z. Tracking Issue: #134.

## 3. Comment and session audit evidence

Every substantive AI session must leave a durable GitHub record in its owning Issue/PR. Record at minimum:
- Session ID, prompt ID, immutable prompt version, prompt SHA-256; exact prompt source path/commit/blob where available.
- If the prompt hash was not captured at execution time, write `NOT RECORDED`; never reconstruct or guess a hash from a paraphrase.
- Work Item and owning Issue; related PRs; accountable Owner and session role.
- Repository, branch, base SHA, exact Head SHA, changed paths and actual work performed.
- Material findings and decision states (PROPOSED / ACCEPTED / REJECTED / OPEN / BLOCKED), decision authority and links to source evidence.
- Exact commands/environment, checks run and NOT RUN, run IDs/URLs, conclusions and tested SHA.
- Reviewer identity/state, dependencies, blockers, risks, handoff Owner and exit condition.
- Merge state; if merged, target branch, actual merge SHA and post-merge verification.

Comments are audit records, not proof by themselves. Every assertion of PASS, merge, approval or DECIDED must link to its source evidence. Preserve failed checks and contradictory historical records; append a correction rather than rewriting history. The Integration Owner maintains the session → Work Item/Issue → PR → commit → CI evidence traceability index. Session authors remain accountable for their own closeout.

## 4. CANDIDATE → DECIDED evidence standard

A CANDIDATE must not be upgraded to DECIDED by consensus language, an AI conclusion, a passing documentation check, or a merged PR alone. A DECIDED record requires:
1. Explicit decision authority: named accountable Owner(s), approval reference and date; cross-owner decisions include all affected Owners or the established arbitration/ADR authority.
2. Exact implementation/specification Commit SHA(s) and changed paths.
3. Successful CI Run ID(s) and URL(s) executed against the exact candidate Head SHA; list workflow/check name and conclusion. If CI is not applicable, explain why and provide reproducible alternative evidence.
4. Required domain evidence: tests, independent review, compatibility/security/failure analysis, benchmark or prototype results as appropriate.
5. Scope, assumptions, non-goals, known limitations and explicit claims not established by the evidence.
6. Synchronized Chinese and English decision records with matching status, identifiers and evidence references.
7. A decision log/ADR or owning specification updated in the same PR, plus links from the owning Issue and Work Item index.

If any mandatory item is absent, retain CANDIDATE, TO_VALIDATE, OPEN or BLOCKED as appropriate. A merged PR is repository integration evidence, not automatic decision authority.

## 5. GitHub platform configuration runbook — manual administrator action required

**Current observed state:** Issue #134 records `main protected=false` and required status checks not enforced. The rulesets endpoint returned HTTP 403 with a plan/visibility limitation message. Therefore process text, PR templates and green CI runs do not currently constitute a hard platform merge gate. This addendum does not claim the controls have been enabled.

**Manual action — Repository Administrator / Owner (suggested: repository owner `oahcom`):**
1. Decide the acceptable hosting/plan path while keeping repository confidentiality: upgrade the private repository owner's GitHub plan to a tier that supports the required private-repository branch protections/rulesets, or choose another private hosting/configuration with equivalent enforceable controls. Do not make this private repository public merely to unlock a feature without an explicit security/privacy decision.
2. In GitHub repository Settings → Branches (or Rules → Rulesets where supported), create a rule targeting exactly `main`.
3. Enable pull requests before merging; require at least one approval; dismiss stale approvals after new commits; require conversation resolution; restrict force pushes and branch deletion; include administrators / disable bypass where the platform supports it. If bypass cannot be disabled, define named emergency actors, reasons, evidence and post-event audit.
4. Require the exact check contexts surfaced by GitHub for the PR workflows. At minimum, require `GOV-DOC-001 structural checks` for governed documentation. Measured 2026-11-25: since #1027 the Rust workflow carries no `pull_request.paths` filter, and `rust-workspace-test` is already one of the sixteen required contexts (protection read back 2026-11-25, `strict: true`, `enforce_admins` enabled), so that check already runs on every pull request to `main` and needs no aggregate gate. Conditional rule: if a later change re-introduces a `paths` filter on a workflow whose context is required, that check will be skipped on non-matching pull requests, and an always-running aggregate gate must be added before the context is made required. Do not guess context names; select the observed check context attached to a real PR Head.
5. Save the rule, then read back the branch/ruleset configuration through GitHub UI/API. Record the rule ID/name, target, enabled settings, bypass actors and timestamp in Issue #134. A 403/permission-denied read is UNKNOWN, not proof of enforcement.

**Verification — Integration Owner (suggested: Integration Owner, independent of the author):**
1. Open a small test PR with a deliberately failing required check on its exact Head; confirm GitHub blocks the normal merge path.
2. Confirm a PR with a passing exact-Head check and independent approval becomes merge-eligible; push a new commit and confirm stale approval is dismissed and checks rerun.
3. Confirm unresolved review conversations block merge; confirm force-push/deletion restrictions and administrator bypass behavior.
4. Record test PR URL, exact Head SHA, failed/passing workflow Run IDs, observed blocked/eligible state, ruleset/branch-protection readback and verifier identity in Issue #134.
5. Keep Issue #134 OPEN until all acceptance criteria are evidenced. A settings screenshot alone is not enough; include API/UI readback and a negative test proving a failing required check cannot merge.

**Suggested ownership:**
- Repository Owner/Admin (`oahcom`): plan/visibility decision, branch/ruleset configuration, bypass policy.
- Integration Owner: workflow context inventory, policy checklist, exact-Head evidence, negative merge test and issue closeout.
- Workflow Maintainer: ensure workflow triggers/check contexts are stable. Measured 2026-11-25: the Rust check needs no aggregate gate, because since #1027 there is no `pull_request.paths` filter and `rust-workspace-test` is one of the sixteen required contexts (protection read back 2026-11-25, `strict: true`, `enforce_admins` enabled). Conditional rule: if a later change re-introduces a `paths` filter on a workflow whose context is required, that check will be skipped on non-matching pull requests, and an always-running aggregate gate must be added before the context is made required.
- Independent Reviewer / Security Owner: review the platform control design and emergency bypass/audit policy.
- Each AI session author: prompt hash, session closeout, exact commits and run evidence.
These are role recommendations, not claims that the named people have accepted assignments.

## 6. Issue #130 session coverage audit

Issue #130 is ADOPTED as a process policy but remains OPEN for operationalization. The Integration Owner should:
1. Enumerate active and completed substantive AI sessions from the Work Items index and related PR/Issue timelines.
2. Match each session to one owning Work Item/Issue and one or more existing PR/Issue carriers; consolidate duplicates rather than creating new PRs for the same result.
3. Check each closeout for session/prompt identity, prompt SHA-256, role/Owner, branch and exact Head, actual work, decision status/authority, CI evidence including NOT RUN checks, review identity, blockers and handoff.
4. Mark historical prompt hashes that were not captured as `NOT RECORDED`; do not fabricate retroactive hashes. Create a follow-up capture requirement for future prompts.
5. Add missing closeouts to the existing carrier, link related sessions bidirectionally, and update `14-ai-development/work-items/INDEX.md`.
6. Report coverage as audited/complete, audited/gaps, or not yet audited. Keep Issue #130 OPEN until all discovered gaps have an owner and explicit closure condition.

## 7. Rollback and emergency correction

- If a merge passes despite a failed/missing required check, immediately stop further normal merges, record the exact PR/Head/merge SHA and run evidence, disable the bypass path if authorized, and open/update a P0 governance incident. Do not rewrite the failed run or history.
- If the merged change is unsafe or materially incorrect, prefer a dedicated revert PR targeting the current main Head. The revert PR must itself pass the applicable exact-Head checks and independent review. Do not force-push or reset shared `main`.
- If revert is unsafe or cannot restore service, use a narrowly scoped forward-fix PR with an explicit mitigation, owner, validation and expiry/exit condition. Record why revert was rejected.
- For a false DECIDED claim, append a correction/supersession record linking the original decision, evidence gap, corrected status and affected downstream decisions. Never silently downgrade or delete the historical decision.
- Emergency bypass is last resort only: authorized actor, documented incident/reason, exact SHA, tests/checks skipped, risk acceptance, time window and mandatory post-event independent review must be recorded in the Issue/PR. Emergency bypass does not retroactively turn skipped checks into PASS.

## 8. Current evidence record — PR #242

- PR #242 merged at `aa711289785395d2efa202e34def64c393ee0ac7`.
- Follow-up verification commit: `4a3e06fd263e9dbd1056179dceb3cb21b17e330f`.
- PR Rust Workflow: Run [44259233587](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44259233587), SUCCESS (PR event; Head `09ab26963293ee460237c6f27c5b95ed3b401730)).
- PR Bilingual documentation gate: Run [44259233358](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44259233358), SUCCESS (PR event; same Head).
- Subsequent main Rust Workflow: Run [44261208110](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44261208110), SUCCESS; push event; exact main Head `fcdecf0a4e638c8b3c9ac0e4623f97c98ed21291`; job `rust-workspace-test`; command `cargo test --workspace --all-targets`.
- The main run validates the later main snapshot containing PR #242; it is distinct from the PR-triggered exact-Head checks above.

## 9. Adoption boundary

This addendum is PROPOSED until reviewed and merged. The existing PR-GOVERNANCE-001 process policy remains ADOPTED. Neither document claims Issue #134's platform enforcement is complete. Issues #130 and #134 remain open until their separate operational acceptance criteria are met.
