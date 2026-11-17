# AI Work Item and Prompt Record Template
# AI 任务与提示词记录模板

**Document ID:** AI-TPL-001  
**Version:** 1.0  
**Status:** PROPOSED

Copy this template for each work item. Store the approved prompt as an immutable version before the AI run.

## 1. Work item manifest / 任务登记

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
prompt_id: ""
prompt_version: "v1"
prompt_sha256: ""
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

## 2. Prompt content / 提示词正文

# [Work Item ID] — [Task Title]

## Role
You are the [named Owner / specialist] for repository `oahcom/AiMemoryBrainArchitecture`.

## Objective
Describe the observable outcome. Do not describe an unapproved implementation as a requirement.

## Authoritative inputs
List exact file paths, branch names, commit SHAs, ADRs, decisions and relevant test fixtures. If a source is unavailable, stop and report it.

## Authority and ownership
- You own:
- You may modify:
- You must not modify:
- Required consultations/approvals:

## Scope
### In scope
- ...

### Out of scope
- ...

## Constraints and invariants
List normative requirements, trust boundaries, compatibility requirements, state-machine invariants and non-negotiable project rules.

## Required work
Provide ordered, bounded steps. Require inspection before modification. Identify design decisions that may be made by this Owner and decisions that must be escalated.

## Acceptance criteria
Each criterion MUST be objectively verifiable. Avoid “high quality”, “robust” or “complete” without a measurable condition.

1. [ ] ...
2. [ ] ...
3. [ ] ...

## Verification plan
List exact commands, tests, fixtures, expected results and required fault/security cases. Mark unavailable checks as NOT RUN with a reason.

## Bilingual documentation requirement (mandatory for architecture-significant work)

Read GOV-DOC-001. Before implementation/design work, list the Chinese and English paths for every architecture-significant artifact. Deliver both versions in the same change set, preserve normative force and decision status, keep stable identifiers unchanged, and update the glossary/translation coverage register when required. A missing counterpart must be marked STALE with owner, source revision, due date, and approved exception; it is not a completed deliverable.

## 双语文档要求（架构类任务强制）

阅读 GOV-DOC-001。在开始设计/实现前，列出每项重要架构交付物的中英文路径，并在同一变更集中交付。两种语言必须保持规范效力和决策状态一致，稳定标识不得改写；必要时同步更新术语表和双语覆盖登记表。缺少对应版本时必须登记 STALE、责任人、源版本、截止日期和获批例外，不能视为完成。

## Required deliverables
- Chinese documentation paths:
- English documentation paths:
- Bilingual parity checklist/evidence:
- Coverage register update:
- Modified/new files:
- Decision/change log:
- Tests:
- Review evidence:
- Final report:

## Stop conditions
Stop and report if:
- a required source or dependency SHA is unavailable;
- authoritative contracts conflict;
- the task requires another Owner's decision;
- a security/data-integrity invariant cannot be maintained;
- acceptance criteria cannot be verified;
- unexpected files or migrations fall outside scope.

## Git and evidence requirements
- Work only on the assigned branch.
- Do not merge other branches.
- Commit with a meaningful message.
- Report full branch HEAD SHA and commit SHA.
- Read back changed files after writing.
- Report changed paths and test evidence.
- Do not claim success for unrun checks.

## Final report format
1. Work Item ID / Prompt ID and version.
2. Actual branch and base/head SHAs.
3. Sources read with exact SHAs.
4. Changes and rationale.
5. Acceptance criteria: PASS / FAIL / NOT RUN, with evidence.
6. Tests: command, environment, expected/actual, result.
7. Independent-review handoff notes.
8. Open questions, risks and dependencies.
9. Commit SHA and read-back verification.
10. Bilingual parity status and Chinese/English paths (or approved STALE exception).
11. Honest final status: IMPLEMENTED / VERIFIED / BLOCKED / PARTIAL.

## 3. Prompt versioning rules / 提示词版本规则

- Use immutable prompt versions: `prompt-v1.md`, `prompt-v2.md`, etc.
- Compute SHA-256 for each approved prompt file and store it in the manifest.
- Any material change to scope, acceptance criteria, authority, dependencies or procedure requires a new version.
- A correction to spelling that cannot change interpretation may be recorded as a non-semantic edit, but the stored artifact and hash must still be updated before execution.
- Record which version was actually used by each AI run.
- Never overwrite a prompt version that has already been executed.
- If a run used an unrecorded conversational clarification, append it as a dated run addendum and assess whether a new prompt version is required.

## 4. Required evidence bundle / 必需证据包

Each completed implementation task should contain, as applicable:

- `manifest.yaml` — task identity and status;
- `prompt-vN.md` — exact executed instruction;
- `prompt.sha256` — prompt integrity digest;
- `implementation-report.md` — author report;
- `test-report.md` — reproducible checks;
- `review-report.md` — independent review;
- `decision-records/` — approved material decisions;
- `integration-report.md` — cross-owner acceptance;
- links to PR, commits and CI runs.

## 5. Suggested repository layout / 建议目录

```text
14-ai-development/
  README.md
  ai-development-standard.md
  iteration-lifecycle.md
  prompt-and-evidence-template.md
  work-items/
    INDEX.md
    AID-YYYY-NNN/
      manifest.yaml
      prompt-v1.md
      prompt.sha256
      implementation-report.md
      test-report.md
      review-report.md
      decision-records/
```

For a multi-owner parent task, use one parent folder with child work items or explicit Owner-specific child IDs. Keep each prompt and evidence bundle immutable and linkable. Do not store secrets, credentials, private user data or raw sensitive production data in prompts or reports.
