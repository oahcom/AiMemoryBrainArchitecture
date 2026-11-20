#!/usr/bin/env python3
"""REQ-08 bounded portable exchange fixture; Python stdlib only, not production auth/BMCP."""
from __future__ import annotations
import argparse, copy, hashlib, hmac, json, os, sqlite3, tempfile
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

CONTRACT = "ai-memory-portable-exchange/1.0"
SCHEMA_V1 = 1
TERMINAL = {"forgotten"}

class Denied(PermissionError):
    pass

def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()

@dataclass(frozen=True)
class Principal:
    tenant: str
    workspace: str
    agent: str
    provider: str
    model: str

@dataclass(frozen=True)
class Record:
    record_id: str
    resource: str
    tenant: str
    workspace: str
    content: str
    lifecycle: str
    version: int
    source_agent: str
    source_provider: str
    source_model: str
    lineage: tuple[str, ...]
    provenance: dict[str, Any]
    created_at: str
    updated_at: str
    def json(self):
        d = asdict(self); d["lineage"] = list(self.lineage); return d
    @classmethod
    def from_json(cls, d):
        x = dict(d); x["lineage"] = tuple(x["lineage"]); return cls(**x)

@dataclass(frozen=True)
class Grant:
    grant_id: str
    issuer: str
    tenant: str
    workspace: str
    agent: str
    audience: str
    resource: str
    actions: tuple[str, ...]
    expires_at: int
    delegation_chain: tuple[str, ...]
    parent_grant: str | None = None
    def json(self):
        d = asdict(self); d["actions"] = list(self.actions); d["delegation_chain"] = list(self.delegation_chain); return d
    @classmethod
    def from_json(cls, d):
        x = dict(d); x["actions"] = tuple(x["actions"]); x["delegation_chain"] = tuple(x["delegation_chain"]); return cls(**x)

class TestAuthority:
    """Local HMAC issuer/trust fixture. Key is test-only, never production identity."""
    def __init__(self, issuer="fixture://req08/authority", key=b"REQ08-LOCAL-ONLY-KEY-ROTATE-IN-PRODUCTION"):
        self.issuer, self._key = issuer, key
        self.trust = {issuer: key}
        self.revoked: set[str] = set()
        self.issued: dict[str, Grant] = {}
    def issue(self, *, tenant, workspace, agent, audience, resource, actions,
              expires_at=4_102_444_800, delegation_chain=None, parent_grant=None):
        chain = tuple(delegation_chain or (self.issuer, agent))
        g = Grant("grant-" + hashlib.sha256((tenant+workspace+agent+resource+str(len(self.issued))).encode()).hexdigest()[:12],
                  self.issuer, tenant, workspace, agent, audience, resource, tuple(sorted(set(actions))),
                  expires_at, chain, parent_grant)
        if len(chain) < 2 or chain[0] != self.issuer or chain[-1] != agent:
            raise ValueError("INVALID_DELEGATION_CHAIN")
        if parent_grant:
            parent = self.issued.get(parent_grant)
            if parent is None or "delegate" not in parent.actions:
                raise ValueError("DELEGATION_NOT_AUTHORIZED")
            if (parent.tenant, parent.workspace, parent.resource) != (tenant, workspace, resource):
                raise ValueError("DELEGATION_SCOPE_ESCALATION")
            if not set(actions).issubset(parent.actions):
                raise ValueError("DELEGATION_ACTION_ESCALATION")
        self.issued[g.grant_id] = g
        claims = g.json()
        return {"claims": claims, "signature": hmac.new(self._key, canonical(claims), hashlib.sha256).hexdigest()}
    def revoke(self, grant_id): self.revoked.add(grant_id)
    def verify(self, token, principal, resource, action, now=1_800_000_000):
        try:
            claims, signature = token["claims"], token["signature"]
            issuer, key = claims["issuer"], self.trust[claims["issuer"]]
        except (KeyError, TypeError):
            raise Denied("UNTRUSTED_ISSUER_OR_MALFORMED_GRANT")
        expected = hmac.new(key, canonical(claims), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, str(signature)): raise Denied("GRANT_SIGNATURE_INVALID")
        try: g = Grant.from_json(claims)
        except (KeyError, TypeError): raise Denied("GRANT_CLAIMS_INVALID")
        if g.grant_id in self.revoked: raise Denied("GRANT_REVOKED")
        if g.expires_at <= now: raise Denied("GRANT_EXPIRED")
        if g.issuer != self.issuer: raise Denied("UNTRUSTED_ISSUER")
        if (g.tenant, g.workspace, g.agent, g.audience) != (principal.tenant, principal.workspace, principal.agent, principal.agent):
            raise Denied("PRINCIPAL_SCOPE_MISMATCH")
        if g.resource != resource: raise Denied("RESOURCE_SCOPE_MISMATCH")
        if action not in g.actions: raise Denied("ACTION_NOT_GRANTED")
        if len(g.delegation_chain) < 2 or g.delegation_chain[0] != g.issuer or g.delegation_chain[-1] != g.agent:
            raise Denied("INVALID_DELEGATION_CHAIN")
        if g.parent_grant:
            parent = self.issued.get(g.parent_grant)
            if parent is None or "delegate" not in parent.actions or parent.grant_id in self.revoked:
                raise Denied("DELEGATION_PARENT_INVALID")
            if (parent.tenant, parent.workspace, parent.resource) != (g.tenant, g.workspace, g.resource) or not set(g.actions).issubset(parent.actions):
                raise Denied("DELEGATION_SCOPE_ESCALATION")
        return g

class AdapterV1(ABC):
    contract_version = CONTRACT
    def __init__(self, authority, principal): self.authority, self.principal = authority, principal
    def _auth(self, token, record, action):
        self.authority.verify(token, self.principal, record.resource, action)
        if (record.tenant, record.workspace) != (self.principal.tenant, self.principal.workspace):
            raise Denied("RECORD_SCOPE_MISMATCH")
        if record.lifecycle in TERMINAL and action in {"read", "share", "export"}:
            raise Denied("RECORD_NOT_EXPORTABLE")
    @abstractmethod
    def _put(self, record): ...
    @abstractmethod
    def _get(self, record_id): ...
    def write(self, record, token):
        self._auth(token, record, "write"); self._put(record)
    def read(self, record_id, token):
        record = self._get(record_id); self._auth(token, record, "read"); return record
    def export(self, record_id, token):
        record = self._get(record_id); self._auth(token, record, "read"); self._auth(token, record, "export")
        body = {"contract": CONTRACT, "schema_version": SCHEMA_V1, "record": record.json()}
        return {**body, "content_sha256": digest(body)}
    def import_record(self, envelope, token):
        body = {k: envelope[k] for k in ("contract", "schema_version", "record")}
        if envelope.get("contract") != CONTRACT or envelope.get("schema_version") != SCHEMA_V1:
            raise ValueError("UNSUPPORTED_EXCHANGE_CONTRACT")
        if not hmac.compare_digest(digest(body), str(envelope.get("content_sha256", ""))):
            raise ValueError("EXCHANGE_DIGEST_MISMATCH")
        record = Record.from_json(envelope["record"])
        self._auth(token, record, "import"); self._auth(token, record, "write")
        self._put(record); return record
    def share(self, record_id, token):
        record = self._get(record_id); self._auth(token, record, "share")
        return self.export(record_id, token)

class JsonFileAdapter(AdapterV1):
    """Provider A: atomic canonical JSON document store."""
    provider_id = "provider-json"
    def __init__(self, path, authority, principal):
        super().__init__(authority, principal); self.path = Path(path)
        if not self.path.exists(): self.path.write_text("{}", encoding="utf-8")
    def _all(self): return json.loads(self.path.read_text(encoding="utf-8"))
    def _put(self, record):
        data = self._all(); data[record.record_id] = record.json()
        tmp = self.path.with_suffix(self.path.suffix + ".tmp"); tmp.write_bytes(canonical(data)); os.replace(tmp, self.path)
    def _get(self, record_id):
        try: return Record.from_json(self._all()[record_id])
        except KeyError: raise KeyError("RECORD_NOT_FOUND")

class SQLiteAdapter(AdapterV1):
    """Provider B: relational SQLite store with explicit row identity."""
    provider_id = "provider-sqlite"
    def __init__(self, path, authority, principal):
        super().__init__(authority, principal); self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, payload BLOB NOT NULL)")
    def _put(self, record):
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO records(record_id,payload) VALUES(?,?) ON CONFLICT(record_id) DO UPDATE SET payload=excluded.payload", (record.record_id, canonical(record.json())))
    def _get(self, record_id):
        with sqlite3.connect(self.path) as db: row = db.execute("SELECT payload FROM records WHERE record_id=?", (record_id,)).fetchone()
        if row is None: raise KeyError("RECORD_NOT_FOUND")
        return Record.from_json(json.loads(row[0]))

def make_record():
    return Record("record.alpha.001", "memory.demo.001", "tenant.red", "workspace.blue",
      "Preserve source identity and lineage when replacing a provider.", "active", 3,
      "agent.alpha", "provider-json", "model-alpha-v3", ("event.001", "record.alpha.001"),
      {"source_event":"event.001", "captured_by":"agent.alpha", "evidence_sha256":"a"*64},
      "2026-11-20T00:00:00Z", "2026-11-20T00:00:00Z")

def fixture_grant(authority, agent="agent.alpha", actions=None, resource="memory.demo.001", workspace="workspace.blue", tenant="tenant.red", **kw):
    return authority.issue(tenant=tenant, workspace=workspace, agent=agent, audience=agent, resource=resource,
                           actions=actions or ["read","write","import","export","share"], **kw)

def migrate_v1_to_v2(envelope):
    if envelope["schema_version"] != 1: raise ValueError("MIGRATION_SOURCE_VERSION")
    record = copy.deepcopy(envelope["record"]); record["retention_class"] = "standard"
    body = {"contract": CONTRACT, "schema_version": 2, "record": record}
    return {**body, "content_sha256": digest(body)}

def rollback_v2_to_v1(envelope, backup_v1):
    if envelope["schema_version"] != 2 or backup_v1["schema_version"] != 1: raise ValueError("ROLLBACK_VERSION_MISMATCH")
    if envelope["record"].keys() - {"retention_class"} != backup_v1["record"].keys(): raise ValueError("ROLLBACK_SHAPE_MISMATCH")
    restored = copy.deepcopy(backup_v1)
    if digest({k: restored[k] for k in ("contract","schema_version","record")}) != restored["content_sha256"]:
        raise ValueError("ROLLBACK_BACKUP_CORRUPT")
    return restored

def demo():
    with tempfile.TemporaryDirectory() as d:
        authority=TestAuthority(); p=Principal("tenant.red","workspace.blue","agent.alpha","provider-json","model-alpha-v3")
        source=JsonFileAdapter(Path(d)/"a.json",authority,p); target=SQLiteAdapter(Path(d)/"b.sqlite",authority,p)
        record=make_record(); token=fixture_grant(authority)
        source.write(record, token); first=source.export(record.record_id,token)
        imported=target.import_record(first,token); second=target.export(imported.record_id,token)
        back=source.import_record(second,token); third=source.export(back.record_id,token)
        assert first == second == third
        print("ROUND_TRIP=PASS (export->SQLite import->re-export->JSON import->re-export; byte-identical envelope)")
        print("IDENTITY_LINEAGE_LIFECYCLE_PROVENANCE=PRESERVED")
        print("PROVIDER_SUBSTITUTION=provider-json -> provider-sqlite -> provider-json")
        migrated=migrate_v1_to_v2(third); rolled=rollback_v2_to_v1(migrated,third); assert rolled == third
        print("MIGRATION=1->2 retention_class=standard; ROLLBACK=2->1 exact snapshot restored")
        print("AUTHORITY=HMAC-SHA256 fixture issuer verified; production credentials=NOT USED")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("command", choices=["demo","migration-demo"]); args=ap.parse_args()
    if args.command == "demo": demo()
    else:
        e={"contract":CONTRACT,"schema_version":1,"record":make_record().json()}; e["content_sha256"]=digest(e)
        m=migrate_v1_to_v2(e); r=rollback_v2_to_v1(m,e); assert r==e
        print("MIGRATION_ROLLBACK=PASS schema 1 -> 2 -> 1; original envelope restored exactly")
    return 0
if __name__ == "__main__": raise SystemExit(main())
