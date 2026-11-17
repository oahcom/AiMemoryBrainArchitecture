# Canonical Domain Invariants
# 规范领域不变量

- ID / 编号: B-INVARS-001
- Status / 状态: CANDIDATE INVARIANT SET — NOT EXECUTED / 候选不变量集 — 尚未执行
- Historical merge-base / 历史合并基点: `b372b62c640a2b656e54b6db62a4ee67d7d8c001` (not current main HEAD / 非当前 main HEAD)
- Owner boundary / Owner 权限边界: B defines domain-level invariants; D/E/F/G/H/I/Storage define and execute owner-local enforcement. / B 定义领域级不变量；D/E/F/G/H/I/Storage 定义并执行各自 Owner 范围内的强制措施。
- Gate / 门禁: B4 NOT READY; specifications are not executable proof. / B4 尚未就绪；规范说明不构成可执行证明。

## 1. Identity invariants / 身份不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| ID-001 | Identity is stable across ordinary content mutation / 普通内容变更不改变身份 | Memory label/content/version changes retain MemoryId. / Memory 标签、内容或版本变化时保留 MemoryId。 | Recompute ID from content or digest. / 根据内容或摘要重新计算身份 ID。 |
| ID-002 | Assigned canonical IDs are never silently reused / 已分配的规范 ID 不得静默复用 | Retired/forgotten ID remains historical and non-reassignable. / 已退役或已遗忘的 ID 保留为历史身份，不得重新分配。 | Reassign an old ID to a new object. / 将旧 ID 重新分配给新对象。 |
| ID-003 | Version identity is distinct from aggregate identity / 版本身份与聚合对象身份不同 | MemoryVersion references stable MemoryId and has a unique version ID. / MemoryVersion 引用稳定的 MemoryId，并具有唯一版本 ID。 | Treat MemoryVersionId as a new MemoryId. / 将 MemoryVersionId 当作新的 MemoryId。 |
| ID-004 | Typed refs preserve type and namespace / 类型化引用保留类型与命名空间 | Consumer resolves ActorRef only as ActorRef in the declared namespace. / 消费方只能在声明的命名空间内将 ActorRef 解析为 ActorRef。 | Cast PrincipalRef/AgentRef/ScopeRef through an untyped string. / 通过无类型字符串将 PrincipalRef/AgentRef/ScopeRef 相互转换。 |
| ID-005 | Ref is not proof of identity or permission / 引用本身不证明身份或权限 | Verifier + I registry resolve identity; I authorizes action. / 验证器与 I 的注册表解析身份；由 I 授权操作。 | Payload-supplied ActorRef authenticates caller. / 将载荷中提供的 ActorRef 当作调用方身份认证。 |
| ID-006 | Cross-tenant identity resolution is explicit / 跨 Tenant 身份解析必须显式进行 | Issuer/security domain/tenant namespace matches authoritative mapping. / Issuer、安全域和 Tenant 命名空间必须匹配权威映射。 | Resolve by subject string alone. / 仅凭 subject 字符串解析身份。 |

## 2. Relationship invariants / 关系不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| REL-001 | Relation endpoints satisfy type constraints / Relation 两端必须满足类型约束 | Relation type allows both endpoint kinds. / Relation 类型定义允许两端对象类型。 | Attach a Memory to a Person-only relation. / 将 Memory 连接到仅允许 Person 的 Relation。 |
| REL-002 | Derivation direction is explicit / 派生方向必须明确 | Target has source refs and lineage. / Target 具有来源引用及派生谱系。 | Source/target reversed or ambiguous. / Source 与 Target 方向颠倒或含义不明确。 |
| REL-003 | Derived object has complete lineage or explicit gap / 派生对象必须具有完整谱系或显式缺口 | All direct/transitive source versions are resolved, or an unavailable reason is recorded. / 所有直接及传递来源版本均已解析，或记录明确的不可用原因。 | Publish a derivative with unknown required ancestry. / 在必要祖先来源未知时发布派生对象。 |
| REL-004 | Unapproved derivation cycles are rejected / 未获批准的派生环必须拒绝 | Graph is acyclic under current candidate policy. / 按当前候选策略，派生图保持无环。 | Create a cycle without explicit approved semantics. / 未经明确批准的语义规则而创建环。 |
| REL-005 | Reference is not ownership or permission / 引用不代表所有权或权限 | Cross-scope link is separately authorized. / 跨 Scope 链接必须单独授权。 | Infer access from graph adjacency or parent scope. / 根据图邻接关系或父 Scope 推断访问权限。 |
| REL-006 | Context entry binds exact source version / Context Entry 绑定精确来源版本 | Entry references exact MemoryId + MemoryVersionId. / Entry 引用精确的 MemoryId 与 MemoryVersionId。 | ContextVersion scalar used as MemoryVersion. / 将 ContextVersion 标量当作 MemoryVersion。 |

## 3. Temporal invariants / 时间不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| TMP-001 | Temporal axes are non-interchangeable / 不同时间轴不得互换 | Occurred/Observed/Recorded/Valid/Transaction times retain separate meanings. / Occurred、Observed、Recorded、Valid、Transaction Time 保留各自独立含义。 | One timestamp populates all fields. / 使用同一个时间戳填充所有时间字段。 |
| TMP-002 | Unknown time is explicit / 未知时间必须显式表示 | Unknown/approximate retains source text and precision. / 未知或近似时间保留来源原文及精度信息。 | Missing time interpreted as epoch/always-valid. / 将缺失时间解释为 Epoch 或永久有效。 |
| TMP-003 | Valid Time and Record/Transaction Time histories remain distinct / Valid Time 与 Record/Transaction Time 历史保持区分 | Query can distinguish valid-at T from known-by T2 where supported. / 在能力支持时，查询可区分“T 时有效”与“T2 时已知”。 | Backdated correction overwrites historical knowledge. / 通过回填修正覆盖历史上当时已知的信息。 |
| TMP-004 | Temporal correction is provenance-bearing / 时间修正必须具有溯源记录 | New immutable assertion/revision records reason and source. / 新的不可变断言/修订记录修正原因与来源。 | Silent mutation of historical Valid Time. / 静默修改历史 Valid Time。 |
| TMP-005 | Time order is not inferred from independent clocks alone / 不得仅凭独立时钟推断因果顺序 | Causal order uses owner-authoritative cursor/receipt. / 因果顺序使用 Owner 权威游标或 Receipt。 | Wall-clock comparison substitutes for causal proof. / 用墙上时钟比较替代因果证明。 |

## 4. Evidence and provenance invariants / 证据与溯源不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| EVD-001 | Verified Claim requires evidence and method / Verified Claim 必须具备证据和方法 | Claim references evidence and verification method. / Claim 引用 Evidence 及验证方法。 | Confidence score alone promotes to Verified. / 仅凭 Confidence 分数将 Claim 提升为 Verified。 |
| EVD-002 | Evidence role/strength is Claim-relative / Evidence 角色与强度相对于 Claim | Link records support/refute/qualify role per Claim. / 关联记录按每个 Claim 记录支持、反驳或限定角色。 | Evidence has one global strength reused for all Claims. / 为 Evidence 设置一个全局强度并套用于所有 Claim。 |
| EVD-003 | Source, Evidence and Provenance are distinct / Source、Evidence 与 Provenance 相互独立 | Source origin, evidence material and derivation trace are independently identified. / 分别标识来源起点、证据材料和派生轨迹。 | Derived summary is represented as original source. / 将派生摘要表示为原始来源。 |
| EVD-004 | Provenance names exact inputs where available / 在可用时 Provenance 必须标识精确输入 | Input object/version/digest/method version recorded. / 记录输入对象、版本、摘要和方法版本。 | Model/method guessed after the fact. / 事后猜测模型或方法。 |
| EVD-005 | Unavailable evidence is not nonexistence / Evidence 不可用不等于其从未存在 | State records expired/forgotten/external unavailable. / 状态明确记录过期、已遗忘或外部不可用。 | Missing blob treated as proof that source never existed. / 将 Blob 缺失视为来源从未存在的证明。 |
| EVD-006 | Forget retention does not preserve forgotten plaintext / Forget 后的保留信息不得保留已遗忘明文 | Only permitted non-reconstructive audit metadata retained. / 仅保留政策允许且不可重建内容的审计元数据。 | Provenance excerpt/digest side channel reconstructs forgotten content. / 通过 Provenance 摘录或摘要侧信道重建已遗忘内容。 |

## 5. State invariants / 状态不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| ST-001 | State is typed by subject and owner / 状态必须绑定明确主体和 Owner | Memory lifecycle uses Memory state machine. / Memory 生命周期使用 Memory 自身状态机。 | Universal status enum used for all entities. / 对所有实体使用通用状态枚举。 |
| ST-002 | Epistemic status is independent from Memory lifecycle / 认知状态独立于 Memory 生命周期 | Active Memory may contain Disputed Claim. / Active Memory 可以包含 Disputed Claim。 | Memory Active interpreted as Claim Verified. / 将 Memory Active 解释为 Claim Verified。 |
| ST-003 | Terminality is owner-defined / 终态由对应 Owner 定义 | Transition checks subject's exact state machine. / 转换依据主体所属的精确状态机检查。 | Same-named state from another module is assumed equivalent. / 假定其他模块的同名状态语义等价。 |
| ST-004 | Forgotten is not a ForgetOperation phase / Forgotten 不是 ForgetOperation 阶段 | D operation phases are separate from Memory Forgotten lifecycle. / D 的操作阶段与 Memory 的 Forgotten 生命周期状态分离。 | Memory.status = Forgetting treated as canonical. / 将 Memory.status = Forgetting 当作规范状态。 |
| ST-005 | Applied, Recorded, Committed, Visible and Published are distinct / Applied、Recorded、Committed、Visible、Published 相互区分 | Each requires correct issuer/evidence. / 每种状态都要求正确的签发方和证据。 | ACK/COMMIT_WON/local state treated as Published or Applied. / 将 ACK、COMMIT_WON 或局部状态当作 Published 或 Applied。 |
| ST-006 | Unknown is not success / Unknown 不等于成功 | Unresolved outcome remains Unknown/InDoubt/Blocked. / 未解决结果保持 Unknown/InDoubt/Blocked。 | Timeout/lost ACK converts to success. / 将超时或 ACK 丢失转换为成功。 |

## 6. Forget and deletion invariants / 遗忘与删除不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| FGT-001 | Forget is not ordinary Delete / Forget 不是普通 Delete | D ForgetOperation/Fence governs suppression and lineage. / D 的 ForgetOperation/Fence 管理抑制及谱系。 | Generic row deletion called Forget. / 将普通行删除称为 Forget。 |
| FGT-002 | Request, authorization, decision, execution and proof are distinct / 请求、授权、决策、执行和证明相互区分 | Request ref, I decision, D fence, per-target receipts and I global result are separate. / Request 引用、I 决策、D Fence、逐目标 Receipt 和 I 全局结果分别记录。 | One status field represents whole Forget. / 用一个状态字段代表整个 Forget 流程。 |
| FGT-003 | D suppression is not global completion / D 抑制完成不等于全局完成 | D CanonicalSuppressionComplete is scoped to D barrier. / D 的 CanonicalSuppressionComplete 仅适用于 D Barrier 范围。 | D declares all backups/external copies erased. / D 宣称所有备份及外部副本均已擦除。 |
| FGT-004 | Logical suppression is not physical purge / 逻辑抑制不等于物理清除 | Storage/backup operator emits target-scoped purge proof. / Storage 或备份操作方签发按目标限定的清除证明。 | Missing row/tombstone treated as physical erase. / 将行缺失或 Tombstone 当作物理擦除证明。 |
| FGT-005 | No resurrection by new ID/content equality / 不得通过新 ID 或内容相同绕过遗忘 | New ingestion checks active fences and lineage/source ancestry. / 新摄取检查有效 Fence 及谱系/来源祖先。 | Same content reintroduced with new ID bypasses Forget. / 通过新 ID 重新引入相同内容以绕过 Forget。 |
| FGT-006 | Historical evidence does not authorize current use / 历史证据不授权当前使用 | Applied/history retained under I policy but current-use eligibility is recomputed. / 按 I 政策保留 Applied/历史记录，但重新计算当前使用资格。 | Old Applied/ACK authorizes resend after revocation/Forget. / 撤销或 Forget 后仍凭旧 Applied/ACK 授权重发。 |

## 7. Operation and protocol invariants / 操作与协议不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| OPR-001 | Protocol object is not domain operation / 协议对象不是领域操作 | Request references an operation ID/type. / Request 引用 Operation ID/Type。 | Request payload itself becomes canonical Memory. / 将 Request 载荷本身变为规范 Memory。 |
| OPR-002 | Receipt proves only declared boundary / Receipt 只证明其声明的边界 | Receipt includes issuer, scope, operation, version and result. / Receipt 包含签发方、Scope、操作、版本和结果。 | ACK expanded beyond declared coverage. / 将 ACK 的证明范围扩大到其声明覆盖范围之外。 |
| OPR-003 | Retry preserves logical identity and digest / 重试保留逻辑身份和摘要 | Same key + same digest is idempotent; changed digest is conflict. / 相同 Key 与相同 Digest 幂等；Digest 改变则冲突。 | Retry creates new operation to evade fence. / 通过创建新操作绕过 Fence。 |
| OPR-004 | Owner-local cursors/epochs are typed / Owner 局部 Cursor/Epoch 必须类型化 | D cursor, I PermissionEpoch, F watermark, G version, Storage XID remain separate. / D Cursor、I PermissionEpoch、F Watermark、G Version、Storage XID 保持分离。 | Compare unrelated counters as global order. / 将无关计数器比较为全局顺序。 |
| OPR-005 | Publication requires Storage authority / 发布必须由 Storage 权威确认 | VisibilityPointer and PublicationReceipt are read back. / 回读 VisibilityPointer 和 PublicationReceipt。 | I COMMIT_WON or E local Published state exposes bytes. / 仅凭 I COMMIT_WON 或 E 局部 Published 状态暴露数据。 |

## 8. Authentication and physical-order invariants / 认证与物理顺序不变量

| ID | Invariant / 不变量 | Positive condition / 正向条件 | Negative condition / 负向条件 |
|---|---|---|---|
| AUTH-001 | C origin signature, H transport authentication and I authorization are separate / C 来源签名、H 传输认证和 I 授权相互独立 | Each is verified by its authority and bound to exact message/context. / 每项均由其权威方验证，并绑定精确消息/上下文。 | Treat payload sender claim or H gateway receipt as C origin proof. / 将载荷中的发送方声明或 H Gateway Receipt 当作 C 来源证明。 |
| AUTH-002 | C object P0 and outer-envelope P0 are distinct / C 对象 P0 与外层 Envelope P0 不同 | Both are independently computed/verified under exact profile and object. / 二者依据各自精确 Profile 和对象独立计算/验证。 | Reuse C object P0 as outer-envelope P0 without explicit approval. / 未经明确批准将 C 对象 P0 复用为外层 Envelope P0。 |
| AUTH-003 | Missing trust evidence is UNKNOWN, never VALID / 缺少信任证据时为 UNKNOWN，绝不能视为 VALID | Missing profile/key history/anti-rollback/principal fails closed. / 缺少 Profile、密钥历史、防回滚或 Principal 信息时 Fail Closed。 | Treat absent trust data as permissive. / 将缺失的信任数据视为允许通过。 |
| AUTH-004 | Protected transport context is verifier-produced / 受保护传输上下文必须由验证器生成 | Context is constructed only by authenticated adapter and bound to channel/session. / Context 只能由经过认证的 Adapter 构造，并绑定 Channel/Session。 | Caller constructs context from payload claims. / 调用方根据载荷声明自行构造 Context。 |
| AUTH-005 | Replay reservation is durable and ordered / Replay Reservation 必须持久且有序 | Reservation/acceptance/prior-result publication have explicit crash-safe semantics. / Reservation、Acceptance 和既有结果发布具有明确的崩溃安全语义。 | In-memory replay set or reserve before required auth checks. / 使用内存 Replay Set，或在必要认证检查前执行 Reservation。 |
| SER-001 | SerializationRevision is local to one physical anchor / SerializationRevision 仅属于单个物理 Anchor | Revision compares only within one AuthoritySerializationAnchorRef. / Revision 只能在同一个 AuthoritySerializationAnchorRef 内比较。 | Compare to D FenceGeneration, I PermissionEpoch, C sequence, COC position or XID. / 将其与 D FenceGeneration、I PermissionEpoch、C Sequence、COC Position 或 XID 比较。 |
| SER-002 | SerializationTransitionRef idempotency includes immutable digest / SerializationTransitionRef 幂等性包含不可变 Digest | Same ref + same digest replays same result. / 相同 Ref 与相同 Digest 重放相同结果。 | Same ref + different digest silently accepted. / 相同 Ref 配不同 Digest 却静默接受。 |

## 9. Candidate executable test catalogue / 候选可执行测试目录

| Test ID | Setup / 前置条件 | Expected result / 预期结果 | Owner |
|---|---|---|---|
| T-ID-01 | Change Memory label/content and create next version. / 修改 Memory 标签/内容并创建下一版本。 | MemoryId stable; MemoryVersionId new. / MemoryId 保持稳定；MemoryVersionId 为新 ID。 | D/Storage |
| T-ID-02 | Reuse retired ID under different object. / 在不同对象上复用已退役 ID。 | Reject. / 拒绝。 | B/D/Storage |
| T-ID-03 | Submit forged PrincipalRef/ActorRef in payload. / 在载荷中提交伪造的 PrincipalRef/ActorRef。 | Not authenticated; fail closed. / 不视为已认证；Fail Closed。 | H/I |
| T-REL-01 | Relation with disallowed endpoint type. / Relation 使用不允许的端点类型。 | Reject with invariant ID. / 按不变量 ID 拒绝。 | B/E |
| T-REL-02 | Derived artifact missing ancestor source version. / 派生工件缺少祖先来源版本。 | Quarantine/private. / 隔离并保持私有。 | E/D/Storage |
| T-TMP-01 | Event occurred before observation and later durable recording. / Event 发生早于观察，之后才持久记录。 | All time axes remain distinct. / 所有时间轴保持区分。 | C/E/D |
| T-TMP-02 | Approximate time “early May”. / 近似时间“五月初”。 | Preserve uncertainty/source text; no exact fabricated instant. / 保留不确定性和来源原文；不得伪造精确时刻。 | E |
| T-EVD-01 | Mark Claim Verified without evidence/method. / 没有 Evidence/Method 却将 Claim 标记为 Verified。 | Reject. / 拒绝。 | E/D |
| T-EVD-02 | One Evidence supports and refutes different Claims. / 同一 Evidence 支持一个 Claim、反驳另一个 Claim。 | Per-link roles retained. / 分别保留每条关联的角色。 | B/E |
| T-ST-01 | Active Memory contains Disputed Claim. / Active Memory 包含 Disputed Claim。 | Valid; lifecycle and epistemic dimensions independent. / 有效；生命周期与认知维度相互独立。 | D/F |
| T-ST-02 | I COMMIT_WON but Storage participant not committed. / I 已 COMMIT_WON，但 Storage Participant 未提交。 | Not Published; remain private/unknown. / 不得视为 Published；保持私有/未知。 | I/Storage/E |
| T-ST-03 | Context delivered ACK without C final submit proof. / Context 已收到 Delivered ACK，但没有 C 最终提交证明。 | Not Applied. / 不得视为 Applied。 | H/C/G |
| T-FGT-01 | D fence wins before derived publication. / 派生发布前 D Fence 获胜。 | Reject/quarantine; no visibility. / 拒绝/隔离；不得可见。 | D/E/Storage |
| T-FGT-02 | D suppression completes but backup target unresolved. / D 抑制完成，但备份目标尚未解决。 | Not global Forget complete. / 不得视为全局 Forget 完成。 | D/I/Storage |
| T-FGT-03 | Reimport same forgotten source under new Memory ID. / 使用新 Memory ID 重新导入相同的已遗忘来源。 | Block by lineage/fence policy. / 根据谱系/Fence 政策阻止。 | D/E/I |
| T-OPR-01 | Same operation key with changed digest. / 相同 Operation Key 配不同 Digest。 | Conflict. / 冲突。 | Owner operation / 操作 Owner |
| T-OPR-02 | Compare PermissionEpoch with ForgetFenceGeneration. / 比较 PermissionEpoch 与 ForgetFenceGeneration。 | Type error/reject. / 类型错误并拒绝。 | I/D/B |

## 10. Validation status / 验证状态

- Test specifications are recorded above; they are not executable results. / 测试规范已记录于上文；它们不是可执行测试结果。
- JSON Schema: NOT CREATED; core identity/Fact-Claim/Applied schemas are not stable enough to freeze. / JSON Schema：尚未创建；核心身份、Fact/Claim/Applied Schema 尚不稳定，不可冻结。
- Executable tests: NOT RUN; this repository is an architecture-definition repository and Issue #7 identifies runtime implementation location/owner as unresolved. / 可执行测试：尚未运行；本仓库是架构定义仓库，Issue #7 指出运行时实现位置/Owner 尚未确定。
- Property-based tests: TO_VALIDATE after nominal type/identity and state machine decisions stabilize. / 属性测试：待名义类型/身份及状态机决策稳定后验证。
- Fault injection: NOT RUN; JF-10 P0 remains open (Issue #10). / 故障注入：尚未运行；JF-10 P0 仍开放（Issue #10）。

## 11. Gate status / 门禁状态

B4 is NOT READY. Invariants are candidate and owner-scoped; test specifications are not executable proof. No schema or runtime conformance is claimed.

B4 尚未就绪。不变量仍为候选且按 Owner 划分；测试规范不是可执行证明。不宣称 Schema 或运行时一致性。
