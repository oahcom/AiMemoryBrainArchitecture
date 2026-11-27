# AID-2026-268 evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Baseline fetched:** 2026-11-27T03:57:43Z  
**Baseline main:** 40195e8bf96b9cc6aa254066b9b72968f29ac361

## Scope

Implement blob-pin integrity checking in the existing required Repository hygiene job. No branch-protection, new-job, or new-workflow changes are in scope.

## Measurements

The baseline full scan and the #1220 negative scan are pending execution by GitHub Actions on an exact checkout. No scan counts, test results, required-context result, or merge SHA are claimed in this evidence file until the corresponding raw outputs are observed.

## Field enumeration

The checker implementation contains explicit branches for:
- top-level `root/root_blob`, `en_mirror/en_mirror_blob`, and `zh_cn_mirror/zh_cn_mirror_blob`;
- `gate_a_reconstruction[].root/reconstructed_root_blob`, resolved against the entry's explicit source commit or a commit SHA explicitly named in its note;
- `related_evidence[].path/blob` and its EN/ZH-CN mirror pairs;
- top-level `evidence_file/evidence_blob`;
- `d_source_blobs[]` entries, resolved against `d_source_commit`;
- `prompt.prompt_file` with `prompt_sha256/prompt_bytes`;
- `session_evidence[].executed_prompt_snapshot_file` with `executed_prompt_sha256/executed_prompt_bytes`.

Non-blob metadata such as timestamps, counts, and status values is deliberately ignored.
