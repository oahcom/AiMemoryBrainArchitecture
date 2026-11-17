# AI-RUN-003 Runtime Data Model and Migration Contract
# AI-RUN-003 Runtime 数据模型与迁移契约

- **Status / 状态:** PROPOSED — storage-neutral logical schema / 提案中——存储无关逻辑 Schema
- **Risk / 风险:** R2 read-only pilot; R3 publication or privileged operations
- **Owners / 责任:** A runtime integration; Storage/Consistency; I security; Testing/Quality
- **Related / 关联:** Issue #30; ADR-RUN-001 through ADR-RUN-006

## 1. Scope / 范围

This document defines the logical records and consistency invariants required by AI-RUN-003. It is intentionally storage-neutral. It does not select SQLite/PostgreSQL, define a production migration, or authorize deployment. Physical schema and migration scripts must be derived only after ADR-RUN-001 is approved and benchmarked.

本文定义 AI-RUN-003 所需逻辑记录和一致性不变量，刻意保持存储无关。不选择 SQLite/PostgreSQL，不定义生产迁移，也不授权部署。物理 Schema 和 Migration 脚本必须在 ADR-RUN-001 批准并完成基准测试后生成。

## 2. Logical entities / 逻辑实体

| Entity | Primary identity | Purpose / 用途 |
|---|---|---|
| `event_inbox` | `(repository_id, delivery_id)` | Durable accepted webhook envelope |
| `delivery_dedup` | `(repository_id, delivery_id)` | Unique delivery identity/retention state |
| `normalized_event` | `event_id` | Parsed, validated event metadata |
| `work_item` | `work_item_id` + unique `work_key` | Semantic work target and state |
| `work_dependency` | `(work_item_id, dependency_id)` | Durable dependency graph edge |
| `work_queue` | `queue_entry_id` | Scheduling order, priority and availability |
| `lease` | `lease_id` | Current/previous worker claim and fencing |
| `run_ledger` | `run_id` | Immutable execution-attempt evidence |
| `authorization` | `authorization_id` | Prompt/Owner/policy capability binding |
| `publication_intent` | `publication_idempotency_key` | Durable external side-effect intent |
| `audit_event` | `audit_event_id` | Append-oriented security/governance trail |
| `schema_migration` | `migration_id` | Applied migration identity and checksum |
| `runtime_policy` | `policy_epoch` | Versioned allowlists, budgets and routing policy |

## 3. Common field rules / 通用字段规则

- All identifiers are opaque, stable and non-secret.
- Repository identity uses immutable GitHub repository ID; full name is stored as descriptive metadata and revalidated.
- Timestamps are UTC with explicit precision; ordering must not depend solely on wall-clock timestamps.
- Every mutable aggregate has a monotonic revision/version.
- Every state transition records actor/service identity, reason code, correlation ID and creation time.
- JSON payload fields are schema-versioned and size-bounded; raw webhook bodies are not copied into ordinary logs.
- Secrets, installation tokens, PATs, private keys, SSH material and model credentials are prohibited in every record.
- Retention and deletion policies are explicit per entity; audit records may have different retention from transient payloads.

所有 ID 不透明、稳定且非秘密；仓库身份使用不可变 GitHub Repository ID；时间为 UTC；排序不能仅依赖墙钟；可变 Aggregate 有单调版本；状态转换记录 Actor/Reason/Correlation；JSON Payload 有 Schema Version/大小限制；禁止所有秘密入库；不同实体分别定义保留/删除策略。

## 4. Entity contracts / 实体契约

### 4.1 event_inbox

Required fields:
- `repository_id`
- `delivery_id`
- `event_type`, `action`
- `received_at`
- `payload_digest`
- `payload_ref` (optional protected storage reference; never inline secret-bearing raw body)
- `signature_key_version`
- `verification_state` (VERIFIED / REJECTED)
- `processing_state` (RECEIVED / NORMALIZED / IGNORED / FAILED / DEAD_LETTER)
- `attempt_count`, `last_error_code`
- `schema_version`

Uniqueness: `(repository_id, delivery_id)`. Only VERIFIED records enter the processing queue. Inbox row and dedup identity commit atomically before 2xx response.

唯一键为 `(repository_id, delivery_id)`。只有 VERIFIED 记录进入处理队列。Inbox 与 Dedup 必须在返回 2xx 前原子提交。

### 4.2 normalized_event

Required fields:
- `event_id`, `repository_id`, `delivery_id`
- `event_type`, `action`, `subject_type`, `subject_id`
- `source_revision`, `source_updated_at`
- `payload_digest`, `normalizer_version`
- `normalized_at`, `schema_version`

This is a derived record. It may be regenerated from a retained verified envelope; it never grants authorization.

该记录为派生物，可从保留的已验签 Envelope 重建，不构成授权。

### 4.3 work_item

Required fields:
- `work_item_id`
- `repository_id`
- `subject_type`, `subject_id`
- `target_revision`
- `work_class`
- `prompt_id`, `prompt_digest`
- `policy_epoch`
- `work_key` (unique canonical semantic identity)
- `state`
- `priority`, `not_before`
- `created_at`, `updated_at`
- `aggregate_revision`
- `supersedes_work_item_id` (nullable)
- `blocked_reason_code`, `last_error_code`

Work key encoding must be versioned and unambiguous as specified by ADR-RUN-004. State transitions are compare-and-set against aggregate revision.

Work Key 编码按 ADR-RUN-004 版本化且无歧义。状态转换必须对 Aggregate Revision 执行 CAS。

### 4.4 work_dependency

Fields:
- `work_item_id`
- `dependency_id`
- `required_state`
- `required_revision`
- `evidence_ref`
- `dependency_type`
- `created_at`

A dependency is satisfied only by evidence matching the required revision and state. Cycles are rejected at graph admission; cycle detection is required.

依赖只有在证据匹配要求的修订和状态时才满足。图准入时拒绝循环，必须执行 Cycle Detection。

### 4.5 work_queue

Fields:
- `queue_entry_id`, `work_item_id`
- `queue_name`, `priority`, `available_at`
- `enqueued_at`, `dequeued_at`
- `attempt_count`, `queue_state`

Queue visibility must be transactionally consistent with work-item eligibility. A queued item must not be claimable if blocked, superseded, cancelled or expired.

队列可见性必须与 Work Item 资格事务一致。Blocked、Superseded、Cancelled、Expired 项不得被 Claim。

### 4.6 lease

Fields:
- `lease_id`, `work_item_id`, `worker_id`
- `fencing_token` (monotonically increasing per work item)
- `issued_at`, `expires_at`, `last_heartbeat_at`
- `lease_state` (ACTIVE / EXPIRED / RELEASED / REVOKED)
- `claim_revision`

Only one ACTIVE lease per work item. Claim and fencing-token increment are atomic. Heartbeat succeeds only for the exact active lease ID, worker ID and fencing token before expiry. Expired leases cannot be revived.

每个 Work Item 同时最多一个 ACTIVE Lease。Claim 和 fencing token 递增必须原子化。Heartbeat 仅对未过期且 Lease ID/Worker ID/Fencing Token 全匹配的租约成功。过期租约不可复活。

### 4.7 run_ledger

Fields:
- `run_id`, `work_item_id`, `worker_id`
- `lease_id`, `fencing_token`
- `authorization_id`, `prompt_digest`
- `base_sha`, `target_revision`, `branch_ref`
- `started_at`, `finished_at`
- `run_state`, `exit_reason`, `error_class`
- `actions_summary`, `files_changed`
- `tests_invoked`, `tests_passed`, `tests_failed`
- `evidence_refs`
- `resource_usage`, `budget_limit`
- `created_at`

Run records are append-oriented; corrections create linked evidence events rather than silently rewriting accepted history.

Run 记录采用追加式；更正通过关联证据事件完成，不静默重写已接受历史。

### 4.8 authorization

Fields:
- `authorization_id`, `work_item_id`, `run_id`
- `repository_id`, `owner_id`, `risk_class`
- `prompt_digest`, `base_sha`, `policy_epoch`
- `allowed_paths_ref`, `allowed_commands_ref`, `network_policy_ref`
- `resource_budget_ref`
- `approval_refs`
- `issued_at`, `expires_at`, `revoked_at`
- `authorization_state`

The capability is audience-bound to one run and cannot be broadened by the worker. Secret bearer values are not stored in the database.

Capability 绑定单一 Run，Worker 不得扩大范围。数据库不存储秘密 Bearer Value。

### 4.9 publication_intent

Fields:
- `publication_idempotency_key` (unique)
- `work_item_id`, `run_id`, `authorization_id`
- `lease_id`, `fencing_token`
- `mutation_type`, `target_ref`, `expected_base_sha`
- `request_digest`, `state`
- `created_at`, `submitted_at`, `confirmed_at`
- `remote_object_id`, `reconciliation_result`

States: PREPARED / SUBMITTED / CONFIRMED / UNKNOWN / FAILED / RECONCILE_REQUIRED / CANCELLED. Never assume local commit and GitHub mutation are one atomic transaction.

状态如上；不得假定本地 Commit 和 GitHub 变更构成一个原子事务。

### 4.10 audit_event

Fields:
- `audit_event_id`, `occurred_at`
- `actor_type`, `actor_id`
- `action`, `object_type`, `object_id`
- `decision`, `reason_code`
- `correlation_id`, `causation_id`
- `policy_version`, `evidence_ref`
- `previous_event_digest`, `event_digest` (if tamper-evident chaining is adopted)

Append-only by application policy. Tamper-evident cryptographic chaining is an open decision and must not be claimed until key management and export verification are designed.

应用策略上只追加。防篡改密码学链仍是开放决策，在密钥管理和导出验证设计完成前不得声称具备。

## 5. State and transaction boundaries / 状态与事务边界

| Transaction | Atomic logical writes | Invariant |
|---|---|---|
| TX-01 Receive/Deduplicate | inbox + delivery_dedup + initial audit | Commit before 2xx |
| TX-02 Normalize/Enqueue | normalized_event + work_item/work_key + queue + audit | No eligible item without queue visibility; no duplicate semantic key |
| TX-03 Claim/Lease | queue claim + lease + fencing increment + run start + audit | Single active lease; monotonic fencing |
| TX-04 Heartbeat/Expire | lease conditional update + audit | Exact lease/fence match; no revival after expiry |
| TX-05 Stage publication | run evidence + publication_intent + audit | Durable intent before remote side effect |
| TX-06 Confirm publication | publication state + remote reference + audit | Reconcile ambiguous outcome before retry |
| TX-07 Revoke authorization | authorization revoke + queued work invalidation + cancellation intent + audit | No new run after revocation |
| TX-08 Supersede work | old work state + queue invalidation + new work/queue + audit | Old revision cannot publish |

Transactions TX-01..TX-06 align with ADR-RUN-001. TX-07/TX-08 are additional logical boundaries requiring Storage/Consistency review and fault tests.

TX-01..TX-06 与 ADR-RUN-001 对齐。TX-07/TX-08 是新增逻辑边界，需 Storage/Consistency 审查和故障测试。

## 6. Ordering and concurrency / 顺序与并发

- Database transaction commit order is authoritative for local state.
- Wall-clock timestamps are observability metadata, not concurrency control.
- Use compare-and-set on aggregate revisions and lease/fencing tuples.
- Never hold a database transaction open while calling GitHub or an LLM.
- Remote API calls use durable outbox/publication intent and reconciliation.
- Queue workers must use bounded claim batches and backpressure.
- Every state transition is idempotent under retry.

本地状态以数据库事务提交顺序为准；墙钟仅用于观测；使用 Aggregate Revision/Lease/Fencing CAS；调用 GitHub/LLM 时不持有数据库事务；远程调用通过 Outbox/Publication Intent 和对账；Claim 批次有界并实施背压；状态转换可幂等重试。

## 7. Retention and privacy / 保留与隐私

- Webhook payload retention is minimized; retain digest and required normalized metadata longer than raw body.
- Dedup records outlive the maximum GitHub retry/replay window plus operational safety margin.
- Run evidence retention is governed by AI development policy and may include code diffs, test logs and summaries; redact secrets and unnecessary personal data.
- Deletion of transient payloads must not erase audit evidence needed to explain authorization and publication decisions.
- Backups must be encrypted, access-controlled, tested and included in retention/deletion policy.
- No secrets or private keys are stored in these tables.

Webhook Payload 最小化保留；Dedup 超过最大重试/重放窗口和安全余量；Run Evidence 按治理策略保留并脱敏；删除临时 Payload 不得抹去解释授权/发布决策所需审计；备份加密控权并纳入删除策略；表中不存秘密。

## 8. Migration contract / Migration 契约

- Migrations are immutable, ordered and checksum-verified.
- Each migration has ID, version, checksum, author, review reference and compatibility statement.
- Apply migrations under an exclusive migration lease/lock.
- A migration must be restartable or have an explicit recovery procedure.
- Back up before destructive/rewriting migration; verify restore path before production rollout.
- Expand/contract changes: add compatible fields/tables, dual-read/write only when specified, backfill with checkpoints, then remove old fields in a later approved migration.
- Never auto-run an unreviewed migration at service startup.
- Migration identity and outcome are recorded in `schema_migration`.

Migration 不可变、有序、校验和验证；记录 ID/版本/Checksum/作者/审查/兼容性；使用独占锁；可重启或有恢复流程；破坏性迁移前备份并验证恢复；使用 Expand/Contract；服务启动不自动执行未审查迁移；记录迁移结果。

## 9. Open physical-design questions / 物理设计待决

1. SQLite WAL vs PostgreSQL decision under ADR-RUN-001 benchmark.
2. Exact isolation level and supported CAS/locking semantics.
3. Payload storage: database BLOB vs protected filesystem/object store reference.
4. Audit tamper-evidence, export and signing-key lifecycle.
5. Retention periods and deletion obligations.
6. Maximum concurrent claimers/workers and queue partitioning.
7. Backup RPO/RTO and restore drills.
8. Schema migration tooling and rollback strategy.

## 10. Acceptance tests / 验收测试

- RM-01 unique delivery constraint under concurrent duplicate inserts.
- RM-02 semantic work-key uniqueness under concurrent event normalization.
- RM-03 transaction crash before/after commit boundaries.
- RM-04 single active lease under concurrent claimers.
- RM-05 monotonic fencing token across expiry/reclaim/restart.
- RM-06 expired heartbeat cannot revive lease.
- RM-07 stale worker cannot stage/publish after reassignment.
- RM-08 authorization revocation invalidates queued work.
- RM-09 superseded revision cannot be claimed or published.
- RM-10 ambiguous GitHub API outcome reconciles before retry.
- RM-11 migration interrupted mid-flight recovers safely.
- RM-12 backup restore preserves queue/lease/run/audit consistency.
- RM-13 retention cleanup cannot remove required audit references.
- RM-14 secret canary scan finds no secret values in DB/export/log.
- RM-15 concurrent load meets the approved latency/throughput targets.

## 11. Decision / 决议

**OPEN — logical model only.** Storage/Consistency must reconcile this model with ADR-RUN-001, propose physical schemas for the selected database, and publish migration/test evidence. No production database, migration or runtime implementation is claimed.

**OPEN——仅逻辑模型。** Storage/Consistency 必须将本模型与 ADR-RUN-001 对齐，为最终选定数据库提出物理 Schema，并提交迁移/测试证据。本文件不声称已部署生产数据库、迁移或 Runtime 实现。
