# Agent Telemetry Model

**Status:** DECIDED semantic boundaries; CANDIDATE field profiles; TO_VALIDATE operational limits  
**Owner:** Session C — Agent Integration boundary pre-design  
**Dependencies:** Session B domain semantics; Session E ingestion mapping; Session H BMCP wire schema.

## 1. Purpose

Telemetry is a structured, bounded description of Agent task state and relevant observations. It helps Brain determine what to remember, retrieve, activate, or reconcile. It is not a transcript of all internal reasoning and is not an authoritative substitute for source evidence.

Telemetry can describe what an Agent is doing, intends to do, plans, which entities/environment are relevant, what action is pending, what was observed, what outcome was reported, what remains uncertain, and what changed in an environment.

## 2. Principles

1. **DECIDED:** Telemetry is typed data, not instruction.
2. **DECIDED:** Intent and plan are prospective; outcome is retrospective.
3. **DECIDED:** Agent report and environment observation retain distinct source kinds.
4. **DECIDED:** Full Chain of Thought (CoT) is not required.
5. **DECIDED:** Every signal is scoped and time-qualified.
6. **DECIDED:** Unknown is not silently converted into a negative or certain fact.
7. **DECIDED:** Telemetry acceptance does not imply Memory creation or verification.
8. **CANDIDATE:** A small canonical core with typed payloads and namespaced extensions is preferable to mirroring arbitrary Agent-native objects.

## 3. CoT policy

Brain MUST NOT require complete hidden CoT, private scratchpads, token-by-token reasoning, or proprietary model traces.

Reasons:
- CoT is model/provider-specific and conflicts with model independence.
- It may expose sensitive or irrelevant internal information.
- It is not a reliable source of externally verifiable facts.
- It increases payload, retention, and security costs.
- Useful memory behavior can be driven by task state, concise plan summaries, entities, observations, outcomes, uncertainty, and provenance.

A concise Plan Summary may be supplied when useful. It is an Agent-authored summary, not a faithful or complete record of hidden reasoning. Brain labels it as reported/planned information, not verified fact.

## 4. Logical telemetry envelope

This is a semantic schema, not the final BMCP wire format.

| Field | Type semantics | Required | Constraint |
|---|---|---:|---|
| telemetry_id | Stable opaque ID | Yes | Unique in producer namespace |
| schema_version | Canonical schema version | Yes | Unsupported major rejected |
| producer_id | Authenticated producer | Yes | Must match credentials |
| agent_id | Logical Agent identity | Yes | Stable namespace |
| agent_instance_id | Running instance | Conditional | Required for context/session |
| session_id | Agent session | Conditional | Required for session signals |
| task_id | Task identity | Conditional | Required for task signals |
| environment_id | Environment namespace | Conditional | Required for environment-specific signals |
| scope | Ownership namespace | Yes | Must be authorized |
| signal_type | Canonical discriminator | Yes | Core enum plus versioned extensions |
| occurred_at | Source event time | When known | Preserve unknown reason |
| observed_at | Observation time | When applicable | Distinct from occurred_at |
| recorded_at | Brain acceptance time | Brain assigned | Producer value not authoritative |
| source_kind | Agent/environment/user/tool/external | Yes | Typed |
| correlation_id | Turn/action/workflow link | No | Recommended |
| idempotency_key | Retry identity | For retryable writes | Stable across retries |
| payload | Typed signal body | Yes | Per-type schema and size limit |
| provenance | Origin/transformation history | For derived claims | Preserve source refs |
| extensions | Namespaced opaque fields | No | Cannot override canonical fields |

Producer timestamps are claims about time. Brain records its own acceptance time and may separately record clock uncertainty.

## 5. Canonical signal types

### 5.1 Task State

Current lifecycle/status of a task as represented by Agent. It is not proof of success or of the truth of task content.

Suggested statuses: created, active, blocked, waiting, completed, failed, cancelled, unknown.

Fields: task_id (required), status (required), status_reason (optional), parent_task_id (optional), changed_at (when known), reported_by (required).

A completed status is still an Agent report unless corroborated by outcome evidence.

### 5.2 Intent

Agent's current desired objective or direction.

Fields: intent_id, task_id, statement, target_entities (references or unresolved mentions), status (current/revised/withdrawn/unknown), effective interval where known.

Intent is prospective and MUST NOT be compiled as a completed Event merely because it was submitted.

### 5.3 Plan Summary

Concise Agent-reported outline of intended steps. It is not full CoT or a guaranteed execution trace.

Fields: plan_id, task_id, summary, optional step_summaries, plan_revision, status (proposed/active/revised/abandoned/completed_reported), created_at, updated_at.

A completed plan lifecycle does not prove every step succeeded. Outcomes require separate signals.

### 5.4 Active Entities

Entities currently salient to a task, with a stated role.

Fields: entity_ref or unresolved mention, role (subject/target/tool/location/participant/resource/other), salience_reason, optional confidence with declared semantics, optional task validity.

A mention is not automatically a canonical Entity. Resolution is Brain-domain logic.

### 5.5 Pending Action

An action intended or scheduled but not confirmed complete.

Fields: action_id, task_id, action_kind, optional target_ref, status (planned/ready/submitted/in_progress/awaiting_result/cancelled/unknown), optional expected_effect, deadline, dependencies.

Pending Action MUST NOT be emitted as a completed outcome. Submission acknowledgement is not proof of intended effect.

### 5.6 Observation

A source-qualified statement that a condition, event, or result was observed.

Fields: observation_id, subject_ref or mention, predicate/observation_type, typed value, source_kind (environment/tool/agent_report/user/external), observed_at, optional method/sensor/tool, recommended raw_evidence_ref, optional quality/limitations.

Observation records what a source reports seeing. It is not automatically independent verification.

### 5.7 Outcome

A reported or observed result associated with an action, task, or plan step.

Fields: outcome_id, related_action_id or task_id, result_status (succeeded/failed/partial/unknown), result_summary, source_kind, occurred_at/observed_at, evidence_refs, optional side_effects.

An Agent-reported outcome remains a report. Tool/environment evidence can strengthen or qualify it. Missing outcome is not failure.

### 5.8 Uncertainty

An explicit statement of what is unknown, ambiguous, conflicting, or estimated.

Fields: optional subject_ref, question_or_proposition, uncertainty_kind (unknown/ambiguous/conflicting_signals/low_observability/estimate), known_limitations, optional confidence_estimate with method, related_signal_refs.

Preserve unresolved state rather than forcing a guessed value.

### 5.9 Risk Signal

A warning of possible harm, irreversibility, privacy, security, or reliability concern.

Fields: risk_id, risk_category, producer-reported severity with documented semantics, related action/task, rationale_summary, mitigation_state, source_kind.

Risk may trigger conservative Brain retrieval/activation policy. It does not authorize or block Agent actions; Agent policy remains authoritative.

### 5.10 Environment Delta

A source-qualified change between two identified environment states.

Fields: environment_id, base_state_ref, new_state_ref or observation_id, typed changes, observed_at, source_kind, completeness (complete/partial/unknown), optional coordinate/schema version.

A true delta requires a valid base state. Without one, submit a snapshot/observation rather than inventing a delta. Deltas are isolated by environment identity.

## 6. Required and optional profile

| Signal | Minimum profile | Enhanced profile | Notes |
|---|---|---|---|
| Producer identity/schema | Required | Required | Authentication-bound |
| Scope | Required | Required | No implicit global scope |
| Task/session identity | When relevant | Required | Continuity |
| Task State | Recommended | Required for proactive orchestration | Agent-reported |
| Intent | Optional | Recommended | Concise |
| Plan Summary | Optional | Optional | Never full CoT |
| Active Entities | Optional | Recommended | Prefer canonical refs |
| Pending Action | Optional | Recommended | Prospective |
| Observation | Required for observation claims | Required | Source/time qualified |
| Outcome | Required when claiming result | Required | Separate from plan |
| Uncertainty | Optional | Recommended | Unknown is valid |
| Risk Signal | Optional | Recommended where available | Map native risk vocab |
| Environment Delta | Optional | Required when claiming stateful delta integration | Requires base and environment |
| Evidence reference | Required for derived/verified claims where available | Required | Artifact/tool ref |
| Full CoT | Never | Never | Not an integration requirement |

**CANDIDATE:** Define minimum and enhanced profiles, while keeping mandatory fields operation-specific. Tier 3 need not produce all proactive telemetry.

## 7. Plan-to-outcome separation

~~~mermaid
flowchart TD
  I[Intent] --> P[Plan Summary]
  P --> A[Pending Action]
  A --> X[Execution outside Brain]
  X --> O[Observation or tool result]
  O --> R[Outcome]
  R --> E[Evidence and provenance]
  E --> C[Candidate Event or Claim]
  C --> M[Memory compilation and governance]
  A -. not proof of .-> R
  P -. not proof of .-> O
~~~

**DECIDED:** Plan describes intended future work; Pending Action describes unconfirmed action; Observation describes what a source observed; Outcome describes a result with source qualification; Evidence supports/refutes/qualifies claims. Memory Compiler decides whether telemetry becomes memory.

## 8. Task and environment switching

Task switch should use explicit task identity and state transition. Do not infer a switch solely from a changed natural-language summary when stable identifiers exist.

Environment switch requires a new environment_id or explicit transition. Environment-local entities, coordinates, snapshots, and deltas must not cross environments without a verified mapping.

If continuity is ambiguous, emit an unknown/ambiguous state or request reconciliation. Never silently merge.

## 9. Validation and normalization

- Reject missing authenticated producer, invalid schema, unauthorized scope, malformed required IDs, and over-limit payloads.
- Preserve original source values when normalization changes representation.
- Keep source time and Brain recorded time separate.
- Treat unknown extensions as opaque.
- Reject or quarantine contradictory envelope and payload identity.
- Bound payload sizes and array lengths.
- Deduplicate retries under scoped idempotency.
- Redaction should preserve a redaction marker and permitted provenance; do not silently imply the omitted data never existed.

## 10. Submission lifecycle

Logical lifecycle:
- Prepared — Adapter formed a submission.
- Submitted — request sent; durable acceptance unknown.
- Accepted — Brain durably accepted and issued receipt.
- Rejected — Brain refused submission.
- Processing — optional asynchronous downstream work.
- Processed — downstream stage completed; no implication that Memory was created.
- FailedRetryable / FailedTerminal — downstream processing outcome.

Final BMCP state names belong to Session H. An Accepted telemetry record remains a durable source record even if semantic processing later fails, subject to retention.

## 11. Security and retention

Do not require or collect full CoT, credentials, API keys, secrets, or unrelated prompt history. Prefer concise summaries and source references. Enforce scope and permission before persistence and readback. Preserve classification/provenance through normalization. Retention applies to raw telemetry and derivatives while respecting lineage and Forget governance. Producer trust labels cannot bypass Brain policy.

## 12. Performance metrics

Measure events/bytes per Agent, task, session, and environment; ingress p50/p95/p99; durable acceptance rate; validation and duplicate rates; telemetry-to-activation lag; Recall quality by profile; CPU/memory/storage/network per signal; redaction rates; and false outcome inference (target zero in deterministic tests).

**TO_VALIDATE:** sampling cadence, payload caps, retention windows, and telemetry-to-activation SLO.

## 13. Acceptance tests

1. Intent alone creates no completed Event/Outcome.
2. Plan Summary and Pending Action do not create successful Outcome.
3. Observation records source kind and observed time separately from Brain recorded time.
4. Agent-reported Outcome is not silently upgraded to independently verified.
5. Environment Delta without environment identity/base is rejected or downgraded to observation.
6. Identical retries under same idempotency scope produce one logical accepted item.
7. Task switch does not inherit unrelated pending actions.
8. Environment switch prevents cross-environment state leakage.
9. Unknown extensions remain opaque and cannot override canonical fields.
10. No integration requires full CoT.
11. Permission-denied telemetry is not accepted as canonical evidence.
12. Missing uncertainty is not interpreted as certainty.

## 14. Interfaces and open questions

| Partner | Confirmation |
|---|---|
| Session B | Event, Evidence, Provenance, epistemic and temporal fields |
| Session E | Signal-to-Event mapping; durable ingress semantics |
| Session F | Retrieval/Activation dimensions, freshness and risk policy |
| Session G | Context update triggers and task/session identity |
| Session H | BMCP message families, enum evolution, schema negotiation, errors |
| Session I | Classification, retention, redaction, audit, idempotency |

**OPEN:** Task State periodic snapshot, transition stream, or both. **CANDIDATE:** transitions plus occasional snapshots for recovery.  
**OPEN:** Whether Brain needs canonical task hierarchy or opaque Agent references.  
**TO_VALIDATE:** Profile-specific payload and frequency limits.

## 15. Decision summary

- **DECIDED:** Telemetry is structured, scoped, source-qualified data, not hidden reasoning.
- **DECIDED:** Full CoT is not required and is not a default ingestion target.
- **DECIDED:** Intent, Plan Summary, and Pending Action are prospective.
- **DECIDED:** Observation and Outcome are distinct and source-qualified.
- **DECIDED:** Unknown/uncertain states are first-class.
- **CANDIDATE:** Small canonical core with typed payloads and namespaced extensions.
- **OPEN:** Wire schema belongs to Session H; domain mapping belongs to Sessions B and E.
