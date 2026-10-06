from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from ai.recommender import get_ai_mode


def render_settings() -> None:
    """Display local app settings and environment status without exposing sensitive values."""
    st.title("Settings")
    st.caption("Academic planning preferences and local system state.")

    st.subheader("AI configuration")
    api_key = os.getenv("AI_API_KEY")
    st.write(get_ai_mode())
    st.write(f"API key configured: {'Yes' if api_key else 'No'}")

    st.subheader("Local data")
    data_path = Path(__file__).resolve().parents[1] / "data" / "study_planner.db"
    st.write(f"Database file: {data_path}")

    st.subheader("Study preferences")
    if "revision_mode" not in st.session_state:
        st.session_state.revision_mode = False
    if "exam_mode" not in st.session_state:
        st.session_state.exam_mode = False

    st.session_state.revision_mode = st.checkbox("Revision mode enabled", value=st.session_state.revision_mode)
    st.session_state.exam_mode = st.checkbox("Exam mode enabled", value=st.session_state.exam_mode)

    st.info("Use the AI Study Planner and dashboard pages to update your study flow. These settings affect the local planning experience.")
