
"""Simplified Pydantic schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema."""
    model_config = {"from_attributes": True}


class Plan(BaseSchema):
    """Plan schema."""
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    status: str
    original_thought: Optional[str] = None
    ai_generated_data: Optional[str] = None
    ai_metadata: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PlanCreate(BaseModel):
    """Schema for creating plans."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    original_thought: Optional[str] = None
    status: Optional[str] = "draft"


class Task(BaseSchema):
    """Task schema."""
    id: UUID
    plan_id: UUID
    title: str
    description: Optional[str] = None
    priority: int
    status: str
    ai_category: Optional[str] = None
    ai_priority_score: Optional[int] = None
    ai_reasoning: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    """Schema for creating tasks."""
    plan_id: UUID
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: int = Field(default=3, ge=1, le=5)


class User(BaseSchema):
    """User schema."""
    id: UUID
    email: str
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# AI-related schemas

class TaskCategory(BaseSchema):
    """Task category schema."""
    name: str = Field(..., description="Name of the category")
    description: str = Field(..., description="Description of what this category includes")
    tasks: List[UUID] = Field(default_factory=list, description="List of task IDs in this category")
    priority_ranking: int = Field(..., ge=1, le=5, description="Priority ranking of this category")


class TaskCategoryWithTasks(TaskCategory):
    """Task category schema with full task details."""
    tasks: List[Task] = Field(description="Full task details")


class PriorityAnalysis(BaseModel):
    """Priority analysis schema."""
    task_id: UUID
    task_title: str
    ai_priority_score: int = Field(..., ge=1, le=10, description="AI-calculated priority score (1-10)")
    reasoning: str = Field(..., description="AI reasoning for this priority")
    estimated_effort: str = Field(..., description="Estimated effort: Low/Medium/High")
    dependencies: List[int] = Field(default_factory=list, description="Indices of dependent tasks")
    impact_level: str = Field(..., description="Impact level: Low/Medium/High")


class AIDashboardSuggestion(BaseModel):
    """AI dashboard suggestion schema."""
    plan_id: UUID
    plan_title: str
    dashboard_title: str
    summary: str
    categories: List[TaskCategory]
    priority_groups: Dict[str, List[UUID]]
    recommendations: List[str]
    estimated_completion_time: str
    next_steps: List[str]
    metadata: Dict[str, Any]


class UserApprovalRequest(BaseModel):
    """User approval request schema."""
    suggestion: AIDashboardSuggestion
    approval_required: bool = True
    user_feedback: Optional[str] = None


class UserApprovalResponse(BaseModel):
    """User approval response schema."""
    approved: bool
    feedback: Optional[str] = None
    modifications: Optional[Dict[str, Any]] = None


class AIInteraction(BaseModel):
    """AI interaction schema."""
    model_config = {"protected_namespaces": ()}

    id: UUID
    user_id: UUID
    plan_id: UUID
    interaction_type: str
    request_data: Optional[str] = None
    response_data: Optional[str] = None
    tokens_used: int = 0
    cost_estimate: float = 0.0
    model_used: Optional[str] = None
    response_time_ms: Optional[int] = None
    user_feedback: Optional[int] = Field(None, ge=1, le=5)
    created_at: datetime


class AIAnalysisRequest(BaseModel):
    """AI analysis request schema."""
    plan_id: UUID
    analysis_type: str = Field(..., description="Type of analysis: categorization, priority, dashboard")
    user_context: Optional[Dict[str, Any]] = None


class AIAnalysisResponse(BaseModel):
    """AI analysis response schema."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    interaction_id: Optional[UUID] = None


class EnhancedPlan(Plan):
    """Enhanced plan schema with AI fields."""
    ai_generated_data: Optional[str] = None
    original_thought: Optional[str] = None
    ai_metadata: Optional[str] = None


class EnhancedTask(Task):
    """Enhanced task schema with AI fields."""
    ai_category: Optional[str] = None
    ai_priority_score: Optional[int] = Field(None, ge=1, le=10)
    ai_reasoning: Optional[str] = None


class AIRecommendation(BaseModel):
    """AI recommendation schema."""
    type: str
    title: str
    description: str
    priority: str
    estimated_impact: str
    action_items: List[str]


class AIDashboardGeneration(BaseModel):
    """AI dashboard generation request."""
    plan_id: UUID
    include_categorization: bool = True
    include_priority_scoring: bool = True
    include_recommendations: bool = True
    user_preferences: Optional[Dict[str, Any]] = None


# Enhanced create schemas with AI support

class PlanCreateWithAI(PlanCreate):
    """Enhanced plan creation schema with AI support."""
    original_thought: Optional[str] = None
    generate_ai_suggestions: bool = False


class TaskCreateWithAI(TaskCreate):
    """Enhanced task creation schema with AI support."""
    ai_category: Optional[str] = None
    suggested_priority: Optional[int] = Field(None, ge=1, le=10)