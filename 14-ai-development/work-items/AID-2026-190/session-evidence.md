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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the contract as received, the environment it ran in, and the commands whose output is quoted in evidence.md. No platform session identifier is available, so the session identity is recorded as NOT_RECORDED rather than inferred."
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
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Evidence — AID-2026-190

## Session role / use case

Correction worker inside a dispatched repair contract. The worker was dispatched to run two
task files end to end: append a `## Correction (2026-11-27)` section to
`GOV-REV-2026-11-21-PR425-001.md` for ten pasted test cases that the head tree does not
contain, and to `AID-2026-113/restore-evidence.md` for new-blob identities that do not
resolve, in all three renditions of each record, without editing any historical table or
any original author declaration.

The role performed was measurement and appended correction. The worker verified each
premise before writing it, and in two places the measurement contradicted the dispatched
text: the ten cases do exist, on an unmerged branch, and the tables carry fifteen new-blob
cells rather than thirteen. Both divergences were recorded as measured rather than as
dispatched, with the branch and the count named.

## Actual AI input

The dispatched contract arrived as two files, captured verbatim in `prompt-v1.md`
(8190 bytes, SHA-256 `ee7c6c2de36dd9b36c7333309a6fe0e97b70bde0c7ad229fe5e705ab4f619543`),
and instructed the assistant to:

- read `fix-brief-common.md` and `unit-refs.md` and execute them end to end without
  asking questions;
- work only in the worktree `D:\code\wt-refs` on branch
  `fix/2026-11-27-refs-fake-evidence`, and never touch the shared clone
  `D:\code\AiMemoryBrainArchitecture`;
- fetch and merge `origin/main` before opening the pull request; use
  `merge_method: merge`, wait for 16 completed successful required contexts with branch
  behind equal to 0, and verify every changed blob against `origin/main` after the merge;
- use the `gho_`-prefixed token from `%USERPROFILE%\.git-credentials` as a bearer token
  without printing it, and allocate an unused `AID-2026-<NNN>` number after checking
  pull-request titles, branches and the tree;
- for `GOV-REV-2026-11-21-PR425-001`: keep the historical register intact, append
  `## Correction (2026-11-27)` listing each of the ten cases as absent from the head tree,
  with the `git grep` evidence actually executed, and mark the section's conclusion
  `NOT_VERIFIABLE_FROM_REPOSITORY`;
- for `AID-2026-113`: keep the original table intact, append `## Correction` giving the
  real blobs at `origin/main` for each of the listed paths, and show that the recorded
  SHAs do not resolve via `git cat-file -t`;
- append in all three renditions (canonical, EN, ZH-CN) with consistent structure, leave
  `verification_status` untouched, and state in the appended section that the original
  declaration does not hold;
- make no change to any historical table, any blob, and any content deletion, and never
  re-declare either record as Verified.

The environment constraints stated with the contract were that `PYTHONUTF8=1` is required
on this host because the console codepage breaks decoding of captured `git` output, and
that block-style YAML is required because `_scalar()` in
`scripts/check_document_management.py` rejects inline `{}`.

The contract text is pinned in `prompt-v1.md`; no prompt-library registration exists for
it, so `prompt_status` is `NOT_RECORDED` and the captured text carries
`executed_prompt_provenance: NOT_VERIFIED`.

## AI-visible output

The assistant reported, and the branch content confirms:

- `git ls-tree -r --name-only HEAD -- 04-memory-compiler/reference-model` returns zero
  lines; `04-memory-compiler` holds seven files at HEAD and no `reference-model/`; ten
  separate `git grep -c -F "<case>" HEAD -- "*.py"` runs returned nothing with exit 1, and
  `git grep -l` found the names only in the register, its two mirrors and
  `TEST-DRAFT-2026-11-21-PR425-M3.md`;
- the ten names do exist at `8142b1ca`, reachable only from
  `refs/heads/owner-e/gap-01-memory-compiler-contract`; extracting that path with
  `git archive` and running the register's discovery pattern gave
  `Ran 10 tests in 0.001s / OK / exit 0`, so the correction records a reachability defect
  rather than asserting fabrication, and names the branch;
- all fifteen new-blob SHAs in `restore-evidence.md` fail `git cat-file -t` with
  `fatal: git cat-file: could not get object info` (exit 128), none equals
  `origin/main:<path>`, and none equals `9142698f:<path>`; the seventeen source, original
  and orphan blobs in the same tables do resolve, and the five Canonical source blobs equal
  `1908ce4d:<path>`, so the correction confines the defect to the new-blob column;
- the dispatched count of thirteen new-blob identities was measured as fifteen (5 + 10);
  the correction lists all fifteen and the manifest records the divergence;
- six files were modified and every one by appending only: 91 added / 0 removed lines in
  each of the three `GOV-REV-2026-11-21-PR425-001.md` renditions, 70 added / 0 removed in
  each of the three `restore-evidence.md` renditions; no `verification_status`,
  `last_verified_date` or `last_verification_note` value was touched in either record;
- no file under `04-memory-compiler/`, `05-memory-runtime/`, `scripts/`, `.github/` or
  `00-governance/` was modified.

## Session reference status

NOT_RECORDED

No platform session identifier is available to this session, so `implementing_ai_session`
names the executing model (`opencode-go/deepseek-v4.1-flash`) rather than an authenticated
account, and the prompt snapshot carries `executed_prompt_provenance: NOT_VERIFIED`.
