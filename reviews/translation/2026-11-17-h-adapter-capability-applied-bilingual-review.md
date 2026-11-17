# H Adapter Capability / Applied Attestation Bilingual Review

- Date: 2026-11-17
- Source branch: `session-h-bmcp-protocol`
- Exact source path: `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- Exact source Blob SHA: `db59b63e322d7255b8b400f47859dcac32bb3027`
- Scope: structural parity and targeted semantic review of the complete EN/zh-CN companion pair.
- Non-goal: Owner approval, protocol/schema freeze, cryptographic approval, implementation verification, interoperability or conformance execution.

## 1. Artifacts

- EN: `docs/en/08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- zh-CN: `docs/zh-CN/08-bmcp-protocol/adapter-capability-and-applied-attestation.md`

The English companion embeds the exact source text and source Blob pin. The Chinese companion carries the same source pin and reciprocal language link.

## 2. Structural readback

| Measure | Owner source | English | Chinese |
|---|---:|---:|---:|
| Headings | 22 | 22 | 22 |
| Table rows (including header/separator rows) | 33 | 33 | 33 |
| Sections | 1–11, including 11.1–11.7 | Same | Same |

The exact Owner source, EN companion and zh-CN companion were fetched back from their respective branches. The English companion contains the exact source content. The Chinese companion preserves the full section hierarchy and table row structure.

## 3. Semantic checks

- Capability declaration and CapabilityEpoch invalidation remain distinct from per-request evidence.
- Tier 1 requires final immutable request observation and successful submit; Tier 2 cannot claim Full; Tier 3 is transport-only.
- The six-stage C/G lifecycle is not collapsed; H does not own G Applied acceptance.
- H's §11 is explicitly CANDIDATE and requires C/G/I/D/B owner decisions. It does not claim wire freeze.
- Exact request/boundary identity, Context/Delivery/attempt, Managed Region inventory/coverage/digest, verifier-bound identity, I/D authority refs, provenance, per-request bypass, replay identity and temporal ordering are retained.
- Forget ACK and Applied Attestation remain separate evidence families.
- The privacy non-claims remain: digest is not anonymization; raw prompt/memory text is not included by default.
- H conformance cases remain SPECIFIED / NOT RUN; implementation and interoperability remain NOT VERIFIED.

No material semantic divergence was found in this targeted translation review.

## 4. Disposition

**Bilingual parity: PASS for this exact source Blob only.**

**Source status remains unchanged:** CANDIDATE; final-request proof profile OPEN with C; authorization binding OPEN with I. C/G/H freeze remains BLOCKED. This review does not count as H Owner acceptance, C/G acceptance, I/D/B approval, wire/schema freeze, implementation verification or test execution.

## 5. H recovery-batch mapping follow-up

H added §11.8 for the CGH-APPLIED-1.1 causal-order and recovery-batch evidence bridge. The current exact H source Blob is now `0dca3dc5463a02be0e19524811afbae87795baf5`, superseding `db59b63e322d7255b8b400f47859dcac32bb3027`. EN/zh-CN companions were refreshed to this exact source.

Updated structural readback: 23/23 headings and 33/33 table rows across source, EN and zh-CN; EN content remains exact source text. The §11.8 candidate mapping preserves COC terminal proof, recovery-batch identity/digest, pre-batch participant completeness, owner high-water attestations, participant reconciliation, I terminal/revocation evidence, D lineage/cutoff/effective-position evidence and Storage same-XID terminal evidence.

This follow-up is still **CANDIDATE / NOT FROZEN**. The report's original 22-heading count is superseded by this 23-heading readback. No H schema/SDK generation, owner approval or conformance execution is implied.

## 6. C provider outcome / owner gate release mapping follow-up

H added §11.9 to explicitly require C-issued `c_provider_receipt_ref` and immutable `c_submit_outcome_ref`, preserve UNKNOWN/IN_DOUBT, require `participant_terminal_proof_ref` only after all owner outcomes are determinate, and reserve `owner_gate_release_attestation_ref` exclusively to I or D. Current exact source Blob: `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`.

Updated structural readback is now 24/24 headings and 33/33 table rows across source, EN and zh-CN. This is a candidate mapping only; no wire schema/SDK has been updated/generated and no C/G/I/D/Storage approval or conformance execution is implied. Previous 23-heading count is superseded.
