"""Strict YAML and structural validation for AID-2026-001's governance Manifest."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from yaml.constructor import ConstructorError
from yaml.resolver import BaseResolver


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "14-ai-development/work-items/AID-2026-001/manifest.yaml"


class UniqueKeySafeLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects duplicate mapping keys at every depth."""


def _construct_unique_mapping(loader: UniqueKeySafeLoader, node: yaml.MappingNode,
                              deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping", node.start_mark,
                "found an unhashable mapping key", key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"found duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeySafeLoader.add_constructor(
    BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def load_yaml_unique(text: str) -> Any:
    """Parse YAML safely and reject duplicate keys in every mapping."""
    return yaml.load(text, Loader=UniqueKeySafeLoader)


def validate_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    data = load_yaml_unique(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest root must be a YAML mapping")

    required = (
        "work_item_id", "title", "class", "risk", "status",
        "repository", "base_branch", "r3_test_matrix",
        "r3_security_specialist_prompt",
        "r3_forget_specialist_prompt",
        "integration_reviewer_prompt",
    )
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing required top-level keys: {missing}")
    if data["work_item_id"] != "AID-2026-001":
        raise ValueError("Unexpected work_item_id")
    if data["class"] != "ARCH" or data["risk"] != "R3":
        raise ValueError("AID-2026-001 must remain ARCH/R3")

    for key in (
        "r3_test_matrix",
        "r3_security_specialist_prompt",
        "r3_forget_specialist_prompt",
        "integration_reviewer_prompt",
    ):
        target = REPO_ROOT / data[key]
        if not target.is_file():
            raise ValueError(f"Manifest path does not exist: {key}={data[key]}")
    return data


if __name__ == "__main__":
    result = validate_manifest()
    print("AID-2026-001 Manifest: unique-key YAML parse and required-field/path checks PASS")
    print("Formal JSON Schema validation is not provided by this repository validator.")
    print(f"Validated Work Item: {result['work_item_id']} ({result['class']}/{result['risk']})")
