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
