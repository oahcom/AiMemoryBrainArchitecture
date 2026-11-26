---
document_metadata:
  domain: domain-model
  role: decision-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner delegate under Issue #305 comment 7042461592"
      decision_date: "2026-11-21"
      approved_version:
        scheme: git
        value: "003fa0063e1e359bc91de8c2950366f757bd1210"
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Issue #305 comment 7042461592"
        - "02-domain-model/domain-model-overview.md @ 5b86fe23ab7c670b4ae13331b56572aee35f5d00"
        - "02-domain-model/core-entities.md @ 06a914699813e36d8bfd69e96c46debb3c3e0cf3"
        - "B ADR branch session-b-domain-model-phase3 @ 2faf8ec38f14dba49e7263d7a60804dae1a74ee2"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "已实时读取所引用的 main 与 B 分支工件；本决策仅确定语义，不冻结实现 Schema。"
    usage_status: Active
    modification_status: Pending-Reapproval
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
    canonical_scope: "Project Owner decision: Fact and Claim semantics and identity"
    canonical_scope_id: "domain-model/fact-claim-identity"
    canonical_scope_keywords:
      - fact
      - claim
      - attestation
      - identity
      - revision
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md"
---

# Owner 决策 — Fact / Claim 语义与身份

- 决策 ID：OWNER-DECISION-FACT-CLAIM-001
- 关联 ADR：B-ADR-FACT-CLAIM-001
- 决策日期：2026-11-21 UTC
- 决策权威：Issue #305 评论 7042461592 授权的 Project Owner delegate
- 行使身份：依照 Project Owner 持续指令履职的统一架构 Owner 会话
- 证据等级：该决策未记录与实现会话的 prompt 配对证据，因此保持 `INDEPENDENCE_UNVERIFIABLE`；共用 GitHub 账号不构成独立性否决理由；不声称存在独立人工签名。

## 1. 决策

**已决定：选择 Option A（Fact 独立 Attestation，Claim 表示命题）以及 I1（稳定 Claim 身份与不可变 Claim 修订）。**

这是开发基线范围内的语义架构决策，解决 B-ADR-FACT-CLAIM-001 中的概念语义及身份/版本问题。

本决策不冻结 JSON Schema、数据库 DDL、存储布局、公共 API、BMCP Wire 字段或 Runtime 实现。

## 2. 采纳的语义

1. Claim 是可归属的命题线程，表示 Actor、来源或流程所断言、观察、报告、推断、质疑、争议、更正或撤回的内容。
2. ClaimRevision 是稳定 Claim 身份下的一个不可变断言状态。
3. Fact 是独立标识、受治理的 Attestation/Adjudication 对象。它不是 Verified Claim 的同义词，不是置信度阈值，也不保证绝对客观真理。
4. FactRevision 是一个不可变 Attestation 状态，必须引用精确 ClaimRevisionRef、Evidence 和 Provenance、Scope、Attestor 身份、Method 及其不可变版本、适用的 I 授权决策、有效时间/记录时间上下文，以及更正/撤销谱系。
5. Claim 可以没有任何 Fact。Verified Claim 不会自动生成 Fact。Fact 可以确认、限定、收窄或替代一个或多个精确 Claim 修订。
6. 历史 ClaimRevision 和 FactRevision 只能追加，禁止静默覆盖。Fact 不得追随 Claim 可变的 latest revision。

## 3. 身份与修订方案

采纳 I1：

- ClaimRef 在声明的身份与 Scope 边界内标识一个稳定命题。
- 每个不可变断言状态具有精确 ClaimRevisionRef。
- FactRef 标识一个稳定的受治理 Attestation 线程。
- 每个不可变 Attestation 状态具有精确 FactRevisionRef。
- 改变命题身份的变化创建新 Claim；不改变身份的 Evidence、Provenance、认知状态或编辑性更新，在现有 ClaimRef 下创建新的 ClaimRevision，并遵循当前 DOMAIN-MODEL-001 §2.4 的分类规则。
- Attestation 结果或其 Evidence/Method 基础发生变化时创建新的 FactRevision，禁止原地修改。
- Scope 变化不得转移身份或访问权。跨 Scope 授权必须独立检查。

采纳当前 DOMAIN-MODEL-001 §2.4 已记录的精确 Claim 身份分类作为语义规则。分类存在歧义时必须 fail-closed，并要求明确的受治理决定；禁止仅凭文本相似度合并 Claim。

## 4. 权威职责分配

| 事项 | 权威 |
|---|---|
| Claim/Fact 语义词汇与认知含义 | Domain Model |
| ClaimRef / ClaimRevisionRef / FactRef / FactRevisionRef 规范身份分配、生命周期、修订提交及 ConflictSet 生命周期 | D |
| Principal 与 Attestor 授权、PermissionEpoch、撤销、保留及 Global Forget 策略 | I |
| D ForgetOperation / ForgetFence 生成与排序；I 在其权威范围内绑定策略并判定全局完成 | D + I |
| 不可变物理持久化和原子提交实现 | Storage，遵循 D 的规范提交契约 |
| 候选抽取与提案生成 | E；不得签发规范 ID，也不得仅凭抽取置信度创建 Fact |
| 检索与 Context 消费 | F/G；只允许精确版本绑定引用 |
| Wire 表示、协议 Envelope 和 Adapter Transport | H；本决策不冻结 Wire 字段 |

任何模块都不得从 Scope 推导 Permission，也不得从 Confidence、模型评分或传输 ACK 推导 Truth。

## 5. 消费模块要求

- E / Memory Compiler 保留中立 CandidateProposition 和 ExtractionIR；可以提交 Claim 提案，但不得签发规范身份。只有在存在明确授权的 Attestation 操作以及必要 Evidence/Provenance 时，才允许提交 Fact 提案。
- D 负责规范身份、不可变修订持久化、生命周期及规范 ConflictSet 决策。D 验证 expected-parent/currentness 与提交语义。
- I 使用当前 PermissionEpoch 和策略授权受保护操作及 Attestor。BMCP 和 E 不得复制 I 的权威。
- F/G 消费精确 ClaimRevisionRef 和 FactRevisionRef；禁止语义相似度解析、latest-head 替换或无约束可变查询。
- H 可以传递不透明、精确版本绑定引用。具体 Wire 字段名称、必填性、序列化及 Schema 仍归 H 所有，尚未冻结。
- Storage 持久化不可变修订并实现 D 定义的原子提交边界。本决策不选择物理数据库或拓扑。

## 6. 对账与替代关系

本决策取代 B-ADR-FACT-CLAIM-001 中较早的 C2 / Option B 候选建议。本决策与当前 main 的 DOMAIN-MODEL-001、core-entities.md，以及区分 Fact 与 Claim 的 I-04 / P-04 保持一致。

旧 ADR 文本保留为决策过程的历史证据。本记录仅取代“尚未选择语义方案”这一早期状态。B-ADR-FACT-CLAIM-001 对 Canonical Schema 冻结及下游实现映射仍保持 ADR-BLOCKED，直至其自身 §8 条件均有证据：B/D/E/F/G/H/I 消费者映射、迁移/兼容计划、符合性场景及验证证据。任何消费者都不得将本语义选择视为 Schema 冻结授权。

术语表中的合并条目 Fact / Claim 必须拆分为 Claim、ClaimRevision、Fact 和 FactRevision。当前 BMCP 正式名称继续使用 Brain Memory Context Protocol。

## 7. 明确未作出的决定

本决策不批准 Fact 验证策略、Attestor 角色目录或普遍适用的 Truth 阈值；不冻结字段级 JSON Schema、DDL、索引或数据库拓扑；不授权 Runtime 实施或数据库迁移；不定义 BMCP Wire Payload 字段或 ACK 语义；不关闭物理 Forget、Restore、Publication 或生产验收门禁；不声称存在独立人工审查或签名。

上述事项仍须依据各自证据和验收标准处理。

## 8. 必须执行的后续工作

1. 更新 B ADR 状态和来源 Pin，使其引用本语义选择；在 B-ADR-FACT-CLAIM-001 §8 全部条件得到证据支持前，继续保持 Schema 冻结状态为 ADR-BLOCKED。
2. 对齐规范术语及双语领域读者文档。
3. 更新 Memory Compiler 和 BMCP 工程交接文档，采用 Option A + I1，但不冻结 Wire/Storage Schema。
4. 保持 Issue #7 的 IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE 不变。
5. 在获得授权的 Runtime 仓库和可执行目标之前，将 Runtime 测试记录为 NOT RUN。

## 9. 验收

该语义决策在开发架构基线中正式采纳。具体实现契约仍为 Candidate，直至责任消费者工件完成精确版本登记和审查。
