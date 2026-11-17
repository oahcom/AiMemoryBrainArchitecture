# DOMAIN-REALITY-001-B — Canonical Domain Model Research
# DOMAIN-REALITY-001-B — 规范领域模型研究

- Owner / 负责人: B — Principal Domain Model & Canonical Semantics Authority
- Status / 状态: IN_PROGRESS — B0 PARTIAL / NOT PASSED; no canonical freeze
- Branch / 分支: `research/domain-reality-001-b`
- Historical research ancestor / 历史研究祖先: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Current main HEAD at 2026-11-17 audit / 本次审计时 main HEAD: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- Latest currentness addendum / 最新时效性补充: `baseline-currentness-and-owner-source-audit.md`
- Research date / 研究日期: 2026-11-17

## 1. Purpose / 目的

This work establishes a minimal, complete, explicit, and verifiable canonical domain model for AI Memory Brain. A currentness/source-audit supplement and official-reference validation supplement were added after the first baseline pass; see those files for newer Owner heads and exact external source review. It audits actual repository contracts before proposing semantic changes. It does not replace Owner-local authority or decide physical implementation.

本研究为 AI Memory Brain 建立最小、完整、明确且可验证的规范领域模型。必须先审计仓库真实契约，再提出语义变更；不得取代各 Owner 的局部权威，也不决定物理实现。

## 2. Governance boundary / 治理边界

B owns shared domain meaning, canonical vocabulary, domain identity, relationships, temporal/evidence semantics, and cross-module semantic consistency. D owns canonical Memory lifecycle and Forget execution semantics; E compiler production semantics; F runtime/retrieval; G Context/ContextVersion/ChangeSet; H protocol semantics; I security identity, authorization and governance; Storage owns persistence/consistency realization; A owns system integration and contract registration.

B 负责共享领域含义、规范词汇、领域身份、关系、时间/证据语义及跨模块一致性。D 负责规范 Memory 生命周期与 Forget 执行语义；E 负责 Compiler 生产语义；F 负责 Runtime/检索；G 负责 Context/ContextVersion/ChangeSet；H 负责协议语义；I 负责安全身份、授权和治理；Storage 负责持久化/一致性实现；A 负责系统集成和契约注册。

No B document silently supersedes an Owner-owned contract. Conflicts are recorded and routed to the correct decision authority. No implementation, production activation, schema freeze, or merge authorization is implied.

B 文档不得静默取代其他 Owner 的权威契约。冲突必须登记并交由正确决策权威处理。本研究不代表实现、生产启用、Schema 冻结或合并授权。

## 3. Work plan and gates / 工作阶段与门禁

| Gate | Exit condition / 退出条件 | Status |
|---|---|---|
| B0 | Actual repository baseline, exact source pins, relevant PRs/issues and authority documents verified / 真实仓库基线、精确来源 Pin、相关 PR/Issue 与权威文档已核验 | PARTIAL |
| B1 | Entity inventory classified; duplication and omissions assessed / 实体清单分类，重复与遗漏完成评估 | IN PROGRESS — candidate inventory + complexity assessment published |
| B2 | Identity, state, temporal, evidence, provenance and relationships reconciled / 身份、状态、时间、证据、溯源与关系完成协调 | IN PROGRESS — candidate identity/state/temporal/relationship semantics published; owner reconciliation open |
| B3 | A/C/D/E/F/G/H/I/Storage/Testing cross-owner matrix and conflict register / 跨 Owner 矩阵及冲突登记完成 | NOT PASSED — first-pass matrix and conflict register published; owner acceptances open |
| B4 | Invariants, schemas, fixtures and validation specifications consistent / 不变量、Schema、Fixtures 与验证规范一致 | NOT READY — invariant/test specs published; schemas/tests intentionally not frozen or run |
| B5 | GitHub commits, PR, exact readback and Blob verification / GitHub 提交、PR、精确读回与 Blob 核验完成 | IN PROGRESS — draft PR #55 created; final inventory/readback pending |
| B6 | Truly separate independent review and governance disposition / 真正独立审查与治理裁决完成 | INDEPENDENT_REVIEW_PENDING |

## 4. Required deliverables / 必需交付物

1. README.md
2. existing-domain-model-baseline.md
3. canonical-domain-entity-inventory.md
4. canonical-identity-semantics.md
5. canonical-state-semantics.md
6. canonical-temporal-evidence-semantics.md
7. canonical-domain-relationships.md
8. domain-model-complexity-assessment.md
9. mature-domain-model-research.md
10. cross-owner-canonical-semantics-matrix.md
11. domain-semantics-conflict-register.md
12. canonical-domain-invariants.md
13. canonical-domain-glossary.md
14. canonical-domain-model.md
15. domain-model-decision-record.md
16. validation/ (schemas, fixtures, tests and validation notes)
17. evidence/ (source index and external research evidence)

Every normative deliverable must contain full Chinese and English semantics in the same file/change set. Unresolved statements remain OPEN, CANDIDATE, TO_VALIDATE or DEFERRED.

每项规范交付物必须在同一文件/变更集中提供完整中英文语义。未决事项必须保留 OPEN、CANDIDATE、TO_VALIDATE 或 DEFERRED 状态。

## 5. Current execution status / 当前执行状态

Published on this branch so far / 本分支已发布：
- existing-domain-model-baseline.md
- baseline-currentness-and-owner-source-audit.md
- canonical-domain-entity-inventory.md
- canonical-identity-semantics.md
- canonical-state-semantics.md
- canonical-temporal-evidence-semantics.md
- canonical-domain-relationships.md
- domain-model-complexity-assessment.md
- mature-domain-model-research.md
- cross-owner-canonical-semantics-matrix.md
- domain-semantics-conflict-register.md
- canonical-domain-invariants.md
- canonical-domain-glossary.md
- canonical-domain-model.md
- domain-model-decision-record.md
- validation/README.md
- evidence/README.md
- evidence/official-reference-validation.md
- evidence/official-reference-validation.md
- baseline-currentness-and-owner-source-audit.md

Remaining work includes completion of A and Testing/Quality source inventory, full exact-version PR/Issue diff audit, explicit relationship and state owner acceptance, schema/fixture design after semantic closure, final readback, and independent review. / 剩余工作包括补齐 A 与 Testing/Quality 源清单、完整精确版本 PR/Issue Diff 审计、关系与状态的 Owner 明确验收、语义闭合后的 Schema/Fixture 设计、最终读回及独立审查。

The actual `main` baseline is pinned in the baseline report. The repository is an architecture-definition repository; README explicitly says implementation has not started by design. The existing B branch is `session-b-domain-model-phase3`; it is not the requested research branch and its Scope/Permission source Blob differs from current main. The research branch's historical merge-base is `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; current main later advanced to `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`. The branch is therefore historically based on the former, not the latter. Current main and this research branch are divergent; PR #55 remains Draft and no merge/rebase is requested.

真实 `main` 基线已在基线报告中 Pin。仓库是架构定义仓库；README 明确说明按设计尚未开始实现。已有 B 分支为 `session-b-domain-model-phase3`，它不是本次研究分支，且其 Scope/Permission 源 Blob 与当前 main 不同。研究分支的历史 Merge Base 为 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；当前 main 后续推进至 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。因此该分支基于前者，而非后者。当前 main 与研究分支存在分叉；PR #55 保持 Draft，不请求合并或 Rebase。

## 6. Stop conditions / 停止条件

Any unresolved identity collision, contradictory state meaning, unowned lifecycle transition, cross-tenant reference ambiguity, Forget/Deletion/Visibility contradiction, or incompatible temporal definition blocks the affected normative contract. Owner decisions are never inferred from silence, summaries, or another Owner's synthesis.

任何未解决的身份冲突、互斥状态含义、无权威归属的生命周期转换、跨 Tenant 引用歧义、Forget/Deletion/Visibility 矛盾或不兼容时间定义，均阻塞受影响的规范契约。不得从沉默、摘要或其他 Owner 的综合意见推断 Owner 决策。


## 7. Branch isolation correction / 分支隔离纠正记录

A subset of initial create-file operations landed on main because the branch parameter was omitted. The exact affected research files were copied to this isolated branch, then removed from main through explicit delete commits. All 13 affected main paths were subsequently checked and returned NOT_FOUND; the branch contains the 19-file research package. Main was not rewritten and historical commits remain auditable. This correction is recorded transparently; it is not treated as a clean initial write.

部分初始 create-file 操作因遗漏 branch 参数而写入 main。受影响的研究文件已复制到本隔离分支，再通过明确的删除提交从 main 移除。随后对 13 个受影响的 main 路径逐一核验，均返回 NOT_FOUND；研究分支包含完整 17 个文件。main 未被重写，历史提交仍可审计。本纠正过程如实记录，不将其描述为从一开始就正确隔离。

## 7. Continued work — 2026-11-17 / 继续工作 — 2026-11-17

- Added `baseline-currentness-and-owner-source-audit.md`: refreshed current-main and selected Owner source snapshots; B0 remains PARTIAL.
- Added `baseline-owner-branch-snapshot-errata.md`: corrects older Owner branch-tip rows using the later Phase 3.8 snapshot in the cross-owner matrix.
- Added `fact-claim-identity-adr.md`: explicit alternatives and a candidate recommendation; no Fact/Claim or Claim identity decision is claimed.
- Added `evidence/official-reference-validation.md`: official domain-modeling reference survey; research patterns are not project contracts.
- PR #55 remains Open / Draft. The branch is not merged and no architecture/schema freeze is requested.

Bilingual coverage and exact readback are still required after each subsequent write. B0 is PARTIAL / NOT PASSED; B2/B3 remain OPEN; B4 is NOT READY; B6 is pending truly independent review.

- 新增 `baseline-currentness-and-owner-source-audit.md`：刷新 current-main 和部分 Owner 源快照；B0 仍 PARTIAL。
- 新增 `baseline-owner-branch-snapshot-errata.md`：使用跨 Owner 矩阵中较新的 Phase 3.8 快照更正旧 Owner 分支 Tip。
- 新增 `fact-claim-identity-adr.md`：列出明确备选方案及候选建议；不宣称已决定 Fact/Claim 或 Claim 身份。
- 新增 `evidence/official-reference-validation.md`：官方领域建模参考研究；外部产品模式不是项目契约。
- PR #55 仍为 Open / Draft。研究分支未合并，也未请求架构/Schema 冻结。

每次后续写入后仍须完成双语覆盖和精确读回。B0 为 PARTIAL / NOT PASSED；B2/B3 仍 OPEN；B4 为 NOT READY；B6 等待真正独立审查。
