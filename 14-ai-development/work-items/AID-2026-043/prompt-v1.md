# AID-2026-043-PROMPT v1 — Make dm2_03 claim identity classification a real acceptance test

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Base: `main` at `87d503baa45918e494ac331aca3b9c103892cd01` (observed 2026-11-21).
Task: complete `crates/memory-domain/tests/phase2_acceptance.rs::dm2_03_ci_classification_vectors` against the already-implemented `claim_identity::classify`, and synchronize the English/Chinese GAP-10 frontier documents.

## Authorized scope

- Use `ClaimRevision::initial` and `ClaimRevision::successor` to construct every prior/candidate pair.
- Cover reachable CI-01, CI-02, CI-03, CI-04, CI-07, CI-08, CI-09, CI-10, CI-11 and CI-13.
- Record CI-05, CI-06 and CI-12 as unreachable because ClaimRevision has no quantifier, modality or confidence field; include the exact source-inspection grep command and its no-match output.
- Assert qualifier changes require `RequiresGovernedDecision` and never fall back to `NewRevision`.
- Assert label-only subject changes preserve identity and classify as `NewRevision`.
- Do not modify `claim_identity.rs`.
- Correct stale classifier-missing statements in both GAP-10 language versions and register this work item plus an INDEX row.

## Constraints

Do not add ignored tests, tautological assertions, APIs, dependencies or unrelated changes. Follow `domain-model-overview.md` §2.4 and the classifier implementation where the current type model makes a normative row unreachable. Keep English and Chinese documents synchronized.

## Verification requested

Run the bilingual gate, focused Phase 2 acceptance test, full memory-domain tests, workspace tests, workspace clippy with `-D warnings`, and `cargo fmt --all -- --check` in Linux/WSL2 Ubuntu. Record exact outputs. If execution is unavailable, report NOT RUN; do not claim PASS.

## Provenance

Frozen from the user-provided task dispatch in this ChatGPT conversation on 2026-11-21. Raw platform payload bytes and session identifier are not exposed.
