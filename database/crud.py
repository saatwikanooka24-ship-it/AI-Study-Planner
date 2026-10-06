from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import select

from database.database import SessionLocal
from database.models import Assignment, Student, StudyPlan, StudySession, Subject, Task
from utils.helpers import parse_date
from utils.validators import validate_assignment_data, validate_profile_data, validate_subject_data, validate_task_data


def get_student() -> Student | None:
    """Return the first student record or None."""
    with SessionLocal() as session:
        student = session.execute(select(Student)).scalar_one_or_none()
        return student


def create_student_profile(data: dict[str, Any]) -> Student:
    """Create or update a single student profile record."""
    validated = validate_profile_data(data)
    with SessionLocal() as session:
        student = session.execute(select(Student)).scalar_one_or_none()
        if student is None:
            student = Student(**validated)
            session.add(student)
        else:
            for key, value in validated.items():
                setattr(student, key, value)
        session.commit()
        session.refresh(student)
        return student


def list_subjects() -> list[Subject]:
    with SessionLocal() as session:
        return session.execute(select(Subject).order_by(Subject.subject_name.asc())).scalars().all()


def save_subject(subject_data: dict[str, Any]) -> Subject:
    validated = validate_subject_data(subject_data)
    with SessionLocal() as session:
        subject_id = validated.pop("id", None)
        subject = None
        if subject_id:
            subject = session.get(Subject, int(subject_id))
        if subject is None:
            subject = Subject(**validated)
            session.add(subject)
        else:
            for key, value in validated.items():
                setattr(subject, key, value)
        session.commit()
        session.refresh(subject)
        return subject


def delete_subject(subject_id: int) -> None:
    with SessionLocal() as session:
        subject = session.get(Subject, subject_id)
        if subject:
            session.delete(subject)
            session.commit()


def list_tasks() -> list[Task]:
    with SessionLocal() as session:
        return session.execute(select(Task).order_by(Task.due_date.is_(None), Task.due_date.asc())).scalars().all()


def save_task(task_data: dict[str, Any]) -> Task:
    validated = validate_task_data(task_data)
    with SessionLocal() as session:
        task_id = validated.pop("id", None)
        task = None
        if task_id:
            task = session.get(Task, int(task_id))
        if task is None:
            task = Task(**validated)
            session.add(task)
        else:
            for key, value in validated.items():
                setattr(task, key, value)
        session.commit()
        session.refresh(task)
        return task


def delete_task(task_id: int) -> None:
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        if task:
            session.delete(task)
            session.commit()


def list_assignments() -> list[Assignment]:
    with SessionLocal() as session:
        return session.execute(select(Assignment).order_by(Assignment.deadline.is_(None), Assignment.deadline.asc())).scalars().all()


def save_assignment(data: dict[str, Any]) -> Assignment:
    validated = validate_assignment_data(data)
    with SessionLocal() as session:
        assignment_id = validated.pop("id", None)
        assignment = None
        if assignment_id:
            assignment = session.get(Assignment, int(assignment_id))
        if assignment is None:
            assignment = Assignment(**validated)
            session.add(assignment)
        else:
            for key, value in validated.items():
                setattr(assignment, key, value)
        session.commit()
        session.refresh(assignment)
        return assignment


def delete_assignment(assignment_id: int) -> None:
    with SessionLocal() as session:
        assignment = session.get(Assignment, assignment_id)
        if assignment:
            session.delete(assignment)
            session.commit()


def list_study_sessions() -> list[StudySession]:
    with SessionLocal() as session:
        return session.execute(select(StudySession).order_by(StudySession.session_date.desc())).scalars().all()


def save_study_session(data: dict[str, Any]) -> StudySession:
    with SessionLocal() as session:
        study_session = StudySession(**data)
        session.add(study_session)
        session.commit()
        session.refresh(study_session)
        return study_session


def list_study_plans() -> list[StudyPlan]:
    with SessionLocal() as session:
        return session.execute(select(StudyPlan).order_by(StudyPlan.created_at.desc())).scalars().all()


def save_study_plan(plan: dict[str, Any]) -> StudyPlan:
    with SessionLocal() as session:
        db_plan = StudyPlan(**plan)
        session.add(db_plan)
        session.commit()
        session.refresh(db_plan)
        return db_plan


def load_sample_data() -> None:
    """Insert a realistic sample student profile and academic data for demo use."""
    student = get_student()
    if student is None:
        create_student_profile(
            {
                "name": "Aarav Sharma",
                "email": "aarav@college.edu",
                "branch": "ECE",
                "year": "3",
                "semester": "5",
                "college": "NIT Engineering College",
                "study_hours_per_day": 5,
                "preferred_study_time": "Evening",
                "difficulty_preference": "Hard",
                "learning_style": "Mixed",
            }
        )

    with SessionLocal() as session:
        existing_subjects = session.execute(select(Subject)).scalars().all()
        if not existing_subjects:
            subjects = [
                Subject(subject_name="Digital Electronics", subject_code="DE101", credits=4, difficulty="Hard", current_preparation=45, target_percentage=80, exam_date=date(2026, 10, 20), notes="Focus on sequential circuits and logic families."),
                Subject(subject_name="Signals and Systems", subject_code="SS201", credits=4, difficulty="Medium", current_preparation=58, target_percentage=78, exam_date=date(2026, 10, 24), notes="Practice Fourier and Laplace transform questions."),
                Subject(subject_name="Network Theory", subject_code="NT204", credits=3, difficulty="Medium", current_preparation=60, target_percentage=82, exam_date=date(2026, 10, 28), notes="Revise Thevenin and network simplification."),
                Subject(subject_name="Engineering Mathematics", subject_code="MTH112", credits=4, difficulty="Hard", current_preparation=50, target_percentage=85, exam_date=date(2026, 10, 18), notes="Solve differential equations and probability problems."),
                Subject(subject_name="Python Programming", subject_code="PY101", credits=3, difficulty="Easy", current_preparation=75, target_percentage=90, exam_date=date(2026, 11, 2), notes="Practice coding and debugging exercises."),
            ]
            session.add_all(subjects)

        existing_tasks = session.execute(select(Task)).scalars().all()
        if not existing_tasks:
            session.add_all(
                [
                    Task(task_name="Prepare circuit analysis notes", subject="Digital Electronics", description="Revise sequential circuits and K-maps.", due_date=date(2026, 10, 10), priority="High", estimated_time=90, status="Pending"),
                    Task(task_name="Solve Signals assignment", subject="Signals and Systems", description="Complete four Fourier transform questions.", due_date=date(2026, 10, 12), priority="High", estimated_time=80, status="In Progress"),
                    Task(task_name="Mathematics revision set", subject="Engineering Mathematics", description="Work through 10 differential equation questions.", due_date=date(2026, 10, 14), priority="Medium", estimated_time=70, status="Pending"),
                    Task(task_name="Python lab practice", subject="Python Programming", description="Finish file handling and loops assignment.", due_date=date(2026, 10, 11), priority="Medium", estimated_time=60, status="Completed"),
                ]
            )

        existing_assignments = session.execute(select(Assignment)).scalars().all()
        if not existing_assignments:
            session.add_all(
                [
                    Assignment(assignment_name="Digital Electronics lab report", subject="Digital Electronics", deadline=date(2026, 10, 9), estimated_hours=4, priority="High", status="Pending"),
                    Assignment(assignment_name="Signals handwritten notes", subject="Signals and Systems", deadline=date(2026, 10, 15), estimated_hours=3, priority="Medium", status="Pending"),
                    Assignment(assignment_name="Math worksheet submission", subject="Engineering Mathematics", deadline=date(2026, 10, 16), estimated_hours=2, priority="High", status="Pending"),
                ]
            )

        existing_sessions = session.execute(select(StudySession)).scalars().all()
        if not existing_sessions:
            session.add_all(
                [
                    StudySession(session_date=date(2026, 10, 6), subject_name="Digital Electronics", session_type="Study", duration_minutes=90, completed=True, notes="Sequential circuits revision."),
                    StudySession(session_date=date(2026, 10, 7), subject_name="Signals and Systems", session_type="Practice", duration_minutes=80, completed=True, notes="Laplace transforms."),
                    StudySession(session_date=date(2026, 10, 8), subject_name="Engineering Mathematics", session_type="Revision", duration_minutes=60, completed=False, notes="Differential equations."),
                ]
            )

        session.commit()
