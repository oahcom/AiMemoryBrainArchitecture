# Session 4 — A：H Unified 1.2.15 Validator / CI / Trust 精确审查
# Session 4 — A: H Unified 1.2.15 Validator / CI / Trust Exact Review

- 审查日期：2026-11-18
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 审查模式：只读源码审查；本报告是 A 协调审查工件，不构成 H/C/I Owner 批准。
- Main 基线：`b3c666e67982cb3d3374e759cfb6552c7765aacb`（Tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`）
- H 分支 HEAD：`0d36324457e39bd50ad56ae902d477c4ea765b61`
- C 分支 HEAD：`71047cdb51139ca4080ac67f451e38a48698859d`
- I 分支 HEAD：`0d071bf1ee7cc71912398c6ae57e4496e08f44ab`
- Storage 分支 HEAD：`830a559bd2f4ec72608f5a51e1a0b43779f2b989`
- 总体裁决：**DEFERRED**
- H 1.2.15 证据状态：**本地 Validator + 精确 HEAD CI 通过；跨 Owner 精确复审不完整；生产 Trust / 签发 / Durable Replay 仍开放**
- 不冻结 Schema，不授权生产，不推进 Gate B/C。

## 1. 执行摘要

H 1.2.15 已经不再只是 Schema 候选。当前 H 分支包含 1.2.15 Schema、专用 Provider Outcome Validator、Gateway Attestation Receiver Validator、21 个 Gateway Attestation 测试方法，以及覆盖这些路径的 GitHub Actions Workflow。GitHub Actions 已在当前 H 分支精确 HEAD 上成功运行 Provider Outcome 工作流。

这证明了有边界的本地 L1/L2 Reference Evidence，但**不能**证明生产认证、生产签名者注册、H Gateway 签发顺序、Durable Replay 或真实 I/D/Storage Authority 集成。C 的 Schema Review 明确写明尚未审查 Validator/CI；后续 C Order Review 虽接受修正后的 Reference Contract 顺序，却没有 Pin/Review 当前 Validator Blob。I 后续 Order Review 绑定的是前序 Gateway Validator Blob，并非当前实现。

因此，不得将 1.2.15 Bundle 视为联合接受、冻结、生产就绪，也不得认为它已具备替代 Storage v3.3.2 中 H 1.2.14 的条件。

## 2. 精确工件与执行证据

| 工件 | 精确 Blob / SHA | 结论 |
|---|---|---|
| H Unified Schema 1.2.15 | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | 结构候选，未冻结 |
| H 1.2.15 C Mapping | `2dc30f193d9c4f4bdc05ca4c137103687db28924` | Mapping 候选 |
| H Local C Provider Outcome Validator | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | 明确不是 Secure Ingress；Authority Callback 注入 |
| H Gateway Attestation Validator | `9cc426d4c26deb452f39daff34c1008dd535e969` | Receiver/Reference Validator；Callback 是部署接缝 |
| H Gateway Attestation Tests | `9a5051b001a6e59d7b71e6dd175e84bb7d01d252` | 含正向与 Fail-Closed 测试 |
| H Provider Outcome Workflow | `2ad679952ce5499a16c8fffa0a1543e26460e6eb` | 覆盖 1.2.15 Schema、Validator 和 Conformance Test 路径 |
| H Gateway P0 Contract Candidate | `93b83ac35114d20d64579d919c0699886940f0fa` | 仅候选；Profile 未注册 |
| CSubmitOutcome 1.0.1 Schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C Object 结构源 |
| C Review 3.8.26 | `c5ff68814be49ec5e6e2c081004e7fa058d276fa` | 接受 Schema Shape 及 C 自有条件；未审 Validator/CI |
| C Order Review 3.8.27 | `3ca06dbfd7d59483e9604b7a68df924c719f60aa` | 将修正后的签发/接收/Replay 顺序接受为 Reference Contract |
| I Review 3.8.22 | `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` | 接受 Schema 作为 Trust-Carrier 候选；未注册 |
| I Order Review 3.8.23 | `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` | 接受 Reference Contract 顺序；生产 Trust/Replay 仍开放 |
| Storage v3.3.2 Manifest | `5c614375e10698e4931d83deb57d20321445e068` | 仍 Pin H 1.2.14，而非 1.2.15 |

当前 H HEAD 的精确 Workflow 证据：
- H Provider Outcome Conformance Run **44079842914**，Job **134027249681**，测试 Commit `0d36324457e39bd50ad56ae902d477c4ea765b61`：**SUCCESS**，Raw Log：**91 项测试，0 失败**。
- H Recovery Cutoff Conformance Run **44079842878**，Job **134027249428**，同一测试 Commit：**SUCCESS**，Raw Log：**288 项测试，22 项 Skip，0 失败**。
- Provider Outcome Run：https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44079842914
- Recovery Cutoff Run：https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44079842878

Provider Outcome Workflow 在整个 provider_outcome 测试目录执行 `python -m unittest discover`。91 项结果是当前 H 精确 HEAD 的真实执行证据，不是“测试文件存在”的推断。288 项运行属于相邻 H Recovery/Wire 证据，不等于 1.2.15 Gateway Trust 证明。

## 3. 技术发现

### H1215-F01 — 已证明精确 HEAD 本地符合性
**严重性：** Medium；对 Reference Candidate 状态非阻塞。  
当前 H HEAD 的两个 Workflow 均成功。Gateway 测试覆盖 Revision Pinning、Origin 字段必填、Owner Authority 限定、Digest/Raw-Bytes 不匹配、Signing Sequence 格式、Profile Registry 缺失返回 UNKNOWN、H Signature 失败时不得提交 Ingress、Origin 不匹配、C Signature 独立失败、C Signature 不可用时 UNKNOWN 且不得 Durable Commit、P0 变异、未知字段拒绝、Replay 授权检查以及 Durable State 不可用。

**证据上限：** 测试注入的是确定性 Callback。断言证明 Callback 编排与本地三态行为，不证明生产 Trust 或真实密码学 Key Verification。

### H1215-F02 — C/I 接受的是 Schema/Order 候选，不是当前可执行 Bundle
**严重性：** High；阻塞跨 Owner 闭环。  
C 3.8.26 接受 Schema Shape 及 C 自有条件，并明确写明尚未审查 Validator/CI。C 3.8.27 接受修正后的顺序：认证原始 C Adapter 并捕获 Raw Ingress；H 签名之前验证 C Object/Schema/Digest/Signature/Semantics；Receiver 独立验证 H Attestation 与 C Object；完成必需检查后才 Durable Replay/Acceptance。但它没有 Pin/Review 当前 Gateway Validator Blob `9cc426...` 或精确 CI Run。

I 3.8.22 仅将 Schema 接受为 Trust-Carrier 候选，并明确保留 Profile Registration、Issuer/Key Approval、Custody、Key Status、Revocation、Historical Verification 与 Anti-Rollback。I 3.8.23 接受顺序作为 Reference Contract，但绑定 Gateway Validator Blob `d16ca2e...`，而当前 H Validator 是 `9cc426...`。因此，不能将 I Review 表述为对当前 Validator 实现的精确复审。

### H1215-F03 — 缺少签发顺序证明
**严重性：** Critical；阻塞。  
当前 `validate_gateway_attested_provider_outcome` 是针对已签名 H Envelope 的 Receiver-side Validator。它先验证 H Attestation，然后才调用 C Provider Outcome Validator。这本身不构成 Receiver Validator 的缺陷；但它无法证明 C 要求的 **Issuer-side 顺序**：H 必须先验证 C Schema/Digest/Signature/Sequence/Provider Evidence/Semantics，之后才能创建或签署 H P0。当前 H Tree 中未发现精确 Issuer 实现、Signing Service Boundary 或 Issuance-order 测试证据。

关闭要求：H 必须提供精确 Issuer Path，或正式定义并证明 C Verification 先于 H Signing 的架构边界；测试必须证明 C Object 为 INVALID/UNKNOWN 时不能签发 H Signature。

### H1215-F04 — Production Trust 与 Replay 仍是 Callback 接缝
**严重性：** Critical；阻塞。  
Gateway Validator 的 Profile Registration、Key Status、H Signature、Integrity Evidence、Identity/Delegation、Origin Receipt、Durable Replay Commit、Replay Disclosure Authorization 均通过注入 Callback 提供。模块自身声明它只是 Reference Integration Implementation，不是生产密码学实现或已部署 Trust Service。C Validator 同样声明缺失 Authority Callback 返回 UNKNOWN，且不是 Production-ready Trust Implementation。

关闭证据至少包括：I 批准的不可变 Profile/Issuer/Signer Registry；Trust Root/Key Custody 与 Lifecycle；持久 H Signing Sequencer 和认证 Key-Status History；Origin Transport Verifier 与不可变 Raw-Byte Receipt；真实 H Signature 与 Integrity-Evidence Verification；支持 Crash Recovery 的 Durable Replay Reservation/Result；Replay 结果披露前重新检查当前 I Authorization/PermissionEpoch、Key Status、Audience/Scope 和 D Forget Fence。

### H1215-F05 — 跨审查 Pin 需要刷新
**严重性：** High；阻塞。  
I 3.8.23 Pin 了旧 Gateway Validator Blob `d16ca2e...`，不是当前 `9cc426...`。C 3.8.27 引用的 C 3.8.26 Review Blob 为 `78fd99...`，而当前 C 分支上的 C 3.8.26 文件 Blob 是 `c5ff688...`。C Schema Review 也明确没有审查 Validator/CI。这些是版本绑定缺口，不代表底层合同必然错误。

关闭要求：H 发布精确 Bundle Manifest，绑定 Schema、Mapping、P0、Issuer/Receiver Validator、全部 Fixture/Test、Workflow 与成功 Run/Job 证据；随后 C/I 对这些精确 Blob 和测试证据复审。任何 Blob 变更都必须重新审查。

### H1215-F06 — Storage Bundle 仍停留在 1.2.14
**严重性：** Critical（后继采用）；阻塞。  
Storage v3.3.2 Blob `5c614375...` 绑定的是 H Unified 1.2.14 Blob `09fcd1...`，不是 1.2.15。旧的 60-test CI 和旧 Review 不能转移为新 Schema/Validator 的证据。在 H/C/I 精确闭环之前，不得发布已被接受的 Storage Successor Manifest。

## 4. 必须关闭的条件

| ID | Owner | 必需关闭证据 | Gate |
|---|---|---|---|
| H1215-C01 | H | 精确 Issuer-side C-before-H-signing 实现或正式 Trust Boundary 规范；测试证明 C INVALID/UNKNOWN 时不能签发 H Signature | Gate A、B |
| H1215-C02 | H | 精确不可变 Bundle Manifest：Schema、Mapping、P0、Validator、Fixture、Test、Workflow、Run/Job SHA 与证据上限 | Gate A |
| H1215-C03 | C | 对当前 H Validator/Issuer Path 的精确复审：12 个条件字段、C 重复字段映射、独立 C Signature、C UNKNOWN/IN_DOUBT 非终态，以及精确 CI Run | Gate A、B |
| H1215-C04 | I | H Profile、Issuer/Authority/Subject/Delegation、Trust Root、Key Custody/Lifecycle、Sequence/Key-Status History、Revocation 优先级、Historical Verification、Anti-Rollback 的精确审查与正式注册决议 | Gate A、B、C |
| H1215-C05 | H + I | 真实 Origin Transport Receipt 与 Raw-Byte Verification；生产 H P0 Digest/Signature 和不可变 Integrity Record；不得仅有 Test Double 证据 | Gate B、C |
| H1215-C06 | H + I + Storage | Durable Replay Identity/Result Reservation、Crash Recovery、同一 Message 恢复、Ambiguous Commit 返回 UNKNOWN，以及 Replay Disclosure 前的 Current Authorization 和 D Forget Fence 检查 | Gate B、C |
| H1215-C07 | Storage + C + I + A | Successor Exact-Version Manifest 绑定 H 1.2.15 和精确 C/I Review；随后 D/Storage/A 对同一 Bundle 重新精确审查 | Gate A、B、C |

所有条件保持 OPEN。不虚构截止日期：只有规定证据发布并完成精确版本读回后才关闭。Delegated Role Review 不等于独立人类 Owner 签名。

## 5. 裁决与允许范围

**A 裁决：DEFERRED。** H 1.2.15 可以继续作为非生产 Reference Candidate，也可用于合成 Conformance Testing。它尚未联合接受、未冻结、未达到生产就绪，也未获生产 Ingress 授权。Storage v3.3.2 仍是当前 Pin 的 Manifest，继续绑定 1.2.14。

禁止：
- 声称 C/I 已完成生产 Trust Registration 或 Owner Approval；
- 将注入式测试 Callback 当作真实 Authority Service；
- 从 Receiver-side Verification Test 推断 Issuer-side Signing Order 正确；
- 将 1.2.14 CI/Review 证据转移到 1.2.15；
- 在 H/C/I 精确闭环前发布“已接受”的 Successor Manifest；
- 推进 Gate B/C、合并 PR、关闭 Issue 或授权生产。

下一步应由 H 发布精确 Bundle 并关闭 Issuer-side 缺口，然后 C 精确审查可执行实现/CI，I 精确审查 Trust/Registration，Storage 发布 Successor Manifest，最后 A 对同一精确 Bundle 复审。
