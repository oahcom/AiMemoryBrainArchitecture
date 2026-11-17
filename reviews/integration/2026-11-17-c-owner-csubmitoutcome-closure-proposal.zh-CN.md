# C Owner 闭合提案 — 面向 CGH-APPLIED-1.1 的 Provider Receipt 与不可变 CSubmitOutcome

> **已被后续 Owner 工件取代（仅作为审计轨迹保留）。** C 已针对精确 recovery-batch package 发布 ACCEPT WITH ENUMERATED EXCEPTIONS 决议，并发布 CSubmitOutcome 1.0.1 规范合同/Schema。当前权威工件为：C Phase 3.6 addendum Blob 45a48249717c8cddb07ab96197730ef93d406c22；C Provider Outcome 规范合同 Blob 819705037da89834e10b6dd2ec6e66c1b8c70886；CSubmitOutcome 1.0.1 Schema Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda。本提案不再代表当前 Producer 合同缺口。

- 日期：2026-11-17
- 状态：**提交 C Owner 审阅的提案 — 不是 Owner 决议**
- C 源基线：`07-agent-integration/phase-3.6-final-request-evidence-contract.md`，Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`。
- G 决议基线：recovery-batch A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`；COC companion Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`。
- H 候选基线：`08-bmcp-protocol/adapter-capability-and-applied-attestation.md`，Blob `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`，§§11.8–11.9。
- 目的：提供范围明确的 C Owner 修订提案，闭合 Producer 侧缺口，同时不把 COC、I、D、Storage 或 G 的权威转移给 C。

## 1. 请求 C 作出的决议

C 应审查并在接受后发布精确版本 Owner 补充规范，定义：
1. 指向实际 Provider/Runtime handoff receipt 的 C 签发引用（`c_provider_receipt_ref`）；
2. 不可变的 C 自有 Submit outcome 记录（`c_submit_outcome_ref` / `CSubmitOutcome`）；
3. 将该 outcome 与已提交请求及相关 participant intent 精确绑定的 identity/digest；
4. 确定性的 ACCEPTED / REJECTED / UNKNOWN 语义及其 Applied 资格后果；
5. 追加式修正、幂等、冲突、replay 和 recovery 行为；
6. C 接受的精确 1.1 package/version 及列明例外。

本提案不是 C 批准，不得记录为 C 已接受。

## 2. 建议的权威边界

- **C 拥有：** 观测其集成路径上的真实 Provider/Runtime handoff；验证 Provider receipt；签发并保护不可变 CSubmitOutcome；将其关联到精确 final request 和 participant intent。
- **Provider/Runtime 拥有：** 在该边界分配的底层 Provider/Runtime receipt 和 request identity。C 可以签发经过认证的引用/证明，但不得伪造 Provider 事实。
- **COC 拥有：** causal-order transaction、reservation、terminal proof、recovery-batch 完整性及 participant-set reconciliation。C 只能绑定/引用这些对象，不得签发。
- **I 拥有：** authorization terminal evidence、sequencer position、revocation cutoff，以及任何 I 自有 pending gate release。
- **D 拥有：** lineage coverage、ForgetFence request cutoff/effective position，以及任何 D 自有 pending gate release。
- **Storage 拥有：** Storage 参与时的 same-XID resolution 和 terminal visibility/non-publication 证据。
- **H 拥有：** BMCP envelope/schema/ACK/capability 传输，以及对 Owner 签发证据的认证保留。H 不得签发 C outcome 或 Owner gate release。
- **G 拥有：** Full Applied 决策、durable Applied fact 和 current-use projection。G 验证完整证据集；任何 C 证据都不能直接改变 Applied 状态。

## 3. 建议的 CSubmitOutcome 语义合同

以下是最低语义合同。精确字段 Schema 由 C Owner 批准或修订；除 §11.9 已存在的 H 候选引用外，本提案不冻结字段名称。

### 3.1 必需绑定

C 签发的 outcome 和 Provider receipt 引用必须绑定：
- Runtime/Provider 实际分配的 `InferenceRequestId`；
- 精确 `FinalRequestBoundaryId` 及 boundary type/profile；
- 精确的变换后 request digest 和 canonicalization/digest profile；
- 若请求携带 managed context，则绑定精确 `ContextId/ContextVersion`、`DeliveryId/DeliveryAttemptId`；
- C 已要求的认证 Agent/Adapter/Runtime/Session 绑定；
- 精确 participant/request identity，以及 participant 属于 COC transaction 时的 causal-order transaction 引用；
- Provider/Runtime receipt identity、证据签发者、完整性/签名/key 引用、Schema version 和 audit/correlation 引用。

本地 render、本地队列接受、中间件 callback、H transport ACK、Adapter materialization receipt、timeout 或 COC recovery observation 均不是 Provider receipt，不能替代。

### 3.2 Outcome 枚举与含义

| Outcome | 必需含义 | Applied 后果 |
|---|---|---|
| `ACCEPTED` | 经过认证的 Provider/Runtime 证据证明精确请求已成功 handoff | 只能满足 C Provider outcome 谓词；绝不直接代表 Applied |
| `REJECTED` | 经过认证的 Provider/Runtime 证据证明在成功 handoff 前被确定拒绝 | 不得支持 Full Applied；保留不可变负面 outcome |
| `UNKNOWN` | handoff 结果无法确定、receipt 缺失/含糊或证据冲突 | Participant 保持 IN_DOUBT；不得 Full Applied；受保护当前使用继续抑制 |

除非约定的权威 Provider/Runtime handoff 边界并有必需 receipt 支持，否则成功的本地 submit 调用并不足够。C 必须定义 retry 是产生新的 InferenceRequestId、新 outcome identity，还是关联的 superseding attempt；不得静默改写既有 outcome。

### 3.3 不可变性与身份

- CSubmitOutcome 签发后只追加、不可变。
- 其 identity 必须绑定精确 request、boundary、participant/request identity 和 evidence kind。
- 相同 identity + 相同 canonical digest 为幂等，并返回原 disposition。
- 相同 identity + digest 改变为 CONFLICT 并隔离；禁止 last-write-wins。
- 修正通过关联的新 superseding record 完成；禁止原地修改。
- 被 supersede 的 request/session/attempt 证据只能保留为历史，不能重新绑定到新 request 或 capability epoch。
- Provider 证据缺失、过期、未认证或矛盾时必须为 UNKNOWN/IN_DOUBT，绝不能推断 ACCEPTED。

## 4. COC 与 recovery-batch 集成

C 不得创建 `CausalOrderTerminalProof`、`recovery_batch_ref`、participant-set completeness attestation、owner high-water attestation、participant reconciliation entry 或 I/D/Storage terminal evidence。

C 应当：
1. 当 participant 存在时，将 CSubmitOutcome 绑定到精确 COC transaction/participant/request digest；
2. 为 C participant entry 发布 C 签发 outcome 引用及 digest；
3. 保留 C Provider outcome 与 COC transaction terminalization 的区别；
4. 接受只有所有必需 participant outcome 均确定且完成 reconciliation 后，才可能存在 COC terminal proof；
5. C outcome 为 UNKNOWN 时保持 IN_DOUBT；COC observation 不得将其变成 ACCEPTED；
6. 永远不得释放 I/D Owner-local gate。只有 I 或 D 才能签发自己的 `owner_gate_release_attestation_ref`。

C Provider ACCEPTED 是 C participant 确定化的必要条件，但不足以证明整个 COC transaction 已 terminal，也不足以让 G 接受 Applied。

## 5. 必需负面案例

所有案例在附加可执行 fixture 和持久化工件前均保持 **SPECIFIED / NOT RUN**。

| ID | 场景 | 预期 C 处置 | 禁止行为 |
|---|---|---|---|
| C-CO-01 | 实际 Provider receipt 证明精确 request 已接受 | 不可变 ACCEPTED CSubmitOutcome | C 直接标记 Applied |
| C-CO-02 | Provider 在 handoff 前确定拒绝 | 不可变 REJECTED outcome | 当作已接受提交 |
| C-CO-03 | Provider receipt 缺失或 timeout 导致 handoff 含糊 | UNKNOWN / IN_DOUBT | 从 timeout 或本地调用推断接受 |
| C-CO-04 | Receipt request ID 或 digest 与 C final request 不匹配 | Reject/quarantine；UNKNOWN | 将 receipt 绑定到另一个 request |
| C-CO-05 | 相同 outcome identity 和 digest 重放 | 幂等，返回原结果 | 重复提升 |
| C-CO-06 | 相同 outcome identity 但 digest 改变 | CONFLICT / quarantine | Last-write-wins |
| C-CO-07 | supersede request/session 后收到迟到 receipt | 仅历史；不回滚当前指针 | 重新绑定旧 receipt |
| C-CO-08 | C outcome ACCEPTED，但 I/D/Storage participant 仍 pending | C 保持 ACCEPTED；整体 transaction 仍 IN_DOUBT | 声称 participant terminal proof 或释放 gate |
| C-CO-09 | 有 COC recovery observation，但没有 C Provider receipt | C outcome UNKNOWN | COC 替代 Provider 证据 |
| C-CO-10 | I/D owner gate release 缺失或由错误 Owner 签发 | Gate 保持关闭 | C/H/COC 合成 REOPENED |

## 6. C Owner 精确版本决议检查清单

记录接受前，C 必须核验：
- 固定精确 C 源 Blob 和精确 H §11.9 源 Blob；
- 固定精确 G recovery-batch A/COC package 配对；
- 明确 C 自有 Provider receipt/outcome Schema 与语义；
- 将 C 证据关联到精确 request 和 participant intent/digest；
- C 不拥有 COC terminal proof、I/D gate release、Storage outcome 或 G Applied；
- UNKNOWN 和证据缺失均 fail closed；
- C conformance 案例和实现状态保持准确标记。

**拟议决议模板（必须由 C Owner 完成，不由本审查者填写）：**
- 决议：PENDING C OWNER REVIEW
- 精确 package Blob(s)：由 C 固定
- 接受的 C 自有条款：由 C 列明
- 例外/依赖：由 C 列明
- C-CO-01..10：执行前为 SPECIFIED / NOT RUN
- 实现/Runtime：有证据前为 NOT VERIFIED

## 7. 非声明

本提案不构成 C Owner 批准、G Applied 接受、H Wire/Schema 冻结、I 授权批准、D Forget 闭合、Storage 拓扑/原子性、COC 部署、实现正确性、Runtime 一致性、全局 Forget 完成或物理擦除证明。
