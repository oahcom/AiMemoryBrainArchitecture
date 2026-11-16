# JF-10 Linearization Reference Model

**Status: executable logical reference model; NOT production implementation.**

This package turns the single-policy-domain JF-10 protocol into a deterministic
state-machine model for D/E/Storage review. It covers:

- stable WorkItemId / PublicationOperationId binding and E retry fencing;
- I-style terminal decision immutability and one-policy-domain rejection;
- Storage prepare, IN_DOUBT, same-XID recovery, abort and receipt consumption;
- the modeled atomic publication invariant across VisibilityPointer,
  PublicationReceipt, owner outcome, receipt-consumption evidence and outbox;
- D fence-first rejection and participant-first fence blocking.

## Run

From the repository root:

    python -m unittest discover -s reviews/storage-consistency/reference_model -v

## Critical limitations

This model uses in-memory maps and is intentionally not a production coordinator,
transaction manager or persistence implementation. It does NOT prove:

- durable coordinator log or I sequencer behavior;
- actual database prepared-XID durability or lock retention;
- serializable isolation across D and Storage authoritative rows;
- coordinator/DB HA failover, backup/restore, replication or split-brain safety;
- real receipt signing, verification, revocation, InventorySeal validation;
- object-store, cache, index, reader and outbox integration.

A passing result means only that the modeled logical invariants hold for these
deterministic cases. G3 remains blocked; JF-10 P0 remains open; production
conformance remains NOT RUN until the designated runtime repository, database,
coordinator and owners are identified and exercised.


## Crash-injection boundaries

The test suite now injects a crash immediately before the modeled local publication commit and immediately after the atomic PublicationRecord insertion. Before-commit crash must leave the operation IN_DOUBT, invisible, and fenced/prepared. After-commit crash must preserve reader visibility through the atomic record; recovery reconstructs readback projections (VisibilityPointer, PublicationReceipt, owner outcome, receipt consumption and outbox) from that record. These are deterministic in-memory fault points, not process-kill or database crash tests.

A branch-scoped GitHub Actions workflow is provided at `.github/workflows/jf10-reference-model.yml` to run the unittest suite on changes and pull requests. A workflow definition is not itself evidence of a successful CI run; retain NOT RUN until a concrete successful run is observed.

## Phase 3.6 COC boundary clarification

The JF-10 model is separate from the A Causal Order Coordinator (COC) model proposed for `CGH-APPLIED-1.1`. It models only the D/E/Storage single-policy-domain publication participant boundary described in this repository. It does not model COC quorum ordering, I/D outage recovery batches, a COC-to-JF-10 atomic bridge, production I sequencer behavior, or cross-system atomicity.

The Storage Owner's exact COC boundary decision is recorded in `reviews/storage-consistency/phase-3.6-coc-storage-boundary-acceptance.md`. A passing JF-10 reference-model suite remains a logical-model result only and cannot close COC-01..16, JF10-01..17 production conformance, Storage C01..C23, or Phase 3.6 G10.

This documentation update intentionally triggers the branch-scoped JF-10 logical-model CI workflow. The workflow result, if produced, must be recorded separately from production conformance.
