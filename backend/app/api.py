"""Minimal API routes for Mindmesh backend."""

import json
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from .database import get_db, User, Plan, Task, AIInteraction
from .schemas import (
    Plan as PlanSchema, PlanCreate, Task as TaskSchema, TaskCreate,
    AIAnalysisRequest, AIAnalysisResponse, AIDashboardSuggestion,
    UserApprovalRequest, UserApprovalResponse, EnhancedPlan, EnhancedTask
)
from .auth import get_current_user
from .ai_service import ai_service

logger = logging.getLogger(__name__)

# Create router
api_router = APIRouter(prefix="/api", tags=["api"])

# Health endpoint
@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

# Plans endpoints
@api_router.post("/plans", response_model=PlanSchema)
async def create_plan(
    plan: PlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new plan."""
    db_plan = Plan(
        user_id=current_user.id,
        title=plan.title,
        description=plan.description,
        original_thought=plan.original_thought,
        status=plan.status or "draft"
    )
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)
    return db_plan

@api_router.get("/plans", response_model=List[PlanSchema])
async def get_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's plans."""
    result = await db.execute(
        select(Plan)
        .where(Plan.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(Plan.created_at.desc())
    )
    return result.scalars().all()

@api_router.get("/plans/{plan_id}", response_model=PlanSchema)
async def get_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific plan."""
    result = await db.execute(
        select(Plan)
        .where(Plan.id == plan_id, Plan.user_id == current_user.id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@api_router.put("/plans/{plan_id}", response_model=PlanSchema)
async def update_plan(
    plan_id: UUID,
    plan_update: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a plan."""
    result = await db.execute(
        select(Plan)
        .where(Plan.id == plan_id, Plan.user_id == current_user.id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Update fields if provided
    for key, value in plan_update.items():
        if hasattr(plan, key) and value is not None:
            setattr(plan, key, value)

    await db.commit()
    await db.refresh(plan)
    return plan

@api_router.delete("/plans/{plan_id}")
async def delete_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a plan."""
    result = await db.execute(
        select(Plan)
        .where(Plan.id == plan_id, Plan.user_id == current_user.id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    await db.delete(plan)
    await db.commit()
    return {"message": "Plan deleted"}

# Tasks endpoints
@api_router.get("/tasks", response_model=List[TaskSchema])
async def get_all_tasks(
    plan_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all user's tasks, optionally filtered by plan."""
    query = select(Task).join(Plan).where(Plan.user_id == current_user.id)

    if plan_id:
        query = query.where(Task.plan_id == plan_id)

    query = query.order_by(Task.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()

@api_router.post("/tasks", response_model=TaskSchema)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task."""
    # Verify plan ownership
    plan_result = await db.execute(
        select(Plan)
        .where(Plan.id == task.plan_id, Plan.user_id == current_user.id)
    )
    if not plan_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Plan not found")

    db_task = Task(
        plan_id=task.plan_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        status="pending"
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@api_router.get("/plans/{plan_id}/tasks", response_model=List[TaskSchema])
async def get_plan_tasks(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tasks for a plan."""
    # Verify plan ownership
    plan_result = await db.execute(
        select(Plan)
        .where(Plan.id == plan_id, Plan.user_id == current_user.id)
    )
    if not plan_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Plan not found")

    result = await db.execute(
        select(Task)
        .where(Task.plan_id == plan_id)
        .order_by(Task.created_at)
    )
    return result.scalars().all()

@api_router.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task."""
    result = await db.execute(
        select(Task)
        .join(Plan)
        .where(Task.id == task_id, Plan.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@api_router.put("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: UUID,
    task_update: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a task."""
    result = await db.execute(
        select(Task)
        .join(Plan)
        .where(Task.id == task_id, Plan.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields if provided
    for key, value in task_update.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task

@api_router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task."""
    result = await db.execute(
        select(Task)
        .join(Plan)
        .where(Task.id == task_id, Plan.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted"}

# AI endpoints

@api_router.post("/ai/analyze-plan", response_model=AIAnalysisResponse)
async def analyze_plan(
    request: AIAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze plan and generate AI-powered task organization."""
    try:
        # Verify plan ownership
        plan_result = await db.execute(
            select(Plan)
            .where(Plan.id == request.plan_id, Plan.user_id == current_user.id)
        )
        plan = plan_result.scalar_one_or_none()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        # Get user context
        user_context = await ai_service.analyze_user_context(current_user.id)

        # Perform analysis based on type
        if request.analysis_type == "dashboard":
            # Generate complete dashboard suggestion
            suggestion = await ai_service.generate_dashboard_suggestion(
                str(request.plan_id), user_context
            )

            # Record interaction
            interaction = await ai_service.record_ai_interaction(
                user_id=current_user.id,
                plan_id=str(request.plan_id),
                interaction_type="dashboard",
                request_data=request.dict(),
                response_data=suggestion,
                response_time_ms=suggestion.get("metadata", {}).get("response_time_ms", 0)
            )

            return AIAnalysisResponse(
                success=True,
                data=suggestion,
                interaction_id=interaction.id
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported analysis type: {request.analysis_type}"
            )

    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        return AIAnalysisResponse(
            success=False,
            error=str(e)
        )


@api_router.post("/ai/suggest-categories", response_model=AIAnalysisResponse)
async def suggest_categories(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Suggest task categories based on content analysis."""
    try:
        # Verify plan ownership and get tasks
        plan_result = await db.execute(
            select(Plan)
            .where(Plan.id == plan_id, Plan.user_id == current_user.id)
        )
        plan = plan_result.scalar_one_or_none()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        tasks_result = await db.execute(
            select(Task).where(Task.plan_id == plan_id)
        )
        tasks = tasks_result.scalars().all()

        if not tasks:
            return AIAnalysisResponse(
                success=False,
                error="No tasks found for categorization"
            )

        # Get user context
        user_context = await ai_service.analyze_user_context(current_user.id)

        # Convert tasks to dict format
        task_dicts = []
        for task in tasks:
            task_dicts.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status
            })

        # Categorize tasks
        categorization_result = await ai_service.categorize_tasks(task_dicts, user_context)

        # Record interaction
        interaction = await ai_service.record_ai_interaction(
            user_id=current_user.id,
            plan_id=str(plan_id),
            interaction_type="categorization",
            request_data={"plan_id": str(plan_id)},
            response_data=categorization_result
        )

        return AIAnalysisResponse(
            success=True,
            data=categorization_result,
            interaction_id=interaction.id
        )

    except Exception as e:
        logger.error(f"Error in categorization: {str(e)}")
        return AIAnalysisResponse(
            success=False,
            error=str(e)
        )


@api_router.post("/ai/rank-priorities", response_model=AIAnalysisResponse)
async def rank_priorities(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """AI-powered task priority ranking with reasoning."""
    try:
        # Verify plan ownership and get tasks
        plan_result = await db.execute(
            select(Plan)
            .where(Plan.id == plan_id, Plan.user_id == current_user.id)
        )
        plan = plan_result.scalar_one_or_none()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        tasks_result = await db.execute(
            select(Task).where(Task.plan_id == plan_id)
        )
        tasks = tasks_result.scalars().all()

        if not tasks:
            return AIAnalysisResponse(
                success=False,
                error="No tasks found for priority ranking"
            )

        # Get user context
        user_context = await ai_service.analyze_user_context(current_user.id)

        # Convert tasks to dict format
        task_dicts = []
        for task in tasks:
            task_dicts.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "ai_category": task.ai_category
            })

        # Score priorities
        priority_result = await ai_service.score_priorities(task_dicts, user_context)

        # Record interaction
        interaction = await ai_service.record_ai_interaction(
            user_id=current_user.id,
            plan_id=str(plan_id),
            interaction_type="ranking",
            request_data={"plan_id": str(plan_id)},
            response_data=priority_result
        )

        return AIAnalysisResponse(
            success=True,
            data=priority_result,
            interaction_id=interaction.id
        )

    except Exception as e:
        logger.error(f"Error in priority ranking: {str(e)}")
        return AIAnalysisResponse(
            success=False,
            error=str(e)
        )


@api_router.post("/ai/generate-dashboard", response_model=AIAnalysisResponse)
async def generate_dashboard(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate complete organized dashboard for user approval."""
    try:
        # Verify plan ownership
        plan_result = await db.execute(
            select(Plan)
            .where(Plan.id == plan_id, Plan.user_id == current_user.id)
        )
        plan = plan_result.scalar_one_or_none()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        # Get user context
        user_context = await ai_service.analyze_user_context(current_user.id)

        # Generate dashboard suggestion
        suggestion = await ai_service.generate_dashboard_suggestion(str(plan_id), user_context)

        # Record interaction
        interaction = await ai_service.record_ai_interaction(
            user_id=current_user.id,
            plan_id=str(plan_id),
            interaction_type="dashboard",
            request_data={"plan_id": str(plan_id)},
            response_data=suggestion,
            response_time_ms=suggestion.get("metadata", {}).get("response_time_ms", 0)
        )

        return AIAnalysisResponse(
            success=True,
            data=suggestion,
            interaction_id=interaction.id
        )

    except Exception as e:
        logger.error(f"Error generating dashboard: {str(e)}")
        return AIAnalysisResponse(
            success=False,
            error=str(e)
        )


@api_router.post("/ai/approve-dashboard", response_model=dict)
async def approve_dashboard(
    request: UserApprovalResponse,
    interaction_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Process user approval and apply AI suggestions."""
    try:
        # Get the AI interaction
        interaction_result = await db.execute(
            select(AIInteraction)
            .where(
                AIInteraction.id == interaction_id,
                AIInteraction.user_id == current_user.id
            )
        )
        interaction = interaction_result.scalar_one_or_none()

        if not interaction:
            raise HTTPException(status_code=404, detail="AI interaction not found")

        if request.approved:
            # Apply AI suggestions to plan and tasks
            response_data = json.loads(interaction.response_data)
            dashboard_data = response_data.get("dashboard_data", {})

            # Update plan with AI-generated data
            plan_result = await db.execute(
                select(Plan)
                .where(Plan.id == interaction.plan_id, Plan.user_id == current_user.id)
            )
            plan = plan_result.scalar_one_or_none()

            if plan:
                plan.ai_generated_data = json.dumps(dashboard_data)
                plan.status = "active"  # Activate the plan with AI suggestions

                # Update tasks with AI categorization and priority
                priority_analysis = response_data.get("priority_analysis", {})
                scored_tasks = priority_analysis.get("scored_tasks", [])

                for task_data in scored_tasks:
                    task_id = task_data.get("id")
                    if task_id:
                        task_result = await db.execute(
                            select(Task)
                            .where(Task.id == task_id, Task.plan_id == plan.id)
                        )
                        task = task_result.scalar_one_or_none()

                        if task:
                            task.ai_category = task_data.get("ai_category")
                            task.ai_priority_score = task_data.get("ai_priority_score")
                            task.ai_reasoning = task_data.get("ai_reasoning")

            # Update interaction with user feedback
            interaction.user_feedback = 5 if request.approved else 2
            if request.feedback:
                # Add feedback to interaction data
                current_response = json.loads(interaction.response_data or "{}")
                current_response["user_feedback"] = request.feedback
                interaction.response_data = json.dumps(current_response)

        await db.commit()

        return {
            "success": True,
            "message": "Dashboard approval processed successfully",
            "approved": request.approved,
            "plan_id": interaction.plan_id
        }

    except Exception as e:
        logger.error(f"Error processing approval: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/ai/interaction-history")
async def get_interaction_history(
    plan_id: Optional[UUID] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI interaction history for user or specific plan."""
    query = select(AIInteraction).where(AIInteraction.user_id == current_user.id)

    if plan_id:
        query = query.where(AIInteraction.plan_id == str(plan_id))

    query = query.order_by(AIInteraction.created_at.desc()).limit(limit)

    result = await db.execute(query)
    interactions = result.scalars().all()

    # Convert to dict for JSON response
    return [
        {
            "id": interaction.id,
            "user_id": interaction.user_id,
            "plan_id": interaction.plan_id,
            "interaction_type": interaction.interaction_type,
            "tokens_used": interaction.tokens_used,
            "cost_estimate": interaction.cost_estimate,
            "model_used": interaction.model_used,
            "response_time_ms": interaction.response_time_ms,
            "user_feedback": interaction.user_feedback,
            "created_at": interaction.created_at
        }
        for interaction in interactions
    ]


@api_router.post("/ai/interaction/{interaction_id}/feedback")
async def provide_feedback(
    interaction_id: str,
    feedback: int = Query(..., ge=1, le=5),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Provide feedback on AI interaction."""
    interaction_result = await db.execute(
        select(AIInteraction)
        .where(
            AIInteraction.id == interaction_id,
            AIInteraction.user_id == current_user.id
        )
    )
    interaction = interaction_result.scalar_one_or_none()

    if not interaction:
        raise HTTPException(status_code=404, detail="AI interaction not found")

    interaction.user_feedback = feedback
    await db.commit()

    return {"message": "Feedback recorded successfully"}


@api_router.post("/ai/organize-prompt")
async def organize_messy_prompt(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Convert messy user prompt into organized categories with todo/doing/upcoming blocks."""
    prompt = request.get("prompt", "")

    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    try:
        # Get user context for personalization
        user_context = await ai_service.analyze_user_context(str(current_user.id))

        # Organize the prompt into categories
        result = await ai_service.organize_into_categories(prompt, user_context)

        # Record the AI interaction
        await ai_service.record_ai_interaction(
            user_id=str(current_user.id),
            plan_id=str(current_user.id),  # Using user_id as placeholder since no plan exists yet
            interaction_type="categorization",
            request_data={"prompt": prompt},
            response_data=result,
            tokens_used=0,  # Gemini doesn't provide token count
            response_time_ms=0
        )

        return result

    except Exception as e:
        logger.error(f"Error organizing prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to organize prompt: {str(e)}")