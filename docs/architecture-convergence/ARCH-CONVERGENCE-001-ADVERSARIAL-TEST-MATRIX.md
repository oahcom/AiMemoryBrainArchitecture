# ARCH-CONVERGENCE-001 — Adversarial Test Matrix
# ARCH-CONVERGENCE-001 — 对抗性测试矩阵

- Status: **DRAFT / TEST DEFINITIONS ONLY / NOT EXECUTED**
- Baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Companion: `ARCH-CONVERGENCE-001-INTEGRATION-REVIEW.md`
- Rule: A PASS must cite exact code commit, database/profile/version/configuration, fixture, test log and Owner scope. A reference-model PASS is not a physical integration PASS.

## 1. Test execution layers / 测试执行层级

| Layer | Purpose | Evidence required |
|---|---|---|
| L0 — Pure contract/model | State transitions, identity, digest, fail-closed rules | Versioned vectors/model and counterexample coverage |
| L1 — Single-process adapter | Repository, transaction and protocol adapter behavior | Exact build, deterministic test logs |
| L2 — Multi-process/concurrency | Real database locking, fencing, races, duplicate delivery | Database/profile, process topology, scheduler/barrier logs |
| L3 — Recovery/restore | Crash, failover, PITR, old-backup anti-rollback | Physical environment, backup/WAL, COC/I/D/Storage proofs |
| L4 — End-to-end | Ingestion through exact request and G Applied | Full cross-owner evidence bundle and independent review |

No test may be promoted to a higher layer by inference.

## 2. Core adversarial scenarios / 核心对抗场景

| ID | Initial state and event sequence | Expected result | Forbidden result | Required fence/version/transaction | Evidence and automated test candidate |
|---|---|---|---|---|---|
| AT-01 Duplicate ingestion | Same authenticated scope submits same idempotency key and digest twice | Original AcceptedReceipt/WorkItem identity returned | Duplicate logical work or second canonical commit | E scoped idempotency key + semantic digest | E receipt ledger; replay same request and compare immutable IDs |
| AT-02 Same logical fact concurrency | Two concurrent candidates represent the same proposed fact while B ADR is blocked | Neutral candidates or explicit conflict; no canonical identity assumption | Silent overwrite, invented FactRef/ClaimRef or arbitrary merge | B ADR gate; D aggregate CAS | Concurrent candidate race; assert no canonical Fact/Claim write |
| AT-03 Crash before canonical commit | Kill process after staging but before D/Storage transaction commit | No visible canonical effect; same logical operation can retry | Partial MemoryVersion, head advance, lifecycle event or cursor | D/Storage atomic write set | Kill-before-commit hook; restart and read all canonical tables |
| AT-04 Crash after canonical commit | Kill after durable commit but before caller ACK | Same receipt, cursor and committed state recovered | Second commit or lost outcome | Stable operation/idempotency identity; commit receipt | Kill-after-commit hook; same-key readback |
| AT-05 Worker lease expiration | Worker A lease expires while a Forget barrier is draining; worker B reclaims | Old lease fenced; work remains open until terminal evidence | Expired lease treated as completion or stale A publishes | Lease generation/fencing token + D producer barrier | Two-worker deterministic lease race |
| AT-06 Partial-processing retry | Retry after compiler/derivative step partially completed | Same WorkItem/lineage; new AttemptId; fresh I/D checks | New logical identity bypasses fence or duplicate canonical mutation | WorkItemId, AttemptId, LeaseId, latest PermissionEpoch/Fence | Inject failure after each stage; retry and compare lineage |
| AT-07 Duplicate/out-of-order outbox | Deliver event twice and deliver cursor N+1 before N | Idempotent projection; contiguous watermark waits for gap | Duplicate side effect or watermark jump | Stable event identity; partition cursor | Outbox replay permutation/property test |
| AT-08 Forget vs ingestion | Registration races with Fence installation | Registration-before-Fence is included; Fence-before-registration rejects/quarantines | Admitted-but-unaccounted producer can publish | D serialized registration/Fence high-water | Barrier race with controlled transaction scheduler |
| AT-09 Forget vs retrieval | Pause after ranking/materialization; install Fence; resume response | Final disclosure revalidates and suppresses affected item | Forgotten content/snippet/count disclosed | Latest D Fence + I authorization at final read | Pause/resume race at serialization boundary |
| AT-10 Forget vs index publication | Pause before index swap; install Fence; resume publisher | Publication rejected/quarantined or filtered before visibility | Stale segment becomes visible | D publication/Fence ordering + F watermark | Index-swap barrier race |
| AT-11 Late stale worker | Worker A loses lease; worker B completes newer attempt; A returns late | A's result rejected/quarantined | Stale worker overwrites current projection or terminal state | Lease fencing + WorkItem generation + source cursor | Late-commit test with two workers |
| AT-12 Revocation after retrieval | Retrieve candidate, advance I PermissionEpoch/revoke, then dispatch | Final egress denied/paused; no Full Applied | Cached Permit or earlier retrieval authorizes dispatch | Current I epoch/decision at final boundary | Pause before provider submit; revoke then resume |
| AT-13 Epoch changes during assembly | Advance PermissionEpoch during Context assembly | Rebuild or block; stale Context cannot dispatch | Old epoch treated current | I sequencer ordering + G ContextVersion | Concurrent epoch mutation between assembly and submit |
| AT-14 PDP failure | Inject timeout, parse error, missing attribute, invalid bundle or indeterminate result | I PEP returns DENY/PAUSE | Skip-on-error or unrelated Permit masks failure | I-owned fail-closed wrapper | Fault injection across every evaluator failure class |
| AT-15 Crash after provider dispatch | Provider may have accepted request; process crashes before outcome/Applied persistence | C outcome UNKNOWN/IN_DOUBT; reconcile same attempt/key | Assume NOT_INVOKED or send under new provider key | ProviderAttemptId + provider idempotency key + exact request digest | Egress crash hook; same-key reconciliation |
| AT-16 Duplicate provider callback | Same callback arrives twice, then conflicting digest arrives | Same identity/digest idempotent; conflicting digest rejected | Duplicate side effect or mutation of terminal outcome | C outcome identity/revision/digest | Callback replay and mutation tests |
| AT-17 Restore older than Forget fence | Restore backup predating newer Fence/PermissionEpoch/inventory seal | RESTORE_FENCED; no listener/read/rebuild/reconnect until reconciliation | Old snapshot serves forgotten or revoked data | COC/I/D/Storage high-waters + same-GID ledger | Physical old-backup restore drill |
| AT-18 Index rebuild after Forget | Rebuild from pre-Fence snapshot after Forget completed | Every batch and final publication checks current Fence; stale build quarantined | Rebuild resurrects target | Fence generation + canonical cursor + final pointer gate | Rebuild from stale snapshot after Fence |
| AT-19 Cross-tenant/principal retrieval | Principal A probes Principal B scope through query, count, cache and error paths | No data or existence/count/snippet leakage | Cross-scope disclosure or cache-key collision | I principal/scope/environment binding | Cross-scope API/index/cache probes |
| AT-20 MCP authorization bypass | Tool submits forged principal/scope or reuses stale grant | Call re-enters I PEP and D visibility; deny if not current | MCP server/connector role becomes Brain authorization | Authenticated transport identity + current PermissionEpoch/Fence | Protected tool calls with forged and revoked contexts |

## 3. Applied/runtime-specific scenarios / Applied 与 Runtime 专项场景

| ID | Initial state and event sequence | Expected result | Forbidden result | Required fence/version/transaction | Evidence and automated test candidate |
|---|---|---|---|---|---|
| AT-21 Tier-2 materialization only | Adapter proves managed-region materialization but cannot observe exact submitted request | Partial/Unknown only | Full Applied | Evidence tier ceiling + final-request boundary identity | H Tier-2 fixture; G predicate must reject Full |
| AT-22 Incomplete managed region | Tier-1 final request observed but region inventory/digest is incomplete | Full Applied rejected | Treat partial region as complete | ContextVersion + region inventory/content digest | Mutate omitted region entry; assert G rejection |
| AT-23 Post-hook request mutation | Final payload changes after evidence hook but before actual provider submit | Evidence rejected or boundary reports different immutable request | Old digest attests mutated request | Immutable final request digest + actual submit ID | Inject post-hook transformer and compare digests |
| AT-24 H evidence without C outcome | H authenticated evidence exists; C outcome missing/UNKNOWN | G Applied absent | H ACK or materialization writes Applied | Same request/attempt identity; C outcome terminal predicate | G persistence test with C evidence omitted |
| AT-25 C outcome without H evidence | C reports handoff accepted; H final-request evidence absent | G Full Applied absent | Provider ACK alone becomes Applied | Same request identity + H eligible evidence | G predicate test with H evidence omitted |
| AT-26 Crash around G Applied commit | Crash before commit, then crash after commit before response | Before: no Applied; after: same Applied record returned | Duplicate Applied record or lost committed decision | G Applied identity + evidence revision + transaction | Kill-before/after G commit and replay same identity |

## 4. Cross-owner acceptance requirements / 跨 Owner 验收要求

| Owner | Required tests owned or co-signed |
|---|---|
| B | AT-02, AT-03, AT-22; typed candidate and semantic gate |
| C | AT-12, AT-15, AT-16, AT-23, AT-25; exact provider submit and same-attempt reconciliation |
| D | AT-03, AT-08–AT-11, AT-17–AT-20; canonical commit, ForgetFence and visibility |
| E | AT-01, AT-05–AT-08; accepted receipt, producer work, lease/retry and lineage |
| F | AT-07, AT-09–AT-11, AT-18–AT-19; projection, retrieval and final disclosure |
| G | AT-09, AT-13, AT-21–AT-26; ContextVersion and sole Applied persistence |
| H | AT-16, AT-21–AT-25; authenticated Adapter/wire evidence and replay |
| I | AT-12–AT-14, AT-17, AT-19–AT-20; identity, PermissionEpoch, revocation and fail-closed PEP |
| Storage | AT-03–AT-08, AT-10–AT-11, AT-17, AT-26; physical atomicity, fencing, outbox and restore |
| COC | AT-04, AT-15, AT-17, AT-26 where COC/JF-10 participates; durable terminal and recovery proof |

## 5. Exit criteria / 退出标准

A scenario is closed only when:
1. The responsible Owner identifies the exact contract/schema/validator version.
2. The test runs against the declared physical profile where the invariant depends on database behavior.
3. Failure injection and recovery are observed, not simulated only in prose.
4. Evidence records commit SHA, database engine/version/config, test command, exit code, log/artifact digest and relevant operation identities.
5. Cross-owner tests include each consumer's acceptance, not only the producer's local unit test.
6. Any unsupported deployment profile or untested failure envelope remains explicitly OPEN.

**Matrix status: 26 test definitions authored; 0 executions claimed by this document.**

**矩阵状态：已定义 26 项测试；本文件不声称其中任何一项已执行。**
