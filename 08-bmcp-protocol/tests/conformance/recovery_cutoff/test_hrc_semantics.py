"""Executable semantic conformance vectors HRC-01..25 for BMCP recovery-cutoff 1.0.4.

Run:
    python -m unittest -v test_hrc_semantics.py

This is a dependency-free semantic test harness over normalized 1.0.4 message models.
It deliberately does NOT claim cryptographic verification or freeze canonical bytes.
The digest helper below is TEST-ONLY; production canonicalization/signature verification
must be injected from the H-approved profile and I-approved trust policy.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from copy import deepcopy


VALID, INVALID, UNKNOWN, STALE, CONFLICT = (
    "VALID", "INVALID", "UNKNOWN", "STALE", "CONFLICT"
)

# TEST-ONLY deterministic digest. Not a normative production wire profile.
def test_digest(value, domain="HRC-TEST-v1"):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256((domain + "\0").encode() + raw).hexdigest()


def owner_snapshot(owner="I", requests=None, admissions=None, highwaters=None,
                   complete=True, ledger_available=True, pagination_complete=True):
    requests = [] if requests is None else requests
    admissions = [] if admissions is None else admissions
    defaults = {
        "I": {"receipt_issue": 0, "receipt_consume": 0, "producer_domain_inventory_epoch": 0},
        "D": {"producer_registration": 0, "work_item": 0, "attempt": 0, "barrier": 0},
        "C": {"reservation": 0, "provider_attempt": 0},
    }[owner]
    if highwaters is not None:
        defaults.update(highwaters)
    return {
        "owner": owner, "gate_ref": owner + "/gate/1", "gate_generation": 1,
        "scope_ref": "scope/test", "scope_generation": 1, "snapshot_generation": 1,
        "anti_rollback_anchor": owner + "/anchor/1",
        "request_entries": deepcopy(requests), "admission_entries": deepcopy(admissions),
        "request_count": len(requests), "admission_count": len(admissions),
        "request_root": test_digest(requests, "owner-request-set"),
        "admission_root": test_digest(admissions, "owner-admission-set"),
        "request_highwaters": deepcopy(defaults), "admission_highwaters": deepcopy(defaults),
        "completeness": "COMPLETE" if complete else "PARTIAL",
        "request_enumeration_status": ("COMPLETE_EMPTY" if not requests else "COMPLETE_NON_EMPTY") if complete else "PARTIAL",
        "admission_enumeration_status": ("COMPLETE_EMPTY" if not admissions else "COMPLETE_NON_EMPTY") if complete else "PARTIAL",
        "ledger_available": ledger_available, "pagination_complete": pagination_complete,
        "signature_valid": True, "key_current": True, "schema_version": "1.0.0",
    }


def admission(ref, owner, status="REGISTERED", participant_ref="COC/P1",
              participant_entry_digest="c" * 64, position=1, seq=1):
    item = {
        "owner_entry_ref": ref + "/row", "owner_admission_ref": ref, "owner_entry_kind": "RECEIPT_ISSUE", "owner": owner,
        "operation_id": "op/" + ref, "operation_digest": "b" * 64,
        "scope_ref": "scope/test", "sequence": seq, "status": status,
    }
    if status == "REGISTERED":
        item.update({"participant_intent_ref": participant_ref,
                     "participant_entry_digest": participant_entry_digest,
                     "participant_position": position})
    return item


def participant(ref="COC/P1", owner="C", admission_ref="C/admit/1",
                digest="a" * 64, position=1, required=("C", "I", "D")):
    return {
        "participant_intent_ref": ref, "owner_kind": owner,
        "owner_admission_ref": admission_ref, "primary_owner_entry_ref": admission_ref + "/row", "operation_id": "op/C/admit/1",
        "operation_digest": "b" * 64, "participant_digest": digest, "scope_ref": "scope/test",
        "term": 1, "index": position, "entry_digest": "c" * 64,
        "required_owner_evidence": list(required),
        "owner_evidence": {"C": ["C/admit/1/row"], "I": ["I/receipt/1/row"], "D": ["D/barrier/1/row"]},
    }


def manifest(entries=None, complete=True, quorum=True, prefix=(1, 10, "d" * 64)):
    entries = [] if entries is None else entries
    return {
        "manifest_id": "manifest/1", "recovery_epoch": "epoch/1",
        "prefix": {"term": prefix[0], "index": prefix[1], "root": prefix[2]},
        "entries": deepcopy(entries), "count": len(entries),
        "authoritative_prefix_entries": deepcopy(entries),
        "root": test_digest(entries, "participant-set"),
        "enumeration_complete": complete, "quorum_read": quorum,
        "cursor_complete": complete, "signature_valid": True,
    }


def batch(snaps=None, man=None):
    snaps = snaps or {x: owner_snapshot(x) for x in ("I", "D", "C")}
    man = man or manifest()
    return {
        "batch_id": "batch/1", "recovery_epoch": "epoch/1", "round": 1,
        "previous_batch_digest": "0" * 64,
        "snapshots": {k: {"ref": k + "/snapshot/1", "digest": test_digest(v, "snapshot"),
                          "value": deepcopy(v)} for k, v in snaps.items()},
        "manifest_ref": man["manifest_id"], "manifest_digest": test_digest(man, "manifest-record"),
        "manifest": deepcopy(man), "prefix": deepcopy(man["prefix"]),
        "quorum_proof_valid": True, "append_after_prefix": True,
        "scope_ref": "scope/test", "scope_complete": True,
    }


def release(owner="I", b=None, current=None, manifest_value=None):
    b = b or batch()
    current = current or b["snapshots"][owner]["value"]
    return {
        "owner": owner, "issuer_is_owner": True, "signature_valid": True,
        "gate_ref": current["gate_ref"], "gate_generation": current["gate_generation"],
        "scope_ref": current["scope_ref"], "scope_generation": current["scope_generation"],
        "request_highwaters": deepcopy(current["request_highwaters"]),
        "admission_highwaters": deepcopy(current["admission_highwaters"]),
        "request_root": current["request_root"], "admission_root": current["admission_root"],
        "batch_id": b["batch_id"], "manifest_ref": b["manifest_ref"],
        "manifest_digest": b["manifest_digest"], "snapshot_generation": current["snapshot_generation"],
        "anti_rollback_anchor": current["anti_rollback_anchor"],
        "cas_succeeded": True, "obligations_terminal": True, "release_kind": "OUTAGE_ADMISSION_RELEASE_ONLY",
    }


def validate_snapshot(s):
    if not s.get("signature_valid") or not s.get("key_current"):
        return UNKNOWN
    if not s.get("ledger_available") or not s.get("pagination_complete"):
        return UNKNOWN
    if s.get("completeness") != "COMPLETE":
        return UNKNOWN
    for name in ("request_entries", "admission_entries"):
        entries = s.get(name)
        if not isinstance(entries, list):
            return INVALID
        count_name = "request_count" if name.startswith("request") else "admission_count"
        root_name = "request_root" if name.startswith("request") else "admission_root"
        if s.get(count_name) != len(entries):
            return INVALID
        refs = [x.get("owner_entry_ref") for x in entries]
        if None in refs or len(refs) != len(set(refs)):
            return INVALID
        if refs != sorted(refs, key=lambda x: (next((e.get("sequence", 0) for e in entries if e["owner_entry_ref"] == x), 0), x)):
            return INVALID
        if s.get(root_name) != test_digest(entries, "owner-request-set" if name.startswith("request") else "owner-admission-set"):
            return INVALID
        status_name = "request_enumeration_status" if name.startswith("request") else "admission_enumeration_status"
        state = s.get(status_name)
        if state not in {"COMPLETE_EMPTY", "COMPLETE_NON_EMPTY"}:
            return UNKNOWN
        if state == "COMPLETE_EMPTY" and entries:
            return INVALID
        if state == "COMPLETE_NON_EMPTY" and not entries:
            return INVALID
        if name.startswith("request") and any(e.get("owner_entry_kind") != "REQUEST" for e in entries):
            return INVALID
        if name.startswith("admission") and any(e.get("owner_entry_kind") == "REQUEST" for e in entries):
            return INVALID
    owner = s.get("owner")
    required = {
        "I": {"receipt_issue", "receipt_consume", "producer_domain_inventory_epoch"},
        "D": {"producer_registration", "work_item", "attempt", "barrier"},
        "C": {"reservation", "provider_attempt"},
    }.get(owner)
    if required is None:
        return INVALID
    for key in ("request_highwaters", "admission_highwaters"):
        if not required.issubset(set(s.get(key, {}))):
            return INVALID
    for entries_name, hw_name in (("request_entries", "request_highwaters"),
                                  ("admission_entries", "admission_highwaters")):
        entries = s[entries_name]
        for e in entries:
            seq = e.get("sequence")
            if not isinstance(seq, int) or seq < 0:
                return INVALID
            # Owner-specific sequence namespace is explicit on each entry.
            namespace = e.get("sequence_namespace")
            if namespace and namespace in s[hw_name] and seq > s[hw_name][namespace]:
                return INVALID
    return VALID


def validate_manifest(m):
    if not m.get("signature_valid"):
        return UNKNOWN
    if not m.get("quorum_read") or not m.get("enumeration_complete") or not m.get("cursor_complete"):
        return UNKNOWN
    entries = m.get("entries")
    if not isinstance(entries, list):
        return INVALID
    if m.get("count") != len(entries):
        return INVALID
    refs = [e.get("participant_intent_ref") for e in entries]
    positions = [(e.get("term"), e.get("index")) for e in entries]
    if None in refs or len(refs) != len(set(refs)) or len(positions) != len(set(positions)):
        return INVALID
    if refs != sorted(refs):
        return INVALID
    for e in entries:
        if not e.get("owner_admission_ref") or not e.get("participant_digest"):
            return INVALID
        if e.get("index", 0) > m["prefix"]["index"]:
            return INVALID
        if not e.get("entry_digest") or not e.get("operation_digest"):
            return INVALID
    if m.get("root") != test_digest(entries, "participant-set"):
        return INVALID
    authoritative = m.get("authoritative_prefix_entries")
    if authoritative is None:
        return UNKNOWN
    authoritative_by_ref = {e.get("participant_intent_ref"): e.get("entry_digest") for e in authoritative}
    manifest_by_ref = {e.get("participant_intent_ref"): e.get("entry_digest") for e in entries}
    if authoritative_by_ref != manifest_by_ref:
        return INVALID
    return VALID


def validate_batch(b):
    if not b.get("quorum_proof_valid") or not b.get("append_after_prefix"):
        return UNKNOWN
    if set(b.get("snapshots", {})) != {"I", "D", "C"}:
        return INVALID
    for owner, item in b["snapshots"].items():
        if test_digest(item.get("value"), "snapshot") != item.get("digest"):
            return INVALID
        result = validate_snapshot(item.get("value", {}))
        if result != VALID:
            return result
    m = b.get("manifest")
    result = validate_manifest(m or {})
    if result != VALID:
        return result
    if b.get("manifest_ref") != m.get("manifest_id"):
        return INVALID
    if b.get("manifest_digest") != test_digest(m, "manifest-record"):
        return INVALID
    if b.get("prefix") != m.get("prefix") or not b.get("scope_complete"):
        return INVALID
    return VALID


def request_entry(row_ref, owner, request_ref=None, digest="d" * 64, seq=1):
    return {"owner_entry_ref": row_ref, "owner_entry_kind": "REQUEST", "owner": owner,
            "request_ref": request_ref or ("request/" + row_ref), "request_digest": digest, "entry_digest": "e" * 64,
            "sequence": seq, "scope_ref": "scope/test"}


def validate_request_dispositions(requests_by_owner, dispositions_by_owner):
    required_owners = {"I", "D", "C"}
    if set(requests_by_owner) != required_owners or set(dispositions_by_owner) != required_owners:
        return UNKNOWN
    for owner in required_owners:
        rows = requests_by_owner[owner]
        edges = dispositions_by_owner[owner]
        row_map = {x.get("owner_entry_ref"): x for x in rows}
        edge_map = {x.get("owner_entry_ref"): x for x in edges}
        if len(row_map) != len(rows) or len(edge_map) != len(edges) or None in row_map or None in edge_map:
            return INVALID
        if set(row_map) != set(edge_map):
            return INVALID
        for row_ref, row in row_map.items():
            edge = edge_map[row_ref]
            if (edge.get("owner_kind") != owner or
                edge.get("owner_request_ref") != row.get("request_ref") or
                edge.get("owner_request_digest") != row.get("request_digest") or
                edge.get("owner_entry_digest") != row.get("entry_digest") or
                edge.get("owner_sequence") != row.get("sequence") or
                edge.get("scope_ref") != row.get("scope_ref")):
                return INVALID
            if edge.get("disposition") == "OUT_OF_SCOPE_WITH_PROOF":
                if not edge.get("proof_ref") or not edge.get("owner_signature_valid"):
                    return INVALID
            elif edge.get("disposition") == "IN_BATCH_REQUEST_SET":
                if not edge.get("owner_signature_valid"):
                    return UNKNOWN
            else:
                return INVALID
    return VALID

def validate_join(admissions_by_owner, m):
    mr = validate_manifest(m)
    if mr != VALID:
        return mr
    entries = {e["participant_intent_ref"]: e for e in m["entries"]}
    seen_admissions = set()
    # Owner Admission -> COC ParticipantManifest direction.
    for owner, admissions in admissions_by_owner.items():
        for a in admissions:
            ref = a.get("owner_entry_ref")
            if (owner, ref) in seen_admissions:
                return INVALID
            seen_admissions.add((owner, ref))
            if a.get("status") == "NOT_REGISTERED":
                if any(k in a for k in ("participant_intent_ref", "participant_entry_digest", "participant_position")):
                    return INVALID
                if a.get("protected_effect_occurred") or not a.get("no_effect_or_pending_proof"):
                    return UNKNOWN
                continue
            if a.get("status") != "REGISTERED":
                return UNKNOWN
            p = entries.get(a.get("participant_intent_ref"))
            if p is None:
                return INVALID
            if (p.get("entry_digest") != a.get("participant_entry_digest") or
                p.get("index") != a.get("participant_position") or
                p.get("operation_id") != a.get("operation_id") or
                p.get("operation_digest") != a.get("operation_digest") or
                p.get("scope_ref") != a.get("scope_ref") or
                p.get("participant_intent_ref") != a.get("participant_intent_ref")):
                return INVALID
            # C admission is the primary manifest anchor; I/D evidence may be many-to-one.
            if owner == "C" and p.get("owner_admission_ref") != a.get("owner_admission_ref"):
                return INVALID
            refs = p.get("owner_evidence", {}).get(owner, [])
            if ref not in refs:
                return INVALID
    # COC ParticipantManifest -> accountable owner evidence direction.
    for p in m["entries"]:
        c_entries = admissions_by_owner.get("C")
        if c_entries is None:
            return UNKNOWN
        owner_entry = next((a for a in c_entries
                            if a.get("owner_admission_ref") == p.get("owner_admission_ref")), None)
        if owner_entry is None or owner_entry.get("status") != "REGISTERED":
            return UNKNOWN
        if owner_entry.get("owner_entry_ref") != p.get("primary_owner_entry_ref"):
            return INVALID
        if owner_entry.get("participant_intent_ref") != p.get("participant_intent_ref"):
            return INVALID
        for required in p.get("required_owner_evidence", []):
            refs = p.get("owner_evidence", {}).get(required, [])
            if not refs:
                return UNKNOWN
            if required not in admissions_by_owner:
                return UNKNOWN
            known = {a.get("owner_entry_ref") for a in admissions_by_owner[required]}
            if any(ref not in known for ref in refs):
                return UNKNOWN
    return VALID


def validate_release(r, current, b):
    if r.get("owner") not in {"I", "D", "C"} or not r.get("issuer_is_owner"):
        return INVALID
    if not r.get("signature_valid"):
        return UNKNOWN
    if r.get("batch_id") != b.get("batch_id") or r.get("manifest_ref") != b.get("manifest_ref") or r.get("manifest_digest") != b.get("manifest_digest"):
        return INVALID
    if r.get("gate_ref") != current.get("gate_ref") or r.get("gate_generation") != current.get("gate_generation"):
        return STALE
    if r.get("scope_ref") != current.get("scope_ref") or r.get("scope_generation") != current.get("scope_generation"):
        return STALE
    for k in ("request_highwaters", "admission_highwaters", "request_root", "admission_root", "snapshot_generation", "anti_rollback_anchor"):
        if r.get(k) != current.get(k):
            return STALE
    if not r.get("cas_succeeded") or not r.get("obligations_terminal"):
        return UNKNOWN
    if r.get("release_kind") != "OUTAGE_ADMISSION_RELEASE_ONLY":
        return INVALID
    return VALID


def validate_epoch_completed(releases, b):
    if set(releases) != {"I", "D", "C"}:
        return INVALID
    for owner, r in releases.items():
        if r.get("owner") != owner:
            return INVALID
        result = validate_release(r, b["snapshots"][owner]["value"], b)
        if result != VALID:
            return result
    return VALID


def validate_jf10(i_terminal, storage_terminal, same_tuple=True):
    if not same_tuple:
        return INVALID
    if i_terminal == "COMMIT_WON" and storage_terminal == "COMMITTED":
        return VALID
    if i_terminal in {"REVOCATION_WON", "INDETERMINATE_ABORTED"} and storage_terminal == "ROLLED_BACK":
        return VALID
    if i_terminal in {"UNKNOWN", "IN_DOUBT"} or storage_terminal in {"UNKNOWN", "IN_DOUBT", "PENDING"}:
        return UNKNOWN
    return INVALID


class HRCConformance(unittest.TestCase):
    def setUp(self):
        self.snaps = {x: owner_snapshot(x) for x in ("I", "D", "C")}
        self.man = manifest()
        self.b = batch(self.snaps, self.man)

    # HRC-01: all request/admission sets explicitly complete-empty.
    def test_HRC_01(self):
        for owner in ("I", "D", "C"):
            self.assertEqual(validate_snapshot(owner_snapshot(owner)), VALID)

    # HRC-02: empty request set and non-empty admission set are independent.
    def test_HRC_02(self):
        s = owner_snapshot("C", admissions=[admission("C/a1", "C")])
        self.assertEqual(validate_snapshot(s), VALID)

    # HRC-03: absent/null or contradictory empty representation is invalid.
    def test_HRC_03(self):
        s = owner_snapshot("I"); s["request_entries"] = None
        self.assertEqual(validate_snapshot(s), INVALID)
        s = owner_snapshot("I"); s["request_entries"] = [admission("I/a", "I")]
        s["request_count"] = 0
        self.assertEqual(validate_snapshot(s), INVALID)

    # HRC-04: zero count with unavailable/partial ledger is UNKNOWN, never EMPTY.
    def test_HRC_04(self):
        s = owner_snapshot("I", ledger_available=False)
        self.assertEqual(validate_snapshot(s), UNKNOWN)

    # HRC-05: count differs from materialized array length.
    def test_HRC_05(self):
        s = owner_snapshot("I"); s["request_count"] = 1
        self.assertEqual(validate_snapshot(s), INVALID)

    # HRC-06: duplicate identity or noncanonical ordering.
    def test_HRC_06(self):
        a = admission("I/a", "I", seq=1); b = admission("I/b", "I", seq=2)
        s = owner_snapshot("I", admissions=[b, a])
        s["admission_count"] = 2
        s["admission_root"] = test_digest([b, a], "owner-admission-set")
        self.assertEqual(validate_snapshot(s), INVALID)
        s = owner_snapshot("I", admissions=[a, a])
        self.assertEqual(validate_snapshot(s), INVALID)

    # HRC-07: I must expose receipt issue, consume and inventory epoch high-waters.
    def test_HRC_07(self):
        s = owner_snapshot("I"); del s["request_highwaters"]["receipt_consume"]
        self.assertEqual(validate_snapshot(s), INVALID)

    # HRC-08: D must expose producer registration, work, attempt and barrier high-waters.
    def test_HRC_08(self):
        s = owner_snapshot("D"); del s["admission_highwaters"]["barrier"]
        self.assertEqual(validate_snapshot(s), INVALID)

    # HRC-09: C must expose reservation and provider-attempt high-waters.
    def test_HRC_09(self):
        s = owner_snapshot("C"); del s["request_highwaters"]["provider_attempt"]
        self.assertEqual(validate_snapshot(s), INVALID)

    # HRC-10: missing prefix page/segment or stale follower is UNKNOWN.
    def test_HRC_10(self):
        m = manifest(complete=False)
        self.assertEqual(validate_manifest(m), UNKNOWN)
        m = manifest(); m["quorum_read"] = False
        self.assertEqual(validate_manifest(m), UNKNOWN)

    # HRC-11: omitting a committed participant invalidates the manifest root/count.
    def test_HRC_11(self):
        p = participant()
        m = manifest([p]); m["entries"] = []; m["count"] = 0
        self.assertEqual(validate_manifest(m), INVALID)

    # HRC-12: REGISTERED admission must join exact participant digest and position.
    def test_HRC_12(self):
        p = participant()
        m = manifest([p])
        a = admission("C/admit/1", "C", participant_entry_digest="f" * 64)
        self.assertEqual(validate_join({"C": [a]}, m), INVALID)

    # HRC-13: NOT_REGISTERED cannot fabricate a COC participant identity.
    def test_HRC_13(self):
        a = admission("C/a", "C", status="NOT_REGISTERED")
        a["no_effect_or_pending_proof"] = True
        a["participant_intent_ref"] = "COC/fake"
        self.assertEqual(validate_join({"C": [a]}, manifest()), INVALID)

    # HRC-14: a manifest participant without accountable owner evidence blocks as UNKNOWN.
    def test_HRC_14(self):
        p = participant(required=["C", "I", "D"])
        p["owner_evidence"] = {"C": ["C/admit/1/row"]}
        m = manifest([p])
        a = admission("C/admit/1", "C")
        self.assertEqual(validate_join({"C": [a]}, m), UNKNOWN)

    # HRC-15: every recovery batch requires I, D and C snapshots.
    def test_HRC_15(self):
        b = batch(self.snaps, self.man); del b["snapshots"]["D"]
        self.assertEqual(validate_batch(b), INVALID)

    # HRC-16: stale snapshot digest or wrong prefix root is invalid.
    def test_HRC_16(self):
        b = deepcopy(self.b); b["snapshots"]["I"]["digest"] = "f" * 64
        self.assertEqual(validate_batch(b), INVALID)
        b = deepcopy(self.b); b["prefix"]["root"] = "e" * 64
        self.assertEqual(validate_batch(b), INVALID)

    # HRC-17: any owner high-water/scope advance before release requires a new round.
    def test_HRC_17(self):
        current = deepcopy(self.snaps["I"]); current["gate_generation"] += 1
        self.assertEqual(validate_release(release("I", self.b), current, self.b), STALE)

    # HRC-18: COC cannot issue or impersonate an owner gate release.
    def test_HRC_18(self):
        r = release("I", self.b); r["issuer_is_owner"] = False
        self.assertEqual(validate_release(r, self.snaps["I"], self.b), INVALID)

    # HRC-19: epoch completion requires exactly one valid I, D and C release.
    def test_HRC_19(self):
        rel = {o: release(o, self.b) for o in ("I", "D")}
        self.assertEqual(validate_epoch_completed(rel, self.b), INVALID)

    # HRC-20: I COMMIT_WON cannot pair with Storage ROLLED_BACK.
    def test_HRC_20(self):
        self.assertEqual(validate_jf10("COMMIT_WON", "ROLLED_BACK"), INVALID)

    # HRC-21: I REVOCATION_WON cannot pair with Storage COMMITTED.
    def test_HRC_21(self):
        self.assertEqual(validate_jf10("REVOCATION_WON", "COMMITTED"), INVALID)

    # HRC-22: unknown/in-doubt on either authority remains unresolved.
    def test_HRC_22(self):
        self.assertEqual(validate_jf10("COMMIT_WON", "UNKNOWN"), UNKNOWN)
        self.assertEqual(validate_jf10("UNKNOWN", "COMMITTED"), UNKNOWN)

    # HRC-23: same identity and same digest is an idempotent replay.
    def test_HRC_23(self):
        def replay(old_id, old_digest, new_id, new_digest):
            return VALID if (old_id, old_digest) == (new_id, new_digest) else CONFLICT
        self.assertEqual(replay("msg/1", "a" * 64, "msg/1", "a" * 64), VALID)

    # HRC-24: same identity with changed digest is a conflict.
    def test_HRC_24(self):
        def replay(old_id, old_digest, new_id, new_digest):
            return VALID if (old_id, old_digest) == (new_id, new_digest) else CONFLICT
        self.assertEqual(replay("msg/1", "a" * 64, "msg/1", "b" * 64), CONFLICT)

    # HRC-25: unknown critical fields, downgrade, duplicate keys and null substitution fail.
    def test_HRC_25(self):
        def strict_wire(raw, version, critical_fields, allowed):
            try:
                pairs = json.loads(raw, object_pairs_hook=lambda p: reject_duplicates(p))
            except ValueError:
                return INVALID
            if version != "1.0.0" or not set(critical_fields).issubset(allowed):
                return INVALID
            if pairs.get("request_entries", "MISSING") is None:
                return INVALID
            return VALID

        def duplicate_json():
            return strict_wire('{"schema_version":"1.0.0","schema_version":"0.9.0"}',
                               "1.0.0", [], {"schema_version"})
        self.assertEqual(duplicate_json(), INVALID)
        self.assertEqual(strict_wire('{"request_entries":null}', "1.0.0", [], {"request_entries"}), INVALID)
        self.assertEqual(strict_wire('{"schema_version":"0.9.0"}', "0.9.0", [], {"schema_version"}), INVALID)
        self.assertEqual(strict_wire('{"schema_version":"1.0.0"}', "1.0.0", ["new_critical"], {"schema_version"}), INVALID)


    # JPF-01: owner-to-participant and participant-to-primary-C joins both resolve.
    def test_JPF_01(self):
        p = participant(required=["C"])
        a = admission("C/admit/1", "C")
        self.assertEqual(validate_join({"C": [a]}, manifest([p])), VALID)

    # JPF-02: two distinct I evidence entries may join one participant.
    def test_JPF_02(self):
        p = participant(required=["C", "I", "D"])
        p["owner_evidence"]["I"] = ["I/issue/1/row", "I/consume/1/row"]
        a = admission("C/admit/1", "C")
        i1 = admission("I/issue/1", "I")
        i2 = admission("I/consume/1", "I", seq=2)
        d1 = admission("D/barrier/1", "D")
        for x in (i1, i2, d1):
            x["operation_id"] = p["operation_id"]
            x["operation_digest"] = p["operation_digest"]
            x["scope_ref"] = p["scope_ref"]
        self.assertEqual(validate_join({"C": [a], "I": [i1, i2], "D": [d1]}, manifest([p])), VALID)

    # JPF-03: D evidence must be in the exact owner ledger.
    def test_JPF_03(self):
        p = participant(required=["C", "D"])
        p["owner_evidence"]["D"] = ["D/barrier/1/row"]
        a = admission("C/admit/1", "C")
        d1 = admission("D/barrier/1", "D")
        d1["operation_id"] = p["operation_id"]
        d1["operation_digest"] = p["operation_digest"]
        d1["scope_ref"] = p["scope_ref"]
        self.assertEqual(validate_join({"C": [a], "D": [d1]}, manifest([p])), VALID)

    # JPF-04: REGISTERED owner admission with no manifest participant is invalid.
    def test_JPF_04(self):
        a = admission("C/admit/1", "C")
        self.assertEqual(validate_join({"C": [a]}, manifest()), INVALID)

    # JPF-05: participant without primary C admission is unknown/quarantined.
    def test_JPF_05(self):
        p = participant()
        self.assertEqual(validate_join({"C": [], "I": [], "D": []}, manifest([p])), UNKNOWN)

    # JPF-06: NOT_REGISTERED must not carry any participant locator.
    def test_JPF_06(self):
        a = admission("C/a", "C", status="NOT_REGISTERED")
        a["no_effect_or_pending_proof"] = True
        a["participant_position"] = 1
        self.assertEqual(validate_join({"C": [a]}, manifest()), INVALID)

    # JPF-07: NOT_REGISTERED with possible effect and no no-effect proof blocks.
    def test_JPF_07(self):
        a = admission("C/a", "C", status="NOT_REGISTERED")
        self.assertEqual(validate_join({"C": [a]}, manifest()), UNKNOWN)

    # JPF-08: one owner admission identity cannot bind two participants.
    def test_JPF_08(self):
        # Isolate the duplicate-primary-admission invariant: unrelated I/D
        # evidence is deliberately not required in this vector.
        p1 = participant(ref="COC/P1", required=["C"])
        p2 = participant(ref="COC/P2", position=2, required=["C"])
        p2["owner_admission_ref"] = "C/admit/1"
        p2["entry_digest"] = "e" * 64
        a = admission("C/admit/1", "C")
        self.assertEqual(validate_join({"C": [a]}, manifest([p1, p2])), INVALID)

    # JPF-09: changed operation/digest/scope is not an alias join.
    def test_JPF_09(self):
        p = participant()
        a = admission("C/admit/1", "C")
        a["scope_ref"] = "scope/other"
        self.assertEqual(validate_join({"C": [a]}, manifest([p])), INVALID)

    # JPF-10: currentness changes invalidate release after JoinProof creation.
    def test_JPF_10(self):
        current = deepcopy(self.snaps["D"])
        current["request_highwaters"]["barrier"] += 1
        self.assertEqual(validate_release(release("D", self.b), current, self.b), STALE)

    # JPF-11: valid manifest without required I/D evidence is UNKNOWN.
    def test_JPF_11(self):
        p = participant(required=["C", "I", "D"])
        a = admission("C/admit/1", "C")
        self.assertEqual(validate_join({"C": [a], "I": [], "D": []}, manifest([p])), UNKNOWN)

    # JPF-12: same GID/DB incarnation and exact I/Storage terminal tuple required.
    def test_JPF_12(self):
        def exact_jf10(i, s, same_participant, same_gid, same_db):
            if not (same_participant and same_gid and same_db):
                return INVALID
            return validate_jf10(i, s)
        self.assertEqual(exact_jf10("COMMIT_WON", "COMMITTED", True, True, True), VALID)
        self.assertEqual(exact_jf10("COMMIT_WON", "COMMITTED", True, False, True), INVALID)
        self.assertEqual(exact_jf10("COMMIT_WON", "ROLLED_BACK", True, True, True), INVALID)

    # JPF-13: every owner request row must have exactly one JoinProof disposition.
    def test_JPF_13(self):
        reqs = {o: [] for o in ("I", "D", "C")}
        reqs["C"] = [request_entry("C/request-row/1", "C")]
        edges = {o: [] for o in ("I", "D", "C")}
        self.assertEqual(validate_request_dispositions(reqs, edges), INVALID)

    # JPF-14: OUT_OF_SCOPE_WITH_PROOF requires owner-signed proof.
    def test_JPF_14(self):
        req = request_entry("C/request-row/1", "C")
        edge = {"owner_kind":"C","owner_entry_ref":"C/request-row/1","owner_request_ref":req["request_ref"],
                "owner_request_digest":req["request_digest"],"owner_entry_digest":req["entry_digest"],"owner_sequence":1,"scope_ref":"scope/test",
                "disposition":"OUT_OF_SCOPE_WITH_PROOF","owner_signature_valid":True}
        reqs = {"I":[],"D":[],"C":[req]}; edges = {"I":[],"D":[],"C":[edge]}
        self.assertEqual(validate_request_dispositions(reqs, edges), INVALID)

    # JPF-15: changed request digest is a conflict, not an alias.
    def test_JPF_15(self):
        req = request_entry("C/request-row/1", "C")
        edge = {"owner_kind":"C","owner_entry_ref":"C/request-row/1","owner_request_ref":req["request_ref"],
                "owner_request_digest":"f"*64,"owner_entry_digest":req["entry_digest"],"owner_sequence":1,"scope_ref":"scope/test",
                "disposition":"IN_BATCH_REQUEST_SET","owner_signature_valid":True}
        self.assertEqual(validate_request_dispositions({"I":[],"D":[],"C":[req]},
                                                       {"I":[],"D":[],"C":[edge]}), INVALID)

    # JPF-16: ledger row identity cannot be substituted by the stable request identity.
    def test_JPF_16(self):
        req = request_entry("C/request-row/1", "C")
        edge = {"owner_kind":"C","owner_entry_ref":"request/C/request-row/1","owner_request_ref":req["request_ref"],
                "owner_request_digest":req["request_digest"],"owner_entry_digest":req["entry_digest"],"owner_sequence":1,"scope_ref":"scope/test",
                "disposition":"IN_BATCH_REQUEST_SET","owner_signature_valid":True}
        self.assertEqual(validate_request_dispositions({"I":[],"D":[],"C":[req]},
                                                       {"I":[],"D":[],"C":[edge]}), INVALID)

    # JPF-17: exact owner request rows may be captured independently of admission rows.
    def test_JPF_17(self):
        req = request_entry("C/request-row/1", "C")
        edge = {"owner_kind":"C","owner_entry_ref":"C/request-row/1","owner_request_ref":req["request_ref"],
                "owner_request_digest":req["request_digest"],"owner_entry_digest":req["entry_digest"],"owner_sequence":1,"scope_ref":"scope/test",
                "disposition":"IN_BATCH_REQUEST_SET","owner_signature_valid":True}
        self.assertEqual(validate_request_dispositions({"I":[],"D":[],"C":[req]},
                                                       {"I":[],"D":[],"C":[edge]}), VALID)

    # JPF-18: the primary OwnerEntryRef must not be substituted with OwnerAdmissionRef.
    def test_JPF_18(self):
        p = participant(required=["C"])
        p["primary_owner_entry_ref"] = "C/admit/1"
        a = admission("C/admit/1", "C")
        self.assertEqual(validate_join({"C": [a]}, manifest([p])), INVALID)

    # JPF-19: stable OwnerAdmissionRef is independently checked from the row ref.
    def test_JPF_19(self):
        p = participant(required=["C"])
        a = admission("C/admit/1", "C")
        a["owner_admission_ref"] = "C/admit/other"
        self.assertEqual(validate_join({"C": [a]}, manifest([p])), INVALID)

def reject_duplicates(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("duplicate JSON key: " + k)
        out[k] = v
    return out
if __name__ == "__main__":
    unittest.main(verbosity=2)
