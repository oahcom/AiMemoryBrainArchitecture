# 简化任务提示词模板 v2

- Template ID：AI-PROMPT-TPL-002
- Version：2.0
- Status：PROPOSED — 需要治理采纳
- English counterpart / 英文对应文件：[TEMPLATE-v2.md](TEMPLATE-v2.md)

> 七项核心要素指七个结构章节，而非七个元数据字段。本模板简化提示词组织方式，不改变权限、验证、双语、安全或验收门禁。

## 1. Task identity / 任务标识
- **Work Item ID：** [WI-ID]
- **Prompt ID / Version：** [PROMPT-ID] v[VERSION]
- **Accountable Owner：** [A–I / 指定跨领域 Owner]
- **Implementer：** [会话/角色]
- **Independent Reviewer：** [会话/角色；如待定，填写 PENDING 和原因]
- **Repository：** [owner/repository]
- **Branch：** [分支]
- **Task Class / Risk：** [ARCH / IMPL / TEST / SEC / MIG / PERF / DOC / OPS] / [R0–R3]
- **Owning Issue / PR：** [URL，或 NOT_CREATED + 原因]

## 2. Goal and boundaries / 目标与边界
**What — 做什么：** [可观察的任务目标。]

**Why — 为什么：** [动机、影响和决策背景。]

**Out of Scope — 不做什么：**
- [明确的非目标。]
- [排除的文件、模块、决策或操作。]

## 3. Context and dependencies / 上下文与依赖
- **Base：** [基线分支] @ [完整 Commit SHA]
- **Required sources：** [准确路径 + 版本/状态 + Blob SHA 或 Commit SHA]
- **Dependency contracts：** [Owner + 契约 + 准确修订；或 NONE]
- **Applicable global/Owner prompts：** [Prompt ID 和路径]
- **Bilingual sources：** [适用时受影响的中英文路径及源版本]
- **State of knowledge：** [DECIDED / CANDIDATE / OPEN / TO_VALIDATE 事实及准确来源]

如果必需来源、版本、审批或依赖不可用或相互冲突，应在该边界停止并报告，不得自行推断。

## 4. Constraints and execution guidance / 约束与执行指导
**Mandatory constraints / 强制约束**
- [规范规则、不变式、信任边界和兼容性要求。]
- [权限边界：允许修改的文件/模块，以及禁止跨 Owner 作出的决策。]
- 阅读并遵守 GOV-DOC-001 及适用的全局/Owner 提示词。改变架构语义的变更必须在同一变更集中提供中英文对应版本，除非存在正式批准且有期限的 STALE 例外。
- 安全、故障、并发、恢复、隐私和兼容性分析 MUST 在任务类别/风险等级对应的生命周期门禁执行。本模板不豁免这些审查。

**Required execution sequence / 必需执行步骤**
1. 检查已固定的来源和依赖。
2. 在授权范围内制定计划并记录未决知识状态。
3. 执行获准的变更。
4. 运行适用验证并记录准确结果。
5. 报告交付物、证据、阻塞和交接。

**Recommended steps / 推荐步骤**
- [可调整的设计/实现顺序或额外交接细节；除非明确标为 MUST，否则属于建议。]

## 5. Acceptance and deliverables / 验收与交付物
**Observable acceptance criteria / 可观测验收条件**
- [ ] [客观条件、证据位置和通过规则。]
- [ ] [客观条件、证据位置和通过规则。]

**Required deliverables / 必需交付物**
- [代码/文档/配置/报告路径。]
- [决策记录、双语清单或其他适用工件。]
- [列出不适用项目及原因。]

验收标准定义完成条件。工件存在本身不能证明其正确或已获批准。

## 6. Evidence and review / 证据与审查
**P0 — mandatory minimum evidence / 必需最低证据**
- 准确执行的 Prompt ID/版本，以及不可变提示词快照的 SHA-256；记录在 Work Item manifest 中。不得伪造缺失摘要。
- Base SHA、实现 Commit SHA、最终分支 Head SHA 和准确的变更文件清单。
- 变更工件的读回确认。
- 带证据链接的验收标准处置，以及所属 Issue/PR 的收尾记录。
- 治理要求适用时，记录独立审查结论和授权验收记录。

**P1 — applicable verification evidence / 适用验证证据**
- 准确测试/检查命令、环境、被测 Commit SHA、预期/实际结果及证据链接。
- 不可用或不适用的检查标记为 NOT RUN / NOT APPLICABLE 并说明原因；不得暗示通过。
- R2/R3、安全、数据完整性、迁移、并发、恢复及其他适用政策仍保留完整测试/审查证据。P1 不是豁免。

**Git workflow / Git 流程**
- Branch / Base SHA： [分支 @ 完整基线 SHA]
- Commit and PR target： [提交计划 / PR 目标]
- Review handoff： [独立审查者及必需证据]
- Merge rule： [除非另行授权，否则 NO MERGE]

**Review level：** [R0 / R1 / R2 / R3]  
**Bilingual parity evidence：** [适用时的中英文路径、源版本、审查者和结果。]

## 7. Stop conditions and coordination / 停止条件与协调
**Stop and escalate when / 出现以下情况时停止并升级**
- [缺少或冲突的必需权限、审批、来源或依赖。]
- [变更跨越 Owner 边界或威胁不变式。]
- [验收无法验证或出现意外范围。]

**Escalation / coordination / 升级与协调**
- **Decision Owner：** [指定 Owner / 权限主体]
- **Tracking route：** [Issue/PR、受影响 Owner、所需决策]
- **Resume condition：** [继续工作前必须满足的客观条件]

## 使用说明
- 保留七个章节；缺失内容使用 NONE、NOT APPLICABLE 或 PENDING + 原因，不得编造。
- 对准确、不可变的已执行提示词快照计算 SHA-256，并存入 Work Item 证据包/manifest。不得在被哈希字节中加入自引用摘要。
- 本提示词不能替代 Work Item manifest、必需全局提示词、GOV-DOC-001、AI-STD-001、ADR 或 GitHub Issue/PR。
- AI-PROMPT-STD-001 §4 的十二项强制内容要素仍全部适用，并按该规范的映射表嵌入七个章节；不得将十二项另行扩展为十二个顶层章节。
- 已执行 v1 提示词继续有效且不可变。仅为新执行/新版本迁移；不得原位改写已执行提示词。
