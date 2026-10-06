from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from database.crud import delete_subject, list_subjects, save_subject


def render_subjects() -> None:
    """Allow adding and viewing subjects."""
    st.title("Subjects")
    st.caption("Track your B.Tech subjects, preparation level, and exam dates.")

    with st.form("subject_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject_name = st.text_input("Subject name")
            subject_code = st.text_input("Subject code")
            credits = st.number_input("Credits", min_value=1, max_value=6, value=3)
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        with col2:
            current_preparation = st.slider("Current preparation (%)", 0, 100, 50)
            target_percentage = st.slider("Target percentage (%)", 0, 100, 80)
            exam_date = st.date_input("Exam date", value=date.today())
            notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save subject")
        if submitted:
            try:
                save_subject(
                    {
                        "subject_name": subject_name,
                        "subject_code": subject_code,
                        "credits": credits,
                        "difficulty": difficulty,
                        "current_preparation": current_preparation,
                        "target_percentage": target_percentage,
                        "exam_date": exam_date,
                        "notes": notes,
                    }
                )
                st.success("Subject saved successfully.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

    subjects = list_subjects()
    if not subjects:
        st.info("No subjects added yet. Add your first subject above.")
        return

    rows = [
        {
            "Subject": subject.subject_name,
            "Code": subject.subject_code,
            "Credits": subject.credits,
            "Difficulty": subject.difficulty,
            "Prep": subject.current_preparation,
            "Target": subject.target_percentage,
            "Exam": str(subject.exam_date) if subject.exam_date else "-",
            "Notes": subject.notes,
        }
        for subject in subjects
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    subject_to_delete = st.selectbox("Delete subject", [subject.subject_name for subject in subjects])
    if st.button("Delete selected subject"):
        for subject in subjects:
            if subject.subject_name == subject_to_delete:
                delete_subject(subject.id)
                st.success(f"Deleted {subject.subject_name}.")
                st.rerun()
                break
