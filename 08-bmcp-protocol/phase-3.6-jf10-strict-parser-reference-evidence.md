# H Phase 3.6 — Strict JSON Parser and Critical Extension Reference Evidence

- Branch HEAD: `0669ca950cf181594717f82503b7c64c800b27f3`
- Parser reference: `08-bmcp-protocol/runtime_reference/strict_json_parser.py`, Blob `3b9b3da645448c773c95a9dcd3c57c8c109bb2da`
- Parser tests: `tests/schema/test_strict_json_parser.py`, Blob `f9c8f44da5c4d52efe78368c54a73eaa1286c374`
- Schema tests: `tests/schema/test_jf10_bridge_schema.py`, Blob `74bc4286abe1489ce29c2446c6fc22445784609f`
- Workflow: `.github/workflows/jf10-bridge-schema.yml`, Blob `f4c01f6bc96294e8e4d13d7a211e3bb6d8b99fee`
- CI run: `43963209651`; job `133635778980`; commit `a81c5c374ad20ac702a962418b50f65c6a16bb2c`
- Result: **23/23 TESTS PASS** (11 schema/fixture + 12 strict parser tests)

## 1. Strict parser behavior tested

1. Duplicate top-level and nested JSON keys are rejected.
2. Invalid UTF-8 and non-finite JSON numbers are rejected.
3. Non-object message roots are rejected.
4. Configured byte-size and nesting-depth limits are enforced.
5. Unknown non-critical extension fields are preserved opaquely and never interpreted.
6. Unknown critical extensions are rejected; supported critical extensions are accepted.
7. Malformed or duplicate critical_extensions declarations are rejected.

## 2. Combined schema/fixture behavior tested

All five JF-10 message families validate against the Draft 2020-12 schema. Tests cover schema version, SHA-256 digest shape, required immutable operation fields, D fence completeness attestation, I revocation cutoff proof, Storage commit pointer/receipt pairing and rollback non-publication proof.

## 3. Limits

This is a Python logical parser reference model, not the production BMCP parser or transport. It does not establish the normative canonicalization profile, cryptographic signature verification, channel binding, key custody, issuer trust, replay protection, generated SDK interoperability, cross-message owner consistency or end-to-end H/C/I/D/E/Storage runtime conformance. The JSON Schema and parser remain candidate artifacts and are NOT production-frozen.