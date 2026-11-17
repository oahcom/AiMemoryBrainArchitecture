# Phase 3.8.24 — H Applied Delivery Evidence 1.0.0 Schema 与 Validator 候选实现

- 状态：**已实现为测试/符合性候选；不是生产密码学或 Durable Replay 服务**
- Owner：H — BMCP Protocol / Wire and Interoperability
- G 消费方决议：`bd297873bc1e593280484a43cb44b56058d9c4ff`（EN），`82553a47fae2d5e796e0742b46231afe465e75b2`（zh-CN）
- H 决议：`be308261c3e000e712a3cdbd3dbf60507156127b`（EN）
- Unified 1.2.15 保持不变：`860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- Gateway Validator 保持不变：`9cc426d4c26deb452f39daff34c1008dd535e969`

## 1. 用途与隔离

这是独立消息族 `APPLIED_DELIVERY_EVIDENCE_RECORDED`，Schema Revision `1.0.0`。它不扩展、不修改 Unified 1.2.15 的 C Provider Outcome Gateway Attestation P0 Allowlist。H Gateway Ingress Replay Identity 与 H Adapter Observation Replay Identity 仍然分离。

## 2. 精确身份投影

- `HDeliveryBindingIdentity`：`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`。
- `HEvidenceIdentity`：`(HDeliveryBindingIdentity, evidence_kind)`。
- `HObservationRecordIdentity`：`(issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`。

第一个元组标识稳定 Delivery Binding；第二个元组选定 Evidence Slot；第三个元组标识一条不可变签名 Observation。三者不得互相替代。

## 3. Schema 与 P0 规则

JSON Schema 使用 Draft 2020-12、`additionalProperties: false`、精确 Revision/Type 常量、类型化必需身份字段、封闭 `evidence_kind` 与 Coverage/Tier Enum、Digest 编码和条件必需性。Validator 从 Schema 属性集合推导 P0 Allowlist，仅显式排除 `payload_digest`、`signature` 和 `integrity_proof_ref`。未知成员直接拒绝，不得从签名投影中静默丢弃。

测试参考 Canonicalizer 使用确定性的排序键 JSON，仅用于本地测试；它不是生产 H Canonicalization Profile，也不选择 JCS、Hash Domain、Signature Algorithm、Key Registry 或 Trust Root。生产 Canonicalization 与密码学 Profile 仍由 I/H 权限方决策，并需要精确向量。

Tier 1 要求 Managed Region Coverage 完整，且 `materialized_context_version` 与 G 的 `context_version` 精确相等。C Submit Outcome 引用和 Record 引用显式保留 C 所有权；H 不生成 Provider Outcome Truth。

## 4. Validator 行为

参考 Validator 执行：
1. 严格 JSON Object 与 JSON Schema 校验；
2. Tier 1 Coverage/Version 谓词；
3. 精确 P0 投影与 Payload Digest 比较；
4. 注入的 Profile Registration、Key Status、Signature、Protected Identity、C Final-Boundary、G Delivery Binding 与 Capability Epoch 检查；
5. Durable Observation Callback，返回 `NEW`、`SAME_DIGEST_REPLAY` 或 `CONFLICT`。

所有 Authority Callback 都采用三态。False 返回 INVALID；不可用/异常/None 返回 UNKNOWN；缺少验证器绝不视为成功。相同 Observation Identity + 相同 Digest 必须返回原 Durable Result Ref；相同身份但 Digest/不可变元组变化则产生 CONFLICT，禁止覆盖原记录。

## 5. 符合性测试

初始测试模块覆盖：Tier 1 正例、未知字段拒绝、每个 Delivery Binding 身份字段必需、Coverage 不完整、Context Version 不匹配、Digest 篡改、身份域分离、UNKNOWN Trust 结果、无效签名、精确重放和变更 Digest 冲突。

从仓库根目录执行：

```bash
python -m pip install -r 08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt
python -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v
```

## 6. CI 精确结果

- Workflow：[H Applied Delivery Evidence Conformance](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44130722532)
- Run ID：`44130722532`；结论：**SUCCESS**
- 精确测试 Commit：`4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`
- 测试套件：11 项，全部通过（Tier 1 正例、未知字段拒绝、七个 Delivery Identity 字段、Coverage/Version Gate、Digest 篡改、身份域分离、三态 UNKNOWN、签名拒绝、同 Digest Replay、变更 Digest Conflict）。
- 并发 H Recovery Cutoff Conformance：[44130722851](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44130722851)，**SUCCESS**。

CI PASS 仅证明精确 Commit 上该候选 Schema/参考 Validator/测试套件通过。不证明生产 JCS/Signature Trust、Durable Ledger 部署、SDK 互操作、Runtime Adapter 行为、C/G/I Owner 接受、Crash/Restore 或 Production Activation。

## 7. 开放 Gate

- C 必须针对当前 CSubmitOutcome Schema 精确审查 C Boundary 与 C Outcome 字段映射。
- G 必须精确审查 Delivery/Context Binding 和 Full Applied Predicate。
- I 必须批准 Signer/Profile/Key Registry、Trust Roots、Canonicalization 与 Anti-rollback。
- H 必须实现 Durable Observation Replay Storage 和部署 Validator 集成。
- SDK 生成、Runtime Adapter 集成、跨语言向量和生产密码学尚未实现。
- 不隐含全局 Applied Freeze、Production Activation 或 Merge 授权。
