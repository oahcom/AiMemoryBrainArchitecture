# Bilingual Semantic Parity Audit
# 双语语义一致性审计

- ID: B-PARITY-001
- Status: BLOCKING FINDING — B5 NOT PASSED
- Audited branch snapshot: `research/domain-reality-001-b` at `c9741e50f44d0468cd9d64ce27c4309c8c61990a`
- Date: 2026-11-17
- Scope: all 21 PR files under DOMAIN-REALITY-001-B
- Method: section-level bilingual-presence screen and direct inspection of representative normative tables/prose. This is a screening audit, not a completed human semantic-equivalence review.

## 1. Executive result / 总体结果

The PR package contains 21 files. The screen flagged 135 sections across 20 files containing English substantive content with no Chinese text in the same section. README.md was the only file with no section flagged. This does not mean every flagged section is mistranslated; it means same-change-set Chinese semantic peers are absent from those sections, so the B5 bilingual coverage requirement is not met.

PR 包含 21 个文件。筛查在 20 个文件中标记出 135 个章节，这些章节包含英文实质内容，但同一章节没有中文文本。README.md 是唯一未被标记的文件。这不表示每个标记章节都存在错误翻译；它表示这些章节缺少同一变更集中的中文语义对应内容，因此 B5 双语覆盖要求尚未满足。

Direct inspection confirms substantive gaps: entity/value-object inventory tables, invariant positive/negative conditions, decision records, owner matrices, validation instructions and ADR decision matrices contain English-only rows or prose. Chinese headings or a glossary paragraph do not satisfy semantic parity.

直接检查确认存在实质缺口：实体/值对象清单、不变量正负条件、决策记录、Owner 矩阵、验证说明和 ADR 决策矩阵均包含仅英文行或正文。中文标题或一段术语解释不能满足语义一致性。

## 2. Per-file screen / 逐文件筛查

Counts are heuristic flagged sections, not translation-error counts. Blob SHAs pin the exact audited file contents.

下列数字为启发式标记章节数，不是翻译错误数量。Blob SHA 固定本次审计的精确文件内容。

| File | Blob SHA | Flagged sections | Priority |
|---|---|---:|---|
| `README.md` | `0820207f9a1d3988fd2c84a13891617c6e4648a2` | 0 | P3 |
| `baseline-currentness-and-owner-source-audit.md` | `27057979cf30da01dc997dbe9f24707e22faccdb` | 1 | P2 |
| `baseline-owner-branch-snapshot-errata.md` | `88bea224e47c6e0bb9a1f60df4c20232799caae5` | 1 | P2 |
| `canonical-domain-entity-inventory.md` | `2e0d45dfef9db2ddee19493cd274194312ad6332` | 6 | P1 |
| `canonical-domain-glossary.md` | `10be80348815c700211a3a2ee9fa602bed50dbd6` | 1 | P2 |
| `canonical-domain-invariants.md` | `1a0d8d8cc32ea03a9350e4184ceffb1a74c9ef3b` | 11 | P0 |
| `canonical-domain-model.md` | `bb7a7adbc34dc8a7323471d6ad30d20841ccab37` | 11 | P0 |
| `canonical-domain-relationships.md` | `c1f8e41a5af56bc867ee41c0a6f93fc44f84a26c` | 5 | P1 |
| `canonical-identity-semantics.md` | `80c9eebdd0cadb7f3590a7d18698b671b3ad2c47` | 7 | P0 |
| `canonical-state-semantics.md` | `7b0a1c0d499a0f9c59e1954cd17636f2ba82ad59` | 8 | P0 |
| `canonical-temporal-evidence-semantics.md` | `e340686f818b1dc678ed834891853ca3e554bd49` | 5 | P0 |
| `cross-owner-canonical-semantics-matrix.md` | `e5d846442bd8415cd5c5a33fd3a1deba36c6059b` | 7 | P0 |
| `domain-model-complexity-assessment.md` | `1586d2321fc09bb320c75ffaacb80a61fe18402f` | 11 | P1 |
| `domain-model-decision-record.md` | `88ac6fd16e82a28615e4ceab0d4ceb6ea8c8107b` | 14 | P0 |
| `domain-semantics-conflict-register.md` | `ee807591f5f642684dfa23cf4dd63ff1196b1c0d` | 4 | P0 |
| `evidence/README.md` | `b5e180da0289981b67db0957323ddebf8685fdfc` | 7 | P2 |
| `evidence/official-reference-validation.md` | `04cb4462de59f6855727f95acdd5ad58f97bdb59` | 1 | P3 |
| `existing-domain-model-baseline.md` | `b8bed3b586f81141aa784783b0b150069db5bf51` | 10 | P0 |
| `fact-claim-identity-adr.md` | `96a2ee7d595fcd4a214201a7c7b6b2a9c3deb961` | 4 | P0 |
| `mature-domain-model-research.md` | `0e6a3b63103a3a6cdf36ecff93648b18053ec655` | 16 | P1 |
| `validation/README.md` | `b68e5ee136fdadba734c9a53e57ef6979cfc4b21` | 5 | P0 |

## 3. Representative exact findings / 代表性精确发现

1. **Entity inventory:** Sections 2–5 contain English-only rationale/status cells for Event, Memory, Memory Version, Claim, Entity, Relation, Evidence, Provenance, Context, Scope, value objects and protocol/security concepts. The one Chinese classification paragraph does not translate those rows.
2. **Invariants:** Identity, relation, temporal, evidence, state, Forget, protocol and authentication invariant tables contain English-only positive/negative conditions; the test catalogue is also English-only.
3. **Decision record:** B-DEC context/problem/alternatives/evidence/decision/consequence/complexity/owner/status blocks are English-only.
4. **Cross-owner matrix:** Source ledger, Owner authority boundaries and semantic conflict summaries lack Chinese row-level counterparts.
5. **Validation / ADR:** Validation prerequisites and result, plus Fact/Claim decision matrix, required Owner decisions and examples, are English-only.

1. **实体清单：**第 2–5 节中的 Event、Memory、Memory Version、Claim、Entity、Relation、Evidence、Provenance、Context、Scope、值对象及协议/安全概念，其理由/状态单元格只有英文。单独的中文分类说明不能翻译这些行。
2. **不变量：**身份、关系、时间、证据、状态、Forget、协议和认证不变量表中的正/负条件只有英文；测试目录也只有英文。
3. **决策记录：**B-DEC 的背景/问题/备选/证据/决策/后果/复杂度/Owner/状态块只有英文。
4. **跨 Owner 矩阵：**来源台账、Owner 权威边界和语义冲突摘要缺少逐行中文对应。
5. **验证/ADR：**验证前置条件与结果，以及 Fact/Claim 决策矩阵、Owner 决策要求和示例均只有英文。

## 4. Remediation order / 修复顺序

1. **P0 first:** canonical model, identity, state, temporal/evidence, invariants, cross-owner matrix, decision record, conflict register, existing baseline, validation README and Fact/Claim ADR.
2. **P1 next:** entity inventory, relationships, complexity assessment and mature-domain research.
3. **P2/P3:** glossary, evidence index, audit addenda and README metadata.
4. Translate every normative table row/cell, not only headings or column labels. Preserve IDs, enums, exact version pins, status, Owner, severity, exceptions and negative conditions.
5. Perform bidirectional paragraph/table-row semantic comparison; verify neither language adds or omits a normative condition.
6. Re-fetch changed files and record new Blob SHAs. The heuristic scan itself is not a passing parity test.

1. **优先 P0：**规范模型、身份、状态、时间/证据、不变量、跨 Owner 矩阵、决策记录、冲突登记、现有基线、Validation README 和 Fact/Claim ADR。
2. **其次 P1：**实体清单、关系、复杂度评估和成熟领域研究。
3. **最后 P2/P3：**术语表、证据索引、审计补充和 README 元数据。
4. 必须逐行/逐单元格翻译规范表格，不能只翻译标题或列名。保留 ID、枚举、精确版本 Pin、状态、Owner、严重级别、例外和负向条件。
5. 双向比较段落/表格行语义，确认两种语言均未增加或遗漏规范条件。
6. 修改后重新读取文件并记录新 Blob SHA。启发式扫描本身不构成双语一致性通过证明。

## 5. Gate disposition / 门禁结论

B5 is **BLOCKED / NOT PASSED** by bilingual semantic coverage, consistent with B-CONFLICT-016. No waiver is assumed. No canonical freeze, schema freeze, implementation authorization or ACCEPTED status may be claimed until P0/P1/P2 remediation and manual semantic parity review are complete.

B5 因双语语义覆盖处于 **BLOCKED / NOT PASSED**，与 B-CONFLICT-016 一致。不假定存在豁免。P0/P1/P2 修复和人工语义一致性复审完成前，不得宣称规范冻结、Schema 冻结、实现授权或 ACCEPTED。
