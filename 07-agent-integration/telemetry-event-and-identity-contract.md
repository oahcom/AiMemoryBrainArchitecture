# Telemetry Event and Identity Contract

- Owner: Session C — Agent Integration Principal Architect
- Status: **DECIDED semantic boundaries; CANDIDATE event profile and ordering details; H/I-dependent identity binding OPEN**
- Branch: `session-c-agent-integration-2026-11-16`
- Baseline: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
- Scope: Agent-side telemetry semantics, producer claims, event identity/order, correction/retraction and consumer requirements.
- Non-goals: BMCP wire encoding/schema (H); canonical Event/Memory commit or compilation (D/E); global identity, grant, authorization and retention policy (I); Context authority (G); Runtime retrieval (F).

## 1. Normative intent

This contract defines what an Agent integration may report to the Brain without exposing complete hidden chain-of-thought (CoT). Telemetry is structured, source-qualified data about task, action, observation, outcome and environment state. It is not a transcript of private reasoning and does not transfer reasoning, planning, action or tool authority from the Agent to the Brain.

The Brain MUST NOT require complete hidden CoT, private scratchpads, token-by-token reasoning, proprietary inference traces or unrelated prompt history. An optional concise PlanSummary is an Agent-authored operational summary, not a faithful or complete representation of hidden reasoning. It MUST be labeled as a report of plan state, not as evidence that steps occurred.

The terms MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are normative.

## 2. Ownership and consumer boundary

| Concern | Authority | C contract |
|---|---|---|
| Agent reasoning, intent, planning, action selection and tool authorization | Agent | Observe/report only; never take authority |
| Telemetry semantic types and evidence quality labels | C | Define and validate semantic distinctions |
| Authenticated Principal, issuer, ProducerIdentity, delegation and permission epoch | I policy; H authenticated transport binding; B typed reference semantics | Require authenticated binding evidence; do not invent identity policy |
| Wire envelope, serialization, signature transport and Adapter SDK | H | Consume H's binding and transport guarantees; no wire schema here |
| Durable acceptance, receipt and compile processing | E | Supply stable source event/idempotency semantics; do not equate acceptance with compilation |
| Canonical Memory/Event identity, lifecycle and Forget fence | D | Preserve source lineage and obey suppression; do not define canonical storage |
| Retrieval and activation | F | Supply typed signals; no retrieval policy ownership |
| ContextVersion, ContextChangeSet and delivery intent | G | Supply correlation/task/session signals; no Context authority |
| Global authorization, revocation, retention and Forget completion | I | Fail closed on unknown/stale policy state; no risk acceptance |

A receiving subsystem may validate and reject telemetry but MUST NOT reinterpret a prospective or reported signal as a verified real-world fact solely because the producer is authenticated.

## 3. Semantic object taxonomy

Each record has exactly one primary semantic kind. Additional related records may be linked by typed references, but consumers MUST NOT collapse these kinds into a generic “event happened” interpretation.

| Kind | Meaning | Minimum semantic constraint | Explicit non-meaning |
|---|---|---|---|
| `Observation` | A source-qualified statement that a source observed a condition, event or state | Identify observer/source kind, observed subject/value, observed time and limitations | Not automatically independently verified or globally true |
| `Outcome` | A reported or observed result associated with an action, task or plan step | Link to action/task; state result status and evidence/source | Not implied by intent, plan, tool submission or acknowledgement |
| `Intent` | Agent's desired objective or direction | Identify intent, task, statement, status and effective time when known | Not a completed action or outcome |
| `PlanSummary` | Concise Agent-authored outline of intended steps | Identify plan/task, revision, status and author/source | Not full CoT, execution trace or proof that any step occurred |
| `PendingAction` | An intended, queued, submitted or in-progress action whose effect is not confirmed | Identify action and explicit pending status | Not successful execution or resulting environment state |
| `ToolCall` | A tool invocation lifecycle record | Distinguish requested, dispatched, acknowledged, returned, failed, cancelled; link call and tool identity | Invocation/return envelope alone does not prove the intended external effect |
| `EnvironmentDelta` | A source-qualified change between two identified states in one environment | Require environment identity and base state; identify resulting state or observation and completeness | Not valid across environments or without a known base |
| `Uncertainty` | Explicit unknown, ambiguous, conflicting, estimated or low-observability state | Preserve unknown kind, limitation and related signals | Missing data is not certainty; confidence is not truth |

### 3.1 Observation

Observation describes what a named source reports observing. Minimum logical attributes:

- `observation_id`;
- subject reference or unresolved mention;
- predicate/observation type and typed value;
- source kind (environment, tool, Agent report, user, external source);
- `observed_at` when known, with clock-quality/uncertainty where available;
- method/sensor/tool reference when applicable;
- evidence reference or explicit reason evidence is unavailable;
- quality, completeness and limitations.

An Agent report is an Agent report even if the Agent is authenticated. A tool or environment observation may be stronger evidence but is not automatically independent verification.

### 3.2 Outcome

Outcome records the result, not the intention. It MUST link to an action/task/plan step where possible and state `succeeded`, `failed`, `partial` or `unknown`. It records source kind, occurrence/observation time, evidence references and relevant side effects. Agent-reported success remains reported success unless corroborated under the consuming domain's evidence policy. Absence of an Outcome is not failure.

### 3.3 Intent and PlanSummary

Intent is prospective. PlanSummary is a compact description of intended work. Revisions create a new revision or append a superseding signal; they do not rewrite history. A plan status of `completed_reported` means only that the producer reports the plan lifecycle as complete; it does not assert that every step succeeded.

### 3.4 PendingAction and ToolCall

PendingAction represents an action that has not reached a confirmed outcome. Its statuses SHOULD distinguish `planned`, `ready`, `submitted`, `in_progress`, `awaiting_result`, `cancelled` and `unknown`.

ToolCall records invocation mechanics separately from effect:
- `requested`: Agent expressed a call request;
- `dispatched`: invocation was handed to the tool boundary;
- `acknowledged`: tool endpoint accepted the call;
- `returned`: a result payload was returned;
- `failed` / `cancelled` / `timed_out`: invocation lifecycle outcome.

A ToolCall return is evidence that a tool returned a payload. It does not automatically establish that a remote side effect committed or that an environment changed. That requires a separate Observation or Outcome with suitable source/evidence.

### 3.5 EnvironmentDelta

EnvironmentDelta MUST identify the environment namespace, base state reference, new state reference or observation, typed changes, source and observation time. If the base state is absent or invalid, the producer MUST submit an Observation or snapshot instead; it MUST NOT fabricate a delta. A delta is meaningful only inside its bound environment. Switching worlds, tenants, save files or simulations requires a new environment identity or an explicitly verified mapping.

### 3.6 Uncertainty

Unknown, ambiguous, conflicting, estimated and low-observability are first-class states. Preserve the question/proposition, known limitations, method of any confidence estimate and related signal references. A consumer MUST NOT coerce uncertainty into a definitive value to simplify storage, ranking or display.

## 4. Logical event record and identity fields

This section defines semantics only. It is not a JSON schema, protobuf, BMCP envelope or serialization contract.

A logical telemetry record SHOULD carry:

| Field | Semantics | Rule |
|---|---|---|
| `event_id` | Stable immutable event identity | Unique in authenticated producer namespace; never reused |
| `event_kind` | One semantic kind from §3 | Required; unknown critical kind rejected, not remapped |
| `schema_version` | Semantic payload version | Independent from BMCP protocol version |
| `producer_claim` | Payload's declared producer reference | Assertion only; must match authenticated binding |
| `agent_id` / `agent_instance_id` | Logical Agent and running instance | Required where the signal is Agent-originated / instance-bound |
| `session_id` / `task_id` | Session/task correlation | Required when the signal is session/task-specific |
| `environment_id` | Environment namespace | Required for environment-dependent signals |
| `scope_ref` | Ownership/applicability namespace reference | Typed reference; never grants permission |
| `source_sequence` | Producer-local ordering position | Monotonic within one producer stream epoch |
| `source_stream_epoch` | Producer sequence reset/reprovision epoch | Required if source sequence can reset |
| `occurred_at` | When represented occurrence happened | Source claim; may be unknown |
| `observed_at` | When source observed it | Distinct from occurred_at |
| `recorded_at` | Brain durable acceptance time | Brain-assigned; producer value is never authoritative |
| `correlation_id` | Related turn/workflow/task/action | Does not establish order or idempotency |
| `causation_id` | Immediate source signal/event | Optional typed reference |
| `idempotency_key` | Retry identity | Required for retryable state-changing ingress; E owns durable receipt semantics |
| `payload` | Typed body for one event kind | Untrusted data, bounded and validated |
| `evidence_refs` / `provenance_refs` | Supporting source lineage | Typed and independently authorized on dereference |

Producer timestamps are claims. The Brain MUST record its own acceptance time and preserve event/observation time separately. Unknown source time MUST be represented as unknown, not replaced with ingestion time.

## 5. Authenticated producer identity versus payload claims

### 5.1 Three distinct values

1. **Authenticated transport principal:** established by H's authenticated channel/credential mechanism under I's approved issuer and trust policy.
2. **Authenticated ProducerIdentity binding:** H resolves the transport principal to a registered producer/application/instance identity and supplies the binding evidence and relevant identity epoch.
3. **Payload identity claims:** fields such as `producer_id`, `agent_id`, `agent_instance_id`, `ActorRef`, `session_id`, `scope_ref` and `environment_id` supplied by the producer. These are assertions/selectors, not authentication.

A payload MUST NOT authenticate itself. A signed payload digest proves integrity under a key; it does not prove that the key is authorized to assert the payload identity or that the assertion is true.

### 5.2 C consumption requirements

Before treating a telemetry record as attributable to a producer, a consumer MUST receive or resolve a trusted authentication-binding result that identifies:
- authenticated Principal and issuer;
- registered ProducerIdentity and producer instance/workload where applicable;
- credential/key validity and revocation state;
- authenticated audience/channel;
- binding/permission epoch or current policy decision reference;
- verification time and correlation to the ingress operation.

C requires H to expose this binding result to the consuming boundary; I defines which issuers, principals, producers, scopes and actions are trusted/authorized. C does not mint principals, decide grants, define delegation, compare policy epochs, or accept security risk.

The consumer compares payload producer/Agent/instance/ActorRef claims to the authenticated binding. Mismatch, missing binding, unknown issuer, stale/revoked epoch or unavailable authorization state MUST be rejected or quarantined according to I policy; it MUST NOT be silently resolved in favor of the payload. Do not persist rejected claims as canonical evidence.

Scope membership and permission are separate. A matching ScopeRef does not grant access. Every consumer reauthorizes at its own sensitive boundary under I policy, including source dereference, compilation, retrieval, Context materialization, delivery and inference application.

## 6. Event identity, ordering and temporal semantics

### 6.1 Event ID and source sequence

`event_id` is immutable and stable across retries and corrections referencing that event. Uniqueness is enforced within the authenticated ProducerIdentity namespace; implementations SHOULD use globally collision-resistant opaque identifiers. An event ID collision with different content is an integrity/idempotency conflict.

`source_sequence` is monotonic within the tuple:

`(authenticated ProducerIdentity, producer_instance, source_stream_epoch)`.

It is not a global Brain sequence, canonical commit cursor, aggregate revision, index watermark, ContextVersion, delivery sequence, permission epoch or Forget fence. It MUST NOT be compared numerically with any of those types.

- Same stream epoch + same sequence + same event ID/digest: duplicate/replay.
- Same stream epoch + same sequence but different event ID/digest: producer integrity conflict; quarantine and investigate.
- Sequence gap: preserve a gap marker and expose incomplete source coverage; do not invent missing events.
- Out-of-order arrival: retain source sequence and arrival/recorded time separately; buffer or process idempotently without rewriting causal history.
- New producer stream epoch: reset is permitted only through authenticated producer re-provisioning/epoch transition; it is not a way to reuse sequence numbers.

### 6.2 Ordering model

There is no universal total order across independent producers. Consumers use:
- source sequence for order within one authenticated producer stream;
- explicit causation links for causal ancestry;
- occurred_at/observed_at for source-reported temporal context;
- Brain recorded_at for durable receipt chronology;
- owner-defined canonical commit cursor for D canonical commits;
- typed downstream watermarks for E/F/G/H-owned progress.

Timestamps alone MUST NOT establish causality. Clock skew, delayed delivery and offline buffering are expected. If ordering cannot be established, preserve ambiguity and do not infer a stronger sequence.

### 6.3 Time fields

- `occurred_at`: represented event time, source asserted.
- `observed_at`: source observation time, source asserted.
- `recorded_at`: Brain durable acceptance time, Brain assigned.
- `valid_time`: interval in which a claim/state is asserted to hold; owned by the consuming domain model, not a substitute for event time.

These fields MUST NOT be conflated. Preserve timezone/precision and clock uncertainty where available. An event may be recorded after it occurred; late arrival does not make it newer in the represented world.

## 7. Revision, correction and retraction

Accepted telemetry is append-only at the semantic contract level. Corrections and retractions are new control records, not silent mutation of a prior event.

A correction MUST include:
- its own immutable `event_id`;
- target event ID and producer namespace;
- target revision or prior digest when known;
- correction sequence and source stream epoch;
- correction reason code and effective/recorded times;
- replacement/patch reference or explicit corrected fields;
- authenticated actor/producer binding.

A retraction MUST include the target event reference, reason category, time and authority. Retraction means the producer withdraws or invalidates its prior report; it does not itself prove the opposite proposition. A later corrected event may supersede the prior assertion while preserving its history.

Consumers MUST:
1. verify the correcting/retracting producer is authorized to amend the target source stream;
2. preserve original and correction lineage;
3. prevent stale replays from undoing a later correction/retraction;
4. recompute downstream derived state or mark it stale;
5. notify D/E/F/G/H/I through their owner-defined mechanisms where the correction affects canonical Memory, indexes, Context, delivery or governance;
6. distinguish source retraction from canonical Memory Forget and global erasure.

C does not define D's canonical revision/lifecycle or ForgetOperation. An event retraction is not a Forget request; a Forget request is not merely a telemetry retraction.

## 8. Environment and scope binding

Environment-dependent observations, outcomes, ToolCalls and deltas MUST carry a typed environment identity resolved through the authoritative registry/adapter binding. A free-text world name, URL, project label or user assertion is insufficient when state isolation depends on it.

The scope tuple may include tenant, user, project, Agent, Agent instance, task, session and environment dimensions as required by the operation. The authoritative semantics and permission decision remain B/I-owned. Missing required dimensions are not wildcards. A consumer MUST reject/quarantine ambiguous environment-bound telemetry rather than inheriting the previous task's environment.

Task/session changes are explicit transitions. Pending actions MUST NOT automatically carry into a new task/session unless the Agent explicitly rebinds them and the receiving policy authorizes it.

## 9. Consumer rules and lifecycle separation

Telemetry acceptance, semantic processing and canonical memory creation are separate stages:

`Submitted → Accepted → Processed/Compiled → CanonicalCommitted → Indexed`

E owns durable Accepted receipt and compiler processing semantics; D owns canonical commit; F owns index publication. A stage's success MUST NOT be inferred from an earlier stage. C's telemetry signal does not itself create a canonical Memory.

Consumers MUST preserve:
- source kind and epistemic status;
- event/observation/recording times;
- scope/environment binding;
- producer identity binding evidence;
- event ID, sequence and correction lineage;
- uncertainty and evidence limitations.

Memory content derived from telemetry remains untrusted data. It MUST NOT become an instruction, policy, tool grant or authorization decision.

## 10. Security, privacy and retention

Do not collect full CoT, credentials, API keys, secrets, unrelated prompt history or raw provider traces as a telemetry requirement. Prefer concise summaries, typed observations, tool/evidence references and explicit uncertainty. Apply payload size/frequency limits, redaction and retention policy at ingress under H/I. Redaction must not silently imply the omitted information never existed; preserve a permitted redaction marker and non-reconstructive provenance.

All telemetry, including signed Agent reports and tool outputs, is untrusted input. Integrity is not truth; authenticated source is not semantic verification. Memory prompt-injection risks remain subject to Agent/product security controls. C does not accept those risks.

## 11. Decision register

| Decision | Status | Authority / note |
|---|---|---|
| Full hidden CoT is not required | **DECIDED** | Governance P-07 and existing C baseline |
| Eight semantic types in §3 are distinct | **DECIDED** | C; consumer mapping remains owner-specific |
| Plan/Intent/PendingAction do not imply completed outcome | **DECIDED** | Governance I-06 / P-07 |
| ToolCall invocation is distinct from external effect | **DECIDED** | C semantic boundary |
| Payload identity is not authentication | **DECIDED** | I policy + H transport binding; C consumption rule |
| Source sequence is producer-stream-local | **CANDIDATE** | C proposal; E/H to confirm durable ingress/replay alignment |
| Correction/retraction are append-only controls | **CANDIDATE** | C proposal; D/E/I align canonical lifecycle/retention |
| Scope and permission remain distinct | **DECIDED** | Governance I-13; B/I authority |
| Wire names, enum encoding and envelope layout | **OPEN / H-owned** | This document is not a wire schema |
| Principal/ProducerIdentity and permission epoch | **OPEN / I/H/B-owned** | Exact branch candidates reviewed; joint approval required |
| Canonical Event/Claim mapping and retention | **OPEN / E/D/B/I-owned** | C does not freeze canonical model |

## 12. Interface impact and unresolved dependencies

| Partner | Required interface | C position |
|---|---|---|
| B | Typed Principal/ActorRef/ScopeRef/EnvironmentRef semantics | Consume B's final typed-reference decision; do not redefine |
| D | Canonical references, commit cursor, lifecycle and Forget fence | Preserve source event lineage; no canonical mutation authority |
| E | Durable Accepted receipt, source cursor/idempotency, correction processing | C supplies event ID/source sequence and typed payload semantics |
| F | Freshness, uncertainty, provenance and environment dimensions | F may consume typed signals; must not promote plans to observations/outcomes |
| G | Task/session/environment correlation and Context trigger semantics | G retains ContextVersion and membership authority |
| H | Authenticated transport principal/ProducerIdentity binding; final request evidence hook | H owns wire, transport and Adapter execution; C defines semantic evidence requirements |
| I | Issuer trust, authorization, permission epoch, revocation, retention and audit | I owns policy; C requires current authenticated binding and fail-closed decisions |

### H dependency snapshot

- Branch: `session-h-bmcp-protocol`
- Head reviewed: `fcc5103399b4c322e52d642cae5a2414969399a7`
- Candidate package: six files under `08-bmcp-protocol/`
- Status: candidate, not frozen. H's Tier 1/2/3 distinction and final-request observability requirements are compatible with this semantic contract. H's identity fields remain dependent on I/B and C event semantics; do not treat candidate wire fields as approved.

### I dependency snapshot

- Branch: `session-i-security-governance-2026-11-16`
- Head reviewed: `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb`
- Candidate package: six files under `09-security-governance/`
- Status: candidate policy, not production security approval. I defines Principal/ProducerIdentity, authorization, permission epochs, revocation and Forget governance; C does not accept residual risk or declare policy approved.

### Open dependencies

1. I + H + B: approve authenticated Principal/ProducerIdentity/ActorRef binding, issuer trust, producer registration and permission epoch.
2. H: expose verifiable authenticated binding to the telemetry consumer without treating payload identity as authentication.
3. E + H: confirm source stream epoch/sequence, idempotency namespace, Accepted receipt and duplicate/out-of-order replay semantics.
4. D + E + I: align event correction/retraction with canonical revision, Forget fence and retention; source retraction is not physical erasure.
5. G + H: align request/session/context/delivery/capability identifiers and stale-delivery suppression.
6. B: finalize typed reference semantics; no C document freezes a new canonical ActorRef or ScopeRef schema.

## 13. Acceptance criteria

- No integration requires complete hidden CoT.
- Intent, PlanSummary, PendingAction, ToolCall, Observation, Outcome, EnvironmentDelta and Uncertainty remain distinct.
- A plan or tool invocation alone cannot produce a completed Outcome.
- Payload producer/actor claims are checked against authenticated binding.
- Event ID and source sequence support duplicate, gap, out-of-order and collision handling.
- Occurred, observed and recorded times remain distinct.
- Corrections/retractions preserve append-only lineage and cannot be undone by stale replay.
- Environment-dependent signals cannot cross environment identity boundaries.
- Unauthorized, ambiguous or stale identity/scope/permission is rejected or quarantined.
- Telemetry acceptance is not represented as canonical commit, indexing or verified truth.
- Memory derived from telemetry remains untrusted data and cannot acquire instruction or tool authority.

## Phase 3 targeted remediation — identity, scope, environment and temporal binding

### 14. Complete logical identity tuple

This is C's semantic consumption profile, not a BMCP schema. H owns wire expression; I owns authentication and authorization policy; B owns ActorRef/ScopeRef domain meaning.

| Attribute | Meaning | Trust and validation |
|---|---|---|
| Authenticated Principal | Issuer-bound caller identity | H exposes authenticated transport evidence; I decides issuer trust and authorization |
| Issuer | Identity authority/federation | Must be authenticated under I policy; payload issuer is only a claim |
| Agent Identity | Registered Agent identity | Bound by H/I to authenticated producer registration; payload Agent ID is not proof |
| Adapter Identity | Registered Adapter and instance | Bound to authenticated transport, audience and capability; self-report is not proof |
| Agent Instance | Concrete execution instance | Bound to Agent identity and runtime session |
| Runtime Session | Runtime session identity/lifecycle | Bound to Agent Instance and Adapter session |
| Task Identity | Task/workflow correlation | Producer-scoped; never a principal or grant |
| Environment Identity | World/tenant/project/save-file/simulation namespace | Mandatory for environment-dependent signals; no cross-environment reuse without explicit authorized mapping |
| ActorRef | Typed actor/principal reference | B defines type; accepted only after authenticated resolution and I authorization |
| ScopeRef | Typed ownership/applicability reference | B defines type; reference is not a grant |
| Permission Epoch | Authorization policy epoch | I owns semantics/issuance; carry as opaque typed token, never compare numerically to other epochs |
| Timestamp / Ordering | occurred/observed/recorded times, source sequence, stream epoch, clock quality | Preserve source and Brain time separately |
| Telemetry Source | Agent, Adapter, Environment Adapter, Tool, User, External or Brain-derived | Bind reporter identity and source kind separately |
| Provenance / Trust Level | Origin, transformation lineage, evidence and assertion quality | Preserve source chain; producer self-label cannot elevate trust |

### 15. Three identity layers

C MUST preserve three values:
1. Transport-authenticated identity: Principal/issuer and authenticated Adapter/Agent binding established at H/I boundary.
2. Payload identity claims: Agent ID, Adapter ID, Producer ID, ActorRef, ScopeRef, Environment ID, task and session assertions. These remain untrusted until validated.
3. Brain-resolved canonical identity: normalized Principal/ActorRef/ProducerIdentity/ScopeRef association plus current authorization decision and Permission Epoch.

Mismatch between transport identity and payload claims MUST be rejected or quarantined. Never silently select the convenient value. An unresolved identity is not a low-confidence canonical identity.

B typed-reference semantics are CANDIDATE. I Principal/ActorRef and Permission Epoch policy is CANDIDATE. H envelope identity fields are CANDIDATE pending B/I/C agreement. No public schema or global identity contract is frozen here.

### 16. Telemetry class binding and authorization

| Telemetry | Required binding | Validation |
|---|---|---|
| Task State | Principal, Agent, instance, session, task, Scope, Permission Epoch, source sequence | Validate task ownership/session; task ID grants nothing |
| Intent | Task binding, source, Scope, Environment where relevant, time | Prospective report only; ingest permission required |
| Plan Summary | Intent binding plus plan ID/revision/provenance | Data-only; never proof of execution |
| Active Entities | Agent/session/task, Environment, Scope, entity refs and provenance | Resolve each ref within authorized Scope/Environment |
| Tool Call / Pending Action | Agent/session/task, tool/call ID, Environment, Scope, lifecycle state | Invocation record does not prove effect or tool authorization |
| Observation | Authenticated reporter, source identity, Environment, Scope, observed time, method/evidence | Reporter is not necessarily observed actor; evidence independently authorized |
| Outcome | Source, linked action/task, Environment, Scope, status/evidence | Agent-reported remains reported, not independently verified |
| Uncertainty | Source, related signals, Scope/Environment, time and limitation | Preserve unknown/conflict; do not coerce |
| Risk Signal | Reporter, taxonomy version, affected resource/Scope/Environment, time | Informs review; does not itself accept risk or grant authority |
| Environment Delta | Environment, base state, resulting state/observation, source sequence, Scope | Reject missing/mismatched base or unauthorized Environment |

Protected ingress validates current permission at the relevant boundary. Unknown issuer, unresolved Scope, stale Permission Epoch, environment mismatch or security-relevant sequence gap fails closed. C does not define I's authorization algorithm.

### 17. Temporal ordering

A logical record SHOULD carry producer-scoped event ID, stream ID, stream epoch, source sequence, occurred_at, observed_at, recorded_at, clock quality, and causal/correlation references. H serializes; E owns durable receipt/compilation; C defines semantics.

- Duplicate with same authenticated producer namespace, stream epoch, event identity and payload digest is idempotent. Same identity with different digest is a conflict and is quarantined.
- Out-of-order records preserve source sequence and causal links. Consumers may buffer within a bounded policy window or process as late, but cannot rewrite source order or infer causality from timestamps alone.
- Late records preserve original occurred/observed time and late arrival/recorded time. They cannot silently overwrite newer state.
- Gaps make stream completeness unknown; reconcile where supported. Do not claim complete history across a gap.
- Corrections/retractions append a new revision referencing prior event and source. They are not physical deletion and require current authorization/Forget checks.
- Clock skew preserves uncertainty; Brain recorded time remains distinct.
- Environment switch requires a new Environment Identity or explicit authorized mapping.

Invalid identity, Scope, permission, environment, integrity or ordering telemetry is rejected or quarantined and MUST NOT enter ordinary E compilation, D canonical commit, F retrieval or G Context assembly. Release requires fresh authorization and explicit validation.

### 18. Compiler and canonicalization guardrail

C telemetry is source material, not canonical Memory. E's normal ingestion, extraction, normalization, evidence/provenance and producer enforcement remain mandatory. D alone controls Canonical Memory commit/lifecycle and ForgetFence. Authentication proves source identity, not truth. No Agent-authenticated Intent, Plan Summary, Pending Action, Tool Call, Observation or self-reported Outcome may be promoted to verified fact solely due to authentication.


## Phase 3.5 identity and telemetry conformance addendum (authoritative)

See `phase-3.5-agent-identity-applied-attestation-untrusted-memory.md` §§2–3. This addendum clarifies that Transport-authenticated Principal, self-reported Agent identity, Adapter identity, Runtime Session, Task Identity, ActorRef, ScopeRef, EnvironmentRef and PermissionEpoch are distinct values with different issuers and proof ceilings. Payload identity fields are claims only. H binds transport identity; I resolves trust/authorization and PermissionEpoch; B owns typed ActorRef/ScopeRef semantics. No C field definition approves B/I/H candidates.

The mandatory telemetry profile now explicitly covers Task State, Intent, Plan Summary, Tool Call, Observation, Outcome, Uncertainty, Risk Signal and Environment Delta with identity, scope, environment, time, provenance and trust requirements. Intent/Plan are prospective; Tool Call is not Tool Result or side-effect proof; Observation is not automatically Verified. Authenticated reporting never upgrades a signal to canonical Fact/Claim. ADR-001 remains ADR-BLOCKED.
