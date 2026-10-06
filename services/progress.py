from __future__ import annotations

from datetime import date
from typing import Any

from utils.helpers import days_until, parse_date


def calculate_completion_percentage(items: list[Any], status_key: str = "status") -> float:
    if not items:
        return 0.0
    completed = sum(1 for item in items if getattr(item, status_key, "") == "Completed")
    return round((completed / len(items)) * 100, 2)


def compute_dashboard_metrics(student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any]) -> dict[str, Any]:
    completed_tasks = sum(1 for task in tasks if task.status == "Completed")
    pending_tasks = sum(1 for task in tasks if task.status != "Completed")
    upcoming_exams = [subject for subject in subjects if getattr(subject, "exam_date", None) is not None]
    upcoming_assignments = [assignment for assignment in assignments if assignment.status != "Completed"]
    overall_progress = 0.0 if not subjects else round(sum(subject.current_preparation for subject in subjects) / len(subjects), 2)
    study_hours_today = sum(session.duration_minutes for session in sessions if session.session_date == date.today())
    streak = 0
    unique_days = sorted({session.session_date for session in sessions})
    if unique_days:
        streak = len(unique_days)

    return {
        "student_name": student.name if student else "Student",
        "branch": student.branch if student else "N/A",
        "year": student.year if student else "N/A",
        "semester": student.semester if student else "N/A",
        "study_hours_today": study_hours_today,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "upcoming_exams": len(upcoming_exams),
        "upcoming_assignments": len(upcoming_assignments),
        "overall_progress": overall_progress,
        "study_streak": streak,
    }


def calculate_study_score(student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any]) -> tuple[int, str]:
    task_total = max(1, len(tasks))
    task_completion = (sum(1 for task in tasks if task.status == "Completed") / task_total) * 100
    total_minutes = sum(session.duration_minutes for session in sessions)
    hours_score = min(100, (total_minutes / max(1, student.study_hours_per_day * 60 * 7)) * 100)

    subject_average = 0.0 if not subjects else sum(subject.current_preparation for subject in subjects) / len(subjects)
    consistency = 0.0
    if sessions:
        unique_days = len({session.session_date for session in sessions})
        consistency = min(100, (unique_days / 7) * 100)

    exam_pressure = 0.0
    exam_subjects = [subject for subject in subjects if getattr(subject, "exam_date", None)]
    if exam_subjects:
        nearest = min(exam_subjects, key=lambda subject: days_until(subject.exam_date) if getattr(subject, "exam_date", None) else 999)
        days_left = days_until(nearest.exam_date)
        exam_pressure = max(0.0, 100 - (days_left * 4))

    score = round(
        (task_completion * 0.35)
        + (hours_score * 0.20)
        + (subject_average * 0.25)
        + (consistency * 0.10)
        + (exam_pressure * 0.10)
    )
    score = max(0, min(100, score))

    if score >= 85:
        explanation = "You are consistent and on track. Keep your momentum and protect your revision time."
    elif score >= 70:
        explanation = "Your progress is solid. Focus on the hardest subjects and complete deadline-driven tasks first."
    elif score >= 50:
        explanation = "You are building momentum. Add more focused sessions and reduce procrastination."
    else:
        explanation = "Your study rhythm needs a reset. Start with the highest-priority subjects and keep sessions shorter but consistent."

    return score, explanation


def get_weekly_progress(tasks: list[Any]) -> list[dict[str, Any]]:
    weekly = []
    for day in range(7):
        day_label = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day]
        completed = sum(1 for task in tasks if task.status == "Completed")
        weekly.append({"day": day_label, "completed": completed, "pending": max(0, len(tasks) - completed)})
    return weekly
