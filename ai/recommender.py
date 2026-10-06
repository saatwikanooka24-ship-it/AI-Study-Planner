from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from ai.prompts import build_question_prompt
from utils.helpers import days_until

load_dotenv()


def get_ai_mode() -> str:
    """Return whether the system is in local fallback mode or API-configured mode."""
    if os.getenv("AI_API_KEY"):
        return "AI mode: API-enabled"
    return "AI mode: Local recommendation engine"


class AIRecommendationEngine:
    def __init__(self) -> None:
        self.api_key = os.getenv("AI_API_KEY")

    def generate_recommendations(self, student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any]) -> list[str]:
        """Return personalized recommendations using local rules when no API key is configured."""
        return self._local_recommendations(student, subjects, tasks, assignments, sessions)

    def _local_recommendations(self, student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any]) -> list[str]:
        recommendations: list[str] = []
        if not subjects:
            return ["Add your subjects to unlock personalized planning suggestions."]

        urgent_exam = min((s for s in subjects if getattr(s, "exam_date", None)), key=lambda s: days_until(s.exam_date), default=None)
        if urgent_exam:
            days_left = days_until(urgent_exam.exam_date)
            if days_left <= 15:
                recommendations.append(
                    f"Your {urgent_exam.subject_name} exam is approaching and your current preparation is only {urgent_exam.current_preparation}%. Consider giving it additional study time this week."
                )

        urgent_task = next((task for task in sorted(tasks, key=lambda item: str(item.due_date or "9999-12-31")) if task.status != "Completed"), None)
        if urgent_task:
            recommendations.append(
                f"Your {urgent_task.task_name} task is due soon. Complete it before starting lower-priority work."
            )

        overdue_assignments = [item for item in assignments if item.status != "Completed" and item.deadline and days_until(item.deadline) < 0]
        if overdue_assignments:
            recommendations.append("You have overdue assignments. Prioritize those before extra revision tasks.")

        weak_subject = max(subjects, key=lambda s: (s.target_percentage - s.current_preparation, {"Hard": 3, "Medium": 2, "Easy": 1}.get(s.difficulty, 2)), default=None)
        if weak_subject:
            recommendations.append(
                f"{weak_subject.subject_name} is your weakest subject right now. Use active recall and short timed practice blocks to improve it steadily."
            )

        if not tasks or len([t for t in tasks if t.status == "Completed"]) < 2:
            recommendations.append("Start with your hardest subject early in the day when your concentration is highest.")

        return recommendations[:5]


def generate_recommendations(student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any]) -> list[str]:
    engine = AIRecommendationEngine()
    return engine.generate_recommendations(student, subjects, tasks, assignments, sessions)


def answer_student_question(question: str, student: Any, subjects: list[Any], tasks: list[Any], assignments: list[Any], sessions: list[Any]) -> str:
    """Return a helpful local answer for common B.Tech student study questions."""
    normalized = question.lower()
    if "which subject should i study today" in normalized or "study today" in normalized:
        if not subjects:
            return "Add subjects first to create a personalized study priority list."
        top_subject = max(subjects, key=lambda s: (s.target_percentage - s.current_preparation, {"Hard": 3, "Medium": 2, "Easy": 1}.get(s.difficulty, 2)))
        return f"Study {top_subject.subject_name} first today. It has the biggest gap between your preparation and target, and it is a high-priority subject."

    if "weak" in normalized and "digital" in normalized:
        return "Use a 3-step plan: revise core concepts, solve 10 short MCQs or numerical questions, and then revisit the toughest topic with active recall."

    if "revision strategy" in normalized or "revision" in normalized:
        return "Follow a 30-20-10 cycle: revise the topic, solve quick questions, and then revisit mistakes. Keep one short recap at the end of the day."

    if "study consistency" in normalized or "consistency" in normalized:
        return "Keep sessions short and consistent. Study your hardest subject early, take a 10-minute break, and protect at least one fixed time block daily."

    if "10 days" in normalized or "few days" in normalized:
        return "Focus on urgent exam topics, high-weightage chapters, and past-year questions. Reduce low-priority tasks and add a daily revision block of 30 minutes."

    if "ece" in normalized or "semester exams" in normalized:
        return "Prioritize high-weightage subjects, revise formulas and diagrams, and complete one timed test every alternate day. Keep your study blocks focused and consistent."

    return build_question_prompt(student, subjects, tasks, assignments, sessions, question)
