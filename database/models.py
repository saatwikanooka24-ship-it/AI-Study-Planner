from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    branch: Mapped[str] = mapped_column(String(100), default="CSE")
    year: Mapped[str] = mapped_column(String(20), default="2")
    semester: Mapped[str] = mapped_column(String(20), default="4")
    college: Mapped[str] = mapped_column(String(200), default="")
    study_hours_per_day: Mapped[int] = mapped_column(Integer, default=4)
    preferred_study_time: Mapped[str] = mapped_column(String(50), default="Evening")
    difficulty_preference: Mapped[str] = mapped_column(String(20), default="Medium")
    learning_style: Mapped[str] = mapped_column(String(50), default="Mixed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subject_name: Mapped[str] = mapped_column(String(200), nullable=False)
    subject_code: Mapped[str] = mapped_column(String(50), default="")
    credits: Mapped[int] = mapped_column(Integer, default=3)
    difficulty: Mapped[str] = mapped_column(String(20), default="Medium")
    current_preparation: Mapped[int] = mapped_column(Integer, default=35)
    target_percentage: Mapped[int] = mapped_column(Integer, default=75)
    exam_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_name: Mapped[str] = mapped_column(String(200), nullable=False)
    subject: Mapped[str] = mapped_column(String(200), default="General")
    description: Mapped[str] = mapped_column(Text, default="")
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="Medium")
    estimated_time: Mapped[int] = mapped_column(Integer, default=60)
    status: Mapped[str] = mapped_column(String(20), default="Pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assignment_name: Mapped[str] = mapped_column(String(200), nullable=False)
    subject: Mapped[str] = mapped_column(String(200), default="General")
    deadline: Mapped[Date | None] = mapped_column(Date, nullable=True)
    estimated_hours: Mapped[int] = mapped_column(Integer, default=3)
    priority: Mapped[str] = mapped_column(String(20), default="Medium")
    status: Mapped[str] = mapped_column(String(20), default="Pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StudySession(Base):
    __tablename__ = "study_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_date: Mapped[Date] = mapped_column(Date, default=datetime.utcnow().date())
    subject_name: Mapped[str] = mapped_column(String(200), default="General")
    session_type: Mapped[str] = mapped_column(String(50), default="Study")
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plan_name: Mapped[str] = mapped_column(String(200), default="Study plan")
    start_date: Mapped[Date] = mapped_column(Date, default=datetime.utcnow().date())
    end_date: Mapped[Date] = mapped_column(Date, default=datetime.utcnow().date())
    plan_content: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
