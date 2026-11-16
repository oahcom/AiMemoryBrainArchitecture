# Phase 3.5 Cross-Module Contract Registry

- Owner: Session A / Principal Integration Architect
- Status: **CANDIDATE coordination register; no Contract Freeze or implementation approval**
- Updated: 2026-11-16
- Source of truth: live GitHub branch refs queried for this review; see §2.
- Authority rule: this registry records owner decisions and compatibility evidence. It does not create, approve or override domain contracts.

## 1. Evidence and status vocabulary

The following are independent evidence dimensions:

| Dimension | Meaning | Does not establish |
|---|---|---|
| Artifact Exists | Exact file is present and readable at the cited branch/HEAD | Owner approval or implementation |
| Owner Decision | The accountable owner explicitly labels a semantic decision DECIDED in an owned artifact | Cross-module acceptance or runtime behavior |
| Cross-module Agreement | Every affected authority owner/consumer has reconciled the same contract and accepted its boundary | Persistence correctness or test pass |
| Implementation Evidence | Executable implementation, durable behavior and reproducible tests support the claim | Production approval unless its governance gate is also met |

Statuses: DECIDED, CANDIDATE, ADR-BLOCKED, OPEN, TO_VALIDATE, NOT RUN. A candidate is not approved. A document's own status is not upgraded by its presence in this registry.

## 2. Live Branch / HEAD / Artifact Registry

All ten refs below were freshly queried through GitHub branch endpoints on 2026-11-16. HEAD values are full 40-character SHAs. Commit evidence links identify the exact current tip commit; the commit message and changed-file list are recorded as the latest change evidence. The GitHub author is the repository account `oahcom`; individual human-owner identity is not independently attested by that metadata.

| Module | Branch | Live HEAD | Owner / authority | Key artifacts inspected at this HEAD | Latest change / commit evidence | Review status |
|---|---|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `f18c64950a84385bd407752c7188e1bd52029a7b` | Session A; Contract Registry, cross-module coordination, Typed Cursor Registry, findings/status | `reviews/integration/contract-registry.md`; `typed-cursor-and-watermark-contract.md`; Phase 2 reconciliation; Phase 3 remediation task pack; A targeted remediation record | `docs(integration): finalize A readback evidence`; changed A targeted remediation record. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/f18c64950a84385bd407752c7188e1bd52029a7b) | Registry source baseline now re-queried; current update is coordination only |
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` | Session B; typed domain references and Fact/Claim model proposal | `typed-reference-registry.md`; `principal-actor-binding-mapping.md`; `ADR-001-fact-claim-semantics.md`; scope/permission model | `docs(domain): clarify typed ScopeRef and cross-environment semantics`; changed scope/permission model. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/66adf6bdcf5ec69a146fe75afe20ce3b85af8448) | Typed reference semantics are owner-authored; joint B/I/H approval remains OPEN; ADR-001 ADR-BLOCKED |
| C | `session-c-agent-integration-2026-11-16` | `a585307222b0169c007915c25ff8ed0da517f3e4` | Session C; telemetry semantics, Agent trust boundary, final-request Applied predicates, untrusted-memory boundary | `phase-3.5-agent-identity-applied-attestation-untrusted-memory.md`; `telemetry-event-and-identity-contract.md`; `security-and-untrusted-memory-boundary.md`; final inference boundary attestation | `docs(agent-integration): reprocess phase 3.5 identity and applied conformance`; four C artifacts changed. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/a585307222b0169c007915c25ff8ed0da517f3e4) | C semantic requirements DECIDED within C; B/I/H/G dependencies and runtime conformance OPEN |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | Session D; canonical Memory, ForgetOperation/Fence, producer barrier and canonical cursor semantics | `forget-fence-and-completion-contract.md`; `forget-fence-operation-and-publication-gate.md`; `commit-cursor-semantics.md`; canonical store/version/lifecycle docs | `docs(memory-brain): record Phase 3.5 forget atomicity decisions`; changed D decision/change log. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/da8e5882d0b238d765d00b2225b79eea45a483b1) | D semantic decisions DECIDED; D/E callable interface and Storage realization/conformance OPEN |
| E | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` | Session E; ingress, compiler work lifecycle, derivative lineage and publication enforcement | `forget-fence-and-derived-registration.md`; `compiler-state-and-producer-admission.md`; accepted receipt/idempotency contract; E decision/change log | `docs(E): record Phase 3.5 reprocessing evidence`; changed E decision/change log. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/c2f14408ba62447c11172d65b93a279fef96d175) | E consumes D semantics; E still labels D/E/Storage atomic boundary OPEN / blocking |
| F | `session-f-memory-runtime` | `f86f9b536ea69d8e0fbb4bf290c7023ef0eada76` | Session F; retrieval, candidate generation, index/cache/Working Set and runtime suppression | `phase-3.5-forget-suppression-and-cursor-consumption.md`; runtime/index/cache docs; reprocessing change log | `docs(runtime): record current Phase 3.5 re-review findings`; changed F reprocessing change log. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/f86f9b536ea69d8e0fbb4bf290c7023ef0eada76) | F runtime safety semantics DECIDED; API realization, backend behavior and conformance TO_VALIDATE/OPEN |
| G | `session-g-memory-context` | `20bf3125cfaf0d0a695a11bc8e8d7dcf5b8f4373` | Session G; Context membership/order/budget/version/change sets/reconciliation/delivery intent | `context-reconciliation.md`; `context-versioning.md`; Context manager/edit/budget docs; G review | `docs(memory-context): align Session G with Phase 3.5 contracts`; seven G artifacts changed. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/20bf3125cfaf0d0a695a11bc8e8d7dcf5b8f4373) | G safety ordering DECIDED; workflow implementation CANDIDATE; cross-owner Applied mapping and execution tests OPEN |
| H | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` | Session H; BMCP wire, protocol/Adapter capability, delivery ACK and reconnect | `phase-3-5-identity-applied-ack-reconnect-contract.md`; envelope/versioning; delivery/ACK; capability/applied attestation; Forget/reconnect; protocol conformance matrix | `docs(h): correct Phase 3.5 source review and evidence log`; changed H Forget ACK remediation change log. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/1ee65928f123d92a4758b0de09bc8d6df1e46253) | H wire/evidence package CANDIDATE; no cross-module approval or runtime conformance |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | Session I; identity/authorization policy, global producer/recipient inventory, global Forget and security governance | `phase-3.5-global-identity-forget-governance.md`; Principal/Actor authorization; global target inventory; threat model; governance decision register; retention/erasure policy | `docs(security): register Applied attestation governance decision`; changed governance decision register. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/5591ad3620ec3f5d74194bd79556dcf3e25bea07) | I governance remains CANDIDATE; all listed governance decisions Proposed, no effective approval |
| Storage/Consistency | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` | Storage/Consistency role; physical transaction, persistence, visibility and recovery realization. Individual accountable engineering approver not recorded. | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` | `docs(storage): rebase Forget atomicity review on Phase 3.5 D E I contracts`; changed Storage realization review. [Commit](https://github.com/oahcom/AiMemoryBrainArchitecture/commit/3a14550648f21c0bc2725dac38b29e099c2f3196) | Proposed design only; NOT IMPLEMENTED / NOT VERIFIED; no Storage authority package on main |

**Freshness caveat:** owner artifacts contain embedded “reviewed HEAD” values that are older than some live refs. The live branch endpoint values above take precedence for this review. In particular, H's Phase 3.5 document cites older C/G/H reprocessing baselines; C's own Phase 3.5 document and other historical review tables also cite older HEADs. This is recorded as source-baseline drift, not silently accepted as current cross-module review evidence.

## 3. Typed contract status and cross-module findings

| ID | Contract / finding | Owner(s) | Current status | Evidence / closure condition |
|---|---|---|---|---|
| CR-P1-01 / INT-P0-03 | D/E producer admission, fence installation, high-water, dependency registration, publish gate, recovery and late derivative suppression | D semantics; E enforcement; Storage realization; I global proof | **OPEN / P0 BLOCKER** | D operation semantics exist; E consumes them but still marks D/E/Storage atomic boundary OPEN; Storage is proposed design only and says NOT IMPLEMENTED / NOT VERIFIED. Require named physical transaction/coordinator, deployed persistence semantics, fault/race evidence and I target closure. |
| CR-P1-02 / INT-X-01 | CanonicalCommitCursor semantics and typed consumer alignment | D owns CanonicalCommitCursor; A coordinates; E/F/G/Storage consume; H opaque transport | D decision **DECIDED**; integration **OPEN** | D selected one globally ordered sequence per Canonical Memory authority; A proposal now reflects it. E consumes it. F defines IndexWatermark. Need current G/H/I consumer source-baseline agreement and Storage sequence/recovery proof. |
| CR-P1-03 | Registry freshness and artifact/branch inventory | A | Re-queried for this review | Live refs and package paths recorded in §2; refresh on every closure review. |
| CR-P1-04 | E source-baseline/change-log supersession | E | **OPEN / E-owned** | E decision log at live HEAD must clearly supersede historical stale review statements and record latest C/G/H/I refs; A does not edit E. |
| CR-P1-05 | I global Forget vector, inventory seal and D/E/F/G/H target evidence mapping | I policy; all module owners supply local evidence | **CANDIDATE / OPEN** | I distinguishes global ProducerDomainInventoryEpoch from D per-Forget work barrier and maps H ACK classes to target/action evidence. Governance decision register remains Proposed; owner mapping and target closure not approved or executed. |
| INT-P0-01 | Fact/Claim canonical semantics | B + Architecture Governance | **ADR-BLOCKED** | B ADR records no named decision authority/approver, no approved option, no timestamp/approval artifact, no effective version. |
| INT-P0-02 / INT-X-03 | Principal, Issuer, ActorRef, ScopeRef, ProducerIdentity, Agent/Adapter binding, Environment, delegation and PermissionEpoch | I policy; B refs; H transport; C consumer; D/E/F/G boundaries | **OPEN / P0 BLOCKER** | B typed refs, I policy and H wire mapping are candidate/joint approval pending. Payload identity is correctly treated as claim only; no signed cross-owner decision or negative-test results. |
| INT-P0-04 | Prompt injection / untrusted memory | C requirements; I threat/risk governance; H enforcement; E/G provenance | **OPEN** | C/I requirements and adversarial matrix exist. I residual-risk acceptance authority is not recorded; test specification is not execution. |
| INT-P1-01 / INT-X-04 | ContextVersion, ChangeSet, delivery and Applied | G state; H evidence/wire; C final boundary; I/D freshness | **CANDIDATE / OPEN** | State stages and exact proof tuple align in documents; H/G/C/I cross-approval and final-boundary/reconnect/late-ACK tests absent. |
| INT-P1-04 / INT-X-06 | Accepted receipt, idempotency, retry/replay/retention | E; H/I/Storage dependencies | **CANDIDATE / OPEN** | E semantics described; identity namespace, storage durability and crash/replay evidence not approved or verified. |
| INT-X-07 | Shared conformance/fault-injection suite | A coordinates; test owner not designated | **TO_VALIDATE / NOT RUN** | Test plans exist; no test IDs/results/logs or reproducible execution evidence supplied. |
| INT-X-08 | Workload/performance budgets | Engineering owner TBD | **OPEN / NOT RUN** | No reproducible workload/hardware benchmarks supplied. |

## 4. Authority and approval guardrails

- D owns CanonicalCommitCursor, ForgetOperation/Fence and per-operation producer work barrier semantics.
- E owns compiler work lifecycle, retries, DLQ/replay and derivative enforcement.
- F owns IndexWatermark and runtime/index/cache behavior.
- G owns ContextVersion, ChangeSet, delivery intent and reconciliation.
- H owns wire representation, Adapter capability/ACK and reconnect.
- I owns Principal trust, authorization, PermissionEpoch, ProducerDomainInventoryEpoch, global target inventory, global completion and physical-erasure policy.
- B owns ActorRef/ScopeRef/typed-reference semantics and Fact/Claim domain recommendation; ADR-001 requires Architecture Governance approval.
- C owns Agent telemetry, trust labels, final-request Applied meaning and managed-region security requirements.
- Storage owns physical persistence/transaction/recovery realization only; accountable engineering decision-maker remains unrecorded.
- A coordinates and records; A does not approve any of these domain decisions.

## 5. Closure rule

No finding is closed by this registry update. Closure requires an exact owner artifact and full live HEAD, explicit owner decision where applicable, cross-module sign-off by every affected owner, and (for implementation/conformance claims) reproducible execution evidence. A later commit invalidates source freshness and requires re-query. No branch is merged by this registry.
