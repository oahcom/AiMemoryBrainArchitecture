# ADR-RUN-001 — Durable Store and Transaction Boundaries
# ADR-RUN-001 — 持久化存储与事务边界

**Status / 状态:** PROPOSED — decision pending Owner, I/security and independent review / 提案中——待 Owner、I/安全及独立审查  
**Date / 日期:** 2026-11-17  
**Work item / 跟踪:** AI-RUN-003, Issue #30, PR #31  
**Decision owner / 决策责任:** A — runtime integration; I — security and governance constraints; pilot Owner — workload acceptance  
**Risk / 风险:** R2 for read-only pilot; R3 once autonomous GitHub writes or privileged operations are enabled  
**Supersedes / 替代:** None

---

## 1. Context / 背景

The event-driven Owner Worker Runtime needs durable state for webhook delivery intake, deduplication, normalized events, work eligibility, queueing, leases, fencing, run records, publication intents and recovery. A process-local queue or mutex cannot survive process restart and cannot coordinate multiple worker processes.

事件驱动 Owner Worker Runtime 需要持久化状态来承载 Webhook 接收、去重、规范化事件、工作资格、队列、租约、fencing、运行记录、发布意图和恢复。进程内 Queue 或 Mutex 无法跨进程重启，也无法协调多个 Worker 进程。

The store is not merely a queue backend. It is the serialization authority for work-item state transitions and lease generations. A storage choice that cannot atomically enforce these transitions is unacceptable, regardless of throughput.

存储层不只是 Queue 后端。它还是 Work Item 状态迁移和租约代际的序列化权威。无论吞吐量多高，不能原子强制这些迁移的存储方案都不可接受。

## 2. Decision drivers / 决策驱动因素

1. **Durable-before-ACK:** a webhook delivery is acknowledged only after its raw/normalized envelope and deduplication identity are durably committed.
2. **Atomic idempotency:** duplicate delivery detection and inbox insertion cannot split across independent commits.
3. **Atomic claim/lease:** selecting eligible work, assigning a lease and incrementing its fencing generation must be one serializable state transition.
4. **Fencing at side-effect boundary:** stale workers cannot publish. The publication broker must validate current lease/fencing state immediately before accepting a mutation.
5. **Recoverable transitions:** queue state, run ledger and publication intent must support crash recovery without inventing exactly-once external side effects.
6. **Auditable history:** important state transitions are append-recorded with actor, time, prior/new state and correlation IDs.
7. **Single-host pilot first:** the current deployment target is one user-managed Ubuntu host; multi-node availability is a future requirement, not an assumed current capability.
8. **Backup/restore correctness:** backups must be consistent and restore tests must include inbox, dedup keys, lease generations and run ledger.
9. **Operational simplicity:** the pilot must be supportable by a small project without hiding correctness problems behind distributed infrastructure.
10. **Security:** secrets are not stored in plaintext application rows; database access is limited to dedicated service identities and filesystem/network policy.

## 3. Non-goals / 非目标

- This ADR does not select the GitHub App permission model or secret manager (ADR-RUN-002).
- This ADR does not select worker sandboxing/isolation (ADR-RUN-003).
- This ADR does not promise exactly-once delivery or exactly-once GitHub side effects.
- This ADR does not authorize autonomous merges, releases, destructive operations or production data changes.
- This ADR does not claim any database has been deployed, benchmarked or recovery-tested.

## 4. Required logical records / 必需逻辑记录

The logical schema is independent of the selected engine. Physical table names and indexes are implementation details.

逻辑 Schema 与具体数据库引擎无关。物理表名和索引属于实现细节。

| Record / 记录 | Minimum responsibility / 最低职责 |
|---|---|
| `event_inbox` | Delivery ID, repository ID, event type, payload digest, received time, verification result, processing state |
| `delivery_dedup` | Unique `(repository_id, delivery_id)` identity and durable first-seen result |
| `normalized_event` | Validated event facts and source inbox reference; raw payload retention is separately bounded |
| `work_item` | Semantic work identity, eligibility, state, target revision and supersession |
| `work_queue` | Durable scheduling/availability state; may be a view/index over work_item if atomicity is preserved |
| `lease` | Work item, worker instance, expiry, monotonically increasing fencing token and lease status |
| `run_ledger` | Append-oriented execution lifecycle and evidence references |
| `publication_intent` | Proposed GitHub mutation, expected base/head, allowed paths, idempotency key and publication state |
| `audit_event` | Actor, action, target, previous/new state, timestamp, correlation and causation IDs |
| `schema_migration` | Ordered schema version and migration integrity metadata |

Do not store webhook secrets, GitHub installation tokens, model-provider keys or SSH credentials in these records. Payload retention must be minimized; persist a digest and only the data needed for authorized processing.

不得在这些记录中保存 Webhook Secret、GitHub Installation Token、模型 Provider Key 或 SSH 凭据。Payload 保留应最小化；持久化摘要以及授权处理所需的数据即可。

## 5. Mandatory transaction boundaries / 强制事务边界

### TX-01 — Receive and deduplicate / 接收与去重

One database transaction must:
1. insert the unique delivery identity;
2. insert the verified inbox envelope (or a durable reference plus digest);
3. record the initial processing state.

If the unique key already exists, return the previously recorded receipt/result without creating a second logical event. Return HTTP success only after commit. If commit outcome is unknown due to connection loss, do not guess: retry using the same delivery identity and resolve through the unique constraint.

一个数据库事务必须完成：插入唯一 Delivery Identity、写入已验证 Inbox Envelope（或持久化引用及摘要）、记录初始处理状态。唯一键已存在时返回原有 Receipt/Result，不创建第二个逻辑事件。只有 Commit 成功后才返回 HTTP 成功。若连接中断导致 Commit 结果未知，不得猜测；使用相同 Delivery Identity 重试并由唯一约束消歧。

### TX-02 — Normalize and enqueue / 规范化与入队

A transaction must persist the normalized event, derive or upsert semantic work identity, and make eligible work visible to the scheduler together. Reprocessing the same delivery or semantic trigger must not create duplicate active work. Superseding a target revision must atomically mark older queued work as superseded where policy requires.

一个事务必须同时持久化规范化事件、派生或 Upsert Semantic Work Identity，并使符合条件的工作对 Scheduler 可见。重复处理同一 Delivery 或 Semantic Trigger 不得产生重复的活跃工作。目标 Revision 被更新时，必须按策略原子地将旧排队工作标记为 Superseded。

### TX-03 — Claim and lease / 认领与租约

A transaction must:
1. select one eligible item using a concurrency-safe claim strategy;
2. verify its state and target revision;
3. assign the worker identity and lease expiry;
4. increment the per-work-item monotonic fencing token;
5. append the lease-acquired audit/run event.

The transaction must ensure that two workers cannot both acquire the same current lease generation. Lease time comparisons must use one authoritative clock source (prefer database time); clock assumptions and maximum skew must be documented. A process-local lock is not sufficient.

一个事务必须完成：并发安全地选择可执行工作、校验状态和目标 Revision、分配 Worker Identity 与租约过期时间、递增 Work Item 级单调 fencing token、追加租约获取审计/运行事件。必须确保两个 Worker 不会同时获得同一当前租约代际。租约时间比较必须使用单一权威时钟源（优先数据库时间），并记录时钟假设和最大偏差。进程内锁不够。

### TX-04 — Heartbeat and expiry / 心跳与过期

Heartbeat must conditionally extend the lease only when work item, worker identity, lease ID and fencing token all match the current lease and the lease has not already expired. A stale worker cannot revive an expired generation. Reclaiming expired work creates a new fencing token; it never reuses the previous token.

只有 Work Item、Worker Identity、Lease ID 和 fencing token 全部匹配当前租约且租约尚未过期时，Heartbeat 才能条件性延长租约。旧 Worker 不能复活已过期代际。重新认领过期工作必须创建新的 fencing token，不得复用旧 Token。

### TX-05 — Run outcome and publication intent / 运行结果与发布意图

The worker's result, evidence references and publication intent must be durably staged before the run is considered ready for publication. The publication broker performs a fresh atomic validation against current work state and lease generation before accepting each side effect. Database transaction commit and GitHub API mutation cannot be one distributed atomic transaction; use an outbox/reconciliation protocol with an idempotency key and explicit uncertain outcome state.

Worker 结果、证据引用和 Publication Intent 必须先持久化暂存，Run 才能进入待发布状态。Publication Broker 在接受每个副作用前，必须针对当前 Work State 和租约代际重新执行原子校验。数据库 Commit 与 GitHub API 变更无法构成一个分布式原子事务；必须使用 Outbox/Reconciliation 协议、幂等键和明确的结果不确定状态。

### TX-06 — Audit / 审计

Every security-relevant state transition must commit with its audit event. Audit history is append-oriented; corrections are additional events, not silent mutation of prior evidence. Tamper-evidence, export and retention requirements remain subject to I/security review.

每个安全相关状态迁移必须与审计事件一同 Commit。审计历史采用追加方式；纠正通过新增事件完成，不得静默修改既有证据。防篡改、导出和保留要求仍需 I/安全审查。

## 6. Delivery semantics / 投递语义

The system provides **at-least-once event processing with idempotent state transitions**, not exactly-once execution.

系统提供**至少一次事件处理 + 幂等状态迁移**，不承诺 Exactly-once 执行。

- GitHub delivery identity: `(repository_id, delivery_id)`.
- Semantic work identity: stable key derived from repository, subject (Issue/PR), target revision, work class and approved prompt digest.
- External side effects use broker-issued idempotency keys where the target API supports them; otherwise the broker must reconcile observed remote state before retry.
- A timeout after sending a GitHub request is an **unknown outcome**, not a failure. Read remote state before repeating the mutation.
- Exactly-once cannot be claimed across the database and GitHub API without a shared transaction protocol, which is not available here.

- GitHub Delivery Identity：`(repository_id, delivery_id)`。
- Semantic Work Identity：由 Repository、Subject（Issue/PR）、目标 Revision、Work Class 和批准的 Prompt Digest 稳定派生。
- 外部副作用使用 Broker 发放的幂等键；若目标 API 不支持，则重试前必须对账远端状态。
- GitHub 请求发送后超时属于**结果未知**，不等于失败。重复变更前先读取远端状态。
- 数据库与 GitHub API 不共享事务协议，因此不得声称跨二者 Exactly-once。

## 7. Candidate options / 候选方案

### Option A — SQLite with WAL / SQLite + WAL

**Advantages / 优点**
- Small operational footprint for one Ubuntu host.
- Local transactional database; no separate database service to operate.
- Suitable candidate for a single-node, low-to-moderate concurrency pilot if transaction and locking tests pass.

**Risks / 风险**
- Single-host durability and availability boundary; host/disk loss remains an outage.
- Write contention and long-running readers can affect WAL checkpointing and latency.
- WAL mode is not a substitute for backup design; copying only the main database file while active can produce an inconsistent backup.
- Network filesystems and shared multi-host access are not acceptable assumptions.
- Concurrency limits and busy/retry behavior must be measured under the real workload.

### Option B — PostgreSQL

**Advantages / 优点**
- Strong multi-process transaction/concurrency behavior and explicit row-level locking primitives.
- Better path toward multiple worker processes or future multi-host operation.
- Mature backup, replication and operational tooling.

**Risks / 风险**
- Additional service lifecycle, credentials, patching, monitoring and backup/restore burden.
- A single PostgreSQL instance on the same Ubuntu host does not itself provide host-level high availability.
- Requires explicit schema, connection pool, migration and operational ownership.

### Option C — Other / 其他

Any alternative (e.g. a managed database) must satisfy the same transaction, fencing, audit, backup, restore, security and availability requirements. It cannot be selected solely to reduce implementation effort.

任何其他方案（例如托管数据库）都必须满足相同的事务、Fencing、审计、备份、恢复、安全和可用性要求。不得仅为减少实现工作量而选型。

## 8. Provisional recommendation / 暂定建议

**No final technology decision is made by this ADR.**

If the first pilot is strictly one host, one trusted service boundary, low/moderate concurrency and no multi-host failover, SQLite WAL is the simplest candidate to benchmark first. This is a conditional pilot hypothesis, not an approval to deploy.

If the acceptance workload requires sustained concurrent claims/writes beyond measured SQLite limits, multiple hosts, database-level role separation, or independent database service lifecycle, evaluate PostgreSQL before implementation freeze.

**本 ADR 不作最终技术决策。**

如果首个试点严格限定为单主机、单可信服务边界、低/中等并发且不要求多主机故障切换，则可优先基准测试 SQLite WAL。这只是有条件的试点假设，不是部署批准。

如果验收负载要求持续并发认领/写入超出 SQLite 实测能力、多主机运行、数据库级角色隔离或独立数据库服务生命周期，则应在实现冻结前评估 PostgreSQL。

## 9. Required benchmark and fault tests / 必需基准与故障测试

No technology can be accepted from a synthetic throughput number alone. Run the same workload and crash matrix against each viable candidate.

不能仅凭一个合成吞吐数字接受某种技术。每个候选方案必须运行相同工作负载和崩溃矩阵。

| Test ID | Scenario / 场景 | Required observation / 必须观察 |
|---|---|---|
| DB-01 | 1, 5, 20 concurrent event writers | p50/p95/p99 commit latency, busy/lock errors, loss/duplication |
| DB-02 | 1, 5, 20 concurrent claimers | No double lease; fencing tokens strictly increase |
| DB-03 | Burst duplicate deliveries | One durable logical delivery; stable receipt |
| DB-04 | Crash before inbox commit | No 2xx; sender retry succeeds |
| DB-05 | Crash after commit before HTTP ACK | Retry deduplicates to prior receipt |
| DB-06 | Crash during claim transaction | Either no lease or one complete lease; no partial state |
| DB-07 | Lease expiry and stale worker resume | Old fencing token rejected at publication broker |
| DB-08 | Disk full / database unavailable | Fail closed; no success ACK or false completion |
| DB-09 | Process kill during WAL/checkpoint or DB write | Recovery integrity and bounded recovery time |
| DB-10 | Backup during active writes, then restore | Consistent restore of inbox, dedup, lease generations and ledger |
| DB-11 | Schema migration interrupted | Safe restart/rollback procedure; no silent partial migration |
| DB-12 | Long-running reader plus write burst | Checkpoint/lock behavior and tail latency |
| DB-13 | Outbox send timeout with remote mutation possibly accepted | Reconciliation avoids duplicate side effect |
| DB-14 | Audit export and integrity check | Complete ordered history and tamper-evidence strategy |

Record hardware/OS/filesystem, database version/configuration, dataset size, workload generator, concurrency, duration, resource consumption, raw results and exact commit SHA. Define numeric SLOs before running the benchmark; do not invent thresholds after seeing results.

记录硬件/OS/文件系统、数据库版本与配置、数据集大小、负载生成器、并发数、持续时间、资源消耗、原始结果和精确 Commit SHA。必须在运行基准前定义数值 SLO；不得看到结果后再倒推阈值。

## 10. Backup, restore and retention / 备份、恢复与保留

- Define RPO/RTO with the project sponsor before production-like use.
- Backups must be encrypted, access-controlled and separate from the host's primary failure domain where practical.
- A backup is not accepted until restore has been tested on an isolated environment.
- Restore must preserve delivery deduplication keys and fencing generations; otherwise stale deliveries or stale workers may be re-admitted.
- Retention/deletion must respect security, privacy and legal policy; webhook raw payloads should have shorter retention than minimal audit metadata where feasible.
- Backup copies and audit exports are security-relevant targets and must be included in access control and deletion governance.

- 类生产使用前由项目 Sponsor 定义 RPO/RTO。
- 备份必须加密、访问受控，并尽可能与主机主要故障域分离。
- 未在隔离环境完成恢复测试的备份不算验收通过。
- 恢复必须保留 Delivery Deduplication Key 和 Fencing Generation，否则旧 Delivery 或旧 Worker 可能重新获得资格。
- 保留/删除必须遵守安全、隐私和法律政策；可行时 Webhook 原始 Payload 的保留期应短于最小化审计元数据。
- 备份副本和审计导出属于安全相关目标，必须纳入访问控制和删除治理。

## 11. Acceptance gates / 验收 Gate

This ADR may move from PROPOSED to ACCEPTED only when all applicable items are evidenced:

1. A publishes workload profile and numeric SLOs (arrival rate, burst, concurrency, retention, RPO/RTO).
2. I reviews data classification, encryption, access control, audit integrity, backup and deletion implications.
3. Pilot Owner confirms operational constraints and recovery expectations.
4. DB-01 through DB-14 are executed for the selected candidate; failures and raw evidence are retained.
5. Transaction boundary tests prove TX-01 through TX-06.
6. A separate implementation PR includes schema migrations, constraints/indexes, crash recovery and integration tests.
7. Independent reviewer reviews both ADR and implementation; A does not self-approve.
8. Governance explicitly approves any R3 transition before autonomous write capability is enabled.

本 ADR 只有在以下适用项目均有证据后才能从 PROPOSED 转为 ACCEPTED：

1. A 发布工作负载画像和数值 SLO（到达速率、突发、并发、保留期、RPO/RTO）。
2. I 审查数据分类、加密、访问控制、审计完整性、备份和删除影响。
3. 试点 Owner 确认运维约束和恢复预期。
4. 对选定候选执行 DB-01 至 DB-14，保留失败结果和原始证据。
5. 事务边界测试证明 TX-01 至 TX-06。
6. 单独实现 PR 包含 Schema Migration、约束/索引、崩溃恢复和集成测试。
7. 独立审查者同时审查 ADR 和实现；A 不得自我批准。
8. 启用自主写能力前，治理权威必须明确批准任何 R3 转换。

## 12. Open questions / 待决问题

- What are the expected webhook event rates and burst sizes?
- What is the maximum number of concurrent Owner runs on the pilot host?
- Is the first pilot strictly single-host, or is multi-host failover a near-term requirement?
- What are the approved RPO/RTO and backup retention requirements?
- Which audit events must be tamper-evident and independently exported?
- What data retention/deletion rules apply to webhook payloads and run artifacts?
- What numeric p95/p99 commit and claim latency SLOs are required?

- 预期 Webhook 事件速率和突发规模是多少？
- 试点主机允许的 Owner Run 最大并发数是多少？
- 首个试点是否严格单机，还是近期就需要多机故障切换？
- 批准的 RPO/RTO 和备份保留要求是什么？
- 哪些审计事件必须防篡改并独立导出？
- Webhook Payload 和 Run Artifact 适用什么数据保留/删除规则？
- Commit 和 Claim 的 p95/p99 延迟 SLO 要求是多少？

## 13. Decision record / 决策记录

| Field / 字段 | Value / 值 |
|---|---|
| Decision | OPEN — no database selected / 未决——未选择数据库 |
| SQLite WAL | Candidate; benchmark required / 候选；必须基准测试 |
| PostgreSQL | Candidate; benchmark required / 候选；必须基准测试 |
| Implementation | NOT STARTED / 未开始 |
| Deployment | NOT DEPLOYED / 未部署 |
| Fault tests | NOT RUN / 未运行 |
| Independent review | PENDING / 待审查 |
| Governance approval | PENDING / 待治理批准 |

A file in the repository is not an approval. A benchmark plan is not benchmark evidence. A passing unit test is not proof of crash recovery or production readiness.

仓库中存在文件不代表决议已批准。基准测试计划不等于基准证据。单元测试通过不等于崩溃恢复或生产就绪证明。
