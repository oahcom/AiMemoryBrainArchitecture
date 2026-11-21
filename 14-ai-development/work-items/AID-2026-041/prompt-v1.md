# AID-2026-041-PROMPT v1 — Shallow-history provenance guard

## User dispatch

Repair `scripts/check_bilingual_docs.py` so embedded bilingual registration provenance cannot be judged from incomplete Git history.

## Scope

1. Make `_file_add_commit()` and `_registration_add_commit()` refuse shallow repositories.
2. Check history completeness at the beginning of `check_embedded_registration_history()` and make `main()` return exit code 2 for an unverifiable shallow-history condition, with the exact diagnostic: `cannot verify registration provenance on a shallow clone; run git fetch --unshallow`.
3. Add two regression tests to `scripts/governance/evidence/test_gate_normative_roots.py`: fake-Git shallow detection and a full-history SHA snapshot for all 21 `EMBEDDED_BILINGUAL_SOURCES` entries.
4. Document that `SELF_REGISTERED_AT_CREATION` SHAs must be derived from full history, including the measured example creation SHA `cd1ab0fb346c770d779b1d8d24297f6811a1a74f` and registration SHA `32a35f422ba6442d1f700cfb327f348c0740a7f2`.
5. Verify full-history PASS, shallow-clone exit 2, and the normative-roots regression suite.

## Explicit exclusions

Do not modify `SELF_REGISTERED_AT_CREATION` values, `EMBEDDED_BILINGUAL_SOURCES`, or the registration ordering policy. Do not add the shallow-boundary SHA `5ce8657d402b911c72ccf1f2bd14c235d49aca86` to any whitelist.

## Acceptance

- Complete-history main gate returns 0.
- A depth-limited clone returns 2 with the exact diagnostic above.
- Existing tests remain green; two new regressions are included.
- Deliver one PR titled `fix(bilingual): refuse to judge registration provenance on a shallow clone`.

## Provenance

Frozen from the user dispatch in the ChatGPT conversation on 2026-11-21. Platform session identifier and raw prompt payload bytes are not exposed; no external prompt-source digest is asserted.
