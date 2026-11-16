"""Storage restore high-water logical reference model; not production orchestration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


class Blocked(RuntimeError):
    pass


@dataclass(frozen=True)
class RestoreReceipt:
    restore_operation_ref: str
    state: str
    coc_prefix_digest: str
    i_proof_digests: tuple
    d_proof_digests: tuple
    storage_ledger_digest: str
    target_lsn: str
    target_timeline: int


class RestoreModel:
    def __init__(self):
        self.audience = "storage-restore"
        self.current_coc = {"epoch": 2, "index": 100, "config_epoch": 3,
                            "prefix_digest": "coc-prefix-100", "anchor": "anchor-100"}
        self.current_i = {
            "pd-A": {"permission_epoch": "pe-A-7", "sequencer_epoch": "ie-A-2",
                     "sequencer_position": "i-A-100", "revocation_highwater": "rev-A-5",
                     "inventory_epoch": 9, "registry_digest": "registry-9",
                     "active_forget_seals": {"forget-1": "seal-1"}},
            "pd-B": {"permission_epoch": "pe-B-4", "sequencer_epoch": "ie-B-1",
                     "sequencer_position": "i-B-40", "revocation_highwater": "rev-B-2",
                     "inventory_epoch": 9, "registry_digest": "registry-9",
                     "active_forget_seals": {"forget-2": "seal-2"}},
        }
        self.current_d = {
            "forget-1": {"fence_generation": 4, "effective_position": "d1-8",
                        "request_cutoff": "d1-cut-7", "producer_highwater": 12,
                        "lineage_digest": "lineage-1", "barrier_state": "COMPLETE",
                        "policy_domain": "pd-A", "inventory_seal_ref": "seal-1"},
            "forget-2": {"fence_generation": 2, "effective_position": "d2-3",
                        "request_cutoff": "d2-cut-2", "producer_highwater": 5,
                        "lineage_digest": "lineage-2", "barrier_state": "COMPLETE",
                        "policy_domain": "pd-B", "inventory_seal_ref": "seal-2"},
        }
        self.current_storage = {
            "ledger_digest": "storage-ledger-7",
            "participants": {
                "participant-1": {"participant_ref": "prepared-participant-1",
                                  "gid": "gid_1234567890", "native_xid": "native-xid:501",
                                  "canonical_authority_db_ref": "db-authority-1",
                                  "system_identifier": "1234567890", "database_oid": "16384",
                                  "prepare_timeline": 1, "prepare_lsn": "0/5004710",
                                  "state": "COMMITTED", "resolution_digest": "resolution-1"},
            },
            "visibility_pairs": {"artifact-1": {"pointer_tx": "tx-1", "receipt_tx": "tx-1"}},
        }
        self.state = "RESTORE_FENCED"
        self.receipt: Optional[RestoreReceipt] = None
        self.owner_service_gate = False

    def _verify_envelope(self, proof: dict, expected_type: str) -> None:
        if proof.get("proof_type") != expected_type:
            raise Blocked(f"wrong proof type: expected {expected_type}")
        if not proof.get("signature_valid") or not proof.get("integrity_valid") or not proof.get("key_version_active"):
            raise Blocked("proof signature/integrity/key version invalid")
        if proof.get("audience") != self.audience:
            raise Blocked("proof audience mismatch")

    def _verify_coc(self, proof: dict) -> None:
        self._verify_envelope(proof, "COCCommittedPrefixProof")
        for key in ("epoch", "index", "config_epoch", "prefix_digest", "anchor"):
            if proof.get(key) != self.current_coc[key]:
                raise Blocked(f"COC committed prefix stale/gapped: {key}")
        if not proof.get("contiguous") or not proof.get("external_anchor_verified"):
            raise Blocked("COC prefix is not contiguous or externally anchored")

    def _verify_i(self, proofs: Dict[str, dict]) -> tuple:
        if set(proofs) != set(self.current_i):
            raise Blocked("I proof set does not cover every affected PolicyDomainRef")
        digests = []
        for domain, expected in self.current_i.items():
            proof = proofs[domain]
            self._verify_envelope(proof, "IControlHighWaterProof")
            if proof.get("policy_domain") != domain:
                raise Blocked("I proof PolicyDomainRef mismatch")
            for key, value in expected.items():
                if proof.get(key) != value:
                    raise Blocked(f"I control high-water stale/mismatch: {domain}.{key}")
            digests.append(proof["proof_digest"])
        return tuple(sorted(digests))

    def _verify_d(self, proofs: Dict[str, dict]) -> tuple:
        if set(proofs) != set(self.current_d):
            raise Blocked("D proof set does not cover every relevant ForgetOperation")
        digests = []
        for operation, expected in self.current_d.items():
            proof = proofs[operation]
            self._verify_envelope(proof, "DForgetControlHighWaterProof")
            if proof.get("forget_operation") != operation:
                raise Blocked("D proof ForgetOperationRef mismatch")
            for key, value in expected.items():
                if proof.get(key) != value:
                    raise Blocked(f"D Forget high-water stale/mismatch: {operation}.{key}")
            if proof.get("barrier_state") != "COMPLETE":
                raise Blocked("D barrier is open/unknown")
            digests.append(proof["proof_digest"])
        return tuple(sorted(digests))

    def _verify_storage(self, proof: dict) -> str:
        self._verify_envelope(proof, "StorageParticipantLedgerProof")
        if proof.get("ledger_digest") != self.current_storage["ledger_digest"]:
            raise Blocked("Storage participant ledger digest mismatch")
        participants = proof.get("participants", {})
        if set(participants) != set(self.current_storage["participants"]):
            raise Blocked("Storage participant set incomplete or contains unknown participant")
        for participant, expected in self.current_storage["participants"].items():
            observed = participants[participant]
            if observed != expected:
                raise Blocked(f"same-GID/native-XID/terminal participant mismatch: {participant}")
            if observed["state"] not in {"COMMITTED", "ROLLED_BACK"}:
                raise Blocked("prepared participant remains unresolved/private")
        if proof.get("visibility_pairs") != self.current_storage["visibility_pairs"]:
            raise Blocked("VisibilityPointer/PublicationReceipt transaction mismatch")
        for pair in proof["visibility_pairs"].values():
            if pair["pointer_tx"] != pair["receipt_tx"]:
                raise Blocked("pointer-only or receipt-only visibility rejected")
        return proof["ledger_digest"]

    def reconcile(self, *, snapshot: dict, coc_proof: dict, i_proofs: Dict[str, dict],
                  d_proofs: Dict[str, dict], storage_proof: dict,
                  final_coc: Optional[dict] = None, final_i: Optional[dict] = None,
                  final_d: Optional[dict] = None) -> RestoreReceipt:
        self.state = "RESTORE_FENCED"
        self.receipt = None
        self.owner_service_gate = False
        if not snapshot.get("wal_contiguous") or not snapshot.get("target_lsn") or not snapshot.get("timeline_verified"):
            raise Blocked("base backup/WAL/timeline does not reach a verified target LSN")
        if not snapshot.get("old_primary_fenced") or not snapshot.get("quarantined"):
            raise Blocked("restore target is not isolated/quarantined or old primary is not fenced")
        self._verify_coc(coc_proof)
        i_digests = self._verify_i(i_proofs)
        d_digests = self._verify_d(d_proofs)
        storage_digest = self._verify_storage(storage_proof)
        # Linearizable stability recheck immediately before receipt issuance.
        if final_coc is not None and final_coc != self.current_coc:
            raise Blocked("COC high-water advanced during restore; replay/reconcile again")
        if final_i is not None and final_i != self.current_i:
            raise Blocked("I control high-water advanced during restore; refresh/reconcile again")
        if final_d is not None and final_d != self.current_d:
            raise Blocked("D Forget high-water advanced during restore; refresh/reconcile again")
        receipt = RestoreReceipt("restore-op-1", "RECONCILED_BUT_FENCED",
                                 coc_proof["prefix_digest"], i_digests, d_digests,
                                 storage_digest, snapshot["target_lsn"], snapshot["target_timeline"])
        self.receipt = receipt
        self.state = "RECONCILED_BUT_FENCED"
        return receipt

    def enable_owner_service(self, *, receipt_verified: bool, owner_gate_verified: bool) -> None:
        if not self.receipt or self.state != "RECONCILED_BUT_FENCED":
            raise Blocked("Storage restore reconciliation receipt is absent")
        if not receipt_verified or not owner_gate_verified:
            raise Blocked("owner-specific release gate not verified")
        self.owner_service_gate = True
        self.state = "OWNER_GATE_RELEASED"

    def global_forget_complete(self) -> bool:
        # Restore reconciliation is never a Global Forget completion proof.
        return False


def valid_envelope(proof_type: str, **fields) -> dict:
    return {"proof_type": proof_type, "signature_valid": True, "integrity_valid": True,
            "key_version_active": True, "audience": "storage-restore",
            "proof_digest": proof_type + "-digest", **fields}


def valid_proofs(model: RestoreModel):
    coc = valid_envelope("COCCommittedPrefixProof", **model.current_coc,
                         contiguous=True, external_anchor_verified=True)
    i = {domain: valid_envelope("IControlHighWaterProof", policy_domain=domain, **values)
         for domain, values in model.current_i.items()}
    d = {op: valid_envelope("DForgetControlHighWaterProof", forget_operation=op, **values)
         for op, values in model.current_d.items()}
    storage = valid_envelope("StorageParticipantLedgerProof",
                             ledger_digest=model.current_storage["ledger_digest"],
                             participants=model.current_storage["participants"],
                             visibility_pairs=model.current_storage["visibility_pairs"])
    return coc, i, d, storage