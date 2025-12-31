#!/usr/bin/env python3
"""
Test priority scoring specifically.
"""

import os
import sys
import asyncio

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service import GeminiAIService

async def test_priority_scoring():
    """Test priority scoring with debug information."""
    print("⭐ Testing Priority Scoring with Debug")
    print("=" * 50)

    ai_service = GeminiAIService()

    test_tasks = [
        {
            "id": "1",
            "title": "Design Database Schema",
            "description": "Create normalized database schema for users, products, and orders",
            "priority": 5,
            "status": "pending",
            "ai_category": "Data Architecture"
        },
        {
            "id": "2",
            "title": "Build User Interface",
            "description": "Create responsive web interface for users to interact with the application",
            "priority": 4,
            "status": "pending",
            "ai_category": "Frontend Development"
        },
        {
            "id": "3",
            "title": "Write Documentation",
            "description": "Create comprehensive documentation for the API and user guide",
            "priority": 3,
            "status": "pending",
            "ai_category": "Technical Documentation"
        }
    ]

    mock_context = {
        "priority_distribution": {"high": 1, "medium": 1, "low": 1}
    }

    print("📝 Tasks for scoring:")
    for task in test_tasks:
        print(f"   • {task['title']} (Category: {task.get('ai_category', 'None')})")
    print()

    # Create the exact prompt that would be sent
    task_info = []
    for i, task in enumerate(test_tasks):
        task_info.append(
            f"Task {i+1}: {task['title']}\n"
            f"Description: {task['description']}\n"
            f"Category: {task.get('ai_category', 'No category')}\n"
            f"Current Priority: {task['priority']}"
        )

    prompt = f"""
    Analyze and rank the following tasks by priority. Consider:
    - User's historical priority patterns: {mock_context}
    - Task dependencies and logical flow
    - Estimated effort vs. impact
    - Urgency and importance

    Tasks to prioritize:

    {chr(10).join(task_info)}

    Provide a JSON response with this structure:
    {{
        "ranked_tasks": [
            {{
                "task_index": 0,
                "ai_priority_score": 1-10,
                "reasoning": "Specific reason for this priority",
                "estimated_effort": "Low/Medium/High",
                "dependencies": ["task_indices"],
                "impact_level": "Low/Medium/High"
            }}
        ],
        "recommendations": ["List of priority recommendations"]
    }}

    Scoring guidelines:
    - 1-3: Low priority (can be deferred)
    - 4-6: Medium priority (important but not urgent)
    - 7-8: High priority (important and somewhat urgent)
    - 9-10: Critical priority (urgent and critical)
    """

    print("🔍 Sending this prompt to Gemini:")
    print("-" * 30)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print("-" * 30)
    print()

    try:
        # Test the actual Gemini API call
        print("📡 Calling Gemini API...")
        response = await ai_service._generate_content(prompt)
        print(f"✅ Got response (length: {len(response)})")
        print(f"Response type: {type(response)}")
        print(f"First 200 chars: {response[:200]}...")
        print()

        # Test JSON extraction
        print("🔧 Testing JSON extraction...")
        json_response = ai_service._extract_json_from_response(response)
        print(f"✅ Extracted JSON (length: {len(json_response)})")
        print(f"Extracted JSON: {json_response[:300]}...")
        print()

        # Try to parse
        import json
        ai_result = json.loads(json_response)
        print("✅ Successfully parsed JSON!")

        ranked_tasks = ai_result.get("ranked_tasks", [])
        recommendations = ai_result.get("recommendations", [])

        print(f"📊 Results:")
        print(f"   Ranked tasks: {len(ranked_tasks)}")
        print(f"   Recommendations: {len(recommendations)}")

        for task_score in ranked_tasks:
            task_idx = task_score.get("task_index", 0)
            print(f"   Task {task_idx + 1}: Score {task_score.get('ai_priority_score', 'N/A')}/10")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_priority_scoring())