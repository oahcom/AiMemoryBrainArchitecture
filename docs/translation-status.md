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
| System design principles/interactions/flows/boundaries/quality reader guide | 00-governance/ and 01-system-architecture/ | docs/zh-CN/01-system-architecture/system-design-guide.md | docs/en/01-system-architecture/system-design-guide.md | COMPLETE — synthesis guide only |
| Principal Integration / contract governance guide (A) | A owner branch: reviews/integration/ | docs/zh-CN/01-system-architecture/integration-governance-guide.md | docs/en/01-system-architecture/integration-governance-guide.md | COMPLETE — reader guide only |
| Detailed design principles, component interactions, data flows, boundaries, quality attributes | Source specifications under 00-governance/ and 01-system-architecture/ | Pending | Existing English sources | NOT STARTED — full source-level translation pending |
| Subsystem responsibility matrix | 01-system-architecture/responsibility-matrix.md | docs/zh-CN/01-system-architecture/responsibility-matrix.md | docs/en/01-system-architecture/responsibility-matrix.md | COMPLETE |
| Domain Model reader guide | 02-domain-model/ | docs/zh-CN/02-domain-model/domain-model-guide.md | docs/en/02-domain-model/domain-model-guide.md | COMPLETE — overview guide only |
| Domain Model detailed contracts (6 source specifications) | 02-domain-model/ | Pending | Existing English sources | NOT STARTED — field-level translation pending |
| Canonical Memory Brain reader guide | D owner branch: 03-memory-brain/ | docs/zh-CN/03-memory-brain/memory-brain-guide.md | docs/en/03-memory-brain/memory-brain-guide.md | COMPLETE — overview guide only |
| Canonical Memory Brain detailed contracts (7 source specifications) | D owner branch: 03-memory-brain/ | Pending | Owner-branch English sources | NOT STARTED — detailed translation pending |
| Memory Compiler reader guide | E owner branch: 04-memory-compiler/ | docs/zh-CN/04-memory-compiler/memory-compiler-guide.md | docs/en/04-memory-compiler/memory-compiler-guide.md | COMPLETE — overview guide only |
| Memory Compiler detailed contracts | E owner branch: 04-memory-compiler/ | Pending | Owner-branch English sources | NOT STARTED — field/stage-level translation pending |
| Memory Runtime reader guide | F owner branch: 05-memory-runtime/ | docs/zh-CN/05-memory-runtime/memory-runtime-guide.md | docs/en/05-memory-runtime/memory-runtime-guide.md | COMPLETE — overview guide only |
| Memory Runtime detailed contracts | F owner branch: 05-memory-runtime/ | Pending | Owner-branch English sources | NOT STARTED — field/policy-level translation pending |
| Memory Context reader guide | G owner branch: 06-memory-context/ | docs/zh-CN/06-memory-context/memory-context-guide.md | docs/en/06-memory-context/memory-context-guide.md | COMPLETE — overview guide only |
| Memory Context detailed contracts | G owner branch: 06-memory-context/ | Pending | Owner-branch English sources | NOT STARTED — detailed state/field translation pending |
| Agent Integration reader guide | C owner branch: 07-agent-integration/ | docs/zh-CN/07-agent-integration/agent-integration-guide.md | docs/en/07-agent-integration/agent-integration-guide.md | COMPLETE — overview guide only |
| Agent Integration detailed contracts | C owner branch: 07-agent-integration/ | Pending | Owner-branch English sources | NOT STARTED — detailed capability/telemetry translation pending |
| BMCP Protocol reader guide | H owner branch: 08-bmcp-protocol/ | docs/zh-CN/08-bmcp-protocol/bmcp-guide.md | docs/en/08-bmcp-protocol/bmcp-guide.md | COMPLETE — overview guide only |
| BMCP Protocol detailed contracts | H owner branch: 08-bmcp-protocol/ | Pending | Owner-branch English sources | NOT STARTED — wire/schema translation pending |
| Storage and Index | 09-storage-and-index/ | Pending | Existing English sources | NOT STARTED |
| Security & Governance reader guide | I owner branch: 09-security-governance/ | docs/zh-CN/09-security-governance/security-governance-guide.md | docs/en/09-security-governance/security-governance-guide.md | COMPLETE — overview guide only |
| Security & Governance detailed contracts | I owner branch: 09-security-governance/ | Pending | Owner-branch English sources | NOT STARTED — policy/identity/Forget detail translation pending |
| Consistency and Recovery | 11-consistency-and-recovery/ | Pending | Existing English sources | NOT STARTED |
| Cross-module conformance and fault-injection reader guide | A owner branch: reviews/integration/cross-module-conformance-plan.md | docs/zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md | docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md | COMPLETE — test guide only; execution NOT_RUN/BLOCKED |
| Detailed Testing and Acceptance specifications/reports | 12-testing-and-acceptance/ and reviews/ | Pending | Existing English sources | NOT STARTED — detailed test cases and review reports pending |
| Detailed technology and Rust engineering | 13-engineering-decisions/ | Pending | Existing English sources | NOT STARTED |

## 3. Translation and readability sequence / 翻译与易读性推进顺序

### Batch 1 — Orientation and shared language / 第一批：系统认知与共同语言
- Portal, style guide, glossary.
- System overview in both languages.
- Technology overview in both languages.
- Status: COMPLETE.

### Batch 2 — Governance and system map / 第二批：治理基线与系统地图
- Status: COMPLETE for reader guides and core maps.
- Detailed component interactions, data flows, boundaries, and quality-attribute source documents: NOT STARTED — full source-level bilingual versions remain pending.
- GOV-DOC-001 adopted in the proposed governance change set; effective as a repository requirement upon merge into the approved main baseline.
- Architecture principles, invariants, terminology source reconciliation.
- Component map, responsibility matrix, system workflows.
- Deliverables: paired Chinese/English documents and cross-links.
- Acceptance: no owner or authority boundary changes; glossary parity checked.

### Batch 3 — Domain and canonical memory / 第三批：领域模型与权威记忆
- D Canonical Memory reader guide: COMPLETE — includes D/E/F/G/H/I ownership split, cursor namespaces, and Forget boundary.
- D detailed source specifications: NOT STARTED — source branch is linked; field/transaction-level translation pending.
- Domain Model reader guide: COMPLETE.
- Detailed B source specifications: NOT STARTED; retain exact field/state semantics during translation.
- D Canonical Memory detailed bilingual work: pending source-branch reconciliation.
- B Domain Model.
- D Canonical Memory, lifecycle, versioning, Forget Fence, commit cursor.
- Acceptance: Fact/Claim OPEN state preserved; exact identifiers and state names unchanged.

### Batch 4 — Memory production and runtime / 第四批：记忆生产与运行时
- E and F reader guides: COMPLETE.
- Detailed E/F owner specifications: NOT STARTED — field-level translation and owner parity review remain pending.
- E Compiler, ingestion, extraction, evidence, consolidation.
- F retrieval, activation, working set, scheduling, anti-resurrection.
- Acceptance: Accepted/Compiled/Canonical Committed/Indexed remain distinct; cursor and Forget semantics stay aligned.

### Batch 5 — Context and Agent boundary / 第五批：上下文与 Agent 边界
- G Context, C Agent Integration, and H BMCP reader guides: COMPLETE.
- Detailed G/C/H contracts: NOT STARTED — schemas, state machines, capability tiers, and proof fields remain to be translated.
- G Context Manager, versioning, edit operations, reconciliation, budget.
- H BMCP schemas and state machines.
- C Adapter integration and inference-boundary Applied proof.
- Acceptance: ContextVersion, Delivery, Applied, PermissionEpoch, and ForgetFenceGeneration remain distinct.

### Batch 6 — Governance, storage, and recovery / 第六批：治理、存储与恢复
- I Security & Governance reader guide: COMPLETE.
- Detailed I policies and contracts: NOT STARTED — principal, authorization, Forget target inventory, backup/erasure and threat model remain to be translated.
- I identity, authorization, Forget, retention, audit.
- Storage/index/cache.
- Consistency/Recovery and COC.
- Acceptance: no logical design is described as implemented or physically verified without evidence.

### Batch 7 — Engineering, tests, and acceptance / 第七批：工程、测试与验收
- Cross-module conformance reader guide: COMPLETE.
- Test execution remains NOT_RUN/BLOCKED until implementations and dependencies exist; no PASS is claimed.
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

A integration governance and conformance reader guides are available in both languages. The detailed A registry, complete test catalogue, and Owner-specific review reports remain to be translated as source-level documents.

Batches 1 and 2 provide the orientation, shared language, governance invariants, component map, and responsibility matrix. This is still not a full translation of all subsystem specifications. Root-level Owner documents remain the detailed source specifications until their paired bilingual versions are completed and reviewed. The mandatory bilingual policy is proposed in this change set and becomes effective as an approved governance baseline when merged.
