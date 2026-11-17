# AID-2026-001 — R3 Contract Test Matrix
# AID-2026-001 — R3 契约测试矩阵

**Work Item:** AID-2026-001
**Classification:** ARCH / R3
**Status:** TEST SPECIFICATION ONLY — NOT EXECUTED
**Applies to:** security identity, authorization, privacy/retention/audit and Forget/deletion normative boundaries.

This matrix defines minimum reproducible contract tests. It is not evidence that tests have run. Each execution must record the exact test harness/version, fixtures, command, output, result, commit SHA and reviewer.

本矩阵定义最低可复现契约测试，不代表测试已经执行。每次执行必须记录准确测试工具及版本、Fixture、命令、输出、结果、Commit SHA 和 Reviewer。

| ID | Contract invariant | Positive case | Negative / failure case | Required observable evidence |
|---|---|---|---|---|
| R3-001 | Domain identity is not a security principal | A domain entity identifier resolves only within its declared domain semantics | Domain identity alone is presented as proof of authentication or authorization | Fixture and assertion showing domain identity cannot grant access |
| R3-002 | Authorization precedes Forget execution | Authorized principal requests Forget within permitted scope | Unauthenticated/unauthorized principal attempts the same operation | Decision trace proving deny occurs before mutation |
| R3-003 | Forget scope is bounded | Authorized request affects exactly the approved subject/scope | Cross-tenant, cross-user or out-of-scope identifier is supplied | Before/after state proving no out-of-scope data changed |
| R3-004 | D/I bilateral contract boundary is respected | D defines canonical lifecycle/deletion semantics and I defines authorization/privacy/retention controls; both agree on joined contract | Either side unilaterally changes the other's authority | Contract fixture and explicit bilateral approval record |
| R3-005 | Retention/legal hold constraints are enforced | Applicable retention/legal hold is evaluated and documented | Forget bypasses mandatory retention/legal hold or silently destroys required audit evidence | Deterministic policy fixture and expected allow/deny outcome |
| R3-006 | Deletion completion is truthful and evidence-backed | Completion is reported only after all required deletion stages reach defined terminal states | Partial failure is reported as complete | Stage-by-stage state and completion assertion |
| R3-007 | Audit evidence is bounded and non-authoritative over domain semantics | Audit records prove who/what/when/scope/result without redefining canonical memory semantics | Audit metadata is treated as authorization or domain truth without validation | Structured audit fixture and validation assertions |
| R3-008 | Retry/idempotency is safe | Repeating the same authorized Forget request does not produce inconsistent outcomes | Retry duplicates destructive side effects or loses completion evidence | Repeated execution trace and invariant checks |
| R3-009 | Partial failure and recovery fail closed | Interrupted deletion is represented as incomplete and safely resumable | System reports success or exposes stale data after incomplete deletion | Fault-injection trace, recovery result and final state assertions |

## Execution record template / 执行记录模板

For every test ID, record:
- Test ID and version:
- Exact source contract SHA(s):
- Test harness and version:
- Fixture/input:
- Exact command:
- Expected result:
- Actual result:
- Pass/fail:
- Logs/evidence reference:
- Executed at commit SHA:
- Executed by:
- Independently reviewed by:

每项测试均须记录：测试 ID/版本、源契约 SHA、测试工具及版本、Fixture/输入、准确命令、预期结果、实际结果、通过/失败、日志/证据引用、执行 Commit SHA、执行者及独立复核者。

**Current execution status:** NOT RUN / NOT EVIDENCED. No acceptance credit may be claimed from this specification alone.


## Forget linearization / evidence / recovery extension — DFI-001…DFI-012

These cases supplement R3-002…R3-009 and are required by the joined contract proposal. They are specifications only; no execution is implied.

| ID | Contract invariant | Positive case | Negative / failure case | Required observable evidence |
|---|---|---|---|---|
| DFI-001 | Suppression linearization fences concurrent reads and derivations | After the canonical fence/tombstone transaction commits, all later reads/derivations/deliveries reject the identity | A stale replica or in-flight reader returns content after the linearization point | Commit/WAL receipt, fence generation, race trace and query-denial assertions |
| DFI-002 | Memory state and Forget operation phase are distinct | Memory is Forgotten while operation remains CleanupInProgress | CleanupInProgress is reported as Completed or Forgotten is interpreted as physical erasure | Separate state-machine snapshots and truthful status assertion |
| DFI-003 | Post-linearization cancellation cannot remove suppression | Pre-suppression cancellation is allowed under policy | Cancel after SuppressionCommitted clears the fence or restores access | Rejected-cancel trace and unchanged fence high-water mark |
| DFI-004 | Required unknown/unsupported targets block Completed | All required targets have verified terminal evidence | A missing, unknown, offline or unsupported mandatory target is counted as success | Sealed inventory revision and aggregation trace |
| DFI-005 | ACK scope is capability-bounded | ACK proves only its declared managed region/action | External or Adapter ACK is treated as proof of hidden-copy physical erasure | Capability profile, authenticated ACK and verifier assertion |
| DFI-006 | Policy exception is explicit and bounded | I approves a residual target with legal basis, controls, owner and expiry/review | Unapproved, unbounded or expired exception is accepted | Approval reference, exception record, expiry and fence evidence |
| DFI-007 | Request idempotency binds canonical parameters | Same principal/scope/target/key and same request hash returns same operation | Same key with different target/purpose/action silently reuses or mutates operation | Canonical request hashes and operation identity trace |
| DFI-008 | Stage checkpoint is protected by lease fencing | Current lease_fence commits checkpoint and evidence | Stale worker commits after lease expiry or concurrent retry | Attempt IDs, lease tokens and CAS rejection trace |
| DFI-009 | Crash recovery reconciles uncertain side effects | Restart queries/reconciles external outcome before retry | Timeout is blindly retried and duplicates a destructive action | Fault-injection trace, provider state and deduplicated action proof |
| DFI-010 | Irreversible stages reauthorize against current policy | Current permission/policy allows stage immediately before execution | Permission revoked or legal hold added after queueing but before execution | PermissionEpoch/policy decision trace and fail-closed result |
| DFI-011 | Inventory expansion invalidates prior completion evaluation | Newly discovered dependency creates inventory revision N+1 and is processed | Old sealed revision remains accepted as complete after a new target appears | Revision history and invalidated evaluation reference |
| DFI-012 | Restore is fenced before data becomes queryable | Restore applies latest Forget generation/high-water mark before serving | Backup restore reintroduces a forgotten identity into reads or delivery | Restore trace, fence comparison and negative query test |

### 中文补充测试

| ID | 契约不变量 | 正向场景 | 负向/故障场景 | 必需可观察证据 |
|---|---|---|---|---|
| DFI-001 | 抑制线性化必须约束并发读取和派生 | 规范 Fence/Tombstone 事务提交后，所有后续读取/派生/交付均拒绝该身份 | 旧 Replica 或在途 Reader 在线性化点后返回内容 | Commit/WAL Receipt、Fence Generation、竞态 Trace 和 Query Denial 断言 |
| DFI-002 | Memory 状态与 Forget Operation 阶段相互独立 | Memory 已 Forgotten，但 Operation 仍为 CleanupInProgress | 将 CleanupInProgress 报告为 Completed，或把 Forgotten 解释为物理擦除 | 两套状态机快照及真实状态断言 |
| DFI-003 | 线性化后取消不得移除抑制 | 策略允许在线性化前取消 | SuppressionCommitted 后取消清除 Fence 或恢复访问 | Cancel 拒绝 Trace 和未变化的 Fence High-water Mark |
| DFI-004 | 必需的未知/不支持目标阻止 Completed | 所有必需目标均有已验证终态证据 | 缺失、未知、离线或不支持的必需目标被计为成功 | 封存清单 Revision 和聚合 Trace |
| DFI-005 | ACK 范围受能力约束 | ACK 仅证明其声明的 Managed Region/Action | 将 External/Adapter ACK 当作隐藏副本物理擦除证明 | Capability Profile、Authenticated ACK 和验证断言 |
| DFI-006 | 策略例外必须明确且有边界 | I 批准带法律依据、控制措施、责任人及到期/复核时间的残留目标 | 未批准、无边界或已过期的例外被接受 | Approval Reference、Exception Record、Expiry 和 Fence 证据 |
| DFI-007 | 请求幂等必须绑定规范参数 | 相同 Principal/Scope/Target/Key 和请求 Hash 返回同一 Operation | 相同 Key 配合不同 Target/Purpose/Action 被静默复用或修改 | 规范请求 Hash 和 Operation Identity Trace |
| DFI-008 | 阶段 Checkpoint 受 Lease Fencing 保护 | 当前 Lease_Fence 提交 Checkpoint 和证据 | Lease 过期或并发重试后，陈旧 Worker 仍提交 | Attempt ID、Lease Token 和 CAS 拒绝 Trace |
| DFI-009 | 崩溃恢复必须对账不确定副作用 | 重启后先查询/对账外部结果，再决定是否重试 | 超时后盲目重试，重复执行破坏性动作 | 故障注入 Trace、Provider 状态和动作去重证明 |
| DFI-010 | 不可逆阶段前必须按当前策略重新授权 | 执行前当前 Permission/Policy 允许该阶段 | 排队后、执行前 Permission 被撤销或新增 Legal Hold | PermissionEpoch/Policy Decision Trace 和 Fail-Closed 结果 |
| DFI-011 | 清单扩展使此前完成评估失效 | 新发现依赖产生 Inventory Revision N+1 并被处理 | 新目标出现后，旧封存 Revision 仍被接受为完成 | Revision 历史和已失效评估引用 |
| DFI-012 | Restore 前必须执行 Fence | Restore 在对外服务前应用最新 Forget Generation/High-water Mark | Backup Restore 使 Forgotten 身份重新进入读取或交付 | Restore Trace、Fence 比较和负向 Query Test |

**Execution status remains NOT RUN / NOT EVIDENCED.** The DFI cases are not test results and do not close any R3 gate.
