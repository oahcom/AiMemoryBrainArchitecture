# AID-2026-001 — R3 Contract Test Matrix
# AID-2026-001 — R3 契约测试矩阵

**Work Item:** AID-2026-001
**Classification:** ARCH / R3
**Status:** TEST SPECIFICATION ONLY — NOT EXECUTED
**Applies to:** security identity, authorization, privacy/retention/audit and Forget/deletion normative boundaries.

This matrix defines minimum reproducible contract tests. It is not evidence that tests have run. Each execution must record the exact test harness/version, fixtures, command, output, result, commit SHA and reviewer.

本矩阵定义最低可复现契约测试，不代表测试已经执行。每次执行必须记录准确测试工具及版本、Fixture、命令、输出、结果、Commit SHA 和 Reviewer。

| ID | Contract invariant | Positive case | Negative / failure case | Required observable evidence |
|---|---|---|---|---|
| R3-001 | Domain identity is not a security principal | A domain entity identifier resolves only within its declared domain semantics | Domain identity alone is presented as proof of authentication or authorization | Fixture and assertion showing domain identity cannot grant access |
| R3-002 | Authorization precedes Forget execution | Authorized principal requests Forget within permitted scope | Unauthenticated/unauthorized principal attempts the same operation | Decision trace proving deny occurs before mutation |
| R3-003 | Forget scope is bounded | Authorized request affects exactly the approved subject/scope | Cross-tenant, cross-user or out-of-scope identifier is supplied | Before/after state proving no out-of-scope data changed |
| R3-004 | D/I bilateral contract boundary is respected | D defines canonical lifecycle/deletion semantics and I defines authorization/privacy/retention controls; both agree on joined contract | Either side unilaterally changes the other's authority | Contract fixture and explicit bilateral approval record |
| R3-005 | Retention/legal hold constraints are enforced | Applicable retention/legal hold is evaluated and documented | Forget bypasses mandatory retention/legal hold or silently destroys required audit evidence | Deterministic policy fixture and expected allow/deny outcome |
| R3-006 | Deletion completion is truthful and evidence-backed | Completion is reported only after all required deletion stages reach defined terminal states | Partial failure is reported as complete | Stage-by-stage state and completion assertion |
| R3-007 | Audit evidence is bounded and non-authoritative over domain semantics | Audit records prove who/what/when/scope/result without redefining canonical memory semantics | Audit metadata is treated as authorization or domain truth without validation | Structured audit fixture and validation assertions |
| R3-008 | Retry/idempotency is safe | Repeating the same authorized Forget request does not produce inconsistent outcomes | Retry duplicates destructive side effects or loses completion evidence | Repeated execution trace and invariant checks |
| R3-009 | Partial failure and recovery fail closed | Interrupted deletion is represented as incomplete and safely resumable | System reports success or exposes stale data after incomplete deletion | Fault-injection trace, recovery result and final state assertions |

## Execution record template / 执行记录模板

For every test ID, record:
- Test ID and version:
- Exact source contract SHA(s):
- Test harness and version:
- Fixture/input:
- Exact command:
- Expected result:
- Actual result:
- Pass/fail:
- Logs/evidence reference:
- Executed at commit SHA:
- Executed by:
- Independently reviewed by:

每项测试均须记录：测试 ID/版本、源契约 SHA、测试工具及版本、Fixture/输入、准确命令、预期结果、实际结果、通过/失败、日志/证据引用、执行 Commit SHA、执行者及独立复核者。

**Current execution status:** NOT RUN / NOT EVIDENCED. No acceptance credit may be claimed from this specification alone.
