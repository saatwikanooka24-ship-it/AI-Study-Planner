from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px


def build_charts_data(subjects: list[Any], tasks: list[Any], sessions: list[Any]) -> dict[str, Any]:
    """Create simple chart-ready DataFrames for analytics views."""
    subject_df = pd.DataFrame(
        [
            {
                "Subject": subject.subject_name,
                "Preparation": subject.current_preparation,
                "Target": subject.target_percentage,
            }
            for subject in subjects
        ],
        columns=["Subject", "Preparation", "Target"],
    )

    task_df = pd.DataFrame(
        [
            {"Status": task.status, "Task": task.task_name}
            for task in tasks
        ],
        columns=["Status", "Task"],
    )

    session_df = pd.DataFrame(
        [
            {"Subject": session.subject_name, "Minutes": session.duration_minutes, "Date": str(session.session_date)}
            for session in sessions
        ],
        columns=["Subject", "Minutes", "Date"],
    )

    empty_subject = pd.DataFrame({"Subject": ["No data"], "Preparation": [0], "Target": [0]})
    empty_tasks = pd.DataFrame({"Status": ["No tasks"], "Task": ["-"], "Count": [1]})
    empty_sessions = pd.DataFrame({"Subject": ["No data"], "Minutes": [0], "Date": ["-"]})

    if subject_df.empty:
        subject_df = empty_subject
    if task_df.empty:
        task_df = empty_tasks
    if session_df.empty:
        session_df = empty_sessions

    task_chart_source = task_df.copy()
    if "Count" not in task_chart_source.columns:
        task_chart_source["Count"] = 1

    return {
        "subject_df": subject_df,
        "task_df": task_df,
        "session_df": session_df,
        "subject_chart": px.bar(subject_df, x="Subject", y="Preparation", title="Subject preparation"),
        "task_chart": px.pie(task_chart_source, names="Status", values="Count", title="Completed vs pending tasks"),
        "hours_chart": px.bar(session_df, x="Date", y="Minutes", color="Subject", title="Study hours per day"),
    }
