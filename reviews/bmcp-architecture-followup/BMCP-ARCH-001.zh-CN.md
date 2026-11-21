# BMCP 架构完成——语义契约与工程交接

- 工作项：BMCP-ARCH-FOLLOWUP-001；文档：BMCP-ARCH-001；版本：0.2.2
- 状态：CANDIDATE / ARCHITECTURE_PARTIAL——不是已冻结协议规范
- Main 基线：c58878fce24528a0842b4f8887c93ddbf465b566
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

## 2. 精确来源登记

当前 Main 来源 Pin 来自 origin/main @ c58878fce24528a0842b4f8887c93ddbf465b566；历史决议/测试证据另按其原始 Commit 标注。H Pin 来自 session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74。

| 来源 | Ref | Blob SHA | 状态 / 用途 |
|---|---|---|---|
| docs/en/08-bmcp-protocol/bmcp-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 228d28671955c977f653bef5b537554e431f9137 | CANDIDATE 概览 / H 权属 |
| 08-bmcp-protocol/protocol-overview.md | H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | b88ef3a6fd3be293e7c2e77d9652f386b169bc47 | CANDIDATE |
| 08-bmcp-protocol/message-envelope-and-versioning.md | 同一 H ref | 5547ecd78d118bd63e571e5daad87194d9b694e4 | CANDIDATE；H 所有 |
| 08-bmcp-protocol/context-delivery-and-acknowledgement.md | 同一 H ref | bf9732cc39d156853b507c3a3a4e573159978f49 | CANDIDATE；G 语义 / H Wire |
| 08-bmcp-protocol/adapter-forget-ack-and-target-binding.md | 同一 H ref | 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8 | CANDIDATE；H Wire，D/I/G 权威 |
| 08-bmcp-protocol/phase-3.7-h-lifecycle-handoff-envelope-semantics-not-frozen.md | 同一 H ref | b2a2648d5576511f68fdb9d87ce4388a1fedd5e9 | NOT FROZEN |
| 08-bmcp-protocol/protocol-conformance-matrix.md | 同一 H ref | 075b2ac6ebe9bda4ec83de04fad07e8027e6a440 | CANDIDATE 测试；无 Runtime PASS |
| 08-bmcp-protocol/runtime_reference/strict_json_parser.py | 同一 H ref | 3b9b3da645448c773c95a9dcd3c57c8c109bb2da | 参考模型，不是生产 Transport |
| 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | H @ `3e8b33df18b9e6fc757ca84ff07a12faebc78e74` | 4b664e3bce465499bcdfd93796349a4ba7074002 | H 来源 Schema；文件名/$id 为 1.0.2，但 Envelope schema_version const 为 1.0.0 |
| docs/en/04-memory-compiler/README.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 5f50d470bf26d46dfffad48ad23059fc7a36c489 | E/D/I 权属 |
| 06-memory-context/README.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 684490d1c4e2c3aeb0236a9083abf9a144f2744c | G Context 子系统概览 |
| 06-memory-context/context-architecture.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 56fcc0ea112d423ef69a3f00e9d626bf4230ca0e | G Context 架构与权属 |
| 06-memory-context/context-versioning.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b | G ContextVersion / ChangeSet / CAS 语义 |
| 06-memory-context/context-reconciliation.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 87063aceebed1c30b7840045ada8e3f348732688 | G Reconciliation 语义 |
| 06-memory-context/context-manager.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | ecc0549137a1738c197d02d12d94a1eb971ed6b5 | G Context Manager 边界 |
| docs/en/04-memory-compiler/compiler-overview.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | c89a256afda105ceac3db75d743ab58d177ef586 | E 流水线 |
| docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | f2a4007f4b17e33de9bcd183c57ee504cfeef6cd | CANDIDATE E Receipt |
| docs/en/07-agent-integration/agent-integration-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | c4e076887634a9e8e46df076efb0f4b70d816e0a | C 所有 Agent 边界 |
| docs/en/03-memory-brain/forget-fence-and-completion-contract.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | c791895333ab6140f035f4f622d5dee9325d422d | D/I Forget 边界 |
| docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 9c054932994bb078e2834df8bd66f73895aa04f5 | D Lifecycle/Fence |
| 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593 | 历史 ADR；语义决策已被取代；消费者映射仍为 Candidate |
| 14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566`（批准来源 `c138654c942dc93b5a36eccb2ff0e41452156429`） | d59756a8eb454480804c482ca03c68345ab5abf2 | 当前来源 Pin；Owner 语义批准是历史证据（Option A + I1），不冻结 Schema |
| docs/en/03-memory-brain/memory-versioning.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 4efbd26db9586f6fcf1897f42ffba287d625b903 | D Revision / Consumer Freeze 边界 |
| docs/en/03-memory-brain/commit-cursor-semantics.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 2de7fe35229372ae5b06093e5e031c2c243fbd7c | D Cursor 语义 |
| docs/en/09-security-governance/security-governance-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 061c5847b3df879eeaf3c71e5eae0bfa162b276a | I Principal / Authorization / PermissionEpoch |
| docs/zh-CN/09-security-governance/security-governance-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 372d27c79dc79d09bcdb0f142c979efdba1c2b6e | I 双语对应文档 |
| 07-agent-integration/agent-integration-overview.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 073ff4ddf71fbcaf959107bb06ab724bfa48e63b | C 规范 Agent 边界 |
| 07-agent-integration/adapter-capability-tiers.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | ca422000ec98cca543fd96b59710346949f7d82e | C Capability Tiers |
| 07-agent-integration/inference-boundary-model.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | e2d5cb6abd9ec40da6e3680531de5944fc8b14df | C Inference Boundary |
| 07-agent-integration/telemetry-model.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0 | C Telemetry |
| 08-bmcp-protocol/protocol-index.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | a5b64941cdc783b385348de1b22e0eaace2c003d | Main BMCP 协议工件索引；RecoveryJoin 1.0.2 条目 |
| 08-bmcp-protocol/protocol-index.zh-CN.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 2fe06d9424821eb96eb006dbb391914c1375afae | BMCP 协议工件索引；RecoveryJoin 1.0.2 条目 |
| 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | bbac8742401249230c629e858d033a09cd8f3acb | RecoveryJoin 1.0.2 结构 JSON Schema；不构成 H Wire 冻结 |
| 08-bmcp-protocol/validators/recovery_join_validator.py | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | fe62c77e1db5ba28704267ac9dd80a2d396d1499 | 结构验证 + 注入式 D 权威回调；候选参考实现 |
| 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 7ae54e0f7777ea2f41b7870e331aa8f388338a6c | RecoveryJoin 1.0.2 类型绑定 / UNKNOWN 状态测试 |
| 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 3af71ec41cb3be968ebedd5d26a12291f1969b2e | RecoveryJoin Schema / 索引 / Fixture 测试 |
| crates/memory-context/tests/e2e_negative_paths.rs | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 8db9a6f573e3ce91136c2f2378ce50e902a0d079 | G 跨 Crate SQLite Store→Context 负向 E2E 测试 |
| crates/memory-store/src/lib.rs | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 6059b3f088922c87f49993a6cbd80c49a884a1c8 | G MemoryStore 实现源码 |
| crates/memory-domain/src/lib.rs | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | b96cb2f74c56ab8a28da7e3ceffcf4adcb1b98d4 | 规范 Claim/Fact Revision 领域类型 |
| 00-governance/terminology.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | b8770fbb58e4fac087698043c40a57531b1d244d | BMCP 规范名称 / 术语权威 |
| C Family Boundary 决策 | PR #430 comment 7060351480；Issue #449 comment 7060126722 | Owner-delegate 决议；不声称独立人工 C 签名 | Family 方向已决定；精确 H Operation Registry / C-H Mapping 仍 OPEN |
| H Confirmation 范围澄清 | PR #428 comment 7060351041；H Scope Correction comment 7060264372 | 仅接受 Owner-delegate 逻辑选择；INDEPENDENCE_UNVERIFIABLE | H-CONFIRM-001..004 各自均为 PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN |
| B domain-model-overview.md | B 分支 `session-b-domain-model-phase3 @ 840202a98cf40a0b3f194afb84bed4d5f3326658` | Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | B 接受 Option A + I1；来源对齐仍待完成 |
| D memory-versioning.md | D 分支 `session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424` | Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb` | D Identity/Revision/ConflictSet 边界；Schema/Currentness Gate 开放 |
| D forget-fence-and-completion-contract.md | 同一 D ref | Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` | D ForgetOperation/Fence 权威 |
| I principal-actor-and-authorization-contract.md | I 分支 `session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6` | Blob `03765efac4bb1153f303ce0030f9e277d602e81d` | I Principal/Actor/Attestor Authorization 边界 |
| I scope-and-revocation-policy.md | 同一 I ref | Blob `71df6aaf21bb1767cd9fe5c947581b871325e023` | I PermissionEpoch/Revocation |
| I global-forget-target-inventory-and-completion-evidence.md | 同一 I ref | Blob `9100061fa986fb6676656169de3fcf9fc1c72664` | I Retention/Global Forget Evaluation |
| PR #436 协议索引/provider_outcome 测试 | PR Head 1ffed9ed127df98b2f823a66ec80ea43d08cb9dc；Merge Commit 02f61194fd4e12993b4c83f7fac8382eee20f5d8 | 已合入 Main | 结构性 Provider Outcome 证据；5 passed / 5 semantic skips |

本次更新已从实时 `session-h-bmcp-protocol` 分支重新读取上述七个 H Blob Pin；它们在当前分支 HEAD `3e8b33df18b9e6fc757ca84ff07a12faebc78e74` 均解析为表中 Blob SHA。此处是有界来源登记，不代表所有 H 工件或消费者均已独立审查。

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

## 8. Runtime 验收计划——NOT RUN

每行都是未来 Runtime 要求。本工作未执行下列任何测试。设计文档/参考模型不等于 Runtime PASS。

### 8.1 现有符合性证据——范围受限，不代表完整协议 PASS

- Main `713774c381effbbe9e70693f88a7fa99a33a040d`：`python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v`——**30 passed，0 failed**，退出码 0。该结果只覆盖 Applied Delivery Evidence 符合性套件。
- PR #436（已于 `02f61194fd4e12993b4c83f7fac8382eee20f5d8` 合并），源 Head `1ffed9ed127df98b2f823a66ec80ea43d08cb9dc`：`python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/provider_outcome -p 'test_*.py' -v`——**运行 10 项；5 passed；5 skipped；0 failed**，退出码 0。跳过的 CPO-02/04/05/09/10 明确需要 Owner C 权威语义 Validator。该结果仅验证 Schema 结构，不验证 C 语义或密码学签名。
- PR #436 的双语协议索引和 provider_outcome 测试现已合入 Main。其索引仍将 RecoveryJoin 1.0.2 的 Schema/Validator/Test 标记为未交付；五个语义测试方法仍需等待 C 的权威 Validator。
- 这些结果不构成完整 BMCP 符合性。Strict JSON Parser 是参考模型，不是生产 Transport。当前不存在 `tests/protocol_test.rs` 和 `crates/bmcp`。
- AT-01..AT-20 仍为 **PLANNED_NOT_RUN**。本架构阶段不存在 Runtime 仓库/实施授权。



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

- 验证快照：精确 Base / merge-base `c58878fce24528a0842b4f8887c93ddbf465b566`；精确候选 Head 记录在 PR 交付报告中。PR Base Ref 为 `bmcp-validation-base-c588`，固定指向 `c58878fce24528a0842b4f8887c93ddbf465b566`。Live `main` 当时实测为 `be77ef7e64b9102a03a7c65a223798fa2003e88b`，且已与 Owner 指定的 `c58878f` 快照分叉，因此本批次不以它作为 Base。此处理保持三文件 Diff 可复现，避免混入分叉历史。此前 `713774c` 批次仅作历史证据。
- §2 Main 来源登记已从 `c58878fce24528a0842b4f8887c93ddbf465b566` 刷新；所有 Main Blob Pin 均针对该精确 Commit 解析。H 来源分支已重新读取：`session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74`；七个 H Blob Pin 已重新获取且匹配。EN/ZH 来源登记 SHA 集合一致。
- 已纳入依赖核验的 Main 变更：#472 G ContextVersion/ChangeSet/CAS 文档和实现；`crates/memory-context/tests/e2e_negative_paths.rs`（SQLite Store→Context 负向路径覆盖）；规范 Claim/Fact Revision 类型；BMCP RecoveryJoin 1.0.2 Schema、索引、结构 Validator 和符合性 Fixture/Tests。RecoveryJoin Validator 的 Schema-only 成功状态为 `STRUCTURALLY_VALID`，Proof/Currentness 需注入 D 权威回调；缺少回调时结果为 `UNKNOWN`，不是 VALID。它不冻结 H Wire/Transport，也不替代 D 权威。G E2E 测试覆盖跨 Scope 拒绝、Candidate Lifecycle 拒绝、过期 Revision 拒绝、Budget 溢出和文件型 SQLite 重启；未覆盖 Forget/Tombstone 公共操作、H ACK 绑定或 C Final-request Applied 证据。
- BMCP-DR-002 仍仅在 D/I 权威边界层面 DECIDED。BMCP-DR-003 仍为 PARTIALLY_DECIDED；精确 C-H Operation Registry/Mapping 仍 OPEN。H-CONFIRM-001..004 仍为 PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN；保留 `INDEPENDENCE_UNVERIFIABLE`。AT-01..AT-20 仍为 **PLANNED_NOT_RUN**；Provider Outcome 的五项 C 语义跳过仍未解决。
- Issue #7 仍为 CLOSED / not_planned，正文保留 `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`。未冻结 Wire/Schema/API，未授权 Runtime、Transport 实施、部署、生产激活或修改 Issue #7。
- `git diff --check origin/main...HEAD`：PASS，退出码 0（最终 Commit 后重跑）。
- `python3 scripts/check_document_management.py --require-changed origin/main`：FAIL，退出码 1；两个基线 DM-06 错误位于 `08-bmcp-protocol/protocol-index.md` 和 `.zh-CN.md`（`Canonical` 缺少 `authority.canonical_scope_id`）。PR 未修改两个索引文件。报告清点：501 governed documents，18 classified / 483 unclassified。未进行范围外元数据修改。
- `python3 scripts/ci/audit_runner_admission.py`：PASS；审计 1 个 self-hosted job / 0 violations；退出码 0。
- `BASE_SHA=$(git merge-base HEAD origin/main) HEAD_SHA=$(git rev-parse HEAD) PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py`：PASS；77 frozen / 0 new gaps / 21 exemptions；退出码 0。三个变更 Markdown 路径位于 `NORMATIVE_ROOTS` 外，门禁明确未执行配对检查。门禁仍保留 same-commit registration-history 规则；旧的 21 条错误未在本快照重现。
- `python3 scripts/check_bilingual_docs_full.py --source-revision c58878fce24528a0842b4f8887c93ddbf465b566`：FAIL；467 个范围内 Markdown / 112 exempt / 81 violations；退出码 1。逐路径分类如下。

### c58878f 快照的 GOV-DOC-001 全树清点

精确命令 `python3 scripts/check_bilingual_docs_full.py --source-revision c58878fce24528a0842b4f8887c93ddbf465b566` 返回 **467 个范围内 Markdown / 112 个豁免 / 81 条 violations / 退出码 1**。这是路径对应关系清点，不是语义翻译审查。81 条按如下类别划分：

- **77 个规范根目录源文件缺少两种语言镜像**（扫描器要求的对应路径为 `docs/en/<source>` 与 `docs/zh-CN/<source>` 两者）：
  - `00-governance/architecture-document-management-policy.md`
  - `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md`
  - `00-governance/templates/document-metadata-template.md`
  - `02-domain-model/phase-2-domain-extension.md`
  - `02-domain-model/phase-2-domain-extension.zh-CN.md`
  - `06-memory-context/context-architecture.md`
  - `06-memory-context/context-budget-and-sufficiency.md`
  - `06-memory-context/context-edit-operations.md`
  - `06-memory-context/context-implementation-coverage.md`
  - `06-memory-context/context-implementation-coverage.zh-CN.md`
  - `06-memory-context/context-manager.md`
  - `06-memory-context/context-reconciliation.md`
  - `06-memory-context/context-versioning.md`
  - `06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md`
  - `06-memory-context/phase-3.8.4-g-c-provider-outcome-consumer-review.md`
  - `06-memory-context/phase-3.8.5-g-storage-logical-serialization-topology-impact-review.md`
  - `06-memory-context/phase-3.8.6-g-review-storage-serialization-anchor.md`
  - `07-agent-integration/adapter-capability-tiers.md`
  - `07-agent-integration/adapter-capability-tiers.zh-CN.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-owner-branch-snapshot-errata.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-entity-inventory.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-glossary.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-invariants.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-model.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-relationships.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-state-semantics.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-temporal-evidence-semantics.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-complexity-assessment.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-decision-record.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-semantics-conflict-register.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/evidence/README.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/evidence/official-reference-validation.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/existing-domain-model-baseline.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/latest-cross-owner-source-reconciliation.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/mature-domain-model-research.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/post-merge-currentness-and-governance-reconciliation.md`
  - `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/validation/README.md`
  - `13-engineering-decisions/technology-architecture-blueprint.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/README.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/architecture-complexity-audit.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/baseline/architecture-baseline.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/deployment-topology-comparison.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/independent-review-handoff.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/mature-project-research.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/open-questions.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-dependency-register.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/CGH-APPLIED-REVIEW-001.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-technology-review-synthesis.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/research-evidence-register.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/rust-ecosystem-assessment.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/technology-capability-matrix.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/technology-recommendation.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-A/workload-model.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/README.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-boundary.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-canonical-contract.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-conflict-register.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-cross-owner-contract-matrix.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-decision-record.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-failure-semantics.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-technology-assessment.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-telemetry.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-validation-plan.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/evidence/README.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/existing-integration-baseline.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/inference-boundary-and-trust-model.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/provider-integration-research.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/provider-outcome-and-execution-evidence.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/tool-execution-boundary.md`
  - `13-engineering-decisions/technology-research/TECH-REALITY-001-C/validation/README.md`

- **4 个 Phase-0 运维研究报告缺少 side-by-side `.en.md`/`.zh-CN.md` Pair 或 `docs/en/14-ai-development` 镜像**：
  - `14-ai-development/research/phase-0/SESSION-1-GITHUB-WORKFLOW-REPORT.md`
  - `14-ai-development/research/phase-0/SESSION-2-PROMPT-RUN-PROVENANCE-REPORT.md`
  - `14-ai-development/research/phase-0/SESSION-3-QUALITY-REVIEW-DEFECT-REPORT.md`
  - `14-ai-development/research/phase-0/SESSION-4-ADOPTION-ISOLATION-REPORT.md`


这 81 条与 `713774c` 历史批次此前报告的 21 条 same-commit registration errors 是独立问题。在 `c58878f` 快照上，结构门禁仍保留“注册必须晚于文件创建”的历史检查，结果为 77 frozen / 0 new gaps / 21 exemptions，**没有 same-commit registration errors**。没有削弱或绕过历史校验。历史 21 条不是当前计数。

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
| BMCP-ARCH-001 / 0.2.2 | reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | main 713774c381effbbe9e70693f88a7fa99a33a040d；H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | 作者准备双语 Pair；独立一致性审查 PENDING |

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
