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


## 7. Additional branch-aware source review (correction to §1)

D branch `session-d-memory-brain-2026-11-16` was read for:
- `03-memory-brain/canonical-memory-store.md`;
- `03-memory-brain/memory-versioning.md`;
- `03-memory-brain/memory-lifecycle-manager.md`;
- `03-memory-brain/memory-brain-overview.md`;
- `reviews/03-memory-brain/three-party-six-dimension-review.md`.

D candidate findings consumed by E:
- CanonicalCommit carries operation/idempotency/request digest, expected/resulting version and commit_sequence; D proposes a monotonic canonical sequence, but sequence scope remains OPEN.
- LifecycleEvent sequence is per Memory aggregate and is not a global canonical commit cursor.
- ForgetOperation includes target inventory, policy/auth references, suppression time, dependency snapshot/watermark, per-target progress, exceptions and completion proof reference.
- D requires suppression before asynchronous cleanup and late-arriving derivatives to be recorded for follow-up cleanup; a producer-registration barrier and atomic pre-publication gate are not closed in the inspected D candidate. D-REV-P1-003 remains OPEN.
- E's contracts intentionally require D/I/Storage to close this race and fail closed until the authoritative gate exists.

H and I branch search returned no matching branches. Their contracts remain **OPEN**, as the Phase 3 Task Pack baseline states. The B Fact/Claim ADR is still not verified as approved; Phase 2 and D's review continue to mark INT-P0-01 ADR-BLOCKED. No E mapping was added.

The E five-file inventory and E self-review remain only partially verified: three E design files were located and read; the GitHub connector did not expose a directory listing or resolve the other two design paths/self-review in this pass. The three located files were updated with the new ingress/Forget constraints. This limitation blocks a claim of complete five-file/self-review review and is recorded as an explicit OPEN review item.


## 8. Completed branch-aware source review (supersedes earlier limitations in §1 and §7)

### E source package

All five E design files were located and read on `session-e-memory-compiler-2026-11-16`:
- `04-memory-compiler/compiler-overview.md`
- `04-memory-compiler/event-ingestion-engine.md`
- `04-memory-compiler/extraction-and-normalization.md`
- `04-memory-compiler/evidence-and-provenance.md`
- `04-memory-compiler/consolidation-and-conflict-resolution.md`

E self-review read:
- `reviews/04-memory-compiler/three-party-six-dimension-review.md`

The five design files were updated with Phase 3 receipt, cursor, identity/retention and Forget registration constraints. The E self-review remains a review record and was not modified.

### D source package

D candidate design and review were read at `session-d-memory-brain-2026-11-16` (baseline commit `9dc08c63f6912320e290a963c634748ec44a81c8`):
- `03-memory-brain/canonical-memory-store.md`
- `03-memory-brain/memory-versioning.md`
- `03-memory-brain/memory-lifecycle-manager.md`
- `03-memory-brain/memory-brain-overview.md`
- `reviews/03-memory-brain/three-party-six-dimension-review.md`

Key D status: CanonicalCommit has operation/idempotency/request digest, expected/resulting version and commit_sequence; sequence scope remains OPEN. LifecycleEvent sequence is per Memory aggregate. ForgetOperation carries target inventory, suppression time, dependency snapshot/watermark, per-target progress and completion proof. D's candidate mentions late derivative discovery/follow-up cleanup but does not close producer-registration epoch plus atomic publish gate; D-REV-P1-003 remains OPEN.

### H source package

H candidate design read on `session-h-bmcp-protocol`, baseline `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`, candidate commit `fcc5103399b4c322e52d642cae5a2414969399a7`:
- `08-bmcp-protocol/protocol-overview.md`
- `08-bmcp-protocol/message-envelope-and-versioning.md`
- `08-bmcp-protocol/context-delivery-and-acknowledgement.md`
- `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- `08-bmcp-protocol/forget-revocation-and-reconnect.md`
- `08-bmcp-protocol/protocol-conformance-matrix.md`

H is present but CANDIDATE, not approved. Its envelope carries owner-defined idempotency namespace/key/digest; H transports E's receipt semantics. It requires authenticated transport principal binding from I, treats payload ActorRef/producer as claims, distinguishes E source cursor, D canonical cursor, lifecycle cursor and F index watermark, and treats Forget fence/permission epoch as opaque. H explicitly cannot declare global Forget completion or provider physical erasure.

### I source package

I candidate design read on `session-i-security-governance-2026-11-16`, baseline `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`, candidate commit `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb`:
- `09-security-governance/security-and-identity-overview.md`
- `09-security-governance/principal-actor-and-authorization-contract.md`
- `09-security-governance/scope-and-revocation-policy.md`
- `09-security-governance/forget-retention-backup-and-erasure-policy.md`
- `09-security-governance/threat-model-and-adversarial-test-plan.md`
- `09-security-governance/audit-and-exception-governance.md`

I is present but CANDIDATE, not approved. It proposes idempotency namespace = authenticated producer + tenant/security domain + operation family + caller key; requires current authorization at ingress and each retry/replay; requires receipt metadata to cover declared retry/replay horizon while numeric periods remain OPEN. Its Forget proof requires a sealed target inventory, producer registration epoch/in-flight barrier, terminal status for all pre-barrier producers, consumer watermarks, and explicit Confirmed or PolicyException targets. Unknown/offline is not success. Its tombstones must be non-reconstructive and bounded; raw content, low-entropy hashes, embeddings, summaries and provenance edges are prohibited.

### B ADR status

No approved B Fact/Claim ADR was verified in the reviewed inputs. Phase 2 and D review retain INT-P0-01 as OPEN / ADR-BLOCKED. CandidateProposition/ExtractionIR mapping remains blocked; no canonical mapping was added.

### Updated dependency disposition

- **H present / CANDIDATE:** wire envelope and serialization can inform field mapping, but no final wire freeze.
- **I present / CANDIDATE:** identity, authorization, retention and global Forget policy can inform enforcement, but no final policy freeze.
- **D present / CANDIDATE:** canonical cursor and Forget fence shape remain owner-controlled; D-REV-P1-003 barrier gap remains blocking.
- **B ADR absent/not approved:** mapping remains ADR-BLOCKED.
