# COC outage-recovery logical reference model

This directory contains an in-memory deterministic model of the Causal Order Coordinator's outage recovery batch for `CGH-APPLIED-1.1`.

Run from this directory:

```bash
python -m unittest discover -v
```

The model covers:
- I/D owner-local pending gates while COC is unavailable;
- fail-closed rejection of new affected intents/submits;
- one recovery-cutoff batch containing I and D request sets without deriving cross-owner order from local clocks;
- enumeration of all affected pre-batch ParticipantIntentRefs;
- owner-specific reconciliation and high-water checks before local gate release;
- RESTORE_FENCED for missing committed prefix or incomplete owner request sets;
- immutable request identity/digest conflict.

**Limitations:** all state is in-memory. This is not a Raft/consensus implementation, production COC, I sequencer, D fence service, durable owner gate, HA/failover/restore or cross-protocol transaction. A passing model suite is not COC-01..16 production conformance and cannot establish deployment or G10 acceptance.

The branch-scoped GitHub Actions workflow `.github/workflows/coc-recovery-reference-model.yml` runs this logical model suite on changes.
