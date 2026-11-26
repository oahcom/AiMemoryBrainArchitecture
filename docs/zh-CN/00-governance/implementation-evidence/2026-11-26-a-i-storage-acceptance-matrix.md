---
document_metadata:
  domain: architecture
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Informative Chinese mirror; no Owner acceptance implied."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "中文决策验收证据镜像"
    canonical_scope_id: "governance/decision-acceptance/zh-CN/system-matrix"
    canonical_scope_keywords:
      - decision-acceptance
      - evidence
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md"
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md"
---

# A–I + Storage 系统级验收矩阵 — AID-2026-11-26-DECISION-ACCEPTANCE-03

> 本矩阵用于追踪责任与证据缺口，不是 conformance 声明。观察到的 main 基线：`d914e8a1f8a1ba24c21c41a9249489d544388185`；合并前重新核对 HEAD。
> 授权归属：`user-authorized operator (delegated by account owner)`；Owner 指定日期：2026-11-26。不推断 Owner 接受或生产证据。

## 系统链路矩阵

| 链路/不变量 | 生产者 | 消费者 | 权威 Owner | 依赖 Owner | 规范源 / DEC | Focused Issue | 失败、恢复、重试、未知状态 | 验收证据 | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| Event ingress → durable acceptance → Compiler → canonical commit | ingress/admission；E 产生 compiler lifecycle/completion | E Compiler，再到 D canonical commit | E 管编译生命周期；D 独占 canonical state | A、D、E、Storage/Consistency、I 授权输入 | E Overview 为候选；D source 在 #1212 观察基线缺失；DEC-08 | #1177 #1184 #1212 | 持久 admission identity；重复请求幂等；明确 retry receipt；unknown 通过持久 receipt 读取对账，不能猜测；提交前失败不得产生 canonical 效果 | 精确生产者/消费者契约；边界崩溃测试；重放/重复测试；Storage 接受 | BLOCKED |
| D Canonical Commit → durable outbox/receipt → F consumer | D 在同一事务产生 canonical-change event | F 消费；E projection request 非权威 | D | E、F、Storage/Consistency、A | D source 在观察 main 缺失；DEC-08 | #1177 #1184 #1212 | commit/outbox 原子；稳定事件身份；F 去重；从持久 receipt/cursor 重放；unknown 由 receipt 对账 | 事务边界、线性化点、崩溃/重启/重放证据；D/E/F 和 Storage 精确版本接受 | BLOCKED |
| F Retrieval / Index / Watermark / Scan Coverage | D 权威 feed；F scanner/indexer | F retrieval/index；G 消费候选 | D 管 canonical cursor/change；F 管 index/watermark | A、D、F、Storage | F normative root 缺失；DEC-07/09 | #1179 #1184 #1212 | 仅推进连续前缀；gap 阻断；重复去重、乱序排序；从 watermark 重放；visible/irrelevant/filtered/gap 区分；unknown 不得视为已扫描 | scanned_through 证明；gap/replay 测试；精确 source/mirror；F Owner 接受 | BLOCKED |
| D Forget Fence → E/F/G/Storage 发布与可见性门 | 按方向由 D 作为逻辑 Fence/version 签发者（仅方向，未验证实现） | E/F/G 派生发布、读取、缓存、队列、重放、恢复路径；Storage 通过 D 派生且可重建的 fence projection 执行物理门控，不得独立签发 generation/cursor 或授权发布 | D 管 Fence 机制；I 管全局政策 | D、E、F、G、I、Storage；涉及 adapter 时 H/C | DEC-10/15；D-FORGET-CONTRACT-001 @ `760a1d48011f2a66c23abcf825a3d067e79b8821`（Draft/Unverified/Informative；Owner 接受待定）；System Boundaries @ `c2aa6823b69313ba27c34625f87f29d2be356606`（Draft/Unverified/Normative） | #1125 #1211 #1209 #1208 #1177 #1212 | 旧 Fence 输出抑制；竞态有线性化点；重试/迟到发布重新检查 Fence；unknown fail closed；旧缓存/索引/队列/重放/恢复不能重新可见 | 每步 issuer/token/linearization/idempotency/failure/visibility 转移表；竞态、崩溃、恢复、陈旧派生物测试；所有权威行接受 | BLOCKED |
| G ContextVersion → Delivery Intent → C/H Accepted evidence | G 创建 ContextVersion/Intent；C/H 各自发出 Accepted 证据 | G 持久化引用；C/H 保留事实权威 | G 管 ContextVersion/Intent；C/H 管各自 Accepted | B、C、G、H，必要时 D/I | G Context Version、C inference boundary、H candidate；DEC-11 | #1180 #1212 | 稳定 Attempt；重复/迟到 ACK 幂等；retry/Unknown/supersession 明确；G 不制造 Accepted；Received/Delivered/Accepted 不混淆 | 持久证据引用、Attempt 绑定、重试/重放测试；C/H/G 精确版本接受 | OPEN |
| C/H Inference Boundary → Applied evidence | H transport/protocol；C inference-boundary evidence；G 评估完整 predicate | G Applied projection / 下游消费者 | C 管推理边界事实；H 管协议完整性；G 管 Applied 状态 | B、C、G、H、D/I 输入 | C inference-boundary；H BMCP candidate；G Applied draft；DEC-11/12 | #1180 #1212 | Accepted 不等于 Applied；Applied 不代表模型理解/使用；timeout/Unknown 不得强制转成成功；重放不能复用过期授权 | 完整 predicate 和类型化证据；状态正反例；持久 ledger/崩溃证据；联合 Owner 接受 | BLOCKED |
| I Authorization / PermissionEpoch / Revocation | I 政策/授权权威 | 所有生产者、读取者、发布门 | I | A–H 及承担执行的 Storage | I normative root 在观察 main 缺失；#1202；DEC-15/16 | #1202 #1208 #1212 | revocation/epoch 变化使旧 permit 失效；expiry/unknown fail closed；重试重新评估当前授权；下游 Owner 不替代 I 政策 | I 逐文件精确源/审批；epoch/revocation 契约；跨 Owner 负例；main pins | BLOCKED |
| Global Forget inventory / evidence / completion | I 管全局 inventory/policy；D 按方向为 canonical Fence 逻辑权威（仅方向，未验证实现）；执行者各自产生证据 | 全局完成评估/审计 | I 管全局政策/完成标准；D 管 canonical Forget/Fence；完成需联合判定 | D 和每个相关执行 Owner；Storage/Consistency | D-FORGET-CONTRACT-001 @ `760a1d48011f2a66c23abcf825a3d067e79b8821`；System Boundaries @ `c2aa6823b69313ba27c34625f87f29d2be356606`；#1208；DEC-15；#1212 | #1208 #1209 #1212 | inventory/证据缺失即未完成；executor unknown 阻断；稳定 operation ID 对账重试；D 或 I 均不得单方宣布全局完成 | 版本化 inventory/evidence 契约；逐目标证据；D + 每个相关执行 Owner 接受；端到端验证 | BLOCKED |
| Storage Atomicity / Durability / Recovery / Restore | Storage/Consistency 产生物理事务与持久化事实 | D/E/F/G/H 和全局门 | Storage/Consistency 管物理实现；逻辑权威仍属于领域 Owner | A、D、E、F、G、H、I | #1212 未建立 Storage 精确规范源；DEC-08/10/15 | #1177 #1184 #1209 #1211 #1212 | commit/outbox 原子；receipt 持久；重试幂等；崩溃一致性；恢复保留 Fence/watermark/receipt；unknown 对账；内存模型不能证明持久性 | 精确 Storage 契约；故障注入、崩溃/重启、持久性、恢复/回滚证据；Storage Owner 接受 | BLOCKED |
| A–I + Storage 全局不变量 I-01…I-24 | 委托裁决表已逐项记录权威责任分配 | 委托裁决表已逐项记录依赖 Owner | `user-authorized operator (delegated by account owner)` 已作出最终责任分配；不推定任何领域 Owner 已接受 | Owner A 负责协调；每行权威 Owner 与依赖 Owner 保留其自身合同接受权 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9`；下方委托映射表；DEC-12 | #1212 及 Focused Issues | 每行已记录来源、映射理由和 Gate A 审查方法；精确版本 Owner 处置仍待完成 | 24 行分别包含原文、Owner/依赖映射、审查方法和待决处置 | PARTIAL |


## DEC-12 — 分阶段关闭：审查门与生产门（Owner 已确认；Gate A 证据待完成）

**方向来源：** [#1212 评论 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311) 记录 Owner C 的分阶段关闭方向：架构审查工作流单独关闭；生产集成验证属于独立验收门。[#1212 评论 7174315211](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174315211) 明确未实现/未验证项保持 BLOCKED / NOT VERIFIED，并指出系统矩阵、规范源基线、跨 Owner 证据和不变量追踪未完成前不得关闭 #1212。验收清单见 [#1212 评论 7174866924](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174866924)。

### Gate A — 仅在以下条件满足后，才可建议将 Architecture Review 工作流标记为 CLOSED

1. 精确提交版本的审查包完整：DEC-01..DEC-20 分别可追踪，18 个唯一方向的去重关系明确。
2. 每条系统流程均列出生产者、消费者、权威 Owner、依赖 Owner、精确规范源路径/Blob、Focused Issue、失败/恢复/未知状态语义及所需证据。
3. I-01..I-24 均保留逐字源声明，并逐项列出最终委托 Authority Owner / Dependent Owners（`OWNER_CONFIRMED`）。这仅是委托操作人的责任分配；Gate A 仍要求 Owner A 和每个相关领域 Owner 对其权威责任行提交自己的精确版本处置。
4. Canonical、EN、ZH-CN 文件具有精确源修订引用、稳定 ID 对齐、决策状态一致和双语语义一致；CI 仅是机械证据，不能替代语义审查。
5. 记录的工作流关闭决策 Owner C 接受精确版本的审查包；Owner A 协调；每个相关领域 Owner 与 Storage/Consistency 接受其权威范围内的审查行。所有决定及异议/延期均绑定该精确版本。
6. 所有未解决的实现与生产符合性项目继续明确标为 BLOCKED / NOT VERIFIED，并有具名后续 Issue；不得因审查关闭而升级状态。

### Gate B — Production Integration / Conformance 独立验收

Gate B 需要单独的精确版本及环境证据：集成实现/构建身份；D/E/F/G/H/I 契约符合性；Storage 原子性、持久性、崩溃/重启及恢复证据；针对重试、重复、未知、撤销、Forget/Fence 和可见性的正反端到端测试；声称生产符合时的当前生产配置/部署身份；以及相关领域 Owner、Storage/Consistency 与 Owner A 的接受。Gate A 结果、文档存在、CI 通过、设计批准或审查关闭均不得被推定为 Gate B 通过。

### Owner C 决定已记录（2026-11-26）

该分阶段关闭决定已记录在下方及 #1212 评论 7182752736；DEC-12 的决定措辞已无待决项。当前阻塞是证据和精确版本跨 Owner 处置，而不是分阶段关闭规则本身。

**Owner C 确认已记录（2026-11-26）：**“我确认：一旦满足 Gate A 的精确版本审查产物与跨 Owner 接受标准，即可将 Architecture Review 工作流标记为 CLOSED，即使实现或 Production Integration/Conformance 行仍为 BLOCKED / NOT VERIFIED；此类审查关闭不构成、不意味着、也不豁免独立的 Gate B 生产验收。”

**记录归属：** `user-authorized operator (delegated by account owner)`。此记录表示已收到以 Owner C 角色提供的委托确认，不伪造自然人的 GitHub 签署身份。

DEC-12 状态：**OWNER_CONFIRMED_GATE_A_PENDING**。分阶段 Gate A/Gate B 规则及 I-01..I-24 委托责任映射已确认，但 Gate A 尚未满足；跨 Owner 精确版本处置及完整组合审查包仍未完成。**#1212 在精确版本审查产物与跨 Owner 接受完成前继续保持 OPEN。** Gate B 生产验收仍独立且强制；不推定任何生产接受。

## 事实词汇不得互相替代

- `Received`：接收方/传输事实，不等于 Accepted。
- `Delivered`：交付事实，不证明接收方接受。
- `Accepted`：C/H 权威证据，不等于 G Applied。
- `Applied`：G 完整 predicate 和持久证据，不等于模型理解或使用。
- `CanonicalCommitted`：D canonical transaction 事实，不等于已索引。
- `Indexed`：F 索引消费事实，不证明扫描覆盖完整。
- `scanned_through`：连续扫描覆盖证明，不是最后可见记录游标。

除非规范转移契约明确规定，不得从一个事实推断另一个事实。

## I-01…I-24 追踪——历史缺口说明（已由下方裁决取代）

在早期证据接收阶段，DEC 清单和 #1212 记录尚未展示全部 24 项不变量原文及逐行 Owner 映射。该历史缺口现已由下方固定精确来源的 24 行委托裁决取代。当前表记录委托操作人作出的 OWNER_CONFIRMED 责任分配；不推定任何列出的领域 Owner 已接受。

每行均记录精确不变量原文、权威 Owner、依赖 Owner、来源 Blob、Focused Issue、Gate A 审查方法，以及独立的待提交精确版本 Owner 处置。不得用聚合 checkbox 代替 24 行逐项记录。

## 系统级结论

矩阵编制属于文档证据工作，不证明物理原子性、持久化、端到端重试/恢复、当前生产符合性或任何领域 Owner 的接受。#1212 在自身条件满足前保持 OPEN。


## I-01…I-24 逐项追踪——历史 PROPOSED 快照

来源：`00-governance/architecture-invariants.md`，观察到的 Blob：`a5a51937133d43585d970cad02dcfd20925078d9`。以下逐项内容对应来源文件中的 24 条不变量。当前元数据为 `decision_status: Under-Review`、批准人/日期 `NOT_RECORDED`、`approval_applicability: Not-Applicable-To-Current-Version`、`evidence_verification: Unverified`、`usage_status: Active`、`modification_status: Pending-Reapproval`、`normative_status: Normative`。PR #1221 同时修订 GOV-DOC-001 §4.3.1，规定 Normative 内容在 Pending-Reapproval 期间仍保持约束力。但来源正文仍将该组标为 CANDIDATE / NOT APPROVED，并称其须等待单独批准；DEC-13 也记录当前没有正式批准。本矩阵不推断正式批准，也不擅自解决正文状态与元数据政策约束力规则之间的张力；该问题继续作为 Gate A / DEC-13 治理事项保持 OPEN。

| ID | 不变量首句（逐字） | 原文首句 | 权威 Owner（PROPOSED） | 依赖 Owner（PROPOSED） | PROPOSED 映射依据（尚未接受） | 规范源 | Focused Issue | 所需验证证据 | 状态 |
|---|---|---|---|---|---|---|---|
| I-01 | The Brain is the logical authority for canonical memory assets and the memory context it manages. | The Brain is the logical authority for canonical memory assets and the memory context it manages. | PROPOSED：Owner D | PROPOSED：Owner B, E, F, G, H, I, Storage/Consistency | Canonical Memory 及其管理的 Context 需要统一逻辑权威；D 管 canonical 状态，其余领域消费或持久化。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-02 | Agents do not define or override the Brain's internal memory organization rules. | Agents do not define or override the Brain's internal memory organization rules. | PROPOSED：Owner B | PROPOSED：Owner D, E, F, G, H | 这是 Agent 不得重定义 Brain 内部规则的跨系统架构边界；B 负责架构边界，各子系统 Owner 在接口处落实。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-03 | The Brain is independent of any specific Agent framework, LLM, or inference vendor. | The Brain is independent of any specific Agent framework, LLM, or inference vendor. | PROPOSED：Owner B | PROPOSED：Owner C, D, E, F, G, H, I, Storage/Consistency | 框架/供应商独立性属于架构可移植性约束；B 管边界，各集成领域避免供应商特定机制成为权威。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-04 | Event, Memory, Fact, Entity, Relation, and Evidence are distinct domain concepts. | Event, Memory, Fact, Entity, Relation, and Evidence are distinct domain concepts. | PROPOSED：Owner B | PROPOSED：Owner C, D, E, F, G, H | Event/Memory/Fact/Entity/Relation/Evidence 的区分是领域语义；B 管领域模型，实施领域保持区分。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-05 | Every derived memory retains provenance to its source evidence or explicitly records why provenance is unavailable. | Every derived memory retains provenance to its source evidence or explicitly records why provenance is unavailable. | PROPOSED：Owner D | PROPOSED：Owner E, F, G, H, Storage/Consistency | 派生记忆的 canonical provenance 必须可审计；D 负责 canonical provenance，E 产生编译来源，其余下游保留引用。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-06 | Intent, plan, prediction, and pending action are not automatically treated as completed outcomes or verified facts. | Intent, plan, prediction, and pending action are not automatically treated as completed outcomes or verified facts. | PROPOSED：Owner B | PROPOSED：Owner C, D, E, G, H | 意图/预测/待执行与已完成事实的区分属于领域状态语义；B 定义规则，C/H/G 与 D/E 落实生命周期边界。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-07 | Editing Memory Context does not directly mutate Canonical Memory. | Editing Memory Context does not directly mutate Canonical Memory. | PROPOSED：Owner D | PROPOSED：Owner G, E, Storage/Consistency | 该不变量防止 Context 编辑旁路修改 Canonical Memory；D 负责 canonical 变更权，G 负责 Context 编辑与版本化。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-08 | Removing a context entry is not equivalent to forgetting or deleting its canonical memory. | Removing a context entry is not equivalent to forgetting or deleting its canonical memory. | PROPOSED：Owner G | PROPOSED：Owner D, I, Storage/Consistency | 该区分起于 Context 移除边界；G 负责 Context 移除，D 负责 canonical Forget 机制，I 负责全局 Forget/Retention 政策。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-09 | Context changes are versioned and tied to a base version or an explicit full-snapshot transition. | Context changes are versioned and tied to a base version or an explicit full-snapshot transition. | PROPOSED：Owner G | PROPOSED：Owner H, C, Storage/Consistency | Context base-version 与 full-snapshot 转换属于 G 的 ContextVersion 语义；H/C 消费版本化交付及推理边界证据。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-10 | A context delivery is Applied only after explicit Adapter acknowledgement. | A context delivery is Applied only after explicit Adapter acknowledgement. | PROPOSED：Owner G | PROPOSED：Owner H, C, Storage/Consistency | Applied 属于 G 的 Context 交付投影，但前置 ACK 来自 Adapter/H 协议边界；C 定义推理边界证据。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-11 | Context changes take effect at a defined inference-context assembly boundary. | Context changes take effect at a defined inference-context assembly boundary. | PROPOSED：Owner C | PROPOSED：Owner G, H | Inference-context assembly boundary 属于 C 的推理语义；G 提供版本化 Context，H 传输并绑定 Adapter 协议证据。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-12 | Memory content is untrusted data and never acquires system/developer instruction authority. | Memory content is untrusted data and never acquires system/developer instruction authority. | PROPOSED：Owner C | PROPOSED：Owner G, H, I, B | 推理时的指令权威边界由 C 落实；G/H 携带不可信记忆数据，I 提供安全政策约束。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-13 | Scope and permission are explicit and independently enforced; Agent, task, session, and environment isolation is preserved. | Scope and permission are explicit and independently enforced; Agent, task, session, and environment isolation is preserved. | PROPOSED：Owner I | PROPOSED：Owner A, B, C, D, E, F, G, H, Storage/Consistency | Scope、permission、revocation 与隔离属于安全授权政策；I 掌政策权威，所有子系统及 Storage 路径必须执行。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-14 | Conflicting claims are not silently overwritten; provenance and resolution history remain auditable. | Conflicting claims are not silently overwritten; provenance and resolution history remain auditable. | PROPOSED：Owner D | PROPOSED：Owner B, E, F, G, Storage/Consistency | Canonical claim 冲突、provenance 与解决历史属于 canonical-memory 完整性；D 管 canonical 状态，E/F/G 提供或消费证据。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-15 | Event time, recording time, and validity time are not conflated. | Event time, recording time, and validity time are not conflated. | PROPOSED：Owner B | PROPOSED：Owner D, E, F, G, Storage/Consistency | 三种时间的区分属于共享领域语义；B 定义模型，D/E/F/G 在记录中分别保留事件、记录及有效时间。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-16 | Retries of state-changing protocol operations are idempotent under their defined idempotency scope. | Retries of state-changing protocol operations are idempotent under their defined idempotency scope. | PROPOSED：Owner H | PROPOSED：Owner D, E, F, G, Storage/Consistency | 该不变量约束跨边界状态变更协议的重试；H 负责协议级幂等语义，D/E/G 与 Storage 实现持久操作身份及效果。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-17 | A context version has one authoritative sequence; concurrent changes are serialized or resolved with explicit concurrency control. | A context version has one authoritative sequence; concurrent changes are serialized or resolved with explicit concurrency control. | PROPOSED：Owner G | PROPOSED：Owner H, C, Storage/Consistency | 唯一权威 ContextVersion 序列及并发控制属于 G 的 Context 状态语义；H/C 参与交付与推理边界排序。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-18 | Adapter acknowledgement proves protocol-level application, not model comprehension or behavioral compliance. | Adapter acknowledgement proves protocol-level application, not model comprehension or behavioral compliance. | PROPOSED：Owner H | PROPOSED：Owner C, G | Adapter ACK 是 H 负责的协议事实；C 负责推理边界含义，G 投影 Applied 但不得推断模型理解。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-19 | Context compaction preserves source references and the ability to expand details when retained data permits. | Context compaction preserves source references and the ability to expand details when retained data permits. | PROPOSED：Owner G | PROPOSED：Owner D, E, F, Storage/Consistency | Context 压缩及展开引用属于 G 的 Context 表示；D/E 提供来源 provenance，F 支持检索，Storage 保留持久引用。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-20 | Forgetting and retention governance cover derived records and secondary representations according to declared policy. | Forgetting and retention governance cover derived records and secondary representations according to declared policy. | PROPOSED：Owner I | PROPOSED：Owner D, E, F, G, H, Storage/Consistency | 派生及次级表示的 Retention/Forget 覆盖属于全局政策；I 管清单与完成标准，D 及各执行 Owner 负责具体删除和证据。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-21 | A subsystem boundary does not imply a separate process, service, or crate. | A subsystem boundary does not imply a separate process, service, or crate. | PROPOSED：Owner B | PROPOSED：Owner A, C, D, E, F, G, H, I, Storage/Consistency | 逻辑子系统边界与部署单元的区分属于架构结构；B 负责架构模型，A 协调全系统一致性。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-22 | Performance claims require reproducible measurement on declared hardware, data, and workload. | Performance claims require reproducible measurement on declared hardware, data, and workload. | PROPOSED：Owner A | PROPOSED：Owner B, C, D, E, F, G, H, I, Storage/Consistency | 可复现性及基准条件声明属于跨项目证据治理；A 负责验收/证据规则，相关子系统 Owner 对具体测量主张负责。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-23 | Every architecture design or semantic architecture change must include Chinese and English documentation in the same change set, subject only to the governed temporary exception in GOV-DOC-001. | Every architecture design or semantic architecture change must include Chinese and English documentation in the same change set, subject only to the governed temporary exception in GOV-DOC-001. | PROPOSED：Owner A | PROPOSED：Owner B, C, D, E, F, G, H, I, Storage/Consistency | 同一变更集双语文档要求属于仓库级治理规则；A 协调政策，各设计 Owner 提供两种语言的文档。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |
| I-24 | Architecture documentation acceptance requires bilingual semantic parity, stable-identifier parity, matching decision status, and traceable source revisions. | Architecture documentation acceptance requires bilingual semantic parity, stable-identifier parity, matching decision status, and traceable source revisions. | PROPOSED：Owner A | PROPOSED：Owner B, C, D, E, F, G, H, I, Storage/Consistency | 语义一致、稳定标识符、决策状态及源修订可追溯属于架构文档验收控制；A 负责跨领域门禁，各源 Owner 验证自身内容。 | `00-governance/architecture-invariants.md` @ `a5a51937133d43585d970cad02dcfd20925078d9` | #1212（系统追踪） | Owner A 与相关 Owner 确认此建议映射后，补齐正反证据及精确规范源接受记录 | BLOCKED |

**历史 PROPOSED 快照的 BLOCKED 原因：** 在当时，不变量源文件尚未逐项指定唯一事实生产者/权威 Owner、依赖 Owner 集、Focused Issue 或独立验证产物。该历史映射缺口现已由下方最终委托分配表取代。当前仍待每位列出的 Owner 对精确版本提交自己的处置；来源文件的批准元数据仍未核验，且 DEC-13 不允许推断批准。


## I-01…I-24 最终委托责任映射裁决

**裁决归属：** `user-authorized operator (delegated by account owner)`（委托操作人；非自然人签名）。  
**裁决日期：** 2026-11-26。  
**范围：** 本追踪矩阵中 Authority Owner 与 Dependent Owners 的最终分配。本裁决不代表任何列出的领域 Owner 已接受，不构成不变量源的规范批准、实施授权或 Gate B 生产验收。

前面的 PROPOSED 表原样保留为历史提案快照。以下表格取代其作为当前记录的映射/状态字段。此处 `VERIFIABLE` 表示精确不变量/来源固定点、委托责任分配、依赖集合及 Gate A 审查方法现已逐条可追踪、可复核；**不**表示权威 Owner 或依赖 Owner 已接受精确版本。该项独立处置状态单独列出，当前仍待提交。

| ID | 权威 Owner（OWNER_CONFIRMED） | 依赖 Owner（OWNER_CONFIRMED） | 最终映射裁决／修订理由 | Gate A 追踪审查方法 | 精确版本 Owner 处置 | 状态 |
|---|---|---|---|---|---|---|
| I-01 | OWNER_CONFIRMED：Owner D | OWNER_CONFIRMED：B, E, F, G, H, I, Storage/Consistency | 确认。D 负责规范记忆权威；其余领域负责消费、治理或物理持久化规范资产及其管理的上下文。 | 检查 D 的规范权威合同与 G 的上下文边界；追踪规范写入是否唯一归属于 D，并确认消费者不能创建竞争性的规范事实。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner D=CONDITIONAL；Dependent Owner B=ACCEPT；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-02 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：C, D, E, F, G, H, I, Storage/Consistency | 相较原 PROPOSED 依赖项 D/E/F/G/H 作修订：增加 C 负责 Agent 边界执行、I 负责安全/治理约束、Storage/Consistency 负责持久化边界隔离。 | 将 Agent 接口合同与 Brain 内部组织规则对照；核验 Agent 发起的重定义或覆盖请求会在相关边界被拒绝。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-03 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：C, D, E, F, G, H, I, Storage/Consistency | 确认。B 负责框架无关的领域边界；各集成、子系统、安全及持久化领域必须保持该边界。 | 审查精确接口及架构依赖中的框架/供应商特定权威；核验替换 Agent 框架、LLM 或推理供应商不会改变 Brain 自身语义。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-04 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：C, D, E, F, G, H, I, Storage/Consistency | 确认。B 负责领域概念语义；所列领域必须在各自合同和表示中保留这些区分。 | 检查领域类型目录及相关 schema/API 映射；核验 Event、Memory、Fact、Entity、Relation 和 Evidence 不会被合并或互相替代。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-05 | OWNER_CONFIRMED：Owner E | OWNER_CONFIRMED：B, D, F, G, I, Storage/Consistency | Authority Owner 从原 PROPOSED D 修订为 E：E 的职责章程明确负责 provenance 与派生记忆生产；D 仍负责规范提交/生命周期，而不是编译来源链的生产者。 | 追踪派生记忆输出至类型化来源证据引用，或明确记录 provenance 不可用的原因；核验该 lineage 在 D 规范提交和持久化后仍保留。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner E=CONDITIONAL；Dependent Owner B=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-06 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：C, D, E, G, H | 确认。意图/计划/预测与已完成事实的区分属于 B 负责的领域状态语义；所列生命周期、编译和集成边界不得将前者提升为事实。 | 审查状态/类型转移及正反用例；核验 intent、plan、prediction 和 pending action 未经独立证据不得进入已完成结果或已验证事实状态。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-07 | OWNER_CONFIRMED：Owner D | OWNER_CONFIRMED：E, G, Storage/Consistency | 确认。D 负责规范变更权；G 负责上下文编辑/版本化，E/Storage 仅通过定义好的接口参与。 | 追踪 Context 编辑命令路径与规范写入路径；核验 Context 编辑不会调用或绕过 D 的规范变更操作。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-08 | OWNER_CONFIRMED：Owner G | OWNER_CONFIRMED：D, I, Storage/Consistency | 确认。G 负责上下文条目移除；D 负责规范 Forget 机制，I 负责全局 Forget/Retention 政策。 | 对比 Context Remove 与规范 Forget 操作合同；核验移除上下文条目只改变上下文，不会生成 Forget/删除回执。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner G=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-09 | OWNER_CONFIRMED：Owner G | OWNER_CONFIRMED：C, H, Storage/Consistency | 确认。G 负责 ContextVersion 及 base-version/snapshot 语义；C/H 在推理和协议边界消费该版本。 | 检查 ChangeSet/base-version 与 full-snapshot 转换记录；核验过期 base 更新会被拒绝或显式协调，且每次接受的转换都有版本锚点。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner G=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-10 | OWNER_CONFIRMED：Owner G | OWNER_CONFIRMED：C, H, Storage/Consistency | 确认。G 负责 Applied 投影谓词；C/H 提供推理边界与 Adapter acknowledgement 事实。 | 检查 Applied 谓词及其证据关联；核验缺少显式 Adapter acknowledgement、超时或 Unknown 状态时不会投影为 Applied。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner G=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-11 | OWNER_CONFIRMED：Owner C | OWNER_CONFIRMED：G, H | 确认。C 负责 inference-context assembly 边界；G 提供版本化上下文，H 提供协议/传输证据。 | 固定推理组装边界和上下文版本；核验上下文变更只在该明确边界生效，而不是在编辑或传输交付时自动生效。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner C=ACCEPT；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-12 | OWNER_CONFIRMED：Owner C | OWNER_CONFIRMED：B, G, H, I | 确认。C 在推理边界执行指令权威隔离；B 定义领域含义，G/H 携带数据，I 提供安全约束。 | 检查记忆到推理的信任边界和对抗用例；核验记忆载荷始终是不可信数据，不能取得 system/developer 指令权威。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner C=ACCEPT；Dependent Owner B=ACCEPT；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-13 | OWNER_CONFIRMED：Owner I | OWNER_CONFIRMED：B, C, D, E, F, G, H, Storage/Consistency | 依赖项从原 PROPOSED 的 A/B/C/D/E/F/G/H/Storage 修订：A 负责集成协调，不执行领域边界；I 保留政策权威，所有实际执行边界的领域均列为依赖方。 | 检查 I 负责的授权/scope 政策及各本地执行边界；核验缺少明确 scope 和 permission 时，跨 Agent/task/session/environment 访问会被拒绝。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner I=CONDITIONAL；Dependent Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-14 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：D, E, F, G, I, Storage/Consistency | Authority Owner 从原 PROPOSED D 修订为 B：冲突处理和 claim 语义属于 B 的领域模型；D 保留规范生命周期/历史，E/F/G/I/Storage 提供或执行相邻证据与持久化。 | 检查 conflict/claim 领域模型及规范历史表示；核验竞争 claim 会被保留或显式解决，并保留 provenance 和解决历史，不会被静默覆盖。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-15 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：D, E, F, G, Storage/Consistency | 确认。B 负责时间领域语义；D/E/F/G 和 Storage 必须在记录及投影中保留不同时间维度。 | 检查时间字段定义和往返记录；当值不同时，核验 event time、recording time 和 validity time 仍被分别表示。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-16 | OWNER_CONFIRMED：Owner H | OWNER_CONFIRMED：D, E, F, G, Storage/Consistency | 确认。H 负责协议层重试/幂等语义；D/E/F/G 和 Storage 在各自边界实现持久操作身份及效果。 | 检查精确幂等 scope/namespace 合同及重放回执；核验状态变更重试产生一个定义好的效果，并保留权威原始结果。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner H=CONDITIONAL；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-17 | OWNER_CONFIRMED：Owner G | OWNER_CONFIRMED：C, H, Storage/Consistency | 确认。G 负责权威 ContextVersion 序列及并发策略；C/H 在推理和交付边界消费有序版本。 | 检查 ContextVersion 序列及并发 ChangeSet 解决机制；核验并发更新会被串行化或产生明确冲突/解决结果，不会出现两个权威后继版本。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner G=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-18 | OWNER_CONFIRMED：Owner H | OWNER_CONFIRMED：C, G | 确认。H 负责 Adapter acknowledgement 的含义与完整性；C 负责推理边界解释，G 负责 Applied 投影。 | 检查 ACK schema 和消费者解释；核验 ACK 证据仅证明协议层应用，不会被用于证明模型理解或行为遵从。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner H=CONDITIONAL；Dependent Owner C=ACCEPT；Dependent Owner G=ACCEPT。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-19 | OWNER_CONFIRMED：Owner G | OWNER_CONFIRMED：D, E, F, Storage/Consistency | 确认。G 负责上下文压缩/展开语义；D/E 提供来源 lineage，F 提供检索，Storage 负责持久保留。 | 检查压缩条目及展开引用；核验来源引用在压缩后仍保留，并且在引用数据仍保留时能够展开详情。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner G=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-20 | OWNER_CONFIRMED：Owner I | OWNER_CONFIRMED：D, E, F, G, H, Storage/Consistency | 确认。I 负责全局 Retention/Forget 政策及完成证据；D 和各执行领域负责本地机制与证据。 | 检查受治理目标清单及逐目标处置/证据；核验派生记录和次级表示均被覆盖，且任何缺失/Unknown 目标都会阻止错误宣告完成。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner I=CONDITIONAL；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-21 | OWNER_CONFIRMED：Owner B | OWNER_CONFIRMED：C, D, E, F, G, H, I, Storage/Consistency | 依赖项从原 PROPOSED 的 A/C/D/E/F/G/H/I/Storage 修订：A 负责协调，不拥有或执行子系统实现边界；实际领域和基础设施参与方才是依赖方。 | 对照逻辑子系统图与进程/服务/crate/构建拓扑；核验逻辑边界不会被误解为必须使用独立部署或编译单元。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-22 | OWNER_CONFIRMED：Owner A | OWNER_CONFIRMED：B, C, D, E, F, G, H, I, Storage/Consistency | 确认。A 负责跨项目证据/验收规则；每个领域 Owner 仍对自身性能主张及测量结果负责。 | 检查每项性能主张的硬件、数据集、工作负载、方法和原始可复现结果；核验可在相同声明条件下复现实测。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner A=CONDITIONAL；Dependent Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-23 | OWNER_CONFIRMED：Owner A | OWNER_CONFIRMED：B, C, D, E, F, G, H, I, Storage/Consistency | 确认。A 协调仓库级双语治理规则；每位设计 Owner 负责在同一变更集中提供两种语言的文档。 | 检查变更集是否包含配对的中文/英文文档，以及任何 GOV-DOC-001 例外记录；核验两种语言产物属于同一受治理变更。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner A=CONDITIONAL；Dependent Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |
| I-24 | OWNER_CONFIRMED：Owner A | OWNER_CONFIRMED：B, C, D, E, F, G, H, I, Storage/Consistency | 确认。A 负责跨领域文档验收门禁；每个来源 Owner 验证自身内容的语义和修订版本。 | 比较 canonical/EN/ZH-CN 的语义、稳定标识符、决策状态和来源修订固定点；核验精确审查修订的双语一致性和可追溯性。 | 代理登记处置（2026-11-26；非自然人 Owner 签署）：Coordinator Owner A=CONDITIONAL；Authority Owner A=CONDITIONAL；Dependent Owner B=ACCEPT；Dependent Owner C=ACCEPT；Dependent Owner D=CONDITIONAL；Dependent Owner E=CONDITIONAL；Dependent Owner F=CONDITIONAL；Dependent Owner G=ACCEPT；Dependent Owner H=CONDITIONAL；Dependent Owner I=CONDITIONAL；Dependent Storage/Consistency=CONDITIONAL。所有 CONDITIONAL 保留均须在下方角色条件解除后方可关闭。 | VERIFIABLE |

**当前行数：** 24/24 逐项可追踪；24 行 `VERIFIABLE`；0 行 `BLOCKED_WITH_REASON`。全部 24 行均已写入 Authority/Dependent 代理处置（10 个角色：3 ACCEPT / 7 CONDITIONAL / 0 REJECT）；七项角色条件仍为 OPEN。来源正式批准状态为 Under-Review，且不适用于当前版本（批准人/日期 NOT_RECORDED；证据 Unverified）。其 Normative + Active + Pending-Reapproval 元数据触发 GOV-DOC-001 §4.3.1；但正文仍标为 CANDIDATE / NOT APPROVED。本矩阵不推断正式批准；正文与元数据政策之间的张力继续由 DEC-13 处理并保持 OPEN。

**Gate A 仍为 PARTIAL / OPEN。** 行级追踪现可复核，但在以下条件满足前不得关闭 Gate A：(1) 解除七项明确登记的角色级 CONDITIONAL 保留，并以精确版本证据回读核验；(2) 完整 A–I + Storage/Consistency 组合审查包固定当前来源修订，并补齐每个端到端边界契约（签发者、请求/响应、身份/游标/幂等范围、线性化点、持久回执、失败/Unknown、重放/恢复及可见性）；(3) 解决或明确处置 D、E、F、I 缺失的 current-main 规范根/合同，以及 Storage/Consistency 来源和接受固定点；(4) 将双语/来源修订一致性与完整精确版本审查产物作为一个整体回读核验。这些是 Gate A 审查/接受前置条件，并不要求 Gate B 生产实施先完成。

**Gate B 仍为 NOT VERIFIED**，必须独立提供集成实现、故障/恢复、端到端符合性及生产证据。#1212 保持 OPEN。


## 2026-11-26 跨 Owner 处置——委托代理登记

**授权与归属：** `user-authorized operator (delegated by account owner)`；裁决日期 `2026-11-26`。人类 Owner 已明确授权同一会话代表本记录列出的全部 Owner 角色。尽管如此，下表每项均为代理登记，不是自然人 Owner 签署、平台认证的 Owner 审查，也不证明其他个人亲自签字。处置范围是本矩阵在当前 PR Head 上的责任映射和 Gate A 审查标准；不授予实现授权、规范批准、生产验收或 Gate A 关闭。

**处置规则：** `ACCEPT` 表示接受该角色的责任映射及逐行审查标准；`CONDITIONAL` 表示接受映射，但受该行明确列出的证据/合同条件约束。没有角色给出 `REJECT`。条件处置已被登记，但在证据读回前，其条件仍是 Gate A 的 OPEN 项。

| 角色 | Authority 条款 | Dependent 条款 | 处置 | 条件 / 保留 | 归属 / 日期 |
|---|---|---|---|---|---|
| Owner A | I-22, I-23, I-24（Authority）；I-01…I-24（协调） | — | **CONDITIONAL** | 接受 I-22..I-24 的 Authority 责任，并协调 I-01…I-24 全部条款的 Gate A 审查；Gate A 关闭仍以完整、固定精确版本的 A–I + Storage/Consistency 组合审查包及双语/来源修订一致性为条件。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner B | I-02, I-03, I-04, I-06, I-14, I-15, I-21 | I-01, I-05, I-12, I-13, I-22, I-23, I-24 | **ACCEPT** | 接受其 Authority/Dependent 责任分配及逐行审查标准；对该映射未记录 B 特有保留。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner C | I-11, I-12 | I-02, I-03, I-04, I-06, I-09, I-10, I-13, I-17, I-18, I-21, I-22, I-23, I-24 | **ACCEPT** | 接受其 Authority/Dependent 责任分配及逐行审查标准；对该映射未记录 C 特有保留。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner D | I-01, I-07 | I-02, I-03, I-04, I-05, I-06, I-08, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | 当前 main 缺少 canonical store 规范源。IMPL2 必须恢复该来源，或正式处置并固定来源版本；之后由 D 核验精确 canonical-authority/lifecycle 合同。来源恢复任务不转派给 D。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner E | I-05 | I-01, I-02, I-03, I-04, I-06, I-07, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | 当前 main 缺少或未固定 compiler receipt/idempotency 与 producer/stage 规范合同。IMPL2 必须恢复、正式处置并固定来源；之后由 E 核验 compiler provenance 和派生记忆语义。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner F | — | I-01, I-02, I-03, I-04, I-05, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | 当前 main 的 F 域规范源/合同尚未形成完整精确版本审查锚点。IMPL2 必须恢复、正式处置并固定缺失来源；之后由 F 核验精确 retrieval/derived-record 边界。来源恢复任务不转派给 F。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner G | I-08, I-09, I-10, I-17, I-19 | I-01, I-02, I-03, I-04, I-05, I-06, I-07, I-11, I-12, I-13, I-14, I-15, I-16, I-18, I-20, I-21, I-22, I-23, I-24 | **ACCEPT** | 接受其 context-versioning、delivery 和 compaction 责任分配及逐行审查标准；对该映射未记录 G 特有保留。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner H | I-16, I-18 | I-01, I-02, I-03, I-04, I-06, I-09, I-10, I-11, I-12, I-13, I-17, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | H、E 与 Storage/Consistency 仍需对幂等命名空间、线性化点及 durable replay/Unknown 合同形成一个一致的精确来源锚点。H 接受其协议权威责任，但以该合同被记录为条件。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Owner I | I-13, I-20 | I-01, I-02, I-03, I-04, I-05, I-08, I-12, I-14, I-21, I-22, I-23, I-24 | **CONDITIONAL** | 当前 main 缺少 security-governance 规范根，DEC-13 批准元数据仍未核验。IMPL2 必须恢复、正式处置并固定来源；I 的策略接受以精确来源和批准证据为条件。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |
| Storage/Consistency | — | I-01, I-02, I-03, I-04, I-05, I-07, I-08, I-09, I-10, I-13, I-14, I-15, I-16, I-17, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | 审查包尚未固定物理事务、持久性、崩溃/重启、恢复及可见性精确合同。必须记录精确来源与证据，并读回 Storage/Consistency 自身的审查处置。 | 该处置由代理登记，非自然人 Owner 签署；日期：2026-11-26 |

**计数：** 共 10 个角色处置：3 ACCEPT、7 CONDITIONAL、0 REJECT。覆盖 Owner A、B、C、D、E、F、G、H、I 及 Storage/Consistency。Authority/Dependent 条款覆盖来自上方 24 条已裁决不变量；这不是独立的人类签署。

## Gate A 关闭清单——当前处置

| Gate A 项 | 状态 | 最小关闭条件 / 责任方 |
|---|---|---|
| 分支与当前 main 同步 | SATISFIED | merge base 等于当前 main；merge base 等于 current main；分支不落后 main。ahead 计数会随本分支提交变化，应以 PR 元数据的最新回读为准，不在此固定；若 main 再前进须重新核对。 |
| 跨 Owner 角色处置已登记 | SATISFIED | 10 个角色均有日期明确的代理处置：3 ACCEPT / 7 CONDITIONAL / 0 REJECT。以下七项条件仍为 OPEN，必须解除后才能关闭 Gate A。 |
| 精确 Head CI | OPEN_PENDING_FINAL_HEAD | 在最终文档 Head 上运行全部适用 pull_request workflows，并读回精确 SHA 与结论；不得复用旧 Head 结果。 |
| 完整 A–I + Storage/Consistency 组合审查材料 | OPEN | Owner A 协调一份固定精确版本的组合包；相关 Owner 逐边界固定规范源，并记录 issuer/authority、请求/响应、身份/游标/幂等命名空间、线性化点、持久回执、失败/Unknown、重放/恢复和可见性。 |
| 缺失规范源根/合同（D/E/F/I） | OPEN — IMPL2 | **规范源恢复或正式处置由 IMPL2 负责。** 最小条件：恢复/发布缺失的 current-main 规范根/合同，或记录受治理的“不恢复”决定及精确替代来源锚点。领域 Owner 在恢复后核验自己的合同；不得重复认领 IMPL2 的来源恢复任务。 |
| Storage/Consistency 物理合同与证据 | OPEN — IMPL2 + Storage/Consistency | IMPL2 提供/恢复规范物理事务、持久性和恢复来源及精确 Blob；Storage/Consistency 对照崩溃/重启、恢复和可见性证据审查，并读回对应代理处置条件已满足。 |
| H 幂等命名空间 / 重放边界 | OPEN — Owner H 与 E、Storage/Consistency | 固定一个跨参与边界一致的精确版本命名空间/范围、线性化点、持久回执及 Unknown/重放合同。 |
| 完整审查包双语语义及来源修订一致性 | OPEN — Owner A / 文档 Owner | 读回完整精确 Head 的 Canonical/EN/ZH-CN 审查包；核对语义、稳定 ID、决策状态及每个来源修订锚点。仅矩阵双语一致不足以关闭。 |
| DEC-13 规范批准证据 | OPEN — 治理授权方；适用来源工作由 IMPL2 负责 | 为精确版本的 Invariants/Principles 来源记录真实批准人、批准日期及权威证据，或作出明确保持未批准状态的受治理处置。不得从本代理登记推断批准。 |

**DEC-12：** 仍为 `OWNER_CONFIRMED_GATE_A_PENDING`。Gate A 为 **PARTIAL / OPEN**，尚未 CLOSED。跨 Owner 处置记录已具备，但条件证据、组合审查材料、规范源和双语一致性项目仍为 OPEN。**Gate B 仍为 NOT VERIFIED**，且独立于 Gate A。#1212 保持 OPEN。
