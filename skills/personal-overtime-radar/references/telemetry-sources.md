# Telemetry Sources Reference

This document outlines the multi-layered telemetry sources used to verify human work activity, physical presence, and after-hours engineering sessions on macOS.

---

## 1. Screenpipe Local SQLite Database

Screenpipe maintains a continuous local SQLite database at `~/.screenpipe/db.sqlite` containing OCR captures, UI events, and synthesized activity intervals.

### A. Activity Intervals Query
```sql
SELECT 
    start_at,
    end_at,
    t.title,
    t.app_name
FROM activity_intervals i
JOIN activity_tasks t ON i.task_id = t.id
WHERE i.start_at >= :start_iso AND i.start_at <= :end_iso
ORDER BY i.start_at ASC;
```

### B. Human UI Events Verification (Click & Keystroke Evidence)
To verify that an active interval was not passive background activity, query `ui_events`:
```sql
SELECT 
    timestamp,
    event_type,
    app_name,
    window_title
FROM ui_events
WHERE timestamp >= :start_iso AND timestamp <= :end_iso
ORDER BY timestamp ASC;
```
- If a time span lacks `ui_events` or OCR frame updates for more than 45 minutes on remote days, treat it as idle time and deduct it from the active session.

---

## 2. macOS Power Management & Sleep Logs

macOS records all sleep, wake, dark wake, and display power assertions in ASL files located in `/var/log/powermanagement/` and readable via `pmset`.

### A. Recent Sleep & Wake Events
```bash
pmset -g log | grep -E "Wake from|Sleep|Display is turned|PreventUserIdle"
```

### B. Departure Sleep Detection
When packing up at the office, macOS enters a `Software Sleep` or `Clamshell Sleep` state (often switching to battery power):
```bash
pmset -g log | grep -E "Entering Sleep state"
```
This timestamp marks the end of on-site presence.

---

## 3. Physical Office Presence & Network Telemetry

To distinguish between in-office work and remote sessions, inspect active Wi-Fi interface details, DHCP lease information, and `/var/log/wifi.log*`.

### A. Known Snappi Office Network Signatures

| Office Location | SSIDs | Default Gateway IPs | Interfaces & Hardware |
| :--- | :--- | :--- | :--- |
| **Corporate Hub (Athens)** | `Corporate_Hub` | `10.25.150.1` (Wi-Fi)<br>`10.25.0.1` (Wired) | `en0` (Wi-Fi), `en7` (USB LAN Dock), FortiGate 90G (`FGT90G...`) |
| **Stadiou HQ (Athens)** | `Snappi_Stadiou` | `10.15.0.1` (VLAN 10)<br>`10.15.20.1` (VLAN 20)<br>`10.212.134.1` (Site VPN) | `en0` (Wi-Fi), corporate Ethernet |
| **Ioannina Office** | `Snappi_Ioannina` | `10.10.190.1`<br>`10.212.100.1` | `en0` (Wi-Fi), local gateway |

### B. Live Interface Inspection
Check active adapters (`en0`, `en7`, `en3`, `en4`, `en5`) via `ipconfig getsummary`:
```bash
ipconfig getsummary en0 | grep -E "SSID|Router|server_identifier|Option_224"
ipconfig getsummary en7 | grep -E "Router|server_identifier|Option_224"
```
Presence of `SSID : Corporate_Hub`, `Router : 10.25.150.1`, `Router : 10.25.0.1`, or Option 224 carrying FortiGate serial numbers confirms on-site presence.

### C. Historical Gateway Parsing (`wifi.log`)
macOS logs DHCP gateway assignments to `/var/log/wifi.log` and compressed archives `/var/log/wifi.log.*.bz2`:
```bash
bzgrep -E "Default Gateway IP Address: (10\.25\.|10\.15\.|10\.10\.)" /var/log/wifi.log*
```
Matches on office gateways establish the exact dates the user worked on premises.

---

## 4. Multi-Repository Git Commit Activity

When Screenpipe is inactive or encounters gaps, authored Git commits provide cryptographic evidence of engineering work:
```bash
git -C <repo_path> log --all --since="YYYY-MM-DD 16:30" --until="YYYY-MM-DD 23:59" \
    --author="Koletsos" --pretty=format:"%cI|%s"
```
The radar automatically inspects `~/repos/SNAPPI/*` and `~/repos/engineering/*`.

---

## 5. Microsoft 365 Calendar & Sent Messages

Query live Outlook and Teams data using the CLI for Microsoft 365 (`m365`) to identify after-hours calls and correspondence.

### A. Late Meetings & Calls
```bash
m365 outlook event list --startDateTime "YYYY-MM-DDT16:30:00Z" --endDateTime "YYYY-MM-DDT23:59:59Z" -o json
```

### B. Sent Communications
```bash
m365 outlook message list --folderId "SentItems" --filter "sentDateTime ge YYYY-MM-DDT16:30:00Z" -o json
```
Meeting subjects and attendees provide primary justification candidates (Choice A).
