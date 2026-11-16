# A–I Module Baseline & Redlines Rollout

- Plan version: 0.1.0
- Status: **PROPOSED — rollout authorization pending G0**
- Coordination: A may track progress; each Module Owner authors and approves its own module baseline.

## Common mandatory work

Each Module Owner must:
1. Read the approved Project Baseline and Project Redlines. Until G0 approval, read these proposals as PROPOSED constraints for analysis, not ACTIVE authority.
2. Read its latest branch-local design files and review reports, plus Phase 2/3 cross-module review artifacts.
3. Create its module baseline using `00-governance/module-baseline-and-redlines-template.md` on its own Owner branch.
4. Define module redlines, authority objects, non-owned objects, exclusive operations and prohibited cross-module actions.
5. Define exact interface/conformance requirements and inherited security constraints.
6. List OPEN/ADR-BLOCKED decisions and affected consumers; do not resolve non-owned ADRs.
7. Provide path, branch, full current HEAD SHA, blob SHA, owner decision, tests/evidence and explicit non-claims.
8. Preserve history; do not merge branches or rewrite review conclusions.

A may coordinate the schedule and cross-module matrix, but may not approve B–I baselines or make their internal authority decisions.

## Module-specific assignment

### A — Integration Governance
Define integration mission, contract registry authority (coordination only), dependency/finding lifecycle, baseline reconciliation, branch-aware evidence freshness, gate orchestration and consumer acceptance tracking. Explicitly state A does not own PGA appointment, project redlines, domain schemas or module internal authority. Must distinguish artifact existence, owner decision, cross-module acceptance, implementation and test evidence. Record how it closes findings only with named owner approvals.

### B — Domain Model
Define canonical domain object taxonomy, typed references, identity/scope reference semantics and domain invariants. Preserve Fact/Claim as ADR-BLOCKED until its declared authority formally decides. Do not allow preference/option analysis to become approval. Explicitly distinguish Event/Memory/Fact/Claim, Evidence/Provenance, Confidence/Relevance and Scope/Permission; identify which semantics are decided vs candidate.

### C — Agent Integration / Telemetry
Define Agent Telemetry, producer assertions vs authenticated identity, Inference Boundary, request/turn correlation and Untrusted Memory handling. Protect System Instructions, Developer Instructions, User Original Input and Agent Safety Policy. Define the managed-region boundary and ensure Brain output cannot become tool/action authority. No Agent planning/execution ownership.

### D — Memory Brain
Define Canonical Memory identity/version, canonical writes, lifecycle, entities/relations, canonical cursor and ForgetFence authority. Define exclusive operations and forbidden direct writes by other modules. Preserve D's semantic decisions separately from storage implementation and global Forget completion policy. Do not claim the D/E/Storage atomic producer registration/publication gate is closed without conformance evidence.

### E — Memory Compiler
Define durable Event ingress, compiler work/lease/retry/DLQ/replay, extraction, derived lineage and publication. Ensure staged artifacts are non-visible until D dependency registration, current auth/fence checks and final publication gate succeed. Do not own Canonical Memory or canonical Forget. Explicitly leave D/E/Storage atomic linearization contract OPEN until implemented and tested.

### F — Memory Runtime / Retrieval
Define retrieval candidate generation, fusion, freshness, working sets, caches and per-index IndexWatermark. Define scope-before-candidate and final response suppression. Must not mutate canonical memory or G Context versions. Define cache/index rebuild and in-flight cancellation behavior under Forget/revocation.

### G — Memory Context
Define desired managed Context membership/order/budget, ContextVersion, reconciliation, delivery intents, removal and Applied evidence. Explicitly separate Context removal from Canonical Memory Forget and Delivered from Applied. Respect C's protected prompt regions and H Adapter evidence semantics. Do not claim global Forget completion.

### H — BMCP Protocol / Adapter
Define wire envelope, versioning, capability negotiation, ACK classes, reconnect/offline behavior, delivery and Adapter-local clear/application attestations. Keep identity/permission fields candidate where B/I authority remains open. Payload source identity is not authentication. Local ACK is not global Forget completion.

### I — Security & Governance
Define Principal, Permission, delegation, revocation, retention, target inventory, Global Forget completion, external recipient/backup governance, audit and residual risk acceptance. Coordinate with B/H on typed identity and wire binding. Define ACK-to-target-state mapping and policy exceptions. I cannot approve project redlines alone.

## Required cross-module rollouts

| Work item | Owners | Required evidence | Must remain open until |
|---|---|---|---|
| Fact/Claim semantics | B + declared ADR authority; D/E/F/G/H consumers | Approved ADR and mapping acceptance | B ADR formally approved and consumers reconciled |
| Principal/ActorRef/ScopeRef | B/I/H + C/D/E/F/G | Exact typed reference and authenticated transport binding; negative tests | All affected owners accept same mapping |
| D/E/Storage producer barrier/publication | D/E/Storage | Linearization contract, crash/race tests, no late derivative | Both race outcomes and recovery verified |
| Canonical cursor propagation | D/A/E/F/G/Storage | D decision consumed; typed cursor mapping and persistence validation | Consumers and Storage conformance pass |
| Forget global proof | D/E/F/G/H/I + Storage | Target inventory, fence/watermark vector, ACK mapping, replay/reconnect/restore tests | No required unknown target; policy-approved exception only |
| Prompt injection | C/E/F/G/H/I | Threat model, poisoning/summary laundering/protected-region tests | Negative tests and residual risk approved |
| Quality/operations | All relevant owners + Verification | Reproducible tests, benchmarks, restore drills, runbooks | Relevant G3–G5 criteria met |

## Rollout sequencing

1. G0 approval and publication of exact active baseline/redline versions.
2. A–I submit owner-authored module baseline proposals in parallel on their own branches.
3. A reconciles cross-module conflicts without overriding owner decisions.
4. Relevant ADR authorities decide open domain questions; owners update consumers.
5. Verification Owner runs conformance against synchronized contracts.
6. PGA/authorities review gate evidence; only then advance G1–G5.

No branch merge is implied or authorized by this rollout plan.
