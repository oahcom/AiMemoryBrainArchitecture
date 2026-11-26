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
        - "00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "仅完成精确版本源盘点和缺口分析；不推断端到端符合性或 Owner 接受。"
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
    canonical_status: Canonical
    canonical_scope: "A-I + Storage/Consistency 精确版本端到端组合审查"
    canonical_scope_id: "architecture/a-i-storage-e2e-composition-review"
    canonical_scope_keywords:
      - end-to-end
      - composition
      - storage-consistency
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
---

# A-I + Storage/Consistency 端到端组合审查

- 工作项：AID-2026-095
- 编号状态：PROVISIONAL；临时数字预留；合并时重新核验 main，如被占用则重编号。
- 精确来源基线：main @ 47fcd80720b742d9c5d3ae137593c59b5cc768a9
- 归属：user-authorized operator (delegated by account owner)，日期 2026-11-26。任何代理处置均为**代理登记，非自然人 Owner 签署**。本文不新增 Owner 接受。
- 目的：提供可证伪的 Gate A 组合检查清单，不宣称实现或生产符合性。

## 1. 阅读规则与判定语义

仅固定上述精确 main 版本中存在的文件。NOT_FOUND_ON_MAIN 是递归 tree 核验后的否定结果。镜像、参考模型、Schema、测试、实现文件或工作记录，不自动升级为 Owner 规范合同。

- VERIFIED_BY_DOCUMENT：精确版本的当前 main 文档完整定义待检查命题，权威状态适用且无未解决跨 Owner 依赖。这不是运行时测试结果。
- BLOCKED_WITH_REASON：命题不完整、矛盾、仅候选、未获接受、缺规范源或缺证据；必须写明缺件及提供者。
- 每个检查点使用 PASS、FAIL 或 NOT EVIDENCED。NOT EVIDENCED 不算 Gate A PASS。任一必需检查点缺失，整条流程保持阻塞。
- 以下八条流程全部为 BLOCKED_WITH_REASON；局部条款有文档，不代表整条流程已验证。
- 不修改 runtime、validator、schema、测试、策略或 Owner 决策。

## 2. 精确来源清单

以下 Blob SHA 来自指定基线的 Git tree/内容读取。缺失路径为明确否定核验结果。

| 精确路径 | Blob SHA | 来源类别 / 限制 |
|---|---|---|
| 00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md | 05fdcc93c5dfee1f635b5ad1a1db86310a88d8f7 | Canonical 工作记录；仅用于可追溯性；其内嵌基线已过期。 |
| 04-memory-compiler/compiler-overview.md | 24c2fc69a8a69176071d46aac871ae16588702b7 | Canonical、Normative、Draft/Unverified；编排仍为候选，且明确排除若干责任。 |
| 04-memory-compiler/phase-1-event-store-contract.md | 17b14591d76160a7c125903b41e7dae014c3c5df | 语义 DECIDED / 实现接缝 CANDIDATE；不包含派发、lease 和生产持久性证明。 |
| 04-memory-compiler/README.md | 88f1a451830b4c7b455462edd6453543778793e4 | Canonical、Informative 阅读指南。 |
| 14-ai-development/work-items/D-OWNER-DECISION-PARTICIPANT-ADMISSION-001.md | 2cff53b2133e26115e2d3808ae9738092602c4d3 | Owner 代理决策；participant_admitted 仍为 false。 |
| 14-ai-development/work-items/D-OWNER-DECISION-CANONICAL-COMMIT-001.md | 2fba6536e95e55e55617bfddefc26a11e269c5b5 | D 决策记录；canonical store 规范根缺失。 |
| 01-system-architecture/forget-fence-and-completion-contract.md | 760a1d48011f2a66c23abcf825a3d067e79b8821 | Canonical、Draft/Unverified/Informative；全局策略和跨模块执行仍开放。 |
| 06-memory-context/context-versioning.md | 57ea7e7298f79d769d6931b1d355c9d3b4f956d6 | G 语义；编码/序列化仍为候选。 |
| 06-memory-context/context-version-immutability-decision.md | 27e9e5f092b17cf4013a533d07949eb73ac6ef4c | Draft/Unverified/Informative；等待 G 接受。 |
| 06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md | 833815e37ac8d7505d93a0a115421dafe3eb08ad | G 所有的 Normative Design Draft；实现未验证，且需跨 Owner 接受。 |
| 07-agent-integration/applied-evidence-contract.md | 273efdd1b02bd9302fc968f07c6d094da2582a6e | Draft/Unverified/Informative；等待 C/G/H 接受。 |
| 07-agent-integration/inference-boundary-model.md | e2d5cb6abd9ec40da6e3680531de5944fc8b14df | 候选边界模型；尚无跨 Owner 冻结。 |
| 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md | d83cde77e98db2e74cf6827d874b0babb4157304 | H 候选合同；必须与 E/G/Storage 对齐。 |
| 08-bmcp-protocol/phase-3.8-h-rj-hw-01-typed-watermark-and-fence-binding-contract.md | e583ac2fb888aa5184eaa6525d9cc564f343785f | H 阶段合同；不是 F 规范检索根。 |
| 08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md | afa294bc42a8488e4569e6a8bdf5437c7a90e247 | H 补充条款；共享消费者接受仍待完成。 |
| 08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md | 7b73491c765091728af6f5306b9efd502cf7f30a | H 补充条款；共享消费者接受仍待完成。 |
| 02-domain-model/phase-1-storage-trait-contract.md | 22ca7cd3777e0132e25f084084610f1e90b60d21 | 候选接口接缝；未选择后端；不构成后端原子性/持久性证明。 |
| 02-domain-model/scope-and-permission-model.md | b5215ae27bd65a6c89c185b496f730b6cd52efa9 | Scope 分离已决定；策略语言和继承边界仍开放。 |
| 14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md | 8ad9bbfa4906a6f9c30a437fd144c6c62c37577d | 代理决策；不证明 I 签发的真实性。 |
| 14-ai-development/adr/OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md | 75e338aa0dbe0161fbc890977c5f4a8234a8c815 | 代理裁定；存在性门禁不等于授权真实性。 |
| crates/memory-event-store-sqlite/src/lib.rs | c68e036e5f8deb7968babc6703a4cf9341d5db40 | 仅为实现证据。 |
| crates/memory-storage-sqlite/src/lib.rs | b7eecd3ec0ec4c3ef3c27bc43fe24c29c91fb11f | 仅为实现证据。 |
| crates/memory-event-store-sqlite/src/forget_fence.rs | 5b71a25b8be24fd0f1d9cf9e22582705d646cf64 | 仅为实现证据。 |
| 06-memory-context/reference-model/g_applied_ledger.py | be24fea19ee72a1fc01350b79d5359e7820848b9 | 仅为参考模型。 |
| 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json | 0700f2077052bd153f9baa86850d9aab89491016 | 存在 Schema 不等于端到端接受。 |
| 09-security-governance/README.md | NOT_FOUND_ON_MAIN | IMPL2/I 恢复或处置；由 I 接受策略。 |
| 03-memory-brain/canonical-memory-store.md | NOT_FOUND_ON_MAIN | IMPL2/D 恢复或处置；由 D 接受 canonical 语义。 |
| 05-memory-runtime/README.md | NOT_FOUND_ON_MAIN | IMPL2/F 恢复或处置；由 F 接受检索语义。 |
| 04-memory-compiler/accepted-receipt-and-idempotency-contract.md | NOT_FOUND_ON_MAIN | IMPL2/E 恢复或处置；由 E 提供回执合同。 |
| 04-memory-compiler/compiler-state-and-producer-admission.md | NOT_FOUND_ON_MAIN | IMPL2/E 恢复或处置；由 E 提供准入合同。 |

### 当前 main 缺失的规范根

| 预期路径 | 结果 | 必须提供者 |
|---|---|---|
| 03-memory-brain/canonical-memory-store.md | NOT_FOUND_ON_MAIN | IMPL2/D 恢复或正式处置；D 接受 canonical 语义。 |
| 05-memory-runtime/README.md | NOT_FOUND_ON_MAIN | IMPL2/F 恢复或正式处置；F 接受 retrieval 语义。 |
| 09-security-governance/README.md | NOT_FOUND_ON_MAIN | IMPL2/I 恢复或正式处置；I 接受 policy 语义。 |
| 04-memory-compiler/accepted-receipt-and-idempotency-contract.md | NOT_FOUND_ON_MAIN | IMPL2/E 恢复或正式处置；E 提供 receipt 合同。 |
| 04-memory-compiler/compiler-state-and-producer-admission.md | NOT_FOUND_ON_MAIN | IMPL2/E 恢复或正式处置；E 提供 admission 合同。 |

docs/en 下的镜像不能在没有明确源层级决策时填补缺失的 canonical root。

## 3. 八条必需端到端流程

每条流程均检查九项：issuer；请求/响应；身份与游标命名空间；幂等范围；线性化点；持久回执；失败/Unknown；重放/恢复；可见性。

### F1 — Event ingress → durable acceptance → Compiler admission

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** E ingress/Compiler；I 授权；D 权威边界；Storage 持久化
- **阻塞原因：** E Event Store 仅是候选实现接缝；accepted-receipt 和 producer-admission 规范根缺失。Compiler Overview 排除最终 canonical 权威与生产派发。D 决策明确 E AdmissionStore 不是 D 权威，publication_participant_admitted 仍为 false。
- **缺失项 / 提供者：** IMPL2/E 恢复或处置缺失回执/准入规范根；E 提供派发/lease/重试合同；I 提供授权 issuer/epoch；D/Storage 提供持久接收边界。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | E 接收 Producer envelope；I 是授权权威；E AdmissionStore 不得自称 D 权威。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | Producer actor、Scope refs、payload ref+digest、幂等键、correlation/causation；返回持久 Accepted receipt 或明确冲突/拒绝。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | Event/receipt ID 稳定；候选幂等元组为 (producer_actor_ref,idempotency_key)；与 D commit、F watermark、H cursor 分离。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | 相同 producer+key+digest 返回原回执；相同 key/不同 digest 冲突；重放前先做 Scope 授权。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | 候选事务同时写入 envelope、digest、receipt、Pending 状态和 compile-intent outbox 行。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | receipt 与 compile intent 同事务持久化；重放返回原 receipt，不重复创建 intent。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | 派发/Worker delivery 与提交后 Unknown 的核对方式尚未完整定义。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | 启动时回填缺失 intent；dispatcher、lease、retry、DLQ 不在当前 adapter 合同内。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | Accepted 不等于 canonical/indexed；在 D/I 门禁允许前必须保持 private staging。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F2 — D Canonical Commit → atomic outbox / receipt → F consumer

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** D canonical 权威；Storage 物理事务；F 消费权威 feed
- **阻塞原因：** D canonical store 规范根缺失。Storage trait 仅为候选，并明确不规定后端/分布式原子性。E compile-intent outbox 不是 D canonical-change outbox。
- **缺失项 / 提供者：** IMPL2/D 恢复/处置 canonical store 根；D 固定 commit/result/cursor/outbox；Storage 提供同事务 commit/outbox 与崩溃证据；F 提供 consumer 去重/ack。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | 只有 D 能签发 canonical identity/version/lifecycle/commit result；Storage 不得签发领域权威事实。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | CanonicalWriteRequest 绑定 expected version、immutable new version、Scope、authorization/Fence、幂等身份；响应区分 committed/conflict/rejected/Unknown。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | D commit cursor 与 D outbox event ID 绑定；F scan watermark 由 F 独立拥有。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | key+request digest 解析为唯一 D receipt；digest 改变则冲突；receipt 查询前检查 Scope。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | 预期单一 Storage 事务包含 immutable version、current-version CAS、幂等记录、D sequence、outbox、receipt。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | D receipt/outbox 必须在重启后可查询；E compile-intent 行不是该回执。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | CAS 冲突是确定结果；rollback 表示未提交；提交期间响应丢失则在查询 receipt 前保持 Unknown。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | F 从持久 D cursor 重放；at-least-once delivery 去重；不得跳过 gap。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | canonical state 仅在 commit 和 D/I/Fence 检查后可见；F projection 只是派生视图。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F3 — F Retrieval / Index / Watermark / Scan Coverage

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** D 拥有 canonical feed；F 拥有 retrieval/index/watermark
- **阻塞原因：** F 规范根 05-memory-runtime/README.md 缺失；检索引擎材料仅位于 docs 镜像。D canonical feed 根也缺失；没有源定义连续 watermark 证明。
- **缺失项 / 提供者：** IMPL2/F 恢复/处置 F 根；D 固定 feed cursor；F 规定 watermark/gap/tombstone/coverage；Storage 固定持久 index checkpoint。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | D 签发 canonical sequence；只有 F 签发 per-index scan watermark 和 retrieval 元数据。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | 请求绑定 actor、resolved Scope、query/filter、一致性要求和 Fence/permission epochs；响应区分 visible/filtered/irrelevant/gap/unknown。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | D cursor、F per-index watermark、shard cursor、continuation token 必须强类型且互相区分。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | Index 按 D event/commit identity + index generation 去重；retrieval retry 不推进 scan watermark。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | 没有 F 源定义 index mutation、连续 watermark 与 coverage proof 的原子边界。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | 每索引 scan-through proof 必须持久化并绑定精确 D cursor 与 gap；其格式尚未固定。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | gap、坏事件、权限失败、Fence 过期或 shard 失败不得计为 scanned。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | 从 D cursor 重建；只有所有前序事件都已处理/核销后才推进连续前缀。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | 检索/发布时检查 D Fence 和 I 授权；过期 index/cache 候选必须抑制。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** D canonical Fence issuer；I 策略/完成；各派生域执行；Storage 仅投影
- **阻塞原因：** D Fence 源为 Draft/Unverified/Informative，且不是 wire schema；I 全局策略根缺失。跨域回执 schema、线性化和生产证据尚未接受。
- **缺失项 / 提供者：** IMPL2/I 恢复/处置策略根；D 固定 Fence operation/inventory 源；I 定义授权/retention/残留例外；E/F/G/H/Storage 提供逐目标持久 ack/重放/可见性证据。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | D 签发 ForgetOperation/Fence；I 签发策略/全局完成；E/F/G/H 各自签发派生执行 ack。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | Operation ID、target inventory/version、policy authority、expected Fence；每个 target 返回 typed per-target ack，含 unknown/exception。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | D operation/Fence cursor、I PermissionEpoch、E/F/G/H target ack、Storage 派生 projection cursor 各自独立。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | 稳定 operation ID + 不可变 target/policy digest；逐目标 ack 绑定 operation+target+generation。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | D 持久单调 Fence commit 是逻辑抑制点；cleanup 随后进行；I global completion 是另一决策点。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | D operation/Fence 与逐目标 ack 必须持久；只有 I 可签发全局完成 receipt。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | Unknown target、timeout、offline Adapter、backup/external copy 或 inventory 缺失均阻止完成；可见性 fail-closed。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | retry 重新检查当前 Fence；restore 先应用 Fence 再暴露数据；旧 publication 不得重新进入可见状态。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | D Fence 立即抑制 canonical refs；所有派生路径执行门禁；物理擦除属于 I 策略。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F5 — C/H Applied evidence → G Applied decision

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** C 拥有 inference facts；H 协议证据；G 是唯一 Applied issuer；I/D/Storage 提供谓词
- **阻塞原因：** G 持久化合同为 Normative Design Draft，实现未验证且需跨 Owner 接受。C Applied 合同为 Draft/Unverified/Informative；H schema/addenda 不证明同一 request/GID 的完整证据 join。
- **缺失项 / 提供者：** C/H/G/Storage/D/I 对齐精确 join 合同；G 证明账本崩溃恢复；Storage 证明 same-GID terminal；相关 Owners 接受同一版本。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | C 签发不可变 CSubmitOutcome；H 签发认证 delivery evidence；只有 G 签发/修改 Applied；D/I/Storage 签发各自独立证明。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | G 对同一 request/causal transaction 的不可变 Applied identity 和完整 evidence revision 求值；返回 Full Applied 或明确 non-applied/Unknown。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | Applied ID、request ID、CSubmitOutcome、H evidence revision、COC GID/participant、I decision/epoch、D Fence、Storage receipt 类型独立但需精确关联。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | 相同 immutable Applied identity+evidence revision 得到同一结果；证据 revision 改变必须显式 supersession/re-evaluation。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | G ledger commit 是 Applied 决策点；适用 JF-10 时，Storage same-GID VisibilityPointer/Receipt 必须先达到 terminal。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | G 决策和证据 join 持久化；Storage same-GID receipt 与 C/H evidence 在崩溃后仍可解析。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | C/H/COC/I/D/Storage 的 Unknown 均保持 non-Applied；已失效 attempt 不得 Applied。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | 重放绑定相同 request/evidence revision；恢复解析 GID 与 high-water marks；旧 attempt 不得复用授权。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | Applied 不等于模型理解；Accepted/Delivered/ACK 单独不能暴露下游结果。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F6 — I Authorization / PermissionEpoch / revocation

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** I 是唯一策略/授权权威；所有子系统负责执行
- **阻塞原因：** I 规范根缺失。Scope/Permission 模型仍将策略与 cache/revocation 保证列为开放项。Authorization ADR 只处理类型/存在性，不证明 I 签发真实性、密码学信任、密钥托管或 quorum。
- **缺失项 / 提供者：** IMPL2/I 恢复/处置策略根；I 提供 issuer、signed decision/attestor、PermissionEpoch、revocation/cache freshness 与 verifier；所有域提供负向执行测试。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | 只有 I 能签发 authorization/attestation 和 policy/epoch 变更；消费者只能验证，不得伪造签发。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | 绑定 actor、action、resource、Scope、purpose/context、policy version；返回 decision ID、issuer、subject digest、issued time、epoch。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | Principal、Scope、policy version、PermissionEpoch、decision ID、attestation ID、revocation cursor 分离。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | decision 绑定不可变 subject digest+policy version；subject/policy 改变必须产生新 decision。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | policy/grant/epoch mutation commit 是 currentness 点；受保护操作在自身边界检查当前 epoch。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | decision 与 revocation/epoch 历史必须持久且可审计；完整 I ledger 缺失。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | policy service 不可用、issuer 未知、epoch 过期或 decision 含糊时，受保护操作 fail-closed。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | retry 重新评估当前授权；撤销后旧队列工作不得继续执行。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | 所有 read/write/publication/retrieval/Forget/restore 边界都执行当前 I policy 和 Scope。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F7 — Global Forget inventory → per-target evidence → I completion

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** I 拥有全局策略/完成；D canonical Fence；各执行域拥有本地证据
- **阻塞原因：** D 明确将全局完成和物理擦除策略交给 I。I 根缺失。D Fence 为 Draft/Unverified/Informative；inventory、backup/external-copy 和 exception 策略尚未接受。
- **缺失项 / 提供者：** IMPL2/I 恢复/处置 I 根；I 定义 inventory、完成谓词、残留例外/backup 和 receipt；D/E/F/G/H/Storage 提供逐目标证据。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | I 定义 inventory/completion 并唯一签发全局完成；D 签发 Fence；各域签发本地 ack。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | Global operation 绑定不可变 inventory version/digest 和 policy；响应逐项列出每个 target 的 typed state/evidence。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | I operation/policy epoch、D Fence cursor、各域 ack ID、Storage projection cursor、backup/external IDs 独立。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | Global op ID+inventory digest+policy version；逐目标 ack 绑定 op+target+Fence generation。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | D Fence commit = 逻辑抑制；I durable completion decision 必须在所有目标证据/例外策略通过后发生。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | D Fence、逐目标 receipts、I completion receipt 均须持久；I receipt 合同缺失。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | 缺目标、executor unknown、offline backup 或未核验外部副本均阻止完成，除非 I 明确批准例外。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | 按稳定 operation ID 对账；restore 先重放 Fence 再 cleanup；inventory 变化必须重新评估。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | D Fence 立即抑制；全局完成不应阻塞初始抑制；物理副本受 I 策略管辖。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

### F8 — Storage atomicity / durability / crash / restore

- **整体状态：** BLOCKED_WITH_REASON
- **权威 / Owner：** Storage/Consistency 负责物理保证；D/E/F/G/I 保留逻辑权威
- **阻塞原因：** Storage trait 仅是候选接口，未选择 backend；测试只是合同形状测试，明确不证明后端原子性、崩溃恢复、多进程序列化或持久性。SQLite 代码只是实现材料，不是已接受证明。
- **缺失项 / 提供者：** IMPL2 固定物理合同；Storage/Consistency 规定事务/隔离/持久性/恢复/same-GID；D/E/F/G/I 接受边界；需可复现故障注入/崩溃证据。

| 检查点 | 合同预期与 PASS/FAIL 判据 | 当前结果 |
|---|---|---|
| **Issuer** | Storage 只证明物理 commit/rollback/Unknown；D 签发 canonical commit/Fence，E Accepted，G Applied，I policy/completion。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **请求/响应** | typed transaction request 绑定 participants、GID、immutable writes、CAS、receipts/outbox、Fence/epoch guards；响应为 committed/aborted/Unknown 并带 proof。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **身份/游标命名空间** | Storage GID/participant、D cursor、E receipt、F watermark、G Applied ID、I epoch 分离；same-GID join 明确。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **幂等范围** | GID+immutable participant/request digest；重复 prepare/commit 返回同一 terminal proof；digest 不同则冲突。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **线性化点** | 物理 transaction commit（或约定的 COC terminal commit）；VisibilityPointer/Receipt 原子提交；逻辑 Owner 决策仍独立。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **持久回执** | Prepared/terminal participant records、commit receipt、visibility pointer、outbox、recovery high-water 均持久。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **失败/Unknown** | commit 前崩溃=abort；提交中崩溃查询 GID；Unknown 解析前保持 hidden；明确记录 heuristic outcome。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **重放/恢复** | 发布前解析 prepared GID/participant/high-water；restore 在 read 前恢复 Fence/PermissionEpoch/watermark。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |
| **可见性** | 仅在权威谓词通过后由原子 VisibilityPointer/PublicationReceipt 发布；D Fence projection 可重建且非权威。 | NOT EVIDENCED — 不满足 Gate A 关闭条件 |

## 4. 跨流程不变量

1. 权威分离：E Accepted、D CanonicalCommit/Fence、F watermark、G Applied、H 协议证据、I 授权/完成和 Storage 物理提交是不同事实，子系统不得签发其他 Owner 的事实。
2. 命名空间分离：Producer 幂等键、D commit cursor、D ForgetFence cursor、F watermark、G ContextVersion/Applied identity、H delivery/evidence revision、I PermissionEpoch、Storage GID/participant/receipt 不可互换。
3. Unknown 不等于成功：可能已持久提交但响应丢失时，必须通过对应 Owner 的持久回执/账本核对；不得换新身份盲目重试。
4. 可见性严于接收：Accepted、Delivered、ACK、canonical commit、indexed、Applied、逻辑抑制、物理擦除和 Global Forget 是不同状态。
5. 恢复顺序：暴露 Storage 投影、F 索引、G Context/Applied、H 重连输出或 E 队列工作前，先恢复 D Fence 与 I 授权当前性。
6. 源文件存在不等于接受：Draft/Unverified/Informative 文档或通过的单元测试，不构成精确版本 Owner 接受或端到端证据。

## 5. Gate A 处置与提供者

| 必需项 | 当前状态 | 提供者 / 下一份证据 |
|---|---|---|
| E ingress receipt + producer lifecycle | OPEN | IMPL2/E 恢复或处置缺失根；E 固定 receipt、dispatch、lease、retry；I/D/Storage 确认边界。 |
| D canonical commit + outbox | OPEN | IMPL2/D 恢复 canonical store 根；D+Storage 提供原子 commit/outbox/receipt 与崩溃证据；F 接受 feed。 |
| F retrieval 与 scan coverage | OPEN | IMPL2/F 恢复规范根；D 固定 feed；F 提供连续 watermark 与 gap/rebuild 证明。 |
| D Forget Fence 与派生可见性 | OPEN | D/I/E/F/G/H/Storage 提供精确逐目标合同与接受；IMPL2/I 提供策略根。 |
| C/H/G Applied | OPEN | C/H/G/Storage/D/I 对齐精确 join 合同；G 证明账本恢复；各 Owner 接受自身证据。 |
| I authorization/revocation | OPEN | IMPL2/I 提供规范根；I 提供 issuer/epoch/revocation/verifier；各域提供负向执行测试。 |
| Global Forget completion | OPEN | I 定义 inventory、例外、备份/外部副本策略与完成回执；D/执行方提供逐目标证据。 |
| Storage atomicity/durability/restore | OPEN | IMPL2 固定物理合同；Storage 提供 transaction/same-GID/fault-injection/crash/restore 证据；逻辑 Owner 接受边界。 |
| Owner A 完整审查协调 | OPEN | Owner A 读取八条流程、所有源 pin 和双语对等性。 |
| 前序矩阵七项 CONDITIONAL 角色保留 | OPEN | 各角色按精确源版本解除条件；代理处置不是自然人签署。 |

Gate A 仍为 PARTIAL / OPEN。Gate B 仍为 NOT VERIFIED。Issue #1212 保持 OPEN。不授权实现、合并、部署或关闭 Issue。

## 6. 审查程序

每个检查点必须引用精确源路径与 blob SHA，指出 issuer/consumer，并附具体测试/证据后记录 PASS/FAIL。若前置条件缺失、含糊、仅候选或未接受，记录 NOT EVIDENCED 并保留 BLOCKED_WITH_REASON。不得把缺失源转换为假定合同。

本包可交付域 Owner 审查，但不满足 Gate A 关闭条件。任何源文件实质变化，都必须更新基线并重新生成 blob pins。
