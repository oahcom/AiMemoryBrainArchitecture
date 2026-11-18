# AID-2026-001 — Joined Forget / Memory Lifecycle Contract Proposal v2
# AID-2026-001 — Forget / Memory 生命周期联合契约提案 v2

**Status: PROPOSED — NOT NORMATIVE UNTIL OWNER D / OWNER I APPROVE THE SAME EXACT CONTENT SHA.**
**状态：PROPOSED — 在 Owner D / Owner I 批准同一精确内容 SHA 前，不具备规范效力。**

- Work Item: AID-2026-001; Task: U-022; coordinating identifier: U-023
- Classification: ARCH / SEC / R3
- Supersedes as current candidate only: v1; v1 remains immutable and traceable.
- Base branch: remediation/aid-2026-001-forget-contract-closure-2026-11-18
- Base commit supplied and independently read before write: 0fd19d60b3698adf2b6de343e99df39d5031aac5
- Inputs: D U-010 (Blob e12bc3beaf7327f7646fa090cb1fe2cda023cacf); I U-011 EN (Blob c9daf61a538a175718e1bb492797cb2b5a51547a); I U-011 ZH (Blob d03d26bbdc96ee9df7f532144d331a3a06be3866); D/I authority matrix (Blob 6c6b3715f95f0aa9c29ad2fd42d15d8b2bae77b2); Owner D/I v2 prompts (Blobs 7005788694b4f89513c62a5d58adcfa74b6c14ec / abf8551e37580f1e18a8f956ba453d88918a87b2).
- Approval: D approval NOT CLAIMED; I approval NOT CLAIMED; same-SHA bilateral approval NOT GRANTED; Storage approval NOT CLAIMED.
- Tests: specifications only; NOT RUN by this document.

本文件是 v2 候选版本；v1 历史 Blob 保留不变。本文不代表 Owner D、Owner I、Storage 或验收权限方已批准。本文不宣告实现、运行时、持久化原子性或 R3 测试通过。

## 1. Purpose, authority and invariants / 目的、权责与不变量

**D owns canonical domain truth. I owns security and governance policy.** D alone defines Memory lifecycle, ForgetOperation domain phases, ForgetFence semantics, the `SuppressionCommitted` trigger and D-domain completion. I owns authenticated-principal trust, authorization/delegation/revocation, PermissionEpoch, privacy/retention/Legal Hold policy, required-target policy, governance evidence acceptance, governance assessment and exception authority. Executors own only their local action/capability and evidence. Storage alone approves and proves durable atomicity, serialization, crash recovery and visibility.

**D 负责规范领域事实；I 负责安全与治理策略。** D 单独定义 Memory 生命周期、ForgetOperation 领域阶段、ForgetFence 语义、`SuppressionCommitted` 触发点及 D 领域完成。I 负责认证主体信任、授权/委托/撤权、PermissionEpoch、隐私/保留/Legal Hold 策略、必需目标策略、治理证据接受、治理评估和例外授权。执行方仅负责本地动作/能力及证据。Storage 单独批准并证明持久化原子性、排序、崩溃恢复和可见性。

Non-negotiable rules:
1. A successful, durable `SuppressionCommitted` is the sole trigger that atomically changes the canonical Memory identity to `Forgotten`. I authorization is a mandatory pre-commit condition, not the trigger. I governance completion is not a precondition for Forgotten.
2. Once Forgotten, the same identity never resurrects. Later failure, revocation, policy change, unknown status or retry cannot lower/remove the fence or restore ordinary access.
3. `Forgotten`, ForgetOperation phase, `PerTargetResult`, D-domain completion, `ExceptionDecision`, `GovernanceAssessment` and physical-erasure evidence are separate typed facts.
4. No unknown, failed, unsupported, unregistered-but-required or unevidenced target is success. No ACK proves beyond its authenticated capability scope.
5. All evidence is append-only; corrections supersede by reference. No historical record is deleted or overwritten.
6. Neither Owner may unilaterally publish this joined contract as normative. Both must approve the same exact content SHA. Silence, implementation, review, or one-sided approval is insufficient.

不可妥协规则：
1. 成功且持久化的 `SuppressionCommitted` 是规范 Memory 身份原子转为 `Forgotten` 的唯一触发条件。I 授权是提交前置条件，不是触发点；I 治理完成不是 Forgotten 的前置条件。
2. Forgotten 后同一身份永不复活。后续失败、撤权、策略变化、未知状态或重试均不得降低/移除 Fence 或恢复普通访问。
3. `Forgotten`、ForgetOperation 阶段、`PerTargetResult`、D 领域完成、`ExceptionDecision`、`GovernanceAssessment` 和物理擦除证据是相互独立的类型化事实。
4. 未知、失败、不支持、未登记但必需或缺少证据的目标均不算成功。ACK 证明范围不得超过其认证能力范围。
5. 所有证据只追加；更正通过引用 supersede。不得删除或覆盖历史记录。
6. 任何一方均不得单方面将联合契约发布为规范。双方必须批准同一精确内容 SHA。沉默、实现、审查或单方批准均不充分。

## 2. D canonical state machine / D 规范状态机

### 2.1 Complete phase set / 完整阶段集合

The canonical D-owned `ForgetOperationPhase` set is exactly:
`Requested`, `AuthorizationPending`, `Authorized`, `SuppressionCommitted`, `InventorySealed`, `CleanupInProgress`, `DomainCompletionEvaluated`, `Completed`, `Blocked`, `Failed`, `Cancelled`.

规范 D 所有的 `ForgetOperationPhase` 阶段集合为：
`Requested`、`AuthorizationPending`、`Authorized`、`SuppressionCommitted`、`InventorySealed`、`CleanupInProgress`、`DomainCompletionEvaluated`、`Completed`、`Blocked`、`Failed`、`Cancelled`。

The canonical evaluation identifier is **`DomainCompletionEvaluated`** in both language versions. `CompletionEvaluated` is a deprecated alias and MUST NOT be emitted as a persisted state, event name, API enum or test oracle. Chinese display label: “领域完成已评估”; do not translate it into a different identifier.

规范评估标识在中英文版本中统一为 **`DomainCompletionEvaluated`**。`CompletionEvaluated` 是废弃别名，不得作为持久化状态、事件名、API 枚举或测试判据输出。中文显示名称为“领域完成已评估”；标识符本身不翻译、不改名。

### 2.2 Transition table / 转换对照表

| Current | Legal next state(s) | Guard / meaning |
|---|---|---|
| Requested | AuthorizationPending, Cancelled, Blocked, Failed | Persist request identity first; cancellation only before suppression. |
| AuthorizationPending | Authorized, Blocked, Failed, Cancelled | Await I decision; deny/defer is not authorization. |
| Authorized | SuppressionCommitted, AuthorizationPending, Blocked, Failed, Cancelled | Revalidate I receipt at commit serialization point; authorization alone does not suppress. |
| SuppressionCommitted | InventorySealed, CleanupInProgress, Blocked, Failed | Durable atomic commit; Memory becomes Forgotten here and never reverses. |
| InventorySealed | CleanupInProgress, Blocked, Failed | Inventory revision fixed for this assessment; new targets require new revision. |
| CleanupInProgress | CleanupInProgress, DomainCompletionEvaluated, Blocked, Failed | Target actions/reconciliation; idempotent checkpoints. |
| DomainCompletionEvaluated | Completed, CleanupInProgress, Blocked, Failed | D evaluates only its own completion predicate; invalidated evaluation returns to cleanup/reconciliation. |
| Blocked | AuthorizationPending, CleanupInProgress, DomainCompletionEvaluated, Failed, Cancelled* | Resume only after blocker condition resolved and required rechecks; Cancelled only pre-commit. |
| Failed | CleanupInProgress, AuthorizationPending, DomainCompletionEvaluated, Blocked | Failed is terminal for the failed attempt, not necessarily for the stable operation; explicit recovery/retry event required. |
| Completed | none | Terminal D-domain result; corrections require a new auditable operation/revision, not mutation. |
| Cancelled | none | Terminal only if cancellation occurred before SuppressionCommitted. |
 
`*` Any transition to Cancelled is forbidden once SuppressionCommitted has succeeded. After commit, stopping a worker/attempt is not operation cancellation.

| 当前状态 | 合法下一状态 | 守卫条件 / 含义 |
|---|---|---|
| Requested | AuthorizationPending、Cancelled、Blocked、Failed | 先持久化请求身份；仅抑制提交前可取消。 |
| AuthorizationPending | Authorized、Blocked、Failed、Cancelled | 等待 I 决策；拒绝/延期不等于授权。 |
| Authorized | SuppressionCommitted、AuthorizationPending、Blocked、Failed、Cancelled | 在提交排序点重新验证 I 回执；授权本身不产生抑制。 |
| SuppressionCommitted | InventorySealed、CleanupInProgress、Blocked、Failed | 持久化原子提交；Memory 在此转为 Forgotten，之后不可逆。 |
| InventorySealed | CleanupInProgress、Blocked、Failed | 本次评估的清单版本固定；新目标要求新版本。 |
| CleanupInProgress | CleanupInProgress、DomainCompletionEvaluated、Blocked、Failed | 执行目标动作/对账；检查点必须幂等。 |
| DomainCompletionEvaluated | Completed、CleanupInProgress、Blocked、Failed | D 只评估自己的完成判定；评估失效时返回清理/对账。 |
| Blocked | AuthorizationPending、CleanupInProgress、DomainCompletionEvaluated、Failed、Cancelled* | 仅在阻塞条件解除且必要复查后恢复；Cancelled 仅限提交前。 |
| Failed | CleanupInProgress、AuthorizationPending、DomainCompletionEvaluated、Blocked | Failed 对失败的 attempt 是终止态，但稳定 Operation 不一定终止；恢复/重试必须有明确事件。 |
| Completed | 无 | D 领域结果终态；更正必须建立可审计的新 Operation/Revision，不得原位改写。 |
| Cancelled | 无 | 仅在 SuppressionCommitted 前取消时为终态。 |

`*` 一旦 SuppressionCommitted 成功，禁止任何转入 Cancelled 的转换。提交后停止 Worker/Attempt 不等于取消 Operation。

### 2.3 Failure, recovery and event history / 失败、恢复与事件历史

Every transition appends an immutable event with: operation_id, event_id, from_phase, to_phase, actor/service identity, authenticated principal where applicable, reason_code, correlation/causation IDs, attempt_id, inventory_revision, policy/authorization references, observed_at from trusted time, event sequence/version and integrity provenance. A retry never rewrites a prior Failed event and never changes operation_id. It creates a new attempt_id and references the prior failed event/checkpoint. `Failed → CleanupInProgress` is legal only through an explicit recovery event after reconciliation and current authorization/policy checks for the next protected action. `Failed → AuthorizationPending` is required when authorization must be reacquired. Ambiguous post-commit outcomes must be reconciled against durable commit evidence before any retry. No failure path after commit removes Forgotten or the fence.

每次转换均追加不可变事件，至少包含：operation_id、event_id、from_phase、to_phase、操作主体/服务身份、适用时的认证 Principal、reason_code、correlation/causation ID、attempt_id、inventory_revision、策略/授权引用、可信时间 observed_at、事件序列/版本及完整性来源。重试不得改写历史 Failed 事件，也不得更换 operation_id；必须创建新的 attempt_id 并引用先前失败事件/检查点。只有在对账完成、下一受保护动作的当前授权/策略复查通过后，才可通过明确恢复事件执行合法的 `Failed → CleanupInProgress`。需要重新授权时必须经过 `Failed → AuthorizationPending`。提交后结果不明，任何重试前必须先对账持久化提交证据。提交后的任何失败路径都不得移除 Forgotten 或 Fence。

## 3. I authorization envelope, receipt and PermissionEpoch / I 授权信封、回执与 PermissionEpoch

### 3.1 Decision envelope / 决策信封

The immutable signed I decision envelope MUST include: decision_id; trusted issuer_id and key/version; subject_principal_id; effective actor_principal_id; ordered delegation_chain with constraints (empty only for direct authority); action; exact resource_scope/target IDs; purpose; policy_id, policy_version and evaluation context/revision; PermissionEpoch; ALLOW or DENY; issued_at, not_before and expires_at; canonical request_hash (actor/delegation, action, scope, purpose and preconditions); audience (specific service/operation/commit boundary); nonce; provenance and cryptographic integrity/signature material. A boolean, unsigned payload, log line, UI state, ACK or decision ID alone is not a receipt.

不可变且带签名的 I 决策信封 MUST 包含：decision_id；可信 issuer_id 及密钥/版本；subject_principal_id；有效 actor_principal_id；带约束的有序 delegation_chain（仅直接授权时可为空）；action；精确 resource_scope/target IDs；purpose；policy_id、policy_version 及评估上下文/修订；PermissionEpoch；ALLOW 或 DENY；issued_at、not_before、expires_at；规范 request_hash（actor/delegation、action、scope、purpose 和前置条件）；audience（特定服务/Operation/提交边界）；nonce；provenance 及密码学完整性/签名材料。布尔值、未签名载荷、日志行、UI 状态、ACK 或单独 decision ID 均不是授权回执。

Verification MUST validate trusted issuer and key status, signature/integrity, audience, request hash, exact scope and purpose, actor and delegation chain, policy version, validity window, nonce uniqueness/replay status and authoritative epoch vector. Verification failure is deny/unknown, never implicit allow.

验证 MUST 校验可信签发者及密钥状态、签名/完整性、audience、request hash、精确 scope 与 purpose、actor 和委托链、策略版本、有效时间窗、nonce 唯一性/重放状态及权威 epoch vector。验证失败只能拒绝/判为未知，绝不隐式允许。

### 3.2 Commit-bound receipt / 绑定提交的回执

The receipt MUST bind the full envelope reference and immutable digest; verification result; verifier principal/service and verifier version; exact operation_id, request_hash, actor, action, target scope and purpose; complete applicable PermissionEpoch vector and policy revision; commit-attempt ID and transaction/serialization identifier; commit-time check result; trusted decision/verification timestamps; unique receipt ID; provenance and integrity protection. It is single-operation, single-audience, exact-scope and validity-window bound; any material request change requires a new decision and receipt.

回执 MUST 绑定完整信封引用及不可变摘要、验证结果、验证者 Principal/服务及验证者版本、精确 operation_id/request_hash/actor/action/target scope/purpose、完整适用 PermissionEpoch vector 和策略修订、提交 attempt ID 与事务/序列化标识、提交时检查结果、可信决策/验证时间戳、唯一 receipt ID、provenance 和完整性保护。回执仅适用于单一 Operation、指定 audience、精确 scope 和有效时间窗；请求发生实质变化必须重新决策并签发回执。

### 3.3 Epoch and revocation race / Epoch 与撤权竞态

I maintains a monotonically increasing, never-reused PermissionEpoch for each authorization subject/policy domain. Every authorization-affecting change (revocation, delegation withdrawal/narrowing, privilege reduction, principal disablement or invalidating policy change) atomically advances the relevant epoch. The authoritative current epoch must be read at the commit serialization point. Multi-principal/delegation/policy operations bind the complete epoch vector. Cache freshness or preflight is not authoritative.

I 对每个授权主体/策略域维护单调递增且永不复用的 PermissionEpoch。任何影响授权的变化（撤权、撤销/收窄委托、权限降低、主体禁用或使授权失效的策略变化）均须原子推进相关 epoch。必须在提交序列化点读取权威当前 epoch。涉及多个主体/委托/策略的操作必须绑定完整 epoch vector。缓存新鲜度或预检不具权威性。

- **COMMIT_WON**: authenticated receipt and full current epoch vector validate, and the suppression commit serializes before revocation takes effect. Storage must prove the ordering and durable atomicity. D's Forgotten transition remains terminal; later revocation cannot undo it.
- **REVOCATION_WON**: revocation/epoch advance serializes first; commit-time comparison detects mismatch and rejects commit. No SuppressionCommitted success and no Forgotten transition. A new decision is required if retry remains policy-permitted.
- **UNKNOWN**: ordering/current epoch/durable transaction result cannot be proven. Before confirmed commit, fail closed and do not claim success; reconcile before retry. If later evidence proves durable SuppressionCommitted succeeded, Forgotten remains terminal and MUST NOT be reversed.

- **COMMIT_WON**：授权回执及完整当前 epoch vector 验证通过，且 Suppression 提交先于撤权生效完成序列化。Storage 必须证明排序和持久化原子性。D 的 Forgotten 终态保持不变；后续撤权不能撤销它。
- **REVOCATION_WON**：撤权/epoch 推进先完成序列化；提交时比较发现不匹配并拒绝提交。不得报告 SuppressionCommitted 成功，也不得发生 Forgotten 转换。若策略仍允许重试，必须重新取得决策。
- **UNKNOWN**：无法证明排序/当前 epoch/持久化事务结果。确认提交前必须 fail closed，不得声称成功；重试前先对账。若后续证据证明 SuppressionCommitted 已持久化成功，Forgotten 仍保持终态且 MUST NOT 逆转。

The check MUST be inside or atomically coupled to the suppression transaction; a TOCTOU gap is prohibited. If authoritative epoch cannot be read, no commit. Storage chooses and proves the implementation mechanism; I defines the security property.

该检查 MUST 位于抑制事务内部或与其原子耦合；禁止 TOCTOU 间隙。无法读取权威 epoch 时不得提交。Storage 选择并证明实现机制；I 定义安全属性。

### 3.4 Nine commit-time checks / 九项提交前检查

At the serialization point verify all nine: (1) trusted issuer and valid signature; (2) authenticated subject, effective actor and valid delegation; (3) exact action/operation/target scope/purpose/request hash; (4) ALLOW, valid time window and correct audience; (5) every epoch equals authoritative current vector and no earlier revocation; (6) current applicable policy revision permits operation; (7) no applicable Legal Hold/mandatory retention prohibits suppression; (8) nonce is replay-safe and receipt not consumed incompatibly; (9) verifier emits integrity-protected evidence bound to transaction and serialization order. These checks authorize the commit only; they do not require downstream cleanup or governance completion.

在序列化点验证九项：(1) 签发者可信且签名有效；(2) subject、有效 actor 和委托链已认证且有效；(3) action/operation/target scope/purpose/request hash 精确匹配；(4) ALLOW、时间窗有效且 audience 正确；(5) 每个 epoch 均等于权威当前 vector 且不存在先序列化撤权；(6) 当前适用策略修订允许该操作；(7) 不存在禁止抑制的适用 Legal Hold/强制保留；(8) nonce 可防重放且回执未被不兼容地消费；(9) 验证者输出绑定事务和序列化顺序的完整性保护证据。上述检查仅授权提交，不要求下游清理或治理完成。

## 4. Governance exceptions and per-target evidence / 治理例外与逐目标证据

### 4.1 Legal Hold / retention decision / Legal Hold / 保留决策

Deny/defer by default where applicable law, binding retention or a valid hold prohibits the requested suppression/deletion. Only a specifically designated I policy authority may approve a legally/policy-permitted narrow exception; no requester, D, executor, Storage or automation may self-approve. If law prohibits an exception, I cannot create one.

适用法律、强制保留或有效 Hold 禁止所请求的抑制/删除时，默认拒绝/延期。只有明确指定的 I 策略授权主体可以批准法律/策略允许的狭窄例外；请求方、D、执行方、Storage 或自动化流程均不得自批。法律禁止例外时，I 无权创设例外。

### 4.2 Exception record / 例外记录

Each immutable exception record MUST include: exception_id; decision_id; status (PENDING/APPROVED/DENIED/EXPIRED/REVOKED/SUPERSEDED); named approving I authority, authenticated principal, role/authority basis and delegation evidence; operation_id; exact target IDs, data classes, systems/regions and scope; legal-hold or retention policy ID/version; jurisdiction and cited basis; reason, necessity/proportionality and alternatives; permitted and prohibited actions; residual data/exposure; access restrictions and compensating controls; evidence references and integrity/provenance; decision/effective/expiry times; next review; accountable policy owner; reevaluation triggers; expiry/revocation disposition and required follow-up. Exception is least-privilege, target-specific, purpose-bound and time-bounded; no blanket, indefinite, implicit or retroactive exception.

每条不可变例外记录 MUST 包含：exception_id、decision_id、状态（PENDING/APPROVED/DENIED/EXPIRED/REVOKED/SUPERSEDED）、批准 I 权限主体姓名/身份、认证 Principal、角色/授权依据及委托证据、operation_id、精确 target IDs/数据类别/系统区域/scope、Legal Hold 或 Retention 策略 ID/版本、司法辖区及引用依据、理由/必要性比例性/替代方案、允许和禁止的动作、残余数据/暴露、访问限制及补偿控制、证据引用和完整性/provenance、决策/生效/到期时间、下次复核、负责策略 Owner、重新评估触发条件、到期/撤销处置及后续动作。例外必须最小权限、逐目标、绑定目的且有时限；禁止一揽子、无限期、隐式或追溯性例外。

An approved exception does NOT change Forgotten, authorize access/retrieval/derivation/delivery/restore, prove target success or physical erasure, set PerTargetResult to Succeeded, or itself establish governance compliance. If legal/policy rules require defer rather than exception, record Deferred/NonCompliant. A preserved legal record must be isolated, access-controlled, purpose-limited, integrity-protected and time-bounded.

例外获批不会改变 Forgotten，不授权访问/检索/派生/交付/恢复，不证明目标成功或物理擦除，不得将 PerTargetResult 设为 Succeeded，也不自动建立治理合规。法律/策略要求延期而非例外时，应记录 Deferred/NonCompliant。依法保留的记录必须隔离、访问受控、目的受限、完整性受保护且有期限。

### 4.3 Inventory policy and seal / 清单策略与封存

I policy declares policy_id/version/revision, effective interval, applicable data classes/jurisdictions/operation/purpose, mandatory target classes/actions, conditional applicability and reasoned exclusions, accepted evidence kinds/freshness/provenance/terminal result, unsupported-capability handling/escalation, inventory revision/seal requirements, invalidation triggers and exception eligibility. D owns domain dependency inventory semantics; each executor owns local discovery/capability facts; I owns global policy and evaluates coverage, but MUST NOT invent discovery facts.

I 策略声明 policy_id/version/revision、生效区间、适用数据类别/司法辖区/操作/目的、必需目标类别/动作、有理由的条件适用与排除、接受的证据类型/新鲜度/provenance/终态结果、不支持能力的处理/升级、清单版本/封存要求、失效触发条件及例外资格。D 负责领域依赖清单语义；各执行方负责本地发现/能力事实；I 负责全局策略并评估覆盖，但 MUST NOT 编造发现事实。

A seal binds inventory_id, monotonic revision, discovery source/owner, discovered_at, scope, policy revision, target IDs/classes, capability states, exclusions and integrity digest. Seal is valid only when discovery owners attest the declared discovery process completed, all known sources were queried, unresolved discovery errors are represented and exclusions explicit. Seal fixes assessment input; it does not prove no undiscovered target exists. New target/revision, policy change, new jurisdiction/data-class facts, restore, evidence expiry, hold/permission change invalidate prior assessment and require reassessment. Unknown/unregistered/unsupported mandatory targets block Compliant.

封存绑定 inventory_id、单调 revision、发现来源/Owner、discovered_at、scope、策略修订、target IDs/classes、能力状态、排除项和完整性摘要。只有发现 Owner 证明声明的发现流程完成、已查询所有已知来源、未解决发现错误已记录且排除项明确时才可封存。封存固定评估输入，不证明不存在未发现目标。新目标/版本、策略变化、新司法辖区/数据类别事实、恢复、证据过期、Hold/权限变化均使旧评估失效并要求重新评估。未知/未登记/不支持的必需目标阻止 Compliant。

### 4.4 Per-target evidence / 逐目标证据

Each target/action record is append-only and includes: operation_id, inventory_revision, target_id, target_class, owner_domain, required_action, capability and capability_profile_version, target_state, D fence_generation, authorization_decision_ref, policy_version_refs, immutable evidence_ref and evidence_kind, trusted observed_at, authenticated verifier and method/version, attempt_id, lease_fence, stable result_code, exception_ref/expiry where applicable, source system/producer identity and signature/checksum or equivalent provenance. Do not omit unsupported/offline/inaccessible targets. Evidence must not reproduce Forgotten content. ACK proves only its stated capability and region; queue ACK is not downstream deletion; cache receipt is namespace/generation-specific; backup expiry is backup-set-specific; external ACK is not physical-erasure proof without independent coverage.

每条目标/动作记录只追加，包含：operation_id、inventory_revision、target_id、target_class、owner_domain、required_action、capability 和 capability_profile_version、target_state、D fence_generation、authorization_decision_ref、policy_version_refs、不可变 evidence_ref/evidence_kind、可信 observed_at、认证 verifier 及方法/版本、attempt_id、lease_fence、稳定 result_code、适用时 exception_ref/expiry、来源系统/Producer 身份及签名/校验和或等效 provenance。不得省略不支持/离线/不可访问目标。证据不得复现 Forgotten 内容。ACK 仅证明其声明的能力和区域；Queue ACK 不等于下游删除；Cache 回执限定 Namespace/Generation；Backup 到期限定 Backup Set；外部 ACK 若无独立覆盖保证，不是物理擦除证明。

## 5. Typed results and completion / 类型化结果与完成

The types are independent:
- `PerTargetResult` (executor): NotStarted, InProgress, Succeeded, Failed, Unknown, Unsupported, NotEvidenced.
- `ExceptionDecision` (I): Pending, Approved, Denied, Expired, Revoked, Superseded.
- `GovernanceAssessment` (I): Pending, Compliant, NonCompliant, Deferred, CompliantWithException.
- `DDomainCompletion` (D): NotEvaluated, Incomplete, Blocked, Completed.
- `MemoryLifecycle` (D): Candidate, Consolidated, Active, Superseded, Archived, Forgotten.
- PhysicalErasureEvidence is target/storage-owner evidence and is not inferred from the above.

类型相互独立：
- `PerTargetResult`（执行方）：NotStarted、InProgress、Succeeded、Failed、Unknown、Unsupported、NotEvidenced。
- `ExceptionDecision`（I）：Pending、Approved、Denied、Expired、Revoked、Superseded。
- `GovernanceAssessment`（I）：Pending、Compliant、NonCompliant、Deferred、CompliantWithException。
- `DDomainCompletion`（D）：NotEvaluated、Incomplete、Blocked、Completed。
- `MemoryLifecycle`（D）：Candidate、Consolidated、Active、Superseded、Archived、Forgotten。
- PhysicalErasureEvidence 是目标/Storage Owner 的证据，不得从以上状态推断。

**ExceptionApproved ≠ Succeeded.** An exception is a policy disposition for residual obligation, never an executor action result. CompliantWithException requires every exception valid, in scope, unexpired, independently approved, supported by compensating controls, and all other mandatory targets compliant. Any pending/failed/unknown/unsupported/not-evidenced mandatory target blocks Compliant. Every assessment binds exact inventory revision, policy revision, authorization receipt, target evidence set and exception decisions. No I assessment may rewrite D Forgotten or D completion.

**ExceptionApproved ≠ Succeeded。** 例外是残余义务的策略处置，不是执行方动作结果。CompliantWithException 要求每个例外均有效、在范围内、未过期、独立批准并有补偿控制，且其他必需目标均合规。任何待处理/失败/未知/不支持/缺证据的必需目标均阻止 Compliant。每项评估绑定精确清单版本、策略版本、授权回执、目标证据集和例外决策。I 评估不得改写 D 的 Forgotten 或 D 完成状态。

## 6. Test specification mapping / 测试规格映射

All cases below are specifications, NOT execution evidence. Execution requires reproducible harness, fixtures, command, environment, expected/actual output and exact tested commit SHA.

以下均为测试规格，不是执行证据。执行必须提供可复现 Harness、Fixture、命令、环境、预期/实际输出及准确测试 Commit SHA。

### 6.1 DFI mapping / DFI 映射

| DFI | Contract clause | Scenario and assertion |
|---|---|---|
| DFI-001 | §§1–2 | Concurrent read/derive vs suppression: after commit no content is returned. |
| DFI-002 | §§1–2,5 | Forgotten while cleanup pending: Memory stays terminal; D completion is not Completed. |
| DFI-003 | §2 | Cancel after SuppressionCommitted is rejected; fence persists. |
| DFI-004 | §§4–5 | Missing/unknown/unsupported mandatory target blocks completion/compliance. |
| DFI-005 | §4.4 | Limited adapter ACK cannot prove hidden provider copy erased. |
| DFI-006 | §§4.2,5 | CompletedWithPolicyException requires bounded I approval, residual controls, review/expiry and effective fence. |
| DFI-007 | §2.3 | Same idempotency key/hash returns same operation; changed hash rejected. |
| DFI-008 | §2.3,4.4 | Stale lease worker cannot commit checkpoint/evidence. |
| DFI-009 | §§2.3,3.2 | Crash after side effect before receipt: reconcile before retry; no duplicate destructive action. |
| DFI-010 | §§3–4 | Mid-operation revocation/Legal Hold change blocks next protected action pending reauthorization. |
| DFI-011 | §4.3 | Late dependency creates new inventory revision and invalidates prior evaluation. |
| DFI-012 | §§1–2,4.3 | Backup restore must apply latest fence before content becomes queryable. |
| DFI-013…022 | §4, owner execution contracts | E/F/G/H/C/Storage race, replay, stale cache, offline reconciliation, ACK capability and restore cases; exact per-owner scenarios remain tied to owner-approved execution-boundary contract. |

### 6.2 I-U011 mapping / I-U011 映射

| Test | Contract clause | Scenario and required assertion |
|---|---|---|
| I-U011-T01 | §3.1 | Forged/unknown issuer or invalid signature: reject, no commit. |
| I-U011-T02 | §3.1–3.2 | Wrong audience, operation, request hash, purpose or scope: reject, no commit. |
| I-U011-T03 | §3.1–3.2 | Expired/not-yet-valid receipt or nonce replay: fail closed, no commit. |
| I-U011-T04 | §3.3 | Receipt epoch differs from authoritative current epoch: reject stale receipt. |
| I-U011-T05 | §3.3 | Revocation serializes first: REVOCATION_WON, no commit. |
| I-U011-T06 | §3.3 | Commit serializes first: COMMIT_WON; Forgotten remains terminal after revocation. |
| I-U011-T07 | §3.3 | UNKNOWN ordering/current epoch: fail closed before confirmed commit; reconcile; proven commit remains Forgotten. |
| I-U011-T08 | §§3.1,3.3 | Delegation revoked or narrowed: epoch/currentness check rejects stale delegation. |
| I-U011-T09 | §4.1–4.2 | Legal Hold/mandatory retention prohibits action: deny/defer; no unauthorized exception. |
| I-U011-T10 | §4.2 | Missing approver, authority basis, scope, jurisdiction, expiry or controls: exception invalid. |
| I-U011-T11 | §5 | Exception approved but target action not done: PerTargetResult is not Succeeded. |
| I-U011-T12 | §4.3,5 | Inventory changes/new target: prior assessment invalidated; reassessment required. |
| I-U011-T13 | §§1–2,5 | D is Forgotten while downstream cleanup incomplete: Forgotten stays terminal; governance remains pending/noncompliant. |
| I-U011-T14 | §3.2 | Receipt verifier, operation binding, transaction ID, epoch, trusted time or integrity provenance absent: reject receipt. |
| I-U011-T15 | §§3.1–3.3 | Request purpose/scope mismatch or nonce reuse across operation: reject. |
| I-U011-T16 | §§4.2–5 | Exception expiry/revocation or missing follow-up: assessment invalidated; no silent renewal. |

## 7. Bilingual semantic verification / 双语语义核验

The EN/ZH pair uses identical identifiers and equivalent MUST/MUST NOT force. Verified item-by-item in this candidate:
1. Authority split: D lifecycle/domain completion vs I security/governance.
2. Unique Forgotten trigger: durable successful SuppressionCommitted; I authorization is precondition only.
3. Canonical phase set and identifier DomainCompletionEvaluated.
4. Failed retry/recovery semantics, stable operation identity and append-only event history.
5. Envelope fields, trusted issuer/signature, delegation, audience, nonce and request hash.
6. Receipt verifier, operation binding, transaction/serialization identity, epoch vector, trusted time and integrity provenance.
7. Monotonic PermissionEpoch, authoritative current vector and COMMIT_WON/REVOCATION_WON/UNKNOWN.
8. Nine commit-time checks.
9. Legal Hold/retention default, exception authority, complete record and non-effects.
10. Inventory policy, discovery ownership, seal criteria and invalidation triggers.
11. Per-target evidence fields, provenance and ACK capability limits.
12. Independent result types and ExceptionApproved ≠ Succeeded.
13. DFI and I-U011 test IDs, scenarios and assertions.
14. Same-SHA bilateral approval and non-claims.

中英文逐项核验采用相同标识符和等效 MUST/MUST NOT 强度。本候选版本逐项核验：
1. 权责分离：D 生命周期/领域完成与 I 安全/治理。
2. Forgotten 唯一触发点：成功持久化 SuppressionCommitted；I 授权仅为前置条件。
3. 规范阶段集合及 DomainCompletionEvaluated 标识。
4. Failed 重试/恢复语义、稳定 Operation 身份及只追加事件历史。
5. 信封字段、可信签发者/签名、委托、audience、nonce 和 request hash。
6. 回执验证者、Operation 绑定、事务/序列化身份、epoch vector、可信时间和完整性来源。
7. 单调 PermissionEpoch、权威当前 vector 及 COMMIT_WON/REVOCATION_WON/UNKNOWN。
8. 九项提交时检查。
9. Legal Hold/Retention 默认规则、例外权限、完整记录和非效力。
10. 清单策略、发现权责、封存条件及失效触发。
11. 逐目标证据字段、provenance 和 ACK 能力边界。
12. 独立结果类型及 ExceptionApproved ≠ Succeeded。
13. DFI 与 I-U011 测试 ID、场景和断言。
14. 同 SHA 双边批准及明确不作出的声明。

## 8. G-04 sub-gap disposition / G-04 子缺口处置

| Gap | Closure evidence in this candidate | Remaining non-document gates |
|---|---|---|
| G04-A | §2.1–2.3: all 11 phases, including AuthorizationPending and Blocked, with transition table. | D approval; implementation/state-transition tests. |
| G04-B | §2.1: DomainCompletionEvaluated is the sole EN/ZH identifier; CompletionEvaluated deprecated. | API/schema and test-oracle consistency check. |
| G04-C | §2.3: Failed attempt terminality, legal recovery transitions including Failed→CleanupInProgress, attempt/operation identity and append-only event history. | Fault-injection/recovery tests. |
| G04-D | §3.1–3.2: complete signed envelope and commit-bound receipt fields. | I approval; crypto/verifier implementation tests. |
| G04-E | §3.3: monotonic epoch, authoritative vector and three race outcomes. | Storage serialization proof and race tests. |
| G04-F | §3.4: all nine commit-time checks; authorization is precondition, not trigger. | Commit-bound implementation and negative tests. |
| G04-G | §4.1–4.2: Legal Hold default, authority, jurisdiction, target scope, status, controls, review/expiry/follow-up. | Case-specific I decision; exception tests. |
| G04-H | §4.3: policy version, discovery ownership, seal conditions and invalidation. | Discovery-owner attestations and inventory tests. |
| G04-I | §5: independent PerTargetResult, ExceptionDecision, GovernanceAssessment; exception never equals success. | Schema/API conformance and typed-result tests. |
| G04-J | §6.2 maps I-U011-T01…T16; §6.1 maps DFI-001…022. | All tests remain NOT RUN until reproducible evidence is attached. |

| 缺口 | 本候选版本中的关闭证据 | 仍未完成的非文档门禁 |
|---|---|---|
| G04-A | §2.1–2.3：完整 11 阶段，含 AuthorizationPending、Blocked 及转换表。 | D 批准；实现/状态转换测试。 |
| G04-B | §2.1：DomainCompletionEvaluated 为中英文唯一标识；CompletionEvaluated 已废弃。 | API/Schema 与测试判据一致性检查。 |
| G04-C | §2.3：Failed attempt 终止性、含 Failed→CleanupInProgress 的合法恢复、attempt/operation 身份及只追加事件历史。 | 故障注入/恢复测试。 |
| G04-D | §3.1–3.2：完整签名信封和绑定提交的回执字段。 | I 批准；密码学/验证器实现测试。 |
| G04-E | §3.3：单调 epoch、权威 vector 和三种竞态结果。 | Storage 排序证明及竞态测试。 |
| G04-F | §3.4：九项提交时检查；授权是前置条件而非触发点。 | 提交绑定实现及负向测试。 |
| G04-G | §4.1–4.2：Legal Hold 默认规则、权限、司法辖区、目标范围、状态、控制、复核/到期/后续处置。 | 个案 I 决策；例外测试。 |
| G04-H | §4.3：策略版本、发现权责、封存条件和失效规则。 | 发现 Owner 证明及清单测试。 |
| G04-I | §5：PerTargetResult、ExceptionDecision、GovernanceAssessment 独立；例外不等于成功。 | Schema/API 一致性及类型化结果测试。 |
| G04-J | §6.2 映射 I-U011-T01…T16；§6.1 映射 DFI-001…022。 | 所有测试在附上可复现证据前均为 NOT RUN。 |

## 9. Finding registration / Finding 登记

The following coordinator-proposed findings are P1 and are routed to existing Issue #41 only:
- U021-G04-001 — P1 — Issue #41 — disposition: document gap addressed in this candidate; keep OPEN pending independent review and D/I same-SHA approval.
- U021-G04-002 — P1 — Issue #41 — disposition: document gap addressed in this candidate; keep OPEN pending independent bilingual identifier/schema review.
- U021-G04-003 — P1 — Issue #41 — disposition: document gap addressed in this candidate; keep OPEN pending Storage ordering proof and reproducible race/recovery tests.
- U021-G04-004 — P1 — Issue #41 — disposition: document gap addressed in this candidate; keep OPEN pending independent test-spec review and execution evidence.

以下协调方候选 Finding 均为 P1，仅回流既有 Issue #41：
- U021-G04-001 — P1 — Issue #41 — 处置：本候选版本已补齐文档缺口；保持 OPEN，待独立审查及 D/I 同 SHA 批准。
- U021-G04-002 — P1 — Issue #41 — 处置：本候选版本已补齐文档缺口；保持 OPEN，待独立双语标识/Schema 审查。
- U021-G04-003 — P1 — Issue #41 — 处置：本候选版本已补齐文档缺口；保持 OPEN，待 Storage 排序证明及可复现竞态/恢复测试。
- U021-G04-004 — P1 — Issue #41 — 处置：本候选版本已补齐文档缺口；保持 OPEN，待独立测试规格审查及执行证据。

## 10. Approval, status and non-claims / 批准、状态与明确不作出的声明

This is a candidate only. It is not NORMATIVE, ADOPTED, production activated, Storage-approved, independently reviewed, tested, accepted or merged. Owner D and Owner I must each post an attributable approval in Issue #41 referring to the same exact content SHA. No unilateral approval can close D-R3-D-003. D-R3-D-003 remains OPEN. AID-2026-001 remains BLOCKED_PENDING_R3_EVIDENCE until the later independent bilingual review, same-SHA bilateral approval, Storage persistence-boundary approval, independent integration review and reproducible R3 evidence are completed.

本文件仅为候选提案，不是 NORMATIVE、ADOPTED、生产激活、Storage 批准、独立审查、测试通过、验收或合并。Owner D 与 Owner I 必须分别在 Issue #41 发布可归属批准，并指向同一精确内容 SHA。任何单方批准均不能关闭 D-R3-D-003。D-R3-D-003 保持 OPEN。AID-2026-001 继续为 BLOCKED_PENDING_R3_EVIDENCE，直至后续独立双语审查、同 SHA 双边批准、Storage 持久化边界批准、独立集成审查及可复现 R3 证据全部完成。

No production implementation, physical erasure, target completion, policy exception approval, Storage atomicity, test execution, Owner D approval or Owner I approval is claimed. No historical record is deleted or overwritten.
不声称生产实现、物理擦除、目标完成、策略例外批准、Storage 原子性、测试执行、Owner D 批准或 Owner I 批准。未删除或覆盖任何历史记录。
