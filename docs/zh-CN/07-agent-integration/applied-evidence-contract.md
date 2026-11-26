---
document_metadata:
  domain: agent-integration
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Owner-delegated direction decision, 2026-11-26"
        - "Work Item AID-2026-091"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Direction decision recorded; exact-version Owner acceptance and normative approval pending."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "agent-integration decision contract"
    canonical_scope_id: "agent-integration/decision-085"
    canonical_scope_keywords:
      - architecture-decision
      - agent-integration
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "07-agent-integration/applied-evidence-contract.md"
    en: "docs/en/07-agent-integration/applied-evidence-contract.md"
---
# C/G Applied 证据契约
决议 ID：APPLIED-EVIDENCE-01
授权人：user-authorized operator (delegated by account owner)
日期：2026-11-26
Owner：C（推理边界证明）、G（Delivery 投影）、H（协议/Adapter 回执）
关联 Issue：#1124、#1135、#1180
状态：方向已裁定；精确版本 C/G/H 验收待完成。

## 状态权威与投影
C/H 拥有 Adapter 在推理边界实际执行行为的证据。G 拥有期望 ContextVersion 以及 G DeliveryIntent/Delivery 投影。G 不得根据本地持久化结果制造 Applied。

状态映射：
- G Prepared：已为精确 ContextVersion 持久化创建 DeliveryIntent。
- G Delivered：存在 Payload 交接/传输回执；不意味着 C/H Accepted 或 Applied。
- C/H Received：Adapter 实例已接收 Payload；G 可保存回执元数据，但不能视为 Applied。
- C/H Accepted：Adapter 已验证 Payload 并接受应用。G 必须按 Attempt 保留该独立元数据，不要求新增 G 生命周期状态。
- G Applied：仅在 G 验证到来自最终推理边界、绑定精确 DeliveryAttempt 和 ContextVersion 的有效 C/H AppliedAttestation 后允许。
- Rejected/Expired/Superseded 保持不同终态。超时/ACK 丢失属于 Unknown/Pending，不能视为 Applied，也不能推断为 Rejected。

Delivery ID 标识逻辑交付；DeliveryAttempt ID 标识一次具体尝试。重试在同一 Delivery ID 下创建新 Attempt ID。Supersession 创建新的逻辑 Delivery ID 或显式后继关系。Attempt 证据不可覆盖。

## 最小不可变 AppliedAttestation 记录
~~~yaml
evidence_schema: "applied-attestation/v1"
attestation_id: "<稳定唯一 ID>"
delivery_id: "<逻辑 Delivery ID>"
delivery_attempt_id: "<唯一 Attempt ID>"
context_id: "<Context ID>"
context_session_id: "<Context Session ID>"
context_version_id: "<不可变 ContextVersion ID>"
context_version_sequence: 42
snapshot_digest:
  algorithm_profile: "<已批准的规范摘要配置>"
  value: "<精确规范有序快照字节的摘要>"
managed_region_id: "<托管区域标识>"
managed_region_digest:
  algorithm_profile: "<已批准的摘要配置>"
  value: "<有效托管区域内容的摘要>"
agent_instance_id: "<Agent 实例>"
adapter_id: "<Adapter>"
adapter_instance_id: "<Adapter 实例>"
inference_boundary_id: "<最终推理边界>"
inference_request_id: "<具体推理请求>"
applied_at: "<UTC 时间戳>"
issuer:
  principal_id: "<已认证签发主体>"
  key_id: "<验证密钥引用>"
  signature: "<签名或不可变验证回执引用>"
verification:
  result: "VERIFIED"
  verifier_id: "<验证者身份>"
  verified_at: "<UTC 时间戳>"
~~~

精确密码算法、密钥生命周期和传输编码仍由 I/H 安全及协议规范确定。在这些配置被固定且可独立验证前，该证据属于 CANDIDATE，不得视为已验证 Applied 证明。Attestation 必须将所有身份字段绑定到 DeliveryIntent/Attempt，并将两个 digest 分别绑定到精确 ContextVersion 和实际托管推理区域。仅数字版本号不足以证明身份。

## 证据权威与落点
- C/H 在 Adapter/推理边界证据源生成并保留不可变 Attestation。
- G 在 DeliveryAttempt Ledger 中按 (Delivery ID, Attempt ID) 持久化不可变引用及验证结果；G Applied 是已验证证据的投影。
- Attestation 摘要及签发者/验证者引用必须保留以供审计/重放。G 可以缓存投影，但不是推理事实来源。
- H 传输 ACK/Receipt 与 C Adapter Accepted 是独立记录，不能重新标记为 Applied。
- 本地文件写入、内存更新、快照持久化或 Adapter 侧存储只能证明 Stored/Materialized（可能还有 Received），不能证明最终推理边界 Applied。

## 验证规则
G 在投影 Applied 前验证：Delivery ID 和 Attempt ID；Context ID/Session/不可变 Version ID/序号；snapshot digest；Agent/Adapter/实例身份；最终 Boundary 和 Inference Request；Managed Region ID/Digest 与实际内容一致；签发者真实性/签名或在固定安全配置下的验证回执；以及相对于当前 Context head、Attempt、Supersession 和 Forget/Revocation 状态未过期。

缺失、格式错误、不匹配、不可验证或过期的证据按失败类别产生 Unknown/Rejected，绝不能 Applied。历史证据保持不可变；当前使用有效性必须重新计算。

## Reviewer PASS/FAIL
- AP-01 PASS：Applied 必须要求来自最终推理边界的 C/H Attestation；否则 FAIL。
- AP-02 PASS：Attestation 绑定逻辑 Delivery ID 和唯一 Attempt ID；否则 FAIL。
- AP-03 PASS：Context/session/不可变 Version ID+序号/snapshot digest 与 DeliveryIntent 匹配；否则 FAIL。
- AP-04 PASS：Agent/Adapter/实例/Boundary/Request 身份均绑定并验证；否则 FAIL。
- AP-05 PASS：包含托管区域身份和 digest，并对实际内容验证；否则 FAIL。
- AP-06 PASS：签发者真实性和验证证据可依据固定安全配置独立核验；否则 FAIL。
- AP-07 PASS：本地持久化/物化/接收不能报告为 Applied；否则 FAIL。
- AP-08 PASS：Received 和 Accepted 与 G Delivered/Applied 区分，且 Accepted 作为 Attempt 元数据保留；否则 FAIL。
- AP-09 PASS：Unknown/ACK 丢失保持 Pending/Unknown，重试使用不同 Attempt ID；否则 FAIL。
- AP-10 PASS：G Applied 仅是不可变 C/H 证据的投影/引用，并因 Supersession/Forget/Revocation 对当前使用失效；否则 FAIL。
- AP-11 PASS：EN/ZH-CN 镜像语义一致；否则 FAIL。
- AP-12 PASS：#1124/#1135/#1180 均有评论且保持 OPEN；否则 FAIL。

## 权威边界
C 拥有推理边界事实；H 拥有协议传输/回执；G 拥有期望 Context 和 Delivery 投影；I 拥有身份/信任/密钥策略；D 拥有 ForgetFence 权威。此决议不增加 G 生命周期状态、不定义 BMCP Wire 值、不选择密码算法，也不授权实施。#1124、#1135、#1180 在各自条件及必要 Owner 验收完成前保持 OPEN。不修改 Runtime/产品代码、测试、Schema、Validator、Workflow、部署或生产状态。
