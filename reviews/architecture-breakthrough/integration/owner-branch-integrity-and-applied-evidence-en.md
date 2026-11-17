# Live Owner Branch Integrity & Applied Delivery Evidence Review (2026-11-18)

- Review ID: ABR-INTEGRATION-002
- Integration track: ABR-INTEGRATION-001 / Draft PR #93
- Governance tracker: Issue #43
- Current main: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Current main tree: `7096e0bc3fdc9a390fccff388f9261522fa424f2`
- Scope: live B/C/D/E/F/G/H/I/Storage branch snapshots, H/C tree-integrity incident recovery, H Applied Delivery Evidence 1.0.0 candidate and consumer-acceptance boundaries.
- Evidence class: exact tree/file readback plus CI metadata; not a full module semantic audit or independent Owner approval.

## 1. Current-state summary

This review confirms an important state change: the damaged HEADs recorded by the earlier A H/C branch-integrity reports are no longer the current Owner branch HEADs. Both H and C have subsequent restoration commits. Relative to their pre-incident baselines, the restored trees contain only a small number of additions and no further deletions.

| Item | Current evidence | Integrated disposition |
|---|---|---|
| H tree integrity | H restored its full tree; current tree adds only 8 files relative to pre-incident HEAD | **Recovery verified; retain incident record** |
| C tree integrity | C restored its full tree; current tree adds only 2 files relative to pre-incident HEAD | **Recovery verified; retain incident record** |
| H Applied Delivery Evidence 1.0.0 | Schema, reference validator, 11 tests and workflow present; CI SUCCESS | **TEST/CONFORMANCE CANDIDATE** |
| CSubmitOutcome 1.0.1 | Current C Owner HEAD contains schema, tests and workflow; CI SUCCESS | **Bounded CI evidence exists** |
| C workflow 1.0.1 trigger path | Current workflow lists only 1.0.0 schema; PR #94 adds the 1.0.1 path | **Trigger gap identified; PR #94 pending review** |
| H 1.0.0 Applied consumer acceptance | H requires C/G/I acceptance; no exact-Blob C/G acceptance decision for H 1.0.0 was found on current heads | **OPEN / NOT FROZEN** |
| Global Applied | G contract is a normative design draft; implementation and cross-Owner acceptance are unverified | **NOT FROZEN / NOT PROVEN** |

## 2. Current main and Owner HEAD snapshot

Live `main` reads as `e52594f181d2edb77448adcfed64a0fbdffaf3aa`. Its tree is `7096e0bc3fdc9a390fccff388f9261522fa424f2`. PR #87's temporary default-branch file write was compensated by a deletion commit; the current main tree is consistent with the recorded baseline, but the Git history pointer has advanced. Do not claim that the commit history was unchanged merely because the tree is identical.

The following HEADs were read from recursive branch trees in this pass:

| Owner | Branch | HEAD | Blob file count | Exact key source / Blob |
|---|---|---|---:|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | 58 | ADR-001 Fact/Claim `df77e4a93cb8fef689ae7c828888d960cbf381d6` |
| C | `session-c-agent-integration-2026-11-16` | `88992da30331121b81cf2773acab11d921daf281` | 136 | CSubmitOutcome 1.0.1 `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; C/G Phase 3.8.23 `4860c627b4d7e84e23fb39ad83411674f3b88c7b` |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | 86 | Forget Fence / Publication Gate `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | 54 | Forget Fence / Derived Registration `00e37ba56596e710513c8d0568acd79141d9101b` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | 49 | Runtime Forget suppression `ce59252dbbdc5d10d016704797e9ba12d5a941bd` |
| G | `session-g-memory-context` | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | 50 | Applied persistence contract EN `bd297873bc1e593280484a43cb44b56058d9c4ff`; ZH `82553a47fae2d5e796e0742b46231afe465e75b2` |
| H | `session-h-bmcp-protocol` | `6608cde89d959257db612d8ff8080f631333f3f3` | 216 | Unified 1.2.15 Schema `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; Applied 1.0.0 Schema `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`; Validator `2f6de24eea737cf75a16ead7495bea4627bb1bb4` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | 161 | Global Forget inventory `9100061fa986fb6676656169de3fcf9fc1c72664`; PermissionEpoch confirmation `bae6a24fe3a374bc816993979a8fa9af52517dea` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | 122 | Producer/Dependency/Visibility `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`; topology ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`; Restore high-water `4f656163aeba532a441eaed1d293a48e2363cb4a` |

**Freshness limitation:** The table proves that these branch HEADs and selected Blobs were read in this pass. It does not prove that every cross-owner Blob referenced inside each Owner document is current, nor does it replace line-by-line review of every file in all nine Owner packages. Issue #43 G1 remains PARTIAL.

## 3. H tree-integrity incident: recovery verification

### 3.1 Incident chain

- Last reviewed pre-incident HEAD: `0d36324457e39bd50ad56ae902d477c4ea765b61`.
- Destructive commit: `0277a8b9ee63be850acc0b8b1b08625524aaa33b`, whose parent is exactly the pre-incident HEAD.
- Destructive commit stats: 160 additions / 92,969 deletions; compare reports 205 files removed and 3 workflow renames; recursive tree contained only 5 files (the A report described 7 entries including directory nodes).
- H restoration commit: `1ca07ed575be1fb2a690e3c2e110a89880ea6454`, explicitly titled “Restore complete branch tree and retain Phase 3.8.23 owner decisions”.
- Current H HEAD: `6608cde89d959257db612d8ff8080f631333f3f3`.

### 3.2 Recovery evidence

Direct compare from pre-incident HEAD `0d363244...` to current H HEAD `6608cde...`:
- ahead 7 commits / behind 0;
- 8 files added;
- 0 files removed;
- 0 files modified;
- 0 files renamed.

The current H tree therefore has more than an Owner assertion: Git compare shows the pre-incident file tree is retained and 8 files were added afterward. The current recursive tree contains 216 Blob files.

### 3.3 Exact H CI scope

- H Applied Delivery Evidence Conformance run `44130722532`: SUCCESS; exact test commit `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`; H's report lists 11 passing tests.
- H Recovery Cutoff Conformance run `44130905292`: SUCCESS; exact HEAD is current H `6608cde...`.
- H Provider Outcome Conformance run `44129938964`: SUCCESS; exact commit `1ca07ed...`.
- The H Applied 1.0.0 workflow's test commit `4e65a2...` is an ancestor of current H HEAD; the final commit at `6608cde...` records the bilingual CI result. Do not misstate the Applied run SHA as the current HEAD.

### 3.4 Remaining H gaps

H Phase 3.8.24 explicitly labels Applied Delivery Evidence 1.0.0 a **TEST/CONFORMANCE CANDIDATE**, not a production cryptographic or durable replay service:
- The local canonicalizer is test-only sorted-key JSON, not a production JCS/profile.
- Signature, key status, profile registration, C final boundary, G binding, capability epoch and durable observation are injected callbacks; production callbacks/services are not implemented.
- SDK, cross-language vectors, Runtime Adapter integration, durable observation ledger, production trust roots/key status and crash/restore validation remain open.
- H Phase 3.8.23 historically accepted identity semantics with exceptions while leaving wire mapping NOT FROZEN. Phase 3.8.24 adds a candidate implementation; it does not automatically promote the earlier decision into consumer acceptance.

## 4. C tree-integrity incident: recovery verification

### 4.1 Incident chain

- Pre-incident C HEAD: `71047cdb51139ca4080ac67f451e38a48698859d`.
- Destructive commit: `a5dff993e5c2928a28deb777c41023cfe923366f`, whose parent is the pre-incident HEAD.
- Destructive commit stats: 144 additions / 21,673 deletions; compare reports 133 files removed, 2 added and 1 renamed; recursive tree contained only 3 files.
- C restoration commit: `88992da30331121b81cf2773acab11d921daf281`, titled “Restore complete branch tree and retain Phase 3.8.23 owner decisions”.

### 4.2 Recovery evidence

Direct compare from pre-incident C HEAD `71047c...` to current C HEAD `88992d...`:
- ahead 2 commits / behind 0;
- 2 files added;
- 0 files removed;
- 0 files modified;
- 0 files renamed.

The current C recursive tree contains 136 Blob files. The C Phase 3.8.23 bilingual identity decision and CSubmitOutcome 1.0.1 schema are present.

### 4.3 C CI and trigger gap

- C Provider Outcome Conformance run `44129914790`: SUCCESS; exact tested commit is current C HEAD `88992da...`.
- Current C workflow Blob `a1f0b8f884f0f294fb3ec96da7c4f11e294e5142` lists only the CSubmitOutcome 1.0.0 schema in push.paths; it does not list the 1.0.1 schema.
- C PR #94 adds only `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` to workflow paths. The scope is precise and does not change schema semantics.
- PR #94 remains Draft. This review does not treat it as merged and does not claim that the new path has been independently tested by a schema-only push. Trigger reliability for an isolated 1.0.1 schema change remains pending that PR's validation.

## 5. Applied Delivery Evidence 1.0.0 cross-owner acceptance matrix

### 5.1 Confirmable now

| Authority | Exact decision/evidence | Current state |
|---|---|---|
| G | Phase 3.8.22 Applied persistence contract, EN/ZH Blobs above | G-owned normative design draft; implementation NOT VERIFIED; exact consumer review of new H 1.0.0 mapping remains required |
| H | Phase 3.8.23 identity review Blob `be308261...`; Phase 3.8.24 candidate report Blob `f193113f...` | H identity semantics ACCEPT WITH EXCEPTIONS; 1.0.0 candidate schema/validator CI PASS; not G/C/I acceptance |
| C | Phase 3.8.23 C/G identity review Blob `4860c627...` | Accepts only C-owned identity semantics in G 3.8.22; explicitly does not accept H wire mapping |
| I | PermissionEpoch formal confirmation Blob `bae6a24...`; I 3.8 Commit Authorization proposal Blob `54bab048...` | PermissionEpoch technical baseline confirmed; complete production issuer/key/profile registration, crypto profile, canonicalization and trust acceptance remain open |
| D | Forget Fence / Publication Gate Blob `4da0b61...` | D operation semantics DECIDED; D/E interface schema, Storage realization and cross-owner conformance OPEN |
| Storage | Option A topology ADR Blob `bb544ba...`; atomic producer/dependency/visibility review Blob `2ab899...` | L1 logical topology selected; D adoption, L3 adversarial proof and L4 physical realization/conformance remain OPEN |

### 5.2 Non-negotiable boundaries

- H Applied Delivery Evidence 1.0.0 is a separate message family; do not widen or contaminate Unified 1.2.15 Gateway Attestation's P0 allowlist.
- H Gateway ingress replay, H Adapter observation replay and G Applied uniqueness are three distinct idempotency domains.
- C ProviderAttempt/OutcomeRecord identities cannot be substituted for H DeliveryBinding/Evidence/Observation identities.
- G is the sole Applied decision authority; H Validator VALID or C HANDOFF_ACCEPTED alone cannot create Full Applied.
- I PermissionEpoch, D ForgetFenceGeneration, Storage cursor, G ContextVersion and H CapabilityEpoch are distinct namespaces; no numeric comparison, conversion or substitution.
- Unknown injected callbacks in the Applied 1.0.0 validator must remain UNKNOWN; the local test canonicalizer is not a production crypto profile.

### 5.3 Remaining blockers

1. No exact G current-HEAD consumer review of H Applied 1.0.0 schema/validator was found.
2. No exact C current-HEAD review of H Applied 1.0.0 schema/validator was found; C Phase 3.8.23 accepts only the C-owned identity tuple in G 3.8.22.
3. I production signer/profile/key-status/canonicalization/trust registration and anti-rollback remain open.
4. H durable observation ledger, production Adapter integration, SDK/cross-language vectors and production crypto are not implemented.
5. G Applied persistence implementation, same-transaction final currentness validation across D/I/COC/Storage and restore behavior are not physically verified.
6. Storage JF-10 same-GID terminal proof and D/I/Storage visibility ordering still require real-topology evidence and a crash campaign.

**Therefore: H Applied Delivery Evidence 1.0.0 = candidate implementation + bounded CI PASS; Global Applied = NOT FROZEN / NOT PROVEN.**

## 6. Forget P0: refined status of current Owner contracts

The Owner files read in this pass support the following boundaries:
- D `forget-fence-operation-and-publication-gate.md`: D operation semantics are DECIDED; D/E interface schema, Storage/Consistency realization and cross-owner conformance remain OPEN. D requires ProducerWork registration and Fence installation to share one linearizable ordering domain; the final visibility commit must revalidate Fence, Dependency Registration and I authorization in that domain.
- E `forget-fence-and-derived-registration.md`: E enforcement contract remains CANDIDATE; every derivative must remain private/non-queryable until durable D dependency registration, current PermissionEpoch/Fence and final Publication Gate succeed.
- I `global-forget-target-inventory-and-completion-evidence.md`: global inventory/completion remains CANDIDATE; D/E/F/G/H/Storage conformance is OPEN. I PermissionEpoch technical confirmation is normative, but external governance profile approval remains BLOCKED.
- I `phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md`: still an I-role proposal; exact Owner approval, crypto profile and conformance remain OPEN.
- Storage `phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md`: provides a candidate atomic realization design; it is not proof of physical topology deployment. Storage L1 Option A ADR is selected, not L3/L4.
- Storage Restore high-water contract and reference model still need physical evidence from real database backup, PITR, failover, rejoin and restore behavior.

Therefore the P0 / NOT READY Forget disposition in ABR-INTEGRATION-001 remains correct, but the precise wording is: **some logical Owner semantics already exist; cross-owner atomic composition, exact interface adoption, physical realization and failure proof remain open.** It would be inaccurate to say that no logical ordering contract exists at all.

## 7. Proposed Issue #43 gate update

| Gate | Effect of this review | Suggested status |
|---|---|---|
| G1 exact current pins | B/C/D/E/F/G/H/I/Storage HEADs and key Blobs refreshed; complete file-level ledger and all referenced-source freshness remain incomplete | PARTIAL |
| G2 Owner authority/consumer acceptance | H/C recovery is not acceptance of Applied 1.0.0 by C/G/I; B ADR blocked | BLOCKED |
| G3 end-to-end state/causal model | Forget logical contracts read; full serial-order and cross-owner race/crash proof not completed | BLOCKED |
| G4 P0/P1 proof | H/C trees restored; JF-10/Forget/Applied/Restore P0/P1 remain open | BLOCKED |
| G5 technology feasibility | Storage L1 Option A selected; L3/L4 and JF-10 physical evidence insufficient | BLOCKED |
| G6 bilingual parity | No complete line-by-line semantic parity review of all Owner bilingual documents in this pass | PARTIAL |
| G7 A integration disposition | Two integration reports submitted in a research Draft PR; Owner decisions still require confirmation by their own authorities | PARTIAL |
| G8 freeze recommendation | Architecture freeze remains unsupported | NOT READY |

## 8. Ordered next steps

1. H: publish a recovered exact-current-head manifest, explain the restoration commit intent/tree and list the 8 new files; keep Applied 1.0.0 separately classified as non-production.
2. C: complete PR #94's 1.0.1 workflow-path review and prove a schema-only push triggers conformance; also issue an exact-version consumer review of H Applied 1.0.0.
3. G: exact-review H Applied 1.0.0 Schema/Validator/P0 projection/identity/replay tuple field by field; do not rely only on H Phase 3.8.23's earlier candidate mapping.
4. I/H: define production signer/profile/key-status/canonicalization/anti-rollback authority, versions, vectors and unknown-state rules.
5. D/E/Storage/I: map D operation semantics, E producer/derived registration, Storage atomic visibility and I CommitAuthorization sequencer into one verifiable order under the same GID/publication operation; prove both race orders and crashes before/after every durable boundary.
6. A: finish source-pin freshness and bilingual parity for all Owner files before updating Issue #43 G1–G8; do not treat tree restoration or CI success as Gate passage.

## 9. Final disposition

- H/C branch tree integrity: **RECOVERED AT CURRENT OWNER HEADS; incident retained; independent Owner intent/acknowledgment remains required where applicable.**
- H Applied Delivery Evidence 1.0.0: **CANDIDATE / BOUNDED CI PASS / NOT PRODUCTION READY.**
- CSubmitOutcome 1.0.1: **CURRENT C HEAD CI PASS; schema-only workflow trigger fix remains pending in PR #94.**
- Global Applied: **NOT FROZEN / NOT PROVEN.**
- Forget/Producer/Derived Publication/Storage/JF-10: **P0 remains open; some logical Owner semantics are decided, but cross-owner and physical closure are unproven.**
- Issue #43: **G1 PARTIAL; G2–G5 BLOCKED; G6 PARTIAL; G7 PARTIAL; G8 NOT READY.**

This report is an integration review only. It does not replace H/C/G/I/D/E/Storage Owner decisions or authorize implementation, merge, Gate release, deployment or production activation.


## 10. ABR-INTEGRATION-003 — Bounded cross-owner Forget model extension

A reproducible Python explicit-state model has been added:
- `reviews/architecture-breakthrough/integration/model/forget_cross_owner_model.py`
- `reviews/architecture-breakthrough/integration/model/test_forget_cross_owner_model.py`
- `reviews/architecture-breakthrough/integration/model/README.md`
- Branch-scoped CI: `.github/workflows/abr-forget-cross-owner-model.yml`

**Result:** the safe transition graph explored 27,472 state/depth pairs through depth 14 with no modeled invariant violation; 11 weakened-guard mutants each produced the expected shortest counterexample. The model command and unittest regression suite both passed GitHub Actions run [44136327645](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44136327645), tested at `89a680bbad7246952d51c61c137b0c3611f52a06`.

New coverage includes D ProducerWork/Fence high-water, E attempt/lease/DLQ/retry/Derived Registration, I COMMIT_WON/REVOCATION_WON/UNKNOWN and held revocation, Storage visibility, F cache/read disclosure, inventory-gap reopening, restore high-water replay, and durable receipt/lost-ACK retry.

Important refinements:
- I COMMIT_WON before revocation permits only that exact participant to complete; revocation is held until the Storage terminal outcome.
- If revocation wins first, publication is forbidden.
- If Fence wins first, final visibility cannot commit; UNKNOWN/NO_PUBLICATION must be resolved and lease terminal evidence established before barrier closure.
- If publication wins first, a later Fence must include it in the barrier; suppress before terminalization.
- A stale backup cannot be released until the current D high-water is replayed.
- ACK loss does not roll back a durable receipt; the same operation key + normalized digest returns the original receipt.
- **Model refinement:** a stale cache fill alone is not sufficient to constitute external disclosure if the final read gate still enforces current Fence/Permission. Stale cache contents may still violate cache freshness/fill contracts, but the security invariant should directly test whether disclosure occurred. The earlier A model treated cache refill itself as a counterexample; this model distinguishes retained bytes from actual disclosure.

This remains a bounded single-Producer/single-lineage/single-Fence abstraction. It does not cover complete producer/recipient/backup inventory, arbitrary dependency DAGs, real MVCC/WAL/2PC, COC/G Applied implementation, multi-replica I/Storage recovery or a physical topology. **It is not TLC, an unbounded proof or production safety certification.**

