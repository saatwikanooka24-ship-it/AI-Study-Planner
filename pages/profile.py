from __future__ import annotations

import streamlit as st

from database.crud import create_student_profile, get_student


def render_profile() -> None:
    """Allow the student to update profile information."""
    student = get_student()
    if student is None:
        st.warning("Create a student profile first.")
        return

    st.title("Student Profile")
    st.caption("Keep your academic details up to date.")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", value=student.name)
            email = st.text_input("Email", value=student.email)
            branch = st.selectbox("Branch", ["CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "AI & ML", "Data Science", "Other"], index=["CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "AI & ML", "Data Science", "Other"].index(student.branch))
            year = st.selectbox("Year", ["1", "2", "3", "4"], index=["1", "2", "3", "4"].index(student.year))
        with col2:
            semester = st.selectbox("Semester", ["1", "2", "3", "4", "5", "6", "7", "8"], index=["1", "2", "3", "4", "5", "6", "7", "8"].index(student.semester))
            college = st.text_input("College", value=student.college)
            study_hours = st.number_input("Study hours per day", min_value=1, max_value=16, value=student.study_hours_per_day)
            preferred_time = st.selectbox("Preferred study time", ["Morning", "Afternoon", "Evening", "Night"], index=["Morning", "Afternoon", "Evening", "Night"].index(student.preferred_study_time))

        difficulty_preference = st.selectbox("Difficulty preference", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(student.difficulty_preference))
        learning_style = st.selectbox("Learning style", ["Visual", "Reading/Writing", "Practice-based", "Mixed"], index=["Visual", "Reading/Writing", "Practice-based", "Mixed"].index(student.learning_style))

        submitted = st.form_submit_button("Save profile")
        if submitted:
            try:
                create_student_profile(
                    {
                        "name": name,
                        "email": email,
                        "branch": branch,
                        "year": year,
                        "semester": semester,
                        "college": college,
                        "study_hours_per_day": study_hours,
                        "preferred_study_time": preferred_time,
                        "difficulty_preference": difficulty_preference,
                        "learning_style": learning_style,
                    }
                )
                st.success("Profile saved successfully.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
