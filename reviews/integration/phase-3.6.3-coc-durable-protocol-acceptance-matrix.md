# Phase 3.6.3 — COC Durable Protocol Exact Owner Acceptance Matrix

- Owner: A — Principal Integration Architect
- Exact Storage protocol: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`
- Exact protocol Blob SHA: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC/JF-10 bridge architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Date: 2026-11-17
- Status: **GATE B DESIGN-LEVEL OWNER REVIEW COMPLETE WITH ENUMERATED EXCEPTIONS; NOT IMPLEMENTED**

## 1. Exact owner review evidence

| Owner | Acceptance artifact Blob SHA | Branch HEAD after acceptance | Disposition |
|---|---|---|---|
| B | `e92ad97ac92469ece2bcd0f7ca6f822966f00232` | `a5bf20b57ebb3db849f91c555b658f9a2ee09851` | Accept with typed-reference/namespace constraints |
| C | `8c8a43f99ecd5986f802fb81ddfa5fd942cef0ae` | `d13aa06ba42820a27bba18ecb6eae13dc9071599` | Accept with provider-boundary/idempotency conditions |
| D | `e2a74d138ccebfb4266d19ea0c0c03f58a815bf5` | `7385e6fa45087a73ea314e8790e22903f3a3be7c` | Accept with fence/lineage/barrier conditions |
| E | `b9dd9af8c770a40b44849d02caac306e0a701100` | `9f53263856ace2cb242b623ceffd6203b1f99df7` | Accept with producer identity/retry/publication conditions |
| G | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `e8547303bc464dbfd42d8d402b538e2b32033934` | Accept with Full Applied/current-use conditions |
| H | `5dfc7ae56b2ae7351d6c2c108f7be3249125f6c3` | `9c33237ecc4801a63d62d1c56184f3d48c53f65f` | Accept with wire/authentication/schema-candidate conditions |
| I | `528945f82e3e25258052240a7a4ba43753ae6cf8` | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | Accept with I authority boundary; one PolicyDomain only |
| A | `d20d08581fd8606a1adf0400bf5dcb24004a9611` | `01cb714c37d37197113f5e614809eb6e9de68df5` | Accept as integrated architecture protocol |
| Storage | `332de9192ccab6f18fc2a0d18700cc9585a98983` | `60033fc324005e3a5a26e3e1bde859378d3db9be` | Accept as Storage architecture specification |

## 2. Gate B design determination

All nine Owner perspectives have recorded exact-Blob review of the same Storage COC durable protocol specification. The protocol includes the required durable log model, quorum/leader and voter-configuration semantics, participant registry/state machine, owner-boundary mapping, outage recovery-cutoff batch, UNKNOWN/IN_DOUBT behavior, snapshot/restore and WAL/PITR requirements, linearizable read APIs, crash/recovery matrix, compaction/retention and engineering handoff.

**Gate B disposition: DESIGN-LEVEL ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS.** The protocol is specified and exact-owner-reviewed. Gate B implementation/conformance is NOT RUN and is not implied.

## 3. Non-waived limits

1. No COC Raft/consensus implementation or quorum service exists; no real voter, leader, network partition or quorum failover test has run.
2. PostgreSQL 18.7 CI tests qualify prepared-XID, WAL/PITR, failover and restore capabilities in isolated fixtures only. They do not prove production COC, I sequencer or D ledger integration.
3. Gate C multi-process and end-to-end fault injection is deferred to the engineering phase after executable services exist.
4. C provider-specific same-key idempotency and ambiguous outcome recovery remain unverified.
5. I sequencer/receipt-consumption implementation, D durable fence/lineage ledger, E compiler ledger and G Applied validator/persistence are not implemented/verified.
6. H schema is a documentation-derived candidate; generated IDL/SDK interoperability, canonical parser, duplicate-key rejection and cryptographic/channel-binding verification remain NOT RUN.
7. Multi-I-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.
8. I36 external governance, ProducerDomainInventoryEpoch/InventorySeal authority, complete target inventory and Global Forget Completion remain OPEN.
9. Fact/Claim ADR-001 remains ADR-BLOCKED; no canonical domain schema or dependent wire schema is frozen.
10. Production COC/Storage deployment, named human operator, KMS, failure-domain placement, numeric RTO and production activation remain engineering/deployment decisions.

## 4. Authority and phase boundary

COC records order and participant observations only. I, D, Storage, C, H, G and B retain their respective authority. The single-I-PolicyDomain profile is the only accepted JF-10 architecture profile; all other cases fail closed.

`IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. This is an architecture-design acceptance, not an implementation, deployment, production readiness or system freeze decision.

**Final:** Gate B design is accepted by all required Owner perspectives with explicit exceptions; Gate C and JF-10 runtime P0 remain open.