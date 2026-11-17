# DOMAIN-REALITY-001-B — Canonical Domain Model Research
# DOMAIN-REALITY-001-B — 规范领域模型研究

- Owner / 负责人: B — Principal Domain Model & Canonical Semantics Authority
- Status / 状态: IN_PROGRESS — B0 PARTIAL / NOT PASSED; no canonical freeze
- Branch / 分支: `research/domain-reality-001-b`
- Historical merge base / 历史合并基点: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Current main HEAD observed / 当前 main HEAD 观察值: `901e38ba7b45ed1822eaefddc2da8d765cf8985c`
- Research branch HEAD at the latest live read before this README refresh / 本文档本次刷新前最近一次实时读取的研究分支 HEAD: `ec5bcc451554f6e7caf513e98427a6b7b7f13c81`
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

The current PR diff reports 22 changed files, 4,177 additions and 0 deletions. This count is PR metadata and must be refreshed after further commits. The research branch is historically based on merge base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; current main is `901e38ba7b45ed1822eaefddc2da8d765cf8985c`. The current compare reported 138 commits ahead and 28 behind, with status DIVERGED. GitHub's latest PR metadata returned mergeable=false; the cause is NOT VERIFIED. This is not treated as a semantic review result. No rebase, retarget or merge is requested. PR base metadata still reports a distinct older base SHA; no rebase or base retarget is requested here.

当前 PR Diff 元数据显示 22 个变更文件、4,177 行新增、0 行删除。该数量来自 PR 元数据，后续提交后必须刷新。研究分支历史上基于 Merge Base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；当前 main 为 `901e38ba7b45ed1822eaefddc2da8d765cf8985c`。最近 Compare 返回 138 commits ahead、28 behind，状态为 DIVERGED。GitHub 的 mergeability 标志在刷新期间曾在 true/false 间变化；最近一次读取为 false。该标志不代表语义验收。不请求 Rebase、改目标分支或合并。PR base 元数据仍报告另一个较旧 SHA；本次不请求 Rebase 或修改 Base。

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
- Fact/Claim and Claim identity ADR decision request; current B Owner preference is Option A (separate Fact attestation + Claim proposition), still ADR-BLOCKED / NOT APPROVED; stable ClaimRef + ClaimRevisionRef remains candidate.
- Official reference validation for DDD, Zep/Graphiti, Mem0, Letta, LangGraph, Temporal, PostgreSQL, W3C PROV-O, RDF/OWL and JSON Schema.

- 基线时效性与 Owner 源文件审计，包含 current-main Pin 和部分 Owner 源证据。
- Owner 分支快照勘误，使用 Phase 3.8 矩阵中的后续数据纠正早期分支 Tip。
- Fact/Claim 与 Claim 身份 ADR 决策请求；当前 B Owner 倾向 Option A（独立 Fact Attestation + Claim 命题），仍 ADR-BLOCKED / NOT APPROVED；稳定 ClaimRef + ClaimRevisionRef 仍为候选。
- DDD、Zep/Graphiti、Mem0、Letta、LangGraph、Temporal、PostgreSQL、W3C PROV-O、RDF/OWL 和 JSON Schema 官方参考核验。

B0 remains PARTIAL / NOT PASSED; B2 remains IN PROGRESS; B3 remains NOT PASSED; B4 remains NOT READY; B6 remains INDEPENDENT_REVIEW_PENDING. No merge is requested.

B0 仍为 PARTIAL / NOT PASSED；B2 仍进行中；B3 未通过；B4 未就绪；B6 等待独立审查。本次不请求合并。


## 9. Bilingual parity gate / 双语一致性门禁

- Added `bilingual-parity-audit.md`: the 22-file package screen flags 135 English-only substantive sections across 20 files. This is a screening result, not a semantic translation verdict.
- B-CONFLICT-016 remains OPEN; B5 is BLOCKED / NOT PASSED until P0/P1/P2 bilingual remediation and manual semantic comparison are complete.
- 新增 `bilingual-parity-audit.md`：22 个文件中，20 个文件被筛查出 135 个仅英文实质章节。该结果是筛查，不是语义翻译终审。
- B-CONFLICT-016 仍 OPEN；P0/P1/P2 双语修复及人工语义对照完成前，B5 保持 BLOCKED / NOT PASSED。


## 10. Bilingual remediation progress / 双语整改进度

- Author-side bilingual rewrites completed for `canonical-domain-invariants.md`, `canonical-state-semantics.md` and `validation/README.md`; exact Blob pins and manual-review status are recorded in `bilingual-parity-audit.md`.
- These rewrites are not independent parity acceptance. B5 remains BLOCKED / NOT PASSED until remaining P0/P1/P2 files are completed and a separate reviewer verifies semantic equivalence.
- 已完成 `canonical-domain-invariants.md`、`canonical-state-semantics.md` 和 `validation/README.md` 的作者侧双语改写；精确 Blob Pin 及人工复审状态记录在 `bilingual-parity-audit.md`。
- 这些改写不构成独立双语验收。剩余 P0/P1/P2 文件完成并由独立审查者验证语义等价前，B5 仍 BLOCKED / NOT PASSED。


## 11. Additional bilingual remediation / 双语整改补充

- `canonical-domain-model.md` has received a full Chinese peer for design principles, object inventories, owner boundaries, model tiers, architecture fit, authenticated-ingress/physical-ordering boundaries and blockers. Exact Blob: `ce441336e2fbba7c7a28c0b4c75482d524a4ade7`.
- The corresponding file-by-file audit entry is recorded in `bilingual-parity-audit.md` as `REMEDIATED — MANUAL PARITY REVIEW PENDING`. This is author-side work only; no independent parity acceptance is claimed.
- `canonical-domain-model.md` 已为设计原则、对象清单、Owner 边界、模型层级、架构适配、认证入口/物理排序边界及阻塞项补齐中文对照。精确 Blob：`ce441336e2fbba7c7a28c0b4c75482d524a4ade7`。
- 对应逐文件审计已在 `bilingual-parity-audit.md` 中登记为 `REMEDIATED — MANUAL PARITY REVIEW PENDING`。这仅是作者侧工作，不代表独立双语验收。
- B5 remains BLOCKED / NOT PASSED; B6 remains INDEPENDENT_REVIEW_PENDING. No merge or canonical freeze is authorized.
- B5 仍为 BLOCKED / NOT PASSED；B6 仍为 INDEPENDENT_REVIEW_PENDING。未授权合并或规范冻结。


## 12. Entity inventory bilingual remediation / 实体清单双语整改

- `canonical-domain-entity-inventory.md` now has Chinese peer text for all classification rules, entity/value-object/association/security/protocol inventory rows, non-collapse distinctions, open questions and gate disposition. Exact Blob: `1bebb0f5ef85a395afce00db8d74c76bdbd3c721`.
- The parity audit records `REMEDIATED — MANUAL PARITY REVIEW PENDING`; this is not independent acceptance.
- `canonical-domain-entity-inventory.md` 已为全部分类规则、实体/值对象/关联/安全/协议清单行、不可合并语义、未决问题和门禁结论补齐中文对照。精确 Blob：`1bebb0f5ef85a395afce00db8d74c76bdbd3c721`。
- 双语审计将其标记为 `REMEDIATED — MANUAL PARITY REVIEW PENDING`；这不构成独立验收。
- B1 remains IN PROGRESS; B5 remains BLOCKED / NOT PASSED; B6 remains INDEPENDENT_REVIEW_PENDING.
- B1 仍进行中；B5 仍为 BLOCKED / NOT PASSED；B6 仍为 INDEPENDENT_REVIEW_PENDING。


## 13A. Chinese gate and deliverable mirror / 中文门禁与交付物对照

| Gate | 中文退出条件 | 当前状态的中文含义 |
|---|---|---|
| B0 | 已读取真实仓库基线、精确来源 Pin、相关 PR/Issue 和权威文件。 | PARTIAL / NOT PASSED：基线已部分核验，但完整 Owner 契约、PR Diff 和最新版本协调未完成。 |
| B1 | 候选实体已分类，重复和遗漏已评估。 | IN PROGRESS：候选清单与复杂度评估已发布，尚未得到全部 Owner 确认。 |
| B2 | Identity、State、Time、Evidence、Provenance 和 Relationships 已协调一致。 | IN PROGRESS：Fact/Claim 与 Claim 身份 ADR 仍是决策请求，未冻结 Schema。 |
| B3 | A/C/D/E/F/G/H/I/Storage/Testing 的跨 Owner 矩阵和冲突登记已完成。 | NOT PASSED：Owner 验收和后继版本 Pin 仍需协调；认证入口和 Storage L4 仍阻塞。 |
| B4 | 不变量、Schema、Fixtures 和验证规范一致。 | NOT READY：目前仅有规范；Schema 和可执行测试尚未获授权/运行。 |
| B5 | GitHub 提交、PR、精确读回、Blob 核验及双语语义对等完成。 | BLOCKED：双语语义对等未完成；见 bilingual-parity-audit.md；仍需最后完整读回。 |
| B6 | 真正独立的审查和治理裁决完成。 | INDEPENDENT_REVIEW_PENDING：当前作者会话不能充当独立审查者。 |

### 核心交付物中文说明

1. existing-domain-model-baseline.md：现有领域模型基线和源文件审计。
2. canonical-domain-entity-inventory.md：候选领域对象清单、分类和存在性理由。
3. canonical-identity-semantics.md：身份、命名空间、类型化引用和稳定性。
4. canonical-state-semantics.md：规范状态词汇、状态机和执行证明边界。
5. canonical-temporal-evidence-semantics.md：时间、Evidence 和 Provenance 语义。
6. canonical-domain-relationships.md：关系类型、基数、所有权、Forget 和 Tenant 边界。
7. domain-model-complexity-assessment.md：实体复杂度、重复抽象、合并/延后/拒绝。
8. mature-domain-model-research.md：DDD、Event Sourcing、Temporal、Graph、标准和成熟项目研究。
9. cross-owner-canonical-semantics-matrix.md：跨 Owner 语义矩阵和精确来源 Pin。
10. domain-semantics-conflict-register.md：冲突、权威、解除条件和 Gate。
11. canonical-domain-invariants.md：可验证不变量和正/负测试条件。
12. canonical-domain-glossary.md：规范中英文词汇及禁止混淆。
13. canonical-domain-model.md：最小/推荐规范模型和关系图。
14. domain-model-decision-record.md：决策依据、备选方案、后果和未决事项。
15. validation/README.md：Schema、Fixtures、正/负例和测试计划。
16. evidence/README.md：外部官方来源索引及证据局限。

补充文件用于时效性审计、Owner 分支快照勘误、Fact/Claim ADR 决策请求、外部来源核验和双语对等审计。文件名和稳定 ID 在中英文版本中保持一致。

### 中文当前执行状态

- 本研究仅建立候选规范语义，不替代 D/E/F/G/H/I/Storage 的 Owner 权威。
- Fact 与 Claim 保持概念区分；是否独立对象/类型仍 ADR-BLOCKED。
- C Origin Signature、H Transport Authentication、I Trust/Authorization 和 Storage Durable Ingress/Replay 是不同证明边界；生产入口仍 BLOCKING。
- Serialization Anchor 是 Storage 物理实现细节，不是规范领域实体或全局时钟。
- PR #55 为 Open/Draft；不请求合并。分支隔离纠正已经记录，main 中 13 个误写路径已核验不存在。
- 双语改写仅是作者侧工作；没有独立双语验收。
- 不宣称实现、生产就绪、Schema 冻结或最终 ACCEPTED。

## 13. Complexity assessment bilingual remediation / 复杂度评估双语整改

- `domain-model-complexity-assessment.md` now has a full Chinese semantic mirror for qualitative assessment dimensions, entity/value-object/derived-view classifications, merge/defer/reject decisions, aggregate analysis, complexity risks, Storage serialization-anchor classification, model tiers and gate status. Exact Blob: `38bee7501e52798152524665778c69659be6cf33`.
- The parity audit records `REMEDIATED — MANUAL PARITY REVIEW PENDING`. This is author-side remediation, not independent semantic acceptance.
- `domain-model-complexity-assessment.md` 已为定性评估维度、实体/值对象/派生视图分类、合并/延后/拒绝决策、聚合分析、复杂度风险、Storage 序列化锚点分类、模型层级及门禁状态补齐完整中文语义对照。精确 Blob：`38bee7501e52798152524665778c69659be6cf33`。
- 双语审计将其标记为 `REMEDIATED — MANUAL PARITY REVIEW PENDING`。这属于作者侧整改，不是独立语义验收。
- B1 remains IN PROGRESS; B5 remains BLOCKED / NOT PASSED; B6 remains INDEPENDENT_REVIEW_PENDING.
- B1 仍进行中；B5 仍为 BLOCKED / NOT PASSED；B6 仍为 INDEPENDENT_REVIEW_PENDING。


## 14. Mature reference research bilingual remediation / 成熟参考研究双语整改

- `mature-domain-model-research.md` now has detailed Chinese peer text for Zep/Graphiti, Mem0, Letta, LangGraph, Temporal, PostgreSQL and JSON Schema, including observed behavior, borrow/do-not-copy boundaries, version caveats and cross-project synthesis. Exact Blob: `1f31eee069f58e9da5b1eeecf7298af8b3c24882`.
- The parity audit records `REMEDIATED — MANUAL PARITY REVIEW PENDING`; this is not independent validation of external-source claims.
- `mature-domain-model-research.md` 已为 Zep/Graphiti、Mem0、Letta、LangGraph、Temporal、PostgreSQL 和 JSON Schema 补齐详细中文对照，包括实际行为、可借鉴/不得照搬边界、版本限制及跨项目综合结论。精确 Blob：`1f31eee069f58e9da5b1eeecf7298af8b3c24882`。
- 双语审计将其标记为 `REMEDIATED — MANUAL PARITY REVIEW PENDING`；这不代表外部来源主张已通过独立验证。
- B1 remains IN PROGRESS; B2/B3 remain open; B5 remains BLOCKED / NOT PASSED; B6 remains INDEPENDENT_REVIEW_PENDING.
- B1 仍进行中；B2/B3 仍未关闭；B5 仍为 BLOCKED / NOT PASSED；B6 仍为 INDEPENDENT_REVIEW_PENDING。


## 15. Existing baseline evidence bilingual remediation / 现有基线证据双语整改

- `existing-domain-model-baseline.md` now includes a full Chinese peer for the Owner branch snapshot, relevant PR/Issue impact, legacy B branch comparison, all five material conflicts, missing definitions, confidence and B0 disposition. Exact Blob: `08f2843db1d41027ee6d1bee9af564ce07a3a793`.
- The file-by-file audit records `REMEDIATED — MANUAL PARITY REVIEW PENDING`; its historical branch/issue snapshots still require live-source refresh before acceptance.
- `existing-domain-model-baseline.md` 已为 Owner 分支快照、相关 PR/Issue 影响、旧 B 分支比较、五项重大语义冲突、缺失定义、基线置信度及 B0 结论补齐完整中文对照。精确 Blob：`08f2843db1d41027ee6d1bee9af564ce07a3a793`。
- 逐文件审计将其标记为 `REMEDIATED — MANUAL PARITY REVIEW PENDING`；其中历史分支/Issue 快照在验收前仍须实时刷新。
- B0 remains PARTIAL / NOT PASSED; B5 remains BLOCKED / NOT PASSED; B6 remains INDEPENDENT_REVIEW_PENDING.
- B0 仍为 PARTIAL / NOT PASSED；B5 仍为 BLOCKED / NOT PASSED；B6 仍为 INDEPENDENT_REVIEW_PENDING。


## 16. Live baseline and evidence refresh / 实时基线与证据刷新 — 2026-11-18

- Live `main` HEAD: `b3c666e67982cb3d3374e759cfb6552c7765aacb`.
- Live research branch HEAD before this README update: `f95b479b223ebb63c8aebcfca13a4cd9b28d5331`.
- PR #55 remains Open / Draft; live PR head matched the research branch before this update. Base SHA remains `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`. Current compare is DIVERGED (145 ahead / 32 behind), merge base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; GitHub reports `mergeable=false`, cause unverified.
- All ten named Owner branch refs were re-read. Selected successor evidence now includes H Unified 1.2.15 mapping, I's exact review of 1.2.15, Storage v3.3.1 and A Phase 3.12.1 review. Exact pins and caveats are in `baseline-currentness-and-owner-source-audit.md`.
- Issue #7 was re-read and remains OPEN; runtime implementation repository, accountable engineering owner, reproducible build/test entry points and deployment topology remain unresolved.
- Official reference validation was refreshed on 2026-11-18. Mem0's detailed official page timed out and remains explicitly NOT REVALIDATED.
- The full 22-file exact Blob/line-count snapshot is in `bilingual-parity-audit.md`; currentness audit Blob is `92b3f6d1b0c6236f245195337129f1d69a5bd499`; official-reference validation Blob is `ef4a0cf448e474b08bf5ff6b80c32dbae705b002`. The parity audit records its own latest exact Blob and all cross-file pins; its self Blob changes whenever it is updated.

- 实时 `main` HEAD：`b3c666e67982cb3d3374e759cfb6552c7765aacb`。
- 本 README 更新前的实时研究分支 HEAD：`f95b479b223ebb63c8aebcfca13a4cd9b28d5331`。
- PR #55 仍为 Open / Draft；本次更新前实时 PR Head 与研究分支一致。Base SHA 仍为 `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`。当前 Compare 为 DIVERGED（领先 145 / 落后 32），Merge Base 为 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；GitHub 返回 `mergeable=false`，原因未核实。
- 已重新读取十个指定 Owner 分支 Ref。选定后继证据现包括 H Unified 1.2.15 Mapping、I 对 1.2.15 的精确复审、Storage v3.3.1 和 A Phase 3.12.1 复审。精确 Pin 和限制见 `baseline-currentness-and-owner-source-audit.md`。
- Issue #7 已重新读取，仍 OPEN；运行时实现仓库、负责工程 Owner、可复现 Build/Test 入口及部署拓扑仍未解决。
- 官方参考资料已于 2026-11-18 刷新。Mem0 详细官方页面读取超时，仍明确标记为本轮未重新验证。
- 全部 22 个文件的精确 Blob/行数快照见 `bilingual-parity-audit.md`；当前性审计 Blob 为 `8641268f6cb93e8154ae1693ace37cc72498a4b8`；官方参考核验 Blob 为 `ef4a0cf448e474b08bf5ff6b80c32dbae705b002`。双语审计记录自身最新精确 Blob 和所有跨文件 Pin；其自身 Blob 会随更新变化。

Gate disposition remains unchanged: B0 PARTIAL / NOT PASSED; B1 IN PROGRESS; B2 IN PROGRESS; B3 NOT PASSED; B4 NOT READY; B5 BLOCKED / NOT PASSED pending independent semantic parity review; B6 INDEPENDENT_REVIEW_PENDING. No schema freeze, implementation authorization, Owner approval, merge or Ready transition is claimed.

门禁结论不变：B0 PARTIAL / NOT PASSED；B1 进行中；B2 进行中；B3 未通过；B4 未就绪；B5 因等待独立语义对等审查而 BLOCKED / NOT PASSED；B6 INDEPENDENT_REVIEW_PENDING。不宣称 Schema 冻结、实现授权、Owner 批准、合并或转为 Ready。


## 17. Blocking cross-owner reconciliation / 阻塞性跨 Owner 协调 — 2026-11-18

A's exact Phase 3.12.1 review of Storage v3.3.1 found a substantive Option A status contradiction. The pinned Storage/D ADR selects Option A as the normative v1 logical architecture and leaves only L4 physical engine/deployment open; Storage v3.3.1 calls Option A a conditional L1 candidate and cites A-01–A-05 clarifications absent from the pinned ADR. A explicitly rejects v3.3.1 as a final consistent manifest until Storage publishes a corrected successor and A re-reviews it.

A 对 Storage v3.3.1 的精确 Phase 3.12.1 复审发现 Option A 状态存在实质矛盾。精确绑定的 Storage/D ADR 已选择 Option A 作为 v1 规范逻辑架构，仅保留 L4 物理引擎/部署开放；Storage v3.3.1 却称 Option A 为 conditional L1 candidate，并引用精确 ADR 中不存在的 A-01–A-05 澄清项。A 明确拒绝将 v3.3.1 作为最终一致 Manifest，直到 Storage 发布修正后继版本并由 A 重新复审。

- New conflict: **B-CONFLICT-017 — BLOCKING / OPEN**.
- Exact evidence: ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; Storage v3.3.1 Blob `f6e61691ecdcfcbf1fb423cc45242868676ca925`; A Phase 3.12.1 review Blob `d3d4e6f4b6d7e82f90e3eee3427c8ace3b4160c8`.
- H Unified 1.2.15 mapping Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924` and I review Blob `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` are later structural-candidate evidence; they do not retroactively amend Storage v3.3.1 or constitute production trust approval.
- Storage owns the successor manifest correction. B records the cross-owner incompatibility and must not edit Storage-owned normative artifacts.
- B3 remains NOT PASSED. G Applied remains FREEZE BLOCKED / NOT VERIFIED; D Forget clearance/lineage/barrier/release remain open; I/H outer-envelope trust/profile/verification remain open; Storage L4 physical realization remains open.

- 新增冲突：**B-CONFLICT-017 — BLOCKING / OPEN**。
- 精确证据：ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`；Storage v3.3.1 Blob `f6e61691ecdcfcbf1fb423cc45242868676ca925`；A Phase 3.12.1 复审 Blob `d3d4e6f4b6d7e82f90e3eee3427c8ace3b4160c8`。
- H Unified 1.2.15 Mapping Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924` 和 I 复审 Blob `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` 属于较新的结构候选证据；它们不会追溯修改 Storage v3.3.1，也不构成生产 Trust 批准。
- Storage 负责修正后继 Manifest。B 只记录跨 Owner 不兼容，不得编辑 Storage 所有的规范工件。
- B3 仍 NOT PASSED。G Applied 仍 FREEZE BLOCKED / NOT VERIFIED；D Forget Clearance/Lineage/Barrier/Release 仍开放；I/H Outer-Envelope Trust/Profile/Verification 仍开放；Storage L4 物理实现仍开放。

No Storage correction, A independent human approval, production authentication, global Forget completion, Applied freeze, L4 deployment or independent QA result is claimed.

不宣称 Storage 已整改、A 独立人类批准、生产认证、Global Forget 完成、Applied 冻结、L4 部署或独立 QA 结果。


## 18. Option A manifest consistency closure / Option A Manifest 一致性关闭 — 2026-11-18

Storage published v3.3.2 and A issued Phase 3.12.2 exact re-review:
- Storage v3.3.2 manifest Blob: `5c614375e10698e4931d83deb57d20321445e068`.
- A Phase 3.12.2 re-review Blob: `eb3c946065aff4fbc6d76f384402fb9f75fa32dc`.
- The successor corrects Option A to “selected as normative v1 logical architecture; L4 physical engine/deployment OPEN” and removes unsupported A-01–A-05 references.
- A marks the prior v3.3.1 Option A status inconsistency **CLOSED at manifest-consistency level** and accepts v3.3.2 as a consistent exact-version candidate with enumerated release blockers.
- B-CONFLICT-017 is therefore **CLOSED — MANIFEST CONSISTENCY REMEDIATED**, with the explicit caveat that Storage and A artifacts are delegated-role outputs, not independent human Owner signatures.
- Storage v3.3.2 / A 3.12.2 bind H 1.2.14 / C 1.0.1 and predecessor C/I reviews. They do not include H 1.2.15; successor binding and fresh A review remain required.
- B3 remains NOT PASSED. Authenticated ingress, I trust/profile/key registration, durable replay, G Applied freeze, D Forget, and Storage L4 remain open.

Storage 已发布 v3.3.2，A 已发布 Phase 3.12.2 精确复审：
- Storage v3.3.2 Manifest Blob：`5c614375e10698e4931d83deb57d20321445e068`。
- A Phase 3.12.2 复审 Blob：`eb3c946065aff4fbc6d76f384402fb9f75fa32dc`。
- 后继版本将 Option A 修正为“已选择 v1 规范逻辑架构；L4 物理引擎/部署 OPEN”，并删除无依据的 A-01–A-05 引用。
- A 将此前 v3.3.1 Option A 状态不一致判为 **Manifest 一致性层面 CLOSED**，并接受 v3.3.2 为带列明 Release Blocker 的一致精确版本候选。
- 因此 B-CONFLICT-017 更新为 **CLOSED — MANIFEST CONSISTENCY REMEDIATED**，但明确注明 Storage 与 A 工件均为委派角色产物，不是独立人类 Owner 签名。
- Storage v3.3.2 / A 3.12.2 绑定 H 1.2.14 / C 1.0.1 和前序 C/I 复审，不包含 H 1.2.15；后继绑定及 A 新复审仍需要。
- B3 仍 NOT PASSED。Authenticated Ingress、I Trust/Profile/Key 注册、Durable Replay、G Applied 冻结、D Forget 和 Storage L4 仍开放。

This closes one document-consistency conflict only. It does not close any production, governance, runtime or physical-storage gate.

这只关闭一项文档一致性冲突，不关闭任何生产、治理、运行时或物理存储门禁。


## 19. B2 semantic closure checkpoint / B2 语义闭合检查点 — 2026-11-18

The B decision record now contains an exact-source B2 checkpoint. It confirms that some semantic distinctions are decided, but the core B2 closure conditions remain open:

B 决策记录现已加入精确来源 B2 检查点。该检查点确认部分语义区分已经确定，但 B2 核心闭合条件仍开放：

- **Fact / Claim:** I-04/P-04 require distinction. The current B Owner ADR prefers Option A (separate Fact attestation object + Claim proposition thread) as a candidate; formal Architecture Governance approval is absent and the ADR remains BLOCKED. The earlier C2/Option B recommendation in this research package is superseded.
- **Claim identity across MemoryVersions:** I1 (stable Claim identity plus immutable version-local snapshots/revisions) is a candidate, not a decision; I2 remains viable; I3 is deferred.
- **Typed identity:** B has approved ActorRef / ScopeRef / EnvironmentRef semantic mapping within B's authority; H wire encoding, I trust/policy, registry authority and runtime conformance are not thereby approved.
- **Scope / Permission:** separation is DECIDED; scope algebra, policy language, inheritance, cached authorization and revocation guarantees remain open.
- **I36 governance:** Issue #5 remains OPEN; I36-GOV-01..10 remain GOVERNANCE-BLOCKED.
- **Session / Conversation:** RuntimeSessionRef, Session ScopeRef, Conversation and Agent identity remain distinct; exact canonical relation and consumer mappings remain open.

- **Fact / Claim：** I-04/P-04 要求概念区分。当前 B Owner ADR 优先推荐 Option A（独立 Fact Attestation 对象 + Claim 命题线程），但尚无正式 Architecture Governance 批准，ADR 仍 BLOCKED。本研究包此前倾向 C2/Option B 的建议已被取代。
- **Claim 跨 MemoryVersion 身份：** I1（稳定 Claim 身份 + 不可变版本局部 Snapshot/Revision）仅为候选，不是决策；I2 仍可选；I3 延后。
- **类型化身份：** B 已在自身权限范围内批准 ActorRef / ScopeRef / EnvironmentRef 语义映射；这不代表 H Wire 编码、I Trust/Policy、Registry 权威或 Runtime Conformance 获批。
- **Scope / Permission：** 二者分离已 DECIDED；Scope 代数、Policy 语言、继承、缓存授权和撤销保证仍开放。
- **I36 治理：** Issue #5 仍 OPEN；I36-GOV-01..10 仍 GOVERNANCE-BLOCKED。
- **Session / Conversation：** RuntimeSessionRef、Session ScopeRef、Conversation 和 Agent Identity 保持区分；规范关系和消费者映射仍开放。

B2 remains IN PROGRESS / NOT PASSED; B4 remains NOT READY. No schema freeze or cross-owner acceptance is inferred.

B2 仍 IN PROGRESS / NOT PASSED；B4 仍 NOT READY。不推断 Schema 冻结或跨 Owner 验收。


## 20. Current B Owner Fact/Claim ADR reconciliation / 当前 B Owner Fact/Claim ADR 对账 — 2026-11-18

The current B Owner branch `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` now provides the controlling B recommendation:
- Summary ADR Blob: `a1024938ff5baba069cf128c69496a44e143330c`.
- Detailed canonical ADR Blob: `df77e4a93cb8fef689ae7c828888d960cbf381d6`.
- Consumer mapping Blob: `dd45a37199c9b69ab6b68f65e051a484a04691d4`.
- B typed-reference approval Blob: `3a1e77889cd9a90cd5822d9f0cb3437880868706` (separate scope; does not approve Fact/Claim).

当前 B Owner 分支 `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` 已提供当前 B 推荐基线：
- 摘要 ADR Blob：`a1024938ff5baba069cf128c69496a44e143330c`。
- 详细规范 ADR Blob：`df77e4a93cb8fef689ae7c828888d960cbf381d6`。
- 消费者映射 Blob：`dd45a37199c9b69ab6b68f65e051a484a04691d4`。
- B 类型化引用批准 Blob：`3a1e77889cd9a90cd5822d9f0cb3437880868706`（独立范围，不批准 Fact/Claim）。

**Current B preference: Option A — separate Claim proposition thread and independently addressable Fact attestation object.** This supersedes the earlier C2/Option B preference in the research ADR. Option A remains CANDIDATE / NOT APPROVED. The formal Architecture Governance authority and approval record are not present; I-04/P-04, main Domain Overview and terminology still contain inconsistent formulations. Both current bilingual domain guides retain ADR-BLOCKED. Issue #43 remains OPEN.

**当前 B 倾向：Option A——Claim 命题线程与独立可寻址 Fact Attestation 对象分离。** 这取代研究 ADR 此前倾向 C2/Option B 的建议。Option A 仍为 CANDIDATE / NOT APPROVED。正式 Architecture Governance 权威和批准记录尚不存在；I-04/P-04、Main Domain Overview 和术语文件仍有不一致表述。当前中英文领域指南均保留 ADR-BLOCKED。Issue #43 仍 OPEN。

Stable ClaimRef + immutable ClaimRevisionRef and ConflictSet over exact ClaimRevisionRefs remain candidates, not frozen schemas. D owns canonical identity allocation/commit and ConflictSet persistence after approval; E keeps neutral CandidateProposition/ExtractionIR; F/G do not assume unapproved Fact/Claim identities; H wire fields remain unfrozen. B2 remains IN PROGRESS / NOT PASSED and B4 NOT READY.

稳定 ClaimRef + 不可变 ClaimRevisionRef，以及按精确 ClaimRevisionRef 构建 ConflictSet，仍是候选，不是冻结 Schema。批准后 D 负责规范身份分配/Commit 和 ConflictSet 持久化；E 保持中立 CandidateProposition/ExtractionIR；F/G 不得假定未批准的 Fact/Claim 身份；H Wire 字段仍未冻结。B2 仍 IN PROGRESS / NOT PASSED，B4 仍 NOT READY。


## 21. D/E/F/G exact consumer alignment / D/E/F/G 精确消费者对齐 — 2026-11-18

The live consumer contracts preserve the ADR-blocked boundary:
- **D:** Canonical Store permits only neutral PropositionRef before INT-P0-01 approval; stable Claim ID + immutable ClaimRevision is a D candidate.
- **E:** CandidateProposition/ExtractionIR is pre-canonical; E does not assign Fact/Claim identity or adjudicate truth.
- **F:** D owns canonical Claim identity/status; F cannot resolve disputed Claims or promote epistemic status.
- **G:** ContextEntry pins exact MemoryVersion; G owns ContextVersion/ChangeSet, not Claim/Fact identity.

实时消费者契约保留 ADR 阻塞边界：
- **D：** INT-P0-01 批准前，Canonical Store 只允许中立 PropositionRef；稳定 Claim ID + 不可变 ClaimRevision 是 D 的候选方案。
- **E：** CandidateProposition/ExtractionIR 属于规范化前表示；E 不分配 Fact/Claim 身份，也不裁决真实性。
- **F：** D 拥有规范 Claim 身份/状态；F 不得解决争议 Claim 或提升认知状态。
- **G：** ContextEntry 固定精确 MemoryVersion；G 拥有 ContextVersion/ChangeSet，不拥有 Claim/Fact 身份。

**Do not conflate Option A labels:** B Fact/Claim Option A means separate Fact attestation object + Claim proposition thread. D Claim identity Option A means stable Claim ID + immutable ClaimRevision. They are different decisions; both remain candidates. No Claim/Fact/ClaimRevision/ConflictSet schema is frozen.

**不得混淆 Option A 编号：** B Fact/Claim Option A 指独立 Fact Attestation 对象 + Claim 命题线程；D Claim Identity Option A 指稳定 Claim ID + 不可变 ClaimRevision。两者是不同决策，均仍为候选。不得冻结 Claim/Fact/ClaimRevision/ConflictSet Schema。

This consumer alignment is source-backed but is not D/E/F/G approval of B's preferred Fact/Claim Option A. B2 remains IN PROGRESS / NOT PASSED; B4 remains NOT READY.

该消费者对齐有来源支持，但不代表 D/E/F/G 已批准 B 优先推荐的 Fact/Claim Option A。B2 仍 IN PROGRESS / NOT PASSED；B4 仍 NOT READY。


## 19. Post-merge currentness and governance reconciliation / 合并后当前性与治理状态核对

**Live status at 2026-11-18 05:22 Asia/Singapore:** PR #55 is CLOSED / MERGED (merged 2026-11-17T19:12:47Z; merge commit `07ee5702cab0d12d6136fe3c024bde9a7af44a97`). Current main HEAD is `a2b8babb1cacfcfbcd590b147bdf34ce162944c2`, and the research package is present in the main tree. The PR review listing contains 10 COMMENTED records and no APPROVED record. The merge does not close B0–B6, grant Architecture Governance approval, or freeze any schema. See [Post-Merge Currentness & Governance Reconciliation](post-merge-currentness-and-governance-reconciliation.md). This section supersedes earlier Open/Draft and “package absent from main” status snapshots.

**截至 2026-11-18 05:22（新加坡时间）的实时状态：** PR #55 已 CLOSED / MERGED（合并时间 2026-11-17T19:12:47Z；Merge Commit `07ee5702cab0d12d6136fe3c024bde9a7af44a97`）。当前 main HEAD 为 `a2b8babb1cacfcfbcd590b147bdf34ce162944c2`，研究包存在于 main Tree。PR Review 列表有 10 条 COMMENTED 记录，没有 APPROVED 记录。该合并不关闭 B0–B6，不代表 Architecture Governance 批准，也不冻结任何 Schema。详见[合并后当前性与治理状态核对](post-merge-currentness-and-governance-reconciliation.md)。本节取代此前 Open/Draft 及“研究包不在 main”的状态快照。


## 20. Latest cross-owner source reconciliation / 最新跨 Owner 来源协调

The exact current B/D/E/F/G and A/C/H/I/Storage branch heads and source Blob pins were refreshed on 2026-11-18. The detailed B2/B3 status, H 1.2.15 evidence ceiling, I production trust registration gap, D/I/Storage Forget proposal disposition and unchanged gate states are recorded in [Latest Cross-Owner Source Reconciliation](latest-cross-owner-source-reconciliation.md). This is a source audit, not Owner acceptance or Governance approval.

2026-11-18 已刷新 B/D/E/F/G 与 A/C/H/I/Storage 的精确当前分支 Head 和来源 Blob Pin。B2/B3 状态、H 1.2.15 证据上限、I 生产 Trust 注册缺口、D/I/Storage Forget 提案状态及未变化的门禁状态，详见[最新跨 Owner 来源协调](latest-cross-owner-source-reconciliation.md)。该文件是来源审计，不是 Owner 验收或 Governance 批准。


## 21. PR #120 merge reconciliation / PR #120 合并状态核对

PR #120 was merged at `2026-11-17T21:29:04Z` by `oahcom`, merge commit `6c325804027b88de1014ab3364cdda7e0c023ba6`. The merged head was `069984b5c3915334d6fa2d3ec409d4c7e36fe549`. Current main was subsequently observed at `ab1fa87d74ca4a632155aa19569533ea560109d5`. PR #120 carried the post-PR-55 merge-status correction; the latest cross-owner source refresh in section 20 is a later isolated follow-up and is not part of PR #120's merged head. The merge does not close B0–B6 or approve any architecture decision.

PR #120 于 `2026-11-17T21:29:04Z` 由 `oahcom` 合并，Merge Commit 为 `6c325804027b88de1014ab3364cdda7e0c023ba6`；合并时 Head 为 `069984b5c3915334d6fa2d3ec409d4c7e36fe549`。此后观察到的 main 为 `ab1fa87d74ca4a632155aa19569533ea560109d5`。PR #120 携带 PR #55 合并状态纠偏；第 20 节的最新跨 Owner 来源刷新是之后隔离进行的后续工作，不属于 PR #120 已合并的 Head。该合并不关闭 B0–B6，也不批准任何架构决策。


## 22. Latest exact C/G/H source refresh / 最新 C/G/H 精确来源刷新

- C branch HEAD: `461dd616209657c3bf485871bdbc2a1b6a652d40`; delegated C review Blob: `c97355b27c2ee8647a03a6e5ef3f8bdac0b34ef7`.
- G branch HEAD: `07a84a5ef5b331180bee47f8a60ef16c2918a700`; delegated G successor consumer decision Blob: `03a86eec0f4d81e6fc1c83274b75080932fdc16b`.
- H branch HEAD: `b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9`; Applied validator Blob: `8febb915ec321cc37cf159b2f5b917a3f945726c`; test Blob: `77cb66b895c5293a2f4883b1d5cb69775e71d00c`.
- H current suite has 29 test methods. The cited 26/26 CI run is tied to earlier H head `9fb2097905ef653b3a2048ac5f6804fc94178d8d`; no exact 29/29 result on current H head is verified.
- B0/B2/B3/B5/B6 remain as recorded; no schema freeze or production authorization is implied.

- C 当前分支 HEAD：`461dd616209657c3bf485871bdbc2a1b6a652d40`；委派 C 复审 Blob：`c97355b27c2ee8647a03a6e5ef3f8bdac0b34ef7`。
- G 当前分支 HEAD：`07a84a5ef5b331180bee47f8a60ef16c2918a700`；委派 G 后继消费者决议 Blob：`03a86eec0f4d81e6fc1c83274b75080932fdc16b`。
- H 当前分支 HEAD：`b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9`；Applied Validator Blob：`8febb915ec321cc37cf159b2f5b917a3f945726c`；测试 Blob：`77cb66b895c5293a2f4883b1d5cb69775e71d00c`。
- H 当前测试套件有 29 个测试方法。引用的 26/26 CI 运行绑定较早 H Head `9fb2097905ef653b3a2048ac5f6804fc94178d8d`；当前 H Head 的精确 29/29 结果未核实。
- B0/B2/B3/B5/B6 维持原记录；不代表 Schema 冻结或生产授权。
