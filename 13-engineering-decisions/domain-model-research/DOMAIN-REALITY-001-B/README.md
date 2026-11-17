# DOMAIN-REALITY-001-B — Canonical Domain Model Research
# DOMAIN-REALITY-001-B — 规范领域模型研究

- Owner / 负责人: B — Principal Domain Model & Canonical Semantics Authority
- Status / 状态: IN_PROGRESS — B0 PARTIAL / NOT PASSED; no canonical freeze
- Branch / 分支: `research/domain-reality-001-b`
- Historical merge base / 历史合并基点: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Current main HEAD observed / 当前 main HEAD 观察值: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- Current research branch HEAD at this document revision / 本文档修订时研究分支 HEAD: `c35379b83edec457b1f7925203d369dfc5ef6c03` (this commit advances the branch; refresh PR metadata for the live tip)
- PR: #55 — Open / Draft; no merge requested
- Research date / 研究日期: 2026-11-17

## 1. Purpose / 目的

This work establishes a minimal, explicit and verifiable candidate canonical domain model for AI Memory Brain. It audits actual repository contracts and mature external domain-modeling references before proposing semantic changes. It does not replace Owner-local authority or decide physical implementation.

本研究为 AI Memory Brain 建立最小、明确、可验证的规范领域模型候选。提出语义变更前，必须审计仓库真实契约和成熟外部领域建模参考。不得取代各 Owner 的局部权威，也不决定物理实现。

## 2. Governance boundary / 治理边界

B owns shared domain meaning, canonical vocabulary, domain identity, relationships, temporal/evidence semantics, and cross-module semantic consistency. D owns canonical Memory lifecycle and Forget execution semantics; E compiler production semantics; F runtime/retrieval; G Context/ContextVersion/ChangeSet; H protocol semantics; I security identity, authorization and governance; Storage owns persistence/consistency realization; A owns system integration and contract registration.

B 负责共享领域含义、规范词汇、领域身份、关系、时间/证据语义及跨模块一致性。D 负责规范 Memory 生命周期与 Forget 执行语义；E 负责 Compiler 生产语义；F 负责 Runtime/检索；G 负责 Context/ContextVersion/ChangeSet；H 负责协议语义；I 负责安全身份、授权和治理；Storage 负责持久化/一致性实现；A 负责系统集成和契约注册。

No B document silently supersedes an Owner-owned contract. Conflicts are recorded and routed to the correct decision authority. No implementation, production activation, schema freeze, or merge authorization is implied.

B 文档不得静默取代其他 Owner 的权威契约。冲突必须登记并交由正确决策权威处理。本研究不代表实现、生产启用、Schema 冻结或合并授权。

## 3. Work plan and gates / 工作阶段与门禁

| Gate | Exit condition / 退出条件 | Status |
|---|---|---|
| B0 | Actual repository baseline, exact source pins, relevant PRs/issues and authority documents verified / 真实仓库基线、精确来源 Pin、相关 PR/Issue 与权威文档已核验 | PARTIAL / NOT PASSED |
| B1 | Entity inventory classified; duplication and omissions assessed / 实体清单分类，重复与遗漏完成评估 | IN PROGRESS — candidate inventory and complexity assessment published |
| B2 | Identity, state, temporal, evidence, provenance and relationships reconciled / 身份、状态、时间、证据、溯源与关系完成协调 | IN PROGRESS — Fact/Claim and Claim identity ADR remains a decision request |
| B3 | A/C/D/E/F/G/H/I/Storage/Testing cross-owner matrix and conflict register / 跨 Owner 矩阵及冲突登记完成 | NOT PASSED — owner acceptance and successor-pin reconciliation open |
| B4 | Invariants, schemas, fixtures and validation specifications consistent / 不变量、Schema、Fixtures 与验证规范一致 | NOT READY — specification only; schemas and executable tests not authorized/run |
| B5 | GitHub commits, PR, exact readback and Blob verification / GitHub 提交、PR、精确读回与 Blob 核验完成 | BLOCKED — bilingual semantic parity incomplete; see bilingual-parity-audit.md; final full-file readback still required |
| B6 | Truly separate independent review and governance disposition / 真正独立审查与治理裁决完成 | INDEPENDENT_REVIEW_PENDING |

## 4. Required and supplemental deliverables / 必需与补充交付物

Core deliverables / 核心交付物：
1. `existing-domain-model-baseline.md`
2. `canonical-domain-entity-inventory.md`
3. `canonical-identity-semantics.md`
4. `canonical-state-semantics.md`
5. `canonical-temporal-evidence-semantics.md`
6. `canonical-domain-relationships.md`
7. `domain-model-complexity-assessment.md`
8. `mature-domain-model-research.md`
9. `cross-owner-canonical-semantics-matrix.md`
10. `domain-semantics-conflict-register.md`
11. `canonical-domain-invariants.md`
12. `canonical-domain-glossary.md`
13. `canonical-domain-model.md`
14. `domain-model-decision-record.md`
15. `validation/README.md`
16. `evidence/README.md`

Supplemental audit/decision deliverables / 补充审计与决策交付物：
- `baseline-currentness-and-owner-source-audit.md`
- `baseline-owner-branch-snapshot-errata.md`
- `bilingual-parity-audit.md`
- `fact-claim-identity-adr.md`
- `evidence/official-reference-validation.md`

Every normative deliverable must contain full Chinese and English semantics in the same file/change set. Unresolved statements remain OPEN, CANDIDATE, TO_VALIDATE or DEFERRED.

每项规范交付物必须在同一文件/变更集中提供完整中英文语义。未决事项必须保留 OPEN、CANDIDATE、TO_VALIDATE 或 DEFERRED 状态。

## 5. Current execution status / 当前执行状态

The current PR diff reports 22 changed files, 2,767 additions and 0 deletions. This count is PR metadata and must be refreshed after further commits. The research branch is historically based on merge base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; current main has advanced to `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`. The current compare reported 64 commits ahead and 26 behind, with status DIVERGED. GitHub's latest PR metadata returned mergeable=false; the cause is NOT VERIFIED. This is not treated as a semantic review result. No rebase, retarget or merge is requested. PR base metadata still reports a distinct older base SHA; no rebase or base retarget is requested here.

当前 PR Diff 元数据显示 22 个变更文件、2,767 行新增、0 行删除。该数量来自 PR 元数据，后续提交后必须刷新。研究分支历史上基于 Merge Base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；当前 main 已推进至 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。最近 Compare 返回 64 commits ahead、26 behind，状态为 DIVERGED。最近 PR 元数据返回 mergeable=true / clean，但这仅是可合并性信号，不代表批准。PR base 元数据仍报告另一个较旧 SHA；本次不请求 Rebase 或修改 Base。

The repository is an architecture-definition repository; README states implementation has not started by design. Issue #7 still requires identification of the canonical runtime implementation repository and accountable engineering owner. No runtime conformance, production readiness, or implementation completion is claimed.

该仓库是架构定义仓库；README 说明按设计尚未开始实现。Issue #7 仍要求确定规范运行时实现仓库及负责工程 Owner。不宣称运行时一致性、生产就绪或实现完成。

## 6. Branch isolation and provenance / 分支隔离与溯源

A subset of initial create-file operations landed on main because the branch parameter was omitted. The affected research artifacts were copied to this isolated branch, then removed from main through explicit delete commits. The audit records the affected paths and verification; main was not rewritten and historical commits remain auditable. This is a delivery-process correction, not a clean initial write.

部分初始 create-file 操作因遗漏 branch 参数而写入 main。受影响研究工件已复制到本隔离分支，再通过明确删除提交从 main 移除。审计记录了受影响路径及核验结果；main 未被重写，历史提交仍可审计。这是交付流程纠正，不是从一开始就正确隔离。

## 7. Stop conditions / 停止条件

Any unresolved identity collision, contradictory state meaning, unowned lifecycle transition, cross-tenant reference ambiguity, Forget/Deletion/Visibility contradiction, incompatible temporal definition, or missing owner acceptance blocks the affected normative contract. Owner decisions are never inferred from silence, summaries, or another Owner's synthesis.

任何未解决的身份冲突、互斥状态含义、无权威归属的生命周期转换、跨 Tenant 引用歧义、Forget/Deletion/Visibility 矛盾、不兼容时间定义或缺少 Owner 验收，均阻塞受影响的规范契约。不得从沉默、摘要或其他 Owner 的综合意见推断 Owner 决策。

## 8. Latest additions / 最新增补

- Baseline currentness and Owner source audit, including current-main pins and selected Owner source evidence.
- Owner branch snapshot errata, correcting earlier branch-tip snapshots from later Phase 3.8 matrix data.
- Fact/Claim and Claim identity ADR decision request; C2 + I1 are candidate recommendations only.
- Official reference validation for DDD, Zep/Graphiti, Mem0, Letta, LangGraph, Temporal, PostgreSQL, W3C PROV-O, RDF/OWL and JSON Schema.

- 基线时效性与 Owner 源文件审计，包含 current-main Pin 和部分 Owner 源证据。
- Owner 分支快照勘误，使用 Phase 3.8 矩阵中的后续数据纠正早期分支 Tip。
- Fact/Claim 与 Claim 身份 ADR 决策请求；C2 + I1 仅为候选建议。
- DDD、Zep/Graphiti、Mem0、Letta、LangGraph、Temporal、PostgreSQL、W3C PROV-O、RDF/OWL 和 JSON Schema 官方参考核验。

B0 remains PARTIAL / NOT PASSED; B2 remains IN PROGRESS; B3 remains NOT PASSED; B4 remains NOT READY; B6 remains INDEPENDENT_REVIEW_PENDING. No merge is requested.

B0 仍为 PARTIAL / NOT PASSED；B2 仍进行中；B3 未通过；B4 未就绪；B6 等待独立审查。本次不请求合并。


## 9. Bilingual parity gate / 双语一致性门禁

- Added `bilingual-parity-audit.md`: the 22-file package screen flags 135 English-only substantive sections across 20 files. This is a screening result, not a semantic translation verdict.
- B-CONFLICT-016 remains OPEN; B5 is BLOCKED / NOT PASSED until P0/P1/P2 bilingual remediation and manual semantic comparison are complete.
- 新增 `bilingual-parity-audit.md`：22 个文件中，20 个文件被筛查出 135 个仅英文实质章节。该结果是筛查，不是语义翻译终审。
- B-CONFLICT-016 仍 OPEN；P0/P1/P2 双语修复及人工语义对照完成前，B5 保持 BLOCKED / NOT PASSED。
