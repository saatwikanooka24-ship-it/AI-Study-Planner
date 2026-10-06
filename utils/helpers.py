from __future__ import annotations

from datetime import date, datetime
from typing import Any


def parse_date(value: date | str | datetime | None) -> date | None:
    """Convert common date input types into a Python date object."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def format_date(value: date | str | datetime | None, fmt: str = "%d %b") -> str:
    parsed = parse_date(value)
    if parsed is None:
        return "Not set"
    return parsed.strftime(fmt)


def days_until(target: date | str | datetime | None) -> int:
    parsed = parse_date(target)
    if parsed is None:
        return 9999
    return (parsed - date.today()).days


def calculate_priority_score(subject: Any, today: date | str | None = None) -> float:
    """Score a subject based on urgency, difficulty, and preparation gap."""
    today_value = parse_date(today) if today else date.today()
    if not hasattr(subject, "difficulty"):
        return 0.0

    difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    difficulty_score = difficulty_map.get(subject.difficulty, 2)
    exam_score = 0
    exam_date = getattr(subject, "exam_date", None)
    if exam_date:
        parsed_exam = parse_date(exam_date)
        if parsed_exam:
            exam_score = max(0, 30 - max(0, (parsed_exam - today_value).days))

    prep_gap = max(0, int(getattr(subject, "target_percentage", 0)) - int(getattr(subject, "current_preparation", 0)))
    credit_score = int(getattr(subject, "credits", 3))
    score = (difficulty_score * 20) + (exam_score * 0.7) + (prep_gap * 0.8) + (credit_score * 6)
    return float(round(score, 2))
