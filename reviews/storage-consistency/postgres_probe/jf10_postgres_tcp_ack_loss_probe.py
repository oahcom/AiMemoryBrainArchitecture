"""Real TCP server-response loss probe for PostgreSQL JF-10 outcomes.

A one-shot TCP proxy drops the PostgreSQL CommandComplete frame for PREPARE
TRANSACTION, COMMIT PREPARED and ROLLBACK PREPARED. The client therefore
observes a broken connection / UNKNOWN result while the server has already
executed the command. Recovery reconnects directly and inspects the same XID.
This is a CI fault-injection test, not production I sequencer/COC integration.
"""
from __future__ import annotations

import socket
import struct
import threading
import time

import psycopg
from psycopg import OperationalError

PG = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "jf10-ci-only",
    "autocommit": True,
    "connect_timeout": 5,
    "sslmode": "disable",
}
CASES = {
    "prepare": ("jf10_tcp_ack_prepare_001", "op-tcp-ack-prepare"),
    "commit": ("jf10_tcp_ack_commit_001", "op-tcp-ack-commit"),
    "rollback": ("jf10_tcp_ack_rollback_001", "op-tcp-ack-rollback"),
}


class DropCommandCompleteProxy:
    def __init__(self, target_tag: str):
        self.target_tag = target_tag
        self.listener = socket.socket()
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(("127.0.0.1", 0))
        self.listener.listen(1)
        self.port = self.listener.getsockname()[1]
        self.dropped = threading.Event()
        self.error = None
        self.client = None
        self.backend = None
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _close(self):
        for s in (self.client, self.backend, self.listener):
            if s is not None:
                try:
                    s.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    s.close()
                except OSError:
                    pass

    def _serve(self):
        try:
            self.client, _ = self.listener.accept()
            self.backend = socket.create_connection(("127.0.0.1", 5432), timeout=5)
            threading.Thread(target=self._client_to_backend, daemon=True).start()
            self._backend_to_client()
        except Exception as exc:
            self.error = repr(exc)
        finally:
            self._close()

    def _client_to_backend(self):
        try:
            while True:
                data = self.client.recv(65536)
                if not data:
                    return
                self.backend.sendall(data)
        except OSError:
            return

    def _backend_to_client(self):
        buf = bytearray()
        while True:
            chunk = self.backend.recv(65536)
            if not chunk:
                return
            buf.extend(chunk)
            while len(buf) >= 5:
                msg_len = struct.unpack("!I", buf[1:5])[0]
                total = 1 + msg_len
                if msg_len < 4 or len(buf) < total:
                    break
                frame = bytes(buf[:total])
                del buf[:total]
                msg_type = frame[0:1]
                payload = frame[5:]
                if msg_type == b"C":
                    tag = payload.rstrip(b"\x00").decode("utf-8", "replace")
                    if tag == self.target_tag:
                        # Do not forward CommandComplete: server-side command
                        # has run, but client cannot observe its acknowledgement.
                        self.dropped.set()
                        return
                self.client.sendall(frame)

    def wait(self, timeout=10):
        if not self.dropped.wait(timeout):
            raise RuntimeError(
                f"proxy did not intercept {self.target_tag}; error={self.error}"
            )


def connect_direct():
    return psycopg.connect(**PG)


def setup():
    with connect_direct() as c:
        version = c.execute("SHOW server_version").fetchone()[0]
        assert version.startswith("18.7 "), version
        settings = {
            k: c.execute("SHOW " + k).fetchone()[0]
            for k in ("max_prepared_transactions", "fsync", "synchronous_commit", "full_page_writes")
        }
        assert int(settings["max_prepared_transactions"]) >= 8, settings
        assert all(settings[k] == "on" for k in ("fsync", "synchronous_commit", "full_page_writes")), settings
        c.execute("DROP TABLE IF EXISTS jf10_tcp_receipt")
        c.execute("DROP TABLE IF EXISTS jf10_tcp_visibility")
        c.execute("DROP TABLE IF EXISTS jf10_tcp_lock")
        c.execute("CREATE TABLE jf10_tcp_lock (id integer PRIMARY KEY, marker text NOT NULL)")
        c.execute("INSERT INTO jf10_tcp_lock VALUES (1, 'tcp-ack-guard')")
        c.execute("CREATE TABLE jf10_tcp_visibility (operation_id text PRIMARY KEY, pointer text NOT NULL)")
        c.execute("CREATE TABLE jf10_tcp_receipt (operation_id text PRIMARY KEY, digest text NOT NULL)")
    print(f"SERVER_VERSION={version}")
    print(f"SERVER_SETTINGS={settings}")


def connect_proxy(proxy: DropCommandCompleteProxy):
    return psycopg.connect(
        host="127.0.0.1",
        port=proxy.port,
        dbname=PG["dbname"],
        user=PG["user"],
        password=PG["password"],
        autocommit=True,
        connect_timeout=5,
        sslmode="disable",
    )


def expect_unknown(proxy: DropCommandCompleteProxy, command):
    observed_unknown = False
    try:
        with connect_proxy(proxy) as c:
            command(c)
    except (OperationalError, OSError):
        observed_unknown = True
    proxy.wait()
    assert observed_unknown, "client unexpectedly observed successful command acknowledgement"
    print(f"CLIENT_OBSERVED_UNKNOWN_AFTER_{proxy.target_tag.replace(' ', '_')}=PASS")


def prepared_state(xid):
    with connect_direct() as c:
        return c.execute("SELECT gid FROM pg_prepared_xacts WHERE gid=%s", (xid,)).fetchone()


def visible_pair(op):
    with connect_direct() as c:
        p = c.execute("SELECT pointer FROM jf10_tcp_visibility WHERE operation_id=%s", (op,)).fetchone()
        r = c.execute("SELECT digest FROM jf10_tcp_receipt WHERE operation_id=%s", (op,)).fetchone()
    return p, r


def assert_private(op):
    assert visible_pair(op) == (None, None), visible_pair(op)


def assert_lock_retained():
    with connect_direct() as c:
        c.execute("BEGIN")
        c.execute("SET LOCAL lock_timeout='500ms'")
        try:
            c.execute("UPDATE jf10_tcp_lock SET marker='must-not-pass' WHERE id=1")
        except psycopg.errors.LockNotAvailable:
            c.execute("ROLLBACK")
            return
        c.execute("ROLLBACK")
    raise AssertionError("prepared participant lock not retained after lost PREPARE ACK")


def prepare_with_lost_tcp_ack():
    xid, op = CASES["prepare"]
    proxy = DropCommandCompleteProxy("PREPARE TRANSACTION")

    def command(c):
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute("SELECT id FROM jf10_tcp_lock WHERE id=1 FOR UPDATE")
        c.execute("INSERT INTO jf10_tcp_visibility VALUES (%s, %s)", (op, "private:" + op))
        c.execute("INSERT INTO jf10_tcp_receipt VALUES (%s, %s)", (op, "sha256:" + op))
        c.execute(f"PREPARE TRANSACTION '{xid}'")

    expect_unknown(proxy, command)
    assert prepared_state(xid) == (xid,), "same XID not prepared after lost TCP ACK"
    assert_private(op)
    assert_lock_retained()
    print("TCP_ACK_LOST_AFTER_PREPARE_SAME_XID_RECOVERED=PASS")
    print("PREPARE_LOST_ACK_NO_PUBLICATION=PASS")


def prepare_direct(kind):
    xid, op = CASES[kind]
    with connect_direct() as c:
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute("SELECT id FROM jf10_tcp_lock WHERE id=1 FOR UPDATE")
        c.execute("INSERT INTO jf10_tcp_visibility VALUES (%s, %s)", (op, "private:" + op))
        c.execute("INSERT INTO jf10_tcp_receipt VALUES (%s, %s)", (op, "sha256:" + op))
        c.execute(f"PREPARE TRANSACTION '{xid}'")
    assert prepared_state(xid) == (xid,)
    assert_private(op)


def terminal_with_lost_tcp_ack(kind):
    xid, op = CASES[kind]
    decision = "COMMIT" if kind == "commit" else "ROLLBACK"
    tag = decision + " PREPARED"
    proxy = DropCommandCompleteProxy(tag)

    def command(c):
        c.execute(f"{decision} PREPARED '{xid}'")

    expect_unknown(proxy, command)
    assert prepared_state(xid) is None, "same XID still prepared after terminal command"
    pointer, receipt = visible_pair(op)
    if decision == "COMMIT":
        assert pointer == ("private:" + op,), pointer
        assert receipt == ("sha256:" + op,), receipt
        print("TCP_ACK_LOST_AFTER_COMMIT_SAME_XID_RECONCILED=PASS")
        print("COMMIT_POINTER_RECEIPT_ATOMIC_VISIBILITY=PASS")
    else:
        assert pointer is None and receipt is None, (pointer, receipt)
        print("TCP_ACK_LOST_AFTER_ROLLBACK_SAME_XID_RECONCILED=PASS")
        print("ROLLBACK_NON_PUBLICATION=PASS")


def main():
    setup()
    prepare_with_lost_tcp_ack()
    # Resolve the prepared XID by the exact original identity after UNKNOWN.
    terminal_with_lost_tcp_ack("prepare")
    for kind in ("commit", "rollback"):
        prepare_direct(kind)
        terminal_with_lost_tcp_ack(kind)
    print("JF10_POSTGRESQL_TCP_ACK_LOSS_RECOVERY=PASS")
    print("LIMITATION=CI_PROXY_TEST_NOT_PRODUCTION_I_SEQUENCER_OR_COC")


if __name__ == "__main__":
    main()
