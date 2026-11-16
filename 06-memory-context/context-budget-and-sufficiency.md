# Context Budget and Sufficiency

**Status:** DECIDED multi-dimensional policy; CANDIDATE optimization; TO_VALIDATE thresholds  
**Owner:** Session G

## 1. Purpose

Budget Manager allocates a bounded managed region while preserving task-required coverage, provenance and uncertainty. Sufficiency asks whether selected Context covers information dimensions required for a task—not whether highest-scoring K memories were selected.

A Context may fit budget and still be insufficient. It may be sufficient for one task and insufficient for another. No universal score or Top-K threshold is assumed.

## 2. Budget dimensions

Budget is a vector:
- token budget under target tokenizer/model profile;
- serialized byte budget and transport/package limits;
- maximum Entry count and distinct canonical refs;
- maximum relation fan-out and provenance depth;
- planning/commit/delivery latency budget;
- refresh frequency and CPU/memory cost;
- compaction cost and expected expansion cost;
- per-tier reserved capacity and protected-entry constraints.

Tokenizer/model identity is a rendering constraint, not a canonical-memory dependency. Unknown tokenizer means conservative byte/count estimates and non-exact token estimates.

## 3. Sufficiency dimensions

Planner declares a task-specific requirement profile and evaluates:
1. **Semantic coverage:** required concepts, facts, procedures or constraints.
2. **Entity coverage:** task-critical entities and disambiguating identities.
3. **Relation coverage:** required relationships/dependencies, not just entity names.
4. **Environment coverage:** correct world/save/tenant/project state.
5. **Temporal validity:** current valid-time; exclude stale/superseded revisions.
6. **Evidence coverage:** critical claims retain supporting evidence/provenance refs and epistemic labels.
7. **Risk coverage:** relevant hazards, irreversible consequences and privacy/security warnings as data.
8. **Uncertainty coverage:** unresolved conflicts, missing observations and confidence limitations.
9. **Freshness/completeness:** canonical/index watermarks current enough; truncation and lag surfaced.
10. **Non-redundancy:** paraphrases do not consume budget without coverage gain.

Each requirement is satisfied, partial, missing, conflicted or unknown, with source refs and rationale.

## 4. Planning algorithm

1. Build a requirement graph from structured task/intent/telemetry and explicit Agent requirements; do not infer private CoT.
2. Identify mandatory anchors: Scope, environment identity, task invariants, critical risk and uncertainty.
3. Request F candidates with scoped filters and coverage categories.
4. Reauthorize and canonical-validate each candidate; reject stale/retracted/forgotten/ineligible versions.
5. Estimate cost and marginal coverage gain for candidate sets.
6. Select under vector constraints, considering relation/evidence dependencies and redundancy.
7. Preserve conflicting claims as alternatives with dispute markers where relevant.
8. Compact only when coverage and traceability survive validation.
9. Place selected entries into P0–P2; defer remaining eligible refs to P3.
10. Emit sufficiency report: omissions, uncertainty, freshness and budget utilization.

Relevance is one input. It cannot compensate for wrong environment, invalid time, missing evidence or denied permission.

## 5. Optimization and compaction

**CANDIDATE:** maximize weighted requirement coverage/marginal utility while penalizing redundancy, latency, token/byte cost, compaction loss and uncertainty hiding. Authorization, Forget, temporal validity, environment match and required evidence are hard constraints before ranking.

Compaction must preserve exact canonical refs/source membership, critical names/quantities/units/time qualifiers/conditions/exceptions, uncertainty and conflict. It must not upgrade reported/inferred claims to verified language or merge inconsistent claims into one synthetic fact. Retain expansion refs subject to current authorization. Record algorithm/model version, input/output hashes, cost and validation outcome. Reject compaction if semantic fidelity cannot be established.

## 6. Sufficiency outcomes

- **Sufficient:** all hard requirements met; no blocking coverage gap; freshness and authorization acceptable.
- **Conditionally sufficient:** core requirements met; named non-critical gaps/uncertainty surfaced.
- **Insufficient:** mandatory requirement missing, stale, materially conflicted or unsupported by evidence.
- **Unknown:** retrieval completeness, canonical freshness, environment identity or required metadata cannot be established.

Sufficiency is task/profile/time-specific. It is not a truth guarantee, Agent readiness signal or permission to act. Agent decides whether it has enough information and whether to act under its own policy.

## 7. Overflow policy

1. Recompute estimates using target rendering profile.
2. Remove redundant P2 entries and move low marginal value to P3.
3. Compact eligible groups with fidelity validation.
4. Reduce optional relation/evidence expansion while retaining required refs and uncertainty.
5. Ask F for narrower candidates or defer refresh if safe.
6. If hard requirements still exceed budget, report Insufficient and exact gaps; do not silently drop P0 or mislabel sufficiency.

## 8. Metrics and decisions

Measure token/byte/count utilization, stage latency, coverage by dimension, omitted requirements, compaction ratio/cost, semantic regression, redundancy, stale-entry rate and task outcome correlation. Test multi-entity planning, environment simulation, conflicts, temporal change, long histories, partial index outage and strict caps.

- **DECIDED:** vector budgets and multi-dimensional sufficiency; hard constraints precede ranking.
- **CANDIDATE:** marginal coverage optimization and tier reserves.
- **TO_VALIDATE:** weights, thresholds, tokenizer variance, compaction fidelity and latency.
- **OPEN:** task requirement schema with F/C; rendering/token accounting with H.


## 9. Phase 3.5 candidate integrity, typed freshness and producer constraints

### 9.1 Runtime candidate admission

F RetrievalResult and ActivationRecommendation are immutable proposals, not Context membership or authorization. G requires exact typed MemoryRef/MemoryVersionRef, ScopeRefs, activation reason, source/evidence refs, epistemic/lifecycle/temporal metadata, uncertainty, completeness/truncation, canonical source references and per-index/per-partition IndexWatermark. G independently re-resolves canonical identity/version/lifecycle with D and current permission/fence with I/D before inclusion.

A single maximum IndexWatermark cannot represent a multi-partition result. Sufficiency records a vector of per-index/per-partition watermarks, contiguous-gap state, freshness requirement and completeness outcome. Missing or lagging partition data is Partial/Unknown; omission is not proof of nonexistence. F cache/index freshness never overrides D canonical retraction, supersession or ForgetFence.

### 9.2 Hard constraints before optimization

The following are admission constraints, not weighted preferences: authenticated identity; complete required Scope including EnvironmentRef; current I PermissionEpoch/authorization; current D ForgetFence and source-lineage eligibility; canonical MemoryVersion/lifecycle/temporal validity; required Evidence/Provenance authorization; classification; and task/environment match. A high relevance score, P0 priority, evidence summary or sufficient token budget cannot compensate for any failed hard constraint.

### 9.3 Compaction as a registered derivative

Compaction is a G-owned derived artifact. Its source set includes every input ContextEntry, exact canonical MemoryVersion, Evidence/Provenance refs and transitive lineage. G records algorithm/model/profile version, canonical input/output digests, omissions/loss, validation outcome and expansion refs. It registers producer work and complete dependency lineage with D before publication, rechecks I PermissionEpoch and D ForgetFence at the final visibility gate, and keeps output private if any receipt/gate is missing or unknown.

Compaction cannot convert disputed/reported/inferred material into verified statements, merge conflicting Claims into a synthetic fact, remove required risk/uncertainty qualifiers or sever provenance. A compacted projection changes desired Context content and therefore participates in a new immutable ContextVersion; it never creates or updates Canonical Memory.

### 9.4 Budget reporting and safe degradation

The sufficiency report adds:
- exact ContextVersion and requirement-profile version;
- per-dimension coverage and omissions;
- per-index/per-partition IndexWatermark vector and completeness gaps;
- canonical commit/fence references and current PermissionEpoch decision;
- budget vector (token estimate/profile, bytes, entries, relation/provenance bounds, latency/CPU);
- compacted source membership and validation/digest profile;
- blocked/deferred refs without leaking unauthorized existence or counts.

If D/I currentness or F completeness cannot be established, mark Unknown/Insufficient for affected requirements and do not publish a Context that implies complete coverage. If hard requirements exceed budget, report the exact safe omissions/gaps; never silently drop protected P0, risk, uncertainty or provenance requirements.
