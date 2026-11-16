# Phase 3 — Cross-Module Contract Registry

- Owner: Session A / Principal Integration Architect
- Status: **CANDIDATE coordination register; not an ADR, contract freeze, or implementation approval**
- Updated: 2026-11-16
- A branch: `session-a-integration-2026-11-16`
- Rule: this registry coordinates owners and evidence; it does not replace any module's authority.

## 1. State vocabulary and evidence levels

These are independent evidence dimensions, not interchangeable approval labels:

| Dimension | Meaning |
|---|---|
| **File present** | Artifact exists at the recorded branch/ref and can be read. |
| **Owner decision** | The accountable module owner has explicitly decided the semantic point in an owned artifact. |
| **Cross-module aligned** | All affected authority owners and consumers have reconciled the interface; no unresolved semantic mismatch remains. |
| **Implementation/test verified** | Executable implementation and reproducible conformance evidence establish the behavior. |

A file can be present while its content remains CANDIDATE, OPEN or ADR-BLOCKED. Owner decision does not prove cross-module alignment. Cross-module alignment does not prove implementation or tests. No row is Contract Approved merely because files exist.

Decision labels: **DECIDED** (owner semantic decision), **CANDIDATE**, **ADR-BLOCKED**, **OPEN**, **TO_VALIDATE**. These labels do not collapse the four evidence dimensions above.

## 2. Actual branch inventory (queried 2026-11-16)

Full commit SHAs were re-resolved from the named branch refs at the start of this remediation. The reviewed main snapshot is recorded separately.

| Session | Branch | Actual HEAD SHA | Formal package / key artifacts | Presence and status |
|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `f76cc558273fbc1a27bb930a2f1e8d940b717c80` | `reviews/integration/contract-registry.md`; `reviews/integration/typed-cursor-and-watermark-contract.md`; `reviews/integration/cross-module-conformance-plan.md`; this remediation record | Present; coordination artifacts CANDIDATE |
| B | `session-b-domain-model-phase3` | `ab19afbf92f67fe0a7679e9aa3a35b015fed89f4` | `02-domain-model/` domain model and Fact/Claim ADR work; review/task-pack references | Branch present; Fact/Claim ADR remains ADR-BLOCKED; exact approval not evidenced |
| D | `session-d-memory-brain-2026-11-16` | `30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6` | `03-memory-brain/commit-cursor-semantics.md`; `03-memory-brain/forget-fence-and-completion-contract.md`; canonical store/version/lifecycle files; D review | Present; CanonicalCommitCursor semantics DECIDED by D; enforcement OPEN |
| E | `session-e-memory-compiler-2026-11-16` | `3dea6096eefa6779eb12e4e788bcf9429d2a3f83` | `04-memory-compiler/decision-change-log.md`; `accepted-receipt-and-idempotency-contract.md`; `forget-fence-and-derived-registration.md`; five compiler design files; E review | Present; candidate package; stale historical statements explicitly superseded by E §8 and current D/H/I refs |
| H | `session-h-bmcp-protocol` | `fcc5103399b4c322e52d642cae5a2414969399a7` | `08-bmcp-protocol/protocol-overview.md`; `message-envelope-and-versioning.md`; `context-delivery-and-acknowledgement.md`; `adapter-capability-and-applied-attestation.md`; `forget-revocation-and-reconnect.md`; `protocol-conformance-matrix.md` | **Design package exists; cross-module contract pending verification**. Candidate, not approved |
| I | `session-i-security-governance-2026-11-16` | `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb` | `09-security-governance/security-and-identity-overview.md`; `principal-actor-and-authorization-contract.md`; `scope-and-revocation-policy.md`; `forget-retention-backup-and-erasure-policy.md`; threat model; audit/exception governance | **Design package exists; cross-module contract pending verification**. Candidate, not approved |

Main review snapshot: `main @ 8a6414158c9c056c1638222534e1993d1bbc99d2`. Parent four-way review: `reviews/integration/phase-3-defghi-cross-module-contract-review.md`. Task pack: `reviews/integration/phase-3-cross-module-remediation-task-pack.md`.

F/G remain dependencies. Their older refs in prior registry/task-pack are historical baselines, not re-queried HEADs in this A remediation; A makes no current-HEAD claim for F/G here. Storage/Consistency implementation owner remains to be named by engineering.

## 3. Issue register — CR findings

| ID | Current state | Accountable owner | Dependencies | Required closure evidence |
|---|---|---|---|---|
| CR-P1-01 D/E producer admission, fence installation and publication linearization | **OPEN / blocking Forget conformance** | D + E jointly at boundary; Storage/Consistency implementation owner TBD | D producer-class and work-item registration; E staged derivative/lineage; atomic dependency registration; fence-aware publish gate | Normative operation/linearization contract, crash/recovery and lease/DLQ/replay rules, race matrix for both serializations, executable tests proving no late publication |
| CR-P1-02 Canonical cursor mismatch | **A coordination correction delivered; integration remains OPEN** | D owns semantics; A coordinates; E/F/G/Storage consume | D global per-authority cursor; E representation; F/G consumer watermarks; Storage sequencing | A typed proposal aligned; E stale text reconciled by E; F/G consumer conformance; Storage transaction/recovery proof |
| CR-P1-03 Registry stale source refs and H/I presence | **A registry correction delivered; ongoing registry freshness required** | A | Actual branch refs and package inventory | Re-queryable branch HEADs and artifact paths; H/I recorded as present candidate packages; evidence dimensions kept separate |
| CR-P1-04 E decision/change-log supersession hygiene | **OPEN / E-owned** | E | D cursor decision; current H/I package refs; historical E statements | E adds explicit supersession/current-state notice while preserving history; E branch readback and owner review |
| CR-P1-05 I global Forget vector / D-H-E target mapping | **OPEN / owner mapping required** | I (global policy); D/E/H/F/G own local evidence | H ACK-to-I target state mapping; Adapter identity/capability/session/region; producer-domain epoch vs work-item barrier; typed fence vs permission epoch | Owner-approved mapping table and negative/unknown/offline cases; no implicit success; conformance evidence |

## 4. INT issue register

| ID | State | Accountable owner | Dependencies | Closure conditions |
|---|---|---|---|---|
| INT-P0-01 Fact/Claim normative identity | **ADR-BLOCKED** | B + Architecture Governance | Domain alternatives; D/E/F/G consumers | Approved ADR and synchronized consumer mappings; no schema freeze before approval |
| INT-P0-02 Principal/ActorRef/ScopeRef/permission binding | **OPEN / identity contract freeze blocked** | I (policy) with B (typed domain refs) and H (transport binding) | Producer identity, issuer/delegation, ScopeRef mapping, E idempotency namespace, D/E/F/G enforcement | Joint owner mapping and approved typed references; authenticated binding; cross-scope and stale-epoch negative tests |
| INT-P0-03 Forget/retention completion and anti-resurrection | **OPEN / blocking** | I (global completion policy); D/E/F/G/H/Storage local enforcement | D fence; E admission/derivative barrier; F suppression; G reconciliation; H clear attestations; backup/external inventory | Atomic D/E/Storage gate; closed target inventory; all required target proofs; restore/replay and late-derivative tests |
| INT-P0-04 Prompt-injection residual risk | **OPEN** | I security governance; C/H inference boundary | B/E provenance and trust labels; C/H protected prompt boundary; Agent tool authorization | Threat model, mitigations, explicit residual-risk acceptance authority and adversarial tests |
| INT-P1-01 ContextVersion/ChangeSet authority | **CANDIDATE** | G | H delivery, C final request boundary, INT-P0-02/03 | G owner decision, H/C proof mapping, CAS/replay/late-ack tests |
| INT-P1-02 Claim revision/ConflictSet/Merge/Split | **ADR-BLOCKED** | B | INT-P0-01; D persistence; E/F/G consumers | Approved Fact/Claim ADR and owner mappings/migration tests |
| INT-P1-03 Telemetry identity/event/ordering | **CANDIDATE** | C | B refs, H envelope, I authenticated identity, E ingress | C owner decision and duplicate/out-of-order/correction tests |
| INT-P1-04 Accepted durability/idempotency | **CANDIDATE** | E | H envelope, I identity/retention, Storage transaction/outbox | E/H/I owner approval and crash/replay evidence |
| INT-P1-05 Applied final-request proof | **CANDIDATE** | G (consumer semantics); H/C produce evidence | Exact request/session/version/delivery/capability | Joint proof semantics and final-boundary conformance |
| INT-P1-06 Provenance/Lifecycle/reference semantics | **OPEN** | B (domain semantics) with D/E | D lifecycle, E provenance, I retention, cursor contract | Typed refs/time/provenance owner alignment and traversal/Forget tests |

## 5. INT-X and D-local coordination register

| ID | State | Owner | Dependency / closure evidence |
|---|---|---|---|
| INT-X-01 Typed cursor/watermark and causal ordering | **CANDIDATE; D semantic decision recorded** | A coordinates; D owns CanonicalCommitCursor | This typed contract aligned to D; Storage durability/recovery; E/F/G consumer conformance |
| INT-X-02 Forget fence/barrier/completion | **OPEN** | I global; D/E/F/G/H local | CR-P1-01/05; target mapping and race tests |
| INT-X-03 Principal/ActorRef/ScopeRef/permission epoch | **OPEN** | I + B + H by authority boundary | INT-P0-02 exact typed mapping and negative tests |
| INT-X-04 Context delivery/Applied/clear/reconnect | **OPEN** | H (wire/Adapter) + G (Context) + C (inference boundary) | INT-P1-01/05; delivery/reconnect/final-request evidence |
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
| D → E: Canonical Memory, MemoryVersion, ForgetFence, Producer Barrier | D | E | D canonical semantics DECIDED; barrier operation OPEN | Exact admission/registration/fence/publication linearization |
| E → D: Canonical Commit, Dependency Registration, Fence-aware Publication | D owns commit; E submits proposals and derivative registrations | D | Candidate interface; atomic boundary OPEN | Durable registration receipt, visibility gate, retries/recovery |
| D/E → F: Canonical Cursor, Forget Suppression, Derived Memory Watermarks | D owns canonical cursor/fence; E supplies derived lineage/work; F owns IndexWatermark | F | D cursor DECIDED; F consumer mapping not verified | Index/channel partition watermarks, suppression/rebuild behavior |
| F → G: RetrievalResult, ActivationRecommendation | F | G | F owns result semantics; consumer alignment not verified here | Freshness/completeness and immutable candidate refs |
| D → G: immutable MemoryVersion references | D | G | D owns immutable version references | G must pin exact versions and revalidate lifecycle/Forget |
| G → H: ContextVersion, ChangeSet, Delivery, Applied Attestation intent | G owns Context state/intent; H owns wire/Adapter ACK | H | Candidate boundary; cross-owner mapping OPEN | Delivery state, final-request proof and ACK semantics |
| I → D/E/F/G/H: identity, authorization, retention, Forget Governance | I | D/E/F/G/H | I package present CANDIDATE; cross-module mapping OPEN | B typed refs; permission epoch; global target inventory and local evidence |
| B → D/E/F/G/H: Fact/Claim, ActorRef, ScopeRef domain semantics | B | D/E/F/G/H | Fact/Claim ADR-BLOCKED; typed refs not frozen | B ADR and I/H mapping; no premature schema freeze |

## 7. H/I presence and approval statement

H and I design packages exist on their named branches at the exact HEADs in §2. Their existence is a repository fact only. It does **not** close INT-P0-02, INT-P0-03, INT-P0-04, INT-X-02, INT-X-03 or INT-X-04, and does not constitute Contract Approved. H/I cross-module contracts remain candidate/pending owner verification.

## 8. Gate discipline

No item is closed by this registry. A closure requires the accountable owner, a versioned artifact, named dependencies, and evidence matching the row's exit condition. Implementation/test verification additionally requires executable test ID/version, environment, fixtures, expected/actual results, logs/artifact references and reproducible rerun. Static document review is not runtime proof.

Historical task-pack baselines and earlier registry values are not current HEAD evidence. The branch SHAs in §2 are the refs re-resolved for this remediation. No module branch was modified or merged.
