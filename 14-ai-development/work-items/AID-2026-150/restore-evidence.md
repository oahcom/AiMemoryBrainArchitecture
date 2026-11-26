---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Work-item evidence; facts pinned to repository observations; no Owner acceptance or natural-person signature asserted."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Evidence for restoring exactly three D Memory Brain normative roots, classifying 57 deferred paths and 11 orphan mirror pairs"
    canonical_scope_id: "ai-development/aid-2026-150-d-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-150"
      - "memory-brain"
      - "normative-root"
      - "blob-comparison"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-150/restore-evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-150/restore-evidence.md"
---
# AID-2026-150 — D Memory Brain normative-root restoration evidence

## Scope and attribution

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Main baseline: `248cef62410cb4a412efb2d83326a1ce32345765`
- Main tree: `f14c234f98b5fa046c2f84bbbe7b5f7dd29b1945`
- D source branch: `session-d-memory-brain-2026-11-16`
- D source branch HEAD: `b525e1f8fee2471a131e4a38efda99804045e424`
- D source tree (Git tree object): `258f53ab74a6618493a15e6a0d190467997bec43`
- Work item: `AID-2026-150`; fixed account range `AID-2026-150..159`; selected `AID-2026-150` after no matching Issue/PR carrier was found.
- Attribution: user-authorized operator (delegated by account owner); no natural-person Owner signature is represented.
- This is source-presence restoration and path classification only. It does not grant Owner acceptance, normative approval, implementation authorization or production conformance.

## 1. Three canonical root blob comparisons

| Canonical path | Source blob SHA | Restored main-branch blob SHA | Body handling |
|---|---|---|---|
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `df07e7cc85ad68d35609f3499bd69ca7fc44d9c2` | `FRONTMATTER_ADDED`; source body preserved byte-for-byte |
| `03-memory-brain/commit-cursor-semantics.md` | `4688a0ca487bf4d853c7f0220408abe8d743d159` | `2c68161d039310b8df0e1387b4f1111ed74699db` | `FRONTMATTER_ADDED`; source body preserved byte-for-byte |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `dd26e3cae2e60dbdc44a6e084004effcd2033efa` | `FRONTMATTER_ADDED`; source body preserved byte-for-byte; EN/ZH-CN stub pair structurally registered |

Each source blob had no GOV-DOC-002 frontmatter. The three restored files prepend valid metadata and then contain the original source body unchanged. Exact in-memory comparison after removing the added frontmatter returned `true` for all three. The new blob SHA therefore differs from the source blob SHA by design.

Lifecycle boundary for all three: `decision_status: Draft`; `normative_status: Informative`. `canonical_status: Canonical` identifies the restored repository source path only; it is not an Owner approval.

## 2. Existing EN/ZH-CN mirror treatment

The two non-conflicted pairs (Canonical Memory Store and Commit Cursor Semantics) were retained. Only GOV-DOC-002 metadata and three-way counterpart references were added; each existing mirror body was byte-for-byte unchanged.

| Mirror | Previous blob SHA | New blob SHA | Body |
|---|---|---|---|
| EN canonical store | `414fe03fd40fb8ad46061d2d8c7d29ba2667f252` | `416bb38b961c6f5628857be23d12f7a475652a19` | unchanged |
| ZH-CN canonical store | `34e0755a079f085df65c2a180cc59b6aaea7ea78` | `ea16b0c0527b63b1de35f76842d3d49866353dee` | unchanged |
| EN cursor semantics | `2de7fe35229372ae5b06093e5e031c2c243fbd7c` | `4199bc66e4fc81fc460237c8bd65817f6c2288f2` | unchanged |
| ZH-CN cursor semantics | `2589cecb258e029c5a18796d019ad5b9806cfbdc` | `bf9529b97ba65c2eacb627f4f5939bfb359c0006` | unchanged |
| EN Fence navigation stub | `9c054932994bb078e2834df8bd66f73895aa04f5` | `5f3334322170c447868b2d20b4b55728f7a8dc35` | metadata + source-status/path correction; still a non-canonical navigation stub |
| ZH-CN Fence navigation stub | `15c60b9a72632975f89e507520eaf32a0b9e603d` | `5f8c8f9d4d61e4181fc7410165a24056f9127a01` | metadata + source-status/path correction; still a non-canonical navigation stub |

The EN and ZH-CN files retain their existing section structures and typed-contract vocabulary. This is a bounded structural correspondence check, not a certified line-by-line translation review. No mirror body was rewritten.

## 3. Fence conflict determination

The original D source blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` is a complete 74,846-character document titled “Forget Fence Atomicity, Producer Admission and Publication Gate”.

The current EN/ ZH-CN file with the same basename is not that document:
- EN navigation/dereference stub: 1,910 characters, old blob `9c054932994bb078e2834df8bd66f73895aa04f5`.
- ZH-CN navigation/dereference stub: 1,224 characters, old blob `15c60b9a72632975f89e507520eaf32a0b9e603d`.
- Both explicitly say the historical source blob is retained but no current normative source path exists, and link to four split parts.
- EN split parts have 21,284 + 12,040 + 30,973 + 12,818 = 77,115 characters in aggregate. The parts contain separately versioned Phase 3.6 / JF-10 additions and are not a byte-preserving partition of the 74,846-character source blob. Their aggregate length alone is not proof of semantic equivalence.

**Disposition:** restore the exact original source body at the canonical root path. Do not replace it with the short dereference stub, and do not concatenate Parts 1–4 into a synthetic replacement. The EN/ZH-CN navigation stub pair receives GOV-DOC-002 metadata and a small source-status/path correction pointing to the restored root; it remains a non-canonical navigation page, not a full translation. The stub pair and four split-part EN/ZH-CN pairs remain `ORPHAN_MIRROR_PENDING_DECISION` pending Owner semantic disposition. Root source selection is resolved and the root metadata uses `canonical_conflict_status: None`. No README is created or modified.

## 4. The other 57 D source paths — none restored

The following 57 paths are the exact remaining D-branch blobs from the AID-2026-107 §10.4 per-file inventory. Classification is preserved verbatim: 29 `HISTORICAL_PHASE_RECORD`, 28 `UNDECIDED`. None is copied into main.

| D source path | Source blob SHA | Classification |
|---|---|---|
| `03-memory-brain/d-forget-normative-index-proposal.md` | `5d1000d93217012d52a5b44c8f6b4343c42f0397` | `UNDECIDED` |
| `03-memory-brain/decision-change-log.md` | `8e8380b8c179ca5176c510a13d496e0197e565b9` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/entity-and-relationship-manager.md` | `14697658d4d873381ca8d4e3bed7c1170368ec29` | `UNDECIDED` |
| `03-memory-brain/forget-fence-and-completion-contract.md` | `1f0391bc49d007c44ec74165bd33d37412cc7990` | `UNDECIDED` |
| `03-memory-brain/gate-release-currentness-cas-and-producer-admission.md` | `7f2861d9441b9be6c8e69f41fd0276636be483a8` | `UNDECIDED` |
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `UNDECIDED` |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | `UNDECIDED` |
| `03-memory-brain/memory-versioning.md` | `af747f339d03bdd4684b6ed60fca05957dc8e1fb` | `UNDECIDED` |
| `03-memory-brain/module-baseline-and-redlines.md` | `84e402f471d452c7dab63a7db344f86b5b57bd7c` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-cgh-applied-1.0-d-forget-fence-authority-confirmation.md` | `b5a0354d263185723954ffb952fdf0b005f59ba8` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` | `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-joint-forget-linearization-decision.md` | `1b6a312ecffd3947bbb4df59f902242482c98a40` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-r1-r2-d-owner-gate-linearization-decision-candidate.md` | `a7cba2c72720bb7873d77f1a9d151df974605a9e` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.1-joint-defect-closure-d-addendum.md` | `53685b864fbbcbac010e60a67c59430be7f27fce` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.10-d-exact-version-recovery-cutoff-review.md` | `e03ca0db209fc8ac5b985e114a31c21fbb136859` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.14-d-exact-review-storage-v3.2.4-successor-manifest.md` | `55ffb6da64023b5f2c7a3d1a8d6bb562de70ab25` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.2-jf10-reference-model-consumption.md` | `a3555162827bd1cc7cf4c0918d4ab9b6ce94c8bb` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.3-d-coc-durable-protocol-acceptance.md` | `e2a74d138ccebfb4266d19ea0c0c03f58a815bf5` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.4-d-prepared-participant-gid-fence-acceptance.md` | `3cba777f8951a5d88e27a314a37c000aeedc19d0` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.5-d-restore-control-highwater-acceptance.md` | `211e54acfb4573b1c51d96f07af297671dfc4c4b` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.6-d-forget-semantic-authority-addendum.md` | `a384ffb4fff7de9b35ba6b3011d2779ad529573d` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.7-d-exact-version-owner-decision.md` | `3603aff5881dd8a375f22aad67b90ade312bbfad` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.7-d-owner-local-gate-admission-release-amendment.md` | `84f6875ce382fb37f35b01140c19a482fcfa9fab` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md` | `2d95099a2e19a8cbec325925b70da576f73d9899` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.8-d-exact-version-owner-rereview-decision.md` | `35fa09e9bd5d15e6ad092c0c0ace52ca02a48692` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.8-d-exact-version-r1-r4-rereview-decision.md` | `5aafe8a977ec0cfa1287e7af8c47c8f67ee3a501` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.9-d-r1-r2-exact-version-delegated-disposition.md` | `7ab4f53c497bce597e422a6df9a85b31a2352602` | `UNDECIDED` |
| `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` | `4c01713bc8793a8926ef18b625b72d132572173d` | `UNDECIDED` |
| `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` | `UNDECIDED` |
| `03-memory-brain/phase-3.8.10-d-review-h-full-path-forget-clearance-callback.md` | `fd576d05a6dbf18ce4920b6a1ce44b957f9f1850` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.11-d-exact-review-h-expanded-full-path-fence-storage-callbacks.md` | `7a9ed2bcf7fd34edc576a4a1be7f4388ee551b43` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.11-d-review-h-expanded-full-path-fence-clearance.md` | `1ce8f25db1971b692112e47aeae431af4e69b5e5` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.12-d-exact-rereview-h-c-p0-projection-test-39-method-ci.md` | `02b74a14c2c5ad35553b41eb7831b6eadceb0ffa` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.12-d-exact-review-h-42-test-cp0-nullable-intent-currentness-boundary.md` | `2bf4514fe7972b72f6c1f904e461f86488d04cda` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.12-d-review-h-nullable-coc-not-invoked-and-p0-matrix.md` | `8f064d29f4868ad5ad598aa49f12bf7709b9a993` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.13-d-review-h-outer-envelope-authenticated-ingress-gate.md` | `152627e00b96355e2ff370acd643a51168c4c78c` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.14-d-exact-review-h-applied-delivery-evidence-replay-fence.md` | `1ebbf827f92ee9244963a550855283421837a1b0` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.14-d-review-h-explicit-outer-signature-profile-requirement.md` | `4b512ad717296c6f8ab5b074048f2169dd9f6df2` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.2-d-recovery-join-and-visibility-exact-review.md` | `6f39475784458d34b347d8566824fa22b308b477` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.3-d-gate-release-currentness-exact-review.md` | `7d45e663b471b7d82a0af8ca5b2e1f14c88f2315` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.4-d-exact-review-h-owner-membership-proof.md` | `0edd96d07960292d938656d5d8a20095750f4cf1` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.4-d-owner-snapshot-membership-proof-contract.md` | `59ff706470f98617bda12397d8236377c73b067d` | `UNDECIDED` |
| `03-memory-brain/phase-3.8.5-d-exact-review-h-unified-1.2.13-owner-proof-compatibility.md` | `84196906cad92367a60c79a74dd241fd80abb96c` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.5-d-recoveryjoin-1.0.2-unified-1.2.12-wire-adoption-amendment.md` | `46b6abd94f3396e5eef7d7456f9b62a3865d4ce2` | `UNDECIDED` |
| `03-memory-brain/phase-3.8.5-d-storage-logical-serialization-topology-review.md` | `7b44f2b3e346eaa34840797bec391465af6130a3` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.6-d-exact-review-unified-1.2.13-recoveryjoin-1.0.2.md` | `1f03f3a83dda3fc1cc364ae9d2d18a3f1b96b590` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.6-d-recoveryjoin-1.0.2-membership-proof-p0-crosswalk.md` | `c4adf827dd62d44c43b8e871dec4835581508adf` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.7-d-exact-review-h-1.2.14-recoveryjoin-1.0.2.md` | `55ae7bc33b37f0e729949fdd2a694eb6211bbc55` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.7-d-exact-review-h-unified-1.2.14-fence-high-water-and-membership.md` | `49d572d4c35cb393009996606f5187eec5c571e5` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.8-d-exact-review-h-unified-1.2.14-current-schema-fence-high-water.md` | `6aca7d020caecf3c69debf614c903bf469583260` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.8-d-review-storage-serialization-anchor.md` | `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.9-d-exact-review-h-authority-join-mapping-1.2.14.md` | `40fee15d7e42d68da231ea161896f85df2921669` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.9-d-review-h-forget-clearance-verifier-seam.md` | `53613f383d064d25ac9f34a00e457f86730f16bf` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.9-d-forget-terminal-semantics-and-linearization-closure-proposal.md` | `9c02b5680317f0092788ad0da66d621338b1c54c` | `UNDECIDED` |
| `03-memory-brain/tests/test_phase_3_9_forget_reference_model.py` | `b712f15bdb3770a3075070f8f3fce573c70defcf` | `UNDECIDED` |

Classification basis:
- `HISTORICAL_PHASE_RECORD`: phase-scoped reviews/re-reviews, reference-model or conformance artifacts, decision/change logs and module baselines retained as process/history evidence, not promoted to independent normative roots.
- `UNDECIDED`: substantive phase decisions/addenda/contracts, subsystem/overview documents, tests or alternatives for which the available evidence does not establish whether they are controlling, superseded or unnecessary. Owner disposition is required before restoration.

## 5. Eleven existing mirror pairs — pending decision, untouched

These 11 filename pairs are not imported as canonical D roots. Both language copies remain unchanged; no README is authored or modified.

| Existing mirror pair | Classification |
|---|---|
| `docs/en/03-memory-brain/README.md` + `docs/zh-CN/03-memory-brain/README.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/entity-and-relationship-manager.md` + `docs/zh-CN/03-memory-brain/entity-and-relationship-manager.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part1.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part1.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part3.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part3.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-brain-guide.md` + `docs/zh-CN/03-memory-brain/memory-brain-guide.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-brain-overview.md` + `docs/zh-CN/03-memory-brain/memory-brain-overview.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-lifecycle-manager.md` + `docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-versioning.md` + `docs/zh-CN/03-memory-brain/memory-versioning.md` | `ORPHAN_MIRROR_PENDING_DECISION` |

No mirror is deleted, concatenated or treated as a canonical source. The Fence navigation stub pair receives only metadata and a source-status/path correction; its semantic status remains pending. The other 10 orphan pairs are unchanged. The `ORPHAN_MIRROR_PENDING_DECISION` label is an inventory disposition, not a claim that the content is invalid.

## 6. Gate and acceptance boundary

- `03-memory-brain` is added to the authoritative `NORMATIVE_ROOTS` list so the three restored canonical documents are covered by the bilingual/document-management gates.
- Existing EN/ZH-CN bodies for the two linked pairs are unchanged; their metadata now points to the root source and sibling mirror.
- The Fence stub pair is structurally linked to the restored root for metadata closure, but remains a non-canonical navigation stub with pending semantic disposition; Parts 1–4 are not linked as mirrors.
- No README, runtime implementation, validator logic, schema, test, workflow, deployment or production artifact is changed. The existing bilingual checker receives only the `NORMATIVE_ROOTS` scope registration for `03-memory-brain`; the independent scope registry receives the matching governed-root entry.
- No Issue is closed by this evidence. Issue #1212 remains open unless the platform state changes independently.
- Independent reviewer: `NOT_ASSIGNED`; Owner acceptance: `NOT_GRANTED`.

PR #1320 is open. The initial PR base advanced after branch creation; the final branch refresh is onto main ac301e09799bcc094e015db4e12d2e6ff53d5010 before final CI/merge. Exact final Head, check results and merge SHA will be recorded in the #1212 post-merge comment.
