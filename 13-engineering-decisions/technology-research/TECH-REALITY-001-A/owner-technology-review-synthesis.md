# Owner Technology Review Synthesis / Owner 技术审查综合

- Task: TECH-REALITY-001-A | Owner A | Snapshot: 2026-11-17
- Method: directly read current owner-branch trees and each published TAR report; compare the report's reviewed HEAD to the current branch HEAD.
- Status: **OWNER REPORTS ARE DELEGATED STATIC REVIEWS, NOT INDEPENDENT OWNER APPROVALS / Owner 报告属于委派静态审查，不是独立 Owner 批准**

## 1. Current owner branch snapshot / 当前 Owner 分支快照

| Owner | Current branch HEAD observed | TAR report blob read | HEAD recorded inside TAR report | Currentness result |
|---|---|---|---|---|
| B | `8f83e4b172bc6bb41df60de58c1884886b22e617` | `fd3e5723b81de10bed806896e4be71ceb7a1669b` | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | Stale baseline; re-review required |
| C | `667bbf84b89dc1a54ddc02852477a74083d2d89b` | `ee42c7192561261789a0c7b5bd16d32c0eaaf14c` | `0a81f370bfc331872897ff83b6cbe051806cfc7b` | Stale baseline; re-review required |
| D | `97e68fbd225bdf0ac71860c01077481afc162d50` | `97c049050d67dd12e0c64ef49b2b05795651608c` | `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8` | Stale baseline; re-review required |
| E | `fdb4f67a83083d995930b88f93975b5ee36080f3` | `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8` | `4402549c39824b89a0dc49973226187c62e056c5` | Stale baseline; re-review required |
| F | `8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3` | `124cc9300442b0e3a1e83603910e1c332b4fae48` | `61814ec33e7c6851c8b64ed9a7ca581c1ebe0b21` | Stale baseline; re-review required |
| G | `f9ca0ddc36e17f74041506f17039f0202d13042e` | `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613` | `270ac5530182dc84d6bb8b5ae05e84d8f0973803` | Stale baseline; re-review required |
| H | `f809be092a6c04db7982cc1bdbdd9c88787a4286` | `cb9d1d97604bdb71bc2f5bf47f6392e03f30ba99` | `6e7cb95f6c99ef45af9ff4e26915f66141996075` | Stale baseline; re-review required |
| I | `28df608b075e619563c6367a8a1c171185c1faaf` | `c24f03aae6ce7bc76eaeb1ed33bb24fb7fcac624` | `0abd1a26008d90c15cbb7d6ebae0f7325f7c1c1b` | Stale baseline; re-review required |
| Storage | `17be31915b06d98d7f822e6e5270b8cde39eb0bb` | No TAR-AI-001 owner report found | N/A | Review current Storage ADR/dossiers directly |

**Currentness implication:** the TAR documents exist, but their reviewed snapshots predate the branch heads observed in this research. Their verdicts are useful design inputs, not current acceptance of all later owner changes. Each affected Owner must re-review the exact current branch head before any final technology freeze.

**当前性含义：** TAR 文档确实存在，但其审查基线早于本次读取的分支 HEAD。报告裁决可作为设计输入，不能视为对后续全部 Owner 变更的当前批准。正式技术冻结前，各 Owner 必须重新审查精确当前分支 HEAD。

## 2. Owner findings / Owner 结论

### B — Domain Model

- TAR-B-001 Blob: `fd3e5723b81de10bed806896e4be71ceb7a1669b`
- Verdict: **CONDITIONAL PASS** for Rust typed-domain + relational core + immutable revisions.
- Recommends Rust newtypes/enums, normalized relational identity/revision/reference tables, FK/unique constraints, immutable revision snapshots, explicit schema versions and bounded JSON extension fields.
- Serde is a serialization framework, not a schema-evolution policy. JSON/CBOR/MessagePack remain candidates.
- **P0:** Fact/Claim canonical identity remains ADR-001 ADR-BLOCKED. ActorRef/ScopeRef/EnvironmentRef semantic mapping approval does not approve I trust, H wire encoding or database keys.
- No DDL, migration, benchmark, fuzz or database test was executed in the report.

### C — Agent Integration

- TAR-C report Blob: `ee42c7192561261789a0c7b5bd16d32c0eaaf14c`
- Verdict: **CONDITIONAL PASS** for capability-tiered integration.
- Recommends language-neutral BMCP client contract, Rust reference SDK, and at least one sidecar/IPC reference implementation; embedded SDK is an optimization profile, not the only topology.
- HTTP(S) is the initial cross-language path; Unix socket / Windows named pipe is the local sidecar candidate.
- Tier 1 Full Applied requires the Agent runtime's final immutable request submission hook; middleware/tool callbacks generally cannot prove it.
- P1: concrete framework final-submit hook, H/I/G/B exact binding, adapter topology prototype, Forget/revocation clear and reconnect tests, protected-region/prompt-injection tests. No framework integration or runtime hook test executed.
- Provider-specific same-key outcome lookup/idempotency and production provider adapters remain unverified.

### D — Canonical Memory

- TAR-D-001 Blob: `97c049050d67dd12e0c64ef49b2b05795651608c`
- Verdict: **CONDITIONAL PASS** for semantic architecture; implementation/physical storage acceptance remains blocked.
- Requires one authoritative serialization boundary for producer admission, Forget fence, dependency completeness, final visibility and terminal disposition.
- SQLite WAL: acceptable first prototype candidate only; one writer and no external prepared-XID proof. PostgreSQL 18.7: leading qualified CI capability candidate for JF-10 prepared-XID profile, not production DB approval.
- DB transaction must atomically bind canonical revision/head, lifecycle event, CanonicalCommitCursor and outbox as applicable.
- Blob staging and SQL visibility need explicit digest, private staging, metadata registration, orphan reconciliation and coordinated backup.
- P0: D/E/Storage integrated admission/fence/dependency/publication implementation and JF-10 I sequencer + Storage prepared-XID + D lineage integration remain unimplemented / not end-to-end tested.

### E — Memory Compiler

- TAR-E-001 Blob: `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8`
- Verdict: **CONDITIONAL PASS** — local durable compiler pipeline is viable; publication/recovery blocked on Storage realization.
- Recommends modular Rust host, durable ingress, DB-backed outbox/worker and optional isolated inference worker; Kafka-class infra not justified absent throughput/multi-host evidence.
- Must preserve distinct Accepted, Registered, Staged, Dependency-Registered, Published, Canonical-Committed and Terminal evidence.
- Compiler outputs remain private until complete dependency set and D/Storage visibility protocol are proven.
- No implementation or executable integration/fault tests are claimed.

### F — Memory Runtime

- TAR-F report Blob: `124cc9300442b0e3a1e83603910e1c332b4fae48`
- Verdict: **CONDITIONAL PASS** for local-first modular Rust runtime.
- Recommends structured filtering + lexical retrieval first, optional ANN/reranking later; disposable per-session Working Sets; cache hits must revalidate current authorization and Forget state.
- Specifically recommends SQL structured filters + FTS5 first, Tantivy only if measured FTS5 limits; ANN only after retrieval benchmark.
- P1: typed CanonicalCommitCursor ↔ per-index IndexWatermark feed, D/E publication gate, search backend benchmark, authorization/completeness before candidate. Runtime/concurrency/rebuild/reconnect/ANN/security suites NOT RUN.

### G — Memory Context

- TAR-G report Blob: `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613`
- Verdict: **CONDITIONAL PASS** for Context architecture.
- G alone owns Context membership/order/budget, ContextVersion, ChangeSet, reconciliation and Delivery intent. Context Remove is not Canonical Forget; Delivered is not Applied.
- SQLite tables + transaction/outbox are first local prototype candidates; PostgreSQL is a scale-out alternative. Tokenizer/context-window budgets are unmeasured.
- P1: ContextVersion + ChangeSet + Delivery durable transaction; D/E publication gate; C/H/G/I Applied verifier; Forget snapshot/delta/reconnect invalidation. No runtime tests executed.

### H — BMCP Protocol

- TAR-H report Blob: `cb9d1d97604bdb71bc2f5bf47f6392e03f30ba99`
- Verdict: **CONDITIONAL PASS** for transport-independent protocol direction.
- JSON + RFC 8785 JCS is the first interoperability prototype candidate; HTTP(S) for remote/cross-language and Unix socket/Windows named pipe for local sidecar.
- CBOR/MessagePack/gRPC remain alternatives only if measured payload/streaming/SDK requirements justify.
- P1: authenticated Principal/Actor/Scope/PermissionEpoch mapping; G/C/H/I Applied binding; Forget ACK ↔ I inventory/D barrier mapping; transport/encoding interop and crypto/key lifecycle. No SDK, transport, crypto or fault tests executed.

### I — Security & Governance

- TAR-I-001 Blob: `c24f03aae6ce7bc76eaeb1ed33bb24fb7fcac624`
- Verdict: **CONDITIONAL PASS** for security architecture; **BLOCKED** for deployable security acceptance and Global Forget completion.
- PermissionEpoch is I-owned, opaque and PolicyDomain-scoped; protected irreversible operations require current I sequencer evidence; JF-10 accepted design profile is single-PolicyDomain only.
- Key custody, encryption-at-rest, audit integrity, IPC/mTLS and policy sequencer implementation are not selected.
- P0: global Forget target inventory/seal and JF-10 sequencer/receipt/prepared participant recovery not implemented/tested; P1: key lifecycle, audit, remote provider egress and restore quarantine.
- The TAR report addenda add logical reference-model evidence (25/25 then 30/30) but no real inventory service, external target deletion, production restore, signed receipt verification or physical erasure.

### Storage / Consistency

- Current branch HEAD: `17be31915b06d98d7f822e6e5270b8cde39eb0bb`
- No separate `reviews/technology/owner-storage-technology-review.md` or equivalent TAR-AI-001 report was found in the current branch tree.
- Current Storage serialization ADR Blob: `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`.
- The 2026-11-17 architecture-level addendum selects **Storage ADR Option A** as the normative v1 logical profile: one logical serializable transaction domain per Canonical Memory authority covering D admission/fence/dependency/publication-participant records and Storage hidden participant/final visibility/outcome/outbox records. D and Storage retain distinct semantic authority; I sequencer and COC quorum log remain independent.
- This is **not** the same naming scheme as this task's deployment topology Option A/B/C. It does not select SQLite/PostgreSQL or a deployed runtime.
- PostgreSQL 18.7 dossier Blob: `0aabf66848dc97deee028c571183c0d7204008c0`. Pinned CI capability subtests report PASS for prepared-XID persistence/lock retention/hard restart/same-XID resolution, synchronous standby promotion, physical backup/restore, coordinator ACK-gap crash, TCP ACK loss, standby-unavailable UNKNOWN/private and WAL PITR.
- Gate A remains PARTIAL PASS / OPEN; current amended Gate B revision requires focused exact-owner re-review; Gate C implementation/fault injection deferred; JF-10 runtime P0 OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.
- The Storage topology ADR's previous body says NO TOPOLOGY SELECTED, but its later addendum supersedes that only for the logical v1 serialization architecture. The physical DB/deployment/runtime remains L4 OPEN.

## 3. Cross-owner synthesis / 跨 Owner 综合

1. The strongest shared candidate is a Rust modular host with a relational transactional authority, DB outbox/workers, structured + lexical retrieval, optional isolated inference, and language-neutral Agent protocol.
2. The most important architecture constraint is not "which queue" but the exact shared serializable transaction domain for D/Storage admission/fence/dependency/final visibility. The current Storage ADR has a logical v1 profile, but its physical realization and JF-10 bridge remain unproven.
3. PostgreSQL 18.7 now has meaningful engine-level CI evidence for prepared transactions and recovery. This moves it ahead of SQLite for JF-10 capability qualification, but does not establish production deployment or D/I/COC application integration.
4. SQLite remains a lower-ops local prototype option for operations that fit its single-writer same-host transaction model. It is not evidence for external I sequencer prepared-XID recovery.
5. F's and G's owner-specific recommendations align on SQLite tables/outbox as local prototypes, but both defer final persistence and transaction decisions to Storage and measured workload.
6. Search recommendations align: structured SQL + FTS5 baseline; Tantivy if measured lexical limits; ANN/vector only after labeled retrieval evaluation.
7. H/C recommendations align: cross-language HTTP contract, Rust SDK and local sidecar/IPC prototype; Full Applied remains tied to real final-request runtime evidence.
8. B recommends typed relational semantics and immutable revisions; Fact/Claim identity remains a schema blocker.
9. I's identity/revocation/global Forget inventory and signed receipt trust remain critical security gates; Cedar or another policy engine cannot replace I authority.
10. Owner TAR verdicts are conditional and branch-currentness is stale; no report constitutes independent human approval or a system-wide technology selection.

## 4. Required follow-up / 后续要求

- Each B–I Owner must refresh its TAR review against the current branch HEAD above and pin all changed source Blobs.
- Storage must publish a TAR-style technology review or A must obtain an explicit Storage decision package covering the logical v1 profile, PostgreSQL 18.7 qualification, residual Gate A/B/C and L4 boundary.
- A must refresh the PR #44 exact evidence ledger because its branch pins are older than the current Owner branch heads listed here.
- The system-level technology recommendation must preserve PostgreSQL 18.7 as leading JF-10 capability candidate, SQLite as a limited local prototype alternative, and no production DB approval.
