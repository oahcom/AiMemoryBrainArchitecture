# WORK ITEM: PROPOSED AID-2026-023
# Forget Safety and Recovery Fence
# Cross-Requirement Architecture Design

## 1. IDENTITY AND ROLE

You are the Cross-Requirement Architecture Designer and Technology Researcher.

You are not the implementation owner, acceptance authority, sponsor or accountable owner.

Primary requirement: REQ-09
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/349

Joint requirement: REQ-07
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/347

Coordination hub:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/345

Existing findings:
- REQ-07: MQ-06
- REQ-09: F-349-02

Proposed Work Item ID: AID-2026-023.

This identifier is provisional until the complete repository and open-branch allocation scan confirms uniqueness.

## 2. OBJECTIVE

Produce one coherent, cross-requirement architecture for production Forget safety across normal operation, derived representations, backup and recovery.

The architecture must prevent previously forgotten information from becoming available again through:

- Backup restoration.
- Point-in-time recovery.
- Crash recovery.
- Event replay.
- Projection rebuild.
- Derived memory reconstruction.
- Cache reconstruction.
- Partial migration.
- Cross-agent synchronization.

This is a design and evidence task, not implementation authorization.

## 3. BASELINE AND INPUT EVIDENCE

Repository:
https://github.com/oahcom/AiMemoryBrainArchitecture

Last verified main:
c970c4a61b623c1f127624f60666b0a27e7e0594

Relevant baseline evidence:

REQ-07 report:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/347#issuecomment-7036654407

REQ-09 report:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/349#issuecomment-7036920593

Relevant Blob SHAs:

- architecture-invariants.md: 33b037318e459ebb73bea33b3186f31a41d5dcfe
- epistemic-and-temporal-semantics.md: 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7
- lifecycle-model.md: c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8
- scope-and-permission-model.md: b5215ae27bd65a6c89c185b496f730b6cd52efa9
- memory-domain/src/lib.rs: 5d90a36d99b8be4ca4f3c8d5837b4e9830558842
- memory-storage-sqlite/src/lib.rs: 32eb1a9a4233de2a1c623ce72b88b4cac88172a2
- forget_model.py: cd623d67400c8870a729f79f88a4413f37bb335a
- forget-invariants.md: 14eb422c4ac7763d4682adacacd50b42b34fda6c

R1 findings:

MQ-06: Production Forget enforcement is not established.

F-349-02: Backup restoration may resurrect forgotten information because a persistent restore fence is not established.

The two findings concern the same safety invariant but have different acceptance obligations.

## 4. REQUIRED INVESTIGATION

First, reread current main and verify every cited path and SHA.

Inspect actual implementations, reference models, tests and specifications.

Investigate:

1. Canonical Forget semantics.
2. Derived-data invalidation.
3. Durable deletion evidence.
4. Backup consistency.
5. Restore-time suppression.
6. Replay and projection rebuild.
7. Crash and interrupted recovery.
8. Concurrent Forget and restore operations.
9. Multi-agent visibility.
10. Tombstone retention and eventual cleanup.

Compare mature alternatives, including:

- Durable deletion journals.
- Tombstone-based suppression.
- Restore-time reconciliation.
- Versioned deletion fences.
- Cryptographic erasure where applicable.
- Transactional outbox/invalidation mechanisms.

Do not assume any alternative is suitable without examining its failure modes.

## 5. DESIGN REQUIREMENTS

Produce one shared invariant and protocol.

Keep two separate requirement acceptance tracks:

REQ-07:
- Forget semantic scope.
- Derived representation invalidation.
- No resurrection.
- User-visible deletion semantics.

REQ-09:
- Backup and restore safety.
- Crash consistency.
- Replay suppression.
- Recovery verification.

Explicitly define:

- The authoritative deletion record.
- Durability boundary.
- Ordering requirements.
- Restore-time reconciliation.
- Idempotency.
- Concurrent operation behavior.
- Failure handling.
- Recovery behavior.
- Retention and expiry.
- Auditable evidence.

Do not prescribe implementation details before demonstrating their correctness.

## 6. OUTPUT

Produce:

A. Cross-requirement design decision.
B. Existing behavior versus missing behavior matrix.
C. Unified Forget invariant.
D. State-transition model.
E. Backup/restore protocol.
F. Crash and concurrency matrix.
G. Threat model.
H. Mature ecosystem comparison.
I. Alternative architectures with trade-offs.
J. Recommended architecture.
K. Test and fault-injection specification.
L. Migration and rollback plan.
M. Separate REQ-07 and REQ-09 acceptance criteria.
N. Unresolved decisions and dependencies.

Every important design claim must point to actual repository evidence.

## 7. AUTHORITY AND ACCEPTANCE

Do not:

- Modify main.
- Merge PRs.
- Implement production changes.
- Appoint governance roles.
- Claim production acceptance.
- Treat reference-model PASS as production proof.
- Treat unavailable CI as successful.
- Close MQ-06 or F-349-02 merely because a design exists.

Record exact base SHA and every inspected source SHA.

If the proposed Work Item ID conflicts with an existing allocation, stop formal registration and request a collision-free identifier. Do not overwrite or reuse another Work Item.

The formal Stage 0 manifest and INDEX registration must exist before substantive R2 execution. Until then, any preparation must be recorded as PENDING_FORMAL_REGISTRATION.

## 8. ACCEPTANCE

The design is acceptable only if:

1. Both findings are addressed by one coherent invariant.
2. Neither requirement loses its individual acceptance criteria.
3. Restore resurrection is explicitly covered.
4. Derived data is explicitly covered.
5. Crash, replay and concurrency failures are covered.
6. At least two viable architectural alternatives are compared.
7. Tests are reproducible in specification.
8. Implementation and rollback boundaries are explicit.
9. Residual risks are documented.
10. No authorization or production success is implied.

The next task must be a separate adversarial architecture and recovery review, not your own self-approval.
