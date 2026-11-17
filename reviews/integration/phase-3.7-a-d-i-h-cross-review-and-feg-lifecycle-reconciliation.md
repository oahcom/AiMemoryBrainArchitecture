# Phase 3.7 — A/D/I/H Cross-Review and Unified F/E/G Lifecycle Reconciliation

- Integrator: A — Principal Integration Architect
- Cross-review perspectives: A (system integration), D (canonical Memory / ForgetFence / lineage), I (Security / authorization), H (BMCP / wire and transport)
- Status: **CROSS-REVIEW COMPLETED; UNIFIED SEMANTIC AMENDMENTS RECORDED; OWNER ACCEPTANCE AND IMPLEMENTATION STILL OPEN**
- Coordination issue: #21
- No branch merge, schema freeze, implementation PASS or production activation is authorized by this document.

## 1. Exact review targets

All findings below are against these exact owner artifacts, not branch names alone:

| Owner | Branch | Commit | Blob | Artifact |
|---|---|---|---|---|
| F | `session-f-memory-runtime` | `413a22d05208e4736895d8233e35587407292fa6` | `23d00ce7ec60c2145f637e7bc9323294b25b4d77` | `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md` |
| E | `session-e-memory-compiler-2026-11-16` | `1e0fcd1e58e215f076043e6cd004892e8fc2bd50` | `ef5e735e0fad3cb1b6475ac2532b1f3419d130b8` | `04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md` |
| G | `session-g-memory-context` | `fc96973a4f5479c5ac5f4f428163a4d4002b8cd0` | `d6d18684ba8a31a538e2e719be3f6e1b715cadf8` | `06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md` |

Controlling semantic sources inspected:
- D ForgetFence / producer registration / publication gate: `03-memory-brain/forget-fence-operation-and-publication-gate.md`, Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`.
- D participant barrier / C-submit causal ordering: `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md`, Blob `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2`.
- I PermissionEpoch formal confirmation: `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md`, Blob `bae6a24fe3a374bc816993979a8fa9af52517dea`.
- I principal trust / authorization / revocation chain: `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md`, Blob `17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c`.
- H envelope/versioning candidate: `08-bmcp-protocol/message-envelope-and-versioning.md`, Blob `5547ecd78d118bd63e571e5daad87194d9b694e4`.
- H restore proof transport boundary: `08-bmcp-protocol/phase-3.6.5-h-restore-proof-transport-boundary-acceptance.md`, Blob `5a4b9a768d7396eb4be58d0d1ed3c6c0021955ea`.

## 2. Four-perspective findings

### 2.1 A — Principal Integration Architect

**Decision: ACCEPT WITH ENUMERATED INTEGRATION AMENDMENTS.**

A finds the three local ownership models directionally compatible. E is the compiler producer, F is the runtime retrieval/projection consumer and derivative maintainer, and G is the desired Context/Delivery/Applied authority. The six lifecycle dimensions are present in each local model without an explicit transfer of canonical Memory or Forget authority.

Required amendments:
1. Define one cross-owner lifecycle vocabulary while retaining owner-local states; do not force one global state machine.
2. Separate object lifecycle from evidence lifecycle and from authority/decision lifecycle. In particular, queue ACK, compiler completion, F IndexWatermark, G ContextVersion, G Applied and Storage RestoreReconciliationReceipt are distinct evidence.
3. Add a typed cross-owner handoff contract for E→F, F→G, G→H/C, and D/I enforcement. A handoff transfers references and evidence, never authority.
4. Define one conjunctive restore-serving gate over independent owner proofs. Do not create a synthetic global numeric high-water or imply a strict numeric order among COC, I, D, Storage, F and G positions.
5. Require append-only historical evidence plus separately recomputed current-use eligibility for F/G artifacts after Forget/revocation.
6. Record all unknown/crash outcomes as blocked or quarantined; do not collapse them into terminal success.

A does not accept a global lifecycle freeze yet because E's EventRef-only admission and the exact producer-class registry schema remain open, and G's Delivery-vs-provider-submit participant boundary needs an explicit amendment.

### 2.2 D — Canonical Memory / ForgetFence / Lineage Architect

**Decision: ACCEPT WITH D-OWNED BOUNDARY AMENDMENTS.**

D confirms:
- Every derivative-capable ProducerWork item must be durably registered before queue insertion, lease, protected source dereference, execution, retry/replay or publication.
- Registration and fence installation share D's linearizable admission/barrier domain. The D fence snapshot must include all earlier registered work; later affected work is rejected/quarantined.
- Complete direct/transitive dependencies are durably registered before visibility. The latest D fence and current I permission must be checked at the same final visibility boundary.
- Retry preserves ProducerWorkItemId and lineage; AttemptId/LeaseId change. DLQ, lease expiry, timeout and worker death are not terminal.
- D alone issues ForgetFence, lineage clearance and producer barrier disposition. Local owners cannot self-close D's barrier.

D requires these amendments to F/E/G:
1. **Producer class registry:** each derivative-capable producer class must be D-registered, versioned, enabled and bound to owner, source-reference classes, output/derivative classes and allowed capabilities (normal, replay, rebuild, cleanup-only). The owner documents' local Producer taxonomy is not by itself an admission grant.
2. **EventRef-only ingress:** E must distinguish acceptance of an EventRef before canonical Memory exists from derivative-capable source dereference. D must explicitly decide whether and how such ingress obtains a producer registration/ledger entry. Until that D decision exists, no EventRef-only work may be treated as admitted derivative production or bypass D's barrier.
3. **Read-only Recall exception:** F's no-registration path is valid only for a bounded, non-persistent, non-derivative read. Any prefetch, cache fill, retained excerpt, embedding, summary, graph expansion, Working Set persistence or replayable output is derivative-capable and must register before the protected read/build.
4. **G Delivery distinction:** Context materialization and retained/snapshot/delta/outbox content are G derivatives and require D dependency registration. Transport delivery itself is a disclosure/transport event, not a substitute for D producer registration. Before C crosses provider submit, the exact ParticipantIntentRef must be registered in D's causal participant barrier with the complete request/region/Context/Delivery/I binding. G cannot infer that participant intent from a DeliveryId or transport ACK.
5. **Terminality:** only a D-accepted terminal disposition plus evidence that no later publication can occur closes D's producer barrier. A local state named Completed, Acked, Cancelled or DeadLettered is not sufficient.

D's fence-request cutoff and effective fence position remain separate; participant intent before the fence request remains in the barrier, while a later intent is FENCE_WON. These rules govern D's barrier; they do not turn F queue or G delivery sequences into D positions.

### 2.3 I — Security, Identity and Governance Architect

**Decision: ACCEPT WITH SECURITY ENFORCEMENT AMENDMENTS.**

I confirms that PermissionEpoch is an opaque I-issued token within one I-registered PolicyDomainRef. It must be checked for authoritative currentness at each protected enforcement boundary. Stale, gapped, unknown, incomparable, unverifiable or indeterminate state means DENY/PAUSE, never ALLOW.

Required amendments:
1. Every producer, queue worker, recall request, source dereference, derivative registration, publication gate, Context selection, delivery/apply and restore replay must bind verifier-authenticated Issuer/Principal/Actor/workload identity, action, resource, purpose, audience, Scope, Environment, delegation chain, PolicyDomainRef and PermissionEpoch as applicable.
2. Payload-supplied `source`, `producer`, `principal`, `actor`, `scope` or `permission_epoch` values are assertions only. They cannot create identity, authorization or a trust binding.
3. PermissionEpoch is never compared with D ForgetFenceGeneration, ProducerRegistrationHighWater, COC position, Storage LSN/GID, F IndexWatermark or G ContextVersion. These values are opaque and authority-local.
4. Workers must revalidate at each protected boundary, not merely at initial queue admission. A previously valid receipt or cached ALLOW is not perpetual authority.
5. Restore must obtain current I policy-domain proofs and revocation/registry continuity. Historical valid evidence may be retained, but historical authorization is not current authorization.
6. Cross-Scope and cross-Environment operations require explicit current grants. Unknown Scope, Environment, producer identity, policy domain or delegation chain blocks the operation.
7. Global Forget completion remains I-governed; E/F/G can report only owner-local suppression, invalidation, cleanup and evidence.

I flags an important wording correction: “current permission and D fence” must mean two independent owner decisions, not one combined token or a cross-owner comparison. A local owner can cache proof only within an explicitly approved bounded validity profile; absent such a profile, it must query/verify current I state and fail closed on uncertainty.

### 2.4 H — BMCP / Protocol Architect

**Decision: ACCEPT SEMANTIC HANDOFFS; WIRE CONTRACT NOT FROZEN.**

H confirms that the three local lifecycle contracts can exchange typed references and signed/authenticated evidence, but the present envelope document remains a candidate. No new shared schema is accepted by this review.

Required amendments:
1. Every cross-owner message must carry a registered message type, schema/profile version, authenticated sender binding, recipient/audience, purpose, correlation/causation, idempotency identity and canonical payload digest where applicable.
2. Distinguish protocol version, payload schema version, ContextVersion, PermissionEpoch, ForgetFenceGeneration, ProducerRegistrationSequence, IndexWatermark, DeliveryAttempt and CapabilityEpoch. Never flatten these into `version`, `generation` or generic `cursor`.
3. Same idempotency identity + same canonical digest is idempotent; same identity + different digest is conflict. Unknown critical fields/enums, duplicate JSON keys, invalid canonical bytes, wrong audience, stale/revoked signer or unsupported security-critical schema fail closed.
4. H transports I/D/Storage/F/G evidence without minting, upgrading, interpreting or substituting its authority. A transport ACK proves receipt at its declared boundary only.
5. Restore proof envelopes must preserve issuer-owned proof families and exact opaque positions. No aggregate “restore high-water” is allowed unless each owner separately signs its own proof and the aggregate is only a manifest of references.
6. H does not equate Delivered with Materialized, Materialized with FinalRequestSubmitted, or FinalRequestSubmitted with G Applied. G applies its own predicate using C/H/I/D evidence.
7. Any wire schema additions remain a separate exact-version H artifact with interoperability vectors and security-negative tests.

H's current envelope candidate leaves dependent identity/domain fields open. Therefore this review authorizes semantic handoff amendments only, not wire schema freeze or a claim of conformance.

## 3. Unified lifecycle resolution

### 3.1 Shared lifecycle vocabulary, not one shared state machine

The following terms are canonical cross-owner concepts. Each owner may add local substates but must preserve these meanings:

| Shared concept | Normative meaning | Owner-local realization |
|---|---|---|
| Accepted | Owner has durably accepted its own input; no other owner's admission implied | E AcceptedReceipt; F/G local intent |
| Registered | D has durably admitted a derivative-capable ProducerWorkItem under an enabled ProducerClass | E/F/G hold D RegistrationReceipt ref |
| Queued | Work is durably scheduled after required registration | E compile queue; F runtime queue; G delivery queue |
| Leased/Running | One attempt currently owns execution; not terminal | E/F/G AttemptId + LeaseId/DeliveryAttemptId |
| Staged/Materialized | Private derivative or exact local materialization exists; not externally visible by itself | E private artifact; F private index/cache generation; G private Context region |
| DependenciesRegistered | D has durable complete lineage/dependency inventory for exact immutable derivative | E/F/G retain D receipt refs |
| GatePending | Current D fence and I permission plus owner-specific publication predicate not yet resolved | E/F/G local pending |
| Published/Visible | Exact owner-specific visibility transition has durably succeeded at its authoritative gate | E artifact publication; F projection activation; G Context version/delivery boundary |
| Suppressed/Invalidated | No current serving/use allowed; cleanup may remain outstanding | F/G local projection; D fence is canonical |
| Unknown/InDoubt | Outcome or authority continuity cannot be established; suppress and retain obligations | all owners |
| TerminalNoPublication | Durable proof that this work cannot publish later; D accepts it for barrier closure | owner supplies evidence; D decides closure |
| RestoredButQuarantined | Bytes/state recovered but not eligible for replay/serve | all owners |

The term **Published** is always scoped to the owner's declared artifact and gate. It never means canonical Memory commit, provider execution, Context Applied or global Forget completion unless the relevant authority separately proves that fact.

### 3.2 Ownership handoffs

1. **E → D:** E registers logical derivative work before enqueue/lease/protected source dereference; D returns registration receipt and barrier position.
2. **E → D dependency inventory:** E registers each immutable artifact's complete direct/transitive lineage before publication.
3. **F recall → G:** F returns candidate typed MemoryVersionRefs plus partition watermark, completeness/gap/truncation, provenance and currentness evidence. G re-resolves exact refs and independently checks I/D before Context membership.
4. **F internal projection:** F registers durable/replayable derivatives; pure ephemeral read-only candidate computation may use read authorization only if it creates no retained derivative or externally reusable content.
5. **G → H:** G sends an immutable Delivery attempt bound to exact ContextVersion, region digest, Adapter/session, Scope/Environment, PermissionEpoch, D fence evidence and capability epoch. H authenticates/transports; it does not decide Applied.
6. **G/H → C:** H/Adapter delivery and materialization evidence are not provider-submit evidence. C must produce the exact FinalRequestSubmitted proof. Before provider side effect, D must have the exact ParticipantIntentRef in its participant barrier, bound to the request and I authorization.
7. **C → G:** C supplies immutable final request boundary evidence. G evaluates its Full Applied predicate; G owns Applied record. Applied means exact request inclusion under predicates, not attention, understanding or successful execution.
8. **D/I → all consumers:** D supplies current fence/lineage decisions; I supplies current authorization. Neither proof replaces the other.

### 3.3 Recall and context conflict resolution

- E's “Recall” is compiler source/evidence resolution only.
- F owns runtime retrieval/candidate generation/ranking and index freshness/completeness.
- G owns Context membership/sufficiency/budget and ContextVersion.
- G must not claim a complete Context if F reports gaps/truncation or if D/I cannot validate all exact source refs.
- F Working Set, E frozen compiler input bundle and G ContextVersion are distinct typed objects with separate lifecycle and retention.
- A cache hit, index hit, compiler source result or prior Applied record cannot bypass current I/D checks.

### 3.4 Queue conflict resolution

- All queues are at-least-once work/delivery mechanisms, not authority.
- Stable logical work identity and canonical request digest survive retry. Attempt/lease/delivery-attempt identity changes per execution/dispatch.
- Same identity/digest is idempotent; same identity/different digest is conflict.
- Lease expiry, retry exhaustion, DLQ, cancel request, queue ACK and missing queue row do not close D barrier.
- Stale worker/attempt cannot publish or promote state.
- Queue restore quarantines entries until D registration/high-water, I currentness, D fence/lineage and relevant Storage/COC evidence reconcile.

### 3.5 Restore conflict resolution: conjunctive proof gate

Restore is an isolated recovery workflow, not a linear comparison of owner counters:

A. Restore bytes and owner ledgers into quarantine/non-serving namespaces.

B. Establish independent, authenticated proofs for:
- Storage restore/participant/visibility ledger and DB-incarnation continuity;
- COC committed prefix and coordinator continuity;
- I per-PolicyDomain current policy/revocation/registry high-water;
- D per-ForgetOperation/lineage fence, producer-registration and dependency inventory high-water;
- owner-local F partition/index watermark and invalidation coverage;
- owner-local G Context/Delivery/Adapter reconciliation state;
- E compiler work/dependency/publication state.

C. Validate each proof against its own issuer, audience, signature, schema, lineage and exact authority identity. The restore manifest may reference all proofs but cannot merge their numeric positions or mint a composite authorization.

D. Replay tombstones/fences and recompute current eligibility before rebuild or delivery. Rebuild only private generations; re-register/reconcile dependencies; run final owner gate.

E. Enable only the partitions, queues, Contexts and sessions whose entire required proof set is current and complete. Partial success is scoped; unknown coverage stays quarantined.

F. Reconnect creates a new authenticated session/capability binding. Old ACKs, leases, attempts, Working Sets and Applied records are not reusable permission to serve or send.

## 4. Consolidated conflict and amendment register

| ID | Severity | Conflict / gap | Unified resolution | Closure authority |
|---|---|---|---|---|
| LIF-01 | BLOCKING | Producer class local declarations could be mistaken for D admission | D versioned ProducerClass registry + durable registration receipt before derivative-capable work | D, then E/F/G |
| LIF-02 | BLOCKING | E EventRef-only ingress before canonical Memory has no fully specified D admission mapping | D must define explicit pre-canonical ingress registration semantics; until then no derivative-capable execution | D + E |
| LIF-03 | BLOCKING | G Delivery/Context materialization could be confused with D participant intent before C provider submit | Separate Context derivative registration, Delivery evidence and D ParticipantIntentRef; C submit only after exact D/I gates | D + G + C + I |
| LIF-04 | BLOCKING | Restore steps risk implying one shared high-water/order | Conjunctive, issuer-specific proof manifest; no cross-authority arithmetic or scalar | A + D + I + H + Storage |
| LIF-05 | BLOCKING | I authorization could be treated as a one-time admission check | I currentness revalidated at every protected enforcement boundary | I + E/F/G |
| LIF-06 | BLOCKING | H envelope candidate not frozen; typed fields and canonical signatures incomplete | Keep semantic contract only; H must submit separate exact-version schema and vectors | H + I + B + owners |
| LIF-07 | MAJOR | F read-only recall exception could accidentally cover retained prefetch/cache | Exception narrowly limited to non-persistent, non-derivative reads; persistent/reusable content is registered derivative | F + D + I |
| LIF-08 | MAJOR | Queue local terminal names could close D barrier | D alone accepts terminal-no-publication evidence; local ACK/DLQ/cancel/complete insufficient | D + E/F/G |
| LIF-09 | MAJOR | E/F/G Context naming/version aliases | E run input, F Working Set, G ContextVersion are separate nominal types and evidence | E/F/G + H |
| LIF-10 | MAJOR | Historical evidence could be reused as current permission after restore/Forget | Preserve history; recompute current-use eligibility against current I/D state | I + D + F/G |
| LIF-11 | MAJOR | Index/Context missing results could be treated as proof of absence/deletion | Gaps/truncation/unknown watermarks mean incomplete/unknown, never absence or Forget proof | F + G + D |
| LIF-12 | MAJOR | Cross-owner ACKs may be upgraded semantically | ACK boundary typed and explicit; H transports only; G/C/D own their evidence | H + G + C + D |

## 5. Required normative amendments to owner artifacts

The following are the unified normative clauses to be incorporated by each owner in a follow-up append-only amendment or exact-file revision on its own branch:

### F amendment
- Add explicit D ProducerClass/RegistrationReceipt precondition for every persistent/replayable derivative and every protected prefetch/cache/Working Set write.
- Define pure read-only recall exception narrowly; no retained content, no reusable derivative, no queue/replay side effect.
- State that F IndexWatermark is partition-local and cannot close D barrier or prove Forget absence.
- Restore serving gate uses independent I/D/Storage/COC proofs and F local coverage; no synthetic scalar high-water.

### E amendment
- Add D-owned EventRef-only ingress decision as a blocking interface dependency.
- Distinguish AcceptedReceipt from D RegistrationReceipt and source dereference permission.
- Make terminal-no-publication a D-accepted evidence result, not a local terminal label.
- Keep retry/recompile identity distinctions; recompile linkage must be D-approved and preserve source lineage.
- Restore must preserve immutable prepared publication tuple and quarantine unknown COC/I/D/Storage continuity.

### G amendment
- Separate Context derivative registration, Delivery dispatch/materialization and D ParticipantIntentRef before C provider submit.
- Explicitly prohibit C provider submit based solely on G DeliveryId, H Delivered/Materialized ACK or G Applied precondition.
- Applied remains G-owned exact-request historical evidence; current-use validity is recomputed after Forget/revocation/restore.
- Restore old Context/ACK/Applied into audit-only/quarantine; authenticate new Adapter session and capability before new delivery.

### D/I/H cross-owner clauses
- D defines producer registry/admission and barrier closure semantics, including EventRef-only ingress disposition and G/C participant intent relation.
- I requires current PermissionEpoch and full authenticated principal/workload/scope/purpose/audience binding at each enforcement boundary.
- H defines typed envelope/issuer/audience/canonical digest/replay/version semantics only after owners settle exact fields; no authority upgrading or schema freeze in this review.

## 6. Acceptance and implementation status

| Item | Current disposition |
|---|---|
| F local lifecycle semantic design | Reviewed; ACCEPT WITH ENUMERATED AMENDMENTS |
| E local lifecycle semantic design | Reviewed; ACCEPT WITH ENUMERATED AMENDMENTS |
| G local lifecycle semantic design | Reviewed; ACCEPT WITH ENUMERATED AMENDMENTS |
| D cross-review | ACCEPT WITH D-OWNED BOUNDARY AMENDMENTS |
| I cross-review | ACCEPT WITH SECURITY ENFORCEMENT AMENDMENTS |
| H cross-review | ACCEPT SEMANTIC HANDOFFS; WIRE CONTRACT NOT FROZEN |
| Unified lifecycle vocabulary | Candidate integration decision; amendments required |
| Shared wire schemas / callable API contracts | NOT FROZEN |
| D/E/Storage atomic registration/dependency/final publication | OPEN / BLOCKING |
| C/G/H FinalRequestSubmitted / Applied proof integration | OPEN / BLOCKING |
| Runtime/compiler/context restore conformance | NOT VERIFIED |
| Production activation / global Forget completion | NOT AUTHORIZED / NOT CLAIMED |

## 7. Next required actions

1. D publishes the EventRef-only ingress disposition and confirms producer registry + participant-intent interaction.
2. E/F/G each append the amendments above to their own branch and pin exact new blobs.
3. I reviews the resulting exact enforcement bindings and negative cases.
4. H proposes exact schemas only after the semantic fields are accepted; include canonicalization, signature, audience, replay and downgrade vectors.
5. A performs final exact-blob reconciliation and issues a separate freeze decision only when all blocking items are closed by their authorities.
6. Storage/C must independently verify crash-safe visibility and provider-submit boundaries; prose acceptance is not implementation proof.

**Final A integration disposition:** the three local lifecycle designs are semantically compatible after the resolutions in this document, but they are not yet freeze-ready. LIF-01 through LIF-06 remain blocking. Do not merge branches, freeze shared schemas, enable production work or declare Forget completion on the strength of this review.


## 8. Phase 3.7 owner-role amendment execution — 2026-11-17

**Status:** Owner-role amendment artifacts have been published on the respective owner branches and read back by exact content. This is an integration-session role execution, not evidence of independent human/agent approval by those Owners. Exact-blob A re-review and implementation remain open.

### 8.1 F/E/G local lifecycle amendments

| Owner | Branch | Commit | Blob | Artifact |
|---|---|---|---|---|
| F | session-f-memory-runtime | 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | 29e9504c75d737c2dd200ebc3306eda555f0b0ac | 05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md |
| E | session-e-memory-compiler-2026-11-16 | 1b5dc2ea6a444fb2556121d6294bc82678e52cde | 4128e867cdcbc40275c0cf527759567408f1058e | 04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md |
| G | session-g-memory-context | 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | c1de241ec69834377d9b0e24aa4770a809796d4b | 06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md |

Each artifact contains appended English and Chinese normative amendments. F narrows read-only Recall and formalizes partition evidence/restore proof; E blocks derivative execution from EventRef-only ingress pending D's explicit path; G separates Context derivatives, Delivery and D ParticipantIntentRef before C submit.

### 8.2 D/I/H authority proposals

| Owner | Branch | Commit | Blob | Artifact |
|---|---|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 30d4997f6a367ddada52e7171ff970b557bb0062 | e2d096e788eab164dc153905ab68350ad26d2ed0 | 03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md |
| I | session-i-security-governance-2026-11-16 | 011323a7a1efd1013f3b84112bd5a6db867eaf9e | 0c0c6f96d2037faf5062eafebfcee02b98a11ed2 | 09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md |
| H | session-h-bmcp-protocol | 1f6a2d3aeedc5a0eefc0d33cca62fc2eaca3f258 | b2a2648d5576511f68fdb9d87ce4388a1fedd5e9 | 08-bmcp-protocol/phase-3.7-h-lifecycle-handoff-envelope-semantics-not-frozen.md |

D now has an explicit semantic disposition: EventRef-only ingress remains quarantined until a separately versioned pre-canonical ingress contract is approved; ProducerClass eligibility and per-work registration are separate; C submit requires exact D ParticipantIntentRef. I specifies current authorization revalidation at every protected boundary and independent PolicyDomain proofs. H defines semantic envelope requirements while explicitly withholding wire freeze.

### 8.3 A integration assessment and remaining blockers

The amendments close the semantic drafting gaps for LIF-01, LIF-02, LIF-03, LIF-05, LIF-07, LIF-08, LIF-09, LIF-10, LIF-11 and LIF-12 at proposal level. LIF-04's conjunctive restore proof model is now repeated in the owner amendments, but exact proof schemas and end-to-end restore evidence remain open. LIF-06 remains open by design: H wire schema is explicitly NOT FROZEN.

A must still perform a line-by-line exact-blob re-review of all six amended artifacts and reconcile with Storage/C owner contracts. D's registry/receipt and ParticipantIntentRef callable schemas, pre-canonical ingress implementation, I verifier integration, H canonical wire schema/security vectors, D/E/Storage atomic registration-to-visibility, and C/G/H final-submit/Applied proof integration remain blocking.

No branch merge, schema freeze, conformance PASS, production activation, provider submit authorization or global Forget completion is authorized by these amendments.


## 9. A exact-blob re-review of the six amendments

A re-fetched all six owner artifacts from their named branches after publication. The returned Blob SHAs exactly match the pins in §8. All six contain substantive Chinese normative text in addition to English. Exact-blob integrity is VERIFIED.

A's semantic re-review disposition:
- **F — ACCEPT WITH ENUMERATED AMENDMENTS:** narrow ephemeral Recall exception, D registration before derivative-capable work, partition-local watermark, D-owned terminality, independent I/D checks and conjunctive restore are explicit.
- **E — ACCEPT WITH ENUMERATED AMENDMENTS:** EventRef-only ingress is quarantined pending D contract; E AcceptedReceipt is separated from D RegistrationReceipt; recompile lineage and D-owned terminality are explicit.
- **G — ACCEPT WITH ENUMERATED AMENDMENTS:** Context derivatives, transport Delivery and D ParticipantIntentRef are separated; C submit is blocked without the exact D reference; Applied remains G-owned historical evidence.
- **D — ACCEPT AS SEMANTIC PROPOSAL; IMPLEMENTATION/SCHEMA OPEN:** ProducerClass eligibility, per-work registration, pre-canonical EventRef quarantine, participant-intent binding and terminality authority are explicit.
- **I — ACCEPT AS SEMANTIC PROPOSAL; VERIFIER/SCHEMA OPEN:** current authorization revalidation, authenticated binding, independent PolicyDomain proof and no cross-authority comparison are explicit.
- **H — ACCEPT SEMANTIC HANDOFFS ONLY; WIRE NOT FROZEN:** typed envelope dimensions, idempotency conflict, fail-closed behavior, proof transport and type separation are explicit.

This re-review does not convert role-played Owner artifacts into independent Owner approvals. LIF-04 remains blocked at proof-schema and end-to-end restore evidence level. LIF-06 remains deliberately open pending H's separate exact-version wire schema and interoperability/security vectors. D/E/Storage atomic registration-to-visibility and C/G/H final-submit/Applied integration remain blocking. Storage and C exact-owner contracts have not been re-reviewed in this Phase 3.7 pass.

**A disposition:** semantic reconciliation is ready for independent Owner validation, but NOT READY FOR SHARED SCHEMA FREEZE, IMPLEMENTATION CONFORMANCE, MERGE OR PRODUCTION ACTIVATION. Issue #21 remains OPEN.
