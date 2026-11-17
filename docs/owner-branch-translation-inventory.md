# Owner Branch Bilingual Migration Inventory / Owner 分支双语迁移清单

- Document ID: DOC-OWNER-INVENTORY-001
- Version: 1.0
- Audit date: 2026-11-17
- Policy: GOV-DOC-001
- Status: Active migration inventory; branch snapshots are not automatically approved main baselines

## 1. Purpose / 目的

This inventory records the exact Owner branch revisions inspected for bilingual coverage. It prevents translations from being based on stale or guessed source versions.

本清单记录已检查双语覆盖情况的 Owner 分支精确版本，避免基于过期或猜测的源版本进行翻译。

A branch SHA is a source snapshot identifier, not an approval signal. A translated companion based on an unmerged Owner branch must retain that source SHA and remain clearly marked as a proposal/owner-branch source until the source design is integrated and accepted.

分支 SHA 只是源快照标识，不代表设计已批准。基于尚未合并 Owner 分支的翻译文件必须保留该 SHA，并明确标记为提案/Owner 分支来源，直到源设计完成集成验收。

## 2. Audited Owner branches / 已审查 Owner 分支

The audit below checked the core Markdown specifications in each module directory for Chinese content. The listed core files were English-only at the inspected branch heads. Phase-specific reports/addenda may contain bilingual sections and must be assessed individually; they are not counted as completed merely because one addendum is bilingual.

以下审计检查各模块目录中的核心 Markdown 规范是否包含中文。所列核心文件在检查时的分支 HEAD 上均为英文版本。阶段性报告/补充文件可能含有双语章节，必须逐份评估；不能因为其中一份补充文件是双语，就将整个模块标记为完成。

| Owner | Branch | Inspected head SHA | Core English-only specs | Bilingual status |
|---|---|---|---:|---|
| B — Domain Model | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 | 10 Phase 3 identity/typed-reference/ADR artifacts | Core six main source specs paired; Phase 3 extensions pending |
| D — Memory Brain | session-d-memory-brain-2026-11-16 | 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3 | 8 | 7/8 core specs paired; large operation/publication gate pending |
| E — Memory Compiler | session-e-memory-compiler-2026-11-16 | a1b8ba129ef7d5f4463bd4229667f0b2bf6d9886 | 8 | 2/8 core specs paired; 6 remain |
| F — Memory Runtime | session-f-memory-runtime | 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | 5 | NOT STARTED — core contracts |
| G — Memory Context | session-g-memory-context | 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | 6 | NOT STARTED — core contracts |
| C — Agent Integration | session-c-agent-integration-2026-11-16 | 0f1df3b9c8bdfbb7991cd9e18842c56c521665c4 | 10 | NOT STARTED — core contracts |
| H — BMCP Protocol | session-h-bmcp-protocol | 8150a450c73d59eba9b81f6aae30e28ab0d7a0e0 | 7 | NOT STARTED — core protocol contracts |
| I — Security & Governance | session-i-security-governance-2026-11-16 | a00173f3cf6c266f638fe89c0d2af0445e0ae30b | 8 | NOT STARTED — core policy/contracts |
| Storage / Consistency | session-storage-consistency-forget-atomicity-2026-11-16 | c49d132502420483810310a7c2948fda26c78378 | Branch contains design, review and executable reference artifacts; detailed per-file inventory pending | NOT STARTED — design and acceptance artifacts |

**Audit limitation:** Counts above include core Markdown specifications selected by module directory and exclude phase reports, change logs, baseline proposals, Python reference models, and schemas. They are not counts of every architecture-related file in the repository.

**审计限制：** 上述数量仅统计按模块目录筛选的核心 Markdown 规范，不包括阶段报告、变更日志、基线提案、Python 参考模型和 Schema。它们不是仓库全部架构文件的总数。

## 3. Translation progress / 当前翻译进度

- System-level specifications: paired for the current source set.
- B main Domain Model specifications: 6/6 paired; Phase 3 typed-reference/identity addenda and ADR-001 remain pending.
- D Memory Brain core specifications: 7/8 paired; the large operation-level Forget Fence/publication-gate contract remains pending.
- E Memory Compiler core specifications: 6/8 paired; Compiler Overview, Event Ingestion, Extraction/Normalization, Consolidation/Conflict Resolution, Accepted Receipt and Producer Admission are paired.
- F/G/C/H/I detailed core specifications: not yet paired.

All translated Owner documents retain their exact source blob SHA. Refresh branch HEAD and re-read source files before translating remaining artifacts.

## 4. Migration order / 迁移顺序

### Batch A — Canonical Memory and Compiler correctness
- D: memory-brain-overview, canonical-memory-store, memory-lifecycle-manager, entity-and-relationship-manager, memory-versioning, commit-cursor-semantics, Forget Fence/completion, publication gate.
- E: compiler-overview, event-ingestion-engine, extraction-and-normalization, consolidation-and-conflict-resolution, evidence-and-provenance, accepted-receipt/idempotency, producer-admission, Forget-derived-registration.
- Preserve the exact D/E/Storage atomic producer admission, fence, dependency registration and publication semantics. Never imply the cross-owner race is closed by translation.

### Batch B — Runtime and Context
- F: runtime overview, retrieval, activation, working-set/cache, scheduling, Forget suppression and anti-resurrection.
- G: context architecture/manager, edit operations, versioning, reconciliation, budget/sufficiency, Applied/Forget reconciliation.
- Preserve D canonical cursors, F index watermarks, G ContextVersion and delivery identifiers as distinct types.

### Batch C — Agent Integration and BMCP
- C: Agent integration overview, telemetry, capability tiers, inference boundary, final-request attestation, security/untrusted-memory boundary, conformance cases.
- H: protocol overview, message envelope/versioning, context delivery/ACK, Forget/reconnect, Adapter capability/Applied attestation, target binding, conformance matrix.
- Preserve exact Applied proof boundary, identity bindings, permission epochs, ForgetFenceGeneration and version semantics.

### Batch D — Security and Governance
- I: security/identity overview, Principal/Actor/authorization, Scope/revocation, retention/backup/erasure, global Forget inventory/completion evidence, audit/exceptions, threat model/adversarial tests.
- Translate policy and evidence semantics without turning UNKNOWN/offline/unsupported targets into successful completion.

### Batch E — Integration, Storage, and Recovery
- A: contract registry, cross-owner decisions, integration acceptance, closure plans, governance decision records.
- Storage/Consistency: COC, JF-10, prepared participant identity, restore high-water, PostgreSQL capability evidence, executable reference models and test reports.
- Preserve distinctions among domain decision, storage design, executable reference model, test execution, and production evidence.

## 5. Translation acceptance / 翻译验收

For every source artifact:
1. Record exact source branch and blob SHA.
2. Create paired English and Chinese files under docs/en and docs/zh-CN with reciprocal links.
3. Preserve all field names, enum values, type names, cursor namespaces, IDs, equations, state transitions, and schema bytes.
4. Preserve DECIDED/CANDIDATE/OPEN/BLOCKED/TO_VALIDATE and PASS/CONDITIONAL PASS/REQUEST CHANGES/NOT REVIEWABLE exactly.
5. Translate all requirements, non-requirements, caveats, failure cases, evidence claims, and explicit non-claims.
6. Record source status separately from translation review status.
7. Update docs/translation-status.md in the same change set.
8. Do not mark an unmerged owner-branch proposal as an approved main baseline.

## 6. Review/report migration / 审查报告迁移

Architecture review reports, Owner acceptance reports, ADRs, and integration decisions are architecture artifacts under GOV-DOC-001. They are migrated after their source contracts are paired, in order to preserve the exact decision context and avoid translating superseded proposals as current requirements.

架构审查报告、Owner 验收报告、ADR 和集成决议都属于 GOV-DOC-001 管辖的架构交付物。它们将在对应源契约完成双语配对后迁移，以保留准确的决策上下文，并避免把已被取代的提案翻译成当前要求。

Historical reports may be marked SUPERSEDED, but their conclusions and evidence must remain traceable. Translation does not reopen or approve the underlying decision.
