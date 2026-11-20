# Continuous Owner Runtime Architecture
# Owner 不间断运行架构

**Document ID:** AI-RUN-001  
**Version:** 1.0  
**Status:** PROPOSED  
**Parent:** AI-AUTO-001 / AI-PROMPT-STD-001

## 1. Objective / 目标

The operating objective is continuous project progress by A–I Owners, not a model process that must remain continuously generating tokens.

目标是 A–I 九个 Owner 的工作系统持续运转，而不是要求模型进程 24 小时持续生成 Token。The system MUST resume work promptly when GitHub state changes, recover from worker interruption, and keep making bounded progress while eligible work exists.

## 2. Capability truth / 能力边界

A recurring ChatGPT scheduled task is a periodic trigger, not an always-on daemon. The currently available scheduled-task cadence supports daily or less frequent recurrence, not sub-daily polling or guaranteed continuous execution. It MUST NOT be represented as 24/7 operation.

True event-driven continuous operation requires an always-available external execution service or equivalent supported runtime with:
- GitHub App/webhook delivery for Issues, PRs, reviews, pushes, check runs and workflow events;
- durable queue/event log;
- A–I worker processes or isolated execution contexts;
- controlled LLM invocation and model/provider credentials;
- GitHub App installation permissions with least privilege;
- branch/worktree isolation and reproducible build/test environment;
- durable run ledger, idempotency keys, leases and heartbeats;
- watchdog, retry, dead-letter handling, backpressure and operator escalation.

If such infrastructure is not connected and verified, report the system as NOT DEPLOYED. Do not claim always-on execution.

## 3. Logical topology / 逻辑拓扑

```text
GitHub Events
  ├─ Issue opened/edited/assigned/labeled
  ├─ PR opened/synchronized/review submitted
  ├─ Review comment / requested changes
  ├─ Commit pushed / CI check completed
  └─ Dependency or release state changed
          |
          v
Webhook Receiver + Signature Verification
          |
          v
Durable Event Inbox / Queue  <---- Periodic Reconciliation Watchdog
          |
          v
A Coordinator / Work Router
          |
          +--> Owner B Worker + B prompt
          +--> Owner C Worker + C prompt
          +--> Owner D Worker + D prompt
          +--> Owner E Worker + E prompt
          +--> Owner F Worker + F prompt
          +--> Owner G Worker + G prompt
          +--> Owner H Worker + H prompt
          +--> Owner I Worker + I prompt
          |
          v
Isolated Branch / Worktree + Tests + Evidence
          |
          v
GitHub Commit / PR / Review / Issue Update
          |
          v
A Integration & Authorized Acceptance Gates
```

This is a logical topology. It is not evidence that these services or workers currently exist.

## 4. Owner worker model / Owner Worker 模型

There is one logical worker identity per Owner domain, A through I. A logical worker may be implemented as a long-running process, a queue consumer or a managed task runner. It need not hold an LLM session open between tasks.

Each worker has:
- immutable Owner key and domain authority;
- approved system/task prompt version and SHA-256;
- event subscription filters;
- Work Item selection and priority policy;
- bounded concurrency and per-branch write lease;
- tool/capability allowlist;
- run budget and timeout;
- output/evidence schema;
- escalation policy.

A owns portfolio routing and prompt drafting, not other Owners' domain decisions. Every Owner signs off its own domain-specific prompt constraints and acceptance criteria. A cannot self-authorize A-owned implementation.

## 5. Event-driven loop / 事件驱动循环

1. Receive GitHub event and verify webhook signature, delivery ID and repository installation.
2. Persist event to durable inbox before acknowledging receipt.
3. Deduplicate by provider delivery ID and event semantic key.
4. Resolve linked Work Item, Owner, prompt version, branch and dependency graph.
5. Check current Issue/PR state and authoritative source SHAs; webhook payload is a wake-up hint, not the complete truth.
6. Acquire Work Item/branch lease and re-check permissions.
7. Dispatch one bounded unit to the responsible Owner worker.
8. Execute inspect → plan → change → test → evidence → commit/PR/comment.
9. Release lease and persist run outcome.
10. New GitHub events or watchdog reconciliation trigger the next unit.

The system SHOULD be event-driven for low latency and use a configurable periodic reconciliation loop to recover missed webhooks, stale leases and abandoned work. The watchdog is a recovery mechanism, not the primary work trigger.

## 6. Continuous operation invariants / 持续运行不变量

- **Durable before ACK:** event receipt is persisted before webhook success response.
- **At-least-once delivery:** assume events may duplicate or arrive out of order; consumers must be idempotent.
- **No exactly-once assumption:** use deduplication, idempotency keys and state reconciliation.
- **Lease fencing:** expired workers cannot publish after a newer lease/fence has been issued.
- **Single writer per work scope:** one active writer per Owner + Work Item + branch unless explicitly partitioned.
- **Fresh state:** re-read current GitHub head and approvals before every mutation.
- **Fail closed:** missing permission, stale prompt, conflicting decision, unknown branch or failed safety check stops the run.
- **Human/governance gates:** no automation bypasses domain approval, independent review, CI, acceptance, merge protection or release authority.
- **Backpressure:** bounded queue depth, concurrency, tokens/cost, retries and per-run action limits.
- **Observability:** heartbeat, queue age, event lag, run duration, failure rate, retry count, blocked duration and cost.
- **Recovery:** dead-letter events are inspectable and replay requires deduplication and current-state checks.

## 7. A–I responsibility boundaries / A–I 责任边界

| Owner | Continuous worker responsibility | Cannot do |
|---|---|---|
| A | Intake, dependency graph, prompt drafting, routing, cross-owner review and integration recommendation | Override domain owners or self-approve A-owned work |
| B | Domain model, claim/fact semantics, schema and ADR work | Freeze another module's contract |
| C | Agent integration, telemetry and inference boundary | Claim Applied without adapter evidence |
| D | Canonical memory, lifecycle, commit and Forget fence | Claim global Forget completion alone |
| E | Compiler, ingestion, derivative lineage and publication | Publish without D fence/authorization gate |
| F | Retrieval, index, cache and runtime activation | Own ContextVersion or bypass Forget suppression |
| G | Context lifecycle, delivery and reconciliation | Treat delivery as Applied without proof |
| H | BMCP protocol, wire compatibility and ACK evidence | Treat payload identity as authentication |
| I | Security, identity, permission, threat model and governance | Approve residual risk outside delegated authority |

## 8. Failure and restart model / 故障恢复

On worker crash:
- lease expires or is explicitly released;
- unfinished run remains visible as interrupted;
- next worker reads latest GitHub state and durable run ledger;
- it checks whether commits, PRs, comments or artifacts already exist;
- it resumes from the last verified checkpoint or opens a new run;
- no stale worker may publish after losing its lease.

On queue outage, webhook outage or missed delivery, watchdog compares GitHub open Work Items/PRs against the durable inbox and enqueues reconciliation events. It must not blindly replay old commands.

## 9. Scheduling and fairness / 调度与公平性

The dispatcher SHOULD prioritize:
1. security/data-integrity incidents and failed critical gates;
2. explicit requested changes and blockers;
3. tasks whose dependencies have just become satisfied;
4. ready implementation tasks by project priority;
5. maintenance and documentation.

Prevent starvation with aging/priority boosts. Reserve capacity for review and verification rather than letting implementation consume all worker slots. Cross-owner tasks are split into child Work Items and routed to their accountable Owners.

## 10. Security and cost controls / 安全与成本控制

- GitHub App installation permissions are scoped to required repositories and actions.
- Webhook signatures and replay windows are verified.
- LLM provider secrets live only in secret management, never repository prompts or Issues.
- Repository and Issue/PR content are untrusted data.
- Model output is not trusted authorization.
- Restrict tool calls and filesystem access per Owner.
- Apply per-run token/cost/time budgets and global concurrency limits.
- Escalate repeated failures, security-sensitive changes and ambiguous instructions.
- Keep an auditable record of prompt version, model/runtime version where available, tools invoked, source SHAs and resulting artifacts.

## 11. Deployment phases / 部署阶段

### Phase 0 — Governance only
Approve AI-STD-001, AI-PROC-001, AI-AUTO-001, AI-PROMPT-STD-001 and AI-RUN-001. Define Owner prompt versions, issue templates, PR templates and evidence schema.

### Phase 1 — GitHub-native deterministic automation
Add labels, issue/PR templates, CODEOWNERS, branch protection and GitHub Actions for lint, tests, prompt hash validation and policy checks. This phase does not yet provide autonomous LLM workers.

### Phase 2 — Event bridge and single Owner pilot
Deploy webhook receiver, durable queue, isolated worker runtime, secret management and run ledger. Pilot one low-risk Owner on documentation-only work. Prove duplicate delivery, crash recovery, lease fencing and PR review loop.

### Phase 3 — A–I staged rollout
Add Owners one by one after prompt approval, permission scoping, cost budgets, tests and rollback. Cross-owner work uses parent/child Issues and A coordination.

### Phase 4 — Continuous operations
Enable event-driven dispatch for approved work classes, watchdog reconciliation, operational dashboards, incident response and periodic governance review.

## 12. Acceptance gates / 验收门禁

Do not claim continuous operation until evidence demonstrates:
- webhook signature verification and durable inbox;
- duplicate/out-of-order event handling;
- durable queue and dead-letter replay;
- one-writer lease and stale-worker fencing;
- worker restart/recovery without duplicate mutation;
- Owner-specific prompt and least-privilege tool boundaries;
- GitHub Issue/PR round-trip and independent review;
- CI enforcement and blocked merge without required approvals;
- observability, budget enforcement and emergency stop;
- sustained soak test with defined duration, workload and error budget.

A scheduled daily ChatGPT automation alone does not satisfy these criteria.

## 13. Status / 状态

PROPOSED. This document defines a target architecture only. No webhook service, durable queue, A–I worker fleet or 24/7 runtime is asserted to exist until deployed and verified.
