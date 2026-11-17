# Phase 3.6.12 — Storage / C / H Exact Version Binding Manifest

- Owner perspective: Storage coordination; C and H verification inputs are recorded as exact artifacts, not impersonated approvals.
- Status: PROPOSED INTEGRATION BINDING — A FINAL REVIEW REQUIRED
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT DEPLOYED
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`

## 1. Exact artifact pins

| Role | Artifact | Exact blob | Status |
|---|---|---|---|
| Storage | COC Durable Log, Participant Registry & Recovery Protocol (contains normative §§15–17) | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Fetched from Storage branch and inspected |
| Storage companion | Storage Design v3.2.2 / Recovery Cutoff Ordering Amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Exact blob referenced by COC §16.1 and §17; companion file was not independently re-fetched in this pass |
| H | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.5.schema.json` | `164ec3c436558d5d93032edc51e127d15e03db4d` | Fetched from H branch and structurally inspected |
| C | C Provider Outcome composable normative source set | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` + `45a48249717c8cddb07ab96197730ef93d406c22` + `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` + `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` | Located in exact C branch tree, fetched by Blob SHA; C exact-owner delegated decision recorded in Blob `1ac84f2b2991e414e2447d16a746ac19328978ed`; ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS |
| Historical COC source | `8ac17816476f280ab6fb3afca0688aa03e37de1d` | historical source blob | Superseded by Storage protocol §§15–17 for ordering and digest semantics |

The Storage v3.2.2 amendment blob `9704d110a06d0c2ee98be960054e0396d0b68546` was fetched directly via GitHub blob retrieval and its complete 13,682-character content inspected. It is titled “Phase 3.6.4 — COC Recovery Cutoff Batch / Participant Manifest Ordering Amendment”; it explicitly binds base COC `8ac178...`, Storage Design v3.1 `d5bdc72...`, and H schema 1.0.5 candidate. It defines the three-digest model and two-phase commit order. The later COC protocol blob `5b950a3...` extends this with §17 dual-ledger union membership and supersedes narrower §§15–16 interpretations. Do not treat `9704d...` as a standalone current complete bundle: it is the ordering amendment source, while `5b950a...` is the later integrated COC protocol. The H schema artifact revision 1.2.5 while protocol-family `schema_version` remains 1.2.0; distinct concepts.

## 2. Normative Batch / Manifest sequence

Storage COC §§15.1–15.2 require this order:

1. I/D/C close their respective gates and freeze owner-local snapshots/high-waters.
2. Establish the exact quorum-committed COC prefix P and anti-rollback anchor.
3. Enumerate and precompute the complete canonical Participant Manifest against P; independently re-read it. This is a staged immutable payload, not yet an authoritative committed record.
4. Commit `COC_RECOVERY_CUTOFF_BATCH`, binding the stable ManifestId, manifest content digest, count, enumeration high-water, prefix and owner snapshots.
5. Commit the separate Participant Manifest record, referencing the exact preceding Batch position/digest and repeating the exact epoch/prefix/ManifestId/content digest/count/high-water.
6. Linearizably read back both records and verify the complete pair before entering participant reconciliation.
7. Reconcile each member; each owner independently issues only its own Gate Release.
8. Append `RECOVERY_EPOCH_COMPLETED` only after all required owner releases and reconciliation evidence are durable.

The API contract rejects batch append without the already computed manifest identity/digest and complete frozen owner snapshots. Manifest append is idempotent on stable batch identity plus manifest identity/digest. Lost ACK recovery must use exact-key lookup and readback, not a second identity.

## 3. Digest dependency — no circular reference

Storage COC §§16.1–16.3 distinguish:

- `ParticipantManifestContentDigest`: precomputed over the canonical immutable manifest-content projection; excludes the future Batch reference and final record proof.
- `RecoveryBatchDigest`: covers the batch payload, including ManifestId and ParticipantManifestContentDigest.
- `ParticipantManifestRecordDigest`: covers the final committed Manifest record, including exact Batch reference/digest and content digest.

Required dependency:

`ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest`

The Batch MUST NOT bind the future Manifest Record digest. The Manifest Record MUST NOT precede its Batch. Owner release and epoch completion bind the exact committed Batch and Manifest record references, positions and entry digests, as well as the appropriate content/record digest values.

## 4. H schema 1.2.5 structural verification

The exact H schema was parsed and checked for these message contracts:

- `COC_RECOVERY_CUTOFF_BATCH` requires prefix, I/D/C owner snapshots, ManifestId/digest, participant count, enumeration high-water and quorum/COC record proof fields.
- `COC_PARTICIPANT_MANIFEST` requires exact Batch reference/position/entry digest, ManifestId/digest, count, enumeration high-water and participants.
- `OWNER_GATE_RELEASE_ATTESTATION` requires exact Batch and Manifest record references, positions and entry digests, owner gate generation, request/admission high-waters, set digests and ledger roots.
- `RECOVERY_EPOCH_COMPLETED` requires exact Batch/Manifest references and digests, reconciliation root and owner release references.
- Participant union uses distinct COC participant and owner-local admission variants; an owner admission may carry an explicit nullable COC ParticipantIntentRef plus absence reason.
- C Provider Outcome message requires CSubmitOutcome identity/digest, provider outcome and evidence references, provider/adapter/idempotency identity, final request boundary and request digest, owner-admission identity/digest, owner ledger/version/sequence/high-water/root, and COC participant/absence binding.

Structural schema validation alone does not establish digest recomputation, cross-record equality, quorum ordering, signature trust, completeness, or provider side-effect truth. Those remain semantic verification requirements.

## 5. C Provider Outcome verification requirements

The H schema 1.2.5 `provider_outcome` enum is exactly:
`HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`.
Do not replace these wire values with semantic paraphrases such as “invoked with receipt”. The schema also exposes `provider_outcome_evidence_ref`, `provider_no_handoff_proof_ref`, `not_invoked_proof_ref`, `unknown_reason_ref`, and a 64-hex `c_submit_outcome_digest`.

C-owned semantic requirements, to be checked against C's exact owner artifact before acceptance:

- `HANDOFF_ACCEPTED`: must prove the exact final request crossed the provider handoff boundary and bind provider/adapter, idempotency key, final request boundary, request digest and immutable CSubmitOutcome. It does not prove downstream durable Memory Brain visibility.
- `HANDOFF_REJECTED`: must prove an authoritative provider rejection for that exact request; distinguish rejection before side effect from rejection after possible side effect. If side-effect absence is not authoritative, classify UNKNOWN/IN_DOUBT rather than safe retry.
- `NOT_INVOKED`: requires authoritative no-handoff proof; timeout, absent request row, lost ACK or worker death is insufficient.
- `UNKNOWN` / `IN_DOUBT`: nonterminal; preserve the exact attempt and evidence, block retry-as-new-operation and keep affected gates closed until authoritative same-key lookup/reconciliation resolves it.

Storage COC §§17.1–17.7 require C's reservation, provider-attempt and provider-outcome high-waters in the frozen C admission ledger; every applicable C admission must enter the union manifest even without a COC ParticipantIntentRef. C alone creates CSubmitOutcome. Batch/Manifest membership, Storage resolution, I terminality, D clearance, H ACK and COC quorum proof cannot synthesize provider success. C's provider gate remains closed through S2/S3 and until S4 exact Batch/Manifest pair readback succeeds. Provider-specific same-key lookup/idempotency is an activation prerequisite.

The schema field-presence check is not proof that outcome-dependent evidence conditions are implemented. The semantic validator must reject missing/contradictory proof refs and must not treat HANDOFF_REJECTED as NOT_INVOKED without proof that no external side effect occurred.

## 6. Blocking conditions and review boundary

1. H schema 1.2.5 structurally represents the Batch-before-Manifest-record order, three distinct digests and dual-ledger union member types. Outcome enum and proof-reference fields were inspected; H owner semantic acceptance and interoperability-vector execution remain pending.
2. C Provider Outcome fields are present in H schema 1.2.5, and Storage COC §16.4/§17 assigns C the gate and owner-local admission accounting across the Batch/Manifest interval. The former C source-discovery blocker is closed by the exact C source set and delegated C decision pinned below. H schema 1.2.5 remains a historical structural pin; C's review also references a 1.2.7 signature-profile amendment, which A/H must pin as the current H bundle before freeze.
3. The Storage v3.1 companion blob is cited by the current COC protocol but was not independently fetched in this pass. A must verify that pin before freezing the bundle.
4. Any schema or protocol change creates a new exact bundle and requires affected-owner re-review.

No implementation, conformance test execution, provider sandbox verification, production activation, physical erasure, or Global Forget Completion is claimed. This document records an architecture-level exact-version binding candidate only.


## 7. Follow-up exact-blob verification (2026-11-17)

Storage amendment blob `9704d110a06d0c2ee98be960054e0396d0b68546` was fetched directly by SHA using GitHub's blob retrieval and inspected in full (13,682 characters). Its content confirms the exact title, three-digest projection, non-circular dependency, and two-phase Batch-before-Manifest-record sequence. It explicitly names Storage Design v3.1 blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca` and base COC blob `8ac17816476f280ab6fb3afca0688aa03e37de1d`. The later integrated COC blob `5b950a3a29bd7a5276b92a49a9114d700718b987` adds §17 dual-ledger union-manifest requirements.

C owner artifact discovery remains unresolved: the C branch's prior review report is present, but the canonical C Provider Outcome contract/schema source could not be located or pinned by exact path/blob in this pass. Consequently C's conditional boundary review must not be promoted to an exact-version Owner acceptance. This is an explicit freeze blocker, not an inferred approval.


## 8. Follow-up — C source discovery, exact pin and Storage cross-check (2026-11-17)

### 8.1 Exact C branch evidence

The C branch was resolved to HEAD `afacd82a4bf03118f40cd010bff6060837132985`; its recursive Git Tree was fetched by exact tree SHA `f5ac9546c6aa7c13443485e50db92a10af320c77`. The following normative source files were present in that tree and fetched by their exact Blob SHAs:

| C source | Path | Blob |
|---|---|---|
| Final Request Evidence Contract | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` |
| C-submit / I-authorization / D-ForgetFence causal-order contract | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` |
| C owner-local admission / recovery-release amendment | `07-agent-integration/phase-3.6.9-c-owner-local-admission-gate-recovery-release-amendment.md` | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| Concrete Provider Egress Gate Adapter contract | `07-agent-integration/provider-egress-gate-adapter-contract.md` | `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` |

Corroborating C reviews:
- Phase 3.6.11 Provider Outcome × Recovery Batch/Manifest: Blob `19519a9dabe8aea66897c01493ab5b65ed8af4aa`.
- Phase 3.8.2 RecoveryJoin / provider-side-effect review: Blob `a7b57bd5531222559666f0f1d9df59a259cde61a`.
- Phase 3.8.3 exact Provider Egress Gate review: Blob `5a27f79087d3a5e01dd23e818d8c7ea0fdb61d1d`.

C's delegated exact-owner binding decision:
- Path: `07-agent-integration/phase-3.8.4-c-provider-outcome-exact-owner-binding-decision.md`
- Commits: `fd245b83865bbf7192e8b24366b89590ade3f3fc` (initial decision), `f756a5beeaa596d1fa6f791a0adbca402206ccbc` (H current-head qualification)
- Current Blob: `1353572f7d5655e3007b2fb5b3f10066f483e6bb`
- Decision: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**.
- Provenance: assistant-authored role simulation at the user's direction; not an independent human C Owner signature.

The canonical C authority is a composable normative source set, not one standalone file. The earlier statement “C owner artifact not located” is superseded. The review report `ce191163...` remains a review artifact and is not substituted for the normative C sources.

### 8.2 Storage independent cross-check

Storage's independent cross-check of the C source set confirms the following integration invariants are mutually consistent with Storage COC §§15–17 and the exact Storage v3.2.2 ordering amendment:

1. C owner-local admission inventory is distinct from the COC participant prefix. Every admitted C operation is represented in C's frozen ledger; where no COC ParticipantIntentRef exists, the manifest carries an explicit null plus reason rather than fabricating a COC participant.
2. CSubmitOutcome is C-authored provider-boundary truth. COC Batch/Manifest membership, Storage Prepared/COMMITTED/PublicationReceipt, I COMMIT_WON, D clearance and H ACK cannot synthesize provider success.
3. C distinguishes provider handoff from COC admission/reservation and from Storage visibility. `HANDOFF_ACCEPTED` is not durable Memory Brain visibility, model execution, user delivery or G Applied.
4. Provider invocation/retry remains blocked after Batch or Manifest commit alone; C requires S4 exact pair readback and semantic join before recovery reconciliation.
5. Ambiguous handoff remains UNKNOWN/IN_DOUBT and is reconciled only under the same immutable request/attempt and provider idempotency key. Generic exactly-once is not assumed.
6. Storage does not author or release C Provider Outcome. C's exact semantic acceptance is recorded as a delegated role decision and remains bounded by provider-specific and runtime evidence exceptions.

### 8.3 Remaining freeze blockers

- Provider-specific idempotency namespace, same-key authoritative lookup, receipt authenticity and no-handoff proof must be established for each production provider.
- C durable Gate/ledger serialization, multi-replica race behavior, crash/restart/restore and real transport Adapter conformance remain unimplemented/unverified.
- H schema 1.2.5 is only the earlier exact structural pin; C review references schema 1.2.7 signature-profile changes. A/H must pin and validate the current H schema + semantic validator + canonical-byte/signature fixtures as one exact bundle.
- A must perform final cross-owner integration review against current I/D/Storage/H heads and preserve all owner-specific release authorities.
- No implementation, provider sandbox test, production activation, universal exactly-once, Full Applied or Global Forget Completion is claimed.

This update closes the document-discovery blocker only. It does not close implementation, provider-specific, H-currentness, conformance or final A acceptance gates.


## 9. Follow-up — current H branch head and C re-review boundary

H branch `session-h-bmcp-protocol` was resolved to HEAD `80ba6748f4c7442f162102a30cfefacefdec0db9`. Its recursive tree confirms the current schema artifact:
- Path: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.11.schema.json`
- Blob: `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Artifact revision: 1.2.11
- On-wire protocol-family version declared by the schema: 1.3.0

The exact schema blob was fetched and inspected. It retains the typed union of COC participants and I/D/C owner-local admissions and Provider Outcome enum support. This does not prove semantic validator completeness or provider truth. C's exact-owner decision was amended at Blob `1353572f7d5655e3007b2fb5b3f10066f483e6bb` to state explicitly that C has NOT yet accepted H 1.2.11 as a complete cross-owner bundle. C/H must review the current schema together with the matching semantic validator, signature/canonicalization profile, canonical-byte fixtures and interoperability vectors before wire freeze.

Storage's binding therefore records:
- C source-discovery blocker: **CLOSED** (exact C source set found and pinned).
- C delegated semantic decision: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**, scoped to its exact source set and previously reviewed mapping.
- Current H 1.2.11 cross-owner acceptance: **OPEN**.
- Provider-specific implementation/conformance and A final integration acceptance: **OPEN**.


## 10. Exact C/H cross-review of current H schema 1.2.11 (2026-11-17)

### 10.1 Exact reviewed pins

| Owner | Artifact | Exact Blob | Result |
|---|---|---|---|
| H | Unified COC/JF-10/Provider Outcome schema artifact 1.2.11 (wire family 1.3.0) | `4f1e103ab4b2ac961d77179dba0b65093532ea40` | Exact schema inspected; structural candidate only |
| H | Phase 3.6.10 semantic validator contract | `4c5c3771575979061e674e40f1f5f3d9b4645bd9` | Earlier proposed contract; not an exact 1.2.11 semantic acceptance |
| H | Phase 3.6.10 exact-version validator decision | `1de7d30f3ca81bc579b396acb0f05e2ead5fe9dd` | Earlier 1.0.4 candidate decision; not current 1.2.11 freeze |
| H | Phase 3.8.3 H/I crypto wire mapping (schema 1.2.8) | `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` | I-specific mapping; not C signature profile and not aligned to 1.2.11 / wire 1.3.0 |
| H | Python wire test | `1a4e754ba9bfa57eb973c6d39731e9f89443b323` | HRC-TEST-v1 / recovery-cutoff 1.0.4 test profile |
| H | JS reference | `992585d3bc323dc0224d0075ef14abd992980f65` | Bespoke test canonicalizer, not production JCS proof |
| H | Wire vectors | `cc7e98c729db8d9f615e17a9542b3cb63f459922` | Three generic recovery/join vectors; no C Provider Outcome cases |
| C | Phase 3.8.5 exact H 1.2.11 Provider Outcome cross-review | `55ebbf340e816b7df5faf4299187bff257a81a92` | Conditional structural acceptance; semantic/wire freeze blocked |
| H | Phase 3.8.4 exact H 1.2.11 Provider Outcome cross-review | `aae5dcb1d0c1ad95c306e469e6fbd96aef67b309` | Structural candidate accepted; semantic/wire freeze blocked |

C review commit: `3e86abf9459c621a19ed986734ddcdbf0ae8a7b7` on `session-c-agent-integration-2026-11-16`.
H review commit: `300a590dd181173e6e8fe22ee3ea937efc18163e` on `session-h-bmcp-protocol`.

### 10.2 C/H cross-review findings

The 1.2.11 schema structurally contains `C_PROVIDER_OUTCOME_RECORDED`, exact outcome enum `HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`, immutable outcome ref/digest, provider/adapter/idempotency-key references, final request boundary/digest, outcome-specific evidence refs, C owner admission/ledger/high-water/root, COC record proof and nullable COC ParticipantIntentRef with an explicit absence reason.

The schema's outcome conditionals are useful: ACCEPTED requires reservation/provider request/receipt/evidence; REJECTED requires reservation/no-handoff proof/evidence; NOT_INVOKED requires not-invoked proof and excludes provider receipt; UNKNOWN/IN_DOUBT requires a reason. These are structural requirements only.

C identifies unresolved semantic requirements: explicit or transitively proven `CGateGeneration` and provider-attempt identity/generation; authoritative same-provider/account/namespace same-key lookup bound to the same immutable attempt/request digest; no-handoff and rejection truth; append-only outcome immutability and contradictory-field rejection; and a C-specific signature profile/projection. H independently identifies the need for a 1.2.11 / wire-family 1.3.0 semantic validator, current envelope/crypto mapping, C-specific signature projection, canonical-byte fixtures and C Provider Outcome vectors.

The available H interop test artifacts are explicitly a recovery-cutoff 1.0.4 / HRC-TEST-v1 profile. Python uses sorted-key JSON serialization and JavaScript uses a bespoke canonicalizer; neither establishes RFC 8785 JCS or production signature bytes. The three visible vectors do not test Provider Outcome semantics, same-key recovery or C gate races. No exact 1.2.11 C-PO execution evidence was established in this review.

### 10.3 Binding disposition and blockers

- H schema 1.2.11: **PINNED; STRUCTURAL CANDIDATE ONLY**.
- C cross-review: **CONDITIONAL STRUCTURAL ACCEPTANCE; SEMANTIC AND WIRE FREEZE BLOCKED**.
- H cross-review: **STRUCTURAL SCHEMA ACCEPTED AS CANDIDATE; SEMANTIC/WIRE FREEZE BLOCKED**.
- H 1.2.11-specific semantic validator and decision: **OPEN**.
- C gate-generation/provider-attempt transitive binding and provider-specific idempotency/lookup semantics: **OPEN**.
- C-specific signature profile/projection and current H envelope alignment: **OPEN**.
- 1.2.11 canonical-byte/signature/provider-outcome vectors and executed cross-language/real-Adapter conformance: **OPEN**.
- A final integration acceptance: **OPEN**.

This section supersedes any earlier implication that the historical H 1.2.5 or 1.2.8 pins constitute the current H wire bundle. Historical sections remain retained as provenance. The current exact H schema pin is 1.2.11 Blob `4f1e103...`; it is not a cross-owner wire freeze.

No provider implementation, executed conformance, production activation, universal exactly-once, Full Applied or Global Forget Completion is claimed. C/H decisions are delegated role simulations authored at the user's direction, not independent human Owner signatures.


## 11. C/H/I Provider Outcome semantic and crypto amendments (2026-11-17)

### 11.1 Exact owner artifacts

| Owner | Artifact | Exact Blob | Disposition |
|---|---|---|---|
| C | Phase 3.8.6 Provider Outcome Gate/Attempt/Idempotency Amendment | `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4` | PROPOSED C semantic amendment; NOT TESTED |
| C | Phase 3.8.7 review of I C-scoped crypto proposal | `794d1dc49f034152407e3a42ba5ac937ea3539f8` | Candidate construction accepted only; I approval and H wire mapping open |
| I | Phase 3.8.4 C Provider Outcome crypto profile addendum | `1bcddbaaa4a9ca730d492a6554941becac305668` | PROPOSED AIMBA-C-CRYPTO-1.0; not registered/approved/frozen |
| H | Phase 3.8.5 exact 1.2.11 Provider Outcome semantic validator contract | `26e529327ae15f57b8169cdec48d9c18fef12097` | PROPOSED; not implemented or executed |
| H | Schema artifact 1.2.11 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` | Structural candidate only |

C amendment commit: `b30d3b779adec2b7c64dc3267c21c5f281ad47eb`.
I addendum commit: `fa4bd5e190f0fdb4ace658969433bdb4ef8f6838`.
H validator latest commit: `ce8ccd5fb319d07911cf68a4c385b2a99eaf4e8e`.

### 11.2 Normative cross-owner alignment

C now specifies the immutable attempt tuple: C outcome, C admission/digest, C gate/generation, provider attempt/generation, provider/account/adapter/endpoint/region, idempotency namespace/key, final request boundary/digest and optional COC intent/reservation. Gate close and final egress commitment must share one durable linearizable authority. Close-wins prevents any older uncommitted send; egress-wins requires the exact attempt to appear in the close in-flight set. A crash after egress commitment without transport result remains UNKNOWN/IN_DOUBT.

Provider same-key lookup must prove the exact same provider/account/endpoint, namespace/key, attempt/generation, request boundary and digest. Provider-specific retention, lookup consistency and receipt authenticity are mandatory capability facts. Generic exactly-once is not assumed; expired/unavailable lookup leaves the attempt IN_DOUBT and bars retry-as-new-operation.

H's proposed semantic validator requires exact schema revision 1.2.11 / wire family 1.3.0, layered structural/crypto/semantic/join/currentness validation, INVALID versus UNKNOWN distinction, C owner ledger joins, COC ParticipantIntent/Reservation joins, and exact Batch-before-Manifest three-digest checks. H does not treat JSON Schema success as semantic acceptance.

I proposes a separate C-scoped cryptographic bundle `AIMBA-C-CRYPTO-1.0`, with distinct C domain separation and independent C key namespace. This is a candidate based on the I cryptographic primitive proposal, not an approved C profile. C accepts only the construction shape; C projection remains C-owned, I trust/key governance remains I-owned, and H must publish the exact projection and validator mapping. No I key, trust root or I P0 projection is reused for C.

### 11.3 Current binding status

- C Gate/Attempt/Same-key semantic amendment: **PROPOSED / NOT TESTED**.
- I C-scoped crypto profile: **CANDIDATE ONLY / NOT APPROVED / NOT REGISTERED**.
- H 1.2.11 semantic validator contract: **PROPOSED / NOT EXECUTED**.
- H schema 1.2.11: **STRUCTURAL CANDIDATE ONLY**.
- C/H exact cross-review: **STRUCTURAL ACCEPTANCE ONLY; SEMANTIC/WIRE FREEZE BLOCKED**.
- Real provider adapter race/idempotency tests: **OPEN**.
- Cross-language canonical-byte/signature/provider-outcome execution: **OPEN**.
- A final integration acceptance: **OPEN**.

No production readiness, universal exactly-once, Full Applied or Global Forget Completion is claimed. These role artifacts are delegated simulations, not independent human Owner signatures.


## 10. Phase 3.8.4 — Owner Snapshot Membership Proof exact binding / Owner Snapshot Membership Proof 精确绑定

### 10.1 H exact protocol/schema bundle

| Artifact | Exact Blob / Evidence |
|---|---|
| H Unified Schema 1.2.11 / wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` |
| H wire mapping 3.8.4 | `a692a790a4c7abef94dba6da9c22b5e06417879a` |
| H union Manifest contract 3.8.4 | `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175` |
| H exact review | `f5ab9a9232b04720faf552a70d5d2962343f843f` |
| H semantic reference module | `6710bd7876be5f2c60640f21090729b8859a7a3e` |
| H RecoveryJoin 1.0.2 tests | `6afa788da2a899f03de8207cb700c40e0533aba1` |
| H Unified 1.2.11 tests | `7582091c22ad7f75ed51dba7fbbd02d43af06933` |
| H Unified 1.2.12 tests | `5b444aa11ffb86c145ec745752204e623c1c2b41` |
| H candidate CI | Run `44050250038`, commit `34fb4ccf8b1580321d38eda1340cf53f73b83f24`, 281 total / 259 passed / 22 skipped / 0 failed |

### 10.2 Owner-owned proof contracts and reviews

| Owner | Proof contract Blob | Exact review Blob | Decision boundary |
|---|---|---|---|
| I | `b1e39c92252eadf8ca592f9a8dc6879cf44fd593` | `658ed437ecd05d226a6658a3f159ce28449b0b36` | Candidate security/wire acceptance with blocking conditions |
| D | `d80dabe7210e681bc4e2290355a38f8b67be9ddd` | `fe4ba71dd3a07d0775e17dbb90e8aeccc3bc71c0` | Accept with conditions; D signer/ledger implementation open |
| C | `5e37185610869951c3b392c9ad143a72b4c702ac` | `c6b317f5050bca745bb6308ad6f77ba7d8284f77` | Accept with enumerated C-owned conditions; provider adapter open |

These are coordinator-authored role-simulated review artifacts, not independent human Owner signatures. Each Owner remains the sole authority for its proof semantics, signature, key status, ledger completeness and anti-rollback.

### 10.3 Storage assessment

Storage accepts the separation of proof authorities and the typed RecoveryJoin 1.0.2 wire envelope as an architecture candidate:

1. A membership proof establishes one exact owner row's inclusion in one exact frozen owner snapshot and that row's owner-local sequence is within the captured high-water.
2. Membership does not establish full-ledger completeness. Each owner must separately attest complete query identity, pagination, count, ordered root/set digest, high-water vector and anti-rollback anchor.
3. H validates structure and exact joins; it must not trust caller-supplied `valid=true`. Its current reference validator requires an injected owner-proof verifier callback. The current CI callback is TEST-ONLY.
4. I, D and C independently sign and verify only their own rows. No owner compares numeric high-waters with another owner or with COC positions.
5. Empty owner sets require a separate owner-signed COMPLETE_EMPTY proof. Count=0, empty array, missing COC ParticipantIntent or queue emptiness are not proof.
6. Late-discovered pre-fence D work or late C provider-attempt evidence invalidates the affected snapshot/reconciliation and keeps the relevant gate closed.

### 10.4 Remaining blockers

- Production I/D/C proof signers, key registries, snapshot queries, pagination and anti-rollback adapters are not implemented or verified.
- H semantic validator's callback is not connected to actual owner trust authorities.
- Storage's COC quorum append, prefix completeness, Batch/Manifest ordering, linearizable S4 readback and production topology remain separate Gate A/B blockers.
- C provider-specific same-key lookup, send-vs-close serialization and real CSubmitOutcome remain unimplemented.
- D producer/worker/derivative ledger and Storage visibility linearization remain unimplemented.
- JF-10 P0 remains OPEN; Multi-PolicyDomain atomicity remains BLOCKED; production activation remains NOT AUTHORIZED.

**Storage disposition: ACCEPT AS ARCHITECTURE/WIRE CANDIDATE WITH BLOCKING IMPLEMENTATION AND OWNER-AUTHORITY CONDITIONS.** No Storage Gate A acceptance, COC deployment, JF-10 closure or production activation is inferred.


## 12. C/H/I exact Provider Outcome projection, wire mapping and governance review (2026-11-17)

This section is the current superseding exact pin set for the C Provider Outcome semantic/crypto/wire bundle. Earlier Section 11 pins remain historical provenance and MUST NOT be treated as the latest current artifacts.

### 12.1 Exact artifact pins

| Owner | Artifact | Exact Blob | Current disposition |
|---|---|---|---|
| C | Phase 3.8.6 Gate/Attempt/Idempotency semantic amendment | `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4` | PROPOSED; tests not run |
| C | Phase 3.8.7 review of I crypto candidate | `794d1dc49f034152407e3a42ba5ac937ea3539f8` | Candidate construction accepted only |
| C | Phase 3.8.8 exact C Provider Outcome signature projection | `39ff523c41f10e3a82442d4746dd7ca7763d271c` | C semantic field inventory proposed; no crypto freeze |
| I | Phase 3.8.4 C-scoped crypto profile proposal | `1bcddbaaa4a9ca730d492a6554941becac305668` | Candidate only |
| I | Phase 3.8.5 governance review/disposition | `41fc0f508ae75e8c16012966160e9e2a1e368881` | Conditional suite acceptance in principle; profile registration NOT APPROVED |
| H | Schema 1.2.11 / wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` | Structural candidate |
| H | Phase 3.8.5 semantic validator contract, corrected and extended | `d0496f32e6a7c0c46b41a9fc21867c354787b32a` | Proposed; not implemented/executed |
| H | Phase 3.8.6 exact 1.2.11 C outcome wire mapping/vector matrix | `de3db907b4077e0e4d37df19d289cf1bf51afbad` | Mapping/vector specification; vectors not executed |

Commit pins:
- C Phase 3.8.8: `36dd8e79ab4400f3824cb97c489780a89844da4b`.
- I Phase 3.8.5: `da8ea75c9ae3d6fffb0594633e478a3d665ab23b`.
- H Phase 3.8.5 correction/extension: `337b98a0ecbaf85768294575c9743844057f40b8`.
- H Phase 3.8.6 mapping/vector matrix: `91001740d461a64877e8ee10a4ce7332678b22e8`.

### 12.2 Exact schema finding

The exact 1.2.11 schema requires inline C outcome ref/digest, five-value outcome enum, provider and adapter refs, idempotency-key ref, final request boundary ID/digest, transaction ref, provider outcome evidence, C owner admission and ledger/high-water/root fields, COC record/quorum refs and nullable ParticipantIntentRef. It does NOT inline CGateRef/CGateGeneration, ProviderAttemptRef/Generation, provider account, endpoint, region or API operation. These are required in the immutable CSubmitOutcome object referenced by `c_submit_outcome_ref`; H must dereference and validate them. This is an explicit schema semantic dependency, not a claim of inline schema coverage.

### 12.3 Governance and release disposition

- I conditionally accepts the primitive suite in principle (JCS/RFC 8785, SHA-256, Ed25519, unpadded Base64url) for a separately scoped C profile, but does not register/approve the profile, C trust root, custody or production use.
- C owns the immutable semantic projection and provider outcome truth.
- H owns exact wire projection/mapping, validator and cross-language conformance.
- I owns cryptographic governance, trust and key lifecycle approval.
- C gate/attempt/provider idempotency tests remain unexecuted.
- H vector matrix is a specification only; no test fixture execution or independent Python/JavaScript agreement is claimed.
- Storage exact pinning is complete for this design bundle only. It does not imply implementation, CI success, production readiness, exactly-once semantics or final A acceptance.

**Current disposition: PROPOSED / DESIGN-LEVEL ONLY.** Protected C Provider Outcome cannot be declared VALID for release until profile registration, immutable C object dereference, H validator implementation, independent vector execution, provider adapter evidence and A final integration acceptance are all complete.

All Owner decisions above are delegated role simulations authored at the user's direction, not independent human Owner signatures.


### 10.5 A integration decision

- A Phase 3.8.4 cross-owner review: `reviews/integration/phase-3.8.4-a-membership-proof-cross-owner-integration-review.md`
- Exact Blob: `e6da7d17e0a347c54b44a9345916cf8e33ff3e7e`
- Decision: **ACCEPT AS CANDIDATE COMPOSITION WITH BLOCKING CONDITIONS**.
- R1/R2 remain OPEN; Storage Gate A remains PARTIAL PASS / OPEN; Gate B and Gate C remain BLOCKED; JF-10 P0 remains OPEN; Multi-PolicyDomain atomicity remains BLOCKED; production activation remains NOT AUTHORIZED.
- Provenance is delegated A-role simulation in the coordinating session, not independent human A Owner/governance sign-off.
