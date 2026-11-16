# Session I — Governance Decision Register

- Owner: Session I — Security, Identity & Governance Principal Architect
- Status: **Candidate register; no policy decision below is effective until the required approval is recorded**
- Register version: `I-GOV-3.5-candidate.1`
- Governing addendum: `phase-3.5-global-identity-forget-governance.md`

## Decision record rules

Each decision records: stable ID, exact decision text, authority owner, required approver(s), approval state, supporting evidence/artifact and version, effective policy version/date, review/expiry, and supersession link. A document commit is not an approval. I may author a policy proposal but cannot self-approve legal, privacy, cross-tenant security or operational risk reserved to independent authorities.

## Decision register

| ID | Governance decision | Owner | Required approver(s) | Evidence / approval basis | Status | Effective version |
|---|---|---|---|---|---|---|
| I35-DEC-01 | Principal is issuer-authenticated and namespaced by issuer + tenant/security domain; payload IDs are claims only | I | Identity/Security Governance; B + H for typed/transport binding | Principal/ActorRef contract; B typed-reference contract; H envelope identity binding; spoof/issuer-negative tests | Proposed | None |
| I35-DEC-02 | ActorRef and ScopeRef remain B-owned typed references; I defines authorization binding, not their schema | I policy / B type authority | B + Architecture Governance | B domain reference approval and I/H mapping review | Proposed | None |
| I35-DEC-03 | Every protected boundary revalidates current authorization; stale Context/cache/lease/decision cannot authorize | I | D/E/F/G/H/C boundary owners + Security Governance | Scope/revocation matrix; per-boundary conformance and revocation-race tests | Proposed | None |
| I35-DEC-04 | Delegation is bounded, non-amplifying, issuer-verified and transitively invalidated by parent revocation | I | Security Governance; Identity/Legal where required | Signed grant model, chain validation, cycle/depth/revocation tests | Proposed | None |
| I35-DEC-05 | PermissionEpoch is I-owned and distinct from D ForgetFenceGeneration, I ProducerDomainInventoryEpoch, F IndexWatermark, G ContextVersion and H AdapterCapabilityEpoch | I | Security Governance + all consuming owners | Typed namespace contract and epoch-mixup negative tests | Proposed | None |
| I35-DEC-06 | I global Producer/Recipient Domain Inventory and D per-Forget WorkItem Barrier are separate mandatory proof layers | I global inventory / D work barrier | D + E + F + G + H + Storage | Inventory seal, D registration receipt/high-water, race/crash/replay tests | Proposed | None |
| I35-DEC-07 | H ACKs map to target/action-bounded evidence; UNKNOWN and UNSUPPORTED are not success | I global mapping / H ACK semantics | H + Security Governance | H ACK contract, target identity/capability/session/scope evidence, replay/expiry tests | Proposed | None |
| I35-DEC-08 | Mandatory Unknown/Failed/missing evidence blocks Completed; exceptions are explicit, narrow, approved and expiring | I | Privacy/Legal + Security + relevant data/service owner | Exception matrix, signed approval, expiry/reopen test | Proposed | None |
| I35-DEC-09 | Backup restore is quarantine-first and replays the current Forget/revocation control ledger before serving | I policy / Storage execution | Storage + Security + Privacy/Legal | Backup inventory, restore drill, stale snapshot fixture and suppression proof | Proposed | None |
| I35-DEC-10 | External recipient receipt is not deletion proof; onward copies and provider-internal uncertainty remain Unknown or exception | I | Privacy/Legal + Data Owner + Security | Contract/API semantics, recipient deletion attestation, onward-recipient inventory | Proposed | None |
| I35-DEC-11 | Physical erasure is distinct from suppression and cleanup; only scope-bound media/key evidence supports an erasure claim | I | Storage + Privacy/Legal + Security | Media/key inventory, crypto-erasure proof, retention/jurisdiction policy | Proposed | None |
| I35-DEC-12 | Audit/tombstone evidence is non-reconstructive and retained only under approved jurisdictional schedule | I | Privacy/Legal + Audit Owner | Data map, retention basis, reconstruction test | Proposed | None |

## Approval and effective-version ledger

No signed approvals or effective-version changes were supplied by this Phase 3.5 document review. Therefore all records above remain **Proposed**, and `I-GOV-3.5-candidate.1` is a document baseline only, not an approved production policy version.

When a decision is approved, append (do not overwrite) an approval entry containing:
- decision ID and exact approved text/hash;
- approver PrincipalRef, Issuer and approval authority;
- independent reviewer PrincipalRef where required;
- evidence artifact IDs/versions and test result references;
- effective policy version and effective timestamp;
- scope/jurisdiction/data classes covered;
- expiry/review date and revocation/supersession conditions.

## OPEN policy decisions

The detailed unresolved decision list is maintained in `phase-3.5-global-identity-forget-governance.md` §6. No OPEN item is implicitly resolved by this register.
