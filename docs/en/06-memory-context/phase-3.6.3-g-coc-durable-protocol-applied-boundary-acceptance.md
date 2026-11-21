# G Owner — Exact COC Durable Protocol Applied-Evidence Boundary Acceptance

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- G JF-10 Applied evidence acceptance Blob: `25c1da1f6769165881d217bb0bb492a997e0e14c`
- G Applied/Forget contract Blob: `aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- Decision: **ACCEPT WITH G-OWNED APPLIED / CURRENT-USE CONDITIONS**
- Mode: delegated G-boundary review under user instruction; not independent human sign-off.

G accepts the COC protocol as one required evidence source, not as an Applied authority:
1. Full Applied requires exact CSubmitOutcome, valid H evidence, I terminal authorization, D complete-lineage barrier/clearance, Storage same-XID resolution and a determinate CausalOrderTerminalProof bound to the same immutable tuple.
2. COC log commit, recovery batch, quorum position, I COMMIT_WON, D clearance, Storage prepared receipt, H ACK or reservation alone never satisfies Full Applied.
3. Missing/stale COC prefix, unresolved recovery batch, missing participant, owner high-water mismatch, unknown I/D/Storage outcome or provider UNKNOWN blocks new Full Applied and protected current use.
4. Historical Applied remains immutable only if valid at its original commit; current-use is separately recomputed against current Context head, authorization, fence, scope, environment, session and capability.
5. COC cannot mint owner decisions or compare COC/I/D/Storage positions.

Exceptions: G Applied validator/persistence and integrated COC/JF-10 lookup are not implemented/verified; G-CO race suites remain NOT RUN. This is design acceptance only and does not claim Global Forget completion or physical erasure.