from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from utils.helpers import calculate_priority_score, parse_date


def build_weekly_timetable(
    subjects: list[Any],
    start_date: date | str,
    daily_hours: int,
    preferred_time: str,
    break_duration: int = 10,
) -> list[dict[str, Any]]:
    """Create a simple weekly timetable for the planning window."""
    start = parse_date(start_date)
    if not start:
        raise ValueError("Start date is required to build the timetable.")

    ranked_subjects = sorted(subjects, key=lambda s: calculate_priority_score(s, start), reverse=True)
    entries: list[dict[str, Any]] = []

    for day_offset in range(7):
        current_day = start + timedelta(days=day_offset)
        time_slots = [preferred_time, "Afternoon", "Evening"]
        for index, subject in enumerate(ranked_subjects[: min(len(ranked_subjects), 3)]):
            entries.append(
                {
                    "Day": current_day.strftime("%A"),
                    "Date": current_day.isoformat(),
                    "Time": time_slots[index % len(time_slots)],
                    "Subject": subject.subject_name,
                    "Topic": subject.subject_name,
                    "Duration": max(45, int(daily_hours * 60 / max(1, min(len(ranked_subjects), 3)))),
                }
            )
        if break_duration:
            entries.append({
                "Day": current_day.strftime("%A"),
                "Date": current_day.isoformat(),
                "Time": "Break",
                "Subject": "Break",
                "Topic": "Short break",
                "Duration": break_duration,
            })

    return entries
