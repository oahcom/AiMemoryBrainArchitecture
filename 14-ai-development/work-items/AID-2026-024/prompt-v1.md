# WORK ITEM: PROPOSED AID-2026-024
# Minimum Executable Brain Evaluation Runtime
# Cross-Requirement Architecture Design

## 1. IDENTITY AND ROLE

You are an Architecture Designer and Technology Researcher.

Primary requirement:
REQ-06 — Issue #346
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/346

Joint requirement:
REQ-10 — Issue #350
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/350

Coordination hub:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/345

Proposed Work Item ID: AID-2026-024.

Formal allocation must be verified before use.

## 2. OBJECTIVE

Design the smallest executable integration path that allows a reproducible evaluation of:

Arm A: No memory.

Arm B: Simple retrieval memory.

Arm C: Complete AI Memory Brain chain.

The same integration path must support reproducible end-to-end performance and cost measurements.

This work does not authorize implementation.

## 3. BASELINE

Repository:
https://github.com/oahcom/AiMemoryBrainArchitecture

Last verified main:
c970c4a61b623c1f127624f60666b0a27e7e0594

R1 evidence:

REQ-06:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/346#issuecomment-7036613128

REQ-10:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/350#issuecomment-7037161287

REQ-06 found:
- Executable domain/storage tests exist.
- Reference-model evaluation historically exists.
- Integrated Brain benchmark is not established.
- Representative corpus is not established.
- Product improvement is not demonstrated.

REQ-10 found:
- Integrated runtime performance is not established.
- Representative workload benchmarks are absent.
- P50/P95/P99 are NOT_MEASURED.
- Resource and model-cost attribution are NOT_MEASURED.

The two findings share the missing integrated runtime but retain separate evaluation responsibilities.

## 4. INVESTIGATION

Inspect:

1. Existing runtime entry points.
2. Domain and storage APIs.
3. Memory retrieval and context preparation.
4. Applied Context evidence.
5. Existing reference models.
6. Available adapter implementations.
7. Model invocation boundaries.
8. Benchmark and test infrastructure.
9. Existing #254 evaluation proposals.
10. Resource and cost measurement opportunities.

Verify current code rather than assuming historical specifications remain accurate.

## 5. REQUIRED DESIGN

Design a minimal executable evaluation architecture.

REQ-06 must define:

- Three-arm comparison.
- Identical task inputs.
- Fair memory initialization.
- Task success measurement.
- Factual correctness.
- Recall precision and recall.
- False and stale memory activation.
- User correction burden.
- Long-term task continuity.

REQ-10 must define:

- End-to-end latency.
- Retrieval latency.
- Model-call latency.
- P50/P95/P99.
- Throughput and concurrency.
- CPU and memory.
- Token usage.
- Model cost.
- Storage growth.
- Degradation behavior.

Specify how both requirements share instrumentation without merging their acceptance criteria.

Design the minimum interface between:

- Task runner.
- Memory system.
- Agent adapter.
- Model invocation.
- Evaluation recorder.
- Performance recorder.

Compare mature benchmarking, tracing and evaluation ecosystems.

## 6. OUTPUT

A. Existing integration inventory.
B. Missing runtime capabilities.
C. Three-arm execution architecture.
D. Fair-comparison protocol.
E. Shared runtime interface.
F. REQ-06 evaluation contract.
G. REQ-10 performance measurement contract.
H. Representative workload design.
I. Dataset and contamination controls.
J. Mature ecosystem comparison.
K. Reproducible benchmark plan.
L. Cost attribution design.
M. Failure and degradation model.
N. Implementation sequence and rollback plan.

Do not fabricate benchmarks, model prices or performance targets.

## 7. AUTHORITY

This is architecture design only.

No main writes, production deployment, infrastructure expansion, merges or authorization.

Do not declare either REQ-06 or REQ-10 implemented or verified.

Do not confuse an executable reference model with an integrated Brain runtime.

Do not report CI PASS when CI has not run.

If formal Stage 0 registration is not available, record PENDING_FORMAL_REGISTRATION and do not claim substantive R2 execution.

## 8. ACCEPTANCE

The design must:

1. Provide an executable path for all three evaluation arms.
2. Explain fair comparison and confounder control.
3. Define separate REQ-06 and REQ-10 acceptance tracks.
4. Define reproducible workloads.
5. Define all required measurements.
6. Explain instrumentation overhead.
7. Provide failure and degradation tests.
8. Identify mature alternatives.
9. State implementation dependencies.
10. Avoid claiming product value before actual experiments.

Next task: independent review of the benchmark architecture and measurement validity.

## 9. STAGE 0 REGISTRATION — UNIFIED SNAPSHOT RULE (BINDING, applies from this first round)

You must produce a Stage 0 registration manifest. The following rule is already adjudicated and is NOT open for redesign:

1. **The dispatched source prompt file is the sole authoritative prompt snapshot.** The coordination layer — not you — will copy it byte-for-byte into the repository as `prompt-v1.md`.
2. **Therefore do not re-output the prompt text.** Do not attempt to reproduce, re-render, summarize, or "clean up" the prompt you received. Observed fact: the message channel strips or alters Markdown structural markers, so any re-output you produce will NOT be byte-identical. Two prior sessions failed exactly here.
3. In the manifest, set the prompt fields to placeholders that the coordination layer will fill with measured values:
   - `prompt_file: 14-ai-development/work-items/<AID>/prompt-v1.md`
   - `prompt_status: PENDING_COORDINATOR_COPY`
   - `prompt_sha256: PENDING_COORDINATOR_MEASUREMENT`
   - `prompt_bytes: PENDING_COORDINATOR_MEASUREMENT`
   - `prompt_provenance_tier: T1`
   - `prompt_provenance_note:` state that the snapshot is mechanically copied by the coordination layer from the dispatch source file, and that byte-equality between the source artifact and the content rendered to this session is `NOT_VERIFIED`.
   - `prompt_delivery_integrity: NOT_VERIFIED`
4. Do not claim the prompt snapshot is verified. Do not invent a SHA-256 or byte count.

Everything else in your manifest must be your own substantive output: scope, non-goals, baseline evidence, dependencies, acceptance criteria, risk, and the explicit `NOT_ASSIGNED` / `NOT_APPOINTED` governance fields. Do not self-appoint sponsor, accountable_owner, or acceptance_authority.

If the identifier `<AID>` has not been confirmed as globally unique, record `identifier_status: PENDING_COORDINATOR_VERIFICATION` rather than asserting it is assigned.

Output the manifest as a single YAML code block. Then stop — do not begin substantive R2 design in this round.
