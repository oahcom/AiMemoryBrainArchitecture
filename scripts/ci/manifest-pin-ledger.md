# Manifest Blob Pin Ledger

This ledger is append-only. Do not edit, reorder, or remove existing records. Add new records only after the corresponding repin commit has been created and its full commit SHA is known.

Each record must satisfy all of the following validity rules:

1. `manifest`, `field`, and `path` identify exactly one declared pin in the manifest.
2. `previous_pin` equals the pin value in the first parent of `repin_commit`.
3. `new_pin` equals the pin value introduced by `repin_commit`.
4. `repin_commit` is a valid full commit SHA and is an ancestor of the commit being verified.
5. Records for the same `(manifest, field, path)` form a continuous history, and the target commit's pin equals the latest recorded `new_pin`.

Replacement basis: the original repin's two 4470 -> 4412 byte transitions are present in squash-merge commit `2ab66153dbcdd8a8f2d68d234914751a748a8f74`; GET /repos/oahcom/AiMemoryBrainArchitecture/compare/2ab66153dbcdd8a8f2d68d234914751a748a8f74...main returned `status=ahead` (candidate is an ancestor of main), and the commit diff covers both manifest paths in the table below.

| manifest | field | path | previous_pin | new_pin | repin_commit |
|---|---|---|---|---|---|
|14-ai-development/work-items/AID-2026-101/manifest.yaml|session_evidence[0].executed_prompt_snapshot_file|14-ai-development/work-items/AID-2026-101/prompt-v1.md|4470|4412|2ab66153dbcdd8a8f2d68d234914751a748a8f74|
|14-ai-development/work-items/AID-2026-102/manifest.yaml|session_evidence[0].executed_prompt_snapshot_file|14-ai-development/work-items/AID-2026-102/prompt-v1.md|4470|4412|2ab66153dbcdd8a8f2d68d234914751a748a8f74|
