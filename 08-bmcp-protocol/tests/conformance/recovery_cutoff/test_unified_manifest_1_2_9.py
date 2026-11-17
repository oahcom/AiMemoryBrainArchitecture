"""Structural and semantic candidate vectors for unified schema artifact 1.2.9."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.9.schema.json"
sys.path.insert(0, str(ROOT / "runtime_reference"))
from unified_manifest_semantics import (
    VALID, INVALID, UNKNOWN, test_digest, owner_snapshot_root_projection,
    manifest_content_projection, manifest_content_digest, validate_manifest_union,
    validate_batch_manifest_pair, validate_owner_release, validate_signature_profile,
    validate_provider_outcome,
)


def snapshots():
    result = {}
    for owner in ("I", "D", "C"):
        s = {
            "owner": owner,
            "owner_snapshot_ref": owner + "/snapshot/1",
            "owner_snapshot_digest": (owner.lower() * 64)[:64],
            "owner_snapshot_attestation_ref": owner + "/attestation/1",
            "owner_snapshot_attestation_digest": (owner.lower() * 64)[:64],
            "owner_gate_generation": "7",
            "request_high_water": "12",
            "admission_high_water": "18",
            "request_ledger_root": (owner.lower() * 64)[:64],
            "admission_ledger_root": (owner.lower() * 64)[:64],
            "owner_ledger_root": (owner.lower() * 64)[:64],
            "anti_rollback_anchor_ref": owner + "/anchor/7",
            "owner_specific_high_waters_digest": (owner.lower() * 64)[:64],
            "ledger_available": True,
            "pagination_complete": True,
        }
        result[owner] = s
    return result


def admission(owner, ref, participant_ref=None):
    s = snapshots()[owner]
    value = {
        "owner_kind": owner,
        "owner_admission_ref": owner + "/" + ref,
        "owner_entry_ref": owner + "/" + ref + "/row",
        "owner_entry_kind": "RESERVATION" if owner == "C" else "WORK_ITEM",
        "owner_ledger_ref": owner + "/ledger/1",
        "owner_ledger_version": "1",
        "owner_local_sequence": "5",
        "owner_high_water": "18",
        "owner_entry_digest": "a" * 64,
        "owner_ledger_root": s["owner_ledger_root"],
        "owner_snapshot_ref": s["owner_snapshot_ref"],
        "owner_snapshot_digest": s["owner_snapshot_digest"],
        "owner_snapshot_attestation_ref": s["owner_snapshot_attestation_ref"],
        "owner_snapshot_attestation_digest": s["owner_snapshot_attestation_digest"],
        "operation_identity_ref": "operation/" + ref,
        "operation_digest": "b" * 64,
        "request_digest": "c" * 64,
        "scope_binding_digest": "d" * 64,
        "admission_state": "ADMITTED_NOT_REGISTERED" if participant_ref is None else "PENDING",
        "effect_boundary": "RESERVATION" if owner == "C" else "WORK_ADMISSION",
        "coc_participant_intent_ref": participant_ref,
        "coc_absence_reason": "not_registered_at_frozen_prefix" if participant_ref is None else None,
    }
    return value


def make_manifest():
    snaps = snapshots()
    registered = admission("C", "admit-1", "participant/1")
    unregistered = admission("D", "work-9", None)
    participant = {
        "member_kind": "COC_PARTICIPANT",
        "participant_intent_ref": "participant/1",
        "transaction_ref": "transaction/1",
        "request_digest": "c" * 64,
        "owner_boundary_ref": "boundary/C/1",
        "policy_domain_ref": "policy/1",
        "participant_tuple_digest": "e" * 64,
        "participant_owner": "C",
        "owner_admission_bindings": [{
            "owner_kind": "C",
            "owner_admission_ref": registered["owner_admission_ref"],
            "owner_entry_ref": registered["owner_entry_ref"],
            "owner_ledger_ref": registered["owner_ledger_ref"],
            "owner_ledger_version": registered["owner_ledger_version"],
            "owner_local_sequence": registered["owner_local_sequence"],
            "owner_high_water": registered["owner_high_water"],
            "owner_entry_digest": registered["owner_entry_digest"],
            "owner_ledger_root": registered["owner_ledger_root"],
            "owner_snapshot_ref": registered["owner_snapshot_ref"],
            "owner_snapshot_digest": registered["owner_snapshot_digest"],
            "owner_snapshot_attestation_ref": registered["owner_snapshot_attestation_ref"],
            "owner_snapshot_attestation_digest": registered["owner_snapshot_attestation_digest"],
            "operation_digest": registered["operation_digest"],
            "scope_binding_digest": registered["scope_binding_digest"],
            "coc_participant_intent_ref": "participant/1",
        }],
    }
    local = {
        "member_kind": "OWNER_LOCAL_ADMISSION",
        **{k: v for k, v in unregistered.items() if k != "coc_absence_reason"},
        "coc_participant_intent_ref": None,
        "coc_absence_reason": unregistered["coc_absence_reason"],
    }
    members = sorted([participant, local], key=lambda x: (
        "0" if x["member_kind"] == "COC_PARTICIPANT" else "1",
        x.get("participant_intent_ref", x.get("owner_kind", "") + ":" + x.get("owner_admission_ref", ""))
    ))
    roots = {k: owner_snapshot_root_projection(v) for k, v in snaps.items()}
    m = {
        "schema_version": "1.3.0",
        "message_type": "PARTICIPANT_SET_RECONCILIATION",
        "manifest_id": "manifest/epoch-1/round-1",
        "recovery_epoch_ref": "epoch/1",
        "prefix": {"coordinator_epoch": "term/4", "coordinator_index": 88,
                   "entry_digest": "f" * 64, "committed_configuration_epoch": "config/2"},
        "enumeration_high_water": "prefix/88",
        "coc_participant_count": 1,
        "owner_local_admission_count": 1,
        "manifest_member_count": 2,
        "member_set_root": test_digest("MANIFEST-MEMBER-SET", members),
        "owner_snapshot_roots": roots,
        "manifest_members": members,
    }
    m["manifest_content_digest"] = manifest_content_digest(m)
    return m, [participant], [registered, unregistered], snaps


class UnifiedSchema129(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def message(self, message_type):
        return next(x["allOf"][1] for x in self.schema["oneOf"]
                    if x["allOf"][1]["properties"]["message_type"]["const"] == message_type)

    def test_SCHEMA129_01_artifact_and_wire_versions_are_distinct(self):
        self.assertTrue(self.schema["$id"].endswith("/1.2.9"))
        self.assertEqual(self.schema["$defs"]["commonEnvelope"]["properties"]["schema_version"]["const"], "1.3.0")

    def test_SCHEMA129_02_manifest_has_typed_union_variants(self):
        items = self.message("PARTICIPANT_SET_RECONCILIATION")["properties"]["manifest_members"]["items"]
        refs = {x["$ref"] for x in items["oneOf"]}
        self.assertEqual(refs, {"#/$defs/cocParticipantMember", "#/$defs/ownerLocalAdmissionMember"})

    def test_SCHEMA129_03_owner_local_member_requires_explicit_null_and_reason(self):
        d = self.schema["$defs"]["ownerLocalAdmissionMember"]
        self.assertEqual(d["properties"]["coc_participant_intent_ref"]["type"], "null")
        self.assertTrue({"coc_participant_intent_ref", "coc_absence_reason", "owner_snapshot_attestation_digest"}.issubset(d["required"]))

    def test_SCHEMA129_04_coc_member_binds_owner_admissions(self):
        d = self.schema["$defs"]["cocParticipantMember"]
        self.assertIn("owner_admission_bindings", d["required"])
        self.assertIn("participant_intent_ref", d["required"])

    def test_SCHEMA129_05_batch_binds_union_counts_root_and_content_digest(self):
        p = self.message("COC_RECOVERY_CUTOFF_BATCH")["properties"]
        self.assertTrue({"manifest_content_digest", "coc_participant_count", "owner_local_admission_count", "manifest_member_count", "member_set_root"}.issubset(p))

    def test_SCHEMA129_06_manifest_binds_owner_snapshot_roots(self):
        p = self.message("PARTICIPANT_SET_RECONCILIATION")["properties"]
        self.assertIn("owner_snapshot_roots", p)
        self.assertEqual(self.schema["$defs"]["ownerSnapshotRoots"]["required"], ["I", "D", "C"])

    def test_SCHEMA129_07_snapshot_attestation_and_owner_specific_highwater_digests_required(self):
        r = set(self.schema["$defs"]["ownerSnapshot"]["required"])
        self.assertTrue({"owner_snapshot_attestation_digest", "owner_specific_high_waters_digest"}.issubset(r))

    def test_SCHEMA129_08_release_and_completion_separate_content_and_record_digests(self):
        for t in ("OWNER_LOCAL_GATE_RELEASE", "RECOVERY_EPOCH_COMPLETED"):
            r = set(self.message(t)["required"])
            self.assertIn("manifest_content_digest", r)
            self.assertIn("manifest_record_entry_digest", r)

    def test_SCHEMA129_09_signature_profile_remains_structural_optional(self):
        p = self.schema["$defs"]["commonEnvelope"]["properties"]
        self.assertIn("signature_profile_id", p)
        self.assertNotIn("signature_profile_id", self.schema["$defs"]["commonEnvelope"]["required"])

    def test_SCHEMA129_10_recovery_messages_do_not_use_ambiguous_manifest_digest(self):
        for t in ("COC_RECOVERY_CUTOFF_BATCH", "PARTICIPANT_SET_RECONCILIATION",
                  "OWNER_LOCAL_GATE_RELEASE", "RECOVERY_EPOCH_COMPLETED"):
            p = self.message(t)["properties"]
            self.assertIn("manifest_content_digest", p)
            self.assertNotIn("manifest_digest", p)


class UnionManifestSemantics(unittest.TestCase):
    def setUp(self):
        self.manifest, self.prefix, self.admissions, self.snapshots = make_manifest()

    def test_UNION_01_exact_union_is_valid(self):
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, self.admissions, self.snapshots), VALID)

    def test_UNION_02_omitted_coc_participant_is_invalid(self):
        self.assertEqual(validate_manifest_union(self.manifest, [], self.admissions, self.snapshots), INVALID)

    def test_UNION_03_omitted_unregistered_owner_admission_is_invalid(self):
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, self.admissions[:1], self.snapshots), INVALID)

    def test_UNION_04_duplicate_coc_participant_is_invalid(self):
        m = deepcopy(self.manifest)
        m["manifest_members"].append(deepcopy(m["manifest_members"][0]))
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_05_duplicate_owner_admission_identity_is_invalid(self):
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, self.admissions + [deepcopy(self.admissions[0])], self.snapshots), INVALID)

    def test_UNION_06_unregistered_member_requires_null_coc_ref(self):
        m = deepcopy(self.manifest)
        m["manifest_members"][1]["coc_participant_intent_ref"] = "participant/fabricated"
        m["member_set_root"] = test_digest("MANIFEST-MEMBER-SET", m["manifest_members"])
        m["manifest_content_digest"] = manifest_content_digest(m)
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_07_unregistered_member_requires_absence_reason(self):
        m = deepcopy(self.manifest)
        m["manifest_members"][1]["coc_absence_reason"] = ""
        m["member_set_root"] = test_digest("MANIFEST-MEMBER-SET", m["manifest_members"])
        m["manifest_content_digest"] = manifest_content_digest(m)
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_08_registered_binding_must_match_exact_owner_row(self):
        m = deepcopy(self.manifest)
        m["manifest_members"][0]["owner_admission_bindings"][0]["owner_entry_ref"] = "wrong/row"
        m["member_set_root"] = test_digest("MANIFEST-MEMBER-SET", m["manifest_members"])
        m["manifest_content_digest"] = manifest_content_digest(m)
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_09_missing_owner_snapshot_is_unknown(self):
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, self.admissions, {"I":self.snapshots["I"],"D":self.snapshots["D"]}), UNKNOWN)

    def test_UNION_10_partial_owner_ledger_pagination_is_unknown(self):
        snaps = deepcopy(self.snapshots)
        snaps["D"]["pagination_complete"] = False
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, self.admissions, snaps), UNKNOWN)

    def test_UNION_11_owner_highwater_advance_is_unknown(self):
        rows = deepcopy(self.admissions)
        rows[1]["owner_high_water"] = "19"
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, rows, self.snapshots), UNKNOWN)

    def test_UNION_12_owner_snapshot_root_mismatch_is_invalid(self):
        m = deepcopy(self.manifest)
        m["owner_snapshot_roots"]["I"]["request_ledger_root"] = "0" * 64
        m["manifest_content_digest"] = manifest_content_digest(m)
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_13_member_count_mismatch_is_invalid(self):
        m = deepcopy(self.manifest)
        m["manifest_member_count"] = 99
        m["manifest_content_digest"] = manifest_content_digest(m)
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_14_member_set_root_mismatch_is_invalid(self):
        m = deepcopy(self.manifest)
        m["member_set_root"] = "0" * 64
        m["manifest_content_digest"] = manifest_content_digest(m)
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_15_manifest_content_digest_mismatch_is_invalid(self):
        m = deepcopy(self.manifest)
        m["manifest_content_digest"] = "0" * 64
        self.assertEqual(validate_manifest_union(m, self.prefix, self.admissions, self.snapshots), INVALID)

    def test_UNION_16_incomplete_coc_prefix_enumeration_is_unknown(self):
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, self.admissions, self.snapshots, False), UNKNOWN)

    def test_UNION_17_registered_admission_missing_from_coc_prefix_is_invalid(self):
        rows = deepcopy(self.admissions)
        rows[0]["coc_participant_intent_ref"] = "participant/missing"
        self.assertEqual(validate_manifest_union(self.manifest, self.prefix, rows, self.snapshots), INVALID)


class SignatureProfileAndProviderOutcome(unittest.TestCase):
    def setUp(self):
        self.registry = {"profile/I/1": {
            "status":"ACTIVE","owner_authority":"I","audience":"coc/validator",
            "purpose":"OWNER_LOCAL_GATE_RELEASE","wire_schema_version":"1.3.0"
        }}

    def test_PROFILE_01_protected_record_requires_profile_id(self):
        self.assertEqual(validate_signature_profile({"owner_authority":"I","audience":"coc/validator"}, True, self.registry, "I", "coc/validator", "OWNER_LOCAL_GATE_RELEASE"), INVALID)

    def test_PROFILE_02_unavailable_trust_registry_is_unknown(self):
        self.assertEqual(validate_signature_profile({"signature_profile_id":"profile/I/1"}, True, None, "I", "coc/validator", "OWNER_LOCAL_GATE_RELEASE"), UNKNOWN)

    def test_PROFILE_03_unknown_profile_is_invalid(self):
        self.assertEqual(validate_signature_profile({"signature_profile_id":"profile/unknown","owner_authority":"I","audience":"coc/validator"}, True, self.registry, "I", "coc/validator", "OWNER_LOCAL_GATE_RELEASE"), INVALID)

    def test_PROFILE_04_exact_profile_is_valid(self):
        m={"signature_profile_id":"profile/I/1","owner_authority":"I","audience":"coc/validator"}
        self.assertEqual(validate_signature_profile(m, True, self.registry, "I", "coc/validator", "OWNER_LOCAL_GATE_RELEASE"), VALID)

    def test_PROFILE_05_wrong_owner_or_audience_is_invalid(self):
        m={"signature_profile_id":"profile/I/1","owner_authority":"C","audience":"other"}
        self.assertEqual(validate_signature_profile(m, True, self.registry, "I", "coc/validator", "OWNER_LOCAL_GATE_RELEASE"), INVALID)

    def test_PROVIDER_01_accepted_requires_provider_receipt(self):
        m={"message_type":"C_PROVIDER_OUTCOME_RECORDED","owner_authority":"C",
           "c_submit_outcome_ref":"out/1","c_submit_outcome_digest":"a"*64,
           "owner_admission_ref":"C/admit/1","owner_ledger_ref":"C/ledger",
           "owner_ledger_version":"1","owner_local_sequence":"2","owner_high_water":"3",
           "owner_ledger_root":"b"*64,"provider_ref":"provider/1","provider_adapter_ref":"adapter/1",
           "provider_idempotency_key_ref":"key/1","request_digest":"c"*64,
           "final_request_boundary_id":"boundary/1","provider_outcome_evidence_ref":"evidence/1",
           "provider_outcome":"HANDOFF_ACCEPTED","provider_request_ref":"request/1",
           "provider_receipt_ref":"receipt/1","participant_reservation_ref":"reservation/1"}
        self.assertEqual(validate_provider_outcome(m), VALID)

    def test_PROVIDER_02_ambiguous_outcome_is_unknown(self):
        m={"message_type":"C_PROVIDER_OUTCOME_RECORDED","owner_authority":"C",
           "c_submit_outcome_ref":"out/1","c_submit_outcome_digest":"a"*64,
           "owner_admission_ref":"C/admit/1","owner_ledger_ref":"C/ledger",
           "owner_ledger_version":"1","owner_local_sequence":"2","owner_high_water":"3",
           "owner_ledger_root":"b"*64,"provider_ref":"provider/1","provider_adapter_ref":"adapter/1",
           "provider_idempotency_key_ref":"key/1","request_digest":"c"*64,
           "final_request_boundary_id":"boundary/1","provider_outcome_evidence_ref":"evidence/1",
           "provider_outcome":"IN_DOUBT","unknown_reason_ref":"provider_lookup_unavailable"}
        self.assertEqual(validate_provider_outcome(m), UNKNOWN)


if __name__ == "__main__":
    unittest.main(verbosity=2)
