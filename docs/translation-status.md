# Bilingual Documentation Coverage & Migration Plan / 双语文档覆盖与迁移计划

- Document ID: DOC-STATUS-001
- Version: 1.0
- Status: Active documentation work plan
- Tracking branch: docs/bilingual-architecture

## 1. Purpose / 目的

This file tracks which architecture materials have equivalent Chinese and English reading versions. It prevents a partial translation effort from being mistaken for full bilingual coverage.

本文件跟踪架构资料的中英文对应情况，避免把第一批双语总览误认为全仓库文档已经完成双语化。

## 2. Coverage status / 覆盖状态

| Area | Source of detailed specification | Chinese guide/spec | English guide/spec | Status |
|---|---|---|---|---|
| Documentation portal | docs/README.md | Shared bilingual portal | Shared bilingual portal | COMPLETE |
| Documentation style | docs/documentation-style-guide.md | Bilingual | Bilingual | COMPLETE |
| Shared glossary | docs/glossary/architecture-glossary.md | Bilingual | Bilingual | COMPLETE |
| System overview | 01-system-architecture/system-overview.md | docs/zh-CN/01-system-architecture/system-overview.md | docs/en/01-system-architecture/system-overview.md | COMPLETE |
| Technology overview | 13-engineering-decisions/technology-architecture-blueprint.md + TAR-AI-001 | docs/zh-CN/13-engineering-decisions/technology-architecture-overview.md | docs/en/13-engineering-decisions/technology-architecture-overview.md | COMPLETE — overview only |
| Bilingual documentation policy | 00-governance/bilingual-documentation-policy.md | Embedded bilingual normative policy | Embedded bilingual normative policy | COMPLETE |
| Architecture invariants | 00-governance/architecture-invariants.md | docs/zh-CN/00-governance/architecture-invariants.md | docs/en/00-governance/architecture-invariants.md | COMPLETE |
| Canonical terminology | 00-governance/terminology.md | docs/zh-CN/00-governance/terminology.md | docs/en/00-governance/terminology.md | COMPLETE |
| System component map | 01-system-architecture/component-map.md | docs/zh-CN/01-system-architecture/component-map.md | docs/en/01-system-architecture/component-map.md | COMPLETE |
| Subsystem responsibility matrix | 01-system-architecture/responsibility-matrix.md | docs/zh-CN/01-system-architecture/responsibility-matrix.md | docs/en/01-system-architecture/responsibility-matrix.md | COMPLETE |
| Domain Model reader guide | 02-domain-model/ | docs/zh-CN/02-domain-model/domain-model-guide.md | docs/en/02-domain-model/domain-model-guide.md | COMPLETE — overview guide only |
| Domain Model detailed contracts (6 source specifications) | 02-domain-model/ | Pending | Existing English sources | NOT STARTED — field-level translation pending |
| Canonical Memory Brain (D) | 03-memory-brain/ | Pending | Existing English sources | NOT STARTED |
| Memory Compiler (E) | 04-memory-compiler/ | Pending | Existing English sources | NOT STARTED |
| Memory Runtime (F) | 05-memory-runtime/ | Pending | Existing English sources | NOT STARTED |
| Memory Context (G) | 06-memory-context/ | Pending | Existing English sources | NOT STARTED |
| Agent Integration (C) | 07-agent-integration/ | Pending | Existing English sources | NOT STARTED |
| BMCP Protocol (H) | 08-protocols/ | Pending | Existing English sources | NOT STARTED |
| Storage and Index | 09-storage-and-index/ | Pending | Existing English sources | NOT STARTED |
| Security and Governance (I) | 10-security-and-governance/ | Pending | Existing English sources | NOT STARTED |
| Consistency and Recovery | 11-consistency-and-recovery/ | Pending | Existing English sources | NOT STARTED |
| Testing and Acceptance | 12-testing-and-acceptance/ | Pending | Existing English sources | NOT STARTED |
| Detailed technology and Rust engineering | 13-engineering-decisions/ | Pending | Existing English sources | NOT STARTED |

## 3. Translation and readability sequence / 翻译与易读性推进顺序

### Batch 1 — Orientation and shared language / 第一批：系统认知与共同语言
- Portal, style guide, glossary.
- System overview in both languages.
- Technology overview in both languages.
- Status: COMPLETE.

### Batch 2 — Governance and system map / 第二批：治理基线与系统地图
- Status: COMPLETE.
- GOV-DOC-001 adopted in the proposed governance change set; effective as a repository requirement upon merge into the approved main baseline.
- Architecture principles, invariants, terminology source reconciliation.
- Component map, responsibility matrix, system workflows.
- Deliverables: paired Chinese/English documents and cross-links.
- Acceptance: no owner or authority boundary changes; glossary parity checked.

### Batch 3 — Domain and canonical memory / 第三批：领域模型与权威记忆
- Domain Model reader guide: COMPLETE.
- Detailed B source specifications: NOT STARTED; retain exact field/state semantics during translation.
- D Canonical Memory detailed bilingual work: pending source-branch reconciliation.
- B Domain Model.
- D Canonical Memory, lifecycle, versioning, Forget Fence, commit cursor.
- Acceptance: Fact/Claim OPEN state preserved; exact identifiers and state names unchanged.

### Batch 4 — Memory production and runtime / 第四批：记忆生产与运行时
- E Compiler, ingestion, extraction, evidence, consolidation.
- F retrieval, activation, working set, scheduling, anti-resurrection.
- Acceptance: Accepted/Compiled/Canonical Committed/Indexed remain distinct; cursor and Forget semantics stay aligned.

### Batch 5 — Context and Agent boundary / 第五批：上下文与 Agent 边界
- G Context Manager, versioning, edit operations, reconciliation, budget.
- H BMCP schemas and state machines.
- C Adapter integration and inference-boundary Applied proof.
- Acceptance: ContextVersion, Delivery, Applied, PermissionEpoch, and ForgetFenceGeneration remain distinct.

### Batch 6 — Governance, storage, and recovery / 第六批：治理、存储与恢复
- I identity, authorization, Forget, retention, audit.
- Storage/index/cache.
- Consistency/Recovery and COC.
- Acceptance: no logical design is described as implemented or physically verified without evidence.

### Batch 7 — Engineering, tests, and acceptance / 第七批：工程、测试与验收
- Rust crate architecture, technology ADRs, deployment, resource budgets.
- Test plans, conformance vectors, fault injection, benchmarks.
- Acceptance: candidate technologies remain candidates until ADR and evidence gates are met.

## 4. Definition of done / 完成定义

A document is not bilingual-complete merely because it has been translated. Each paired document must satisfy:

1. Same document ID and compatible semantic version.
2. Same section structure for equivalent content.
3. Same normative force: MUST/SHOULD/MAY and DECIDED/CANDIDATE/OPEN/TO_VALIDATE.
4. Same technical identifiers, enum values, field names, state transitions, and examples.
5. Same caveats, failure modes, security boundaries, and non-guarantees.
6. Reciprocal links between language versions.
7. Internal links and Mermaid diagrams validated.
8. Readability review by a reader who did not author the source.
9. Owner review where wording could affect a normative contract.
10. Exact source revision and review evidence recorded.

## 5. Change-control rule / 变更控制

- Translation is not an architecture decision.
- If the source contract changes, update both language versions in the same change set.
- If only one language can be updated immediately, mark the other STALE and record the source revision it has not yet incorporated.
- Never resolve an OPEN issue by choosing more definitive wording in translation.
- Keep a distinction between explanatory guides and normative owner specifications.

## 6. Current limitation / 当前限制

Batches 1 and 2 provide the orientation, shared language, governance invariants, component map, and responsibility matrix. This is still not a full translation of all subsystem specifications. Root-level Owner documents remain the detailed source specifications until their paired bilingual versions are completed and reviewed. The mandatory bilingual policy is proposed in this change set and becomes effective as an approved governance baseline when merged.
