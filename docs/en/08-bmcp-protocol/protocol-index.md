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
  bilingual_counterpart:
    source: "08-bmcp-protocol/protocol-index.md"
---

# BMCP Protocol Message Index

- Scope: `08-bmcp-protocol/`
- Audited base: `2f8c00d835b04c75e71f1a6ba33e1e465445dec0`
- Purpose: inventory actual `message_type` constraints by schema source and artifact presence. This index does not certify semantic correctness or production conformance.
- Checker: `python3 08-bmcp-protocol/scripts/check_protocol_index.py`
- Regression tests: `python3 -m unittest discover -s 08-bmcp-protocol/tests -p 'test_protocol_index_consistency.py' -v`

## Inventory method and measured result

The inventory walks only `08-bmcp-protocol/schemas/*.json` and only counts finite string constraints attached to a property named `message_type` (`const`, `enum`, including nested `oneOf`/`anyOf`/`allOf` and conditional branches). It does not count unrelated enums, status values, event names, prose, fixtures, or a generic `message_type: { "type": "string" }` declaration without a finite value.

| Measurement | Audited base result |
|---|---:|
| JSON Schema files in `schemas/` | 32 |
| Files with finite `message_type` constraints | 31 |
| Files without a finite `message_type` constraint | 1 |
| Unique message types | 22 |
| Message-type rows in this index | 22 |
| Missing / extra / duplicate / invalid index rows | 0 / 0 / 0 / 0 |

The one schema without a finite message type is `schemas/bmcp.i-owner-snapshot-attestation-1.0.0.schema.json`. Its presence is counted in the Schema total, not treated as an unindexed message.

## Message types

JSON Pointers below identify the exact `const` constraint (or the enclosing property where stated). For repeated version families, the index records representative observed artifacts; it does not declare those versions canonical/current.

| Message type | Definition source | Schema and JSON Pointer | Validator | Conformance test | Status |
|---|---|---|---|---|---|
| `APPLIED_DELIVERY_EVIDENCE_RECORDED` | `phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md`; `phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md` | `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` — `/properties/message_type/const` | `validators/applied_delivery_evidence_validator.py` | `tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | **IMPLEMENTED (artifact presence)** — schema, validator and test files exist. Not a production-conformance claim. |
| `COC_PARTICIPANT_MANIFEST` | Schema-local definition; `runtime_reference/recovery_cutoff_semantics.py` is reference code, not an authority source | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/participantManifest/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_two_phase_recovery.py` (fixture/reference coverage) | **SCHEMA PRESENT** — test/reference presence does not establish authoritative conformance. |
| `COC_RECOVERY_CUTOFF_BATCH` | Schema-local definition; `runtime_reference/unified_manifest_semantics.py` is reference code, not an authority source | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/0/allOf/1/properties/message_type/const` | — (reference semantics are not a production validator) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`; `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py` | **SCHEMA + REFERENCE TESTS PRESENT** — no production or authority-backed conformance claim. |
| `C_PROVIDER_OUTCOME_RECORDED` | C-owned CSubmitOutcome 1.0.1 source schema fixture; H Phase 3.8.26 join addendum; C outcome semantics remain C-owned | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/10/allOf/1/properties/message_type/const`; repeated conditional guard at `/oneOf/10/allOf/9/if/properties/message_type/const` | `validators/provider_outcome_validator.py`; `validators/provider_outcome_validator_1_2_15.py`; `validators/envelope_auth_validator.py`; `validators/gateway_attestation_validator.py` | `tests/conformance/provider_outcome/test_provider_outcome.py`; `tests/conformance/provider_outcome/test_provider_outcome_validator.py`; `tests/conformance/provider_outcome/test_envelope_auth_validator.py`; `tests/conformance/provider_outcome/test_gateway_attestation_validator.py` | **PARTIAL** — BMCP structure/reference validation exists; C-owned issuer, ledger, gate, provider-side-effect and final-request authority checks remain external/UNKNOWN when unavailable. |
| `I_JF10_TERMINAL_DECISION_OBSERVED` | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` (source reference); exact message spelling is preserved | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/2/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |
| `JF10_BRIDGE_RECONCILIATION_RECORDED` | Schema-local definition; no separate normative source mapped in this scoped audit | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/4/properties/message_type/const`; also Unified 1.2.17 `/oneOf/9/allOf/1/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py` (message-family coverage) | **SCHEMA + LIMITED TEST REFERENCE** — no dedicated validator or production conformance claim. |
| `JF10_I_TERMINAL_DECISION_OBSERVED` | Schema-local definition; do not conflate with `I_JF10_TERMINAL_DECISION_OBSERVED` | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/7/allOf/1/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`; `tests/conformance/recovery_cutoff/test_i_crypto_profile.py` | **SCHEMA + REFERENCE TESTS PRESENT** — no production authority claim. |
| `JF10_PREPARED_PARTICIPANT_REGISTERED` | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/1/properties/message_type/const`; also Unified 1.2.17 `/oneOf/6/allOf/1/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py` (message-family coverage) | **SCHEMA + LIMITED TEST REFERENCE** — no dedicated validator or production conformance claim. |
| `JF10_PREPARE_INTENT_REGISTERED` | `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md`; `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/0/properties/message_type/const`; also Unified 1.2.17 `/oneOf/5/allOf/1/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py` (message-family coverage) | **SCHEMA + LIMITED TEST REFERENCE** — no dedicated validator or production conformance claim. |
| `JF10_STORAGE_PARTICIPANT_RESOLVED` | Schema-local definition; do not conflate with `STORAGE_JF10_PARTICIPANT_RESOLVED` | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/8/allOf/1/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py` (message-family coverage) | **SCHEMA + LIMITED TEST REFERENCE** — no dedicated validator or production conformance claim. |
| `OWNER_ADMISSION_ENTRY` | Schema-local definition; no separate normative source mapped in this scoped audit | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/admissionEntry/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |
| `OWNER_ADMISSION_SNAPSHOT_ATTESTATION` | Schema-local definition; no separate normative source mapped in this scoped audit | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/ownerSnapshot/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |
| `OWNER_GATE_RELEASE_ATTESTATION` | Schema-local definition; no separate normative source mapped in this scoped audit | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/gateRelease/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |
| `OWNER_LOCAL_GATE_RELEASE` | `runtime_reference/owner_gate_release_semantics_1_2_17.py` (reference semantics only) | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/3/allOf/1/properties/message_type/const` | — (reference code is not an authority-backed production validator) | `tests/conformance/recovery_cutoff/test_owner_gate_release_1_2_17.py`; `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py` | **SCHEMA + REFERENCE TESTS PRESENT** — authority-dependent checks remain UNKNOWN without owner verifiers. |
| `OWNER_LOCAL_PENDING_GATE` | `runtime_reference/unified_manifest_semantics.py` (reference semantics only) | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/2/allOf/1/properties/message_type/const` | — (reference code is not an authority-backed production validator) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`; `tests/conformance/recovery_cutoff/test_i_crypto_profile.py` | **SCHEMA + REFERENCE TESTS PRESENT** — authority-dependent checks remain UNKNOWN without owner verifiers. |
| `PARTICIPANT_SET_RECONCILIATION` | `runtime_reference/unified_manifest_semantics.py` (reference semantics only) | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/1/allOf/1/properties/message_type/const` | — (reference code is not an authority-backed production validator) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`; `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py` | **SCHEMA + REFERENCE TESTS PRESENT** — authority-dependent checks remain UNKNOWN without owner verifiers. |
| `RECOVERY_CUTOFF_BATCH` | `runtime_reference/recovery_cutoff_semantics.py` (reference semantics only) | `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/recoveryBatch/properties/message_type/const` | — (no dedicated authority-backed validator located) | `tests/conformance/recovery_cutoff/test_two_phase_recovery.py`; `tests/conformance/recovery_cutoff/test_hrc_semantics.py` | **SCHEMA + REFERENCE TESTS PRESENT** — no production or authority-backed conformance claim. |
| `RECOVERY_EPOCH_COMPLETED` | Schema-local definition; present in both Recovery Cutoff and Unified families | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` — `/oneOf/4/allOf/1/properties/message_type/const`; and `schemas/bmcp.recovery-cutoff-1.0.5.schema.json` — `/$defs/epochCompleted/properties/message_type/const` | — (no dedicated validator located) | `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_15.py`; `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17.py`; `tests/conformance/recovery_cutoff/test_two_phase_recovery.py` | **SCHEMA + REFERENCE TESTS PRESENT** — no production conformance claim. |
| `RECOVERY_JOIN_PROOF` | Phase 3.8 H-RJ-HW-01 §§5–7; message-type spelling is inherited from pinned source Schema Blob `4b664e3bce465499bcdfd93796349a4ba7074002` | `schemas/bmcp.recovery-join-1.0.2.schema.json` — `/properties/message_type/const` | `validators/recovery_join_validator.py` | `tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py`; `tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` | **IMPLEMENTED (artifact presence)** — not a claim of D proof adoption, production conformance or authority-backed currentness; absent D callbacks remain UNKNOWN. |
| `STORAGE_JF10_PARTICIPANT_RESOLVED` | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`; exact spelling differs from Unified `JF10_STORAGE_PARTICIPANT_RESOLVED` | `schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json` — `/oneOf/3/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |
| `Storage.PreparedParticipantReceipt` | Schema-local definition; no separate normative source mapped in this scoped audit | `schemas/bmcp.storage-prepared-participant-proof-1.0.0.schema.json` — `/$defs/preparedReceiptMessage/properties/message_type/const; repeated conditional guard at /$defs/preparedReceiptMessage/allOf/0/if/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |
| `Storage.StorageResolutionProof` | Schema-local definition; no separate normative source mapped in this scoped audit | `schemas/bmcp.storage-prepared-participant-proof-1.0.0.schema.json` — `/$defs/storageResolutionMessage/properties/message_type/const; repeated conditional guard at /$defs/storageResolutionMessage/allOf/0/if/properties/message_type/const` | — (no dedicated validator located) | — (no message-specific test located) | **SCHEMA PRESENT** — no conformance verdict. |

## Complete Schema inventory

All 32 JSON Schema files in the audited `schemas/` directory:

- `bmcp.applied-ack-1.1.0-jf10-bridge.schema.json`
- `bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json`
- `bmcp.applied-delivery-evidence-1.0.0.schema.json`
- `bmcp.coc-jf10-unified-1.2.0.schema.json`
- `bmcp.coc-jf10-unified-1.2.1.schema.json`
- `bmcp.coc-jf10-unified-1.2.2.schema.json`
- `bmcp.coc-jf10-unified-1.2.3.schema.json`
- `bmcp.coc-jf10-unified-1.2.4.schema.json`
- `bmcp.coc-jf10-unified-1.2.5.schema.json`
- `bmcp.coc-jf10-unified-1.2.6.schema.json`
- `bmcp.coc-jf10-unified-1.2.7.schema.json`
- `bmcp.coc-jf10-unified-1.2.8.schema.json`
- `bmcp.coc-jf10-unified-1.2.9.schema.json`
- `bmcp.coc-jf10-unified-1.2.10.schema.json`
- `bmcp.coc-jf10-unified-1.2.11.schema.json`
- `bmcp.coc-jf10-unified-1.2.12.schema.json`
- `bmcp.coc-jf10-unified-1.2.13.schema.json`
- `bmcp.coc-jf10-unified-1.2.14.schema.json`
- `bmcp.coc-jf10-unified-1.2.15.schema.json`
- `bmcp.coc-jf10-unified-1.2.16.schema.json`
- `bmcp.coc-jf10-unified-1.2.17.schema.json`
- `bmcp.i-owner-snapshot-attestation-1.0.0.schema.json`
- `bmcp.recovery-cutoff-1.0.0.schema.json`
- `bmcp.recovery-cutoff-1.0.1.schema.json`
- `bmcp.recovery-cutoff-1.0.2.schema.json`
- `bmcp.recovery-cutoff-1.0.3.schema.json`
- `bmcp.recovery-cutoff-1.0.4.schema.json`
- `bmcp.recovery-cutoff-1.0.5.schema.json`
- `bmcp.recovery-join-1.0.0.schema.json`
- `bmcp.recovery-join-1.0.1.schema.json`
- `bmcp.recovery-join-1.0.2.schema.json`
- `bmcp.storage-prepared-participant-proof-1.0.0.schema.json`

## Unified Schema version declaration

**Latest observed artifact:** `bmcp.coc-jf10-unified-1.2.17.schema.json`; **canonical current version: NOT DECLARED**.

Evidence:
- The audited directory contains the 18 distinct Unified artifacts numbered 1.2.0 through 1.2.17.
- 1.2.17 has the highest observed semantic version and its own description identifies it as artifact revision 1.2.17. That does not declare it the canonical current version.
- No release/supersession rule or authoritative current-version declaration was found in the Unified schemas or this index.
- Conformance material still explicitly references earlier versions, including 1.2.8, 1.2.10, 1.2.11, 1.2.12, 1.2.14, 1.2.15 and 1.2.16. The 1.2.10 test has a local skip annotation saying its semantics are superseded by 1.2.11/1.2.12; that test annotation is not a repository-wide release policy.
- Therefore this index MUST NOT say `Current unified schema: ...1.2.17...` until an authority decision is recorded.

**Required authority decision:** BMCP Protocol Owner (Owner H) must provide the version-release/supersession rule and recommend the canonical version; Architecture Owner must ratify the canonical-current declaration. Neither role is silently substituted by filename ordering in this index.

## Type definitions (not message types)

These are not counted among the 22 message types:

| Type | Definition source | Classification |
|---|---|---|
| `ProducerRegistrationHighWater` | Phase 3.8 H-RJ-HW-01 §3 | Typed high-water value; not a message envelope. |
| `ForgetFenceGeneration` | Phase 3.8 H-RJ-HW-01 §5 | Typed fence generation; not a message envelope. |

## Evidence-boundary declaration

This index records schema constraints and the presence or absence of named validator/test artifacts. It does **not** determine whether semantics are correct, complete, secure, interoperable, or accepted by an Owner.

- `IMPLEMENTED (artifact presence)` does not mean production conformance, runtime integration, owner adoption, or authority-backed currentness.
- `PARTIAL` does not mean DONE. It identifies an incomplete boundary and missing external authority.
- BMCP-local Schema/structural validation does not equal C semantic validation.
- A reference implementation or fixture test is not automatically an authoritative validator.
- `UNKNOWN` remains UNKNOWN when the required authority or evidence is unavailable.

Without C authority, BMCP cannot establish issuer/profile/key authenticity, C ledger inclusion or high-water currentness, gate linearization, provider evidence authenticity, actual provider side-effect truth, COC transaction joins, or the binding between `RequestDigest` and bytes observed at the final provider request boundary. Those checks must be delegated to the C-owned verifier; unavailable authority or evidence must remain `UNKNOWN`.

The same boundary applies to I/D/Storage-owned trust, membership, fence, and prepared-participant authority. Local shape or deterministic binding checks do not establish those external facts.

## Index consistency gate

The checker enforces:
1. Every finite message type found in a Schema is indexed exactly once.
2. Every indexed message type exists in at least one Schema.
3. Duplicate index rows fail.
4. Each row names an existing Schema that actually constrains that exact message type.
5. A newly added Schema message type fails until the index is updated.
6. Removed/renamed Schema message types leave a stale index row and fail.
7. Enums unrelated to the `message_type` property are not counted.

Run from the repository root:

```sh
python3 08-bmcp-protocol/scripts/check_protocol_index.py
python3 -m unittest discover -s 08-bmcp-protocol/tests -p 'test_protocol_index_consistency.py' -v
```

The checker is an index-consistency gate only. It does not validate the message semantics, transport, framing, session, handshake, production runtime, or C/D/I/Storage authority.

## Conformance test runners

The conformance tests are organized under `08-bmcp-protocol/tests/conformance/`.

| Scope | Run command or setup | Coverage |
|---|---|---|
| `applied_delivery_evidence/` | `python -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v` | All tests in this directory. |
| `recovery_cutoff/` — RecoveryJoin | `python -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p 'test_recovery_join*.py' -v` | RecoveryJoin tests matching the filename pattern. |
| `provider_outcome/` — C crypto profile | `python -m unittest discover -s provider_outcome -p 'test_c_crypto_profile*interop.py' -v` (run from `08-bmcp-protocol/tests/conformance/`) | C crypto profile interoperability tests; 6 tests. |
| `recovery_cutoff/` — I crypto profile | `python -m unittest discover -s recovery_cutoff -p 'test_i_crypto_profile.py' -v` (run from `08-bmcp-protocol/tests/conformance/`) | I crypto profile interoperability tests; 7 tests. |
| `recovery_cutoff/` — HRC semantics | `python -m unittest discover -s recovery_cutoff -p 'test_hrc_semantics.py' -v` (run from `08-bmcp-protocol/tests/conformance/`) | HRC semantic tests; 44 tests. |
| Conformance Node dependencies | Run `npm ci` from `08-bmcp-protocol/tests/conformance/`. | Installs the locked `canonicalize@5.1.0` dependency from `package-lock.json`. The three `.mjs` reference implementations import `canonicalize`. |

The workflow `.github/workflows/h-applied-delivery-evidence-conformance.yml` runs the five Python discovery commands above. The Node dependency is required by the three crypto profile interoperability test files: without the installed dependency, their Node subprocesses fail rather than skip. Locally, the three test files passed with the dependency installed (13 tests total). The HRC semantic test file passed with both `python -m unittest` and `python -m pytest` (44 tests). These local results do not state that the workflow has passed.

## CSubmitOutcome conformance boundary

The provider_outcome suite checks the pinned C-owned Draft 2020-12 schema and deterministic structure. It is not C's semantic validator. CPO-02, CPO-04, CPO-05, CPO-09 and CPO-10 remain dependent on C-owned outcome semantics, ledger/high-water authority, gate evidence and final-request-boundary proof.

A BMCP-local validator may check schema validity, required fields, types, enums, unknown members, duplicate JSON member rejection and deterministic relationships between fields present in the supplied object. It cannot convert unavailable C evidence into success.

## RecoveryJoin 1.0.2 conformance boundary

The RecoveryJoin schema, validator and conformance tests are present. The validator checks JSON/schema structure and deterministic D typed-watermark/Fence tuple bindings. It returns `UNKNOWN` when D-authoritative membership-proof authentication or Fence currentness verification is not supplied. This does not mean D adopted the proposed proof format or that production/runtime conformance exists.
