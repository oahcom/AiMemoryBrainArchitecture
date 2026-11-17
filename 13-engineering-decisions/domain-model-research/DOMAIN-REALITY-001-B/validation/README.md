# Validation Package
# 验证包

- Status / 状态: SPECIFICATION ONLY — no executable tests run / 仅规范说明 — 尚未运行可执行测试
- Reason / 原因: Core Fact/Claim, typed-reference field grammar, Context schema, Applied wire mapping and JF-10 storage interface are not frozen. The repository has no runtime implementation in main; Issue #7 requires the authoritative runtime repository and engineering owner to be identified. / 核心 Fact/Claim、类型化引用字段语法、Context Schema、Applied Wire 映射及 JF-10 Storage 接口均未冻结。main 中没有运行时实现；Issue #7 要求确定权威运行时仓库及负责工程 Owner。

## 1. Included test specifications / 已包含的测试规范

- See ../canonical-domain-invariants.md, Section 9. / 参见 ../canonical-domain-invariants.md 第 9 节。
- Identity, relationship, temporal, evidence, state, Forget/deletion and protocol invariants are enumerated with positive/negative conditions and owner assignments. / 已列出身份、关系、时间、证据、状态、Forget/删除和协议不变量，并为其规定正向/负向条件及 Owner 归属。

## 2. Schema disposition / Schema 处置

No normative JSON Schema is emitted in this pass. Doing so would freeze unresolved field names and requiredness. Candidate schemas may be created only after:

本轮不发布规范性 JSON Schema，否则会冻结尚未解决的字段名称和必填性。只有满足以下条件后，才可创建候选 Schema：

1. B Fact/Claim and Claim identity ADR closure. / B 的 Fact/Claim 与 Claim 身份 ADR 已关闭。
2. I/B typed reference grammar and namespace acceptance. / I/B 已验收类型化引用语法与命名空间。
3. G ContextVersion/ChangeSet/Applied exact schema acceptance. / G 已验收精确版本的 ContextVersion/ChangeSet/Applied Schema。
4. H wire schema and C/G/H Applied package acceptance. / H Wire Schema 及 C/G/H Applied 套件已验收。
5. D/E/Storage publication/Forget gate interface acceptance. / D/E/Storage 已验收发布/Forget 门禁接口。

## 3. Required future validation / 后续必需验证

- JSON Schema Draft 2020-12 meta-schema validation for stable serialized contracts. / 对稳定序列化契约执行 JSON Schema Draft 2020-12 Meta-Schema 验证。
- Positive and negative fixture suites for each entity/reference/state. / 为每种实体、引用和状态建立正向及负向 Fixture 套件。
- Property-based tests for ID non-reuse, version monotonicity, relation endpoint constraints, scope isolation and idempotency. / 针对 ID 不复用、版本单调性、Relation 端点约束、Scope 隔离和幂等性执行属性测试。
- Fault-injection tests for D fence vs publication, I revocation vs submit, same-XID recovery and restore quarantine. / 针对 D Fence 与发布竞争、I 撤销与提交竞争、同一 XID 恢复及 Restore 隔离执行故障注入测试。
- Bilingual semantic parity check. / 执行双语语义一致性检查。
- Owner-specific executable tests in the canonical runtime implementation repository. / 在规范运行时实现仓库中执行各 Owner 专属可执行测试。

## 4. Current result / 当前结果

- Schema validation: NOT RUN / NOT CREATED. / Schema 验证：尚未运行 / 尚未创建。
- Unit/integration tests: NOT RUN. / 单元/集成测试：尚未运行。
- Property tests: NOT RUN. / 属性测试：尚未运行。
- Fault injection: NOT RUN. / 故障注入：尚未运行。
- Runtime implementation evidence: NOT VERIFIED. / 运行时实现证据：尚未核验。

## 5. Gate status / 门禁状态

B4 is NOT READY. This document records a validation plan and current evidence limits only. It does not claim executable conformance, schema readiness or production readiness.

B4 尚未就绪。本文件仅记录验证计划及当前证据限制，不宣称可执行一致性、Schema 就绪或生产就绪。
