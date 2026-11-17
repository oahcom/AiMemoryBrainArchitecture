# Phase 3.6.8 — Exact-Version Binding Manifest
## Storage v3.2.2 + C Provider Outcome + H Unified BMCP Schema 1.2.4

- Owner: A — Principal Integration Architect (integration register authority)
- Status: **EXACT REVIEW BUNDLE — NO JOINT CONTRACT FREEZE / NO PRODUCTION AUTHORIZATION**
- Date: 2026-11-17
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Scope: COC Recovery Cutoff Batch / Participant Manifest order, C Provider Outcome, H unified protocol schema and current I/D cross-owner tuple inputs.

## 1. Normative exact bundle

The following immutable Blob IDs are the only artifacts in this review bundle. No floating branch-head or "latest" references are normative.

| ID | Owner | Artifact | Branch | Exact Blob | Scope / disposition |
|---|---|---|---|---|---|
| A-01 | A | `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md` | `session-a-integration-2026-11-16` | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` | Parent COC architecture §§11–12; integration baseline only |
| S-01 | Storage | `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.2.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `4039fd4c08aa0bb7da63fe5dab92e419487f48d1` | Current Storage proposal; owner-local freeze before P; complete union Manifest; Batch→Manifest→read-back |
| S-02 | Storage / COC companion | `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `8ac17816476f280ab6fb3afca0688aa03e37de1d` | Current PostgreSQL §14 participant identity/receipt companion |
| S-03 | Storage | `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | v3.1 historical parent |
| I-01 | I | `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md` | `session-i-security-governance-2026-11-16` | `cf4b76f151204fa47b156b5d807e7378c28fd268` | Current I proposal: gate/registry/currentness/key/restore and signed-subrecord requirements; exact I approval still pending |
| D-01 | D | `03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md` | `session-d-memory-brain-2026-11-16` | `2d95099a2e19a8cbec325925b70da576f73d9899` | Current D proposal: boundary fencing, lineage closure, C provider outcome and I currentness requirements; exact D approval still pending |
| C-01 | C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `session-c-agent-integration-2026-11-16` | `45a48249717c8cddb07ab96197730ef93d406c22` | C source contract and existing Provider Outcome authority |
| C-02 | C | `07-agent-integration/phase-3.6.8.2-c-provider-outcome-storage-v3.2.2-current-i-d-rereview.md` | `session-c-agent-integration-2026-11-16` | `535579cdfeedf705195bb4aa04cf1a85cb9b9a0f` | Exact C review: ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS |
| H-01 | H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `session-h-bmcp-protocol` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | H identity, protected operation and wire ownership baseline |
| H-02 | H | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.4.schema.json` | `session-h-bmcp-protocol` | `1dc2d3a2675503c5ab97134d57d4c2b7bb80ca15` | Current unified Draft 2020-12 schema candidate, 11 message variants, 2 manifest member variants |
| H-03 | H | `08-bmcp-protocol/phase-3.6.8.3-h-unified-coc-jf10-provider-outcome-schema-v1.2.4-decision.md` | `session-h-bmcp-protocol` | `3aa617cd7066405d84a5bd027eaaad1f9c3bc9bc` | Exact H review: ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS; schema not frozen |

## 2. Exact ordering pinned by this bundle

The normative recovery sequence is:

1. **S0a — Owner-local freeze:** I, D and C independently close their affected admission/side-effect gates and atomically capture request/admission ledgers, high-waters, counts, roots and anti-rollback anchors. In-flight operations not yet registered in COC remain in their owner ledgers.
2. **S0b — COC prefix freeze:** after quorum restoration, enter RECOVERY_FENCED and obtain linearizable prefix `P=(CoordinatorEpoch, CoordinatorIndex, EntryDigest, CommittedConfigurationEpoch)`. No protected COC append follows P.
3. **S1 — Complete union Manifest:** enumerate all COC ParticipantIntentRefs at/before P plus every applicable I/D/C owner-local admission through frozen high-waters. Represent members as typed `COC_PARTICIPANT` or `OWNER_LOCAL_ADMISSION`; no COC absence may silently omit an owner admission.
4. **S2 — Batch commit:** quorum-commit `COC_RECOVERY_CUTOFF_BATCH` binding P, RecoveryEpoch, I/D/C snapshots, ManifestId/Digest/count and enumeration high-waters.
5. **S3 — Manifest Record commit:** quorum-commit the separate `PARTICIPANT_SET_RECONCILIATION` record, referencing the exact prior Batch position/digest and carrying the canonical union member payload.
6. **S4 — Linearizable read-back:** re-read both committed records and verify order, P, RecoveryEpoch, ManifestId/Digest/count, member union, owner roots/generations and both quorum proofs.
7. **Only after S4:** participant-specific recovery/reconciliation may begin. No provider invocation/retry, Storage resolution, visibility publication, owner Gate release or serving may occur after S2/S3 alone.

The ManifestDigest covers canonical union payload + P + RecoveryEpoch + frozen owner snapshot roots; it excludes the later Batch back-reference. The Manifest Record envelope carries the exact Batch position/digest, avoiding circular hashing.

## 3. C Provider Outcome binding

C alone authors `CSubmitOutcome` from actual provider/runtime boundary evidence. The exact outcome is bound to:
- CSubmitOutcomeRef/digest and C authority/adapter boundary;
- OwnerAdmissionRef, C owner ledger ref/version/root/high-water;
- optional COC ParticipantIntentRef, explicit null + reason when not yet registered;
- provider identity, stable idempotency-key reference, provider request/receipt;
- FinalRequestBoundaryId and exact request digest;
- transaction/reservation and applicable Storage PreparedParticipant/GID/DB incarnation/attempt/ledger/tuple;
- I terminal and D clearance/fence evidence where applicable.

Outcome enum: `HANDOFF_ACCEPTED`, `HANDOFF_REJECTED`, `NOT_INVOKED`, `UNKNOWN/IN_DOUBT`. Storage COMMITTED, I COMMIT_WON, D clearance, COC commit, H ACK and G Applied do not synthesize provider outcome. HANDOFF_ACCEPTED is not inference completion, content correctness or G Applied.

C's exact review is conditional on provider-specific same-key idempotency, authoritative receipt/lookup and crash recovery; these remain unverified.

## 4. H Unified Schema 1.2.4 binding

Schema `bmcp.coc-jf10-unified/1.2.4` covers:
- COC Recovery Cutoff Batch;
- Participant Manifest Record;
- Owner Pending Gate / Owner Gate Release;
- RecoveryEpoch completion;
- five JF-10 participant/decision/resolution/reconciliation messages;
- C Provider Outcome.

It has two typed manifest member variants: `COC_PARTICIPANT` and `OWNER_LOCAL_ADMISSION`. The latter requires owner-ledger identity/root/high-water and an explicit nullable COC ParticipantIntentRef with absence reason when null.

H's exact decision is conditional. JSON Schema is structural only; S0a/S0b order, S1 union completeness, Batch/Manifest cross-record equality, count/member equality, quorum proofs, signatures, canonical bytes and actual provider outcome require semantic validators and owner-authoritative verification.

## 5. Superseded exact artifacts (not normative for this bundle)

- Storage v3.2 Blob `e7ab80cdf8af5e0d50c407b06a5deb618d1e2ae6` — superseded by v3.2.1 and v3.2.2.
- Storage v3.2.1 Blob `491e8e916cf9b1609c5220fb41fb766b8cddccf2` — superseded by v3.2.2 after current I/D exact pins were refreshed.
- H unified schema 1.2.0 Blob `8eb2d28701483b1e49cfb55c954ec4adfa54f3b4`, 1.2.1 Blob `746d66aa231af1ef2f7c3571dbc31c46e28b2547`, 1.2.2 Blob `6d4e6e4075fcec392dbc46c97f132a7ca08d8df1`, 1.2.3 Blob `4ff62c587dac1566d95004a0fad95ca35d25f4e6` — superseded by 1.2.4.
- C v3.2 review Blob `f538d921d06c92dfaba13fbe326a80d6550fe1b7` and C v3.2.1 review Blob `377c16531d5d8b43b353a09f61ebac9e999fc48d` — exact predecessor reviews only.
- H v3.2/v3.2.1 review Blobs `1079350927991032ca13e6af1ec3f84f1eabbc2b` and `36ed239019e34eaafff9e22b127a58e8e2557842` — exact predecessor reviews only.

No approval transfers across Blob IDs. This manifest is the only current bundle index for the A final review described below.

## 6. Remaining governance and verification gates

- I and D Phase 3.6.8 artifacts above are current proposals but still require their own exact-Blob Owner decisions. Their inclusion is not approval.
- Storage v3.2.2 is a revised proposal, not a Storage implementation or conformance result.
- C and H decisions are assistant-authored role-based review proposals; they are not independent human Owner signatures or vendor approvals.
- H schema 1.2.4 is not a frozen wire/cryptographic profile. I/H trust policy, key lifecycle, canonicalization and anti-rollback approval remain open.
- Provider-specific idempotency and same-key recovery are not verified.
- COC quorum operator/deployment, crash/restore, exact canonical-byte interoperability and runtime fault tests are not evidenced.
- Gate B/C sequencing, JF-10 P0, I36-GOV-01..10 governance approval, Multi-PolicyDomain atomicity, Global Forget E2E, physical erasure and Production Activation remain OPEN/BLOCKED/NOT VERIFIED as applicable.

**Manifest disposition:** exact immutable review bundle published for A's final integration review. It is not a joint Owner freeze, implementation PASS, production authorization or Global Forget completion.

## 7. Provenance

Assistant-authored integration binding manifest committed at the user's direction. It is not an A cryptographic signature or independent human A Owner approval.
