#!/usr/bin/env python3
"""
Direct test of Gemini API to debug response issues.
"""

import os
import sys
import json

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings

def test_gemini_direct():
    """Test Gemini API directly to see what's happening."""
    print("🔍 Testing Gemini API directly...")
    print("=" * 50)

    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.google_api_key)

        print(f"✅ Using model: {settings.gemini_model}")
        print(f"✅ Temperature: {settings.gemini_temperature}")
        print(f"✅ Max tokens: {settings.gemini_max_tokens}")
        print()

        # Create model
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config={
                "temperature": settings.gemini_temperature,
                "max_output_tokens": settings.gemini_max_tokens,
            }
        )

        # Test 1: Simple text generation
        print("📝 Test 1: Simple text generation")
        print("-" * 30)

        prompt1 = "Hello, can you respond with a simple greeting?"
        response1 = model.generate_content(prompt1)
        print(f"Response: {response1.text}")
        print(f"Response type: {type(response1.text)}")
        print()

        # Test 2: JSON generation
        print("📝 Test 2: JSON generation")
        print("-" * 30)

        prompt2 = '''Generate a JSON response with this structure:
        {
            "categories": [
                {
                    "name": "Development",
                    "description": "Development tasks",
                    "tasks": [0, 1],
                    "priority_ranking": 5
                }
            ],
            "reasoning": "Test reasoning"
        }'''

        response2 = model.generate_content(prompt2)
        print(f"Response: {response2.text}")
        print(f"Response type: {type(response2.text)}")

        # Try to parse as JSON
        try:
            parsed = json.loads(response2.text)
            print("✅ Successfully parsed as JSON")
            print(f"Parsed: {parsed}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("Trying to extract JSON from response...")

            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response2.text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                print(f"Extracted JSON: {json_str}")
                try:
                    parsed = json.loads(json_str)
                    print("✅ Successfully parsed extracted JSON")
                    print(f"Parsed: {parsed}")
                except json.JSONDecodeError as e2:
                    print(f"❌ Still failed to parse extracted JSON: {e2}")
            else:
                print("❌ No JSON found in response")

        print()

        # Test 3: Our categorization prompt
        print("📝 Test 3: Our categorization prompt")
        print("-" * 30)

        tasks = [
            {
                "title": "Design Database Schema",
                "description": "Create database structure",
                "priority": 5
            },
            {
                "title": "Write Tests",
                "description": "Create test suite",
                "priority": 4
            }
        ]

        task_info = []
        for i, task in enumerate(tasks):
            task_info.append(
                f"Task {i+1}: {task['title']}\n"
                f"Description: {task['description']}\n"
                f"Priority: {task['priority']}"
            )

        prompt3 = f"""
        Analyze the following tasks and group them into logical categories.

        Tasks to categorize:

        {chr(10).join(task_info)}

        Provide a JSON response with this structure:
        {{
            "categories": [
                {{
                    "name": "Category Name",
                    "description": "Brief description",
                    "tasks": [task_indices],
                    "priority_ranking": 1-5
                }}
            ],
            "reasoning": "Explanation"
        }}

        Guidelines:
        - Create 2-3 meaningful categories
        - Each task should belong to exactly one category
        - Categories should be logical and actionable
        - Priority ranking: 1 (lowest) to 5 (highest category)
        """

        response3 = model.generate_content(prompt3)
        print(f"Response: {response3.text}")
        print(f"Response type: {type(response3.text)}")
        print(f"Response length: {len(response3.text)}")

        # Try to parse as JSON
        try:
            parsed = json.loads(response3.text)
            print("✅ Successfully parsed categorization response as JSON")
            print(f"Categories: {len(parsed.get('categories', []))}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            # Try to extract JSON
            json_match = re.search(r'\{.*\}', response3.text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                try:
                    parsed = json.loads(json_str)
                    print("✅ Successfully parsed extracted JSON")
                    print(f"Categories: {len(parsed.get('categories', []))}")
                except json.JSONDecodeError as e2:
                    print(f"❌ Still failed to parse extracted JSON: {e2}")
                    print(f"Extracted JSON: {json_str[:200]}...")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini_direct()
    if success:
        print("\n🎉 Direct Gemini API test completed!")
    else:
        print("\n❌ Direct Gemini API test failed!")