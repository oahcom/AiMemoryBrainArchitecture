# Unified Remediation & Evidence Register — Current Snapshot

- Register ID: P-UNIFIED-MBR-REMEDIATION-001
- Revision: 2026-11-17 / current live-branch reconciliation
- Status: **OPEN — coordination register only**
- Supersedes: earlier cumulative snapshots and stale status rows in this file. Historical decisions remain immutable at their exact artifact/blob pins.
- Authority: Session P coordinates and records evidence. A–I Owners retain module decisions; Storage retains physical storage realization; I retains security/governance authority; the authorized project governance body retains G0/PGA authority.

## 1. Decision and evidence rules

1. An artifact commit proves only that an artifact exists at a pinned blob.
2. An Owner decision applies only to the exact source blob(s) it names.
3. A role-simulated review authored by the coordinating ChatGPT session is a technical review input, **not an independent Owner signature**.
4. ACCEPT WITH CONDITIONS is not unconditional acceptance, implementation approval, conformance PASS, production readiness or system freeze.
5. Reference-model/schema tests do not prove production runtime, multi-process races, real adapters, physical erasure, restore safety or operational readiness.
6. DEFERRED_TO_ENGINEERING_PHASE is not an architecture defect, but its future acceptance criteria must remain explicit.
7. No project-wide freeze, G0 ratification or main-branch integration is inferred from module-level decisions.

## 2. Current branch snapshot

Observed GitHub branch refs at this refresh. These are point-in-time HEADs, not immutable decision pins.

| Role | Branch | Observed HEAD |
|---|---|---|
| A | session-a-integration-2026-11-16 | bccd8769e981310b85da4974fb4af98e41f9f374 |
| B | session-b-domain-model-phase3 | 310f305575d6f406e80d5d6ebf951bcd9e79e35f |
| C | session-c-agent-integration-2026-11-16 | 018de5044810e755d4e21cb21e982526c27eb9a8 |
| D | session-d-memory-brain-2026-11-16 | a3ea0de75ca7b2297589293ec142f2cb07757282 |
| E | session-e-memory-compiler-2026-11-16 | 5fb76b666fac49ceeb51ddb7c320fe5975313d99 |
| F | session-f-memory-runtime | e4c26214b8f78169c0e20f1faae23f945c3afeb9 |
| G | session-g-memory-context | b0c515399c6a336dcbf17a1ced6925413c804d5c |
| H | session-h-bmcp-protocol | 26378ea59675f31ac0455d745e9cbedab898db8c |
| I | session-i-security-governance-2026-11-16 | ba0d1dfcca9392f3a20c405169c83b41da3f12b7 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 337fe8bffa178e64ad8e4750f1ede1d561424edc |
| main | main | 3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f |

P vs main remains **diverged**. Re-query the live compare before any integration because every P coordination commit changes the ahead count. No merge, force-update or main write is authorized or performed.

## 3. Current system gate vector

| Gate / decision | Current state | Meaning |
|---|---|---|
| Nine A–I module baseline proposals | **PROPOSED** | All nine proposals exist; no exact Owner baseline adoption is recorded. |
| A–I baseline adoption | **OPEN** | Context/COC acceptance artifacts are not module baseline adoption. |
| TAB-001 Owner technology reports | **8/8 PRESENT** | B/C/D/E/F/G/H/I reports exist. A's final report has a later conditional reassessment but stale front matter and source manifest still need consolidation. |
| TAB-001 system direction | **CONDITIONAL PASS — architecture design only** | Candidate direction may proceed to controlled engineering planning; not a technology freeze. |
| B Fact/Claim ADR-001 | **ADR-BLOCKED / P0** | No formal Architecture Governance decision. |
| Applied 1.1 exact design bundle | **DESIGN DECISIONS RECORDED WITH EXCEPTIONS** | A's matrix distinguishes the immutable Applied package pair 4961ffef... + companion fc3bac39... from separate COC/JF-10 bridge architecture a3c51ec.... This resolves the former pin-role ambiguity; do not substitute one blob for the other. |
| Applied schema / interface freeze | **NOT AUTHORIZED** | H schema remains candidate; final-request/runtime evidence and conformance remain open. |
| Context optimization / Observation Archive | **CONDITIONAL DESIGN ACCEPTANCE** | A's final matrix records eight non-A Owner perspectives as ACCEPT WITH CONDITIONS. F/G joint Recall contract and module baseline updates remain open. |
| JF-10 Gate A | **PARTIAL PASS / OPEN** | PostgreSQL 18.7 isolated capability evidence exists; remaining architecture decisions, I/D cross-owner semantics and operational profile remain open. |
| JF-10 Gate B prior protocol 4ac63... | **DESIGN-LEVEL ACCEPTANCE WITH EXCEPTIONS** | Exact role-based acceptance matrix exists for that exact blob only. |
| JF-10 current protocol 86ff3... | **PUBLISHED / FOCUSED RE-REVIEW PENDING** | §14 adds PreparedTransactionGID/native-XID mapping. Storage accepts with conditions; A/H/I role reviews are coordinator-simulated, H/I no approval; independent Owner decisions remain pending. |
| Storage Design v2 4ed423... | **FRESH PROPOSAL / REVIEW OPEN** | Adds R1–R6 disposition, recovery epoch completion, repeated batches and GID mapping. Issue #16 remains open; no independent exact-v2 acceptance is established. |
| Prepared-participant trust / wire envelope | **NOT APPROVED** | A conditional with amendments; H and I are CANDIDATE / NO APPROVAL in role-simulated reviews. |
| JF-10 Gate C | **DEFERRED_TO_ENGINEERING_PHASE** | No production implementation/fault-injection PASS. |
| JF-10 P0 / multi-PolicyDomain | **OPEN / BLOCKED** | Single-I-PolicyDomain architecture profile only; production activation not authorized. |
| I Global Forget | **GOVERNANCE-BLOCKED / NOT COMPLETED** | I36-GOV-01..10 proposal only; no external governance approval, production inventory seal or target evidence. |
| Project G0 / architecture freeze | **GOVERNANCE-OPEN / NOT AUTHORIZED** | No PGA appointment or exact G0 approval evidenced. |

## 4. Current COC / JF-10 exact-version map

| Artifact | Exact pin | Current decision status |
|---|---|---|
| A COC/JF-10 bridge architecture | Blob a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d | Owner boundary decisions recorded with exceptions; A's separate R1–R6 review remains open. |
| Common JF-10 v2 protocol | Blob 94679897e84a6f58fd8b9467b5249e1a885cb0b0 | Existing decisions apply only to this exact protocol; generic XID wording needs alignment with the newer GID/native-XID distinction. |
| Phase 3.6.3 COC protocol prior revision | Blob 4ac63ac79491e79ec0c9114ef73941c73d7bbf25 | A/B/C/D/E/G/H/I/Storage exact role-based design decisions with enumerated exceptions. |
| Phase 3.6.3 COC protocol amended revision | Blob 8ac17816476f280ab6fb3afca0688aa03e37de1d (live file re-fetch) | Current live companion includes expanded §14 identity tuple; v2 header still pins 86ff3..., creating version drift. Exact cross-version reconciliation and independent Owner review pending. |
| Storage Design v2 | Blob 4ed4234ce548a814a9496adf7a14c4459ea9f7ce | Fresh proposal. Includes R1–R6 disposition, recovery manifest/batches, owner gate release, GID/native-XID distinction. Issue #16 open. |
| H JF-10 schema candidate | Blob a8a945cc3623c2907003b93625e3c79742150944 | Candidate only; opaque XID reference fields are not yet explicitly mapped to PreparedTransactionGID vs native XID or DatabaseIncarnationRef. |
| A exact COC acceptance matrix | Blob 9a39e48a394fedbab16d15589056d59ef33f390f | Covers prior protocol Blob 4ac63..., not amended Blob 86ff... or Storage Design v2 4ed.... |

The old 4ac63... acceptance must not be carried forward to 86ff3... or 4ed423.... The A/H/I role reviews of the two newer targets explicitly disclose coordinating-session provenance and are not independent signatures.

## 5. Executed evidence — separate suites, separate claims

| Area | Exact evidence | Result | Non-claim |
|---|---|---|---|
| Storage PostgreSQL 18.7 capability | Pinned PITR/prepared-XID workflow code set; runs 43958775001 and 43959079736; tested code commit 83bdacbafa840808dca9be7a8c76c4df83c63504; later Storage changes reviewed as documentation-only | **7/7 PASS** | Not production DB selection, COC implementation, production HA/fencing, real I/D ledger integration or production restore proof. |
| F anti-resurrection reference model | Model Blob 33fa2ca2dc29771aca241e194f13e078a4f8d774; tests Blob c2575327a75577923440ef770d42122218a1e091; run 43961714501, job 133630540252, commit f1ba5c478e395da6b126423e32e20d0990e61920 | **19/19 PASS** | Logical reference model only; no actual ANN/index/cache/Working Set implementation, multi-process race, production reconnect or restore proof. |
| H JF-10 schema + strict parser | Schema Blob a8a945cc3623c2907003b93625e3c79742150944; schema tests Blob 74bc4286abe1489ce29c2446c6fc22445784609f; parser Blob 3b9b3da645448c773c95a9dcd3c57c8c109bb2da; parser tests Blob f9c8f44da5c4d52efe78368c54a73eaa1286c374; run 43963251050, job 133635914698 | **23/23 PASS** | Candidate schema/reference parser only; no canonicalization profile, signature verification, key custody, GID/native-XID field mapping, generated SDK or live transport interoperability. |
| I Global Forget inventory/completion model | Tests Blob 428e15c6263b5b2d730b93ce5412d55e782a449b; run 43963450717, job 133636592112, tested commit 8a6a6e67696c496e265b3d87f1a550fe5e8bb2a0 | **30/30 PASS** | Logical model only; no production inventory registry, real TargetInventorySeal, external recipient proof, physical erasure or governance approval. |
| COC in-memory outage model / JF-10 semantic validator | A integration report records separate reference suites | **11 / 18 PASS** | Not a Raft/COC service, distributed fault injection or production conformance. |

## 6. Active remediation actions

| ID | Priority | Work item | Accountable authority | Current state | Closure evidence |
|---|---|---|---|---|---|
| UMR-001 | P0 | Resolve Fact/Claim ADR-001 | B recommends; designated Architecture Governance authority decides | ADR-BLOCKED | Exact option, rationale, approver authority, version, migration and consumer acceptance. |
| UMR-002 | P0 | Close remaining JF-10 Gate A architecture decisions | Storage + D/E; I for authorization/sequencer; A integrates | PARTIAL PASS / OPEN | Exact producer admission, fence/lineage, prepared participant, visibility/receipt/outcome, restore and authoritative-reader contracts; exact Owner acceptance. |
| UMR-003 | P0 | Focused exact review of current COC protocol 8ac178... | A/B/C/D/E/G/H/I as affected; Storage owns source | OPEN | Independent exact-blob decisions; no carry-forward from 4ac63... or 86ff3...; reconcile §14 GID/native-XID fields and all affected consumer contracts. |
| UMR-004 | P0 | Review Storage Design v2 4ed423... and close A R1–R6 | A/I/D/C/H; B/E/G targeted review; Storage owns source | OPEN — Issue #16 | Independent exact-v2 decisions; verify R1–R6, immutable manifest, repeated batches, owner gate release, GID tuple and normative relationship to current companion 8ac178.... |
| UMR-005 | P0 | Close PreparedParticipant identity, trust and wire contract | A/B/H/I; C/D/E/Storage affected | NOT APPROVED | P has a non-normative candidate mapping at 00-governance/proposals/prepared-participant-identity-and-gate-b-manifest-proposal.md (Blob 371e3c07520897a0c7ba2027c5b9ba0991ae1183). Closure still requires Owner decisions on DatabaseIncarnationRef; PrepareAttemptRef/generation; durable participant-ledger version; authoritative PREPARED readback; original prepare vs recovery coordinates; exact I terminal receipt consumption; strict nominal types and signed bytes. |
| UMR-006 | P0 | Establish canonical COC Gate B artifact manifest | A integrates; Storage/H/B/I own their respective contracts | OPEN | P has a non-normative canonical bundle proposal at 00-governance/proposals/prepared-participant-identity-and-gate-b-manifest-proposal.md (Blob 371e3c07520897a0c7ba2027c5b9ba0991ae1183). A must designate protocol 86ff3... + Storage Design v2 4ed... relationship, pin A bridge a3c51..., common JF-10 protocol 9467..., H schema and exact RecordType/BMCP mapping; state normative precedence and config-epoch/quorum proof inheritance. |
| UMR-007 | P0 | Complete I Global Forget governance | I + authorized independent Privacy/Legal/Security/Identity governance approvers | GOVERNANCE-BLOCKED | Exact I36-GOV-01..10 approvals, sealed target inventory, recipient/backup/restore evidence, exception approvals and physical-erasure evidence where required. 30/30 model tests do not close this. |
| UMR-008 | P1 | Update B typed model and E producer contract for GID tuple | B and E; H/I/D/C/Storage consume | OPEN | Distinct PreparedParticipantRef, PreparedTransactionGID, NativeXidObserved, DatabaseIncarnationRef, DBIdentity and PrepareAttempt types; exact immutable producer/participant tuple and replay rules. |
| UMR-009 | P1 | Update H schema and strict wire envelope for new identity tuple | H; B/I/A review | OPEN | Explicit field mapping or new fields for GID vs native XID, DatabaseIncarnationRef, PrepareAttemptRef/generation, DB incarnation, receipt/proof payload, signer/audience/purpose; positive/negative tests. Current 23/23 tests do not cover these semantics. |
| UMR-010 | P1 | Update Storage readiness §26.2, self-review and COC design pins | Storage | OPEN | Readiness currently says “preallocate exact XID” without GID/native-XID distinction; self-review still pins old 4ac63...; update to current 86ff3... + 4ed423... and one canonical version vector. |
| UMR-011 | P0 | Obtain independent A/I/D/C/H decisions for A R1–R6 | A integrates; I/D/C/H decide their own authority | OPEN — Issue #14 | Each Owner pins exact A bundle and current Storage v2, addresses every finding, and posts append-only decision; Storage's v2 disposition alone is not Owner acceptance; P exact-version audit is non-normative. |
| UMR-012 | P1 | Reconcile A context-optimization decision register and closure tracker | A | STALE / OPEN | Record D/F/G conditional acceptances, new A final matrix, current COC versions and live branch heads; distinguish F/G design acceptance from joint Recall contract acceptance. |
| UMR-013 | P1 | Consolidate A final TAB-001 system review | A | STALE / OPEN | Front matter still says NOT REVIEWABLE while §19.4 says CONDITIONAL PASS; §2.2 still says B/D/E/I reports missing; §19.2 source manifest has stale H/I heads. Refresh current evidence and exact version status. |
| UMR-014 | P1 | Update F/G module baseline proposals | F and G | OPEN | F baseline must include Observation Archive/RecallSession/ReadCursor/ReadReceipt/completeness; G baseline must include TSS/ObservationRef/compaction/fidelity/lineage-loss/Forget invalidation. Current branch changes add acceptance/evidence docs, not baseline adoption. |
| UMR-015 | P1 | Close F/G joint Recall contract | F/G; A coordinates; B/H/I/D consulted | CONDITIONAL / OPEN | One exact same-version F/G contract, field ownership, completeness, stale cursor, authorization, Forget invalidation and paired negative tests; separate conditional acceptances do not equal joint acceptance. |
| UMR-016 | P1 | Promote F anti-resurrection model to runtime conformance | F + D/I/H/Storage | LOGICAL MODEL PASS / RUNTIME OPEN | Real index/cache/Working Set invalidation, multi-process race, offline/reconnect, restore and stale snapshot/Delta fault tests. |
| UMR-017 | P1 | Refresh TAB-001 final report source pins and evidence | A | REVIEWABILITY PASS / REPORT CLEANUP OPEN | All eight Owner reports now exist; refresh branch HEADs and include H 23/23, I 30/30, F 19/19 with explicit non-claims; remove superseded missing-report text. |
| UMR-018 | P1 | Reconcile COC record names and commit proof across protocol/v2/H | A/Storage/H/B | OPEN | Map v2 COC_RECOVERY_CUTOFF_BATCH, PARTICIPANT_SET_RECONCILIATION, OWNER_LOCAL_GATE_RELEASE, RECOVERY_EPOCH_COMPLETED to protocol RecordTypes and BMCP messages; align VoterConfigurationEpoch/COCCommitReceipt quorum proof. |
| UMR-019 | P1 | Close CausalOrderDomain registry and anti-rollback authority | I + Storage + A | OPEN | Explicit I-owned PolicyDomain/CausalOrderDomain registry/version, change/revocation authority, anchor custody/failure domain and stale/restore behavior. |
| UMR-020 | P1 | Refresh Storage readiness and dossier to latest v2 | Storage | OPEN | Pin v2 Blob 4ed423...; reconcile §§23–27 and old Gate B statements; separate Gate A partial, prior4ac accepted, current86ff re-review, v2 fresh review, Gate C deferred. |
| UMR-021 | P1 | Refresh F/G context optimization integration evidence | A/F/G | CONDITIONAL DESIGN ACCEPTANCE | A final matrix has eight conditional Owner perspectives; update old decision register and preserve open F/G joint Recall, runtime and conformance blockers. |
| UMR-022 | P1 | Update I Global Forget evidence record | I | 30/30 MODEL PASS / GOVERNANCE OPEN | Update evidence docs from 25/25 to 30/30; retain explicit non-claims and I36-GOV-01..10 proposal-only status. |
| UMR-023 | P1 | Update H strict parser evidence record | H | 23/23 MODEL/SCHEMA PASS / WIRE APPROVAL OPEN | Evidence doc and current branch pins; strict parser remains reference-only and does not close signature/canonicalization or GID schema. |
| UMR-024 | P2 | Preserve Applied package/COC artifact role reconciliation | A/P | **CLOSED — DESIGN DECISION LEVEL** | A matrix distinguishes immutable Applied pair 4961+fc3 from separate bridge architecture a3c51; do not silently substitute. |
| UMR-025 | P1 | Normalize Gate A/B/C phase vector and remove stale status language | Storage + A | OPEN | Gate A PARTIAL PASS / OPEN; prior4ac design accepted with exceptions; current86ff focused re-review; v2 4ed fresh review; Gate B implementation NOT RUN; Gate C DEFERRED_TO_ENGINEERING_PHASE. |
| UMR-026 | P1 | Preserve strict role/provenance boundary for all Owner decisions | A–I + P | OPEN | Role-simulated coordinator reviews are technical inputs only; obtain actual Owner-session confirmation or replace them with independently authored exact decisions. |
| UMR-027 | P1 | Maintain no-merge integration boundary | P + A; governance authority when appointed | OPEN / SAFETY CONTROL | P/main diverged; live compare and reviewed non-destructive reconciliation required before any integration; no merge/force update without explicit authorization. |
| UMR-028 | P1 | Complete module baseline adoption and governance ratification | A–I + Project Governance Authority | OPEN | Each Owner adopts/rejects exact proposal version; formal PGA appointment and G0 approval required before project-wide freeze. |

| UMR-029 | P0 | Reconcile Storage v2 R1–R6 against current companion protocol and close exact-version gaps | Storage; I/D/C/H/A for their own authority | OPEN — Issues #14/#16 | Session P exact-version audit Blob pending/now published at `00-governance/reviews/storage-v2-r1-r6-coordinator-exact-version-audit.md`; R1/R4 substantially addressed in proposal, R2/R3/R5/R6 remain blocked/conditional. Require exact owner-local linearization, joined C in-flight admission manifest, D per-fence canonical lineage proof, full §14 identity tuple reconciliation, current companion pin 8ac178..., H schema binding to A §§11–12 and independent A/I/D/C/H decisions. No role-simulated review counts as acceptance. |

| UMR-030 | P0 | Close Issue #20 Archive × Forget × Inventory × Restore exact-version owner reviews | D/I/F/E/G/H independently; A integrates; Storage owns realization | OPEN — Issue #20 | Target Storage Blob 6f4b003b0a398c15b1f22a03c612f2c58afa3e7d. Session P created six role-separated review-input artifacts and an A-style integration readiness assessment on P branch only; these are coordinator simulations, NOT independent Owner decisions. D/I/G/H simulated NEEDS REVISION; F/E simulated ACCEPT WITH ENUMERATED CONDITIONS. Require exact Owner artifacts on their own branches, D/I semantic closure, F/E/G local lifecycle/release, H schemas + I security profile, Storage revised bundle and A formal integration. Issue #4 governance and JF-10 P0 remain separate. |

## 7. Current issue trackers

| Issue | Scope | Current state |
|---|---|---|
| #11 | A–I module baseline rollout | Open; proposals remain PROPOSED; owner decisions and baseline adoption tracked separately. |
| #14 | A COC persistence review R1–R6 | Open; P exact-version audit finds R1/R4 substantially addressed in proposal; R2/R3/R5/R6 remain conditional/blocked; independent I/D/C/H decisions still required. |
| #15 | Current COC protocol 86ff3... focused review | Open; A/H/I role reviews are coordinator-simulated; no independent exact acceptance. |
| #16 | Storage Design v2 4ed423... exact review | Open; A/I/H role reviews are coordinator-simulated; D/C exact-v2 decisions absent; P audit identifies R2/R3/R5/R6 and companion pin/schema gaps. |
| #17 | Prepared GID / JF-10 / signed wire envelope | Open; A conditional with amendments; H/I no approval in role-simulated reviews; independent decisions required. |
| #20 | Archive × Forget × Inventory × Restore exact-version owner review | Open; six P role-review inputs and provisional A integration assessment published, but independent D/I/F/E/G/H decisions remain NONE; A formal integration decision NOT ISSUED.

## 8. Required operating sequence

1. Storage reconciles the normative relationship between protocol 86ff3... and Storage Design v2 4ed423..., updates readiness §26.2 and its self-review, and preserves exact immutable pins.
2. B/E/G provide targeted type, producer and Applied-consumption review; H updates strict schema/nominal fields; I defines the security trust profile; D/C verify owner-local gate/provider semantics.
3. A publishes a canonical Gate B manifest and updates its COC/context decision registers, closure tracker and final system review.
4. I/D/C/H publish independent Issue #14 R1–R6 decisions; A integrates them. Role-simulated reviews do not close this gate.
5. F/G update their own baseline proposals and close the exact joint Recall contract; F advances from model to runtime fault tests.
6. I obtains authorized governance decisions for I36-GOV-01..10 and real Global Forget inventory/target evidence.
7. Only after exact Owner decisions, formal governance authority and required engineering evidence may any project freeze or production activation be considered.

## 9. Non-claims

- No final database product selection is inferred from PostgreSQL 18.7 capability tests.
- No COC/Raft service, production DB adapter, I sequencer, D ledger, F runtime archive, G Applied validator, H production parser/SDK or C provider integration is claimed implemented.
- No global Forget completion, physical erasure, backup purge, external recipient deletion or legal/privacy approval is claimed.
- No Gate C implementation/fault-injection PASS is claimed.
- No module baseline is APPROVED; no G0/PGA ratification; no architecture freeze; no production activation.
- No A–I branch or main merge has been performed by Session P.

## 10. Change log

- 2026-11-17: Reconciled live A–I/Storage branches, exact COC/Applied/context decisions, TAB-001 report coverage, F/H/I model/schema tests and current issue #14–#17 status. Closed UMR-024 at design-decision level; all other active blockers remain tracked above.
- 2026-11-17: Added UMR-029 and pinned Session P exact-version audit of Storage v2 R1–R6. Re-fetched current companion protocol Blob 8ac178... and identified mismatch with v2 header's 86ff3... pin; no Owner acceptance inferred.
- 2026-11-17: Added UMR-030 and six role-separated coordinator review inputs plus provisional A integration assessment for Issue #20 exact Blob 6f4b003b...; all are explicitly non-Owner decisions.


- 2026-11-17: Added Issue #20 Owner Remediation Execution Pack (coordinator proposal), exact review target Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`, P commit `ee661045f5820e9029ad19f2dba4f558dcb0682d`, file Blob `6ac0d9296747491b815d531acfe06f7a974eb6ca`. It converts simulated findings into bounded D/I/F/E/G/H/Storage/A deliverables; no Owner decisions or implementation are inferred.
