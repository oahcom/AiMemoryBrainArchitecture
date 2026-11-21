# BMCP 协议消息类型索引

- 范围：`08-bmcp-protocol/`
- 基线：`1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- 目的：按文件是否存在登记消息类型工件，不为语义正确性背书。

## 消息类型

| 消息类型 | 定义出处 | Schema | Validator | 一致性测试 | 状态 |
|---|---|---|---|---|---|
| `APPLIED_DELIVERY_EVIDENCE_RECORDED` | Phase 3.8.25 加固补充；Phase 3.8.26 CSubmitOutcome 关联补充 | `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json`（1.0.0） | `validators/applied_delivery_evidence_validator.py` | `tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | **IMPLEMENTED** — schema、validator、测试文件均存在。测试执行证据：由外部验证方提供，见 PR 描述。 |
| `C_PROVIDER_OUTCOME_RECORDED` | C 所有的 CSubmitOutcome 1.0.1 来源 schema；Phase 3.8.26 引用 | C 所有外部 Schema Blob：`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`；BMCP 内无 schema | **BMCP 内缺失** | `tests/conformance/provider_outcome/test_provider_outcome.py` — 仅结构验证，不含 C 语义一致性 | **PARTIAL** — BMCP 本地 validator 和 C 语义一致性验证仍缺失。本 PR 新增测试仅验证 schema 结构，不是 C 语义 Validator。 |
| `RECOVERY_JOIN`（RecoveryJoin 1.0.2） | Phase 3.8 H-RJ-HW-01 契约引用 | `schemas/` 下**未交付** | **未交付** | **未交付** | **NOT DEFINED** — 存在契约引用，但 schema 未交付。 |

## 类型定义（非消息类型）

| 类型 | 定义出处 | 分类 |
|---|---|---|
| `ProducerRegistrationHighWater` | Phase 3.8 H-RJ-HW-01 §3 | 类型化高水位值；不是消息 envelope |
| `ForgetFenceGeneration` | Phase 3.8 H-RJ-HW-01 §5 | 类型化 Fence generation；不是消息 envelope |

## 证据边界声明

本索引只登记指定仓库基线中 schema、validator 和测试工件是否存在。它**不**判定这些工件的语义是否正确、完整、安全、可互操作或已获 Owner 接受。

- `IMPLEMENTED` 表示 schema、validator、一致性测试文件三者均存在；这本身不代表本 PR 中测试已通过，也不代表生产/runtime 行为已经实现。
- `PARTIAL` 明确标识缺失工件及所有权边界；外部 schema 不得被算作 BMCP 本地实现。
- `NOT DEFINED` 表示契约/文档中存在引用，但 BMCP schema 目录没有交付相应 schema 工件。
- 语义正确性由规范性契约及对应 Owner 裁定。CSubmitOutcome 的 Outcome 语义仍归 C 所有。
- 对于 `APPLIED_DELIVERY_EVIDENCE_RECORDED`，测试执行证据由外部验证方提供，并在 PR 描述中引用；本索引不声称 Owner H 在本地执行过测试。

## CSubmitOutcome 一致性边界

新增的 provider_outcome 测试仅对 CPO-01、CPO-03、CPO-06、CPO-07、CPO-08 执行 Draft 2020-12 JSON Schema 结构验证。CPO-02、CPO-04、CPO-05、CPO-09、CPO-10 因预期结果需要 C Owner 权威语义 Validator 而明确 skip。Fixture 签名占位值及未注册 Profile 不构成密码学验证证据。

CPO-08 被标记为 COC 半配对向量，但当前记录实际包含两个非 null 的 COC participant 引用。该 fixture 因另一个结构原因不符合 schema：HANDOFF_ACCEPTED 缺少 ProviderRequestRef 和 ProviderReceiptRef。测试会记录此差异，并通过内存变异单独验证 schema 会拒绝 COC 半配对；不会声称未修改的 CPO-08 fixture 本身展示了该 COC 缺陷。
