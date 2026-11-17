# Counterexample Catalog

These shortest traces are found by mutating one required guard in the abstract model. They show why the guard is necessary; they are not claims that production executed these traces.

| ID | Mutated guard | Shortest trace | Violated invariant | Minimal repair |
|---|---|---|---|---|
| CE-01 | Worker publication omits final Fence recheck | admit → install_fence → publish | F1/F2 | Final authoritative Fence + lineage check inside atomic visibility transaction |
| CE-02 | Admission is not serialized with Fence | install_fence → admit | F3/F4 | Same D serialization domain; post-Fence admission rejected/quarantined |
| CE-03 | Index rebuild omits Fence validation before segment swap | admit → publish → install_fence → rebuild_index | F1/F5 | Build from canonical snapshot plus replay; validate latest Fence immediately before atomic segment swap and on retrieval |
| CE-04 | Cache refill omits current Fence check | admit → publish → install_fence → repopulate_cache | F1/F5 | Cache key binds D Fence context; every hit and fill revalidates current authority; fail closed on unknown |
| CE-05 | Restore accepts stale backup and drops Forget high-water | install_fence → restore | F1/F7 | Restore quarantine; replay and verify current control high-waters; prevent service release until stable recheck |

Additional races: lost ACK after durable receipt must reuse the same operation and digest; overlapping Forget operations preserve the maximum applicable generation; derived registration before Fence is included in the barrier and after Fence is rejected/quarantined; unresolved prepared Storage participants remain private; late discovery invalidates prior closed-world proof and reopens reconciliation.

Reproduce all traces with model/forget_model.py.
