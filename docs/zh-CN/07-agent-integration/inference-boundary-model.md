# Inference Boundary Model（推理边界模型）

**状态：**安全/语义边界 DECIDED；执行细节 CANDIDATE；provider mapping OPEN  
**Owner：**Session C — Agent 集成边界预设计  
**Dependencies：**Session G — Memory Context；Session H — BMCP/Adapter；Session I — consistency and recovery。

## 1. 目的

定义 Brain 管理的 Memory Context 在何种情况下可被视为已应用于 Agent inference request。这样可以避免假设 Brain 能重写正在执行的 model context，也可以防止将 delivery acknowledgements 错误表述为 application。

Inference boundary 是 Agent/Adapter 为某次特定 inference invocation 组装 effective context，并将该 request 提交给 inference runtime 的位置。

## 2. 规范性原则

- **DECIDED：**Brain 对其管理的 Memory Context version 具有权威。
- **DECIDED：**Adapter 在 Agent inference assembly boundary 应用期望的 context。
- **DECIDED：**Changes 在未来的 boundary 生效。
- **DECIDED：**从 Brain 的角度看，in-flight request 是 immutable。
- **DECIDED：**Received、Accepted 和 Applied 是不同状态。
- **DECIDED：**Applied 仅证明 Adapter 在约定的 boundary 应用了指定 version。
- **DECIDED：**Applied 不证明模型的 attention、comprehension、recall 或 behavioral compliance。
- **DECIDED：**Brain 不能覆盖 system/developer instructions、user input、Agent safety policy 或 tool authorization。
- **DECIDED：**Context Remove 不等于 Canonical Memory Forget。

## 3. Boundary sequence

~~~mermaid
sequenceDiagram
  participant B as Brain Context Manager
  participant S as Context Sync
  participant A as Agent Adapter
  participant R as Request Assembler
  participant L as LLM Runtime
  B->>S: Change Set base v to target v+1
  S->>A: Deliver
  A-->>S: Received(delivery id)
  A->>A: Validate scope, version, budget, operations
  A-->>S: Accepted or Rejected
  Note over A,R: Wait for next inference assembly boundary
  R->>A: Prepare request
  A->>R: Apply managed region v+1
  R->>L: Submit immutable request
  A-->>S: Applied(v+1, boundary correlation)
  L-->>R: Response
~~~

Boundary 可以是 prompt builder、middleware hook、request interceptor、context API 或等效机制。逻辑语义不依赖具体实现。

## 4. Context composition 与受保护区域

| Region | Owner | Brain may modify? |
|---|---|---:|
| System instructions | Platform/runtime or Agent deployment | No |
| Developer instructions | Application/developer | No |
| Agent safety/tool policy | Agent/application | No |
| User-originated input | User/application capture | No |
| Brain-managed memory region | Brain defines content; Adapter applies | Yes, only by contract |
| Agent working state | Agent | No absent a separate contract |
| Tool schemas/authorization | Agent/platform | No |

Adapter 必须识别精确的 managed region。如果 Agent 无法隔离该区域，集成就不能声称达到 Tier 1。Memory 必须序列化为不可信数据，绝不能提升为 instructions。

**CANDIDATE：**使用 context ID、version、scope 和 content classification metadata 来界定 managed region。分隔符本身不是安全边界；强制执行属于 Adapter 和 request assembly 的职责。

## 5. Delivery、receipt、acceptance、application

| State/term | Meaning | Evidence |
|---|---|---|
| Prepared | Brain 已生成 delivery artifact | Brain delivery record |
| Delivered | Transport 已将 artifact 交给 Adapter endpoint | Transport result |
| Received | Adapter 确认收到 artifact | Adapter receipt |
| Accepted | Adapter 已验证 scope、version、capability、budget、operations | Adapter acceptance |
| Applied | 精确 target version 已在 inference boundary 的 managed region 中物化 | Adapter attestation |
| Rejected | Adapter 以 typed reason 拒绝 artifact | Adapter rejection |
| Expired | 根据 validity policy，artifact 已不再符合资格 | Brain delivery state |
| Superseded | 更新的权威 version 使该 delivery 过时 | Brain context/delivery record |

Delivered 不等于 Received；Received 不等于 Accepted；Accepted 不等于 Applied。

Adapter MUST NOT 仅因为收到、解析、排队、缓存、追加到未使用的 template，或将 update 转发到上游，就报告 Applied；除非已确认该内容确实在 boundary 处物化到 managed region。

## 6. Applied attestation

逻辑 Applied record 字段：

| Field | Meaning |
|---|---|
| context_id | Brain-managed context identity |
| context_session_id | Target Agent context session |
| target_context_version | 精确应用的 version |
| adapter_id / adapter_instance_id | 经认证、执行应用的 Adapter |
| agent_instance_id | Agent instance |
| boundary_id | Inference assembly hook identity |
| inference_request_id | 可用时的 request correlation |
| applied_at | Adapter application time |
| applied_region_digest | 已物化区域的 optional digest |
| application_mode | Snapshot、delta materialization 等 |
| coverage | 是否覆盖完整 managed region |
| capability_epoch | 执行应用时所依据的 capability declaration |

Digest 是 optional 的，且不得暴露敏感内容；canonicalization 必须有版本。Applied 是 Adapter attestation，不是 provider-side proof。

**OPEN：**inference_request_id 是否必须提供。**CANDIDATE：**若可获得则要求提供；否则要求唯一的 boundary invocation ID。

## 7. Version 和 base 规则

- Brain Context Manager 拥有权威的 context version sequence。
- Adapter 按 context session 维护本地 applied-version watermark。
- Delta 仅当其 base 与 Adapter 已物化的 version 匹配时才能应用。
- 未知 base、gaps 或意外 version 必须触发 rejection/reconciliation，不得猜测。
- 通过 full snapshot 或明确支持的 recovery operation 进行 reconciliation。
- 除非受治理地 reset 为新的 session identity，否则同一 context session 中的 Applied versions 必须单调递增。
- 更新的 context versions 可以 supersede pending deliveries。
- Context Remove 只影响 context entry；除非另有 Forget workflow 获得授权并完成，否则 canonical Memory 仍然存在。

## 8. Delivery state machine

~~~mermaid
stateDiagram-v2
  [*] --> Prepared
  Prepared --> Delivered: transport handoff
  Delivered --> Received: Adapter receipt
  Delivered --> Expired: TTL elapsed
  Received --> Accepted: validation succeeds
  Received --> Rejected: validation fails
  Accepted --> Applied: applied at inference boundary
  Accepted --> Rejected: pre-apply condition invalid
  Prepared --> Superseded: newer version
  Delivered --> Superseded: newer version
  Received --> Superseded: newer version
  Accepted --> Superseded: newer version before apply
  Rejected --> [*]
  Applied --> [*]
  Expired --> [*]
  Superseded --> [*]
~~~

终态 delivery states 为 Applied、Rejected、Expired 和 Superseded。终态失败后的 retry 使用新的 delivery identity，除非 protocol semantics 明确定义了 retry identity。

Transitions：
- Prepared to Delivered：transport 确认 handoff。
- Delivered to Received：Adapter 针对 delivery ID 返回 receipt。
- Received to Accepted：scope/schema/capability/base/budget validation 通过。
- Received to Rejected：validation 失败。
- Accepted to Applied：精确 target version 在 inference boundary 物化。
- Accepted to Rejected：应用前条件变为无效。
- Pending state to Superseded：更新的权威 version 使 artifact 失效。
- Pending state to Expired：validity policy 在应用前到期。

Timeout 既不是 Applied，也不是 Rejected。记录 pending/unknown transport outcome，并按 delivery ID/version 进行 reconciliation。

## 9. Snapshot 和 delta

**CANDIDATE：**
- 当 base continuity 已知时，正常增量更新使用 Deltas。
- Bootstrap、recovery、version gaps、不可信的本地状态或不兼容历史使用 Full snapshots。
- Adapter 在报告 Applied 之前，必须物化完整的 target region。
- 解析 delta 不等于 application；生成的 region 必须在 boundary 处实际使用。

如果某项 operation 无法应用，默认做法是 reject delivery。Partial application 需要明确的 Session G/H semantics、per-entry results，以及不同于 full acknowledgement 的 acknowledgement。在这些内容定义之前，Applied 表示完整的 managed-region application。

## 10. Concurrency 和 inference races

1. Adapter 选择一个 serialization point，用于在 boundary 处物化。
2. Request assembler 为每次 invocation 获取一个 immutable managed-region snapshot。
3. 如果 update 在 snapshot freeze 之前到达，并且通过验证，则可以应用。
4. 如果 update 在 freeze 之后到达，则只能应用于后续 request。
5. In-flight request 绝不能被重新标记为使用更新的 context version。
6. Brain 对并发 context changes 进行序列化；Adapter reject unknown-base deltas。
7. Request retries 记录它们是复用相同 context version，还是组装了更新的 version。

## 11. Offline、reconnect、restart、mismatch

**Adapter offline：**Brain 在 TTL/retention 约束下跟踪 pending delivery。Agent 在没有新鲜 proactive updates 的情况下继续运行。不得作出 Applied claim。

**Reconnect：**Adapter 完成认证，并报告 context/session identity、capability epoch 和最后已知的 applied version。
- Equal version：resume。
- Behind with contiguous history：如果支持则发送 deltas。
- Behind with missing history：full snapshot。
- Unknown/invalid version：full reconciliation；不要信任任意的 client advancement。
- Newer Brain version：过时的 pending deltas 可以变为 Superseded。

**Restart：**可以报告持久化且经过 integrity-check 的 applied state。否则状态为 unknown，在声称 synchronization 之前必须执行 full snapshot。

**Capability change：**递增 capability epoch。重新验证已 accepted 但尚未 applied 的 deliveries。旧 epoch 的 attestations 不能证明新 boundary 下的 coverage。

## 12. Failure isolation

默认情况下，Brain outage 不得导致 Agent execution 失败。只有在 previously applied local memory 仍获授权且符合 retention/revocation 要求时，Agent 才可以继续使用受保护的 native context 和这些 memory。如果无法确认 freshness，Adapter 将其标记为 stale/unknown，由 Agent policy 决定是否使用。

Permission revocation、Forget 或 retention expiry 可能要求本地 context reconciliation。没有 acknowledgement 和明确的 assurance model，Brain 不能假设远端已完成 physical deletion。

## 13. Security

- Authenticate Adapter 并绑定 context/session identity。
- 在每次 delivery 和 reconciliation 时授权 scope。
- 根据 Brain session record 验证 client version。
- 将 memory 视为不可信数据。
- 保护 instruction、user、policy 和 tool regions。
- 优先记录 IDs、versions、digests 和 outcomes，而不是 raw content。
- 确保 offline caches 遵守 Forget、revocation 和 retention。
- 将 Applied 视为可审计的 Adapter assertion，而不是 model behavior 的证明。

## 14. Metrics 和 tests

测量 generation-to-delivery、delivery-to-Received、Received-to-Accepted、Accepted-to-Applied latency；version lag；rejected/expired/superseded rates；snapshot/delta ratio；reconciliation success；boundary coverage；stale-context use；revocation propagation。

Acceptance scenarios：
1. Received 但尚未 Accepted，不是 Applied。
2. 没有 inference request 的 Accepted 仍保持 Accepted。
3. 在 request N 期间到达的 update 最早只能在 request N+1 应用。
4. 错误 target version 的 attestation 被 reject。
5. Delta base mismatch 触发 snapshot reconciliation。
6. version unknown 的 restart 要求 full snapshot。
7. Middleware bypass 不得产生 Applied attestation。
8. Budget overflow 不得产生虚假的 full Applied。
9. Boundary 之前发生 permission revocation 时，必须阻止 application。
10. Context Remove 保持 canonical Memory 不变。
11. Forget 调用独立的 governance workflow。
12. Protected regions 保持不变。
13. Duplicate delivery 是 idempotent。
14. Superseded old version 之后不能被悄然应用。

## 15. Interfaces 和开放问题

| Partner | Required agreement |
|---|---|
| Session G | Context/session IDs, version/base, snapshot/delta, Change Set atomicity, partial-apply policy |
| Session H | Message states, acknowledgement schema, retry identity, timeout, capability epoch, errors |
| Session I | Durable applied watermark, reconnect recovery, audit, retention, Forget propagation |
| Agent framework/runtime | Actual assembly hook, immutable submission point, request correlation, context slot |

**OPEN：**Applied 是否与 request submission 同步发出。**CANDIDATE：**仅在最终 region materialization 完成且 request 已提交到 submission path 后发出。

**OPEN：**Streaming/multi-stage inference 可能在每个 Agent turn 中产生多个 requests。**CANDIDATE：**对每个 inference request boundary 分别 attestation，并使用 turn correlation 将它们关联。

**OPEN：**Middleware 声称最终 request visibility 所需的 evidence，属于 Session H conformance 问题。

## 16. 决策摘要

- **DECIDED：**Inference boundary 是 request-context assembly/commit。
- **DECIDED：**In-flight inference 不会被动态重写。
- **DECIDED：**Delivery、receipt、acceptance 和 application 相互独立。
- **DECIDED：**Applied 标识精确 version 和 boundary；它不证明 comprehension。
- **DECIDED：**Brain 只修改其 managed region。
- **CANDIDATE：**正常同步使用 Deltas；bootstrap/recovery 使用 snapshots。
- **DECIDED：**Unknown base 要求 rejection 或 reconciliation。
- **OPEN：**Wire acknowledgements 和 Adapter conformance 属于 Session H；context authority 仍属于 Session G。

## 17. C Applied 证据生产义务——委托方向决策，2026-11-26

C 拥有 Agent 推理组装边界观测到的事实，不拥有 G 最终 Applied 投影。C 必须为 Full Applied 候选产生两份不同的不可变证据：(1) FINAL_REQUEST_SUBMITTED，证明精确不可变请求跨越最终 Submit 边界；(2) APPLIED_CONTEXT_OBSERVED，证明精确、完整的 Brain-managed Region 存在于该请求中。两份证据必须绑定相同的 context_id、精确 context_version、context_session_id、delivery_id、delivery_attempt_id、Agent/Adapter/Runtime 身份、inference_request_id、final_request_boundary_id/type、adapter_capability_epoch 和 managed_region_id/revision。

证据必须携带版本化规范 Managed Region Digest Profile、期望和观测 SHA-256 Digest、精确 Inventory Digest，以及 COMPLETE Coverage。本地文件写入、缓存 Template 更新、Queue 入队、传输 Receipt 或 Accepted 结果都不能替代这两种最终边界证明。现有 H Schema 1.0.0 仅是候选 Envelope 映射；H 保留 Wire 和签名权威。

C 输出不可变 Outcome Record 引用和 Payload Digest；H 对其进行认证/封装；G 将精确 C/H 引用保存在稳定 DeliveryAttempt 上，并且只有在所有谓词、当前 I PermissionEpoch 和 D ForgetFence 检查通过后，才提交 G AppliedRecord。C 不宣布 G Applied，任何证据都不能证明模型理解。

PASS/FAIL：
- CG-A1..CG-A3 PASS 当且仅当完整身份、两种证据和精确完整 Region 的 SHA-256 Commitment 均存在且匹配；否则 FAIL。
- CG-A4 PASS 当且仅当 C 证据不可变、因果顺序正确并绑定唯一最终请求边界；否则 FAIL。
- CG-A8 PASS 当且仅当本地持久化/物化不能单独被报告为推理边界 Applied；否则 FAIL。

方向由 user-authorized operator (delegated by account owner) 于 2026-11-26 记录。C、G、H 保留精确版本验收权；不授予实现或 Wire 冻结授权。
