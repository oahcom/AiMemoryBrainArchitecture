"""TEST-profile owner snapshot semantic validator for H Unified 1.2.17.

All cryptographic, live-ledger, pagination and anti-rollback authorities are
injected. No production trust is implied.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Callable, Mapping

VALID, INVALID, UNKNOWN = "VALID", "INVALID", "UNKNOWN"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DECIMAL = re.compile(r"^(0|[1-9][0-9]*)$")
MAX_D_TYPED_HIGH_WATER = (1 << 63) - 1
D_SIGNED_64_HIGH_WATER_FIELDS = frozenset({
    "producer_registration_high_water",
    "work_item_high_water",
    "attempt_high_water",
    "barrier_generation",
    "forget_fence_generation_high_water",
})


def _is_canonical_decimal(value: str) -> bool:
    """Accept only the canonical unsigned decimal wire form; never rewrite signed bytes."""
    return isinstance(value, str) and DECIMAL.fullmatch(value) is not None


def _canonical_d_high_water(value: str) -> str | None:
    """Parse one D nominal high-water and return its canonical decimal projection."""
    if not isinstance(value, str) or re.fullmatch(r"[0-9]+", value) is None:
        return None
    number = int(value)
    if number > MAX_D_TYPED_HIGH_WATER:
        return None
    return str(number)

D_BOUNDED_STRING_FIELDS = frozenset({
    "producer_registration_high_water",
    "work_item_high_water",
    "attempt_high_water",
    "barrier_generation",
    "forget_fence_generation_high_water",
    "dependency_closure_cursor",
})

OWNER_FIELDS = {
    "I": {
        "receipt_issue_high_water", "receipt_consume_high_water", "permission_epoch",
        "producer_domain_inventory_epoch_ref", "registry_snapshot_digest", "relevant_entry_set_root",
    },
    "D": {
        "producer_registration_high_water", "work_item_high_water", "attempt_high_water",
        "barrier_generation", "barrier_root", "forget_fence_generation_high_water",
        "dependency_closure_cursor", "dependency_closure_root",
    },
    "C": {
        "reservation_high_water", "provider_attempt_high_water", "provider_outcome_high_water",
        "provider_idempotency_namespace_ref", "final_request_boundary_generation",
    },
}


def _td(domain: str, value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(("BMCP-" + domain + "-TEST-v1|").encode("ascii") + raw).hexdigest()


def validate_owner_snapshot_1_2_17(
    snapshot: Mapping,
    owner: str,
    *,
    verify_attestation: Callable | None = None,
    verify_ledger_currentness: Callable | None = None,
    verify_anti_rollback: Callable | None = None,
) -> str:
    if not isinstance(snapshot, Mapping):
        return UNKNOWN
    if owner not in OWNER_FIELDS or snapshot.get("owner") != owner:
        return INVALID

    required = {
        "owner", "owner_gate_ref", "owner_gate_generation", "scope_generation_ref",
        "request_high_water", "request_count", "request_set_digest", "request_ledger_root",
        "admission_high_water", "admission_count", "admission_set_digest", "admission_ledger_root",
        "owner_snapshot_ref", "owner_snapshot_digest", "owner_snapshot_attestation_ref",
        "owner_snapshot_attestation_digest", "owner_ledger_root", "anti_rollback_anchor_ref",
        "owner_specific_high_waters", "owner_specific_high_waters_digest",
    }
    if any(k not in snapshot or snapshot[k] is None or snapshot[k] == "" for k in required):
        return UNKNOWN

    values = snapshot.get("owner_specific_high_waters")
    if not isinstance(values, Mapping) or set(values) != OWNER_FIELDS[owner]:
        return INVALID
    if owner == "D" and any(
        not isinstance(values.get(field), str)
        or not 1 <= len(values[field]) <= 512
        for field in D_BOUNDED_STRING_FIELDS
    ):
        return INVALID
    if any(not isinstance(v, str) or not v for v in values.values()):
        return INVALID

    numeric_fields = {
        "request_high_water", "request_count", "admission_high_water", "admission_count",
        "owner_gate_generation",
    }
    if any(not isinstance(snapshot[k], str) or not DECIMAL.fullmatch(snapshot[k]) for k in numeric_fields):
        return INVALID

    for key in ("request_set_digest", "request_ledger_root", "admission_set_digest",
                "admission_ledger_root", "owner_snapshot_digest", "owner_snapshot_attestation_digest",
                "owner_ledger_root", "owner_specific_high_waters_digest"):
        if not isinstance(snapshot[key], str) or not HEX64.fullmatch(snapshot[key]):
            return INVALID

    digest_projection = dict(values)
    for key, value in values.items():
        if key.endswith("digest") or key.endswith("_root"):
            if not HEX64.fullmatch(value):
                return INVALID
        if key.endswith("_high_water") or key.endswith("_generation"):
            if key in D_SIGNED_64_HIGH_WATER_FIELDS:
                # D 1.3.1 §5.1 requires accepting leading zeroes, then
                # canonicalizing independently within this nominal type.
                # D-AUTH-QUERY-1.0 §2.2 bounds all five D numeric types.
                canonical_value = _canonical_d_high_water(value)
                if canonical_value is None:
                    return INVALID
                digest_projection[key] = canonical_value
            elif not _is_canonical_decimal(value):
                return INVALID

    if snapshot["owner_specific_high_waters_digest"] != _td("OWNER-SPECIFIC-HIGH-WATERS", digest_projection):
        return INVALID

    if not all(callable(x) for x in (verify_attestation, verify_ledger_currentness, verify_anti_rollback)):
        return UNKNOWN

    attestation = verify_attestation(snapshot, owner)
    if attestation is None or attestation == UNKNOWN:
        return UNKNOWN
    if attestation is not True:
        return INVALID

    anti_rollback = verify_anti_rollback(snapshot, owner)
    if anti_rollback is None or anti_rollback == UNKNOWN:
        return UNKNOWN
    if anti_rollback is not True:
        return INVALID

    current = verify_ledger_currentness(snapshot, owner)
    if current is None or current == UNKNOWN or current is not True:
        return UNKNOWN
    return VALID
