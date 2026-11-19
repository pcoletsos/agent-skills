#!/usr/bin/env python3
"""
Personal Overtime Radar Engine
Performs forensic telemetry extraction, office location detection, session clustering,
payroll increment rounding, Excel generation, and macOS clipboard staging for after-hours engineering overtime.
"""

import argparse
import bz2
import datetime
import glob
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path


KNOWN_OFFICE_GATEWAYS = {
    "10.25.150.1": "Corporate Hub (Athens)",
    "10.25.0.1": "Corporate Hub (Athens - Wired)",
    "10.15.0.1": "Stadiou HQ (Athens)",
    "10.15.20.1": "Stadiou HQ (Athens - VLAN 20)",
    "10.10.190.1": "Ioannina Office",
    "10.212.134.1": "Stadiou HQ (Athens - Site VPN)",
    "10.212.100.1": "Ioannina Office (Site VPN)",
}

KNOWN_OFFICE_SSIDS = {
    "Corporate_Hub": "Corporate Hub (Athens)",
    "Snappi_Stadiou": "Stadiou HQ (Athens)",
    "Snappi_Ioannina": "Ioannina Office",
}


PASSIVE_BACKGROUND_APPS = {
    "qualys cloud agent",
    "loginwindow",
    "usernotificationcenter",
    "controlcenter",
}


def get_default_screenpipe_path() -> Path:
    return Path.home() / ".screenpipe" / "db.sqlite"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Personal Overtime Radar Engine")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--screenpipe-db",
        type=str,
        default=str(get_default_screenpipe_path()),
        help="Path to Screenpipe SQLite database",
    )
    parser.add_argument(
        "--output-excel",
        type=str,
        help="Path to output Excel file (defaults to Desktop)",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Disable copying TSV data to macOS clipboard",
    )
    parser.add_argument(
        "--employee-id",
        type=str,
        default="SHN000191",
        help="Employee ID for payroll claims",
    )
    parser.add_argument(
        "--force-office",
        action="store_true",
        help="Treat all audited days as in-office days",
    )
    parser.add_argument(
        "--office-days",
        type=str,
        help="Comma-separated YYYY-MM-DD dates to treat as in-office days",
    )
    parser.add_argument(
        "--repos-root",
        type=str,
        default=str(Path.home() / "repos"),
        help="Path to local repositories root for Git activity corroboration",
    )
    parser.add_argument(
        "--vault-root",
        type=str,
        default=str(Path.home() / "repos" / "SNAPPI" / "snappi-2-brain"),
        help="Path to snappi-2-brain vault for meeting and transcript context",
    )
    return parser.parse_args()


def parse_iso(dt_str: str) -> datetime.datetime:
    """Parse ISO datetime string, supporting variable fractional seconds and timezone offsets."""
    cleaned = dt_str.replace("Z", "+00:00")
    try:
        dt = datetime.datetime.fromisoformat(cleaned)
    except Exception:
        base = cleaned.split(".")[0]
        dt = datetime.datetime.strptime(base, "%Y-%m-%dT%H:%M:%S")

    # Ensure UTC timezone awareness if none is present
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def detect_office_days(
    start_date: datetime.date,
    end_date: datetime.date,
    force_office: bool = False,
    explicit_office_days: set = None,
) -> dict:
    """
    Detect in-office days using historical Wi-Fi/DHCP logs and live network interfaces.
    Returns a dict mapping datetime.date -> location description string.
    """
    office_days = {}

    if force_office:
        curr = start_date
        while curr <= end_date:
            office_days[curr] = "Office (Forced)"
            curr += datetime.timedelta(days=1)
        return office_days

    if explicit_office_days:
        for d in explicit_office_days:
            office_days[d] = "Office (Manual)"

    # 1. Historical inspection of /var/log/wifi.log and compressed archives
    gw_pattern = re.compile(
        r"([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d+\s+\d+:\d+:\d+).*Default Gateway IP Address:\s*([0-9.]+)"
    )

    current_year = datetime.date.today().year
    for log_path in sorted(glob.glob("/var/log/wifi.log*")):
        try:
            f = (
                bz2.open(log_path, "rt", errors="ignore")
                if log_path.endswith(".bz2")
                else open(log_path, "r", errors="ignore")
            )
            for line in f:
                if "Default Gateway IP Address:" in line:
                    m = gw_pattern.search(line)
                    if m:
                        dt_str, gw = m.groups()
                        if gw in KNOWN_OFFICE_GATEWAYS:
                            parts = dt_str.split()
                            try:
                                d = datetime.datetime.strptime(
                                    f"{current_year} {parts[1]} {parts[2]}", "%Y %b %d"
                                ).date()
                                if start_date <= d <= end_date:
                                    office_days[d] = KNOWN_OFFICE_GATEWAYS[gw]
                            except Exception:
                                pass
            f.close()
        except Exception:
            pass

    # 2. Live network inspection for the current date
    today = datetime.date.today()
    if start_date <= today <= end_date:
        for iface in ["en0", "en7", "en3", "en4", "en5"]:
            try:
                proc = subprocess.run(
                    ["ipconfig", "getsummary", iface],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                output = proc.stdout
                if not output:
                    continue

                for ssid, loc in KNOWN_OFFICE_SSIDS.items():
                    if f"SSID : {ssid}" in output:
                        office_days[today] = loc
                        break

                for gw, loc in KNOWN_OFFICE_GATEWAYS.items():
                    if f"Router : {gw}" in output or f"server_identifier (ip): {gw}" in output:
                        office_days[today] = loc
                        break

                if "FGT90G" in output or "FortiGate" in output:
                    if today not in office_days:
                        office_days[today] = "Corporate Office (FortiGate)"
            except Exception:
                pass

    return office_days


def round_payroll_hours(hours: float, is_office: bool = False) -> float:
    """
    Round hours to 30-minute payroll increments (.0 or .5).
    - Remote days (Option 2 Balanced Model): Apply 5.5-minute cutoff rule.
    - Office days (In-Office Zero-Cut Model): Never cut or average down hours.
      Rounds up to the nearest half-hour increment (half-hour ceiling with 1-min buffer).
    """
    whole = int(hours)
    minutes = (hours - whole) * 60.0

    if is_office:
        # Do not cut hours or average down
        if minutes <= 1.0:
            return float(whole)
        elif minutes <= 30.0:
            return float(whole) + 0.5
        else:
            return float(whole) + 1.0
    else:
        # Standard remote 5.5-minute cutoff rule
        if minutes <= 5.5:
            return float(whole)
        elif minutes <= 35.5:
            return float(whole) + 0.5
        else:
            return float(whole) + 1.0


def extract_telemetry(db_path: Path, start_dt: datetime.datetime, end_dt: datetime.datetime) -> list:
    """Extract activity intervals and corroborating titles from Screenpipe."""
    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Screenpipe stores UTC timestamps; convert local boundary datetimes to UTC ISO strings
    start_utc = start_dt.astimezone(datetime.timezone.utc)
    end_utc = end_dt.astimezone(datetime.timezone.utc)

    start_iso = start_utc.strftime("%Y-%m-%dT%H:%M:%S")
    end_iso = end_utc.strftime("%Y-%m-%dT%H:%M:%S")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}

    intervals = []
    if "activity_intervals" in tables and "activity_tasks" in tables:
        cursor.execute(
            """
            SELECT i.start_at, i.end_at, t.title, t.app_name
            FROM activity_intervals i
            JOIN activity_tasks t ON i.task_id = t.id
            WHERE i.start_at >= ? AND i.start_at <= ?
            ORDER BY i.start_at ASC
            """,
            (start_iso, end_iso),
        )
        for row in cursor.fetchall():
            app_name = row["app_name"] or ""
            if app_name.lower() in PASSIVE_BACKGROUND_APPS:
                continue
            start_local = parse_iso(row["start_at"]).astimezone()
            end_local = parse_iso(row["end_at"]).astimezone()
            duration = (end_local - start_local).total_seconds()
            intervals.append({
                "start": start_local,
                "end": end_local,
                "duration": max(0.0, duration),
                "app": app_name,
                "title": row["title"] or "",
            })
    elif "frames" in tables:
        cursor.execute(
            """
            SELECT timestamp, app_name, window_name
            FROM frames
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp ASC
            """,
            (start_iso, end_iso),
        )
        for row in cursor.fetchall():
            app_name = row["app_name"] or ""
            if app_name.lower() in PASSIVE_BACKGROUND_APPS:
                continue
            ts_local = parse_iso(row["timestamp"]).astimezone()
            intervals.append({
                "start": ts_local,
                "end": ts_local + datetime.timedelta(seconds=10),
                "duration": 10.0,
                "app": app_name,
                "title": row["window_name"] or "",
            })

    conn.close()
    return intervals


def extract_corroborating_git_activity(repos_root: Path, start_dt: datetime.datetime, end_dt: datetime.datetime) -> list:
    """Extract authored Git commits across known repos to corroborate evening sessions."""
    if not repos_root.exists():
        return []

    intervals = []
    # Inspect top repos under repos_root
    target_repos = [
        repos_root / "SNAPPI" / "snappi-2-brain",
        repos_root / "SNAPPI" / "snappi-project-radar",
        repos_root / "engineering" / "agents" / "agent-skills",
    ]

    # Also include any immediate children under repos/SNAPPI/
    snappi_dir = repos_root / "SNAPPI"
    if snappi_dir.exists():
        for p in snappi_dir.iterdir():
            if p.is_dir() and (p / ".git").exists() and p not in target_repos:
                target_repos.append(p)

    since_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
    until_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    for repo in target_repos:
        if not (repo / ".git").exists():
            continue
        try:
            cmd = [
                "git",
                "-C",
                str(repo),
                "log",
                "--all",
                f"--since={since_str}",
                f"--until={until_str}",
                "--author=Koletsos",
                "--pretty=format:%cI|%s",
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=3)
            for line in res.stdout.splitlines():
                if "|" in line:
                    iso_str, subject = line.split("|", 1)
                    try:
                        c_dt = parse_iso(iso_str).astimezone()
                        intervals.append({
                            "start": c_dt - datetime.timedelta(minutes=15),
                            "end": c_dt,
                            "duration": 15.0 * 60.0,
                            "app": "git",
                            "title": f"git: {subject}",
                        })
                    except Exception:
                        pass
        except Exception:
            pass

    return intervals


def extract_pmset_sleep_timestamps(start_date: datetime.date, end_date: datetime.date) -> dict:
    """Extract the last evening sleep timestamp for each day from pmset -g log."""
    sleep_by_date = {}
    try:
        proc = subprocess.run(
            ["pmset", "-g", "log"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
        # Match lines like: 2026-11-18 20:54:08 +0200 Sleep ... Entering Sleep state
        sleep_re = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+([+-]\d{4})\s+Sleep\s+.*Entering Sleep state", re.M)
        for m in sleep_re.finditer(proc.stdout):
            d_str, t_str, tz_str = m.groups()
            d = datetime.date.fromisoformat(d_str)
            if start_date <= d <= end_date:
                dt = datetime.datetime.strptime(f"{d_str} {t_str} {tz_str}", "%Y-%m-%d %H:%M:%S %z")
                # We want evening departure sleeps (post 16:30)
                if dt.time() >= datetime.time(16, 30):
                    if d not in sleep_by_date or dt > sleep_by_date[d]:
                        sleep_by_date[d] = dt
    except Exception:
        pass
    return sleep_by_date


def load_meeting_context(vault_root: Path) -> dict:
    """Load meeting titles and projects by date from 05_MEETINGS/ledger/."""
    ledger_dir = vault_root / "05_MEETINGS" / "ledger"
    meetings = {}
    if not ledger_dir.exists():
        return meetings

    for p in ledger_dir.glob("2026-*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
            d_m = re.search(r"^date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text, re.M)
            if d_m:
                d = datetime.date.fromisoformat(d_m.group(1))
            else:
                try:
                    d = datetime.date.fromisoformat(p.stem[:10])
                except Exception:
                    continue

            t_m = re.search(r"^title:\s*(.+)$", text, re.M)
            if t_m:
                title = t_m.group(1).strip().strip('"\'')
            else:
                title = p.stem[11:].replace("-", " ")

            p_m = re.search(r"^project:\s*(.+)$", text, re.M)
            proj = p_m.group(1).strip() if p_m else None
            if proj in ("null", "-", "none", ""):
                proj = None

            meetings.setdefault(d, []).append({
                "title": title,
                "project": proj,
            })
        except Exception:
            pass
    return meetings


def synthesize_reason(
    day_date: datetime.date,
    apps: set,
    titles: list,
    is_weekend: bool,
    is_office: bool = False,
    day_meetings: list = None,
) -> str:
    """Synthesize high-importance practitioner reason from meetings, transcripts, and engineering activity."""
    if day_meetings:
        def score_m(m_item):
            t = m_item["title"].lower()
            score = 0
            if any(k in t for k in [
                "security hardening", "security sign off", "ananke", "proof of address", "epay",
                "payments walkthrough", "payments mechanism", "installments", "settlements",
                "vouchers change request", "api deliverables", "mvp prioritization",
                "data anonymization", "subscription bundles", "payments api blocked"
            ]):
                score += 25
            elif any(k in t for k in ["walkthrough", "solution", "architecture", "infosec", "payments", "vouchers", "open points"]):
                score += 15
            elif "vodafone flex" in t or "vf flex" in t:
                score += 10
            elif "alignment" in t or "sync" in t:
                score += 5
            if "meal vouchers alignment" in t:
                score -= 8
            if any(k in t for k in ["standup", "stand up", "daily sync", "daily stand up"]):
                score -= 10
            return score

        sorted_m = sorted(day_meetings, key=score_m, reverse=True)
        best = sorted_m[0]["title"]
        clean = re.sub(r"[^a-zA-Z0-9\s-]", " ", best).strip().lower()
        clean = " ".join(clean.split())
        clean = clean.replace("vodafone flex passages of the one-to-one call on the ", "")
        clean = clean.replace("vodafone flex passages of three calls of 26 october 2026", "vodafone flex mobile architecture and strategic portfolio sync")
        clean = clean.replace("snappi x vodafone x epay ", "snappi x vodafone epay ")
        if clean:
            return clean

    # Fallback to Screenpipe & Git titles
    text_corpus = " ".join(titles).lower()
    if "recipe" in text_corpus or "kyc" in text_corpus:
        return "onboarding journey recipe and repository synchronization"
    elif "task" in text_corpus or "taskctl" in text_corpus:
        return "weekend task engine roadmap and runtime architecture design"
    elif "confluence" in text_corpus or "spec" in text_corpus:
        return "weekend architecture spec audit and confluence tech docs sync"
    elif "incident" in text_corpus or "friends" in text_corpus:
        return "weekend service delivery incident triage and pilot sync"
    elif "payment" in text_corpus:
        return "weekend payments walkthrough and settlement reconciliation design"
    elif "meal vouchers" in text_corpus or "voucher" in text_corpus:
        return "meal vouchers solution alignment and cards architecture review"
    elif is_weekend:
        return "weekend architecture review and spec reconciliation"
    elif is_office:
        return "on-site architecture alignment and delivery sync"
    else:
        return "architecture delivery and specification sync"


def synthesize_justifications(apps: set, titles: list, is_weekend: bool, is_office: bool = False) -> tuple:
    """Generate concise, project-attributed, Kranias-style lowercase justifications."""
    text_corpus = " ".join(titles).lower()

    meeting_match = None
    if "teams" in apps or "meeting" in text_corpus or "call" in text_corpus:
        for t in titles:
            t_low = t.lower()
            if any(k in t_low for k in ["sync", "alignment", "catchup", "review", "uat", "standup"]):
                clean = re.sub(r"[^a-zA-Z0-9\s]", " ", t_low)
                words = clean.split()
                if len(words) >= 2:
                    meeting_match = " ".join(words[:4])
                    break

    project = "architecture"
    if "biometric" in text_corpus or "ekyc" in text_corpus:
        project = "biometrics"
    elif "payment" in text_corpus or "sepa" in text_corpus or "iris" in text_corpus:
        project = "payments"
    elif "card" in text_corpus or "debit" in text_corpus or "visa" in text_corpus:
        project = "cards"
    elif "deposit" in text_corpus or "saving" in text_corpus:
        project = "deposits"
    elif "radar" in text_corpus:
        project = "project radar"
    elif "onboarding" in text_corpus:
        project = "onboarding"
    elif "recipe" in text_corpus or "kyc" in text_corpus:
        project = "kyc reliance"

    if meeting_match:
        choice_a = meeting_match
        choice_b = f"hld sync {project}"
    elif is_office:
        choice_a = f"office alignment {project}"
        choice_b = f"hld sync {project}"
    else:
        if is_weekend:
            choice_a = f"weekend release {project}"
            choice_b = f"architecture review {project}"
        else:
            choice_a = f"hld sync {project}"
            choice_b = f"prd review {project}"

    return choice_a.lower(), choice_b.lower()


def process_daily_overtime(
    intervals: list,
    office_days: dict,
    evening_sleeps: dict = None,
    meetings_by_date: dict = None,
) -> list:
    """
    Group intervals by day, apply contract boundaries, office detection, and calculate net hours.
    - Office Days: Zero-cut policy (no idle gap deduction, continuous span from cutoff, half-hour ceiling).
    - Remote Days: Option 2 Balanced Model (gap clustering <=150m, idle deduction >45m, 5.5-minute cutoff rule).
    """
    days = {}
    for item in intervals:
        day_key = item["start"].date()
        days.setdefault(day_key, []).append(item)

    # Ensure days with evening sleeps or office presence are not omitted even if Screenpipe had 0 entries
    if evening_sleeps:
        for s_date, s_dt in evening_sleeps.items():
            if s_date not in days and s_date in office_days:
                days[s_date] = [{
                    "start": s_dt - datetime.timedelta(hours=3),
                    "end": s_dt,
                    "duration": 3.0 * 3600.0,
                    "app": "office_presence",
                    "title": "office presence session",
                }]

    results = []

    for day_date, day_items in sorted(days.items()):
        weekday = day_date.weekday()  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
        is_weekend = weekday in (5, 6)
        is_office = day_date in office_days
        location_desc = office_days.get(day_date, "Remote")

        # Determine contract cutoff in local time
        if is_weekend:
            cutoff_time = datetime.time(0, 0, 0)
        elif weekday == 4:  # Friday
            cutoff_time = datetime.time(16, 30, 0)
        else:  # Monday to Thursday
            cutoff_time = datetime.time(17, 0, 0)

        # Filter items strictly occurring after cutoff
        after_hours = []
        for it in day_items:
            it_start_time = it["start"].time()
            if is_weekend or it_start_time >= cutoff_time or it["end"].time() > cutoff_time:
                after_hours.append(it)

        if not after_hours:
            continue

        after_hours.sort(key=lambda x: x["start"])

        # Determine start time (clamped to contract cutoff)
        tz = after_hours[0]["start"].tzinfo
        cutoff_dt = datetime.datetime.combine(day_date, cutoff_time, tzinfo=tz)

        if is_office:
            # On office days, regular contract hours end at cutoff_time; overtime starts immediately at cutoff
            first_session_start = cutoff_dt
        else:
            first_session_start = max(after_hours[0]["start"], cutoff_dt)

        last_session_end = after_hours[-1]["end"]

        # If pmset recorded an evening departure sleep later than last activity on office day, use it
        if is_office and evening_sleeps and day_date in evening_sleeps:
            if evening_sleeps[day_date] > last_session_end:
                last_session_end = evening_sleeps[day_date]

        apps_seen = set()
        titles_seen = []
        for it in after_hours:
            if it["app"]:
                apps_seen.add(it["app"].lower())
            if it["title"]:
                titles_seen.append(it["title"])

        if is_office:
            # IN-OFFICE ZERO-CUT POLICY:
            # Do NOT cut hours for internal gaps or breaks. Presence at office counts continuously.
            total_active_seconds = max(0.0, (last_session_end - cutoff_dt).total_seconds())
            raw_hours = total_active_seconds / 3600.0

            # Discard sessions < 20 minutes
            if raw_hours < 0.33:
                continue

            # In-Office rounding: Never cut or average down hours (half-hour ceiling)
            payroll_hours = round_payroll_hours(raw_hours, is_office=True)
            location_tag = f"🏢 Office ({location_desc})"
        else:
            # REMOTE DAYS: Option 2 Balanced Model
            # Cluster sessions separated by <= 150 minutes
            clusters = []
            current_cluster = [after_hours[0]]

            for it in after_hours[1:]:
                prev_end = current_cluster[-1]["end"]
                gap_seconds = (it["start"] - prev_end).total_seconds()
                if gap_seconds <= 150 * 60:
                    current_cluster.append(it)
                else:
                    clusters.append(current_cluster)
                    current_cluster = [it]
            clusters.append(current_cluster)

            total_active_seconds = 0.0
            for cluster in clusters:
                cluster_start = cluster[0]["start"]
                cluster_end = cluster[-1]["end"]
                cluster_duration = (cluster_end - cluster_start).total_seconds()

                # Deduct internal idle gaps > 45 min within cluster
                internal_idle = 0.0
                for i in range(len(cluster) - 1):
                    inter_gap = (cluster[i + 1]["start"] - cluster[i]["end"]).total_seconds()
                    if inter_gap > 45 * 60:
                        internal_idle += inter_gap

                effective_cluster_seconds = max(0.0, cluster_duration - internal_idle)
                total_active_seconds += effective_cluster_seconds

            raw_hours = total_active_seconds / 3600.0

            # Discard sessions < 20 minutes (0.33h)
            if raw_hours < 0.33:
                continue

            # Weekend threshold: discard days with < 1.0h active work
            if is_weekend and raw_hours < 1.0:
                continue

            # Apply 30-minute payroll increment rounding (5.5-minute cutoff rule)
            payroll_hours = round_payroll_hours(raw_hours, is_office=False)
            location_tag = "🏠 Remote"

        day_m = meetings_by_date.get(day_date, []) if meetings_by_date else None
        reason = synthesize_reason(day_date, apps_seen, titles_seen, is_weekend, is_office, day_m)
        choice_a, choice_b = synthesize_justifications(apps_seen, titles_seen, is_weekend, is_office)

        results.append({
            "date": day_date,
            "day_name": day_date.strftime("%a"),
            "location": location_tag,
            "is_office": is_office,
            "start_time": first_session_start.strftime("%H:%M"),
            "end_time": last_session_end.strftime("%H:%M"),
            "raw_hours": raw_hours,
            "payroll_hours": payroll_hours,
            "reason": reason,
            "choice_a": choice_a,
            "choice_b": choice_b,
        })

    return results


def export_workbook(results: list, output_path: Path, employee_id: str = "SHN000191"):
    """Write results to professionally styled Excel workbook (.xlsx) matching exact Date, Day, Overtime, Reason columns."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = openpyxl.Workbook()

    # Sheet 1: Exact requested deliverable columns (Date, Day, Overtime, Reason)
    ws_main = wb.active
    ws_main.title = "Overtime"
    ws_main.views.sheetView[0].showGridLines = True

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")

    thin_border = Border(
        left=Side(style="thin", color="D1D5DB"),
        right=Side(style="thin", color="D1D5DB"),
        top=Side(style="thin", color="D1D5DB"),
        bottom=Side(style="thin", color="D1D5DB"),
    )

    headers = ["Date", "Day", "Overtime", "Reason"]
    ws_main.append(headers)
    for col_idx in range(1, len(headers) + 1):
        cell = ws_main.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    for r_idx, row in enumerate(results, start=2):
        ws_main.append([
            row["date"].strftime("%d/%m/%Y"),
            row["day_name"],
            row["payroll_hours"],
            row["reason"],
        ])
        for col_idx in range(1, len(headers) + 1):
            c = ws_main.cell(row=r_idx, column=col_idx)
            c.border = thin_border
            if col_idx in (1, 2):
                c.alignment = center_align
            elif col_idx == 3:
                c.alignment = right_align
                c.number_format = "0.0"
            else:
                c.alignment = left_align

    # Total Row
    last_row = len(results) + 2
    ws_main.cell(row=last_row, column=1, value="Total")
    total_cell = ws_main.cell(row=last_row, column=3, value=f"=SUM(C2:C{last_row - 1})")
    total_cell.number_format = "0.0"
    total_font = Font(name="Calibri", size=11, bold=True)
    ws_main.cell(row=last_row, column=1).font = total_font
    total_cell.font = total_font

    # Sheet 2: Audit Breakdown (Auditability with Location, Spans, Raw Hours)
    ws_audit = wb.create_sheet(title="Audit Breakdown")
    ws_audit.views.sheetView[0].showGridLines = True
    audit_headers = ["Date", "Day", "Location", "Active Span", "Raw Hours", "Payroll Hours", "Reason"]
    ws_audit.append(audit_headers)
    for col_idx in range(1, len(audit_headers) + 1):
        cell = ws_audit.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = PatternFill(start_color="374151", end_color="374151", fill_type="solid")
        cell.alignment = center_align

    for r_idx, row in enumerate(results, start=2):
        ws_audit.append([
            row["date"].strftime("%d/%m/%Y"),
            row["day_name"],
            row["location"],
            f"{row['start_time']} - {row['end_time']}",
            round(row["raw_hours"], 2),
            row["payroll_hours"],
            row["reason"],
        ])
        for col_idx in range(1, len(audit_headers) + 1):
            c = ws_audit.cell(row=r_idx, column=col_idx)
            c.border = thin_border
            if col_idx in (1, 2, 4):
                c.alignment = center_align
            elif col_idx in (5, 6):
                c.alignment = right_align
                c.number_format = "0.0"
            else:
                c.alignment = left_align

    # Auto-fit column widths on both sheets
    for ws in [ws_main, ws_audit]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    output_path = output_path.with_suffix(".xlsx")
    wb.save(str(output_path))
    print(f"Excel workbook generated: {output_path}")


def stage_to_clipboard(results: list):
    """Stage tab-separated rows directly into macOS pbcopy."""
    tsv_lines = []
    for r in results:
        date_str = r["date"].strftime("%d/%m/%Y")
        day_str = r["day_name"]
        hours_str = f"{r['payroll_hours']:.1f}"
        reason = r["reason"]
        tsv_lines.append(f"{date_str}\t{day_str}\t{hours_str}\t{reason}")

    tsv_data = "\n".join(tsv_lines)

    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        proc.communicate(input=tsv_data.encode("utf-8"))
        print(f"Staged {len(results)} rows into macOS clipboard (pbcopy). Ready for paste.")
    except Exception as e:
        print(f"Warning: Could not copy to pbcopy: {e}", file=sys.stderr)


def main():
    args = parse_arguments()

    today = datetime.date.today()
    if args.start_date:
        start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
    else:
        start_date = today.replace(day=1)

    if args.end_date:
        end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
    else:
        end_date = today

    explicit_office_dates = set()
    if args.office_days:
        for s in args.office_days.split(","):
            s = s.strip()
            if s:
                explicit_office_dates.add(datetime.datetime.strptime(s, "%Y-%m-%d").date())

    # Detect office presence across date range
    office_days = detect_office_days(
        start_date=start_date,
        end_date=end_date,
        force_office=args.force_office,
        explicit_office_days=explicit_office_dates,
    )

    tz = datetime.datetime.now().astimezone().tzinfo
    start_dt = datetime.datetime.combine(start_date, datetime.time.min, tzinfo=tz)
    end_dt = datetime.datetime.combine(end_date, datetime.time.max, tzinfo=tz)

    db_path = Path(args.screenpipe_db).expanduser()
    intervals = extract_telemetry(db_path, start_dt, end_dt)

    # Corroborate with local git activity
    repos_root = Path(args.repos_root).expanduser()
    git_intervals = extract_corroborating_git_activity(repos_root, start_dt, end_dt)
    intervals.extend(git_intervals)

    # Extract evening departure sleep timestamps from pmset
    evening_sleeps = extract_pmset_sleep_timestamps(start_date, end_date)

    # Load meeting context from vault
    vault_root = Path(args.vault_root).expanduser()
    meetings_by_date = load_meeting_context(vault_root)

    if not intervals and not evening_sleeps:
        print(f"No activity intervals or telemetry found between {start_date} and {end_date}.")
        return

    results = process_daily_overtime(intervals, office_days, evening_sleeps, meetings_by_date)

    if not results:
        print(f"No qualifying overtime sessions found between {start_date} and {end_date}.")
        return

    total_hours = sum(r["payroll_hours"] for r in results)
    office_count = sum(1 for r in results if r["is_office"])
    remote_count = len(results) - office_count

    print("\n### ⏱️ Overtime Audit Summary")
    print(f"- **Audited Span**: {start_date} to {end_date}")
    print(f"- **Active Overtime Days**: {len(results)} ({office_count} Office, {remote_count} Remote)")
    print(f"- **Total Overtime Hours**: {total_hours:.1f}h\n")

    print("| Date | Day | Overtime | Reason |")
    print("| :--- | :--- | :--- | :--- |")
    for r in results:
        d_str = r["date"].strftime("%d/%m/%Y")
        print(f"| {d_str} | {r['day_name']} | {r['payroll_hours']:.1f}h | {r['reason']} |")

    desktop_dir = Path.home() / "Desktop"
    month_name = start_date.strftime("%B")
    year_str = start_date.strftime("%Y")
    excel_path = Path(args.output_excel).expanduser() if args.output_excel else desktop_dir / f"SNAPPI_{month_name}_{year_str}_Overtime.xlsx"

    export_workbook(results, excel_path, employee_id=args.employee_id)

    if not args.no_clipboard:
        stage_to_clipboard(results)


if __name__ == "__main__":
    main()
