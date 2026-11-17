# PRODUCT-FIRST-001 — Session 04: Security, Authorization & Governance Product Adoption
# PRODUCT-FIRST-001 — 会话 04：安全、授权与治理产品采用性研究

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Research baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Research branch: `research/product-first-001-session-04-security-governance`
- Status: **RESEARCH / CANDIDATE RECOMMENDATIONS ONLY**
- Authority: No Security / Forget / Lifecycle / Evidence contract is changed by this report.
- Decision: No technology is approved or frozen. Draft PR only; do not merge.

---

## 0. Executive Decision / 执行摘要

### English

**Recommendation: evaluate Cedar as the only initial policy-evaluation product candidate; do not adopt OPA and OpenFGA together. Do not introduce OpenFGA in the minimum runnable system.** Keep authentication/principal binding, authorization-state authority, permission/revocation epochs, Forget authorization and fences, enforcement, and audit evidence under Brain/I and the owning domain contracts.

Cedar is unusually well aligned with this Rust architecture: the official `cedar-policy` Rust crate embeds the evaluator in-process and provides a schema-aware policy validation path. It avoids a mandatory policy sidecar/service and a second database. It is a PDP/policy language, not an identity provider, relationship database, grant/revocation authority, PEP, or durable audit ledger.

OPA is capable and general-purpose, but its common non-Go integration is a separate local daemon/sidecar or a Wasm runtime plus a project-maintained host SDK/management plane. That is additional operational and integration surface for a single Rust modular monolith. OPA remains a valid later candidate if cross-language policy distribution, infrastructure policy, or a broad policy ecosystem becomes a measured requirement.

OpenFGA is a specialized relationship authorization service. It is a plausible later fit if Brain develops substantial, high-fan-out user/group/resource sharing and inherited relationship graphs. It introduces a separate Go service, tuple store, model lifecycle, synchronization/reconciliation, availability, and consistency concerns. It must not become the source of truth for Brain memory identity, Scope ownership, grants, Forget, or lifecycle.

**No multi-engine stack is recommended.** If later evidence proves both attribute/guardrail policies and large relationship graphs are required, a deliberately composed Cedar + OpenFGA design may be evaluated. One authoritative PEP decision path must combine both with deny-on-error and current revocation fencing; neither product can independently grant access.

### 中文

**建议：将 Cedar 作为首个策略求值产品候选进行验证；不同时引入 OPA 和 OpenFGA；最小可运行系统暂不采用 OpenFGA。** 身份认证与 Principal 绑定、授权状态权威、Permission/Revocation Epoch、Forget 授权与 Fence、执行强制点以及审计证据，继续由 Brain/I 和各 Owner 契约掌握。

Cedar 与 Rust 架构高度匹配：官方 `cedar-policy` Rust crate 可在进程内嵌入求值器，并提供基于 Schema 的策略验证能力。它不强制增加策略 Sidecar/服务或第二套数据库。但 Cedar 只是 PDP/策略语言，不是身份提供方、关系数据库、Grant/Revocation 权威、PEP 或持久化审计账本。

OPA 功能强大且通用，但非 Go 系统的常见集成方式是独立本地 Daemon/Sidecar，或 Wasm Runtime 加项目自行维护的 Host SDK/管理平面。对于单体 Rust 模块化架构，这会增加运行与集成面。若未来经过测量确认存在跨语言策略分发、基础设施策略或广泛策略生态需求，OPA 仍可重新评估。

OpenFGA 是专门的关系授权服务。如果 Brain 将来出现大量用户/群组/资源共享及继承关系图，它可能适用。但它会引入独立 Go 服务、Tuple Store、Model 生命周期、同步/协调、可用性和一致性问题。它不能成为 Brain Memory 身份、Scope 归属、Grant、Forget 或 Lifecycle 的事实权威。

**不建议多引擎组合。** 若未来证据证明同时需要属性/护栏策略与大型关系图，可再评估 Cedar + OpenFGA 的组合。组合必须有唯一权威 PEP 决策路径，采用错误即拒绝并执行当前撤销 Fence；任何一个产品都不能单独授予访问权。

### Evidence / 证据状态

- **VERIFIED** — Current main README says the repository is an architecture definition and implementation has not started by design.
- **VERIFIED** — Main bilingual security guide says security is end-to-end, Scope is not Permission, missing required Scope is deny/indeterminate, async workers reauthorize, and identity/permission unavailability fails closed.
- **VERIFIED** — D canonical Forget contract separates D's canonical fence/suppression authority from I's global authorization, revocation, retention, backup/external-copy, and physical-erasure authority.
- **PARTIALLY VERIFIED** — Product capabilities and current public documentation were inspected; no Brain prototype, workload benchmark, license counsel review, or production security audit was performed.
- **VERIFIED** — This report is research only and does not change a normative contract.

证据状态：
- **VERIFIED** — 当前 main README 声明仓库是架构定义，按设计尚未开始生产实现。
- **VERIFIED** — main 双语安全指南明确安全是端到端属性、Scope 不等于 Permission、缺少必需 Scope 时拒绝/不确定、异步 Worker 重新授权、身份/权限不可用时 Fail Closed。
- **VERIFIED** — D Forget 规范区分 D 的 Canonical Fence/抑制权威与 I 的全局授权、撤销、Retention、备份/外部副本及物理擦除权威。
- **PARTIALLY VERIFIED** — 已检查产品能力和当前公开文档；未运行 Brain 原型/负载基准，未进行律师许可审查或生产安全审计。
- **VERIFIED** — 本报告仅为研究，不修改规范性契约。

---

## 1. Baseline / 基线

### 1.1 Exact repository baseline / 仓库精确基线

| Item | Evidence | Status |
|---|---|---|
| Repository | `oahcom/AiMemoryBrainArchitecture` | VERIFIED |
| Default branch | `main` | VERIFIED |
| HEAD | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | VERIFIED |
| Repository purpose | Architecture specification repository | VERIFIED |
| Production implementation | Not started by design, per README | VERIFIED |
| Security guide | `docs/en/09-security-governance/security-governance-guide.md`, Blob `3d3fa33c016c1c601374bab1e621cfec8b2b403d` | VERIFIED |
| Chinese security guide | `docs/zh-CN/09-security-governance/security-governance-guide.md`, Blob `57423eaab9053f7b59869a493fedec583601f7fb` | VERIFIED |
| D Forget Fence contract | D branch `session-d-memory-brain-2026-11-16`, Blob `1f0391bc49d007c44ec74165bd33d37412cc7990` | VERIFIED |
| D Lifecycle Manager | D branch `session-d-memory-brain-2026-11-16`, Blob `8b972035b449e1eab546aedc9cc5b30581600c65` | VERIFIED |
| D Memory Brain overview | D branch `session-d-memory-brain-2026-11-16`, Blob `b4ed712ac0626ab127cccfd205c50a9013df01fb` | VERIFIED |

### 1.2 Existing security authority / 现有安全权威

The current main security guide is explicitly **CANDIDATE global governance contract; not production security certification**. It describes three planes:

1. Identity Plane — establish the authenticated actor/principal and producer/service binding.
2. Decision Plane — evaluate Actor, Action, Resource, typed Scope, delegation, policy, consent/retention, and current epochs.
3. Enforcement/Evidence Plane — domain owners enforce at their boundaries; I governs cross-system revocation, retention, audit and global Forget completion.

Current guide invariants:
- ScopeRef is not Permission.
- PermissionEpoch invalidates stale decisions/leases; ForgetFence is a separate D-owned suppression generation.
- Caller-provided ActorRef, payload identity, display names and model output do not prove authentication.
- Required Scope dimensions missing means deny/indeterminate, never wildcard.
- Reauthorize at ingress, canonical read, Evidence dereference, mutation, lifecycle transition, Context activation/delivery, export/share, Forget, audit, and async worker execution.
- Identity/permission outage fails closed for protected operations.
- Backup restore must apply Forget fences before restored content becomes queryable or deliverable.
- Logs/metrics must not leak protected payloads; audit metadata and source content have different retention/erasure rules.

当前 main 安全指南状态明确为 **CANDIDATE 全局治理契约；不是生产安全认证**。它定义三个平面：身份平面、决策平面、执行/证据平面。

现有不变量包括：ScopeRef 不等于 Permission；PermissionEpoch 与 D 的 ForgetFence 不可混淆；调用方自报身份不构成认证；必需 Scope 缺失时拒绝/不确定而非通配；入口、读取、Evidence 解引用、修改、Lifecycle、Context 投递、导出、Forget、Audit 和异步执行均需授权；权限服务故障时 Fail Closed；Backup Restore 必须先应用 Forget Fence；日志不得泄露受保护内容。

**Status: VERIFIED** against the two current-main bilingual guides. The guides are candidate governance contracts, not implementation evidence.

### 1.3 Prior PR context / 既有 PR 背景

| PR | Verified description-level context | Relevance | Status |
|---|---|---|---|
| #45 | Historical TECH-REALITY-001-A research, old base `b372b62...`, research head `6c7c591...`; includes Cedar/OPA/OpenFGA product scan | Prior product scan is not current approval | VERIFIED description; current exact PR metadata/readback not fully re-established |
| #56 | Independent review of #45; verdict REVISE / feasibility NOT YET PROVEN; identified source-currentness and evidence gaps | Do not inherit #45 recommendations as approved | VERIFIED description |
| #73 | Draft remediation based on main `b3c666e...`; role-simulated integration; explicitly says D/E/I/Storage Phase 3.8 sources remain proposals and no real Owner sign-off is claimed | Current-source caveats and authority boundaries | VERIFIED description; PR body evidence only |

PR #45/#56/#73 are research/review/remediation artifacts, not approvals of Cedar, OPA, OpenFGA, or security architecture. PR #56's REVISE finding is not silently closed by this session. Exact PR head metadata and all review threads were not independently fetched in this run.

PR #45/#56/#73 的说明分别表明：#45 是历史技术研究；#56 对其给出 REVISE / NOT YET PROVEN；#73 是基于当前 main 的角色模拟整改材料，并明确没有真实 Owner 签署。它们都不是 Cedar/OPA/OpenFGA 或安全架构批准。PR #56 的 REVISE 不会因本会话而自动关闭。本轮未完整重新读取三项 PR 的最新 Head 元数据和全部 Review Threads。

---

## 2. Product Comparison / 产品比较

### 2.1 Cedar

**What it provides**
- Authorization policy language and deterministic PDP/authorizer.
- Principal / Action / Resource / Context request shape (PARC).
- Permit/forbid policies, default deny, forbid-overrides-permit.
- Schema validation/type checking when policies are created or changed.
- Rust-native `cedar-policy` crate for in-process evaluation.
- Policy/entity inputs remain application-supplied; Cedar does not authenticate principals or own durable policy/grant state.

**Critical semantic caveat**
Cedar's documented evaluator uses **skip-on-error** for an individual policy: an evaluation error causes that policy to be ignored in the combined result. Default deny applies only if no Permit policy successfully matches. Therefore, Brain must not treat a plain Cedar `Allow` as sufficient if any relevant policy evaluation error occurred. The Brain authorization wrapper must inspect diagnostics and convert any relevant error, missing entity, malformed context, schema mismatch, unknown policy revision, or incomplete input into **Indeterminate → Deny**. This is a mandatory integration rule, not an optional configuration.

**Fit**
Strong fit for a Rust modular monolith and a single initial policy engine. It avoids an external PDP service. It does not supply relationship tuple persistence, authentication, revocation epochs, policy activation authority, or tamper-evident audit evidence.

**Status:** VERIFIED for documented capability and Rust crate availability; PARTIALLY VERIFIED for production suitability because Brain-specific performance, MSRV compatibility, dependency review and adversarial conformance remain untested.

### 2.1 Cedar（中文）

**提供能力**
- 授权策略语言和确定性 PDP/Authorizer。
- Principal / Action / Resource / Context（PARC）请求结构。
- Permit/Forbid、默认拒绝、Forbid 优先于 Permit。
- 策略创建/更新阶段的 Schema 验证和类型检查。
- Rust 原生 `cedar-policy` crate，可进程内求值。
- Principal 与实体数据由应用提供；Cedar 不认证 Principal，也不拥有持久化 Policy/Grant 状态。

**关键语义风险**
Cedar 文档说明单条策略求值错误采用 **skip-on-error**：出错策略会从组合决策中忽略。默认拒绝只在没有任何成功匹配的 Permit 时生效。因此 Brain 不能在存在相关策略错误时，仅凭 Cedar 返回的 `Allow` 放行。Brain 授权封装层必须检查 Diagnostics，并将任何相关错误、实体缺失、Context 格式错误、Schema 不匹配、未知 Policy Revision 或输入不完整转换为 **Indeterminate → Deny**。这是强制集成规则，而非可选配置。

**适配性**
非常适合 Rust 模块化单体作为首个策略引擎，无需外部 PDP 服务。但不提供关系 Tuple 持久化、身份认证、撤销 Epoch、策略激活权威或防篡改审计证据。

**状态：** 产品能力和 Rust crate 可用性 VERIFIED；Brain 生产适用性 PARTIALLY VERIFIED，仍需 MSRV/性能/依赖审查及对抗性一致性测试。

Official references:
- https://docs.cedarpolicy.com/auth/authorization.html
- https://docs.cedarpolicy.com/policies/validation.html
- https://docs.cedarpolicy.com/other/security.html
- https://docs.rs/cedar-policy/latest/cedar_policy/
- https://github.com/cedar-policy/cedar

### 2.2 OPA

**What it provides**
- General-purpose policy decision engine and Rego policy language.
- Explicit PDP/PEP separation.
- REST API, Go SDK, and compiled Wasm integration options.
- Policy/data bundles, bundle revision metadata, optional signature verification, status and decision logs.
- Broad infrastructure and cross-language policy use cases.

**Costs and risks for this project**
- REST integration usually means an OPA process/sidecar and secured local API.
- Wasm removes the OPA daemon from the request path, but Brain must own a Wasm runtime, host integration, supported built-in constraints, SDK, policy activation/version management, health/status and decision-log delivery.
- OPA's bundle updates are eventually consistent; an older replica can serve an older bundle. Signature verification proves bundle integrity/authenticity, not that the bundle is the newest or that a revoked permission is already absent.
- Decision logs can contain full input and result; explicit masking/minimization and a separate authoritative audit sink are required.
- Rego is general-purpose and therefore broader than the narrow authorization policy surface currently demonstrated by Brain.

**Fit**
OPA is not intrinsically unsuitable. It is simply not the minimum-complexity fit for an initial Rust modular monolith with no proven need for a cross-stack policy platform. Reconsider only if the same policy engine must govern multiple languages/services, infrastructure policy, or organization-wide policy distribution.

**Status:** VERIFIED for deployment/integration modes and bundle/log capabilities; PARTIALLY VERIFIED for Brain fit; no Brain OPA/Wasm prototype exists.

### 2.2 OPA（中文）

**提供能力**
- 通用策略决策引擎和 Rego 语言。
- 明确 PDP/PEP 分离。
- REST API、Go SDK、编译为 Wasm 的集成方式。
- Policy/Data Bundle、Revision 元数据、可选签名校验、Status 和 Decision Log。
- 适用于基础设施和跨语言策略场景。

**本项目的成本与风险**
- REST 集成通常意味着额外 OPA 进程/Sidecar 及受保护的本地 API。
- Wasm 虽然可从请求路径中移除 OPA Daemon，但 Brain 仍需负责 Wasm Runtime、Host 集成、内建函数支持约束、SDK、Policy 激活/版本管理、健康状态和 Decision Log 投递。
- OPA Bundle 更新是最终一致的；旧 Replica 可能提供旧 Bundle。签名只能证明 Bundle 完整性/来源可信，不能证明它是最新版本，也不能证明已撤销权限已经消失。
- Decision Log 可能包含完整输入和结果，必须进行显式脱敏/最小化，并另设权威审计 Sink。
- Rego 的通用性超过 Brain 当前已证明需要的授权策略范围。

**适配性**
OPA 并非技术上不适合，只是不符合当前 Rust 模块化单体的最小复杂度目标。只有当多个语言/服务、基础设施策略或组织级策略分发成为真实需求时才重新评估。

**状态：** 部署/集成方式、Bundle/Log 能力 VERIFIED；Brain 适配性 PARTIALLY VERIFIED；尚无 Brain OPA/Wasm 原型。

Official references:
- https://www.openpolicyagent.org/docs
- https://www.openpolicyagent.org/docs/deploy
- https://www.openpolicyagent.org/docs/integration
- https://www.openpolicyagent.org/docs/management-bundles
- https://www.openpolicyagent.org/docs/management-decision-logs

### 2.3 OpenFGA

**What it provides**
- Zanzibar-inspired relationship-based authorization (ReBAC).
- Authorization models plus relationship tuples; Check/List APIs.
- Immutable authorization model versions; clients can pin a model ID.
- PostgreSQL/MySQL storage and a separate Go server; SQLite is documented as beta in the current repository README.
- Query consistency controls. `HIGHER_CONSISTENCY` can bypass cache and read the database, at additional latency.

**Costs and risks for this project**
- Requires a separate service and tuple store, plus secure service authentication, availability, database migrations, model deployment, tuple writes, reconciliation and operational telemetry.
- Relationship tuples duplicate or project relationships already owned by Brain. Every relationship change must be transactionally or recoverably synchronized; drift can over-grant or deny.
- Default cached checks can retain an old allow until cache expiry when permissions change. Higher consistency reduces this risk by reading the database, but it does not create an atomic transaction with Brain's protected operation or define Brain's PermissionEpoch/ForgetFence.
- It is not a complete authentication solution and not a general replacement for Cedar-style ABAC/guardrail policy.
- It does not own Brain's canonical memory/relationship truth, lifecycle, Forget dependency graph, external deletion or audit evidence.

**Fit**
Potential future specialist for high-volume, complex sharing/group inheritance. Not justified for initial adoption until relationship query complexity and workload are measured. A relational model in Brain's authoritative store plus Cedar policy evaluation is simpler at current stage.

**Status:** VERIFIED for core model/service capabilities and public consistency controls; PARTIALLY VERIFIED for Brain workload fit and operational cost; no Brain tuple projection or consistency prototype exists.

### 2.3 OpenFGA（中文）

**提供能力**
- 受 Zanzibar 启发的关系授权（ReBAC）。
- Authorization Model + Relationship Tuple；支持 Check/List API。
- Authorization Model 不可变版本；调用方可 Pin Model ID。
- PostgreSQL/MySQL 存储与独立 Go Server；当前仓库 README 将 SQLite 标记为 Beta。
- 提供查询一致性选项；`HIGHER_CONSISTENCY` 可绕过缓存直接读取数据库，但会增加延迟。

**本项目的成本与风险**
- 增加独立服务、Tuple Store、服务认证、可用性、数据库迁移、Model 发布、Tuple 写入、对账和运维遥测。
- Tuple 可能复制或投影 Brain 已拥有的关系。每次关系变化都必须事务性或可恢复地同步，漂移可能导致过度授权或错误拒绝。
- 默认缓存检查在权限变化后可能持续返回旧 Allow，直到缓存 TTL 到期。Higher Consistency 通过直接读库降低风险，但不能与 Brain 受保护操作构成原子事务，也不能定义 Brain 的 PermissionEpoch/ForgetFence。
- 它不是完整身份认证方案，也不能全面替代 Cedar 风格的 ABAC/Guardrail 策略。
- 它不拥有 Brain Canonical Memory/Relation 真相、Lifecycle、Forget 依赖图、外部删除或审计证据。

**适配性**
未来若出现高规模复杂共享/群组继承，可以作为专门组件。当前尚无关系查询复杂度和负载证据，不足以支持首期引入。现阶段 Brain 权威存储中的关系模型加 Cedar 策略求值更简单。

**状态：** 核心模型/服务能力及公开一致性选项 VERIFIED；Brain 负载适配性和运维成本 PARTIALLY VERIFIED；没有 Brain Tuple 投影或一致性原型。

Official references:
- https://openfga.dev/project
- https://openfga.dev/blog/query-consistency-options-announcement
- https://github.com/openfga/openfga
- https://github.com/openfga/openfga/blob/main/docs/architecture/architecture.md

### 2.4 Other candidates / 其他候选

| Candidate | Potential role | Disposition | Status |
|---|---|---|---|
| Casbin | Embedded RBAC/ABAC policy library, multiple languages | Not preferred over Cedar for Rust-native typed policy validation; compare only if Cedar integration fails | PARTIALLY VERIFIED |
| SpiceDB | Zanzibar-style ReBAC service | Similar deployment/tuple consistency costs to OpenFGA; no reason to evaluate both initially | UNVERIFIED for this Brain workload |
| AWS Verified Permissions | Managed Cedar-based policy service | Vendor-managed service may conflict with model-agnostic/local-first and adds cloud dependency; possible future hosted deployment option | PARTIALLY VERIFIED |
| Cedar + OpenFGA | Attribute/guardrail + graph relationship split | Future-only, requires one composite PEP and a common epoch/fencing protocol | CANDIDATE / NOT APPROVED |

---

## 3. Capability Mapping / 能力映射

| Capability | Mature product contribution | Brain/I authority that remains | Status |
|---|---|---|---|
| Policy evaluation | Cedar PDP; OPA alternative | Brain supplies trusted PARC/context and decides error semantics | VERIFIED |
| Authorization | Cedar evaluates allow/deny | I owns policy/grant authority; PEPs enforce | VERIFIED |
| ReBAC | OpenFGA optional graph evaluation | Brain owns canonical typed relations; I owns grants and Scope binding | PARTIALLY VERIFIED |
| ABAC | Cedar attributes/context; OPA Rego | Brain resolves trusted attributes, never caller assertions | VERIFIED |
| Multi-tenant isolation | Products can evaluate tenant attributes/relations | Brain resolves mandatory typed Scope at every read/write edge; DB constraints/RLS may be defense in depth only | VERIFIED |
| Policy versioning | Cedar policy sets/schema; OPA bundle revisions; OpenFGA model IDs | I owns activation authority, monotonic policy revision, effective-from and rollback rules | PARTIALLY VERIFIED |
| Revocation | Product cache/refresh/consistency mechanisms | I owns PermissionEpoch/GrantEpoch and revocation authority; PEP must enforce current epoch | VERIFIED |
| Audit | OPA decision logs; Cedar diagnostics; OpenFGA/OTel telemetry | I owns authoritative append-only audit evidence and retention/redaction rules | VERIFIED |
| Data access enforcement | Products return decisions | Every Brain/Storage/Index/Cache/Adapter/Worker PEP enforces before disclosure or side effect | VERIFIED |
| Forget authorization | Cedar can evaluate request permission | I authorizes; D owns operation/fence; no PDP product may mark Forget complete | VERIFIED |
| Provider permission | Policy may decide whether a provider may receive a payload | I owns provider trust/recipient policy; H/C enforces at actual egress and records truthful ACK | VERIFIED |
| Agent tool permission | Policy can evaluate a tool/action/resource request | Brain does not become Agent planner/tool executor; host Agent PEP remains responsible and must not treat memory text as authority | VERIFIED |
| Security observability | OTel/logs/metrics/decision diagnostics | I audit ledger remains evidence authority; telemetry is not proof of authorization or Forget | VERIFIED |

---

## 4. Security Boundary Analysis / 安全边界分析

### 4.1 Required five-authority separation / 必须区分的五种权威

| Plane / Authority | Meaning | Proposed owner | Product may help? |
|---|---|---|---|
| PDP — Policy Decision Point | Computes a policy decision from a trusted request | Cedar candidate behind I-owned policy activation | Yes |
| PEP — Policy Enforcement Point | Blocks or permits the actual read/write/egress/worker side effect | Each owning boundary: API, D, E, F, G, H/C, Storage, export/restore | Product SDK can assist; cannot replace boundary ownership |
| Authorization State Authority | Authoritative Principal/Grant/Delegation/Scope binding and active policy version | I governance state, backed by canonical durable storage | No product becomes authority by default |
| Revocation Authority | Monotonic revocation/PermissionEpoch and rules for stale decisions/leases | I; enforced by all PEPs | Products may distribute signals, not own final revocation truth |
| Audit Evidence Authority | Durable evidence of request, decision, policy/epoch, enforcement and result | I-governed append-only evidence store; domain receipts from PEPs | Product logs are supplemental only |

A PDP response is not an enforcement receipt. A PEP receipt is not a grant. A grant is not a Forget fence. A trace is not audit evidence. A successful policy evaluation is not proof that the data read or provider egress was actually protected.

PDP 决策不是执行回执；PEP 回执不是 Grant；Grant 不是 Forget Fence；Trace 不是审计证据；策略求值成功也不能证明数据读取或 Provider Egress 确实受到保护。

### 4.2 Request contract / 请求契约

Every protected decision request must be constructed by trusted Brain code, not accepted as arbitrary model or caller JSON:

- authenticated Principal/ActorRef bound to verified transport/session identity;
- explicit Action enum and typed ResourceRef;
- resolved owner Scope plus all required applicability scopes;
- trusted attributes with provenance and freshness;
- purpose, delegation chain, provider/recipient identity where applicable;
- current policy revision and PermissionEpoch/GrantEpoch;
- ForgetFence/lineage status for data-bearing resources;
- correlation/causation IDs and non-sensitive request digest.

Missing, unresolved, stale, conflicting, or untrusted inputs are **Indeterminate → Deny**. No wildcard fallback. A Cedar entity/context input is an evaluation fact, not an identity credential.

### 4.3 Enforcement points / 执行强制点

Mandatory PEP locations:
1. Ingress / authentication binding.
2. Canonical read and every provenance/evidence dereference.
3. Every relationship edge and target traversed.
4. Mutation, lifecycle transition and grant/delegation change.
5. Retrieval candidate materialization, cache read/write and index projection.
6. Context snapshot/delta activation and inference delivery.
7. Provider payload egress, export and sharing.
8. Queue admission, lease acquisition, retry, replay and final publication.
9. Forget request initiation/approval and each irreversible cleanup action.
10. Backup restore before data becomes queryable or deliverable.
11. Audit/evidence read and administrative policy mutation.

A vector DB metadata filter is a prefilter/defense-in-depth only. It cannot authorize access because filters can be stale, omitted, malformed, bypassed by alternate code paths, or applied before relationship/evidence dereferences. Every returned candidate must be re-authorized against canonical identity, Scope, policy/grant revision, PermissionEpoch and ForgetFence before disclosure.

Agent Runtime tool allowlists are local PEP configuration, not Brain authorization truth. The model/Agent may request an action; it cannot mint Principal, Scope, Grant, permission, or bypass a PEP. Provider-side permission/consent and data-retention promises must be checked at egress and evidenced; a provider's API acceptance is not proof of its downstream deletion.

### 4.4 Fail-closed wrapper / Fail-Closed 封装

The policy adapter returns a typed tri-state result:

- `Permit(decision_id, policy_revision, permission_epoch, diagnostics)`
- `Deny(decision_id, policy_revision, permission_epoch, reason)`
- `Indeterminate(error_class, missing_inputs, observed_revision)`

Only Permit may proceed, and only if the PEP independently confirms current epoch/fence at the enforcement point. For Cedar, any policy evaluation error in the relevant decision set must force Indeterminate regardless of the Cedar combined decision. Policy engine timeout, crash, unknown revision, failed signature, stale epoch, schema mismatch or incomplete relationship lookup also force Indeterminate.

---

## 5. Revocation and Forget Analysis / 撤销与 Forget 分析

### 5.1 Revocation invariants / 撤销不变量

A revoked permission must not remain effective merely because a token, queue item, cache, OPA bundle, OpenFGA cache, Agent session, vector index, or Adapter previously observed an Allow.

Required minimum semantics:
1. I durably commits a monotonically increasing PermissionEpoch/GrantEpoch (or equivalent per-scope/resource epoch) with the grant/revocation change.
2. Every decision binds the exact policy revision and observed epoch.
3. Every protected PEP checks that the decision epoch is still current immediately before disclosure or side effect.
4. Async work reauthorizes before lease/execute and again before irreversible publish/egress/commit when the action can outlive the initial check.
5. Caches are keyed by principal, typed Scope set, action, resource/version, policy revision, epoch, environment and relevant ForgetFence. Invalidation is an optimization; epoch comparison is the safety mechanism.
6. If current epoch cannot be established, protected action is denied/indeterminate.
7. For a protected write, the authorization epoch must be fenced with the write (same transaction/conditional commit or an equivalent proven serialization protocol). A check-then-write race is not sufficient.
8. A revocation receipt records the new epoch and the PEP propagation/observation state; do not claim global revocation completion until all mandatory PEPs have observed/enforced the fence or a policy-approved bounded exception exists.

### 5.2 What products can and cannot guarantee / 产品能保证与不能保证的内容

- Cedar is an evaluator. It does not invalidate cached application decisions or manage PermissionEpoch.
- OPA bundle signing authenticates bundle contents; bundle activation is eventually consistent. It does not guarantee that every replica has the newest policy at the instant a grant is revoked.
- OpenFGA `HIGHER_CONSISTENCY` bypasses its cache and reads the database, reducing stale-check risk. It still does not atomically serialize a Brain data operation with Brain's authorization epoch and does not own ForgetFence.
- No selected product replaces a Brain-side revocation fence, PEP checks or recovery protocol.

### 5.3 Forget is a separate authority and state machine / Forget 是独立权威和状态机

Forget is not a permission revoke and is not a policy update. It requires:
- I authenticates and authorizes the Forget request, checks subject rights, ownership, Scope, purpose, delegation, retention and legal hold.
- D creates the durable ForgetOperation, monotonic ForgetFence generation, target-set digest, producer registration barrier and canonical suppression proof.
- E/F/G/H/Storage/Backup/External Recipient owners enforce their own suppression/cleanup boundary and provide per-target evidence.
- I determines global completion, approved residual exceptions, backup/external-copy policy and physical-erasure requirements.
- Restore/replay/rebuild must reapply the latest fence before any content becomes visible.

PermissionEpoch and ForgetFence must never be conflated. A grant revocation prevents a principal from acting; a ForgetFence suppresses the target/lineage for all applicable principals and producers. Replacing one with the other creates both over-blocking and resurrection vulnerabilities.

### 5.4 Critical race / 关键竞态

A non-atomic sequence of:
`read current ForgetFence → process → publish derivative`
is unsafe. D's contract requires durable producer registration before work, fence/barrier capture, register-before-visible dependency inventory, and a final fence check immediately before publication. A stale authorization or a current PermissionEpoch cannot override a later ForgetFence. The publish gate must enforce both independent controls.

**Status:** The D contract is VERIFIED as a source requirement; implementation/linearizability is NOT VERIFIED. No product in this comparison supplies this Brain-specific proof.

---

## 6. Deployment and License Risks / 部署与许可风险

| Product | Integration/deployment | License evidence | Key operational risks | Status |
|---|---|---|---|---|
| Cedar | Rust crate in-process; no required daemon | Apache-2.0 in official repo/docs.rs | Pin exact crate/MSRV; review transitive dependencies/features; policy/schema rollout; bound input sizes; skip-on-error wrapper | VERIFIED license/capability; PARTIAL compatibility |
| OPA | Sidecar/daemon REST or Wasm runtime + host SDK | OPA project Apache-2.0 (verify exact distribution artifacts before adoption) | Extra process/runtime, secure local API, bundle freshness, signing config, management APIs, log masking, resource usage | PARTIAL |
| OpenFGA | Go server + PostgreSQL/MySQL; SQLite beta; HTTP/gRPC | Apache-2.0 in official repository | Extra service/database, tuple drift, cache staleness, model migration, API authentication, HA/backup/monitoring | VERIFIED license/repo facts; PARTIAL workload cost |

Deployment recommendation:
- Initial architecture: Cedar library inside the Rust process, policy data/version metadata in the existing authoritative Brain persistence boundary; no new authorization service or database.
- Do not persist Cedar policy decisions as durable grants. Persist source grants/relations/decisions and version references in Brain/I authority; evaluate per request.
- Avoid storing full memory text, Evidence payloads, prompt content, provider payloads or secrets in policy inputs or decision logs. Pass typed IDs, minimal trusted attributes and digests.
- Pin exact dependency version and lockfile; review MSRV, feature flags, unsafe/dependency tree, release cadence and security advisories before any implementation approval.
- OpenFGA, if later justified, should be a separate optional service with its own database and explicit synchronization contract; it must not be a required dependency for canonical reads until availability/failure behavior is proven.
- OPA remains an alternate, not an additional mandatory component.

部署建议：
- 首期采用 Rust 进程内 Cedar Library，策略数据/版本元数据放在现有 Brain 权威持久化边界，不增加授权服务或数据库。
- 不把 Cedar 决策持久化为 Grant。Brain/I 保存源 Grant/Relation/Decision 及版本引用，每次请求重新求值。
- Policy Input/Decision Log 不保存 Memory 全文、Evidence 内容、Prompt、Provider Payload 或 Secret，只传递类型化 ID、最小可信属性和 Digest。
- 在批准实现前 Pin 精确依赖版本与 Lockfile，审查 MSRV、Feature、Unsafe/依赖树、发布节奏和安全公告。
- OpenFGA 只有在后续证据充分时才作为可选独立服务，并建立明确同步契约；在可用性/故障语义未证明前，不得成为 Canonical Read 的必要依赖。
- OPA 作为替代候选，而不是额外强制组件。

License notes:
- Cedar official repository and docs.rs currently report Apache-2.0; official Cargo metadata surfaced version 4.14.0 and Rust version 1.89. These are current research observations, not a pinned project selection.
- OpenFGA official repository reports Apache-2.0; its README describes PostgreSQL 14+, MySQL 8, and SQLite beta.
- OPA's exact license and notices must be checked against the exact binary/container/source artifact chosen at adoption time; this report does not constitute legal review.
- Transitive dependency licenses, bundled assets, trademarks, and SaaS/service terms require a separate software bill of materials/license scan.

许可说明：
- Cedar 官方仓库/docs.rs 当前报告 Apache-2.0；官方 Cargo 元数据显示版本 4.14.0、Rust 版本 1.89。这是本次研究观察，不是项目锁定版本。
- OpenFGA 官方仓库报告 Apache-2.0；README 描述 PostgreSQL 14+、MySQL 8、SQLite Beta。
- OPA 必须在采用时针对实际选用的二进制/容器/源码制品核验许可证和 Notice；本报告不构成法律审查。
- 传递依赖、内置资源、商标及 SaaS/服务条款需单独进行 SBOM/许可证扫描。

---

## 7. Adoption Matrix / 采用矩阵

| Capability | Recommendation | Initial status | Gate to reconsider |
|---|---|---|---|
| Cedar policy evaluator | **ADOPT AS VALIDATION CANDIDATE** | CANDIDATE / NOT APPROVED | Rust compatibility, deny-on-error wrapper, typed input contract, conformance and benchmark |
| OPA | DEFER | NOT ADOPTED | Demonstrated multi-language/cross-service policy need that Cedar cannot meet economically |
| OpenFGA | DEFER | NOT ADOPTED | Measured graph depth/fan-out/sharing workload; tuple sync proof; consistency and availability tests |
| Casbin | DEFER | NOT ADOPTED | Cedar integration/expressiveness failure backed by prototype |
| Cedar + OpenFGA | FUTURE OPTION ONLY | NOT APPROVED | Composite PEP, common epoch/fence semantics, failure matrix and end-to-end evidence |
| Brain/I authorization state | KEEP INTERNAL / AUTHORITATIVE | Existing contract ownership | Owner approval and conformance; no external product substitution |
| Revocation/PermissionEpoch | KEEP INTERNAL / AUTHORITATIVE | Candidate contract | Atomic state transition + PEP observation/fault-injection proof |
| ForgetFence/operation/completion | KEEP D/I AUTHORITY | D/I contracts | Existing Owner gates; this research cannot change them |
| Audit evidence | KEEP I-GOVERNED AUTHORITY | Candidate governance contract | Append-only integrity, access controls, retention and evidence verification |
| PEP enforcement | KEEP AT EACH DOMAIN BOUNDARY | Contractual requirement | Per-boundary negative tests and runtime proof |

---

## 8. Recommended Security Architecture / 推荐安全架构

### 8.1 Logical flow / 逻辑流程

```text
Authenticated Transport / Session
          |
          v
Identity Binding (I policy; trusted ActorRef)
          |
          v
Typed Authorization Request Builder
  Principal + Action + Resource + Scope + Purpose
  Trusted Attributes + Policy Revision + PermissionEpoch
  ForgetFence / lineage status
          |
          v
Cedar PDP (in-process candidate)
          |
          v
Fail-Closed Decision Adapter
  Any relevant eval error => INDETERMINATE / DENY
          |
          v
Domain PEP at actual operation boundary
  Recheck current PermissionEpoch + ForgetFence
  Fence authorization with protected write/egress
          |
          v
Domain operation / response
          |
          +----> PEP enforcement receipt
          |
          v
I-governed append-only Audit Evidence
```

### 8.2 Authority placement / 权威归属

- I: Principal/issuer/delegation trust, policy activation, grants, Scope-to-principal binding, PermissionEpoch/revocation, retention, audit governance, global Forget completion.
- D: canonical Memory identity/version/lifecycle, ForgetOperation, ForgetFence generation, producer barrier and canonical suppression proof.
- E/F/G/H/C/Storage: local PEP enforcement and boundary-specific receipts; no owner may delegate away its enforcement obligation to a query filter.
- Cedar: pure PDP evaluation over trusted inputs and the active policy snapshot.
- OpenFGA (future optional): graph relation query only; tuples are a derived/managed authorization projection, not canonical Brain relationship truth.
- OTel: operational telemetry/correlation only; not an audit evidence authority.

### 8.3 Minimum implementation sequence (not authorization to implement) / 最小实现顺序（不构成实现授权）

1. Define typed request/response and authority boundaries; no product dependency yet.
2. Define I-owned policy revision, grant/epoch, revocation and trusted-attribute sources.
3. Build a pure policy adapter interface and a deterministic fake PDP for PEP conformance tests.
4. Prototype Cedar in-process and enforce deny-on-any-relevant-evaluation-error.
5. Add one protected read/write PEP path and demonstrate epoch/fence recheck at the final boundary.
6. Add audit evidence receipt and negative tests.
7. Only then evaluate OpenFGA/OPA based on measured unmet requirements.

No step authorizes modifying existing Security/Forget/Owner contracts. Any semantic changes require the owning review/ADR path.

---

## 9. Threat Model Changes / 威胁模型变化

| Threat | Product-related failure mode | Required mitigation |
|---|---|---|
| Stale Allow after revocation | Cedar caller cache, OPA stale bundle, OpenFGA cache TTL | Monotonic I epoch; final PEP epoch check; fail closed if unavailable |
| Cedar skip-on-error | A relevant policy errors but another Permit still returns Allow | Inspect diagnostics; any relevant error => Indeterminate/Deny |
| Policy rollback/replay | Older valid signed policy bundle/model activated | Monotonic policy revision/anti-rollback; trusted activation ledger |
| Cross-tenant leakage | Caller-supplied tenant attribute or omitted filter | Trusted typed Scope resolution at every PEP; missing Scope denies |
| Tuple drift | OpenFGA tuple projection differs from canonical relation/grant state | Transactional/outbox sync, reconciliation, fail-closed uncertainty |
| PDP bypass | Direct database, index, cache, provider, worker or restore path skips decision | Enumerated PEP coverage; deny-by-default boundary tests |
| Check-then-use race | Permission revoked or Forget fence advanced after initial check | Epoch/fence recheck at commit/egress; serialize or CAS with write |
| Agent prompt injection | Memory text asks agent to invoke tool or widen permission | Memory is data only; Agent host PEP checks independent principal/grant |
| Evidence side-channel | Unauthorized caller learns existence through reference traversal/error | Authorize each edge/target; not-found-or-not-visible responses |
| Audit data leakage | OPA logs contain full inputs; telemetry contains content | Data minimization, field masking, separate audit schema and access policy |
| Forget resurrection | Restore/replay/index rebuild emits forgotten descendant | D fence and lineage recheck before visibility; restore barrier |
| Provider copy ambiguity | Provider accepted request but hidden copy/retention unknown | I recipient policy; H egress PEP; per-recipient truthful evidence and exception |
| Service outage | PDP/relationship service unavailable | Protected operation fail closed; explicit degraded state, no stale allow fallback |
| Policy administrator compromise | Malicious or accidental policy grants broad access | Restricted policy mutation, review, schema validation, signed/versioned activation, audit |
| Denial-of-service | Huge policy/context/entity graph or relationship traversal | Input limits, Cedar schema/type validation, OpenFGA traversal bounds, timeouts and quotas |

---

## 10. Acceptance Criteria / 验收标准

All criteria are **NOT YET TESTED** unless a test artifact is attached. A future product adoption must pass all mandatory items below.

| ID | Acceptance criterion | Required evidence | Status |
|---|---|---|---|
| SEC-PF-01 | Every protected action has an enumerated PEP; no direct bypass | PEP inventory + negative integration tests | NOT TESTED |
| SEC-PF-02 | Principal/ActorRef bound to authenticated transport identity | spoofing and invalid credential tests | NOT TESTED |
| SEC-PF-03 | Required typed Scope missing/ambiguous => deny/indeterminate | cross-tenant adversarial tests | NOT TESTED |
| SEC-PF-04 | Cedar schema validates policy set before activation | invalid policy/schema fixtures | NOT TESTED |
| SEC-PF-05 | Any relevant Cedar evaluation error => Indeterminate/Deny | error-injection tests, including Permit + unrelated/relevant error cases | NOT TESTED |
| SEC-PF-06 | Default deny and forbid-overrides-permit preserved | truth table and property tests | NOT TESTED |
| SEC-PF-07 | Policy revision anti-rollback; no stale policy activation | restart/replica/replay tests | NOT TESTED |
| SEC-PF-08 | Revocation epoch invalidates cached/queued/leased authorization | cache, queue, lease and worker race tests | NOT TESTED |
| SEC-PF-09 | Authorization epoch fenced with protected mutation/egress | concurrent revoke-vs-commit fault injection | NOT TESTED |
| SEC-PF-10 | PDP outage/timeout/unknown revision fails closed | outage and timeout tests | NOT TESTED |
| SEC-PF-11 | Every Evidence edge/target independently authorized | graph traversal and side-channel tests | NOT TESTED |
| SEC-PF-12 | Vector/index/cache filter cannot independently authorize | bypass and stale projection tests | NOT TESTED |
| SEC-PF-13 | Forget request authorized by I; D Fence remains independent | owner contract conformance tests | NOT TESTED |
| SEC-PF-14 | Fence/lineage rechecked before publish, restore and replay | race/rebuild/backup-restore tests | NOT TESTED |
| SEC-PF-15 | Unknown/failed/unsupported targets never count as Forget success | per-target completion proof tests | NOT TESTED |
| SEC-PF-16 | Provider egress is authorized at actual egress boundary | provider deny/revoke/timeout tests | NOT TESTED |
| SEC-PF-17 | Agent tool invocation cannot inherit authority from memory text | prompt-injection/tool-host PEP tests | NOT TESTED |
| SEC-PF-18 | Audit evidence binds actor, action, resource, scope, policy revision, epoch, decision, PEP result and time | tamper/omission/replay verification | NOT TESTED |
| SEC-PF-19 | Logs/metrics do not expose protected content | redaction and data-leak tests | NOT TESTED |
| SEC-PF-20 | Product version, MSRV, license and transitive dependencies are pinned/reviewed | Cargo lock/SBOM/license report | NOT TESTED |
| SEC-PF-21 | Bilingual text has clause-level semantic parity | independent bilingual review | NOT TESTED |
| SEC-PF-22 | No Security/Forget/Owner contract changed without its Owner approval | diff and Owner approval evidence | VERIFIED for this research-only change; future changes not tested |

### Explicit non-acceptance / 明确不接受的情况

- A Cedar `Allow` with a relevant evaluation error.
- An OPA bundle signature treated as proof of freshness/revocation.
- An OpenFGA cached `allowed=true` treated as current authorization without epoch/fence validation.
- A vector DB filter, SQL filter, Agent tool list, Provider consent flag, or cache key treated as the sole PEP.
- A queue-time decision treated as permanent worker authorization.
- A tombstone, ACK, telemetry event or product log treated as global Forget completion.
- A product's own policy store treated as Brain's canonical identity, grant, relation, lifecycle or audit authority.

---

## 11. Open Risks and Closure Conditions / 未解决风险与关闭条件

| Risk | Current status | Closure condition |
|---|---|---|
| I source contract exact files and current branch/head were not exhaustively re-read in this session | PARTIALLY VERIFIED | Read all I normative files at exact branch/head; pin Blob SHAs and review status |
| Current main guide is candidate, not security certification | VERIFIED | I Owner approval plus independent review and conformance evidence |
| PermissionEpoch/GrantEpoch transactional semantics and cache invalidation details | OPEN / NOT VERIFIED | I contract defines scope, monotonicity, linearization and PEP propagation |
| Cedar skip-on-error handling is an integration hazard | VERIFIED product behavior; mitigation NOT TESTED | Deny-on-any-relevant-error wrapper plus adversarial tests |
| Cedar MSRV/dependency compatibility with eventual Brain Rust baseline | OPEN | Pin exact version and run workspace build/security/SBOM review |
| OPA bundle freshness and rollback protection | PARTIALLY VERIFIED | If adopted, define anti-rollback activation ledger and PEP epoch fence |
| OpenFGA tuple synchronization and cache semantics | PARTIALLY VERIFIED | If adopted, define canonical-to-tuple outbox, reconciliation, HIGHER_CONSISTENCY policy and race tests |
| No measured Brain ReBAC workload | UNVERIFIED | Produce representative relationship graph, fan-out, latency and update workload |
| PEP inventory may omit hidden data paths | OPEN | Enumerate all read/write/egress/worker/restore paths; independent threat review |
| Audit evidence immutability and retention/forget interactions | OPEN | I-approved evidence schema, tamper detection, retention and access tests |
| D fence + Storage atomic publish gate / end-to-end suppression | OPEN | D/E/Storage integration and crash/race/fault-injection proof |
| Provider and external-recipient deletion evidence | OPEN | I recipient policy, H truthful ACK mapping, explicit residual exceptions |
| PR #56 findings about prior research package | REVISE remains prior disposition | Separate reviewer must assess this report at exact base/head; no inherited approval |

---

## 12. Final Disposition / 最终结论

### English

1. **Cedar: RECOMMENDED CANDIDATE for a bounded Rust in-process PDP prototype. Not approved, not frozen.**
2. **OPA: DEFER.** Revisit only for demonstrated cross-language/cross-service policy distribution or infrastructure policy requirements.
3. **OpenFGA: DEFER.** Revisit only when measured relationship graph scale/complexity justifies a separate authorization service and tuple synchronization.
4. **Do not adopt multiple products in the minimum runnable system.**
5. Keep identity, authorization state, revocation, Forget, PEP enforcement and audit evidence as explicit Brain/I/domain authorities.
6. Product adoption cannot relax Scope, permission, ForgetFence, Evidence, lifecycle, restore or fail-closed invariants.
7. No technology decision, architecture freeze, contract change, implementation authorization or production-readiness claim is made.

### 中文

1. **Cedar：推荐作为 Rust 进程内 PDP 原型候选。尚未批准、尚未冻结。**
2. **OPA：暂缓。** 只有出现已证明的跨语言/跨服务策略分发或基础设施策略需求时重新评估。
3. **OpenFGA：暂缓。** 只有测量证明关系图规模/复杂度足以支持独立授权服务和 Tuple 同步时重新评估。
4. **最小可运行系统不引入多个产品。**
5. 身份、授权状态、撤销、Forget、PEP 执行和审计证据继续作为明确的 Brain/I/领域权威。
6. 产品采用不能弱化 Scope、Permission、ForgetFence、Evidence、Lifecycle、Restore 或 Fail-Closed 不变量。
7. 本报告不作技术决策批准、架构冻结、契约变更、实现授权或生产就绪声明。

---

## Appendix A — Source and Evidence Register / 附录 A — 来源与证据登记

### Repository sources / 仓库来源

1. Main README at `b3c666e67982cb3d3374e759cfb6552c7765aacb`.
2. `docs/en/09-security-governance/security-governance-guide.md` Blob `3d3fa33c016c1c601374bab1e621cfec8b2b403d`.
3. `docs/zh-CN/09-security-governance/security-governance-guide.md` Blob `57423eaab9053f7b59869a493fedec583601f7fb`.
4. D `03-memory-brain/forget-fence-and-completion-contract.md` Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`.
5. D `03-memory-brain/memory-lifecycle-manager.md` Blob `8b972035b449e1eab546aedc9cc5b30581600c65`.
6. D `03-memory-brain/memory-brain-overview.md` Blob `b4ed712ac0626ab127cccfd205c50a9013df01fb`.
7. PR #45, #56, #73 descriptions as noted in §1.3; these are historical context, not normative source.

### Product sources / 产品来源

- Cedar authorization semantics: https://docs.cedarpolicy.com/auth/authorization.html
- Cedar validation: https://docs.cedarpolicy.com/policies/validation.html
- Cedar security best practices: https://docs.cedarpolicy.com/other/security.html
- Cedar Rust crate: https://docs.rs/cedar-policy/latest/cedar_policy/
- Cedar official repository/license/MSRV: https://github.com/cedar-policy/cedar
- OPA deployment: https://www.openpolicyagent.org/docs/deploy
- OPA integration modes: https://www.openpolicyagent.org/docs/integration
- OPA Wasm: https://www.openpolicyagent.org/docs/wasm
- OPA bundles/signatures/eventual consistency: https://www.openpolicyagent.org/docs/management-bundles
- OPA decision logs and masking: https://www.openpolicyagent.org/docs/management-decision-logs
- OpenFGA project and deployment: https://openfga.dev/project
- OpenFGA consistency options: https://openfga.dev/blog/query-consistency-options-announcement
- OpenFGA repository/license/storage: https://github.com/openfga/openfga
- OpenFGA architecture: https://github.com/openfga/openfga/blob/main/docs/architecture/architecture.md

### Evidence status legend / 证据状态定义

- **VERIFIED** — exact repository artifact or official product documentation was read and supports the stated fact.
- **PARTIALLY VERIFIED** — source supports part of the claim, but Brain-specific compatibility, current exact version, runtime behavior or independent review is incomplete.
- **UNVERIFIED** — no direct evidence or test was obtained; treat as an open question, not a fact.
- **NOT TESTED** — an acceptance criterion is specified but no executable evidence was produced.

---

**End of report. / 报告结束。**
