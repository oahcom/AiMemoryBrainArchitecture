# B — Exact Type Review of Storage COC Protocol v3 / Prepared Participant Contract

- Owner boundary: B — Domain Model
- Branch: `session-b-domain-model-phase3`
- Review target: Storage v3 commit `db226387b0f2dede30a32a19a1478136b368cc1e`, Blob `4a60420d457f359780c568dce42b8bef000026ca`
- Related Storage source: `phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- B registry before this change: Blob `63ccb4bf687b00dea2b21fc2773f3018648d76e6`
- H schema 1.1.1 candidate reviewed: Blob `c0bbfc7611a8d88a39cee209831db32b62601fde`
- A closure authority: `phase-3.6-final-closure-plan.md`, Blob `0adca0f54ff6ee1e344949cb48334ff475fad247`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — B SEMANTIC TYPE BOUNDARY ONLY**

## 1. Scope and evidence boundary

B reviewed Storage v3 §§15.1–15.7 and the companion §14 mapping against the current B typed-reference registry. This is a domain-type decision only. It does not accept Storage implementation, I security policy, H wire encoding, COC deployment or D/E runtime behavior.

## 2. Adversarial findings

### B-V3-01 — Missing B registrations

The pre-review B registry defined PreparedParticipantRef, PreparedTransactionGID and EngineNativeTransactionXIDRef, but did not define DatabaseIncarnationRef, PrepareAttemptRef, PrepareAttemptGeneration, ParticipantLedgerRef, ParticipantLedgerVersion or the complete ParticipantTupleDigest semantics required by Storage v3. These are not optional metadata: they participate in authoritative lookup, attempt replay and proof binding. The registry is amended in §13 of the current B source.

### B-V3-02 — Native XID nominal type ambiguity

Storage v3 uses PostgreSQLNativeXID as an engine-assigned unsigned numeric value. The existing B registry uses EngineNativeTransactionXIDRef, an engine-neutral opaque reference. They are not silently identical. B now defines PostgreSQLNativeXID as the PostgreSQL-specific native value and retains EngineNativeTransactionXIDRef for engine-neutral references/other adapters. H must carry an explicit engine-specific type discriminator and preserve the distinction.

### B-V3-03 — PostgreSQL metadata spelling drift

Storage v3 uses PostgreSQLSystemIdentifier, PostgreSQLDatabaseOID, PostgreSQLTimeline and PostgreSQLLSN; older B vocabulary used PostgresSystemIdentifier, DatabaseOID, Timeline and LSN. B records the full PostgreSQL-prefixed spellings as canonical for this adapter and the older names as compatibility vocabulary only. No numeric coercion or cross-authority ordering follows from the naming alignment.

### B-V3-04 — I terminal proof must bind the complete Storage attempt

Storage v3 §15.7 lists the core I terminal proof tuple but does not explicitly enumerate PrepareAttemptRef/generation and ParticipantLedgerRef/version. Those fields are required to prevent a valid receipt from one prepare attempt being replayed against another attempt or a newer ledger state. I must bind the exact Storage PreparedParticipantReceipt digest and complete participant tuple digest in its atomic receipt-consumption record. B records this as a cross-owner dependency, not an I decision.

### B-V3-05 — Authority boundaries preserved

DatabaseIncarnationRef issuance and participant-ledger truth remain Storage-owned. I authorization/PermissionEpoch and receipt consumption remain I-owned. COC positions remain COC-owned. H encoding remains H-owned. B does not infer that a typed reference is authentic or authorized merely because it is well-formed.

## 3. Required normative mapping

The B registry §13 now defines the added nominal types and the complete lookup key. H must encode those exact semantic distinctions. I must bind the same participant/attempt/ledger tuple in its terminal proof. Storage must implement the incarnation registry and append-only attempt ledger. No cross-owner position comparison or fallback to GID-only lookup is accepted.

## 4. Test and implementation status

- B semantic review: completed as a candidate type decision.
- B runtime type validator: **NOT RUN**; no B executable domain-model harness was identified.
- H schema/validator: the pre-review 1.1.1 schema does not contain DatabaseIncarnationRef, PrepareAttemptRef, PrepareAttemptGeneration or ParticipantLedgerRef/Version; H work is required.
- Storage implementation: not evidenced by this architecture repository's owner artifacts; no implementation PASS inferred.
- Fact/Claim ADR-001: **ADR-BLOCKED**, unchanged.

## 5. A G0–G10 reconciliation

This artifact supports G4 only at B's domain semantic boundary. It is not C/D/E/F/G/Storage consumer acceptance and does not close G6. It is not external governance approval (G5), I36/H36 execution (G7), CFG freeze (G8), runtime/security execution (G9) or overall readiness (G10). A remains the final acceptance authority.

## 6. Provenance

This is a B-role review and domain-model amendment prepared by the delegated B/I/H joint developer session at the user's direction. It is not an independently authenticated human signature or evidence that a separate B session executed tests.


## 7. Addendum — companion §14 is not yet reconciled with v3

The live companion protocol §14 Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` was re-read. It omits DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version and the v3 ParticipantTupleDigest as separate required fields. Storage v3 §§15.1–15.7 Blob `4a60420d457f359780c568dce42b8bef000026ca` requires them. This is a cross-document contract gap, not a cosmetic naming issue.

**B-V3-06:** Storage must amend §14 to the v3 tuple or explicitly supersede §14 for this profile. The B registry §13.5 now records the required action. Until Storage publishes one consistent normative tuple, B's v3 type semantics are accepted only as a candidate mapping; no cross-owner contract freeze is claimed.


## 8. 2026-11-18 exact-source supersession — current Storage tuple is aligned

The historical B-V3-04 and B-V3-06 findings were based on Storage v3 Blob `4a60420d457f359780c568dce42b8bef000026ca` and companion §14 Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`. Those are not the current Storage branch source pair.

Current exact readback:
- Storage v3.2.3 normative body Blob: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- Current companion §14 Blob: `dbc1dfd4c488c5d5e5a328388487d190984e8adc`.
- Storage v3.3.2 candidate manifest Blob: `5c614375e10698e4931d83deb57d20321445e068`.

The current companion §14.1–14.4 contains the full DB-incarnation / prepare-attempt / participant-ledger / tuple-digest binding, authoritative PREPARED observation, receipt required fields and replay/recovery rules. Current v3.2.3 §15.7 binds the same attempt/ledger/receipt/tuple fields into I's terminal proof. Accordingly:

- **B-V3-04: RESOLVED at current document-alignment level.** The current v3.2.3 I proof tuple includes PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, PreparedParticipantReceiptRef/digest and ParticipantTupleDigest.
- **B-V3-06: RESOLVED at current document-alignment level.** Current companion §14 carries the same complete tuple as the v3 design body; the older §14 Blob is historical.
- B-V3-01..03 type distinctions remain as previously accepted; B-V3-05 owner boundaries remain unchanged.

The v3.3.2 manifest remains a candidate and explicitly requires a fresh exact A review. It currently pins the v3.2.3 body but does not explicitly list the current companion §14 Blob above. Storage/A must add that exact source pin or publish a successor bundle and obtain affected-Owner exact-version review. This B addendum is not acceptance of the whole v3.3.2 bundle, an implementation result or a contract freeze.

B runtime type validation remains NOT RUN; Fact/Claim ADR-001 remains ADR-BLOCKED. BIH36-JD-01..17 are unchanged.
