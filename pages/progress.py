from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from database.crud import get_student, list_study_sessions, list_subjects, list_tasks
from services.progress import calculate_study_score


def render_progress() -> None:
    """Track study progress, compute scores, and record sessions."""
    student = get_student()
    subjects = list_subjects()
    tasks = list_tasks()
    sessions = list_study_sessions()

    if student is None:
        st.warning("Create your profile first.")
        return

    st.title("Progress Tracker")
    st.caption("Monitor your consistency and subject preparation.")

    score, explanation = calculate_study_score(student, subjects, tasks, [], sessions)
    st.subheader("Study Score")
    st.progress(score, text=f"Your Study Score: {score}/100")
    st.caption(explanation)

    if subjects:
        col1, col2, col3 = st.columns(3)
        for index, subject in enumerate(subjects):
            progress_value = min(100, max(0, subject.current_preparation))
            if index % 3 == 0:
                with col1:
                    st.write(subject.subject_name)
                    st.progress(progress_value)
                    st.caption(f"{progress_value}% prepared")
            elif index % 3 == 1:
                with col2:
                    st.write(subject.subject_name)
                    st.progress(progress_value)
                    st.caption(f"{progress_value}% prepared")
            else:
                with col3:
                    st.write(subject.subject_name)
                    st.progress(progress_value)
                    st.caption(f"{progress_value}% prepared")

    st.subheader("Log a study session")
    with st.form("study_session_form"):
        session_subject = st.selectbox("Subject", [subject.subject_name for subject in subjects] or ["General"])
        session_type = st.selectbox("Session type", ["Study", "Practice", "Revision", "Exam Prep"])
        session_duration = st.number_input("Duration (minutes)", min_value=15, max_value=240, value=60)
        session_notes = st.text_area("Notes")
        submitted = st.form_submit_button("Mark session completed")
        if submitted:
            from database.crud import save_study_session
            save_study_session({
                "session_date": date.today(),
                "subject_name": session_subject,
                "session_type": session_type,
                "duration_minutes": session_duration,
                "completed": True,
                "notes": session_notes,
            })
            st.success("Study session recorded successfully.")
            st.rerun()

    if sessions:
        st.subheader("Recent study sessions")
        session_df = pd.DataFrame([
            {
                "Date": str(session.session_date),
                "Subject": session.subject_name,
                "Type": session.session_type,
                "Minutes": session.duration_minutes,
                "Completed": "Yes" if session.completed else "No",
            }
            for session in sessions[-10:]
        ])
        st.dataframe(session_df, use_container_width=True)

        fig = px.bar(session_df, x="Date", y="Minutes", color="Subject", title="Study hours per day")
        st.plotly_chart(fig, use_container_width=True)
