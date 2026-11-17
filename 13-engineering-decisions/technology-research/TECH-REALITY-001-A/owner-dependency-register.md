# Owner Dependency Register / Owner 依赖登记表

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **INPUT REQUIRED — NO OWNER DECISION INFERRED / 需要输入，不推断 Owner 决策**

## 1. Register / 登记表

| Owner | Required confirmation | A's concrete question | Technology impact | Blocking? |
|---|---|---|---|---|
| B — Domain Model | Fact/Claim ADR; typed IDs and Scope/Principal/Actor mapping; temporal/epistemic constraints | Which canonical types and uniqueness/identity constraints must persist independently? Which fields remain blocked by Fact/Claim? | SQL schema, keys, indexes, serialization, migrations, provenance | Yes for schema freeze |
| C — Agent Integration | Adapter deployment tiers; final inference-request Applied evidence; provider egress and identity binding | What exact adapter capabilities and evidence are available in Tier 1/2/3, and where is the final request boundary? | Protocol, SDK language, process topology, auth, context delivery, provider side effects | Yes for Applied/adapter topology |
| D — Canonical Memory | CanonicalCommitCursor, lifecycle and Forget authority; fence semantics | What exact durable operation linearizes producer admission against Forget and canonical visibility? | SQL transaction, lock/CAS, cursor schema, restore and publication gate | Critical |
| E — Memory Compiler | Accepted Event, idempotency, durable work state, lease/retry and staged derivatives | Can Event + outbox + blob registration be committed/recovered without false Accepted? What is the durable work and fence admission sequence? | Outbox/worker, queue choice, model isolation, blob staging, DLQ/replay | Critical |
| F — Memory Runtime | Retrieval channels, ranking, activation, watermarks, cache/fence filtering | What is the minimum channel set for first vertical slice? Which filters are authoritative before ranking/context? | FTS5/Tantivy/vector selection, cache, index topology and rebuild | Yes for search selection |
| G — Memory Context | ContextVersion authority, ChangeSet, delivery and Applied consumption | Which state is durable vs recomputable, and what evidence can G accept as Applied? | Context persistence, delivery queue, snapshot/delta, retry and protocol | Critical for context sync |
| H — BMCP Protocol | Wire schema/version, capability negotiation, ACK taxonomy | What message encoding/transport and compatibility rules are normative? How does ACK bind to C final-request evidence? | JSON/CBOR/gRPC/HTTP/IPC, SDKs, versioning and identity envelope | Yes for protocol freeze |
| I — Security & Governance | Principal/Actor identity, Scope/Permission, PermissionEpoch, revocation, Forget targets, key custody | Is Cedar-like embedded policy compatible? What revocation and restore guarantees are required? Which target classes are mandatory? | Policy engine, auth boundary, cache semantics, audit, crypto and backup | Critical |
| Storage / Consistency | Physical transaction topology; COC/JF-10 protocol bridge; prepared transaction support | Which database/topology is approved, and what exact transaction/participant evidence proves the required cross-owner operations? | SQLite vs PostgreSQL, prepared XID, locks, durable COC, recovery cutoff | Critical |
| Testing / Quality | Executable reference model, race/fault matrix, conformance vectors | Which test harness can prove both serial orders, crash windows, replay, restore and no-resurrection? | Prototype scope, CI, fault injection and acceptance gates | Critical |
| Observability / Performance | Correlation IDs, redaction, queue/index/Forget/Applied metrics | Which metrics and audit records are mandatory and which latency/capacity objectives are measurable? | tracing, OTel, exporters, dashboards, SLOs | Yes for SLO baseline |
| Release / Operations | Target OS, packaging, upgrade, backup/restore, deployment and RTO/RPO | Which platforms and operator responsibilities are in scope for first release? | systemd/OCI, migration, key store, backup and restore | Yes for deployment acceptance |

## 2. Required response format / 输入要求

Each Owner response should identify:
1. Exact source branch, commit SHA, path and Blob SHA.
2. Current status (DECIDED / CANDIDATE / OPEN / ADR-BLOCKED / TO_VALIDATE).
3. Normative contract and explicit non-guarantees.
4. Physical technology capabilities required.
5. Required tests and evidence.
6. Dependencies on other Owners and unresolved conflicts.

Each Owner's domain decision remains with that Owner. A's role is to map dependencies, expose incompatibilities and produce system-level alternatives, not to decide on their behalf.

各 Owner 的领域决策仍由对应 Owner 负责。A 的职责是映射依赖、暴露不兼容项并提出系统级备选方案，而不是代替 Owner 决策。

## 3. Current known blocking inputs / 当前已知阻塞输入

- B Fact/Claim ADR remains ADR-BLOCKED according to current consolidation issue #43 and PR #44.
- D/Storage serialization topology remains ADR-BLOCKED; exact physical transaction proof is incomplete.
- D/E/Storage producer admission, fence and publication gate remains critical OPEN work tracked by Issue #25.
- C/G/H Applied chain is not frozen; Issue #3 says Applied Contract Frozen = NO.
- I Global Forget target inventory/governance remains blocked per Issues #4/#5 and PR #44.
- JF-10 Gate B/C remain blocked; COC recovery-cutoff and JF-10 prepared-participant bridge are distinct protocols and automatic composition is not approved.

## 4. Escalation rule / 升级规则

If an owner-owned semantic contract is missing or conflicting, mark the affected technology recommendation **BLOCKED**. Do not fill the gap with a library default, a model inference, or a simulated owner approval.

## 5. 完整中文版本 / Chinese Version

### 5.1 Owner 输入需求

| Owner | 必须确认的事项 | A 需要回答的问题 | 技术影响 | 是否阻塞 |
|---|---|---|---|---|
| B 领域模型 | Fact/Claim ADR、Typed ID、Scope/Principal/Actor 映射、时间/认知约束 | 哪些 Canonical Type 和唯一性约束必须持久化？哪些字段被 Fact/Claim 阻塞？ | SQL Schema、Key、Index、Protocol、Migration | Schema 冻结阻塞 |
| C Agent 集成 | Adapter Tier、Final Inference Request Applied、Provider Egress | 各 Tier 能力和最终请求边界是什么？ | Protocol、SDK、部署、Auth、Provider 副作用 | Applied/Adapter 拓扑阻塞 |
| D Canonical Memory | CanonicalCommitCursor、Lifecycle、Forget Fence | Producer Admission 与 Forget Fence 的线性化点是什么？ | SQL Transaction、Lock/CAS、Cursor、Restore | 严重阻塞 |
| E Compiler | Accepted Event、Idempotency、Work State、Lease/Retry、Derivative | Event+Outbox+Blob 如何持久且不产生虚假 Accepted？ | Outbox/Worker、Queue、Inference、Blob | 严重阻塞 |
| F Retrieval | 检索通道、Ranking、Activation、Watermark、Cache/Fence | 首个切片的最小通道是什么？候选前如何权威过滤？ | FTS5/Tantivy/Vector/Cache | Search 选型阻塞 |
| G Context | ContextVersion、ChangeSet、Delivery、Applied | 哪些状态持久化，哪些可重建？Applied 如何验证？ | Context DB、Outbox、Snapshot/Delta | Context 同步阻塞 |
| H Protocol | Wire Schema/Version、Capability、ACK | 编码/传输/兼容规则是什么？ACK 如何绑定 C Final Request？ | JSON/CBOR/gRPC/HTTP/IPC | Protocol 冻结阻塞 |
| I Security | Principal/Actor、Scope/Permission、PermissionEpoch、Revocation、Forget Inventory、Key Custody | Cedar 是否符合 I 语义？撤销和 Restore 要求是什么？ | Policy、Auth、Cache、Audit、Crypto | 严重阻塞 |
| Storage/Consistency | 物理事务拓扑、COC/JF-10、Prepared XID | 批准何种 DB/拓扑？哪些证据证明跨 Owner 操作？ | SQLite/PostgreSQL、Lock、Recovery | 严重阻塞 |
| Testing | Reference Model、Race/Fault Matrix、Conformance | 哪些 Harness 能证明双向竞争、崩溃、Replay、Restore？ | Prototype、CI、Fault Injection | 严重阻塞 |
| Observability | Correlation、Redaction、Queue/Index/Forget/Applied Metrics | 必须记录哪些指标？哪些 SLO 可测？ | tracing、OTel、Dashboard | SLO 基线阻塞 |
| Release/Ops | OS、Packaging、Upgrade、Backup、RTO/RPO | 首发支持哪些平台？谁负责运维？ | systemd/OCI、Migration、Key、Backup | 部署验收阻塞 |

### 5.2 Owner 回答格式

每个 Owner 必须给出精确 Source Branch/Commit/Path/Blob、状态（DECIDED/CANDIDATE/OPEN/ADR-BLOCKED/TO_VALIDATE）、规范契约及不保证项、物理技术能力要求、测试证据、跨 Owner 依赖和未解决冲突。A 只负责集成映射和暴露不兼容，不代替领域决策。

### 5.3 当前已知阻塞

- B Fact/Claim ADR 仍 ADR-BLOCKED。
- D/Storage 序列化物理实现和 JF-10 应用桥接仍未闭合；Storage 最新 ADR 只关闭逻辑 v1 序列化档案。
- D/E/Storage Producer Admission、Fence、Dependency、Publication 仍是关键 OPEN。
- C/G/H Applied Contract Frozen = NO。
- I Global Forget Target Inventory 和治理审批仍阻塞。
- JF-10 Gate B 修订协议需要精确 Owner 复审，Gate C 延后到工程阶段，Runtime P0 仍 OPEN。


## 6. Current successor-bundle dependency update — 2026-11-17 / 后继 Bundle 依赖更新

Storage v3.2.6 manifest Blob `dbfa37617d109d5891a067769e858085e2ce547a` binds the current candidate interfaces, but explicitly records **NOT JOINTLY FROZEN** and H 1.2.13 exact CI OPEN. This is a delegated Storage-role manifest, not independent human Owner approval.

- **C:** CSubmitOutcome 1.0.1 candidate CI (19 tests) is recorded SUCCESS; provider-specific idempotency and UNKNOWN outcome recovery remain OPEN.
- **D:** structural carrier candidate reviewed; lineage completeness, late-discovery and final release CAS remain OPEN.
- **H:** Unified 1.2.13 / wire 1.3.0, RecoveryJoin 1.0.2 and RecoveryCutoff 1.0.5 are pinned; exact 1.2.13 CI is NOT RUN, despite predecessor H 1.2.12 CI.
- **I:** structural I P0 candidate and crypto profile architecture are recorded; L3 family vectors, production trust/key status, anti-rollback and production activation remain OPEN.
- **Storage:** PostgreSQL 18.7 has seven isolated CI capability subtests PASS; Gate A remains PARTIAL PASS / OPEN. Live COC/I/D application integration and production deployment are not proven.

These statuses refine the earlier TAR currentness snapshot; they do not replace Owner authority or authorize a technology choice.

Storage v3.2.6 Manifest 绑定当前候选接口，但明确记录 **NOT JOINTLY FROZEN**，H 1.2.13 精确 CI OPEN。该 Manifest 是委派 Storage 角色工件，不是独立人工 Owner 批准。

- **C：** CSubmitOutcome 1.0.1 候选 CI（19 项）记录为 SUCCESS；Provider 特定幂等和 UNKNOWN 结果恢复仍 OPEN。
- **D：** 结构载体候选已有审查；Lineage 完整性、迟到发现和最终 Barrier Release CAS 仍 OPEN。
- **H：** Unified 1.2.13 / wire 1.3.0、RecoveryJoin 1.0.2、RecoveryCutoff 1.0.5 已绑定；精确 1.2.13 CI 未运行，旧 H 1.2.12 CI 不可转移。
- **I：** I P0 结构候选和 Crypto Profile 架构已有记录；L3 家族向量、生产信任/密钥状态、防回滚和生产激活仍 OPEN。
- **Storage：** PostgreSQL 18.7 七项隔离 CI 能力子测试 PASS；Gate A 仍 PARTIAL PASS / OPEN。实时 COC/I/D 应用集成和生产部署未证明。

这些状态用于细化此前 TAR 当前性快照，不替代 Owner 权威，也不授权技术选型。
