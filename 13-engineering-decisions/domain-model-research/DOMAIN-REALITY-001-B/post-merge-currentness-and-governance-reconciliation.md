# DOMAIN-REALITY-001-B — Post-Merge Currentness & Governance Reconciliation
# DOMAIN-REALITY-001-B — 合并后当前性与治理状态核对

- Audit time / 审计时间: 2026-11-18 05:22 Asia/Singapore
- Repository / 仓库: `oahcom/AiMemoryBrainArchitecture`
- Scope / 范围: PR #55 merge event, current main tree, review disposition and B research gates
- Authority / 权限: factual repository-state reconciliation only; no architecture approval

## 1. Verified PR state / 已核实 PR 状态

GitHub reports PR #55 as **CLOSED / MERGED**, merged at `2026-11-17T19:12:47Z` by `oahcom`.

- PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/55
- Head branch: `research/domain-reality-001-b`
- Merged head SHA: `e9554bd36bb2848441965bcf587413e7280482ed`
- Recorded base SHA: `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`
- Merge commit: `07ee5702cab0d12d6136fe3c024bde9a7af44a97`
- Merge commit parent: `22e64ef2df60b4c2b022885aa3a50f12490b8f36`
- Merge commit reported stats: 5,357 additions, 0 deletions.
- The merge commit is an ancestor of current `main`; compare merge commit → `main` reports 23 commits ahead, 0 behind.
- The merge commit has one parent and the PR branch head is not an ancestor of main; this is a squash-style content integration, not preservation of the source branch ancestry.

GitHub 当前将 PR #55 报告为 **CLOSED / MERGED**，合并时间为 `2026-11-17T19:12:47Z`，操作者为 `oahcom`。

- PR、Head 分支、合并时 Head SHA、Base SHA、Merge Commit、Parent 和统计数据如上。
- 该 Merge Commit 是当前 `main` 的祖先；从 Merge Commit 比较到 `main` 为领先 23 个 Commit、落后 0 个。
- Merge Commit 只有一个 Parent，原 PR 分支 Head 并非 main 的祖先；这是类似 Squash 的内容集成，并未保留源分支的提交祖先关系。

Earlier Open/Draft statements are historical snapshots and are superseded by this section.

此前 Open/Draft 状态均为历史快照，由本节取代。

## 2. Current main and content presence / 当前 main 与内容存在性

At audit time:

- Main HEAD: `a2b8babb1cacfcfbcd590b147bdf34ce162944c2`
- Tree: `16df623723013aa615e9a51765a444835d4b9cad`
- Latest observed commit message: `docs(recovery): audit closed-unmerged PR content disposition (#118)`

A recursive read of that exact main tree confirms that `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/` is present, including the README, all 16 core deliverables, and supplemental currentness, bilingual-parity, Fact/Claim ADR and official-reference files. Earlier claims that this package had zero paths on main are superseded.

审计时 main HEAD 为 `a2b8babb1cacfcfbcd590b147bdf34ce162944c2`，Tree 为 `16df623723013aa615e9a51765a444835d4b9cad`。对该 Tree 的递归读取确认完整研究包存在于 main，包括 README、16 项核心交付物及当前性、双语对等、Fact/Claim ADR 和官方来源补充文件。此前声称 main 中该研究包路径数为 0 的记录已被取代。

## 3. Review disposition / 审查状态

The PR review listing contains 10 records, all with state `COMMENTED`, and zero `APPROVED` records. Comments include A-B5 findings and latest-head rechecks; they are not approvals and do not close the cited findings.

PR Review 列表包含 10 条记录，全部为 `COMMENTED`，没有 `APPROVED` 记录。评论包括 A-B5 发现及最新 Head 复核；评论不等于批准，也不会自动关闭所列发现。

The merge event does not establish independent B5 bilingual semantic acceptance, B6 independent review completion, Architecture Governance approval, D/E/F/G acceptance of B's Fact/Claim representation, canonical/schema freeze, implementation authorization or production readiness.

该合并事件不能证明 B5 双语语义独立验收、B6 独立审查、Architecture Governance 批准、D/E/F/G 接受 B 的 Fact/Claim 表示、规范/Schema 冻结、实现授权或生产就绪。

## 4. B research gates remain unchanged / B 研究门禁保持不变

| Gate | Status | Meaning |
|---|---|---|
| B0 | PARTIAL / NOT PASSED | Source/PR/Issue audit is not exhaustive |
| B1 | IN PROGRESS | Entity inventory and complexity review still require Owner confirmation |
| B2 | IN PROGRESS / NOT PASSED | Fact/Claim and Claim identity decisions remain ADR-blocked |
| B3 | NOT PASSED | Cross-owner acceptance and ingress/Applied/Forget/Storage evidence remain open |
| B4 | NOT READY | No final approved schema/fixtures; executable validation not authorized or run |
| B5 | BLOCKED / NOT PASSED | Independent clause-by-clause bilingual semantic review remains pending |
| B6 | INDEPENDENT_REVIEW_PENDING | Separate independent review and governance disposition remain outstanding |

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

B's current preferred candidate remains **B Fact/Claim Option A**: a separate Claim proposition thread and independently addressable Fact attestation object. It remains CANDIDATE / ADR-BLOCKED / NOT APPROVED; no named Architecture Governance authority, approver, timestamp or approval record has been verified.

Do not conflate this with **D Claim Identity Option A**: stable Claim ID plus immutable ClaimRevision. These are separate decisions. D/E/F/G source alignment does not constitute acceptance of B's Fact/Claim Option A. No Claim/Fact/ClaimRevision/ConflictSet schema, DDL, API or wire contract is frozen.

B 当前优先候选仍为 **B Fact/Claim Option A**：独立 Claim 命题线程与可独立寻址的 Fact Attestation 对象。该方案仍为 CANDIDATE / ADR-BLOCKED / NOT APPROVED；未核实具名 Architecture Governance 权威、批准人、时间戳或批准记录。

不得将其与 **D Claim Identity Option A**（稳定 Claim ID + 不可变 ClaimRevision）混淆。两者是不同决策。D/E/F/G 来源对齐不代表接受 B 的 Fact/Claim Option A。不得冻结 Claim/Fact/ClaimRevision/ConflictSet Schema、DDL、API 或 Wire 契约。

## 6. Execution boundary / 执行边界

This addendum records the already-observed merge and corrects stale status claims. It does not reverse the merge or write to main. Subsequent author-side corrections remain on a new branch based on current main and require a separate review path. No schema, implementation or production activation work is authorized.

本补充文件记录已发生的合并并纠正过期状态，不回滚合并，也不直接写入 main。后续作者侧修订在基于当前 main 的新分支中进行，并需单独审查。本补充文件不授权 Schema、实现或生产启用工作。


## 7. Subsequent PR #120 merge / 后续 PR #120 合并

A later documentation-only follow-up, PR #120, was merged at `2026-11-17T21:29:04Z` by `oahcom`. Merge commit: `6c325804027b88de1014ab3364cdda7e0c023ba6`; merged head: `069984b5c3915334d6fa2d3ec409d4c7e36fe549`. Main was subsequently observed at `ab1fa87d74ca4a632155aa19569533ea560109d5`. PR #120 incorporated the post-PR-55 status corrections. The later latest cross-owner source refresh is a separate, unmerged follow-up and is not included in PR #120.

后续仅文档类 PR #120 于 `2026-11-17T21:29:04Z` 由 `oahcom` 合并。Merge Commit：`6c325804027b88de1014ab3364cdda7e0c023ba6`；合并时 Head：`069984b5c3915334d6fa2d3ec409d4c7e36fe549`。此后观察到的 main 为 `ab1fa87d74ca4a632155aa19569533ea560109d5`。PR #120 纳入 PR #55 后的状态纠偏。后续最新跨 Owner 来源刷新是独立、尚未合并的后续工作，不包含在 PR #120 中。


## 8. Latest cross-owner source refresh — 2026-11-18

The subsequent DOMAIN-REALITY-001-B source refresh now records C `461dd616209657c3bf485871bdbc2a1b6a652d40`, G `07a84a5ef5b331180bee47f8a60ef16c2918a700`, and H `b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9` as current branch heads. The C and G review artifacts are delegated role reviews, not independent human Owner approvals. H's current Applied Delivery Evidence suite has 29 test methods; the cited 26/26 CI result is for earlier H head `9fb2097905ef653b3a2048ac5f6804fc94178d8d`, not the current H head. H-ADE-001/002/003 have candidate reference-code coverage; production C/I/D authority, H durable replay, G persistence/restore and Full Applied remain open.

后续 DOMAIN-REALITY-001-B 来源刷新记录 C `461dd616209657c3bf485871bdbc2a1b6a652d40`、G `07a84a5ef5b331180bee47f8a60ef16c2918a700`、H `b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9` 为当前分支 Head。C/G 复审属于委派角色审查，不是独立人类 Owner 批准。H 当前 Applied Delivery Evidence 套件包含 29 个测试方法；引用的 26/26 CI 结果针对旧 H Head `9fb2097905ef653b3a2048ac5f6804fc94178d8d`，不是当前 Head。H-ADE-001/002/003 已有候选参考代码覆盖；生产 C/I/D 权威、H Durable Replay、G Persistence/Restore 和 Full Applied 仍开放。


## Post-PR #131 exact-head CI evidence correction — 2026-11-18 / PR #131 合并后精确 Head CI 证据修正

The statements above that the H 29-test suite had no exact-head CI result were accurate at the time of the earlier source refresh, but are now superseded for the bounded reference-candidate test run. PR #131 Head `40c52edb97f1a103bb92b89f5a68bd895565bb7b` triggered GitHub Actions run [#44182801145](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44182801145). Job `applied-delivery-evidence` completed SUCCESS, including the step `Run Applied Delivery Evidence schema and semantic conformance tests`; the log records **Ran 29 tests ... OK**. This proves the 29-method reference suite ran successfully on PR #131's exact Head. It does not prove that the H Owner branch Head itself was directly tested, nor does it establish independent Owner approval, production cryptographic trust, live C Owner Ledger resolution, real I/D authority-ledger wiring, durable H replay, G Applied persistence/restore, multi-replica recovery, Full Applied, or production readiness. The older 26/26 run #44180835412 remains evidence for its earlier H Head only.

此前关于 H 29 项测试没有精确 Head CI 结果的表述，在当时来源刷新时是准确的；但对于有界参考候选测试运行而言，现已被后续证据取代。PR #131 的 Head `40c52edb97f1a103bb92b89f5a68bd895565bb7b` 触发 GitHub Actions Run [#44182801145](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44182801145)。Job `applied-delivery-evidence` 成功完成，其中 `Run Applied Delivery Evidence schema and semantic conformance tests` 步骤成功；日志明确记录 **Ran 29 tests ... OK**。这证明 29 项参考套件已在 PR #131 的精确 Head 上成功运行。但这不证明 H Owner 分支 Head 本身直接经过测试，也不代表独立 Owner 批准、生产密码学信任、真实 C Owner Ledger 解析、真实 I/D 权威账本接线、H Durable Replay、G Applied Persistence/Restore、多副本恢复、Full Applied 或生产就绪。较早的 26/26 Run #44180835412 仍只适用于其对应的旧 H Head。
