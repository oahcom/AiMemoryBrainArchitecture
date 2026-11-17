# Phase 3.6.10 — H Recovery Cutoff Semantic Validator Contract

- Owner perspective: H — BMCP Protocol Architect
- Status: **PROPOSED VALIDATION CONTRACT — EXACT-VERSION H / I / D / C / STORAGE / A REVIEW REQUIRED**
- Scope: A §11 Recovery Cutoff Batch, owner snapshots/admission sets, COC ParticipantManifest, owner-only release and A §12 JF-10 bridge joins
- This is a specification of validators and vectors, not an implementation or conformance result.

## 0. Exact source bundle

| Source | Blob |
|---|---|
| A Phase 3.6 architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H recovery schema 1.0.4 | `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |

Schema 1.0.4 is the current structural candidate at the time of this document. The semantic rules below are additional requirements and are not implied by JSON Schema validity.

## 1. Validator architecture

Implement five independently testable validators and one composition validator:

1. `validateOwnerSnapshot`
2. `validateParticipantManifest`
3. `validateRecoveryCutoffBatch`
4. `validateOwnerGateRelease`
5. `validateRecoveryEpochCompleted`
6. `validateRecoveryJoin` — composes the first five and the JF-10 bridge validators.

Each validator returns one of `VALID`, `INVALID`, or `UNKNOWN`. Missing authoritative source, incomplete pagination, stale read, unavailable owner, unverifiable signature or unresolved anti-rollback state returns UNKNOWN and MUST NOT be coerced to VALID or EMPTY.

## 2. Owner snapshot validation

For each I/D/C owner snapshot:

1. Validate schema ID/version, strict field set, issuer/subject/owner authority, audience, purpose, signer/key status and signature under I-approved trust policy.
2. Resolve the exact owner ledger source and completeness method; reject a stale replica or partial cursor.
3. Verify GateRef, GateGeneration, scope binding, scope generation, snapshot generation and anti-rollback anchor are current and monotonic.
4. Independently validate request and admission ledgers:
   - request member entries have `owner_entry_kind=REQUEST`;
   - admission member entries MUST NOT have REQUEST kind;
   - request/admission high-waters are from the exact owner ledger namespace;
   - I requires receipt_issue, receipt_consume and producer_domain_inventory_epoch high-waters;
   - D requires producer_registration, work_item, attempt and barrier high-waters;
   - C requires reservation and provider_attempt high-waters.
5. Require exact array count equality and canonical ordering by the owner's declared immutable sequence/ref ordering. Duplicate owner_entry_ref is INVALID.
6. Recompute each member digest and each member-set root using the exact H canonicalization/digest profile; compare to declared values.
7. COMPLETE_EMPTY is VALID only when the array is present and empty, count is zero, root equals the canonical empty-set root, ledger query is complete, and owner attestation signs that exact state.
8. COMPLETE_NON_EMPTY requires non-empty array, exact count and root. NOT_ENUMERATED/PARTIAL/UNAVAILABLE/UNKNOWN never qualifies as empty.
9. Validate all owner-specific high-waters and ensure no member exceeds its captured high-water. If the owner ledger advances before release, snapshot becomes STALE and a later recovery round is required.

## 3. COC ParticipantManifest validation

1. Obtain the exact quorum-confirmed prefix position (term/index) and root using a linearizable COC read.
2. Enumerate every ParticipantIntent in the affected causal-order domain through that exact prefix; pagination must be complete and cursor continuity verified.
3. Validate each typed participant entry: unique ParticipantIntentRef, owner kind, mandatory owner_admission_ref, operation identity, participant digest, term/index and entry digest. Resolve owner_admission_ref against the exact signed C admission ledger; Storage participants additionally join the exact JF-10 PreparedParticipant tuple.
4. Verify every entry is actually present in the committed prefix at its declared term/index and the digest matches the committed record.
5. Recompute participant count and canonical participant-set root.
6. COMPLETE_EMPTY requires a complete prefix enumeration and canonical empty root. A missing log segment, unavailable quorum, incomplete page or stale follower is UNKNOWN, not empty.
7. Reject duplicate participant refs, duplicate positions, conflicting operation identities or one identity bound to different digests.
8. The manifest is immutable and bound to RecoveryEpoch, prefix root and previous-prefix digest. A later prefix is a new manifest/round, never an in-place mutation.

## 4. RecoveryCutoffBatch validation

1. Validate quorum proof and ensure the batch is appended after the exact prefix it closes.
2. Require exactly one I, one D and one C snapshot reference and digest for this Phase 3.6.9 recovery scope. Missing owner is not empty.
3. Fetch each snapshot by exact immutable ref and verify its digest, signature and scope binding.
4. Fetch the ParticipantManifest by exact ref and verify its digest, prefix term/index/root and complete enumeration.
5. Verify RecoveryEpoch, recovery round, previous batch digest and reconciliation attempt generation form an append-only chain with no gaps or forks.
6. Ensure the batch's scope binding equals the exact owner scope bindings and causal-order domain scope; partial or widened scope is UNKNOWN/INVALID.
7. Reject any batch that attempts to sort or compare I/D/C local sequence numbers against one another or against COC term/index.
8. Recompute batch digest over the canonical protected payload and verify the quorum commit proof.

## 5. Cross-set RecoveryJoin validation

The join is a typed relation, not a global sequence.

For each owner admission member:
- If `REGISTERED`, its exact ParticipantIntentRef, COC position and entry digest MUST match one unique participant manifest entry. The owner operation identity/digest and scope must match the participant payload.
- If `NOT_REGISTERED`, the member MUST carry no ParticipantIntentRef/position/digest. It remains an owner-local obligation and must be registered under the same stable identity before any later protected effect, or terminalized by authoritative no-effect evidence.
- Multiple owner evidence entries may legitimately refer to one participant (for example issue/consume evidence), but the same owner entry cannot map to multiple participants unless an explicit typed cardinality contract allows it.
- Every affected participant in the COC manifest must have an accountable owner binding (mandatory C owner_admission_ref, plus I receipt/terminal evidence, D barrier membership and Storage participant where applicable). A participant with no accountable owner evidence is UNKNOWN and blocks release.
- A Storage participant is joined through the exact JF-10 participant tuple; it is not treated as a separate user request merely because it has a Storage owner kind.

The join proof records exact member refs/digests and participant refs/digests. It does not synthesize a cross-owner high-water or fabricate missing entries.

## 6. JF-10 cross-schema join (A §12)

The recovery-cutoff messages supplement `bmcp.applied-ack/1.1.0`; they do not replace its five JF-10 bridge message families.

For every applicable Storage participant, the cross-schema validator MUST compare the same immutable tuple across the RecoveryJoin, JF-10 bridge, I proof and Storage receipt/resolution:
- ParticipantIntentRef / CausalOrderTransactionRef;
- PublicationOperationId / RequestDigest / ParticipantTupleDigest;
- PreparedParticipantRef / PreparedTransactionGID;
- CanonicalAuthorityDBRef / DatabaseIncarnationRef / PostgreSQLNativeXID where known;
- PrepareAttemptRef / PrepareAttemptGeneration;
- ParticipantLedgerRef / ParticipantLedgerVersion;
- COC prepare-intent position/digest;
- I receipt ref, single-use consumption identity and terminal proof;
- Storage PreparedParticipantReceipt and StorageResolutionProof.

Terminal mapping is mandatory:
- I COMMIT_WON → same participant and same XID Storage COMMITTED; provider invocation additionally requires D clearance and C's final gate.
- I REVOCATION_WON or INDETERMINATE_ABORTED → same participant and same XID Storage ROLLED_BACK; provider invocation is forbidden.
- I UNKNOWN/IN_DOUBT or Storage UNKNOWN/IN_DOUBT → unresolved; no release.
- Contradictory I/Storage terminal pair → INVALID and quarantine; never resolve by COC observation or timeout.

## 7. Owner Gate Release validation

1. Validate owner signature and authority; I/D/C may issue only their own gate release.
2. Compare release GateRef/Generation, scope/scope generation, request high-water/root, admission high-water/root, snapshot generation/digest and anti-rollback anchor against the latest authoritative owner ledger.
3. Perform the final compare-and-commit at the owner authority. A precomputed release message without successful currentness CAS is not a release.
4. Verify exact RecoveryEpoch/round/RecoveryCutoffBatch/ParticipantManifest and all owner obligations are terminal or explicitly safe no-effect.
5. Any post-high-water request, inventory epoch advance, D projection/lineage advance, C provider-attempt advance, changed root or stale key status invalidates the candidate and requires a subsequent round.
6. A release is typed OUTAGE_ADMISSION_RELEASE_ONLY. It does not clear effective ForgetFence, prove Global Forget Completion, resolve Storage visibility or manufacture provider success.

## 8. RecoveryEpochCompleted validation

COC may record RECOVERY_EPOCH_COMPLETED only after:
- every required immutable cutoff round is present and chained;
- each round's batch, prefix and participant manifest validates;
- all affected participants are reconciled;
- exactly one valid current I release, one D release and one C release are present for the applicable scope/generation;
- no UNKNOWN/IN_DOUBT, missing owner, missing prefix page or stale high-water remains.

The completion record is a COC observation, not an owner gate release or a substitute for I/D/C authority.

## 9. Required positive and negative vectors

| ID | Scenario | Expected |
|---|---|---|
| HRC-01 | I/D/C request and admission sets all complete-empty with valid signed canonical empty roots | VALID |
| HRC-02 | Request set empty, admission set non-empty, independent roots correct | VALID |
| HRC-03 | COMPLETE_EMPTY with null/missing array or non-empty array | INVALID |
| HRC-04 | Zero count but ledger unavailable/partial pagination | UNKNOWN / INVALID |
| HRC-05 | Count differs from array length | INVALID |
| HRC-06 | Duplicate owner_entry_ref or noncanonical member order | INVALID |
| HRC-07 | I snapshot omits receipt_consume or inventory epoch high-water | INVALID |
| HRC-08 | D snapshot omits work/attempt/barrier high-water | INVALID |
| HRC-09 | C snapshot omits provider_attempt high-water | INVALID |
| HRC-10 | COC participant prefix has missing page/segment or stale follower read | UNKNOWN |
| HRC-11 | ParticipantManifest omits one committed pre-batch ParticipantIntent | INVALID |
| HRC-12 | REGISTERED owner member points to wrong participant digest/position | INVALID |
| HRC-13 | NOT_REGISTERED member carries a fabricated ParticipantIntentRef | INVALID |
| HRC-14 | Affected participant has no accountable owner admission/barrier/receipt evidence | UNKNOWN |
| HRC-15 | Batch omits I, D or C snapshot | INVALID |
| HRC-16 | Batch references stale snapshot digest or wrong prefix root | INVALID |
| HRC-17 | High-water/scope generation advances before owner release CAS | STALE; next round required |
| HRC-18 | COC attempts to issue an I/D/C release | INVALID |
| HRC-19 | RecoveryEpochCompleted has fewer than one valid I, D and C release | INVALID |
| HRC-20 | I COMMIT_WON paired with Storage ROLLED_BACK | INVALID |
| HRC-21 | I REVOCATION_WON paired with Storage COMMITTED | INVALID |
| HRC-22 | I or Storage UNKNOWN/IN_DOUBT | UNKNOWN; release blocked |
| HRC-23 | Same message identity/same digest replay | VALID idempotent replay |
| HRC-24 | Same message identity/changed digest | CONFLICT / INVALID |
| HRC-25 | Unknown critical field, downgrade, duplicate JSON key or absent/null substitution | INVALID |

## 10. Status and owner acceptance boundary

This contract specifies H's semantic validation obligations. It does not implement the validators or establish canonical-byte/signature interoperability. H exact-version acceptance, I trust-policy approval, C/D/Storage owner review, A integration acceptance and executable tests remain required.

No protocol/schema/cryptographic freeze, runtime conformance, deployment, production activation or JF-10 P0 closure is claimed.


## 11. Executable candidate suite and RecoveryJoin wire candidate

The following implementation artifacts have been added on the H branch:

| Artifact | Path | Current Blob | Purpose |
|---|---|---|---|
| HRC semantic suite | `08-bmcp-protocol/tests/conformance/recovery_cutoff/test_hrc_semantics.py` | `794ac0c34aaad921e5d4a5bcc42b6601f7caf817` | 25 HRC unittest cases plus 12 JPF bidirectional-join cases |
| Wire interop candidate suite | `08-bmcp-protocol/tests/conformance/recovery_cutoff/test_wire_interop.py` | `18e50957848178f3f35593b3e618dfa9b90cdb31` | Strict JSON parsing, duplicate-key rejection, absent/null distinction, canonical test bytes, counter encoding and critical-field behavior |
| RecoveryJoin schema candidate | `08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.0.schema.json` | `9a0aa3f2b5165a12e4326437c95e91d9f1adbe75` | Strict structural candidate for both directional edge sets, owner snapshots, JF-10 sub-join and difference sets |

Run the dependency-free candidate suite from the test directory:

```bash
python -m unittest -v test_hrc_semantics.py test_wire_interop.py
```

The HRC suite has 37 unittest methods: HRC-01..25 and JPF-01..12. The wire suite has 10 additional methods. The code is committed as an executable candidate, but **has not yet been run in CI or independently reproduced**. No PASS is claimed.

### 11.1 Semantic model vs wire model

The HRC test harness operates on a normalized semantic projection of the 1.0.4 message family. It is not a replacement for JSON Schema validation or signature verification. A production adapter must map exact wire fields into the normalized model without dropping:
- request vs admission enumeration status and independent roots/counts;
- owner-specific high-waters and namespace identity;
- COC prefix position, participant entry digest and mandatory primary C admission ref;
- additional I/D evidence edges and JF-10 participant tuple;
- exact Batch, Manifest record and JoinProof identities/digests.

The candidate helper digest profile named HRC-TEST-v1 is test-only. It MUST NOT be used as a production canonicalization or signature profile. Production canonical bytes and cryptographic trust require H approval and I security approval.

### 11.2 Join Proof schema boundary

The new RecoveryJoin schema is a candidate extension, not a change to recovery-cutoff 1.0.4 or JF-10 bridge 1.1.0. It carries separate OwnerAdmissionToParticipant and ParticipantToOwnerEvidence relations. The current recovery-cutoff 1.0.4 participant entry's owner_admission_ref remains the primary C admission anchor; it does not encode all I/D receipt, work, attempt, barrier or lineage evidence. Those are represented as explicit typed edges in RecoveryJoinProof.

Schema validity alone cannot prove:
- prefix completeness against the live quorum log;
- owner-ledger completeness or empty-set truth;
- signature/key status and anti-rollback;
- both directional set equality;
- currentness CAS at owner gate release;
- same-XID I/Storage terminal coupling.

Those remain runtime semantic validators and owner-authority checks.

### 11.3 Required next implementation increment

1. Add a wire-to-normalized adapter for all six 1.0.4 message families.
2. Validate each raw message against its exact JSON Schema before semantic evaluation.
3. Implement the six validators in §1 as production modules, with injected H canonicalization and I trust-verifier interfaces.
4. Replace test-only digest helper with the exact H/I-approved profile only after formal approval.
5. Run the 47 existing structural parser cases plus HRC-01..25, JPF-01..12 and WIRE-01..10 in CI.
6. Add differential vectors in at least two independent implementations; compare canonical bytes, digests, signature input bytes, error codes and replay behavior.
7. Publish raw CI logs, deterministic seeds, source/schema hashes and independent H/I/D/C/Storage review.

Until then, status is **EXECUTABLE CANDIDATE COMMITTED / NOT RUN / NOT CONFORMANCE-VERIFIED**.
