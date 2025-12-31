#!/usr/bin/env python3
"""
Debug JSON extraction specifically.
"""

import os
import sys
import re

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service import GeminiAIService

def debug_json_extraction():
    """Debug the JSON extraction with sample response."""
    print("🔧 Debugging JSON Extraction")
    print("=" * 50)

    ai_service = GeminiAIService()

    # Sample response that we know is problematic
    sample_response = '''```json
{
    "ranked_tasks": [
        {
            "task_index": 0,
            "ai_priority_score": 10,
            "reasoning": "This is a test"
        }
    ],
    "recommendations": ["Test recommendation"]
}
```'''

    print("📝 Sample response:")
    print(sample_response)
    print()

    print("🔍 Testing extraction patterns:")
    print("-" * 30)

    json_patterns = [
        (r'```json\s*\n(.*?)\n```', 'Pattern 1: ```json\\n...\\n```'),
        (r'```json\n(.*?)\n```', 'Pattern 2: ```json\\n...\\n``` (no space)'),
        (r'```\s*\n(.*?)\n```', 'Pattern 3: ```\\n...\\n``` (no lang)'),
        (r'```\n(.*?)\n```', 'Pattern 4: ```\\n...\\n``` (no lang, no space)'),
        (r'```json\s*(.*?)```', 'Pattern 5: ```json...```'),
        (r'```\s*(.*?)```', 'Pattern 6: ```...```')
    ]

    for pattern, description in json_patterns:
        match = re.search(pattern, sample_response, re.DOTALL | re.MULTILINE)
        if match:
            json_content = match.group(1).strip()
            print(f"✅ {description}")
            print(f"   Matched: '{json_content[:50]}...'")

            import json
            try:
                parsed = json.loads(json_content)
                print(f"   ✅ Valid JSON: {len(parsed.get('ranked_tasks', []))} tasks")
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON: {e}")
        else:
            print(f"❌ {description} - No match")

    print()
    print("🔧 Testing our extraction function:")
    print("-" * 30)

    extracted = ai_service._extract_json_from_response(sample_response)
    print(f"Extracted: '{extracted[:100]}...'")
    print(f"Length: {len(extracted)}")

    import json
    try:
        parsed = json.loads(extracted)
        print("✅ Successfully parsed!")
        print(f"Ranked tasks: {len(parsed.get('ranked_tasks', []))}")
    except json.JSONDecodeError as e:
        print(f"❌ Still failed to parse: {e}")

if __name__ == "__main__":
    debug_json_extraction()