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


@dataclass
class OwnerSnapshot:
    """Membership and complete-enumeration are deliberately separate proofs."""
    owner: str
    generation: int
    high_water: str
    rows: list
    pagination_complete: bool = False
    attested: bool = False
    anti_rollback: bool = False
    complete_empty_proof: bool = False
    sealed: bool = False
    completeness_invalidated: bool = False

    @staticmethod
    def ordered_root(rows):
        import hashlib
        payload = "\\n".join(rows).encode("utf-8")
        return "sha256:" + hashlib.sha256(payload).hexdigest()

    def proves_membership(self, row, generation):
        return generation == self.generation and row in self.rows

    def seal_complete(self, declared_count, declared_root):
        if self.completeness_invalidated:
            raise ProtocolError("late discovery invalidated prior snapshot attestation")
        if not self.pagination_complete or not self.attested or not self.anti_rollback:
            raise ProtocolError("snapshot completeness evidence missing")
        if declared_count != len(self.rows):
            raise ProtocolError("snapshot count mismatch")
        if declared_root != self.ordered_root(self.rows):
            raise ProtocolError("snapshot ordered root mismatch")
        if not self.rows and not self.complete_empty_proof:
            raise ProtocolError("empty set requires signed COMPLETE_EMPTY proof")
        self.sealed = True
        return {"owner": self.owner, "generation": self.generation,
                "high_water": self.high_water, "count": declared_count,
                "root": declared_root}

    def discover_late_row(self, row):
        if row not in self.rows:
            self.rows.append(row)
            self.sealed = False
            self.completeness_invalidated = True


@dataclass
class RecoveryManifest:
    """Two disjoint evidence domains; never invent a cross-owner scalar order."""
    cutoff: dict | None = None
    reconciliation: dict | None = None

    def commit_cutoff(self, batch_ref, batch_digest, coc_prefix, owner_high_waters):
        candidate = {"batch_ref": batch_ref, "batch_digest": batch_digest,
                     "coc_prefix": coc_prefix,
                     "owner_high_waters": dict(owner_high_waters)}
        if self.cutoff and self.cutoff != candidate:
            raise ProtocolError("recovery cutoff pair is immutable")
        self.cutoff = candidate
        return self.cutoff

    def reconcile(self, coc_participants, owner_admissions):
        if not self.cutoff:
            raise ProtocolError("cutoff batch must commit before reconciliation")
        if self.reconciliation:
            candidate_digest = (tuple(coc_participants), tuple(owner_admissions))
            if self.reconciliation["inputs"] != candidate_digest:
                raise ProtocolError("recovery must resume the same manifest pair")
            return self.reconciliation
        prefix = self.cutoff["coc_prefix"]
        for item in coc_participants:
            if item["coc_position"] > prefix:
                raise ProtocolError("COC participant beyond frozen prefix")
        hwm = self.cutoff["owner_high_waters"]
        for item in owner_admissions:
            if item["owner"] not in hwm:
                raise ProtocolError("owner admission without owner-local cutoff")
            if item["owner_position"] > hwm[item["owner"]]:
                raise ProtocolError("owner admission beyond owner-local HWM")
        identities = [("COC", x["participant_ref"]) for x in coc_participants]
        identities += [(x["owner"], x["admission_ref"]) for x in owner_admissions]
        if len(identities) != len(set(identities)):
            raise ProtocolError("duplicate typed manifest member")
        import hashlib, json
        inputs = (tuple(coc_participants), tuple(owner_admissions))
        member_root = hashlib.sha256(
            json.dumps(identities, sort_keys=True).encode()).hexdigest()
        content_digest = hashlib.sha256(
            json.dumps(inputs, sort_keys=True).encode()).hexdigest()
        self.reconciliation = {
            "inputs": inputs,
            "member_set_root": member_root,
            "manifest_content_digest": content_digest,
            "manifest_record_entry_digest": hashlib.sha256(
                (content_digest + ":record").encode()).hexdigest(),
            "batch_digest": self.cutoff["batch_digest"],
            "batch_entry_digest": hashlib.sha256(
                (self.cutoff["batch_digest"] + ":entry").encode()).hexdigest()
        }
        return self.reconciliation


@dataclass
class FRecallProjection:
    """F candidates are hints only; every page is revalidated at the final gate."""
    candidates: dict = field(default_factory=dict)
    invalidated: set = field(default_factory=set)

    def index(self, ref, source_digest):
        self.candidates[ref] = {"source_digest": source_digest, "visible": True}

    def invalidate(self, ref):
        self.invalidated.add(ref)
        if ref in self.candidates:
            self.candidates[ref]["visible"] = False

    def return_page(self, refs, current_d, current_i, integrity_ok=True):
        returned = []
        for ref in refs:
            candidate = self.candidates.get(ref)
            if (not candidate or not candidate["visible"] or ref in self.invalidated
                    or ref not in current_d or ref not in current_i or not integrity_ok):
                continue
            returned.append(ref)
        return returned


@dataclass
class EDerivation:
    """Stable WorkItem/Attempt identity; expiry and DLQ never prove no publication."""
    work_item_id: str
    request_digest: str
    attempt: int = 0
    lease_id: str | None = None
    state: str = "REGISTERED"
    staged_digest: str | None = None
    storage_participant: str | None = None
    d_admission: str | None = None
    terminal_outcome: str | None = None

    def retry(self, request_digest):
        if request_digest != self.request_digest:
            raise ProtocolError("stable WorkItem identity changed request digest")
        if self.state in {"PUBLISHED", "NO_PUBLICATION"}:
            return self.attempt
        self.attempt += 1
        self.lease_id = f"{self.work_item_id}:lease:{self.attempt}"
        self.state = "LEASED"
        return self.attempt

    def stage_private(self, digest):
        if self.state != "LEASED":
            raise ProtocolError("attempt must hold a current lease before staging")
        self.staged_digest = digest
        self.state = "PRIVATE_STAGED"

    def prepare_storage(self, participant_ref):
        if self.state != "PRIVATE_STAGED":
            raise ProtocolError("private stage required before Storage prepare")
        self.storage_participant = participant_ref
        self.state = "STORAGE_PREPARED_HIDDEN"

    def admit_d(self, admission_ref):
        if self.state != "STORAGE_PREPARED_HIDDEN":
            raise ProtocolError("D publication admission requires durable Storage prepare")
        self.d_admission = admission_ref
        self.state = "D_ADMITTED"

    def resolve(self, outcome):
        if outcome not in {"COMMITTED_VISIBLE", "NO_PUBLICATION"}:
            self.state = "UNKNOWN_IN_DOUBT"
            raise UnknownOutcome("nonterminal outcome retains private stage and admission")
        if not self.storage_participant or not self.d_admission:
            raise ProtocolError("terminal resolution lacks Storage/D participant join")
        self.terminal_outcome = outcome
        self.state = "PUBLISHED" if outcome == "COMMITTED_VISIBLE" else "NO_PUBLICATION"
        return self.state


@dataclass
class GContextVersion:
    """G ContextVersion is non-canonical and every fragment retains D lineage."""
    version: int = 1
    fragments: dict = field(default_factory=dict)
    stale: bool = False
    deliveries: dict = field(default_factory=dict)

    def materialize(self, fragment_ref, source_refs, d_generation):
        if not source_refs:
            raise ProtocolError("Context derivative requires source lineage")
        if self.stale:
            raise ProtocolError("stale ContextVersion cannot be extended")
        self.fragments[fragment_ref] = {
            "source_refs": tuple(source_refs), "d_generation": d_generation}
        return self.version

    def apply_delta(self, base_version, fragment_ref, source_refs, d_generation):
        if base_version != self.version:
            raise ProtocolError("stale Snapshot/Delta base version")
        self.materialize(fragment_ref, source_refs, d_generation)
        self.version += 1
        return self.version

    def forget(self, forgotten_sources, current_d_generation):
        for fragment in self.fragments.values():
            if set(fragment["source_refs"]) & set(forgotten_sources):
                self.stale = True
        if self.stale:
            self.version += 1
            self.deliveries.clear()
        return {"version": self.version, "stale": self.stale,
                "d_generation": current_d_generation}

    def create_delivery(self, delivery_id, context_version, d_generation):
        if self.stale or context_version != self.version:
            raise ProtocolError("stale ContextVersion cannot be delivered")
        self.deliveries[delivery_id] = {
            "version": context_version, "d_generation": d_generation}
        return delivery_id

    def replay_delivery(self, delivery_id, current_d_generation):
        item = self.deliveries.get(delivery_id)
        if not item or self.stale or item["d_generation"] != current_d_generation:
            raise ProtocolError("old delivery/ACK is not replay authority")
        return True


@dataclass
class CProviderOutcome:
    """C may submit only an exact D-admitted, I-authorized immutable request."""
    intents: dict = field(default_factory=dict)
    provider_calls: dict = field(default_factory=dict)
    outcomes: dict = field(default_factory=dict)
    quarantined: set = field(default_factory=set)

    def admit_intent(self, intent_id, request_digest, d_participant_ref,
                     i_receipt, current_permission_epoch):
        old = self.intents.get(intent_id)
        if old:
            if old["request_digest"] != request_digest:
                raise ProtocolError("C intent immutable request digest conflict")
            return old
        if not d_participant_ref:
            raise ProtocolError("C provider intent requires exact D participant")
        if (not i_receipt or i_receipt.get("outcome") != "COMMIT_WON"
                or i_receipt.get("permission_epoch") != current_permission_epoch):
            raise ProtocolError("C provider intent requires current I COMMIT_WON proof")
        self.intents[intent_id] = {
            "request_digest": request_digest,
            "d_participant_ref": d_participant_ref,
            "i_receipt_ref": i_receipt.get("receipt_ref"),
            "permission_epoch": current_permission_epoch,
            "state": "ADMITTED"
        }
        return self.intents[intent_id]

    def submit(self, intent_id, provider_idempotency_key):
        intent = self.intents.get(intent_id)
        if not intent:
            raise ProtocolError("provider submit without admitted C intent")
        old = self.provider_calls.get(intent_id)
        if old:
            if old["idempotency_key"] != provider_idempotency_key:
                raise ProtocolError("unknown provider outcome must reuse same idempotency key")
            return old
        call = {"idempotency_key": provider_idempotency_key,
                "state": "SUBMITTED_UNKNOWN"}
        self.provider_calls[intent_id] = call
        intent["state"] = "SUBMITTED_UNKNOWN"
        return call

    def record_outcome(self, intent_id, provider_idempotency_key, outcome, digest):
        if outcome not in {"SUCCEEDED", "FAILED_NO_SIDE_EFFECT"}:
            raise ProtocolError("provider outcome must be a declared terminal outcome")
        call = self.provider_calls.get(intent_id)
        if not call or call["idempotency_key"] != provider_idempotency_key:
            raise ProtocolError("provider outcome does not bind exact invocation")
        previous = self.outcomes.get(intent_id)
        candidate = {"outcome": outcome, "digest": digest,
                     "idempotency_key": provider_idempotency_key}
        if previous and previous != candidate:
            self.quarantined.add(intent_id)
            raise ProtocolError("conflicting provider terminal outcomes")
        self.outcomes[intent_id] = candidate
        call["state"] = outcome
        self.intents[intent_id]["state"] = outcome
        return candidate

    def lookup_after_timeout(self, intent_id, provider_idempotency_key):
        call = self.provider_calls.get(intent_id)
        if not call or call["idempotency_key"] != provider_idempotency_key:
            raise ProtocolError("authoritative lookup must use same invocation key")
        return self.outcomes.get(intent_id, {"outcome": "UNKNOWN"})
