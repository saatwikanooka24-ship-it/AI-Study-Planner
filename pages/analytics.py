from __future__ import annotations

import streamlit as st

from database.crud import list_assignments, list_study_sessions, list_subjects, list_tasks
from services.analytics import build_charts_data


def render_analytics() -> None:
    """Display analytics charts for study progress and academic load."""
    st.title("Analytics")
    st.caption("Monitor your preparation trends and weekly performance.")

    subjects = list_subjects()
    tasks = list_tasks()
    sessions = list_study_sessions()
    charts = build_charts_data(subjects, tasks, sessions)

    if not subjects and not tasks and not sessions:
        st.info("Add subjects and track study sessions to unlock analytics.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts["hours_chart"], use_container_width=True)
        st.plotly_chart(charts["subject_chart"], use_container_width=True)
    with col2:
        st.plotly_chart(charts["task_chart"], use_container_width=True)

    if not charts["subject_df"].empty:
        st.subheader("Preparation overview")
        st.dataframe(charts["subject_df"], use_container_width=True)
