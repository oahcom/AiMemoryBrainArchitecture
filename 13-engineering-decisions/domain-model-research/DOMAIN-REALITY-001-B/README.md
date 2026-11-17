# DOMAIN-REALITY-001-B — Canonical Domain Model Research
# DOMAIN-REALITY-001-B — 规范领域模型研究

- Owner / 负责人: B — Principal Domain Model & Canonical Semantics Authority
- Status / 状态: IN_PROGRESS — B0 baseline partially verified; no canonical freeze
- Branch / 分支: `research/domain-reality-001-b`
- Base commit / 基线提交: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Research date / 研究日期: 2026-11-17

## 1. Purpose / 目的

This work establishes a minimal, complete, explicit, and verifiable canonical domain model for AI Memory Brain. It audits actual repository contracts before proposing semantic changes. It does not replace Owner-local authority or decide physical implementation.

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
| B1 | Entity inventory classified; duplication and omissions assessed / 实体清单分类，重复与遗漏完成评估 | NOT STARTED |
| B2 | Identity, state, temporal, evidence, provenance and relationships reconciled / 身份、状态、时间、证据、溯源与关系完成协调 | NOT STARTED |
| B3 | A/C/D/E/F/G/H/I/Storage/Testing cross-owner matrix and conflict register / 跨 Owner 矩阵及冲突登记完成 | NOT STARTED |
| B4 | Invariants, schemas, fixtures and validation specifications consistent / 不变量、Schema、Fixtures 与验证规范一致 | NOT STARTED |
| B5 | GitHub commits, PR, exact readback and Blob verification / GitHub 提交、PR、精确读回与 Blob 核验完成 | NOT STARTED |
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

The actual `main` baseline is pinned in the baseline report. The repository is an architecture-definition repository; README explicitly says implementation has not started by design. The existing B branch is `session-b-domain-model-phase3`; it is not the requested research branch and its Scope/Permission source Blob differs from current main. The new research branch was created from the verified main HEAD without modifying main or the existing B branch.

真实 `main` 基线已在基线报告中 Pin。仓库是架构定义仓库；README 明确说明按设计尚未开始实现。已有 B 分支为 `session-b-domain-model-phase3`，它不是本次研究分支，且其 Scope/Permission 源 Blob 与当前 main 不同。新研究分支从已核验的 main HEAD 创建，没有修改 main 或既有 B 分支。

## 6. Stop conditions / 停止条件

Any unresolved identity collision, contradictory state meaning, unowned lifecycle transition, cross-tenant reference ambiguity, Forget/Deletion/Visibility contradiction, or incompatible temporal definition blocks the affected normative contract. Owner decisions are never inferred from silence, summaries, or another Owner's synthesis.

任何未解决的身份冲突、互斥状态含义、无权威归属的生命周期转换、跨 Tenant 引用歧义、Forget/Deletion/Visibility 矛盾或不兼容时间定义，均阻塞受影响的规范契约。不得从沉默、摘要或其他 Owner 的综合意见推断 Owner 决策。
