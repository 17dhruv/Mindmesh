#!/usr/bin/env python3
"""
Test with real user situation and confusion.
"""

import os
import sys
import asyncio
from uuid import uuid4
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service import GeminiAIService

async def analyze_user_situation():
    """Analyze the user's real confusing situation."""
    print("🧠 Analyzing User's Confusing Situation with Gemini AI")
    print("=" * 60)

    # Create AI service
    ai_service = GeminiAIService()

    # User's raw thought/feeling
    original_thought = """I'm really confused right now. I have my DAA exam in 6 days but I haven't revised DP properly.
Also need to finish my Mindmesh frontend landing page before next week.
At the same time I want to apply for 3 internships, but my resume is outdated.
There's also a group project meeting tomorrow evening which I almost forgot.
I feel like I should also go to the gym because I've been skipping it.
And I still haven't paid my hostel fees."""

    # Extract tasks from the user's thoughts
    user_tasks = [
        {
            "id": str(uuid4()),
            "title": "Revise DP for DAA Exam",
            "description": "Study Dynamic Programming thoroughly for DAA exam in 6 days - exam is very urgent and critical",
            "priority": 5,
            "status": "pending",
            "deadline_days": 6,
            "impact": "Academic performance, exam success"
        },
        {
            "id": str(uuid4()),
            "title": "Finish Mindmesh Frontend Landing Page",
            "description": "Complete frontend development for Mindmesh landing page - deadline next week",
            "priority": 4,
            "status": "pending",
            "deadline_days": 7,
            "impact": "Project completion, portfolio"
        },
        {
            "id": str(uuid4()),
            "title": "Update Resume for Internship Applications",
            "description": "Update and tailor resume to apply for 3 internships - career opportunities",
            "priority": 4,
            "status": "pending",
            "deadline_days": 10,
            "impact": "Career prospects, internships"
        },
        {
            "id": str(uuid4()),
            "title": "Attend Group Project Meeting",
            "description": "Tomorrow evening group project meeting - can't miss this one",
            "priority": 5,
            "status": "pending",
            "deadline_days": 1,
            "impact": "Team coordination, project success"
        },
        {
            "id": str(uuid4()),
            "title": "Go to Gym",
            "description": "Go to gym - been skipping lately, need to maintain health and energy levels",
            "priority": 3,
            "status": "pending",
            "deadline_days": 2,
            "impact": "Physical health, mental clarity"
        },
        {
            "id": str(uuid4()),
            "title": "Pay Hostel Fees",
            "description": "Pay overdue hostel fees - administrative priority, potential late fees",
            "priority": 4,
            "status": "pending",
            "deadline_days": 3,
            "impact": "Financial stability, avoid penalties"
        }
    ]

    print("📝 User's Situation:")
    print("-" * 30)
    print(original_thought)
    print()

    print("📋 Extracted Tasks:")
    print("-" * 30)
    for i, task in enumerate(user_tasks, 1):
        print(f"{i}. {task['title']}")
        print(f"   🎯 Priority: {task['priority']}/5")
        print(f"   ⏰ Deadline: {task['deadline_days']} days")
        print(f"   💭 Impact: {task['impact']}")
        print()

    # Mock user context
    mock_context = {
        "total_plans": 1,
        "plan_data": [],
        "task_categories": [],
        "priority_distribution": {
            "high": 2,
            "medium_high": 2,
            "medium": 1,
            "medium_low": 1,
            "low": 0
        },
        "current_situation": "Academic pressure with conflicting priorities",
        "time_constraint": "Very tight - multiple urgent deadlines"
    }

    try:
        print("🤖 AI Analysis Starting...")
        print("=" * 60)

        # Step 1: Categorize tasks
        print("📂 Step 1: Task Categorization")
        print("-" * 30)

        categorization_result = await ai_service.categorize_tasks(user_tasks, mock_context)

        categories = categorization_result.get("categories", [])
        for category in categories:
            print(f"📁 **{category['name']}**")
            print(f"   💭 {category['description']}")
            print(f"   🎯 Priority Ranking: {category['priority_ranking']}/5")

            # Show tasks in this category
            category_task_indices = category.get("tasks", [])
            for task_idx in category_task_indices:
                if 0 <= task_idx < len(user_tasks):
                    task = user_tasks[task_idx]
                    print(f"   → {task['title']} ({task['deadline_days']} days)")

        print(f"\n📊 **Categorization Reasoning:**")
        print(f"   {categorization_result.get('reasoning', 'N/A')}")
        print()

        # Step 2: Priority scoring
        print("⭐ Step 2: AI Priority Scoring")
        print("-" * 30)

        # Use categorized tasks if available
        tasks_for_scoring = categorization_result.get("categorized_tasks", user_tasks)
        priority_result = await ai_service.score_priorities(tasks_for_scoring, mock_context)

        scored_tasks = priority_result.get("scored_tasks", [])
        print("🎯 **AI-Recommended Priority Order:**")
        print()

        for i, task in enumerate(scored_tasks, 1):
            print(f"**{i}. {task.get('title', 'Unknown Task')}**")
            print(f"   📊 AI Priority Score: {task.get('ai_priority_score', 'N/A')}/10")
            print(f"   🧠 AI Reasoning: {task.get('ai_reasoning', 'N/A')}")
            print(f"   💪 Estimated Effort: {task.get('estimated_effort', 'N/A')}")
            print(f"   🎯 Impact Level: {task.get('impact_level', 'N/A')}")
            print()

        print("💡 **AI Recommendations:**")
        recommendations = priority_result.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        print()

        # Step 3: Dashboard generation
        print("📊 Step 3: Dashboard Suggestion")
        print("-" * 30)

        # Create a mock plan for dashboard generation
        plan_id = str(uuid4())
        dashboard_result = await ai_service.generate_dashboard_suggestion(plan_id, mock_context)

        dashboard_data = dashboard_result.get("dashboard_data", {})

        print("🎨 **AI-Generated Dashboard:**")
        print()
        print(f"📈 **Title:** {dashboard_data.get('dashboard_title', 'Personal Dashboard')}")
        print(f"📝 **Summary:** {dashboard_data.get('summary', 'No summary available')}")
        print(f"⏱️  **Estimated Completion Time:** {dashboard_data.get('estimated_completion_time', 'Unknown')}")
        print()

        print("🗂️ **Task Categories:**")
        for category in dashboard_data.get("categories", []):
            print(f"   • {category.get('name', 'Unnamed')} (Priority: {category.get('priority_ranking', 'N/A')})")

        print()
        print("🎯 **Priority Groups:**")
        priority_groups = dashboard_data.get("priority_groups", {})
        for group, tasks in priority_groups.items():
            print(f"   • {group.capitalize()}: {len(tasks)} tasks")

        print()
        print("📋 **Immediate Next Steps:**")
        for i, step in enumerate(dashboard_data.get("next_steps", []), 1):
            print(f"   {i}. {step}")
        print()

        print("=" * 60)
        print("🎉 **AI Analysis Complete!**")
        print()
        print("💡 **Key Insights:**")
        print("   • The AI understands your time pressure and multiple conflicting priorities")
        print("   • Tasks have been categorized by life areas (Academic, Career, Health, Administrative)")
        print("   • Priorities are scored based on urgency, impact, and dependencies")
        print("   • The system provides clear reasoning for each recommendation")
        print()
        print("🚀 **Next Steps:**")
        print("   1. Review the AI suggestions")
        print("   2. Approve the dashboard plan")
        print("   3. Start with the highest-priority tasks")
        print("   4. The system will track your progress and adjust recommendations")

        return True

    except Exception as e:
        print(f"❌ Error during AI analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(analyze_user_situation())