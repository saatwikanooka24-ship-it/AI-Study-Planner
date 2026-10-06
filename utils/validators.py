from __future__ import annotations

from datetime import date
from typing import Any

from utils.helpers import parse_date


def validate_profile_data(data: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(data)
    if not cleaned.get("name"):
        raise ValueError("Student name cannot be empty.")
    if not cleaned.get("email"):
        raise ValueError("Email cannot be empty.")
    hours = int(cleaned.get("study_hours_per_day", 0) or 0)
    if hours <= 0:
        raise ValueError("Study hours must be positive.")
    cleaned["study_hours_per_day"] = hours
    return cleaned


def validate_subject_data(data: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(data)
    if not cleaned.get("subject_name"):
        raise ValueError("Subject name cannot be empty.")

    prep = int(cleaned.get("current_preparation", 0) or 0)
    target = int(cleaned.get("target_percentage", 0) or 0)
    if not 0 <= prep <= 100:
        raise ValueError("Preparation percentage must be between 0 and 100.")
    if not 0 <= target <= 100:
        raise ValueError("Target percentage must be between 0 and 100.")
    cleaned["current_preparation"] = prep
    cleaned["target_percentage"] = target

    exam_date = parse_date(cleaned.get("exam_date"))
    if cleaned.get("exam_date") and exam_date is None:
        raise ValueError("Exam date is invalid. Use YYYY-MM-DD.")
    cleaned["exam_date"] = exam_date
    return cleaned


def validate_task_data(data: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(data)
    if not cleaned.get("task_name"):
        raise ValueError("Task name cannot be empty.")
    due_date = parse_date(cleaned.get("due_date"))
    if cleaned.get("due_date") and due_date is None:
        raise ValueError("Task deadline must be a valid date.")
    cleaned["due_date"] = due_date
    return cleaned


def validate_assignment_data(data: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(data)
    if not cleaned.get("assignment_name"):
        raise ValueError("Assignment name cannot be empty.")
    deadline = parse_date(cleaned.get("deadline"))
    if cleaned.get("deadline") and deadline is None:
        raise ValueError("Assignment deadline must be a valid date.")
    cleaned["deadline"] = deadline
    return cleaned
