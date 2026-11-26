---
document_metadata:
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-193/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: DECIDED quality priorities and measurement principles). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: 4350733173d29451a8ea4aa6a544de46526b4fd7."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: "docs/en/01-system-architecture/system-quality-attributes.md"
    zh-CN: "docs/zh-CN/01-system-architecture/system-quality-attributes.md"
---
# System Quality Attributes

**Status:** DECIDED quality priorities and measurement principles; CANDIDATE architectural tactics; TO_VALIDATE quantitative targets.  
**Scope:** System-level quality model and verification plan. This document does not claim unmeasured performance or prescribe a deployment topology.

## 1. Quality model

The system must be evaluated as a memory infrastructure in real Agent workflows, not merely as a vector-search benchmark. Quality attributes interact: stronger provenance and authorization may add latency; aggressive caching may reduce latency but increase staleness risk; larger context may improve coverage but consume tokens and distract the Agent.

Priority attributes:
1. Correctness and epistemic integrity.
2. Scope isolation, authorization, and privacy.
3. Canonical/context consistency and recoverability.
4. Provenance integrity and governed forgetting.
5. Predictable latency and bounded resource use.
6. Adapter interoperability and evolvability.
7. Availability and fault containment.
8. Useful memory activation and measurable Agent-level benefit.
9. Operability, observability, and testability.

## 2. Quality attribute scenarios

| Attribute | Stimulus | Required response | Measurement / evidence |
|---|---|---|---|
| Semantic correctness | Agent submits plan, prediction, observation, or outcome | Preserve epistemic distinction; plan alone never becomes completed fact | Adversarial and property-based domain tests; false-outcome rate |
| Provenance integrity | Compiler derives or compacts memory | Every derived claim remains traceable to source evidence or explicit provenance gap | Provenance coverage; lineage traversal tests |
| Isolation | Principal queries another user/Agent/environment scope | Deny before protected data affects results or context | Cross-tenant/Agent/environment penetration tests |
| Context consistency | Concurrent edits or lost delta | One authoritative sequence; reject/reconcile stale base; snapshot repairs gaps | Version invariant tests; reconciliation success |
| Applied correctness | Adapter receives context change while inference is in flight | Apply only at subsequent assembly boundary; acknowledge exact version | Instrumented Adapter boundary test |
| Forgetting | Authorized Forget targets canonical memory and derivatives | Access suppression and staged cleanup; no premature completion claim | Time-to-suppression, derivative coverage, backup policy audit |
| Ingestion durability | Storage/Compiler/model outage during Event submission | Accepted means durable; accepted Event survives downstream outage | Crash injection and replay |
| Recall responsiveness | Agent issues bounded Recall under load | Return authorized candidates or explicit timeout/partial result within declared budget | p50/p95/p99 latency, timeout and partial rates |
| Resource boundedness | Large corpus or burst telemetry | Enforce admission, candidate, graph-depth, cache, and queue limits | CPU/RAM/VRAM/disk, queue depth, overload tests |
| Interoperability | New Agent/LLM implementation connects | Stable Brain contract works through Adapter capability tier | Conformance suite across independent Adapters |
| Evolvability | Protocol/schema adds optional capability | Version negotiation and backward-compatible behavior or explicit rejection | Compatibility matrix tests |
| Availability | One logical subsystem is unavailable | Failure is contained; unrelated durable data and authority remain intact | Fault-injection and dependency-isolation tests |
| Utility | Memory activation changes Agent task performance | Improvement or regression is measured against baseline, not assumed | Controlled Agent-task evaluation |

## 3. System quality budgets

Numerical budgets remain **OPEN** until workload and hardware baselines are fixed. The following are required budget dimensions, not target values.

| Dimension | Metric | Segmentation |
|---|---|---|
| Ingestion | Acceptance latency, durable commit latency, rejection/backpressure rate | payload size, source, concurrent writers |
| Compilation | Queue age, stage duration, retry count, time-to-canonical | deterministic vs model-assisted stages; model availability |
| Recall | End-to-end and per-stage latency, timeout/partial rate, candidate count | warm/cold cache, corpus size, query type, scope cardinality |
| Activation | Telemetry-to-decision latency, false activation, missed relevant memory | task class, risk class, Adapter tier |
| Context | Planning/edit/commit latency, version conflict rate, token/byte budget utilization | context size, edit type, concurrent sessions |
| Synchronization | delivery latency, Applied lag, retry count, snapshot frequency, version-gap rate | online/offline Adapter, delta size, network condition |
| Governance | authorization latency, Forget time-to-suppression, policy-completion time | derivative count, backup policy, scope size |
| Resources | CPU, RAM, disk IO/capacity, GPU/VRAM, network | local hardware profile, concurrency, model enabled/disabled |
| Quality | precision/recall of useful memory, unsupported-claim rate, provenance coverage, conflict preservation | labeled workload and evaluation set |
| Agent outcome | task success, tool/action error, recovery time, repeated-question rate, context token overhead | task/environment/Agent/LLM cohorts |

## 4. Performance and evaluation methodology

### 4.1 Reproducible benchmark declaration

Every result must include:
- hardware: CPU, physical memory, GPU model/VRAM, storage type, OS/runtime;
- software revision, configuration, model and quantization if used;
- corpus size, Event/Memory/Claim/Entity counts, average and tail payload sizes;
- scope distribution, number of Agent instances and concurrent sessions;
- query mix: structured, lexical, semantic, temporal, relational, hybrid;
- cache state and warm-up protocol;
- concurrency, arrival rate, burst profile, duration;
- correctness dataset and ground-truth labeling method;
- percentile calculation, sample count, confidence interval where applicable.

No multiplier or performance advantage is accepted without a reproducible comparison using the same workload and correctness criteria.

### 4.2 Required baselines

Compare:
1. No memory / Agent-native baseline.
2. Simple retrieval baseline (e.g. lexical or embedding-only) where relevant.
3. Brain retrieval without activation.
4. Brain retrieval plus activation/context management.
5. Brain with model-assisted compilation versus deterministic-only pipeline.

These are evaluation baselines, not technology commitments. Comparisons must account for added prompt tokens, retrieval latency, and false activations.

### 4.3 Quality metrics

Suggested definitions:
- **Useful-memory precision:** relevant activated entries / all activated entries, under a labeled task-context judgment.
- **Useful-memory recall:** relevant activated entries / all judged-relevant eligible entries.
- **Unsupported-claim rate:** activated claims lacking required evidence/provenance or exceeding source epistemic status.
- **Scope leakage rate:** protected records disclosed outside authorized scope; target is zero in security tests.
- **Version correctness:** fraction of acknowledgements matching the exact intended context and version; invalid Applied claims target zero.
- **Staleness exposure:** served candidate whose source generation is older than the required consistency fence.
- **Forget suppression latency:** time from durable Forget fence to denial of reads/activation for target data.
- **Agent-level utility:** paired task success and error metrics against declared baseline, with confidence intervals and task stratification.

Evaluation labels and adjudication procedure are **OPEN** and must be defined before interpreting quality scores.

## 5. Availability and fault isolation

**DECIDED:** Logical component failures must not silently corrupt another component's authoritative state.

Required behavior:
- Event acceptance remains independent of model inference availability.
- Compiler backlog is durable and bounded; overload applies admission control.
- Canonical Store failure prevents canonical writes from claiming success.
- Index/cache failure causes detectable degradation or safe fallback; secondary structures are rebuildable.
- Retrieval timeout does not mutate context.
- MCM failure preserves last committed Context version.
- Sync/Adapter outage delays application without changing Applied state.
- Forget has a durable job/fence and resumable per-target progress.
- Governance authorization failure fails closed for protected reads/writes.
- Observability loss must not violate mandatory audit obligations; exact fail-open/fail-closed classes remain OPEN.

Availability SLOs and recovery objectives (RTO/RPO) require workload and deployment assumptions; do not invent values at architecture stage.

## 6. Security and privacy quality

Required controls:
- Authenticate source principal and Adapter.
- Authorize every operation using Permission independently of Scope.
- Enforce tenant/user/Agent/session/environment partitioning at query and mutation boundaries.
- Treat source text, telemetry, observations, and retrieved memories as untrusted data.
- Keep memory region delimited and subordinate to System/Developer instructions, user input, and Agent safety policy.
- Minimize telemetry collection; full hidden CoT is not required.
- Redact sensitive payloads from logs and metrics.
- Propagate Forget to canonical data and applicable derivatives under declared policy.
- Audit administrative and high-impact operations without retaining erased content unnecessarily.

Verification includes threat modeling, negative authorization tests, prompt-injection fixtures, data-flow review, retention/erasure audits, and secret/log scanning.

## 7. Interoperability and evolvability

**DECIDED:** Brain contracts are Agent- and model-independent; integration variance belongs in Adapter mappings and capability negotiation.

Test:
- one Tier 1 inference-boundary Adapter;
- one Tier 2 middleware Adapter;
- one Tier 3 event/Recall integration;
- multiple LLM providers behind at least one Adapter where feasible;
- unknown optional fields, unsupported operations, version mismatch, and downgrade paths.

An Adapter must declare limitations; Brain must not imply guarantees beyond that tier. Exact tier definitions belong to Agent Integration/BMCP specifications.

## 8. Resource efficiency and local-first operation

Measure CPU, RAM, disk IO, storage growth, GPU/VRAM, and network independently. The local target hardware profile must be declared per experiment; optional model-assisted processing must be isolated from deterministic ingestion and retrieval paths.

**CANDIDATE:** Resource budgets enforced at admission, compilation scheduling, retrieval candidate expansion, context token/byte planning, and cache sizing.

**TO_VALIDATE:** Feasibility and throughput of model-assisted compilation on target 12–16 GB VRAM systems; no claim is made before benchmark.

## 9. Observability requirements

Every cross-component operation should be traceable through correlation/causation IDs and expose:
- request/event/context/delivery identifiers (appropriately redacted);
- component and stage, outcome/error class, attempt count;
- queue age and stage duration;
- canonical/index generation and Context base/target/applied versions;
- scope class without leaking sensitive identifiers;
- resource usage and saturation;
- policy decision and denial reason code where safe.

Logs, metrics, and traces are not substitutes for domain Evidence or Provenance.

## 10. Verification strategy

| Test level | Focus | Example |
|---|---|---|
| Contract | Schema, status, ownership, compatibility | Adapter conformance and invalid payload rejection |
| Invariant/property | Non-negotiable semantics | No Applied without ack; no plan-to-outcome promotion |
| Integration | Cross-component sequencing | Event accepted → compiled → canonical → indexed |
| Concurrency | Race and version safety | Concurrent canonical/context edits |
| Fault injection | Recovery and isolation | Kill compiler/index/sync at each commit boundary |
| Security | Isolation, auth, injection | Cross-scope recall and malicious memory payload |
| Performance | Latency, throughput, resource bounds | Mixed workload p50/p95/p99 |
| Agent task | End-to-end utility | Multi-session task with and without memory |
| Governance | Forget/retention | Derivative cleanup and backup expiration |

## 11. Acceptance criteria

1. All quality scenarios above have executable tests or a documented manual verification procedure.
2. No cross-scope disclosure in the defined adversarial test suite.
3. No false Accepted receipt before durable Event commit.
4. No unsupported claim promotion in labeled plan/outcome fixtures.
5. No invalid Applied acknowledgement in Adapter conformance tests.
6. No silent Context version gap advancement.
7. Canonical state remains correct after index/cache loss and rebuild.
8. Forget never reports policy completion before required targets complete or are explicitly recorded as policy-exempt residuals.
9. All reported performance numbers include the benchmark declaration in §4.1.
10. Agent-level utility reports include baseline, task stratification, token overhead, and uncertainty.
11. Resource overload produces bounded behavior and explicit backpressure/degradation.
12. Protocol evolution tests verify supported and unsupported capability paths.

## 12. Open questions and validation backlog

| ID | Status | Priority | Question |
|---|---|---:|---|
| QA-01 | OPEN | High | Define representative Agent workloads and benchmark corpus. |
| QA-02 | TO_VALIDATE | High | Establish p50/p95/p99 targets for Recall and Context application on declared hardware. |
| QA-03 | OPEN | High | Define RTO/RPO and audit availability requirements for intended deployment modes. |
| QA-04 | TO_VALIDATE | High | Measure useful-memory precision/recall and Agent-level utility versus simple retrieval baselines. |
| QA-05 | TO_VALIDATE | Medium | Determine resource envelope for model-assisted compilation on local GPU profiles. |
| QA-06 | OPEN | Medium | Define evaluation label adjudication and confidence interval methodology. |
| QA-07 | OPEN | Medium | Define Forget completion and backup/replica residual reporting. |
| QA-08 | OPEN | Medium | Define Adapter tier conformance coverage and compatibility support window. |

## 13. Decision summary

- **DECIDED:** Correctness, provenance, isolation, context consistency, governed forgetting, and measurable Agent utility are first-class quality attributes.
- **DECIDED:** Performance claims require reproducible workloads and hardware declarations; no multiplier is assumed.
- **DECIDED:** Failure isolation preserves canonical authority and explicit degraded states.
- **CANDIDATE:** Enforce budgets at ingress, compiler, retrieval, context, and cache boundaries.
- **TO_VALIDATE:** Numerical latency/throughput/resource targets, model-assisted compilation feasibility, and Agent-level benefit.
- **OPEN:** Workload corpus, SLO/RTO/RPO, evaluation labels, and backup erasure semantics.
