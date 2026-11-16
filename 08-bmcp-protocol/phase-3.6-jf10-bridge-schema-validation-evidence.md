# H Phase 3.6 — JF-10 Bridge Schema Validation Evidence

- Branch HEAD: `eab7ee9d196437daed31d5853570b7fb7acf08b6`
- Schema: `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json`, Blob `a8a945cc3623c2907003b93625e3c79742150944`
- Test: `tests/schema/test_jf10_bridge_schema.py`, Blob `74bc4286abe1489ce29c2446c6fc22445784609f`
- Workflow: `.github/workflows/jf10-bridge-schema.yml`, Blob `5201c22b512bf7ed2c227b06c3e3aba0bba8b91a`
- CI run: `43962364955`; job `133632849768`; commit `eab7ee9d196437daed31d5853570b7fb7acf08b6`
- Result: **11/11 TESTS PASS**

## 1. Executed validation

1. Draft 2020-12 schema self-validation.
2. Exactly five distinct message_type variants.
3. One valid minimal fixture for each of the five message families, with root oneOf selecting exactly one variant.
4. Invalid SHA-256 payload digest rejected.
5. Wrong schema version rejected.
6. Missing immutable PublicationOperationId rejected.
7. Empty D fence request set requires D completeness attestation.
8. I revocation PRESENT requires owner cutoff proof.
9. Storage COMMITTED requires PublicationReceipt + VisibilityPointer transaction.
10. Storage ROLLED_BACK requires non-publication proof and forbids visibility fields.
11. Cross-message reconciliation truth is explicitly left to semantic validator/owner lookups rather than inferred from schema shape.

## 2. Exact CI outcome

Workflow run `43962364955` concluded SUCCESS. The raw job log reports 11 tests in 0.160 seconds and `OK`.

## 3. Limits

This validates JSON Schema structure and field-shape constraints only. It does not validate duplicate JSON key rejection/canonicalization, cryptographic signature or channel binding, issuer trust, cross-message owner consistency, unknown critical extension rejection, generated SDK interoperability, transport replay, or any live H/C/I/D/E/Storage runtime. The schema remains a candidate and is NOT production-frozen.