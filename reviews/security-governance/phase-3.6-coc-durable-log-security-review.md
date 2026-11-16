# I Owner Review — COC Durable Log, Owner-local Gates & JF-10 Bridge

- Reviewer: I — Security & Governance Architect
- Review target: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design.md`
- Exact target: commit 9a975f665ee60f4551effe0104ea8f867716d9dd; blob cd5566b3d99b5204401ac713a5bb2dcf89a02726
- Decision: **NEEDS_REVISION**
- Scope: I authority, security invariants and governance controls. This is not external governance approval, production activation or implementation verification.

## 1. Accepted within I authority

I accepts COC as a cross-authority causal-order/evidence service only when it records I-issued evidence without minting, altering, inferring or reversing I authorization, PermissionEpoch, revocation victory or JF-10 terminality. The proposal correctly keeps COC positions separate from I sequencer positions and correctly requires durable I/D pending gates while COC is unavailable. The common recovery batch may bind I and D request inventories but must not order them by owner-local clocks.

The proposal's fail-closed defaults, quorum-confirmed append, linearizable reads, stable-key/digest idempotency, hard conflict, leader recovery fencing, restore fencing, two-person high-risk recovery and non-expiring IN_DOUBT are necessary controls.

## 2. Blocking findings

### I-COC-01 — JF-10 composition exceeds the current I COC disposition (BLOCKING)

I's current composition disposition accepts COC as the CGH cross-authority order input and explicitly does **not** approve automatic COC↔JF-10 composition. The COC proposal includes a JF-10 same-XID bridge as if it were part of this COC persistence contract. This may be developed as a separately governed interface, but it cannot be treated as accepted by I merely because I previously accepted a different exact JF-10 v2 bundle.

Required amendment: label the JF-10 section a proposed, separately gated bridge; pin the exact I JF-10 v2 owner disposition and require fresh exact-version I acceptance of this proposal's composition. Do not infer that the COC recovery batch decides or clears the I owner gate.

### I-COC-02 — Exact owner-final-gate participant must be explicit (BLOCKING)

I's binding JF-10 requirement is that the sequenced operation is the exact Storage owner-final visibility gate, not a detached COMMIT_WON authorization token followed by an independent Storage commit. The proposal must bind owner_boundary, stable participant, XID, DB identity, participant digest, operation ID/digest, policy domain, PermissionEpoch, single-use receipt consumption and I sequencer position in one I coordinator transaction. Storage then resolves that exact prepared participant; visibility is not implied by I COMMIT.

### I-COC-03 — Recovery batch completeness proof needs an atomic definition (BLOCKING)

§5.3 appends the batch before enumerating pre-P participants, while the record definition says the batch contains participant enumeration high-water. This leaves ambiguity over what the quorum-committed batch actually certifies. Define the owner inventory snapshot/high-water capture and participant manifest before append, or introduce a separately committed, batch-bound manifest record. A mismatch or unavailable I sequencer must keep the I local gate closed.

### I-COC-04 — Security envelope is a list of open decisions, not a complete freeze contract (BLOCKING FOR FREEZE)

Canonical serialization, digest/signature algorithms, issuer/audience semantics, key rotation, key revocation propagation, compromise recovery, membership/configuration epoch authentication, and algorithm agility remain open. That is acceptable as a technical proposal but not sufficient for a frozen or deployable protocol. Specify the threat model for compromised owner keys, replay across recovery epochs, leader rollback/term reuse, malicious or stale checkpoint restore, and privileged archive replacement.

### I-COC-05 — Owner-local gate close/reopen proof needs explicit anti-rollback binding (BLOCKING)

Require each owner gate durable attestation to bind owner authority, stable request ID/digest, owner cursor/high-water, local gate generation, recovery epoch and exact batch digest. Reopen must be owner-signed, idempotent, monotonic and conditional on complete reconciliation. COC cannot issue an I gate release. A restored older owner snapshot must not reopen an already closed gate; require an independently retained monotonic anchor or equivalent authoritative owner recovery proof.

## 3. Required security invariants

1. No quorum commit proof, no protected append/favorable read.
2. No current I authoritative sequencer read, no I terminal inference.
3. A pending I cutoff closes receipt issuance and consumption before pending acknowledgement.
4. COC batch membership is not I revocation victory or PermissionEpoch advancement.
5. I gate release is emitted only by I and is bound to the exact recovery epoch, batch digest, complete I request set and monotonic I high-water.
6. Same message/request identity + same canonical digest is idempotent; changed digest is conflict and security-event evidence.
7. No wall-clock or cross-authority cursor comparison.
8. No restore/rollback/compaction path may erase unresolved participant or owner-gate evidence.
9. No operator override, lease expiry or timeout may resolve UNKNOWN/IN_DOUBT.
10. Multi-PolicyDomain JF-10 remains BLOCKED absent a separate I-approved atomic profile.

## 4. Threat/control review

| Threat | Proposal coverage | Required strengthening |
|---|---|---|
| Minority partition / stale leader | Good fail-closed baseline | Bind leader term + committed config epoch to every commit/read proof |
| Lost append ACK / replay | Stable key + digest | Specify authoritative linearizable same-key lookup and replay retention |
| Owner-key compromise/revocation | Open decision | Define key status at signing and verification time, revocation propagation and compromised historical evidence policy |
| Snapshot rollback / stale restore | RESTORE_FENCED | Define independent monotonic high-water/checkpoint anchor and anti-rollback source |
| Malicious operator / force clear | Two-person recovery; no override | Enumerate roles, dual-control actions, immutable audit, separation of duties |
| Incomplete owner inventory | Owner high-water | Signed completeness attestation and post-snapshot request handling |
| Digest collision / canonicalization mismatch | Digest field | Freeze canonicalization and algorithm agility/version domain separation |

## 5. Owner-local Gate decision

I accepts the principle that I durably suspends affected receipt issuance/consumption during COC outage and reopens only after its complete recovery batch and all affected pre-batch participants are reconciled against I's authoritative sequencer/high-water. Gate release clears only the outage gate; it does not issue authorization or itself advance PermissionEpoch.

The exact owner-local gate proof and anti-rollback semantics remain insufficiently specified in this version.

## 6. JF-10 same-XID bridge decision

I accepts same-XID forward/rollback recovery as the correct Storage recovery direction after a durable I decision, with COC later recording owner-signed evidence idempotently. I rejects any reading in which COC decides XID outcome, a standalone I COMMIT token authorizes a detached Storage commit, or a COC record is treated as visibility. This proposal needs a new exact I decision before claiming the bridge is accepted.

**Disposition:** COC as CGH evidence/order service — acceptable in principle with the above conditions. This exact Storage proposal — **NEEDS_REVISION**. No external governance approval, production policy activation, implementation or conformance pass is claimed.
