from __future__ import annotations

from typing import Any


def build_question_prompt(student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any], question: str) -> str:
    """Create a local study guidance response from the student's profile and current tasks."""
    subject_names = ", ".join(subject.subject_name for subject in subjects[:5]) if subjects else "No subjects added yet"
    pending_tasks = len([task for task in tasks if task.status != "Completed"])
    upcoming_exam = next((subject.subject_name for subject in subjects if subject.exam_date), "No exam scheduled")

    return (
        f"Based on your profile as a {student.branch} student in semester {student.semester}, "
        f"you should focus on {subject_names}. You currently have {pending_tasks} pending tasks and an upcoming exam in {upcoming_exam}. "
        f"Keep your most difficult subject in the first study block of the day and make sure you complete your nearest deadline before secondary work.\n\n"
        f"Student question: {question}"
    )
