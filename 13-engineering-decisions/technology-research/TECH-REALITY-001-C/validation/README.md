# Validation Assets / 验证资产

## Status
- Design scenarios: 20 defined in `agent-integration-validation-plan.md`.
- Executable provider adapter tests: NOT RUN.
- Real provider tests: NOT RUN.
- Real tool side-effect/recovery tests: NOT RUN.
- C/H cryptographic profile registration: NOT RUN / NOT REGISTERED.
- H Unified 1.2.15 exact validator CI: NOT VERIFIED in this C pass.
- G Applied end-to-end tests: NOT RUN / NOT VERIFIED.
- Forget-vs-late-result fault injection: NOT RUN.
- Performance benchmarks: NOT RUN.

## Required future assets
1. Version-pinned Provider capability fixtures per provider/model/API.
2. Streaming transcripts: complete, partial, malformed, disconnected, duplicated and late terminal events.
3. Request/Attempt idempotency and timeout race fixtures.
4. Tool side-effect lost-ACK fixtures with external reconciliation.
5. CSubmitOutcome 1.0.1 schema and cryptographic vectors from exact C owner branch.
6. H exact-version 1.2.15 schema/validator/CI bundle from H.
7. G Applied predicate fixtures and D Forget fence/lineage race fixtures.
8. Redaction tests with synthetic secrets and sensitive content.
9. Trace propagation tests across process boundaries and untrusted ingress.
10. Cross-tenant authorization negative fixtures owned/approved by I.

No production secrets, live user memory or real personal data may be used in synthetic conformance fixtures.
