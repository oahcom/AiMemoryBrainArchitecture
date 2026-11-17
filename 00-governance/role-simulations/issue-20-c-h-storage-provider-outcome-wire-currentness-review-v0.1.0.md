# Issue #20 — C/H/Storage Provider Outcome Wire Currentness Review v0.1.0
# Issue #20 — C/H/Storage Provider Outcome Wire 当前性审查 v0.1.0

- Status / 状态: **PROPOSED / COORDINATOR CROSS-REVIEW ONLY**
- Scope / 范围: CSubmitOutcome 1.0.1, BMCP Unified 1.2.12, RecoveryJoin 1.0.2, C/H candidate validators, Storage v3.2.4 successor bundle.
- Provenance / 来源: Session P simulated C, H, Storage and A review perspectives; this is not an independent Owner signature or a Storage successor manifest.
- Decision / 结论: **CANDIDATE SEMANTICS ACCEPTABLE; EXACT-VERSION BUNDLE NOT CURRENT / NOT FREEZE-ELIGIBLE.**

## 1. Current exact source inventory / 当前精确源清单

Observed branch heads at this review:
- C: `session-c-agent-integration-2026-11-16` — `6d9f312bcedf1a09a80a23226a47ea83927e5975`
- H: `session-h-bmcp-protocol` — `26462ada1dcf3b0405accbbf01a3084e497bd77a`
- Storage: `session-storage-consistency-forget-atomicity-2026-11-16` — `2b345da79fa13ae82f45b053bfcf43344bb26893`

| Authority | Exact current artifact | Blob / evidence |
|---|---|---|
| C semantic Provider Outcome contract | `phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` |
| C Provider Outcome wire amendment | `phase-3.8.10-c-submit-outcome-unified-1.2.12-recoveryjoin-1.0.2-wire-amendment.md` | `b1124441d14f75c82e884a57590581b6813d21fe` |
| C 1.0.1 sequence namespace amendment | `phase-3.11.1-c-submit-outcome-1.0.1-sequence-namespace-amendment.md` | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` |
| C immutable object schema | `c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C 1.0.1 fixture pack | `c_submit_outcome_1_0_1_vectors.json` | `c447f8c2908469c52cb52a448101495a331277c5` |
| C 1.0.1 test harness | `test_c_submit_outcome_1_0_1.py` | `0357c7fc22c714ce50ed4ce4771510431f2b1637` |
| H Unified 1.2.12 current schema file | `bmcp.coc-jf10-unified-1.2.12.schema.json` | `9aa366d857d0229687df7e44e8e70d2097a99237` |
| H RecoveryJoin 1.0.2 schema | `bmcp.recovery-join-1.0.2.schema.json` | `4b664e3bce465499bcdfd93796349a4ba7074002` |
| H exact C 1.0.1 mapping | `phase-3.8.7-h-schema-1.2.12-c-provider-outcome-1.0.1-exact-mapping.md` | `fad28f1b62f6a686669e209ebe30d69df6330d75` |
| H validator core | `provider_outcome_validator.py` | `1a92c0cf7146e2884bd38232005dd9a55d558a85` |
| H validator tests | `test_provider_outcome_validator.py` | `a90b5c4042581b3962e36e0728983bfce441bdd1` |
| Storage v3.2.4 successor exact-version manifest | `phase-3.6.14-storage-v3.2.4-successor-exact-version-binding-manifest.md` | `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7` |
| Storage C Provider Outcome boundary review | `phase-3.8.4-storage-c-provider-outcome-boundary-review.md` | `a99d9df1e14f990f0d4ccd47d48d008b9d9c01fe` |

## 2. Material exact-version mismatches / 重要精确版本失配

### Finding CHS-01 — Storage successor manifest is stale for C and H

Storage manifest Blob `6fc0bed...` currently binds:
- CSubmitOutcome **1.0.0** schema Blob `b5e87fa...`;
- H Unified **1.2.12** schema Blob `a54f669...`;
- H RecoveryJoin 1.0.2 Blob `4b664e3...`.

But the current C source composition has an explicit 1.0.1 immutable successor:
- C 1.0.1 schema Blob `a631bc7...`;
- C sequence namespace amendment Blob `6fa67af...`;
- C 1.0.1 fixture/test blobs `c447f8c...` / `0357c7f...`.

The current H Unified 1.2.12 file is Blob `9aa366d...`, not `a54f669...`. H commit `c2dffd0ce80774c80310295c77806886517e6435` changed the schema description from claiming artifact revision 1.2.11 to correctly stating 1.2.12. The artifact path and declared revision remain 1.2.12, but its immutable Blob changed. The prior exact pin therefore no longer identifies the current file. No prior review automatically transfers to the new Blob.

**Required:** Storage Owner must publish a new successor exact-version manifest (or a clearly versioned successor amendment) binding C 1.0.1, H Unified current Blob `9aa366d...`, H RecoveryJoin 1.0.2 Blob `4b664e3...`, H mapping Blob `fad28f1...`, C amendment Blob `6fa67af...`, and all applicable Storage/C/H/I/D/A sources. Do not rewrite v3.2.4 in place.

### Finding CHS-02 — C wire amendment still describes the 1.0.0 object

C Phase 3.8.10 Blob `b112444...` says its wire table maps to CSubmitOutcome 1.0.0 and pins C schema Blob `b5e87fa...`. C Phase 3.11.1 Blob `6fa67af...` explicitly introduces immutable CSubmitOutcome 1.0.1 with required `sequence_namespace_ref`, supersedes 1.0.0 for new records and says H must validate the namespace against the C key-status event ledger and signing sequencer.

H Phase 3.8.7 Blob `fad28f1...` already maps BMCP 1.2.12 to CSubmitOutcome 1.0.1, but its H Unified schema pin is stale (see CHS-01). The C Phase 3.8.10 source should be amended or superseded so that its mapping table, exact C object revision and RecoveryJoin proof mapping cannot be read as authorizing 1.0.0 for new records.

**Required:** C publishes a new immutable amendment explicitly composing C 1.0.1 + H Unified 1.2.12 current exact Blob + RecoveryJoin 1.0.2. H independently confirms the updated mapping. Keep 1.0.0 as historical only.

### Finding CHS-03 — H mapping document has an old H schema Blob pin

Current H mapping Blob `fad28f1...` identifies C object schema 1.0.1 correctly, but its front matter still pins H Unified 1.2.12 Blob `a54f669...`. The current H schema file is Blob `9aa366d...`. The H mapping document itself was updated to a new Blob, but its embedded exact source pin was not refreshed.

**Required:** H issues a new immutable mapping revision pinning `9aa366d...` or a newly versioned schema successor if H chooses not to treat the changed content as the same artifact revision. H must also confirm the exact schema artifact revision / wire-family version fields in the mapping and validator.

### Finding CHS-04 — RecoveryJoin artifact revision versus schema_version must be explicit

RecoveryJoin file name, `$id` and title identify artifact 1.0.2, while its `schema_version` property is `const 1.0.0`. This may intentionally distinguish immutable artifact revision from a stable wire-family version, but unlike Unified 1.2.12 the RecoveryJoin contract does not clearly state that distinction in the schema envelope.

**Required:** H documents whether `schema_version=1.0.0` is the protocol-family version and where artifact revision 1.0.2 is authenticated/selected. Do not silently change the const without checking existing consumers.

## 3. Semantic cross-owner review / 跨 Owner 语义复审

### C perspective
C remains sole authority for provider handoff truth. Its five outcomes remain distinct:
- `HANDOFF_ACCEPTED`: exact request handoff accepted; not model completion or Storage visibility.
- `HANDOFF_REJECTED`: rejection does not by itself prove no side effect.
- `NOT_INVOKED`: requires positive durable no-handoff proof.
- `UNKNOWN` / `IN_DOUBT`: nonterminal; preserve exact attempt, request digest and provider key; no retry-as-new-operation.

C egress gate close and physical transport handoff must share one durable serialization point. Every physical send is attempt-bound; same-key reconciliation is not a new send. Provider capability/lookup guarantees remain provider-specific.

### H perspective
H validates exact BMCP envelope, dereferenced immutable C object, digest, schema/profile, signature/key status, duplicated-field equality, owner ledger membership and external I/D/COC/Storage joins. H schema validity or a C signature alone cannot establish provider truth or owner-ledger completeness. Missing verifier, key-status or owner callback is UNKNOWN, not VALID.

### Storage perspective
Storage review Blob `a99d9df...` accepts C Blob `8197050...` only as the C-owned Provider Outcome semantic source for the Storage/C authority join. Storage `StorageVisibilityOutcome` remains separate from C provider handoff outcome:
- C `HANDOFF_ACCEPTED` does not imply Storage `COMMITTED_VISIBLE`;
- Storage `COMMITTED_VISIBLE` does not prove provider acceptance;
- either side UNKNOWN keeps the relevant cross-owner participant unresolved;
- COC commit proves record ordering, not provider truth.

### A integration perspective
Candidate semantics compose without merging authorities, but the exact source/consumer bundle is not current and not fully re-pinned. A must review only after Storage, C and H publish successor exact artifacts and I/D confirm any affected membership/signature projections. No freeze.

## 4. Executed candidate evidence / 已执行候选证据

| Suite | Exact run / commit | Result | Boundary |
|---|---|---|---|
| C Provider Outcome 1.0.1 | Run `44059935858`, commit `b49966361b4b3121a2ebf4105b4e0c57a612e945` | **19 tests PASS** | Exact C 1.0.1 schema/test/vector blobs match the current C branch; structural/semantic vectors and test-only candidate crypto interoperability. No provider adapter, real gate race, provider lookup or registered trust profile. |
| H Provider Outcome validator | Run `44060704553`, commit `8c377a7218b70621d2348b47341d4cf4755b3733` | **17 tests PASS** | Validator/test blobs `1a92c0c...` / `a90b5c4...` remain byte-identical at current H head. Candidate schema/digest/crypto and local fail-closed semantic checks; injected authority callbacks are not production-connected. |
| H Recovery Cutoff / wire suite | Run `44062391968`, commit `26462ada1dcf3b0405accbbf01a3084e497bd77a` | **288 total: 266 pass, 22 skipped, 0 failed** | Bounded H candidate semantic/wire tests; 22 skips are superseded 1.2.10 fixtures. Not production COC quorum or owner verifier proof. |
| H schema validation | Run `44062392943`, commit `26462ada1dcf3b0405accbbf01a3084e497bd77a` | **47 tests PASS** | Candidate BMCP JF-10 / Storage proof schema validation only. |

These results are useful candidate evidence, not Owner acceptance, production adapter evidence or architecture freeze. The C profile `AIMBA-C-CRYPTO-1.0` remains NOT REGISTERED; I-governed trust root, key lifecycle and anti-rollback remain open.

## 5. Required next sequence / 必须的后续顺序

1. **C:** publish a new immutable C wire amendment composing CSubmitOutcome 1.0.1 with the exact current H Unified 1.2.12 and RecoveryJoin 1.0.2 artifacts; preserve 1.0.0 as historical.
2. **H:** publish a new exact mapping revision pinning the exact current H schema Blob and C 1.0.1 object; resolve RecoveryJoin artifact-revision vs wire-version declaration.
3. **Storage:** publish a new successor exact-version manifest (v3.2.5 or explicitly named successor) binding all exact C/H/I/D/Storage sources and the H mapping; do not edit v3.2.4 in place.
4. **I/D:** independently confirm that C 1.0.1 sequence namespace and RecoveryJoin 1.0.2 membership-proof mapping preserve their owner-owned P0, key-status, high-water, snapshot and anti-rollback authority.
5. **C/H/Storage:** re-run cross-owner exact Blob review after the successor manifest exists. Record any conditional acceptance only against that exact manifest.
6. **A:** perform the final integration review of the same manifest and exact Owner decisions. Freeze remains NOT APPROVED until all authority and implementation gates close.

## 6. Non-claims / 非声明

This review does not approve or claim:
- production C egress adapter, provider-specific same-key lookup or exactly-once side effects;
- durable C sequencer, append-only C outcome ledger or real owner snapshot membership;
- I profile registration, production key custody/rotation/revocation or anti-rollback checkpoint;
- H production authority callbacks, COC quorum persistence or generated SDK interoperability;
- Storage deployed topology, database transaction serialization, physical restore/visibility proof;
- production Global Forget completion, architecture freeze or activation.

本审查不批准或声称生产 C Egress Adapter、Provider 幂等查询、Exactly-once 副作用、C Durable Sequencer/Ledger、生产 I Key/Trust、H Authority Callback、COC Quorum、Storage 部署拓扑、数据库事务线性化、物理 Restore/Visibility、Global Forget Completion、架构冻结或生产激活。
