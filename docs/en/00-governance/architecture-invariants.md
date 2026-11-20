# Architecture Invariants

- Document ID: GOV-INV-001
- Version: 1.1
- Source: [Normative source specification](../../../00-governance/architecture-invariants.md)
- Chinese counterpart: [架构不变量](../../zh-CN/00-governance/architecture-invariants.md)
- Status: DECIDED baseline

These invariants are normative constraints for all subsystem specifications and future implementations.

| ID | Invariant |
|---|---|
| I-01 | The Brain is the logical authority for canonical memory assets and the memory context it manages. |
| I-02 | Agents do not define or override the Brain's internal memory organization rules. |
| I-03 | The Brain is independent of any specific Agent framework, LLM, or inference vendor. |
| I-04 | Event, Memory, Fact, Entity, Relation, and Evidence are distinct domain concepts. |
| I-05 | Every derived memory retains provenance to its source evidence or explicitly records why provenance is unavailable. |
| I-06 | Intent, plan, prediction, and pending action are not automatically treated as completed outcomes or verified facts. |
| I-07 | Editing Memory Context does not directly mutate Canonical Memory. |
| I-08 | Removing a context entry is not equivalent to forgetting or deleting its canonical memory. |
| I-09 | Context changes are versioned and tied to a base version or an explicit full-snapshot transition. |
| I-10 | A context delivery is Applied only after explicit Adapter acknowledgement. |
| I-11 | Context changes take effect at a defined inference-context assembly boundary. |
| I-12 | Memory content is untrusted data and never acquires system/developer instruction authority. |
| I-13 | Scope and permission are explicit and independently enforced; Agent, task, session, and environment isolation is preserved. |
| I-14 | Conflicting claims are not silently overwritten; provenance and resolution history remain auditable. |
| I-15 | Event time, recording time, and validity time are not conflated. |
| I-16 | Retries of state-changing protocol operations are idempotent under their defined idempotency scope. |
| I-17 | A context version has one authoritative sequence; concurrent changes are serialized or resolved with explicit concurrency control. |
| I-18 | Adapter acknowledgement proves protocol-level application, not model comprehension or behavioral compliance. |
| I-19 | Context compaction preserves source references and the ability to expand details when retained data permits. |
| I-20 | Forgetting and retention governance cover derived records and secondary representations according to declared policy. |
| I-21 | A subsystem boundary does not imply a separate process, service, or crate. |
| I-22 | Performance claims require reproducible measurement on declared hardware, data, and workload. |
| I-23 | Every architecture design or semantic architecture change must include Chinese and English documentation in the same change set, subject only to the governed temporary exception in GOV-DOC-001. |
| I-24 | Architecture documentation acceptance requires bilingual semantic parity, stable-identifier parity, matching decision status, and traceable source revisions. |

## AID-2026-014 Claim/Fact semantic invariants

- Claim and Fact are independent canonical objects.
- Claim identity is stable across proposition-preserving revisions.
- ClaimRevision is immutable and must be addressed by exact ClaimRevisionRef.
- FactRevision must bind exact ClaimRevisionRef, Evidence, Provenance, Scope, Attestor and Method/Version.
- FactRevision must retain the exact I authorization decision reference.
- F and G must not substitute current-head or semantic-similarity resolution for exact historical revision references.
- Forget enforcement must cover shared Fact dependencies and every declared alternate read path.
- These are semantic invariants, not Schema, DDL, public API or implementation-acceptance approvals.

## Enforcement expectation

Each subsystem specification must identify which invariants it enforces, which it relies on, and how violations are detected and handled. An implementation review must not waive an invariant implicitly; a change requires an explicit architecture decision record and impact analysis.

All architecture Owners must comply with [GOV-DOC-001 Bilingual Architecture Documentation Policy](../../../00-governance/bilingual-documentation-policy.md). A temporary STALE exception must be explicit, time-bounded, and tracked.
