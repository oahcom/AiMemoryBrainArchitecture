# Phase 3.8.23 — C 精确消费方决议：G Applied Persistence Identity Join

- 角色：模拟 C Owner 的委托审查；不是独立人类 Owner 签署。
- 决议：对以下 C 所有身份语义 **ACCEPT WITH ENUMERATED EXCEPTIONS（附明确例外接受）**。
- G 目标 EN Blob：`bd297873bc1e593280484a43cb44b56058d9c4ff`
- G 目标 zh-CN Blob：`82553a47fae2d5e796e0742b46231afe465e75b2`
- CSubmitOutcome 1.0.1 Schema Blob：`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C Provider Submit Outcome 规范合同 Blob：`819705037da89834e10b6dd2ec6e66c1b8c70886`
- C Final Request Evidence Blob：`fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`
- C causal-order addendum Blob：`45a48249717c8cddb07ab96197730ef93d406c22`

## 1. 决议范围

本决议仅审查上述精确 G Phase 3.8.22 Blob 中的 C/G 身份连接。它不接受 H wire mapping、COC/Storage restore 语义、I/D 顺序、G 持久化实现或全局 Applied 冻结。任一 G Blob 发生变化，本决议即失效。

## 2. 逐字段决议

### 2.1 CProviderAttemptIdentity — ACCEPT

G 元组：
`(issuer_authority_ref, sequence_namespace_ref, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, IdempotencyNamespaceRef, IdempotencyKeyRef, RequestDigest)`

C 确认 CSubmitOutcome 1.0.1 支持这些语义字段：
- `issuer_authority_ref` + `sequence_namespace_ref`：签发方及 Owner Ledger 序列命名空间。该序列只在签发方权威记录范围内有效，不是全局序列。
- `ProviderAttemptRef` + `ProviderAttemptGeneration`：稳定逻辑 Attempt 及显式 Generation。
- `ProviderRef` + `ProviderAccountRef`：Provider 与经认证的 Account/Tenant 范围。
- `IdempotencyNamespaceRef` + `IdempotencyKeyRef`：稳定 Provider Key 命名空间与 Key 引用。
- `RequestDigest`：精确不可变最终请求 Digest。请求 Digest 改变即属于不同 Provider Attempt 范围，禁止沿用旧幂等身份重试。

C 要求消费者保留 C 签发的精确引用并比较完整元组；禁止显示名称归一化、推断 Account 或重建 Key。

### 2.2 COutcomeRecordIdentity — ACCEPT

G 元组：
`(issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

C 确认该元组是不可变 Ledger Observation 身份，与 ProviderAttempt 身份不同。`payload_digest` 和 `OutcomeEvidenceDigest` 是内容完整性值，不是身份字段。

相同 Record Identity + 相同 Payload Digest + 相同不可变元组 = 精确重放。相同 Record Identity 但 Payload Digest 或不可变元组改变 = 完整性冲突，必须隔离且不得晋升。C Record Sequence 仅在自身 Issuer/Sequence Namespace 内有序；消费者不得与 COC、I、D 或 Storage 位置进行数值比较。

### 2.3 RequestDigest 与 Digest 分域 — ACCEPT

`RequestDigest` 纳入 ProviderAttempt Identity，是因为 C 的 Provider 幂等 Key 受 Provider/Account/Endpoint/Model 语义及不可变请求 Digest 约束。这不允许将 `payload_digest`、`OutcomeEvidenceDigest`、H P0 Digest、H Receipt Digest、COC Participant Digest 或 G EvidenceSetDigest 放入 GAppliedIdentity。

C P0/Object Digest 与 H Envelope P0 Digest 属于不同密码学域。Digest 不能替代签发方认证、Ledger 纳入证明、语义结果验证或精确 Source Record Identity。

### 2.4 迟到 Receipt / Successor Observation — 有条件 ACCEPT

C 接受在同一 ProviderAttempt Identity 下追加 Successor Observation，但必须满足：
1. 每条 Successor 都有新的不可变 COutcomeRecordIdentity 和 C Owner-Ledger 位置；
2. 通过适用的 `PriorObservationRef`、`SupersedesObservationRef` 和/或 `ReconciliationParentRef` 建立精确 lineage；
3. Provider/Account/Key/Request Digest/Attempt Generation 保持不变；
4. C 语义明确它是 lookup/reconciliation/late receipt，而不是第二次物理发送。

Successor 可以丰富同一逻辑 G Applied Identity 的 Evidence Revision，但不得改写原记录，也不得为逃避 UNKNOWN/IN_DOUBT 而创建新 ProviderAttempt。

### 2.5 UNKNOWN / IN_DOUBT / Retry — ACCEPT

C 确认 UNKNOWN 与 IN_DOUBT 均为非终态。恢复必须查询/协调同一 Provider Idempotency Key 与精确 Request Digest。禁止 retry-as-new、Key 轮换、Account/Region/Model failover、SDK 自动重试、Redirect 或 Transport Reconnect 绕过 C Egress Gate。若 Provider 不支持权威幂等或查询，歧义必须保持 IN_DOUBT，并禁用自动重试。

只有包含必要 Provider 与 Participant 证据的确定性 C `HANDOFF_ACCEPTED` 才有资格进入 G Full Applied 评估。C Outcome 本身绝不等于 G Applied。

## 3. 例外与开放依赖

1. H 必须接受并实现独立的 H Delivery Evidence Mapping；C 的接受不批准 H Schema 或 Validator。
2. 未来 H Schema/Validator 若重复承载 C 所有字段，C 必须重新审查，确保与不可变 C Object 精确相等，且不把 Provider Truth 转移给 H。
3. COC/Storage 必须独立接受 G Participant/GID/Restore 连接。
4. 本委托审查不是独立人类 C Owner 批准、Provider 集成证据或 Runtime 符合性证明。

## 4. 结论

**C 身份语义：针对精确 G Phase 3.8.22 Blob 接受，附上述条件与例外。C/H Wire Interoperability：未接受/未验证。G Persistence 实现：未验证。全局 Applied Freeze：NO。Production Activation：NOT AUTHORIZED。**
