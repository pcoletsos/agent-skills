---
name: check-service-flows
description: Audit live service flows, operational health, failed systemd units, Docker container states, and runtime error logs across micro-kolbr00 and local environments.
version: 0.1.0
status: draft
---

# Check Service Flows Skill

## Purpose
Inspect, diagnose, and audit operational service flows, system downtime, failed systemd units, Docker container health, and background automation pipelines across `micro-kolbr00` and local environments.

---

## When to Use
- A user asks:
  - "Check service flows"
  - "Are any services down?"
  - "Check service health"
  - "What services are down?"
  - "Audit systemd services"
  - "Inspect KIMDIS scraper flow"
  - "Inspect Alert Gateway flow"
  - "Show service errors or downtime"
- You suspect a pipeline has stalled, failed to fire, or crashed silently.
- You need to verify that background daemons, timers, or Docker containers are healthy before or after a deployment.

---

## Fast Automated Execution

Use the repository's companion CLI script for instant health auditing:

```bash
# 1. Executive Health Dashboard
# Audits host CPU/RAM/Disk, failed units, all monitored systemd services, and Docker containers.
python scripts/check_service_flows.py

# 2. Down or Degraded Filter
# Shows strictly services, containers, or units that are stopped, failed, or unhealthy.
python scripts/check_service_flows.py --down

# 3. Deep Flow Inspection: KIMDIS Daily Tender Digest
# Checks timer schedule, next run countdown, last execution exit status, and recent scraper logs.
python scripts/check_service_flows.py --flow kimdis

# 4. Deep Flow Inspection: SD-03 Alert Gateway & HR Expiries
# Checks PostgreSQL container health on port 55432, worker polling loop, and Socket Mode listener.
python scripts/check_service_flows.py --flow gateway

# 5. Deep Flow Inspection: Docker Workload Health
# Audits all 15 active container states, health checks, and uptimes.
python scripts/check_service_flows.py --flow docker

# 6. Deep Flow Inspection: Telemetry & Error Alerting
# Checks Uptime Kuma webhook receiver on port 8765 and single-pane observability dashboard.
python scripts/check_service_flows.py --flow telemetry

# 7. Tail Recent Host Error Logs
# Displays the last 25 critical journalctl errors (journalctl -p err..emerg).
python scripts/check_service_flows.py --logs

# 8. Machine-Readable JSON Export
# Outputs structured JSON metrics for programmatic inspection or agent parsing.
python scripts/check_service_flows.py --json
```

---

## Manual Diagnostic Procedures

If the CLI script is unavailable or deep interactive diagnosis is required via SSH to `micro-kolbr00`:

### Procedure 1: Check Failed Systemd Units
```bash
ssh micro-kolbr00 "systemctl list-units --state=failed --no-pager"
```
If any unit is listed as failed:
```bash
ssh micro-kolbr00 "journalctl -u <unit_name> -n 30 --no-pager"
```

### Procedure 2: Verify Monitored Consultation Daemons
```bash
ssh micro-kolbr00 "systemctl is-active \
  sd01-kimdis-daily-digest.timer \
  sd03-kimdis-feedback-slack.service \
  sd03-alert-gateway-slack.service \
  sd03-alert-gateway-worker.service \
  kuma-debug-webhook.service \
  observability-dashboard.service"
```

### Procedure 3: Verify Docker Container Health
```bash
ssh micro-kolbr00 "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.State}}'"
```
Check specifically for:
- `sd03-alert-gateway-postgres-1`: Must be `Up (healthy)`.
- `uptime-kuma`: Must be `Up (healthy)`.
- `bookstack_app` and `bookstack_db`: Must be `Up`.

### Procedure 4: Check Daily Timer Schedules
```bash
ssh micro-kolbr00 "systemctl list-timers | grep kimdis"
```
Verify the timer is waiting and that the next trigger date/time matches the scheduled run window (08:00 Athens time).

### Procedure 5: Check Host Resource Utilization
```bash
ssh micro-kolbr00 "uptime; free -h; df -h /"
```
Ensure available disk space is >5 GiB and RAM usage is below 85%.

---

## Key Monitored Flows & Architecture

1. **KIMDIS Tender Digest Pipeline (`sd01`)**:
   - `sd01-kimdis-daily-digest.timer`: Fires daily at 05:00 UTC (08:00 Athens).
   - `sd01-kimdis-daily-digest.service`: Runs `run_digest.sh`, queries KIMDIS API, posts notices to `#alerts-kimdis`.
   - `sd03-kimdis-feedback-slack.service`: Socket Mode listener handling client review buttons and error report modals.

2. **Alert Gateway Pipeline (`sd03`)**:
   - `sd03-alert-gateway-postgres-1`: PostgreSQL 16 database storing contract schedules and audit outbox.
   - `sd03-alert-gateway-worker.service`: Delivery daemon claiming due alerts and dispatching to `#alerts-hr-ergani`.
   - `sd03-alert-gateway-slack.service`: Socket Mode listener recording user button clicks and acknowledgements.

3. **Engineering Telemetry & Alerting Pipeline**:
   - `kuma-debug-webhook.service`: Webhook receiver on port 8765 forwarding Uptime Kuma events to `#kolnetic-debug`.
   - `slack-failure-alert@.service`: Systemd template unit bound via `OnFailure=` to dispatch P1 cards if any persistent service crashes.
   - `observability-dashboard.service`: Single-pane-of-glass metrics API running on port 8888.

---

## Output Report Formats

### Executive Health Dashboard Format
```markdown
# Service Flow & Infrastructure Health Dashboard
**Target Host:** `micro-kolbr00`  |  **Architecture:** Linux x86_64

## 🖥️ Host Resource Health
- **CPU Utilization**: 0.5%
- **RAM Usage**: 42.1%
- **Disk Space**: 24.3% used (57.1 GiB free)
- **Load Average (1m, 5m, 15m)**: [0.18, 0.35, 0.28]

✅ **No failed systemd units detected on host.**

## ⚙️ Monitored Consultation Services (Systemd)
| Service / Unit | Flow | Type | State | Status |
|---|---|---|---|---|
| `sd01-kimdis-daily-digest.timer` | `kimdis` | timer | `active` | 🟢 |
| `sd03-kimdis-feedback-slack.service` | `kimdis` | daemon | `active` | 🟢 |
| `sd03-alert-gateway-slack.service` | `gateway` | daemon | `active` | 🟢 |
| `sd03-alert-gateway-worker.service` | `gateway` | daemon | `active` | 🟢 |
| `kuma-debug-webhook.service` | `telemetry` | daemon | `active` | 🟢 |

## 🐳 Docker Workload Health
| Container | State | Status | Health |
|---|---|---|---|
| `sd03-alert-gateway-postgres-1` | `running` | Up 4 weeks (healthy) | 🟢 |
| `uptime-kuma` | `running` | Up 4 weeks (healthy) | 🟢 |
```

---

## Operating Rules
- **No Em Dashes**: Never use em dashes in any response text, output reports, or documentation.
- **Safe Probing**: Always use non-destructive status checks (`systemctl status`, `docker ps`, `curl`). Do not restart or stop production services without explicit confirmation.
- **Credential Hygiene**: Never output unredacted tokens, database passwords, or auth headers into logs or summary reports.

---

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
