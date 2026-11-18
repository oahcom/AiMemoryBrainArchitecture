# RFC-IDE-001 — 幂等身份元组契约

- 契约 ID：RFC-IDE-001
- 版本：1.0.0
- 状态：PROPOSED。核心语义以 DECIDED 提案提交评审；保留期限与运行参数仍为 CANDIDATE / TO_VALIDATE。
- 英文对应：reviews/contracts/RFC-IDE-001-idempotency-identity-tuple.en.md
- 消费者：Event Store、SQLite Event Store Adapter、Receipt 持久化/恢复及后续幂等写入 API。
- 权限边界：定义逻辑身份与重放语义；不选择物理数据库、事务拓扑、具体 Schema、加密方案或生产保留策略。

## 1. 目的

精确定义一次追加请求在何种身份条件下才算此前请求的重试。契约防止不同 Producer 或授权 Scope 之间意外去重，也防止同一个 Key 被不同内容复用时错误返回成功。

## 2. 类型化输入

幂等追加由以下三个相互独立的值判定：

1. **Producer Identity（谁发起操作）。** 稳定、经过认证、类型化的逻辑 Producer 主体身份，拥有自己的重试命名空间。它不是显示名称、进程 ID、连接 ID、用户自填标签，也不是若干字段的部分匹配集合。如果 Producer 模型区分主体与 Producer 安装/实例，必须由身份归属契约明确其类型及组合方式；实现不得自行猜测实例身份是否参与。
2. **Scope（授权边界）。** 经过规范化的类型化 Scope 引用；Producer 必须在该 Scope 下获得追加授权，操作及其 Receipt 也仅在该边界内可见。Scope 不能从 Key 推断，也不能替代授权检查。每次请求（包括重试）在披露 Receipt 前都 MUST 重新检查当前授权。
3. **Idempotency Key（调用方选择的重试句柄）。** 由 Producer 生成的不透明、非空且有长度上限的值。它仅在下文定义的命名空间内有意义，不要求全局唯一，也不携带任何授权能力。

Digest 是幂等契约覆盖的规范化请求 Payload 的密码学摘要。它与身份元组共同比较，而不是替代身份元组。规范化规则及摘要算法/版本必须由 Event Store Payload 完整性契约固定；本 RFC 不擅自选择。

## 3. 身份命名空间与重放判定

**DECIDED 提案——精确命名空间：**

    IdempotencyNamespace = (ProducerIdentity, Scope, IdempotencyKey)

该元组必须类型化，但 Scope 身份/相等域目前为 **CANDIDATE / TO_VALIDATE**，尚不具规范性。权威 Scope 字段（包括 `scope_id`、`scope_kind` 和/或 `namespace_key` 中哪些字段参与）、namespace/authority 限定、规范化规则及兼容/legacy 行为，必须由 B/domain 与 I/security Owner 共同决定后，才能依赖 Scope 精确相等。在此之前，实现不得根据字段名称或现有 helper 行为自行推断比较器。实现 MUST NOT 拼接未经转义的字符串、仅比较部分字段，或用显示标签替代类型化身份。

当且仅当以下条件全部成立时，请求才是此前已接受请求的重放：
- 经过认证的 ProducerIdentity 完全相等；
- Scope 相等性为 **CANDIDATE / TO_VALIDATE**，须等待权威 Scope 身份与相等规则；目前不得将其视为规范性重放条件。
- IdempotencyKey 完全相等；
- 当前请求的 Digest 与持久化 Receipt 绑定的 Digest 完全相等。

仅有相同 Producer Identity 与 Digest **不足以**判定重放；Scope 与 Idempotency Key 也必须相同。但 Scope 比较域仍为 **CANDIDATE / TO_VALIDATE**；在 B/domain 与 I/security Owner 决定 Scope 身份元组、authority/namespace 限定、规范化及兼容规则前，不得将该重放谓词视为完整的规范性规则。命名空间相同但 Digest 不同，属于 Key 冲突，不属于重放。

第一个成功提交的请求胜出。对同一命名空间的并发请求 MUST 由原子唯一性/CAS 边界串行化。恰好一个请求可以创建 Receipt 并追加事件；相同 Digest 的并发请求观察到胜出请求的 Receipt；不同 Digest 的请求收到冲突。未提交事件与 Receipt 的失败事务不占用该 Key。

## 4. Scope 行为

**CANDIDATE / TO_VALIDATE——等待权威 Scope 身份决议：** Scope 被提议作为幂等命名空间的一部分。同一 Producer Identity 和 Idempotency Key 是否能在两个 Scope 引用中形成独立操作/Receipt，取决于 §3 所述尚未解决的 Scope 身份/相等域。在 B/domain 与 I/security Owner 决定该规则前，不得将跨 Scope 重放隔离当作规范性比较规则。

该提议描述的是命名空间隔离，而非跨 Scope 授权；其具体适用仍取决于上述尚未解决的 Scope 身份/相等决议。调用方必须在目标 Scope 中独立完成认证和授权。无权访问的调用方收到常规授权拒绝；实现不得泄露另一个 Scope 中是否存在匹配 Key。

如果项目策略要求 Key 在 Producer 的所有 Scope 之间共享一个全局命名空间，则这是需要明确提出并经评审的替代方案，必须通过显式的后续决议取代本提案；不得由数据库唯一索引是否包含 Scope 而意外决定。

## 5. 冲突与错误行为

对于已存在且未过期的命名空间：

| 请求情况 | 必须行为 |
|---|---|
| Producer Identity + Scope + Key + Digest 全部相同 | 返回原 Receipt 并标记为重放；不得再次追加 |
| Producer Identity + Scope + Key 相同，但 Digest 不同 | 返回 IDEMPOTENCY_KEY_CONFLICT；不得追加；不得替换 Receipt |
| Producer Identity 不同，Scope + Key 相同 | 属于独立命名空间；不存在重放关系 |
| Producer Identity + Key 相同，但 Scope 不同 | CANDIDATE / TO_VALIDATE——只有 B/domain 与 I/security 决定 Scope 身份/相等域后，才能判定为独立命名空间及禁止跨 Scope 披露 Receipt |
| Producer Identity 类型仅部分匹配 | 属于不同命名空间；不得部分匹配去重 |
| 原操作结果仍未决/UNKNOWN 时命中相同命名空间 | 返回/恢复同一未决 Receipt 状态；不得启动第二次追加 |

冲突响应 SHOULD 标明冲突类别，但不得披露已存 Payload 或其他 Scope 的 Receipt。只有当前授权检查通过后才可返回 Receipt 数据。

## 6. Receipt 契约、持久性与生命周期

Receipt 是将一个命名空间绑定到已接受 Digest 及追加结果的持久化记录。至少记录类型化 Producer Identity、Scope、Idempotency Key、Digest（包括算法/版本标识）、操作/事件引用、终态或明确的未决状态，以及所选保留策略要求的创建/过期元数据。精确物理 Schema 由 Event Store 实现方负责。

**DECIDED 提案：**
- 事件追加与初始 Receipt 预留/提交 MUST 在 Event Store 逻辑提交边界上原子完成。不得存在已提交事件却没有对应 Receipt，也不得存在表示成功却没有对应已提交事件的 Receipt。
- 进程重启后必须从持久化状态恢复相同的重放/冲突结果；内存缓存永远不能成为事实来源。
- UNKNOWN/进行中的 Receipt 不得视为成功，也不得被当作再次追加的许可。重试准入前必须先协调事件与 Receipt 状态。
- 重放请求不得刷新原始创建时间，也不得暗中延长保留期限。

**CANDIDATE——保留策略：** 完整 Receipt 至少保留至 Producer 支持的最大重试/重放期限，并额外覆盖所需审计与恢复窗口。具体 TTL 数值取决于部署与策略，本 RFC 不冻结该数值。

**CANDIDATE——安全清理模型：** 不得简单删除过期 Receipt 后就把同一命名空间当成新请求；延迟到达的重试可能因此重复追加。建议评审以下方案：(a) 在整个 Key 禁止复用期间保留精简、持久化的 tombstone，至少包含命名空间、Digest 与过期/退役状态；或 (b) 要求显式 Producer Key-generation epoch/命名空间轮换，并在证明延迟投递有界后才回收旧命名空间。在方案确定前，过期 Key 必须 fail-closed（返回 IDEMPOTENCY_KEY_EXPIRED / 不追加）；只有在保持重放安全的前提下才可压缩 Receipt Payload/元数据。

**TO_VALIDATE：** 完整 Receipt、精简 tombstone 或 epoch 回收方案，哪一种最能平衡存储成本、审计、隐私与重放安全。通过延迟消息/重放测试、崩溃恢复、备份/恢复，以及过期与重试并发测试验证。

## 7. 边界用例

1. **跨 Scope 重放——CANDIDATE / TO_VALIDATE：** Producer P 在 Scope A 使用 Key K、Digest D1 提交；同一个 P 在 Scope B 使用 K、D1 提交。这些引用是否标识不同命名空间、因而是否属于新的追加而非重放，仍待 B/domain 与 I/security 对 Scope 身份/相等域作出决议。未经所需授权，Scope B 不得获得 Scope A 的 Receipt。
2. **Producer Identity 部分相同：** 若归属身份契约声明 instance 是身份类型的一部分，则 ProducerIdentity=(tenant=T, principal=P, instance=I1) 与 (tenant=T, principal=P, instance=I2) 是不同身份。即使 Scope、Key、Digest 相同也不去重。如果 instance 不属于规范 ProducerIdentity 类型，实现必须一致采用该规范类型；Adapter 不得各自决定。
3. **同一命名空间下 Digest 不同：** P + Scope A + Key K 首次提交 Digest D1。后续相同命名空间但 Digest D2 的请求必须返回 IDEMPOTENCY_KEY_CONFLICT；不得追加第二个事件，原 Receipt 保持不变。
4. **相同 Digest 并发重试：** 两个请求以相同命名空间及 D1 竞争。一个提交，另一个返回同一 Receipt。最终只能存在一个事件。
5. **崩溃/UNKNOWN：** 进程在提交边界附近崩溃。重启后 Adapter 必须协调持久化 Event 与 Receipt 状态；不得因为内存 Receipt 缺失就推断事务中止，也不得因为请求超时就推断成功。

## 8. 决策登记表

| 主题 | 状态 | 提案/验证方法 |
|---|---|---|
| 类型化命名空间 = ProducerIdentity + Scope + Key | CANDIDATE / TO_VALIDATE（Scope 组成部分） | B/domain 与 I/security 决定参与的 Scope 字段、namespace/authority 限定、规范化规则及兼容/legacy 规则；之后验证精确相等 |
| 重放要求命名空间与 Digest 均相同 | Scope 相等性为 CANDIDATE / TO_VALIDATE | 权威 Scope 相等域决议后再进行确定性单测/参考模型测试 |
| 同一命名空间不同 Digest 属于冲突 | DECIDED 提案 | 负向测试；断言不产生第二次追加且原 Receipt 不变 |
| 跨 Scope 使用相同 Key 相互独立 | CANDIDATE / TO_VALIDATE | B/domain 与 I/security 决定何时两个 Scope 引用不同；之后进行双 Scope 隔离与 Receipt 不可披露测试 |
| 禁止 Producer Identity 部分匹配 | DECIDED 提案 | 身份类型矩阵与序列化往返测试 |
| ProducerIdentity 具体组成（主体还是实例） | CANDIDATE | 身份 Owner 发布精确规范类型及认证映射 |
| Digest 规范化与算法/版本 | TO_VALIDATE | Payload 完整性契约；跨版本黄金向量 |
| 完整 Receipt 的 TTL 数值 | CANDIDATE | 明确最大重试期限、审计及恢复要求 |
| Tombstone 或 epoch 回收 | CANDIDATE | 延迟重放、崩溃、恢复、并发与成本实验 |
| Event + Receipt 物理原子实现 | TO_VALIDATE | 真实文件 SQLite 事务测试；崩溃/故障注入与重启重放 |
| UNKNOWN 协调规则 | TO_VALIDATE | 在每个边界终止进程；证明无重复追加或虚假成功 |

本 RFC 中的 DECIDED 提案是提交评审的规范性提案，不代表已经成为仓库范围内获批决议。只有在负责的架构/领域/安全评审者接受并更新决策记录后，才能升级为 DECIDED。未获接受的项目必须保留为 CANDIDATE 或 OPEN。

## 9. Event Store SQLite Adapter 集成

SQLite Adapter MUST 作为逻辑契约的消费者实现本 RFC，不得重新定义契约。

- 契约引用：RFC-IDE-001 v1.0.0
- 规范引用方式：RFC-IDE-001 §3–§6（命名空间、重放判定、Scope 隔离、冲突、Receipt 生命周期）。
- 必须实现：对精确类型化命名空间建立持久化唯一性边界；相同 Digest 重放返回持久化 Receipt；Digest 不同则冲突；披露 Receipt 前先授权；Event 与 Receipt 原子提交；重启后恢复相同语义；清理不得悄然重新开放已退役 Key。
- 必须测试：同命名空间同 Digest 重放；同命名空间不同 Digest 冲突；跨 Scope 同 Key；不同/部分相同 ProducerIdentity；并发首写竞争；提交前后崩溃；重启 Receipt 恢复；过期/清理与延迟重放。
- 不得越权：SQLite 事务/存储机制可以证明物理原子性，但不得决定 ProducerIdentity 组成、Scope 授权或 Receipt 保留策略。

建议代码/文档引用：Implements RFC-IDE-001 v1.0.0, §3–§6。若后续版本改变语义，Adapter MUST 固定引用精确修订版本，并增加迁移/一致性测试。

## 10. 非目标与开放依赖

本 RFC 不决定事件顺序、EventId 生成、Payload 规范化、密码学摘要算法、授权策略内部实现、跨 Scope 数据共享、超出逻辑原子性要求的事务拓扑，也不决定生产保留/法律保全规则。这些由各自契约与权威方负责。

## 11. 评审与验收

必需评审方：Domain Model / Producer Identity 权威方、Scope / Security 权威方、Event Store Owner、Storage 实现 Owner。验收要求：中英语义一致；对每项 DECIDED 提案明确批准或列明例外；对 CANDIDATE / TO_VALIDATE 项关闭问题，或保留并给出责任方及验证证据；Event Store SQLite Adapter 实现线确认消费该契约。

本 RFC 或其 PR 均不意味着实现或生产验收已完成。
