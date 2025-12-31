"""Test configuration and fixtures."""

import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

# Set test environment variables
os.environ["TESTING"] = "true"
os.environ["GOOGLE_API_KEY"] = "test-key"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_ANON_KEY"] = "test-anon-key"
os.environ["SUPABASE_SERVICE_KEY"] = "test-service-key"
os.environ["SUPABASE_JWT_SECRET"] = "test-jwt-secret"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_db_session():
    """Create a mock database session."""
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.execute = AsyncMock()
    session.scalar = AsyncMock()
    session.scalar_one_or_none = AsyncMock()
    session.scalars = AsyncMock()
    session.fetchall = AsyncMock()
    return session


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini AI response for testing."""
    return {
        "categories": [
            {
                "name": "Development",
                "description": "Software development tasks",
                "tasks": [0, 1],
                "priority_ranking": 5
            },
            {
                "name": "Testing",
                "description": "Quality assurance tasks",
                "tasks": [2],
                "priority_ranking": 4
            }
        ],
        "reasoning": "Tasks categorized based on their development lifecycle phase"
    }


@pytest.fixture
def mock_priority_response():
    """Mock priority analysis response for testing."""
    return {
        "ranked_tasks": [
            {
                "task_index": 0,
                "ai_priority_score": 9,
                "reasoning": "Critical infrastructure component",
                "estimated_effort": "High",
                "dependencies": [],
                "impact_level": "High"
            },
            {
                "task_index": 1,
                "ai_priority_score": 7,
                "reasoning": "Important for user experience",
                "estimated_effort": "Medium",
                "dependencies": [0],
                "impact_level": "Medium"
            },
            {
                "task_index": 2,
                "ai_priority_score": 6,
                "reasoning": "Quality assurance task",
                "estimated_effort": "Low",
                "dependencies": [0, 1],
                "impact_level": "Medium"
            }
        ],
        "recommendations": [
            "Focus on core development first",
            "Ensure thorough testing before deployment"
        ]
    }


@pytest.fixture
def mock_dashboard_response():
    """Mock dashboard generation response for testing."""
    return {
        "dashboard_title": "AI Generated Development Dashboard",
        "summary": "Comprehensive plan with 3 development tasks",
        "categories": [
            {
                "name": "Backend Development",
                "description": "Server-side development tasks",
                "tasks": [0, 1],
                "priority_ranking": 5
            },
            {
                "name": "Quality Assurance",
                "description": "Testing and validation tasks",
                "tasks": [2],
                "priority_ranking": 4
            }
        ],
        "priority_groups": {
            "critical": ["task-1"],
            "high": ["task-2"],
            "medium": ["task-3"],
            "low": []
        },
        "recommendations": [
            "Start with backend API development",
            "Implement comprehensive testing",
            "Monitor performance metrics"
        ],
        "estimated_completion_time": "3-4 weeks",
        "next_steps": [
            "Set up development environment",
            "Create API endpoints",
            "Write unit tests",
            "Deploy to staging"
        ]
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": str(uuid4()),
        "email": "test@example.com",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_plan_data(sample_user_data):
    """Sample plan data for testing."""
    return {
        "id": str(uuid4()),
        "user_id": sample_user_data["id"],
        "title": "Test Development Plan",
        "description": "A comprehensive plan for developing a new feature",
        "status": "draft"
    }


@pytest.fixture
def sample_tasks_data(sample_plan_data):
    """Sample tasks data for testing."""
    return [
        {
            "id": str(uuid4()),
            "plan_id": sample_plan_data["id"],
            "title": "Design Database Schema",
            "description": "Create efficient database structure",
            "priority": 5,
            "status": "pending"
        },
        {
            "id": str(uuid4()),
            "plan_id": sample_plan_data["id"],
            "title": "Implement API Endpoints",
            "description": "Build RESTful API for the application",
            "priority": 4,
            "status": "pending"
        },
        {
            "id": str(uuid4()),
            "plan_id": sample_plan_data["id"],
            "title": "Write Unit Tests",
            "description": "Create comprehensive test suite",
            "priority": 3,
            "status": "pending"
        },
        {
            "id": str(uuid4()),
            "plan_id": sample_plan_data["id"],
            "title": "Deploy to Production",
            "description": "Deploy application to production server",
            "priority": 2,
            "status": "pending"
        }
    ]


@pytest.fixture
def mock_ai_interaction_data(sample_user_data, sample_plan_data):
    """Sample AI interaction data for testing."""
    return {
        "id": str(uuid4()),
        "user_id": sample_user_data["id"],
        "plan_id": sample_plan_data["id"],
        "interaction_type": "dashboard",
        "request_data": {"plan_id": sample_plan_data["id"]},
        "response_data": {"success": True, "data": "mock response"},
        "tokens_used": 150,
        "cost_estimate": 0.075,
        "model_used": "gemini-1.5-pro",
        "response_time_ms": 1200,
        "user_feedback": 5
    }


# Mock patches for commonly used dependencies

@pytest.fixture
def mock_settings():
    """Mock application settings."""
    with pytest.MonkeyPatch().context() as m:
        m.setenv("GOOGLE_API_KEY", "test-api-key")
        m.setenv("GEMINI_MODEL", "gemini-1.5-pro-test")
        m.setenv("GEMINI_TEMPERATURE", "0.1")
        m.setenv("GEMINI_MAX_TOKENS", "1024")
        yield


@pytest.fixture
def mock_google_generativeai():
    """Mock Google Generative AI library."""
    with pytest.MonkeyPatch().context() as m:
        # Mock the generativeai module
        mock_genai = MagicMock()
        m.setattr("google.generativeai", mock_genai)

        # Mock the GenerativeModel class
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model

        # Mock the configure function
        mock_genai.configure = MagicMock()

        yield mock_genai, mock_model


@pytest.fixture
def mock_tenacity():
    """Mock tenacity retry library."""
    with pytest.MonkeyPatch().context() as m:
        mock_retry = MagicMock()
        m.setattr("tenacity.retry", mock_retry)
        m.setattr("tenacity.stop_after_attempt", MagicMock())
        m.setattr("tenacity.wait_exponential", MagicMock())
        yield mock_retry


# Database test fixtures

@pytest.fixture
async def test_database():
    """Create test database tables."""
    # This would typically create test tables
    # For now, we'll use mocks
    yield
    # Cleanup would go here


@pytest.fixture
def mock_sqlalchemy():
    """Mock SQLAlchemy components."""
    with pytest.MonkeyPatch().context() as m:
        # Mock SQLAlchemy components
        mock_select = MagicMock()
        mock_async_session = MagicMock()
        mock_create_engine = MagicMock()

        m.setattr("sqlalchemy.select", mock_select)
        m.setattr("sqlalchemy.ext.asyncio.async_sessionmaker", mock_async_session)
        m.setattr("sqlalchemy.ext.asyncio.create_async_engine", mock_create_engine)

        yield mock_select, mock_async_session, mock_create_engine


# Authentication test fixtures

@pytest.fixture
def mock_auth():
    """Mock authentication dependencies."""
    with pytest.MonkeyPatch().context() as m:
        # Mock get_current_user function
        mock_user = MagicMock()
        mock_user.id = str(uuid4())
        mock_user.email = "test@example.com"

        mock_get_current_user = MagicMock(return_value=mock_user)
        m.setattr("app.auth.get_current_user", mock_get_current_user)

        yield mock_get_current_user, mock_user


# FastAPI test client fixture

@pytest.fixture
def test_app():
    """Create test FastAPI application."""
    from app.main import app
    return app


# Async HTTP client fixture

@pytest.fixture
async def http_client(test_app):
    """Create async HTTP client for testing."""
    import httpx
    async with httpx.AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


# Utility functions for testing

def assert_valid_uuid(uuid_string: str) -> bool:
    """Check if string is a valid UUID."""
    try:
        uuid_obj = uuid4(uuid_string)
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False


def assert_valid_datetime(datetime_string: str) -> bool:
    """Check if string is a valid datetime format."""
    try:
        from datetime import datetime
        datetime.fromisoformat(datetime_string.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        return False


# Test data generators

def generate_test_tasks(count: int = 3) -> list:
    """Generate test tasks with varying priorities."""
    tasks = []
    for i in range(count):
        tasks.append({
            "id": str(uuid4()),
            "title": f"Test Task {i+1}",
            "description": f"Description for test task {i+1}",
            "priority": (i % 5) + 1,  # Priorities 1-5
            "status": "pending"
        })
    return tasks


def generate_test_categories(count: int = 3) -> list:
    """Generate test categories."""
    categories = []
    category_names = ["Development", "Testing", "Documentation", "Deployment", "Research"]

    for i in range(min(count, len(category_names))):
        categories.append({
            "name": category_names[i],
            "description": f"Tasks related to {category_names[i].lower()}",
            "tasks": [j for j in range(i*2, (i+1)*2)],  # Assign some task indices
            "priority_ranking": (i % 5) + 1
        })
    return categories


# Error simulation fixtures

@pytest.fixture
def simulate_api_error():
    """Context manager to simulate API errors."""
    class SimulateError:
        def __init__(self, exception_type=Exception, message="API Error"):
            self.exception_type = exception_type
            self.message = message

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            raise self.exception_type(self.message)

    return SimulateError


# Performance testing fixtures

@pytest.fixture
def performance_thresholds():
    """Performance thresholds for testing."""
    return {
        "max_response_time_ms": 5000,  # 5 seconds
        "min_categorization_accuracy": 0.8,  # 80%
        "max_token_usage": 2000,
        "max_cost_per_request": 0.10  # $0.10
    }


# Logging test fixtures

@pytest.fixture
def capture_logs():
    """Fixture to capture log messages during tests."""
    import logging
    from io import StringIO

    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.DEBUG)

    # Add handler to root logger
    logger = logging.getLogger()
    logger.addHandler(handler)

    yield log_capture

    # Cleanup
    logger.removeHandler(handler)


# Markers for different test types

pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.performance = pytest.mark.performance
pytest.mark.security = pytest.mark.security
pytest.mark.ai = pytest.mark.ai


# Test configuration

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security tests"
    )
    config.addinivalue_line(
        "markers", "ai: marks tests as AI-specific tests"
    )


# Test collection hooks

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on file location."""
    for item in items:
        # Add AI marker to tests in ai-related files
        if "ai" in item.nodeid.lower():
            item.add_marker(pytest.mark.ai)

        # Add integration marker to integration tests
        if "integration" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)

        # Add unit marker to unit tests
        if "test_ai_service" in item.nodeid:
            item.add_marker(pytest.mark.unit)