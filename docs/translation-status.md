# Bilingual Documentation Coverage & Migration Plan / 双语文档覆盖与迁移计划

- Document ID: DOC-STATUS-001
- Version: 1.0
- Status: Active documentation work plan
- Tracking branch: docs/bilingual-coverage-completion

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
| TAB-001 full technology blueprint | 13-engineering-decisions/technology-architecture-blueprint.md | Pending | Existing English source | NOT STARTED — full blueprint translation and technical parity review pending |
| Bilingual documentation policy | 00-governance/bilingual-documentation-policy.md | Embedded bilingual normative policy v1.1 | Embedded bilingual normative policy v1.1 | COMPLETE — mandatory duties for every AI developer/session; enforced through AI development standard and prompt template |
| Design principles source specification | 00-governance/design-principles.md | docs/zh-CN/00-governance/design-principles.md | docs/en/00-governance/design-principles.md | COMPLETE — source-aligned pair |
| System architecture source specification | 01-system-architecture/system-overview.md | docs/zh-CN/01-system-architecture/system-architecture-specification.md | docs/en/01-system-architecture/system-architecture-specification.md | COMPLETE — source-aligned pair; distinct from reader guide |
| Architecture invariants | 00-governance/architecture-invariants.md | docs/zh-CN/00-governance/architecture-invariants.md | docs/en/00-governance/architecture-invariants.md | COMPLETE |
| Canonical terminology | 00-governance/terminology.md | docs/zh-CN/00-governance/terminology.md | docs/en/00-governance/terminology.md | COMPLETE |
| System quality attributes source specification | 01-system-architecture/system-quality-attributes.md | docs/zh-CN/01-system-architecture/system-quality-attributes.md | docs/en/01-system-architecture/system-quality-attributes.md | COMPLETE — source-aligned pair |
| System boundary source specification | 01-system-architecture/system-boundaries.md | docs/zh-CN/01-system-architecture/system-boundaries.md | docs/en/01-system-architecture/system-boundaries.md | COMPLETE — source-aligned pair |
| System component map | 01-system-architecture/component-map.md | docs/zh-CN/01-system-architecture/component-map.md | docs/en/01-system-architecture/component-map.md | COMPLETE |
| System design principles/interactions/flows/boundaries/quality reader guide | 00-governance/ and 01-system-architecture/ | docs/zh-CN/01-system-architecture/system-design-guide.md | docs/en/01-system-architecture/system-design-guide.md | COMPLETE — synthesis guide only |
| Principal Integration / contract governance guide (A) | A owner branch: reviews/integration/ | docs/zh-CN/01-system-architecture/integration-governance-guide.md | docs/en/01-system-architecture/integration-governance-guide.md | COMPLETE — reader guide only |
| Component interaction source specification | 01-system-architecture/component-interactions.md | docs/zh-CN/01-system-architecture/component-interactions.md | docs/en/01-system-architecture/component-interactions.md | COMPLETE — source-aligned pair |
| System data flow source specification | 01-system-architecture/data-flows.md | docs/zh-CN/01-system-architecture/data-flows.md | docs/en/01-system-architecture/data-flows.md | COMPLETE — source-aligned pair |
| Subsystem responsibility matrix | 01-system-architecture/responsibility-matrix.md | docs/zh-CN/01-system-architecture/responsibility-matrix.md | docs/en/01-system-architecture/responsibility-matrix.md | COMPLETE |
| Domain Model reader guide | 02-domain-model/ | docs/zh-CN/02-domain-model/domain-model-guide.md | docs/en/02-domain-model/domain-model-guide.md | COMPLETE — overview guide only |
| Domain Model overview | 02-domain-model/domain-model-overview.md | docs/zh-CN/02-domain-model/domain-model-overview.md | docs/en/02-domain-model/domain-model-overview.md | COMPLETE — source-aligned pair |
| Core domain entities | 02-domain-model/core-entities.md | docs/zh-CN/02-domain-model/core-entities.md | docs/en/02-domain-model/core-entities.md | COMPLETE — source-aligned pair |
| Epistemic and temporal semantics | 02-domain-model/epistemic-and-temporal-semantics.md | docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md | docs/en/02-domain-model/epistemic-and-temporal-semantics.md | COMPLETE — source-aligned pair |
| Memory lifecycle model | 02-domain-model/lifecycle-model.md | docs/zh-CN/02-domain-model/lifecycle-model.md | docs/en/02-domain-model/lifecycle-model.md | COMPLETE — source-aligned pair |
| Relationships and provenance | 02-domain-model/relationships-and-provenance.md | docs/zh-CN/02-domain-model/relationships-and-provenance.md | docs/en/02-domain-model/relationships-and-provenance.md | COMPLETE — source-aligned pair |
| Scope and Permission model | 02-domain-model/scope-and-permission-model.md | docs/zh-CN/02-domain-model/scope-and-permission-model.md | docs/en/02-domain-model/scope-and-permission-model.md | COMPLETE — source-aligned pair |
| Domain Model Phase 3 identity/typed-reference extensions and ADR-001 | B Owner branch exact Blobs: typed-reference `e9a6bd21e06bc02a5208619f5a949217860b1c00`; Principal/Actor `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | docs/zh-CN/02-domain-model/typed-reference-and-scope-semantics.md; docs/zh-CN/02-domain-model/principal-actor-binding-mapping.md | docs/en/02-domain-model/typed-reference-and-scope-semantics.md; docs/en/02-domain-model/principal-actor-binding-mapping.md | PAIRED — two Phase 3 identity companions; ADR-001 remains ADR-BLOCKED and no identity freeze implied |
| Canonical Memory Brain reader guide | D owner branch: 03-memory-brain/ | docs/zh-CN/03-memory-brain/memory-brain-guide.md | docs/en/03-memory-brain/memory-brain-guide.md | COMPLETE — overview guide only |
| D Memory Brain overview | 03-memory-brain/memory-brain-overview.md | docs/zh-CN/03-memory-brain/memory-brain-overview.md | docs/en/03-memory-brain/memory-brain-overview.md | COMPLETE — source-aligned pair |
| D Canonical Memory Store | 03-memory-brain/canonical-memory-store.md | docs/zh-CN/03-memory-brain/canonical-memory-store.md | docs/en/03-memory-brain/canonical-memory-store.md | COMPLETE — source-aligned pair |
| D Memory Lifecycle Manager | 03-memory-brain/memory-lifecycle-manager.md | docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md | docs/en/03-memory-brain/memory-lifecycle-manager.md | COMPLETE — source-aligned pair |
| D Entity and Relationship Manager | 03-memory-brain/entity-and-relationship-manager.md | docs/zh-CN/03-memory-brain/entity-and-relationship-manager.md | docs/en/03-memory-brain/entity-and-relationship-manager.md | COMPLETE — source-aligned pair |
| D Memory Versioning | 03-memory-brain/memory-versioning.md | docs/zh-CN/03-memory-brain/memory-versioning.md | docs/en/03-memory-brain/memory-versioning.md | COMPLETE — source-aligned pair |
| D Canonical Commit Cursor Semantics | 03-memory-brain/commit-cursor-semantics.md | docs/zh-CN/03-memory-brain/commit-cursor-semantics.md | docs/en/03-memory-brain/commit-cursor-semantics.md | COMPLETE — source-aligned pair |
| D Forget Fence and Completion Contract | 03-memory-brain/forget-fence-and-completion-contract.md | docs/zh-CN/03-memory-brain/forget-fence-and-completion-contract.md | docs/en/03-memory-brain/forget-fence-and-completion-contract.md | COMPLETE — source-aligned pair |
| D Forget Fence Operation and Publication Gate | 03-memory-brain/forget-fence-operation-and-publication-gate.md | docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md + parts 1–4 | docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md + parts 1–4 | COMPLETE — long source split into four parallel bilingual parts |
| E Memory Compiler Overview | 04-memory-compiler/compiler-overview.md | docs/zh-CN/04-memory-compiler/compiler-overview.md | docs/en/04-memory-compiler/compiler-overview.md | COMPLETE — source-aligned pair |
| E Accepted Receipt and Idempotency Contract | 04-memory-compiler/accepted-receipt-and-idempotency-contract.md | docs/zh-CN/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | COMPLETE — source-aligned pair |
| E Compiler State and D Producer Admission | 04-memory-compiler/compiler-state-and-producer-admission.md | docs/zh-CN/04-memory-compiler/compiler-state-and-producer-admission.md | docs/en/04-memory-compiler/compiler-state-and-producer-admission.md | COMPLETE — source-aligned pair |
| E Event Ingestion Engine | 04-memory-compiler/event-ingestion-engine.md | docs/zh-CN/04-memory-compiler/event-ingestion-engine.md | docs/en/04-memory-compiler/event-ingestion-engine.md | COMPLETE — source-aligned pair; source blob 9fa3db53175452bf9e6f0fce8b1540765e46905f |
| E Extraction and Normalization | 04-memory-compiler/extraction-and-normalization.md | docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | docs/en/04-memory-compiler/extraction-and-normalization.md | COMPLETE — source-aligned pair; source blob c18780403de2d1dbcf471bdb8abdaa009a4a78e1 |
| E Consolidation and Conflict Resolution | 04-memory-compiler/consolidation-and-conflict-resolution.md | docs/zh-CN/04-memory-compiler/consolidation-and-conflict-resolution.md | docs/en/04-memory-compiler/consolidation-and-conflict-resolution.md | COMPLETE — source-aligned pair; source blob d16f8e2e41a6cca81ad285e5f79f075d87e64edb |
| E Evidence and Provenance | 04-memory-compiler/evidence-and-provenance.md | docs/zh-CN/04-memory-compiler/evidence-and-provenance.md | docs/en/04-memory-compiler/evidence-and-provenance.md | COMPLETE — source-aligned pair; source blob 38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963 |
| E remaining detailed contracts | 04-memory-compiler/ | Pending | Owner-branch English sources | IN PROGRESS — 7 of 8 core specs paired; 1 remains (Forget Fence and Derived Registration) |
| Memory Runtime detailed contracts (5 core specifications) | F owner branch; audited head 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | docs/zh-CN/05-memory-runtime/ | docs/en/05-memory-runtime/ | PAIRED IN PR #28 — 5/5 detailed pairs present; independent semantic review pending |
| Memory Context detailed contracts (6 core specifications) | G owner branch; audited head 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | Pending | Owner-branch English sources | NOT STARTED — 6 core specs are English-only |
| Agent Integration detailed contracts (10 core specifications) | C owner branch; audited head 0f1df3b9c8bdfbb7991cd9e18842c56c521665c4 | Pending | Owner-branch English sources | NOT STARTED — 10 core specs are English-only |
| BMCP Protocol detailed contracts (7 core specifications) | H owner branch; refresh exact source blobs per Phase 3.6 audit | Pending for normative core contracts | Owner-branch English sources | NOT STARTED — 7 normative core specs remain unpaired; separate H identity consumer/conformance status report is paired below |
| Security & Governance detailed contracts (8 core specifications) | I owner branch; audited head a00173f3cf6c266f638fe89c0d2af0445e0ae30b | Pending | Owner-branch English sources | NOT STARTED — 8 core specs are English-only |
| Memory Compiler reader guide | E owner branch: 04-memory-compiler/ | docs/zh-CN/04-memory-compiler/memory-compiler-guide.md | docs/en/04-memory-compiler/memory-compiler-guide.md | COMPLETE — overview guide only |
| Memory Runtime reader guide | F owner branch: 05-memory-runtime/ | docs/zh-CN/05-memory-runtime/memory-runtime-guide.md | docs/en/05-memory-runtime/memory-runtime-guide.md | COMPLETE — overview guide only |
| Memory Context reader guide | G owner branch: 06-memory-context/ | docs/zh-CN/06-memory-context/memory-context-guide.md | docs/en/06-memory-context/memory-context-guide.md | COMPLETE — overview guide only |
| Agent Integration reader guide | C owner branch: 07-agent-integration/ | docs/zh-CN/07-agent-integration/agent-integration-guide.md | docs/en/07-agent-integration/agent-integration-guide.md | COMPLETE — overview guide only |
| BMCP Protocol reader guide | H owner branch: 08-bmcp-protocol/ | docs/zh-CN/08-bmcp-protocol/bmcp-guide.md | docs/en/08-bmcp-protocol/bmcp-guide.md | COMPLETE — overview guide only |\n| H Phase 3.6 identity consumer/conformance status report | 08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md; source Blob 8afb914731a34d8ab44331f54f1f39bfd8ec37ce | docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md | docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md | PAIRED — status report only; H36/H36-SR NOT RUN; does not count as a normative core-spec pair |
| Storage and Index | 09-storage-and-index/ | Pending | Existing English sources | NOT STARTED |
| Security & Governance reader guide | I owner branch: 09-security-governance/ | docs/zh-CN/09-security-governance/security-governance-guide.md | docs/en/09-security-governance/security-governance-guide.md | COMPLETE — overview guide only |
| Consistency and Recovery | 11-consistency-and-recovery/ | Pending | Existing English sources | NOT STARTED |
| Cross-module conformance and fault-injection reader guide | A owner branch: reviews/integration/cross-module-conformance-plan.md | docs/zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md | docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md | COMPLETE — test guide only; execution NOT_RUN/BLOCKED |
| Detailed Testing and Acceptance specifications/reports | 12-testing-and-acceptance/ and reviews/ | Pending | Existing English sources | NOT STARTED — detailed test cases and review reports pending |
| Detailed technology and Rust engineering | 13-engineering-decisions/ | Pending | Existing English sources | NOT STARTED |

**Exact Owner branch source snapshots and migration batches:** [Owner Branch Bilingual Migration Inventory](owner-branch-translation-inventory.md). The audited branch SHAs are source references only; refresh each branch HEAD before translating or accepting a companion.

## 3. PR #28 branch overlay / PR #28 分支覆盖状态

The following describes the current bilingual companion files on `docs/bilingual-coverage-completion`, not the historical Owner source-branch audit snapshots. `PAIRED` means both language files exist in the PR branch; it does not mean semantic review, source-branch reconciliation, or governance acceptance is complete.

以下状态描述 `docs/bilingual-coverage-completion` 分支中的双语对应文件，不覆盖历史 Owner 源分支审计快照。`PAIRED` 仅表示 PR 分支中中英文文件均存在，不表示语义复审、源分支基线核对或治理验收已经完成。

| Owner | Detailed core source set | PR #28 bilingual coverage | Remaining work |
|---|---:|---|---|
| B | 6 main specs + Phase 3 identity extensions | 6/6 main specs; 2 Phase 3 identity companions paired | ADR-001 remains ADR-BLOCKED; INT-P0-02 / INT-X-03 remain OPEN; independent semantic review and cross-owner approval pending |
| D | 8 core specs | 8/8 paired | Source-branch reconciliation and semantic acceptance |
| E | 8 core specs | 7/8 paired | Forget Fence and Derived Registration |
| F | 5 core specs | 5/5 paired | Independent semantic review |
| G/C/H/I | 6/10/7/8 core specs | Reader guides only; detailed pairs not started; H identity status report is a separate paired report | Full detailed contracts and reviews |
| Storage/Consistency | Per-source inventory pending | No detailed paired set | COC/JF-10/identity/restore/high-water/acceptance evidence inventory and translation |

## 4. Translation and readability sequence / 翻译与易读性推进顺序

### Batch 1 — Orientation and shared language / 第一批：系统认知与共同语言
- Portal, style guide, glossary.
- System overview in both languages.
- Technology overview in both languages.
- Status: COMPLETE.

### Batch 2 — Governance and system map / 第二批：治理基线与系统地图
- Status: COMPLETE for reader guides and core maps.
- Detailed design principles, system overview, component interactions, data flows, system boundaries, and quality-attribute source documents: COMPLETE — source-aligned bilingual pairs.
- GOV-DOC-001 is present on main as the normative repository-wide policy and applies to new architecture work.
- Architecture principles, invariants, terminology source reconciliation.
- Component map, responsibility matrix, system workflows.
- Deliverables: paired Chinese/English documents and cross-links.
- Acceptance: no owner or authority boundary changes; glossary parity checked.

### Batch 3 — Domain and canonical memory / 第三批：领域模型与权威记忆
- D Canonical Memory reader guide: COMPLETE — includes D/E/F/G/H/I ownership split, cursor namespaces, and Forget boundary.
- D: 8/8 core specifications have bilingual companions in PR #28; the long Forget Fence Operation/Publication Gate is split into four parallel bilingual parts. Source-branch reconciliation and independent semantic review remain separate gates.
- Domain Model reader guide: COMPLETE.
- B's six main source specifications: COMPLETE — source-aligned bilingual pairs added. Phase 3 typed-reference/Scope and Principal/Actor mapping now have exact-Blob bilingual companions (2/2); ADR-001 decision package remains NOT STARTED and ADR-BLOCKED. INT-P0-02 / INT-X-03 remain OPEN.
- D Canonical Memory bilingual companions: present in PR #28 (8/8); source-branch reconciliation and semantic acceptance remain pending.
- B Domain Model.
- D Canonical Memory, lifecycle, versioning, Forget Fence, commit cursor.
- Acceptance: Fact/Claim OPEN state preserved; exact identifiers and state names unchanged.

### Batch 4 — Memory production and runtime / 第四批：记忆生产与运行时
- E and F reader guides: COMPLETE.
- E: 7/8 core specifications have bilingual companions; the remaining source scope is Forget Fence and Derived Registration. F: all 5/5 detailed core specifications are paired in PR #28; independent semantic review remains pending.
- E Compiler, ingestion, extraction, evidence, consolidation.
- F retrieval, activation, working set, scheduling, anti-resurrection: 5/5 detailed bilingual pairs present in PR #28; semantic review pending.
- Acceptance: Accepted/Compiled/Canonical Committed/Indexed remain distinct; cursor and Forget semantics stay aligned.

### Batch 5 — Context and Agent boundary / 第五批：上下文与 Agent 边界
- G Context, C Agent Integration, and H BMCP reader guides: COMPLETE.
- G/C/H normative detailed contracts: NOT STARTED — G has 6, C has 10 and H has 7 core specifications; refresh exact source Blob SHAs before translation. H Phase 3.6 identity consumer/conformance status report is separately PAIRED; H36/H36-SR remain NOT RUN.
- G Context Manager, versioning, edit operations, reconciliation, budget.
- H BMCP schemas and state machines.
- C Adapter integration and inference-boundary Applied proof.
- Acceptance: ContextVersion, Delivery, Applied, PermissionEpoch, and ForgetFenceGeneration remain distinct.

### Batch 6 — Governance, storage, and recovery / 第六批：治理、存储与恢复
- I Security & Governance reader guide: COMPLETE.
- I detailed policies/contracts: NOT STARTED — 8 English-only core specifications at audited head; refresh source SHA before translation.
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

## 5. Definition of done / 完成定义

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

## 6. Change-control rule / 变更控制

- Translation is not an architecture decision.
- If the source contract changes, update both language versions in the same change set.
- If only one language can be updated immediately, mark the other STALE and record the source revision it has not yet incorporated.
- Never resolve an OPEN issue by choosing more definitive wording in translation.
- Keep a distinction between explanatory guides and normative owner specifications.

## 7. Current limitation / 当前限制

A integration governance and conformance reader guides are available in both languages. The detailed A registry, complete test catalogue, and Owner-specific review reports remain to be translated as source-level documents.

Batches 1 and 2 provide the orientation, shared language, governance invariants, component map, responsibility matrix, and the source-aligned system-level specifications. The six core Domain Model source specifications are also paired. The H Phase 3.6 identity consumer/conformance status report now has a separate bilingual pair, but this does not complete H's normative core contracts or imply H36 execution. This is not yet a full translation of all Owner branch contracts, technology decisions, detailed test plans, or review reports. GOV-DOC-001 is already part of the main governance baseline.\n\nThe 2026-11-17 Phase 3.6 identity/Applied/Storage source audit is recorded in [the source audit report](../reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md). It records currentness findings BSR-28-005 and BSR-28-006 and keeps the high-risk detailed-contract coverage finding BSR-28-007 OPEN.


## 8. B Phase 3 identity companion batch — 2026-11-17

Two exact B Owner-branch source artifacts now have reciprocal Chinese/English companions in PR #28:

| Source artifact | Owner branch | Exact source Blob SHA | English companion | Chinese companion | Preserved source status |
|---|---|---|---|---|---|
| `02-domain-model/typed-reference-and-scope-semantics.md` | `session-b-domain-model-phase3` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | `docs/en/02-domain-model/typed-reference-and-scope-semantics.md` | `docs/zh-CN/02-domain-model/typed-reference-and-scope-semantics.md` | CANDIDATE; ClaimRef conditional on ADR-001; I36-GOV-03/04 BLOCKED |
| `02-domain-model/principal-actor-binding-mapping.md` | `session-b-domain-model-phase3` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | `docs/en/02-domain-model/principal-actor-binding-mapping.md` | `docs/zh-CN/02-domain-model/principal-actor-binding-mapping.md` | CANDIDATE; INT-P0-02 / INT-X-03 OPEN; I36 governance decisions remain blocked |

Pair presence is not semantic acceptance, identity freeze, I policy approval, H wire freeze, or ADR-001 closure. The detailed semantic parity review must separately inspect both pairs. Exact source Blob pins are not Owner branch HEADs.
