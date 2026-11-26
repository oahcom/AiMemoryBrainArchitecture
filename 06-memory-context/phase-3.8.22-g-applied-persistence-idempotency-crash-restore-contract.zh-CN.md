---
document_metadata:
  domain: memory-context
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: G-owned normative design draft; implementation NOT VERIFIED; cross-owner acceptance required). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: 47423d6f95e613b2f1556f5e359da85d7820617b."
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md"
    zh-CN: "docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md"
---
# Phase 3.8.22 — G 规范性 Applied 持久化、幂等、崩溃恢复与 Restore-Fencing 合同

- Owner：G — ContextVersion、Delivery、Applied State 与 Reconciliation
- 分支：`session-g-memory-context`
- 状态：**G 自有规范性设计草案；实现未验证；需要跨 Owner 精确版本接受**
- 决策模式：按用户指示集中扮演 G 角色起草并自审；**不是独立人类 Owner 签署**。
- 范围：G Applied 决议持久化账本，以及它与 CSubmitOutcome、H Evidence、COC Participant/Terminal Evidence、I Authorization、D ForgetFence 和 Storage Same-GID Resolution 的关联。
- 本合同补充既有精确 G 决议，不会默默修改或替代 §2 所列决议。共享冻结前必须取得新的 C/H/COC/Storage 精确版本消费方决议。

## 1. 规范性结论

G 拥有唯一、持久化、按请求划分的 Applied 决议。C、H、COC、I、D、Storage 均不得创建或修改 G 的 Applied Record。

只有 G 针对一个不可变逻辑 Applied Identity 验证完整 Evidence Revision，且所有证据属于同一 Request 与 Causal Transaction 时，才允许提交 Full Applied：

1. C 的不可变、权威 CSubmitOutcome 证明精确 Final Request 已发生确定成功的 Provider Handoff。
2. H 的 Adapter/Runtime/Delivery 证据经过认证、当前有效、完整性有效，并绑定同一 Request 和 Evidence Revision。
3. COC Terminal Proof 标识同一 Transaction、Participant、Reservation、Request Digest 和 Terminal Result，并具有完整 Recovery-Batch 与 Owner High-Water 证据。
4. I 的适用 Authorization/Receipt-Consumption Terminal Evidence 与 D 的完整 Lineage ForgetFence Evidence 分别由各自权威认证，并由各自权威给出顺序关系。
5. 适用 JF-10 Storage Participant 时，Storage 必须证明 Same-GID Terminal Resolution，以及精确的原子 VisibilityPointer/PublicationReceipt 或 Non-Publication Outcome。
6. G 自身的 ContextVersion、Delivery Attempt、Scope/Environment、Managed-Region Inventory/Digest、Identity、Session 和 Capability Predicate 在要求的线性化点全部通过。

Transport ACK、H Validator Result、COC Quorum/Commit、I COMMIT_WON、D Clearance、Storage Prepared Receipt、C Provider Receipt 或 CSubmitOutcome 中的任何单项，都不能单独构成 Full Applied。

Full Applied 仅表示指定 ContextVersion 在有效授权/Fence/Capability 绑定下包含于精确提交的 Request。它不证明模型已开始执行、注意到内容、理解、回忆、行为使用、回答正确、用户已收到、全局 Forget 完成或物理擦除。

## 2. 精确源文件 Pin 与证据边界

本草案从各 Owner 指定分支读取并核对了以下工件：

| 证据族 | 精确来源 | Blob SHA | G 的用途/限制 |
|---|---|---|---|
| G Applied / Forget 基线 | `session-g-memory-context:06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G 生命周期、Predicate、历史事实/当前使用分离及 CGH-APPLIED-1.1 决议 |
| G JF-10 Bridge 接受 | `phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | `25c1da1f6769165881d217bb0bb492a997e0e14c` | COC/JF-10 是必要证据，不是 G Authority |
| G Durable COC Boundary | `phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | 完整 Terminal Proof 与 Fail-Closed Recovery 边界 |
| G Prepared Participant/GID | `phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | 精确 PreparedParticipant/GID/DB Incarnation 元组；Native XID 仅是观察值 |
| G Restore Consumer Acceptance | `phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | `0910fea807b96a896e361cd2722e4c94df55187b` | Restore 不等于 Applied 或 Current-Use Authorization |
| C CSubmitOutcome 1.0.1 Schema | `session-c-agent-integration-2026-11-16:07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | 不可变 C 对象结构；Issuer、Ledger、Provider Truth 和 Join 仍需语义验证 |
| C 规范性 Provider Submit Outcome | `phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` | 五值 Outcome 代数、Same-Key Recovery 与不可变 C Attempt 语义 |
| C Causal-Order Addendum | `phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` | 因果顺序与 Recovery-Batch 组合 |
| C Final Request Evidence | `phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | 实际不可变 Post-Transformation Request Boundary |
| H Unified 1.2.15 Schema | `session-h-bmcp-protocol:08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.15.schema.json` | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | 候选 Wire Structure；不是 JF-10 Applied ACK Schema |
| H 1.2.15 Gateway Validator | `validators/gateway_attestation_validator.py` | `9cc426d4c26deb452f39daff34c1008dd535e969` | 本地 Gateway-Attested Ingress/Replay Validator；生产 Callback 仍是部署接口 |
| H 1.2.15 Provider Validator | `validators/provider_outcome_validator_1_2_15.py` | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | 本地 C 对象/Schema/语义验证；不负责 G Applied 决议 |
| H JF-10 Applied ACK Bridge Schema | `bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` | `a8a945cc3623c2907003b93625e3c79742150944` | 独立候选 Schema 家族；不可与 H Unified Provider Outcome 混用 |

G 已接受的 A Recovery-Batch Package 与配套 COC Architecture 精确 Blob 分别为 `4961ffefc0f9920efb8425a9b2a7af42d8f64819` 和 `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`。这些精确引用不证明 Coordinator、Durable Participant Service 或 Storage 实现已部署。

H 1.2.15 本地测试/CI 仅是候选级证据，其 Callback 接口使用确定性 Test Double。本合同不声称生产 Trust Root、真实 I/D Owner Ledger、已部署 COC Quorum、Durable Replay Service、Provider Truth、Storage Same-GID Recovery 或多副本线性化已经成立。

## 3. 身份模型——四种不可互换的 Identity

### 3.1 CSubmitOutcome Identity（C 所有）

G 必须区分稳定逻辑 Provider Attempt 与每条不可变 C Outcome Observation：

`CProviderAttemptIdentity = (issuer_authority_ref, sequence_namespace_ref, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, IdempotencyNamespaceRef, IdempotencyKeyRef, RequestDigest)`

`COutcomeRecordIdentity = (issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

C 对象还必须绑定精确 `AdapterRef`、`EndpointRef`、API Operation、`FinalRequestBoundaryRef`、`RequestDigest`、分配后实际的 `ActualInferenceRequestId`、`CausalOrderTransactionRef`、COC Intent/Reservation Ref，以及适用 Outcome/Evidence Ref。

- `CProviderAttemptIdentity` 在同一个逻辑 Provider Attempt 的追加式 Outcome Observation 之间保持稳定。
- `COutcomeRecordIdentity` 标识一条不可变 C Ledger Record。`payload_digest`、`OutcomeEvidenceDigest`、`RequestDigest` 是内容/完整性值，不是 Identity 替代物。
- 相同 COutcomeRecordIdentity + 相同不可变 C Payload Digest 表示同一 Record。相同 Record Identity + 不同 Payload Digest 或不可变 Record 元组变化，属于硬完整性冲突，必须隔离。
- 迟到 Receipt 或 Same-Key Lookup 必须由 C 追加为新的不可变 Observation/Successor，具有新的 COutcomeRecordIdentity，并通过 C 的 Prior/Supersedes/Reconciliation Ref 明确关联到同一 CProviderAttemptIdentity；不得改写原 C Record 或创建新的 Provider Attempt。
- `UNKNOWN` 和 `IN_DOUBT` 是非终态，必须保留同一个 ProviderAttempt 和 Provider Idempotency Key；禁止 Retry-as-New。

只有 C 的确定成功 Handoff Outcome（当前为 `HANDOFF_ACCEPTED`，且所有必需 Provider/Participant Proof 齐全）才具备进入 Full Applied 评估的资格。`HANDOFF_REJECTED`、`NOT_INVOKED`、`UNKNOWN` 和 `IN_DOUBT` 均不得产生 Full Applied。

### 3.2 H Evidence Identity（H 所有的协议证据）

G 必须区分稳定 H Delivery Binding、每一种 Evidence Kind 与每条不可变 H Ingress Observation：

`HDeliveryBindingIdentity = (adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`

`HEvidenceIdentity = (HDeliveryBindingIdentity, evidence_kind)`

`HObservationRecordIdentity = (issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

以上均为**建议的标准化消费方元组**。共享冻结前，C 和 H 必须明确确认精确字段名、Requiredness、Canonicalization，以及它们与当前 H 1.2.15 Schema/Validator 的映射。G 不声称现有 H Schema 或 Validator 已经冻结这些元组。

**已观察到的映射缺口：**本次读取的 H 1.2.15 JSON Schema 并未将完整 HDeliveryBindingIdentity 暴露为一等 Schema Property：`adapter_instance_ref`、`runtime_session_ref`、`delivery_id`、`delivery_attempt_id`、`inference_request_id`、`final_request_boundary_id` 和 `adapter_capability_epoch` 均未出现在本次审查读取的 Schema Property 集合中。Gateway Validator 的 Signed P0 Allowlist 虽包含 `provider_adapter_ref`、`actual_inference_request_id` 和 `final_request_boundary_id`，但它本身尚未建立上述完整元组。H 必须选择：(a) 在版本化 Signed P0 Mapping 中新增并验证缺失字段；或 (b) 绑定一份承载完整元组、经过认证且不可变的 H Owner Evidence Record，并提供精确 Schema/Validator 映射。在 C/H 接受该精确映射之前，HEvidenceIdentity 只是 G 消费方要求/提案，不是已冻结的 H Wire Contract。

HDeliveryBindingIdentity 和 HEvidenceIdentity 均不包含 Digest。H P0 Digest 是不可变内容，必须与 HObservationRecordIdentity 分开比较：

- 相同 HObservationRecordIdentity + 相同 H P0 Digest + 相同且经过认证的不可变 Receipt/Result Ref：精确重放，返回原始持久化 H 处置结果；
- 相同 HObservationRecordIdentity + 不同 H P0 Digest：`CONFLICT`，隔离两份 Observation，禁止 Last-Write-Wins；
- 只有当 H 的认证 Owner Ledger 明确将新的 HObservationRecordIdentity 关联到同一个 Delivery Binding 时，才允许在相同 HDeliveryBindingIdentity 下追加 Successor Observation；该 Observation 是新的 Evidence Revision，不是新的 G Applied Attempt；
- HDeliveryBindingIdentity 变化（例如新的 DeliveryAttempt、RuntimeSession 或 CapabilityEpoch）即构成不同逻辑 Delivery，不得重新绑定到旧 Applied Attempt。

H Ingress Replay Protection 是独立层。H 的 Message Identity/Nonce 与 H P0 Digest 用于保护认证 Envelope Ingress/Replay；它们不是 G Applied Identity，也不是 C ProviderAttempt Identity。H 的 `IDEMPOTENT_REPLAY` 只证明同一 H Ingress Result 获得授权重放，不证明产生了新的 G Applied Commit。

### 3.3 COC Participant Identity（COC/Storage 所有）

适用 JF-10 Participant 时，G 必须绑定精确 Participant 元组：

`COCParticipantIdentity = (CausalOrderTransactionRef, ParticipantIntentRef, ParticipantReservationRef, PreparedParticipantRef, PreparedTransactionGID, CanonicalAuthorityDBRef, DB system/database incarnation, ParticipantTupleDigest)`

在适用时，还必须绑定原始 Prepare Timeline/LSN、Publication Operation/Request Digest、Owner Boundary、COC Intent Position/Digest、Storage Signer/Key Version/Audience，以及精确 VisibilityPointer/PublicationReceipt Transaction/Digest。

- `PreparedParticipantRef` 和 `PreparedTransactionGID` 是稳定 Participant Identity/Handle。
- Native Storage XID 只是观察证据，不能替代 PreparedTransactionGID 或 Participant Identity。
- COC Transaction/Participant Identity 不得与 I Sequencer Position、D Fence Generation、G ContextVersion、Delivery Cursor 或 ProviderAttempt Generation 互换。
- COC Terminal Proof 必须绑定相同 Transaction、Participant、Reservation、不可变 Request Digest、Participant Digest、Terminal Outcome，以及 Recovery-Batch/Owner High-Water Evidence。
- Participant Enumeration 缺失不等于空 Participant Set。Owner High-Water 证据缺失、不完整或回退均为 UNKNOWN，必须阻止晋升。

### 3.4 G Applied Identity（G 所有）

G 必须为预期 Applied Fact 派生一个稳定逻辑身份：

`GAppliedIdentity = (ContextId, ContextVersion, DeliveryId, DeliveryAttemptId, InferenceRequestId, FinalRequestBoundaryId, CProviderAttemptIdentity, HDeliveryBindingIdentity, COCParticipantIdentity)`

持久化唯一键为：

`GAppliedIdentityKey = SHA-256("AIMBA-G-APPLIED-IDENTITY-v1\\0" || Canonical(GAppliedIdentity))`

Canonicalization 必须使用明确版本化、确定性的 Profile，拒绝重复 JSON Key 和未知 Critical Field，并保留类型差异。每条 Record 都必须保存 Canonicalization Profile ID 与实现 Revision。

Identity Key 不包含 C Outcome Payload Digest、Provider Receipt Digest、H P0 Digest、C Outcome Evidence Digest、Participant Digest 或 G Aggregate Digest。这些值是绑定到 Identity 的不可变**证据内容**，必须独立比较。C 的 `RequestDigest` 是 CProviderAttemptIdentity 中唯一以 Digest 形式出现的组成部分，因为 C 将精确 Request 变化定义为不同 Provider Attempt/Key Scope；它不是 C Outcome Payload Digest，也不是 H/COC Evidence Digest。这样可避免通过更改 Evidence Digest 伪造新的逻辑 Applied Identity。

不同 ContextVersion、DeliveryAttempt、InferenceRequestId、Final Boundary、C Outcome Identity、H Evidence Identity 或 COC Participant Identity，构成不同逻辑 Applied Attempt。不得覆盖或回滚较早 Record。

## 4. Evidence Revision 与 Digest 冲突规则

对一个 GAppliedIdentity 的每次评估，都必须引用不可变 Evidence Revision：

`AppliedEvidenceRevision = (GAppliedIdentityKey, revision_number, EvidenceSetDigest, exact_source_refs)`

`EvidenceSetDigest = SHA-256("AIMBA-G-APPLIED-EVIDENCE-v1\\0" || Canonical(complete evidence set))`

Evidence Set 必须按适用情况包含：

- 精确 COutcomeRecordIdentity、其 C Payload Digest、稳定 CProviderAttemptIdentity、C RequestDigest 和 Provider Outcome Evidence Ref；
- 精确 H HEvidenceIdentity 与 HObservationRecordIdentity、H Schema Artifact Revision、H P0 Digest、认证 Receipt/Result Ref、Materialization/Managed-Region Inventory 与 Digest；
- 精确 COC Transaction/Participant/Reservation/GID Identity、Terminal Proof Ref/Digest、Recovery-Batch Ref/Digest、Participant Completeness 与 Owner High-Water Vector；
- I Decision/Receipt/PermissionEpoch Proof Ref 与 Digest；
- D Fence Generation、Lineage Proof、Request Cutoff 和 Effective Position，分别保存，不得合并；
- Storage DB Incarnation、Same-GID Resolution Proof、Native XID Observation、VisibilityPointer/PublicationReceipt 或 Non-Publication Proof；
- 精确 G ContextVersion、Delivery Attempt、Scope/Environment、Agent/Adapter/Runtime/Session、CapabilityEpoch 和 Predicate-Profile Revision。

规范性重复处理：

| 条件 | G 必须采取的行为 |
|---|---|
| 相同 GAppliedIdentityKey + 相同 Revision Number + 相同 EvidenceSetDigest | 返回原始持久化处置和 Receipt；不得创建第二条 Applied Row，不得改写时间戳 |
| 相同 Key + 相同 Revision Number + 不同 EvidenceSetDigest | 硬冲突；隔离两份 Evidence Set；禁止覆盖 |
| 相同 HObservationRecordIdentity + 不同 H P0 Digest | H Evidence Conflict；G 禁止晋升 |
| 相同 COutcomeRecordIdentity + 不同 C Payload Digest 或不可变 Record 元组 | C Evidence Conflict；G 禁止晋升 |
| 相同 COCParticipantIdentity + 不同 Participant/Terminal Digest 或矛盾 Terminal Result | COC/Storage Conflict；G 禁止晋升 |
| 新的、有效的 C Successor Observation 或 H Successor Observation，且明确关联同一 CProviderAttemptIdentity/HDeliveryBindingIdentity | 追加新的 Evidence Revision；保留旧 Revision 与处置；重新评估同一个 GAppliedIdentity，绝不创建新 Attempt Identity |
| 已提交 Full Applied 后到达迟到 Evidence | 只追加历史 Enrichment；不得改写原 Applied Record 或追溯修改 Predicate Snapshot |

只有来源权威签发了新的不可变 Successor/Observation，并且它关联到同一原始 Attempt 时，才允许创建新的 Evidence Revision。调用方不得把同一 Source Identity 下的篡改字节标记为新 Revision。

`UNKNOWN` 或 `IN_DOUBT` 评估必须在同一 GAppliedIdentityKey 下持久化为非 Full 的未解决处置。后续权威证据可以追加 Successor Evidence Revision，并触发对同一 Identity 的重新评估；不得创建新的 ProviderAttempt、Provider Idempotency Key、Delivery Attempt 或 COC Participant 来逃避未解决状态。

一个 GAppliedIdentityKey 最多只能存在一条不可变 Full Applied Commit。后续 Revocation/Forget/Supersession 应产生独立的 Invalidation/Current-Use Event，不得修改历史 Applied Commit。

## 5. G 持久化协议

G Persistence Layer 必须对 `GAppliedIdentityKey` 建立 Durable Unique Constraint，并对 `(GAppliedIdentityKey, revision_number)` 建立第二个 Unique Constraint。最终 Applied Table/Event Stream 必须确保每个逻辑 Identity 最多只有一条 Full Applied Commit。

最小本地原子提交单元：

1. Insert-or-Read G Applied Identity Reservation；
2. 插入不可变 Evidence Revision 及其 Source Pin/Digest；
3. 持久化 Predicate Result 与精确 Authority Snapshot/Cursor；
4. 仅当完整 Predicate 通过时，追加不可变 Full Applied Fact；
5. 追加 Audit/Decision Event 及任何本地 Outbox Notification；
6. 将全部本地 Row/Event 原子提交。

不得让部分 Applied Row 对外可见。数据库 Unique Conflict 必须通过读取现有 Durable Identity/Revision 并执行 §4 规则解决，绝不能通过覆盖解决。

最终本地提交前，G 必须针对权威 I、D、COC、Storage Evidence 重新验证 Currentness/Linearization Predicate，包括适用 Context BaseVersion/CAS 与 Delivery Attempt。若 Authority 不可用、证据过期或位置不可比较，结果为 UNKNOWN，不得提交 Full Applied Fact。

G 不得跨域比较不透明的 COC、I、D 和 Storage Position。每个 Owner 必须验证自己的 Ordering Domain 并提供针对同一 Participant/Request 的 Terminal Proof/Cutoff Relation。G 消费已签署的关系，不得自行创造全局数值顺序。

## 6. 崩溃、超时与重试恢复

| 崩溃/故障点 | 预期持久化状态 | 恢复规则 |
|---|---|---|
| G Identity Reservation 前 | 无 G Reservation 或 Applied Fact | 仅在重新验证所有 Gate 后，使用同一逻辑 Request Identity 重新提交 |
| Reservation 后、Evidence Revision 前 | Reservation Pending；没有 Full Applied | 按精确 GAppliedIdentityKey 读取并恢复；不得分配第二个 Key |
| 本地原子提交期间，调用方不知道结果 | 本地 Row 要么全部提交，要么全部未提交 | 按精确 GAppliedIdentityKey 与 Revision 读取；Storage 读取不可用时保持 UNKNOWN/IN_DOUBT |
| Full Applied 已提交，但响应/ACK 未送达 | 不可变 Applied Fact 与 Audit Event 已存在 | 返回原始 Receipt/Disposition；不得插入第二条 Fact |
| C Provider Handoff 已发生，但 C Outcome/Receipt 未持久化 | C Outcome 为 UNKNOWN/IN_DOUBT；G 无 Full Applied | C 使用同一 ProviderAttempt 与同一 Provider Idempotency Key 协调恢复；G 持续抑制受保护内容 |
| COC Terminal Proof 已存在，但 G 尚未提交 | COC Terminal Proof 不可变；G Identity 可能 Pending | 重新验证精确 Proof，并在同一 GAppliedIdentityKey 下提交 |
| COC/Provider/Storage Authority 不可用 | Participant 或 Evidence 未解决 | 禁止 Full Applied；保持必要 Barrier；禁止 Retry-as-New |
| Recovery Batch 不完整或 Owner High-Water 回退 | Batch 不完整 | 阻止新的 Full Applied 和受保护 Current Use，直到权威协调完成 |

Retry 是同一 Identity 的读取/协调恢复，不是新 Transaction。自动 SDK Retry、Transport Retry、Redirect、Account/Region/Model Failover、Stream Restart 或 Provider Re-Send 均不得绕过 C 的 Same-Key Policy 或 G Identity Reservation。

Timeout、进程崩溃、Row 缺失、ACK 丢失、Queue 为空或 Provider Lookup 故障，均不能证明 `NOT_INVOKED`、`HANDOFF_REJECTED`、Rollback 或 Safe Abort。若可能已发生副作用，必须保留 `IN_DOUBT`。

## 7. Restore Fencing 与回滚抵抗

Restore 是新的 Trust Boundary，不是通往 Applied 或 Current Use Authorization 的捷径。

在恢复的 Context、Delivery、Applied 或 Evidence Ledger 数据可被服务、Materialize、Replay 或用于提交新的 Applied Fact 之前，G 必须安装 Durable `GRestoreFence`，阻止受影响的 Protected Use 与新的 Full Applied 晋升。

Restore Reconciliation 至少必须绑定：

- 恢复后的 DB Incarnation/System/Database Identity 与 Restore Epoch；
- 精确 Storage Snapshot/Checkpoint 和 Restore Receipt；
- G Applied Ledger Checkpoint、Sequence/High-Water 与 Evidence-Revision High-Water；
- COC Prefix/Terminal Participant Ledger 与 Recovery-Batch High-Water；
- I PermissionEpoch/Revocation Terminal High-Water；
- D ForgetFence/Lineage High-Water，包括 Pending Cutoff/Effective-Position 状态；
- 当前 Context Head 与 Delivery Cursor/Attempt High-Water；
- 每个未解决 Prepared Transaction 的精确 Same-GID/Participant Resolution。

Restore 必须从不可变 Identity Key 与 Evidence Revision 重建并验证 Unique Index。相同 Digest 的重复 Key 去重到原始 Durable Record；相同 Key、不同 Digest 的碰撞必须隔离并阻止受影响 Scope。Restore 不得签发替代 Applied Identity、Provider Key、Delivery Attempt 或 COC Participant Identity 来伪装旧工作为新工作。

早于 I Revocation、D ForgetFence、COC Participant Terminal、Storage Publication/Rollback 或 G Applied Invalidation 的恢复 Snapshot 均为 Stale。G 必须抑制它，并与当前 Owner High-Water 协调。High-Water 过期或缺失属于 UNKNOWN，不得解释为零或空集合。

只有 Durable、Authenticated 的 RestoreReconciliationReceipt 证明所有必要 Ledger/Prefix 与 Owner High-Water Vector 完整且当前有效、所有 Prepared Participant 均有确定 Same-GID Terminal Resolution，并且新鲜 I/D/Current Context/Capability 检查通过后，才可清除 Restore Fence。G 无权签发 I 或 D Proof，也无权清除 Owner Local Barrier。

任何恢复的 Snapshot、Delta、ACK、Cache、Queue Item 或历史 Applied Record，都不得复活当前 Forget Tombstone 覆盖的内容。历史 Applied 保留为历史；在独立重新授权并完成 Reconciliation 前，Current Use 仍然禁止。

## 8. Forget/Revocation 竞争与 Current-Use Projection

G 必须保持以下顺序域相互独立：

- C Provider Attempt/Handoff 与不可变 CSubmitOutcome Sequence；
- COC Transaction/Participant Order 与 Terminal Proof；
- I Policy Sequencer Decision/Receipt 与 Revocation Request Cutoff；
- D ForgetFence Generation、Request Cutoff 与 Effective Position；
- Storage Same-GID Resolution/Publication Position；
- G Local Applied Commit 与 Context/Delivery Version。

规则：

1. 若 I Revocation 在适用 Receipt Consumption 前获胜，则阻止 Provider Admission/Full Applied。
2. 先前的 I Terminal COMMIT_WON 可以对其精确 Participant 保持已提交；后续 Revocation 不得改写它，但必须在其权威 Cutoff 生效时得到遵守。
3. D Forget Request 若早于 Participant-Intent Cutoff，则拒绝 Admission。较晚 D Fence 必须计入所有先前未解决 Participant；没有 D 明确的安全 Terminal Proof，不得将其视为已越过未解决 Participant 而生效。
4. 若有效 Provider Submission/Applied 在线性化顺序上早于后续 Effective Forget/Revocation，保留历史 Applied，并追加 `InvalidatedForCurrentUse`。
5. 若 Forget/Revocation 排在 Submission 之前，则禁止 Full Applied。
6. 若顺序、Lineage、Owner High-Water 或 Provider Outcome 未知，不得晋升 Full Applied；必须抑制 Protected Current Use，并保留 UNKNOWN/IN_DOUBT。
7. Restore、Retry 或 Duplicate Evidence 不得绕过 Forget/Revocation Barrier。

Current Use 是独立 Projection，在每次 Protected Use 前以及每次 Final Request Submission 前重新计算。必须检查当前 Context Head、Delivery Status/Attempt、I PermissionEpoch/Decision、D Fence/Lineage、Scope/Environment、认证 Identity、RuntimeSession、Adapter CapabilityEpoch 及未解决 Participant/Recovery State。历史 Applied 本身永远不是 Current-Use Authorization。

## 9. G Applied 机器可读记录的必需字段

实现至少必须持久化以下不可变字段（字段名为逻辑合同名称；Generated Schema/SDK 映射仍是独立交付物）：

- `g_applied_identity_key`、`identity_canonicalization_profile`、`identity_schema_revision`；
- 精确 ContextId/ContextVersion、DeliveryId/DeliveryAttemptId、InferenceRequestId、FinalRequestBoundaryId；
- CProviderAttemptIdentity、COutcomeRecordIdentity、CSubmitOutcomeRef、CSubmitOutcomeDigest、RequestDigest、ProviderAttemptRef/Generation、Provider Idempotency Namespace/Key Ref；
- HDeliveryBindingIdentity、HEvidenceIdentity、HObservationRecordIdentity、H Schema Artifact Revision、H P0 Digest、Authenticated H Receipt/Result Ref、Adapter/Runtime/Session/CapabilityEpoch；
- COCParticipantIdentity、CausalOrderTransactionRef、Participant Intent/Reservation Ref、PreparedParticipantRef、PreparedTransactionGID、DB Incarnation、ParticipantTupleDigest；
- COC Terminal Proof、Recovery-Batch Proof、Participant Completeness 与 Owner High-Water Ref/Digest；
- I Authorization/Receipt/PermissionEpoch Ref 与 Digest；
- D ForgetFence Generation、Lineage Proof、Request Cutoff 与 Effective Position，分别记录；
- Storage Same-GID Terminal Proof、Native XID Observation、VisibilityPointer/PublicationReceipt 或 Non-Publication Proof；
- Scope/Environment、Agent/Adapter/Runtime Identity、Managed-Region Inventory/Revision/Digest 与 Predicate-Profile Revision；
- Evidence Revision Number、EvidenceSetDigest、Decision Disposition、G Applied Commit Receipt、本地 Ledger Sequence/High-Water 与时间戳；
- Restore Epoch/Fence Ref 与 Invalidation/Current-Use Projection Event。

未知或不可用的 Proof 必须显式表示为 UNKNOWN，并附 Reason 与 Missing-Source List。不得用空字符串、空数组、伪造零位置或省略 Participant Set 表示未知。

## 10. 符合性义务——已规定，尚未执行

| ID | 对抗场景 | 必须结果 |
|---|---|---|
| G-AP-P01 | 相同 Identity/Revision/Digest 提交两次 | 只有一条 Durable Applied Fact；第二次返回原 Receipt |
| G-AP-P02 | 相同 Identity/Revision 但 Aggregate Digest 改变 | Conflict/Quarantine；禁止覆盖 |
| G-AP-P03 | 相同 HObservationRecordIdentity 但 H P0 Digest 改变 | Conflict/Quarantine；禁止 Full Applied |
| G-AP-P04 | 相同 COutcomeRecordIdentity 但 C Payload Digest 改变 | Conflict/Quarantine；禁止 Full Applied |
| G-AP-P05 | 相同 COC Participant Identity 但 Terminal Digest/Outcome 矛盾 | Conflict/UNKNOWN；禁止 Full Applied |
| G-AP-P06 | Provider Side Effect 可能发生后 C 为 UNKNOWN/IN_DOUBT | 同一 ProviderAttempt/Key；禁止 Full Applied；保持 Barrier |
| G-AP-P07 | Provider Handoff 后、C Outcome 持久化前崩溃 | IN_DOUBT；只允许 Same-Key Recovery |
| G-AP-P08 | G Local Commit 后、调用方收到响应前崩溃 | 读取原 Commit；不得产生第二条 Applied Fact |
| G-AP-P09 | G Atomic Commit 期间崩溃 | 本地事务全有或全无；按同一 Identity 解析 |
| G-AP-P10 | COC Terminal Proof 已存在但 G Commit Pending | 重新验证并使用同一 G Identity 提交 |
| G-AP-P11 | Recovery Batch 漏掉一个 Pre-Batch Participant | UNKNOWN；禁止新的 Full Applied |
| G-AP-P12 | Restore 后 Owner High-Water 回退 | Restore Fence 保持；阻止 Protected Use |
| G-AP-P13 | 恢复后的 DB Incarnation/GID 与 Prepared Participant 不同 | UNKNOWN/IN_DOUBT；禁止 Visibility/Applied 晋升 |
| G-AP-P14 | 恢复 Snapshot 早于 D Forget 或 I Revocation | 抑制 Stale Content；禁止复活 |
| G-AP-P15 | 有效历史 Applied 后发生 Effective Forget | 保留历史 Record；使 Current Use 失效 |
| G-AP-P16 | Forget/Revocation 与 Provider Submit 的顺序未知 | UNKNOWN；抑制；禁止 Full Applied |
| G-AP-P17 | Delivery Supersession 后收到相同 Key 的 Duplicate ACK | 仅历史记录；不得修改更新的 Attempt |
| G-AP-P18 | H Replay 有效但 G Applied Predicate 不完整 | 禁止 Full Applied；H Replay Result 不等于 G Commit |

必需测试包括 Durable Database Crash Injection、Process Restart、多副本并发重复提交、从 Stale Checkpoint Restore、Owner High-Water Regression、精确 Same-GID Lookup 和 Current-Use Revalidation。仅有 Pure Unit Test 或 Callback Double 不足以关闭生产 Persistence/Restore 义务。

## 11. Owner 边界与必须取得的接受

- G 拥有 Applied Identity、Evidence-Revision Ledger、Full Applied Predicate、Durable Commit/Idempotency、Historical/Current-Use Projection 与 G Restore Fence。
- C 独占 CSubmitOutcome Truth、ProviderAttempt 与 Same-Provider-Key Recovery。
- H 独占 Wire Schema、Authenticated Adapter/Runtime/Delivery Evidence、H Envelope Replay/Integrity 与 CapabilityEpoch。
- COC 拥有 Coordinator Transaction/Participant/Terminal/Recovery-Batch Ordering Evidence；不得代签 C/I/D/Storage/G 决议。
- I 独占 PermissionEpoch、Authorization 与 Revocation Terminal Evidence。
- D 独占 Canonical ForgetOperation、ForgetFence、Lineage、Request Cutoff 与 Effective Position。
- Storage 独占 DB Incarnation、Same-GID Resolution、VisibilityPointer/PublicationReceipt 与 Restore Receipt。
- G 不跨 Owner 比较不透明 Position，也不推断缺失的 Owner Proof。

本补充合同称为 Shared/Frozen 前，必须取得以下精确版本接受：

1. C 接受 G Identity/Evidence-Revision 与 CSubmitOutcome 1.0.1 及 C Causal-Order Source Pin 的精确 Join。
2. H 接受精确 HEvidenceIdentity/HDeliveryBindingIdentity 元组，并提供其到 Unified 1.2.15 Gateway Evidence 的缺失 Signed-Schema/Owner-Record 字段映射，同时确认 H Ingress Replay 与 G Applied Idempotency 的区别。
3. COC/Storage 接受精确 Participant/GID/Terminal/Restore 绑定与 Recovery 语义。
4. I 与 D 在各自权威范围内确认 Owner Evidence/Cutoff/High-Water 字段。
5. G 实现提供 Generated Machine-Readable Schema/SDK、Durable Unique Index、Crash/Restart/Restore Test，并由独立审查针对精确 Commit 读回。

H 1.2.14、此前 G Consumer Review、CGH-APPLIED-1.1 Semantic Package、Schema-Only Acceptance 或 Documentation CI 的批准均不自动转移。本文件是 G 自有设计合同，不是实现存在的证明。

## 12. 当前处置

- G Applied Persistence / Idempotency 合同：**本 G 草案已规定；尚未实现/验证**。
- CSubmitOutcome 1.0.1 精确源绑定：**已 Pin；需要 C 对本补充合同精确接受**。
- H EvidenceIdentity 元组：**提案；当前 1.2.15 Schema 未暴露全部 Binding 字段；需要 H/C 精确字段映射及 Schema/Owner-Record 扩展**。
- COC Participant/GID Join：**G 已有设计接受；仍需 COC/Storage 实现与本补充合同精确接受**。
- Crash/Restart/Restore-Fencing 符合性：**已规定 / 未运行**。
- G Applied Persistence 生产证明：**未验证**。
- 全局 C/G/H Applied 冻结：**NO**。
- 生产 Egress/Activation：**NOT AUTHORIZED**。

本合同不声称 Provider Side Effect Exactly-Once、模型执行、全局 Forget 完成、物理擦除或生产就绪。


## 13. 可执行参考模型证据 — 2026-11-18

已在合并 PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) 中加入有明确边界的单节点 SQLite 参考模型：

- `06-memory-context/reference-model/g_applied_ledger.py`
- `06-memory-context/reference-model/test_g_applied_ledger.py`
- `.github/workflows/g-applied-reference-model.yml`

精确 PR Head 的运行 [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388) 与合并后 main 的运行 [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305) 均已 SUCCESS。合并后运行绑定 main Commit `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf`；Job Log 报告 **8 项测试通过**。

可执行用例覆盖：
1. 完整正向 Gate 且 C 为 `HANDOFF_ACCEPTED` 时创建唯一记录；
2. 相同逻辑身份与相同 Evidence Digest 返回原记录；
3. 相同身份但 Evidence Digest 变化时产生持久化冲突，且不覆盖原记录；
4. `HANDOFF_REJECTED`、`NOT_INVOKED`、`UNKNOWN`、`IN_DOUBT` 均不能创建 Full Applied；
5. 缺失或失败的 Authority/Evidence Gate Fail-Closed；
6. 关闭并重新打开数据库后的读回与同记录重放；
7. 不同逻辑身份创建不同记录；
8. 拒绝未声明的 Identity 字段。

**证据上限：** 该成果是符合性/参考原型，不是生产 G Runtime，也不是 G Owner 的实现验收。它仅使用单个本地 SQLite 数据库，并由调用方提供 Gate 布尔值。它不证明多副本线性化、分布式 Restore-Fencing、后续 I/D 变化后的 Current-Use Revalidation、真实 C/H/COC/I/D/Storage 权威解析、密码学认证或生产持久化拓扑。因此第 12 节状态不变：生产 G Applied Persistence 与跨 Owner Full Applied 仍为 **NOT VERIFIED / NOT FROZEN**。
