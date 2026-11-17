# Agent Integration Decision Record / Agent 集成决策记录

## C-DEC-001 — Keep Agent Runtime outside Brain domain
- Status: **DECIDED (boundary principle; based on existing main C overview and responsibility matrix)**.
- Context: Agent planning/tool loops must not become canonical Memory authority.
- Alternatives: embed Agent framework into Brain; Brain owns tool execution; external Agent with adapter.
- Decision: external/embedded Agent runtimes remain clients; Brain owns canonical memory and governed context.
- Consequences: adapter contracts and identity checks required; Agent framework replaceable.
- Owner impact: A/B/D/H/I; exact implementation remains open.
- Reversal: only a formal architecture governance decision changing responsibility matrix.
- 中文：Agent Runtime 不属于 Brain 的规范领域权威；Agent 通过 Adapter 访问 Brain，Brain 保留 Memory/Context 治理权。

## C-DEC-002 — Model output is untrusted candidate data
- Status: **DECIDED (B epistemic distinctions + C boundary; exact pipeline OPEN)**.
- Decision: generation does not establish truth, verification or canonical status. Validation/provenance and D/E rules remain mandatory.
- 中文：模型输出不自动成为事实或 Canonical Memory，必须保留来源并经过相应验证与生命周期流程。

## C-DEC-003 — Preserve C Provider Handoff Outcome algebra
- Status: **CANDIDATE / exact joint adoption OPEN**.
- Evidence: historical C Phase 3.8.4 defines HANDOFF_ACCEPTED, HANDOFF_REJECTED, NOT_INVOKED, UNKNOWN, IN_DOUBT.
- Decision: retain as C-owned candidate semantics; do not replace with generic success/failure. H schema and I trust must reconcile exact version.
- Reversal: C Owner and H/I/A exact-version decisions.
- 中文：保留 C 的五态 Handoff 候选语义，等待 H/I/A 精确版本联合核验。

## C-DEC-004 — Layered Provider Capability Registry
- Status: **CANDIDATE**.
- Alternatives: direct per-provider adapters; one lossy common interface; capability registry plus native extensions.
- Decision: narrow normalized port plus provider-specific adapters and explicit capabilities.
- Consequences: more conformance tests, less false compatibility.
- Reversal: representative prototype shows material complexity/performance harm and alternative preserves all guarantees.
- 中文：候选采用能力登记表加 Provider 专属 Adapter，禁止以统一接口掩盖能力差异。

## C-DEC-005 — Modular Integration Layer, not distributed services
- Status: **CANDIDATE / A topology remains unapproved**.
- Decision: modular logical layer in a local-first modular monolith; optional isolated inference process.
- Consequences: simpler local deployment and transaction boundaries; module seams need tests.
- 中文：当前阶段优先模块化集成层，不提前拆成分布式服务。

## C-DEC-006 — OTel trace context, not audit authority
- Status: **CANDIDATE**.
- Decision: use W3C trace context for causal observability; keep audit and authorization evidence under I.
- Consequences: privacy allowlist, redaction, sampling and retention policy required.
- 中文：OTel/W3C 用于调用链关联，不等同于安全审计或业务提交证明。

## OPEN decisions / 未决决策
- C crypto profile and I trust profile registration.
- H 1.2.15 validator/CI and Storage successor bundle.
- G Applied exact predicate and end-to-end acceptance.
- I tool permission/capability policy.
- Provider API version and SDK/license pins.
- Runtime repository/accountable engineering owner (A identifies Issue #7 open).


## 完整中文版本

C-DEC-001：Agent Runtime 位于 Brain 领域之外。状态 DECIDED（边界原则，依据当前 C Overview 和责任矩阵）。Agent 负责规划和工具循环，Brain 保留规范 Memory 权威。Agent Framework 可替换，需 Adapter 和身份检查。除非治理正式修改责任矩阵，否则不得反转此边界。

C-DEC-002：模型输出是未受信候选数据。状态 DECIDED（依据 B 认识论区分和 C 边界，具体流水线仍 OPEN）。模型生成不建立事实、验证或 Canonical 状态。必须保留来源并服从验证、D/E 规则。

C-DEC-003：保留 C Provider Handoff 五态代数。状态 CANDIDATE，精确联合采纳 OPEN。历史 C Phase 3.8.4 定义 HANDOFF_ACCEPTED、HANDOFF_REJECTED、NOT_INVOKED、UNKNOWN、IN_DOUBT。等待 C/H/I/A 精确版本决策。

C-DEC-004：分层 Provider Capability Registry。状态 CANDIDATE。采用窄统一接口加 Provider 专属 Adapter 和明确能力登记。需要更多符合性测试，以换取避免虚假兼容。

C-DEC-005：模块化集成层而非分布式服务。状态 CANDIDATE，A 拓扑仍未批准。候选在本地优先模块化单体内组织模块，Inference Worker 可选隔离。

C-DEC-006：OTel Trace Context 不拥有 Audit 权威。状态 CANDIDATE。W3C Trace Context 用于因果可观测；安全审计和授权证据由 I 负责。

未决事项包括 C/I 密码配置注册、H 1.2.15 Validator/CI、Storage 后继 Manifest、G Applied Predicate、I Tool 权限策略、Provider API/SDK 版本和许可证，以及正式 Runtime 仓库/工程 Owner。
