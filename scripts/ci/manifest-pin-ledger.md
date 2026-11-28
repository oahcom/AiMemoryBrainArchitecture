# Manifest Blob Pin Ledger

This ledger is append-only. Do not reorder or remove existing records. Add new records only after the corresponding repin commit has been created and its full commit SHA is known. A recorded repin_commit may be corrected only when repository history proves the recorded SHA is wrong and the replacement identifies the commit that actually introduced the recorded pin transition; the manifest, field, path, previous_pin, and new_pin must remain unchanged.

Correction: the two AID-2026-101 and AID-2026-102 rows below incorrectly recorded an unmerged branch commit. Their pin transitions were introduced on the verified target history by 44b57170b86c7f3e56744da756ed24744b1c659c. Only repin_commit is corrected.

Each record must satisfy all of the following validity rules:

1. `manifest`, `field`, and `path` identify exactly one declared pin in the manifest.
2. `previous_pin` equals the pin value in the first parent of `repin_commit`.
3. `new_pin` equals the pin value introduced by `repin_commit`.
4. `repin_commit` is a valid full commit SHA and is an ancestor of the commit being verified.
5. Records for the same `(manifest, field, path)` form a continuous history, and the target commit's pin equals the latest recorded `new_pin`.

| manifest | field | path | previous_pin | new_pin | repin_commit |
|---|---|---|---|---|---|
|14-ai-development/work-items/AID-2026-101/manifest.yaml|session_evidence[0].executed_prompt_snapshot_file|14-ai-development/work-items/AID-2026-101/prompt-v1.md|4470|4412|44b57170b86c7f3e56744da756ed24744b1c659c|
|14-ai-development/work-items/AID-2026-102/manifest.yaml|session_evidence[0].executed_prompt_snapshot_file|14-ai-development/work-items/AID-2026-102/prompt-v1.md|4470|4412|44b57170b86c7f3e56744da756ed24744b1c659c|
