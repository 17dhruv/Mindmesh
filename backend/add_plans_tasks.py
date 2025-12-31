#!/usr/bin/env python3
"""Add plans and tasks for existing users"""

import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import engine

async def add_plans_and_tasks():
    """Add plans and tasks for existing users"""
    async with engine.connect() as conn:
        try:
            # Get existing users
            users_result = await conn.execute(text("SELECT id, email FROM users"))
            users = users_result.fetchall()

            if not users:
                print("❌ No users found. Please create users first.")
                return

            print(f"✅ Found {len(users)} existing users")

            # Create 5 plans for existing users
            plans = []
            plan_titles = [
                "Build Mobile App MVP",
                "Learn Machine Learning",
                "Home Renovation Project",
                "Start YouTube Channel",
                "Plan Summer Vacation"
            ]

            for i, title in enumerate(plan_titles):
                plan_id = str(uuid.uuid4())
                user = users[i % len(users)]
                plans.append(plan_id)

                await conn.execute(text("""
                    INSERT INTO plans (id, user_id, title, description, status, created_at, updated_at)
                    VALUES (:id, :user_id, :title, :description, :status, :created_at, :updated_at)
                """), {
                    'id': plan_id,
                    'user_id': user.id,
                    'title': title,
                    'description': f'Detailed plan for {title.lower()}',
                    'status': 'active',
                    'created_at': datetime.utcnow() - timedelta(days=i*2),
                    'updated_at': datetime.utcnow()
                })

            await conn.commit()
            print("✅ Created 5 mock plans")

            # Create 10 tasks distributed across plans
            task_data = [
                ("Research market requirements", "Research and analyze market needs", 5),
                ("Design UI/UX mockups", "Create wireframes and designs", 5),
                ("Set up development environment", "Install tools and frameworks", 3),
                ("Build core functionality", "Implement main features", 5),
                ("Write unit tests", "Create test cases", 3),
                ("Deploy to staging", "Deploy to staging server", 2),
                ("Gather user feedback", "Collect and analyze feedback", 3),
                ("Create documentation", "Write user and developer docs", 2),
                ("Plan marketing strategy", "Design marketing approach", 3),
                ("Launch beta version", "Release beta to users", 5)
            ]

            for i, (title, description, priority) in enumerate(task_data):
                await conn.execute(text("""
                    INSERT INTO tasks (id, plan_id, title, description, priority, status, created_at, updated_at)
                    VALUES (:id, :plan_id, :title, :description, :priority, :status, :created_at, :updated_at)
                """), {
                    'id': str(uuid.uuid4()),
                    'plan_id': plans[i % len(plans)],
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'status': 'pending',
                    'created_at': datetime.utcnow() - timedelta(hours=i),
                    'updated_at': datetime.utcnow()
                })

            await conn.commit()
            print("✅ Created 10 mock tasks")

            # Verify final data count
            plans_count = await conn.execute(text("SELECT COUNT(*) FROM plans"))
            tasks_count = await conn.execute(text("SELECT COUNT(*) FROM tasks"))

            print("\n📊 Final Database Summary:")
            print(f"   Users: {len(users)}")
            print(f"   Plans: {plans_count.scalar()}")
            print(f"   Tasks: {tasks_count.scalar()}")
            print("\n✅ Mock data successfully added!")
            print("\n👉 You can now view this data in your Supabase dashboard!")

        except Exception as e:
            print(f"❌ Error: {e}")
            await conn.rollback()

if __name__ == "__main__":
    asyncio.run(add_plans_and_tasks())