# P — Current-main Root-first Priority Reassessment (Delta)
- Assessment: PRIORITY-001-D1
- Baseline: `main@ca69d50d1fc6c19a930128de700b0f2328bf32fb`
- Parent: PR #46 F/D/P report Blob `081610b1734ec08dc7c35c75fae1cae3ca713be4`.
- Delta evidence: B parity audit Blob `a877ceff906da01e70e277a81b95978982af3ede`.

## Priority adjustment
Add a scoped **P0 evidence-readiness task for B-dependent decisions**, not a new global implementation P0:
1. Complete remaining B research translations for PARTIAL/PROVISIONAL rows.
2. Independently verify REMEDIATED rows clause-by-clause and preserve stable IDs/statuses/examples/source pins.
3. Confirm B Owner's actual ADR/decision status; do not infer that translation means Fact/Claim is approved.
4. Refresh exact consumer pins and A's G2/G6 disposition.

This task ranks ahead of any schema or contract freeze that relies on those B research artifacts. It does not outrank unrelated physical correctness work or block isolated synthetic preparation.

## Keep the existing root-first order
- Preserve system authority, domain semantics, security/Forget and physical atomicity as root correctness prerequisites.
- Keep Storage/COC/JF-10, D/E/I race/recovery, and C/G/H Applied closure on their existing P0 paths.
- Keep vector/ANN, advanced reranking and scale-out deferred as previously decided.
- Do not elevate document translation to a substitute for B's domain decision or for executable correctness proof.

## Exit criteria
Per-file bilingual status accepted by an independent reviewer; exact current Blob pins; unresolved rows retained with Owner/deadline; B Owner decision explicitly recorded; downstream consumers acknowledge exact version; A updates G2/G6. No Gate passes solely because a translation PR merges.

## Disposition
The global priority order is unchanged. This is a bounded evidence-readiness addition with a hard ordering constraint only for B-dependent normative decisions.
