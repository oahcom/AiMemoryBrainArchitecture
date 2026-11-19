# L2-01-D-E-STORAGE-PRODUCER-FENCE 对齐报告

<badge color="warning">OPEN — 独立核验进行中</badge> <badge color="info">READ-ONLY</badge>

**治理立场：不作 Owner 代决策，不把提案视为批准，不把 reference-model 测试视为物理实现通过。**

本轮执行边界：

- 仅读取 `oahcom/AiMemoryBrainArchitecture` 既有 GitHub 载体。
- 不创建 PR/Issue，不提交 Git，不修改 assignee、Issue 状态或 PR 状态。
- AI-EXEC-001 v1.1、AI-EXEC-002 v1.1 的实际加载版本必须有仓库证据；v1.2 PENDING ADOPTION 不自动生效。
- 未取得精确 SHA、Blob SHA 或 Owner 正式决定的事项，一律保留 `OPEN` / `TO_VALIDATE`。
- 所有缺失的 Decision_ID 标记为 `NOT_CREATED`，不虚构登记记录。

**重要权限界限：** 本报告是 A 统筹下的 L2 对齐意见，不是 D、E、Storage、I 或 F 的正式批准，也不构成跨域接口冻结或生产启用授权。

## 1. 启动基线核验

<badge color="success">SHA 已核实</badge>

| 项目 | 实测结果 |
|---|---|
| 仓库 | `oahcom/AiMemoryBrainArchitecture` |
| main | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` |
| remediation 分支 | `745c768deca0a5826d436744213bed3beb65cd85` |
| AI-EXEC-001 | v1.1，ADOPTED |
| AI-EXEC-001 Blob | `b809d770f93f5a2244988f04f68ad913b29f5e76` |
| AI-EXEC-002 | v1.1，ADOPTED |
| AI-EXEC-002 v1.2 | PENDING ADOPTION，不作为本轮执行规范 |
| AI-EXEC-002 当前 main Blob | `772cee6b9a9a9c510c79adfd85eefd96397573c2` |

两个 commit 均由 GitHub 返回的实际 commit SHA 与请求值一致。

特别注意：main 上的 AI-EXEC-002 文件实际已经是 v1.2，但文件头明确声明 v1.1 经 PR #256 合并采用、v1.2 尚待采用。因此，本轮按 v1.1 的有效性口径执行，没有将 v1.2 的新增内容冒充为已生效规则。

**启动证据限制：** 当前对话包含 LOADED 声明，但尚未发现将本次完整指令快照及其 SHA-256 持久登记到五个 Issue 之一的证据。不能把本次聊天声明等同于已经完成 T2 持久化登记。

## 2. 五个 Issue 状态与责任矩阵

<text color="secondary" size="xs">GitHub 实际读取；以下均为 2026-11-19 的读取结果。</text>

| Issue | 当前状态 | 主责边界 | 实际阻塞 |
|---|---|---|---|
| [#2](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/2) | OPEN | D / E / Storage，I、F 协同 | Phase 3.6 联合决策没有完整独立 Owner 签署；物理发布边界未证明 |
| [#10](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/10) | OPEN | Storage 主责物理能力；A/COC 协同 | Gate A 尚未全部通过，Gate B/C 顺序阻塞 |
| [#14](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/14) | OPEN / HOLD | A 统筹，I/D/C/H/Storage 分别负责 | Recovery Cutoff、Owner-local Gate、JF-10 组合及物理恢复未完成 |
| [#20](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/20) | OPEN / HOLD | Storage 主责；D/I/F/E/G/H 协同 | Producer 分类、Inventory、Forget、Restore 的精确 Owner 决定和端到端证明不足 |
| [#25](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/25) | OPEN | D/E/I/Storage | Phase 3.8 精确版本独立批准及物理原子发布仍缺失 |

五件 Issue 均未关闭，且均未指定 GitHub assignee。

当前评论数量分别为：

- #2：12
- #10：62
- #14：54
- #20：33
- #25：96

评论数量、角色模拟和协调方登记均不构成 Owner 批准。

### 责任映射核验

| Issue | A 的初分 | 本轮判断 |
|---|---|---|
| #2 | D | <badge color="success">基本成立</badge> D 拥有 ForgetFence 和 ProducerWork 语义，但不是联合决策唯一责任方 |
| #10 | Storage | <badge color="success">成立</badge> Storage 主责数据库/XID/可见性物理实现；A 负责 COC 集成 |
| #14 | A（跨 Owner 整合） | <badge color="success">成立</badge> A 负责整合，不拥有其他 Owner 的协议决定权 |
| #20 | Storage | <badge color="success">成立</badge> Storage 主责其物理持久化与恢复提案，但不能替代 D/I/F/G 的语义决定 |
| #25 | D | <badge color="warning">需要修正</badge> D 主责 ForgetFence 和依赖语义；整体是 D/E/I/Storage 联合决策，不应登记成 D 单方负责 |

这里必须区分三个概念：

1. 领域语义责任。
2. 物理实现责任。
3. 跨领域集成协调责任。

不能用一个主责标签把三者合并。

## 3. Source Artifact → Commit SHA → Blob SHA

以下只列本轮实际读取并取得 Blob SHA 的主要证据。未取得的 commit SHA 明确标记，不从分支名称或评论内容推算。

| Artifact | Branch / Ref | Commit SHA | Blob SHA |
|---|---|---|---|
| AI-EXEC-001.md | main | `d61f813c…` | `b809d770…` |
| AI-EXEC-002.md | main | `d61f813c…` | `772cee6b…` |
| D ForgetFence 主契约 | session-d | NOT_VERIFIED | `4da0b61b…` |
| D Phase 3.7 契约 | session-d | NOT_VERIFIED | `4c01713b…` |
| E Phase 3.6 联合决策 | session-e | NOT_VERIFIED | `aaa15de9…` |
| E Phase 3.7 生命周期 | session-e | NOT_VERIFIED | `4fb9e585…` |
| I Phase 3.6 授权契约 | session-i | NOT_VERIFIED | `5a5304d4…` |
| I Phase 3.7 授权契约 | session-i | NOT_VERIFIED | `e3b1b5d9…` |
| Storage Phase 3.7 实现方案 | session-storage | NOT_VERIFIED | `2ab899ee…` |
| Storage Archive/Restore 提案 | commit `a6597309…` | `a6597309…` | `6f4b003b…` |
| A Phase 3.8.1 集成提案 | session-a | NOT_VERIFIED | `ad5450ea…` |

<text color="secondary" size="xs">缩写 SHA 仅用于表格可读性，完整值以本报告前文、Issue 正文及仓库文件为准。</text>

关键的版本纠正：

- #25 正文中最早的 D/E/Storage 三个 Blob 已被后续精确读回版本取代。
- 当前有效复核基线应使用 D `4c01713...`、E `4fb9e585...`、I `e3b1b5d9...`、Storage `2ab899ee...`。
- A 的 `ad5450ea...` 是实际读取的提案 Blob，不能因为它更新了精确 Pin 就视为 Owner 批准。
- #20 的 Storage `6f4b003...` 是独立审查对象，不是 Storage 领域权威契约的替代品。

---

## 4. D/E/Storage 现存契约对齐

### 4.1 D：ProducerWork 与 ForgetFence

<badge color="success">语义 DECIDED</badge> <badge color="warning">物理实现 OPEN</badge>

D 的契约明确规定：

1. ProducerClass 必须已注册且启用。
2. 必须先获得 D 持久化 RegistrationReceipt。
3. 然后才能入队、租约、读取受保护源数据、执行或重放。
4. ProducerWork 注册与 ForgetFence 安装必须处于同一线性化排序域。
5. 依赖集合必须完整持久化，才能发布。
6. 最终可见性转换必须重新验证最新 ForgetFence。
7. PermissionEpoch 由 I 独立验证，禁止与 D 的 FenceGeneration 比较。
8. 超时、丢失 ACK、租约过期均不能证明工作已经终结。

特别纠正一个容易导致实现错误的地方：

**EventRef-only ingress 可以先登记。**

当 authenticated producer、启用的 ProducerClass、精确 Scope、请求摘要和 D 批准的 lineage token/digest 完整时，D 可以在 Canonical MemoryRef 尚不存在时登记 ProducerWork。

但：

- 该工作仍计入 D barrier。
- 不能因此授权受保护 payload dereference。
- 精确 Canonical refs/revisions 必须在 dependency registration/publication 前补齐。
- 不完整身份或 lineage 仍然 quarantine。

因此，不能再使用「没有 MemoryRef 就一律不允许 ProducerWork 登记」的旧理解。

### 4.2 E：生命周期与身份稳定性

<badge color="success">核心语义已明确</badge>

E 的身份关系：

| 身份 | 生命周期 |
|---|---|
| ProducerWorkItemId | 根工作义务稳定身份 |
| AttemptId | 每次执行尝试独立 |
| LeaseEpoch | 每次重新分配推进 |
| DerivationRunId | 每次重新编译创建新值 |
| ArtifactId | 不可变产物身份 |
| DependencySetDigest | 完整依赖集合摘要 |

Retry、DLQ replay、worker recovery 不得创建新的无关联根 WorkItemId。

Recompile 保留根 WorkItemId，创建新的 DerivationRunId。若形成独立调度工作，必须创建与根关联的 child WorkItem，并纳入相同 barrier。

E 的实际阻塞：

- 完整 dependency set 的持久化实现。
- 与 D 的实际 fence 序列化。
- 与 Storage 的最终 visibility commit。
- E36-01..23 的真实执行证据。

E 的 Phase 3.6 文档明确说明：这是架构决策记录，不是运行实现验证。不能把该文件当成 E 独立批准 #2 的证据。

### 4.3 Storage：物理原子性

<badge color="warning">PROPOSED PHYSICAL REALIZATION</badge>

Storage Phase 3.7 文件明确把责任分开：

- D：语义准入、Fence、依赖完整性、Publication 决策。
- E：编译、Attempt、Lease、Derivation、私有 staging。
- I：授权、PermissionEpoch、撤销。
- Storage：持久化、事务隔离、序列化、可见性和崩溃恢复。

推荐模型是每个 Canonical Memory authority 的强一致事务域。

以下操作必须在同一个线性化决策域内排序：

1. RegisterProducerWork。
2. InstallForgetFence + CaptureProducerRegistrationHighWater。
3. RegisterDerivedDependency。
4. PublishDerivedIfFenceCurrent。
5. CompleteProducerWork。

禁止用：

- process-local mutex；
- queue 顺序；
- eventual replica；
- outbox-only；
- check-then-write；
- 先发 D token，再独立执行 Storage 写入。

**但这份 Storage 文件的状态仍然是 PROPOSED PHYSICAL REALIZATION；不是已经选定并部署的数据库事务拓扑。**

## 5. DECIDED / CANDIDATE / OPEN / TO_VALIDATE

| 项目 | 当前分类 | 证据判断 |
|---|---|---|
| D ProducerClass / RegisterProducerWork 语义 | DECIDED | D 权威契约明确 |
| D EventRef-only ingress | DECIDED | D Phase 3.7 §8 |
| ProducerWorkItemId retry 稳定性 | DECIDED | E 生命周期契约 |
| AttemptId / LeaseEpoch 隔离 | DECIDED | E 生命周期契约 |
| 完整 transitive dependency registration | DECIDED（语义） | 物理实现未证实 |
| D Fence / producer barrier 排序 | DECIDED（语义） | 真实事务尚未证实 |
| I PermissionEpoch 独立权威 | DECIDED（语义） | 最终提交点消费仍待验证 |
| Storage 单事务物理方案 | CANDIDATE | 尚未选定部署拓扑 |
| PostgreSQL 18.7 | CANDIDATE（物理能力） | 已有五类 CI 证据，不代表生产部署 |
| COC 持久化方案 | CANDIDATE | 存在逻辑模型和设计，未证明生产持久化 |
| H RecoveryJoin schema | CANDIDATE | 不能当作冻结协议 |
| Archive/Restore 全链路原子性 | OPEN | 缺完整 Owner 决定及运行证据 |
| D/E/Storage Phase 3.8 联合批准 | OPEN | 缺精确版本独立批准 |
| 多 PolicyDomain 原子授权 | OPEN / BLOCKED | I 明确不接受未经批准的多域组合 |
| 最终 visibility crash/failover conformance | TO_VALIDATE | 真实端到端执行不足 |

### 已经明确批准的事项

这里采用严格口径：只有可归属于对应权威角色、针对准确版本的决定才计入。

**I：**

Issue #2 评论中的 I composition disposition `9e1f66dd...` 明确接受 COC 作为 CGH 因果顺序证据服务，但不接受自动 COC↔JF-10 组合。

**Storage：**

Issue #2 中 Storage 的决定：

- Artifact：`phase-3.6-coc-storage-boundary-acceptance.md`
- Blob：`a589d983ac145244962c22e5da3a55427aa35ff8`
- Commit：`7b83e61c44dd4b67fa2059a3bff83d453aeaf757`
- 决定：`CONFIRMED WITH CHANGES`

它确认的是 COC 逻辑架构边界，不是已部署的物理事务或 JF-10 原子性。

**E：**

存在 E Phase 3.6 联合架构决策文件，但其决策权限说明是用户委派的 D/E/Storage 联合架构角色。不能将其直接算作独立 E Owner 对 #2 或 #25 的签署。

**D：**

D 的 ForgetFence 语义契约已经明确，但当前 Phase 3.8 精确版本的独立 Owner 接受记录尚未得到充分证明。

**A：**

A 的集成审查、整合和候选提案不替代任何领域 Owner 的决定。

## 6. D/E/Storage 责任冲突清单

| 编号 | 冲突 | 裁定 |
|---|---|---|
| C-01 | D 语义与 Storage 数据库写入权限混淆 | D 决定语义，Storage 只提供物理持久化 |
| C-02 | E Recompile 创建新根工作身份 | 禁止；根身份稳定，DerivationRunId 独立 |
| C-03 | Storage D Admission 后再独立写入 | 禁止；必须存在可证明的原子排序协议 |
| C-04 | I PermissionEpoch 由 Storage 比较或推算 | 禁止；I 必须提供自身权威证据 |
| C-05 | D PublicationParticipantRef 与 Storage PreparedParticipantRef 混用 | 禁止；属于不同名义类型 |
| C-06 | COC ACK 被当作 Storage commit | 禁止 |
| C-07 | COC 自动替 I/D 释放 owner-local gate | 禁止 |
| C-08 | UNKNOWN 被转换成 ABORT 或成功 | 禁止；必须保留私有状态和 barrier |
| C-09 | Storage 提案被误认为 Owner 批准 | 禁止 |
| C-10 | PostgreSQL CI 被误认为生产环境证明 | 禁止 |

### 特别重要：两个身份顺序不能混为一谈

**Producer admission 顺序：**

```text
D RegisterProducerWork
        ↓
D durable RegistrationReceipt
        ↓
E Queue / Lease / Execute
```

**Derivative publication 顺序：**

```text
Storage hidden durable participant
        ↓
D PublicationParticipantRef
        ↓
I single-use CommitAuthorizationReceipt
        ↓
Storage final visibility commit
        ↓
D / I independent closeout
```

其中最终 commit 必须同时验证当前 D Fence、完整 dependency receipts、有效 I 授权证明和准确 Storage participant。

UNKNOWN 时不能发布，不能关闭 D/I barrier。

## 7. 依赖 DAG 与执行顺序

<box border radius="lg" padding={3} gap={2}>
  <title size="lg">执行依赖图</title>
  <box background="rgba(46,160,67,0.10)" radius="md" padding={2}>
    **D：Producer Registry / Fence / Lineage 语义**

    **E：WorkItem / Attempt / Lease 生命周期**

    **I：PermissionEpoch / Revocation 语义**
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box border radius="md" padding={2}>
    **Storage：选定真实事务域与持久化 participant**

    当前：候选 PostgreSQL 18.7，生产拓扑未证实。
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box border radius="md" padding={2}>
    **D：登记 PublicationParticipantRef**

    绑定准确 Storage participant。
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box border radius="md" padding={2}>
    **I：单次授权消费与终局证明**

    必须绑定同一操作、同一请求摘要和 PolicyDomain。
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box background="rgba(46,160,67,0.10)" radius="md" padding={2}>
    **Storage：最终 visibility commit**

    原子提交可见性指针、PublicationReceipt 和 outbox。
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box border radius="md" padding={2}>
    **D / I：各自完成 terminalization**

    UNKNOWN 不得提前释放屏障。
  </box>
</box>

### 可以独立并行的工作

1. D：补全 ProducerRegistrationHighWater 命名空间、ForgetFence currentness proof。
2. E：实现本地稳定 WorkItemId、Attempt/Lease fencing、私有 staging。
3. I：完善 PermissionEpoch 当前性证明和 revocation sequencer。
4. Storage：生产数据库及部署拓扑选型、PITR、HA、故障恢复探测。
5. H：完善类型化 schema、canonicalization、签名和兼容性测试。
6. A：维护精确 Pin、跨 Owner 冲突表和依赖矩阵。

以上工作可以并行设计或在隔离环境实现，但不得提前宣称联合 publication conformance。

### 必须保持 BLOCKED 的工作

- 依赖不完整时的最终 publication。
- 没有 D RegistrationReceipt 的 ProducerWork 执行。
- 没有 I 当前授权证明的最终 visibility commit。
- JF-10 自动与 COC 组合的生产流程。
- 未完成 Recovery Cutoff reconciliation 的 owner gate reopening。
- Restore 尚未完成 D/I 独立控制账本核验时的 serving。
- Multi-PolicyDomain 原子授权。

## 8. 每个 Issue 的下一步与关闭条件

| Issue | 明确下一步 | 关闭条件 |
|---|---|---|
| #2 | D/E/I/Storage 分别对当前准确版本作出正式决定；Storage 给出物理事务边界 | 四方决定、I/F 消费契约及真实发布竞争测试齐全 |
| #10 | Storage 完成 Gate A 剩余生产环境核验；A 推进 Gate B | Gate A 全部通过，再推进 Gate B，最后 Gate C |
| #14 | I/D/C/H 对 Recovery Cutoff、Owner-local Gate 和 same-XID 分别作出准确版本决定 | 五方独立决定、完整参与者集合证明、崩溃恢复测试 |
| #20 | Storage/D/I/F/E/G/H 对分类、Inventory、Forget、Restore 分别完成决定 | Owner 决定齐全，Inventory 完整，Restore/PITR 证据通过 |
| #25 | D/E/I/Storage 对四个最新 Phase 3.8 Blob 分别决定 | 四方决定、Storage 物理实现、D/I 参与者核验、端到端 conformance |

### #10 特别状态

<badge color="warning">Gate A — PARTIAL PASS / OPEN</badge>

五类 PostgreSQL 18.7 CI 证据已被 Issue 记录：

- 单节点 prepared-XID + hard restart。
- 双节点同步 standby promotion。
- pg_basebackup restore + unresolved prepared-XID。
- Coordinator crash / unrecorded ACK。
- TCP response loss + same-XID reconciliation。

但这些不代表真实 Canonical Authority 已部署 PostgreSQL 18.7。

仍缺：

1. 实际 Canonical Authority runtime executable 和 DB adapter。
2. WAL-archive PITR。
3. Old-primary fencing / split-brain prevention。
4. 同步 standby 不可用时 protected PREPARE 的 fail-closed 证明。
5. 实际 host/zone/cloud storage durability。
6. 真实 I/D control-ledger source/high-water。
7. 人类生产 on-call、runbook、监控及 RPO/RTO。

因此：

- Gate A：PARTIAL PASS / OPEN。
- Gate B：BLOCKED。
- Gate C：BLOCKED。
- JF-10 P0：OPEN。
- Production activation：NOT AUTHORIZED。

## 9. 需要 A 裁定的跨域问题

以下是统筹层需要处理的事项，不是本会话代替 A 做决定。

| Finding | 问题 | 建议处理 |
|---|---|---|
| A-01 | #2 与 #25 共享底层原子发布问题，但阶段不同 | 保留两个 Issue，各自记录历史和验收边界 |
| A-02 | #14 的 COC 与 JF-10 是否可组合 | 保持分离，等待完整联合协议及 I/D/Storage 决定 |
| A-03 | #20 Archive/Restore 与 #25 producer visibility 的接口关系 | 建立共同依赖，不强行归并 |
| A-04 | D/E/Storage 语义与物理实现的证据混杂 | 统一要求 DECIDED、IMPLEMENTED、VERIFIED 分开登记 |
| A-05 | AI-EXEC-002 v1.2 已出现在 main | 继续按 v1.1 执行，等待正式 adoption |
| A-06 | Phase 3.8 D/E/I/Storage 决定逾期 | 保留 OPEN/HOLD，不能由协调方模拟签署 |

---

## 10. Decision Register

本轮没有创建或修改任何持久化决策记录。

| Decision_ID | Delta_Scope | Evidence | Unresolved_Findings |
|---|---|---|---|
| L2-01-DEC-001 | #2 D/E/Storage | NOT_CREATED；已有 D/E/Storage 契约 | 独立 Owner 决定、物理原子性 |
| L2-01-DEC-002 | #10 JF-10 | NOT_CREATED；五类 CI 证据 | Gate A 剩余条件、Gate B/C |
| L2-01-DEC-003 | #14 COC | NOT_CREATED；I composition、Storage COC boundary | Cutoff、Gate、same-XID 联合证明 |
| L2-01-DEC-004 | #20 Archive/Restore | NOT_CREATED；Storage 提案 | Owner 接受、Inventory 和 Restore |
| L2-01-DEC-005 | #25 Producer admission | NOT_CREATED；D/E/I/Storage 最新 Blob | 独立批准、物理实现、端到端测试 |

所有上述 Decision_ID 均为建议登记标识，不是已经创建的正式决策。

## 11. 最终 L2 裁定

<badge color="danger">NO-GO — 联合契约冻结</badge>

<badge color="warning">GO — 有限并行的领域设计和隔离实现</badge>

本轮可以确认：

1. D 的 ProducerWork/Fence 语义基础已经明确。
2. E 的稳定身份和生命周期规则已经明确。
3. I 的授权与撤销权威边界已经明确。
4. Storage 的事务原子性要求已经明确。
5. 五个 Issue 的责任划分可以继续作为统筹基础。

但目前不能确认：

- 所有领域 Owner 已对当前精确版本正式批准。
- 存在已选定、已部署的共同事务域。
- COC 与 JF-10 已形成安全的完整组合。
- Archive × Forget × Inventory × Restore 已经端到端验证。
- 生产环境具备最终可见性原子提交能力。

**Decision_ID：NOT_CREATED**

**Delta_Scope：** 只读核验五个 Issue、四个领域契约及跨域依赖。

**Relevant_Artifacts：** 见第 1、3 节；无法直接证明的 Commit SHA 不予补填。

**Evidence：** GitHub Issue 正文、评论、指定分支文件的实际读取结果及 commit SHA 核验。

**Unresolved_Findings：** #2、#10、#14、#20、#25 全部保持 OPEN。

**停止条件：** 已达到需要正式 Owner 决定、物理拓扑证据和跨域 conformance 的边界；不继续推断或代签。

**交付结论：本报告可交 A 整合，但不能作为任何 Owner 的正式 ACCEPT，也不能作为 PR 合并或生产激活授权。**

---
