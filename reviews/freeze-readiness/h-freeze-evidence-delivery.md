# H — Freeze-Readiness Evidence Delivery / 冻结前证据交付

- Role / Owner: H — BMCP Protocol Architect
- Delivery stage: **STRUCTURAL SCHEMA + REFERENCE PARSER EVIDENCE DELIVERED**
- Freeze disposition: **BLOCKED — NOT FROZEN / NOT INTEROPERABILITY-VERIFIED**
- Snapshot branch: `session-h-bmcp-protocol`
- Snapshot HEAD: `1c6ddd301d538652ceea22ea665d50c5fad8178e`
- Owner technology review Blob: `cb9d1d97604bdb71bc2f5bf47f6392e03f30ba99`
- Provenance: assistant-authored delegated H-role delivery at the user's direction; not an independent human Owner signature.

## 1. Executive disposition / 执行结论

H has delivered structural schemas and reference-parser evidence, including a recorded 23/23 CI pass for the JF-10 bridge schema plus strict parser reference suite. Recovery Cutoff 1.0.5 and unified COC/JF-10 schema artifacts are available as candidates.

The exact-version decision reviewed for the unified schema is v1.2.4, while the current branch contains a newer schema artifact v1.2.6. The v1.2.6 artifact's description says its on-wire family `schema_version` remains 1.2.0. No exact H decision for v1.2.6 was located in the reviewed bundle. Therefore the latest schema artifact must not silently inherit the v1.2.4 acceptance.

H 已交付结构化 Schema 与参考解析器证据，包括 JF-10 Bridge Schema + Strict Parser 参考套件 23/23 CI 通过记录。Recovery Cutoff 1.0.5 与统一 COC/JF-10 Schema 均已有候选版本。

但统一 Schema 的精确版本决议审查对象是 v1.2.4，而当前分支已存在更新的 v1.2.6 Schema Artifact。v1.2.6 的描述明确指出线上协议族 `schema_version` 仍为 1.2.0。当前证据中未找到对 v1.2.6 的 H 精确版本决议，因此不得把 v1.2.4 的接受自动继承到 v1.2.6。

## 2. Exact evidence register / 精确证据清单

| Evidence | Exact Blob / Run | Result and scope |
|---|---|---|
| JF-10 bridge schema validation evidence | `318c433d5b96966ecd47e6d1b265a0b12b28e581` | 11/11 structural tests PASS; run 43962364955 |
| Strict parser reference evidence | `d974ee1b166af4a94ab8ad7601744f40f32f98c6` | 23/23 combined schema/fixture + strict parser tests PASS; run [43963209651](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43963209651), job 133635778980, test commit `a81c5c374ad20ac702a962418b50f65c6a16bb2c` |
| Recovery Cutoff 1.0.5 schema | `3d451778b9867c3b54779c5cd478522993719025` | Structural candidate; semantic completeness/order require validators |
| Unified COC/JF-10 schema artifact 1.2.6 | `ea8d644df17ea88ed368980b7d5930cd33934fd2` | Current branch artifact; no exact H approval for this artifact revision located |
| H exact review of Recovery Cutoff 1.0.5 | `86ee608007a4f9432eda8143e2a830afd3eece0c` | ACCEPT WITH ENUMERATED AMENDMENTS; NOT FROZEN / NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED |
| H exact review of unified schema 1.2.4 | `3aa617cd7066405d84a5bd027eaaad1f9c3bc9bc` | ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS; exact v1.2.4 only |
| H Batch/Manifest validator addendum | `c216853412f654d92e2890ddcc2dffc12406cbe6` | Proposed wire/semantic validator amendment; vectors specified, not run |
| H Recovery Cutoff semantic contract | `b4cae9c0c9121c27ea2933c029b83b3f4367672b` | Proposed contract; complete owner-local request/admission accounting required |

## 3. Protocol invariants / 协议不变量

1. Batch and Manifest are two quorum-committed records, not one synthetic record. Manifest content is precomputed; Batch binds its content digest; final Manifest record back-references the exact committed Batch. Required digest dependency: ContentDigest → BatchDigest → ManifestRecordDigest.
2. A Manifest record committed before Batch is invalid. A crash between Batch and Manifest leaves a fenced incomplete pair; recovery resumes exact stable IDs/digests or remains RESTORE_FENCED.
3. Owner request sets and owner admission sets remain distinct. I/D/C owner-local high-waters and COC participant prefix are not collapsed into one list or synthetic global counter.
4. COMPLETE_EMPTY requires positive authoritative evidence: status, present empty array, count and canonical empty root. Missing/null/unavailable/partial pagination/stale replica/timeout/UNKNOWN are not empty.
5. Every participant must join its exact owner admission. Storage entries must join the exact JF-10 prepared participant tuple. Cross-owner numeric counters are never compared.
6. H owns wire representation and validators; C owns provider outcome truth; I owns trust and authorization; D owns Forget/fence semantics; Storage owns prepared participant and visibility outcome.
7. Provider outcome is not inferable from Batch, Manifest membership, Storage resolution, I terminality, D clearance, COC commit or H transport ACK.

## 4. What the evidence does not prove / 证据边界

- The 23/23 run covers the JF-10 1.1.0 bridge schema and strict parser reference suite at its recorded commit. It does not validate the newer unified 1.2.6 schema or Recovery Cutoff 1.0.5 semantic behavior.
- JSON Schema does not prove quorum commitment, owner signatures, complete source enumeration, digest preimage equality, Batch-before-Manifest log order, bidirectional joins or provider truth.
- H 3.6.12 exact review explicitly leaves required vectors SPECIFIED / NOT RUN: canonical digest fixtures across independent implementations, Batch/Manifest ordering/replay, complete pagination, owner roots/high-waters, provider outcome schema, downgrade/duplicate-key/unknown-critical/wrong-audience rejection.
- Canonical byte profile, Unicode/number/time normalization, absent/null semantics, cryptographic signature profile, key lifecycle, generated SDK and cross-language interoperability remain OPEN.
- Unified schema v1.2.6 has no exact-version H decision in this delivery snapshot. It is not approved by v1.2.4 review.

## 5. Latest HRC / RecoveryJoin executable candidate — exact current pins

The latest H branch and A cross-owner review identify the following exact candidate bundle:

| Artifact | Blob SHA | Scope |
|---|---|---|
| RecoveryJoin schema 1.0.0 | `dd3234aa1c74caf6d0e335875cd96e0b2b64082f` | Typed bidirectional owner/participant edges and row identity |
| H semantic validator contract | `b3218298f58cff9b92cb1c38e453af6fd4d0dd50` | HRC/JPF/WIRE/SCHEMA execution contract |
| HRC semantic suite | `60a2f4db4bd12f2131ecd147db9bbe328da6db50` | 25 HRC + 19 JPF = 44 methods (JPF-08 fixture corrected) |
| Wire interop candidate suite | `1a4e754ba9bfa57eb973c6d39731e9f89443b323` | 10 methods |
| Schema integrity candidate suite | `67aba74c120f2916d768e7b01c45408ee2624f3a` | 12 methods |
| CI workflow | `.github/workflows/h-recovery-cutoff-conformance.yml`, Blob `ea7a3d9c365b84352d3bac69da94fe0d510e46a4` | Runs all `test_*.py` under `08-bmcp-protocol/tests/conformance/recovery_cutoff` |

**Total: 66 unittest methods specified in the current candidate code (25 HRC + 19 JPF + 10 WIRE + 12 SCHEMA).**

- First exact candidate run [44039825581](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44039825581) exposed one failure: JPF-08 returned UNKNOWN before reaching its intended duplicate-primary-admission assertion because the fixture also required absent I/D evidence.
- H corrected the fixture to isolate the C primary-admission invariant (the test does not weaken production validation): test file Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`.
- Rerun [44039990464](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44039990464), exact test commit `da94bcc1796cb350eed12845e49cbc3663faab9c`, job `133891944149`: **66 tests PASS**.
- This is a reference-model/schema/wire-candidate CI pass only. It does not exercise live owner ledgers, quorum COC, I cryptographic trust, C provider adapter, D fence CAS, Storage physical visibility transaction or multi-language independent implementation.



The HRC/WIRE candidate uses TEST-ONLY canonical digest helpers. It is not an approved production canonicalization, signature, key-trust or cross-language byte profile. Passing this candidate suite cannot by itself close H-FR-04/H-FR-06 or I-RJ-05.

## 6. Freeze exit criteria / 冻结退出条件

| ID | Required evidence | Current status |
|---|---|---|
| H-FR-01 | Exact H review/decision for schema artifact 1.2.6 and its on-wire version mapping | OPEN |
| H-FR-02 | Dedicated versioned CSubmitOutcome schema/message family, accepted by both H and C | OPEN |
| H-FR-03 | Executable semantic validators for completeness, roots/counts, owner joins, digest projection and Batch/Manifest ordering | OPEN |
| H-FR-04 | At least two independent implementations produce identical canonical digest/signature preimages | OPEN |
| H-FR-05 | Negative tests: duplicate keys, downgrade, absent/null, unknown critical, wrong audience, replay and stale generation | OPEN |
| H-FR-06 | Transport/SDK interoperability and cryptographic verification against I-approved trust profile | OPEN |
| H-FR-07 | Exact H/I/C/Storage/A acceptance of one immutable integrated bundle | OPEN |

## 7. H final delivery statement / H 最终交付声明

**Delivered:** schema artifacts, structural bridge validation and strict parser reference evidence, plus exact-version design dispositions.

**Not delivered:** full semantic validator conformance, v1.2.6 exact approval, provider-outcome wire freeze, cryptographic/canonical-byte interoperability or production SDK/transport acceptance.

**Decision:** H documentary/structural evidence delivery is complete for this stage. H freeze-readiness remains **BLOCKED** until H-FR-01 through H-FR-07 are satisfied.

## 8. Latest CI confirmation / 最新 CI 再确认

The current H branch snapshot was re-executed by [run 44040312711](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040312711), job `133893012456`, checking out H branch commit `e53d9b8a5fc9f4a77fb3ece8b3c3540b20698d1c`. The raw job log reports **66 tests, OK**. The test source remains HRC/JPF Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`, WIRE Blob `1a4e754ba9bfa57eb973c6d39731e9f89443b323`, SCHEMA Blob `67aba74c120f2916d768e7b01c45408ee2624f3a`. This is a repeatable candidate-suite PASS only; production wire/crypto, independent language interoperability, live owner/COC adapters and physical JF-10 remain OPEN.


## 8. Current 66-test CI execution refresh / 当前 66 项 CI 执行刷新

The current exact H candidate bundle remains:
- RecoveryJoin schema 1.0.0: `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- H semantic validator contract: `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`.
- HRC/JPF suite: `60a2f4db4bd12f2131ecd147db9bbe328da6db50` — 25 HRC + 19 JPF.
- Wire suite: `1a4e754ba9bfa57eb973c6d39731e9f89443b323` — 10.
- Schema integrity suite: `67aba74c120f2916d768e7b01c45408ee2624f3a` — 12.
- Workflow: `.github/workflows/h-recovery-cutoff-conformance.yml`, Blob `ea7a3d9c365b84352d3bac69da94fe0d510e46a4`.

Latest run [44040502709](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040502709), commit `1c6ddd301d538652ceea22ea665d50c5fad8178e`, job `semantic-and-wire-tests`: **66 tests ran, OK**. This supersedes earlier 61/56-method inventories and the previous successful run 44039990464 as the latest recorded H candidate CI evidence.

This result is limited to the checked-in Python reference semantic, wire-negative and schema-integrity candidate tests. It does not close H-FR-01/02/04/06/07: exact schema 1.2.6 approval, CSubmitOutcome schema acceptance, two independent production canonical-byte/signature implementations, I-approved cryptographic trust, SDK/transport interoperability and one immutable integrated H/I/C/D/Storage/A bundle remain OPEN. H freeze remains **BLOCKED — NOT FROZEN / NOT INTEROPERABILITY-VERIFIED**.
