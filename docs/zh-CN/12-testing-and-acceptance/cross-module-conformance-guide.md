# 跨模块一致性与故障注入指南

- 文档 ID：DOC-TEST-001
- 版本：1.0
- 协调方：A — Principal Integration
- 参与方：B/C/D/E/F/G/H/I、Storage/Consistency、Testing/QA、Engineering
- 源规范：A Owner 分支中的 Phase 3 Cross-Module Conformance and Fault-Injection Plan
- 对应英文：[Cross-Module Conformance & Fault-Injection Guide](../../en/12-testing-and-acceptance/cross-module-conformance-guide.md)
- 状态：TO_VALIDATE 测试设计；不声称任何测试已经执行或通过

## 1. 什么才算测试证据

允许的结果状态：
- NOT_RUN：没有执行证据。
- BLOCKED：由于实现或依赖缺失，无法执行。
- FAIL：存在可复现反例。
- PASS：必须有版本化测试代码/流程、声明的环境、确定性 Fixture、预期与实际结果、日志/产物引用以及可复现的再次运行。
- TO_VALIDATE：候选测试设计或契约仍待审查。

静态文档一致性不等于运行时 Conformance。测试计划不证明测试已经通过。

每条证据必须包括 Test ID/Version、Contract Revision/Commit、代码/流程版本、环境和依赖版本、确定性 Fixture/Seed、准确命令、预期结果、实际结果、日志/Trace/Artifact 引用、时间、审查者和重跑结果。必须脱敏 Secret 和已遗忘内容。

## 2. 测试套件与 Owner

| 套件 | 负责 Owner | 必需协作方 |
|---|---|---|
| TC-01 领域身份和引用 | B | D/E/F/G |
| TC-02 Scope/身份/权限 | I | B/C/D/E/F/G/H |
| TC-03 Event Accepted/Idempotency | E | C/H/I/Storage |
| TC-04 Canonical Commit/Revision/Lifecycle | D | B/E/Storage |
| TC-05 Typed Cursor/Watermark | D 负责 Canonical；E 负责 Ingress/Publication；G 负责 Context；A 协调 | D/E/F/G/Storage |
| TC-06 Forget/Anti-resurrection | I | D/E/F/G/H/Storage |
| TC-07 Retrieval Freshness/Cache | F | D/E/I/G |
| TC-08 Context CAS/Reconciliation/Delivery | G | D/F/H/C/I |
| TC-09 Applied Final-request Attestation | H | C/G/I |
| TC-10 Provenance/Lifecycle/Temporal | B | D/E/F/I |
| TC-11 Adapter/Security Prompt Boundary | C | H/I/Agent Runtime |
| TC-12 Workload/Performance | Engineering | D/E/F/G/Storage |

如果必需契约或实现缺失，测试套件保持 BLOCKED。这是依赖状态，不是对缺席模块质量的负面评价。

## 3. 关键测试场景

### 领域和身份
- 新版本提交后，旧的不可变 Version Reference 仍能准确读取。
- 没有显式共享授权时，跨 Scope 引用必须拒绝。
- Fact/Claim 身份测试在 ADR 批准前保持 BLOCKED。
- Entity Merge/Split 保留旧引用和明确映射。
- 认证 Transport Identity 不得被 Payload 自报身份替代；不一致时拒绝。

### 接收与编译
- Event 和可恢复 Compile Intent 持久化前不得返回 Accepted Receipt。
- 重复投递必须幂等；相同 Key 对应不同 Payload Digest 时必须判为冲突。
- Worker 崩溃、Lease 过期、Retry、DLQ 和 Replay 不得产生重复 Canonical 效果。
- 模型不可用不得导致已接收 Event 丢失。

### Cursor、Forget 和防复活
- 不同命名空间的 Typed Cursor 不得比较或强制转换。
- Watermark 只能推进已连续核算的前缀。
- Forget 必须与 Producer Admission、Dependency Registration 和 Publication 进行竞态测试。
- 在线性化边界的每个崩溃点，都不得暴露已遗忘派生物。
- Index Rebuild 和 Cache Refill 不得使已抑制内容复活。
- Backup Restore 必须在恢复数据可查询之前执行 Forget Fence。

### Context 与 Adapter
- 并发 Context 编辑必须使用唯一权威版本序列。
- 过期 ChangeSet 必须拒绝或协调。
- Delivery 和 Applied 状态不得混淆。
- Tier 1 Applied 必须绑定实际提交的最终请求。
- 离线重连必须协调当前 ContextVersion、PermissionEpoch 和 ForgetFenceGeneration。
- Prompt Injection 内容必须在受管区域中保持为数据。

### 安全和运维
- 跨用户/Agent/Environment 查询不得返回受保护内容、数量或存在性信息。
- 权限撤销必须在排队/Lease 任务实际执行时生效。
- 未知/不支持的 Forget 目标，未经批准的例外不得算作成功。
- 性能结果必须声明硬件、语料、并发和百分位计算方法。

## 4. PASS 的证据标准

PASS 必须具备：
1. 准确的契约版本和 Owner 批准。
2. 可执行测试或可复现人工流程。
3. 已声明环境和确定性 Fixture。
4. 预期与实际结果。
5. 脱敏后的日志/Trace/Artifact。
6. 审查者和可重复运行证据。

设计审查、文档 Diff 或静态 Lint 通过，不能证明并发、崩溃恢复、安全或性能。

## 5. 执行顺序

1. 解决阻塞性的领域/身份契约。
2. 实现可靠接收、Canonical Commit、Cursor 和 Forget 线性化。
3. 集成 Index、Cache、Context 和 Adapter 证明。
4. 执行安全和防复活故障测试。
5. 正确性关键行为稳定后，再执行代表性性能/资源 Benchmark。

详细测试目录见 [A Owner 分支 Conformance Plan](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-a-integration-2026-11-16/reviews/integration/cross-module-conformance-plan.md)。
