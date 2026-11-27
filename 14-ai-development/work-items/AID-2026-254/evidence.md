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
        - "14-ai-development/work-items/AID-2026-254/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The baseline numbers below were independently recomputed from the GitHub Git Trees and Contents API at base commit a7a252eb670b31066a0ffea35dc28cbe6ef5b836. The script is committed as a reproducible local read-only equivalent; this session did not claim a local CLI execution."
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
      - "attention-cost"
      - "context-switching"
      - "work-item-fanout"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-254 — Attention and context-switching cost measurement

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Decision status:** proposed measurement mechanism; no natural-person Owner approval or acceptance is claimed.

## 1. Measurement definition

This work item introduces **declared root/domain fan-out** as a reproducible proxy for attention and context-switching burden:

- For each Work Item manifest, read only path-bearing list entries under `scope.changes`, `scope.files_to_create`, `scope.files_to_modify`, or `scope.files_changed`.
- For each declared repository path, take its first repository-root directory (for example `scripts/`, `docs/`, `07-agent-integration/`, or `.github/`).
- Count distinct roots per Work Item. A root is counted once even if many files under it change.
- The cohort is the ten numerically newest `AID-2026-NNN/manifest.yaml` files present at the measured Git ref. The measurement is a scope/fan-out proxy, **not** a claim about elapsed time, cognitive load, or observed human session count. Undeclared paths are not inferred.

Reproduction command (standard library only; read-only):

```sh
python3 scripts/measure_attention_context_cost.py --ref a7a252eb670b31066a0ffea35dc28cbe6ef5b836 --limit 10
```

The script reads committed Git objects with `git ls-tree` and `git show`; it does not write files, alter manifests, or add dependencies. The baseline below was recomputed for that exact ref from the GitHub Git Trees API (recursive tree, `truncated=false`) and the ten manifest blobs via the GitHub Contents API, applying the same scope-list/root-set rule. This was an API-side readback, not a claim that the shell command ran in this API-only session.

## 2. Measured baseline

```text
ref=a7a252eb670b31066a0ffea35dc28cbe6ef5b836 cohort=10
AID-2026-251 roots=3 [.github, 14-ai-development, scripts]
AID-2026-240 roots=4 [14-ai-development, docs, reviews, scripts]
AID-2026-211 roots=5 [00-governance, 09-security-governance, 14-ai-development, docs, scripts]
AID-2026-210 roots=3 [07-agent-integration, 14-ai-development, docs]
AID-2026-204 roots=3 [14-ai-development, docs, scripts]
AID-2026-200 roots=3 [01-system-architecture, 02-domain-model, 06-memory-context]
AID-2026-199 roots=1 [scripts]
AID-2026-198 roots=3 [14-ai-development, docs, scripts]
AID-2026-197 roots=2 [.github, scripts]
AID-2026-193 roots=2 [14-ai-development, docs]
mean_roots_per_work_item=2.90 (29/10)
max_roots_per_work_item=5
distribution=1:1, 2:2, 3:5, 4:1, 5:1
over_soft_budget(>3)=2 [AID-2026-240, AID-2026-211]
over_hard_cap(>5)=0 [none]
```

Calculation source: `GET /repos/oahcom/AiMemoryBrainArchitecture/git/trees/a7a252eb670b31066a0ffea35dc28cbe6ef5b836?recursive=1` to enumerate the tree; `GET /repos/oahcom/AiMemoryBrainArchitecture/contents/14-ai-development/work-items/AID-2026-NNN/manifest.yaml?ref=a7a252eb670b31066a0ffea35dc28cbe6ef5b836` for each cohort manifest. The cohort and every root set are listed above so the arithmetic can be checked independently.

## 3. Budget and overrun handling

The proposed operating thresholds are:

- **Budget: at most 3 distinct roots per Work Item.** This is the observed cohort mean rounded up to a whole-root budget (2.90 → 3), not a claim that three is a universal cognitive limit.
- **Soft overrun: 4–5 roots.** Before implementation proceeds, split independently deliverable work into separate Work Items/PRs where ownership and acceptance boundaries permit. If splitting would create more coordination overhead or break a coherent change, record a short exception in the manifest/evidence naming the roots, why they must remain coupled, and the mitigation (one owner, one PR, one acceptance checklist).
- **Hard stop: more than 5 roots.** Do not start or continue implementation until the scope is decomposed or an explicit accountable-Owner exception is recorded. A hard-stop exception is not implied by a proxy operator's signature.
- Re-measure at dispatch and before PR creation. If the scope changes and crosses a threshold, update the manifest and record the reason; do not silently absorb new roots.

On this baseline, two of ten items exceed the soft budget (AID-2026-240 at four roots and AID-2026-211 at five); none exceeds the hard cap. This is a retrospective signal, not a retrospective finding of fault.

## 4. Limits and next measurement

The current repository does not provide a consistent machine-readable session-switch ledger for every Work Item. Therefore this deliverable does not invent a session-switch count. A future extension should record session handoffs explicitly in each `session-evidence.md` (from-session role, to-session role, handoff reason, timestamp or ordered sequence) before aggregating session transitions. Root fan-out remains available now because it can be reconstructed from committed manifest scope.

## 5. Attribution and acceptance boundary

Recorded by **user-authorized operator (delegated by account owner)** on **2026-11-27**. This is a proxy work record, not a natural-person Owner signature. Thresholds are proposed for AC8 review; Issue #265 remains open and unchanged.
