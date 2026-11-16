# Final Inference Boundary and Applied Attestation

- Owner: Session C — Agent Integration Principal Architect
- Status: **DECIDED semantic proof boundary; CANDIDATE evidence profile; H/G/I implementation dependencies OPEN**
- Branch: `session-c-agent-integration-2026-11-16`
- Baseline: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
- Related: INT-P1-01, INT-P1-05, INT-X-04, INT-P0-04.
- Non-goals: BMCP wire encoding (H); Context membership/version (G); global authorization and risk acceptance (I); inference internals or model attention.

## 1. Purpose and normative boundary

This contract defines the strongest statement an Adapter may make about a Brain-managed Memory Context being applied to an inference request.

The **final inference request boundary** is the last controlled point at which the effective request has been fully assembled, all request transformations relevant to the inference payload have completed, and the exact immutable request is committed/submitted to the inference runtime/provider interface. The proof boundary is not:
- receipt of a Context Snapshot/Delta;
- successful parsing, validation or queueing;
- writing an Adapter-local cache or prompt template;
- inserting content into an intermediate buffer;
- a pre-submit prompt-builder callback whose output may later be changed, bypassed or discarded;
- an internal “applied version” counter;
- a provider response or model behavior.

A Full Applied claim requires evidence that the complete target managed region was present in the exact final request submitted for the identified inference invocation. It proves boundary inclusion only. It does **not** prove that the model attended to, understood, remembered, trusted, used or complied with the content. It does not prove response correctness or behavioral impact.

The Agent retains all reasoning, planning, action selection, tool invocation and safety authority. A Memory Context is data, not an instruction source.

## 2. Boundary stages and evidence levels

| Stage | Description | What can be claimed |
|---|---|---|
| Context received | Adapter transport confirms delivery receipt | Received only |
| Context accepted | Adapter validates target version, base, scope, authorization, budget and capability | Accepted only |
| Managed-region materialized | Target region exists in Adapter-controlled request assembly state | Materialized/Partial evidence only |
| Final request assembled | All relevant transformations completed; exact request payload is fixed | Assembly evidence; not yet submitted |
| Runtime submission observed | Exact final request is handed to inference runtime/provider interface and submission result/request ID is known | Eligible for Full Applied if all other evidence is valid |
| Inference executed/responded | Runtime processes request and may return response | No additional claim about attention/use |

The **submission linearization point** is the point after the final immutable request representation is formed and before control returns to a caller that could mutate or replace it. H must define how the Adapter observes and attests this point for each supported integration. If a platform exposes no reliable submit hook/request ID, Full Applied is not attestable.

## 3. Applied coverage states

The following coverage labels are semantic states, not wire enum declarations:

- **Full Applied:** every entry/byte/token in the exact target Context version's declared managed region is represented in the final immutable request submitted to the inference runtime; target request/session/delivery/capability binding and authorization evidence are valid.
- **Partial:** only an identified subset or transformed subset is materialized, or full coverage cannot be established. Must include explicit coverage gaps where safe.
- **Bypassed:** inference request proceeded without the managed region or used an unmanaged fallback.
- **Unknown:** evidence is missing, ambiguous, lost, timed out or cannot establish whether the target region reached the final request.
- **Rejected:** Adapter refused the operation before application.
- **Superseded/Expired:** the target is no longer eligible for application under G/D/I state.

Only Full Applied is eligible to set the corresponding G Delivery to Applied. Partial, Bypassed and Unknown MUST NOT be normalized to Full or to a generic success.

## 4. Capability tiers and Full Applied eligibility

C's tier semantics MUST be aligned with H's Adapter conformance package:

| Tier | Observable/control surface | Permitted application statement |
|---|---|---|
| **Tier 1 — Final-request observable** | Adapter can observe the exact final request at the runtime submission boundary, identify the submitted request, prove managed-region completeness and bind evidence to capability epoch | Full Applied may be attested per request when all proof conditions pass; otherwise Partial/Bypassed/Unknown |
| **Tier 2 — Managed-region observable** | Adapter can inspect/materialize its managed region at a controlled pre-submit hook but cannot independently prove the exact final request submitted to the runtime | Partial or Unknown only; **Full Applied forbidden** |
| **Tier 3 — Transport/basic integration** | Adapter can authenticate/negotiate/receive and possibly provide Recall results, but cannot observe managed-region application at final request boundary | Received/Accepted/Delivered/Rejected/Unknown only; no Applied claim |

Tier is a conformance ceiling, not a quality ranking. A Tier 1 integration can still produce Partial, Bypassed or Unknown for an individual request. Capability declarations alone do not establish conformance; tests and runtime evidence are required. If observability or control is lost, downgrade/degrade before making further claims.

### Reconciliation with existing C baseline

The earlier Tier 2 wording allowed attesting insertion into a request passing through a controlled middleware hook if it inspected the final outgoing representation. This is narrowed here to remove ambiguity: **unless the integration can prove the exact final immutable request was submitted to the inference runtime, it is not Full Applied**. H's current candidate defines Tier 2 as managed-region observable but not independently runtime-submission observable; this document adopts that stricter common ceiling. A middleware integration may qualify as Tier 1 only if it passes the same final-submit evidence tests, regardless of its product label.

## 5. Required binding tuple

Every application attestation MUST bind all of the following exact identifiers:

`AppliedBinding = (inference_request_id, agent_instance_id, session_id, context_id, context_version_id, delivery_id, adapter_id, adapter_instance_id, capability_epoch, boundary_id)`

Required semantics:

- `inference_request_id`: unique identifier assigned to the actual final request submission, not a turn-level guess.
- `agent_instance_id`: authenticated running Agent instance.
- `session_id`: exact Agent context/session receiving the request.
- `context_id` and `context_version_id`: G-owned Context identity and exact immutable target version.
- `delivery_id`: exact G delivery intent / H delivery instance that caused the materialization.
- `adapter_id` and `adapter_instance_id`: authenticated applying Adapter identity and concrete instance.
- `capability_epoch`: exact negotiated Adapter capability revision used to establish observability and controls.
- `boundary_id`: specific request assembly/submission hook or runtime integration point.

An attestation missing any mandatory binding MUST be Unknown or lower; it MUST NOT be Full Applied. A retry that creates a new inference request needs a new request ID and a separate attestation. A single delivery may be applied to multiple requests, but each request receives its own evidence record.

The attestation also SHOULD carry:
- target coverage profile and managed-region entry count/coverage summary;
- canonical managed-region digest and canonicalization profile;
- final request digest or privacy-safe reference to independently verifiable submit evidence;
- submitted-at time and runtime submit receipt/status;
- authenticated Principal/ProducerIdentity reference and current I permission epoch/decision reference;
- applicable D Forget fence reference/current check result;
- G target Context/Delivery status and freshness check;
- evidence verifier/version and integrity metadata.

Permission epoch and Forget fence are owner-issued typed values. C/H MUST NOT mint, increment or reinterpret them.

## 6. Evidence construction and verification

A Full Applied proof requires all checks below to succeed for the same request:

1. **Authenticated Adapter:** H proves the applying Adapter instance is bound to the authenticated transport Principal/ProducerIdentity; I's current policy permits the operation and recipient/session/scope.
2. **Exact G target:** G identifies the authoritative ContextVersion and Delivery target; the attestation references those exact IDs, not “latest” or a local counter.
3. **Freshness and suppression:** immediately before submission, the Adapter/assembly boundary confirms the delivery is not expired/superseded and no newer D Forget fence, I revocation/permission epoch or G Context target invalidates it.
4. **Managed-region isolation:** the Brain-managed region is structurally separate and the Adapter modifies only that region. Protected regions are unchanged.
5. **Completeness:** the materialized region matches the complete declared target ContextVersion under a versioned canonicalization profile; no silent truncation, omitted entry, partial operation or stale delta.
6. **Finalization:** all prompt/request transforms, templates, compaction and middleware changes affecting the request have completed. No later component can silently remove/replace the managed region before submit.
7. **Submission evidence:** the exact immutable final request is handed to the runtime/provider interface; a request ID/submit receipt or equivalent trustworthy evidence identifies that invocation.
8. **Cryptographic/integrity binding:** evidence binds the exact request, managed-region digest, target version, delivery and capability epoch; tampering or substitution is detectable.
9. **Durable record:** attestation is recorded idempotently and can be queried by request/delivery IDs. A lost ACK yields Unknown until reconciliation, not inferred success.
10. **No supersession race:** the proof is evaluated against the applicable current policy/fence and delivery ordering; late evidence cannot reactivate a superseded or forgotten target.

A digest alone is insufficient. It may prove content equality under a canonicalization profile but does not prove that the bytes were submitted. A submit callback without a stable request identifier and immutable payload binding is insufficient. An Adapter's self-assertion without authenticated identity/integrity binding is insufficient.

### 6.1 Privacy-preserving evidence

Do not log raw prompt content, raw Memory text, user input, secrets, complete model request or hidden CoT merely to prove application. Prefer:
- digest of the managed region under a documented canonicalization profile;
- digest or opaque evidence reference for the final request;
- exact non-sensitive IDs and capability epoch;
- signed runtime submit receipt or protected verifier reference;
- coverage counters and explicit omitted-entry reasons.

Hashing low-entropy sensitive text may permit dictionary reconstruction. I owns evidence classification, retention and audit policy; H/C must use keyed or otherwise privacy-reviewed evidence when an unkeyed digest would expose content. Do not claim a digest is non-reconstructive without review.

## 7. Protected regions and authority separation

The Agent's effective request may contain multiple authority zones:

| Region | Owner | Adapter may write? |
|---|---|---:|
| Platform/System instructions | Platform/runtime | **No** |
| Developer/application instructions | Application/developer | **No** |
| Agent safety policy and tool authorization | Agent/application/platform | **No** |
| User-originated input and attachments | User/application capture | **No** |
| Tool schemas, credentials and execution grants | Agent/platform/tool runtime | **No** |
| Brain-managed Memory region | Brain defines content; Adapter applies data | **Yes, only within the isolated region and authorized contract** |
| Agent-private working state | Agent | **No**, absent a separate explicit contract |

Memory, Evidence, summaries, Entity labels, provenance text and model-generated compactions are untrusted data even when authenticated or signed. They MUST NOT be assigned System/Developer roles or merged into privileged policy/tool instructions. Delimiters are useful structure but are not by themselves a security boundary; Adapter and request assembly must enforce region isolation.

The Adapter MUST NOT:
- overwrite, reorder or weaken protected System/Developer/User/Agent Policy content;
- convert Memory text into privileged role messages;
- add tool schemas, credentials, tool grants or action authorization based on Memory;
- change Agent safety policy or bypass the Agent's independent authorization before any tool/action;
- treat a memory statement that an action is “approved”, “safe” or “completed” as authorization or execution evidence.

If the integration cannot isolate a managed data region, it cannot claim Tier 1 Full Applied. If the Agent cannot maintain independent tool authorization, the integration is non-conformant regardless of tier.

## 8. Failure and race semantics

| Condition | Required result |
|---|---|
| Context received but not applied | Received/Accepted only |
| Adapter buffer updated; no final submit observed | Unknown or Partial; never Full |
| Managed region truncated or subset applied | Partial |
| Request bypasses managed region | Bypassed |
| Runtime submit outcome unknown | Unknown |
| Request ID missing or not bound to final payload | Unknown |
| Capability epoch changed before submit | Re-negotiate/revalidate; otherwise Unknown/Rejected |
| G Context target superseded | Superseded; no Full Applied for stale target |
| D Forget fence or I revocation advances before submit | Block submission/application; reconcile |
| ACK lost after valid submit | Query by exact request/delivery; remain Unknown until proof recovered |
| Late ACK arrives after supersession/revocation | Historical evidence only; cannot restore eligibility |
| Agent continues without Brain | Allowed under Agent policy; no Applied claim |

An inference already submitted is immutable from Brain's perspective. A later Forget/revocation cannot retract tokens already processed or erase provider-retained request copies. H/I own the relevant local-clear and external-recipient policies; no provider/model erasure claim is implied.

## 9. Observability and audit minimum

Record non-content evidence sufficient to reconstruct:
- exact request/session/context version/delivery/capability epoch binding;
- authenticated Adapter identity and permission decision epoch/reference;
- applicable Forget fence check;
- boundary and runtime submission outcome;
- managed-region coverage and canonical digest profile;
- attestation status and reason for Partial/Bypassed/Unknown;
- retry, supersession and late-ACK lineage.

Do not record full prompts or hidden reasoning by default. Retention and audit minimization are I-owned.

## 10. Decision register and dependencies

| Item | Status | Owner |
|---|---|---|
| Full Applied means complete managed region in exact final submitted request | **DECIDED** | C semantic boundary; H execution; G consumer |
| Applied never proves model attention/use | **DECIDED** | Governance I-18 / P-10 |
| Full Applied requires Tier 1 final-request observability | **DECIDED** | C aligned with H candidate |
| Tier 2 without final submit observation cannot claim Full | **DECIDED** | C/H |
| Exact request/session/context version/delivery/capability epoch binding | **DECIDED** | C semantics; H evidence transport; G Context authority |
| Concrete attestation encoding, signing and transport | **OPEN / H-owned** | H candidate branch |
| ContextVersion and Delivery authoritative identifiers/state | **OPEN dependency / G-owned** | G branch; no C override |
| Principal/permission epoch/revocation evidence | **OPEN dependency / I-owned** | I candidate branch; no C policy approval |
| Runtime submit hook and immutable request evidence | **TO_VALIDATE** | H + Agent runtime integration |
| Evidence retention, digest privacy and external provider policy | **OPEN / I-owned** | C makes no risk acceptance |

## 11. Acceptance criteria

- Applied evidence binds exact request, session, ContextVersion, Delivery and capability epoch.
- Full requires final-request observability and proof of actual runtime submission.
- Tier 2 and Tier 3 cannot claim Full Applied.
- Missing or ambiguous evidence produces Partial, Bypassed or Unknown, never inferred success.
- Applied is not model attention, comprehension, use, response quality or behavioral compliance.
- Memory is isolated as untrusted data.
- Protected System/Developer/User/Agent Policy regions remain unchanged.
- Tool authorization remains independent and Agent-owned.
- Forget/revocation/supersession wins over stale delivery and late ACK.
