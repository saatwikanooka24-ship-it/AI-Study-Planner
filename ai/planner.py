from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from utils.helpers import calculate_priority_score, parse_date


def _topic_for_subject(subject_name: str) -> str:
    topics = {
        "Digital Electronics": "Sequential Circuits",
        "Signals and Systems": "Fourier Series",
        "Network Theory": "Thevenin Equivalent",
        "Engineering Mathematics": "Differential Equations",
        "Python Programming": "Problem Solving",
    }
    return topics.get(subject_name, "Core Concepts")


def generate_study_plan(
    student: Any,
    subjects: list[Any],
    start_date: date | str,
    end_date: date | str,
    daily_hours: int,
    preferred_time: str,
    break_duration: int = 10,
    revision_mode: bool = False,
    exam_mode: bool = False,
) -> list[dict[str, Any]]:
    """Generate a prioritized daily study schedule for the planning period."""
    start = parse_date(start_date)
    end = parse_date(end_date) or start
    if not start or not end:
        raise ValueError("Both start and end dates are required.")

    if not subjects:
        return [{"date": start.isoformat(), "sessions": [{"time": preferred_time, "subject": "General", "topic": "Foundation Review", "duration": max(60, int(daily_hours * 60)), "type": "Study"}]}]

    ranked_subjects = sorted(subjects, key=lambda s: calculate_priority_score(s, start), reverse=True)
    plan: list[dict[str, Any]] = []
    total_days = (end - start).days + 1
    study_minutes = max(30, int(daily_hours * 60))
    break_minutes = max(5, int(break_duration))

    for offset in range(total_days):
        current_day = start + timedelta(days=offset)
        sessions: list[dict[str, Any]] = []
        remaining_minutes = study_minutes
        subject_cycle = ranked_subjects

        for index, subject in enumerate(subject_cycle):
            if remaining_minutes <= 0:
                break
            duration = min(90, max(50, int((remaining_minutes / max(1, len(subject_cycle) - index)))))
            if exam_mode and subject.exam_date:
                days_left = (subject.exam_date - current_day).days
                if days_left <= 14:
                    duration = min(120, max(duration, 90))
            if revision_mode and subject.current_preparation < 70:
                duration = min(110, max(duration, 70))
            duration = min(duration, remaining_minutes)
            if duration <= 0:
                continue

            session_time = preferred_time if index % 2 == 0 else "Evening"
            sessions.append(
                {
                    "day": current_day.strftime("%A"),
                    "date": current_day.isoformat(),
                    "time": session_time,
                    "subject": subject.subject_name,
                    "topic": _topic_for_subject(subject.subject_name),
                    "duration": duration,
                    "type": "Study",
                }
            )
            remaining_minutes -= duration

            if remaining_minutes >= break_minutes and index < len(subject_cycle) - 1:
                sessions.append(
                    {
                        "day": current_day.strftime("%A"),
                        "date": current_day.isoformat(),
                        "time": "Break",
                        "subject": "Break",
                        "topic": "Short Break",
                        "duration": break_minutes,
                        "type": "Break",
                    }
                )
                remaining_minutes -= break_minutes

        if not sessions:
            sessions.append(
                {
                    "day": current_day.strftime("%A"),
                    "date": current_day.isoformat(),
                    "time": preferred_time,
                    "subject": "General",
                    "topic": "Light revision",
                    "duration": min(study_minutes, 60),
                    "type": "Revision",
                }
            )

        plan.append({"date": current_day.isoformat(), "day": current_day.strftime("%A"), "sessions": sessions})

    return plan


def calculate_priority_score(subject: Any, today: date | str | None = None) -> float:
    """Score a subject based on difficulty, urgency, preparation gap, target gap and credits."""
    today_value = parse_date(today) if today else date.today()
    difficulty_score = {"Easy": 1, "Medium": 2, "Hard": 3}.get(subject.difficulty, 2)
    exam_gap = 0
    if getattr(subject, "exam_date", None):
        exam_date = parse_date(subject.exam_date)
        if exam_date:
            exam_gap = max(0, 30 - max(0, (exam_date - today_value).days))
    preparation_gap = max(0, subject.target_percentage - subject.current_preparation)
    target_gap = max(0, subject.target_percentage - subject.current_preparation)
    credit_score = int(getattr(subject, "credits", 3))
    score = (difficulty_score * 20) + (exam_gap * 0.7) + (preparation_gap * 0.8) + (target_gap * 0.5) + (credit_score * 5)
    return float(score)
