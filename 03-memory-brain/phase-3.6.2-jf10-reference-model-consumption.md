# D Owner — JF-10 Executable Reference Model Consumption

- Status: **REFERENCE-MODEL MAPPING / OWNER REVIEW REQUIRED**
- Model source: Storage Owner branch, `reviews/storage-consistency/reference_model/jf10_linearization_model.py`
- Scope: logical D fence/publication ordering only; not production D implementation.

## D-owned behavior represented

The reference model's `DPublicationGate` represents two mandatory orderings:

1. **Fence-first:** once D closes the publication gate and advances ForgetFenceGeneration, a prepare carrying the old generation or arriving while closed is rejected.
2. **Participant-first:** once a Storage participant is prepared under the current D generation, Forget cannot advance the fence until that exact participant reaches a terminal COMMIT/ABORT resolution.

The model retains the prepared-operation marker while the participant is UNKNOWN/IN_DOUBT. It releases the marker only after terminal recovery. This is the logical behavior covered by JF10-D-14..15.

## Required production mapping

D implementation must identify the authoritative ForgetFence and barrier/dependency ledger, the transaction/lock boundary shared with Storage, the captured generation carried by the publication intent, and the recovery signal that permits fence advancement. A local cache or process mutex is not sufficient.

## Explicit non-claims

This model does not implement D's durable fence, ProducerWork/Dependency ledgers, distributed lock, serializable database transaction, or crash recovery. It does not pass D36 or JF10-D-14..15. D owner review and production-equivalent evidence remain required.
