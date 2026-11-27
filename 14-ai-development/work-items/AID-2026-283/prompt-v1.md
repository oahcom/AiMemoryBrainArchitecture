---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-283/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured task capture; the digest covers this committed file including this block."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "prompt-snapshot"
      - "work-item-uniqueness"
      - "merge-time-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-280 — Executed implementation prompt

## Role

L1 triage owner and L2 implementation session.

Repository: oahcom/AiMemoryBrainArchitecture.

## Task

Repair the work-item uniqueness gate bypass caused by GitHub Update-branch.

## Background

AID-2026-279 introduced:

scripts/ci/check_work_item_uniqueness.py

The gate is required through:

GOV-DOC-002 metadata checks

The previous implementation calculates introduced directories relative to merge-base.

Independent reproduction demonstrated that after one PR introduces and merges an ID, another PR introducing the same ID can Update-branch against main. The merge-base advances, the second PR's introduced set becomes empty, and the gate incorrectly reports PASS.

This is a contract defect because strict branch protection requires the operation that erases the old comparison evidence.

## Required contract

A candidate claims a work-item directory when:

1. The directory exists in candidate HEAD.
2. At least one non-merge commit in base..head first introduces the directory relative to its first parent.

Update-branch merge commits must not independently create claims by importing directories from base.

An existing directory receiving additional files must not be classified as a new claim.

A deleted candidate directory must not remain an active claim.

## Implementation

Make the minimum changes to:

- scripts/ci/check_work_item_uniqueness.py
- scripts/ci/test_work_item_uniqueness.py

Preserve the existing required context, exit codes, and unrelated behavior.

Do not rewrite the existing uniqueness gate.

## Tests

Retain all five existing tests.

Add three independent temporary-Git-history tests:

1. Update-branch does not erase the original claim.
2. Adding a file to an existing base directory is permitted.
3. Two branches independently introducing the same ID cannot both pass after the first merges and the second updates its base.

Expected total: eight tests.

## Mutation requirements

Demonstrate that:

- Restoring merge-base comparison causes the Update-branch assertions to fail.
- Treating every added file as a new claim causes the additive test to fail.
- Existing occupied/return-code mutations remain detectable.

## Out of scope

Do not retrospectively renumber existing duplicate IDs.

Do not automatically resolve historical duplicates.

Do not rename the required context.

Do not redesign the governance subsystem.

## Evidence

Record:

- Exact base SHA.
- Exact candidate head SHA.
- Changed files.
- Test command and complete output.
- Mutation commands and complete output.
- Pull request URL and merge SHA, if merged.

The prompt's SHA-256 and byte count are supplied by the delivery operator after the final prompt file is written.
