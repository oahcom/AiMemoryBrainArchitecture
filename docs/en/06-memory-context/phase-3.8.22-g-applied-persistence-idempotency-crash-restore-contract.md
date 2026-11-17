# G Applied Persistence, Idempotency, Crash Recovery and Restore-Fencing

- Canonical normative source: `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md`
- Chinese normative peer: `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`
- Status: **REFERENCE MODEL AVAILABLE; PRODUCTION IMPLEMENTATION NOT VERIFIED**

## Reader summary

G alone owns the durable Full Applied decision. A C `HANDOFF_ACCEPTED` is necessary but insufficient. G must join the exact C Provider Attempt/Outcome, authenticated H delivery evidence, COC participant/terminal proof, current I authorization, D ForgetFence, applicable Storage same-GID terminal result, and G Context/Delivery predicates.

The G Phase 3.8.22 contract defines the logical Applied identity, evidence-revision rules, same-identity/same-digest replay, changed-digest conflict quarantine, crash/restart behavior and restore fencing. Its exact Owner acceptance and production implementation requirements remain normative in the canonical source.

## Executable reference evidence — 2026-11-18

Merged PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) adds a bounded single-node SQLite reference model under `06-memory-context/reference-model/`.

- Exact PR-head run [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388): SUCCESS.
- Post-merge main run [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305): SUCCESS on main commit `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf`; 8 tests passed.
- Covered: positive HANDOFF_ACCEPTED commit; idempotent same-digest replay; changed-digest conflict without overwrite; rejection of all four non-success C outcomes; fail-closed missing/false gates; restart/readback; distinct identities; exact identity field-set validation.

## Evidence ceiling

This reference model is not production G runtime code or G Owner acceptance. It uses one local SQLite database and caller-supplied gate booleans. It does not prove multi-replica linearization, distributed restore fencing, current-use revalidation after later I/D changes, live C/H/COC/I/D/Storage authority resolution, cryptographic authentication or production durability topology. Production G Applied and cross-owner Full Applied remain **NOT VERIFIED / NOT FROZEN**.
