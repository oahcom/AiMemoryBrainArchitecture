# Nested Claim Multi-Scope Write Authorization Test

Status: PENDING_OWNER_DECISION

Work Item: AID-2026-009
Issue: #264

Implementation baseline:
- Main: 5972a1d2f1028893d17f28a00c84202b3083da43
- SQLite Blob: d6287a3deb6497f35ca35cb73e10766cfab6449a

## Purpose

Determine whether a caller authorized for only a subset of a
parent Memory's scopes may create a Claim carrying a scope that
belongs to the parent Memory but is outside the caller's authorized
scope set.

## Fixture

Parent Memory scopes:
- s1
- s2

Caller authorized scopes:
- s1

New Claim scopes:
- s2

## Expected Result

PENDING_OWNER_DECISION.

The test MUST NOT be marked passing or failing until the
B/domain and I/security Owners decide the authorization rule.

Candidate policy A:
- Require every Claim scope to be contained in the caller's
  authorized scope set.
- Under this policy, the write MUST be denied.

Candidate policy B:
- Permit a different explicitly authorized parent-mediated
  write rule.
- Under this policy, the result MUST follow the approved
  rule and its documented authorization evidence.

## Required Assertions After Decision

1. The implementation follows the approved Owner policy.
2. Rejected writes leave no partial Claim or version state.
3. No unauthorized ScopeRef is persisted.
4. The test covers both single-scope and multi-scope parents.
5. The test records the exact contract version used.

## Acceptance Gate

Do not convert this specification into a normative executable
assertion until both relevant Owners have recorded their decisions.

After approval:
- Implement the corresponding positive and negative cases.
- Run the targeted SQLite tests.
- Record the CI run ID and exact tested commit SHA.
- Verify transaction rollback on rejection.
