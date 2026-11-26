---
document_metadata:
  domain: protocol
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Work Item AID-2026-099"
        - "Issues #1212, #1208, #1135"
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "仅为候选合同；不声称实现、生产持久性、多副本线性化或跨 Owner 接受。"
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "H BMCP 幂等命名空间、请求去重、持久回执、线性化与重放边界"
    canonical_scope_id: "bmcp-protocol/h-idempotency-replay-boundary"
    canonical_scope_keywords:
      - bmcp
      - idempotency
      - namespace
      - replay
      - durable-receipt
      - linearization
      - unknown
      - attempt-identity
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md"
    en: "docs/en/08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md"
---

# H 幂等命名空间与重放边界合同

- 合同 ID：H-IDEMPOTENCY-REPLAY-001；版本 0.1.0。
- 状态：**Draft / Candidate / Informative**；未批准、非规范性、非线缆/Schema 冻结。
- 工作项：AID-2026-099（PROVISIONAL）。
- H 拥有 BMCP 请求身份、传输 Attempt、协议回执与重放披露。H 不拥有 C Provider Outcome 真值、G Applied、D ForgetFence、I 授权策略或 Storage 物理原子性。

## 1. 阅读规则与术语

本文是候选提案，不是实现证据。MUST/MUST NOT 是拟议合同要求，不代表当前已批准规范。DOCUMENTED_ONLY 检查文本是否定义规则；EVIDENCE_REQUIRED 必须提供精确版本实现、存储、符合性或 Owner 证据，不能仅凭文字通过。

- **逻辑操作：** 一次语义意图，在传输重试中保持稳定。
- **幂等键：** 调用方生成的稳定 Token，在显式 authority/scope/operation 命名空间内标识该逻辑操作。
- **Attempt ID：** 一次具体入口/传输执行。每次重试均为新 Attempt。
- **回执：** 对准入或终态结果的不可变证据；不证明 C Provider 成功或 G Applied。
- **Duplicate：** 请求处置分类，不是持久生命周期状态。

## 2. 权限边界与精确源 pin

| 事项 | 权限归属 | H 边界 |
|---|---|---|
| BMCP 封套、请求/Key 绑定、传输 Attempt、协议回执和重放响应 | H | 本候选定义拟议 H 侧边界 |
| Provider handoff outcome 与不可变 CSubmitOutcome | C | H 解析/认证精确 C 记录；不得改写 C Outcome 或 SideEffectStatus |
| Applied 决策及 AppliedAttestation / DeliveryAttempt 关联 | G | H receipt/ACK 不等于 Applied；仅 G 拥有 Applied |
| ForgetOperation、Fence generation、目标 lineage 与 suppression | D | 重放披露前复核 D 当前性；H 不创建、推进或清除 Fence |
| 当前授权、PermissionEpoch、issuer/key 状态和重放授权 | I | H 调用 I 所有的当前授权；历史签名不足以授权 |
| 业务变更、幂等原子性、提交/恢复和物理存储 | Storage | H 消费 Storage 证据，不定义后端 Schema 或事务协议 |

从 main 基线 **d5107f68a7f1b61f5f2f7352fadf828aae06cf1c** 读取：
- 07-agent-integration/applied-evidence-contract.md — Blob **273efdd1b02bd9302fc968f07c6d094da2582a6e**：H receipt/ACK 不等于 Applied；重试保持逻辑 Delivery ID 并使用不同 Attempt ID；G 仅从已验证的不可变 C/H 证据投影 Applied。
- 06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md — Blob **833815e37ac8d7505d93a0a115421dafe3eb08ad**：G 拥有唯一持久的每请求 Applied 决策；H 证据只是多个谓词之一；适用 JF-10 时要求 Storage same-GID 终态解析及原子 VisibilityPointer/PublicationReceipt 或 non-publication 证明。
- 01-system-architecture/forget-fence-and-completion-contract.md — Blob **760a1d48011f2a66c23abcf825a3d067e79b8821**：D 拥有 ForgetOperation/Fence 和 canonical suppression；I 拥有授权、保留策略和全局完成；H 拥有 wire、Adapter 本地状态、重连及可信应用/清除确认。
- 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md — Blob **d83cde77e98db2e74cf6827d874b0babb4157304**：其 namespace 是 D 的 ProducerWork Registration Ledger namespace，不是 H 幂等命名空间；不得别名或复用。
- 02-domain-model/phase-1-storage-trait-contract.md — Blob **22ca7cd3777e0132e25f084084610f1e90b60d21**：候选 Storage seam 规定 immutable version、current-version CAS、idempotency record 和 canonical commit sequence 属于同一可恢复边界；同 key/同 digest 可返回原回执；同 key/不同 digest 是 IdempotencyConflict。形状测试不证明后端原子性/持久性。
- H Phase 3.8.25 — Blob **afa294bc42a8488e4569e6a8bdf5437c7a90e247**；H Phase 3.8.26 — Blob **7b73491c765091728af6f5306b9efd502cf7f30a**：重放披露前独立检查 I 当前授权和 D Fence，并精确关联 CSubmitOutcome record/sequence/payload-digest/final-boundary；resolver/verifier seam 尚未验证。

**Storage / AID-2026-098 依赖：** 此 main 基线不存在 AID-2026-098 目录或 manifest，也未发现该编号的 PR。因此其精确 Storage 合同版本/blob 为 **NOT AVAILABLE ON THIS BASELINE**。本提案将 Storage 原子性与持久化细节留给 AID-2026-098，不臆造或重复定义。跨 Owner 冻结前，必须 pin 其精确路径/版本/blob 并核验 H/Storage 映射。上述 Storage Trait 只是候选 seam，不能替代 AID-2026-098。

## 3. 幂等命名空间与 Key 所有权

### 3.1 拟议查找身份

查找身份是完整元组，不是裸 Key：

**HIdempotencyIdentity = (protocol_domain, authority_ref, tenant_or_scope_ref, operation_kind, key_profile, idempotency_key)**

- protocol_domain：固定 H/BMCP 域标识和合同族。
- authority_ref：拥有此操作命名空间的 Authority。
- tenant_or_scope_ref：已解析的 tenant/canonical scope 身份，不是展示字符串。
- operation_kind：区分语义不同的命令。
- key_profile：约定的 opaque-key 编码/版本。
- idempotency_key：调用方生成的不透明值。

**默认作用域为 per authority + tenant/scope + operation kind**，不是 per-agent、per-session 或 per-attempt。Agent 和 Session 是绑定请求属性及授权输入，不是默认去重维度。明确归属 Agent 的操作，只有经单独审查的 profile 才能加入稳定的 agent_authority_ref。Session 轮换/重连不得创建新逻辑操作。Attempt ID 永不属于幂等 Key。

### 3.2 生成与碰撞隔离

1. 发起操作的 Producer/Client 在首次发送前生成一个 opaque key，并在重试/重连中保留。
2. 不得仅因 timeout、ACK 丢失或 reconnect 由 H 生成新 Key。
3. 每次传输执行分配新的 H Attempt ID。
4. Key profile 必须提供适合部署环境的抗碰撞唯一性。Entropy/encoding 细节等待 H/I 安全审查；本文不选择 UUID/hash/密码算法。
5. Namespace 组件在比较/索引前使用无歧义、带版本、长度分隔的规范元组编码。禁止有歧义的分隔符拼接。
6. 不同 authority、tenant/scope 或 operation kind 下相同裸 Key 是不同身份。同一完整元组但 request digest 不同则是 Conflict，不是第二个操作。
7. Key 不得仅由可变 Session ID、Agent 展示名、时间戳、payload digest 或 Attempt ID 派生。

### 3.3 Request digest 绑定

首次接受将完整 namespace 元组绑定到一个不可变 request digest 和精确 final request boundary。Digest 算法、规范序列化、volatile transport 字段处理和 profile 协商由适用 C/H 合同拥有，必须一致 pin；本文不创建竞争的 digest profile。重试必须复现相同语义 digest。语义 payload 变化必须创建新逻辑操作和新 Key。

## 4. 去重窗口与持久化

- 去重从权威 H replay ledger 持久保留完整元组及 request digest 时开始，不是内存缓存。
- 记录及 replay-protection tombstone 至少保留到 Owner policy 声明的最大重试/恢复/重放期限。本文不臆造固定时长。若没有安全的有限期限，只要重放仍可能产生副作用，就不得静默过期该身份。
- 响应正文/telemetry 到期不允许复用 Key。紧凑 tombstone 仍须在要求期限内拒绝冲突复用。
- H 协议回执/重放元数据保存在 H 所有的持久 ledger。业务变更、immutable domain version、CAS、idempotency record 和 canonical commit sequence 由 Storage 所有，并遵循 AID-2026-098。
- H admission receipt 不证明 Storage 业务提交。Storage prepared receipt 本身也不是 G Applied。
- 若 H 与 Storage ledger 无法按适用 Storage/COC 合同原子更新，操作保持 Pending/Unknown，直到 reconciliation 证明终态。

## 5. 线性化点

存在两个不同的点：

1. **H admission 线性化：** 权威 H replay ledger 提交完整元组、request digest、logical operation 引用和首个 Attempt ID 的唯一 reservation，并生成持久 admission receipt 的时刻。并发竞争必须串行化为一个赢家。此前请求未被持久接受；此后重试解析到同一逻辑操作。
2. **Domain-effect 线性化：** Storage AID-2026-098 定义的业务变更及其 idempotency receipt/canonical commit sequence 作为一个可恢复边界提交的时刻。H 不定义该事务，H admission 不意味着该点已发生。

C final request boundary、CSubmitOutcome 和 G Applied 线性化仍由 C/G 独立治理。H 线性化不意味着 Provider handoff、Adapter application 或 G Applied。

## 6. 持久回执与不可变性

候选回执最小字段（仅字段词汇，不是冻结 Schema）：

~~~yaml
receipt_schema: h-idempotency-receipt/0.1
receipt_id: <stable opaque ID>
protocol_domain: <H/BMCP domain>
namespace:
  authority_ref: <authority>
  tenant_or_scope_ref: <resolved scope>
  operation_kind: <operation>
  key_profile: <profile version>
  idempotency_key: <opaque key>
logical_operation_id: <stable logical operation ID>
request_digest: {profile: <pinned profile>, value: <digest>}
final_request_boundary_ref: <immutable boundary ref>
first_attempt_id: <H attempt ID>
observed_attempt_id: <current/retry attempt ID>
receipt_state: <PENDING | SUCCEEDED | FAILED>
disposition: <NEW | DUPLICATE | CONFLICT>
admitted_at: <UTC timestamp>
terminal_at: <UTC timestamp or null>
domain_commit_ref: <Storage-owned ref or null>
c_outcome_ref: <C-owned immutable ref or null>
applied_attestation_ref: <evidence ref consumed by G or null>
issuer: {authority_ref: <H authority>, key_ref: <verification key ref>}
integrity: {profile: <pinned profile>, digest: <receipt digest>, proof_ref: <signature or immutable proof>}
~~~

回执还绑定经认证 caller/principal 和 I 授权决策引用，但二者不能替代重放时的当前授权。回执不复制敏感 payload 明文。

- admission 后 receipt_id、namespace 元组、logical operation ID、request digest、final boundary 和 first Attempt ID 不可变。
- 重试创建新 Attempt ID 和 append-only observation，不覆盖回执或旧 Attempt 证据。
- 状态变化通过 append-only transition/evidence record 表示。可缓存可变 latest-status 投影，但它不是审计源。
- 终态回执不得从 SUCCEEDED 改写为 FAILED 或反向改写。更正需新建关联记录，明确 issuer/reason，原记录保留。
- Receipt digest/signature 认证精确不可变字段和证据引用。密码 profile 等待 H/I 注册和接受。

## 7. 失败与重复语义

| 状态/处置 | 含义 | 规则 |
|---|---|---|
| Unknown | 无法确认权威持久 reservation/终态记录，或 lookup/recovery authority 不可用。是认知状态，不证明没有副作用。 | 用相同元组/key/digest、全新 Attempt ID 重试；查询/协调权威 ledger。不得声称成功或可安全创建新 Key。 |
| Pending | H durable reservation 已存在，尚无权威 domain 终态。 | 同 key/同 digest 返回 Pending/既有回执；协调 Storage/C 证据；不得执行第二个逻辑操作。 |
| Failed | 权威持久终态失败已记录。 | 同 Key 返回同一终态失败。终态失败后的新语义尝试是新逻辑操作，使用新 Key 和显式 successor link。 |
| Duplicate | 当前请求匹配既有元组/key/digest。是响应处置，不是持久状态。 | 返回既有 receipt/state，不重复副作用。披露受保护结果前重新检查 I 授权和 D Fence。 |
| Conflict | 相同完整元组/key 对应不同 request digest。 | 拒绝为 IdempotencyConflict；不修改旧回执，不创建另一操作。 |

Timeout、连接丢失、崩溃、ACK 缺失、ledger 不可用、签名不可验证或恢复不完整均为 Unknown/Pending，不是 Failed。Failed 必须有权威终态失败证据。H admission 前的验证/授权拒绝是 non-accepted，不得误报为持久操作失败。

## 8. 重放与崩溃恢复

1. 同一逻辑操作重试复用完整元组、Key、logical operation ID 和 request digest。
2. 每次传输执行使用新 Attempt ID；Attempt 证据按 logical operation + Attempt ID 追加保存。
3. 恢复先解析既有 H receipt，再解析 Storage AID-2026-098 transaction/receipt。stale replica 中缺少记录或 timeout 不证明“未提交”。
4. Storage 报告已提交时，H 仅在当前 replay authorization 和 Fence 检查通过后返回不可变结果引用。持久终态 abort/failure 返回终态。Storage 未解决则保持 Pending/Unknown 并 reconciliation，不重复业务副作用。
5. H reservation 后、domain commit 前崩溃，reservation 保持 Pending 并协调。domain commit 后、H terminal projection 前崩溃，恢复读取 Storage commit receipt 并追加 H terminal observation，不得再次执行变更。
6. 新逻辑操作、语义 payload 变化或终态后的显式 successor 使用新 Key 和 logical operation ID。可关联前序操作，但不复用 receipt identity。

### 8.1 C/G Applied 关联

- H receipt/delivery ACK 仅证明 H 协议/传输事实。
- H 证据按 record ref、sequence、payload digest、final request boundary 精确关联不可变 CSubmitOutcome；若 C 提供 ActualInferenceRequestId，必须等于 H inference request ID。
- C 独自拥有 Outcome 和 SideEffectStatus。H 不得从 transport ACK 推断 Provider 成功或改写 C outcome。
- G 独自拥有持久 Applied。G 消费认证后的 H 证据、C outcome、COC/Storage same-GID 终态证明、I 授权、D Fence lineage 和 G 自身谓词。
- 按 AID-2026-091 AP-02/AP-09，逻辑 Delivery ID 在重试中保持稳定，每次重试使用不同 DeliveryAttempt ID。H Attempt ID 必须明确映射到该身份。重试回执不得覆盖旧 AppliedAttestation。ACK 丢失仍为 Unknown/Pending，绝非 Applied。

## 9. Fence 与重放披露

历史上有效的 receipt 不构成永久披露许可。返回既有结果或受保护回执字段前，H 独立重新检查：
- I 当前授权、PermissionEpoch、issuer/key 状态、principal/delegation、audience 和 scope；
- D 当前 ForgetOperation/Fence/lineage 适用性与当前性。

两项检查均 fail-closed：任一 False/denied 则不披露受保护结果；任一 Unknown/unavailable/exception 则不披露并返回不含受保护结果的 Unknown/authorization-pending；仅两者均当前有效才披露获准的 receipt/result 引用。D 拥有 Fence generation/lineage/suppression。I 拥有授权/撤销及全局 Forget policy。H 不清除 Fence，也不把 replay 当成重新物化已遗忘内容的许可。历史回执不可变，即使当前使用/披露资格被撤销。

## 10. 非目标与未决事项

本文不定义 Storage schema、数据库事务、WAL/fsync profile、COC same-GID 协议、VisibilityPointer 或 PublicationReceipt；这些属于 Storage/AID-2026-098。本文不定义 CSubmitOutcome 或 G Applied 语义、D namespace canonicalization/Fence generation、I policy、密码 Key/签名/hash/canonical JSON/entropy profile，也不设固定去重 TTL。不声称生产多副本线性化、持久重放、崩溃恢复或 runtime conformance。

未决事项：H/I 接受 Key/receipt profile；AID-2026-098 精确 Storage pin 和保留映射；H Attempt ID ↔ C/G DeliveryAttempt 映射；C/G/H 接受 digest/final-boundary join；D/I replay callback 证据；Owner 接受 H admission 线性化。

## 11. 审查检查点

PASS/FAIL 必须针对精确文档版本和证据记录。DOCUMENTED_ONLY 可通过文本检查；EVIDENCE_REQUIRED 不能仅凭 prose 或本地形状测试通过。

| ID | PASS 条件 | FAIL 条件 | 证据 |
|---|---|---|---|
| HIR-01 | 完整元组包含 protocol domain、authority、resolved scope、operation kind、key profile、opaque key | 仅裸 Key 或有歧义元组 | DOCUMENTED_ONLY |
| HIR-02 | Producer 每逻辑操作生成一个 Key 并在重试保留 | timeout/reconnect 轮换 Key | DOCUMENTED_ONLY |
| HIR-03 | Agent/session 是绑定属性而非默认去重维度；Attempt 独立 | Session/Agent/Attempt 拆分同一逻辑操作 | DOCUMENTED_ONLY |
| HIR-04 | namespace 编码无歧义且跨域隔离 | 有歧义拼接/跨 scope 别名 | DOCUMENTED_ONLY |
| HIR-05 | 去重始于 H durable reservation；tombstone 超过 replay horizon | 仅内存或过早过期允许重复副作用 | EVIDENCE_REQUIRED |
| HIR-06 | Storage mutation、version/CAS、idempotency receipt、commit sequence 遵循 AID-2026-098 原子边界 | H 自创 Storage 原子性或部分写被视为提交 | EVIDENCE_REQUIRED |
| HIR-07 | H admission LP 是持久唯一 reservation；domain-effect LP 归 Storage | admission 与业务提交混淆 | DOCUMENTED_ONLY |
| HIR-08 | 并发同 Key 竞争只产生一个逻辑操作和持久回执 | 双赢家或无可恢复赢家 | EVIDENCE_REQUIRED |
| HIR-09 | Receipt 绑定 namespace、digest、logical operation、first/current Attempt、boundary、issuer、proof refs | 身份/来源缺失或可变 | DOCUMENTED_ONLY |
| HIR-10 | Receipt identity 不可变；转换 append-only | 重试覆盖 receipt/终态 | DOCUMENTED_ONLY |
| HIR-11 | timeout/crash/resolver 不可用/证据不可验证保持 Unknown/Pending | 将不确定性推断为成功或终态失败 | DOCUMENTED_ONLY |
| HIR-12 | Pending duplicate 返回既有 receipt，不执行第二逻辑操作 | Pending duplicate 启动另一副作用 | EVIDENCE_REQUIRED |
| HIR-13 | Failed 需要持久权威终态失败 | 临时/模糊错误成为终态 Failed | DOCUMENTED_ONLY |
| HIR-14 | 同 Key/同 digest 是 Duplicate；不同 digest 是 Conflict | mismatch 返回旧成功或修改旧 receipt | EVIDENCE_REQUIRED |
| HIR-15 | 同逻辑重试复用 Key/logical ID；每次传输重试新 Attempt ID | 复用 Attempt 或普通重试换 Key | DOCUMENTED_ONLY |
| HIR-16 | Storage commit 前后崩溃均可协调且不重复副作用 | 恢复丢失已提交结果或重复 mutation | EVIDENCE_REQUIRED |
| HIR-17 | H Attempt 映射到不同 C/G DeliveryAttempt；G Applied 需自身完整证据 | H ACK/receipt 升级 Applied 或覆盖证据 | EVIDENCE_REQUIRED |
| HIR-18 | 重放披露独立复核 I 授权与 D Fence，并 fail-closed | 历史 receipt/signature 绕过当前 I/D | EVIDENCE_REQUIRED |

## 12. 当前处置

**仅为已文档化候选。** 本提案分离 H 幂等、C outcome、G Applied、D Fence、I 授权和 Storage 原子性边界；不证明跨 Owner 接受、不证明 AID-2026-098 已可用/pin，也不证明实现符合。所有 EVIDENCE_REQUIRED 检查点保持 OPEN。本文件不修改 runtime、validator、schema、workflow、部署或 Issue 状态。
