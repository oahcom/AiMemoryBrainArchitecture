# Reader mirror for the Chinese G Applied persistence contract

This English reader mirror corresponds to the canonical Chinese normative source:
`06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`.

The contract assigns the durable Full Applied decision exclusively to G. C `HANDOFF_ACCEPTED` is necessary but insufficient; G must join C Provider Outcome, authenticated H evidence, COC participant/terminal proof, I authorization, D ForgetFence, applicable Storage same-GID resolution, and G Context/Delivery predicates.

Merged PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) adds a bounded single-node SQLite reference model. Exact PR-head run [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388) and post-merge main run [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305) passed; the latter is pinned to main `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf` and reports 8 tests OK.

This is a reference/conformance prototype, not production G runtime or Owner acceptance. It does not prove multi-replica linearization, distributed restore fencing, current-use revalidation, live authority resolution, cryptographic authentication or production durability. Production G Applied and cross-owner Full Applied remain **NOT VERIFIED / NOT FROZEN**.
