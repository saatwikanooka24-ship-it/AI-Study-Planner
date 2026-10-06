from __future__ import annotations

import streamlit as st

from ai.recommender import answer_student_question, generate_recommendations, get_ai_mode
from database.crud import get_student, list_assignments, list_study_sessions, list_subjects, list_tasks


def render_ai_assistant() -> None:
    """Chatbot-style assistant using local recommendation logic."""
    student = get_student()
    if student is None:
        st.warning("Create your profile first to use the assistant.")
        return

    st.title("AI Study Assistant")
    st.caption(get_ai_mode())

    subjects = list_subjects()
    tasks = list_tasks()
    assignments = list_assignments()
    sessions = list_study_sessions()

    recommended_questions = [
        "How should I prepare for my ECE semester exams?",
        "I have only 10 days for exams. Make me a plan.",
        "Which subject should I study today?",
        "I am weak in Digital Electronics. What should I do?",
        "Give me a revision strategy.",
        "How can I improve my study consistency?",
    ]

    st.subheader("Ask a question")
    question = st.selectbox("Sample questions", recommended_questions, index=0)
    if st.button("Get guidance"):
        answer = answer_student_question(question, student, subjects, tasks, assignments, sessions)
        st.markdown(f"**Answer:**\n{answer}")

    st.subheader("Personalized recommendations")
    for item in generate_recommendations(student, subjects, tasks, assignments, sessions):
        st.info(item)
