#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
id ai-owner-worker >/dev/null 2>&1 || useradd --system --home /var/lib/ai-owner-worker --shell /usr/sbin/nologin ai-owner-worker
install -d -o root -g root -m 0755 /opt/ai-owner-worker
install -o root -g root -m 0755 "$ROOT/automation/owner_worker.py" /opt/ai-owner-worker/owner_worker.py
install -d -o root -g ai-owner-worker -m 0750 /etc/ai-owner-worker
if [ ! -e /etc/ai-owner-worker/worker.env ]; then
  install -o root -g ai-owner-worker -m 0640 "$ROOT/automation/worker.env.example" /etc/ai-owner-worker/worker.env
  echo "Created /etc/ai-owner-worker/worker.env. Populate credentials out-of-band before starting the service."
fi
install -o root -g root -m 0644 "$ROOT/automation/systemd/ai-owner-worker.service" /etc/systemd/system/ai-owner-worker.service
systemctl daemon-reload
echo "Installed. Review worker.env, then run: systemctl enable --now ai-owner-worker"
