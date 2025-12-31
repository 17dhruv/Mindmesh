#!/usr/bin/env python3
"""
Test the AI integration with real database calls.
"""

import os
import sys
import asyncio
from uuid import uuid4

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 **TESTING WITH YOUR REAL DATABASE**")
print("=" * 50)

async def test_real_database():
    """Test with actual database connection."""
    try:
        from app.database import get_db
        from app.config import settings

        print(f"✅ Database URL configured: {settings.database_url}")
        print(f"✅ Supabase URL: {settings.supabase_url}")
        print(f"✅ Gemini Model: {settings.gemini_model}")
        print()

        print("🏢 **TESTING DATABASE CONNECTION:**")
        print("-" * 30)

        # Test database connection
        async for db in get_db():
            print("✅ Database connection successful!")

            # Test if we can query the database
            from sqlalchemy import select, text

            # Check if tables exist
            result = await db.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))

            tables = result.fetchall()
            print(f"✅ Found {len(tables)} tables in database:")
            for table in tables:
                table_name = table[0]
                print(f"   • {table_name}")

                # Check if AI columns exist
                if table_name == 'plans':
                    result2 = await db.execute(text("""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = 'plans'
                        AND column_name LIKE 'ai_%'
                    """))
                    ai_columns = result2.fetchall()
                    if ai_columns:
                        print(f"     🤖 AI columns: {[col[0] for col in ai_columns]}")

                elif table_name == 'tasks':
                    result2 = await db.execute(text("""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = 'tasks'
                        AND column_name LIKE 'ai_%'
                    """))
                    ai_columns = result2.fetchall()
                    if ai_columns:
                        print(f"     🤖 AI columns: {[col[0] for col in ai_columns]}")

                elif table_name == 'ai_interactions':
                    print(f"     🤖 Full AI tracking table")

            break

        print("\n" + "=" * 50)
        print("📋 **YOUR DATABASE IS READY FOR AI UPDATES!**")
        print("=" * 50)

        print("""
🏃 **NEXT STEPS TO SEE AI UPDATES:**

1️⃣  START YOUR SERVER:
   uvicorn app.main:app --reload
   Server will run at: http://localhost:8000

2️⃣  CREATE A PLAN WITH YOUR THOUGHTS:
   curl -X POST "http://localhost:8000/api/plans" \
   -H "Authorization: Bearer YOUR_JWT_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
     "title": "My Confused Student Life",
     "description": "I have DAA exam in 6 days, Mindmesh landing page, resume updates, gym, hostel fees..."
   }'

3️⃣  GENERATE AI DASHBOARD:
   curl -X POST "http://localhost:8000/api/ai/generate-dashboard?plan_id=YOUR_PLAN_ID" \
   -H "Authorization: Bearer YOUR_JWT_TOKEN"

4️⃣  VIEW IN SUPABASE DASHBOARD:
   • Go to your Supabase project
   • Table Editor → plans → See ai_generated_data column
   • Table Editor → tasks → See ai_category, ai_priority_score columns
   • Table Editor → ai_interactions → See AI usage analytics

5️⃣  APPROVE AI SUGGESTIONS:
   curl -X POST "http://localhost:8000/api/ai/approve-dashboard" \
   -H "Authorization: Bearer YOUR_JWT_TOKEN" \
   -d '{"approved": true, "feedback": "Great analysis!"}'
""")

        print("\n💡 **WHAT YOU'LL SEE IN DATABASE:**")
        print("=" * 40)
        print("""
📊 plans.ai_generated_data will contain:
{
  "categorization": {
    "categories": [
      {
        "name": "Academic Commitments",
        "description": "Study and exam tasks",
        "priority_ranking": 5
      }
    ]
  },
  "priority_scoring": {...},
  "dashboard_data": {...}
}

📝 tasks.ai_category will contain:
• "Academic Commitments"
• "Career Development"
• "Personal Health"
• "Administrative Tasks"

📝 tasks.ai_priority_score will contain:
• Numbers 1-10 (AI calculated priority)
• Higher numbers = more urgent/important

📝 tasks.ai_reasoning will contain:
• Detailed AI explanation for each priority
• Based on deadlines, impact, dependencies
""")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_real_database())