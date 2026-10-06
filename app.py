import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from database.crud import create_student_profile, get_student, load_sample_data
from database.database import init_db
from pages.ai_assistant import render_ai_assistant
from pages.analytics import render_analytics
from pages.dashboard import render_dashboard
from pages.planner import render_planner
from pages.profile import render_profile
from pages.progress import render_progress
from pages.settings import render_settings
from pages.subjects import render_subjects
from pages.tasks import render_tasks

load_dotenv()


def render_welcome_screen() -> None:
    """Show a simple onboarding flow for first-time users."""
    st.title("AI Study Planner")
    st.caption("Plan smarter. Study better. Achieve more.")
    st.info("Welcome! Set up your profile and subjects to generate your personalized study plan.")

    with st.form("welcome_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="name@college.edu")
            branch = st.selectbox("Branch", ["CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "AI & ML", "Data Science", "Other"])
            year = st.selectbox("Year", ["1", "2", "3", "4"])
        with col2:
            semester = st.selectbox("Semester", ["1", "2", "3", "4", "5", "6", "7", "8"])
            college = st.text_input("College", placeholder="Your college name")
            study_hours = st.number_input("Study hours per day", min_value=1, max_value=16, value=4)
            preferred_study_time = st.selectbox("Preferred study time", ["Morning", "Afternoon", "Evening", "Night"])

        submitted = st.form_submit_button("Create profile")
        if submitted:
            if not name or not email or not college:
                st.error("Please fill in your name, email, and college before continuing.")
                return
            create_student_profile(
                {
                    "name": name,
                    "email": email,
                    "branch": branch,
                    "year": year,
                    "semester": semester,
                    "college": college,
                    "study_hours_per_day": study_hours,
                    "preferred_study_time": preferred_study_time,
                    "difficulty_preference": "Medium",
                    "learning_style": "Mixed",
                }
            )
            st.success("Profile created successfully!")
            st.rerun()

    sample_data = st.button("Load sample B.Tech data")
    if sample_data:
        load_sample_data()
        st.success("Sample data loaded successfully.")
        st.rerun()


def main() -> None:
    """Application entry point."""
    BASE_DIR = Path(__file__).resolve().parent
    os.makedirs(BASE_DIR / "data", exist_ok=True)
    init_db()

    st.set_page_config(
        page_title="AI Study Planner",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    student = get_student()
    if student is None:
        render_welcome_screen()
        return

    nav_options = {
        "Dashboard": "dashboard",
        "Student Profile": "profile",
        "Subjects": "subjects",
        "AI Study Planner": "planner",
        "Tasks & Assignments": "tasks",
        "Progress Tracker": "progress",
        "AI Study Assistant": "ai_assistant",
        "Analytics": "analytics",
        "Settings": "settings",
    }

    with st.sidebar:
        st.title("AI Study Planner")
        st.caption("Plan smarter. Study better. Achieve more.")
        navigation = st.radio("Navigation", list(nav_options.keys()), index=0)

    if navigation == "Dashboard":
        render_dashboard()
    elif navigation == "Student Profile":
        render_profile()
    elif navigation == "Subjects":
        render_subjects()
    elif navigation == "AI Study Planner":
        render_planner()
    elif navigation == "Tasks & Assignments":
        render_tasks()
    elif navigation == "Progress Tracker":
        render_progress()
    elif navigation == "AI Study Assistant":
        render_ai_assistant()
    elif navigation == "Analytics":
        render_analytics()
    elif navigation == "Settings":
        render_settings()


if __name__ == "__main__":
    main()
