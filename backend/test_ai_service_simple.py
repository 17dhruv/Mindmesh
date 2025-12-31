#!/usr/bin/env python3
"""
Simple test of the AI service with real API calls.
"""

import os
import sys
import asyncio

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service import GeminiAIService

async def test_ai_service_simple():
    """Test AI service with simple tasks."""
    print("🚀 Testing AI Service with Real Gemini API")
    print("=" * 50)

    # Create AI service
    ai_service = GeminiAIService()

    # Simple test tasks
    test_tasks = [
        {
            "title": "Design Database Schema",
            "description": "Create normalized database schema for users, products, and orders",
            "priority": 5
        },
        {
            "title": "Build User Interface",
            "description": "Create responsive web interface for users to interact with the application",
            "priority": 4
        },
        {
            "title": "Write Documentation",
            "description": "Create comprehensive documentation for the API and user guide",
            "priority": 3
        }
    ]

    mock_context = {
        "task_categories": [],
        "priority_distribution": {"high": 1, "medium": 1, "low": 1}
    }

    print("📝 Test Tasks:")
    for i, task in enumerate(test_tasks, 1):
        print(f"   {i}. {task['title']} (Priority: {task['priority']})")
    print()

    # Test 1: Categorization
    print("📂 Test 1: Task Categorization")
    print("-" * 30)

    try:
        categorization_result = await ai_service.categorize_tasks(test_tasks, mock_context)
        print("✅ Categorization successful!")

        categories = categorization_result.get("categories", [])
        for category in categories:
            print(f"   📁 {category['name']}: {category['description']}")
            print(f"      Tasks: {len(category['tasks'])}")
            print(f"      Priority: {category['priority_ranking']}/5")

        categorized_count = len(categorization_result.get("categorized_tasks", 0))
        print(f"   📊 Categorized {categorized_count} out of {len(test_tasks)} tasks")
        print(f"   💡 Reasoning: {categorization_result.get('reasoning', 'N/A')}")

    except Exception as e:
        print(f"❌ Categorization failed: {str(e)}")
        import traceback
        traceback.print_exc()

    print()

    # Test 2: Priority Scoring
    print("⭐ Test 2: Priority Scoring")
    print("-" * 30)

    try:
        # Use categorized tasks if available, otherwise use original tasks
        tasks_for_scoring = categorization_result.get("categorized_tasks", test_tasks) if 'categorization_result' in locals() else test_tasks

        priority_result = await ai_service.score_priorities(tasks_for_scoring, mock_context)
        print("✅ Priority scoring successful!")

        scored_tasks = priority_result.get("scored_tasks", [])
        for task in scored_tasks:
            print(f"   🎯 {task['title']}")
            print(f"      Score: {task['ai_priority_score']}/10")
            print(f"      Effort: {task.get('estimated_effort', 'N/A')}")
            print(f"      Reasoning: {task.get('ai_reasoning', 'N/A')[:100]}...")

        recommendations = priority_result.get("recommendations", [])
        if recommendations:
            print("   💡 Recommendations:")
            for rec in recommendations:
                print(f"      • {rec}")

    except Exception as e:
        print(f"❌ Priority scoring failed: {str(e)}")
        import traceback
        traceback.print_exc()

    print()

    # Test 3: JSON extraction
    print("🔧 Test 3: JSON Extraction Test")
    print("-" * 30)

    try:
        test_responses = [
            '{"test": "direct json"}',
            '```json\n{"test": "json in code block"}\n```',
            'Some text\n{"test": "json in text"}\nMore text',
            '```json\n{"test": "json with spaces"}   \n```'
        ]

        for i, response in enumerate(test_responses, 1):
            extracted = ai_service._extract_json_from_response(response)
            print(f"   {i}. Response: {response}")
            print(f"      Extracted: {extracted}")
            print()

    except Exception as e:
        print(f"❌ JSON extraction test failed: {str(e)}")

    print("🎉 Simple AI Service Test Completed!")


if __name__ == "__main__":
    asyncio.run(test_ai_service_simple())