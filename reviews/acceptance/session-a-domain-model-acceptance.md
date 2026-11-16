# B Owner Acceptance — A Context Optimization / Observation Archive

- Owner: B — Domain Model Architect
- Decision: **ACCEPT WITH CONDITIONS**
- Reviewed A integration commit (requested pin): `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f`
- A branch was re-queried; live branch HEAD at review time: `a480a713db358b30dc4cf7c9157025b3c116e439`. This decision is pinned to the requested commit, not silently rebased to the live tip.
- B branch: `session-b-domain-model-phase3`; observed HEAD before this commit: `30580b094b9cb0ac747ff2849bec5ad68db3e272`.

## 1. Exact A artifacts reviewed

| Path | Blob SHA |
|---|---|
| reviews/integration/nvidia-context-optimization-system-integration-review.md | `b53db1ecb7830a7f1057d09c8ef73aceab942cea` |
| reviews/integration/context-optimization-system-contract-candidates.md | `55257bdf85a56a78df96b797b063bc49d91f5a6d` |
| reviews/integration/context-optimization-conformance-plan.md | `1c941c3e55be1e539a76ef89f297c168296c7db2` |
| reviews/integration/context-optimization-owner-decision-register.md | `36581cf286ddf2516f571eb823fddc9cf8707d80` |

A review identifies the F Archive / G Context split, explicitly labels cross-owner freeze unauthorized and Rust blocked. The conformance plan is PROPOSED / NOT RUN. These are not runtime acceptance claims.

## 2. B baseline and authority considered

Reviewed B `02-domain-model/typed-reference-and-scope-semantics.md` (Blob `e9a6bd21e06bc02a5208619f5a949217860b1c00`) and `02-domain-model/typed-reference-registry.md` (Blob `08af297cb010f7e6ac5e3f29daa4469be112e12e`) at the observed B branch. B's existing rule is decisive: a reference names an identity/version; it is not a credential, permission, authorization receipt or proof of existence/currentness. H owns serialization; I owns trust/authorization; F/G own their runtime/context identities.

## 3. Formal decision and accepted boundary

B accepts the *conceptual domain boundary only*, subject to the conditions below:

1. **ArchiveObjectManifest / ArchiveLocator** are F-owned runtime/archive identities. ArchiveLocator MUST pin one immutable archive object revision, content hash, source identity/revision and selector coordinate system. It is not a domain authorization grant.
2. **ContextObservationReference** is a G-owned, ContextVersion-bound relationship/edge to an exact ArchiveLocator/source revision. It is not the same type or identity as ArchiveLocator and must not be cast to it.
3. **Observation** is a source-qualified occurrence/record, not automatically a proposition or canonical Memory. It requires stable identity if independently referenced, plus source, observed/recorded time and revision identity.
4. **Evidence** is a typed provenance/attestation relation to an exact source/version/range. A ReadReceipt proves only that F returned specified bytes/range under recorded checks; it does not prove semantic truth, independent verification, authorization for future access, or Agent application.
5. **Derived Summary** is a non-authoritative, immutable derived artifact with its own identity/version, derivation profile, source revision set and lineage. It remains epistemically no stronger than its inputs unless an explicit B/D/E-governed transition says otherwise.
6. **Canonical Memory** remains D-governed. Neither Archive capture, TSS nor compaction promotes content to Canonical Memory.
7. **TSS** should be a G-owned typed Context projection, versioned by ContextVersion; it is not a new canonical domain aggregate and not private Agent reasoning/CoT. Its internal field schema remains G-owned pending B review of epistemic/temporal mapping.
8. **CompactionLineage** and **LossLedger** have domain-significant audit meaning (source-to-retained/omitted mapping, version, reason, fidelity result, rehydration pointer), but their storage/event DTOs remain G runtime implementation details until a stable semantic contract is approved.

## 4. Required identity, version and governance fields

For domain-visible references and provenance edges, require as applicable:
- issuing authority / namespace, fixed discriminator, opaque non-reused object ID;
- immutable version/revision ID where bytes or source state can change;
- owner Scope and applicability ScopeRefs, kept distinct from identity;
- authenticated Principal/Actor attribution via trusted binding (never caller self-assertion);
- source kind, source identity, source revision/hash and selector coordinate system;
- observed_at, recorded_at, and source-valid-time where applicable (do not collapse clocks);
- epistemic status (Reported / Inferred / Verified or the B-approved vocabulary), confidence/quality metadata with defined semantics, and explicit provenance;
- lifecycle/currentness/suppression state as an authority-owned result, not inferred from ID;
- retention/Forget lineage references and permission checkpoint metadata where needed for protected operations.

A locator's expiry or a source revision change makes the old reference STALE/EXPIRED; it does not mutate the old identity or silently retarget it. A forgotten identity is never reused; access may be suppressed/unavailable under D/I policy.

## 5. Runtime implementation details, not stable B domain types

RecallSession, ReadCursor, ReadBudget, cache entry, page map, index watermark, retry/attempt ID, transport delivery ID, adapter capability epoch, ACK, token budget counters and physical archive shard are module/runtime or protocol details. They may carry typed references but do not become B domain aggregates merely because they appear in DTOs. H defines wire schema; F/G define runtime DTOs.

## 6. Cross-owner findings

- **B↔C:** ContextObservationReference / source refs identify what was selected; Agent Applied Evidence is a separate C/H/G attestation tied to exact final request and ContextVersion. No reference or ReadReceipt proves application.
- **B↔E:** compiler artifacts must retain exact typed source references and epistemic lineage. Canonical registration is D/E authority, not implied by a domain ref.
- **B↔H:** B accepts semantic discriminators and namespace/version distinctions only. H wire field names, encodings, enum values and compatibility are NOT accepted/frozen by this decision.
- Object-name collision warning: “reference”, “receipt”, “version”, “evidence”, “summary” are not interchangeable across B/F/G/H/C.

## 7. P0 / P1 and conditions

**P0**
- No joint F/G/D/I/H/C path yet demonstrates that a source ref remains authorized/current from recall through Context commit and final request submission, including Forget/revocation races.
- No executable conformance suite exists in this architecture repository; A's plan is NOT RUN.

**P1**
- Formal B vocabulary for Observation/Evidence/DerivedSummary and epistemic transitions must be added before treating these as reusable domain contracts.
- TSS schema, lineage/loss semantics, source-time model and ref invalidation mapping require G proposal and B review.
- Exact reference-to-wire mapping and schema compatibility require H decision; exact Principal/Scope/Permission policy requires I.

Conditions: B's acceptance applies only to the object/authority separation and reference semantics in §3–4. It does not approve A's full F/G API, G TSS schema, H BMCP schema, E publication API, security policy or runtime behavior.

## 8. Negative conformance requirements (all NOT RUN)

All 15 scenarios below are required; no runnable test evidence was found in this architecture-only review.

| # | Preconditions / sequence | Expected protocol + Agent behavior | Retry / evidence | Test status / owner |
|---|---|---|---|---|
| 1 | F returns ReadReceipt; no delivery follows | Receipt remains read fact; Agent must not claim applied | No retry as Applied; retain range/hash/receipt | NOT RUN; F/B/C |
| 2 | Adapter submit fails, retry starts | Same logical delivery, new attempt; no duplicate semantic application | Idempotency key+digest, attempt lineage | NOT RUN; C/H |
| 3 | Agent applied v; G creates v+1 | Historical application retained; v becomes superseded for new use | Preserve old Applied evidence + supersession | NOT RUN; G/C/H |
| 4 | Offline queue contains old v | Reconnect suppresses stale item before replay | Current fence/epoch/version proof | NOT RUN; H/G/I |
| 5 | ACK says success but Applied evidence absent | No Applied conclusion | Reconcile; retain ACK stage and missing-proof reason | NOT RUN; H/C/G |
| 6 | Cursor resumed under different ContextVersion | Reject cursor; open new authorized session | Session/revision/selector binding | NOT RUN; F/H |
| 7 | Source revision changes after reference minted | Old ref STALE; no silent rebinding | Old/new source revision hashes and invalidation | NOT RUN; F/G/B |
| 8 | Compaction summary submitted as canonical derived | Reject absent D registration + E gate | Artifact lineage and denied publication trace | NOT RUN; E/D/G |
| 9 | Publication has missing ancestor | Gate rejects / remains private | Complete dependency digest/receipt | NOT RUN; E/D/Storage |
| 10 | Forget then old derivative replayed | Suppress/quarantine; never republish | Fence generation, lineage, gate receipt | NOT RUN; D/E/I |
| 11 | Client continues after STALE response | Agent/Adapter must stop using stale data | Error + local suppression record | NOT RUN; H/C/F/G |
| 12 | Duplicate recall/delivery request | Idempotent result; no duplicate application | Stable request/delivery key, digest, dedup record | NOT RUN; F/H/C |
| 13 | Timeout leaves outcome ambiguous | UNKNOWN, not success/failure guess | Query/reconcile by stable operation ID | NOT RUN; H/C/G |
| 14 | Permission revoked in existing session | Fail closed at next read/delivery boundary | Principal, PermissionEpoch, denial trace | NOT RUN; I/H/F/G |
| 15 | Recall succeeds, delivery fails | Recall result does not imply Context application | Separate Recall and Delivery state/evidence | NOT RUN; F/G/H/C |

## 9. Cross-owner dependencies and gate

Required: F owns archive identity/revision/read facts; G owns Context edge/version/lineage/TSS; C defines final request boundary; H defines wire and truthful transport ACK; E/D define canonical derivative gate; I defines identity, authorization, retention and revocation; Storage proves durability/recovery.

**Interface freeze:** NOT APPROVED. B accepts domain boundary semantics only, not wire/schema.
**Implementation:** NOT AUTHORIZED. No Rust or runtime implementation approval.
**Next gate:** G submits exact typed TSS/lineage semantics; F/G submit one pinned Recall/Context reference contract; H maps B types to versioned wire schema; C/H/G close Applied evidence semantics; D/E/I/Storage close Forget/publication and recovery.
