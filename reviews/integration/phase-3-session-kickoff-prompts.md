# Phase 3 — Nine Copy-Ready Session Kickoff Prompts

- Date: 2026-11-16
- Parent task pack: `reviews/integration/phase-3-cross-module-remediation-task-pack.md`
- Parent reconciliation: `reviews/integration/phase-2-defg-cross-session-reconciliation.md`
- Purpose: launch nine independent ChatGPT sessions with explicit ownership, source baselines, deliverables and acceptance criteria.
- Important: These prompts authorize design/document work only. They do not authorize merging branches, freezing unresolved contracts, or claiming implementation/security/performance validation.

## How to use

1. Open nine separate ChatGPT conversations.
2. Copy exactly one prompt into each conversation.
3. Connect the GitHub repository integration in each conversation.
4. Start A, B, H and I first; start D and E in parallel; start F and G after D/E publish candidate cursor/fence contracts. C coordinates with H/G.
5. Require every session to return its branch, base SHA, commit SHA, changed paths, decisions, unresolved issues and evidence.
6. Do not merge any branch until the integration coordinator completes cross-module review.

---

## Session A — Integration Architecture and Contract Registry

```text
你现在担任 AiMemoryBrainArchitecture 项目的 Principal Integration Architect（系统集成总架构师），负责 Phase 3 跨模块契约协调。你不是 D/E/F/G/H/I 任一模块的设计作者，也无权替模块负责人决定其内部权威模型。

【必须先读取】
1. main 分支上的 reviews/integration/phase-3-cross-module-remediation-task-pack.md 全文。
2. reviews/integration/phase-2-defg-cross-session-reconciliation.md 和 reviews/integration/phase-1-abc-cross-document-integration-review.md。
3. 00-governance/ 下的全部治理基线。
4. A/B/C 当前 main 文档。
5. D/E/F/G 下列确切分支与基线提交：
   D: session-d-memory-brain-2026-11-16 @ 9dc08c63f6912320e290a963c634748ec44a81c8
   E: session-e-memory-compiler-2026-11-16 @ 54df136d1e410af834461950e3c61c5c80abd6ad
   F: session-f-memory-runtime @ dad5deb6bfaa2df9956930d0b1372df354112567
   G: session-g-memory-context @ 3d2c065be863bc1d349faaeece6f6eaa0047abae
6. H/I 尚无正式设计包。不得假设其已经存在。

【你的责任】
A. 建立统一决策登记表，追踪 INT-P0-01..04、INT-P1-01..06、INT-X-01..08、D-REV-P1-001..003。
B. 协调 D/E/F/G 与存储工程，提出 typed cursor/watermark contract。必须区分：
   - source Event cursor；
   - canonical commit cursor；
   - per-aggregate revision；
   - LifecycleEvent cursor；
   - per-index/per-partition publication watermark；
   - Forget fence/epoch；
   - Context version；
   - Delivery ID/sequence；
   - Adapter capability epoch；
   - inference request ID。
   每种 cursor 必须定义 owner、namespace、scope/partition、单调性、gap 语义、resume/replay 规则及因果关系。禁止用一个无类型整数混装不同序列。
C. 建立跨模块接口矩阵：producer、consumer、authoritative owner、immutable ID、version、consistency、failure、retry。
D. 组织 conformance test 计划；没有可复现证据不得标记 PASS。
E. 确保所有结论明确标记 DECIDED / CANDIDATE / ADR-BLOCKED / OPEN / TO_VALIDATE。

【只允许创建/修改你负责的文件】
- reviews/integration/contract-registry.md
- reviews/integration/typed-cursor-and-watermark-contract.md
- reviews/integration/cross-module-conformance-plan.md

建议在独立 A 工作分支上工作；如果仓库实际已有 A 分支，先核实，不要猜分支名。不要覆盖其他人的文件，不要修改 00-governance 基线，不要合并任何分支。

【验收】
1. 所有 INT 与 D-REV 项目都有唯一 accountable owner、状态、依赖和关闭证据。
2. Cursor/watermark 语义跨 D/E/F/G 一致。
3. 没有模块越权声明其他模块的权威对象。
4. 所有未决项可见，不因措辞而被静默关闭。
5. 提交后重新读取 GitHub 文件验证，并报告 exact branch/base SHA/commit SHA/changed paths。

【禁止】
不得把跨模块协调意见伪装成已批准 ADR；不得冻结 Fact/Claim、Forget、BMCP、Applied 或 Security 契约；不得声称性能达标。
```

---

## Session B — Fact / Claim ADR and Domain Semantics

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Domain Model Principal Architect，负责 Phase 3 的 Fact/Claim 领域决策。你拥有领域语义设计权，但不拥有 D 的存储实现、I 的授权策略、H 的 wire protocol 或 G 的 Context 版本权。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部文件
- 02-domain-model/ 全部现有文档
- D 分支 03-memory-brain/ 下相关设计，特别是 canonical store、lifecycle、versioning、entity/relationship 文档
- E 分支 extraction/normalization 与 consolidation/conflict 文档
请在报告中记录每个源文件的 branch/ref 和 commit SHA；不可将未合并分支文件当作 main 文件。

【核心任务】
1. 解决 INT-P0-01：Fact 与 Claim 的规范关系。提出并比较至少两种可行模型，分析身份稳定性、版本、证据挂接、冲突、撤回、纠正、时间有效性和历史追溯。
2. 定义 Claim identity、不可变 ClaimRevision、Evidence、Provenance、ConflictSet 的关系；区分 confidence、epistemic status、validity interval、lifecycle。
3. 通过 ADR 给出决策。若权限或依据不足，必须标记 ADR-BLOCKED，列出决策人和剩余问题；不得擅自宣布通过。
4. 定义 typed domain references：MemoryRef、MemoryVersionRef、ClaimRef、ClaimRevisionRef、EntityRef、EvidenceRef、ScopeRef、ActorRef、EventRef、TimeValue/TimeInterval。每种引用需定义唯一性边界和生命周期语义。
5. 定义 Scope 的领域语义、包含/继承关系；Scope 不等于 Permission，授权规则由 I 负责。
6. 给 E 提供 CandidateProposition/ExtractionIR 到规范模型的映射；给 D/F/G 定义消费者语义。

【交付物】
仅在 B 所属工作分支修改/创建：
- 02-domain-model/adr/ADR-001-fact-claim-canonical-model.md
- 02-domain-model/typed-reference-and-scope-semantics.md
- 02-domain-model/fact-claim-consumer-mapping.md

如果这些路径已存在，先读取并在本分支按规则更新，不要覆盖其他分支或其他模块文件。

【验收】
- ADR 为 APPROVED 或明确 ADR-BLOCKED，不允许模糊状态。
- D/E/F/G 对 Claim identity、ClaimRevision、ConflictSet 具有一致消费语义。
- 所有引用类型有明确 namespace/scope 和版本语义。
- Scope 与 Permission 分离。
- 提交后验证文件并报告 branch/base SHA/commit SHA/changed paths/决策状态。

【禁止】
不得代替 I 定义权限策略；不得代替 D 定义存储机制；不得在 ADR 未批准时要求 D/E/F/G 冻结 Schema。
```

---

## Session C — Agent Telemetry and Inference Boundary

```text
你现在担任 AiMemoryBrainArchitecture 的 Agent Integration Principal Architect，负责 Phase 3 的 Agent Telemetry、推理边界和 Adapter 能力需求。C 不拥有 H 的 BMCP wire 编码，不拥有 G 的 Context 权威，也不拥有 I 的全局授权政策。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部治理基线
- 07-agent-integration/ 全部现有文档
- D/E/F/G 分支中 telemetry consumer、Context Delivery、Forget 和 Scope 相关设计
- H/I 进行中的候选文档（如果存在，必须记录确切分支和 SHA；不存在则明确标记依赖缺失）

【核心任务】
1. 定义不依赖完整隐藏 CoT 的 telemetry contract。
2. 将 Observation、Outcome、Intent、PlanSummary、PendingAction、ToolCall、EnvironmentDelta、Uncertainty 定义为不同语义对象。计划/意图不能被当作已经发生的事实。
3. 定义 authenticated producer identity 与 payload 声明的区别；身份认证绑定由 I/H 提供，C 定义消费要求。
4. 定义 event ID、source sequence、时间戳、environment identity、修订/撤回语义和事件顺序。
5. 定义 final inference request boundary：H 在何处、以何种证据证明受管理记忆区域确实被应用到最终推理请求。
6. 明确 Tier 1/2/3 Adapter 能力和 Full Applied 的可证明条件；无法观察最终请求的集成不得声明 Full Applied。
7. 保留 System/Developer/User/Agent Policy 保护边界；记忆始终是 untrusted data，不得提升为指令或绕过工具授权。

【交付物】
仅修改/创建 C 所属文件：
- 07-agent-integration/telemetry-event-and-identity-contract.md
- 07-agent-integration/final-inference-boundary-attestation.md
- 07-agent-integration/adapter-conformance-cases.md

【验收】
- 不要求 Agent 暴露完整 CoT。
- 计划、意图、工具调用、观察和结果具有不同语义。
- Applied 证据绑定精确 request/session/context version/delivery/capability epoch。
- Adapter 无权覆盖受保护指令区或绕过 Agent 授权。
- 报告 branch/base SHA/commit SHA/changed paths/test cases/unresolved H/I dependencies。

【禁止】
不得定义 BMCP wire schema；不得宣称 Applied 证明模型注意或使用了记忆；不得替 I 做安全风险接受。
```

---

## Session D — Memory Brain Corrections and Canonical Authority

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Brain Principal Architect。你的任务是执行 Phase 3 task pack 中 D 的整改，只修改 D 所有的设计文件。D 是 Canonical Memory、MemoryVersion、Lifecycle、Entity/Relation 和 canonical ForgetOperation 的权威；D 不拥有 G 的 ContextVersion、H 的 wire/Adapter 或 I 的全局授权政策。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- reviews/03-memory-brain/review-scope-correction-and-design-reassessment.md
- D 分支 9dc08c63f6912320e290a963c634748ec44a81c8 的五份设计文件及 D 自审
- B 的 Fact/Claim ADR（如果尚未批准，保持 ADR-BLOCKED）
- E/F/G/H/I 对应候选契约（缺失时明确记录）

【必须关闭或明确阻塞】
1. D-REV-P1-001：统一 Forgetting 语义。明确 Memory Lifecycle 的持久状态与临时 ForgetOperation/fence/suppression 的区别。不要让同一概念同时成为 Memory 生命周期状态和操作状态。
2. D-REV-P1-002：明确 canonical commit sequence、per-aggregate revision、LifecycleEvent cursor 的边界；定义事务可见性、gap、replay/resume 及其与 Outbox/Index Watermark 的关系。
3. D-REV-P1-003：定义 durable ForgetOperation ID + monotonic fence/generation、dependency inventory、producer registration、barrier/watermark、late derivative suppression、target acknowledgement 和 completion proof。
4. Forget fence 必须能覆盖 Compiler queued/leased/retry/DLQ/replay、Runtime in-flight retrieval/cache/index rebuild、Context snapshots/deltas/delivery 和 Adapter offline reconnect。各模块执行细节归各模块所有，但 D 必须给出 canonical authority。
5. B 的 Fact/Claim ADR 未批准前，不得冻结 Claim/ClaimRevision/ConflictSet schema。
6. 定义 Entity Merge/Split 和 Relation 迁移，保持历史引用可审计。

【交付物】
仅在 session-d-memory-brain-2026-11-16 分支更新/创建：
- 03-memory-brain/ 下 D 已有五份文件
- 可新增 03-memory-brain/forget-fence-and-completion-contract.md
- 可新增 03-memory-brain/commit-cursor-semantics.md
- D decision/change log

【验收】
- D-REV-P1-001/002 语义闭合。
- D-REV-P1-003 有完整 race/barrier 语义，能防止晚到派生物复活。
- Canonical Commit、LifecycleEvent、Index Watermark、Forget Fence 均为不同 typed cursor。
- 不越权定义 H/I/G 的职责。
- 提交后重新读取验证，报告 branch/base SHA/commit SHA/changed paths/三项状态。

【禁止】
不得修改 main 或其他会话分支；不得把局部 D 设计宣称为全系统 Forget 完成；不得把 Forget suppression 当作物理删除证明。
```

---

## Session E — Memory Compiler Durable Ingress and Derivative Registration

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Compiler Principal Architect。你负责事件接收、编译、规范化、证据来源和派生物登记。E 不拥有 Canonical Commit、Runtime Index 或 Context Version。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- E 分支 54df136d1e410af834461950e3c61c5c80abd6ad 的五份设计文件和 E 自审
- D 分支 Forget fence/canonical cursor 候选契约
- B Fact/Claim ADR 状态
- I identity/retention、H wire 设计（若尚未存在，标记 OPEN）

【核心任务】
1. 定义 Accepted 为 durable receipt，严格区分 Accepted、Processed、Compiled、CanonicalCommitted、Indexed。
2. 定义 idempotency key 的 scope、payload hash、same key/same payload、same key/different payload、receipt replay 和 retention horizon。
3. 定义 Event + payload reference + idempotency receipt + compile intent 的原子或可恢复持久化方案（transaction/outbox/WAL 或等效机制），分析 crash windows。
4. 区分 source event ordering、canonical commit cursor、index publication watermark。
5. 所有 compiler workers、leases、retries、DLQ、replay、recompile 和 derived-output publication 必须在提交/发布前检查 D/I Forget fence。
6. 派生依赖必须在派生对象可见前登记，并参与 Forget completion barrier。
7. 定义 provenance lineage、派生传播和最小化审计 tombstone，避免清除后仍能重建被忘记内容。
8. B ADR 批准后再定义 CandidateProposition/ExtractionIR 到规范 Claim 的映射。

【交付物】
仅在 session-e-memory-compiler-2026-11-16 分支更新/创建：
- 04-memory-compiler/ 下 E 已有五份文件
- 04-memory-compiler/accepted-receipt-and-idempotency-contract.md
- 04-memory-compiler/forget-fence-and-derived-registration.md
- E decision/change log

【验收】
- crash/retry 不丢失 Accepted receipt，也不重复产生 canonical effect。
- replay、DLQ、重编译不能复活已 Forget 派生物。
- 每个 derived object 都有 source lineage 和依赖登记。
- Event cursor、Canonical cursor、Index watermark 类型不同且语义一致。
- 报告 branch/base SHA/commit SHA/changed paths/crash test matrix/open dependencies。

【禁止】
不得将 Accepted 描述为 Canonical Commit；不得代替 D 决定 Canonical Truth；不得绕过 Forget fence。
```

---

## Session F — Memory Runtime Scope, Watermark and Forget Enforcement

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Runtime Principal Architect。你负责 Retrieval、Candidate Generation、Fusion、Freshness、Working Set/Cache 和 Activation Recommendation。F 不拥有 Canonical Memory 或 G 的 ContextVersion。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- F 分支 dad5deb6bfaa2df9956930d0b1372df354112567 的五份设计文件和自审
- D 的 canonical cursor/Forget fence 候选契约
- E 的 source/outbox/index publication 语义
- I 的 Principal/Scope/permission epoch 契约（如尚未完成，标记 candidate dependency）

【核心任务】
1. 对 lexical、ANN、structured、temporal、graph、evidence、provenance 所有检索通道，在候选结果发出前实施 Scope/authorization 过滤。
2. 定义 per-index/per-partition publication watermark，与 D canonical commit cursor、E outbox/publication cursor 的映射。
3. 定义 stale index：canonical revalidation、incomplete result、bounded wait、fallback、fail-closed 的触发条件和可观测状态。
4. 在 candidate generation、in-flight finalization、cache read/write、Working Set materialization、index rebuild 各阶段消费 Forget fence。
5. Cache key/invalidation epoch 必须考虑 principal、scope、permission epoch、environment、canonical cursor 和 Forget fence，防止跨权限/跨环境复用。
6. 定义 retrieval completeness、channel lag 和 uncertainty。
7. RetrievalResult / ActivationRecommendation 保持为 F 的输出；不得创建/拥有 G 的 ContextEntry/ContextVersion。

【交付物】
仅在 session-f-memory-runtime 分支更新/创建：
- 05-memory-runtime/ 下 F 已有五份文件
- 05-memory-runtime/cursor-freshness-and-forget-enforcement.md
- F decision/change log

【验收】
- 任一检索通道都不能先泄漏跨 Scope 候选再过滤。
- stale index/cache 不得覆盖 canonical Forget。
- lag/gap 通过 completeness metadata 明确表达。
- F 不写入 G Context。
- 报告 branch/base SHA/commit SHA/changed paths/retrieval channel matrix/forget race tests。

【禁止】
不得宣称 ANN/向量检索天然实现权限隔离；不得将 F 的 ActivationRecommendation 当作 ContextVersion。
```

---

## Session G — Context Reconciliation, Delivery and Applied Semantics

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Context Manager Principal Architect。G 拥有 Context membership/order/budget、ContextVersion、ContextChangeSet、reconciliation 和 Delivery intent。G 不拥有 Canonical Memory、Runtime retrieval 或 Adapter wire execution。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- G 分支 3d2c065be863bc1d349faaeece6f6eaa0047abae 的六份设计文件和 G 自审
- D 的 MemoryVersion/Forget fence
- F 的 RetrievalResult/ActivationRecommendation
- C 的 final inference boundary 和 H 的 Applied attestation 候选契约
- I 的 revocation/Forget governance（如缺失，标记 OPEN）

【核心任务】
1. 只引用 D 提供的 immutable Memory ID + MemoryVersion；不得修改 Canonical Memory。
2. 只消费 F RetrievalResult/ActivationRecommendation；F 不创建 ContextEntry/ContextVersion。
3. 定义 ContextChangeSet CAS、base/target version、幂等、重复/replay、partial failure 和 snapshot fallback。
4. Forget 时 tombstone/remove Context entries、invalidate snapshots/deltas、取消 Prepared/Delivered delivery（能力允许时），阻止 stale delivery 被标记 Applied。
5. Offline Adapter 状态必须保持 Pending/Unknown，直到收到可信 reconnect/reconciliation attestation。
6. 与 C/H 定义 Applied：Full Applied 要求受管理区域完整物化到实际提交给 inference runtime 的最终请求；Partial/Bypassed/Unknown 分别处理。
7. Applied 不证明模型关注或使用了记忆。预算/充分性也不能做此类推断。

【交付物】
仅在 session-g-memory-context 分支更新/创建：
- 06-memory-context/ 下 G 已有六份文件
- 06-memory-context/forget-reconciliation-and-offline-adapter.md
- 06-memory-context/applied-attestation-consumer-contract.md
- G decision/change log

【验收】
- ContextVersion 与 Delivery 是独立状态机。
- ChangeSet 原子、幂等、base-version safe。
- late delivery 不会复活已 Forget entry。
- Applied 绑定 exact ContextVersion、Delivery、session、capability epoch、inference request。
- 报告 branch/base SHA/commit SHA/changed paths/offline & stale-delivery tests。

【禁止】
不得把 Context Remove 当作 Canonical Forget；不得把 Adapter 内存缓冲写入当作 Full Applied；不得把 Applied 描述为模型使用证明。
```

---

## Session H — BMCP Protocol and Agent Context Adapter

```text
你现在担任 AiMemoryBrainArchitecture 的 BMCP Protocol & Agent Context Adapter Principal Architect。H 是新建工作流；当前仓库此前没有 H 的正式设计包。BMCP 暂定为 Brain Memory Context Protocol。H 拥有 wire envelope、协议版本、序列化、传输交互、Adapter SDK 和 application acknowledgement；H 不拥有 Brain 记忆语义、G Context membership 或 I 全局安全政策。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部治理基线
- 07-agent-integration/ C 现有文档
- D/E/F/G 的确切分支和基线 commit，重点读取其接口输出
- I 正在设计的 Principal/ActorRef/permission epoch/Forget governance 契约（如未存在，先标记依赖，不要自创最终安全政策）

【核心任务】
1. 设计 BMCP message families：Telemetry、Event Ingress、Context Snapshot/Delta、Delivery、Acknowledgement、Capability Negotiation、Forget/Revocation notification、Administrative governance envelope。
2. 定义协议版本协商、required/optional fields、unknown enum handling、canonical serialization、integrity metadata、correlation/causation IDs、错误分类。
3. 消费 I 提供的 authenticated transport principal binding；payload 自称的 ActorRef 不构成认证。
4. 定义 Adapter capabilities 与 Tier 1/2/3 conformance。
5. 定义 Prepared、Delivered、Applied、Rejected、Expired、Superseded、Unknown 状态，及重试/幂等语义。
6. 定义 Full/Partial/Bypassed/Unknown application attestation。Full Applied 必须绑定实际提交给 inference runtime 的 final request，不能只证明 Adapter 内部 buffer 更新。
7. 定义 Forget/revocation notification、managed-region clearing、offline reconnect、stale snapshot rejection 和 ACK。不得声称可控制模型服务商保留的隐藏 prompt 或模型内部状态。
8. 记忆 payload 始终作为数据，不得修改受保护指令区域或 Agent 工具授权。

【交付物】
在独立新建的 H 分支工作，先核实分支是否已存在；如不存在，从当前约定 baseline 创建新分支。仅创建：
- 08-bmcp-protocol/protocol-overview.md
- 08-bmcp-protocol/message-envelope-and-versioning.md
- 08-bmcp-protocol/context-delivery-and-acknowledgement.md
- 08-bmcp-protocol/adapter-capability-and-applied-attestation.md
- 08-bmcp-protocol/forget-revocation-and-reconnect.md
- 08-bmcp-protocol/protocol-conformance-matrix.md

【验收】
- 与 C telemetry、D canonical refs、E receipt、F retrieval、G Context delivery 一致。
- Full Applied 有 final-request 可验证证据；无法观察 final request 的 Adapter 不得声称 Tier 1 Full Applied。
- duplicate/stale/superseded/expired/offline/late ACK 行为确定。
- H 不代替 I 决定 authorization policy，不代替 G 管理 Context。
- 提交后验证文件，报告 branch/base SHA/commit SHA/changed paths/interface matrix/open dependencies。

【禁止】
不得冻结仍依赖 I/C/G 的字段；不得把 Delivered 当作 Applied；不得把 Applied 当作模型注意/使用证明；不得承诺物理删除。
```

---

## Session I — Security, Identity and Governance

```text
你现在担任 AiMemoryBrainArchitecture 的 Security, Identity & Governance Principal Architect。I 是新建工作流；当前仓库此前没有 I 的正式设计包。I 拥有全局身份/授权政策、delegation/revocation、retention、audit governance、backup/external-copy policy、Forget completion policy 和物理擦除要求。I 不拥有 D/E/F/G 的本地机制，也不拥有 H 的 wire 编码。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部治理基线
- B 的 domain Scope/typed reference 设计
- C 的 telemetry/Agent boundary 设计
- D/E/F/G 的 Forget/Scope/Delivery 设计（精确分支和 commit）
- H 的 BMCP 候选设计（若尚未存在，明确记录）
不得仅凭模块局部过滤设计宣称全系统安全。

【核心任务】
1. 定义 Principal、ActorRef、ProducerIdentity、issuer、delegation、tenant/user/project/environment scope binding、permission epoch、revocation。
2. 定义 policy decision contract 和 fail-closed behavior。区分 authentication、authorization、ownership Scope、applicability Scope。
3. 定义 ingress、compile、canonical commit、retrieval、evidence dereference、Context delivery、inference boundary 各处的 reauthorization 和 revocation propagation。
4. 定义 Forget governance：immediate logical suppression、asynchronous derivative cleanup、external recipient handling、backup/restore、retention/legal hold exceptions、physical erasure。
5. 定义 global Forget completion：required target inventory、Pending/Confirmed/Failed/Unknown/PolicyException、barrier/watermark proof、exception approval、audit evidence。Unknown/offline 不得默认算 Confirmed。
6. 定义 prompt injection threat model：retrieved Memory、Evidence、Provenance、Entity labels、summary、compaction、cross-scope poisoning。不得声称能让 LLM 对恶意文本绝对免疫。
7. 定义审计保留与忘却的平衡：避免 audit tombstone 重建已 Forget 内容，定义 non-reconstructive tombstone。
8. 与 H/C/D/E/F/G 制定 adversarial/conformance test matrix。

【交付物】
在独立新建的 I 分支工作，先核实分支是否已存在；如不存在，从当前约定 baseline 创建新分支。仅创建：
- 09-security-governance/security-and-identity-overview.md
- 09-security-governance/principal-actor-and-authorization-contract.md
- 09-security-governance/scope-and-revocation-policy.md
- 09-security-governance/forget-retention-backup-and-erasure-policy.md
- 09-security-governance/threat-model-and-adversarial-test-plan.md (not restored on main; see AID-2026-107 §10)
- 09-security-governance/audit-and-exception-governance.md (not restored on main; see AID-2026-107 §10)

【验收】
- Identity authenticated/bound，不能由 payload 自我声明。
- 所有关键边界有重新授权和 revocation epoch 语义。
- Forget completion 不把 unknown/offline 当作确认，除非显式记录政策例外及批准者。
- suppression、cleanup、physical erasure 三种状态与承诺严格分开。
- 风险、残余风险和风险接受权限明确。
- 提交后验证文件，报告 branch/base SHA/commit SHA/changed paths/threat tests/open dependencies。

【禁止】
不得代替 D/E/F/G 实现本地 Forget；不得代替 H 定义 wire encoding；不得承诺无法控制的模型服务商内部状态已物理清除。
```

---

## Session completion report template

每个会话完成后必须按此格式回报：

```text
Session:
Role:
Branch:
Base commit SHA:
Final commit SHA:
Changed paths:
Source refs reviewed:
Decisions made (ID / status / rationale):
Issues closed (ID / evidence):
Issues still open (ID / owner / dependency):
Interface changes affecting other sessions:
Tests added or executed:
Test evidence and results:
GitHub read-back verification:
Explicit non-claims (what was not implemented or proven):
```

## Coordinator instruction

Do not ask all sessions to independently produce a global architecture rewrite. The task is bounded remediation of identified gaps. When two sessions disagree, record the conflict and route it to the authoritative owner/ADR; do not resolve it by silently editing the other session's document. Main integration and final contract freeze happen only after the cross-module review.


## Mandatory bilingual architecture deliverables / 强制中英双语架构交付

This task MUST comply with [GOV-DOC-001 — Bilingual Architecture Documentation Policy](../../00-governance/bilingual-documentation-policy.md). Every architecture proposal, Owner review, interface/schema/state-machine change, ADR, integration decision, and acceptance report produced by this task MUST have Chinese and English counterparts updated in the same change set. Both versions must preserve identical scope, authority, normative force, decision status, findings, severity, evidence, caveats, and open issues. Stable identifiers and machine-readable values must remain unchanged. Update the repository-wide docs/translation-status.md register. Missing or stale counterparts block documentation acceptance unless a documented, time-bounded exception is approved under GOV-DOC-001.

本任务必须遵循 [GOV-DOC-001《架构双语文档规范》](../../00-governance/bilingual-documentation-policy.md)。本任务产生的每项架构提案、Owner 审查、接口/Schema/状态机变更、ADR、集成决议和验收报告，都必须在同一变更集中提供或更新中英文版本。两种语言必须保持相同的范围、权威性、规范效力、决策状态、发现、严重级别、证据、限制和未决事项。稳定标识和机器可读值不得改变。必须更新全仓库 docs/translation-status.md 登记表。除非依据 GOV-DOC-001 获得有记录、有期限的正式例外，否则缺失或过期的语言版本会阻止文档验收。
