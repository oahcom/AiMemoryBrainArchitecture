# BMCP 架构完成——语义契约与工程交接

- 工作项：BMCP-ARCH-FOLLOWUP-001；文档：BMCP-ARCH-001；版本：0.2.3
- 状态：CANDIDATE / ARCHITECTURE_PARTIAL——不是已冻结协议规范
- Stage B 候选基线：2efcbd09f4e6ba499e9d22be72fa04d5135a0de7
- H 源快照：session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74
- 对应版本：[English](BMCP-ARCH-001.en.md) | [中文版本](BMCP-ARCH-001.zh-CN.md)
- 范围：架构语义、阶段边界、依赖映射、验收计划和工程交接
- 排除：Runtime 代码；H 所有的规范 Wire/Schema/Transport/ACK/Validator 修改；D/I 权威变更；C 的 Agent/MCP-to-BMCP Mapping 决议。Owner 已决定 Fact/Claim 语义；精确消费者/Wire Mapping 仍为 Candidate。

## 1. 处置结论

**ARCHITECTURE_PARTIAL。** 本文是候选语义整合和工程交接，不是协议冻结。

H 实时分支包含候选 Envelope、版本、规范化、错误分类、Delivery/ACK、Forget/重连、Strict JSON Parser 参考和符合性材料。这些文件仍归 H 所有；文件存在不等于批准或冻结。H 生命周期交接明确标记 Wire Schema NOT FROZEN；符合性矩阵是候选测试规范，不是 Runtime 证据。

Owner 已合并批准 Fact/Claim 语义决策（Option A + I1）；精确 Compiler/Domain 消费者映射仍为 Candidate。BMCP MUST NOT 冻结规范 Fact/Claim Wire Payload 字段。D 拥有 Canonical Identity/Lifecycle 和 D Forget Fence；I 拥有授权和 PermissionEpoch。BMCP 消费这些权威，不得创建替代机制。

Issue #7 的记录保持 IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE。根据 Owner 阶段关闭裁决，GitHub 当前报告 Issue #7 为 CLOSED / not_planned；本工作不重开或修改它。延期不等于 Runtime 授权。

**规范名称：** 仓库规范术语表 `00-governance/terminology.md` 将 BMCP 定义为 **Brain Memory Context Protocol**（main `c58878fce24528a0842b4f8887c93ddbf465b566`，术语表 Blob `b8770fbb58e4fac087698043c40a57531b1d244d`）。初始派发文本中的 “Brain Memory Control Protocol” 在本仓库中不是规范名称，予以纠正。H 的协议文档必须保留 “Context”；名称问题不再是未决项。

## 2. Stage B 当前来源登记（main @ 88bf4875）

本表的 Main 来源 Pin 已统一对齐到 Stage B 基线 main @ 2efcbd09f4e6ba499e9d22be72fa04d5135a0de7。32 条 Pin 均按精确 Git Tree Blob 复核；其中 9 个来源路径的 Blob 与 C588 历史快照不同。H 来源 Pin 仍来自 H 分支 session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74。本表只记录锚点，不替代对变更来源的语义影响审查。

| 来源 | Ref | Blob SHA | 状态 / 用途 |
|---|---|---|---|
| docs/en/08-bmcp-protocol/bmcp-guide.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 228d28671955c977f653bef5b537554e431f9137 | CANDIDATE 概览 / H 权属 |
| 08-bmcp-protocol/protocol-overview.md | H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | b88ef3a6fd3be293e7c2e77d9652f386b169bc47 | CANDIDATE |
| 08-bmcp-protocol/message-envelope-and-versioning.md | 同一 H ref | 5547ecd78d118bd63e571e5daad87194d9b694e4 | CANDIDATE；H 所有 |
| 08-bmcp-protocol/context-delivery-and-acknowledgement.md | 同一 H ref | bf9732cc39d156853b507c3a3a4e573159978f49 | CANDIDATE；G 语义 / H Wire |
| 08-bmcp-protocol/adapter-forget-ack-and-target-binding.md | 同一 H ref | 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8 | CANDIDATE；H Wire，D/I/G 权威 |
| 08-bmcp-protocol/phase-3.7-h-lifecycle-handoff-envelope-semantics-not-frozen.md | 同一 H ref | b2a2648d5576511f68fdb9d87ce4388a1fedd5e9 | NOT FROZEN |
| 08-bmcp-protocol/protocol-conformance-matrix.md | 同一 H ref | 075b2ac6ebe9bda4ec83de04fad07e8027e6a440 | CANDIDATE 测试；无 Runtime PASS |
| 08-bmcp-protocol/runtime_reference/strict_json_parser.py | 同一 H ref | 3b9b3da645448c773c95a9dcd3c57c8c109bb2da | 参考模型，不是生产 Transport |
| 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | H @ `3e8b33df18b9e6fc757ca84ff07a12faebc78e74` | 4b664e3bce465499bcdfd93796349a4ba7074002 | H 来源 Schema；文件名/$id 为 1.0.2，但 Envelope schema_version const 为 1.0.0 |
| docs/en/04-memory-compiler/README.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 5f50d470bf26d46dfffad48ad23059fc7a36c489 | E/D/I 权属 |
| 06-memory-context/README.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 684490d1c4e2c3aeb0236a9083abf9a144f2744c | G Context 子系统概览 |
| 06-memory-context/context-architecture.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 56fcc0ea112d423ef69a3f00e9d626bf4230ca0e | G Context 架构与权属 |
| 06-memory-context/context-versioning.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b | G ContextVersion / ChangeSet / CAS 语义 |
| 06-memory-context/context-reconciliation.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 87063aceebed1c30b7840045ada8e3f348732688 | G Reconciliation 语义 |
| 06-memory-context/context-manager.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | ecc0549137a1738c197d02d12d94a1eb971ed6b5 | G Context Manager 边界 |
| docs/en/04-memory-compiler/compiler-overview.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | c89a256afda105ceac3db75d743ab58d177ef586 | E 流水线 |
| docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | f2a4007f4b17e33de9bcd183c57ee504cfeef6cd | CANDIDATE E Receipt |
| docs/en/07-agent-integration/agent-integration-guide.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 7952e808d7ad58267608f720617fd38effa32322 | C 所有 Agent 边界 |
| docs/en/03-memory-brain/forget-fence-and-completion-contract.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | c791895333ab6140f035f4f622d5dee9325d422d | D/I Forget 边界 |
| docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 9c054932994bb078e2834df8bd66f73895aa04f5 | D Lifecycle/Fence |
| 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593 | 历史 ADR；语义决策已被取代；消费者映射仍为 Candidate |
| 14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d`（批准来源 `c138654c942dc93b5a36eccb2ff0e41452156429`） | d59756a8eb454480804c482ca03c68345ab5abf2 | 当前来源 Pin；Owner 语义批准是历史证据（Option A + I1），不冻结 Schema |
| docs/en/03-memory-brain/memory-versioning.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 4efbd26db9586f6fcf1897f42ffba287d625b903 | D Revision / Consumer Freeze 边界 |
| docs/en/03-memory-brain/commit-cursor-semantics.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 2de7fe35229372ae5b06093e5e031c2c243fbd7c | D Cursor 语义 |
| docs/en/09-security-governance/security-governance-guide.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 061c5847b3df879eeaf3c71e5eae0bfa162b276a | I Principal / Authorization / PermissionEpoch |
| docs/zh-CN/09-security-governance/security-governance-guide.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 372d27c79dc79d09bcdb0f142c979efdba1c2b6e | I 双语对应文档 |
| 07-agent-integration/agent-integration-overview.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 0d66fb8383197d27dd04792b084b19d99bb81e93 | C 规范 Agent 边界 |
| 07-agent-integration/adapter-capability-tiers.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 17ef7914387de02637c6055c833b384fddf680e6 | C Capability Tiers |
| 07-agent-integration/inference-boundary-model.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | e2d5cb6abd9ec40da6e3680531de5944fc8b14df | C Inference Boundary |
| 07-agent-integration/telemetry-model.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0 | C Telemetry |
| 08-bmcp-protocol/protocol-index.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 309d70845495013fe679b6870b0ab299877c9b55 | Main BMCP 协议工件索引；RecoveryJoin 1.0.2 条目 |
| 08-bmcp-protocol/protocol-index.zh-CN.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 3ffa15e255c585962b94515e8e6bcdf37f1dba75 | BMCP 协议工件索引；RecoveryJoin 1.0.2 条目 |
| 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | f951427a20c32930eb93ae955011ecb40c6b1667 | RecoveryJoin 1.0.2 结构 JSON Schema；不构成 H Wire 冻结 |
| 08-bmcp-protocol/validators/recovery_join_validator.py | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 0080a722db7665fc3bd4ead756dfa50fa712b705 | 结构验证 + 注入式 D 权威回调；候选参考实现 |
| 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 7ae54e0f7777ea2f41b7870e331aa8f388338a6c | RecoveryJoin 1.0.2 类型绑定 / UNKNOWN 状态测试 |
| 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | bc8709fda08cad9d00044205cf1eb1fb8f1a6ff4 | RecoveryJoin Schema / 索引 / Fixture 测试 |
| crates/memory-context/tests/e2e_negative_paths.rs | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | b5b854c5e586e7e8a4cc95f8855331d9f8c8c857 | G 跨 Crate SQLite Store→Context 负向 E2E 测试 |
| crates/memory-store/src/lib.rs | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | 6059b3f088922c87f49993a6cbd80c49a884a1c8 | G MemoryStore 实现源码 |
| crates/memory-domain/src/lib.rs | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | b96cb2f74c56ab8a28da7e3ceffcf4adcb1b98d4 | 规范 Claim/Fact Revision 领域类型 |
| 00-governance/terminology.md | main @ `88bf4875d1d6266c26cf5e293e43e7d402f7006d` | b8770fbb58e4fac087698043c40a57531b1d244d | BMCP 规范名称 / 术语权威 |
| C Family Boundary 决策 | PR #430 comment 7060351480；Issue #449 comment 7060126722 | Owner-delegate 决议；不声称独立人工 C 签名 | Family 方向已决定；精确 H Operation Registry / C-H Mapping 仍 OPEN |
| H Confirmation 范围澄清 | PR #428 comment 7060351041；H Scope Correction comment 7060264372 | 仅接受 Owner-delegate 逻辑选择；INDEPENDENCE_UNVERIFIABLE | H-CONFIRM-001..004 各自均为 PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN |
| B domain-model-overview.md | B 分支 `session-b-domain-model-phase3 @ 840202a98cf40a0b3f194afb84bed4d5f3326658` | Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | B 接受 Option A + I1；来源对齐仍待完成 |
| D memory-versioning.md | D 分支 `session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424` | Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb` | D Identity/Revision/ConflictSet 边界；Schema/Currentness Gate 开放 |
| D forget-fence-and-completion-contract.md | 同一 D ref | Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` | D ForgetOperation/Fence 权威 |
| I principal-actor-and-authorization-contract.md | I 分支 `session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6` | Blob `03765efac4bb1153f303ce0030f9e277d602e81d` | I Principal/Actor/Attestor Authorization 边界 |
| I scope-and-revocation-policy.md | 同一 I ref | Blob `71df6aaf21bb1767cd9fe5c947581b871325e023` | I PermissionEpoch/Revocation |
| I global-forget-target-inventory-and-completion-evidence.md | 同一 I ref | Blob `9100061fa986fb6676656169de3fcf9fc1c72664` | I Retention/Global Forget Evaluation |
| PR #436 协议索引/provider_outcome 测试 | PR Head 1ffed9ed127df98b2f823a66ec80ea43d08cb9dc；Merge Commit 02f61194fd4e12993b4c83f7fac8382eee20f5d8 | 已合入 Main | 结构性 Provider Outcome 证据；5 passed / 5 semantic skips |

本次更新已从实时 `session-h-bmcp-protocol` 分支重新读取上述八个 H Blob Pin；它们在当前分支 HEAD `3e8b33df18b9e6fc757ca84ff07a12faebc78e74` 均解析为表中 Blob SHA。此处是有界来源登记，不代表所有 H 工件或消费者均已独立审查。

### 2.3 B/D/I Owner 决议 Pin

- B Owner 决议：PR #429 comment 7060251435；B 来源分支 `session-b-domain-model-phase3 @ 840202a98cf40a0b3f194afb84bed4d5f3326658`；`domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`。
- D Owner 决议：PR #429 comment 7060243632；D 来源分支 `session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424`；`memory-versioning.md` Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb`；Forget 契约 Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`。
- I Owner 决议：PR #429 comment 7060259541；I 来源分支 `session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6`；Principal/Actor 契约 Blob `03765efac4bb1153f303ce0030f9e277d602e81d`；Scope/Revocation Blob `71df6aaf21bb1767cd9fe5c947581b871325e023`；Global Forget Inventory Blob `9100061fa986fb6676656169de3fcf9fc1c72664`。

## 3. 文件所有权矩阵与修改范围

| 文件 / 区域 | Owner | 本工作项 | 边界 |
|---|---|---|---|
| 08-bmcp-protocol/** | H | 只读 | 不修改 H Schema、Validator、ACK、Transport 或规范 |
| docs/{en,zh-CN}/08-bmcp-protocol/** | H / 文档治理 | 只读 | 不重写指南/状态记录 |
| 04-memory-compiler/** 和 Compiler 文档 | E；依赖语义由 B/D/I 管 | 只读 | 不修改 Compiler 或 Fact/Claim |
| 07-agent-integration/** 和 C Contract | C | 只读 | 不修改 Agent/MCP 策略 |
| D Memory Brain / Forget 契约 | D | 只读 | 不修改 Identity/Lifecycle/Fence |
| I Authorization / PermissionEpoch | I | 只读 | 不修改 Principal/Permission/Global Forget |
| reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | 本 BMCP 架构工作项 | 新建 | 仅候选整合/交接 |
| reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | 同上 | 新建 | 语义对应版本 |
| docs/governance/translation-status.md | Governance Register | 仅元数据 | 登记 Review Pair；保留 H 核心规范状态 |

不涉及 Rust 源码、测试、JSON Schema、Transport/Validator 实现或生产配置。

## 4. Parse / Execute / Respond 契约

### 4.1 分层边界

1. **Wire / Transport Decode——H：** Framing、信道认证、字节到文本/UTF-8 解码、严格 Wire 语法、规范化/完整性和 Envelope 解码。
2. **Protocol Parse——BMCP 语义层：** 只接受解码后的 Envelope 和受保护认证对端上下文；检查协议必填项、版本/能力兼容性和已注册 Family/Operation；规范化类型化 Request。
3. **Execute——操作 Owner/Service：** 路由至允许列表 Handler；获取 I 授权；校验 D Identity/Lifecycle/Fence；调用所属领域 Service。
4. **Respond——BMCP 语义 + H 序列化：** 构造有关联的业务结果或分类错误。H 负责 Wire 表示和序列化。
5. **ACK——H 证据族：** 独立报告 Transport 或 Adapter 观察。ACK 不是业务响应或领域 Receipt。

原始字节 MUST NOT 进入 BMCP Semantic Parse。未来在同一进程部署也不合并权威。

### 4.2 Parse

**输入：** H 解码 Envelope 和受保护认证 Transport Context。Payload Identity 只是声明；认证 Principal 来自可信信道/Security Context 和 I Binding。

**候选逻辑字段：** Protocol Family/Version；Message Identity；Family+Operation 标识；Payload 和 Payload Schema/Content Type；Correlation 和可选 Causation；状态变更操作的 Idempotency Tuple；Source/Recipient Selector；条件性 Scope/Environment Ref；适用的 Owner 签发 PermissionEpoch、ForgetFence、ContextVersion、CapabilityEpoch；Expiry 和 Integrity 结果。

H 候选 Envelope 命名 protocol、protocol_version、message_id、message_type、payload_content_type、payload_schema_version、payload、correlation_id、causation_id、idempotency、scope_ref、permission_epoch、forget_fence 和 capability_epoch。这些是来源字段，**不是已批准字段名/必填性/Schema**。

**规范化内部 Request（不是 Wire Schema）：**

| 成员 | 含义 | 权威 |
|---|---|---|
| protocol_version | 已协商版本 | H |
| message_id | 消息不可变身份；候选 Request 关联键 | H |
| correlation_id / causation_id | 工作流关联 / 直接因果父消息 | H |
| operation_ref | 已注册 Family + Operation | H Registry；语义由 Owner 定义 |
| parameters | 类型化 Payload；Owner 校验前不透明 | 操作 Owner |
| idempotency_ref | Owner 范围 Key + 规范语义摘要 | 操作 Owner；H 传输 |
| authenticated_principal | 受保护对端身份，不能来自 Payload | I 批准 Binding |
| scope_ref / environment_ref | 不透明类型化领域 Ref | 适用时 B/I/D |
| permission_epoch | I 签发授权新鲜度 | I |
| forget_fence_ref | D 签发屏障证据，必要时绑定 I Policy | D/I |
| context_version / capability_epoch | 独立不透明令牌 | G / H |

语义边界要求 Message Identity、已协商 Version、已注册 Operation 和类型化 Payload。多消息/异步操作要求 Correlation。状态变更/可重试操作要求 Idempotency。Scope、Environment、PermissionEpoch、ForgetFence、ContextVersion 和 CapabilityEpoch 由操作 Owner 决定条件性必填；不得虚构通配默认值。Causation 和命名空间化非关键扩展可选。未知关键字段/枚举/操作按 H 最终兼容契约 fail-closed。

Parse 失败：已解码 Envelope 格式错误；缺少必填字段；不支持版本；未知操作；不支持关键扩展；参数结构无效；请求过期。Parse MUST NOT 调用记忆服务、授权副作用、签发身份或改变领域状态。

H 候选协商禁止静默主版本降级。精确 major/minor/patch 和 Payload Schema 协商归 H 所有。

**H 的 Request ID 问题：** 当前 Envelope 定义 message_id，没有独立 request_id。H 必须决定 message_id 是否就是响应 causation_id 引用的 Request Identity，或是否需要独立稳定 Command Identity。BMCP MUST NOT 单方面增加 Wire request_id。

### 4.3 Execute

Execute 仅在 Parse 成功后开始。这是语义分派契约，不是 Runtime Scheduler 规范。

1. 通过版本化允许列表 Registry 解析 operation_ref；未知/禁用操作在副作用前拒绝。
2. 使用受保护认证身份，向 I 批准接口请求当前授权和 PermissionEpoch。Payload Principal/Actor/Producer/Scope 声明不能自我认证。
3. 调用操作 Owner Validator。H 校验协议/Wire 结构，不裁定领域真值或业务权限。
4. 规范 Memory 操作使用 D 所有的 Identity/Lifecycle/Revision 操作。BMCP 不签发 CanonicalRef、不选择 Lifecycle Transition、不分配 Canonical Cursor。
5. 在 D/I 要求的每个受保护边界重新校验 D Forget Fence 和 I Authorization/PermissionEpoch，包括不可逆/可见性改变前。Stale、不可用、不可比较或 Unknown 均阻止操作。D Fence 与 I PermissionEpoch 是不同类型命名空间，禁止比较/转换/替代。
6. 调用所属 Service（如 E Ingress/Receipt、D Canonical Lifecycle、G Context/Delivery）。BMCP 不直接写规范存储或实现 Service 状态机。
7. 相同 Owner 范围 Idempotency Key + 相同语义摘要返回原 Operation/Receipt，不重复副作用。相同 Key + 不同摘要为 Conflict。用同一 Key 和权威查询解决不确定提交；不得创建新 Key 逃避 UNKNOWN。
8. Timeout、响应丢失、进程丢失或持久化结果不确定时保持 UNKNOWN，直到 Owner Reconciliation。Timeout 不证明失败/Abort/成功/未调用。不得盲目重试非幂等副作用。
9. 并发遵循 Owner CAS/Sequencer/Fence/Transaction 规则。BMCP 消息顺序、墙上时钟和 Correlation ID 不是领域提交顺序。Cancel 不等于 Rollback。
10. 返回 Owner 实际 Receipt/Result，不升级语义。E AcceptedReceipt 只代表 E 契约下持久化 Ingress 接受，不代表 Compile、Canonical Commit、Publication 或 Applied。

本文不冻结具体 Operation Catalogue 或 Runtime Service API。

### 4.4 Respond

业务响应是 Operation 语义结果；ACK 是独立 Transport/Adapter 观察。

逻辑响应：已协商 Protocol Version；新的不可变 Response Message Identity；Request 关联；Operation 标识；互斥的 Success/Result 或 Failure/Error；Owner 签发的 Result/Receipt/Evidence Ref；以及 H 批准的安全重试元数据。

**候选关联：** Response causation_id 引用 Request message_id；Response correlation_id 保留 Workflow Correlation；Response 有自己的 message_id。必须由 H 确认，不是冻结 Wire 规则。

只有 Operation Owner 返回其定义的成功终态/Receipt 才算成功。Transport 发送成功、HTTP 2xx、Queue 接受或收到 ACK 不等于业务成功。失败保留 Owner 结果，并区分执行前拒绝、领域冲突、授权拒绝、Timeout/Unknown 和内部失败。UNKNOWN 不得变成确定成功/失败。

H 拥有 Response 字段名、编码、规范化、签名、版本和 Transport。脱敏受保护 Payload、Secret、Credential、内部路径和跨 Scope 对象存在性。存在性披露遵循 I Policy。仅在安全时返回稳定 Code、Correlation 和 Retryability；详细诊断保留在受保护日志。

## 5. ACK、Validator 和错误语义

### 5.1 ACK（归 H 所有）

H 候选设计区分 Prepared/Delivered/Applied/Rejected/Expired/Superseded/Unknown，以及独立 Forget ACK 类别，例如 SUPPRESSED、本地 Buffer/Cache/Queue Action、FAILED、UNKNOWN。Forget ACK 不是 Applied ACK。

| 问题 | 当前证据 | 处置 |
|---|---|---|
| 目的 | 针对一个已识别 Message/Delivery/Action 的有限观察 | H 候选 |
| Receipt？ | 部分 ACK 报告 Transport/Delivery Receipt；边界因 Family 而异 | H 逐类映射 |
| 执行完成？ | 不允许一般性推断 | H 确认 |
| 持久化成功？ | 只有 Owner 专属 Receipt 证明其持久化边界 | E/Storage + H 映射 |
| Timeout/ACK 丢失 | Reconciliation 前 Unknown | H 候选；重试配置归 H |
| 重复 ACK | 相同稳定 ACK ID+Digest 幂等；相同 ID 不同 Digest 冲突 | H 候选；消费者管理状态 |
| 关联 | 精确 Operation/Delivery/Attempt/Session/Target/Evidence Tuple | H Wire 映射；D/G/I 消费 |

H 必须确认 ACK Family、证据边界、持久化点、Correlation Tuple、重试期限、Replay/Retention 和 Consumer Mapping。本文不设计 ACK。

### 5.2 Validator 分层

| 层级 | Owner | 输入 | 输出 / 失败 |
|---|---|---|---|
| Transport Framing、Byte Decode、UTF-8、重复 Key/Canonical JSON、Integrity、认证信道 | H，使用 I 批准信任机制 | 原始字节/信道 | 解码认证 Envelope 或 Wire Reject；不执行业务 |
| Envelope 结构、Protocol Version、Required/Critical Field、注册 Family | H | 解码 Envelope | 协议有效 Envelope 或 H Error |
| Operation 参数结构/Schema | H 管协议 Schema 机制；操作 Owner 管语义约束 | 类型化 Payload + Registry Entry | 结构有效或 Validation Reject；Schema Version 固定 |
| 业务授权 / PermissionEpoch | I | 认证 Principal + Operation + Scope + 当前 Epoch | allow/deny/unknown；unknown fail-closed |
| Canonical Identity/Lifecycle/Forget Fence | D；Policy Binding 由 I 管 | 类型化 Canonical Ref + Operation + Fence Context | Owner 认证的有效/当前结果或 Reject/Unknown |
| Fact/Claim Schema 和 Identity | B 决策，D 管 Identity/Lifecycle，E 管 Candidate Producer | Candidate IR / 拟议规范对象 | ADR 和消费者验收前 BLOCKED |
| ContextVersion / ChangeSet / Delivery | G | Context Payload + 精确 Base/Target | G 校验结果；H 只编码/传输 |
| Runtime Result/Receipt | 执行领域 Owner | 已校验、已授权 Operation | Owner Result/Receipt；H Validator 不推断 |

H Validator MUST NOT 成为业务授权引擎、规范 Schema 权威或 Forget/PermissionEpoch 权威。

### 5.3 错误分类（候选映射，不是冻结 Enum）

H 当前 Envelope 候选列出 ENVELOPE_INVALID、VERSION_UNSUPPORTED、MESSAGE_TYPE_UNSUPPORTED、REQUIRED_FIELD_UNSUPPORTED、ENUM_UNSUPPORTED、INTEGRITY_FAILED、AUTHENTICATION_FAILED、IDENTITY_BINDING_MISMATCH、NOT_AUTHORIZED、PERMISSION_EPOCH_STALE、FENCE_STALE、CONTEXT_BASE_MISMATCH、DUPLICATE_REPLAY、IDEMPOTENCY_CONFLICT、EXPIRED、SUPERSEDED、RATE_LIMITED、RESOURCE_EXHAUSTED、TRANSIENT_UNAVAILABLE、INTERNAL_ERROR。在 H 精确版本契约获接受前仍为候选。

| 请求分类 | 现有 H 候选 / 缺口 | 状态 |
|---|---|---|
| INVALID_REQUEST | ENVELOPE_INVALID；别名/范围需 H | BLOCKED_BY_H_CONTRACT |
| UNSUPPORTED_VERSION | VERSION_UNSUPPORTED | BLOCKED_BY_H_CONTRACT |
| INVALID_PARAMETERS | 无精确通用 Code；可能使用 Owner 专属校验 | BLOCKED_BY_H_CONTRACT |
| UNKNOWN_OPERATION | MESSAGE_TYPE_UNSUPPORTED | BLOCKED_BY_H_CONTRACT |
| UNAUTHORIZED | 区分 Authentication 与 I Policy Denial：AUTHENTICATION_FAILED vs NOT_AUTHORIZED | BLOCKED_BY_H_CONTRACT |
| FORBIDDEN | 候选 NOT_AUTHORIZED；隐藏/不存在由 I 决定 | BLOCKED_BY_H_CONTRACT |
| NOT_FOUND | 未确认 H 通用 Code；I 控制存在性披露 | BLOCKED_BY_H_CONTRACT |
| CONFLICT | 具体候选 IDEMPOTENCY_CONFLICT、CONTEXT_BASE_MISMATCH、FENCE_STALE、SUPERSEDED；无冻结通用 Code | BLOCKED_BY_H_CONTRACT |
| VALIDATION_FAILED | 协议、领域 Schema、授权、完整性错误保持区分 | BLOCKED_BY_H_CONTRACT |
| EXECUTION_FAILED | Owner 定义确定失败与 UNKNOWN；H 映射未确认 | BLOCKED_BY_H_CONTRACT |
| TIMEOUT | 副作用边界不确定即 UNKNOWN；TRANSIENT_UNAVAILABLE 不证明失败 | BLOCKED_BY_H_CONTRACT |
| INTERNAL_ERROR | 候选 INTERNAL_ERROR；脱敏/重试策略待 H | BLOCKED_BY_H_CONTRACT |

概念 Error Response：稳定 Code、Retryable、可选安全 Retry-After、Correlation Ref、脱敏 Detail。精确字段/映射/重试归 H。未经 H 批准不得把请求名称发布为 Wire Enum。

## 6. 跨模块依赖矩阵

| 模块 | 权威 | BMCP 消费 / 交互 | 未决依赖 |
|---|---|---|---|
| H | Wire Envelope/Version、Transport、ACK 编码、Validator、协议符合性 | 认证解码 Envelope；Family Registry；Response/ACK 序列化 | 精确 Wire/Transport/ACK/Validator 仍 CANDIDATE / NOT FROZEN |
| E | Ingress 接受、Candidate IR、Compiler 阶段/Lineage、AcceptedReceipt | 类型化 Ingress Operation；原样返回 E Receipt/Result | 可调用 API 和 Wire 映射；AcceptedReceipt 不等于 Canonical Commit |
| B | Fact/Claim 含义和规范领域决策 | 仅携带 Owner 批准的类型化 Ref/Payload | Owner 已批准 Option A + I1；精确消费者映射仍为 Candidate |
| D | Canonical Identity、Lifecycle、Canonical Commit/Revision、Forget Fence | 传递类型化 Ref 并消费 D Receipt/Currentness | 精确 Runtime API 绑定 |
| I | Principal Trust、Authorization、PermissionEpoch、Revocation、Global Forget Policy | 受保护 Principal Context 和当前授权决策 | 精确批准接口/Profile |
| C | Agent/Adapter 边界、Telemetry、Final Inference Request | C Adapter 将 Agent Request 映射到注册 BMCP Operation | MCP/Adapter Mapping 和 Request Identity |
| G | Context Membership/Version、ChangeSet、Delivery Intent、Applied State | 传递 Context Operation 和 Evidence；G 决定 Context/Applied | 精确字段/API Mapping 和消费者验收 |
| Storage | Durable Transaction、Visibility、Persistence | 仅经所属 Service 调用；透传 Receipt | 不允许 BMCP 直接写 Storage；拓扑延期 |

### 6.1 Memory Compiler

BMCP 不是 Memory Compiler。E 拥有 Candidate IR 和 Compiler Pipeline。BMCP 只能按 E 当前 Schema/Receipt 契约携带 E 所有的 Ingress/Candidate 对象。必须区分：Transport Receipt/Delivery；E 持久化 AcceptedReceipt；Compiler Execution/Candidate；D Producer Admission/Canonical Commit；Dependency Registration/Final Publication；F Indexing/G Context Activation。

合并的 Owner 决策已选择 Option A + I1 作为 Fact/Claim 语义方向。本决策不批准 Fact/Claim Discriminator、Canonical Wire Identity、Schema、DDL 或 Payload 字段。精确消费者映射仍为 Candidate，直至责任工件完成版本 Pin 和审查；相关 Payload 保持不透明，或只使用已批准的中立候选引用。

### 6.2 Agent Integration / MCP

C 拥有 Agent/Adapter 语义；H 拥有 BMCP Wire/Transport。MCP 是 Agent Host ↔ C 的北向 Tool/Resource 接口；BMCP 是 C Agent Adapter ↔ Memory Brain 经 H 的协议边界。MCP Method 不是 BMCP Message。MCP Server 是 C 所有的 Agent Adapter/Gateway，不是 BMCP，也不得形成平行 Canonical Brain API。只有在 H 注册了精确 Family/Operation、且对应版本化契约已 Pin 并获接受时，C MCP Server 才能跨入 BMCP。Agent、Agent Runtime、Model、Provider、Tool、Session 和 Principal 保持不同。

| 逻辑 BMCP Family | 相对 C Adapter 的方向 | C 对 MCP Mapping 的处置 |
|---|---|---|
| Telemetry | Agent/Adapter → Brain | 只有 H 注册精确 Operation 且 I/C Identity/Authorization Binding 获接受后，才可由 Agent-facing Tool 发起 |
| Event Ingress | Producer/Agent → Brain | 只能经 H 注册 Ingress Operation 和 E Durable Receipt/Idempotency 契约；除非返回 E Receipt，否则 MCP Result 不等于 E Acceptance |
| Context Snapshot | Brain → Adapter | 向 C 的入站 Delivery；不是通用 MCP Request/Response Operation |
| Context Delta | Brain → Adapter | 向 C 的入站 Delivery；G 拥有 Version/Base/ChangeSet 语义；不是通用 MCP Request/Response Operation |
| Delivery | Brain → Adapter | 入站 H/G Delivery Lifecycle；C 仅在声明的 Inference Boundary 应用 Brain-managed Region |
| Acknowledgement | Adapter → Brain | C Adapter 发出 H 定义的 Evidence；不是 MCP Success，也不能替代 G Applied |
| Forget / Revocation | Brain/I → Adapter，并带授权控制请求 | C 消费 D/I Owner-issued Control；Agent-facing Request 只能路由到 I/D 授权 Operation，绝不实现 C-local Forget |
| Administrative Governance | I/Control Plane → Adapter/Gateway | 仅控制面；除非有显式 I Policy 和 H Operation Registration，否则不得暴露为普通 Agent Tool |

F 所有的 Retrieval/Recall 在当前 H Family Inventory 中不是 BMCP Message Family。C MUST NOT 发明 BMCP Search Operation。未来任何 MCP Memory-search Tool 都必须依赖单独 Pin 的 F-owned Query API 和 I/D Authorization Path；在此之前状态为 unavailable / dependency-not-ready。

身份映射仅为逻辑层：C 保留 AgentRequestId、AgentAttemptId、AgentTurnId、AgentSessionId 作为 C-owned Identity。H `message_id` 标识每条 BMCP Message；H `correlation_id` 关联 Workflow；H `causation_id` 标识直接父 Message/Event。AgentRequestId 可以作为本地 Workflow Correlation 输入，但 MUST NOT 被序列化为新造的 H `request_id`；每条 H Message 都有自己的 H `message_id`。AgentAttemptId 不是 Transport Attempt ID，也不是 Operation Idempotency Key。状态变更 Operation 使用所属 Owner 的 Idempotency Identity + Canonical Payload Digest；相同 Identity/Digest 重放，Identity 相同但 Digest 不同则 Conflict。

C 只能在声明的 Capability Tier 提供 Final-request-boundary Evidence；H 负责传输，G 拥有 Applied Acceptance。MCP Tool Success、HTTP 2xx、H Transport ACK、E AcceptedReceipt 和 G Applied 是不同结果。本决议只决定 Family-level Routing；MCP Tool/Resource Name、Schema、H Operation ID/Registry、精确 Wire Field、ACK Schema、Transport 和 Consumer Acceptance 仍由 Issue #449 跟踪且 OPEN。

### 6.3 D/I

D 是 Canonical Identity/Lifecycle 和 D 签发 Forget Fence 的权威。I 是 Principal Trust、Authorization、PermissionEpoch 和 Global Forget Policy 的权威。BMCP 传递带签发者类型的不透明 Ref，并请求签发权威校验 Currentness。不得创建平行 Identity、Authorization、Epoch、Fence 或 Global Completion 机制。PermissionEpoch 和 ForgetFenceGeneration 属于不同命名空间。任一权威不可用或返回 Stale/Unknown/Incomparable 证据时，受保护 Memory 保持抑制并停止执行。

## 7. H 确认与 Owner 决议请求

H 所有事项先交 H 确认，不伪装成 Owner 决议。

### 7.1 H 确认请求

**H-CONFIRM-001 — Envelope / Request Identity**
- MODULE：BMCP / H
- ISSUE_OR_ADR：H message-envelope-and-versioning.md；protocol-overview.md
- DECISION_REQUIRED：BMCP 规范全称；message_id 是否就是 Request Identity 或需独立 request_id；精确 Response Correlation；Version/Type/Payload Schema/Idempotency 必填性；Operation Registry 和未知操作行为。
- CURRENT_FACTS：H Envelope 为 CANDIDATE；规范术语表已确定为 “Brain Memory Context Protocol”；初始派发中的 “Brain Memory Control Protocol” 已纠正为非规范写法。
- H_OWNED_CONTRACTS：Envelope、Versioning 和 Wire 字段名归 H。
- CROSS_MODULE_CONFLICT：C Request/Attempt ID、H Message ID、领域 Operation ID 不可互换。
- OPTIONS：保留当前全称和 message_id；或发布独立 Command ID 及显式映射。
- RECOMMENDED_OPTION：保留 H 现有权属；ID 保持区分；冻结前发布映射。
- MEMORY_COMPILER_IMPACT：E Receipt/Idempotency Identity 保持独立。
- AGENT_INTEGRATION_IMPACT：C Request/Attempt Mapping 必须明确。
- D_I_IMPACT：权威不变；Identity Claims 仍由 D/I 校验。
- RUNTIME_IMPLEMENTATION_IMPACT：Request/Response Correlation 等待 H 映射。
- REQUIRED_AUTHORITY：H，C/E/G 消费者复审。
- OWNER_DECISION：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN；INDEPENDENCE_UNVERIFIABLE；NOT_WIRE_FROZEN
- EVIDENCE：`00-governance/terminology.md` Blob b8770fbb58e4fac087698043c40a57531b1d244d；H Envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4。
- FOLLOW_UP_ACTIONS：H 发布版本化映射；消费者复审。

**H-CONFIRM-002 — Wire Decode / Parse 边界**
- MODULE：BMCP / H
- ISSUE_OR_ADR：H Envelope 和 Strict JSON Reference
- DECISION_REQUIRED：Transport Framing、Byte Decode、Canonicalization/Integrity 与 Decode 后 Protocol Parse 的精确拆分；重复 Key、无效 UTF-8/Unicode、深度/大小、Critical Extension 规则。
- CURRENT_FACTS：Strict Parser 是参考模型，不是生产 Transport；本文 Semantic Parse 仅接受解码认证 Envelope。
- H_OWNED_CONTRACTS：原始 Wire Decode 和 Envelope 结构校验。
- CROSS_MODULE_CONFLICT：H 字节解码/Transport 职责不得转入 BMCP 语义层。
- OPTIONS：H 管原始字节和 Envelope 校验；BMCP 管 Operation Resolution/Request Normalization。
- RECOMMENDED_OPTION：保留此拆分。
- MEMORY_COMPILER_IMPACT：E 只接收已解析类型化 Ingress Request。
- AGENT_INTEGRATION_IMPACT：Adapter/Gateway 使用 H Transport 边界。
- D_I_IMPACT：权威不变。
- RUNTIME_IMPLEMENTATION_IMPACT：原始字节不得进入 Semantic Parser。
- REQUIRED_AUTHORITY：H。
- OWNER_DECISION：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN；INDEPENDENCE_UNVERIFIABLE；NOT_WIRE_FROZEN
- EVIDENCE：Strict Parser Blob 3b9b3da645448c773c95a9dcd3c57c8c109bb2da。
- FOLLOW_UP_ACTIONS：H 发布阶段契约和测试向量。

**H-CONFIRM-003 — ACK Family / Retry**
- MODULE：BMCP / H
- ISSUE_OR_ADR：H Delivery/ACK 和 Forget ACK 契约
- DECISION_REQUIRED：ACK Family、精确 Evidence Boundary、持久化点、Correlation Tuple、重复/Replay 处理、Retry Horizon 和 Consumer。
- CURRENT_FACTS：H 区分 Delivery Lifecycle、Forget Action ACK、Applied；ACK 丢失在 Reconciliation 前为 Unknown。
- H_OWNED_CONTRACTS：ACK Wire/Transport 编码和重传行为。
- CROSS_MODULE_CONFLICT：通用 ACK 不得暗示执行、持久化提交、Applied 或 Forget 完成。
- OPTIONS：保留独立 ACK Family，每个只表示一个有限观察。
- RECOMMENDED_OPTION：保持分离并显式映射 Consumer。
- MEMORY_COMPILER_IMPACT：E AcceptedReceipt 与 Transport ACK 分离。
- AGENT_INTEGRATION_IMPACT：Adapter 只报告可观察边界。
- D_I_IMPACT：D/I 独立判断 Fence/Target 满足情况。
- RUNTIME_IMPLEMENTATION_IMPACT：ACK 实现等待 H 和消费者验收。
- REQUIRED_AUTHORITY：H；D/I/G/E 复审各自消费语义。
- OWNER_DECISION：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN；INDEPENDENCE_UNVERIFIABLE；NOT_WIRE_FROZEN
- EVIDENCE：H ACK Blob 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8。
- FOLLOW_UP_ACTIONS：H 发布 ACK-to-consumer 矩阵。

**H-CONFIRM-004 — Validator / Error Mapping**
- MODULE：BMCP / H
- ISSUE_OR_ADR：H Envelope 和 Conformance Matrix
- DECISION_REQUIRED：Validator 分层、规范 Error Enum、Response Schema、Retryability/脱敏；映射十二类语义错误，不能合并 Authentication/Authorization/Validation/Conflict/Unknown。
- CURRENT_FACTS：H Taxonomy 是候选；请求通用名称并非 H Code 全部现有值。
- H_OWNED_CONTRACTS：Wire/Protocol Validator 和 Error Serialization。
- CROSS_MODULE_CONFLICT：领域 Validator 和 I Authorization 必须保持 Owner 所有。
- OPTIONS：保留 H 具体 Code；仅在版本化映射无损时添加 Alias。
- RECOMMENDED_OPTION：保留具体分类并发布分层校验/映射。
- MEMORY_COMPILER_IMPACT：E Error 与 Protocol Error 分离。
- AGENT_INTEGRATION_IMPACT：C 映射 Agent-facing Error，不改变规范语义。
- D_I_IMPACT：D/I 决策仍具权威性。
- RUNTIME_IMPLEMENTATION_IMPACT：H 契约前 Error Mapping 阻塞。
- REQUIRED_AUTHORITY：H；领域 Owner 批准各自结果。
- OWNER_DECISION：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN；INDEPENDENCE_UNVERIFIABLE；NOT_WIRE_FROZEN
- EVIDENCE：H Envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4。
- FOLLOW_UP_ACTIONS：H 发布 Taxonomy 和测试向量。

### 7.1.1 H 逻辑确认处置——PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

**权威/身份说明：**由 Project Owner Delegate 汇总，并以 H 协议 Owner 角色依据 Issue #305 comment 7042461592 及 Owner 常设指示作出。本记录不是独立人工 H 签名；证据状态仍为 INDEPENDENCE_UNVERIFIABLE。

**H 精确来源快照：**分支 session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74。
- Protocol Overview Blob：b88ef3a6fd3be293e7c2e77d9652f386b169bc47
- Message Envelope / Versioning Blob：5547ecd78d118bd63e571e5daad87194d9b694e4
- Context Delivery / Acknowledgement Blob：bf9732cc39d156853b507c3a3a4e573159978f49
- Adapter Forget ACK / Target Binding Blob：5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8
- Strict JSON Parser Reference Blob：3b9b3da645448c773c95a9dcd3c57c8c109bb2da
- Phase 3.7 Lifecycle Handoff Blob：b2a2648d5576511f68fdb9d87ce4388a1fedd5e9
- Protocol Conformance Matrix Blob：075b2ac6ebe9bda4ec83de04fad07e8027e6a440

#### H-CONFIRM-001——Message / Request Identity：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

- message_id 是一条 BMCP Message 唯一且不可变的身份。
- correlation_id 将一个 Workflow / Turn / Delivery 关联起来；causation_id 标识直接父 Message / Event。
- 可改变状态或可重试的操作还必须具有 Owner 范围内的幂等身份及 Canonical Payload Digest。
- 当前 H 候选 Envelope 没有独立的核心 request_id。C 保留其所有的 AgentRequestId 和 AgentAttemptId。C 将一个 Agent Request 映射为一条或多条 BMCP Message，并通过 correlation / causation 表达关联，不得混淆 Agent Request、Agent Attempt、BMCP Message、Transport Attempt 或 Idempotency Identity。
- 本项仅接受逻辑身份区分；字段编码、命名空间语法和 Wire Schema 均未冻结。

#### H-CONFIRM-002——Raw Wire Decode 与 Semantic Parse：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

- H 负责经认证的 Transport Binding、Framing / Raw-byte Intake、严格 UTF-8/JSON Decode、重复 Key / 非有限数 / 深度 / 大小拒绝、Envelope 结构校验、Protocol Version / Capability 与 Integrity 检查。
- BMCP Semantic Parse 只能在 Decode 和 Envelope Validation 成功后开始；它解析已注册的 Family / Operation，并分派给相应 Domain Authority。
- Semantic Parse 不得重新解析 Raw Bytes 或绕过 H 的 Strict Decoder。H Decode 不得推断 B/D/E/F/G/I 业务语义。
- Strict Parser Blob 是非生产参考模型，不是 Runtime Parser，也不构成实现 PASS。

#### H-CONFIRM-003——ACK Family / Evidence / Retry：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

- Delivery Lifecycle 保持 Prepared / Delivered / Applied / Rejected / Expired / Superseded / Unknown。超时或缺少 Evidence 必须为 Unknown，不得推断成功。
- Delivered 仅证明 Transport Endpoint 收到消息。Applied 必须符合 G 所有的 Context / Application 语义，并具有所需的 C Inference-boundary Evidence；H 负责传输/验证 Evidence，但不能签发 G Applied。
- Forget ACK 与 Applied 分离。Adapter-local 的 SUPPRESSED、LOCAL_BUFFER_CLEARED、LOCAL_CACHE_PURGED、QUEUED_DELIVERY_CANCELLED、FAILED、UNKNOWN、UNSUPPORTED 只证明所声明的 Target / Region / Session / Capability 范围。只有 I 评估全局 Target 是否满足及 PolicyException。
- 已完成动作的 ACK Identity / Evidence Digest 保持稳定；重传复用该值，Transport Attempt Identity 可以变化。相同 Operation Key + 相同 Target Digest 为幂等；相同 Key + 不同 Digest 为冲突。Local Success 后缺少 ACK，在 Query / Reconciliation 前仍为 Unknown。
- ACK 不代表模型注意、理解、Provider 删除、物理擦除或全局 Forget 完成。

#### H-CONFIRM-004——Validator 分层 / Error Mapping：PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

1. Transport / Security Integration 对 Peer / Workload Principal 进行认证；Principal 和 Authorization Policy 归 I 所有。Payload Identity Fields 仅是声明。
2. H 校验 Raw Syntax、Envelope Requiredness / Unknown-critical 行为、Protocol Version / Capability、Integrity、Replay 和 Idempotency。
3. Domain Validator 仍由各自 Authority 所有：B 负责语义；D 负责 Canonical Identity / Lifecycle / ForgetFence；E 负责 Admission / Receipt；F 负责 Retrieval；G 负责 ContextVersion / Delivery / Applied；I 负责 Authorization / PermissionEpoch / Forget Policy。
4. C 所有 Final Inference-request Boundary Evidence；H 不得从 Transport ACK 推断 Applied。
5. Error Class 保留 Authentication、Authorization、Validation、Unsupported、Conflict、Expired、RateLimited / ResourceExhausted、Internal 和 Unknown。现有 Code Label 在 H 的独立版本化 Wire Contract 完成审查前仍是 Candidate；没有任何 Error Enum 被冻结。

**H-CONFIRM-001..004 当前状态：**均为 PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN，并保留 INDEPENDENCE_UNVERIFIABLE。PR #428 comments 7060351041 和 7060264372 中记录的逻辑决议仅在其明确范围内被接受；精确 Registry / Schema / Requiredness / Crypto / Persistence / Error / Consumer Artifacts 仍开放。不得标记 H 七份规范核心文件已完成，也不得声称存在独立 H 签名、跨 Owner Consumer Acceptance 或 H Implementation / Conformance 闭合。

### 7.1.2 H 范围澄清——逻辑决议与精确工件状态

H 范围澄清记录于 PR #428 comment 7060264372。四项确认均不得整体标记为关闭；当前每项状态统一为 `PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN`，并保留 `INDEPENDENCE_UNVERIFIABLE`：
- H-CONFIRM-001：逻辑 Message Identity、Workflow Correlation、Immediate Causation 和 Operation Idempotency 的区分已决定；Operation Family Registry、各 Family 字段必填性、精确 Request/Response Schema、Wire Name/Type 仍 OPEN。
- H-CONFIRM-002：RFC 8785 JCS 已选为逻辑 Canonicalization 基础；Signed-object Bytes、Digest Exclusion、Signature Suite、Key Lifecycle 和 I Crypto-profile Acceptance 仍 OPEN。
- H-CONFIRM-003：ACK Evidence 必须先持久记录再发送，并支持幂等重放；缺失 ACK 保持 UNKNOWN；物理持久化拓扑/Adapter 和 Storage Acceptance 仍 OPEN。
- H-CONFIRM-004：Fail-closed Validation Order 和不同逻辑 Error Class 已决定；精确 Enum 拼写、Wire Schema、Retry Profile 和 Owner-specific Mapping 仍 OPEN。

这些逻辑决议不冻结 Schema、Crypto Profile、Persistence Topology、Error Enum，也不证明 H 七份规范核心文件完成、跨 Owner Consumer Acceptance 或 Runtime/Conformance 闭合。

### 7.2 Owner 决议请求

**DECISION_REQUEST_ID: BMCP-DR-001**
- MODULE：BMCP
- ISSUE_OR_ADR：B-ADR-FACT-CLAIM-001（13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md）
- DECISION_REQUIRED：使 B-ADR-FACT-CLAIM-001 与 Owner 语义选择对齐，并完成消费者映射/验收；在此之前不得冻结 Canonical Schema 或 Wire 字段。
- CURRENT_FACTS：合并的 `OWNER-DECISION-FACT-CLAIM-001` 已选择 Option A（Fact 独立 Attestation、Claim 表示命题）及 I1（稳定 Claim Identity + 不可变 ClaimRevision），并取代 B ADR 作为当前语义决策请求。精确消费者实现映射、迁移/兼容和符合性仍为 Candidate，直至责任工件完成版本 Pin 和审查；没有任何 Wire 字段获批。
- H_OWNED_CONTRACTS：未来 Wire 字段/Schema Mapping 归 H 所有且未冻结；本语义选择不批准任何 Wire 字段。
- CROSS_MODULE_CONFLICT：语义方向已选择，但 E Candidate IR、D Identity/Lifecycle、I Authorization/Attestor Policy 和 H Payload Mapping 仍需精确消费者验收和来源 Pin，之后才能冻结共享 Schema。
- OPTIONS：(A) 保留已选 Option A + I1 语义方向，在 消费者契约验收 门禁完成前继续保持 Payload 字段不透明；(B) 只有通过后续替代 Owner 决策才重新打开语义选择。
- RECOMMENDED_OPTION：A；不得把语义选择当作 Schema 批准。
- MEMORY_COMPILER_IMPACT：E 保持 Candidate-neutral；不冻结规范 Fact/Claim 输出 Schema。
- AGENT_INTEGRATION_IMPACT：C 只携带不透明的已批准 Ref。
- D_I_IMPACT：D/I 语义不变；B 决议后审查消费者。
- RUNTIME_IMPLEMENTATION_IMPACT：决议前不能实现最终 Fact/Claim Payload/Schema/Migration。
- REQUIRED_AUTHORITY：Owner 语义选择记录于 PR #446 (merged)；Schema 冻结仍需 B/D/E/F/G/H/I 消费者映射和验收。
- OWNER_DECISION：SEMANTIC_DIRECTION_APPROVED_OPTION_A_I1；WIRE_SCHEMA_MAPPING_CANDIDATE
- EVIDENCE：`OWNER-DECISION-FACT-CLAIM-001` PR #446 (merged) @ `ad5ca81a32b413aef3f9b5bccd06030aabde8275`；B ADR Blob 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593。
- FOLLOW_UP_ACTIONS：B 更新 ADR 状态/来源 Pin；D/E/F/G/H/I 记录精确消费者映射和验收；补齐迁移/兼容计划及符合性场景；所有 §8 条件满足前 Payload 保持不透明。

**DECISION_REQUEST_ID: BMCP-DR-002**
- MODULE：BMCP
- ISSUE_OR_ADR：D Canonical Identity/Lifecycle 和 Forget Fence；I Authorization/PermissionEpoch 契约
- DECISION_REQUIRED：发布 BMCP 必须消费的精确可调用权威接口、类型化 Request/Receipt 和 Currentness 结果词汇；不要求变更权属/语义。
- CURRENT_FACTS：D 拥有规范身份/生命周期和 D Fence；I 拥有授权/PermissionEpoch；H Envelope 引用依赖这些契约。
- H_OWNED_CONTRACTS：D/I 发布后 H 映射为 Wire 字段。
- CROSS_MODULE_CONFLICT：权属明确；Mainline 指南未建立精确可调用跨边界接口和 Error Mapping。
- OPTIONS：(A) 发布版本化 D/I Service Contract + H Mapping；(B) 暂时保持引用不透明。
- RECOMMENDED_OPTION：当前选择 B；Runtime 进入前必须完成 A。
- MEMORY_COMPILER_IMPACT：E 消费 D/I 语义，不复制权威。
- AGENT_INTEGRATION_IMPACT：MCP/Adapter 不得绕过 D/I。
- D_I_IMPACT：不改变权威；仅请求精确接口发布和消费者审查。
- RUNTIME_IMPLEMENTATION_IMPACT：接口/Currentness 证据前受保护 Handler 阻塞。
- REQUIRED_AUTHORITY：D、I；之后 H 确认 Wire Mapping。
- OWNER_DECISION：DECIDED_AT_AUTHORITY_BOUNDARY；EXACT_CALLABLE_API_IDL_SCHEMA_DEFERRED_TO_D_I_VERSIONED_CONTRACTS；H/BMCP/C MUST NOT INVENT AUTHORITY API OR CURRENTNESS SEMANTICS
- EVIDENCE：D/I authority boundary is decided by PR #429 comments 7060243632 and 7060259541; D owns canonical identity/revision/currentness/lifecycle/ConflictSet/ForgetOperation/ForgetFence; I owns Principal/Actor and attestor authorization, PermissionEpoch, revocation, retention and global Forget policy/evaluation. Exact callable API/IDL/schema/crypto/storage/wire mapping remain OPEN. H Overview Blob b88ef3a6fd3be293e7c2e77d9652f386b169bc47；D Forget Blob c791895333ab6140f035f4f622d5dee9325d422d。
- FOLLOW_UP_ACTIONS：D/I 发布接口/向量；H 映射；BMCP 更新对照表。

**DECISION_REQUEST_ID: BMCP-DR-003**
- MODULE：BMCP
- ISSUE_OR_ADR：C Agent Integration Canonical Contract / Guide
- DECISION_REQUIRED：确认 Agent/MCP-to-BMCP Operation Mapping、Request/Attempt/Message Identity、认证 Principal 交接和 Final Inference Boundary。
- CURRENT_FACTS：C Owner 决议 PR #430 comment 7060351480 已决定 Family-level Routing。MCP 是 Agent Host ↔ C 北向接口；BMCP 是 C Agent Adapter ↔ Brain 经 H 的协议边界。逻辑 Family Matrix 和 Identity Mapping 已记录于 §6.2。Issue #449 comment 7060126722 提供绑定语义方向。
- H_OWNED_CONTRACTS：精确 Operation ID/Registry、版本化 Schema、Wire Field、ACK Encoding 和 Transport 归 H 所有；C 不得发明 H Field 或 Operation ID。
- CROSS_MODULE_CONFLICT：Family 方向已决定，但精确 H Operation Registry、Schema、C Tool/Resource Name 和 C/H Consumer Acceptance 仍由 Issue #449 跟踪且 OPEN。MCP Tool Success、BMCP Business Outcome、Transport ACK、E Receipt 和 G Applied 仍须区分。
- OPTIONS：(A) C-owned MCP Agent Adapter/Gateway 映射到已注册 H BMCP Family/Operation；(B) MCP 暴露平行 Canonical Brain API。
- RECOMMENDED_OPTION：A 已在 Family-routing 层面 DECIDED；拒绝 B。精确 C/H Operation Mapping 在 H 契约 Pin 和 Consumer Acceptance 前继续 OPEN。
- MEMORY_COMPILER_IMPACT：MCP Ingress 仍使用 E AcceptedReceipt 和 D Admission。
- AGENT_INTEGRATION_IMPACT：C 保留 AgentRequestId/AgentAttemptId/AgentTurnId/AgentSessionId；Workflow Correlation 映射到 H correlation_id，不新增 request_id；精确 C Tool/Resource 与 H Operation Binding 仍 OPEN。
- D_I_IMPACT：Canonical Identity/Lifecycle 和 Authorization 仍归 D/I。
- RUNTIME_IMPLEMENTATION_IMPACT：Gateway 等待 H Mapping 和 C 验收。
- REQUIRED_AUTHORITY：C + H；D/I 审查涉及权威身份的映射。
- OWNER_DECISION：PARTIALLY_DECIDED；MCP_IS_AGENT_HOST_TO_C_NORTHBOUND；BMCP_IS_C_ADAPTER_TO_BRAIN_VIA_H；FAMILY_DIRECTION_DECIDED_PER_PR_430_COMMENT_7060351480；EXACT_H_OPERATION_IDS_SCHEMAS_C_TOOL_RESOURCE_NAMES_AND_CONSUMER_ACCEPTANCE_OPEN_UNDER_ISSUE_449
- EVIDENCE：C Guide Blob c4e076887634a9e8e46df076efb0f4b70d816e0a；`07-agent-integration/agent-integration-overview.md` 与 `08-bmcp-protocol` 权属边界。
- FOLLOW_UP_ACTIONS：C 将 Family Matrix 和逻辑 Identity Mapping 对齐到其 Canonical Source/Mirrors；C/H 在 [Issue #449](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/449) 下发布并接受精确版本化 Operation Mapping；H 只审查 H-owned Wire/Transport 工件；不建平行 API。



### 7.3 已解决与仍开放的决策登记

| 项目 | 处置 | 精确边界 / 下一责任方 |
|---|---|---|
| BMCP 规范名称 | 已解决——Brain Memory Context Protocol | Main terminology Blob `b8770fbb58e4fac087698043c40a57531b1d244d`；“Brain Memory Control Protocol”不是规范名称 |
| Fact/Claim 语义 | 已解决——Option A + I1 | 已合并 Owner 决策 PR #446；Blob `d59756a8eb454480804c482ca03c68345ab5abf2` |
| Fact/Claim 字段/Wire Schema | CANDIDATE / NOT FROZEN | B/D/E/F/G/H/I 消费者工件须完成版本 Pin 和审查；未批准任何 Payload 字段 |
| H-CONFIRM-001..004 | PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN | 逻辑层选择按 PR #428 comments 7060351041 / 7060264372；INDEPENDENCE_UNVERIFIABLE；精确 Registry/Schema/Crypto/Persistence/Error/Consumer Artifact 仍 OPEN |
| BMCP-DR-002 | DECIDED_AT_AUTHORITY_BOUNDARY / CALLABLE_API_IDL_SCHEMA_DEFERRED | D/I 权威边界已决定；精确 Callable API/IDL/Schema/Crypto/Storage/Wire Mapping 仍由 D/I/H 发布并保持 OPEN |
| BMCP-DR-003 / MCP Mapping | PARTIALLY_DECIDED——Issue #449 | MCP 为 C 北向 Agent Adapter/Gateway；BMCP 为 C Adapter 经 H 到 Brain；Family Routing 已由 PR #430 comment 7060351480 决定；精确 C/H Operation Mapping 仍 OPEN |
| BMCP Runtime / AT-01..AT-20 | NOT AUTHORIZED / NOT RUN | Issue #7 实施绑定继续延期 |

**BMCP-DR-002 的 D/I 证据（权属证据，不是可调用 API 发布）：**
- D：`docs/en/03-memory-brain/forget-fence-and-completion-contract.md` Blob `c791895333ab6140f035f4f622d5dee9325d422d`；`forget-fence-operation-and-publication-gate.md` Blob `9c054932994bb078e2834df8bd66f73895aa04f5`；`memory-versioning.md` Blob `4efbd26db9586f6fcf1897f42ffba287d625b903`；`commit-cursor-semantics.md` Blob `2de7fe35229372ae5b06093e5e031c2c243fbd7c`。
- I：`docs/en/09-security-governance/security-governance-guide.md` Blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a`；中文镜像 Blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e`。
- 这些来源定义领域语义和操作名称，不是完整可调用 API/IDL，也没有冻结 Wire 表示。D 定义 RegisterProducerWork、InstallForgetFence、PublishDerivedIfFenceCurrent、CompleteProducerWork、ResolveProducerWork、ReconcileForgetBarrier 等操作。I 定义 PermissionEpoch、AuthorizationDecisionRef、撤销/Currentness 和证据接受语义；没有冻结的公共 authorize() Endpoint/Schema。
- 裁决：D 仍是 Canonical ForgetOperation/Fence 和 Producer-barrier 语义的唯一权威；I 仍是 Principal Authorization、PermissionEpoch、撤销和 Global Forget Policy 的唯一权威。BMCP 只携带 Owner 签发的不透明 Ref/Epoch，并在接口发布后调用对应权威的 Validation/Currentness 操作。PermissionEpoch 与 ForgetFence 是不同名义类型。缺失/过期/不可用/不确定证据必须 Fail-closed。

**C Mapping 边界：**PR #430 comment 7060351480 已决定 Family-level Routing；[Issue #449](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/449) 仍 OPEN，跟踪精确 H Operation ID/Schema、C Tool/Resource Name、C-H Consumer Acceptance。MCP 是 Agent Host ↔ C 北向接口；BMCP 是 C Adapter ↔ Brain 经 H 的协议边界。C 的 AgentRequestId 仅可作为本地 Workflow Correlation 输入，不得新增 H request_id；H 每条 Message 有独立 message_id，correlation_id/causation_id 分别表示 Workflow/直接父事件。Event Ingress/Telemetry/Forget/Admin 必须经过注册 H Operation 和 Owner Authorization；Context Snapshot/Delta/Delivery 为入站；Acknowledgement 仅是 Adapter Evidence，不是 MCP Success 或 G Applied。Recall/Search 归 F，当前不是 BMCP Family，不得发明 Search。

### 7.4 B/D/I Owner 决议（委托角色；不声称独立人工签名）

- **B——PR #429 comment 7060251435：**接受 Option A + I1。Claim 是可归属的命题线程；ClaimRevision 不可变；Fact 是独立受治理的 Attestation；FactRevision 绑定精确 ClaimRevisionRef(s)、Evidence / Provenance 及经授权的 Attestor / Method Context。B 拥有语义词汇；D 拥有 Canonical Identity；I 拥有 Authorization。
- **D——PR #429 comment 7060243632：**接受 Option A + I1 作为 Canonical Domain 输入。D 拥有 ClaimRef / ClaimRevisionRef 与 FactRef / FactRevisionRef 的分配、Revision Commit / Currentness、Lifecycle、Lineage、ConflictSet 和 ForgetOperation / ForgetFence。精确 Immutable-revision Transaction / Currentness、Schema、Migration / Compatibility、Consumer Acceptance 和 Conformance 仍 OPEN。
- **I——PR #429 comment 7060259541：**接受 Option A + I1 作为 Security-policy 输入。Fact 创建/修订属于受保护操作，要求认证的 Principal / Actor Binding、精确 Attestor Authorization，以及在最终 Authorization / Commit 时仍当前有效的 I-issued PermissionEpoch。缓存的 ALLOW / Session / Lease / ACK 不能复用为授权。I 拥有 Attestor Authorization、Revocation、Retention / Legal-hold / Backup 和 Global Forget Evaluation。精确 Policy Partitioning、Issuer / Registry Binding 和 Consumer Mapping 仍 OPEN。

**必需的来源对齐：**B 必须更新其 domain-model-overview 和 B-ADR 状态/来源 Pin；D 必须更新现有 memory-versioning / Forget 来源及镜像；I 必须更新现有 Principal / Actor Authorization 与 Forget 来源及镜像。当前来源中关于语义选择尚未决定/ADR-blocked 的陈述，就语义选择而言已过时；但 Schema / API / Implementation Gate 仍开放。

## 8. Runtime 验收计划——NOT RUN

每行都是未来 Runtime 要求。本工作未执行下列任何测试。设计文档/参考模型不等于 Runtime PASS。

### 8.1 现有符合性证据——范围受限，不代表完整协议 PASS

- Main `713774c381effbbe9e70693f88a7fa99a33a040d`：`python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v`——**30 passed，0 failed**，退出码 0。该结果只覆盖 Applied Delivery Evidence 符合性套件。
- PR #436（已于 `02f61194fd4e12993b4c83f7fac8382eee20f5d8` 合并），源 Head `1ffed9ed127df98b2f823a66ec80ea43d08cb9dc`：`python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/provider_outcome -p 'test_*.py' -v`——**运行 10 项；5 passed；5 skipped；0 failed**，退出码 0。跳过的 CPO-02/04/05/09/10 明确需要 Owner C 权威语义 Validator。该结果仅验证 Schema 结构，不验证 C 语义或密码学签名。
- PR #436 的双语协议索引和 provider_outcome 测试现已合入 Main。其索引仍将 RecoveryJoin 1.0.2 的 Schema/Validator/Test 标记为未交付；五个语义测试方法仍需等待 C 的权威 Validator。
- 这些结果不构成完整 BMCP 符合性。Main 现在包含 crates/bmcp-protocol，这是针对 APPLIED_DELIVERY_EVIDENCE_RECORDED 1.0.0 的有界 Rust 实现切片，并带有 P0 Conformance Suite。它不是完整 BMCP Family/Operation Stack、生产 Transport 或端到端 Runtime。历史路径 tests/protocol_test.rs 仍不存在；当前 P0 Suite 位于 crates/bmcp-protocol/tests/p0_conformance.rs。
- AT-01..AT-20 仍为 **PLANNED_NOT_RUN**。本架构阶段不声明生产 Runtime 集成或生产激活；当前 Rust Crate 只是有界协议实现切片。



| ID / 场景 | OWNER | PRECONDITION | EXPECTED_RESULT | TEST_METHOD | DEPENDENCY | ACCEPTANCE_STATUS |
|---|---|---|---|---|---|---|
| AT-01 合法请求解析 | H + BMCP | H 解码认证 Envelope；版本支持；Operation 注册 | 一个规范化 Request；Parse 无副作用 | Golden Envelope + Operation Schema | H Envelope/Registry | BLOCKED_BY_H_CONTRACT |
| AT-02 非法请求解析 | H | Envelope 格式错误 / 缺必填 | Execute 前拒绝；脱敏稳定 Error | 负向 Envelope Vector | H Validator | BLOCKED_BY_H_CONTRACT |
| AT-03 不支持版本 | H | 无共同主版本 | VERSION_UNSUPPORTED；不降级/分派 | Version Negotiation Matrix | H Version Contract | BLOCKED_BY_H_CONTRACT |
| AT-04 缺少参数 | H + 操作 Owner | 必需 Payload 字段缺失 | 校验拒绝；不调用 Service | 每操作负向 Schema Vector | H + Domain Schema | BLOCKED_BY_H_CONTRACT |
| AT-05 未知操作 | H | Family/Operation 未注册 | 副作用前拒绝 | Registry 负向/Fuzz | H Registry | BLOCKED_BY_H_CONTRACT |
| AT-06 未授权 | I + H | 认证 Principal 被当前 I Policy 拒绝 | Deny；不调用受保护服务；不泄露跨 Scope | Authorization 负向集成 | I API/Epoch + H Binding | BLOCKED_BY_OWNER_CONTRACT |
| AT-07 Request/Response 关联 | H | Request 有 message_id/correlation_id | Response Causation 引用 Request；保留 Correlation | 多消息 Round-trip | H Request Identity | BLOCKED_BY_H_CONTRACT |
| AT-08 执行成功 | 领域 Owner + BMCP | Parse/校验/授权通过；Owner 返回成功 Receipt | Response 含精确 Owner Result；ACK 独立 | Service Contract 集成 | E/D/G API | BLOCKED_BY_OWNER_CONTRACT |
| AT-09 执行失败 | 领域 Owner + H | Owner 返回确定失败 | 保留 Failure；不伪造成功 | 注入 Service Fault | Owner Error + H Mapping | BLOCKED_BY_H_CONTRACT |
| AT-10 超时 | Owner + H | 可能副作用前后 Timeout | Owner Reconciliation 前 UNKNOWN；同一 Key | 各边界 Crash/Timeout | Owner Lookup/Reconcile | BLOCKED_BY_OWNER_CONTRACT |
| AT-11 ACK Receipt | H | 对一个声明边界的有效 ACK | 只记录该边界；不推断执行/持久化 | ACK Schema/Consumer | H ACK | BLOCKED_BY_H_CONTRACT |
| AT-12 ACK 丢失 | H + Owner | 副作用可能完成；ACK/Response 丢失 | UNKNOWN；同身份 Reconcile；不盲目重复 | Network Fault + Journal Reconcile | H ACK + Owner Idempotency | BLOCKED_BY_H_CONTRACT |
| AT-13 重复 Request | Owner + H | 相同幂等身份和摘要 | 返回原结果；不重复副作用 | 并发 Duplicate/Replay | Owner Idempotency | BLOCKED_BY_OWNER_CONTRACT |
| AT-14 重复 ACK | H + Consumer | 相同 ACK ID/Digest，再相同 ID/不同 Digest | Replay 幂等；摘要改变 Conflict；不变更状态 | ACK Replay/Mutation Vector | H ACK + D/G/I Mapping | BLOCKED_BY_H_CONTRACT |
| AT-15 Validator 拒绝 | H + Owner | Envelope/Schema/Critical Extension 无效 | 在正确层拒绝；不进入后续阶段 | 分层负向套件 | H Validator + Domain Schema | BLOCKED_BY_H_CONTRACT |
| AT-16 Forget Fence 冲突 | D + I + H | D Fence 或 I Epoch Stale/Unknown | Fail-closed；不执行受保护 Apply/Commit；保留抑制 | 两种 Race 顺序 + 权威故障 | D/I Currentness API | BLOCKED_BY_OWNER_CONTRACT |
| AT-17 Canonical Identity 冲突 | D（Fact/Claim 另依赖 B ADR） | Payload Ref 与 D Identity 不匹配或 Fact/Claim 未决 | Reject/Quarantine；不签发/转换身份 | Forged/Mismatch Identity Vector | D API；B ADR | BLOCKED_BY_OWNER_CONTRACT |
| AT-18 序列化稳定性 | H | 精确 Schema/Profile/Version | 同语义对象产生获批 Canonical Bytes/Digest | 跨语言 Golden Vector | H Canonicalization/Signature | BLOCKED_BY_H_CONTRACT |
| AT-19 Unicode | H | 有效/无效 UTF-8、补充字符、规范化边界、重复 Key | 按 Profile 保留有效 Unicode；拒绝无效/歧义形式 | 跨语言 Unicode/畸形字节 | H Wire Decode/Canonicalization | BLOCKED_BY_H_CONTRACT |
| AT-20 Request/Response 一致性 | H + 领域 Owner | Request ID/Correlation/Operation/Idempotency 固定 | Response 关联精确 Request，只返回 Owner Result | 端到端 Trace 断言 | H Correlation + Owner Result | BLOCKED_BY_H_CONTRACT |

BLOCKED_BY_H_CONTRACT 表示缺少 H 所有的 Wire/Transport/ACK/Validator 决策或精确映射。BLOCKED_BY_OWNER_CONTRACT 表示缺少权威 Owner 领域契约/API 或 ADR 决议。Runtime 授权和精确 Build 可用前所有测试均为 NOT RUN；依赖标签不是测试结果。

## 9. Runtime 工程交接 / Issue #7 进入条件

保持绑定不变：IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE。

Issue #7 当前根据 Owner 阶段关闭裁决为 CLOSED / not_planned；正文保留延期和工程进入清单。本工作不编辑 Issue #7，也不宣布 Runtime 进入。

**以下条件全部满足才可进入：**
1. BMCP 语义契约获责任架构权威接受；未决语义明确列出。
2. H 冻结版本化 Wire、Transport、ACK、Validator 契约，包括 Error/Conformance Mapping。
3. H/C/E/D/I/G 按需接受跨模块 Request/Response/Receipt/ACK 映射。
4. Owner 已批准 Fact/Claim Option A + I1 语义；精确消费者映射仍为 Candidate，直至 D/I/Storage/H 契约完成版本 Pin 和审查；E Candidate IR 和 Receipt API 精确固定。
5. C 通过 Issue #449 发布、H 审查 Agent Integration / MCP-to-BMCP Mapping；MCP 不得替代协议。
6. D/I 发布 Identity/Lifecycle、Forget Fence、Authorization、PermissionEpoch Currentness 的精确可调用接口。
7. 指定 Canonical Runtime 仓库/分支（或授权新仓库）、责任工程 Owner/维护者、Build、CI、测试命令和产物来源。
8. 相关权威记录 Deployment Topology、持久化、队列、Recipient Adapter、Observability、Recovery 和 Operator 职责。
9. 完整验收套件在不可变 Runtime Commit 上执行并保留可复现原始证据；UNKNOWN/Recovery/Race 均 fail-closed。
10. 独立安全/领域审查和所需 Owner 验收完成。不隐含生产激活授权。

| 工作流 | 下一项工件 | 责任权威 | 进入状态 |
|---|---|---|---|
| H | 冻结 Envelope/Version、Wire Decode、ACK、Validator、Error/Conformance | H | BLOCKED_BY_H_CONTRACT |
| B / Governance | 将已批准 Owner 决策映射到精确消费者契约；Schema 仍为 Candidate | B + D/E/F/G/H/I | BLOCKED_BY_OWNER_CONTRACT |
| D | Canonical Identity/Lifecycle/Fence API 和 Receipt | D | BLOCKED_BY_OWNER_CONTRACT |
| I | Authorization/PermissionEpoch/Revocation API | I | BLOCKED_BY_OWNER_CONTRACT |
| E | Candidate IR、AcceptedReceipt、Service 边界 | E | BLOCKED_BY_OWNER_CONTRACT |
| C | Agent/MCP Adapter-to-BMCP Mapping | C + H | BLOCKED_BY_OWNER_CONTRACT |
| G | ContextVersion/Delivery/Applied/ACK Mapping | G + H | BLOCKED_BY_OWNER_CONTRACT |
| Engineering Leadership | Canonical Runtime Repo/Team/CI/Deployment 权限 | Engineering Leadership | DEFERRED_TO_ENGINEERING_PHASE |
| BMCP 架构集成 | Owner 回复后刷新来源 Pin | BMCP 架构负责人 | NOT STARTED |

## 10. 治理与验证

- 验证快照：精确 Base / merge-base `c58878fce24528a0842b4f8887c93ddbf465b566`；精确候选 Head 记录在 PR 交付报告中。PR Base Ref 为 `bmcp-validation-base-c588`，固定指向 `c58878fce24528a0842b4f8887c93ddbf465b566`。Owner 通过 GitHub Compare 核验：`c58878fce24528a0842b4f8887c93ddbf465b566` 是当时观察到的 live `main` `2998f6321b90888d65ac9d972a169f86482e08b` 的祖先，`ahead_by=16`、`behind_by=0`、`merge_base_commit=c58878f`。浅克隆本地 `git merge-base` 为空不能证明提交图无共同祖先。本轮不追逐 live main；受控基线固定为 C588。此前 `713774c` 批次仅作历史证据。
- §2 Main 来源登记已刷新到 2efcbd09；32 条 Main Blob Pin 均针对该精确 Commit 解析。H 来源分支仍为 session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74；八个 H Blob Pin 保持匹配。EN/ZH 来源登记 SHA 集合一致。
- 已纳入依赖核验的 Main 变更：#472 G ContextVersion/ChangeSet/CAS 文档和实现；`crates/memory-context/tests/e2e_negative_paths.rs`（SQLite Store→Context 负向路径覆盖）；规范 Claim/Fact Revision 类型；BMCP RecoveryJoin 1.0.2 Schema、索引、结构 Validator 和符合性 Fixture/Tests。RecoveryJoin Validator 的 Schema-only 成功状态为 `STRUCTURALLY_VALID`，Proof/Currentness 需注入 D 权威回调；缺少回调时结果为 `UNKNOWN`，不是 VALID。它不冻结 H Wire/Transport，也不替代 D 权威。G E2E 测试覆盖跨 Scope 拒绝、Candidate Lifecycle 拒绝、过期 Revision 拒绝、Budget 溢出和文件型 SQLite 重启；未覆盖 Forget/Tombstone 公共操作、H ACK 绑定或 C Final-request Applied 证据。
- BMCP-DR-002 仍仅在 D/I 权威边界层面 DECIDED。BMCP-DR-003 仍为 PARTIALLY_DECIDED；精确 C-H Operation Registry/Mapping 仍 OPEN。H-CONFIRM-001..004 仍为 PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN；保留 `INDEPENDENCE_UNVERIFIABLE`。AT-01..AT-20 仍为 **PLANNED_NOT_RUN**；Provider Outcome 的五项 C 语义跳过仍未解决。
- Issue #7 仍为 CLOSED / not_planned，正文保留 `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`。未冻结 Wire/Schema/API，未授权 Runtime、Transport 实施、部署、生产激活或修改 Issue #7。
- `git diff --check c58878fce24528a0842b4f8887c93ddbf465b566...HEAD`：PASS，退出码 0（最终 Commit 后重跑）。
- `python3 scripts/check_document_management.py --require-changed c58878fce24528a0842b4f8887c93ddbf465b566`：FAIL，退出码 1；两个基线 DM-06 错误位于 `08-bmcp-protocol/protocol-index.md` 和 `.zh-CN.md`（`Canonical` 缺少 `authority.canonical_scope_id`）。PR 未修改两个索引文件。报告清点：501 governed documents，18 classified / 483 unclassified。未进行范围外元数据修改。


**独立基线缺项——明确排除在 #453 之外：** Owner 独立核验 `08-bmcp-protocol/protocol-index.md`（Blob `a5b64941cdc783b385348de1b22e0eaace2c003d`）和 `08-bmcp-protocol/protocol-index.zh-CN.md`（Blob `2fe06d9424821eb96eb006dbb391914c1375afae`）。两个 Front Matter 均包含 `authority.canonical_status`、`authority.normative_status`、`authority.canonical_conflict_status`，但缺少 `authority.canonical_scope_id`（DM-06）。中文文件实际路径是仓库根目录下的 `08-bmcp-protocol/protocol-index.zh-CN.md`，不是 `docs/zh-CN/`。两个文件均不属于 #453 三个修改路径。Owner 原则上授权独立 H-owned 双语修复载体，但仓库开放 PR 数超过配额，暂不创建。不得猜测 Scope ID 或弱化 DM-06；这不是 #453 的修复范围。
- `python3 scripts/ci/audit_runner_admission.py`：PASS；审计 1 个 self-hosted job / 0 violations；退出码 0。
- `BASE_SHA=c58878fce24528a0842b4f8887c93ddbf465b566 HEAD_SHA=$(git rev-parse HEAD) PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py`：PASS；77 frozen / 0 new gaps / 21 exemptions；注册历史重新枚举：21 条注册源（18 条晚于创建、3 条精确历史 allowlist），0 个错误；退出码 0。三个变更 Markdown 路径位于 `NORMATIVE_ROOTS` 外，门禁明确未执行配对检查。门禁仍保留 same-commit registration-history 规则；旧的 21 条错误未在本快照重现。
- `python3 scripts/check_bilingual_docs_full.py --source-revision c58878fce24528a0842b4f8887c93ddbf465b566`：FAIL；467 个范围内 Markdown / 112 exempt / 81 violations；退出码 1。逐路径分类如下。

### c58878f 快照的 GOV-DOC-001 全树清点

精确命令 `python3 scripts/check_bilingual_docs_full.py --source-revision c58878fce24528a0842b4f8887c93ddbf465b566` 返回 **467 个范围内 Markdown / 112 个豁免 / 81 条 violations / 退出码 1**。这是路径对应关系清点，不是语义翻译审查。81 条按如下类别划分：

### GOV-DOC-001：81 条冻结快照逐路径分类

以下每个源文件均存在于冻结基线 `c58878fce24528a0842b4f8887c93ddbf465b566`，因此 81 条均为 Stage A 基线既有项。前 77 条属于 NORMATIVE_ROOTS 镜像缺项（预期的 `docs/en/<source>` 与 `docs/zh-CN/<source>` 两个路径均缺失）；最后 4 条属于 Phase-0 报告配对缺项（缺少 side-by-side `.en.md`/`.zh-CN.md` Pair 或所需的 `docs/en/14-ai-development` 镜像）。Owner 标签是按路径/领域作的路由分类，不构成新的 Canonical Owner 指派。全部排除在 #453 范围之外；处置为各 Owner 分别登记，不进行整体清扫。

| # | 精确源路径 | Owner / 路由 | 规则 | C588 基线 | 处置 |
|---:|---|---|---|---|---|
| 01 | `00-governance/architecture-document-management-policy.md` | Repository Governance（仓库治理） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 02 | `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` | Repository Governance（仓库治理） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 03 | `00-governance/templates/document-metadata-template.md` | Repository Governance（仓库治理） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 04 | `02-domain-model/phase-2-domain-extension.md` | B — Domain Model（领域模型） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 05 | `02-domain-model/phase-2-domain-extension.zh-CN.md` | B — Domain Model（领域模型） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 06 | `06-memory-context/context-architecture.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 07 | `06-memory-context/context-budget-and-sufficiency.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 08 | `06-memory-context/context-edit-operations.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 09 | `06-memory-context/context-implementation-coverage.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 10 | `06-memory-context/context-implementation-coverage.zh-CN.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 11 | `06-memory-context/context-manager.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 12 | `06-memory-context/context-reconciliation.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 13 | `06-memory-context/context-versioning.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 14 | `06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 15 | `06-memory-context/phase-3.8.4-g-c-provider-outcome-consumer-review.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 16 | `06-memory-context/phase-3.8.5-g-storage-logical-serialization-topology-impact-review.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 17 | `06-memory-context/phase-3.8.6-g-review-storage-serialization-anchor.md` | G — Memory Context（记忆上下文） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 18 | `07-agent-integration/adapter-capability-tiers.md` | C — Agent Integration（Agent 集成） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 19 | `07-agent-integration/adapter-capability-tiers.zh-CN.md` | C — Agent Integration（Agent 集成） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 20 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 21 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 22 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-owner-branch-snapshot-errata.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 23 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 24 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-entity-inventory.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 25 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-glossary.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 26 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-invariants.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 27 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-model.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 28 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-relationships.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 29 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 30 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-state-semantics.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 31 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-temporal-evidence-semantics.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 32 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 33 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-complexity-assessment.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 34 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-decision-record.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 35 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-semantics-conflict-register.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 36 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/evidence/README.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 37 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/evidence/official-reference-validation.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 38 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/existing-domain-model-baseline.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 39 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 40 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/latest-cross-owner-source-reconciliation.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 41 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/mature-domain-model-research.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 42 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/post-merge-currentness-and-governance-reconciliation.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 43 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/validation/README.md` | B — Domain Model research（领域模型研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 44 | `13-engineering-decisions/technology-architecture-blueprint.md` | Architecture / Engineering Leadership（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 45 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/README.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 46 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/architecture-complexity-audit.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 47 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/baseline/architecture-baseline.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 48 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/deployment-topology-comparison.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 49 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/independent-review-handoff.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 50 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/mature-project-research.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 51 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/open-questions.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 52 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-dependency-register.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 53 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/CGH-APPLIED-REVIEW-001.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 54 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 55 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-technology-review-synthesis.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 56 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/research-evidence-register.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 57 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/rust-ecosystem-assessment.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 58 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/technology-capability-matrix.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 59 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/technology-recommendation.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 60 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/workload-model.md` | Architecture / Technology research（本次扫描未解析具体 Owner） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 61 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/README.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 62 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-boundary.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 63 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-canonical-contract.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 64 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-conflict-register.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 65 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-cross-owner-contract-matrix.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 66 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-decision-record.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 67 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-failure-semantics.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 68 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-technology-assessment.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 69 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-telemetry.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 70 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-validation-plan.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 71 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/evidence/README.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 72 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/existing-integration-baseline.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 73 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/inference-boundary-and-trust-model.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 74 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/provider-integration-research.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 75 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/provider-outcome-and-execution-evidence.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 76 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/tool-execution-boundary.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 77 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/validation/README.md` | C — Agent Integration research（Agent 集成研究） | GOV-DOC-001 NORMATIVE_ROOTS：双语镜像均缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 78 | `14-ai-development/research/phase-0/SESSION-1-GITHUB-WORKFLOW-REPORT.md` | Engineering Governance / Phase-0 operations（工程治理 / Phase-0 运维） | GOV-DOC-001 Phase-0 报告：side-by-side Pair / docs/en 镜像缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 79 | `14-ai-development/research/phase-0/SESSION-2-PROMPT-RUN-PROVENANCE-REPORT.md` | Engineering Governance / Phase-0 operations（工程治理 / Phase-0 运维） | GOV-DOC-001 Phase-0 报告：side-by-side Pair / docs/en 镜像缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 80 | `14-ai-development/research/phase-0/SESSION-3-QUALITY-REVIEW-DEFECT-REPORT.md` | Engineering Governance / Phase-0 operations（工程治理 / Phase-0 运维） | GOV-DOC-001 Phase-0 报告：side-by-side Pair / docs/en 镜像缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |
| 81 | `14-ai-development/research/phase-0/SESSION-4-ADOPTION-ISOLATION-REPORT.md` | Engineering Governance / Phase-0 operations（工程治理 / Phase-0 运维） | GOV-DOC-001 Phase-0 报告：side-by-side Pair / docs/en 镜像缺失 | 基线既有 | 排除 #453；各 Owner 分别登记，不整体清扫 |

### 冻结快照的 embedded-bilingual 注册历史重新枚举

C588 快照的门禁注册表包含 21 条 embedded-bilingual 源记录：18 条注册提交晚于源文件创建提交；3 条属于显式列出的历史同提交例外，且创建提交 SHA 与 allowlist SHA 精确匹配。`check_embedded_registration_history()` 返回空错误列表。门禁输出的 `exemptions: 21` 统计的是已登记的 embedded-bilingual 源，不是 21 条违规。因此，`713774c` 历史批次报告的 21 条 same-commit 错误**未在 C588 重现**。历史规则未改变。

| # | 已注册源路径 | 源文件创建提交 | 注册提交 | C588 结果 |
|---:|---|---|---|---|
| 01 | `00-governance/bilingual-documentation-policy.md` | `cd1ab0fb346c770d779b1d8d24297f6811a1a74f` | `32a35f422ba6442d1f700cfb327f348c0740a7f2` | 注册晚于源文件创建 |
| 02 | `14-ai-development/ai-development-standard.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 03 | `00-governance/architecture-document-management-policy.md` | `0c73f639bf7392a5381d0cc0d9cafd53017bfe05` | `0c73f639bf7392a5381d0cc0d9cafd53017bfe05` | 历史同提交例外；allowlist SHA 精确匹配 |
| 04 | `00-governance/architecture-document-metadata.schema.yaml` | `0c73f639bf7392a5381d0cc0d9cafd53017bfe05` | `965a66b9a92cd4c2b20f4b6100721c779be7f784` | 注册晚于源文件创建 |
| 05 | `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md` | `04d35f90d6f1389ee17dc8fba1a32600bd7ac8ec` | `04d35f90d6f1389ee17dc8fba1a32600bd7ac8ec` | 历史同提交例外；allowlist SHA 精确匹配 |
| 06 | `00-governance/bilingual-governance-migration-register.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | 注册晚于源文件创建 |
| 07 | `00-governance/templates/bilingual-issue-template.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | 注册晚于源文件创建 |
| 08 | `00-governance/templates/bilingual-umbrella-requirement-template.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | 注册晚于源文件创建 |
| 09 | `00-governance/templates/bilingual-commit-message.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | 注册晚于源文件创建 |
| 10 | `00-governance/templates/repository-policy-inheritance.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | 注册晚于源文件创建 |
| 11 | `00-governance/templates/document-metadata-template.md` | `ae37a41900f1950a8d78d4be9e1f6a27b2edb1bb` | `b45430428c1e65cae36a9f7d63a11a78008a8f8a` | 注册晚于源文件创建 |
| 12 | `00-governance/reports/bilingual-baseline-remediation-report.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | 注册晚于源文件创建 |
| 13 | `00-governance/reports/f06-object-reconciliation.md` | `9990b645555aef83714ff92c97255110b1fa0960` | `9990b645555aef83714ff92c97255110b1fa0960` | 历史同提交例外；allowlist SHA 精确匹配 |
| 14 | `14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md` | `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 15 | `14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.md` | `1957faa6349613280576bfa5f2a3a7107f6cb719` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 16 | `14-ai-development/PR-GOVERNANCE-001.md` | `3754d049db840b049728afd814faac968bf10749` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 17 | `14-ai-development/prompt-and-evidence-template.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 18 | `14-ai-development/prompt-authoring-standard.md` | `6faa3b038c02bce27b3b4443d6f1be95cf5c5beb` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 19 | `14-ai-development/iteration-lifecycle.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 20 | `14-ai-development/owner-automation-operating-model.md` | `6faa3b038c02bce27b3b4443d6f1be95cf5c5beb` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |
| 21 | `14-ai-development/README.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | 注册晚于源文件创建 |

81 条镜像缺项与注册历史检查是两个独立维度。上面的 C588 重新枚举得到 21 条 embedded-bilingual 注册源，其中 18 条晚于源文件创建，3 条精确匹配历史 allowlist，历史检查错误为 0。未削弱或绕过任何历史规则。

- `python3 scripts/governance/bilingual/test_bilingual_scripts.py`：PASS，13/13；退出码 0。
- `python3 scripts/test_check_document_management.py`：PASS，214/214；退出码 0。测试运行中的负向 Fixture diagnostics 属于预期输出。
- `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v`：PASS，30/30；退出码 0。
- `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/provider_outcome -p 'test_*.py' -v`：10 run / 5 passed / 5 skipped / 0 failed；退出码 0。CPO-02/04/05/09/10 仍等待 Owner C 权威 Semantic Validator。
- `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p 'test_*.py' -v`：FAIL，31 run / 28 passed / 3 failed；退出码 1。失败项：重复 JSON Member 测试要求具体重复键错误详情，但 Validator 返回通用 `invalid JSON: ValueError`；Schema/Index 测试找不到 protocol-index 中精确 `message_type` 条目；合法完整消息 Fixture 有六个对象违反 non-empty 约束。这些是当前 Main RecoveryJoin 工件问题，本 PR 未修改相关文件。
- `python3 -m unittest discover -s 06-memory-context/reference-model -p 'test_g_applied_ledger.py' -v`：PASS，8/8；退出码 0。
- `cargo test --offline -p memory-context --test e2e_negative_paths`：未完成；编译因 `Disk quota exceeded` / LLVM 输出流 I/O 错误失败；退出码 101。不声称 Rust G E2E PASS。
- 独立语义/双语复审仍 PENDING。20 行 AT 矩阵仍仅在 ZH 逐项列出；EN 仅记录汇总 `PLANNED_NOT_RUN`。已披露此不对称，不表述为双语一致。
- 未修改 H 所有规范文件、G 实现、C/D/I 权威文件、治理门禁、Schema 或 Baseline Registry。PR 范围仍严格为三个文件。

## 11. 双语变更清单

| 文档 / 版本 | 英文路径 | 中文路径 | 来源版本 | 一致性 |
|---|---|---|---|---|
| BMCP-ARCH-001 / 0.2.2 | reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | main c58878fce24528a0842b4f8887c93ddbf465b566；H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | 作者准备双语 Pair；独立一致性审查 PENDING |

Coverage Register 仅将此登记为 Review/Handoff Pair，不改变 “BMCP Protocol detailed contracts (7 core specifications)” 条目；双语规范核心文档覆盖仍为 NOT STARTED。结构配对不等于语义双语一致性审查。

## 12. 最终状态

- ARCHITECTURE_DELIVERABLE_STATUS：**ARCHITECTURE_PARTIAL**
- PARSE_CONTRACT_STATUS：候选语义边界已说明；H Wire/Decode Mapping 待定
- EXECUTE_CONTRACT_STATUS：CANDIDATE；D/I 可调用接口和 C/H Mapping 待定；Fact/Claim 语义已批准
- RESPOND_CONTRACT_STATUS：CANDIDATE；H Response Envelope/Correlation Mapping 待定
- H_DEPENDENCY_STATUS：**PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN**；INDEPENDENCE_UNVERIFIABLE
- CROSS_MODULE_DEPENDENCIES：H、B、C、D、E、G、I
- OWNER_DECISIONS_REQUIRED：BMCP-DR-001 语义已批准 / Consumer-Schema Gate OPEN；BMCP-DR-002 Authority Boundary DECIDED / Callable API-IDL-Schema-Crypto-Storage-Wire Mapping OPEN；BMCP-DR-003 Family Routing PARTIALLY DECIDED / Exact C-H Mapping OPEN under Issue #449
- ISSUE_7_STATUS：IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE；GitHub CLOSED / not_planned；未改变
- RUNTIME_IMPLEMENTATION_STATUS：NOT AUTHORIZED / NOT STARTED
- PR / Commit：仅在 Push 和 PR 成功后填写；不授权 Merge

**下一步：** H 根据已接受的 H-CONFIRM-001..004 更新并版本化规范双语 Wire/Envelope/ACK/Validator 工件。B/D/E/F/G/H/I 完成精确消费者工件版本 Pin 与审查；D/I 发布精确权威接口；C 通过 Issue #449 发布 MCP-to-BMCP 映射。随后 BMCP 架构集成刷新精确 Pin。所有工程进入前置条件均有证据前，Runtime 继续延期。


## 13. Stage B 晋升候选快照——未验收

- 候选基线：`2efcbd09f4e6ba499e9d22be72fa04d5135a0de7`（准备时已核验与当前 `main` 完全一致）。
- 候选分支：`promotion/bmcp-arch-001-stage-b-ef7f7310`；该分支仅承载 BMCP 交接三文件，不是对受控验证分支的整体晋升。
- Stage A 历史：PR #453 仅合入 `bmcp-validation-base-c588`（C588），产生合并提交 `7c7801db396b92c57ad37020fe170f65f25e43ce`。它没有合入 `main`；Stage A 的三个文件 Blob 在 `main @ 2efcbd09f4e6ba499e9d22be72fa04d5135a0de7` 上不存在或不同。
- 范围：本文档、中文对应文档、docs/governance/translation-status.md。独立的 protocol-index DM-06 变更已存在于基线 2efcbd09，不属于本候选。21 条 registration 历史仍是独立验证维度，本候选不修改该历史。
- §2 Main 来源登记已刷新到 2efcbd09；这只是 Blob 锚点刷新，不替代对变更来源文件的语义影响审查。§10 Stage A 门禁证据仍为 C588 历史证据。验收前仍必须完成 exact-head 门禁和独立双语语义审查。
- Stage A 精确 Head `8c26cdce9f71adfaac9fdded1e308ee75f6223f0` 的 GitHub Actions 失败项：
  - Run `44900545305`，Job `GOV-DOC-001 structural checks`：FAILURE。
  - Run `44900545344`，Job `GOV-DOC-002 metadata checks`：FAILURE。
  - Run `44900360222`，Job `GOV-DOC-002 metadata checks`：FAILURE。
  - Run `44900344742`，Job `audit`（Runner Admission）：FAILURE。
  - Run `44900344727`，Job `GOV-DOC-001 structural checks`：FAILURE。
- GitHub 返回了失败 Job 摘要，但 Job steps 接口为空；下载每个 Job 日志均返回 `BlobNotFound`。因此可以归因到工作流/Job 检查面，但精确失败命令和行号**尚未核实**。不得用本地 PASS 推断 GitHub 失败原因。
- Stage A 本地实测仅作诊断背景：GOV-DOC-001 全树扫描发现 C588 基线既有 81 项（退出码 1）；GOV-DOC-002 报告两个 DM-06 缺少 `canonical_scope_id` 及 483 条未分类记录（退出码 1）；本地 Runner Admission 为 1 个 self-hosted Job / 0 violations（退出码 0）；RecoveryJoin 工件测试 28 通过 / 3 失败（退出码 1）。这些结果不能覆盖 GitHub 工作流失败。
- 不声明 current-main acceptance。由于 Owner 报告的 open-PR 名额受限，未创建 PR。本分支仅是范围受控的晋升候选；状态仍为 `NOT ACCEPTED / ARCHITECTURE_PARTIAL`，等待来源刷新、exact-head 门禁和独立语义审查。

### Stage B 基线对账与候选验证

- 基线 2efcbd09 上两个独立 protocol-index 文件现在均包含 authority.canonical_scope_id = protocol/bmcp-message-type-index：英文 Blob 309d70845495013fe679b6870b0ab299877c9b55；中文 Blob 3ffa15e255c585962b94515e8e6bcdf37f1dba75。C588 的 DM-06 缺字段发现属于历史状态，在 Stage B 基线上已不再复现。两个索引文件均未被本候选修改。
- 在 2efcbd09 上独立运行 embedded-bilingual registration-history 检查，枚举 21 条来源记录，错误列表为空。该项仍在本三文件候选之外。
- 在 2efcbd09 上运行 RecoveryJoin 1.0.2 符合性套件，共 31 项全部通过（退出码 0）。Stage A 的三个 RecoveryJoin 失败在上游变更后不再复现：重复成员错误保留专用诊断；Schema/Index 工件测试可按精确 message_type 单元格定位；空 Owner High-water Map 合法且有明确说明。
- Stage B Main 来源登记已在两份语言文档中刷新为 88bf4875 的 32 组精确路径/Blob Pin；EN/ZH Pin 集合一致，与 Git Tree Blob 全量比对得到 0 个错误。C588 至 88bf4875 期间有 9 个来源 Blob 发生变化：
  - docs/en/07-agent-integration/agent-integration-guide.md — 7952e808d7ad58267608f720617fd38effa32322
  - 07-agent-integration/agent-integration-overview.md — 0d66fb8383197d27dd04792b084b19d99bb81e93
  - 07-agent-integration/adapter-capability-tiers.md — 17ef7914387de02637c6055c833b384fddf680e6
  - 08-bmcp-protocol/protocol-index.md — 309d70845495013fe679b6870b0ab299877c9b55
  - 08-bmcp-protocol/protocol-index.zh-CN.md — 3ffa15e255c585962b94515e8e6bcdf37f1dba75
  - 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json — dca5a00fb8c96e5fad40005fdca5f7f58cf0e768
  - 08-bmcp-protocol/validators/recovery_join_validator.py — fcf2c73cad226e0f46ac68439a37a3a3f24a7c36
  - 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py — c028b4b797f170a43f38390bff9574bd1751acbb
  - crates/memory-context/tests/e2e_negative_paths.rs — 00af5aa978030af57a63d3698c34ca5c24ae018b
- 来源影响审查：当前 C Overview / Guide 已明确 Family-level C/H 路由及 Identity / Principal 边界，同时仍将精确 C-H Operation ID 和 Schema 标记为 OPEN。Adapter Tier 更新区分 DeliveryPayload 与 Brain-side ContextSnapshot。Agent Integration Rust Crate 是确定性参考模型，没有网络 Transport、Persistence、BMCP Negotiation 或生产 Telemetry。Memory Context Crate 仍是 private/staged 模型，止于 Persistence/Transport 之前。其负向 E2E 套件有 8 个测试函数（7 个 active、1 个 ignored），但 MemoryStore/MemoryStorage 没有公开 Forget/Tombstone 操作；预先标记 Forgotten 的生命周期测试不等于测试 Forget 转换。中间基线 ef7f7310 观察到的编译标记已由当前 Main 提交 2efcbd09（PR #493）删除；当前 Memory Context lib.rs Blob 为 6070c1cea116f8253e884f91bb7bc8cf8393c1c8。BMCP Index 增加 Scope Metadata；RecoveryJoin 变更允许真实空 Owner High-water Map，并保留重复成员诊断。这些变更均不授权完整 Runtime，也不冻结 Wire/API 契约。
- 候选精确 Head 的本地门禁结果见最终执行回报；本文档不嵌入会自我引用的 Commit SHA。git diff --check PASS（0）；GOV-DOC-002 增量 --require-changed PASS（0；507 governed / 27 classified / 480 unclassified，仅增量判定）；Runner Admission PASS（0；1 个 self-hosted Job / 0 violations）；变更双语门禁 PASS（0；77 frozen / 0 new gaps / 21 exemptions，仅结构检查，三个变更 Markdown 路径在 NORMATIVE_ROOTS 外，未执行配对检查）；GOV-DOC-001 全树扫描 FAIL（1；473 in-scope / 114 exempt / 81 项既有缺口）；双语脚本测试 PASS（13/13，0）；Document Management 测试 PASS（225/225，0）；RecoveryJoin 符合性 PASS（31/31，0）。
- 初步镜像自检：编号标题序列一致（各 31 项）；81 条逐路径分类的路径集合完全一致；两份注册历史表各有 21 行。此前中文稿缺失的两个章节（7.1.1 H 逻辑确认处置、7.4 B/D/I Owner 决议）现已补译并插入。这是本会话自检，不等同于独立语义复审。
- Main 从 f687346c 前移到 89d5e37d，包含两个提交：17cde205 增加十项 Memory Compiler 规范场景测试；89d5e37d（PR #488）增加有界 Rust APPLIED_DELIVERY_EVIDENCE_RECORDED 1.0.0 协议切片。随后 Main 从 89d5e37d 前移到 67074d2f，仅更新 14-ai-development/work-items/GAP-BASELINE-001.md（增加 87 行）。随后 Main 从 67074d2f 前移到 2efcbd09，三个提交影响七条路径：Adapter Tier 镜像、Agent Integration 参考模型、Memory Context 参考模型、G 负向 E2E 测试及其覆盖文档。候选已 Rebase 到 2efcbd09；两个受影响的来源 Pin 已在上表刷新。因有意保留 PR 名额，候选分支未触发 GitHub Actions。Exact-head GitHub CI 仍待运行；不得将本地门禁结果报告为远端 CI 成功。独立语义复审也仍待完成。候选状态保持 NOT ACCEPTED。

### 最新 Main 实现更新——PR #488、Agent Integration 与 Memory Context

- 提交 89d5e37d（保留在当前基线 2efcbd09 中）包含 PR #488：新增 Rust Crate crates/bmcp-protocol，仅实现单一消息类型 APPLIED_DELIVERY_EVIDENCE_RECORDED 1.0.0。它包含类型化 Evidence 结构、Strict JSON Parser、语义校验和 P0 Canonical Digest 逻辑。P0 集成测试将 Rust Digest 与 Python 参考 Validator 对照。这是真实但有界的实现切片，不是完整 BMCP 协议栈或生产 Runtime 集成。
- 89d5e37d 上实现工件的精确 Blob：crates/bmcp-protocol/Cargo.toml c7bdc7ae3123ab7407ba778b2e519da353d68f3b；crates/bmcp-protocol/src/lib.rs 64e805126e807e9d5dd6ac9677795e71740fb2bb；crates/bmcp-protocol/tests/p0_conformance.rs a315f90500207af2de2dfd875134320ec448e952；08-bmcp-protocol/validators/applied_delivery_evidence_validator.py 260aed537be67e06df220d4ba7dc0ae022a59555；08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py f1ea451ca1cace7ce2cc07eed0d2f4411085e2ee；Workspace Cargo.toml 98e47a1719e872f6d5c30fa5614f2551ccc17c09；crates/memory-compiler/src/lib.rs c764398646db912b9822e055fb9b914ad00b4557。
- 在精确 89d5e37d 源树上本地验证：CARGO_BUILD_JOBS=1 cargo test --offline -p bmcp-protocol 完成，42 个单元测试通过、4 个 P0 Conformance 测试通过、0 失败，Doc Tests 为 0（退出码 0）。这只验证有界 Crate，不证明 Transport、所有 BMCP Message Family、跨 Owner Consumer 或生产部署已完成。
- 同次 Main 前移中的另一个提交 17cde205 为 crates/memory-compiler/src/lib.rs 增加十项规范场景测试。该项不属于 BMCP 三文件候选；本工作未修改 Memory Compiler 代码，也未运行其测试套件。
- 这两个提交共改变七个实现/构建/测试路径，均不与候选三文件或 32 条 Main 来源登记 Pin 重叠。候选保留所有上游变更，不回退或复制这些代码。


### Main 增量 67074d2f 至 ef7f7310（中间源码快照）

- 当前 Main 变更路径：07-agent-integration/adapter-capability-tiers.md（Blob 17ef7914387de02637c6055c833b384fddf680e6）；07-agent-integration/adapter-capability-tiers.zh-CN.md（Blob f4cf88d60b7a99149c8af656104bad5c09cfb6fc）；crates/agent-integration/src/lib.rs（Blob 14362b93edd39684b1093a24368d3a32fcd960a6）；crates/memory-context/src/lib.rs（Blob 4fad76242c6426f594904d0f0c9f8871670aecc4）；crates/memory-context/tests/e2e_negative_paths.rs（Blob 00af5aa978030af57a63d3698c34ca5c24ae018b）；06-memory-context/context-implementation-coverage.md（Blob 51e01fdfa7b7e276145440f12c3b687cc7e2f4f0）及其中文镜像（Blob d511d447dee1638509c5f196bccc6788c1197ec5）。32 行 Main 来源登记已刷新其中两个受影响的 Pin。
- G 覆盖文档报告 68 个单元测试、5 个负向路径测试和 1 个 Store-to-Context 集成测试；当前 e2e_negative_paths.rs 文件实际包含 8 个测试函数。该数量不一致属于独立 G 文档对账项，本候选不修改。该套件明确说明公开 Forget/Tombstone 转换尚不可用；预先标记 Forgotten 的生命周期测试只验证已标记项目会被排除。
- 中间基线 ef7f7310 的编译失败已由 PR #493、提交 112f54ba（保留在当前 Main 2efcbd09 中）修复，该提交删除了泄漏的执行环境标记。当前源码 Blob 6070c1cea116f8253e884f91bb7bc8cf8393c1c8 正常结束。最新基线 `cargo test --offline -p memory-context` PASS：68 个单元测试、7 个 active 负向 E2E、1 个 ignored、1 个 Store-to-Context 测试；退出码 0。
- PR #488 的 BMCP Rust Crate 及其来源/测试 Blob 从 89d5e37d 到 2efcbd09 未发生变化。因此上文记录的 42 个单元测试 + 4 个 P0 测试结果覆盖当前基线中相同的 Crate 源码字节。

### Main 增量 ef7f7310 至 112f54ba

- PR #493、提交 112f54ba 相对 ef7f7310 仅修改 crates/memory-context/src/lib.rs：删除位于闭合大括号之后泄漏的工具环境行。当前 Blob 为 6070c1cea116f8253e884f91bb7bc8cf8393c1c8。这是上游 G Owner 修复，不属于本三文件候选。
- 该提交说明记录 68 个单元测试 + 7 个 active 负向 E2E 测试（1 个 ignored）+ 1 个 Store-to-Context 测试，以及 workspace 231 passed / 0 failed。本交接已独立重跑 `cargo test --offline -p memory-context`：68 unit / 7 active E2E / 1 ignored / 1 Store-to-Context，全部通过；退出码 0。


### 最新 Main 增量 112f54ba 至 2efcbd09

- Main 仅前移一个提交 2efcbd09，相对 112f54ba 只修改 14-ai-development/work-items/GAP-BASELINE-001.md（+99 行）。候选路径、32 条来源 Pin、BMCP Schema/Validator 和 Runtime 源码均未改变。当前候选以该最新 Main 提交为基线。
- 该 2efcbd09 工作项更正还记录了双语门禁的残余误接受：中文源文件配零字节 .zh-CN.md 仍会通过；两份文件各含一个 CJK 字符也会通过。记录给出的最小修复是要求 partner 文件本身含中文。本候选不修改该门禁缺陷；因此变更双语门禁 PASS 仅是结构证据，不能替代独立语义镜像复审。


### 最新基线 Stage B 验证

- GitHub 基线 `2efcbd09f4e6ba499e9d22be72fa04d5135a0de7`；远端候选分支仍严格限定为声明的三条路径。本地门禁运行于重建树；基线变更 Blob 与候选三文件 Blob 均已按 SHA 与 GitHub base/head 逐一核对，树内容字节一致。此处本地 synthetic commit ID 不是 GitHub commit ID。
- `git diff --check`：PASS（0）。`check_document_management.py --require-changed`：PASS（0），507 governed / 27 classified / 480 unclassified，仅为增量结论。Runner admission：PASS（0），1 个 self-hosted job / 0 violation。变更双语门禁：PASS（0），77 frozen / 0 new gaps / 21 exemptions；三条变更 Markdown 路径位于 NORMATIVE_ROOTS 外，未做配对检查。GOV-DOC-001 全量扫描：FAIL（1），473 in-scope / 114 exempt / 81 violations。
- 双语脚本测试：PASS 13/13（0）。Document Management 测试：PASS 225/225（0）。RecoveryJoin：PASS 31/31（0）。BMCP Rust：PASS 42 unit + 4 P0（0）。Agent Integration：PASS 8/8（0）。Memory Context：PASS 68 unit + 7 active negative E2E + 1 ignored + 1 store-to-context（0）。
- 注册历史：21 条来源记录，0 errors。来源镜像检查：每种语言 32 条 Main Pin、0 Blob mismatch；31 个编号标题一致；81 条分类路径集合一致；每种语言 21 行注册表。候选仍为 NOT ACCEPTED：GOV-DOC-001 仍有 81 条既有违规，当前 Main 已记录双语门禁残余误接受，独立语义复审待完成；为保留 PR 名额，没有运行 PR-triggered GitHub Actions。


### Main 增量 2efcbd09 至 1d0ecb97

- Main 前移九个提交，影响 16 条路径。32 条 Main Pin 中有三条来源发生变化，已在上表刷新：RecoveryJoin Schema Blob f951427a20c32930eb93ae955011ecb40c6b1667；RecoveryJoin schema-artifact 测试 Blob bc8709fda08cad9d00044205cf1eb1fb8f1a6ff4；Memory Context 负向 E2E Blob b5b854c5e586e7e8a4cc95f8855331d9f8c8c857。32 行 Main 登记仍完整；相对 C588 不同的九条来源路径总数仍为九。
- 其他 Main 变更包括中文 Adapter Capability Tier 镜像（Blob 6b409eaba0e1b9421a9b2bd2d164ef53b41131f7，共 294 行）及归档补充；GAP-06-FORGET-PATH-UNREACHABLE 中英文工作项；AID-2026-040 authority log；Memory Context Cargo 与 E2E 测试；Memory Compiler Cargo/源码；双语门禁脚本和新回归测试；precheck-delivery 脚本/测试；H Applied Delivery 工作流更新。精确 Blob 已在英文增量清单中列出。
- 当前双语谓词仍是 _has_any_chinese(source) OR _has_any_chinese(partner)。Main 的 GAP-BASELINE-001.md 重现两种残余误接受：中文源配零字节 .zh-CN.md partner，以及两份英文内容各含一个 CJK 字符的文件对。新增回归测试只拒绝两侧均无 CJK 的全英文文件对，未覆盖这两种残余情况。文档给出的最小修复是要求 _has_any_chinese(partner)。本候选不修改该门禁缺陷；变更路径 PASS 仅是结构证据。
- GAP-06-FORGET-PATH-UNREACHABLE 建议在共同的 MemoryStorage 读取边界执行持久 ForgetFence。当前 E2E 文件有九个测试函数：八个 active、一个 ignored。active 的 forget_fence_is_not_yet_enforced_by_memory_store_reads 证明记录 fence 后 MemoryStore 读取仍能返回 revision；ignored 的 forgotten_memory_is_excluded_from_context 因没有公开 Forget API 而不可达。这是独立 G-owned 工作项，不属于三文件候选。
- 当前 Main 的 docs/governance/translation-status.md Blob 为 d9098d1261a7da3a3bdcb9ec923643bf37cb361d，尚无 BMCP architecture review/handoff 行；两份 review 文件在 main 上均不存在。本候选新增两份 review 文件和一条 status 行，不重复晋升已存在的 review 内容。


### Stage A exact-head CI 失败归因补充

PR body 含 BILINGUAL-MANIFEST: COMPLETE。C588 上的三个工作流定义分别执行：
- Architecture document management gate：python3 scripts/test_check_document_management.py，随后 python3 scripts/check_document_management.py --require-changed "$PR_BASE"。
- Runner admission policy：python3 scripts/ci/audit_runner_admission.py。
- Bilingual documentation gate：传入 PR base/head/body 执行 python3 scripts/check_bilingual_docs.py。

精确 head 的五次 PR run 均为 FAILURE：runner 44900344742 / job 136834725880；document management 44900360222 / job 136834769371；bilingual 44900344727 / job 136834725761；bilingual rerun 44900545305 / job 136835321425；document-management rerun 44900545344 / job 136835321501。全部对应 head 8c26cdce9f71adfaac9fdded1e308ee75f6223f0、base C588。GitHub job steps 为空（steps=null），日志下载返回 404 BlobNotFound。

本地精确 head 复现：Document Management 自测 214/214 通过，但增量 GOV-DOC-002 返回两个 DM-06 错误：protocol-index.md 与 .zh-CN.md 缺少 authority.canonical_scope_id（退出码 1）；这是 document-management 失败的高概率原因，但日志不可用，不能确认具体失败 step。Runner admission 本地 1 job / 0 violation 通过，而 CI 失败，原因未知。Bilingual 工作流只执行 check_bilingual_docs.py（不执行独立全量扫描）；传入精确 PR body marker 后本地复现 77 frozen / 0 new gaps / 21 exemptions 通过，但 CI 失败，原因未知。81 项 GOV-DOC-001 全量扫描是独立本地清单，不是该工作流的命令。不得根据不可用日志推断 CI PASS 或宣称根因已确定。


### Main 增量 1d0ecb97 至 88bf4875

- Main 前移一个提交，影响七条路径。32 行 Main 来源登记中有一条 Blob 更新：08-bmcp-protocol/validators/recovery_join_validator.py 当前为 0080a722db7665fc3bd4ead756dfa50fa712b705。该路径此前已属于 C588 至当前的九条变化来源之一，因此不同来源路径总数仍为九。
- Agent Integration 在 crates/agent-integration/src/lib.rs（Blob 980ab9b765601d3f4a5bd19f364feb8d0e63161f）和 delivery_lifecycle.rs（Blob 6825b89fd29be99a9066e459f1a4285c9db5bd6a）新增 DeliveryState 状态机及 AppliedAttestation 要求：七种状态、九个 attestation 字段、新增 19 个测试；原有八个测试保留。它仍是确定性参考模型，不是生产 Transport/Persistence。
- Phase 2 新增 memory-domain Cargo.toml（Blob 6067566f77231c62bb1bfe0715ef33f3ff2e5d3b）和 phase2_acceptance.rs（Blob ce0ea872e91d52fce558e706e3c3b6c0d2ced491）：18 个验收测试，7 个通过、11 个因所需 Domain 类型/Registry 尚未实现而 ignored。不得把 ignored 测试解释为已验收。
- RecoveryJoin Validator Blob 0080a722 不再把重复成员诊断折叠为通用 invalid JSON。Main 提交说明报告 31 个 RecoveryJoin 测试通过。
- check_document_management.py Blob 85bd0d77599fdf880e3be243705243e3be33e2a9 将 .pytest_cache 与 __pycache__ 纳入结构例外。其全树门禁明确为 INCOMPLETE（退出码 2）：17 classified / 485 backlog；自测 224/224。该全树结果不同于候选的 --require-changed 增量结果，后者需单独重跑。
