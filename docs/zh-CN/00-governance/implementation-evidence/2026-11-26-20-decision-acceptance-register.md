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
        - "00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md"
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
    canonical_scope_id: "governance/decision-acceptance/zh-CN/register"
    canonical_scope_keywords:
      - decision-acceptance
      - evidence
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md"
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md"
---

# 20 项方向决策验收登记表 — AID-2026-11-26-DECISION-ACCEPTANCE-03

> 本文件是证据登记，不是 Owner 接受、规范生效、实现授权、实现验证或生产符合性声明。
> 授权归属：`user-authorized operator (delegated by account owner)`（代理决策者，不是自然人签名）。
> Owner 指定日期：2026-11-26。GitHub 实际登记时间可能早于该日期；两者分别保留。
> 观察到的 main 基线：`6314a65bd8be48c1a4bb0768e9960c4c808110ab`；合并前必须重新核对 HEAD。

## 计数与状态规则

本登记包含 **20 个 DEC 登记项、18 个唯一方向**。DEC-16 与 DEC-17 是同一项受治理的逐文件规范源恢复方向下，I/H 两个领域的分条登记；DEC-19 与 DEC-20 是同一 binding-force 治理方向下有先后依赖的两个阶段。20 个 DEC ID 均保留独立追踪；两组均分别保留证据和前置条件追踪。

状态：OPEN = 已记录方向但验收证据不全；PARTIAL = 有部分组成/文档证据但仍缺必要接受门；BLOCKED = 明确前置条件或权威证据阻塞；VERIFIED 仅在所有验收条件及所需 Owner 接受均有证据时使用。本表不将任何项目标为 VERIFIED。

六种状态必须分开：Direction Approved、Owner Accepted、Normative Source Effective、Implementation Authorized、Implementation Verified、Production Conformant。

## 决策清单

| DEC | 已选方向 | 原始决策记录 | Owner / 联合依赖 Owner | 独立验收条件 | 验证方法 | 状态 |
|---|---|---|---|---|---|---|
| DEC-01 | MemoryVersion canonical reference manifest：C 混合方案；显式引用必须等于规范内容推导结果，不一致拒绝提交并重算 digest | [#1191 评论 7174300340](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1191#issuecomment-7174300340)，详细决定 [7174521705](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1191#issuecomment-7174521705) | C；B、D | Claim revision refs 为权威成员集；其他 refs 为确定性派生投影；提交时核对；digest 从规范结果重算；历史版本引用精确 | 精确 Blob 审查；推导与显式输入一致/不一致正反例；提交拒绝及 digest 测试 | OPEN |
| DEC-02 | Partial-Scope MemoryVersion 披露：B 安全投影 | [#1128 评论 7174029131](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1128#issuecomment-7174029131) | B；C、D、I | 内容和全部关联引用按 Scope 过滤；投影 digest 与 canonical digest 明确区分；不泄漏隐藏标识或完整 digest；canonical snapshot 不变 | 混合 Scope fixture；返回引用/digest 检查；披露正反例 | OPEN |
| DEC-03 | Claim–Evidence 关系模型：C，独立版本化关联对象 | [#1103 评论 7174030149](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1103#issuecomment-7174030149) | C；B、D | 关联对象保存角色/评估；ClaimRevision 固定精确关联对象 revision；校验生命周期、Scope、Provenance | 类型与 revision 审查；精确引用正反例 | OPEN |
| DEC-04 | Provenance 完整性：C，分层权威/解释记录 | [#1104 评论 7174031071](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1104#issuecomment-7174031071) | C；B、D、E | 可验证权威记录必须有 target、typed source refs、精确版本、input digests、actor、lineage；不完整记录只能是明确非权威说明 | 字段/类型审查；规范发布拒绝测试；lineage 验证 | OPEN |
| DEC-05 | Evidence 可附着性、授权、保留与 Forget：C，正交分层维度 | [#1170 评论 7174032150](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1170#issuecomment-7174032150)，细化 [7174508996](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1170#issuecomment-7174508996) | C；B、D、I | 可用性、授权、保留、Forget 分离；附着/读取联合判定；明确 forgotten/revoked 优先级；payload 擦除后 EvidenceRef 仍可解析 | 决策表；组合与优先级测试；历史引用解析 | OPEN |
| DEC-06 | 子对象 Forget 与不可变历史：A 负责历史语义 + C 负责依赖闭包执行 | [#1174 评论 7174032987](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1174#issuecomment-7174032987)，细化 [7174512700](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1174#issuecomment-7174512700) | A、C；B、D、I 及相关 F/G/Storage | 历史快照不可变且读取时抑制；当前存活视图使用受治理 successor version；覆盖派生对象、缓存、索引、投影；抑制状态不能伪装成从未存在 | 依赖图/读取面清单；历史/当前读取测试；派生清理、Fence、审计证据 | OPEN |
| DEC-07 | F 正式规范源处理：A | [#1179 评论 7174052619](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1179#issuecomment-7174052619)，合并记录 [7174288361](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1179#issuecomment-7174288361) | A；F、D、E、I、Storage | 候选设计、F Owner 接受、规范生效分别记录；逐文件 source/mirror pin；先解决开放项 | 文件清单、Blob、Owner review、治理审批、main 逐文件核验 | OPEN |
| DEC-08 | D→E→F Canonical Commit 与消费事件：A | [#1177 评论 7174287587](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1177#issuecomment-7174287587)、[#1184 评论 7174053488](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1184#issuecomment-7174053488)、[#1212 评论 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311) | A；D、E、F、Storage/Consistency 联合接受 | Canonical Commit 与权威 change event/outbox/receipt 同一原子边界；可审计线性化点；E 请求只能引用已提交 D revision/cursor | 精确契约审查；事务、崩溃、恢复、重放、幂等证据；Storage 接受 | OPEN |
| DEC-09 | F 水位与扫描覆盖证明：A | [#1179 评论 7174060184](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1179#issuecomment-7174060184)、[#1184 评论 7174286863](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1184#issuecomment-7174286863) | A；F、D、Storage | scanned_through/连续覆盖证明；visible/irrelevant/filtered/gap 区分；gap 阻止推进；从水位重放；last-visible 不是覆盖证明 | gap/replay/重复/乱序测试；连续前缀证明；精确来源 | OPEN |
| DEC-10 | Forget Fence 与派生发布边界：A | [#1209 评论 7174055125](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1209#issuecomment-7174055125)、[#1212 评论 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311) | A；D、E、F、G、I、Storage，涉及传输时含 H/C | D-FORGET-CONTRACT-001 @ `760a1d48011f2a66c23abcf825a3d067e79b8821`（Draft/Unverified/Informative；Owner 接受待定）；System Boundaries @ `c2aa6823b69313ba27c34625f87f29d2be356606`（Draft/Unverified/Normative）；D 权威 Fence 证明和发布门；旧 Fence 派生物不能发布/重新可见；每步明确 issuer、token、线性化点、幂等和 unknown/failure | 转移/竞态表；缓存、队列、重放、恢复、崩溃测试；逐 Owner 接受 | OPEN |
| DEC-11 | G Delivery 与 C/H Accepted 证据映射：B | [#1180 评论 7174054303](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1180#issuecomment-7174054303)，细化 [7174289110](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1180#issuecomment-7174289110) | B；C、H、G 联合接受；必要时 D/I 输入 | G 不新增 Accepted 状态；持久化权威 C/H Accepted 证据引用并绑定稳定 Attempt；Accepted 不等于 Applied | 精确状态/证据映射；持久关联与重放测试；C/H/G 接受 | OPEN |
| DEC-12 | 工作流 CLOSED 分阶段验收：C（已确认；Gate A 待完成） | [#1212 评论 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311)、[矩阵 7174315211](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174315211)、验收清单 7174866924 | C；A、各领域 Owner、Storage/Consistency | Gate A：精确版本审查包、流程/不变量追踪、Owner 联合接受及双语/源修订一致；实现/生产行可明确保持 BLOCKED / NOT VERIFIED。Gate B：独立要求集成构建、D/E/F/G/H/I 符合性、Storage 故障恢复证据、端到端测试及生产 Owner 接受。Gate A 不推定 Gate B。 | Owner C 的分阶段关闭确认已于 2026-11-26 记录；十个必需 Owner 角色的处置现已在该分支以代理方式登记（3 ACCEPT / 7 CONDITIONAL / 0 REJECT）；每项均明确注明由代理登记、非自然人 Owner 签署。条件证据仍为 OPEN：完整精确版本组合审查、规范源恢复/固定、Storage/Consistency 物理合同、H 幂等/重放协调、完整审查包双语/来源修订一致性及 DEC-13 批准证据。Gate A 为 PARTIAL / OPEN | OWNER_CONFIRMED_GATE_A_PENDING |
| DEC-13 | Principles / Invariants 批准效力：C；当前版本不批准 | [#1189 评论 7174316473](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7174316473) | C；A、治理批准人 | 当前版本 CANDIDATE/Pending-Reapproval；不推断历史批准；根文件与 EN/ZH 元数据一致；精确版本另行提交批准 | frontmatter/Blob 比较；双语扫描；批准记录审查 | OPEN |
| DEC-14 | Owner A–I 与 subsystem/capability 命名空间分离：A，使用非碰撞 SYS-* 名称 | [#1196 评论 7174317289](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1196#issuecomment-7174317289) | A；A–I 各 Owner 对自身职责行接受 | subsystem 标签不再冒充 Owner；能力到 Owner 完整映射；Primary/Supporting/Joint 和权威边界明确 | 图表/矩阵审查；映射完整性检查；双语差异；逐 Owner 接受 | OPEN |
| DEC-15 | D/I Forget、Retention 与全局完成权威：B 联合决定 | [#1208 评论 7174318079](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1208#issuecomment-7174318079) | B（方向）；I 全局政策；D 规范机制；相关执行 Owner 联合接受 | I 管全局授权/保留/legal hold/外部副本/清单/完成标准；D 管 canonical Forget/Fence/D 域谓词；全局完成需 D 与相关执行 Owner 接受；System Boundaries @ `c2aa6823b69313ba27c34625f87f29d2be356606`（Draft/Unverified/Normative）；D-FORGET-CONTRACT-001 @ `760a1d48011f2a66c23abcf825a3d067e79b8821`（Draft/Unverified/Informative）；I security-governance source root 仍缺失 | 权威措辞差异；精确证据契约；联合接受和端到端证明 | OPEN |
| DEC-16 | I 规范源逐文件恢复：A | [#1202 评论 7174318902](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1202#issuecomment-7174318902) | A；I；逐文件要求的联合/依赖 Owner | 每个文件登记 path/blob/role/dependencies/reviewers/mirror/eligibility；依赖 ADR 和治理批准先于单文件恢复；禁止整分支合并 | 逐文件资格矩阵；Blob；审批；main tree 核验 | OPEN |
| DEC-17 | H BMCP 规范源逐文件恢复：A | [#1203 评论 7174319680](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1203#issuecomment-7174319680) | A；H；C/G 等协议依赖 Owner | H 精确文件清单和协议覆盖；逐文件依赖/联合审查/治理审批；禁止整分支合并；恢复不等于协议冻结或 conformance | 文件清单、Blob、镜像、审批、main 核验；conformance 独立核验 | OPEN |
| DEC-18 | Phase 1 语义冻结与工程授权：A，保持 DEFERRED | [#1197 评论 7174320446](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1197#issuecomment-7174320446) | A；Phase 1 领域 Owner；工程授权另行负责 | 保留 `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`；Phase 1 仅语义冻结；历史 Rust 工作不构成新授权；不得暗示 Runtime/Storage/生产启动 | 精确措辞审查；检索所有 implementation-next-step 表述；双语一致 | OPEN |
| DEC-19 | governance binding-force 规则 Stage 1：A | [#1037 裁决 7153761392](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1037#issuecomment-7153761392)，顺序约束 [7154085008](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1037#issuecomment-7154085008) | A；C 治理审查 | `normative_status` 决定约束力；Informative 仅对已发生事实有权威性，不是要求来源；Active 不使 Informative 生效；Pending-Reapproval 不改变分类；changelog 和中英同文件一致 | 精确条款差异；同文件双语语义审查；确认未扩大 checker/schema 授权 | OPEN |
| DEC-20 | schema/checker/migration/test 授权 Stage 2，等待 Stage 1：A | [#1049 评论 7174322035](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1049#issuecomment-7174322035) | A；另行指定治理 Owner、实施 Owner、验收 Owner | #1037 完成前不得开始；另行 AID 必须明确 schema、checker、migration、tests、责任 Owner、验收权威；本决定本身不授权实施 | 核验 #1037 完成；审查独立 AID 范围和权威；本工作流不改代码/schema/checker | BLOCKED |

## 重复方向与先后关系

- DEC-08 在 #1177/#1184/#1212 多处登记，是同一方向。
- DEC-09 在 #1179/#1184 登记，并由 #1212 汇总。
- DEC-10 在 #1209/#1212 登记，#1177 提供 D source 背景证据。
- DEC-16 和 DEC-17 是同一项受治理的逐文件规范源恢复方向下，I/H 两个领域的分条登记。两个领域仍须分别提供证据，但唯一方向只计一次。
- DEC-19 → DEC-20 是严格先后依赖；Stage 2 在 Stage 1 完成且独立 AID 签发前保持 BLOCKED。
- 本表链接的是方向记录，不代表 Owner 已接受。

## Issue 验收 checklist 模板

向对应 Issue 追加而不是替换历史内容。以下项目在证据落盘前全部保持未勾选：

- [ ] canonical source 与精确 blob/commit 已记录
- [ ] EN mirror 已核验
- [ ] ZH-CN mirror 已核验
- [ ] 交叉引用和依赖 ADR 已核验
- [ ] 验证方法及原始输出已附
- [ ] 责任 Owner 接受精确版本
- [ ] 每个依赖/联合 Owner 接受其权威职责行
- [ ] 必要治理审批已记录
- [ ] 剩余限制及 unknown/recovery 行为已记录
- [ ] 实现授权、实现验证、生产符合性分别记录（仅在其范围内）

本登记不关闭任何 Issue。


## I-01…I-24 委托责任映射裁决（2026-11-26）

**归属：** `user-authorized operator (delegated by account owner)`（委托操作人；非自然人签名）。  
**处置：** A–I + Storage 矩阵中的 24 项 Authority Owner / Dependent Owners 分配，现确认为该委托操作人的最终责任映射裁决，状态为 **OWNER_CONFIRMED**。此前 PROPOSED 行仍保留在矩阵中作为历史提案快照。本裁决不冒充任何列出的 Owner，也不代表其接受精确版本合同。

**计数：** 24/24 项映射已裁决；相对先前提案，2 项 Authority Owner 作了修订（I-05 D→E；I-14 D→B）；3 组依赖 Owner 作了修订（I-02 增加 C/I/Storage；I-13 与 I-21 移除 A，因为 A 负责协调而不执行这些领域边界）；其余映射按矩阵所列理由确认或保留。行级 Gate A 追踪：24 行 VERIFIABLE，0 行 BLOCKED_WITH_REASON。精确版本 Owner 处置：24 行仍为 PENDING（权威 Owner 与每一位列出的依赖 Owner 必须分别对其权威责任行作出回应）。

**DEC-12 / Gate A 状态：** `OWNER_CONFIRMED_GATE_A_PENDING`；Gate A 仍为 **PARTIAL / OPEN**，不得标记 CLOSED。本委托映射裁决只完成责任分配任务，不满足精确版本跨 Owner 处置或完整 A–I + Storage/Consistency 端到端组合审查包。Gate A 尚缺：(1) Owner A 及每一位相关权威/依赖 Owner 提交精确版本 ACCEPT/REJECT/CONDITIONAL/BLOCKED 处置；(2) 所有端到端流程的 current-main 来源/版本固定点及完整边界合同，包括签发者、请求/响应、身份/游标/幂等范围、线性化点、持久回执、失败/Unknown、重放/恢复和可见性；(3) 解决或明确处置 D/E/F/I 缺失的规范根/合同，以及 Storage/Consistency 来源/接受固定点；(4) 一份经回读核验、包含 EN/ZH-CN 语义与来源修订一致性的精确版本审查包。当前 Invariants 来源依据 DEC-13 仍未获批准；此处不推定任何批准。

**Gate B：** 仍为 NOT VERIFIED，且独立于 Gate A。不得从本次 Gate A 追踪裁决推定生产集成、故障/恢复测试、端到端符合性或生产 Owner 接受。#1212 保持 OPEN。


## 2026-11-26 cross-Owner dispositions — delegated proxy record

**Authority and attribution:** `user-authorized operator (delegated by account owner)`; decision date `2026-11-26`. The human Owner has expressly authorized one session to represent all listed Owner roles for this record. Each disposition below is nevertheless a proxy record, not a natural-person Owner signature, platform-authenticated Owner review, or evidence that another individual personally signed. The dispositions apply to the exact responsibility mapping and Gate A review criteria in this matrix at the current PR head; they do not grant implementation authorization, normative approval, production acceptance, or Gate A closure.

**Disposition rule:** `ACCEPT` accepts the role's assigned responsibility mapping and row-level review criteria. `CONDITIONAL` accepts that mapping subject to the explicit evidence/contract condition in the row. No role issued `REJECT`. A conditional record is a recorded disposition, but its condition remains an open Gate A item until evidence is read back.

| Role | Authority rows | Dependent rows | Disposition | Condition / reservation | Attribution / date |
|---|---|---|---|---|---|
| Owner A | I-22, I-23, I-24 (Authority); I-01…I-24 (coordination) | — | **CONDITIONAL** | Accepts I-22..I-24 responsibility and the review criteria; Gate A closure is conditional on a complete exact-version A–I + Storage/Consistency composition package and bilingual/source-revision parity. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner B | I-02, I-03, I-04, I-06, I-14, I-15, I-21 | I-01, I-05, I-12, I-13, I-22, I-23, I-24 | **ACCEPT** | Accepts its assigned authority/dependency responsibilities and row-level review criteria; no B-specific reservation is recorded against the mapping. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner C | I-11, I-12 | I-02, I-03, I-04, I-06, I-09, I-10, I-13, I-17, I-18, I-21, I-22, I-23, I-24 | **ACCEPT** | Accepts its assigned authority/dependency responsibilities and row-level review criteria; no C-specific reservation is recorded against the mapping. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner D | I-01, I-07 | I-02, I-03, I-04, I-05, I-06, I-08, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The current-main canonical store normative source is absent. IMPL2 must restore or formally disposition and pin that source; D then verifies the exact canonical-authority and lifecycle contract. D is not re-assigned the source-restoration task. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner E | I-05 | I-01, I-02, I-03, I-04, I-06, I-07, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The compiler receipt/idempotency and producer/stage normative contracts are absent or not pinned on current main. IMPL2 must restore or formally disposition and pin those sources; E then verifies compiler provenance and derived-memory semantics. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner F | — | I-01, I-02, I-03, I-04, I-05, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The F-domain normative source root/contract is not present as a complete current-main review pin. IMPL2 must restore or formally disposition and pin the missing source; F then verifies the exact retrieval/derived-record boundary. F is not re-assigned source restoration. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner G | I-08, I-09, I-10, I-17, I-19 | I-01, I-02, I-03, I-04, I-05, I-06, I-07, I-11, I-12, I-13, I-14, I-15, I-16, I-18, I-20, I-21, I-22, I-23, I-24 | **ACCEPT** | Accepts its assigned context-versioning, delivery and compaction responsibilities and row-level review criteria; no G-specific reservation is recorded against the mapping. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner H | I-16, I-18 | I-01, I-02, I-03, I-04, I-06, I-09, I-10, I-11, I-12, I-13, I-17, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The exact idempotency namespace, linearization and durable replay/Unknown contract still needs one reconciled source pin across H, E and Storage/Consistency. H accepts its protocol authority subject to that exact contract being recorded. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner I | I-13, I-20 | I-01, I-02, I-03, I-04, I-05, I-08, I-12, I-14, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The current-main security-governance normative root is absent and DEC-13 approval metadata remains unverified. IMPL2 must restore or formally disposition and pin the source; I's policy acceptance remains conditional on exact-source and approval evidence. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Storage/Consistency | — | I-01, I-02, I-03, I-04, I-05, I-07, I-08, I-09, I-10, I-13, I-14, I-15, I-16, I-17, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The exact physical transaction, durability, crash/restart, restore and visibility contract is not pinned in the review package. The exact source and evidence must be recorded and Storage/Consistency's own review disposition read back. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |

**Counts:** 10 role dispositions; 3 ACCEPT; 7 CONDITIONAL; 0 REJECT. Roles covered: Owner A, B, C, D, E, F, G, H, I, and Storage/Consistency. The Authority/Dependent row coverage is derived from the 24 adjudicated invariant rows above; it is not an independent human signature.

## Gate A closeout checklist — current disposition

| Gate A item | Status | Minimum condition to close / accountable party |
|---|---|---|
| Branch synchronized with current main | SATISFIED | Merge base equals current main; merge base equals current main and the branch is not behind it. The ahead count is volatile as review commits accumulate and is reported from current PR metadata, not frozen here. Recheck if main advances again. |
| Cross-Owner role dispositions recorded | SATISFIED | All 10 roles have a dated proxy disposition; 3 ACCEPT / 7 CONDITIONAL / 0 REJECT. The seven conditions below remain OPEN and must be discharged before Gate A can close. |
| Exact-head CI | OPEN_PENDING_FINAL_HEAD | Run all applicable pull_request workflows on the final documentation head and read back the exact SHA and conclusions; do not reuse earlier-head results. |
| Complete A–I + Storage/Consistency composition review artifact | OPEN | Owner A coordinates one exact-version package; each relevant Owner pins the canonical source and documents issuer/authority, request/response, identity/cursor/idempotency namespace, linearization point, durable receipt, failure/Unknown, replay/recovery and visibility for each end-to-end boundary. |
| Missing normative source roots/contracts (D/E/F/I) | OPEN — IMPL2 | **IMPL2 owns source restoration or explicit disposition and exact source pins.** Minimum: restore/publish the missing current-main normative roots/contracts or record a governed non-restoration disposition with exact replacement source pins. Domain Owners validate their contracts after restoration; they do not duplicate-claim IMPL2's source-restoration task. |
| Storage/Consistency physical contract and evidence | OPEN — IMPL2 + Storage/Consistency | IMPL2 supplies/restores the canonical physical transaction/durability/recovery source and exact blob pin; Storage/Consistency reviews and records the corresponding proxy disposition condition as satisfied against crash/restart, restore and visibility evidence. |
| H idempotency namespace / replay boundary | OPEN — Owner H with E and Storage/Consistency | Record one reconciled exact-version namespace/scope, linearization, durable receipt and Unknown/replay contract across the participating boundaries. |
| Full-package bilingual semantic and source-revision parity | OPEN — Owner A / documentation Owners | Read back the complete exact-head Canonical/EN/ZH-CN review package; verify semantic parity, stable IDs, decision states and every source revision pin. Matrix-only parity is insufficient. |
| DEC-13 normative approval evidence | OPEN — governance authority; source work by IMPL2 where applicable | Record the actual approver, approval date and authoritative evidence for the exact Invariants/Principles source, or issue a governed disposition that explicitly keeps it unapproved. Do not infer approval from this proxy record. |

**DEC-12:** remains `OWNER_CONFIRMED_GATE_A_PENDING`. Gate A is **PARTIAL / OPEN**, not CLOSED. The cross-Owner disposition record is now present, but conditional evidence and composition/source/parity items remain OPEN. **Gate B remains NOT VERIFIED** and separate. #1212 remains OPEN.
