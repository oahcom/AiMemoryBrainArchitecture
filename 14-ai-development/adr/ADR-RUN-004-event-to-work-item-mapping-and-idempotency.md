# ADR-RUN-004 — Event-to-Work-Item Mapping and Semantic Idempotency
# ADR-RUN-004 — 事件到工作项映射与语义幂等

- Status / 状态: PROPOSED — decision pending / 提案中——待决议
- Owners / 责任: A (routing), relevant A–I Owner (domain semantics), I (security), Testing/Quality (conformance)
- Risk / 风险: R2 read-only; R3 repository writes or destructive work
- Related: Issue #30; ADR-RUN-001; ADR-RUN-002; ADR-RUN-003

## 1. Problem / 问题

GitHub webhooks are at-least-once, can be duplicated, delayed, reordered, and can describe intermediate state. Delivery identity is not work identity. A runtime must not start duplicate work because multiple event types describe the same current target, nor execute stale work after the target changes.

GitHub Webhook 至少一次投递，可能重复、延迟、乱序，并描述中间状态。Delivery 身份不等于 Work 身份。多个事件描述同一当前目标时不得重复启动任务；目标变化后不得执行过期工作。

## 2. Identity layers / 身份层次

1. **Delivery identity:** `(repository_id, delivery_id)`; unique inbox record, as defined by ADR-RUN-001.
2. **Observed event identity:** normalized event type/action + source object IDs + source revision/updated_at + payload digest. This is diagnostic and reconciliation metadata, not an authorization token.
3. **Work identity:** semantic target key generated only after fetching current GitHub state and evaluating policy.
4. **Run identity:** unique execution attempt; retries may create new run IDs while preserving the same work identity.
5. **Publication identity:** stable idempotency key per requested side effect, bound to work ID, expected base/head SHA and mutation kind.

1. **Delivery 身份：** `(repository_id, delivery_id)`，对应 ADR-RUN-001 的唯一 Inbox 记录。
2. **观察事件身份：** 规范化事件类型/action、源对象 ID、源修订/updated_at 和 Payload 摘要。用于诊断和对账，不是授权 Token。
3. **Work 身份：** 只有读取 GitHub 当前状态并完成策略判断后才能生成的语义目标键。
4. **Run 身份：** 每次执行尝试唯一；重试可生成新 Run ID，但保持相同 Work 身份。
5. **Publication 身份：** 每个副作用请求稳定的幂等键，绑定 Work ID、预期 Base/Head SHA 和变更类型。

## 3. Canonical work key / 规范 Work Key

Proposed canonical tuple:

`repository_id | work_subject_type | work_subject_id | target_revision | work_class | prompt_digest | policy_epoch`

Where:
- `target_revision` is the current immutable commit SHA for code/PR work; for issue-only work use a normalized issue state revision derived from the current API snapshot (not event timestamp alone).
- `work_class` is one of the governed classes (ARCH, IMPL, TEST, SEC, MIG, PERF, DOC, OPS).
- `prompt_digest` binds exact approved prompt bytes.
- `policy_epoch` changes when the applicable authorization/eligibility policy changes.

提议的规范元组如上。代码/PR 工作的 `target_revision` 使用当前不可变 Commit SHA；Issue-only 工作使用当前 API Snapshot 派生的规范状态修订，不能只用事件时间戳。Work Class 使用治理定义类别；Prompt Digest 绑定精确批准字节；Policy Epoch 在授权/资格策略变化时递增。

Hash the canonical serialization with a versioned encoding (e.g. canonical JSON with fixed field names/order or length-prefixed binary fields). Encoding version is part of the key. Do not concatenate ambiguous strings without length boundaries. Never include secrets or raw user content in the key.

使用带版本的规范序列化（例如固定字段名/顺序的 Canonical JSON，或长度前缀二进制字段）后再 Hash；编码版本属于 Key。不得无边界拼接字符串，不得包含秘密或原始用户内容。

## 4. Event mapping / 事件映射

| Event source / 事件源 | Re-fetch / 重新读取 | Possible action / 可能动作 |
|---|---|---|
| Issue opened/edited/labeled/assigned | Current issue, labels, assignees, linked PRs, project policy | Re-evaluate eligibility; create or supersede bounded work |
| Issue comment | Current issue + comment identity/body; treat body as untrusted | Wake approved workflow only; never interpret as privileged command |
| PR opened/synchronize/ready/closed | Current PR, head/base SHA, merge state, changed paths, checks | Create/rebase/supersede review or test work |
| PR review submitted | Current review state and latest PR head | Re-evaluate required changes/acceptance |
| Check run/suite completed | Current check suite and target SHA | Unlock dependent task only if required checks pass for exact SHA |
| Push | Current branch head and protected-branch policy | Reconcile only tracked branches; do not infer authorization from push |
| Workflow run completed | Current run conclusion and source SHA | Attach evidence; re-evaluate dependency gates |

Event is only a wake-up. The evaluator re-fetches state, validates repository allowlist, branch/PR state, required approvals, check conclusions, target SHA and current policy before creating work.

事件只是唤醒信号。Evaluator 必须重读状态，验证仓库白名单、Branch/PR 状态、必要批准、Check 结论、目标 SHA 和当前策略后才能创建 Work。

## 5. Coalescing and supersession / 合并与过期

- Multiple events for the same canonical work key coalesce into one eligible work item.
- A newer target revision supersedes queued work for an older revision.
- A leased/running older revision receives a cancellation request; the worker must stop at a safe checkpoint and cannot publish against the newer target.
- A completed work item is not rerun for the same key unless an explicit retry/reopen policy creates a new policy epoch or run request.
- Distinct work classes may coexist only where their declared dependency graph allows it.
- Out-of-order events never roll the work target backwards.

- 相同 Canonical Work Key 的多个事件合并为一个合格 Work Item。
- 新目标修订使旧修订的排队任务 superseded。
- 旧修订已租赁/运行时发出取消请求；Worker 在安全检查点停止，且不得针对新目标发布。
- 相同 Key 的已完成工作不重复运行，除非明确 Retry/Reopen 策略创建新 Policy Epoch 或 Run Request。
- 不同 Work Class 只有在依赖图允许时才可并存。
- 乱序事件永不使目标版本回退。

## 6. Dependency graph / 依赖图

A work item declares:
- required predecessor work IDs and minimum accepted states;
- required source branch/head SHA;
- required Owner approvals and security approvals;
- required CI/check names and exact target SHA;
- blocking findings and waiver authority (if any).

A dependency is satisfied only by durable GitHub evidence or an accepted run-ledger record bound to the exact expected revision. A comment saying “done” is not proof.

Work Item 声明前置 Work ID/最低状态、源 Branch/Head SHA、Owner/I 批准、精确 SHA 对应的 CI Check、阻塞 Finding 和豁免权威。依赖只能由绑定精确修订的 Durable GitHub 证据或已接受 Run Ledger 记录满足；“已完成”的评论不是证明。

## 7. Publication idempotency / 发布幂等

Before each side effect, Publication Broker checks:
- current work key and work state;
- active lease and fencing token;
- expected base/head SHA;
- prompt digest and Owner approval;
- allowed mutation type/path;
- whether the same publication idempotency key already completed.

Each publication intent has a durable state: PREPARED → SUBMITTED → CONFIRMED, or UNKNOWN/FAILED/RECONCILE_REQUIRED. Because GitHub and the local store do not share a transaction, ambiguous API outcomes require re-fetch and reconciliation before retry. Do not blindly repeat a create operation.

每次副作用前，Broker 检查 Work Key/状态、有效租约/fencing token、预期 SHA、Prompt Digest/Owner 批准、允许变更类型/路径及该 Publication Key 是否已完成。Publication Intent 状态为 PREPARED → SUBMITTED → CONFIRMED，或 UNKNOWN/FAILED/RECONCILE_REQUIRED。GitHub 与本地存储不共享事务，API 结果不确定时必须先重读对账，不能盲目重试 Create 操作。

## 8. Acceptance tests / 验收测试

- EVT-01 duplicate delivery IDs create one inbox identity.
- EVT-02 distinct delivery IDs for the same current revision coalesce.
- EVT-03 out-of-order event cannot revert target revision.
- EVT-04 changed PR head supersedes queued old-head work.
- EVT-05 running old-head worker cannot publish after supersession.
- EVT-06 required check on wrong SHA does not satisfy dependency.
- EVT-07 issue comment content cannot bypass prompt/authorization policy.
- EVT-08 retry after ambiguous GitHub API outcome reconciles before mutation.
- EVT-09 same publication key does not create duplicate side effects.
- EVT-10 policy epoch change invalidates stale eligibility.
- EVT-11 repository ID/name mismatch is rejected.
- EVT-12 replay/reconciliation discovers missed events without duplicate work.

测试要求覆盖重复 Delivery、语义合并、乱序、Head 变化、旧 Worker 发布、错误 SHA Check、评论注入、API 不确定结果、Publication 去重、Policy Epoch、仓库身份不匹配及漏事件对账。

## 9. Decision / 决议

**OPEN.** The canonical tuple and mapping above are proposed. A, I, affected Owner(s) and Testing/Quality must approve field semantics, serialization, policy epoch ownership and test vectors before implementation. Do not treat an illustrative hash format as frozen wire schema.

**OPEN。** 上述 Canonical Tuple 和映射均为提案。实现前须由 A、I、相关 Owner 和 Testing/Quality 批准字段语义、序列化、Policy Epoch 权威及测试向量。示例 Hash 格式不得视为已冻结 Wire Schema。
