from __future__ import annotations

import streamlit as st

from ai.recommender import generate_recommendations
from database.crud import get_student, list_assignments, list_study_sessions, list_subjects, list_tasks
from services.progress import calculate_study_score, compute_dashboard_metrics


def render_dashboard() -> None:
    """Render the main dashboard with student summary and recommendations."""
    student = get_student()
    subjects = list_subjects()
    tasks = list_tasks()
    assignments = list_assignments()
    sessions = list_study_sessions()

    if student is None:
        st.warning("Create a profile to see the dashboard.")
        return

    st.title("Dashboard")
    st.caption("Your personalized study overview")

    metrics = compute_dashboard_metrics(student, subjects, tasks, assignments, sessions)
    score, explanation = calculate_study_score(student, subjects, tasks, assignments, sessions)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Student", metrics["student_name"])
    col2.metric("Branch", metrics["branch"])
    col3.metric("Semester", f"{metrics['year']} / {metrics['semester']}")
    col4.metric("Today", f"{metrics['study_hours_today']} min")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Completed tasks", metrics["completed_tasks"])
    col2.metric("Pending tasks", metrics["pending_tasks"])
    col3.metric("Upcoming exams", metrics["upcoming_exams"])
    col4.metric("Overall progress", f"{metrics['overall_progress']}%")

    row = st.columns(4)
    row[0].metric("Study streak", f"{metrics['study_streak']} days")
    row[1].metric("Assignments", metrics["upcoming_assignments"])
    row[2].metric("Study Score", f"{score}/100")
    row[3].metric("Study hours", f"{metrics['study_hours_today']} min")

    st.subheader("Today's plan")
    if tasks:
        sorted_tasks = sorted(tasks, key=lambda task: (task.status != "Pending", str(task.due_date or "9999-12-31"), task.priority))
        for task in sorted_tasks[:5]:
            with st.container():
                st.markdown(f"- {task.task_name} • {task.subject} • {task.priority} • {task.status}")
    else:
        st.info("No tasks available. Add some tasks to build a daily plan.")

    st.subheader("Study score and tip")
    st.progress(score)
    st.write(f"Your Study Score: {score}/100")
    st.caption(explanation)

    recommendations = generate_recommendations(student, subjects, tasks, assignments, sessions)
    if recommendations:
        st.subheader("AI recommendations")
        for item in recommendations:
            st.info(item)

    st.subheader("Upcoming exam and assignments")
    exam_cols = st.columns(2)
    with exam_cols[0]:
        st.write("Upcoming exams")
        if subjects:
            for subject in sorted(subjects, key=lambda ref: str(ref.exam_date or "9999-12-31")):
                if getattr(subject, "exam_date", None):
                    days_left = (subject.exam_date - __import__("datetime").date.today()).days
                    st.markdown(f"- {subject.subject_name}: {subject.exam_date} ({days_left} days left)")
        else:
            st.write("No exam dates added yet.")
    with exam_cols[1]:
        st.write("Pending assignments")
        if assignments:
            for assignment in assignments[:5]:
                st.markdown(f"- {assignment.assignment_name} • {assignment.subject} • {assignment.deadline}")
        else:
            st.write("No assignments added yet.")

    st.subheader("Start studying")
    if tasks:
        st.button("Mark first pending task as complete", key="complete_first_task")
        if "complete_first_task" in st.session_state and st.session_state.complete_first_task:
            first_pending = next((task for task in tasks if task.status != "Completed"), None)
            if first_pending:
                first_pending.status = "Completed"
                from database.crud import save_task
                save_task({"id": first_pending.id, "task_name": first_pending.task_name, "subject": first_pending.subject, "description": first_pending.description, "due_date": first_pending.due_date, "priority": first_pending.priority, "estimated_time": first_pending.estimated_time, "status": "Completed"})
                st.success("The first pending task has been marked complete.")
                st.rerun()
    else:
        st.info("Add your first task from the Tasks & Assignments page.")
