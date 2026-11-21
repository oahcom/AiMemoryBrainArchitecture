---
document_metadata:
  domain: protocol
  role: index
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Candidate
    canonical_scope_id: protocol/bmcp-message-type-index
    normative_status: Informative
    canonical_conflict_status: None
---

# BMCP Protocol Message Index

- Scope: `08-bmcp-protocol/`
- Baseline: `1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- Purpose: inventory message-type artifacts by file presence, not to certify semantic correctness.

## Message types

| Message type | Definition source | Schema | Validator | Conformance test | Status |
|---|---|---|---|---|---|
| `APPLIED_DELIVERY_EVIDENCE_RECORDED` | Phase 3.8.25 hardening addendum; Phase 3.8.26 CSubmitOutcome join addendum | `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` (1.0.0) | `validators/applied_delivery_evidence_validator.py` | `tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | **IMPLEMENTED** — all three artifacts are present. Test execution evidence: external verification; see PR description. |
| `C_PROVIDER_OUTCOME_RECORDED` | CSubmitOutcome 1.0.1 C-owned source schema; referenced by Phase 3.8.26 | External C-owned Schema Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; no BMCP-owned schema | **Missing in BMCP** | `tests/conformance/provider_outcome/test_provider_outcome.py` — schema-structure-only; no C semantic conformance | **PARTIAL** — BMCP-local validator and C semantic conformance remain missing. The test added in this PR validates schema structure only; it is not a C semantic validator. |
| `RECOVERY_JOIN_PROOF` (RecoveryJoin 1.0.2) | Phase 3.8 H-RJ-HW-01 §§5–7 | `schemas/bmcp.recovery-join-1.0.2.schema.json` | `validators/recovery_join_validator.py` — structural plus D-local binding helpers; D authority injected | `tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py` (schema identity + valid/invalid fixtures); `tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` (D-binding helpers) | **IMPLEMENTED (artifact presence)** — all three files are present. This is not a claim of D proof adoption, production conformance, or authority-backed currentness; absent D callbacks remain `UNKNOWN`. |

## Type definitions (not message types)

| Type | Definition source | Classification |
|---|---|---|
| `ProducerRegistrationHighWater` | Phase 3.8 H-RJ-HW-01, §3 | Typed high-water value; not a message envelope |
| `ForgetFenceGeneration` | Phase 3.8 H-RJ-HW-01, §5 | Typed fence generation; not a message envelope |

## Evidence-boundary declaration

This index records whether named schema, validator and test artifacts exist at the indexed repository baseline. It does **not** determine whether their semantics are correct, complete, secure, interoperable, or accepted by an Owner.

- `IMPLEMENTED` means the schema, validator and conformance-test file are all present. It does not by itself mean tests passed in this PR or that production/runtime behavior exists.
- `PARTIAL` identifies missing artifacts and ownership boundaries; an external schema is not reclassified as a BMCP-local implementation.
- `NOT DEFINED` means a contract/document reference exists but no schema artifact was delivered in the BMCP schema directory.
- Semantic correctness is determined by the normative contract and responsible Owner. CSubmitOutcome outcome semantics remain C-owned.
- For `APPLIED_DELIVERY_EVIDENCE_RECORDED`, test-execution evidence is supplied externally and referenced in the PR description; this index does not claim a local test run by Owner H.

## CSubmitOutcome conformance boundary

The provider_outcome suite checks only the pinned C-owned Draft 2020-12 schema and deterministic structure. It is not C's semantic validator. CPO-02, CPO-04, CPO-05, CPO-09 and CPO-10 remain skipped pending the C-owned inputs below.

| Vector | What the vector asserts | Required C-owned authority/input |
|---|---|---|
| CPO-02 — rejected but ambiguous | `HANDOFF_REJECTED` with `POSSIBLE_OR_UNKNOWN` is a valid observation but not a terminal no-effect conclusion | A versioned outcome/disposition table defining rejected-but-ambiguous semantics, terminality, retry/reconciliation policy and the evidence that may close the uncertainty; a validator result for the observation-vs-terminal distinction |
| CPO-04 — unknown | `UNKNOWN` is an indeterminate provider outcome, not proof of no side effect | A normative UNKNOWN reason taxonomy and transition/closure rules; the authoritative proof sources and a tri-state verifier that returns `VALID`/`INVALID`/`UNKNOWN` without converting unavailable evidence into success |
| CPO-05 — in doubt | `IN_DOUBT` is not interchangeable with `UNKNOWN` | A separate IN_DOUBT state definition, reconciliation transitions, terminality rules and required evidence for resolution; a validator test proving its distinction from CPO-04 |
| CPO-09 — high-water exceeded | `COwnerLocalSequence > COwnerHighWater` is invalid | A C-authoritative ledger/high-water proof with ledger identity, sequence namespace, root/version, signature and currentness; a verifier that binds the record sequence to that authoritative cutoff |
| CPO-10 — request digest conflict | The C record's `RequestDigest` conflicts with the digest of the actual final request boundary | C's canonicalization/digest profile, the authoritative final-boundary bytes or immutable boundary proof, and a verifier that recomputes/binds the wire digest. The fixture's `wire_request_digest` is vector context, not a CSubmitOutcome schema property |

For all five vectors, Owner C must publish a versioned normative outcome/validation contract, a callable authoritative interface equivalent to `validate_c_submit_outcome(record, context)`, the evidence/proof formats and trust/key/ledger verification interface used by that function, and raw positive/negative fixtures with expected results. Its result contract must separate tri-state verification (`VALID`/`INVALID`/`UNKNOWN`) from the provider observation disposition and terminality/reconciliation state; a single Boolean or tri-state alone cannot express CPO-02's `VALID_AS_OBSERVATION_NOT_TERMINAL` expectation or distinguish CPO-04 from CPO-05. C must define the exact result schema. A function stub without its authority contract and evidence inputs is insufficient.

A BMCP-local validator can check:
- Draft 2020-12 schema validity, required fields, types, enums, unknown members and the schema's outcome-dependent structural rules;
- local COC participant intent/reservation pairing;
- duplicate JSON member rejection and deterministic equality between fields that are actually present in the same supplied object;
- the shape of references/digests and whether a test fixture is explicitly marked unregistered or cryptographically placeholder-only.

Without C authority, BMCP cannot establish issuer/profile/key authenticity, C ledger inclusion or current high-water, gate linearization, provider evidence authenticity, actual provider side-effect truth, COC transaction joins, or the binding between `RequestDigest` and bytes observed at the final provider request boundary. Those checks must be delegated to the C-owned verifier; unavailable authority or evidence must remain `UNKNOWN`.

CPO-08 fixture decision: **Option 1 — corrected valid baseline plus separate invalid vector.** `CPO-08-valid-baseline` now contains both required HANDOFF_ACCEPTED provider references and a complete COC pair. `CPO-08-coc-half-pair` is a separate negative vector with the same provider references and only the COC reservation set to null, so its rejection isolates the intended COC half-pair rule. The test no longer relies on an unrelated missing-provider-reference defect.

## RecoveryJoin 1.0.2 conformance boundary

The following three BMCP artifacts are present:
- `schemas/bmcp.recovery-join-1.0.2.schema.json`
- `validators/recovery_join_validator.py`
- `tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py`

The schema and tests cover the structural fields and requiredness stated in H-RJ-HW-01 §§5–7. The exact schema message_type is `RECOVERY_JOIN_PROOF`, inherited from the contract-pinned source Schema Blob `4b664e3bce465499bcdfd93796349a4ba7074002`; H-RJ-HW-01 itself does not independently define that message-type string, so its normative ownership remains a contract gap. The validator checks JSON/schema structure and deterministic D typed-watermark/Fence tuple bindings. It returns `UNKNOWN` when D-authoritative membership-proof authentication or Fence currentness verification is not supplied. It does not claim that D has adopted the proposed proof format, and it does not claim production/runtime conformance.

Contract ambiguities are preserved rather than guessed:
- The pinned source schema Blob `4b664e3bce465499bcdfd93796349a4ba7074002` declares envelope `schema_version = 1.0.0`, while its schema `$id` and the contract's artifact filename identify 1.0.2. H-RJ-HW-01 does not explicitly resolve this; the existing envelope const is preserved and the discrepancy is marked in schema `$comment`.
- §5.4 names the currentness-proof generation field `forget_fence_generation`; §5.9 pseudocode refers to `proof.fence_generation`. The schema follows the explicit §5.4 object and does not invent an alias.
- §5.8 names `lineage_manifest_digest` as a currentness-proof field but §5.4 omits it from the object and required list. The schema admits it as optional and the validator returns `UNKNOWN` when the evidence requires comparison but the proof omits it.
- §§3.5/4.2 refer to `snapshot.owner_specific_high_waters.producer_registration_high_water`, while §§5.5/7.1 specify a top-level `ownerSnapshot.producer_registration_high_water`. The schema and validator follow the explicit schema-addition snippets in §§5.5/7.1; the contract should reconcile this carrier-path mismatch before semantic adoption.
- §5.7 says `target_set_digest` and `forget_fence_namespace_ref` SHOULD be conditionally required for D LINEAGE/BARRIER_MEMBERSHIP evidence, not MUST. They are schema properties but not hard-required; the semantic helper returns `UNKNOWN` if absent.
- D's actual namespace identifier encoding, authoritative proof issuance, signature verification and currentness query interface remain NOT_SUPPLIED by the contract. The schema validates shape only; authority-dependent checks require injected D callbacks.

## Test execution evidence

Owner H did not execute local pytest in this round. Test-method counts are not execution results: provider_outcome has 10 test methods (5 semantic skips); applied_delivery_evidence has 30; RecoveryJoin 1.0.2 has 26. No passed/skipped/failed runtime totals are claimed here. External rerun output is still required.
