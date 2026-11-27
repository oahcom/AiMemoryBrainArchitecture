# Session role / use case

Role: implementation and repository governance operator.
Use case: define a Work Item manifest schema and a read-only checker for
Issue #266 AC4, preserving all existing manifest contents.

# Actual AI input

The user instructed the assistant to create AID-2026-251, define the required
manifest key set and the documentation/session_evidence/implementation shapes,
add a read-only checker under scripts/ci, integrate it into the existing CI
workflow, quantify legacy violations without migrating them, and report the
merge and post-merge verification. The user specified that the PR body must
reference a real Issue, include AI-assisted-work disclosure and this file path.

# AI-visible output

The assistant created a schema, checker, work-item records and CI integration
through the GitHub repository API. CI output and merge verification are to be
recorded only after GitHub reports those results.

署名：user-authorized operator (delegated by account owner)
日期：2026-11-27
