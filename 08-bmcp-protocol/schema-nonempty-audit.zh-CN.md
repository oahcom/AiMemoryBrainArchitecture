# Schema 非空约束审计

**审计基线：** `main`，提交 `88bf4875d1d6266c26cf5e293e43e7d402f7006d`（2026-11-21）。范围：`08-bmcp-protocol/schemas/` 目录下全部直接子级 `*.json`；共检查 2 个文件。

## 统计

- 盘点约束：**93 处**，其中 `minLength: 1` 为 74 处、`pattern` 为 17 处、条件 `minProperties: 1` 为 2 处；`minItems` 为 **0**。
- 已检查 required 数组属性：**14 个**。键必须出现，但没有 `minItems`，因此结构上仍允许 `[]`。
- 修改 **2 处**条件约束：原来的兜底 `else` 分支会在 PARTIAL/NOT_ENUMERATED/UNAVAILABLE/UNKNOWN 且 count 为 0 时也强制 highwater 非空。现在只有 count 大于 0 或状态为 COMPLETE_NON_EMPTY 时才要求非空；零计数的不完整/不可用状态允许为空。
- 保留 **91 处** `minLength`/`pattern` 和 **2 处**收窄后的条件 `minProperties`，并为保留约束补充理由 description。

## 判定规则

required 属性不等于集合必须非空。required 数组键可以包含 `[]`。对 highwater，正数 observed count 或 COMPLETE_NON_EMPTY 状态意味着至少存在一项；零计数的 PARTIAL/NOT_ENUMERATED/UNAVAILABLE/UNKNOWN 状态可能没有可报告 highwater，不得合成。标识符、摘要、计数器、签名和 reason 在提供时不能是空值。

## 完整盘点

| schema | 位置 | 约束 | 可能合法为空？ | 处理 | 理由 |
|---|---|---|---|---|---|
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/issuer_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/sender_authority_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/sender_subject_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/audience` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/message_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/message_nonce` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/signing_sequence_namespace_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/signing_record_sequence` | `pattern=^(0\|[1-9][0-9]*)$` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化计数器采用规范的非负十进制表示；空字符串不属于该数值域。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/signature_profile_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 空签名不包含认证材料。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/key_id_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/key_version` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/adapter_instance_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/runtime_session_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/delivery_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/delivery_attempt_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/inference_request_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/final_request_boundary_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/adapter_capability_epoch` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/adapter_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/runtime_instance_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/context_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/context_version` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/materialized_context_version` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/final_request_boundary_type` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/managed_region_id` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/managed_region_revision` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须携带非空标识符或证据值。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/managed_region_inventory_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/managed_region_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/digest_profile` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要必须承载完整规范化内容承诺；空字符串不是摘要。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/evidence_issuer_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/evidence_schema_version` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/submission_monotonic_sequence` | `pattern=^(0\|[1-9][0-9]*)$` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化计数器采用规范的非负十进制表示；空字符串不属于该数值域。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/correlation_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/causation_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/audit_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/c_submit_outcome_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/c_outcome_record_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/c_outcome_record_sequence` | `pattern=^(0\|[1-9][0-9]*)$` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化计数器采用规范的非负十进制表示；空字符串不属于该数值域。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/c_outcome_payload_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/payload_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/signature` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 空签名不包含认证材料。 |
| `bmcp.applied-delivery-evidence-1.0.0.schema.json` | `/properties/integrity_proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ref` | `pattern=^[A-Za-z][A-Za-z0-9._:/-]*$` | 否——此分支要求值非空 | 保留并收窄条件 | 引用必须以 ASCII 字母开头并包含标识符；空文本无法标识协议对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/counter` | `pattern=^(0\|[1-9][0-9]*)$` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化计数器采用规范的非负十进制表示；空字符串不属于该数值域。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/properties/request_ledger_query_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/properties/admission_ledger_query_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/properties/key_status_generation` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/properties/request_complete_empty_proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/properties/admission_complete_empty_proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/allOf/0/then/properties/request_highwaters` | `minProperties=1` | 否——此分支要求值非空 | 保留并收窄条件 | 仅在已观察到至少一项或枚举状态为 COMPLETE_NON_EMPTY 时要求 map 非空；零计数的不完整/不可用状态仍允许为空。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/ownerSnapshot/allOf/1/then/properties/admission_highwaters` | `minProperties=1` | 否——此分支要求值非空 | 保留并收窄条件 | 仅在已观察到至少一项或枚举状态为 COMPLETE_NON_EMPTY 时要求 map 非空；零计数的不完整/不可用状态仍允许为空。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/noParticipantDisposition/properties/reason` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 空 reason 无法表达处置理由。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/noParticipantDisposition/properties/out_of_scope_proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/noParticipantDisposition/properties/out_of_scope_proof_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/jf10Join/properties/postgres_cluster_system_identifier` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 空值无法标识 PostgreSQL 集群。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/requestDisposition/properties/out_of_scope_proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/requestDisposition/properties/out_of_scope_proof_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/owner_authority_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/scope_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/scope_generation` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/owner_ledger_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/owner_ledger_version` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/ledger_query_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/owner_high_water` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/canonical_empty_root` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/key_status_generation` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/anti_rollback_anchor_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/signature_profile_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/signature_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/completeEmptyProof/properties/proof_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/proof_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/owner_authority_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/request_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/operation_identity_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/operation_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/target_class_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/scope_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/scope_generation` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/applicability_policy_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/reason_code` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 空 reason 无法表达处置理由。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/owner_ledger_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/owner_ledger_version` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/owner_high_water` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/ledger_query_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/key_status_generation` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 类型化序列、代际、epoch 或版本必须可在其命名空间内解析和比较。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/anti_rollback_anchor_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/signature_profile_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/signature_ref` | `minLength=1` | 否——此分支要求值非空 | 保留并收窄条件 | 字段出现时必须指向明确协议对象、Authority、接收方或资源；空字符串无法标识对象。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/outOfScopeProof/properties/proof_digest` | `pattern=^[0-9a-f]{64}$` | 否——此分支要求值非空 | 保留并收窄条件 | 摘要采用固定宽度的小写十六进制完整值；空串或不完整文本不是内容承诺。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/forgetFenceGeneration` | `pattern=^(0\|[1-9][0-9]*)$` | 否——此分支要求值非空 | 保留并收窄条件 | 该字段使用封闭规范词法表示；空字符串不属于该值域。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/properties/owner_admission_to_participant` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 没有 Owner admission→participant 关联边时为空。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/properties/owner_admission_no_participant` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 没有缺少 participant registration 的 Owner admission 时为空。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/properties/participant_to_owner_evidence` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 当前 cutoff 不存在 participant→owner evidence 关联边时为空。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/properties/jf10_participant_joins` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 没有纳入范围的 JF10 participant join 时为空。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/properties/owner_request_dispositions` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | Owner request 集合为空时为空；completeness 与 difference 证据仍独立表达。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/properties/owner_snapshot_membership_proofs` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 没有 admission row 需要 membership proof 时为空；被引用的 proof 仍必须有对应记录。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/participantEvidenceJoin/properties/required_owner_set` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 结构上允许为空；具体 participant 是否允许没有 required owner，须由领域语义裁定。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/participantEvidenceJoin/properties/owner_evidence` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 结构上允许为空；具体 participant join 是否允许没有 owner evidence，须由领域语义裁定。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/differenceSets/properties/owner_registered_without_participant` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 为空表示未发现 owner 已注册但无 participant 的差异。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/differenceSets/properties/participant_without_primary_owner_admission` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 为空表示未发现 participant 缺少 primary owner admission 的差异。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/differenceSets/properties/participant_without_required_owner_evidence` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 为空表示未发现 participant 缺少 required owner evidence 的差异。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/differenceSets/properties/duplicate_or_conflicting_join_edges` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 为空表示未发现重复或冲突的 join edge。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/differenceSets/properties/unproved_not_registered_effects` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 为空表示未发现未证明的 not-registered effect。 |
| `bmcp.recovery-join-1.0.2.schema.json` | `/$defs/differenceSets/properties/owner_request_without_disposition` | `required (array property)` | 是——结构上允许空数组 | 保留 required；不加 minItems | 为空表示没有 owner request 缺少 disposition。 |

## Pattern 说明

17 处 pattern 全部登记，包括十进制计数器与固定宽度摘要。ref pattern 要求首字符为 ASCII 字母，因此也强制非空。守卫保守地登记所有 pattern。

## 范围与限制

扫描范围仅为 `schemas/` 下的直接子级 JSON Schema 文件，不包括递归子目录、Markdown 中嵌入的 schema 片段、运行时 validator 或外部契约。守卫检测新增或变更的 `minProperties`、`minItems`、`minLength` 和 `pattern` 声明。它不能证明保留约束具有规范依据；这仍需人工对照契约审查。守卫也不裁定空数组的业务语义，亦不推断 schema 规则之外的业务含义。
