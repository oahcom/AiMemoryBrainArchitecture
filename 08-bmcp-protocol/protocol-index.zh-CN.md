# BMCP 协议消息类型索引

- 范围：`08-bmcp-protocol/`
- 基线：`1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- 目的：按文件是否存在登记消息类型工件，不为语义正确性背书。

## 消息类型

| 消息类型 | 定义出处 | Schema | Validator | 一致性测试 | 状态 |
|---|---|---|---|---|---|
| `APPLIED_DELIVERY_EVIDENCE_RECORDED` | Phase 3.8.25 加固补充；Phase 3.8.26 CSubmitOutcome 关联补充 | `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json`（1.0.0） | `validators/applied_delivery_evidence_validator.py` | `tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | **IMPLEMENTED** — schema、validator、测试文件均存在。测试执行证据：由外部验证方提供，见 PR 描述。 |
| `C_PROVIDER_OUTCOME_RECORDED` | C 所有的 CSubmitOutcome 1.0.1 来源 schema；Phase 3.8.26 引用 | C 所有外部 Schema Blob：`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`；BMCP 内无 schema | **BMCP 内缺失** | `tests/conformance/provider_outcome/test_provider_outcome.py` — 仅结构验证，不含 C 语义一致性 | **PARTIAL** — BMCP 本地 validator 和 C 语义一致性验证仍缺失。本 PR 新增测试仅验证 schema 结构，不是 C 语义 Validator。 |
| `RECOVERY_JOIN`（RecoveryJoin 1.0.2） | Phase 3.8 H-RJ-HW-01 §§5–7 | `schemas/bmcp.recovery-join-1.0.2.schema.json` | `validators/recovery_join_validator.py` — 结构验证及 D 本地绑定 helper；D 权威能力通过回调注入 | `tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` | **IMPLEMENTED（工件存在性）** — 三个文件均已存在。这不表示 D 已采纳 proof 格式、生产一致性已成立或权威 currentness 已验证；缺少 D callbacks 时结果保持 `UNKNOWN`。 |

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

provider_outcome 测试套件只针对固定的 C 所有 Draft 2020-12 schema 和确定性结构进行检查；它不是 C 的语义 Validator。CPO-02、CPO-04、CPO-05、CPO-09、CPO-10 仍然 skip，等待以下 C 所有输入。

| 向量 | 向量断言 | C 必须提供的权威输入 |
|---|---|---|
| CPO-02 — rejected but ambiguous | `HANDOFF_REJECTED` + `POSSIBLE_OR_UNKNOWN` 是有效观测，但不是终局的无副作用结论 | 版本化 Outcome/Disposition 表，定义拒绝但仍有歧义的语义、终局性、重试/协调策略以及关闭不确定性所需证据；Validator 必须区分“观测有效”与“终局” |
| CPO-04 — unknown | `UNKNOWN` 表示 Provider Outcome 未确定，不代表没有副作用 | 规范化 UNKNOWN 原因分类及状态迁移/关闭规则；权威证明来源；返回 `VALID`/`INVALID`/`UNKNOWN` 三态且不得把证据不可用转成成功的验证器 |
| CPO-05 — in doubt | `IN_DOUBT` 不得与 `UNKNOWN` 混为一谈 | 独立的 IN_DOUBT 状态定义、协调迁移、终局性规则及解决所需证据；证明其与 CPO-04 区别的 Validator 测试 |
| CPO-09 — high-water exceeded | `COwnerLocalSequence > COwnerHighWater` 无效 | C 权威 Ledger/High-Water 证明，包含 Ledger 身份、sequence namespace、root/version、签名和当前性；将记录序号绑定到该权威 cutoff 的验证器 |
| CPO-10 — request digest conflict | C 记录的 `RequestDigest` 与实际最终请求边界的 digest 冲突 | C 的规范化/digest profile、权威最终边界字节或不可变边界证明，以及重新计算/绑定 wire digest 的验证器。Fixture 的 `wire_request_digest` 是向量上下文，不是 CSubmitOutcome schema 属性 |

针对上述五个向量，Owner C 必须发布版本化规范 Outcome/验证契约、等价于 `validate_c_submit_outcome(record, context) -> VALID | INVALID | UNKNOWN` 的权威可调用接口、该函数使用的证据/证明格式及 trust/key/ledger 验证接口，以及带预期结果的原始正反向 fixtures。只有函数桩而没有权威契约和证据输入是不够的。

不依赖 C 的 BMCP 本地 Validator 可以检查：
- Draft 2020-12 schema 有效性、必填字段、类型、枚举、未知成员和 schema 中依赖 Outcome 的结构规则；
- COC participant intent/reservation 配对；
- 重复 JSON member 拒绝，以及同一输入对象中确实同时存在的字段之间的确定性相等关系；
- 引用/digest 的结构，以及测试 fixture 是否明确标注为未注册或仅含密码学占位值。

没有 C 权威能力时，BMCP 无法确立 issuer/profile/key 的真实性、C Ledger inclusion 或当前 High-Water、gate linearization、Provider evidence 真实性、实际 Provider side-effect truth、COC transaction join，或 `RequestDigest` 与最终 Provider 请求边界实际字节之间的绑定。这些检查必须委托给 C 所有的 Validator；权威能力或证据不可用时必须保持 `UNKNOWN`。

CPO-08 fixture 决策：**选项 1 — 修正有效基线，并单独保留无效向量。** `CPO-08-valid-baseline` 现在包含 HANDOFF_ACCEPTED 所需的两个 Provider 引用以及完整 COC 配对。`CPO-08-coc-half-pair` 是独立负向量，保留相同 Provider 引用，只将 COC reservation 设为 null，因此拒绝结果隔离地验证预期 COC 半配对规则。测试不再依赖无关的 Provider 引用缺失缺陷。

## RecoveryJoin 1.0.2 一致性边界

以下三个 BMCP 工件现已存在：
- `schemas/bmcp.recovery-join-1.0.2.schema.json`
- `validators/recovery_join_validator.py`
- `tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py`

Schema 和测试覆盖 H-RJ-HW-01 §§5–7 中明确规定的结构字段及必填性。Validator 检查 JSON/schema 结构和确定性的 D 类型化高水位/Fence 元组绑定。若未提供 D 权威 membership-proof authentication 或 Fence currentness 验证，则返回 `UNKNOWN`。这不代表 D 已采纳该 proposed proof 格式，也不代表生产/runtime 一致性已经成立。

对契约歧义保留明确标记，不作猜测：
- 固定源 Schema Blob `4b664e3bce465499bcdfd93796349a4ba7074002` 声明 envelope `schema_version = 1.0.0`，而 schema `$id` 和契约工件文件名标识 1.0.2。H-RJ-HW-01 没有明确解决此差异；保留现有 envelope const，并在 schema `$comment` 中标记。
- §5.4 将 currentness-proof generation 字段命名为 `forget_fence_generation`；§5.9 伪代码却引用 `proof.fence_generation`。Schema 遵循 §5.4 明确的对象定义，不臆造别名。
- §5.8 将 `lineage_manifest_digest` 命名为 currentness-proof 字段，但 §5.4 未将其列入对象属性和 required 列表。Schema 允许该字段但不要求；当 evidence 需要比较而 proof 未提供该字段时，Validator 返回 `UNKNOWN`。
- §5.7 规定 D LINEAGE/BARRIER_MEMBERSHIP evidence 的 `target_set_digest` 和 `forget_fence_namespace_ref` SHOULD 条件必填，而非 MUST。Schema 定义这两个属性但不强制；语义 helper 在缺失时返回 `UNKNOWN`。
- D 实际 namespace identifier 编码、权威 proof 签发、签名验证和 currentness 查询接口仍未由契约提供。Schema 只验证结构；依赖权威的检查需要注入 D callbacks。

## 测试执行证据

Owner H 本轮未执行本地 pytest。测试函数数量不等于执行结果：provider_outcome 有 10 个测试函数（其中 5 个语义 skip）；applied_delivery_evidence 有 30 个；RecoveryJoin 1.0.2 有 26 个。本轮不声称任何 passed/skipped/failed 实际运行总数，仍需外部重新执行输出。
