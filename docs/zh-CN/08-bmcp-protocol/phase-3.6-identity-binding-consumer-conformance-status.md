# H — Phase 3.6 身份绑定消费者与一致性状态

- 文档 ID：H36-IDENTITY-CONSUMER-STATUS
- Owner：Session H — BMCP Protocol
- 源分支：`session-h-bmcp-protocol`
- 源路径：`08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md`
- 精确源 Blob SHA：`8afb914731a34d8ab44331f54f1f39bfd8ec37ce`
- 源状态：**协议绑定技术设计 JOINT-DECIDED；消费者 Owner 验收 OPEN；治理批准 GOVERNANCE-BLOCKED；H36 NOT RUN**
- 对应文件状态：**双语阅读对应文件；不改变源决策状态**
- English companion: [English](../../en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md)
- 范围：仅覆盖 H 所有的协议绑定与一致性证据。本记录不是外部治理批准，也不构成下游消费者签署验收。

> 源快照说明：源文件 §1 记录的是历史发现时的基线。重新读取当前 H 分支后，受保护操作绑定文件的当前 Blob 为 `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`，而非下表历史记录中的 `9845c97ac43d7888732afafe12e28850ec02add8`。本译文保留源记录的历史事实；该差异登记为当前性问题，不静默改写历史记录。

## 1. 实时源基线

| 工件 | 分支 | 发现时源 HEAD | 路径 | Blob SHA |
|---|---|---|---|---|
| H 受保护操作绑定 | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` |
| H 协议一致性矩阵 | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/protocol-conformance-matrix.md` | `075b2ac6ebe9bda4ec83de04fad07e8027e6a440` |
| H ACK/目标绑定 | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md` | 已确认当前路径；本记录不改变其语义 |
| I 联合信任策略 | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| B 类型化身份闭环 | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |

## 2. 决策语义保持

BIH36-JD-01..17 保持不变。H 保留以下协议含义：

- 对 issuer、principal、ActorRef、workload、audience 和 session，权威来源是受保护的 verifier/transport 上下文，而不是不可信 Payload。
- 已认证的 channel/session 绑定、消息完整性和授权是三个不同概念。
- ACK 证据必须绑定到已认证的 Adapter 实例、Agent/runtime、全新的 RuntimeSessionRef、ActorRef、operation/delivery/forget 身份、精确 Scope 角色、CapabilityEpoch、PermissionEpoch、适用的 ForgetFence、证据摘要和不可变 ACK ID。
- 相同 identity+digest 的 ACK 重复提交必须幂等；相同 ID 但 digest 不同属于冲突。
- D/G/I 分别在各自权威 sequencer 上排序接受。H ingress receipt sequence 仅是证据，不得与 Owner cursor 或本地墙钟时间进行数值比较。
- Reconnect 必须重新认证，重新验证 issuer/workload/capability/PermissionEpoch/ForgetFence，抑制陈旧状态，协调日志，然后才允许恢复。
- 未知、格式错误或不支持的必需安全字段必须 fail closed；不得降级，也不得回退信任 Payload。

本状态记录不提出任何技术语义变更。

## 3. H 一致性测试清单

保留现有 H36 矩阵，不缩减测试范围。以下 18 项全部为 **已定义 / NOT RUN**。

| 测试 ID | 场景 | 必需结果 | 执行环境 | 命令 | 输入/实际结果 | 日志/证据 | 状态 |
|---|---|---|---|---|---|---|---|
| H36-01 | Payload 中伪造 PrincipalRef | 受保护 Principal 保持权威；拒绝不匹配 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-02 | 伪造 ActorRef | 拒绝调用方自行创建或不匹配的 ActorRef | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-03 | 伪造 ProducerRef | 要求已认证 workload 映射到已注册 Producer | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-04 | 未知 Issuer | 在 Principal 解析前拒绝 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-05 | Issuer/key 已撤销 | 拒绝；使受影响 session 失效并执行协调 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-06 | Credential 已过期 | 在 reconnect 和受保护边界拒绝 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-07 | Delegation 已过期 | 拒绝；不得继续以 grantor 身份行动 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-08 | Delegation 已撤销 | 拒绝并要求当前 PermissionEpoch | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-09 | PermissionEpoch 陈旧 | 拒绝受保护操作 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-10 | 跨 Scope 访问 | 缺少 I 明确批准的 grant 时拒绝 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-11 | 跨 Environment 访问 | 缺少精确 bridge/grant 时拒绝 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-12 | 已认证 Principal 与 Payload ActorRef 不匹配 | 拒绝/隔离并审计 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-13 | 旧 Session ACK 重放 | 仅作为历史记录；不得修改新 session 状态 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-14 | 撤销期间 Reconnect | 在重新取得 trust/epoch/fence 并完成协调前不得恢复 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-15 | 未授权 Forget Operation | 在修改 target/fence 前拒绝 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-16 | ACK ID 使用不同 digest 重用 | IDEMPOTENCY_CONFLICT；状态不变 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-17 | 缺少必需 Scope/Environment | 拒绝；不得使用 wildcard/default | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |
| H36-18 | 协议 major downgrade | VERSION_UNSUPPORTED；不得削弱认证 | 未提供 | 未提供 | 未执行 | 无 | NOT RUN |

### 必须追加的 H36-SR 测试 — 同样 NOT RUN

§10.6 的追加测试仍属于范围，不能省略：

1. Channel binding 不匹配。
2. 同一消息跨 session/audience 重放。
3. Nonce 重用。
4. Canonicalization 中重复 key 造成歧义。
5. 缺少/未知 Operation Requiredness Registry profile。
6. Sender 隐去适用的 EnvironmentRef。
7. 跨 Adapter 的 ACK ID 冲突。
8. 相同 ACK ID 但 digest 不同。
9. ACK 到达与 revocation/fence advance 竞争，且覆盖两个先后顺序。
10. Adapter 实例替换后的 reconnect replay。
11. 旧有效 session 下的 capability downgrade。
12. I sequencer/epoch 读取与提交竞争；以及 I36-SR-07 要求的 multi-domain coordinator 故障场景。

没有提供执行环境、命令、fixture、预期/实际输出、日志或签名测试工件。没有任何测试可标记为 PASS 或 FAIL。

## 4. 消费者验收

阅读 H 协议文档或消费 BMCP 消息，不构成 Owner 验收。源文件的原始发现快照中，没有发现任何消费者针对精确 H36/BIH 契约版本作出的明确 Owner 验收。

| 消费者 | H 提供的契约字段/必需行为 | 消费者 Owner | 验收状态 | 所需证据 |
|---|---|---|---|---|
| C Agent Integration | 已认证 Agent/runtime 与 Adapter 身份；final request 边界；session/epoch/fence；拒绝 Payload 身份不匹配及不支持的 capability | C | OPEN | C Owner 验收必须绑定 H 契约 commit 和 final-request enforcement |
| D Memory Brain | 已认证 ACK 身份、operation 和 target 绑定；Owner 本地 ForgetFence 排序；旧 session/已撤销 ACK 仅保留历史意义 | D | OPEN | D Owner 验收及 D sequencer 验收证据 |
| E Memory Compiler | 已认证 Producer/Adapter 绑定；ingress receipt 与幂等；publication 时检查 permission/fence | E | OPEN | E Owner 在 ingress/publication 边界的验收 |
| F Memory Runtime | 已认证 retrieval principal/adapter/session；当前 permission 和 revocation；抑制陈旧候选 | F | OPEN | F Owner 在 candidate emission/cache 边界的验收 |
| G Context Manager | 已认证 Adapter ACK；ContextVersion/Delivery/session 绑定；PermissionEpoch 与撤销排序；reconnect/迟到 ACK 行为 | G | OPEN | G Owner 对 Applied 状态转换的验收 |
| H BMCP | Wire envelope、受保护 verifier context、channel binding、requiredness、ACK 和 reconnect | H | 技术设计 JOINT-DECIDED；未记录独立消费者验收 | 不声称存在独立 H-session 签名或运行时证明 |
| Storage/Consistency | 已认证 commit context，以及 durable visibility 边界上的当前 PermissionEpoch/fence | Storage | OPEN | Storage Owner 对 protocol-to-storage 绑定的验收和 durable transaction 证据 |
| A Integration Registry | 精确 H source ref/status 登记；不得从工件存在推断验收 | A | 作为登记活动为 OPEN；不是批准方 | A 可登记 Owner 证据，但不能代替消费者批准 |

所有未被明确验收的消费者侧身份字段仍未获验收。本记录没有证据证明各消费者端到端接受 PrincipalRef、ActorRef、ScopeRef、EnvironmentRef、Producer/Adapter 身份、已认证 transport binding、PermissionEpoch 校验、revocation、伪造 Payload 拒绝以及 Unknown/Unsupported 行为。

## 5. B/I/H 确认与治理边界

- B domain type 确认：委托形成的联合技术基线；不声称存在独立 B-session 签名。
- I governance 确认：技术策略基线已决定；外部批准仍为 GOVERNANCE-BLOCKED。
- H protocol binding 确认：委托形成的联合技术基线；不声称存在独立 H-session 签名。
- 跨模块技术一致：仅 B/I/H。
- 消费者验收：C/D/E/F/G/Storage 为 OPEN；A 仅负责登记。
- H36 执行：NOT RUN。
- I36 执行：NOT RUN。
- Fact/Claim ADR-001 仍独立处于 ADR-BLOCKED。

## 6. 退出标准

只有在已识别的 build 上执行全部必需 H36 和 H36-SR 测试，并保留已认证 fixtures、预期/实际结果、非敏感日志及 Owner 复核后，H36 才能标记为 conformant。跨模块消费者验收必须由每个消费者 Owner 明确作出。外部治理批准必须由指定治理权威提供，不能从本 commit 推断。本记录不授权合并任何分支。

## 7. 消费者验收状态更新 — 2026-11-16

§4 表格是原始发现快照。以下当前 Owner 工件为对应消费者提供了设计层验收证据，仅对这些消费者取代此前的 OPEN 状态：

| 消费者 | Owner 验收工件 | Blob SHA | 当前设计验收状态 |
|---|---|---|---|
| D | `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md`，位于 `session-d-memory-brain-2026-11-16` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | DESIGN-ACCEPTED |
| E | `04-memory-compiler/phase-3.6-bih-identity-consumer-acceptance.md`，位于 `session-e-memory-compiler-2026-11-16` | `6f4100618695fcf971560fb784f7887a72798c96` | DESIGN-ACCEPTED |
| H（自身消费者边界） | `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md`，位于 `session-h-bmcp-protocol` | `ccbac2d30234df9b910565a7326d100d11a6494e` | DESIGN-ACCEPTED |
| Storage | `reviews/storage-consistency/phase-3.6-bih-identity-consumer-acceptance.md`，位于 `session-storage-consistency-forget-atomicity-2026-11-16` | `ec8e49d0d11c72d37ad0c291611a96a1122ba6f5` | DESIGN-ACCEPTED |

仍为 OPEN：C、F、G。A 仍仅负责登记。这些验收只覆盖设计语义；运行时实现和一致性仍为 NOT VERIFIED / NOT RUN。I 外部治理批准仍为 GOVERNANCE-BLOCKED。JF-10 仍为 P0 OPEN，且 H 不接受当前拆分的 Phase-B/Phase-C 候选方案符合 I36-SR-02。

本状态更新不改变 BIH36-JD-01..17，不声称存在人工签名，也不关闭 G6/G7/G10。
