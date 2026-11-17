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
