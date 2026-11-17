# G Phase 3.6 Applied / Forget / Reconciliation Bilingual Review

- Date: 2026-11-17
- Source branch: `session-g-memory-context`
- Source path: `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`
- Exact source Blob SHA: `aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- Scope: complete EN/zh-CN companion pair, including all Owner decision addenda through the CGH-APPLIED-1.1 recovery-batch amendment.
- Non-goal: Owner approval beyond decisions already present in source, C/G/H global freeze, implementation verification or conformance execution.

## 1. Artifacts

- EN: `docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`
- zh-CN: `docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`

The English companion embeds the exact Owner source content and source Blob pin. The Chinese companion carries the same source pin and reciprocal language link.

## 2. Structural readback

| Measure | Owner source | English | Chinese |
|---|---:|---:|---:|
| Headings | 21 | 21 | 21 |
| Table rows (including header/separator rows) | 37 | 37 | 37 |
| Lines | 272 | 275 | 273 |

All three artifacts were fetched back from GitHub. The English companion contains the exact Owner source content. The Chinese companion preserves all 21 headings and 37 table rows, including all 15 G-36 conformance cases and all decision addenda.

## 3. Semantic checks

- Six lifecycle stages remain separate; G alone owns Applied acceptance.
- Full Applied retains all 13 acceptance predicates, including exact request/boundary identity, authenticated identity/session, Scope/Environment, Managed Region inventory/digest, current I PermissionEpoch/decision, D ForgetFence/lineage, H CapabilityEpoch, C submit evidence and no prior invalidation.
- Historical Applied and current-use validity remain separate; later Forget/revocation invalidates current use without rewriting valid history.
- Forget tombstone scope and all nine G-owned suppression/invalidation actions are retained; G does not claim F index/cache purge or H local Adapter purge.
- Context Remove remains membership removal, not Canonical Forget.
- Reconnect remains a new trust boundary; stale Snapshot/Delta and old ACK cannot be replayed without current authority checks.
- G-36-01..15 remain SPECIFIED / NOT RUN.
- CFG, Issue #3, Issue #6, CGH-APPLIED-1.1, its current-candidate reaffirmation, and recovery-batch amendment retain their exact Blob references, owner dispositions and enumerated exceptions.
- No translation upgrades G's ACCEPT WITH ENUMERATED EXCEPTIONS to global freeze or implementation approval.

No material semantic divergence was found in this targeted review.

## 4. Disposition

**Bilingual parity: PASS for this exact source Blob.**

G source state remains: semantic decisions recorded; C/G/H Applied freeze BLOCKED; implementation/execution NOT VERIFIED. G's own exact-version decisions remain limited to their pinned A package versions and enumerated exceptions. G conformance remains SPECIFIED / NOT RUN. This review does not prove C/G/H global freeze, implementation, runtime behavior, global Forget completion or physical erasure.
