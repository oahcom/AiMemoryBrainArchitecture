---
document_metadata:
  domain: protocol
  role: index
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Candidate
    canonical_scope_id: protocol/bmcp-message-type-index
    normative_status: Informative
    canonical_conflict_status: None
  bilingual_counterpart:
    source: "08-bmcp-protocol/protocol-index.md"
---

# BMCP 协议消息类型索引

- 范围：`08-bmcp-protocol/`
- 审计基线：`2f8c00d835b04c75e71f1a6ba33e1e465445dec0`
- 目的：按 Schema 中真实的 `message_type` 约束登记消息及工件存在性。本索引不为语义正确性或生产一致性背书。
- 检查器：`python3 08-bmcp-protocol/scripts/check_protocol_index.py`
- 回归测试：`python3 -m unittest discover -s 08-bmcp-protocol/tests -p 'test_protocol_index_consistency.py' -v`

## 盘点方法与实测结果

盘点器只遍历 `08-bmcp-protocol/schemas/*.json`，只统计附着于名为 `message_type` 的属性上的有限字符串约束（`const`、`enum`，包括嵌套的 `oneOf`/`anyOf`/`allOf` 和条件分支）。其他枚举、状态值、事件名、散文、fixture，以及没有有限取值的通用声明 `message_type: { "type": "string" }` 均不计为消息类型。

| 指标 | 审计基线结果 |
|---|---:|
| `schemas/` 中的 JSON Schema 文件 | 32 |
| 含有限 `message_type` 约束的文件 | 31 |
| 不含有限 `message_type` 约束的文件 | 1 |
| 唯一消息类型 | 22 |
| 本索引消息类型行数 | 22 |
| 缺失 / 多余 / 重复 / 无效索引行 | 0 / 0 / 0 / 0 |

唯一不含有限消息类型约束的文件是 `schemas/bmcp.i-owner-snapshot-attestation-1.0.0.schema.json`。它计入 Schema 文件总数，但不被误判为漏索引的消息。

## 消息类型

以下 JSON Pointer 指向精确的 `const` 约束（另有说明时除外）。对于重复版本族，本索引记录代表性观测工件，不据此宣布该版本为规范当前版本。

| 消息类型 | 定义来源 | Schema 与 JSON Pointer | Validator | 一致性测试 | 当前状态 |
|---|---|---|---|---|---|
| `APPLIED_DELIVERY_EVIDENCE_RECORDED` | `phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md`；`phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md` | `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` — `/properties/message_type/const` | `validators/applied_delivery_evidence_validator.py` | `tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | **IMPLEMENTED (artifact presence)** — Schema、Validator 和测试文件均存在；不代表生产一致性。 |
| `COC_PARTICIPANT_MANIFEST` | Schema 内定义；`runtime_reference/recovery_cutoff_semantics.py` 是参考代码，不是权威来源 | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/participantManifest/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_two_phase_recovery.py`（fixture/参考覆盖） | **SCHEMA PRESENT** — 测试/参考代码存在不等于权威一致性成立。 |
| `COC_RECOVERY_CUTOFF_BATCH` | Schema 内定义；`runtime_reference/unified_manifest_semantics.py` 是参考代码，不是权威来源 | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/0/allOf/1/properties/message_type/const` | —（参考语义不是生产 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`；`tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 不代表生产或权威一致性。 |
| `C_PROVIDER_OUTCOME_RECORDED` | C 所有的 CSubmitOutcome 1.0.1 来源 Schema fixture；H Phase 3.8.26 join 补充；C Outcome 语义仍归 C 所有 | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/10/allOf/1/properties/message_type/const`；重复条件 guard：`/oneOf/10/allOf/9/if/properties/message_type/const` | `validators/provider_outcome_validator.py`；`validators/provider_outcome_validator_1_2_15.py`；`validators/envelope_auth_validator.py`；`validators/gateway_attestation_validator.py` | `tests/conformance/provider_outcome/test_provider_outcome.py`；`tests/conformance/provider_outcome/test_provider_outcome_validator.py`；`tests/conformance/provider_outcome/test_envelope_auth_validator.py`；`tests/conformance/provider_outcome/test_gateway_attestation_validator.py` | **PARTIAL** — BMCP 结构/参考验证已存在；C 所有的 issuer、ledger、gate、provider side-effect 和最终请求权威检查仍属外部依赖；证据不可用时保持 UNKNOWN。 |
| `I_JF10_TERMINAL_DECISION_OBSERVED` | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`（来源引用）；保留精确消息拼写 | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/2/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |
| `JF10_BRIDGE_RECONCILIATION_RECORDED` | Schema 内定义；本次限定范围内未映射到独立规范来源 | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/4/properties/message_type/const`；Unified 1.2.17：`/oneOf/9/allOf/1/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`（消息族覆盖） | **SCHEMA + LIMITED TEST REFERENCE** — 无专用 Validator 或生产一致性结论。 |
| `JF10_I_TERMINAL_DECISION_OBSERVED` | Schema 内定义；不得与 `I_JF10_TERMINAL_DECISION_OBSERVED` 混为一谈 | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/7/allOf/1/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`；`tests/conformance/recovery_cutoff/test_i_crypto_profile.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 不代表生产权威验证。 |
| `JF10_PREPARED_PARTICIPANT_REGISTERED` | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/1/properties/message_type/const`；Unified 1.2.17：`/oneOf/6/allOf/1/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`（消息族覆盖） | **SCHEMA + LIMITED TEST REFERENCE** — 无专用 Validator 或生产一致性结论。 |
| `JF10_PREPARE_INTENT_REGISTERED` | `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md`；`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/0/properties/message_type/const`；Unified 1.2.17：`/oneOf/5/allOf/1/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`（消息族覆盖） | **SCHEMA + LIMITED TEST REFERENCE** — 无专用 Validator 或生产一致性结论。 |
| `JF10_STORAGE_PARTICIPANT_RESOLVED` | Schema 内定义；不得与 `STORAGE_JF10_PARTICIPANT_RESOLVED` 混为一谈 | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/8/allOf/1/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`（消息族覆盖） | **SCHEMA + LIMITED TEST REFERENCE** — 无专用 Validator 或生产一致性结论。 |
| `OWNER_ADMISSION_ENTRY` | Schema 内定义；本次限定范围内未映射到独立规范来源 | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/admissionEntry/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |
| `OWNER_ADMISSION_SNAPSHOT_ATTESTATION` | Schema 内定义；本次限定范围内未映射到独立规范来源 | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/ownerSnapshot/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |
| `OWNER_GATE_RELEASE_ATTESTATION` | Schema 内定义；本次限定范围内未映射到独立规范来源 | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/gateRelease/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |
| `OWNER_LOCAL_GATE_RELEASE` | `runtime_reference/owner_gate_release_semantics_1_2_17.py`（仅参考语义） | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/3/allOf/1/properties/message_type/const` | —（参考代码不是权威生产 Validator） | `tests/conformance/recovery_cutoff/test_owner_gate_release_1_2_17.py`；`tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 缺少 Owner verifier 时，权威检查仍为 UNKNOWN。 |
| `OWNER_LOCAL_PENDING_GATE` | `runtime_reference/unified_manifest_semantics.py`（仅参考语义） | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/2/allOf/1/properties/message_type/const` | —（参考代码不是权威生产 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`；`tests/conformance/recovery_cutoff/test_i_crypto_profile.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 缺少 Owner verifier 时，权威检查仍为 UNKNOWN。 |
| `PARTICIPANT_SET_RECONCILIATION` | `runtime_reference/unified_manifest_semantics.py`（仅参考语义） | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/1/allOf/1/properties/message_type/const` | —（参考代码不是权威生产 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`；`tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 缺少 Owner verifier 时，权威检查仍为 UNKNOWN。 |
| `RECOVERY_CUTOFF_BATCH` | `runtime_reference/recovery_cutoff_semantics.py`（仅参考语义） | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/recoveryBatch/properties/message_type/const` | —（未找到专用权威 Validator） | `tests/conformance/recovery_cutoff/test_two_phase_recovery.py`；`tests/conformance/recovery_cutoff/test_hrc_semantics.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 不代表生产或权威一致性。 |
| `RECOVERY_EPOCH_COMPLETED` | Schema 内定义；同时存在于 Recovery Cutoff 与 Unified 版本族 | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/4/allOf/1/properties/message_type/const`；以及 `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/epochCompleted/properties/message_type/const` | —（未找到专用 Validator） | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`; `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py`；`tests/conformance/recovery_cutoff/test_two_phase_recovery.py` | **SCHEMA + REFERENCE TESTS PRESENT** — 不代表生产一致性。 |
| `RECOVERY_JOIN_PROOF` | Phase 3.8 H-RJ-HW-01 §§5–7；消息类型拼写继承自固定源 Schema Blob `4b664e3bce465499bcdfd93796349a4ba7074002` | `schemas/bmcp.recovery-join-1.0.2.schema.json` — `/properties/message_type/const` | `validators/recovery_join_validator.py` | `tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py`；`tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` | **IMPLEMENTED (artifact presence)** — 不代表 D 已采纳 proof、生产一致性成立或权威 currentness 已验证；缺少 D callbacks 时保持 UNKNOWN。 |
| `STORAGE_JF10_PARTICIPANT_RESOLVED` | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`；精确拼写不同于 Unified 的 `JF10_STORAGE_PARTICIPANT_RESOLVED` | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/3/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |
| `Storage.PreparedParticipantReceipt` | Schema 内定义；本次限定范围内未映射到独立规范来源 | `schemas/bmcp.storage-prepared-participant-proof-1.0.0.schema.json` — `/$defs/preparedReceiptMessage/properties/message_type/const; repeated conditional guard at /$defs/preparedReceiptMessage/allOf/0/if/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |
| `Storage.StorageResolutionProof` | Schema 内定义；本次限定范围内未映射到独立规范来源 | `schemas/bmcp.storage-prepared-participant-proof-1.0.0.schema.json` — `/$defs/storageResolutionMessage/properties/message_type/const; repeated conditional guard at /$defs/storageResolutionMessage/allOf/0/if/properties/message_type/const` | —（未找到专用 Validator） | —（未找到消息专属测试） | **SCHEMA PRESENT** — 不给出一致性结论。 |

## 完整 Schema 清单

本次审计目录中全部 32 个 JSON Schema 文件：

- `bmcp.applied-ack-1.1.0-jf10-bridge.schema.json`
- `bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json`
- `bmcp.applied-delivery-evidence-1.0.0.schema.json`
- `bmcp.coc-jf10-unified-1.2.0.schema.json`
- `bmcp.coc-jf10-unified-1.2.1.schema.json`
- `bmcp.coc-jf10-unified-1.2.2.schema.json`
- `bmcp.coc-jf10-unified-1.2.3.schema.json`
- `bmcp.coc-jf10-unified-1.2.4.schema.json`
- `bmcp.coc-jf10-unified-1.2.5.schema.json`
- `bmcp.coc-jf10-unified-1.2.6.schema.json`
- `bmcp.coc-jf10-unified-1.2.7.schema.json`
- `bmcp.coc-jf10-unified-1.2.8.schema.json`
- `bmcp.coc-jf10-unified-1.2.9.schema.json`
- `bmcp.coc-jf10-unified-1.2.10.schema.json`
- `bmcp.coc-jf10-unified-1.2.11.schema.json`
- `bmcp.coc-jf10-unified-1.2.12.schema.json`
- `bmcp.coc-jf10-unified-1.2.13.schema.json`
- `bmcp.coc-jf10-unified-1.2.14.schema.json`
- `bmcp.coc-jf10-unified-1.2.15.schema.json`
- `bmcp.coc-jf10-unified-1.2.16.schema.json`
- `bmcp.coc-jf10-unified-1.2.17.schema.json`
- `bmcp.i-owner-snapshot-attestation-1.0.0.schema.json`
- `bmcp.recovery-cutoff-1.0.0.schema.json`
- `bmcp.recovery-cutoff-1.0.1.schema.json`
- `bmcp.recovery-cutoff-1.0.2.schema.json`
- `bmcp.recovery-cutoff-1.0.3.schema.json`
- `bmcp.recovery-cutoff-1.0.4.schema.json`
- `bmcp.recovery-cutoff-1.0.5.schema.json`
- `bmcp.recovery-join-1.0.0.schema.json`
- `bmcp.recovery-join-1.0.1.schema.json`
- `bmcp.recovery-join-1.0.2.schema.json`
- `bmcp.storage-prepared-participant-proof-1.0.0.schema.json`

## Unified Schema 版本声明

**Latest observed artifact：** `bmcp.coc-jf10-unified-1.2.17.schema.json`；**canonical current version: NOT DECLARED**。

证据：
- 审计目录中存在 18 个不同的 Unified 工件，编号为 1.2.0 至 1.2.17。
- 1.2.17 是当前观测到的最高语义版本，其自身 description 将其称为 artifact revision 1.2.17；这并未声明它是规范当前版本。
- 在 Unified Schemas 和本索引中，没有找到版本发布/替代规则，也没有找到权威 current-version 声明。
- 一致性材料仍明确引用较早版本，包括 1.2.8、1.2.10、1.2.11、1.2.12、1.2.14、1.2.15 和 1.2.16。1.2.10 测试有一条本地 skip 注释，称其语义被 1.2.11/1.2.12 替代；这条测试注释不是整个仓库的版本发布政策。
- 因此，在权威裁定记录前，本索引 MUST NOT 写成 `Current unified schema: ...1.2.17...`。

**所需权威裁定：** BMCP Protocol Owner（Owner H）必须提供版本发布/替代规则并推荐规范版本；Architecture Owner 必须批准 canonical-current 声明。本索引不以文件名排序代替任何一方的裁定。

## 类型定义（非消息类型）

以下类型不计入 22 个消息类型：

| 类型 | 定义来源 | 分类 |
|---|---|---|
| `ProducerRegistrationHighWater` | Phase 3.8 H-RJ-HW-01 §3 | 类型化 high-water 值；不是消息 envelope。 |
| `ForgetFenceGeneration` | Phase 3.8 H-RJ-HW-01 §5 | 类型化 Fence generation；不是消息 envelope。 |

## 证据边界声明

本索引记录 Schema 约束以及指定 Validator/测试工件是否存在。它**不**判定语义是否正确、完整、安全、可互操作或已获 Owner 接受。

- `IMPLEMENTED (artifact presence)` 不代表生产一致性、Runtime 集成、Owner 采纳或权威 currentness。
- `PARTIAL` 不等于 DONE；它表示边界未完成且仍依赖外部权威。
- BMCP 本地 Schema/结构验证不等于 C 语义验证。
- 参考实现或 fixture 测试不会自动成为权威 Validator。
- 必要权威或证据不可用时，`UNKNOWN` 必须继续保持 `UNKNOWN`。

没有 C 权威能力时，BMCP 无法确立 issuer/profile/key authenticity、C ledger inclusion 或 high-water currentness、gate linearization、provider evidence authenticity、实际 provider side-effect truth、COC transaction joins，或 `RequestDigest` 与最终 provider 请求边界实际字节之间的绑定。这些检查必须委托给 C 所有的 verifier；权威能力或证据不可用时必须保持 `UNKNOWN`。

I/D/Storage 所有的 trust、membership、fence 和 prepared-participant 权威也适用相同边界。本地结构或确定性绑定检查不能证明这些外部事实。

## 索引一致性门禁

检查器强制验证：
1. 每个 Schema 中发现的有限消息类型必须且只能出现在索引中一次。
2. 每个索引消息类型必须至少存在于一个 Schema。
3. 重复索引行必须失败。
4. 每行必须引用真实存在、且确实约束该消息类型的 Schema。
5. 新增 Schema 消息类型后，未更新索引必须失败。
6. 删除或重命名消息类型后，陈旧索引行必须被发现并失败。
7. 与 `message_type` 无关的枚举不得被计入。

从仓库根目录运行：

```sh
python3 08-bmcp-protocol/scripts/check_protocol_index.py
python3 -m unittest discover -s 08-bmcp-protocol/tests -p 'test_protocol_index_consistency.py' -v
```

该检查器只负责索引一致性，不验证消息语义、transport、framing、session、handshake、生产 Runtime 或 C/D/I/Storage 权威。

## 一致性测试运行入口

一致性测试位于 `08-bmcp-protocol/tests/conformance/` 下。

| 范围 | 运行命令或准备步骤 | 覆盖内容 |
|---|---|---|
| `applied_delivery_evidence/` | `python -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v` | 此目录下的全部测试。 |
| `recovery_cutoff/` — RecoveryJoin | `python -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p 'test_recovery_join*.py' -v` | 文件名匹配该模式的 RecoveryJoin 测试。 |
| `provider_outcome/` — C 加密配置 | `python -m unittest discover -s provider_outcome -p 'test_c_crypto_profile*interop.py' -v`（在 `08-bmcp-protocol/tests/conformance/` 下运行） | C 加密配置互操作测试；6 项。 |
| `recovery_cutoff/` — I 加密配置 | `python -m unittest discover -s recovery_cutoff -p 'test_i_crypto_profile.py' -v`（在 `08-bmcp-protocol/tests/conformance/` 下运行） | I 加密配置互操作测试；7 项。 |
| `recovery_cutoff/` — HRC 语义 | `python -m unittest discover -s recovery_cutoff -p 'test_hrc_semantics.py' -v`（在 `08-bmcp-protocol/tests/conformance/` 下运行） | HRC 语义测试；44 项。 |
| Conformance Node 依赖 | 在 `08-bmcp-protocol/tests/conformance/` 下运行 `npm ci`。 | 根据 `package-lock.json` 安装锁定的 `canonicalize@5.1.0` 依赖。三个 `.mjs` 参考实现均导入 `canonicalize`。 |

工作流 `.github/workflows/h-applied-delivery-evidence-conformance.yml` 运行上述五条 Python discover 命令。三个加密配置互操作测试文件需要 Node 依赖；未安装该依赖时，其 Node 子进程会失败，而不是跳过测试。本机安装依赖后，三个测试文件通过（共 13 项）。HRC 语义测试文件分别通过 `python -m unittest` 和 `python -m pytest`（44 项）。这些本机结果不表示工作流已经通过。

## CSubmitOutcome 一致性边界

provider_outcome 测试套件只检查固定的 C 所有 Draft 2020-12 Schema 和确定性结构；它不是 C 的语义 Validator。CPO-02、CPO-04、CPO-05、CPO-09 和 CPO-10 仍依赖 C 所有的 Outcome 语义、Ledger/High-Water 权威、Gate 证据和最终请求边界证明。

BMCP 本地 Validator 可以检查 Schema 有效性、必填字段、类型、枚举、未知成员、重复 JSON member 拒绝，以及输入对象中实际存在字段之间的确定性关系。它不能把不可用的 C 证据转换为成功。

## RecoveryJoin 1.0.2 一致性边界

RecoveryJoin Schema、Validator 和一致性测试均存在。Validator 检查 JSON/Schema 结构及确定性的 D 类型化 high-water/Fence 元组绑定。若未提供 D 权威 membership-proof authentication 或 Fence currentness 验证，则返回 `UNKNOWN`。这不表示 D 已采纳 proposed proof 格式，也不表示生产/Runtime 一致性已经成立。
