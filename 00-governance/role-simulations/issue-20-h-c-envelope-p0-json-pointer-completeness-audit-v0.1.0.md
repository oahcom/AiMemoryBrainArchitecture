# H/C Outer Envelope P0 JSON-Pointer Completeness Audit v0.1.0
# H/C 外层 Envelope P0 JSON Pointer 完整性审计 v0.1.0

- Status: **P COORDINATOR SOURCE-LEVEL FINDING / H OWNER CORRECTION REQUIRED / NOT NORMATIVE**
- H schema 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- C corrected signer/P0 candidate Blob: `310e7e0073d3c32f594bc151f10c249c828ce30f`
- H exact JSON-Pointer mapping Blob: `4ba7e1699215d02224f805a15484b1da2e40c03f`
- Audit method: mechanically compare the H schema's `commonEnvelope` properties plus the `C_PROVIDER_OUTCOME_RECORDED` oneOf branch properties against the pointer rows in H Phase 3.8.20.
- P HEAD before audit: `e3663f542e49b4f325561a1e78bb8ee2c8574a81`

## 1. Result / 结果

The schema contains:
- `commonEnvelope`: 33 properties;
- `C_PROVIDER_OUTCOME_RECORDED` branch: 42 properties;
- unique top-level schema properties across the composed message: **69**;
- required properties across common envelope + C branch: **48**;
- pointer rows found in H Phase 3.8.20 table: **68**.

The only schema property not represented as a row in the H JSON-Pointer inventory table is:

`/coc_previous_entry_digest`

The C corrected P0 candidate and H mapping's exclusion section both explicitly classify this field as coordinator-appended COC evidence excluded from the C-origin outer P0. Therefore this is **not currently an identified P0 inclusion error**. It is an **inventory completeness/documentation defect**: the mapping table lists the other coordinator-appended COC fields as excluded rows but omits this one, despite calling the table the exact JSON-Pointer inventory.

No required schema property is missing from the table's included/excluded pointer set after accounting for the declared P0 exclusions; the omission is specifically the explicit excluded-field row for `coc_previous_entry_digest`.

## 2. Required H correction / H 必需修正

Add an explicit row to Phase 3.8.20:

| JSON Pointer | Source schema | Outer P0 | Notes |
|---|---|---:|---|
| `/coc_previous_entry_digest` | commonEnvelope | No | Coordinator-appended COC chain evidence; independently verify and join to the signed C-origin message |

Then rerun the mechanical inventory check and update the H mapping Blob. C, I, Storage and A reviews that bind the old mapping Blob must be refreshed to the corrected Blob. Do not silently change the C-origin P0 exclusion semantics; the proposed correction is to make the existing exclusion explicit in the table.

## 3. Other checks / 其他检查

- H `commonEnvelope` has 33 properties and the C message-family branch has 42 properties.
- All 48 required members appear in the mapping table.
- The 68 mapped pointer rows are unique at the top-level JSON Pointer path.
- The missing row is the only schema property absent from the table.
- This audit does not establish cryptographic correctness of the P0 extractor, JCS canonicalization, digest recomputation or signature verification; H Phase 3.8.19's callbacks remain test doubles.
- The P0 mapping is still a candidate, not a frozen wire contract.

## 4. Disposition / 结论

**P1 DOCUMENTATION COMPLETENESS FINDING.** H should add the explicit excluded pointer row and publish a successor mapping Blob. The exact P0 exclusion itself remains consistent with C's corrected candidate; do not change its meaning without C approval.

本项为 **P1 文档完整性问题**。H 应补充明确的排除 Pointer 行并发布后继 Mapping Blob。现有 P0 排除语义与 C 修正候选一致；未经 C 批准不得改变其含义。

This is a coordinator source-level audit, not an H Owner signature or independent security approval.
