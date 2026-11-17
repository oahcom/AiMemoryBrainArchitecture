# DOMAIN-REALITY-001-B — Post-Merge Currentness & Governance Reconciliation
# DOMAIN-REALITY-001-B — 合并后当前性与治理状态核对

- Audit time / 审计时间: 2026-11-18 05:22 Asia/Singapore
- Repository / 仓库: `oahcom/AiMemoryBrainArchitecture`
- Scope / 范围: PR #55 merge event, current main tree, review disposition and unchanged B research gates
- Authority / 权限: factual repository-state reconciliation only; no architecture approval

## 1. Verified PR state / 已核实 PR 状态

GitHub currently reports PR #55 as **CLOSED / MERGED**, merged at `2026-11-17T19:12:47Z` by `oahcom`.

- PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/55
- Head branch: `research/domain-reality-001-b`
- Merged head SHA: `e9554bd36bb2848441965bcf587413e7280482ed`
- Recorded base SHA: `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`
- Merge commit: `07ee5702cab0d12d6136fe3c024bde9a7af44a97`
- Merge commit parent: `22e64ef2df60b4c2b022885aa3a50f12490b8f36`
- Merge commit reported stats: 5,357 additions, 0 deletions.
- The merge commit is an ancestor of current `main`; compare `07ee5702...` → `main` reports 23 commits ahead, 0 behind.

PR #55 is therefore not Open/Draft. Earlier statements in this package describing it as Open/Draft are historical snapshots and are superseded by this section.

GitHub 当前将 PR #55 报告为 **CLOSED / MERGED**，合并时间为 `2026-11-17T19:12:47Z`，操作者为 `oahcom`。

- PR：上方链接
- Head 分支：`research/domain-reality-001-b`
- 合并时 Head SHA：`e9554bd36bb2848441965bcf587413e7280482ed`
- PR 记录的 Base SHA：`052715487bd5e95aab8b9bb386c162cf2d6bf6d3`
- Merge Commit：`07ee5702cab0d12d6136fe3c024bde9a7af44a97`
- Merge Commit Parent：`22e64ef2df60b4c2b022885aa3a50f12490b8f36`
- Merge Commit 统计：新增 5,357 行，删除 0 行。
- 该 Merge Commit 是当前 `main` 的祖先；从 `07ee5702...` 比较到 `main` 为领先 23 个 Commit、落后 0 个。

因此 PR #55 已不是 Open/Draft。本研究包此前将其描述为 Open/Draft 的内容均属于历史快照，由本节取代。

## 2. Current main and content presence / 当前 main 与内容存在性

At audit time, the live `main` commit is:

- Main HEAD: `a2b8babb1cacfcfbcd590b147bdf34ce162944c2`
- Tree: `16df623723013aa615e9a51765a444835d4b9cad`
- Latest observed main commit message: `docs(recovery): audit closed-unmerged PR content disposition (#118)`

A recursive read of that exact main tree confirms that `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/` **is present**, including the README, all 16 core deliverables, and the supplemental currentness, bilingual-parity, Fact/Claim ADR and official-reference files. The earlier claim that this package had zero paths on main is no longer true after PR #55 was merged.

审计时实时 `main`：

- Main HEAD：`a2b8babb1cacfcfbcd590b147bdf34ce162944c2`
- Tree：`16df623723013aa615e9a51765a444835d4b9cad`
- 最新观察到的 main 提交说明：`docs(recovery): audit closed-unmerged PR content disposition (#118)`

对该精确 Main Tree 的递归读取确认，`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/` **当前存在**，包含 README、全部 16 项核心交付物，以及当前性审计、双语对等、Fact/Claim ADR 和官方来源补充文件。PR #55 合并后，此前“main 中该研究包路径数为 0”的说法已不再成立。

## 3. Review disposition / 审查状态

The current PR review listing contains 10 review records, and all 10 have state `COMMENTED`. There are **zero APPROVED review records** in that listing. The comments include A-B5 findings and latest-head rechecks; they are not approvals and do not close the cited findings.

当前 PR Review 列表包含 10 条记录，状态全部为 `COMMENTED`；其中 **没有 APPROVED 记录**。评论包括 A-B5 发现及最新 Head 复核；评论不等于批准，也不会自动关闭所列发现。

The merge event is a repository fact. It is not evidence of:
- independent B5 bilingual semantic acceptance;
- B6 independent review completion;
- Architecture Governance approval of Fact/Claim Option A;
- D/E/F/G acceptance of the B Fact/Claim representation;
- canonical/schema freeze, implementation authorization or production readiness.

合并事件是仓库事实，但不能证明：
- B5 双语语义独立验收完成；
- B6 独立审查完成；
- Architecture Governance 已批准 Fact/Claim Option A；
- D/E/F/G 已接受 B 的 Fact/Claim 表示；
- 规范/Schema 已冻结、实现已获授权或系统已具备生产就绪性。

## 4. B research gates remain unchanged / B 研究门禁保持不变

| Gate | Status | Meaning |
|---|---|---|
| B0 | PARTIAL / NOT PASSED | Source/PR/Issue audit is not exhaustive |
| B1 | IN PROGRESS | Entity inventory and complexity review still require Owner confirmation |
| B2 | IN PROGRESS / NOT PASSED | Fact/Claim and Claim identity decisions remain ADR-blocked |
| B3 | NOT PASSED | Cross-owner acceptance and ingress/Applied/Forget/Storage evidence remain open |
| B4 | NOT READY | No final approved schema/fixtures; executable validation not authorized or run |
| B5 | BLOCKED / NOT PASSED | Independent clause-by-clause bilingual semantic review remains pending |
| B6 | INDEPENDENT_REVIEW_PENDING | A separate independent review and governance disposition remain outstanding |

| 门禁 | 状态 | 含义 |
|---|---|---|
| B0 | PARTIAL / NOT PASSED | 来源/PR/Issue 审计尚未穷尽 |
| B1 | IN PROGRESS | 实体清单和复杂度审查仍需 Owner 确认 |
| B2 | IN PROGRESS / NOT PASSED | Fact/Claim 与 Claim 身份决策仍 ADR 阻塞 |
| B3 | NOT PASSED | 跨 Owner 验收及 Ingress/Applied/Forget/Storage 证据仍开放 |
| B4 | NOT READY | 没有最终批准的 Schema/Fixtures；未授权或运行可执行验证 |
| B5 | BLOCKED / NOT PASSED | 独立逐条双语语义审查仍待完成 |
| B6 | INDEPENDENT_REVIEW_PENDING | 仍需独立审查及治理裁决 |

## 5. Fact/Claim decision boundary / Fact/Claim 决策边界

The current B Owner preference remains **B Fact/Claim Option A**: a separate Claim proposition thread and independently addressable Fact attestation object. It remains CANDIDATE / ADR-BLOCKED / NOT APPROVED because no named Architecture Governance authority, approver, timestamp or approval record has been verified.

Do not conflate this with **D Claim Identity Option A**, which means stable Claim ID plus immutable ClaimRevision. These are separate decisions. D/E/F/G source alignment does not constitute acceptance of B's Fact/Claim Option A. No Claim/Fact/ClaimRevision/ConflictSet schema, DDL, API or wire contract is frozen.

当前 B Owner 仍优先推荐 **B Fact/Claim Option A**：独立 Claim 命题线程与可独立寻址的 Fact Attestation 对象。但该方案仍为 CANDIDATE / ADR-BLOCKED / NOT APPROVED，因为尚未核实具名 Architecture Governance 权威、批准人、时间戳或批准记录。

不得将其与 **D Claim Identity Option A** 混淆；后者指稳定 Claim ID + 不可变 ClaimRevision。这是不同决策。D/E/F/G 来源语义对齐不等于接受 B 的 Fact/Claim Option A。不得冻结 Claim/Fact/ClaimRevision/ConflictSet Schema、DDL、API 或 Wire 契约。

## 6. Execution boundary / 执行边界

This addendum records the already-observed merge and corrects stale status claims. It does not attempt to reverse the merge or write to `main`. Subsequent author-side corrections remain isolated on `research/domain-reality-001-b` and require a new review path. No schema, implementation or production activation work is authorized by this addendum.

本补充文件记录已发生的合并并纠正过期状态，不尝试回滚合并，也不写入 `main`。后续作者侧修订继续隔离在 `research/domain-reality-001-b`，并需通过新的审查路径交付。本补充文件不授权 Schema、实现或生产启用工作。
