# C Canonical Integration Contract / C 规范集成合同

**Status: C-owned semantic requirements proposed; not cross-owner wire-frozen.**

## MUST / 必须
1. Agent, Agent Runtime, Model, Provider, Tool, Session and Principal MUST remain distinct concepts.
2. Every inference Request and Attempt MUST have stable identities and explicit idempotency scope.
3. Provider handoff, execution lifecycle, response receipt, parse, validation, tool execution, Brain commit/visibility and G Applied MUST be distinct evidence stages.
4. Model-generated content MUST NOT be promoted to Verified Claim or Canonical Memory solely because a model or Provider returned it.
5. Provider-native response metadata MUST be preserved where available; absent metadata MUST use explicit unavailable/not-reported/unknown/not-applicable semantics.
6. Retry after ambiguous handoff MUST reconcile the same Attempt and provider idempotency key before creating another Attempt.
7. Late and duplicate results MUST be appended as immutable observations; conflicts require reconciliation.
8. Tool side effects MUST be separately authorized, identified and evidenced; cancellation MUST NOT imply rollback.
9. Brain candidate and write operations MUST pass I authorization and D lifecycle/Forget checks. Agent/Tool has no direct canonical storage path.
10. C final-request evidence MUST bind the actual immutable post-transformation request and actual submit boundary. G alone decides Applied.
11. Trace, Correlation, Request, Attempt, Operation, Session and Principal identifiers MUST NOT be substituted for one another.
12. Telemetry MUST minimize sensitive content and MUST NOT be treated as immutable audit proof.

## MUST NOT / 禁止
- MUST NOT equate HTTP 200, provider acceptance, tool success or output parse with canonical operation success.
- MUST NOT claim NOT_INVOKED from timeout or lost acknowledgement alone.
- MUST NOT retry non-idempotent side effects blindly.
- MUST NOT accept Agent payload identity as authenticated Principal.
- MUST NOT let external Agent mutate canonical Memory or lifecycle state.
- MUST NOT sign C Provider Outcome with an unregistered/untrusted key or claim H/I registration from schema presence.
- MUST NOT use stale Context or Memory references after Forget/revocation invalidation.

## C-owned vs external authority / C 自有与外部权威
C owns Agent/Provider integration requirements, inference request/attempt semantics, Provider handoff evidence, tool integration evidence requirements and telemetry correlation requirements. B owns typed domain meaning; D owns canonical lifecycle/Forget; E owns derived-memory production; F owns retrieval/activation; G owns ContextVersion/Applied; H owns BMCP schema/wire/ACK; I owns identity/authorization/trust/privacy governance; Storage owns durable commit/visibility mechanics; A owns system integration and deployment decision.

## Compatibility / 兼容
C's historical CSubmitOutcome 1.0.1 and H Unified 1.2.15 are candidate artifacts only. This document does not change their schema, fields, signature profile, wire version or acceptance status. Any normative field-level change requires exact owner review and a successor immutable version.


## 完整中文版本

### 必须要求
1. Agent、Runtime、Model、Provider、Tool、Session 和 Principal 必须是不同概念。
2. 每个 Inference Request/Attempt 必须有稳定身份和明确幂等作用域。
3. Provider Handoff、执行生命周期、响应接收、解析、验证、Tool 执行、Brain Commit/Visibility 和 G Applied 必须分开记录。
4. 不能仅因模型或 Provider 返回内容就将其升级为 Verified Claim 或 Canonical Memory。
5. 必须保留 Provider 原生响应元数据；缺失字段使用明确的 Unavailable/Not Reported/Unknown/Not Applicable。
6. Handoff 状态不明确时，必须先对账同一 Attempt 和 Provider Key，再考虑创建新 Attempt。
7. 迟到/重复结果必须作为不可变观察追加；冲突必须进入 Reconciliation。
8. Tool 副作用必须独立授权、标识和留证；取消不等于回滚。
9. Brain 候选和写操作必须通过 I 授权和 D 生命周期/Forget 检查。Agent/Tool 不得直接访问规范存储。
10. C 最终请求证据必须绑定实际不可变请求及真实提交边界；G 独自决定 Applied。
11. Trace、Correlation、Request、Attempt、Operation、Session 和 Principal 标识不得互换。
12. 遥测必须最小化敏感内容，不能替代不可篡改审计证明。

### 禁止要求
不得将 HTTP 200、Provider 接受、Tool 成功或输出解析等同于规范操作成功；不得仅凭超时/ACK 丢失认定 NOT_INVOKED；不得盲目重试非幂等副作用；不得将 Agent 载荷身份当认证主体；不得允许外部 Agent 修改 Canonical Memory 或生命周期；不得在未注册信任密钥上签名或把 Schema 存在误认为 I/H 已批准；Forget/撤权后不得复用失效 Context/Memory Reference。

### 权威边界
C 负责 Agent/Provider 集成要求、推理 Request/Attempt、Provider Handoff 证据、Tool 集成证据要求和遥测关联。B 负责领域类型；D 负责生命周期/Forget；E 负责派生记忆；F 负责检索激活；G 负责 ContextVersion/Applied；H 负责 BMCP Wire/ACK；I 负责身份/授权/信任/隐私；Storage 负责持久化 Commit/Visibility；A 负责系统集成和部署决策。

历史 CSubmitOutcome 1.0.1 与 H Unified 1.2.15 仅为候选。本文不修改其 Schema、字段、签名配置、Wire Version 或接受状态。任何字段级规范变化都必须由权威 Owner 审查并发布不可变后继版本。
