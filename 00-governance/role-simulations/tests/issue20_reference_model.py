"""Issue #20 deterministic cross-owner reference model; not production code."""
from dataclasses import dataclass, field


class ProtocolError(Exception):
    pass


class UnknownOutcome(ProtocolError):
    pass


@dataclass(frozen=True)
class Publication:
    operation_id: str
    digest: str
    participant_ref: str
    scope: str
    artifact_id: str


@dataclass
class DAuthority:
    generation: int = 1
    registration_high_water: int = 0
    fence_installed: bool = False
    admissions: dict = field(default_factory=dict)
    unresolved: set = field(default_factory=set)
    terminal: dict = field(default_factory=dict)

    def admit(self, work_id: str, digest: str):
        old = self.admissions.get(work_id)
        if old:
            if old["digest"] != digest:
                raise ProtocolError("D idempotency conflict")
            return old
        if self.fence_installed:
            raise ProtocolError("D fence blocks admission")
        self.registration_high_water += 1
        receipt = {"work_id": work_id, "digest": digest,
                   "sequence": self.registration_high_water,
                   "generation": self.generation}
        self.admissions[work_id] = receipt
        self.unresolved.add(work_id)
        return receipt

    def install_fence(self):
        if not self.fence_installed:
            self.generation += 1
            self.fence_installed = True
        return {"generation": self.generation,
                "high_water": self.registration_high_water,
                "member_ids": tuple(sorted(self.unresolved))}

    def terminalize(self, work_id: str, outcome: str):
        if outcome not in {"PUBLISHED", "NO_PUBLICATION"}:
            raise ProtocolError("UNKNOWN is nonterminal")
        if work_id not in self.admissions:
            raise ProtocolError("unknown D admission")
        self.terminal[work_id] = outcome
        self.unresolved.discard(work_id)

    def release_fence(self, expected_generation: int, expected_high_water: int):
        if not self.fence_installed:
            raise ProtocolError("no active fence")
        if (expected_generation != self.generation or
                expected_high_water != self.registration_high_water):
            raise ProtocolError("stale D release CAS")
        if self.unresolved:
            raise ProtocolError("D barrier has unresolved members")
        self.fence_installed = False
        return {"generation": self.generation, "released": True}


@dataclass
class IAuthority:
    permission_epoch: str = "perm-1"
    gate_generation: int = 1
    revoked: bool = False
    receipts: dict = field(default_factory=dict)
    unresolved: set = field(default_factory=set)

    def consume(self, publication: Publication, outcome: str):
        old = self.receipts.get(publication.operation_id)
        if old:
            if old["digest"] != publication.digest or old["participant_ref"] != publication.participant_ref:
                raise ProtocolError("I receipt replay/binding conflict")
            return old
        if self.revoked or outcome == "REVOCATION_WON":
            result = "REVOCATION_WON"
        elif outcome == "COMMIT_WON":
            result = "COMMIT_WON"
        elif outcome == "UNKNOWN":
            result = "UNKNOWN/IN_DOUBT"
        else:
            raise ProtocolError("invalid I decision")
        receipt = {"outcome": result, "digest": publication.digest,
                   "participant_ref": publication.participant_ref,
                   "permission_epoch": self.permission_epoch,
                   "gate_generation": self.gate_generation}
        self.receipts[publication.operation_id] = receipt
        if result in {"COMMIT_WON", "UNKNOWN/IN_DOUBT"}:
            self.unresolved.add(publication.operation_id)
        return receipt

    def revoke(self):
        self.revoked = True
        if self.unresolved:
            return "PENDING"
        self.gate_generation += 1
        self.permission_epoch = f"perm-{self.gate_generation}"
        return "EFFECTIVE"

    def close_participant(self, publication: Publication, storage_outcome: str):
        receipt = self.receipts.get(publication.operation_id)
        if not receipt or receipt["digest"] != publication.digest:
            raise ProtocolError("missing/mismatched I receipt")
        if storage_outcome not in {"COMMITTED_VISIBLE", "NO_PUBLICATION"}:
            raise UnknownOutcome("I participant remains unresolved")
        self.unresolved.discard(publication.operation_id)
        if self.revoked and not self.unresolved:
            self.gate_generation += 1
            self.permission_epoch = f"perm-{self.gate_generation}"
            return "REVOCATION_EFFECTIVE"
        return "CLOSED"


@dataclass
class StorageAuthority:
    participants: dict = field(default_factory=dict)

    def prepare(self, publication: Publication):
        old = self.participants.get(publication.participant_ref)
        if old:
            if old["digest"] != publication.digest:
                raise ProtocolError("Storage participant identity conflict")
            return old
        participant = {"publication": publication, "digest": publication.digest,
                       "state": "PRIVATE_PREPARED"}
        self.participants[publication.participant_ref] = participant
        return participant

    def resolve(self, publication: Publication, d_admission: dict | None,
                i_receipt: dict, current_d_generation: int,
                current_i_epoch: str, outcome: str):
        participant = self.participants.get(publication.participant_ref)
        if not participant:
            raise UnknownOutcome("exact prepared participant absent")
        if participant["publication"] != publication:
            raise ProtocolError("participant tuple mismatch")
        if not d_admission:
            raise ProtocolError("D admission absent; remain private")
        if (d_admission.get("work_id") != publication.operation_id or
                d_admission.get("digest") != publication.digest):
            raise ProtocolError("D admission binding mismatch")
        if d_admission.get("generation") != current_d_generation:
            raise ProtocolError("stale D FenceGeneration clearance")
        if (i_receipt["digest"] != publication.digest or
                i_receipt["participant_ref"] != publication.participant_ref):
            raise ProtocolError("I receipt binding mismatch")
        if i_receipt["permission_epoch"] != current_i_epoch:
            raise ProtocolError("stale PermissionEpoch")
        if outcome == "UNKNOWN":
            raise UnknownOutcome("storage outcome unresolved")
        if i_receipt["outcome"] != "COMMIT_WON" and outcome == "COMMITTED_VISIBLE":
            raise ProtocolError("I did not authorize forward resolution")
        if outcome == "COMMITTED_VISIBLE":
            participant["state"] = "COMMITTED_VISIBLE"
        elif outcome == "NO_PUBLICATION":
            participant["state"] = "NO_PUBLICATION"
        else:
            raise ProtocolError("invalid Storage terminal outcome")
        participant["d_generation_at_commit"] = current_d_generation
        return participant["state"]


@dataclass
class Protocol:
    d: DAuthority = field(default_factory=DAuthority)
    i: IAuthority = field(default_factory=IAuthority)
    storage: StorageAuthority = field(default_factory=StorageAuthority)

    def publish(self, publication: Publication, i_decision="COMMIT_WON",
                storage_outcome="COMMITTED_VISIBLE"):
        # Storage Prepare precedes D PublicationParticipant admission.
        self.storage.prepare(publication)
        self.d.admit(publication.operation_id, publication.digest)
        i_receipt = self.i.consume(publication, i_decision)
        if i_receipt["outcome"] == "UNKNOWN/IN_DOUBT":
            raise UnknownOutcome("I decision unresolved; private bytes retained")
        if i_receipt["outcome"] == "REVOCATION_WON":
            storage_state = self.storage.resolve(
                publication, self.d.admissions.get(publication.operation_id),
                i_receipt, self.d.generation, self.i.permission_epoch,
                "NO_PUBLICATION")
        else:
            storage_state = self.storage.resolve(
                publication, self.d.admissions.get(publication.operation_id),
                i_receipt, self.d.generation, self.i.permission_epoch,
                storage_outcome)
        d_terminal = "PUBLISHED" if storage_state == "COMMITTED_VISIBLE" else "NO_PUBLICATION"
        self.d.terminalize(publication.operation_id, d_terminal)
        self.i.close_participant(publication, storage_state)
        return storage_state


@dataclass
class RestoreGate:
    required: tuple = ("storage", "coc", "i", "d", "f", "e", "g", "adapter")
    verified: dict = field(default_factory=dict)
    state: str = "RESTORE_FENCED"

    def attest(self, owner: str, digest: str, current: bool = True):
        if owner not in self.required:
            raise ProtocolError("unknown restore proof authority")
        self.verified[owner] = (digest, current)

    def release(self):
        if any(owner not in self.verified or not self.verified[owner][0] or
               not self.verified[owner][1] for owner in self.required):
            raise ProtocolError("restore proof conjunction incomplete/stale")
        self.state = "SERVING"
        return self.state
