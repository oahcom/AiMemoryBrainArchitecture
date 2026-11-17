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

The audit below checked the core Markdown specifications in each module directory for Chinese content at the exact historical Owner branch heads listed in the table. Those source-branch snapshots are intentionally preserved as audit evidence; the separate PR #28 companion status is recorded in Section 3 below. Phase-specific reports/addenda are not counted as completed merely because one addendum is bilingual.

以下审计是在表中列明的历史 Owner 分支精确 HEAD 上检查各模块核心 Markdown 规范是否包含中文。为保留审计证据，表中源分支快照状态不被改写；PR #28 中双语对应文件的当前状态另见下文第 3 节。阶段性报告/补充文件必须逐份评估，不能因为其中一份补充文件是双语，就将整个模块标记为完成。

| Owner | Branch | Inspected head SHA | Core English-only specs | Bilingual status |
|---|---|---|---:|---|
| B — Domain Model | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 | 10 Phase 3 identity/typed-reference/ADR artifacts | Core six main source specs paired; Phase 3 extensions pending |
| D — Memory Brain | session-d-memory-brain-2026-11-16 | 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3 | 8 | Historical source-branch audit only; PR #28 now contains 8/8 bilingual companions |
| E — Memory Compiler | session-e-memory-compiler-2026-11-16 | a1b8ba129ef7d5f4463bd4229667f0b2bf6d9886 | 8 | 2/8 core specs paired; 6 remain |
| F — Memory Runtime | session-f-memory-runtime | 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | 5 | Historical source-branch audit only; PR #28 now contains 5/5 bilingual companions; semantic review pending |
| G — Memory Context | session-g-memory-context | 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | 6 | NOT STARTED — core contracts |
| C — Agent Integration | session-c-agent-integration-2026-11-16 | 0f1df3b9c8bdfbb7991cd9e18842c56c521665c4 | 10 | NOT STARTED — core contracts |
| H — BMCP Protocol | session-h-bmcp-protocol | 8150a450c73d59eba9b81f6aae30e28ab0d7a0e0 | 7 | NOT STARTED — core protocol contracts |
| I — Security & Governance | session-i-security-governance-2026-11-16 | a00173f3cf6c266f638fe89c0d2af0445e0ae30b | 8 | NOT STARTED — core policy/contracts |
| Storage / Consistency | session-storage-consistency-forget-atomicity-2026-11-16 | c49d132502420483810310a7c2948fda26c78378 | Branch contains design, review and executable reference artifacts; detailed per-file inventory pending | NOT STARTED — design and acceptance artifacts |

**Audit limitation:** Counts above include core Markdown specifications selected by module directory and exclude phase reports, change logs, baseline proposals, Python reference models, and schemas. They are not counts of every architecture-related file in the repository.

**审计限制：** 上述数量仅统计按模块目录筛选的核心 Markdown 规范，不包括阶段报告、变更日志、基线提案、Python 参考模型和 Schema。它们不是仓库全部架构文件的总数。

## 3. PR #28 companion status / PR #28 双语对应文件状态

- System-level specifications: paired for the current source set.
- B main Domain Model specifications: 6/6 paired; two Phase 3 identity/Scope and Principal/Actor companions now paired against exact Owner Blob SHAs; ADR-001 remains ADR-BLOCKED and INT-P0-02 / INT-X-03 remain OPEN.
- D Memory Brain core specifications: 8/8 bilingual companions present in PR #28, including the four-part operation/publication gate. Source-branch reconciliation and semantic acceptance remain pending.
- E Memory Compiler core specifications: 7/8 paired; Compiler Overview, Event Ingestion, Extraction/Normalization, Consolidation/Conflict Resolution, Evidence/Provenance, Accepted Receipt and Producer Admission are paired. Only Forget Fence/Derived Registration remains.
- F Memory Runtime: 5/5 detailed core specifications paired in PR #28; independent semantic review pending.
- G/C/H/I detailed core specifications: not yet paired; reader guides only.

All translated Owner documents retain their exact source blob SHA. Refresh branch HEAD and re-read source files before translating remaining artifacts. Pair presence is not semantic approval or source-branch integration.

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


## 7. Phase 3.6 targeted source refresh — 2026-11-17

The following exact source Blob SHAs were re-read directly from their named Owner branches for the PR #28 high-risk follow-up. These are file Blob SHAs, not branch HEADs or approval signals.

| Owner | Source path | Branch | Current file Blob SHA | Preserved source state |
|---|---|---|---|---|
| B | `02-domain-model/typed-reference-and-scope-semantics.md` | `session-b-domain-model-phase3` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | CANDIDATE; Claim identity conditional on ADR-001 |
| B | `02-domain-model/principal-actor-binding-mapping.md` | `session-b-domain-model-phase3` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | CANDIDATE; INT-P0-02 / INT-X-03 OPEN |
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | C decisions recorded; C/G/H freeze BLOCKED; implementation/execution NOT VERIFIED |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G decisions recorded; C/G/H freeze BLOCKED; implementation/execution NOT VERIFIED |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `session-h-bmcp-protocol` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | JOINT-DECIDED technical baseline; governance/consumer acceptance OPEN; implementation/conformance NOT VERIFIED |
| H | `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md` | `session-h-bmcp-protocol` | `8afb914731a34d8ab44331f54f1f39bfd8ec37ce` | JOINT-DECIDED technical design; governance BLOCKED; H36 NOT RUN |
| I | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `session-i-security-governance-2026-11-16` | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED technical baseline; governance BLOCKED; implementation/conformance NOT VERIFIED |
| Storage | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `175ee7b1349cfdb79a19898b311a88391ed88010` | Logical proposal; physical topology and implementation proof OPEN |
| Storage | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` | ADR-BLOCKED; candidate options only; no deployed topology selected |
| Storage | `reviews/storage-consistency/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | CANDIDATE; I acceptance required; NOT IMPLEMENTED; NOT RUN; JF-10 P0 OPEN |
| Storage | `reviews/storage-consistency/phase-3.6.5-restore-control-highwater-and-quarantine-contract.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `4f656163aeba532a441eaed1d293a48e2363cb4a` | CANDIDATE; exact I-D-A-Storage review required; restore remains fenced |

### Currentness findings

- **BSR-28-005 — OPEN:** H's identity status report records historical protected-operation Blob `9845c97ac43d7888732afafe12e28850ec02add8`; live branch readback now returns `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`. Preserve the historic record and request a dated H currentness correction.
- **BSR-28-006 — OPEN:** the previously cited Storage topology Blob `080433f8e13a500522bc2754da64057edb0ae9d8` is no longer the live path Blob; readback returns `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`. The ADR remains BLOCKED and no topology is selected.
- **BSR-28-007 — OPEN:** PR #28 contains a bilingual pair for the H identity consumer/conformance status report only. This is not one of the seven H normative core-spec pairs and does not complete B/C/G/H/I/Storage detailed contracts.

Full findings and disposition: [Phase 3.6 identity / Applied / Storage source audit](../reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md).


## 8. B Phase 3 bilingual companion batch — 2026-11-17

| Source | Owner branch | Exact source Blob SHA | PR #28 pair | Source state |
|---|---|---|---|---|
| `02-domain-model/typed-reference-and-scope-semantics.md` | `session-b-domain-model-phase3` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | EN + zh-CN companions | CANDIDATE; Claim identity conditional on ADR-001; I36-GOV-03/04 GOVERNANCE-BLOCKED |
| `02-domain-model/principal-actor-binding-mapping.md` | `session-b-domain-model-phase3` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | EN + zh-CN companions | CANDIDATE; INT-P0-02 / INT-X-03 OPEN; no identity freeze |

These source Blob SHAs were re-read from the named B Owner branch in this turn. They are file Blob SHAs, not branch HEADs or approval evidence. Translation pairing does not approve I policy, H wire fields, D/E schema migrations, or ADR-001.


## 9. C Phase 3.6 final-request evidence pair — 2026-11-17

| Owner source | Branch | Exact Blob SHA | Paired docs | Source state |
|---|---|---|---|---|
| `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | EN + zh-CN | C semantic decisions recorded; C/G/H cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED; C-FR-01..12 NOT RUN |

This is 1 of 10 C detailed core specifications, not completion of the C set. C's approval with enumerated exceptions does not approve H wire, G Applied state authority, I authorization, D Forget fence or runtime implementation.


## 10. C/G/H Phase 3.6 Applied cross-owner review — 2026-11-17

| Owner | Source path | Branch | Exact source Blob SHA | Companion status | Preserved source state |
|---|---|---|---|---|---|
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | EN + zh-CN pair present; targeted parity review PASS | C semantic decisions recorded; C/G/H freeze BLOCKED; C-FR-01..12 NOT RUN; implementation NOT VERIFIED |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | Pair NOT YET CREATED; cross-owner semantic review recorded | G decisions recorded; C/G/H freeze BLOCKED; implementation/execution NOT VERIFIED |
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `ed6b43a29aa368d772c701ffc83309a5aadf3c00` | Pair BLOCKED pending H/C exact field mapping; H36-AP-01..07 OPEN | CANDIDATE; final-request proof profile OPEN with C; authorization binding OPEN with I |

Cross-owner report: `reviews/translation/2026-11-17-cgh-applied-contract-cross-owner-review.md` and Chinese companion. The six-stage lifecycle and historical/current-use semantics align; H's exact wire field mapping is not yet sufficient for a faithful normative translation. This report is not Owner approval, wire freeze, implementation verification or conformance execution.


## H candidate field-mapping revision — 2026-11-17

| Owner | Source path | Branch | Current exact Blob SHA | Revision / status |
|---|---|---|---|---|
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `db59b63e322d7255b8b400f47859dcac32bb3027` | §11 candidate field-mapping proposal added; C/G acceptance and I/D/B authority confirmations pending; wire/schema freeze NO; implementation/conformance NOT VERIFIED / NOT RUN |

The prior reviewed Blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00` is superseded for currentness by the exact live Blob above. This is a candidate revision, not an Owner approval or C/G/H freeze. H bilingual companions remain pending until exact-version review and acceptance.


## H Adapter Capability / Applied Attestation bilingual pair — 2026-11-17

| Owner | Source path | Branch | Exact source Blob SHA | EN companion | zh-CN companion | Review / source state |
|---|---|---|---|---|---|---|
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `db59b63e322d7255b8b400f47859dcac32bb3027` | `docs/en/08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `docs/zh-CN/08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | 22/22 headings; 33/33 table rows; targeted parity PASS; source CANDIDATE; C proof profile OPEN; I authorization binding OPEN; NOT FROZEN |

Review reports: `reviews/translation/2026-11-17-h-adapter-capability-applied-bilingual-review.md` and Chinese companion. This is 1 of H's 7 detailed core specifications, not H-set completion. C/G/I/D/B approvals and implementation/conformance evidence remain separate.


## G Phase 3.6 Applied / Forget / Reconciliation bilingual pair — 2026-11-17

| Owner | Source path | Branch | Exact source Blob SHA | EN companion | zh-CN companion | Review / source state |
|---|---|---|---|---|---|---|
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | `docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | 21/21 headings; 37/37 table rows; targeted parity PASS; G decisions recorded; C/G/H freeze BLOCKED; implementation NOT VERIFIED; G-36-01..15 NOT RUN |

Review reports: `reviews/translation/2026-11-17-g-phase36-applied-forget-bilingual-review.md` and Chinese companion. The pair includes the full G Owner decision history through the exact CGH-APPLIED-1.1 recovery-batch amendment. Translation does not extend or globalize any pinned Owner decision.



## H recovery-batch candidate source refresh — 2026-11-17

| Owner | Source path | Branch | Current exact Blob SHA | Companion parity / disposition |
|---|---|---|---|---|
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `0dca3dc5463a02be0e19524811afbae87795baf5` | EN + zh-CN refreshed; 23/23 headings; 33/33 table rows; candidate mapping §11.8; H36-AP-08 OPEN; C/G/I/D/Storage acceptance pending; no schema freeze |

Supersedes the previous H source Blob `db59b63e322d7255b8b400f47859dcac32bb3027`. The H companion remains 1/7 detailed core specifications.



## H provider outcome / owner gate source refresh — 2026-11-17

| Owner | Source path | Branch | Current exact Blob SHA | Companion parity / disposition |
|---|---|---|---|---|
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `74be8374a67da385a5f0f8e34c7aef2b38b72bcf` | EN + zh-CN refreshed; 24/24 headings; 33/33 table rows; §11.9 C provider outcome/owner gate mapping; H36-AP-09 OPEN; no wire schema/SDK mapping or consumer acceptance |

Supersedes H Blob `0dca3dc5463a02be0e19524811afbae87795baf5`. H companion remains 1/7 detailed core specifications.
