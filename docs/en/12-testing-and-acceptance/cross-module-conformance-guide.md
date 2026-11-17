# Cross-Module Conformance & Fault-Injection Guide

- Document ID: DOC-TEST-001
- Version: 1.0
- Coordinator: A — Principal Integration
- Contributors: B/C/D/E/F/G/H/I, Storage/Consistency, Testing/QA, Engineering
- Source: A owner branch, Phase 3 Cross-Module Conformance and Fault-Injection Plan
- Chinese counterpart: [跨模块一致性与故障注入指南](../../zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md)
- Status: TO_VALIDATE test design; no test is claimed executed or passed

## 1. What counts as test evidence

Allowed result states:
- NOT_RUN — no execution evidence.
- BLOCKED — cannot execute because an implementation/dependency is absent.
- FAIL — reproducible counterexample.
- PASS — only with versioned test code/procedure, declared environment, deterministic fixture, expected and actual results, logs/artifact reference, and reproducible rerun.
- TO_VALIDATE — candidate test design or contract awaiting review.

Static document consistency is not runtime conformance. A test plan does not prove a test passed.

Every evidence record must include test ID/version, contract revision/commit, code/procedure revision, environment and dependency versions, deterministic fixture/seed, exact command, expected result, actual result, logs/traces/artifact reference, timestamp, reviewer, and rerun result. Secrets and forgotten payloads must be redacted.

## 2. Test suites and owners

| Suite | Accountable owner | Required collaborators |
|---|---|---|
| TC-01 Domain identity and references | B | D/E/F/G |
| TC-02 Scope/identity/permission | I | B/C/D/E/F/G/H |
| TC-03 Event Accepted/idempotency | E | C/H/I/Storage |
| TC-04 Canonical commit/revision/lifecycle | D | B/E/Storage |
| TC-05 Typed cursors/watermarks | D canonical; E ingress/publication; G Context; A coordinates | D/E/F/G/Storage |
| TC-06 Forget/anti-resurrection | I | D/E/F/G/H/Storage |
| TC-07 Retrieval freshness/cache | F | D/E/I/G |
| TC-08 Context CAS/reconciliation/delivery | G | D/F/H/C/I |
| TC-09 Applied final-request attestation | H | C/G/I |
| TC-10 Provenance/lifecycle/temporal | B | D/E/F/I |
| TC-11 Adapter/security prompt boundary | C | H/I/Agent runtime |
| TC-12 Workload/performance | Engineering | D/E/F/G/Storage |

A suite remains BLOCKED if its required contract or implementation is absent. That is a dependency status, not a negative quality verdict on an unavailable component.

## 3. Critical scenarios

### Domain and identity
- Immutable version references continue to resolve after a newer version commits.
- Cross-Scope references are rejected without explicit sharing authorization.
- Fact/Claim identity tests remain BLOCKED until the ADR is approved.
- Entity merge/split preserves old references and explicit mappings.
- Authenticated transport identity overrides no payload-supplied identity; mismatch is rejected.

### Ingestion and compilation
- No Accepted receipt before Event and recoverable compile intent are durable.
- Duplicate delivery is idempotent; same key with different payload digest is a conflict.
- Worker crash, lease expiry, retry, DLQ, and replay do not duplicate canonical effects.
- Model outage does not lose accepted Events.

### Cursors, Forget, and anti-resurrection
- Typed cursors cannot be compared or coerced across namespaces.
- Watermark advances only a contiguous accounted-for prefix.
- Forget races with producer admission, dependency registration, and publication.
- Crash at each linearization boundary does not expose a forgotten derivative.
- Index rebuild and cache refill cannot resurrect suppressed content.
- Backup restore applies Forget fences before restored data is queryable.

### Context and Adapter
- Concurrent Context edits use one authoritative version sequence.
- Stale ChangeSet is rejected or reconciled.
- Delivery/Applied states cannot be conflated.
- Tier 1 Applied binds to the final request actually submitted.
- Offline reconnect reconciles current ContextVersion, PermissionEpoch, and ForgetFenceGeneration.
- Prompt-injection payload remains data inside the managed region.

### Security and operations
- Cross-user/Agent/environment query returns no protected content, count, or existence leak.
- Revoked permission blocks queued/leased work at execution.
- Unknown/unsupported Forget targets are not counted as successful without an approved exception.
- Performance results declare hardware, corpus, concurrency, and percentile method.

## 4. Evidence standard for PASS

A PASS requires:
1. Exact contract revision and owner approvals.
2. Executable test or reproducible manual procedure.
3. Declared environment and deterministic fixtures.
4. Expected and actual result.
5. Logs/traces/artifacts with sensitive data redacted.
6. Reviewer and repeatable rerun evidence.

A design review, document diff, or green static lint is not sufficient for concurrency, crash recovery, security, or performance claims.

## 5. Execution order

1. Resolve blocking domain/identity contracts.
2. Implement durable acceptance, canonical commit, cursor and Forget linearization.
3. Integrate indexes, caches, Context and Adapter proof.
4. Run security and anti-resurrection fault suites.
5. Run representative performance/resource benchmarks after correctness-critical behavior stabilizes.

See the [A owner branch conformance plan](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-a-integration-2026-11-16/reviews/integration/cross-module-conformance-plan.md) for the detailed test catalogue.
