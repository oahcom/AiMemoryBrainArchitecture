# AID-2026-046-PROMPT v1 — Prove the key-status verifier's False rejection path

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Tracking carrier: PR #616 (REQ-08 applied-delivery trust callback tests).
Base: `main` at `792565ac60795ece14f8575774a72563c69e8b1f`.
Current PR head: `f9e88cd7329e42ab616ba6837a7348411a5c929e`.
Task: complete negative-path test coverage for all seven `AppliedDeliveryChecks` tri-state callbacks.

## Authorized scope

- Modify only `08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` and the focused PR #616 work-item evidence.
- Add a test that sets `verify_key_status=lambda evidence: False`, invokes `validate_applied_delivery_evidence`, and asserts:
  - result status is `INVALID`;
  - the exact error `key status verifier rejected evidence` is present.
- Preserve the existing `None -> UNKNOWN` test; do not conflate `None` with `False`.
- Preserve existing tests for signature rejection and the separate `verify_c_submit_outcome_record` callback.
- Update the PR description and AID manifest to state the correct negative-path coverage count.
- Do not change validator implementation or `_tri_state`.

## Explicit non-goals

- Do not modify production validator code, evidence schemas, cryptographic algorithms, or protocol message definitions.
- Do not change the 21 missing message parsers or production authentication/tenant isolation.
- Do not implement MCP server `tools/call` response envelopes; that is AID-2026-044 / Issue #617.
- Do not push directly to `main`; update the existing PR #616 branch.

## Verification requested

Run the focused Python unittest suite on the exact final PR head. Record exact HEAD SHA, Python version, OS/architecture, full command, raw exit code, and output. Also run `check_protocol_index.py` with the exact command/output and the recorded mutation test that proves each new negative test fails when its corresponding rejection branch is removed. The previous 38-test report on `eac8c465...` is not exact-head verification for the rebased head `f9e88cd...`. GitHub Actions remains billing-blocked; no CI PASS is expected or claimed.

## Acceptance criteria

1. `verify_key_status=False` is explicitly tested and returns `INVALID`.
2. The exact rejection error `key status verifier rejected evidence` is asserted.
3. `verify_key_status=None` continues to return `UNKNOWN`.
4. The seven callback negative paths are accurately counted and each is covered by a False-return test.
5. The full focused suite and protocol-index checker pass on the exact final head, with environment and raw exit codes recorded.
6. PR #616 and AID-2026-046 record the final coverage and all limitations.

## Provenance

Frozen from the independent technical review on PR #616 and the current user instruction to continue convergence. The original implementation prompt is not available in this context; this v1 prompt governs only the remaining key-status test and exact-head verification and does not fabricate the original author prompt or session ID.
