# X — Current-main Complexity Reassessment (Delta)
- Assessment: ARCH-CX-001-D1
- Baseline: `main@ca69d50d1fc6c19a930128de700b0f2328bf32fb`
- Parent assessment: PR #49, Blob `c509120644d6f7c7223decf3f9f0ee33b0548bb7`, based on `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Delta evidence: B bilingual parity audit Blob `a877ceff906da01e70e277a81b95978982af3ede`.

## Delta assessment
The new main commit adds no runtime module, state machine, protocol, database, queue, or execution dependency. Therefore the prior High architecture complexity rating is unchanged. It does, however, provide concrete evidence that documentation/evidence governance is itself a material cognitive and verification cost:
- 22 B research file rows are tracked with differing PARTIAL, REMEDIATED—MANUAL REVIEW PENDING, and PROVISIONAL states.
- Closure requires clause/row parity, stable-ID/status/source-pin checks, internal-link checks, and a separate independent review.
- Author-side translation remediation creates a second state (translated but not independently verified) that must not be conflated with accepted normative content.

## Complexity budget update
Keep the existing eight-dimension model and do not inflate structural or runtime state scores based on documentation alone. Update A/governance cognitive and verification complexity to **5 / Extreme (high confidence for this bounded B research package)**. The project-wide cognitive complexity remains High; a universal 5 for every module is not justified by this one audit.

New hotspot: **Bilingual evidence lifecycle** — source edit → translation → exact Blob pin → parity audit → independent review → Owner decision/adoption → downstream consumer refresh. This is a governance/verification workflow, not a runtime service.

## Simplification controls
1. Maintain one authoritative bilingual artifact per decision, not separate drifting translations.
2. Automate stable-ID, table-row, enum/status, link and Blob-pin checks where mechanically possible.
3. Keep manual semantic review for normative meaning; automation cannot certify equivalence.
4. Do not require retranslation of unchanged clauses; use content-hash/change-scoped parity review.
5. Keep research drafts, Owner-approved decisions, and implementation evidence as separate maturity states.

## Disposition
**NOT PROVEN** remains unchanged for system-wide implementability/verifiability/maintainability. The new audit strengthens evidence for governance burden but does not prove the runtime architecture is more complex or less feasible. No architecture simplification may remove correctness-bearing states or Owner review boundaries.
