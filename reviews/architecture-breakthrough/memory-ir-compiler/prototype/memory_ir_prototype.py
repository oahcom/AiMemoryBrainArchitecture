#!/usr/bin/env python3
"""Synthetic, standard-library-only Direct-vs-IR Memory Formation experiment.

This is a research harness, not a production compiler or a B-domain schema.
"""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "sample_experiences.json"
REQUIRED = ("source_id", "event_id", "subject", "predicate", "value", "text", "scope")
ALLOWED_EPISTEMIC = {"observed", "reported", "inferred", "verified", "disputed", "retracted"}
IR_VERSION = "0.1.0"
RULESET_VERSION = "rules-0.1.0"

def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

def direct_pipeline(rows):
    """A deliberately compact direct mapping: parse, qualify and write in one pass."""
    objects, errors = [], []
    for n, row in enumerate(rows, 1):
        missing = [k for k in REQUIRED if not row.get(k)]
        if missing:
            errors.append({"row": n, "error": "missing:" + ",".join(missing)})
            continue
        obj = {
            "subject": row["subject"], "predicate": row["predicate"], "value": row["value"],
            "valid_from": row.get("valid_from"), "valid_to": row.get("valid_to"),
            "epistemic": row.get("epistemic", "reported"),
            "confidence": row.get("confidence"), "scope": row["scope"],
            "evidence": [{"source_id": row["source_id"], "event_id": row["event_id"],
                          "source_digest": row.get("source_digest")}]
        }
        objects.append(obj)
    conflicts = detect_conflicts(objects)
    return {"objects": objects, "errors": errors, "conflicts": conflicts}

def parse_to_ir(rows):
    """Create an immutable-ish, typed candidate envelope without resolving canonical IDs."""
    ir, diagnostics = [], []
    for n, row in enumerate(rows, 1):
        missing = [k for k in REQUIRED if not row.get(k)]
        if missing:
            diagnostics.append({"stage": "parse", "row": n, "code": "IR001",
                                "message": "required source/evidence fields missing", "fields": missing})
            continue
        epistemic = row.get("epistemic", "reported")
        if epistemic not in ALLOWED_EPISTEMIC:
            diagnostics.append({"stage": "typecheck", "row": n, "code": "IR002",
                                "message": "unknown epistemic value", "value": epistemic})
            continue
        ir.append({
            "ir_version": IR_VERSION, "node_id": "node-" + digest(row)[:12],
            "node_kind": "assertion_candidate",
            "typed_value": {"subject": {"type": "entity_mention", "value": row["subject"]},
                            "predicate": {"type": "predicate", "value": row["predicate"]},
                            "object": {"type": "literal", "value": row["value"]}},
            "qualification": {"epistemic": epistemic, "confidence": row.get("confidence"),
                              "valid_time": {"from": row.get("valid_from"), "to": row.get("valid_to")},
                              "scope": row["scope"], "authority": row.get("authority", "unknown")},
            "evidence": [{"source_id": row["source_id"], "event_id": row["event_id"],
                          "source_digest": row.get("source_digest"), "quote": row["text"]}],
            "provenance": {"extractor": "synthetic-rule-extractor", "extractor_version": "1",
                           "ruleset_version": RULESET_VERSION, "input_digest": digest(row)}
        })
    return ir, diagnostics

def semantic_validate(ir):
    valid, diagnostics = [], []
    for node in ir:
        q = node["qualification"]
        if not node["evidence"] or not node["provenance"].get("input_digest"):
            diagnostics.append({"stage": "semantic", "node_id": node["node_id"], "code": "IR003",
                                "message": "evidence/provenance required"})
            continue
        if q["confidence"] is not None and not (0 <= q["confidence"] <= 1):
            diagnostics.append({"stage": "semantic", "node_id": node["node_id"], "code": "IR004",
                                "message": "confidence outside [0,1]"})
            continue
        if q["valid_time"]["from"] and q["valid_time"]["to"] and q["valid_time"]["to"] < q["valid_time"]["from"]:
            diagnostics.append({"stage": "semantic", "node_id": node["node_id"], "code": "IR005",
                                "message": "invalid temporal interval"})
            continue
        valid.append(node)
    return valid, diagnostics

def normalize_and_lower(ir):
    """Lower IR to a research target shape; entity resolution is intentionally not performed."""
    out = []
    for node in ir:
        t, q = node["typed_value"], node["qualification"]
        out.append({
            "subject_mention": t["subject"]["value"], "predicate": t["predicate"]["value"],
            "value": t["object"]["value"], "valid_from": q["valid_time"]["from"],
            "valid_to": q["valid_time"]["to"], "epistemic": q["epistemic"],
            "confidence": q["confidence"], "scope": q["scope"], "authority": q["authority"],
            "evidence": copy.deepcopy(node["evidence"]), "provenance": copy.deepcopy(node["provenance"]),
            "ir_version": node["ir_version"], "node_id": node["node_id"]
        })
    return out

def detect_conflicts(objects):
    """Conservative same-subject/predicate/scope + overlapping-valid-time conflict proposal."""
    found = []
    for i, a in enumerate(objects):
        for b in objects[i+1:]:
            if (a["subject"] if "subject" in a else a["subject_mention"]) != (b["subject"] if "subject" in b else b["subject_mention"]):
                continue
            if a["predicate"] != b["predicate"] or a["scope"] != b["scope"] or a["value"] == b["value"]:
                continue
            a0, b0 = a.get("valid_from"), b.get("valid_from")
            a1, b1 = a.get("valid_to"), b.get("valid_to")
            if a0 and b0 and (not a1 or b0 <= a1) and (not b1 or a0 <= b1):
                found.append({"left": a.get("node_id", digest(a)[:12]), "right": b.get("node_id", digest(b)[:12]),
                              "kind": "overlapping_value_disagreement", "disposition": "preserve_both_review"})
    return found

def run():
    rows = load()
    direct = direct_pipeline(rows)
    ir, parse_diag = parse_to_ir(rows)
    valid, semantic_diag = semantic_validate(ir)
    lowered = normalize_and_lower(valid)
    ir_objects = [{"subject_mention": x["subject_mention"], "predicate": x["predicate"], "value": x["value"],
                   "valid_from": x["valid_from"], "valid_to": x["valid_to"], "epistemic": x["epistemic"],
                   "confidence": x["confidence"], "scope": x["scope"], "evidence": x["evidence"],
                   "provenance": x["provenance"]} for x in lowered]
    ir_conflicts = detect_conflicts(lowered)
    # Re-run byte-equivalent transformation; IDs and output digests should remain stable.
    ir2, d2 = parse_to_ir(rows)
    valid2, d22 = semantic_validate(ir2)
    lowered2 = normalize_and_lower(valid2)
    deterministic = digest(lowered) == digest(lowered2) and parse_diag == d2 and semantic_diag == d22
    # A single-source edit: unaffected source rows retain identical IR node IDs.
    changed = copy.deepcopy(rows)
    changed[2]["confidence"] = 0.96
    ir_changed, _ = parse_to_ir(changed)
    old_by_src = {n["evidence"][0]["source_id"]: n["node_id"] for n in ir}
    new_by_src = {n["evidence"][0]["source_id"]: n["node_id"] for n in ir_changed}
    unaffected = [k for k in old_by_src if k != "src-003" and k in new_by_src and old_by_src[k] == new_by_src[k]]
    total_sources = len({r["source_id"] for r in rows if r.get("source_id")})
    direct_prov = sum(bool(o.get("evidence")) for o in direct["objects"])
    ir_prov = sum(bool(o.get("evidence")) and bool(o.get("provenance")) for o in lowered)
    result = {
        "experiment": "synthetic-direct-vs-ir", "ir_version": IR_VERSION, "ruleset_version": RULESET_VERSION,
        "input_rows": len(rows), "accepted_direct": len(direct["objects"]), "accepted_ir": len(lowered),
        "metrics": {
            "provenance_completeness": {"direct_evidence_coverage": f"{direct_prov}/{len(direct['objects'])}",
                                        "ir_evidence_plus_lineage_coverage": f"{ir_prov}/{len(lowered)}"},
            "type_validation": {"direct_errors": len(direct["errors"]), "ir_diagnostics": len(parse_diag)+len(semantic_diag)},
            "conflict_detection": {"direct": len(direct["conflicts"]), "ir": len(ir_conflicts)},
            "reprocessing_determinism": deterministic,
            "incremental_processing": {"unchanged_source_nodes_reused": len(unaffected), "eligible_unchanged_sources": total_sources-1},
            "schema_evolution": "raw input retained; IR version stamped; migration policy not implemented in prototype",
            "error_localization": {"direct": direct["errors"], "ir": parse_diag+semantic_diag},
            "processing_cost": {"direct_passes": 1, "ir_passes": 3, "model_calls": 0},
            "data_loss": {"direct_valid_records": len(direct["objects"]), "ir_valid_records": len(lowered),
                          "rejected_rows_retained_as_diagnostics": len(parse_diag)+len(semantic_diag)}
        },
        "direct": direct, "ir_diagnostics": parse_diag+semantic_diag, "ir_lowered": lowered,
        "ir_conflicts": ir_conflicts
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    run()
