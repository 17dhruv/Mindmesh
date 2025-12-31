#!/usr/bin/env python3
"""
Test script to demonstrate Gemini API integration with Mindmesh.

This script tests the AI service functionality with sample data.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List

# Mock imports for testing without a real database
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service import GeminiAIService
from app.config import settings


class MockDatabase:
    """Mock database for testing."""

    def __init__(self):
        self.users = {}
        self.plans = {}
        self.tasks = {}
        self.interactions = {}

    def get_user_plans(self, user_id: str) -> List[Dict]:
        """Get user's plans with tasks."""
        user_plans = [plan for plan in self.plans.values() if plan["user_id"] == user_id]
        for plan in user_plans:
            plan["tasks"] = [task for task in self.tasks.values() if task["plan_id"] == plan["id"]]
        return user_plans

    def get_plan_by_id(self, plan_id: str) -> Dict:
        """Get plan by ID."""
        return self.plans.get(plan_id)

    def get_plan_tasks(self, plan_id: str) -> List[Dict]:
        """Get tasks for a plan."""
        return [task for task in self.tasks.values() if task["plan_id"] == plan_id]

    def add_interaction(self, interaction: Dict):
        """Add AI interaction."""
        interaction["id"] = str(uuid.uuid4())
        interaction["created_at"] = datetime.utcnow()
        self.interactions[interaction["id"]] = interaction
        return interaction


def create_sample_data() -> tuple:
    """Create sample data for testing."""
    # Create sample user
    user_id = str(uuid.uuid4())

    # Create sample plan
    plan_id = str(uuid.uuid4())
    plan = {
        "id": plan_id,
        "user_id": user_id,
        "title": "E-commerce Platform Development",
        "description": "Build a comprehensive e-commerce platform with user authentication, product catalog, shopping cart, and payment processing",
        "status": "draft",
        "created_at": datetime.utcnow()
    }

    # Create sample tasks
    tasks = [
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Design Database Schema",
            "description": "Create normalized database schema for users, products, orders, and payments. Include proper relationships and indexing strategies.",
            "priority": 5,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Implement User Authentication",
            "description": "Develop secure user registration, login, and session management with JWT tokens. Include password recovery and email verification.",
            "priority": 5,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Build Product Catalog API",
            "description": "Create RESTful API endpoints for product CRUD operations, search functionality, and category management. Include image upload support.",
            "priority": 4,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Develop Shopping Cart",
            "description": "Implement shopping cart functionality with add/remove items, quantity management, and session persistence. Include cart-to-order conversion.",
            "priority": 4,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Integrate Payment Gateway",
            "description": "Integrate Stripe payment processing with support for credit cards and digital wallets. Include transaction history and refund capabilities.",
            "priority": 3,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Write Unit Tests",
            "description": "Create comprehensive unit tests for all API endpoints, business logic, and database operations. Target 90% code coverage.",
            "priority": 3,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Deploy to Production",
            "description": "Set up production environment with Docker, configure CI/CD pipeline, and implement monitoring and logging. Include security hardening.",
            "priority": 2,
            "status": "pending",
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "title": "Create Admin Dashboard",
            "description": "Build administrative interface for managing products, orders, users, and system settings. Include analytics and reporting features.",
            "priority": 2,
            "status": "pending",
            "created_at": datetime.utcnow()
        }
    ]

    return user_id, plan, tasks


async def test_ai_service():
    """Test the AI service with sample data."""
    print("🚀 Testing Gemini AI Integration with Mindmesh")
    print("=" * 50)

    # Check if API key is configured
    if settings.google_api_key == "[YOUR-GEMINI-API-KEY]":
        print("⚠️  WARNING: Gemini API key not configured!")
        print("Please add your API key to the .env file:")
        print("GOOGLE_API_KEY=your_actual_api_key_here")
        print("\nFor testing purposes, we'll continue with mocked responses...")

    # Create AI service instance
    ai_service = GeminiAIService()

    # Create sample data
    user_id, plan, tasks = create_sample_data()

    print(f"📋 Created sample plan: {plan['title']}")
    print(f"📝 Plan has {len(tasks)} tasks")
    print()

    try:
        # Test 1: Analyze user context (mocked)
        print("🔍 Test 1: Analyzing User Context")
        print("-" * 30)

        # Since we don't have a real database, we'll create a mock context
        mock_context = {
            "total_plans": 1,
            "plan_data": [{
                "title": plan["title"],
                "description": plan["description"],
                "status": plan["status"],
                "tasks": tasks
            }],
            "task_categories": [],
            "priority_distribution": {
                "high": 2,
                "medium_high": 2,
                "medium": 2,
                "medium_low": 1,
                "low": 1
            }
        }

        print(f"✅ User context analyzed:")
        print(f"   - Total plans: {mock_context['total_plans']}")
        print(f"   - High priority tasks: {mock_context['priority_distribution']['high']}")
        print(f"   - Medium priority tasks: {mock_context['priority_distribution']['medium_high'] + mock_context['priority_distribution']['medium']}")
        print(f"   - Low priority tasks: {mock_context['priority_distribution']['medium_low'] + mock_context['priority_distribution']['low']}")
        print()

        # Test 2: Task categorization
        print("📂 Test 2: Task Categorization")
        print("-" * 30)

        try:
            categorization_result = await ai_service.categorize_tasks(tasks, mock_context)

            print("✅ Tasks categorized successfully:")
            for category in categorization_result.get("categories", []):
                print(f"   📁 {category['name']}: {category['description']}")
                print(f"      Priority ranking: {category['priority_ranking']}/5")
                print(f"      Tasks: {len(category['tasks'])}")
            print(f"   📊 Categorized {len(categorization_result['categorized_tasks'])} out of {len(tasks)} tasks")
            print(f"   💡 Reasoning: {categorization_result.get('reasoning', 'N/A')}")

        except Exception as e:
            print(f"❌ Categorization failed: {str(e)}")
            print("   This is expected if API key is not configured")
        print()

        # Test 3: Priority scoring
        print("⭐ Test 3: Priority Scoring")
        print("-" * 30)

        try:
            # Use categorized tasks if available, otherwise use original tasks
            tasks_for_scoring = categorization_result.get("categorized_tasks", tasks)

            priority_result = await ai_service.score_priorities(tasks_for_scoring, mock_context)

            print("✅ Tasks prioritized successfully:")
            scored_tasks = priority_result.get("scored_tasks", [])
            for task in scored_tasks:
                print(f"   🎯 {task['title']}")
                print(f"      AI Priority Score: {task['ai_priority_score']}/10")
                print(f"      Estimated Effort: {task.get('estimated_effort', 'N/A')}")
                print(f"      Reasoning: {task.get('ai_reasoning', 'N/A')[:100]}...")
                print()

            print(f"💡 Recommendations:")
            for rec in priority_result.get("recommendations", []):
                print(f"   • {rec}")

        except Exception as e:
            print(f"❌ Priority scoring failed: {str(e)}")
            print("   This is expected if API key is not configured")
        print()

        # Test 4: Dashboard generation
        print("📊 Test 4: Dashboard Generation")
        print("-" * 30)

        try:
            dashboard_result = await ai_service.generate_dashboard_suggestion(plan["id"], mock_context)

            print("✅ Dashboard generated successfully:")
            dashboard_data = dashboard_result.get("dashboard_data", {})
            print(f"   📈 Title: {dashboard_data.get('dashboard_title', 'N/A')}")
            print(f"   📝 Summary: {dashboard_data.get('summary', 'N/A')}")
            print(f"   ⏱️  Estimated time: {dashboard_data.get('estimated_completion_time', 'N/A')}")

            print("   🗂️  Categories:")
            for category in dashboard_data.get("categories", []):
                print(f"      • {category['name']} (Priority: {category.get('priority_ranking', 'N/A')})")

            print("   🎯 Next Steps:")
            for step in dashboard_data.get("next_steps", []):
                print(f"      • {step}")

        except Exception as e:
            print(f"❌ Dashboard generation failed: {str(e)}")
            print("   This is expected if API key is not configured")
        print()

        # Test 5: Cost estimation
        print("💰 Test 5: Cost Estimation")
        print("-" * 30)

        # Test various token usage scenarios
        test_tokens = [100, 500, 1000, 2000]

        print("💡 Cost estimates for different token usages:")
        for tokens in test_tokens:
            cost = ai_service._estimate_cost(tokens)
            print(f"   📊 {tokens:,} tokens → ${cost:.4f}")

        print()
        print("🎉 Testing completed!")

    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


def display_sample_data():
    """Display the sample data structure."""
    user_id, plan, tasks = create_sample_data()

    print("📋 Sample Data Structure:")
    print("=" * 50)
    print(f"User ID: {user_id}")
    print()

    print("Plan:")
    print(json.dumps(plan, indent=2, default=str))
    print()

    print("Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']}")
        print(f"   Priority: {task['priority']}/5")
        print(f"   Description: {task['description'][:100]}...")
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Gemini AI integration with Mindmesh")
    parser.add_argument("--sample-data", action="store_true", help="Display sample data structure only")

    args = parser.parse_args()

    if args.sample_data:
        display_sample_data()
    else:
        asyncio.run(test_ai_service())