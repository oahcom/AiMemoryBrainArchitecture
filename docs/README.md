> **🎨 当前阶段：架构设计** - 正在完善架构规范,试点项目 ai-memory-adapter 已启动 MVP 开发

---


**这些文档是架构的权威定义,开发必须遵循**

| 目录 | 说明 | 入口 |
|------|------|------|
| `en-US/` | 英文规范性文档 | [📖 English Docs](./en-US/README.md) |
| `zh-CN/` | 中文规范性文档 | [📖 中文文档](./zh-CN/README.md) |

**核心规范**:
- [AID-2026-000: Architecture Decision Records](./en-US/AID-2026-000-architecture-decision-records.md) - ADR 规范
- [MVP Architecture Decisions](./MVP-ARCHITECTURE-DECISIONS.md) - 试点项目最小可用架构

---


**这些是待评审的架构方案,非规范性文档,不可直接实现**

| 目录 | 说明 |
|------|------|
| `architecture-convergence/` | 候选架构文档集 + 进度追踪 |

⚠️ **警告**: 候选架构文档正在评审中,不代表最终决策。查看 [收敛进度追踪](./architecture-convergence/STATUS-TRACKER.md)

---


| 目录 | 说明 |
|------|------|
| `governance/` | 文档治理、审计报告、归档 |
| `templates/` | ADR 和文档模板 |

---


**开发者**:
- **试点项目开发** → [MVP Architecture Decisions](./MVP-ARCHITECTURE-DECISIONS.md)
- **提交新 ADR** → [模板](./templates/aid-template.md)
- **查看规范** → [中文文档](./zh-CN/README.md) / [English Docs](./en-US/README.md)

**架构师**:
- **候选架构评审** → [architecture-convergence/](./architecture-convergence/)
- **收敛进度** → [STATUS-TRACKER.md](./architecture-convergence/STATUS-TRACKER.md)
- **文档治理** → [governance/](./governance/)

---


```
候选架构 → 评审 → 规范性文档 → 实现 → 归档
   ↓                    ↓
待处理              开发依据
```

---


- [x] 建立 ADR 规范 (AID-2026-000)
- [x] MVP 架构裁决 (2026-11-20)
- [x] 文档治理体系建立 (2026-11-20)
- [ ] 候选架构收敛 (进行中)
- [ ] 试点项目验证 (ai-memory-adapter)

---


- 新架构决策 → 先创建候选架构,提交到 `architecture-convergence/`
- 修改规范性文档 → 必须通过评审,遵循 ADR 流程
- 翻译状态 → 查看 [governance/translation-status.md](./governance/translation-status.md)
