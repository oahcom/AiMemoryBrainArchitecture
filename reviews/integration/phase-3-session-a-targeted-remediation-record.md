# Session A — Phase 3 Targeted Remediation Record

- Date: 2026-11-16
- Branch: `session-a-integration-2026-11-16`
- Scope: Contract Registry, Typed Cursor coordination proposal, issue/dependency status.
- Authority boundary: A coordinates cross-module contracts only; no D/E/H/I-owned design file was modified.

## 1. Source and branch verification

At execution start, the following refs were resolved to actual commit objects:

| Branch | HEAD SHA |
|---|---|
| `session-a-integration-2026-11-16` | `f76cc558273fbc1a27bb930a2f1e8d940b717c80` |
| `session-b-domain-model-phase3` | `ab19afbf92f67fe0a7679e9aa3a35b015fed89f4` |
| `session-d-memory-brain-2026-11-16` | `30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6` |
| `session-e-memory-compiler-2026-11-16` | `3dea6096eefa6779eb12e4e788bcf9429d2a3f83` |
| `session-h-bmcp-protocol` | `fcc5103399b4c322e52d642cae5a2414969399a7` |
| `session-i-security-governance-2026-11-16` | `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb` |

Main was read at `8a6414158c9c056c1638222534e1993d1bbc99d2`, including the four-way Phase 3 review and remediation task pack. D's `03-memory-brain/commit-cursor-semantics.md` was read from D's current branch. E's `04-memory-compiler/decision-change-log.md` was read from E's current branch. H's envelope and Forget/reconnect contracts and I's Principal/authorization and Forget/retention contracts were read from their current branches.

## 2. Changes made

1. Replaced stale source baselines in `reviews/integration/contract-registry.md` with actual A/B/D/E/H/I branch HEAD SHAs and package paths.
2. Corrected H/I status: both packages exist and are explicitly marked “design package exists; cross-module contract pending verification”. Neither is Contract Approved.
3. Split evidence into file presence, owner decision, cross-module alignment and implementation/test verification.
4. Added CR-P1-01..05, CR-P0-01..02 context, INT-P0-01..04, INT-P1-01..06, INT-X-01..08 and D-REV-P1-001..003 ownership, dependency and closure conditions.
5. Recorded the cross-module dependency directions D→E, E→D, D/E→F, F→G, D→G, G→H, I→D/E/F/G/H and B→D/E/F/G/H.
6. Replaced the stale partitioned CanonicalCommitCursor candidate in `typed-cursor-and-watermark-contract.md` with D's owner decision: one global ordered cursor per Canonical Memory Authority; independent AggregateRevision per aggregate; LifecycleEventCursor per Memory; F-owned IndexWatermark per index/channel partition; ForgetFence generation is separate.
7. Kept Storage/Consistency implementation, transaction/crash recovery, multi-authority routing and E/F/G consumer behavior explicitly OPEN.
8. Added this record to document superseded status and remaining open work.

## 3. Before/after disposition

| Item | Before | After |
|---|---|---|
| CR-P1-01 | OPEN; atomic producer admission/fence/publication boundary not implementable/verified | **OPEN**; D/E/Storage operation and race evidence required |
| CR-P1-02 | OPEN; A proposal conflicted with D cursor decision | A proposal corrected to D's global per-authority semantics; integration/Storage/F/G validation **OPEN** |
| CR-P1-03 | OPEN; D/E SHAs stale; H/I marked absent | A registry corrected to current A/B/D/E/H/I refs; H/I present candidate packages; cross-contract status remains pending |
| CR-P1-04 | OPEN; E log contains stale statements | **OPEN / E-owned**; E must add supersession notice and current disposition |
| CR-P1-05 | CANDIDATE / mapping required | **OPEN / I-owned mapping**; H ACK, target inventory and two producer-registration levels need owner mapping |
| CR-P0-01 / INT-P0-01 | ADR-BLOCKED | **ADR-BLOCKED**; no Fact/Claim approval inferred |
| CR-P0-02 / INT-P0-02 | OPEN | **OPEN**; B/I/H typed identity mapping and negative tests required |
| INT-P0-03 | OPEN | **OPEN**; atomic Forget gate and end-to-end target evidence missing |
| INT-P0-04 | OPEN | **OPEN**; threat-model and residual-risk acceptance evidence required |
| INT-X-01 | CANDIDATE / cursor conflict | A proposal now matches D semantics; Storage and consumer conformance still **OPEN** |
| D-REV-P1-002 | OPEN | D semantic decision **DECIDED**; Storage implementation validation **OPEN** |
| D-REV-P1-003 | OPEN | **OPEN**; no atomic producer barrier/publication proof |
| INT-X-02/03/04 | OPEN | **OPEN**; no closure inferred from H/I package presence |

## 4. Important supersession notes

- Earlier Registry wording that H/I were absent is superseded by the actual H/I branch/package evidence recorded in the updated registry.
- Earlier A partitioned CanonicalCommitCursor wording is superseded by D's current owner decision and the revised typed contract.
- E's decision log contains historical sections that state H/I were absent and D cursor scope was undecided; its later §8 explicitly supersedes earlier limitations, but CR-P1-04 remains assigned to E for a clear current-state notice. A does not edit E's file.
- D's semantic cursor decision does not establish Storage implementation, atomic commit sequencing, crash recovery, monotonicity under failover, or F/G consumer conformance.
- H/I file presence does not close INT-P0-02, INT-P0-03, INT-P0-04, INT-X-02, INT-X-03 or INT-X-04.

## 5. Explicit non-closures

The following remain open: D/E/Storage atomic producer admission, fence installation, dependency registration and publication gate; B Fact/Claim ADR; B/I/H Principal/ActorRef/ScopeRef mapping; I global Forget completion/target mapping; F/G consumer alignment; Storage cursor realization; implementation, fault-injection, security and performance evidence.

No module branches were merged. No D/E/H/I-owned files were modified. No implementation or conformance test is claimed PASS.
