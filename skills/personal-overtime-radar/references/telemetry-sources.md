# Telemetry Sources Reference

This document outlines the multi-layered telemetry sources used to verify human work activity, physical presence, and after-hours engineering sessions on macOS.

---

## 1. Screenpipe Local SQLite Database

Screenpipe maintains a continuous local SQLite database at `~/.screenpipe/db.sqlite` containing OCR captures, UI events, and synthesized activity intervals.

### A. Activity Intervals Query
```sql
SELECT 
    id,
    start_time,
    end_time,
    duration,
    activity_type,
    app_name,
    window_title
FROM activity_intervals
WHERE start_time >= :start_iso AND end_time <= :end_iso
ORDER BY start_time ASC;
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
- If a time span lacks `ui_events` or OCR frame updates for more than 45 minutes, treat it as idle time and deduct it from the active session.

---

## 2. macOS Power Management & Sleep Logs

macOS records all sleep, wake, dark wake, and display power assertions in ASL files located in `/var/log/powermanagement/` and readable via `pmset`.

### A. Recent Sleep & Wake Events
```bash
pmset -g log | grep -E "Wake from|Sleep|Display is turned|PreventUserIdle"
```

### B. Historical ASL Query
```bash
syslog -d /var/log/powermanagement -k Time ge "YYYY-MM-DD 00:00:00" | grep -i "wake"
```
- A `Wake from Normal Sleep` event establishes when the machine resumed active operation.
- A `Sleep` or `ClamshellSleep` event establishes when the workstation was closed or suspended.

---

## 3. Physical Office Presence & Network Telemetry

To distinguish between in-office work and remote sessions, inspect active Wi-Fi interface details and DHCP lease information.

### A. Current Wi-Fi BSSID and SSID
```bash
system_profiler SPAirPortDataType | grep -A 10 "Current Network Information"
```
Or via the Apple80211 tool:
```bash
/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport -I
```

### B. Gateway and IP Configuration
```bash
ipconfig getsummary en0 | grep -E "Router|IPAddress|Subnet"
```
- An IP on `10.15.0.0/24` with Gateway `10.15.0.1` and SSID `Snappi_Stadiou` confirms physical presence at headquarters.

---

## 4. Multi-Repository Git Commit Activity

Inspect local Git repositories for commits authored by the user during evening hours.

```bash
git -C <repo_path> log --all --since="YYYY-MM-DD 16:30" --until="YYYY-MM-DD 23:59" \
    --author="Koletsos" --pretty=format:"%h %ad %s" --date=iso
```
- Late-night commits provide irrefutable, cryptographic evidence of active engineering delivery.

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
- Meeting subjects and attendees provide primary justification candidates (Choice A).
