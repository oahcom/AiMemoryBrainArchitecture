# 提示词 v1 → v2 迁移指南

- Guide ID：AI-PROMPT-MIGRATION-001
- Version：1.0
- Status：PROPOSED — 需要治理采纳
- English counterpart / 英文对应文件：[MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)

## 1. 迁移政策
v2 将历史模板的 15 个强制标题压缩为七个核心章节。结构压缩不删除适用的治理义务、证据、审批或历史记录。AI-PROMPT-STD-001 §4 的十二项强制内容要素全部保留，并嵌入七章节，不再作为额外的顶层标题。

- 已执行的 v1 提示词继续有效且不可变。
- 不得批量重写活动中的提示词。只有在需要且获准进行新执行/新版本时，才创建 v2 副本。
- 保留原始提示词、版本、SHA-256、Issue/PR 链接、提交、审查和验收记录。
- 如果源字节或历史摘要无法验证，记录 NOT_VERIFIED；不得猜测。
- 七章节是提示词布局。Work Item manifest、证据包、全局提示词、GOV-DOC-001 和会话收尾仍然适用。

## 2. 旧新映射
| v2 核心章节 | 合并的 v1 要素 | 迁移规则 |
|---|---|---|
| 1. Task identity / 任务标识 | 1、3、4（身份/角色/仓库） | 合并 Work Item、Prompt ID/版本、Owner、实现者、审查者、仓库/分支、类别/风险和 Issue/PR 载体。Base/依赖 SHA 放在第 3 节。 |
| 2. Goal and boundaries / 目标与边界 | 2、6 | 写明 What、Why 和明确的 Out of Scope。 |
| 3. Context and dependencies / 上下文与依赖 | 4、5 | 记录准确 Base SHA、源路径/修订和依赖契约；标记 DECIDED/CANDIDATE/OPEN/TO_VALIDATE。 |
| 4. Constraints and execution guidance / 约束与执行指导 | 7、8、适用的 11、14 | 区分强制不变式/权限与可调整的推荐步骤，并保留必需执行顺序。 |
| 5. Acceptance and deliverables / 验收与交付物 | 9、12、适用的 15 | 定义可观测完成条件和交付物，包括 GOV-DOC-001 适用时的双语路径/清单。 |
| 6. Evidence and review / 证据与审查 | 1（提示词摘要）、10、13、适用的 12/15 | 保留 Prompt SHA-256、Commit/Head/变更路径/读回/验收证据、测试、审查和最终报告格式。 |
| 7. Stop conditions and coordination / 停止条件与协调 | 14 | 保留停止、升级、决策 Owner、协调和恢复条件。 |

## 3. 迁移但不豁免
### 安全、故障、并发、恢复和兼容性
这些要求并未从治理中删除。提示词不再要求在任务尚未明确时提前穷尽推测性分析。Owner 应在设计、实现、验证和审查等适当门禁处理适用风险。R2/R3 以及安全/数据完整性要求保持不变。

### 双语文档
双语工作由 GOV-DOC-001 和 GLB-DOC-001 管理，而不是通过额外的第十五个标题管理。提示词仍必须在架构语义发生变化时标识受影响的中英文路径，将双语工作纳入范围/验收，并提供一致性证据。缺失对应版本仍为 NOT DONE，除非存在正式批准且有期限的 STALE 例外。

### 测试与证据
P0/P1 是适用性分类，不是跳过必需检查的许可。架构探索早期可以暂未确定具体命令，但在验证门禁前必须明确。每项已执行检查均记录被测 SHA 和结果。未运行的必需检查标记为 NOT RUN，不得标记 PASS。

### SHA-256 与 Git 可追溯性
在有要求时，Git commit/blob 标识不能替代准确执行提示词快照的 SHA-256。将提示词摘要存入 Work Item manifest/证据包。Commit SHA、最终 Head SHA、变更路径、读回、审查和验收记录仍是 P0。

## 4. 迁移步骤
1. 识别源提示词并核实 Work Item、Owner、执行状态、源版本和历史摘要。
2. 保持源文件不变。仅为新/获准执行创建新的 v2 工件，并链接到源版本。
3. 按映射表迁移字段。将每项要求分类为：保留在核心章节、由全局政策管理、有理由地不适用，或仍未解决。
4. 重新检查 Owner 权限、允许/禁止路径、依赖 SHA、可观测验收、证据和停止条件。
5. 检查 GOV-DOC-001 适用性、成对路径、双语 manifest 和覆盖登记。
6. 在执行前，对新提示词准确字节计算并独立核验 SHA-256，记录到 manifest。
7. 获取必需的提示词审查和 Owner 授权。只有适用的 Ready 门禁通过后才能开始。

## 5. 试点迁移
示例源自准确的历史 T2 派发载荷快照，而不是仓库中的 T1 prompt-v1.md 工件：

- Source payload：14-ai-development/work-items/AID-2026-003/t2-snapshot-fix-prompt.source.txt
- Source blob：a274aa761074683b0fd6a7aadcfe917b140fc227
- Source type：逐字 T2 已发送载荷快照，9,807 个 Unicode 字符；归档于 Commit d84dcbe269706bec384b02f24de6a0e635da9aa0。
- Dispatch record：按 AID-2026-003 manifest 记录，于 2026-11-18 20:52:09 +08:00 派发至会话 6afd9f7f-d544-83ee-98d1-92d7aafb3bcf。

该载荷快照不同于 14-ai-development/work-items/AID-2026-003/prompt-v1.md（Blob 71332a2b8f412d1bb58d4d53bdb25880dc2f1431）。该 T1 仓库提示词不是本试点的来源。不得混淆 T2 派发快照与 T1 仓库提示词。

work-item-003-v2-migration-example.md 是仅根据上述 T2 快照制作的回顾性、非执行示例。它不会取代或修改任一历史工件，不会重新打开 AID-2026-003，也不代表 Owner 批准。由于该示例未获准执行，其 executed-prompt SHA-256 为 NOT APPLICABLE。

## 6. 迁移检查表
- [ ] 已核实源提示词和历史身份；源文件保持不变。
- [ ] 已分配新的 Prompt ID/版本；已记录与源版本的关系。
- [ ] 已填充七个章节；未丢失任何必需权限/约束。
- [ ] Base/依赖引用和准确源路径均为当前版本。
- [ ] 验收条件可观测且有证据位置。
- [ ] P0 可追溯性和适用的 P1 验证得到保留。
- [ ] GOV-DOC-001 和双语 manifest 要求已满足。
- [ ] 适用的安全、故障、并发、恢复和兼容性门禁得到保留。
- [ ] 已从准确字节计算提示词摘要，并在执行前记录。
- [ ] 已记录必需审查和 Owner 授权。
