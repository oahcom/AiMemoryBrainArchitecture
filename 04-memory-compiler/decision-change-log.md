---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Restored byte-for-byte from Owner source branch; Owner acceptance remains pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "E-domain Memory Compiler record decision-change-log.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-decision-change-log"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - decision-change-log
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



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


## 9. Phase 3 targeted remediation — current branch HEAD reconciliation

This section is appended as a correction to the historical notes above. Earlier statements are preserved as historical audit records; where they conflict with this section, this section records the newer inspection and superseding status.

### 9.1 Exact current source refs read for this remediation

| Owner | Branch | Current HEAD inspected | Result |
|---|---|---|---|
| E | `session-e-memory-compiler-2026-11-16` | `3dea6096eefa6779eb12e4e788bcf9429d2a3f83` | Current E package tree enumerated; all eight E design paths identified, core ingress/Forget/provenance/overview files read |
| D | `session-d-memory-brain-2026-11-16` | `30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6` | Current ForgetFence, CanonicalCommitCursor and MemoryVersioning read |
| H | `session-h-bmcp-protocol` | `fcc5103399b4c322e52d642cae5a2414969399a7` | Current envelope and Forget/Revocation package inspected; CANDIDATE only |
| I | `session-i-security-governance-2026-11-16` | `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb` | Current Principal/ActorRef/ProducerIdentity and Forget/Retention package inspected; CANDIDATE only |
| B | `session-b-domain-model-phase3` | `ab19afbf92f67fe0a7679e9aa3a35b015fed89f4` | Current ADR-001 and typed ScopeRef semantics inspected; ADR remains ADR-BLOCKED |

The requested `reviews/integration/phase-3-defghi-cross-module-contract-review.md` was not present in the current A branch tree and returned NOT_FOUND when fetched. It is not represented as read. The Phase 3 Task Pack was read from A's current branch; A's Contract Registry and Typed Cursor proposal were also read. The absence of the named review report remains a source-evidence limitation.

### 9.2 D decisions now consumed — supersede older entries in §§1, 2, 7 and 8

- **DECIDED — CanonicalCommitCursor:** one globally ordered sequence per Canonical Memory authority, allocated only at successful durable canonical transaction commit.
- **DECIDED — AggregateRevision:** independent per-aggregate revision sequence; every committed revision carries its CanonicalCommitCursor.
- **DECIDED — LifecycleEventCursor:** independent contiguous per-Memory lifecycle stream; each event also records its enclosing CanonicalCommitCursor.
- **DECIDED — ForgetFenceCursor:** D-owned tuple `(forget_operation_id, fence_generation, target_set_digest)`; independent of canonical commit, lifecycle, permission and index positions.
- **DECIDED — Producer barrier semantics:** D's producer registry captures a registration high-water mark at fence installation; every pre-fence registration must reach durable terminal disposition. Queue deletion, lease expiry, timeout or worker loss is not terminal.
- **DECIDED — Register-before-visible principle:** derivative registration precedes visibility and final gate rechecks latest fence; this is a semantic requirement, not a published callable API.
- **OPEN / BLOCKING — D/E/Storage atomicity:** D has not specified callable registration/dependency/publication operations, complete receipt fields, a transaction owner, or a proven linearization protocol coupling final gate and Storage visibility. D-REV-P1-003's implementation-level race remains open.

### 9.3 H/I/B alignment and state

- **H present / CANDIDATE:** authenticated transport principal binding is authoritative; payload ProducerId/ActorRef/ScopeRef are claims/selectors only. Permission epoch and Forget fence are distinct typed fields; replay rechecks both. No wire freeze.
- **I present / CANDIDATE:** ProducerIdentity binds authenticated Principal/issuer, registered producer/application, workload/instance, credential validity/epoch, permitted event families, security domain and revocation status. PermissionEpoch is I-owned. Authorization must be rechecked at the operation's commit/disclosure linearization point. No policy freeze.
- **B present / ADR-BLOCKED:** ScopeRef is a typed domain reference, not permission. ClaimRef/ClaimRevisionRef and Fact/Claim canonical mapping remain blocked by ADR-001. CandidateProposition/ExtractionIR must not auto-promote.
- **H/I status correction:** historical statements that H/I branches were absent are superseded; formal candidate packages now exist.

### 9.4 E decisions and supersession ledger

| Historical item | Prior state | Current disposition |
|---|---|---|
| E-DEC-001 Accepted vs processing milestones | CANDIDATE | **CANDIDATE, sharpened**: AcceptedReceipt, CompilerCompletionReceipt, CanonicalCommitReceipt, DerivedRegistrationReceipt, PublicationReceipt and F Index ACK are distinct evidence |
| E-DEC-002 Idempotency namespace | CANDIDATE | **CANDIDATE, sharpened**: bind authenticated Principal + ProducerIdentity + validated Scope binding + security domain + operation family + caller key; exact normalization awaits H/I/B |
| E-DEC-003 same-key digest behavior | CANDIDATE | **CANDIDATE**: same key/same digest returns original; different digest conflicts |
| E-DEC-004 acceptance linearization | CANDIDATE | **CANDIDATE**: durable Event + payload ref/digest + idempotency + receipt + compile intent in one transaction or proven WAL |
| E-DEC-005 cursor separation | CANDIDATE | **D semantic decision consumed**: CanonicalCommitCursor global per Brain authority; AggregateRevision and LifecycleEventCursor independent; IndexWatermark F-owned; ForgetFenceCursor D-owned; PermissionEpoch I-owned; ContextVersion G-owned |
| E-DEC-006 fence checks on async work | CANDIDATE | **CANDIDATE E enforcement**; final gate remains OPEN/BLOCKING |
| E-DEC-007 dependency registration before visibility | CANDIDATE / blocking | **D semantic rule DECIDED; D/E/Storage atomic operation OPEN/BLOCKING** |
| E-DEC-008 non-reconstructive tombstone | CANDIDATE | **CANDIDATE** subject to I's retention/audit approval |
| E-DEC-009 Fact/Claim mapping | ADR-BLOCKED | **ADR-BLOCKED — unchanged** |

### 9.5 Changed paths in this remediation

- `04-memory-compiler/forget-fence-and-derived-registration.md` — rewritten to consume current D fence, producer barrier and cursor decisions; records exact missing D/E/Storage operations.
- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` — rewritten to split Accepted, Compiler Completion, Canonical Commit, Derived Registration, Publication and F Index evidence.
- `04-memory-compiler/compiler-state-and-producer-admission.md` — new E-owned lifecycle and D admission mapping.
- `04-memory-compiler/evidence-and-provenance.md` — append typed cursor and pre-visibility lineage registration requirements.
- `04-memory-compiler/decision-change-log.md` — append this source/decision correction while preserving all earlier audit history.

### 9.6 Tests and verification status

All conformance scenarios in the updated E documents are **NOT RUN**. This delivery is design/documentation only. No Storage transaction, D endpoint, worker, queue, DLQ, fence service, permission service, publication gate or runtime test was executed. The E branch commit and post-write file readback are recorded in the final delivery report after commit creation.


## 10. Final concurrent-branch refresh before delivery

H and I advanced while this E remediation was being authored. Their latest branch refs were re-read before final delivery; the semantics used above were checked against these current heads, superseding the earlier H/I SHAs recorded in §9.1.

| Owner | Branch | Latest HEAD re-read | Relevant current files |
|---|---|---|---|
| H | `session-h-bmcp-protocol` | `3c4c03c28c4e50cc6eed89d505725b873241bad7` | `message-envelope-and-versioning.md` blob `5547ecd78d118bd63e571e5daad87194d9b694e4`; `forget-revocation-and-reconnect.md` blob `695909360782987781e259187041618f495f1c8c` |
| I | `session-i-security-governance-2026-11-16` | `135afd3d8333256ee2efcca9525a39a9d06739fc` | `principal-actor-and-authorization-contract.md` blob `4f6f5691a599a0566b036f4240003152d64e2242`; `forget-retention-backup-and-erasure-policy.md` blob `db602095f1b9760798ea423b09887ae8b9b4821c` |

The refreshed H/I documents continue to require authenticated transport binding, reject payload self-asserted producer/actor/scope identity as authentication, recheck current PermissionEpoch and ForgetFence on replay and at the commit/disclosure boundary, and keep local Adapter acknowledgement distinct from global Forget completion. H/I remain CANDIDATE, not frozen.

The current A-branch tree and repository code search did not locate `reviews/integration/phase-3-defghi-cross-module-contract-review.md`; that named review remains unavailable and is not claimed as read.



---
## 9. Phase 3.5 — Authoritative supersession and current disposition

This section is the current E-side source alignment. Earlier statements remain as historical audit records, but where they conflict with this section they are **SUPERSEDED** and must not be used as current status.

### 9.1 Superseded historical statements

| Historical statement / section | Status | Superseded by |
|---|---|---|
| §1 says D Forget fence/canonical cursor candidate was not verified and D sequence scope remained OPEN | **SUPERSEDED** | Phase 3 cross-module review plus D current Forget Fence and commit-cursor semantics; D CanonicalCommitCursor is per-authority global |
| §7 says D barrier/atomic pre-publication gate was not closed and D-REV-P1-003 remains broadly undefined | **PARTIALLY SUPERSEDED** | D now specifies Producer Registration Barrier, register-before-visible and latest-fence publish-gate semantics; narrower D/E/Storage atomic operation/linearization remains OPEN |
| §7 says H and I branches were absent | **SUPERSEDED** | H and I candidate packages exist at branch heads recorded in Phase 3 cross-module review; their contracts are not frozen/approved |
| §1/§7 says I identity/retention and H wire/Adapter contracts unavailable | **SUPERSEDED AS PRESENCE CLAIM ONLY** | I/H candidate contracts have been read; identity, retention, ACK mapping and wire schemas remain candidate/open dependencies |
| §1/§7 limitations on E five-file inventory and self-review | **SUPERSEDED ONLY TO THE EXTENT VERIFIED IN §8** | §8 records completed source inventory; this update does not claim runtime tests or implementation evidence |
| Any wording that treats a local E fence precheck as sufficient for publication | **SUPERSEDED** | PublishDerivedIfFenceCurrent must be D-authoritative and serialize against fence installation; E local checks are defense-in-depth only |
| Any wording that implies Accepted means compiled/committed/published | **SUPERSEDED** | AcceptedReceipt evidence matrix: Accepted is durable ingress only |

### 9.2 Current branch/source baseline

The Phase 3 cross-module review records these reviewed branch heads (full SHA):

| Session | Branch | Reviewed HEAD | Current package status |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | f76cc558273fbc1a27bb930a2f1e8d940b717c80 | Coordination artifacts; registry correction remains A-owned |
| B | session-b-domain-model-phase3 | ab19afbf92f67fe0a7679e9aa3a35b015fed89f4 | Fact/Claim ADR remains ADR-BLOCKED; typed references not frozen |
| D | session-d-memory-brain-2026-11-16 | 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6 | Forget and cursor semantics present; D/E/Storage atomic realization OPEN |
| E | session-e-memory-compiler-2026-11-16 | 3dea6096eefa6779eb12e4e788bcf9429d2a3f83 | E design package; Phase 3.5 updates are committed separately after this reviewed baseline |
| H | session-h-bmcp-protocol | fcc5103399b4c322e52d642cae5a2414969399a7 | Candidate Forget ACK/reconnect package exists; not frozen |
| I | session-i-security-governance-2026-11-16 | 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb | Candidate global Forget/identity policy exists; not frozen |

F and G are not part of the Phase 3 D/E/H/I review's recorded branch-head set. No F/G HEAD is inferred here. The E branch's post-review HEAD is the commit SHA reported by the Phase 3.5 delivery, not the historical reviewed baseline above.

### 9.3 Current authoritative dependency decisions

- **D Producer Barrier — DECIDED semantic requirement:** D's current Forget contract requires closed-world ProducerClass/ProducerWork registration, durable registration before execution/lease/retry/DLQ replay/publication, fence installation capturing producer-registration high-water, terminal disposition for all pre-fence work, durable dependency registration before visibility and latest-fence recheck immediately before publication.
- **D/E/Storage operation contract — OPEN / BLOCKING:** exact inputs/outputs/errors and linearization for RegisterProducerWork, InstallForgetFence, RegisterDerivedDependency, PublishDerivedIfFenceCurrent and CompleteProducerWork must be jointly implementable and tested. D's semantic requirements are not proof of a callable API or transaction implementation.
- **H/I — CANDIDATE PRESENT:** H has Adapter-local ACK and reconnect candidate contracts; I has global Forget inventory/completion, identity/authorization and retention/backup candidate contracts. H ACK is local evidence only; I alone owns global completion policy.
- **B Fact/Claim — ADR-BLOCKED:** E continues to treat CandidateProposition/ExtractionIR as pre-canonical compiler artifacts. No canonical Fact/Claim mapping, schema freeze or wire field is approved by this update.
- **CanonicalCommitCursor — D DECIDED:** one per-authority global sequence. AggregateRevision, LifecycleEventCursor, F IndexWatermark, D ForgetFenceGeneration, I PermissionEpoch and G ContextVersion are independent typed namespaces.
- **Unverified implementation — NOT PASSED:** design documents and static reviews are not runtime conformance. No test is marked PASS without executable fixture, environment, expected/actual output and retained evidence.

### 9.4 Phase 3.5 change inventory

| E file | Change |
|---|---|
| compiler-state-and-producer-admission.md | ProducerClass vs WorkItem registration; lease/attempt/retry/DLQ/replay/recompile and terminal evidence; crash recovery |
| forget-fence-and-derived-registration.md | Five D operation mapping; staging/visibility boundary; publish evidence; explicit OPEN contracts; 16 race/fault cases |
| accepted-receipt-and-idempotency-contract.md | Accepted-to-publication state matrix; duplicate submission; ACK-loss recovery; cursor namespaces |
| decision-change-log.md | Explicit supersession markers and current cross-module status |

### 9.5 Gate disposition

- CR-P1-01: **OPEN / BLOCKING** — D/E/Storage atomic registration, dependency visibility and final publish linearization remain unresolved and unimplemented.
- INT-P0-03: **OPEN** — end-to-end Forget requires D/E/F/G/H/I and Storage evidence; this E documentation change cannot close it.
- CR-P1-02 / INT-X-01: E semantic cursor descriptions are aligned to D's per-authority global decision; A/F/G/Storage integration and executable durability/recovery validation remain outside this E-only change.
- INT-P0-01: **ADR-BLOCKED** — B Fact/Claim approval remains absent/unverified.
- H/I: candidate package existence is acknowledged; no cross-module contract freeze or security approval is implied.



---
## 9.6 D Phase 3.5 operation-level refinement — current

The current D normative source is 03-memory-brain/forget-fence-operation-and-publication-gate.md (D branch session-d-memory-brain-2026-11-16; blob 2c5b1358ff58f99af838b741a75966ccd07ad088) and D's decision-change-log §7 (blob 1deecb7e97a35782aa48f9053398d8b3ff9b0932). This refinement supersedes any implication in §9.3 that only five D operations are defined.

D's complete semantic operation set is:
1. RegisterProducerClass
2. RegisterProducerWork
3. InstallForgetFence
4. CaptureProducerRegistrationHighWater
5. RegisterDerivedDependency
6. PublishDerivedIfFenceCurrent
7. CompleteProducerWork
8. ResolveProducerWork
9. ReconcileForgetBarrier

D35-01 through D35-07 are DECIDED semantic contracts; D35-08 Storage/Consistency ownership and implementation is OPEN / owner unassigned; D35-09 E/I/H/B integration remains OPEN; D35-10 runtime fault tests are NOT RUN. D's operation contract expressly does not assert that APIs or a Storage transaction already exist.

ProducerRegistrationSequence / ProducerRegistrationHighWater and ProducerRegistryVersion are separate D ledger types. They are not CanonicalCommitCursor or ForgetFenceGeneration. E stores each unchanged and does not compare across namespaces.

The five operations explicitly requested in the Session E task are mapped in §1; this addendum supplies the four supporting operations required by D's current normative contract. CR-P1-01 and INT-P0-03 remain OPEN.



---
## 9.7 OPEN item precision — D semantic contract now specified

This section supersedes the earlier §5/§9.3/§9.5 wording to the extent it implies D's operation-level semantic inputs, outputs, idempotency, error outcomes or linearization points are still unspecified.

D's current normative file 03-memory-brain/forget-fence-operation-and-publication-gate.md specifies all nine semantic operations and their typed inputs/outputs, idempotency, error vocabulary and linearization points. D decision log §7 records D35-01 through D35-07 as DECIDED semantic contracts. In particular, RegisterProducerWork and InstallForgetFence share one linearizable order; fence installation captures ProducerRegistryVersion and ProducerRegistrationHighWater; CaptureProducerRegistrationHighWater verifies the immutable cutoff; PublishDerivedIfFenceCurrent is linearized with visibility; ResolveProducerWork and ReconcileForgetBarrier define recovery/reconciliation.

Accordingly:
- Any prior E OPEN item framed as “D has not defined operation inputs/outputs/errors/high-water/race ordering” is **SUPERSEDED**.
- Remaining OPEN: callable API/transport schemas and wire error mapping; I/H/B authenticated identity and PermissionEpoch binding; I/A reconciliation of global producer/recipient inventory with D's local registry; exact E recompile child/re-admission identity; named Storage/Consistency owner and tested transaction/CAS/hidden-prepare implementation; executable conformance.
- D35-08 is OPEN because Storage/Consistency ownership is unassigned and realization is unvalidated.
- D35-09 is OPEN for E/I/H/B integration and global inventory coordination.
- D35-10 is NOT RUN; design tables are not test results.

No D semantic decision is changed by this E update. CR-P1-01 and INT-P0-03 remain OPEN.


---

## 10. Phase 3.5 Reprocessing — Supersession, Source Evidence and Current OPEN Register

This section is the current E-side status record. Historical entries above remain for audit; conflicting statements are superseded here.

### 10.1 Superseded historical statements

| Historical statement | Status | Replacement |
|---|---|---|
| D Forget barrier/producer semantics absent | **SUPERSEDED** | D operation contract defines nine semantic operations, typed receipts, idempotency, errors and linearization |
| D operation inputs/outputs/errors/high-water/race order unspecified | **SUPERSEDED** | D35-01..07 semantic decisions; only callable transport/API and tested Storage realization remain OPEN |
| H/I branches absent | **SUPERSEDED** | Current H/I candidate packages read at HEADs below; existence is not approval |
| D CanonicalCommitCursor scope undecided or partitioned | **SUPERSEDED** | D decides one global sequence per Canonical Memory authority |
| Local E fence precheck/cached token sufficient for publication | **SUPERSEDED** | D PublishDerivedIfFenceCurrent linearizes with visibility and serializes against Fence installation |
| Lease expiry, queue deletion, worker loss or DLQ parking terminalizes work | **SUPERSEDED** | D barrier stays open until durable terminal receipt and reconciliation |
| Accepted implies compilation, canonical commit or publication | **SUPERSEDED** | AcceptedReceipt is durable ingress/compile-intent evidence only |
| E allocates CanonicalCommitCursor or IndexWatermark | **SUPERSEDED** | D owns CanonicalCommitCursor; F owns IndexWatermark; E stores owner-issued values unchanged |
| E may freeze Fact/Claim mapping | **SUPERSEDED / ADR-BLOCKED** | B Fact/Claim ADR remains ADR-BLOCKED; CandidateProposition/ExtractionIR stay pre-canonical |

### 10.2 Exact branch HEAD inventory read before this E commit

| Owner | Branch | Full HEAD SHA | Read/status |
|---|---|---|---|
| Main | `main` | `8a6414158c9c056c1638222534e1993d1bbc99d2` | Required D/E/H/I review read |
| A | `session-a-integration-2026-11-16` | `f18c64950a84385bd407752c7188e1bd52029a7b` | Read-only coordination input |
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` | Fact/Claim ADR remains ADR-BLOCKED |
| C | `session-c-agent-integration-2026-11-16` | `35de58ddc93c5f1e554596cdfc430cd6c392d355` | Not modified; no C decision inferred |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | Current Forget operations, cursor and decision log read |
| E parent | `session-e-memory-compiler-2026-11-16` | `13a720724fcfae84f4c4abe36fbc44dd2820445d` | Parent HEAD for this E-only update |
| F | `session-f-memory-runtime` | `8b16a3621cbe2be4badac1799822b64824532b25` | Not modified; no F implementation claim |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` | Not modified; no G implementation claim |
| H | `session-h-bmcp-protocol` | `a830628ec0f15a960277412c67c2197565ca1dc4` | Forget/Revocation/Offline Reconnect read; CANDIDATE |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | Global inventory/identity/Forget policy read; CANDIDATE |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `ec0e29d9b6e6e32728116514376214503aeb2434` | Proposed realization review; implementation OPEN |

### 10.3 Required source files read

- Cross-module review: `reviews/integration/phase-3-defghi-cross-module-contract-review.md` on main.
- D: `03-memory-brain/forget-fence-operation-and-publication-gate.md`, `commit-cursor-semantics.md`, `decision-change-log.md`.
- E: all five compiler design files, plus compiler-state, Forget/derived-registration, Accepted receipt/idempotency and this change log.
- H: `08-bmcp-protocol/forget-revocation-and-reconnect.md` (CANDIDATE).
- I: `09-security-governance/phase-3.5-global-identity-forget-governance.md`, `forget-retention-backup-and-erasure-policy.md`, `principal-actor-and-authorization-contract.md` (CANDIDATE).

### 10.4 OPEN register

| OPEN ID | Exact unresolved issue | Owner(s) |
|---|---|---|
| OPEN-API-01 | Callable D API/transport schemas, authenticated binding, serialization/versioning and semantic error-to-wire mapping | D/H/B/I |
| OPEN-STORAGE-01 | Named Storage owner and validated transaction/CAS/serializable/hidden-prepare realization; fence-to-visibility shared linearization, durability, failover, replica/read and restore guarantees | Storage + D/E |
| OPEN-I-AUTH-01 | Current I PermissionEpoch and authorization decision freshness/revocation proof at final publication boundary | I + D/E |
| OPEN-REGISTRY-GLOBAL-01 | Reconcile I ProducerDomainInventoryEpoch and A/module inventory with D ProducerRegistryVersion/ProducerRegistrationHighWater; prove global closed-world completeness | I/A + D/E/H |
| OPEN-RECOMPILE-01 | Explicit linked child/re-admission identity for recompile and barrier accounting | D/E |
| OPEN-REC-01 | AcceptedReceipt + payload ref + idempotency + CompileIntent/outbox transaction/WAL durability and crash-recovery profile | E + Storage |
| OPEN-REC-02 | Canonical semantic digest/canonicalization profile and B/H typed identity/Scope serialization | E + B/H/I |
| OPEN-REC-03 | Idempotency/tombstone retention horizon and disclosure-safe post-Forget receipt lookup | I + E/Storage |
| OPEN-TEST-01 | Executable race/fault fixtures, crash/failover injection, actual outputs and owner-reviewed evidence | D/E/Storage + consumers |

D operation-level semantic fields, result receipts, idempotency, error outcomes and linearization are DECIDED; this OPEN register must not be read as reopening those decisions. D35-08 Storage ownership/realization, D35-09 cross-owner integration and D35-10 runtime fault tests remain OPEN/NOT RUN.

### 10.5 Cross-owner disposition and non-claims

- D producer barrier and operation semantics are DECIDED; D/E/Storage implementation and executable conformance remain OPEN.
- CanonicalCommitCursor is one global sequence per Canonical Memory authority. AggregateRevision is per aggregate; LifecycleEventCursor per Memory; IndexWatermark per F index/channel partition; ForgetFenceGeneration is D's separate fencing namespace; PermissionEpoch is I-owned; ContextVersion is G-owned. No cross-namespace comparison or substitution.
- H/I packages exist but remain CANDIDATE. H ACK is target/action/capability/session bounded; I owns global inventory, target aggregation and completion.
- B Fact/Claim remains ADR-BLOCKED; no canonical schema/API/wire field is approved by this E update.
- CR-P1-01 and INT-P0-03 remain OPEN/BLOCKING. Documentation does not prove atomic D/E/Storage enforcement or global Forget completion.
- All fault/race cases are NOT RUN. No implementation, runtime, storage, security or performance test is claimed PASS.
- Only E-owned files under `04-memory-compiler/` are modified; all other module files are read-only inputs.

### 10.6 Files changed by this reprocessing

- `04-memory-compiler/compiler-state-and-producer-admission.md` — lifecycle, stable identities, lease/retry/DLQ/replay/recompile/terminal semantics and corrected D decision status.
- `04-memory-compiler/forget-fence-and-derived-registration.md` — five requested D operations + four supporting operations, visibility boundary, exact OPEN items and expanded fault matrix.
- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` — independent receipt state matrix, duplicate submission and recovery/replay semantics.
- `04-memory-compiler/decision-change-log.md` — supersession ledger, branch HEAD inventory, source read evidence and OPEN register.


### 10.7 Commit and readback evidence for this reprocessing

E-only file commits (each commit changes exactly the named path):

| File | Commit SHA |
|---|---|
| `compiler-state-and-producer-admission.md` | `2c11cca8ca2b68da53f8ede9e85acd56d8b34a96` |
| `forget-fence-and-derived-registration.md` | `262d36d2cc551192d75cf510eb44e4ae1795c1a8` |
| `accepted-receipt-and-idempotency-contract.md` | `07833bc582d63ba68000291fbf840cb97b42b575` |
| `decision-change-log.md` — supersession/source/HEAD record | `09f5892d0999f0933a73ccc6ac784ce4dd54e8a0` |
| `accepted-receipt-and-idempotency-contract.md` — explicit ForgetFenceGeneration namespace correction | `488621d0d2d8493bee2c098a791c96bbf3e3c954` |

Readback confirmed the updated files on the E branch, including the revalidation sections, D-to-E mapping, fault matrix, receipt state matrix, and typed cursor/fence-generation table. The final decision-log self-update commit and resulting branch HEAD are reported in the delivery record after refetch. No other path was changed by these commits.

The readback is document/commit evidence only. It does not establish an executable D endpoint, a Storage transaction, runtime publication safety, or test PASS.

 
---

## Phase 3.6 — Fence-Enforced Compiler Publication and Durable Dependency Atomicity

**Status:** DESIGN CONTRACT COMPLETE / IMPLEMENTATION NOT VERIFIED. This entry supersedes Phase 3.5 candidate wording only where the Phase 3.6 E-owned protocol below is more specific. It does not claim D/Storage/F/I approval or implementation.

### 1. Source baseline read for this pass

| Owner | Branch | HEAD read | Evidence / disposition |
|---|---|---|---|
| Integration review | main | `8a6414158c9c056c1638222534e1993d1bbc99d2` | `reviews/integration/phase-3-defghi-cross-module-contract-review.md`; Conditional Pass, CR-P1-01 OPEN/BLOCKING |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | D operation-level semantics; not yet a Phase 3.6-updated HEAD in this pass |
| E | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` | E source baseline before this Phase 3.6 change set |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` | Proposed shared serialization design only; not approved implementation |
| F | `session-f-memory-runtime` | `f86f9b536ea69d8e0fbb4bf290c7023ef0eada76` | Rebuild/backfill/replay consumer contract and typed evidence matrix |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | Global inventory branch HEAD; inventory artifact blob `9100061fa986fb6676656169de3fcf9fc1c72664` |

The current D branch contains the Phase 3.5 operation-level contract, not a separately verified Phase 3.6 operation revision. Storage's branch report is a proposed realization, not an approved Storage authority. The integration review is historical and remains Conditional Pass; it is not an approval of this E update.

### 2. D operation mapping consumed

E consumes D semantic operations without inventing transport schemas: RegisterProducerClass, RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. E's final gate requirement is that current fence validation, active work/attempt/lease validation, complete dependency receipts, current I authorization and the visibility transition share one serialization decision.

### 3. Joint decisions requested

- **D request:** confirm root WorkItemId stability across retry, DLQ replay, recompile and worker recovery; confirm that recompile uses a new DerivationRunId without changing the root barrier identity; confirm the exact current-fence/source-ancestor checks and publication-vs-fence race outcome.
- **Storage request:** confirm the shared transaction/serialization authority and exact linearization point spanning D's fence/producer ledger, complete dependency registration and artifact visibility marker; or provide the approved durable prepare/commit coordinator, hidden-prepare invariant, fence/permission revalidation at final visibility CAS, participant recovery and restore protocol.
- **I request:** confirm how current PermissionEpoch and revocation decision are made authoritative at the final visibility commit; E cannot independently assert currentness.
- **F request:** confirm indexer/rebuild/backfill/replay consume only committed PUBLISHED artifacts and revalidate current fence/permission before indexing and serving.

No response or approval is inferred from document presence. Confirmation status remains OPEN until an explicit owner decision is recorded.

### 4. E-owned paths changed

- `04-memory-compiler/compiler-state-and-producer-admission.md`
- `04-memory-compiler/forget-fence-and-derived-registration.md`
- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md`
- `04-memory-compiler/phase-3.6-producer-publication-conformance.md`
- `04-memory-compiler/decision-change-log.md`

No D, Storage, F, I or A path is modified by this change set.

### 5. Verification boundary

The documentation defines E's producer protocol, private staging, final publish gate, receipt semantics, retry/recovery rules and F handoff. It does not establish executable APIs, transaction isolation, atomic dependency registration, lease fencing, visibility enforcement, restore safety or runtime behavior. E36-01..20 are NOT RUN. Final commit/readback evidence is recorded in the delivery response after the E branch refetch.
