# AID-2026-279 Prompt Snapshot

Source: user-provided task in the S6-A implementation conversation.
Capture status: structured task snapshot, not a raw platform transcript.
Date: 2026-11-27.

Implement Issue #1341 as a serialized merge-time work-item uniqueness gate in
oahcom/AiMemoryBrainArchitecture using GitHub API only. A candidate newly
introducing an AID-YYYY-NNN directory must be rejected when the identifier is
already present on the latest target branch. New files beneath a directory
already present at merge-base must be accepted. Exit codes: 0 PASS, 1
VIOLATION, 2 INCOMPLETE; missing refs or unreadable Git state never pass.

Create scripts/ci/check_work_item_uniqueness.py and
scripts/ci/test_work_item_uniqueness.py. Wire both explicitly into the existing
GOV-DOC-002 metadata checks job, which is already a required context; do not add
a job or alter the 16 required contexts. Use PR_BASE / PUSH_BEFORE selection,
with push base github.event.before. Do not modify branch protection,
check_manifest_blob_pins.py, or repository-hygiene.yml. Use a unique
work-item number in 260-279, preserve block-style YAML metadata, include
required PR evidence declarations, and provide actual execution, open-PR,
serialization, and post-merge evidence.
