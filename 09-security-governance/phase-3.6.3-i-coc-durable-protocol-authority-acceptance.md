# I Owner — Exact COC Durable Protocol I-Authority Boundary Acceptance

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- I JF-10 v2 disposition Blob: `8069ff86988396442c8d9dc3fd58653683abe2f3`
- I COC/JF-10 composition boundary Blob: `9e1f66ddbe0952f17068b1638feb8ab0094588c3`
- Decision: **ACCEPT WITH I-OWNED AUTHORIZATION / REVOCATION BOUNDARIES — SINGLE POLICY DOMAIN ONLY**
- Mode: delegated I technical-boundary review under user instruction; not external governance approval or independent human signature.

I accepts the protocol only as a COC ordering and participant-accounting contract:
1. I remains sole authority for PolicyDomainRef, CommitAuthorizationReceipt, receipt consumption, PermissionEpoch, revocation ordering and I terminal outcome.
2. COC records I-issued requests and signed terminal observations; it never mints, reverses or infers I decisions.
3. A COC outage requires I to durably suspend affected receipt issuance/consumption as PENDING_COC_CUTOFF. I reopens only after its own request set, pre-batch participants, sequencer outcomes and high-water are reconciled.
4. COC recovery batch does not order I and D local request times. I's sequencer position remains incomparable to COC/D/Storage positions.
5. JF-10 remains limited to one PolicyDomainRef. Multi-policy-domain atomicity remains BLOCKED / NOT ACCEPTED.
6. Missing/invalid InventorySeal or ProducerDomainInventoryEpoch evidence remains UNKNOWN where policy requires it; COC cannot supply I inventory authority.

Exceptions: I sequencer implementation, durable receipt consumption, failover/restore and end-to-end integration are NOT VERIFIED. I36-GOV-01..10 and global inventory/Global Forget governance remain GOVERNANCE-BLOCKED. This technical acceptance does not approve external policy or Global Forget completion.