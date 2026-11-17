# Owner B — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-B-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Session B — Fact / Claim ADR and Domain Semantics

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Domain Model Principal Architect，负责 Phase 3 的 Fact/Claim 领域决策。你拥有领域语义设计权，但不拥有 D 的存储实现、I 的授权策略、H 的 wire protocol 或 G 的 Context 版本权。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部文件
- 02-domain-model/ 全部现有文档
- D 分支 03-memory-brain/ 下相关设计，特别是 canonical store、lifecycle、versioning、entity/relationship 文档
- E 分支 extraction/normalization 与 consolidation/conflict 文档
请在报告中记录每个源文件的 branch/ref 和 commit SHA；不可将未合并分支文件当作 main 文件。

【核心任务】
1. 解决 INT-P0-01：Fact 与 Claim 的规范关系。提出并比较至少两种可行模型，分析身份稳定性、版本、证据挂接、冲突、撤回、纠正、时间有效性和历史追溯。
2. 定义 Claim identity、不可变 ClaimRevision、Evidence、Provenance、ConflictSet 的关系；区分 confidence、epistemic status、validity interval、lifecycle。
3. 通过 ADR 给出决策。若权限或依据不足，必须标记 ADR-BLOCKED，列出决策人和剩余问题；不得擅自宣布通过。
4. 定义 typed domain references：MemoryRef、MemoryVersionRef、ClaimRef、ClaimRevisionRef、EntityRef、EvidenceRef、ScopeRef、ActorRef、EventRef、TimeValue/TimeInterval。每种引用需定义唯一性边界和生命周期语义。
5. 定义 Scope 的领域语义、包含/继承关系；Scope 不等于 Permission，授权规则由 I 负责。
6. 给 E 提供 CandidateProposition/ExtractionIR 到规范模型的映射；给 D/F/G 定义消费者语义。

【交付物】
仅在 B 所属工作分支修改/创建：
- 02-domain-model/adr/ADR-001-fact-claim-canonical-model.md
- 02-domain-model/typed-reference-and-scope-semantics.md
- 02-domain-model/fact-claim-consumer-mapping.md

如果这些路径已存在，先读取并在本分支按规则更新，不要覆盖其他分支或其他模块文件。

【验收】
- ADR 为 APPROVED 或明确 ADR-BLOCKED，不允许模糊状态。
- D/E/F/G 对 Claim identity、ClaimRevision、ConflictSet 具有一致消费语义。
- 所有引用类型有明确 namespace/scope 和版本语义。
- Scope 与 Permission 分离。
- 提交后验证文件并报告 branch/base SHA/commit SHA/changed paths/决策状态。

【禁止】
不得代替 I 定义权限策略；不得代替 D 定义存储机制；不得在 ADR 未批准时要求 D/E/F/G 冻结 Schema。
```

---
