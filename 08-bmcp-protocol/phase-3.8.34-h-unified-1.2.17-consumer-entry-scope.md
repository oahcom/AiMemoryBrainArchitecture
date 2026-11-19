# Phase 3.8.34 — H Unified 1.2.17 Consumer-Entry Scope Declaration

- Date: 2026-11-19
- Branch: `session-h-bmcp-protocol`
- Baseline HEAD supplied for this task: `dd3cacde4af541205d2dc1e50f8a196666ea3a7b`
- Scope: TEST-profile reference validators and conformance fixtures only
- This declaration does not authorize production consumption or change any D Owner contract.

## 1. Determination

`08-bmcp-protocol/runtime_reference/unified_manifest_semantics.py` declares itself as a TEST-profile reference validator for unified BMCP manifest 1.2.9. Its historical/default mode is **not** a complete Schema 1.2.17 consumer.

There was nevertheless a real mixed-version test call path: `test_unified_manifest_owner_snapshot_alignment.py` imported `validate_owner_snapshot` and `validate_union`, checked the D eight-field shape against Schema 1.2.17, but constructed I and C snapshots with the legacy five-field and three-field shapes. Thus that test was exercising a partial 1.2.17/legacy composition, not proving full 1.2.17 I/D/C compatibility. No production runtime caller of either reference validator was identified in the inspected `08-bmcp-protocol` runtime/test call paths.

The old combined-validator default must not be implicitly used for Schema 1.2.17. A version must be selected explicitly.

## 2. Field-set boundary and compatibility repair

Schema `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` defines closed owner-specific sets:

- I: six fields, including `permission_epoch` and `producer_domain_inventory_epoch_ref`; the legacy `inventory_epoch_ref` alias is not accepted.
- D: eight fields, including ForgetFence and dependency-closure fields.
- C: five fields, including `provider_idempotency_namespace_ref` and `final_request_boundary_generation`.

The combined reference validator now has an explicit `schema_artifact_revision` argument on `validate_owner_snapshot` and `validate_union`:

- Default `"1.2.9"`: preserves the historical I five-field / C three-field sets. This default is for existing legacy reference fixtures only; it is not a Schema 1.2.17 entry.
- Explicit `"1.2.17"`: requires the exact I six-field / C five-field sets above. Legacy aliases/sets fail closed.
- Any other revision: returns `INVALID`.
- The D eight-field contract and the existing injected authority-callback behavior are unchanged.

No automatic field-set guessing or mixed-version fallback is performed. A 1.2.17 composition caller must pass `schema_artifact_revision="1.2.17"` to `validate_union`.

## 3. 1.2.17 designated TEST-profile verification entries

Owner Snapshot semantic validation is designated to:

- File: `08-bmcp-protocol/runtime_reference/owner_snapshot_semantics_1_2_17.py`
- Function: `validate_owner_snapshot_1_2_17`

Its tests import and invoke that function from:

- `tests/conformance/recovery_cutoff/test_owner_snapshot_1_2_17.py`
- `tests/conformance/recovery_cutoff/test_owner_snapshot_semantics_1_2_17.py`

For a composed I/D/C manifest reference check, the explicit versioned entry is:

- File: `08-bmcp-protocol/runtime_reference/unified_manifest_semantics.py`
- Function: `validate_union(..., schema_artifact_revision="1.2.17")`

These are TEST-profile reference entry points. They are not production runtime consumers, do not establish live owner-ledger/attestation/currentness integration, and do not confer production authorization.

## 4. Call-path inventory

The following are the inspected Python call sites relevant to the three requested function names (line numbers refer to the delivered source revision):

1. `runtime_reference/unified_manifest_semantics.py:41` — defines `validate_owner_snapshot`.
2. `runtime_reference/unified_manifest_semantics.py:176` — defines `validate_union`; line 194 calls `validate_owner_snapshot` internally.
3. `tests/conformance/recovery_cutoff/test_unified_manifest_owner_snapshot_alignment.py:12-13` — test-fixture imports of `validate_owner_snapshot` and `validate_union`; direct assertions and composed calls occur at lines 56-187. This is the pre-existing mixed-version alignment fixture, not a production entry.
4. `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17_composed_entry.py:11-13` — new test-fixture imports; direct and composed explicit-revision calls occur at lines 106-180.
5. `runtime_reference/owner_snapshot_semantics_1_2_17.py:48` — defines `validate_owner_snapshot_1_2_17`.
6. `tests/conformance/recovery_cutoff/test_owner_snapshot_1_2_17.py:10-11,72,91` — imports and invokes the dedicated 1.2.17 snapshot validator.
7. `tests/conformance/recovery_cutoff/test_owner_snapshot_semantics_1_2_17.py:11-13,90-173` — imports and invokes the dedicated validator for D bounded-field regressions.

Related but distinct: `test_recovery_join_1_0_2.py:10-11,87-107` calls `validate_owner_snapshot_membership_proof_payload`; that function validates membership-proof payloads and is not any of the three snapshot/union entry points listed above.

The 1.2.17 semantic-reference note `phase-3.8.33-h-unified-1.2.17-owner-gate-release-semantic-reference.md` identifies `owner_gate_release_semantics_1_2_17.py` as the Owner Gate Release reference validator. That is a separate function family and does not designate the 1.2.9 combined validator as a 1.2.17 owner-snapshot consumer.

## 5. Regression coverage

New suite: `tests/conformance/recovery_cutoff/test_unified_manifest_1_2_17_composed_entry.py`.

It covers:
- legacy I/C sets accepted in default legacy mode and rejected in 1.2.17 mode;
- new I/C sets rejected in legacy mode and accepted in explicit 1.2.17 mode;
- unknown revisions fail closed;
- composed union accepts the exact legacy set in legacy mode;
- composed union accepts exact I6/D8/C5 sets in explicit 1.2.17 mode;
- composed union rejects legacy I/C sets in 1.2.17 mode and rejects new I/C sets in legacy mode.

The existing `VALID` / `INVALID` / `UNKNOWN` result vocabulary and injected authority-callback rules are unchanged. The only intended classification change is version-specific closed-world field-set selection: old I/C sets are INVALID under explicit 1.2.17; new I/C sets are INVALID under the legacy default.

## 6. Test command and execution evidence

The repository workflow `.github/workflows/h-recovery-cutoff-conformance.yml` specifies:

```sh
python -m unittest discover \
  -s 08-bmcp-protocol/tests/conformance/recovery_cutoff \
  -p "test_*.py" -v
```

Workflow environment: Python 3.12; pinned Python dependencies `rfc8785==0.1.4`, `cryptography==44.0.2`, `jsonschema==4.23.0`; Node.js 22 and `canonicalize@2.1.0` for the independent wire tests.

Push-triggered runs observed for the implementation commits:
- Run 44598609915 (code commit `a04d4010152577cab2f27b4c1359e955ea91e447`): conclusion FAILURE.
- Run 44598682938 (test commit `cba1f67ccdeb8a4dcdfe560e9005647b8afac12a`): conclusion FAILURE.

For both runs the GitHub Jobs response reported the job as completed with an empty `steps` array. No Python test process output or per-test PASS/FAIL/SKIP results was available. Therefore this delivery does **not** claim that the suite passed or that any test was executed. The workflow failure must be diagnosed/re-run before test acceptance. Python/dependency versions above are workflow-pinned versions, not a claim about an observed runner process.

## 7. Authority and non-claims

- This is an implementation/scope declaration only.
- It is not an independent review and does not close, upgrade, or adjudicate F-43-10.
- It is not a closure basis for F-43-08 and does not perform its identifier reconciliation.
- It does not close F-43-09.
- It does not declare G8 READY.
- It does not adopt D 1.3.0 or authorize H to consume D 1.3.0.
- It does not modify D Owner contracts, historical Finding anchors, PRs, Issues, or branches.
- The delivered code/test commits and this document do not establish production VALID/INVALID/UNKNOWN authority beyond the TEST-profile reference semantics described above.
