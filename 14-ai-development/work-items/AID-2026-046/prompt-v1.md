# AID-2026-046-PROMPT v1 — Add the missing key-status False rejection test

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Baseline: PR #616 merged at `fe5bad9eb8f6261f040bb2a10bfccc46ceb603b9`.
Current base: `main` at `87f54bb44d9cd2872d7faf7c5c146dd85cae6fc1`.
Tracking scope: REQ-08, Issue #348.
Task: complete the one remaining negative-path test for the seven `AppliedDeliveryChecks` tri-state callbacks. PR #616 is already merged; deliver a new follow-up PR.

## Authorized scope

- Modify only `08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` and the focused AID evidence.
- Add a test that sets `verify_key_status=lambda evidence: False`, invokes `validate_applied_delivery_evidence`, and asserts:
  - result status is `INVALID`;
  - the exact error `key status verifier rejected evidence` is present.
- Preserve the existing `verify_key_status=None -> UNKNOWN` test; do not conflate `None` with `False`.
- Preserve existing signature rejection and the separate `verify_c_submit_outcome_record` callback test.
- Update the test count and any coverage claims so they accurately state that all seven tri-state callbacks have a False-return negative test.
- Do not change validator implementation or `_tri_state`.
- Deliver through a new PR linked to AID-2026-046; do not modify `main` directly.

## Explicit non-goals

- Do not modify production validator code, evidence schemas, cryptographic algorithms, or protocol message definitions.
- Do not change the 21 missing message parsers or production authentication/tenant isolation.
- Do not implement MCP server `tools/call` response envelopes; that is AID-2026-044 / Issue #617.
- Do not reopen PR #616; the missing test is a follow-up.

## Verification requested

Run the focused Python unittest suite on the exact final follow-up PR head. Record exact HEAD SHA, Python version, OS/architecture, full command, raw exit code, and output. Also run `check_protocol_index.py` using the exact repository path/command and record output, plus a mutation test showing that removing the `verify_key_status=False` rejection causes the new test to fail. The previous 38-test report from PR #616 is not exact-head verification of this follow-up. GitHub-hosted Actions remain billing-blocked; no CI PASS is expected or claimed.

## Acceptance criteria

1. `verify_key_status=False` is explicitly tested and returns `INVALID`.
2. The exact rejection error `key status verifier rejected evidence` is asserted.
3. `verify_key_status=None` continues to return `UNKNOWN`.
4. All seven tri-state callbacks have an explicit False-return negative test.
5. The focused suite and protocol-index checker pass on the exact final head, with environment and raw exit codes recorded.
6. The follow-up PR and AID-2026-046 record the final coverage and all limitations.

## Provenance

Frozen from the separate-session technical review of PR #616 and its post-merge coverage finding, plus the current user instruction to continue convergence. The original PR #616 implementation prompt is not available; this v1 prompt governs only the remaining key-status test and does not fabricate the original author prompt or session ID.
