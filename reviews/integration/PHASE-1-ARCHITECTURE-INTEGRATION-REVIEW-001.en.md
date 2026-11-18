# Phase 1 Architecture Integration Review — A/B/C

- Document ID: ARCH-INTEGRATION-REVIEW-P1-ABC-001-EN
- Version: 1.0.0
- Status: **CANDIDATE — integration review; not architecture approval or freeze**
- Review date: 2026-11-18
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base: `main@6b5db2918cffc2281deb22fd9858a37dbaeec726`
- Scope: A (system/technology reality), B (canonical domain model), C (Agent integration/inference boundary)
- Authority: integration review only. A/B/C and other domain Owners retain their decision rights.

## 1. Executive disposition

**Overall: PARTIAL INTEGRATION — NOT READY FOR ARCHITECTURE FREEZE.**

This report integrates A/B/C source packages and their available reviews against the observed main baseline. It does not select a technology stack, approve an ADR, change Owner contracts, authorize implementation or close Issue #43.

The most important conclusions are:

1. **DECIDED (bounded):** Phase 1 domain implementation has a limited freeze for Event, Memory, MemoryVersion, Claim as a proposition, ScopeRef separation from Permission, immutable MemoryVersion and provenance references. This is not a global domain freeze.
2. **OPEN:** Fact/Claim representation and Claim identity across Memory Versions remain unresolved. The current domain overview's wording that Fact is merely a qualified Claim conflicts with architecture invariant I-04 and the blocked Fact/Claim ADR. Do not silently treat the overview wording as a governance decision.
3. **CANDIDATE:** A local-first modular monolith is a sensible starting topology; SQLite WAL is bounded to same-host/single-writer use. Neither is a production deployment decision.
4. **CANDIDATE / OPEN:** C's Agent/Model/Provider/Tool/Brain evidence boundaries are coherent, but cross-owner bindings and exact Applied evidence acceptance are not frozen.
5. **DECIDED (semantic authority):** G owns the Applied state/predicate; C produces actual final-request submission evidence; H owns wire/transport; I owns authorization; D owns Forget-fence semantics. No single receipt substitutes for the others.
6. **TO_VALIDATE:** Cross-module race, recovery, replay, security, provider-side-effect and end-to-end Applied conformance need reproducible integration tests. Design documents and bounded reference tests do not establish production behavior.

No finding in this report authorizes production readiness.

## 2. Exact source and review pins

A branch HEAD and a file Blob SHA are different identities. The following table records exact source Blob SHAs actually fetched for this review. Research branch/PR commit values below are the reviewed snapshots declared by the corresponding PR/review records; they are not asserted as today's branch tips unless separately stated.

| Track | Primary design/source | Blob SHA | Review / reconciliation source | Blob SHA |
|---|---|---|---|---|
| A | `TECH-REALITY-001-A/README.md` (research branch `ai/TECH-REALITY-001-A/principal-technology-research`) | `e69498b4945213e797e9c7ba1ab5a4a3080c2b6a` | `TECH-REALITY-001-A-independent-review.md` | `ce0eac90abe2fe558b7d594f44501bbddac9678` |
| A | `technology-recommendation.md` | `cc2269dfd5d95fe85089287e1be9579bddce1ef2` | `TECH-REALITY-001-A-independent-review-follow-up.md` | `b0dc6a76bca0d5ddc55f97a5bfb61347fe07304f` |
| A | `owner-dependency-register.md` | `58fd1ecb1ef318de92a2ad9fa3ab9147ec2999a5` | — | — |
| B | `DOMAIN-REALITY-001-B/README.md` (research branch `research/domain-reality-001-b`) | `66ad32e6a2ce5369c49984738bb8fb17b3c2048a` | `B5-LATEST-HEAD-RECHECK-002.en.md` | `ede8f2698463a41330ed318935cfb70b032054a7` |
| B | `canonical-domain-model.md` | `ce441336e2fbba7c7a28c0b4c75482d524a4ade7` | `B5-LATEST-HEAD-RECHECK-002.zh-CN.md` | `54218eb060025ed182863097b80262cb58a3eaa5` |
| B | `domain-semantics-conflict-register.md` | `3063d0620dafd23dff30f91181d9c329552ee11e` | Mainline `02-domain-model/phase-1-domain-model-freeze.md` | `8be3d7d48be35f847fe97c9d217d684c3f41644a` |
| B | Mainline `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | Mainline `02-domain-model/ADR-001-fact-claim-semantics.md` | `a1024938ff5baba069cf128c69496a44e143330c` |
| C | `TECH-REALITY-001-C/README.md` (research branch `research/tech-reality-001-c`) | `d913cf925e54e30ca05bbfa64fe2fdd282e1ecda` | `C-REVIEW-001-agent-integration-independent-review.md` | `e704004b13007a80c4f03408b9db2ea067cf76b5` |
| C | `agent-integration-canonical-contract.md` | `eaf8c2d3d4449a5fefe78498a8a22d2764796059` | `C-REVIEW-001-phase-3.8.24-h-applied-delivery-evidence-consumer-review.md` | `3300d95b3074a7bf6690718e0ab7f6cbd9afb9ae` |
| C | `agent-integration-cross-owner-contract-matrix.md` | `e0cdd1d318adf5e5f48ad8602a8e3c986d0e4c0f` | Mainline `01-system-architecture/system-overview.md` | `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256` |
| A integration | `phase-3.5-cross-module-closure-review.md` | `a05f1d817514bbed7bddec1729d6598d0835ef3e` | `phase-3.6-baseline-manifest.md` | `0a2dd28a1977f6e73340e2f5daafd8da5c8ff5c2` |

**Review evidence caveat:** A's independent review is separate-session/context review, not a different model/provider or human audit. B's B5 recheck is explicitly an A integration evidence review, not a complete independent semantic review or B Owner approval. C-REVIEW-001 is delegated C-role technical review/remediation; human independent review remains pending. These review artifacts are not equivalent approval signatures.

**B source-currentness caveat:** The B research README and some embedded source snapshots contain historical main/branch/PR values. The B5 latest-head recheck explicitly records target PR #55 Head `e9554bd36bb2848441965bcf587413e7280482ed`, historical main `e52594f181d2edb77448adcf64f2` (full SHA recorded in the artifact), and identifies residual parity/currentness findings. Use the exact Blob pins above for the inspected bytes; do not copy the README's embedded baseline as today's main.

## 3. Current main baseline

Observed main HEAD for this review: `6b5db2918cffc2281deb22fd9858a37dbaeec726`.

The baseline files read for the system contract include:

- `01-system-architecture/system-overview.md` — Blob `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256`
- `02-domain-model/phase-1-domain-model-freeze.md` — Blob `8be3d7d48be35f847fe97c9d217d684c3f41644a`
- `02-domain-model/domain-model-overview.md` — Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`
- `02-domain-model/ADR-001-fact-claim-semantics.md` — Blob `a1024938ff5baba069cf128c69496a44e143330c`
- `00-governance/architecture-invariants.md` — Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe`

The baseline is newer than the previously relayed `aa711289...` snapshot. This report uses the actual main HEAD observed during this run.

## 4. Cross-module interface matrix

| Interface / data boundary | Authority and producer | Consumer / required behavior | Status | Evidence gap / closure |
|---|---|---|---|---|
| Canonical object vocabulary and typed refs | B defines domain meaning and typed identity semantics | D/E/F/G/H/I/Storage consume refs without treating them as grants | DECIDED for Phase 1 object separation; CANDIDATE for broader typed identity/authority binding | Fact/Claim and Claim identity ADRs remain blocked; exact cross-owner field mapping required |
| Event acceptance → compiler work | Storage/Event Store provides durable accepted custody; E owns compiler work and derivative lifecycle | E must not report semantic compilation or canonical publication from durable acceptance alone | DECIDED boundary; physical sequence TO_VALIDATE | Event/receipt/outbox semantics and E work lifecycle require exact end-to-end recovery/fault evidence; do not duplicate Event Store work |
| Canonical Memory / MemoryVersion | B defines meaning; D owns canonical lifecycle, version and Forget operations; Storage implements durable transaction | Immutable versions, CAS/stale-write handling, canonical commit cursor and provenance visibility | DECIDED bounded Phase 1 domain semantics; runtime proof tracked by Storage PRs | Multi-owner publication/Forget linearization and production deployment remain OPEN; review PR #244/#249 rather than recreate |
| Claim / Fact | B owns shared domain semantics; Architecture Governance decides ADR; D owns canonical persistence if adopted | E proposes candidate propositions; consumers must not mint or freeze Fact/Claim identity | OPEN / ADR-BLOCKED | Overview wording conflicts with I-04; preserve neutral PropositionRef or existing bounded Phase 1 Claim semantics until ADR approval |
| Scope / Permission / Principal | B owns typed domain reference meaning; I owns authentication, authorization, delegation and PermissionEpoch; H transports authenticated identity | All read/write paths fail closed on mismatched scope, actor, permission or stale epoch | DECIDED distinction; cross-owner trust binding CANDIDATE / OPEN | B/I/H exact shared version and negative conformance evidence not fully accepted |
| Agent / Model / Provider / Tool | C defines Agent integration requirements and request/attempt semantics | Agent plans/acts; Brain owns canonical memory; provider and tool outputs are evidence, not canonical success | DECIDED as C semantic boundary within its authority | Cross-owner identity, retry, provider idempotency and side-effect evidence require implementation validation |
| Provider handoff / outcome | C owns ProviderAttempt and handoff semantics | Preserve ACCEPTED / REJECTED / NOT_INVOKED / UNKNOWN / IN_DOUBT; reconcile same attempt after ambiguous handoff | CANDIDATE / OPEN for joint bindings | No C end-to-end Provider/Brain integration execution; UNKNOWN/IN_DOUBT recovery and provider-specific idempotency TO_VALIDATE |
| Context delivery / Applied | G owns ContextVersion, ChangeSet and Applied state; H owns transport/wire/ACK; C emits final-request evidence; I authorizes; D supplies Forget currentness | Delivery, materialization, final request submission, Applied and execution start remain distinct | DECIDED ownership split; cross-owner Applied predicate CANDIDATE / OPEN | H 1.0.0 identity shape candidate only; COutcomeRecord/final-boundary field mapping not accepted; G durable Applied persistence/recovery not proven |
| Forget / revocation / visibility | D owns Forget operation/fence and canonical suppression; I owns global policy/authorization/inventory; Storage owns physical persistence/visibility; E/F/G/H enforce local effects | No stale derivative/context/read may resurrect or expose fenced content | DECIDED ownership separation; global completion OPEN | JF-10/physical visibility/recovery is separate from SQLite Phase 1 tests; rely on dedicated D/E/I/Storage work |
| Observability / audit | C telemetry requirements; I audit/privacy governance; each owner emits authoritative evidence for its own transitions | Trace IDs correlate but do not become authorization or audit proof | CANDIDATE | Redaction, retention, integrity and production issuer/key registration remain TO_VALIDATE |

## 5. Responsibility conflict table

| ID | Conflict / stale or incompatible claim | Correct authority split | Status | Required action |
|---|---|---|---|---|
| R-01 | Main domain overview says Fact is a qualified interpretation of Claim, while I-04 and B ADR-001 preserve Fact/Claim distinction and block representation decision | B proposes domain semantics; Architecture Governance approves ADR; D owns canonical persistence mechanics | OPEN / ADR-BLOCKED | Correct overview wording or explicitly mark it non-normative pending ADR; do not choose an option in this report |
| R-02 | Stable Claim identity across Memory Versions was previously phrased as decided in a superseded path | B ADR / D canonical identity contract; implementation PR #194 explicitly preserves this as OPEN | OPEN | Keep Claim identity cross-version unresolved; do not infer stable ID from Phase 1 Claim proposition semantics |
| R-03 | A technology recommendation could be mistaken for stack/deployment selection | A recommends; Storage chooses/validates physical transaction realization; I owns security; D/E/G/H own their semantics | CANDIDATE | Keep all stacks and topology options non-approved; validate through measured workload and physical integration evidence |
| R-04 | A historical shorthand that Storage topology is wholly undecided is stale | Storage ADR selected Option A for L1 logical serialization only; L4 engine/deployment remains open | DECIDED L1 selection evidence; OPEN L4 | Carry both levels separately; do not call it either “no topology selected” or “Storage solved” |
| R-05 | Provider response / HTTP success / tool success can be misread as Brain commit or user outcome | C owns Provider/Tool evidence; D/Storage own canonical commit; G owns Applied | DECIDED semantic separation | Preserve explicit outcome stages and reconciliation; verify with real provider and tool adapters |
| R-06 | Transport ACK or materialization can be misread as Applied | H owns transport; C final request evidence; G Applied decision; I/D currentness | DECIDED authority split; CANDIDATE acceptance contract | Full Applied only after G accepts exact final-request evidence under current identity/permission/fence predicates |
| R-07 | Scope identity can be treated as permission or payload identity as authenticated Principal | B defines ScopeRef/typed refs; I owns authz/trust; H binds authenticated sender; C consumes protected identity | DECIDED distinction; OPEN joint trust binding | Fail closed; require shared typed binding and negative tests |
| R-08 | A/B/C research/review snapshots contain stale main/owner baselines and review status overclaims | A maintains integration evidence; each source Owner maintains source; reviewer records exact target Blob/Head | OPEN currentness | Re-read exact sources on each gate; distinguish historical report, current source and approval state |
| R-09 | B's bilingual audit has internal status/pin inconsistencies | B owns source remediation; A can record evidence only | OPEN / B5 BLOCKED | Do not claim B5 passed; reconcile controlling Blob manifest and section status before B package acceptance |
| R-10 | C review's delegated technical review could be mistaken for human independent approval | C owns integration semantics; human/independent reviewer owns review provenance | OPEN | Keep human independent review pending; no cross-owner freeze inferred |

## 6. Architecture invariant delta table

| Invariant | Mainline baseline | A/B/C integration finding | Status |
|---|---|---|---|
| I-04 Event, Memory, Fact, Entity, Relation and Evidence are distinct domain concepts | Normative invariant | Current overview's Fact-as-qualified-Claim wording is inconsistent; ADR-001 is blocked | OPEN — normative conflict requires governance decision |
| I-05 Derived Memory retains provenance | Normative invariant | B model and C boundary preserve lineage; exact provenance granularity remains owner-dependent | DECIDED principle; TO_VALIDATE completeness |
| I-06 Intent/plan/prediction/pending action are not completed outcomes | Normative invariant | C separates intent, provider handoff, tool side effect and Brain outcome | DECIDED semantic rule; TO_VALIDATE adapter behavior |
| I-07/I-08 Context edits/removal do not mutate/delete canonical Memory | Normative invariants | B separates ContextEntry; G owns context; D owns canonical lifecycle/Forget | DECIDED |
| I-10 Context delivery Applied only after explicit Adapter acknowledgement | Normative invariant | ACK is necessary protocol evidence but insufficient alone; G must validate C final-submit evidence plus H/I/D bindings | CANDIDATE refinement; governance wording reconciliation OPEN |
| I-12 Memory content is untrusted data | Normative invariant | C preserves untrusted-memory and prompt-injection boundary | DECIDED requirement; adversarial runtime execution TO_VALIDATE |
| I-13 Scope and Permission are independently enforced | Normative invariant | B defines namespace/ref; I owns authorization; H authenticates transport; C consumes bound identity | DECIDED separation; joint enforcement TO_VALIDATE |
| I-14 Conflicting claims retain provenance and resolution history | Normative invariant | B model preserves conflict; Claim identity and Fact adjudication remain open | DECIDED preservation rule; TO_VALIDATE implementation |
| I-16 State-changing retries are idempotent in declared scope | Normative invariant | C distinguishes request/attempt/idempotency; E/Storage define accepted receipts; RFC-IDE-001 separate proposal | DECIDED principle; cross-domain exact tuple adoption OPEN |
| I-18 Adapter ACK proves protocol application, not model comprehension | Normative invariant | C/G/H stages additionally distinguish Delivered, Materialized, Submitted, Applied and ExecutionStarted | DECIDED |
| I-22 Performance claims require reproducible measurement | Normative invariant | A workload envelopes are assumptions; no complete representative Brain benchmark | TO_VALIDATE |
| I-23/I-24 Bilingual architecture change and parity requirements | Normative invariants | A/B/C packages are bilingual in intent; B5 audit still records internal status/pin inconsistency | OPEN for B5 acceptance; every new change must pass GOV-DOC-001 |

### Invariant interpretation note

This report does not amend I-10 or any other invariant. It identifies a potential semantic refinement: Adapter acknowledgement cannot alone establish Applied if the system also requires proof of actual final request submission and G acceptance. The invariant owner/governance process must decide whether to amend the wording or clarify the evidence hierarchy in a subordinate contract.

## 7. DECIDED / CANDIDATE / OPEN / TO_VALIDATE register

### DECIDED — bounded, source-backed

- Phase 1 minimal domain scope is bounded by the current Phase 1 freeze document; global unresolved decisions remain explicitly open.
- Event, Memory, MemoryVersion, Claim proposition, Evidence and Provenance are distinct concepts; Event acceptance is not truth.
- MemoryVersion is immutable; successor writes require expected-parent/CAS or equivalent concurrency control.
- Scope is not Permission; typed reference is not authorization.
- Agent, Model, Provider, Tool and Brain are distinct roles; Provider acceptance and Tool success do not establish canonical Memory success.
- G owns Applied state; C owns actual final-request evidence; H owns wire/transport; I owns authorization; D owns Forget fence semantics.
- No ACK, digest, local render or model output alone proves Full Applied or model comprehension.

### CANDIDATE — plausible, not approved/frozen

- Local-first modular monolith as initial implementation shape.
- SQLite WAL as a local/same-host single-writer substrate where workload and transaction constraints fit.
- Storage Option A as the L1 logical serialization direction only; it is not an L4 physical database/deployment choice.
- A's minimum/balanced/high-scale stacks.
- C/H Applied Delivery Evidence 1.0.0 identity shape and related candidate schema.
- Shared B/I/H typed identity binding pending accountable approval.

### OPEN — decision or owner acceptance missing

- Fact/Claim conceptual representation and whether Fact is a separate attestation object.
- Claim identity across Memory Versions.
- Current overview / I-04 wording conflict.
- B5 independent clause-by-clause bilingual parity acceptance and controlling source manifest consistency.
- Joint C/H COutcomeRecord and final-request-boundary mapping.
- G Applied contract freeze and durable Applied persistence/recovery.
- I governance approvals, production trust/issuer/key registration and cross-owner authorization adoption.
- D/E/I/Storage publication/Forget atomicity, physical visibility and global completion.
- Production database, deployment topology, HA, DR, backup/restore and operational ownership.

### TO_VALIDATE — evidence required

- Cross-owner provider handoff and ambiguous retry/reconciliation against real provider adapters.
- Tool side-effect idempotency, authorization, cancellation and compensation behavior.
- Exact C/H schema validator consuming real CSubmitOutcome 1.0.1 records, not all-success callbacks.
- G durable Applied persistence, idempotency, crash/restart and restore.
- Permission revocation / Forget fence races at actual final-request submission boundary.
- End-to-end no-resurrection across D/E/F/G/H/I/Storage.
- Security adversarial suite, redaction and telemetry-retention behavior.
- Representative workload and performance benchmarks on declared hardware/data.
- Multi-process/multi-host linearizability, power-loss and production DR where claimed.

## 8. Superseded / stale statements to correct

1. **Do not use** A's 2026-11-16 branch manifest as a live 2026-11-18 HEAD inventory. Its branch values are historical. Use its exact artifact Blob pins only for the bytes it identifies.
2. **Do not use** A research README's historical main baseline `b372b62...` as current main. It is the research package's pinned creation baseline.
3. **Do not use** B research README's embedded `901e38...` main observation as current. B5 recheck is a later review snapshot but itself records historical main `e52594...`; this report's current main is `6b5db291...`.
4. **Do not infer** that PR #55 merge (if observed in later history) approved B5, Fact/Claim Option A, Claim identity, or any schema. Its recorded reviews were COMMENTED, not APPROVED; B5 remains blocked.
5. **Do not describe** Storage Option A as “no logical topology selected”; L1 was selected. **Do not describe** it as a complete physical deployment solution; L4 remains open.
6. **Do not infer** C/H candidate CI proves live provider trust, production signature validation, durable replay, G Applied persistence or end-to-end integration.
7. **Do not infer** A/B/C review documents represent human independent Owner approvals. Their provenance limitations are explicit.

## 9. Evidence and non-claims

- Current main baseline is the observed commit stated in §3.
- Source Blob SHAs in §2 identify exact fetched file bytes.
- A/B/C review verdicts are recorded as their authors' stated review dispositions, with their independence limitations.
- Historical CI IDs quoted in C review material are bounded evidence for those exact candidate commits only; they are not this report's CI evidence and do not transfer to a new Head.
- This report does not claim new code/test execution, production behavior, owner approval, issue closure, architecture freeze, technology selection, schema freeze or production readiness.

## 10. Required next closure sequence

1. B resolves the Fact/Claim ADR and Claim identity question through the designated governance/Owner process; correct the main overview only through an authorized bilingual change.
2. B closes B5 with an exact, self-consistent Blob manifest and independent clause-by-clause bilingual semantic review.
3. C/H complete exact immutable COutcomeRecord ↔ H evidence mapping and validator tests with real cross-schema fixtures; keep G as sole Applied authority.
4. G/I/D/H/C agree on one exact Applied contract version, authority bindings, currentness predicates and recovery semantics.
5. D/E/I/Storage complete publication/Forget logical and physical proof without conflating their decision rights.
6. A refreshes integration registry only after exact source readback; do not use this report to close Issue #43 or replace its dedicated owner work.
7. Run reproducible end-to-end, security, race, recovery and workload tests; record exact source commit, CI run, environment and limitations.

## 11. Change control

This is an additive integration review artifact. It does not modify A/B/C source contracts, architecture invariants, Issue #43, implementation code, PR #244/#249, Event Store work, RFC-IDE-001, PR governance or merge-evidence work. Any normative correction must be made by the accountable Owner in a separate bilingual change with its own review and exact-head evidence.

**Disposition: CANDIDATE — partial integration review complete; architecture freeze NOT READY.**


## 12. Commit-bound CI evidence for bounded DECIDED statements

The DECIDED labels above refer to bounded semantic/source-owner decisions, not a new cross-owner freeze. The following exact-head runs are the only CI evidence relied on for related executable behavior:

| Bounded claim | Exact commit / tested source | CI Run ID | Result | Evidence ceiling |
|---|---|---:|---|---|
| Phase 1 domain + SQLite adapter regression surface | PR #249 Head `7411ec57ef87f995cd7be14cc3ccd44620a8e0f8` | `44276433236` | SUCCESS; workspace 55 passed, 0 failed; domain target 12 passed; SQLite adapter 26 passed | Supports the tested Phase 1 domain/adapter behavior only; PR remains a candidate pending independent review and does not prove global Fact/Claim, production, multi-process or power-loss semantics |
| C Provider Outcome reference behavior | C restored Owner source `88992da30331121b81cf2773acab11d921daf281` | `44129914790` | SUCCESS; 19 tests, 0 failures | C reference/provider-outcome suite only; not C end-to-end Brain integration, live provider truth, production trust or cross-owner acceptance |
| H Applied Delivery Evidence 1.0.0 candidate validator | H tested code commit `4e65a2` (review record abbreviates this SHA) | `44130722532` | SUCCESS; 11 tests, 0 failures | H candidate schema/validator only; not exact COutcomeRecord integration, G durable Applied, production crypto or wire freeze |

The two C/H run IDs above are reproduced from the C-REVIEW-001 addendum Blob `3300d95b3074a7bf6690718e0ab7f6cbd9afb9ae`; they are not this report's CI and do not transfer to a changed commit. The exact full H commit SHA is not present in the inspected review artifact; the abbreviated `4e65a2...` is deliberately not expanded or guessed.

GitHub Actions lookup for the report PR's final readback commit returned no PR-triggered workflow runs; combined status returned no status contexts. Therefore this report's documentation CI is **NOT RUN / NO RUN ID OBSERVED**. Do not treat the PR as CI-passing. Exact final PR Head and final report Blob SHAs are recorded in the PR description after the last readback.
