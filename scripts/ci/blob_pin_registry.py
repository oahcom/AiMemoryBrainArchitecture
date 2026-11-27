"""Explicit registry of manifest fields that declare blob pins or non-blob refs.

Unknown digest-shaped fields are deliberately not inferred from their names.
Add a field only after its locator relationship has been verified in real
manifest data.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PinSpec:
    locator_keys: Tuple[str, ...]
    algorithm: str
    scope_source: str = "locator"


FIELD_REGISTRY = {
    # Prompt content digests.
    "prompt_sha256": PinSpec(
        locator_keys=("prompt_file",),
        algorithm="sha256",
    ),
    "executed_prompt_sha256": PinSpec(
        locator_keys=("executed_prompt_snapshot_file",),
        algorithm="sha256",
    ),
    "executed_prompt_bytes": PinSpec(
        locator_keys=("executed_prompt_snapshot_file",),
        algorithm="byte-length",
    ),

    # Git blob object IDs. The `file` sibling was observed in the nested
    # records in AID-2026-001; do not generalize this mapping to other fields.
    "git_blob_sha": PinSpec(
        locator_keys=("file",),
        algorithm="git-blob-sha1",
    ),
    "sha256_or_blob_sha": PinSpec(
        locator_keys=("file",),
        algorithm="git-blob-sha1",
    ),

    # Commit/tree/index references are not blob pins.
    "implementation_commits": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
    "base_commit_sha": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
    "prompt_file_commit_sha": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
    "merged_head_sha": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
    "merge_commit_sha": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
    "tree_sha": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
    "index_sha": PinSpec(
        locator_keys=(),
        algorithm="NON_BLOB",
        scope_source="none",
    ),
}
