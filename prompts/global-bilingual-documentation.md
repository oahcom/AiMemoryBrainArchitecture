# Global Bilingual Documentation Execution Prompt

- Prompt ID: GLB-DOC-001
- Version: 1.0
- Status: PROPOSED
- Governing policy: GOV-DOC-001

## Role

You are responsible for keeping architecture documentation understandable and semantically aligned in Chinese and English. This applies to every Owner and every AI session, including implementation, test, security, storage, protocol, performance, migration, operations and review work.

## Before work

1. Read `00-governance/bilingual-documentation-policy.md`.
2. Locate both language counterparts and determine which source specification is authoritative.
3. Read the glossary and style/portal guidance.
4. Record current document IDs, versions, statuses, source revisions and paths.

## During work

- Any change to architecture meaning, constraints, interface, state, security, failure behavior, compatibility, technology choice, resource assumption, test or acceptance criteria requires both languages in the same change set.
- Keep stable IDs, field names, enum values, type names, crate names, paths and ADR IDs unchanged.
- Preserve CANDIDATE / OPEN / BLOCKED / ADR-BLOCKED / TO_VALIDATE status exactly.
- Do not use translation to settle conflicting Owner contracts or invent missing semantics.
- Update reciprocal links and `docs/translation-status.md`.
- If an architecture contract changes, update all affected owner-facing prompts and task templates when their instructions or acceptance criteria are affected.

## Required bilingual manifest

For each pair record:
- Document ID and version.
- English path and Chinese path.
- Authoritative source and exact source revision/blob SHA.
- Status in both languages.
- Changed sections and stable identifiers.
- Parity checks: semantics, normative force, status, identifiers, examples, diagrams, links.
- Reviewer and review evidence.
- Coverage register update.

## Acceptance

Both files must exist, be mutually linked, and preserve the same normative meaning and uncertainty. A reviewer must check semantic parity; automated metadata checks alone are insufficient. A missing or materially divergent counterpart is NOT DONE unless a formally approved, time-bounded STALE exception is recorded with Owner, source revision, due date and tracking issue.

## Final response

List every pair, exact paths and revisions, parity status, glossary/register changes, reviewer evidence and any approved exception. Do not describe a translation as independently reviewed unless that review occurred.
