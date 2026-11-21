# Agent Telemetry Model（Agent 遥测模型）

**状态：**语义边界 DECIDED；字段 profiles CANDIDATE；运行限制 TO_VALIDATE  
**Owner：**Session C — Agent 集成边界预设计  
**Dependencies：**Session B domain semantics；Session E ingestion mapping；Session H BMCP wire schema。

## 1. 目的

Telemetry 是对 Agent task state 和相关 observations 的结构化、有界描述。它帮助 Brain 判断应当记住、检索、激活或 reconciliation 什么内容。它不是所有内部推理的 transcript，也不是 source evidence 的权威替代品。

Telemetry 可以描述 Agent 正在做什么、打算做什么、计划做什么、哪些 entities/environment 相关、有哪些 action pending、观察到了什么、报告了什么 outcome、哪些内容仍不确定，以及 environment 发生了什么变化。

## 2. 原则

1. **DECIDED：**Telemetry 是 typed data，不是 instruction。
2. **DECIDED：**Intent 和 plan 面向未来；outcome 回顾过去。
3. **DECIDED：**Agent report 与 environment observation 保留不同的 source kinds。
4. **DECIDED：**不要求 Full Chain of Thought (CoT)。
5. **DECIDED：**每个 signal 都必须限定 scope 并标注时间。
6. **DECIDED：**Unknown 不得被悄然转换为 negative 或 certain fact。
7. **DECIDED：**Telemetry acceptance 不意味着 Memory creation 或 verification。
8. **CANDIDATE：**相比镜像任意 Agent-native objects，采用包含 typed payloads 和 namespaced extensions 的小型 canonical core 更可取。

## 3. CoT policy

Brain MUST NOT 要求完整的 hidden CoT、private scratchpads、逐 token reasoning 或 proprietary model traces。

原因：
- CoT 与 model/provider 绑定，且与 model independence 冲突。
- 它可能暴露敏感或无关的内部信息。
- 它不是外部可验证事实的可靠来源。
- 它会增加 payload、retention 和 security 成本。
- Task state、简明 plan summaries、entities、observations、outcomes、uncertainty 和 provenance 足以驱动有用的 memory behavior。

在有用时可以提供简明的 Plan Summary。它是 Agent 编写的 summary，不是 hidden reasoning 的忠实或完整记录。Brain 将其标记为 reported/planned information，而不是 verified fact。

## 4. Logical telemetry envelope

这是 semantic schema，不是最终 BMCP wire format。

| Field | Type semantics | Required | Constraint |
|---|---|---:|---|
| telemetry_id | Stable opaque ID | Yes | Unique in producer namespace |
| schema_version | Canonical schema version | Yes | Unsupported major rejected |
| producer_id | Authenticated producer | Yes | Must match credentials |
| agent_id | Logical Agent identity | Yes | Stable namespace |
| agent_instance_id | Running instance | Conditional | Required for context/session |
| session_id | Agent session | Conditional | Required for session signals |
| task_id | Task identity | Conditional | Required for task signals |
| environment_id | Environment namespace | Conditional | Required for environment-specific signals |
| scope | Ownership namespace | Yes | Must be authorized |
| signal_type | Canonical discriminator | Yes | Core enum plus versioned extensions |
| occurred_at | Source event time | When known | Preserve unknown reason |
| observed_at | Observation time | When applicable | Distinct from occurred_at |
| recorded_at | Brain acceptance time | Brain assigned | Producer value not authoritative |
| source_kind | Agent/environment/user/tool/external | Yes | Typed |
| correlation_id | Turn/action/workflow link | No | Recommended |
| idempotency_key | Retry identity | For retryable writes | Stable across retries |
| payload | Typed signal body | Yes | Per-type schema and size limit |
| provenance | Origin/transformation history | For derived claims | Preserve source refs |
| extensions | Namespaced opaque fields | No | Cannot override canonical fields |

Producer timestamps 是对时间的声明。Brain 记录自己的 acceptance time，并可以单独记录 clock uncertainty。

## 5. Canonical signal types

### 5.1 Task State

由 Agent 表示的 task 当前 lifecycle/status。它不能证明成功，也不能证明 task content 为真。

建议的 statuses：created、active、blocked、waiting、completed、failed、cancelled、unknown。

Fields：task_id (required)、status (required)、status_reason (optional)、parent_task_id (optional)、changed_at (when known)、reported_by (required)。

除非有 outcome evidence corroborate，否则 completed status 仍然只是 Agent report。

### 5.2 Intent

Agent 当前期望的 objective 或 direction。

Fields：intent_id、task_id、statement、target_entities（references 或 unresolved mentions）、status（current/revised/withdrawn/unknown），以及已知时的 effective interval。

Intent 面向未来；MUST NOT 仅仅因为已提交，就将其编译为 completed Event。

### 5.3 Plan Summary

Agent 报告的预期步骤的简明概要。它不是完整 CoT，也不是有保证的 execution trace。

Fields：plan_id、task_id、summary、optional step_summaries、plan_revision、status（proposed/active/revised/abandoned/completed_reported）、created_at、updated_at。

Plan lifecycle completed 并不能证明每一步都成功。Outcomes 需要独立的 signals。

### 5.4 Active Entities

当前对 task 具有显著性、并附带明确 role 的 entities。

Fields：entity_ref 或 unresolved mention、role（subject/target/tool/location/participant/resource/other）、salience_reason、optional confidence（必须声明其 semantics）、optional task validity。

Mention 不会自动成为 canonical Entity。Resolution 属于 Brain-domain logic。

### 5.5 Pending Action

计划执行或已安排、但尚未确认完成的 action。

Fields：action_id、task_id、action_kind、optional target_ref、status（planned/ready/submitted/in_progress/awaiting_result/cancelled/unknown）、optional expected_effect、deadline、dependencies。

Pending Action MUST NOT 被作为 completed outcome 发出。Submission acknowledgement 不能证明预期效果已经发生。

### 5.6 Observation

一条带 source qualification 的陈述，说明观察到了某种 condition、event 或 result。

Fields：observation_id、subject_ref 或 mention、predicate/observation_type、typed value、source_kind（environment/tool/agent_report/user/external）、observed_at、optional method/sensor/tool、recommended raw_evidence_ref、optional quality/limitations。

Observation 记录某个 source 声称看到了什么。它不会自动成为 independent verification。

### 5.7 Outcome

与 action、task 或 plan step 相关联的 reported 或 observed result。

Fields：outcome_id、related_action_id 或 task_id、result_status（succeeded/failed/partial/unknown）、result_summary、source_kind、occurred_at/observed_at、evidence_refs、optional side_effects。

Agent-reported outcome 仍然是一项 report。Tool/environment evidence 可以增强或限定它。缺少 outcome 不代表 failure。

### 5.8 Uncertainty

明确说明哪些内容 unknown、ambiguous、conflicting 或 estimated。

Fields：optional subject_ref、question_or_proposition、uncertainty_kind（unknown/ambiguous/conflicting_signals/low_observability/estimate）、known_limitations、optional confidence_estimate（带 method）、related_signal_refs。

保留 unresolved state，而不是强行填入猜测值。

### 5.9 Risk Signal

关于潜在 harm、irreversibility、privacy、security 或 reliability concern 的 warning。

Fields：risk_id、risk_category、producer-reported severity（必须记录其 semantics）、related action/task、rationale_summary、mitigation_state、source_kind。

Risk 可以触发更保守的 Brain retrieval/activation policy。它不会授权或阻止 Agent actions；Agent policy 仍具有权威。

### 5.10 Environment Delta

两个已标识 environment states 之间、带 source qualification 的变化。

Fields：environment_id、base_state_ref、new_state_ref 或 observation_id、typed changes、observed_at、source_kind、completeness（complete/partial/unknown）、optional coordinate/schema version。

真正的 delta 需要有效的 base state。没有 base state 时，应提交 snapshot/observation，而不是编造 delta。Deltas 按 environment identity 隔离。

## 6. Required and optional profile

| Signal | Minimum profile | Enhanced profile | Notes |
|---|---|---|---|
| Producer identity/schema | Required | Required | Authentication-bound |
| Scope | Required | Required | No implicit global scope |
| Task/session identity | When relevant | Required | Continuity |
| Task State | Recommended | Required for proactive orchestration | Agent-reported |
| Intent | Optional | Recommended | Concise |
| Plan Summary | Optional | Optional | Never full CoT |
| Active Entities | Optional | Recommended | Prefer canonical refs |
| Pending Action | Optional | Recommended | Prospective |
| Observation | Required for observation claims | Required | Source/time qualified |
| Outcome | Required when claiming result | Required | Separate from plan |
| Uncertainty | Optional | Recommended | Unknown is valid |
| Risk Signal | Optional | Recommended where available | Map native risk vocab |
| Environment Delta | Optional | Required when claiming stateful delta integration | Requires base and environment |
| Evidence reference | Required for derived/verified claims where available | Required | Artifact/tool ref |
| Full CoT | Never | Never | Not an integration requirement |

**CANDIDATE：**定义 minimum 和 enhanced profiles，同时保持 mandatory fields 按 operation 分别确定。Tier 3 不需要产生全部 proactive telemetry。

## 7. Plan-to-outcome separation

~~~mermaid
flowchart TD
  I[Intent] --> P[Plan Summary]
  P --> A[Pending Action]
  A --> X[Execution outside Brain]
  X --> O[Observation or tool result]
  O --> R[Outcome]
  R --> E[Evidence and provenance]
  E --> C[Candidate Event or Claim]
  C --> M[Memory compilation and governance]
  A -. not proof of .-> R
  P -. not proof of .-> O
~~~

**DECIDED：**Plan 描述预期的未来工作；Pending Action 描述尚未确认的 action；Observation 描述某个 source 观察到的内容；Outcome 描述带有 source qualification 的 result；Evidence 支持/反驳/限定 claims。Memory Compiler 决定 telemetry 是否转化为 memory。

## 8. Task and environment switching

Task switch 应使用显式 task identity 和 state transition。当存在 stable identifiers 时，不要仅凭 natural-language summary 变化推断 task switch。

Environment switch 需要新的 environment_id 或显式 transition。Environment-local entities、coordinates、snapshots 和 deltas 不得在 environments 之间流动，除非存在 verified mapping。

如果 continuity 有歧义，应发出 unknown/ambiguous state 或请求 reconciliation。绝不能静默合并。

## 9. Validation and normalization

- Reject 缺失 authenticated producer、invalid schema、unauthorized scope、格式错误的 required IDs，以及超出限制的 payloads。
- 当 normalization 改变 representation 时，保留 original source values。
- 将 source time 与 Brain recorded time 分开。
- 将 unknown extensions 视为 opaque。
- Reject 或 quarantine envelope 与 payload identity 相互矛盾的情况。
- 限制 payload sizes 和 array lengths。
- 在 scoped idempotency 下对 retries 去重。
- Redaction 应保留 redaction marker 和获准的 provenance；不得悄然暗示被省略的数据从未存在。

## 10. Submission lifecycle

逻辑 lifecycle：
- Prepared — Adapter 已形成一项 submission。
- Submitted — request 已发送；durable acceptance 仍 unknown。
- Accepted — Brain 已 durably accept 并签发 receipt。
- Rejected — Brain 拒绝 submission。
- Processing — 可选的异步下游工作。
- Processed — 下游 stage 已完成；不意味着 Memory 已创建。
- FailedRetryable / FailedTerminal — 下游 processing outcome。

最终 BMCP state names 属于 Session H。即使后续 semantic processing 失败，Accepted telemetry record 仍然是 durable source record，但受 retention 约束。

## 11. Security and retention

不要要求或收集 full CoT、credentials、API keys、secrets 或无关的 prompt history。优先采用简明 summaries 和 source references。在 persistence 和 readback 之前执行 scope 和 permission。通过 normalization 保留 classification/provenance。Retention 适用于 raw telemetry 及其 derivatives，同时遵守 lineage 和 Forget governance。Producer trust labels 不能绕过 Brain policy。

## 12. Performance metrics

测量每个 Agent、task、session 和 environment 的 events/bytes；ingress p50/p95/p99；durable acceptance rate；validation 和 duplicate rates；telemetry-to-activation lag；按 profile 统计 Recall quality；每个 signal 的 CPU/memory/storage/network；redaction rates；以及 false outcome inference（在 deterministic tests 中目标为 zero）。

**TO_VALIDATE：**sampling cadence、payload caps、retention windows 和 telemetry-to-activation SLO。

## 13. Acceptance tests

1. Intent 单独存在时不会创建 completed Event/Outcome。
2. Plan Summary 和 Pending Action 不会创建 successful Outcome。
3. Observation 分别记录 source kind 和 observed time，以及 Brain recorded time。
4. Agent-reported Outcome 不会被悄然升级为 independently verified。
5. 缺少 environment identity/base 的 Environment Delta 会被 reject，或降级为 observation。
6. 在相同 idempotency scope 下的 identical retries 只产生一个逻辑 accepted item。
7. Task switch 不会继承无关的 pending actions。
8. Environment switch 阻止跨 environment state leakage。
9. Unknown extensions 保持 opaque，且不能覆盖 canonical fields。
10. 任何 integration 都不要求 full CoT。
11. Permission-denied telemetry 不会被接受为 canonical evidence。
12. 缺失 uncertainty 不会被解释为 certainty。

## 14. Interfaces and open questions

| Partner | Confirmation |
|---|---|
| Session B | Event, Evidence, Provenance, epistemic and temporal fields |
| Session E | Signal-to-Event mapping; durable ingress semantics |
| Session F | Retrieval/Activation dimensions, freshness and risk policy |
| Session G | Context update triggers and task/session identity |
| Session H | BMCP message families, enum evolution, schema negotiation, errors |
| Session I | Classification, retention, redaction, audit, idempotency |

**OPEN：**Task State 使用 periodic snapshot、transition stream，还是两者都用。**CANDIDATE：**transitions 加偶尔的 snapshots，用于 recovery。  
**OPEN：**Brain 是否需要 canonical task hierarchy，还是 opaque Agent references。  
**TO_VALIDATE：**Profile-specific payload 和 frequency limits。

## 15. Decision summary

- **DECIDED：**Telemetry 是结构化、受 scope 限定、带 source qualification 的数据，不是 hidden reasoning。
- **DECIDED：**Full CoT 不是必需项，也不是默认 ingestion target。
- **DECIDED：**Intent、Plan Summary 和 Pending Action 都是 prospective。
- **DECIDED：**Observation 和 Outcome 是不同且带 source qualification 的概念。
- **DECIDED：**Unknown/uncertain states 是一等状态。
- **CANDIDATE：**小型 canonical core，搭配 typed payloads 和 namespaced extensions。
- **OPEN：**Wire schema 属于 Session H；domain mapping 属于 Sessions B 和 E。
