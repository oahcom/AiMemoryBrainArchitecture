"""G-local executable reference model for Context ChangeSets.

This is an in-memory semantic model only. It does not provide durable storage,
cross-store atomicity, D/I authority, transport, or production concurrency.
External gate facts are inputs and are never minted by this module.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping


class ContextModelError(ValueError):
    pass


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


@dataclass
class ContextLedger:
    context_id: str
    scope_refs: tuple[str, ...]
    head_version: int = 1
    entries: dict[str, dict[str, Any]] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    idempotency: dict[str, tuple[str, dict[str, Any]]] = field(default_factory=dict)
    tombstones: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.context_id or not self.scope_refs or self.head_version < 1:
            raise ContextModelError("context identity and positive initial version required")
        if len(set(self.scope_refs)) != len(self.scope_refs):
            raise ContextModelError("duplicate scope reference")

    def apply_changeset(
        self,
        *,
        base_version: int,
        idempotency_key: str,
        operations: list[Mapping[str, Any]],
    ) -> dict[str, Any]:
        if not idempotency_key or not operations:
            raise ContextModelError("idempotency key and non-empty operations required")
        payload_digest = _digest(list(operations))
        previous = self.idempotency.get(idempotency_key)
        if previous:
            old_digest, old_result = previous
            if old_digest == payload_digest:
                return {**deepcopy(old_result), "status": "IDEMPOTENT_REPLAY"}
            raise ContextModelError("IDEMPOTENCY_KEY_REUSE")
        if base_version != self.head_version:
            raise ContextModelError("BASE_VERSION_MISMATCH")

        staged = deepcopy(self.entries)
        staged_tombstones = set(self.tombstones)
        for op in operations:
            self._apply_one(staged, staged_tombstones, op)

        target_version = self.head_version + 1
        result = {
            "status": "COMMITTED_IN_REFERENCE_MODEL",
            "context_id": self.context_id,
            "base_version": self.head_version,
            "target_version": target_version,
            "payload_digest": payload_digest,
            "entry_ids": sorted(staged),
        }
        # One in-memory state transition after every operation validates.
        self.entries = staged
        self.tombstones = staged_tombstones
        self.head_version = target_version
        self.history.append(deepcopy(result))
        self.idempotency[idempotency_key] = (payload_digest, deepcopy(result))
        return deepcopy(result)

    def _apply_one(
        self,
        staged: dict[str, dict[str, Any]],
        tombstones: set[str],
        op: Mapping[str, Any],
    ) -> None:
        kind = op.get("type")
        if kind == "ADD":
            entry = deepcopy(op.get("entry"))
            self._validate_entry(entry)
            entry_id = entry["entry_id"]
            if entry_id in staged or entry_id in tombstones:
                raise ContextModelError("ENTRY_ID_EXISTS_OR_TOMBSTONED")
            membership = (entry["memory_id"], entry["memory_version_id"])
            if any((e["memory_id"], e["memory_version_id"]) == membership for e in staged.values()):
                raise ContextModelError("DUPLICATE_MEMBERSHIP")
            staged[entry_id] = entry
            return
        if kind == "UPDATE":
            entry_id = op.get("entry_id")
            if entry_id not in staged:
                raise ContextModelError("ENTRY_NOT_FOUND")
            patch = op.get("patch")
            allowed = {"tier", "priority", "rendered_content", "activation_reason", "content_hash"}
            if not isinstance(patch, Mapping) or not patch or set(patch) - allowed:
                raise ContextModelError("INVALID_UPDATE_PATCH")
            staged[entry_id].update(deepcopy(dict(patch)))
            if not staged[entry_id].get("rendered_content", "").strip():
                raise ContextModelError("EMPTY_RENDERING")
            return
        if kind == "REMOVE":
            entry_id = op.get("entry_id")
            if entry_id not in staged:
                raise ContextModelError("ENTRY_NOT_FOUND")
            del staged[entry_id]
            tombstones.add(entry_id)
            return
        if kind == "REPLACE":
            old_id = op.get("old_entry_id")
            entry = deepcopy(op.get("entry"))
            if old_id not in staged:
                raise ContextModelError("ENTRY_NOT_FOUND")
            self._validate_entry(entry)
            new_id = entry["entry_id"]
            if new_id != old_id and (new_id in staged or new_id in tombstones):
                raise ContextModelError("ENTRY_ID_EXISTS_OR_TOMBSTONED")
            del staged[old_id]
            tombstones.add(old_id)
            membership = (entry["memory_id"], entry["memory_version_id"])
            if any((e["memory_id"], e["memory_version_id"]) == membership for e in staged.values()):
                raise ContextModelError("DUPLICATE_MEMBERSHIP")
            staged[new_id] = entry
            return
        if kind == "REORDER":
            order = op.get("entry_ids")
            if not isinstance(order, list) or len(order) != len(set(order)) or set(order) != set(staged):
                raise ContextModelError("REORDER_MUST_NAME_EACH_ENTRY_ONCE")
            for position, entry_id in enumerate(order):
                staged[entry_id]["position"] = position
            return
        if kind == "EXPIRE":
            entry_id = op.get("entry_id")
            if entry_id not in staged:
                raise ContextModelError("ENTRY_NOT_FOUND")
            del staged[entry_id]
            tombstones.add(entry_id)
            return
        raise ContextModelError("UNKNOWN_OPERATION")

    def _validate_entry(self, entry: Any) -> None:
        required = ("entry_id", "memory_id", "memory_version_id", "scope_refs",
                    "lifecycle", "rendered_content", "source_refs", "content_hash")
        if not isinstance(entry, Mapping) or any(k not in entry for k in required):
            raise ContextModelError("ENTRY_SHAPE_INVALID")
        if not all(isinstance(entry[k], str) and entry[k].strip()
                   for k in ("entry_id", "memory_id", "memory_version_id",
                             "lifecycle", "rendered_content", "content_hash")):
            raise ContextModelError("ENTRY_REQUIRED_FIELD_EMPTY")
        if entry["lifecycle"] not in ("Active", "Consolidated"):
            raise ContextModelError("CANONICAL_LIFECYCLE_INELIGIBLE")
        scopes = set(entry["scope_refs"])
        if not set(self.scope_refs).issubset(scopes):
            raise ContextModelError("SCOPE_MISMATCH")
        if not entry["source_refs"]:
            raise ContextModelError("LINEAGE_MISSING")


def reconcile_entry(
    entry: Mapping[str, Any],
    *,
    canonical_status: str,
    permission_current: bool | None,
    forget_clear: bool | None,
    retrieval_complete: bool,
) -> dict[str, str]:
    """Classify one entry from caller-supplied authority observations.

    None means unknown, never allow. This function does not call D, I or F.
    """
    if not retrieval_complete:
        return {"classification": "Unknown", "action": "Block"}
    if permission_current is not True or forget_clear is not True:
        return {"classification": "Blocked", "action": "Block"}
    mapping = {
        "ACTIVE": ("Valid", "Keep"),
        "CONSOLIDATED": ("Valid", "Keep"),
        "SUPERSEDED": ("Superseded", "ReplaceOrRemove"),
        "RETRACTED": ("Retracted", "Remove"),
        "FORGOTTEN": ("Forgotten", "Remove"),
        "EXPIRED": ("Expired", "Remove"),
        "UNKNOWN": ("Unknown", "Block"),
    }
    classification, action = mapping.get(canonical_status, ("Unknown", "Block"))
    return {"classification": classification, "action": action}


def current_use_allowed(
    *,
    context_is_head: bool,
    delivery_not_superseded: bool,
    permission_current: bool | None,
    forget_clear: bool | None,
    scope_matches: bool,
    session_current: bool,
    capability_current: bool,
) -> bool:
    """Fail-closed G-local projection; booleans are externally verified inputs."""
    return all((
        context_is_head, delivery_not_superseded,
        permission_current is True, forget_clear is True,
        scope_matches, session_current, capability_current,
    ))
