from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from database.crud import delete_assignment, delete_task, list_assignments, list_subjects, list_tasks, save_assignment, save_task


def render_tasks() -> None:
    """Manage tasks and assignments for the student."""
    st.title("Tasks & Assignments")
    st.caption("Stay on top of deadlines and academic work.")

    subjects = list_subjects()
    subject_names = [subject.subject_name for subject in subjects]

    task_tab, assignment_tab = st.tabs(["Tasks", "Assignments"])

    with task_tab:
        with st.form("task_form"):
            task_name = st.text_input("Task name")
            task_subject = st.selectbox("Subject", subject_names or ["General"])
            description = st.text_area("Description")
            due_date = st.date_input("Due date", value=date.today())
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            estimated_time = st.number_input("Estimated time (minutes)", min_value=15, max_value=300, value=60)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
            if st.form_submit_button("Add task"):
                try:
                    save_task(
                        {
                            "task_name": task_name,
                            "subject": task_subject,
                            "description": description,
                            "due_date": due_date,
                            "priority": priority,
                            "estimated_time": estimated_time,
                            "status": status,
                        }
                    )
                    st.success("Task saved successfully.")
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

        tasks = list_tasks()
        if not tasks:
            st.info("No tasks yet.")
        else:
            task_df = pd.DataFrame([
                {
                    "Task": task.task_name,
                    "Subject": task.subject,
                    "Due": str(task.due_date or "-"),
                    "Priority": task.priority,
                    "Estimated": task.estimated_time,
                    "Status": task.status,
                }
                for task in tasks
            ])
            st.dataframe(task_df, use_container_width=True)

            for task in tasks:
                col1, col2, col3 = st.columns([3, 1, 1])
                col1.write(f"{task.task_name} - {task.subject}")
                if col2.button("Complete", key=f"complete_task_{task.id}"):
                    save_task({
                        "id": task.id,
                        "task_name": task.task_name,
                        "subject": task.subject,
                        "description": task.description,
                        "due_date": task.due_date,
                        "priority": task.priority,
                        "estimated_time": task.estimated_time,
                        "status": "Completed",
                    })
                    st.rerun()
                if col3.button("Delete", key=f"delete_task_{task.id}"):
                    delete_task(task.id)
                    st.rerun()

    with assignment_tab:
        with st.form("assignment_form"):
            assignment_name = st.text_input("Assignment name", key="assignment_name")
            assignment_subject = st.selectbox("Subject", subject_names or ["General"], key="assignment_subject")
            deadline = st.date_input("Deadline", value=date.today(), key="assignment_deadline")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="assignment_priority")
            estimated_hours = st.number_input("Estimated hours", min_value=1, max_value=20, value=3, key="assignment_hours")
            assignment_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], key="assignment_status")
            if st.form_submit_button("Add assignment"):
                try:
                    save_assignment(
                        {
                            "assignment_name": assignment_name,
                            "subject": assignment_subject,
                            "deadline": deadline,
                            "estimated_hours": estimated_hours,
                            "priority": priority,
                            "status": assignment_status,
                        }
                    )
                    st.success("Assignment saved successfully.")
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

        assignments = list_assignments()
        if not assignments:
            st.info("No assignments yet.")
        else:
            assignment_df = pd.DataFrame([
                {
                    "Assignment": assignment.assignment_name,
                    "Subject": assignment.subject,
                    "Deadline": str(assignment.deadline or "-"),
                    "Priority": assignment.priority,
                    "Hours": assignment.estimated_hours,
                    "Status": assignment.status,
                }
                for assignment in assignments
            ])
            st.dataframe(assignment_df, use_container_width=True)

            for assignment in assignments:
                col1, col2, col3 = st.columns([3, 1, 1])
                col1.write(f"{assignment.assignment_name} - {assignment.subject}")
                if col2.button("Complete", key=f"complete_assignment_{assignment.id}"):
                    save_assignment({
                        "id": assignment.id,
                        "assignment_name": assignment.assignment_name,
                        "subject": assignment.subject,
                        "deadline": assignment.deadline,
                        "estimated_hours": assignment.estimated_hours,
                        "priority": assignment.priority,
                        "status": "Completed",
                    })
                    st.rerun()
                if col3.button("Delete", key=f"delete_assignment_{assignment.id}"):
                    delete_assignment(assignment.id)
                    st.rerun()
