# Validation Assets / 验证资产

## Status
- Design scenarios: 20 defined in `agent-integration-validation-plan.md`.
- Executable provider adapter tests: NOT RUN.
- Real provider tests: NOT RUN.
- Real tool side-effect/recovery tests: NOT RUN.
- C/H cryptographic profile registration: NOT RUN / NOT REGISTERED.
- H Unified 1.2.15 exact validator CI: NOT VERIFIED in this C pass.
- G Applied end-to-end tests: NOT RUN / NOT VERIFIED.
- Forget-vs-late-result fault injection: NOT RUN.
- Performance benchmarks: NOT RUN.

## Required future assets
1. Version-pinned Provider capability fixtures per provider/model/API.
2. Streaming transcripts: complete, partial, malformed, disconnected, duplicated and late terminal events.
3. Request/Attempt idempotency and timeout race fixtures.
4. Tool side-effect lost-ACK fixtures with external reconciliation.
5. CSubmitOutcome 1.0.1 schema and cryptographic vectors from exact C owner branch.
6. H exact-version 1.2.15 schema/validator/CI bundle from H.
7. G Applied predicate fixtures and D Forget fence/lineage race fixtures.
8. Redaction tests with synthetic secrets and sensitive content.
9. Trace propagation tests across process boundaries and untrusted ingress.
10. Cross-tenant authorization negative fixtures owned/approved by I.

No production secrets, live user memory or real personal data may be used in synthetic conformance fixtures.


## 中文验证资产说明

### 当前状态
验证设计已定义 20 个场景。Provider Adapter 可执行测试、真实 Provider 测试、真实 Tool 副作用/恢复测试均 NOT RUN。C/H 密码配置 NOT REGISTERED。H Unified 1.2.15 精确 Validator CI 本次 NOT VERIFIED。G Applied 端到端测试 NOT RUN/NOT VERIFIED。Forget 与迟到结果故障注入 NOT RUN。性能基准 NOT RUN。

### 后续必须准备的资产
1. 每个 Provider/Model 的固定版本能力 Fixture。
2. 完整、部分、畸形、断连、重复和迟到 Streaming Transcript。
3. Request/Attempt 幂等和超时竞态 Fixture。
4. Tool 副作用后 ACK 丢失及外部对账 Fixture。
5. CSubmitOutcome 1.0.1 Schema 与精确 C Owner 密码向量。
6. H 1.2.15 精确 Schema/Validator/CI Bundle。
7. G Applied Predicate 与 D Forget Fence/Lineage 竞态 Fixture。
8. 使用合成 Secret 和敏感内容的脱敏测试。
9. 跨进程 Trace 传播和不可信入口测试。
10. 由 I 拥有/批准的跨 Tenant 授权负面 Fixture。

不得在合成符合性 Fixture 中使用生产 Secret、真实用户 Memory 或真实个人数据。


## H 1.2.15 external CI evidence / H 1.2.15 外部 CI 证据
H exact-head local tests have been verified directly from GitHub Actions, not executed by this C research branch:
- Commit `0d36324457e39bd50ad56ae902d477c4ea765b61`: Provider Outcome run 44079842914, 91 tests, 0 failures, SUCCESS.
- Same commit: Recovery Cutoff run 44079842878, 288 tests, 22 skipped, 0 failures, SUCCESS.
These are H local reference tests only. C Agent/Provider/Tool/Brain end-to-end tests, C/H/I trust production tests, Forget-vs-late-result integration and C benchmarks remain NOT RUN.

### 中文
H 精确 HEAD 的本地测试已通过 GitHub Actions 实际日志核验，但不是由 C 本研究分支执行：Provider Outcome 91 项、0 失败；Recovery Cutoff 288 项、22 项跳过、0 失败。它们仅是 H 本地参考测试。C 的 Agent/Provider/Tool/Brain 端到端测试、C/H/I 生产 Trust 测试、Forget 与迟到结果集成测试以及 C 基准测试仍全部 NOT RUN。
