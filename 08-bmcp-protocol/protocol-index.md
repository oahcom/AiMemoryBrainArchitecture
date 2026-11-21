# BMCP Protocol Message Index

- Scope: `08-bmcp-protocol/`
- Baseline: `1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- Purpose: inventory message-type artifacts by file presence, not to certify semantic correctness.

## Message types

| Message type | Definition source | Schema | Validator | Conformance test | Status |
|---|---|---|---|---|---|
| `APPLIED_DELIVERY_EVIDENCE_RECORDED` | Phase 3.8.25 hardening addendum; Phase 3.8.26 CSubmitOutcome join addendum | `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` (1.0.0) | `validators/applied_delivery_evidence_validator.py` | `tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | **IMPLEMENTED** — all three artifacts are present. Test execution evidence: external verification; see PR description. |
| `C_PROVIDER_OUTCOME_RECORDED` | CSubmitOutcome 1.0.1 C-owned source schema; referenced by Phase 3.8.26 | External C-owned Schema Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; no BMCP-owned schema | **Missing in BMCP** | **Missing at baseline** in provider_outcome suite | **PARTIAL** — BMCP-local validator and conformance test were absent. The test added in this PR validates schema structure only; it is not a C semantic validator. |
| `RECOVERY_JOIN` (RecoveryJoin 1.0.2) | Referenced by Phase 3.8 H-RJ-HW-01 contract | **Not delivered** under `schemas/` | **Not delivered** | **Not delivered** | **NOT DEFINED** — contract reference exists; schema not delivered. |

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

The provider_outcome test added with this index exercises only Draft 2020-12 JSON Schema structure for CPO-01, CPO-03, CPO-06, CPO-07 and CPO-08. CPO-02, CPO-04, CPO-05, CPO-09 and CPO-10 are explicitly skipped because their expected outcomes require Owner C's authoritative semantic validator. Fixture signature placeholders and the unregistered profile are not cryptographic verification evidence.

CPO-08 is labelled as a COC half-pair vector, but its checked-in record contains both non-null COC participant references. It is schema-invalid for a separate structural reason: HANDOFF_ACCEPTED lacks ProviderRequestRef and ProviderReceiptRef. The test records this discrepancy and separately probes the schema's COC half-pair rejection using an in-memory mutation; it does not claim the unmodified CPO-08 fixture demonstrates that COC defect.
