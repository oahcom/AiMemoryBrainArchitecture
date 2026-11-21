# Memory Compiler reference model

Contract-level Python reference model only.

Run from repository root:

```sh
python3 -m unittest discover -s 04-memory-compiler/reference-model -p 'test_*.py' -v
```

No external dependencies are required (Python 3 standard library only). The model does not persist state and does not implement a production compiler.

## Stage-to-test coverage

The table maps the six stages in the compiler stage contract to the current ten unit tests. “Not covered” is an explicit scope statement: passing tests establish only the listed examples, not the complete stage contract.

| Stage | Contract clause | Covered tests | Semantics not covered |
|---|---|---|---|
| Ingest | §3 — Ingest | `test_ingest_is_deterministic`; `test_ingest_fails_closed_on_missing_scope` | No test for same event ID with a different digest conflict; malformed event-envelope/custody fields and multiple SourceMemory outputs are not exercised. |
| Validate | §3 — Validate | `test_validation_rejects_digest_mismatch` (indirectly: `normalize` rejects a source whose content no longer matches its digest) | No direct validation-stage API test; missing identity/content, invalid scope, unsupported encoding, and typed retryability/error metadata are not covered. |
| Normalize | §3 — Normalize | `test_normalize_is_deterministic_and_retains_digest`; `test_validation_rejects_digest_mismatch` | Normalizer ID/version changes, unsupported encodings, ambiguous structures, and normalizer failures are not tested. |
| Derive | §3 — Derive | `test_derive_identity_is_stable`; `test_derive_rejects_empty_inputs` | Multi-parent merge ordering and output content semantics are not asserted; transformation exceptions/invalid output, transformation-version changes, and canonical parameter serialization are not tested. |
| Provenance | §3 — Provenance; §4 — Required provenance fields and Traceback termination | `test_provenance_resolves_root_sources_and_event_anchors`; `test_provenance_rejects_missing_parent`; `test_provenance_rejects_cycles`; `test_provenance_requires_at_least_one_parent` | Transitive derived-parent chains and digest mismatch during traversal are not directly tested. Multiple event anchors per source are not representable in this reference model (each `SourceMemory` has only one `source_event_id`), so preservation of multiple anchors is not implemented here, not merely untested. Duplicate-root de-duplication/sort order and all required-field/alignment invariants are not comprehensively tested. |
| Publish gate | §3 — Publish gate; §5 — Cross-owner decisions | No direct test. `test_derive_identity_is_stable` covers candidate identity only, not the gate. | Policy/authority decision availability, fail-closed publication blocking, Owner I permission outcomes, Owner D canonical acceptance, concurrent publication races, and publisher idempotency are not tested or implemented. |

The suite contains ten tests and intentionally does not claim full semantic coverage of any stage. In particular, the Publish gate is a contract boundary only; this reference model has no publication side effect.
