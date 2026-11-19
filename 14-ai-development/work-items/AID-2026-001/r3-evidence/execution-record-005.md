# R3 Execution Record 005 (Coordinator Local Execution, U-056)

- Timestamp: 2026-11-19 15:58 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.12)
- Command: `python -m unittest test_r3_contract` and `python -m unittest test_forget_model`
  (cwd: `reference-model/`)
- Commit under test: `3b267c88bbe6a27d57a28bcdef3dbc546253063d`
  (branch tip of `remediation/aid-2026-001-forget-contract-closure-2026-11-18`, parent `bdc3791`)
- Model blob: `33eb1c918fe3620206f24e72dad3001e5e5abaf4` (52,335 bytes, sha256 `ed6a689722ea627f20ca…`, 1,386 lines)
- Test blob (`test_r3_contract.py`): `a8a0f326eb5d1969ac5b8916cafa13f1ef1a3f8f` (62,037 bytes, sha256 `6eca9f98b05bae8f49fa…`, 1,714 lines)
- Test blob (`test_forget_model.py`): `5d09c6717a81428a23235fb0c87ccf3ade1671d9` (7,565 bytes, 150 lines)

## Result

```
Ran 71 tests in 0.007s

OK

Ran 14 tests in 0.001s

OK
```

Exit codes: 0, 0. Total 85 tests (71 contract + 14 forget).

`test_r3_contract` composition: DFI 22, OwnerIU011 T01–T16 16, StorageFaults STOR-01..07 7,
AuthorizationCommitEntry 14, AtomicPublicationFaultInjection FSTOR-01..12 12 → 71 total.

## Delta closed here

**F-D-NEW-01 (P1, Owner D): idempotent lookup vs first-commit phase gate.**

`commit_suppression()` now resolves `operation_registry.get(key)` before the first-commit
phase whitelist. A legitimate retry after the workflow advanced to `CLEANUP` / `COMPLETED`
reaches its idempotent identity instead of being rejected with
`authorization workflow phase required`. The whitelist remains on the first-commit path, so a
`CLEANUP` first commit with a valid credential is still refused. Authorization validation runs
before the existing lookup, so idempotency is not an authorization bypass.

**F-OI-04 (P2, Owner I): receipt authenticity and context binding.**

`Authorization.receipt` is now an immutable `ReceiptCredential`
(`receipt_id`, `issuer`, `audience`, `operation`, `request_hash`, `purpose`, `scope`,
`permission_epoch`, `nonce`, `not_before`, `expires_at`, `signature`). `_validate_authorization()`
asks the injected `ReceiptVerifier` for authenticity and validity window, then checks the
credential's own bindings against the live call (issuer, audience, operation, request hash,
purpose, scope superset, PermissionEpoch in both credential and authorization, nonce equality
with `Authorization.nonce`). `AuthorizationReference` retains the full credential, with
`receipt_id` and `nonce` as derived read-only properties. Retry audit credential fields are
derived from the verified credential, not assembled by the caller.

## Tests added

| Test | Covers |
|---|---|
| `test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit` | CLEANUP retry returns the original commit with a full retry audit and no projection change; CLEANUP first commit is refused with no side effects |
| `test_FSTOR_11_receipt_credential_verification_and_retry_binding` | 10 rejection cases (rejected signature ×2, wrong issuer/audience/operation/request hash/purpose/scope/epoch, credential-vs-authorization nonce mismatch) each with an explicit no-side-effect assertion, plus one accepted fresh credential fully audited |
| `test_FSTOR_12_default_verifier_fails_closed` | An unconfigured model rejects the credential, publishes no commit, writes no retry audit, consumes no nonce |
| `test_FSTOR_07` (amended) | Compares `authorization_receipt` against `receipt_id` (was string vs object) and asserts the reference carries the same credential id |

## Non-vacuity check

Run against `3948024` (model blob `ee3df6f5…`), the F-D-NEW-01 and F-OI-04 gaps reproduce
directly and the new suite cannot even import against that model:

- `F-D-NEW-01`: first commit at `AUTHORIZED`, set `phase = CLEANUP`, retry with a fresh
  authorization → `ContractViolation: authorization workflow phase required`.
- `F-OI-04`: `Authorization(nonce="forged-nonce", receipt_id="totally-made-up")` was accepted and
  its fabricated string persisted as `authorization_reference.receipt_id`; the retry audit record
  had keys `['authorization_receipt', 'commit_id', 'nonce', 'operation_id', 'permission_epoch',
  'request_hash', 'retry_id', 'retry_result']` and no credential object.
- The 3948024 model has no `ReceiptCredential`, no `receipt_verifier` field, and its
  `Authorization` fields end at `receipt_id`.

The new tests therefore constrain new behaviour rather than passing trivially.

## Test-double boundary

`TrustAllReceiptVerifier` is test-only. It checks only that a signature string is present and the
validity window holds; it provides **no** cryptographic assurance. FSTOR_12 exists to keep that
shortcut out of the shipped default. Real signature verification — wrong key, wrong algorithm,
tampered signature, revoked key — is **NOT RUN** and must be covered by an independent test of the
production verifier.

## Provenance

- Author session `6afe842b-1430-83ee-9f30-3547ca54ba1b` returned the A (phase-gate split) /
  B (`ReceiptCredential` + `ReceiptVerifier`) / D (FSTOR_07 assertion) plan and the FSTOR_10/11
  method bodies at 15:34 with an explicit `NOT RUN` declaration and the governance table
  (U-049 retained, DFI-013/021 limits, no PR/Issue).
- The author's answer was split across two assistant messages; the first harvest captured only
  the tail (16,426 chars starting at "## 3. D"). The complete answer is 26,847 chars and was
  recovered from the raw conversation mapping. No section of the plan was missing from the
  recovery.
- Implementation, test migration and local execution by the coordinator. This remains
  coordinator-side execution, not independent review.

## Limits

- In-memory reference model. No physical WAL, durability, or crash-recovery claim (DFI-021).
- Deterministic sequential interleavings only; no concurrency linearizability proof (DFI-013).
- Does not prove a real issuing service can mint a fresh credential per attempt. That is an
  operational requirement stated by Owner I, verified here only at the model boundary.
