#!/usr/bin/env python3
"""
Test with actual response from Gemini.
"""

import os
import sys
import json
import asyncio

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service import GeminiAIService

async def test_actual_response():
    """Test with actual Gemini response."""
    print("🔍 Testing Actual Gemini Response")
    print("=" * 50)

    ai_service = GeminiAIService()

    # Get actual response from Gemini
    test_tasks = [
        {
            "id": "1",
            "title": "Design Database Schema",
            "description": "Create normalized database schema",
            "priority": 5,
            "ai_category": "Data Architecture"
        }
    ]

    mock_context = {"priority_distribution": {"high": 1}}

    # Create a simplified prompt
    task_info = f"Task 1: {test_tasks[0]['title']}\nDescription: {test_tasks[0]['description']}\nCategory: {test_tasks[0]['ai_category']}\nCurrent Priority: {test_tasks[0]['priority']}"

    prompt = f"""
    Analyze and rank the following task:

    {task_info}

    Provide a JSON response with this structure:
    {{
        "ranked_tasks": [
            {{
                "task_index": 0,
                "ai_priority_score": 1-10,
                "reasoning": "Reasoning for priority"
            }}
        ],
        "recommendations": ["Recommendation"]
    }}
    """

    try:
        response = await ai_service._generate_content(prompt)
        print("📡 Raw response from Gemini:")
        print("-" * 30)
        print(repr(response))
        print()
        print("📝 Response content:")
        print("-" * 30)
        print(response)
        print()

        print("🔧 Extracting JSON...")
        extracted = ai_service._extract_json_from_response(response)
        print("📝 Extracted content:")
        print("-" * 30)
        print(repr(extracted))
        print()
        print("📝 Extracted content (readable):")
        print("-" * 30)
        print(extracted)
        print()

        try:
            parsed = json.loads(extracted)
            print("✅ Successfully parsed JSON!")
            print(f"Ranked tasks: {len(parsed.get('ranked_tasks', []))}")

            # Display the parsed data
            for task in parsed.get('ranked_tasks', []):
                print(f"   Task {task['task_index'] + 1}: Score {task['ai_priority_score']}/10")
                print(f"   Reasoning: {task['reasoning']}")

            return True

        except json.JSONDecodeError as e:
            print(f"❌ JSON parse failed: {e}")
            print(f"Error position: {e.pos if hasattr(e, 'pos') else 'N/A'}")

            # Try to find the issue
            print("\n🔍 Looking for issues...")
            if extracted.startswith('```'):
                print("   Still starts with markdown block")
            elif not extracted.startswith('{'):
                print(f"   Doesn't start with JSON object, starts with: {extracted[:20]}")

            return False

    except Exception as e:
        print(f"❌ Error getting response: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_actual_response())