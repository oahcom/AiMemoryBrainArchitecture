# Session E — Decision / Change Log

**Branch:** `session-e-memory-compiler-2026-11-16`  
**Baseline:** `54df136d1e410af834461950e3c61c5c80abd6ad`  
**Date:** 2026-11-16  
**Status:** Candidate remediation delivery; not cross-module contract freeze, implementation sign-off or security approval.

## 1. Reviewed inputs and evidence limits

| Input | Result | Notes |
|---|---|---|
| `reviews/integration/phase-3-cross-module-remediation-task-pack.md` | READ | E ownership, WS-6, WS-3 enforcement and acceptance criteria |
| `reviews/integration/phase-2-defg-cross-session-reconciliation.md` | READ | INT-P0-03, INT-P1-04/06, INT-X-01/02/06 and gate dependencies |
| `04-memory-compiler/extraction-and-normalization.md` | READ | CandidateProposition remains pre-canonical; source modality and IR lineage |
| `04-memory-compiler/evidence-and-provenance.md` | READ | Evidence/Provenance lineage and dependency obligations |
| `04-memory-compiler/consolidation-and-conflict-resolution.md` | READ | D canonical authority; existing cross-module interface appendix |
| E branch five-file inventory and E self-review | **NOT FULLY VERIFIED** | The connector exposed the three named E design paths above, but did not expose a directory tree or resolve the remaining two design-file paths/self-review. No claim is made that all five were read. This is a review limitation to close before sign-off. |
| D Forget fence/canonical cursor candidate | **OPEN — NOT VERIFIED** | Candidate filenames/contract refs were not confirmed from D branch during this pass. E contract therefore treats D schema, epoch namespace and barrier as dependencies, not local decisions. |
| B Fact/Claim ADR | **ADR-BLOCKED / NOT VERIFIED APPROVED** | Phase 2 and Task Pack identify INT-P0-01 as OPEN / ADR-BLOCKED. E does not map to canonical Claim. |
| I identity/retention | **OPEN** | Task Pack identifies I as new workstream; no approved I contract assumed. |
| H wire/Adapter | **OPEN** | Task Pack identifies H as new workstream; no approved H contract assumed. |

## 2. Decisions and proposals

| ID | Decision / change | State | Owner / dependency |
|---|---|---|---|
| E-DEC-001 | Accepted means durable receipt only; distinct from Processed, Compiled, CanonicalCommitted and Indexed | CANDIDATE | E; H/I/Storage review |
| E-DEC-002 | Idempotency key is namespaced by authenticated issuer, producer, security domain and event family | CANDIDATE | H/I/B approve identity types |
| E-DEC-003 | Same key/same semantic digest returns original receipt; same key/different digest conflicts | CANDIDATE | E/H/Storage |
| E-DEC-004 | Acceptance linearization point is transaction commit binding Event, payload ref/digest, idempotency receipt and compile-intent outbox | CANDIDATE | Storage/Consistency validates implementation |
| E-DEC-005 | Source Event cursor, D canonical commit cursor and F index watermark are different typed namespaces | CANDIDATE | D/F/A/Storage align exact cursor definitions |
| E-DEC-006 | Every worker/retry/lease/DLQ/replay/recompile/publication checks current authorization and D Forget fence; fail closed on unknown fence | CANDIDATE | D/I provide authoritative fence/policy APIs |
| E-DEC-007 | Derived dependency registration must be durable before derivative visibility; producer runs participate in D barrier | CANDIDATE / BLOCKING D DEPENDENCY | D atomic registration/publication gate required |
| E-DEC-008 | Audit tombstone is content-free, non-reconstructive and insufficient as physical-erasure proof | CANDIDATE | I approves fields and retention |
| E-DEC-009 | CandidateProposition/ExtractionIR mapping remains blocked until B/Governance ADR approval | ADR-BLOCKED | B/Governance; D consumes decision |

## 3. Changed paths

- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` — new.
- `04-memory-compiler/forget-fence-and-derived-registration.md` — new.
- `04-memory-compiler/decision-change-log.md` — new.
- Existing E design documents were not rewritten in this candidate patch; their current contracts are cross-referenced by the two new boundary contracts. Follow-up edits require verified inventory and a path-scoped review.

## 4. Interface impact

| Module | E impact | Required owner decision |
|---|---|---|
| D | Consume Forget fence, producer barrier, dependency registration and canonical commit result/cursor; E submits only proposals | D owns exact canonical and Forget contracts |
| B | Neutral IR mapping to Fact/Claim | Approve ADR-001 first |
| F | E emits post-canonical publication requests; never owns index watermark | F defines index ACK/watermark |
| G | E emits canonical impact events only | G owns ContextVersion and reconciliation |
| H | E consumes authenticated envelope and returns durable receipt/status | H defines BMCP and Adapter wire semantics |
| I | E consumes identity, permission epoch, retention and Forget policy | I owns global governance/completion |
| Storage/Consistency | Event + payload ref + receipt + compile intent durability | Select/validate transaction/outbox/WAL realization |

## 5. Acceptance and conformance matrix

| Acceptance | Design coverage | Status |
|---|---|---|
| Crash/retry preserves Accepted receipt | Transactional inbox/outbox and crash matrix | CANDIDATE; requires storage fault-injection |
| No duplicate canonical effect | Stable operation key; query D after unknown outcome | CANDIDATE; D conformance required |
| Replay/DLQ/recompile cannot resurrect forgotten derivatives | Fence check at every stage and publication gate | BLOCKED on D/I atomic barrier and conformance |
| Every derived object has source lineage and registered dependency | Pre-visibility dependency registration | CANDIDATE; Storage/D gate required |
| Event, canonical and index cursors are distinct | Typed namespace contract | CANDIDATE; exact D/F definitions open |
| B Fact/Claim mapping only after approval | Explicit ADR gate | ADR-BLOCKED |
| Five-file E review and self-audit complete | Not all paths verified | OPEN |

## 6. Change control

This branch change does not merge D/F/G/H/I work, freeze wire/schema contracts, select a concrete database product, define I retention durations, declare physical erasure, or claim production tests passed. Any D/I/H schema mismatch must be reconciled by the owning module before contract freeze.
