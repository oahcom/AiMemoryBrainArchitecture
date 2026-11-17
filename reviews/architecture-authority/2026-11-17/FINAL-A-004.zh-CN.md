# FINAL-A-004 — 当前 Main 基线更正与独立审查补充

- 权威：A 集成评估；不替代任何 Owner 权威。
- 日期：2026-11-17
- 本补充锁定的 Main 当前 HEAD：`901e38ba7b45ed1822eaefddc2da8d765cf8985c`
- 父提交：`ca69d50d1fc6c19a930128de700b0f2328bf32fb`
- 变更：`revert(domain): remove research-only bilingual audit from main`
- A 审查分支：`review/session-4-a-final-architecture-authority-current-2026-11-17`
- 替代范围：FINAL-A-004 仅在当前 Main 时效性和 B 审计文件可用性方面取代 FINAL-A-003；不抹除此前发现或 Owner 决策。

## 1. 基线更正

此前 FINAL-A-003 的基线 `ca69d50d1fc6c19a930128de700b0f2328bf32fb` 已不再是当前版本。Main 当前指向 `901e38ba7b45ed1822eaefddc2da8d765cf8985c`。

最新提交恰好删除以下文件：
`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md`
（131 行；提交文件状态为 removed）。

此前记录的审计 Blob `a877ceff906da01e70e277a81b95978982af3ede` 现在仅属于历史证据。该文件已不在当前 Main 中，不得将其描述为当前 Main 源工件或当前 B5 关闭证据。

## 2. B5 与 G6 裁决

- B5 仍为 **BLOCKED / NOT PASSED**。审计文件被删除并不能证明底层双语缺陷已经修复；它意味着该审计文件已从当前 Main 证据集中撤回。
- 只有在历史 Commit 上精确回读后，才可将此前审计 Blob 作为历史背景参考。它不能证明当前源状态、B Owner 接受、消费者采用或独立语义对等。
- Issue #43 G6 仍为 **PARTIAL / NOT PASSED**。A 全套文件的语义对等审查尚未完成，也不得推定全系统独立双语验收通过。
- 除非 B 发布当前权威决策且消费者接受其精确版本，否则 B Fact/Claim 仍为 ADR-BLOCKED。
- 不得混淆 B5（B 研究包门禁）与 Issue #43 G6（全系统双语门禁）。

## 3. A 文件包时效性与审查边界

本 PR 中十份 A 文档（20 个中英文文件）保留其历史内部基线 Pin。不得静默改写这些 Pin：该文件包按其记录的基线编写，FINAL-A-003 是后续增量。现在 FINAL-A-004 是本次审查中控制当前 Main 增量的文件。

本轮已执行的独立审查：
- 重新读取 PR #60 实时元数据及全部 22 个变更文件条目。
- 从 A 精确审查分支读取 SYS-RISK-002、ARCH-CX-002、DEV-FEAS-002、DEP-DAG-002、PRIORITY-002、READINESS-002、CONFLICT-002、GATE-002、DEFERRED-002 和 FINAL-A-002 的中英文配对文件。
- 确认十组文件保留了匹配的文档身份和总体决策结构。
- 发现时效漂移：十份基线文件及 FINAL-A-002 仍标记 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`；FINAL-A-003 标记 `ca69d50d1fc6c19a930128de700b0f2328bf32fb`；二者相对当前 Main `901e38...` 均已成为历史版本。
- 尚未完成逐句语义对等、每个表格单元格及跨文档状态/Owner/期限的一致性审计。结构相似不等于语义等价证明。

## 4. R/X/F/D/P 刷新依赖

PR #62 按 `ca69d50d1fc6c19a930128de700b0f2328bf32fb` 编写，且其增量引用了现在已删除的 B 审计文件。它不再构成针对 `901e38...` 的完整当前 Main 刷新。

所需纠正：
1. 将 PR #62 原十份文件重新分类为针对 ca69d50 的历史增量。
2. 发布针对 main@901e38 的中英文后继增量，明确记录 B 审计文件删除及其造成的 B5 证据限制。
3. R/X/F/D/P 结论必须受限于实际重新读取的精确源证据；不得声称历史审计仍是当前证据。
4. A 在精确 Blob 回读后，才可更新 G1/G6/G7。

## 5. 控制性裁决与 Gate

整体决策仍为 **DEFERRED**；架构状态仍为 **ARCHITECTURE_NOT_READY**。

- G1：PARTIAL；已识别当前 Main，但尚未完整刷新所有权威源/消费者 Pin。
- G2–G5：BLOCKED。
- G6：PARTIAL / NOT PASSED。
- G7：仅为候选 A 集成裁决；独立接受仍待完成。
- G8：NOT READY。
- JF-10 Gate A：PARTIAL PASS / OPEN；Gate B、Gate C：BLOCKED。
- 不接受、不豁免任何 Critical 风险。
- COND-NB-01 仍是唯一接受的非阻塞能力延期，仅限 Vector/ANN 生产能力，归 F 负责，并遵守已记录的 P2 关闭标准。
- 不授权实现冻结、Schema/Technology Freeze、合并、Gate 放行、部署或生产激活。

## 6. 必需的后续证据

| 事项 | 责任 Owner | 必需证据 | Gate 边界 |
|---|---|---|---|
| 当前 B 研究/领域源与 B5 | B | 当前分支 HEAD、精确源 Blob、完成双语整改、独立逐条/逐行对等、B Owner 决策 | 任何依赖 B 的规范冻结前；B5 |
| R/X/F/D/P 当前 Main 后继增量 | R/X/F/D/P 作者；A 集成 | 针对 main@901e38 的双语后继文件，并绑定全部精确源 Blob | G1/G6/G7 |
| A 文件包语义对等 | 独立审查者 | 覆盖 20 个文件及 FINAL-A-003/004 的条款/表格/状态/ID/Owner/期限对等矩阵 | G6 |
| Owner/消费者接受 | 各领域 Owner | 精确版本决策及消费者采用证据 | G2 |
| 物理正确性与运维 | D/I/Storage/C/G/H 及项目权威 | Forget/Publication、JF-10、Applied、Recovery、拓扑和生产运维证明 | G3–G5；JF-10 |

对于尚无责任 Owner 接受的事项，不虚构日历截止日期。必须在依赖它的规范决策、Schema Freeze、实现准入或 Gate 转换前关闭。

## 7. 权威边界

本补充是集成审查更正，不是 B Owner 决策，不替代 R/X/F/D/P 源作者批准，也不是外部独立验收。它不授权修改 Main 或 Owner 分支。