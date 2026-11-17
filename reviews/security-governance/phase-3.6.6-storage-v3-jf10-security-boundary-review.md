# I — Exact Security Boundary Review of Storage COC Protocol v3

- Owner boundary: I — Security & Governance
- Branch: session-i-security-governance-2026-11-16
- Exact Storage v3 target: commit db226387b0f2dede30a32a19a1478136b368cc1e, Blob 4a60420d457f359780c568dce42b8bef000026ca
- Companion Storage prepared-participant source: Blob 86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7
- I authorization contract reviewed: 09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md, Blob 5a5304d48aa912dcf6f817099bd5659371d8cdc8
- I JF-10 disposition: 09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md, Blob 8069ff86988396442c8d9dc3fd58653683abe2f3
- I prepared-participant acceptance: Blob 20fc13bbfe7b93c0d6f6233fd714c57dadca1fda
- H schema 1.1.1 candidate reviewed: Blob c0bbfc7611a8d88a39cee209831db32b62601fde
- A final closure plan: Blob 0adca0f54ff6ee1e344949cb48334ff475fad247
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — I AUTHORIZATION / SECURITY SEMANTICS ONLY; CRYPTOGRAPHIC PROFILE NOT FROZEN**

## 1. Authority boundary

I retains exclusive authority for:
- issuer/key trust and the authorization status of a signing principal;
- PolicyDomainRef, PermissionEpoch and revocation ordering;
- CommitAuthorizationReceipt issuance and single-use consumption;
- I sequencer terminality and I owner-gate close/release;
- I-owned key-status history and I anti-rollback evidence.

COC may persist and order I-issued evidence. COC position, batch membership, leader state or quorum ACK is never I authorization, I terminality, PermissionEpoch or an I gate-release decision. Storage owns the prepared participant, GID/native-XID/DB-incarnation facts and visibility resolution. H transports and validates the evidence but cannot create I authority.

## 2. Adversarial findings against exact v3

### I-V3-01 — Owner-local I gate lacks an explicit serialization point

Storage v3 §§5.2 and 6.1 correctly require atomic owner snapshot/gate closure and owner-only release, but do not define the I sequencer transaction/CAS that serializes:
- accepting an IRevocationRequestRef;
- closing receipt issuance and receipt consumption;
- incrementing the I gate generation;
- capturing the complete I request high-water and request-set digest;
- racing receipt issue/consume operations.

**Required I rule:** the authoritative PolicyDomain sequencer must provide one serializable transaction for CloseIRecoveryGate. That transaction must durably append the idempotent request (stable IRevocationRequestRef + RequestDigest), set the affected gate to PENDING_COC_CUTOFF, increment GateGeneration, and capture the I request high-water/request-set count/digest before acknowledging the request. Every receipt issuance and consumption transaction must serialize through the same sequencer and check the gate state/generation inside its transaction. No separate cache or local wall-clock check is sufficient.

The scope key must bind PolicyDomainRef plus the exact revocation scope digest (principal/actor/resource/action, ScopeRef and EnvironmentRef selectors as applicable). A scope expansion is a new immutable request and gate generation; it cannot silently widen an already sealed snapshot.

### I-V3-02 — In-flight receipt/participant classification must be explicit

The I snapshot must distinguish:
1. **Receipt issued, not consumed:** no COMMIT_WON exists. Once the close transaction wins, consumption is suspended; the receipt is retained as unresolved evidence and cannot be used after the gate closes.
2. **Receipt consumption ordered before close and terminalized COMMIT_WON:** the terminal decision is immutable. The exact participant is included in the pre-batch reconciliation set; a later revocation remains pending behind that participant until the applicable C/D/Storage outcome is authoritatively terminal.
3. **Receipt consumption ordered after close:** deny/suspend it; do not issue a favorable terminal proof.
4. **Concurrent or uncertain transaction outcome:** return UNKNOWN/IN_DOUBT and keep the I gate closed.

Any I-admitted operation not yet COC-registered must remain discoverable from the I sequencer's durable admission/receipt ledger and be included in reconciliation or rejected before any downstream side effect. It must not disappear between the I snapshot and COC participant enumeration.

### I-V3-03 — Recovery Cutoff Batch and gate release need a second high-water check

I release must be an I-signed, idempotent compare-and-set against the exact:
- IRevocationRequestRef set and digest, including explicit empty-set proof;
- PolicyDomainRef, owner high-water, GateGeneration and independent anti-rollback anchor;
- RecoveryEpoch, committed Recovery Cutoff Batch position/digest and Participant Manifest digest;
- complete applicable pre-batch participant reconciliation root;
- proof that no request after the captured high-water was admitted through the closed gate.

If a new in-scope request or scope generation appears during reconciliation, I does not release the old gate. It remains closed and requires a subsequent immutable batch/manifest round. COC's RECOVERY_EPOCH_COMPLETED is not an I release. Clearing the temporary outage gate does not advance PermissionEpoch or declare revocation effective; the normal I revocation terminalization remains a separate I sequencer decision.

### I-V3-04 — I terminal proof tuple is missing attempt and ledger bindings

Storage v3 §15.7 binds the participant, GID, DB authority/incarnation, operation/request digest, owner boundary, PolicyDomainRef, PermissionEpoch, I position and terminal outcome. It does not explicitly require the immutable PrepareAttemptRef/PrepareAttemptGeneration and ParticipantLedgerRef/ParticipantLedgerVersion that §15.3 requires in the Storage participant tuple.

I's atomic receipt-consumption record MUST additionally bind:
- PreparedParticipantReceiptRef and its exact signed payload digest;
- PreparedParticipantRef and PreparedTransactionGID;
- CanonicalAuthorityDBRef and DatabaseIncarnationRef;
- PrepareAttemptRef and PrepareAttemptGeneration;
- ParticipantLedgerRef and ParticipantLedgerVersion;
- PublicationOperationId, RequestDigest and ParticipantTupleDigest;
- COC prepare-intent identity/position/digest;
- exact Storage owner-final-gate participant and owner boundary;
- PolicyDomainRef, PermissionEpoch, CommitAuthorizationReceiptRef/digest and one-time ReceiptConsumptionRef;
- I sequencer identity/epoch/position and terminal outcome.

I verifies the Storage receipt as Storage-owned evidence and binds its digest; I does not interpret or mint PostgreSQL native XID, Storage outcome or VisibilityPointer. A proof for another attempt, ledger version, DB incarnation or owner-final-gate participant is CONFLICT.

### I-V3-05 — Outcome vocabulary conflict: ABORT_WON is not an accepted I outcome

Storage v3 §7.3 uses ABORT_WON / REVOCATION_WON / INDETERMINATE_ABORTED. The current I terminal contract and H 1.1.1 candidate enumerate COMMIT_WON, REVOCATION_WON and INDETERMINATE_ABORTED; they do not define ABORT_WON.

For this review, ABORT_WON is **not accepted**. Storage v3 must use the I-owned vocabulary exactly:
- COMMIT_WON: I terminal success for the exact bound participant; Storage may forward-resolve the same participant after verifying the proof.
- REVOCATION_WON: I terminal revocation outcome; Storage rolls back the same participant.
- INDETERMINATE_ABORTED: I has durably selected the abort terminal for the exact participant; Storage rolls back that same participant.
- UNKNOWN / IN_DOUBT: nonterminal; no commit, rollback inference, gate release or new XID.

INDETERMINATE_ABORTED is a terminal I decision, not a synonym for UNKNOWN. Storage resolution outcome remains a separate enum (COMMITTED, ROLLED_BACK, UNKNOWN). The I enum and Storage enum MUST NOT be merged.

### I-V3-06 — Anti-rollback anchor authority and recovery proof need explicit I semantics

Storage v3 §8 calls for independent monotonic anchors but leaves the I anchor's authority and verification protocol to I. I requires an anchor independent of the restored Storage database and the COC snapshot, binding at least:
- PolicyDomainRef and current PermissionEpoch;
- I sequencer identity/epoch/committed position;
- receipt-consumption high-water and exact consumed-receipt set/root;
- owner gate generation and request high-water;
- issuer/key-status registry generation and trust-root version;
- checkpoint digest, previous checkpoint and trusted time/append-only evidence.

A restore must compare the recovered I state against the independent current anchor before issuing or consuming receipts or reopening the gate. A missing, stale, rolled-back, gapped or contradictory anchor/key-status proof is UNKNOWN and keeps the gate closed. A local DB sequence, COC position or timestamp is not an independent anchor.

### I-V3-07 — Signed envelope is a candidate; exact policy and historical verification are not frozen

Storage v3 §16.1–16.4 correctly delegates security policy to I and wire/canonicalization to H. I's required envelope trust semantics are:
- issuer principal and issuer trust-root identity;
- subject PreparedParticipantRef;
- owner authority and signer authority;
- audience, target EnvironmentRef, purpose/message type and schema version;
- key ID/version, algorithm-profile ID, canonicalization-profile ID and digest-profile ID;
- trusted signing-time evidence and key-status evidence;
- payload digest over the complete canonical payload;
- signature over a domain-separated construction covering the protected header and complete canonical payload bytes.

I proposes the following **candidate** domain separation for joint I/H review (not frozen or activated):

`SignatureInput = UTF8("AIMB\u0000StoragePreparedParticipant\u0000v1") || 0x00 || U64BE(header_length) || canonical_header || U64BE(payload_length) || canonical_payload`

The canonical header and payload byte rules, Unicode behavior, duplicate-key rejection, numeric/string representation and digest profile must be specified by H and jointly accepted by I. The signature algorithm suite and key custody provider remain I/Security Governance decisions; this review selects neither.

Historical verification MUST distinguish mathematical signature validity from whether the key was authorized for this issuer/purpose at signing time and whether a later revocation or compromise is effective. Later revocation does not silently rewrite history; a compromise effective before signing may invalidate the proof. Missing public-key, trust-root, trusted-time or key-status history yields UNKNOWN, not implicit validity.

### I-V3-08 — Governance approval is separate and remains blocked

This technical review does not approve I36-GOV-01..10, issuer federation, delegation, cross-Scope or cross-Environment grants, offline authorization leases, break-glass, Global Forget exceptions, Environment Registry Authority or InventorySeal. The I governance register remains authoritative; all ten external governance decisions remain **GOVERNANCE-BLOCKED / NOT APPROVED** until the authorized bodies create effective approval records. No named external approver or signed approval is invented here.

## 3. Normative I replacement clauses for Storage v3

### 3.1 Close gate and capture high-water atomically

CloseIRecoveryGate(IRevocationRequestRef, RequestDigest, PolicyDomainRef, ScopeDigest) MUST execute in the authoritative I PolicyDomain sequencer as one serializable transaction:

1. Verify the request issuer and exact immutable request tuple.
2. If the same request ref + digest already exists, return the original gate record idempotently. Same ref with a different digest is CONFLICT.
3. Append the request; set the affected gate to PENDING_COC_CUTOFF; increment GateGeneration; atomically capture the request-set high-water, count and digest.
4. Make both receipt issuance and receipt consumption fail closed for the affected scope before the transaction commits.
5. Return the signed pending attestation only after durable commit.

Receipt issue/consume operations serialize against this transaction. If they commit first, their exact operation/participant records are in the in-flight reconciliation set. If gate close commits first, the issue/consume operation is denied. No admitted operation may exist outside both records.

### 3.2 Release gate only against exact recovered state

ReleaseIRecoveryGate MUST be an I-owned monotonic CAS requiring the exact committed batch and manifest, request-set digest/count, owner high-water, GateGeneration, anti-rollback anchor and complete applicable participant reconciliation root. A new request, high-water advance, scope expansion or participant omission keeps the gate closed and requires another batch/manifest round. Release clears only the outage gate; it does not change PermissionEpoch or declare revocation victory.

### 3.3 Atomic I terminal receipt-consumption proof

One I PolicyDomain sequencer transaction MUST validate current issuer/key status and PermissionEpoch, consume the exact CommitAuthorizationReceipt once, bind the complete Storage participant/attempt/ledger tuple and exact owner-final-gate participant, and persist the terminal outcome plus proof. A detached token, COC projection or Storage receipt is not I terminality. The proof's digest must cover the exact signed Storage PreparedParticipantReceipt digest and the immutable participant tuple digest.

### 3.4 I outcome and Storage resolution mapping

| I terminal outcome | Storage action | Provider action |
|---|---|---|
| COMMIT_WON | Resolve same participant/GID in same DB incarnation forward, after exact proof validation | C may invoke only after all required D predicates and COC registrations |
| REVOCATION_WON | Roll back same participant/GID; prove non-publication | MUST NOT invoke |
| INDETERMINATE_ABORTED | Roll back same participant/GID; prove non-publication | MUST NOT invoke |
| UNKNOWN / IN_DOUBT / PENDING | Retain prepared participant, locks and private bytes; no terminal inference | MUST NOT invoke |

No ABORT_WON value is introduced by this review.

## 4. Additional I-owned conformance cases

The following supplementary cases are specified, **NOT RUN**:
- I-COC-V3-01: receipt issuance racing gate close in both sequencer orders;
- I-COC-V3-02: receipt consumption racing gate close in both sequencer orders;
- I-COC-V3-03: admitted-but-not-COC-registered participant remains enumerable;
- I-COC-V3-04: post-high-water request forces a subsequent batch;
- I-COC-V3-05: same request ID/digest idempotent; changed digest conflict;
- I-COC-V3-06: scope expansion increments gate generation and cannot reopen a narrower gate;
- I-COC-V3-07: terminal proof replay against another attempt/ledger version is rejected;
- I-COC-V3-08: ABORT_WON is rejected; only I-owned terminal outcomes accepted;
- I-COC-V3-09: restored receipt-consumption/key-status snapshot behind the independent anchor remains fenced;
- I-COC-V3-10: missing historical key-status evidence yields UNKNOWN.

No I service implementation, independent anchor service, signed fixtures, executable I36/JF-10 integration harness or test-run evidence was supplied for these cases. They are not PASS.

## 5. A G0–G10 and Phase 3.6 disposition

- G4: I technical review of Storage v3 is **ACCEPT WITH ENUMERATED AMENDMENTS**, limited to I authority and authorization semantics.
- G5: **BLOCKED** — I36-GOV-01..10 have no effective external approvals.
- G6: **BLOCKED/PARTIAL** — this is not C/D/E/F/G/Storage consumer acceptance.
- G7: **NOT RUN** — I36/H36 and the supplementary I-COC-V3 cases have no execution evidence.
- G2/G3/G8/G9/G10: unchanged from A's plan; this artifact does not close them.
- JF-10 P0: OPEN; single PolicyDomain only; multi-PolicyDomain atomicity remains BLOCKED.
- Global Forget completion and physical erasure: not claimed.

## 6. Provenance

This is an I-role technical review and candidate policy addendum prepared by the delegated B/I/H joint developer session at the user's direction. It is not an independently authenticated human signature or external Security/Identity/Privacy/Legal approval. No cryptographic algorithm, production key custody system or effective governance policy is approved by this artifact.
