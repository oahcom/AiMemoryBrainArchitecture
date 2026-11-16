# I Owner — Exact Restore IControlHighWaterProof Boundary Acceptance

- Exact Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- I PermissionEpoch/authorization contract Blob: `17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c`
- I Global Forget inventory contract Blob: `9100061fa986fb6676656169de3fcf9fc1c72664`
- Decision: **ACCEPT WITH I-OWNED CONTROL-HIGH-WATER / GOVERNANCE CONDITIONS**
- Mode: delegated I technical-boundary review; not external governance approval or independent human signature.

I accepts the IControlHighWaterProof semantic boundary:

1. One proof is issued per affected PolicyDomainRef and binds the current opaque PermissionEpoch, I sequencer epoch/position within that domain, revocation/control-ledger high-water and digest, current ProducerDomainInventoryEpoch, producer/recipient registry digest, signer/key version, audience and verification time.
2. For each active ForgetOperation affecting the restored dataset, the proof references the current I TargetInventorySeal and digest. Missing, stale or invalid seal, registry gap or epoch change blocks restore release.
3. PermissionEpoch values from different PolicyDomainRefs are never compared, maxed or collapsed. The restore process must preserve each independent proof.
4. IControlHighWaterProof is a current control-state snapshot, not an authorization grant, D fence clearance, COC commit proof or Storage visibility receipt. Storage cannot mint or reinterpret I's decision.
5. Storage rechecks I high-waters immediately before its RestoreReconciliationReceipt. If revocation, trust, policy or inventory epoch advances during restore, the proof is stale and reconciliation repeats.
6. The restored service still revalidates current I authorization at each protected commit/disclosure boundary. Restore reconciliation does not grandfather stale ALLOW, offline lease or old session.

Exceptions: I sequencer proof API, signed proof format, audience/key verification and real restore integration are NOT IMPLEMENTED / NOT RUN. I36-GOV-01..10 remain GOVERNANCE-BLOCKED / NOT APPROVED; this technical acceptance does not approve issuer trust, delegation, cross-Scope/Environment grants, offline leases, retention exceptions, Global Forget completion or physical erasure.