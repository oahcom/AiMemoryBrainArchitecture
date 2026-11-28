---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-350/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Repair instructions for AID-2026-350: runtime invariant decision request for DEF-drift-03, DEF-drift-04 and DEF-tests-01."
    canonical_scope_id: "ai-development/aid-2026-350-prompt-v1"
    canonical_scope_keywords:
      - "AID-2026-350"
      - "prompt"
      - "runtime invariant"
      - "owner decision"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

你是 GitHub 仓库 `oahcom/AiMemoryBrainArchitecture` 的作者。你没有该仓库的读写权限，也不能运行命令或访问网络。你的唯一输出是可逐字落盘的编辑块。

## 任务
输出一份**新增** Markdown 文档的完整内容：一份提交给 Owner 的「运行时不变量裁决请求」，覆盖三条已裁定为 HIGH 的运行时缺陷。文档只做三件事：(1) 陈述事实；(2) 每条缺陷给出一个待裁决问题并列出每个选项的后果；(3) 声明裁决作出前相关实现不得改动，且本文件不构成规范。

## 落位（唯一文件）
`14-ai-development/work-items/AID-2026-11-28-RUNTIME-INVARIANT-DECISION-REQUEST/RUNTIME-INVARIANT-DECISION-REQUEST-2026-11-28.md`

## 事实（逐字采用，行号即基线，不得改写、不得新增仓库中不存在的位置）
基线：`origin/main`。

### DEF-drift-03 —— 两套同名 `DeliveryState`，ACK 被当作终态
- `crates/agent-integration/src/lib.rs:462`：`pub enum DeliveryState { Delivered, Received, Accepted, Applied, Rejected, Expired, Superseded }`；`:474` 的 `is_terminal` 返回 `Applied | Rejected | Expired | Superseded`。
- `crates/memory-context/src/delivery_lifecycle.rs:36`：另一套同名枚举 `DeliveryState { Pending, Delivered, Acknowledged, Superseded, Abandoned }`；`:53` 的 `is_terminal` 返回 `Acknowledged | Superseded | Abandoned`；`:305` 在 ACK 处置为 `Current` 时执行 `record.state = DeliveryState::Acknowledged;`。
- 规范锚点 `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-state-semantics.md:87`：`Acknowledged` 不证明超出该 ACK 声明范围的更强操作，可能是 `Applied` 的必要条件而非充分条件；`README.md:130`：传输成功不构成应用成功的证据。
- 裁定结论（独立裁定方，2026-11-28）：真缺陷，HIGH 成立；最小边界为「ACK 只记录传输确认，不得解释为应用成功」；两套枚举的统一属于更大范围，不混入本缺陷。
- 阻塞点：需 Owner 裁定 `Acknowledged` 是否允许继续作为内部终态。

### DEF-drift-04 —— Producer Work 直接写入 `Accepted`
- `crates/memory-compiler/src/admission.rs:23`：`WorkState` 枚举（含 `Accepted`、`Published`、`Rejected`、`Cancelled`、`Terminal` 等）。
- `:578` `transition_work_state` 校验 `legal_transition` 并持久化新状态；`:648` `register_producer_work`；`:684` 的 INSERT 直接把 `state_json` 写成 `encode(&WorkState::Accepted)`，生产路径未调用 `transition_work_state`（该函数当前仅有测试调用）。
- 规范锚点 `04-memory-compiler/compiler-state-and-producer-admission.md:222`：终态断言由 D 拥有接受权，E 不得仅凭本地状态关闭 D barrier 项；`04-memory-compiler/accepted-receipt-and-idempotency-contract.md:62`：`ProducerRegistrationReceipt` 只证明工作项已被持久准入，不证明「工作已运行、输出存在、依赖已注册或发布成功」。
- 裁定结论（独立裁定方，2026-11-28）：真缺陷，HIGH 成立；不得把 `Accepted` 直接改成某个终态，也不得仅为通过检查而增加自动终结；worker 失败/丢失/重启时的终态归属须沿用既有业务语义。
- 阻塞点：需 Owner 裁定 worker 未完成或丢失时，工作项由哪个责任方、依据什么证据转入哪个既有持久终态。

### DEF-tests-01 —— 拒绝准入返回通用 `Suppressed`
- `crates/memory-compiler/src/lib.rs:653-656`：`if !proof.publication_participant_admitted || !proof.protected_visibility_authorized { return Ok(PublishedDerivative { derivative: staged, disposition: PublicationDisposition::Suppressed }) }`。
- 规范锚点 `04-memory-compiler/extraction-and-normalization.md:444`：成功准入的 Producer participant MUST 获得可审计的拒绝处置，且该处置 MUST 显式绑定精确的 rejected PublicationParticipant identity、对应的 `StorageVisibilityParticipantRef` 与精确 publication tuple identity；通用操作级 suppression disposition MUST NOT 满足该要求。
- 裁定结论（独立裁定方，2026-11-28）：真缺陷，HIGH 成立；保留既有 `Suppressed` disposition，不新增公开 disposition、不改 wire schema，仅补内部可审计证据。
- 阻塞点：需 Owner 确认证据载体——三个身份字段是否必须作为同一条拒绝准入记录的不可分割关联键持久化。

## frontmatter 要求（完整 `document_metadata`，YAML 顶层键顺序照抄下列结构）
- `domain: ai-development`
- `role: work-record`
- `lifecycle.approval`：`decision_status: Draft`、`approver: null`、`decision_date: null`、`approved_version: null`、`approval_scope.type: Full-document`、`approval_applicability: Not-Applicable-To-Current-Version`、`evidence_reference: []`、`revocation: null`
- `lifecycle.evidence_verification`：`verification_status: Unverified`、`last_verified_date: null`、`last_verification_note` 说明「事实行号取自 origin/main 指定提交快照，未在运行时复验」
- `lifecycle.usage_status: Active`、`lifecycle.modification_status: New`
- `lifecycle.supersession`：`supersedes: []`、其余字段 `null`
- `lifecycle.archival`：全部 `null`
- `authority.canonical_status: Non-Canonical`、`canonical_scope`/`canonical_scope_id`/`canonical_scope_keywords` 按内容填写、`canonical_conflict_status: None`、`canonical_conflict_resolution: null`、`normative_status: Informative`
- 顶层 `steward: "user-authorized operator (delegated by account owner)"` —— 必须逐字，不得改写
- 不要声明 `bilingual_counterpart`，不要声称存在任何镜像文件

## 正文结构
1. 标题：`# 运行时不变量裁决请求（drift-03 / drift-04 / tests-01）`
2. 头部要点：文档性质（提交 Owner 裁决的请求）、基线（`origin/main`，文中行号以该基线为准）、文件不构成规范
3. §1 / §2 / §3 各节：每条缺陷先用**不超过 6 行**陈述事实（代码位置、规范位置、裁定结论）；然后给出**一条**待裁决问题（单句，可用有限选项回答）；再逐行列出每个选项的后果（每选项一行，形如 `- 选项 A：<后果>。`）
4. §4：裁决前冻结声明（裁决作出前，相关实现不得改动）+ 本文件非规范声明

## 硬约束
- 不写代码改动、补丁、diff、伪代码；不给实现建议、技术方案推荐、修复顺序
- 不写计划、时间表、里程碑、负责人指派
- 不得替 Owner 作决定；不得把任何选项标为「推荐」，也不得用措辞暗示倾向；不得声称已获批准或已裁决
- 不得引入上述事实之外的仓库位置、文件或行号
- 正文用中文；代码标识符、路径、枚举名、字段名保留原文

## 输出契约（逐字，只输出这一个块，块外不写任何文字）
===FILE: 14-ai-development/work-items/AID-2026-11-28-RUNTIME-INVARIANT-DECISION-REQUEST/RUNTIME-INVARIANT-DECISION-REQUEST-2026-11-28.md|CREATE===
---NEW---
<完整文件内容>
===END===
