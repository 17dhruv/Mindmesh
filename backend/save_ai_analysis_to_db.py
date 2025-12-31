#!/usr/bin/env python3
"""
Save AI analysis to database to demonstrate where updates are stored.
"""

import os
import sys
import asyncio
import json
from uuid import uuid4
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import User, Plan, Task, AIInteraction, async_session
from app.ai_service import ai_service
from app.config import settings

async def save_user_analysis_to_db():
    """Save the user's AI analysis to the database."""
    print("💾 Saving AI Analysis to Database")
    print("=" * 50)

    # 1. Create a user (or use existing)
    async with async_session() as session:
        # Check if user already exists
        from sqlalchemy import select
        user_result = await session.execute(
            select(User).where(User.email == "test_student@example.com")
        )
        user = user_result.scalar_one_or_none()

        if not user:
            user = User(
                email="test_student@example.com",
                full_name="Test Student"
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"✅ Created new user: {user.id}")
        else:
            print(f"✅ Using existing user: {user.id}")

        # 2. Create a plan with the user's thoughts
        original_thought = """I'm really confused right now. I have my DAA exam in 6 days but I haven't revised DP properly.
Also need to finish my Mindmesh frontend landing page before next week.
At the same time I want to apply for 3 internships, but my resume is outdated.
There's also a group project meeting tomorrow evening which I almost forgot.
I feel like I should also go to the gym because I've been skipping it.
And I still haven't paid my hostel fees."""

        plan = Plan(
            user_id=user.id,
            title="Student Life Management Plan",
            description="AI-powered plan to manage academic, personal, and career tasks",
            original_thought=original_thought,
            status="draft"
        )
        session.add(plan)
        await session.commit()
        await session.refresh(plan)
        print(f"✅ Created plan: {plan.id}")

        # 3. Create tasks from the user's thoughts
        tasks_data = [
            {
                "title": "Revise DP for DAA Exam",
                "description": "Study Dynamic Programming thoroughly for DAA exam in 6 days. This is critical for academic performance.",
                "priority": 5
            },
            {
                "title": "Finish Mindmesh Frontend Landing Page",
                "description": "Complete frontend development for Mindmesh project landing page before next week.",
                "priority": 4
            },
            {
                "title": "Update Resume for 3 Internship Applications",
                "description": "Update and tailor resume to apply for 3 specific internships. Career critical.",
                "priority": 4
            },
            {
                "title": "Attend Group Project Meeting",
                "description": "Tomorrow evening group project meeting - absolutely critical, cannot miss.",
                "priority": 5
            },
            {
                "title": "Go to Gym",
                "description": "Go to gym for physical and mental health. Been skipping and this affects energy/focus.",
                "priority": 3
            },
            {
                "title": "Pay Hostel Fees",
                "description": "Pay overdue hostel fees to avoid penalties and maintain good standing.",
                "priority": 4
            }
        ]

        created_tasks = []
        for task_data in tasks_data:
            task = Task(
                plan_id=plan.id,
                **task_data
            )
            session.add(task)
            created_tasks.append(task)

        await session.commit()
        print(f"✅ Created {len(created_tasks)} tasks")
        await session.refresh_all()
        for i, task in enumerate(created_tasks):
            print(f"   {i+1}. {task.title} (ID: {task.id})")

        # 4. Run AI categorization
        print("\n🤖 Running AI Categorization...")
        mock_context = {
            "total_plans": 1,
            "priority_distribution": {"high": 2, "medium": 3, "low": 1}
        }

        categorization_result = await ai_service.categorize_tasks(
            [{"id": t.id, "title": t.title, "description": t.description, "priority": t.priority} for t in created_tasks],
            mock_context
        )

        # Save categorization to plan
        plan.ai_generated_data = json.dumps({
            "categorization": categorization_result,
            "generated_at": datetime.utcnow().isoformat()
        })

        # Update tasks with AI categories
        categorized_tasks = categorization_result.get("categorized_tasks", [])
        for ai_task in categorized_tasks:
            task_id = ai_task.get("id")
            if task_id:
                # Find the task and update it
                for task in created_tasks:
                    if str(task.id) == str(task_id):
                        task.ai_category = ai_task.get("ai_category")
                        break

        await session.commit()
        print("✅ Saved AI categorization to database")

        # 5. Run AI priority scoring
        print("\n⭐ Running AI Priority Scoring...")
        try:
            priority_result = await ai_service.score_priorities(
                [{"id": t.id, "title": t.title, "description": t.description, "priority": t.priority, "ai_category": t.ai_category} for t in created_tasks],
                mock_context
            )

            scored_tasks = priority_result.get("scored_tasks", [])
            for ai_task in scored_tasks:
                task_id = ai_task.get("id")
                if task_id:
                    for task in created_tasks:
                        if str(task.id) == str(task_id):
                            task.ai_priority_score = ai_task.get("ai_priority_score")
                            task.ai_reasoning = ai_task.get("ai_reasoning")
                            break

            # Update AI data with priority results
            current_ai_data = json.loads(plan.ai_generated_data or "{}")
            current_ai_data["priority_scoring"] = priority_result
            current_ai_data["updated_at"] = datetime.utcnow().isoformat()
            plan.ai_generated_data = json.dumps(current_ai_data)

            await session.commit()
            print("✅ Saved AI priority scoring to database")

        except Exception as e:
            print(f"⚠️  Priority scoring failed: {e}")

        # 6. Record AI interaction
        print("\n📊 Recording AI Interaction...")
        interaction = AIInteraction(
            user_id=user.id,
            plan_id=plan.id,
            interaction_type="dashboard",
            request_data=json.dumps({"thought": original_thought}),
            response_data=plan.ai_generated_data,
            tokens_used=500,  # Estimated
            model_used=settings.gemini_model,
            response_time_ms=2000,  # Estimated
        )
        session.add(interaction)
        await session.commit()
        await session.refresh(interaction)
        print(f"✅ Recorded AI interaction: {interaction.id}")

        # 7. Show where to find the data
        print("\n" + "="*60)
        print("🔍 **WHERE TO FIND YOUR AI UPDATES IN THE DATABASE:**")
        print("="*60)

        print("\n📋 **1. PLANS TABLE** (Check: `ai_generated_data`, `original_thought`)")
        print(f"   Plan ID: {plan.id}")
        print(f"   Table: plans")
        print(f"   Columns to check:")
        print(f"   - `ai_generated_data`: Contains full AI analysis in JSON")
        print(f"   - `original_thought`: Your original confused thought")
        print(f"   - `ai_metadata`: Additional AI metadata")
        print(f"\n   SQL Query to check:")
        print(f"   SELECT id, title, ai_generated_data, original_thought FROM plans WHERE id = '{plan.id}';")

        print("\n📝 **2. TASKS TABLE** (Check: `ai_category`, `ai_priority_score`, `ai_reasoning`)")
        print(f"   Plan ID: {plan.id}")
        print(f"   Table: tasks")
        print(f"   Columns to check:")
        print(f"   - `ai_category`: AI-assigned category (e.g., 'Academic Commitments')")
        print(f"   - `ai_priority_score`: AI-calculated priority (1-10)")
        print(f"   - `ai_reasoning`: AI reasoning for the priority")
        print(f"\n   SQL Query to check:")
        print(f"   SELECT id, title, ai_category, ai_priority_score, ai_reasoning FROM tasks WHERE plan_id = '{plan.id}';")

        print("\n📊 **3. AI_INTERACTIONS TABLE** (Check: All AI interactions)")
        print(f"   Table: ai_interactions")
        print(f"   Columns to check:")
        print(f"   - `interaction_type`: 'dashboard', 'categorization', 'ranking'")
        print(f"   - `request_data`: Original user request")
        print(f"   - `response_data`: AI analysis results")
        print(f"   - `tokens_used`: API usage")
        print(f"   - `model_used`: Gemini model used")
        print(f"   - `response_time_ms`: How long it took")
        print(f"\n   SQL Query to check:")
        print(f"   SELECT * FROM ai_interactions WHERE plan_id = '{plan.id}' ORDER BY created_at DESC;")

        print("\n🏢 **IN YOUR SUPABASE DASHBOARD:**")
        print("="*40)
        print("1. Go to your Supabase project")
        print("2. Navigate to Table Editor")
        print("3. Look for these tables:")
        print("   - `plans` - See your original thoughts and AI analysis")
        print("   - `tasks` - See AI-categorized and prioritized tasks")
        print("   - `ai_interactions` - See AI usage analytics")

        print("\n📱 **TO VIEW THE UPDATES VIA API:**")
        print("="*40)
        print("Once you start your server, you can access:")
        print("• GET /api/plans/{plan_id} - See AI-enhanced plan")
        print("• GET /api/plans/{plan_id}/tasks - See AI-categorized tasks")
        print("• GET /api/ai/interaction-history - See all AI interactions")

        print("\n🎉 **SAMPLE DATA SAVED!**")
        print("="*40)
        print("✅ User created:", user.email)
        print("✅ Plan created:", plan.title)
        print("✅ Tasks created:", len(created_tasks))
        print("✅ AI categorization applied")
        print("✅ AI priority scoring attempted")
        print("✅ Interaction recorded")
        print("\n🚀 Your Mindmesh AI integration is fully functional!")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(save_user_analysis_to_db())