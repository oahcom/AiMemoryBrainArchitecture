# DOMAIN-REALITY-001-B — Bilingual Semantic Parity Audit
# DOMAIN-REALITY-001-B — 双语语义对等审计

- ID: B-BILINGUAL-001
- Status: **NOT PASSED — B5 BLOCKED**
- Governing policy: GOV-DOC-001 Blob b51b054b9f1022133666542680df74dfe19de2fb
- Governing invariants: I-23/I-24, architecture invariants Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe
- Audit scope: all research files currently present on branch research/domain-reality-001-b, including the supplemental Fact/Claim ADR and owner-branch snapshot errata.
- Audit date: 2026-11-17

## 1. Acceptance rule / 验收规则

A file is bilingual-complete only when the full normative content is present in both languages in the same file/change set, with semantic parity, stable-ID parity, matching decision status, matching examples/constraints and traceable source revisions. A bilingual title, summary, or translated introduction does not satisfy the policy if tables, decision clauses, schemas, invariants or test conditions remain single-language.

只有当同一文件/变更集中完整提供两种语言的全部规范内容，并且语义、稳定 ID、决策状态、示例/约束及来源版本均一致时，才算双语完整。如果表格、决策条款、Schema、不变量或测试条件仍只有一种语言，仅有双语标题、摘要或翻译后的引言并不满足规范。

## 2. File-by-file audit / 逐文件审计

| File | Current language coverage | Parity status | Required action |
|---|---|---|---|
| README.md | Bilingual purpose and governance sections; work-plan tables and some status details are English-only | PARTIAL | Translate all table cells, gate explanations and remaining-work statements |
| existing-domain-model-baseline.md | Bilingual executive summaries and selected sections; most evidence tables and issue/PR rows are English-only | PARTIAL | Full Chinese peer for every evidence table, branch row, conflict, missing definition and gate conclusion |
| baseline-currentness-and-owner-source-audit.md | Many bilingual sections; several owner/source tables and detailed Phase 3.8 findings are English-only | PARTIAL | Translate all tables, currentness corrections, issue state and test authority evidence |
| baseline-owner-branch-snapshot-errata.md | Bilingual headings and paragraphs; snapshot table and gate effects are English-only | PARTIAL | Translate the owner/branch/commit/artifact table and all scope/gate conditions |
| fact-claim-identity-adr.md | Chinese peers added for source evidence, conceptual/identity alternatives, decision matrix, authority acceptance table and all eight required examples; Blob `0bbea0beec6a5828c2db5ae267fac40f59ad7f1f` | REMEDIATED — MANUAL PARITY REVIEW PENDING | Independently compare each alternative, matrix cell, example and ADR status; ensure no recommendation was promoted to decision |
| canonical-domain-entity-inventory.md | Bilingual headings and narrative; most entity/classification tables are English-only | PARTIAL | Translate each concept row, rationale, status and open question |
| canonical-identity-semantics.md | Full Chinese peer text added for canonical distinctions, stability rules, typed namespaces, trust-resolution order, serialization types, open questions and decision record; Blob `bc8816eadcd14a1dd01ae03ed68de553b2bb1483` | REMEDIATED — MANUAL REVIEW PENDING | Independently verify type distinctions, authority boundaries, exact pins and no semantic drift |
| canonical-state-semantics.md | Full Chinese peer text added for state matrices, critical terms, ordering, state-machine requirements, owner evidence and blockers; Blob `2c42b4b9d8311e218d0e6fadd7b1f3a7d9c10017` | REMEDIATED — MANUAL REVIEW PENDING | Independently verify every state/authority/proof boundary and the new B-STATE-007 alignment |
| canonical-temporal-evidence-semantics.md | Bilingual headings and selected paragraphs; time/evidence tables and much of the provenance section are English-only | PARTIAL | Translate all field definitions, alternatives, invariants and open decisions |
| canonical-domain-relationships.md | Bilingual headings and short explanations; relationship/cardinality matrix is English-only | PARTIAL | Translate every relation, cardinality, owner, deletion and tenant rule |
| domain-model-complexity-assessment.md | Bilingual headings and selected narrative; entity and complexity tables are English-only | PARTIAL | Translate every assessment row, classification and recommendation |
| mature-domain-model-research.md | Bilingual executive synthesis and selected conclusions; detailed external-reference findings and tables are mostly English-only | PARTIAL | Provide complete Chinese equivalent for every DDD/ES/Temporal/Graph/standard/project finding |
| cross-owner-canonical-semantics-matrix.md | Bilingual headings and selected explanation; source ledger and semantic matrix are English-only | PARTIAL | Translate every Owner, artifact pin, concept row, status and conflict |
| domain-semantics-conflict-register.md | Bilingual headings and some explanatory text; conflict rows and resolution conditions are English-only | PARTIAL | Translate all conflict records and decision authority/closure conditions |
| canonical-domain-invariants.md | Full English/Chinese peer columns added for identity, relation, temporal, evidence, state, Forget, protocol, authentication, serialization invariants and all candidate tests; new Blob `51792426bb71609ceecf8d13491f9ab0b36c91eb` | REMEDIATED — MANUAL PARITY REVIEW PENDING | Independently compare every ID/row and confirm no semantic drift; do not treat author translation as independent verification |
| canonical-domain-glossary.md | Chinese term column exists; definitions, non-definitions, owners and status columns are English-only | PARTIAL | Translate every definition, non-definition, related concept and status |
| canonical-domain-model.md | Bilingual headings and selected narrative; entity lists, ownership tables and blocking issues are English-only | PARTIAL | Full Chinese equivalent for model, diagrams, owner boundaries and gate constraints |
| domain-model-decision-record.md | Bilingual headings and selected decisions; detailed ADR context/alternatives/consequences are English-only | PARTIAL | Translate every decision record field and rejected alternative |
| validation/README.md | Full Chinese peer text added for test scope, schema prerequisites, future validation and current result; Blob `a2bb3d494fadd5ae411d9b8227d83dd50a16a895` | REMEDIATED — MANUAL REVIEW PENDING | Verify test-section reference and clause equivalence against invariants/owner contracts |
| evidence/README.md | Chinese peers added for all source titles, section descriptions, evidence limitations and version caveats; Blob `bda915327a0ee77fb78e9a52bc094986254a1a60` | REMEDIATED — MANUAL REVIEW PENDING | Verify official URLs, product-version scope and no stronger claims than source evidence |
| evidence/official-reference-validation.md | English headings and Chinese peer explanations are present for each major section; source links and some “do not infer” clauses require line-by-line comparison | PROVISIONAL — RECHECK | Perform clause-by-clause parity check and align source/version notes |
| bilingual-parity-audit.md | Bilingual acceptance rules and selected narrative; file-by-file table and status/action cells are English-only | PARTIAL | Translate every audit row and re-audit after all other files are translated |

## 3. Current conclusion / 当前结论

**B5 MUST NOT PASS.** Most normative files are only partially bilingual. The presence of Chinese headings and selected translated paragraphs must not be presented as full bilingual compliance. The branch is a research draft only.

**B5 不得通过。** 大多数规范文件目前仅部分双语。不得将中文标题和部分翻译段落描述为完整双语合规。本分支目前仅为研究草稿。

## 4. Required remediation / 必需整改

1. Translate every English-only table and normative paragraph into complete Chinese peer text.
2. Preserve the same stable IDs, field names, enum values, statuses, evidence pins and decision references in both languages.
3. Use terminology from canonical-domain-glossary.md; where Chinese and English are not exact one-to-one, explain the semantic distinction.
4. Compare both language versions clause by clause; do not rely on translation by summary.
5. Re-run internal-link, stable-ID, status and source-pin checks after translation.
6. Have a separate independent reviewer verify bilingual parity and high-risk semantic equivalence.
7. Only then update README B5 and PR #55 to reflect the actual verified state.

1. 将每个仅有英文的表格和规范段落完整翻译为中文对照文本。
2. 两种语言必须保留相同的稳定 ID、字段名、枚举值、状态、证据 Pin 和决策引用。
3. 使用 canonical-domain-glossary.md 中的术语；如果中英文不能严格一一对应，必须解释语义差异。
4. 逐条对照两个语言版本；不得以摘要翻译代替完整翻译。
5. 翻译后重新检查内部链接、稳定 ID、状态和来源 Pin。
6. 由独立审查者核验双语对等及高风险语义一致性。
7. 只有完成上述工作后，才可以更新 README B5 和 PR #55 的实际验证状态。

## 5. Gate / 门禁

- B5: BLOCKED — bilingual parity incomplete.
- B6: INDEPENDENT_REVIEW_PENDING.
- No review/acceptance/merge status may be inferred from this audit.


## 6. Remediation progress / 整改进展

- `canonical-domain-invariants.md` has been rewritten with Chinese peers for every invariant row, positive/negative condition, candidate test setup/result and validation/gate statement. Current Blob: `51792426bb71609ceecf8d13491f9ab0b36c91eb`.
- This is author-side remediation only. It is not an independent semantic parity pass. B5 remains BLOCKED until the remaining P0/P1/P2 files are translated and a separate reviewer checks exact clause/row equivalence.

- `canonical-domain-invariants.md` 已为每条不变量、正/负条件、候选测试前置条件/预期结果以及验证/门禁说明补齐中文对应内容。当前 Blob：`51792426bb71609ceecf8d13491f9ab0b36c91eb`。
- 这仅是作者侧整改，不构成独立语义一致性验收。剩余 P0/P1/P2 文件完成翻译并由独立审查者逐条核对后，B5 才能解除阻塞。


- `canonical-state-semantics.md` has also been rewritten with Chinese peer text for all state matrices, critical execution terms, ordering constraints, state-machine requirements, cross-owner evidence and blockers. Current Blob: `2c42b4b9d8311e218d0e6fadd7b1f3a7d9c10017`.
- `canonical-state-semantics.md` 也已为所有状态矩阵、关键执行术语、顺序约束、状态机要求、跨 Owner 证据和阻塞项补齐中文对应内容。当前 Blob：`2c42b4b9d8311e218d0e6fadd7b1f3a7d9c10017`。


- `canonical-state-semantics.md` current Blob: `2c42b4b9d8311e218d0e6fadd7b1f3a7d9c10017`; full Chinese peer text has been added, including B-STATE-007 for the I-10 ACK sufficiency ambiguity.
- `canonical-state-semantics.md` 当前 Blob：`2c42b4b9d8311e218d0e6fadd7b1f3a7d9c10017`；已补齐完整中文对应内容，包括针对 I-10 ACK 充分性歧义的 B-STATE-007。


- `canonical-identity-semantics.md` has received a full Chinese peer for all tables, rules, resolution steps, unresolved questions and decision record. Current Blob: `bc8816eadcd14a1dd01ae03ed68de553b2bb1483`.
- `fact-claim-identity-adr.md` now has Chinese peers for its evidence, decision matrices, authority requirements and all eight validation examples. Current Blob: `0bbea0beec6a5828c2db5ae267fac40f59ad7f1f`.
- `evidence/README.md` now has Chinese peers for all source titles, source-purpose labels, evidence limitations and version caveats. Current Blob: `bda915327a0ee77fb78e9a52bc094986254a1a60`.
- `canonical-identity-semantics.md` 已为全部表格、规则、解析步骤、未决问题和决策记录补齐中文对应内容。当前 Blob：`bc8816eadcd14a1dd01ae03ed68de553b2bb1483`。
- `fact-claim-identity-adr.md` 已为证据表、决策矩阵、Owner 验收要求和全部八个验证示例补齐中文对应内容。当前 Blob：`0bbea0beec6a5828c2db5ae267fac40f59ad7f1f`。
- `evidence/README.md` 已为所有来源标题、来源用途说明、证据局限和版本注意事项补齐中文对应内容。当前 Blob：`bda915327a0ee77fb78e9a52bc094986254a1a60`。
