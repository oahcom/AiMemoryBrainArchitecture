# D-OWNER-DECISION-PARTICIPANT-ADMISSION-001 — 发布参与者准入签发方

**状态：** 已裁定（Owner 代理裁定；开发基线与当前仓库契约）  
**裁定者：** D Owner，在 D 所拥有的 Fence/Admission 权限边界内  
**裁定日期：** 2026-11-21  
**基线：** `7d1a00714aed6e32e7ea4a28f041e15f43cda376`  
**范围：** GAP-12 §5 第 4 步；`PublicationProof::publication_participant_admitted`  
**兼容性：** Phase 1 冻结契约不变；不修改 Rust、Schema、Public API 或 `DomainError`。

## 1. 决定

**D 为当前开发基线选择选项 A：在现有契约下，`publication_participant_admitted` 必须持续保持 `false`。** 原因是 §8 所称的 D 权威边界并不是 E 侧的 `AdmissionStore`，而当前不存在能够合法确立所需 COC quorum、Storage 签名和 I 终态证据的 D 侧签发方。该决定不禁止未来在外部签发方存在后，另行批准生产集成。

指定的权威边界是 `compiler-stage-contract.md` §8 明确命名的 **D authoritative Fence/Admission**。这只指定负责作出准入决定的权威边界；它并未指定 `AdmissionStore` 为该签发方，也没有创建本地开发基线替代实现。

在当前基线中，任何本地记录、调用方断言或开发信任锚都不能使该标志变为 `true`。生产 Adapter 必须继续报告 `false`。

## 2. §8 的 “D authoritative Fence/Admission” 是否指 AdmissionStore？

**不是。** §8 中的表述标识所需的 D 权威边界，而不是 E 侧 SQLite 实现 `crates/memory-compiler/src/admission.rs`。

基线证据：

1. `admission.rs` 开头明确将其描述为 **E 侧生命周期状态与本地 SQLite 准入账本**，并明确说明它“不声称自己是 D 权威 Producer Ledger”，也不是跨服务的 D/Storage 可见性事务。
2. `admission.rs:261-292` 的 Schema 只有五张表：`admission_meta`、`producer_registry`、`producer_work`、`dependency_edges` 和 `publication_receipts`。其中没有发布参与者注册表或记录。
3. `admission.rs:738` 的 `AdmissionStore::final_publication_gate` 被定义为本地 SQLite 串行化操作，而不是 D Service API。它检查 Producer Work 与依赖闭包，并持久化本地 Publication Receipt；它不会验证 COC quorum、Storage 签名或 I 终态决定。
4. `publication_authority.rs:104` 报告的值是 `publication_participant_admitted: false`。
5. `OWNER-DECISION-PUBLICATION-RECORD-001.md` 的 D7.1 明确撤回了在 E 层构建 D 侧发布参与者注册表的早期承诺；D7.2 将缺失的外部依赖分配给 COC、Storage 和 I。

这个区别具有实质意义：本地 Producer Registry 与 Publication Receipt，并不等于 D 签发的发布参与者准入。§8 的条目是一个权威要求，不是证明该权威已由 `AdmissionStore` 实现。

## 3. 如果答案为是：引用类型 / 记录 / 验证器

**不适用。** §2 的答案是否，因此本决定不会定义本地引用类型、追加式参与者表或本地验证器。在当前基线中定义这些内容会违反 D7.1，并把外部声明转换成本地签发的授权凭据。

所需证据链仍是 C 契约规定的内容：

- 针对精确 participant 与不可变 operation tuple 的 COC quorum 证据；
- 由 Storage 签名的 `PreparedParticipantReceipt`，并作为 `JF10_PREPARED_PARTICIPANT_REGISTERED` 持久注册；
- I 针对同一不可变 tuple 作出的权威终态决定。

**准入决定签发方**是 §8 命名的 D authoritative Fence/Admission 边界。COC、Storage 和 I 是所需的上游证据签发方；它们都不能替代 D 的准入决定。本地开发基线不指定任何替代签发方。

<!-- OPEN：仓库尚未识别已部署的 D Service Endpoint，也没有识别一个能够消费全部三类外部证据的具体 D 实现。本决定有意不虚构这样的实现。 -->

## 4. 如果答案为否：为什么该标志在此基线下必须为 false

C 契约在以下位置有明确要求：

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:137`：

> 在精确 participant 已具备 quorum-committed 的 `JF10_PREPARE_INTENT_REGISTERED`、Storage 签名的 `PreparedParticipantReceipt` 已作为 `JF10_PREPARED_PARTICIPANT_REGISTERED` 持久注册，并且 I Owner Final Gate 已针对同一不可变 tuple 产生权威终态决定之前，C MUST NOT 调用受保护的 Provider Side Effect。

GAP-13 记录了以下实测缺失：

| 所需元素 | 基线证据 |
|---|---|
| JF10 Rust 状态 | `grep -rn "JF10" --include="*.rs" crates/` → 0 |
| PreparedParticipantReceipt | 只有 Candidate Schema；该 Schema 明确没有选择密码学套件或密钥策略 |
| Validator | `protocol-index.md:55`：没有专用 Validator，也没有生产符合性声明 |
| C Conformance | C-CO-01..10 与 H-JF10-01..10 均为 SPECIFIED / NOT RUN |
| Storage 签名密钥策略 | 没有密钥托管、轮换或验证实现 |

本地 Registry 无法制造上述任何事实。诸如 `d-owner-proxy/dev-baseline-v1` 的开发基线签发方，会成为 COC、Storage 和 I 的替代签名者，而不只是 D 自身的开发实现。这会违反 C §2 的证据模型和 D7.1 的撤回决定。

因此，在此开发基线和当前契约内，该标志必须保持 **false**。只有在外部证据签发方和 D 的消费权威均已实现并验证后，才可以通过新的 Owner 决策重新考虑。这并不声称这些外部系统永远不能构建。

## 5. 与 D7.1 的关系

**本决定支持 D7.1；既不撤销，也不缩小 D7.1。**

D7.1 撤回了在 E 层/本地修复中构建 D 侧发布参与者注册表的承诺，因为该事实依赖 COC quorum、Storage 签名和 I 的终态决定。本决定补充 §8 的解释：

- `D authoritative Fence/Admission` 是指定的 D 权威边界。
- `AdmissionStore` 不是该边界；它明确是 E 侧本地账本。
- 未来的 D 实现可以消费这三类外部证据并签发权威准入决定，但当前未授权任何本地替代实现。
- D7.1 的外部依赖仍是前置条件。不会创建本地 Registry，也不会把证明标志改为 true。

早期表述中“在外部签发方存在之前保持 false”的含义仍然保留：外部签发方未来存在只是必要条件，不会自动产生授权。D 仍必须验证精确 tuple 并作出 D 所拥有的准入决定。

## 6. Phase 1 兼容性

这是一个仅涉及文档的决定。它不修改：

- `PublicationProof` 或其八个字段；
- Phase 1 冻结契约或 `dm2_14` 预期；
- 任何 Rust 源码、Schema、序列化、Public API 或 `DomainError` 变体；
- 任何可观察的发布处置。

**兼容性结论：** Phase 1 契约保持不变，因此本决定不会引入 Phase 1 不兼容。此决定会话通过 GitHub-only 工作流无法执行 `dm2_14`；因此其运行结果是 **NOT RUN**，不得声称为新的 PASS。在发布前，正常验证环境仍必须确认它在不变条件下通过。

## 7. 本决定不涉及的事项

以下内容仍为 **OUT-OF-SCOPE（dev-baseline）**，本决定不会批准或模拟：

- 生产密码学套件、规范化、签名验证、密钥托管、轮换、撤销或 HSM；
- COC quorum 算法、成员关系、持久共识、故障切换或运营部署；
- Storage 的生产签名配置与持久注册实现；
- I 的 Owner Final Terminal Decision 实现；
- 消费精确三方证据 tuple 的 D 生产 Adapter/API；
- 生产符合性、互操作性和端到端发布。

**生产替代路径：** COC 必须针对精确 participant/operation digest 暴露可验证的 quorum-committed intent；Storage 必须发布并运行签名/密钥策略，并持久注册已签名的 Prepared Participant Receipt；I 必须针对精确不可变 tuple 提供权威终态决定；随后 D 才能实现 §8 的 Fence/Admission 签发方，对三类引用进行验证。只有这些门槛通过后，未来的 D 决策才可以授权有记录支撑的 Validator，并允许生产 Adapter 从权威来源取得 `publication_participant_admitted = true`。缺失、过期、未签名、不匹配或不确定的证据必须继续 fail-closed，保持 false。

## 8. 关闭标准

1. `compiler-stage-contract.md` §8 继续将 D authoritative Fence/Admission 标识为所需权威；不得把 `AdmissionStore` 描述为该权威。
2. 本决定不得修改 `admission.rs`；该文件继续明确标识为 E 侧本地账本。
3. 不得引入本地 `publication_participants` 表、本地 participant 签发方或开发基线捷径。
4. 在未来经授权的集成存在之前，`publication_authority.rs` 必须继续报告 `publication_participant_admitted: false`。
5. C 契约的三项证据要求必须保持不变；不得把 GAP-13 的实测缺失描述成实现或符合性。
6. GAP-12 §5 第 4 步必须引用本决定。
7. Phase 1 冻结内容和 `dm2_14` 输入必须保持逐字节不变；发布前，正常验证环境必须记录 `dm2_14` 未改变且 PASS。
8. 任何未来将该值改为 true 的变更，都必须由新的 D 决策明确指定签发方、记录、验证器、证据绑定规则和生产验证；本文件本身不授权此类变更。
