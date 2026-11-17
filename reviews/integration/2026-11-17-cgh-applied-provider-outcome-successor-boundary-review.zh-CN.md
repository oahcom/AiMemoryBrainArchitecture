# C/G/H 后继版本边界审查——Applied ACK 与 Provider Outcome 1.2.15

- 日期：2026-11-17
- 审查模式：协调会话中的委托式 C/G/H 专家角色审查；**不是独立人类 Owner 签署**
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- PR 背景：PR #28 仍为 Draft/Open；本报告不授权合并或启用。
- 范围：当前 H Unified 1.2.15 精确 Schema 候选、C Schema 结构审查、G 当前消费方版本绑定、C Provider Submit Outcome 语义，以及它与 JF-10 Applied ACK Schema 家族的边界。

## 1. 重新读取的精确源版本

| 工件 | 分支 / 路径 | 精确 Blob SHA | 当前状态 |
|---|---|---|---|
| H Unified 1.2.15 Schema | `session-h-bmcp-protocol` / `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.15.schema.json` | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | 已读回精确候选 Schema |
| H 1.2.15 Mapping 补充 | H 分支 / `08-bmcp-protocol/phase-3.8.21-h-exact-schema-mapping-unified-1.2.15-gateway-attestation.md` | `2dc30f193d9c4f4bdc05ca4c137103687db28924` | 候选 Mapping 说明；已被下列后续代码/CI 证据更新 |
| H 1.2.15 C Validator | H 分支 / `08-bmcp-protocol/validators/provider_outcome_validator_1_2_15.py` | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | 本地 C 对象/Schema/语义 Validator；需要 Authority Callback |
| H 1.2.15 Gateway Validator | H 分支 / `08-bmcp-protocol/validators/gateway_attestation_validator.py` | `9cc426d4c26deb452f39daff34c1008dd535e969` | Gateway-Attested Ingress/Replay Validator；生产接口由 Callback 注入 |
| H 1.2.15 Gateway Tests | H 分支 / `08-bmcp-protocol/tests/conformance/provider_outcome/test_gateway_attestation_validator.py` | `9a5051b001a6e59d7b71e6dd175e84bb7d01d252` | 21 个确定性 Unit/Fixture 测试 |
| H Workflow（修正前） | H 分支 / `.github/workflows/h-provider-outcome-conformance.yml` | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | 仅有 1.2.14 Path Filter；已被替代 |
| H Workflow（已修正） | H 分支 / `.github/workflows/h-provider-outcome-conformance.yml` | `2ad679952ce5499a16c8fffa0a1543e26460e6eb` | 纳入 1.2.15 Schema、两个 Validator、Envelope Validator、测试路径和 Workflow |
| H 精确 CI（修正前） | Run `44078755981`，Commit `e3e4cab0aab2c68f9db98bd50bc387b1895c3773` | — | SUCCESS；共 91 个测试，其中包括 21 个 H 1.2.15 Gateway 测试 |
| H 精确 CI（修正后） | Run `44079842914`，Commit `0d36324457e39bd50ad56ae902d477c4ea765b61` | — | SUCCESS；共 91 个测试，其中包括 21 个 H 1.2.15 Gateway 测试；Callback Fixture 使用确定性 Test Double |
| C 1.2.15 Schema 审查 | C 分支 / `07-agent-integration/phase-3.8.26-c-exact-review-h-unified-1.2.15-gateway-attestation-schema.md` | `c5ff68814be49ec5e6e2c081004e7fa058d276fa` | 委托 C 角色接受 Schema Shape，但附带条件 |
| G Applied 源合同 | G 分支 / `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G 自有语义；持久化实现未验证 |
| G 精确 Full-Path 消费审查 | G 分支 / `06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | `1894860c76336f8739d354b72beed3992cffd17e` | 明确绑定 H 1.2.14 × CSubmitOutcome 1.0.1 |
| C 规范 Provider Submit Outcome | C 分支 / `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` | C 语义权威 |
| CSubmitOutcome 1.0.1 Schema | C 分支 / `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | 不可变 C 对象 Schema |
| H JF-10 Applied ACK Schema | H 分支 / `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` | `a8a945cc3623c2907003b93625e3c79742150944`；独立 Schema 家族 | JF-10 Bridge Applied ACK，不是 Provider Outcome |

本次读取时观察到的分支 HEAD：C `71047cdb51139ca4080ac67f451e38a48698859d`、G `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe`、H `e3e4cab0aab2c68f9db98bd50bc387b1895c3773`。

## 2. 版本边界：1.2.15 尚未成为 G 接受的消费版本

H 1.2.15 是 Unified Wire Family 的不可变后继候选（Wire Family 仍为 1.3.0）。其 Provider Outcome Branch 新增条件性 Origin Transport Receipt/Digest、原始 Ingress Bytes Digest、H Signing Profile 和 Sequence 证据。H 分支现在已有 `provider_outcome_validator_1_2_15.py`、`gateway_attestation_validator.py` 和 21 个 Gateway Attestation 测试。精确 H CI Run `44078755981` 在 Commit `e3e4cab0aab2c68f9db98bd50bc387b1895c3773` 上 SUCCESS，共 91 个测试，其中包括上述 21 个 1.2.15 Gateway 测试。这修正了此前 Mapping 说明发布时“尚无 Validator/CI 结论”的状态。

测试 Fixture 对 Protected Transport、H/C Signature/Profile/Key Status、Origin Receipt、Durable Ingress/Replay 和 Owner Authority 接口使用确定性 Callback Test Double。该运行构成有意义的本地候选验证，但不证明生产 Trust Root、真实 I Registry/Delegation、实时 Owner Ledger、已部署的 Durable Replay Storage、Provider Truth 或生产 Ingress。

H 分支已修正过时 Workflow：Revision 描述现在区分 1.2.14 Compatibility 与 1.2.15 Gateway-Attested Conformance；Path Filter 已纳入 1.2.15 Schema、两个 1.2.15 Validator、Envelope-Auth Validator、Conformance Tests 和 Workflow 文件。修正后的 Workflow 已读回，Blob 为 `2ad679952ce5499a16c8fffa0a1543e26460e6eb`；修正后精确 Run `44079842914` 在 Commit `0d36324457e39bd50ad56ae902d477c4ea765b61` 上 SUCCESS，共 91 个测试，其中包括 21 个 1.2.15 Gateway 测试。上述路径的 CI Trigger Wiring P1 已关闭。

C 的精确审查仅接受 1.2.15 的 **Schema Shape**，并附带 C 自有语义条件，且该审查早于当前 Validator/CI 证据。C 现在必须复审精确的 1.2.15 Validator/Test/CI Pin。例如，H 必须认证 Origin Receipt，将原始 Adapter 身份绑定到不可变 C 对象，验证 Raw-Byte Digest，独立验证 H 与 C 签名，执行 Wire/Object 重复字段精确相等，并保持 C 的 UNKNOWN/IN_DOUBT 非终态。

G 当前 Phase 3.8.18 Full-Path 审查仍绑定 H Unified 1.2.14 与 CSubmitOutcome 1.0.1。不能通过推定把该接受转移到 1.2.15。G 必须针对精确的 1.2.15 Schema、Validator、Fixture 和 CI 工件重新审查，才能接受该后继版本作为 G Applied 消费输入。

**结论：** H 1.2.15 = Schema 候选；C = 附条件接受 Schema Shape；G = 没有证据表明已接受 1.2.15 消费版本。三方 1.2.15 Full-Path 接受状态 = OPEN。

## 3. 不得混淆 Provider Outcome 与 Applied ACK

当前存在两种不同的消息/证据族：

1. **经 H Unified 承载的 C Provider Outcome**：CSubmitOutcome 1.0.1 是 C 所有的不可变语义对象。H 负责认证和验证 Transport/Envelope 及精确对象 Join。Provider Handoff Truth 仍由 C 独占。
2. **BMCP Applied ACK 1.1.0 JF-10 Bridge**：独立 Schema 家族，用于 JF-10 Bridge/Prepared-GID 和 Applied Boundary 证据。

第二类不是第一类的 Wire 表示。H 对 C Provider Outcome 成功签发 Gateway Attestation，本身不会创建 G Applied。反之，JF-10 Bridge Applied ACK 也不能证明 Provider Handoff、G Applied 持久化或 Global Forget Completion。每个 Consumer Contract 都必须明确消息族、Schema Artifact Revision、不可变对象引用和权威 Owner。

## 4. 幂等至少分为三个独立层次

### 4.1 C Provider Attempt 幂等

C 规范合同为一个逻辑 Provider Attempt 定义稳定的 ProviderIdempotencyKeyRef，并将其限定于 Provider/Account/Endpoint-Model 语义和不可变 RequestDigest。恢复不确定 Handoff 时必须复用同一 Key 和 RequestDigest；这是同一 Attempt 的协调查询，而不是新发送。UNKNOWN/IN_DOUBT 禁止 retry-as-new。不支持权威 Same-Key Lookup 的 Provider 不得承诺 Exactly-once。

### 4.2 H Envelope/Evidence Replay 与冲突处理

H 必须认证精确 C 对象，验证重复 Wire/Object 字段相等、Origin Receipt 与 Raw-Byte Integrity、Signing Sequence/Key-Status 关联，以及 Durable Replay/Currentness。1.2.15 Schema 只是增加承载字段，本身并未实现这些语义检查。在完成所需的未 Mock 正向/负向路径并读回精确 CI 前，不能称 H Schema 候选已符合 Validator 或生产冻结。

### 4.3 G Applied Commit 幂等

G 源合同规定：Applied 按精确 Request/Attempt/Evidence Identity 提交；相同 Identity + Digest 返回原处置；相同 Identity 但 Digest 改变则 Conflict/Quarantine；迟到证据不能回滚更新的 ContextVersion 或 Delivery Attempt。

但是，当前 G 源文件与 1.2.14 Consumer Review 尚未建立完整、精确绑定的 Durable Applied Persistence Key/Transaction Contract，尚未明确联合绑定：
- 稳定 H Evidence Identity（Digest 应作为内容比较，而不是未经说明地混入 Identity）；
- CSubmitOutcomeRef + 不可变 C Object Digest + 精确 Provider Attempt/Request 元组；
- 适用时的 COC Transaction / Participant / Reservation Identity；
- G ContextVersion + DeliveryAttempt + InferenceRequestId + FinalRequestBoundaryId；
- Durable G Applied Record Key、唯一性约束、事务边界、重复返回行为、内容变化冲突行为、崩溃恢复与 Restore/Replay 行为。

这是 **G 自有持久化合同缺口**，不应因此改变 C Provider Idempotency 语义。Provider Attempt Key、H Evidence/Replay Identity 与 G Applied Commit Key 必须是不同的强类型身份，并明确它们之间的 Crosswalk。

## 5. 必须完成的关闭工作

| 优先级 | Owner | 下一项必需工件/证明 | Gate |
|---|---|---|---|
| P1 | H | 取得 C 对 Validator/Test/CI Pin 的精确复审；在声明生产能力前以真实生产 Authority 集成证据替换 Callback Double | Workflow Path Wiring 已修正；H 1.2.15 仍为 Candidate；本地测试通过不等于生产符合性 |
| P1 | G | 发布 Applied Persistence/Idempotency 补充合同：定义 Durable Key、唯一性范围、C/H/COC 精确 Crosswalk、同 Digest 重放、不同 Digest 冲突、Supersession、Crash Recovery 和 Restore Fencing | 无实现证据前不得声明 G Persistence PASS |
| P1 | G + C + H | 精确 1.2.15 Consumer Matrix：各 Owner 接受同一不可变 Schema/Mapping/Validator/Fixture/CI 集；不得继承前序版本批准 | 精确决议完成前不得接受 1.2.15 Full-Path |
| P2 | C/H/G | 为 ProviderIdempotencyKeyRef、H Envelope/Evidence Identity、CSubmitOutcome Identity、G Applied Record Identity 保留不同强类型标识；仅定义必要的相等/关联边 | 禁止跨层身份合并 |
| P2 | D/I/Storage/COC | 继续独立权威证明及 Recovery/Restore 验收；H/G 不得自我声明这些权威 | 生产启用仍受阻 |

## 6. 审查结论

- 六阶段生命周期与权威分工：**语义一致**。
- C Provider Outcome 语义与同 Key 不确定状态恢复：**已规范；生产 Provider Truth/幂等未验证**。
- H Unified 1.2.15 Schema 与本地 Validator 路径：**候选；21 个 Gateway 测试已纳入 91-test H CI 并 SUCCESS；仍需 C 精确复审 Validator/CI；生产 Authority 接口未验证**。
- G 对 H Unified 1.2.15 的消费接受：**无证据**。
- G Applied Durable Persistence/Idempotency 实现：**未验证**。
- JF-10 Bridge Applied ACK 与 Provider Outcome 的区别：**必须显式保留**。
- 全局 C/G/H Applied 合同冻结：**NO**。
- 生产 Provider Egress/启用：**NOT AUTHORIZED**。
- PR #28：**Draft/Open；无合并授权**。

本报告仅记录协调会话中的委托式技术审查，不修改任何 Owner 决议，不把前序 Blob 的批准转移到新版本，也不声称独立人类 Owner 签署。
