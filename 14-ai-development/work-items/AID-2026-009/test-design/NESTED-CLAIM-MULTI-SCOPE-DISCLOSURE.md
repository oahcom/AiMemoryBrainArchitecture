# Nested Claim Multi-Scope ScopeRef Disclosure Test

Status: PENDING_OWNER_DECISION

Work Item: AID-2026-009
Issue: #264

Implementation baseline:
- Main: 5972a1d2f1028893d17f28a00c84202b3083da43
- SQLite Blob: d6287a3deb6497f35ca35cb73e10766cfab6449a

## Purpose

Determine how a multi-scope Claim is exposed to a reader
authorized for only a subset of the Claim's scopes.

## Fixture

Claim scopes:
- s1
- s2

Reader authorized scopes:
- s1

Unauthorized scope:
- s2

## Expected Result

PENDING_OWNER_DECISION.

The test MUST NOT assume that the Claim must be entirely hidden
or that its ScopeRef metadata must be projected before the
relevant Owners approve the disclosure policy.

Candidate policy A:
- Hide the entire Claim if the reader does not satisfy the
  required authorization rule.

Candidate policy B:
- Permit Claim visibility but project ScopeRef metadata to
  the authorized subset.

Candidate policy C:
- Permit another explicitly documented disclosure model
  approved by the relevant Owners.

## Required Assertions After Decision

1. Claim visibility follows the approved disclosure policy.
2. Unauthorized ScopeRef metadata is not disclosed unless
   explicitly permitted by the approved policy.
3. Returned metadata is consistent across all read paths.
4. Historical versions follow the same approved policy.
5. The test records the exact disclosure contract version.

## Acceptance Gate

Do not convert this specification into a normative executable
assertion until the B/domain and I/security Owners have recorded
their decisions.

After approval:
- Implement the approved visibility and projection behavior.
- Test both current and historical reads.
- Test direct and nested read paths.
- Record targeted test names, CI Run ID and exact tested commit SHA.
