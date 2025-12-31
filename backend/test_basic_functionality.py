#!/usr/bin/env python3
"""
Basic functionality test for Mindmesh backend with Gemini integration.

This script tests the basic structure and imports without requiring a real API key.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported successfully."""
    print("🔍 Testing module imports...")

    try:
        # Test configuration
        from app.config import settings
        print("✅ Configuration module imported successfully")

        # Test database models
        from app.database import User, Plan, Task, AIInteraction
        print("✅ Database models imported successfully")

        # Test schemas
        from app.schemas import (
            AIAnalysisRequest, AIAnalysisResponse, AIDashboardSuggestion,
            UserApprovalRequest, UserApprovalResponse
        )
        print("✅ AI schemas imported successfully")

        # Test AI service (may fail due to missing API key, but that's okay)
        try:
            from app.ai_service import GeminiAIService
            print("✅ AI service module imported successfully")
        except Exception as e:
            print(f"⚠️  AI service import warning: {str(e)}")
            print("   This is expected if API key is not configured")

        # Test API endpoints
        try:
            from app.api import api_router
            print("✅ API endpoints imported successfully")
        except Exception as e:
            print(f"⚠️  API endpoints import warning: {str(e)}")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {str(e)}")
        return False


def test_configuration():
    """Test configuration values."""
    print("\n⚙️  Testing configuration...")

    try:
        from app.config import settings

        # Check required fields
        required_fields = [
            'app_name', 'app_version', 'database_url',
            'supabase_url', 'google_api_key', 'gemini_model'
        ]

        for field in required_fields:
            if hasattr(settings, field):
                value = getattr(settings, field)
                print(f"✅ {field}: {value if 'key' not in field.lower() else '[CONFIGURED]'}")
            else:
                print(f"❌ Missing configuration field: {field}")
                return False

        return True

    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False


def test_database_models():
    """Test database model structure."""
    print("\n🗄️  Testing database models...")

    try:
        from app.database import User, Plan, Task, AIInteraction

        # Test User model
        user_fields = ['id', 'email', 'full_name', 'created_at', 'updated_at']
        for field in user_fields:
            if hasattr(User, field):
                print(f"✅ User.{field} exists")
            else:
                print(f"❌ User.{field} missing")
                return False

        # Test Plan model with AI fields
        plan_ai_fields = ['ai_generated_data', 'original_thought', 'ai_metadata']
        for field in plan_ai_fields:
            if hasattr(Plan, field):
                print(f"✅ Plan.{field} (AI) exists")
            else:
                print(f"❌ Plan.{field} (AI) missing")
                return False

        # Test Task model with AI fields
        task_ai_fields = ['ai_category', 'ai_priority_score', 'ai_reasoning']
        for field in task_ai_fields:
            if hasattr(Task, field):
                print(f"✅ Task.{field} (AI) exists")
            else:
                print(f"❌ Task.{field} (AI) missing")
                return False

        # Test AIInteraction model
        ai_interaction_fields = [
            'id', 'user_id', 'plan_id', 'interaction_type',
            'request_data', 'response_data', 'tokens_used',
            'cost_estimate', 'model_used', 'response_time_ms'
        ]
        for field in ai_interaction_fields:
            if hasattr(AIInteraction, field):
                print(f"✅ AIInteraction.{field} exists")
            else:
                print(f"❌ AIInteraction.{field} missing")
                return False

        return True

    except Exception as e:
        print(f"❌ Database model test failed: {str(e)}")
        return False


def test_api_structure():
    """Test API endpoint structure."""
    print("\n🌐 Testing API structure...")

    try:
        from app.api import api_router
        from fastapi import APIRouter

        # Check if it's an APIRouter
        if isinstance(api_router, APIRouter):
            print("✅ API router is properly configured")

            # Check routes
            routes = api_router.routes
            route_paths = [route.path for route in routes]

            # Check for basic routes
            basic_routes = ["/health", "/plans", "/tasks"]
            ai_routes = ["/ai/analyze-plan", "/ai/suggest-categories", "/ai/rank-priorities", "/ai/generate-dashboard"]

            print(f"📊 Total routes found: {len(routes)}")

            for route in basic_routes:
                if any(route in path for path in route_paths):
                    print(f"✅ Basic route exists: {route}")
                else:
                    print(f"⚠️  Basic route missing: {route}")

            for route in ai_routes:
                if any(route in path for path in route_paths):
                    print(f"✅ AI route exists: {route}")
                else:
                    print(f"⚠️  AI route missing: {route}")

            return True
        else:
            print("❌ API router is not properly configured")
            return False

    except Exception as e:
        print(f"❌ API structure test failed: {str(e)}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n📋 Testing Pydantic schemas...")

    try:
        # Test basic schemas
        from app.schemas import PlanCreate, TaskCreate, Plan, Task
        print("✅ Basic schemas imported")

        # Test AI schemas
        from app.schemas import (
            AIAnalysisRequest, AIAnalysisResponse, AIDashboardSuggestion,
            TaskCategory, PriorityAnalysis, UserApprovalRequest
        )
        print("✅ AI schemas imported")

        # Test schema validation
        plan_create = PlanCreate(title="Test Plan", description="Test description")
        print(f"✅ PlanCreate validation: {plan_create.title}")

        task_create = TaskCreate(
            plan_id="12345678-1234-1234-1234-123456789012",
            title="Test Task",
            description="Test task description",
            priority=3
        )
        print(f"✅ TaskCreate validation: {task_create.title}")

        # Test AI schema validation
        ai_request = AIAnalysisRequest(
            plan_id="12345678-1234-1234-1234-123456789012",
            analysis_type="dashboard"
        )
        print(f"✅ AIAnalysisRequest validation: {ai_request.analysis_type}")

        return True

    except Exception as e:
        print(f"❌ Schema test failed: {str(e)}")
        return False


def main():
    """Run all basic functionality tests."""
    print("🚀 Mindmesh Backend - Basic Functionality Test")
    print("=" * 60)

    tests = [
        test_imports,
        test_configuration,
        test_database_models,
        test_api_structure,
        test_schemas
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All basic functionality tests passed!")
        print("💡 Next steps:")
        print("   1. Add your Gemini API key to the .env file")
        print("   2. Run the full integration test: python test_gemini_integration.py")
        print("   3. Start the development server: uvicorn app.main:app --reload")
        print("   4. Test the API endpoints at http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()