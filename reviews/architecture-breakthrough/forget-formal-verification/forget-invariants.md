# Forget Invariants — F1 to F8

Legend: LOGICAL MODEL PASS means the bounded model passes under stated transition assumptions. NOT PROVEN means repository evidence is insufficient for a production claim.

| ID | Invariant | Logical disposition | Repository / production disposition |
|---|---|---|---|
| F1 | No resurrection | PASS under persistent monotonic Fence, restore high-water and fail-closed reads | NOT PROVEN; restore implementation and every projection read gate are not physically verified |
| F2 | No stale publication | PASS under final D Fence check in the same atomic visibility boundary | NOT PROVEN; Storage/D/E atomic realization remains open |
| F3 | Admission safety | PASS if admission and Fence share one serialization domain and post-Fence lineage is rejected/quarantined | NOT PROVEN; D semantics exist, E/Storage integration remains candidate/open |
| F4 | Dependency completeness | NOT PROVEN at cross-module composition level | I closed-world producer/recipient inventory and seal governance remain blocked; E derivative closure is Candidate |
| F5 | Visibility safety | PASS in abstraction when all reads/disclosures revalidate latest Fence | NOT PROVEN; F/G/H implementation and end-to-end conformance absent |
| F6 | Idempotency | PASS for stable operation+digest, immutable receipt and ACK-loss retry | PARTIAL; D defines idempotency, G Applied is draft, cross-owner terminalization proposal not accepted |
| F7 | Restore fencing | PASS when durable D/I/COC/Storage high-waters survive and release is fenced | NOT PROVEN; restore model is candidate and physical backup/PITR/HA campaign not evidence of full protocol |
| F8 | Crash consistency | NOT PROVEN | No integrated production transaction/runtime; JF-10 cross-authority crash-atomic coupling remains P0 open |

## Conditions

- F1 fails if restore activates a snapshot whose Forget high-water is older than current durable Forget epoch.
- F2 fails if a worker publishes based only on admission-time token without a final authoritative check at commit.
- F3 fails if registration races independently with Fence installation or retry creates a new untracked work identity.
- F4 requires both D's concrete admitted-work high-water and I's complete producer/recipient-domain inventory; neither substitutes for the other.
- F5 includes candidate generation, index lookup, cache hit/write, final result serialization, Context snapshots/deltas, delivery and Adapter reconnect.
- F6 requires same-key/same-digest replay to return the same durable outcome; same-key/different-digest must conflict. Lost ACK must not undo a durable receipt.
- F7 requires restore to preserve monotonic control state, verify contiguous COC prefix, exact I/D high-waters, Storage participant ledger and visibility-pointer/receipt pairing, then recheck stability before release.
- F8 includes crash before/after every durable boundary, unknown outcomes, stale replicas, failover and prepared participant recovery.

No F invariant is certified for production by this report.
