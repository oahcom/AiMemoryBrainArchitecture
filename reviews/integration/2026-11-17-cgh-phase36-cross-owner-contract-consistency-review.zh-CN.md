# C/G/H Phase 3.6 跨 Owner 契约一致性复审

- 日期：2026-11-17
- 复审类型：独立跨 Owner 契约审计（不是单纯翻译复审）
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- PR：#28，`docs/bilingual-coverage-completion`
- 精确源基线：
  - C：`07-agent-integration/phase-3.6-final-request-evidence-contract.md`，分支 `session-c-agent-integration-2026-11-16`，Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`。
  - G：`06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`，分支 `session-g-memory-context`，Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`。
  - H：`08-bmcp-protocol/adapter-capability-and-applied-attestation.md`，分支 `session-h-bmcp-protocol`，当前 Blob `0dca3dc5463a02be0e19524811afbae87795baf5`。
- G 相关精确决议锚点：
  - CGH-APPLIED-1.1 candidate A package Blob：`d4eef4aecf94f922f7933c1e1fec14a69ad17dec`。
  - Recovery-batch A package Blob：`4961ffefc0f9920efb8425a9b2a7af42d8f64819`。
  - 配套 COC Blob：`fc3bac39ec64fda68b8cba5e1aada4e719e5acea`。

## 1. 总体结论

**C/G/H 跨 Owner 契约：尚不可冻结。**

六阶段生命周期语义一致，权威边界总体正确：C 生产最终请求/Provider 侧证据；H 负责 Adapter 协议/能力并保留经过认证的 Owner 证据；只有 G 接受 Applied。但 G 最新 CGH-APPLIED-1.1 recovery-batch 决议要求的证据，当前 C producer 合同尚未定义为 C 签发的输出或明确消费的引用集合。H §11.8 已识别新增证据桥接，但仍是候选映射保留条款，不是冻结的 Schema 或已实现 Wire 合同。

这是实质性 P1 契约缺口，不是翻译缺陷。本复审不提升任何 Owner 决议或实现状态。

## 2. 已对齐且成立的跨 Owner 语义

| 主题 | C | H | G | 结果 |
|---|---|---|---|---|
| 生命周期 | 区分 Prepared、Delivered、Materialized、Final Request Submitted、Applied、Execution Started | 区分传输、物化、提交证据和 Applied 证明 | 定义相同六阶段并拥有 Applied | 对齐 |
| 最终提交权威 | 仅在精确变换后请求跨越成功 Runtime/Provider Submit 边界后产生证据 | H 不得推断 C Provider outcome | G 要求 C 证据并验证谓词 | 原则上对齐 |
| Applied 权威 | C 明确不修改 Applied | H 明确不拥有 Applied 接受权 | G 是唯一 Applied 权威 | 对齐 |
| 能力上限 | Tier 2/3、bypass/unknown 不得声称 Full | Tier 1/2/3 能力上限；Full 要求最终请求可观测 | Full Applied 拒绝不完整/未知 coverage | 对齐 |
| 历史/当前使用分离 | 保留历史证据；后续撤销/fence 使当前使用失效 | 后续 Forget/撤销使当前使用失效，不改写有效历史 | 历史 Applied 不可变；独立重新计算当前使用投影 | 对齐 |
| 重复与迟到证据 | 相同 identity/digest 幂等；digest 改变冲突；迟到证据不能回滚 | 相同 identity/digest 与 replay 规则 | 相同 identity/digest 幂等且不得回滚 | 对齐 |
| Forget 顺序 | 顺序未知 => Unknown/抑制 | 不得从接收顺序/时间/ACK 推断跨权威顺序 | 顺序未知 => 不产生新的 Full Applied，并抑制当前使用 | 原则上对齐 |

## 3. 发现项

### XCH-36-001 — C producer 合同未定义 G 的 CGH-APPLIED-1.1 C 证据集

**严重级别：P1 — 冻结阻塞**

G 最新 recovery-batch 修订至少要求：
- 精确的 C Provider receipt 和不可变的 `CSubmitOutcome`；
- 确定的 `CausalOrderTerminalProof`，绑定相同 transaction、request/participant digest、reservation 和 terminal outcome；
- 在任何新的 Full Applied 提升前，提供 recovery-batch 证据、完整 pre-batch participant 枚举/协调结果、Owner high-water attestations，以及 I/D/Storage 各自的 terminal evidence。

当前 C 源文件（Blob `fd2f47...`）要求真实的 Runtime/Provider 分配的 `InferenceRequestId`、成功 Submit 边界和通用 submission outcome，但没有定义 `CSubmitOutcome` 证据对象、实际 Provider receipt 合同，或精确的 1.1 causal-order/recovery-batch 证据绑定与引用。C 当前最新明确的精确版本 Owner 决议仍是 CGH-APPLIED-1.0；该源文件没有记录 C 对精确 1.1 recovery-batch package 的接受。

**必要闭合动作**
1. C Owner 定义 C 所有的 Provider handoff receipt 和不可变 `CSubmitOutcome` 字段、identity、digest、成功/失败/未知语义、幂等及 replay 行为。
2. C 将 outcome 明确绑定到精确 request、FinalRequestBoundaryId、delivery attempt、participant intent/request digest，以及适用时的 causal-order transaction。
3. C 只消费/引用 COC terminal proof 和 recovery-batch/participant 证据，不得自行签发这些证据。COC、I、D、Storage 证据仍分别归其权威所有。
4. C Owner 必须针对当前 1.1 recovery-batch package 发布精确版本决议（或发布 successor package 并重新绑定决议）。

闭合前，G 不能安全地认为当前 C producer 合同已满足完整 1.1 谓词。

### XCH-36-002 — H §11.8 是候选映射，不是冻结或已实现的 1.1 Wire 合同

**严重级别：P1 — 冻结阻塞**

当前 H 源 Blob `0dca3d...` 包含 §11.8，枚举 causal-order、recovery-batch、participant completeness、Owner high-water、I terminal、D lineage/cutoff/effective-position，以及有条件的 Storage same-XID 证据引用。它正确禁止 H 签发或推断 COC、I、D、C Provider 或 Storage outcome，并要求不同顺序域保持独立。

但 §11.8 明确仍是候选保留条款。它说明不能据此证明当前 JSON Schema/SDK 已包含这些字段，并要求 H 在相关 C/G/I/D/Storage 确认后发布精确增量 Schema 版本。G 将 `bmcp.applied-ack/1.1.0` 列为目标，但本次审查没有在 H 源文件中发现该目标已经作为已发布、冻结的 Schema/SDK 实现的证据。

**必要闭合动作**
1. H 发布 1.1 证据桥接的精确版本化 Schema 和 SDK 字段映射。
2. H 提供机器可读的必需/可选/条件字段规则、空集合证明语义、UNKNOWN/IN_DOUBT 处理、完整性覆盖、replay identity 和兼容规则。
3. H 获得 C/G/I/D/Storage 精确版本确认；不得把这些确认解释为权威转移给 H。
4. H 提供可执行的 Schema/序列化/验证 fixture。没有证据前状态保持 NOT RUN。

### XCH-36-003 — 跨 Owner 精确版本决议链不完整

**严重级别：P1 — 冻结阻塞**

G 已在列明例外的前提下接受自身 Applied 谓词和 recovery-batch 前置条件。H 将 1.1 桥接记录为候选。C 当前源文件记录的是 CGH-APPLIED-1.0 决议，并未记录对精确 1.1 recovery-batch 证据配置的接受。因此，最新 G 决议没有形成可证明的 C/G/H 精确版本联合接受链。

**必要闭合动作：** 一个共享 package/version 必须固定精确 C、G、H 源 Blob，以及精确 A/COC 决议 package Blob。每个 Owner 必须在自身权威范围内明确接受同一个 package/version，并列出例外。不得从下游消费者映射或先前 1.0 决议推断接受。

### XCH-36-004 — 1.1 之前的顺序措辞需要明确的取代规则

**严重级别：P2 — 规范歧义**

较早的 G/C 条款引用 Owner commit cursor、可信接收方 receipt sequence，以及通用 boundary timestamp/monotonic sequence。1.1 H 桥接正确规定 COC、I、D、Storage 顺序域相互独立，不得比较或替代；wall-clock、H receiver sequence、消息到达顺序、timeout、ACK 缺失或 reconnect 均不能建立跨权威顺序。

后续 1.1 决议似乎旨在细化较早的通用措辞，但本次审查的源文件集合没有提供一条简洁的优先级声明，明确指出哪些旧顺序规则在 1.1 中被取代。

**必要闭合动作：** G/C/H 发布规范性优先级说明：对于 CGH-APPLIED-1.1，只有指定 profile 下的精确 Owner 签发证据和 CausalOrderTerminalProof 才能建立所需的跨参与方 terminal disposition；本地 sequence 只在本地有效，绝不做数值比较。旧 1.0 行为仅适用于精确的 1.0 package。

### XCH-36-005 — Execution、recovery 和 Forget 竞争证据仍未执行

**严重级别：P1（生产就绪阻塞）；不是翻译阻塞**

C conformance、G-36/CGH 和 H conformance 案例仍为 SPECIFIED / NOT RUN。G 明确表示 coordinator/operator 和 durable participant/order service 尚未指定/部署/验证，且尚未证明 G validator/persistence 消费完整 recovery-batch 证据集。没有声称任何实现或生产通过。

**必要闭合动作：** 执行确定性测试，覆盖 Provider handoff outcomes、same-XID resolution、recovery-cutoff batches、缺失/不完整 participant enumeration、I revocation race、D fence race、Storage terminal visibility/non-publication、replay、digest 改变、reconnect 和 unknown-order suppression。附加持久化证据和 Owner 签字。合同接受不等于 Runtime 验证。

## 4. 权威与证据归属矩阵

| 证据 | 生产者/权威 | H 职责 | G 职责 |
|---|---|---|---|
| 最终不可变请求 / Provider handoff / CSubmitOutcome | C + 实际 Runtime/Provider receipt | 认证 envelope 并保留 opaque evidence | 验证；不得合成 |
| CausalOrderTerminalProof / recovery batch | COC coordinator/order authority | 验证 Schema/完整性并保留引用 | 新 Full Applied 前必须具备 |
| I authorization terminal / sequencer / revocation cutoff | I | 保留认证引用 | 验证；不得推断策略 |
| D lineage / fence request cutoff / effective position | D | 保留认证引用 | 验证；不得推断 fence |
| Storage same-XID terminal resolution / visibility | Storage | 保留认证引用 | Storage 参与时必须要求 |
| Adapter capability / ACK / session / Wire integrity | H | 拥有并认证 | 消费；不得仅凭 ACK 提升 Applied |
| Applied fact 和 current-use projection | G | 无权威 | 唯一所有者 |

## 5. H 当前源 pin 修正与旧报告取代

已重新读取当前 H Owner 源文件，Blob 为 `0dca3dc5463a02be0e19524811afbae87795baf5`。当前 EN 和 zh-CN companion 均固定到该 Blob，并包含 §11.8。本 PR 先前发布的 H parity 报告使用旧源 SHA `db59b63e322d7255b8b400f47859dcac32bb3027`；该报告由本次当前源复审取代，不得再作为当前 H 源修订的证据。

## 6. 最终判定

- C/G/H 六阶段生命周期与核心权威边界语义：**PASS WITH ENUMERATED EXCEPTIONS**。
- CGH-APPLIED-1.1 recovery-batch 证据在 C/G/H 之间的完整性：**BLOCKED**。
- H 1.1 Schema/SDK 冻结：**尚未成立**。
- 精确版本 C/G/H 联合接受：**尚未成立**。
- Runtime/conformance/production 验证：**NOT VERIFIED / NOT RUN**。
- PR #28 继续保持 Draft/Open；本复审不授权合并。

本报告任何发现均不提升 Owner 状态，不批准实现，不证明全局 Forget 完成，也不证明物理擦除。
