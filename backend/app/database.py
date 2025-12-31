"""Simplified database models."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, Integer, DateTime, ForeignKey,
    Index, CheckConstraint, Float, Uuid
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

from .config import settings


class Base(DeclarativeBase):
    """Base model."""


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plans = relationship("Plan", back_populates="user", cascade="all, delete-orphan")


class Plan(Base):
    """Plan model."""
    __tablename__ = "plans"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="draft", nullable=False)
    # AI fields
    ai_generated_data = Column(Text)  # JSON string for AI analysis
    original_thought = Column(Text)   # Raw user input
    ai_metadata = Column(Text)        # Additional AI metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="plans")
    tasks = relationship("Task", back_populates="plan", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_plans_user_id", "user_id"),
        Index("idx_plans_status", "status"),
        CheckConstraint("status IN ('draft', 'active', 'completed', 'archived')", name="check_plan_status"),
    )


class Task(Base):
    """Task model."""
    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    plan_id = Column(Uuid, ForeignKey("plans.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=3, nullable=False)
    status = Column(String, default="pending", nullable=False)
    # AI fields
    ai_category = Column(String)      # AI-assigned category
    ai_priority_score = Column(Integer)  # AI-calculated priority
    ai_reasoning = Column(Text)       # AI reasoning for priority
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plan = relationship("Plan", back_populates="tasks")

    # Indexes
    __table_args__ = (
        Index("idx_tasks_plan_id", "plan_id"),
        Index("idx_tasks_status", "status"),
        Index("idx_tasks_ai_category", "ai_category"),
        CheckConstraint("priority BETWEEN 1 AND 5", name="check_task_priority"),
        CheckConstraint("status IN ('todo', 'doing', 'upcoming', 'completed', 'pending', 'in_progress')", name="check_task_status"),
        CheckConstraint("ai_priority_score BETWEEN 1 AND 10", name="check_ai_priority_score"),
    )


class AIInteraction(Base):
    """AI Interaction model for tracking AI usage and analytics."""
    __tablename__ = "ai_interactions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Uuid, ForeignKey("plans.id"), nullable=False)
    interaction_type = Column(String, nullable=False)  # 'analysis', 'categorization', 'ranking', 'dashboard'
    request_data = Column(Text)        # JSON request
    response_data = Column(Text)       # JSON response
    tokens_used = Column(Integer, default=0)
    cost_estimate = Column(Float, default=0.0)
    model_used = Column(String)
    response_time_ms = Column(Integer)  # Response time in milliseconds
    user_feedback = Column(Integer)    # User satisfaction rating 1-5
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
    plan = relationship("Plan")

    # Indexes
    __table_args__ = (
        Index("idx_ai_interactions_user_id", "user_id"),
        Index("idx_ai_interactions_plan_id", "plan_id"),
        Index("idx_ai_interactions_type", "interaction_type"),
        Index("idx_ai_interactions_created_at", "created_at"),
        CheckConstraint("interaction_type IN ('analysis', 'categorization', 'ranking', 'dashboard')", name="check_interaction_type"),
        CheckConstraint("user_feedback BETWEEN 1 AND 5", name="check_user_feedback"),
    )


# Database setup
engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession)


async def get_db():
    """Get database session."""
    async with async_session() as session:
        yield session


# Export models
__all__ = ["User", "Plan", "Task", "AIInteraction", "get_db"]