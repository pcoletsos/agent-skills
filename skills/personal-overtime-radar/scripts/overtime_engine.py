#!/usr/bin/env python3
"""
Personal Overtime Radar Engine
Performs forensic telemetry extraction, session clustering, payroll increment rounding,
Excel generation, and macOS clipboard staging for after-hours engineering overtime.
"""

import argparse
import datetime
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path


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


def round_payroll_hours(hours: float) -> float:
    """
    Round to nearest 30-minute payroll increment (.0 or .5).
    Rounds up to next half-hour only if trailing active minutes exceed
    the half-hour mark by more than 5.5 minutes.
    """
    whole = int(hours)
    minutes = (hours - whole) * 60.0

    if minutes <= 5.5:
        return float(whole)
    elif minutes <= 35.5:
        return float(whole) + 0.5
    else:
        return float(whole) + 1.0


def extract_telemetry(db_path: Path, start_dt: datetime.datetime, end_dt: datetime.datetime) -> list:
    """Extract activity intervals and corroborating titles from Screenpipe."""
    if not db_path.exists():
        print(f"Warning: Screenpipe database not found at {db_path}", file=sys.stderr)
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
            start_local = parse_iso(row["start_at"]).astimezone()
            end_local = parse_iso(row["end_at"]).astimezone()
            duration = (end_local - start_local).total_seconds()
            intervals.append({
                "start": start_local,
                "end": end_local,
                "duration": max(0.0, duration),
                "app": row["app_name"] or "",
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
            ts_local = parse_iso(row["timestamp"]).astimezone()
            intervals.append({
                "start": ts_local,
                "end": ts_local + datetime.timedelta(seconds=10),
                "duration": 10.0,
                "app": row["app_name"] or "",
                "title": row["window_name"] or "",
            })

    conn.close()
    return intervals


def process_daily_overtime(intervals: list) -> list:
    """Group intervals by day, apply contract boundaries, cluster gaps, and calculate net hours."""
    days = {}
    for item in intervals:
        day_key = item["start"].date()
        days.setdefault(day_key, []).append(item)

    results = []

    for day_date, day_items in sorted(days.items()):
        weekday = day_date.weekday()  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
        is_weekend = weekday in (5, 6)

        # Determine contract cutoff in local time
        if is_weekend:
            cutoff = datetime.time(0, 0, 0)
        elif weekday == 4:  # Friday
            cutoff = datetime.time(16, 30, 0)
        else:  # Monday to Thursday
            cutoff = datetime.time(17, 0, 0)

        # Filter items strictly occurring after cutoff
        after_hours = []
        for it in day_items:
            it_start_time = it["start"].time()
            if is_weekend or it_start_time >= cutoff:
                after_hours.append(it)

        if not after_hours:
            continue

        after_hours.sort(key=lambda x: x["start"])

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
        apps_seen = set()
        titles_seen = []

        first_session_start = clusters[0][0]["start"]
        last_session_end = clusters[-1][-1]["end"]

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

            for it in cluster:
                if it["app"]:
                    apps_seen.add(it["app"].lower())
                if it["title"]:
                    titles_seen.append(it["title"])

        raw_hours = total_active_seconds / 3600.0

        # Discard sessions < 20 minutes (0.33h)
        if raw_hours < 0.33:
            continue

        # Weekend threshold: discard days with < 1.0h active work
        if is_weekend and raw_hours < 1.0:
            continue

        # Apply 30-minute payroll increment rounding
        payroll_hours = round_payroll_hours(raw_hours)

        choice_a, choice_b = synthesize_justifications(apps_seen, titles_seen, is_weekend)

        results.append({
            "date": day_date,
            "day_name": day_date.strftime("%a"),
            "start_time": first_session_start.strftime("%H:%M"),
            "end_time": last_session_end.strftime("%H:%M"),
            "raw_hours": raw_hours,
            "payroll_hours": payroll_hours,
            "choice_a": choice_a,
            "choice_b": choice_b,
        })

    return results


def synthesize_justifications(apps: set, titles: list, is_weekend: bool) -> tuple:
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

    if meeting_match:
        choice_a = meeting_match
        choice_b = f"hld sync {project}"
    else:
        if is_weekend:
            choice_a = f"weekend release {project}"
            choice_b = f"architecture review {project}"
        else:
            choice_a = f"hld sync {project}"
            choice_b = f"prd review {project}"

    return choice_a.lower(), choice_b.lower()


def export_workbook(results: list, output_path: Path):
    """Write results to Excel (.xlsx) using openpyxl if available, or TSV fallback."""
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Overtime"

        headers = ["Date", "Day", "Span", "Raw Hours", "Payroll Hours", "Choice A", "Choice B"]
        ws.append(headers)

        for row in results:
            ws.append([
                row["date"].strftime("%d/%m/%Y"),
                row["day_name"],
                f"{row['start_time']} - {row['end_time']}",
                round(row["raw_hours"], 2),
                row["payroll_hours"],
                row["choice_a"],
                row["choice_b"],
            ])

        wb.save(str(output_path))
        print(f"Excel workbook generated: {output_path}")
    except ImportError:
        tsv_path = output_path.with_suffix(".tsv")
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.write("Date\tDay\tSpan\tRaw Hours\tPayroll Hours\tChoice A\tChoice B\n")
            for row in results:
                f.write(
                    f"{row['date'].strftime('%d/%m/%Y')}\t{row['day_name']}\t"
                    f"{row['start_time']} - {row['end_time']}\t"
                    f"{round(row['raw_hours'], 2)}\t{row['payroll_hours']}\t"
                    f"{row['choice_a']}\t{row['choice_b']}\n"
                )
        print(f"openpyxl not installed. Saved TSV fallback: {tsv_path}")


def stage_to_clipboard(results: list):
    """Stage tab-separated rows directly into macOS pbcopy."""
    tsv_lines = []
    for r in results:
        date_str = r["date"].strftime("%d/%m/%Y")
        hours_str = f"{r['payroll_hours']:.1f}"
        justification = r["choice_a"]
        tsv_lines.append(f"{date_str}\t{hours_str}\t{justification}")

    tsv_data = "\n".join(tsv_lines)

    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        proc.communicate(input=tsv_data.encode("utf-8"))
        print(f"Staged {len(results)} rows into macOS clipboard (pbcopy). Ready for Cmd+V in SharePoint.")
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

    # Combine with local time bounds, then extract_telemetry converts to UTC
    tz = datetime.datetime.now().astimezone().tzinfo
    start_dt = datetime.datetime.combine(start_date, datetime.time.min, tzinfo=tz)
    end_dt = datetime.datetime.combine(end_date, datetime.time.max, tzinfo=tz)

    db_path = Path(args.screenpipe_db).expanduser()
    intervals = extract_telemetry(db_path, start_dt, end_dt)

    if not intervals:
        print(f"No activity intervals found between {start_date} and {end_date}.")
        return

    results = process_daily_overtime(intervals)

    if not results:
        print(f"No qualifying overtime sessions found between {start_date} and {end_date}.")
        return

    total_hours = sum(r["payroll_hours"] for r in results)

    print("\n### ⏱️ Overtime Audit Summary")
    print(f"- **Audited Span**: {start_date} to {end_date}")
    print(f"- **Active Overtime Days**: {len(results)}")
    print(f"- **Total Overtime Hours**: {total_hours:.1f}h\n")

    print("| Date | Day | Span | Hours | Choice A (Priority) | Choice B (Alternative) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in results:
        d_str = r["date"].strftime("%d/%m/%Y")
        span = f"{r['start_time']} - {r['end_time']}"
        print(f"| {d_str} | {r['day_name']} | {span} | {r['payroll_hours']:.1f}h | {r['choice_a']} | {r['choice_b']} |")

    desktop_dir = Path.home() / "Desktop"
    month_name = start_date.strftime("%B")
    year_str = start_date.strftime("%Y")
    excel_path = Path(args.output_excel).expanduser() if args.output_excel else desktop_dir / f"SNAPPI_{month_name}_{year_str}_Overtime.xlsx"

    export_workbook(results, excel_path)

    if not args.no_clipboard:
        stage_to_clipboard(results)


if __name__ == "__main__":
    main()
