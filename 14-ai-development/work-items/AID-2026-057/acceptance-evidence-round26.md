---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "This file is the raw stdout of measure_ab.py and verify_ab_buckets.py, pasted without editing. Both were run against the pre-patch tree at _w58 (v2026-11-24.2) as the inventory definition and the branch head as the candidate predicate. Re-running either script reproduces every line."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-057 — round-26 acceptance evidence

Verbatim output of the two verifiers, captured at `main = 95c1261` with the
candidate inventory defined by the pre-patch predicate (`2026-11-24.2`) over the
pre-patch tree. Kept unedited so a reader can re-derive every number in the PR
body without trusting the prose.

Verifiers:
- `measure_ab.py` — admitted/refused split, regression and over-reach checks.
- `verify_ab_buckets.py` — re-derives the bucket decomposition of the refused set.

## AC8 — measure_ab.py

```
versions: pre=2026-11-24.2  d=2026-11-24.3  ab=2026-11-24.5
inventory (pre-patch refused set) = 113

after D only (v24.3):  admitted 5 / refused 108
after A/B  (v24.5):  admitted 83 / refused 30

=== newly admitted BY A/B, i.e. admitted now but not by D (78) ===
  .governance/GOV-DOC-001-inheritance.json
  00-governance/architecture-document-metadata.schema.yaml
  00-governance/document-scope-registry.yaml
  08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json
  08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json
  08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.0.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.1.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.10.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.11.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.12.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.13.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.14.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.15.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.16.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.17.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.2.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.3.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.4.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.5.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.6.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.7.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.8.schema.json
  08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.9.schema.json
  08-bmcp-protocol/schemas/bmcp.i-owner-snapshot-attestation-1.0.0.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.0.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.1.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.2.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.3.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.4.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.5.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.0.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.1.schema.json
  08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json
  08-bmcp-protocol/schemas/bmcp.storage-prepared-participant-proof-1.0.0.schema.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c-key-status-event-1.0.0.schema.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c-submit-outcome-1.0.0.schema.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c-submit-outcome-1.0.1.schema.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c_crypto_profile_expected_vectors.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c_crypto_profile_expected_vectors_1_0_1.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c_crypto_profile_vector.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c_crypto_profile_vector_1_0_1.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c_submit_outcome_1_0_0_vectors.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/c_submit_outcome_1_0_1_vectors.json
  08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/h-full-provider-outcome-positive-1.0.1.json
  08-bmcp-protocol/tests/conformance/recovery_cutoff/fixtures/invalid_complete_empty_proof.json
  08-bmcp-protocol/tests/conformance/recovery_cutoff/fixtures/invalid_forget_fence_generation.json
  08-bmcp-protocol/tests/conformance/recovery_cutoff/fixtures/invalid_owner_snapshot_membership_proof.json
  08-bmcp-protocol/tests/conformance/recovery_cutoff/fixtures/valid_recovery_join_1_0_2.json
  08-bmcp-protocol/tests/conformance/recovery_cutoff/i_crypto_profile_vector.json
  08-bmcp-protocol/tests/conformance/recovery_cutoff/wire_interop_vectors.json
  14-ai-development/governance-register/evidence/attribution-1491856051.json
  14-ai-development/governance-register/evidence/direct-commit-filesets.json
  14-ai-development/governance-register/evidence/direct-main-commits-p2.json
  14-ai-development/governance-register/evidence/direct-main-commits-p3.json
  14-ai-development/governance-register/evidence/direct-main-commits.json
  14-ai-development/governance-register/evidence/issue-closures.json
  14-ai-development/governance-register/evidence/main-paths.json
  14-ai-development/governance-register/evidence/merge-gate-evidence.json
  14-ai-development/governance-register/evidence/number-domain-scan.json
  14-ai-development/remote-worker-inventory.yaml
  crates/agent-integration/Cargo.toml
  crates/bmcp-protocol/Cargo.toml
  crates/bmcp-server/Cargo.toml
  crates/brain-cli/Cargo.toml
  crates/memory-compiler/Cargo.toml
  crates/memory-compiler/VERIFICATION.txt
  crates/memory-context/Cargo.toml
  crates/memory-context/VERIFICATION.txt
  crates/memory-domain/Cargo.toml
  crates/memory-event-store-sqlite/Cargo.toml
  crates/memory-event-store/Cargo.toml
  crates/memory-storage-sqlite/Cargo.toml
  crates/memory-storage/Cargo.toml
  crates/memory-store/Cargo.toml
  crates/memory-store/VERIFICATION.txt
  scripts/bilingual-baseline.txt
  scripts/ci/baselines/bilingual-docs.txt

=== still admitted 5 from D (must all still be admitted) ===
  OK   08-bmcp-protocol/tests/conformance/package-lock.json
  OK   08-bmcp-protocol/tests/conformance/package.json
  OK   08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt
  OK   14-ai-development/work-items/AID-2026-001/reference-model/.gitignore
  OK   14-ai-development/work-items/AID-2026-003/t2-snapshot-fix-prompt.source.txt

=== STILL REFUSED (30) ===
  08-bmcp-protocol/tests/conformance/recovery_cutoff/test-logs/2026-11-20-full-suite-python312.log
  14-ai-development/work-items/ADOPTION-EVIDENCE-2026-P1/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-GATE-ROOTS-001/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-INDEX-REFRESH-001/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-MANIFEST-YAML-001/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-T1/manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-T3/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-T3/tier-confirmation-proposal.yaml
  14-ai-development/work-items/FIX-2026-P1-T3/tier-mapping-proposal.yaml
  14-ai-development/work-items/FIX-2026-P1-T4-FU1/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-T4-FU2/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-T4-FU3/authorization-manifest.yaml
  14-ai-development/work-items/FIX-2026-P1-T4/authorization-manifest.yaml
  14-ai-development/work-items/P2-T2-MEMORY-SCHEMA/authorization-manifest.yaml
  Cargo.lock
  VERIFICATION.txt
  benchmarks/req02/results-2026-11-20.json
  benchmarks/req10_e2e/dev-fixture-report.json
  crates/bmcp-server/tests/fixtures/invalid_duplicate_key.json
  crates/bmcp-server/tests/fixtures/invalid_missing_field.json
  crates/bmcp-server/tests/fixtures/valid.json
  crates/brain-cli/fixtures/event.json
  recovery/PR-RECOVERY-002-INVENTORY.csv
  reviews/architecture-breakthrough/forget-model/ForgetModel.cfg
  reviews/architecture-breakthrough/forget-model/ForgetModel.tla
  reviews/architecture-breakthrough/memory-ir-compiler/prototype/sample_experiences.json
  reviews/architecture-breakthrough/memory-ir-compiler/prototype/shadow_corpus_24.json
  reviews/req06-evaluation-pilot/corpus.jsonl
  reviews/req06-evaluation-pilot/pilot-results.json
  scripts/governance/status_migration/PR272-evidence-hardening.sha256

reconcile: 83 + 30 = 113 (inventory 113)  OK

AC8 (owner-revised): expect 83 admitted / 30 refused
MEASURED:            83 admitted / 30 refused
AC8 verdict: PASS

no-regression: every path admitted by pre or D must still be admitted by AB = True
no-overreach: every path AB admits that pre refused must be in the inventory = True
```

## AC9 — verify_ab_buckets.py

```
refused total = 30 ; admitted total = 83 ; inventory = 113

C13  declared  2  measured  2  OK
C14  declared  9  measured  9  OK
C15  declared  1  measured  1  OK
C16  declared  1  measured  1  OK
C18  declared  6  measured  6  OK
D3   declared 11  measured 11  OK
UNB  none

C total measured = 19 (declared 19) OK
C 19 + D3 11 = 30  vs refused 30  OK

AC9 historical classification untouched: 74 + 4 + 19 + 16 = 113
VERDICT: all buckets reconcile
```
