from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from ai.planner import generate_study_plan
from database.crud import get_student, list_subjects, save_study_plan
from services.scheduler import build_weekly_timetable


def render_planner() -> None:
    """Generate an AI-powered study plan from the profile and subjects."""
    student = get_student()
    subjects = list_subjects()
    if student is None:
        st.warning("Create your profile first.")
        return
    if not subjects:
        st.warning("Add at least one subject before generating a study plan.")
        return

    st.title("AI Study Planner")
    st.caption("Create a personalized plan around your subjects, deadlines, and daily study capacity.")

    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=date.today())
            end_date = st.date_input("End date", value=date.today())
            daily_study_hours = st.number_input("Daily study hours", min_value=1, max_value=12, value=student.study_hours_per_day)
            preferred_time = st.selectbox("Preferred study time", ["Morning", "Afternoon", "Evening", "Night"], index=["Morning", "Afternoon", "Evening", "Night"].index(student.preferred_study_time))
        with col2:
            break_duration = st.number_input("Break duration (minutes)", min_value=5, max_value=30, value=10)
            revision_mode = st.checkbox("Revision mode")
            exam_mode = st.checkbox("Exam mode")
            selected_subjects = st.multiselect("Subjects", [subject.subject_name for subject in subjects], default=[subject.subject_name for subject in subjects[:3]])

        submitted = st.form_submit_button("Generate AI Study Plan")
        if submitted:
            chosen_subjects = [subject for subject in subjects if subject.subject_name in selected_subjects]
            if not chosen_subjects:
                st.error("Please select at least one subject.")
                st.stop()
            try:
                plan = generate_study_plan(
                    student,
                    chosen_subjects,
                    start_date,
                    end_date,
                    daily_study_hours,
                    preferred_time,
                    break_duration,
                    revision_mode=revision_mode,
                    exam_mode=exam_mode,
                )
                save_study_plan({
                    "plan_name": "AI Study Plan",
                    "start_date": start_date,
                    "end_date": end_date,
                    "plan_content": str(plan),
                })
                st.session_state["study_plan"] = plan
                st.success("Study plan generated successfully.")
            except ValueError as exc:
                st.error(str(exc))

    if "study_plan" in st.session_state:
        plan = st.session_state["study_plan"]
        st.subheader("Generated study schedule")
        for day_plan in plan:
            with st.expander(f"{day_plan['day']} - {day_plan['date']}"):
                for session in day_plan["sessions"]:
                    st.write(f"{session['time']}: {session['subject']} | {session['topic']} | {session['duration']} min")

        weekly_entries = build_weekly_timetable(chosen_subjects if "chosen_subjects" in locals() else subjects, start_date, daily_study_hours, preferred_time, break_duration)
        if weekly_entries:
            st.subheader("Weekly timetable")
            st.dataframe(pd.DataFrame(weekly_entries), use_container_width=True)
