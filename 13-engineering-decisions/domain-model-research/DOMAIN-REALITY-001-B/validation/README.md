# Validation Package
# 验证包

- Status: SPECIFICATION ONLY — no executable tests run
- Reason: core Fact/Claim, typed-reference field grammar, Context schema, Applied wire mapping and JF-10 storage interface are not frozen. The repository has no runtime implementation in main; Issue #7 requires the authoritative runtime repository and engineering owner to be identified.

## Included test specifications
- See ../canonical-domain-invariants.md, Section 8.
- Identity, relationship, temporal, evidence, state, Forget/deletion and protocol invariants are enumerated with positive/negative conditions and owner assignments.

## Schema disposition
No normative JSON Schema is emitted in this pass. Doing so would freeze unresolved field names and requiredness. Candidate schemas may be created only after:
1. B Fact/Claim and Claim identity ADR closure;
2. I/B typed reference grammar and namespace acceptance;
3. G ContextVersion/ChangeSet/Applied exact schema acceptance;
4. H wire schema and C/G/H Applied package acceptance;
5. D/E/Storage publication/Forget gate interface acceptance.

## Required future validation
- JSON Schema Draft 2020-12 meta-schema validation for stable serialized contracts.
- Positive and negative fixture suites for each entity/reference/state.
- Property-based tests for ID non-reuse, version monotonicity, relation endpoint constraints, scope isolation and idempotency.
- Fault-injection tests for D fence vs publication, I revocation vs submit, same-XID recovery and restore quarantine.
- Bilingual semantic parity check.
- Owner-specific executable tests in the canonical runtime implementation repository.

## Current result
- Schema validation: NOT RUN / NOT CREATED
- Unit/integration tests: NOT RUN
- Property tests: NOT RUN
- Fault injection: NOT RUN
- Runtime implementation evidence: NOT VERIFIED
