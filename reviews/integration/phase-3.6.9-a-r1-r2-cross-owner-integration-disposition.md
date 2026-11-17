# Phase 3.6.9 — A Cross-Owner Integration Disposition for R1/R2

- Role: A — Principal Integration Architect
- Decision: **ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED**
- Scope: A-COC-R1 Recovery Cutoff Batch completeness and A-COC-R2 Owner-local Gate linearization
- Provenance: **delegated role simulation authored in the coordinating ChatGPT session at the user's direction; not an independent human A Owner signature**
- Status: architecture integration review only; R1/R2 remain OPEN

## 1. Exact integrated source bundle

| Source | Blob |
|---|---|
| A architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC durable protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H wire contract | `707ed85642ba4b0275c4ec851d599fde28ec6cae` |
| H recovery schema 1.0.3 | `9c3b98abab0c04a241a93c5e6f02e9424059b07b` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |

## 2. Role decision records reviewed

The following are assistant-authored delegated role simulations, not independent Owner approvals:

| Role | Decision record Blob | Disposition |
|---|---|---|
| I | `6bf56407721f1271f315d799f9bd57055393c176` | ACCEPT WITH ENUMERATED AMENDMENTS |
| D | `7ab4f53c497bce597e422a6df9a85b31a2352602` | ACCEPT WITH ENUMERATED AMENDMENTS |
| C | `a26f9631021917955dd93ee1234fe2fbeac7cfd1` | ACCEPT WITH ENUMERATED AMENDMENTS |
| H | `3595221167cde69eaabf95fe7926440c4ca92822` | ACCEPT WITH ENUMERATED AMENDMENTS |

Storage's cross-owner follow-up review is Blob `aefd9e74849f650df4a715f05bb83a6ad8150210`.

## 3. A integrated finding

### R1 — Recovery Cutoff Batch completeness

The architecture now correctly separates three sets:

1. I/D/C owner-local request sets;
2. I/D/C owner-local admission/receipt/work/reservation/provider-attempt sets;
3. COC's exact quorum-committed ParticipantIntent prefix set.

The H 1.0.3 candidate carries separate request and admission roots, owner-specific high-waters, typed participant manifest entries, and batch references to I/D/C snapshots. The Storage/COC design preserves exact prefix and immutable recovery rounds. Post-high-water requests remain gated and require subsequent rounds.

**A finding:** semantically coherent direction, but R1 is not closed because schema structure is not proof of set completeness. A still requires an authoritative cross-message join proof, complete prefix enumeration, count/root/canonical-order validators, exact owner membership coverage, and current I inventory/D projection checks at release. A missing owner set or missing page cannot be interpreted as empty.

### R2 — Owner-local Gate linearization

I and D each define one owner-local durable close transaction/CAS and same-domain fencing at protected effect boundaries. C now adds the final provider-egress boundary, distinguishing reservation from actual outbound send and preventing a reserved/not-dispatched attempt from being sent after C Gate close. The Storage/COC authorities remain separate and cannot release owner gates.

**A finding:** the local linearization architecture is coherent as a specification, but R2 is not closed. No executable proof currently demonstrates:
- I receipt issue/consume racing I gate close;
- D admission/final publication racing FenceGeneration;
- C final egress send racing CGateGeneration;
- high-water/scope change racing final owner-release CAS;
- crash/lost ACK/partition/restart preserving the same ledger and gate generation.

C's egress adapter is a particularly important boundary: a process-local check followed by an unrelated provider network call cannot establish the required ordering. If the adapter cannot serialize the send boundary or enforce a current fencing capability, it must fail closed.

## 4. Blocking clarifications before closure

1. **Semantic H validator:** count equals array length; canonical order/root; explicit empty digest; no null/missing substitution; unique owner entry and ParticipantIntentRef; exact COC prefix completeness; exact I/D/C release cardinality; no stale/downgraded schema.
2. **Bidirectional set join:** every REGISTERED owner entry maps to exactly one COC manifest participant and every affected COC participant maps to an accountable owner entry/class. NOT_REGISTERED entries remain explicit owner-local obligations.
3. **I currentness:** release CAS revalidates PermissionEpoch, IGateGeneration, ProducerDomainInventoryEpoch, registry digest, relevant entry generations, TargetInventorySeal and anti-rollback.
4. **D currentness:** release CAS revalidates FenceGeneration, I registry projection, lineage/dependency closure, terminal publication/no-publication proofs and restore checkpoint identity.
5. **C egress:** concrete gateway proves send-vs-gate-close serialization, same-key recovery and no send after gate close for NOT_DISPATCHED attempts.
6. **Storage/COC:** immutable participant manifest, exact pre-batch prefix/root, owner-local admission roots and recovery-round chaining must be reconciled without synthetic cross-owner sequence or authority substitution.
7. **Independent exact-version Owner decisions:** I/D/C/H must publish their own decisions from their own Owner sessions/branch governance. The delegated records above cannot satisfy this predicate.
8. **A fresh review:** after independent decisions and any normative amendments, A must pin one immutable bundle and issue a new exact-version integration disposition.

## 5. Decision

A accepts the direction of the proposed R1/R2 composition but **does not accept closure**.

- R1: SUBSTANTIALLY SPECIFIED / OPEN
- R2: SPECIFIED IN OWNER CANDIDATES / OPEN
- Issue #14: OPEN
- JF-10 P0: OPEN
- Multi-PolicyDomain atomicity: BLOCKED
- Implementation/conformance: NOT RUN
- Production activation: NOT AUTHORIZED

This decision does not freeze the COC protocol, H schema, cryptographic profile, database adapter or production topology. No merge or deployment is authorized.
