"""Tests for Gemini AI Service."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.ai_service import GeminiAIService
from app.database import User, Plan, Task


@pytest.fixture
def ai_service():
    """Create AI service instance for testing."""
    return GeminiAIService()


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
        ),
        Task(
            id=str(uuid4()),
            plan_id=mock_plan.id,
            title="Deploy Application",
            description="Deploy to production environment",
            priority=3,
            status="pending"
        )
    ]


class TestGeminiAIService:
    """Test suite for GeminiAIService."""

    @pytest.mark.asyncio
    async def test_analyze_user_context_empty(self, ai_service, mock_user):
        """Test analyzing user context with no existing data."""
        with patch('app.ai_service.async_session') as mock_session:
            # Mock empty result
            mock_result = MagicMock()
            mock_result.fetchall.return_value = []
            mock_session.return_value.__aenter__.return_value.execute.return_value = mock_result

            context = await ai_service.analyze_user_context(mock_user.id)

            assert context["total_plans"] == 0
            assert context["plan_data"] == []
            assert context["task_categories"] == []
            assert context["priority_distribution"]["high"] == 0

    @pytest.mark.asyncio
    async def test_analyze_user_context_with_data(self, ai_service, mock_user, mock_plan, mock_tasks):
        """Test analyzing user context with existing data."""
        with patch('app.ai_service.async_session') as mock_session:
            # Mock result with data
            mock_result = MagicMock()
            mock_result.fetchall.return_value = [
                # Plan 1 with tasks
                (mock_plan.title, mock_plan.description, "active", "2024-01-01",
                 mock_tasks[0].title, mock_tasks[0].description, mock_tasks[0].priority, "pending", "Development"),
                (mock_plan.title, mock_plan.description, "active", "2024-01-01",
                 mock_tasks[1].title, mock_tasks[1].description, mock_tasks[1].priority, "pending", "Testing"),
            ]
            mock_session.return_value.__aenter__.return_value.execute.return_value = mock_result

            context = await ai_service.analyze_user_context(mock_user.id)

            assert context["total_plans"] == 1
            assert len(context["plan_data"]) == 1
            assert "Development" in context["task_categories"]
            assert "Testing" in context["task_categories"]
            assert context["priority_distribution"]["high"] == 1

    @pytest.mark.asyncio
    async def test_categorize_tasks_success(self, ai_service, mock_tasks):
        """Test successful task categorization."""
        context = {"task_categories": ["Development", "Testing"]}

        mock_response = json.dumps({
            "categories": [
                {
                    "name": "Development",
                    "description": "Software development tasks",
                    "tasks": [0, 2],  # Task 1 and 3
                    "priority_ranking": 5
                },
                {
                    "name": "Testing",
                    "description": "Testing and QA tasks",
                    "tasks": [1],  # Task 2
                    "priority_ranking": 4
                }
            ],
            "reasoning": "Tasks categorized based on their nature and purpose"
        })

        with patch.object(ai_service, '_generate_content', return_value=mock_response):
            result = await ai_service.categorize_tasks(mock_tasks, context)

            assert "categorized_tasks" in result
            assert "categories" in result
            assert "reasoning" in result
            assert len(result["categories"]) == 2
            assert result["categories"][0]["name"] == "Development"
            assert result["categories"][1]["name"] == "Testing"
            assert len(result["categorized_tasks"]) == 3

    @pytest.mark.asyncio
    async def test_categorize_tasks_api_failure(self, ai_service, mock_tasks):
        """Test task categorization with API failure."""
        context = {"task_categories": []}

        with patch.object(ai_service, '_generate_content', side_effect=Exception("API Error")):
            result = await ai_service.categorize_tasks(mock_tasks, context)

            assert result["categorized_tasks"] == mock_tasks
            assert len(result["categories"]) == 1
            assert result["categories"][0]["name"] == "General"
            assert "AI categorization failed" in result["reasoning"]

    @pytest.mark.asyncio
    async def test_score_priorities_success(self, ai_service, mock_tasks):
        """Test successful priority scoring."""
        context = {"priority_distribution": {"high": 1, "medium": 1, "low": 1}}

        mock_response = json.dumps({
            "ranked_tasks": [
                {
                    "task_index": 0,
                    "ai_priority_score": 9,
                    "reasoning": "Critical for project start",
                    "estimated_effort": "High",
                    "dependencies": [],
                    "impact_level": "High"
                },
                {
                    "task_index": 1,
                    "ai_priority_score": 7,
                    "reasoning": "Important for quality assurance",
                    "estimated_effort": "Medium",
                    "dependencies": [0],
                    "impact_level": "Medium"
                },
                {
                    "task_index": 2,
                    "ai_priority_score": 6,
                    "reasoning": "Final deployment task",
                    "estimated_effort": "Medium",
                    "dependencies": [0, 1],
                    "impact_level": "High"
                }
            ],
            "recommendations": ["Focus on API development first", "Ensure thorough testing"]
        })

        with patch.object(ai_service, '_generate_content', return_value=mock_response):
            result = await ai_service.score_priorities(mock_tasks, context)

            assert "scored_tasks" in result
            assert "recommendations" in result
            assert len(result["scored_tasks"]) == 3
            assert result["scored_tasks"][0]["ai_priority_score"] == 9
            assert result["scored_tasks"][1]["ai_priority_score"] == 7
            assert len(result["recommendations"]) == 2

    @pytest.mark.asyncio
    async def test_score_priorities_api_failure(self, ai_service, mock_tasks):
        """Test priority scoring with API failure."""
        context = {"priority_distribution": {}}

        with patch.object(ai_service, '_generate_content', side_effect=Exception("API Error")):
            result = await ai_service.score_priorities(mock_tasks, context)

            assert len(result["scored_tasks"]) == 3
            assert result["scored_tasks"][0]["ai_priority_score"] == 10  # 5 * 2
            assert result["scored_tasks"][1]["ai_priority_score"] == 8   # 4 * 2
            assert result["scored_tasks"][2]["ai_priority_score"] == 6   # 3 * 2
            assert "Using original priority as fallback" in result["scored_tasks"][0]["ai_reasoning"]

    @pytest.mark.asyncio
    async def test_generate_dashboard_suggestion(self, ai_service, mock_plan, mock_tasks):
        """Test complete dashboard suggestion generation."""
        user_context = {"task_categories": [], "priority_distribution": {}}

        # Mock database calls
        with patch('app.ai_service.async_session') as mock_session:
            # Mock plan result
            mock_plan_result = MagicMock()
            mock_plan_result.fetchone.return_value = mock_plan
            # Mock tasks result
            mock_tasks_result = MagicMock()
            mock_tasks_result.fetchall.return_value = mock_tasks

            def mock_execute(query, params=None):
                if "plans WHERE" in str(query):
                    return mock_plan_result
                elif "tasks WHERE" in str(query):
                    return mock_tasks_result
                return MagicMock()

            mock_session.return_value.__aenter__.return_value.execute.side_effect = mock_execute

            # Mock AI methods
            categorization_result = {
                "categorized_tasks": mock_tasks,
                "categories": [{"name": "Development", "tasks": [0, 1, 2], "priority_ranking": 5}],
                "reasoning": "All tasks are development-related"
            }

            priority_result = {
                "scored_tasks": mock_tasks,
                "recommendations": ["Focus on development tasks"]
            }

            dashboard_response = json.dumps({
                "dashboard_title": "Development Plan Dashboard",
                "summary": "Comprehensive development plan with 3 tasks",
                "categories": categorization_result["categories"],
                "priority_groups": {
                    "high": [mock_tasks[0].id],
                    "medium": [mock_tasks[1].id],
                    "low": [mock_tasks[2].id]
                },
                "recommendations": priority_result["recommendations"],
                "estimated_completion_time": "2-3 weeks",
                "next_steps": ["Start with API development"]
            })

            with patch.object(ai_service, 'categorize_tasks', return_value=categorization_result), \
                 patch.object(ai_service, 'score_priorities', return_value=priority_result), \
                 patch.object(ai_service, '_generate_content', return_value=dashboard_response):

                suggestion = await ai_service.generate_dashboard_suggestion(mock_plan.id, user_context)

                assert suggestion["plan_id"] == mock_plan.id
                assert suggestion["plan_title"] == mock_plan.title
                assert "dashboard_data" in suggestion
                assert "categorization" in suggestion
                assert "priority_analysis" in suggestion
                assert "metadata" in suggestion
                assert suggestion["dashboard_data"]["dashboard_title"] == "Development Plan Dashboard"
                assert len(suggestion["categorization"]["categories"]) == 1

    @pytest.mark.asyncio
    async def test_record_ai_interaction(self, ai_service, mock_user, mock_plan):
        """Test recording AI interactions."""
        request_data = {"test": "request"}
        response_data = {"test": "response"}

        with patch('app.ai_service.async_session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance

            interaction_id = str(uuid4())
            mock_interaction = MagicMock()
            mock_interaction.id = interaction_id
            mock_session_instance.refresh.return_value = None

            # Mock the AIInteraction creation
            with patch('app.ai_service.AIInteraction') as mock_ai_interaction:
                mock_ai_interaction.return_value.id = interaction_id

                interaction = await ai_service.record_ai_interaction(
                    user_id=mock_user.id,
                    plan_id=mock_plan.id,
                    interaction_type="test",
                    request_data=request_data,
                    response_data=response_data,
                    tokens_used=100,
                    response_time_ms=500
                )

                assert interaction.id == interaction_id
                mock_session_instance.add.assert_called_once()
                mock_session_instance.commit.assert_called_once()

    def test_estimate_cost(self, ai_service):
        """Test cost estimation based on token usage."""
        # Test with various token counts
        cost_100_tokens = ai_service._estimate_cost(100)
        cost_1000_tokens = ai_service._estimate_cost(1000)
        cost_0_tokens = ai_service._estimate_cost(0)

        assert cost_1000_tokens > cost_100_tokens
        assert cost_0_tokens == 0.0
        assert cost_100_tokens > 0

    @pytest.mark.asyncio
    async def test_generate_content_retry_success(self, ai_service):
        """Test successful content generation with retry logic."""
        mock_response = MagicMock()
        mock_response.text = "Generated content"

        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_model.return_value.generate_content.return_value = mock_response

            result = await ai_service._generate_content("Test prompt")

            assert result == "Generated content"

    @pytest.mark.asyncio
    async def test_generate_content_retry_failure(self, ai_service):
        """Test content generation failure after retries."""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_model.return_value.generate_content.side_effect = Exception("API Error")

            with pytest.raises(Exception):
                await ai_service._generate_content("Test prompt")


if __name__ == "__main__":
    pytest.main([__file__])