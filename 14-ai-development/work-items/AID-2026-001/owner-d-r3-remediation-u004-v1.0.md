<!--
Archive wrapper added 2026-11-18.
Classification: FROZEN HISTORICAL PROMPT / TRANSPORT_NORMALIZED.
The prompt body below is the rendering-retrieved copy supplied by the human Owner.
It is NOT the unrecoverable 12,359-byte original capture and is NOT byte-identical evidence for that original.
The supplied capture metadata (12,202 UTF-8 bytes, no trailing newline; SHA-256 22ea8670d0a06880713547b806947e4d14086bb725c9af1a13828e9c2ac0b31a) is provenance reported by the human Owner, not a hash of this archive file.
The embedded Prompt SHA-256 1ff44263b8b4dbb554419010ed280741454bb80c836cec6e6005815e247e7c4b is retained as a historical declaration only; it is not verified against this rendering-retrieved body.
This archived prompt is not a current execution instruction. Its historical branch/PR pins must not be used as live authority. In particular, its own stop condition requires stopping if PR #66 is merged; PR #66 is merged.
Canonical execution instructions must be separately versioned and pinned to an exact immutable commit.
-->

# Archive provenance / 归档来源

- Prompt ID: `AID-2026-001-U-004`
- Version: `v1.0`
- Archive status: `FROZEN_HISTORICAL / TRANSPORT_NORMALIZED`
- Capture class: rendering-retrieved copy supplied by human Owner
- Human-reported capture: 12,202 UTF-8 bytes, excluding trailing newline
- Human-reported capture SHA-256: `22ea8670d0a06880713547b806947e4d14086bb725c9af1a13828e9c2ac0b31a`
- Original declared source: 12,359 UTF-8 bytes; unrecoverable; not reconstructed
- Original embedded SHA-256 declaration: `1ff44263b8b4dbb554419010ed280741454bb80c836cec6e6005815e247e7c4b` (historical declaration only)
- Integrity disposition: `TRANSPORT_EQUIVALENT_UNPROVEN`
- Execution disposition: `HISTORICAL_ONLY — DO NOT EXECUTE AS CURRENT TASK`
- Reason: the prompt's recorded baseline and PR pins are stale; PR #66 is merged, and §3/§10 explicitly require STOP when PR #66 is merged.

---

# Original prompt body / 原提示词正文

U-004 — Owner D R3 Forget/Lifecycle Remediation Continuation

Prompt ID: AID-2026-001-U-004
Version: v1.0
SHA-256: 1ff44263b8b4dbb554419010ed280741454bb80c836cec6e6005815e247e7c4b
Work Item: AID-2026-001
Tracking: oahcom/AiMemoryBrainArchitecture, Issue #41
Role: Owner D remediation session (not independent reviewer; not Owner I)
Risk: R3
Task class: ARCH / DOC / TEST-EVIDENCE (tests only when actually executable)
Execution authority: human Owner's explicit instruction to continue in this session. This is not unattended or scheduled model execution.

1. Identity

You are acting solely as Owner D for AID-2026-001. The findings in scope are D-R3-D-001, D-R3-D-002 and D-R3-D-004. D-R3-D-003 is a bilateral D/I approval gate and is not closable by D alone.

Governing instructions: read the current main versions of:

14-ai-development/AI-EXEC-001.md

14-ai-development/AI-EXEC-002.md

prompts/global-project-developer.md

prompts/global-bilingual-documentation.md

the current Owner D prompt under prompts/ (identify its canonical current path and version)

Also read the current Issue #41, the AID-2026-001 manifest, and the exact existing D/I/Storage proposal artifacts before editing. If any required instruction is unavailable, stop and report the precise gap; do not claim it was loaded.

2. Objective

Close the D-owned semantic defects without creating parallel work:

D-R3-D-001: make Lifecycle Manager authority, D domain ownership, and I governance/authorization ownership mutually consistent and non-overlapping.

D-R3-D-002: define the exact legal point and preconditions for Memory.lifecycle = Forgotten, including the I authorization dependency and the failure/unknown/revocation outcomes.

D-R3-D-004: define a typed, exhaustive, monotonic mapping between Memory lifecycle and ForgetOperation phase/state, without collapsing the two state machines.

Produce a D-owned, bilingual, reviewable proposal and exact evidence. Do not represent the proposal as approved or normative until the required authorities approve the same exact content.

3. Baseline and existing carrier — no new branch

Repository: oahcom/AiMemoryBrainArchitecture.

Supplied and compare-accepted main baseline: 6b5db2918cffc2281deb22fd9858a37dbaeec726.

Reuse the existing candidate branch:

proposal/d-forget-terminal-linearization-closure-2026-11-18

Existing carrier: PR #66, “docs(D): propose Forget terminal and linearization closure (Phase 3.9)”.

Recorded PR #66 proposal Head:

4d1a04449cdb8bbdb516e4fd72048173defbece4

Companion I carrier: proposal/i-d-forget-terminal-authorization-2026-11-18, PR #68, recorded Head:

a71985e360c7ab8aa8ca7e8d63b9460035cc9e02

Related joined remediation carrier:

remediation/aid-2026-001-forget-contract-closure-2026-11-18 (PR #72).

Storage review carrier: PR #71.

These recorded Heads are pins to verify, not permission to overwrite a newer Head. Before any mutation, independently read the live refs and PR metadata. If the D branch is absent, its current Head differs from the recorded Head, PR #66 is merged, its target/base cannot be established, or another channel has advanced it, STOP before editing.

If PR #66 is closed but unmerged, do not reopen it; proceed on the existing branch only if the live Head and ownership are unambiguous, and report that no open PR currently carries the work.

If PR #66 is open, preserve its existing target/base.

Do not create a replacement branch, PR, or issue. Do not rebase or force-push. Do not target or modify main.

4. Authority and prohibited actions

You may author D-owned domain semantics and D-owned evidence.

You may not:

approve your own proposal, act as Owner I, or simulate an I signature;

approve Storage's commit/atomicity boundary on Storage's behalf;

convert CANDIDATE/OPEN/TO_VALIDATE to DECIDED by assertion;

declare any of the findings VERIFIED_FIXED, ACCEPTED, or CLOSED merely because prose was added;

merge, deploy, activate production behavior, change permissions/rulesets, or create a new PR/Issue;

claim a test passed unless it was actually executed on the exact identified source/test commit and the output is retained.

D-R3-D-003 requires a separate Owner I decision and explicit D/I bilateral approval against the same exact joined-contract Blob SHA.

I must independently approve/reject I-owned authorization, PermissionEpoch/currentness, revocation ordering, exception, and global-evaluator semantics.

Storage must separately approve the authoritative commit boundary.

A non-implementing Integration Reviewer must later review the joined exact version.

5. Scope

In scope:

D lifecycle and ForgetOperation semantics relevant to the three findings;

exact I authorization receipt interface and D-side validation/consumption boundary, without taking ownership of I's implementation or policy;

D/I authority matrix alignment;

bilingual D proposal and necessary D-owned cross-references;

state mapping, invariants, negative cases, and executable-test specifications;

Issue #41 and AID-2026-001 manifest/evidence updates on the existing carrier only.

Out of scope:

implementing I authorization or global governance policy;

Storage physical topology, production code, or physical-erasure claims;

unrelated Owner/module changes;

topology-in-repository work, production R3 certification, or acceptance/merge.

6. State of knowledge

Treat as established only after re-reading exact source artifacts:

PR #66 is the focused D Phase 3.9 proposal; PR #68 is the I authorization companion; PR #71 is a Storage-role review; PR #72 is a broader joined D/I remediation proposal.

The prior independent Owner D review was BLOCKED on D-R3-D-001…004.

Existing reference-model results are bounded model evidence only, not production R3 conformance.

Record each relevant contract as DECIDED, CANDIDATE, OPEN, or TO_VALIDATE with source path, Blob SHA and approving authority.

Preserve conflicts; do not silently reconcile by inventing authority.

7. Required steps

Preflight: read all governing instructions and current Issue #41/manifest; verify main SHA, D branch live Head, PR #66 target/base/state, and companion PR/branch Heads. Fetch the exact D/I/Storage proposal documents and relevant controlling lifecycle/security contracts.

Collision guard: use the stable work key AID-2026-001/U-004/D-R3-D-001+002+004. Re-read recent Issue #41 comments and branch Head. If another channel has an active claim or a newer commit touching the same scope, do not race it; stop and report. Before editing, record a short idempotent execution claim on Issue #41 containing this work key, branch, observed Head and Prompt ID/hash. Do not create a new Issue.

Build a finding-to-clause matrix. For each finding record: original defect, affected contract clauses, D-owned correction, I/Storage dependency, required proof, acceptance authority, and remaining OPEN items.

Inspect the existing PR #66 files and related PR #68/#72/#71 artifacts. Reuse and amend the existing D carrier. Do not duplicate existing clauses or tests. Reconcile overlapping proposals by exact Blob comparison and explicit precedence; do not copy stale snapshots wholesale.

Correct the D-owned bilingual proposal and state mapping. At minimum define:

distinct Memory lifecycle vs ForgetOperation phase;

monotonic transitions;

pre-Fence vs post-Fence failure/cancellation;

canonical suppression vs logical Forgotten vs global completion vs physical erasure;

exact event binding;

I receipt validation;

COMMIT_WON, REVOCATION_WON, and UNKNOWN;

stale proof/fence, retry, idempotency, replay and recovery behavior;

D outcome closeout.

Ensure no D clause grants D authority over I policy or lets I rewrite D's canonical domain result. State the D/I handoff and Storage commit-boundary obligations explicitly.

Add or amend test specifications for each transition/race. Execute only tests that are actually runnable in the available repository environment. For every executed test record command, runtime, source SHA, test SHA, exact commit, raw result and limitations. A reasoning walkthrough, generated table, test plan, or unexecuted model is NOT a test PASS.

Update the manifest and execution record truthfully. Keep R3 and Work Item status blocked/pending until all independent approvals and required evidence exist. Do not mark D-R3-D-003 complete.

Re-read the resulting branch Head and every changed Blob. Check bilingual semantic parity, links, schema/manifest validity where executable, and diff scope. If a validation cannot run, record NOT RUN with reason.

Update Issue #41 with the finding matrix, changed paths/Blob SHAs, exact Head, prompt provenance, test evidence, D decision status, I handoff request and explicit remaining blockers. Do not declare DECIDED/ACCEPTED.

Stop and hand off to Owner I for independent authorization review and same-Blob bilateral decision. Then require Storage's exact commit-boundary decision and independent Integration Review before any acceptance consideration.

8. Acceptance criteria

All three D findings have clause-level, bilingual, exact-Blob remediation proposals.

D/I authority boundaries are consistent and no authority is self-assigned.

Memory lifecycle and ForgetOperation are distinct typed state machines with a complete explicit mapping and failure semantics.

Forgotten transition is bound to current D suppression evidence and the exact I authorization outcome; revocation/unknown/stale evidence fails closed without rolling back an installed Fence.

Every claimed verification is reproducible and exact-commit-bound; unexecuted tests are explicitly NOT RUN.

Existing branch/PR carrier is reused; no new branch, PR or Issue is created.

Issue #41 and manifest point to the same exact resulting Head and prompt provenance.

Overall disposition remains BLOCKED/PENDING until I, Storage and independent review gates are met.

9. Verification

Use repository-supported deterministic checks only. Record exact commands and outputs.

Never infer CI success from workflow-file presence, infer runtime behavior from a reference model, or treat old test runs as current-Head evidence.

No test PASS may be claimed from reasoning, simulation in prose, or test-source inspection.

10. Git workflow

Work only on proposal/d-forget-terminal-linearization-closure-2026-11-18, using the live verified Head as the expected parent.

Commit only the smallest coherent D-owned changes.

Before each write, re-read the branch Head; after each commit, verify fast-forward ancestry and exact resulting Head.

No force push, no rebase, no main write, no merge, no new branch, no new PR, no new Issue.

Preserve the existing PR base and disposition; never reopen or retarget it. If PR #66 is merged, stop. If it is closed unmerged, keep the branch-only continuation and report the lack of an open integration carrier.

11. Stop and escalation

Stop immediately on branch/PR mismatch, concurrent channel mutation, unclear D/I authority, incompatible controlling contracts, missing source, unexpected scope expansion, failed validation, or any request to self-approve.

Report the exact observed state and escalate to the human Owner.

Route I-owned clauses to Owner I and Storage commit-boundary clauses to Storage.

Do not improvise an approval.

12. Evidence and final report

Return:

LOADED or LOADED-PARTIAL with exact governing documents/sections actually read;

main SHA, D branch live Head, PR #66 state/base/head and companion PR/branch Head readbacks;

Prompt ID/version/SHA-256 and execution claim key;

finding-to-clause matrix for D-R3-D-001/002/004;

changed paths, Blob SHAs, commit SHA and exact branch Head;

tests: PASS only for actually executed exact-commit runs; otherwise NOT RUN / NOT EVIDENCED;

D's own decision (proposal only unless authorized exact-Blob Owner decision recorded);

Owner I handoff and D-R3-D-003 bilateral approval status;

Storage and independent-review dependencies;

Issue #41 comment URL/ID if actually written;

final status: BLOCKED / PENDING unless every required authority and evidence gate is independently satisfied.

=== END ORIGINAL PROMPT BODY ===
