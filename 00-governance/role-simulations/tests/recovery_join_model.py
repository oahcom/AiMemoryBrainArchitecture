"""RecoveryJoin 1.0.2 union/completeness reference model; not production verifier."""
from dataclasses import dataclass, field
import hashlib
import json


class JoinError(Exception):
    pass


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class OwnerSnapshot:
    owner: str
    rows: tuple
    high_water: int
    snapshot_ref: str
    snapshot_digest: str
    snapshot_count: int
    snapshot_root: str
    query_id: str
    pagination_complete: bool
    anti_rollback_current: bool
    complete_empty_signed: bool = False

    def expected_root(self):
        return digest(sorted(self.rows))

    def assert_complete(self):
        if not self.query_id or not self.pagination_complete:
            raise JoinError("owner query/pagination incomplete")
        if not self.anti_rollback_current:
            raise JoinError("owner anti-rollback state unknown")
        if len(set(self.rows)) != len(self.rows):
            raise JoinError("duplicate owner snapshot row")
        if self.snapshot_count != len(self.rows):
            raise JoinError("owner snapshot count mismatch")
        if self.snapshot_root != self.expected_root():
            raise JoinError("owner snapshot root mismatch")
        if not self.rows and not self.complete_empty_signed:
            raise JoinError("empty set requires signed COMPLETE_EMPTY proof")


@dataclass(frozen=True)
class MembershipProof:
    owner: str
    row_id: str
    sequence: int
    snapshot_ref: str
    snapshot_digest: str
    proof_digest: str
    signature_valid: bool
    key_status_current: bool


def verify_membership(snapshot: OwnerSnapshot, proof: MembershipProof):
    if proof.owner != snapshot.owner or proof.row_id not in snapshot.rows:
        raise JoinError("proof does not identify a row in this owner snapshot")
    if proof.snapshot_ref != snapshot.snapshot_ref or proof.snapshot_digest != snapshot.snapshot_digest:
        raise JoinError("proof snapshot binding mismatch")
    if proof.sequence > snapshot.high_water:
        raise JoinError("row sequence exceeds captured owner high-water")
    if not proof.signature_valid or not proof.key_status_current:
        raise JoinError("owner signature/key status is not trusted")
    if not proof.proof_digest:
        raise JoinError("missing proof digest")
    return True


@dataclass
class CanonicalUnion:
    coc_participants: tuple
    owner_rows: tuple
    snapshots: dict
    proofs: tuple
    owner_bindings: dict = field(default_factory=dict)

    def build(self, recovery_epoch: str, prefix_digest: str):
        if len(set(self.coc_participants)) != len(self.coc_participants):
            raise JoinError("duplicate COC participant")
        proof_index = {(p.owner, p.row_id): p for p in self.proofs}
        if len(proof_index) != len(self.proofs):
            raise JoinError("duplicate membership proof identity")
        for snapshot in self.snapshots.values():
            snapshot.assert_complete()

        coc_members = []
        for participant in self.coc_participants:
            bindings = sorted(self.owner_bindings.get(participant, ()))
            for owner, row_id in bindings:
                snapshot = self.snapshots.get(owner)
                proof = proof_index.get((owner, row_id))
                if snapshot is None or proof is None:
                    raise JoinError("missing owner binding/snapshot proof")
                verify_membership(snapshot, proof)
            coc_members.append({
                "kind": "COC_PARTICIPANT",
                "participant_intent_ref": participant,
                "owner_admission_bindings": bindings,
            })

        owner_only = []
        seen = set()
        for row in self.owner_rows:
            owner, row_id = row["owner"], row["row_id"]
            identity = (owner, row_id)
            if identity in seen:
                raise JoinError("duplicate owner-local admission")
            seen.add(identity)
            snapshot = self.snapshots.get(owner)
            proof = proof_index.get(identity)
            if snapshot is None or proof is None:
                raise JoinError("missing owner-local membership proof")
            verify_membership(snapshot, proof)
            parent = row.get("parent_intent_ref")
            if parent:
                if parent not in self.coc_participants:
                    raise JoinError("fabricated or unknown ParticipantIntentRef")
                if row_id not in {r for o, r in self.owner_bindings.get(parent, ()) if o == owner}:
                    raise JoinError("owner row not joined to parent participant")
                continue
            if not row.get("absence_reason"):
                raise JoinError("owner-only member needs non-empty COC absence reason")
            owner_only.append({
                "kind": "OWNER_LOCAL_ADMISSION",
                "owner": owner,
                "owner_admission_ref": row_id,
                "coc_participant_intent_ref": None,
                "coc_absence_reason": row["absence_reason"],
            })

        represented = set()
        for participant, bindings in self.owner_bindings.items():
            if participant not in self.coc_participants:
                raise JoinError("binding references unknown COC participant")
            represented.update(bindings)
        owner_rows_set = {(r["owner"], r["row_id"]) for r in self.owner_rows}
        snapshot_rows = {(owner, row) for owner, snap in self.snapshots.items() for row in snap.rows}
        if represented | seen != snapshot_rows:
            raise JoinError("owner snapshot rows are not represented exactly once")

        members = coc_members + owner_only
        member_set_root = digest(members)
        owner_roots = {
            owner: {
                "snapshot_ref": snap.snapshot_ref,
                "snapshot_digest": snap.snapshot_digest,
                "high_water": snap.high_water,
                "row_root": snap.expected_root(),
            }
            for owner, snap in sorted(self.snapshots.items())
        }
        content = {
            "recovery_epoch": recovery_epoch,
            "prefix_digest": prefix_digest,
            "coc_participant_count": len(coc_members),
            "owner_local_admission_count": len(owner_only),
            "manifest_member_count": len(members),
            "member_set_root": member_set_root,
            "owner_snapshot_roots": owner_roots,
            "manifest_members": members,
        }
        return {
            **content,
            "manifest_content_digest": digest(content),
            "manifest_record_entry_digest": None,
            "batch_digest": None,
            "batch_entry_digest": None,
        }


@dataclass
class TwoPhaseRecovery:
    state: str = "RECOVERY_FENCED"
    batch: dict | None = None
    manifest: dict | None = None
    owner_releases: set = field(default_factory=set)

    def commit_batch(self, batch_id: str, batch_digest: str, manifest_content_digest: str):
        candidate = {"batch_id": batch_id, "batch_digest": batch_digest,
                     "manifest_content_digest": manifest_content_digest}
        if self.batch:
            if self.batch != candidate:
                raise JoinError("same batch identity with changed digest")
            return self.batch
        self.batch = candidate
        self.state = "BATCH_COMMITTED_MANIFEST_PENDING"
        return candidate

    def commit_manifest(self, batch_id: str, manifest_content_digest: str,
                        manifest_record_entry_digest: str, members: tuple):
        if not self.batch:
            raise JoinError("Batch must commit before Manifest")
        if batch_id != self.batch["batch_id"]:
            raise JoinError("Manifest references different Batch")
        if manifest_content_digest != self.batch["manifest_content_digest"]:
            raise JoinError("Manifest content digest differs from Batch")
        if not manifest_record_entry_digest:
            raise JoinError("missing final Manifest record-entry digest")
        self.manifest = {
            "batch_id": batch_id,
            "manifest_content_digest": manifest_content_digest,
            "manifest_record_entry_digest": manifest_record_entry_digest,
            "members": members,
        }
        self.state = "MANIFEST_COMMITTED_OWNER_RELEASES_PENDING"
        return self.manifest

    def release_owner(self, owner: str, expected_high_water: int,
                      current_high_water: int, content_digest: str,
                      record_entry_digest: str):
        if not self.manifest:
            raise JoinError("cannot release before Manifest")
        if expected_high_water != current_high_water:
            raise JoinError("owner currentness CAS failed")
        if content_digest != self.manifest["manifest_content_digest"]:
            raise JoinError("wrong Manifest content digest")
        if record_entry_digest != self.manifest["manifest_record_entry_digest"]:
            raise JoinError("wrong Manifest record-entry digest")
        self.owner_releases.add(owner)

    def complete(self, required_owners=("I", "D", "C")):
        if not self.manifest or not set(required_owners).issubset(self.owner_releases):
            raise JoinError("owner releases incomplete")
        self.state = "RECOVERY_EPOCH_COMPLETED"
        return self.state
