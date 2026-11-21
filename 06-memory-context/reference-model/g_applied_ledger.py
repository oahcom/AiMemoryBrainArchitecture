"""Executable reference model for G-owned Applied idempotency.

This is a conformance prototype, NOT production G runtime code. Callers must
supply independently authenticated evidence/gate results. It does not create
C, H, COC, I, D, or Storage authority and does not implement current-use
revalidation, distributed consensus, or multi-replica fencing.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any, Mapping


IDENTITY_FIELDS = (
    "context_id",
    "context_version",
    "delivery_id",
    "delivery_attempt_id",
    "inference_request_id",
    "final_request_boundary_id",
    "provider_attempt_ref",
    "h_delivery_binding_ref",
    "coc_participant_ref",
)
REQUIRED_GATES = (
    "c_outcome_authenticated",
    "h_evidence_authenticated",
    "coc_terminal_proof_valid",
    "i_authorization_current",
    "d_forget_fence_clear",
    "storage_terminal_resolution_valid",
    "g_context_delivery_current",
)


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("value is not canonical JSON data") from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


class GAppliedLedger:
    """Single-node SQLite reference ledger with durable unique identity."""

    def __init__(self, database: str | Path):
        self.database = str(database)
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS applied (
                    identity_key TEXT PRIMARY KEY,
                    identity_json BLOB NOT NULL,
                    evidence_digest TEXT NOT NULL,
                    evidence_json BLOB NOT NULL,
                    record_id INTEGER NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS conflicts (
                    identity_key TEXT NOT NULL,
                    conflicting_evidence_digest TEXT NOT NULL,
                    evidence_json BLOB NOT NULL,
                    PRIMARY KEY (identity_key, conflicting_evidence_digest)
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.database, timeout=10, isolation_level=None)
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=10000")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def evaluate(
        self,
        identity: Mapping[str, Any],
        c_outcome: str,
        evidence: Mapping[str, Any],
        gates: Mapping[str, bool],
    ) -> dict[str, Any]:
        if not isinstance(identity, Mapping) or set(identity) != set(IDENTITY_FIELDS):
            raise ValueError("identity must contain exactly the nine declared GApplied identity fields")
        if any(not isinstance(identity[k], str) or not identity[k] for k in IDENTITY_FIELDS):
            raise ValueError("all GApplied identity fields must be non-empty strings")
        if not isinstance(evidence, Mapping) or not evidence:
            raise ValueError("evidence must be a non-empty mapping")

        # Non-success C outcomes can never create a Full Applied record.
        if c_outcome != "HANDOFF_ACCEPTED":
            return {"status": "BLOCKED", "reason": "C outcome is not HANDOFF_ACCEPTED"}

        if not isinstance(gates, Mapping) or set(gates) != set(REQUIRED_GATES):
            return {"status": "BLOCKED", "reason": "complete exact gate set is required"}
        if any(type(gates[name]) is not bool for name in REQUIRED_GATES):
            return {"status": "BLOCKED", "reason": "gate results must be boolean"}
        if not all(gates[name] for name in REQUIRED_GATES):
            return {"status": "BLOCKED", "reason": "one or more required authority/evidence gates did not pass"}

        identity_json = _canonical(dict(identity))
        identity_key = _digest({
            "domain": "AIMBA-G-APPLIED-IDENTITY-v1",
            "identity": dict(identity),
        })
        evidence_record = {
            "c_outcome": c_outcome,
            "evidence": dict(evidence),
            "gates": dict(gates),
        }
        evidence_json = _canonical(evidence_record)
        evidence_digest = hashlib.sha256(evidence_json).hexdigest()

        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT record_id, evidence_digest FROM applied WHERE identity_key=?",
                (identity_key,),
            ).fetchone()
            if row:
                if row[1] == evidence_digest:
                    db.execute("COMMIT")
                    return {
                        "status": "IDEMPOTENT_REPLAY",
                        "record_id": row[0],
                        "identity_key": identity_key,
                        "evidence_digest": evidence_digest,
                    }
                db.execute(
                    "INSERT OR IGNORE INTO conflicts(identity_key, conflicting_evidence_digest, evidence_json) VALUES (?, ?, ?)",
                    (identity_key, evidence_digest, evidence_json),
                )
                db.execute("COMMIT")
                return {
                    "status": "CONFLICT",
                    "record_id": row[0],
                    "identity_key": identity_key,
                    "original_evidence_digest": row[1],
                    "conflicting_evidence_digest": evidence_digest,
                }

            cursor = db.execute(
                "INSERT INTO applied(identity_key, identity_json, evidence_digest, evidence_json, record_id) VALUES (?, ?, ?, ?, (SELECT COALESCE(MAX(record_id), 0)+1 FROM applied))",
                (identity_key, identity_json, evidence_digest, evidence_json),
            )
            record_id = db.execute(
                "SELECT record_id FROM applied WHERE identity_key=?", (identity_key,)
            ).fetchone()[0]
            db.execute("COMMIT")
            return {
                "status": "FULL_APPLIED",
                "record_id": record_id,
                "identity_key": identity_key,
                "evidence_digest": evidence_digest,
            }
        except Exception:
            if db.in_transaction:
                db.execute("ROLLBACK")
            raise
        finally:
            db.close()

    def read(self, identity: Mapping[str, Any]) -> dict[str, Any] | None:
        if not isinstance(identity, Mapping) or set(identity) != set(IDENTITY_FIELDS):
            raise ValueError("identity must contain exactly the nine declared GApplied identity fields")
        key = _digest({"domain": "AIMBA-G-APPLIED-IDENTITY-v1", "identity": dict(identity)})
        with closing(self._connect()) as db:
            row = db.execute(
                "SELECT record_id, identity_json, evidence_digest, evidence_json FROM applied WHERE identity_key=?",
                (key,),
            ).fetchone()
        if row is None:
            return None
        return {
            "record_id": row[0],
            "identity": json.loads(row[1]),
            "evidence_digest": row[2],
            "evidence": json.loads(row[3]),
        }

    def conflict_count(self, identity: Mapping[str, Any]) -> int:
        key = _digest({"domain": "AIMBA-G-APPLIED-IDENTITY-v1", "identity": dict(identity)})
        with closing(self._connect()) as db:
            return db.execute(
                "SELECT COUNT(*) FROM conflicts WHERE identity_key=?", (key,)
            ).fetchone()[0]
