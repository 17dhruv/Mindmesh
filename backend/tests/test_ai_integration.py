"""Integration tests for AI endpoints."""

import json
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.database import User, Plan, Task, AIInteraction


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    return User(
        id=str(uuid4()),
        email="test@example.com",
        full_name="Test User"
    )


@pytest.fixture
def mock_plan(mock_user):
    """Create a mock plan for testing."""
    return Plan(
        id=str(uuid4()),
        user_id=mock_user.id,
        title="Test Plan",
        description="A test plan for AI analysis"
    )


@pytest.fixture
def mock_tasks(mock_plan):
    """Create mock tasks for testing."""
    return [
        Task(
            id=str(uuid4()),
            plan_id=mock_plan.id,
            title="Develop API",
            description="Create REST API endpoints",
            priority=5,
            status="pending"
        ),
        Task(
            id=str(uuid4()),
            plan_id=mock_plan.id,
            title="Write Tests",
            description="Create unit and integration tests",
            priority=4,
            status="pending"
        )
    ]


class TestAIEndpointsIntegration:
    """Integration tests for AI endpoints."""

    @pytest.mark.asyncio
    async def test_analyze_plan_success(self, client, mock_user, mock_plan):
        """Test successful plan analysis."""
        # Mock authentication
        with patch('app.auth.get_current_user', return_value=mock_user):
            # Mock database queries
            with patch('app.api.select') as mock_select:
                # Mock plan query
                mock_plan_result = AsyncMock()
                mock_plan_result.scalar_one_or_none.return_value = mock_plan
                # Mock AI interaction query
                mock_interaction_result = AsyncMock()
                mock_interaction = MagicMock()
                mock_interaction.id = str(uuid4())
                mock_interaction_result.scalar_one_or_none.return_value = mock_interaction

                def mock_execute_query(*args, **kwargs):
                    if "plans WHERE" in str(args[0]):
                        return mock_plan_result
                    return mock_interaction_result

                mock_select.return_value.where.return_value = mock_plan_result

                # Mock AI service
                mock_context = {"task_categories": [], "priority_distribution": {}}
                mock_suggestion = {
                    "plan_id": mock_plan.id,
                    "plan_title": mock_plan.title,
                    "dashboard_data": {
                        "dashboard_title": "AI Generated Dashboard",
                        "summary": "Test plan analysis",
                        "categories": [],
                        "priority_groups": {},
                        "recommendations": ["Test recommendation"],
                        "estimated_completion_time": "1 week",
                        "next_steps": ["Start with API development"]
                    },
                    "metadata": {"response_time_ms": 1500}
                }

                with patch('app.api.ai_service') as mock_ai_service:
                    mock_ai_service.analyze_user_context.return_value = mock_context
                    mock_ai_service.generate_dashboard_suggestion.return_value = mock_suggestion
                    mock_ai_service.record_ai_interaction.return_value = mock_interaction

                    response = await client.post(
                        "/api/ai/analyze-plan",
                        json={
                            "plan_id": mock_plan.id,
                            "analysis_type": "dashboard"
                        }
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "data" in data
                    assert "interaction_id" in data
                    assert data["data"]["plan_id"] == mock_plan.id

    @pytest.mark.asyncio
    async def test_analyze_plan_not_found(self, client, mock_user):
        """Test plan analysis with non-existent plan."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_result = AsyncMock()
                mock_result.scalar_one_or_none.return_value = None
                mock_select.return_value.where.return_value = mock_result

                response = await client.post(
                    "/api/ai/analyze-plan",
                    json={
                        "plan_id": str(uuid4()),
                        "analysis_type": "dashboard"
                    }
                )

                assert response.status_code == 404
                assert "Plan not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_suggest_categories_success(self, client, mock_user, mock_plan, mock_tasks):
        """Test successful category suggestions."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                # Mock plan query
                mock_plan_result = AsyncMock()
                mock_plan_result.scalar_one_or_none.return_value = mock_plan

                # Mock tasks query
                mock_tasks_result = AsyncMock()
                mock_tasks_result.scalars.return_value.all.return_value = mock_tasks

                # Mock interaction query
                mock_interaction_result = AsyncMock()
                mock_interaction = MagicMock()
                mock_interaction.id = str(uuid4())
                mock_interaction_result.scalar_one_or_none.return_value = mock_interaction

                def mock_execute_query(*args, **kwargs):
                    if "plans WHERE" in str(args[0]):
                        return mock_plan_result
                    elif "tasks WHERE" in str(args[0]):
                        return mock_tasks_result
                    return mock_interaction_result

                mock_select.return_value.where.side_effect = lambda condition: mock_execute_query()

                # Mock AI service
                mock_context = {"task_categories": ["Development", "Testing"]}
                mock_categorization = {
                    "categorized_tasks": mock_tasks,
                    "categories": [
                        {
                            "name": "Development",
                            "description": "Development tasks",
                            "tasks": [0, 1],
                            "priority_ranking": 5
                        }
                    ],
                    "reasoning": "Tasks categorized based on development nature"
                }

                with patch('app.api.ai_service') as mock_ai_service:
                    mock_ai_service.analyze_user_context.return_value = mock_context
                    mock_ai_service.categorize_tasks.return_value = mock_categorization
                    mock_ai_service.record_ai_interaction.return_value = mock_interaction

                    response = await client.post(
                        f"/api/ai/suggest-categories?plan_id={mock_plan.id}"
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "data" in data
                    assert "interaction_id" in data
                    assert len(data["data"]["categories"]) == 1

    @pytest.mark.asyncio
    async def test_suggest_categories_no_tasks(self, client, mock_user, mock_plan):
        """Test category suggestions with no tasks."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                # Mock plan query
                mock_plan_result = AsyncMock()
                mock_plan_result.scalar_one_or_none.return_value = mock_plan

                # Mock empty tasks query
                mock_tasks_result = AsyncMock()
                mock_tasks_result.scalars.return_value.all.return_value = []

                def mock_execute_query(*args, **kwargs):
                    if "plans WHERE" in str(args[0]):
                        return mock_plan_result
                    return mock_tasks_result

                mock_select.return_value.where.side_effect = lambda condition: mock_execute_query()

                response = await client.post(
                    f"/api/ai/suggest-categories?plan_id={mock_plan.id}"
                )

                assert response.status_code == 200
                data = response.json()
                assert data["success"] is False
                assert "No tasks found" in data["error"]

    @pytest.mark.asyncio
    async def test_rank_priorities_success(self, client, mock_user, mock_plan, mock_tasks):
        """Test successful priority ranking."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                # Mock plan and tasks queries similar to categorization test
                mock_plan_result = AsyncMock()
                mock_plan_result.scalar_one_or_none.return_value = mock_plan

                mock_tasks_result = AsyncMock()
                mock_tasks_result.scalars.return_value.all.return_value = mock_tasks

                mock_interaction_result = AsyncMock()
                mock_interaction = MagicMock()
                mock_interaction.id = str(uuid4())
                mock_interaction_result.scalar_one_or_none.return_value = mock_interaction

                mock_select.return_value.where.side_effect = lambda condition: mock_plan_result

                # Mock AI service
                mock_context = {"priority_distribution": {"high": 1, "medium": 1}}
                mock_priority_result = {
                    "scored_tasks": [
                        {
                            "id": mock_tasks[0].id,
                            "ai_priority_score": 9,
                            "ai_reasoning": "Critical for project success",
                            "estimated_effort": "High"
                        },
                        {
                            "id": mock_tasks[1].id,
                            "ai_priority_score": 7,
                            "ai_reasoning": "Important for quality",
                            "estimated_effort": "Medium"
                        }
                    ],
                    "recommendations": ["Focus on high-priority tasks first"]
                }

                with patch('app.api.ai_service') as mock_ai_service:
                    mock_ai_service.analyze_user_context.return_value = mock_context
                    mock_ai_service.score_priorities.return_value = mock_priority_result
                    mock_ai_service.record_ai_interaction.return_value = mock_interaction

                    response = await client.post(
                        f"/api/ai/rank-priorities?plan_id={mock_plan.id}"
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "data" in data
                    assert len(data["data"]["scored_tasks"]) == 2
                    assert data["data"]["scored_tasks"][0]["ai_priority_score"] == 9

    @pytest.mark.asyncio
    async def test_generate_dashboard_success(self, client, mock_user, mock_plan):
        """Test successful dashboard generation."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_plan_result = AsyncMock()
                mock_plan_result.scalar_one_or_none.return_value = mock_plan

                mock_interaction_result = AsyncMock()
                mock_interaction = MagicMock()
                mock_interaction.id = str(uuid4())
                mock_interaction_result.scalar_one_or_none.return_value = mock_interaction

                mock_select.return_value.where.return_value = mock_plan_result

                # Mock AI service
                mock_context = {"task_categories": [], "priority_distribution": {}}
                mock_suggestion = {
                    "plan_id": mock_plan.id,
                    "plan_title": mock_plan.title,
                    "dashboard_data": {
                        "dashboard_title": "Test Dashboard",
                        "summary": "AI-generated dashboard",
                        "categories": [],
                        "priority_groups": {"high": [], "medium": [], "low": []},
                        "recommendations": ["Complete tasks in priority order"],
                        "estimated_completion_time": "2 weeks",
                        "next_steps": ["Start with high-priority tasks"]
                    },
                    "metadata": {"response_time_ms": 2000}
                }

                with patch('app.api.ai_service') as mock_ai_service:
                    mock_ai_service.analyze_user_context.return_value = mock_context
                    mock_ai_service.generate_dashboard_suggestion.return_value = mock_suggestion
                    mock_ai_service.record_ai_interaction.return_value = mock_interaction

                    response = await client.post(
                        f"/api/ai/generate-dashboard?plan_id={mock_plan.id}"
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "data" in data
                    assert data["data"]["dashboard_data"]["dashboard_title"] == "Test Dashboard"

    @pytest.mark.asyncio
    async def test_approve_dashboard_success(self, client, mock_user):
        """Test successful dashboard approval."""
        interaction_id = str(uuid4())
        plan_id = str(uuid4())

        mock_interaction = AIInteraction(
            id=interaction_id,
            user_id=mock_user.id,
            plan_id=plan_id,
            interaction_type="dashboard",
            response_data=json.dumps({
                "dashboard_data": {"title": "Test Dashboard"},
                "priority_analysis": {
                    "scored_tasks": [
                        {
                            "id": str(uuid4()),
                            "ai_category": "Development",
                            "ai_priority_score": 9,
                            "ai_reasoning": "Critical task"
                        }
                    ]
                }
            })
        )

        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_interaction_result = AsyncMock()
                mock_interaction_result.scalar_one_or_none.return_value = mock_interaction

                mock_plan_result = AsyncMock()
                mock_plan = MagicMock()
                mock_plan_result.scalar_one_or_none.return_value = mock_plan

                mock_task_result = AsyncMock()
                mock_task = MagicMock()
                mock_task_result.scalar_one_or_none.return_value = mock_task

                def mock_execute_query(*args, **kwargs):
                    if "ai_interactions" in str(args[0]):
                        return mock_interaction_result
                    elif "plans" in str(args[0]):
                        return mock_plan_result
                    elif "tasks" in str(args[0]):
                        return mock_task_result
                    return AsyncMock()

                mock_select.return_value.where.side_effect = lambda condition: mock_execute_query()

                with patch('app.api.async_session') as mock_session:
                    mock_session_instance = AsyncMock()
                    mock_session.return_value.__aenter__.return_value = mock_session_instance

                    response = await client.post(
                        f"/api/ai/approve-dashboard?interaction_id={interaction_id}",
                        json={
                            "approved": True,
                            "feedback": "Great analysis!"
                        }
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["approved"] is True
                    assert data["plan_id"] == plan_id

    @pytest.mark.asyncio
    async def test_approve_dashboard_not_found(self, client, mock_user):
        """Test dashboard approval with non-existent interaction."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_result = AsyncMock()
                mock_result.scalar_one_or_none.return_value = None
                mock_select.return_value.where.return_value = mock_result

                response = await client.post(
                    f"/api/ai/approve-dashboard?interaction_id={str(uuid4())}",
                    json={"approved": False}
                )

                assert response.status_code == 404
                assert "AI interaction not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_interaction_history(self, client, mock_user):
        """Test getting AI interaction history."""
        interactions = [
            AIInteraction(
                id=str(uuid4()),
                user_id=mock_user.id,
                plan_id=str(uuid4()),
                interaction_type="dashboard",
                tokens_used=100,
                cost_estimate=0.05
            ),
            AIInteraction(
                id=str(uuid4()),
                user_id=mock_user.id,
                plan_id=str(uuid4()),
                interaction_type="categorization",
                tokens_used=50,
                cost_estimate=0.025
            )
        ]

        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_result = AsyncMock()
                mock_result.scalars.return_value.all.return_value = interactions
                mock_select.return_value.where.return_value.order_by.return_value.limit.return_value = mock_result

                response = await client.get("/api/ai/interaction-history")

                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2
                assert data[0]["interaction_type"] == "dashboard"
                assert data[1]["interaction_type"] == "categorization"

    @pytest.mark.asyncio
    async def test_provide_feedback(self, client, mock_user):
        """Test providing feedback on AI interaction."""
        interaction_id = str(uuid4())
        mock_interaction = AIInteraction(
            id=interaction_id,
            user_id=mock_user.id,
            plan_id=str(uuid4()),
            interaction_type="dashboard"
        )

        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_result = AsyncMock()
                mock_result.scalar_one_or_none.return_value = mock_interaction
                mock_select.return_value.where.return_value = mock_result

                with patch('app.api.async_session') as mock_session:
                    mock_session_instance = AsyncMock()
                    mock_session.return_value.__aenter__.return_value = mock_session_instance

                    response = await client.post(
                        f"/api/ai/interaction/{interaction_id}/feedback?feedback=5"
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert "Feedback recorded successfully" in data["message"]

    @pytest.mark.asyncio
    async def test_provide_feedback_not_found(self, client, mock_user):
        """Test providing feedback on non-existent interaction."""
        with patch('app.auth.get_current_user', return_value=mock_user):
            with patch('app.api.select') as mock_select:
                mock_result = AsyncMock()
                mock_result.scalar_one_or_none.return_value = None
                mock_select.return_value.where.return_value = mock_result

                response = await client.post(
                    f"/api/ai/interaction/{str(uuid4())}/feedback?feedback=3"
                )

                assert response.status_code == 404
                assert "AI interaction not found" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__])