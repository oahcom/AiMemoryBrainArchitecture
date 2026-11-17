# PR-RECOVERY-002 — Closed PR Content Recovery Audit
# PR 关闭未合并内容回收审计

- Audit date: 2026-11-18 (Asia/Singapore)
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Scope: all 16 pull requests found closed and unmerged in the live repository snapshot
- Purpose: determine whether each closed PR's useful content is preserved, superseded, intentionally rejected, or still requires recovery
- This is a repository-content audit. It does not approve architecture, close Issues/Gates, or grant production authorization.

## Executive result / 执行结论

The repository had **0 open PRs, 73 merged PRs, and 16 closed-unmerged PRs** at audit time (89 PRs total). The 16 closed-unmerged PRs were individually classified below.

No closed-unmerged PR was reopened or merged merely to change its status. The audit found no confirmed missing implementation or research artifact that should be restored as-is. Several PRs are explicitly rejected or superseded; the remaining content is present on main or on its intended Owner branch.

本次实时快照为 **0 个 Open PR、73 个已合并 PR、16 个关闭但未合并 PR**（共 89 个 PR）。下文逐项分类。没有为了改变状态而重新打开或合并旧 PR。未发现需要原样恢复的、已确认丢失的实现或研究成果。

## Per-PR disposition / 逐项裁定

| PR | Result | Evidence and disposition |
|---|---|---|
| #1 | PRESERVED ON MAIN | All 26 changed paths exist in current main. The Session G candidate package was subsequently published through #115 and #117. No re-merge needed. |
| #12 | VALIDATION-ONLY / ALREADY APPLIED TO OWNER BRANCH | Its one-line PostgreSQL version assertion adjustment is already present on target branch `session-storage-consistency-forget-atomicity-2026-11-16` (Blob `184e0507fd225ee18f321f3f1ce6a63f869b13f3`). The exact PR head check run “PostgreSQL 18.7 durable prepared-XID probe” completed SUCCESS. The PR explicitly requested no merge; the branch already contains the fix. |
| #23 | PRESERVED ON MAIN | All 12 changed paths exist in current main. Conflict-free AID-2026-001 governance artifacts were later published by #116. |
| #38 | REJECTED / HISTORICAL ONLY | PR description explicitly says API-key-based Owner Worker implementation is NOT APPROVED and must not be merged, deployed, or used as a design baseline. Preserve as historical audit evidence only. |
| #40 | REJECTED / HISTORICAL ONLY | PR description explicitly says Codex CLI / ChatGPT OAuth POC is NOT APPROVED and superseded by the ChatGPT ordinary-conversation execution direction. Preserve as historical audit evidence only. |
| #47 | SUPERSEDED BY LATER X ASSESSMENT | The earlier bilingual complexity assessment was replaced by the later X assessment published through #49 under `reviews/complexity/`. The old PR's exact paths are not present on main; the later assessment is the successor, not a byte-for-byte copy. |
| #48 | SUPERSEDED BY LATER R ASSESSMENT | The earlier R risk report was replaced by the later SYS-RISK-001 report published through #50 under `reviews/architecture/`. The old PR's exact path is not present on main; the later assessment is the successor, not a byte-for-byte copy. |
| #53 | SUPERSEDED / CONTENT PRESERVED | Its 20 bilingual architecture-authority deliverable paths are present in current main. Later corrected versions #57/#58 used the same deliverable set and corrected source provenance; the current main contains all 20 paths. |
| #57 | SUPERSEDED / CONTENT PRESERVED | Its 20 bilingual architecture-authority deliverable paths are present in current main. #58 is the clean-base successor version; do not merge the duplicate branch. |
| #58 | CONTENT PRESERVED ON MAIN | All 20 changed paths exist in current main. Its report keeps the overall outcome DEFERRED and architecture state ARCHITECTURE_NOT_READY; no Gate/freeze/production approval is implied. |
| #73 | CONTENT PRESERVED ON MAIN | All 17 changed paths exist in current main, including the owner-remediation record and two reference-model test files. #114 later published the three owner-remediation files as a focused current-source integration. No re-merge needed. |
| #80 | SUPERSEDED BY #84 | The closed PR contains only the bilingual workstream charter. The later architecture-breakthrough package #84 includes Forget model artifacts (`ForgetModel.tla`, `ForgetModel.cfg`) and associated research. The charter itself is not separately copied to main. |
| #81 | SUPERSEDED BY #86 | The closed PR contains only the bilingual workstream charter. The later Memory Operating System package #86 contains architecture alternatives, resource-manager contract, prototype and benchmark materials. The charter itself is not separately copied to main. |
| #82 | SUPERSEDED BY #85 | The closed PR contains only the bilingual workstream charter. The later Memory IR package #85 contains the compiler proposal, domain model, prototype implementation and sample experiences. The charter itself is not separately copied to main. |
| #96 | SUPERSEDED ON INTENDED OWNER BRANCH | Both changed H Owner artifacts are present on target branch `session-h-bmcp-protocol`. The PR body explicitly marks this recovery snapshot SUPERSEDED after the Owner branch advanced without deletions. Do not merge the stale recovery snapshot. |
| #97 | SUPERSEDED ON INTENDED OWNER BRANCH | Both changed C Owner artifacts are present on target branch `session-c-agent-integration-2026-11-16`. The PR body explicitly marks this recovery snapshot SUPERSEDED after the Owner branch advanced without deletions. Do not merge the stale recovery snapshot. |

## Evidence boundaries / 证据边界

1. “Present on main” means the exact changed path exists in the recursively fetched current main Git tree. It does not claim byte-identical content unless a Blob SHA was separately checked.
2. “Superseded” means a later successor artifact exists or the PR itself explicitly says so. It does not mean every sentence of the older report was copied verbatim.
3. PR #12's successful check is a single-node PostgreSQL capability probe. It is not evidence of replication/failover, production restore, hardware durability, or JF-10 closure.
4. PR #96/#97 preservation is checked against each PR's intended Owner target branch, not main. These artifacts must not be promoted to main without the respective Owner's integration path.
5. Rejected PR #38/#40 remain historical only. Their implementations must not be revived from these closed PRs.

## Follow-up / 后续

- Keep the repository's Open PR queue at zero; new work should enter through a fresh, scoped PR.
- Do not reopen #38/#40 or merge stale #96/#97 recovery snapshots.
- If the old #47/#48 or #80/#81/#82 charter text is later needed for provenance, recover it as an explicitly historical appendix, not as a competing current assessment.
- Continue tracking architecture readiness, Owner approvals, Gates, and production proof independently of PR closure counts.

