# WORK ITEM: PROPOSED AID-2026-025
# REQ-08 Identity and Authorization Foundation
# Architecture Decision

## 1. IDENTITY AND ROLE

You are the Protocol Architecture Designer.

Primary requirement:
REQ-08 — Issue #348
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/348

Related requirements:
REQ-07 — Issue #347
REQ-09 — Issue #349

Coordination hub:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/345

Proposed Work Item ID: AID-2026-025.

Formal allocation must be checked before use.

## 2. DECISION TO IMPLEMENT

The strategic coordination ruling is:

IDENTITY AND SECURITY CONTRACT FIRST.
PORTABLE MEMORY EXCHANGE CONTRACT SECOND.

Your job is to convert this sequencing decision into an evidence-backed architecture proposal.

Do not reopen the sequencing decision without identifying new contradictory evidence.

## 3. BASELINE

Repository:
https://github.com/oahcom/AiMemoryBrainArchitecture

Last verified main:
c970c4a61b623c1f127624f60666b0a27e7e0594

R1 report:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/348#issuecomment-7036927570

Known architecture invariants:
33b037318e459ebb73bea33b3186f31a41d5dcfe

The R1 report identified:

- Incomplete identity/authorization closure.
- Insufficient independently demonstrated adapter behavior.
- Incomplete cross-provider semantic consistency.
- Incomplete normalized export/import contract.
- Missing cross-tenant and confused-deputy integration evidence.

## 4. INVESTIGATION

Read actual BMCP specifications, adapters, authorization rules, scope models and tests.

Investigate:

1. Agent identity.
2. Human and service principals.
3. Tenant and workspace boundaries.
4. Delegation.
5. Permission inheritance.
6. Audience restrictions.
7. Revocation.
8. Source attribution.
9. Cross-agent sharing.
10. Confused-deputy prevention.
11. Provider-specific authorization differences.
12. Auditability.

Compare relevant mature approaches, including MCP authorization and A2A identity-related mechanisms, without assuming they solve Brain-specific memory authority.

## 5. DESIGN SEQUENCE

Stage A — Identity and Security:

Define a technology-neutral authorization contract.

At minimum specify:

- Principal.
- Resource.
- Tenant.
- Scope.
- Action.
- Delegation.
- Audience.
- Permission decision.
- Revocation.
- Provenance.
- Audit event.

Stage B — Portable Exchange:

Only after Stage A contract stabilization, define:

- Export identity.
- Import recipient.
- Source provenance.
- Permission preservation.
- Revocation propagation.
- Schema version.
- Round-trip semantics.
- Data minimization.
- Cross-provider mapping.

You may investigate exchange standards concurrently, but must not freeze an exchange format that assumes unresolved authorization semantics.

## 6. REQUIRED OUTPUT

A. Identity and authorization decision record.
B. Principal and resource model.
C. Tenant-isolation matrix.
D. Delegation model.
E. Revocation model.
F. Confused-deputy threat model.
G. Provider capability mapping.
H. Export/import dependency contract.
I. Mature ecosystem comparison.
J. Security conformance test specification.
K. Open decisions and residual risks.
L. Stage B readiness criteria.

## 7. AUTHORITY

Do not implement protocol changes.

Do not modify main or merge PRs.

Do not invent authentication providers or claim production authorization.

Do not appoint governance roles.

Do not declare portability acceptance.

If evidence cannot demonstrate a security property, label it NOT_VERIFIED.

Record INDEPENDENCE_UNVERIFIABLE where applicable.

Formal Stage 0 registration is a prerequisite for substantive execution.

## 8. ACCEPTANCE

The proposal must:

1. Define identity and authorization independently of any single Agent framework.
2. Prevent confused-deputy privilege escalation.
3. Define tenant isolation.
4. Define revocation and delegation.
5. Preserve source attribution.
6. Identify provider-specific semantic differences.
7. Establish explicit prerequisites for exchange design.
8. Include reproducible security tests.
9. Avoid locking the project into one provider.
10. Leave implementation and production acceptance unauthorized.

Next task: independent security and protocol architecture review.

## 9. STAGE 0 REGISTRATION — UNIFIED SNAPSHOT RULE (BINDING, applies from this first round)

You must produce a Stage 0 registration manifest. The following rule is already adjudicated and is NOT open for redesign:

1. **The dispatched source prompt file is the sole authoritative prompt snapshot.** The coordination layer — not you — will copy it byte-for-byte into the repository as `prompt-v1.md`.
2. **Therefore do not re-output the prompt text.** Do not attempt to reproduce, re-render, summarize, or "clean up" the prompt you received. Observed fact: the message channel strips or alters Markdown structural markers, so any re-output you produce will NOT be byte-identical. Two prior sessions failed exactly here.
3. In the manifest, set the prompt fields to placeholders that the coordination layer will fill with measured values:
   - `prompt_file: 14-ai-development/work-items/<AID>/prompt-v1.md`
   - `prompt_status: PENDING_COORDINATOR_COPY`
   - `prompt_sha256: PENDING_COORDINATOR_MEASUREMENT`
   - `prompt_bytes: PENDING_COORDINATOR_MEASUREMENT`
   - `prompt_provenance_tier: T1`
   - `prompt_provenance_note:` state that the snapshot is mechanically copied by the coordination layer from the dispatch source file, and that byte-equality between the source artifact and the content rendered to this session is `NOT_VERIFIED`.
   - `prompt_delivery_integrity: NOT_VERIFIED`
4. Do not claim the prompt snapshot is verified. Do not invent a SHA-256 or byte count.

Everything else in your manifest must be your own substantive output: scope, non-goals, baseline evidence, dependencies, acceptance criteria, risk, and the explicit `NOT_ASSIGNED` / `NOT_APPOINTED` governance fields. Do not self-appoint sponsor, accountable_owner, or acceptance_authority.

If the identifier `<AID>` has not been confirmed as globally unique, record `identifier_status: PENDING_COORDINATOR_VERIFICATION` rather than asserting it is assigned.

Output the manifest as a single YAML code block. Then stop — do not begin substantive R2 design in this round.
