# Phase 3.6.10 — A Exact-Version Integration Re-review of R1/R2

- Role: A — Principal Integration Architect
- Decision: **ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED**
- Scope: A-COC-R1 Recovery Cutoff Batch completeness and A-COC-R2 Owner-local Gate linearization
- Provenance: **delegated role simulation authored in the coordinating ChatGPT session at the user's direction; not an independent human A Owner signature**
- Status: architecture review only; R1/R2 remain OPEN

## 1. Exact source bundle

| Source | Blob |
|---|---|
| A Phase 3.6 architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H recovery wire contract | `b4cae9c0c9121c27ea2933c029b83b3f4367672b` |
| H recovery schema 1.0.4 | `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1` |
| H semantic validator contract | `7e6f67518e476fe9798f23a87798c7a3eb352f3c` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |

## 2. Exact delegated role review records

These are role simulations and do not satisfy independent Owner approval:

| Role | Decision artifact Blob | Disposition |
|---|---|---|
| I | `a0fee9ef41c52ea3948286e6ec9a348cc1b17168` | ACCEPT WITH ENUMERATED AMENDMENTS |
| D | `e03ca0db209fc8ac5b985e114a31c21fbb136859` | ACCEPT WITH ENUMERATED AMENDMENTS |
| C | `694b19dd5c52db1b8206c0f5986464bd64194cbd` | ACCEPT WITH ENUMERATED AMENDMENTS |
| H | `1de7d30f3ca81bc579b396acb0f05e2ead5fe9dd` | ACCEPT WITH ENUMERATED AMENDMENTS |

## 3. Integration analysis

### R1 — Recovery Cutoff Batch completeness

The model now has three distinct completeness domains:
1. I/D/C owner-local request sets;
2. I/D/C owner-local admission/receipt/work/reservation/provider-attempt sets;
3. the COC quorum-committed ParticipantIntent prefix set.

H 1.0.4 requires owner-specific high-waters, separate request/admission arrays and roots, explicit empty-state vocabulary, typed COC participant entries and mandatory owner-admission identity. The H semantic validator contract specifies count/root, canonical order, complete-prefix enumeration, cross-set joins and release cardinality. Storage/COC remains the durable coordinator/participant authority and does not assume owner-local ledger completeness from its own prefix.

**A finding:** R1 is now substantially specified at the documentation level. It remains OPEN because the validator is not implemented or run, the authoritative owner/COC sources have not produced signed completeness evidence, and no executable proof demonstrates that every affected owner admission and every pre-batch COC participant is joined without omission.

### R2 — Owner-local Gate linearization

I specifies the I-sequencer close transaction and same-sequencer receipt issue/consume fencing. D specifies the D-local fence transaction and generation enforcement at every admission and final publication boundary. C specifies the C-local close transaction and a final egress gateway boundary: reservation is not provider invocation; a reserved/not-dispatched attempt cannot send after Gate close; a sent/ambiguous pre-close attempt is reconciled by the same key. Each owner retains sole release authority.

**A finding:** R2 is now substantially specified at the documentation level. It remains OPEN because no concrete I/D/C implementation proves the local transaction/CAS boundaries, no C adapter proves provider egress serialization against Gate close, and no fault test proves final release currentness against concurrent high-water/scope changes.

## 4. Blocking conditions before R1/R2 closure

1. Execute H semantic validators and the HRC-01..25 positive/negative vectors, including exact canonical bytes, root recomputation, prefix pagination, participant identity uniqueness and bidirectional join.
2. Obtain authoritative I/D/C owner-signed snapshot, completeness, and release evidence from their own services; delegated role documents are not signatures.
3. Demonstrate I gate-close vs receipt issue/consume races, including lost ACK, stale cache, leader change and restore.
4. Demonstrate D fence-close vs every admission and final publication boundary, including stale worker and late-discovery races.
5. Demonstrate C gate-close vs actual provider egress, including gate-close-wins, send-wins, ambiguous send, same-key recovery and adapter partition.
6. Demonstrate Storage/COC exact prefix/manifest/batch joins, with no missing page, omitted participant or fabricated owner sequence.
7. Demonstrate final I/D/C owner-release compare-and-commit after re-reading current scope, high-waters, roots, inventory/lineage and anti-rollback state.
8. Obtain independent exact-version I/D/C/H Owner decisions and a fresh A review after any normative amendments.

## 5. Decision and gate status

A accepts the proposed composition as a coherent architecture direction but **does not close R1 or R2**.

- R1: SUBSTANTIALLY SPECIFIED / OPEN
- R2: SUBSTANTIALLY SPECIFIED / OPEN
- Issue #14: OPEN
- JF-10 P0: OPEN
- Multi-PolicyDomain atomicity: BLOCKED
- Implementation/conformance: NOT RUN
- Production activation: NOT AUTHORIZED

No protocol/schema/cryptographic freeze, deployment, production readiness or implementation authorization is implied.
