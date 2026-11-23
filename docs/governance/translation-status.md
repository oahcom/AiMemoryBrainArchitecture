---
document_metadata:
  domain: architecture
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
---

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
| REQ02-LEXICAL-BENCH-001 | benchmarks/req02/fts5_vs_like.py + results-2026-11-20.json | docs/zh-CN/13-engineering-decisions/req02-fts5-vs-like-benchmark.md | docs/en/13-engineering-decisions/req02-fts5-vs-like-benchmark.md | COMPLETE — bilingual candidate evidence; not a technology decision |
| ADR-REQ02-LEXICAL-001 | ADR-REQ02-LEXICAL-001 — bounded selection of SQLite FTS5 for the initial local lexical channel | docs/zh-CN/13-engineering-decisions/req02-fts5-vs-like-decision.md | docs/en/13-engineering-decisions/req02-fts5-vs-like-decision.md | COMPLETE — bounded decision; not a system-wide technology freeze |
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
| E Accepted Receipt and Idempotency Contract | 04-memory-compiler/accepted-receipt-and-idempotency-contract.md | docs/zh-CN/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | DEREFERENCED — historical bilingual pair retained; no current normative source path; counterparts are reading evidence, not an authoritative substitute |
| E Compiler State and D Producer Admission | 04-memory-compiler/compiler-state-and-producer-admission.md | docs/zh-CN/04-memory-compiler/compiler-state-and-producer-admission.md | docs/en/04-memory-compiler/compiler-state-and-producer-admission.md | DEREFERENCED — historical bilingual pair retained; no current normative source path; counterparts are reading evidence, not an authoritative substitute |
| E Event Ingestion Engine | 04-memory-compiler/event-ingestion-engine.md | docs/zh-CN/04-memory-compiler/event-ingestion-engine.md | docs/en/04-memory-compiler/event-ingestion-engine.md | COMPLETE — source-aligned pair; source blob 9fa3db53175452bf9e6f0fce8b1540765e46905f |
| E Extraction and Normalization | 04-memory-compiler/extraction-and-normalization.md | docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | docs/en/04-memory-compiler/extraction-and-normalization.md | COMPLETE — source-aligned pair; source blob c18780403de2d1dbcf471bdb8abdaa009a4a78e1 |
| E Consolidation and Conflict Resolution | 04-memory-compiler/consolidation-and-conflict-resolution.md | docs/zh-CN/04-memory-compiler/consolidation-and-conflict-resolution.md | docs/en/04-memory-compiler/consolidation-and-conflict-resolution.md | COMPLETE — source-aligned pair; source blob d16f8e2e41a6cca81ad285e5f79f075d87e64edb |
| E Evidence and Provenance | 04-memory-compiler/evidence-and-provenance.md | docs/zh-CN/04-memory-compiler/evidence-and-provenance.md | docs/en/04-memory-compiler/evidence-and-provenance.md | COMPLETE — source-aligned pair; source blob 38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963 |
| E remaining detailed contracts | 04-memory-compiler/ | Pending | Owner-branch English sources | IN PROGRESS — 7 of 8 core specs paired; 1 remains (Forget Fence and Derived Registration) |
| Memory Runtime detailed contracts (5 core specifications) | F owner branch; audited head 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | docs/zh-CN/05-memory-runtime/ | docs/en/05-memory-runtime/ | PAIRED IN PR #28 — 5/5 detailed pairs present; independent semantic review pending |
| Memory Context detailed contracts (6 core specifications) | G owner branch; audited head 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | Pending | Owner-branch English sources | NOT STARTED — 6 core specs are English-only |
| Agent Integration detailed contracts (10 core specifications) | C Owner branch; Phase 3.6 final-request evidence Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | docs/zh-CN/07-agent-integration/phase-3.6-final-request-evidence-contract.md | docs/en/07-agent-integration/phase-3.6-final-request-evidence-contract.md | 1/10 core specs paired; C decisions recorded; C/G/H cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED |
| BMCP Protocol detailed contracts (7 core specifications) | H owner branch; refresh exact source blobs per Phase 3.6 audit | Pending for normative core contracts | Owner-branch English sources | NOT STARTED — 7 normative core specs remain unpaired; separate H identity consumer/conformance status report is paired below |
| Security & Governance detailed contracts (8 core specifications) | I owner branch; audited head a00173f3cf6c266f638fe89c0d2af0445e0ae30b | Pending | Owner-branch English sources | NOT STARTED — 8 core specs are English-only |
| Memory Compiler reader guide | E owner branch: 04-memory-compiler/ | docs/zh-CN/04-memory-compiler/memory-compiler-guide.md | docs/en/04-memory-compiler/memory-compiler-guide.md | COMPLETE — overview guide only |
| Memory Runtime reader guide | F owner branch: 05-memory-runtime/ | docs/zh-CN/05-memory-runtime/memory-runtime-guide.md | docs/en/05-memory-runtime/memory-runtime-guide.md | COMPLETE — overview guide only |
| Memory Context reader guide | G owner branch: 06-memory-context/ | docs/zh-CN/06-memory-context/memory-context-guide.md | docs/en/06-memory-context/memory-context-guide.md | COMPLETE — overview guide only |
| Agent Integration reader guide | C owner branch: 07-agent-integration/ | docs/zh-CN/07-agent-integration/agent-integration-guide.md | docs/en/07-agent-integration/agent-integration-guide.md | COMPLETE — overview guide only |
| BMCP Protocol reader guide | H owner branch: 08-bmcp-protocol/ | docs/zh-CN/08-bmcp-protocol/bmcp-guide.md | docs/en/08-bmcp-protocol/bmcp-guide.md | COMPLETE — overview guide only |
| BMCP architecture review/handoff (BMCP-ARCH-001 v0.2.2) | reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | #453 merge commit `7c7801db396b92c57ad37020fe170f65f25e43ce`; EN Blob `b496a891fee8a1b50d640c72be6f6d4fa93e14ae`; ZH-CN Blob `bd0036aa37a5aefec136326c62fc50b076bebc1e` | REVIEW/HANDOFF PAIR ONLY — CANDIDATE / ARCHITECTURE_PARTIAL; independent semantic bilingual review PENDING; does not count toward the 7 normative core specifications |
| H Phase 3.6 identity consumer/conformance status report | 08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md; source Blob 8afb914731a34d8ab44331f54f1f39bfd8ec37ce | docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md | docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md | PAIRED — status report only; H36/H36-SR NOT RUN; does not count as a normative core-spec pair |
| Storage and Index | 09-storage-and-index/ | Pending | Existing English sources | NOT STARTED |
| Security & Governance reader guide | I owner branch: 09-security-governance/ | docs/zh-CN/09-security-governance/security-governance-guide.md | docs/en/09-security-governance/security-governance-guide.md | COMPLETE — overview guide only |
| Consistency and Recovery | 11-consistency-and-recovery/ | Pending | Existing English sources | NOT STARTED |
| Cross-module conformance and fault-injection reader guide | A owner branch: reviews/integration/cross-module-conformance-plan.md | docs/zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md | docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md | COMPLETE — test guide only; execution NOT_RUN/BLOCKED |
| Detailed Testing and Acceptance specifications/reports | 12-testing-and-acceptance/ and reviews/ | Pending | Existing English sources | NOT STARTED — detailed test cases and review reports pending |
| Detailed technology and Rust engineering | 13-engineering-decisions/ | Pending | Existing English sources | NOT STARTED |
| AI development process execution rules | `14-ai-development/AI-EXEC-001.md` (v1.1; source commit `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856`; source blob `372a290359f9e9de2bd81d7901beb2f084e6e3a4`) | Embedded Chinese v1.1 — source authority | `docs/en/14-ai-development/AI-EXEC-001.md` (translation commit `e0e20ed30b4a21c2e26d0a4c0903a63c0293a46f`; translation blob `c93db6a480bbe8f5ebbc8f3e56b570a920a20ad7`; initial commit `0d2857a0fd026e49048031a7fd8b5d0d137ebf87`) | COMPLETE — source-aligned pair; original STALE exception approved through 2026-12-02, completed early 2026-11-18; AID-2026-004 / Issue #218 |
| AI development prompt execution rules | `14-ai-development/AI-EXEC-002.md` (v1.1; source commit `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856`; source blob `ebb7f1ee9a084864c454711d271499cfbf8d386f`) | Embedded Chinese v1.1 — source authority | `docs/en/14-ai-development/AI-EXEC-002.md` (translation commit `08b07d228dbe78a209a5af68c4988b292e65e9c8`; translation blob `96aab56ce856484e24ad99ec6944a4c45ceb763b`) | COMPLETE — source-aligned pair; original STALE exception approved through 2026-12-02, completed early 2026-11-18; AID-2026-004 / Issue #218 |
| AI ecosystem-loop rollout plan | `14-ai-development/AI-EXEC-ROLLOUT-001.md` (v4.0; source commit `778b4d3b4b6c846faa6a02247d31d14a33d8b626`; source blob `14082151e2839e966349498138b9001d01de9bed`) | Embedded Chinese v4.0 — source authority | `docs/en/14-ai-development/AI-EXEC-ROLLOUT-001.md` (translation commit `e683ea275dfaf85fff0f9d18bb706d3bdb5d60a1`; translation blob `87e4314d1df9bbff2321eb1053078bb5f7148d8d`) | COMPLETE — source-aligned pair; original STALE exception approved through 2026-12-02, completed early 2026-11-18; AID-2026-004 / Issue #218 |

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
| G/C/H/I | 6/10/7/8 core specs | C: 1/10 detailed core specs paired (Phase 3.6 final-request evidence); G/H normative detailed pairs not started; H identity status report is separate paired report | Remaining detailed contracts and cross-owner semantic reviews |
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

Batches 1 and 2 provide the orientation, shared language, governance invariants, component map, responsibility matrix, and the source-aligned system-level specifications. The six core Domain Model source specifications are also paired. The H Phase 3.6 identity consumer/conformance status report now has a separate bilingual pair, but this does not complete H's normative core contracts or imply H36 execution. This is not yet a full translation of all Owner branch contracts, technology decisions, detailed test plans, or review reports. GOV-DOC-001 is already part of the main governance baseline.

The 2026-11-17 Phase 3.6 identity/Applied/Storage source audit is recorded in [the source audit report](../../reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md). It records currentness findings BSR-28-005 and BSR-28-006 and keeps the high-risk detailed-contract coverage finding BSR-28-007 OPEN.


## 8. B Phase 3 identity companion batch — 2026-11-17

Two exact B Owner-branch source artifacts now have reciprocal Chinese/English companions in PR #28:

| Source artifact | Owner branch | Exact source Blob SHA | English companion | Chinese companion | Preserved source status |
|---|---|---|---|---|---|
| `02-domain-model/typed-reference-and-scope-semantics.md` | `session-b-domain-model-phase3` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | `docs/en/02-domain-model/typed-reference-and-scope-semantics.md` | `docs/zh-CN/02-domain-model/typed-reference-and-scope-semantics.md` | CANDIDATE; ClaimRef conditional on ADR-001; I36-GOV-03/04 BLOCKED |
| `02-domain-model/principal-actor-binding-mapping.md` | `session-b-domain-model-phase3` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | `docs/en/02-domain-model/principal-actor-binding-mapping.md` | `docs/zh-CN/02-domain-model/principal-actor-binding-mapping.md` | CANDIDATE; INT-P0-02 / INT-X-03 OPEN; I36 governance decisions remain blocked |

Pair presence is not semantic acceptance, identity freeze, I policy approval, H wire freeze, or ADR-001 closure. The targeted review [BSR-28-B-IDENTITY-001](../../reviews/translation/2026-11-17-b-phase3-identity-bilingual-semantic-review.md) has now inspected both pairs and found no material Chinese/English semantic divergence. This is translation parity only; exact source Blob pins are not Owner branch HEADs and all source CANDIDATE/OPEN/BLOCKED statuses remain unchanged.


## 9. C Phase 3.6 final-request evidence companion — 2026-11-17

- Source: `07-agent-integration/phase-3.6-final-request-evidence-contract.md`
- Owner branch: `session-c-agent-integration-2026-11-16`
- Exact source Blob SHA: `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`
- Pair: `docs/en/07-agent-integration/phase-3.6-final-request-evidence-contract.md` and `docs/zh-CN/07-agent-integration/phase-3.6-final-request-evidence-contract.md`
- Source state preserved: C semantic decisions recorded; C/G/H cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED; C-FR-01..12 SPECIFIED / NOT RUN.
- Scope: one of C's ten detailed core specifications only. The companion does not freeze H wire fields, G Applied authority, I authorization policy, D Forget fence, or any implementation.


## 10. C/G/H Phase 3.6 Applied cross-owner review — 2026-11-17

- Independent review: [English report](../../reviews/translation/2026-11-17-cgh-applied-contract-cross-owner-review.md) / [中文报告](../../reviews/translation/2026-11-17-cgh-applied-contract-cross-owner-review.zh-CN.md).
- Exact sources re-read: C `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`; G `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; H Adapter Capability/Applied `ed6b43a29aa368d772c701ffc83309a5aadf3c00`.
- Six-stage lifecycle, historical/current-use distinction, and C/G duplicate/late-evidence semantics are aligned.
- H Adapter candidate remains CANDIDATE; final-request proof profile OPEN with C; authorization binding OPEN with I. Findings H36-AP-01..07 identify unresolved exact boundary identity, target/attempt mapping, managed-region inventory/coverage, I/D authority vector, verifier-bound identity, evidence provenance, and per-request bypass coverage.
- H Adapter pair is intentionally NOT marked complete: source-to-source field alignment must be resolved before translation can safely represent a normative protocol contract.
- C/G/H freeze remains BLOCKED. C-FR-01..12 and G-36-01..15 remain SPECIFIED / NOT RUN; H Adapter conformance NOT RUN; implementation NOT VERIFIED.


## H Owner candidate field-mapping revision — 2026-11-17

H's `session-h-bmcp-protocol` source `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` was revised with §11, an exact final-request field-mapping proposal. Current exact source Blob SHA: `db59b63e322d7255b8b400f47859dcac32bb3027` (replaces prior reviewed Blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00`). The addendum proposes explicit FinalRequestBoundaryId/type, Context/Delivery/attempt bindings, managed-region identity/revision/inventory/coverage/digest, verifier-bound identities, I/D authority references, provenance, per-request bypass coverage, replay identity and temporal rules.

This remains H CANDIDATE only: C confirmation, G Applied-consumer acceptance, I/D/B authority confirmation, versioned wire schema and conformance remain pending. Do not mark the H bilingual pair complete until this exact source version is independently accepted/aligned and translated.


## H Owner 候选字段映射修订 — 2026-11-17

H 的 `session-h-bmcp-protocol` 源文件 `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` 已新增 §11 精确 final-request 字段映射提案。当前精确源 Blob SHA：`db59b63e322d7255b8b400f47859dcac32bb3027`（替代此前复审的 Blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00`）。补充条款提议明确 FinalRequestBoundaryId/type、Context/Delivery/attempt 绑定、Managed Region 身份/修订/inventory/coverage/digest、verifier 身份绑定、I/D 权威引用、证据来源信息、逐请求 bypass 覆盖、重放身份和时间顺序规则。

此版本仍仅为 H CANDIDATE：C 确认、G Applied 消费方接受、I/D/B 权威确认、版本化 Wire Schema 和一致性测试均待完成。在该精确源版本经过独立接受/对齐并翻译前，不得把 H 双语配对标记为完成。


## 11. H Adapter Capability / Applied Attestation bilingual companion — 2026-11-17

- Exact H source Blob: `db59b63e322d7255b8b400f47859dcac32bb3027` on `session-h-bmcp-protocol`.
- Pair: `docs/en/08-bmcp-protocol/adapter-capability-and-applied-attestation.md` and `docs/zh-CN/08-bmcp-protocol/adapter-capability-and-applied-attestation.md`.
- Structural readback: 22/22 headings and 33/33 table rows in source, EN and zh-CN; EN content is exact source text plus source/language metadata.
- Targeted semantic parity review: [EN report](../../reviews/translation/2026-11-17-h-adapter-capability-applied-bilingual-review.md) / [中文报告](../../reviews/translation/2026-11-17-h-adapter-capability-applied-bilingual-review.zh-CN.md) — PASS for this exact Blob only.
- H source status remains CANDIDATE; final-request proof profile OPEN with C; authorization binding OPEN with I. H conformance NOT RUN; implementation/interoperability NOT VERIFIED; C/G/H freeze BLOCKED.
- Coverage: 1/7 H detailed core specifications paired. This does not complete H's detailed contract set or the C/G/H freeze.


## 12. G Phase 3.6 Applied / Forget / Reconciliation bilingual companion — 2026-11-17

- Exact G source Blob: `aa3afa73d8a76cc6f025839c52bfbff6a983046a` on `session-g-memory-context`.
- Pair: `docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` and `docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`.
- Structural readback: 21/21 headings and 37/37 table rows across source, EN and zh-CN; EN companion contains exact source content.
- Targeted semantic parity: [EN report](../../reviews/translation/2026-11-17-g-phase36-applied-forget-bilingual-review.md) / [中文报告](../../reviews/translation/2026-11-17-g-phase36-applied-forget-bilingual-review.zh-CN.md) — PASS for this exact Blob.
- G source status remains semantic decisions recorded; C/G/H Applied freeze BLOCKED; implementation/execution NOT VERIFIED; G-36-01..15 SPECIFIED / NOT RUN.



## H recovery-batch source refresh — 2026-11-17

- Current H source Blob: `0dca3dc5463a02be0e19524811afbae87795baf5`, superseding `db59b63e322d7255b8b400f47859dcac32bb3027`.
- H EN/zh-CN companions refreshed. Structural readback: 23/23 headings and 33/33 table rows across source/EN/zh-CN; targeted parity PASS pending updated final report readback.
- H §11.8 adds candidate mapping for CGH-APPLIED-1.1 COC terminal proof, recovery-batch completeness, owner high-water, participant reconciliation, I/D owner evidence and Storage same-XID terminal proof.
- New H36-AP-08 remains OPEN: no updated/generated H wire schema/SDK or exact ACK message-family binding; C/G/I/D/Storage confirmations and conformance remain pending. H source remains CANDIDATE; C/G/H freeze BLOCKED.



## H provider outcome / owner gate mapping refresh — 2026-11-17

- Current H source Blob: `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`, superseding `0dca3dc5463a02be0e19524811afbae87795baf5`.
- H EN/zh-CN companions refreshed; structural parity now 24/24 headings and 33/33 table rows across source/EN/zh-CN.
- §11.9 requires C-issued provider receipt and immutable CSubmitOutcome; terminal proof only after all owner outcomes are determinate; I/D exclusively issue their own gate-release attestations.
- H36-AP-09 remains OPEN because the exact H wire message-family Schema/SDK mapping and consumer acceptance are not present. H candidate remains CANDIDATE; C/G/I/D/Storage acceptance and conformance remain pending; C/G/H freeze BLOCKED.


## 13. C/G/H cross-owner Phase 3.6 contract audit — 2026-11-17

- Independent cross-owner audit: `reviews/integration/2026-11-17-cgh-phase36-cross-owner-contract-consistency-review.md` and Chinese companion.
- Exact baselines: C `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`; G `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; H current `0dca3dc5463a02be0e19524811afbae87795baf5`.
- Result: six-stage lifecycle and core authority split aligned; **CGH-APPLIED-1.1 recovery-batch evidence chain BLOCKED**. C source does not yet define the required CSubmitOutcome/provider receipt contract or record exact-version acceptance of the 1.1 recovery-batch package. H §11.8 is a candidate mapping, not frozen schema/SDK. Exact-version C/G/H joint acceptance is not established.
- Findings XCH-36-001..005; P1 blockers and P2 ordering-language ambiguity detailed in the cross-owner report. All conformance remains NOT RUN / implementation NOT VERIFIED.
- H current companion pin is `0dca3dc5463a02be0e19524811afbae87795baf5`; earlier H parity report against `db59b63e322d7255b8b400f47859dcac32bb3027` is superseded for current-source evidence.



## C exact-version recovery-batch acceptance gap — 2026-11-17

- New finding **C36-AP-01 — OPEN**: current C source Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` accepts the pinned CGH-APPLIED-1.0 package and BIH consumer package, but contains no explicit C Owner acceptance of G's later CGH-APPLIED-1.1 recovery-batch amendment or complete CSubmitOutcome/provider-receipt mapping for that profile.
- G 1.1 requires actual C provider receipt and immutable CSubmitOutcome. H §§11.8–11.9 only propose carrying C-issued references; H cannot substitute for C's producer decision.
- C must publish exact-version acceptance/mapping for C provider receipt, CSubmitOutcome, terminal reference, UNKNOWN/IN_DOUBT and causal binding. Until then C/G/H 1.1 acceptance remains BLOCKED.


## 14. H current-source refresh and CSubmitOutcome closure proposal — 2026-11-17

- H source moved again to Blob `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`; current EN/zh-CN companions pin this exact Blob and include §§11.8–11.9. Structural readback: 24/24 headings and 33/33 table rows across source/EN/zh-CN; EN companion contains exact source content. §11.9 now explicitly maps C-issued `c_provider_receipt_ref` / `c_submit_outcome_ref`, participant terminal proof eligibility and I/D-exclusive gate release, but remains CANDIDATE.
- Cross-owner audit refreshed to H Blob `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`: [EN](../../reviews/integration/2026-11-17-cgh-phase36-cross-owner-contract-consistency-review.md) / [中文](../../reviews/integration/2026-11-17-cgh-phase36-cross-owner-contract-consistency-review.zh-CN.md).
- C source remains Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` and still does not define the C-issued Provider receipt/CSubmitOutcome object or record exact-version acceptance of the G recovery-batch 1.1 package. A bounded non-normative closure proposal was added: [EN](../../reviews/integration/2026-11-17-c-owner-csubmitoutcome-closure-proposal.md) / [中文](../../reviews/integration/2026-11-17-c-owner-csubmitoutcome-closure-proposal.zh-CN.md). This is NOT a C Owner decision and does not amend C source.
- C/G/H joint 1.1 freeze remains BLOCKED; H schema/SDK freeze NOT ESTABLISHED; implementation NOT VERIFIED; conformance NOT RUN.



## C cross-authority causal-order companion — 2026-11-17

- Exact C source: `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, branch `session-c-agent-integration-2026-11-16`, Blob `45a48249717c8cddb07ab96197730ef93d406c22`.
- Pair: `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` and `docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`.
- Structural readback: 14/14 headings; no tables in source/EN/zh-CN; EN exact source content. Targeted parity: [EN report](../../reviews/translation/2026-11-17-c-submit-causal-order-bilingual-review.md) / [中文报告](../../reviews/translation/2026-11-17-c-submit-causal-order-bilingual-review.zh-CN.md) — PASS for this exact Blob.
- C explicitly ACCEPTS WITH ENUMERATED EXCEPTIONS the exact CGH-APPLIED-1.1 recovery-batch amendment, A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`. C36-AP-01 is RESOLVED at source-decision level; this does not resolve H wire/schema mapping or deployment/test gates.
- C detailed core companion coverage is now 2/10 (Final Request Evidence + C-submit causal-order).



## C36-AP-01 disposition correction — 2026-11-17

The earlier OPEN entry is superseded. C's separate cross-authority causal-order source Blob `45a48249717c8cddb07ab96197730ef93d406c22` explicitly accepts the exact CGH-APPLIED-1.1 recovery-batch amendment with enumerated exceptions and defines CSubmitOutcome/provider evidence. **C36-AP-01: RESOLVED at C source-decision level.** This does not close H36-AP-09, H wire Schema/SDK mapping, coordinator/provider implementation, or conformance.


## 15. Corrected current C/G/H exact-version review — 2026-11-17

- Corrected cross-owner report (supersedes the earlier false-positive gap assessment): [EN](../../reviews/integration/2026-11-17-cgh-phase36-cross-owner-contract-consistency-review.md) / [中文](../../reviews/integration/2026-11-17-cgh-phase36-cross-owner-contract-consistency-review.zh-CN.md).
- C exact current evidence: recovery-batch Owner decision Blob `45a48249717c8cddb07ab96197730ef93d406c22`; normative C provider outcome contract Blob `819705037da89834e10b6dd2ec6e66c1b8c70886`; CSubmitOutcome 1.0.1 schema Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; current 38-test review Blob `24337b79cfea6264a8a6f11fa414578fc559716c`.
- H exact current evidence: Unified 1.2.14 Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`; C/H mapping Blob `1cbe74eba69325510d6b1019d971661f965eabf8`; validator/test/fixture Blobs `eab961a08d41e871f38543b18ee60cf024977414` / `540056d7c4f290c31290b17c264c69cfd76b1cb2` / `c80247a6ecfbb4a29ff0993e8e2aea4829d00626`; H full-path closure Blob `cda025fb157815570b3280fa5ff168d5e62453b1`.
- Exact H CI run `44070924346`, commit `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`, job `133996627914` SUCCESS; 38 methods (32 H validator unit/fixture + 6 C crypto interop). All ten authority callbacks remain deterministic test doubles; production trust/authority integration is not proven.
- G delegated current consumer review Blob `1894860c76336f8739d354b72beed3992cffd17e`; G ACCEPTS WITH ENUMERATED G-OWNED APPLIED CONDITIONS at L1/L2 only; not an independent human G Owner signature, not frozen.
- Bilingual PR companions added for G Phase 3.8.18 and C Phase 3.8.19. These are review artifacts, not new normative core-contract coverage counts.
- Earlier CSubmitOutcome closure proposal is marked SUPERSEDED by actual C Owner contract/decision artifacts. The earlier cross-owner report has been corrected; do not use its initial XCH-36-001..003 false-positive status.
- Gate: C/H L1/L2 local full-path PASS; G delegated consumer review accepted with conditions; global Applied contract NOT FROZEN; production authority integration OPEN/NOT VERIFIED; G Applied persistence NOT VERIFIED; L3/L4 NOT RUN.


## 16. Final PR structural readback after C/G review pairs — 2026-11-17

- G Phase 3.8.18 companion parity: source bilingual 9 headings / 16 table rows; EN and zh-CN each 8 headings / 8 table rows (source has two language title headings). Exact source Blob `1894860c76336f8739d354b72beed3992cffd17e`.
- C Phase 3.8.19 companion parity: source bilingual 6 headings; EN and zh-CN each 5 headings (source has two language title headings). Exact source Blob `24337b79cfea6264a8a6f11fa414578fc559716c`.
- H Phase 3.8.14 full-path closure Chinese test count/scope corrected to match English: 38 total methods = 32 H validator unit/fixture + 6 C crypto interop. Current closure Blob `cda025fb157815570b3280fa5ff168d5e62453b1`; exact CI run `44070924346` SUCCESS.
- PR #28 current head `8431312367a44b70246912884547a377cf69116c`; workflow run `44072368844` / Run #114, job GOV-DOC-001 structural checks: **SUCCESS**. This proves paired-document/manifest structure only, not semantic review, architecture approval, implementation or conformance.
- PR remains Draft/Open, 158 files changed; no merge authorized.


## 17. Final current-head structural CI and Issue #3 reconciliation — 2026-11-17

- Issue #3 received current C/G/H exact-version reconciliation comment ID `6946497217`, including exact C/H/G pins, L1/L2 CI evidence ceiling and remaining production gates.
- PR #28 current head: `3b5ce54c1687e9c7591f9e6e70e5c24f2afa465d`; workflow runs `44072524932` (#116) and `44072518263` (#115) both completed SUCCESS; job `GOV-DOC-001 structural checks` succeeded.
- Structural gate remains limited to paired-document/manifest structure. It does not establish translation semantic approval, Owner signature, schema freeze, implementation, L3/L4 conformance or production readiness.
- PR #28 remains Draft/Open; 158 files changed; no merge or production activation authorized.


## 18. FIX-2026-P1-T1 prompt template bilingual companions — remediation

- Work Item: FIX-2026-P1-T1 / Issue #268. The original PR #269 was merged into main at `cd3f5d7191000f6414134ef235cac94f33ca87e8` despite the independent review disposition requiring it to remain Draft/Open; this entry records follow-up remediation only and does not retroactively authorize that merge.
- Paired artifacts: `prompts/00-setup/TEMPLATE-v2.md` ↔ `prompts/00-setup/TEMPLATE-v2.zh-CN.md`; `prompts/00-setup/MIGRATION-GUIDE.md` ↔ `prompts/00-setup/MIGRATION-GUIDE.zh-CN.md`.
- Reciprocal links are present in each pair. Both language versions preserve the same seven-section structure, IDs, status, mandatory constraints, evidence rules, migration mapping, source provenance, and NOT RUN / NOT APPLICABLE semantics.
- Structural parity self-check: 7/7 numbered core sections in both template versions; 6/6 top-level numbered sections in both migration-guide versions; matching IDs/version/status and reciprocal links. This is implementer self-check only, NOT independent semantic-parity approval.
- Exact-head semantic parity review: PENDING independent reviewer. GOV-DOC-001 structural/link checker and repository automated tests: NOT RUN in this remediation commit.
- The prompt-authoring standard §4 was also reconciled bilingually in its existing bilingual source artifact; its twelve mandatory content requirements are mapped into the seven structural sections. No governance adoption or Owner acceptance is implied.

## 19. Source revision pointer remediation / 来源版本指针修复

This record tracks provenance metadata only; it does not change normative content or assert semantic-parity approval.

- Six stale source-blob references were refreshed in both English and Chinese counterparts to the exact current source blobs.
- Sixteen missing normative source targets (twelve under the removed `03-memory-brain/` root and four missing files under `04-memory-compiler/`) are explicitly marked `DEREFERENCED` in both language counterparts.
- Each dereferenced record preserves the historical source Blob identifier and identifies a surviving opposite-language reading counterpart; no translation is represented as a normative replacement.
- The change covers 44 bilingual metadata documents and adds the read-only checker `scripts/check_source_revision_pointers.py`.
- No deleted source artifact is reconstructed, no domain decision is inferred, and no production-readiness or semantic acceptance is claimed.

- 六处陈旧源 Blob 引用已在中英文对照文件中更新为准确的当前源 Blob。
- 十六处缺失的规范源目标已在中英文对照文件中标记为 `DEREFERENCED`，并保留历史 Blob 与替代阅读路径。
- 本次变更覆盖 44 份双语元数据文档，并新增只读检查脚本；不重建已删除源文件，不推断领域决策或生产就绪状态。
