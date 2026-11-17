**状态：** CANDIDATE 领域契约；只有依赖的 ADR/身份审批完成后才具有规范效力。  
**Owner：** Memory Domain Model（B）  
**关联 Issue：** INT-P0-01、INT-P0-02、INT-P1-02、INT-P1-03、INT-P1-06、DM-005、DM-006  
**源分支：** `session-b-domain-model-phase3`  
**精确源 Blob SHA：** `e9a6bd21e06bc02a5208619f5a949217860b1c00`  
**对应文件状态：** 双语阅读对应文件；不改变源决策状态。  
**English companion:** [English](../../en/02-domain-model/typed-reference-and-scope-semantics.md)

# 类型化引用与 Scope 语义

## 1. 目的与边界

本文定义领域引用的逻辑身份、命名空间、版本固定和生命周期含义；不定义数据库键、物理分区、Wire 序列化、令牌格式、授权授予或存储实现。

- B 负责领域引用的语义及唯一性边界。
- D 负责规范 Memory 持久化、提交机制、生命周期转换权威和规范对象存储行为。
- E 负责源接收、抽取和提案生成。
- F 负责索引、检索投影、新鲜度和激活建议。
- G 负责 Memory Context 成员关系及 ContextVersion。
- H 负责 Wire 表示及已认证传输绑定。
- I 负责认证/授权策略、委托、撤销、保留及 Forget 完成策略。

类型化引用是对领域身份的寻址，不是调用方有权读取或修改目标的证明。

## 2. 命名空间模型

### 2.1 Brain authority 命名空间

每个规范对象引用都在一个稳定的 **BrainAuthority 命名空间**内解释。该命名空间是签发规范 ID 的逻辑权威边界。Opaque ID 在该权威命名空间内唯一，且不得重新分配给其他对象。若部署存在多个独立 Brain authority，authority namespace 本身就是引用身份的一部分；不同 authority 的 ID 不可比较，也不得隐式关联。

### 2.2 Scope 不是 ID 命名空间

Scope 是附着于对象的显式领域关系，用于限定归属和适用性，而不是替代身份唯一性。

- 对象经授权领域操作改变 applicability Scope 集合时，其身份保持稳定。
- 对象跨 Scope 移动或共享，不得静默签发新身份；应按所属聚合体定义，产生可审计的 Scope 绑定变更/版本。
- 引用上的可选 Scope hint 仅是校验/消歧约束，不是授权授予。
- Tenant/user/project 边界可以表示为 Scope kind，但 B 不定义物理租户分区。

### 2.3 通用引用封套

类型化引用在概念上包含：

- `authority_namespace`：签发该身份的 Brain authority；
- `object_id`：opaque、无语义、永不复用的 ID；
- `object_type`：由引用类型固定，不由调用方自由文本控制；
- `version_id`：不可变版本/修订引用必需；稳定身份引用不包含；
- `scope_hint`：可选、已解析的 ScopeRef，用于校验/上下文，不代表权限；
- `schema_family/version`：必要时用于解释兼容性的元数据。

编码由 H 负责。上述是语义内容，不是规定 JSON/protobuf 封套。

## 3. 类型化引用

### 3.1 MemoryRef

- **目标：** 稳定的规范 Memory 身份。
- **唯一性：** `(BrainAuthority, memory_id)`；在单一 BrainAuthority 内唯一，不从内容或 Scope 派生。
- **版本：** 不固定版本，只解析身份。不可变内容应使用 MemoryVersionRef。
- **Scope：** 目标有一个 owner Scope 和零个或多个 applicability ScopeRef。可见性针对精确对象和操作评估。
- **生命周期：** 身份跨 MemoryVersion 持续存在。Superseded/Archived 仍是历史身份。Forgotten 身份不得复用；内容访问可按 I 策略被抑制或不可用。

### 3.2 MemoryVersionRef

- **目标：** 一个已提交且不可变的 Memory 快照。
- **唯一性：** `(BrainAuthority, memory_version_id)`；必须唯一解析到一个 MemoryRef 和序列号。
- **版本：** 版本身份内在固定；引用 MUST NOT 通过不断变化的 current pointer 解析。历史查询应包含/解析 parent version 和 commit sequence。
- **Scope：** 继承该版本时 Memory 的显式 owner/applicability 绑定；Scope 变化应记录在版本/历史中，不得静默推断。
- **生命周期：** 提交后不可变，不得重写。后续 MemoryVersion 可使其被取代；历史读取仍须精确，但受 Forget/retention 约束。忘记后的 payload 可变为不可用，而无需重新分配引用。

### 3.3 ClaimRef

- **目标：** 稳定 Claim 身份/命题线程，前提是 Fact/Claim ADR 批准 Claim 身份。
- **唯一性：** `(BrainAuthority, claim_id)`；跨 ClaimRevision 稳定，不基于文本哈希，也不得复用。
- **版本：** 不固定 revision；仅标识命题线程。需要精确断言内容时不得使用它替代具体 revision。
- **Scope：** Claim 携带 owner/applicability ScopeRefs；引用检查精确目标可见性。Scope 变化不改变 claim_id，但需要可审计的 revision/binding event。
- **生命周期：** 更正、细化和撤回期间身份稳定；终态 Forget 限制不允许 ID 复用。

### 3.4 ClaimRevisionRef

- **目标：** 某个 Claim 的一个不可变修订。
- **唯一性：** `(BrainAuthority, claim_id, claim_revision_id)`；revision ID 在 Claim 内唯一，该组合在不同 authority 间也无歧义。
- **版本：** 必须包含精确 revision ID 和按 Claim 单调递增的序列；除 genesis 外只有一个 parent。不得使用浮动的“latest”语义。
- **Scope：** 必须与 Claim 身份及该 revision 的显式 ScopeRefs 兼容；不得通过继承扩大访问。
- **生命周期：** 提交后不可变。更正、认知状态变化、有效性更正或撤回都追加新 revision；旧引用在 Forget 约束下仍有历史意义。

### 3.5 EntityRef

- **目标：** 具有稳定身份的 Entity。
- **唯一性：** `(BrainAuthority, entity_id)`。
- **版本：** 不固定版本；消费者需要精确描述属性时可使用 EntityVersionRef。本文不擅自创建未要求的规范引用类型，但精确 Entity 版本引用仍是 D 所有的规范需求。
- **Scope：** 不得从标签推断身份。Owner/applicability Scope 限定解析和遍历。
- **生命周期：** Provisional/Resolved/Merged/Split/Retired 状态不得复用 ID。合并必须创建显式 redirect/migration 记录；历史 EntityRef 仍指向原始身份。

### 3.6 EvidenceRef

- **目标：** 稳定 Evidence 身份。
- **唯一性：** `(BrainAuthority, evidence_id)`；Evidence 身份策略可用 source/version、locator、digest、Scope 和 kind 检测重复，但已签发 ID 必须 opaque 且稳定。
- **版本：** Evidence 内容/来源绑定 MUST 不可变，或指向精确 source version/digest。源字节/digest 变化必须创建新 Evidence 身份/版本或显式完整性冲突记录，不得静默覆盖。
- **Scope：** Evidence 有自己的 ScopeRefs，限制可能比其支持的 Claim/Memory 更严格。可访问 Claim 不意味着可访问 Evidence。
- **生命周期：** 可用性可以是 available、restricted、expired、forgotten 或 external_unavailable。引用可为审计保留，而解引用被拒绝/不可用。

### 3.7 ScopeRef

- **目标：** 一个已注册的 Scope 身份。
- **唯一性：** `(BrainAuthority, scope_id)`；Scope kind 是经过校验的元数据，不是调用方选择的命名空间。
- **版本：** 身份稳定；若 containment/属性变化，必须有 Scope descriptor revision 或版本化变更记录。消费者不得假定可变 parent pointer 在历史上恒定。
- **Scope 绑定：** ScopeRef 表示领域命名空间/归属/适用上下文，不携带 grant。
- **生命周期：** active、suspended、closed 或 retired descriptor 状态可限制新的领域关联。历史引用按 retention 规则仍可解析；closed/retired ID 永不复用。

### 3.8 ActorRef

- **目标：** 由已认证身份基础设施解析出的稳定 actor/principal subject 身份。
- **唯一性：** 在声明的身份联邦内按 `(issuer, subject_id)` 唯一；必要时绑定 BrainAuthority 映射。显示名、邮箱字符串、Agent 提供的 payload ID 或模型生成标签都不是身份键。
- **版本：** subject 身份稳定；认证凭据/密钥轮换和委托变化是身份/安全事件，除非 issuer/subject 身份改变，否则不产生新的领域 actor 身份。
- **Scope：** ActorRef 可关联多个 Scope，但这种关联不授予访问权限。
- **生命周期：** active、disabled、revoked 或 unknown 身份状态由 H/I 身份服务解析；B 只定义引用语义。历史归因与当前授权必须区分。

### 3.9 EventRef

- **目标：** 一个已接受、不可变的源 Event 身份。
- **唯一性：** `(BrainAuthority, event_id)`；producer-local ID 必须以已认证 producer/source 身份作为命名空间，再映射为 Brain 签发的 EventRef。
- **版本：** 给定 digest/version 的 Event payload 不可变。更正应创建新的 EventRef 或关联原始事件的显式 correction event，不得原地修改。
- **Scope：** Scope 和 Environment Scope 从可信 ingress metadata 捕获；源文本不能自行指定它们。
- **生命周期：** accepted、processing、processed、quarantined、expired、forgotten 是不同的摄取/保留状态，不是 Claim epistemic status。即使 payload 不可解引用，EventRef 仍是审计身份。

## 4. TimeValue 与 TimeInterval

TimeValue 和 TimeInterval 是类型化领域值，不是全局可寻址对象身份。

### 4.1 TimeValue

TimeValue 表示具有来源意识的时间边界或时间点，包括：

- 规范化时刻或有界不确定区间；
- 精度/粒度（tick、秒、日、月、年、近似）；
- 时区/偏移，或明确的未知时区；
- 确定性/不确定性限定；
- 可用时保留原始来源短语和 locale；
- 来源 EventRef/EvidenceRef 或其他来源引用；
- 规范化方法/版本。

TimeValue 不是 ID。即使规范化时刻相同，若精度/来源不确定性不同，也不一定语义等价。Unknown 必须显式表达；它不是零、无穷或“所有时间”。

### 4.2 TimeInterval

TimeInterval 是一对 TimeValue 边界及边界语义：

- 起止边界可以已知、近似或显式未知/无界；
- 默认区间约定为左闭右开 `[start, end)`，除非领域词汇明确要求其他约定；
- 除非领域明确建模逆序/不确定区间，否则 start 晚于 end 属无效；
- 缺少 interval 表示“有效性未指定/未知”，不是“始终有效”；
- 无界起止与未知起止不同；
- 必须保留原始表达及规范化不确定性的可追溯性。

Event Time、Recorded At、Commit/Transaction Time 和 Valid Time 是不同的时钟。

## 5. Scope 领域语义

### 5.1 Scope 定义

Scope 是具名且具有身份的领域命名空间，声明对象属于何处、适用于何处或应在何处解释。Scope 支持身份解析分区、provenance 遍历、关系有效性、环境隔离和上下文组装。

Scope **不是**：
- permission、role、grant、ACL、policy decision 或 authenticated principal；
- Actor 可以读写其中对象的证明；
- 安全过滤器实现或物理存储分区；
- ContextVersion 或任务指令。

### 5.2 Scope kinds

候选注册类型包括：

- `system`：Brain authority 级命名空间；
- `tenant`：租户/客户边界；
- `user`：用户所有领域；
- `project`：项目/工作区边界；
- `agent`：逻辑 Agent 身份；
- `agent_instance`：一个 Agent runtime 实例；
- `task`：一个任务/工作项；
- `session`：一次交互会话；
- `environment`：一个世界、存档、模拟、设备或隔离环境状态。

词汇表由 registry 版本化。未知 kind 不得静默转换为更宽泛的 Scope。

### 5.3 Containment

候选 containment 语义：

- 在规范 Scope 树中，一个 Scope 至多有一个 **containment parent**；根节点为 BrainAuthority/system Scope。
- Containment 仅表示命名空间组织和生命周期归属，不表示权限继承或资源可见性。
- 跨域成员关系（例如一个 Agent 参与多个项目）通过显式类型化关联记录表达，不得设置多个 containment parent。
- Parent/child 环无效。重新指定 parent 是可审计的 Scope descriptor 变更；历史 parent 关系须通过版本历史保留。
- 一个对象有一个 owner ScopeRef 和零个或多个 applicability ScopeRef。归属与适用性是不同关系。

### 5.4 继承与组合

“继承”一词仅限领域元数据和校验：

- 子 Scope 只有在 Scope-kind registry 明确允许时，才可继承父 Scope 的描述性默认值或词汇约束。
- 子 Scope **不继承** grants、roles、permissions、读取可见性、写入权、retention 例外或授权决定。
- Parent Scope 成员身份不会自动使 child-scoped 资源对 parent-scoped 查询或 sibling Scope 可见。
- 跨多个 Scope 的适用性必须显式表达。命题依赖环境时，其 Environment Scope 是必需的；不兼容的 Environment Scope 不得被合并或当作相同对象比较。
- 领域操作的 Scope 组合是显式集合/关系约束，不是授权表达式。主体是否可执行操作由 I 决定。

### 5.5 归属与适用性

- **Owner Scope：** 除非未来治理批准共享所有权模型，否则每个规范对象恰有一个主要归属命名空间。
- **Applicability Scopes：** 命题/对象具有意义或预期适用的零个或多个 Scope。
- Child-scope 对象不会自动成为 owner-scope 对象。
- 跨 owner Scope 共享需要显式领域 sharing/link 记录及 I 授权。引用 hint 永远不是共享 grant。
- Scope mismatch 是领域校验结果；Permission Denied 是授权结果。两者是不同错误，不得混淆。

## 6. 跨模块消费者规则

- **D：** 存储稳定身份和精确不可变版本引用；校验引用存在性、类型、Scope 兼容性及 parent/version lineage。D 负责提交机制和生命周期权威。
- **E：** 从可信 ingress 携带源 EventRef、ScopeRefs 和 Environment Scope；映射批准前使用 candidate refs；绝不通过文本哈希创建规范 ClaimRef。
- **F：** 在候选暴露前按可信 Scope 上下文过滤候选生成；按精确引用及相关 Scope/policy epoch 为投影/缓存设键；重新校验规范引用并显式标注滞后/不完整。F 负责检索，不负责身份。
- **G：** Context entry 固定精确 MemoryVersionRef；不得把浮动 MemoryRef 当作内容版本证明。G 只负责 ContextVersion 和成员关系。
- **H：** 将这些语义序列化为版本化 Wire 形式，并把 ActorRef 绑定到已认证传输身份；B 不定义 Wire 格式。
- **I：** 解析授权、grants、撤销、保留和 Forget 策略。ScopeRef 单独永不构成授权。

## 7. 校验与一致性案例

1. 两个 BrainAuthority 命名空间中的相同 opaque object ID 不代表同一对象。
2. 两个 Scope 中相同的显示标签不能证明 Entity 身份相同。
3. 移动对象 applicability Scope 不会静默签发新身份。
4. Child Scope 不继承 Parent Permission，也不会使 sibling 资源可见。
5. EvidenceRef 不可访问时，MemoryRef 仍可能可读。
6. 历史/固定版本 Context 读取中，MemoryRef 不能替代 MemoryVersionRef。
7. 冲突、更正或 as-of 结果中，ClaimRef 不能替代 ClaimRevisionRef。
8. Event producer-local ID 冲突由已认证 producer 命名空间消解。
9. 未知时间不等于无界时间；近似时间保留精度/不确定性。
10. Retired Scope ID 和 forgotten object ID 永不复用。
11. Scope mismatch 与 Permission Denied 是不同的校验/授权结果。
12. 缺少显式兼容领域关系及 I 授权时，拒绝跨 Environment 候选匹配。

## 8. 依赖与未决事项

- **ADR-BLOCKED：** ClaimRef/ClaimRevisionRef 以 ADR-001 批准为前提；INT-P0-01 阻塞期间，不授权规范 Claim 身份。
- **与 I/H 的 OPEN 项：** ActorRef issuer、联邦、已认证 Principal 绑定、委托及撤销 epoch。
- **与 D 的 OPEN 项：** 精确版本/修订引用封套、对象生命周期历史和规范身份分配机制。
- **与 H 的 OPEN 项：** Wire 序列化及 schema 演进。
- **与 I 的 OPEN 项：** Scope/Permission 评估和 retention/Forget 策略。
- **TO_VALIDATE：** 高基数 Scope 组合、历史引用解析和 provenance 遍历限制。

## 9. 源基线与来源

| 来源 | 分支/ref | Commit SHA | Blob SHA |
|---|---|---|---|
| Governance invariants | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `66266667bdbb1cf15a2644fa98db5ecaaf3bb23b` |
| Governance principles | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `192e6ba6e9287792a02b679dda0d391844270228` |
| Terminology | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `9b287ebe027ae01128baf164952ce15aad050638` |
| 六份 Domain Model 文档 | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | 各 Blob SHA 见 ADR-001 源表 |
| D canonical store | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `4e4db0ed8847d060d235a1dedb394dfd4bda317d` |
| D versioning | 同上 | 同上 | `c32e58f7a845a9b075e68eb1c93f63649996d580` |
| D entity/relationship manager | 同上 | 同上 | `5688ef4fa682bc3e81aad5a9939e19ffc41ddf57` |
| E extraction/normalization | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `438f0c795fbcf8ed2c5e05615f1b96aa448efe85` |
| E consolidation/conflict | 同上 | 同上 | `bac3123d02e726ecffd8eb73ada515dea566e7e6` |

**分支说明：** D/E 引用来自各自尚未合并的分支及精确 commit；不表示这些内容已进入 main。

## 10. Phase 3.6 Scope / Environment 边界补充（CANDIDATE）

- **状态：** B 领域语义 CANDIDATE；I36-GOV-03 和 I36-GOV-04 仍为 GOVERNANCE-BLOCKED。
- **基线：** B HEAD `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`；此前 Blob `7c4517ee16e824f91c04306e000457662430ef69`。

### 10.1 ScopeRef、EnvironmentRef、Permission 与 Policy Domain 正交

- **ScopeRef** 标识对象/请求被解释时的归属或适用边界。
- **EnvironmentRef** 标识权威外部状态域（world/save/simulation/device fleet）；它不是 ScopeRef，也不是标签。
- **Permission** 是针对已认证 Principal、精确 action/resource、audience、purpose 及已解析 Scope/Environment 元组的决定；它不是引用。
- **Policy Domain** 是 I 用于策略评估/当前性及 PermissionEpoch 的分区；它不是 Scope，也不必与 tenant、project、environment 或 storage partition 相同。
- ScopeRef 或 EnvironmentRef 不授予任何权限。Scope 匹配不意味着 ALLOW。Policy-domain epoch 不标识资源。

### 10.2 候选 Scope 层级与命名空间

- Scope 身份由权威 Scope registry/security domain 和 opaque、永不复用的 Scope ID 构成命名空间；Scope kind 是 registry 校验的元数据，不是调用方选择的类型文本。
- 候选层级：BrainAuthority/system root → tenant → user/project/workspace → 由相关权威注册的 Agent/Agent-instance/task/session/environment Scope。这是领域分类提案，不强制每个部署实例化所有层级。
- 候选 containment 规则：每个 Scope 至多一个 containment parent；禁止环；重新挂接必须版本化/审计。跨域成员关系是显式 association，不是第二个 parent。
- 每个规范对象有一个 owner ScopeRef 和零个或多个带角色标签的 applicability ScopeRef，除非另有单独批准的共享所有权模型。
- Ownership Scope 表示保管/管理所有权；applicability Scope 表示命题/资源在哪些范围有意义。MUST NOT 将两者压平为一个无序并集。
- Scope version/descriptor 变更不改变稳定 ScopeRef 身份。若查询依赖历史 parent/descriptor，必须按版本解析。

### 10.3 跨 Scope 引用和访问规则

- 类型化关系只有在领域关系本身有效且两个端点均可解析时，才可引用另一 Scope 中的对象。存储引用不等于获得解引用权限。
- 默认不允许跨 Scope 可见性或操作。Parent/child、sibling、同一 Principal、同一 Agent、同一标签或同一 tenant 关系都不隐含 grant。
- Parent containment 仅是组织/领域元数据，绝不意味着权限继承、可见性继承、写入权、retention 例外或 policy-domain 等价。
- 如有显式 sharing/grant，必须由 I 授权，并绑定 recipient、action、resource、source/target Scope、audience、purpose、expiry 和 revocation。它们不改写所有权，也不合并命名空间。
- 每个 endpoint 以及每次 Evidence/Provenance 解引用都必须独立接受授权检查。
- Scope mismatch（领域关系不兼容）与 permission denial（策略禁止本来有效的操作）是不同结果。

### 10.4 跨 Environment 访问

- 绑定环境的 Event、Observation、Claim candidate、Memory 或 Relation 必须携带已解析 EnvironmentRef 及其必需的 Environment Scope 关联；自由文本标签、URL、世界名称或坐标不得替代身份。
- 两个环境中相同的 Agent、Principal、project label 或 Scope kind 不代表环境等价。
- 默认拒绝跨 Environment 引用/访问。Bridge 必须具备 registry-backed source/target EnvironmentRef、显式 mapping/relation、provenance、获授权的 recipient/action/purpose 和当前 I policy decision。
- EnvironmentRef 稳定身份与 environment revision 分离。身份之间存在 bridge 不意味着其 revision 或状态等价。
- 对依赖环境的操作，缺失或歧义的必需 EnvironmentRef 产生 INDETERMINATE/block，不得使用 wildcard/default environment。

### 10.5 校验与授权边界

1. 通过受保护的 H/I 边界认证 Principal/Issuer/RuntimeSession。
2. 对照权威 registry 解析 ScopeRef 和 EnvironmentRef；拒绝未知 type、issuer、namespace、kind 或 retired identity。
3. 校验 owner/applicability 角色、containment 兼容性、environment 绑定和领域关系。
4. 解析任何显式 delegation/sharing/bridge 引用；有效性策略归 I 所有。
5. 请求 I 对精确 action/resource/audience/purpose 及 source/target Scope/Environment 授权。
6. 在最终受保护 commit/disclosure 边界重新校验当前 I PermissionEpoch；D ForgetFence 和其他 Owner token 独立检查。

此顺序是 B 的候选校验契约，不是 I 授权策略或 H Wire schema。

### 10.6 未决决定

- **OPEN / I36-GOV-03 GOVERNANCE-BLOCKED：** 跨 Scope grant 模型、containment/sharing 代数及任何继承语义。
- **OPEN / I36-GOV-04 GOVERNANCE-BLOCKED：** 跨 Environment 联邦、bridge 准入和信任边界。
- **OPEN / I36-GOV-06 GOVERNANCE-BLOCKED：** policy-domain 分区及 PermissionEpoch 语义。
- **OPEN / I + B：** 权威 Scope registry owner、Scope kind registry 和稳定命名空间契约。
- **OPEN / H：** 精确序列化及多 Scope Wire 表示。
- **OPEN / D/E/C：** 精确 producer 字段、owner/applicability 角色名称及 EnvironmentRef 迁移/必需性。
- **CANDIDATE / B：** 单一 containment parent、不隐式继承权限、owner/applicability 区分及默认拒绝跨边界引用规则。

### 10.7 ADR 独立性

本补充不改变 ADR-001。Fact/Claim 规范身份、revision、attestation 和存储语义仍为 **ADR-BLOCKED**。Scope/Environment 类型化不意味着批准任何 Fact/Claim 方案。
