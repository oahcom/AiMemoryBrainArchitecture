# Phase 3 — Cross-Module Contract Registry

- Owner: Session A / Principal Integration Architect
- Status: **CANDIDATE coordination register; not an ADR, contract freeze, or implementation approval**
- Updated: 2026-11-16 (re-executed against live branch refs)
- A branch: `session-a-integration-2026-11-16`
- Rule: this registry coordinates owners and evidence; it does not replace any module's authority.

## 1. State vocabulary and evidence levels

These are independent evidence dimensions, not interchangeable approval labels.

| Evidence dimension | Meaning |
|---|---|
| **File present** | Artifact exists at the recorded branch/ref and was readable. |
| **Owner decision** | The accountable module owner explicitly decided the semantic point in an owned artifact. |
| **Cross-module aligned** | All affected authority owners and consumers reconciled the interface; no unresolved semantic mismatch remains. |
| **Implementation/test verified** | Executable implementation and reproducible conformance evidence establish the behavior. |

A file can be present while its content is CANDIDATE, OPEN or ADR-BLOCKED. Owner decision does not prove cross-module alignment. Cross-module alignment does not prove implementation or tests. No row is Contract Approved merely because files exist.

Decision labels: **DECIDED**, **CANDIDATE**, **ADR-BLOCKED**, **OPEN**, **TO_VALIDATE**.

## 2. Live branch inventory and source evidence

Branch HEADs below were queried directly from GitHub branch refs at the start of this A re-execution. The main review baseline is recorded separately. A's listed HEAD is the pre-write source HEAD; the final post-write A HEAD is recorded in the remediation record.

| Session | Branch | Live HEAD SHA | Formal package / key artifacts inspected | Evidence status |
|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `e270118dd22e47140a5232f5f131d97e965d39dc` | `reviews/integration/contract-registry.md`; `typed-cursor-and-watermark-contract.md`; `cross-module-conformance-plan.md`; A remediation record | Present; coordination artifacts CANDIDATE |
| B | `session-b-domain-model-phase3` | `ab19afbf92f67fe0a7679e9aa3a35b015fed89f4` | `02-domain-model/domain-model-overview.md`; `typed-reference-and-scope-semantics.md`; `adr/ADR-001-fact-claim-canonical-model.md`; `fact-claim-consumer-mapping.md` | Package present; ADR explicitly ADR-BLOCKED; typed refs CANDIDATE |
| D | `session-d-memory-brain-2026-11-16` | `30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6` | `03-memory-brain/commit-cursor-semantics.md`; `forget-fence-and-completion-contract.md`; canonical store/version/lifecycle files; `reviews/03-memory-brain/three-party-six-dimension-review.md` | Package present; per-authority global cursor semantics DECIDED; storage and producer gate enforcement OPEN |
| E | `session-e-memory-compiler-2026-11-16` | `2dea3ae510c57987460d940224db569d43df78f1` | `04-memory-compiler/decision-change-log.md`; `accepted-receipt-and-idempotency-contract.md`; `forget-fence-and-derived-registration.md`; five compiler design files; `reviews/04-memory-compiler/three-party-six-dimension-review.md` | Package present; cursor decision consumed in §9; atomic D/E/Storage gate OPEN; log's H/I refresh now behind live refs |
| H | `session-h-bmcp-protocol` | `d46961254bc50995479bd43abed0ee6fe1cdcbb6` | `08-bmcp-protocol/protocol-overview.md`; `message-envelope-and-versioning.md`; `context-delivery-and-acknowledgement.md`; `adapter-capability-and-applied-attestation.md`; `forget-revocation-and-reconnect.md`; `adapter-forget-ack-and-target-binding.md`; `protocol-conformance-matrix.md` | **Design package exists; cross-module contract pending verification**; CANDIDATE, not approved |
| I | `session-i-security-governance-2026-11-16` | `4c7c5f953b166bc512064f6de3b7d18a742d0449` | `09-security-governance/security-and-identity-overview.md`; `principal-actor-and-authorization-contract.md`; `scope-and-revocation-policy.md`; `forget-retention-backup-and-erasure-policy.md`; `global-forget-target-inventory-and-completion-evidence.md`; threat model; audit/exception governance; Phase 3 remediation report | **Design package exists; cross-module contract pending verification**; CANDIDATE, not approved |

Main review baseline: `main @ 8a6414158c9c056c1638222534e1993d1bbc99d2`.
- Four-way review: `reviews/integration/phase-3-defghi-cross-module-contract-review.md` (blob `edaccb802e0425f2d47bd4b613fab4dfde107144`).
- Task pack: `reviews/integration/phase-3-cross-module-remediation-task-pack.md` (blob `7abe73e5209ee985c9807b95d99616069911a6b7`).
- D cursor decision: D branch file blob `4688a0ca487bf4d853c7f0220408abe8d743d159`.
- E decision/change log: E branch file blob `507af0e1b993334df5c24f02785c28c0e3997172`.
- H envelope / Forget ACK: blobs `5547ecd78d118bd63e571e5daad87194d9b694e4` / `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8`.
- I identity / global Forget inventory: blobs `4f6f5691a599a0566b036f4240003152d64e2242` / `1c1df360b4586e9b83fb62ee0a808bf5d27ba476`.
- B ADR-001: blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`; its own text explicitly states ADR-BLOCKED.

F/G remain required consumers. Their current branch HEADs and current consumer artifacts were not re-queried in this A run; no current-HEAD or consumer-conformance claim is made for F/G. Storage/Consistency implementation owner remains to be named by engineering.

## 3. CR issue register

| ID | Current state | Accountable owner | Dependencies | Required closure evidence |
|---|---|---|---|---|
| CR-P1-01 D/E producer admission, fence installation and publication linearization | **OPEN / blocking Forget conformance** | D + E jointly at boundary; Storage/Consistency implementation owner TBD | D producer-class/work-item registration and fence high-water; E staged derivative/lineage; atomic dependency registration; final fence-aware publish gate | Callable operation/linearization contract; crash/recovery, lease/DLQ/replay rules; both race serializations; executable tests proving no late publication |
| CR-P1-02 Canonical cursor mismatch | **A semantic coordination correction delivered; integration OPEN** | D owns semantics; A coordinates; E/F/G/Storage consume | D global per-authority cursor; E representation; F/G consumer watermarks; Storage sequencing | A proposal aligned to D; E current cursor consumption; F/G consumer conformance; Storage transaction/recovery proof |
| CR-P1-03 Registry stale source refs and H/I presence | **Re-executed A registry correction delivered; freshness remains ongoing** | A | Live branch refs and package inventory | Re-queryable branch HEADs/artifact paths; H/I marked present candidate packages; four evidence dimensions retained |
| CR-P1-04 E decision/change-log supersession hygiene | **OPEN / E-owned follow-up** | E | D cursor decision; current H/I refs; historical E statements and current refresh | E-owned supersession/current-state notice refreshed to live H/I heads; E readback and owner review |
| CR-P1-05 I global Forget vector / D-H-E target mapping | **I candidate mapping present; cross-owner verification OPEN** | I global policy; D/E/H/F/G own local evidence | H ACK-to-I target-state mapping; Adapter identity/capability/session/region; I inventory epoch vs D work barrier; typed fence vs permission epoch | Owner-approved mapping and negative/offline/unsupported cases; no implicit success; conformance evidence |
| CR-P0-01 Fact/Claim canonical semantics | **ADR-BLOCKED** | B + Architecture Governance | B ADR-001 and D/E/F/G consumer mappings | Explicit formal ADR approval by accountable governance authority; synchronized consumer contracts; no schema/API freeze before approval |
| CR-P0-02 Principal/ActorRef/ScopeRef identity mapping | **OPEN / identity freeze blocked** | I policy; B typed refs; H transport binding | Issuer/delegation binding, ProducerIdentity, ScopeRef semantics, PermissionEpoch, E idempotency namespace | Joint B/I/H owner mapping, authenticated binding contract, cross-scope/stale-epoch negative tests |

## 4. INT issue register

| ID | State | Accountable owner | Dependencies | Closure conditions |
|---|---|---|---|---|
| INT-P0-01 Fact/Claim normative identity | **ADR-BLOCKED** | B + Architecture Governance | Domain alternatives; D/E/F/G consumers | Approved ADR and synchronized consumer mappings; no schema freeze before approval |
| INT-P0-02 Principal/ActorRef/ScopeRef/permission binding | **OPEN / identity contract freeze blocked** | I policy with B typed refs and H transport binding | Producer identity, issuer/delegation, ScopeRef mapping, E idempotency namespace, D/E/F/G enforcement | Joint owner mapping and approved typed references; authenticated binding; cross-scope and stale-epoch negative tests |
| INT-P0-03 Forget/retention completion and anti-resurrection | **OPEN / blocking** | I global completion policy; D/E/F/G/H/Storage local enforcement | D fence; E admission/derivative barrier; F suppression; G reconciliation; H clear attestations; backup/external inventory | Atomic D/E/Storage gate; sealed target inventory; all required target proofs; restore/replay and late-derivative tests |
| INT-P0-04 Prompt-injection residual risk | **OPEN** | I security governance; C/H inference boundary | B/E provenance and trust labels; C/H protected prompt boundary; Agent tool authorization | Threat model, mitigations, explicit residual-risk acceptance authority and adversarial tests |
| INT-P1-01 ContextVersion/ChangeSet authority | **CANDIDATE** | G | H delivery, C final request boundary, INT-P0-02/03 | G owner decision, H/C proof mapping, CAS/replay/late-ACK tests |
| INT-P1-02 Claim revision/ConflictSet/Merge/Split | **ADR-BLOCKED** | B | INT-P0-01; D persistence; E/F/G consumers | Approved Fact/Claim ADR and owner mappings/migration tests |
| INT-P1-03 Telemetry identity/event/ordering | **CANDIDATE** | C | B refs, H envelope, I authenticated identity, E ingress | C owner decision and duplicate/out-of-order/correction tests |
| INT-P1-04 Accepted durability/idempotency | **CANDIDATE** | E | H envelope, I identity/retention, Storage transaction/outbox | E/H/I owner approval and crash/replay evidence |
| INT-P1-05 Applied final-request proof | **CANDIDATE** | G consumer semantics; H/C produce evidence | Exact request/session/version/delivery/capability | Joint proof semantics and final-boundary conformance |
| INT-P1-06 Provenance/Lifecycle/reference semantics | **OPEN** | B domain semantics with D/E | D lifecycle, E provenance, I retention, cursor contract | Typed refs/time/provenance owner alignment and traversal/Forget tests |

## 5. INT-X and D-local coordination register

| ID | State | Owner | Dependency / closure evidence |
|---|---|---|---|
| INT-X-01 Typed cursor/watermark and causal ordering | **CANDIDATE; D semantic decision recorded** | A coordinates; D owns CanonicalCommitCursor; F owns IndexWatermark | A proposal aligned; Storage durability/recovery and E/F/G consumer conformance |
| INT-X-02 Forget fence/barrier/completion | **OPEN** | I global; D/E/F/G/H local | CR-P1-01/05; target mapping and race tests |
| INT-X-03 Principal/ActorRef/ScopeRef/PermissionEpoch | **OPEN** | I + B + H by authority boundary | INT-P0-02 exact typed mapping and negative tests |
| INT-X-04 Context delivery/Applied/clear/reconnect | **OPEN** | H wire/Adapter; G Context; C inference boundary | INT-P1-01/05; delivery/reconnect/final-request evidence |
| INT-X-05 Canonical lifecycle/Claim revision/ConflictSet | **ADR-BLOCKED where dependent on Fact/Claim** | B; D owns canonical Memory lifecycle | INT-P0-01 and D owner alignment |
| INT-X-06 Accepted/idempotency/replay/retention | **CANDIDATE** | E; H/I/Storage dependencies | INT-P1-04; crash/replay and retention approval |
| INT-X-07 Shared conformance/fault-injection suite | **TO_VALIDATE** | A coordinates; testing owner TBD | Executable suite, declared environment/fixtures, raw logs and reproducible rerun |
| INT-X-08 Workload benchmarks/resource budgets | **OPEN** | Engineering owner TBD | Stable contracts and reproducible workload/hardware measurements |
| D-REV-P1-001 lifecycle/Forget vocabulary | **CANDIDATE pending D review evidence** | D | One consistent normative lifecycle table and I mapping |
| D-REV-P1-002 canonical commit sequence scope | **D DECIDED; Storage/consumer validation OPEN** | D semantics; Storage implementation | Per-authority global cursor semantics; transaction visibility/gap/replay/recovery tests |
| D-REV-P1-003 durable Forget fence and late-derivative barrier | **OPEN** | D + E; I global completion | Atomic producer admission/fence/publication gate and conformance race evidence |

## 6. Cross-module dependency map

| Dependency | Authority / producer | Consumer(s) | Version status | Open items |
|---|---|---|---|---|
| D → E: Canonical Memory, MemoryVersion, ForgetFence, Producer Barrier | D | E | Canonical semantics and barrier invariants DECIDED by D; callable atomic boundary OPEN | Producer-class vs work-item registration; exact fence/admission/publication linearization |
| E → D: Canonical Commit, Dependency Registration, Fence-aware Publication | D owns commit; E submits proposals and derivative registrations | D | Candidate interface; atomic boundary OPEN | Durable registration receipt, visibility gate, retry/recovery and final recheck |
| D/E → F: Canonical Cursor, Forget Suppression, Derived Memory Watermarks | D owns canonical cursor/fence; E supplies derived lineage/work; F owns IndexWatermark | F | D cursor DECIDED; F consumer mapping not verified in this run | Index/channel partition watermarks, suppression/rebuild and replay behavior |
| F → G: RetrievalResult, ActivationRecommendation | F | G | F owns result semantics; current consumer alignment not verified | Freshness/completeness and immutable candidate refs |
| D → G: immutable MemoryVersion references | D | G | D owns immutable version refs | G pins exact versions and revalidates lifecycle/Forget |
| G → H: ContextVersion, ChangeSet, Delivery, Applied Attestation intent | G owns Context state/intent; H owns wire/Adapter ACK | H | Candidate boundary; cross-owner mapping OPEN | Delivery state, final-request proof, ACK and reconnect semantics |
| I → D/E/F/G/H: identity, authorization, retention, Forget Governance | I | D/E/F/G/H | I package present CANDIDATE; cross-module mapping OPEN | B typed refs; PermissionEpoch; global inventory and local evidence |
| B → D/E/F/G/H: Fact/Claim, ActorRef, ScopeRef domain semantics | B | D/E/F/G/H | Fact/Claim ADR-BLOCKED; typed refs CANDIDATE | B/Governance ADR; I/H mapping; no premature schema freeze |

## 7. H/I presence and approval statement

H and I design packages exist on their named branches at the live HEADs in §2. Their existence is a repository fact only. It does **not** close INT-P0-02, INT-P0-03, INT-P0-04, INT-X-02, INT-X-03 or INT-X-04, and does not constitute Contract Approved. H/I cross-module contracts remain CANDIDATE/pending owner verification.

## 8. Gate discipline and limitations

No item is closed by this registry. Closure requires the accountable owner, a versioned artifact, named dependencies and evidence matching the row's exit condition. Implementation/test verification additionally requires executable test ID/version, environment, fixtures, expected/actual results, logs/artifact references and reproducible rerun. Static document review is not runtime proof.

The four-way review is a static branch-aware document review, not implementation evidence. The E change log's recorded H/I source refs are older than the live H/I HEADs recorded here; E must refresh its own source baseline. F/G live HEADs were not queried in this A run. No module branch was modified or merged by this registry update.
