"""COC outage-recovery logical reference model.

In-memory deterministic model only. It is not a consensus log, production
coordinator, I sequencer, D fence service, or durable participant registry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


class ProtocolError(RuntimeError):
    pass


class Blocked(ProtocolError):
    pass


@dataclass(frozen=True)
class OwnerRequest:
    owner: str
    request_ref: str
    domain_ref: str
    local_sequence: int
    request_digest: str
    lineage: Tuple[str, ...] = ()


@dataclass
class Participant:
    intent_ref: str
    domain_ref: str
    request_digest: str
    lineage: Tuple[str, ...]
    intent_position: int
    i_state: str = "PENDING"
    d_state: str = "PENDING"
    c_outcome: str = "UNKNOWN"


@dataclass(frozen=True)
class RecoveryBatch:
    batch_ref: str
    position: int
    i_request_refs: Tuple[str, ...]
    d_request_refs: Tuple[str, ...]
    pre_batch_participant_refs: Tuple[str, ...]
    request_set_digest: str


class CoordinatorModel:
    """Models outage cutoffs and recovery batching; all state is in memory."""

    def __init__(self) -> None:
        self.available = True
        self.restore_fenced = False
        self.position = 0
        self.log: List[dict] = []
        self.pending_gates: Dict[str, Dict[str, OwnerRequest]] = {"I": {}, "D": {}}
        self.cutoffs: List[Tuple[int, OwnerRequest]] = []
        self.participants: Dict[str, Participant] = {}
        self.batch: Optional[RecoveryBatch] = None
        self.affected_by_owner: Dict[str, set[str]] = {"I": set(), "D": set()}

    def _append(self, record: dict) -> int:
        if not self.available or self.restore_fenced:
            raise Blocked("COC is unavailable or RESTORE_FENCED")
        self.position += 1
        committed = dict(record)
        committed["position"] = self.position
        self.log.append(committed)
        return self.position

    def set_outage(self) -> None:
        self.available = False

    def record_owner_request(self, request: OwnerRequest) -> str:
        if request.owner not in ("I", "D"):
            raise ProtocolError("only I and D owner cutoffs are modeled")
        prior = self.pending_gates[request.owner].get(request.request_ref)
        if prior is not None:
            if prior != request:
                raise ProtocolError("owner request identity rebound to changed digest/binding")
            return "PENDING_COC_CUTOFF"
        if not self.available:
            self.pending_gates[request.owner][request.request_ref] = request
            return "PENDING_COC_CUTOFF"
        pos = self._append({"kind": "OWNER_REQUEST_CUTOFF", "request": request})
        self.cutoffs.append((pos, request))
        return "RECORDED"

    def admit_intent(self, intent_ref: str, domain_ref: str, request_digest: str,
                     lineage: Tuple[str, ...] = ()) -> Participant:
        if not self.available or self.restore_fenced:
            raise Blocked("no new protected intent while COC is unavailable/fenced")
        for owner in ("I", "D"):
            for req in self.pending_gates[owner].values():
                if self._affects(req, domain_ref, lineage):
                    raise Blocked("owner-local pending gate blocks affected intent")
        for cutoff_pos, req in self.cutoffs:
            if self._affects(req, domain_ref, lineage) and cutoff_pos < self.position + 1:
                raise Blocked("committed owner cutoff wins over new intent")
        if intent_ref in self.participants:
            prior = self.participants[intent_ref]
            if (prior.domain_ref, prior.request_digest, prior.lineage) != (
                domain_ref, request_digest, lineage
            ):
                raise ProtocolError("ParticipantIntentRef rebound")
            return prior
        pos = self._append({"kind": "PARTICIPANT_INTENT", "intent_ref": intent_ref,
                            "domain_ref": domain_ref, "request_digest": request_digest,
                            "lineage": lineage})
        participant = Participant(intent_ref, domain_ref, request_digest, lineage, pos)
        self.participants[intent_ref] = participant
        return participant

    @staticmethod
    def _affects(req: OwnerRequest, domain_ref: str, lineage: Tuple[str, ...]) -> bool:
        if req.domain_ref != domain_ref:
            return False
        if req.owner == "I":
            return True
        return not req.lineage or bool(set(req.lineage).intersection(lineage))

    def recover_batch(self, *, prefix_valid: bool = True,
                      owner_complete: Optional[Dict[str, bool]] = None) -> RecoveryBatch:
        if not self.available:
            raise Blocked("cannot recover without COC quorum")
        if self.restore_fenced:
            raise Blocked("restore remains fenced")
        owner_complete = owner_complete or {}
        if not prefix_valid:
            self.restore_fenced = True
            self.log.append({"kind": "RESTORE_FENCED", "reason": "MISSING_PREFIX"})
            raise Blocked("unprovable committed prefix; RESTORE_FENCED")
        for owner in ("I", "D"):
            if self.pending_gates[owner] and not owner_complete.get(owner, False):
                self.restore_fenced = True
                self.log.append({"kind": "RESTORE_FENCED",
                                 "reason": f"{owner}_OWNER_REQUEST_SET_INCOMPLETE"})
                raise Blocked("owner request completeness not proven; RESTORE_FENCED")
        if self.batch is not None:
            return self.batch

        i_requests = tuple(sorted(self.pending_gates["I"]))
        d_requests = tuple(sorted(self.pending_gates["D"]))
        affected = set()
        for participant in self.participants.values():
            if any(self._affects(self.pending_gates["I"][ref],
                                 participant.domain_ref, participant.lineage)
                   for ref in i_requests):
                self.affected_by_owner["I"].add(participant.intent_ref)
                affected.add(participant.intent_ref)
            if any(self._affects(self.pending_gates["D"][ref],
                                 participant.domain_ref, participant.lineage)
                   for ref in d_requests):
                self.affected_by_owner["D"].add(participant.intent_ref)
                affected.add(participant.intent_ref)
        # Request arrays are separately canonicalized. Their order is not a
        # cross-owner temporal order; one batch position covers both sets.
        import hashlib
        request_set = "|".join([*(f"I:{x}" for x in i_requests),
                                *(f"D:{x}" for x in d_requests)])
        digest = hashlib.sha256(request_set.encode("utf-8")).hexdigest()
        batch_ref = f"recovery-batch-{self.position + 1}"
        pos = self._append({"kind": "RECOVERY_CUTOFF_BATCH", "batch_ref": batch_ref,
                            "i_requests": i_requests, "d_requests": d_requests,
                            "pre_batch_participants": tuple(sorted(affected)),
                            "request_set_digest": digest})
        self.batch = RecoveryBatch(batch_ref, pos, i_requests, d_requests,
                                   tuple(sorted(affected)), digest)
        return self.batch

    def reconcile_participant(self, intent_ref: str, *, i_state: str,
                              d_state: str, c_outcome: str) -> None:
        participant = self.participants[intent_ref]
        if i_state not in ("COMMIT_WON", "REVOCATION_WON", "ABORTED", "UNKNOWN", "PENDING"):
            raise ProtocolError("invalid I reconciliation state")
        if d_state not in ("CLEARANCE_CONFIRMED", "FENCE_WON", "ABORTED", "UNKNOWN", "PENDING"):
            raise ProtocolError("invalid D reconciliation state")
        if c_outcome not in ("ACCEPTED", "REJECTED", "UNKNOWN"):
            raise ProtocolError("invalid C outcome")
        participant.i_state = i_state
        participant.d_state = d_state
        participant.c_outcome = c_outcome

    def release_owner_gate(self, owner: str, *, owner_high_water: int) -> None:
        if owner not in ("I", "D") or self.batch is None:
            raise Blocked("no applicable owner gate or recovery batch")
        requests = self.pending_gates[owner]
        if not requests:
            return
        required_high_water = max(r.local_sequence for r in requests.values())
        if owner_high_water < required_high_water:
            raise Blocked("owner high-water does not cover all outage requests")
        for intent_ref in self.affected_by_owner[owner]:
            participant = self.participants[intent_ref]
            if owner == "I" and participant.i_state in ("PENDING", "UNKNOWN"):
                raise Blocked("I participant remains unresolved")
            if owner == "D" and participant.d_state in ("PENDING", "UNKNOWN"):
                raise Blocked("D participant remains unresolved")
            if participant.c_outcome == "UNKNOWN":
                raise Blocked("C provider outcome remains IN_DOUBT")
            if participant.i_state == "REVOCATION_WON" and participant.c_outcome == "ACCEPTED":
                raise ProtocolError("provider accepted after I revocation won")
            if participant.d_state == "FENCE_WON" and participant.c_outcome == "ACCEPTED":
                raise ProtocolError("provider accepted after D fence won")
        self._append({"kind": "OWNER_LOCAL_GATE_RELEASE", "owner": owner,
                      "batch_ref": self.batch.batch_ref,
                      "owner_high_water": owner_high_water})
        self.pending_gates[owner].clear()

    def provider_submit_allowed(self, domain_ref: str,
                                lineage: Tuple[str, ...] = ()) -> bool:
        if not self.available or self.restore_fenced:
            return False
        for owner in ("I", "D"):
            if any(self._affects(req, domain_ref, lineage)
                   for req in self.pending_gates[owner].values()):
                return False
        return True
