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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "事实行号取自 origin/main 指定提交快照，未在运行时复验。"
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
    canonical_scope: "运行时 DeliveryState 终态语义、Producer Work 终态责任归属、PublicationParticipant 拒绝准入审计证据关联"
    canonical_scope_id: "RUNTIME-INVARIANT-DECISION-REQUEST-2026-11-28"
    canonical_scope_keywords:
      - "DEF-drift-03"
      - "DEF-drift-04"
      - "DEF-tests-01"
      - "DeliveryState"
      - "Acknowledged"
      - "Producer Work"
      - "Accepted"
      - "PublicationParticipant"
      - "拒绝准入"
      - "运行时不变量"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# 运行时不变量裁决请求（drift-03 / drift-04 / tests-01）

**文档性质：** 提交给 Owner 的运行时不变量裁决请求，供 Owner 对以下三条已由独立裁定方认定为 HIGH 的运行时缺陷作出明确裁决。

**事实基线：** `origin/main`。本文所有代码位置及行号均以该基线为准。

**文件效力：** 本文件仅陈述已提供的事实、列明待裁决问题及各选项的后果，并声明裁决前的实现冻结要求。本文件不构成规范，不新增或修改任何规范性约束，也不代表 Owner 已作出批准或裁决。

## §1. DEF-drift-03 —— 两套同名 `DeliveryState`，ACK 被当作终态

**事实：**
- `crates/agent-integration/src/lib.rs:462`：`DeliveryState` 包含 `Delivered`、`Received`、`Accepted`、`Applied`、`Rejected`、`Expired`、`Superseded`；`:474` 的 `is_terminal` 返回 `Applied | Rejected | Expired | Superseded`。
- `crates/memory-context/src/delivery_lifecycle.rs:36`：另一套同名 `DeliveryState` 包含 `Pending`、`Delivered`、`Acknowledged`、`Superseded`、`Abandoned`；`:53` 的 `is_terminal` 返回 `Acknowledged | Superseded | Abandoned`。
- `crates/memory-context/src/delivery_lifecycle.rs:305`：ACK 处置为 `Current` 时执行 `record.state = DeliveryState::Acknowledged;`。
- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-state-semantics.md:87`：`Acknowledged` 不证明超出该 ACK 声明范围的更强操作，可能是 `Applied` 的必要条件而非充分条件；`README.md:130`：传输成功不构成应用成功的证据。
- 独立裁定方于 2026-11-28 裁定：真缺陷，HIGH 成立；最小边界为「ACK 只记录传输确认，不得解释为应用成功」；两套枚举的统一属于更大范围，不混入本缺陷。
- 当前阻塞点：需 Owner 裁定 `Acknowledged` 是否允许继续作为内部终态。

**待 Owner 裁决的问题：**

`Acknowledged` 是否允许继续作为 `memory-context` 内部终态？

**选项及后果：**
- 选项 A：允许 `Acknowledged` 继续作为内部终态，其终态含义仅限于对应 ACK 所声明的传输确认，不代表应用成功。
- 选项 B：不允许 `Acknowledged` 作为内部终态，其终态含义不再由 ACK 确认本身成立，应用成功与传输确认继续保持不同的状态语义。

## §2. DEF-drift-04 —— Producer Work 直接写入 `Accepted`

**事实：**
- `crates/memory-compiler/src/admission.rs:23`：`WorkState` 枚举包含 `Accepted`、`Published`、`Rejected`、`Cancelled`、`Terminal` 等状态。
- `crates/memory-compiler/src/admission.rs:578`：`transition_work_state` 校验 `legal_transition` 并持久化新状态。
- `crates/memory-compiler/src/admission.rs:648`：`register_producer_work`；`:684` 的 INSERT 直接把 `state_json` 写成 `encode(&WorkState::Accepted)`。
- 生产路径未调用 `transition_work_state`，该函数当前仅有测试调用。
- `04-memory-compiler/compiler-state-and-producer-admission.md:222`：终态断言由 D 拥有接受权，E 不得仅凭本地状态关闭 D barrier 项；`04-memory-compiler/accepted-receipt-and-idempotency-contract.md:62`：`ProducerRegistrationReceipt` 只证明工作项已被持久准入，不证明工作已运行、输出存在、依赖已注册或发布成功。
- 独立裁定方于 2026-11-28 裁定：真缺陷，HIGH 成立；不得把 `Accepted` 直接改成某个终态，也不得仅为通过检查而增加自动终结；worker 失败、丢失或重启时的终态归属须沿用既有业务语义。
- 当前阻塞点：需 Owner 裁定 worker 未完成或丢失时，工作项由哪个责任方、依据什么证据转入哪个既有持久终态。

**待 Owner 裁决的问题：**

worker 未完成或丢失时，工作项应由哪个责任方依据什么证据决定是否转入哪个既有持久终态？

**选项及后果：**
- 选项 A：由拥有工作执行结果确认责任的一方作出终态决定，并以其可确认的持久执行结果作为依据；工作项终态归属随该责任方的业务语义确定。
- 选项 B：由拥有 Producer Work 准入及工作项管理责任的一方作出终态决定，并以其能够确认的持久失败或丢失证据作为依据；工作项终态归属随该责任方的业务语义确定。
- 选项 C：worker 未完成或丢失本身不足以构成终态证据；在缺少 Owner 明确认可的终态责任方及证据依据时，不据此认定工作项已达到既有持久终态。

## §3. DEF-tests-01 —— 拒绝准入返回通用 `Suppressed`

**事实：**
- `crates/memory-compiler/src/lib.rs:653-656`：当 `!proof.publication_participant_admitted || !proof.protected_visibility_authorized` 时，直接返回 `Ok(PublishedDerivative { derivative: staged, disposition: PublicationDisposition::Suppressed })`。
- `04-memory-compiler/extraction-and-normalization.md:444`：成功准入的 Producer participant MUST 获得可审计的拒绝处置。
- 同一规范位置要求该处置显式绑定精确的 rejected `PublicationParticipant` identity、对应的 `StorageVisibilityParticipantRef` 与精确 publication tuple identity。
- 同一规范位置明确规定，通用操作级 suppression disposition MUST NOT 满足上述要求。
- 独立裁定方于 2026-11-28 裁定：真缺陷，HIGH 成立；保留既有 `Suppressed` disposition，不新增公开 disposition、不改 wire schema，仅补内部可审计证据。
- 当前阻塞点：需 Owner 确认证据载体——三个身份字段是否必须作为同一条拒绝准入记录的不可分割关联键持久化。

**待 Owner 裁决的问题：**

三个身份字段是否必须作为同一条拒绝准入记录的不可分割关联键持久化？

**选项及后果：**
- 选项 A：必须作为同一条拒绝准入记录的不可分割关联键持久化；该记录整体关联精确的 rejected `PublicationParticipant` identity、对应的 `StorageVisibilityParticipantRef` 与精确 publication tuple identity。
- 选项 B：不要求三个身份字段位于同一条拒绝准入记录；三个字段可以分别持久化，但其关联关系仍须能够明确对应同一次拒绝准入处置。

## §4. 裁决前冻结与文件效力

**裁决前冻结声明：**

上述三条缺陷均已由独立裁定方认定为 HIGH，且各自存在尚待 Owner 明确的运行时不变量裁决事项。

在 Owner 对 §1、§2、§3 分别作出明确裁决之前，相关实现不得改动。

本声明适用于上述三条缺陷涉及的相关实现，不因其中某一条缺陷已被讨论、某一选项已被提出或某一项事实已被确认而自动解除。选项的列出不构成选择、批准或实施授权。

**非规范声明：**

本文件是提交 Owner 的裁决请求，不是规范、设计决议、实现契约或规范性解释文件。

本文件中的事实陈述以指定的 `origin/main` 基线为准；裁定结论是独立裁定方于 2026-11-28 给出的缺陷等级及边界判断，不等同于 Owner 对待裁决问题的正式决定。

本文列出的选项仅用于明确各项待裁决问题及其后果，不表示任何选项已被采纳或优先认可。

本文件不构成对现有规范的修改、豁免、替代或补充，也不构成任何实现变更的授权。相关规范及既有业务语义的效力不因本文件的创建而改变。
