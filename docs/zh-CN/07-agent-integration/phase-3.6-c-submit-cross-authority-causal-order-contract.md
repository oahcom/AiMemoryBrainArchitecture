<!-- 源文件：session-c-agent-integration-2026-11-16 / 07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md / Blob 45a48249717c8cddb07ab96197730ef93d406c22 -->
<!-- English companion: ../../en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md -->

# C Owner 合同补充 — C-submit / I-authorization / D-ForgetFence 因果排序

- Owner：Session C — Agent Integration 与实际 Final Request Submit 边界
- 分支：`session-c-agent-integration-2026-11-16`
- 目标配置：`CausalOrderProfile/1.0`
- 目标 H Schema：`bmcp.applied-ack/1.1.0`
- 目标公共 package：`CGH-APPLIED-1.1`（拟议后继版本；尚未跨 Owner 冻结）
- 状态：**C-SIDE CONTRACT AMENDMENT SPECIFIED；coordinator 部署及跨 Owner 接受仍 OPEN**
- 精确源 Blob SHA：`45a48249717c8cddb07ab96197730ef93d406c22`

## 1. C 权威与边界

C 仍是唯一有权产生不可变证据、证明精确的 post-transformation request 已跨越实际且成功的 Provider/Runtime Submit 边界的 Owner。C 不签发 I authorization，不签发 D fence，不因而承担 common coordinator 的运营责任，也不修改 G Applied 状态。

本地 buffer、middleware render、transport ACK、reservation receipt、provider-call intent 或 H receiver durability receipt 均不构成成功 Submit。

## 2. Submit 前必需顺序

1. 固定精确 final request bytes/语义规范形式及 digest；绑定实际 ContextId/ContextVersion、DeliveryId/attempt、InferenceRequestId namespace、FinalRequestBoundaryId、ManagedRegion digest、认证 Principal/Actor/Agent/Adapter/Runtime/session、ScopeBindingSet、适用 EnvironmentRef 和 CapabilityEpoch。
2. 创建 CausalOrderTransactionRef，并从已注册 coordinator 获得持久化 ParticipantIntentRef，绑定精确 request digest、boundary、identity/session、context/delivery 和 capability。该 intent 必须在任何 Provider side effect 前注册，且不等于 Submit 许可。
3. 将精确 intent 绑定到 I 签发的一次性 CommitAuthorizationReceipt；I 在自身 sequencer 中消费一次并返回 IAuthorizationTerminalRef。若撤销胜出则 abort；若授权胜出，后续撤销在 participant 尚未终结前不能越过该 participant 生效。
4. 将同一 intent 绑定到 D 的 ForgetFence 及完整 target/source/ancestor lineage。只有不存在更早 fence 胜出的情况下，D 才返回 DParticipantClearanceRef；任何后续 fence 都必须在该未解决 participant 后等待。
5. Coordinator 验证精确 I/D Owner 引用，并最终确定 ParticipantReservationRef。任何 Owner proof 缺失、过期或不匹配时，不得调用 Provider。
6. 在最终 reservation 的幂等/attempt 合同下，恰好调用 Provider/Runtime 一次；捕获实际 Provider receipt 和实际 InferenceRequestId。
7. 追加 CSubmitOutcomeRef。取得绑定 C、I、D terminal evidence 的 CausalOrderTerminalProofRef。
8. 只有实际 Provider outcome 成功且 terminal proof 确定时，才发出 Final Request Submitted 证据。否则发出 REJECTED / UNKNOWN / IN_DOUBT，并抑制 Full Applied。

## 3. Race 与 barrier 语义

- 在 ParticipantIntentRef 之后请求的 D fence，在 C 的精确 Submit outcome 持久化终结或安全 abort 被权威提交前，不能越过该未解决 intent 生效。
- I receipt consumption 前提出的 I revocation 可以胜出并强制 abort。I 将 receipt 终结为 COMMIT_WON 后，后续撤销的生效必须等待该 participant 终结。
- 若 Provider success 被证明早于后续 effective fence/revocation，则保留历史 Submit 事实；后续 D/I 转换使当前使用资格失效。
- 若 D fence 或 I revocation 在 reservation/authorization consumption 前胜出，C MUST NOT 调用 Provider。
- 若 timeout/crash 后 Provider outcome 未知，participant 保持 IN_DOUBT。C MUST NOT 以新操作重试或报告成功；reconciliation 必须使用同一 transaction/reservation 和 Provider idempotency key。D/I barrier 保持打开。
- 若 coordinator order、Owner evidence、lineage 或精确 digest 无法 reconciliation，C 发出 UNKNOWN，不产生 Full Applied 证据。

## 4. 必需 C 证据字段

在现有 C Final Request Submission Evidence 字段之外，还要求：
- CausalOrderProfileRef、CausalOrderCoordinatorRef、CausalOrderTransactionRef；
- ParticipantIntentRef 及其 coordinator epoch/position；ParticipantReservationRef 和最终 reservation position；
- CommitAuthorizationReceiptRef 和 IAuthorizationTerminalRef；
- ForgetFenceRef/generation、ForgetLineageCoverageRef 和 DParticipantClearanceRef；
- CSubmitOutcomeRef、实际 Provider receipt ref、实际 InferenceRequestId 和 FinalRequestBoundaryId；
- CausalOrderTerminalProofRef、terminal outcome 和 proof digest；
- 精确 request/managed-region digests 及 canonicalization profile IDs。

所有 refs 仍为 opaque 且由对应 authority 签发。C 验证 issuer/integrity 和精确绑定；C 不重新解释 I/D 语义，也不比较它们各自独立的 epoch 数值。

## 5. 禁止的捷径

- 不得用 wall-clock 比较、跨进程本地 monotonic clock 比较、H receiver sequence、ACK 到达顺序或 event-bus delivery 顺序作为因果证明。
- 未完成 participant reservation 和兼容的 I/D clearance 前，不得 Submit。
- Provider outcome 未知时，不得通过自动 reservation expiry 静默释放 D/I barrier。
- Provider outcome 含糊时，不得用新 transaction 重试。
- 不得仅凭 reservation、PermissionDecision、PermissionEpoch、ForgetFenceGeneration、transport ACK 或部分 lineage 声称 Full Applied。

## 6. C 一致性

新增 C-CO-01..10，并与 H36-CO-01..10 对齐：side effect 前 reservation；错误 digest/重放 I receipt；revocation-first；fence-first；fence 等待 reservation；成功 Submit 后发生后续 fence/revocation；crash/Provider outcome unknown；coordinator failover/restore；矛盾 terminal evidence；wall-clock/receiver-order 反转。

状态：**SPECIFIED / NOT RUN**。不声称生产 Provider 集成或 Runtime 一致性已通过。

## 7. 接受边界

该工件规定 C 的集成行为要求。它不批准 I receipt 实现、D barrier 实现、coordinator operator/deployment、H Wire Schema、G Applied predicate 或 Storage durability。在拟议的 CGH-APPLIED-1.1 冻结前，仍须跨 Owner 接受精确的 `CausalOrderProfile/1.0` 和 `bmcp.applied-ack/1.1.0`。

## C Owner 精确版本决议 — CGH-APPLIED-1.1

- A package：`reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- 精确 A package Blob SHA：`9808b31f840606b329f1a794935dfc9c5084d63b`
- 公共合同：`CGH-APPLIED-1.1`
- 因果配置：`CausalOrderProfile/1.0`
- H Schema 目标：`bmcp.applied-ack/1.1.0`

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS**，仅限 C 对实际 final-request/Provider Submit 边界及 C 自有证据的权威范围。

C 接受规范顺序：Provider side effect 前持久化 ParticipantIntent；精确 I receipt consumption/terminal 与 D lineage-bound clearance；coordinator finalized reservation；实际 Provider handoff；不可变 CSubmitOutcome；以及 common terminal proof。C 接受 I COMMIT_WON、D clearance、reservation、H ACK 或 coordinator intent 单独均不能证明 Provider success。只有 C 根据实际观测到的 Provider/Runtime outcome，并包含实际 Provider receipt 和 InferenceRequestId，才签发 CSubmitOutcome；只有确定的 ACCEPTED handoff 才可支持 Final Request Submitted。

例外与闭合条件：
1. Coordinator/operator、durable participant registry 和 monotonic order store 尚未指定/部署/验证。C 的接受以单一 durable transaction/participant 能在 process death、crash、failover 和 restore 后存续且不会释放 IN_DOUBT 为条件。
2. 不能泛化假定 Provider exactly-once 语义。生产激活要求每个 Provider 有专属 idempotency/recovery 合同，证明同一 transaction/key 恢复，且模糊结果后不会作为新操作重试。
3. CSubmitOutcome 和 CausalOrderTerminalProof 必须绑定精确 final request digest、boundary、transaction、reservation、实际 Provider receipt 和 outcome；Provider 结果缺失/含糊时保持 UNKNOWN/IN_DOUBT，并保留 I/D barrier。
4. H 1.1.0 字段映射及密码学/重放互操作仍是候选/未验证；C 不批准 H 实现或密码学治理。
5. G 独占验证并提交 Applied；C 的接受不构成 G 接受、测试、部署或当前使用资格。

不声称 C-CO 已执行或生产实现已验证。本决议仅适用于上述精确 A Blob，不转移任何 CGH-APPLIED-1.0 批准。

## C Owner 精确版本再次确认 — 当前 CGH-APPLIED-1.1 候选

- A candidate Blob SHA：`d4eef4aecf94f922f7933c1e1fec14a69ad17dec`
- Profile：`CausalOrderProfile/1.0`；H Schema：`bmcp.applied-ack/1.1.0`

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS**，仅限 C 的 final-request/Provider 边界及 C 自有证据。

C 再次确认该候选的精确顺序和证据链：Provider side effect 前持久化 ParticipantIntentRef；I receipt consumption 和 IAuthorizationTerminalRef；D lineage-bound clearance 和 fence cutoff；coordinator-finalized ParticipantReservationRef；实际 Provider/Runtime handoff；不可变 CSubmitOutcomeRef；以及 CausalOrderTerminalProofRef。I COMMIT_WON、D clearance、reservation、coordinator intent 和 H ACK 均不证明 Provider success。C 仅依据实际 Provider 观测签发 CSubmitOutcome，其中包括 Provider receipt、实际 InferenceRequestId、FinalRequestBoundaryId 和精确 request digest。UNKNOWN 保持 IN_DOUBT，不得作为新 transaction 重试。

C 接受当前 outage-cutoff safety 规则作为必要 admission invariant：若 COC 不可用，C 不创建或接受新的 protected intent/reservation，也不调用 Provider。C 依赖 I/D 在各自 request cutoff 持久化提交至 COC 前保持本地 admission gate 关闭；C 不从 coordinator 不可用推断不存在 revocation/fence。

例外：(1) COC/operator 和 durable participant registry 尚未指定/部署/验证；(2) Provider 专属同 key 幂等和含糊 outcome 恢复仍待证明；(3) H 1.1.0 互操作及 I crypto/key 治理仍开放；(4) G 接受和 C-CO 执行仍开放/未运行。本决议仅适用于上述精确 A Blob，不转移 1.0 批准。

## C 精确版本接受 — CGH-APPLIED-1.1 recovery-batch 修订

- A package Blob：`4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC Blob：`fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Profile：`CausalOrderProfile/1.0`

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS**，仅限 C 的实际 final-request/Provider 边界和 C 自有 Submit 证据。

C 接受新增 COC-outage recovery-batch 规则，作为必要的 fail-closed 条件。COC 不可用期间，对于无法确认公共因果顺序/cutoff 状态的受保护操作，C MUST NOT 创建/接受新的 protected intent 或 reservation，且 MUST NOT 调用 Provider。C 不从 coordinator 不可用推断不存在 I revocation 或 D fence。恢复后，C 必须核算所有 pre-batch 的 C-owned participant/outcome；Provider 结果未知时保持 UNKNOWN/IN_DOUBT，不得转换为安全 abort，也不得作为新操作重试。

C 接受 recovery batch 不按 I/D 本地时钟对请求排序。C 为每个既有 participant 提供精确不可变 CSubmitOutcome 证据；C 不裁决 I revocation 或 D lineage/fence outcome。

例外：(1) COC、participant registry 和 operator 尚未指定/部署；(2) Provider 专属同 key 幂等和 crash recovery 尚未验证；(3) package 尚未为每项 recovery-batch evidence 固定生产 Wire encoding，该 Schema 由 H 负责；(4) C-CO 和 Provider fault tests 尚未运行。本决议仅适用于上述精确 A/COC Blob 配对，不转移任何 1.0 或此前 1.1 批准。

## C Owner 精确版本决议 — JF-10 prepared participant ↔ COC bridge（Issue #8）

作为一个精确的跨 Owner 接口集合审阅以下决议包：

- A COC 架构：`reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`，分支 `session-a-integration-2026-11-16`，Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`，§§12.1–12.8。
- I JF-10 bridge 处置：`09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`，Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`，§11.2。
- D/Storage 公共 JF-10 v2 recovery protocol：Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`。
- D bridge 决议：`03-memory-brain/forget-fence-operation-and-publication-gate.md`，Blob `5a56c406578fdf257509315eb3f6f3f75456116c`。
- Storage bridge 决议：`reviews/storage-consistency/forget-atomicity-storage-realization-review.md`，Blob `55c01f4512f2e3d8aac767dd004e768ae073178e`。
- H BMCP Wire 映射：`08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`，Blob `1716b23741479740f9e12003cbf2bd1a80c63aab`，§12.10；增量 `bmcp.applied-ack/1.1.0` 候选。
- 本次追加前的 C Owner 合同：Blob `a72a3eb1e5207f67c01f804508311f42db9a6e0a`。

**C 决议：接受精确 JF-10 ↔ COC bridge bundle，但附带 C 自有条件。**

该接受仅限 C 的实际 final-request/Provider side-effect 边界及 C 自有 Submit outcome 证据。不批准 I authorization 语义、D fence/lineage 语义、Storage transaction 语义、COC consensus/deployment 或 H 密码学治理。

### 约束性 C 集成规则

1. 在精确 participant 已有 quorum-committed `JF10_PREPARE_INTENT_REGISTERED`、Storage 签名的 `PreparedParticipantReceipt` 已持久注册为 `JF10_PREPARED_PARTICIPANT_REGISTERED`，且 I owner-final gate 已针对精确不可变 tuple 产生权威 terminal decision 前，C MUST NOT 调用受保护 Provider side effect。C 必须在整个过程中保留相同 operation/digest、participant、policy domain、owner boundary、预分配 Storage XID 和 COC 引用。
2. C 的 Provider invocation 仍是不可逆外部 side-effect 边界。C MUST 将实际观测结果记录为 C-owned `CSubmitOutcome`，绑定精确 final request digest、FinalRequestBoundaryId、transaction/reservation、Provider idempotency key、实际 Provider receipt，以及可用时的实际 InferenceRequestId。COC record、I COMMIT_WON、D clearance、Storage prepared receipt、H ACK 或 reservation 单独均不能证明 Provider success。
3. Provider ACCEPTED 只有在 handoff 证据确定时才是 terminal。Provider REJECTED 只有在确定未 handoff 时才是 terminal。Timeout、进程死亡、响应丢失、Provider 证据矛盾，或无法查询同一个 Provider idempotency key，均保持 UNKNOWN/IN_DOUBT。C MUST NOT 作为新 transaction 重试或 mint 新 XID；应保留相同 participant 和 Provider idempotency key 进行 reconciliation，I/D barrier 继续保持。
4. C 将精确 CSubmitOutcome 和证据引用报告到 COC lifecycle。COC 的 `I_JF10_TERMINAL_DECISION_OBSERVED` 只是对 I 签名决议的观察，不能替代 I 决议。COC 的 `STORAGE_JF10_PARTICIPANT_RESOLVED` 只是对 Storage same-XID 结果的观察，不能替代 Storage 权威 outcome。C MUST NOT 合成任一结果。
5. D fence-first 顺序阻止 C 调用 Provider。若 prepare-intent 早于 D fence cutoff，则 participant 必须留在 D barrier 中，直到 I terminal decision、Storage same-XID resolution、C Provider outcome 和适用 lineage 义务均具备权威证据。UNKNOWN 永不释放 barrier。
6. C 接受 H §12.10 作为五个 bridge record family 的增量 Wire Schema 候选映射，但以精确 tuple 验证及 issuer/signature 验证为条件。H Schema 候选接受不代表已生成 Schema、SDK 互操作、密码算法批准或生产部署。
7. Scope 限定为单一 I PolicyDomain。C 拒绝将多 PolicyDomain 原子性或按域部分聚合表示为一次成功操作。

### C 自有例外与验证门禁

- 每个生产 Provider 都 MUST 证明专属 idempotency 和同 key outcome lookup/recovery；不假定通用 exactly-once 语义。
- C Provider Adapter 在生产使用前，必须证明 participant 到 Provider key 的持久绑定能够跨进程 crash、restart、failover 和 restore 保持。
- C-CO-01..10 与 H-JF10-01..10 仍为 SPECIFIED / NOT RUN；不声称实现或互操作通过。
- C 不批准 COC operator/quorum 部署、I sequencer 实现、D fence 实现、Storage DB/XA 能力、密钥保管/轮换或生产激活。
- 多 PolicyDomain 原子性仍为 BLOCKED / NOT ACCEPTED。JF-10 仍为 P0 OPEN。

这只是 C 对精确 bundle 的独立架构/接口接受。不将任何此前 CGH-APPLIED-1.0 或 1.1 决议转移到其他 Artifact SHA，也不关闭实现、部署或一致性门禁。
